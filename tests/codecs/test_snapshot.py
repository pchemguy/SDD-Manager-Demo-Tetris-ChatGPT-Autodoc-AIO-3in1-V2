"""A shared corpus checks the complete runtime contract and Draft 2020-12 schema."""
import copy,json,re
from datetime import datetime
from pathlib import Path
import pytest
from jsonschema import Draft202012Validator,FormatChecker
DEFAULTS=dict(ghost='show',hardDrop='on',next='on',hardDropLock='general',lock='interval',hold='on')
def doc():return dict(formatVersion=1,results=[],settings=DEFAULTS.copy())
def row(n=1,score=0,time='2026-01-01T00:00:00.000Z'):
    return dict(id=f'00000000-0000-4000-8000-{n:012}',score=score,timestamp=time)
def corpus():
    good=[doc(),{**doc(),'results':[row(1,9007199254740991,'0001-01-01T00:00:00.000Z'),row(2,0,'9999-12-31T23:59:59.999Z')]},{**doc(),'results':[row(n,n) for n in range(10)]}]
    bad=[None,[],{},dict(formatVersion=1,results=[]),{**doc(),'extra':1},{**doc(),'formatVersion':2},{**doc(),'formatVersion':True},{**doc(),'results':[row(n) for n in range(11)]},{**doc(),'results':[row(),row()]}]
    for key in DEFAULTS:
        value=doc();del value['settings'][key];bad.append(value)
        for invalid in ['unknown','',True,1,None]:
            value=doc();value['settings'][key]=invalid;bad.append(value)
    value=doc();value['settings']['extra']='on';bad.append(value)
    for patch in [{'id':'invalid'},{'score':-1},{'score':True},{'score':1.5},{'score':9007199254740992},{'timestamp':'2026-02-30T00:00:00.000Z'},{'timestamp':'2026-01-01T00:00:00Z'},{'timestamp':'0000-01-01T00:00:00.000Z'},{'timestamp':'2026-01-01T00:00:60.000Z'},{'extra':1}]:bad.append({**doc(),'results':[{**row(),**patch}]})
    return [(value,True) for value in good]+[(value,False) for value in bad]
@pytest.mark.parametrize('value,valid',corpus())
def test_schema_and_runtime_complete_validation_agree(driver,value,valid):
    schema=json.loads((Path(__file__).resolve().parents[2]/'schemas/tetris-save.schema.json').read_text())
    checker=FormatChecker()
    @checker.checks('date-time',raises=(ValueError,TypeError))
    def canonical_time(value):
        if not isinstance(value,str):return True
        parsed=datetime.fromisoformat(value.replace('Z','+00:00'))
        return parsed.strftime('%Y-%m-%dT%H:%M:%S.')+f'{parsed.microsecond//1000:03}Z'==value if parsed.year>=1000 else parsed.isoformat(timespec='milliseconds').replace('+00:00','Z')==value
    Draft202012Validator.check_schema(schema)
    structural=Draft202012Validator(schema,format_checker=checker).is_valid(value)
    semantic=not isinstance(value,dict) or not isinstance(value.get('results'),list) or len({r.get('id') for r in value['results'] if isinstance(r,dict)})==len(value['results'])
    assert (structural and semantic)==valid
    r=driver('snapshot',document=value)
    assert ('error' not in r)==valid
    if valid:assert r['immutable']

def test_canonicalizes_only_a_fully_valid_candidate(driver):
    value={**doc(),'results':[row(1,2),row(2,8)]}
    r=driver('snapshot',document=value)
    assert r['snapshot']['results'][0]['score']==8 and value['results'][0]['score']==2
