/** Transient extension recovery data. No clock runs while its document is absent. */
import {create,type GameState} from '../core/game.js';
import {cells,valid,type Kind} from '../core/geometry.js';
import {deepest} from '../core/landing.js';
import {validateResults,rank,type Result} from './results.js';
export interface Session{game:GameState;results:Result[]}
const kinds=['I','O','T','S','Z','J','L'];
export function validateSession(input:unknown):Session{
 const fail=():never=>{throw Error('Invalid session snapshot');};
 if(!input||typeof input!=='object'||Array.isArray(input))return fail();
 const root=input as Record<string,unknown>;
 if(Object.keys(root).sort().join()!=='game,results'||!root.game||typeof root.game!=='object')return fail();
 const s=structuredClone(root.game) as GameState;
 if(Object.keys(s).sort().join()!==Object.keys(create()).sort().join())return fail();
 if(!Array.isArray(s.board)||s.board.length!==20||s.board.some(row=>!Array.isArray(row)||row.length!==10||row.some(v=>v!==null&&v!=='P'&&!kinds.includes(v))))return fail();
 if(!['idle','running','paused','game-over'].includes(s.status))return fail();
 for(const key of ['score','lines','level','seed','bonuses'] as const)if(!Number.isSafeInteger(s[key])||s[key]<0)return fail();
 if(s.level!==1+Math.floor(s.lines/10)||s.seed>0xffffffff||s.bonuses>3)return fail();
 if(typeof s.heldUsed!=='boolean'||typeof s.penetrator!=='boolean'||s.holdKind!==null&&!kinds.includes(s.holdKind))return fail();
 if(!Array.isArray(s.queue)||s.queue.length>7||new Set(s.queue).size!==s.queue.length||s.queue.some(k=>!kinds.includes(k)))return fail();
 for(const key of ['time','gravityAt'] as const)if(typeof s[key]!=='number'||!Number.isFinite(s[key])||s[key]<0)return fail();
 for(const key of ['groundedAt','groundedInterval','lockAt'] as const)if(s[key]!==null&&(typeof s[key]!=='number'||!Number.isFinite(s[key])||s[key]!<0))return fail();
 if((s.groundedAt===null)!==(s.groundedInterval===null)||s.groundedAt!==null&&(s.groundedAt>s.time||s.groundedInterval!<100||s.groundedInterval!>1000)||s.lockAt!==null&&(s.groundedAt===null||s.lockAt!==s.groundedAt+s.groundedInterval!))return fail();
 if(s.piece!==null){const p=s.piece;
  if(typeof p!=='object'||Object.keys(p).sort().join()!=='kind,rotation,x,y'||!kinds.includes(p.kind)||!Number.isInteger(p.rotation)||p.rotation<0||p.rotation>3||!Number.isInteger(p.x)||!Number.isInteger(p.y))return fail();
  if(cells(p).some(([x,y])=>x<0||x>=10||y< -2||y>=20))return fail();
  if(s.status!=='game-over'&&(s.penetrator?!deepest(s.board,p):!valid(s.board,p)))return fail();
 }else if(s.status!=='idle')return fail();
 if(s.status==='idle'&&s.piece!==null)return fail();
 return{game:s,results:rank(validateResults(root.results))};
}
export function paused(input:unknown):Session{const s=validateSession(input);if(s.game.status==='running')s.game.status='paused';return s;}
