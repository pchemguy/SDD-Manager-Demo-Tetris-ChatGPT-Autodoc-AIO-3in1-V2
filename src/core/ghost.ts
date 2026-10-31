/** Dynamic visibility uses every occupied projected cell, not its origin or box. */
import {cells,type Piece} from './geometry.js';
export function ghostVisible(piece:Piece):boolean{return cells(piece).every(([,y])=>y>=10);}
