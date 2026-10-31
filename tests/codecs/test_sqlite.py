"""Actual SQLite bytes, independent sqlite3 inspection, hostile schema/data rejection."""
import base64,json,sqlite3
import pytest
from test_snapshot import doc,row
SQL="""CREATE TABLE high_scores(id TEXT PRIMARY KEY NOT NULL, score INTEGER NOT NULL CHECK(score >= 0 AND score <= 9007199254740991), timestamp TEXT NOT NULL);
CREATE TABLE settings(key TEXT PRIMARY KEY NOT NULL, value TEXT NOT NULL);"""
def database(mutation=None,schema=SQL):
    db=sqlite3.connect(':memory:');db.executescript('PRAGMA user_version=1; PRAGMA application_id=1413829714;'+schema)
    db.executemany('INSERT INTO settings(key,value) VALUES(?,?)',doc()['settings'].items())
    db.execute('INSERT INTO high_scores VALUES(?,?,?)',tuple(row().values()))
    if mutation:db.executescript(mutation)
    db.commit();data=db.serialize();db.close();return base64.b64encode(data).decode()
@pytest.mark.parametrize('results',[[],[row(1,0),row(2,9007199254740991)],[row(n,n) for n in range(10)]])
def test_roundtrip_and_external_reader(driver,results):
    candidate={**doc(),'results':results};r=driver('sqlite',encode=True,document=candidate)
    assert 'error' not in r and r['closed']==2
    data=base64.b64decode(r['base64']);assert data.startswith(b'SQLite format 3\0')
    db=sqlite3.connect(':memory:');db.deserialize(data)
    assert db.execute('PRAGMA user_version').fetchone()[0]==1
    assert db.execute('PRAGMA application_id').fetchone()[0]==1413829714
    assert dict(db.execute('SELECT key,value FROM settings'))==candidate['settings']
    assert sorted(db.execute('SELECT id,score,timestamp FROM high_scores'))==sorted(tuple(v.values()) for v in results)
    assert db.execute('PRAGMA integrity_check').fetchone()[0]=='ok';db.close()
    assert r['snapshot']==driver('snapshot',document=candidate)['snapshot']
@pytest.mark.parametrize('mutation',[
    'PRAGMA user_version=0','PRAGMA user_version=2','PRAGMA application_id=0',
    'CREATE TABLE extra(x)','CREATE VIEW extra AS SELECT * FROM settings',
    'CREATE TRIGGER extra AFTER INSERT ON settings BEGIN SELECT 1; END',
    "DELETE FROM settings WHERE key='hold'","UPDATE settings SET key='unknown' WHERE key='hold'",
    "UPDATE settings SET value='TRUE' WHERE key='hold'","UPDATE settings SET value=x'6f6e' WHERE key='hold'",
    "UPDATE high_scores SET timestamp='2026-02-30T00:00:00.000Z'","UPDATE high_scores SET timestamp=x'3031'",
    "UPDATE high_scores SET id='invalid'",'PRAGMA ignore_check_constraints=ON; UPDATE high_scores SET score=-1',
    'UPDATE high_scores SET score=1.5','PRAGMA ignore_check_constraints=ON; UPDATE high_scores SET score=9007199254740992',
    "PRAGMA ignore_check_constraints=ON; UPDATE high_scores SET score='not-a-number'",
])
def test_metadata_objects_rows_and_storage_classes_rejected(driver,mutation):
    r=driver('sqlite',base64=database(mutation))
    assert r.get('error') and r['closed']==1
@pytest.mark.parametrize('schema',[
    SQL.replace('CHECK(score >= 0 AND score <= 9007199254740991)',''),
    SQL.replace('AND score <=','OR score <='),
    SQL.replace('score >= 0 AND score <= 9007199254740991','(score >= 0 AND score) <= 9007199254740991'),
    SQL.replace('score >= 0','score >= -1'),
    SQL.replace('id TEXT PRIMARY KEY NOT NULL','id TEXT PRIMARY KEY'),
    SQL.replace('score INTEGER','score REAL'),
    SQL.replace('timestamp TEXT NOT NULL',"timestamp TEXT NOT NULL, generated TEXT GENERATED ALWAYS AS ('x') VIRTUAL"),
    SQL.replace('value TEXT NOT NULL','value TEXT NOT NULL, extra TEXT'),
    SQL.replace('key TEXT PRIMARY KEY NOT NULL','key TEXT NOT NULL'),
    SQL.replace('CHECK(score >= 0 AND score <= 9007199254740991)',"DEFAULT 'CHECK(score >= 0 AND score <= 9007199254740991)'"),
])
def test_malformed_schema_and_fake_check_literals_rejected(driver,schema):
    r=driver('sqlite',base64=database(schema=schema));assert r.get('error') and r['closed']==1

def test_harmless_sql_quoting_whitespace_and_indexes_accepted(driver):
    schema=SQL.replace('score >= 0 AND score <= 9007199254740991','(("score" >= 0) AND ([score] <= 9007199254740991))').replace('high_scores','"high_scores"')
    r=driver('sqlite',base64=database('CREATE INDEX extra_index ON high_scores(score)',schema))
    assert not r.get('error') and r['closed']==1

def test_unknown_corrupt_truncated_and_excess_rows(driver):
    for data in [b'not sqlite',b'SQLite format 3\0'+b'\0'*50,base64.b64decode(database())[:100]]:
        assert driver('sqlite',base64=base64.b64encode(data).decode()).get('error')
    inserts=';'.join(f"INSERT INTO high_scores VALUES('00000000-0000-4000-8000-{n:012}',0,'2026-01-01T00:00:00.000Z')" for n in range(2,12))
    assert driver('sqlite',base64=database(inserts)).get('error')

def test_virtual_table_is_rejected(driver):
    encoded=database("DROP TABLE high_scores; CREATE VIRTUAL TABLE high_scores USING fts5(id,score,timestamp)")
    r=driver('sqlite',base64=encoded);assert r.get('error') and r['closed']==1
