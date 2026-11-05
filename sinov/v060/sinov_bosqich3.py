"""Bilimjon 0.6.0 — 3-bosqich: 🎨 realistik mashina va ikonkalar, 🔧 garaj (konstruktor + krash-test), 🤖 kod-yo'l (L.11).
Ishga tushirish: python3 sinov/v060/sinov_bosqich3.py  (skrinshotlar: /tmp/bj060_3_*.png)"""
import os, sys, time, subprocess
from playwright.sync_api import sync_playwright

D = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.abspath(os.path.join(D, '..', '..'))
PORT = 8773; URL = f'http://localhost:{PORT}/'
srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT)], cwd=SITE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
ERR = []
def ok(c, m):
    print(('✅ ' if c else '❌ ') + m)
    if not c: ERR.append(m)
def NAV(pg, h, ms=400):
    pg.goto(URL + '?tez=1#' + h); pg.evaluate('BJ.A.render()'); pg.wait_for_timeout(ms)
SHOT = lambda pg, n: pg.screenshot(path=f'/tmp/bj060_3_{n}.png', full_page=True)

with sync_playwright() as p:
    br = p.chromium.launch(); ctx = br.new_context(viewport={'width': 390, 'height': 844}, service_workers='block'); pg = ctx.new_page()
    pg.on('pageerror', lambda e: ERR.append(f'pageerror: {e}')); ev = pg.evaluate
    pg.goto(URL + '?tez=1'); pg.wait_for_timeout(400)
    pg.fill('#on', 'Sinov'); pg.fill('#p1', '1234'); pg.fill('#p2', '1234'); pg.click('#go'); pg.wait_for_timeout(300)
    K, Q = ev("""(()=>{const A=BJ.A; const k=A.newBola({laqab:'Kichik',daraja:'g0',avatar:'🐯',dunyo:'garaj'}); const q=A.newBola({laqab:'Katta',daraja:'g2',avatar:'🦄',dunyo:'orol'});
      A.S().sozlama.uyqu=''; A.S().joriy=k.id; A.save(true); return [k.id,q.id]})()""")
    setj = lambda i: ev(f"(()=>{{const s=BJ.A.S(); s.joriy='{i}'; BJ.A.save(true)}})()")
    # ---- 🎨 realistik mashina va ikonkalar
    r = ev("""(()=>{const A=BJ.art, out={}; const svg=A.car({gildirak:3,kuzov:3,motor:3,spoyler:3,nitro:3,rang:4,stiker:3,fara:3},{w:200});
      out.car = /<svg class="car"/.test(svg) && /clipPath/.test(svg) && /class="wheel"/.test(svg); const ids=(svg.match(/id="([^"]+)"/g)||[]); out.uniq = new Set(ids).size===ids.length;
      out.icons = A.ICON_KEYS.every(k=>/^<svg class="ico"/.test(A.icon(k,{s:40}))); out.n = A.ICON_KEYS.length; out.none = A.icon('yoq')==='';
      const d=document.createElement('div'); d.innerHTML=A.car({},{w:200})+A.icon('marra',{s:40}); document.body.appendChild(d); out.bad = d.querySelectorAll('parsererror').length; d.remove(); return out})()""")
    ok(r['car'] and r['uniq'], "Yangi mashina: kesish, shina/disk guruhlari, gradient id'lari takrorlanmaydi")
    ok(r['icons'] and r['n'] >= 23 and r['none'], f"{r['n']} ta realistik ikonka; noma'lum kalit — bo'sh (emoji zaxira ishlaydi)")
    # ---- 🔧 qism olish: har ?tez da 2 ta birinchi urinishdagi to'g'ri javob → 1 qism; orol bolasiga yo'q
    r = ev(f"""(()=>{{const A=BJ.A, b=A.S().bolalar['{K}'], q=A.S().bolalar['{Q}']; const a=[A.konsJavob(b),A.konsJavob(b),A.konsJavob(q)]; return [a, b.kons.q.slice(), b.kons.n, !!q.kons]}})()""")
    ok(r[0][0] is None and r[0][1] == 'rama' and r[0][2] is None and r[1] == ['rama'] and r[2] == 0 and not r[3], f"Kerakli sondagi to'g'ri javobdan keyin 1-qism (rama); orol bolasiga qism berilmaydi {r}")
    lg = ev(f"BJ.A.readLog('{K}',BJ.A.todayKey()).filter(e=>e.t==='kons').length"); ok(lg == 1, 'Log: {t:"kons"}')
    # onAnswer orqali (sinov ekrani, tanlov savoli birinchi urinishda to'g'ri)
    setj(K); NAV(pg, 'sinov-L.1-1', 400)
    a = ev("window.__bjCur().it.a"); pg.locator(f'.opt[data-v="{a}"]').first.click(); pg.wait_for_timeout(1500)
    ok(ev(f"BJ.A.S().bolalar['{K}'].kons.n") == 1, "Birinchi urinishda to'g'ri javob — garaj hisoblagichi +1 (onAnswer)")
    # ---- uy ekrani: garaj tugmasi, ikonkali detallar, yo'ldagi realistik mashina
    ev(f"""(()=>{{const A=BJ.A, b=A.S().bolalar['{K}']; ['gildirak','kuzov','motor'].forEach((k,i)=>b.detal.push({{k,t:1,nom:k,ic:'🔩',ts:Date.now()}})); A.save(true)}})()""")
    NAV(pg, 'uy', 500)
    t = pg.inner_text('[data-garaj]')
    ok('Garaj' in t and '1/6' in t, f'Uyda «🔧 Garaj — Poyga bolidi: 1/6 qism» tugmasi ({t.strip()})')
    ok(pg.locator('.coll .ico').count() == 3, "Detallar qatorida emoji o'rniga realistik ikonkalar")
    ok(ev("document.documentElement.scrollWidth") <= 390, "Uy ekrani 390 px da gorizontal surilmaydi")
    SHOT(pg, 'uy_garaj')
    setj(Q); NAV(pg, 'uy', 400)
    ok(pg.locator('[data-garaj]').count() == 0, "Orol bolasida garaj tugmasi yo'q")
    NAV(pg, 'garaj', 300); ok(pg.locator('.gcard').count() == 0, "Orol bolasi #garaj ochsa — uyiga qaytadi")
    setj(K)
    # ---- garaj ekrani va yig'ish (hamma qism bor)
    ev(f"""(()=>{{const A=BJ.A, b=A.S().bolalar['{K}']; b.kons.q=A.garaj.loy(0).q.slice(); A.save(true)}})()""")
    NAV(pg, 'garaj', 500)
    ok(pg.locator('.gq.bor').count() == 6 and pg.locator('[data-yig]').count() == 1, "Garaj: 6/6 qism, «🔧 Yig'ishni boshlash» tugmasi")
    ok(ev("document.documentElement.scrollWidth") <= 390, "Garaj 390 px da sig'adi"); SHOT(pg, 'garaj')
    pg.click('[data-yig]'); pg.wait_for_timeout(500)
    ok(pg.locator('.ypart').count() == 6 and pg.locator('.yslot').count() == 6, "Yig'ish: 6 qism va 6 ta soya-uya")
    SHOT(pg, 'yigish_bosh')
    # xato joy: spoylerni old g'ildirak uyasiga
    pg.click('.ypart[data-p="spoyler"]'); bb = pg.locator('.yslot[data-s="gOld"]').bounding_box(); pg.mouse.click(bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] / 2); pg.wait_for_timeout(200)
    ok(pg.locator('.yslot.on').count() == 0 and pg.locator('.ypart').count() == 6, "Noto'g'ri uyaga qo'yilmaydi")
    # sudrash bilan: rama
    pe = pg.locator('.ypart[data-p="rama"]').bounding_box(); bb = pg.locator('.yslot[data-s="rama"]').bounding_box()
    pg.mouse.move(pe['x'] + pe['width'] / 2, pe['y'] + pe['height'] / 2); pg.mouse.down(); pg.mouse.move(bb['x'] + bb['width'] * 0.3, bb['y'] + bb['height'] / 2, steps=8); pg.mouse.up(); pg.wait_for_timeout(250)
    ok(pg.locator('.yslot.on').count() == 1, "Sudrab qo'yish ishlaydi (rama)")
    # qolganlari bosib-tanlab; g'ildiraklar almashtirilsa ham (bolidda o'lchami boshqa — faqat o'z joyiga)
    for q in ['gOrqa', 'motor', 'kuzov', 'gOld', 'spoyler']:
        pg.click(f'.ypart[data-p="{q}"]'); bb = pg.locator(f'.yslot[data-s="{q}"]').bounding_box(); pg.mouse.click(bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] / 2); pg.wait_for_timeout(200)
    pg.wait_for_timeout(400)
    r = ev(f"(()=>{{const k=BJ.A.S().bolalar['{K}'].kons; return [k.tayyor.length, k.li, k.q.length, k.tayyor[0]&&k.tayyor[0].holat]}})()")
    ok(r == [1, 1, 0, 'butun'] and pg.locator('[data-kr]').count() == 1, f"Mashina yig'ildi → «tayyor» ro'yxatida, keyingi loyiha (monster-trak) boshlandi {r}")
    SHOT(pg, 'yigildi')
    # ---- 💥 krash-test
    pg.click('[data-kr]'); pg.wait_for_timeout(2300); SHOT(pg, 'krash')
    ok(pg.locator('.fxlayer').count() == 1, "Krash-test sahnasi (≤8 s, o'tkazib yuboriladi)")
    pg.wait_for_timeout(1500)
    r = ev(f"(()=>{{const k=BJ.A.S().bolalar['{K}'].kons; return [k.tayyor[0].holat, k.tayyor[0].krash]}})()")
    ok(r == ['buzuq', 1] and pg.locator('.ypart').count() == 6, f"Krashdan keyin parchalandi → qayta yig'ish ekrani {r}")
    lg = ev(f"BJ.A.readLog('{K}',BJ.A.todayKey()).filter(e=>e.t==='garaj').map(e=>e.hodisa).join(',')"); ok(lg == 'yigdi,krash', f'Log: yigdi, krash ({lg})')
    st = ev("BJ.fx.stats.effects.filter(e=>e.kind==='krash').map(e=>e.ms)"); ok(st and max(st) <= 8000, f'Krash sahnasi uzunligi ≤ 8 s ({st})')
    for q in ['rama', 'gOrqa', 'motor', 'kuzov', 'gOld', 'spoyler']:
        pg.click(f'.ypart[data-p="{q}"]'); bb = pg.locator(f'.yslot[data-s="{q}"]').bounding_box(); pg.mouse.click(bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] / 2); pg.wait_for_timeout(150)
    pg.wait_for_timeout(300)
    r = ev(f"(()=>{{const k=BJ.A.S().bolalar['{K}'].kons; return [k.tayyor.length, k.tayyor[0].holat, k.tayyor[0].yig]}})()")
    ok(r == [1, 'butun', 2], f"Qayta yig'ildi: yangi mashina qo'shilmadi, holat butun {r}")
    # monster-trak: ikki g'ildirak bir xil — almashtirib qo'ysa ham bo'ladi
    ev(f"""(()=>{{const A=BJ.A, b=A.S().bolalar['{K}']; b.kons.q=A.garaj.loy(1).q.slice(); A.save(true)}})()""")
    NAV(pg, 'garaj', 400); pg.click('[data-yig]'); pg.wait_for_timeout(400)
    pg.click('.ypart[data-p="gOld"]'); bb = pg.locator('.yslot[data-s="gOrqa"]').bounding_box(); pg.mouse.click(bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] / 2); pg.wait_for_timeout(200)
    ok(pg.locator('.yslot.on').count() == 1 and pg.locator('.ypart[data-p="gOld"]').count() == 0 and pg.locator('.ypart[data-p="gOrqa"]').count() == 1, "Monster-trak: bir xil g'ildiraklar istalgan uyaga tushadi")
    SHOT(pg, 'yigish_trak')
    # ---- 🌙 kun chegarasi garajga ham amal qiladi
    ev(f"(()=>{{const A=BJ.A; A.agg(A.S().bolalar['{K}']).faol=40*60; A.damSinov=true; A.save(true)}})()")
    NAV(pg, 'garaj', 400); ok(pg.locator('.dam').count() == 1, 'Vaqt tugaganda garaj ham yopiq')
    ev(f"(()=>{{const A=BJ.A; A.agg(A.S().bolalar['{K}']).faol=0; A.damSinov=false; A.save(true)}})()")
    # ---- 🤖 kod-yo'l generatori
    r = ev("""(()=>{const g=BJ.gen, bad=[]; let st={1:[99,0],2:[99,0],3:[99,0]}; for(const q of [1,2,3]) for(let i=0;i<150;i++){ const it=g.make('L.11',q,{}); const v=g.valid(it); if(v!==true) bad.push(q+':'+v);
      const n=it.runs.reduce((a,r)=>a+r[1],0); st[q][0]=Math.min(st[q][0],n); st[q][1]=Math.max(st[q][1],n); if(q===1&&(it.slot||it.takror)) bad.push('q1 slot'); if(q>1&&(!it.takror||it.runs.length>it.slot)) bad.push('slot');
      if(it.ex.path.some(c=>it.tos.includes(c))) bad.push('tos yolda'); } return {bad:bad.slice(0,5), st}})()""")
    ok(not r['bad'], f"L.11: 450 ta topshiriq yaroqli, to'siq yo'lda emas, buyruq joyi yetadi ({r['bad']})")
    ok(3 <= r['st']['1'][0] and r['st']['1'][1] <= 5 and r['st']['2'][1] <= 8 and r['st']['3'][1] <= 11, f"Qadamlar: q1 3–5, q2 ≤8, q3 ≤11 ({r['st']})")
    ok(ev("BJ.A.MANT_KUN.g0.flat().includes('L.11') && BJ.A.MANT_KUN.g1.flat().includes('L.11') && BJ.A.MANT_KUN.g2.flat().includes('L.11')"), "Kod-yo'l uchala darajaning mantiq jadvalida")
    # ---- 🤖 kod-yo'l UI (maktabgacha, q1): avval xato, keyin to'g'ri dastur
    NAV(pg, 'sinov-L.11-1', 400)
    it = ev("window.__bjCur().it")
    ok(pg.locator('.kyb .ico').count() >= 2 + len(it['tos']) and pg.locator('[data-n]').count() == 0, "Kod-yo'l: realistik mashina, marra, konuslar; maktabgachada «×» yo'q")
    SHOT(pg, 'kodyol_q1')
    # xato: start chetidan tashqariga
    sx, sy, w = it['start'] % it['w'], it['start'] // it['w'], it['w']
    d0 = 0 if sy == 0 else 3 if sx == 0 else 2 if sy == it['h'] - 1 else 1 if sx == w - 1 else None
    if d0 is None:  # chetda emas — to'siqqa yoki yo'q bo'lsa, to'xtab qolish xatosi
        d0 = (it['runs'][0][0] + 2) % 4
    pg.click(f'[data-d="{d0}"]'); pg.click('[data-run]'); pg.wait_for_timeout(500)
    fb = pg.inner_text('#fb'); ok(('Bum' in fb) or ("to'xtadi" in fb), f"Xato dastur: «💥 Bum!» yoki «🛑 to'xtadi» ({fb.strip()[:40]})")
    pg.wait_for_timeout(300); pg.click('[data-del]')
    for d, n in it['runs']:
        for _ in range(n): pg.click(f'[data-d="{d}"]')
    ok(pg.locator('.kyc').count() == sum(n for _, n in it['runs']), "Maktabgacha: har bosish — bitta buyruq")
    pg.click('[data-run]'); pg.wait_for_timeout(1500)
    r = ev("window.__bjCur().sinovNatija")
    ok(r and r['togri'] and r['xato_soni'] == 0, f"To'g'ri dastur → marraga yetdi; 1 ta xato hali «birinchi urinish» (sinov — me'yoriy) {r and {k: r[k] for k in ('togri', 'xato_soni')}}")
    # ---- q2 (orol, takror va buyruq joyi)
    setj(Q); NAV(pg, 'sinov-L.11-2', 400); it = ev("window.__bjCur().it")
    ok(pg.locator('.kyc.bo').count() == it['slot'] and pg.locator('[data-n]').count() == 3, f"q2: {it['slot']} ta buyruq joyi va ×2 ×3 ×4 tugmalari")
    for i in range(it['slot'] + 1): pg.click('[data-d="1"]')
    ok(pg.locator('.kyc:not(.bo)').count() == it['slot'], "Joy to'lsa yangi buyruq qo'shilmaydi")
    for i in range(it['slot']): pg.click('[data-del]')
    for d, n in it['runs']:
        pg.click(f'[data-d="{d}"]')
        if n > 1: pg.click(f'[data-n="{n}"]')
    SHOT(pg, 'kodyol_q2_orol')
    pg.click('[data-run]'); pg.wait_for_timeout(1500)
    r = ev("window.__bjCur().sinovNatija"); ok(r and r['togri'] and r['xato_soni'] == 0, "Takrorli dastur (masalan ➡️×3) to'g'ri bajarildi")
    # ---- labirint va missiya yo'li: realistik qahramon
    setj(K); NAV(pg, 'sinov-L.6-1', 400)
    ok(pg.locator('.maze .ico').count() == 2, "Labirintda emoji o'rniga realistik mashina va marra bayrog'i")
    pg.click('[data-d="1"]'); pg.wait_for_timeout(100); SHOT(pg, 'labirint')
    NAV(pg, 'missiya', 800)
    ok(pg.locator('.road .rcar svg.car').count() == 1 and pg.locator('.road .rflag .ico').count() == 1, "Missiya yo'lida bolaning o'z mashinasi va marra bayrog'i")
    SHOT(pg, 'missiya')
    br.close()
srv.terminate()
print('\nXATOLAR:', ERR if ERR else "yo'q"); sys.exit(1 if ERR else 0)
