/** Standard SRS ordered kicks in screen coordinates (+y downward); O stays stationary. */
import {valid,type Board,type Piece,type Point} from './geometry.js';
const common:Record<string,Point[]>={
 '0>1':[[0,0],[-1,0],[-1,-1],[0,2],[-1,2]],
 '1>0':[[0,0],[1,0],[1,1],[0,-2],[1,-2]],
 '1>2':[[0,0],[1,0],[1,1],[0,-2],[1,-2]],
 '2>1':[[0,0],[-1,0],[-1,-1],[0,2],[-1,2]],
 '2>3':[[0,0],[1,0],[1,-1],[0,2],[1,2]],
 '3>2':[[0,0],[-1,0],[-1,1],[0,-2],[-1,-2]],
 '3>0':[[0,0],[-1,0],[-1,1],[0,-2],[-1,-2]],
 '0>3':[[0,0],[1,0],[1,-1],[0,2],[1,2]]
};
const line:Record<string,Point[]>={
 '0>1':[[0,0],[-2,0],[1,0],[-2,1],[1,-2]],
 '1>0':[[0,0],[2,0],[-1,0],[2,-1],[-1,2]],
 '1>2':[[0,0],[-1,0],[2,0],[-1,-2],[2,1]],
 '2>1':[[0,0],[1,0],[-2,0],[1,2],[-2,-1]],
 '2>3':[[0,0],[2,0],[-1,0],[2,-1],[-1,2]],
 '3>2':[[0,0],[-2,0],[1,0],[-2,1],[1,-2]],
 '3>0':[[0,0],[1,0],[-2,0],[1,2],[-2,-1]],
 '0>3':[[0,0],[-1,0],[2,0],[-1,-2],[2,1]]
};
export function rotate(board:Board,piece:Piece,direction:1|-1,canPlace:(p:Piece)=>boolean=p=>valid(board,p)):Piece{
 if(piece.kind==='O')return piece;
 const rotation=(piece.rotation+(direction===1?1:3))%4;
 for(const[x,y]of(piece.kind==='I'?line:common)[`${piece.rotation}>${rotation}`]){
  const p={...piece,rotation,x:piece.x+x,y:piece.y+y};if(canPlace(p))return p;
 }
 return piece;
}
