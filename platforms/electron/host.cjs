'use strict';
/** Main-process capabilities stay here; renderer has no Node, preload or filesystem IPC. */
const path=require('node:path'),{pathToFileURL}=require('node:url');
const {mapRequest,collectAssets,allowNavigation,startupURL}=require('./protocol.cjs');
const CSP="default-src 'self'; script-src 'self' 'wasm-unsafe-eval'; style-src 'self' 'unsafe-inline'; object-src 'none'; frame-src 'none'; base-uri 'self'";
async function boot(electron,{rendererRoot,argv=process.argv}){
 const {app,session,BrowserWindow,net}=electron;
 app.setName('Tetris');app.setAppUserModelId('io.github.pchemguy.tetris');await app.whenReady();
 const partition='persist:tetris',ses=session.fromPartition(partition),allowed=collectAssets(rendererRoot);
 ses.protocol.handle('https',async request=>{
  const mapped=mapRequest(request.url,request.method,rendererRoot,allowed);
  if(mapped.status!==200)return new Response('Resource unavailable',{status:mapped.status});
  try{const response=await net.fetch(pathToFileURL(mapped.file).href);if(!response.ok)return new Response('Resource unavailable',{status:404});return new Response(request.method==='HEAD'?null:response.body,{status:200,headers:{'Content-Type':mapped.type,'Content-Security-Policy':CSP,'Cache-Control':'no-cache'}});}
  catch{return new Response('Resource unavailable',{status:404});}
 });
 ses.setPermissionRequestHandler((_contents,_permission,callback)=>callback(false));ses.setPermissionCheckHandler(()=>false);
 ses.on('will-download',(event,item)=>{
  const name=item.getFilename();if(!['tetris-save.json','tetris-save.sqlite'].includes(name)){event.preventDefault();return;}
  item.setSaveDialogOptions({title:'Save Tetris results and settings',defaultPath:path.join(app.getPath('downloads'),name),filters:[{name:name.endsWith('.json')?'JSON':'SQLite',extensions:[name.endsWith('.json')?'json':'sqlite']}]});
 });
 const window=new BrowserWindow({title:'Tetris',width:1440,height:1000,minWidth:640,minHeight:720,autoHideMenuBar:true,webPreferences:{partition,sandbox:true,contextIsolation:true,nodeIntegration:false,webSecurity:true,webviewTag:false}});
 const pauseRenderer=()=>{if(!window.webContents.isDestroyed())window.webContents.executeJavaScript("window.dispatchEvent(new Event('blur'))").catch(()=>{});};
 for(const event of ['blur','hide','minimize'])window.on(event,pauseRenderer);
 window.setMenuBarVisibility(false);window.webContents.setWindowOpenHandler(()=>({action:'deny'}));
 const denyRemote=(event,url)=>{if(!allowNavigation(url))event.preventDefault();};
 window.webContents.on('will-navigate',denyRemote);window.webContents.on('will-redirect',denyRemote);window.webContents.on('will-attach-webview',event=>event.preventDefault());
 app.on('window-all-closed',()=>app.quit());let quitting=false;
 app.on('before-quit',event=>{if(quitting)return;event.preventDefault();quitting=true;ses.cookies.flushStore().catch(error=>console.error('Cookie flush failed:',error.message)).finally(()=>app.quit());});
 await window.loadURL(startupURL(argv));return window;
}
module.exports={boot,CSP};
