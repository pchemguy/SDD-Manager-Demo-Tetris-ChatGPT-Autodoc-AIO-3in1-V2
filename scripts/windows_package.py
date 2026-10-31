"""Stream the verified upstream runtime and owned app into a complete portable archive."""
from pathlib import Path
import json,zipfile,shutil
from download_electron import ensure_runtime,config
ROOT=Path(__file__).resolve().parents[1]
def member(name):
    item=zipfile.ZipInfo(name,date_time=(1980,1,1,0,0,0));item.compress_type=zipfile.ZIP_DEFLATED;item.external_attr=(0o100755 if name.endswith('.exe') else 0o100644)<<16;return item
def package_windows(output,metadata):
    upstream=ensure_runtime();locked=json.loads((ROOT/'platforms/electron/runtime-files.json').read_text());runtime=config()
    if locked['electronVersion']!=runtime['electronVersion']:raise ValueError('Windows runtime lock version mismatch')
    app=ROOT/'dist/desktop'
    if not (app/'renderer/index.html').is_file():raise RuntimeError('Build desktop renderer before packaging')
    path=output/'tetris-windows-x64.zip'
    with zipfile.ZipFile(upstream) as source,zipfile.ZipFile(path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=6,allowZip64=True) as archive:
        for name,entry in sorted(locked['files'].items()):
            with source.open(entry['sourceName']) as reader,archive.open(member(name),'w') as writer:shutil.copyfileobj(reader,writer,1024*1024)
        for source_file in sorted(app.rglob('*')):
            if source_file.is_file():archive.writestr(member('resources/app/'+source_file.relative_to(app).as_posix()),source_file.read_bytes())
        docs={'INSTALL.md':ROOT/'platforms/electron/INSTALL.md','FILES.md':ROOT/'FILES.md','THIRD-PARTY-NOTICES.md':ROOT/'THIRD-PARTY-NOTICES.md','LICENSE.tetris':ROOT/'LICENSE'}
        for name,source_file in docs.items():archive.writestr(member(name),source_file.read_bytes())
        provenance={'electronVersion':runtime['electronVersion'],'upstreamArchive':runtime['distributions']['win32-x64']['filename'],'upstreamSHA256':runtime['distributions']['win32-x64']['sha256'],'platform':'win32','arch':'x64','distribution':'unsigned portable development package'}
        archive.writestr(member('runtime-info.json'),json.dumps(provenance,sort_keys=True)+'\n');archive.writestr(member('build-info.json'),json.dumps(metadata,sort_keys=True)+'\n')
    return path
