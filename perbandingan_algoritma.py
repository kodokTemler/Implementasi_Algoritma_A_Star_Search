import heapq
from collections import deque
from copy import deepcopy

import matplotlib.pyplot as plt


# =========================================================
# 1. DATA JALAN DAN HEURISTIK
# =========================================================

GRAF = {
    "Rumah": {"Warung": 2, "Taman": 4},
    "Warung": {"Rumah": 2, "Perpustakaan": 2},
    "Taman": {"Rumah": 4, "Kampus": 5},
    "Perpustakaan": {"Warung": 2, "Kampus": 3},
    "Kampus": {"Taman": 5, "Perpustakaan": 3},
}

HEURISTIK = {
    "Rumah": 6,
    "Warung": 4,
    "Taman": 4,
    "Perpustakaan": 2,
    "Kampus": 0,
}


# =========================================================
# 2. ALGORITMA A*
# =========================================================

def a_star(graf, heuristik, awal, tujuan):
    antrean = [(heuristik[awal], 0, [awal])]
    biaya_terbaik = {awal: 0}
    ekspansi = []

    while antrean:
        _, jarak, jalur = heapq.heappop(antrean)
        sekarang = jalur[-1]

        # Lewati kandidat lama yang sudah memiliki biaya lebih baik.
        if jarak != biaya_terbaik[sekarang]:
            continue

        # Tujuan tidak dihitung sebagai ekspansi karena
        # daftar tetangganya tidak diperiksa.
        if sekarang == tujuan:
            return jalur, jarak, ekspansi

        ekspansi.append(sekarang)

        for tetangga, bobot in graf[sekarang].items():
            g_baru = jarak + bobot

            if g_baru < biaya_terbaik.get(tetangga, float("inf")):
                biaya_terbaik[tetangga] = g_baru
                f_baru = g_baru + heuristik[tetangga]

                heapq.heappush(
                    antrean,
                    (f_baru, g_baru, jalur + [tetangga])
                )

    return None, None, ekspansi


# =========================================================
# 3. ALGORITMA DIJKSTRA
# =========================================================

def dijkstra(graf, awal, tujuan):
    # A* dengan seluruh heuristik nol bekerja seperti Dijkstra.
    heuristik_nol = {tempat: 0 for tempat in graf}
    return a_star(graf, heuristik_nol, awal, tujuan)


# =========================================================
# 4. ALGORITMA BFS
# =========================================================

def bfs(graf, awal, tujuan):
    antrean = deque([[awal]])
    ditemukan = {awal}
    ekspansi = []

    while antrean:
        jalur = antrean.popleft()
        sekarang = jalur[-1]

        if sekarang == tujuan:
            # BFS memilih rute berdasarkan jumlah ruas.
            # Total kilometer baru dijumlahkan dari rute tersebut.
            jarak = sum(
                graf[a][b]
                for a, b in zip(jalur, jalur[1:])
            )
            return jalur, jarak, ekspansi

        ekspansi.append(sekarang)

        for tetangga in graf[sekarang]:
            if tetangga not in ditemukan:
                ditemukan.add(tetangga)
                antrean.append(jalur + [tetangga])

    return None, None, ekspansi


# =========================================================
# 5. MEMBUAT LIMA KASUS UJI
# =========================================================

def buat_kasus(nomor):
    # Salin data agar perubahan tidak merusak graf asli.
    graf = deepcopy(GRAF)
    awal, tujuan = "Rumah", "Kampus"

    if nomor == 1:
        nama = "S1 - Jalan normal"

    elif nomor == 2:
        nama = "S2 - Warung–Perpustakaan ditutup"
        del graf["Warung"]["Perpustakaan"]
        del graf["Perpustakaan"]["Warung"]

    elif nomor == 3:
        nama = "S3 - Perpustakaan–Kampus menjadi 10 km"
        graf["Perpustakaan"]["Kampus"] = 10
        graf["Kampus"]["Perpustakaan"] = 10

    elif nomor == 4:
        nama = "S4 - Kampus tidak terhubung"
        del graf["Taman"]["Kampus"]
        del graf["Perpustakaan"]["Kampus"]
        graf["Kampus"] = {}

    elif nomor == 5:
        nama = "S5 - Awal sama dengan tujuan"
        awal = tujuan = "Kampus"

    else:
        raise ValueError("Nomor kasus harus 1 sampai 5.")

    return nama, graf, awal, tujuan


# =========================================================
# 6. MENAMPILKAN HASIL DAN GRAFIK
# =========================================================

def bandingkan(nomor):
    nama, graf, awal, tujuan = buat_kasus(nomor)

    hasil = {
        "A*": a_star(graf, HEURISTIK, awal, tujuan),
        "Dijkstra": dijkstra(graf, awal, tujuan),
        "BFS": bfs(graf, awal, tujuan),
    }

    print("\n" + "=" * 65)
    print(nama)
    print("=" * 65)

    for algoritma, (jalur, jarak, ekspansi) in hasil.items():
        print(f"\nAlgoritma       : {algoritma}")
        print(
            "Rute            :",
            " -> ".join(jalur) if jalur else "Tidak ada rute"
        )
        print(
            "Total jarak     :",
            f"{jarak} km" if jarak is not None else "Tidak tersedia"
        )
        print("Jumlah ekspansi :", len(ekspansi))
        print(
            "Urutan ekspansi :",
            " -> ".join(ekspansi) if ekspansi else "Tidak ada"
        )

    algoritma = list(hasil)
    warna = ["#217A89", "#64748B", "#D97732"]

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

    # Grafik jarak: rute yang tidak tersedia tidak diberi nilai nol.
    jarak_valid = []

    for i, nama_algoritma in enumerate(algoritma):
        jarak = hasil[nama_algoritma][1]

        if jarak is None:
            axes[0].text(
                i, 0.5, "Tidak ada\nrute",
                ha="center",
                transform=axes[0].get_xaxis_transform()
            )
        else:
            jarak_valid.append(jarak)
            axes[0].bar(i, jarak, color=warna[i], width=0.6)
            axes[0].annotate(
                f"{jarak:g}",
                (i, jarak),
                xytext=(0, 5),
                textcoords="offset points",
                ha="center"
            )

    axes[0].set_xticks(range(3), algoritma)
    axes[0].set_xlim(-0.6, 2.6)
    axes[0].set_ylim(0, max([1] + jarak_valid) * 1.3)
    axes[0].set_title("Perbandingan total jarak")
    axes[0].set_ylabel("Jarak (km)")

    # Grafik jumlah ekspansi.
    jumlah = [len(hasil[a][2]) for a in algoritma]

    bars = axes[1].bar(
        algoritma, jumlah, color=warna, width=0.6
    )
    axes[1].bar_label(bars, padding=4)
    axes[1].set_ylim(0, max([1] + jumlah) * 1.3)
    axes[1].set_title("Perbandingan jumlah ekspansi")
    axes[1].set_ylabel("Jumlah ekspansi simpul")

    for ax in axes:
        ax.set_axisbelow(True)
        ax.grid(axis="y", alpha=0.2)

    fig.suptitle(nama)
    fig.tight_layout()

    nama_file = f"perbandingan_S{nomor}.png"
    fig.savefig(nama_file, dpi=200)
    print(f"\nGrafik disimpan sebagai: {nama_file}")

    plt.show()
    plt.close(fig)


# =========================================================
# 7. MENU PROGRAM
# =========================================================

if __name__ == "__main__":
    print("PERBANDINGAN A*, DIJKSTRA, DAN BFS")
    print("1. Jalan normal")
    print("2. Warung–Perpustakaan ditutup")
    print("3. Perpustakaan–Kampus menjadi 10 km")
    print("4. Kampus tidak terhubung")
    print("5. Awal sama dengan tujuan")

    try:
        pilihan = int(input("\nPilih kasus [1–5]: "))
        if pilihan not in range(1, 6):
            raise ValueError
    except ValueError:
        print("Masukan harus angka 1 sampai 5.")
    else:
        bandingkan(pilihan)