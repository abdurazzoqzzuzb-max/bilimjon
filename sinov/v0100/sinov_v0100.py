"""Bilimjon 0.10.0 «v10» — u 14.11: 🎛 ota-ona har bola uchun fan/bo'limlarni o'chiradi (arab tilini bilmaydigan bola — arabsiz), ⏱ missiya uzunligi,
🎁 missiya 3 bosqich + 3 tadan birini tanlash sovg'asi (pul emas), katta sovg'a, 🔥 olov sovg'asi, 🐾 jonivor parvarishi (itsiz), 🧸 xona, 👕 yopiq kiyimlar,
🚗 ulovlar (realistik mashina/uchar ot — poygada ham), 🛍 do'kon (⭐ va so'm), 🎨 rassom studiyasi (chizish, chelak, raqamli bo'yash, galereya + ota-ona olqishi).
Ishga tushirish: python3 sinov/v0100/sinov_v0100.py (skrinshotlar: /tmp/bj0100_*.png)"""
import os, sys, time, subprocess, json, re
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.abspath(os.path.join(D, '..', '..'))
PORT = 8818; URL = f'http://localhost:{PORT}/'
srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT)], cwd=SITE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
ERR = []; PE = []
def ok(c, m): print(('✅ ' if c else '❌ ') + m); (None if c else ERR.append(m))
html = open(os.path.join(SITE, 'index.html'), encoding='utf-8').read(); VJ = json.load(open(os.path.join(SITE, 'version.json'), encoding='utf-8'))
VER = re.search(r"A\.VER = '([\d.]+)'", html)[1]; SWV = re.search(r"const V = P \+ '([\d.]+)'", open(os.path.join(SITE, 'sw.js'), encoding='utf-8').read())[1]
try:
  with sync_playwright() as p:
    br = p.chromium.launch()
    ctx = br.new_context(viewport={'width': 390, 'height': 844}, service_workers='block', device_scale_factor=2)
    P = ctx.new_page(); P.on('pageerror', lambda e: PE.append(str(e))); ev = P.evaluate
    P.goto(URL + '?tez=1'); P.wait_for_timeout(400)
    P.fill('#on', 'Sinov oila'); P.fill('#p1', '1234'); P.fill('#p2', '1234'); P.click('#go'); P.wait_for_timeout(300)
    OM, AB, SB = ev("""(()=>{const A=BJ.A; const o=A.newBola({laqab:'Qiz',daraja:'g2',avatar:'🦄',dunyo:'orol'}), a=A.newBola({laqab:'Kichik',daraja:'g0',avatar:'🦁',dunyo:'garaj'}), s=A.newBola({laqab:'Sabo',daraja:'g1',avatar:'🐼',dunyo:'orol',arab:'AL.1'});
      [o,a,s].forEach(b=>{b.boshlandi=A.addDays(A.todayKey(),-20);}); A.S().sozlama.uyqu=''; A.S().joriy=o.id; A.save(true); return [o.id,a.id,s.id]})()""")
    X = lambda bid, e: ev(f"(()=>{{const A=BJ.A, V=A.sv, b=A.S().bolalar['{bid}']; return {e}}})()")
    setj = lambda bid: ev(f"(()=>{{BJ.A.S().joriy='{bid}'; BJ.A.save(true)}})()")
    W = lambda: ev("document.documentElement.scrollWidth")
    def GO(h, ms=450): ev("BJ.A.closeSheets(); location.hash='x'"); P.wait_for_timeout(80); ev(f"location.hash='{h}'"); P.wait_for_timeout(ms)
    T = ev("BJ.A.todayKey()")

    # ================= 0. VERSIYA =================
    yang = ev("BJ.A.YANGI")
    ok(VER == SWV == VJ['ver'] == '0.10.0' and VJ['verk'] == ev("BJ.A.VERK") == '10', f"Versiya: index {VER} = sw.js {SWV} = version.json {VJ['ver']} (v{VJ['verk']})")
    ok(VJ['yangi'] == yang and 2 <= len(yang) <= 4 and all(len(x) <= 90 for x in yang), f"version.json «yangi» = A.YANGI ({len(yang)} qator)")
    bd = html.split('function bolaDefaults()')[1][:1500]; dfl = html.split('function defaults()')[1][:1500]
    ok(not any(k + ':' in bd for k in ('fanOff', 'bolimOff', 'uzun', 'kjins', 'sv')) and 'fanOff' not in dfl, "Yangi maydonlar (fanOff, bolimOff, uzun, kjins, sv) bolaDefaults/defaults ga QO'SHILMAGAN")
    ok(ev("BJ.A.yangilik.VER_YANGI['0.10.0'].join(',')") == 'sovga,avto,mantiq,rassom' and ev("['sovga','avto','mantiq','rassom'].every(k=>!!BJ.A.yangilik.B[k])"), "🆕 Yangilik turi: 🎁 Sovg'alarim, 🏎️ Garaj, 🧠 Mantiq, 🎨 Rassom")
    ok(not re.search(r"j_it|kuchuk|'🐕'|'🐶'|🐷|cho'chqa", html.split('/* ================= KATALOG')[1][:9000]), "Katalogda it va cho'chqa yo'q (u: itsiz)")

    # ================= 1. UY EKRANI =================
    GO('uy', 700)
    ok(P.locator('.svh [data-svgo]').count() == 1 and P.locator('.svh [data-rassom]').count() == 1, "Uyda: 🎁 Sovg'alarim va 🎨 Rassom plitkalari")
    ok(W() <= 390, f"390 px: uy ekrani ({W()})"); P.screenshot(path='/tmp/bj0100_uy.png')

    # ================= 2. 🎛 FANLAR =================
    X(SB, "(b.fanOff={ar:1}, A.save(true), 1)")
    m = X(SB, "(()=>{const m=A.buildMission(b); return m.steps.map(s=>s.k+':'+s.fan)})()")
    ok(not any(s.endswith(':ar') for s in m) and 'duel:ar' not in m, f"Arab o'chiq bola: missiyada arab qadami yo'q ({', '.join(m)})")
    fin = X(SB, "(()=>{const m=A.buildFinal(b); return m.steps.map(s=>s.k+':'+s.fan)})()")
    ok(not any(s.endswith(':ar') for s in fin), f"Arab o'chiq: yakshanba finalida ham yo'q ({', '.join(fin)})")
    setj(SB); GO('mashq', 500)
    ok(P.locator('[data-f="ar"]').count() == 0 and P.locator('[data-ar]').count() == 0 and P.locator('[data-f="mat"]').count() == 1, "Mashq ekranida 🕌 arab yo'q, matematika bor")
    X(SB, "(b.takror=[{tugun:'AL.1',q:1,due:A.addDays(A.todayKey(),-1)},{tugun:'M1.1',q:1,due:A.addDays(A.todayKey(),-1)}], A.save(true), 1)")
    ok(X(SB, "A.dueReview(b).map(x=>x.tugun).join(',')") == 'M1.1', "Takrorlash: arab tuguni chiqarildi (faqat M1.1)")
    ok(X(SB, "A.daraxt.shoxlar(b).every(s=>s.fan!=='ar')"), "🌳 Daraxtda arab shoxi yo'q")
    X(SB, "(b.fanOff={ar:1, mat:1, mant:1}, A.save(true), 1)")
    m2 = X(SB, "(()=>{const m=A.buildMission(b); return m.steps.map(s=>s.k+':'+s.fan)})()")
    ok(not any(s.endswith(':mat') or s.endswith(':mant') or s.endswith(':ar') for s in m2) and any(s == 'blok:til' for s in m2), f"Matematika+mantiq+arab o'chiq: faqat qolgan fanlar ({', '.join(m2)})")
    ok(X(SB, "A.q3 && true") and ev("(()=>{const A=BJ.A,b=A.S().bolalar['%s']; return A.fanOn(b,'mat')===false && A.tugunOn(b,'M1.1')===false && A.tugunOn(b,'H1.1')===true})()" % SB), "fanOn / tugunOn yordamchilari to'g'ri")
    X(SB, "(b.fanOff={mat:1,til:1,en:1,mant:1,ar:1,oqish:1,dunyo:1}, A.save(true), 1)")
    m3 = X(SB, "A.buildMission(b).steps.map(s=>s.k+':'+s.fan)")
    ok(len(m3) >= 2 and m3[-1] == 'yakun:yakun', f"Hamma fan o'chsa ham missiya bo'sh emas ({', '.join(m3)})")
    X(SB, "(b.fanOff={ar:1}, A.save(true), 1)")

    # ================= 3. ⏱ MISSIYA UZUNLIGI =================
    L = X(OM, "(()=>{A.uzunSinov=1; const tz=A.TEZ; A.TEZ=false; const n=u=>{b.uzun=u; return A.buildMission(b).steps.filter(s=>s.k==='blok').reduce((a,s)=>a+s.n,0)}; const r=[n('qisqa'),n('orta'),n('toliq')]; delete b.uzun; const d=A.uzunOf(b); A.TEZ=tz; A.uzunSinov=0; return r.concat([d])})()")
    ok(L[0] < L[1] < L[2] and L[3] == 'orta', f"Missiya uzunligi: qisqa {L[0]} < o'rta {L[1]} < to'liq {L[2]} savol; 2-sinf standarti — o'rta")
    ok(X(AB, "A.uzunOf(b)") == 'toliq', "Maktabgacha standarti — to'liq (missiyasi o'zi qisqa)")

    # ================= 4. 🧩 BO'LIMLAR =================
    X(OM, "(b.bolimOff={albom:1, zal:1, rassom:1}, A.save(true), 1)"); setj(OM); GO('uy', 600)
    ok(P.locator('[data-albom]').count() == 0 and P.locator('[data-zal]').count() == 0 and P.locator('[data-rassom]').count() == 0 and P.locator('[data-hikoya]').count() == 1, "O'chiq bo'limlar uyda ko'rinmaydi (albom, zal, rassom), hikoya bor")
    GO('albom', 500); ok(ev("location.hash") == '#uy' and P.locator('[data-svgo]').count() == 1, "O'chiq bo'limga havola bilan kirilsa — uyga qaytaradi")
    GO('rassom', 400); ok(ev("location.hash") == '#uy', "O'chiq 🎨 rassom — uyga qaytaradi")
    X(OM, "(b.bolimOff={}, A.save(true), 1)")

    # ================= 5. 👨‍👩‍👧 OTA-ONA FORMASI =================
    ev("BJ.A.otaOk={rol:'admin',t:Date.now()}"); GO('ota-tahrir-' + SB, 700)
    ok(P.locator('[data-fan]').count() == 8 and P.locator('[data-bolim]').count() == 13 and P.locator('#fun').count() == 1 and P.locator('#fkj').count() == 1, "Formada: 8 fan, 13 bo'lim, missiya uzunligi, kiyim to'plami")
    ok(not P.locator('[data-fan="ar"]').is_checked() and ev("document.getElementById('farab').hidden"), "Arab o'chiq — arab daraja tanlovlari yashirin")
    P.locator('[data-fan="ar"]').check(); ok(not ev("document.getElementById('farab').hidden"), "Arab yoqilsa — tanlovlar ko'rinadi"); P.locator('[data-fan="ar"]').uncheck()
    for f in ('mat', 'til', 'en', 'mant'): P.locator(f'[data-fan="{f}"]').uncheck()
    P.click('[data-save]'); P.wait_for_timeout(300)
    ok(ev("location.hash").startswith('#ota-tahrir') and X(SB, "!b.fanOff.mat"), "Hamma asosiy fan o'chirilsa — saqlanmaydi (kamida bitta qolsin)")
    P.locator('[data-fan="mat"]').check(); P.locator('[data-fan="til"]').check(); P.locator('[data-bolim="bozor"]').uncheck(); P.select_option('#fun', 'qisqa'); P.select_option('#fkj', 'q')
    P.screenshot(path='/tmp/bj0100_forma.png', full_page=True); P.click('[data-save]'); P.wait_for_timeout(300)
    sv = X(SB, "({f:b.fanOff, o:b.bolimOff, u:b.uzun, k:b.kjins})")
    ok(sv['f'] == {'en': 1, 'mant': 1, 'ar': 1} and sv['o'] == {'bozor': 1} and sv['u'] == 'qisqa' and sv['k'] == 'q', f"Saqlandi: fanOff {sv['f']}, bolimOff {sv['o']}, uzun {sv['u']}, kiyim {sv['k']}")
    X(SB, "(b.fanOff={ar:1}, b.bolimOff={}, A.save(true), 1)")

    # ================= 6. 🎁 MISSIYA BOSQICHLARI =================
    ev("BJ.A.svSinov=1"); setj(OM)
    X(OM, "(()=>{b.missiya=A.buildMission(b); const m=b.missiya, tot=m.steps.reduce((s,x)=>s+(x.n||1),0); let c=0, i=0; while(i<m.steps.length && c*3<tot){c+=m.steps[i].n||1; i++;} m.si=i; for(let j=0;j<i;j++) m.res[j]=Array(m.steps[j].n||1).fill({ok:1,ms:1}); A.save(true); return 1})()")
    GO('missiya', 900)
    ok(P.locator('.svk').count() == 3 and 'bosqich tugadi' in P.locator('.sheet').inner_text(), "1/3 da: «1-bosqich tugadi» — 3 ta sovg'a kartasi")
    kid = P.locator('.svk').first.get_attribute('data-svk'); P.screenshot(path='/tmp/bj0100_bosqich.png')
    P.locator('.svk').first.click(); P.wait_for_timeout(900)
    ok(X(OM, f"b.sv.ol[A.todayKey()+':1']==='{kid}' && b.missiya.bq===1") and 'seniki' in P.locator('.sheet').inner_text(), f"Tanlangan sovg'a ({kid}) berildi, bosqich belgilandi")
    P.locator('[data-svt="0"]').click(); P.wait_for_timeout(500)
    ok(P.locator('.svk').count() == 0 and P.locator('.road .svrg.ol').count() == 1, "«Davom etamiz» → missiya davom etadi; yo'lda 1-sovg'a ✓")
    X(OM, "(()=>{const m=b.missiya, tot=m.steps.reduce((s,x)=>s+(x.n||1),0); let c=0, i=0; while(i<m.steps.length && c*3<2*tot){c+=m.steps[i].n||1; i++;} if(m.steps[i] && m.steps[i].k==='yakun') i--; for(let j=0;j<i;j++) m.res[j]=Array(m.steps[j].n||1).fill({ok:1,ms:1}); m.si=i; m.cur=null; A.save(true); return 1})()")
    GO('missiya', 900)
    ok(P.locator('.svk').count() == 3 and '2-bosqich' in P.locator('.sheet').inner_text(), "2/3 da: «2-bosqich tugadi» — yana 3 tadan biri")
    P.locator('[data-svkeyin]').click(); P.wait_for_timeout(400); GO('missiya', 900)
    ok(P.locator('.svk').count() == 3, "«Keyinroq» — sovg'a yo'qolmaydi, missiyaga qaytganda yana chiqadi")
    P.locator('.svk').nth(1).click(); P.wait_for_timeout(800)
    ok(X(OM, "!!b.sv.ol[A.todayKey()+':2'] && b.missiya.bq===2 && b.sv.ovq>=0"), "2-bosqich sovg'asi olindi")

    # ================= 7. 🎁 KATTA SOVG'A + 🔥 OLOV =================
    X(OM, "(()=>{[1,2,3].forEach(i=>{A.agg(b,A.addDays(A.todayKey(),-i)).missiya=1}); const m=b.missiya; m.done=true; A.agg(b).missiya=1; A.save(true); return 1})()")
    GO('natija', 1600)
    ok(P.locator('.svk').count() == 3 and "KATTA" in P.locator('.sheet').inner_text(), "Missiya tugadi → KATTA sovg'a oynasi")
    d2 = X(OM, "b.sv.tq[A.todayKey()+':k'].map(id=>(V.KAT[id]||{d:9}).d)")
    ok(all(x >= 2 for x in d2 if x != 9), f"Katta sovg'a — «yaxshi» yoki «noyob» buyumlar ({d2})")
    P.locator('.svk').first.click(); P.wait_for_timeout(900); P.screenshot(path='/tmp/bj0100_katta.png')
    ok('Yana bir' in P.locator('.sheet').inner_text(), "Olov 4 kun (≥3) — «🎁 Yana bir sovg'a!» tugmasi")
    P.locator('[data-svt="0"]').click(); P.wait_for_timeout(500)
    ok(P.locator('.svk').count() == 3 and 'ketma-ket' in P.locator('.sheet').inner_text(), "🔥 3 kun ketma-ket — noyob sovg'a oynasi")
    P.locator('.svk').last.click(); P.wait_for_timeout(800)
    ok(X(OM, "!!b.sv.ol['olov:3'] && !!b.sv.ol[A.todayKey()+':k'] && V.kutilgan(b).length===0"), "Katta va olov sovg'alari olindi, kutilganlar qolmadi")

    # ================= 8. 🛍 DO'KON (⭐ va so'm) =================
    X(OM, "(b.yulduz=200, b.sv.sarf=0, A.save(true), 1)")
    GO('sovga-dokon', 500); P.locator('[data-svdt="oyin"]').click(); P.wait_for_timeout(300)
    bid0 = P.locator('[data-svsot][data-p="yul"]').first.get_attribute('data-svsot'); n0 = X(OM, f"V.narx(V.KAT['{bid0}'])")
    P.locator('[data-svsot][data-p="yul"]').first.click(); P.wait_for_timeout(300); P.click('.sheet [data-ok]'); P.wait_for_timeout(500)
    ok(X(OM, f"V.ega(b,'{bid0}') && b.sv.sarf==={n0} && V.yul(b)===200-{n0} && b.yulduz===200"), f"⭐ bilan sotib olindi ({bid0}, {n0}⭐): sarf yoziladi, b.yulduz (reyting) o'zgarmaydi")
    GO('uy', 500); ok(P.locator('[data-yul]').first.inner_text().strip() == f"⭐ {200 - n0}", "Uyda ⭐ — sarflanadigan yulduz")
    X(OM, "(b.yulduz=b.sv.sarf+5, A.save(true), 1)"); GO('sovga-dokon', 500)
    P.locator('[data-svdt="jon"]').click(); P.wait_for_timeout(300); P.locator('[data-svsot][data-p="yul"]').first.click(); P.wait_for_timeout(300)
    ok(P.locator('.sheet').count() == 0, "⭐ yetmasa — sotib olinmaydi (eslatma)")
    setj(AB); X(AB, "(A.pul.st(b).h=50000, A.save(true), 1)"); GO('sovga-dokon', 500); P.locator('[data-svdt="oyin"]').click(); P.wait_for_timeout(300)
    uid = P.locator('[data-svsot][data-p="som"]').first.get_attribute('data-svsot'); sn = X(AB, f"A.pul.narxK(b, ({{1:3000,2:7000,3:15000}})[V.KAT['{uid}'].d])")
    P.locator('[data-svsot][data-p="som"]').first.click(); P.wait_for_timeout(300); P.click('.sheet [data-ok]'); P.wait_for_timeout(700)
    ok(X(AB, f"V.ega(b,'{uid}') && A.pul.st(b).h===50000-{sn}"), f"💵 so'm bilan sotib olindi ({uid}, {sn} so'm)")
    ok(W() <= 390, f"390 px: do'kon ({W()})"); P.screenshot(path='/tmp/bj0100_dokon.png')

    # ================= 9. 🏎️ AVTOSALON — realistik mashina, qism yig'ish, tuning =================
    ok(X(AB, "A.bezak(b).model==='sedan'") and 'carm"' in X(AB, "BJ.art.car(A.bezak(b),{w:200})"), "Garaj bolasining o'z mashinasi — realistik sport sedan (sahna, yo'l, poyga — A.bezak)")
    ok(X(OM, "V.mos(b,V.KAT['u_malika'])===true && !V.KAT['u_kupe']") and 'class="pegasus"' in X(OM, "BJ.art.pegasus({}, {w:200})"), "Orolda — realistik uchar otlar; garaj presetlari olib tashlangan (mashina — qism yig'ib)")
    GO('avto', 600)
    ok(P.locator('.avcar svg.carm').count() == 1 and P.locator('.avc').count() == 5 and P.locator('.avt').count() == 10, "🏎️ Garaj: shou-rum, 5 mashina, 10 tuning turi")
    ok(X(AB, "A.avto.st(b).maq") == 'kupe' and P.locator('.avqs span').count() == 6, "Maqsad: GT kupe — 6 qism uyasi")
    X(AB, "(A.avto.qism(b,5,'sinov'), 1)"); ok(X(AB, "A.avto.st(b).q===5 && !A.avto.st(b).ega.kupe"), "5 qism — hali ochilmadi")
    o1 = X(AB, "A.avto.qism(b,2,'sinov')"); ok(o1 == 'kupe' and X(AB, "!!A.avto.st(b).ega.kupe && A.avto.st(b).q===1 && A.avto.st(b).maq==='jip' && A.avto.st(b).yangi==='kupe'"), "6-qismda GT kupe ochildi, ortgan qism keyingi maqsadga (jip) o'tdi")
    GO('uy', 2000); ok(P.locator('.sheet .avnew').count() == 1, "Uyga kirganda: «🎉 Yangi mashina ochildi!» oynasi")
    P.click('.sheet [data-ok]'); P.wait_for_timeout(600); ok(X(AB, "A.avto.st(b).a==='kupe' && A.bezak(b).model==='kupe' && !A.avto.st(b).yangi"), "«Shu bilan haydayman» — faol mashina GT kupe")
    X(AB, "(b.yulduz=(b.sv&&b.sv.sarf||0)+100, A.save(true), 1)"); GO('avto', 500); P.click('[data-avk="disk"]'); P.wait_for_timeout(200); P.click('[data-avv="2"]'); P.wait_for_timeout(200)
    ok(P.locator('.avcar svg.carm').count() == 1 and 'Qora sport' in P.locator('.avo.sel').inner_text(), "Tuningni bosganda katta mashinada oldindan ko'rinadi")
    s1 = X(AB, "b.sv.sarf"); P.click('[data-avbuy="yul"]'); P.wait_for_timeout(500)
    ok(X(AB, f"A.avto.st(b).t.kupe.disk===2 && b.sv.sarf==={s1}+20 && A.bezak(b).disk===2"), "⭐ 20 ga «Qora sport» disk sotib olindi va o'rnatildi")
    P.click('[data-avk="neon"]'); P.wait_for_timeout(200); P.click('[data-avv="1"]'); P.wait_for_timeout(200); h0 = X(AB, "A.pul.st(b).h"); P.click('[data-avbuy="som"]'); P.wait_for_timeout(300); P.click('.sheet [data-ok]'); P.wait_for_timeout(600)
    ok(X(AB, f"A.avto.st(b).t.kupe.neon===1 && A.pul.st(b).h==={h0}-A.pul.narxK(b,4000)"), "💵 so'm bilan «Ko'k neon» olindi")
    ok(X(AB, "(b.detal=[{k:'spoyler',t:2}], A.avto.tEga(b,'kupe','spoyler',2) && !A.avto.tEga(b,'kupe','spoyler',3))"), "Eski missiya detallari — bepul tuning (spoyler 2-daraja)")
    ok(W() <= 390, f"390 px: garaj ({W()})"); P.screenshot(path='/tmp/bj0100_garaj.png', full_page=True)
    tv2 = X(AB, "(()=>{delete b.sv.tq['t-g']; return V.tanlov(b,'t-g',1).map(k=>k.id)})()")
    ok('x_qism' in tv2 and 'x_tun' in tv2, f"Garaj bolasining sovg'a tanlovida: 🔩 qism ×2 va ⭐ tuning ({tv2})")
    q0 = X(AB, "A.avto.st(b).q"); X(AB, "V.olish(b,'t-g','x_qism','sinov')"); ok(X(AB, f"A.avto.st(b).q==={q0}+2"), "«🔩 Mashina qismi ×2» tanlansa — maqsadga 2 qism")
    ok(X(AB, "(()=>{const k=A.todayKey(); delete A.avto.st(b).mk[k]; const q=A.avto.st(b).q; A.avto.missiyaQism(b); A.avto.missiyaQism(b); return A.avto.st(b).q-q})()") == 2, "Missiya oxiri — 🔩 2 qism (kuniga bir marta)")

    # ================= 10. 👕 KIYIMLAR (qizlar — yopiq) =================
    ok(X(SB, "V.kj(b)==='q' && !V.mos(b,V.KAT['k_futbolka']) && V.mos(b,V.KAT['k_romol']) && V.mos(b,V.KAT['k_chopon'])"), "Qizlar to'plami: ro'mol, chopon bor; o'g'il bolalar kiyimi yo'q")
    setj(SB); X(SB, "(V.ber(b,'k_romol'), V.ber(b,'k_koylak'), A.save(true), 1)"); GO('sovga-kiy', 500)
    ok(X(SB, "b.sv.kiy.bosh==='k_romol' && b.sv.kiy.ust==='k_koylak'") and '🧕' in P.locator('.svq').inner_text(), "Kiyim olinganda bo'sh joyga o'zi kiyiladi — qahramonda 🧕")
    P.locator('[data-svkiy="k_romol"]').click(); P.wait_for_timeout(300); ok(X(SB, "!b.sv.kiy.bosh"), "Kiyimni bossa — yechiladi")
    P.screenshot(path='/tmp/bj0100_kiy.png')

    # ================= 11. 🐾 JONIVOR =================
    X(SB, "(V.ber(b,'j_mushuk'), b.sv.ovq=1, b.yulduz=b.sv.sarf+10, A.save(true), 1)"); GO('sovga-jon', 500)
    ok(P.locator('[data-svpet]').count() == 1 and P.locator('.svbar').count() == 3, "Jonivor sahnasi: 🐈 + 3 ko'rsatkich (to'qlik, quvonch, tozalik)")
    X(SB, "(b.sv.jon.j_mushuk.toq=20, b.sv.jon.j_mushuk.ts=Date.now(), A.save(true), 1)"); GO('uy', 500)
    ok('och' in P.locator('[data-svgo]').inner_text(), "Uyda: «🍎 Jonivoring och qoldi»")
    GO('sovga-jon', 500); P.locator('[data-svam="ovqat"]').click(); P.wait_for_timeout(1300)
    ok(X(SB, "V.jh(b.sv.jon.j_mushuk).toq>=59 && b.sv.ovq===0"), "🍎 Ovqat: to'qlik +40, zaxira kamaydi")
    s0 = X(SB, "b.sv.sarf"); P.locator('[data-svam="ovqat"]').click(); P.wait_for_timeout(1300)
    ok(X(SB, f"b.sv.sarf==={s0}+3"), "Ovqat zaxirasi tugasa — 3⭐ ga beriladi")
    P.locator('[data-svam="suv"]').click(); P.wait_for_timeout(1200); r = X(SB, "V.amal(b,'j_mushuk','suv')")
    ok(r and r.get('xato'), "💧 Suv — 3 soatda bir marta (qayta bosilsa: «chanqamagan»)")
    for i in range(5): P.locator('[data-svpet]').click(force=True); P.wait_for_timeout(120)
    P.wait_for_timeout(1000); ok(X(SB, "!!b.sv.jon.j_mushuk.oyTs"), "🧶 Jonivorni 5 marta tez bosish — birga o'ynash")
    ok(X(SB, "(b.sv.jon.j_mushuk.ts=Date.now()-5*864e5, V.kayfiyat(b.sv.jon.j_mushuk).t.indexOf(\"sog'indim\")>=0 && V.jh(b.sv.jon.j_mushuk).toq===0)"), "5 kun kelmasa — jonivor o'lmaydi, «Seni sog'indim» (aybdorlik yo'q)")
    ok(X(SB, "V.osish(0)[1]==='Chaqaloq' && V.osish(250)[1]==='Katta'"), "O'sish bosqichlari: chaqaloq → o'smir → katta → yulduz")
    ok(W() <= 390, f"390 px: jonivor ({W()})"); P.screenshot(path='/tmp/bj0100_jon.png')

    # ================= 12. 🎨 RASSOM =================
    setj(OM); GO('rassom', 600)
    ok(P.locator('#rcv').count() == 1 and P.locator('[data-rc]').count() == 7, "Chizish: kanvas va 7 ta bepul rang")
    bx = P.locator('#rcv').bounding_box(); P.mouse.move(bx['x'] + 40, bx['y'] + 40); P.mouse.down(); P.mouse.move(bx['x'] + 200, bx['y'] + 160, steps=12); P.mouse.up(); P.wait_for_timeout(200)
    px = ev("(()=>{const c=document.getElementById('rcv'), x=c.getContext('2d'), k=c.width/c.getBoundingClientRect().width; const d=x.getImageData(Math.round(120*k),Math.round(100*k),1,1).data; return [d[0],d[1],d[2]]})()")
    ok(px[0] > 180 and px[1] < 120, f"Qalam chizdi (qizil piksel {px})")
    P.click('[data-ra="chelak"]'); P.wait_for_timeout(200); P.click('[data-rc="#1E88E5"]'); P.wait_for_timeout(200); P.click('[data-ra="chelak"]'); P.wait_for_timeout(200)
    bx = P.locator('#rcv').bounding_box(); P.mouse.click(bx['x'] + bx['width'] - 20, bx['y'] + bx['height'] - 20); P.wait_for_timeout(300)
    px2 = ev("(()=>{const c=document.getElementById('rcv'), x=c.getContext('2d'); const d=x.getImageData(c.width-8,c.height-8,1,1).data; return [d[0],d[1],d[2]]})()")
    ok(px2[2] > 200 and px2[0] < 80, f"🪣 Chelak — oq fonni ko'kka bo'yadi ({px2})")
    P.click('[data-rsave]'); P.wait_for_timeout(800)
    ok(ev("(async()=>{return (await BJ.A.sv.rasmlar('%s')).length})()" % OM) == 1 and X(OM, "b.sv.rasN===1"), "💾 Galereyaga saqlandi (IndexedDB, faqat shu qurilmada)")
    ok('"src"' not in json.dumps(X(OM, "b.sv")) and 'data:image' not in json.dumps(X(OM, "b")), "Rasm bola hujjatiga (bulutga) yozilmaydi")
    P.screenshot(path='/tmp/bj0100_chiz.png')
    P.click('[data-rt="raqam"]'); P.wait_for_timeout(400)
    nreg = P.locator('[data-rr]').count(); ok(nreg >= 10 and P.locator('.rrsvg text').count() == nreg, f"🔢 Raqamli bo'yash: {nreg} bo'lak, har birida misol")
    ex = ev("BJ.A.sv.RR[0].R.map(r=>r[1])"); lbl = [P.locator(f'.rrsvg text[data-rt="{i}"]').text_content() for i in range(nreg)]
    def hisob(t):
        t = t.replace('−', '-').replace('×', '*').replace(':', '//'); return eval(t)
    ok(all(hisob(lbl[i]) == ex[i] for i in range(nreg)), f"Har misol javobi — rang raqami ({lbl[:4]} → {ex[:4]})")
    wrong = 1 if ex[0] != 1 else 2; P.click(f'[data-rrc="{wrong}"]'); P.locator('[data-rr="0"]').dispatch_event('click'); P.wait_for_timeout(300)
    ok(P.locator('[data-rr="0"]').get_attribute('fill') == '#FFFFFF', "Noto'g'ri rang — bo'yalmaydi")
    y0 = X(OM, "b.yulduz")
    for i in range(nreg):
        P.click(f'[data-rrc="{ex[i]}"]'); P.locator(f'[data-rr="{i}"]').dispatch_event('click'); P.wait_for_timeout(60)
    P.wait_for_timeout(1500)
    ok(P.locator('.rrsvg text').count() == 0 and X(OM, "b.yulduz") == y0 + 3 and 'tayyor' in P.locator('.sheet').inner_text(), "Hamma bo'lak bo'yaldi → «Rasm tayyor!» +3⭐")
    ok(ev("(async()=>{return (await BJ.A.sv.rasmlar('%s')).length})()" % OM) == 2, "Bo'yalgan rasm ham galereyaga tushdi")
    P.screenshot(path='/tmp/bj0100_raqam.png'); P.click('.sheet [data-gal]'); P.wait_for_timeout(700)
    ok(P.locator('.rag').count() == 2, "🖼 Galereyada 2 rasm"); P.locator('.rag').first.click(); P.wait_for_timeout(300)
    P.click('.sheet [data-olq]'); P.wait_for_timeout(200); P.fill('#svpin', '1234'); P.wait_for_timeout(300); y1 = X(OM, "b.yulduz")
    P.click('.sheet [data-o="3"]'); P.wait_for_timeout(700)
    ok(P.locator('.ragol').count() == 1 and X(OM, "b.yulduz") == y1 + 2, "👨‍👩‍👧 Ota-ona olqishi (PIN bilan) 🏆 → rasmda belgi, bolaga +2⭐")
    ok(W() <= 390, f"390 px: rassom ({W()})")

    # ================= 12b. 🧠 MANTIQ O'YINLARI =================
    setj(AB); GO('mantiq', 500)
    ok(P.locator('.mtk').count() == 7, "🧠 Mantiq: 7 xil o'yin (naqsh, ortiqcha, chiroqlar, robot, minora, tarozi, sudoku)")
    ok(X(AB, "A.mantiq.mt(b,'naqsh').lv") == 1 and X(OM, "A.mantiq.mt(b,'naqsh').lv") == 5, "Boshlang'ich daraja yoshga qarab: maktabgacha 1, 2-sinf 5")
    for g in ['naqsh', 'ortiqcha', 'chiroq', 'robot', 'minora', 'tarozi', 'sudoku']:
        GO('mantiq-' + g, 450); ok(P.locator('#mtg').inner_html().strip() != '' and W() <= 390 and P.locator('[data-say]').count() == 1, f"{g}: o'yin chizildi, 🔊 tushuntirish tugmasi, 390 px")
    GO('mantiq-naqsh', 450); a = ev("String(BJ.A.mantiq._c.ans)")
    opts = [P.locator(f'[data-mo="{i}"]').inner_text() for i in range(P.locator('[data-mo]').count())]
    P.locator(f'[data-mo="{opts.index(a)}"]').click(); P.wait_for_timeout(1200)
    ok(X(AB, "A.mantiq.mt(b,'naqsh').lv") == 2 and P.locator('.sheet').count() == 1 and '2-daraja' in P.locator('.sheet').inner_text(), "Naqsh yutildi → 2-daraja ochildi (keyingisi qiyinroq)")
    P.click('.sheet [data-ok]'); P.wait_for_timeout(500); a2 = ev("String(BJ.A.mantiq._c.ans)"); o2 = [P.locator(f'[data-mo="{i}"]').inner_text() for i in range(P.locator('[data-mo]').count())]
    ok(len(o2) >= 3 and ev("BJ.A.mantiq._c.lv") == 2, "Keyingi daraja yangi naqsh bilan boshlandi")
    lvx = X(AB, "(()=>{const x=A.mantiq.mt(b,'tarozi'); x.lv=4; x.x=0; A.mantiq.natijaMt(b,'tarozi',false); A.mantiq.natijaMt(b,'tarozi',false); return x.lv})()")
    ok(lvx == 3, "2 marta ketma-ket yutqazsa — bir daraja osonlashadi (bola zerikmasin, qiynalmasin)")
    GO('mantiq-minora', 450)
    def hp(i): P.locator(f'[data-p="{i}"]').click(); P.wait_for_timeout(120)
    hp(0); hp(1); hp(0); hp(1); P.wait_for_timeout(300)
    ok(X(AB, "true") and P.locator('.mthp').nth(1).locator('.mthd').count() == 1, "Minora: katta halqani kichigi ustiga qo'yib bo'lmaydi")
    hp(0); hp(2); hp(1); hp(2); P.wait_for_timeout(1000)
    ok(P.locator('.sheet').count() == 1 and X(AB, "A.mantiq.mt(b,'minora').lv") == 2, "Minora 2 halqa — yechildi, 2-daraja (3 halqa)")
    GO('mantiq-chiroq', 450); on0 = P.locator('.mtb.on').count(); P.locator('.mtb').first.click(); P.wait_for_timeout(200)
    ok(P.locator('.mtb.on').count() != on0 or P.locator('.sheet').count() == 1, "Chiroqlar: bosilganda o'zi va qo'shnilari almashadi")
    GO('mantiq-sudoku', 450); blank = P.locator('.mtsc.bo').first; blank.click(); P.wait_for_timeout(150)
    ok(P.locator('[data-v]:not([disabled])').count() >= 3, "Sudoku: bo'sh katak tanlanganda rasmlar tanlovi ochiladi")
    ok(any(t.startswith('mt_') for t in ev("BJ.A.oyin.turlar(BJ.A.bola())")), "Dam olish oynasida ham mantiq o'yinlari (bir xil o'yin takrorlanmasin)")
    mt_txt = ev("BJ.A.mantiq.matnlar()"); ok(len(mt_txt) >= 20 and not any(ch.isdigit() for t in mt_txt for ch in t), f"🔊 Ovozli tushuntirishlar: {len(mt_txt)} ta ibora (raqamsiz — neyron ovozga tayyor)")
    X(AB, "(b.bolimOff={mantiq:1}, A.save(true), 1)"); GO('uy', 500); ok(P.locator('[data-mtgo]').count() == 0 and not any(t.startswith('mt_') for t in ev("BJ.A.oyin.turlar(BJ.A.bola())")), "Ota-ona 🧠 Mantiqni o'chirsa — uyda ham, dam olishda ham yo'q"); X(AB, "(b.bolimOff={}, A.save(true), 1)")

    # ================= 13. 🎁 SOVG'A TANLOVI — xilma-xillik, 3A =================
    tv = X(AB, "(()=>{const L=V.tanlov(b,'t-x',1); return L.map(k=>k.t)})()")
    ok(len(tv) == 3 and len(set(tv)) >= 2, f"3 tadan biri: turli turlar ({tv}) — tasodifiy quti emas, bola ko'rib tanlaydi")
    ok(X(AB, "JSON.stringify(V.tanlov(b,'t-x',1).map(k=>k.id))===JSON.stringify(b.sv.tq['t-x'])"), "Qayta ochilganda o'sha 3 ta (almashtirib yuborilmaydi)")

    # ================= 14. Xatolar =================
    ok(not PE, "Sahifa xatolari yo'q" + (f": {PE[:3]}" if PE else ''))
    br.close()
finally:
  srv.terminate()
print(f"\n{len(ERR)} ta xato" if ERR else "\nHAMMASI OK"); sys.exit(1 if ERR else 0)
