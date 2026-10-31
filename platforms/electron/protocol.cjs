'use strict';
/** Fixed-root mapping validates the raw path before URL dot-segment normalization. */
const path=require('node:path'),fs=require('node:fs');
const DEFAULT_URL='app://tetris/index.html';
function collectAssets(root,prefix=''){
 const result=new Set();for(const entry of fs.readdirSync(path.join(root,prefix),{withFileTypes:true})){const name=prefix+entry.name;if(entry.isDirectory())for(const child of collectAssets(root,name+'/'))result.add(child);else if(entry.isFile())result.add(name);}return result;
}
function parsedLocal(value){
 if(typeof value!=='string'||!/^app:\/\/tetris(?=\/|[?#]|$)/i.test(value))return null;
 try{
  const url=new URL(value);if(url.protocol!=='app:'||url.hostname.toLowerCase()!=='tetris'||url.port||url.username||url.password)return null;
  const raw=/^app:\/\/[^/?#]+([^?#]*)/i.exec(value)?.[1]??'',decoded=decodeURIComponent(raw||'/');
  if(/[\\\0%]/.test(decoded)||decoded.split('/').some(segment=>segment==='.'||segment==='..'))return null;
  return{url,decoded};
 }catch{return null;}
}
function mapRequest(value,method,root,allowed){
 if(!['GET','HEAD'].includes(method))return{status:405};const parsed=parsedLocal(value);if(!parsed)return{status:404};
 const name=parsed.decoded==='/'?'index.html':parsed.decoded.slice(1);if(!allowed.has(name))return{status:404};
 const file=path.resolve(root,name),base=path.resolve(root)+path.sep;if(!file.startsWith(base))return{status:404};
 const types={'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.css':'text/css; charset=utf-8','.wasm':'application/wasm','.json':'application/json','.png':'image/png','.svg':'image/svg+xml'};
 return{status:200,file,type:types[path.extname(name)]??'application/octet-stream'};
}
function allowNavigation(value){const parsed=parsedLocal(value);return !!parsed&&['/','/index.html'].includes(parsed.decoded);}
function startupURL(argv){const value=argv.find(arg=>arg.startsWith('--game-url='))?.slice('--game-url='.length);return value&&allowNavigation(value)?value:DEFAULT_URL;}
module.exports={mapRequest,collectAssets,allowNavigation,startupURL,DEFAULT_URL};
