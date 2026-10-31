/** Dynamic visibility uses every occupied projected cell, not its origin or box. */
import {cells,type Piece} from './geometry.js';
export function ghostVisible(piece:Piece,mode:'hide'|'dynamic'|'show'='dynamic'):boolean{return mode==='show'||mode==='dynamic'&&cells(piece).every(([,y])=>y>=10);}
