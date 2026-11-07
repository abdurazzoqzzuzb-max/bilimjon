"""Bilimjon 0.7.3 — 🇬🇧 inglizcha so'z ovozi: «🔊 Eshitish» neyron fayl (ovoz/en_jenny) bilan, iPhone'da media pleyer (jim tugma to'smaydi).
Sabab (07.11, u: «jim rejimda savollar o'qilyapti, lekin Eshitish tugmasi ishlamayapti» — speechSynthesis iPhone'da jim tugmaga bo'ysunadi).
Haqiqiy fayllar (main'dagi ovoz/en_jenny, GitHub Actions yasagan), iPhone UA, autoplay ruxsatisiz. Ishga tushirish: python3 sinov/v073/sinov_en_ios.py"""
import os, sys, time, json, subprocess
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.abspath(os.path.join(D, '..', '..'))
PORT = 8798; URL = f'http://localhost:{PORT}/'
srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT)], cwd=SITE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1'
ERR, OV = [], {'ok': 0, 'yoq': []}
def ok(c, m): print(('✅ ' if c else '❌ ') + m); (None if c else ERR.append(m))
# speechSynthesis hisoblagichi: neyron fayl bor joyda telefon ovozi ISHLATILMASLIGI kerak
SS = "window.__ss = 0; try { const sp = speechSynthesis.speak.bind(speechSynthesis); speechSynthesis.speak = u => { window.__ss++; window.__ssT = u.text; try { sp(u); } catch (e) {} }; } catch (e) {}"
try:
  with sync_playwright() as p:
    br = p.chromium.launch()
    ctx = br.new_context(viewport={'width': 390, 'height': 844}, user_agent=UA, is_mobile=True, has_touch=True, service_workers='block')
    ctx.add_init_script(SS)
    pg = ctx.new_page(); PE = []
    pg.on('pageerror', lambda e: PE.append(str(e)))
    pg.on('response', lambda r: (OV.__setitem__('ok', OV['ok'] + 1) if r.status == 200 else OV['yoq'].append(r.url)) if '/en_jenny/' in r.url and r.url.endswith('.mp3') else None)
    ev = pg.evaluate; H = lambda: ev("BJ.A.ovoz.holat()")
    def kut(js, ms=8000):
        t = time.time()
        while time.time() - t < ms / 1000:
            if ev(js): return True
            pg.wait_for_timeout(100)
        return False
    pg.goto(URL + '?tez=1'); pg.wait_for_timeout(500)
    pg.fill('#on', 'Sinov'); pg.fill('#p1', '1234'); pg.fill('#p2', '1234'); pg.click('#go'); pg.wait_for_timeout(300)
    ev("""(()=>{const A=BJ.A; const k=A.newBola({laqab:'Kichik',daraja:'g0',avatar:'🐯',dunyo:'garaj',ingliz:true}); A.S().sozlama.uyqu=''; A.S().joriy=k.id; A.save(true)})()""")
    # 0) ro'yxat: ilovadagi HAMMA inglizcha matn uchun fayl bor
    R = json.load(open(os.path.join(SITE, 'ovoz', 'en_jenny', 'royxat.json')))
    ids = ev("BJ.A.ovoz.enMatnlar().map(t => BJ.A.ovoz.enId(t))"); yoq = [i for i in ids if i not in set(R['id'])]
    ok(len(ids) >= 140 and not yoq, f"inglizcha matnlar {len(ids)} ta — hammasiga fayl bor (yo'q: {yoq[:5]})")
    tts = ev("""(()=>{ const o = new Set(), O = BJ.A.ovoz; Object.keys(BJ.gen.reg).filter(i => i.indexOf('EN.') === 0).forEach(id => { for (let q = 1; q <= 3; q++) for (let i = 0; i < 60; i++) { const it = BJ.gen.make(id, q, { g0: i % 2 === 0 }); if (it.tts) o.add(O.enId(it.tts)); } }); return [...o]; })()""")
    ok(tts and all(i in set(R['id']) for i in tts), f"EN generatorlari: {len(tts)} xil aytiladigan so'z/ibora — hammasi ro'yxatda")
    # 1) EN q1 «Eshit va rasmini top»: teginishgacha navbat → teginish → o'zbekcha savol → inglizcha so'z O'ZI (neyron, media)
    pg.goto(URL + '?tez=1&r=1#sinov-EN.ranglar-1'); ev('BJ.A.render()')
    ok(pg.locator('[data-say]').count() == 1, "🔊 Eshitish tugmasi bor")
    ok(kut("BJ.A.ovoz.holat().kut", 6000), "teginishdan oldin: savol navbatda (iPhone qoidasi)")
    bb = pg.locator('.q').bounding_box(); pg.touchscreen.tap(bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] / 2)
    ok(kut("BJ.A.ovoz.holat().enOk >= 1", 15000), f"o'zbekcha savoldan keyin inglizcha so'z o'zi aytildi (neyron fayl) — {H()}")
    ok(H()['msrc'] == 'blob:' and H()['yol'] == 'media', "inglizcha so'z ham media pleyerda (WAV blob) — jim tugma to'smaydi")
    # 2) «🔊 Eshitish» bosilsa — yana neyron fayl, tugma yonib turadi, telefon ovozi ishlatilmaydi
    n0 = H()['enOk']; pg.locator('[data-say]').tap()
    ok(kut("!!document.querySelector('[data-say].gapir')", 4000), "bosilganda tugma yonib turadi (.gapir)")
    ok(kut(f"BJ.A.ovoz.holat().enOk > {n0}", 8000), "🔊 Eshitish → so'z oxirigacha aytildi")
    ok(ev("window.__ss") == 0 and H()['enTel'] == 0, f"telefon ovozi (speechSynthesis) ishlatilmadi: {ev('window.__ss')}")
    # 3) «Savol ovozi» o'chiq bo'lsa ham Eshitish ishlaydi
    ev("(()=>{const s=BJ.A.S(); s.sozlama.nutq={v:2,nom:'',avto:true,variant:true}; BJ.A.save(true)})()")
    pg.goto(URL + '?tez=1&r=2#sinov-EN.ranglar-1'); ev('BJ.A.render()'); pg.wait_for_timeout(500)
    ok(pg.locator('.uzb').count() == 0, "savol ovozi o'chiq — o'zbekcha 🔊 yo'q")
    n0 = H()['enOk']; pg.locator('[data-say]').tap()
    ok(kut(f"BJ.A.ovoz.holat().enOk > {n0}", 10000), "savol ovozi o'chiq bo'lsa ham 🔊 Eshitish neyron ovozda aytdi (1-teginishning o'zida)")
    ev("(()=>{const s=BJ.A.S(); s.sozlama.nutq={v:2,nom:'madina_jonli',avto:true,variant:true}; BJ.A.save(true)})()")
    # 4) javobning o'zi bo'lgan so'z (q3 «🍎 Bu inglizcha qanday?» va iboralar): oldindan AYTILMAYDI, javobdan keyin aytiladi
    pg.goto(URL + '?tez=1&r=3#sinov-EN.ranglar-3'); ev('BJ.A.render()')
    ok(ev("!!window.__bjCur().it.ttsKeyin") and pg.locator('[data-say]').count() == 0, "q3: tugma yo'q (javobni oldindan aytib qo'ymaydi)")
    bb = pg.locator('.q').bounding_box(); pg.touchscreen.tap(bb['x'] + 5, bb['y'] + 5)
    kut("BJ.A.ovoz.holat().mn >= 1 && !document.querySelector('.q.gapir')", 12000); pg.wait_for_timeout(900)
    n0 = H()['enOk']; ok(n0 == 0, f"q3: o'zbekcha savoldan keyin inglizcha javob o'zi aytilmadi (enOk={n0})")
    ev("window.__bjJavob(true)")
    ok(kut(f"BJ.A.ovoz.holat().enOk > {n0}", 8000), "q3: to'g'ri javobdan keyin to'g'ri talaffuz eshitildi")
    ib = ev("""(()=>{ for (let i = 0; i < 400; i++) { const it = BJ.gen.make('EN.salom', 3, {}); if (it.ex && it.ex.ib) return !!it.ttsKeyin; } return null; })()""")
    ok(ib is True, f"iboralar savoli ham javobdan keyin aytiladi (ttsKeyin={ib})")
    # 5) 2 xato → kichik dars: so'z darsda aytiladi
    pg.goto(URL + '?tez=1&r=4#sinov-EN.ranglar-1'); ev('BJ.A.render()'); pg.wait_for_timeout(300)
    bb = pg.locator('.q').bounding_box(); pg.touchscreen.tap(bb['x'] + 5, bb['y'] + 5); kut("BJ.A.ovoz.holat().me", 5000)
    n0 = H()['enOk']
    for k in range(2):   # ikki marta noto'g'ri variant
        pg.locator(f'.opt:not([data-v="{ev("window.__bjCur().it.a")}"])').nth(k).tap(); pg.wait_for_timeout(700)
    ok(kut("!!document.querySelector('[data-dsay]')", 6000), "2 xatodan keyin kichik dars ochildi")
    ok(kut(f"BJ.A.ovoz.holat().enOk > {n0}", 10000), "darsda inglizcha so'z neyron ovozda aytildi")
    # 6) faylsiz matn — telefon ovozi (zaxira)
    ev("BJ.A.speak('zebra crossing qwerty')"); pg.wait_for_timeout(400)
    ok(ev("window.__ss") >= 1 and ev("window.__ssT") == 'zebra crossing qwerty', "fayli yo'q matn — telefon ovozi (zaxira) bilan")
    ok(not PE, f"JS xato yo'q {PE[:3]}"); PE.clear()
    # 7) Android/kompyuter — WebAudio bilan neyron fayl
    c2 = br.new_context(viewport={'width': 390, 'height': 844}, service_workers='block'); c2.add_init_script(SS); p2 = c2.new_page()
    p2.on('pageerror', lambda e: PE.append(str(e)))
    p2.goto(URL + '?tez=1'); p2.wait_for_timeout(400)
    p2.fill('#on', 'Sinov'); p2.fill('#p1', '1234'); p2.fill('#p2', '1234'); p2.click('#go'); p2.wait_for_timeout(300)
    p2.evaluate("""(()=>{const A=BJ.A; const k=A.newBola({laqab:'Katta',daraja:'g1',avatar:'🦁',dunyo:'garaj'}); A.S().sozlama.uyqu=''; A.S().joriy=k.id; A.save(true)})()""")
    p2.goto(URL + '?tez=1&r=5#sinov-EN.ranglar-1'); p2.evaluate('BJ.A.render()'); p2.wait_for_timeout(500)
    p2.locator('[data-say]').click()
    t = time.time(); r = False
    while time.time() - t < 10:
        if p2.evaluate("BJ.A.ovoz.holat().enOk >= 1"): r = True; break
        p2.wait_for_timeout(100)
    h2 = p2.evaluate("BJ.A.ovoz.holat()")
    ok(r and h2['yol'] == 'webaudio' and p2.evaluate("window.__ss") == 0, f"Android/kompyuter: WebAudio bilan neyron fayl, telefon ovozisiz ({h2['yol']}, enOk={h2['enOk']})")
    ok(not PE, f"JS xato yo'q (Android) {PE[:3]}")
    ok(OV['ok'] >= 3 and not OV['yoq'], f"en_jenny fayllari: {OV['ok']} ta yuklandi, yo'q fayl: {OV['yoq'][:3]}")
    br.close()
finally:
    srv.terminate()
print(f"\n{'HAMMASI OK' if not ERR else str(len(ERR)) + ' ta xato'}")
for e in ERR: print('  -', e)
sys.exit(1 if ERR else 0)
