/** Browser host adapter. No storage dependency leaks into game/application rules. */
import {resolveSettings,type Resolution} from '../../app/resolve-settings.js';
import {keys,validateSettings,type Settings,type SettingKey} from '../../app/settings.js';
export interface SettingsHost{readonly href:string;readonly cookie:string;readonly secure:boolean;setCookie(value:string):void;replaceURL(value:string):void}
export const browserSettingsHost:SettingsHost={get href(){return location.href;},get cookie(){return document.cookie;},get secure(){return ['https:','app:'].includes(location.protocol);},setCookie(value){document.cookie=value;},replaceURL(value){history.replaceState(null,'',value);}};
export class BrowserSettings{
 constructor(private host:SettingsHost=browserSettingsHost){}
 resolve():Resolution{return resolveSettings(new URL(this.host.href).search,this.host.cookie);}
 private suffix():string{return '; Path=/; SameSite=Lax; Max-Age=31536000'+(this.host.secure?'; Secure':'');}
 save(patch:Partial<Settings>):void{
  validateSettings(patch);const url=new URL(this.host.href);
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
