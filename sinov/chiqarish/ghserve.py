# GitHub Pages kabi: har faylga Cache-Control: max-age=600 (+ Last-Modified/304)
import sys, http.server, functools
class H(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'max-age=600'); super().end_headers()
    def log_message(self, *a): pass
port, d = int(sys.argv[1]), sys.argv[2]
http.server.ThreadingHTTPServer(('', port), functools.partial(H, directory=d)).serve_forever()
