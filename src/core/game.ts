/** Pure classic game transitions; only explicit commands advance game time. */
import {emptyBoard,cells,valid,type Board,type Piece,type Kind} from './geometry.js';
import {rotate} from './rotation.js';
import {next} from './source.js';
export interface GameState{board:Board;piece:Piece|null;status:'idle'|'running'|'paused'|'game-over';score:number;lines:number;level:number;time:number;gravityAt:number;seed:number;queue:Kind[];holdKind:Kind|null;heldUsed:boolean}
export type Command={type:string;ms?:number;seed?:number};
export type GameEvent={type:'lock'|'clear'|'complete';score?:number;lines?:number};
export function create(seed=1):GameState{return{board:emptyBoard(),piece:null,status:'idle',score:0,lines:0,level:1,time:0,gravityAt:1000,seed,queue:[],holdKind:null,heldUsed:false};}
export function interval(level:number):number{return Math.max(100,1000*0.8**(level-1));}
function draw(s:GameState):void{
 const draw=next(s.seed,s.queue);s.seed=draw.seed;s.queue=draw.queue;
 s.piece={kind:draw.kind,rotation:0,x:3,y:-1};
}
function complete(s:GameState,events:GameEvent[]):void{s.status='game-over';events.push({type:'complete',score:s.score});}
function spawn(s:GameState,events:GameEvent[]):void{draw(s);if(!valid(s.board,s.piece!))complete(s,events);}
function add(s:GameState,points:number):void{s.score=Math.min(Number.MAX_SAFE_INTEGER,s.score+points);}
function lock(s:GameState,events:GameEvent[]):void{
 if(!s.piece)return;
 if(cells(s.piece).some(([,y])=>y<0)){complete(s,events);return;}
 for(const[x,y]of cells(s.piece))s.board[y][x]=s.piece.kind;
 events.push({type:'lock'});
 const remaining=s.board.filter(row=>row.some(v=>v===null)),count=20-remaining.length;
 if(count){s.board=[...Array.from({length:count},()=>Array(10).fill(null)),...remaining];add(s,[0,100,300,500,800][count]*s.level);s.lines+=count;s.level=1+Math.floor(s.lines/10);events.push({type:'clear',lines:count});}
 s.heldUsed=false;spawn(s,events);s.gravityAt=s.time+interval(s.level);
}
function down(s:GameState,events:GameEvent[],soft:boolean):void{
 if(!s.piece)return;const candidate={...s.piece,y:s.piece.y+1};
 if(valid(s.board,candidate)){s.piece=candidate;if(soft)add(s,1);}else lock(s,events);
}
export function reduce(state:GameState,action:Command):{state:GameState;events:GameEvent[]}{
 let s=structuredClone(state);const events:GameEvent[]=[];
 if(action.type==='start'){s=create(action.seed??s.seed);s.status='running';spawn(s,events);return{state:s,events};}
 if(action.type==='pause'&&s.status==='running'){s.status='paused';return{state:s,events};}
 if(action.type==='resume'&&s.status==='paused'){s.status='running';return{state:s,events};}
 if(s.status!=='running'||!s.piece)return{state:s,events};
 if(action.type==='advance'){
  const ms=action.ms??0;if(!Number.isFinite(ms)||ms<=0)return{state:s,events};
  const target=s.time+ms;
  while(s.status==='running'&&s.gravityAt<=target){s.time=s.gravityAt;down(s,events,false);if(s.gravityAt<=s.time)s.gravityAt=s.time+interval(s.level);}
  if(s.status==='running')s.time=target;
 }else if(action.type==='hold'&&!s.heldUsed){
  const outgoing=s.piece.kind,stored=s.holdKind;s.holdKind=outgoing;s.heldUsed=true;
  if(stored){s.piece={kind:stored,rotation:0,x:3,y:-1};if(!valid(s.board,s.piece))complete(s,events);}else spawn(s,events);
 }else if(action.type==='down')down(s,events,true);
 else if(action.type==='left'||action.type==='right'){
  const next={...s.piece,x:s.piece.x+(action.type==='left'?-1:1)};if(valid(s.board,next))s.piece=next;
 }else if(action.type==='cw'||action.type==='ccw'){
  s.piece=rotate(s.board,s.piece,action.type==='cw'?1:-1);
 }
 return{state:s,events};
}
