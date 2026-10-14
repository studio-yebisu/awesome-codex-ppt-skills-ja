#!/usr/bin/env python3
"""Route verified image requests or carry them through a manual generation exchange."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

from PIL import Image, ImageOps

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'runtime/src'))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'runtime/scripts'))
from slidepoise.generation import compatible_tools, resolve_preferences
from prepare_generation import file_binding, load, verify_request
from prepare_image_edit import verify_edit_request
from raster_sources import image_facts, validate_background


def verified(path):
    purpose = load(path).get('purpose')
    if purpose == 'host_image_generation_request':
        return verify_request(path)
    if purpose == 'host_image_edit_request':
        return verify_edit_request(path)
    if purpose == 'host_illustration_edit_request':
        request = load(path)
        for record in [*request['input_bindings'].values(), *request['reference_images']]:
            if file_binding(Path(record['path']))['sha256'] != record['sha256']:
                raise ValueError('Illustration inputs changed. Prepare a new request.')
        if request['prompt'] != Path(request['input_bindings']['brief']['path']).read_text(encoding='utf-8'):
            raise ValueError('Illustration prompt differs from its compiled brief')
        if hashlib.sha256(request['prompt'].encode()).hexdigest() != request['prompt_sha256']:
            raise ValueError('Illustration prompt binding changed')
        return request
    raise ValueError('Use a compiled slide, image edit or illustration request')


def request_settings(request):
    if request['purpose'] == 'host_image_edit_request':
        request = verified(Path(request['input_bindings']['generation_request']['path']))
    config = load(Path(request['input_bindings']['config']['path']))
    return resolve_preferences(config.get('generation', {}))


def route(path, inventory, chosen=None):
    request = verified(path)
    settings = request_settings(request)
    if settings['mode'] == 'manual':
        return {'mode': 'manual', 'next_action': 'Export the prompt and references for the user.'}
    checks = compatible_tools(request, inventory, settings)
    selected = settings['tool'] if settings['mode'] == 'tool' else chosen
    if settings['mode'] == 'tool' and chosen and chosen != selected:
        raise ValueError('The selected tool differs from the saved preference. Update the preference first.')
    eligible = [item['id'] for item in checks if item['compatible']]
    if selected and selected not in eligible:
        return {'mode': settings['mode'], 'selected_tool': selected, 'available': False, 'tools': checks,
                'next_action': 'Resolve the selected tool or ask the user to choose another tool or manual generation.'}
    return {'mode': settings['mode'], 'selected_tool': selected, 'available': bool(eligible), 'tools': checks,
            'model': settings['model'] or None, 'instructions': settings['instructions'],
            'request': str(path.resolve()), 'next_action': 'The Agent calls the selected compatible tool with the exact prompt and ordered references.' if selected else
            'The Agent chooses among compatible tools using their descriptions and the slide requirements. If none are available, offer manual generation.'}


def export_bundle(path, output):
    request = verified(path)
    output = output.expanduser().resolve()
    if output.exists():
        raise ValueError('This handoff folder already exists. Use a new folder to preserve the previous exchange.')
    inputs = [path, *[Path(r['path']) for r in request['reference_images']]]
    if any(p.resolve().is_relative_to(output) for p in inputs):
        raise ValueError('The handoff folder must be separate from its input files')
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=output.parent, prefix='.image-handoff-') as temporary:
        stage = Path(temporary) / 'handoff'
        bundle = stage / 'bundle'
        bundle.mkdir(parents=True)
        (bundle / 'prompt.txt').write_bytes(request['prompt'].encode('utf-8'))
        attachments = []
        for number, reference in enumerate(request['reference_images'], 1):
            source = Path(reference['path'])
            name = re.sub(r'[^a-zA-Z0-9_-]', '-', reference.get('id', 'reference'))[:60]
            target = bundle / 'references' / f'{number:02d}-{name}{source.suffix.lower()}'
            target.parent.mkdir(exist_ok=True)
            shutil.copyfile(source, target)
            if file_binding(target)['sha256'] != reference['sha256']:
                raise ValueError('A reference changed during export. Prepare the request again.')
            attachments.append({'file': target.relative_to(bundle).as_posix(), 'purpose': reference.get('purpose', ''),
                                'sha256': reference['sha256']})
        settings = request_settings(request)
        portable = {'operation': request['purpose'], 'canvas': request['canvas'], 'background': request.get('background'),
                    'model': settings['model'] or None, 'instructions': settings['instructions'], 'references': attachments}
        (bundle / 'request.json').write_text(json.dumps(portable, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
        lines = ['# Generate the image', '', '1. Open your image generator and attach the reference files in the order below.',
                 '2. Copy all of prompt.txt into the prompt field. Keep the specified canvas proportions.',
                 '3. Download the original image file and return it to the Agent in this conversation.', '',
                 'If your generator cannot accept the prompt or all the references, tell the Agent before changing them.', '',
                 'The Agent will inspect the returned image and continue building the PowerPoint.', '', '## Attachments', '']
        lines += [f"{i}. `{item['file']}` {item['purpose']}" for i, item in enumerate(attachments, 1)] or ['No image attachments are required.']
        if settings['model']:
            lines += ['', f"Selected model {settings['model']}"]
        if settings['instructions']:
            lines += ['', settings['instructions']]
        (bundle / 'README.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
        hashes = {p.relative_to(bundle).as_posix(): file_binding(p)['sha256'] for p in sorted(bundle.rglob('*')) if p.is_file()}
        archive_path = stage / 'image-generation.zip'
        with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as archive:
            for name in hashes:
                archive.write(bundle / name, name)
        receipt = {'schema_version': '1.0', 'request': file_binding(path), 'files': hashes,
                   'archive_sha256': file_binding(archive_path)['sha256']}
        (stage / 'handoff.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
        verified(path)
        stage.rename(output)
    return {'folder': str(output), 'bundle': str(output / 'image-generation.zip'), 'prompt': str(output / 'bundle/prompt.txt'),
            'reference_count': len(attachments)}


def import_result(handoff, image, output):
    handoff, image, output = handoff.resolve(), image.resolve(), output.resolve()
    receipt = load(handoff / 'handoff.json')
    if receipt.get('schema_version') != '1.0' or file_binding(Path(receipt['request']['path'])) != receipt['request']:
        raise ValueError('The generation request changed after export. Prepare a new handoff.')
    request = verified(Path(receipt['request']['path']))
    for name, digest in receipt['files'].items():
        source = (handoff / 'bundle' / name).resolve()
        if not source.is_relative_to(handoff / 'bundle') or file_binding(source)['sha256'] != digest:
            raise ValueError('The exported prompt or references changed. Prepare a new handoff.')
    if file_binding(handoff / 'image-generation.zip')['sha256'] != receipt['archive_sha256']:
        raise ValueError('The exported archive changed. Prepare a new handoff.')
    record_path = output.with_suffix(output.suffix + '.json')
    if output.exists() or record_path.exists():
        raise ValueError('The output already exists. Use a new candidate filename.')
    if output.suffix.lower() != '.png':
        raise ValueError('Use a .png filename for the returned candidate')
    with Image.open(image) as candidate:
        candidate.load()
        rgba = ImageOps.exif_transpose(candidate).convert('RGBA')
        alpha = rgba.getchannel('A').getextrema()
        if request.get('background') == 'transparent':
            validate_background(image_facts(image), 'transparent')
        output.parent.mkdir(parents=True, exist_ok=True)
        rgba.save(output, icc_profile=candidate.info.get('icc_profile'))
    facts = {'request': receipt['request'], 'returned_file': file_binding(image), 'candidate': file_binding(output),
             'dimensions_px': list(rgba.size), 'alpha_range': list(alpha), 'requested_canvas': request['canvas'],
             'review_required': 'Inspect content, canvas proportions, references and visual fidelity before reconstruction. File import does not accept the design.'}
    record_path.write_text(json.dumps(facts, indent=2) + '\n', encoding='utf-8')
    return facts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    actions = parser.add_subparsers(dest='action', required=True)
    call = actions.add_parser('route')
    call.add_argument('--request', type=Path, required=True)
    call.add_argument('--capabilities', type=Path)
    call.add_argument('--tool')
    export = actions.add_parser('export')
    export.add_argument('--request', type=Path, required=True)
    export.add_argument('--output', type=Path, required=True)
    result = actions.add_parser('import')
    result.add_argument('--handoff', type=Path, required=True)
    result.add_argument('--image', type=Path, required=True)
    result.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.action == 'route':
            value = route(args.request, load(args.capabilities) if args.capabilities else {'tools': []}, args.tool)
        elif args.action == 'export':
            value = export_bundle(args.request, args.output)
        else:
            value = import_result(args.handoff, args.image, args.output)
        print(json.dumps(value, indent=2, ensure_ascii=False))
    except (ValueError, OSError, KeyError) as error:
        parser.exit(1, f'{error}\n')


if __name__ == '__main__':
    main()
