/** Sole command/clock owner; elapsed deadlines and scheduled input precede new commands. */
import {create,reduce,type Command,type GameState,type GameEvent} from '../core/game.js';
export class Controller{
 private current:GameState;
 private lastClock:number;
 private listeners=new Set<(s:GameState,events:GameEvent[])=>void>();
 /** Input adapter drains due repeat events before an external command or frame. */
 beforeCommand:(at:number)=>void=()=>{};
 constructor(private seed:()=>number,private clock:()=>number=()=>0){this.current=create(seed());this.lastClock=clock();}
 get state():GameState{return structuredClone(this.current);}
 subscribe(listener:(s:GameState,events:GameEvent[])=>void):()=>void{this.listeners.add(listener);listener(this.state,[]);return()=>this.listeners.delete(listener);}
 private advance(at:number):GameEvent[]{
  const delta=Math.max(0,at-this.lastClock);this.lastClock=Math.max(at,this.lastClock);
  if(this.current.status!=='running'||!delta)return[];
  const r=reduce(this.current,{type:'advance',ms:delta});this.current=r.state;return r.events;
 }
 private notify(events:GameEvent[]):void{for(const fn of this.listeners)fn(this.state,events);}
 dispatch(command:Command):void{const now=this.clock();this.beforeCommand(now);this.dispatchAt(command,now);}
 /** Scheduled repeats use their monotonic due time, avoiding animation-frame ordering drift. */
 dispatchAt(command:Command,at:number):void{
  const events=this.advance(at),action=command.type==='start'?{...command,seed:this.seed()}:command;
  const result=reduce(this.current,action);this.current=result.state;this.notify([...events,...result.events]);
 }
 tick():void{const now=this.clock();this.beforeCommand(now);const events=this.advance(now);if(this.current.status==='running'||events.length)this.notify(events);}
}
