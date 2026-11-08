"""Bilimjon 💻 kompyuter yo'riqnomasi uchun HAQIQIY ekranlar (kompyuter oynasi 1100×720; namuna oila, haqiqiy ism yo'q).
Ishlatish: python3 sinov/yoriqnoma/suratlar_pc.py <papka>   → <papka>/pc_*.png
Yo'riqnoma o'zi: python3 sinov/yoriqnoma/yoriqnoma_pc.py <papka> (shu skriptni chaqiradi)."""
import os, sys, time, subprocess, json
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.abspath(os.path.join(D, '..', '..')); FAKE = os.path.join(SITE, 'sinov', 'bulut')
OUT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '/tmp/bj_pc/sur'); os.makedirs(OUT, exist_ok=True)
PORT = 8813; URL = f'http://localhost:{PORT}/'; W, H = 1100, 720
SOAT = '2026-11-12T16:40:00'
srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT)], cwd=SITE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
PE = []
STORE = {}
def fs(arg):   # soxta Firebase — faqat kirish ekrani uchun
    a = json.loads(arg)
    if a[0] == 'get': return json.dumps(STORE.get(a[1]))
    if a[0] == 'list': return '[]'
    return 'null'
FILES = {'firebase-app.js': 'export function initializeApp(c){return {c}}', 'firebase-auth.js': open(os.path.join(FAKE, 'auth.js')).read(), 'firebase-firestore.js': open(os.path.join(FAKE, 'fs.js')).read()}
YASHIR = "document.querySelectorAll('.toast,.toasts').forEach(e=>e.remove())"
def sur(pg, nom, ms=400):
    pg.wait_for_timeout(ms); pg.evaluate(YASHIR); pg.screenshot(path=os.path.join(OUT, nom + '.png')); print('📸', nom)
NAMUNA = """(()=>{const A=BJ.A, s=A.S(); s.sozlama.uyqu=''; const D=A.weekDays(A.isoWeek());
  const yasa=(o, kunlar, yul)=>{ const b=A.newBola(o); b.yaratildi=D[0]; b.boshlandi=D[0];
    kunlar.forEach(k=>{ b.kun[k]=Object.assign(A.agg(b,k),{faol:1500,n:24,ok1:20,missiya:1,yulduz:yul}); }); b.yulduz=yul*kunlar.length; return b; };
  const a=yasa({laqab:'Aziz',daraja:'g1',avatar:'🐯',dunyo:'garaj'}, D.slice(0,3), 14), l=yasa({laqab:'Lola',daraja:'g0',avatar:'🦋',dunyo:'orol'}, D.slice(0,2), 11);
  a.detal=['gildirak','spoyler','nitro']; s.joriy=a.id; A.save(true); return [a.id,l.id]})()"""
try:
  with sync_playwright() as p:
    br = p.chromium.launch()
    def kontekst(bulut=False):
        c = br.new_context(viewport={'width': W, 'height': H}, device_scale_factor=1.5, service_workers='block')
        if bulut:
            c.expose_function('__fs', fs)
            c.route('https://www.gstatic.com/firebasejs/**', lambda r: r.fulfill(status=200, content_type='text/javascript', body=FILES[r.request.url.split('/')[-1]]))
        c.route('https://fonts.googleapis.com/**', lambda r: r.fulfill(status=200, content_type='text/css', body=''))
        c.route('https://fonts.gstatic.com/**', lambda r: r.abort())
        c.route('**/version.json*', lambda r: r.fulfill(status=200, content_type='application/json', body='{"ver":"0.0.1"}'))
        pg = c.new_page(); pg.clock.set_fixed_time(SOAT); pg.on('pageerror', lambda e: PE.append(str(e))); return pg
    # 1) kirish ekrani (yangi kompyuter — 🔒 eshik)
    pg = kontekst(True); ev = pg.evaluate
    pg.goto(URL + '?eshik=1'); pg.wait_for_timeout(900)
    pg.click('.tndots button[data-d="4"]'); pg.wait_for_timeout(700); pg.click('[data-nx]'); pg.wait_for_timeout(900)
    pg.fill('#be', 'namuna.oila@gmail.com'); pg.fill('#bp', 'parol123'); sur(pg, 'pc_kirish')
    pg.context.close()
    # 2) bola ekranlari
    pg = kontekst(); ev = pg.evaluate; NV = [0]
    def NAV(h, q='', ms=700): NV[0] += 1; pg.goto(URL + f'?tez=1{q}&r={NV[0]}#' + h); ev('BJ.A.render()'); pg.wait_for_timeout(ms)
    pg.goto(URL + '?tez=1'); pg.wait_for_timeout(600)
    pg.fill('#on', 'Namuna oila'); pg.fill('#p1', '1234'); pg.fill('#p2', '1234'); pg.click('#go'); pg.wait_for_timeout(500)
    AZ, LO = ev(NAMUNA)
    NAV('tanla'); sur(pg, 'pc_tanla')
    NAV('uy', ms=900); sur(pg, 'pc_uy')
    NAV('missiya', ms=900)
    for _ in range(40):
        if ev("!!(window.__bjCur && __bjCur() && __bjCur().it && document.querySelector('#body .opt') && !__bjCur().it.matn && String(__bjCur().it.sav).length < 40)"): break
        b = pg.locator('#app .btn.big, #app [data-next], #app [data-go-on]')
        if b.count(): b.first.click(); pg.wait_for_timeout(500)
        elif ev("!!(window.__bjCur && __bjCur() && __bjCur().cb)"): ev("window.__bjJavob(true)"); pg.wait_for_timeout(500)
        else: pg.wait_for_timeout(300)
    sur(pg, 'pc_savol', ms=900)
    # 📱 bitta bola — bitta qurilma: kompyuterda boshqa qurilmaniki
    ev(f"(()=>{{const b=BJ.A.S().bolalar['{AZ}']; b.qurilma={{id:'q_tel', nom:'Dadamning telefoni', ts:Date.now()-3600e3}}; BJ.A.save(true)}})()")
    NV[0] += 1; pg.goto(URL + f'?tez=1&qulf=1&r={NV[0]}#missiya'); ev('BJ.A.bulutUlangan=()=>true; BJ.A.render()'); sur(pg, 'pc_qurq', ms=900)   # qulf faqat akkauntli oilada — suratda soxta
    # ota-ona paneli
    NAV('uy'); ev("BJ.A.otaOk={rol:'admin',t:Date.now()}"); ev("location.hash='ota'"); sur(pg, 'pc_ota', ms=700)
    pg.context.close()
finally:
  srv.terminate()
print('JS xato:', PE[:5] if PE else "yo'q")
