"""Assemble deterministic static browser ZIP and its stable checksum inventory."""
from pathlib import Path
import hashlib
import json
import subprocess
import zipfile
from verify_packages import verify
ROOT = Path(__file__).resolve().parents[1]
def package_browser():
    output = ROOT/'artifacts';output.mkdir(exist_ok=True)
    source = ROOT/'dist/browser'
    if not (source/'index.html').is_file(): raise RuntimeError('Build the production browser bundle first')
    files = {p.relative_to(source).as_posix(): p.read_bytes() for p in source.rglob('*') if p.is_file()}
    for name in ['INSTALL.md', 'THIRD-PARTY-NOTICES.md', 'LICENSE']: files[name] = (ROOT/name).read_bytes()
    metadata = {'version': json.loads((ROOT/'package.json').read_text())['version'], 'sourceCommit': subprocess.check_output(['git','rev-parse','HEAD'], cwd=ROOT, text=True).strip(), 'dirty': bool(subprocess.check_output(['git','status','--porcelain','--untracked-files=no'], cwd=ROOT))}
    files['build-info.json'] = (json.dumps(metadata, sort_keys=True)+'\n').encode()
    path = output/'tetris-browser.zip'
    with zipfile.ZipFile(path, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, content in sorted(files.items()):
            item = zipfile.ZipInfo(name, date_time=(1980,1,1,0,0,0));item.compress_type=zipfile.ZIP_DEFLATED;item.external_attr=0o644<<16;archive.writestr(item,content)
    checks = ''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n' for p in sorted(output.glob('*.zip')))
    (output/'SHA256SUMS.txt').write_text(checks)
    verify(output)
if __name__ == '__main__': package_browser()
