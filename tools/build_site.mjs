import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
const root=fileURLToPath(new URL('../',import.meta.url));
for(const script of ['tools/build_project_manifest.py','tools/build_catalog_site.py','tools/build_support_pages.py']){
  const result=spawnSync('python',[script],{cwd:root,stdio:'inherit',windowsHide:true});
  if(result.status!==0)process.exit(result.status||1);
}
