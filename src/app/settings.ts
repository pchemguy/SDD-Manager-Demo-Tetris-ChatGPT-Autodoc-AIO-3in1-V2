/** Canonical, host-independent configuration; all boundaries reject coercion. */
export const domains={ghost:['hide','dynamic','show'],hardDrop:['on','off'],next:['on','off'],hardDropLock:['general','immediate'],lock:['failed','interval'],hold:['on','off']} as const;
export type Settings={[K in keyof typeof domains]:(typeof domains)[K][number]};
export type SettingKey=keyof Settings;
export const defaults:Settings={ghost:'show',hardDrop:'on',next:'on',hardDropLock:'general',lock:'interval',hold:'on'};
export const keys=Object.keys(domains) as SettingKey[];
export function isValue(key:SettingKey,value:unknown):boolean{return typeof value==='string'&&(domains[key] as readonly string[]).includes(value);}
export function validateSettings(input:unknown,complete=false):Partial<Settings>{
 if(!input||typeof input!=='object'||Array.isArray(input))throw Error('Settings must be an object');
 const obj=input as Record<string,unknown>;
 if(Object.keys(obj).some(k=>!keys.includes(k as SettingKey)||!isValue(k as SettingKey,obj[k]))||complete&&keys.some(k=>!Object.hasOwn(obj,k)))throw Error('Invalid or missing setting');
 return {...obj} as Partial<Settings>;
}
