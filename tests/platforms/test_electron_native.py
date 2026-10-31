"""Opt-in compatible-host probe; Node automation is driven and reported by pytest."""
import json,os,signal,sqlite3,subprocess
from pathlib import Path
import pytest
ROOT=Path(__file__).resolve().parents[2]
def test_packaged_app_origin_cookies_files_and_isolation_on_available_electron(tmp_path):
    binary=os.environ.get('TETRIS_ELECTRON_BINARY');source=os.environ.get('TETRIS_DESKTOP_APP')
    if not binary or not source:pytest.skip('Native Electron probe is opt-in; Windows execution is separately unavailable on Linux')
    source=Path(source);entry=tmp_path/'bootstrap.cjs';profile=tmp_path/'profile';profile.mkdir();downloads=tmp_path/'downloads';downloads.mkdir()
    entry.write_text("const e=require('electron');e.app.setPath('userData',process.env.TETRIS_TEST_PROFILE);require("+json.dumps(str(source/'main.cjs'))+");")
    request=dict(binary=binary,entry=str(entry),profile=str(profile),downloads=str(downloads),version=json.loads((ROOT/'package.json').read_text())['version'])
    proc=subprocess.Popen(['node','tests/support/electron-native-driver.cjs'],cwd=ROOT,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,start_new_session=os.name!='nt')
    try:out,err=proc.communicate(json.dumps(request),timeout=70)
    except subprocess.TimeoutExpired:
        if os.name!='nt':os.killpg(proc.pid,signal.SIGTERM)
        else:proc.terminate()
        try:proc.communicate(timeout=3)
        except subprocess.TimeoutExpired:
            if os.name!='nt':os.killpg(proc.pid,signal.SIGKILL)
            else:proc.kill()
        raise
    assert proc.returncode==0,err
    evidence=json.loads(out);assert evidence['origin']=='https://tetris.invalid' and evidence['secure'] and evidence['noNode'] and evidence['popupDenied'] and evidence['reopenedSettings'] and evidence['sessionResultsCleared']
    db=sqlite3.connect(evidence['sqlite']);assert db.execute('PRAGMA user_version').fetchone()[0]==1
    assert len(list(db.execute('SELECT key,value FROM settings')))==6;db.close()
