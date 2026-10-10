"""Jalankan: py uji_backend.py. Memeriksa hasil terhadap acuan independen."""
from data_kasus import semua_hasil

def main():
    data=semua_hasil();jumlah=0
    expected=[(7,3),(7,4),(9,4)]
    for key,entry in data['experiments'].items():
        cfg=entry['cfg'];g=cfg['graph']
        for algo,r in entry['runs'].items():
            jumlah+=1
            if r['path'] is not None:
                assert r['path'][0]==cfg['start'] and r['path'][-1]==cfg['goal']
                assert sum(g[a][b] for a,b in zip(r['path'],r['path'][1:]))==r['cost']
            else:assert entry['best'] is None
            if algo!='BFS' and key!='heuristic:H6':assert r['cost']==entry['best']
            assert len([f for f in r['frames'] if f['type']=='expand'])==len(r['expanded'])
    for algo,(cost,exp) in zip(data['algos'],expected):
        r=data['experiments']['scenario:S1']['runs'][algo]
        assert (r['cost'],len(r['expanded']))==(cost,exp)
    r=data['experiments']['heuristic:H6']['runs']['A*']
    assert (r['cost'],len(r['expanded']))==(9,2)
    r=data['experiments']['reopen:R1']['runs']['A*']
    assert r['expanded']==['S','A','B','A'] and r['cost']==4
    assert jumlah==50
    print('LULUS: 50 eksekusi Python, biaya, keabsahan rute, dan jumlah ekspansi.')

if __name__=='__main__':main()
