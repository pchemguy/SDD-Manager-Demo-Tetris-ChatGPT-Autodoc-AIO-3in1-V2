import {startPanel} from '../platform/extensions/panel.js';void startPanel('chromium').catch(e=>{document.querySelector('#app')!.textContent='Cannot open Tetris: '+String(e);});
