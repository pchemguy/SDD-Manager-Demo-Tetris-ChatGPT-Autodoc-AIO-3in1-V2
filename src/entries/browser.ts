/** Browser composition root: shared controller/view, local clock and lifecycle. */
import {FileExchange} from '../app/files.js';
import {browserCodec} from '../platform/browser/codec.js';
import {downloadFile} from '../platform/browser/files.js';
import {bindFileControls} from '../ui/files.js';
import {BrowserSettings} from '../platform/browser/settings.js';
import {Controller} from '../app/controller.js';
import {seed,resultHost} from '../platform/browser/host.js';
import {mount} from '../ui/view.js';
import {bindInput} from '../ui/input.js';
import '../ui/styles.css';
const app=new Controller(seed,()=>performance.now(),resultHost),persistence=new BrowserSettings();
let diagnostic='';
try{const resolved=persistence.resolve();app.updateSettings(resolved.settings);if(resolved.invalid.length)diagnostic='Invalid configuration: '+resolved.invalid.join(', ');try{persistence.initialize();}catch(e){diagnostic+=(diagnostic?'. ':'')+String(e);}}catch(e){diagnostic='Settings could not be read: '+String(e);}
mount(document.querySelector<HTMLElement>('#app')!,app);
const notice=(message:string)=>{document.querySelector('#notice')!.textContent=message;};
bindFileControls(document.querySelector<HTMLElement>('#app')!,new FileExchange(app,persistence,browserCodec),downloadFile);
notice(diagnostic);app.onSettingsChange=patch=>{try{persistence.save(patch);notice('');}catch(e){notice(String(e));}};bindInput(app);
function frame(){app.tick();requestAnimationFrame(frame);}requestAnimationFrame(frame);
