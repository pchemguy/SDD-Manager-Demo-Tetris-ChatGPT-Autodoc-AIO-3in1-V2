/** Common byte limit is enforced before decoding or allocating codec state. */
export const MAX_BYTES=2*1024*1024;
export function checkSize(bytes:Uint8Array):void{if(bytes.byteLength>MAX_BYTES)throw Error('Save files must be at most 2 MiB');}
