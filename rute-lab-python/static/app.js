import {names,algos,scenarios,hs,config,solve,optimum} from './engine.js';
const $=s=>document.querySelector(s);
const colors={'A*':'#087f5b',Dijkstra:'#3268ca',BFS:'#b95b19'};
const state={mode:'scenario',value:'S1',algo:'A*',metric:'cost',frame:0};
let cfg,runs,current,best,timer=null;
const label=n=>names[n]||n;
const route=p=>p?p.map(label).join(' → '):'Tidak ada rute';
const number=n=>n===null?'—':String(n).replace('.',',');
const options=()=>state.mode==='heuristic'?['A*']:state.mode==='reopen'?['A*']:algos;
function pause(){if(timer){clearInterval(timer);timer=null;}$('#play').textContent='Putar langkah';}
function calculate(){pause();cfg=config(state.mode,state.value);best=optimum(cfg);runs=Object.fromEntries(options().map(a=>[a,solve(cfg,a)]));current=runs[state.algo];state.frame=current.frames.length-1;}
function selectMode(mode,value){state.mode=mode;state.value=value??({scenario:'S1',heuristic:'H3',weight:'3',reopen:'R1'}[mode]);state.algo='A*';calculate();render(true);}
function configureControls(){
 document.querySelectorAll('[data-mode]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.mode===state.mode)));
 let html='';
 if(state.mode==='scenario')html=`<div class="control-row"><label for="scenario">Skenario</label><select id="scenario">${scenarios.map(([id,t])=>`<option value="${id}" ${id===state.value?'selected':''}>${id} · ${t}</option>`).join('')}</select></div>`;
 if(state.mode==='heuristic')html=`<div class="control-row"><label for="heuristic">Heuristik</label><select id="heuristic">${hs.map(h=>`<option value="${h.id}" ${h.id===state.value?'selected':''}>${h.id} · ${h.name}</option>`).join('')}</select></div>`;
 if(state.mode==='weight')html=`<div class="control-row"><label for="weight">Jarak P–K</label><input id="weight" type="range" min="2" max="10" step="1" value="${state.value}" aria-valuetext="${state.value} kilometer"><output id="weight-value" class="weight-value" for="weight">${state.value} km</output></div>`;
 if(state.mode==='reopen')html='<div class="reopen-explain">Graf tambahan · S, A, B, G</div>';
 $('#controls').innerHTML=html;
 $('#scenario')?.addEventListener('change',e=>changeValue(e.target.value));
 $('#heuristic')?.addEventListener('change',e=>changeValue(e.target.value));
 $('#weight')?.addEventListener('input',e=>{e.target.setAttribute('aria-valuetext',`${e.target.value} kilometer`);$('#weight-value').textContent=e.target.value+' km';changeValue(e.target.value);});
}
function changeValue(value){state.value=value;calculate();render();}
function card(algo,res){const valid=res.cost===best,missing=res.cost===null;return `<article class="result-card" style="--accent:${colors[algo]}"><div class="result-top"><span class="algo-name"><i class="algo-dot"></i>${algo}</span><span class="badge ${missing?'':valid?'ok':'warn'}">${missing?'Tidak terhubung':valid?'Jarak minimum':'Bukan minimum'}</span></div><div class="result-metrics"><span class="result-number">${number(res.cost)}<small>km</small></span><span class="exp-number"><b>${res.expanded.length}</b> ekspansi</span></div><p class="result-route">${route(res.path)}</p></article>`;}
function render(control=false){
 if(control)configureControls();
 $('#context').textContent=state.mode==='scenario'?scenarios.find(s=>s[0]===state.value)[2]:state.mode==='heuristic'?'Graf dan jalan tetap normal. Hanya perkiraan biaya menuju Kampus yang berubah. Dijkstra dan BFS tidak memakai nilai ini.':state.mode==='weight'?'Geser jarak Perpustakaan–Kampus dari 2 sampai 10 km. Jalan lain dan heuristik dasar tetap.':'Heuristik tidak melebihi biaya sisa optimum, tetapi tidak konsisten. Simpul A perlu diproses kembali setelah ditemukan jalur yang lebih murah.';
 if(options().length===3)$('#results').innerHTML=algos.map(a=>card(a,runs[a])).join('');
 else{
  const h=hs.find(h=>h.id===state.value);
  $('#results').innerHTML=card('A*',current)+`<article class="result-card" style="--accent:#6b7e93"><div class="result-top"><span class="algo-name">Acuan optimum</span><span class="badge">Enumerasi jalur</span></div><span class="result-number">${best}<small>km</small></span><p class="result-route">Selisih hasil A*: ${current.cost-best} km dari biaya minimum.</p></article><article class="result-card" style="--accent:${h&&!h.ad?'#b95b19':'#6b7e93'}"><div class="result-top"><span class="algo-name">Sifat heuristik</span></div><div style="font-weight:700;font-size:17px">${h&&!h.ad?'Melebihi biaya optimum':'Admissible'}</div><p class="result-route">${h?h.con?'Konsisten pada setiap jalan.':'Tidak konsisten pada sebagian jalan.':'Tidak konsisten · A diekspansi dua kali.'}</p></article>`;
 }
 $('#algo-switch').innerHTML=options().map(a=>`<button data-algo="${a}" aria-pressed="${a===state.algo}">${a}</button>`).join('');
 document.querySelectorAll('[data-algo]').forEach(b=>b.addEventListener('click',()=>{pause();state.algo=b.dataset.algo;current=runs[state.algo];state.frame=current.frames.length-1;render();}));
 $('.map-panel').style.setProperty('--accent',colors[state.algo]);
 $('#map-meta').innerHTML=`<b>${label(cfg.start)}</b> ke <b>${label(cfg.goal)}</b> <span aria-hidden="true">·</span> ${state.algo==='A*'?'f(n) = g(n) + h(n)':state.algo==='Dijkstra'?'Prioritas biaya g(n) · h(n) = 0':'Antrean FIFO · urutan masuk'}`;
 renderBars();renderExperiment();renderFrame();
}
function renderBars(){
 document.querySelectorAll('[data-metric]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.metric===state.metric)));
 const data=state.mode==='heuristic'?hs.map(h=>({id:h.id,res:solve(config('heuristic',h.id)),color:h.id==='H6'?colors.BFS:colors['A*']})):options().map(a=>({id:a,res:runs[a],color:colors[a]}));
 const vals=data.map(d=>state.metric==='cost'?d.res.cost:d.res.expanded.length),max=Math.max(1,...vals.filter(v=>v!==null));
 $('#bars').innerHTML=data.map((d,i)=>`<div class="bar-row ${data.length>3?'compact':''}" style="--accent:${d.color}"><div class="bar-label"><span>${d.id}${state.mode==='heuristic'&&d.id===state.value?' · dipilih':''}</span><b>${vals[i]===null?'Tidak ada rute':number(vals[i])+(state.metric==='cost'?' km':' simpul')}</b></div><div class="bar-track"><div class="bar-fill" style="width:${vals[i]===null?0:vals[i]/max*100}%"></div></div></div>`).join('');
 let title,desc;
 if(state.mode==='scenario'){
  [title,desc]=({S1:['Jarak sama, usaha berbeda.','A* dan Dijkstra menemukan 7 km. A* memeriksa 3 simpul, Dijkstra 4. BFS memilih 2 ruas dengan total 9 km.'],S2:['Jalur alternatif melalui Taman.','Ketiga algoritma memperoleh 9 km dengan 3 ekspansi. Warung diperiksa, tetapi tidak masuk rute akhir.'],S3:['Kandidat pertama belum tentu terbaik.','A* lebih dahulu menemukan Kampus dengan biaya 14, lalu memperbaikinya menjadi 9 melalui Taman.'],S4:['Tidak ada rute bukan berarti 0 km.','Semua algoritma memeriksa 4 simpul lalu kehabisan kandidat. Tanda — menunjukkan tujuan tidak dapat dicapai.'],S5:['Pencarian selesai tanpa ekspansi.','Awal sudah berada di Kampus. Jarak 0 km dan 0 ekspansi merupakan hasil yang valid.']})[state.value];
 }else if(state.mode==='heuristic'){
  [title,desc]=state.value==='H6'?['Lebih sedikit belum tentu lebih baik.','H6 hanya memeriksa 2 simpul, tetapi menghasilkan 9 km. Estimasi berlebih membuat rute optimum 7 km terlewat.']:state.value==='H5'?['Tidak konsisten, masih optimal di graf ini.','H5 menghasilkan 7 km dan 3 ekspansi. Ekspansi ulang tidak selalu terjadi; lihat contoh pada tab Ekspansi ulang.']:['Perkiraan membantu memilih kandidat.','H0–H2 memeriksa 4 simpul. H3–H4 cukup 3 simpul dengan hasil 7 km. Heuristik yang lebih tepat tidak selalu mengurangi ekspansi lagi.'];
 }else if(state.mode==='weight'){
  const w=Number(state.value);[title,desc]=w<5?['Rute melalui Perpustakaan lebih pendek.',`Biaya minimum 4 + ${w} = ${4+w} km. BFS tetap memilih jalur melalui Taman sepanjang 9 km.`]:w===5?['Dua rute, sama-sama minimum.','A* melewati Perpustakaan; Dijkstra dan BFS melewati Taman. Keduanya 9 km. Perbedaan rute tidak berarti ada hasil yang salah.']:['Rute melalui Taman menjadi pilihan.',`Jalur Perpustakaan berbiaya ${4+w} km. Ketiga algoritma memilih jalur Taman sepanjang 9 km.`];
 }else [title,desc]=['Simpul A diperiksa dua kali.','Urutan ekspansi S, A, B, A. Setelah B diperiksa, biaya A turun dari 3 menjadi 2. Hasil akhirnya S → B → A → G, biaya 4.'];
 $('#insight').innerHTML=`<b>${title}</b><p>${desc}</p>`;
}
function renderFrame(){
 const f=current.frames[state.frame],done=f.type==='goal'||f.type==='empty';
 $('#step-count').textContent=`Langkah ${state.frame} / ${current.frames.length-1}`;
 $('#progress').style.width=`${state.frame/(current.frames.length-1)*100}%`;
 $('#step').disabled=done;$('#reset').disabled=state.frame===0&&!timer;
 let title,desc;
 if(f.type==='init'){title='Siap memulai pencarian';desc=`${label(cfg.start)} masuk antrean dengan g = 0. ${state.algo==='BFS'?'Kandidat diproses sesuai urutan masuk.':`Prioritas awal ${state.algo==='A*'?cfg.h[cfg.start]:0}.`}`;}
 else if(f.type==='goal'){title=`Tujuan ditemukan · ${current.cost} km`;desc=route(current.path)+'. Tujuan langsung dikembalikan; tetangganya tidak diperiksa.';}
 else if(f.type==='empty'){title='Antrean kosong · tidak ada rute';desc=`Sebanyak ${f.expanded.length} ekspansi selesai, tetapi ${label(cfg.goal)} tidak dapat dicapai.`;}
 else if(f.type==='stale'){title=`Lewati kandidat lama: ${label(f.node)}`;desc='Biaya pada kandidat ini lebih besar dari biaya terbaik terbaru.';}
 else{title=`Ekspansi ${label(f.node)} · g = ${f.entry.g}${state.algo==='A*'?`, h = ${cfg.h[f.node]}, f = ${f.entry.f}`:''}`;desc=f.updates.length?f.updates.map(u=>`${label(u.node)}${u.old!==null?' diperbarui '+u.old+' → '+u.g:' ditambahkan, g = '+u.g}${state.algo==='A*'?', f = '+u.f:''}`).join('; ')+'.':'Tidak ada tetangga yang menghasilkan kandidat baru atau biaya lebih murah.';}
 $('#step-title').textContent=title;$('#step-description').textContent=desc;
 drawGraph(f,done);
 const queue=f.queue;
 $('#queue-label').textContent=`${queue.length} kandidat ${done?'tersisa':'menunggu'}`;
 $('#queue').innerHTML=queue.length?`<table><thead><tr><th>Simpul</th><th>g</th><th>h</th><th>${state.algo==='BFS'?'Urutan':'f'}</th><th>Status</th></tr></thead><tbody>${queue.map((q,i)=>{const n=q.path.at(-1),stale=state.algo!=='BFS'&&q.g!==f.best[n];return `<tr class="${stale?'stale-row':''}"><td>${label(n)}</td><td>${q.g}</td><td>${state.algo==='BFS'?'—':state.algo==='Dijkstra'?0:cfg.h[n]}</td><td>${state.algo==='BFS'?i+1:q.f}</td><td>${stale?'Entri lama':done?'Tidak diproses':i===0?'Berikutnya':'Menunggu'}</td></tr>`;}).join('')}</tbody></table>`:'<p class="sequence-note">Tidak ada kandidat dalam antrean.</p>';
 $('#queue-note').textContent=state.algo==='BFS'?'Urutan mengikuti FIFO. Nilai g ditampilkan sebagai jarak jalur, bukan prioritas BFS.':'g = jarak yang ditempuh; h = perkiraan sisa jarak; f = g + h. Kandidat diurutkan menurut f, lalu g, lalu nama pada jalur; tampilan ini bukan posisi fisik heap.';
 $('#sequence').innerHTML=f.expanded.length?f.expanded.map((n,i)=>`${i?'<span class="sequence-separator" aria-hidden="true">·</span>':''}<span class="node-chip ${i===f.expanded.length-1?'active':''}" title="${label(n)} · ekspansi ${i+1}">${n}</span>`).join(''):'<span class="sequence-note">Belum ada simpul diekspansi.</span>';
}
function drawGraph(f,done){
 const pos=state.mode==='reopen'?{S:[90,180],A:[320,80],B:[320,290],G:[580,180]}:{R:[85,210],W:[245,75],P:[435,75],K:[595,210],T:[340,295]};
 const edges=state.mode==='reopen'?[['S','A'],['S','B'],['B','A'],['A','G'],['B','G']]:[['R','W'],['R','T'],['W','P'],['P','K'],['T','K']];
 const chosen=done&&current.path?new Set(current.path.slice(1).map((n,i)=>[current.path[i],n].sort().join(''))):new Set();
 const awaiting=new Set(f.queue.filter(q=>q.g===f.best[q.path.at(-1)]).map(q=>q.path.at(-1)));
 const pathActive=!done&&f.entry?new Set(f.entry.path.slice(1).map((n,i)=>[f.entry.path[i],n].sort().join(''))):new Set();
 const color=colors[state.algo];
 let svg=`<title>${state.algo}, ${done?route(current.path):'langkah '+state.frame}</title>`;
 for(const [a,b] of edges){const p=pos[a],q=pos[b],w=cfg.graph[a][b],closed=w===undefined,isRoute=chosen.has([a,b].sort().join('')),active=pathActive.has([a,b].sort().join(''));const stroke=closed?'#be7379':isRoute?color:active?'#50788e':'#b9c9d6';const mx=(p[0]+q[0])/2,my=(p[1]+q[1])/2;svg+=`<g><title>${label(a)}–${label(b)}: ${closed?'ditutup':w+' km'}</title><line x1="${p[0]}" y1="${p[1]}" x2="${q[0]}" y2="${q[1]}" stroke="${stroke}" stroke-width="${isRoute?5:active?4:2.5}" ${closed?'stroke-dasharray="7 6"':''}/><rect x="${mx-20}" y="${my-13}" width="40" height="26" rx="7" fill="${isRoute?color:'#fff'}" stroke="${closed?'#e2bfc1':'#dbe5eb'}"/><text x="${mx}" y="${my+5}" text-anchor="middle" class="edge-number" fill="${isRoute?'white':closed?'#a95761':'#35556b'}">${closed?'×':w}</text></g>`;}
 for(const [n,[x,y]] of Object.entries(pos)){const inRoute=done&&current.path?.includes(n),expanded=f.expanded.includes(n),wait=awaiting.has(n),currentNode=f.node===n;const fill=inRoute?color:expanded?'#183c57':'white',stroke=inRoute?color:currentNode?'#567d97':wait?'#cf972b':'#b5c8d6';svg+=`<g tabindex="0" role="img" aria-label="${label(n)}, ${expanded?'sudah diekspansi':wait?'menunggu':'belum diproses'}, h ${state.algo==='A*'?cfg.h[n]:0}"><title>${label(n)} · g = ${f.best[n]??'belum diketahui'} · h = ${state.algo==='A*'?cfg.h[n]:0}</title>${currentNode?`<circle cx="${x}" cy="${y}" r="32" fill="none" stroke="${color}" stroke-width="1.5" opacity=".25"/>`:''}<circle class="node-circle" cx="${x}" cy="${y}" r="24" fill="${fill}" stroke="${stroke}" stroke-width="${wait?3:2}"/><text class="node-letter" x="${x}" y="${y+6}" text-anchor="middle" fill="${inRoute||expanded?'white':'#17344a'}">${n}</text><text class="node-label" x="${x}" y="${y+48}" text-anchor="middle">${label(n)}</text><text class="node-h" x="${x}" y="${y+65}" text-anchor="middle">${n===cfg.start&&n===cfg.goal?'awal & tujuan':state.algo==='BFS'?n===cfg.start?'awal':n===cfg.goal?'tujuan':'':`h = ${state.algo==='A*'?cfg.h[n]:0}`}</text></g>`;}
 $('#graph').innerHTML=svg;
}
function table(headers,rows){return `<table><thead><tr>${headers.map(h=>`<th scope="col">${h}</th>`).join('')}</tr></thead><tbody>${rows.map(r=>`<tr ${r.id?`data-select="${r.id}" tabindex="0" aria-label="Pilih ${r.id}"`:''} class="${String(r.id)===state.value?'current-row':''}">${r.cells.map(c=>`<td>${c}</td>`).join('')}</tr>`).join('')}</tbody></table>`;}
function renderExperiment(){
 let title,ref,headers,rows;$('#experiment-chart').innerHTML='';
 if(state.mode==='scenario'){
  title='Lima kondisi jalan';ref='Tabel VI';headers=['Skenario','A* · km / ekspansi','Dijkstra · km / ekspansi','BFS · km / ekspansi'];rows=scenarios.map(([id,t])=>({id,cells:[`<b>${id}</b> · ${t}`,...algos.map(a=>{const r=solve(config('scenario',id),a);return `${number(r.cost)} / ${r.expanded.length}`;})]}));
 }else if(state.mode==='heuristic'){
  title='Tujuh konfigurasi heuristik';ref='Tabel VIII–IX';headers=['Kode','h(R, W, T, P, K)','Admissible','Konsisten','Jarak','Ekspansi'];rows=hs.map(h=>{const r=solve(config('heuristic',h.id));return {id:h.id,cells:[`<b>${h.id}</b> · ${h.name}`,h.values.join(' · '),h.ad?'Ya':'Tidak',h.con?'Ya':'Tidak',r.cost+' km',r.expanded.length]};});
 }else if(state.mode==='weight'){
  title='Saat jarak jalan berubah';ref='Tabel X';headers=['Bobot P–K','A* · km / ekspansi','Dijkstra · km / ekspansi','BFS · km / ekspansi','Optimum'];rows=Array.from({length:9},(_,i)=>{const w=i+2,c=config('weight',w);return {id:String(w),cells:[w+' km',...algos.map(a=>{const r=solve(c,a);return `${r.cost} / ${r.expanded.length}`;}),optimum(c)+' km']};});drawWeightChart();
 }else{
  title='Bagaimana biaya diperbaiki';ref='Tabel XI';headers=['Dipilih','g','Peristiwa'];rows=[{cells:['S',0,'A ditemukan dengan g = 3; B dengan g = 1.']},{cells:['A',3,'G ditemukan dengan biaya 5.']},{cells:['B',1,'Biaya A diperbaiki dari 3 menjadi 2.']},{cells:['A',2,'Biaya G diperbaiki dari 5 menjadi 4.']},{cells:['G',4,'Selesai: S → B → A → G.']}];
 }
 $('#experiment-title').textContent=title;$('#table-ref').textContent=ref;$('#experiment-table').innerHTML=table(headers,rows);
 document.querySelectorAll('tr[data-select]').forEach(tr=>{const select=()=>{changeValue(tr.dataset.select);configureControls();};tr.addEventListener('click',select);tr.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();select();}});});
}
function drawWeightChart(){const xs=Array.from({length:9},(_,i)=>i+2),x=w=>70+(w-2)*91,y=v=>208-(v-6)*44;let svg='<svg class="mini-chart" viewBox="0 0 900 275" role="img" aria-label="Grafik bobot jalan: A* dan Dijkstra meningkat dari 6 km ke 9 km, lalu tetap. BFS selalu 9 km.">';for(let v=6;v<=10;v++)svg+=`<line x1="70" y1="${y(v)}" x2="798" y2="${y(v)}" stroke="#e1e8ee"/><text x="45" y="${y(v)+5}" font-size="14" fill="#526879">${v}</text>`;svg+=`<text x="70" y="20" font-size="14" fill="#526879">Jarak rute (km)</text><line x1="${x(+state.value)}" y1="32" x2="${x(+state.value)}" y2="218" stroke="#536e84" stroke-dasharray="4 5"/>`;
 const ys=xs.map(w=>solve(config('weight',w)).cost);svg+=`<polyline points="${xs.map((w,i)=>`${x(w)},${y(ys[i])}`).join(' ')}" fill="none" stroke="${colors['A*']}" stroke-width="4"/><line x1="70" y1="${y(9)}" x2="798" y2="${y(9)}" stroke="${colors.BFS}" stroke-width="3" stroke-dasharray="7 5"/>`;
 xs.forEach((w,i)=>{svg+=`<circle cx="${x(w)}" cy="${y(ys[i])}" r="5" fill="${colors['A*']}"/><rect x="${x(w)-4}" y="${y(9)-4}" width="8" height="8" fill="white" stroke="${colors.BFS}" stroke-width="2"/><text x="${x(w)}" y="236" text-anchor="middle" font-size="14" fill="#526879">${w}</text>`;});svg+='<text x="440" y="265" text-anchor="middle" font-size="14" fill="#526879">Bobot Perpustakaan–Kampus (km)</text></svg>';
 $('#experiment-chart').innerHTML=svg+`<div class="chart-legend"><span style="--accent:${colors['A*']}">A* dan Dijkstra</span><span style="--accent:${colors.BFS}">BFS</span></div>`;
}
document.querySelectorAll('[data-mode]').forEach(b=>b.addEventListener('click',()=>selectMode(b.dataset.mode)));
document.querySelectorAll('[data-metric]').forEach(b=>b.addEventListener('click',()=>{state.metric=b.dataset.metric;renderBars();}));
$('#play').addEventListener('click',()=>{if(timer){pause();return;}if(state.frame>=current.frames.length-1)state.frame=0;renderFrame();$('#play').textContent='Jeda';timer=setInterval(()=>{state.frame=Math.min(state.frame+1,current.frames.length-1);renderFrame();if(state.frame===current.frames.length-1)pause();},1500);});
$('#step').addEventListener('click',()=>{pause();state.frame=Math.min(state.frame+1,current.frames.length-1);renderFrame();});
$('#reset').addEventListener('click',()=>{pause();state.frame=0;renderFrame();});
document.addEventListener('visibilitychange',()=>{if(document.hidden)pause();});
calculate();render(true);
// The optional browser API uses the same controls and calculated results.
if(document.modelContext?.registerTool){
 const lifecycle=new AbortController();
 const snapshot=()=>({mode:state.mode,value:state.value,algorithm:state.algo,optimum:best,results:Object.fromEntries(Object.entries(runs).map(([a,r])=>[a,{cost:r.cost,path:r.path?.map(label)??null,expansions:r.expanded.length}]))});
 const register=tool=>{try{Promise.resolve(document.modelContext.registerTool(tool,{signal:lifecycle.signal})).catch(()=>{});}catch{}};
 register({name:'read_comparison',title:'Baca perbandingan',description:'Read the currently displayed algorithm comparison.',inputSchema:{type:'object',properties:{},additionalProperties:false},annotations:{readOnlyHint:true,untrustedContentHint:false},execute:()=>snapshot()});
 register({name:'configure_comparison',title:'Atur perbandingan',description:'Select a report experiment and display its results and route.',inputSchema:{type:'object',properties:{mode:{type:'string',enum:['scenario','heuristic','weight','reopen']},value:{type:'string'},algorithm:{type:'string',enum:algos}},required:['mode','value'],additionalProperties:false},annotations:{readOnlyHint:false,untrustedContentHint:false},execute:input=>{if(!input||typeof input!=='object')throw new Error('Pengaturan tidak valid.');const {mode,value,algorithm='A*'}=input;const valid=mode==='scenario'?scenarios.some(s=>s[0]===value):mode==='heuristic'?hs.some(h=>h.id===value):mode==='weight'?/^(2|3|4|5|6|7|8|9|10)$/.test(value):mode==='reopen'?value==='R1':false;if(!valid||!algos.includes(algorithm)||(['heuristic','reopen'].includes(mode)&&algorithm!=='A*'))throw new Error('Pilih eksperimen dan algoritma yang tersedia.');selectMode(mode,value);state.algo=algorithm;current=runs[algorithm];state.frame=current.frames.length-1;render();return snapshot();}});
 window.addEventListener('pagehide',()=>lifecycle.abort(),{once:true});
}
