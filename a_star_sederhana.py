import heapq

# Daftar jalan dan jaraknya dalam kilometer.
graf = {
    "Rumah": {"Warung": 2, "Taman": 4},
    "Warung": {"Rumah": 2, "Perpustakaan": 2},
    "Taman": {"Rumah": 4, "Kampus": 5},
    "Perpustakaan": {"Warung": 2, "Kampus": 3},
    "Kampus": {"Taman": 5, "Perpustakaan": 3},
}

# Perkiraan jarak khusus menuju Kampus.
heuristik = {
    "Rumah": 6,
    "Warung": 4,
    "Taman": 4,
    "Perpustakaan": 2,
    "Kampus": 0,
}


def a_star(graf, heuristik, awal, tujuan):
    # Isi antrean: (f, g, jalur).
    antrean = [(heuristik[awal], 0, [awal])]

    # Biaya terbaik yang sudah ditemukan ke setiap tempat.
    biaya_terbaik = {awal: 0}

    while antrean:
        # Ambil kandidat dengan f terkecil.
        _, jarak, jalur = heapq.heappop(antrean)
        sekarang = jalur[-1]

        # Abaikan catatan biaya lama.
        if jarak != biaya_terbaik[sekarang]:
            continue

        # Jika tujuan dipilih, kembalikan hasil.
        if sekarang == tujuan:
            return jalur, jarak

        # Periksa tempat yang terhubung langsung.
        for tetangga, jarak_jalan in graf[sekarang].items():
            g_baru = jarak + jarak_jalan

            # Simpan hanya jika menemukan biaya lebih murah.
            if g_baru < biaya_terbaik.get(tetangga, float("inf")):
                biaya_terbaik[tetangga] = g_baru

                # Rumus utama A*: f = g + h.
                f_baru = g_baru + heuristik[tetangga]

                # Tambahkan tempat berikutnya ke jalur.
                jalur_baru = jalur + [tetangga]

                heapq.heappush(
                    antrean,
                    (f_baru, g_baru, jalur_baru)
                )

    return None, None


if __name__ == "__main__":
    jalur, jarak = a_star(
        graf, heuristik, "Rumah", "Kampus"
    )

    if jalur is None:
        print("Tidak ada rute menuju kampus.")
    else:
        print("Rute terpendek:", " -> ".join(jalur))
        print("Total jarak:", jarak, "km")