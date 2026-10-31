/** Deterministic subprocess bridge; excluded from production bundles. */
import {readFileSync} from 'node:fs';
import * as geometry from '../../src/core/geometry.js';
const q=JSON.parse(readFileSync(0,'utf8'));
if(q.op==='geometry')console.log(JSON.stringify({cells:geometry.cells(q.piece),valid:geometry.valid(q.board??geometry.emptyBoard(),q.piece)}));
else throw Error('Unknown operation');
