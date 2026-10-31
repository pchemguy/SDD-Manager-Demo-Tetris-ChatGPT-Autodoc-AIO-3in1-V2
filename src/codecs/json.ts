/** Strict UTF-8 JSON with duplicate decoded member-name detection before validation. */
import {validateSnapshot,type Snapshot} from '../app/snapshot.js';
import {checkSize} from './limits.js';
function rejectDuplicateNames(source:string):void{
 const stack:{object:boolean;names:Set<string>}[]=[];
 for(let i=0;i<source.length;i++){
  const c=source[i];if(c==='{'||c==='['){stack.push({object:c==='{',names:new Set()});continue;}if(c==='}'||c===']'){stack.pop();continue;}
  if(c!=='"')continue;const start=i++;while(i<source.length){if(source[i]==='\\'){i+=2;continue;}if(source[i]==='"')break;i++;}
  let next=i+1;while(/\s/.test(source[next]??'')&&next<source.length)next++;
  const context=stack.at(-1);if(source[next]===':'&&context?.object){const key=JSON.parse(source.slice(start,i+1)) as string;if(context.names.has(key))throw Error('Duplicate JSON member: '+key);context.names.add(key);}
 }
}
export function decodeJSON(bytes:Uint8Array):Snapshot{
 checkSize(bytes);let text:string;
 try{text=new TextDecoder('utf-8',{fatal:true,ignoreBOM:true}).decode(bytes);}catch{throw Error('Unsupported text encoding: expected UTF-8');}
 if(text.charCodeAt(0)===0xfeff)text=text.slice(1);
 let parsed:unknown;try{parsed=JSON.parse(text);}catch{throw Error('Corrupt JSON: invalid syntax');}
 rejectDuplicateNames(text);return validateSnapshot(parsed);
}
export function encodeJSON(input:unknown):Uint8Array{const snapshot=validateSnapshot(input),bytes=new TextEncoder().encode(JSON.stringify(snapshot,null,2)+'\n');checkSize(bytes);return bytes;}
