"""Bilimjon 0.7.0 — 1c-bosqich: 🎮 O'YINLAR ZALI.
Zal missiyadan keyin ochiladi, kuniga ≤ N daqiqa (sozlama), 4 yangi o'yin (🏁 turbo + 👻 arvoh, 🚦 svetofor, 🧱 devor, 🃏 xotira) + eski 3 ta,
shaxsiy rekord + 📜 guvohnoma, oila rekordlari yosh bo'yicha, vaqt hisobi, 390 px.
Ishga tushirish: python3 sinov/v070/sinov_bosqich1c.py  (skrinshotlar: /tmp/bj070_1c_*.png)"""
import os, sys, time, subprocess, datetime
from playwright.sync_api import sync_playwright

D = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.abspath(os.path.join(D, '..', '..'))
PORT = 8778; URL = f'http://localhost:{PORT}/'
srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT)], cwd=SITE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
ERR = []
def ok(c, m):
    print(('✅ ' if c else '❌ ') + m)
    if not c: ERR.append(m)
NV = [0]
SHOT = lambda pg, n: pg.screenshot(path=f'/tmp/bj070_1c_{n}.png', full_page=True)

try:
  with sync_playwright() as p:
    br = p.chromium.launch(); ctx = br.new_context(viewport={'width': 390, 'height': 844}, service_workers='block'); pg = ctx.new_page()
    pg.on('pageerror', lambda e: ERR.append(f'pageerror: {e}')); ev = pg.evaluate
    def NAV(h, ms=500):
        NV[0] += 1; pg.goto(URL + f'?tez=1&r={NV[0]}#' + h); ev('BJ.A.render()'); pg.wait_for_timeout(ms)
    def GO(h, ms=400):
        ev(f"location.hash='{h}'"); pg.wait_for_timeout(ms)
    pg.goto(URL + '?tez=1'); pg.wait_for_timeout(400)
    pg.fill('#on', 'Sinov'); pg.fill('#p1', '1234'); pg.fill('#p2', '1234'); pg.click('#go'); pg.wait_for_timeout(300)
    K, Q, R = ev("""(()=>{const A=BJ.A; const k=A.newBola({laqab:'Kichik',daraja:'g0',avatar:'🐯',dunyo:'garaj'}); const q=A.newBola({laqab:'Katta',daraja:'g2',avatar:'🦄',dunyo:'orol'});
      const r=A.newBola({laqab:'Orta',daraja:'g1',avatar:'🐼',dunyo:'garaj'});
      A.S().sozlama.uyqu=''; A.S().joriy=k.id; A.save(true); return [k.id,q.id,r.id]})()""")
    setj = lambda bid: ev(f"(()=>{{const s=BJ.A.S(); s.joriy='{bid}'; BJ.A.save(true)}})()")
    X = lambda bid, e: ev(f"(()=>{{const A=BJ.A, b=A.S().bolalar['{bid}']; return {e}}})()")
    W390 = lambda: ev("[document.documentElement.scrollWidth, Math.max(...[...document.querySelectorAll('.top .ib, .top .pill')].map(e=>e.getBoundingClientRect().right), 0)]")

    # ---- model va standartlar
    r = X(K, "[typeof A.zal, A.S().sozlama.zal, b.zal, A.zal.holat(b).k, A.zal.limitDaq(), typeof A.oyin.zalRun, A.FAN.zal.nom]")
    ok(r == ['object', 10, None, 'qulf', 10, 'function', "O'yinlar zali"], f"Modul, sozlama.zal=10, b.zal=null, missiyagacha qulf {r}")
    ok(X(K, "(()=>{const s=A.migrate(JSON.parse(JSON.stringify(Object.assign({}, A.S(), {sozlama: {ovoz: .5}})))); return s.sozlama.zal})()") == 10, "Eski holatdan yangilanganda sozlama.zal = 10")

    # ---- qulf: uy tugmasi va ekran
    NAV('uy')
    ok(pg.locator('[data-zal].qulf').count() == 1 and '🔒' in pg.inner_text('[data-zal]'), "Uyda zal tugmasi 🔒 (missiyadan keyin)")
    pg.click('[data-zal]'); pg.wait_for_timeout(200)
    ok('missiyani bajar' in pg.inner_text('body') and ev("location.hash") in ('#uy', ''), "Qulf tugma bosilsa — toast, zalga o'tmaydi")
    GO('zal')
    ok('Zal hali yopiq' in pg.inner_text('body'), "#zal to'g'ridan-to'g'ri — «yopiq» ekrani")
    GO('zal-turbo')
    ok('Zal hali yopiq' in pg.inner_text('body') and pg.locator('canvas.zcv').count() == 0, "#zal-turbo ham missiyasiz ochilmaydi")

    # ---- ochiq
    X(K, "(A.agg(b).missiya=1, A.save(true), 0)")
    NAV('uy')
    ok(pg.locator('[data-zal].ochiq.pulse').count() == 1 and '10 daq' in pg.inner_text('[data-zal]'), "Missiyadan keyin zal ochiq, ⏱ 10 daq, yorqin tugma")
    w = W390(); ok(w[0] <= 390 and w[1] <= 390, f"390 px: uy ekrani {w}")
    pg.click('[data-zal]'); pg.wait_for_timeout(400)
    ok(ev("location.hash") == '#zal' and pg.locator('.zcard').count() == 7, "Zal: 7 ta o'yin kartasi")
    ok(pg.locator('.zcard .zbad').count() == 4, "4 ta yangi o'yinda «YANGI» belgisi")
    w = W390(); bb = ev("Math.max(...[...document.querySelectorAll('.zcard')].map(e=>e.getBoundingClientRect().right))")
    ok(w[0] <= 390 and bb <= 390, f"390 px: zal ekrani {w} {bb}")
    SHOT(pg, 'zal')

    # ---- misol generatori
    r = ev("""(()=>{const Z=BJ.A.zal; let bad=[]; for (const g of ['g0','g1','g2']) for (let lv=0; lv<9; lv++) for (let i=0;i<300;i++){ const T=Z.misol(g,lv);
      const vs=T.o.map(o=>o.v); if (T.o.length!==3 || new Set(vs).size!==3 || T.a<0 || T.a>2) { bad.push([g,lv,'opt',vs]); continue; }
      if (T.k==='mat') { const e=T.sav.v.replace('×','*').replace('−','-').replace(':','/'); const n=eval(e); if (n!==vs[T.a] || !Number.isInteger(n) || n<0 || vs.some(v=>v<0)) bad.push([g,lv,T.sav.v,vs,T.a]); }
      if (T.k==='son' && vs[T.a]!==T.sav.v) bad.push([g,lv,'son']); if (T.k==='rang' && vs[T.a]!==T.sav.v) bad.push([g,lv,'rang']); }
      return bad.slice(0,5)})()""")
    ok(r == [], f"misol: 8 100 topshiriq — 3 ta har xil variant, javob to'g'ri, manfiy yo'q {r}")
    r = ev("(()=>{const Z=BJ.A.zal; return [Z.misol('g0',0).k, Z.misol('g0',4).k, Z.misol('g1',0).k, Z.misol('g2',5).k]})()")
    ok(r == ['rang', 'son', 'mat', 'mat'], f"Yosh bo'yicha: g0 rang → son, g1/g2 misol {r}")

    # ---- 🏁 TURBO GONKA
    def turbo(togri=True):
        GO('zal', 150); GO('zal-turbo', 300)
        for _ in range(400):
            s = ev("(()=>{const S=window.__bjZal(); return S && S.game ? S.game.state() : null})()")
            if not s or s['fin']: break
            if s['a'] is not None: ev(f"window.__bjZal().game.setLane({s['a'] if togri else (s['a'] + 1) % 3})")
            pg.wait_for_timeout(40)
        pg.wait_for_timeout(500)
    GO('zal-turbo', 300)
    ok(pg.locator('canvas.zcv').count() == 1 and pg.locator('[data-goal]').count() == 1, "Turbo: canvas + 🎯 topshiriq paneli")
    s = ev("window.__bjZal().game.state()")
    ok(s['N'] == 3 and s['gh'] is False and s['k'] == 'rang', f"Turbo (tez): 3 darvoza, arvoh hali yo'q, maktabgacha — rang {s}")
    SHOT(pg, 'turbo')
    w = W390(); ok(w[0] <= 390, f"390 px: turbo {w}")
    turbo(True)
    txt = pg.inner_text('body')
    ok('YANGI REKORD' in txt and pg.locator('.zguv svg').count() == 1, "Turbo tugadi → 🏆 YANGI REKORD + 📜 guvohnoma")
    r = X(K, "[b.zal.rek.turbo && b.zal.rek.turbo.v > 0, b.zal.rek.turbo.n, b.zal.arvoh && b.zal.arvoh.s.length > 3, b.zal.arvoh.n, b.zal.guv.length, b.zal.son.turbo]")
    ok(r == [True, 3, True, 3, 1, 2], f"Rekord (vaqt, n=3), 👻 arvoh yozildi, guvohnoma 1, o'ynalgan 2 marta {r}")
    ok('3/3 darvoza' in txt, "Natija izohi: 3/3 darvoza to'g'ri")
    lg = X(K, "A.readLog(b.id, A.todayKey()).filter(e=>e.t==='zal').map(e=>[e.tur,e.rek,e.erta])")
    ok(['turbo', 1, 0] in lg and ['turbo', 0, 1] in lg, f"Log: {{t:'zal'}} rekord va erta chiqish yozildi {lg}")
    SHOT(pg, 'turbo_rekord')
    v1 = X(K, "b.zal.rek.turbo.v")
    pg.click('[data-yana]'); pg.wait_for_timeout(300)
    ok(ev("window.__bjZal().game.state().gh") is True and '👻' in pg.inner_text('[data-gh]'), "Ikkinchi poyga: 👻 arvoh bor")
    turbo(False)
    txt = pg.inner_text('body')
    ok('YANGI REKORD' not in txt and 'Rekording' in txt and X(K, "b.zal.rek.turbo.v") == v1, f"Xato yo'laklar → sekinroq, rekord o'zgarmadi ({v1} s), «Rekording … yetasan»")
    ok('0/3 darvoza' in txt, "Natija izohi: 0/3")

    # ---- 🚦 SVETOFOR
    GO('zal-svetofor', 300)
    ok(pg.locator('[data-gz]').count() == 1 and pg.locator('[data-br]').count() == 1, "Svetofor: GAZ va TORMOZ pedallari")
    SHOT(pg, 'svetofor')
    for _ in range(200):
        s = ev("window.__bjZal() && window.__bjZal().game.state()")
        if not s or s['fin']: break
        ev(f"window.__bjZal().game.gas({'true' if s['ph'] == 'yashil' else 'false'}); window.__bjZal().game.brake({'true' if s['ph'] != 'yashil' else 'false'})")
        pg.wait_for_timeout(30)
    pg.wait_for_timeout(400)
    sv = X(K, "b.zal.rek.svetofor")
    ok(sv and sv['v'] > 0 and 'YANGI REKORD' in pg.inner_text('body') and '0 ta jarima' in pg.inner_text('body'), f"Svetofor: qoidaga amal qilib yurdi — masofa rekord, jarimasiz {sv}")
    GO('zal', 200); GO('zal-svetofor', 300)
    for _ in range(200):
        s = ev("window.__bjZal() && window.__bjZal().game.state()")
        if not s or s['fin']: break
        ev("window.__bjZal().game.gas(true)"); pg.wait_for_timeout(30)
    pg.wait_for_timeout(400)
    ok('jarima' in pg.inner_text('body') and '0 ta jarima' not in pg.inner_text('body'), "Qizilda gaz bosib tursa — 🚨 jarima yoziladi")

    # ---- 🧱 DEVOR SINDIRISH
    GO('zal', 200); GO('zal-devor', 300)
    ok(pg.locator('.dvb').count() == 3 and pg.locator('.dvtop svg').count() == 1, "Devor: spidometr + 3 javob tugmasi")
    SHOT(pg, 'devor')
    def devor_javob(togri):
        s = ev("window.__bjZal().game.state()"); ev(f"window.__bjZal().game.javob({s['a'] if togri else (s['a'] + 1) % 3})"); pg.wait_for_timeout(150)
    devor_javob(True); devor_javob(True); pg.wait_for_timeout(1700)
    s = ev("window.__bjZal().game.state()")
    ok(s['lvl'] == 1 and s['need'] == 55, f"2 to'g'ri javob → tezlik yetdi → 💥 1-devor sindi, keyingisi 55 km/soat {s}")
    devor_javob(False); devor_javob(False); pg.wait_for_timeout(1700)
    s = ev("window.__bjZal().game.state()")
    ok(s['lvl'] == 1 and s['tries'] == 1, f"Xato javoblar → tezlik yetmadi, urinish −1 {s}")
    devor_javob(False); devor_javob(False); pg.wait_for_timeout(1900)
    ok(X(K, "b.zal.rek.devor && b.zal.rek.devor.v") == 1 and 'ta devor' in pg.inner_text('body'), "2 marta chidadi → o'yin tugadi, rekord 1 ta devor")

    # ---- 🃏 GARAJ XOTIRASI
    GO('zal', 200); GO('zal-xotira', 300)
    s = ev("window.__bjZal().game.state()")
    ok(s['P'] == 2 and len(s['deck']) == 4 and pg.locator('.xk').count() == 4, f"Xotira (tez): 2 juft, 4 karta {s['deck']}")
    SHOT(pg, 'xotira')
    d = s['deck']; a0 = d[0]; j = d.index(a0, 1); other = [i for i in range(4) if i not in (0, j)]
    ev(f"window.__bjZal().game.flip(0)"); ev(f"window.__bjZal().game.flip({other[0]})"); pg.wait_for_timeout(200)
    ok(ev("window.__bjZal().game.state().moves") == 1 and pg.locator('.xk.on').count() == 0, "Har xil juft → yopildi, 1 yurish")
    for i in (0, j, other[0], other[1]): ev(f"window.__bjZal().game.flip({i})"); pg.wait_for_timeout(120)
    pg.wait_for_timeout(300)
    ok(X(K, "b.zal.rek.xotira && [b.zal.rek.xotira.v, b.zal.rek.xotira.n]") == [3, 2], "Hammasi topildi → rekord 3 yurish (2 juft)")

    # ---- eski o'yinlar zalda: poyga / pazl
    GO('zal', 200); GO('zal-poyga', 300)
    S = ev("(()=>{const S=window.__bjOyin(); return S && [S.zal, S.tur, S.sek]})()")
    ok(S == [True, 'poyga', 6], f"Poyga zal rejimida (A.oyin.zalRun, 6 s tez) {S}")
    ok('Zalga' in pg.inner_text('[data-qayt]'), "Tugma «↩ Zalga»")
    for _ in range(60):
        st = ev("(()=>{const S=window.__bjOyin(); return S && S.game ? S.game.state() : null})()")
        if not st: break
        if st['a'] is not None: ev(f"window.__bjOyin().game.setLane({st['a']})")
        pg.wait_for_timeout(150)
    pg.wait_for_timeout(5000)
    ok(X(K, "b.zal.rek.poyga && b.zal.rek.poyga.v") and pg.locator('.zres').count() == 1, f"Poyga tugadi → zal natija ekrani, rekord {X(K, 'b.zal.rek.poyga')}")
    ok(X(K, "A.readLog(b.id, A.todayKey()).filter(e=>e.t==='oyin').length") == 0, "Zal o'yini «dam olish o'yini» logiga yozilmaydi")

    # ---- erta chiqish (hash o'zgarsa)
    GO('zal', 200); GO('zal-svetofor', 300); GO('uy', 1200)
    lg = X(K, "A.readLog(b.id, A.todayKey()).filter(e=>e.t==='zal' && e.tur==='svetofor').map(e=>e.erta)")
    ok(lg[-1] == 1 and ev("window.__bjZal()") is None, f"O'yindan chiqib ketsa — seans yopiladi, erta=1 {lg}")

    # ---- vaqt hisobi va chegara
    s0 = X(K, "A.zal.qoldi(b)")
    ok(s0 < 600, f"O'ynalgan vaqt sanaldi: qolgan {s0} s < 600")
    X(K, "(b.zal.sek[A.todayKey()] = 600 - 1, A.save(true), 0)")
    GO('zal-svetofor', 300); pg.wait_for_timeout(1400)
    ok(pg.locator('.zres').count() == 1 and 'tugadi' in pg.inner_text('body'), "Zal vaqti tugadi → o'yin yakunlandi, «Bugungi zal vaqti tugadi»")
    ok(pg.locator('[data-yana][disabled]').count() == 1, "«Yana» tugmasi o'chiq")
    NAV('uy')
    ok('bugun tugadi' in pg.inner_text('[data-zal]'), "Uyda: «bugun tugadi»")
    GO('zal'); ok('vaqti tugadi' in pg.inner_text('body'), "Zal ekrani: «Bugungi zal vaqti tugadi»")

    # ---- ota-ona sozlamasi
    ev("BJ.A.otaOk={rol:'admin',t:Date.now()}"); GO('ota-sozlama', 400)
    ok(pg.locator('#zl').count() == 1 and ev("document.querySelector('#zl').value") == '10', "⚙️ Sozlamalar: 🕹️ zal daqiqasi (10)")
    pg.select_option('#zl', '20'); pg.click('[data-save]'); pg.wait_for_timeout(300)
    ok(ev("BJ.A.S().sozlama.zal") == 20 and X(K, "A.zal.qoldi(b)") > 500, "20 daqiqa saqlandi → yana vaqt bor")
    ev("BJ.A.S().sozlama.zal = 0; BJ.A.save(true)"); NAV('uy')
    ok(pg.locator('[data-zal]').count() == 0, "0 — zal yopiq: uyda tugma yo'q")
    GO('zal'); ok('Zal yopiq' in pg.inner_text('body'), "#zal → «ota-ona o'chirgan»")
    ev("BJ.A.S().sozlama.zal = 10; BJ.A.save(true)"); X(K, "(b.zal.sek={}, A.save(true), 0)")

    # ---- oila rekordlari (yosh bo'yicha) va boshqa bolalar
    setj(Q); X(Q, "(A.agg(b).missiya=1, A.save(true), 0)")
    NAV('zal-turbo', 300)
    ok(ev("window.__bjZal().game.state().k") == 'mat', "2-sinf bolasida turbo darvozalari — misol")
    turbo(True)
    ok(X(Q, "!!b.zal.rek.turbo") and X(Q, "b.zal.arvoh.g") == 'g2', "Katta qizning o'z rekordi va arvohi (g2)")
    setj(R); X(R, "(A.agg(b).missiya=1, A.save(true), 0)")
    NAV('zal-xotira', 300)
    ok(ev("window.__bjZal().game.state().P") == 2, "1-sinf: xotira")
    ev("window.__bjZal().game.stop()")
    NAV('zal-rekord', 400)
    t = pg.inner_text('body')
    ok(t.count('Maktabgacha') == 7 and t.count('2-sinf va kattalar') == 7 and t.count('1-sinf') == 7, "Oila rekordlari: har o'yinda 3 yosh guruhi alohida")
    ok(pg.locator('.zrw.men').count() == 7, "O'z qatori ajratilgan (sen)")
    w = W390(); ok(w[0] <= 390, f"390 px: rekordlar {w}")
    SHOT(pg, 'rekord')

    # ---- guvohnomalar
    setj(K); NAV('zal-guv', 400)
    ok(pg.locator('.zgv').count() == X(K, "b.zal.guv.length") >= 4, f"📜 Guvohnomalar ro'yxati ({X(K, 'b.zal.guv.length')})")
    pg.locator('.zgv').first.click(); pg.wait_for_timeout(300)
    ok(pg.locator('.sheet .zguv svg').count() == 1 and pg.locator('.sheet [data-png]').count() == 1, "Guvohnoma ochiladi + «💾 Rasm qilib saqlash»")
    with pg.expect_download(timeout=5000) as dl:
        pg.click('.sheet [data-png]')
    ok(dl.value.suggested_filename.endswith('.png'), f"PNG yuklab olindi: {dl.value.suggested_filename}")
    SHOT(pg, 'guvohnoma')

    # ---- rekord taqqoslash qoidasi
    r = ev("""(()=>{const Z=BJ.A.zal; return [Z.yaxshiMi('turbo', 9, {v:10,n:3}, 3), Z.yaxshiMi('turbo', 11, {v:10,n:3}, 3), Z.yaxshiMi('svetofor', 0, null, 0),
      Z.yaxshiMi('svetofor', 50, {v:40}, 0), Z.yaxshiMi('xotira', 20, {v:10,n:6}, 8)]})()""")
    ok(r == [True, False, False, True, True], f"Rekord: vaqt/yurish — kam yaxshi, masofa — ko'p, 0 — rekord emas, boshqa o'lcham — yangi {r}")

    # ---- orol dunyosi: ko'rinish
    setj(Q); NAV('zal', 400)
    SHOT(pg, 'zal_orol')
    GO('zal-xotira', 300)
    ok(pg.locator('.xm.orol').count() == 1, "Orol bolasida xotira kartalari — kristall uslub")
    ev("window.__bjZal().game.stop()")

    ok(not [e for e in ERR if e.startswith('pageerror')], "Sahifa xatosiz (pageerror yo'q)")
    br.close()
finally:
    srv.terminate()
print('\nJAMI XATO:', len(ERR))
for e in ERR: print(' -', e)
sys.exit(1 if ERR else 0)
