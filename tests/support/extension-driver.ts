import {readFileSync} from 'node:fs';
import {Coordinator,type Store} from '../../src/platform/extensions/coordinator.js';
import {create,reduce} from '../../src/core/game.js';
import {validateSession} from '../../src/app/session.js';
import {defaults} from '../../src/app/settings.js';
const q=JSON.parse(readFileSync(0,'utf8'));
class Memory implements Store{data:Record<string,unknown>={};writes=0;fail=false;async get(key:string){return structuredClone(this.data[key]);}async set(key:string,value:unknown){if(this.fail)throw Error('Storage unavailable');this.writes++;this.data[key]=structuredClone(value);}async remove(key:string){delete this.data[key];}}
const local=new Memory(),session=new Memory();
const game=reduce(create(1),{type:'start'}).state;
const saved={game,results:[]};
if(q.mutate)Object.assign(game,q.mutate);
if(q.op==='validation'){let error='';try{validateSession(Object.hasOwn(q,'value')?q.value:saved);}catch(e){error=String(e);}console.log(JSON.stringify({error}));}
else{let yields=0;const c=new Coordinator(local,session),a=await c.connect('a',async()=>{yields++;return{...saved,game:{...game,score:47}};}),b=await c.connect('b',async()=>saved);let rejected=false,error='';
if(q.op==='owner'){await c.commit('a',1,saved);try{await c.commit('b',1,saved);}catch{rejected=true;}const claim=await c.claim('b');try{await c.commit('a',2,saved);}catch{rejected=true;}console.log(JSON.stringify({a,b,claim,yields,rejected,local:local.data,session:session.data}));}
if(q.op==='failure'){await c.commit('a',1,saved);const before=JSON.stringify(session.data);session.fail=true;try{await c.commit('a',2,{...saved,game:{...game,score:55}});}catch(e){error=String(e);}console.log(JSON.stringify({error,unchanged:before===JSON.stringify(session.data),view:await c.view()}));}
if(q.op==='restart'){await c.settings('a',{ghost:'dynamic'});await c.commit('a',1,saved);await c.disconnect('a');const reopened=await c.connect('c',async()=>saved);session.data={};const fresh=await new Coordinator(local,session).connect('fresh',async()=>saved);console.log(JSON.stringify({reopened,fresh,local:local.data}));}
if(q.op==='sequence'){await c.commit('a',2,saved);try{await c.commit('a',1,{...saved,game:{...game,score:999}});}catch(e){error=String(e);}console.log(JSON.stringify({error,view:await c.view()}));}
if(q.op==='restore'){await c.commit('a',1,saved);const snapshot={formatVersion:1,settings:{...defaults,ghost:'hide'},results:[]};await c.restore('a',snapshot);console.log(JSON.stringify({view:await c.view(),local:local.data,session:session.data}));}
if(q.op==='query'){const resolved=await c.seed('a','?ghost=hide&hold=bad');console.log(JSON.stringify({resolved,view:await c.view(),local:local.data}));}
}
