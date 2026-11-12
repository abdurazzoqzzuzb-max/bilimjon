# Bilimjon — Claude uchun qisqa xotira

Javoblar o'zbekcha. Repo PUBLIC: ism, familiya, oila ma'lumoti, Telegram manzili, email yozilmaydi (sinovlarda — o'ylab topilgan).
**Limit tejash (08.11, u «o'zing hal qil»):** bu fayl har chatda yuklanadi — QISQA saqlanadi. Batafsil tarix va eski qarorlar — `docs/TARIX.md` (avtomatik yuklanmaydi; `grep -n "<so'z>" docs/TARIX.md` → faqat kerakli bo'lim). Yangi versiya tugaganda: bu yerga 3–6 qator, tafsilot — TARIX oxiriga.

## Loyiha
- Oilaviy o'yin-darslik (PWA), maktabgacha + 1–2-sinf. Sayt: https://abdurazzoqzzuzb-max.github.io/bilimjon/ (GitHub Pages, main / root). Beta: `…/bilimjon/beta/` (main'dagi `beta/`).
- Fayllar: `index.html` (butun ilova, 23 ta `<script>`), `sw.js`, `manifest.webmanifest`, ikonlar, `firestore.rules` (NAMUNA: `__ADMIN_UID__`), `qoidalar/firestore-0.5.0.rules` (orqaga), `admin/` (Claude boshqaruvi), `sinov/`, `docs/TARIX.md`. FAQAT main'da: `beta/`, `ovoz/` (neyron mp3, `iboralar.json`, `skript/yasa.py`), `.github/workflows/ovoz.yml`.
- Firebase **bilimjon-4c008** (Spark, eur3), kirish — email + parol (iPhone'da Google yo'q). SDK gstatic 13.2.0, faqat akkauntli telefonda yuklanadi.

## Versiya va chiqarish
- Saytda va beta'da: **0.9.1** («v9.1», 12.11; 0.8.0 dan to'g'ri: 🌳 daraxt, 🔁 xato savol, 🎯 3 qiyin, 👀 ko'z dami, 🏃 estafeta, 🆕 yangilik turi + 👏 olqish, 🃏 albom, 🎯 o'z maqsadi, 🔥 olov, 📖 hikoya, 👨‍👩‍👧 viktorina, 🎤 ovozim). Qoidalar Firebase'da: **0.9.1** (azo: ixtiyoriy zal, bu, dz, ol).
- Har versiyada uchalasi: `index.html` → `A.VER = 'x.y.z'`, `sw.js` → `P + 'x.y.z'`, **`version.json`** → `ver`, `verk`, `yangi[]` (bolalar tushunadigan 2–4 qator «Nima yangi»); ekranda `A.VERK` («v8»); `start()` dagi versiya toast'i.
- 🔄 Yangilanish (0.8.0): ilova `version.json` ni tekshiradi (ochilganda, qaytganda, 20 daq) → faoliyatda emas — o'zi yangilanadi (oyna 3 s), faoliyatda — tasma [Yangilash][Keyinroq]. Eski telefon albatta yangilansin desangiz: `min` = yangi ver (majburiy — faoliyatda ham 5 s). Sinov: `sinov/v080/sinov_yangilash.py`. 0.7.9 va eskilarda bu kod yo'q — ular 0.8.0 ga faqat ilovani qayta ochganda o'tadi.
- Tartib: yangi tarmoq `v0.x.y` (main'dan) → har bosqich push → beta: main worktree'da `python3 sinov/beta/beta_yig.py origin/<tarmoq> beta` → faqat `beta/` commit → u sinaydi → **«chiqar»** desa: `prod_e2e.py` (eski main vs main+tarmoq, 23 tekshiruv) → main'ga `merge --no-ff` → push → GitHub API deployments (github.io proksida yopiq) → qoidalar o'zgargan bo'lsa `qoidalar <oila emaili>`.
- Orqaga: `git revert -m 1 <merge>`; qoidalar eski ilova bilan mos qilib yoziladi; to'liq eski — admin `qoidalar - eski`.

- 🧪 **Beta = 0.9.0** («v9», tarmoq `v0.9.0` = v0.8.2 ustiga, 11.11; u «chiqar» desa saytga — 0.8.1–0.8.2 ham birga). 2-bosqich: 🌳 daraxt (`A.daraxt`, `b.daraxt`, ota-ona sovg'alari `S.dsov` — oila hujjati, `#daraxt`, `#daraxt-m-<tugun>`), 🔁 aynan xato savol 1–3–7 kun (`b.xq` ≤ 12, `A.xqYoz/xqNatija`, missiya qadami `xato`), 🎯 kunning 3 qiyini (`A.q3`, `b.q3`, `#qiyin3`, tur `qiyin3` — recordAnswer'ga kirmaydi), 👀 ko'zga dam 15 daq/20 s (`kozDam`; o'chiq — `sozlama.kozDam === false`), 🏃 estafeta (`A.estafeta`, `#estafeta`; guruh a'zo yozuviga `bu`/`dz`), 🆕 yangilik turi + 🔔 unutilgan bo'lim eslatmasi (`A.yangilik`, `VER_YANGI` — har yangi versiyada to'ldiring; `b.kor/b.yv/b.esYop`). ⚠️ **Qoidalar 0.9.0** (azo: ixtiyoriy `bu`, `dz`): «chiqar» da merge'dan OLDIN `qoidalar <admin email>`; eski qoidada ham ishlaydi (rad etilsa ularsiz yozadi, `L.sync.gx`). 0.8.2 va 0.9.0 tafsiloti — TARIX (v0.9.0 tarmog'ida).
- 🗺️ **Reja (u 10.11 tanladi, «hammasi yoqdi»):** ✅ 2-bosqich (0.9.0, beta). Qoldi — 3-bosqich: 📈 TAHLIL + individual reja (`docs/TAHLIL.md`), 🎤 o'qishni ovozga yozish; tanlovlar: 11 🧑‍🏫 «Men o'qituvchiman», 12 🛒 hayotiy vazifa (rasm + ota-ona tasdig'i), 13 🏫 maktab mavzusiga moslash, 14 📜 oylik diplom PDF.

## Sinov
- Hammasi: **`bash sinov/hammasi.sh`** (2 qator parallel — CPU 2 yadro; har sinovga 1 qator natija). Yakka: `python3 sinov/vXXX/<fayl>.py`, `node sinov/admin/sinov_admin.js`. `node --check` — har `<script>` bloki (hammasi.sh qiladi).
- `?tez=1` — tez rejim, `#sinov-<tugun>-<q>`, `window.__bjCur/__bjJavob/__bjOyin/__bjZal/__bjChipta/__bjUch`. Soxta Firebase: `sinov/bulut/fs.js`, `auth.js` (gstatic yo'naltiriladi, ombor + qoidalar Python'da).
- 🔒 Yangi telefon eshigi localhost'da va `?tez=1` da O'CHIQ; sinovda `?eshik=1`.
- Tasodifiy yiqilishi mumkin (qayta ishga tushiring): `v060/4` ovchi q3, `v071` «o'rniga yangi savol», `v070/1c` parallel yuklamada.

## Kod xaritasi (index.html, tartib bilan)
Kontent banki `BJ.bank` → generatorlar `BJ.gen` (mat M0–M2, mantiq L, ona tili H, yozuv Y, OL, EN, AR, KASHF, arab 2 `BJ.arab`: AQ/AY/TJ.1–8) → core `BJ.A` (holat `A.S()`, log, `makeItem`, `buildMission`, `recordAnswer`, kun chegarasi, xulosa) → bola tomoni (router `render()`, missiya, mashq, vazifa, arena, kichik dars + kino, Tushunmadim, 📖 tanishtiruv `screenTanish`) → o'yinlar `A.oyin` → garaj → zal `A.zal` → so'm `A.pul` → bozor `A.bozor` → xarita `A.xarita` → 🌳 `A.daraxt` → 🏃 `A.estafeta` → 🆕 `A.yangilik` → 🧩 0.9.1 (`A.t91`, `A.olov`, `A.maqsad`, `A.albom`, `A.hikoya`, `A.olqish`, `A.viktorina`, `A.ovozim`) → uch o'qish `A.uch` → ovoz `A.ovoz` → ☁️ bulut (sinxron, 🛡️ ruxsat, 👑 hamma oilalar, ✈️ Telegram, 🔒 `A.eshik`, reyting guruhi) → ota-ona paneli (`ota-*`) → `start()`.

## O'zgarmas qoidalar (buzilsa — xato bo'lgan)
- Oila darajasidagi yangi sozlamani `defaults()` ga QO'SHMANG (`migrate` umumiy holatni o'zgartirib, bulut yangiligini bosib ketadi) — `=== 'x'` / `!== false` bilan o'qing.
- `fixBola`/`migrate` ichida faqat hoisted `function` yoki ichki o'zgaruvchi (TDZ — holat bo'sh qaytgan).
- NUTQ yoki generator matni o'zgarsa — `python3 sinov/ovoz/inventar.py ovoz/iboralar.json` → main'ga push (Actions mp3 yasaydi). Ovozni o'sha id bilan qayta yasasangiz — `sw.js` `OV` ni oshiring.
- Lookbehind regex yo'q (eski iOS). Firestore hujjati ≤1 MB (`S.sovga` + `S.dokon` rasmlari ~720 KB — oshirmang).
- Dizayn: realistik + animatsiya, multfilm emas (u 4 marta aytgan). 390 px da gorizontal siljish yo'q.
- 👆 Ikki marta bosish zoom'i yo'q (0.7.8, u so'radi): `html{touch-action:manipulation}`, hamma input ≥ 16px. Ikki barmoq bilan kattalashtirish QOLADI (u tanladi) — viewport'ga `user-scalable=no` qo'ymang. touchend bilan ikki bosishni to'xtatmang (o'yinlarda tez bosish yo'qoladi).
- 🔐 Pul FOIZSIZ (0.7.9, u: «pul tegilmasa ko'payadi — islomiy jihatdan to'g'ri emas»): sandiqchaga foiz/o'sish qo'shmang, 🐷 cho'chqa tasvirini ishlatmang. Tejash — faqat ota-ona mukofoti (bozor 🪙) yoki orzu uchun yig'ish.
- 🧩 0.9.1 maydonlari (`b.olq/albom/maqsad/mqTarix/olovMax/olovBos/hikoya/ovozYoz`, `S.vikt/viktOchiq`) defaults'ga QO'SHILMAGAN. Olqish — faqat 6 tayyor ibora (erkin matn bolalar orasida YO'Q). 🎤 ovoz fayli faqat IndexedDB'da — bulutga yubormang. Yangi bo'lim qo'shsangiz: `A.yangilik.B` + `bolimOf` + `VER_YANGI[ver]` (tur — doim birinchi kirilmagani).
- `obuna`: bulut hujjati `q === 'admin'` bo'lsa undagi `guruh` olinadi.
- 📱 Bitta bola — bitta qurilma (0.8.0): `b.qurilma {id, nom, ts}` — bolaDefaults'ga QO'SHILMAGAN; sinxronda qurilma maydoni yangirog'i (ts) qoladi (`bolaQabul`, `qurOl`). ⏱ O'yin vaqti — `oyinMin` (oila/bola, bo'sh = 1 daq); eski `oyinDaq` o'qilmaydi.

## 🇬🇧 Road to 8 (IELTS) — `ielts/` (0.4.0, 08.11)
- Alohida sahifa `…/bilimjon/ielts/` — bolalar ilovasiga tegmaydi (o'z SW'i yo'q). Manba endi `ielts/index.html` o'zi (0.3.0 planshet HTML + ☁️ bulut moduli). Versiya: `R8.meta.version` + `ielts/version.json` (ilova o'zi yangilanadi, mashq paytida emas).
- Bulut (qoidalar o'zgarmagan): `oila/{uid}/ielts/holat` (`j` = to'liq holat JSON, ≤60 s / mashq tugashi bilan), `jonli` (≤30 s), `sozlama.norma` (faqat admin). Kirish — Bilimjon akkaunti + 🛡️ ruxsat («Road to 8 (IELTS)»); admin akkaunt → 👑 nazorat paneli (jonli, 7 kun, mashqlar, norma, JSON). Faqat Chrome (boshqa brauzer → `intent://` Chrome).
- 0.4.0: ⚠️ taxmin (o'qishga yetmaydigan vaqt) va ℹ️ 12 soat ichida qayta to'plam — natija/XP/muhrga kirmaydi; takrorlash — darsning 1-qadami; norma 120 daq (yakshanba yarmi); bosh sahifa — norma + bitta tugma.
- Hafta rejasi (u tasdiqlagan): Tokyo/London + MP3, eslatmalar + 21:00 Telegram hisobot, Bilimjon reytingi (reja % bo'yicha) + zal qulfi, diagnostik mock.

## 👑 Admin (Claude chatdan; telefon/akkaunt yo'qolsa ham)
- Yopiq repo `abdurazzoqzzuzb-max/bilimjon-admin`, workflow `admin.yml` (main'dagi `admin/admin.js` ni ishlatadi). Ishga tushirish: GitHub MCP `actions_run_trigger` (run_workflow, `admin.yml`, ref `main`, inputs `{buyruq, a1, a2, tasdiq}`) → `actions_list` (runs → jobs) → `get_job_logs` (job_id, return_content); yoki `bash admin/claude_adm.sh <buyruq> [a1] [a2] [tasdiq]` (gh ishlasa).
- Buyruqlar: `holat`, `statistika [email]`, `ruxsat <email> ok|rad|blok|ochir`, `ruxsat hammasi ok`, `guruh <email1> <email2>`, `telegram [@user|-]`, `qoidalar <admin email>` (beta/firestore.rules bo'lsa o'sha), `zaxira` (har dushanba o'zi ham), `admin <email> ber|ol`, `parol`, `akkaunt`, `kochir` — oxirgi to'rttasi FAQAT u aniq so'rasa.
- 🏆 Ilovada (0.7.8, faqat admin akkaunt): ⚙️ Sozlamalar va 📲 Oila reytingi → «🏆 Oilalar reyting guruhi» → «➕ Guruhga qo'shish» (`guruhOilaQosh`: `oila/{uid}.j.guruh` + `q:'admin'`). `guruh/{kod}/oilalar/{uid}` ni o'sha oila telefoni O'ZI yozadi (`guruhObuna` → `guruhAzoYoz`, belgi `L.sync.ga`), eski guruhdagi yozuvlarini o'chiradi. Oila bulutda bo'lmasa (ruxsat kutyapti / oila yaratmagan) — qo'shib bo'lmaydi.
- Firebase kaliti yopiq repoda: HECH QACHON o'qilmaydi, chatga yozilmaydi, so'ralmaydi.

## U bilan ish tartibi
- **Yangi odam ulanishi:** odam ilovada «📨 Ruxsat so'rash» → «✈️ Telegram'da egasiga yozish» → xabar unga keladi → u chatga «ha» + email (yoki xabar) → Claude `ruxsat <email> ok` (rad: `ruxsat <email> rad`); reyting guruhiga — u aytsa `guruh <uning emaili> <yangi email>`. Telegram manzili `ilova/egasi` da (qo'yilgan; `holat` ko'rsatadi).
- **«yo'riqnoma»:** `python3 sinov/yoriqnoma/yoriqnoma.py <papka>` (`--suratsiz` — eski ekranlar) → «pastki chegara» har sahifada ≤ 925 → PDF + 6 JPG SendUserFile bilan. Matn — `SAHIFALAR`, ekranlar — `suratlar.py` (namuna oila, haqiqiy ism yo'q). PDF/JPG repoga yozilmaydi. PDF — sahifa rasmlaridan yig'iladi (HTML'dan to'g'ridan-to'g'ri PDF iPhone/Telegram'da qora to'rtburchak va kesilgan sarlavha berardi, 08.11); tekshiruv: `pdftoppm -r 54 -png <pdf> chk`.
- **«kompyuter yo'riqnoma»** (u 08.11 so'radi): `python3 sinov/yoriqnoma/yoriqnoma_pc.py <papka>` (ekranlar — `suratlar_pc.py`, 1100×720 oyna) → `Bilimjon_kompyuter_v8.pdf` + `Bilimjon_PC_1…6.jpg`: Edge/Chrome'da o'rnatish, ish stolidagi yorliq, «Kirish» (ro'yxat emas), bitta qurilma, foydalanish, yangilanish. Menyu yo'llari rus tilida (08.11 tekshirilgan) — brauzer o'zgarsa SAHIFALAR'ni tuzating.
- **«TAHLIL»** (u tasdiqlagan reja, 08.11): `docs/TAHLIL.md` — hamma oilalar ma'lumoti → har bolaga individual reja (`oila/{uid}/reja/{bid}`) + umumiy tuzatish. Holat: reja tayyor, u tanladi — reja hisobotdan keyin DARHOL avtomatik qo'llanadi (tasdiq kutilmaydi); 1-bosqich (admin `tahlil`) — keyingi chatda.
- **«📚 Bugungi qiyinlar»** matnini tashlasa: o'sha tugunlar uchun `DARS` qoidasi va `DARS_QADAM` ni kuchaytirish → sinov → versiya → beta.
- Javob oxirida: «🕒 sana · savol vaqti → javob vaqti · 👤 profil». Drive xotirasi (OXIRGI.md) — katta ish tugaganda.

## Ochiq ishlar (u tasdiqlasa)
- 📄 Yo'riqnoma PDF (0.8.0 matni: maxfiylik gapi, bitta bola — bitta qurilma, o'zi yangilanadi) — u «yo'riqnoma» desa yasab yuboriladi (ekranlar suratlar.py).
- 🎁 «1 oy bepul, keyin pullik» — hozircha faqat matn (to'lov va cheklov yo'q).
- 🎙️ Arab so'zlari qizining ovozida (132 yozuv) — «hali boshlama». Ota-ona ovozi — keyinroq. Gemini ovozi — `GEMINI_API_KEY` qo'yilsa.
- 11-sinfgacha kengaytirish — avval pilot (1 fan × 1 sinf, darslik PDF'ini u beradi).
- Xavfsizlik (u qiladi): kalitni secret `FIREBASE_SA` ga o'tkazish + eski kalitni o'chirish (rotate), GitHub 2FA, Firebase 2-egasi.
- [?] Bozor: aka-uka jamoa rejimi; g0 arabcha takroriy o'qish; FX effekt tovushlari iPhone jim rejimida.
