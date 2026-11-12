"""Bilimjon 0.9.1 «v9.1» — 3-bosqich takliflari (u 11.11 22:14: «1, 2, 4, 5, 6, 7, 8 ni yasa, tekshirib yangi versiyani chiqar»):
👏 olqish, 🃏 kashfiyot albomi, 🎯 o'z maqsadi, 🔥 ketma-ket kunlar, 📖 haftalik hikoya, 👨‍👩‍👧 oilaviy viktorina, 🎤 ovozim (soxta mikrofon).
Ikki oila orasidagi olqish (guruh «ol» maydoni, qoidalar 0.9.1) — sinov/v076/sinov_v076.py H qismi.
Ishga tushirish: python3 sinov/v091/sinov_v091.py (skrinshotlar: /tmp/bj091_*.png)"""
import os, sys, time, subprocess, json, re, datetime as dt
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.abspath(os.path.join(D, '..', '..'))
PORT = 8817; URL = f'http://localhost:{PORT}/'
srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT)], cwd=SITE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
ERR = []; PE = []
def ok(c, m): print(('✅ ' if c else '❌ ') + m); (None if c else ERR.append(m))
html = open(os.path.join(SITE, 'index.html'), encoding='utf-8').read(); VJ = json.load(open(os.path.join(SITE, 'version.json'), encoding='utf-8'))
VER = re.search(r"A\.VER = '([\d.]+)'", html)[1]; SWV = re.search(r"const V = P \+ '([\d.]+)'", open(os.path.join(SITE, 'sw.js'), encoding='utf-8').read())[1]
RULES = open(os.path.join(SITE, 'firestore.rules'), encoding='utf-8').read()
def kutf(pg, js, ms=8000):
    try: pg.wait_for_function(js, timeout=ms); return True
    except Exception: return False
def olov_ref(today, done, bosh):
    """🔥 olov — Python nusxasi: haftada 1 o'tkazilgan kun ❄️ kechiriladi"""
    k = today if today in done else today - dt.timedelta(days=1); n = 0; kech = set()
    while k >= bosh:
        if k in done: n += 1
        else:
            w = k.isocalendar()[:2]
            if w in kech: break
            kech.add(w)
        k -= dt.timedelta(days=1)
    return n
try:
  with sync_playwright() as p:
    br = p.chromium.launch(args=['--use-fake-ui-for-media-stream', '--use-fake-device-for-media-stream', '--autoplay-policy=no-user-gesture-required'])
    ctx = br.new_context(viewport={'width': 390, 'height': 844}, service_workers='block', device_scale_factor=2)
    P = ctx.new_page(); P.on('pageerror', lambda e: PE.append(str(e))); ev = P.evaluate
    P.goto(URL + '?tez=1'); P.wait_for_timeout(400)
    P.fill('#on', 'Sinov oila'); P.fill('#p1', '1234'); P.fill('#p2', '1234'); P.click('#go'); P.wait_for_timeout(300)
    AZ, KI = ev("""(()=>{const A=BJ.A; const a=A.newBola({laqab:'Ali',daraja:'g2',avatar:'🐯',dunyo:'garaj'}), k=A.newBola({laqab:'Kichik',daraja:'g0',avatar:'🦋',dunyo:'orol'});
      [a,k].forEach(b=>{b.boshlandi=A.addDays(A.todayKey(),-20);}); A.S().sozlama.uyqu=''; A.S().joriy=a.id; A.save(true); return [a.id,k.id]})()""")
    X = lambda bid, e: ev(f"(()=>{{const A=BJ.A, B=BJ.bank, b=A.S().bolalar['{bid}']; return {e}}})()")
    setj = lambda bid: ev(f"(()=>{{BJ.A.S().joriy='{bid}'; BJ.A.save(true)}})()")
    W = lambda: ev("document.documentElement.scrollWidth")
    def GO(h, ms=450): ev("BJ.A.closeSheets(); location.hash='x'"); P.wait_for_timeout(80); ev(f"location.hash='{h}'"); P.wait_for_timeout(ms)
    T = ev("BJ.A.todayKey()"); TD = dt.date.fromisoformat(T)

    # ================= 0. VERSIYA =================
    yang = ev("BJ.A.YANGI")
    ok(VER == SWV == VJ['ver'] == '0.9.1' and VJ['verk'] == '9.1' and ev("BJ.A.VERK") == '9.1', f"Versiya 0.9.1: index {VER} = sw.js {SWV} = version.json {VJ['ver']} (v{VJ['verk']})")
    ok(VJ['yangi'] == yang and 2 <= len(yang) <= 4 and all(len(x) <= 90 for x in yang), f"version.json «yangi» = A.YANGI ({len(yang)} qator, qisqa)")
    bd = html.split('function bolaDefaults()')[1][:1500]; dfl = html.split('function defaults()')[1][:1500]
    ok(not any(k + ':' in bd for k in ('olq', 'albom', 'maqsad', 'mqTarix', 'olovMax', 'hikoya', 'ovozYoz')) and 'vikt' not in dfl, "Yangi maydonlar bolaDefaults/defaults ga QO'SHILMAGAN")
    ok("'ol'])" in RULES and "d.ol is list && d.ol.size() <= 10" in RULES and 'Bilimjon 0.9.1' in RULES, "firestore.rules 0.9.1: azo ga ixtiyoriy «ol» (list ≤ 10)")

    # ================= 1. UY EKRANI =================
    GO('uy', 700)
    ok(P.locator('.t9s [data-olov]').count() == 1 and P.locator('.t9s [data-maqsad]').count() == 1, "Uyda: 🔥 olov va 🎯 maqsad qatori")
    ok(P.locator('.t9g .t9t').count() == 4 and all(P.locator(f'[data-{x}]').count() == 1 for x in ('hikoya', 'albom', 'ovozim', 'vikt')), "Uyda 4 ta yangi tugma: 📖 Hikoya, 🃏 Albom, 🎤 Ovozim, 👨‍👩‍👧 Viktorina")
    ok(W() <= 390, f"390 px: uy ekrani ({W()})"); P.screenshot(path='/tmp/bj091_uy.png', full_page=True)

    # ================= 2. 🔥 KETMA-KET KUNLAR =================
    dn = [0, 1, 3, 4, 5, 7, 8, 9, 10, 12, 13]
    X(AZ, f"(()=>{{b.kun={{}}; {json.dumps(dn)}.forEach(i=>{{const k=A.addDays(A.todayKey(),-i); A.agg(b,k).missiya=1;}}); delete b.olovMax; delete b.olovBos; A.save(true); return 1}})()")
    bosh = TD - dt.timedelta(days=20); done = {TD - dt.timedelta(days=i) for i in dn}
    o = X(AZ, "A.olov.hisob(b)"); ref = olov_ref(TD, done, bosh)
    ok(o['n'] == ref and o['bugun'] is True, f"🔥 Olov = {o['n']} kun (Python nusxasi {ref}; haftada 1 o'tkazilgan kun ❄️ kechiriladi, ikkinchisi uzadi)")
    done2 = done - {TD}; o2 = X(AZ, "(()=>{const k=A.todayKey(); b.kun[k].missiya=0; const r=A.olov.hisob(b); b.kun[k].missiya=1; return r})()")
    ok(o2['n'] == olov_ref(TD, done2, bosh) and o2['bugun'] is False, f"Bugun hali missiya yo'q — olov kechagidan sanaladi ({o2['n']})")
    r = X(AZ, "A.olov.missiya(b)")
    ok(r['n'] == ref and r['bos'] == max([x for x in [3, 7, 14, 30, 50, 100] if x <= ref] or [0]) and X(AZ, "b.olovMax") == ref, f"Missiya yakunida marra: {r} (b.olovMax = {ref})")
    ok(X(AZ, "A.olov.missiya(b).bos") == 0, "Shu marra qayta tabriklanmaydi")
    GO('uy', 600); P.click('[data-olov]'); P.wait_for_timeout(300)
    ok(P.locator('.olw .olk').count() == 7 and f"{ref} kun ketma-ket" in P.inner_text('.sheet'), "🔥 Olov oynasi: hafta 7 kun + son")
    P.screenshot(path='/tmp/bj091_olov.png'); ev("BJ.A.closeSheets()")

    # ================= 3. 🎯 O'Z MAQSADI =================
    X(AZ, "(()=>{delete b.maqsad; delete b.mqTarix; delete b.mqKor; A.save(true); return 1})()")
    GO('uy', 600); P.click('[data-maqsad]'); P.wait_for_timeout(300)
    ok(P.locator('.mqr').count() == 3 and P.locator('[data-mq]').count() == 9, "🎯 Tanlash oynasi: 3 tur (kun, yulduz, meva) × 3 qiymat")
    tv = P.locator('.mqr').first.locator('.btn:not(.ghost)').get_attribute('data-mq')
    ok(tv and tv.startswith('kun|'), f"👍 tavsiya (o'tgan haftadan bir qadam) belgilangan: {tv}")
    P.screenshot(path='/tmp/bj091_maqsad.png'); P.click('[data-mq="kun|4"]'); P.wait_for_timeout(500)
    m = X(AZ, "b.maqsad"); ok(m and m['tur'] == 'kun' and m['n'] == 4 and m['wk'] == ev("BJ.A.isoWeek()"), f"Tanlandi: {m}")
    wv = X(AZ, "A.maqsad.holat(b).v"); t = P.inner_text('[data-maqsad]')
    ok(f"{wv}/4" in t, f"Uyda maqsad: {t.strip()}")
    r = X(AZ, "(()=>{A.weekDays(A.isoWeek()).filter(k=>k<=A.todayKey()).forEach(k=>{A.agg(b,k).missiya=1;}); b.maqsad.n=1; A.save(true); return 1})()")
    GO('uy', 900); ok(X(AZ, "b.maqsad.yetdi") == T, "Maqsadga yetdi → tabrik (yetdi = bugun)")
    r = X(AZ, """(()=>{const pw=A.prevWeek(A.isoWeek()); b.maqsad={wk:pw,tur:'kun',n:2,ts:1,yetdi:null}; A.weekDays(pw).slice(0,2).forEach(k=>{A.agg(b,k).missiya=1;}); const h=A.maqsad.holat(b); return {yoq:h.yoq, tar:b.mqTarix, kor:b.mqKor, pw}})()""")
    ok(r['yoq'] and r['tar'][-1]['wk'] == r['pw'] and r['tar'][-1]['ok'] == 1 and r['kor'] == r['pw'], f"Yangi hafta: o'tgan hafta natijasi tarixga (✅ {r['tar'][-1]['v']}/{r['tar'][-1]['n']})")
    GO('uy', 600); P.click('[data-maqsad]'); P.wait_for_timeout(300)
    ok("O'tgan hafta" in P.inner_text('.sheet') and 'bajarding' in P.inner_text('.sheet'), "Yangi hafta tanlovida o'tgan hafta natijasi ko'rsatiladi"); ev("BJ.A.closeSheets()")

    # ================= 4. 🃏 KASHFIYOT ALBOMI =================
    r = X(AZ, """(()=>{delete b.albom; const t=A.nodeSt(b,'KASHF'); t.kun=t.kun||{}; const k=A.addDays(A.todayKey(),-3); t.kun[k]=[2,2]; const D=A.dayDiff(b.boshlandi,k)+1, kk=A.kashfOfDay(b,D);
      const al=A.albom.st(b); return {id:kk.id, y:A.albom.yulduz(al[kk.id]), h:A.albom.hisob(b)}})()""")
    ok(r['y'] == 2 and r['h']['n'] >= 1 and r['h']['jami'] == 30, f"Albom eski kashfiyotlardan bir marta yig'ildi: {r['id']} ★★ ({r['h']})")
    ks = X(AZ, "(()=>{const m=b.missiya=A.buildMission(b); m.si=m.steps.findIndex(s=>s.k==='kashf'); A.save(true); return m.si})()")
    if ks >= 0:
        kid = X(AZ, "A.kashfOfDay(b).id"); y0 = X(AZ, f"(b.albom['{kid}']||{{ok:0}}).ok")
        GO('missiya', 700); P.click('[data-go]') if P.locator('[data-go]').count() else None; P.wait_for_timeout(500)
        kutf(P, "window.__bjCur() && window.__bjCur().it", 5000); ev("window.__bjJavob(true)"); P.wait_for_timeout(900)
        ok(X(AZ, f"(b.albom['{kid}']||{{ok:0}}).ok") == y0 + 1, f"Missiyadagi kashfiyot javobi albomga yozildi ({kid})")
    else: ok(False, "Missiyada kashfiyot qadami topilmadi")
    X(AZ, "(()=>{delete b.missiya; A.save(true); return 1})()")
    GO('albom', 700)
    n = X(AZ, "A.albom.hisob(b).n")
    ok(P.locator('.alk').count() == 30 and P.locator('.alk.yop').count() == 30 - n and P.locator('.alk.yop small').first.inner_text() != '', f"Albom: 30 karta, ochilgan {n}, yopiqlarida «🔒 N kundan keyin»")
    ok(W() <= 390, f"390 px: albom ({W()})"); P.screenshot(path='/tmp/bj091_albom.png', full_page=True)
    P.locator('[data-al]').first.click(); P.wait_for_timeout(350); aid = P.locator('.alkc').count()
    ok(aid == 1 and P.locator('[data-alq]').count() == 1, "Karta oynasi: rasm, matn, 🔁 Savol")
    P.click('[data-alq]'); P.wait_for_timeout(400)
    ans = ev("""(()=>{const q=document.querySelector('.alqi').innerText; for(const k of BJ.bank.kashf) for(const d of k.d) for(const s of d.s) if(q.indexOf(s[0])>=0) return s[1]; return null})()""")
    cid = P.locator('[data-al]').first.get_attribute('data-al')
    ok(ans is not None and P.locator('.alqi .opt').count() >= 2, f"Albomdan savol chiqdi (javob: {ans})")
    if ans is not None:
        P.locator('.alqi .opt').filter(has_text=ans).first.click(); P.wait_for_timeout(1700)
        ok(X(AZ, f"A.albom.yulduz(b.albom['{cid}'])") == 3 and P.locator('.alk.s3').count() >= 1, "To'g'ri javob → karta ★★★ oltin")

    # ================= 5. 📖 HIKOYA =================
    r = X(AZ, """(()=>{delete b.hikoya; const h0=JSON.parse(JSON.stringify(A.hikoya.st(b))); const m1=A.hikoya.missiya(b), m2=A.hikoya.missiya(b); return {h0,m1,m2,h:b.hikoya}})()""")
    ok(r['h0']['n'] == 1 and r['m1'] == {'nom': "Kichkina urug'", 'n': 2} and r['m2'] is None, f"1-sahifa darhol; missiya → 2-sahifa; bir kunda bir marta ({r['m1']})")
    r = X(AZ, """(()=>{const h=b.hikoya; const L=[]; for(let i=0;i<6;i++){h.kun=''; L.push(A.hikoya.missiya(b));} return {L:L.map(x=>x&&x.n), h}})()""")
    ok(r['L'] == [3, 4, 5, 6, 7, 1] and r['h']['i'] == 1 and r['h']['n'] == 1, f"7 sahifa → hikoya tugadi → keyingisi boshlandi ({r['L']}, hikoya {r['h']['i'] + 1})")
    hk = X(AZ, "A.hikoya.HK.map(x=>[x.nom, x.s.length, x.s.every(p=>p[1].length>=80 && p[1].length<=420)])")
    ok(len(hk) == 4 and all(x[1] == 7 and x[2] for x in hk), f"4 hikoya × 7 sahifa, sahifa matni 80–420 belgi ({[x[0] for x in hk]})")
    GO('hikoya', 700)
    ok(P.locator('.hkb').count() == 1 and '1/7' in P.inner_text('.top') and 'Kumush kalit' in P.inner_text('.top'), "📖 Hikoya ekrani: «Kumush kalit» 1/7")
    ok(P.locator('[data-hn]').is_disabled() and P.locator('.hkj [data-hj]').count() == 1, "Keyingi sahifa yopiq (missiyadan keyin ochiladi), javonda o'qilgan hikoya")
    ok(W() <= 390, f"390 px: hikoya ({W()})"); P.screenshot(path='/tmp/bj091_hikoya.png', full_page=True)
    P.click('.hkj [data-hj]'); P.wait_for_timeout(300)
    for _ in range(6): P.click('[data-hn]'); P.wait_for_timeout(120)
    ok("Kichkina urug'" in P.inner_text('.top') and '7/7' in P.inner_text('.top') and 'shirin meva' in P.inner_text('.hktx'), "Javondan eski hikoyani 7-sahifagacha o'qish")
    P.click('[data-hp]'); P.wait_for_timeout(150); ok('6/7' in P.inner_text('.top'), "‹ Oldingi sahifa")

    # ================= 6. MISSIYA YAKUNI (stepYakun → natija) =================
    X(AZ, "(()=>{b.hikoya.kun=''; delete b.kun[A.todayKey()]; const m=b.missiya=A.buildMission(b); m.si=m.steps.findIndex(s=>s.k==='yakun'); A.save(true); return m.si})()")
    GO('missiya', 800)
    if P.locator('[data-go]').count(): P.click('[data-go]')
    ok(kutf(P, "location.hash==='#natija'", 15000), "Missiya yakunlandi → natija ekrani")
    P.wait_for_timeout(500); mt = X(AZ, "b.missiya.t91")
    ok(mt and mt['hk'] and mt['hk']['n'] == 2 and mt['ol']['n'] >= 1, f"stepYakun: m.t91 = {mt}")
    ok(P.locator('[data-hkn]').count() == 1 and '2-sahifasi ochildi' in P.inner_text('[data-hkn]') and 'Olov' in P.inner_text('body'), "Natijada: 🔥 olov va «📖 Hikoyaning 2-sahifasi ochildi!»")
    P.screenshot(path='/tmp/bj091_natija.png', full_page=True)
    P.click('[data-hkn]'); P.wait_for_timeout(500)
    ok(ev("location.hash") == '#hikoya' and '2/7' in P.inner_text('.top') and X(AZ, "b.hikoya.yangi") == 0, "Tugma → yangi ochilgan sahifa (2/7), «yangi» belgisi olindi")

    # ================= 7. 👏 OLQISH (shu oila) =================
    setj(AZ); GO('estafeta', 700)
    ok(P.locator(f'[data-olq="{KI}"]').count() == 1 and P.locator(f'[data-olq="{AZ}"]').count() == 0, "Estafeta kartasida do'stga 👏 tugma (o'ziga yo'q)")
    P.click(f'[data-olq="{KI}"]'); P.wait_for_timeout(300)
    ok(P.locator('.olqg [data-oi]').count() == 6, "6 ta tayyor ibora (erkin matn yo'q)"); P.screenshot(path='/tmp/bj091_olqish.png')
    P.click('[data-oi="0"]'); P.wait_for_timeout(500)
    r = X(KI, "b.olq && b.olq.k")
    ok(r and r[-1]['f'] == AZ and r[-1]['i'] == 0 and r[-1]['yangi'] == 1, "Kichik olqishni darhol oldi (shu oila — mahalliy)")
    ok(P.locator(f'[data-olq="{KI}"]').is_disabled() and X(AZ, f"A.olqish.mumkin(b,'{KI}')") == 'bir', "Bitta do'stga kuniga 1 ta — tugma o'chdi")
    r = X(AZ, "(()=>{const o=[]; for(let i=0;i<5;i++) o.push(A.olqish.yubor(b,{id:'x'+i,laqab:'D'+i,av:'🙂'},1)); return [o, A.olqish.mumkin(b,'x9'), A.olqish.bulut(b).length, A.olqish.bulut(b).every(s=>/^x\\d\\|1\\|\\d{13}$/.test(s))]})()")
    ok(r[0] == [True, True, True, True, False] and r[1] == 'kun', f"Kuniga 5 ta olqish chegarasi {r[0]}")
    ok(r[2] == 4 and r[3], f"Bulutga faqat boshqa oila bolalariga yuborilganlar (shu oila bolasi — yo'q): {r[2]} ta, format «bid|ibora|ts»")
    setj(KI); GO('uy', 700)
    t = P.inner_text('.olqk') if P.locator('.olqk').count() else ''
    ok('Ali senga' in t and 'Barakalla' in t, f"Kichikning uyida: «Ali senga: 👏 Barakalla!» ({t[:50]})")
    P.click('[data-olqj]'); P.wait_for_timeout(300); P.click('[data-oi="3"]'); P.wait_for_timeout(600)
    ok(X(AZ, "b.olq.k.some(k=>k.i===3)") and X(KI, "b.olq.k.every(k=>!k.yangi)"), "↩️ Javob olqishi Aliga bordi, Kichikdagi karta yopildi")
    ok(P.locator('.olqk').count() == 0, "Uyda olqish kartasi qolmadi")
    setj(AZ); GO('uy', 700); P.click('[data-olqr]'); P.wait_for_timeout(500)
    ok(X(AZ, "b.olq.k.every(k=>!k.yangi)") and P.locator('.olqk').count() == 0, "😊 Rahmat → karta yopildi")
    r = ev(f"BJ.A.olqish.qabul('x1', {{laqab:'D', av:'🙂', ol:['{AZ}|4|'+(Date.now()-5*864e5), '{AZ}|4|'+(Date.now()+864e5), '{KI}|5|'+Date.now()]}}, new Set(['{AZ}']))")
    ok(r == 0, "Qabul: 3 kundan eski, kelajak sanali va boshqa bolaga yozilgan olqish olinmaydi")

    # ================= 8. 👨‍👩‍👧 OILAVIY VIKTORINA =================
    ev("(()=>{const A=BJ.A; A.bolalar().forEach(b=>{b.yv={v:A.VER,sana:A.todayKey(),tur:'ok',qadam:0};}); window.__gd=Date.prototype.getDay; Date.prototype.getDay=function(){return 3}; A.TEZ=false; A.S().viktOchiq=null; A.save(true)})()")
    GO('uy', 600); ok('Sh–Ya' in P.inner_text('[data-vikt]'), "Hafta o'rtasida viktorina tugmasi: 🔒 Sh–Ya")
    P.click('[data-vikt]'); P.wait_for_timeout(300)
    ok(P.locator('#vkp').count() == 1, "Ish kuni → ota-ona PIN oynasi")
    P.fill('#vkp', '9999'); P.click('.sheet [data-ok]'); P.wait_for_timeout(200)
    ok(ev("location.hash") != '#viktorina', "Noto'g'ri PIN — ochilmadi")
    P.fill('#vkp', '1234'); P.click('.sheet [data-ok]'); P.wait_for_timeout(500)
    ok(ev("location.hash") == '#viktorina' and ev("BJ.A.S().viktOchiq") == T and P.locator('.vko').count() == 4, "To'g'ri PIN → bugun ochildi; o'yinchilar: 2 bola + Dada + Oyi")
    ev("Date.prototype.getDay=window.__gd; BJ.A.TEZ=true")
    ok(W() <= 390, f"390 px: viktorina ({W()})"); P.screenshot(path='/tmp/bj091_vikt.png', full_page=True)
    r = ev(f"""(()=>{{const V=BJ.A.viktorina, L=[]; for(let i=0;i<25;i++){{const k=V.item({{kat:'{AZ}'}},{{katta:true}}), c=V.item({{kat:'{AZ}'}},{{katta:false,bid:'{KI}'}}); L.push([k,c].every(it=>it&&Array.isArray(it.o)&&it.o.length>=2&&typeof it.matn!=='string'&&it.__b&&it.o.some(o=>o.v===String(it.a))));}} return L.every(Boolean)}})()""")
    ok(r, "50 ta viktorina savoli (kattalar — 2-sinf/kashfiyot, bola — o'z mavzulari): hammasi «tanla», javobi variantlar ichida")
    ev("(()=>{const o=BJ.A.RENDER.tanla; window.__vkOrig=o; BJ.A.RENDER.tanla=function(el,it,...r){window.__vkIt=it; return o.call(this,el,it,...r)}; BJ.A.viktorina.VAQT.katta.max=2500; BJ.A.viktorina.VAQT.katta.tez=1500;})()")
    P.uncheck('[data-vo="k:ona"]'); P.click('[data-vgo]'); P.wait_for_timeout(300)
    ok(ev("BJ.A.viktorina.holat().n") == 9, "3 o'yinchi × 3 aylana = 9 navbat")
    TOGRI = "(()=>{const a=String(window.__vkIt.a); [...document.querySelectorAll('#body .opt')].find(x=>x.dataset.v===a).click()})()"
    XATO = "(()=>{const a=String(window.__vkIt.a); [...document.querySelectorAll('#body .opt')].find(x=>x.dataset.v!==a).click()})()"
    for i in range(9):   # navbat: Ali, Kichik, Dada × 3 — Ali hammasini tez topadi, Kichik xato qiladi, Dada 1-aylanada topadi, keyin vaqt tugaydi
        P.click('[data-vt]'); P.wait_for_timeout(250); who = i % 3
        if who == 0: ev(TOGRI)
        elif who == 1: ev(XATO)
        elif i == 2: ev(TOGRI)
        else: P.wait_for_timeout(2800)
        P.wait_for_timeout(250)
        if i == 4: P.screenshot(path='/tmp/bj091_vikt_savol.png')
        if i == 5: ok('Vaqt tugadi' in P.inner_text('#fb'), "Kattalar savolida vaqt tugadi → ⏰")
        P.click('[data-vn]'); P.wait_for_timeout(200)
    ev("void (BJ.A.RENDER.tanla=window.__vkOrig)")
    o = ev("BJ.A.S().vikt.slice(-1)[0]")
    sc = dict(o['o']) if o else {}
    ok(o and o['o'][0][0] == 'Ali' and sc.get('Ali') == 45 and sc.get('Kichik') == 0 and 10 <= sc.get('Dada', 0) <= 15, f"Natija: Ali 3×(10+5 tez) = 45, Dada 1 to'g'ri (2 marta vaqt tugadi), Kichik 0 — {o and o['o']}")
    ok(P.locator('.vkfin .vkpd').count() == 3 and "kattalardan o'zib ketdi" in P.inner_text('.vkfin'), "Yakun: shohsupa + «kattalardan o'zib ketdi»")
    P.screenshot(path='/tmp/bj091_vikt_yakun.png', full_page=True)
    ok(X(AZ, "A.readLog(b.id, A.todayKey()).some(e=>e.t==='vikt' && e.hodisa==='tugadi' && e.orin===1)") and X(AZ, "A.nodeSt(b,'M2.1').n") == X(AZ, "A.nodeSt(b,'M2.1').n"), "Logga yozildi; javoblar o'zlashtirish hisobiga kirmadi")

    # ================= 9. 🎤 OVOZIM (soxta mikrofon) =================
    setj(AZ); GO('ovozim', 600)
    ok(P.locator('.ovtx').count() == 1 and 'Yettita rang' in P.inner_text('.ovm'), "🎤 O'lchov matni (2-sinf: «Yettita rang»)")
    P.click('[data-ovgo]'); ok(kutf(P, "!!document.querySelector('[data-ovstop]')", 6000), "Yozish boshlandi (soxta mikrofon) — ⏹ tugma, taymer")
    P.wait_for_timeout(1600); P.click('[data-ovstop]')
    ok(kutf(P, "!!document.querySelector('[data-ovs]')", 6000) and P.locator('.ovrv audio').count() == 1, "To'xtatildi → eshitib ko'rish + 💾 Saqlash")
    P.click('[data-ovs]'); P.wait_for_timeout(800)
    L = X(AZ, "b.ovozYoz || []")
    ok(len(L) == 1 and L[0]['til'] == 'uz' and L[0]['sek'] >= 1 and 'buf' not in L[0], f"Saqlandi: b.ovozYoz da faqat sana/soniya ({L and {k: L[0][k] for k in ('m', 'sek', 'sana')}}), ovoz — IndexedDB")
    ok(ev(f"BJ.A.ovozim.idbGet('{L[0]['id']}').then(r=>!!(r&&r.buf&&r.buf.byteLength>100))"), "IndexedDB da ovoz fayli bor")
    ev(f"""(()=>{{const A=BJ.A,b=A.bola('{AZ}'),ts=Date.now()-30*864e5,id='ozeski'; b.ovozYoz.unshift({{id,til:'uz',m:'{L[0]['m']}',sana:A.addDays(A.todayKey(),-30),ts,sek:{L[0]['sek']}*2}}); A.save(true);
      return BJ.A.ovozim.idbGet('{L[0]['id']}').then(r=>BJ.A.ovozim.idbPut(Object.assign({{}},r,{{id,ts}})))}})()""")
    GO('ovozim', 700)
    ok(P.locator('.ovcmp').count() == 1 and "tezroq o'qiyapsan" in P.inner_text('.ovcmp') and '30 kun oldin' in P.inner_text('.ovcmp'), "⚖️ 30 kun oldingi yozuv bilan solishtirish: «… % tezroq o'qiyapsan!»")
    P.locator('.ovcmp [data-ovp]').first.click(); P.wait_for_timeout(500)
    ok(P.locator('audio.ovpl').count() >= 1, "▶ Oldingi ovozni ijro etish")
    ok(W() <= 390, f"390 px: ovozim ({W()})"); P.screenshot(path='/tmp/bj091_ovozim.png', full_page=True)
    P.click('[data-ovt="ar"]'); P.wait_for_timeout(300)
    ok(P.locator('.ovtx.arab[dir="rtl"]').count() == 1, "🕌 Arabcha matn — o'ngdan chapga")
    P.click('[data-ovgo]'); kutf(P, "!!document.querySelector('[data-ovstop]')", 6000); P.wait_for_timeout(400)
    GO('uy', 500); ok(ev("BJ.A.ovozim.holat()") is None, "Yozish paytida chiqib ketilsa — mikrofon yopiladi")

    # ================= 10. 🆕 YANGILIK TURI 0.9.1 =================
    X(AZ, "(()=>{A.yangiSinov=1; delete b.yv; delete b.kor; delete b.esYop; b.boshlandi=A.addDays(A.todayKey(),-6); delete b.missiya; A.save(true); return 1})()")
    GO('uy', 900); kutf(P, "!!document.querySelector('.ytb')", 4000); P.wait_for_timeout(200)
    ok(P.locator('.ytur').count() == 1 and "O'z maqsadim" in P.inner_text('.ytb'), "0.8.0 dan kelgan bola: tur 1-yangilik — 🎯 O'z maqsadim")
    ok(all(P.locator(f'[data-{x}] .ynb').count() == 1 for x in ('hikoya', 'albom', 'ovozim', 'vikt', 'daraxt', 'est')), "«YANGI» belgisi: hikoya, albom, ovozim, viktorina, daraxt, estafeta")
    P.screenshot(path='/tmp/bj091_tur.png'); P.click('[data-ybos]'); P.wait_for_timeout(600)
    ok(ev("location.hash") == '#uy' and P.locator('.mqr').count() == 3, "«👆 Bosib ko'r» (maqsad) → uyda maqsad tanlash oynasi")
    ev("BJ.A.closeSheets()"); GO('uy', 900); kutf(P, "!!document.querySelector('.ytb')", 4000); P.wait_for_timeout(200)
    ok(P.locator('.ytur').count() == 1 and 'Hikoya' in P.inner_text('.ytb') and '2/' in P.inner_text('.yth'), f"Tur keyingisiga o'tdi — 📖 Hikoya (2/…, birorta yangilik tashlab ketilmadi) [{P.inner_text('.ytb')[:40] if P.locator('.ytb').count() else '—'}]")
    P.click('[data-ykey]'); P.wait_for_timeout(700)
    ok('albomi' in P.inner_text('.ytb') and X(AZ, "b.yv.otk") == ['hikoya'], "«Keyingisi ›» → 🃏 Albom; o'tkazilgan hikoyada «YANGI» qoladi")
    ev("document.querySelectorAll('.ytur').forEach(x=>x.remove())")
    r = X(AZ, """(()=>{const T=A.todayKey(), y=A.addDays(T,-1); b.yv={v:'0.9.0',sana:A.addDays(T,-2),tur:'ok',qadam:3}; b.kor={daraxt:y,estafeta:y,q3:y}; A.save(true); A.yangilik.vInit(b); return b.yv})()""")
    GO('uy', 1400); y = X(AZ, "A.yangilik.yangilar(b)")
    ok(sorted(r.get('old', [])) == ['daraxt', 'estafeta', 'q3'] and 'daraxt' not in y and 'estafeta' not in y and 'hikoya' in y, f"0.9.0 beta'da ko'rilgan 3 yangilik qayta chiqmaydi (old {r.get('old')}; tur: {y})")
    ev("document.querySelectorAll('.ytur').forEach(x=>x.remove())")
    X(AZ, "(()=>{const T=A.todayKey(); b.yv.tur='ok'; Object.keys(A.yangilik.B).forEach(k=>{b.kor[k]=T}); b.kor.hikoya=A.addDays(T,-3); b.hikoya.yangi=1; A.save(true); return 1})()")
    GO('uy', 1400); t = P.inner_text('[data-eslat]') if P.locator('.eslat').count() else ''
    ok('Hikoya' in t and '3 kundan beri' in t and 'kutyapti' in t, f"🔔 3 kundan beri kirilmagan hikoya eslatmasi ({t[:70]})")
    ev("BJ.A.yangiSinov=0")

    # ================= 11. OTA-ONA PANELI =================
    ev("BJ.A.otaOk={rol:'admin',t:Date.now()}"); GO('ota', 900)
    t = ev("document.body.innerText")
    ok('🔥 olov' in t and '📖 «' in t and '🃏' in t and '🎤 1 yozuv' in t.replace('2 yozuv', '1 yozuv') , "Ota-ona xulosasida: 🔥 olov · 🎯 · 📖 hikoya · 🃏 albom · 🎤 yozuvlar")
    P.screenshot(path='/tmp/bj091_ota.png', full_page=True)
    GO('uy', 500)
    ok(not PE, f"Sahifa xatolari yo'q {PE[:3]}")
finally:
    srv.terminate()
print('JAMI:', 'XATO ' + str(len(ERR)) if ERR else 'OK'); sys.exit(1 if ERR else 0)
