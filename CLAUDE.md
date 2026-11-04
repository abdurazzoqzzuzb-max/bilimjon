# Bilimjon — Claude uchun loyiha xotirasi

Yangi chat shu fayldan davom etadi. Javoblar o'zbekcha. Repo PUBLIC: bu yerga ism, familiya, oila ma'lumoti yozilmaydi.

## Loyiha
- Oilaviy o'yin-darslik (PWA). Sayt: https://abdurazzoqzzuzb-max.github.io/bilimjon/ (GitHub Pages, main / root).
- Fayllar: `index.html` (butun ilova, ichida 13 ta `<script>` moduli), `sw.js` (network-first kesh), `manifest.webmanifest`, `icon.svg`, `icon-192.png`, `icon-512.png`.
- **Haqiqat manbai — shu repo.** Kompyuterdagi `Desktop\Claude outputs\Bilimjon` (ko'p faylli manba va v0.1.1 ZIP) ESKI, ishlatilmaydi.
- Hamma oilalar uchun bitta umumiy versiya. Yangilanish telefonga o'zi keladi (ilovani yopib qayta ochganda), natijalar telefonda (localStorage) qoladi.

## Versiya
- Hozir: **0.2.0** (04.11.2026).
- Har chiqarishda ikkalasi birga oshiriladi: `index.html` → `VER = 'x.y.z'`, `sw.js` → `const V = 'bj-vx.y.z'`.

## Modullar xaritasi (index.html, tartib bilan)
1. Kontent banki (`BJ.bank`).
2. Generatorlar: mat `M0.1–M2.14` · mantiq `L.1–L.10` · ona tili `H0–H2` · yozuv `Y0.1–Y0.4` · olimpiada `OL` · `EN.*`, `AR.*`, `AL.*`, `KASHF`. Ro'yxat: `BJ.gen.reg`, yaratish: `gen.make(id, q, ctx)`.
3. Core (`BJ.A`): holat `A.S()`, log `A.pushLog/readLog`, rejalash `makeItem`, `buildMission`, `pickNode`, `recordAnswer`.
4. Bola tomoni: router, `screenMission → stepRun → showItem → onAnswer`, `RENDER.{tanla,yoz,tartib,farq,labirint,sudoku,xotira,iz,yigish}`, Arena (`arenaNext(b, given)`), **KICHIK DARS**.
5. Ota-ona paneli (`ota-*` yo'nalishlari), `exportPanel` (BJW2), `qiyinPanel`, zaxira, `start()`.

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

## KEYINGI: 2-bosqich (foydalanuvchi so'ragan)
- Har 5 ta savoldan keyin avtomatik «🎮 Dam olish o'yini», 2–3 daqiqa, mantiqni o'stiradigan:
  maktabgacha / garaj dunyosi → poyga (to'g'ri javobli yo'lakka burilish);
  2-sinf / orol dunyosi → pazl yig'ish va rasm chizish.
- Missiya ekranida «😴 Charchadim» → boshqa fanga o'tadi, joriy blok keyinroqqa qoladi.
- Pedagogik qaror: o'yin faqat 5 ta savol ishlangandan keyin ochiladi; «Charchadim» o'yinga emas, boshqa fanga olib boradi (tugma qiyin savoldan qochish yo'li bo'lmasin).
- Ota-ona ⚙️ Sozlamalar: o'yin chastotasi (necha savolda bir) va davomiyligi.
- Qayta ishlatish mumkin: `ART.race` (poyga sahnasi), `L.10` shakl yig'ish (pazl asosi), `FX.bigScene`, `ART.car`, `ART.pegasus`.
