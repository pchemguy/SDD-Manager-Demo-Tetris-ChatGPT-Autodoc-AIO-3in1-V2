/** Normal contiguous descent or penetrator deepest collision-free visible landing. */
import {valid,cells,type Board,type Piece} from './geometry.js';
export function deepest(board:Board,piece:Piece):Piece|null{
 if(cells(piece).some(([x,y])=>x<0||x>=10||y< -2||y>=20))return null;
 let result:Piece|null=null;
 for(let y=piece.y;y<20;y++){const candidate={...piece,y};if(valid(board,candidate)&&cells(candidate).every(([,row])=>row>=0))result=candidate;}
 return result;
}
export function landing(board:Board,piece:Piece,penetrator=false):Piece{
 if(penetrator){const result=deepest(board,piece);if(!result)throw Error('No valid penetrator landing');return result;}
 let result={...piece};while(valid(board,{...result,y:result.y+1}))result.y++;return result;
}
