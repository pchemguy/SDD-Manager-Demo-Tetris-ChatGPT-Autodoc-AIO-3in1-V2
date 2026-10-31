/** Complete format-v1 structural/schema constraints, then result semantics/ranking. */
import {validateSettings,type Settings} from './settings.js';
import {rank,validateResults,type Result} from './results.js';
export interface Snapshot{formatVersion:1;results:Result[];settings:Settings}
export function validateSnapshot(input:unknown):Snapshot{
 if(!input||typeof input!=='object'||Array.isArray(input))throw Error('Save document must be an object');
 const value=input as Record<string,unknown>,fields=['formatVersion','results','settings'];
 if(Object.keys(value).length!==3||!fields.every(k=>Object.hasOwn(value,k)))throw Error('Missing or extra save fields');
 if(value.formatVersion!==1)throw Error('Unsupported save format version');
 const results=validateResults(value.results),settings=validateSettings(value.settings,true) as Settings;
 return{formatVersion:1,results:rank(results),settings};
}
