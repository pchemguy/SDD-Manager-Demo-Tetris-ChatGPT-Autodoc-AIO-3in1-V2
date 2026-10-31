/** Pure game transitions with explicit monotonic gravity and grounded deadlines. */
import {emptyBoard,cells,valid,type Board,type Piece,type Kind} from './geometry.js';
import {landing,deepest} from './landing.js';
import {rotate} from './rotation.js';
import {next} from './source.js';
export interface GameState{board:Board;piece:Piece|null;status:'idle'|'running'|'paused'|'game-over';score:number;lines:number;level:number;time:number;gravityAt:number;seed:number;queue:Kind[];holdKind:Kind|null;heldUsed:boolean;groundedAt:number|null;groundedInterval:number|null;lockAt:number|null;bonuses:number;penetrator:boolean}
export type Rules={lock:'failed'|'interval';hardDropLock:'general'|'immediate';hardDrop?:boolean;hold?:boolean};
export type Command={type:string;ms?:number;seed?:number};
export type GameEvent={type:'lock'|'clear'|'complete';score?:number;lines?:number};
export function create(seed=1):GameState{return{board:emptyBoard(),piece:null,status:'idle',score:0,lines:0,level:1,time:0,gravityAt:1000,seed,queue:[],holdKind:null,heldUsed:false,groundedAt:null,groundedInterval:null,lockAt:null,bonuses:0,penetrator:false};}
export function interval(level:number):number{return Math.max(100,1000*0.8**(level-1));}
function clearGround(s:GameState):void{s.groundedAt=null;s.groundedInterval=null;s.lockAt=null;}
function refresh(s:GameState,rules:Rules):void{
 if(!s.piece||s.status!=='running')return;
 if(s.penetrator?landing(s.board,s.piece,true).y>s.piece.y:valid(s.board,{...s.piece,y:s.piece.y+1})){clearGround(s);return;}
 if(s.groundedAt===null){s.groundedAt=s.time;s.groundedInterval=interval(s.level);}
 s.lockAt=rules.lock==='interval'?s.groundedAt+s.groundedInterval!:null;
}
function draw(s:GameState):void{
 const draw=next(s.seed,s.queue);s.seed=draw.seed;s.queue=draw.queue;
 s.piece={kind:draw.kind,rotation:0,x:3,y:-1};s.penetrator=false;clearGround(s);
}
function complete(s:GameState,events:GameEvent[]):void{s.status='game-over';events.push({type:'complete',score:s.score});}
function spawn(s:GameState,events:GameEvent[]):void{draw(s);if(!valid(s.board,s.piece!))complete(s,events);}
function add(s:GameState,points:number):void{s.score=Math.min(Number.MAX_SAFE_INTEGER,s.score+points);}
function lock(s:GameState,events:GameEvent[],rules:Rules):void{
 if(!s.piece)return;
 if(cells(s.piece).some(([,y])=>y<0)||!valid(s.board,s.piece)){complete(s,events);return;}
 for(const[x,y]of cells(s.piece))s.board[y][x]=s.penetrator?'P':s.piece.kind;
 events.push({type:'lock'});
 const remaining=s.board.filter(row=>row.some(v=>v===null)),count=20-remaining.length;
 if(count===4)s.bonuses=Math.min(3,s.bonuses+1);
 if(count){s.board=[...Array.from({length:count},()=>Array(10).fill(null)),...remaining];add(s,[0,100,300,500,800][count]*s.level);s.lines+=count;s.level=1+Math.floor(s.lines/10);events.push({type:'clear',lines:count});}
 s.heldUsed=false;spawn(s,events);s.gravityAt=s.time+interval(s.level);refresh(s,rules);
}
function down(s:GameState,events:GameEvent[],soft:boolean,rules:Rules):void{
 if(!s.piece)return;const candidate={...s.piece,y:s.piece.y+1};
 if(s.penetrator?landing(s.board,s.piece,true).y>s.piece.y:valid(s.board,candidate)){s.piece=candidate;if(soft)add(s,1);}else if(rules.lock==='failed')lock(s,events,rules);
 refresh(s,rules);
}
export function reduce(state:GameState,action:Command,rules:Rules={lock:'interval',hardDropLock:'general'}):{state:GameState;events:GameEvent[]}{
 let s=structuredClone(state);const events:GameEvent[]=[];
 if(action.type==='start'){s=create(action.seed??s.seed);s.status='running';spawn(s,events);refresh(s,rules);return{state:s,events};}
 if(action.type==='pause'&&s.status==='running'){s.status='paused';return{state:s,events};}
 if(action.type==='resume'&&s.status==='paused'){s.status='running';return{state:s,events};}
 if(s.status!=='running'||!s.piece)return{state:s,events};
 refresh(s,rules);if(s.lockAt!==null&&s.lockAt<=s.time)lock(s,events,rules);
 if(s.status!=='running'||!s.piece)return{state:s,events};
 if(action.type==='advance'){
  const target=s.time+(action.ms??0);if(!Number.isFinite(target)||target<=s.time)return{state:s,events};
  while(s.status==='running'){
   const at=Math.min(s.gravityAt,s.lockAt??Infinity);if(at>target)break;s.time=Math.max(s.time,at);
   if(s.lockAt!==null&&s.lockAt<=s.time)lock(s,events,rules);
   else{down(s,events,false,rules);s.gravityAt=s.time+interval(s.level);}
  }
  if(s.status==='running')s.time=target;
 }else if(action.type==='activate'&&!s.penetrator&&s.bonuses>0&&deepest(s.board,s.piece)){s.penetrator=true;s.bonuses--;
 }else if(action.type==='hardDrop'&&rules.hardDrop!==false){
  const target=landing(s.board,s.piece,s.penetrator);add(s,(target.y-s.piece.y)*2);s.piece=target;refresh(s,rules);if(rules.hardDropLock==='immediate')lock(s,events,rules);
 }else if(action.type==='hold'&&rules.hold!==false&&!s.heldUsed&&!s.penetrator){
  const outgoing=s.piece.kind,stored=s.holdKind;s.holdKind=outgoing;s.heldUsed=true;clearGround(s);
  if(stored){s.piece={kind:stored,rotation:0,x:3,y:-1};if(!valid(s.board,s.piece))complete(s,events);}else spawn(s,events);
 }else if(action.type==='down')down(s,events,true,rules);
 else if(action.type==='left'||action.type==='right'){
  const candidate={...s.piece,x:s.piece.x+(action.type==='left'?-1:1)};if(s.penetrator?deepest(s.board,candidate)!==null:valid(s.board,candidate))s.piece=candidate;
 }else if(action.type==='cw'||action.type==='ccw')s.piece=rotate(s.board,s.piece,action.type==='cw'?1:-1,p=>s.penetrator?deepest(s.board,p)!==null:valid(s.board,p));
 refresh(s,rules);
 return{state:s,events};
}
