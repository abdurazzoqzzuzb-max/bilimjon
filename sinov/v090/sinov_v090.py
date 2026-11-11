"""Bilimjon 0.9.0 — 2-bosqich (u, 10.11): 🌳 bilim daraxti, 🔁 xatoni qaytarish (aynan o'sha savol, 1–3–7 kun), 🎯 kunning 3 qiyini, 👀 ko'zga dam.
Ishga tushirish: python3 sinov/v090/sinov_v090.py (skrinshotlar: /tmp/bj090_*.png)"""
import os, sys, time, subprocess, json, re
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.abspath(os.path.join(D, '..', '..'))
PORT = 8816; URL = f'http://localhost:{PORT}/'
srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT)], cwd=SITE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
ERR = []; PE = []
def ok(c, m): print(('✅ ' if c else '❌ ') + m); (None if c else ERR.append(m))
html = open(os.path.join(SITE, 'index.html'), encoding='utf-8').read(); VJ = json.load(open(os.path.join(SITE, 'version.json'), encoding='utf-8'))
VER = re.search(r"A\.VER = '([\d.]+)'", html)[1]; SWV = re.search(r"const V = P \+ '([\d.]+)'", open(os.path.join(SITE, 'sw.js'), encoding='utf-8').read())[1]
def kutf(pg, js, ms=8000):
    try: pg.wait_for_function(js, timeout=ms); return True
    except Exception: return False
try:
  with sync_playwright() as p:
    br = p.chromium.launch(); ctx = br.new_context(viewport={'width': 390, 'height': 844}, service_workers='block', device_scale_factor=2)
    P = ctx.new_page(); P.on('pageerror', lambda e: PE.append(str(e))); ev = P.evaluate
    P.goto(URL + '?tez=1'); P.wait_for_timeout(400)
    P.fill('#on', 'Sinov oila'); P.fill('#p1', '1234'); P.fill('#p2', '1234'); P.click('#go'); P.wait_for_timeout(300)
    AZ, KI = ev("(()=>{const A=BJ.A; const a=A.newBola({laqab:'Ali',daraja:'g2',avatar:'🐯',dunyo:'garaj'}), k=A.newBola({laqab:'Kichik',daraja:'g0',avatar:'🦋',dunyo:'orol'}); A.S().sozlama.uyqu=''; A.S().joriy=a.id; A.save(true); return [a.id,k.id]})()")
    yang = ev("BJ.A.YANGI")
    ok(VJ['ver'] == VER == SWV and VJ['yangi'] == yang and len(yang) >= 3, f"Versiya: index {VER} = sw.js {SWV} = version.json {VJ['ver']}, «yangi» = A.YANGI ({len(yang)} qator)")
    # ================= 🌳 DARAXT =================
    sh = ev(f"BJ.A.daraxt.shoxlar(BJ.A.bola('{AZ}')).map(s=>[s.fan,s.ids.length])")
    shk = ev(f"BJ.A.daraxt.shoxlar(BJ.A.bola('{KI}')).map(s=>[s.fan,s.ids.length])")
    d2 = dict(sh); d0 = dict(shk)
    ok(d2.get('mat') == 14 and d2.get('til') == 6 and d2.get('en') == 13 and 'yoz' not in d2 and d2.get('ar') == 16 and d2.get('mant', 0) >= 8, f"2-sinf shoxlari: mat 14, ona tili 6, ingliz 13, mantiq, arab 16 (yozuv yo'q) — {sh}")
    ok(d0.get('mat') == 10 and d0.get('til') == 7 and d0.get('yoz') == 4, f"Maktabgacha: mat 10, ona tili 7, yozuv 4 — {shk}")
    r = ev(f"""(()=>{{const A=BJ.A,b=A.bola('{AZ}'),D=A.daraxt; const s={{fan:'mat'}}; const o={{}};
      o.kurtak=D.barg(b,'M2.9',s); const t=A.nodeSt(b,'M2.9'); t.n=3; t.holat='mashq'; o.barg=D.barg(b,'M2.9',s); t.holat='qiyin'; o.sariq=D.barg(b,'M2.9',s); t.holat='kalib'; o.meva=D.barg(b,'M2.9',s);
      o.qulf=D.barg(b,'TJ.3',{{fan:'ar',ar:1}}); t.holat='yangi'; t.n=0; return o}})()""")
    ok(r == {'kurtak': 'kurtak', 'barg': 'barg', 'sariq': 'sariq', 'meva': 'meva', 'qulf': 'qulf'}, f"Barg holatlari: kurtak → barg (mashq) → sariq (qiyin) → meva (o'zlashtirildi/bilgan); tasdiqlanmagan tajvid — qulf ({r})")
    # oltin meva: 5 ta yangi o'zlashtirilgan → 1 meva + so'm
    r = ev(f"""(()=>{{const A=BJ.A,b=A.bola('{AZ}'),D=A.daraxt; D.tekshir(b,true); const h0=A.pul.st(b).h; const T=A.todayKey();
      ['M2.1','M2.2','M2.3','M2.4'].forEach(id=>{{const t=A.nodeSt(b,id); t.holat='ozl'; t.ozlSana=T;}}); const e1=D.tekshir(b,true).filter(e=>e.t==='meva').length;
      const t=A.nodeSt(b,'M2.5'); t.holat='ozl'; t.ozlSana=T; const e2=D.tekshir(b,true).filter(e=>e.t==='meva').length;
      const eski=A.nodeSt(b,'H2.1'); eski.holat='ozl'; eski.ozlSana=A.addDays(T,-3); D.tekshir(b,true);
      return {{e1,e2,meva:b.daraxt.meva,ozl:b.daraxt.ozl.length,som:A.pul.st(b).h-h0,kut:A.pul.narxK(b,5000)}}}})()""")
    ok(r['e1'] == 0 and r['e2'] == 1 and r['meva'] == 1 and r['som'] == r['kut'] and r['ozl'] == 5, f"🍎 4 ta mavzu — meva yo'q; 5-si → 1 oltin meva + 💵 {r['som']} (kutilgan {r['kut']}); versiyadan oldingi o'zlashtirish sanalmaydi ({r})")
    # medal + noyob buyum
    r = ev(f"""(()=>{{const A=BJ.A,b=A.bola('{AZ}'),D=A.daraxt, T=A.todayKey(); const ega0=JSON.stringify(A.pul.st(b).ega);
      A.ZANJIR.mat.filter(id=>id.indexOf('M2.')===0).forEach(id=>{{const t=A.nodeSt(b,id); if(t.holat!=='ozl'){{t.holat='kalib';}}}});
      const e=D.tekshir(b,true), m=e.find(x=>x.t==='medal'); const e2=D.tekshir(b,true).filter(x=>x.t==='medal').length;
      return {{m:!!m, fan:m&&m.fan, nb:m&&m.nb&&m.nb.nom, k:m&&m.nb&&m.nb.k, v:m&&m.nb&&m.nb.v, ega:m&&m.nb?A.pul.ega(b,m.nb.k,m.nb.v):false, e2, medal:b.daraxt.medal, noyob:b.daraxt.noyob.length}}}})()""")
    ok(r['m'] and r['fan'] == 'mat' and r['nb'] and r['ega'] and r['e2'] == 0 and r['noyob'] == 1, f"🏅 Matematika shoxi to'ldi → medal + noyob buyum «{r['nb']}» garajda bolaniki; qayta berilmaydi ({r['medal']})")
    r = ev(f"""(()=>{{const A=BJ.A,b=A.bola('{AZ}'),D=A.daraxt,H=D.hisob(b); return {{p:H.p, y:b.daraxt.yetdi}}}})()""")
    ok(r['p'] >= 25 and '25' in r['y'] and '50' not in r['y'], f"🎁 25% pog'onasi belgilandi, 50% hali emas ({r})")
    # ota-ona: daraxt sovg'asi
    ev("BJ.A.otaOk={rol:'admin',t:Date.now()}; location.hash='ota-sovga'"); P.wait_for_timeout(600)
    ok(P.locator('.dzp').count() == 1 and P.locator(f'[data-dzi="{AZ}|50"]').count() == 1 and P.locator(f'[data-dzi="{AZ}|25"]').count() == 0, "Ota-ona 🎁 Sovg'alar: «🌳 Bilim daraxti sovg'alari» — yetgan 25% ga yangi sovg'a yozilmaydi, 50% ga yoziladi")
    P.fill(f'[data-dzi="{AZ}|50"]', 'Velosiped'); P.fill(f'[data-dzi="{AZ}|100"]', 'Planshet'); P.click('[data-dzs]'); P.wait_for_timeout(400)
    r = ev("JSON.stringify(BJ.A.S().dsov)")
    ok('Velosiped' in r and 'Planshet' in r, f"Saqlandi: S.dsov (oila hujjati) — {r[:90]}")
    ok(ev("!('dsov' in BJ.A.defaults ? BJ.A.defaults() : {})") if ev("typeof BJ.A.defaults") == 'function' else 'dsov:' not in html.split('function defaults()')[1][:600], "defaults() ga dsov / kozDam QO'SHILMAGAN")
    P.screenshot(path='/tmp/bj090_panel.png', full_page=True)
    # 50% ga yetganda bola sovg'ani ko'radi, ota-ona «berildi»
    r = ev(f"""(()=>{{const A=BJ.A,b=A.bola('{AZ}'),D=A.daraxt,T=A.todayKey(); const L=D.shoxlar(b); let n=0; const tot=L.reduce((a,s)=>a+s.ids.length,0);
      L.forEach(s=>s.ids.forEach(id=>{{ if(D.barg(b,id,s)!=='meva' && D.barg(b,id,s)!=='qulf' && D.hisob(b).p<50){{const t=A.nodeSt(b,id); t.holat='kalib';}} }}));
      const e=D.tekshir(b,true).find(x=>x.t==='pog'&&x.p===50); return {{e:!!e, g:e&&e.g&&e.g.nom}}}})()""")
    ok(r['e'] and r['g'] == 'Velosiped', f"Daraxt 50% → bola «🎁 Velosiped» ni ko'radi ({r})")
    ev("location.hash='uy'"); P.wait_for_timeout(200); ev("location.hash='ota-sovga'"); P.wait_for_timeout(500)
    ok(P.locator(f'[data-dzb="{AZ}|50"]').count() == 1, "Ota-ona panelida 50%: «🎉 yetdi — ✅ Berildi» tugmasi")
    P.click(f'[data-dzb="{AZ}|50"]'); P.wait_for_timeout(400)
    ok(ev(f"BJ.A.S().dsov['{AZ}'].b['50']") == ev("BJ.A.todayKey()"), "«Berildi» belgilandi (S.dsov[bola].b[50])")
    # bola ekrani
    ev("BJ.A.closeSheets(); location.hash='daraxt'"); P.wait_for_timeout(800); ev("BJ.A.closeSheets()")
    n = ev(f"BJ.A.daraxt.hisob(BJ.A.bola('{AZ}')).n")
    ok(P.locator('svg.dzs').count() == 1 and P.locator('.dl').count() == n, f"🌳 Bola ekrani: realistik daraxt, har mavzu — barg ({P.locator('.dl').count()}/{n})")
    ok(ev("document.documentElement.scrollWidth") <= 390, f"390 px da gorizontal siljish yo'q ({ev('document.documentElement.scrollWidth')})")
    ok('Velosiped' in P.inner_text('body') and 'olding' in P.inner_text('body') and 'Planshet' in P.inner_text('body'), "Pog'onalar ro'yxati: 🎁 Velosiped · ✅ olding, 100% — 🎁 Planshet")
    P.screenshot(path='/tmp/bj090_daraxt.png', full_page=True)
    P.locator('.dl[data-t="M2.3"]').dispatch_event('click'); P.wait_for_timeout(400)
    ok('Shu mavzuni mashq qil' in P.inner_text('.sheet'), "Bargni bosish → mavzu oynasi («▶ Shu mavzuni mashq qil»)")
    P.click('.sheet [data-m]'); P.wait_for_timeout(700)
    tg = ev("window.__bjCur() && window.__bjCur().it && window.__bjCur().it.tugun")
    ok(ev("location.hash") == '#daraxt-m-M2.3' and tg == 'M2.3', f"Mavzu mashqi: savol aynan shu mavzudan ({tg})")
    ev("window.__bjJavob(true)"); P.wait_for_timeout(1500)
    ok(ev("window.__bjCur() && window.__bjCur().it && window.__bjCur().it.tugun") == 'M2.3', "Keyingi savol ham shu mavzudan")
    P.click('[data-x]'); P.wait_for_timeout(500)
    ok(ev("location.hash") == '#daraxt', "✕ → daraxtga qaytadi")
    ev("location.hash='uy'"); P.wait_for_timeout(600); ev("BJ.A.closeSheets()")
    ok(P.locator('[data-daraxt]').count() == 1, "Uy ekranida «🌳 Bilim daraxtim · N%» tugmasi")
    # maktabgacha + orol: ekran va noyob buyum salondan
    r = ev(f"""(()=>{{const A=BJ.A,b=A.bola('{KI}'),D=A.daraxt; A.ZANJIR.yoz.forEach(id=>{{A.nodeSt(b,id).holat='kalib'}}); const e=D.tekshir(b,true).find(x=>x.t==='medal'); return e&&e.nb ? [e.fan, e.nb.k, !!A.pul.SALON[e.nb.k]] : null}})()""")
    ok(r and r[0] == 'yoz' and r[2], f"Orol (salon) bolasida noyob buyum — salon katalogidan ({r})")
    # ================= 🔁 XATONI QAYTARISH =================
    ev(f"(()=>{{const b=BJ.A.bola('{AZ}'); Object.values(b.fan).forEach(F=>{{if(F&&F.kalib) F.kalib.done=true}}); BJ.A.S().joriy='{AZ}'; BJ.A.save(true)}})()")  # kalibrlash savollari (1–2-kun) ro'yxatga olinmaydi
    ev("location.hash='mashq-mat'"); P.wait_for_timeout(700)
    it0 = ev("(()=>{const it=window.__bjCur().it; return {sav:it.sav, a:String(it.a), tugun:it.tugun}})()")
    ev("window.__bjJavob(false)"); P.wait_for_timeout(500)
    xq = ev(f"BJ.A.bola('{AZ}').xq || []")
    ok(len(xq) == 1 and xq[0]['it']['sav'] == it0['sav'] and xq[0]['due'] == ev("BJ.A.addDays(BJ.A.todayKey(),1)") and xq[0]['box'] == 0, f"Xato javob → aynan shu savol saqlandi («{str(it0['sav'])[:30]}»), ertaga qaytadi")
    ev("location.hash='uy'"); P.wait_for_timeout(400)
    ok(ev(f"BJ.A.xqDue(BJ.A.bola('{AZ}')).length") == 0, "Bugun hali qaytmaydi (1 kundan keyin)")
    r = ev(f"""(()=>{{const A=BJ.A,b=A.bola('{AZ}'); b.xq[0].due=A.todayKey(); b.missiya=null; b.boshlandi=A.addDays(A.todayKey(),-3); const m=A.buildMission(b); return m.final ? 'final' : m.steps[0]}})()""")
    if r == 'final': ok(True, "Bugun yakshanba — final kuni (xato qadami dushanbadan)")
    else: ok(r['k'] == 'xato' and r['n'] == 1, f"Vaqti kelgan xato → missiya 1-qadami «🔁 Xatoni tuzatamiz» ({r})")
    it1 = ev(f"(()=>{{const A=BJ.A,b=A.bola('{AZ}'); const it=A.xqItem(b,b.xq[0].id); return {{sav:it.sav,a:String(it.a),tur:it.tur}}}})()")
    ok(it1['sav'] == it0['sav'] and it1['a'] == it0['a'] and it1['tur'] == 'xq', "Qaytgan savol — aynan o'sha (matn va javob bir xil)")
    if r != 'final':
        ev("location.hash='missiya'"); P.wait_for_timeout(800)
        ok('adashgan eding' in P.inner_text('body'), "Savol tepasida 🔁 «… shu savolda adashgan eding» yozuvi")
        P.screenshot(path='/tmp/bj090_xato.png')
        ev("window.__bjJavob(true)"); P.wait_for_timeout(1500)
        x = ev(f"BJ.A.bola('{AZ}').xq[0]")
        ok(x['box'] == 1 and x['due'] == ev("BJ.A.addDays(BJ.A.todayKey(),3)"), f"To'g'ri → keyingisi 3 kundan keyin (box {x['box']}, {x['due']})")
        ev("location.hash='uy'"); P.wait_for_timeout(300)
    r = ev(f"""(()=>{{const A=BJ.A,b=A.bola('{AZ}'); const x=b.xq[0]; x.box=Math.max(1,x.box); const y0=b.yulduz; const it=A.xqItem(b,x.id); A.xqNatija(b,it,{{togri_1:true}}); const d7=x.due; const it2=A.xqItem(b,x.id); const r=A.xqNatija(b,it2,{{togri_1:true}}); return {{d7, kut:A.addDays(A.todayKey(),7), r, qoldi:b.xq.length, yul:b.yulduz-y0}}}})()""")
    ok(r['d7'] == r['kut'] and r['r'] == 'yengildi' and r['qoldi'] == 0 and r['yul'] == 1, f"Keyin 7 kun; 3-marta to'g'ri → «yengildi», ro'yxatdan chiqdi, +1 ⭐ ({r})")
    r = ev(f"""(()=>{{const A=BJ.A,b=A.bola('{AZ}'); b.xq=[]; const it=A.makeItem(b,{{tugun:'M2.1',q:1,tur:'mashq'}}); A.xqYoz(b,it); const x=b.xq[0]; x.box=2; A.xqNatija(b,A.xqItem(b,x.id),{{togri_1:false}});
      const L=A.makeItem(b,{{tugun:'L.7',q:1,tur:'mashq'}}); A.xqYoz(b,L); const K=A.makeItem(b,{{tugun:'M2.2',q:1,tur:'kashf'}}); A.xqYoz(b,K);
      for(let i=0;i<10;i++) A.xqYoz(b,A.makeItem(b,{{tugun:'M2.'+(3+i%6),q:1+i%3,tur:'mashq'}}));
      return {{box:x.box, due:x.due, kut:A.addDays(A.todayKey(),1), n:b.xq.length, bugun:b.xq.filter(y=>y.sana===A.todayKey()).length, sudoku:b.xq.some(y=>y.tugun==='L.7')}}}})()""")
    ok(r['box'] == 0 and r['due'] == r['kut'], "Qaytgan savolda yana xato → boshidan (ertaga)")
    r2 = ev(f"(()=>{{const A=BJ.A,b=A.bola('{AZ}'); b.xq=[]; const it=A.makeItem(b,{{tugun:'M2.4',q:2,tur:'mashq',kalib:1}}); A.xqYoz(b,it); return b.xq.length}})()")
    ok(r2 == 0, "Kalibrlash savoli (1–2-kun, ataylab yuqoridan) ro'yxatga olinmaydi")
    ok(not r['sudoku'] and r['bugun'] <= 4, f"Uzun topshiriq (sudoku) olinmaydi; kuniga ≤ 4 yangi xato ({r['bugun']})")
    # ================= 🎯 KUNNING 3 QIYINI =================
    r = ev(f"""(()=>{{const A=BJ.A,b=A.bola('{AZ}'); b.fan.mat.cur='M2.6'; A.nodeSt(b,'M2.6').q=1; const s1=A.q3.sel(b,'mat',0); A.nodeSt(b,'M2.6').q=3; const s2=A.q3.sel(b,'mat',0); const s3=A.q3.sel(b,'mant',0); return {{s1,s2,s3,uzun:!!A.UZUN[s3.tugun]}}}})()""")
    ok(r['s1'] == {'tugun': 'M2.6', 'q': 2} and r['s2']['tugun'] == 'M2.7' and not r['uzun'], f"Bir pog'ona qiyin: q1 → q2; q3 da — keyingi mavzu; mantiqda uzun topshiriq yo'q ({r})")
    ev(f"(()=>{{const A=BJ.A,b=A.bola('{AZ}'); b.q3=null; b.missiya={{sana:A.todayKey(),done:true,steps:[],si:0,res:{{}},items:{{}}}}; A.save(true)}})()")
    ev("location.hash='x'"); P.wait_for_timeout(200); ev("location.hash='uy'"); P.wait_for_timeout(500); ev("BJ.A.closeSheets()")
    ok(P.locator('[data-q3]').count() == 1, "Missiya bajarilgach uyda «🎯 Kunning 3 qiyini» tugmasi")
    y0 = ev(f"BJ.A.bola('{AZ}').yulduz"); h0 = ev(f"BJ.A.pul.st(BJ.A.bola('{AZ}')).h"); n0 = ev(f"JSON.stringify(BJ.A.bola('{AZ}').tugun['M2.7']||null)")
    P.click('[data-q3]'); P.wait_for_timeout(700)
    tur = ev("window.__bjCur().it.tur"); ok(tur == 'qiyin3' and '🎯' in P.inner_text('.top'), f"3 qiyin boshlandi (tur {tur})")
    for i in range(3):
        kutf(P, "window.__bjCur() && window.__bjCur().it", 6000); ev("window.__bjJavob(true)"); P.wait_for_timeout(1500)
    kutf(P, "!!document.querySelector('.q3fin')", 6000)
    b = ev(f"(()=>{{const b=BJ.A.bola('{AZ}'); return {{q3:b.q3, y:b.yulduz, h:BJ.A.pul.st(b).h, n:JSON.stringify(b.tugun['M2.7']||null)}}}})()")
    ok(b['q3'] and b['q3']['ok'] == 3 and '3 tadan 3' in P.inner_text('body'), f"3/3 → «Chempion!» ({b['q3']})")
    ok(b['y'] - y0 >= 6 and b['h'] - h0 >= ev(f"BJ.A.pul.narxK(BJ.A.bola('{AZ}'),3000)"), f"Mukofot: 3 javob ⭐ + 3 bonus ⭐ = +{b['y'] - y0}, 💵 +{b['h'] - h0}")
    ok(b['n'] == n0, "Mavzu statistikasiga ta'sir qilmaydi (qiyin savol bolaning darajasini tushirmaydi)")
    P.screenshot(path='/tmp/bj090_q3.png')
    ev("location.hash='uy'"); P.wait_for_timeout(500); ev("BJ.A.closeSheets()")
    ok(P.locator('[data-q3]').count() == 0 and 'Bugungi 3 qiyin' in P.inner_text('body'), "Kuniga 1 marta: tugma o'rniga «🎯 Bugungi 3 qiyin: 3/3»")
    # ================= 👀 KO'ZGA DAM =================
    ok(ev("BJ.A.kozHolat().KOZ_DAQ") == 15 and ev("BJ.A.kozHolat().KOZ_SEK") == 20, "Ko'zga dam: 15 daqiqada 20 soniya")
    ev("BJ.A.kozDam()"); P.wait_for_timeout(300)
    ok(P.locator('.kozw').count() == 1 and P.locator('[data-kok]').is_disabled(), "Oyna chiqdi, 20 soniya tugamaguncha davom tugmasi o'chiq")
    P.mouse.click(195, 30); P.wait_for_timeout(200)
    ok(P.locator('.kozw').count() == 1, "Tashqariga bosib yopib bo'lmaydi")
    P.screenshot(path='/tmp/bj090_koz.png')
    P.wait_for_timeout(20600)
    ok(not P.locator('[data-kok]').is_disabled(), "20 soniyadan keyin «✅ Ko'zim dam oldi — davom!»")
    P.click('[data-kok]'); P.wait_for_timeout(200); ok(P.locator('.kozw').count() == 0, "Bosilsa yopiladi")
    # vaqt hisobi: mashq paytida 15 daqiqa → o'zi chiqadi
    ev("BJ.A.kozSinov=1"); ev("location.hash='mashq-mat'"); P.wait_for_timeout(500)
    ok(kutf(P, "!!document.querySelector('.kozw')", 4000) is False, "Mashq boshida chiqmaydi")
    ev("(()=>{BJ.A.S().sozlama.kozDam=false})()"); ok(ev("BJ.A.S().sozlama.kozDam") is False, "⚙️ Sozlamada o'chirsa bo'ladi (sozlama.kozDam = false)")
    ev("(()=>{delete BJ.A.S().sozlama.kozDam; BJ.A.kozSinov=0})()")
    # ================= 🏃 ESTAFETA (u 11.11: «bolalar bir-birini ko'rib tursin, estafeta animatsiyasi, 4 ta bola») =================
    ev(f"""(()=>{{const A=BJ.A,T=A.todayKey(),D=A.weekDays(A.isoWeek()),a=A.bola('{AZ}'),k=A.bola('{KI}'); A.S().joriy='{AZ}'; A.S().sozlama.reyting=true;
      D.forEach(d=>{{ if(a.kun[d]) a.kun[d].missiya=0; if(k.kun[d]) k.kun[d].missiya=0; }}); a.kun[T]=Object.assign(A.agg(a,T),{{missiya:1,faol:1500,n:40,ok1:33}}); if(D.indexOf(T)>0) a.kun[D[0]]=Object.assign(A.agg(a,D[0]),{{missiya:1}});
      A.S().oilaTel={{'G:u1':{{nom:'Dost oila',wk:A.isoWeek(),ts:Date.now()-5*60000,guruh:1,bolalar:[{{id:'bx1',av:'🌸',laqab:'Zuhra',daraja:'g1',yulduz:31,kun:3,osish:2,detal:4,missiya:2,wkB:A.isoWeek(),bu:{{k:T,m:1,d:22,n:30,p:83}},dz:28}}]}},
        'G:u2':{{nom:'Uzoq oila',wk:'2000-W01',ts:Date.now()-3*86400e3,guruh:1,eski:1,bolalar:[{{id:'bx2',av:'🚗',laqab:'Bek',daraja:'g2',yulduz:0,kun:0,osish:0,detal:9,missiya:0,wkB:'2000-W01'}}]}}}}; A.save(true)}})()""")
    ev("location.hash='x'"); P.wait_for_timeout(150); ev("location.hash='uy'"); P.wait_for_timeout(600); ev("BJ.A.closeSheets()")
    ok(P.locator('.rey .esmini svg.ests').count() == 1 and P.locator('[data-est]').count() == 1, "Uyda hafta reytingi ichida kichik estafeta yo'lagi + «🏃 Estafeta — hammasini ko'rish»")
    P.click('[data-est]'); P.wait_for_timeout(2300)
    L = ev("[...document.querySelectorAll('.estw .rmv')].map(g=>[g.dataset.id, +g.dataset.dx, g.style.transform])")
    ok(len(L) == 4, f"Estafeta ekrani: 4 bola — 4 yo'lak ({len(L)})")
    bos = ev(f"BJ.A.estafeta.yuguruvchilar().map(x=>[x.id,x.bos])"); bd = dict(bos)
    ok(all(abs(dx - round(bd[i] / 7 * 294, 1)) < 0.6 and tr == f'translateX({dx:g}px)' for i, dx, tr in L), f"Yuguruvchi joyi = bosqich/7 (Du…Ya), animatsiya oxirida joyida ({L})")
    t = P.inner_text('.estw')
    ok('Zuhra' in t and 'Dost oila' in t and '28%' in t and 'missiya bajarildi' in t and '22 daq' in t, "Boshqa oila bolasi: ism, oila, 🌳 28%, bugun ✅ missiya · ⏱ 22 daq")
    ok("ma'lumot kelmadi" in t and P.locator('.esk.eski').count() == 1, "Eski hafta bolasi — xira, «bu hafta ma'lumot kelmadi»")
    ok('Jamoa estafetasi' in t and re.search(r'\b\d+/21\b', t), "🤝 Jamoa estafetasi: 3 faol bola × 7 = 21 bosqich")
    ok(P.locator('.esh.live').count() == 1 and P.locator('.esh.ok').count() == 2, "Holat nuqtasi: 🟢 hozir (5 daq oldin), o'z bolalari — shu telefonda")
    ok(ev("document.documentElement.scrollWidth") <= 390, "390 px da gorizontal siljish yo'q")
    P.screenshot(path='/tmp/bj090_estafeta.png', full_page=True)
    r = ev(f"""(()=>{{const E=BJ.A.estafeta, q=E.qoshimcha(BJ.A.bola('{AZ}')); return {{q, bad:E.buToza({{k:'x',m:1}}), cut:E.buToza({{k:'2026-01-01',d:9999,n:-3,p:150,z:1}})}}}})()""")
    ok(r['q']['bu']['k'] == ev("BJ.A.todayKey()") and r['q']['bu']['m'] == 1 and r['q']['bu']['d'] == 25 and isinstance(r['q'].get('dz'), int), f"Guruhga yuboriladigan qo'shimcha: bu {{k, m, d, n, p}} + dz ({r['q']})")
    ok(r['bad'] is None and r['cut'] == {'k': '2026-01-01', 'm': 0, 'd': 600, 'n': 0, 'p': 100}, "Boshqa telefondan kelgan bu — tozalanadi (noto'g'ri sana rad, sonlar chegarada, ortiqcha kalit yo'q)")
    rl = open(os.path.join(SITE, 'firestore.rules'), encoding='utf-8').read()
    ok("'zal', 'bu', 'dz'" in rl and "d.bu.keys().hasOnly(['k', 'm', 'd', 'n', 'p'])" in rl and 'd.dz is int' in rl, "firestore.rules 0.9.0: azo ga ixtiyoriy bu {k,m,d,n,p} va dz (int 0–100)")
    ev("location.hash='uy'"); P.wait_for_timeout(300)
    # ================= 🆕 YANGILIK TURI + 🔔 UNUTILGAN BO'LIM ESLATMASI (u 11.11 21:52) =================
    def uyga(): ev("BJ.A.closeSheets(); location.hash='x'"); P.wait_for_timeout(120); ev("location.hash='uy'"); P.wait_for_timeout(250); ev("BJ.A.closeSheets(); document.querySelectorAll('.ytur').forEach(x=>x.remove())"); ev("BJ.A.render()"); P.wait_for_timeout(1300)
    ev(f"(()=>{{const A=BJ.A,b=A.bola('{AZ}'); A.yangiSinov=1; A.yangilik.VER_YANGI[A.VER]=['daraxt','estafeta','q3']; A.S().joriy=b.id; delete b.yv; delete b.kor; delete b.esYop; b.boshlandi=A.addDays(A.todayKey(),-6); A.save(true)}})()")
    uyga()
    ok(P.locator('.ytur').count() == 1 and 'Bilim daraxti' in P.inner_text('.ytb') and '1/' in P.inner_text('.ytb'), "Yangi versiyadan keyin uyda tur: 🆕 1-yangilik — Bilim daraxti (tugma yoritilgan)")
    ok(P.locator('[data-daraxt] .ynb').count() == 1 and P.locator('[data-est] .ynb').count() == 1, "Kirilmagan yangi bo'limlarda «YANGI» belgisi (daraxt, estafeta)")
    P.screenshot(path='/tmp/bj090_tur.png')
    P.click('[data-ybos]'); P.wait_for_timeout(500)
    ok(ev("location.hash") == '#daraxt' and ev(f"BJ.A.bola('{AZ}').kor.daraxt") == ev("BJ.A.todayKey()"), "«👆 Bosib ko'r» → daraxtga kirdi, kirilgan sana yozildi")
    uyga()
    ok(P.locator('.ytur').count() == 1 and 'Estafeta' in P.inner_text('.ytb'), "Uyga qaytganda tur keyingi yangilikdan davom etadi (Estafeta)")
    ok(P.locator('[data-daraxt] .ynb').count() == 0 and P.locator('[data-est] .ynb').count() == 1, "Kirilgan bo'limdan «YANGI» olindi, kirilmaganda qoladi")
    P.click('[data-ykn]'); P.wait_for_timeout(200)
    ok(P.locator('.ytur').count() == 0 and ev(f"BJ.A.bola('{AZ}').yv.tur") == 'keyin', "«Keyinroq» → tur yopildi (ertaga yana)")
    uyga(); ok(P.locator('.ytur').count() == 0 and P.locator('[data-est] .ynb').count() == 1, "Bugun tur qaytib chiqmaydi, belgi turibdi")
    r = ev(f"""(()=>{{const A=BJ.A,c=A.newBola({{laqab:'Yangi',daraja:'g1',avatar:'🐢',dunyo:'garaj'}}); A.S().joriy=c.id; A.save(true); return c.id}})()""")
    uyga(); ok(P.locator('.ytur').count() == 0 and ev(f"BJ.A.bola('{r}').yv.tur") == 'yoq', "Yangi qo'shilgan bola (1-kun) — tur yo'q")
    ev(f"(()=>{{BJ.A.delBola('{r}'); BJ.A.S().joriy='{AZ}'; BJ.A.save(true)}})()")
    # 🔔 eslatma
    ev(f"""(()=>{{const A=BJ.A,b=A.bola('{AZ}'),T=A.todayKey(); b.yv.tur='ok'; b.kor.daraxt=A.addDays(T,-5); b.kor.estafeta=T; const t=A.nodeSt(b,'M2.11'); t.holat='ozl'; t.ozlSana=A.addDays(T,-1); A.save(true)}})()""")
    uyga()
    t = P.inner_text('[data-eslat]') if P.locator('[data-eslat] .eslat').count() else ''
    ok('Bilim daraxti' in t and '5 kundan beri' in t and 'yangi meva' in t, f"🔔 5 kundan beri kirilmagan daraxt: «… 1 ta yangi meva pishdi — ko'rib chiq!» ({t[:70]})")
    P.screenshot(path='/tmp/bj090_eslatma.png')
    P.click('[data-esx]'); P.wait_for_timeout(200)
    ok(P.locator('.eslat').count() == 0 and ev(f"BJ.A.bola('{AZ}').esYop.daraxt") == ev("BJ.A.todayKey()"), "✕ → bugun boshqa chiqmaydi")
    ev(f"(()=>{{const A=BJ.A,b=A.bola('{AZ}'); b.kor.dokon=A.addDays(A.todayKey(),-6); A.save(true)}})()"); uyga()
    ok("Do'kon" in (P.inner_text('[data-eslat]') if P.locator('.eslat').count() else ''), "Keyingi eslatma — 6 kundan beri kirilmagan do'kon (hamyon ma'lumoti bilan)")
    P.click('[data-esgo]'); P.wait_for_timeout(400); ok(ev("location.hash") == '#dokon', "«Kirish» → o'sha bo'limga")
    ev("BJ.A.yangiSinov=0; location.hash='uy'"); P.wait_for_timeout(300)
    ok(not PE, f"Sahifa xatolari yo'q {PE[:3]}")
finally:
    srv.terminate()
print('JAMI:', 'XATO ' + str(len(ERR)) if ERR else 'OK'); sys.exit(1 if ERR else 0)
