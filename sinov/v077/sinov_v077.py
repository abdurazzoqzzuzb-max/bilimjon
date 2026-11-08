"""Bilimjon 0.7.7 — masala savollarida ortiqcha «📄 Matn 1» oynasi chiqmasligi (it.matn = 1 — faqat «masala» belgisi; o'qish matni — satr).
Topildi: 08.11, yo'riqnoma uchun ekran rasmlarida. + imlo: do'konda «oyang» → «oying» (u telefondan ko'rsatdi). Ishga tushirish: python3 sinov/v077/sinov_v077.py"""
import os, sys, time, subprocess
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.abspath(os.path.join(D, '..', '..'))
PORT = 8812; URL = f'http://localhost:{PORT}/'
srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT)], cwd=SITE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
ERR = []; PE = []
def ok(c, m): print(('✅ ' if c else '❌ ') + m); (None if c else ERR.append(m))
try:
  with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(viewport={'width': 390, 'height': 844}); pg.on('pageerror', lambda e: PE.append(str(e))); ev = pg.evaluate
    pg.goto(URL + '?tez=1'); pg.wait_for_timeout(400)
    pg.fill('#on', 'Sinov'); pg.fill('#p1', '1234'); pg.fill('#p2', '1234'); pg.click('#go'); pg.wait_for_timeout(300)
    ev("(()=>{const A=BJ.A; const b=A.newBola({laqab:'Sinov',daraja:'g1',avatar:'🐯',dunyo:'garaj'}); A.S().sozlama.uyqu=''; A.S().joriy=b.id; A.save(true)})()")
    r = ev("""(()=>{const A=BJ.A, G=BJ.gen, b=A.bola(), bir={}, satr={}; let bad=[];
      Object.keys(G.reg).forEach(id=>{ for (let q=1;q<=3;q++) for (let i=0;i<25;i++) { let it; try { it=G.make(id,q,{dunyo:'garaj',harflar:[],oldin:[]}); } catch(e) { continue; }
        if (!it) continue; const h=A.headHTML(b,it);
        if (it.matn===1) { bir[id]=(bir[id]||0)+1; if (h.indexOf('class="matn"')>=0) bad.push(id); }
        if (typeof it.matn==='string' && it.matn) { satr[id]=(satr[id]||0)+1; if (h.indexOf('class="matn"')<0 || h.indexOf('<p>1</p>')>=0) bad.push('s:'+id); } } });
      return {bir:Object.keys(bir), satr:Object.keys(satr), bad:[...new Set(bad)]}})()""")
    ok(len(r['bir']) >= 3 and not [x for x in r['bad'] if not x.startswith('s:')], f"«masala» belgili savollar ({', '.join(r['bir'])}) — «📄 Matn» oynasi YO'Q")
    ok(len(r['satr']) >= 1 and not [x for x in r['bad'] if x.startswith('s:')], f"o'qish matni bor savollar ({', '.join(r['satr'])}) — matn oynasi joyida")
    t = r['bir'][0]; topildi = False
    for i in range(30):
        pg.goto(URL + f'?tez=1&r={i}#sinov-{t}-1'); ev('BJ.A.render()'); pg.wait_for_timeout(150)
        if ev("!!(window.__bjCur && __bjCur() && __bjCur().it && __bjCur().it.matn===1)"): topildi = True; break
    ok(topildi and pg.locator('details.matn').count() == 0 and pg.locator('#body .opt').count() >= 2, f"ekranda ({t}): masala savoli — ortiqcha oyna yo'q, variantlar bor")
    VER = ev("BJ.A.VER"); ok(tuple(map(int, VER.split('.'))) >= (0, 7, 7) and ('bj-v' + VER) in open(os.path.join(SITE, 'sw.js'), encoding='utf-8').read().replace("P + '", 'bj-v'), f"VER {VER} (≥ 0.7.7) · sw.js bj-v{VER}")
    src = open(os.path.join(SITE, 'index.html'), encoding='utf-8').read()
    ok('oyang' not in src and src.count('oyingga') >= 3, "Imlo (u ko'rsatdi, 08.11): «oyangga» → «oyingga», «oyang beradi» → «oying beradi»")
    ok(not PE, f"JS xato yo'q {PE[:3]}")
finally:
  srv.terminate()
print('\nJAMI XATO:', len(ERR)); [print(' -', e) for e in ERR]; sys.exit(1 if ERR else 0)
