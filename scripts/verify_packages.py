"""Check stable names, ZIP safety/resources, source metadata and byte checksums."""
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
import zipfile
ROOT = Path(__file__).resolve().parents[1]
def verify_names(names, expected):
    if len(names) != len(set(names)) or set(names) != set(expected):
        raise ValueError('Release asset names must exactly match the stable platform contract')
def expected_names():
    minor = int(json.loads((ROOT/'package.json').read_text())['version'].split('.')[1])
    names = ['tetris-browser.zip']
    if minor >= 9: names.append('tetris-windows-x64.zip')
    if minor >= 10: names += ['tetris-chromium-extension.zip', 'tetris-firefox-extension.zip']
    return names + ['SHA256SUMS.txt']
def verify(directory):
    directory = Path(directory);expected = expected_names()
    verify_names([p.name for p in directory.iterdir() if p.is_file()], expected)
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
    verify(sys.argv[1] if len(sys.argv)>1 else ROOT/'artifacts')
