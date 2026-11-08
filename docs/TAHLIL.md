# «TAHLIL» — hamma oilalar bo'yicha individual yaxshilash (reja, 08.11; u «ha» dedi — tushunilgan talab tasdiqlandi)

U (11:24): «so'raganimda hamma oilalarning ma'lumotini birdaniga yig'ib (akkaunt, statistika, qayerda xato qilgan, reyting, nimalar bo'lgan),
qayerda xato qilayotganini topib, yangi versiyada o'sha bolaga foydali bo'ladigan qilib — individual — o'zgartirish kerak».

## Oqim (u «TAHLIL» yozadi)
1. **Yig'ish** — admin buyrug'i `tahlil [kun=7]` (yopiq repo workflow, Firebase admin): har oila → har bola: faol vaqt, kunlar, missiyalar,
   aniqlik (1-urinish), median tezlik, tugunlar (`b.tugun`: n, ok1, hint, holat, q), log `ans` dan xato savollar + xato turi, «Tushunmadim»,
   «so'rayman», «charchadim», o'yin/zal, reyting guruhi o'rni, pul/xarid. Natija — JSON (faqat yopiq repo logi / chat; OCHIQ REPOGA YOZILMAYDI).
2. **Tahlil (Claude)** — har bola: 3 zaif mavzu (sababi: xato turi, misol), 2 kuchli, tezlik/charchash, motivatsiya; umumiy: hamma yiqilgan
   savol = ilova xatosi (generator, tushuntirish, javob varianti).
3. **Individual reja** — `oila/{uid}/reja/{bid}` (admin yozadi — qoidalar o'zgarmaydi: admin oila/** ga yozadi, egasi o'qiydi):
   `{ fokus:[tugun], dars:[tugun], tez:[tugun], gacha:'YYYY-MM-DD', izoh, v }`. Ilova (0.8.0 dan) o'qiydi: missiyada fokus ×1.5–2,
   birinchi uchrashda kichik dars, kuchli mavzuda qiyinlik +1, ota-ona panelida «🎯 Bu haftaning rejasi». 7 kunda o'zi eskiradi.
   Bola hujjatiga (`bolalar/{bid}`) YOZILMAYDI — telefon o'zgarishi bilan to'qnashmasin.
4. **Umumiy tuzatishlar** — tarmoq → sinov → beta → u «chiqar» desa sayt.
5. **Hisobot unga** — har bola 2–3 qator (zaif → nima qilindi), oila bo'yicha 1 jadval.

## Bosqichlar
- 1-bosqich: `admin/admin.js` → `tahlil` + `sinov/admin` sinovi; birinchi haqiqiy hisobot.
- 2-bosqich: ilova 0.8.0 — `reja` o'qish + missiyaga ta'sir + ota-ona kartasi; sinov (soxta Firebase), beta, chiqar.
- 3-bosqich: haftalik tartib (yakshanba kechqurun u «TAHLIL» → reja → dushanbadan yangi hafta); xohlasa — avtomatik (scheduled task).

## Xavf va qoidalar
- Maxfiylik: boshqa oilalar bolalarining natijasini admin (u) va Claude ko'radi — yo'riqnomaga 1 gap qo'shish tavsiya («natijalar
  ilova egasi tomonidan o'quv rejasi uchun ko'rib chiqiladi»). Ismlar/emaillar ochiq repoga, Drive'ga yozilmaydi.
- Firestore Spark limiti (50k o'qish/kun) — 3–5 oila uchun bir tahlil ~1–2k o'qish, xavfsiz.
- Reja faqat yumshoq (ulush/tartib) — bola o'z darajasidan tushib ketmaydi; reja eskirsa ilova odatdagi moslashuvga qaytadi.
