/** Serialized ownership and storage only: this module never imports a game transition. */
import {paused,validateSession,type Session} from '../../app/session.js';
import {defaults,keys,isValue,validateSettings,type Settings} from '../../app/settings.js';
import {resolveSettings} from '../../app/resolve-settings.js';
import {validateSnapshot,type Snapshot} from '../../app/snapshot.js';
export interface Store{get(key:string):Promise<unknown>;set(key:string,value:unknown):Promise<void>;remove(key:string):Promise<void>}
export interface View{owner:string|null;generation:number;session:Session|null;settings:Settings;notice:string}
type Peer={yield:()=>Promise<Session|null>;sequence:number};
function equal(a:unknown,b:unknown):boolean{
 if(Object.is(a,b))return true;
 if(!a||!b||typeof a!=='object'||typeof b!=='object'||Array.isArray(a)!==Array.isArray(b))return false;
 const x=a as Record<string,unknown>,y=b as Record<string,unknown>,names=Object.keys(x).sort();
 return names.join()===Object.keys(y).sort().join()&&names.every(k=>equal(x[k],y[k]));
}
export class Coordinator{
 private blocked=false;private owner:string|null=null;private generation=0;private saved:Session|null=null;private config:Settings={...defaults};private notice='';private peers=new Map<string,Peer>();
 private writes:Promise<unknown>=Promise.resolve();private transfers:Promise<unknown>=Promise.resolve();private ready:Promise<void>;
 onChange:(view:View)=>void=()=>{};
 constructor(private local:Store,private transient:Store){this.ready=this.load();void this.ready.catch(()=>{});}
 private async load(){const [config,state]=await Promise.all([this.local.get('settings'),this.transient.get('session')]);
  if(config!==undefined){const c=config as {formatVersion:number;settings:Record<string,unknown>};try{
   if(c.formatVersion!==1||!c.settings||typeof c.settings!=='object'||Array.isArray(c.settings))throw Error();
   const invalid:string[]=[];for(const key of keys){if(isValue(key,c.settings[key]))Object.assign(this.config,{[key]:c.settings[key]});else invalid.push(key);}
   if(invalid.length)this.notice='Invalid saved settings: '+invalid.join(', ')+'. Defaults applied only to those values.';
  }catch{this.notice='Invalid saved settings record; defaults applied.';}}
  if(state!==undefined){const s=state as {formatVersion:number;generation:number;session:unknown};try{if(s.formatVersion!==1||!Number.isSafeInteger(s.generation)||s.generation<0)throw Error();this.saved=paused(s.session);this.generation=s.generation;this.notice=[this.notice,'Recovered last confirmed session, paused. Recent unconfirmed input may be lost.'].filter(Boolean).join(' ');}catch{this.notice='Invalid session data; start a new game.';}}
 }
 private serial<T>(fn:()=>Promise<T>):Promise<T>{const p=this.writes.then(async()=>{await this.ready;return fn();});this.writes=p.catch(()=>{});return p;}
 async view():Promise<View>{await this.ready;return structuredClone({owner:this.owner,generation:this.generation,session:this.saved,settings:this.config,notice:this.notice});}
 private async publish(){const view=await this.view();this.onChange(view);return view;}
 private require(id:string){if(this.blocked)throw Error('Storage recovery is blocked. Reload the extension before continuing.');if(this.owner!==id||!this.peers.has(id))throw Error('This panel does not own the game. Use Start to take control.');}
 private async checked(store:Store,key:string,value:unknown){await store.set(key,value);if(!equal(await store.get(key),value))throw Error('Storage readback failed');}
 private async save(session:Session){const generation=this.generation+1;await this.checked(this.transient,'session',{formatVersion:1,generation,session});this.saved=structuredClone(session);this.generation=generation;}
 async connect(id:string,onYield:()=>Promise<Session|null>):Promise<View>{return this.serial(async()=>{if(this.peers.has(id))throw Error('Duplicate panel');this.peers.set(id,{yield:onYield,sequence:0});if(!this.owner&&!this.blocked)this.owner=id;return this.publish();});}
 async commit(id:string,sequence:number,input:unknown):Promise<View>{const candidate=validateSession(input);return this.serial(async()=>{this.require(id);const peer=this.peers.get(id)!;if(!Number.isSafeInteger(sequence)||sequence<=peer.sequence)throw Error('Stale session sequence');await this.save(candidate);peer.sequence=sequence;return this.publish();});}
 async settings(id:string,patch:unknown):Promise<View>{const parsed=validateSettings(patch);return this.serial(async()=>{this.require(id);const settings={...this.config,...parsed};await this.checked(this.local,'settings',{formatVersion:1,settings});this.config=settings;return this.publish();});}
 async seed(id:string,search:string){const initial=await this.view(),cookie=keys.map(k=>'tetris_'+k+'='+initial.settings[k]).join('; '),resolved=resolveSettings(search,cookie);if(Object.keys(resolved.explicit).length)await this.settings(id,resolved.explicit);return resolved;}
 async claim(id:string):Promise<View>{const p=this.transfers.then(async()=>{
  await this.ready;if(this.blocked)throw Error('Storage recovery is blocked. Reload the extension before continuing.');if(!this.peers.has(id))throw Error('Disconnected panel');if(this.owner===id)return this.view();
  const old=this.owner,peer=old?this.peers.get(old):undefined;let final:Session|null=null;
  if(peer){let timer:ReturnType<typeof setTimeout>|undefined;try{final=await Promise.race([peer.yield(),new Promise<never>((_,reject)=>{timer=setTimeout(()=>reject(Error('Owner did not respond')),1500);})]);}catch{this.notice='Previous panel unavailable. Recovered last confirmed state, paused.';}finally{clearTimeout(timer);}}
  return this.serial(async()=>{if(!this.peers.has(id))throw Error('Disconnected panel');if(final)await this.save(paused(final));else if(this.saved)await this.save(paused(this.saved));this.owner=id;return this.publish();});
 });this.transfers=p.catch(()=>{});return p;}
 async disconnect(id:string):Promise<void>{await this.serial(async()=>{this.peers.delete(id);if(this.owner===id){this.owner=null;if(this.saved){try{await this.save(paused(this.saved));}catch{this.saved=paused(this.saved);this.notice='Storage failed. Last confirmed session is paused; reopen to recover.';}}}await this.publish();});}
 async restore(id:string,input:unknown):Promise<View>{const snapshot=validateSnapshot(input);return this.serial(async()=>{this.require(id);if(!this.saved)throw Error('Session has not been initialized');const previousConfig=this.config,previousSession=this.saved,previousGeneration=this.generation,oldLocal=await this.local.get('settings'),oldTransient=await this.transient.get('session');
  try{await this.checked(this.local,'settings',{formatVersion:1,settings:snapshot.settings});if(this.saved)await this.save({...paused(this.saved),results:snapshot.results});this.config=snapshot.settings;}
  catch(e){try{for(const [store,key,value]of [[this.local,'settings',oldLocal],[this.transient,'session',oldTransient]] as const){if(value===undefined)await store.remove(key);else await this.checked(store,key,value);}this.config=previousConfig;this.saved=previousSession;this.generation=previousGeneration;}catch{this.blocked=true;this.owner=null;this.notice='Restore rollback could not be confirmed. Reload the extension before continuing.';await this.publish();}throw e;}
  return this.publish();
 });}
}
