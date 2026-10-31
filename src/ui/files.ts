/** Manual controls only; content chooses format, while cancellation has no commit path. */
import type {FileExchange,FileFormat} from '../app/files.js';
import {MAX_BYTES} from '../codecs/limits.js';
export function bindFileControls(root:HTMLElement,exchange:FileExchange,download:(bytes:Uint8Array,name:string,type:string)=>void):void{
 const input=root.querySelector<HTMLInputElement>('#restore-input')!,format=root.querySelector<HTMLSelectElement>('#file-format')!;
 const notice=(message:string)=>{root.querySelector('#notice')!.textContent=message;};
 exchange.onBusy=busy=>{root.querySelectorAll<HTMLInputElement|HTMLSelectElement|HTMLButtonElement>('#settings input,#settings select,#settings button').forEach(control=>{control.disabled=busy;});root.querySelector('#settings')!.setAttribute('aria-busy',String(busy));};
 root.querySelector('#save')!.addEventListener('click',async()=>{
  const selected=format.value as FileFormat,name='tetris-save.'+(selected==='json'?'json':'sqlite');
  try{notice('Preparing download...');const bytes=await exchange.save(selected);download(bytes,name,selected==='json'?'application/json':'application/vnd.sqlite3');notice('Download offered: '+name);}
  catch(error){notice('Save failed: '+String(error));}
 });
 root.querySelector('#restore')!.addEventListener('click',()=>{if(!exchange.busy)input.click();});
 input.addEventListener('change',async()=>{
  const file=input.files?.[0];if(!file)return;
  try{if(exchange.busy)throw Error('A file operation is already in progress');if(file.size>MAX_BYTES)throw Error('Save files must be at most 2 MiB');notice('Validating restore...');await exchange.restore(async()=>new Uint8Array(await file.arrayBuffer()));notice('Restored results and all six settings. Use Start when ready.');}
  catch(error){notice('Restore failed: '+String(error));}finally{input.value='';}
 });
}
