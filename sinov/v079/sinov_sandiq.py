"""Bilimjon 0.7.9 — 🔐 Orzu sandiqchasi (oldin 🐷 cho'chqa-kassa +5%). U (08.11): «cho'chqa emas — quticha qil; pul tegilmasa ko'payadi
g'oyasini olib tashla — islomiy tomondan to'g'ri emas». Tekshiriladi: ilovada 🐷 va «foiz»/«+5%» yo'q, sandiqcha rasmi va matni, solish
(tanga animatsiyasi), 14 kundan keyin ham pul o'zgarmaydi, maqsad kartasi sandiqchani hisobga oladi, ota-ona paneli, bozor tejash belgisi 🪙, 390 px.
Ishga tushirish: python3 sinov/v079/sinov_sandiq.py  (skrinshotlar: /tmp/bj079_*.png)"""
import os, sys, time, subprocess, re
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.abspath(os.path.join(D, '..', '..'))
PORT = 8810; URL = f'http://localhost:{PORT}/'
srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT)], cwd=SITE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
ERR = []; PE = []; NV = [0]
def ok(c, m): print(('✅ ' if c else '❌ ') + m); (None if c else ERR.append(m))
SRC = open(os.path.join(SITE, 'index.html'), encoding='utf-8').read()
try:
  with sync_playwright() as p:
    br = p.chromium.launch(); ctx = br.new_context(viewport={'width': 390, 'height': 844}, service_workers='block', device_scale_factor=2); pg = ctx.new_page()
    pg.on('pageerror', lambda e: PE.append(str(e))); ev = pg.evaluate
    def NAV(h, ms=450): NV[0] += 1; pg.goto(URL + f'?tez=1&r={NV[0]}#' + h); ev("BJ.A.otaOk={rol:'admin',t:Date.now()}; BJ.A.render()"); pg.wait_for_timeout(ms)
    # kod: 🐷 faqat izohda, foiz hisobi yo'q
    kod = re.sub(r'/\*.*?\*/', '', SRC, flags=re.S)
    ok('🐷' not in kod and "Cho'chqa" not in kod, "Ilova matnida 🐷 va «Cho'chqa» yo'q (faqat tarix izohida)")
    ok('FOIZ' not in kod and '+5%' not in kod and not re.search(r"tur: 'foiz'", kod), "Foiz hisobi va «+5%» matni yo'q")
    pg.goto(URL + '?tez=1'); pg.wait_for_timeout(400)
    pg.fill('#on', 'Sinov'); pg.fill('#p1', '1234'); pg.fill('#p2', '1234'); pg.click('#go'); pg.wait_for_timeout(300)
    Q, K = ev("""(()=>{const A=BJ.A; const q=A.newBola({laqab:'Aziz',daraja:'g1',avatar:'🦊',dunyo:'garaj'}); const k=A.newBola({laqab:'Kichik',daraja:'g0',avatar:'🐯',dunyo:'garaj'});
      A.S().sozlama.uyqu=''; A.S().joriy=q.id; A.pul.st(q).h=12000; A.save(true); return [q.id,k.id]})()""")
    NAV('dokon', 500); t = pg.inner_text('body')
    ok(pg.locator('.kassa .sndq').count() == 1 and 'Orzu sandiqchasi' in t, "Do'konda 🔐 Orzu sandiqchasi — sandiqcha rasmi bilan")
    ok('5%' not in t and 'tegmasang' not in t and 'kassa' not in t.lower().replace('kassaga', ''), "Do'konda foiz/«tegmasang» yo'q")
    pg.screenshot(path='/tmp/bj079_dokon_bosh.png')
    pg.click('[data-ks]'); pg.wait_for_timeout(300); sh = pg.inner_text('.sheet')
    ok("Orzu sandiqchasiga solish" in sh and "ko'paymaydi" in sh and '%' not in sh, "Solish oynasi: «ko'paymaydi ham, kamaymaydi ham», foiz yo'q")
    pg.click('.sheet [data-s="5000"]'); pg.wait_for_timeout(250)
    ok(pg.locator('.sndw.tush').count() == 1, "Solingandan keyin tanga tushish animatsiyasi (sndw.tush)")
    pg.wait_for_timeout(1500); pg.screenshot(path='/tmp/bj079_dokon_solindi.png')
    r = ev(f"(()=>{{const p=BJ.A.pul.st(BJ.A.S().bolalar['{Q}']); return [p.h,p.kassa]}})()")
    ok(r == [7000, 5000], f"Hamyon 7 000, sandiqcha 5 000 {r}")
    ev(f"(()=>{{const p=BJ.A.pul.st(BJ.A.S().bolalar['{Q}']); p.kassaTs=BJ.A.addDays(BJ.A.todayKey(),-21); BJ.A.save(true)}})()")
    NAV('dokon', 500)
    r = ev(f"(()=>{{const p=BJ.A.pul.st(BJ.A.S().bolalar['{Q}']); return [p.h,p.kassa]}})()")
    ok(r == [7000, 5000], f"21 kundan keyin ham o'zgarmadi (foiz yo'q) {r}")
    ok(pg.locator('.sndw.tush').count() == 0, "Qayta ochilganda animatsiya takrorlanmaydi")
    # maqsad: sandiqcha + hamyon
    ev(f"""(()=>{{const A=BJ.A, s=A.S(); s.dokon=[{{id:'g1',kim:'hamma',nom:'Lego',rasm:'',narx:10000,takror:false,yaratildi:Date.now()}}]; A.pul.st(s.bolalar['{Q}']).maqsad='g1'; A.save(true)}})()""")
    NAV('dokon', 500); t = pg.inner_text('.kassa')
    ok('Lego' in t and '12 000' in t and '10 000' in t, f"Sandiqcha kartasida orzu: «Lego», sandiqcha + hamyon = 12 000 / 10 000")
    pg.screenshot(path='/tmp/bj079_dokon_orzu.png')
    NAV('uy', 600); t = pg.inner_text('.maqsad') if pg.locator('.maqsad').count() else ''
    ok("Sandiqchadagi pul bilan yetadi" in t, f"Uydagi maqsad kartasi: «Sandiqchadagi pul bilan yetadi» ({t[:80]!r})")
    # maktabgacha — yo'q
    ev(f"(()=>{{const s=BJ.A.S(); s.joriy='{K}'; BJ.A.pul.st(s.bolalar['{K}']).h=5000; BJ.A.save(true)}})()"); NAV('dokon', 400)
    ok(pg.locator('.kassa').count() == 0, "Maktabgacha bolada sandiqcha yo'q")
    # ota-ona paneli
    NAV('ota-pul', 500); t = pg.inner_text('body')
    ok('Orzu sandiqchasi' in t and 'foiz yo' in t and '🐷' not in t and '🔐 5 000' in t, "Ota-ona paneli: sozlama matni (foiz yo'q) va hamyonda «+ 🔐 5 000»")
    ok(ev("document.documentElement.scrollWidth<=390"), "390 px — gorizontal siljish yo'q")
    ok(not PE, f"JS xato yo'q {PE[:3]}")
finally:
  srv.terminate()
print('\nJAMI XATO:', len(ERR)); [print(' -', e) for e in ERR]; sys.exit(1 if ERR else 0)
