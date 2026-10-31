/** Copy only pinned deployable assets; never include package directories or dev code. */
import {mkdir,copyFile} from 'node:fs/promises';
await mkdir('public/runtime',{recursive:true});await mkdir('public/schemas',{recursive:true});
await copyFile('node_modules/sql.js/dist/sql-wasm.wasm','public/runtime/sql-wasm.wasm');
await copyFile('schemas/tetris-save.schema.json','public/schemas/tetris-save.schema.json');
