/** All codecs and Wasm stay local; size checks precede runtime initialization. */
import initSqlJs from 'sql.js';
import type {SqlJsStatic} from 'sql.js';
import {encodeJSON,decodeJSON} from '../../codecs/json.js';
import {encodeSQLite,decodeSQLite,isSQLite} from '../../codecs/sqlite.js';
import {checkSize} from '../../codecs/limits.js';
import type {FileCodec,FileFormat} from '../../app/files.js';
import type {Snapshot} from '../../app/snapshot.js';
let engine:Promise<SqlJsStatic>|undefined;
function sqlite():Promise<SqlJsStatic>{
 if(!engine)engine=initSqlJs({locateFile:()=>new URL('./runtime/sql-wasm.wasm',document.baseURI).href}).catch(error=>{engine=undefined;throw error;});return engine;
}
export const browserCodec:FileCodec={
 async decode(bytes:Uint8Array):Promise<Snapshot>{checkSize(bytes);return isSQLite(bytes)?decodeSQLite(bytes,await sqlite()):decodeJSON(bytes);},
 async encode(snapshot:Snapshot,format:FileFormat):Promise<Uint8Array>{if(format==='json')return encodeJSON(snapshot);if(format==='sqlite')return encodeSQLite(snapshot,await sqlite());throw Error('Unsupported save format');}
};
