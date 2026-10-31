/** Seeded Fisher-Yates bags; input queues are never mutated and preview stays available. */
import {kinds,type Kind} from './geometry.js';
function shuffle(seed:number):{bag:Kind[];seed:number}{
 const bag=[...kinds];let n=seed||1;
 for(let i=bag.length-1;i>0;i--){n^=n<<13;n^=n>>>17;n^=n<<5;n>>>=0;const j=Math.floor(n/4294967296*(i+1));[bag[i],bag[j]]=[bag[j],bag[i]];}
 return{bag,seed:n};
}
export function next(seed:number,queue:Kind[]):{kind:Kind;queue:Kind[];seed:number}{
 let rest=[...queue];if(!rest.length){const r=shuffle(seed);rest=r.bag;seed=r.seed;}
 const kind=rest.shift()!;if(!rest.length){const r=shuffle(seed);rest=r.bag;seed=r.seed;}
 return{kind,queue:rest,seed};
}
