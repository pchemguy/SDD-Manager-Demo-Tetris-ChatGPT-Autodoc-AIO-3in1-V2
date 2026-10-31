/** Browser host adapter. No storage dependency leaks into game/application rules. */
import {resolveSettings,type Resolution} from '../../app/resolve-settings.js';
import {keys,validateSettings,type Settings,type SettingKey} from '../../app/settings.js';
export interface SettingsHost{readonly href:string;readonly cookie:string;readonly secure:boolean;setCookie(value:string):void;replaceURL(value:string):void}
export const browserSettingsHost:SettingsHost={get href(){return location.href;},get cookie(){return document.cookie;},get secure(){return ['https:','app:'].includes(location.protocol);},setCookie(value){document.cookie=value;},replaceURL(value){history.replaceState(null,'',value);}};
export class BrowserSettings{
 private failedRollback=false;
 get blocked():boolean{return this.failedRollback;}
 private assertWritable():void{if(this.failedRollback)throw Error('Persistence blocked after rollback failure; reload to reconcile');}
 /** A validated restore writes all values, with explicit value/URL rollback on host failure. */
 commit(settings:Settings):void{
  validateSettings(settings,true);this.assertWritable();const href=this.host.href,before=new Map<SettingKey,string|undefined>();
  const read=(key:SettingKey)=>{const name='tetris_'+key,values=this.host.cookie.split(';').map(s=>s.trim()).filter(s=>s.startsWith(name+'='));if(values.length>1)throw Error('Ambiguous saved cookie: '+key);return values[0]?.slice(name.length+1);};
  for(const key of keys)before.set(key,read(key));
  try{this.save(settings);}catch(error){
   let failed=false;
   for(const key of keys){const value=before.get(key);try{this.host.setCookie('tetris_'+key+'='+(value??'')+(value===undefined?this.suffix().replace('Max-Age=31536000','Max-Age=0'):this.suffix()));}catch{failed=true;}}
   try{this.host.replaceURL(href);}catch{failed=true;}
   try{if(this.host.href!==href||keys.some(key=>read(key)!==before.get(key)))failed=true;}catch{failed=true;}
   if(failed){this.failedRollback=true;throw Error('Persistence write failed; rollback could not be confirmed. Reload to reconcile.');}
   throw Error('Restore persistence failed; previous values restored: '+String(error));
  }
 }

 constructor(private host:SettingsHost=browserSettingsHost){}
 resolve():Resolution{return resolveSettings(new URL(this.host.href).search,this.host.cookie);}
 private suffix():string{return '; Path=/; SameSite=Lax; Max-Age=31536000'+(this.host.secure?'; Secure':'');}
 save(patch:Partial<Settings>):void{
  this.assertWritable();validateSettings(patch);const url=new URL(this.host.href);
  for(const key of Object.keys(patch) as SettingKey[]){
   const value=patch[key]!,name='tetris_'+key;
   this.host.setCookie(name+'='+encodeURIComponent(value)+this.suffix());
   const values=this.host.cookie.split(';').map(s=>s.trim()).filter(s=>s.startsWith(name+'='));
   if(values.length!==1||values[0]!==name+'='+encodeURIComponent(value))throw Error('Settings persistence could not be confirmed: '+key+' cookie');
   url.searchParams.set(key,value);
  }
  if(Object.keys(patch).length){this.host.replaceURL(url.href);if(this.host.href!==url.href)throw Error('Settings persistence could not be confirmed: URL');}
 }
 /** Startup saves explicit URL values but preserves the supplied URL verbatim. */
 initialize():Resolution{
  const result=this.resolve();
  for(const key of keys){const value=result.explicit[key];if(value===undefined)continue;
   const name='tetris_'+key;this.host.setCookie(name+'='+encodeURIComponent(value)+this.suffix());
   const values=this.host.cookie.split(';').map(s=>s.trim()).filter(s=>s.startsWith(name+'='));
   if(values.length!==1||values[0]!==name+'='+encodeURIComponent(value))throw Error('Settings persistence could not be confirmed: '+key+' cookie');
  }
  return result;
 }
}
