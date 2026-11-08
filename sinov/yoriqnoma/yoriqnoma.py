"""Bilimjon 📘 YO'RIQNOMA + TAKLIFNOMA — yangi oilaga yuboriladi (iPhone va Android, rasmli, 6 sahifa 9:16).
Ishlatish:  python3 sinov/yoriqnoma/yoriqnoma.py [papka=/tmp/bj_yoriqnoma] [--suratsiz]
  → <papka>/Bilimjon_yoriqnoma_v7.6.pdf  +  <papka>/Bilimjon_1.jpg … Bilimjon_6.jpg (1080×1920 — Telegram albomi uchun)
  • versiya (v7.6) index.html dagi A.VER dan o'zi olinadi; ekran rasmlari — sinov/yoriqnoma/suratlar.py (haqiqiy ilova, namuna oila);
  • matnni o'zgartirish — pastdagi SAHIFALAR (har sahifa — sarlavha + qadamlar). Yangi versiyada: matnni tuzatish → qayta ishga tushirish.
  • Repoga faqat shu generator yoziladi (ism, oila ma'lumoti yo'q); tayyor PDF/PNG — faqat chatda."""
import os, re, sys, html, subprocess, base64, io
from playwright.sync_api import sync_playwright
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.abspath(os.path.join(D, '..', '..'))
ARG = [a for a in sys.argv[1:] if not a.startswith('--')]
OUT = os.path.abspath(ARG[0] if ARG else '/tmp/bj_yoriqnoma'); SUR = os.path.join(OUT, 'sur'); os.makedirs(SUR, exist_ok=True)
VER = re.search(r"A\.VER = '([\d.]+)'", open(os.path.join(SITE, 'index.html'), encoding='utf-8').read()).group(1)
VK = (lambda q: q[1] + ('.' + q[2] if q[2] != '0' else '') if q[0] == '0' else q[0] + '.' + q[1])(VER.split('.'))
SAYT = 'https://abdurazzoqzzuzb-max.github.io/bilimjon/'
SAYT_K = 'abdurazzoqzzuzb-max.github.io/bilimjon'
if '--suratsiz' not in sys.argv or not os.path.exists(os.path.join(SUR, '04_uy.png')):
    subprocess.run([sys.executable, os.path.join(D, 'suratlar.py'), SUR], check=True)

def img(nom, w=None, q=84):   # ekran rasmi → JPEG data URI (PDF yengil bo'lsin)
    im = Image.open(os.path.join(SUR, nom + '.png')).convert('RGB')
    if w: im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, 'JPEG', quality=q, optimize=True); return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
ICON = 'data:image/png;base64,' + base64.b64encode((lambda b: (Image.open(os.path.join(SITE, 'icon-512.png')).convert('RGBA').resize((256, 256), Image.LANCZOS).save(b, 'PNG'), b.getvalue())[1])(io.BytesIO())).decode()
e = html.escape

def tel(nom, w=168, kes=None, cls=''):   # telefon ramkasidagi haqiqiy ekran (kes — yuqoridan necha % ko'rinsin)
    h = round(w * 844 / 390 * (kes or 1))
    return f'<div class="tel {cls}" style="width:{w}px;height:{h}px"><img src="{img(nom, 600)}" alt=""></div>'

# ---------- telefon tizimi tugmalari (soddalashtirilgan chizma — qayerni bosishni ko'rsatadi) ----------
GOLD = '#FFC94A'
def ring(x, y, r=17): return f'<circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{GOLD}" stroke-width="3.5"/><circle cx="{x}" cy="{y}" r="{r + 7}" fill="none" stroke="{GOLD}" stroke-opacity=".35" stroke-width="2"/>'
def ios_bar():
    return f'''<svg viewBox="0 0 260 96" width="236"><rect x="2" y="2" width="256" height="92" rx="18" fill="#F2F2F7" stroke="#D1D1D6"/>
    <rect x="16" y="12" width="228" height="30" rx="9" fill="#E3E3E8"/><text x="130" y="32" font-size="11.5" text-anchor="middle" fill="#3A3A3C" font-family="Inter">🔒 {e(SAYT_K)}</text>
    <g fill="none" stroke="#0A84FF" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><path d="M34 62 l-7 8 7 8"/><path d="M76 62 l7 8 -7 8"/>
    <path d="M124 58 v18 M118 64 l6 -6 6 6 M117 68 h-5 v14 h24 v-14 h-5"/><path d="M168 60 q8 -3 14 1 v18 q-6 -4 -14 -1z M182 61 q6 -4 14 -1 v18 q-8 -3 -14 1"/><rect x="214" y="60" width="16" height="18" rx="3"/><path d="M218 56 h12 q4 0 4 4 v12"/></g>
    {ring(124, 70)}</svg>'''
def ios_sheet():
    q = [('Скопировать', '⧉', 0), ('Добавить в Избранное', '☆', 0), ('На экран «Домой»', '⊞', 1), ('Добавить заметку', '✎', 0)]
    rows = ''.join(f'<g transform="translate(0,{26 + i * 38})"><rect x="12" y="0" width="236" height="34" rx="8" fill="{"#FFF7DD" if h else "#FFFFFF"}" stroke="{GOLD if h else "#E5E5EA"}" stroke-width="{3 if h else 1}"/>'
                   f'<text x="24" y="22" font-size="13" font-family="Inter" font-weight="{700 if h else 500}" fill="#1C1C1E">{e(t)}</text><text x="232" y="23" font-size="15" text-anchor="end" fill="#3A3A3C">{ic}</text></g>' for i, (t, ic, h) in enumerate(q))
    return f'<svg viewBox="0 0 260 186" width="236"><rect x="2" y="2" width="256" height="182" rx="18" fill="#F2F2F7" stroke="#D1D1D6"/><rect x="110" y="9" width="40" height="5" rx="2.5" fill="#C7C7CC"/>{rows}</svg>'
def ios_add():
    return f'''<svg viewBox="0 0 260 120" width="236"><rect x="2" y="2" width="256" height="116" rx="18" fill="#F2F2F7" stroke="#D1D1D6"/>
    <text x="22" y="30" font-size="13" fill="#0A84FF" font-family="Inter">Отменить</text>
    <text x="238" y="30" font-size="13.5" text-anchor="end" font-weight="800" fill="#0A84FF" font-family="Inter">Добавить</text><ellipse cx="208" cy="26" rx="40" ry="17" fill="none" stroke="#FFC94A" stroke-width="3.5"/>
    <rect x="14" y="46" width="232" height="60" rx="12" fill="#fff" stroke="#E5E5EA"/><image href="{ICON}" x="24" y="54" width="44" height="44"/><text x="80" y="74" font-size="15" font-weight="700" fill="#1C1C1E" font-family="Inter">Bilimjon</text>
    <text x="80" y="92" font-size="10.5" fill="#8E8E93" font-family="Inter">{e(SAYT_K)}</text></svg>'''
def and_bar():
    return f'''<svg viewBox="0 0 260 70" width="236"><rect x="2" y="2" width="256" height="66" rx="16" fill="#FFFFFF" stroke="#DADCE0"/>
    <path d="M22 35 h14 M29 28 v14" stroke="#5F6368" stroke-width="2.2" stroke-linecap="round"/><rect x="48" y="16" width="160" height="38" rx="19" fill="#F1F3F4"/>
    <text x="128" y="39.5" font-size="8.6" text-anchor="middle" fill="#3C4043" font-family="Inter">{e(SAYT_K)}</text><rect x="214" y="24" width="18" height="22" rx="4" fill="none" stroke="#5F6368" stroke-width="2"/><text x="223" y="40" font-size="10" text-anchor="middle" fill="#5F6368" font-family="Inter">1</text>
    <g fill="#3C4043"><circle cx="246" cy="25" r="2.6"/><circle cx="246" cy="35" r="2.6"/><circle cx="246" cy="45" r="2.6"/></g>{ring(246, 35, 14)}</svg>'''
def and_menu():
    q = [('Новая вкладка', 0), ('Закладки', 0), ('Установить приложение', 1), ('Добавить на главный экран', 1), ('Настройки', 0)]
    rows = ''.join(f'<g transform="translate(0,{12 + i * 34})"><rect x="10" y="0" width="240" height="30" rx="7" fill="{"#FFF7DD" if h else "#FFFFFF"}" stroke="{GOLD if h else "#FFFFFF"}" stroke-width="{2.6 if h else 0}"/>'
                   f'<text x="22" y="20" font-size="12.5" font-family="Inter" font-weight="{700 if h else 500}" fill="#202124">{e(t)}</text></g>' for i, (t, h) in enumerate(q))
    return f'<svg viewBox="0 0 260 186" width="236"><rect x="2" y="2" width="256" height="182" rx="14" fill="#FFFFFF" stroke="#DADCE0"/>{rows}</svg>'
def and_add():
    return f'''<svg viewBox="0 0 260 120" width="236"><rect x="2" y="2" width="256" height="116" rx="18" fill="#FFFFFF" stroke="#DADCE0"/><image href="{ICON}" x="20" y="18" width="40" height="40"/>
    <text x="72" y="34" font-size="14" font-weight="700" fill="#202124" font-family="Inter">Установить приложение?</text><text x="72" y="52" font-size="12" fill="#5F6368" font-family="Inter">Bilimjon</text>
    <text x="128" y="98" font-size="13" text-anchor="middle" fill="#1A73E8" font-weight="600" font-family="Inter">Отмена</text><rect x="164" y="80" width="84" height="28" rx="14" fill="#1A73E8"/>
    <text x="206" y="99" font-size="12.5" text-anchor="middle" fill="#fff" font-weight="700" font-family="Inter">Установить</text><rect x="159" y="75" width="94" height="38" rx="19" fill="none" stroke="#FFC94A" stroke-width="3.5"/></svg>'''
def ekran_belgi():   # bosh ekrandagi belgi
    return f'''<svg viewBox="0 0 260 112" width="236"><defs><linearGradient id="wp" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3B2A6B"/><stop offset="1" stop-color="#0F3D5E"/></linearGradient></defs>
    <rect x="2" y="2" width="256" height="108" rx="18" fill="url(#wp)"/>{"".join(f'<rect x="{18 + i * 60}" y="16" width="44" height="44" rx="11" fill="#ffffff" fill-opacity=".16"/>' for i in (0, 1, 3))}
    <image href="{ICON}" x="138" y="16" width="44" height="44"/>{ring(160, 38, 30).replace('r="30"', 'r="28"')}<text x="160" y="80" font-size="11" text-anchor="middle" fill="#fff" font-weight="600" font-family="Inter">Bilimjon</text>
    <text x="130" y="101" font-size="10" text-anchor="middle" fill="#ffffff" fill-opacity=".7" font-family="Inter">bosh ekran (рабочий стол)</text></svg>'''

def qadam(n, sar, mat, rasm=''):
    return f'<div class="qd"><div class="qn">{n}</div><div class="qm"><b>{sar}</b><p>{mat}</p>{rasm}</div></div>'
def bosh(ic, sar, kichik=''):
    return f'<div class="bsh"><span class="bic">{ic}</span><div><h2>{sar}</h2>{f"<small>{kichik}</small>" if kichik else ""}</div><span class="vpill">v{VK}</span></div>'
def oyoq(n): return f'<div class="oyoq"><span>Bilimjon · oilaviy o\'yin-darslik</span><span>{n} / 6</span></div>'
LINK = f'<a class="url" href="{SAYT}">{e(SAYT_K)}</a>'

# ======================= SAHIFALAR (matnni shu yerda o'zgartiring) =======================
SAHIFALAR = [
# 1 — taklifnoma
f'''<div class="cover"><img class="logo" src="{ICON}" alt=""><h1>Bilimjon</h1><div class="sub">oilaviy o'yin-darslik · v{VK}</div>
<div class="taklif"><div class="tk">✉️ TAKLIFNOMA</div><h3>Sizni oilamiz ilovasiga taklif qilamiz!</h3>
<p>Farzandlaringiz har kuni <b>20–30 daqiqa</b> o'ynab o'rganadi: matematika, ona tili va o'qish, ingliz va arab tili, mantiq. Savollar <b>ovozda o'qiladi</b>, xato qilsa — rasmli kichik dars. Missiyadan keyin — o'yinlar zali, sovg'alar va <b>oilalar o'rtasida reyting</b>.</p><p class="bep">🎁 Birinchi <b>1 oy — bepul</b>, keyin pullik.</p></div>
<div class="fan">{tel('04_uy', 132, .62, 'f1')}{tel('05_savol', 150, .55, 'f2')}{tel('09_zal', 132, .62, 'f3')}</div>
<div class="maxfiy"><b>🔒 Bu — shaxsiy oilaviy ilova</b><span>Faqat taklif qilingan oilalar uchun. Iltimos, havolani va shu yo'riqnomani boshqa hech kimga yubormang.</span></div>
<div class="keyin">📲 O'rnatish — 5 daqiqa: <b>2-sahifa — iPhone</b>, <b>3-sahifa — Android</b></div></div>{oyoq(1)}''',
# 2 — iPhone
bosh('', 'iPhone\'ga o\'rnatish', 'Faqat <b>Safari</b> brauzerida (Chrome emas)') + '<div class="qlar">' +
qadam(1, 'Safari\'da oching', f'Havolani bosing yoki Safari\'ga yozing:<br>{LINK}', '') +
qadam(2, '«Поделиться» → «На экран «Домой»»', 'Pastdagi <b>kvadrat va strelka</b> belgisini bosing, ro\'yxatni pastga suring va <b>«На экран «Домой»»</b> (Add to Home Screen) ni tanlang.', f'<div class="mk2">{ios_bar()}{ios_sheet()}</div>') +
qadam(3, '«Добавить» → bosh ekrandan oching', 'O\'ng tepadagi <b>«Добавить»</b>. Endi ilovani har doim bosh ekrandagi <b>Bilimjon</b> belgisidan oching.', f'<div class="mk2">{ios_add()}{ekran_belgi()}</div>') +
'</div><div class="eslat">💡 Ovoz chiqmasa — telefonni jim rejimdan chiqaring va ekranga bir marta teging.</div>' + oyoq(2),
# 3 — Android
bosh('', 'Android\'ga o\'rnatish', '<b>Google Chrome</b> brauzerida') + '<div class="qlar">' +
qadam(1, 'Chrome\'da oching', f'Havolani bosing yoki Chrome\'ga yozing:<br>{LINK}', '') +
qadam(2, '⋮ (uch nuqta) → «Установить приложение»', 'O\'ng tepadagi <b>⋮</b> ni bosing va <b>«Установить приложение»</b> yoki <b>«Добавить на главный экран»</b> ni tanlang (Install app / Add to Home screen).', f'<div class="mk2">{and_bar()}{and_menu()}</div>') +
qadam(3, '«Установить» → bosh ekrandan oching', 'Tasdiqlang. Endi ilovani har doim bosh ekrandagi <b>Bilimjon</b> belgisidan oching.', f'<div class="mk2">{and_add()}{ekran_belgi()}</div>') +
'</div><div class="eslat">💡 Menyuda bu band bo\'lmasa — Chrome\'ni Play Market\'dan yangilang.</div>' + oyoq(3),
# 4 — 0.7.7: kirish va ruxsat (ruxsatgacha ilova ochilmaydi)
bosh('🔒', 'Kirish va ruxsat', 'Birinchi ochilganda — 3 daqiqa') + '<div class="qlar">' +
qadam(1, 'Tanishtiruv → «Ro\'yxatdan o\'tish»', 'Ilova o\'zi <b>5 ta rasmli slayd</b> bilan tanishtiradi. Oxirgisida — <b>«✉️ Ro\'yxatdan o\'tish / kirish»</b>.', f'<div class="row2">{tel("30_tanish1", 132, .43)}{tel("31_tanish5", 132, .43)}</div>') +
qadam(2, 'Email va yangi parol', 'Email va <b>yangi parol</b> (Gmail paroli emas) → <b>«Ro\'yxatdan o\'tish»</b>.', f'<div class="row2">{tel("20_akkaunt", 132, .5)}<div class="izoh">🔑 iPhone ham, Android ham — <b>faqat email + parol</b>. Parolni yozib qo\'ying: oilaning 2-telefonida ham kerak.</div></div>') +
qadam(3, 'Ruxsat so\'rang → Telegram', 'Oila nomi → <b>«📨 Ruxsat so\'rash»</b> → <b>«✈️ Telegram\'da egasiga yozish»</b> → Telegram\'da <b>➤</b> (yuborish).', f'<div class="row2">{tel("21_ruxsat_kerak", 132, .48)}{tel("22_kutilmoqda", 132, .48)}</div>') +
'</div><div class="eslat">⏳ Ruxsatgacha ilova ochilmaydi. Egasi ✅ bosishi bilan ekran <b>o\'zi</b> yangilanadi — keyingi sahifa.</div>' + oyoq(4),
# 5 — oila va bola (ruxsatdan keyin)
bosh('👨‍👩‍👧', 'Oila va bolalar', 'Ruxsatdan keyin — 2 daqiqa') + '<div class="qlar">' +
qadam(1, 'Oila nomi va ota-ona PIN', 'Oila nomini yozing va <b>4 raqamli PIN</b> o\'ylang — u ota-ona paneli uchun. <b>Bolalarga aytmang.</b>', f'<div class="row2">{tel("01_oila", 150, .7)}<div class="izoh">📱 <b>2-telefonda</b> (oyisi yoki dadasi): ilovani o\'rnating → tanishtiruv → <b>«Kirish»</b> — xuddi shu email va parol. Bolalar va natijalar o\'zi keladi.</div></div>') +
qadam(2, 'Bolani qo\'shing', '<b>Laqab</b> (ism-familiya emas), avatar va <b>sinf</b> → «Saqlash». Har bola uchun takrorlang.', f'<div class="row2">{tel("02_bola", 150, .62)}{tel("03_tanla", 150, .62)}</div>') +
'</div><div class="eslat">✅ Tayyor! Natijalar bulutda o\'zi saqlanadi. Bola o\'z rasmini bosadi va <b>«🚀 Missiyani boshlash»</b>.</div>' + oyoq(5),
# 6 — reyting va kundalik
bosh('🏆', 'Oilalar o\'rtasida reyting', 'Bolalar boshqa oila bolalari bilan musobaqalashadi') + '<div class="qlar">' +
qadam(1, 'Guruh kodini kiriting', 'Sizni taklif qilgan oiladan <b>10 belgili guruh kodini</b> so\'rang. 👨‍👩‍👧 → <b>«📲 Oila reytingi»</b> → kod → <b>«🔗 Qo\'shilish»</b>. Yoki egasiga yozing — o\'zi qo\'shib qo\'yadi.', f'<div class="row2">{tel("24_guruh_kod", 140, .42)}{tel("10_rekordlar", 140, .42)}</div>') +
'</div><div class="kun"><b>Har kuni</b><ul><li>🚀 <b>1 ta missiya</b> (20–35 daq) — keyin 🎮 <b>o\'yinlar zali</b> ochiladi.</li><li>🔑 Zalni missiyasiz ham ochish mumkin — ota-ona PIN bilan.</li><li>📊 Ota-ona panelida — <b>hafta xulosasi</b> va bolaning savollari.</li>'
f'<li>🔄 Yangi versiya chiqqanda — ilovani <b>yopib qayta oching</b> (tepada «v{VK}» yozuvi).</li></ul></div>'
'<div class="maxfiy kichik"><b>🔒 Eslatma</b><span>Ilova shaxsiy — boshqalarga ulashmang. Savol bo\'lsa — sizni taklif qilgan odamga yozing.</span></div>' + oyoq(6),
]

CSS = '''
@page { size: 540px 960px; margin: 0 }
*{box-sizing:border-box;margin:0;padding:0} html,body{background:#0B1020}
body{font-family:Inter,"Noto Color Emoji",sans-serif;color:#EAF0FF;-webkit-font-smoothing:antialiased}
.pg{width:540px;height:960px;position:relative;overflow:hidden;padding:30px 30px 0;page-break-after:always;
  background:radial-gradient(ellipse 90% 55% at 85% -5%,rgba(124,77,255,.30),transparent 60%),radial-gradient(ellipse 80% 50% at -10% 105%,rgba(0,184,212,.20),transparent 60%),linear-gradient(170deg,#121A30 0%,#0B1020 62%,#0A0E1A 100%)}
.pg:last-child{page-break-after:auto}
b{color:#fff;font-weight:700}
.cover{display:flex;flex-direction:column;align-items:center;text-align:center;padding-top:4px}
.logo{width:92px;height:92px;border-radius:22px;box-shadow:0 14px 34px -10px rgba(0,0,0,.8),0 0 0 1px rgba(255,255,255,.12)}
h1{font:800 46px/1.05 "Inter Display",Inter;letter-spacing:-.5px;margin-top:12px;background:linear-gradient(180deg,#fff,#BFD2FF);-webkit-background-clip:text;color:transparent}
.sub{color:#9AA8C7;font-size:15px;margin-top:4px;letter-spacing:.3px}
.taklif{margin-top:18px;padding:16px 18px 15px;border-radius:20px;text-align:left;background:linear-gradient(180deg,rgba(255,255,255,.08),rgba(255,255,255,.03));border:1px solid rgba(255,201,74,.45);box-shadow:0 20px 40px -24px rgba(0,0,0,.9)}
.tk{font:800 11px Inter;letter-spacing:2.4px;color:#FFC94A}.taklif p.bep{margin:9px 0 0;padding:7px 11px;border-radius:12px;font-weight:700;color:#FFE3A0;background:rgba(255,201,74,.12);border:1px solid rgba(255,201,74,.38)}.taklif p.bep b{color:#FFC94A}.taklif h3{font:800 21px/1.2 "Inter Display",Inter;margin:6px 0 7px}.taklif p{font-size:14.2px;line-height:1.5;color:#C9D3EA}
.fan{position:relative;height:236px;width:100%;margin-top:14px}
.fan .tel{position:absolute;top:10px}.fan .f1{left:28px;transform:rotate(-8deg)}.fan .f3{right:28px;transform:rotate(8deg)}.fan .f2{left:50%;margin-left:-75px;top:0;z-index:2}
.maxfiy{margin-top:12px;width:100%;padding:12px 14px;border-radius:16px;text-align:left;display:flex;flex-direction:column;gap:3px;background:rgba(255,82,82,.10);border:1px solid rgba(255,138,128,.45)}
.maxfiy b{font-size:14.5px}.maxfiy span{font-size:13px;line-height:1.42;color:#F1C9C5}.maxfiy.kichik{margin-top:12px}
.keyin{margin-top:12px;font-size:13.5px;color:#AEB9D3}
.bsh{display:flex;align-items:center;gap:12px;margin-bottom:14px}.bsh h2{font:800 27px/1.1 "Inter Display",Inter;letter-spacing:-.3px}.bsh small{display:block;color:#9AA8C7;font-size:13.5px;margin-top:3px}
.bic{font-size:30px;line-height:1}.bic:empty{display:none}.vpill{margin-left:auto;align-self:flex-start;font:700 12px Inter;padding:4px 9px;border-radius:999px;background:rgba(255,201,74,.16);color:#FFC94A;border:1px solid rgba(255,201,74,.4)}
.qlar{display:flex;flex-direction:column;gap:11px}
.qd{display:flex;gap:12px;padding:13px 14px;border-radius:18px;background:linear-gradient(180deg,rgba(255,255,255,.075),rgba(255,255,255,.025));border:1px solid rgba(255,255,255,.10)}
.qn{flex:0 0 34px;height:34px;border-radius:50%;display:flex;align-items:center;justify-content:center;font:800 17px Inter;color:#241A00;background:linear-gradient(160deg,#FFE08A,#F2B416);box-shadow:0 6px 14px -6px rgba(242,180,22,.8)}
.qm{flex:1;min-width:0}.qm>b{display:block;font-size:16.5px;line-height:1.25}.qm p{font-size:13.6px;line-height:1.45;color:#C2CCE3;margin-top:4px}
.url{display:inline-block;margin-top:7px;padding:7px 11px;border-radius:10px;background:#060A14;border:1px solid rgba(255,201,74,.55);color:#FFD772;font:600 13.4px "DejaVu Sans Mono",monospace;text-decoration:none;letter-spacing:-.2px}
.mk2{display:flex;gap:10px;align-items:flex-start;margin-top:9px}.mk2 svg{display:block;flex:1;width:0;height:auto;filter:drop-shadow(0 8px 14px rgba(0,0,0,.45))}
.row2{display:flex;gap:12px;align-items:flex-start;margin-top:9px}
.izoh{flex:1;font-size:12.8px;line-height:1.45;color:#C2CCE3;padding:10px 12px;border-radius:14px;background:rgba(255,201,74,.08);border:1px solid rgba(255,201,74,.28)}
.tel{flex:0 0 auto;border-radius:22px;padding:5px;background:linear-gradient(160deg,#2B3040,#06080D 40%,#1A1E29);box-shadow:0 18px 34px -14px rgba(0,0,0,.95),inset 0 0 0 1px rgba(255,255,255,.12);overflow:hidden}
.tel img{display:block;width:100%;border-radius:17px}
.eslat{margin-top:12px;font-size:13.4px;line-height:1.45;color:#C2CCE3;padding:11px 13px;border-radius:14px;background:rgba(0,184,212,.09);border:1px solid rgba(0,184,212,.32)}
.kun{margin-top:12px;padding:13px 15px;border-radius:18px;background:linear-gradient(180deg,rgba(124,77,255,.16),rgba(124,77,255,.05));border:1px solid rgba(124,77,255,.4)}
.kun>b{font-size:15.5px}.kun ul{list-style:none;margin-top:6px;display:flex;flex-direction:column;gap:5px}.kun li{font-size:13.4px;line-height:1.42;color:#D2D9EC}
.oyoq{position:absolute;left:30px;right:30px;bottom:18px;display:flex;justify-content:space-between;font-size:11.5px;color:#6F7C99;letter-spacing:.3px}
'''
HTML = '<!doctype html><html lang="uz"><head><meta charset="utf-8"><title>Bilimjon — yo\'riqnoma</title><style>' + CSS + '</style></head><body>' + ''.join(f'<section class="pg">{s}</section>' for s in SAHIFALAR) + '</body></html>'
hf = os.path.join(OUT, 'yoriqnoma.html'); open(hf, 'w', encoding='utf-8').write(HTML)
PDF = os.path.join(OUT, f'Bilimjon_yoriqnoma_v{VK}.pdf')
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(viewport={'width': 540, 'height': 960}, device_scale_factor=2)
    pg.goto('file://' + hf); pg.wait_for_timeout(600)
    toshdi = pg.evaluate("[...document.querySelectorAll('.pg')].map((s,i)=>{const m=Math.max(...[...s.querySelectorAll('.qlar,.kun,.eslat,.maxfiy,.keyin,.fan')].map(e=>e.getBoundingClientRect().bottom - s.getBoundingClientRect().top),0); return [i+1, Math.round(m)]})")
    print('sahifa pastki chegarasi (≤ 925 bo\'lsin):', toshdi)
    for i, el in enumerate(pg.query_selector_all('.pg')):   # Telegram albomi uchun JPEG (1080×1920)
        t = os.path.join(OUT, f'_s{i + 1}.png'); el.screenshot(path=t); Image.open(t).convert('RGB').save(os.path.join(OUT, f'Bilimjon_{i + 1}.jpg'), 'JPEG', quality=90, optimize=True); os.remove(t)
    pg.pdf(path=PDF, width='540px', height='960px', print_background=True, margin={'top': '0', 'bottom': '0', 'left': '0', 'right': '0'})
    br.close()
print('✅', PDF, f'({os.path.getsize(PDF) // 1024} KB)'); print('✅ JPG:', ', '.join(f'Bilimjon_{i + 1}.jpg' for i in range(len(SAHIFALAR))))
