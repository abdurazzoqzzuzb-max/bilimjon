"""Bilimjon 0.7.2 — 🔊 iPhone ovozi: media pleyer yo'li (WAV + <audio>), teginishda ochilish, navbat (KUT), namuna, 🔧 tekshiruv va «Boshqa usul».
Sabab (07.11, u: «savol yonib turadi, lekin ovoz yo'q»): iPhone'da WebAudio jim qolardi. Haqiqiy ovoz fayllari (main'dagi ovoz/) bilan, iPhone UA,
autoplay ruxsatisiz (Safari kabi — teginishdan oldin ovoz chiqmaydi). Ishga tushirish: python3 sinov/v072/sinov_ovoz_ios.py"""
import os, sys, time, subprocess
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.abspath(os.path.join(D, '..', '..'))
PORT = 8797; URL = f'http://localhost:{PORT}/'
srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT)], cwd=SITE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1'
ERR, OV = [], {'ok': 0, 'yoq': []}
def ok(c, m): print(('✅ ' if c else '❌ ') + m); (None if c else ERR.append(m))
try:
  with sync_playwright() as p:
    br = p.chromium.launch()
    ctx = br.new_context(viewport={'width': 390, 'height': 844}, user_agent=UA, is_mobile=True, has_touch=True, service_workers='block')
    pg = ctx.new_page(); PE = []
    pg.on('pageerror', lambda e: PE.append(str(e)))
    pg.on('response', lambda r: (OV.__setitem__('ok', OV['ok'] + 1) if r.status == 200 else OV['yoq'].append(r.url)) if '/ovoz/' in r.url and r.url.endswith('.mp3') else None)
    ev = pg.evaluate; H = lambda: ev("BJ.A.ovoz.holat()")
    def kut(js, ms=8000):
        t = time.time()
        while time.time() - t < ms / 1000:
            if ev(js): return True
            pg.wait_for_timeout(100)
        return False
    pg.goto(URL + '?tez=1'); pg.wait_for_timeout(500)
    pg.fill('#on', 'Sinov'); pg.fill('#p1', '1234'); pg.fill('#p2', '1234'); pg.click('#go'); pg.wait_for_timeout(300)
    ev("""(()=>{const A=BJ.A; const k=A.newBola({laqab:'Kichik',daraja:'g0',avatar:'🐯',dunyo:'garaj'}); A.S().sozlama.uyqu=''; A.S().joriy=k.id; A.save(true)})()""")
    # 1) yangi sahifa — teginish hali yo'q: ovoz navbatga tushadi, 🔊 miltillaydi
    pg.goto(URL + '?tez=1&r=1#sinov-M0.10-1'); ev('BJ.A.render()')
    ok(kut("BJ.A.ovoz.holat().kut", 6000), "teginishdan oldin: savol navbatda (KUT), avtomatik ijro bloklanmadi deb xato chiqmadi")
    h = H(); ok(h['yol'] == 'media' and not h['me'], f"iPhone'da yo'l — media, pleyer hali yopiq ({h['yol']}, me={h['me']})")
    ok(pg.locator('.uzb.teg').count() == 1, "🔊 tugmasi miltillaydi (teginish kerak)")
    ok('teging' in ev("document.body.innerText"), "«Ovoz uchun ekranga bir marta teging» xabari")
    # 2) birinchi teginish → pleyer ochiladi → savol o'zi o'qiladi
    bb = pg.locator('.q').bounding_box(); pg.touchscreen.tap(bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] / 2)
    ok(kut("BJ.A.ovoz.holat().me && !!document.querySelector('.q.gapir')", 6000), "teginishdan keyin pleyer ochildi va savol o'qilmoqda (.q.gapir)")
    h = H(); ok(h['msrc'] == 'blob:', f"ovoz bitta WAV (blob) sifatida media pleyerda ({h['msrc']})")
    ok(kut("BJ.A.ovoz.holat().mn >= 1 && !document.querySelector('.q.gapir')", 10000), f"ijro oxirigacha yetdi (ended) — {H()['mn']} marta")
    # 3) 🔊 tugmasi — qayta eshitish
    n0 = H()['mn']; pg.locator('.uzb').click()
    ok(kut(f"BJ.A.ovoz.holat().mn > {n0}", 10000), "🔊 bosilganda qayta o'qildi")
    # 4) javobdan keyin keyingi savol teginishsiz o'zi o'qiladi
    pg.goto(URL + '?tez=1&r=2#sinov-M0.10-1'); ev('BJ.A.render()')   # yangi hujjat — hisoblagich 0 dan
    pg.wait_for_timeout(600); h = H(); n0 = 0
    if not h['me']:  # yangi hujjat — yana bitta teginish kerak (Safari ham shunday)
        bb = pg.locator('.q').bounding_box(); pg.touchscreen.tap(bb['x'] + 5, bb['y'] + 5)
    ok(kut(f"BJ.A.ovoz.holat().mn > {n0}", 10000), "yangi sahifada 1 teginishdan keyin o'qildi")
    n0 = H()['mn']; ev("window.__bjJavob(true)"); pg.wait_for_timeout(300)
    ok(kut(f"BJ.A.ovoz.holat().mn > {n0}", 12000), "javobdan keyin keyingi savol teginishsiz o'zi o'qildi")
    # 5) ota-ona paneli: namuna + 🔧 tekshiruv + «Boshqa usul»
    pg.goto(URL + '?tez=1&r=3#ota-ovoz'); ev("BJ.A.otaOk={rol:'admin',t:Date.now()}; BJ.A.render()"); pg.wait_for_timeout(700)
    n0 = H()['mn']; pg.locator('[data-nam]').tap()
    ok(kut("!!document.querySelector('[data-nam].gapir')", 8000), "▶ Namuna o'qilmoqda (tugma yonib turibdi)")
    ok(kut(f"BJ.A.ovoz.holat().mn > {n0}", 40000), "▶ Namuna media pleyerda oxirigacha o'qildi")
    pg.locator('[data-tek]').tap(); ok(kut("!!document.querySelector('[data-eh]')", 15000), "🔧 tekshiruv tugadi")
    t = ev("document.body.innerText"); ok('media pleyer' in t and 'Media pleyer ochiq' in t, "tekshiruvda «Usul: media pleyer» va «pleyer ochiq»")
    pg.locator('[data-eh="0"]').tap(); pg.wait_for_timeout(200)
    kod = ev("(document.querySelector('[data-ehn] input')||{}).value||''")
    ok('yol=media' in kod and 'me=ochiq' in kod and 'ijro=ok' in kod, f"natija qatori: {kod[:90]}")
    pg.locator('[data-yol]').tap(); ok(kut("!!document.querySelector('[data-eh]')", 15000), "«🔁 Boshqa usulda sinash» qayta tekshirdi")
    pg.locator('[data-eh="0"]').tap(); pg.wait_for_timeout(200)
    kod = ev("(document.querySelector('[data-ehn] input')||{}).value||''")
    ok('yol=webaudio' in kod and ev("BJ.A.S().sozlama.nutq.yol") == 'webaudio', f"usul WebAudio ga o'tdi va saqlandi: {kod[:70]}")
    pg.locator('[data-yol]').tap(); pg.wait_for_timeout(300)
    ok(ev("BJ.A.S().sozlama.nutq.yol") == 'media', "yana media pleyerga qaytdi")
    ok(not PE, f"JS xato yo'q {PE[:3]}"); PE.clear()
    # 6) iPhone bo'lmagan telefon — avvalgidek WebAudio
    c2 = br.new_context(viewport={'width': 390, 'height': 844}, service_workers='block'); p2 = c2.new_page()
    p2.goto(URL + '?tez=1'); p2.wait_for_timeout(400)
    ok(p2.evaluate("BJ.A.ovoz.holat().yol") == 'webaudio', "Android/kompyuter — yo'l WebAudio (o'zgarmadi)")
    ok(OV['ok'] >= 3 and not OV['yoq'], f"ovoz fayllari: {OV['ok']} ta yuklandi, yo'q fayl: {OV['yoq'][:3]}")
    br.close()
finally:
    srv.terminate()
print(f"\n{'HAMMASI OK' if not ERR else str(len(ERR)) + ' ta xato'}")
for e in ERR: print('  -', e)
sys.exit(1 if ERR else 0)
