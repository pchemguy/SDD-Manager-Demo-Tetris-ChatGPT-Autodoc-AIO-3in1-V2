/** Browser composition root: shared controller/view, local clock and lifecycle. */
import {Controller} from '../app/controller.js';
import {seed} from '../platform/browser/host.js';
import {mount} from '../ui/view.js';
import {bindInput} from '../ui/input.js';
import '../ui/styles.css';
const app=new Controller(seed,()=>performance.now());mount(document.querySelector<HTMLElement>('#app')!,app);bindInput(app);
function frame(){app.tick();requestAnimationFrame(frame);}requestAnimationFrame(frame);
