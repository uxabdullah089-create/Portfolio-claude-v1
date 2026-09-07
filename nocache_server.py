import sys, os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

class H(SimpleHTTPRequestHandler):
    def send_header(self, key, value):
        # drop validators so the browser can never serve a 304 / memory-cache hit
        if key.lower() in ('last-modified', 'etag'):
            return
        super().send_header(key, value)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def log_message(self, *a):
        pass

port = int(sys.argv[1])
os.chdir(sys.argv[2])
print(f'no-cache server on {port} serving {os.getcwd()}', flush=True)
ThreadingHTTPServer(('127.0.0.1', port), H).serve_forever()
