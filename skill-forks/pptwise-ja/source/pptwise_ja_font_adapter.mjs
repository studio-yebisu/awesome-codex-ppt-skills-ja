// Local font allowlist adapter for the exact original 0.44.0 source-built CLI.
// Original files, layout methods and PPTX bytes are not patched on disk.
import {registerHooks} from 'node:module';
import {createHash} from 'node:crypto';
import {pathToFileURL} from 'node:url';
const cli=process.argv[2];
if(!cli) throw new Error('Pass the fixed original cli.js path first.');
const originalChunkHash='36c3b6ef31a0e36b5814e357e8033b12ae61f9e90537b0ddb6e54c7b19df2d1e';
registerHooks({load(url,context,nextLoad){
 const result=nextLoad(url,context);
 if(!url.endsWith('/chunk-DQABTUNM.js')) return result;
 const source=Buffer.from(result.source).toString('utf8');
 if(createHash('sha256').update(source).digest('hex')!==originalChunkHash) throw new Error('Font adapter requires the pinned original chunk; no fuzzy patch attempted.');
 const safe='var ROLE_DEFAULT = {';
 const cjk='var EA_FALLBACK_FACE = ROLE_DEFAULT.heading;';
 if(source.split(safe).length!==2||source.split(cjk).length!==2) throw new Error('Expected font-set insertion points are not unique.');
 const localized=source.replace(safe,'SAFE_FONTS.add("zen kaku gothic new");\nSAFE_FONTS.add("space grotesk");\n'+safe)
  .replace(cjk,'CJK_SAFE_FACES.add("zen kaku gothic new");\n'+cjk);
 return {...result,source:localized};
}});
process.argv=[process.argv[0],cli,...process.argv.slice(3)];
await import(pathToFileURL(cli).href);
