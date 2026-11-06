"""Bilimjon 0.7.0 — 2-bosqich: 🧺 OILA BOZORI.
Oila puli alohida (bola hamyoniga tegmaydi), ro'yxat (ehtiyoj) → kassa → xohish javoni (haftasiga 1) → chek, tejash 50% (haftasiga ≤ 5 000·k),
yosh bo'yicha: g0 sanash + avtomatik to'lov, g1 «yetadimi?» + kupyura, g2 «qaysi arzon?» + qaytim. Ota-ona paneli: topshiriq shakli, narx xotirasi, cheklar, xohish javoni.
Ishga tushirish: python3 sinov/v070/sinov_bosqich2.py  (skrinshotlar: /tmp/bj070_2_*.png)"""
import os, sys, time, json, subprocess
from playwright.sync_api import sync_playwright

D = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.abspath(os.path.join(D, '..', '..'))
PORT = 8779; URL = f'http://localhost:{PORT}/'
srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT)], cwd=SITE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
ERR = []
def ok(c, m):
    print(('✅ ' if c else '❌ ') + m)
    if not c: ERR.append(m)
NV = [0]
SHOT = lambda pg, n: pg.screenshot(path=f'/tmp/bj070_2_{n}.png', full_page=True)
V = lambda l, n, h=1: {'l': l, 'narx': n, 'haj': h}
ROY1 = [  # 1-sinf: 5 ta narsa
    {'id': 'i1', 'k': 'non', 'nom': 'Non', 'miq': 2, 'bir': 'dona', 'v': [V(0, 3000), V(1, 4000), V(2, 6000)]},
    {'id': 'i2', 'k': 'sut', 'nom': 'Sut', 'miq': 1, 'bir': 'l', 'v': [V(0, 9000), V(1, 12000), V(2, 15000)]},
    {'id': 'i3', 'k': 'olma', 'nom': 'Olma', 'miq': 1, 'bir': 'kg', 'v': [V(0, 10000), V(2, 18000)]},
    {'id': 'i4', 'k': 'tuxum', 'nom': 'Tuxum', 'miq': 10, 'bir': 'dona', 'v': [V(0, 14000, 10), V(1, 16000, 10)]},
    {'id': 'i5', 'k': 'kartoshka', 'nom': 'Kartoshka', 'miq': 2, 'bir': 'kg', 'v': [V(0, 5000), V(1, 6000)]}]
ROY0 = [  # maktabgacha: 3 ta «dona»
    {'id': 'k1', 'k': 'non', 'nom': 'Non', 'miq': 3, 'bir': 'dona', 'v': [V(0, 3000), V(2, 5000)]},
    {'id': 'k2', 'k': 'suv', 'nom': 'Suv', 'miq': 2, 'bir': 'dona', 'v': [V(0, 2000), V(1, 3000)]},
    {'id': 'k3', 'k': 'qatiq', 'nom': 'Qatiq', 'miq': 1, 'bir': 'dona', 'v': [V(0, 6000), V(2, 9000)]}]
ROY2 = [  # 2-sinf: qadoqlari har xil (birlik narxi savoli)
    {'id': 'q1', 'k': 'guruch', 'nom': 'Guruch', 'miq': 2, 'bir': 'kg', 'v': [V(0, 12000, 1), V(1, 6500, 0.5), V(2, 23000, 2)]},
    {'id': 'q2', 'k': 'sut', 'nom': 'Sut', 'miq': 1, 'bir': 'l', 'v': [V(0, 5000, 0.5), V(1, 9000, 1)]},
    {'id': 'q3', 'k': 'non', 'nom': 'Non', 'miq': 2, 'bir': 'dona', 'v': [V(0, 3000), V(1, 4000)]},
    {'id': 'q4', 'k': 'piyoz', 'nom': 'Piyoz', 'miq': 1, 'bir': 'kg', 'v': [V(0, 4000), V(2, 7000)]},
    {'id': 'q5', 'k': 'tuz', 'nom': 'Tuz', 'miq': 1, 'bir': 'paket', 'v': [V(0, 2000), V(1, 3000)]},
    {'id': 'q6', 'k': 'choy', 'nom': 'Choy', 'miq': 1, 'bir': 'paket', 'v': [V(0, 15000), V(2, 25000)]}]

try:
  with sync_playwright() as p:
    br = p.chromium.launch(); ctx = br.new_context(viewport={'width': 390, 'height': 844}, service_workers='block'); pg = ctx.new_page()
    pg.on('pageerror', lambda e: ERR.append(f'pageerror: {e}')); ev = pg.evaluate
    def NAV(h, ms=450):
        NV[0] += 1; pg.goto(URL + f'?tez=1&r={NV[0]}#' + h); ev('BJ.A.render()'); pg.wait_for_timeout(ms)
    def GO(h, ms=350):
        ev(f"location.hash='{h}'"); pg.wait_for_timeout(ms)
    pg.goto(URL + '?tez=1'); pg.wait_for_timeout(400)
    pg.fill('#on', 'Sinov'); pg.fill('#p1', '1234'); pg.fill('#p2', '1234'); pg.click('#go'); pg.wait_for_timeout(300)
    K, Q, R = ev("""(()=>{const A=BJ.A; const k=A.newBola({laqab:'Kichik',daraja:'g0',avatar:'🐯',dunyo:'garaj'}); const q=A.newBola({laqab:'Katta',daraja:'g2',avatar:'🦄',dunyo:'orol'});
      const r=A.newBola({laqab:'Orta',daraja:'g1',avatar:'🐼',dunyo:'garaj'});
      A.S().sozlama.uyqu=''; A.S().joriy=r.id; A.save(true); return [k.id,q.id,r.id]})()""")
    setj = lambda bid: ev(f"(()=>{{const s=BJ.A.S(); s.joriy='{bid}'; BJ.A.save(true)}})()")
    X = lambda bid, e: ev(f"(()=>{{const A=BJ.A, Z=A.bozor, b=A.S().bolalar['{bid}']; return {e}}})()")
    W390 = lambda: ev("[document.documentElement.scrollWidth, Math.max(0, ...[...document.querySelectorAll('.top .ib, .top .pill, .bzit, .bzbar, .card')].map(e=>e.getBoundingClientRect().right))]")
    def mk(bid, byu, roy):
        return ev(f"""(()=>{{const A=BJ.A, z=A.bozor.bz(); const t={{id:A.rid(6),kim:'{bid}',byu:{byu},roy:{json.dumps(roy)},ts:Date.now(),sana:A.todayKey(),holat:'yangi',sav:{{}},son:{{}},savol:{{n:0,ok:0,q:{{}}}},tolandi:false,sarf:0,xoh:null}};
          z.top.push(t); A.save(true); return t.id}})()""")
    T = lambda tid, e: ev(f"(()=>{{const A=BJ.A, t=A.bozor.bz().top.find(x=>x.id==='{tid}'); return {e}}})()")
    def tolash(tray_only=False):
        """Ochiq to'lov varag'ida pullarni tanlab berish (ortiqcha pulsiz)."""
        info = ev("""(()=>{const el=document.querySelector('.sheet'); const t=el.querySelector('.tsum').textContent; const m=t.match(/narxi ([\\d ]+)/); return [[...el.querySelectorAll('[data-v]')].map(x=>+x.dataset.v), m?+m[1].replace(/ /g,''):0]})()""")
        notes, narx = info
        bor = {}
        for v in ev("""[...document.querySelectorAll('.sheet [data-v]')].map(x=>[+x.dataset.v, +x.querySelector('i').textContent.slice(1)])"""): bor[v[0]] = v[1]
        pool = sorted([v for v, c in bor.items() for _ in range(c)], reverse=True); tray = []
        for v in pool:
            if sum(tray) >= narx: break
            tray.append(v)
        while True:
            rm = [v for v in sorted(tray) if sum(tray) - v >= narx]
            if not rm: break
            tray.remove(rm[0])
        for v in tray: pg.click(f'.sheet .tl2 [data-v="{v}"]'); pg.wait_for_timeout(40)
        return narx, sum(tray)

    # ================= MODEL =================
    r = X(R, "[typeof A.bozor, A.S().sozlama.bozor, A.S().sozlama.bozorXoh, b.bozor, A.FAN.bozor.nom, Z.bz().xoh.map(x=>x.k).join(','), Z.bz().xoh.every(x=>x.narx===null)]")
    ok(r == ['object', True, True, None, 'Oila bozori', 'kola,chips', True], f"Modul, sozlama (bozor, xohish javoni yoqiq), b.bozor=null, xohish standarti kola+chips narxsiz {r}")
    ok(ev("(()=>{const s=BJ.A.migrate(JSON.parse(JSON.stringify(Object.assign({}, BJ.A.S(), {sozlama: {ovoz: .5}, bozor: undefined})))); return [s.sozlama.bozor, s.sozlama.bozorXoh, 'bozor' in s]})()") == [True, True, True], "Eski holatdan yangilanganda sozlama.bozor/bozorXoh = true")
    ok(ev("BJ.A.bozor.oilaAjrat(50000).join(',')") == '20000,20000,10000' and ev("Math.max(...BJ.A.bozor.oilaAjrat(100000))") == 20000, "Oila hamyoni mayda kupyuralarda (≤ 20 000)")
    ok(ev("[BJ.A.bozor.miqT(0.5,'kg'), BJ.A.bozor.miqT(2,'kg'), BJ.A.bozor.miqT(0.5,'l'), BJ.A.bozor.miqT(3,'dona'), BJ.A.bozor.qd(10,'dona'), BJ.A.bozor.qd(0.5,'kg')]") == ['500 g', '2 kg', '500 ml', '3 ta', '10 talik qadoq', '500 g'], "Miqdor yozuvi: 500 g, 2 kg, 500 ml, 3 ta, 10 talik qadoq")
    # birlik narxi savoli
    r = ev(f"(()=>{{const Z=BJ.A.bozor, R={json.dumps(ROY2)}; return R.map(Z.savolJavob)}})()")
    ok(r == [2, 1, -1, -1, -1, -1], f"«Qaysi arzon?»: faqat qadoqlari har xil va bitta aniq eng arzoni bor narsada (guruch — 2 kg qop, sut — 1 l) {r}")
    ok(ev("BJ.A.bozor.savolJavob({v:[{narx:6000,haj:.5},{narx:12000,haj:1}]})") == -1, "Birlik narxlari teng bo'lsa — savol yo'q")
    # tejash
    ok(X(R, "[Z.tejMuk(b, 10000), Z.tejMuk(b, 10050), Z.tejMuk(b, 30000), Z.tejMuk(b, 0), A.pul.narxK(b, 5000)]") == [5000, 5000, 5000, 0, 5000], "Tejash: 50%, 100 ga yaxlit, haftasiga ≤ 5 000·k")
    X(R, "(A.pul.st(b).byudjet=100000, 0)"); ok(X(R, "Z.tejMuk(b, 30000)") == 10000, "Bola byudjeti 100 000 (k=2) → tejash chegarasi 10 000")
    X(R, "(A.pul.st(b).byudjet=null, A.save(true), 0)")
    ev("BJ.A.S().sozlama.pul=false"); ok(X(R, "Z.tejMuk(b, 10000)") == 0, "So'm iqtisodi o'chiq → tejash mukofoti 0"); ev("BJ.A.S().sozlama.pul=true; BJ.A.save(true)")
    # tekshir()
    tk = lambda F: ev(f"(()=>{{const r=BJ.A.bozor.tekshir({json.dumps(F)}); return [r.xato, r.ogoh, r.mn, r.mx]}})()")
    r = tk({'kim': [R], 'byu': 50000, 'roy': [{'id': 'a', 'k': 'non', 'nom': 'Non', 'miq': 2, 'bir': 'dona', 'v': [{'narx': 3000, 'haj': 1}, {'narx': None, 'haj': 1}, {'narx': None, 'haj': 1}]}]})
    ok(any('kamida 2 ta narx' in x for x in r[0]), f"Shakl: bitta narx — xato {r[0]}")
    r = tk({'kim': [R], 'byu': 50000, 'roy': [{'id': 'a', 'k': 'olma', 'nom': 'Olma', 'miq': 1, 'bir': 'kg', 'v': [{'narx': 8000, 'haj': 1}, {'narx': 5000, 'haj': 0.4}, {'narx': None, 'haj': 1}]}]})
    ok(any('qadoqlarga aniq' in x for x in r[0]), f"Shakl: 1 kg ni 400 g qadoqqa bo'lib bo'lmaydi — xato {r[0]}")
    r = tk({'kim': [R], 'byu': 10000, 'roy': [{'id': 'a', 'k': 'olma', 'nom': 'Olma', 'miq': 2, 'bir': 'kg', 'v': [{'narx': 8000, 'haj': 1}, {'narx': 9000, 'haj': 1}, {'narx': None, 'haj': 1}]}]})
    ok(any('yetmaydi' in x for x in r[0]) and r[2] == 16000, f"Shakl: eng arzoni ham byudjetdan katta — xato {r[0]}")
    r = tk({'kim': [K], 'byu': 90000, 'roy': [{'id': 'a', 'k': 'olma', 'nom': 'Olma', 'miq': 2, 'bir': 'kg', 'v': [{'narx': 8000, 'haj': 1}, {'narx': 9000, 'haj': 1}, {'narx': None, 'haj': 1}]}]})
    ok(not r[0] and any('qimmatlari bilan ham' in x for x in r[1]) and any('«dona»' in x for x in r[1]) and any('3 ta narsa' in x for x in r[1]), f"Shakl ogohlantirishlari: byudjet juda katta, maktabgachaga kg, soni {r[1]}")
    ok(tk({'kim': [], 'byu': 0, 'roy': []})[0][:2] == ['Kimga — kamida bitta bolani belgilang', "Ro'yxatga kamida bitta narsa qo'shing"], "Shakl: bo'sh — kimga va ro'yxat xatosi")

    # ================= 👨‍👩‍👧 OTA-ONA PANELI =================
    ev("BJ.A.otaOk={rol:'admin',t:Date.now()}"); GO('ota', 400)
    ok(pg.locator('[data-go="ota-bozor"]').count() == 1, "Ota-ona menyusida «🧺 Oila bozori»")
    pg.click('[data-go="ota-bozor"]'); pg.wait_for_timeout(350)
    ok(ev("location.hash") == '#ota-bozor' and pg.locator('#bzon:checked').count() == 1 and pg.locator('#bzxo:checked').count() == 1, "Panel: sozlama — bozor va xohish javoni yoqiq")
    ok(pg.locator('[data-xn]').count() == 2 and pg.locator('[data-xadd]').count() == 4, "Xohish javoni: kola, chips + 4 ta qo'shish tugmasi")
    pg.fill('[data-xn="kola"]', '7000'); pg.dispatch_event('[data-xn="kola"]', 'change'); pg.wait_for_timeout(100)
    pg.fill('[data-xn="chips"]', '8000'); pg.dispatch_event('[data-xn="chips"]', 'change'); pg.wait_for_timeout(100)
    pg.click('[data-xadd="muzqaymoq"]'); pg.wait_for_timeout(250)
    ok(ev("BJ.A.bozor.bz().xoh.map(x=>[x.k,x.narx]).join(';')") == 'kola,7000;chips,8000;muzqaymoq,', "Xohish narxlari saqlandi (kola 7 000, chips 8 000), muzqaymoq narxsiz qo'shildi")
    w = W390(); ok(w[0] <= 390, f"390 px: bozor paneli {w}")
    SHOT(pg, 'ota_panel')
    # --- yangi topshiriq shakli
    pg.click('[data-yangi]'); pg.wait_for_timeout(350)
    ok(ev("location.hash") == '#ota-bozor-yangi' and pg.locator('[data-kim]').count() == 3, "Yangi topshiriq shakli: 3 bola")
    pg.check(f'[data-kim="{R}"]'); pg.wait_for_timeout(250)
    ok('1-sinf' in pg.inner_text('body') and pg.locator('[data-namuna]:not([disabled])').count() == 1, "Bola tanlandi → yosh maslahati, namuna tugmasi ochildi")
    pg.click('[data-namuna]'); pg.wait_for_timeout(300)
    ok(pg.locator('.bzf').count() == 5, f"1-sinf namunasi: 5 ta narsa ({pg.locator('.bzf').count()})")
    pg.click('[data-saqla]'); pg.wait_for_timeout(250)
    ok(X(R, "Z.bz().top.length") == 0 and pg.locator('.bzxt').count() >= 1, "Narxsiz saqlab bo'lmaydi (⛔ xatolar ko'rinadi)")
    narxlar = [[3000, 4000, 5000], [9000, 11000, 14000], [10000, 14000, 18000], [14000, 16000, 0], [5000, 6000, 0]]
    for i, ns in enumerate(narxlar):
        for j, n in enumerate(ns):
            if n: pg.fill(f'.bzf[data-i="{i}"] [data-f="n{j}"]', str(n))
    pg.fill('#bzbyu', '60000'); pg.wait_for_timeout(150)
    s = pg.inner_text('#bzsum')
    ok('eng arzon' in s and '62 000' not in s and pg.locator('.bzxt').count() == 0, f"Narxlar to'ldirildi — xato yo'q, savat oralig'i ko'rinadi: {s[:90]}")
    w = W390(); ok(w[0] <= 390, f"390 px: topshiriq shakli {w}")
    SHOT(pg, 'ota_forma')
    pg.click('[data-saqla]'); pg.wait_for_timeout(350)
    t1 = X(R, "Z.faol(b) && Z.faol(b).id")
    r = T(t1, "[t.byu, t.roy.length, t.holat, t.roy[3].v.length, t.roy[3].v[0].haj, t.roy.map(x=>x.v.map(v=>v.l).join('')).join('|')]")
    ok(r == [60000, 5, 'yangi', 2, 10, '012|012|012|01|01'], f"Topshiriq yaratildi: byudjet, 5 narsa, tuxum 10 talik qadoq, bo'sh narxlar tashlandi {r}")
    ok(ev("Object.keys(BJ.A.bozor.bz().narx).sort().join(',')") == 'kartoshka,non,olma,sut,tuxum' and ev("BJ.A.bozor.bz().narx.sut.v[1][0]") == 11000, "Narx xotirasi saqlandi")
    ok(ev("location.hash") == '#ota-bozor' and 'hali ochmagan' in pg.inner_text('body'), "Panelda faol topshiriq: «hali ochmagan»")
    # narx xotirasi keyingi shaklda
    ok(ev("BJ.A.bozor.yangiNarsa('sut').v.map(v=>v.narx).join(',')") == '9000,11000,14000', "Keyingi safar narxlar o'zi chiqadi")
    # bir bolada ikkinchi faol topshiriq — taqiq
    ok(any('tugallanmagan' in x for x in ev(f"BJ.A.bozor.tekshir({{kim:['{R}'], byu:50000, roy:{json.dumps([{'id':'z','k':'non','nom':'Non','miq':1,'bir':'dona','v':[{'narx':3000,'haj':1},{'narx':4000,'haj':1}]}])}}}).xato")), "Faol topshiriq bor bolaga yangisini berib bo'lmaydi")
    # yangi ro'yxatni testdagi ROY1 ga almashtiramiz (aniq hisob uchun)
    T(t1, f"(t.roy={json.dumps(ROY1)}, t.byu=60000, BJ.A.save(true), 0)")

    # ================= 📗 1-SINF: oqim =================
    setj(R); h0 = X(R, "A.pul.st(b).h")
    NAV('uy')
    ok(pg.locator('[data-bozor].pulse').count() == 1 and 'yangi topshiriq' in pg.inner_text('[data-bozor]'), "Uyda yorqin «🧺 Oila bozori · yangi topshiriq!» tugmasi")
    w = W390(); ok(w[0] <= 390, f"390 px: uy ekrani {w}")
    pg.click('[data-bozor]'); pg.wait_for_timeout(400)
    ok(ev("location.hash") == '#bozor' and pg.locator('.bzkir').count() == 1 and 'Ehtiyoj' in pg.inner_text('.bzkir') and 'Xohish' in pg.inner_text('.bzkir'), "Bozor: kirish varag'i — ehtiyoj va xohish")
    ok(T(t1, "t.holat") == 'jarayon' and X(R, "A.readLog(b.id, A.todayKey()).filter(e=>e.t==='bozor'&&e.hodisa==='boshladi').length") == 1, "Holat → jarayon, log «boshladi»")
    pg.click('.bzkir [data-ok]'); pg.wait_for_timeout(250)
    ok(pg.locator('.bzit').count() == 5 and pg.locator('[data-kassa][disabled]').count() == 1, "5 ta narsa kartasi, kassa yopiq")
    ok('60 000' in pg.inner_text('.bzham') and pg.locator('.bzham .bnk').count() == 3, "Oila hamyoni: 60 000 — 3 ta 20 000 lik")
    w = ev("[document.documentElement.scrollWidth, document.querySelector('.bzbar [data-kassa]').getBoundingClientRect().right]")
    ok(w[0] <= 390 and w[1] <= 390, f"390 px: kassa paneli sig'adi {w}")
    SHOT(pg, 'g1_royxat')
    def tanla(iid, vi):
        pg.click(f'[data-it="{iid}"]'); pg.wait_for_timeout(200)
        if pg.locator('.sheet [data-q]').count():
            a = ev(f"(()=>{{const b=BJ.A.bola(), t=BJ.A.bozor.faol(b); return BJ.A.bozor.savolJavob(t.roy.find(x=>x.id==='{iid}'))}})()")
            pg.click(f'.sheet [data-q="{a}"]'); pg.wait_for_timeout(250)
        pg.click(f'.sheet [data-v="{vi}"]'); pg.wait_for_timeout(200)
    pg.click('[data-it="i4"]'); pg.wait_for_timeout(200)
    ok(pg.locator('.sheet .bzvar').count() == 2 and '10 talik qadoq' in pg.inner_text('.sheet'), "Tuxum varag'i: 2 variant, «10 talik qadoq»")
    ok(pg.locator('.sheet .bztg').count() == 2, "Variantlarda tanga belgisi (arzon 1, o'rta 2)")
    pg.click('.sheet [data-v="1"]'); pg.wait_for_timeout(200)
    for iid, vi in (('i1', 2), ('i2', 1), ('i3', 1), ('i5', 0)): tanla(iid, vi)
    # non 2×6000=12000, sut 12000, olma qimmat 18000, tuxum 16000, kartoshka 2×5000=10000 → 68 000 > 60 000
    ok(T(t1, "BJ.A.bozor.jami(t)") == 68000 and 'Yetmayapti' in pg.inner_text('.bzham'), "Savat 68 000 — «Yetmayapti 8 000»")
    ok(pg.locator('[data-kassa]:not([disabled])').count() == 1 and pg.locator('.bzit.ok').count() == 5, "Hamma tanlandi → kassa ochiq")
    ok('2 × 6 000 = 12 000' in pg.inner_text('[data-it="i1"]'), "Kartada hisob: 2 × 6 000 = 12 000")
    w = W390(); ok(w[0] <= 390, f"390 px: ro'yxat {w}")
    pg.click('[data-kassa]'); pg.wait_for_timeout(250)
    ok('yetadimi' in pg.inner_text('.sheet').lower(), "1-sinf: kassada «Oila puli yetadimi?»")
    pg.click('.sheet [data-h="1"]'); pg.wait_for_timeout(200)
    ok('solishtir' in pg.inner_text('#bzyh') and pg.locator('.sheet [data-h="1"][disabled]').count() == 1, "Noto'g'ri «Ha» → maslahat")
    pg.click('.sheet [data-h="0"]'); pg.wait_for_timeout(250)
    ok(pg.locator('.sheet').count() == 0 and not T(t1, "t.tolandi") and T(t1, "[t.savol.n, t.savol.ok]") == [1, 0], "«Yo'q» to'g'ri → kassadan qaytdi, to'lanmadi; savol 0/1")
    tanla('i3', 0); tanla('i1', 0)  # olma 10 000, non 2×3000 → 12000+12000+... = 6000+12000+10000+16000+10000 = 54 000
    ok(T(t1, "BJ.A.bozor.jami(t)") == 54000, "Arzonroq tanlandi → 54 000")
    pg.click('[data-kassa]'); pg.wait_for_timeout(250); pg.click('.sheet [data-h="1"]'); pg.wait_for_timeout(300)
    ok("Oila pulidan to'la" in pg.inner_text('.sheet') and pg.locator('.sheet .tl2 [data-v="20000"]').count() == 1, "To'lov varag'i: «Oila pulidan to'la», oila kupyuralari")
    narx, ber = tolash()
    ok(narx == 54000 and ber == 60000 and pg.locator('.sheet [data-ok]:not([disabled])').count() == 1, f"Kupyuralar berildi: {ber} / {narx}")
    pg.click('.sheet [data-ok]'); pg.wait_for_timeout(400)
    ok(T(t1, "[t.tolandi, t.sarf]") == [True, 54000] and X(R, "A.pul.st(b).h") >= h0, "To'landi 54 000 — bola hamyonidan yechilmadi")
    ok(X(R, "A.readLog(b.id, A.todayKey()).filter(e=>e.t==='pul'&&e.tur==='xarid').length") == 0, "Bola hamyonidan «xarid» logi yo'q")
    # xohish javoni: qoldi 6 000 → kola 7 000 va chips 8 000 sig'maydi → javon yo'q → to'g'ridan-to'g'ri chek
    ok(ev("location.hash") == '#bozor' and pg.locator('.bzchek').count() == 1, "Qoldi 6 000 — xohish sig'maydi → darhol chek")
    ok(T(t1, "[t.holat, t.natija.qoldi, t.natija.tej, t.natija.oila]") == ['tugadi', 6000, 3000, 3000], "Chek: qoldi 6 000 → tejash 3 000 hamyonga, 3 000 oilaga")
    ok(X(R, "A.pul.st(b).h") == h0 + 3000 and X(R, f"b.bozor.tej[A.isoWeek()]") == 3000, "Hamyonga +3 000 (tejash), haftalik hisob 3 000")
    ok(X(R, "A.readLog(b.id, A.todayKey()).some(e=>e.t==='pul'&&e.tur==='tejash'&&e.s===3000)") and X(R, "A.readLog(b.id, A.todayKey()).some(e=>e.t==='bozor'&&e.hodisa==='tugadi'&&e.arzon===3&&e.n===5)"), "Log: pul «tejash», bozor «tugadi» (arzon 3/5)")
    c = pg.inner_text('.bzchek'); ok('BILIMJON BOZORI' in c and '54 000' in c and '+3 000' in c, "Chek matni: jami, tejash")
    SHOT(pg, 'g1_chek')
    pg.click('[data-uy]'); pg.wait_for_timeout(300)
    ok(pg.locator('[data-bozor]').count() == 0, "Topshiriq tugadi — uyda bozor tugmasi yo'q")
    GO('bozor', 350); ok('topshirig\'i yo\'q' in pg.inner_text('body') and pg.locator('.bzchek').count() == 1, "#bozor → «topshiriq yo'q» + oxirgi chek")

    # ---- 2-topshiriq: xohish javoni (qoldi ko'p) → kola; haftalik tejash chegarasi
    t2 = mk(R, 50000, ROY1[:2])  # non + sut
    NAV('bozor', 350); pg.click('.bzkir [data-ok]'); pg.wait_for_timeout(200)
    tanla('i1', 0); tanla('i2', 0)  # 6000 + 9000 = 15 000 → qoldi 35 000
    pg.click('[data-kassa]'); pg.wait_for_timeout(250); pg.click('.sheet [data-h="1"]'); pg.wait_for_timeout(300); tolash(); pg.click('.sheet [data-ok]'); pg.wait_for_timeout(400)
    ok(pg.locator('.bzxh').count() == 2 and pg.locator('[data-ol="muzqaymoq"]').count() == 0, "Xohish javoni: kola va chips (narxsiz muzqaymoq ko'rinmaydi)")
    tx = pg.inner_text('.bzxh:has([data-ol="kola"])')
    ok('Kola = 7 000' in tx and '0 so\'mlik' not in tx, f"Kola narxi; haftalik chegara qolgani 2 000 → voz kechish matni: {tx.strip()[:80]}")
    ok("+2 000" in pg.inner_text('[data-tej]'), "«Yo'q, tejayman (+2 000)» — haftalik chegara (5 000 − 3 000)")
    w = W390(); ok(w[0] <= 390, f"390 px: xohish javoni {w}")
    SHOT(pg, 'g1_xohish')
    pg.click('[data-ol="kola"]'); pg.wait_for_timeout(300)
    tolash(); pg.click('.sheet [data-ok]'); pg.wait_for_timeout(400)
    ok(T(t2, "[t.holat, t.xoh && t.xoh.k, t.natija.qoldi, t.natija.tej]") == ['tugadi', 'kola', 28000, 2000], "Kola olindi: qoldi 28 000, tejash 2 000 (chegara)")
    ok(X(R, "b.bozor.xoh[A.isoWeek()]") == 1 and X(R, "b.bozor.tej[A.isoWeek()]") == 5000, "Haftalik: xohish ishlatildi, tejash 5 000 (to'ldi)")
    ok('Kola' in pg.inner_text('.bzchek') and 'xohish' in pg.inner_text('.bzchek'), "Chekda xohish qatori")
    # ---- 3-topshiriq shu hafta: xohish yo'q, tejash 0
    t3 = mk(R, 30000, ROY1[:1])
    NAV('bozor', 350); pg.click('.bzkir [data-ok]'); pg.wait_for_timeout(200); tanla('i1', 0)
    pg.click('[data-kassa]'); pg.wait_for_timeout(250); pg.click('.sheet [data-h="1"]'); pg.wait_for_timeout(300); tolash(); pg.click('.sheet [data-ok]'); pg.wait_for_timeout(400)
    ok(pg.locator('.bzxh').count() == 0 and T(t3, "[t.holat, t.natija.tej, t.natija.oila]") == ['tugadi', 0, 24000], "Shu hafta 2-marta: xohish javoni yo'q, tejash chegarasi to'lgan → hammasi oilaga")

    # ================= 👶 MAKTABGACHA: sanash + avtomatik to'lov =================
    setj(K); hk = X(K, "A.pul.st(b).h"); tk0 = mk(K, 27000, ROY0)
    NAV('uy'); ok(pg.locator('[data-bozor]').count() == 1, "Maktabgacha: uyda bozor tugmasi")
    pg.click('[data-bozor]'); pg.wait_for_timeout(350); pg.click('.bzkir [data-ok]'); pg.wait_for_timeout(200)
    ok('Qoladi' not in pg.inner_text('.bzham'), "g0: hamyonda «Qoladi» raqami yo'q (sodda)")
    pg.click('[data-it="k1"]'); pg.wait_for_timeout(200)
    ok(pg.locator('.sheet .bztg .tanga').count() == 1 + 3, "g0 variantlari tangalar bilan (arzon 1, qimmat 3)")
    pg.click('.sheet [data-v="1"]'); pg.wait_for_timeout(250)
    ok(pg.locator('.sheet .bzsnq').count() == 1 and '3 ta sol' in pg.inner_text('.sheet'), "Variant tanlandi → «Savatga 3 ta sol!»")
    for _ in range(2): pg.click('.sheet [data-tap]'); pg.wait_for_timeout(80)
    ok(pg.inner_text('.sheet .bzsn').strip() == '2 / 3' and pg.locator('.sheet .bzsav .bzi').count() == 2, "Sanash: 2 / 3, savatda 2 ta rasm")
    SHOT(pg, 'g0_sanash')
    pg.click('.sheet [data-tap]'); pg.wait_for_timeout(300)
    ok(T(tk0, "t.son.k1") == 3 and pg.locator('.sheet').count() == 0 and pg.locator('[data-it="k1"].ok').count() == 1, "3 ta sanaldi → yopildi, ✓")
    pg.click('[data-it="k2"]'); pg.wait_for_timeout(200); pg.click('.sheet [data-v="0"]'); pg.wait_for_timeout(250)
    pg.click('.sheet [data-tap]'); pg.wait_for_timeout(100)
    ev("BJ.A.closeSheets ? BJ.A.closeSheets() : document.querySelector('.scrim').remove()"); pg.wait_for_timeout(200); ev("BJ.A.render()"); pg.wait_for_timeout(250)
    ok(pg.locator('[data-it="k2"].yarim').count() == 1 and 'Sana: 1 / 2' in pg.inner_text('[data-it="k2"]') and pg.locator('[data-kassa][disabled]').count() == 1, "Sanash chala qoldi → kartada «Sana: 1 / 2», kassa yopiq")
    pg.click('[data-it="k2"]'); pg.wait_for_timeout(200)
    ok(pg.locator('.sheet .bzsnq').count() == 1, "Chala narsa bosilsa — sanash davom etadi")
    pg.click('.sheet [data-tap]'); pg.wait_for_timeout(300)
    pg.click('[data-it="k3"]'); pg.wait_for_timeout(200); pg.click('.sheet [data-v="1"]'); pg.wait_for_timeout(250); pg.click('.sheet [data-tap]'); pg.wait_for_timeout(300)
    # 3×5000 + 2×2000 + 9000 = 28 000 > 27 000
    pg.click('[data-kassa]'); pg.wait_for_timeout(250)
    ok(not T(tk0, "t.tolandi") and pg.locator('.sheet').count() == 0, "g0: pul yetmasa kassa ochilmaydi (toast)")
    pg.click('[data-it="k1"]'); pg.wait_for_timeout(200); pg.click('.sheet [data-v="0"]'); pg.wait_for_timeout(250)
    for _ in range(3): pg.click('.sheet [data-tap]'); pg.wait_for_timeout(80)
    pg.wait_for_timeout(250)
    # 9000 + 4000 + 9000 = 22 000 > 20 000 → qatiq arzon
    pg.click('[data-it="k3"]'); pg.wait_for_timeout(200); pg.click('.sheet [data-v="0"]'); pg.wait_for_timeout(250); pg.click('.sheet [data-tap]'); pg.wait_for_timeout(300)
    ok(T(tk0, "BJ.A.bozor.jami(t)") == 19000, "g0 savat 19 000")
    pg.click('[data-kassa]'); pg.wait_for_timeout(300)
    ok(pg.locator(".sheet [data-ok]").count() == 1 and "To'layman" in pg.inner_text('.sheet') and pg.locator('.sheet .tl2').count() == 0, "g0: avtomatik to'lov varag'i (kupyura tanlash yo'q)")
    pg.click('.sheet [data-ok]'); pg.wait_for_timeout(400)
    # qoldi 8 000 → xohish javoni: kola 7 000, chips 8 000; tejash 4 000
    ok(pg.locator('.bzxh').count() == 2 and '+4 000' in pg.inner_text('[data-tej]'), "g0: qoldi 8 000 → xohish javoni, «tejayman (+4 000)»")
    tx = pg.inner_text('.bzxh:has([data-ol="chips"])'); tk = pg.inner_text('.bzxh:has([data-ol="kola"])')
    ok("8 000 so'm + 4 000 so'mlik tejash mukofotidan voz kechish" in tx and "3 500 so'mlik" in tk, f"«chips = N so'm + M so'mlik tejash mukofotidan voz kechish»: {tx.strip()[:90]} | {tk.strip()[-60:]}")
    SHOT(pg, 'g0_xohish')
    pg.click('[data-ol="chips"]'); pg.wait_for_timeout(300)
    ok("To'layman" in pg.inner_text('.sheet'), "g0: xohish ham avtomatik to'lov")
    pg.click('.sheet [data-ok]'); pg.wait_for_timeout(400)
    ok(T(tk0, "[t.holat, t.xoh && t.xoh.k, t.natija.qoldi, t.natija.tej]") == ['tugadi', 'chips', 0, 0] and X(K, "A.pul.st(b).h") == hk, "g0: chips olindi → qoldi 0, tejash 0, bola hamyoni o'zgarmadi")

    # ================= 📘 2-SINF: birlik narxi savoli + qaytim =================
    setj(Q); tq = mk(Q, 70000, ROY2)
    NAV('bozor', 350); pg.click('.bzkir [data-ok]'); pg.wait_for_timeout(200)
    SHOT(pg, 'g2_royxat')
    pg.click('[data-it="q1"]'); pg.wait_for_timeout(250)
    ok('Qaysi biri arzon' in pg.inner_text('.sheet') and pg.locator('.sheet [data-q]').count() == 3, "Guruch: «🧮 Qaysi biri arzon?» — 3 qadoq")
    pg.click('.sheet [data-q="1"]'); pg.wait_for_timeout(200)
    h = pg.inner_text('#bzqh'); ok('1 kg' in h and '13 000' in h and '11 500' in h, f"Noto'g'ri → maslahat: 1 kg ga keltirish {h[:120]}")
    pg.click('.sheet [data-q="2"]'); pg.wait_for_timeout(300)
    ok(pg.locator('.sheet .bzvar[data-v]').count() == 3 and T(tq, "[t.savol.n, t.savol.ok, t.savol.q.q1]") == [1, 0, 1], "2-urinishda to'g'ri → variantlar varag'i; savol 0/1")
    ok('2 × 12 000 = 24 000' in pg.inner_text('.sheet') and '4 × 6 500 = 26 000' in pg.inner_text('.sheet'), "Qator hisobi: 2 × 12 000, 4 × 6 500")
    pg.click('.sheet [data-v="2"]'); pg.wait_for_timeout(250)  # 2 kg qop 23 000
    pg.click('[data-it="q1"]'); pg.wait_for_timeout(250)
    ok('Qaysi biri arzon' not in pg.inner_text('.sheet'), "Savol bir marta — qayta ochilganda so'ralmaydi")
    pg.click('.sheet [data-x]'); pg.wait_for_timeout(150)
    for iid, vi in (('q2', 1), ('q3', 1), ('q4', 1), ('q5', 1), ('q6', 1)): tanla(iid, vi)
    # 23000 + 9000 + 8000 + 7000 + 3000 + 25000 = 75 000 > 70 000
    pg.click('[data-kassa]'); pg.wait_for_timeout(250)
    ok(not T(tq, "t.tolandi") and pg.locator('.sheet').count() == 0, "g2: byudjetdan oshsa — kassa ochilmaydi")
    pg.click('[data-it="q6"]'); pg.wait_for_timeout(200)
    ok('byudjetdan oshadi' in pg.inner_text('.sheet .bzvar[data-v="1"]'), "g2: qimmat variantda «byudjetdan oshadi»")
    pg.click('.sheet [data-v="0"]'); pg.wait_for_timeout(250)  # 65 000
    pg.click('[data-kassa]'); pg.wait_for_timeout(300)
    narx, ber = tolash(); pg.click('.sheet [data-ok]'); pg.wait_for_timeout(250)
    qt = ber - narx
    ok(narx == 65000 and pg.locator('.sheet [data-q]').count() >= 2 and 'qancha qaytaradi' in pg.inner_text('.sheet'), f"g2: qaytim savoli ({ber} − {narx})")
    pg.click(f'.sheet [data-q="{qt}"]'); pg.wait_for_timeout(400)
    ok(T(tq, "[t.tolandi, t.sarf]") == [True, 65000], "Qaytim to'g'ri → to'landi")
    # qoldi 5 000 → xohish (kola 7 000) sig'maydi → chek; g2 chegarasi 5 000, tejash 2 500
    ok(T(tq, "[t.holat, t.natija.tej]") == ['tugadi', 2500], "g2: chek, tejash 2 500")
    w = W390(); ok(w[0] <= 390, f"390 px: chek {w}")
    SHOT(pg, 'g2_chek')

    # ---- ota-ona: cheklar
    ev("BJ.A.otaOk={rol:'admin',t:Date.now()}"); GO('ota-bozor', 400)
    ok(pg.locator('.bzdt').count() == 5, f"Panel: 5 ta chek ({pg.locator('.bzdt').count()})")
    pg.click('.bzdt >> nth=0'); pg.wait_for_timeout(150)
    ok('Arzonini tanladi' in pg.inner_text('.bzdt >> nth=0') and pg.locator('.bzdt[open] .bzchek').count() == 1, "Chek ochiladi: «Arzonini tanladi», chek ichida")
    SHOT(pg, 'ota_cheklar')
    # bekor qilish
    t4 = mk(K, 20000, ROY0); GO('ota', 200); GO('ota-bozor', 350)
    pg.click(f'[data-del="{t4}"]'); pg.wait_for_timeout(200); pg.click('.sheet [data-ha]'); pg.wait_for_timeout(300)
    ok(ev(f"BJ.A.bozor.bz().top.some(t=>t.id==='{t4}')") is False, "Faol topshiriq bekor qilindi")
    # sozlama o'chirildi
    mk(K, 20000, ROY0); pg.click('#bzon'); pg.wait_for_timeout(250)
    ok(ev("BJ.A.S().sozlama.bozor") is False, "Bozor o'chirildi (sozlama)")
    setj(K); NAV('uy'); ok(pg.locator('[data-bozor]').count() == 0, "O'chiq: uyda tugma yo'q")
    GO('bozor', 300); ok(ev("location.hash") == '#uy', "O'chiq: #bozor → uyga")
    ev("BJ.A.S().sozlama.bozor = true; BJ.A.save(true)")
    # arxiv chegarasi
    r = ev("""(()=>{const Z=BJ.A.bozor, z=Z.bz(); for(let i=0;i<20;i++) z.top.push({id:'x'+i,kim:'q',byu:1,roy:[],holat:'tugadi',tugadiTs:i,sav:{},son:{},savol:{n:0,ok:0,q:{}}});
      const b=BJ.A.bola(); const t=Z.faol(b); t.tolandi=true; t.sarf=t.byu; Z.yakun(b,t); return z.top.filter(t=>t.holat==='tugadi').length})()""")
    ok(r == 12, f"Cheklar arxivi ≤ 12 ({r})")
    # uyqu vaqti / kun chegarasi: bozor ham tekshiriladi
    ok(ev("document.documentElement.outerHTML.includes('qutqar-|zal|bozor)/.test(h)')") and ev("document.documentElement.outerHTML.includes('zal-|bozor)/;')"), "Router: bozor kun chegarasi/uyqu tekshiruvida; bulutda faol ekran")

    ok(not [e for e in ERR if e.startswith('pageerror')], "Sahifa xatosiz (pageerror yo'q)")
    br.close()
finally:
    srv.terminate()
print('\nJAMI XATO:', len(ERR))
for e in ERR: print(' -', e)
sys.exit(1 if ERR else 0)
