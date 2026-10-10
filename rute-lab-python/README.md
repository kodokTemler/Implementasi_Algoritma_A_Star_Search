# RuteLab dengan backend Python

## Menjalankan di Windows
Ekstrak seluruh ZIP. Buka folder rute-lab-python di VS Code, lalu Terminal > New Terminal.
Gunakan Python 3.10 atau lebih baru:

```powershell
py server.py
```

Buka http://localhost:8000/ . Biarkan terminal tetap terbuka.
Jika `py` tidak tersedia, gunakan `python server.py`.
Tidak perlu pip install, npm, Flask, database, atau menjalankan Laragon.
Folder boleh disimpan di C:\laragon\www, tetapi akses melalui port server Python
(http://localhost:8000/), bukan URL Apache Laragon atau file://.
Jika port terpakai: `py server.py --port 8001`, kemudian http://localhost:8001/.
Ctrl+C untuk menghentikan server. Server ini khusus demonstrasi lokal, terikat ke 127.0.0.1.

## Alur yang dijelaskan kepada dosen
1. server.py menyajikan halaman dari folder static.
2. Browser meminta GET /api/eksperimen.
3. data_kasus.py menyiapkan 5 skenario, 7 heuristik, 9 bobot, dan contoh reopen.
4. algoritma.py menjalankan A* (heapq), Dijkstra (h=0), BFS (deque), serta enumerasi acuan.
5. Python mengembalikan rute, biaya, ekspansi, dan jejak antrean dalam JSON.
6. JavaScript menggambar peta, tabel, grafik, dan memutar jejak dari Python.

Semua 50 eksekusi dihitung saat halaman dimuat. Pergantian tab, slider, dan tombol
animasi membaca hasil Python yang sudah diterima, tanpa menghitung algoritma di JavaScript.
Muat ulang halaman untuk meminta perhitungan ulang. Buka http://localhost:8000/api/eksperimen
untuk melihat respons mentah. Terminal mencetak pesan setiap perhitungan berhasil.

## File yang perlu dipresentasikan
- algoritma.py: buka fungsi a_star; jelaskan heapq, g+h, biaya_terbaik, pemeriksaan
  kandidat lama, pemeriksaan tujuan, dan perbaikan biaya tetangga. Fungsi dijkstra
  memanggil A* dengan h=0. Fungsi bfs menggunakan deque dan popleft.
- data_kasus.py: data jalan, heuristik, konfigurasi lima skenario, dan penyiapan hasil.
- server.py: server web dan endpoint penghubung Python dengan browser.
- uji_backend.py: pemeriksaan 50 eksekusi dan validasi hasil.
- static/index.html: struktur halaman.
- static/style.css: desain responsif.
- static/app.js: interaksi, animasi, grafik, tabel.
- static/engine.js: adapter pengambil JSON, bukan mesin algoritma JavaScript.

## Perbedaan dengan kode Python sederhana
Graf memakai singkatan R/W/T/P/K agar cocok dengan peta; NAMA memetakan ke nama lengkap.
Heap menyimpan (f, g, nama_lengkap_jalur, jalur_singkatan). Komponen nama lengkap menjaga
aturan pemecah nilai seri sesuai kode laporan. Return berupa dictionary berisi
path, cost, expanded, frames agar browser bisa menampilkan animasi, bukan hanya tuple rute/jarak.
Pencatatan frames adalah tambahan untuk tampilan; biaya dan aturan pemilihan tetap mengikuti A*.
Jumlah ekspansi tidak memasukkan tujuan yang langsung dikembalikan.

## Mencoba dan memeriksa
```powershell
py uji_backend.py
```
S1: A* 7 km/3 ekspansi; Dijkstra 7/4; BFS 9/4.
S2: semuanya 9/3. S3: semuanya 9/4. S4: tidak ada rute/4. S5: 0/0.
H6 sengaja berlebih dan menghasilkan 9 km (bukan optimum 7).
Reopen: S,A,B,A; biaya 4.

Untuk mengubah kode atau data Python: simpan perubahan, hentikan server dengan Ctrl+C,
jalankan lagi, lalu refresh browser. Server tidak memakai auto-reload.
Data awal mengikuti laporan; mengubah data perlu diikuti penyesuaian teks penjelasan
skenario di app.js yang masih khusus untuk contoh laporan. Status heuristik pada tabel
H0–H6 dihitung oleh Python. Pastikan bobot nonnegatif dan heuristik valid untuk jaminan optimalitas.

Google Fonts pada CSS bersifat opsional; tanpa internet memakai font pengganti.
Tidak mengukur waktu/memori. Data ilustratif, bukan peta nyata. Kode disusun dengan bantuan AI;
pahami implementasi dan ikuti aturan pengungkapan bantuan dari dosen.
