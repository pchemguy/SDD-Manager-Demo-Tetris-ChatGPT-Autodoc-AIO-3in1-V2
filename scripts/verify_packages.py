"""Check stable names, ZIP safety/resources, source metadata and byte checksums."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import struct
import sys
import zipfile
ROOT = Path(__file__).resolve().parents[1]
def release_files(directory):
    # Managed file transfers may create sidecars; publish only the visible release inventory.
    return [p for p in Path(directory).iterdir() if p.is_file() and not p.name.startswith('.')]
def verify_names(names, expected):
    if len(names) != len(set(names)) or set(names) != set(expected):
        raise ValueError('Release asset names must exactly match the stable platform contract')
def expected_names():
    minor = int(json.loads((ROOT/'package.json').read_text())['version'].split('.')[1])
    names = ['tetris-browser.zip']
    if minor >= 9: names.append('tetris-windows-x64.zip')
    if minor >= 10: names += ['tetris-chromium-extension.zip', 'tetris-firefox-extension.zip']
    return names + ['SHA256SUMS.txt']
def verify_pe(data):
    if len(data)<64 or data[:2]!=b'MZ':raise ValueError('Invalid Windows PE DOS header')
    offset=struct.unpack_from('<I',data,0x3c)[0]
    if offset+26>len(data) or data[offset:offset+4]!=b'PE\0\0':raise ValueError('Invalid Windows PE header')
    machine,sections=struct.unpack_from('<HH',data,offset+4);magic=struct.unpack_from('<H',data,offset+24)[0]
    if machine!=0x8664 or sections<1 or magic!=0x20b:raise ValueError('Windows runtime must be x64 PE32+')
def verify_windows(archive,version):
    locked=json.loads((ROOT/'platforms/electron/runtime-files.json').read_text());runtime=json.loads((ROOT/'platforms/electron/runtime.json').read_text())
    app=ROOT/'dist/desktop';owned={p.relative_to(app).as_posix():p for p in app.rglob('*') if p.is_file()}
    required=set(locked['files'])|{'resources/app/'+n for n in owned}|{'INSTALL.md','FILES.md','THIRD-PARTY-NOTICES.md','LICENSE.tetris','runtime-info.json','build-info.json'}
    if set(archive.namelist())!=required:raise ValueError('Windows runtime/application inventory mismatch')
    for name,entry in locked['files'].items():
        if archive.getinfo(name).file_size!=entry['size']:raise ValueError('Wrong Windows runtime size: '+name)
        digest=hashlib.sha256()
        with archive.open(name) as stream:
            prefix=stream.read(4096);digest.update(prefix)
            if name.endswith(('.exe','.dll')):verify_pe(prefix)
            for chunk in iter(lambda:stream.read(1024*1024),b''):digest.update(chunk)
        if digest.hexdigest()!=entry['sha256']:raise ValueError('Wrong Windows runtime bytes: '+name)
    for name,source in owned.items():
        if archive.read('resources/app/'+name)!=source.read_bytes():raise ValueError('Wrong bundled desktop app resource: '+name)
    for name in ['main.cjs','host.cjs','protocol.cjs']:
        if archive.read('resources/app/'+name)!=(ROOT/'platforms/electron'/name).read_bytes():raise ValueError('Stale desktop host policy')
    meta=json.loads(archive.read('resources/app/package.json'));provenance=json.loads(archive.read('runtime-info.json'))
    if meta.get('version')!=version or meta.get('main')!='main.cjs' or provenance['electronVersion']!=runtime['electronVersion'] or provenance['upstreamSHA256']!=runtime['distributions']['win32-x64']['sha256']:raise ValueError('Windows version/runtime identity mismatch')
    if archive.read('resources/app/renderer/runtime/sql-wasm.wasm')!=(ROOT/'node_modules/sql.js/dist/sql-wasm.wasm').read_bytes():raise ValueError('Wrong Windows SQLite Wasm')
    if archive.read('resources/app/renderer/schemas/tetris-save.schema.json')!=(ROOT/'schemas/tetris-save.schema.json').read_bytes():raise ValueError('Wrong Windows save schema')
    html=archive.read('resources/app/renderer/index.html').decode()
    for ref in re.findall(r'(?:src|href)="([^"]+)"',html):
        if ref.startswith(('http:','https:','//')) or 'resources/app/renderer/'+ref.removeprefix('./') not in archive.namelist():raise ValueError('Missing/remote desktop entry resource')
    print('Verified Windows x64 PE/runtime hashes and owned app inventory:',len(locked['files']),'runtime files')
def verify_extension(archive,family,version):
    source=ROOT/'dist/extensions'/family;owned={p.relative_to(source).as_posix():p for p in source.rglob('*') if p.is_file()}
    required=set(owned)|{'INSTALL.md','THIRD-PARTY-NOTICES.md','LICENSE','FILES.md','build-info.json'}
    if set(archive.namelist())!=required:raise ValueError('Extension resource inventory mismatch')
    m=json.loads(archive.read('manifest.json'))
    if m.get('manifest_version')!=3 or m.get('version')!=version:raise ValueError('Extension manifest/version mismatch')
    expected={'storage','sidePanel'} if family=='chromium' else {'storage'}
    if set(m.get('permissions',[]))!=expected or any(k in m for k in ['host_permissions','content_scripts','externally_connectable']):raise ValueError('Extension permissions mismatch')
    if m.get('content_security_policy',{}).get('extension_pages')!="script-src 'self' 'wasm-unsafe-eval'; object-src 'self'":raise ValueError('Extension CSP mismatch')
    if family=='chromium':
        if m.get('minimum_chrome_version')!='116' or m.get('side_panel')!={'default_path':'panel.html'} or m.get('background')!={'service_worker':'background.js'}:raise ValueError('Chromium sidebar API floor/entry mismatch')
    else:
        if m.get('browser_specific_settings',{}).get('gecko',{}).get('strict_min_version')!='115.0' or m.get('sidebar_action',{}).get('default_panel')!='panel.html' or m.get('background')!={'scripts':['background.js']}:raise ValueError('Firefox sidebar API floor/entry mismatch')
    for name,path in owned.items():
        if archive.read(name)!=path.read_bytes():raise ValueError('Extension resource bytes mismatch: '+name)
    if archive.read('runtime/sql-wasm.wasm')!=(ROOT/'node_modules/sql.js/dist/sql-wasm.wasm').read_bytes() or archive.read('schemas/tetris-save.schema.json')!=(ROOT/'schemas/tetris-save.schema.json').read_bytes():raise ValueError('Extension codec/schema bytes mismatch')
    html=archive.read('panel.html').decode()
    for ref in re.findall(r'(?:src|href)="([^"]+)"',html):
        if ref.startswith(('http:','https:','//','/')) or ref.removeprefix('./') not in required:raise ValueError('Remote/missing extension entry resource')
    if b'harness-bridge' in archive.read('panel.js') or b'requestAnimationFrame' in archive.read('background.js'):raise ValueError('Test bridge or background gameplay in extension')
    for size in [16,32,48,128]:
        name=m.get('icons',{}).get(str(size));data=archive.read(name) if name in required else b''
        if not data.startswith(b'\x89PNG\r\n\x1a\n') or len(data)<24 or struct.unpack('>II',data[16:24])!=(size,size):raise ValueError('Extension icon mismatch')
    print('Verified',family,'manifest, local codec/UI/background, source inventory and icons')
def verify(directory,release_source=None):
    directory = Path(directory);expected = expected_names()
    verify_names([p.name for p in release_files(directory)], expected)
    checks = {}
    for line in (directory/'SHA256SUMS.txt').read_text().splitlines():
        digest, name = line.split('  ', 1)
        if name in checks or not re.fullmatch('[a-f0-9]{64}', digest): raise ValueError('Invalid checksum inventory')
        checks[name] = digest
    verify_names(list(checks), [n for n in expected if n.endswith('.zip')])
    version = json.loads((ROOT/'package.json').read_text())['version']
    for name in checks:
        path = directory/name
        if hashlib.sha256(path.read_bytes()).hexdigest() != checks[name]: raise ValueError('Checksum mismatch: '+name)
        with zipfile.ZipFile(path) as z:
            members = z.namelist()
            if len(members) != len(set(members)) or z.testzip(): raise ValueError('Corrupt/duplicate ZIP members')
            for info in z.infolist():
                p = PurePosixPath(info.filename)
                if p.is_absolute() or '..' in p.parts or '\\' in info.filename or ((info.external_attr >> 16) & 0o170000) == 0o120000: raise ValueError('Unsafe archive member')
                if info.filename.endswith('.tkn') or any(part in {'node_modules','.agents','.test-build','tests','test-results'} for part in p.parts): raise ValueError('Development/secret content in runtime archive')
            identity=json.loads(z.read('build-info.json'))
            if identity.get('version')!=version or not re.fullmatch('[a-f0-9]{40}',identity.get('sourceCommit','')):raise ValueError('Wrong archive build identity')
            if release_source and (identity['sourceCommit']!=release_source or identity.get('dirty') is not False):raise ValueError('Release archive is not the exact clean source')
            if name in ['tetris-chromium-extension.zip','tetris-firefox-extension.zip']:verify_extension(z,'chromium' if 'chromium' in name else 'firefox',version)
            if name == 'tetris-windows-x64.zip':verify_windows(z,version)
            if name == 'tetris-browser.zip':
                for required in ['index.html', 'INSTALL.md', 'THIRD-PARTY-NOTICES.md', 'LICENSE', 'build-info.json']:
                    if required not in members: raise ValueError('Missing '+required)
                if int(version.split('.')[1])>=7:
                    for resource in ['runtime/sql-wasm.wasm','schemas/tetris-save.schema.json']:
                        if resource not in members:raise ValueError('Missing file runtime resource '+resource)
                    if z.read('runtime/sql-wasm.wasm')!=(ROOT/'node_modules/sql.js/dist/sql-wasm.wasm').read_bytes():raise ValueError('Wrong SQLite Wasm runtime')
                    if z.read('schemas/tetris-save.schema.json')!=(ROOT/'schemas/tetris-save.schema.json').read_bytes():raise ValueError('Wrong save schema resource')
                data = json.loads(z.read('build-info.json'))
                if data['version'] != version or not re.fullmatch('[a-f0-9]{40}', data['sourceCommit']): raise ValueError('Wrong build identity')
                if any(b'renderFixture' in z.read(n) for n in members if n.endswith('.js')): raise ValueError('Development renderer harness in runtime code')
                html = z.read('index.html').decode()
                for ref in re.findall(r'(?:src|href)="([^"]+)"', html):
                    if ref.startswith(('http:', 'https:', '//')): raise ValueError('Remote required runtime asset')
                    if ref.removeprefix('./').split('?')[0] not in members: raise ValueError('Missing entry resource '+ref)
    print('Verified actual asset names, archive resources/safety and checksums:', ', '.join(expected))
if __name__ == '__main__':
    verify(sys.argv[1] if len(sys.argv)>1 else ROOT/'artifacts',sys.argv[2] if len(sys.argv)>2 else None)
