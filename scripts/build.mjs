/** Cumulative renderer builds keep host entry points separate and runtime assets local. */
import './prepare-assets.mjs';
import {spawnSync} from 'node:child_process';
import {mkdir,copyFile,readFile,writeFile} from 'node:fs/promises';
function vite(args){const result=spawnSync(process.execPath,['node_modules/vite/bin/vite.js','build',...args],{stdio:'inherit'});if(result.status!==0)process.exit(result.status??1);}
vite(['--outDir','dist/browser','--base','./']);vite(['--config','platforms/electron/vite.config.ts']);
await mkdir('dist/desktop',{recursive:true});
for(const name of ['main.cjs','host.cjs','protocol.cjs'])await copyFile('platforms/electron/'+name,'dist/desktop/'+name);
const meta=JSON.parse(await readFile('package.json','utf8'));
await writeFile('dist/desktop/package.json',JSON.stringify({name:'tetris',productName:'Tetris',version:meta.version,main:'main.cjs',type:'commonjs',private:true},null,2)+'\n');
await import('./build-extensions.mjs');
