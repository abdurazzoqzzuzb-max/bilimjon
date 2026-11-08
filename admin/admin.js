#!/usr/bin/env node
/* Bilimjon — 👑 ADMIN BOSHQARUVI (Claude chatdan yoki GitHub'dan; telefon kerak emas).
   07.11.2026 (u: «telefonimni yo'qotishim, akkauntim yo'qolishi mumkin — hamma narsani shu chatdan qila olay; adminlik — o'zimning akkauntimda»).
   Ishlaydigan joyi: YOPIQ (private) repo «bilimjon-admin» dagi GitHub Actions (admin.yml) — loglar faqat egasiga ko'rinadi.
   Kalit: Firebase xizmat akkaunti (service account) JSON — secrets.FIREBASE_SA, yoki yopiq repoga yuklangan fayl (ildizda yoki kalit/ papkasida,
   nomi qanday bo'lsa ham — ichida "type": "service_account" bo'lsa topiladi; telefondan yuklash uchun). Kalit chatga HECH QACHON yozilmaydi.
   Bu fayl ochiq repoda turadi — ichida maxfiy narsa yo'q; kalitsiz hech narsa qila olmaydi.

   Buyruqlar (BUYRUQ, A1, A2, TASDIQ — muhit o'zgaruvchilari):
     yordam                         — ro'yxat
     holat                          — hamma akkauntlar: email, admin, ruxsat, oila, bolalar, oxirgi kirish/sinxron, versiya
     statistika [email|hammasi]     — bolalar: bu hafta va o'tgan 4 hafta (kun, daqiqa, missiya, aniqlik), oxirgi faol kun
     ruxsat <email> <ok|rad|blok|ochir>
     ruxsat hammasi ok              — bulutda oilasi bor hamma akkauntga ruxsat (rad/blok qilinganlardan tashqari) — qoidalardan OLDIN
     admin <email> <ber|ol>         — custom claim admin=true (qoidalardagi admin())
     parol <email> <yangi_parol>    — parolni o'rnatish (kamida 6 belgi; logda yashiriladi)
     akkaunt <email> <yoq|ochir|ochirish>   — o'chirib qo'yish / yoqish / butunlay o'chirish (ochirish — TASDIQ=HA)
     kochir <eski_email> <yangi_email>      — oila bulut ma'lumotini yangi akkauntga (TASDIQ=HA)
     qoidalar <admin_email>         — firestore.rules ni Firebase'ga qo'yish (__ADMIN_UID__ → shu akkaunt)
     qoidalar - eski                — ORQAGA: eski 0.5.0 qoidalari (ruxsat tizimisiz, hamma oila o'z bulutiga yozadi)
     zaxira                         — hamma Firestore ma'lumoti → zaxira/bilimjon_YYYY-MM-DD.json.gz (Actions artifact, 90 kun)
     guruh <email1> <email2>        — ikki oilani bitta 🏆 reyting guruhiga ulash (1-oilaning guruhi; yo'q bo'lsa — yangi kod).
                                      Telefonlar o'zi oladi (ilovani yopib qayta ochish); a'zo yozuvlarini har oila telefoni o'zi yozadi.
     telegram [@username|+998…|-]   — egasining Telegram manzili (ilova/egasi): yangi oila ruxsat so'raganda «✈️ Telegram'da egasiga yozish»
                                      xabarni shu manzilga tayyorlaydi. Bo'sh — hozirgisini ko'rsatadi, «-» — o'chiradi. (qoidalar 0.7.7 kerak emas — Admin SDK)
*/
'use strict';
const fs = require('fs'), path = require('path'), zlib = require('zlib');

const KUN = 864e5;
const tk = d => { const x = new Date(d.getTime() + 5 * 3600e3); return x.toISOString().slice(0, 10); };   // Toshkent sanasi
function haftaKunlari(oldin = 0, bugun = new Date()) {   // dushanbadan yakshanbagacha (Toshkent)
  const t = new Date(tk(bugun) + 'T00:00:00Z'), dw = (t.getUTCDay() + 6) % 7, du = new Date(t.getTime() - (dw + 7 * oldin) * KUN);
  return Array.from({ length: 7 }, (_, i) => new Date(du.getTime() + i * KUN).toISOString().slice(0, 10));
}
const vaqt = ms => { if (!ms) return '—'; const d = new Date(+ms + 5 * 3600e3); return d.toISOString().slice(8, 10) + '.' + d.toISOString().slice(5, 7) + '.' + d.toISOString().slice(0, 4) + ' ' + d.toISOString().slice(11, 16); };
const sana = k => k ? k.slice(8, 10) + '.' + k.slice(5, 7) + '.' + k.slice(0, 4) : '—';
const json = (s, d) => { try { return JSON.parse(s); } catch (e) { return d; } };
const DARAJA = { g0: 'Maktabgacha', g1: '1-sinf', g2: '2-sinf', g3: '3-sinf', g4: '4-sinf' };
const RXH = { kutish: 'kutyapti', ok: 'ruxsat bor', rad: 'rad etilgan', blok: "to'xtatilgan" };

function haftaStat(b, kunlar) {
  const K = (b && b.kun) || {}; let kun = 0, sek = 0, n = 0, ok = 0, mis = 0;
  kunlar.forEach(k => { const a = K[k]; if (!a) return; if ((a.faol || 0) > 60) kun++; sek += a.faol || 0; n += a.n || 0; ok += a.ok1 || 0; if (a.missiya) mis++; });
  return { kun, daq: Math.round(sek / 60), mis, n, foiz: n ? Math.round(ok * 100 / n) : null };
}
const oxirgiFaol = b => Object.keys((b && b.kun) || {}).filter(k => (b.kun[k].faol || 0) > 60).sort().pop() || '';

async function hammaFoydalanuvchi(auth) {
  const out = []; let t;
  do { const r = await auth.listUsers(1000, t); out.push(...r.users); t = r.pageToken; } while (t);
  return out;
}
async function foydalanuvchi(auth, email) {
  if (!email || !/@/.test(email)) throw new Error('Email kerak (A1)');
  try { return await auth.getUserByEmail(String(email).trim().toLowerCase()); } catch (e) { throw new Error('Bunday akkaunt yo\'q: ' + email); }
}
async function oilaOl(db, uid) {
  const o = await db.doc('oila/' + uid).get(), x = o.exists ? o.data() : null, j = x ? json(x.j, {}) : null, bolalar = [];
  if (x) { const s = await db.collection('oila/' + uid + '/bolalar').get(); s.forEach(d => { const b = json((d.data() || {}).j, null); if (b && b.id) bolalar.push(b); }); }
  return { bor: !!x, x, j, bolalar };
}

const B = {};
B.yordam = async ({ log }) => { log(fs.readFileSync(__filename, 'utf8').split('*/')[0].split('Buyruqlar')[1] || ''); };

B.holat = async ({ auth, db, log }) => {
  const users = await hammaFoydalanuvchi(auth), rx = {};
  (await db.collection('ruxsat').get()).forEach(d => { rx[d.id] = d.data() || {}; });
  log(`👑 Bilimjon — akkauntlar: ${users.length} ta · ${vaqt(Date.now())} (Toshkent)\n`);
  const qator = [];
  for (const u of users) {
    const o = await oilaOl(db, u.uid), r = rx[u.uid] || {}, adm = !!(u.customClaims && u.customClaims.admin);
    qator.push({ u, o, r, adm, ts: (o.x && o.x.ts) || 0 });
  }
  qator.sort((a, b) => (b.adm - a.adm) || (b.ts - a.ts));
  qator.forEach(({ u, o, r, adm }, i) => {
    log(`${i + 1}. ${u.email || '(emailsiz)'}${adm ? '  👑 ADMIN' : ''}${u.disabled ? '  ⛔ O\'CHIRILGAN' : ''}`);
    log(`   uid: ${u.uid} · ochilgan: ${vaqt(Date.parse(u.metadata.creationTime))} · oxirgi kirish: ${vaqt(Date.parse(u.metadata.lastSignInTime || '') || 0)}`);
    log(`   ruxsat: ${r.holat ? RXH[r.holat] || r.holat : "so'ralmagan"}${r.oila ? ' («' + r.oila + '»)' : ''}`);
    if (o.bor) log(`   oila: «${(o.j.oila && o.j.oila.nom) || '—'}» · bolalar: ${o.bolalar.map(b => b.laqab).join(', ') || '—'} · oxirgi sinxron: ${vaqt(o.x.ts)} · v${o.x.v || '?'}${o.j.guruh && o.j.guruh.kod ? ' · 🏆 guruh ' + o.j.guruh.kod : ''}`);
    else log(`   oila: bulutda ma'lumot yo'q`);
  });
  const eg = await db.doc('ilova/egasi').get().catch(() => null), tg = eg && eg.exists ? (eg.data() || {}).tg : '';
  log(`\n✈️ Telegram (yangi oilalar yozadi): ${tg || "qo'yilmagan — «telegram @username»"}`);
  const yetim = Object.keys(rx).filter(uid => !users.some(u => u.uid === uid));
  if (yetim.length) log(`\n⚠️ Akkaunti o'chirilgan, lekin ruxsat yozuvi qolgan: ${yetim.length} ta`);
};

B.statistika = async ({ auth, db, log, A1 }) => {
  const users = !A1 || A1 === 'hammasi' ? await hammaFoydalanuvchi(auth) : [await foydalanuvchi(auth, A1)];
  const H = [0, 1, 2, 3, 4].map(i => haftaKunlari(i));
  for (const u of users) {
    const o = await oilaOl(db, u.uid); if (!o.bor) continue;
    log(`\n🏠 «${(o.j.oila && o.j.oila.nom) || '—'}» — ${u.email}`);
    if (!o.bolalar.length) log('   bolalar yo\'q');
    o.bolalar.forEach(b => {
      log(`   ${b.avatar || '🙂'} ${b.laqab} (${DARAJA[b.daraja] || b.daraja || '?'}) · oxirgi faol kun: ${sana(oxirgiFaol(b))}`);
      H.forEach((kunlar, i) => { const s = haftaStat(b, kunlar);
        log(`      ${i === 0 ? 'bu hafta   ' : i + ' hafta oldin'}: ${s.kun} kun · ${s.daq} daq · ${s.mis} missiya · ${s.foiz == null ? 'javob yo\'q' : s.foiz + '% to\'g\'ri (' + s.n + ')'}`); });
    });
  }
};

B.ruxsat = async ({ auth, db, log, A1, A2 }) => {
  if (String(A1 || '').toLowerCase() === 'hammasi') {
    if (String(A2 || '').toLowerCase() !== 'ok') throw new Error('Faqat: ruxsat hammasi ok');
    const users = await hammaFoydalanuvchi(auth); let n = 0, otdi = 0;
    for (const u of users) {
      const o = await db.doc('oila/' + u.uid).get(); if (!o.exists) continue;
      const r = await db.doc('ruxsat/' + u.uid).get(), h0 = r.exists ? (r.data() || {}).holat : '';
      if (h0 === 'ok' || h0 === 'rad' || h0 === 'blok') { otdi++; log(`   ${u.email}: o'zgarmadi (${RXH[h0]})`); continue; }
      const j = json((o.data() || {}).j, {}), nom = (j.oila && j.oila.nom) || 'Oila';
      await db.doc('ruxsat/' + u.uid).set(Object.assign(r.exists ? {} : { email: u.email || '', oila: nom, ts: Date.now() }, { holat: 'ok', hal: Date.now() }), { merge: true });
      n++; log(`   ✅ ${u.email} («${nom}»)`);
    }
    return log(`✅ Ruxsat berildi: ${n} ta oila · o'zgarmadi: ${otdi} ta`);
  }
  const u = await foydalanuvchi(auth, A1), h = String(A2 || '').toLowerCase();
  if (h === 'ochir') { await db.doc('ruxsat/' + u.uid).delete(); return log(`🗑 ${u.email}: ruxsat yozuvi o'chirildi`); }
  if (!['ok', 'rad', 'blok'].includes(h)) throw new Error('A2: ok | rad | blok | ochir');
  const eski = await db.doc('ruxsat/' + u.uid).get();
  await db.doc('ruxsat/' + u.uid).set(Object.assign(eski.exists ? {} : { email: u.email || '', oila: 'Oila', ts: Date.now() }, { holat: h, hal: Date.now() }), { merge: true });
  log(`✅ ${u.email}: ruxsat → ${RXH[h]}`);
};

B.admin = async ({ auth, log, A1, A2 }) => {
  const u = await foydalanuvchi(auth, A1), ber = String(A2 || 'ber').toLowerCase() !== 'ol';
  const c = Object.assign({}, u.customClaims || {}); if (ber) c.admin = true; else delete c.admin;
  await auth.setCustomUserClaims(u.uid, c);
  log(`${ber ? '👑' : '↩'} ${u.email}: admin ${ber ? 'berildi' : 'olindi'}. Ilovada ☁️ dan chiqib qayta kirsin (yoki 1 soat kutsin).`);
};

B.parol = async ({ auth, log, A1, A2 }) => {
  const u = await foydalanuvchi(auth, A1);
  if (!A2 || String(A2).length < 6) throw new Error('Parol kamida 6 belgi bo\'lsin (A2)');
  await auth.updateUser(u.uid, { password: String(A2) });
  log(`🔑 ${u.email}: yangi parol o'rnatildi (logda yashirilgan). Endi ilovada shu email + yangi parol bilan «Kirish».`);
};

B.akkaunt = async ({ auth, db, log, A1, A2, TASDIQ }) => {
  const u = await foydalanuvchi(auth, A1), h = String(A2 || '').toLowerCase();
  if (h === 'yoq') { await auth.updateUser(u.uid, { disabled: false }); return log(`✅ ${u.email}: akkaunt yoqildi`); }
  if (h === 'ochir') { await auth.updateUser(u.uid, { disabled: true }); return log(`⛔ ${u.email}: akkaunt o'chirib qo'yildi (kira olmaydi; ma'lumot saqlanadi)`); }
  if (h === 'ochirish') {
    if (TASDIQ !== 'HA') throw new Error('Butunlay o\'chirish uchun TASDIQ=HA kerak');
    await auth.deleteUser(u.uid); return log(`🗑 ${u.email}: akkaunt butunlay o'chirildi (bulutdagi oila ma'lumoti qoldi — kerak bo'lsa «kochir» bilan boshqa akkauntga)`);
  }
  throw new Error('A2: yoq | ochir | ochirish');
};

B.kochir = async ({ auth, db, log, A1, A2, TASDIQ }) => {
  const s = await foydalanuvchi(auth, A1), d = await foydalanuvchi(auth, A2);
  if (s.uid === d.uid) throw new Error('Bir xil akkaunt');
  if (TASDIQ !== 'HA') throw new Error(`Ko'chirish uchun TASDIQ=HA kerak (${d.email} dagi bulut ma'lumoti almashadi)`);
  const o = await db.doc('oila/' + s.uid).get(); if (!o.exists) throw new Error(s.email + ': bulutda oila ma\'lumoti yo\'q');
  const x = o.data(), now = Date.now();
  await db.doc('oila/' + d.uid).set({ j: x.j, ts: now, q: 'admin', v: x.v || '' }, { merge: true });
  let nb = 0, nl = 0;
  for (const doc of (await db.collection('oila/' + s.uid + '/bolalar').get()).docs) { await db.doc('oila/' + d.uid + '/bolalar/' + doc.id).set({ j: doc.data().j, ts: now, q: 'admin' }); nb++; }
  for (const doc of (await db.collection('oila/' + s.uid + '/log').get()).docs) { await db.doc('oila/' + d.uid + '/log/' + doc.id).set(doc.data(), { merge: true }); nl++; }
  log(`🔁 ${s.email} → ${d.email}: oila + ${nb} bola + ${nl} kunlik log ko'chirildi. Yangi akkaunt egasi ilovani yopib qayta ochsin.`);
};

B.qoidalar = async ({ auth, db, rules, log, A1, A2, QOIDA_FAYL }) => {
  if (String(A2 || '').toLowerCase() === 'eski') {   /* orqaga qaytish: qoidalar/firestore-0.5.0.rules (admin/ruxsat yo'q) */
    const ef = path.join(path.dirname(QOIDA_FAYL), 'qoidalar', 'firestore-0.5.0.rules');
    if (!fs.existsSync(ef)) throw new Error('Eski qoidalar fayli yo\'q: qoidalar/firestore-0.5.0.rules');
    await rules.releaseFirestoreRulesetFromSource(fs.readFileSync(ef, 'utf8'));
    return log('↩ Eski (0.5.0) qoidalar qo\'yildi: ruxsat tizimi o\'chdi, har oila o\'z bulutiga avvalgidek yozadi.');
  }
  /* beta/firestore.rules — eng yangi qoidalar (beta har doim saytdagidan yangi yoki teng; qoidalar eski ilova bilan ham ishlaydi) */
  const fayl = [QOIDA_FAYL, path.join(path.dirname(QOIDA_FAYL), 'beta', 'firestore.rules')].reverse().find(f => f && fs.existsSync(f)) || QOIDA_FAYL;
  const u = await foydalanuvchi(auth, A1), t = fs.readFileSync(fayl, 'utf8');
  if (t.indexOf('__ADMIN_UID__') < 0) throw new Error('Qoidalar faylida __ADMIN_UID__ joyi yo\'q');
  const src = t.split('__ADMIN_UID__').join(u.uid);
  await rules.releaseFirestoreRulesetFromSource(src);
  log(`🛡️ Firestore qoidalari qo'yildi (admin: ${u.email}). Yangi oila endi faqat ruxsat bilan bulutga ulanadi.`);
  if (db) {   /* ogohlantirish: bulutda oilasi bor, lekin ruxsati yo'q akkauntlar endi bulutga yoza olmaydi */
    const users = await hammaFoydalanuvchi(auth), yoq = [];
    for (const x of users) {
      if (x.uid === u.uid) continue;
      const o = await db.doc('oila/' + x.uid).get(); if (!o.exists) continue;
      const r = await db.doc('ruxsat/' + x.uid).get(); if (!r.exists || (r.data() || {}).holat !== 'ok') yoq.push(x.email || x.uid);
    }
    if (yoq.length) log(`⚠️ Ruxsatsiz ${yoq.length} ta oila bulutga yoza olmaydi (telefonda ishlayveradi): ${yoq.join(', ')} → «ruxsat hammasi ok» yoki «ruxsat <email> ok»`);
    else log('✅ Bulutdagi hamma oilaning ruxsati bor.');
  }
};

B.zaxira = async ({ db, log, ZAXIRA_PAPKA }) => {
  const out = { v: 1, ts: Date.now(), oila: {}, ruxsat: {}, guruh: {} };
  for (const o of (await db.collection('oila').get()).docs) {
    const r = { doc: o.data(), bolalar: {}, log: {} };
    (await db.collection('oila/' + o.id + '/bolalar').get()).forEach(d => { r.bolalar[d.id] = d.data(); });
    (await db.collection('oila/' + o.id + '/log').get()).forEach(d => { r.log[d.id] = d.data(); });
    out.oila[o.id] = r;
  }
  (await db.collection('ruxsat').get()).forEach(d => { out.ruxsat[d.id] = d.data(); });
  for (const g of (await db.collection('guruh').get()).docs) {
    const r = { doc: g.data(), oilalar: {}, azo: {} };
    (await db.collection('guruh/' + g.id + '/oilalar').get()).forEach(d => { r.oilalar[d.id] = d.data(); });
    (await db.collection('guruh/' + g.id + '/azo').get()).forEach(d => { r.azo[d.id] = d.data(); });
    out.guruh[g.id] = r;
  }
  fs.mkdirSync(ZAXIRA_PAPKA, { recursive: true });
  const f = path.join(ZAXIRA_PAPKA, `bilimjon_${tk(new Date())}.json.gz`), buf = zlib.gzipSync(JSON.stringify(out));
  fs.writeFileSync(f, buf);
  log(`💾 Zaxira: ${Object.keys(out.oila).length} oila, ${Object.keys(out.ruxsat).length} ruxsat, ${Object.keys(out.guruh).length} guruh → ${path.basename(f)} (${Math.round(buf.length / 1024)} KB)`);
  return f;
};

/* 🏆 0.7.6: ikki oilani bitta reyting guruhiga ulash. guruh/{kod} {yaratdi, ts}, guruh/{kod}/oilalar/{uid} {ts}, oila/{uid}.j.guruh = {kod, qoshildi}.
   Kod: 1-oilaniki → bo'lmasa 2-oilaniki → bo'lmasa yangi (10 belgi, A-Z2-9). Boshqa guruhda bo'lgan oila u yerdan chiqariladi (oilalar + o'z bolalarining azo yozuvlari).
   Telefon oila hujjatini onSnapshot bilan oladi (q:'admin'); a'zo (azo) yozuvlarini — o'zi (keyingi sinxronda). */
const KOD_ALF = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
const yangiKod = () => Array.from(require('crypto').randomBytes(10), x => KOD_ALF[x % KOD_ALF.length]).join('');
B.guruh = async ({ auth, db, log, A1, A2 }) => {
  if (!A2) throw new Error('Ikkita email kerak: guruh <email1> <email2>');
  const u1 = await foydalanuvchi(auth, A1), u2 = await foydalanuvchi(auth, A2);
  if (u1.uid === u2.uid) throw new Error('Bir xil akkaunt');
  const U = [u1, u2], O = [];
  for (const u of U) { const o = await db.doc('oila/' + u.uid).get(); if (!o.exists) throw new Error(`${u.email}: bulutda oila yo'q — avval ilovaga shu akkaunt bilan kirsin (☁️ Oila akkaunti)`); O.push({ x: o.data(), j: json((o.data() || {}).j, null) }); }
  if (O.some(o => !o.j || typeof o.j !== 'object')) throw new Error("Oila hujjati o'qilmadi (j buzuq)");
  const ok = k => typeof k === 'string' && /^[A-Z2-9]{10}$/.test(k), k1 = O[0].j.guruh && O[0].j.guruh.kod, k2 = O[1].j.guruh && O[1].j.guruh.kod;
  let kod = ok(k1) ? k1 : ok(k2) ? k2 : null, yangi = false; const now = Date.now();
  if (kod && !(await db.doc('guruh/' + kod).get()).exists) { await db.doc('guruh/' + kod).set({ yaratdi: u1.uid, ts: now }); log(`ℹ️ guruh/${kod} hujjati yo'q edi — yaratildi`); }
  if (!kod) { do { kod = yangiKod(); } while ((await db.doc('guruh/' + kod).get()).exists); await db.doc('guruh/' + kod).set({ yaratdi: u1.uid, ts: now }); yangi = true; }
  for (let i = 0; i < 2; i++) {
    const u = U[i], o = O[i], eski = o.j.guruh && o.j.guruh.kod;
    if (eski && eski !== kod) {   /* boshqa guruhdan chiqarish: oilalar yozuvi va shu oila bolalarining a'zo yozuvlari */
      await db.doc('guruh/' + eski + '/oilalar/' + u.uid).delete().catch(() => {});
      let n = 0; for (const d of (await db.collection('guruh/' + eski + '/azo').get()).docs) { if ((d.data() || {}).uid === u.uid) { await db.doc('guruh/' + eski + '/azo/' + d.id).delete(); n++; } }
      log(`↪ ${u.email}: eski guruh ${eski} dan chiqarildi (${n} a'zo yozuvi)`);
    }
    await db.doc('guruh/' + kod + '/oilalar/' + u.uid).set({ ts: now });
    if (eski !== kod) { o.j.guruh = { kod, qoshildi: now }; await db.doc('oila/' + u.uid).set({ j: JSON.stringify(o.j), ts: now, q: 'admin' }, { merge: true }); }
  }
  const azo = (await db.collection('guruh/' + kod + '/azo').get()).docs.map(d => d.data() || {});
  log(`🏆 Reyting guruhi ${kod}${yangi ? ' (yangi)' : ''}: «${(O[0].j.oila && O[0].j.oila.nom) || u1.email}» + «${(O[1].j.oila && O[1].j.oila.nom) || u2.email}»`);
  log(`   a'zo yozuvlari hozir: ${azo.length} ta (${U.map(u => u.email + ': ' + azo.filter(a => a.uid === u.uid).length).join(', ')}) — qolganini telefonlar ilova ochilganda o'zi yozadi.`);
  log('   Telefonlarda: ilovani yopib qayta ochish → bola uyidagi 🏆 hafta reytingida va 🎮 o\'yinlar reytingida boshqa oila ko\'rinadi.');
};

/* ✈️ 0.7.7: egasining Telegram manzili — ilova/egasi {tg, ts}. Ochiq repoga yozilmaydi (faqat Firestore'da). */
function tgToza(t) {
  t = String(t || '').trim().replace(/^https?:\/\/(www\.)?t(elegram)?\.me\//i, '').replace(/^@/, '').replace(/[?#].*$/, '');
  if (/^[A-Za-z][A-Za-z0-9_]{4,31}$/.test(t)) return t;
  const n = t.replace(/\D/g, ''); return /^\+?[\d\s()-]+$/.test(t) && n.length >= 9 && n.length <= 15 ? '+' + n : '';
}
B.telegram = async ({ db, log, A1 }) => {
  const ref = db.doc('ilova/egasi'), v = String(A1 || '').trim();
  if (!v) { const d = await ref.get(), tg = d.exists ? (d.data() || {}).tg : ''; return log(tg ? `✈️ Telegram: ${tg}` : "✈️ Telegram hali qo'yilmagan — yangi oilalar «📤 Egasiga xabar» (ulashish) bilan yuboradi"); }
  if (v === '-' || /^o'?chir$/i.test(v)) { await ref.delete(); return log("✈️ Telegram manzili o'chirildi"); }
  const tg = tgToza(v); if (!tg) throw new Error('Telegram: @username (5–32 belgi: harf, raqam, _) yoki +998… telefon raqami');
  await ref.set({ tg, ts: Date.now() });
  log(`✈️ Telegram qo'yildi: ${tg}${tg[0] === '+' ? ' (raqam: xabar matni tayyor bo\'lmaydi — @username yaxshiroq)' : ''}. Yangi oila «✈️ Telegram'da egasiga yozish»ni bossa — xabar shu yerga keladi.`);
};

async function ishla(buyruq, deps) {
  const f = B[String(buyruq || 'yordam').toLowerCase()];
  if (!f) throw new Error('Noma\'lum buyruq: ' + buyruq + ' (yordam — ro\'yxat)');
  return f(deps);
}
/* Kalitni topish: secret → SA_FAYL → yopiq repodagi istalgan JSON (ildiz yoki kalit/) ichida "type":"service_account" */
function kalitTop(env, papka) {
  if (env.FIREBASE_SA && env.FIREBASE_SA.trim()) return { sa: env.FIREBASE_SA, manba: 'secret' };
  if (env.SA_FAYL && fs.existsSync(env.SA_FAYL)) return { sa: fs.readFileSync(env.SA_FAYL, 'utf8'), manba: 'fayl' };
  if (papka && fs.existsSync(papka)) {
    for (const d of [papka, path.join(papka, 'kalit')]) {
      if (!fs.existsSync(d)) continue;
      for (const f of fs.readdirSync(d).filter(x => /\.json$/i.test(x)).sort()) {
        const t = fs.readFileSync(path.join(d, f), 'utf8'), j = json(t, null);
        if (j && j.type === 'service_account' && j.private_key && j.client_email) return { sa: t, manba: 'fayl' };
      }
    }
  }
  return null;
}
module.exports = { ishla, B, haftaKunlari, haftaStat, tk, kalitTop, tgToza };

if (require.main === module) {
  (async () => {
    const admin = require('firebase-admin'), env = process.env;
    const k = kalitTop(env, env.SA_PAPKA);
    if (!k) throw new Error('Kalit yo\'q: secrets.FIREBASE_SA qo\'yilmagan va yopiq repoda kalit JSON fayli topilmadi');
    const cred = JSON.parse(k.sa);
    console.log(`🔑 Kalit: ${k.manba === 'secret' ? 'GitHub secret' : 'yopiq repodagi fayl'} · loyiha ${cred.project_id}`);
    admin.initializeApp({ credential: admin.credential.cert(cred), projectId: cred.project_id });
    await ishla(env.BUYRUQ, { auth: admin.auth(), db: admin.firestore(), rules: admin.securityRules(), log: s => console.log(s),
      A1: (env.A1 || '').trim(), A2: (env.A2 || '').trim(), TASDIQ: (env.TASDIQ || '').trim(),
      QOIDA_FAYL: env.QOIDA_FAYL || path.join(__dirname, '..', 'firestore.rules'), ZAXIRA_PAPKA: env.ZAXIRA_PAPKA || 'zaxira' });
  })().catch(e => { console.error('❌ ' + (e && e.message || e)); process.exit(1); });
}
