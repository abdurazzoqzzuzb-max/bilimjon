"""Bilimjon 0.6.0 — 5-bosqich: 💰 so'm iqtisodi (hamyon, mukofotlar byudjetga mos, kuniga 30 javob, 5 kun bonusi, 🐷 kassa,
to'lov kupyura bilan / qaytim savoli, 🎁 haqiqiy sovg'a buyurtmasi → Berildi / Bekor, 🏎️ tuning va 🦄 salon, konstruktor qismi, 390 px).
Ishga tushirish: python3 sinov/v060/sinov_bosqich5.py  (skrinshotlar: /tmp/bj060_5_*.png)"""
import os, sys, time, subprocess, tempfile, re
from playwright.sync_api import sync_playwright
from PIL import Image

D = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.abspath(os.path.join(D, '..', '..'))
PORT = 8775; URL = f'http://localhost:{PORT}/'
srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT)], cwd=SITE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
RASM = os.path.join(tempfile.mkdtemp(), 'lego.png'); Image.new('RGB', (1600, 1200), (40, 120, 230)).save(RASM)
ERR = []
def ok(c, m):
    print(('✅ ' if c else '❌ ') + m)
    if not c: ERR.append(m)
NV = [0]
def NAV(pg, h, ms=400):
    NV[0] += 1; pg.goto(URL + f'?tez=1&r={NV[0]}#' + h); pg.evaluate('BJ.A.render()'); pg.wait_for_timeout(ms)
def NAVO(pg, h, ms=400):
    NV[0] += 1; pg.goto(URL + f'?tez=1&r={NV[0]}#' + h); pg.evaluate("BJ.A.otaOk={rol:'admin',t:Date.now()}; BJ.A.render()"); pg.wait_for_timeout(ms)
SHOT = lambda pg, n: pg.screenshot(path=f'/tmp/bj060_5_{n}.png', full_page=True)
SRC = open(os.path.join(SITE, 'index.html'), encoding='utf-8').read()

with sync_playwright() as p:
    br = p.chromium.launch(); ctx = br.new_context(viewport={'width': 390, 'height': 844}, service_workers='block'); pg = ctx.new_page()
    pg.on('pageerror', lambda e: ERR.append(f'pageerror: {e}')); ev = pg.evaluate
    pg.goto(URL + '?tez=1'); pg.wait_for_timeout(400)
    pg.fill('#on', 'Sinov'); pg.fill('#p1', '1234'); pg.fill('#p2', '1234'); pg.click('#go'); pg.wait_for_timeout(300)
    K, Q, R = ev("""(()=>{const A=BJ.A; const k=A.newBola({laqab:'Kichik',daraja:'g0',avatar:'🐯',dunyo:'garaj'}); const q=A.newBola({laqab:'Katta',daraja:'g2',avatar:'🦄',dunyo:'orol'});
      const r=A.newBola({laqab:'Orta',daraja:'g1',avatar:'🐼',dunyo:'garaj'}); A.S().sozlama.uyqu=''; A.S().joriy=k.id; A.save(true); return [k.id,q.id,r.id]})()""")
    setj = lambda bid: ev(f"(()=>{{const s=BJ.A.S(); s.joriy='{bid}'; BJ.A.save(true)}})()")
    H = lambda bid: ev(f"BJ.A.pul.st(BJ.A.S().bolalar['{bid}']).h")
    def berP(bid, s): ev(f"(()=>{{const b=BJ.A.S().bolalar['{bid}'], p=BJ.A.pul.st(b); p.h={s}; BJ.A.save(true)}})()")

    # ---- standart sozlama va bola maydoni
    r = ev(f"""(()=>{{const s=BJ.A.S(); return [s.sozlama.pul, s.sozlama.byudjet, s.sozlama.kassa, Array.isArray(s.dokon), s.bolalar['{K}'].pul]}})()""")
    ok(r == [True, 50000, True, True, None], f"Standart: so'm yoqilgan, byudjet 50 000, kassa yoqilgan, S.dokon=[], bola.pul=null {r}")
    ok("'dokon'" not in re.search(r"const MAHALLIY = \[[^\]]*\]", SRC).group(0), "S.dokon bulutga (umumiy) chiqadi — MAHALLIY ro'yxatida yo'q")
    # ---- mukofotlar byudjetga moslashadi
    r = ev("""(()=>{const A=BJ.A, s=A.S(), out=[]; for (const v of [20000,50000,100000]) { s.sozlama.byudjet=v; const m=A.pul.MUK(null); out.push([m.javob,m.missiya,m.vazifa,m.bonus]); } s.sozlama.byudjet=50000; return out})()""")
    ok(r == [[100, 800, 400, 4000], [200, 2000, 1000, 10000], [400, 4000, 2000, 20000]], f"Mukofot byudjetga mos: 20k / 50k / 100k {r}")
    r = ev(f"""(()=>{{const A=BJ.A, b=A.S().bolalar['{R}']; A.pul.st(b).byudjet=100000; const j=A.pul.MUK(b).javob, n=A.pul.narxK(b,5000); A.pul.st(b).byudjet=null; return [j,n]}})()""")
    ok(r == [400, 10000], f"Bolaning o'z byudjeti (100 000) → javob +400, tuning narxi ×2 {r}")
    # ---- to'g'ri javob (onAnswer orqali) +200; birinchi urinishda xato bo'lsa — yo'q
    NAV(pg, 'sinov-L.1-1', 400)
    a = ev("window.__bjCur().it.a"); pg.locator(f'.opt[data-v="{a}"]').first.click(); pg.wait_for_timeout(1300)
    ok(H(K) == 200, f"Birinchi urinishda to'g'ri javob → +200 so'm (hamyon {H(K)})")
    NAV(pg, 'sinov-L.1-1', 400)
    a = ev("window.__bjCur().it.a"); xs = [x for x in ev("window.__bjCur().it.o.map(o=>String(o.v))") if x != str(a)]
    pg.locator(f'.opt[data-v="{xs[0]}"]').first.click(); pg.wait_for_timeout(700); pg.locator(f'.opt[data-v="{a}"]').first.click(); pg.wait_for_timeout(1300)
    ok(H(K) == 200, f"Avval xato, keyin to'g'ri → pul berilmaydi (hamyon {H(K)})")
    # ---- kuniga 30 ta chegarasi, javob logga yozilmaydi
    r = ev(f"""(()=>{{const A=BJ.A, b=A.S().bolalar['{R}']; let s=0; for (let i=0;i<40;i++) s+=A.pul.javob(b); const d=A.pul.st(b).kun[A.todayKey()];
      return [s, d.n, A.pul.st(b).h, A.readLog('{R}',A.todayKey()).filter(e=>e.t==='pul').length]}})()""")
    ok(r == [6000, 30, 6000, 0], f"40 ta javobdan faqat 30 tasiga pul (6 000), javob puli logni to'ldirmaydi {r}")
    # ---- uy ekrani: hamyon pill, do'kon tugmasi
    NAV(pg, 'uy', 400)
    ok('200' in pg.inner_text('[data-dokon]'), "Uyda do'kon tugmasida hamyon summasi (💵 200)")
    ok(pg.locator('.top .verb').inner_text() == 'v6' and pg.locator('.top .verb').is_visible(), "Uyda tepada oddiy versiya belgisi «v6» ko'rinadi")
    bb = ev("(()=>{const r=document.querySelector('.top [data-ota]').getBoundingClientRect(); return r.right})()"); ok(bb <= 390, f"Uy tepasidagi 👨‍👩‍👧 tugmasi ekrandan chiqmaydi (o'ng chet {bb})")
    ok(pg.locator('[data-dokon]').count() == 1, "Uyda «🛒 Do'kon» tugmasi")
    # ---- missiya mukofoti + 5 kun bonusi + o'rnatilgan detal tanlovi yangisiga bo'shaydi
    NAV(pg, 'missiya', 500)
    ev(f"""(()=>{{const A=BJ.A, b=A.S().bolalar['{K}'], wk=A.isoWeek(), T=A.todayKey(); A.weekDays(wk).filter(k=>k!==T).slice(0,4).forEach(k=>{{A.agg(b,k).missiya=1}});
      A.pul.st(b).joy.gildirak=0; const m=b.missiya; m.si=m.steps.findIndex(x=>x.k==='yakun'); A.save(true)}})()""")
    h0 = H(K); NAV(pg, 'missiya', 900)
    t = pg.inner_text('.reveal') if pg.locator('.reveal').count() else ''
    r = ev(f"""(()=>{{const A=BJ.A, b=A.S().bolalar['{K}'], p=A.pul.st(b); return [b.missiya.pulM, 'gildirak' in p.joy, A.readLog('{K}',A.todayKey()).filter(e=>e.t==='pul').map(e=>e.tur)]}})()""")
    ok(H(K) - h0 == 12000 and r[0] == 12000, f"Missiya +2 000 va haftada 5-kun bonusi +10 000 → +12 000 ({H(K) - h0})")
    ok('12 000' in t, f"Mukofot ekranida «💵 +12 000 so'm» ({t[:80]!r})")
    ok(not r[1] and r[2] == ['missiya', 'bonus'], f"Yangi detal kelganda o'sha turdagi tanlov bo'shaydi; log: {r[2]}")
    SHOT(pg, 'mukofot')
    r = ev(f"(()=>{{const A=BJ.A, b=A.S().bolalar['{K}']; return A.pul.missiya(b)}})()")
    ok(r == 2000, f"Shu haftada ikkinchi bonus yo'q — keyingi missiya faqat +2 000 ({r})")
    # ---- matnli uyga vazifa «✅ Bajardim» → +1 000
    ev(f"""(()=>{{const A=BJ.A, b=A.S().bolalar['{K}'], T=A.todayKey(); b.vazifa.push({{id:'vz1',berildi:T,muddat:T,fan:'izoh',bolim:null,n:0,izoh:"Kitob o'qi",qildi:0,ok:0,done:false}}); A.save(true)}})()""")
    h0 = H(K); NAV(pg, 'uy', 400); pg.click('[data-vzok="vz1"]'); pg.wait_for_timeout(400)
    ok(H(K) - h0 == 1000, f"Uyga vazifa bajarildi → +1 000 so'm ({H(K) - h0})")

    # ---- 👨‍👩‍👧 ota-ona: do'konga haqiqiy sovg'a (rasm siqiladi), ➕ qo'shimcha mukofot
    NAVO(pg, 'ota', 400)
    ok(pg.locator('[data-go="ota-pul"]').count() == 1, "Ota-ona menyusida «💰 Pul va do'kon»")
    NAVO(pg, 'ota-pul', 400)
    pg.select_option('#dk', Q); pg.fill('#dn', 'Lego mashina'); pg.fill('#dz', '12000'); pg.set_input_files('#dr', RASM); pg.wait_for_timeout(900)
    ok('hafta' in pg.inner_text('#dzi'), f"Narx yozilganda «taxminan N hafta yig'iladi» ({pg.inner_text('#dzi')})")
    pg.click('[data-dv]'); pg.wait_for_timeout(300)
    pg.select_option('#dk', 'hamma'); pg.fill('#dn', 'Muzqaymoq'); pg.fill('#dz', '3000'); pg.check('#dt'); pg.click('[data-dv]'); pg.wait_for_timeout(300)
    g = ev("BJ.A.S().dokon")
    ok(len(g) == 2 and g[0]['narx'] == 12000 and g[0]['kim'] == Q and g[0]['rasm'].startswith('data:image/jpeg') and len(g[0]['rasm']) <= 40000 and g[1]['takror'], f"2 ta sovg'a: Lego (12 000, rasm {len(g[0]['rasm'])} ≤ 40 000 belgi) va 🔁 Muzqaymoq")
    pg.fill(f'[data-sm="{R}"]', '1500'); pg.click(f'[data-pl="{R}"]'); pg.wait_for_timeout(300)
    ok(H(R) == 7500 and ev(f"BJ.A.readLog('{R}',BJ.A.todayKey()).some(e=>e.t==='pul'&&e.tur==='ota'&&e.s===1500)"), f"➕ 1 500 qo'shildi va logga yozildi ({H(R)})")
    ok(ev("document.documentElement.scrollWidth") <= 390, "Ota-ona «💰 Pul va do'kon» 390 px da surilmaydi")
    SHOT(pg, 'ota_pul')

    # ---- 2-sinf: kupyura bilan to'lash + qaytim savoli
    setj(Q); berP(Q, 15000); NAV(pg, 'dokon', 400)
    ok(pg.locator('.dsg').count() == 2 and pg.locator('[data-ol]').count() == 2, "Kattaning do'konida 2 sovg'a (o'ziniki + hammaga), ikkalasiga puli yetadi")
    ok(pg.locator('.kassa').count() == 1, "2-sinfda 🐷 cho'chqa-kassa bor")
    SHOT(pg, 'dokon_sovga')
    lego = ev("BJ.A.S().dokon[0].id"); pg.click(f'[data-ol="{lego}"]'); pg.wait_for_timeout(300)
    pg.click('.sheet [data-v="10000"]'); pg.wait_for_timeout(100); pg.click('.sheet [data-v="5000"]'); pg.wait_for_timeout(100)
    ok(pg.is_enabled('.sheet [data-ok]'), "15 000 berildi (narxi 12 000) — «To'lash» ochiq")
    pg.click('.sheet [data-ok]'); pg.wait_for_timeout(200)
    vs = ev("[...document.querySelectorAll('.sheet [data-q]')].map(x=>+x.dataset.q)")
    ok(3000 in vs and len(vs) >= 2, f"Qaytim savoli: variantlar {vs}")
    xato = [v for v in vs if v != 3000][0]; pg.click(f'.sheet [data-q="{xato}"]'); pg.wait_for_timeout(200)
    ok(H(Q) == 15000 and '15 000 − 12 000' in pg.inner_text('.sheet'), "Noto'g'ri qaytim → pul olinmaydi, maslahat «15 000 − 12 000 = ?»")
    SHOT(pg, 'qaytim')
    pg.click('.sheet [data-q="3000"]'); pg.wait_for_timeout(500)
    r = ev(f"BJ.A.pul.st(BJ.A.S().bolalar['{Q}']).xarid.map(x=>[x.nom,x.holat])")
    ok(H(Q) == 3000 and r == [['Lego mashina', 'kutish']], f"To'g'ri qaytim → sotib olindi, hamyonda 3 000, buyurtma kutishda {r}")
    NAV(pg, 'uy', 400); ok('Lego mashina' in pg.inner_text('.kidw') and '⏳' in pg.inner_text('.kidw'), "Bola uyida «⏳ Lego mashina — sotib olding!»")
    # ---- 🦄 salon: ortiqcha pul ogohlantirishi, taqa sotib olish va pegasus rangi
    berP(Q, 6000); NAV(pg, 'dokon', 300); pg.click('[data-tab="tun"]'); pg.wait_for_timeout(300)
    ok(pg.locator('.dprev .pegasus').count() == 1 and pg.locator('[data-kt="taqa"]').count() == 1, "Orol bolasida 🦄 salon (taqa, bant, yol…)")
    pg.click('[data-kt="taqa"]'); pg.wait_for_timeout(200); pg.click('[data-tv="1"]'); pg.wait_for_timeout(200)
    ok('#FFD54F' in pg.inner_html('.dprev'), "Oltin taqa tanlanganda oldindan ko'rish (tuyoqlar oltin)")
    pg.click('[data-sot]'); pg.wait_for_timeout(300)
    pg.click('.sheet [data-v="5000"]'); pg.click('.sheet [data-v="1000"]'); pg.wait_for_timeout(150)
    ok(not pg.is_enabled('.sheet [data-ok]') and pg.locator('.sheet .warn').count() == 1, "Ortiqcha pul berilsa — «bitta pul ortiqcha» va to'lash yopiq")
    pg.click('.sheet [data-t="1"]'); pg.wait_for_timeout(150); pg.click('.sheet [data-ok]'); pg.wait_for_timeout(200); pg.click('.sheet [data-q="2000"]'); pg.wait_for_timeout(500)
    r = ev(f"(()=>{{const b=BJ.A.S().bolalar['{Q}'], p=BJ.A.pul.st(b); return [p.h, p.ega.taqa, p.joy.taqa, BJ.A.bezak(b).taqa]}})()")
    ok(r == [3000, [1], 1, 1], f"Oltin taqa sotib olindi va o'rnatildi {r}")
    NAV(pg, 'uy', 400); ok('#FFD54F' in pg.inner_html('[data-xmap] .xhero'), "Bola uyidagi uchar otda oltin taqa (0.7.0 dan — xaritadagi qahramon)")
    # ---- 🐷 cho'chqa-kassa: solish, 14 kunda 2 marta +5%, olish
    r = ev(f"""(()=>{{const A=BJ.A, b=A.S().bolalar['{Q}'], p=A.pul.st(b); p.h=10000; const s=A.pul.kassaSol(b,5000); p.kassaTs=A.addDays(A.todayKey(),-14);
      const f=A.pul.kassaFoiz(b), k=p.kassa, ts=p.kassaTs===A.todayKey(), o=A.pul.kassaOl(b); return [s,f,k,ts,o,p.h,p.kassa]}})()""")
    ok(r == [5000, 600, 5600, True, 5600, 10600, 0], f"Kassa: 5 000 solindi → 14 kunda +300 +300 = 5 600 → olindi, hamyon 10 600 {r}")
    ok(ev(f"(()=>{{const b=BJ.A.S().bolalar['{K}']; return BJ.A.pul.st(b).kassa}})()") == 0, "Maktabgacha bolada kassa yo'q (kassaBor — faqat 1-sinfdan)")

    # ---- 👨‍👩‍👧 Berildi; maktabgacha — avtomatik to'lov; Bekor → pul qaytadi; 🔁 qayta sotuvda
    NAVO(pg, 'ota', 400); ok('🔔 1' in pg.inner_text('[data-go="ota-pul"]'), "Menyuda «💰 Pul va do'kon 🔔 1»")
    NAVO(pg, 'ota-pul', 400); pg.click('[data-bd]'); pg.wait_for_timeout(300)
    r = ev(f"BJ.A.pul.st(BJ.A.S().bolalar['{Q}']).xarid[0].holat"); ok(r == 'berildi', f"«✅ Berildi» → holat {r}")
    ok(ev(f"BJ.A.pul.sovgalar(BJ.A.S().bolalar['{Q}']).map(g=>g.nom)") == ['Muzqaymoq'], "Berilgan Lego (takrorsiz) do'kondan yo'qoladi")
    setj(K); berP(K, 5000); NAV(pg, 'dokon', 400)
    ok(pg.locator('.kassa').count() == 0, "Maktabgacha bolada kassa ko'rinmaydi")
    muz = ev("BJ.A.S().dokon[1].id"); pg.click(f'[data-ol="{muz}"]'); pg.wait_for_timeout(300)
    ok(pg.locator('.sheet .tray svg').count() >= 1, "Maktabgacha: «sotuvchiga beriladigan» pullar rasmda ko'rsatiladi")
    pg.click('.sheet [data-ok]'); pg.wait_for_timeout(500); ok(H(K) == 2000, f"Maktabgacha avtomatik to'lov: 5 000 − 3 000 = {H(K)}")
    NAVO(pg, 'ota-pul', 400); pg.click('[data-bk]'); pg.wait_for_timeout(300)
    r = ev(f"(()=>{{const p=BJ.A.pul.st(BJ.A.S().bolalar['{K}']); return [p.h, p.xarid[0].holat, BJ.A.pul.sovgalar(BJ.A.S().bolalar['{K}']).length]}})()")
    ok(r == [5000, 'bekor', 1], f"«↩️ Bekor» → pul qaytdi, 🔁 sovg'a yana sotuvda {r}")

    # ---- 🏎️ tuning: neon sotib olish, o'rnatish / almashtirish, rang, konstruktor qismi
    setj(K); berP(K, 30000); NAV(pg, 'dokon', 300); pg.click('[data-tab="tun"]'); pg.wait_for_timeout(300)
    ok(pg.locator('.dcar svg.car').count() == 1 and pg.locator('.chips .chip').count() == 11, f"Tuning garaj: mashina oldindan ko'rish + 11 bo'lim ({pg.locator('.chips .chip').count()})")
    pg.click('[data-kt="neon"]'); pg.wait_for_timeout(200); pg.click('[data-tv="2"]'); pg.wait_for_timeout(200)
    ok('#FF4FB0' in pg.inner_html('.dcar') and pg.locator('.dcar .neon').count() == 1, "Pushti neon oldindan ko'rinadi")
    SHOT(pg, 'tuning')
    pg.click('[data-sot]'); pg.wait_for_timeout(300); pg.click('.sheet [data-ok]'); pg.wait_for_timeout(500)
    r = ev(f"(()=>{{const b=BJ.A.S().bolalar['{K}'], p=BJ.A.pul.st(b); return [p.h, p.ega.neon, p.joy.neon]}})()")
    ok(r == [25000, [2], 2], f"Pushti neon sotib olindi (5 000) va o'rnatildi {r}")
    pg.click('[data-tv="0"]'); pg.wait_for_timeout(200); pg.click('[data-joy]'); pg.wait_for_timeout(200)
    pg.click('[data-tv="2"]'); pg.wait_for_timeout(200)
    ok(pg.locator('[data-joy]').count() == 1 and pg.locator('[data-sot]').count() == 0, "Sotib olingan narsa qayta pulsiz «🔧 O'rnatish»")
    pg.click('[data-joy]'); pg.wait_for_timeout(200)
    ok(ev(f"BJ.A.pul.st(BJ.A.S().bolalar['{K}']).joy.neon") == 2 and H(K) == 25000, "Qayta o'rnatildi, pul yechilmadi")
    pg.click('[data-kt="rang"]'); pg.wait_for_timeout(200); pg.click('[data-tv="6"]'); pg.wait_for_timeout(200); pg.click('[data-sot]'); pg.wait_for_timeout(300); pg.click('.sheet [data-ok]'); pg.wait_for_timeout(500)
    ok(H(K) == 20000 and ev(f"BJ.A.carRang(BJ.A.S().bolalar['{K}'])") == '#37474F', "Grafit bo'yoq (5 000) — mashina rangi #37474F")
    ok(pg.locator('[data-qism]').count() == 1, "Tuningda «🔧 Keyingi qism — 3 000 so'm» kartasi")
    q0 = ev(f"BJ.A.garaj.kons(BJ.A.S().bolalar['{K}']).q.length"); pg.click('[data-qism]'); pg.wait_for_timeout(300); pg.click('.sheet [data-ok]'); pg.wait_for_timeout(500)
    r = ev(f"(()=>{{const b=BJ.A.S().bolalar['{K}']; return [BJ.A.garaj.kons(b).q.length, BJ.A.readLog('{K}',BJ.A.todayKey()).some(e=>e.t==='kons'&&e.dokon===1)]}})()")
    ok(r[0] == q0 + 1 and r[1] and H(K) == 17000, f"Konstruktor qismi sotib olindi: {q0} → {r[0]} qism, log dokon:1")
    ok(ev("document.documentElement.scrollWidth") <= 390, "Tuning ekrani 390 px da surilmaydi")
    NAV(pg, 'missiya', 600)
    ok('#FF4FB0' in pg.inner_html('.road .rcar') and '#37474F' in pg.inner_html('.road .rcar'), "Missiya yo'lidagi mashinada pushti neon va grafit rang")
    ok(pg.locator('.top [data-pul]').count() == 1, "Missiya ekranida tepada 💵 hamyon")
    ev(f"(()=>{{const b=BJ.A.S().bolalar['{K}']; BJ.A.pul.st(b).h=1234500; b.yulduz=1234; BJ.A.save(true)}})()"); NAV(pg, 'uy', 400)
    bb = ev("(()=>{const r=document.querySelector('.top [data-ota]').getBoundingClientRect(); return r.right})()"); ok(bb <= 390, f"Katta summa va ko'p yulduzda ham 👨‍👩‍👧 tugmasi ekranda (o'ng chet {bb})")
    NAV(pg, 'missiya', 500); bb = ev("(()=>{const r=document.querySelector('.top [data-pul]').getBoundingClientRect(); return r.right})()"); ok(bb <= 390, f"Missiyada katta summali hamyon ekranga sig'adi (o'ng chet {bb})")
    # ---- rasmlar: yangi tuning qismlari to'g'ri SVG, id takrorlanmaydi
    r = ev("""(()=>{const A=BJ.art, out={}; const svg=A.car({gildirak:3,kuzov:3,motor:3,spoyler:3,nitro:3,rang:7,stiker:3,fara:3,shina:2,bamper:3,neon:3},{w:200});
      out.bm=['bm1','bm2','bm3'].every(c=>svg.includes(c)); out.shina=svg.includes('oqyoz'); out.neon=svg.includes('#76FF03')&&svg.includes('feGaussianBlur'); out.oq=svg.includes('ECEFF1')||/#ecef/i.test(svg);
      const ids=(svg.match(/id="([^"]+)"/g)||[]); out.uniq=new Set(ids).size===ids.length; const pg=A.pegasus({taqa:2,kokil:2},{w:200}); out.peg=pg.includes('#81D4FA')&&pg.includes('class="bant"')&&pg.includes('#7C4DFF');
      const d=document.createElement('div'); d.innerHTML=svg+pg+A.car({},{w:200}); document.body.appendChild(d); out.bad=d.querySelectorAll('parsererror').length; out.base=!A.car({},{w:200}).includes('class="neon"'); d.remove(); return out})()""")
    ok(r['bm'] and r['shina'] and r['neon'] and r['uniq'] and r['bad'] == 0, f"Mashina: bamper 1–3, oq yon yozuvli shina, yashil neon (blur) — to'g'ri SVG {r}")
    ok(r['peg'] and r['base'], "Uchar ot: zangori taqa, binafsha bant; tuningsiz mashinada neon yo'q")
    # ---- so'm o'chirilsa
    ev("(()=>{BJ.A.S().sozlama.pul=false; BJ.A.save(true)})()"); NAV(pg, 'uy', 300)
    ok(pg.locator('[data-pul]').count() == 0 and pg.locator('[data-dokon]').count() == 0, "So'm o'chirilsa — uyda hamyon va do'kon yo'q")
    NAV(pg, 'dokon', 300); ok(pg.locator('.dokon').count() == 0, "So'm o'chirilsa — #dokon uyga qaytaradi")
    ok(ev(f"BJ.A.pul.javob(BJ.A.S().bolalar['{K}'])") == 0, "So'm o'chirilsa — javobga pul yo'q")
    ev("(()=>{BJ.A.S().sozlama.pul=true; BJ.A.save(true)})()")
    # ---- eski holatdan yangilanish (sozlama.pul yo'q, S.dokon yo'q, bola.pul yo'q)
    pg.close(); pg = ctx.new_page(); pg.on('pageerror', lambda e: ERR.append(f'pageerror: {e}')); ev = pg.evaluate
    pg.goto(URL + 'manifest.webmanifest'); pg.wait_for_timeout(200)  # ilova ishlamaydigan sahifa — holat qayta yozilmaydi
    ev("""(()=>{const s=JSON.parse(localStorage.getItem('bj_state_v1')); delete s.sozlama.pul; delete s.sozlama.byudjet; delete s.sozlama.kassa; delete s.dokon; Object.values(s.bolalar).forEach(b=>delete b.pul); localStorage.setItem('bj_state_v1', JSON.stringify(s))})()""")
    pg.goto(URL + '?tez=1&eski=1#uy'); pg.wait_for_timeout(500)
    r = ev(f"(()=>{{const s=BJ.A.S(); return [s.sozlama.pul, s.sozlama.byudjet, Array.isArray(s.dokon), BJ.A.pul.st(s.bolalar['{K}']).h]}})()")
    ok(r == [True, 50000, True, 0], f"Eski (0.5.x) holatdan: so'm yoqiladi, byudjet 50 000, hamyon 0 {r}")
    ok(pg.locator('[data-dokon]').count() == 1, "Eski holatdan keyin uyda do'kon tugmasi")
    br.close()
srv.terminate()
print('\nXATOLAR:', ERR if ERR else "yo'q"); sys.exit(1 if ERR else 0)
