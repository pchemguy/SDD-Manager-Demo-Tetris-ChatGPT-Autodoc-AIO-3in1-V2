/** Deterministic subprocess bridge; excluded from production bundles. */
import initSqlJs from 'sql.js';
import {resolve} from 'node:path';
import {checkSize} from '../../src/codecs/limits.js';
import {encodeSQLite,decodeSQLite,isSQLite} from '../../src/codecs/sqlite.js';
import {encodeJSON,decodeJSON} from '../../src/codecs/json.js';
import {FileExchange} from '../../src/app/files.js';
import {BrowserSettings,type SettingsHost} from '../../src/platform/browser/settings.js';
import {validateSnapshot} from '../../src/app/snapshot.js';
import {newID} from '../../src/platform/browser/host.js';
import {rank,validateResults} from '../../src/app/results.js';
import {resolveSettings} from '../../src/app/resolve-settings.js';
import {Controller} from '../../src/app/controller.js';
import {readFileSync} from 'node:fs';
import {ghostVisible} from '../../src/core/ghost.js';
import {landing} from '../../src/core/landing.js';
import * as source from '../../src/core/source.js';
import * as game from '../../src/core/game.js';
import * as geometry from '../../src/core/geometry.js';
function testResultHost(){let n=0;return{id:()=>`00000000-0000-4000-8000-${String(++n).padStart(12,'0')}`,timestamp:()=>"2026-01-01T00:00:00.000Z"};}
const q=JSON.parse(readFileSync(0,'utf8'));
if(q.op==='sqlite'){let closed=0;const SQL=await initSqlJs({locateFile:file=>resolve('node_modules/sql.js/dist',file)}),engine={Database:class extends SQL.Database{close(){closed++;super.close();}}};try{if(q.encode){const bytes=encodeSQLite(q.document,engine);console.log(JSON.stringify({base64:Buffer.from(bytes).toString('base64'),snapshot:decodeSQLite(bytes,engine),closed}));}else console.log(JSON.stringify({snapshot:decodeSQLite(new Uint8Array(Buffer.from(q.base64,'base64')),engine),closed}));}catch(e){console.log(JSON.stringify({error:String(e),closed}));}}
else if(q.op==='json'){try{if(q.encode){const bytes=encodeJSON(q.document);console.log(JSON.stringify({text:new TextDecoder().decode(bytes),snapshot:decodeJSON(bytes)}));}else console.log(JSON.stringify({snapshot:decodeJSON(q.bytes?new Uint8Array(q.bytes):new TextEncoder().encode(q.text))}));}catch(e){console.log(JSON.stringify({error:String(e)}));}}
else if(q.op==='fileTransaction'){
 let now=0,writes=0,href='https://game.invalid/play?keep=abc#stay';const cookie=new Map<string,string>([['tetris_ghost','dynamic'],['unrelated','yes']]);
 const host:SettingsHost={get href(){return href;},get cookie(){return [...cookie].map(([k,v])=>k+'='+v).join('; ');},secure:true,setCookie(value){writes++;if(q.failAt&&(writes===q.failAt||q.failAlways&&writes>=q.failAt))throw Error('Injected host write failure');const [pair]=value.split(';'),at=pair.indexOf('='),k=pair.slice(0,at),v=pair.slice(at+1);if(value.includes('Max-Age=0'))cookie.delete(k);else cookie.set(k,v);},replaceURL(value){href=value;}};
 const persistence=new BrowserSettings(host),app=new Controller(()=>1,()=>now,testResultHost());app.updateSettings(persistence.resolve().settings);app.dispatch({type:'start'});
 const before={state:app.state,settings:app.settings,results:app.results,cookie:host.cookie,href};
 const codec={async decode(bytes:Uint8Array){checkSize(bytes);if(isSQLite(bytes)){const SQL=await initSqlJs({locateFile:file=>resolve('node_modules/sql.js/dist',file)});return decodeSQLite(bytes,SQL);}return decodeJSON(bytes);},async encode(snapshot:unknown){return encodeJSON(snapshot);}};
 const exchange=new FileExchange(app,persistence,codec);let error='',locked=false;
 let concurrent='';const pending=exchange.restore(q.base64?new Uint8Array(Buffer.from(q.base64,'base64')):new TextEncoder().encode(q.text)),second=exchange.save('json').catch(e=>{concurrent=String(e);});try{app.updateSettings({ghost:'hide'});}catch{locked=true;}
 try{await pending;}catch(e){error=String(e);}await second;
 const after={state:app.state,settings:app.settings,results:app.results,cookie:host.cookie,href};let blockedWritePrevented=false;if(persistence.blocked){const old=writes;try{persistence.save({ghost:'hide'});}catch{blockedWritePrevented=writes===old;}}console.log(JSON.stringify({before,after,error,locked,concurrent,busy:exchange.busy,writes,blocked:persistence.blocked,blockedWritePrevented,settingsLocked:app.settingsLocked}));
}
else if(q.op==='exportCapture'){
 let now=0,release:((bytes:Uint8Array)=>void)|undefined;const app=new Controller(()=>1,()=>now,testResultHost());app.dispatch({type:'start'});
 const codec={async decode(bytes:Uint8Array){checkSize(bytes);if(isSQLite(bytes)){const SQL=await initSqlJs({locateFile:file=>resolve('node_modules/sql.js/dist',file)});return decodeSQLite(bytes,SQL);}return decodeJSON(bytes);},encode(snapshot:unknown){const bytes=encodeJSON(snapshot);return new Promise<Uint8Array>(resolve=>{release=()=>resolve(bytes);});}};
 const exchange=new FileExchange(app,{commit(){}},codec),pending=exchange.save('json');now=300000;app.tick();release!(new Uint8Array());const bytes=await pending;
 console.log(JSON.stringify({snapshot:decodeJSON(bytes),currentResults:app.results,busy:exchange.busy}));
}
else if(q.op==='snapshot'){try{const before=JSON.stringify(q.document),snapshot=validateSnapshot(q.document);console.log(JSON.stringify({snapshot,immutable:before===JSON.stringify(q.document)}));}catch(e){console.log(JSON.stringify({error:String(e)}));}}
else if(q.op==='hostIDs'){Object.defineProperty(crypto,'randomUUID',{value:undefined});console.log(JSON.stringify(Array.from({length:100},()=>newID())));}
else if(q.op==='results'){try{const input=q.results,copy=JSON.stringify(input);const results=q.rank?rank(input):validateResults(input);console.log(JSON.stringify({results,immutable:copy===JSON.stringify(input)}));}catch(e){console.log(JSON.stringify({error:String(e)}));}}
else if(q.op==='session'){let now=0,n=0;const app=new Controller(()=>1,()=>now,{id:()=>`00000000-0000-4000-8000-${String(++n).padStart(12,'0')}`,timestamp:()=>new Date(Date.UTC(2026,0,1)+now).toISOString()});for(const step of q.steps){now=step.at??now;if(step.settings)app.updateSettings(step.settings);else if(step.tick)app.tick();else app.dispatch(step.command);}const copy=app.results;if(copy[0])copy[0].score=123456;console.log(JSON.stringify({state:app.state,results:app.results,settings:app.settings}));}
else if(q.op==='resolveSettings')console.log(JSON.stringify(resolveSettings(q.search??'',q.cookie??'')));
else if(q.op==='settings'){let now=0;const app=new Controller(()=>1,()=>now,testResultHost());const errors=[];for(const step of q.steps??[]){now=step.at??now;try{if(step.settings)app.updateSettings(step.settings);else app.dispatch(step.command);}catch(e){errors.push(String(e));}}console.log(JSON.stringify({state:app.state,settings:app.settings,errors}));}
else if(q.op==='geometry')console.log(JSON.stringify({cells:geometry.cells(q.piece),valid:geometry.valid(q.board??geometry.emptyBoard(),q.piece)}));
else if(q.op==='game'){let state=Object.assign(game.create(q.seed??1),q.fixture??{});const events:game.GameEvent[]=[];let immutable=true;let rules=q.rules;for(const a of q.actions??[]){const before=JSON.stringify(state);if(a.rules)rules=a.rules;const r=game.reduce(state,a,rules);immutable=immutable&&before===JSON.stringify(state);state=r.state;events.push(...r.events);}console.log(JSON.stringify({state,events,immutable}));}
else if(q.op==='source'){let seed=q.seed??1,queue:geometry.Kind[]=[];const draws=[];for(let i=0;i<q.count;i++){const r=source.next(seed,queue);seed=r.seed;queue=r.queue;draws.push(r.kind);}console.log(JSON.stringify(draws));}
else if(q.op==='landing')console.log(JSON.stringify(landing(q.board??geometry.emptyBoard(),q.piece,q.penetrator??false)));
else if(q.op==='clock'){let now=0;const app=new Controller(()=>1,()=>now,testResultHost()),events:game.GameEvent[]=[];app.subscribe((s,e)=>events.push(...e));for(const step of q.steps){now=step.at;app.dispatch(step.command);}console.log(JSON.stringify({state:app.state,events}));}
else if(q.op==='ghostVisible')console.log(JSON.stringify(ghostVisible(q.piece)));
else throw Error('Unknown operation');
