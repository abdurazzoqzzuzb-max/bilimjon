"""Bilimjon 0.8.1 — 📡 yuborilmagan natija eslatmasi (u, 10.11: kompyuterda internetsiz o'ynalsa reyting yangilanmaydi — «har 6 soatda chiqsin»).
Ishga tushirish: python3 sinov/v081/sinov_yuborish.py (skrinshot: /tmp/bj081_tasma.png)"""
import os, sys, time, subprocess, json, threading
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.abspath(os.path.join(D, '..', '..')); FAKE = os.path.join(SITE, 'sinov', 'bulut')
PORT = 8814; URL = f'http://localhost:{PORT}/'
srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT)], cwd=SITE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
ERR = []; PE = []
def ok(c, m): print(('✅ ' if c else '❌ ') + m); (None if c else ERR.append(m))
STORE = {}; LOCK = threading.RLock(); ADM = 'U_admintestuz'
def ruxsatli(uid): return uid == ADM or (STORE.get('ruxsat/' + str(uid)) or {}).get('holat') == 'ok'
def ruxsat(op, path, who):
    uid = who.get('uid'); p = path.split('/')
    if uid is None: return False
    if p[0] in ('ruxsat', 'ilova'): return op != 'list' or uid == ADM
    if p[0] == 'oila': return uid == ADM or (len(p) > 1 and uid == p[1] and (op in ('get', 'list') or ruxsatli(uid)))
    return p[0] == 'guruh'
def fs(arg):
    a = json.loads(arg); op = a[0]; who = a[-1] if isinstance(a[-1], dict) else {}; who = who or {}
    with LOCK:
        if not ruxsat(op if op != 'del' else 'del', a[1], who): return json.dumps({'__err': 'permission-denied'})
        if op == 'get': return json.dumps(STORE.get(a[1]))
        if op == 'list': pre = a[1] + '/'; return json.dumps([[k, v] for k, v in STORE.items() if k.startswith(pre) and '/' not in k[len(pre):]])
        if op == 'del': STORE.pop(a[1], None); return 'null'
        if op == 'set':
            path, data, merge = a[1], a[2], a[3]; old = dict(STORE.get(path) or {}) if merge else {}
            for k, v in data.items():
                if isinstance(v, dict) and '__au' in v: cur = list(old.get(k) or []); [cur.append(x) for x in v['__au'] if x not in cur]; old[k] = cur
                else: old[k] = v
            STORE[path] = old; return 'null'
    return 'null'
FILES = {'firebase-app.js': 'export function initializeApp(c){return {c}}', 'firebase-auth.js': open(os.path.join(FAKE, 'auth.js')).read(), 'firebase-firestore.js': open(os.path.join(FAKE, 'fs.js')).read()}
def tel(br, nom, ua=None):
    ctx = br.new_context(viewport={'width': 390, 'height': 844}, service_workers='block', device_scale_factor=2, user_agent=ua); ctx.expose_function('__fs', fs)
    ctx.route('https://www.gstatic.com/firebasejs/**', lambda r: r.fulfill(status=200, content_type='text/javascript', body=FILES[r.request.url.split('/')[-1]]))
    pg = ctx.new_page(); pg.on('pageerror', lambda e: PE.append(f'{nom}: {e}')); return pg
IPH = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1'
AND = 'Mozilla/5.0 (Linux; Android 14; SM-A546E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Mobile Safari/537.36'
def kutf(pg, js, ms=10000):
    try: pg.wait_for_function(js, timeout=ms); return True
    except Exception: return False
Q = '?x=1'
try:
  with sync_playwright() as p:
    br = p.chromium.launch()
    STORE['ruxsat/U_dosttestuz'] = {'email': 'dost@test.uz', 'oila': 'Dost oila', 'ts': 1, 'holat': 'ok'}
    def oila(pg):
        pg.goto(URL + Q); pg.wait_for_timeout(400)
        pg.fill('#on', 'Dost oila'); pg.fill('#p1', '1234'); pg.fill('#p2', '1234'); pg.click('#go'); pg.wait_for_timeout(300)
        return pg.evaluate("(()=>{const A=BJ.A; const b=A.newBola({laqab:'Lola',daraja:'g1',avatar:'🌸',dunyo:'garaj'}); A.S().sozlama.uyqu=''; A.S().joriy=b.id; A.save(true); return b.id})()")
    ESKI = "(h=>{const o=JSON.parse(localStorage.getItem('bj_yub')||'{}'); o.kut=Date.now()-h*3600e3; localStorage.setItem('bj_yub',JSON.stringify(o))})"
    # ---- akkauntsiz oila: eslatma yo'q
    P = tel(br, 'LOKAL', AND); oila(P); P.evaluate("(()=>{BJ.A.bola().yulduz+=3; BJ.A.save(true)})()")
    P.evaluate(ESKI + "(9)"); P.evaluate("location.hash='uy'"); P.wait_for_timeout(500); P.evaluate("BJ.A.ybTekshir()"); P.wait_for_timeout(300)
    h = P.evaluate("BJ.A.yuborHolat()")
    ok(not h['ulangan'] and P.locator('.ybt').count() == 0, f"Akkauntsiz oilada eslatma yo'q ({h})")
    P.context.close()
    # ---- akkauntli qurilma (kompyuter kabi)
    P = tel(br, 'PC'); bid = oila(P)
    P.evaluate("BJ.A.otaOk={rol:'admin',t:Date.now()}"); P.goto(URL + Q + '#ota-bulut'); P.wait_for_timeout(500)
    P.fill('#be', 'dost@test.uz'); P.fill('#bp', 'parol123'); P.click('[data-in]')
    ok(kutf(P, "BJ.A.bulutUlangan() && BJ.A.yuborHolat().ulangan && !BJ.A.yuborHolat().bor", 15000), "Akkaunt ulandi, hammasi yuborilgan (bor=false)")
    P.goto(URL + Q + '#uy'); P.wait_for_timeout(600)
    P.context.set_offline(True); P.wait_for_timeout(200)
    P.evaluate("(()=>{BJ.A.bola().yulduz+=7; BJ.A.save(true)})()"); P.wait_for_timeout(300)
    ok(P.evaluate("BJ.A.yuborHolat().bor"), "Internetsiz o'ynaldi → yuborilmagan natija bor")
    P.evaluate("BJ.A.ybTekshir()"); P.wait_for_timeout(200)
    ok(P.locator('.ybt').count() == 0 and P.evaluate("JSON.parse(localStorage.getItem('bj_yub')).kut > Date.now()-60000"), "Darrov emas — vaqt belgilandi, 6 soat kutiladi")
    P.evaluate(ESKI + "(5.9)"); P.evaluate("BJ.A.ybTekshir()"); P.wait_for_timeout(200)
    ok(P.locator('.ybt').count() == 0, "5.9 soat — hali eslatma yo'q")
    P.evaluate(ESKI + "(7)"); P.evaluate("BJ.A.ybTekshir()"); P.wait_for_timeout(300)
    t = P.inner_text('.ybt') if P.locator('.ybt').count() else ''
    ok('7 soatdan beri yuborilmagan' in t and 'Hozir yuborish' in t, f"6 soatdan keyin — tasma: {t[:70]!r}")
    P.screenshot(path='/tmp/bj081_tasma.png'); ok(P.evaluate("document.documentElement.scrollWidth<=390") if P.viewport_size['width'] == 390 else True, "Gorizontal siljish yo'q")
    P.evaluate("location.hash='mashq'"); P.wait_for_timeout(900)
    ok(P.locator('.ybt').count() == 0, "Mashq paytida tasma yo'q (bolaga xalal bermaydi)")
    P.evaluate("location.hash='uy'"); ok(kutf(P, "!!document.querySelector('.ybt')", 3000), "Uyga qaytganda — yana chiqdi")
    P.click('[data-ybk]'); P.wait_for_timeout(300); P.evaluate("BJ.A.ybTekshir()"); P.wait_for_timeout(200)
    ok(P.locator('.ybt').count() == 0, "«Keyinroq» — yopildi va darrov qaytmaydi")
    P.evaluate("(()=>{const o=JSON.parse(localStorage.getItem('bj_yub')); o.yop=Date.now()-6.1*3600e3; localStorage.setItem('bj_yub',JSON.stringify(o))})()"); P.evaluate("BJ.A.ybTekshir()"); P.wait_for_timeout(300)
    ok(P.locator('.ybt').count() == 1, "«Keyinroq» dan 6 soat o'tgach — yana eslatadi")
    P.click('[data-ybh]'); P.wait_for_timeout(600)
    ok(P.locator('.ybt').count() == 1 and P.evaluate("BJ.A.yuborHolat().bor"), "Internet yo'q — «Hozir yuborish» ogohlantiradi, tasma qoladi")
    P.context.set_offline(False); P.wait_for_timeout(300)
    if P.locator('[data-ybh]').count(): P.click('[data-ybh]')
    ok(kutf(P, "!document.querySelector('.ybt') && !BJ.A.yuborHolat().bor", 25000), "Internet qaytdi → «Hozir yuborish» → yuborildi, tasma yo'qoldi")
    with LOCK: d = STORE.get(f'oila/U_dosttestuz/bolalar/{bid}')
    ok(d and json.loads(d['j']).get('yulduz', 0) >= 7, "Bulutga yangi natija yetib bordi (yulduzlar)")
    ok(P.evaluate("localStorage.getItem('bj_yub')") in ('{}', None), "Eslatma holati tozalandi")
    ok(not PE, f"JS xato yo'q {PE[:3]}")
finally:
  srv.terminate()
print('\nJAMI XATO:', len(ERR)); [print(' -', e) for e in ERR]; sys.exit(1 if ERR else 0)
