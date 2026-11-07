"""Bilimjon 0.7.1 — 🔊 SAVOL OVOZI (07.11).
A) NUTQ: misollar o'zbekcha gapga, sonlar suffiks bilan (bitta, qirqqa, to'rtinchi), ismlar alohida bo'lak; hamma generatorlarda xatosiz,
   bo'laklarda raqam/arabcha/emoji qolmaydi. Pedagogik qoida: o'qish sinovidagi so'z, bitta harf, arabcha/inglizcha so'z o'qilmaydi; diktantda so'z 2 marta.
B) Ekran: maktabgachaga savol o'zi o'qiladi (bir marta), kattaga — 🔊 tugma bilan; variantni bosib turish javob emas; ovoz o'chiq / ro'yxat yo'q — tugma yo'q;
   ota-ona paneli (ovoz tanlash, namuna); 390 px.
Ovoz fayllari Playwright'da soxta (qisqa WAV tovush, boshida va oxirida jimlik). Ishga tushirish: python3 sinov/v071/sinov_ovoz.py"""
import os, sys, time, subprocess, json, struct, math, io, wave
from playwright.sync_api import sync_playwright

D = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.abspath(os.path.join(D, '..', '..'))
PORT = 8795; URL = f'http://localhost:{PORT}/'
srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT)], cwd=SITE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)
ERR = []
def ok(c, m): print(('✅ ' if c else '❌ ') + m) or (None if c else ERR.append(m))
SHOT = lambda pg, n: pg.screenshot(path=f'/tmp/bjovoz_{n}.png', full_page=True)

def tovush(sek=0.3):  # 0,15 s jimlik + tovush + 0,2 s jimlik — jimlik kesilishini ham sinaydi
    sr = 16000; b = io.BytesIO(); w = wave.open(b, 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
    fr = [0] * int(0.15 * sr) + [int(9000 * math.sin(2 * math.pi * 440 * i / sr)) for i in range(int(sek * sr))] + [0] * int(0.2 * sr)
    w.writeframes(struct.pack('<%dh' % len(fr), *fr)); w.close(); return b.getvalue()
WAV = tovush()
ROY = {'ids': [], 'mode': 'ok'}; REQ = []
def ovoz_route(route):
    u = route.request.url; REQ.append(u)
    if u.endswith('royxat.json'):
        if ROY['mode'] != 'ok': return route.fulfill(status=404, body='yo\'q')
        return route.fulfill(status=200, content_type='application/json', body=json.dumps({'v': 2, 'n': len(ROY['ids']), 'id': ROY['ids']}))
    if u.endswith('.mp3'): return route.fulfill(status=200, content_type='audio/mpeg', body=WAV)
    route.fulfill(status=404, body='')

def tel(br, nom, url):
    ctx = br.new_context(viewport={'width': 390, 'height': 844}, service_workers='block')
    ctx.route('**/ovoz/**', ovoz_route)
    pg = ctx.new_page(); pg.on('pageerror', lambda e: ERR.append(f'{nom} pageerror: {e}'))
    pg.goto(url); pg.wait_for_timeout(400); return pg
def kut(pg, js, ms=6000):
    try: pg.wait_for_function(js, timeout=ms); return True
    except Exception: return False

try:
  with sync_playwright() as p:
    br = p.chromium.launch(args=['--autoplay-policy=no-user-gesture-required'])
    pg = tel(br, 'A', URL + '?tez=1'); ev = pg.evaluate
    pg.fill('#on', 'Ovoz'); pg.fill('#p1', '1234'); pg.fill('#p2', '1234'); pg.click('#go'); pg.wait_for_timeout(300)
    K, O = ev("""(()=>{const A=BJ.A; const k=A.newBola({laqab:'Kichik',daraja:'g0',avatar:'🐯',dunyo:'garaj'}); const o=A.newBola({laqab:'Orta',daraja:'g1',avatar:'🐼',dunyo:'garaj'});
      [k,o].forEach(b=>{b.boshlandi='2026-10-28';}); A.S().sozlama.uyqu=''; A.S().joriy=k.id; A.save(true); return [k.id,o.id]})()""")
    # ======================= A) NUTQ =======================
    M = lambda t: ev("t => BJ.A.ovoz.NUTQ.matn(BJ.A.ovoz.NUTQ.reja(t))", t)
    I = lambda t: ev("t => BJ.A.ovoz.NUTQ.reja(t).map(x => x.id)", t)
    for t, kut_ in [("13 − 8 = ?", "o'n uchdan sakkizni ayirsak, nechchi bo'ladi?"), ("8 + 1 = ?", "sakkizga birni qo'shsak, nechchi bo'ladi?"), ("6 × 3 = ?", "oltini uchga ko'paytirsak, nechchi bo'ladi?"),
                    ("40 + 2 = ?", "qirqqa ikkini qo'shsak, nechchi bo'ladi?"), ("1 dm = ? sm", "bir detsimetr necha santimetr?"), ("1040 + 1 = ?", "ming qirqqa birni qo'shsak, nechchi bo'ladi?"),
                    ("1 ta va yana 1 ta. Hammasi nechta?", "bitta va yana bitta. Hammasi nechta?"), ("Qatorda Laylo oldindan 4-chi turibdi.", "Qatorda Laylo oldindan to'rtinchi turibdi."),
                    ("17  □  9", "o'n yetti va to'qqizni solishtir: katta, kichik yoki teng?"), ("yarim soat = ? daqiqa", "yarim soat necha daqiqa?"), ("Xuddi shu harfni top:  ب", "Xuddi shu harfni top")]:
        ok(M(t) == kut_, f"A: «{t}» → «{M(t)}»")
    ok(I("Malikada 9 ta yong'oq bor edi.")[:2] == ['i_malikada', 'n9_ta'], "A: ism (i_malikada) va son (n9_ta) — alohida bo'lak")
    ok(I("13 − 8 = ?")[:2] == ['n13_dan', 'n8_ni'], "A: son id = qiymat + qo'shimcha (n13_dan, n8_ni)")
    ok(I("270 + 500 = ?")[:3] == ['h2', 'n70_ga', 'h5_ni'], "A: 100 dan katta son — yuz (h2) + qoldiq (n70_ga)")
    ok(I("«tulki» qaysi harf bilan boshlanadi?") == I("«tulki» qaysi harf bilan boshlanadi?") and len(I("«tulki» qaysi harf bilan boshlanadi?")) == 2, "A: «so'z» alohida bo'lak (so'z × ko'rsatma kombinatsiyasi yo'q)")
    sw = ev("""(() => { const reg = BJ.gen.reg, O = BJ.A.ovoz, xato = [], harflar = (BJ.harfTartib||[]).slice(); let n = 0, bol = 0;
      for (const id of Object.keys(reg)) for (let q = 1; q <= 3; q++) for (const g of [true, false]) for (let i = 0; i < 12; i++) {
        let it; try { it = BJ.gen.make(id, q, { g0: g, dunyo: 'garaj', harflar, kashfSavol: i }); } catch (e) { break; } it.tugun = id; n++;
        let r; try { r = O.savolReja(it); if (g && Array.isArray(it.o)) it.o.forEach(o => r = r.concat(O.reja(O.variantMatn(it, o)))); } catch (e) { xato.push(id + ' istisno: ' + e); continue; }
        r.forEach(x => { bol++; if (!x.id || !x.t) xato.push(id + ' bo\\'sh'); if (/\\d/.test(x.t)) xato.push(id + ' raqam: ' + x.t); if (/[\\u0600-\\u06FF]/.test(x.t)) xato.push(id + ' arabcha: ' + x.t); if (/[\\u{1F300}-\\u{1FAFF}\\u2600-\\u27BF]/u.test(x.t)) xato.push(id + ' emoji: ' + x.t); if (x.k === 'n' && !/^[nhks]\\d+(_[a-z]+)?$/.test(x.id)) xato.push(id + ' son id: ' + x.id); });
      } return { n, bol, xato: [...new Set(xato)].slice(0, 12) }; })()""")
    ok(sw['n'] > 8000 and not sw['xato'], f"A: {sw['n']} topshiriq, {sw['bol']} bo'lak — xatosiz, raqam/arabcha/emoji yo'q {sw['xato']}")
    PQ = lambda js: ev(f"""(() => {{ const O = BJ.A.ovoz, mk = (id, q, c) => {{ const it = BJ.gen.make(id, q || 1, Object.assign({{ g0: true, dunyo: 'garaj', harflar: (BJ.harfTartib||[]).slice() }}, c || {{}})); it.tugun = id; return it; }}; {js} }})()""")
    ok(PQ("for (let i=0;i<20;i++){ const it = mk('H0.6'); const t = O.savolReja(it).map(x=>x.t).join(' '); if (t.indexOf(it.sav) >= 0 || !/o'qi/i.test(t)) return false; } return true;"), "A: o'qish sinovi (H0.6) — so'z o'qilmaydi, faqat «So'zni o'qi…»")
    hq = PQ("let n = 0; for (let i=0;i<60;i++){ for (const id of ['H0.2','H0.5','H1.1']) { const it = mk(id); if (/«\\s*[A-Za-z]{1,2}['ʻ]?\\s*»/.test(it.sav) && !/bo'g'in/.test(it.sav)) { n++; if (O.savolReja(it).some(x => it.sav.indexOf(x.t) >= 0 || /harf/.test(x.t))) return -1; } } } return n;")
    ok(hq > 5, f"A: bitta harf («N» harfini top) — o'qilmaydi, kattalar tovush bilan aytadi ({hq} ta savol)")
    ok(PQ("const it = mk('H2.6', 1, { g0: false }); const t = O.savolReja(it).map(x=>x.t); return t.filter(x => x.replace(/[.]/g,'') === String(it.a)).length === 2;"), "A: diktant — so'z ikki marta aytiladi")
    ok(PQ("for (let i=0;i<20;i++){ const it = mk('EN.hayvon', 1); const t = O.savolReja(it).map(x=>x.t).join(' '); if (it.tts && t.indexOf(it.tts) >= 0) return false; } return true;"), "A: inglizcha so'z o'zbek ovozida o'qilmaydi")
    ok(PQ("const it = mk('H2.2', 1, {g0:false}); return it.o.every(o => !O.variantMatn(it, o));") and PQ("const it = mk('M0.3'); return it.o.every(o => !O.variantMatn(it, o));"), "A: imlo va raqam variantlari o'qilmaydi")
    ok(PQ("const it = mk('H0.7'); return it.o.some(o => O.variantMatn(it, o));"), "A: so'zli variant («⚽ to'p») — o'qiladi (emoji'siz)")
    # ovoz fayllari ro'yxati: shu sahifadagi kod bilan yig'ilgan inventar (haqiqiy ovoz/iboralar.json shunday yig'iladi)
    ROY['ids'] = ev("""(() => { const reg = BJ.gen.reg, O = BJ.A.ovoz, s = new Set(), harflar = (BJ.harfTartib||[]).slice();
      for (const id of Object.keys(reg)) for (let q = 1; q <= 3; q++) for (const g of [true, false]) for (let i = 0; i < 25; i++) { let it; try { it = BJ.gen.make(id, q, { g0: g, dunyo: 'garaj', harflar, kashfSavol: i }); } catch (e) { break; } it.tugun = id;
        O.savolReja(it).forEach(x => s.add(x.id)); if (Array.isArray(it.o)) it.o.forEach(o => O.reja(O.variantMatn(it, o)).forEach(x => s.add(x.id))); }
      for (let n = 0; n <= 100; n++) ['', 'ta', 'ga', 'ni', 'dan'].forEach(q => O.NUTQ.sonQism(n, q).forEach(x => s.add(x.id))); return [...s]; })()""")
    ok(len(ROY['ids']) > 1500, f"A: inventar — {len(ROY['ids'])} bo'lak")
    # ======================= B) EKRAN =======================
    X = lambda bid, e: ev(f"(()=>{{const A=BJ.A, b=A.S().bolalar['{bid}']; return {e}}})()")
    NV = [0]
    def NAV(h, ms=600, ota=False):
        NV[0] += 1; pg.goto(URL + f'?tez=1&r={NV[0]}#' + h)
        ev(("BJ.A.otaOk={rol:'admin',t:Date.now()}; " if ota else '') + 'BJ.A.render()'); pg.wait_for_timeout(ms)
    def missiya(bid, fan='mat'):
        X(bid, f"""(()=>{{const m=b.missiya=A.buildMission(b); const bl=m.steps.find(s=>s.k==='blok'&&s.fan==='{fan}')||m.steps.find(s=>s.k==='blok'); const y=m.steps.find(s=>s.k==='yakun')||{{k:'yakun'}};
          m.steps=[Object.assign({{}},bl,{{n:3,olimp:0}}), y]; m.si=0; m.res={{}}; m.cur=null; m.done=false; m.soraQ=[]; m.soraN=0; A.save(true); return 1}})()""")
    def setj(bid): ev(f"(()=>{{const s=BJ.A.S(); s.joriy='{bid}'; BJ.A.save(true)}})()")
    mp3 = lambda: len([u for u in REQ if u.endswith('.mp3') and '/namuna/' not in u])
    setj(K); missiya(K); r0 = mp3(); NAV('missiya', 300)
    ok(kut(pg, "!!document.querySelector('[data-uzs]') && !document.querySelector('[data-uzs]').disabled"), "B: maktabgacha — savolda 🔊 tugma (faol)")
    ok(kut(pg, "!!document.querySelector('.q.gapir')", 4000), "B: maktabgacha — savol O'ZI o'qildi (2A)")
    ok(mp3() > r0, f"B: ovoz fayllari yuklandi ({mp3() - r0} ta)")
    it1 = ev("window.__bjCur().it.sav"); n_oq = ev("window.__bjCur().it.uzOqildi")
    ok(n_oq == 1, "B: o'qildi belgisi (uzOqildi) qo'yildi")
    ok(kut(pg, "!document.querySelector('.q.gapir')", 6000), "B: o'qish tugadi — belgi o'chdi")
    SHOT(pg, '1_g0')
    r = ev("(()=>{const b=document.querySelector('[data-uzs]').getBoundingClientRect(), q=document.querySelector('.q').getBoundingClientRect(); return [document.documentElement.scrollWidth, b.right, b.width, b.height, q.left, q.right]})()")
    ok(r[0] <= 390 and r[1] <= 390 and r[2] >= 40 and r[3] >= 40, f"B: 390 px — tugma ekranda, ≥40 px ({r})")
    pg.click('[data-pause]'); pg.wait_for_timeout(300); NAV('missiya', 1200)
    ok(ev("window.__bjCur().it.sav") == it1 and not ev("!!document.querySelector('.q.gapir')"), "B: pauzadan qaytganda o'sha savol QAYTA o'qilmaydi")
    pg.click('[data-uzs]'); ok(kut(pg, "!!document.querySelector('.q.gapir')", 3000), "B: 🔊 bosilsa — qayta o'qiydi")
    pg.click('[data-uzs]'); pg.wait_for_timeout(200); ok(not ev("!!document.querySelector('.q.gapir')"), "B: o'qiyotganda 🔊 bosilsa — to'xtaydi")
    # kattaroq bola: avtomatik emas, tugma bilan
    setj(O); missiya(O); NAV('missiya', 1300)
    ok(ev("!!document.querySelector('[data-uzs]')") and not ev("!!document.querySelector('.q.gapir')"), "B: 1-sinf — tugma bor, o'zi o'qilmaydi")
    pg.click('[data-uzs]'); ok(kut(pg, "!!document.querySelector('.q.gapir')", 3000), "B: 1-sinf — 🔊 bosilganda o'qiydi")
    SHOT(pg, '2_g1')
    # 3A: variantni bosib turish
    setj(K); NAV('sinov-H0.7-1', 900)
    ok(ev("document.querySelectorAll('.opt.uzv').length") >= 2, "B: so'zli variantlar «bosib tursa o'qiladi» belgisi bilan")
    bx = pg.locator('.opt.uzv').first.bounding_box(); r0 = mp3()
    pg.mouse.move(bx['x'] + bx['width'] / 2, bx['y'] + bx['height'] / 2); pg.mouse.down(); pg.wait_for_timeout(750); pg.mouse.up(); pg.wait_for_timeout(250)
    ok(ev("BJ.A.CUR().sinovNatija === undefined") and ev("!document.querySelector('.opt.ok,.opt.no')"), "B: bosib turish — javob HISOBLANMADI")
    ok(mp3() > r0 or ev("!!document.querySelector('.opt.uzlp,.opt.gapir')"), "B: bosib turish — variant o'qildi")
    pg.wait_for_timeout(600); pg.locator('.opt').first.click(); pg.wait_for_timeout(300)
    ok(ev("BJ.A.CUR().sinovNatija !== undefined"), "B: oddiy bosish — javob qabul qilindi")
    # sozlama: o'chiq / ro'yxat yo'q
    ev("(()=>{const s=BJ.A.S(); s.sozlama.nutq={nom:'',avto:true,variant:true,tugma:true}; BJ.A.save(true)})()"); missiya(K); NAV('missiya', 900)
    ok(not ev("!!document.querySelector('[data-uzs]')"), "B: ovoz o'chiq — tugma yo'q")
    ev("(()=>{const s=BJ.A.S(); s.sozlama.nutq.nom='madina'; BJ.A.save(true); localStorage.removeItem('bj_ovoz_royxat_madina')})()"); ROY['mode'] = 'yoq'
    missiya(K); NAV('missiya', 1200)
    ok(not ev("!!document.querySelector('[data-uzs]')") and not ev("!!document.querySelector('.q.gapir')"), "B: fayllar hali yo'q (404) — tugma chiqmaydi, xato yo'q")
    ROY['mode'] = 'ok'
    # ota-ona paneli
    NAV('ota', 500, ota=True); ok('Savol ovozi' in ev("document.body.innerText"), "B: ota-ona menyusida «🔊 Savol ovozi»")
    NAV('ota-ovoz', 900, ota=True)
    ok(ev("document.querySelectorAll('input[name=uzn]').length") == 4 and ev("document.querySelector('input[name=uzn][value=madina]').checked"), "B: panel — 3 ovoz + o'chiq, standart Madina")
    pg.check('input[name=uzn][value=sardor]'); pg.wait_for_timeout(300)
    ok(ev("BJ.A.S().sozlama.nutq.nom") == 'sardor', "B: Sardor tanlandi — saqlandi")
    pg.uncheck('input[data-k=avto]'); pg.wait_for_timeout(100); ok(ev("BJ.A.S().sozlama.nutq.avto") is False, "B: «o'zi o'qilsin» o'chirildi — saqlandi")
    r0 = len(REQ); pg.click('[data-nam=madina]'); pg.wait_for_timeout(700)
    ok(any('/namuna/madina_n' in u for u in REQ[r0:]), "B: ▶ Namuna — namuna fayllari yuklandi")
    SHOT(pg, '3_panel')
    ok(any('/ovoz/sardor/royxat.json' in u for u in REQ), "B: ovoz almashganda o'sha ovozning ro'yxati so'raldi")
    br.close()
finally:
    srv.terminate()
print('\nNATIJA:', 'HAMMASI O\'TDI ✅' if not ERR else f'{len(ERR)} ta xato ❌'); [print(' -', e) for e in ERR]
sys.exit(1 if ERR else 0)
