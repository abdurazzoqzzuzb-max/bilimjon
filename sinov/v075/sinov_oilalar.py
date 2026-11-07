"""Bilimjon 0.7.5 — 👨‍👩‍👧 «Hamma oilalar» (admin nazorati): firestore.rules 0.7.5 (admin oila/** ni o'qiydi va yozadi) Python nusxasi,
soxta Firebase, 4 telefon. Admin: oilalar ro'yxati (nom, email, versiya, ruxsat), 👁 bolalari (bu hafta), ✉️ parol tiklash xati,
🔁 ma'lumotni yangi akkauntga ko'chirish (eski telefon yo'qolgan holat) → yangi telefonga o'zi keladi. Oddiy oila boshqa oilani o'qiy olmaydi.
Ishga tushirish: python3 sinov/v075/sinov_oilalar.py"""
import os, sys, time, subprocess, json, threading
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.abspath(os.path.join(D, '..', '..')); FAKE = os.path.join(SITE, 'sinov', 'bulut')
PORT = 8797; URL = f'http://localhost:{PORT}/'
srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT)], cwd=SITE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
ERR = []; PE = []
def ok(c, m): print(('✅ ' if c else '❌ ') + m); (None if c else ERR.append(m))
STORE = {}; LOCK = threading.RLock(); RULES = {'on': True, 'admin': 'U_admintestuz'}; WRITES = []
def ruxsatli(uid): return uid == RULES['admin'] or (STORE.get('ruxsat/' + str(uid)) or {}).get('holat') == 'ok'
def sorov_togri(d, who):
    return set(d) <= {'email', 'oila', 'ts', 'holat'} and d.get('holat') == 'kutish' and d.get('email') == who.get('email') \
        and isinstance(d.get('oila'), str) and len(d['oila']) <= 24 and isinstance(d.get('ts'), int) and not isinstance(d.get('ts'), bool)
def ruxsat(op, path, who, new=None):   # firestore.rules 0.7.5 mantig'i
    uid = who.get('uid'); p = path.split('/'); adm = uid is not None and uid == RULES['admin']
    if p[0] == 'ruxsat':
        if uid is None: return False
        if op == 'list': return adm
        if op == 'get': return uid == p[1] or adm
        if op == 'del': return adm
        if adm: return True
        old = STORE.get(path)
        return uid == p[1] and (old is None or old.get('holat') == 'kutish') and sorov_togri(new, who)
    if p[0] == 'oila':
        if uid is None: return False
        if adm: return True
        if len(p) < 2 or uid != p[1]: return False
        return op in ('get', 'list') or ruxsatli(uid)
    if p[0] == 'guruh': return op in ('get', 'list', 'del') or uid is not None and ruxsatli(uid)
    return False
def fs(arg):
    a = json.loads(arg); op = a[0]; who = a[-1] if isinstance(a[-1], dict) else {}; who = who or {}
    with LOCK:
        if op == 'get':
            if not ruxsat('get', a[1], who): return json.dumps({'__err': 'permission-denied'})
            return json.dumps(STORE.get(a[1]))
        if op == 'list':
            if not ruxsat('list', a[1], who): return json.dumps({'__err': 'permission-denied'})
            pre = a[1] + '/'; return json.dumps([[k, v] for k, v in STORE.items() if k.startswith(pre) and '/' not in k[len(pre):]])
        if op == 'del':
            if not ruxsat('del', a[1], who): return json.dumps({'__err': 'permission-denied'})
            STORE.pop(a[1], None); return 'null'
        if op == 'set':
            path, data, merge = a[1], a[2], a[3]; old = dict(STORE.get(path) or {}) if merge else {}
            for k, v in data.items():
                if isinstance(v, dict) and '__au' in v: cur = list(old.get(k) or []); [cur.append(x) for x in v['__au'] if x not in cur]; old[k] = cur
                else: old[k] = v
            if not ruxsat('set', path, who, old): return json.dumps({'__err': 'permission-denied'})
            STORE[path] = old; WRITES.append(('set', path, who.get('uid'))); return 'null'
    return 'null'
FILES = {'firebase-app.js': 'export function initializeApp(c){return {c}}', 'firebase-auth.js': open(os.path.join(FAKE, 'auth.js')).read(), 'firebase-firestore.js': open(os.path.join(FAKE, 'fs.js')).read()}
def tel(br, nom):
    ctx = br.new_context(viewport={'width': 390, 'height': 844}, service_workers='block'); ctx.expose_function('__fs', fs)
    ctx.route('https://www.gstatic.com/firebasejs/**', lambda r: r.fulfill(status=200, content_type='text/javascript', body=FILES[r.request.url.split('/')[-1]]))
    pg = ctx.new_page(); pg.on('pageerror', lambda e: PE.append(f'{nom} pageerror: {e}')); pg.goto(URL); pg.wait_for_timeout(400); return pg
def oila(pg, nom): pg.fill('#on', nom); pg.fill('#p1', '1234'); pg.fill('#p2', '1234'); pg.click('#go'); pg.wait_for_timeout(300)
def kut(pg, js, ms=8000):
    try: pg.wait_for_function(js, timeout=ms); return True
    except Exception: return False
PUMP = [None]
def pump(ms): PUMP[0].wait_for_timeout(ms)
def kutpy(f, ms=10000):
    t = time.time()
    while time.time() - t < ms / 1000:
        with LOCK:
            if f(): return True
        pump(200)
    with LOCK: return bool(f())
TXT = lambda pg: pg.evaluate("document.body.innerText")
BOLA = """(()=>{const A=BJ.A; const b=A.newBola({laqab:'%s',daraja:'g1',avatar:'%s',dunyo:'orol'}); const k=A.todayKey(); b.kun[k]=Object.assign(A.agg(b,k),{faol:1500,n:20,ok1:17,missiya:1}); A.pushLog(b.id,{t:'ans',ts:Date.now(),bola:b.id,tugun:'M1.1',togri_1:1}); A.flushLog(); A.save(true); return b.id})()"""
def ota(pg, h='#ota-bulut'): pg.evaluate("BJ.A.otaOk={rol:'admin',t:Date.now()}"); pg.goto(URL + h); pg.wait_for_timeout(500)
try:
  with sync_playwright() as p:
    br = p.chromium.launch()
    # --- admin
    AD = tel(br, 'ADMIN'); oila(AD, 'Admin oila'); PUMP[0] = AD; AD.evaluate(BOLA % ('Ali', '🦊'))
    ota(AD); AD.fill('#be', 'admin@test.uz'); AD.fill('#bp', 'parol123'); AD.click('[data-in]')
    ok(kut(AD, "document.body.innerText.includes('siz — admin')"), "admin — «🛡️ Ruxsatlar · siz — admin»")
    AD.click('[data-rxtel]'); AD.wait_for_timeout(200); AD.click('.scrim [data-ok]'); AD.wait_for_timeout(300)
    ok(kutpy(lambda: (STORE.get('oila/U_admintestuz') or {}).get('e') == 'admin@test.uz'), "oila hujjatida email (e) — admin kimligini taniydi")
    # --- Javlon (eski telefon): so'rov → ruxsat → bulut
    JV = tel(br, 'JAVLON'); oila(JV, 'Javlon oila'); jbid = JV.evaluate(BOLA % ('Sabo', '🌸'))
    ota(JV); JV.fill('#be', 'javlon@test.uz'); JV.fill('#bp', 'parol123'); JV.click('[data-up]')
    ok(kut(JV, "document.body.innerText.includes('Ruxsat kerak')"), "Javlon — «🛡️ Ruxsat kerak»")
    ok("admin) oilangiz bulutdagi natijalarini ko'ra oladi" in TXT(JV), "so'rov ekranida ochiq aytiladi: admin natijalarni ko'ra oladi va yordam beradi")
    JV.click('[data-rxq]'); ok(kutpy(lambda: (STORE.get('ruxsat/U_javlontestuz') or {}).get('holat') == 'kutish'), "so'rov yuborildi")
    ok(kut(AD, "!!document.querySelector('[data-rxa=\"ok|U_javlontestuz\"]')", 8000), "admin ro'yxatida so'rov"); AD.click('[data-rxa="ok|U_javlontestuz"]')
    ok(kutpy(lambda: f'oila/U_javlontestuz/bolalar/{jbid}' in STORE and any(k.startswith('oila/U_javlontestuz/log/') for k in STORE), 12000), "ruxsatdan keyin Javlon oilasi bulutda (bola + log)")
    # --- oddiy oila boshqani o'qiy olmaydi
    r = JV.evaluate("""(async()=>{const m=await import('https://www.gstatic.com/firebasejs/13.2.0/firebase-firestore.js'); const o=[];
      try{ await m.getDocs(m.collection({},'oila')); o.push('royxat'); }catch(e){ o.push(e.code||String(e)); }
      try{ await m.getDoc(m.doc({},'oila','U_admintestuz')); o.push('oqidi'); }catch(e){ o.push(e.code||String(e)); }
      try{ await m.setDoc(m.doc({},'oila','U_admintestuz'),{j:'{}'}); o.push('yozdi'); }catch(e){ o.push(e.code||String(e)); } return o; })()""")
    ok(r == ['permission-denied'] * 3, f"oddiy oila: boshqa oilalar ro'yxati / o'qish / yozish — rad {r}")
    # --- admin: hamma oilalar
    ota(AD); ok(kut(AD, "!!document.querySelector('[data-oil]')"), "admin kartasida «👨‍👩‍👧 Oilalarni ko'rish»")
    AD.click('[data-oil]'); ok(kut(AD, "document.body.innerText.includes('Javlon oila') && document.body.innerText.includes('javlon@test.uz')", 8000), "ro'yxatda Javlon oilasi: nomi va emaili")
    t = TXT(AD); ok('👑 Admin oila' in t and '✅ ruxsat' in t and ' · v0.7' in t, "admin oilasi 👑 tepada; ruxsat holati va versiya ko'rinadi")
    AD.click('[data-oilb="U_javlontestuz"]'); ok(kut(AD, "document.body.innerText.includes('Sabo')", 8000), "👁 Bolalari — Sabo")
    t = TXT(AD); ok("Bu hafta: 1 kun · 25 daq · 🎯 1 missiya · 85% to'g'ri (20 javob)" in t, "bola qisqa natijasi: kun, daqiqa, missiya, aniqlik")
    ok(AD.evaluate("document.documentElement.scrollWidth") <= 390, "390 px — gorizontal sirpanish yo'q")
    AD.screenshot(path='/tmp/bj075_oilalar.png', full_page=True)
    AD.click('[data-oilr="U_javlontestuz"]'); AD.wait_for_timeout(200)
    ok('javlon@test.uz' in AD.locator('.scrim').inner_text() and '1 soat' in AD.locator('.scrim').inner_text(), "✉️ parol tiklash varag'i: email va «1 soat»")
    AD.click('.scrim [data-ok]'); ok(kut(AD, "document.body.innerText.includes('Xat yuborildi: javlon@test.uz')", 4000), "✉️ xat yuborildi (toast)")
    # --- Javlon telefoni yo'qoldi: yangi telefon, yangi akkaunt (bo'sh) → admin ko'chiradi
    JN = tel(br, 'JAVLON_YANGI'); JN.goto(URL + '#bulut'); JN.wait_for_timeout(500)
    JN.fill('#be', 'javlon2@test.uz'); JN.fill('#bp', 'parol123'); JN.click('[data-up]')
    ok(kut(JN, "document.body.innerText.includes('Ruxsat kerak')"), "yangi akkaunt — «Ruxsat kerak»")
    JN.fill('#rxn', 'Javlon yangi'); JN.click('[data-rxq]'); ok(kutpy(lambda: 'ruxsat/U_javlon2testuz' in STORE), "yangi akkaunt so'rovi")
    ok(kut(AD, "!!document.querySelector('[data-rxa=\"ok|U_javlon2testuz\"]')", 8000), "admin ko'radi"); AD.click('[data-rxa="ok|U_javlon2testuz"]')
    ok(kutpy(lambda: (STORE.get('ruxsat/U_javlon2testuz') or {}).get('holat') == 'ok'), "yangi akkauntga ruxsat")
    ota(AD); AD.click('[data-oil]'); kut(AD, "!!document.querySelector('[data-oilk=\"U_javlontestuz\"]')", 6000)
    AD.click('[data-oilk="U_javlontestuz"]'); AD.wait_for_timeout(200)
    opts = AD.evaluate("[...document.querySelectorAll('#oilq option')].map(o=>o.value)")
    ok('U_javlon2testuz' in opts and 'U_admintestuz' not in opts and 'U_javlontestuz' not in opts, f"🔁 nishon ro'yxati: o'zi va admin yo'q {opts}")
    AD.select_option('#oilq', 'U_javlon2testuz'); AD.click('.scrim [data-ok]')
    ok(kut(AD, "document.body.innerText.includes(\"Ko'chirildi: 1 bola, 1 kunlik log\")", 10000), "admin: «🔁 Ko'chirildi: 1 bola, 1 kunlik log ✓»")
    ok(kutpy(lambda: f'oila/U_javlon2testuz/bolalar/{jbid}' in STORE and any(k.startswith('oila/U_javlon2testuz/log/') for k in STORE), 12000), "🔁 ko'chirildi: oila + bola + log yangi akkauntda")
    with LOCK: ok(STORE['oila/U_javlontestuz'].get('j') and f'oila/U_javlontestuz/bolalar/{jbid}' in STORE, "eski akkauntdagi nusxa o'zgarmadi")
    JN.reload(); JN.wait_for_timeout(500)
    ok(kut(JN, "(BJ.A.bolalar()||[]).some(b=>b.laqab==='Sabo')", 15000), "yangi telefon: Sabo va natijalari o'zi keldi")
    ok(JN.evaluate("(()=>{const b=BJ.A.bolalar().find(b=>b.laqab==='Sabo'); return b && b.kun[BJ.A.todayKey()].n})()") == 20, "bolaning bugungi natijasi ham ko'chdi (20 javob)")
    # --- admin 2-telefoni: ko'radi, lekin ✉️/🔁 o'chiq
    A2 = tel(br, 'ADMIN2'); A2.goto(URL + '#bulut'); A2.wait_for_timeout(500)
    A2.fill('#be', 'admin@test.uz'); A2.fill('#bp', 'parol123'); A2.click('[data-in]'); kut(A2, "BJ.A.S().oila && BJ.A.S().adminTel", 10000)
    ota(A2); kut(A2, "!!document.querySelector('[data-oil]')", 6000); A2.click('[data-oil]'); kut(A2, "!!document.querySelector('[data-oilk=\"U_javlontestuz\"]')", 8000)
    ok(not A2.locator('[data-oilk="U_javlontestuz"]').is_enabled() and not A2.locator('[data-oilr="U_javlontestuz"]').is_enabled() and A2.locator('[data-oilb="U_javlontestuz"]').is_enabled(),
       "admin 2-telefoni: 👁 ko'rish bor, ✉️ va 🔁 faqat admin telefonida")
    ok(not PE, f"JS xato yo'q {PE[:3]}")
    br.close()
finally:
    srv.terminate()
print(f"\n{'HAMMASI OK' if not ERR else str(len(ERR)) + ' ta xato'}")
for e in ERR: print('  -', e)
sys.exit(1 if ERR else 0)
