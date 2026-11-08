"""Bilimjon 0.7.7 — 🔒 yangi telefon eshigi + 📖 tanishtiruv + ✈️ egasiga Telegram (08.11, u: «yangi odam ruxsatdan oldin ishlatmasin —
faqat rasmli ma'lumot; tanishtiruv ilova ichida; kim ulansa menga Telegram'dan xabar kelsin; 1 oy tekin, keyin pullik»).
Soxta Firebase (sinov/bulut/fs.js, auth.js) + firestore.rules 0.7.7 Python nusxasi (ilova/egasi: o'qish — kirgan, yozish — admin).
Ishga tushirish: python3 sinov/v077/sinov_eshik.py"""
import os, sys, time, subprocess, json, threading
from urllib.parse import unquote
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.abspath(os.path.join(D, '..', '..')); FAKE = os.path.join(SITE, 'sinov', 'bulut')
PORT = 8813; URL = f'http://localhost:{PORT}/'
srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT)], cwd=SITE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
ERR = []; PE = []; SUR = os.environ.get('SURAT')   # SURAT=<papka> — ekran rasmlari (ko'rib chiqish uchun)
def sur(pg, n): (pg.screenshot(path=os.path.join(SUR, n + '.png'), full_page=True) if SUR else None)
def ok(c, m): print(('✅ ' if c else '❌ ') + m); (None if c else ERR.append(m))
STORE = {}; LOCK = threading.RLock(); RULES = {'admin': 'U_admintestuz'}
def ruxsatli(uid): return uid == RULES['admin'] or (STORE.get('ruxsat/' + str(uid)) or {}).get('holat') == 'ok'
def sorov_togri(d, who):
    return set(d) <= {'email', 'oila', 'ts', 'holat'} and d.get('holat') == 'kutish' and d.get('email') == who.get('email') \
        and isinstance(d.get('oila'), str) and len(d['oila']) <= 24 and isinstance(d.get('ts'), int) and not isinstance(d.get('ts'), bool)
def ruxsat(op, path, who, new=None):   # firestore.rules 0.7.7 mantig'i
    uid = who.get('uid'); p = path.split('/'); adm = uid is not None and uid == RULES['admin']
    if uid is None: return False
    if p[0] == 'ilova': return op in ('get', 'list') or adm
    if p[0] == 'ruxsat':
        if op == 'list': return adm
        if op == 'get': return uid == p[1] or adm
        if op == 'del': return adm
        if adm: return True
        old = STORE.get(path)
        return uid == p[1] and (old is None or old.get('holat') == 'kutish') and sorov_togri(new, who)
    if p[0] == 'oila':
        if adm: return True
        if len(p) < 2 or uid != p[1]: return False
        return op in ('get', 'list') or ruxsatli(uid)
    if p[0] == 'guruh': return op in ('get', 'list', 'del') or ruxsatli(uid)
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
            STORE[path] = old; return 'null'
    return 'null'
FILES = {'firebase-app.js': 'export function initializeApp(c){return {c}}', 'firebase-auth.js': open(os.path.join(FAKE, 'auth.js')).read(), 'firebase-firestore.js': open(os.path.join(FAKE, 'fs.js')).read()}
def tel(br, nom, q='?eshik=1'):
    ctx = br.new_context(viewport={'width': 390, 'height': 844}, service_workers='block', has_touch=True); ctx.expose_function('__fs', fs)
    ctx.route('https://www.gstatic.com/firebasejs/**', lambda r: r.fulfill(status=200, content_type='text/javascript', body=FILES[r.request.url.split('/')[-1]]))
    pg = ctx.new_page(); pg.on('pageerror', lambda e: PE.append(f'{nom} pageerror: {e}')); pg.goto(URL + q); pg.wait_for_timeout(500); return pg
def kut(pg, js, ms=8000):
    try: pg.wait_for_function(js, timeout=ms); return True
    except Exception: return False
TXT = lambda pg: pg.evaluate("document.body.innerText")
HASH = lambda pg: pg.evaluate("location.hash")
ONB = lambda pg: pg.locator('#on').count() > 0
def royxat(pg, email, nom=None):
    pg.fill('#be', email); pg.fill('#bp', 'parol123'); pg.click('[data-up]')
    kut(pg, "document.body.innerText.indexOf('Ruxsat kerak')>=0 || document.body.innerText.indexOf('Ruxsat kutilmoqda')>=0")
    if nom: pg.fill('#rxn', nom); pg.click('[data-rxq]'); kut(pg, "document.body.innerText.indexOf('Ruxsat kutilmoqda')>=0")
try:
  with sync_playwright() as p:
    br = p.chromium.launch()
    # ===== A) 📖 Tanishtiruv (yangi telefon) =====
    T = tel(br, 'YANGI1')
    ok(HASH(T) == '#tanish' and T.locator('.tnw').count() == 1 and '1 / 5' in TXT(T) and T.locator('.tndots button').count() == 5, "yangi telefon: birinchi ekran — 📖 tanishtiruv (5 slayd)")
    ok(not ONB(T) and T.evaluate("document.documentElement.scrollWidth") <= 390, "oila yaratish ekrani ko'rinmaydi · 390 px da gorizontal siljish yo'q")
    T.click('[data-nx]'); T.wait_for_timeout(200); s2 = '2 / 5' in TXT(T) and 'Har kuni' in TXT(T)
    T.click('[data-pr]'); T.wait_for_timeout(200); ok(s2 and '1 / 5' in TXT(T), "«Keyingi →» va «←» ishlaydi")
    T.click('.tndots button[data-d="2"]'); T.wait_for_timeout(200); d3 = '3 / 5' in TXT(T) and "O'yinlar" in TXT(T)
    T.evaluate("""(()=>{const w=document.querySelector('.tnw'), t=(x)=>new Touch({identifier:1,target:w,clientX:x,clientY:400});
      w.dispatchEvent(new TouchEvent('touchstart',{touches:[t(320)],changedTouches:[t(320)],bubbles:true})); w.dispatchEvent(new TouchEvent('touchend',{touches:[],changedTouches:[t(120)],bubbles:true}));})()""")
    T.wait_for_timeout(200); ok(d3 and '4 / 5' in TXT(T) and 'Ota-ona' in TXT(T), "nuqtalar va barmoq bilan surish (swipe) — slayd almashadi")
    T.click('[data-sk]'); T.wait_for_timeout(200); t5 = TXT(T)
    ok('5 / 5' in t5 and '1 oy' in t5 and 'bepul' in t5 and 'pullik' in t5 and 'tarqatmang' in t5 and T.locator('[data-sk]').count() == 0, "«O'tkazish» → oxirgi slayd: 🎁 1 oy bepul, keyin pullik · tarqatmang")
    ok(all(T.locator('.tnsc svg').count() >= 1 for _ in [0]) and 'Ro\'yxatdan o\'tish' in T.inner_text('[data-nx]'), "oxirgi slayd: rasm (SVG) + «✉️ Ro'yxatdan o'tish / kirish»")
    T.click('[data-nx]'); T.wait_for_timeout(600); g = TXT(T)
    ok(HASH(T) == '#bulut' and "Bilimjon'ga kirish" in g and T.locator('.eqd span').count() == 3 and T.locator('.eqd .on').count() == 1 and 'bepul' in g, "→ ☁️ kirish ekrani (eshik): 3 qadam, 1-qadam faol, 1 oy bepul")
    kut(T, "!!document.querySelector('#be')"); sur(T, 'e1_kirish'); ok(T.locator('#be').count() == 1 and T.locator('[data-up]').count() == 1 and T.locator('[data-in]').count() == 1, "email + parol: «Ro'yxatdan o'tish» va «Kirish»")
    yop = []
    for h in ['', '#uy', '#ota', '#ota-qosh', '#missiya', '#zal', '#mashq', '#dokon', '#tanla']:
        T.goto(URL + '?eshik=1' + h); T.wait_for_timeout(450)
        if ONB(T) or T.locator('.kid,.ota .menu,[data-id]').count() or HASH(T) not in ('#bulut', '#tanish'): yop.append(h or "''")
    ok(not yop and HASH(T) == '#bulut', f"ruxsatsiz hech qaysi ekran ochilmaydi (uy, ota-ona, missiya, zal…){' — OCHILDI: ' + ', '.join(yop) if yop else ''}; tanishtiruv qayta chiqmaydi")
    T.click('[data-bk]'); T.wait_for_timeout(300); ok(HASH(T) == '#tanish' and '1 / 5' in TXT(T), "eshikda «←» → tanishtiruvga qaytadi")
    T.goto(URL + '?eshik=1#bulut'); T.wait_for_timeout(400)
    # ===== B) Ro'yxat → ruxsat so'rash (Telegram qo'yilmagan) =====
    royxat(T, 'yangi@test.uz'); g = TXT(T); sur(T, 'e2_sorov')
    ok('Ruxsat kerak' in g and 'bepul' in g and T.locator('#rxn').count() == 1 and T.locator('.eqd span').nth(1).get_attribute('class') == 'on', "ro'yxatdan keyin: «🛡️ Ruxsat kerak» + oila nomi, 2-qadam faol")
    ok("Egasi tasdiqlashi bilan ilova shu telefonda ochiladi" in g and 'hozir ham to\'liq ishlaydi' not in g, "yangi telefonga matn: ilova ruxsatdan keyin ochiladi (eski «hozir ham ishlaydi» emas)")
    T.fill('#rxn', 'Yangi oila'); T.click('[data-rxq]'); kut(T, "document.body.innerText.indexOf('Ruxsat kutilmoqda')>=0")
    with LOCK: r = STORE.get('ruxsat/U_yangitestuz') or {}
    ok(r.get('holat') == 'kutish' and r.get('oila') == 'Yangi oila' and r.get('email') == 'yangi@test.uz', "📨 so'rov bulutda: ruxsat/{uid} kutish")
    ok(T.locator('a.tg').count() == 0 and T.locator('[data-rxm]').count() == 1 and T.locator('.eqd .on').count() == 1 and 'Egasi' in T.inner_text('.eqd .on'), "Telegram qo'yilmagan: «📤 Egasiga xabar» (ulashish), 3-qadam faol")
    T.goto(URL + '?eshik=1#uy'); T.wait_for_timeout(500); ok(HASH(T) == '#bulut' and not ONB(T) and 'Ruxsat kutilmoqda' in TXT(T), "kutayotganda ham ilova yopiq (#uy → kirish ekrani)")
    ok(T.evaluate("(async()=>{try{await window.__fs(JSON.stringify(['set','ilova/egasi',{tg:'buzgunchi'},false,{uid:'U_yangitestuz',email:'yangi@test.uz'}]));return 1}catch(e){return 0}})()") == 1 and 'ilova/egasi' not in STORE,
       "qoidalar: oddiy akkaunt ilova/egasi ga yoza olmaydi (Telegram manzilini almashtira olmaydi)")
    # ===== C) Admin: ✈️ Telegram manzilini qo'yadi =====
    AD = tel(br, 'ADMIN', '?tez=1'); AD.fill('#on', 'Admin oila'); AD.fill('#p1', '1234'); AD.fill('#p2', '1234'); AD.click('#go'); AD.wait_for_timeout(300)
    AD.evaluate("(()=>{const A=BJ.A; const b=A.newBola({laqab:'Ali',daraja:'g1',avatar:'🦊',dunyo:'garaj'}); A.save(true)})()")
    AD.evaluate("BJ.A.otaOk={rol:'admin',t:Date.now()}"); AD.goto(URL + '?tez=1#ota-bulut'); AD.wait_for_timeout(500)
    AD.evaluate("BJ.A.otaOk={rol:'admin',t:Date.now()}"); AD.evaluate("location.hash='ota'"); AD.wait_for_timeout(200); AD.evaluate("location.hash='ota-bulut'"); kut(AD, "!!document.querySelector('#be')")
    AD.fill('#be', 'admin@test.uz'); AD.fill('#bp', 'parol123'); AD.click('[data-in]'); kut(AD, "!!document.querySelector('#tgn')", 10000)
    ok(AD.locator('#tgn').count() == 1 and "Hali qo'yilmagan" in TXT(AD), "admin panelida: ✈️ Telegram kartasi (hali qo'yilmagan)")
    AD.fill('#tgn', 'bil'); AD.click('[data-tgs]'); AD.wait_for_timeout(400); bad = 'ilova/egasi' not in STORE
    AD.fill('#tgn', '@Bilim_Ega'); AD.click('[data-tgs]'); kut(AD, "document.body.innerText.indexOf('Saqlandi')>=0", 4000); AD.wait_for_timeout(300)
    with LOCK: eg = STORE.get('ilova/egasi') or {}
    AD.evaluate("document.querySelector('.rxtg').scrollIntoView()"); sur(AD, 'e4_admin')
    ok(bad and eg.get('tg') == 'Bilim_Ega' and isinstance(eg.get('ts'), int), "✈️ «💾 Saqlash»: noto'g'ri manzil rad, @Bilim_Ega → ilova/egasi")
    # ===== D) 2-yangi telefon: Telegram tugmasi tayyor xabar bilan =====
    J = tel(br, 'YANGI2'); J.click('[data-sk]'); J.click('[data-nx]'); kut(J, "!!document.querySelector('#be')")
    royxat(J, 'dost@test.uz', 'Dost oila'); kut(J, "!!document.querySelector('a.tg')", 6000)
    sur(J, 'e3_kutish'); href = J.get_attribute('a.tg', 'href') or ''; txt = unquote(href.split('?text=')[-1]) if '?text=' in href else ''
    ok(href.startswith('https://t.me/Bilim_Ega?text=') and 'dost@test.uz' in txt and 'Dost oila' in txt and J.get_attribute('a.tg', 'target') == '_blank',
       "⏳ kutish ekranida «✈️ Telegram'da egasiga yozish» → t.me/Bilim_Ega, xabarda oila va email")
    ok(J.locator('[data-rxm]').count() == 1 and J.evaluate("document.documentElement.scrollWidth") <= 390, "zaxira: «📤 Boshqa yo'l bilan» · 390 px")
    # ===== E) Egasi ✅ → ilova ochiladi: oila yaratish → ishlaydi =====
    with LOCK: STORE['ruxsat/U_dosttestuz']['holat'] = 'ok'
    kut(J, "!!document.querySelector('#on')", 12000)
    ok(ONB(J) and HASH(J) in ('', '#'), "egasi ✅ → shu ekran o'zi yangilanadi → oila yaratish (bulut bo'sh)")
    J.fill('#on', 'Dost oila'); J.fill('#p1', '4321'); J.fill('#p2', '4321'); J.click('#go'); J.wait_for_timeout(500)
    ok(J.evaluate("!!BJ.A.S().oila") and HASH(J).startswith('#ota'), "oila yaratildi → bola qo'shish (ota-ona paneli)")
    J.goto(URL + '?eshik=1#uy'); J.wait_for_timeout(600); ok(HASH(J) != '#bulut' and HASH(J) != '#tanish', "qayta ochilganda ilova ochiq (eshik yo'q)")
    def oilaBulutda():
        x = STORE.get('oila/U_dosttestuz'); return bool(x and json.loads(x['j']).get('oila', {}).get('nom') == 'Dost oila')
    t0 = time.time()
    while time.time() - t0 < 12:
        with LOCK:
            if oilaBulutda(): break
        J.wait_for_timeout(300)
    with LOCK: ok(oilaBulutda(), "yangi oila bulutga yozildi (ruxsat bor — sinxron ishlaydi)")
    # ===== F) Rad etilgan — ochilmaydi =====
    with LOCK: STORE['ruxsat/U_yangitestuz']['holat'] = 'rad'
    kut(T, "document.body.innerText.indexOf('Ruxsat berilmadi')>=0", 8000); T.goto(URL + '?eshik=1#uy'); T.wait_for_timeout(600)
    ok('Ruxsat berilmadi' in TXT(T) and not ONB(T) and HASH(T) == '#bulut', "rad etilgan akkaunt: «❌ Ruxsat berilmadi», ilova ochilmaydi")
    # ===== G) Boshqa holatlar =====
    A2 = tel(br, 'ADMIN2'); A2.click('[data-sk]'); A2.click('[data-nx]'); kut(A2, "!!document.querySelector('#be')")
    A2.fill('#be', 'admin@test.uz'); A2.fill('#bp', 'parol123'); A2.click('[data-in]')
    t0 = time.time()
    while time.time() - t0 < 10 and not A2.evaluate("!!(BJ.A.S().oila && Object.keys(BJ.A.S().bolalar).length)"): A2.wait_for_timeout(300)
    A2.wait_for_timeout(500); ok(A2.evaluate("!!(BJ.A.S().oila && Object.keys(BJ.A.S().bolalar).length)") and HASH(A2) not in ('#bulut', '#tanish') and 'Ali' in TXT(A2),
       "egasi yangi telefonda «Kirish» → bulutdagi oila keladi, ilova ochiladi")
    E = tel(br, 'ESKI', '?tez=1'); E.fill('#on', 'Eski oila'); E.fill('#p1', '1111'); E.fill('#p2', '1111'); E.click('#go'); E.wait_for_timeout(300)
    ok(True, "?tez=1 da (sinovlar) eshik yo'q — oila yaratish ekrani avvalgidek")
    E.goto(URL + '?eshik=1'); E.wait_for_timeout(600)
    ok(E.evaluate("!!BJ.A.S().oila") and HASH(E) not in ('#bulut', '#tanish') and not ONB(E), "eski telefon (oilasi bor, akkauntsiz) — o'zgarishsiz ishlaydi")
    E.evaluate("BJ.A.otaOk={rol:'admin',t:Date.now()}"); E.evaluate("location.hash='ota'"); E.wait_for_timeout(400)
    ok(E.locator('[data-go="tanish"]').count() == 1, "ota-ona menyusida «📖 Tanishtiruv (yangi oilaga)»")
    E.click('[data-go="tanish"]'); E.wait_for_timeout(300); E.click('[data-sk]'); E.wait_for_timeout(200)
    lab = E.inner_text('[data-nx]'); E.click('[data-nx]'); E.wait_for_timeout(400)
    ok('Tushunarli' in lab and HASH(E) == '#ota', "oilasi bor telefonda tanishtiruv → «✓ Tushunarli» → ota-ona paneli")
    S = tel(br, 'SINOV', '?tez=1&eshik=1'); ok(HASH(S) == '#tanish' and not ONB(S), "?tez=1&eshik=1 — sinovda eshik yoqiladi")
    L0 = tel(br, 'LOCAL', ''); ok(ONB(L0), "localhost (eski sinovlar) — eshik yo'q, oila yaratish ekrani")
    ok(not PE, f"JS xato yo'q {PE[:3]}")
finally:
  srv.terminate()
print('\nJAMI XATO:', len(ERR)); [print(' -', e) for e in ERR]; sys.exit(1 if ERR else 0)
