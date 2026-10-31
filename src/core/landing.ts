/** Collision-free downward landing, shared by hard drop and read-only ghost projection. */
import {valid,type Board,type Piece} from './geometry.js';
export function landing(board:Board,piece:Piece):Piece{
 let result={...piece};while(valid(board,{...result,y:result.y+1}))result.y++;return result;
}
