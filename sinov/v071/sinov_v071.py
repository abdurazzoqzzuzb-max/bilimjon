"""Bilimjon 0.7.1 — 🤔 «Tushunmadim» + 🙋 «Ota-onamdan so'rayman» va 🛡️ ruxsat tizimi.
A) Tushunmadim: tugma (missiya, mashq, vazifa; arenada yo'q), soddaroq varaq, oson misol (joriy javob ochilmaydi), «maslahat» logi,
   so'rash ≤ 3, savol missiya/vazifa oxirida (mashqda 2 savoldan keyin, ?tez=1) qaytadi, ota-ona paneli 🔔, Bugungi qiyinlar matni,
   sozlama, 390 px, hamma generatorlar bo'yicha oson misol tekshiruvi.
B) Ruxsat: soxta Firebase + Python'da firestore.rules mantig'i (eski qoidalar / yangi qoidalar). Admin (yoqish kartasi, qoidalar matni
   ID bilan, admin telefoni), yangi oila (so'rov → kutish → ruxsat → bulut ulanadi), to'xtatish (sinxron to'xtaydi), admin 2-telefoni
   (tugmalar o'chiq), 🧪 sinov rejimi (oila ma'lumotiga hech narsa yozilmaydi, ruxsat paneli ishlaydi).
Ishga tushirish: python3 sinov/v071/sinov_v071.py  (skrinshotlar: /tmp/bj071_*.png)"""
import os, sys, time, subprocess, json, threading, shutil, tempfile
from playwright.sync_api import sync_playwright

D = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.abspath(os.path.join(D, '..', '..')); FAKE = os.path.join(SITE, 'sinov', 'bulut')
PORT, PORT2 = 8791, 8792; URL = f'http://localhost:{PORT}/'
TMP = tempfile.mkdtemp(prefix='bj071_')
shutil.copytree(SITE, os.path.join(TMP, 's'), ignore=shutil.ignore_patterns('.git', 'beta'))
subprocess.run([sys.executable, os.path.join(SITE, 'sinov', 'beta', 'beta_yig.py'), '.', os.path.join(TMP, 's', 'beta')], cwd=SITE, check=True, capture_output=True)
srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT)], cwd=SITE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
srv2 = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT2)], cwd=os.path.join(TMP, 's'), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)
ERR = []
def ok(c, m):
    print(('✅ ' if c else '❌ ') + m)
    if not c: ERR.append(m)
SHOT = lambda pg, n: pg.screenshot(path=f'/tmp/bj071_{n}.png', full_page=True)

# ---------------- soxta Firestore + firestore.rules mantig'i (Python) ----------------
STORE = {}; LOCK = threading.RLock(); RULES = {'on': False, 'admin': 'U_admintestuz'}; WRITES = []
def ruxsatli(uid): return uid == RULES['admin'] or (STORE.get('ruxsat/' + str(uid)) or {}).get('holat') == 'ok'
def sorov_togri(d, who):
    return set(d) <= {'email', 'oila', 'ts', 'holat'} and d.get('holat') == 'kutish' and d.get('email') == who.get('email') \
        and isinstance(d.get('oila'), str) and len(d['oila']) <= 24 and isinstance(d.get('ts'), int) and not isinstance(d.get('ts'), bool)
def ruxsat(op, path, who, new=None):
    uid = who.get('uid'); p = path.split('/'); adm = uid is not None and uid == RULES['admin']
    if p[0] == 'ruxsat':
        if not RULES['on'] or uid is None: return False
        if op == 'list': return adm
        if op == 'get': return uid == p[1] or adm
        if op == 'del': return adm
        if adm: return True
        old = STORE.get(path)
        return uid == p[1] and (old is None or old.get('holat') == 'kutish') and sorov_togri(new, who)
    if p[0] == 'oila':
        if uid is None or uid != p[1]: return False
        return op in ('get', 'list') or not RULES['on'] or ruxsatli(uid)
    if p[0] == 'guruh':
        return op in ('get', 'list', 'del') or uid is not None and (not RULES['on'] or ruxsatli(uid))
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
            STORE.pop(a[1], None); WRITES.append(('del', a[1], who.get('uid'))); return 'null'
        if op == 'set':
            path, data, merge = a[1], a[2], a[3]
            old = dict(STORE.get(path) or {}) if merge else {}
            for k, v in data.items():
                if isinstance(v, dict) and '__au' in v:
                    cur = list(old.get(k) or []); [cur.append(x) for x in v['__au'] if x not in cur]; old[k] = cur
                else: old[k] = v
            if not ruxsat('set', path, who, old): return json.dumps({'__err': 'permission-denied'})
            STORE[path] = old; WRITES.append(('set', path, who.get('uid'))); return 'null'
    return 'null'
FILES = {'firebase-app.js': 'export function initializeApp(c){return {c}}',
         'firebase-auth.js': open(os.path.join(FAKE, 'auth.js')).read(), 'firebase-firestore.js': open(os.path.join(FAKE, 'fs.js')).read()}

def tel(br, nom, url=URL, fake=True):
    ctx = br.new_context(viewport={'width': 390, 'height': 844}, service_workers='block')
    if fake:
        ctx.expose_function('__fs', fs)
        ctx.route('https://www.gstatic.com/firebasejs/**', lambda r: r.fulfill(status=200, content_type='text/javascript', body=FILES[r.request.url.split('/')[-1]]))
    pg = ctx.new_page(); pg.on('pageerror', lambda e: ERR.append(f'{nom} pageerror: {e}'))
    pg.goto(url); pg.wait_for_timeout(400); return pg
def oila(pg, nom):
    pg.fill('#on', nom); pg.fill('#p1', '1234'); pg.fill('#p2', '1234'); pg.click('#go'); pg.wait_for_timeout(300)
def kut(pg, js, ms=8000):
    try: pg.wait_for_function(js, timeout=ms); return True
    except Exception: return False
PUMP = [None]   # sync Playwright: soxta Firestore chaqiruvlari faqat Playwright kutayotganda ishlaydi — time.sleep emas, wait_for_timeout
def pump(ms): PUMP[0].wait_for_timeout(ms)
def kutpy(f, ms=10000):
    t = time.time()
    while time.time() - t < ms / 1000:
        with LOCK:
            if f(): return True
        pump(200)
    with LOCK: return bool(f())
TXT = lambda pg: pg.evaluate("document.body.innerText")

try:
  with sync_playwright() as p:
    br = p.chromium.launch()
    # ======================= A) 🤔 TUSHUNMADIM =======================
    pg = tel(br, 'A', URL + '?tez=1', fake=False); ev = pg.evaluate
    oila(pg, 'Sinov')
    K, O = ev("""(()=>{const A=BJ.A; const k=A.newBola({laqab:'Kichik',daraja:'g0',avatar:'🐯',dunyo:'garaj'}); const o=A.newBola({laqab:'Orta',daraja:'g1',avatar:'🐼',dunyo:'garaj'});
      [k,o].forEach(b=>{b.boshlandi='2026-10-28';}); A.S().sozlama.uyqu=''; A.S().joriy=o.id; A.save(true); return [k.id,o.id]})()""")
    X = lambda bid, e: ev(f"(()=>{{const A=BJ.A, b=A.S().bolalar['{bid}']; return {e}}})()")
    NV = [0]
    def NAV(h, ms=500, ota=False):
        NV[0] += 1; pg.goto(URL + f'?tez=1&r={NV[0]}#' + h)
        ev(("BJ.A.otaOk={rol:'admin',t:Date.now()}; " if ota else '') + 'BJ.A.render()'); pg.wait_for_timeout(ms)
    def kichikMissiya(bid, n=3):
        return X(bid, f"""(()=>{{const m=b.missiya=A.buildMission(b); const bl=m.steps.find(s=>s.k==='blok'&&s.fan==='mat')||m.steps.find(s=>s.k==='blok'); const y=m.steps.find(s=>s.k==='yakun')||{{k:'yakun'}};
          m.steps=[Object.assign({{}},bl,{{n:{n},olimp:0}}), Object.assign({{}}, m.steps.find(s=>s.k==='blok'&&s!==bl&&s.fan!==bl.fan)||bl, {{n:1, olimp:0}}), y]; m.si=0; m.res={{}}; m.cur=null; m.done=false; m.soraQ=[]; m.soraN=0; A.save(true); return m.steps.map(s=>s.k+':'+(s.fan||''))}})()""")
    def setj(bid): ev(f"(()=>{{const s=BJ.A.S(); s.joriy='{bid}'; BJ.A.save(true)}})()")
    CURIT = lambda: ev("(()=>{const c=BJ.A.CUR(); return c&&c.it?{sav:c.it.sav,a:String(c.it.a),tur:c.it.tur,tugun:c.it.tugun,t:c.it.t}:null})()")
    def javob(tog=True):   # javob → yangi topshiriq (yoki «Davom») chiqquncha kutiladi — bitta savolga ikki marta javob bo'lmasin
        ev("window.__jv = BJ.A.CUR() && BJ.A.CUR().it"); ev(f"window.__bjJavob({'true' if tog else 'false'})")
        kut(pg, "!BJ.A.CUR() || BJ.A.CUR().it !== window.__jv || !!document.querySelector('[data-next],[data-twin]')", 5000); pg.wait_for_timeout(120)
    kichikMissiya(O); NAV('missiya', 700)
    ok(pg.locator('[data-tush]').count() == 1, "A: missiya savolida «🤔 Tushunmadim» tugmasi bor")
    ok(pg.locator('.qrow [data-charch]').count() == 1, "A: «😴 Charchadim» ham o'sha qatorda")
    r = ev("(()=>{const q=document.querySelector('.qrow'); const R=[...q.querySelectorAll('.btn')].map(b=>b.getBoundingClientRect()); return [document.documentElement.scrollWidth, Math.max(...R.map(x=>x.right)), Math.min(...R.map(x=>x.left)), R.map(x=>x.height)]})()")
    ok(r[0] <= 390 and r[1] <= 390 and r[2] >= 0 and min(r[3]) >= 44, f"A: 390 px — qator sig'adi, tugma ≥44 px ({r})")
    SHOT(pg, '1_missiya')
    it0 = CURIT(); pg.click('[data-tush]'); pg.wait_for_timeout(500)
    ok(pg.locator('.scrim .tushs').count() == 1 and 'Keling, soddaroq' in TXT(pg), "A: «Keling, soddaroq» varag'i ochildi")
    ok(len(pg.locator('.tushs .dq').inner_text().strip()) > 10, "A: soddaroq tushuntirish matni bor")
    ex = ev("(()=>{const d=document.querySelector('.tushs .dsav'); return d?d.innerText:null})()")
    if ex is not None:
        ok(ex.strip() != it0['sav'].strip(), f"A: oson misol — boshqa savol («{ex[:30]}» ≠ «{it0['sav'][:30]}»)")
        jv = pg.locator('.tushs [data-tans]').inner_text()
        ok(('Javob: ' + it0['a']) not in jv.replace('✅ ', ''), f"A: misol javobi joriy savol javobi emas ({jv.strip()[:30]})")
    else: ok(False, 'A: mat savolida oson misol chiqmadi')
    SHOT(pg, '2_tushunmadim')
    lg = X(O, "A.readLog(b.id, A.todayKey()).filter(e=>e.t==='tush')")
    ok(len(lg) == 1 and lg[0]['tugun'] == it0['tugun'], "A: logda {t:'tush'} yozildi")
    pg.click('[data-tok]'); pg.wait_for_timeout(300)
    ok(pg.locator('.scrim').count() == 0 and CURIT()['sav'] == it0['sav'], "A: «Endi o'zim urinaman» — o'sha savolga qaytadi")
    javob(True)
    e = X(O, "A.readLog(b.id, A.todayKey()).filter(e=>e.t==='ans').pop()")
    ok(e and e['maslahat'] == 1 and e['togri_1'] == 1, "A: Tushunmadim'dan keyingi javob «maslahat bilan» (maslahat=1)")
    # --- so'rash ×3
    res0 = X(O, "(b.missiya.res[b.missiya.si]||[]).length")
    for i in range(1, 4):
        if not kut(pg, "!!document.querySelector('[data-tush]')", 4000): ok(False, f'A: {i}-so\'rash: tugma yo\'q'); break
        before = CURIT(); pg.click('[data-tush]'); pg.wait_for_timeout(300)
        pg.click('[data-sora]'); pg.wait_for_timeout(500)
        st = X(O, "[b.missiya.soraQ.length, (b.sora||[]).length, (b.missiya.res[b.missiya.si]||[]).length, b.missiya.si, b.missiya.steps[b.missiya.si].k]")
        ok(st[0] == i and st[1] == i and st[2] == res0, f"A: {i}-so'rash — navbatda {st[0]}, panelda {st[1]}, missiya hisobi o'zgarmadi")
        ok(CURIT() is not None and CURIT()['sav'] != before['sav'] or st[3] != 0, f"A: {i}-so'rash — o'rniga yangi savol")
    pg.click('[data-tush]'); pg.wait_for_timeout(300)
    ok(pg.locator('[data-sora]').count() == 0 and "marta so'rading" in TXT(pg), "A: 4-marta — «so'rayman» yo'q (missiyada ≤ 3)")
    pg.click('[data-tok]'); pg.wait_for_timeout(200)
    for _ in range(12):
        c = CURIT()
        if c and c['tur'] == 'sora': break
        if pg.locator('[data-next]').count(): pg.click('[data-next]'); pg.wait_for_timeout(300); continue
        javob(True)
    c = CURIT()
    ok(c and c['tur'] == 'sora', "A: blok tugagach so'ralgan savol qaytdi (yakundan oldin)")
    ok(pg.locator('.sorab').count() == 1 and 'Ota-ona bilan' in pg.locator('.top .ttl').inner_text(), "A: «🙋 Ota-ona bilan» sarlavhasi va belgi")
    ok(pg.locator('[data-tush]').count() == 0 and pg.locator('[data-charch]').count() == 0, "A: qaytgan savolda Tushunmadim/Charchadim yo'q")
    SHOT(pg, '3_sora_qaytdi')
    ss = X(O, "b.missiya.soraQ.map(q=>q.it.sav)")
    ok(c['sav'] == ss[0], "A: qaytgan savol — aynan so'ralgan savol")
    ids = X(O, "b.missiya.soraQ.map(q=>q.id)")
    SID = lambda i: kut(pg, f"BJ.A.CUR() && BJ.A.CUR().it && BJ.A.CUR().it.soraId==='{ids[i]}'", 4000)
    javob(True)                                                                       # 1-chi: to'g'ri
    ok(SID(1), "A: 2-so'ralgan savol keldi"); ev("BJ.A.CUR().cb({togri:false, javob:'?'})"); pg.wait_for_timeout(200); javob(True)   # 2-chi: 1 xato, keyin to'g'ri
    ok(SID(2), "A: 3-so'ralgan savol keldi"); javob(False)                           # 3-chi: yakuniy xato
    if pg.locator('[data-next]').count(): pg.click('[data-next]'); pg.wait_for_timeout(400)
    h = X(O, "b.sora.map(x=>[x.holat, x.ok1||0])")
    ok(h == [['yechdi', 1], ['yechdi', 0], ['qiyin', 0]], f"A: natijalar ota-ona paneli uchun yozildi {h}")
    m = X(O, "[b.missiya.si, b.missiya.steps[b.missiya.si] && b.missiya.steps[b.missiya.si].k, b.missiya.soraQ.every(q=>q.qaytdi), (b.missiya.res[0]||[]).length]")
    ok(m[1] == 'yakun' and m[2] and m[3] == 3, f"A: keyin — yakun poygasi, so'ralganlar missiya hisobiga qo'shilmadi {m}")
    # --- ota-ona paneli
    NAV('ota', 500, ota=True)
    ok('🙋 Bola savollari 🔔 3' in TXT(pg), "A: panel menyusida «🙋 Bola savollari 🔔 3»")
    NAV('ota-sora', 600, ota=True)
    ok(pg.locator('.sork').count() == 3 and pg.locator('.sork .sj').count() == 3, "A: 3 ta karta, har birida to'g'ri javob")
    t = TXT(pg); ok("Keyin o'zi yechdi" in t and 'Yana qiyin' in t and 'Kattalar uchun' in t and 'Tushunmadim (7 kun)' in t, "A: holatlar, kattalar uchun yechim va 7 kunlik Tushunmadim statistikasi")
    ok(ev("document.documentElement.scrollWidth") <= 390, "A: panel 390 px ga sig'adi")
    SHOT(pg, '4_ota_sora')
    pg.click('[data-sk]'); pg.wait_for_timeout(400)
    ok(X(O, "b.sora.filter(x=>x.kor).length") == 1 and pg.locator('[data-sk]').count() == 2, "A: «✅ Tushuntirdim» — belgilandi")
    NAV('ota', 400, ota=True); ok('🙋 Bola savollari 🔔 2' in TXT(pg), "A: 🔔 2 ga tushdi")
    NAV('ota-qiyin', 500, ota=True); q = pg.locator('textarea').input_value()
    ok('|tush=5|sora=3' in q and q.count('SORA|') == 3, "A: «Bugungi qiyinlar» matnida tush=5 (1 + 3 so'rash + 1), sora=3 va SORA| qatorlari")
    # --- mashq
    NAV('mashq-mat', 600)
    ok(pg.locator('[data-tush]').count() == 1 and pg.locator('[data-charch]').count() == 0, "A: mashqda Tushunmadim bor (Charchadim yo'q)")
    m0 = CURIT(); pg.click('[data-tush]'); pg.wait_for_timeout(300); pg.click('[data-sora]'); pg.wait_for_timeout(500)
    ok(ev("BJ.A.CUR().soraQ.length") == 1 and X(O, "A.agg(b).soraM") == 1, "A: mashqda so'raldi (kunlik hisob soraM=1)")
    javob(True); javob(True)
    c = CURIT(); ok(c and c['tur'] == 'sora' and c['sav'] == m0['sav'] and pg.locator('.sorab').count() == 1, "A: mashqda 2 savoldan keyin qaytdi (?tez=1)")
    javob(True); ok(X(O, "b.sora[b.sora.length-1].holat") == 'yechdi' and ev("BJ.A.CUR().n") == 2, "A: mashq hisobi (n) so'ralgan savolni sanamaydi")
    # --- uyga vazifa
    X(O, "(b.vazifa=b.vazifa||[]).push({id:'vz1', berildi:A.todayKey(), muddat:A.todayKey(), fan:'mat', bolim:null, n:2, izoh:'', qildi:0, ok:0, done:false}), A.save(true), 1")
    NAV('vazifa-vz1', 600)
    v0 = CURIT(); pg.click('[data-tush]'); pg.wait_for_timeout(300)
    ok("vazifa oxirida" in TXT(pg), "A: vazifada «vazifa oxirida qaytadi» yozuvi")
    pg.click('[data-sora]'); pg.wait_for_timeout(500); javob(True); javob(True)
    c = CURIT(); ok(c and c['tur'] == 'sora' and c['sav'] == v0['sav'], "A: vazifa savollari tugagach so'ralgan savol qaytdi")
    javob(True); pg.wait_for_timeout(300)
    ok('Uyga vazifa bajarildi' in TXT(pg) and X(O, "b.vazifa[0].qildi") == 2, "A: keyin vazifa yakuni, hisob 2/2 (3 emas)")
    # --- mashq + vazifa kunlik chegarasi: 3
    NAV('mashq-mat', 500); pg.click('[data-tush]'); pg.wait_for_timeout(300); pg.click('[data-sora]'); pg.wait_for_timeout(400)
    pg.click('[data-tush]'); pg.wait_for_timeout(300)
    ok(pg.locator('[data-sora]').count() == 0, "A: mashq+vazifada kuniga 3 ta so'rash (4-si yo'q)")
    pg.click('[data-tok]')
    # --- arena, sozlama, g0
    NAV('arena', 500); ok(pg.locator('[data-tush]').count() == 0, "A: arenada Tushunmadim yo'q")
    ev("BJ.A.S().sozlama.tush=false; BJ.A.save(true)"); kichikMissiya(O); NAV('missiya', 500)
    ok(pg.locator('[data-tush]').count() == 0 and pg.locator('[data-charch]').count() == 1, "A: ⚙️ sozlamada o'chirilsa — tugma yo'q")
    ev("BJ.A.S().sozlama.tush=true; BJ.A.save(true)")
    NAV('ota-sozlama', 400, ota=True); ok(pg.locator('#tu').is_checked(), "A: ⚙️ «Tushunmadim» katagi bor")
    setj(K); kichikMissiya(K); NAV('missiya', 600)
    if pg.locator('[data-tush]').count():
        pg.click('[data-tush]'); pg.wait_for_timeout(400); ok("Kattalar o'qib bersin" in TXT(pg), "A: maktabgacha — «Kattalar o'qib bersin»"); SHOT(pg, '5_g0'); pg.click('[data-tok]')
    else: ok(False, 'A: g0 missiyasida Tushunmadim yo\'q')
    # --- hamma generatorlar: oson misol to'g'ri, javob ochilmaydi, matnlar toza
    sw = ev("""(()=>{const A=BJ.A, T=A.tushSinov, reg=BJ.gen.reg, S=A.S(), out={n:0, misol:0, kino:0, xato:[], bosh:[]};
      for (const bid of S.tartib) { const b=S.bolalar[bid];
        for (const id of Object.keys(reg)) for (const q of [1,2,3]) { let it; try { it=A.makeItem(b,{tugun:id,q,tur:'missiya'}); } catch(e){ continue; } if (!it || it.tugun!==id) continue;
          const sl=T.soddaLines(b,it); if (!sl.length || sl.some(x=>typeof x!=='string' || /undefined|NaN|null/.test(x))) out.xato.push('sodda '+id+' '+sl.join('|'));
          if (!(it.t==='tanla'||it.t==='yoz')) continue; out.n++;
          const om=T.osonMisol(b,it); if (!om) { if (typeof it.matn!=='string' && !['KASHF','OL'].includes(id)) out.bosh.push(id); continue; } out.misol++;
          if (om.tugun!==id || String(om.a)===String(it.a) || typeof om.matn==='string' || (om.sig && it.sig ? om.sig===it.sig : (om.sav===it.sav && om.tts===it.tts && JSON.stringify(om.vis||0)===JSON.stringify(it.vis||0)))) out.xato.push('misol '+id+' q'+q);
          const e1=it.ex||{}, e2=om.ex||{}; if (e1.a!=null && e1.b!=null && e2.a!=null && e2.b!=null && isFinite(+e1.a) && isFinite(+e2.a)) { const K=e=>Math.max(+e.a,+e.b,e.op==='+'?(+e.a)+(+e.b):+e.a); if (K(e1)>=6) { out.son=(out.son||0)+1; if (K(e2)<=K(e1)) out.oson=(out.oson||0)+1; else (out.katta=out.katta||[]).push(id+': '+it.sav+' → '+om.sav); } }
          try { if (A.kino(b,om)) out.kino++; } catch(e) { out.xato.push('kino '+id+' '+e.message); } } }
      out.bosh=[...new Set(out.bosh)]; return out})()""")
    ok(not sw['xato'], f"A: {sw['n']} ta tanla/yoz topshirig'i — oson misol va soddaroq matnda xato yo'q {sw['xato'][:5]}")
    ok(sw.get('oson', 0) >= 0.8 * sw.get('son', 1),  # qolganlari — joriy savol tugunning eng kichik sonlarida (masalan 10 + 10): misol shu ko'nikma, o'xshash kattalikda
        f"A: sonli misollarning (joriy son ≥ 6) {sw.get('oson')}/{sw.get('son')} tasida misol joriy savoldan katta emas {(sw.get('katta') or [])[:12]}")
    ok(sw['misol'] >= 0.8 * sw['n'], f"A: oson misol {sw['misol']}/{sw['n']} topshiriqda ({sw['kino']} tasi rasmli kino); misolsiz tugunlar: {sw['bosh'][:12]}")
    pg.context.close()

    # ======================= B) 🛡️ RUXSAT TIZIMI =======================
    AD = tel(br, 'ADMIN'); oila(AD, 'Admin oila'); PUMP[0] = AD
    abid = AD.evaluate("(()=>{const b=BJ.A.newBola({laqab:'Ali',daraja:'g1',avatar:'🦊'}); BJ.A.save(true); return b.id})()")
    AD.evaluate("BJ.A.otaOk={rol:'admin',t:Date.now()}"); AD.goto(URL + '#ota-bulut'); AD.wait_for_timeout(500)
    AD.fill('#be', 'admin@test.uz'); AD.fill('#bp', 'parol123'); AD.click('[data-in]')
    ok(kutpy(lambda: 'oila/U_admintestuz' in STORE), "B: eski qoidalar — admin oilasi bulutga yozildi (0.7.0 dagidek)")
    ok(kut(AD, "document.body.innerText.includes('Ruxsat tizimi — yoqilmagan')"), "B: «🛡️ Ruxsat tizimi — yoqilmagan» kartasi")
    ok(kut(AD, "(document.querySelector('[data-rxt]')||{}).value && document.querySelector('[data-rxt]').value.includes('U_admintestuz')"), "B: qoidalar matniga akkaunt ID si qo'yildi")
    qt = AD.evaluate("document.querySelector('[data-rxt]').value")
    ok('__ADMIN_UID__' not in qt and qt.count("'U_admintestuz'") == 1 and 'match /ruxsat/{uid}' in qt, "B: matnda joy qolmadi, admin() da 1 marta, ruxsat bo'limi bor")
    SHOT(AD, '6_yoqish')
    RULES['on'] = True
    AD.click('[data-rxk]'); ok(kut(AD, "document.body.innerText.includes('Ruxsatlar') && document.body.innerText.includes('siz — admin')"), "B: yangi qoidalar → «🔄 Tekshirish» → «Siz — admin»")
    ok("Hali so'rov yo'q" in TXT(AD) and AD.locator('[data-rxtel]').count() == 1, "B: so'rov yo'q; «📱 Shu telefon — admin telefoni» tugmasi")
    AD.click('[data-rxtel]'); AD.wait_for_timeout(200); AD.click('.scrim [data-ok]'); AD.wait_for_timeout(400)
    ok(AD.evaluate("BJ.A.S().adminTel && BJ.A.S().adminTel.q===BJ.A.S().qurilma.id") and 'shu telefon' in TXT(AD), "B: admin telefoni belgilandi")
    AD.evaluate(f"(()=>{{const b=BJ.A.S().bolalar['{abid}']; b.yulduz=7; BJ.A.save(true)}})()")
    ok(kutpy(lambda: '"yulduz":7' in (STORE.get(f'oila/U_admintestuz/bolalar/{abid}') or {}).get('j', ''), 9000), "B: yangi qoidalarda admin oilasi sinxroni ishlayapti")
    # --- yangi oila
    YA = tel(br, 'YANGI'); oila(YA, 'Yangi oila')
    ybid = YA.evaluate("(()=>{const b=BJ.A.newBola({laqab:'Vali',daraja:'g1',avatar:'🐼'}); BJ.A.save(true); return b.id})()")
    YA.evaluate("BJ.A.otaOk={rol:'admin',t:Date.now()}"); YA.goto(URL + '#ota-bulut'); YA.wait_for_timeout(500)
    YA.fill('#be', 'yangi@test.uz'); YA.fill('#bp', 'parol123'); YA.click('[data-up]')
    ok(kut(YA, "document.body.innerText.includes('Ruxsat kerak')"), "B: yangi oila — «🛡️ Ruxsat kerak»")
    pump(1500)
    ok(not any(k.startswith('oila/U_yangitestuz') for k in STORE), "B: ruxsatsiz — bulutga hech narsa yozilmadi")
    ok(YA.locator('#rxn').input_value() == 'Yangi oila', "B: oila nomi o'zi to'ldi")
    SHOT(YA, '7_ruxsat_kerak')
    YA.click('[data-rxq]')
    ok(kutpy(lambda: (STORE.get('ruxsat/U_yangitestuz') or {}).get('holat') == 'kutish'), "B: so'rov yozildi (holat: kutish)")
    d = STORE.get('ruxsat/U_yangitestuz') or {}
    ok(d.get('email') == 'yangi@test.uz' and d.get('oila') == 'Yangi oila' and set(d) == {'email', 'oila', 'ts', 'holat'}, f"B: so'rov maydonlari qoidaga mos {sorted(d)}")
    ok(kut(YA, "document.body.innerText.includes('Ruxsat kutilmoqda')"), "B: «⏳ Ruxsat kutilmoqda»")
    YA.evaluate("BJ.A.otaOk={rol:'admin',t:Date.now()}"); YA.goto(URL + '#ota'); YA.wait_for_timeout(400)
    ok('☁️ Oila akkaunti ⏳' in TXT(YA), "B: yangi oila menyusida ⏳ belgisi")
    YA.goto(URL + '#ota-bulut'); YA.wait_for_timeout(600)
    # o'zini tasdiqlay olmaydi (qoida)
    selfok = YA.evaluate("""(async()=>{try{ const m=await import('https://www.gstatic.com/firebasejs/13.2.0/firebase-firestore.js'); await m.setDoc(m.doc({},'ruxsat','U_yangitestuz'),{email:'yangi@test.uz',oila:'X',ts:Date.now(),holat:'ok'}); return 'yozildi'; }catch(e){ return e.code; }})()""")
    ok(selfok == 'permission-denied' and STORE['ruxsat/U_yangitestuz']['holat'] == 'kutish', "B: o'ziga «ok» yozolmaydi")
    # admin ko'radi
    ok(kut(AD, "document.body.innerText.includes('yangi@test.uz')", 6000), "B: admin ro'yxatida yangi so'rov (jonli)")
    ok(AD.locator('[data-rxa="ok|U_yangitestuz"]').is_enabled(), "B: admin telefonida «✅ Ruxsat berish» faol")
    SHOT(AD, '8_admin_royxat')
    AD.goto(URL + '#ota'); AD.wait_for_timeout(400); ok('☁️ Oila akkaunti 🔔 1' in TXT(AD), "B: admin menyusida 🔔 1")
    AD.goto(URL + '#ota-bulut'); AD.wait_for_timeout(800)
    AD.click('[data-rxa="ok|U_yangitestuz"]')
    ok(kutpy(lambda: (STORE.get('ruxsat/U_yangitestuz') or {}).get('holat') == 'ok'), "B: ruxsat berildi (holat: ok)")
    ok(kutpy(lambda: 'oila/U_yangitestuz' in STORE and f'oila/U_yangitestuz/bolalar/{ybid}' in STORE, 10000), "B: yangi oila o'zi bulutga ulandi (oila + bola)")
    ok(kut(YA, "document.body.innerText.includes('Ulangan')"), "B: yangi oila ekranida «✅ Ulangan»")
    # to'xtatish
    AD.wait_for_timeout(600); AD.click('[data-rxa="blok|U_yangitestuz"]'); AD.wait_for_timeout(200); AD.click('.scrim [data-ok]')
    ok(kutpy(lambda: (STORE.get('ruxsat/U_yangitestuz') or {}).get('holat') == 'blok'), "B: admin «🚫 To'xtatish»")
    YA.evaluate(f"(()=>{{const b=BJ.A.S().bolalar['{ybid}']; b.yulduz=9; BJ.A.save(true)}})()")
    ok(kut(YA, "document.body.innerText.includes(\"Bulut to'xtatilgan\")", 12000), "B: yangi oila — keyingi yozishda «🚫 Bulut to'xtatilgan»")
    ok('"yulduz":9' not in STORE[f'oila/U_yangitestuz/bolalar/{ybid}']['j'], "B: to'xtatilgandan keyin ma'lumot yozilmadi")
    n0 = len([w for w in WRITES if w[2] == 'U_yangitestuz']); pump(7000)
    ok(len([w for w in WRITES if w[2] == 'U_yangitestuz']) == n0, "B: sinxron to'xtadi (7 s da yangi urinish yo'q)")
    AD.click('[data-rxa="ok|U_yangitestuz"]')
    ok(kutpy(lambda: '"yulduz":9' in STORE[f'oila/U_yangitestuz/bolalar/{ybid}']['j'], 12000), "B: qayta ruxsat → sinxron o'zi tiklandi")
    # admin 2-telefoni (oyisi): ro'yxat ko'rinadi, tugmalar o'chiq
    A2 = tel(br, 'ADMIN2'); A2.goto(URL + '#bulut'); A2.wait_for_timeout(500)
    A2.fill('#be', 'admin@test.uz'); A2.fill('#bp', 'parol123'); A2.click('[data-in]')
    kut(A2, "BJ.A.S().oila && BJ.A.S().adminTel", 8000)
    A2.evaluate("BJ.A.otaOk={rol:'admin',t:Date.now()}"); A2.goto(URL + '#ota-bulut'); A2.wait_for_timeout(600)
    ok(kut(A2, "document.body.innerText.includes('yangi@test.uz')", 6000) and not A2.locator('[data-rxa="blok|U_yangitestuz"]').is_enabled(), "B: admin 2-telefoni — ro'yxat bor, tugmalar o'chiq")
    ok('faqat admin telefonida' in TXT(A2), "B: «Ruxsat faqat admin telefonida beriladi» yozuvi")
    SHOT(A2, '9_admin2')
    # 🧪 sinov rejimi (beta): oila ma'lumoti bulutga yozilmaydi, ruxsat paneli ishlaydi
    BU = f'http://localhost:{PORT2}/'
    BT = tel(br, 'BETA', BU); oila(BT, 'Beta oila'); btb = BT.evaluate("(()=>{const b=BJ.A.newBola({laqab:'Beta',daraja:'g1',avatar:'🐼'}); BJ.A.save(true); return b.id})()")
    BT.goto(BU + 'beta/'); BT.wait_for_timeout(500); BT.fill('#bpin', '1234'); BT.click('[data-ok]'); BT.wait_for_timeout(300); BT.click('[data-nus]'); BT.wait_for_timeout(700)
    ok(BT.evaluate("BJ.A.BETA && BJ.A.VER") == '0.7.1', "B: 🧪 beta ochildi (v7.1)")
    w0 = len([w for w in WRITES if w[1].startswith('oila/')])
    BT.evaluate("BJ.A.otaOk={rol:'admin',t:Date.now()}"); BT.goto(BU + 'beta/#ota-bulut'); BT.wait_for_timeout(600)
    ok('Sinov rejimi' in TXT(BT) and BT.locator('#be').count() == 1, "B: beta ☁️ — kirish va sinov izohi")
    BT.fill('#be', 'admin@test.uz'); BT.fill('#bp', 'parol123'); BT.click('[data-in]')
    ok(kut(BT, "document.body.innerText.includes('Ruxsatlar') && document.body.innerText.includes('yangi@test.uz')", 8000), "B: beta'da admin ruxsat paneli ishlaydi")
    ok(BT.evaluate("BJ.A.S().bolalar['" + btb + "'] ? 1 : 0") == 1, "B: beta'da nusxa olingan bola bor")
    BT.evaluate("(()=>{const s=BJ.A.S(); s.bolalar['" + btb + "'].yulduz=99; BJ.A.save(true)})()"); BT.wait_for_timeout(7500)
    ok(not any(btb in w[1] for w in WRITES) and not any(btb in k for k in STORE), "B: beta oila ma'lumotini bulutga YOZMADI (bola hujjati yo'q)")
    ok(not any('"yulduz":99' in (v.get('j') or '') for k, v in STORE.items() if k.startswith('oila/')), "B: bulutda beta o'zgarishi yo'q")
    SHOT(BT, '10_beta')
    br.close()
finally:
    srv.terminate(); srv2.terminate(); shutil.rmtree(TMP, ignore_errors=True)
print('\nNATIJA:', 'HAMMASI O\'TDI ✅' if not ERR else f'{len(ERR)} ta xato ❌'); [print(' -', e) for e in ERR]
sys.exit(1 if ERR else 0)
