"""Bilimjon 0.7.0 → 0.7.1 PROD sinovi (iPhone kengligi, haqiqiy ovoz fayllari, service worker yoqilgan).
1) 0.7.0 saytida oila + 3 bola + biroz o'yin; 2) xuddi shu manzilda 0.7.1 ga almashtirish (telefondagi yangilanish kabi);
3) har bola uchun to'liq missiya (tasodifiy javoblar); 4) hamma ekranlar; 5) tasodifiy bosishlar (monkey).
Ishlatish (chiqarishdan OLDIN): eski = hozirgi main, yangi = main + tarmoq birlashmasi (ovoz/ papkasi bilan):
  git worktree add /tmp/eski origin/main
  git worktree add /tmp/yangi -b chiqar origin/main && (cd /tmp/yangi && git merge --no-ff origin/<tarmoq>)
  python3 sinov/chiqarish/prod_e2e.py /tmp/eski /tmp/yangi        (MISSIYA_ONLY=1 — faqat 1–3-qism)
Server GitHub Pages kabi har faylga max-age=600 beradi (ghserve.py) — yangilanish 2-ochishda kelishi tekshiriladi.
07.11 (0.7.1 chiqarishi): 23 tekshiruv — hammasi o'tdi. 0.7.2 dan versiyalar fayllardan o'qiladi."""
import sys, os, time, random, subprocess, shutil, json
from playwright.sync_api import sync_playwright

OLD, NEW = sys.argv[1], sys.argv[2]
import re
def _ver(d): return re.search(r"A\.VER = '([\d.]+)'", open(os.path.join(d, 'index.html'), encoding='utf-8').read()).group(1)
VOLD, VNEW = _ver(OLD), _ver(NEW)
VK = lambda v: (lambda q: (q[0] + '.' + q[1]) if q[0] != '0' else q[1] + ('.' + q[2] if q[2] != '0' else ''))(v.split('.'))
PORT = 8850; URL = f'http://localhost:{PORT}/'
UDD = '/tmp/bj_prod_ctx'; shutil.rmtree(UDD, ignore_errors=True)
UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1'
random.seed(7)
ERR, NOTE = [], []
srv = None
def serve(d):
    global srv
    if srv: srv.terminate(); srv.wait()
    srv = subprocess.Popen([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ghserve.py'), str(PORT), d], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(0.8)
def ok(c, m): print(('✅ ' if c else '❌ ') + m); (None if c else ERR.append(m))

OV = {'ok': 0, '404': 0, 'id404': []}
def on_resp(r):
    u = r.url
    if '/ovoz/' in u and u.endswith('.mp3'):
        if r.status == 200: OV['ok'] += 1
        else: OV['404'] += 1; OV['id404'].append(u.split('/ovoz/')[1])
    elif u.startswith(URL) and r.status >= 400:
        ERR.append(f'HTTP {r.status} {u}')

try:
  with sync_playwright() as p:
    serve(OLD)
    ctx = p.chromium.launch_persistent_context(UDD, viewport={'width': 390, 'height': 844}, user_agent=UA, is_mobile=True, has_touch=True,
                                               args=['--autoplay-policy=no-user-gesture-required'])
    pg = ctx.pages[0] if ctx.pages else ctx.new_page()
    PE = []
    pg.on('pageerror', lambda e: PE.append(str(e)))
    pg.on('console', lambda m: PE.append('console.error: ' + m.text[:200]) if m.type == 'error' and 'Failed to load resource' not in m.text and 'fonts.g' not in m.text else None)
    pg.on('response', on_resp)
    ev = pg.evaluate
    # ---------- 1) 0.7.0 ----------
    pg.goto(URL + '?tez=1'); pg.wait_for_timeout(800)
    pg.fill('#on', 'Sinov'); pg.fill('#p1', '1234'); pg.fill('#p2', '1234'); pg.click('#go'); pg.wait_for_timeout(500)
    ids = ev("""(()=>{const A=BJ.A; const r=[['Kichik','g0','garaj'],['Orta','g1','orol'],['Katta','g2','garaj']].map(([l,d,w])=>{const b=A.newBola({laqab:l,daraja:d,avatar:'🐯',dunyo:w}); b.boshlandi='2026-10-28'; return b.id});
      A.S().sozlama.uyqu=''; A.S().joriy=r[0]; A.save(true); return r})()""")
    ok(ev('BJ.A.VER') == VOLD, f"{VOLD} ochildi ({ev('BJ.A.VER')})")
    def setj(bid): ev(f"(()=>{{const s=BJ.A.S(); s.joriy='{bid}'; BJ.A.save(true)}})()")
    NV = [0]
    def NAV(h, ms=600, ota=False, tez=True):
        NV[0] += 1; pg.goto(URL + (f'?tez=1&r={NV[0]}' if tez else f'?r={NV[0]}') + '#' + h)
        ev(("BJ.A.otaOk={rol:'admin',t:Date.now()}; " if ota else '') + 'BJ.A.render()'); pg.wait_for_timeout(ms)
    for bid in ids:
        setj(bid); NAV('missiya', 700)
        for _ in range(5):
            if ev("!!(window.__bjCur && __bjCur() && __bjCur().cb)"): ev("window.__bjJavob(true)"); pg.wait_for_timeout(700)
    oldYul = ev("Object.values(BJ.A.S().bolalar).map(b=>[b.id,b.yulduz||0, Object.keys(b.tugun||{}).length])")
    ok(not PE, f"{VOLD} da xato yo'q {PE[:3]}"); PE.clear()

    # ---------- 2) yangilanish VOLD → VNEW (xuddi telefondagidek: sahifa qayta ochiladi) ----------
    serve(NEW)
    vers = []
    for i in range(4):
        pg.goto(URL); pg.wait_for_timeout(2500); vers.append(ev('BJ.A.VER'))
    NOTE.append(f'ochishlar ketma-ketligi (GitHub Pages keshi 10 daq bilan): {vers}')
    ok(ev('BJ.A.VER') == VNEW, f"yangilanishdan keyin versiya {ev('BJ.A.VER')} (ochishlar: {vers})")
    ok(ev('BJ.A.S().appVer') == VNEW, 'appVer yangilandi')
    newYul = ev("Object.values(BJ.A.S().bolalar).map(b=>[b.id,b.yulduz||0, Object.keys(b.tugun||{}).length])")
    ok(sorted(newYul) == sorted(oldYul), f"bolalar va natijalar saqlandi ({len(newYul)} bola)")
    kk = ev("caches.keys()")
    ok('bj-v' + VNEW in kk and 'bj-v' + VOLD not in kk, f"service worker keshi yangilandi {kk}")
    ok('v' + VK(VNEW) in ev("document.body.innerText"), f"ekranda «v{VK(VNEW)}» belgisi")
    nz = ev("JSON.stringify(BJ.A.S().sozlama.nutq||null)"); NOTE.append('nutq sozlamasi: ' + nz)
    ok(not PE, f"yangilanishda xato yo'q {PE[:3]}"); PE.clear()

    # ---------- 3) har bola uchun to'liq missiya ----------
    SKIP = ('data-bk', 'data-out', 'data-charch', 'data-chiq', 'data-toz')
    def tugma_bos():
        # ko'rinib turgan, yoqilgan tugmalardan «oldinga» yuradiganini bosadi
        return ev("""(()=>{const vis=e=>{const r=e.getBoundingClientRect(); return r.width>0&&r.height>0&&!e.disabled&&getComputedStyle(e).visibility!=='hidden'};
          const sc=[...document.querySelectorAll('.scrim .btn, .scrim button')].filter(vis); const all=sc.length?sc:[...document.querySelectorAll('#app .btn, #app button')].filter(vis);
          const yaxshi=/Darsga qaytish|Savolga o'tish|Poygaga|➜|Davom|Keyingi|Boshla|tayyor|Tushundim|O'qib bo'ldim|Eslab qoldim|Endi o'zim|Yakunla|Natija|Olish|Ochish|Zo'r|Oldinga|Uyga|Tekshir|OK|Ha\\b|✓/i;
          const L2=all.filter(e=>!/^[⏸⏯⏮◀▶]$/.test((e.innerText||'').trim()) && !/Pauza|⏸/.test(e.innerText||'')); let b=L2.find(e=>e.matches('[data-next],[data-twin],[data-ok],[data-go-on]')) || L2.find(e=>yaxshi.test(e.innerText)) || L2.find(e=>!/(data-bk|data-out|data-charch|data-tush|data-sora)/.test(e.outerHTML.slice(0,140)));
          if(!b) return null; b.click(); return (b.innerText||b.getAttribute('aria-label')||'?').trim().slice(0,30)})()""")
    def missiya(bid, maxq=260):
        setj(bid); NAV('missiya', 800); n = 0; bos = []; jav = 0
        for i in range(maxq):
            st = ev("(()=>{const b=BJ.A.bola(); return {done: !!(b.missiya&&b.missiya.done), h: location.hash}})()")
            if st['done']: break
            qayt = ev("(()=>{const b=[...document.querySelectorAll('#app .btn, #app button')].find(e=>/Darsga qaytish|Davom etamiz|O'qishga qaytish/.test(e.innerText)); if(b){b.click(); return true} return false})()")
            if qayt: pg.wait_for_timeout(500); continue
            if ev("!!(window.__bjOyin && __bjOyin() && document.querySelector('canvas, .pz, .kz, .pg, .oyin'))") and not ev("window.__finBos===location.href"):
                ev("window.__finBos=location.href; try{BJ.A.oyin.finish()}catch(e){}"); pg.wait_for_timeout(700); continue
            if ev("!!(window.__bjUch && __bjUch() && __bjUch().state)"):
                try: ev("__bjUch().tugat(40)")
                except Exception: pass
                pg.wait_for_timeout(400)
            if ev("!!(window.__bjCur && __bjCur() && __bjCur().cb && __bjCur().it && document.querySelector('#body') && !document.querySelector('.scrim'))"):
                ev("window.__jv=__bjCur().it"); ev(f"window.__bjJavob({'true' if random.random() < 0.8 else 'false'})"); jav += 1
                pg.wait_for_timeout(450); continue
            t = tugma_bos(); bos.append(t); pg.wait_for_timeout(450)
            if t is None and st['h'] in ('', '#'): NAV('missiya', 600)
        st = ev("(()=>{const b=BJ.A.bola(); return {done: !!(b.missiya&&b.missiya.done), si: b.missiya&&b.missiya.si, n: b.missiya&&b.missiya.steps.length}})()")
        return st, jav, bos
    for bid in ids:
        st, jav, bos = missiya(bid)
        nm = ev(f"BJ.A.S().bolalar['{bid}'].laqab")
        ok(st['done'], f"{nm}: missiya oxirigacha o'tdi ({jav} javob, qadam {st['si']}/{st['n']})")
        if not st['done']: NOTE.append(f'{nm} oxirgi bosishlar: {bos[-12:]} | ekran: ' + ev("document.querySelector('#app').innerText.slice(0,200).replace(/\\n/g,' | ')"))
        ok(not PE, f"{nm}: missiyada JS xato yo'q {PE[:3]}"); PE.clear()
    ok(OV['ok'] > 20, f"ovoz fayllari haqiqatan yuklandi: {OV['ok']} ta")
    ok(OV['404'] == 0, f"yo'q ovoz fayli (404): {OV['404']} {OV['id404'][:5]}")

    if os.environ.get('MISSIYA_ONLY'): raise SystemExit(0)
    # ---------- 4) hamma ekranlar ----------
    OTA = ['ota', 'ota-arab', 'ota-bozor', 'ota-bozor-yangi', 'ota-bulut', 'ota-eksport', 'ota-hisobot', 'ota-ovoz', 'ota-pul', 'ota-qiyin', 'ota-qosh', 'ota-reyting', 'ota-sora', 'ota-sovga', 'ota-sozlama', 'ota-vazifa', 'ota-xarita', 'ota-zaxira'] + \
          [f'ota-bola-{ids[0]}', f'ota-harf-{ids[0]}', f'ota-oqish-{ids[1]}', f'ota-tahrir-{ids[2]}', f'ota-mavzu-{ids[1]}']
    for h in OTA:
        NAV(h, 700, ota=True)
        if PE: ok(False, f"#{h}: {PE[:2]}"); PE.clear()
    NAV('ota-ovoz', 900, ota=True)
    pg.click('[data-tek]'); pg.wait_for_timeout(3500)
    t = ev("document.body.innerText"); ok('Besh' in t and 'Fayl yuklandi' in t, "🔧 Ovozni tekshirish ishladi (fayl yuklandi)")
    pg.click('[data-eh="1"]'); pg.wait_for_timeout(300)
    kod = ev("(document.querySelector('[data-ehn] input')||{}).value||''"); NOTE.append('tekshiruv qatori: ' + kod)
    ok(kod.startswith('OVOZ|iPhone') and ('yol=media' in kod if VNEW >= '0.7.2' else True), f"natija qatori: {kod[:70]}")
    KID = ['', 'mashq', 'mashq-mat', 'mashq-til', 'mashq-ar', 'zal', 'dokon', 'garaj', 'bozor', 'arena']
    for bid in ids:
        setj(bid)
        for h in KID:
            NAV(h, 700)
            if PE: ok(False, f"bola {bid[:4]} #{h}: {PE[:2]}"); PE.clear()
    ok(True, f"ekranlar aylanib chiqildi: ota {len(OTA)} ta, bola {len(KID)}×{len(ids)}")

    # ---------- 5) mashq + Tushunmadim + so'rayman (har bola) ----------
    for bid in ids:
        setj(bid); NAV('mashq-mat', 800)
        for i in range(14):
            if pg.locator('[data-tush]').count() and i == 3:
                pg.click('[data-tush]'); pg.wait_for_timeout(4600)
                if pg.locator('[data-sora]').count(): pg.click('[data-sora]'); pg.wait_for_timeout(500)
                elif pg.locator('[data-tok]').count(): pg.click('[data-tok]'); pg.wait_for_timeout(300)
            if ev("!!(window.__bjCur && __bjCur() && __bjCur().cb && __bjCur().it && document.querySelector('#body') && !document.querySelector('.scrim'))"):
                ev(f"window.__bjJavob({'true' if random.random() < 0.7 else 'false'})"); pg.wait_for_timeout(450)
            else: tugma_bos(); pg.wait_for_timeout(450)
        if PE: ok(False, f"mashq/tushunmadim {bid[:4]}: {PE[:2]}"); PE.clear()
    ok(True, 'mashq + Tushunmadim aylanib chiqildi')

    # ---------- 6) monkey: tasodifiy bosishlar ----------
    for bid in ids:
        setj(bid); NAV('', 700)
        for i in range(120):
            ev("""(()=>{const vis=e=>{const r=e.getBoundingClientRect(); return r.width>0&&r.height>0&&!e.disabled};
              const L=[...document.querySelectorAll('.scrim button, .scrim .btn, #app button, #app .btn, #app .opt, #app [data-go]')].filter(vis).filter(e=>!/data-(out|toz|chiq|del)\\b|danger/.test(e.outerHTML.slice(0,160)));
              if(L.length) L[Math.floor(Math.random()*L.length)].click()})()""")
            pg.wait_for_timeout(180)
            if ev("location.hash").startswith('#ota') and random.random() < 0.3: NAV('', 300)
        if PE: ok(False, f"monkey {bid[:4]}: {PE[:4]}"); PE.clear()
        else: ok(True, f"monkey {ev(f'BJ.A.S().bolalar[\"{bid}\"].laqab')}: 120 bosish, xato yo'q")
    ctx.close()
finally:
    if srv: srv.terminate()
print('\nIZOH:', *NOTE, sep='\n  ')
print(f"\nNATIJA: {'HAMMASI OK' if not ERR else str(len(ERR)) + ' ta muammo'}")
for e in ERR: print('  -', e)
