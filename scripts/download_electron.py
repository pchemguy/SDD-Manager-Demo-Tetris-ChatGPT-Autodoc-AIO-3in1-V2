"""Fetch immutable official Electron assets and verify both pinned and upstream checksums."""
from pathlib import Path, PurePosixPath
import hashlib,json,sys,urllib.request,zipfile
ROOT=Path(__file__).resolve().parents[1]
def digest_file(path):
    digest=hashlib.sha256()
    with Path(path).open('rb') as stream:
        for chunk in iter(lambda:stream.read(1024*1024),b''):digest.update(chunk)
    return digest.hexdigest()
def config():return json.loads((ROOT/'platforms/electron/runtime.json').read_text())
def ensure_runtime(platform='win32-x64'):
    locked=config();asset=locked['distributions'][platform];checks=(ROOT/'platforms/electron/SHASUMS256.txt').read_bytes()
    if hashlib.sha256(checks).hexdigest()!=locked['checksumFile']['sha256']:raise ValueError('Wrong upstream checksum inventory')
    checksum=next(line.split()[0] for line in checks.decode().splitlines() if line.split()[-1].lstrip('*')==asset['filename'])
    if checksum!=asset['sha256']:raise ValueError('Electron checksum sources disagree')
    cache=ROOT/'build/vendor';cache.mkdir(parents=True,exist_ok=True);path=cache/asset['filename']
    if path.is_file() and path.stat().st_size==asset['size'] and digest_file(path)==asset['sha256']:return path
    partial=path.with_suffix('.part');last_error=None
    for url in [asset['apiURL'],asset['browserURL']]:
        try:
            request=urllib.request.Request(url,headers={'Accept':'application/octet-stream','Cache-Control':'no-cache','User-Agent':'Tetris-package-verifier'})
            digest=hashlib.sha256();total=0;next_report=16*1024*1024
            with urllib.request.urlopen(request,timeout=90) as response,partial.open('wb') as output:
                for chunk in iter(lambda:response.read(1024*1024),b''):
                    output.write(chunk);digest.update(chunk);total+=len(chunk)
                    if total>=next_report:print('Electron',platform,'downloaded',total//(1024*1024),'MiB',flush=True);next_report+=16*1024*1024
            if total!=asset['size'] or digest.hexdigest()!=asset['sha256']:raise ValueError('Electron download size/checksum mismatch')
            partial.replace(path);print('Verified official Electron archive',platform,asset['sha256'],flush=True);return path
        except Exception as error:last_error=type(error).__name__;partial.unlink(missing_ok=True)
    raise RuntimeError('Official Electron runtime download failed: '+str(last_error))
def create_windows_lock():
    path=ensure_runtime();files={}
    with zipfile.ZipFile(path) as archive:
        for item in sorted(archive.infolist(),key=lambda i:i.filename):
            if item.is_dir() or item.filename=='resources/default_app.asar':continue
            name=item.filename;parts=PurePosixPath(name)
            if parts.is_absolute() or '..' in parts.parts or '\\' in name or ((item.external_attr>>16)&0o170000)==0o120000:raise ValueError('Unsafe upstream runtime path')
            target='Tetris.exe' if name=='electron.exe' else name;digest=hashlib.sha256()
            with archive.open(item) as source:
                for chunk in iter(lambda:source.read(1024*1024),b''):digest.update(chunk)
            files[target]={'sourceName':name,'size':item.file_size,'sha256':digest.hexdigest()}
    (ROOT/'platforms/electron/runtime-files.json').write_text(json.dumps({'electronVersion':config()['electronVersion'],'files':files},indent=2)+'\n')
    print('Locked',len(files),'official Windows runtime files')
if __name__=='__main__':
    if '--lock-windows' in sys.argv:create_windows_lock()
    else:print(ensure_runtime(sys.argv[1] if len(sys.argv)>1 else 'win32-x64'))
