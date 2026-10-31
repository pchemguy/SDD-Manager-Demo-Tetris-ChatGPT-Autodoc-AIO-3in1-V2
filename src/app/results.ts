/** Completed-result contract and immutable deterministic top-ten ranking. */
export interface Result{id:string;score:number;timestamp:string}
export interface ResultHost{id:()=>string;timestamp:()=>string}
export function validTimestamp(value:unknown):value is string{
 if(typeof value!=='string'||!/^(?!0000)[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9]{3}Z$/.test(value))return false;
 try{return new Date(value).toISOString()===value;}catch{return false;}
}
export function validateResult(input:unknown):Result{
 if(!input||typeof input!=='object'||Array.isArray(input))throw Error('Invalid result object');
 const r=input as Result;
 if(Object.keys(r).length!==3||!['id','score','timestamp'].every(k=>Object.hasOwn(r,k)))throw Error('Missing or extra result fields');
 if(typeof r.id!=='string'||!/^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/.test(r.id))throw Error('Invalid result ID');
 if(!Number.isSafeInteger(r.score)||r.score<0)throw Error('Invalid result score');
 if(!validTimestamp(r.timestamp))throw Error('Invalid result timestamp');
 return {...r};
}
export function validateResults(input:unknown,limit=10):Result[]{
 if(!Array.isArray(input)||input.length>limit)throw Error('Invalid result count');
 const rows=input.map(validateResult);if(new Set(rows.map(r=>r.id)).size!==rows.length)throw Error('Duplicate result ID');return rows;
}
export function rank(input:unknown):Result[]{return validateResults(input,Infinity).sort((a,b)=>b.score-a.score||(a.timestamp<b.timestamp?-1:a.timestamp>b.timestamp?1:0)||(a.id<b.id?-1:a.id>b.id?1:0)).slice(0,10);}
