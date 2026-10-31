/** Policy test bridge; never bundled into desktop resources. */
const fs=require('node:fs'),path=require('node:path'),os=require('node:os'),{fileURLToPath}=require('node:url');
const {mapRequest,startupURL}=require('../../platforms/electron/protocol.cjs');
const {boot}=require('../../platforms/electron/host.cjs');
const q=JSON.parse(fs.readFileSync(0,'utf8'));
(async()=>{
 if(q.op==='map'){console.log(JSON.stringify(mapRequest(q.url,q.method??'GET',path.resolve('build/protocol-fixture'),new Set(['index.html','assets/main.js','runtime/sql-wasm.wasm']))));return;}
 if(q.op==='startup'){console.log(JSON.stringify(startupURL(q.args)));return;}
 const root=fs.mkdtempSync(path.join(os.tmpdir(),'tetris-electron-'));fs.mkdirSync(path.join(root,'runtime'));fs.writeFileSync(path.join(root,'index.html'),'game');fs.writeFileSync(path.join(root,'runtime/sql-wasm.wasm'),Buffer.from([0,97,115,109,1,0,0,0]));
 const calls=[],appEvents={},sessionEvents={},webEvents={};let handler,windowOptions,url,openHandler,downloadOptions,quit=0,flush=0,permission;
 const ses={protocol:{handle(s,fn){calls.push('handler:'+s);handler=fn;}},setPermissionRequestHandler(fn){permission=fn;},setPermissionCheckHandler(){},cookies:{async flushStore(){flush++;}},on(name,fn){sessionEvents[name]=fn;}};
 class Window{constructor(options){windowOptions=options;this.webContents={on(name,fn){webEvents[name]=fn;},setWindowOpenHandler(fn){openHandler=fn;}};}setMenuBarVisibility(){}async loadURL(value){url=value;}on(){}}
 const electron={protocol:{registerSchemesAsPrivileged(value){calls.push('schemes');calls.push(value);}},app:{setName(){},setAppUserModelId(){},async whenReady(){calls.push('ready');},on(name,fn){appEvents[name]=fn;},getPath(){return root;},quit(){quit++;}},session:{fromPartition(value){calls.push(value);return ses;}},BrowserWindow:Window,net:{async fetch(value){return new Response(fs.readFileSync(fileURLToPath(value)));}}};
 try{
  await boot(electron,{rendererRoot:root,argv:q.args??[]});const response=await handler(new Request('app://tetris/index.html?ghost=hide#stay')),wasm=await handler(new Request('app://tetris/runtime/sql-wasm.wasm')),head=await handler(new Request('app://tetris/index.html',{method:'HEAD'}));
  let remotePrevented=false,localPrevented=false;webEvents['will-navigate']({preventDefault(){remotePrevented=true;}},'https://example.invalid/');webEvents['will-navigate']({preventDefault(){localPrevented=true;}},'app://tetris/index.html?ghost=hide#stay');
  let permissionAllowed=true;permission(null,'notifications',value=>{permissionAllowed=value;});
  let badDownloadPrevented=false;sessionEvents['will-download']({preventDefault(){badDownloadPrevented=true;}},{getFilename(){return 'bad.exe';}});
  sessionEvents['will-download']({preventDefault(){throw Error('Valid download blocked');}},{getFilename(){return 'tetris-save.sqlite';},setSaveDialogOptions(value){downloadOptions=value;}});
  if(appEvents['before-quit']){appEvents['before-quit']({preventDefault(){}});await new Promise(resolve=>setImmediate(resolve));}
  console.log(JSON.stringify({calls,windowOptions,url,response:{status:response.status,body:await response.text(),csp:response.headers.get('content-security-policy')},wasm:{status:wasm.status,type:wasm.headers.get('content-type')},head:await head.text(),remotePrevented,localPrevented,open:openHandler({url:'https://example.invalid/'}),permissionAllowed,badDownloadPrevented,downloadOptions,quit,flush}));
 }finally{fs.rmSync(root,{recursive:true,force:true});}
})().catch(error=>{console.error(error);process.exitCode=1;});
