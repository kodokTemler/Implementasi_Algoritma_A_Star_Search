import heapq
from copy import deepcopy


# =========================================================
# 1. DATA DASAR
# =========================================================

graf = {
    "Rumah": {"Warung": 2, "Taman": 4},
    "Warung": {"Rumah": 2, "Perpustakaan": 2},
    "Taman": {"Rumah": 4, "Kampus": 5},
    "Perpustakaan": {"Warung": 2, "Kampus": 3},
    "Kampus": {"Taman": 5, "Perpustakaan": 3},
}

heuristik = {
    "Rumah": 6,
    "Warung": 4,
    "Taman": 4,
    "Perpustakaan": 2,
    "Kampus": 0,
}


# =========================================================
# 2. ALGORITMA A* — SAMA DENGAN KODE ANDA
# =========================================================

def a_star(graf, heuristik, awal, tujuan):
    # Isi antrean: (f, g, jalur).
    antrean = [(heuristik[awal], 0, [awal])]

    # Biaya terbaik yang sudah ditemukan ke setiap tempat.
    biaya_terbaik = {awal: 0}

    while antrean:
        # Ambil kandidat dengan prioritas terkecil.
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


# =========================================================
# 3. FUNGSI UNTUK MENUTUP JALAN DUA ARAH
# =========================================================

def tutup_jalan(data_graf, tempat_a, tempat_b):
    del data_graf[tempat_a][tempat_b]
    del data_graf[tempat_b][tempat_a]


# =========================================================
# 4. MENYIAPKAN LIMA SKENARIO
# =========================================================

def buat_skenario():
    # Setiap skenario memakai salinan graf yang terpisah.
    # Perubahan satu skenario tidak memengaruhi skenario lain.
    daftar = {}

    # S1: menggunakan seluruh jalan pada data asli.
    daftar["S1"] = {
        "nama": "Jalan normal",
        "graf": deepcopy(graf),
        "awal": "Rumah",
        "tujuan": "Kampus",
        "manual": (
            "Melalui Warung dan Perpustakaan: 2 + 2 + 3 = 7 km.\n"
            "Melalui Taman: 4 + 5 = 9 km.\n"
            "Jarak minimum = 7 km."
        ),
        "harapan": 7,
    }

    # S2: menutup jalan Warung–Perpustakaan pada kedua arah.
    graf_s2 = deepcopy(graf)
    tutup_jalan(graf_s2, "Warung", "Perpustakaan")

    daftar["S2"] = {
        "nama": "Jalan Warung–Perpustakaan ditutup",
        "graf": graf_s2,
        "awal": "Rumah",
        "tujuan": "Kampus",
        "manual": (
            "Jalur melalui Warung tidak dapat dilanjutkan "
            "ke Perpustakaan.\n"
            "Rute yang tersedia menuju Kampus melalui Taman:\n"
            "4 + 5 = 9 km."
        ),
        "harapan": 9,
    }

    # S3: mengubah jarak Perpustakaan–Kampus menjadi 10 km.
    graf_s3 = deepcopy(graf)
    graf_s3["Perpustakaan"]["Kampus"] = 10
    graf_s3["Kampus"]["Perpustakaan"] = 10

    daftar["S3"] = {
        "nama": "Jarak Perpustakaan–Kampus menjadi 10 km",
        "graf": graf_s3,
        "awal": "Rumah",
        "tujuan": "Kampus",
        "manual": (
            "Melalui Warung dan Perpustakaan: 2 + 2 + 10 = 14 km.\n"
            "Melalui Taman: 4 + 5 = 9 km.\n"
            "Jarak minimum = 9 km."
        ),
        "harapan": 9,
    }

    # S4: menghapus seluruh jalan yang terhubung ke Kampus.
    graf_s4 = deepcopy(graf)
    tutup_jalan(graf_s4, "Taman", "Kampus")
    tutup_jalan(graf_s4, "Perpustakaan", "Kampus")

    daftar["S4"] = {
        "nama": "Semua akses menuju Kampus terputus",
        "graf": graf_s4,
        "awal": "Rumah",
        "tujuan": "Kampus",
        "manual": (
            "Tidak ada jalan yang terhubung ke Kampus.\n"
            "Hasil yang benar: tidak ada rute."
        ),
        "harapan": None,
    }

    # S5: pengguna sudah berada di tujuan.
    daftar["S5"] = {
        "nama": "Titik awal sama dengan tujuan",
        "graf": deepcopy(graf),
        "awal": "Kampus",
        "tujuan": "Kampus",
        "manual": (
            "Posisi awal sudah berada di Kampus.\n"
            "Tidak perlu melewati jalan apa pun.\n"
            "Total jarak = 0 km."
        ),
        "harapan": 0,
    }

    return daftar


# =========================================================
# 5. MENJALANKAN DAN MEMERIKSA SATU SKENARIO
# =========================================================

def jalankan_skenario(kode, data):
    print("\n" + "=" * 65)
    print(f"{kode}: {data['nama']}")
    print("=" * 65)

    print("Titik awal :", data["awal"])
    print("Tujuan     :", data["tujuan"])

    print("\nPERHITUNGAN MANUAL")
    print(data["manual"])

    # Jalankan fungsi A* menggunakan graf skenario yang dipilih.
    jalur, jarak = a_star(
        data["graf"],
        heuristik,
        data["awal"],
        data["tujuan"]
    )

    print("\nHASIL PROGRAM")

    if jalur is None:
        print("Tidak ada rute menuju kampus.")
    else:
        print("Rute terpendek:", " -> ".join(jalur))

        # Tampilkan bobot setiap ruas pada rute hasil.
        bobot_ruas = [
            data["graf"][a][b]
            for a, b in zip(jalur, jalur[1:])
        ]

        if bobot_ruas:
            penjumlahan = " + ".join(map(str, bobot_ruas))
            print(f"Perhitungan rute: {penjumlahan} = {jarak} km")
        else:
            print("Tidak ada perpindahan karena awal = tujuan.")

        print("Total jarak:", jarak, "km")

    # Periksa hasil terhadap jawaban manual.
    if data["harapan"] is None:
        sesuai = jalur is None and jarak is None
    else:
        sesuai = (
            jalur is not None
            and jarak == data["harapan"]
        )

        # Selain biaya, periksa awal, tujuan, dan keabsahan rute.
        if sesuai:
            sesuai = (
                jalur[0] == data["awal"]
                and jalur[-1] == data["tujuan"]
                and all(
                    b in data["graf"].get(a, {})
                    for a, b in zip(jalur, jalur[1:])
                )
            )

        if sesuai:
            biaya_rute = sum(
                data["graf"][a][b]
                for a, b in zip(jalur, jalur[1:])
            )
            sesuai = biaya_rute == jarak

    print(
        "\nStatus pengujian:",
        "LULUS — sesuai perhitungan manual."
        if sesuai
        else "GAGAL — perlu diperiksa."
    )

    return sesuai


# =========================================================
# 6. MENU PROGRAM
# =========================================================

if __name__ == "__main__":
    daftar_skenario = buat_skenario()

    while True:
        print("\nPENGUJIAN ALGORITMA A*")
        print("1. S1 — Jalan normal")
        print("2. S2 — Jalan Warung–Perpustakaan ditutup")
        print("3. S3 — Jarak Perpustakaan–Kampus menjadi 10 km")
        print("4. S4 — Semua akses menuju Kampus terputus")
        print("5. S5 — Titik awal sama dengan tujuan")
        print("6. Jalankan semua skenario")
        print("0. Keluar")

        pilihan = input("\nPilih menu [0–6]: ").strip()

        if pilihan == "0":
            print("Program selesai.")
            break

        elif pilihan == "6":
            jumlah_lulus = 0

            for kode, data in daftar_skenario.items():
                if jalankan_skenario(kode, data):
                    jumlah_lulus += 1

            print("\n" + "=" * 65)
            print(
                f"RINGKASAN: {jumlah_lulus} dari "
                f"{len(daftar_skenario)} skenario lulus."
            )
            print("=" * 65)

        elif pilihan in {"1", "2", "3", "4", "5"}:
            kode = f"S{pilihan}"
            jalankan_skenario(kode, daftar_skenario[kode])

        else:
            print("Pilihan tidak valid. Masukkan angka 0 sampai 6.")
