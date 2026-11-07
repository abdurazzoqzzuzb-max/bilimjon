"""Bilimjon 🔊 — ovoz iboralari inventari (ovoz/iboralar.json uchun).
Ilovaning O'Z kodi (A.ovoz.savolReja / variantMatn / NUTQ) bilan hamma generatorlar matnidan bo'laklar yig'iladi + kafolatli sonlar va ismlar.
Ishlatish (ilova tarmog'ida, masalan v0.7.1):  python3 sinov/ovoz/inventar.py <iboralar.json yo'li> [N=300] [--tozala]
  → fayldagi "iboralar" yangilanadi (ovozlar/namuna saqlanadi). Keyin main'ga commit + push → GitHub Actions (ovoz.yml) yo'q fayllarni yasaydi.
NUTQ kodi o'zgarsa — id lar o'zgaradi: inventarni qayta yig'ing (eski fayllarni Actions o'zi o'chiradi).
0.7.3: "iboralar_en" — inglizcha so'z/iboralar (A.ovoz.enMatnlar, id = A.ovoz.enId) → ovoz/en_jenny/ (toplam: "en"). Har generator
topshirig'idagi it.tts shu ro'yxatda bo'lishi tekshiriladi."""
import json, os, subprocess, sys, time
from playwright.sync_api import sync_playwright
SITE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
A = [x for x in sys.argv[1:] if not x.startswith('--')]; OUT = A[0]; N = int(A[1]) if len(A) > 1 else 300; PORT = 8796
TOZALA = '--tozala' in sys.argv  # bo'lmasa — eski bo'laklar ham qoladi (kam uchraydiganlar yo'qolmasin)
JS = r"""(N) => {
 const reg = BJ.gen.reg, O = BJ.A.ovoz, NQ = O.NUTQ, ib = {}, harflar = (BJ.harfTartib || []).slice(), add = r => r.forEach(x => { ib[x.id] = x.t; });
 const ctxs = [{ g0: true, dunyo: 'garaj', harflar }, { g0: false, dunyo: 'orol', harflar }, { g0: true, dunyo: 'orol', harflar: harflar.slice(0, 8) }];
 let n = 0;
 for (const id of Object.keys(reg)) for (let q = 1; q <= 3; q++) for (const c of ctxs) for (let i = 0; i < N; i++) {
   let it; try { it = BJ.gen.make(id, q, Object.assign({}, c, { kashfSavol: i })); } catch (e) { break; } it.tugun = id; n++;
   add(O.savolReja(it)); if (Array.isArray(it.o)) it.o.forEach(o => add(O.reja(O.variantMatn(it, o))));
 }
 for (let k = 0; k <= 100; k++) ['', 'ta', 'ga', 'ni', 'dan'].forEach(s => add(NQ.sonQism(k, s)));
 for (let k = 1; k <= 30; k++) ['inchi', 'tasi', 'tasini'].forEach(s => add(NQ.sonQism(k, s)));
 for (let y = 1; y <= 9; y++) ['', 'ga', 'ni', 'dan'].forEach(s => { add(NQ.sonQism(y * 100, s)); add(NQ.sonQism(y * 1000, s)); });
 NQ.ISMLAR.forEach(i => ['', 'niki', 'ning', 'dan', 'da', 'ga', 'ni'].forEach(s => add(NQ.reja(i + s))));
 Object.keys(NQ.HARF_NOM).forEach(k => add([NQ.harfQism(k)]));   // 07.11: harflar nomi (a, be, de …) — hammasi kafolatli
 const en = {}, enYoq = new Set(); O.enMatnlar().forEach(t => { en[O.enId(t)] = t; });
 for (const id of Object.keys(reg)) for (let q = 1; q <= 3; q++) for (let i = 0; i < 40; i++) { let it; try { it = BJ.gen.make(id, q, ctxs[i % 3]); } catch (e) { break; } if (it.tts && !en[O.enId(it.tts)]) enYoq.add(it.tts); }
 return { n, ib, en, enYoq: [...enYoq] };
}"""
srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT)], cwd=SITE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
try:
    with sync_playwright() as p:
        br = p.chromium.launch(); pg = br.new_page(); pg.goto(f'http://localhost:{PORT}/?tez=1'); pg.wait_for_timeout(900)
        d = pg.evaluate(JS, N); br.close()
finally: srv.terminate()
cfg = json.load(open(OUT, encoding='utf-8')) if os.path.exists(OUT) else {'v': 2, 'ovozlar': {}, 'namuna': {}}
bad = [k for k, v in d['ib'].items() if not v.strip() or any(ch.isdigit() for ch in v)]
if bad: sys.exit('❌ raqamli/bo\'sh bo\'lak: ' + ', '.join(bad[:10]))
if d['enYoq']: sys.exit('❌ inglizcha tts ro\'yxatda yo\'q: ' + ', '.join(d['enYoq'][:10]))
eskiE = set(cfg.get('iboralar_en', {})); yE = {} if TOZALA else dict(cfg.get('iboralar_en', {})); yE.update(d['en']); cfg['iboralar_en'] = dict(sorted(yE.items()))
print(f"🇬🇧 inglizcha: {len(cfg['iboralar_en'])} (+{len(set(cfg['iboralar_en']) - eskiE)} yangi)")
eski = set(cfg.get('iboralar', {})); yangi = {} if TOZALA else dict(cfg.get('iboralar', {})); yangi.update(d['ib']); cfg['iboralar'] = dict(sorted(yangi.items()))
json.dump(cfg, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=0)
print(f"✅ {d['n']} topshiriq → {len(cfg['iboralar'])} bo'lak (+{len(set(cfg['iboralar']) - eski)} yangi, −{len(eski - set(cfg['iboralar']))} eski)")
