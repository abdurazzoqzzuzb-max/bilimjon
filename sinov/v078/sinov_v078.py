"""Bilimjon 0.7.8 — 🏆 admin: ⚙️ Sozlamalar va 📲 Oila reytingida «Oilalar reyting guruhi» — oilani bir tugma bilan guruhga qo'shish.
Admin oila/{uid}.j.guruh + q:'admin' yozadi; qo'shilgan oila telefoni guruhni oladi va guruh/{kod}/oilalar/{uid} ni O'ZI yozadi
(qoidalar o'zgarmagan — soxta Firebase'da oilalar yozuvi faqat egasiga ruxsat etilgan), eski guruhdagi yozuvlarini o'chiradi.
Ishga tushirish: python3 sinov/v078/sinov_v078.py  (skrinshotlar: /tmp/bj078_*.png)"""
import os, sys, time, subprocess, json, threading
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.abspath(os.path.join(D, '..', '..')); FAKE = os.path.join(SITE, 'sinov', 'bulut')
PORT = 8808; URL = f'http://localhost:{PORT}/'
srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT)], cwd=SITE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
ERR = []; PE = []
def ok(c, m): print(('✅ ' if c else '❌ ') + m); (None if c else ERR.append(m))

# ---------- soxta Firebase: qoidalar 0.7.7 ga yaqin (guruh/{kod}/oilalar/{uid} — faqat egasi yozadi va o'chiradi) ----------
STORE = {}; LOCK = threading.RLock(); ADM = 'U_admintestuz'; RAD = []
AZO = {'uid', 'oila', 'av', 'laqab', 'daraja', 'yulduz', 'kun', 'osish', 'detal', 'missiya', 'wk', 'ts', 'zal'}
def ruxsatli(uid): return uid == ADM or (STORE.get('ruxsat/' + str(uid)) or {}).get('holat') == 'ok'
def ruxsat(op, path, who, new=None):
    uid = who.get('uid'); p = path.split('/'); adm = uid == ADM
    if uid is None: return False
    if p[0] in ('ruxsat', 'ilova'): return op != 'list' or adm
    if p[0] == 'oila':
        if adm: return True
        if len(p) < 2 or uid != p[1]: return False
        return op in ('get', 'list') or ruxsatli(uid)
    if p[0] == 'guruh':
        azomi = len(p) > 1 and ('guruh/%s/oilalar/%s' % (p[1], uid)) in STORE
        if op in ('get', 'list'): return azomi or len(p) <= 2
        if len(p) == 2: return op == 'set' and ruxsatli(uid)
        if p[2] == 'oilalar':
            if op == 'del': return uid == p[3]
            return uid == p[3] and ruxsatli(uid) and ('guruh/' + p[1]) in STORE and set(new) <= {'ts'}
        if p[2] == 'azo':
            if op == 'del': return (STORE.get(path) or {}).get('uid') == uid
            return azomi and ruxsatli(uid) and set(new) <= AZO and new.get('uid') == uid
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
            if not ruxsat('del', a[1], who): RAD.append(('del', a[1], who.get('uid'))); return json.dumps({'__err': 'permission-denied'})
            STORE.pop(a[1], None); return 'null'
        if op == 'set':
            path, data, merge = a[1], a[2], a[3]; old = dict(STORE.get(path) or {}) if merge else {}
            for k, v in data.items():
                if isinstance(v, dict) and '__au' in v: cur = list(old.get(k) or []); [cur.append(x) for x in v['__au'] if x not in cur]; old[k] = cur
                else: old[k] = v
            if not ruxsat('set', path, who, old): RAD.append(('set', path, who.get('uid'))); return json.dumps({'__err': 'permission-denied'})
            STORE[path] = old; return 'null'
    return 'null'
FILES = {'firebase-app.js': 'export function initializeApp(c){return {c}}', 'firebase-auth.js': open(os.path.join(FAKE, 'auth.js')).read(), 'firebase-firestore.js': open(os.path.join(FAKE, 'fs.js')).read()}
def tel(br, nom):
    ctx = br.new_context(viewport={'width': 390, 'height': 844}, service_workers='block', device_scale_factor=2); ctx.expose_function('__fs', fs)
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
def ota(pg, h='#ota-bulut'): pg.evaluate("BJ.A.otaOk={rol:'admin',t:Date.now()}"); pg.goto(URL + h); pg.wait_for_timeout(600)
def bola(pg, laqab, av):
    return pg.evaluate(f"""(()=>{{const A=BJ.A; const b=A.newBola({{laqab:'{laqab}',daraja:'g1',avatar:'{av}',dunyo:'garaj'}}); A.S().sozlama.uyqu=''; A.S().joriy=b.id; A.save(true); return b.id}})()""")
def jg(u): return json.loads(STORE['oila/' + u]['j']).get('guruh') or {}

try:
  with sync_playwright() as p:
    br = p.chromium.launch()
    STORE['ruxsat/U_dosttestuz'] = {'email': 'dost@test.uz', 'oila': 'Dost oila', 'ts': 1, 'holat': 'ok'}
    STORE['ruxsat/U_yangitestuz'] = {'email': 'yangi@test.uz', 'oila': 'Yangi oila', 'ts': 2, 'holat': 'kutish'}
    AD = tel(br, 'ADMIN'); PUMP[0] = AD; oila(AD, 'Admin oila'); abid = bola(AD, 'Aziz', '🦊')
    ota(AD); AD.fill('#be', 'admin@test.uz'); AD.fill('#bp', 'parol123'); AD.click('[data-in]')
    ok(kutpy(lambda: f'oila/{ADM}/bolalar/{abid}' in STORE, 12000), "Admin oilasi bulutda")
    DS = tel(br, 'DOST'); oila(DS, 'Dost oila'); dbid = bola(DS, 'Lola', '🌸')
    ota(DS); DS.fill('#be', 'dost@test.uz'); DS.fill('#bp', 'parol123'); DS.click('[data-in]')
    ok(kutpy(lambda: f'oila/U_dosttestuz/bolalar/{dbid}' in STORE, 12000), "Dost oilasi bulutda (ruxsat bor)")
    DS.goto(URL + '#uy'); DS.wait_for_timeout(500)
    # Dost avval boshqa (eski) guruhda — admin.js uslubida
    ESKI = 'ESK2ESK2ES'; now = int(time.time() * 1000)
    with LOCK:
        STORE['guruh/' + ESKI] = {'yaratdi': 'U_dosttestuz', 'ts': now}; STORE[f'guruh/{ESKI}/oilalar/U_dosttestuz'] = {'ts': now}
        o = STORE['oila/U_dosttestuz']; j = json.loads(o['j']); j['guruh'] = {'kod': ESKI, 'qoshildi': now}; STORE['oila/U_dosttestuz'] = dict(o, j=json.dumps(j), ts=now, q='admin')
    ok(kutpy(lambda: f'guruh/{ESKI}/azo/{dbid}' in STORE, 15000), "Dost eski guruhda a'zo (boshlang'ich holat)")

    # ---- A) ⚙️ Sozlamalar — admin kartasi ----
    ota(AD, '#ota-sozlama'); t = AD.evaluate("document.body.innerText")
    ok('Oilalar reyting guruhi' in t and AD.locator('#gadw [data-gal]').count() == 1, "⚙️ Sozlamalar: admin uchun «🏆 Oilalar reyting guruhi» kartasi")
    ok("hali yo'q" in t, "Admin guruhi yo'q — «birinchi oilani qo'shganda o'zi yaratiladi»")
    AD.fill('#onm', 'Admin oila 2')   # saqlanmagan forma — karta yangilanganda yo'qolmasin
    AD.click('#gadw [data-gal]'); ok(kutf(AD, "document.querySelectorAll('#gadw .rxi').length===2", 6000), "Oilalar ro'yxati: 2 ta boshqa oila (o'zi yo'q)")
    ok(AD.input_value('#onm') == 'Admin oila 2', "Karta yangilanganda sozlamalar formasi o'zgarmadi")
    t = AD.inner_text('#gadw')
    ok('Dost oila' in t and 'boshqa guruhda' in t and AD.locator('#gadw [data-gaq]').count() == 1, "Dost oila — «➕ Guruhga qo'shish» (boshqa guruhda)")
    ok('Yangi oila' in t and 'ruxsat kutyapti' in t, "Yangi oila — «⏳ ruxsat kutyapti», tugma yo'q")
    AD.screenshot(path='/tmp/bj078_admin_sozlama.png')
    AD.click('#gadw [data-gaq]'); AD.wait_for_timeout(300); ok(AD.locator('.sheet [data-ok]').count() == 1, "Tasdiqlash oynasi")
    AD.click('.sheet [data-ok]')
    ok(kutf(AD, "!!(BJ.A.S().guruh||{}).kod", 6000), "Admin guruhi o'zi yaratildi")
    KOD = AD.evaluate("BJ.A.S().guruh.kod")
    ok(kutpy(lambda: jg('U_dosttestuz').get('kod') == KOD and STORE['oila/U_dosttestuz'].get('q') == 'admin', 8000), "Bulutda Dost oilasi: j.guruh = admin kodi, q:'admin'")
    ok(kutf(AD, "document.querySelector('#gadw') && document.querySelector('#gadw').innerText.includes('guruhda') && !document.querySelector('#gadw [data-gaq]')", 6000), "Kartada: «🏆 guruhda»")
    AD.screenshot(path='/tmp/bj078_admin_qoshildi.png')
    # ---- B) Dost telefoni o'zi ulanadi ----
    ok(kutf(DS, f"(BJ.A.S().guruh||{{}}).kod==='{KOD}'", 10000), "Dost telefoni yangi guruhni oldi")
    ok(kutpy(lambda: f'guruh/{KOD}/oilalar/U_dosttestuz' in STORE, 10000), "guruh/KOD/oilalar/Dost — Dost telefonining O'ZI yozdi (qoidalar o'zgarmagan)")
    ok(kutpy(lambda: f'guruh/{KOD}/azo/{dbid}' in STORE, 15000), "Dost bolasining a'zo yozuvi yangi guruhda")
    ok(kutpy(lambda: f'guruh/{ESKI}/oilalar/U_dosttestuz' not in STORE and f'guruh/{ESKI}/azo/{dbid}' not in STORE, 10000), "Eski guruhdan Dost yozuvlari olib tashlandi")
    ok(kutf(AD, "Object.keys(BJ.A.S().oilaTel||{}).some(q=>q.indexOf('G:')===0 && (BJ.A.S().oilaTel[q].bolalar||[]).some(x=>x.laqab==='Lola'))", 15000), "Admin telefoniga Dost bolasi (Lola) reytingda keldi")
    ok(kutf(DS, "Object.keys(BJ.A.S().oilaTel||{}).some(q=>q.indexOf('G:')===0 && (BJ.A.S().oilaTel[q].bolalar||[]).some(x=>x.laqab==='Aziz'))", 15000), "Dost telefoniga admin bolasi (Aziz) keldi")
    # 0.9.0: bu sinovda Firebase'da hali ESKI qoidalar (0.7.7) — ilova bu/dz maydonli yozuv rad etilsa, ularsiz qayta yozadi
    rad_oil = [r for r in RAD if '/oilalar/' in r[1]]; rad_azo = sorted(set(r[1] for r in RAD if '/azo/' in r[1]))
    azo_bor = [k for k in STORE if '/azo/' in k]
    ok(not rad_oil and azo_bor and all('bu' not in STORE[k] for k in azo_bor) and all(k in STORE for k in rad_azo if k.split('/')[1] in [x.split('/')[1] for x in azo_bor]), f"Eski qoidalar (0.7.7): oilalar yozuvi rad etilmadi; bu/dz li a'zo yozuvi rad etilsa — o'sha zahoti ularsiz yozildi (rad {len(rad_azo)}, yozuv {len(azo_bor)}) {rad_oil[:2]}")
    # ---- C) takror, 📲 Oila reytingi, oddiy oila ----
    ota(AD, '#ota-reyting'); ok(AD.locator('#gadw').count() == 1 and 'Oilalar reyting guruhi' in AD.inner_text('#gadw'), "📲 Oila reytingi: admin kartasi ham bor")
    AD.click('#gadw [data-gal]'); ok(kutf(AD, "document.querySelector('#gadw') && document.querySelector('#gadw').innerText.includes('guruhda')", 6000), "Reyting panelida ham «🏆 guruhda»")
    for h, n in (('#ota', 'oddiy_menyu'), ('#ota-sozlama', 'oddiy_sozlama'), ('#ota-bulut', 'oddiy_akkaunt'), ('#ota-reyting', 'oddiy_reyting')):
        ota(DS, h); DS.wait_for_timeout(500); DS.screenshot(path=f'/tmp/bj078_{n}.png', full_page=True)
    ota(DS, '#ota-sozlama'); ok(DS.locator('#gadw').count() == 0 and 'Oilalar reyting guruhi' not in DS.evaluate("document.body.innerText"), "Oddiy oila sozlamasida admin kartasi YO'Q")
    for h, n in (('#ota-bulut', 'admin_akkaunt'),):
        ota(AD, h); AD.wait_for_timeout(500); AD.screenshot(path=f'/tmp/bj078_{n}.png', full_page=True)
    ok(AD.evaluate("document.documentElement.scrollWidth<=390") and DS.evaluate("document.documentElement.scrollWidth<=390"), "390 px — gorizontal siljish yo'q")
    ok(not PE, f"JS xato yo'q {PE[:3]}")
finally:
  srv.terminate()
print('\nJAMI XATO:', len(ERR)); [print(' -', e) for e in ERR]; sys.exit(1 if ERR else 0)
