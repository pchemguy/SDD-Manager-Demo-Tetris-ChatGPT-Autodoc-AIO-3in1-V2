/** Foreground owns commands. Background acknowledges every accepted snapshot without ticking. */
import {extensionAPI,type Family} from './api.js';
import type {View} from './coordinator.js';
import type {Session} from '../../app/session.js';
import {Controller} from '../../app/controller.js';
import {FileExchange} from '../../app/files.js';
import {browserCodec} from '../browser/codec.js';
import {downloadFile} from '../browser/files.js';
import {seed,resultHost} from '../browser/host.js';
import {mount} from '../../ui/view.js';
import {bindInput} from '../../ui/input.js';
import {bindFileControls} from '../../ui/files.js';
import '../../ui/styles.css';
export async function startPanel(family:Family):Promise<void>{
 const api=extensionAPI(family),port=api.runtime.connect({name:'tetris-panel'});let diagnostic='';let request=0,sequence=0,id='',owner=false,muted=true,failed=false,transferring=false,claiming=false;
 const pending=new Map<number,{resolve:(value:any)=>void;reject:(e:Error)=>void;timer:ReturnType<typeof setTimeout>}>();
 const app=new Controller(seed,()=>performance.now(),resultHost);let chain:Promise<void>=Promise.resolve(),queued=0,exchange:FileExchange|undefined,input:ReturnType<typeof bindInput>|undefined;
 const notice=(text:string)=>{let node=document.querySelector('#host-notice');if(!node){node=document.createElement('p');node.id='host-notice';node.setAttribute('role','status');document.querySelector('#app')!.prepend(node);}node.textContent=text;};
 const capture=():Session=>({game:app.state,results:app.results});
 const rpc=(type:string,data:object={}):Promise<any>=>new Promise((resolve,reject)=>{const key=++request;const timer=setTimeout(()=>{pending.delete(key);reject(Error('Extension storage acknowledgment timed out'));},10000);pending.set(key,{resolve,reject,timer});try{port.postMessage({request:key,type,...data});}catch(e){clearTimeout(timer);pending.delete(key);reject(Error(String(e)));}});
 const controls=()=>{document.querySelectorAll<HTMLButtonElement|HTMLSelectElement>('#start,#setting-controls select,#save,#restore').forEach(node=>{node.disabled=!owner||failed||transferring||Boolean(exchange?.busy);});const pause=document.querySelector<HTMLButtonElement>('#pause');if(pause)pause.disabled=failed||transferring;};
 const stop=(e:unknown)=>{failed=true;const prior=muted;muted=true;app.dispatch({type:'pause'});muted=prior;input?.clear();notice('Session storage unavailable. Game paused. Reopen the panel to recover the last confirmed state. '+String(e));controls();};
 const apply=(view:View)=>{if(!id)return;const wasOwner=owner;owner=view.owner===id;
  if(!owner||!wasOwner){muted=true;if(view.session)app.restoreSession(view.session,view.settings);else app.updateSettings(view.settings);muted=false;}
  if(view.notice)notice(view.notice);else if(!owner)notice('Read-only panel. Use Start or P to take control and resume.');else if(!transferring)notice(diagnostic);controls();
 };
 port.onMessage.addListener((message:any)=>{
  if(message.event==='view'){if(!exchange?.busy&&!transferring)apply(message.view);return;}
  if(message.event==='yield'){void(async()=>{transferring=true;app.dispatch({type:'pause'});input?.clear();controls();try{while(exchange?.busy)await new Promise(resolve=>setTimeout(resolve,10));await chain;port.postMessage({type:'yielded',session:capture()});}catch{port.postMessage({type:'yielded',session:null});}finally{owner=false;transferring=false;controls();}})();return;}
  const waiter=pending.get(message.request);if(waiter){clearTimeout(waiter.timer);pending.delete(message.request);if(message.error)waiter.reject(Error(message.error));else waiter.resolve(message.value);}
 });
 port.onDisconnect.addListener(()=>{for(const waiter of pending.values()){clearTimeout(waiter.timer);waiter.reject(Error('Background connection closed'));}pending.clear();stop('Connection closed.');});
 const hello=await rpc('hello');id=hello.id;owner=hello.view.owner===id;
 if(owner){const resolved=await rpc('seed',{search:location.search});if(resolved.invalid.length)diagnostic='Invalid configuration: '+resolved.invalid.join(', ');hello.view=await rpc('claim');}
 app.updateSettings(hello.view.settings);if(hello.view.session)app.restoreSession(hello.view.session,hello.view.settings);
 mount(document.querySelector<HTMLElement>('#app')!,app);document.querySelector('.file-controls')!.append(document.querySelector('#notice')!);if(hello.view.notice||diagnostic)notice([hello.view.notice,diagnostic].filter(Boolean).join(' '));
 const enqueue=(work:()=>Promise<unknown>)=>{queued++;chain=chain.then(async()=>{if(failed)return;await work();}).then(()=>{queued--;}).catch(e=>{queued--;stop(e);});if(queued>30&&app.state.status==='running'){app.dispatch({type:'pause'});notice('Storage is catching up. Game paused; wait before resuming.');}return chain;};
 app.subscribe(()=>{if(!muted&&owner&&!failed){const session=capture(),n=++sequence;void enqueue(()=>rpc('commit',{sequence:n,session}));}controls();});
 app.authorize=command=>{
  if(muted)return true;if(failed)return command.type==='pause';if(owner)return !transferring||command.type==='pause';
  if((command.type==='resume'||command.type==='start')&&!claiming){claiming=true;void(async()=>{try{const view:View=await rpc('claim');apply(view);if(!owner)throw Error('Control was not granted');const seeded=await rpc('seed',{search:location.search});muted=true;app.updateSettings(seeded.settings);muted=false;app.dispatch({type:command.type==='start'?'start':app.state.status==='paused'?'resume':'start'});}catch(e){stop(e);}finally{claiming=false;}})();}return false;
 };
 app.onSettingsChange=patch=>{if(!muted&&owner)void enqueue(()=>rpc('settings',{patch}));};
 exchange=new FileExchange(app,{async commit(_settings,snapshot){if(!owner||failed)throw Error('Take control before restoring');await chain;await rpc('restore',{snapshot});}},browserCodec);
 bindFileControls(document.querySelector<HTMLElement>('#app')!,exchange,downloadFile);const onBusy=exchange.onBusy;exchange.onBusy=busy=>{onBusy(busy);controls();};
 input=bindInput(app);muted=false;
 if(owner){const session=capture(),n=++sequence;void enqueue(()=>rpc('commit',{sequence:n,session}));}
 else notice('Read-only panel. Use Start or P to take control and resume.');controls();
 let previous=0;function frame(at:number){if(at-previous>=50){previous=at;app.tick();}requestAnimationFrame(frame);}requestAnimationFrame(frame);
 window.addEventListener('pagehide',()=>{app.dispatch({type:'pause'});input?.clear();});
}
