/** Serialized manual file exchange: isolated decode, full validation, host commit, app commit. */
import type {Controller} from './controller.js';
import {validateSnapshot,type Snapshot} from './snapshot.js';
import type {Settings} from './settings.js';
export type FileFormat='json'|'sqlite';
export interface FileCodec{decode(bytes:Uint8Array):Promise<Snapshot>;encode(snapshot:Snapshot,format:FileFormat):Promise<Uint8Array>}
export interface SettingsCommit{commit(settings:Settings,snapshot?:Snapshot):void|Promise<void>}
export class FileExchange{
 private active=false;
 onBusy:(busy:boolean)=>void=()=>{};
 get busy():boolean{return this.active;}
 constructor(private app:Controller,private persistence:SettingsCommit,private codec:FileCodec){}
 private async run<T>(operation:()=>Promise<T>):Promise<T>{
  if(this.active)throw Error('A file operation is already in progress');this.active=true;this.app.settingsLocked=true;
  try{this.onBusy(true);return await operation();}finally{this.active=false;this.app.settingsLocked=false;this.onBusy(false);}
 }
 async save(format:FileFormat):Promise<Uint8Array>{return this.run(async()=>{const captured=this.app.snapshot();return this.codec.encode(captured,format);});}
 async restore(source:Uint8Array|(()=>Promise<Uint8Array>)):Promise<void>{return this.run(async()=>{const bytes=typeof source==='function'?await source():source,candidate=validateSnapshot(await this.codec.decode(bytes));await this.persistence.commit(candidate.settings,candidate);this.app.replaceSnapshot(candidate);});}
}
