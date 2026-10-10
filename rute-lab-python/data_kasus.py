"""Ubah data eksperimen di sini; hitung ulang dengan memuat ulang halaman."""
from algoritma import NAMA, a_star, dijkstra, bfs, optimum

SKENARIO = [
 ['S1','Jalan normal','Seluruh jalan terbuka. Cari perjalanan dengan jarak paling pendek.'],
 ['S2','Jalan ditutup','Jalan Warung–Perpustakaan ditutup pada kedua arah.'],
 ['S3','Jarak bertambah','Jarak Perpustakaan–Kampus berubah dari 3 menjadi 10 km.'],
 ['S4','Tujuan terputus','Kedua jalan menuju Kampus ditutup. Tidak tersedia rute.'],
 ['S5','Sudah di tujuan','Titik awal dan tujuan sama-sama Kampus.']]
HEURISTIK = [
 ('H0','Tanpa perkiraan',[0,0,0,0,0]),
 ('H1','¼ heuristik dasar',[1.5,1,1,.5,0]),
 ('H2','½ heuristik dasar',[3,2,2,1,0]),
 ('H3','Heuristik dasar',[6,4,4,2,0]),
 ('H4','Biaya sisa tepat',[7,5,5,3,0]),
 ('H5','Tidak konsisten',[7,0,5,3,0]),
 ('H6','Estimasi berlebih',[6,100,4,100,0])]


def konfigurasi(mode, value):
    graf={'R':{'W':2,'T':4},'W':{'R':2,'P':2},'T':{'R':4,'K':5},
          'P':{'W':2,'K':3},'K':{'T':5,'P':3}}
    h=dict(zip(graf, HEURISTIK[3][2]))
    awal,tujuan='R','K'
    def hapus(a,b):
        del graf[a][b]; del graf[b][a]
    if mode=='scenario':
        if value=='S2':hapus('W','P')
        if value=='S3':graf['P']['K']=graf['K']['P']=10
        if value=='S4':hapus('P','K');hapus('T','K')
        if value=='S5':awal='K'
    elif mode=='heuristic':
        h=dict(zip(graf,next(x[2] for x in HEURISTIK if x[0]==value)))
    elif mode=='weight':graf['P']['K']=graf['K']['P']=int(value)
    elif mode=='reopen':
        graf={'S':{'A':3,'B':1},'A':{'S':3,'B':1,'G':2},
              'B':{'S':1,'A':1,'G':100},'G':{'A':2,'B':100}}
        h={'S':4,'A':0,'B':3,'G':0};awal,tujuan='S','G'
    return dict(graph=graf,h=h,start=awal,goal=tujuan)


def semua_hasil():
    hasil={};hs=[];jumlah=0
    for mode,values in [('scenario',[s[0] for s in SKENARIO]),
                        ('heuristic',[h[0] for h in HEURISTIK]),
                        ('weight',list(range(2,11))),('reopen',['R1'])]:
        for value in values:
            c=konfigurasi(mode,str(value));g,h,s,t=c['graph'],c['h'],c['start'],c['goal']
            runs={'A*':a_star(g,h,s,t)}
            if mode in ('scenario','weight'):
                runs.update(Dijkstra=dijkstra(g,s,t),BFS=bfs(g,s,t))
            jumlah+=len(runs)
            hasil[f'{mode}:{value}']=dict(cfg=c,best=optimum(g,s,t),runs=runs)
            if mode=='heuristic':
                exact={n:optimum(g,n,t) for n in g}
                ad=h[t]==0 and all(exact[n] is None or h[n]<=exact[n] for n in g)
                con=h[t]==0 and all(h[u]<=w+h[v] for u in g for v,w in g[u].items())
                src=next(x for x in HEURISTIK if x[0]==value)
                hs.append(dict(id=value,name=src[1],values=src[2],ad=ad,con=con))
    return dict(names=NAMA,algos=['A*','Dijkstra','BFS'],scenarios=SKENARIO,
                hs=hs,experiments=hasil,executions=jumlah,backend='Python / heapq + deque')
