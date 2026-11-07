"""Bilimjon 🔊 — neyron ovoz fayllarini yasash (GitHub Actions'da ishlaydi; kompyuter shart emas).
Kirish: ovoz/iboralar.json  {"v": 1, "ovozlar": {"madina": {"voice": "uz-UZ-MadinaNeural", "rate": "-8%"}, ...},
                             "iboralar": {"<id>": "<matn>", ...}, "namuna": {"<id>": "<matn>", ...}}
Chiqish: ovoz/<ovoz>/<id>.mp3 (faqat yo'qlari yasaladi) + ovoz/<ovoz>/royxat.json (tayyor id'lar).
Namuna: ovoz/namuna/<ovoz>_<id>.mp3 — ota-ona ilovada eshitib tanlaydi.
Litsenziya [?]: edge-tts — Microsoft Edge «Read aloud» xizmati (rasmiy API emas); oilaviy, notijorat foydalanish uchun."""
import asyncio, json, os, sys, time
import edge_tts

ILD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # ovoz/
FMT = 'audio-24khz-48kbitrate-mono-mp3'

async def bitta(matn, voice, rate, yol, urinish=4):
    for i in range(urinish):
        try:
            c = edge_tts.Communicate(matn, voice, rate=rate)
            tmp = yol + '.tmp'
            with open(tmp, 'wb') as f:
                async for ch in c.stream():
                    if ch['type'] == 'audio': f.write(ch['data'])
            if os.path.getsize(tmp) < 400: raise RuntimeError('bo\'sh audio')
            os.replace(tmp, yol); return True
        except Exception as e:
            print('  ⚠️', voice, matn[:40], str(e)[:160], file=sys.stderr); await asyncio.sleep(2 + i * 3)
    try: os.remove(yol + '.tmp')
    except OSError: pass
    return False

async def ishla(ish, parallel=6):
    sem = asyncio.Semaphore(parallel); ok = [0]; xato = []
    async def w(x):
        async with sem:
            if await bitta(*x): ok[0] += 1
            else: xato.append(x[3])
    await asyncio.gather(*(w(x) for x in ish))
    return ok[0], xato

def main():
    cfg = json.load(open(os.path.join(ILD, 'iboralar.json'), encoding='utf-8'))
    tanlangan = sys.argv[1:] or list(cfg['ovozlar'])
    ish = []
    os.makedirs(os.path.join(ILD, 'namuna'), exist_ok=True)
    for on, o in cfg['ovozlar'].items():
        for nid, matn in (cfg.get('namuna') or {}).items():
            y = os.path.join(ILD, 'namuna', f'{on}_{nid}.mp3')
            if not os.path.exists(y): ish.append((matn, o['voice'], o.get('rate', '+0%'), y))
    for on in tanlangan:
        o = cfg['ovozlar'][on]
        if not o.get('toliq'): continue  # to'liq to'plam faqat tanlangan ovoz uchun
        papka = os.path.join(ILD, on); os.makedirs(papka, exist_ok=True)
        for iid, matn in cfg['iboralar'].items():
            y = os.path.join(papka, iid + '.mp3')
            if not os.path.exists(y): ish.append((matn, o['voice'], o.get('rate', '+0%'), y))
    t = time.time(); print('yasaladi:', len(ish))
    n, xato = asyncio.run(ishla(ish))
    for on in tanlangan:
        papka = os.path.join(ILD, on)
        if os.path.isdir(papka) and cfg['ovozlar'][on].get('toliq'):
            for f in os.listdir(papka):  # endi ishlatilmaydigan (matni o'zgargan) fayllar
                if f.endswith('.mp3') and f[:-4] not in cfg['iboralar']: os.remove(os.path.join(papka, f))
        if os.path.isdir(papka):
            bor = sorted(f[:-4] for f in os.listdir(papka) if f.endswith('.mp3'))
            json.dump({'v': cfg.get('v', 1), 'n': len(bor), 'id': bor}, open(os.path.join(papka, 'royxat.json'), 'w'), separators=(',', ':'))
    print(f'✅ {n} ta, ❌ {len(xato)} ta, {time.time() - t:.0f} s')
    if xato: print('\n'.join(xato[:50]))
    if ish and n == 0: sys.exit('❌ birorta ham fayl yasalmadi')

if __name__ == '__main__': main()
