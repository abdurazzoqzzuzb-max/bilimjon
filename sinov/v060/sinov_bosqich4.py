"""Bilimjon 0.6.0 — 4-bosqich: 🔤 harf mashqlari xilma-xilligi (6 format, qiyinlashish, yangi harf tezroq, oraliq takror, bilgan harflari testi).
Ishga tushirish: python3 sinov/v060/sinov_bosqich4.py  (skrinshotlar: /tmp/bj060_4_*.png)"""
import os, sys, time, subprocess
from playwright.sync_api import sync_playwright

D = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.abspath(os.path.join(D, '..', '..'))
PORT = 8774; URL = f'http://localhost:{PORT}/'
srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT)], cwd=SITE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
ERR = []
def ok(c, m):
    print(('✅ ' if c else '❌ ') + m)
    if not c: ERR.append(m)
NV = [0]
def NAV(pg, h, ms=400):
    NV[0] += 1; pg.goto(URL + f'?tez=1&r={NV[0]}#' + h); pg.evaluate('BJ.A.render()'); pg.wait_for_timeout(ms)
SHOT = lambda pg, n: pg.screenshot(path=f'/tmp/bj060_4_{n}.png', full_page=True)

with sync_playwright() as p:
    br = p.chromium.launch(); ctx = br.new_context(viewport={'width': 390, 'height': 844}, service_workers='block'); pg = ctx.new_page()
    pg.on('pageerror', lambda e: ERR.append(f'pageerror: {e}')); ev = pg.evaluate
    pg.goto(URL + '?tez=1'); pg.wait_for_timeout(400)
    pg.fill('#on', 'Sinov'); pg.fill('#p1', '1234'); pg.fill('#p2', '1234'); pg.click('#go'); pg.wait_for_timeout(300)
    K = ev("""(()=>{const A=BJ.A; const k=A.newBola({laqab:'Kichik',daraja:'g0',avatar:'🐯',dunyo:'garaj'}); k.harfK=8; A.S().sozlama.uyqu=''; A.S().joriy=k.id; A.save(true); return k.id})()""")
    # ---- generator: 6 format × 3 qiyinlik × har xil harflar — hammasi yaroqli
    r = ev("""(()=>{const g=BJ.gen, T=BJ.harfTartib, out={bad:[],n:0,fmt:{},nopt:{}}; const node=h=>BJ.uz.UNLI.includes(h)?'H0.1':['m','n','l','s','t'].includes(h)?'H0.2':'H0.5';
      for (const f of BJ.uz.HFMT) for (const q of [1,2,3]) for (const h of T) for (let k=0;k<4;k++) { const ctx={harflar:T.slice(0,12),harf:h,fmt:f};
        const it=g.make(node(h),q,ctx); out.n++; const v=g.valid(it); if (v!==true) out.bad.push([f,q,h,v]); if (it.harf!==h) out.bad.push([f,q,h,'harf '+it.harf]);
        out.fmt[it.fmt]=(out.fmt[it.fmt]||0)+1; if (it.fmt==='top'&&f==='top') out.nopt[q]=it.o.length; }
      return out})()""")
    ok(not r['bad'] and r['n'] > 2000, f"{r['n']} ta topshiriq (6 format × 3 qiyinlik × 30 harf) — hammasi yaroqli {r['bad'][:5]}")
    ok(all(r['fmt'].get(f, 0) > 50 for f in ['top', 'tovush', 'ovchi', 'boshqa', 'juft', 'nechta']), f"Hamma 6 format chiqadi {r['fmt']}")
    ok(r['nopt'] == {'1': 3, '2': 4, '3': 6}, f"Qiyinlashish: 3 → 4 → 6 variant {r['nopt']}")
    r = ev("""(()=>{const g=BJ.gen, out={}; const it2=g.make('H0.5',2,{harflar:BJ.harfTartib,harf:'b',fmt:'top'}), it3=g.make('H0.5',3,{harflar:BJ.harfTartib,harf:'b',fmt:'top'}), it1=g.make('H0.5',1,{harflar:BJ.harfTartib,harf:'b',fmt:'top'});
      out.sim2=it2.o.filter(o=>['d','p'].includes(o.v)).length; out.sim3=it3.o.filter(o=>['d','p'].includes(o.v)).length; out.sim1=it1.o.filter(o=>['d','p'].includes(o.v)).length;
      out.st3=it3.o.every(o=>/color/.test(o.st)&&/rotate/.test(o.st)); out.st1=it1.o.every(o=>!o.st);
      const ov=g.make('H0.1',3,{harflar:BJ.harfTartib,harf:'a',fmt:'ovchi'}); out.ov=[ov.cells.length, ov.nT, ov.cells.filter(x=>x.v==='a').length, ov.cells.some(x=>x.v==='a'&&x.h==='a'), ov.cells.some(x=>x.v==='a'&&x.h==='A')];
      const bo=g.make('H0.5',2,{harflar:BJ.harfTartib,harf:'b',fmt:'boshqa'}); out.bo=[bo.o.length, ['D','P'].includes(bo.o[+bo.a].h)];
      return out})()""")
    ok(r['sim1'] == 0 and r['sim2'] == 1 and r['sim3'] == 2, f"O'xshash harflar: q1 — 0, q2 — 1, q3 — 2 (b → d, p) {r}")
    ok(r['st3'] and r['st1'], "q3 — har xil rang + shrift + burilish; q1 — oddiy ko'rinish")
    ok(r['ov'][0] == 16 and r['ov'][1] == r['ov'][2] and r['ov'][3] and r['ov'][4], f"Harf ovchisi q3: 4×4, katta va kichik «A» aralash {r['ov']}")
    ok(r['bo'][0] == 6 and r['bo'][1], f"Boshqachasi q2: 6 harf, bittasi o'xshash harf (b orasida d/p) {r['bo']}")
    # ---- pickLetters: ketma-ket bir xil harf ham, bir xil format ham chiqmaydi
    r = ev(f"""(()=>{{const A=BJ.A, b=A.S().bolalar['{K}']; let pr=null, rep=0, frep=0, f={{}}, h={{}};
      for (let i=0;i<400;i++) {{ const s=A.pickLetters(b); if (!s.fmt) continue; if (pr&&pr.harf===s.harf) rep++; if (pr&&pr.fmt===s.fmt) frep++; f[s.fmt]=1; h[s.harf]=(h[s.harf]||0)+1; pr=s; }}
      return [rep, frep, Object.keys(f).length, h]}})()""")
    ok(r[0] == 0 and r[1] == 0 and r[2] >= 4, f"400 tanlov: ketma-ket bir xil harf {r[0]}, bir xil format {r[1]}, formatlar {r[2]} xil")
    # ---- zaif eski harf ko'proq, bilgani kamroq (oraliq takror)
    r = ev(f"""(()=>{{const A=BJ.A, b=A.S().bolalar['{K}'], T=A.todayKey(); const K=A.knownLetters(b); b.harfSt={{}};
      K.forEach(h=>b.harfSt[h]={{n:10,ok:10,o:[1,1,1,1,1,1,1,1,1,1],iv:8,due:A.addDays(T,5)}}); b.harfSt['m']={{n:10,ok:4,o:[0,1,0,1,0,0,1,0,1,0],iv:1,due:T}};
      const c={{}}; b.harfOxirgi=null; for (let i=0;i<600;i++) {{ const h=A.harfTanla(b,K); c[h]=(c[h]||0)+1; b.harfOxirgi=null; }} return [c, K.slice(-2)]}})()""")
    eski = {k: v for k, v in r[0].items() if k not in r[1] and k != 'm'}
    ok(r[0].get('m', 0) > 120 and sum(eski.values()) == 0, f"Eski harflardan faqat zaifi (m) va eng yangi 2 tasi chiqadi; yaxshi bilganlari — vaqti kelguncha yo'q {r[0]}")
    r = ev(f"""(()=>{{const A=BJ.A, b=A.S().bolalar['{K}'], T=A.todayKey(); b.harfSt['o']={{n:3,ok:3,o:[1,1,1],iv:2,due:T}};
      A.letterProgress(b,{{harf:'o'}},true); const a=[b.harfSt.o.iv, b.harfSt.o.due===A.addDays(T,4)]; A.letterProgress(b,{{harf:'o'}},true); a.push(b.harfSt.o.iv);
      A.letterProgress(b,{{harf:'o'}},false); a.push(b.harfSt.o.iv, b.harfSt.o.due===A.addDays(T,1)); return a}})()""")
    ok(r == [4, True, 4, 1, True], f"Oraliq takror: to'g'ri (vaqti kelganda) → 2→4 kun, shu kuni yana to'g'ri — o'zgarmaydi, xato → ertaga {r}")
    # ---- yangi harf: kuniga 2 tagacha
    r = ev(f"""(()=>{{const A=BJ.A, b=A.S().bolalar['{K}']; b.harfK=5; b.harfKun=null; b.harfKunN=0; const T=BJ.harfTartib, got=[];
      for (let k=0;k<4;k++) {{ const nw=T[b.harfK-1]; for (let i=0;i<3;i++) {{ const r=A.letterProgress(b,{{harf:nw}},true); if (r) got.push(r); }} }} return [got, b.harfK]}})()""")
    ok(len(r[0]) == 2 and r[1] == 7, f"Yangi harf tezroq ochiladi, lekin kuniga ko'pi bilan 2 ta {r}")
    # ---- UI: har formatni 390 px da ko'rish va bosish
    ev(f"(()=>{{const b=BJ.A.S().bolalar['{K}']; b.harfK=12; BJ.A.save(true)}})()")
    for f, q in [('top', 3), ('boshqa', 3), ('juft', 2), ('nechta', 3), ('tovush', 2)]:
        NAV(pg, f'sinov-H0.1-{q}-{f}', 400)
        it = ev("(()=>{const c=window.__bjCur().it; return {fmt:c.fmt,a:c.a,n:c.o.length,t:c.t}})()")
        ok(it['fmt'] == f and pg.locator('.opt').count() == it['n'], f"Ekranda «{f}» q{q}: {it['n']} variant")
        ok(ev("document.documentElement.scrollWidth") <= 390, f"«{f}» 390 px da sig'adi"); SHOT(pg, f)
        pg.locator(f'.opt[data-v="{it["a"]}"]').first.click(); pg.wait_for_timeout(500)
        ok(pg.locator('.opt.ok').count() == 1, f"«{f}»: to'g'ri javob qabul qilindi")
    NAV(pg, 'sinov-H0.1-3-ovchi', 400)
    it = ev("(()=>{const c=window.__bjCur().it; return {a:c.a,cells:c.cells.map(x=>x.v),nT:c.nT,t:c.t}})()")
    ok(it['t'] == 'ovchi' and pg.locator('.ovc').count() == 16, "🔍 Harf ovchisi: 4×4 panjara"); SHOT(pg, 'ovchi')
    ok(ev("document.documentElement.scrollWidth") <= 390, "Ovchi 390 px da sig'adi")
    wrong = [i for i, v in enumerate(it['cells']) if v != it['a']][0]
    pg.locator(f'.ovc[data-i="{wrong}"]').click(); pg.wait_for_timeout(150)
    for i, v in enumerate(it['cells']):
        if v == it['a']: pg.locator(f'.ovc[data-i="{i}"]').click(); pg.wait_for_timeout(80)
    nok = pg.locator('.ovc.ok').count(); pg.wait_for_timeout(300); r = ev("(()=>{const r=window.__bjCur().sinovNatija; return r?{togri:r.togri,xato_soni:r.xato_soni,xato_turi:r.xato_turi}:null})()")
    ok(r and r['togri'] and r['xato_soni'] == 1 and nok == it['nT'], f"Ovchi: hammasi topildi, 1 xato — baribir to'g'ri hisoblanadi {r} {nok}/{it['nT']}")
    # ---- kichik dars egizagi o'sha harf va formatda
    r = ev(f"""(()=>{{const A=BJ.A, b=A.S().bolalar['{K}']; const it=A.makeItem(b,{{tugun:'H0.5',q:2,harf:'b',fmt:'juft'}}); const tw=A.makeItem(b,{{tugun:it.tugun,q:1,tur:'dars',harf:it.harf,fmt:it.fmt}}); return [it.fmt,it.harf,tw.fmt,tw.harf]}})()""")
    ok(r == ['juft', 'b', 'juft', 'b'], f"Dars egizagi — o'sha harf, o'sha format {r}")
    # ---- missiya ichida: til bloki savollari xilma-xil
    r = ev(f"""(()=>{{const A=BJ.A, b=A.S().bolalar['{K}']; const f={{}}; let s=0; for (let i=0;i<300;i++) {{ const sel=A.pickNode(b,'til',{{i}}); if (!sel.fmt) continue; s++; const it=A.makeItem(b,sel); f[it.fmt]=(f[it.fmt]||0)+1; if (BJ.gen.valid(it)!==true) return 'yaroqsiz '+it.fmt; }} return f}})()""")
    ok(isinstance(r, dict) and len(r) >= 5 and max(r.values()) < 0.4 * sum(r.values()), f"Maktabgacha til blokida harf savollari 5–6 formatda, birortasi 40% dan oshmaydi {r}")
    # ---- 🔤 bilgan harflari testi (ota-ona)
    ev(f"(()=>{{const b=BJ.A.S().bolalar['{K}']; b.harfK=2; BJ.A.otaOk={{rol:'admin',t:Date.now()}}; BJ.A.save(true)}})()")
    NAV(pg, f'ota-bola-{K}', 200); ev("BJ.A.otaOk={rol:'admin',t:Date.now()}; BJ.A.render()"); pg.wait_for_timeout(300)
    ok(pg.locator(f'[data-go="ota-harf-{K}"]').count() == 1, "Bola sahifasida «🔤 Bilgan harflari testi» tugmasi")
    pg.click(f'[data-go="ota-harf-{K}"]'); pg.wait_for_timeout(300)
    ok(pg.locator('.htl').count() == 1, "Test ekrani: katta harf, ✅ / ❌"); SHOT(pg, 'harftest')
    for _ in range(5): pg.click('[data-ha]'); pg.wait_for_timeout(60)
    pg.click('[data-yoq]'); pg.wait_for_timeout(60); pg.click('[data-ha]'); pg.wait_for_timeout(60); pg.click('[data-yoq]'); pg.wait_for_timeout(60); pg.click('[data-yoq]'); pg.wait_for_timeout(200)
    ok(pg.locator('[data-sv]').count() == 1 and '7' in pg.inner_text('[data-sv]'), "Natija: birinchi ❌ gacha 2+5 = 7 ta harf")
    pg.click('[data-sv]'); pg.wait_for_timeout(300)
    r = ev(f"(()=>{{const b=BJ.A.S().bolalar['{K}']; return [b.harfK, Object.keys(b.harfSt).length>=5, BJ.A.readLog('{K}',BJ.A.todayKey()).some(e=>e.t==='harfTest')]}})()")
    ok(r[0] == 7 and r[1] and r[2], f"Saqlandi: harfK=7, yangi harflar takrorga qo'shildi, log {r}")
    ok(not [e for e in ERR if e.startswith('pageerror')], 'Sahifada JS xatosi yo\'q')
    br.close()
srv.terminate()
print(f"\n{'XATO: ' + str(len(ERR)) if ERR else 'HAMMASI OK'}"); sys.exit(1 if ERR else 0)
