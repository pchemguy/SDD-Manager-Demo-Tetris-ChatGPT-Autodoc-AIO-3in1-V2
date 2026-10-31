"""Actual user-selected downloads/restores through the shared runtime and local Wasm."""
import json,sqlite3
from pathlib import Path
from playwright.sync_api import expect
SETTINGS=dict(ghost='hide',hardDrop='off',next='off',hardDropLock='immediate',lock='failed',hold='off')
def candidate():return dict(formatVersion=1,results=[dict(id='00000000-0000-4000-8000-000000000001',score=17,timestamp='2026-01-01T00:00:00.000Z')],settings=SETTINGS.copy())
def restore(page,data,name='save.bin'):
    page.locator('#restore-input').set_input_files(dict(name=name,mimeType='application/octet-stream',buffer=data))
def save(page,format):
    page.locator('#file-format').select_option(format)
    with page.expect_download(timeout=15000) as pending:page.locator('#save').click()
    downloaded=pending.value
    assert downloaded.suggested_filename=='tetris-save.'+('json' if format=='json' else 'sqlite')
    return Path(downloaded.path()).read_bytes()
def observable(page):
    return dict(settings={k:page.locator('#setting-'+k).input_value() for k in SETTINGS},rows=page.locator('#leaderboard-body').inner_html(),cookie=page.context.cookies(),url=page.url)

def test_restore_applies_all_settings_pauses_without_reset_and_cross_format_downloads(page):
    page.locator('#start').click()
    fields=['score','level','lines','active-kind','hold-piece','next-piece'];before={k:page.locator('#'+k).text_content() for k in fields}
    restore(page,json.dumps(candidate()).encode())
    expect(page.locator('#notice')).to_contain_text('Restored')
    expect(page.locator('#state')).to_have_text('Paused')
    assert {k:page.locator('#'+k).text_content() for k in fields}==before
    assert json.loads(save(page,'json'))==candidate()
    for key,value in SETTINGS.items():
        expect(page.locator('#setting-'+key)).to_have_value(value)
        assert page.evaluate('(key)=>new URL(location.href).searchParams.get(key)',key)==value
    assert {c['name']:c['value'] for c in page.context.cookies()}=={'tetris_'+k:v for k,v in SETTINGS.items()}
    sqlite=save(page,'sqlite');assert sqlite.startswith(b'SQLite format 3\0')
    db=sqlite3.connect(':memory:');db.deserialize(sqlite)
    assert dict(db.execute('SELECT key,value FROM settings'))==SETTINGS;db.close()
    page.locator('#setting-ghost').select_option('show');restore(page,sqlite,'wrong.json')
    expect(page.locator('#setting-ghost')).to_have_value('hide')
    assert json.loads(save(page,'json'))==candidate()
    page.locator('#toggle-settings').click()
    expect(page.locator('#save')).to_be_hidden();expect(page.locator('#restore')).to_be_hidden()
    assert page.locator('[data-gameplay]').count()==2

def test_invalid_cancelled_and_oversize_files_leave_observables_unchanged(page):
    page.locator('#start').click();page.keyboard.press('p');before=observable(page)
    for data in [b'{}',b'bad binary\0',b'\xc0\xaf',b' '*2097153]:
        restore(page,data);expect(page.locator('#notice')).to_contain_text('Restore failed')
        assert observable(page)==before
    with page.expect_file_chooser() as pending:page.locator('#restore').click()
    pending.value.set_files([])
    assert observable(page)==before

def test_settings_and_file_controls_are_locked_during_file_read(page):
    page.evaluate("() => {const read=File.prototype.arrayBuffer;File.prototype.arrayBuffer=async function(){await new Promise(resolve=>setTimeout(resolve,800));return read.call(this)}}")
    restore(page,json.dumps(candidate()).encode())
    expect(page.locator('#setting-ghost')).to_be_disabled(timeout=200)
    expect(page.locator('#save')).to_be_disabled(timeout=200)
    expect(page.locator('#notice')).to_contain_text('Restored')
    expect(page.locator('#setting-ghost')).to_be_enabled()
