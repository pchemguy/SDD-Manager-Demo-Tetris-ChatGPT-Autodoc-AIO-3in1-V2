/** Explicit family avoids mistaking modern Chromium's browser alias for Firefox. */
export type Family='chromium'|'firefox';
export function extensionAPI(family:Family){const globals=globalThis as unknown as Record<string,any>,api=globals[family==='chromium'?'chrome':'browser'];if(!api?.runtime||!api?.storage)throw Error('Extension API unavailable');return api;}
export function call(family:Family,target:any,name:string,...args:any[]):Promise<any>{
 if(family==='firefox')return Promise.resolve(target[name](...args));
 const api=extensionAPI(family);return new Promise((resolve,reject)=>{target[name](...args,(value:unknown)=>{const error=api.runtime.lastError;if(error)reject(Error(error.message));else resolve(value);});});
}
export function store(family:Family,area:any){return{async get(key:string){return(await call(family,area,'get',key))[key];},async set(key:string,value:unknown){await call(family,area,'set',{[key]:value});},async remove(key:string){await call(family,area,'remove',key);}};}
