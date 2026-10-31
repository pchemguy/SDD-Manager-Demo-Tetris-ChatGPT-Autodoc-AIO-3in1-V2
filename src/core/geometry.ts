/** Tetromino coordinates and settled-board collision boundary (screen y increases down). */
export type Kind='I'|'O'|'T'|'S'|'Z'|'J'|'L';
export type Point=[number,number];
export type Board=(Kind|'P'|null)[][];
export type Piece={kind:Kind;rotation:number;x:number;y:number};
export const kinds:Kind[]=['I','O','T','S','Z','J','L'];
const shapes:Record<Kind,Point[]>={I:[[0,1],[1,1],[2,1],[3,1]],O:[[1,0],[2,0],[1,1],[2,1]],T:[[1,0],[0,1],[1,1],[2,1]],S:[[1,0],[2,0],[0,1],[1,1]],Z:[[0,0],[1,0],[1,1],[2,1]],J:[[0,0],[0,1],[1,1],[2,1]],L:[[2,0],[0,1],[1,1],[2,1]]};
export function emptyBoard():Board{return Array.from({length:20},()=>Array<Kind|null>(10).fill(null));}
export function cells(p:Piece):Point[]{
 const pivot=p.kind==='I'?1.5:1;
 return shapes[p.kind].map(([sx,sy])=>{
  let x=sx,y=sy;
  if(p.kind!=='O')for(let i=0;i<((p.rotation%4)+4)%4;i++)[x,y]=[pivot-(y-pivot),pivot+(x-pivot)];
  return [x+p.x,y+p.y];
 });
}
export function valid(b:Board,p:Piece):boolean{
 return cells(p).every(([x,y])=>x>=0&&x<10&&y>=-2&&y<20&&(y<0||b[y][x]===null));
}
