"""Bilimjon 0.7.0 — 1b-bosqich: 🎬 rasmli kichik dars («kino»).
Tekshiruv: har M-tugun generatorida kino xatosiz quriladi va oxirgi sahna javobni to'g'ri ko'rsatadi; 2 xato → rasmli dars →
sahnalar o'zi oqadi → «Endi o'zim yechaman» → egizak; egizakda 1-xato → mini-kino (javobsiz); matnli yechim yig'ma bo'limda; 390 px.
Ishga tushirish: python3 sinov/v070/sinov_bosqich1b.py  (skrinshotlar: /tmp/bj070_1b_*.png)"""
import os, sys, time, subprocess
from playwright.sync_api import sync_playwright

D = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.abspath(os.path.join(D, '..', '..'))
PORT = 8777; URL = f'http://localhost:{PORT}/'
srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT)], cwd=SITE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
ERR = []
def ok(c, m):
    print(('✅ ' if c else '❌ ') + m)
    if not c: ERR.append(m)
NV = [0]
try:
  with sync_playwright() as p:
    br = p.chromium.launch(); ctx = br.new_context(viewport={'width': 390, 'height': 844}, service_workers='block'); pg = ctx.new_page()
    pg.on('pageerror', lambda e: ERR.append(f'pageerror: {e}')); ev = pg.evaluate
    def NAV(h, ms=500):
        NV[0] += 1; pg.goto(URL + f'?tez=1&r={NV[0]}#' + h); ev('BJ.A.render()'); pg.wait_for_timeout(ms)
    pg.goto(URL + '?tez=1'); pg.wait_for_timeout(400)
    pg.fill('#on', 'Sinov'); pg.fill('#p1', '1234'); pg.fill('#p2', '1234'); pg.click('#go'); pg.wait_for_timeout(300)
    K, Q = ev("""(()=>{const A=BJ.A; const k=A.newBola({laqab:'Kichik',daraja:'g0',avatar:'🐯',dunyo:'garaj'}); const q=A.newBola({laqab:'Katta',daraja:'g2',avatar:'🦄',dunyo:'orol'});
      A.S().sozlama.uyqu=''; A.S().joriy=k.id; A.save(true); return [k.id,q.id]})()""")
    setj = lambda bid: ev(f"(()=>{{const s=BJ.A.S(); s.joriy='{bid}'; BJ.A.save(true)}})()")

    # ---- generator bo'yicha mulk sinovi: kino xatosiz, oxirgi sahna = javob
    r = ev(f"""(()=>{{const A=BJ.A, b=A.S().bolalar['{K}'], reg=BJ.gen.reg, out={{n:0,kino:0,xato:[],tur:{{}}}};
      Object.keys(reg).filter(id=>/^M[0-2]\\./.test(id)).forEach(id=>{{ for (let q=1;q<=3;q++) for (let i=0;i<25;i++) {{ let it; try {{ it=A.makeItem(b,{{tugun:id,q,tur:'missiya'}}); }} catch(e) {{ continue; }}
        out.n++; let sc; try {{ sc=A.kino(b,it); }} catch(e) {{ out.xato.push(id+' throw '+e.message); continue; }} if (!sc) continue; out.kino++; out.tur[id]=(out.tur[id]||0)+1;
        const L=sc[sc.length-1], f=String(L.f||'').replace(/<[^>]+>/g,''), a=String(it.a);
        if (id!=='M0.5' && !(f===a || f.endsWith('= '+a) || f.endsWith('= '+a) || f.replace(/\\s/g,'')===a || L.cap.indexOf(a)>=0)) out.xato.push(id+' q'+q+': «'+it.sav+'» a='+a+' f='+f+' cap='+L.cap);
        if (sc.some(s=>!s.cap)) out.xato.push(id+' bo\\'sh yozuv');
        const nob=sc.reduce((m,s)=>Math.max(m,(s.gr||[]).reduce((x,g)=>x+g.length,0)),0); if (nob>40) out.xato.push(id+' juda ko\\'p narsa '+nob);
      }} }}); out.xato=out.xato.slice(0,8); return out}})()""")
    ok(not r['xato'], f"M-tugunlar: {r['n']} topshiriq, {r['kino']} tasida kino; xatolar: {r['xato']}")
    kt = sorted(r['tur'].keys()); print('   kino bor tugunlar:', ' '.join(kt))
    for need in ['M0.3', 'M0.9', 'M0.10', 'M1.1', 'M1.2', 'M2.1', 'M2.2', 'M2.4']:
        ok(need in r['tur'], f"{need} uchun rasmli dars bor")
    # ---- maxsus holatlar
    r = ev("""(()=>{const A=BJ.A, b={dunyo:'garaj'}; const q=A.kino(b,{tugun:'M1.1',ex:{a:7,b:5,op:'+'},a:12,sav:'7 + 5 = ?'}), x=A.kino(b,{tugun:'M2.2',ex:{a:38,b:25,op:'+'},a:63,sav:'38 + 25'}),
      y=A.kino(b,{tugun:'M2.2',ex:{a:52,b:27,op:'−'},a:25,sav:'52 − 27'}), t=A.kino(b,{tugun:'M1.2',a:14,sav:'14 da nechta o\\'nlik?'}), z=A.kino(b,{tugun:'M1.1',ex:{a:9,b:4,op:'+',yoq:'b'},a:4,sav:'9 + □ = 13'}),
      bus=A.kino(b,{tugun:'M2.4',ex:{f:9},a:9,sav:"Avtobusda 8 kishi bor edi. 3 kishi tushdi, 4 kishi chiqdi. Nechta?"});
      return {q:[q.length,q[2].f], x:[x.length, x.some(s=>/10 tasi → 1 o'nlik/.test(s.cap)), x[x.length-1].f], y:[y.some(s=>/maydalaymiz/.test(s.cap)), y[y.length-1].f], t:[t.length, t[2].f.replace(/<[^>]+>/g,'')], z:[z.length, z[2].f], bus:[bus.length, bus[3].f]}})()""")
    ok(r['q'] == [3, '7 + 5 = 12'], f"7 + 5: 3 sahna (bor edi → keldi → hammasi) {r['q']}")
    ok(r['x'] == [4, True, '38 + 25 = 63'], f"38 + 25: o'tishli — «10 birlik → 1 o'nlik» sahnasi {r['x']}")
    ok(r['y'] == [True, '52 − 27 = 25'], f"52 − 27: «1 o'nlikni maydalaymiz» sahnasi {r['y']}")
    ok(r['t'] == [3, '14 = 10 + 4'], f"14 = 1 bog'lam + 4 kubik, raqam ranglari bilan {r['t']}")
    ok(r['z'] == [3, '□ = 4'], f"9 + □ = 13: yashiringan son {r['z']}")
    ok(r['bus'] == [4, '8 − 3 + 4 = 9'], f"Avtobus masalasi: 4 sahna {r['bus']}")

    # ---- oqim: 2 xato → rasmli dars
    # M2.2 q2 ba'zan «Qaysi misolning javobi N?» turini beradi — unda kino yo'q (oddiy dars). Kinoli savol chiqquncha qayta ochiladi (07.11: sinov tasodifan yiqilardi)
    setj(Q)
    for _ in range(15):
        NAV('sinov-M2.2-2', 500)
        if ev("!!BJ.A.kino(BJ.A.bola(), window.__bjCur().it)"): break
    ev("window.__bjCur().cb({togri:false, javob:'1'})"); pg.wait_for_timeout(300)
    ok(pg.locator('#fb .hint').count() == 1 and pg.locator('.kino').count() == 0, "1-xato: oddiy maslahat (kino yo'q)")
    ev("window.__bjCur().cb({togri:false, javob:'2'})"); pg.wait_for_timeout(500)
    ok(pg.locator('.kinod').count() == 1 and pg.locator('.kino').count() == 1, "2-xato: 🎬 rasmli dars ochildi")
    ok(pg.locator('details.dmatn').count() == 1 and not ev("document.querySelector('details.dmatn').open"), "Matnli yechim kattalar uchun yig'ma bo'limda (yopiq)")
    pg.wait_for_timeout(1200)
    ok(ev("document.querySelector('[data-twin]').disabled") is False, "Sahnalar tugagach «Endi o'zim yechaman» ochiladi")
    ok('kyash' not in ev("document.querySelector('[data-dans]').className"), "Oxirida javob ko'rinadi")
    ok(ev("document.querySelector('.kfor').classList.contains('top')"), "Oxirgi sahnada katta yashil formula")
    sw = ev("document.documentElement.scrollWidth"); ok(sw <= 390, f"390 px ichida ({sw})")
    pg.screenshot(path='/tmp/bj070_1b_dars.png', full_page=True)
    ok(ev("(()=>{document.querySelector('[data-krep]').click(); return document.querySelector('[data-kd=\"0\"]').className})()") == 'on', "⏮ — kino boshidan")
    ok(ev("BJ.A.readLog(BJ.A.S().joriy, BJ.A.todayKey()).some(e=>e.t==='kino')"), "Log: {t:'kino'}")
    pg.locator('[data-twin]').click(); pg.wait_for_timeout(400)
    ok(ev("window.__bjCur().it.tur") == 'dars', "Egizak savol chiqdi (tur: dars)")
    kbor = ev("!!BJ.A.kino(BJ.A.bola(), window.__bjCur().it)")
    ev("window.__bjCur().cb({togri:false, javob:'1'})"); pg.wait_for_timeout(500)
    ok(pg.locator('#fb .kino.mini').count() == (1 if kbor else 0) and pg.locator('#fb .hint').count() == 1, f"Egizakda 1-xato → {'mini-kino (o`sha sonlar bilan)' if kbor else 'oddiy maslahat (bu turdagi egizakda kino yo`q)'}")
    ok(not ev("document.querySelector('#fb .kfor.top')"), "Mini-kino javobni oshkor qilmaydi (oxirgi sahnasiz)")
    pg.screenshot(path='/tmp/bj070_1b_mini.png', full_page=True)

    # ---- maktabgacha: qo'shish
    setj(K); NAV('sinov-M0.9-1', 500)
    ev("window.__bjCur().cb({togri:false, javob:'1'})"); pg.wait_for_timeout(200); ev("window.__bjCur().cb({togri:false, javob:'2'})"); pg.wait_for_timeout(1500)
    ok(pg.locator('.kinod').count() == 1, "Maktabgacha (M0.9): rasmli dars")
    ok(pg.locator('.kinod .dkat').count() == 0, "«Kattalar o'qib bersin» yozuvi yo'q — bola o'zi ko'radi")
    pg.screenshot(path='/tmp/bj070_1b_g0.png', full_page=True)
    # ---- kino bo'lmagan fan — eski matnli dars ishlaydi
    NAV('sinov-H0.1-1-top', 500)
    for i in range(2): ev("window.__bjCur().cb({togri:false, javob:'zz'})"); pg.wait_for_timeout(300)
    ok(pg.locator('.dars').count() == 1, "Matematika bo'lmagan savolda eski dars o'zgarmadi")
    ok(not [e for e in ERR if e.startswith('pageerror')], "Sahifada JS xatosi yo'q")
finally:
    srv.kill()
print(f"\n{'XATO: ' + str(len(ERR)) if ERR else 'HAMMASI OʻTDI'}")
sys.exit(1 if ERR else 0)
