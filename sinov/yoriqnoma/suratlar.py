"""Bilimjon 📘 yo'riqnoma — ilovaning HAQIQIY ekranlarini suratga oladi (namuna oila, soxta bulut; haqiqiy ism yo'q).
Ishlatish: python3 sinov/yoriqnoma/suratlar.py <papka>   → <papka>/*.png (390×844, 2× — telefon ekrani)
Yo'riqnoma o'zi: python3 sinov/yoriqnoma/yoriqnoma.py (shu skriptni chaqiradi)."""
import os, sys, time, subprocess, json, threading
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.abspath(os.path.join(D, '..', '..')); FAKE = os.path.join(SITE, 'sinov', 'bulut')
OUT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '/tmp/bj_yoriqnoma/sur'); os.makedirs(OUT, exist_ok=True)
PORT = 8811; URL = f'http://localhost:{PORT}/'
SOAT = '2026-11-12T16:40:00'   # payshanba — xaritada 3 kun bajarilgan
srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT)], cwd=SITE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
PE = []
# ---------- soxta Firebase (sinov/v076 dagidek, qoidalarsiz) ----------
STORE = {}; LOCK = threading.RLock()
def fs(arg):
    a = json.loads(arg); op = a[0]; who = (a[-1] if isinstance(a[-1], dict) else {}) or {}
    with LOCK:
        if op == 'get':
            if a[1].startswith('ruxsat/') and who.get('uid') == 'U_admin' : return json.dumps(STORE.get(a[1]))
            return json.dumps(STORE.get(a[1]))
        if op == 'list':
            if a[1] == 'ruxsat' and who.get('uid') != 'U_admin': return json.dumps({'__err': 'permission-denied'})
            pre = a[1] + '/'; return json.dumps([[k, v] for k, v in STORE.items() if k.startswith(pre) and '/' not in k[len(pre):]])
        if op == 'del': STORE.pop(a[1], None); return 'null'
        if op == 'set':
            path, data, merge = a[1], a[2], a[3]; old = dict(STORE.get(path) or {}) if merge else {}
            if path.startswith('oila/') and (STORE.get('ruxsat/' + str(who.get('uid'))) or {}).get('holat') != 'ok': return json.dumps({'__err': 'permission-denied'})
            for k, v in data.items():
                if isinstance(v, dict) and '__au' in v: cur = list(old.get(k) or []); [cur.append(x) for x in v['__au'] if x not in cur]; old[k] = cur
                else: old[k] = v
            STORE[path] = old; return 'null'
    return 'null'
FILES = {'firebase-app.js': 'export function initializeApp(c){return {c}}', 'firebase-auth.js': open(os.path.join(FAKE, 'auth.js')).read(), 'firebase-firestore.js': open(os.path.join(FAKE, 'fs.js')).read()}
def kutpy(pg, f, ms=10000):
    t = time.time()
    while time.time() - t < ms / 1000:
        with LOCK:
            if f(): return True
        pg.wait_for_timeout(200)
    return False
YASHIR = "document.querySelectorAll('.toast,.toasts').forEach(e=>e.remove())"
def sur(pg, nom, full=False, ms=350):
    pg.wait_for_timeout(ms); pg.evaluate(YASHIR); pg.screenshot(path=os.path.join(OUT, nom + '.png'), full_page=full); print('📸', nom)

NAMUNA = """(()=>{const A=BJ.A, s=A.S(); s.sozlama.uyqu=''; const D=A.weekDays(A.isoWeek());
  const yasa=(o, kunlar, yul)=>{ const b=A.newBola(o); b.yaratildi=D[0]; b.boshlandi=D[0];
    kunlar.forEach(k=>{ b.kun[k]=Object.assign(A.agg(b,k),{faol:1500,n:24,ok1:20,missiya:1,yulduz:yul}); }); b.yulduz=yul*kunlar.length; return b; };
  const a=yasa({laqab:'Aziz',daraja:'g1',avatar:'🐯',dunyo:'garaj'}, D.slice(0,3), 14), l=yasa({laqab:'Lola',daraja:'g0',avatar:'🦋',dunyo:'orol'}, D.slice(0,2), 11);
  a.detal=['gildirak','spoyler','nitro']; s.joriy=a.id; A.save(true); return [a.id,l.id]})()"""

try:
  with sync_playwright() as p:
    br = p.chromium.launch(args=['--autoplay-policy=no-user-gesture-required'])
    def kontekst(bulut=False):
        c = br.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2, service_workers='block', has_touch=True)
        if bulut:
            c.expose_function('__fs', fs)
            c.route('https://www.gstatic.com/firebasejs/**', lambda r: r.fulfill(status=200, content_type='text/javascript', body=FILES[r.request.url.split('/')[-1]]))
        c.route('https://fonts.googleapis.com/**', lambda r: r.fulfill(status=200, content_type='text/css', body=''))
        c.route('https://fonts.gstatic.com/**', lambda r: r.abort())
        pg = c.new_page(); pg.clock.set_fixed_time(SOAT); pg.on('pageerror', lambda e: PE.append(str(e))); return pg
    pg = kontekst(); ev = pg.evaluate
    NV = [0]
    def NAV(h, ms=600): NV[0] += 1; pg.goto(URL + f'?tez=1&r={NV[0]}#' + h); ev('BJ.A.render()'); pg.wait_for_timeout(ms)
    # ===== 1) oila yaratish =====
    pg.goto(URL + '?tez=1'); pg.wait_for_timeout(600)
    pg.fill('#on', 'Namuna oila'); pg.fill('#p1', '1234'); pg.fill('#p2', '1234'); sur(pg, '01_oila')
    pg.click('#go'); pg.wait_for_timeout(500)
    pg.fill('#fl', 'Aziz'); pg.click('.avb[data-a="🐯"]'); pg.select_option('#fd', 'g1'); sur(pg, '02_bola')
    AZ, LO = ev(NAMUNA)
    # ===== 2) bola ekranlari =====
    NAV('tanla'); sur(pg, '03_tanla')
    NAV('uy', 900); sur(pg, '04_uy')
    NAV('missiya', 900)
    for _ in range(40):
        if ev("!!(window.__bjCur && __bjCur() && __bjCur().it && document.querySelector('#body .opt') && !__bjCur().it.matn && String(__bjCur().it.sav).length < 40)"): break   # qisqa, chiroyli savol
        b = pg.locator('#app .btn.big, #app [data-next], #app [data-go-on]')
        if b.count(): b.first.click(); pg.wait_for_timeout(500)
        elif ev("!!(window.__bjCur && __bjCur() && __bjCur().cb)"): ev("window.__bjJavob(true)"); pg.wait_for_timeout(500)
        else: pg.wait_for_timeout(300)
    sur(pg, '05_savol', ms=900)
    NAV('uy'); ev("BJ.A.oyin.boshla(BJ.A.bola(), {k:'yoriqnoma'}, ()=>{})"); pg.wait_for_timeout(300)
    ev("(()=>{const t=document.querySelector('[data-tm]'); if(t) t.textContent='⏱ 3:00'})()"); sur(pg, '06_dam', ms=100)   # ?tez=1 da 8 s — oddiy rejimdagi 3 daqiqa ko'rinsin
    NAV('zal'); sur(pg, '07_zal_qulf')
    pg.click('[data-rux]'); pg.wait_for_timeout(250); pg.fill('.sheet #zp', '1234'); pg.click('.sheet [data-d="20"]'); sur(pg, '08_zal_pin')
    ev(f"(()=>{{const b=BJ.A.S().bolalar['{AZ}']; BJ.A.agg(b).missiya=1; BJ.A.save(true)}})()"); NAV('zal'); sur(pg, '09_zal')
    # zal natijasi + reyting (guruhdagi boshqa oila bilan)
    wk = ev("BJ.A.isoWeek()")
    ev(f"""(()=>{{const s=BJ.A.S(); s.oilaTel=s.oilaTel||{{}}; s.oilaTel['G:udost']={{nom:"Do'st oila", guruh:1, wk:'{wk}', ts:Date.now(), bolalar:[
      {{id:'gb1', av:'🦁', laqab:'Sardor', daraja:'g1', wkB:'{wk}', yulduz:38, kun:3, osish:2, detal:4, missiya:3, zal:{{r:{{turbo:[24.6,10], xotira:[14,8]}}, h:{{turbo:[24.6,10]}}, p:{{}}}}}},
      {{id:'gb2', av:'🐼', laqab:'Madina', daraja:'g0', wkB:'{wk}', yulduz:30, kun:2, osish:1, detal:2, missiya:2, zal:{{r:{{poyga:[18,0]}}, h:{{}}, p:{{}}}}}}]}};
      const b=s.bolalar['{AZ}']; b.zal=b.zal||{{}}; b.zal.rek=Object.assign(b.zal.rek||{{}},{{turbo:{{v:27.9,n:10,sana:BJ.A.todayKey(),ts:Date.now(),gl:'g1'}}, svetofor:{{v:410,n:0,sana:BJ.A.todayKey(),ts:Date.now(),gl:'g1'}}}});
      const l=s.bolalar['{LO}']; l.zal={{rek:{{poyga:{{v:21,n:0,sana:BJ.A.todayKey(),ts:Date.now(),gl:'g0'}}}},sek:{{}},son:{{}},guv:[]}}; BJ.A.save(true)}})()""")
    NAV('zal-rekord', 700); sur(pg, '10_rekordlar')
    NAV('uy', 900); sur(pg, '11_uy_reyting', full=True)
    # ota-ona paneli
    NAV('uy'); ev("BJ.A.otaOk={rol:'admin',t:Date.now()}"); ev("location.hash='ota'"); sur(pg, '12_ota', ms=600)
    ev("location.hash='ota-sozlama'"); pg.wait_for_timeout(500); ev("document.querySelector('#zl').scrollIntoView({block:'start'}); scrollBy(0,-90)"); sur(pg, '13_sozlama')
    ev("location.hash='ota-hisobot'"); sur(pg, '14_hisobot', ms=600)
    pg.context.close()

    # ===== 3) ☁️ oila akkaunti (soxta bulut) =====
    pg = kontekst(True); ev = pg.evaluate
    pg.goto(URL); pg.wait_for_timeout(600); pg.fill('#on', 'Namuna oila'); pg.fill('#p1', '1234'); pg.fill('#p2', '1234'); pg.click('#go'); pg.wait_for_timeout(400)
    AZ, LO = ev(NAMUNA)
    ev("BJ.A.otaOk={rol:'admin',t:Date.now()}"); pg.goto(URL + '#ota-bulut'); pg.wait_for_timeout(900)
    pg.fill('#be', 'namuna.oila@gmail.com'); pg.fill('#bp', 'parol123'); sur(pg, '20_akkaunt')
    STORE['ruxsat/U_admin'] = {'holat': 'ok'}
    pg.click('[data-up]'); pg.wait_for_timeout(1500)
    if pg.locator('#rxn').count(): pg.fill('#rxn', 'Namuna oila')
    sur(pg, '21_ruxsat_kerak', ms=500)
    if pg.locator('[data-rxq]').count(): pg.click('[data-rxq]'); pg.wait_for_timeout(1200)
    sur(pg, '22_kutilmoqda', ms=400)
    u = [k.split('/')[1] for k in STORE if k.startswith('ruxsat/') and k != 'ruxsat/U_admin']
    with LOCK:
        for x in u: STORE['ruxsat/' + x] = dict(STORE['ruxsat/' + x], holat='ok', hal=int(time.time() * 1000))
    kutpy(pg, lambda: any(k.startswith('oila/') for k in STORE), 15000); pg.wait_for_timeout(1200)
    pg.goto(URL + '#ota-bulut'); ev("BJ.A.otaOk={rol:'admin',t:Date.now()}"); ev("BJ.A.render()"); sur(pg, '23_ulandi', ms=900)
    ev("location.hash='ota-reyting'"); pg.wait_for_timeout(700)
    if pg.locator('#gk').count(): pg.fill('#gk', 'K7M2QX9PLA'); ev("document.querySelector('#gk').scrollIntoView({block:'center'})")
    sur(pg, '24_guruh_kod')
    # guruhga qo'shilgandan keyin (boshqa oila bor)
    me = u[0] if u else 'U_x'; KOD = 'K7M2QX9PLA'; now = int(time.time() * 1000)
    with LOCK:
        STORE['guruh/' + KOD] = {'yaratdi': 'U_dost', 'ts': now}; STORE[f'guruh/{KOD}/oilalar/U_dost'] = {'ts': now}
        wk = ev("BJ.A.isoWeek()")
        for bid, av, lq, dr, yl in (('gb1', '🦁', 'Sardor', 'g1', 38), ('gb2', '🐼', 'Madina', 'g0', 30)):
            STORE[f'guruh/{KOD}/azo/{bid}'] = {'uid': 'U_dost', 'oila': "Do'st oila", 'av': av, 'laqab': lq, 'daraja': dr, 'yulduz': yl, 'kun': 3, 'osish': 2, 'detal': 3, 'missiya': 3, 'wk': wk, 'ts': now}
    pg.click('[data-gk]'); pg.wait_for_timeout(2500); ev("document.querySelector('[data-gs]') && document.querySelector('[data-gs]').closest('.card').scrollIntoView({block:'center'})"); sur(pg, '25_guruh_ichida', ms=600)
    pg.context.close()
finally:
  srv.terminate()
print('JS xato:', PE[:5] if PE else "yo'q")
