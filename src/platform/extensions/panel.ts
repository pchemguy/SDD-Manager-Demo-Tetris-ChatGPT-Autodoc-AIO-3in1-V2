/** Launch composition; lifecycle and file adapters are added by the next integration task. */
import {extensionAPI,type Family} from './api.js';
import {Controller} from '../../app/controller.js';
import {seed,resultHost} from '../browser/host.js';
import {mount} from '../../ui/view.js';
import {bindInput} from '../../ui/input.js';
import '../../ui/styles.css';
export async function startPanel(family:Family):Promise<void>{
 const port=extensionAPI(family).runtime.connect({name:'tetris-panel'});
 const hello:any=await new Promise((resolve,reject)=>{port.onMessage.addListener((m:any)=>{if(m.request===1){if(m.error)reject(Error(m.error));else resolve(m.value);}});port.postMessage({request:1,type:'hello'});});
 const app=new Controller(seed,()=>performance.now(),resultHost);app.updateSettings(hello.view.settings);mount(document.querySelector<HTMLElement>('#app')!,app);bindInput(app);
 function frame(){app.tick();requestAnimationFrame(frame);}requestAnimationFrame(frame);
}
