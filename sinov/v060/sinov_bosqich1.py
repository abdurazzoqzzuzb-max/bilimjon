"""Bilimjon 0.6.0 — 1-bosqich: 🌙 kun chegarasi + uyqu, 🎮 o'yin sozlamasi har bolaga, ⚖️ adolatli reyting, 💥 kombo.
Ishga tushirish: python3 sinov/v060/sinov_bosqich1.py  (skrinshotlar: /tmp/bj060_*.png)"""
import os, sys, time, subprocess
from playwright.sync_api import sync_playwright

D = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.abspath(os.path.join(D, '..', '..'))
PORT = 8771; URL = f'http://localhost:{PORT}/'
srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT)], cwd=SITE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
ERR = []
def ok(c, m):
    print(('✅ ' if c else '❌ ') + m)
    if not c: ERR.append(m)

with sync_playwright() as p:
    br = p.chromium.launch()
    ctx = br.new_context(viewport={'width': 390, 'height': 844}, service_workers='block'); pg = ctx.new_page()
    pg.on('pageerror', lambda e: ERR.append(f'pageerror: {e}'))
    ev = pg.evaluate
    # ---- eski (0.5.1) holatdan yangilanish: yangi maydonlarsiz holat
    pg.goto(URL); pg.wait_for_timeout(400)
    pg.fill('#on', 'Sinov'); pg.fill('#p1', '1234'); pg.fill('#p2', '1234'); pg.click('#go'); pg.wait_for_timeout(300)
    ids = ev("""(()=>{const A=BJ.A; const k=A.newBola({laqab:'Kichik',daraja:'g0',avatar:'🐯',dunyo:'garaj'}); const q=A.newBola({laqab:'Katta',daraja:'g2',avatar:'🦄',dunyo:'orol'});
      const s=A.S(); delete s.sozlama.uyqu; [k,q].forEach(b=>{['kunDaq','oyinHar','oyinDaq','oyinMin','qoshDaq','uyquOchiq','komboMax'].forEach(f=>delete b[f]);}); A.save(true); return [k.id,q.id]})()""")
    pg.reload(); pg.wait_for_timeout(500)
    m = ev("(()=>{const s=BJ.A.S(), b=s.bolalar[Object.keys(s.bolalar)[0]]; return {uyqu:s.sozlama.uyqu, q: JSON.stringify(b.qoshDaq), kd: b.kunDaq}})()")
    ok(m['uyqu'] == '21:00' and m['q'] == '{}' and m['kd'] is None, f'Eski holatdan yangilanish: uyqu 21:00, yangi maydonlar to\'ldi {m}')
    K, Q = ids
    # ---- 🌙 kun chegarasi
    ev("BJ.A.S().sozlama.uyqu=''; BJ.A.save(true)")
    lim = ev(f"[BJ.A.kunLimit(BJ.A.S().bolalar['{K}']), BJ.A.kunLimit(BJ.A.S().bolalar['{Q}'])]")
    ok(lim == [25, 35], f'Standart chegara: maktabgacha 25, 2-sinf 35 ({lim})')
    ok(ev(f"(()=>{{const b=BJ.A.S().bolalar['{K}']; b.kunDaq=0; const r=BJ.A.qolganSek(b)===Infinity && !BJ.A.damHolat(b); b.kunDaq=null; return r}})()"), '«Cheklanmagan» (0) — hech qachon to\'xtamaydi')
    ev(f"(()=>{{const s=BJ.A.S(); s.joriy='{K}'; BJ.A.agg(s.bolalar['{K}']).faol=25*60; BJ.A.save(true)}})()")
    pg.goto(URL + '#missiya'); pg.wait_for_timeout(500)
    ok(pg.locator('.dam').count() == 1 and 'yetarli' in pg.inner_text('.ttl'), 'Chegaraga yetgan bola missiyani ochsa — «😴 Bugunga yetarli» ekrani')
    pg.screenshot(path='/tmp/bj060_dam_limit.png')
    pg.goto(URL + '#arena'); pg.wait_for_timeout(300); ok(pg.locator('.dam').count() == 1, 'Arena ham yopiq')
    pg.goto(URL + '#mashq'); pg.wait_for_timeout(300); ok(pg.locator('.dam').count() == 1, 'Mashq ham yopiq')
    pg.click('[data-qosh]'); pg.fill('#dp', '9999'); pg.click('.sheet [data-ok]'); pg.wait_for_timeout(200)
    ok(ev(f"BJ.A.kunLimit(BJ.A.S().bolalar['{K}'])+((BJ.A.S().bolalar['{K}'].qoshDaq||{{}})[BJ.A.todayKey()]||0)") == 25, "Noto'g'ri PIN — vaqt qo'shilmadi")
    pg.fill('#dp', '1234'); pg.click('.sheet [data-ok]'); pg.wait_for_timeout(500)
    ok(pg.locator('.dam').count() == 0 and ev(f"Math.round(BJ.A.qolganSek(BJ.A.S().bolalar['{K}'])/60)") == 10, 'To\'g\'ri PIN — +10 daqiqa, mashq ochildi')
    lg = ev(f"BJ.A.readLog('{K}',BJ.A.todayKey()).filter(e=>e.t==='dam').length"); ok(lg == 1, 'Log: {t:"dam"} yozildi')
    # missiya davom etayotgan bo'lsa — 15 daqiqa imtiyoz
    g = ev(f"""(()=>{{const b=BJ.A.S().bolalar['{K}'], d=BJ.A.agg(b); d.faol=(25+10+5)*60; const a=!!BJ.A.damHolat(b), c=!BJ.A.damHolat(b,true); d.faol=(25+10+16)*60; const e=!!BJ.A.damHolat(b,true); d.faol=0; return [a,c,e]}})()""")
    ok(g == [True, True, True], f'Boshlangan missiyaga 15 daq imtiyoz, keyin to\'xtaydi ({g})')
    # ---- uyqu vaqti
    u = ev("""(()=>{const A=BJ.A, z=A.S().sozlama; z.uyqu='21:00'; const d=h=>{const x=new Date(); x.setHours(h,10,0,0); return x;};
      return [A.uyquMi(d(21)), A.uyquMi(d(23)), A.uyquMi(d(3)), A.uyquMi(d(6)), A.uyquMi(d(20))]})()""")
    ok(u == [True, True, True, False, False], f'Uyqu oralig\'i 21:00–05:00 ({u})')
    ev("""(()=>{const x=new Date(Date.now()-60000); BJ.A.S().sozlama.uyqu=String(x.getHours()).padStart(2,'0')+':'+String(x.getMinutes()).padStart(2,'0'); BJ.A.save(true)})()""")
    hh = ev("new Date().getHours()")
    if hh >= 5:
        pg.goto(URL + '#arena'); pg.wait_for_timeout(400)
        ok(pg.locator('.dam').count() == 1 and 'Uxlash' in pg.inner_text('.ttl'), 'Uxlash vaqti — arena o\'rniga «🌙 Uxlash vaqti»')
        pg.screenshot(path='/tmp/bj060_dam_uyqu.png')
        pg.click('[data-qosh]'); pg.fill('#dp', '1234'); pg.click('.sheet [data-ok]'); pg.wait_for_timeout(500)
        ok(pg.locator('.dam').count() == 0, 'Uyquda PIN bilan +10 daqiqa ochildi')
    ev("BJ.A.S().sozlama.uyqu=''; BJ.A.save(true)")
    # ---- uy ekranida qolgan vaqt
    pg.goto(URL + '#uy'); pg.wait_for_timeout(400)
    ok('daqiqa' in pg.inner_text('.kidw'), 'Uy ekranida «⏳ Bugun yana N daqiqa»')
    # ---- 🎮 o'yin sozlamasi har bolaga
    c = ev(f"""(()=>{{const A=BJ.A, s=A.S(), k=s.bolalar['{K}'], q=s.bolalar['{Q}']; s.sozlama.oyinHar=5; s.sozlama.oyinMin=3; k.oyinHar=3; k.oyinMin=2; q.oyinHar=null;
      const r=[A.oyinCfg(k), A.oyinCfg(q)]; k.oyinHar=0; r.push(A.oyinCfg(k)); k.oyinHar=3; return r.map(x=>[x.har,x.daq])}})()""")
    ok(c == [[3, 2], [5, 3], [0, 2]], f'O\'yin sozlamasi: bola o\'zi 3/2, oila 5/3, o\'chiq 0 ({c})')
    ev("BJ.A.otaOk={rol:'admin',t:Date.now()}"); pg.goto(URL + f'#ota-tahrir-{K}'); pg.wait_for_timeout(400)
    has = pg.locator('#fz').count() == 1 and pg.locator('#fo').count() == 1 and pg.locator('#fp').count() == 1
    ok(has, 'Bola tahririda: ⏳ kunlik vaqt, 🎮 o\'yin, ⏱ davomiylik')
    if has:
        pg.screenshot(path='/tmp/bj060_forma.png', full_page=True)
    # ---- ⚖️ adolatli reyting
    r = ev(f"""(()=>{{const A=BJ.A, s=A.S(), k=s.bolalar['{K}'], q=s.bolalar['{Q}'], t=A.todayKey(); A.agg(k).missiya=0; A.agg(q).missiya=1; A.agg(q).faol=900;
      k.yulduzKun[t]=69; q.yulduzKun[t]=13; A.save(true); return A.reytingRoyxat().map(x=>[x.laqab,x.maqsad])}})()""")
    ok(r[0][0] == 'Katta' and r[0][1] > r[1][1], f'Reyting: missiyani bajargan (⭐13) ⭐69 li bolaning oldida ({r})')
    pg.goto(URL + '#uy'); pg.wait_for_timeout(400)
    ok('🎯' in pg.inner_text('.rey'), 'Bola ekranidagi reytingda 🎯 maqsad ko\'rsatkichi')
    # ---- 💥 kombo (tez rejim, arena)
    pg.goto(URL + '?tez=1#arena'); pg.wait_for_timeout(600)
    for i in range(5):
        ev("(()=>{const C=BJ.A.CUR(); BJ.A.onAnswer(C.b,null,null,C.it,C.st,{togri:true,javob:C.it.a,el:document.body})})()")
        if i == 2: pg.wait_for_timeout(250); ok(pg.locator('.kombo').count() == 1, '3 ta ketma-ket to\'g\'ri → «🔥 3 KOMBO!»'); pg.screenshot(path='/tmp/bj060_kombo.png')
        pg.wait_for_timeout(1700)
    km = ev(f"[BJ.A.agg(BJ.A.S().bolalar[BJ.A.S().joriy]).komboMax, BJ.A.S().bolalar[BJ.A.S().joriy].komboMax]")
    ok(km[0] >= 5 and km[1] >= 5, f'Kombo rekordi saqlandi ({km})')
    ev("(()=>{const C=BJ.A.CUR(); BJ.A.onAnswer(C.b,null,null,C.it,C.st,{togri:false,javob:'x',el:document.body,yakuniy:1})})()"); pg.wait_for_timeout(300)
    kl = ev(f"BJ.A.readLog(BJ.A.S().joriy,BJ.A.todayKey()).filter(e=>e.t==='kombo').map(e=>e.n)")
    ok(kl[:2] == [3, 5], f'Log: kombo 3 va 5 da yozildi ({kl})')
    br.close()
srv.terminate()
print('\nXATOLAR:', ERR if ERR else "yo'q"); sys.exit(1 if ERR else 0)
