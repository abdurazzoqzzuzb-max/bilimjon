"""Bilimjon 🔊 — neyron ovoz fayllarini yasash (GitHub Actions'da ishlaydi; kompyuter shart emas).
Kirish: ovoz/iboralar.json
  "ovozlar": {"<nom>": {"dvigatel": "edge"|"gemini", ...sozlama, "toliq": true|false, "namuna": true|false}}
     edge   — voice (uz-UZ-MadinaNeural…), rate ("-18%"), pitch ("+0Hz")
     gemini — model (gemini-3.8-flash-tts…), voice (Kore…), style (ohang: «iliq, quvnoq…»); kalit — GitHub secret GEMINI_API_KEY
  "iboralar": {"<id>": "<matn>"}, "namuna": {"<id>": "<matn>"}
Chiqish: ovoz/<nom>/<id>.mp3 (faqat yo'qlari) + ovoz/<nom>/royxat.json {v, n, id, sig}; namuna: ovoz/namuna/<nom>_<id>.mp3.
Sozlama (sig) o'zgarsa — o'sha ovozning hamma fayli qayta yasaladi.
TALAFFUZ (07.11, foydalanuvchi: «G' va O' ni yaxshi aytolmayapti»): ilova matnida o' / g' ASCII apostrof bilan — TTS uni pauza/tutuq
deb o'qiydi. TTS ga yuborishdan oldin rasmiy imlo: oʻ gʻ (U+02BB), tutuq belgisi ʼ (U+02BC). Fayl id lari (ilova matni) o'zgarmaydi.
Litsenziya [?]: edge-tts — Edge «Read aloud» xizmati (rasmiy API emas), oilaviy notijorat foydalanish; Gemini — bepul tarifda matnlar Google'ga ochiq (umumiy savollar, shaxsiy ma'lumot yo'q)."""
import asyncio, base64, hashlib, io, json, os, re, shutil, subprocess, sys, time, urllib.request, wave

ILD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # ovoz/
OKO = 'ʻ'; TUTUQ = 'ʼ'

def talaffuz(t):
    t = re.sub(r"([OoGg])['‘’`ʼ]", lambda m: m.group(1) + OKO, t)       # oʻ gʻ
    t = re.sub(r"(?<=[A-Za-z])['‘’`](?=[A-Za-z])", TUTUQ, t)              # maʼno, sanʼat
    return t

def imzo(o):  # sozlama imzosi — o'zgarsa qayta yasaladi
    k = {x: o.get(x) for x in ('dvigatel', 'voice', 'rate', 'pitch', 'model', 'style', 'imlo')}
    return hashlib.sha1(json.dumps(k, sort_keys=True).encode()).hexdigest()[:10]

# ---------------- edge-tts ----------------
async def edge_bitta(matn, o, yol):
    import edge_tts
    c = edge_tts.Communicate(matn, o['voice'], rate=o.get('rate', '+0%'), pitch=o.get('pitch', '+0Hz'))
    tmp = yol + '.tmp'
    with open(tmp, 'wb') as f:
        async for ch in c.stream():
            if ch['type'] == 'audio': f.write(ch['data'])
    if os.path.getsize(tmp) < 400: raise RuntimeError("bo'sh audio")
    os.replace(tmp, yol)

# ---------------- Gemini TTS (Interactions API) ----------------
def gemini_bitta(matn, o, yol):
    key = os.environ.get('GEMINI_API_KEY')
    if not key: raise RuntimeError('GEMINI_API_KEY yo\'q')
    tx = {'type': 'text', 'text': matn}
    if o.get('style'): tx['annotations'] = [{'type': 'speech_metadata', 'style': o['style']}]
    body = {'model': o.get('model', 'gemini-3.8-flash-tts'), 'input': [{'type': 'user_input', 'content': [tx]}],
            'response_format': {'type': 'audio'}, 'generation_config': {'speech_config': [{'voice': o.get('voice', 'Kore')}]}}
    req = urllib.request.Request('https://generativelanguage.googleapis.com/v1beta/interactions', data=json.dumps(body).encode(),
                                 headers={'Content-Type': 'application/json', 'x-goog-api-key': key})
    with urllib.request.urlopen(req, timeout=120) as r: d = json.loads(r.read())
    b64 = None
    def izla(x):
        nonlocal b64
        if b64: return
        if isinstance(x, dict):
            if isinstance(x.get('data'), str) and len(x['data']) > 1000: b64 = x['data']; return
            for v in x.values(): izla(v)
        elif isinstance(x, list):
            for v in x: izla(v)
    izla(d)
    if not b64: raise RuntimeError('audio yo\'q: ' + json.dumps(d)[:300])
    raw = base64.b64decode(b64)
    if raw[:4] != b'RIFF':  # sarlavhasiz PCM 24 kHz s16le
        bio = io.BytesIO(); w = wave.open(bio, 'wb'); w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000); w.writeframes(raw); w.close(); raw = bio.getvalue()
    tmp = yol + '.wav'; open(tmp, 'wb').write(raw)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', tmp, '-ac', '1', '-ar', '24000', '-b:a', '48k', yol], check=True); os.remove(tmp)

async def bitta(matn, o, yol, urinish=4):
    matn = talaffuz(matn) if o.get('imlo', 2) >= 2 else matn
    for i in range(urinish):
        try:
            if o.get('dvigatel', 'edge') == 'gemini': await asyncio.to_thread(gemini_bitta, matn, o, yol)
            else: await edge_bitta(matn, o, yol)
            return True
        except Exception as e:
            print('  ⚠️', o.get('voice'), matn[:40], str(e)[:200], file=sys.stderr); await asyncio.sleep(2 + i * 4)
    for x in (yol + '.tmp', yol + '.wav'):
        try: os.remove(x)
        except OSError: pass
    return False

async def ishla(ish, parallel):
    sem = asyncio.Semaphore(parallel); ok = [0]; xato = []
    async def w(x):
        async with sem:
            if await bitta(*x): ok[0] += 1
            else: xato.append(x[2])
    await asyncio.gather(*(w(x) for x in ish))
    return ok[0], xato

def main():
    cfg = json.load(open(os.path.join(ILD, 'iboralar.json'), encoding='utf-8'))
    tanlangan = sys.argv[1:] or list(cfg['ovozlar'])
    gem = bool(os.environ.get('GEMINI_API_KEY'))
    os.makedirs(os.path.join(ILD, 'namuna'), exist_ok=True)
    ish = {'edge': [], 'gemini': []}
    for on in tanlangan:
        o = dict(cfg['ovozlar'][on]); dv = o.get('dvigatel', 'edge'); sig = imzo(o)
        if dv == 'gemini' and not gem: print(f'⏭ {on}: GEMINI_API_KEY secret yo\'q — o\'tkazildi'); continue
        if o.get('namuna', True):
            sf = os.path.join(ILD, 'namuna', on + '.sig')
            if not os.path.exists(sf) or open(sf).read().strip() != sig:
                for f in os.listdir(os.path.join(ILD, 'namuna')):
                    if f.startswith(on + '_n') and f.endswith('.mp3') and f[len(on) + 2:-4].isdigit(): os.remove(os.path.join(ILD, 'namuna', f))
                open(sf, 'w').write(sig)
            for nid, matn in (cfg.get('namuna') or {}).items():
                y = os.path.join(ILD, 'namuna', f'{on}_{nid}.mp3')
                if not os.path.exists(y): ish[dv].append((matn, o, y))
        if not o.get('toliq'): continue
        papka = os.path.join(ILD, on); rf = os.path.join(papka, 'royxat.json')
        if os.path.exists(rf) and json.load(open(rf)).get('sig') != sig: shutil.rmtree(papka)   # sozlama o'zgardi — qaytadan
        os.makedirs(papka, exist_ok=True)
        for f in os.listdir(papka):  # matni o'zgargan (endi ishlatilmaydigan) fayllar
            if f.endswith('.mp3') and f[:-4] not in cfg['iboralar']: os.remove(os.path.join(papka, f))
        for iid, matn in cfg['iboralar'].items():
            y = os.path.join(papka, iid + '.mp3')
            if not os.path.exists(y): ish[dv].append((matn, o, y))
    t = time.time(); print('yasaladi: edge', len(ish['edge']), '· gemini', len(ish['gemini']))
    n1, x1 = asyncio.run(ishla(ish['edge'], 6)) if ish['edge'] else (0, [])
    n2, x2 = asyncio.run(ishla(ish['gemini'], 2)) if ish['gemini'] else (0, [])
    for on in tanlangan:
        o = cfg['ovozlar'][on]; papka = os.path.join(ILD, on)
        if o.get('toliq') and os.path.isdir(papka):
            bor = sorted(f[:-4] for f in os.listdir(papka) if f.endswith('.mp3'))
            json.dump({'v': cfg.get('v', 1), 'n': len(bor), 'id': bor, 'sig': imzo(o)}, open(os.path.join(papka, 'royxat.json'), 'w'), separators=(',', ':'))
    xato = x1 + x2; n = n1 + n2
    print(f'✅ {n} ta, ❌ {len(xato)} ta, {time.time() - t:.0f} s')
    if xato: print('\n'.join(xato[:50]))
    if (ish['edge'] or ish['gemini']) and n == 0: sys.exit('❌ birorta ham fayl yasalmadi')

if __name__ == '__main__': main()
