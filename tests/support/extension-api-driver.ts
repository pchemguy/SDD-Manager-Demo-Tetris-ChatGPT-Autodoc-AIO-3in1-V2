import {startBackground} from '../../src/platform/extensions/background.js';
import {store,type Family} from '../../src/platform/extensions/api.js';
const family=process.argv[2] as Family,calls:string[]=[];let clicked:(tab:unknown)=>void=()=>{},stored:unknown;
const promiseArea={async get(){return{settings:stored};},async set(value:any){stored=value.settings;},async remove(){stored=undefined;}};
const callbackArea={get(_key:any,callback:any){callback({settings:stored});},set(value:any,callback:any){stored=value.settings;callback();},remove(_key:any,callback:any){stored=undefined;callback();}};
function api(name:Family){return{runtime:{id:'test',onConnect:{addListener(){}},lastError:undefined},storage:{local:name==='chromium'?callbackArea:promiseArea,session:name==='chromium'?callbackArea:promiseArea},action:{onClicked:{addListener(fn:any){if(name===family)clicked=fn;}}},sidePanel:{open(options:any){if(options.windowId!==7)throw Error('Wrong launch scope');calls.push('chromium');return Promise.resolve();}},sidebarAction:{open(){calls.push('firefox');return Promise.resolve();}}};}
Object.assign(globalThis,{chrome:api('chromium'),browser:api('firefox')});startBackground(family);clicked({windowId:7});const area=store(family,family==='chromium'?callbackArea:promiseArea);await area.set('settings',{v:3});console.log(JSON.stringify({calls,stored:await area.get('settings')}));
