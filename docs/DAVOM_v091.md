# 0.9.1 «v9.1» — DAVOM (11.11.2026 22:31, pauza: limit)
U (11.11 22:14): «takliflardan 1, 2, 4, 5, 6, 7, 8 ni yasa, tekshirib yangi versiyani chiqar» (3 — «Men o'qituvchiman» — YO'Q).
1 👏 olqish · 2 🃏 kashfiyot albomi · 4 🎯 o'z maqsadi · 5 🔥 ketma-ket kunlar · 6 📖 haftalik hikoya · 7 👨‍👩‍👧 oilaviy viktorina · 8 🎤 o'qishni yozib olish.

## Tayyor
- `docs/qoralama/t91_modul.js` — butun modul (`<script>` bloki, A.t91/olov/maqsad/albom/hikoya/olqish/viktorina/ovozim + CSS, 4 hikoya × 7 sahifa). index.html ga HALI QO'YILMAGAN, sinalmagan.

## Qoldi (tartib bilan)
1. Modulni index.html ga yangilik `<script>` idan keyin (UCH MARTA O'QISH dan oldin) qo'yish.
2. Ulash: render() — `hikoya`, `albom`, `ovozim`, `viktorina`, `maqsad` (uy + mqOyna); screenHome — `<div data-eslat></div>` dan keyin `A.t91.holatHTML(b)`, Mashq qatoridan keyin `A.t91.tilesHTML(b)`, oxirida `A.t91.uyBind(b)`;
   stepYakun — missiya=1 bo'lganda `m.t91 = A.t91.missiya(b)`; screenResult — `A.t91.natijaHTML(b, m.t91)` + `natijaBind()`; afterAnswer — recordAnswer'dan keyin `if (it.kashf && A.albom) A.albom.javob(b, it.kashf, !!e.togri_1)`;
   estafeta karta — boshqa bolaga 👏 tugma (`A.olqish.tanla`); guruhYuborIsh — `yangi` bo'lsa `d.ol = A.olqish.bulut(b)` (bo'sh bo'lmasa), fallback'da `delete d2.ol`; guruhObuna — har hujjatda `A.olqish.qabul(d.id, x, mening)`;
   yangilik — B ga hikoya/albom/ovozim/vikt/maqsad, bolimOf, VER_YANGI['0.9.1'] = [q3, maqsad, hikoya, albom, ovozim, vikt, daraxt, estafeta], b.yv.old (0.9.0 beta'dagilarga eski 3 tasi qayta chiqmasin);
   ota-ona xulosa9 — `A.t91.otaQator(b)`.
3. firestore.rules 0.9.1: azo keys + `'ol'`, `(!('ol' in d) || (d.ol is list && d.ol.size() <= 10))`. Sinovlar: v076 AZO + ol tekshiruvi + 2 oila olqish almashuvi; v090 qoidalar satri; sinov_bulut kalitlar.
4. Versiya 0.9.1 (A.VER, A.YANGI = version.json yangi, sw.js, version.json verk «9.1»).
5. sinov/v091/sinov_v091.py (har qism + 390 px + soxta mikrofon: --use-fake-ui-for-media-stream --use-fake-device-for-media-stream) → hammasi.sh ga.
6. inventar.py ga hikoya matnlari (A.hikoya.matnlar()) → main'da ovoz.
7. Beta → (u «chiqar» degan) qoidalar → prod_e2e → main merge → deploy → CLAUDE.md/TARIX → Drive OXIRGI.
