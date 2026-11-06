"""Bilimjon 0.7.0 — 3-bosqich: 🌍 Kashfiyot 2.0 · 📖 Uch marta o'qish · 🕌 TJ.7 ra (tafxim/tarqiq) va TJ.8 vaqf belgilari.
Kontent (30 mavzu, uy tajribalari, 26 matn so'z soni), ra dvigateli (qo'lda yozilgan javoblar bilan), generatorlar gen.valid,
kashfiyot oqimi (karta → 1 savol → «🏠 Uyda sinab ko'r» → uyda «✅ Bajardim» → +2 ⭐), viktorina = shu hafta mavzulari,
uch marta o'qish (3 o'qish, juda tez → qayta, kattalar tinglaydi → WCPM, natija, savol), ota-ona panellari, 390 px.
Ishga tushirish: python3 sinov/v070/sinov_bosqich3.py  (skrinshotlar: /tmp/bj070_3_*.png)"""
import os, sys, time, subprocess, datetime, json
from playwright.sync_api import sync_playwright

D = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.abspath(os.path.join(D, '..', '..'))
PORT = 8781; URL = f'http://localhost:{PORT}/'
srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT)], cwd=SITE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
ERR = []
def ok(c, m):
    print(('✅ ' if c else '❌ ') + m)
    if not c: ERR.append(m)
NV = [0]
SHOT = lambda pg, n: pg.screenshot(path=f'/tmp/bj070_3_{n}.png', full_page=True)
JUMA, YAKSH = datetime.datetime(2026, 11, 6, 10, 0), datetime.datetime(2026, 11, 8, 10, 0)
# Ra hukmi — qo'lda (tajvid kitoblari bo'yicha) yozilgan javoblar; dvigatel shunga teng bo'lishi shart
RA_QOLDA = {'رَبِّ': 'tafxim', 'رُسُلٌ': 'tafxim', 'رِجَالٌ': 'tarqiq', 'مَرْيَمُ': 'tafxim', 'الْأَرْضِ': 'tafxim', 'الْقُرْآنُ': 'tafxim', 'يُرْزَقُونَ': 'tafxim',
            'فِرْعَوْنَ': 'tarqiq', 'مِرْيَةٍ': 'tarqiq', 'شِرْعَةً': 'tarqiq', 'قِرْطَاسٍ': 'tafxim', 'مِرْصَادًا': 'tafxim', 'فِرْقَةٍ': 'tafxim', 'ارْجِعِي': 'tafxim'}
RAV_QOLDA = {'وَالْفَجْرِ': 'tafxim', 'الْقَدْرِ': 'tafxim', 'وَالْعَصْرِ': 'tafxim', 'خُسْرٍ': 'tafxim', 'ذِكْرٌ': 'tarqiq', 'خَيْرٌ': 'tarqiq', 'قَدِيرٌ': 'tarqiq',
             'الْبَصِيرُ': 'tarqiq', 'النَّارِ': 'tafxim', 'غَفُورٌ': 'tafxim'}

try:
  with sync_playwright() as p:
    br = p.chromium.launch(); ctx = br.new_context(viewport={'width': 390, 'height': 844}, service_workers='block'); pg = ctx.new_page()
    pg.clock.set_fixed_time(JUMA)
    pg.on('pageerror', lambda e: ERR.append(f'pageerror: {e}')); ev = pg.evaluate
    def NAV(h, ms=500, ota=False):
        NV[0] += 1; pg.goto(URL + f'?tez=1&r={NV[0]}#' + h)
        ev(("BJ.A.otaOk={rol:'admin',t:Date.now()}; " if ota else '') + 'BJ.A.render()'); pg.wait_for_timeout(ms)
    def GO(h, ms=400):
        ev(f"location.hash='{h}'"); pg.wait_for_timeout(ms)
    pg.goto(URL + '?tez=1'); pg.wait_for_timeout(400)
    pg.fill('#on', 'Sinov'); pg.fill('#p1', '1234'); pg.fill('#p2', '1234'); pg.click('#go'); pg.wait_for_timeout(300)
    K, Q, R = ev("""(()=>{const A=BJ.A; const k=A.newBola({laqab:'Kichik',daraja:'g0',avatar:'🐯',dunyo:'garaj'}); const q=A.newBola({laqab:'Katta',daraja:'g2',avatar:'🦄',dunyo:'orol'});
      const r=A.newBola({laqab:'Orta',daraja:'g1',avatar:'🐼',dunyo:'garaj'});
      [k,q,r].forEach(b=>{b.boshlandi='2026-10-28';}); A.S().sozlama.uyqu=''; A.S().joriy=r.id; A.save(true); return [k.id,q.id,r.id]})()""")
    setj = lambda bid: ev(f"(()=>{{const s=BJ.A.S(); s.joriy='{bid}'; BJ.A.save(true)}})()")
    X = lambda bid, e: ev(f"(()=>{{const A=BJ.A, B=BJ.bank, b=A.S().bolalar['{bid}']; return {e}}})()")
    W390 = lambda: ev("[document.documentElement.scrollWidth, Math.max(...[...document.querySelectorAll('.top .ib, .top .pill')].map(e=>e.getBoundingClientRect().right), 0)]")
    def missiyaQadam(bid, k, final=False):
        return X(bid, f"(()=>{{const m=b.missiya=A.{'buildFinal' if final else 'buildMission'}(b); m.si=m.steps.findIndex(s=>s.k==='{k}'); A.save(true); return m.si}})()")

    # ================= 1. KONTENT =================
    r = ev("""(()=>{const B=BJ.bank, K=['kosmos','osmon','suv','tabiat','hayvon','tana','texnika','yer']; const bad=[];
      B.kashf.forEach(k=>{ if(!K.includes(k.kat)) bad.push(k.id+' kat'); const u=k.uy; if(!u||!u.t||!Array.isArray(u.s)||u.s.length!==4||new Set(u.s.slice(1)).size!==3||(u.a!=null&&!(u.a>=0&&u.a<=2))||!u.iz) bad.push(k.id+' uy');
        if(k.d.length!==3) bad.push(k.id+' d'); k.d.forEach((d,i)=>{ if(!d.t||!d.s.length) bad.push(k.id+' t'+i); d.s.forEach(s=>{ if(s.length!==4||new Set(s.slice(1)).size!==3) bad.push(k.id+' s'+i); }); });
        if(!Array.isArray(k.en)||k.en.length!==2) bad.push(k.id+' en'); });
      return [B.kashf.length, new Set(B.kashf.map(k=>k.id)).size, bad]})()""")
    ok(r[0] == 30 and r[1] == 30 and not r[2], f"🌍 30 mavzu (k1–k30), hammasida kat + uy tajribasi + 3 chuqurlik {r[2][:5]}")
    r = ev("""(()=>{const B=BJ.bank, wc=t=>t.split(/\\s+/).filter(w=>/[A-Za-z0-9']/.test(w)).length, bad=[];
      B.matn.filter(m=>+m.id.slice(1)>=7).forEach(m=>{const n=wc(m.t); if(m.d===1?(n<35||n>55):(n<70||n>100)) bad.push(m.id+':'+n); if(m.s.length<2||m.s.length>3) bad.push(m.id+' s'); m.s.forEach(s=>{if(s.length!==4||new Set(s.slice(1)).size!==3) bad.push(m.id+' v');});});
      return [B.matn.filter(m=>m.d===1).length, B.matn.filter(m=>m.d===2).length, new Set(B.matn.map(m=>m.id)).size===B.matn.length, bad]})()""")
    ok(r[0] == 13 and r[1] == 13 and r[2] and not r[3], f"📖 Matnlar: d1 13 ta, d2 13 ta, yangi 20 tasi so'z soni (35–55 / 70–100) va 2–3 savol {r[3]}")
    r = ev("""(()=>{const g=BJ.gen, B=BJ.bank; let n=0, bad=[]; B.kashf.forEach(k=>[1,2,3].forEach(q=>{const d=k.d[q-1]; for(let si=0;si<d.s.length+1;si++){const it=g.make('KASHF',q,{kashfId:k.id,kashfSavol:si}); n++; const v=g.valid(it); if(v!==true) bad.push(k.id+q+':'+v);}})); return [n,bad]})()""")
    ok(r[0] >= 90 and not r[1], f"KASHF generatori: {r[0]} ta topshiriq gen.valid {r[1][:3]}")

    # ================= 2. 🕌 RA DVIGATELI va TJ.7 / TJ.8 =================
    r = ev("""(()=>{const a=BJ.arab; return [a.RA.map(w=>[w,a.raHukm(w).h]), a.RAV.map(w=>[w,a.raHukm(w,{v:true}).h])]})()""")
    xa = [w for w, h in r[0] if RA_QOLDA.get(w) != h]; xv = [w for w, h in r[1] if RAV_QOLDA.get(w) != h]
    ok(len(r[0]) == 14 and not xa, f"Ra dvigateli: 14 ta oddiy misol qo'lda yozilgan hukmga teng {xa}")
    ok(len(r[1]) == 10 and not xv, f"Ra dvigateli: 10 ta vaqf misoli qo'lda yozilgan hukmga teng {xv}")
    r = ev("""(()=>{const a=BJ.arab, bog=w=>{const out=[];let c=null;for(const ch of w){if(/[\\u064B-\\u0670\\u065F]/.test(ch)){if(c)c.m.push(ch)}else if(/[\\u0621-\\u064A]/.test(ch)){c={h:ch,m:[]};out.push(c)}else c=null}return out};
      const ws=a.RA.concat(a.RAV), bad=[]; ws.forEach(w=>{ if((w.match(/ر/g)||[]).length!==1) bad.push(w+' ra'); bog(w).forEach(x=>{ if(x.m.filter(c=>c!=='\\u0651').length>1) bad.push(w+' harakat'); }); });
      a.VQO.forEach(e=>e.p.filter(x=>typeof x==='string').forEach(w=>bog(w).forEach(x=>{ if(x.m.filter(c=>c!=='\\u0651').length>1) bad.push(w+' harakat'); })));
      const joiz=['مِصْرَ','الْقِطْرِ','يَسْرِ','فِرْقٍ'].filter(w=>ws.includes(w)); return [bad, joiz]})()""")
    ok(not r[0] and not r[1], f"Har so'zda bitta ر, har harfda ≤ 1 harakat; ikkalasi joiz so'zlar qo'shilmagan {r}")
    r = ev("""(()=>{const g=BJ.gen; const out={}; ['TJ.7','TJ.8'].forEach(id=>{let n=0,bad=[],tur=new Set(); [1,2,3].forEach(q=>[true,false].forEach(g0=>{for(let i=0;i<80;i++){const it=g.make(id,q,{g0}); n++; const v=g.valid(it); if(v!==true) bad.push(q+':'+v); tur.add(it.k.slice(0,2));}})); out[id]=[n,bad.slice(0,3),[...tur].sort()];}); return out})()""")
    ok(r['TJ.7'][0] == 480 and not r['TJ.7'][1] and set(r['TJ.7'][2]) >= {'rb', 'rh', 'rs'}, f"TJ.7: 480 topshiriq (3 qiyinlik × g0/katta) gen.valid, 3 xil savol turi {r['TJ.7'][2]} {r['TJ.7'][1]}")
    ok(r['TJ.8'][0] == 480 and not r['TJ.8'][1] and set(r['TJ.8'][2]) >= {'vb', 'vm', 'vo'}, f"TJ.8: 480 topshiriq gen.valid, belgi/ma'no/oyat turlari {r['TJ.8'][2]} {r['TJ.8'][1]}")
    r = ev("""(()=>{const a=BJ.arab, g=BJ.gen; return [a.TJ.includes('TJ.7')&&a.TJ.includes('TJ.8'), a.BOLIM.tajvid.ids.length, a.BOLIM.aralash.ids.includes('TJ.8'), !!a.TJ_MISOL['TJ.7']&&a.TJ_MISOL['TJ.7'].length, a.TJ_MISOL['TJ.8'].length,
      a.DARS['TJ.7'].length, a.QADAM['TJ.7'](g.make('TJ.7',3,{})).length, a.QADAM['TJ.8'](g.make('TJ.8',3,{})).length>=2,
      a.mavjud({sozlama:{tjTasdiq:{}}},['TJ.7','TJ.8']).length, a.mavjud({sozlama:{tjTasdiq:{'TJ.7':1}}},['TJ.7','TJ.8']).join()]})()""")
    ok(r[0] and r[1] == 8 and r[2] and r[3] == 24 and r[4] == 10, f"TJ ro'yxati 8 ta, tajvid/aralash bo'limida, tasdiq misollari (24 ra, 7 belgi + 3 oyat) {r[:5]}")
    ok(r[5] == 4 and r[6] == 3 and r[7] and r[8] == 0 and r[9] == 'TJ.7', f"DARS + QADAM (3 qadam), tasdiqsiz yopiq, faqat tasdiqlangani ochiq {r[5:]}")
    r = ev("""(()=>{const g=BJ.gen, it=g.make('TJ.7',1,{g0:true}); return [it.ota||'', it.t, it.o.length]})()""")
    ok('arabchasini' in r[0], f"Maktabgacha bolaga ota-ona maslahati qo'shiladi {r}")

    # ================= 3. 🌍 KASHFIYOT OQIMI =================
    ok(X(R, "[A.S().sozlama.kashfUy, Array.isArray(b.kashfUy), b.uch]") == [True, True, None], "Standart: sozlama.kashfUy = true, b.kashfUy = [], b.uch = null")
    ok(X(R, "(()=>{const s=A.migrate(JSON.parse(JSON.stringify(Object.assign({}, A.S(), {sozlama:{ovoz:.5}})))); const x=Object.values(s.bolalar)[0]; delete x.kashfUy; A.migrate(s); return [s.sozlama.kashfUy, Array.isArray(Object.values(s.bolalar)[0].kashfUy)]})()") == [True, True], "Eski holatdan yangilanganda ham kashfUy bor")
    setj(R); missiyaQadam(R, 'kashf'); NAV('missiya', 600)
    kid = X(R, "b.missiya.steps[b.missiya.si].id")
    ok(pg.locator('.kcard.k2 .ksc svg.ksc-svg').count() == 1 and pg.locator('.kmed').count() == 1, f"Kashfiyot kartasi: realistik sahna + shisha medalyon ({kid})")
    ok(pg.locator('.kcard .dragon, .kcard svg.drg, .kcard .drg').count() == 0 and 'ajdar' not in pg.inner_html('.kcard').lower(), "Kartada ajdar YO'Q")
    ok(pg.locator('.kkat').count() == 1, f"Kategoriya yorlig'i: {pg.inner_text('.kkat') if pg.locator('.kkat').count() else '-'}")
    w = W390(); bb = ev("document.querySelector('.kcard').getBoundingClientRect().right")
    ok(w[0] <= 390 and bb <= 390, f"390 px: kashfiyot kartasi {w} {bb}")
    SHOT(pg, 'kashf_karta')
    pg.click('[data-go]'); pg.wait_for_timeout(500)
    ok(X(R, "b.missiya.steps[b.missiya.si].savollar") == 1, "Kashfiyotda 1 ta savol")
    ev("window.__bjJavob(true)")
    try: pg.wait_for_selector('.kuy [data-ok], [data-next]', timeout=5000)
    except Exception: pass
    nx = pg.locator('[data-next]')
    if nx.count(): nx.first.click()
    try: pg.wait_for_selector('.kuy [data-ok]', timeout=5000)
    except Exception: pass
    ok(pg.locator('.kuy [data-ok]').count() == 1 and "Uyda sinab" in pg.inner_text('body'), "Savoldan keyin «🏠 Uyda sinab ko'r» kartasi")
    SHOT(pg, 'kashf_uy')
    si0 = X(R, "b.missiya.si"); pg.click('.kuy [data-ok]'); pg.wait_for_timeout(500)
    r = X(R, "[b.kashfUy.length, b.kashfUy[0] && b.kashfUy[0].holat, b.kashfUy[0] && b.kashfUy[0].id, b.missiya.si]")
    ok(r[0] == 1 and r[1] == 'kut' and r[2] == kid and r[3] == si0 + 1, f"«📌 Eslab qoldim» → b.kashfUy da 'kut', missiya keyingi qadamga {r}")
    ok(X(R, "A.readLog(b.id, A.todayKey()).some(e=>e.t==='kashf'&&e.hodisa==='eslab')"), "Log: {t:'kashf', hodisa:'eslab'}")
    X(R, "(A.kashfUyQosh(b, b.kashfUy[0].id), 0)"); ok(X(R, "b.kashfUy.length") == 1, "Bir mavzu ikki marta kutishga qo'shilmaydi")
    # uyda
    X(R, "(b.kashfUy.push({sana: A.addDays(A.todayKey(), -8), id: 'k9', holat: 'kut'}), A.save(true), 0)")
    NAV('uy', 500)
    ok(pg.locator('.kuyc').count() == 1 and pg.locator('[data-kuy]').count() == 1, "Uy ekranida 1 ta «🏠 Uy tajribasi» (8 kunligi ko'rinmaydi)")
    w = W390(); ok(w[0] <= 390 and w[1] <= 390, f"390 px: uy ekrani {w}")
    SHOT(pg, 'uy_tajriba')
    y0 = X(R, "b.yulduz"); pg.click('[data-kuy]'); pg.wait_for_timeout(300)
    ok(pg.locator('.sheet .kuyo [data-v]').count() == 3, "Bajardim → kuzatuv savoli, 3 variant")
    a = X(R, f"(B.kashf.find(k=>k.id==='{kid}').uy.a)")
    pg.locator('.sheet [data-v]').nth(a if a is not None else 0).click(); pg.wait_for_timeout(200)
    ok(pg.locator('.sheet .explain').count() == 1 and pg.locator('.sheet [data-ol]').count() == 1, "Javobdan keyin izoh va «⭐ +2 olish»")
    pg.click('.sheet [data-ol]'); pg.wait_for_timeout(400)
    r = X(R, f"[b.yulduz - {y0}, b.kashfUy[0].holat, b.kashfUy[0].bsana === A.todayKey(), A.readLog(b.id, A.todayKey()).some(e=>e.t==='kashf'&&e.hodisa==='uy')]")
    ok(r == [2, 'bajardi', True, True], f"+2 ⭐, holat 'bajardi', log {{t:'kashf', hodisa:'uy'}} {r}")
    ok(pg.locator('.kuyc').count() == 0, "Bajarilgach kartasi yo'qoladi")
    # sozlama o'chiq
    X(R, "(A.S().sozlama.kashfUy=false, b.kashfUy.push({sana: A.todayKey(), id: 'k3', holat: 'kut'}), A.save(true), 0)")
    NAV('uy', 400); ok(pg.locator('.kuyc').count() == 0, "⚙️ kashfUy o'chiq → uyda karta yo'q")
    missiyaQadam(R, 'kashf'); NAV('missiya', 500); pg.click('[data-go]'); pg.wait_for_timeout(400); ev("window.__bjJavob(true)"); pg.wait_for_timeout(900)
    nx = pg.locator('[data-next]')
    if nx.count(): nx.first.click(); pg.wait_for_timeout(500)
    ok(pg.locator('.kuy [data-ok]').count() == 0, "⚙️ kashfUy o'chiq → missiyada «Uyda sinab ko'r» chiqmaydi")
    X(R, "(A.S().sozlama.kashfUy=true, A.save(true), 0)")
    # 8 ta sahna (ko'rib chiqish uchun)
    NAV('uy', 300)
    ev("""(()=>{const A=BJ.A; document.body.innerHTML='<div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;padding:6px;background:#111">'+['kosmos','osmon','suv','tabiat','hayvon','tana','texnika','yer'].map(k=>'<div class="ksc" style="height:110px;border-radius:10px">'+BJ.art.kashfSahna(k)+'<div class="kkat">'+k+'</div></div>').join('')+'</div>';})()""")
    pg.wait_for_timeout(300); SHOT(pg, 'sahnalar')
    ok(ev("document.querySelectorAll('.ksc svg').length") == 8, "8 ta kategoriya sahnasi chiziladi")
    # viktorina = shu hafta mavzulari
    pg.clock.set_fixed_time(YAKSH); setj(Q)
    r = X(Q, "[A.dayNo(b), A.haftaKashf(b)]")
    exp = [f"k{(d - 1) % 30 + 1}" for d in range(r[0] - 6, r[0])]
    ok(r[1] == exp, f"Viktorina mavzulari: D−6…D−1 → {r[1]}")
    missiyaQadam(Q, 'viktorina', final=True); NAV('missiya', 600)
    ids = []
    for i in range(2):
        ids.append(ev("(window.__bjCur().it||{}).ex && window.__bjCur().it.ex.id")); ev("window.__bjJavob(true)"); pg.wait_for_timeout(1800)
        nx = pg.locator('[data-next]')
        if nx.count(): nx.first.click(); pg.wait_for_timeout(600)
    ok(all(x in r[1] for x in ids if x) and len(set(ids)) == 2, f"Yakshanba viktorinasi savollari shu haftaning mavzularidan: {ids}")
    pg.clock.set_fixed_time(JUMA)

    # ================= 4. 📖 UCH MARTA O'QISH =================
    setj(R); X(R, "(b.missiya=null, A.save(true), 0)"); missiyaQadam(R, 'oqish'); NAV('missiya', 600)
    ok("Uch marta" in pg.inner_text('.top .ttl'), f"Sarlavha: {pg.inner_text('.top .ttl')}")
    s = ev("window.__bjUch().state()")
    ok(s['faza'] == 'kirish' and pg.locator('#ukat').count() == 1 and pg.locator('.uchn i').count() == 3, f"Kirish: matn, «👨 Kattalar tinglaydi», 3 nuqta {s}")
    ok(X(R, f"B.matn.find(m=>m.id==='{s['matn']}').d") == 1, "1-sinf bolasiga d1 matni")
    SHOT(pg, 'uch_kirish')
    n = s['soz']
    pg.click('[data-bosh]'); pg.wait_for_timeout(200)
    ok(ev("window.__bjUch().state().faza") == 'oqish' and pg.locator('#utm').count() == 1, "▶ Boshla → taymer va «✓ O'qib bo'ldim»")
    w = W390(); ok(w[0] <= 390, f"390 px: o'qish ekrani {w}")
    pg.click('[data-tug]'); pg.wait_for_timeout(200)
    ok(ev("window.__bjUch().state().faza") == 'oqish', "Juda tez bosilsa (< 4 s) qabul qilinmaydi")
    ev("window.__bjUch().tugat(30)"); pg.wait_for_timeout(300)
    s = ev("window.__bjUch().state()"); w1 = round(n * 60 / 30)
    ok(s['w'] == [w1] and s['faza'] == 'kirish', f"1-o'qish: {n} so'z / 30 s = {w1} so'z/daq {s}")
    pg.click('[data-bosh]'); pg.wait_for_timeout(150); ev(f"window.__bjUch().tugat({n * 60 / 140})"); pg.wait_for_timeout(300)
    s = ev("window.__bjUch().state()")
    ok(s['faza'] == 'tez' and s['w'] == [w1] and 'Shoshilma' in pg.inner_text('body'), "1-sinfda > 130 so'z/daq → «Shoshilma», o'qish qayta")
    pg.click('[data-qayta]'); pg.wait_for_timeout(150); ev("window.__bjUch().tugat(25)"); pg.wait_for_timeout(300)
    pg.click('[data-bosh]'); pg.wait_for_timeout(150); ev("window.__bjUch().tugat(20)"); pg.wait_for_timeout(500)
    s = ev("window.__bjUch().state()"); ws = [w1, round(n * 60 / 25), round(n * 60 / 20)]; osish = round((ws[2] - ws[0]) * 100 / ws[0])
    ok(s['faza'] == 'natija' and s['w'] == ws and pg.locator('.ubars .ub').count() == 3, f"3 o'qish → natija, 3 ustun {s['w']}")
    ok(pg.inner_text('.uosish').strip() == f'+{osish}%', f"O'sish: {pg.inner_text('.uosish')} (kutilgan +{osish}%)")
    r = X(R, "[b.uch.tarix.length, b.uch.tarix[0].w, b.uch.tarix[0].kat, A.readLog(b.id, A.todayKey()).filter(e=>e.t==='oqish'&&e.tur==='uch').length, b.oqilgan.length]")
    ok(r[0] == 1 and r[1] == ws and r[2] is False and r[3] == 1 and r[4] >= 1, f"b.uch.tarix yozildi, log tur:'uch', matn o'qilganlar ro'yxatida {r}")
    w = W390(); ok(w[0] <= 390, f"390 px: natija {w}")
    SHOT(pg, 'uch_natija')
    pg.click('[data-sav]'); pg.wait_for_timeout(300)
    ok(pg.locator('.uopts [data-o]').count() == 3, "Tushunish savoli: 3 variant")
    tj = X(R, f"(()=>{{const m=B.matn.find(x=>x.id==='{s['matn']}'); return m.s.map(x=>x[1])}})()")
    btns = pg.locator('.uopts [data-o]'); k = next(i for i in range(3) if btns.nth(i).inner_text().strip() in tj)
    si0 = X(R, "b.missiya.si"); btns.nth(k).click(); pg.wait_for_timeout(300)
    ok(pg.locator('.uopts .togri').count() == 1 and X(R, "b.uch.tarix[0].sav") == 1, "To'g'ri javob → yashil, sav = 1")
    pg.click('[data-dav]'); pg.wait_for_timeout(500)
    r = X(R, "[b.missiya.si, (b.missiya.res[b.missiya.si-1]||[]).length]")
    ok(r == [si0 + 1, 1], f"Davom → missiya keyingi qadamga {r}")
    # kattalar tinglaydi
    X(R, "(b.missiya=null, A.save(true), 0)"); missiyaQadam(R, 'oqish'); NAV('missiya', 600)
    s = ev("window.__bjUch().state()"); n = s['soz']; wl0 = X(R, "b.wcpm.length")
    pg.check('#ukat'); pg.click('[data-bosh]'); pg.wait_for_timeout(150); ev("window.__bjUch().tugat(30)"); pg.wait_for_timeout(300)
    ok(ev("window.__bjUch().state().faza") == 'belgi' and pg.locator('[data-saq]').count() == 1, "👨 Kattalar tinglaydi → xato so'zlarni belgilash ekrani")
    ev("window.__bjUch().xatoBos(0)"); ev("window.__bjUch().xatoBos(2)"); pg.click('[data-saq]'); pg.wait_for_timeout(300)
    r = X(R, "[b.uch.kat, b.wcpm.length, b.wcpm[b.wcpm.length-1].wcpm, b.wcpm[b.wcpm.length-1].tur]")
    ok(r == [True, wl0 + 1, round((n - 2) * 60 / 30), 'uch'], f"WCPM = (so'z − 2 xato)·60/30, 1-o'qish b.wcpm ga ham yozildi {r}")
    pg.click('[data-bosh]'); pg.wait_for_timeout(150); ev(f"window.__bjUch().tugat({n * 60 / 300})"); pg.wait_for_timeout(300)
    ok(ev("window.__bjUch().state().faza") == 'belgi', "Kattalar tinglaganda tezlik chegarasi qo'llanmaydi")
    # o'tkazish
    X(R, "(b.missiya=null, A.save(true), 0)"); missiyaQadam(R, 'oqish'); NAV('missiya', 600); si0 = X(R, "b.missiya.si")
    pg.click('[data-skip]'); pg.wait_for_timeout(400)
    ok(X(R, "b.missiya.si") == si0 + 1, "«Bugun o'tkazamiz» → keyingi qadam")
    # 2-sinf chegarasi 170
    setj(Q); pg.clock.set_fixed_time(JUMA); X(Q, "(b.missiya=null, A.save(true), 0)"); missiyaQadam(Q, 'oqish'); NAV('missiya', 600)
    s = ev("window.__bjUch().state()"); n = s['soz']
    ok(X(Q, f"B.matn.find(m=>m.id==='{s['matn']}').d") == 2, "2-sinf bolasiga d2 matni")
    pg.click('[data-bosh]'); pg.wait_for_timeout(150); ev(f"window.__bjUch().tugat({n * 60 / 160})"); pg.wait_for_timeout(300)
    ok(ev("window.__bjUch().state().faza") == 'kirish', "2-sinfda 160 so'z/daq qabul qilinadi (chegara 170)")
    ok(X(K, "A.buildMission(b).steps.some(s=>s.k==='oqish')") is False, "Maktabgacha bolaga o'qish qadami yo'q")

    # ================= 5. OTA-ONA =================
    NAV(f'ota-oqish-{R}', 500, ota=True)
    ok("1-o'qish" in pg.inner_text('body') and pg.locator('svg.chart').count() >= 2 and pg.locator('table.tb tr').count() >= 2, "📖 Ota-ona: 1-o'qish (sovuq) grafigi + kunlik o'sish jadvali")
    ok(pg.locator('#mt').count() == 1, "Eski 1 daqiqalik test ham saqlandi")
    SHOT(pg, 'ota_oqish')
    GO('ota-sozlama'); ok(pg.locator('#ku').count() == 1 and pg.is_checked('#ku'), "⚙️ «🏠 Uyda sinab ko'r» sozlamasi")
    pg.uncheck('#ku'); pg.click('[data-save]'); pg.wait_for_timeout(300)
    ok(ev("BJ.A.S().sozlama.kashfUy") is False, "Saqlanganda kashfUy = false"); ev("BJ.A.S().sozlama.kashfUy=true; BJ.A.save(true)")
    r = X(R, "A.xulosa(b, A.isoWeek()).q.join('\\n')")
    ok('Uy tajribalari: 1 ta bajarildi' in r and "Uch marta o'qish" in r, f"📊 Hafta xulosasida uy tajribalari va uch marta o'qish")
    NAV('ota-arab', 500, ota=True)
    t = pg.inner_text('body')
    ok('/8' in t and 'ra — qalin' in t and 'vaqf belgilari' in t.lower(), "🕌 Arab tasdig'i: 8 bo'lim, TJ.7 va TJ.8 misollari")
    pg.locator('details.tjd summary', has_text='vaqf').click(); pg.wait_for_timeout(200)
    ok("boshqa vaqf belgilari" in pg.inner_text('body'), "TJ.8 tasdig'ida «boshqa belgilar bo'lsa — ayting» eslatmasi")
    SHOT(pg, 'ota_arab')
    # TJ.8 vis va TJ.7 sinov ekrani
    NAV('sinov-TJ.8-3', 500)
    ok(pg.locator('.vqv .vqb').count() >= 1 or pg.locator('[data-o], .opt, .ans button').count() >= 2, "TJ.8 sinov ekrani ochiladi")
    SHOT(pg, 'tj8')
    NAV('sinov-TJ.7-2', 500); SHOT(pg, 'tj7')
    ok(pg.locator('.arab').count() >= 1, "TJ.7 sinov ekrani ochiladi")
    br.close()
finally:
    srv.terminate()
print('\n' + ('HAMMASI O\'TDI ✅' if not ERR else f'XATOLAR: {len(ERR)}'))
for e in ERR: print(' -', e)
sys.exit(1 if ERR else 0)
