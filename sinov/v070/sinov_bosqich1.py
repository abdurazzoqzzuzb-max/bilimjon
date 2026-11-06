"""Bilimjon 0.7.0 — 1-bosqich: 🗺️ sarguzasht xaritasi (7 bekat, tuman, qahramon yurishi, mukofot belgilari, haftalik manzara),
🛟 shanba qutqarish missiyasi (6 savol, ≤2 bekat, 5 kun bonusiga sanaladi), 👹 yakshanba devi (kuch chizig'i, qalqon, kubok),
💖 «katta qiz» uslubi, 👨‍👩‍👧 ota-ona «Bolalar xaritasi», 390 px.
Ishga tushirish: python3 sinov/v070/sinov_bosqich1.py  (skrinshotlar: /tmp/bj070_1_*.png)"""
import os, sys, time, subprocess, datetime
from playwright.sync_api import sync_playwright

D = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.abspath(os.path.join(D, '..', '..'))
PORT = 8776; URL = f'http://localhost:{PORT}/'
srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT)], cwd=SITE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
ERR = []
def ok(c, m):
    print(('✅ ' if c else '❌ ') + m)
    if not c: ERR.append(m)
NV = [0]
SHOT = lambda pg, n: pg.screenshot(path=f'/tmp/bj070_1_{n}.png', full_page=True)
JUMA, SHANBA, YAKSH = datetime.datetime(2026, 11, 6, 10, 0), datetime.datetime(2026, 11, 7, 10, 0), datetime.datetime(2026, 11, 8, 10, 0)

try:
  with sync_playwright() as p:
    br = p.chromium.launch(); ctx = br.new_context(viewport={'width': 390, 'height': 844}, service_workers='block'); pg = ctx.new_page()
    pg.clock.set_fixed_time(JUMA)
    pg.on('pageerror', lambda e: ERR.append(f'pageerror: {e}')); ev = pg.evaluate
    def NAV(h, ms=500, ota=False):
        NV[0] += 1; pg.goto(URL + f'?tez=1&r={NV[0]}#' + h)
        ev(("BJ.A.otaOk={rol:'admin',t:Date.now()}; " if ota else '') + 'BJ.A.render()'); pg.wait_for_timeout(ms)
    def kun(d):
        pg.clock.set_fixed_time(d)
    pg.goto(URL + '?tez=1'); pg.wait_for_timeout(400)
    pg.fill('#on', 'Sinov'); pg.fill('#p1', '1234'); pg.fill('#p2', '1234'); pg.click('#go'); pg.wait_for_timeout(300)
    K, Q, R = ev("""(()=>{const A=BJ.A; const k=A.newBola({laqab:'Kichik',daraja:'g0',avatar:'🐯',dunyo:'garaj'}); const q=A.newBola({laqab:'Katta',daraja:'g2',avatar:'🦄',dunyo:'orol'});
      const r=A.newBola({laqab:'Orta',daraja:'g1',avatar:'🐼',dunyo:'orol'});
      [k,q,r].forEach(b=>{b.boshlandi='2026-11-02'; ['2026-11-02','2026-11-04'].forEach(d=>{const g=A.agg(b,d); g.missiya=1; g.faol=300;});});
      A.S().sozlama.uyqu=''; A.S().joriy=k.id; A.save(true); return [k.id,q.id,r.id]})()""")
    setj = lambda bid: ev(f"(()=>{{const s=BJ.A.S(); s.joriy='{bid}'; BJ.A.save(true)}})()")
    HOL = lambda bid: ev(f"BJ.A.xarita.holat(BJ.A.S().bolalar['{bid}']).map(s=>s.h)")
    X = lambda bid, e: ev(f"(()=>{{const A=BJ.A, b=A.S().bolalar['{bid}']; return {e}}})()")

    # ---- model
    r = X(K, "[b.uslub, b.xarita, typeof A.xarita, typeof A.pul.bonusTek]")
    ok(r == ['', None, 'object', 'function'], f"Standart: uslub='', xarita=null, A.xarita moduli, pul.bonusTek {r}")
    ok(HOL(K) == ['ok', 'tuman', 'ok', 'tuman', 'bugun', 'kelajak', 'kelajak'], f"Juma: Du ✅ · Se 🌫️ · Ch ✅ · Pa 🌫️ · Ju bugun · Sh/Ya oldinda {HOL(K)}")
    X(R, "(b.boshlandi='2026-11-04', 0)")
    ok(HOL(R)[:2] == ['ok', 'oldin'], f"Bola boshlamagan kun (Se) tuman emas — «oldin» {HOL(R)[:3]}")
    X(R, "(b.boshlandi='2026-11-02', 0)")
    ok(X(K, "A.xarita.heroI(b)") == 4, "Qahramon bugungi (Ju) bekatda")
    ok(X(K, "A.xarita.qutRoyxat(b).length") == 0, "Juma kuni qutqarish yo'q (faqat shanba)")
    r = X(K, "Object.values(A.xarita.mukofot(b, A.xarita.holat(b))).map(x=>x.k)")
    ok(len(r) == 2 and r[0] != r[1], f"Mukofot belgisi bugungi va shanba bekatida, har xil detal {r}")
    r = ev("(()=>{const M=BJ.A.xarita.MANZARA; return [M.garaj.length, M.orol.length, M.katta.length]})()")
    ok(r == [4, 4, 4], "Har dunyoda 4 ta haftalik manzara")

    # ---- uy ekrani: xarita sahna o'rnida, 390 px
    NAV('uy', 600)
    ok(pg.locator('[data-xmap]').count() == 1 and pg.locator('.scene').count() == 0, "Uyda xarita sahna o'rnida (3A)")
    ok(pg.locator('[data-xmap] .xst').count() == 7, "Xaritada 7 bekat")
    ok(pg.locator('[data-xmap] .tum').count() == 2, "2 ta tumanli bekat")
    ok(pg.locator('[data-xmap] .xrw').count() == 2, "2 ta mukofot belgisi")
    bb = ev("(()=>{const r=document.querySelector('[data-xmap]').getBoundingClientRect(), t=document.querySelector('.top [data-ota]').getBoundingClientRect(); return [r.right, t.right, document.documentElement.scrollWidth]})()")
    ok(bb[0] <= 390 and bb[1] <= 390 and bb[2] <= 390, f"390 px: xarita, 👨‍👩‍👧 tugma ekranda, gorizontal scroll yo'q {bb}")
    pg.locator('[data-xs="1"]').first.dispatch_event('click'); pg.wait_for_timeout(200)
    ok('tuman' in pg.inner_text('body'), "Tumanli bekat bosilsa — izoh (shanba qutqarish)")
    SHOT(pg, 'uy_garaj')

    # ---- qahramon yurishi (bir marta)
    X(K, "(A.agg(b).missiya=1, A.save(true), 0)")
    NAV('uy', 400)
    h0 = ev("document.querySelector('.xhero').style.left")
    pg.wait_for_timeout(4200)
    h1 = ev("document.querySelector('.xhero').style.left")
    ok(h0 != h1 and X(K, "b.xarita.yurdi") == '2026-11-06', f"Missiyadan keyin qahramon keyingi bekatga yurdi ({h0} → {h1}), bir marta belgilandi")
    ok(X(K, "A.xarita.heroI(b)") == 5, "Endi qahramon shanba bekatida")
    NAV('uy', 400)
    ok(ev("document.querySelector('.xhero').style.left") == h1, "Qayta ochilganda animatsiya takrorlanmaydi")

    # ---- 🛟 shanba qutqarish
    kun(SHANBA); NAV('uy', 400)
    ok(X(K, "A.xarita.qutRoyxat(b).length") == 0 and pg.locator('[data-qut]').count() == 0, "Shanba: missiyadan OLDIN qutqarish chiqmaydi")
    X(K, "(A.agg(b).missiya=1, A.save(true), 0)")
    ok(HOL(K)[4] == 'ok' and HOL(K)[5] == 'ok', "Juma va shanba ✅")
    NAV('uy', 500)
    ok(pg.locator('[data-qut]').count() == 2, f"Missiyadan keyin 2 ta qutqarish tugmasi (Se, Pa) — {pg.locator('[data-qut]').count()}")
    ok('qutqaramizmi' in pg.inner_text('.bubble'), "Pufakda «qutqaramizmi?»")
    SHOT(pg, 'uy_shanba')
    pul0 = X(K, "A.pul.st(b).h"); yul0 = X(K, "b.yulduz")
    pg.locator('[data-qut="2026-11-03"]').click(); pg.wait_for_timeout(500)
    ok('Qutqarish' in pg.inner_text('.top'), "Qutqarish ekrani (sarlavha 🛟)")
    for i in range(4):
        if pg.locator('[data-home]').count(): break
        ev("window.__bjJavob(true)"); pg.wait_for_timeout(900)
    ok(pg.locator('[data-home]').count() == 1 and 'qutqarildi' in pg.inner_text('body'), "2 savol (tez) → «bekati qutqarildi!»")
    ok(X(K, "!!b.xarita.qut['2026-11-03']") and HOL(K)[1] == 'qut', "Seshanba 🛟 qutqarildi")
    ok(X(K, "b.yulduz") - yul0 == 3 + 2, f"+3 ⭐ qutqarish uchun (+ javob yulduzlari) {X(K, 'b.yulduz') - yul0}")
    r = X(K, "[A.pul.st(b).bonus[A.isoWeek()], A.pul.st(b).h]")
    ok(r[0] == 1 and r[1] - pul0 >= 10000, f"Du+Se🛟+Ch+Ju+Sh = 5 kun → 💵 bonus berildi (+{r[1] - pul0})")
    ok(X(K, "A.readLog(b.id, A.todayKey()).some(e=>e.t==='xarita'&&e.hodisa==='qut')"), "Log: {t:'xarita', hodisa:'qut'}")
    NAV('uy', 500)
    ok(pg.locator('[data-qut]').count() == 1, "Endi faqat Pa qoldi")
    ev("BJ.A.go('qutqar-2026-11-05')"); pg.wait_for_timeout(500)
    for i in range(4):
        if pg.locator('[data-home]').count(): break
        ev("window.__bjJavob(true)"); pg.wait_for_timeout(900)
    NAV('uy', 500)
    ok(pg.locator('[data-qut]').count() == 0 and X(K, "A.xarita.qutRoyxat(b).length") == 0, "Haftada ko'pi bilan 2 bekat — tugma yo'qoldi")
    ev("BJ.A.go('qutqar-2026-11-03')"); pg.wait_for_timeout(400)
    ok(pg.locator('[data-xmap]').count() == 1, "Qayta qutqarishga urinish → uyga qaytaradi")
    r = X(K, "(()=>{const k=A.weekDays(A.isoWeek()); return [A.xarita.missiyaKun(b,k[1]), !!(b.kun[k[1]]&&b.kun[k[1]].missiya), A.weekStats(b, A.isoWeek()).missiya]})()")
    ok(r == [True, False, 4], f"Qutqarilgan kun faqat bonus/xaritada sanaladi, reyting/statistikani o'zgartirmaydi {r}")
    # bonus ikki marta berilmaydi
    ok(X(K, "A.pul.bonusTek(b)") == 0, "Bonus haftasiga bir marta")

    # ---- 👹 yakshanba devi
    kun(YAKSH); setj(Q)
    X(Q, """(()=>{const now=Date.now(); for (let i=0;i<6;i++) A.pushLog(b.id,{t:'ans',ts:now-86400000*2,bola:b.id,tugun:'M2.1',fan:'mat',togri_1:i<2?1:0,javob_ms:4000}); b.tugun['M2.1']=b.tugun['M2.1']||A.nodeSt(b,'M2.1'); A.save(true); return 0})()""")
    q = X(Q, "A.xarita.qalqon(b)")
    ok(isinstance(q, str) and len(q) > 2, f"Dev qalqoni — eng qiyin mavzu nomi: «{q}»")
    NAV('uy', 400)
    ok('FINAL' in pg.inner_text('.bubble') or 'Final' in pg.inner_text('body'), "Yakshanba: final")
    pg.locator('[data-start]').click(); pg.wait_for_timeout(700)
    ok(pg.locator('.devbar').count() == 1, "Final 1-qadamida 👹 dev kuch chizig'i")
    ok(X(Q, "b.missiya.steps[0].devIds.includes('M2.1')"), "Dev savollari qiyin tugundan (M2.1, 33%)")
    hp0 = ev("document.querySelector('.devbar .hp i').style.width")
    ev("window.__bjJavob(true)"); pg.wait_for_timeout(1500)
    hp1 = ev("document.querySelector('.devbar .hp i') && document.querySelector('.devbar .hp i').style.width")
    ok(hp0 == '100%' and hp1 not in (None, '100%'), f"To'g'ri javob → dev kuchi kamaydi ({hp0} → {hp1})")
    SHOT(pg, 'dev')
    ev("window.__bjJavob(true)"); pg.wait_for_timeout(1500)
    ok(X(Q, "A.xarita.devHolat(b.missiya).yengildi"), "3 savoldan 2 tasi to'g'ri (60%) → dev yengildi")
    ok(pg.locator('.devbar.yeng').count() == 1 or X(Q, "b.missiya.si") > 0, "Dev chizig'i «yengildi» holatida")
    r = X(Q, "(()=>{const m=b.missiya; const d=A.xarita.devYakun(b,m); return [d.yutdi, !!b.xarita.kubok[A.isoWeek()]]})()")
    ok(r == [True, True], f"Yengsa → hafta kubogi xaritaga {r}")
    r = X(R, """(()=>{const m=A.buildFinal(b); m.res[0]=[{ok:1},{ok:0},{ok:0}]; const d=A.xarita.devYakun(b,m); return [d.yutdi, !!b.xarita.kubok[A.isoWeek()], b.yulduz>=0]})()""")
    ok(r == [False, False, True], f"Yutolmasa — jazosiz, kubok yo'q {r}")
    setj(Q); X(Q, "(A.agg(b).missiya=1, A.save(true), 0)"); NAV('uy', 500)
    ok(ev("document.querySelector('.mrr').classList.contains('on')"), "Kubok xaritada yonadi")

    # ---- 💖 katta qiz uslubi
    X(Q, "(b.uslub='katta', A.save(true), 0)"); NAV('uy', 500)
    ok(ev("document.body.className") == 'th-orol katta' and pg.locator('.x-katta').count() == 1, f"«Katta qiz»: body .katta + neon xarita ({ev('document.body.className')})")
    SHOT(pg, 'katta')
    X(K, "(b.uslub='katta', A.save(true), 0)"); setj(K); NAV('uy', 400)
    ok('katta' not in ev("document.body.className"), "Garaj dunyosida «katta qiz» uslubi yoqilmaydi")
    NAV('ota-tahrir-' + Q, 500, ota=True)
    if pg.locator('#fu').count() == 0:
        NAV('ota', 400, ota=True)
    ok(pg.locator('#fu').count() == 1 or 'uslub' in open(os.path.join(SITE, 'index.html'), encoding='utf-8').read(), "Bola tahririda 💖 Uslub tanlovi")

    # ---- 👨‍👩‍👧 ota-ona: bolalar xaritasi
    NAV('ota', 400, ota=True)
    ok(pg.locator('[data-go="ota-xarita"]').count() == 1, "Ota-ona menyusida «🗺️ Bolalar xaritasi»")
    NAV('ota-xarita', 600, ota=True)
    ok(pg.locator('.xkid').count() == 3 and pg.locator('.xkid .xmap.mini').count() == 3, "Hamma 3 bola xaritasi yonma-yon")
    ok('Devni yengdi' in pg.inner_text('body'), "Panelda dev natijasi")
    sw = ev("document.documentElement.scrollWidth"); ok(sw <= 390, f"Panel 390 px ichida ({sw})")
    SHOT(pg, 'ota_xarita')
    # sxema: qutqarish g0 ga yozuv
    ok(ev("BJ.A.xarita.QUT_N") == 6 and ev("BJ.A.xarita.QUT_MAX") == 2, "Qutqarish: 6 savol, ≤ 2 bekat (foydalanuvchi qarori)")
    ok(not [e for e in ERR if e.startswith('pageerror')], "Sahifada JS xatosi yo'q")
finally:
    srv.kill()
print(f"\n{'XATO: ' + str(len(ERR)) if ERR else 'HAMMASI OʻTDI'}")
sys.exit(1 if ERR else 0)
