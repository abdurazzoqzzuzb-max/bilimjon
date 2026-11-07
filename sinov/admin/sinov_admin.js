/* Bilimjon admin.js sinovi — soxta firebase-admin (auth, firestore, securityRules) bilan. Ishga tushirish: node sinov/admin/sinov_admin.js */
'use strict';
const path = require('path'), fs = require('fs'), os = require('os'), zlib = require('zlib');
const { ishla, haftaKunlari } = require(path.join(__dirname, '..', '..', 'admin', 'admin.js'));
let XATO = 0; const ok = (c, m) => { console.log((c ? '✅ ' : '❌ ') + m); if (!c) XATO++; };
// --- soxta ombor
const ST = {}, USERS = [];
const snap = (p, d) => ({ id: p.split('/').pop(), exists: d != null, data: () => d == null ? undefined : JSON.parse(JSON.stringify(d)) });
const db = {
  doc: p => ({ get: async () => snap(p, ST[p]), set: async (d, o) => { ST[p] = o && o.merge ? Object.assign({}, ST[p] || {}, d) : Object.assign({}, d); }, delete: async () => { delete ST[p]; } }),
  collection: p => ({ get: async () => { const pre = p + '/', docs = Object.keys(ST).filter(k => k.startsWith(pre) && !k.slice(pre.length).includes('/')).map(k => snap(k, ST[k])); return { docs, size: docs.length, forEach: f => docs.forEach(f) }; } })
};
const user = (uid, email, x) => Object.assign({ uid, email, disabled: false, customClaims: null, metadata: { creationTime: 'Thu, 05 Nov 2026 10:00:00 GMT', lastSignInTime: 'Sat, 07 Nov 2026 18:00:00 GMT' } }, x || {});
const auth = {
  listUsers: async (n, t) => t ? { users: USERS.slice(2) } : { users: USERS.slice(0, 2), pageToken: USERS.length > 2 ? 'p2' : undefined },
  getUserByEmail: async e => { const u = USERS.find(x => x.email === e); if (!u) throw new Error('yo\'q'); return u; },
  updateUser: async (uid, d) => { const u = USERS.find(x => x.uid === uid); if (d.password) u._parol = d.password; if ('disabled' in d) u.disabled = d.disabled; },
  setCustomUserClaims: async (uid, c) => { USERS.find(x => x.uid === uid).customClaims = c; },
  deleteUser: async uid => { USERS.splice(USERS.findIndex(x => x.uid === uid), 1); }
};
let QOYILDI = null; const rules = { releaseFirestoreRulesetFromSource: async s => { QOYILDI = s; } };
// --- ma'lumot
USERS.push(user('UadminUID', 'admin@test.uz'), user('UjavUID', 'javlon@test.uz'), user('Ujav2UID', 'javlon2@test.uz'));
const bu = haftaKunlari(0), otgan = haftaKunlari(1);
const bola = (id, laqab, d) => ({ id, laqab, avatar: '🌸', daraja: 'g1', kun: d });
ST['oila/UadminUID'] = { j: JSON.stringify({ oila: { nom: 'Admin oila' }, tartib: ['a1'] }), ts: Date.now(), v: '0.7.5', e: 'admin@test.uz' };
ST['oila/UadminUID/bolalar/a1'] = { j: JSON.stringify(bola('a1', 'Ali', { [bu[0]]: { faol: 1800, n: 30, ok1: 27, missiya: 1 } })) };
ST['oila/UjavUID'] = { j: JSON.stringify({ oila: { nom: 'Javlon oila' }, tartib: ['s1'] }), ts: Date.now() - 3600e3, v: '0.7.4' };
ST['oila/UjavUID/bolalar/s1'] = { j: JSON.stringify(bola('s1', 'Sabo', { [bu[1]]: { faol: 1500, n: 20, ok1: 17, missiya: 1 }, [otgan[2]]: { faol: 900, n: 10, ok1: 6 } })) };
ST['oila/UjavUID/log/s1_' + bu[1]] = { bid: 's1', kun: bu[1], e: ['{"t":"ans"}'] };
ST['ruxsat/UjavUID'] = { email: 'javlon@test.uz', oila: 'Javlon oila', ts: 1, holat: 'ok' };
ST['guruh/ABCDEFGH23'] = { yaratdi: 'UadminUID', ts: 1 }; ST['guruh/ABCDEFGH23/oilalar/UadminUID'] = { ts: 1 };
const L = []; const log = s => L.push(String(s)); const run = (b, x) => ishla(b, Object.assign({ auth, db, rules, log, A1: '', A2: '', TASDIQ: '' }, x || {}));
const xato = async (b, x) => { try { await run(b, x); return null; } catch (e) { return e.message; } };
(async () => {
  L.length = 0; await run('holat'); const h = L.join('\n');
  ok(/akkauntlar: 3 ta/.test(h) && h.includes('javlon2@test.uz') && h.includes('«Javlon oila»') && h.includes('Sabo') && h.includes('v0.7.4'), 'holat: 3 akkaunt (2 sahifa), oila, bola, versiya');
  ok(h.includes('ruxsat: ruxsat bor') && h.includes("ruxsat: so'ralmagan") && h.includes("bulutda ma'lumot yo'q"), 'holat: ruxsat holatlari va bulutsiz akkaunt');
  L.length = 0; await run('statistika', { A1: 'javlon@test.uz' }); const s = L.join('\n');
  ok(s.includes("bu hafta   : 1 kun · 25 daq · 1 missiya · 85% to'g'ri (20)") && s.includes("1 hafta oldin: 1 kun · 15 daq · 0 missiya · 60% to'g'ri (10)"), 'statistika: bu hafta va o\'tgan hafta');
  L.length = 0; await run('statistika', { A1: 'hammasi' }); ok(L.join('\n').includes('Ali') && L.join('\n').includes('Sabo'), 'statistika hammasi: ikkala oila');
  await run('ruxsat', { A1: 'javlon2@test.uz', A2: 'ok' });
  ok(ST['ruxsat/Ujav2UID'] && ST['ruxsat/Ujav2UID'].holat === 'ok' && ST['ruxsat/Ujav2UID'].email === 'javlon2@test.uz', "ruxsat: so'rovsiz akkauntga ham ruxsat (yozuv yaratiladi)");
  await run('ruxsat', { A1: 'javlon@test.uz', A2: 'blok' }); ok(ST['ruxsat/UjavUID'].holat === 'blok' && ST['ruxsat/UjavUID'].oila === 'Javlon oila', "ruxsat blok: eski maydonlar saqlanadi");
  ok(/ok \| rad/.test(await xato('ruxsat', { A1: 'javlon@test.uz', A2: 'zo\'r' }) || ''), 'ruxsat: noto\'g\'ri holat rad');
  await run('admin', { A1: 'javlon2@test.uz', A2: 'ber' }); ok(USERS.find(u => u.uid === 'Ujav2UID').customClaims.admin === true, 'admin ber: custom claim');
  await run('admin', { A1: 'javlon2@test.uz', A2: 'ol' }); ok(!('admin' in USERS.find(u => u.uid === 'Ujav2UID').customClaims), 'admin ol');
  ok(/6 belgi/.test(await xato('parol', { A1: 'javlon@test.uz', A2: '123' }) || ''), 'parol: 6 belgidan kam — rad');
  L.length = 0; await run('parol', { A1: 'javlon@test.uz', A2: '08801991' });
  ok(USERS.find(u => u.uid === 'UjavUID')._parol === '08801991' && !L.join('').includes('08801991'), 'parol o\'rnatildi va logga yozilmadi');
  ok(/yo'q/.test(await xato('parol', { A1: 'yoq@test.uz', A2: '123456' }) || ''), "parol: yo'q email — tushunarli xato");
  await run('akkaunt', { A1: 'javlon@test.uz', A2: 'ochir' }); ok(USERS.find(u => u.uid === 'UjavUID').disabled, "akkaunt ochir: o'chirib qo'yildi");
  await run('akkaunt', { A1: 'javlon@test.uz', A2: 'yoq' }); ok(!USERS.find(u => u.uid === 'UjavUID').disabled, 'akkaunt yoq');
  ok(/TASDIQ=HA/.test(await xato('kochir', { A1: 'javlon@test.uz', A2: 'javlon2@test.uz' }) || ''), "kochir: tasdiqsiz — rad");
  await run('kochir', { A1: 'javlon@test.uz', A2: 'javlon2@test.uz', TASDIQ: 'HA' });
  ok(ST['oila/Ujav2UID'] && ST['oila/Ujav2UID/bolalar/s1'] && ST['oila/Ujav2UID/log/s1_' + bu[1]] && ST['oila/UjavUID/bolalar/s1'], "kochir: oila + bola + log yangi akkauntda, eskisi qoldi");
  ok(/TASDIQ=HA/.test(await xato('akkaunt', { A1: 'javlon@test.uz', A2: 'ochirish' }) || ''), "akkaunt ochirish: tasdiqsiz — rad");
  const qd = fs.mkdtempSync(path.join(os.tmpdir(), 'bjq')); fs.copyFileSync(path.join(__dirname, '..', '..', 'firestore.rules'), path.join(qd, 'firestore.rules'));
  await run('qoidalar', { A1: 'admin@test.uz', QOIDA_FAYL: path.join(qd, 'firestore.rules') });
  fs.mkdirSync(path.join(qd, 'beta')); fs.writeFileSync(path.join(qd, 'beta', 'firestore.rules'), "// beta __ADMIN_UID__ token.admin");
  await run('qoidalar', { A1: 'admin@test.uz', QOIDA_FAYL: path.join(qd, 'firestore.rules') });
  ok(QOYILDI === "// beta UadminUID token.admin", 'qoidalar: beta/firestore.rules bo\'lsa — o\'sha (eng yangi) qo\'yiladi');
  await run('qoidalar', { A1: 'admin@test.uz', QOIDA_FAYL: path.join(__dirname, '..', '..', 'firestore.rules') }).catch(() => {});
  fs.rmSync(path.join(qd, 'beta'), { recursive: true }); await run('qoidalar', { A1: 'admin@test.uz', QOIDA_FAYL: path.join(qd, 'firestore.rules') });
  ok(QOYILDI && QOYILDI.includes("'UadminUID'") && !QOYILDI.includes('__ADMIN_UID__') && QOYILDI.includes('request.auth.token.admin == true'), "qoidalar: admin uid qo'yildi, claim ham qoldi");
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'bjz')); L.length = 0; const f = await run('zaxira', { ZAXIRA_PAPKA: tmp });
  const z = JSON.parse(zlib.gunzipSync(fs.readFileSync(f)));
  ok(Object.keys(z.oila).length === 3 && z.oila.UjavUID.bolalar.s1 && Object.keys(z.oila.UjavUID.log).length === 1 && z.ruxsat.UjavUID && z.guruh.ABCDEFGH23.oilalar.UadminUID, 'zaxira: oila (bola, log), ruxsat, guruh — hammasi faylda');
  ok(/Noma'lum buyruq/.test(await xato('salom') || ''), "noma'lum buyruq — xato");
  L.length = 0; await run('yordam'); ok(L.join('').includes('statistika') && L.join('').includes('qoidalar'), 'yordam: buyruqlar ro\'yxati');
  console.log(XATO ? `\n${XATO} ta xato` : '\nHAMMASI OK'); process.exit(XATO ? 1 : 0);
})().catch(e => { console.error(e); process.exit(1); });
