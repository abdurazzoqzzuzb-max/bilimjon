"""Bilimjon 0.7.4 — hafta xulosasi mantiqi, savol ovozi vaqti javob tezligidan ayirilishi, olimpiada qiyinligi, bir martalik ism tuzatish.
Sabab (07.11): o'rtog'ining qizi hisobotida «2/5 — muntazamlik past», «Olimpiada (40%) — ko'proq chiqadi» (noto'g'ri: olimpiada rejalashtirilmaydi),
«10 ichida + − (100%)» lekin o'zlashtirilmagan (savol ovozi o'qilayotgan vaqt «sekin javob» bo'lib, qiyinlik oshmasdi). Ishga tushirish:
python3 sinov/v074/sinov_v074.py"""
import os, sys, time, json, subprocess
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.abspath(os.path.join(D, '..', '..'))
PORT = 8799; URL = f'http://localhost:{PORT}/'
srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT)], cwd=SITE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
ESKI = bytes.fromhex('4261626f786174').decode(); YANGI = 'S' + ESKI[1:]   # bolaning ismi repoga ochiq yozilmaydi (ilovada ham — fnv xesh)
ERR = []
def ok(c, m): print(('✅ ' if c else '❌ ') + m); (None if c else ERR.append(m))
try:
  with sync_playwright() as p:
    br = p.chromium.launch(args=['--autoplay-policy=no-user-gesture-required'])
    ctx = br.new_context(viewport={'width': 390, 'height': 844}, service_workers='block')
    pg = ctx.new_page(); PE = []
    pg.on('pageerror', lambda e: PE.append(str(e)))
    ev = pg.evaluate
    pg.clock.set_fixed_time('2026-11-07T12:00:00')   # shanba (W45: 02.11–08.11)
    def kut(js, ms=8000):
        t = time.time()
        while time.time() - t < ms / 1000:
            if ev(js): return True
            pg.wait_for_timeout(100)
        return False
    pg.goto(URL + '?tez=1'); pg.wait_for_timeout(500)
    pg.fill('#on', 'Sinov'); pg.fill('#p1', '1234'); pg.fill('#p2', '1234'); pg.click('#go'); pg.wait_for_timeout(300)
    # ---------- A) bir martalik ism tuzatish ----------
    ev("""(()=>{const A=BJ.A; const a=A.newBola({laqab:'Malika',daraja:'g1',avatar:'🦋',dunyo:'orol'}); const s=A.S(); s.uyqu=''; s.sozlama.uyqu=''; s.joriy=a.id; A.save(true);
      const raw=JSON.parse(localStorage.getItem(A.KEY)); const id='bxato01'; raw.bolalar[id]=Object.assign(JSON.parse(JSON.stringify(raw.bolalar[a.id])),{id, laqab:'""" + ESKI + """', kod:'B9'}); raw.tartib.push(id); A.setS(raw); })()""")   # eski holat yuklanganda (migrate → fixBola)
    pg.reload(); pg.wait_for_timeout(500)
    L = ev("BJ.A.bolalar().map(b => [b.laqab, !!b.ismTuz])")
    ok([YANGI, True] in L and ['Malika', False] in L, f"xatoli ism bir marta tuzatildi, boshqasi o'zgarmadi: {L}")
    ev("(()=>{const b=BJ.A.bolalar().find(x=>x.ismTuz); b.laqab='" + ESKI + "'; BJ.A.save(true)})()"); pg.reload(); pg.wait_for_timeout(400)
    ok(ESKI in ev("BJ.A.bolalar().map(b=>b.laqab)"), "ota-ona qaytadan o'zgartirsa — ilova qayta tegmaydi (bir martalik)")
    ok('611f9d28' in open(os.path.join(SITE, 'index.html'), encoding='utf-8').read() and 'oxat' not in open(os.path.join(SITE, 'index.html'), encoding='utf-8').read().lower(),
       "repoda ism yo'q — faqat xesh")
    # ---------- B) savol ovozi vaqti javob tezligidan ayiriladi ----------
    # (soat to'xtatilmagan alohida oyna — vaqt o'lchanadi)
    c2 = br.new_context(viewport={'width': 390, 'height': 844}, service_workers='block'); pg = c2.new_page(); pg.on('pageerror', lambda e: PE.append(str(e))); ev = pg.evaluate
    pg.goto(URL + '?tez=1'); pg.wait_for_timeout(500)
    pg.fill('#on', 'Sinov'); pg.fill('#p1', '1234'); pg.fill('#p2', '1234'); pg.click('#go'); pg.wait_for_timeout(300)
    ev("(()=>{const A=BJ.A; const b=A.newBola({laqab:'Malika',daraja:'g1',avatar:'🦋',dunyo:'orol'}); A.S().sozlama.uyqu=''; A.S().joriy=b.id; A.save(true)})()")
    pg.goto(URL + '?tez=1&r=1#sinov-M1.1-1'); ev('BJ.A.render()')
    ok(kut("!!document.querySelector('.q.gapir')", 6000), "M1.1 savoli ovozda o'qilmoqda")
    ok(kut("!document.querySelector('.q.gapir') && BJ.A.ovoz.ijroMs() > 0", 12000), "o'qish tugadi")
    oqish = ev("BJ.A.ovoz.ijroMs()"); pg.wait_for_timeout(1500); ev("window.__bjJavob(true)"); pg.wait_for_timeout(300)
    e = ev("(()=>{const b=BJ.A.bola(); const L=BJ.A.readLog(b.id, BJ.A.todayKey()).filter(e=>e.t==='ans'); return L[L.length-1]})()")
    ok(e and e['ovoz_ms'] >= oqish - 50 and e['ovoz_ms'] >= 800, f"ovoz vaqti logda: ovoz_ms={e and e['ovoz_ms']} (o'qish {oqish} ms)")
    ok(e and 1400 <= e['javob_ms'] <= 2600, f"javob tezligi — ovoz tugagandan keyingi vaqt: javob_ms={e and e['javob_ms']} (xom {e and e['javob_ms'] + e['ovoz_ms']})")
    pg.goto(URL + '?tez=1&r=2#sinov-M1.1-1'); ev('BJ.A.render()')
    kut("!!document.querySelector('.q.gapir')", 6000); pg.wait_for_timeout(300); ev("window.__bjJavob(true)"); pg.wait_for_timeout(300)
    e2 = ev("(()=>{const b=BJ.A.bola(); const L=BJ.A.readLog(b.id, BJ.A.todayKey()).filter(e=>e.t==='ans'); return L[L.length-1]})()")
    ok(e2 and e2['ovoz_ms'] == 0, f"o'qish paytida javob bergan bo'lsa — xom vaqt (ovoz_ms={e2 and e2['ovoz_ms']}, javob_ms={e2 and e2['javob_ms']})")
    # 8 ta to'g'ri javob: ovozdan keyin 3 s o'ylaydi → qiyinlik oshadi (avval xom vaqt me'yordan oshib, q o'zgarmasdi)
    ev("(()=>{const b=BJ.A.bola(); delete b.tugun['M1.1']; BJ.A.save(true)})()")
    for i in range(8):
        pg.goto(URL + f'?tez=1&r=q{i}#sinov-M1.1-1'); ev('BJ.A.render()')
        kut("!!document.querySelector('.q.gapir')", 6000); kut("!document.querySelector('.q.gapir')", 12000); pg.wait_for_timeout(3000); ev("window.__bjJavob(true)"); pg.wait_for_timeout(200)
    t = ev("(()=>{const t=BJ.A.bola().tugun['M1.1']; return {q:t.q, ms:t.ms.slice(-8)}})()")
    L8 = ev("(()=>{const b=BJ.A.bola(); return BJ.A.readLog(b.id, BJ.A.todayKey()).filter(e=>e.t==='ans').slice(-8).map(e=>e.javob_ms+e.ovoz_ms)})()")
    ok(t['q'] >= 2, f"8 ta to'g'ri (ovozdan keyin ~3 s) → qiyinlik oshdi: q={t['q']}; hisobga olingan ms {sorted(t['ms'])[4]} · xom ms {sorted(L8)[4]} (me'yor 5000)")
    # ---------- C) olimpiada qiyinligi ----------
    r = ev("""(()=>{const A=BJ.A, b=A.bola(); const f=w=>{ b.tugun.OL={n:w.length,ok1:0,hint:0,ms:[],oyna:w,holat:'mashq',q:1,oldin:[],kun:{},srs:null}; return A.olimpQ(b); };
      const g=b.daraja; const out=[f([0,0,0,0,0,0,1,0]), f([1,1,1,1,1,1,1,0]), f([1,0,1,0,0,1]), f([0,0,0])]; b.daraja='g0'; out.push(f([0,0,0,0,0,0])); b.daraja=g; delete b.tugun.OL; return out; })()""")
    ok(r == [1, 3, 2, 2, 1], f"olimpiada: g1 12% → q1, 88% → q3, 50% → q2 (o'zgarmaydi), kam urinish → q2, g0 → q1 (pastga tushmaydi): {r}")
    pg = ctx.pages[0]; ev = pg.evaluate   # ---------- D) hafta xulosasi (o'rtog'ining qizi holati; soat 07.11) ----------
    x = ev("""(()=>{const A=BJ.A; const b=A.newBola({laqab:'Yangi',daraja:'g1',avatar:'🌸',dunyo:'orol'}); b.yaratildi='2026-11-05'; b.boshlandi='2026-11-05';
      const kun=(k,faol,y)=>{ b.kun[k]=Object.assign(A.agg(b,k),{faol, missiya:1, yarim:y}); };
      kun('2026-11-05',1900,[[40,36],[40,33]]); kun('2026-11-06',1950,[[35,30],[34,28]]);
      const add=(k,tugun,ok)=>A.pushLog(b.id,{t:'ans',ts:new Date(k+'T15:00:00').getTime(),bola:b.id,fan:'mat',tugun,togri_1:ok?1:0,togri:ok?1:0,javob_ms:3000,maslahat:0,tur:'missiya'});
      for(let i=0;i<9;i++) add('2026-11-05','M1.1',1); [1,0,1,0,0].forEach(o=>add('2026-11-06','OL',o)); for(let i=0;i<8;i++) add('2026-11-06','H1.1',i<7);
      b.tugun['M1.1']={n:9,ok1:9,hint:0,ms:[],oyna:[1,1,1,1,1,1,1,1,1],holat:'mashq',q:1,oldin:[],kun:{},srs:null}; A.flushLog(); A.save(true);
      return A.xulosa(b, A.isoWeek()); })()""")
    m = x['matn']; print('   ' + m.replace('\n', '\n   '))
    ok('2/3 kun faol' in m and '05.11 dan boshlagan' in m, "kunlar bola boshlagan kundan sanaladi (2/3, «05.11 dan boshlagan»)")
    ok('Muntazamlik past' not in m, "hafta o'rtasida qo'shilgan bolaga «muntazamlik past» deyilmaydi")
    ok('Olimpiada masalalari: 2/5 (40%)' in m and 'Olimpiada masalasi (' not in m and "ko'proq chiqadi" not in m, "olimpiada — alohida qatorda, «qiyin» ro'yxatida ham, «ko'proq chiqadi» ham yo'q")
    ok('punkt pasaydi (biroz' in m and "o'zgargan" not in m, "charchash: «7 punkt pasaydi (biroz — odatiy holat)»")
    ok('deyarli xatosiz' in m, "100% mavzu — «ilova asta-sekin qiyinlashtiradi»")
    # oddiy (to'liq hafta) bola: muntazamlik tavsiyasi hali ham ishlaydi
    x2 = ev("""(()=>{const A=BJ.A; const b=A.newBola({laqab:'Eski',daraja:'g1',avatar:'🐻',dunyo:'garaj'}); b.yaratildi='2026-10-20'; b.boshlandi='2026-10-20';
      b.kun['2026-11-03']=Object.assign(A.agg(b,'2026-11-03'),{faol:1500,missiya:1}); A.save(true); return A.xulosa(b, A.isoWeek()).matn; })()""")
    ok('1/6 kun faol' in x2 and 'Muntazamlik past' in x2, "eski bola, haftada 1 kun → «muntazamlik past» (o'zgarmagan)")
    # ota-ona ekrani ochiladi
    pg.goto(URL + '?tez=1&r=h#ota-hisobot'); ev("BJ.A.otaOk={rol:'admin',t:Date.now()}; BJ.A.render()"); pg.wait_for_timeout(500)
    ok('Olimpiada masalalari' in ev("document.body.innerText"), "📊 Hafta xulosasi ekranida yangi qatorlar")
    ok(not PE, f"JS xato yo'q {PE[:3]}")
    br.close()
finally:
    srv.terminate()
print(f"\n{'HAMMASI OK' if not ERR else str(len(ERR)) + ' ta xato'}")
for e in ERR: print('  -', e)
sys.exit(1 if ERR else 0)
