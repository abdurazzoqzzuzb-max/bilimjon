"""Bilimjon 🧪 — sinov rejimi papkasini yig'ish: `beta/` = ko'rsatilgan tarmoqdagi ilova fayllari (bolalar ilovasiga tegmaydi).
Ishlatish (repo ildizida, odatda main'da):  python3 sinov/beta/beta_yig.py <tarmoq> [papka=beta]
  (<tarmoq> = «.» — ishchi papkadagi fayllardan; faqat avtomatik sinov uchun)
  • fayllar git'dan olinadi (`git show <tarmoq>:<fayl>`) — ishchi papkadagi o'zgarishlar aralashmaydi;
  • manifest nomi «Bilimjon 🧪», sw.js o'zi /beta/ ni taniydi (alohida bj-beta- kesh), index.html — /beta/ manzilida xotira bj_beta_*;
  • papkaga VERSIYA.txt (tarmoq, commit, VER) yoziladi. Keyin: git add beta && git commit && git push (faqat beta/ o'zgaradi).
0.7.1 da qayta yozildi (0.7.0 dagi nusxa repo'ga tushmagan edi)."""
import json, os, re, subprocess, sys

FAYLLAR = ['index.html', 'sw.js', 'manifest.webmanifest', 'icon.svg', 'icon-192.png', 'icon-512.png', 'firestore.rules', 'qoidalar/firestore-0.5.0.rules']
QATIY = {'index.html', 'sw.js', 'manifest.webmanifest'}

def git(*a, raw=False):
    r = subprocess.run(['git', *a], capture_output=True)
    if r.returncode: raise SystemExit('git ' + ' '.join(a) + ': ' + r.stderr.decode(errors='replace').strip())
    return r.stdout if raw else r.stdout.decode().strip()

def main():
    if len(sys.argv) < 2: raise SystemExit(__doc__)
    tarmoq, papka = sys.argv[1], (sys.argv[2] if len(sys.argv) > 2 else 'beta')
    if papka.strip('/') in ('', '.', '..') or '..' in papka: raise SystemExit("Papka nomi noto'g'ri")
    ishchi = tarmoq == '.'
    commit = git('rev-parse', '--short', 'HEAD') + ('+ishchi' if ishchi else '') if ishchi else git('rev-parse', '--short', tarmoq)
    os.makedirs(papka, exist_ok=True); yozildi = []
    for f in FAYLLAR:
        try:
            if ishchi:
                if not os.path.exists(f): raise SystemExit(f)
                b = open(f, 'rb').read()
            else: b = git('show', f'{tarmoq}:{f}', raw=True)
        except SystemExit:
            if f in QATIY: raise
            print('⚠️ tarmoqda yo\'q:', f); continue
        if f == 'manifest.webmanifest':
            m = json.loads(b.decode('utf-8')); m['name'] = 'Bilimjon 🧪 Sinov'; m['short_name'] = 'Bilimjon 🧪'; m['theme_color'] = '#E65100'
            b = (json.dumps(m, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
        out = os.path.join(papka, f); os.makedirs(os.path.dirname(out) or '.', exist_ok=True)
        with open(out, 'wb') as fh: fh.write(b)
        yozildi.append(f)
    html = open(os.path.join(papka, 'index.html'), encoding='utf-8').read()
    ver = (re.search(r"A\.VER = '([\d.]+)'", html) or [None, '?'])[1]
    sw = open(os.path.join(papka, 'sw.js'), encoding='utf-8').read(); swv = (re.search(r"const V = P \+ '([\d.]+)'", sw) or [None, '?'])[1]
    if ver != swv: raise SystemExit(f'❌ index.html VER {ver} ≠ sw.js V {swv}')
    if 'A.BETA' not in html: raise SystemExit('❌ index.html da sinov rejimi (A.BETA) yo\'q')
    with open(os.path.join(papka, 'VERSIYA.txt'), 'w', encoding='utf-8') as fh:
        fh.write(f'Bilimjon sinov rejimi\ntarmoq: {tarmoq}\ncommit: {commit}\nVER: {ver}\n')
    print(f'✅ {papka}/ ← {tarmoq} ({commit}), VER {ver}: ' + ', '.join(yozildi))

if __name__ == '__main__': main()
