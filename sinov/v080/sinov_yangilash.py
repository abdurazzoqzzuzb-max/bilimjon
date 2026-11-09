"""Bilimjon 0.8.0 — 🔄 yangilanish tizimi va ⏱ dam olish o'yini 1 daqiqa (u, 08.11).
• ⏱ eski oyinDaq (3) e'tiborsiz — hammada 1 daqiqa; ⚙️ sozlamada 1–5 (standart 1); bola uchun alohida.
• 🔄 version.json = A.VER = sw.js V; sw.js version.json ni keshlamaydi; ⚙️ «📲 Versiya» kartasi, tekshirish, 📖 qo'llanma.
• Soxta yangi versiya (route): uy ekranida — oyna o'zi chiqadi va qayta yuklaydi (?yv= tozalanadi), 2 urinishdan keyin «yopib qayta oching» tasmasi (halqa yo'q);
  faoliyatda (#mashq) — oyna emas, tasma [Yangilash][Keyinroq]; uyga qaytganda o'zi yangilaydi; majburiy (min) — faoliyatda ham oyna, «Keyinroq» yo'q.
Ishga tushirish: python3 sinov/v080/sinov_yangilash.py  (skrinshotlar: /tmp/bj080y_*.png)"""
import os, sys, time, subprocess, json, re
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.abspath(os.path.join(D, '..', '..'))
PORT = 8812; URL = f'http://localhost:{PORT}/'
srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT)], cwd=SITE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
ERR = []; PE = []
def ok(c, m): print(('✅ ' if c else '❌ ') + m); (None if c else ERR.append(m))
html = open(os.path.join(SITE, 'index.html'), encoding='utf-8').read(); sw = open(os.path.join(SITE, 'sw.js'), encoding='utf-8').read()
VER = re.search(r"A\.VER = '([\d.]+)'", html)[1]; SWV = re.search(r"const V = P \+ '([\d.]+)'", sw)[1]; VJ = json.load(open(os.path.join(SITE, 'version.json'), encoding='utf-8'))
ok(VJ['ver'] == VER == SWV and VJ.get('verk') and isinstance(VJ.get('yangi'), list) and VJ['yangi'], f"version.json ({VJ['ver']}) = A.VER ({VER}) = sw.js V ({SWV}), verk va «yangi» ro'yxati bor")
ok("version\\.json" in sw and 'return;' in sw.split('version\\.json')[1][:40], "sw.js version.json ni keshlamaydi (tarmoqqa o'tkazadi)")
KEYIN = '.'.join(VER.split('.')[:2] + [str(int(VER.split('.')[2]) + 1)])   # joriy versiyadan bitta yangi (soxta)
def yangiVer(v, mn=None): return json.dumps({'ver': v, 'verk': v.split('.')[1] + '.' + v.split('.')[2], 'min': mn or '0.8.0', 'yangi': ["🎮 Yangi o'yin", '📚 Yangi darslar']})
def tel(br, nom, fake=None):
    ctx = br.new_context(viewport={'width': 390, 'height': 844}, service_workers='block', device_scale_factor=1)
    if fake: ctx.route('**/version.json*', lambda r: r.fulfill(status=200, content_type='application/json', body=fake))
    pg = ctx.new_page(); pg.on('pageerror', lambda e: PE.append(f'{nom}: {e}')); return pg
def oila(pg, url=URL):
    pg.goto(url); pg.wait_for_timeout(400)
    pg.fill('#on', 'Sinov'); pg.fill('#p1', '1234'); pg.fill('#p2', '1234'); pg.click('#go'); pg.wait_for_timeout(300)
    return pg.evaluate("(()=>{const A=BJ.A; const b=A.newBola({laqab:'Ali',daraja:'g1',avatar:'🦊',dunyo:'garaj'}); A.S().sozlama.uyqu=''; A.S().joriy=b.id; A.save(true); return b.id})()")
def kutf(pg, js, ms=10000):
    try: pg.wait_for_function(js, timeout=ms); return True
    except Exception: return False
try:
  with sync_playwright() as p:
    br = p.chromium.launch()
    # ---- ⏱ dam olish o'yini — 1 daqiqa
    P = tel(br, 'OYIN'); bid = oila(P)
    c = P.evaluate("(()=>{const A=BJ.A,s=A.S(),b=A.bola(); s.sozlama.oyinDaq=3; b.oyinDaq=3; A.save(true); return A.oyinCfg(b).daq})()")
    ok(c == 1, f"Eski sozlama (oyinDaq=3) bo'lsa ham o'yin 1 daqiqa ({c})")
    P.evaluate("BJ.A.otaOk={rol:'admin',t:Date.now()}"); P.goto(URL + '#ota-sozlama'); P.wait_for_timeout(500)
    ok(P.eval_on_selector('#od', 'e=>e.value') == '1' and 'standart' in P.inner_text('#od'), "⚙️ «O'yin davomiyligi»: 1 daqiqa (standart) tanlangan")
    P.select_option('#od', '3'); P.click('[data-save]'); P.wait_for_timeout(400)
    c = P.evaluate("(()=>{const A=BJ.A,b=A.bola(); const r=[A.S().sozlama.oyinMin, A.oyinCfg(b).daq]; b.oyinMin=2; r.push(A.oyinCfg(b).daq); b.oyinMin=null; return r})()")
    ok(c == [3, 3, 2], f"Ota-ona 3 daqiqaga ko'paytirdi → 3; bola uchun alohida 2 → 2 ({c})")
    # ---- ⚙️ versiya kartasi
    P.evaluate("BJ.A.otaOk={rol:'admin',t:Date.now()}"); P.goto(URL + '#ota-sozlama'); P.wait_for_timeout(500)
    t = P.inner_text('body')
    ok('📲 Versiya' in t and f"v{VJ['verk']}" in t and VER in t, f"⚙️ «📲 Versiya» kartasi: v{VJ['verk']} ({VER})")
    P.click('[data-yvt]'); ok(kutf(P, "document.querySelector('[data-yvs]') && document.querySelector('[data-yvs]').textContent.indexOf('eng yangisi')>=0", 6000), "«🔄 Tekshirish» — ✅ eng yangisi")
    P.click('[data-yvq]'); P.wait_for_timeout(300); q = P.inner_text('.sheet')
    ok('iPhone' in q and 'Android' in q and 'Yangilash' in q, "📖 «Qanday yangilanadi?» — iPhone va Android qadamlari")
    P.screenshot(path='/tmp/bj080y_qollanma.png'); P.context.close()
    # ---- uy ekranida yangi versiya: o'zi yangilanadi, halqa yo'q
    P = tel(br, 'UY', yangiVer(KEYIN)); oila(P); P.goto(URL + '#uy'); P.wait_for_timeout(300)
    ok(kutf(P, "!!document.querySelector('.yvo')", 8000), "Uy ekranida yangi versiya → «🆕 … keldi» oynasi o'zi chiqdi")
    t = P.inner_text('.yvo') if P.locator('.yvo').count() else ''
    ok('v1.8' in t or '1.8' in t or "Yangi o'yin" in t, f"Oynada versiya va «Nima yangi» ro'yxati ({t[:80]!r})")
    P.screenshot(path='/tmp/bj080y_oyna.png')
    ok(kutf(P, "performance.getEntriesByType('navigation')[0] && location.search.indexOf('yv=')<0 && BJ.A.yvHolat && Date.now()-performance.timeOrigin<6000", 12000), "3 s dan keyin qayta yuklandi, manzildagi ?yv= tozalandi")
    ok(kutf(P, "!!document.querySelector('.yvt') && document.querySelector('.yvt').textContent.indexOf('Yangilanmadi')>=0", 30000), "Server eski fayl bersa — 2 urinishdan keyin to'xtadi: «Yangilanmadi — yopib qayta oching» tasmasi")
    n = P.evaluate("JSON.parse(localStorage.getItem('bj_yv')||'{}').n")
    ok(n == 2 and P.locator('.yvo').count() == 0, f"Halqa yo'q: urinish {n}, oyna yo'q")
    P.goto(URL + '#tanla'); P.wait_for_timeout(1200); ok(P.locator('.yvo').count() == 0, "To'xtagandan keyin sahifa almashganda ham oyna qayta chiqmaydi")
    P.click('.yvt [data-yvq]') if P.locator('.yvt [data-yvq]').count() else None; P.wait_for_timeout(300)
    ok(P.locator('.sheet').count() == 1, "Tasmadagi «📖 Qanday?» qo'llanmani ochadi")
    P.context.close()
    # ---- faoliyatda: tasma, Keyinroq, uyga qaytganda o'zi
    P = tel(br, 'FAOL', yangiVer(KEYIN)); oila(P); P.goto(URL + '#mashq'); P.wait_for_timeout(300)
    ok(kutf(P, "!!document.querySelector('.yvt')", 8000) and P.locator('.yvo').count() == 0, "Mashq paytida — oyna emas, pastda «🆕 Yangi versiya» tasmasi")
    P.screenshot(path='/tmp/bj080y_tasma.png')
    ok(P.evaluate("document.documentElement.scrollWidth<=390"), "390 px — tasma bilan gorizontal siljish yo'q")
    ok(P.locator('.yvt [data-yvk]').count() == 1, "Oddiy versiyada «Keyinroq» tugmasi bor")
    P.click('.yvt [data-yvk]'); P.wait_for_timeout(300); ok(P.locator('.yvt').count() == 0, "«Keyinroq» — tasma yopildi")
    P.goto(URL + '#mashq'); P.wait_for_timeout(600); ok(P.locator('.yvt').count() == 0 and P.locator('.yvo').count() == 0, "Keyinroq'dan keyin mashq ichida bezovta qilmaydi")
    P.evaluate("location.hash='uy'"); ok(kutf(P, "!!document.querySelector('.yvo')", 4000), "Uyga qaytganda — o'zi yangilash oynasi")
    P.context.close()
    # ---- majburiy (min)
    P = tel(br, 'MAJ', yangiVer(KEYIN, KEYIN)); oila(P); P.goto(URL + '#mashq'); P.wait_for_timeout(300)
    ok(kutf(P, "!!document.querySelector('.yvo')", 8000), "Majburiy versiya — mashq paytida ham oyna")
    ok(P.locator('[data-yvk]').count() == 0, "Majburiyda «Keyinroq» yo'q")
    P.context.close()
    ok(not PE, f"JS xato yo'q {PE[:3]}")
finally:
  srv.terminate()
print('\nJAMI XATO:', len(ERR)); [print(' -', e) for e in ERR]; sys.exit(1 if ERR else 0)
