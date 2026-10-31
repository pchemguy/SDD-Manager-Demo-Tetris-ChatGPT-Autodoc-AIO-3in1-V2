/** Sole command/clock owner; elapsed deadlines and scheduled input precede new commands. */
import {create,reduce,type Command,type GameState,type GameEvent} from '../core/game.js';
import {validateSnapshot,type Snapshot} from './snapshot.js';
import {rank,type Result,type ResultHost} from './results.js';
import {defaults,validateSettings,type Settings} from './settings.js';
export class Controller{
 settingsLocked=false;
 snapshot():Snapshot{return validateSnapshot({formatVersion:1,results:this.results,settings:this.settings});}
 replaceSnapshot(input:unknown):void{
  const candidate=validateSnapshot(input),now=this.clock();this.beforeCommand(now);const events=this.advance(now);
  this.accept(reduce(this.current,{type:'pause'},this.rules));this.config=candidate.settings;this.history=candidate.results;this.notify(events);
 }
 private history:Result[]=[];
 private completionRecorded=false;
 get results():Result[]{return this.history.map(r=>({...r}));}
 private accept(result:{state:GameState;events:GameEvent[]}):void{
  this.current=result.state;
  for(const event of result.events)if(event.type==='complete'&&!this.completionRecorded){
   this.history=rank([...this.history,{id:this.resultHost.id(),score:event.score!,timestamp:this.resultHost.timestamp()}]);this.completionRecorded=true;
  }
 }
 onSettingsChange:(patch:Partial<Settings>)=>void=()=>{};
 private config:Settings={...defaults};
 get settings():Settings{return {...this.config};}
 private get rules(){return{lock:this.config.lock,hardDropLock:this.config.hardDropLock,hardDrop:this.config.hardDrop==='on',hold:this.config.hold==='on'};}
 updateSettings(patch:unknown):void{
  if(this.settingsLocked)throw Error('A file operation is in progress');
  const parsed=validateSettings(patch),now=this.clock();this.beforeCommand(now);const events=this.advance(now);
  this.config={...this.config,...parsed};const result=reduce(this.current,{type:'configure'},this.rules);this.accept(result);this.notify([...events,...result.events]);this.onSettingsChange(parsed);
 }
 private current:GameState;
 private lastClock:number;
 private listeners=new Set<(s:GameState,events:GameEvent[])=>void>();
 /** Input adapter drains due repeat events before an external command or frame. */
 beforeCommand:(at:number)=>void=()=>{};
 constructor(private seed:()=>number,private clock:()=>number,private resultHost:ResultHost){this.current=create(seed());this.lastClock=clock();}
 get state():GameState{return structuredClone(this.current);}
 subscribe(listener:(s:GameState,events:GameEvent[])=>void):()=>void{this.listeners.add(listener);listener(this.state,[]);return()=>this.listeners.delete(listener);}
 private advance(at:number):GameEvent[]{
  const delta=Math.max(0,at-this.lastClock);this.lastClock=Math.max(at,this.lastClock);
  if(this.current.status!=='running'||!delta)return[];
  const r=reduce(this.current,{type:'advance',ms:delta},this.rules);this.accept(r);return r.events;
 }
 private notify(events:GameEvent[]):void{for(const fn of this.listeners)fn(this.state,events);}
 dispatch(command:Command):void{const now=this.clock();this.beforeCommand(now);this.dispatchAt(command,now);}
 /** Scheduled repeats use their monotonic due time, avoiding animation-frame ordering drift. */
 dispatchAt(command:Command,at:number):void{
  const events=this.advance(at),action=command.type==='start'?{...command,seed:this.seed()}:command;
  if(command.type==='start')this.completionRecorded=false;
  const result=reduce(this.current,action,this.rules);this.accept(result);this.notify([...events,...result.events]);
 }
 tick():void{const now=this.clock();this.beforeCommand(now);const events=this.advance(now);if(this.current.status==='running'||events.length)this.notify(events);}
}
