/** Resolve each setting independently, retaining only valid explicit URL writes. */
import {defaults,keys,isValue,type Settings,type SettingKey} from './settings.js';
export interface Resolution{settings:Settings;explicit:Partial<Settings>;invalid:SettingKey[]}
function decode(text:string,plus=false):string|null{try{return decodeURIComponent(plus?text.replace(/\+/g,' '):text);}catch{return null;}}
export function resolveSettings(search:string,cookie:string):Resolution{
 const queries=new Map<string,(string|null)[]>(),cookies=new Map<string,(string|null)[]>();
 for(const segment of search.replace(/^\?/,'').split('&')){if(!segment)continue;const at=segment.indexOf('='),key=decode(at<0?segment:segment.slice(0,at),true);if(key===null)continue;const value=decode(at<0?'':segment.slice(at+1),true);queries.set(key,[...(queries.get(key)??[]),value]);}
 for(const segment of cookie.split(';')){const at=segment.indexOf('=');if(at<0)continue;const key=segment.slice(0,at).trim(),value=decode(segment.slice(at+1).trim());cookies.set(key,[...(cookies.get(key)??[]),value]);}
 const settings={...defaults},explicit:Partial<Settings>={},invalid:SettingKey[]=[];
 for(const key of keys){
  const query=queries.get(key),saved=cookies.get('tetris_'+key);let value:unknown;
  if(query?.length===1&&isValue(key,query[0])){value=query[0];Object.assign(explicit,{[key]:value});}
  else{
   if(query)invalid.push(key);
   if(saved?.length===1&&isValue(key,saved[0]))value=saved[0];
   else if(saved&&!invalid.includes(key))invalid.push(key);
  }
  if(value!==undefined)Object.assign(settings,{[key]:value});
 }
 return{settings,explicit,invalid};
}
