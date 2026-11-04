# Bilimjon — Claude uchun loyiha xotirasi

Yangi chat shu fayldan davom etadi. Javoblar o'zbekcha. Repo PUBLIC: bu yerga ism, familiya, oila ma'lumoti yozilmaydi.

## Loyiha
- Oilaviy o'yin-darslik (PWA). Sayt: https://abdurazzoqzzuzb-max.github.io/bilimjon/ (GitHub Pages, main / root).
- Fayllar: `index.html` (butun ilova, ichida 14 ta `<script>` moduli), `sw.js` (network-first kesh), `manifest.webmanifest`, `icon.svg`, `icon-192.png`, `icon-512.png`.
- **Haqiqat manbai — shu repo.** Kompyuterdagi `Desktop\Claude outputs\Bilimjon` (ko'p faylli manba va v0.1.1 ZIP) ESKI, ishlatilmaydi.
- Hamma oilalar uchun bitta umumiy versiya. Yangilanish telefonga o'zi keladi (ilovani yopib qayta ochganda), natijalar telefonda (localStorage) qoladi.

## Versiya
- Hozir: **0.3.0** (04.11.2026).
- Har chiqarishda ikkalasi birga oshiriladi: `index.html` → `VER = 'x.y.z'`, `sw.js` → `const V = 'bj-vx.y.z'`.

## Modullar xaritasi (index.html, tartib bilan)
1. Kontent banki (`BJ.bank`).
2. Generatorlar: mat `M0.1–M2.14` · mantiq `L.1–L.10` · ona tili `H0–H2` · yozuv `Y0.1–Y0.4` · olimpiada `OL` · `EN.*`, `AR.*`, `AL.*`, `KASHF`. Ro'yxat: `BJ.gen.reg`, yaratish: `gen.make(id, q, ctx)`.
3. Core (`BJ.A`): holat `A.S()`, log `A.pushLog/readLog`, rejalash `makeItem`, `buildMission`, `pickNode`, `recordAnswer`.
4. Bola tomoni: router, `screenMission → stepRun → showItem → onAnswer → missionNext`, `RENDER.{tanla,yoz,tartib,farq,labirint,sudoku,xotira,iz,yigish}`, Arena (`arenaNext(b, given)`), **KICHIK DARS**, **😴 CHARCHADIM**, `reytingHTML`.
5. **O'yinlar** (`A.oyin`): `boshla(b, m, done)`, `poyga`, `pazl`, `kozgu`, `pgTask(lv)`, `KZ` rasmlari, `pzRasm`.
6. Ota-ona paneli (`ota-*` yo'nalishlari), `exportPanel` (BJW2), `qiyinPanel`, `reytingPanel` (`ota-reyting`), zaxira, `start()`.

## 0.2.0 — KICHIK DARS (bajarildi)
- `onAnswer`: 1-xato → maslahat. 2-xato → `darsMumkin(it, r)` (faqat `t` = tanla | yoz; KASHF va duel emas) → `darsFlow` → `showLesson`: qoida (`DARS[tugun]` yoki `DARS_FAN[fan]`) + shu savolning namuna yechimi (`DARS_QADAM[tugun]` yoki `mathSteps(ex)`) + javob → «Men tayyorman» (5 s) → `twinItem`: o'xshash yangi savol, `tur: 'dars'`.
- Egizak `m.res` ga yozilmaydi (missiya hisobi o'zgarmaydi). 2 ta egizak ham xato bo'lsa → «Bu mavzu hozircha qiyin» va davom.
- Log: `{ t: 'dars', tugun, n }`. Ota-ona: «📚 Bugungi qiyinlar» → `BILIMJON-QIYIN|...` matni (BOLA / Q / e qatorlari).

## Kundalik ish tartibi
1. Foydalanuvchi kun oxirida «📚 Bugungi qiyinlar» matnini chatga tashlaydi.
2. Claude shu tugunlar uchun `DARS` qoidasi va `DARS_QADAM` namuna yechimini kuchaytiradi (bola xatosi turiga qarab).
3. Sinov → versiya oshiriladi → commit → push → sayt yangilanganini tekshirish (`sw.js` dagi `V`).

## Sinov
- `python3 -m http.server 8765` + Playwright (Chromium o'rnatilgan).
- `?tez=1` → tez rejim (`A.TEZ`), `#sinov-<tugun>-<q>` ekrani, `window.__bjCur()` joriy topshiriqni beradi.
- Majburiy tekshiruvlar: har `<script>` bloki `node --check`; barcha `M*` tugunlarida `mathSteps` oxirgi qatori javobga teng; xato → dars → egizak → missiya oqimi; telefon kengligida (390 px) ko'rinish.

## 0.3.0 — 2-bosqich (bajarildi)
- **🎮 Dam olish o'yini**: missiyada har `sozlama.oyinHar` (standart 5; 0 — o'chiq) ta savoldan keyin `oyinDaq` (1–5, standart 3) daqiqa. Hisob `m.oyinN` (faqat `m.res` ga yozilgan savollar; dars egizagi sanalmaydi). Faqat yakun qolganda o'yin chiqmaydi. Yulduz bermaydi. Vaqt tugasa — joriy raundni tugatishga 45 s.
  - g0 → 🏎️ poyga (orolda 🦄 parvoz): 3 yo'lak, 🎯 belgiga mos yo'lakni bosish. `pgTask(lv)`: 0–1 shakl/rang → 2–3 + son (1–3) → 4+ son 1–5 va naqsh (AB, AAB; 5+ ABB, ABC). Har 3 ketma-ket to'g'rida daraja +1.
  - g1+ → tanlov: 🧩 pazl (o'zimiz chizgan rasm, bolaning detallari bilan; 3×3, 3-raunddan 4×4; tap-tap yoki sudrash) yoki 🎨 ko'zgu rasm (8×8, chap yarmi tayyor, o'ngini simmetrik bo'yash; `KZ` 8 ta rasm, oson → qiyin; «🔍 Tekshir»).
  - Bola progressi: `b.oyin = { pazl, kozgu, oxirgi }`. Log: `{ t: 'oyin', tur, sek, ok, xato, raund, erta }`, kunlik `agg.oyin/oyinSek`, vaqt `fan.oyin`.
- **😴 Charchadim** (missiya savoli ostida): tasdiqlansa joriy blok yakundan oldinga ko'chadi (`moveLater`, natijalar bilan), `st.qoldi` — aynan shu savol keyin birinchi chiqadi, `st.kechik` — har blok faqat bir marta. Darsda va egizakda tugma yo'q. Boshqa fan qolmasa — 1 daqiqalik dam (cho'zilish) varag'i. Log `{ t: 'charch', fan, k, tugun }`.
- **🏆 Hafta reytingi** (serversiz): bola uyida (`sozlama.reyting`, 2+ bola bo'lsa). Tartib: hafta ⭐ → faol kunlar → 🚀 o'sish (bu hafta o'zlashtirilgan ko'nikmalar). Boshqa telefon: ota-ona → 📲 Oila reytingi → `BILIMJON-REYTING|1|qurilma|oila|hafta|ts` + `B|id|avatar|laqab|daraja|yulduz|kun|osish|detal|missiya` kodini yuborish/qo'yish → `S.oilaTel[qurilma]`. O'z kodi va eski kod rad etiladi.
- Ota-ona: ⚙️ Sozlamalar → o'yin chastotasi, davomiyligi, reyting ko'rinishi. «📚 Bugungi qiyinlar» → `BOLA|…|charch=fanlar|oyin=n`. BJW2 → `|oyin=n|charch=n`.

## Sinov (0.3.0 qo'shimcha)
- `?tez=1`: o'yin 8 s, pazl 2×2; `window.__bjOyin()` — joriy o'yin seansi (`game.state()`, `game.swap`, `game.setLane`, `game.setCol/setAt`), `A.oyin.finish()`.
- Tekshiruvlar: `pgTask` — 3 ta katakda bitta to'g'ri; `KZ` — 8×8 va simmetrik; `pzRasm` — to'g'ri SVG; 5 savol → o'yin → darsga qaytish; Charchadim → blok ko'chishi va o'sha savol qaytishi; 2 xato → dars (Charchadim yo'q); eski 0.2.0 holatdan yangilanish.

## KEYINGI (g'oyalar, foydalanuvchi tasdig'isiz qilinmaydi)
- Oilalar orasidagi reyting (server/Firebase, taxalluslar, ota-ona roziligi) — xavf: bolalar ma'lumoti internetga chiqadi, ochiq reyting orqada qolgan bolaning ishtiyoqini so'ndirishi mumkin.
- O'yin sozlamasini har bola uchun alohida qilish (hozir oila uchun bitta).
