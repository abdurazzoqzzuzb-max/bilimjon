"""Bilimjon 0.8.0 — 📱 bitta bola — bitta qurilma (u, 08.11: «dadasi, oyisi, kompyuter bitta akkauntda — bitta bola bitta profildan o'ynasin»).
Ikki telefon (soxta Firebase, bitta oila akkaunti, ?qulf=1): A telefonda bola missiyani boshlaydi → bola A niki (b.qurilma, bulutga sinxron) →
B telefonda faoliyat yopiq («boshqa qurilmada o'ynaydi»), uy ochiq, ota-ona paneli ochiq → B da PIN bilan o'tkazish → endi A da yopiq.
Akkauntsiz oilada va ?qulf siz localhost da qulf yo'q. ⚙️ qurilma nomi. Maxfiylik gapi (ruxsat kartasi, tanishtiruv). 390 px.
Ishga tushirish: python3 sinov/v080/sinov_qurilma.py  (skrinshotlar: /tmp/bj080_*.png)"""
import os, sys, time, subprocess, json, threading
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.abspath(os.path.join(D, '..', '..')); FAKE = os.path.join(SITE, 'sinov', 'bulut')
PORT = 8811; URL = f'http://localhost:{PORT}/'
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
Q = '?qulf=1'
try:
  with sync_playwright() as p:
    br = p.chromium.launch()
    STORE['ruxsat/U_dosttestuz'] = {'email': 'dost@test.uz', 'oila': 'Dost oila', 'ts': 1, 'holat': 'ok'}
    # ---- akkauntsiz oila: qulf yo'q
    L0 = tel(br, 'LOKAL', IPH); L0.goto(URL + Q); L0.wait_for_timeout(400)
    L0.fill('#on', 'Lokal'); L0.fill('#p1', '1234'); L0.fill('#p2', '1234'); L0.click('#go'); L0.wait_for_timeout(300)
    L0.evaluate("(()=>{const A=BJ.A; const b=A.newBola({laqab:'Ali',daraja:'g1',avatar:'🦊',dunyo:'garaj'}); A.S().sozlama.uyqu=''; A.S().joriy=b.id; A.save(true)})()")
    L0.goto(URL + Q + '#mashq'); L0.wait_for_timeout(500)
    ok(L0.locator('.qurq').count() == 0 and L0.evaluate("!BJ.A.bola().qurilma"), "Akkauntsiz oilada qulf yo'q (bola qurilmaga bog'lanmaydi)")
    L0.context.close()
    # ---- A telefon (iPhone): oila + bola + akkaunt
    PA = tel(br, 'A', IPH); PA.goto(URL + Q); PA.wait_for_timeout(400)
    PA.fill('#on', 'Dost oila'); PA.fill('#p1', '1234'); PA.fill('#p2', '1234'); PA.click('#go'); PA.wait_for_timeout(300)
    bid = PA.evaluate("(()=>{const A=BJ.A; const b=A.newBola({laqab:'Lola',daraja:'g1',avatar:'🌸',dunyo:'garaj'}); A.S().sozlama.uyqu=''; A.S().joriy=b.id; A.save(true); return b.id})()")
    PA.evaluate("BJ.A.otaOk={rol:'admin',t:Date.now()}"); PA.goto(URL + Q + '#ota-bulut'); PA.wait_for_timeout(500)
    PA.fill('#be', 'dost@test.uz'); PA.fill('#bp', 'parol123'); PA.click('[data-in]')
    ok(kutf(PA, "BJ.A.bulutUlangan && BJ.A.bulutUlangan()", 10000), "A telefon: akkaunt ulandi")
    PA.goto(URL + Q + '#mashq'); PA.wait_for_timeout(700)
    q = PA.evaluate("BJ.A.bola().qurilma")
    ok(q and q.get('nom') == 'iPhone' and PA.locator('.qurq').count() == 0, f"A: bola birinchi faoliyatda shu qurilmaga bog'landi (nom: iPhone) {q}")
    t0 = time.time(); ok_sync = False
    while time.time() - t0 < 12:
        with LOCK:
            d = STORE.get(f'oila/U_dosttestuz/bolalar/{bid}')
            if d and (json.loads(d['j']).get('qurilma') or {}).get('id') == q['id']: ok_sync = True; break
        PA.wait_for_timeout(300)
    ok(ok_sync, "b.qurilma bulutga yozildi (bola hujjati)")
    # ---- B telefon (Android): xuddi shu akkaunt bilan kirish
    PB = tel(br, 'B', AND); PB.goto(URL + Q + '#bulut'); PB.wait_for_timeout(600)
    if PB.locator('#be').count() == 0:
        PB.goto(URL + Q); PB.wait_for_timeout(400)
        if PB.locator('#bk').count(): PB.click('#bk'); PB.wait_for_timeout(500)
    PB.fill('#be', 'dost@test.uz'); PB.fill('#bp', 'parol123'); PB.click('[data-in]')
    ok(kutf(PB, f"BJ.A.S().bolalar && BJ.A.S().bolalar['{bid}'] && BJ.A.S().bolalar['{bid}'].qurilma", 15000), "B telefon: bola va uning qurilmasi bulutdan keldi")
    PB.evaluate(f"(()=>{{const s=BJ.A.S(); s.joriy='{bid}'; BJ.A.save(true)}})()")
    PB.goto(URL + Q + '#uy'); PB.wait_for_timeout(600)
    ok(PB.locator('.qurq').count() == 0, "B: bola uyi ochiq (faqat ko'rish)")
    for h in ('mashq', 'missiya', 'zal', 'dokon'):
        PB.goto(URL + Q + '#' + h); PB.wait_for_timeout(450)
        ok(PB.locator('.qurq').count() == 1, f"B: #{h} — «boshqa qurilmada o'ynaydi» ekrani")
    t = PB.inner_text('.qurq')
    ok('Lola boshqa qurilmada' in t and 'iPhone' in t and 'Android telefon' in t, "Ekranda: bola, uning qurilmasi (iPhone) va bu qurilma (Android telefon)")
    PB.screenshot(path='/tmp/bj080_qulf.png')
    ok(PB.evaluate("document.documentElement.scrollWidth<=390"), "390 px — gorizontal siljish yo'q")
    PB.evaluate("BJ.A.otaOk={rol:'admin',t:Date.now()}"); PB.goto(URL + Q + '#ota'); PB.wait_for_timeout(500)
    ok(PB.locator('.qurq').count() == 0 and PB.locator('[data-go="ota-sozlama"]').count() == 1, "B: ota-ona paneli ochiq")
    # noto'g'ri PIN, keyin to'g'ri — o'tkazish
    PB.goto(URL + Q + '#mashq'); PB.wait_for_timeout(450); PB.click('[data-qo]'); PB.wait_for_timeout(250)
    PB.fill('#qp', '9999'); PB.click('.sheet [data-ok]'); PB.wait_for_timeout(250)
    ok(PB.locator('.sheet').count() == 1 and PB.evaluate(f"BJ.A.S().bolalar['{bid}'].qurilma.nom") == 'iPhone', "Noto'g'ri PIN — o'tkazilmadi")
    PB.fill('#qp', '1234'); PB.click('.sheet [data-ok]'); PB.wait_for_timeout(600)
    ok(PB.locator('.qurq').count() == 0 and PB.evaluate(f"BJ.A.S().bolalar['{bid}'].qurilma.nom") == 'Android telefon', "To'g'ri PIN — bola endi B da o'ynaydi, mashq ochildi")
    ok(kutf(PA, f"BJ.A.S().bolalar['{bid}'].qurilma.nom==='Android telefon'", 15000), "A telefonga o'tkazish sinxron bilan yetdi")
    PA.goto(URL + Q + '#missiya'); PA.wait_for_timeout(500)
    ok(PA.locator('.qurq').count() == 1, "A: endi faoliyat yopiq (bola B da)")
    # ⚙️ qurilma nomi
    PB.evaluate("BJ.A.otaOk={rol:'admin',t:Date.now()}"); PB.goto(URL + Q + '#ota-sozlama'); PB.wait_for_timeout(500)
    ok('Bitta bola — bitta qurilma' in PB.inner_text('body') and 'shu qurilma' in PB.inner_text('body'), "⚙️ Sozlamalar: «Bitta bola — bitta qurilma» kartasi, Lola — shu qurilma")
    PB.fill('#qnm', 'Oyimning telefoni'); PB.click('[data-save]'); PB.wait_for_timeout(500)
    ok(PB.evaluate(f"BJ.A.S().qurilma.nom==='Oyimning telefoni' && BJ.A.S().bolalar['{bid}'].qurilma.nom==='Oyimning telefoni'"), "Qurilma nomi saqlandi va bolaning qurilma nomi yangilandi")
    ok(kutf(PA, f"BJ.A.S().bolalar['{bid}'].qurilma.nom==='Oyimning telefoni'", 15000), "A telefonda ham yangi nom («Oyimning telefoni»)")
    PA.goto(URL + Q + '#mashq'); PA.wait_for_timeout(500); ok('Oyimning telefoni' in PA.inner_text('.qurq'), "A ekranida: «Oyimning telefoni»")
    # ?qulf siz localhost — o'chiq
    PA.goto(URL + '#mashq'); PA.wait_for_timeout(500); ok(PA.locator('.qurq').count() == 0, "localhost'da ?qulf=1 siz qulf o'chiq (eski sinovlar buzilmaydi)")
    # maxfiylik gapi
    src = open(os.path.join(SITE, 'index.html'), encoding='utf-8').read()
    ok(src.count("ilova egasi tomonidan o'quv rejasi uchun ko'rib chiqiladi") >= 2, "Maxfiylik gapi: ruxsat kartasi va tanishtiruvda")
    ok(not PE, f"JS xato yo'q {PE[:3]}")
finally:
  srv.terminate()
print('\nJAMI XATO:', len(ERR)); [print(' -', e) for e in ERR]; sys.exit(1 if ERR else 0)
