# A* Sederhana - Pencarian Rute Terpendek

Implementasi algoritma A* untuk mencari rute terpendek dari **Rumah** ke **Kampus** pada graf berbobot (jarak dalam kilometer).

Program dilengkapi **5 skenario pengujian** yang membandingkan perhitungan manual dengan hasil program, serta validasi otomatis terhadap kebenaran rute.

## Pustaka

| Pustaka | Keterangan |
|---|---|
| Python 3.x | Bahasa pemrograman |
| `heapq` | Modul bawaan Python sebagai priority queue |

Tidak ada pustaka tambahan dari luar (tidak perlu `pip install` apa pun).

## Cara Menjalankan

Pastikan Python 3 sudah terpasang, lalu jalankan di terminal:

```bash
python a_star_sederhana.py
```

## Data Graf dan Heuristik

Graf bersifat dua arah (bila ada jalan A–B, maka B–A juga tersedia).

| Tempat | Tetangga (jarak km) |
|---|---|
| Rumah | Warung (2), Taman (4) |
| Warung | Rumah (2), Perpustakaan (2) |
| Taman | Rumah (4), Kampus (5) |
| Perpustakaan | Warung (2), Kampus (3) |
| Kampus | Taman (5), Perpustakaan (3) |

Nilai heuristik (`h`) — perkiraan jarak tiap tempat menuju Kampus:

| Tempat | h |
|---|---|
| Rumah | 6 |
| Warung | 4 |
| Taman | 4 |
| Perpustakaan | 2 |
| Kampus | 0 |

## Menu Program

```text
PENGUJIAN ALGORITMA A*
1. S1 — Jalan normal
2. S2 — Jalan Warung–Perpustakaan ditutup
3. S3 — Jarak Perpustakaan–Kampus menjadi 10 km
4. S4 — Semua akses menuju Kampus terputus
5. S5 — Titik awal sama dengan tujuan
6. Jalankan semua skenario
0. Keluar
```

## Skenario Pengujian

| Kode | Skenario | Perhitungan Manual | Harapan |
|---|---|---|---|
| S1 | Jalan normal | Rumah → Warung → Perpustakaan → Kampus = 2 + 2 + 3 | 7 km |
| S2 | Jalan Warung–Perpustakaan ditutup | Rute ke Kampus melalui Taman = 4 + 5 | 9 km |
| S3 | Jarak Perpustakaan–Kampus menjadi 10 km | Rute melalui Taman = 4 + 5 | 9 km |
| S4 | Semua akses menuju Kampus terputus | Tidak ada jalan ke Kampus | Tidak ada rute |
| S5 | Titik awal sama dengan tujuan (Kampus) | Sudah di tujuan, tanpa perpindahan | 0 km |

## Cara Kerja A\*

- **Graf** — dictionary berisi tempat dan jarak antar tempat yang saling terhubung.
- **Heuristik** — perkiraan jarak masing-masing tempat menuju Kampus (nilai `h`).
- **Rumus A\*** — `f = g + h`, di mana `g` adalah jarak aktual dari titik awal dan `h` adalah perkiraan heuristik ke tujuan.
- **`heapq`** — dipakai sebagai priority queue agar kandidat dengan `f` terkecil selalu diproses duluan.
- **`biaya_terbaik`** — menyimpan biaya terbaik ke tiap tempat agar jalur lama yang sudah lebih mahal bisa diabaikan.
- **`deepcopy`** — setiap skenario memakai salinan graf terpisah, sehingga perubahan satu skenario (mis. menutup jalan) tidak memengaruhi skenario lain.

## Contoh Keluaran

```text
=================================================================
S2: Jalan Warung–Perpustakaan ditutup
=================================================================
Titik awal : Rumah
Tujuan     : Kampus

PERHITUNGAN MANUAL
Jalur melalui Warung tidak dapat dilanjutkan ke Perpustakaan.
Rute yang tersedia menuju Kampus melalui Taman:
4 + 5 = 9 km.

HASIL PROGRAM
Rute terpendek: Rumah -> Taman -> Kampus
Perhitungan rute: 4 + 5 = 9 km
Total jarak: 9 km

Status pengujian: LULUS — sesuai perhitungan manual.
```

Menjalankan **menu 6** akan menguji semua skenario sekaligus:

```text
=================================================================
RINGKASAN: 5 dari 5 skenario lulus.
=================================================================
```

## Status Pengujian

Setiap skenario divalidasi otomatis, bukan hanya mencocokkan total jarak:

- Total jarak hasil program harus sama dengan perhitungan manual.
- Titik awal dan titik tujuan rute harus benar.
- Setiap ruas pada rute harus benar-benar ada di graf skenario tersebut.
- Jumlah bobot seluruh ruas harus sama dengan total jarak yang dilaporkan.

Bila semua kondisi terpenuhi, skenario dinyatakan **LULUS**; jika tidak, muncul status **GAGAL — perlu diperiksa**.
