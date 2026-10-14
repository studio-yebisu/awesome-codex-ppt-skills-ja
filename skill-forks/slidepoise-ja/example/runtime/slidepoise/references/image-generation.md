# Image generation

Use the compiled generation request as the common boundary for native image tools, MCP tools, other authorised integrations and manual generation. The host Agent handles discovery and invocation. SlidePoise checks input bindings and packages files. It never infers image capability from the host's name or silently substitutes deterministic drawing.

## Configure through conversation

Read `slidepoise generation show` for saved preferences. For a presentation already in progress, read `slidepoise generation show --run <run>` and the resolved configuration. Ask only when the choice is material or unclear.

- Automatic is the default. Discover suitable capabilities in the current conversation and use one that meets the request.
- A selected tool is an explicit preference. Resolve its actual tool identifier with the user and save it. If unavailable, explain what needs connecting or offer manual generation. Never silently switch providers.
- Manual means the Agent supplies the exact prompt and ordered references. The user generates the image and returns the original file. Continue planning and other independent work while waiting, then inspect the returned image before reconstruction.

Use `slidepoise generation configure --mode manual` to save a default, or add `--run <run>` to change just this presentation. Use `--mode auto` to return to discovery. To bind a tool, use `--mode tool --tool <actual-tool-id>`. Optional `--model` and `--instructions` record user preferences. An empty string clears either field. The Console's System page edits these same defaults. Global changes apply to new presentations. For the current presentation, set its override explicitly and resolve its configuration again before compiling the next request.

Never put credentials in preferences, prompts or handoff bundles. Configure authentication in the provider's own integration. A provider URL or model name alone does not establish a working connection.

## Discover and select

Inspect native tools first, then discover connected image tools through the host's tool search, MCP inventory and relevant installed skills. Consider all suitable options against the requested model, attachments, editing requirements and output. A native tool has no automatic quality advantage over an MCP tool.

Read tool descriptions and schemas. Confirm image generation versus image search, image input support, edit support, available models, prompt and attachment limits, and alpha output for transparent edits. Some native tools have no model selector. Respect that interface and do not claim a specific model was used without evidence. Unknown limits are unknown, not unlimited. Never truncate the compiled prompt or drop a reference to fit a tool. Resolve the capacity issue upstream or choose a suitable integration with the user's preferences intact.

The Agent may record the current inventory in a run-local file, using the tool IDs it actually discovered. This is an observation of this conversation, not a permanent provider registry. For example, each entry in `tools` has `id`, `available`, `operations` (generate and/or edit), `reference_images`, optional `models`, optional `max_prompt_chars`, optional `max_reference_images`, and optional `transparent_background`. Read the actual schema to fill these facts. Do not copy an example ID and pretend the tool exists.

Run `slidepoise generation route --request <request.json> --capabilities <inventory.json>`. It reports compatibility facts without ranking design quality. Choose a tool using the task requirements and its documented capability, then pass `--tool <id>` to check the choice. Recheck availability when reconnecting, resuming in another host or after a tool failure.

Invoke the selected tool through the host with the exact `prompt` and ordered `reference_images`. Adapt field names to the tool's schema, preserving image order, content and required canvas proportions. Record the tool, model when known, source request and returned image in the run's generation evidence. Inspect the returned image. Successful tool execution does not establish visual acceptance.

When no suitable tool is available, offer to connect one or use manual generation. Do not force manual mode without the user's choice. Stop only the dependent image work while that decision is pending.

## Manual exchange

Compile the normal generation request first. Then run

```bash
slidepoise generation export --request <generation-request.json> --output <new-handoff-folder>
```

Give the user the generated `image-generation.zip`, a visible copy of its `prompt.txt` and the reference files when the host supports individual attachments. The ZIP contains instructions, the exact prompt, numbered references and portable request details. Explain that the references are attached in number order and that they should return the downloaded image file. If they choose another model with different limits, help adapt the source inputs and compile again before exporting.

Keep the local handoff folder. It binds the exchange to the original request and source files. When the user returns an image, run

```bash
slidepoise generation import --handoff <handoff-folder> --image <returned-image> --output <new-candidate.png>
```

Import checks that the request and references remain current, reads the returned image and records file facts. It does not accept the image or infer that it depicts the requested slide. Inspect it against the intent, source assets, content canvas and shared deck decisions. If a returned image has the wrong framing, use the existing visually authored canvas-normalisation route or request a corrected image. Reconstruct through the same semantic map, OpenCV and compiler as an automatically generated candidate.

If the plan or references changed while waiting, recompile and export a new exchange. Keep the old candidate as a record. Never refresh hashes to disguise stale inputs.

## Edits and transparent illustrations

`prepare_image_edit.py` produces requests for focused slide corrections. Route or export these with the same commands. The current candidate is the first attachment.

`prepare_illustration_refinement.py` also emits a `.request.json` and `.edit.txt` beside each source crop. Each request carries only its own illustration. Use these for native, MCP or manual edits. Transparent requests require actual alpha output. If the chosen provider cannot supply it, explain the limitation and retain a suitable original crop or agree on another provider. Do not make optional refinement block an otherwise usable illustration.

After import or tool return, inspect edges on contrasting backgrounds and at slide size, then follow `illustration-refinement.md` to register and apply the reviewed artwork. The same checks apply regardless of where the image was generated.
