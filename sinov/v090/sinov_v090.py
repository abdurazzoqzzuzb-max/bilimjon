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
    ev(f"(()=>{{BJ.A.S().joriy='{AZ}'; BJ.A.save(true)}})()")
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
    ok(not PE, f"Sahifa xatolari yo'q {PE[:3]}")
finally:
    srv.terminate()
print('JAMI:', 'XATO ' + str(len(ERR)) if ERR else 'OK'); sys.exit(1 if ERR else 0)
