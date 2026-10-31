"""Assemble cumulative deployable platforms and the stable checksum inventory."""
from pathlib import Path
import hashlib,json,subprocess,zipfile
from verify_packages import verify,release_files
ROOT=Path(__file__).resolve().parents[1]
def metadata():return {'version':json.loads((ROOT/'package.json').read_text())['version'],'sourceCommit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),'dirty':bool(subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=ROOT))}
def package_browser(output,identity):
    source=ROOT/'dist/browser'
    if not (source/'index.html').is_file():raise RuntimeError('Build browser production bundle first')
    files={p.relative_to(source).as_posix():p.read_bytes() for p in source.rglob('*') if p.is_file()}
    for name in ['INSTALL.md','THIRD-PARTY-NOTICES.md','LICENSE','FILES.md']:files[name]=(ROOT/name).read_bytes()
    files['build-info.json']=(json.dumps(identity,sort_keys=True)+'\n').encode()
    with zipfile.ZipFile(output/'tetris-browser.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for name,content in sorted(files.items()):
            item=zipfile.ZipInfo(name,date_time=(1980,1,1,0,0,0));item.compress_type=zipfile.ZIP_DEFLATED;item.external_attr=0o100644<<16;archive.writestr(item,content)
def package_extension(output,identity,family):
    source=ROOT/'dist/extensions'/family
    if not (source/'manifest.json').is_file():raise RuntimeError('Build sidebar production bundles first')
    files={p.relative_to(source).as_posix():p.read_bytes() for p in source.rglob('*') if p.is_file()}
    for name in ['THIRD-PARTY-NOTICES.md','LICENSE','FILES.md']:files[name]=(ROOT/name).read_bytes()
    files['INSTALL.md']=(ROOT/'platforms/extensions/INSTALL.md').read_bytes()
    files['build-info.json']=(json.dumps(identity,sort_keys=True)+'\n').encode()
    with zipfile.ZipFile(output/f'tetris-{family}-extension.zip','w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as archive:
        for name,content in sorted(files.items()):
            item=zipfile.ZipInfo(name,date_time=(1980,1,1,0,0,0));item.compress_type=zipfile.ZIP_DEFLATED;item.external_attr=0o100644<<16;archive.writestr(item,content)
def main():
    output=ROOT/'artifacts';output.mkdir(exist_ok=True);identity=metadata();minor=int(identity['version'].split('.')[1]);package_browser(output,identity)
    if minor>=9:
        from windows_package import package_windows
        package_windows(output,identity)
    if minor>=10:
        for family in ['chromium','firefox']:package_extension(output,identity,family)
    checks=''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n' for p in sorted(p for p in release_files(output) if p.name.endswith('.zip')));(output/'SHA256SUMS.txt').write_text(checks)
    verify(output)
if __name__=='__main__':main()
