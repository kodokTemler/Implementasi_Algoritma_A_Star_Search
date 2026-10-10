"""Algoritma yang benar-benar dipanggil web. Hanya pustaka standar Python."""
import heapq
from collections import deque
from copy import deepcopy

NAMA = {'R':'Rumah','W':'Warung','T':'Taman','P':'Perpustakaan','K':'Kampus',
        'S':'S','A':'A','B':'B','G':'G'}


def a_star(graf, heuristik, awal, tujuan):
    """A* heapq dengan jejak untuk animasi; prioritas (f, g, nama pada jalur)."""
    antrean = []
    biaya_terbaik = {awal: 0}
    ekspansi, langkah = [], []

    def masukkan(jalur, g):
        # Nama lengkap mempertahankan tie-break kode Python pada laporan.
        heapq.heappush(antrean, (g + heuristik[jalur[-1]], g,
                                [NAMA[n] for n in jalur], jalur))

    def catat(simpul, jenis, entri=None, perubahan=None):
        kandidat = [dict(f=f, g=g, path=list(p)) for f,g,_,p in sorted(antrean)]
        langkah.append(dict(node=simpul, type=jenis, entry=entri,
                            updates=perubahan or [], queue=kandidat,
                            best=dict(biaya_terbaik), expanded=list(ekspansi)))

    masukkan([awal], 0)
    catat(None, 'init')
    while antrean:
        f, jarak, _, jalur = heapq.heappop(antrean)
        sekarang = jalur[-1]
        entri = dict(f=f, g=jarak, path=jalur)
        if jarak != biaya_terbaik[sekarang]:
            catat(sekarang, 'stale', entri)
            continue
        if sekarang == tujuan:
            catat(sekarang, 'goal', entri)
            return dict(path=jalur, cost=jarak, expanded=ekspansi, frames=langkah)
        ekspansi.append(sekarang)
        perubahan = []
        for tetangga, bobot in graf[sekarang].items():
            g_baru = jarak + bobot
            if g_baru < biaya_terbaik.get(tetangga, float('inf')):
                lama = biaya_terbaik.get(tetangga)
                biaya_terbaik[tetangga] = g_baru
                masukkan(jalur + [tetangga], g_baru)
                perubahan.append(dict(node=tetangga, g=g_baru, h=heuristik[tetangga],
                                      f=g_baru+heuristik[tetangga], old=lama))
        catat(sekarang, 'expand', entri, perubahan)
    catat(None, 'empty')
    return dict(path=None, cost=None, expanded=ekspansi, frames=langkah)


def dijkstra(graf, awal, tujuan):
    """Dijkstra memakai A* dengan seluruh h = 0."""
    return a_star(graf, {n:0 for n in graf}, awal, tujuan)


def bfs(graf, awal, tujuan):
    """BFS FIFO meminimalkan jumlah ruas, bukan kilometer."""
    antrean = deque([dict(f=0, g=0, path=[awal])])
    ditemukan = {awal}
    biaya = {awal:0}
    ekspansi, langkah = [], []
    def catat(n, jenis, entri=None, perubahan=None):
        langkah.append(dict(node=n, type=jenis, entry=deepcopy(entri),
                            updates=deepcopy(perubahan or []), queue=deepcopy(list(antrean)),
                            best=dict(biaya), expanded=list(ekspansi)))
    catat(None, 'init')
    while antrean:
        entri = antrean.popleft()
        jalur, jarak = entri['path'], entri['g']
        sekarang = jalur[-1]
        if sekarang == tujuan:
            catat(sekarang, 'goal', entri)
            return dict(path=jalur, cost=jarak, expanded=ekspansi, frames=langkah)
        ekspansi.append(sekarang)
        perubahan = []
        for tetangga, bobot in graf[sekarang].items():
            if tetangga not in ditemukan:
                ditemukan.add(tetangga)
                g = jarak + bobot
                biaya[tetangga] = g
                antrean.append(dict(f=g, g=g, path=jalur+[tetangga]))
                perubahan.append(dict(node=tetangga, g=g, h=0, f=g, old=None))
        catat(sekarang, 'expand', entri, perubahan)
    catat(None, 'empty')
    return dict(path=None, cost=None, expanded=ekspansi, frames=langkah)


def optimum(graf, awal, tujuan):
    """Acuan independen untuk graf kecil: seluruh jalur sederhana."""
    biaya = []
    def telusuri(jalur, total):
        u = jalur[-1]
        if u == tujuan:
            biaya.append(total)
            return
        for v,w in graf[u].items():
            if v not in jalur:
                telusuri(jalur+[v], total+w)
    telusuri([awal], 0)
    return min(biaya) if biaya else None
