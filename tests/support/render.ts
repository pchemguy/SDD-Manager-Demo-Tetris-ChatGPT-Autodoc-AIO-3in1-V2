/** Test-only view boundary: real renderer with detached domain fixtures, never shipped. */
import {defaults} from '../../src/app/settings.js';
import {create,type GameState} from '../../src/core/game.js';
import {mount} from '../../src/ui/view.js';
import type {Controller} from '../../src/app/controller.js';
import '../../src/ui/styles.css';
(window as unknown as {renderFixture:(input:Partial<GameState>)=>void}).renderFixture=(input)=>{
 const state={...create(1),...input};
 const controller={get results(){return [];},get settings(){return {...defaults,ghost:'dynamic'};},updateSettings(){},get state(){return structuredClone(state);},subscribe(fn:(s:GameState)=>void){fn(structuredClone(state));return()=>{};},dispatch(){}} as unknown as Controller;
 mount(document.querySelector<HTMLElement>('#app')!,controller);
};
