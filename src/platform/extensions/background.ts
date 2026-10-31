/** No game loop: background coordinates durable acknowledgments and launch only. */
import {Coordinator} from './coordinator.js';
import {extensionAPI,store,type Family} from './api.js';
export function startBackground(family:Family){
 const api=extensionAPI(family),coordinator=new Coordinator(store(family,api.storage.local),store(family,api.storage.session));
 const peers=new Map<string,any>();let next=0;
 coordinator.onChange=view=>{for(const port of peers.values())try{port.postMessage({event:'view',view});}catch{}};
 api.action.onClicked.addListener((tab:any)=>{if(family==='chromium')api.sidePanel.open({windowId:tab.windowId}).catch(console.error);else api.sidebarAction.open().catch(console.error);});
 api.runtime.onConnect.addListener((port:any)=>{
  if(port.name!=='tetris-panel'||port.sender?.id!==api.runtime.id)return;
  const id=String(++next);peers.set(id,port);let yielded:((value:any)=>void)|null=null;
  port.onDisconnect.addListener(()=>{peers.delete(id);yielded?.(null);void coordinator.disconnect(id).catch(console.error);});
  const ready=coordinator.connect(id,()=>new Promise(resolve=>{yielded=resolve;port.postMessage({event:'yield'});}));
  port.onMessage.addListener((message:any)=>{
   if(message?.type==='yielded'){yielded?.(message.session);yielded=null;return;}
   void(async()=>{try{await ready;let value;
    if(message.type==='hello')value={id,view:await coordinator.view()};
    else if(message.type==='commit')value=await coordinator.commit(id,message.sequence,message.session);
    else if(message.type==='claim')value=await coordinator.claim(id);
    else if(message.type==='settings')value=await coordinator.settings(id,message.patch);
    else if(message.type==='seed')value=await coordinator.seed(id,message.search);
    else if(message.type==='restore')value=await coordinator.restore(id,message.snapshot);
    else throw Error('Unknown request');
    port.postMessage({request:message.request,value});
   }catch(e){try{port.postMessage({request:message.request,error:String(e)});}catch{}}})();
  });
 });
}
