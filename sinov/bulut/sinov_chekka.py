"""Bilimjon 0.6.0 — sinxron chekka holatlari (soxta Firebase):
1) telefon soati farqi (oyisining soati 10 daqiqa orqada) · 2) yozish xatosida log yo'qolmasligi
3) bir necha kun internetsiz qolgan log · 4) ikki telefonda bir vaqtda o'ynash → bir xil holatga kelish."""
import json, os, sys, time, subprocess, threading
from playwright.sync_api import sync_playwright

D = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.abspath(os.path.join(D, '..', '..'))
PORT = 8766
srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT)], cwd=SITE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)
URL = f'http://localhost:{PORT}/'
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
         'firebase-auth.js': open(os.path.join(D, 'auth.js')).read(),
         'firebase-firestore.js': open(os.path.join(D, 'fs.js')).read()}
ERR = []
def ok(c, m):
    print(('✅ ' if c else '❌ ') + m)
    if not c: ERR.append(m)

def tel(br, nom, siljish_ms=0):
    ctx = br.new_context(viewport={'width': 390, 'height': 800}, service_workers='block')
    ctx.expose_function('__fs', fs)
    if siljish_ms:  # telefon soati noto'g'ri
        ctx.add_init_script(f"(()=>{{const d={siljish_ms}, N=Date.now.bind(Date); Date.now=()=>N()+d; const O=Date; window.Date=class extends O{{constructor(...a){{ if(!a.length) super(N()+d); else super(...a); }} static now(){{return N()+d}} }};}})()")
    ctx.route('https://www.gstatic.com/firebasejs/**', lambda r: r.fulfill(status=200, content_type='text/javascript', body=FILES[r.request.url.split('/')[-1]]))
    pg = ctx.new_page(); pg.on('pageerror', lambda e: ERR.append(f'{nom} pageerror: {e}'))
    pg.goto(URL); pg.wait_for_timeout(500); return pg

def oila(pg, nom):
    pg.fill('#on', nom); pg.fill('#p1', '1234'); pg.fill('#p2', '1234'); pg.click('#go'); pg.wait_for_timeout(300)

def kirish(pg, email):
    pg.wait_for_selector('#be', timeout=5000); pg.fill('#be', email); pg.fill('#bp', 'parol123'); pg.click('[data-in]')

ev = lambda pg, js: pg.evaluate(js)
UID = 'oila/U_soattestuz'

with sync_playwright() as p:
    br = p.chromium.launch()
    A = tel(br, 'A'); oila(A, 'Soat oila')
    bid = ev(A, "(()=>{const b=BJ.A.newBola({laqab:'Ali',daraja:'g1',avatar:'🦊'}); b.yulduz=5; BJ.A.save(true); return b.id})()")
    ev(A, "BJ.A.otaOk={rol:'admin',t:Date.now()}"); A.goto(URL + '#ota-bulut'); kirish(A, 'soat@test.uz'); A.wait_for_timeout(2500)
    ok(f'{UID}/bolalar/{bid}' in STORE, 'A: bola bulutga yozildi')

    # ---------- 1) Soat farqi: oyisining (B) soati 10 daqiqa orqada
    B = tel(br, 'B', siljish_ms=-600000)
    ok(abs(ev(B, 'Date.now()') + 600000 - time.time() * 1000) < 5000, 'B: soati haqiqatan 10 daqiqa orqada')
    B.click('#bk'); kirish(B, 'soat@test.uz'); B.wait_for_timeout(2500)
    ok(ev(B, f"BJ.A.bola('{bid}').yulduz") == 5, 'B: bulutdan bola olindi (⭐5)')
    ev(B, f"(()=>{{const b=BJ.A.bola('{bid}'); b.yulduz=8; BJ.A.save(true);}})()"); B.wait_for_timeout(500); ev(B, 'BJ.bulut.tick()')
    A.wait_for_timeout(2500)
    ya = ev(A, f"BJ.A.bola('{bid}').yulduz"); ok(ya == 8, f'Soat farqi: B (orqada) o\'ynagani A ga keldi (⭐ {ya}, kutilgan 8)')
    ev(A, f"(()=>{{const b=BJ.A.bola('{bid}'); b.yulduz=11; BJ.A.save(true);}})()"); A.wait_for_timeout(300); ev(A, 'BJ.bulut.tick()')
    B.wait_for_timeout(2500)
    yb = ev(B, f"BJ.A.bola('{bid}').yulduz"); ok(yb == 11, f'Soat farqi: A o\'ynagani B ga keldi (⭐ {yb}, kutilgan 11)')
    ev(B, "(()=>{const s=BJ.A.S(); s.oila.nom='Soat oila 2'; BJ.A.save(true);})()"); B.wait_for_timeout(300); ev(B, 'BJ.bulut.tick()')
    A.wait_for_timeout(2500)
    on = ev(A, "BJ.A.S().oila.nom"); ok(on == 'Soat oila 2', f'Soat farqi: B dagi oila sozlamasi A ga keldi ({on})')

    # ---------- 2) Yozish xatosi (internet bor, server javob bermadi) — log yo'qolmasin
    ev(A, "window.__fsFail=true")
    ev(A, f"(()=>{{BJ.A.pushLog('{bid}',{{t:'javob',ts:Date.now(),ok:1,belgi:'xato-paytida'}}); BJ.A.flushLog();}})()")
    ev(A, "BJ.bulut.tick().catch(()=>{})"); A.wait_for_timeout(800)
    ev(A, "BJ.bulut.logOl(2).catch(()=>{})"); A.wait_for_timeout(500)   # ilova qayta ochilganday — sync izlari saqlanadi
    ev(A, "window.__fsFail=false"); ev(A, "BJ.bulut.tick()"); A.wait_for_timeout(1500)
    lg = [v for k, v in STORE.items() if '/log/' in k and k.startswith(UID)]
    bor = any('xato-paytida' in e for v in lg for e in v.get('e', []))
    ok(bor, 'Yozish xatosidan keyin log bulutga baribir yetdi')
    # sahifa qayta yuklanganda ham (sync izlari localStorage'dan)
    ev(A, "window.__fsFail=true")
    ev(A, f"(()=>{{BJ.A.pushLog('{bid}',{{t:'javob',ts:Date.now(),ok:1,belgi:'reload-oldidan'}}); BJ.A.flushLog();}})()")
    ev(A, "BJ.bulut.tick().catch(()=>{})"); A.wait_for_timeout(600); ev(A, "BJ.bulut.logOl(2).catch(()=>{})"); A.wait_for_timeout(500)
    A.reload(); A.wait_for_timeout(3500); ev(A, "BJ.bulut.tick()"); A.wait_for_timeout(1500)
    lg = [v for k, v in STORE.items() if '/log/' in k and k.startswith(UID)]
    ok(any('reload-oldidan' in e for v in lg for e in v.get('e', [])), 'Xato + ilovani qayta ochish: log baribir yetdi')

    # ---------- 3) Bir necha kun internetsiz: 3 kun oldingi log ham yuboriladi
    ev(A, f"""(()=>{{const t=Date.now()-3*86400000; BJ.A.pushLog('{bid}',{{t:'javob',ts:t,ok:1,belgi:'uch-kun'}}); BJ.A.flushLog();
      const L=JSON.parse(localStorage.getItem('bj_bulut_v1')); L.oxirgi=Date.now()-3*86400000-3600000; localStorage.setItem('bj_bulut_v1',JSON.stringify(L));}})()""")
    A.reload(); A.wait_for_timeout(3500); ev(A, "BJ.bulut.tick()"); A.wait_for_timeout(1500)
    lg = [v for k, v in STORE.items() if '/log/' in k and k.startswith(UID)]
    ok(any('uch-kun' in e for v in lg for e in v.get('e', [])), '3 kun internetsiz qolgan telefon: eski kun logi ham yuborildi')

    # ---------- 4) Ikki telefonda bir vaqtda bitta bola → oxiri bir xil holat
    A.goto(URL + '#ota'); B.goto(URL + '#ota'); A.wait_for_timeout(1500); B.wait_for_timeout(1500)
    ev(A, f"(()=>{{const b=BJ.A.bola('{bid}'); b.yulduz=20; BJ.A.save(true);}})()")
    ev(B, f"(()=>{{const b=BJ.A.bola('{bid}'); b.yulduz=21; BJ.A.save(true);}})()")
    ev(A, "BJ.bulut.tick()"); ev(B, "BJ.bulut.tick()"); A.wait_for_timeout(9000); B.wait_for_timeout(500)
    ya, yb = ev(A, f"BJ.A.bola('{bid}').yulduz"), ev(B, f"BJ.A.bola('{bid}').yulduz")
    bulut = json.loads(STORE[f'{UID}/bolalar/{bid}']['j'])['yulduz']
    ok(ya == yb == bulut, f'Bir vaqtda o\'ynash: ikkala telefon va bulut bir xil (A {ya}, B {yb}, bulut {bulut})')
    br.close()
srv.terminate()
print('\nXATOLAR:', ERR if ERR else "yo'q")
sys.exit(1 if ERR else 0)
