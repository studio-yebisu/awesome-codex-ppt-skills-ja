from pathlib import Path
import importlib.util,sys,shutil
C=Path(__file__).resolve().parents[1]
p=C/'source/build_seaslides_repository_example.py';s=importlib.util.spec_from_file_location('sea_local',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
m.ROOT=C;m.OUT=C;m.UP=C/'source/upstream';m.SKILL=m.UP/m.REL
m.prepare();e=m.runtime()
for argv,name in [([sys.executable,e/'scripts/validate_project.py',C,'--source-only','--profile','standard-project'],'source-gate-rebuild.log'),([sys.executable,e/'scripts/html_compiler.py',C,'--all'],'compiler-rebuild.log'),([sys.executable,e/'scripts/validate_project.py',C,'--require-build','--artifact-profile','visual'],'visual-gate-rebuild.log')]:m.run(argv,name,cwd=C)
for i in range(1,6):shutil.copy2(C/f'output/browser_pngs/slide_{i:02}.png',C/f'render/slide-{i:02}.png')
print('original gates and synchronized artifacts complete; visual review required')
