# Bilimjon — Claude uchun loyiha xotirasi

Yangi chat shu fayldan davom etadi. Javoblar o'zbekcha. Repo PUBLIC: bu yerga ism, familiya, oila ma'lumoti yozilmaydi.

## Loyiha
- Oilaviy o'yin-darslik (PWA). Sayt: https://abdurazzoqzzuzb-max.github.io/bilimjon/ (GitHub Pages, main / root).
- Fayllar: `index.html` (butun ilova, ichida 16 ta `<script>` moduli), `sw.js` (network-first kesh; Firebase SDK cache-first), `manifest.webmanifest`, `icon.svg`, `icon-192.png`, `icon-512.png`, `firestore.rules` (konsoldagi qoidalar nusxasi), `sinov/bulut/` (soxta Firebase bilan sinov).
- **Haqiqat manbai — shu repo.** Kompyuterdagi `Desktop\Claude outputs\Bilimjon` (ko'p faylli manba va v0.1.1 ZIP) ESKI, ishlatilmaydi.
- Hamma oilalar uchun bitta umumiy versiya. Yangilanish telefonga o'zi keladi (ilovani yopib qayta ochganda), natijalar telefonda (localStorage) qoladi; ☁️ akkaunt ulangan oilada Firestore'da ham.

## Versiya
- Hozir: **0.5.1** (05.11.2026).
- Har chiqarishda ikkalasi birga oshiriladi: `index.html` → `VER = 'x.y.z'`, `sw.js` → `const V = 'bj-vx.y.z'`.

## Modullar xaritasi (index.html, tartib bilan)
1. Kontent banki (`BJ.bank`).
2. Generatorlar: mat `M0.1–M2.14` · mantiq `L.1–L.10` · ona tili `H0–H2` · yozuv `Y0.1–Y0.4` · olimpiada `OL` · `EN.*`, `AR.*`, `AL.*`, `KASHF` · **arab 2 (`BJ.arab`)**: `AQ.1–4`, `AY.1–4`, `TJ.1–6`. Ro'yxat: `BJ.gen.reg`, yaratish: `gen.make(id, q, ctx)`.
3. Core (`BJ.A`): holat `A.S()`, log `A.pushLog/readLog`, rejalash `makeItem`, `buildMission`, `pickNode`, `recordAnswer`.
4. Bola tomoni: router, `screenMission → stepRun → showItem → onAnswer → missionNext`, `RENDER.{tanla,yoz,tartib,farq,labirint,sudoku,xotira,iz,yigish,arharf,daftar}`, **📚 Mashq** (`screenMashq`, `mashqStart/mashqNext`, `CUR.k='mashq'`), **📝 Uyga vazifa** (`vazifaHTML`, `vazifaStart`, `vazifaDone`), Arena (`arenaNext(b, given)`), **KICHIK DARS**, **😴 CHARCHADIM**, `reytingHTML`.
5. **O'yinlar** (`A.oyin`): `boshla(b, m, done)`, `poyga`, `pazl`, `kozgu`, `pgTask(lv)`, `KZ` rasmlari, `pzRasm`.
6. **☁️ Bulut** (`BJ.bulut`, 0.5.0): `A.bulutPanel(top, bindTop)` (`#ota-bulut`, akkauntsiz yangi telefonda `#bulut`), `A.guruhHTML/guruhBind` (reyting paneliga karta), `A.bulutStart` (start() da), core'da `A.logMerge`.
7. Ota-ona paneli (`ota-*` yo'nalishlari), `exportPanel` (BJW2), `qiyinPanel`, `reytingPanel` (`ota-reyting`), `vazifaPanel` (`ota-vazifa`), `arabPanel` (so'z, ibora, tajvid tasdig'i), zaxira, `start()`.

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

## 0.4.0 — Arab tili kuchaytirildi, Mashq, Uyga vazifa (bajarildi)
- **Arab tili 2** (`BJ.arab`, alohida modul): bemalol o'qiydigan-yozadigan bolalar uchun (arab = `asosiy`). Daraja sinfga emas, `b.arDaraja` (1–3) ga qarab — `arPick` birinchi marta `q = arDaraja` qo'yadi, keyin odatdagi moslashuv.
  - O'qish: `AQ.1` ma'no, `AQ.2` arabchasini top, `AQ.3` belgilar (shadda/sukun/tanvin) va harflar soni, `AQ.4` iboralar (`B.arIbora`, 20 ta).
  - Yozish: `AY.1` harf kartochkalaridan so'z yig'ish (`RENDER.arharf`, imlo), `AY.2` harflarni qo'shish, `AY.3` tushib qolgan harf, `AY.4` daftarga yozish (`RENDER.daftar`, o'zi baholaydi — faqat «📓 Daftar» bo'limi va vazifada).
  - Tajvid: `TJ.1` shamsiy/qamariy lom, `TJ.2` nun sokin va tanvin (izhor, idg'om g'unnali/g'unnasiz, iqlob, ixfo), `TJ.3` mim sokin, `TJ.4` qalqala, `TJ.5` madd (tabiiy, muttasil, munfasil, lozim), `TJ.6` g'unna. Har biriga o'zbekcha `DARS` qoidasi (kichik dars).
  - Lug'at: 112 so'z (yangi mavzular: kiyim, fel, sifat, vaqt, din, oshxona; son 6–10, ovqat, tabiat qo'shimchalari).
  - Tasdiq: so'z va iboralar — `sozlama.arTasdiq` (kamida 6 so'z / 4 ibora), tajvid — bo'lim bo'yicha `sozlama.tjTasdiq`. Tasdiqsiz bo'lim bolaga 🔒.
  - Bo'limlar `BJ.arab.BOLIM`: aralash, oqish, yozish, tajvid, lugat, daftar.
- **🎯 Fokus fan** (`b.fokus`, bola tahririda): fokus fanning bloki ikki barobar; `ar` + `asosiy` bo'lsa, duel dan keyin `{ k: 'blok', fan: 'ar', arBolim: 'aralash' }` bloki.
- **📚 Mashq** (bola uyi → `#mashq`): fan tanlash, arabda bo'lim tanlash → `#mashq-<fan>[-<bolim>]`. Cheksiz savol, kichik dars, har `oyinHar` savolda o'yin, yulduz arena bilan umumiy kunlik 20 chegarasida (`tur: 'mashq'`).
- **📝 Uyga vazifa** (`b.vazifa[]`: `{ id, berildi, muddat, fan, bolim, n, izoh, qildi, ok, done, doneSana, qolda }`): ota-ona → 📝 Uyga vazifa (bir nechta bolaga birdan). Bola uyida karta → `#vazifa-<id>` (`tur: 'vazifa'`, yulduz chegarasiz) → tugasa +5 ⭐. Faqat matnli vazifa (`fan: 'izoh'`) → bola «✅ Bajardim» (+2 ⭐). «📚 Bugungi qiyinlar» → `VZ|fan=…|bolim=…|n|qildi|ok|holat`.
- Sinov: arab matnlarida bitta harfda ko'pi bilan bitta harakat; lom/nun/mim hukmi hal qiluvchi harfdan mustaqil tekshiriladi; qalqala, g'unna, madd evristikalari; 14 tugun × 3 qiyinlik × g0/katta generatorlari `gen.valid`.

## 0.4.1 — 1-kun natijalari bo'yicha (bajarildi)
- Kuchaytirilgan darslar: `M1.2` (o'nlik-birlik; o'zbekcha aytilish tartibi = yozilish tartibi, «14 ≠ 41», tayoqcha rasmi `DARS_VIS`), `M2.4` (kalit so'zlar, q1–q2 uchun namuna yechim), `EN.*` (hamma mavzuga `enQadam`, ranglar uchun eslab qolish bog'lamlari), arab `AQ.1–3`, `TJ.1` (`BJ.arab.QADAM`: harfma-harf tahlil, ta marbuta = muannas).
- Darsda: arabcha bo'laklar `<bdi dir=rtl>` (`escB`) — aralashmaydi; `it.tts` bo'lsa 🔊 tugma va avtomatik ovoz.
- Maktabgacha bola: hamma arab 2 savolida `ota` maslahati («Savolni o'qib bering»), `AQ.3` belgi savolida belgining rasmi.
- Charchash: oxirgi 3 kundagi missiyada 2-yarmida aniqlik 15+ punkt tushgan bo'lsa → `b.qisqaKun` = bugun → `blokSoni` ×0,75 (endi 16 chegarasidan KEYIN qo'llanadi, `reja.qisqa` ham shunday). Ota-ona kartochkasida 😴 yozuvi.

## 0.5.0 — ☁️ Oila akkaunti va 🏆 Reyting guruhi (bajarildi)
- Firebase loyihasi: **bilimjon-4c008** (Spark, bepul), egasi — oilaning Google akkaunti. Analytics va Gemini o'chiq. Web ilova «Bilimjon PWA», config `index.html` dagi `CFG` (ochiq kalitlar — xavfsizlik qoidalarda).
- Auth: Google + Email/Parol yoqilgan. Ruxsat etilgan domenlar: localhost, bilimjon-4c008.firebaseapp.com, **abdurazzoqzzuzb-max.github.io**.
- Firestore: Standard, **eur3**, production mode; qoidalar = `firestore.rules` (o'zgartirsangiz — konsolga ham qo'ying).
- SDK `https://www.gstatic.com/firebasejs/13.2.0/` dan dinamik `import()`; faqat `localStorage.bj_bulut_v1` (uid, email, sync izlari) bor telefonda yoki ☁️ ekran ochilganda yuklanadi. Akkauntsiz oila — avvalgidek serversiz.
- Ma'lumot: `oila/{uid}` {j: umumiy S (bolalar, joriy, qurilma, lastBackup, seenVer, appVer va `G:` reyting yozuvlarisiz), ts, q} · `oila/{uid}/bolalar/{bid}` {j: bola JSON, ts, q} · `oila/{uid}/log/{bid}_{kun}` {bid, kun, e: arrayUnion(JSON satr)}.
- Sinxron: har 6 s (va sahifa yashirilganda) hash bilan o'zgargan qism yuboriladi. Qabul — `onSnapshot`. Qoida: boshqa telefon yangiroq yozgan va bu telefonda o'zgarmagan bo'lsa olinadi; ikkalasida o'zgargan bo'lsa — shu (ishlatilayotgan) telefon ustun. Bola missiya/arena/mashq/vazifa ekranida bo'lsa yangilanish `pending` da kutadi, ekrandan chiqqach qo'llanadi. Bola o'chirilishi ham sinxron. Log ikki telefondan birlashadi (takrorsiz), ochilganda oxirgi 7 kun olinadi.
- Birinchi kirish: bulut bo'sh → shu telefon yuklanadi; telefonda oila yo'q → bulutdagi olinadi (PIN ham); ikkalasida bor → so'raladi: «☁️ Bulutdagini olish» (eski holat `bj_oldin_bulut` da) yoki «➕ Birlashtirish» (bir xil id — ko'proq javobi bori).
- 🏆 Reyting guruhi: kod 10 belgi (`A-Z2-9`). `guruh/{kod}` {yaratdi, ts}, `guruh/{kod}/oilalar/{uid}`, `guruh/{kod}/azo/{bid}` {uid, oila, av, laqab, daraja, yulduz, kun, osish, detal, missiya, wk, ts}. Qabul qilingan a'zolar `S.oilaTel['G:'+uid]` ga yoziladi — eski reyting ro'yxati (`reytingRoyxat`) o'zgarishsiz ishlaydi. `S.guruh = {kod}` oila darajasida sinxron (oyisining telefoni ham avtomatik qo'shiladi).
- Akkauntsiz oilalar uchun 0.3.0 dagi «📲 kod almashish» qoladi.
- Sinov: `python3 sinov/bulut/sinov_bulut.py` — Playwright, gstatic so'rovlari soxta modullarga (`sinov/bulut/fs.js`, `auth.js`) yo'naltiriladi, ombor Python'da; 3 telefon (dadasi, oyisi, boshqa oila), 21 tekshiruv. Haqiqiy Firebase faqat saytda, foydalanuvchi kirgandan keyin tekshiriladi.
- Xavf/eslatma: bitta akkauntni bir nechta oila bilan bo'lishmaslik (ekranda ogohlantirish bor). Tavsiya: Google Cloud'da API kalitini `abdurazzoqzzuzb-max.github.io/*` referrer bilan cheklash.

## 0.5.1 — iPhone kirish tuzatishi (bajarildi)
- iPhone uy ekranidagi PWA'da `signInWithPopup` Google oynasidan javob qaytmaydi (foydalanuvchi sinab ko'rdi: hisob tanlanadi, «Продолжить», lekin ilovaga kirmaydi). Redirect ham ishlamaydi (authDomain boshqa domen, Safari storage ajratishi). Yechim: email + parol asosiy usul; iOS'da (`IOS`) Google tugmasi yashirilgan, boshqa qurilmalarda ikkinchi o'rinda + «bitta oila, bitta usul» ogohlantirishi; Google bosilib 40 s javob bo'lmasa toast.
- Oila qarori: hamma telefonda email + parol (Google bilan aralashtirmaslik — Firebase tasdiqlanmagan email-parolni Google bilan almashtirib yuborishi mumkin).

## 0.6.0 — REJA (05.11.2026, foydalanuvchi tasdiqladi; tarmoq `v0.6.0`, saytga faqat «chiqar» deganda)
Asos — 1-kun ma'lumoti: maktabgacha bola 53 daq faol (18–22 soat), 30-savoldan keyin aniqlik 93% → 67%; 2-sinf bolasi 13 daq, 87%, missiya tugatilmagan, 2× «charchadim»; ⭐ reyting yoshlar orasida adolatsiz (69 ga 13).
Pedagogik qoidalar: sovg'a — muntazamlik uchun (tezlik uchun emas), oila umumiy sovg'asi; solishtirish — o'z maqsadi % bilan; katta effekt — har javobda emas, kombo/marrada.
- [x] Sinxron: soat farqi (hash bo'yicha qabul), log yo'qolishi, ko'p kun oflayn — `sinov/bulut/sinov_chekka.py` (10 tekshiruv).
- [x] 1. 🌙 Kun chegarasi: `A.kunLimit(b)` (`b.kunDaq`: null — standart `KUN_STD` g0 25 / g1–g2 35, 0 — cheklanmagan), `A.qolganSek`, `b.qoshDaq[kun]` (PIN bilan +10). Uyqu: `sozlama.uyqu` ('21:00', '' — o'chiq), oraliq uyqu…05:00, `b.uyquOchiq`. `A.damHolat(b, davom)` → {sabab:'limit'|'uyqu'}; davom=true — boshlangan missiyaga 15 daq imtiyoz. Tekshiruv: router (missiya/arena/mashq/vazifa), `missionNext`, `arenaNext`, `mashqNext` → `screenDam`. Taymer: 3 daq qolganda va 0 da toast. Uyda `vaqtHTML`. Log `{t:'dam'}`. `?tez=1` da o'chiq (`A.damSinov=true` bilan yoqiladi).
- [x] 1. 🎮 `A.oyinCfg(b)` — `b.oyinHar`/`b.oyinDaq` (null — oila sozlamasi); bola tahririda `#fz #fo #fp`, ⚙️ da `#uq` (uyqu).
- [x] 1. ⚖️ `reytingRoyxat`: `x.maqsad` = bajarilgan missiya kunlari / haftaning o'tgan kunlari (%), tartib maqsad → kun → 🚀 → ⭐. Yangi maydon YO'Q (guruh `firestore.rules` o'zgarmaydi). Ekranda «🎯 m/d».
- [x] 1. 💥 Kombo: `KOMBO` (kid modul), `komboMarra` 3, 5, 8, 12, 16…; `komboFX` — portlash + `.kombo` yozuvi, 5+ da bonus ⭐ 1/2/3; dars egizagi sanalmaydi; `agg.komboMax`, `b.komboMax`, log `{t:'kombo'}`.
- [ ] 2. 🎁 Sovg'a vitrinasi: ota-ona sovg'a nomi + rasmi (kamera, siqilgan JPEG), shart (masalan 7 kundan 5 kun maqsad); bola uyida «sovg'agacha N%»; oila umumiy sovg'asi.
- [ ] 2. 📊 Hafta hisoboti (ota-ona): vaqt, aniqlik fan bo'yicha, charchash, eng zaif/kuchli ko'nikma, keyingi hafta tavsiyasi.
- [ ] 3. 🔧 Konstruktor + krash-test (garaj): detal 10–15 to'g'ri javobda 1 ta; yig'ish → devorga urish → parchalanish → qayta yig'ish.
- [ ] 3. 🤖 Kod-yo'l: strelkalar ketma-ketligi bilan labirint (g0 3–5 qadam, g1+ «×N» takror).
- [ ] 4. 🗺️ Sarguzasht xaritasi: hafta = 7 bekat, yakshanba — boss/final.
- [ ] 4. 💖 «Katta qiz» uslubi (orol uchun ixtiyoriy tema: neon-pushti, kamroq multfilm).
- [ ] 5. 🌍 Kun kashfiyoti: 1 fakt + 1 savol + uyda topshiriq.
- [ ] 5. 📖 O'qish tezligi: 1 matn 3 marta, so'z/daq o'sishi.
- [ ] 5. 🕌 Arab: ra (tafxim/tarqiq), vaqf belgilari — yangi TJ tugunlari, DARS, tasdiq.
- [ ] 6. 🎙️ Ota-ona ovozi: MediaRecorder, 3–5 s qisqa yozuv, Firestore'da (Storage — faqat Blaze tarif!), iPhone↔Android ijro sinovi.
- [ ] 7. To'liq sinov, VER 0.6.0, push main faqat «chiqar» bilan.
- Sinovlar: `sinov/v060/sinov_bosqich1.py` (21), `sinov/bulut/sinov_bulut.py` (21), `sinov/bulut/sinov_chekka.py` (10).

## KEYINGI (g'oyalar, foydalanuvchi tasdig'isiz qilinmaydi)
- ⚔️ Jonli duel (ikki oila, videoqo'ng'iroqda) — 0.6.0 ga kirmadi.
- Arab: tajvid misollarini oyisi/ustoz izohi bilan kengaytirish.
