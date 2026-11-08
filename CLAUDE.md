# Bilimjon — Claude uchun qisqa xotira

Javoblar o'zbekcha. Repo PUBLIC: ism, familiya, oila ma'lumoti, Telegram manzili, email yozilmaydi (sinovlarda — o'ylab topilgan).
**Limit tejash (08.11, u «o'zing hal qil»):** bu fayl har chatda yuklanadi — QISQA saqlanadi. Batafsil tarix va eski qarorlar — `docs/TARIX.md` (avtomatik yuklanmaydi; `grep -n "<so'z>" docs/TARIX.md` → faqat kerakli bo'lim). Yangi versiya tugaganda: bu yerga 3–6 qator, tafsilot — TARIX oxiriga.

## Loyiha
- Oilaviy o'yin-darslik (PWA), maktabgacha + 1–2-sinf. Sayt: https://abdurazzoqzzuzb-max.github.io/bilimjon/ (GitHub Pages, main / root). Beta: `…/bilimjon/beta/` (main'dagi `beta/`).
- Fayllar: `index.html` (butun ilova, 23 ta `<script>`), `sw.js`, `manifest.webmanifest`, ikonlar, `firestore.rules` (NAMUNA: `__ADMIN_UID__`), `qoidalar/firestore-0.5.0.rules` (orqaga), `admin/` (Claude boshqaruvi), `sinov/`, `docs/TARIX.md`. FAQAT main'da: `beta/`, `ovoz/` (neyron mp3, `iboralar.json`, `skript/yasa.py`), `.github/workflows/ovoz.yml`.
- Firebase **bilimjon-4c008** (Spark, eur3), kirish — email + parol (iPhone'da Google yo'q). SDK gstatic 13.2.0, faqat akkauntli telefonda yuklanadi.

## Versiya va chiqarish
- Saytda va beta'da: **0.7.9** («v7.9», 08.11; 🔐 Orzu sandiqchasi — cho'chqa-kassa va foiz olib tashlandi). Qoidalar Firebase'da: **0.7.7** (0.7.8–0.7.9 qoidani o'zgartirmaydi).
- Har versiyada ikkalasi: `index.html` → `A.VER = 'x.y.z'`, `sw.js` → `P + 'x.y.z'`; ekranda `A.VERK` («v7.7»); `start()` dagi versiya toast'i (eski versiyadan kelganlarga).
- Tartib: yangi tarmoq `v0.x.y` (main'dan) → har bosqich push → beta: main worktree'da `python3 sinov/beta/beta_yig.py origin/<tarmoq> beta` → faqat `beta/` commit → u sinaydi → **«chiqar»** desa: `prod_e2e.py` (eski main vs main+tarmoq, 23 tekshiruv) → main'ga `merge --no-ff` → push → GitHub API deployments (github.io proksida yopiq) → qoidalar o'zgargan bo'lsa `qoidalar <oila emaili>`.
- Orqaga: `git revert -m 1 <merge>`; qoidalar eski ilova bilan mos qilib yoziladi; to'liq eski — admin `qoidalar - eski`.

## Sinov
- Hammasi: **`bash sinov/hammasi.sh`** (2 qator parallel — CPU 2 yadro; har sinovga 1 qator natija). Yakka: `python3 sinov/vXXX/<fayl>.py`, `node sinov/admin/sinov_admin.js`. `node --check` — har `<script>` bloki (hammasi.sh qiladi).
- `?tez=1` — tez rejim, `#sinov-<tugun>-<q>`, `window.__bjCur/__bjJavob/__bjOyin/__bjZal/__bjChipta/__bjUch`. Soxta Firebase: `sinov/bulut/fs.js`, `auth.js` (gstatic yo'naltiriladi, ombor + qoidalar Python'da).
- 🔒 Yangi telefon eshigi localhost'da va `?tez=1` da O'CHIQ; sinovda `?eshik=1`.
- Tasodifiy yiqilishi mumkin (qayta ishga tushiring): `v060/4` ovchi q3, `v071` «o'rniga yangi savol», `v070/1c` parallel yuklamada.

## Kod xaritasi (index.html, tartib bilan)
Kontent banki `BJ.bank` → generatorlar `BJ.gen` (mat M0–M2, mantiq L, ona tili H, yozuv Y, OL, EN, AR, KASHF, arab 2 `BJ.arab`: AQ/AY/TJ.1–8) → core `BJ.A` (holat `A.S()`, log, `makeItem`, `buildMission`, `recordAnswer`, kun chegarasi, xulosa) → bola tomoni (router `render()`, missiya, mashq, vazifa, arena, kichik dars + kino, Tushunmadim, 📖 tanishtiruv `screenTanish`) → o'yinlar `A.oyin` → garaj → zal `A.zal` → so'm `A.pul` → bozor `A.bozor` → xarita `A.xarita` → uch o'qish `A.uch` → ovoz `A.ovoz` → ☁️ bulut (sinxron, 🛡️ ruxsat, 👑 hamma oilalar, ✈️ Telegram, 🔒 `A.eshik`, reyting guruhi) → ota-ona paneli (`ota-*`) → `start()`.

## O'zgarmas qoidalar (buzilsa — xato bo'lgan)
- Oila darajasidagi yangi sozlamani `defaults()` ga QO'SHMANG (`migrate` umumiy holatni o'zgartirib, bulut yangiligini bosib ketadi) — `=== 'x'` / `!== false` bilan o'qing.
- `fixBola`/`migrate` ichida faqat hoisted `function` yoki ichki o'zgaruvchi (TDZ — holat bo'sh qaytgan).
- NUTQ yoki generator matni o'zgarsa — `python3 sinov/ovoz/inventar.py ovoz/iboralar.json` → main'ga push (Actions mp3 yasaydi). Ovozni o'sha id bilan qayta yasasangiz — `sw.js` `OV` ni oshiring.
- Lookbehind regex yo'q (eski iOS). Firestore hujjati ≤1 MB (`S.sovga` + `S.dokon` rasmlari ~720 KB — oshirmang).
- Dizayn: realistik + animatsiya, multfilm emas (u 4 marta aytgan). 390 px da gorizontal siljish yo'q.
- 👆 Ikki marta bosish zoom'i yo'q (0.7.8, u so'radi): `html{touch-action:manipulation}`, hamma input ≥ 16px. Ikki barmoq bilan kattalashtirish QOLADI (u tanladi) — viewport'ga `user-scalable=no` qo'ymang. touchend bilan ikki bosishni to'xtatmang (o'yinlarda tez bosish yo'qoladi).
- 🔐 Pul FOIZSIZ (0.7.9, u: «pul tegilmasa ko'payadi — islomiy jihatdan to'g'ri emas»): sandiqchaga foiz/o'sish qo'shmang, 🐷 cho'chqa tasvirini ishlatmang. Tejash — faqat ota-ona mukofoti (bozor 🪙) yoki orzu uchun yig'ish.
- `obuna`: bulut hujjati `q === 'admin'` bo'lsa undagi `guruh` olinadi.

## 👑 Admin (Claude chatdan; telefon/akkaunt yo'qolsa ham)
- Yopiq repo `abdurazzoqzzuzb-max/bilimjon-admin`, workflow `admin.yml` (main'dagi `admin/admin.js` ni ishlatadi). Ishga tushirish: GitHub MCP `actions_run_trigger` (run_workflow, `admin.yml`, ref `main`, inputs `{buyruq, a1, a2, tasdiq}`) → `actions_list` (runs → jobs) → `get_job_logs` (job_id, return_content); yoki `bash admin/claude_adm.sh <buyruq> [a1] [a2] [tasdiq]` (gh ishlasa).
- Buyruqlar: `holat`, `statistika [email]`, `ruxsat <email> ok|rad|blok|ochir`, `ruxsat hammasi ok`, `guruh <email1> <email2>`, `telegram [@user|-]`, `qoidalar <admin email>` (beta/firestore.rules bo'lsa o'sha), `zaxira` (har dushanba o'zi ham), `admin <email> ber|ol`, `parol`, `akkaunt`, `kochir` — oxirgi to'rttasi FAQAT u aniq so'rasa.
- 🏆 Ilovada (0.7.8, faqat admin akkaunt): ⚙️ Sozlamalar va 📲 Oila reytingi → «🏆 Oilalar reyting guruhi» → «➕ Guruhga qo'shish» (`guruhOilaQosh`: `oila/{uid}.j.guruh` + `q:'admin'`). `guruh/{kod}/oilalar/{uid}` ni o'sha oila telefoni O'ZI yozadi (`guruhObuna` → `guruhAzoYoz`, belgi `L.sync.ga`), eski guruhdagi yozuvlarini o'chiradi. Oila bulutda bo'lmasa (ruxsat kutyapti / oila yaratmagan) — qo'shib bo'lmaydi.
- Firebase kaliti yopiq repoda: HECH QACHON o'qilmaydi, chatga yozilmaydi, so'ralmaydi.

## U bilan ish tartibi
- **Yangi odam ulanishi:** odam ilovada «📨 Ruxsat so'rash» → «✈️ Telegram'da egasiga yozish» → xabar unga keladi → u chatga «ha» + email (yoki xabar) → Claude `ruxsat <email> ok` (rad: `ruxsat <email> rad`); reyting guruhiga — u aytsa `guruh <uning emaili> <yangi email>`. Telegram manzili `ilova/egasi` da (qo'yilgan; `holat` ko'rsatadi).
- **«yo'riqnoma»:** `python3 sinov/yoriqnoma/yoriqnoma.py <papka>` (`--suratsiz` — eski ekranlar) → «pastki chegara» har sahifada ≤ 925 → PDF + 6 JPG SendUserFile bilan. Matn — `SAHIFALAR`, ekranlar — `suratlar.py` (namuna oila, haqiqiy ism yo'q). PDF/JPG repoga yozilmaydi. PDF — sahifa rasmlaridan yig'iladi (HTML'dan to'g'ridan-to'g'ri PDF iPhone/Telegram'da qora to'rtburchak va kesilgan sarlavha berardi, 08.11); tekshiruv: `pdftoppm -r 54 -png <pdf> chk`.
- **«TAHLIL»** (u tasdiqlagan reja, 08.11): `docs/TAHLIL.md` — hamma oilalar ma'lumoti → har bolaga individual reja (`oila/{uid}/reja/{bid}`) + umumiy tuzatish. Holat: reja tayyor, u tanladi — reja hisobotdan keyin DARHOL avtomatik qo'llanadi (tasdiq kutilmaydi); 1-bosqich (admin `tahlil`) — keyingi chatda.
- **«📚 Bugungi qiyinlar»** matnini tashlasa: o'sha tugunlar uchun `DARS` qoidasi va `DARS_QADAM` ni kuchaytirish → sinov → versiya → beta.
- Javob oxirida: «🕒 sana · savol vaqti → javob vaqti · 👤 profil». Drive xotirasi (OXIRGI.md) — katta ish tugaganda.

## Ochiq ishlar (u tasdiqlasa)
- 🚧 **0.8.0 YARIM (08.11 12:45, limit tugadi) — tarmoq `v0.8.0`:** 📱 bitta bola — bitta qurilma (render'da `qurQulf` → `screenQurilma`, PIN bilan o'tkazish, ⚙️ qurilma nomi; faqat akkaunt ulanganda; localhost/tez da ?qulf=1) + maxfiylik gapi (ruxsat kartasi, tanishtiruv, yo'riqnoma 1-bet) + yo'riqnoma 5-bet ogohlantirish. Sinov `sinov/v080/sinov_qurilma.py`: 17/20 — 3 yiqilish SINOV xatosi: A telefon `#mashq` da turganda o'tkazish `pending` (faolMi) — sinovda A ni avval `#uy` ga o'tkazish kerak. Keyin: hammasi.sh (+v080) → prod_e2e 0.7.9→0.8.0 → chiqarish (u «srazu chiqar», «mayda narsalar bitta to'liq versiyada» dedi) → yo'riqnoma PDF yuborish.
- ⏭️ **KEYINGI VERSIYADA ALBATTA (u 08.11 11:51 aytdi):** maxfiylik gapi — «Natijalar ilova egasi tomonidan o'quv rejasi uchun ko'rib chiqiladi.» → `sinov/yoriqnoma/yoriqnoma.py` `SAHIFALAR` (1-sahifa, taklifnoma ostida) + ilovadagi 📖 tanishtiruv / 🛡️ ruxsat so'rash kartasi. Alohida versiya chiqarilmaydi — navbatdagi tuzatish bilan birga.
- 🎁 «1 oy bepul, keyin pullik» — hozircha faqat matn (to'lov va cheklov yo'q).
- 🎙️ Arab so'zlari qizining ovozida (132 yozuv) — «hali boshlama». Ota-ona ovozi — keyinroq. Gemini ovozi — `GEMINI_API_KEY` qo'yilsa.
- 11-sinfgacha kengaytirish — avval pilot (1 fan × 1 sinf, darslik PDF'ini u beradi).
- Xavfsizlik (u qiladi): kalitni secret `FIREBASE_SA` ga o'tkazish + eski kalitni o'chirish (rotate), GitHub 2FA, Firebase 2-egasi.
- [?] Bozor: aka-uka jamoa rejimi; g0 arabcha takroriy o'qish; FX effekt tovushlari iPhone jim rejimida.
