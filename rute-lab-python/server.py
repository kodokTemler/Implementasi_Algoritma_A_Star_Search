"""Jalankan: py server.py. Server lokal tanpa Flask atau pip install."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
from urllib.parse import urlsplit
from data_kasus import semua_hasil

ROOT=Path(__file__).resolve().parent
class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if urlsplit(self.path).path=='/api/eksperimen':
            try:
                hasil=semua_hasil()
                data=json.dumps(hasil,ensure_ascii=False).encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type','application/json; charset=utf-8')
                self.send_header('Cache-Control','no-store')
                self.send_header('Content-Length',str(len(data)))
                self.end_headers();self.wfile.write(data)
                print(f"Python menghitung {hasil['executions']} eksekusi untuk browser.",flush=True)
            except Exception:
                import traceback
                traceback.print_exc()
                self.send_error(500,'Perhitungan Python gagal; periksa terminal.')
        else:
            super().do_GET()

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=8000)
    args=parser.parse_args()
    handler=partial(Handler,directory=str(ROOT/'static'))
    server=ThreadingHTTPServer(('127.0.0.1',args.port),handler)
    print(f'Buka http://localhost:{args.port}/ — Ctrl+C untuk berhenti.',flush=True)
    try:server.serve_forever()
    except KeyboardInterrupt:pass
    finally:server.server_close()
