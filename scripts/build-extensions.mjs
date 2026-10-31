/** Two local-asset bundles, with classic IIFE backgrounds for both host APIs. */
import {build} from 'esbuild';
import {mkdir,cp,copyFile,readFile,writeFile,rm} from 'node:fs/promises';
for(const family of ['chromium','firefox']){
 const out='dist/'+family;await rm(out,{recursive:true,force:true});await mkdir(out,{recursive:true});
 for(const entry of ['background','panel'])await build({entryPoints:[`src/entries/${family}-${entry}.ts`],outfile:`${out}/${entry}.js`,bundle:true,minify:true,platform:'browser',target:family==='chromium'?'chrome116':'firefox115',format:entry==='background'?'iife':'esm',external:['fs','path','crypto'],define:{'process.env.NODE_ENV':'"production"'}});
 await copyFile('platforms/extensions/'+family+'/manifest.json',out+'/manifest.json');
 let html=await readFile('platforms/extensions/panel.html','utf8');html=html.replace('</head>','<link rel="stylesheet" href="./panel.css"></head>');await writeFile(out+'/panel.html',html);
 for(const dir of ['runtime','schemas'])await cp('public/'+dir,out+'/'+dir,{recursive:true});
 await cp('platforms/extensions/icons',out+'/icons',{recursive:true});
}
