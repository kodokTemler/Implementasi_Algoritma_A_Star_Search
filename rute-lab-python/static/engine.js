// Adapter API. Tidak ada algoritma pencarian di JavaScript.
let data;
try {
 const response = await fetch('/api/eksperimen', {cache:'no-store'});
 if (!response.ok) throw new Error(`HTTP ${response.status}`);
 data = await response.json();
} catch (error) {
 document.body.innerHTML = '<main><h1>Backend Python belum tersedia</h1><p>Jalankan <code>py server.py</code>, lalu buka <code>http://localhost:8000/</code>. Periksa terminal untuk rincian kesalahan.</p><button onclick="location.reload()">Coba lagi</button></main>';
 throw error;
}
export const {names, algos, scenarios, hs} = data;
export function config(mode='scenario', value='S1') {
 const key = `${mode}:${value}`;
 return {...data.experiments[key].cfg, key};
}
export function solve(cfg, algo='A*') {
 return data.experiments[cfg.key].runs[algo];
}
export function optimum(cfg) {
 return data.experiments[cfg.key].best;
}
