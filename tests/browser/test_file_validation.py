"""Packaged-style cross-format state equivalence and rejection non-mutation."""
import copy,json,sqlite3
from playwright.sync_api import expect
from test_files import candidate,restore,save,observable

def full_candidate():
    value=candidate();value['results']=[dict(id=f'00000000-0000-4000-8000-{n:012}',score=0 if n==0 else 9007199254740991-n,timestamp=f'2026-01-{n+1:02}T00:00:00.000Z') for n in range(10)]
    value['results'].sort(key=lambda r:(-r['score'],r['timestamp'],r['id']));return value

def test_full_empty_and_cross_format_semantic_equality(page):
    for value in [full_candidate(),{**candidate(),'results':[]}]:
        restore(page,json.dumps(value).encode());expect(page.locator('#notice')).to_contain_text('Restored')
        assert json.loads(save(page,'json'))==value
        binary=save(page,'sqlite');db=sqlite3.connect(':memory:');db.deserialize(binary)
        assert sorted(db.execute('SELECT id,score,timestamp FROM high_scores'))==sorted(tuple(r.values()) for r in value['results'])
        assert dict(db.execute('SELECT key,value FROM settings'))==value['settings'];db.close()
        restore(page,binary);expect(page.locator('#notice')).to_contain_text('Restored')
        assert json.loads(save(page,'json'))==value

def test_malformed_json_and_sqlite_preserve_results_settings_cookies_url(page):
    good=full_candidate();restore(page,json.dumps(good).encode());expect(page.locator('#notice')).to_contain_text('Restored')
    binary=save(page,'sqlite');before=observable(page);bad=[]
    for mutate in [lambda d:d.update(extra=1),lambda d:d.update(formatVersion=2),lambda d:d['settings'].pop('hold'),lambda d:d['settings'].update(hold=True),lambda d:d['results'][0].update(score=-1),lambda d:d['results'][0].update(score=9007199254740992),lambda d:d['results'][0].update(timestamp='2026-02-30T00:00:00.000Z'),lambda d:d['results'].append(d['results'][0])]:
        value=copy.deepcopy(good);mutate(value);bad.append(json.dumps(value).encode())
    value=copy.deepcopy(good);value['results']=value['results'][:2];value['results'][1]['id']=value['results'][0]['id'];bad.append(json.dumps(value).encode())
    bad.append(json.dumps(good).replace('"hold": "off"','"hold": "off", "\\u0068old": "on"').encode())
    for mutation in ['PRAGMA user_version=2','PRAGMA application_id=0','CREATE TABLE extra(x)',"UPDATE settings SET value='bad' WHERE key='hold'",'UPDATE high_scores SET score=1.5',"UPDATE high_scores SET timestamp='bad'"]:
        db=sqlite3.connect(':memory:');db.deserialize(binary);db.executescript(mutation);db.commit();bad.append(db.serialize());db.close()
    bad.extend([binary[:100],b'\xc0\xaf',b' '*2097153])
    for data in bad:
        restore(page,data);expect(page.locator('#notice')).to_contain_text('Restore failed')
        assert observable(page)==before

def test_sqlite_under_strict_script_csp_with_no_external_runtime_requests(page,csp_url):
    requests=[];page.on('request',lambda r:requests.append(r.url));page.goto(csp_url)
    binary=save(page,'sqlite');assert binary.startswith(b'SQLite format 3\0')
    restore(page,binary);expect(page.locator('#notice')).to_contain_text('Restored')
    assert any('/runtime/sql-wasm.wasm' in url for url in requests)
    assert all(url.startswith(csp_url) for url in requests)
