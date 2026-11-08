"""Bilimjon 💻 KOMPYUTER YO'RIQNOMASI — Windows 10/11 ga o'rnatish (Edge / Chrome), ish stolidagi yorliq, foydalanish (6 sahifa 9:16).
Ishlatish:  python3 sinov/yoriqnoma/yoriqnoma_pc.py [papka=/tmp/bj_pc] [--suratsiz]
  → <papka>/Bilimjon_kompyuter_v8.pdf  +  <papka>/Bilimjon_PC_1.jpg … _6.jpg (1080×1920 — Telegram albomi uchun)
  • Uslub (CSS) — telefon yo'riqnomasidan (yoriqnoma.py) o'zi olinadi; ekranlar — suratlar_pc.py (haqiqiy ilova, 1100×720 oyna, namuna oila).
  • Windows/Edge/Chrome tugmalari — soddalashtirilgan chizma (logotipsiz), yozuvlar rus tilidagi Windows'dagidek, matnda inglizchasi ham.
  • Edge/Chrome menyu yo'llari 08.11.2026 da tekshirilgan: Edge «… → Приложения → Установить этот сайт как приложение», edge://apps → «Подробности»;
    Chrome «⋮ → Трансляция, сохранение и отправка → Установить страницу как приложение…». Brauzer yangilansa — matnni shu yerda tuzating.
  • Repoga faqat generator yoziladi; tayyor PDF/JPG — faqat chatda."""
import os, re, sys, html, subprocess, base64, io
from playwright.sync_api import sync_playwright
from PIL import Image
D = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.abspath(os.path.join(D, '..', '..'))
ARG = [a for a in sys.argv[1:] if not a.startswith('--')]
OUT = os.path.abspath(ARG[0] if ARG else '/tmp/bj_pc'); SUR = os.path.join(OUT, 'sur'); os.makedirs(SUR, exist_ok=True)
VER = re.search(r"A\.VER = '([\d.]+)'", open(os.path.join(SITE, 'index.html'), encoding='utf-8').read()).group(1)
VK = (lambda q: q[1] + ('.' + q[2] if q[2] != '0' else '') if q[0] == '0' else q[0] + '.' + q[1])(VER.split('.'))
SAYT = 'https://abdurazzoqzzuzb-max.github.io/bilimjon/'; SAYT_K = 'abdurazzoqzzuzb-max.github.io/bilimjon'
if '--suratsiz' not in sys.argv or not os.path.exists(os.path.join(SUR, 'pc_uy.png')):
    subprocess.run([sys.executable, os.path.join(D, 'suratlar_pc.py'), SUR], check=True)
CSS0 = re.search(r"\nCSS = '''(.*?)'''", open(os.path.join(D, 'yoriqnoma.py'), encoding='utf-8').read(), re.S).group(1)
ICON = 'data:image/png;base64,' + base64.b64encode((lambda b: (Image.open(os.path.join(SITE, 'icon-512.png')).convert('RGBA').resize((128, 128), Image.LANCZOS).save(b, 'PNG'), b.getvalue())[1])(io.BytesIO())).decode()
e = html.escape; S = 1.5   # suratlar 1.5× da

def kes(nom, x0, y0, x1, y1, w):   # ekran bo'lagi (CSS px) → JPEG data URI
    im = Image.open(os.path.join(SUR, nom + '.png')).convert('RGB').crop(tuple(round(v * S) for v in (x0, y0, x1, y1)))
    im = im.resize((w * 2, round(im.height * w * 2 / im.width)), Image.LANCZOS); b = io.BytesIO(); im.save(b, 'JPEG', quality=84, optimize=True)
    return 'data:image/jpeg;base64,' + base64.b64encode(b.getvalue()).decode()
def oyna(nom, kesim, w=480, cls=''):   # Bilimjon ilova oynasi (Windows oynasi kabi — sarlavha satri, − □ ×)
    return (f'<div class="oyna {cls}" style="width:{w}px"><div class="osar"><img src="{ICON}" alt=""><span>Bilimjon</span><i>—</i><i>☐</i><i class="x">✕</i></div>'
            f'<img class="oimg" src="{kes(nom, *kesim, w)}" alt=""></div>')
def qadam(n, sar, mat, rasm=''): return f'<div class="qd"><div class="qn">{n}</div><div class="qm"><b>{sar}</b><p>{mat}</p>{rasm}</div></div>'
def bosh(ic, sar, kichik=''): return f'<div class="bsh"><span class="bic">{ic}</span><div><h2>{sar}</h2>{f"<small>{kichik}</small>" if kichik else ""}</div><span class="vpill">v{VK}</span></div>'
def oyoq(n): return f'<div class="oyoq"><span>Bilimjon · kompyuterda (Windows)</span><span>{n} / 6</span></div>'
LINK = f'<a class="url" href="{SAYT}">{e(SAYT_K)}</a>'
UZ = lambda s: f'<span class="ru">«{s}»</span>'   # Windows/brauzer tugmasi yozuvi (rus tilida)

# ---------- soddalashtirilgan chizmalar (logotipsiz) ----------
INST = '<svg viewBox="0 0 24 24" width="17" height="17"><rect x="3" y="4" width="15" height="11" rx="2" fill="none" stroke="#1B1B1B" stroke-width="1.8"/><path d="M8 19h6M11 15v4" stroke="#1B1B1B" stroke-width="1.8" stroke-linecap="round"/><path d="M19 10v6M16 13h6" stroke="#0067C0" stroke-width="2.2" stroke-linecap="round"/></svg>'
def mk_bar(menu=False):
    m = ('<div class="mmenu"><div>Новая вкладка</div><div>Избранное</div><div class="on">Приложения <em>›</em></div><div>Параметры</div>'
         f'<div class="sub"><div class="ring">{INST}Установить этот сайт как приложение</div><div>Просмотреть приложения</div></div></div>') if menu else ''
    return (f'<div class="mk"><div class="mbar"><span class="mdot"></span><div class="maddr">🔒 {e(SAYT_K)}</div><span class="mic ring">{INST}</span><span class="mic mdots">⋯</span></div>{m}</div>')
def mk_ornat():
    return (f'<div class="mk mdlg"><b>Установить приложение</b><div class="mapp"><img src="{ICON}" alt=""><div><span>Bilimjon</span><small>{e(SAYT_K)}</small></div></div>'
            '<div class="mbtn"><span class="pri ring">Установить</span><span>Отмена</span></div></div>')
def mk_tanlov():
    t = lambda s, on: f'<div class="mchk {"on" if on else ""}"><i>{"✓" if on else ""}</i>{s}</div>'
    return (f'<div class="mk mdlg"><div class="mapp"><img src="{ICON}" alt=""><div><span>Bilimjon установлено</span><small>Где показывать приложение?</small></div></div>'
            + t('Закрепить на панели задач', 1) + '<div class="ring rb">' + t('Создать ярлык на рабочем столе', 1) + '</div>'
            + t('Разрешить автозапуск при входе', 0) + '<div class="mbtn"><span class="pri ring">Разрешить</span><span>Не разрешать</span></div></div>')
def mk_stol():   # ish stoli: yorliq + vazifalar paneli
    ic = lambda s, c: f'<div class="dic"><span style="background:{c}"></span><small>{s}</small></div>'
    return (f'<div class="desk"><div class="dicons">{ic("Корзина", "#7A8BA8")}{ic("Этот компьютер", "#4C8BD6")}'
            f'<div class="dic bj ring"><img src="{ICON}" alt=""><small>Bilimjon</small></div></div>'
            f'<div class="tbar"><span class="tst">Пуск</span><span class="tic"></span><span class="tic"></span><span class="tic bj ring"><img src="{ICON}" alt=""></span><span class="tic"></span></div></div>')
def mk_pusk():   # Пуск → Все приложения → Bilimjon → ish stoliga sudrash
    return (f'<div class="mk mpusk"><div class="mps"><b>Все приложения</b><div>Блокнот</div><div class="bj ring"><img src="{ICON}" alt="">Bilimjon</div><div>Калькулятор</div><div>Камера</div></div>'
            f'<div class="sudr"><span>sichqoncha bilan<br>ushlab sudrang</span><b>➜</b><div class="dic bj"><img src="{ICON}" alt=""><small>Bilimjon</small></div><em>ish stoli</em></div></div>')

# ======================= SAHIFALAR =======================
SAHIFALAR = [
# 1 — muqova
f'''<div class="cover"><img class="logo" src="{ICON}" alt=""><h1>Bilimjon</h1><div class="sub">kompyuterda · Windows 10 / 11 · v{VK}</div>
{oyna('pc_uy', (300, 0, 800, 380), 400, 'cov')}
<div class="kun chap"><b>Nima kerak</b><ul>
<li>💻 <b>Windows 10 yoki 11</b> kompyuter yoki noutbuk</li>
<li>🌐 <b>Microsoft Edge</b> (Windows'da o'zi bor) yoki <b>Google Chrome</b> va internet</li>
<li>🔑 <b>Oila akkaunti</b> — telefondagi Bilimjon'ning <b>email va paroli</b>. Akkaunt hali yo'q bo'lsa — avval telefon yo'riqnomasi bo'yicha oching.</li></ul></div>
<div class="kun chap yashil"><b>Kompyuterda nima yaxshi</b><ul><li>🖥️ Katta ekran, ish stolida o'z belgisi, brauzer tablarisiz alohida oyna</li><li>🔄 Ilova o'zi yangilanadi; natijalar telefon bilan bitta oilada</li></ul></div>
<div class="keyin">⏱ O'rnatish — 3 daqiqa: <b>2-sahifa — Edge</b>, <b>3-sahifa — ish stolidagi belgi va Chrome</b></div></div>{oyoq(1)}''',
# 2 — Edge
bosh('🌐', "Edge'da o'rnatish", 'Tavsiya — Windows\'ning o\'z brauzeri') + '<div class="qlar">' +
qadam(1, "Edge'ni oching va manzilni yozing", f'Manzil satriga yozing (yoki havolani bosing):<br>{LINK}') +
qadam(2, "O'rnatish belgisini bosing", f'Manzil satri o\'ngidagi <b>□+</b> belgi. Ko\'rinmasa: <b>⋯</b> → {UZ("Приложения")} → {UZ("Установить этот сайт как приложение")} <small>(ingl.: Apps → Install this site as an app)</small>.', mk_bar(True)) +
qadam(3, f'{UZ("Установить")} ni bosing', 'Bilimjon alohida oynada ochiladi — endi u kompyuterdagi ilova.', mk_ornat()) +
qadam(4, 'Ish stoliga belgi qo\'ying', f'Chiqqan oynada {UZ("Создать ярлык на рабочем столе")} va {UZ("Закрепить на панели задач")} ni belgilang → {UZ("Разрешить")}. «Avtozapusk» — <b>belgilamang</b>.', mk_tanlov()) +
'</div>' + oyoq(2),
# 3 — ish stoli belgisi + Chrome
bosh('🖥️', 'Ish stolidagi belgi', "Belgi chiqmagan bo'lsa yoki Chrome ishlatsangiz") + '<div class="qlar">' +
qadam(1, "Пуск'dan sudrab olish — eng oson", f'{UZ("Пуск")} → {UZ("Все приложения")} → <b>Bilimjon</b>ni sichqoncha bilan ushlab, ish stoliga sudrab tashlang.', mk_pusk()) +
qadam(2, 'Edge orqali', f'Manzil satriga <code>edge://apps</code> yozing → Bilimjon → {UZ("Подробности")} → {UZ("Создать ярлык на рабочем столе")}.') +
qadam(3, "Google Chrome'da o'rnatish", f'<b>⋮</b> → {UZ("Трансляция, сохранение и отправка")} → {UZ("Установить страницу как приложение…")} → {UZ("Установить")} <small>(ingl.: Cast, save and share → Install page as app)</small>. Belgi: <code>chrome://apps</code> → Bilimjon ustida o\'ng tugma → {UZ("Создать ярлыки")} → {UZ("Рабочий стол")}.') +
'</div><div class="row3">' + mk_stol() + f'<div class="izoh">✅ Natija: ish stolida va pastdagi panelda <b>Bilimjon</b> belgisi. Ikki marta bosing — ilova ochiladi.<br><br>📌 Panelga mahkamlash: Bilimjon ochiq turganda pastdagi belgisi ustida o\'ng tugma → {UZ("Закрепить на панели задач")}.</div></div>' + oyoq(3),
# 4 — birinchi ochish
bosh('🔑', 'Birinchi ochish', 'Telefondagi oila akkaunti bilan') + '<div class="qlar">' +
qadam(1, f'{UZ("Kirish")} — Ro\'yxatdan o\'tish EMAS', 'Ish stolidagi Bilimjon → tanishtiruvni varaqlang → telefondagi <b>xuddi shu email va parol</b> → <b>«Kirish»</b>. Bolalar va natijalar o\'zi keladi. «Ro\'yxatdan o\'tish» — yangi, bo\'sh oila ochadi.', oyna('pc_kirish', (290, 335, 810, 615), 360)) +
qadam(2, 'Bolani tanlang va o\'ynang', 'Bosh ekranda — «Kim o\'ynaydi?». Ota-ona paneli (👨‍👩‍👧 belgisi, PIN bilan) kompyuterda ham to\'liq ishlaydi.') +
'</div><div class="eslat ogoh"><b>📱 Bitta bola — bitta qurilma.</b> Bola telefonda o\'ynab yurgan bo\'lsa, kompyuterda <b>«boshqa qurilmada o\'ynaydi»</b> chiqadi — yulduz va natijalar aralashmasin. Kompyuterga o\'tkazish: <b>«🔑 Endi shu qurilmada o\'ynasin»</b> → ota-ona PIN. Shundan keyin telefonda bu bola ochilmaydi (qaytarish — telefonda xuddi shunday).</div>' +
oyna('pc_qurq', (305, 210, 795, 480), 330, 'mrk') + oyoq(4),
# 5 — foydalanish
bosh('🖱️', "Kompyuterda o'ynash", 'Sichqoncha, klaviatura, ovoz') +
oyna('pc_savol', (300, 0, 800, 330), 440, 'mrk') +
'''<div class="kun"><b>Qulay qilish</b><ul>
<li>🖱️ Javoblar va o'yinlar — <b>sichqoncha</b> bilan (sudrash — bosib turib). Sensorli ekranda — barmoq bilan ham.</li>
<li>🔍 Kattaroq ko'rinsin: <b>Ctrl</b> va <b>+</b> (kichraytirish — Ctrl va −, asl holi — <b>Ctrl + 0</b>). Oynani to'liq yoying — ☐ tugma.</li>
<li>🔊 Savollar ovozda o'qiladi: karnay yoki naushnik yoqilgan bo'lsin; 🔊 tugma — qayta eshitish.</li>
<li>⏱ Kun chegarasi, uyqu vaqti, dam olish o'yini (1 daqiqa) — kompyuterda ham xuddi telefondagidek.</li>
<li>🌐 Natijalar bulutga saqlanadi — telefondagi ota-ona panelida ham ko'rinadi. Internet qisqa uzilsa ham o'ynash davom etadi, keyin o'zi yuboriladi.</li></ul></div>''' + oyoq(5),
# 6 — yangilanish va savollar
bosh('🔄', 'Yangilanish va savollar') + '<div class="qlar">' +
qadam(1, 'Ilova o\'zi yangilanadi', 'Yangi versiya chiqsa — <b>«🆕 Bilimjon … keldi»</b> oynasi, 3 soniyada o\'zi yangilanadi. Dars paytida — pastda «Yangilash / Keyinroq». Natijalar saqlanadi.') +
qadam(2, 'Versiyani tekshirish', f'Tepada <b>v{VK}</b>. Ota-ona → ⚙️ Sozlamalar → <b>«📲 Versiya»</b> → «🔄 Yangilanishni tekshirish». Eski raqam qolsa — Bilimjon oynasini yoping (✕) va qayta oching yoki <b>F5</b>.') +
'</div><div class="kun"><b>Savollar</b><ul>'
"<li>❓ <b>O'rnatish belgisi yo'q</b> — manzil to'liq yozilganini tekshiring (oxiri <b>/bilimjon/</b>), sahifa ochilib bo'lsin, keyin <b>⋯</b> menyudan (2-sahifa).</li>"
"<li>❓ <b>Parol noto'g'ri</b> — «Parolni unutdim» → email'ga tiklash havolasi keladi. Bu Gmail paroli emas — Bilimjon uchun o'ylab topilgan parol.</li>"
"<li>❓ <b>Bola ochilmayapti</b> — u boshqa qurilmada (4-sahifa).</li>"
f"<li>❓ <b>O'chirish</b> — <code>edge://apps</code> → Bilimjon → {UZ('Удалить')} (Chrome: <code>chrome://apps</code> → o'ng tugma → {UZ('Удалить из Chrome')}). Natijalar bulutda qoladi.</li>"
"<li>⚠️ Brauzer tarixini «hamma ma'lumotlar» bilan tozalamang — Bilimjon'ga qayta «Kirish» kerak bo'ladi.</li></ul></div>"
'<div class="maxfiy kichik"><b>🔒 Eslatma</b><span>Ilova shaxsiy — havolani boshqalarga ulashmang. Natijalar ilova egasi tomonidan o\'quv rejasi uchun ko\'rib chiqiladi. Savol bo\'lsa — sizni taklif qilgan odamga yozing.</span></div>' + oyoq(6),
]

CSS = CSS0 + '''
.ru{font-weight:700;color:#FFE3A0;white-space:normal}.qm small,.qm p small{color:#8E9AB8;font-size:12px}
code{font:600 12.6px "DejaVu Sans Mono",monospace;color:#FFD772;background:#060A14;border:1px solid rgba(255,201,74,.4);padding:1px 6px;border-radius:7px}
.oyna{margin:10px auto 0;border-radius:12px;overflow:hidden;background:#202020;box-shadow:0 18px 34px -14px rgba(0,0,0,.95),0 0 0 1px rgba(255,255,255,.14)}
.oyna.cov{margin-top:14px}.oyna.mrk{margin-top:10px}
.osar{display:flex;align-items:center;gap:7px;height:26px;padding:0 0 0 9px;background:#2B2B2B;color:#E8E8E8;font:600 11.5px Inter}
.osar img{width:14px;height:14px;border-radius:3px}.osar span{flex:1}.osar i{font-style:normal;width:34px;text-align:center;color:#CFCFCF;font-size:11px}.osar i.x{color:#E8E8E8}
.oimg{display:block;width:100%}
.kun.chap{text-align:left;width:100%}.kun.yashil{background:linear-gradient(180deg,rgba(0,200,120,.14),rgba(0,200,120,.04));border-color:rgba(0,200,120,.42)}
.mk{margin-top:8px;background:#F7F7F7;color:#1B1B1B;border-radius:12px;padding:7px 8px;font:500 11px/1.25 Inter;box-shadow:0 10px 22px -12px rgba(0,0,0,.9);position:relative}
.mk b{color:#1B1B1B}.ring{outline:3px solid #FFC94A;outline-offset:2px;border-radius:8px}
.mbar{display:flex;align-items:center;gap:7px}.mdot{width:10px;height:10px;border-radius:50%;background:#C9C9C9}
.maddr{flex:1;background:#fff;border:1px solid #DADADA;border-radius:999px;padding:5px 10px;font:500 11px "DejaVu Sans Mono",monospace;color:#333;white-space:nowrap;overflow:hidden}
.mic{display:flex;align-items:center;justify-content:center;width:26px;height:24px;border-radius:7px}.mdots{font-size:16px;font-weight:800;color:#333}
.mmenu{display:flex;gap:8px;margin-top:6px;align-items:flex-start}.mmenu>div:not(.sub){display:none}
.mmenu{flex-wrap:wrap}.mmenu>div.on{display:block;padding:6px 10px;background:#E6EEF8;border-radius:7px;font-weight:700}.mmenu em{font-style:normal;color:#666}
.mmenu .sub{display:flex;flex-direction:column;gap:4px;background:#fff;border:1px solid #E2E2E2;border-radius:9px;padding:6px;flex:1}
.mmenu .sub>div{display:flex;align-items:center;gap:7px;padding:3px 7px;border-radius:7px;font-size:11px;color:#1B1B1B}.mmenu .sub>div:last-child{color:#777}
.mdlg{padding:8px 11px;display:flex;flex-direction:column;gap:4px}.mapp{display:flex;align-items:center;gap:9px}.mapp img{width:30px;height:30px;border-radius:7px}
.mapp span{display:block;font-weight:700;font-size:12.5px}.mapp small{color:#666;font-size:10.5px}
.mbtn{display:flex;gap:8px;justify-content:flex-end;margin-top:2px}.mbtn span{padding:5px 13px;border-radius:7px;border:1px solid #D0D0D0;background:#fff;font-weight:600}
.mbtn span.pri{background:#0067C0;color:#fff;border-color:#0067C0}
.mchk{display:flex;align-items:center;gap:8px;padding:2px 2px}.mchk i{width:15px;height:15px;border-radius:4px;border:1.5px solid #8A8A8A;display:flex;align-items:center;justify-content:center;font-style:normal;font-size:10px;color:#fff;font-weight:800}
.mchk.on i{background:#0067C0;border-color:#0067C0}.rb{padding:1px 0}
.mpusk{display:flex;gap:10px;align-items:center}.mps{flex:0 0 170px;background:#fff;border:1px solid #E2E2E2;border-radius:10px;padding:7px;display:flex;flex-direction:column;gap:3px}
.mps>div{padding:4px 7px;border-radius:6px;color:#444}.mps>div.bj{display:flex;align-items:center;gap:7px;color:#1B1B1B;font-weight:700;background:#EEF4FB}.mps img{width:16px;height:16px;border-radius:4px}
.sudr{flex:1;display:flex;align-items:center;gap:8px;color:#444;font-size:10.5px;line-height:1.3}.sudr b{font-size:22px;color:#0067C0}.sudr em{font-style:normal;color:#777}
.dic{display:flex;flex-direction:column;align-items:center;gap:3px;width:62px;text-align:center}.dic img,.dic span{width:34px;height:34px;border-radius:8px;display:block}.dic small{font-size:9.5px;line-height:1.15}
.row3{display:flex;gap:12px;align-items:stretch;margin-top:11px}.row3 .izoh{font-size:12.6px}
.desk{flex:0 0 200px;height:206px;border-radius:12px;position:relative;overflow:hidden;background:linear-gradient(150deg,#1D4E89,#3C7CC4 55%,#86B7E8);box-shadow:0 10px 22px -12px rgba(0,0,0,.9)}
.dicons{position:absolute;left:10px;top:8px;display:flex;flex-direction:column;gap:3px}.desk .dic{color:#fff}.desk .dic span{opacity:.9}
.tbar{position:absolute;left:0;right:0;bottom:0;height:30px;background:rgba(240,243,248,.88);display:flex;align-items:center;justify-content:center;gap:7px}
.tst{font:700 9px Inter;color:#1B1B1B;padding:3px 6px;border-radius:5px;background:#fff}.tic{width:18px;height:18px;border-radius:5px;background:#9FB0C8;display:block}.tic.bj{background:none}.tic img{width:18px;height:18px;border-radius:4px;display:block}
'''
HTML = '<!doctype html><html lang="uz"><head><meta charset="utf-8"><title>Bilimjon — kompyuter yo\'riqnomasi</title><style>' + CSS + '</style></head><body>' + ''.join(f'<section class="pg">{s}</section>' for s in SAHIFALAR) + '</body></html>'
hf = os.path.join(OUT, 'yoriqnoma_pc.html'); open(hf, 'w', encoding='utf-8').write(HTML)
PDF = os.path.join(OUT, f'Bilimjon_kompyuter_v{VK}.pdf')
with sync_playwright() as p:
    br = p.chromium.launch(); pg = br.new_page(viewport={'width': 540, 'height': 960}, device_scale_factor=2)
    pg.goto('file://' + hf); pg.wait_for_timeout(600)
    toshdi = pg.evaluate("[...document.querySelectorAll('.pg')].map((s,i)=>{const m=Math.max(...[...s.querySelectorAll('.qlar,.kun,.eslat,.maxfiy,.keyin,.oyna,.row3')].map(e=>e.getBoundingClientRect().bottom - s.getBoundingClientRect().top),0); return [i+1, Math.round(m)]})")
    print('sahifa pastki chegarasi (≤ 925 bo\'lsin):', toshdi)
    for i, el in enumerate(pg.query_selector_all('.pg')):
        t = os.path.join(OUT, f'_s{i + 1}.png'); el.screenshot(path=t); Image.open(t).convert('RGB').save(os.path.join(OUT, f'Bilimjon_PC_{i + 1}.jpg'), 'JPEG', quality=90, optimize=True); os.remove(t)
    # PDF = sahifa rasmlari + bosiladigan havolalar (telefon yo'riqnomasidagidek — iPhone/Telegram ko'rgichida xavfsiz)
    hav = pg.evaluate("[...document.querySelectorAll('.pg')].map(s=>{const o=s.getBoundingClientRect(); return [...s.querySelectorAll('a[href]')].map(a=>{const r=a.getBoundingClientRect(); return [a.href, r.left-o.left, r.top-o.top, r.width, r.height, a.classList.contains('url') ? a.textContent : '']})})")
    def sah(i):
        d = base64.b64encode(open(os.path.join(OUT, f'Bilimjon_PC_{i + 1}.jpg'), 'rb').read()).decode()
        a = ''.join(f'<a class="{"url pu" if t else ""}" href="{h}" style="position:absolute;left:{x:.1f}px;top:{y:.1f}px;width:{w:.1f}px;height:{hh:.1f}px">{e(t)}</a>' for h, x, y, w, hh, t in hav[i])
        return f'<section style="position:relative;width:540px;height:960px;overflow:hidden;page-break-after:always;break-after:page"><img src="data:image/jpeg;base64,{d}" style="display:block;width:540px;height:960px">{a}</section>'
    pg.set_content('<!doctype html><html><head><meta charset="utf-8"><style>@page{size:540px 960px;margin:0}html,body{margin:0;padding:0;background:#0B0F1A}' + re.search(r'\.url\{[^}]*\}', CSS).group(0) + '.pu{box-sizing:border-box;margin:0;display:flex;align-items:center;justify-content:center;padding:0;white-space:nowrap}</style></head><body>' + ''.join(sah(i) for i in range(len(SAHIFALAR))) + '</body></html>')
    pg.wait_for_timeout(300)
    pg.pdf(path=PDF, width='540px', height='960px', print_background=True, margin={'top': '0', 'bottom': '0', 'left': '0', 'right': '0'})
    br.close()
print('✅', PDF, f'({os.path.getsize(PDF) // 1024} KB)'); print('✅ JPG:', ', '.join(f'Bilimjon_PC_{i + 1}.jpg' for i in range(len(SAHIFALAR))))
