/** Browser-only entropy port; no game rules or stored session history. */
export function seed():number{return crypto.getRandomValues(new Uint32Array(1))[0];}

/** Real completion metadata is assigned once at the browser boundary. */
export function newID():string{
 const bytes=crypto.getRandomValues(new Uint8Array(16));bytes[6]=(bytes[6]&15)|64;bytes[8]=(bytes[8]&63)|128;
 const hex=Array.from(bytes,b=>b.toString(16).padStart(2,'0')).join('');return [hex.slice(0,8),hex.slice(8,12),hex.slice(12,16),hex.slice(16,20),hex.slice(20)].join('-');
}
export const resultHost={id:newID,timestamp:()=>new Date().toISOString()};
