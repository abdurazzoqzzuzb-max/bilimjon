"""Bilimjon 0.7.6 — 🎮 o'yinlar: zal 🔑 ota-ona ruxsati (PIN), dam olishda 7 o'yindan tanlov (A.zal.damRun), 🏆 o'yin reytingi (oila + reyting guruhi),
🏅 haftaning chempioni, 🧠 bilim chiptasi, 📊 hafta xulosasida o'yin qatori; ☁️ guruh a'zosiga «zal» maydoni (qoidalar 0.7.6 Python nusxasi) va
admin «guruh» buyrug'i bilan qo'yilgan guruh telefonda mahalliy o'zgarish bo'lsa ham yo'qolmasligi.
Ishga tushirish: python3 sinov/v076/sinov_v076.py  (skrinshotlar: /tmp/bj076_*.png)"""
import os, sys, time, subprocess, json, threading
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.abspath(os.path.join(D, '..', '..')); FAKE = os.path.join(SITE, 'sinov', 'bulut')
PORT = 8806; URL = f'http://localhost:{PORT}/'
srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT)], cwd=SITE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
ERR = []; PE = []
def ok(c, m): print(('✅ ' if c else '❌ ') + m); (None if c else ERR.append(m))
SHOT = lambda pg, n: pg.screenshot(path=f'/tmp/bj076_{n}.png', full_page=True)

# ---------- soxta Firebase (qoidalar 0.7.6 — guruh azo: ruxsat etilgan maydonlar + ixtiyoriy zal {r, h, p}) ----------
STORE = {}; LOCK = threading.RLock(); RULES = {'admin': 'U_admintestuz'}; RAD = []
AZO = {'uid', 'oila', 'av', 'laqab', 'daraja', 'yulduz', 'kun', 'osish', 'detal', 'missiya', 'wk', 'ts', 'zal', 'bu', 'dz', 'ol'}   # qoidalar 0.9.1
def ruxsatli(uid): return uid == RULES['admin'] or (STORE.get('ruxsat/' + str(uid)) or {}).get('holat') == 'ok'
def azo_togri(d, uid):
    if not set(d) <= AZO or d.get('uid') != uid: return False
    if 'zal' in d and not (isinstance(d['zal'], dict) and set(d['zal']) <= {'r', 'h', 'p'}): return False
    if 'bu' in d and not (isinstance(d['bu'], dict) and set(d['bu']) <= {'k', 'm', 'd', 'n', 'p'}): return False
    if 'dz' in d and not (isinstance(d['dz'], int) and 0 <= d['dz'] <= 100): return False
    if 'ol' in d and not (isinstance(d['ol'], list) and len(d['ol']) <= 10): return False   # 0.9.1: 👏 olqishlar
    return isinstance(d.get('laqab'), str) and len(d['laqab']) <= 24 and isinstance(d.get('yulduz'), int)
def ruxsat(op, path, who, new=None):
    uid = who.get('uid'); p = path.split('/'); adm = uid is not None and uid == RULES['admin']
    if uid is None: return False
    if p[0] == 'ruxsat': return op != 'list' or adm
    if p[0] == 'oila':
        if adm: return True
        if len(p) < 2 or uid != p[1]: return False
        return op in ('get', 'list') or ruxsatli(uid)
    if p[0] == 'guruh':
        azomi = len(p) > 1 and ('guruh/%s/oilalar/%s' % (p[1], uid)) in STORE
        if op in ('get', 'list'): return azomi or len(p) == 1
        if len(p) == 4 and p[2] == 'azo' and op == 'set':
            r = azomi and ruxsatli(uid) and azo_togri(new, uid)
            if not r: RAD.append(path)
            return r
        return ruxsatli(uid)
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
def tel(br, nom):
    ctx = br.new_context(viewport={'width': 390, 'height': 844}, service_workers='block'); ctx.expose_function('__fs', fs)
    ctx.route('https://www.gstatic.com/firebasejs/**', lambda r: r.fulfill(status=200, content_type='text/javascript', body=FILES[r.request.url.split('/')[-1]]))
    pg = ctx.new_page(); pg.on('pageerror', lambda e: PE.append(f'{nom} pageerror: {e}')); pg.goto(URL); pg.wait_for_timeout(400); return pg
def oila(pg, nom): pg.fill('#on', nom); pg.fill('#p1', '1234'); pg.fill('#p2', '1234'); pg.click('#go'); pg.wait_for_timeout(300)
def kutf(pg, js, ms=8000):
    try: pg.wait_for_function(js, timeout=ms); return True
    except Exception: return False
PUMP = [None]
def kutpy(f, ms=10000):
    t = time.time()
    while time.time() - t < ms / 1000:
        with LOCK:
            if f(): return True
        PUMP[0].wait_for_timeout(200)
    with LOCK: return bool(f())
def ota(pg, h='#ota-bulut'): pg.evaluate("BJ.A.otaOk={rol:'admin',t:Date.now()}"); pg.goto(URL + h); pg.wait_for_timeout(500)

try:
  with sync_playwright() as p:
    br = p.chromium.launch(args=['--autoplay-policy=no-user-gesture-required'])
    ctx = br.new_context(viewport={'width': 390, 'height': 844}, service_workers='block'); pg = ctx.new_page()
    pg.on('pageerror', lambda e: PE.append(f'pageerror: {e}')); ev = pg.evaluate
    NV = [0]
    def NAV(h, ms=450): NV[0] += 1; pg.goto(URL + f'?tez=1&r={NV[0]}#' + h); ev('BJ.A.render()'); pg.wait_for_timeout(ms)
    def GO(h, ms=400): ev(f"location.hash='{h}'"); pg.wait_for_timeout(ms)
    def kut(js, ms=8000):
        t = time.time()
        while time.time() - t < ms / 1000:
            if ev(js): return True
            pg.wait_for_timeout(80)
        return False
    pg.goto(URL + '?tez=1'); pg.wait_for_timeout(400)
    pg.fill('#on', 'Sinov'); pg.fill('#p1', '1234'); pg.fill('#p2', '1234'); pg.click('#go'); pg.wait_for_timeout(300)
    K, Q, R = ev("""(()=>{const A=BJ.A; const k=A.newBola({laqab:'Kichik',daraja:'g0',avatar:'🐯',dunyo:'garaj'}); const q=A.newBola({laqab:'Orta',daraja:'g1',avatar:'🦄',dunyo:'orol'});
      const r=A.newBola({laqab:'Katta',daraja:'g2',avatar:'🐼',dunyo:'garaj'}); A.S().sozlama.uyqu=''; A.S().joriy=k.id; A.save(true); return [k.id,q.id,r.id]})()""")
    setj = lambda bid: ev(f"(()=>{{const s=BJ.A.S(); s.joriy='{bid}'; BJ.A.save(true)}})()")
    X = lambda bid, e: ev(f"(()=>{{const A=BJ.A, b=A.S().bolalar['{bid}']; return {e}}})()")
    W = lambda: ev("Math.max(document.documentElement.scrollWidth, ...[...document.querySelectorAll('#app *, .sheet *')].map(e=>e.getBoundingClientRect().right).filter(x=>x<2000))")

    # ================= A) 🔑 ZAL — OTA-ONA RUXSATI =================
    ok(ev("BJ.A.S().sozlama.zalOchish === undefined && BJ.A.S().sozlama.zalChipta === undefined"), "Yangi sozlamalar defaults() ga QO'SHILMAGAN (yangilanishda umumiy holat o'zgarib, bulut sinxroni to'qnashmasin)")
    NAV('uy')
    ok(pg.locator('[data-zal].qulf').count() == 1 and '🔒' in pg.inner_text('[data-zal]'), "Missiyasiz: uyda «🔒 missiyadan keyin» tugmasi")
    pg.click('[data-zal]'); pg.wait_for_timeout(350)
    ok(ev("location.hash") == '#zal' and 'Zal hali yopiq' in pg.inner_text('body') and pg.locator('[data-rux]').count() == 1, "Bosilsa — «yopiq» ekrani va «🔑 Ota-ona ruxsati» tugmasi")
    SHOT(pg, 'yopiq')
    pg.click('[data-rux]'); pg.wait_for_timeout(200)
    ok(pg.locator('.sheet [data-d]').count() == 3 and pg.locator('.sheet #zp').count() == 1, "PIN varag'i: +10 / +20 / +30 daqiqa tanlovi va PIN")
    pg.fill('.sheet #zp', '0000'); pg.click('.sheet [data-ok]'); pg.wait_for_timeout(200)
    ok(X(K, "A.zal.ruxsatDaq(b)") == 0 and pg.locator('.sheet').count() == 1, "Noto'g'ri PIN — ruxsat yo'q")
    pg.click('.sheet [data-d="20"]'); pg.fill('.sheet #zp', '1234'); pg.click('.sheet [data-ok]'); pg.wait_for_timeout(450)
    r = X(K, "[A.zal.holat(b).k, A.zal.ruxsatDaq(b), Math.round(A.zal.qoldi(b)), A.zal.bugunDaq(b)]")
    ok(r == ['ochiq', 20, 1800, 30], f"To'g'ri PIN, +20 → zal ochiq, bugun 10+20=30 daq {r}")
    ok(ev("location.hash") == '#zal' and pg.locator('.zcard').count() == 7 and '🔑 Ota-ona ruxsati bilan' in pg.inner_text('body'), "Zal ochildi: 7 o'yin, «🔑 Ota-ona ruxsati bilan»")
    ok(any(e.get('hodisa') == 'ruxsat' and e.get('daq') == 20 for e in X(K, "A.readLog(b.id, A.todayKey()).filter(e=>e.t==='zal')")), "Log: {t:'zal', hodisa:'ruxsat', daq:20}")
    ok(W() <= 391, f"390 px: zal ekrani ({W()})")
    ev("BJ.A.S().sozlama.zal=0; BJ.A.save(true)"); setj(Q); NAV('uy')
    ok(X(Q, "A.zal.holat(b).k") == 'yopiq' and pg.locator('[data-zal].qulf').count() == 1 and '🔑' in pg.inner_text('[data-zal]'), "Zal o'chiq (0): uyda «🔑 ota-ona ruxsati bilan» tugmasi")
    pg.click('[data-zal]'); pg.wait_for_timeout(300)
    ok("o'chirib qo'ygan" in pg.inner_text('body') and pg.locator('[data-rux]').count() == 1, "Zal o'chiq — ekran ham ruxsat tugmasi bilan")
    pg.click('[data-rux]'); pg.wait_for_timeout(150); pg.fill('.sheet #zp', '1234'); pg.click('.sheet [data-ok]'); pg.wait_for_timeout(350)
    ok(X(Q, "[A.zal.holat(b).k, A.zal.bugunDaq(b)]") == ['ochiq', 10], "Zal o'chiq bo'lsa ham PIN bilan +10 daq ochiladi (faqat ruxsat vaqti)")
    ev("BJ.A.S().sozlama.zal=10; BJ.A.S().sozlama.zalOchish='doim'; BJ.A.save(true)")
    ok(X(R, "A.zal.holat(b).k") == 'ochiq', "«Har doim» rejimi: missiyasiz ham ochiq")
    ev("delete BJ.A.S().sozlama.zalOchish; BJ.A.save(true)")
    ok(X(R, "A.zal.holat(b).k") == 'qulf', "Standart (missiyadan keyin): missiyasiz — qulf")
    NAV('uy'); ev("BJ.A.otaOk={rol:'admin',t:Date.now()}"); GO('ota-sozlama', 400)
    ok(pg.locator('#zo').count() == 1 and pg.locator('#zc').is_checked(), "⚙️: «Zal qachon ochiladi» tanlovi va 🧠 chipta (standart yoqiq)")
    pg.select_option('#zo', 'doim'); pg.uncheck('#zc'); pg.click('[data-save]'); pg.wait_for_timeout(300)
    ok(ev("[BJ.A.S().sozlama.zalOchish, BJ.A.S().sozlama.zalChipta]") == ['doim', False], "⚙️ saqlandi: zalOchish='doim', zalChipta=false")
    ev("BJ.A.S().sozlama.zalOchish='missiya'; BJ.A.S().sozlama.zalChipta=true; BJ.A.save(true)")

    # ================= B) 🎮 DAM OLISHDA 7 O'YIN =================
    ok(ev("Object.values(BJ.A.S().bolalar).map(b=>BJ.A.oyin.turlar(b).length)") == [7, 7, 7], "Dam olish: har yoshga 7 ta o'yin (g0, g1, g2)")
    setj(K); NAV('uy'); ev("window.__dn=0")
    BOSH = "BJ.A.oyin.boshla(BJ.A.bola(), {k:'sinov'}, ()=>{window.__dn=(window.__dn||0)+1})"
    ev(BOSH); pg.wait_for_timeout(250)
    ok(pg.locator('.damg .zcard').count() == 7 and 'Darsga qaytish' in pg.inner_text('body') and ev("BJ.A.CUR().k") == 'oyin', "Maktabgacha bolaga ham tanlov ekrani: 7 o'yin (zIcon), «↩ Darsga qaytish», CUR=oyin")
    ok(W() <= 391 and ev("document.querySelector('.damg').getBoundingClientRect().bottom") < 844 + 40, f"390 px: tanlov ekrani sig'adi ({W()})")
    SHOT(pg, 'dam_tanlov')
    ev("window.__bjOyin().sek = 120")
    zs0 = X(K, "(b.zal && b.zal.sek && b.zal.sek[A.todayKey()]) || 0")
    pg.click('[data-o="turbo"]'); pg.wait_for_timeout(300)
    ok(pg.locator('canvas.zcv').count() == 1 and ev("!!(window.__bjZal() && window.__bjZal().dam)"), "Turbo dam olish rejimida (A.zal.damRun) ochildi")
    for _ in range(500):
        s = ev("(()=>{const S=window.__bjZal(); return S && S.game ? S.game.state() : null})()")
        if not s or s['fin']: break
        if s['a'] is not None: ev(f"window.__bjZal().game.setLane({s['a']})")
        pg.wait_for_timeout(40)
    pg.wait_for_timeout(600)
    ok(pg.locator('[data-yana]').count() == 1 and pg.locator('[data-boshqa]').count() == 1 and pg.locator('[data-dars]').count() == 1, "Natija: «🔁 Yana», «🎮 Boshqa o'yin», «▶ Darsga» (vaqt bor)")
    ok(pg.locator('.zres-rt .zrw').count() >= 1 and 'Reyting' in pg.inner_text('.zres-rt'), "Natija ostida 🏆 reyting jadvali")
    zs1 = X(K, "(b.zal && b.zal.sek && b.zal.sek[A.todayKey()]) || 0")
    ok(abs(zs1 - zs0) < 0.01, f"Dam olishdagi o'yin zal daqiqalariga sanalmaydi ({zs0} → {zs1})")
    r = X(K, "[!!(b.zal.rek.turbo), !!(b.zal.hb && b.zal.hb[A.isoWeek()] && b.zal.hb[A.isoWeek()].turbo), A.readLog(b.id, A.todayKey()).filter(e=>e.t==='zal' && e.tur==='turbo').map(e=>[e.dam||0, e.erta])]")
    ok(r[0] and r[1] and [1, 0] in r[2], f"Rekord, hafta natijasi (hb) va zal logi dam:1 bilan yozildi {r}")
    SHOT(pg, 'dam_natija')
    pg.click('[data-boshqa]'); pg.wait_for_timeout(300)
    ok(pg.locator('.damg .zcard').count() == 7 and "Yana bir o'yin" in pg.inner_text('body'), "«Boshqa o'yin» → tanlov ekrani (vaqt davom etadi)")
    pg.click('[data-o="xotira"]'); pg.wait_for_timeout(300)
    s = ev("window.__bjZal().game.state()"); dk = s['deck']; i0 = 0; j = next(i for i in range(1, len(dk)) if dk[i] == dk[0])
    rest = [i for i in range(len(dk)) if i not in (0, j)]
    for i in (0, j, rest[0], next(k for k in rest[1:] if dk[k] == dk[rest[0]])): ev(f"window.__bjZal().game.flip({i})"); pg.wait_for_timeout(120)
    pg.wait_for_timeout(500)
    ok(pg.locator('[data-dars]').count() == 1, "Xotira tugadi → natija")
    pg.click('[data-dars]'); pg.wait_for_timeout(300)
    lg = X(K, "A.readLog(b.id, A.todayKey()).filter(e=>e.t==='oyin').map(e=>[e.tur,e.raund,e.erta])")
    ok(ev("window.__dn") == 1 and ev("window.__bjOyin()") is None and lg and lg[-1][0] == 'xotira' and lg[-1][1] == 2 and lg[-1][2] == 1, f"«▶ Darsga» → darsga qaytdi, {{t:'oyin'}} logi: 2 o'yin, vaqt qolgan (erta) {lg[-1:]}")
    # vaqt tugashi: majburiy yakun → faqat «Darsga»
    ev(BOSH); pg.wait_for_timeout(200); ev("window.__bjOyin().sek = 3"); pg.click('[data-o="svetofor"]'); pg.wait_for_timeout(200)
    ok(kut("!!document.querySelector('[data-dars]')", 15000) and pg.locator('[data-yana]').count() == 0 and "Dam olish vaqti tugadi" in pg.inner_text('body'), "Dam olish vaqti tugasa — o'yin yakunlanadi, faqat «▶ Darsga qaytish»")
    pg.click('[data-dars]'); pg.wait_for_timeout(250); ok(ev("window.__dn") == 2, "Darsga qaytdi")
    # chiqib ketish
    GO('dam-sinov', 300); ev(BOSH); pg.wait_for_timeout(200); ev("window.__bjOyin().sek = 60"); pg.click('[data-o="devor"]'); pg.wait_for_timeout(300); GO('uy', 1300)
    lz = X(K, "A.readLog(b.id, A.todayKey()).filter(e=>e.t==='zal' && e.tur==='devor').map(e=>[e.dam||0,e.erta])")
    ok(ev("window.__bjZal()") is None and ev("window.__bjOyin()") is None and [1, 1] in lz, f"O'yin paytida boshqa ekranga — ikkala seans yopiladi, log erta {lz}")
    # eski o'yin (pazl) ham shu tanlovdan
    ev(BOSH); pg.wait_for_timeout(200); pg.click('[data-o="pazl"]'); pg.wait_for_timeout(300)
    ok(ev("!!(window.__bjOyin() && window.__bjOyin().game && window.__bjOyin().tur==='pazl')") and pg.locator('.pzb').count() == 1, "🧩 Pazl maktabgacha bolaga ham ochiladi")
    ev("BJ.A.oyin.finish()"); pg.wait_for_timeout(300)
    if pg.locator('[data-dav]').count(): pg.click('[data-dav]'); pg.wait_for_timeout(200)
    ok(ev("window.__dn") == 3, "Pazl tugadi → darsga")
    # missiya ichida (oyinHar=1): savoldan keyin tanlov chiqadi
    setj(R); ev("(()=>{const b=BJ.A.bola(); b.oyinHar=1; b.oyinDaq=1; BJ.A.save(true)})()"); NAV('missiya', 700)
    for _ in range(20):
        if pg.locator('.damg').count(): break
        if ev("!!(window.__bjCur && __bjCur() && __bjCur().cb && document.querySelector('#body'))"): ev("window.__bjJavob(true)"); pg.wait_for_timeout(500); continue
        b = pg.locator('#app .btn.big, [data-next], [data-ok]')
        if b.count(): b.first.click(); pg.wait_for_timeout(400)
        else: pg.wait_for_timeout(200)
    ok(pg.locator('.damg .zcard').count() == 7, "Missiyada (2-sinf): savoldan keyin dam olish — 7 o'yin tanlovi")
    pg.click('[data-qayt]'); pg.wait_for_timeout(400)
    ok(ev("location.hash") == '#missiya' and pg.locator('.damg').count() == 0, "«↩ Darsga qaytish» → missiya davom etadi")
    ev("(()=>{const b=BJ.A.bola(); b.oyinHar=null; b.oyinDaq=null; BJ.A.save(true)})()")

    # ================= C) 🏆 REYTING (oila + reyting guruhi) =================
    wk = ev("BJ.A.isoWeek()")
    ev(f"""(()=>{{const s=BJ.A.S(); s.oilaTel=s.oilaTel||{{}}; s.oilaTel['G:udost']={{nom:"Do'st oila", guruh:1, wk:'{wk}', ts:Date.now(), bolalar:[
      {{id:'gb1', av:'🐻', laqab:'Dost', daraja:'g0', wkB:'{wk}', zal:{{r:{{turbo:[0.9,3], xotira:[1,2]}}, h:{{turbo:[0.9,3]}}, p:{{}}}}}},
      {{id:'gb2', av:'🐺', laqab:'Bori', daraja:'g2', wkB:'{wk}', zal:{{r:{{svetofor:[999,0]}}, h:{{}}, p:{{}}}}}}]}}; BJ.A.save(true)}})()""")
    setj(K); NAV('zal-rekord', 450); t = pg.inner_text('body')
    ok("Dost" in t and "Do'st oila" in t and 'Bori' in t, "🏆 Rekordlar: reyting guruhidagi boshqa oila bolalari ham (oila nomi bilan)")
    r = ev("[...document.querySelectorAll('.zrk')][0].innerText")
    ok('🥇' in r and r.index('Dost') < r.index('Kichik'), "Turbo (maktabgacha): boshqa oiladagi bola 0.9 s — 🥇, bizniki keyin")
    ok(pg.locator('.zrw.men').count() == 7 and pg.locator('.zrw.gr').count() >= 3, "O'z qatori (sen) har o'yinda, boshqa oila qatorlari ajratilgan")
    ok(W() <= 391, f"390 px: rekordlar ({W()})")
    SHOT(pg, 'reyting')
    gz = X(K, "A.zal.guruhZal(b)")
    ok(gz and set(gz) == {'r', 'h', 'p'} and 'turbo' in gz['r'] and 'xotira' in gz['h'] and isinstance(gz['r']['turbo'][0], (int, float)), f"guruhZal: {{r, h, p}} — guruhga yuboriladigan o'yin natijalari {gz and list(gz['r'])}")
    ok(X(Q, "A.zal.guruhZal(b)") is None, "O'ynamagan bola — zal maydoni yuborilmaydi (null)")

    # ================= D) 🧠 BILIM CHIPTASI =================
    setj(K); X(K, "(b.zal.ruxsat={}, A.agg(b).missiya=1, b.zal.sek[A.todayKey()]=599, A.save(true), 0)"); NAV('zal')
    ok(pg.locator('[data-chip]').count() == 0 and X(K, "A.zal.chiptaMumkin(b)") is False, "10 daqiqadan oldin chipta yo'q")
    X(K, "(b.zal.sek[A.todayKey()]=600, A.save(true), 0)"); NAV('zal')
    ok(pg.locator('[data-chip]').count() == 1, "10 daqiqa o'ynagandan keyin — 🎟️ Bilim chiptasi kartasi")
    q0 = X(K, "A.zal.qoldi(b)"); pg.click('[data-chip]'); pg.wait_for_timeout(350)
    it = ev("window.__bjChipta");
    ok(it and it['t'] == 'tanla' and pg.locator('.sheet .zchs .opt').count() >= 2 and ev("BJ.gen.reg[window.__bjChipta.tugun].fan") == 'mat', f"Chipta savoli — matematika, variantli ({it and it['tugun']} q{it and it['q']})")
    pg.locator(f'.sheet .opt[data-v="{it["a"]}"]').first.click(); pg.wait_for_timeout(300)
    r = X(K, "[b.zal.chipta[A.todayKey()].n, b.zal.chipta[A.todayKey()].ok, A.zal.bugunDaq(b)]")
    ok(r == [1, 1, 12] and "+2 daqiqa" in pg.inner_text('.sheet'), f"To'g'ri javob → zalga +2 daqiqa (10 → 12) {r}")
    ok(X(K, "A.zal.qoldi(b)") - q0 >= 119, "Qolgan vaqt 2 daqiqaga oshdi")
    pg.click('.sheet [data-dv]'); pg.wait_for_timeout(300)
    ok(X(K, "A.zal.chiptaMumkin(b)") is False, "Keyingi chipta — yana 10 daqiqadan keyin (20 daq)")
    X(K, "(b.zal.sek[A.todayKey()]=1200, A.save(true), 0)"); NAV('zal'); pg.click('[data-chip]'); pg.wait_for_timeout(300)
    it = ev("window.__bjChipta"); xv = ev("[...document.querySelectorAll('.sheet .opt')].map(e=>e.dataset.v).find(v=>v!==String(window.__bjChipta.a))")
    pg.locator(f'.sheet .opt[data-v="{xv}"]').first.click(); pg.wait_for_timeout(300)
    r = X(K, "[b.zal.chipta[A.todayKey()].n, b.zal.chipta[A.todayKey()].ok, A.zal.bugunDaq(b)]")
    ok(r == [2, 1, 12] and pg.locator('.sheet .opt.ok').count() == 1 and "Hechqisi yo'q" in pg.inner_text('.sheet'), f"Xato → jazosiz, to'g'ri javob ko'rsatiladi, vaqt o'zgarmaydi {r}")
    pg.click('.sheet [data-dv]'); pg.wait_for_timeout(250)
    X(K, "(b.zal.chipta[A.todayKey()].n=3, b.zal.sek[A.todayKey()]=4000, A.save(true), 0)")
    ok(X(K, "A.zal.chiptaMumkin(b)") is False, "Kuniga ko'pi bilan 3 ta chipta")
    X(K, "(b.zal.chipta[A.todayKey()].n=0, A.save(true), 0)"); ev("BJ.A.S().sozlama.zalChipta=false; BJ.A.save(true)")
    ok(X(K, "A.zal.chiptaMumkin(b)") is False, "⚙️ chipta o'chirilsa — chiqmaydi")
    ev("BJ.A.S().sozlama.zalChipta=true; BJ.A.save(true)")
    NAV('zal'); ok("tugadi" in pg.inner_text('body') and pg.locator('[data-chip]').count() == 1, "Zal vaqti tugagan ekranda ham chipta taklifi (+2 daqiqa)")
    SHOT(pg, 'chipta')
    lc = X(K, "A.readLog(b.id, A.todayKey()).filter(e=>e.hodisa==='chipta').map(e=>e.togri)")
    ok(lc == [1, 0], f"Log: {{t:'zal', hodisa:'chipta', togri}} {lc}")

    # ================= E) 📊 HAFTA XULOSASI — o'yin qatori =================
    X(K, "(A.agg(b).oyinSek=(A.agg(b).oyinSek||0)+125, A.save(true), 0)")
    m = X(K, "A.xulosa(b, A.isoWeek()).matn")
    ok("🎮 O'yinlar: zalda" in m and 'dam olishda' in m and 'yangi rekord' in m and 'Turbo gonka' in m, "📊 Hafta xulosasi: «🎮 O'yinlar: zalda N daq, dam olishda M daq · 🏆 yangi rekord: …»")
    ok("🎮 O'yinlar" not in X(Q, "A.xulosa(b, A.isoWeek()).matn"), "O'ynamagan bolada o'yin qatori yo'q")
    ok(not PE, f"A–E: JS xato yo'q {PE[:3]}"); PE.clear()

    # ================= F) 🏅 HAFTANING CHEMPIONI (soat: dushanba 16.11.2026, o'tgan hafta W46) =================
    c2 = br.new_context(viewport={'width': 390, 'height': 844}, service_workers='block'); pg2 = c2.new_page(); pg2.on('pageerror', lambda e: PE.append(f'F: {e}')); e2 = pg2.evaluate
    pg2.clock.set_fixed_time('2026-11-16T12:00:00')
    pg2.goto(URL + '?tez=1'); pg2.wait_for_timeout(400); pg2.fill('#on', 'Chemp'); pg2.fill('#p1', '1234'); pg2.fill('#p2', '1234'); pg2.click('#go'); pg2.wait_for_timeout(300)
    r = e2("""(()=>{const A=BJ.A, pw='2026-W46'; const k=A.newBola({laqab:'Kichik',daraja:'g0',avatar:'🐯',dunyo:'garaj'}), q=A.newBola({laqab:'Orta',daraja:'g1',avatar:'🦄',dunyo:'orol'}), q2=A.newBola({laqab:'Opa',daraja:'g1',avatar:'🦋',dunyo:'orol'});
      const s=A.S(); s.sozlama.uyqu=''; s.joriy=k.id;
      k.zal={rek:{},sek:{},son:{},guv:[],hb:{[pw]:{turbo:[5.2,3], xotira:[4,2]}}}; q.zal={rek:{},sek:{},son:{},guv:[],hb:{[pw]:{turbo:[3.1,3], svetofor:[150,0]}}}; q2.zal={rek:{},sek:{},son:{},guv:[],hb:{[pw]:{svetofor:[150,0]}}};
      s.guruh={kod:'ABCDEFGH23'}; s.oilaTel={'G:ux':{nom:'Boshqa', guruh:1, bolalar:[{id:'x1',av:'🐻',laqab:'Xbola',daraja:'g1',wkB:'2026-W47',zal:{r:{},h:{},p:{turbo:[2.9,3]}}}, {id:'x2',av:'🐺',laqab:'Ybola',daraja:'g0',wkB:'2026-W46',zal:{r:{},h:{turbo:[6.0,3]},p:{}}}]}};
      A.save(true); delete A.guruhOlindi; A.zal.chempHisob(); const a=k.zal.chemp; A.guruhOlindi=Date.now(); A.zal.chempHisob();
      return {kut: a===undefined, k: k.zal.chemp[pw].map(c=>[c.tur,c.ish]), q: q.zal.chemp[pw].map(c=>c.tur), q2: q2.zal.chemp[pw].map(c=>c.tur), guv: k.zal.guv.filter(g=>g.chemp).length, kids:[k.id,q.id]}})()""")
    ok(r['kut'], "Guruh ma'lumoti hali kelmagan (dushanba) — chempion keyinroq hisoblanadi")
    ok(sorted(r['k']) == [['turbo', 2], ['xotira', 1]], f"Maktabgacha: turbo (2 ishtirokchi: 5.2 s < boshqa oiladagi 6.0 s) va xotira — chempion {r['k']}")
    ok(r['q'] == ['svetofor'] and r['q2'] == ['svetofor'], f"1-sinf: turbo — boshqa oiladagi bola (2.9 s, o'tgan hafta «p») yutdi; svetofor teng — ikkalasi chempion {r['q']} {r['q2']}")
    ok(r['guv'] == 2, "Chempion guvohnomalari 📜 ro'yxatga qo'shildi")
    pg2.goto(URL + '?tez=1&r=1#uy'); pg2.wait_for_timeout(1300)
    ok(pg2.locator('.sheet .zchemp').count() == 1 and 'Haftaning chempioni' in pg2.inner_text('.sheet') and 'CHEMPION' in e2("document.querySelector('.sheet svg').outerHTML"), "Uyda bir marta bayram: «🏅 Haftaning chempioni» + CHEMPION guvohnomasi")
    pg2.screenshot(path='/tmp/bj076_chempion.png', full_page=True)
    pg2.goto(URL + '?tez=1&r=2#uy'); pg2.wait_for_timeout(1200)
    ok(pg2.locator('.sheet .zchemp').count() == 0, "Ikkinchi marta ko'rsatilmaydi")
    xm = e2(f"BJ.A.xulosa(BJ.A.S().bolalar['{r['kids'][0]}'], '2026-W46').matn")
    ok("haftaning chempioni" in xm, "📊 O'tgan hafta xulosasida «🏅 haftaning chempioni»")
    pg2.goto(URL + '?tez=1&r=3#zal-guv'); pg2.wait_for_timeout(500)
    ok(pg2.locator('.zgv.ch').count() == 2, "📜 Guvohnomalar: chempion guvohnomalari ajratilgan")
    c2.close()
    ok(not PE, f"F: JS xato yo'q {PE[:3]}"); PE.clear()

    # ================= G) ☁️ GURUH: zal maydoni (qoidalar) va admin «guruh» buyrug'i =================
    AD = tel(br, 'ADMIN'); oila(AD, 'Admin oila'); PUMP[0] = AD
    abid = AD.evaluate("""(()=>{const A=BJ.A; const b=A.newBola({laqab:'Ali',daraja:'g1',avatar:'🦊',dunyo:'garaj'}); b.zal={rek:{turbo:{v:4.2,n:3,sana:A.todayKey(),ts:Date.now(),gl:'g1'}},sek:{},son:{},guv:[],hb:{[A.isoWeek()]:{turbo:[4.2,3]}}}; A.S().sozlama.uyqu=''; A.save(true); return b.id})()""")
    ota(AD); AD.fill('#be', 'admin@test.uz'); AD.fill('#bp', 'parol123'); AD.click('[data-in]')
    ok(kutpy(lambda: 'oila/U_admintestuz' in STORE and f'oila/U_admintestuz/bolalar/{abid}' in STORE, 12000), "Admin oilasi bulutda")
    STORE['ruxsat/U_dosttestuz'] = {'email': 'dost@test.uz', 'oila': 'Dost oila', 'ts': 1, 'holat': 'ok'}
    JV = tel(br, 'DOST'); oila(JV, 'Dost oila')
    jbid = JV.evaluate("""(()=>{const A=BJ.A; const b=A.newBola({laqab:'Sabo',daraja:'g1',avatar:'🌸',dunyo:'orol'}); A.S().sozlama.uyqu=''; A.S().joriy=b.id; A.save(true); return b.id})()""")
    ota(JV); JV.fill('#be', 'dost@test.uz'); JV.fill('#bp', 'parol123'); JV.click('[data-in]')
    ok(kutpy(lambda: f'oila/U_dosttestuz/bolalar/{jbid}' in STORE, 12000), "Dost oilasi bulutda (ruxsat bor)")
    JV.goto(URL + '#uy'); JV.wait_for_timeout(600)
    # Dost telefonida mahalliy o'zgarish (hali bulutga yetmagan) — admin guruh qo'yadi: guruh yo'qolmasligi kerak
    JV.evaluate("window.__fsFail=true; BJ.A.S().sozlama.reyting=false; BJ.A.save(true)"); JV.wait_for_timeout(300)
    KOD = 'QWERTYUP23'; now = int(time.time() * 1000)
    with LOCK:   # admin.js «guruh» buyrug'i kabi
        STORE['guruh/' + KOD] = {'yaratdi': 'U_admintestuz', 'ts': now}
        for u in ('U_admintestuz', 'U_dosttestuz'):
            STORE[f'guruh/{KOD}/oilalar/{u}'] = {'ts': now}; o = STORE['oila/' + u]; j = json.loads(o['j']); j['guruh'] = {'kod': KOD, 'qoshildi': now}
            STORE['oila/' + u] = dict(o, j=json.dumps(j, ensure_ascii=False), ts=now, q='admin')
    ok(kutf(JV, f"(BJ.A.S().guruh||{{}}).kod==='{KOD}'", 8000), "Dost telefoni (mahalliy o'zgarish bor edi) admin qo'ygan guruhni oldi")
    ok(kutf(AD, f"(BJ.A.S().guruh||{{}}).kod==='{KOD}'", 8000), "Admin telefoni guruhni oldi")
    JV.evaluate("window.__fsFail=false")
    ok(kutpy(lambda: f'guruh/{KOD}/azo/{abid}' in STORE and 'zal' in STORE[f'guruh/{KOD}/azo/{abid}'], 15000), "Admin bolasining a'zo yozuvi «zal» maydoni bilan (qoidalar 0.7.6 — qabul qilindi)")
    ok(kutpy(lambda: f'guruh/{KOD}/azo/{jbid}' in STORE, 15000), "Dost bolasining a'zo yozuvi ham (o'ynamagan — zal maydonisiz)")
    ok(STORE.get(f'guruh/{KOD}/azo/{abid}', {}).get('zal', {}).get('r', {}).get('turbo') == [4.2, 3], f"zal.r.turbo = [4.2, 3] {STORE.get(f'guruh/{KOD}/azo/{abid}', {}).get('zal')}")
    ok(not [x for x in RAD if '/azo/' in x], f"Qoidalar hech bir a'zo yozuvini rad etmadi {RAD[:3]}")
    ok(all('bu' in STORE[k] and 'dz' in STORE[k] for k in STORE if f'guruh/{KOD}/azo/' in k), "0.9.0 qoidalari bilan a'zo yozuvida bu (bugun) va dz (daraxt %) bor — estafeta uchun")
    ok(kutpy(lambda: json.loads(STORE['oila/U_dosttestuz']['j']).get('guruh', {}).get('kod') == KOD and json.loads(STORE['oila/U_dosttestuz']['j']).get('sozlama', {}).get('reyting') is False, 12000),
       "Dost telefoni o'z o'zgarishini yubordi — bulutda guruh ham, mahalliy sozlama ham saqlandi")
    ok(kutf(JV, "Object.keys(BJ.A.S().oilaTel||{}).some(q=>q.indexOf('G:')===0 && (BJ.A.S().oilaTel[q].bolalar||[]).some(x=>x.zal && x.zal.r && x.zal.r.turbo))", 12000), "Dost telefoniga admin bolasining o'yin rekordi keldi")
    JV.goto(URL + '#zal-rekord'); JV.wait_for_timeout(700); t = JV.evaluate("document.body.innerText")
    ok('Ali' in t and 'Admin oila' in t and '4.2 s' in t, "Dost bolasi 🏆 Rekordlar ekranida boshqa oila bolasini ko'radi (Ali · Admin oila · 4.2 s)")
    JV.screenshot(path='/tmp/bj076_guruh.png', full_page=True)
    # ================= H) 👏 0.9.1: boshqa oila bolasiga olqish (guruh a'zo yozuvidagi «ol», qoidalar 0.9.1) =================
    ok(kutf(AD, f"Object.keys(BJ.A.S().oilaTel||{{}}).some(q=>(BJ.A.S().oilaTel[q].bolalar||[]).some(x=>x.id==='{jbid}'))", 12000), "Admin telefoni Dost bolasini guruhdan ko'radi")
    r = AD.evaluate(f"(()=>{{const A=BJ.A,b=A.bola('{abid}'); A.S().joriy=b.id; const y=A.olqish.yubor(b,{{id:'{jbid}',laqab:'Sabo',av:'🌸'}},2); A.save(true); A.bulutYubor(); return [y, A.olqish.bulut(b)]}})()")
    ok(r[0] is True and len(r[1]) == 1 and r[1][0].startswith(jbid + '|2|'), f"Ali → Sabo (boshqa oila): «🔥 Zo'r ketyapsan!» — bulut ro'yxatida {r[1]}")
    ok(kutpy(lambda: any(str(x).startswith(jbid + '|2|') for x in (STORE.get(f'guruh/{KOD}/azo/{abid}', {}).get('ol') or [])), 15000), "Admin bolasining a'zo yozuvida «ol» (qoidalar 0.9.1 qabul qildi)")
    ok(not [x for x in RAD if '/azo/' in x], f"«ol» bilan a'zo yozuvi rad etilmadi {RAD[:3]}")
    ok(kutf(JV, f"((BJ.A.bola('{jbid}').olq||{{}}).k||[]).some(k=>k.f==='{abid}' && k.i===2 && k.yangi)", 15000), "Dost telefonida Sabo olqishni oldi (faqat o'z bolasiga yozilgani)")
    JV.evaluate(f"(()=>{{BJ.A.S().joriy='{jbid}'; BJ.A.save(true); location.hash='x'; location.hash='uy'}})()"); JV.wait_for_timeout(700)
    t = JV.inner_text('.olqk') if JV.locator('.olqk').count() else ''
    ok('Ali' in t and "Zo'r ketyapsan" in t, f"Sabo uy ekranida: «Ali senga: 🔥 Zo'r ketyapsan!» ({t[:60]})")
    JV.screenshot(path='/tmp/bj076_olqish.png', full_page=True)
    ok(AD.evaluate(f"BJ.A.olqish.qabul('{jbid}', {{ol:['{abid}|0|'+Date.now(), 'yomon|9|1', '<b>|1|'+Date.now()]}}, new Set(['{abid}']))") == 1, "Qabul: noto'g'ri satrlar (ibora 9, HTML) tashlanadi, faqat o'z bolamizga yozilgani olinadi")
    ok(not PE, f"G: JS xato yo'q {PE[:3]}")
finally:
  srv.terminate()
print('\nJAMI XATO:', len(ERR)); [print(' -', e) for e in ERR]; sys.exit(1 if ERR else 0)
