"""Bilimjon 0.6.0 — 2-bosqich: 🎁 sovg'a vitrinasi, 📊 hafta xulosasi. python3 sinov/v060/sinov_bosqich2.py (skrinshotlar /tmp/bj060_*.png)"""
import os, sys, time, subprocess, tempfile
from playwright.sync_api import sync_playwright
from PIL import Image

D = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.abspath(os.path.join(D, '..', '..'))
PORT = 8772; URL = f'http://localhost:{PORT}/'
srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT)], cwd=SITE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
RASM = os.path.join(tempfile.mkdtemp(), 'sovga.png'); Image.new('RGB', (1600, 1200), (230, 40, 60)).save(RASM)
ERR = []
def ok(c, m):
    print(('✅ ' if c else '❌ ') + m)
    if not c: ERR.append(m)

with sync_playwright() as p:
    br = p.chromium.launch(); ctx = br.new_context(viewport={'width': 390, 'height': 844}, service_workers='block'); pg = ctx.new_page()
    pg.on('pageerror', lambda e: ERR.append(f'pageerror: {e}')); ev = pg.evaluate
    pg.goto(URL); pg.wait_for_timeout(400)
    pg.fill('#on', 'Sinov'); pg.fill('#p1', '1234'); pg.fill('#p2', '1234'); pg.click('#go'); pg.wait_for_timeout(300)
    K, Q = ev("""(()=>{const A=BJ.A; const k=A.newBola({laqab:'Kichik',daraja:'g0',avatar:'🐯',dunyo:'garaj'}); const q=A.newBola({laqab:'Katta',daraja:'g2',avatar:'🦄',dunyo:'orol'});
      A.S().sozlama.uyqu=''; A.save(true); return [k.id,q.id]})()""")
    ev("BJ.A.otaOk={rol:'admin',t:Date.now()}")
    # ---- 🎁 rasmli sovg'a — kichik bolaga, 2 kun
    pg.goto(URL + '#ota-sovga'); pg.wait_for_timeout(400)
    ok(pg.locator('#sk option').count() == 3, "Kimga: 2 bola + 👨‍👩‍👧 oila")
    pg.select_option('#sk', K); pg.fill('#sn', 'Lego mashina'); pg.set_input_files('#sr', RASM); pg.wait_for_timeout(800); pg.fill('#sh', '2'); pg.click('[data-sv]'); pg.wait_for_timeout(300)
    g = ev("BJ.A.S().sovga[0]")
    ok(g and g['nom'] == 'Lego mashina' and g['rasm'].startswith('data:image/jpeg') and len(g['rasm']) <= 80000 and g['n'] == 2, f"Sovg'a saqlandi, rasm siqildi ({len(g['rasm']) if g else 0} belgi)")
    # sirli — kattaga, 1 kun; oila — 3 kun
    pg.select_option('#sk', Q); pg.fill('#sn', 'Pushti velosiped'); pg.fill('#sh', '1'); pg.check('#ss'); pg.click('[data-sv]'); pg.wait_for_timeout(300)
    pg.select_option('#sk', 'oila'); pg.uncheck('#sj'); ok(pg.input_value('#sh') == '8', 'Oila (jamoa belgisi olinsa — yig\'indi) shart avtomatik 2×4=8')
    pg.fill('#sn', 'Hayvonot bog\'i'); pg.fill('#sh', '3'); pg.click('[data-sv]'); pg.wait_for_timeout(300)
    pg.screenshot(path='/tmp/bj060_sovga_ota.png', full_page=True)
    # o'tgan haftadagi bajarilmagan sovg'a — bolaga ko'rinmaydi
    ev(f"(()=>{{const A=BJ.A; A.S().sovga.push({{id:'eski1',kim:'{K}',nom:'Eski',rasm:'',n:5,hafta:A.prevWeek(A.isoWeek()),yetdi:{{}},berildi:{{}}}}); A.save(true)}})()")
    # ---- bola ekrani
    ev(f"(()=>{{const s=BJ.A.S(); s.joriy='{K}'; BJ.A.save(true)}})()"); pg.goto(URL + '#uy'); pg.wait_for_timeout(500)
    t = pg.inner_text('.kidw')
    ok('Lego mashina' in t and '0/2' in t and pg.locator('.sovga img.sgimg').count() == 1, 'Bola ekranida sovg\'a rasmi, nomi va «0/2 kun»')
    ok("Oila sovg'asi" in t and 'Eski' not in t and 'velosiped' not in t, "Oila sovg'asi ko'rinadi; eski va boshqa bolaning sovg'asi ko'rinmaydi")
    # 2 kun missiya → yetdi + bayram
    ev(f"""(()=>{{const A=BJ.A, b=A.S().bolalar['{K}'], d=A.weekDays(A.isoWeek()); [d[0],d[1]].forEach(k=>{{A.agg(b,k).missiya=1}}); A.save(true)}})()""")
    pg.goto(URL + '#tanla'); pg.wait_for_timeout(200); pg.goto(URL + '#uy'); pg.wait_for_timeout(900)
    t = pg.inner_text('body')
    ok('Seniki' in t and ev("!!BJ.A.S().sovga[0].yetdi[BJ.A.isoWeek()]"), "2/2 → «🎉 Seniki!», bayram bir marta belgilandi")
    pg.screenshot(path='/tmp/bj060_sovga_bola.png', full_page=True)
    lg = ev(f"BJ.A.readLog('{K}',BJ.A.todayKey()).filter(e=>e.t==='sovga').length"); ok(lg == 1, 'Log: {t:"sovga"}')
    # sirli: katta bola ekranida nom yashirin, 1 kun → ochiladi
    ev(f"(()=>{{const s=BJ.A.S(); s.joriy='{Q}'; BJ.A.save(true)}})()"); pg.goto(URL + '#tanla'); pg.wait_for_timeout(200); pg.goto(URL + '#uy'); pg.wait_for_timeout(500)
    t = pg.inner_text('.kidw'); ok('Sirli' in t and 'velosiped' not in t, "Sirli sovg'a: nomi yashirin")
    ev(f"(()=>{{const A=BJ.A, b=A.S().bolalar['{Q}']; A.agg(b,A.weekDays(A.isoWeek())[2]).missiya=1; A.save(true)}})()")
    pg.goto(URL + '#tanla'); pg.wait_for_timeout(200); pg.goto(URL + '#uy'); pg.wait_for_timeout(900)
    t = pg.inner_text('.kidw'); ok('velosiped' in t and 'Seniki' in t, "Shart bajarildi — sirli sovg'a ochildi")
    # oila: 2 + 1 = 3 kun → yetdi
    ok(ev("BJ.A.sovgaHolat(BJ.A.S().sovga[2]).yetdi") and ev("BJ.A.sovgaHolat(BJ.A.S().sovga[2]).bor") == 3, "Oila sovg'asi: ikkala bolaning kunlari qo'shildi (3/3)")
    # ota-ona «Berildi»
    pg.goto(URL + '#ota-sovga'); pg.wait_for_timeout(400); pg.locator('[data-bd]').first.click(); pg.wait_for_timeout(300)
    ok(ev("BJ.A.sovgaHolat(BJ.A.S().sovga[0]).berildi"), "Ota-ona «✅ Berildi» belgiladi")
    # ---- 📊 hafta xulosasi
    ev(f"""(()=>{{const A=BJ.A, ids=Object.keys(BJ.gen.reg).filter(i=>/^M0\\./.test(i)).slice(0,2), now=Date.now();
      for(let i=0;i<12;i++) A.pushLog('{K}',{{t:'ans',ts:now+i,bola:'{K}',fan:'mat',tugun:ids[0],togri_1:1,togri:1,javob_ms:3000,maslahat:0}});
      for(let i=0;i<10;i++) A.pushLog('{K}',{{t:'ans',ts:now+50+i,bola:'{K}',fan:'mat',tugun:ids[1],togri_1:i<3?1:0,togri:1,javob_ms:6000,maslahat:1}});
      A.flushLog(); A.agg(A.S().bolalar['{K}']).faol=20*60; A.save(true)}})()""")
    pg.goto(URL + '#ota-hisobot'); pg.wait_for_timeout(500)
    t = pg.inner_text('.wrap')
    ok('Kuchli' in t and 'Qiyin' in t and 'Tavsiya' in t and '68%' in t, "Hafta xulosasi: kuchli/qiyin mavzu, aniqlik 68% (15/22), tavsiya")
    pg.screenshot(path='/tmp/bj060_hisobot.png', full_page=True)
    pg.goto(URL + '#ota'); pg.wait_for_timeout(400)
    ok(pg.locator('[data-go="ota-sovga"]').count() == 1 and pg.locator('[data-go="ota-hisobot"]').count() == 1, "Ota-ona menyusida 🎁 va 📊 tugmalari")
    br.close()
srv.terminate()
print('\nXATOLAR:', ERR if ERR else "yo'q"); sys.exit(1 if ERR else 0)
