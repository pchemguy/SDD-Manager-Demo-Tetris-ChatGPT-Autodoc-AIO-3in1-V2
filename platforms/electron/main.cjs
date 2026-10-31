'use strict';
const path=require('node:path'),electron=require('electron'),{boot}=require('./host.cjs');
boot(electron,{rendererRoot:path.join(__dirname,'renderer'),argv:process.argv}).catch(error=>{console.error('Tetris could not start:',error.message);electron.app.quit();});
