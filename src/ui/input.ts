/** Focus-aware input; repeat events are drained chronologically before host commands/time. */
import type {Controller} from '../app/controller.js';
export function bindInput(app:Controller):{repeat:(now:number)=>void;clear:()=>void}{
 const held=new Map<string,{type:string;next:number}>();
 const map:Record<string,string>={ArrowLeft:'left',ArrowRight:'right',ArrowDown:'down',ArrowUp:'cw',' ':'cw',z:'ccw',r:'start',Enter:'hardDrop',c:'hold',x:'activate'};
 const clear=()=>held.clear();
 app.subscribe(s=>{if(s.status!=='running')clear();});
 const repeat=(now:number)=>{
  if(app.state.status!=='running'){clear();return;}
  while(held.size){const due=[...held.values()].sort((a,b)=>a.next-b.next)[0];if(due.next>now)break;const at=due.next;due.next+=50;app.dispatchAt({type:due.type},at);if(app.state.status!=='running'){clear();break;}}
 };
 app.beforeCommand=repeat;
 window.addEventListener('keydown',e=>{
  if(e.ctrlKey||e.metaKey||e.altKey||(e.target instanceof HTMLElement&&e.target.closest('input,select,textarea,button,[contenteditable="true"]')))return;
  const key=e.key.length===1?e.key.toLowerCase():e.key;let type=map[key];
  if(key==='p')type=app.state.status==='running'?'pause':app.state.status==='paused'?'resume':'';
  if(!type)return;e.preventDefault();if(e.repeat||held.has(key))return;app.dispatch({type});
  if(['left','right','down'].includes(type)&&app.state.status==='running')held.set(key,{type,next:performance.now()+(type==='down'?50:150)});
  if(type==='pause'||type==='start')clear();
 });
 document.addEventListener('focusin',e=>{if(e.target instanceof HTMLElement&&e.target.closest('input,select,textarea,button,[contenteditable="true"]'))clear();});
 window.addEventListener('keyup',e=>{repeat(performance.now());held.delete(e.key);});
 window.addEventListener('blur',()=>{clear();app.dispatch({type:'pause'});});
 document.addEventListener('visibilitychange',()=>{if(document.hidden){clear();app.dispatch({type:'pause'});}});
 return{clear,repeat};
}
