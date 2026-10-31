/** Opt-in real Electron bridge, invoked only by pytest in an isolated local profile. */
const {_electron}=require('playwright'),fs=require('node:fs'),assert=require('node:assert/strict');
const q=JSON.parse(fs.readFileSync(0,'utf8'));let app;
(async()=>{
 try{
  app=await _electron.launch({executablePath:q.binary,args:['--no-sandbox','--ozone-platform=headless','--disable-gpu',q.entry,'--game-url=https://tetris.invalid/index.html?ghost=show&keep=1#native'],env:{...process.env,TETRIS_TEST_PROFILE:q.profile},timeout:15000});
  const page=await app.firstWindow({timeout:15000});page.setDefaultTimeout(7000);await page.waitForSelector('#board');
  const origin=await page.evaluate(()=>location.origin),secure=await page.evaluate(()=>isSecureContext),noNode=await page.evaluate(()=>typeof require==='undefined'&&typeof process==='undefined');
  assert.equal(origin,'https://tetris.invalid');assert(secure&&noNode);assert((await page.evaluate(()=>document.cookie)).includes('tetris_ghost=show'),await page.locator('#notice').innerText());assert((await page.locator('.edition').innerText()).includes(q.version));
  await page.locator('#setting-ghost').selectOption('dynamic');assert((await page.evaluate(()=>document.cookie)).includes('tetris_ghost=dynamic'));await page.reload();assert.equal(await page.locator('#setting-ghost').inputValue(),'dynamic');
  await page.locator('#start').click();await page.keyboard.press('Enter');assert(Number(await page.locator('#score').innerText())>0);
  await app.evaluate(({BrowserWindow})=>BrowserWindow.getAllWindows()[0].hide());await page.waitForFunction(()=>document.querySelector('#state').textContent==='Paused');
  await app.evaluate(({BrowserWindow})=>BrowserWindow.getAllWindows()[0].show());assert.equal(await page.locator('#state').innerText(),'Paused');
  await app.evaluate(({session},folder)=>session.fromPartition('persist:tetris').on('will-download',(_event,item)=>item.setSavePath(folder+'/'+item.getFilename())),q.downloads);
  await page.locator('#file-format').selectOption('sqlite');await page.locator('#save').click();const file=q.downloads+'/tetris-save.sqlite',deadline=Date.now()+10000;
  while((!fs.existsSync(file)||fs.statSync(file).size<100)&&Date.now()<deadline)await new Promise(resolve=>setTimeout(resolve,50));assert(fs.readFileSync(file).subarray(0,16).equals(Buffer.from('SQLite format 3\0')));
  await page.locator('#restore-input').setInputFiles(file);await page.waitForFunction(()=>document.querySelector('#notice').textContent.includes('Restored'));
  assert((await page.url()).endsWith('#native'));const popupDenied=await page.evaluate(()=>window.open('https://example.invalid/')===null);assert(popupDenied);
  const prefs=await app.evaluate(({BrowserWindow})=>BrowserWindow.getAllWindows()[0].webContents.getLastWebPreferences());assert(prefs.contextIsolation&&!prefs.nodeIntegration&&prefs.sandbox);
  await page.locator('#setting-hardDropLock').selectOption('immediate');await page.locator('#start').click();for(let i=0;i<35;i++)await page.keyboard.press('Enter');assert.equal(await page.locator('#state').innerText(),'Game over');assert.equal(await page.locator('#leaderboard-body tr').count(),1);
  await app.close();app=undefined;
  app=await _electron.launch({executablePath:q.binary,args:['--no-sandbox','--ozone-platform=headless','--disable-gpu',q.entry,'--game-url=https://tetris.invalid/index.html?keep=2#reopen'],env:{...process.env,TETRIS_TEST_PROFILE:q.profile},timeout:15000});
  const reopened=await app.firstWindow({timeout:15000});reopened.setDefaultTimeout(7000);await reopened.waitForSelector('#board');assert.equal(await reopened.locator('#setting-ghost').inputValue(),'dynamic');assert.equal(await reopened.locator('#setting-hardDropLock').inputValue(),'immediate');assert.equal(await reopened.locator('#leaderboard-body tr').count(),0);assert.equal(await reopened.locator('#state').innerText(),'Ready');
  console.log(JSON.stringify({origin,secure,noNode,popupDenied,sqlite:file,reopenedSettings:true,sessionResultsCleared:true,prefs:{sandbox:prefs.sandbox,contextIsolation:prefs.contextIsolation,nodeIntegration:prefs.nodeIntegration}}));
 }finally{if(app)await app.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});
