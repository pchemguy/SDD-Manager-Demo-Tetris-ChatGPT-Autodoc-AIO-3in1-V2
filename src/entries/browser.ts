/** Browser composition root: shared controller/view, local clock and lifecycle. */
import {Controller} from '../app/controller.js';
import {seed} from '../platform/browser/host.js';
import {mount} from '../ui/view.js';
import {bindInput} from '../ui/input.js';
import '../ui/styles.css';
const app=new Controller(seed);mount(document.querySelector<HTMLElement>('#app')!,app);const input=bindInput(app);
let previous=performance.now();function frame(now:number){const delta=now-previous;previous=now;app.tick(delta);input.repeat(now);requestAnimationFrame(frame);}requestAnimationFrame(frame);
