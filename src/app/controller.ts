/** Sole application command owner; views receive detached read-only snapshots. */
import {create,reduce,type Command,type GameState,type GameEvent} from '../core/game.js';
export class Controller{
 private current:GameState;
 private listeners=new Set<(s:GameState,events:GameEvent[])=>void>();
 constructor(private seed:()=>number){this.current=create(seed());}
 get state():GameState{return structuredClone(this.current);}
 subscribe(listener:(s:GameState,events:GameEvent[])=>void):()=>void{this.listeners.add(listener);listener(this.state,[]);return()=>this.listeners.delete(listener);}
 dispatch(command:Command):void{
  const action=command.type==='start'?{...command,seed:this.seed()}:command;
  const result=reduce(this.current,action);this.current=result.state;
  for(const fn of this.listeners)fn(this.state,result.events);
 }
 tick(ms:number):void{if(this.current.status==='running')this.dispatch({type:'advance',ms});}
}
