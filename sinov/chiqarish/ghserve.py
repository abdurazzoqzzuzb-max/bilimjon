# GitHub Pages kabi: har faylga Cache-Control: max-age=600 (+ Last-Modified/304)
import sys, http.server, functools
class H(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'max-age=600'); super().end_headers()
    def log_message(self, *a): pass
    def do_GET(self):
        # GitHub Pages ETag (mazmun) bo'yicha tekshiradi; bu yerda fayl vaqti (mtime) eski papkada yangiroq bo'lib qolishi mumkin —
        # noto'g'ri «304» bermaslik uchun shartli so'rov e'tiborga olinmaydi (har doim 200, mazmun o'zgargani kabi)
        if 'If-Modified-Since' in self.headers: del self.headers['If-Modified-Since']
        return super().do_GET()
port, d = int(sys.argv[1]), sys.argv[2]
http.server.ThreadingHTTPServer(('', port), functools.partial(H, directory=d)).serve_forever()
