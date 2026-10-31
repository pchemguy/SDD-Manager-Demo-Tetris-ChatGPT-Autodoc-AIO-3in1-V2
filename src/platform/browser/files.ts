/** Standard download port shared by browser, secure desktop renderer and extension pages. */
export function downloadFile(bytes:Uint8Array,name:string,type:string):void{
 const url=URL.createObjectURL(new Blob([Uint8Array.from(bytes).buffer],{type})),link=document.createElement('a');let clicked=false;
 try{link.href=url;link.download=name;link.hidden=true;document.body.append(link);link.click();clicked=true;}
 finally{link.remove();if(clicked)setTimeout(()=>URL.revokeObjectURL(url),1000);else URL.revokeObjectURL(url);}
}
