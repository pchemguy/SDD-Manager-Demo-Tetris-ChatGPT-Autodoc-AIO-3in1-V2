/** Keyboard focus/repeat policy; only handled game keys suppress native defaults. */
import type {Controller} from '../app/controller.js';
export function bindInput(app:Controller):{repeat:(now:number)=>void;clear:()=>void}{
 const held=new Map<string,{type:string;next:number}>();
 const map:Record<string,string>={ArrowLeft:'left',ArrowRight:'right',ArrowDown:'down',ArrowUp:'cw',' ':'cw',z:'ccw',r:'start'};
 const clear=()=>held.clear();
 window.addEventListener('keydown',e=>{
  if(e.ctrlKey||e.metaKey||e.altKey||(e.target instanceof HTMLElement&&e.target.closest('input,select,textarea,button,[contenteditable="true"]')))return;
  const key=e.key.length===1?e.key.toLowerCase():e.key;let type=map[key];
  if(key==='p')type=app.state.status==='running'?'pause':app.state.status==='paused'?'resume':'';
  if(!type)return;e.preventDefault();if(e.repeat||held.has(key))return;app.dispatch({type});
  if(['left','right','down'].includes(type)&&app.state.status==='running')held.set(key,{type,next:performance.now()+(type==='down'?50:150)});
  if(type==='pause'||type==='start')clear();
 });
 window.addEventListener('keyup',e=>held.delete(e.key));
 window.addEventListener('blur',()=>{clear();app.dispatch({type:'pause'});});
 document.addEventListener('visibilitychange',()=>{if(document.hidden){clear();app.dispatch({type:'pause'});}});
 return{clear,repeat(now){if(app.state.status!=='running'){clear();return;}for(const value of held.values())while(value.next<=now){app.dispatch({type:value.type});value.next+=50;}}};
}
