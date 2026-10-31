/** Isolated ordinary SQLite files; fixed queries only, never execute imported schema SQL. */
import type {Database,SqlJsStatic,SqlValue} from 'sql.js';
import {validateSnapshot,type Snapshot} from '../app/snapshot.js';
import {keys} from '../app/settings.js';
import {checkSize} from './limits.js';
export type SQLiteEngine=Pick<SqlJsStatic,'Database'>;
export const sqliteHeader=new TextEncoder().encode('SQLite format 3\0');
export function isSQLite(bytes:Uint8Array):boolean{return bytes.length>=16&&sqliteHeader.every((v,i)=>bytes[i]===v);}
const schemaSQL=`CREATE TABLE high_scores(id TEXT PRIMARY KEY NOT NULL,score INTEGER NOT NULL CHECK(score >= 0 AND score <= 9007199254740991),timestamp TEXT NOT NULL);
CREATE TABLE settings(key TEXT PRIMARY KEY NOT NULL,value TEXT NOT NULL);`;
function rows(db:Database,sql:string):SqlValue[][]{return db.exec(sql)[0]?.values??[];}
/** Tokenize only to recognize a constrained numeric bounds CHECK; literals/comments cannot spoof it. */
function hasScoreBounds(sql:string):boolean{
 const tokens:{text:string;word:boolean}[]=[];
 for(let i=0;i<sql.length;){
  const c=sql[i];if(/\s/.test(c)){i++;continue;}
  if(sql.slice(i,i+2)==='--'){const end=sql.indexOf('\n',i+2);i=end<0?sql.length:end+1;continue;}
  if(sql.slice(i,i+2)==='/*'){const end=sql.indexOf('*/',i+2);if(end<0)return false;i=end+2;continue;}
  if(c==='\''||c==='"'||c==='`'||c==='['){const end=c==='['?']':c;let text='';i++;while(i<sql.length){if(sql[i]===end){if(sql[i+1]===end&&c!=='['){text+=end;i+=2;continue;}i++;break;}text+=sql[i++];}tokens.push({text:c==='\''?'#literal':text.toLowerCase(),word:false});continue;}
  const match=/^[a-zA-Z_][a-zA-Z_0-9]*|^[0-9]+|^(?:>=|<=|!=|<>|==)/.exec(sql.slice(i));
  const text=match?.[0]??c;tokens.push({text:text.toLowerCase(),word:/^[a-zA-Z_]/.test(text)});i+=text.length;
 }
 for(let i=0;i<tokens.length;i++)if(tokens[i].word&&tokens[i].text==='check'&&tokens[i+1]?.text==='('){
  let depth=1,j=i+2;for(;j<tokens.length;j++){if(tokens[j].text==='(')depth++;if(tokens[j].text===')'&&!--depth)break;}
  if(!depth&&boundsExpression(tokens.slice(i+2,j).map(t=>t.text)))return true;
 }
 return false;
}
type Expr={kind:'score'}|{kind:'number';value:string}|{kind:'compare'|'and';op:string;left:Expr;right:Expr};
function boundsExpression(tokens:string[]):boolean{
 let at=0;
 const primary=():Expr=>{const token=tokens[at++];if(token==='('){const value=conjunction();if(tokens[at++]!==')')throw Error('group');return value;}if(token==='score')return{kind:'score'};if(token&&/^[0-9]+$/.test(token))return{kind:'number',value:token};throw Error('operand');};
 const comparison=():Expr=>{const left=primary(),op=tokens[at];if(op==='>='||op==='<='){at++;return{kind:'compare',op,left,right:primary()};}return left;};
 const conjunction=():Expr=>{let left=comparison();while(tokens[at]==='and'){at++;left={kind:'and',op:'and',left,right:comparison()};}return left;};
 const predicates=(value:Expr):string[]=>{
  if(value.kind==='and')return [...predicates(value.left),...predicates(value.right)];
  if(value.kind!=='compare')throw Error('predicate');
  const {left,right,op}=value;
  if(left.kind==='score'&&right.kind==='number'){
   if(op==='>='&&right.value==='0')return ['lower'];if(op==='<='&&right.value==='9007199254740991')return ['upper'];
  }
  if(right.kind==='score'&&left.kind==='number'){
   if(op==='<='&&left.value==='0')return ['lower'];if(op==='>='&&left.value==='9007199254740991')return ['upper'];
  }
  throw Error('bounds');
 };
 try{const expr=conjunction();if(at!==tokens.length)return false;return new Set(predicates(expr)).size===2;}catch{return false;}
}

function columns(db:Database,table:'high_scores'|'settings',expected:[string,string,number][]):void{
 const actual=rows(db,`PRAGMA table_xinfo(${table})`);
 if(actual.length!==expected.length||actual.some((r,i)=>r[0]!==i||r[1]!==expected[i][0]||String(r[2]).toUpperCase()!==expected[i][1]||r[3]!==1||r[5]!==expected[i][2]||r[6]!==0))throw Error('Invalid SQLite table columns: '+table);
}
export function encodeSQLite(input:unknown,SQL:SQLiteEngine):Uint8Array{
 const snapshot=validateSnapshot(input),db=new SQL.Database();
 try{
  db.run('BEGIN; PRAGMA user_version=1; PRAGMA application_id=1413829714;'+schemaSQL);
  for(const r of snapshot.results)db.run('INSERT INTO high_scores(id,score,timestamp) VALUES(?,?,?)',[r.id,r.score,r.timestamp]);
  for(const key of keys)db.run('INSERT INTO settings(key,value) VALUES(?,?)',[key,snapshot.settings[key]]);
  db.run('COMMIT');const bytes=db.export();checkSize(bytes);return bytes;
 }finally{db.close();}
}
export function decodeSQLite(bytes:Uint8Array,SQL:SQLiteEngine):Snapshot{
 checkSize(bytes);if(!isSQLite(bytes))throw Error('Corrupt SQLite header');let db:Database|undefined;
 try{
  db=new SQL.Database(bytes);db.run('PRAGMA trusted_schema=OFF; PRAGMA query_only=ON');
  if(rows(db,'PRAGMA user_version')[0]?.[0]!==1||rows(db,'PRAGMA application_id')[0]?.[0]!==1413829714)throw Error('Unsupported SQLite format metadata/version');
  const objects=rows(db,"SELECT type,name,sql FROM sqlite_master WHERE name NOT LIKE 'sqlite_%'");
  if(objects.some(r=>r[0]==='view'||r[0]==='trigger'))throw Error('Invalid SQLite view/trigger');
  const tables=objects.filter(r=>r[0]==='table');
  if(tables.length!==2||!['high_scores','settings'].every(name=>tables.some(r=>r[1]===name))||tables.some(r=>/^\s*CREATE\s+VIRTUAL\b/i.test(String(r[2]))))throw Error('Invalid SQLite user tables');
  const tableList=rows(db,'PRAGMA table_list');if(!['high_scores','settings'].every(name=>tableList.some(r=>r[0]==='main'&&r[1]===name&&r[2]==='table')))throw Error('SQLite tables must be ordinary');
  columns(db,'high_scores',[['id','TEXT',1],['score','INTEGER',0],['timestamp','TEXT',0]]);columns(db,'settings',[['key','TEXT',1],['value','TEXT',0]]);
  if(!hasScoreBounds(String(tables.find(r=>r[1]==='high_scores')![2])))throw Error('Missing SQLite score bounds CHECK');
  const integrity=rows(db,'PRAGMA integrity_check');if(integrity.length!==1||integrity[0][0]!=='ok')throw Error('Corrupt SQLite integrity');
  const scores=rows(db,'SELECT id,score,timestamp,typeof(id),typeof(score),typeof(timestamp) FROM high_scores LIMIT 11');
  if(scores.some(r=>r[3]!=='text'||r[4]!=='integer'||r[5]!=='text'))throw Error('Invalid SQLite score storage classes');
  const saved=rows(db,'SELECT key,value,typeof(key),typeof(value) FROM settings LIMIT 7');
  if(saved.length!==6||saved.some(r=>r[2]!=='text'||r[3]!=='text')||new Set(saved.map(r=>r[0])).size!==6)throw Error('Invalid SQLite setting rows/storage classes');
  return validateSnapshot({formatVersion:1,results:scores.map(r=>({id:r[0],score:r[1],timestamp:r[2]})),settings:Object.fromEntries(saved.map(r=>[String(r[0]),r[1]]))});
 }catch(error){throw Error('SQLite restore failed: '+String(error));}finally{db?.close();}
}
