"""Bilimjon 0.8.2 — 🏁 gonka/devor zinapoyasi, 🤝 jamoa sovg'asi (B1), 🌙 bugungi xulosa, 🆕 yangilik kartasi, 👑 oilalar holati, ☁️ yuborish belgisi (u, 10.11).
Ishga tushirish: python3 sinov/v082/sinov_v082.py (skrinshot: /tmp/bj082_panel.png)"""
import os, sys, time, subprocess, json, threading
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.abspath(os.path.join(D, '..', '..')); FAKE = os.path.join(SITE, 'sinov', 'bulut')
PORT = 8815; URL = f'http://localhost:{PORT}/'
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
Q = '?tez=1'
import re
html = open(os.path.join(SITE, 'index.html'), encoding='utf-8').read(); VJ = json.load(open(os.path.join(SITE, 'version.json'), encoding='utf-8'))
VER = re.search(r"A\.VER = '([\d.]+)'", html)[1]
try:
  with sync_playwright() as p:
    br = p.chromium.launch()
    STORE['ruxsat/U_dosttestuz'] = {'email': 'dost@test.uz', 'oila': 'Dost oila', 'ts': 1, 'holat': 'ok'}
    def oila(pg, q=Q):
        pg.goto(URL + q); pg.wait_for_timeout(400)
        pg.fill('#on', 'Dost oila'); pg.fill('#p1', '1234'); pg.fill('#p2', '1234'); pg.click('#go'); pg.wait_for_timeout(300)
        return pg.evaluate("(()=>{const A=BJ.A; const a=A.newBola({laqab:'Ali',daraja:'g2',avatar:'🐯',dunyo:'garaj'}), l=A.newBola({laqab:'Lola',daraja:'g1',avatar:'🦋',dunyo:'orol'}); A.S().sozlama.uyqu=''; A.S().joriy=a.id; A.save(true); return [a.id,l.id]})()")
    P = tel(br, 'A'); AZ, LO = oila(P); ev = P.evaluate
    yang = ev("BJ.A.YANGI")
    ok(VJ['ver'] == VER and VJ['yangi'] == yang and len(yang) >= 2, f"version.json = A.VER ({VER}), «yangi» = A.YANGI ({len(yang)} qator)")
    # ---- 🏁 zinapoya
    r = ev("""(()=>{const M=BJ.A.zalMisol, P=BJ.A.zalPOG, out={}; for (const g of ['g1','g2']) for (let lv=0; lv<P[g]; lv++) { let mx=0, bad=0, ikki=0; for (let i=0;i<600;i++) { const T=M(g,lv), e=T.sav.v.replace(/−/g,'-').replace(/×/g,'*').replace(/:/g,'/'), n=Function('return '+e)(); if (n!==T.n || T.o[T.a].v!==T.n || T.o.length!==3) bad++; const nums=(T.sav.v.match(/\\d+/g)||[]).map(Number); mx=Math.max(mx,...nums); { const m=T.sav.v.match(/^(\\d\\d) [+−] (\\d\\d)$/); if (m && !(+m[1]%10===0 && +m[2]%10===0)) ikki++; } } out[g+lv]={mx,bad,ikki}; } return out})()""")
    ok(all(v['bad'] == 0 for v in r.values()), f"Zinapoya: hamma pog'onada misol va to'g'ri javob mos ({sum(v['bad'] for v in r.values())} xato)")
    ok(r['g10']['mx'] <= 5 and r['g11']['mx'] <= 10 and r['g13']['mx'] <= 19, f"1-sinf: ① 5 gacha, ② 10 gacha, ④ 20 gacha ({r['g10']['mx']}, {r['g11']['mx']}, {r['g13']['mx']})")
    ok(r['g20']['ikki'] == 0 and r['g21']['ikki'] == 0 and r['g23']['ikki'] > 0, f"2-sinf: ①–② da «67−25» kabi ikki xonali ± yo'q (faqat 40+30 kabi o'nliklar), ④ da bor ({r['g20']['ikki']}, {r['g21']['ikki']}, {r['g23']['ikki']})")
    # ---- 🧱 devor: 3 ta ketma-ket to'g'ri → +1, xato → −1, saqlanadi
    BOSH = "BJ.A.oyin.boshla(BJ.A.bola(), {k:'sinov'}, ()=>{})"
    def devor_boshla():
        ev("location.hash='dam-sinov'"); P.wait_for_timeout(300); ev(BOSH); P.wait_for_timeout(200); ev("window.__bjOyin().sek = 60"); P.click('[data-o="devor"]'); P.wait_for_timeout(400)
        return ev("window.__bjZal() && window.__bjZal().game.state()")
    def dj(togri):
        kutf(P, "!!document.querySelector('.dvb') && !document.querySelector('.dvb.ok,.dvb.no')", 6000)
        s0 = ev("window.__bjZal().game.state()"); ev(f"window.__bjZal().game.javob({s0['a'] if togri else (s0['a'] + 1) % 3})"); P.wait_for_timeout(200)
        s1 = ev("window.__bjZal().game.state()")
        kutf(P, "(window.__bjZal() && window.__bjZal().game.state().fin) || (!!document.querySelector('.dvb') && !document.querySelector('.dvb.ok,.dvb.no'))", 6000)
        return s1
    s0 = devor_boshla(); ok(s0 and s0['lv'] == 0 and '📶 1/6' in P.inner_text('body'), f"Devor: 2-sinf, birinchi marta — 1-pog'onadan (📶 1/6) {s0 and s0['lv']}")
    dj(True); dj(True); s3 = dj(True)
    ok(s3['lv'] == 1 and ev(f"BJ.A.bola('{AZ}').zal.pog.g2") == 1, f"3 ta ketma-ket to'g'ri → 2-pog'ona, saqlandi ({s3['lv']})")
    s4 = dj(False); ok(s4['lv'] == 0 and ev(f"BJ.A.bola('{AZ}').zal.pog.g2") == 0, f"Xato → bir pog'ona osonroq ({s4['lv']})")
    ev(f"(()=>{{BJ.A.bola('{AZ}').zal.pog.g2=4; BJ.A.save(true)}})()"); ev("window.__bjZal() && window.__bjZal().game.stop && window.__bjZal().game.stop()")
    s5 = devor_boshla(); ok(s5 and s5['lv'] == 3, f"Keyingi o'yin: oxirgi yetgan pog'onadan (5) bittasi past — 4-pog'onadan ({s5 and s5['lv']})")
    ev("location.hash='uy'"); P.wait_for_timeout(600)
    # ---- 🤝 jamoa sovg'asi (B1)
    h = ev(f"""(()=>{{const A=BJ.A,s=A.S(),D=A.weekDays(A.isoWeek()); s.sovga=[{{id:'j1',kim:'oila',nom:'Park',n:3,har:true,hafta:A.isoWeek(),yetdi:{{}},berildi:{{}}}}];
      const a=A.bola('{AZ}'), l=A.bola('{LO}'); D.slice(0,3).forEach(k=>{{a.kun[k]=Object.assign(A.agg(a,k),{{missiya:1}})}}); D.slice(0,1).forEach(k=>{{l.kun[k]=Object.assign(A.agg(l,k),{{missiya:1}})}}); A.save(true);
      return A.sovgaHolat(s.sovga[0])}})()""")
    ok(h['har'] and not h['yetdi'] and [x['bor'] for x in h['per']] == [3, 1], f"Jamoa: Ali 3/3, Lola 1/3 → hali yetmadi (yig'indi 4 bo'lsa ham) {[x['bor'] for x in h['per']]}")
    ev("location.hash='tanla'"); P.wait_for_timeout(300); ev(f"BJ.A.S().joriy='{AZ}'; location.hash='uy'"); P.wait_for_timeout(700)
    t = P.inner_text('body')
    ok("Jamoa sovg'asi" in t and 'Sen bajarding' in t and 'Lola' in t, "Bola ekrani: 🤝 jamoa kartasi, «Sen bajarding! Jamoada yana 1 kishi qoldi»")
    h2 = ev(f"""(()=>{{const A=BJ.A,D=A.weekDays(A.isoWeek()),l=A.bola('{LO}'); D.slice(1,3).forEach(k=>{{l.kun[k]=Object.assign(A.agg(l,k),{{missiya:1}})}}); A.save(true); return A.sovgaHolat(A.S().sovga[0])}})()""")
    ok(h2['yetdi'], "Ikkalasi ham 3 kundan — sovg'a yetdi")
    # ---- 🌙 bugungi xulosa + 🆕 yangilik (ota-ona paneli tepasida)
    ev(f"""(()=>{{const A=BJ.A,b=A.bola('{AZ}'),k=A.todayKey(); b.kun[k]=Object.assign(A.agg(b,k),{{faol:1080,missiya:1}}); A.save(true);
      for (let i=0;i<5;i++) A.pushLog(b.id,{{t:'ans',ts:Date.now()-1000*i,bola:b.id,fan:'mat',tugun:'M2.4',savol:'67 − 25 = ?',javob:'35',togri_javob:'42',togri_1:0}});
      A.pushLog(b.id,{{t:'ans',ts:Date.now(),bola:b.id,fan:'mat',tugun:'M2.1',savol:'3 + 4',javob:'7',togri_javob:'7',togri_1:1}}); A.flushLog && A.flushLog();}})()""")
    ev("BJ.A.otaOk={rol:'admin',t:Date.now()}; location.hash='ota'"); P.wait_for_timeout(800)
    t = P.inner_text('body')
    ok('Bugungi xulosa' in t and '18 daq' in t and '6 savol' in t and 'Birga yeching' in t and '67 − 25' in t and '35' in t and '42' in t, "🌙 Bugungi xulosa: 18 daq · 6 savol · qiynalgan mavzu · «67 − 25» — u 35 dedi, to'g'risi 42")
    ok("hali o'ynamadi" in t, "O'ynamagan bola — «bugun hali o'ynamadi»")
    ok(P.locator('.xul').count() == 1 and ev("!!(document.querySelector('.xul').compareDocumentPosition(document.querySelector('.wkbar')) & 4)"), "Xulosa panelning eng tepasida (hafta jadvalidan oldin)")
    P.screenshot(path='/tmp/bj082_panel.png', full_page=True)
    ok('Yangilik' in t and P.locator('.ynk li').count() == len(yang), "🆕 Yangilik kartasi (shu versiya nima yangi)")
    P.click('[data-ynk]'); P.wait_for_timeout(200); ev("location.hash='uy'"); P.wait_for_timeout(300); ev("location.hash='ota'"); P.wait_for_timeout(600)
    ok(P.locator('.ynk').count() == 0, "«✓ Ko'rdim» dan keyin chiqmaydi")
    ok(P.locator('[data-sync-chip]').count() == 0, "Akkauntsiz oilada ☁️ belgi yo'q")
    oh = ev("""BJ.A.oilaHolatHTML([{uid:'a',nom:'Biz',ts:Date.now()-3600e3,v:'"""+VER+"""',holat:'admin'},{uid:'b',nom:'Asqarovlar',ts:Date.now()-31*3600e3,v:'0.8.0'},{uid:'c',nom:'Maxmudjonov',ts:Date.now()-41*3600e3,v:'0.7.7'}])""")
    ok('Asqarovlar' in oh and '⚠️' in oh and '🔄' in oh and oh.index('Asqarovlar') < oh.index('Biz'), "👑 Oilalar holati: kech yuborganlar va eski versiyalar ⚠️/🔄 bilan tepada")
    P.context.close()
    # ---- yangi versiya: panelga kirilganda darhol
    P2 = tel(br, 'B'); P2.context.route('**/version.json*', lambda r: r.fulfill(status=200, content_type='application/json', body=json.dumps({'ver': '9.9.9', 'verk': '9.9', 'min': '0.8.0', 'yangi': ['Sinov yangiligi']}))); oila(P2)
    P2.evaluate("BJ.A.otaOk={rol:'admin',t:Date.now()}; BJ.A.yvHolat && 0"); P2.evaluate("location.hash='ota'")
    ok(kutf(P2, "!!document.querySelector('.yvo')", 6000), "Panelga kirilganda yangi versiya darhol tekshirildi → «🆕 … keldi» oynasi")
    P2.context.close()
    # ---- ☁️ akkauntli qurilmada belgi
    P3 = tel(br, 'C'); oila(P3, '?x=1'); P3.evaluate("BJ.A.otaOk={rol:'admin',t:Date.now()}"); P3.goto(URL + '?x=1#ota-bulut'); P3.wait_for_timeout(500)
    P3.fill('#be', 'dost@test.uz'); P3.fill('#bp', 'parol123'); P3.click('[data-in]')
    ok(kutf(P3, "BJ.A.bulutUlangan() && !BJ.A.yuborHolat().bor", 15000), "Akkaunt ulandi")
    P3.goto(URL + '?x=1#uy'); P3.wait_for_timeout(700)
    ok(kutf(P3, "!!document.querySelector('[data-sync-chip].ok')", 12000), "☁️✓ — hammasi yuborilgan")
    P3.context.set_offline(True); P3.evaluate("(()=>{BJ.A.bola().yulduz+=2; BJ.A.save(true)})()"); P3.evaluate("location.hash='tanla'"); P3.wait_for_timeout(300); P3.evaluate("location.hash='uy'"); P3.wait_for_timeout(500)
    ok(P3.locator('[data-sync-chip].off').count() == 1, "📡✕ — internet yo'q, natija shu qurilmada")
    P3.click('[data-sync-chip]'); P3.wait_for_timeout(300); ok("Internet yo'q" in P3.inner_text('body'), "Belgini bosganda — tushuntirish")
    P3.context.set_offline(False); ok(kutf(P3, "!!document.querySelector('[data-sync-chip].ok')", 20000), "Internet qaytdi → o'zi yubordi → ☁️✓")
    P3.context.close()
    ok(not PE, f"JS xato yo'q {PE[:3]}")
finally:
  srv.terminate()
print('\nJAMI XATO:', len(ERR)); [print(' -', e) for e in ERR]; sys.exit(1 if ERR else 0)
