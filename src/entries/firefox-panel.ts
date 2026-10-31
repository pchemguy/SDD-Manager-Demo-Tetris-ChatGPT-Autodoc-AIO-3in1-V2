import {startPanel} from '../platform/extensions/panel.js';void startPanel('firefox').catch(e=>{document.querySelector('#app')!.textContent='Cannot open Tetris: '+String(e);});
