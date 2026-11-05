"""Bilimjon 0.5.0 — soxta Firebase bilan 3 telefon sinovi: dadasi (A), oyisi (B), boshqa oila (C)."""
import json, os, sys, time, subprocess, threading
from playwright.sync_api import sync_playwright

D = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(os.path.join(D, '..', '..')); FAKE = D
srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8765'], cwd=SITE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)
STORE = {}; LOCK = threading.Lock()

def fs(arg):
    a = json.loads(arg); op = a[0]
    with LOCK:
        if op == 'get': return json.dumps(STORE.get(a[1]))
        if op == 'del': STORE.pop(a[1], None); return 'null'
        if op == 'list':
            pre = a[1] + '/'; return json.dumps([[k, v] for k, v in STORE.items() if k.startswith(pre) and '/' not in k[len(pre):]])
        if op == 'set':
            path, data, merge = a[1], a[2], a[3]
            old = dict(STORE.get(path) or {}) if merge else {}
            for k, v in data.items():
                if isinstance(v, dict) and '__au' in v:
                    cur = list(old.get(k) or []); [cur.append(x) for x in v['__au'] if x not in cur]; old[k] = cur
                else: old[k] = v
            STORE[path] = old; return 'null'
    return 'null'

FILES = {'firebase-app.js': 'export function initializeApp(c){return {c}}',
         'firebase-auth.js': open(os.path.join(FAKE, 'auth.js')).read(),
         'firebase-firestore.js': open(os.path.join(FAKE, 'fs.js')).read()}
ERR = []
ok = lambda c, m: print(('✅ ' if c else '❌ ') + m) or (None if c else ERR.append(m))

def tel(br, nom):
    ctx = br.new_context(viewport={'width': 390, 'height': 800}, service_workers='block')
    ctx.expose_function('__fs', fs)
    ctx.route('https://www.gstatic.com/firebasejs/**', lambda r: r.fulfill(status=200, content_type='text/javascript', body=FILES[r.request.url.split('/')[-1]]))
    pg = ctx.new_page(); pg.on('pageerror', lambda e: ERR.append(f'{nom} pageerror: {e}'))
    pg.goto('http://localhost:8765/'); pg.wait_for_timeout(500); return pg

def oila(pg, nom):
    pg.fill('#on', nom); pg.fill('#p1', '1234'); pg.fill('#p2', '1234'); pg.click('#go'); pg.wait_for_timeout(300)

def kirish(pg, email):
    pg.wait_for_selector('#be', timeout=5000); pg.fill('#be', email); pg.fill('#bp', 'parol123'); pg.click('[data-in]')

ev = lambda pg, js: pg.evaluate(js)
with sync_playwright() as p:
    br = p.chromium.launch()
    # ---- A: dadasi telefoni, oila + 2 bola + natija
    A = tel(br, 'A'); oila(A, 'Test oila')
    bid = ev(A, "(()=>{const b=BJ.A.newBola({laqab:'Ali',daraja:'g1',avatar:'🦊'}); BJ.A.newBola({laqab:'Vali',daraja:'g0',avatar:'🐼'}); b.yulduz=5; BJ.A.save(true); BJ.A.pushLog(b.id,{t:'javob',ts:Date.now(),ok:1}); BJ.A.flushLog(); return b.id})()")
    ev(A, "BJ.A.otaOk={rol:'admin',t:Date.now()}"); A.goto('http://localhost:8765/#ota'); A.wait_for_timeout(300)
    ok(A.locator('[data-go="ota-bulut"]').count() == 1, 'Panel menyusida ☁️ Oila akkaunti tugmasi bor')
    A.click('[data-go="ota-bulut"]'); kirish(A, 'dad@test.uz'); A.wait_for_timeout(2500)
    ok('oila/U_dadtestuz' in STORE, "A: oila hujjati bulutga yozildi")
    ok(f'oila/U_dadtestuz/bolalar/{bid}' in STORE, 'A: bola bulutga yozildi')
    lg = [k for k in STORE if '/log/' in k]; ok(len(lg) >= 1 and len(STORE[lg[0]]['e']) >= 1, 'A: log arrayUnion bilan yozildi')
    ok(A.locator('text=Ulangan').count() >= 1, 'A: ekranda «✅ Ulangan»')
    # ---- B: oyisi telefoni, yangi — «Akkauntim bor»
    B = tel(br, 'B'); ok(B.locator('#bk').count() == 1, 'B: birinchi ekranda «☁️ Akkauntim bor» bor')
    B.click('#bk'); kirish(B, 'dad@test.uz'); B.wait_for_timeout(2500)
    sb = ev(B, "(()=>{const s=BJ.A.S(); return {oila:s.oila&&s.oila.nom, n:Object.keys(s.bolalar).length, y:(s.bolalar['%s']||{}).yulduz, pin:!!s.pin, log:BJ.A.readLog('%s',BJ.A.todayKey()).length}})()" % (bid, bid))
    ok(sb['oila'] == 'Test oila' and sb['n'] == 2 and sb['y'] == 5 and sb['pin'], f'B: bulutdan oila, 2 bola, ⭐5, PIN olindi {sb}')
    ok(sb['log'] >= 1, 'B: log ham keldi')
    ok(B.locator('.kid').count() == 2, 'B: bola tanlash ekranida 2 bola')
    # ---- B da o'ynaldi → A ga keladi
    ev(B, f"(()=>{{const b=BJ.A.bola('{bid}'); b.yulduz=9; BJ.A.save(true); BJ.A.pushLog(b.id,{{t:'javob',ts:Date.now()+5,ok:0}}); BJ.A.flushLog();}})()")
    A.goto('http://localhost:8765/#ota'); A.wait_for_timeout(9000)
    ya = ev(A, f"BJ.A.bola('{bid}').yulduz"); ok(ya == 9, f'A: B dagi natija keldi (⭐ {ya})')
    ev(A, "BJ.bulut.logOl(2)"); A.wait_for_timeout(800)
    la = ev(A, f"BJ.A.readLog('{bid}',BJ.A.todayKey()).length"); ok(la >= 2, f'A: B logi qo\'shildi ({la} yozuv, takrorsiz)')
    # ---- faol missiyada kelgan yangilanish kutib turadi
    ev(A, f"(()=>{{const s=BJ.A.S(); s.joriy='{bid}'; BJ.A.save(true); history.replaceState(null,'','#missiya');}})()")
    ev(B, f"(()=>{{const b=BJ.A.bola('{bid}'); b.yulduz=12; BJ.A.save(true);}})()"); A.wait_for_timeout(8000)
    ok(ev(A, f"BJ.A.bola('{bid}').yulduz") == 9, 'A: missiya paytida bola holati almashtirilmadi (kutib turdi)')
    A.evaluate("location.hash='uy'"); A.wait_for_timeout(1500)
    ok(ev(A, f"BJ.A.bola('{bid}').yulduz") == 12, 'A: missiyadan chiqqach yangilanish qo\'llandi')
    # ---- bola o'chirish sinxroni
    vid = ev(B, "BJ.A.bolalar().find(b=>b.laqab==='Vali').id"); ev(B, f"BJ.A.delBola('{vid}')"); B.wait_for_timeout(7000); A.wait_for_timeout(2000)
    ok(f'oila/U_dadtestuz/bolalar/{vid}' not in STORE and ev(A, f"!BJ.A.S().bolalar['{vid}']"), 'Bola o\'chirilishi ikkala telefonga yetdi')
    # ---- 🏆 Reyting guruhi: A yaratadi, C (boshqa oila) qo'shiladi
    ev(A, "BJ.A.otaOk={rol:'admin',t:Date.now()}"); A.goto('http://localhost:8765/#ota-reyting'); A.wait_for_timeout(500)
    A.click('[data-gy]'); A.wait_for_timeout(1500)
    kod = ev(A, "BJ.A.S().guruh&&BJ.A.S().guruh.kod"); ok(bool(kod) and len(kod) == 10, f'A: guruh yaratildi ({kod})')
    ok(ev(B, "new Promise(r=>setTimeout(()=>r(BJ.A.S().guruh&&BJ.A.S().guruh.kod),7000))") == kod, 'B: guruh kodi oyisining telefoniga ham o\'tdi')
    C = tel(br, 'C'); oila(C, 'Qoshni'); ev(C, "(()=>{const b=BJ.A.newBola({laqab:'Zuhra',daraja:'g1',avatar:'🦄'}); b.yulduz=3; BJ.A.save(true);})()")
    ev(C, "BJ.A.otaOk={rol:'admin',t:Date.now()}"); C.goto('http://localhost:8765/#ota-bulut'); kirish(C, 'qoshni@test.uz'); C.wait_for_timeout(2000)
    C.goto('http://localhost:8765/#ota-reyting'); C.wait_for_timeout(600)
    C.fill('#gk', 'NOTOGRI123')  # 10 belgi, lekin bunday guruh yo'q — soxta omborda rad etish yo'q, shuning uchun to'g'ri kodni sinaymiz
    C.fill('#gk', kod.lower()); C.click('[data-gk]'); C.wait_for_timeout(8000)
    tc = ev(C, "Object.keys(BJ.A.S().oilaTel).filter(q=>q.startsWith('G:')).map(q=>BJ.A.S().oilaTel[q])")
    ok(len(tc) == 1 and any(b['laqab'] == 'Ali' and b['yulduz'] >= 0 for b in tc[0]['bolalar']), f'C: guruhda A oilasining bolasi ko\'rindi ({tc and [b["laqab"] for b in tc[0]["bolalar"]]})')
    A.wait_for_timeout(2000)
    ta = ev(A, "Object.keys(BJ.A.S().oilaTel).filter(q=>q.startsWith('G:')).length"); ok(ta == 1, 'A: guruhda C oilasi ko\'rindi')
    rr = ev(A, "BJ.A.reytingRoyxat().map(x=>x.laqab)"); ok('Zuhra' in rr, f'A: reyting ro\'yxatida Zuhra ({rr})')
    azo = [k for k in STORE if k.startswith(f'guruh/{kod}/azo/')]; d0 = STORE[azo[0]]
    ok(set(d0.keys()) <= {'uid','oila','av','laqab','daraja','yulduz','kun','osish','detal','missiya','wk','ts'}, 'Guruhga faqat ruxsat etilgan maydonlar yozildi (ism-familiya yo\'q)')
    # ---- akkauntsiz telefon: SDK umuman yuklanmaydi
    ctx = br.new_context(service_workers='block'); n = []
    ctx.on('request', lambda r: n.append(r.url) if 'firebasejs' in r.url else None)
    pz = ctx.new_page(); pz.goto('http://localhost:8765/'); pz.wait_for_timeout(800)
    ok(not n, 'Akkauntsiz telefonda Firebase yuklanmaydi')
    # ---- telefon kengligi skrinshoti
    A.goto('http://localhost:8765/#ota-bulut'); A.wait_for_timeout(500); A.screenshot(path=os.path.join('/tmp', 'shot_bulut.png'))
    A.goto('http://localhost:8765/#ota-reyting'); A.wait_for_timeout(500); A.screenshot(path=os.path.join('/tmp', 'shot_reyting.png'), full_page=True)
    br.close()
srv.terminate()
print('\nXATOLAR:', ERR if ERR else 'yo\'q')
