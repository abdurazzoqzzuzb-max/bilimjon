"""Bilimjon 0.10.0 — 15.11 tekshiruvi: 🗓 yakshanba finali (bosqich sovg'asi yo'q, oxirida noyob KATTA sovg'a), ⭐ sovg'a bonusi sandiqqa kirmaydi,
🎁 tanlanmay qolgan KATTA sovg'a ertasi kuni ham kutadi. Sana Playwright soati bilan qotiriladi (kunga bog'liq emas).
Ishga tushirish: python3 sinov/v0100/sinov_v0100_kun.py"""
import os, sys, time, subprocess, datetime as dt
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.abspath(os.path.join(D, '..', '..'))
PORT = 8819; URL = f'http://localhost:{PORT}/'
srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT)], cwd=SITE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
ERR = []; PE = []
def ok(c, m): print(('✅ ' if c else '❌ ') + m); (None if c else ERR.append(m))
def ochil(br, vaqt):
    ctx = br.new_context(viewport={'width': 390, 'height': 844}, service_workers='block')
    ctx.clock.install(time=vaqt)
    P = ctx.new_page(); P.on('pageerror', lambda e: PE.append(str(e)))
    P.goto(URL + '?tez=1'); P.wait_for_timeout(400)
    P.fill('#on', 'Sinov oila'); P.fill('#p1', '1234'); P.fill('#p2', '1234'); P.click('#go'); P.wait_for_timeout(300)
    bid = P.evaluate("""(()=>{const A=BJ.A; const b=A.newBola({laqab:'Qiz',daraja:'g2',avatar:'🦄',dunyo:'orol'}); b.boshlandi=A.addDays(A.todayKey(),-20);
      A.S().sozlama.uyqu=''; A.S().joriy=b.id; A.svSinov=1; A.save(true); return b.id})()""")
    X = lambda e: P.evaluate(f"(()=>{{const A=BJ.A, V=A.sv, b=A.S().bolalar['{bid}']; return {e}}})()")
    return ctx, P, X
try:
  with sync_playwright() as p:
    br = p.chromium.launch()
    # ================= 1. YAKSHANBA =================
    ctx, P, X = ochil(br, dt.datetime(2026, 11, 15, 10, 0))
    ok(X("A.isSunday()") is True, "Soat qotirildi: 15.11.2026 — yakshanba")
    r = X("(()=>{const m=b.missiya=A.buildMission(b); A.save(true); return {f:!!m.final, k:m.steps.map(s=>s.k)}})()")
    ok(r['f'] and r['k'][0].startswith('final'), f"Yakshanba: missiya — final ({', '.join(r['k'])})")
    r = X("""(()=>{const m=b.missiya, tot=m.steps.reduce((s,x)=>s+(x.n||1),0); let c=0,i=0; while(i<m.steps.length && c*3<2*tot){c+=m.steps[i].n||1;i++;}
      if(m.steps[i]&&m.steps[i].k==='yakun') i--; for(let j=0;j<i;j++) m.res[j]=Array(m.steps[j].n||1).fill({ok:1,ms:1}); m.si=i; m.cur=null; A.save(true); return V.bosqich(b,m)})()""")
    P.evaluate("location.hash='missiya'"); P.wait_for_timeout(800)
    ok(r is False and P.locator('.sheet .svk').count() == 0, "Finalda yo'l-yo'lakay bosqich sovg'asi chiqmaydi (kod shunday: final — bitta noyob sovg'a)")
    r = X("(()=>{b.missiya.done=true; A.agg(b).missiya=1; A.save(true); return V.kutilgan(b).map(o=>[o.kalit,o.d])})()")
    ok(any(k.endswith(':k') and d == 3 for k, d in r), f"Final tugadi → KATTA sovg'a NOYOB darajada (d=3): {r}")
    P.evaluate("location.hash='natija'"); P.wait_for_timeout(1800)
    ok(P.locator('.sheet .svk').count() == 3 and 'finali' in P.locator('.sheet').inner_text(), "Natija ekranida: «🏆 Yakshanba finali — KATTA sovg'a!» + 3 karta")
    ctx.close()

    # ================= 2. ⭐ SOVG'A BONUSI =================
    ctx, P, X = ochil(br, dt.datetime(2026, 11, 16, 10, 0))
    r = X("""(()=>{b.yulduz=50; const y0=b.yulduz, w0=A.weekStars(b), s0=V.yul(b); V.olish(b,'2026-11-16:1','x_yul2','bosqich'); V.olish(b,'2026-11-16:2','x_tun','bosqich');
      return {y:b.yulduz-y0, w:A.weekStars(b)-w0, s:V.yul(b)-s0, bonus:b.sv.bonus}})()""")
    ok(r['y'] == 0 and r['w'] == 0 and r['s'] == 35 and r['bonus'] == 35, f"Sovg'a ⭐ (+20 va +15): do'kon uchun +{r['s']}, haftalik yulduz/sandiq +{r['w']}, b.yulduz +{r['y']}")
    r = X("(()=>{const k=V.KAT[V.K.find(x=>x.t==='oyin'&&x.d===1).id]; const n0=V.yul(b); V.sotib(b,k.id); return {n0, ok:!!document.querySelector('.sheet [data-ok]')}})()")
    if r['ok']: P.click('.sheet [data-ok]'); P.wait_for_timeout(300)
    r2 = X("({y:V.yul(b), sarf:b.sv.sarf, yul:b.yulduz})")
    ok(r['ok'] and r2['y'] == r['n0'] - 25 and r2['yul'] == 50, f"Bonus ⭐ bilan do'kondan xarid: {r['n0']} → {r2['y']} (b.yulduz {r2['yul']} o'zgarmadi)")
    ok("nom: `+${d * 10} ⭐ do'kon uchun`" in open(os.path.join(SITE, 'index.html'), encoding='utf-8').read(), "Sovg'a nomi: «+20 ⭐ do'kon uchun» (yulduz sandiqqa emas)")
    ctx.close()

    # ================= 3. KATTA SOVG'A ERTASIGA QOLADI =================
    ctx, P, X = ochil(br, dt.datetime(2026, 11, 16, 21, 50))
    X("(()=>{const m=b.missiya=A.buildMission(b); m.done=true; A.agg(b).missiya=1; A.save(true); return V.kutilgan(b).length})()")
    k0 = X("V.kutilgan(b).map(o=>o.kalit)")
    ok('2026-11-16:k' in k0 and X("b.sv.kk && b.sv.kk.k") == '2026-11-16:k', f"Kechqurun missiya tugadi, sovg'a tanlanmadi: {k0}")
    P.clock.set_system_time(dt.datetime(2026, 11, 17, 9, 0)); P.wait_for_timeout(100)
    k1 = X("(()=>{b.missiya=A.buildMission(b); A.save(true); return V.kutilgan(b).map(o=>[o.kalit,o.d])})()")
    ok(['2026-11-16:k', 2] in k1, f"Ertasi kuni (yangi missiya ochilgan) — kechagi KATTA sovg'a hali kutyapti: {k1}")
    P.evaluate("location.hash='x'"); P.wait_for_timeout(50); P.evaluate("location.hash='uy'"); P.wait_for_timeout(600)
    ok(P.locator('.svh .svt.hot, [data-svkut], .svt.hot').count() >= 1, "Uy ekranida 🎁 belgisi yonadi")
    X("(()=>{const ids=V.tanlov(b,'2026-11-16:k',2); V.olish(b,'2026-11-16:k',ids[0].id,'missiya'); return 1})()")
    ok(X("V.kutilgan(b).length") == 0, "Olingach — boshqa chiqmaydi")
    P.clock.set_system_time(dt.datetime(2026, 11, 20, 9, 0)); P.wait_for_timeout(50)
    X("(()=>{b.sv.kk={k:'2026-11-16:k',f:0}; delete b.sv.ol['2026-11-16:k']; return 1})()")
    ok(X("V.kutilgan(b).length") == 0, "3+ kun o'tgan tanlanmagan sovg'a — endi chiqmaydi (2 kun chegarasi)")
    ctx.close()
    ok(not PE, f"JS xatolari yo'q ({PE[:2]})")
    br.close()
finally:
    srv.terminate()
print(f"\nNATIJA: {'HAMMASI OK' if not ERR else str(len(ERR)) + ' XATO'}")
sys.exit(1 if ERR else 0)
