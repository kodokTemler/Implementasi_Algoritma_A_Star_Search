# A* Sederhana - Pencarian Rute Terpendek

Implementasi algoritma A* untuk mencari rute terpendek dari **Rumah** ke **Kampus** pada graf berbobot (jarak dalam kilometer).

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

## Contoh Keluaran

```text
Rute terpendek: Rumah -> Warung -> Perpustakaan -> Kampus
Total jarak: 7 km
```

## Penjelasan Singkat

- **Graf** — dictionary berisi tempat dan jarak antar tempat yang saling terhubung.
- **Heuristik** — perkiraan jarak masing-masing tempat menuju Kampus (nilai `h`).
- **Rumus A\*** — `f = g + h`, di mana `g` adalah jarak aktual dari titik awal dan `h` adalah perkiraan heuristik ke tujuan.
- **`heapq`** — dipakai sebagai priority queue agar kandidat dengan `f` terkecil selalu diproses duluan.
- **`biaya_terbaik`** — menyimpan biaya terbaik ke tiap tempat agar jalur lama yang sudah lebih mahal bisa diabaikan.
