/** Deterministic subprocess bridge; excluded from production bundles. */
import {Controller} from '../../src/app/controller.js';
import {readFileSync} from 'node:fs';
import {ghostVisible} from '../../src/core/ghost.js';
import {landing} from '../../src/core/landing.js';
import * as source from '../../src/core/source.js';
import * as game from '../../src/core/game.js';
import * as geometry from '../../src/core/geometry.js';
const q=JSON.parse(readFileSync(0,'utf8'));
if(q.op==='geometry')console.log(JSON.stringify({cells:geometry.cells(q.piece),valid:geometry.valid(q.board??geometry.emptyBoard(),q.piece)}));
else if(q.op==='game'){let state=Object.assign(game.create(q.seed??1),q.fixture??{});const events:game.GameEvent[]=[];let immutable=true;let rules=q.rules;for(const a of q.actions??[]){const before=JSON.stringify(state);if(a.rules)rules=a.rules;const r=game.reduce(state,a,rules);immutable=immutable&&before===JSON.stringify(state);state=r.state;events.push(...r.events);}console.log(JSON.stringify({state,events,immutable}));}
else if(q.op==='source'){let seed=q.seed??1,queue:geometry.Kind[]=[];const draws=[];for(let i=0;i<q.count;i++){const r=source.next(seed,queue);seed=r.seed;queue=r.queue;draws.push(r.kind);}console.log(JSON.stringify(draws));}
else if(q.op==='landing')console.log(JSON.stringify(landing(q.board??geometry.emptyBoard(),q.piece,q.penetrator??false)));
else if(q.op==='clock'){let now=0;const app=new Controller(()=>1,()=>now),events:game.GameEvent[]=[];app.subscribe((s,e)=>events.push(...e));for(const step of q.steps){now=step.at;app.dispatch(step.command);}console.log(JSON.stringify({state:app.state,events}));}
else if(q.op==='ghostVisible')console.log(JSON.stringify(ghostVisible(q.piece)));
else throw Error('Unknown operation');
