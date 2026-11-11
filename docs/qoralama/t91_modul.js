<script>
/* Bilimjon — 🧩 0.9.1 «v9.1»: 3-bosqich takliflari (u 11.11 22:14: «takliflardan 1, 2, 4, 5, 6, 7, 8 ni yasa … tekshirib yangi versiyani chiqar»).
   Asos (11.11 taklifda aytilgan): ⭐, so'm, sovg'a va medal yetarli — yangi qismlar MUKOFOTGA emas, do'stlik, qiziquvchanlik va o'zi tanlashga quriladi
   (ortiqcha asoslash effekti). Shuning uchun bu yerda pul ham, yulduz ham berilmaydi.
   👏 Olqish — estafetada do'stiga 6 tayyor iboradan biri (erkin matn YO'Q). Shu oila bolasi — darhol (b.olq.k); boshqa oila — guruh a'zo yozuvidagi
      `ol` ro'yxati: ["<kimga bid>|<ibora 0–5>|<ts>"], ≤ 10, 3 kunlik (qoidalar 0.9.1: ixtiyoriy list ≤ 10). Qabul qiluvchi faqat o'z bolasiga yozilganini regex bilan oladi.
      Cheklov: kuniga 5 ta, bitta do'stga kuniga 1 ta.
   🃏 Kashfiyot albomi — 30 ta «Kun kashfiyoti» karta. Ochilish: KASHF javobi (eskilari tugun kun tarixidan bir marta). ★ ko'rdi · ★★ 2 to'g'ri · ★★★ «🔁 savol» to'g'ri.
   🎯 O'z maqsadi — haftada bir marta bola o'zi tanlaydi: 📅 missiya kunlari, ⭐ yulduz yoki 🍎 yangi meva (o'zlashtirgan mavzu); 👍 — o'tgan haftadan bir qadam.
      Yetganda tabrik; keyingi hafta boshida natija (tarix 8 hafta).
   🔥 Ketma-ket kunlar — missiya bajarilgan kunlar; haftada 1 kun o'tkazilsa ❄️ kechiriladi. b.kun dan hisoblanadi, saqlanadi faqat rekord (b.olovMax, b.olovBos).
   📖 Hikoya — har kunlik missiya bitta sahifa ochadi (kuniga 1). 7 sahifa — hikoya tugaydi, keyingi missiya yangisini boshlaydi. 1-sahifa — darhol sovg'a.
   👨‍👩‍👧 Oilaviy viktorina — bitta telefonda navbatma-navbat: bola o'z mavzularidan, kattalar — 2-sinfning eng qiyini va kashfiyot, vaqt kam. 10 + 5 (tez).
      Shanba–yakshanba ochiq, boshqa kun — ota-ona PIN bilan (S.viktOchiq = sana). Javoblar o'zlashtirish hisobiga kirmaydi (bolaning nusxasidan).
   🎤 Ovozim — o'lchov matnini o'qib, ovozini yozadi (MediaRecorder → IndexedDB, faqat shu telefonda; b.ovozYoz — faqat sana/soniya). 25+ kun oldingisi bilan solishtiradi.
   Yangi maydonlar bolaDefaults/defaults ga QO'SHILMAGAN: b.olq, b.albom, b.maqsad, b.mqTarix, b.mqKor, b.olovMax, b.olovBos, b.hikoya, b.ovozYoz; S.vikt, S.viktOchiq. */
(function (G) {
'use strict';
const BJ = G.BJ, A = BJ.A, FX = BJ.fx, ART = BJ.art, B = BJ.bank;
const { $, $$, esc } = A;
const toast = m => A.toast(m), sheet = (h, m, o) => A.sheet(h, m, o), closeSheets = () => A.closeSheets();
const S = () => A.S(), T = () => A.todayKey();
const sana2 = k => k ? k.slice(8, 10) + '.' + k.slice(5, 7) : '';
const tozala = s => String(s == null ? '' : s).replace(/[<>&"'`\u0000-\u001f]/g, '').trim();
const ok1 = (b, k) => { const a = (b.kun || {})[k]; return !!(a && a.missiya); };
const play = n => { try { FX.play(n); } catch (e) {} };
const burst = b => { try { FX.burst(innerWidth / 2, innerHeight * 0.3, { tema: b.dunyo, n: 40 }); } catch (e) {} };
const KUN = ['Du', 'Se', 'Ch', 'Pa', 'Ju', 'Sh', 'Ya'];
const fmtS = s => Math.floor(s / 60) + ':' + String(Math.round(s % 60)).padStart(2, '0');
const app = () => A.app;

/* ===================== 🔥 KETMA-KET KUNLAR ===================== */
const OLOV_BOS = [3, 7, 14, 30, 50, 100];
function olov(b) {
  const t = T(), bosh = b.boshlandi || b.yaratildi || t, kech = {}, muz = []; let k = ok1(b, t) ? t : A.addDays(t, -1), n = 0, oxir = null;
  for (let i = 0; i < 800 && k >= bosh; i++, k = A.addDays(k, -1)) {
    if (ok1(b, k)) { n++; oxir = k; continue; }
    const w = A.isoWeek(k); if (kech[w]) break; kech[w] = 1; muz.push(k);
  }
  const mz = oxir ? muz.filter(x => x > oxir) : [], wk = A.isoWeek(t);
  return { n, muz: mz, bugun: ok1(b, t), xavf: n > 0 && !ok1(b, t) && mz.some(x => A.isoWeek(x) === wk), max: Math.max(n, +b.olovMax || 0) };
}
function olovMissiya(b) {
  const o = olov(b); if (o.n > (+b.olovMax || 0)) b.olovMax = o.n;
  if (o.n < (+b.olovBos || 0)) b.olovBos = OLOV_BOS.filter(x => x <= o.n).pop() || 0;
  const bos = OLOV_BOS.filter(x => x <= o.n).pop(); if (bos && (+b.olovBos || 0) < bos) { b.olovBos = bos; return { n: o.n, bos }; }
  return { n: o.n, bos: 0 };
}
function haftaQator(b, belgi) {
  const D = A.weekDays(A.isoWeek()), t = T();
  return `<div class="olw">${D.map((k, i) => { const c = belgi(k, t); return `<div class="olk ${c[0]}"><b>${KUN[i]}</b><span>${c[1]}</span></div>`; }).join('')}</div>`;
}
function olovOyna(b) {
  const o = olov(b);
  sheet(`<div class="olh"><div class="olf${o.n ? '' : ' off'}">🔥</div><div><h2>${o.n ? o.n + ' kun ketma-ket!' : 'Olovni yoq!'}</h2><div class="sm mut">Eng uzun olov: ${o.max} kun</div></div></div>
  ${haftaQator(b, (k, t) => ok1(b, k) ? ['ok', '🔥'] : o.muz.includes(k) ? ['muz', '❄️'] : k === t ? ['bugun', '⏳'] : k > t ? ['kel', '·'] : ['yoq', '–'])}
  <p class="sm">🔥 Har kuni missiya — olov yonib turadi.<br>❄️ Haftada 1 kun dam olsang ham olov o'chmaydi — faqat muzlab turadi.</p>
  ${o.xavf ? '<div class="note kn">Bu hafta ❄️ ishlatilgan — bugungi missiya olovingni saqlaydi 💪</div>' : !o.n ? '<div class="note kn">Bugungi missiyani bajar — olov yonadi!</div>' : ''}
  <button class="btn big" data-x>Zo'r!</button>`);
}

/* ===================== 🎯 O'Z MAQSADI ===================== */
const MQ = {
  kun: { ic: '📅', nom: 'Missiya kunlari', bir: 'kun', val: (b, wk) => A.weekDays(wk).filter(k => ok1(b, k)).length, d: () => [4, 5, 7] },
  yulduz: { ic: '⭐', nom: 'Yulduz', bir: 'yulduz', val: (b, wk) => A.weekDays(wk).reduce((s, k) => s + (+((b.kun || {})[k] || {}).yulduz || 0), 0),
    d: lw => { const x = Math.max(40, Math.round((lw || 0) / 10) * 10); return [x, x + 30, x + 60]; } },
  meva: { ic: '🍎', nom: "Yangi meva (o'zlashtirgan mavzu)", bir: 'meva', val: (b, wk) => { const D = new Set(A.weekDays(wk)); return Object.keys(b.tugun || {}).filter(id => b.tugun[id] && b.tugun[id].holat === 'ozl' && D.has(b.tugun[id].ozlSana)).length; }, d: () => [2, 3, 5] }
};
function mqHolat(b) {
  const wk = A.isoWeek(); let m = b.maqsad && typeof b.maqsad === 'object' && MQ[b.maqsad.tur] ? b.maqsad : null;
  if (m && m.wk !== wk) {
    const v = MQ[m.tur].val(b, m.wk), h = Array.isArray(b.mqTarix) ? b.mqTarix : (b.mqTarix = []);
    if (!h.some(y => y.wk === m.wk)) { h.push({ wk: m.wk, tur: m.tur, n: m.n, v, ok: v >= m.n ? 1 : 0 }); if (h.length > 8) h.splice(0, h.length - 8); b.mqKor = m.wk; }
    b.maqsad = m = null; A.save(true);
  }
  if (!m) return { yoq: true, wk };
  const x = MQ[m.tur], v = x.val(b, wk); return { m, x, v, ok: v >= m.n, wk, p: Math.min(100, Math.round(100 * v / Math.max(1, m.n))) };
}
function mqTekshir(b) { const h = mqHolat(b); if (h.yoq || !h.ok || h.m.yetdi) return false; h.m.yetdi = T(); A.save(true); A.pushLog(b.id, { t: 'maqsad', ts: Date.now(), bola: b.id, hodisa: 'yetdi', tur: h.m.tur, n: h.m.n }); return true; }
function mqTanla(b) {
  const h = (b.mqTarix || []).slice(-1)[0], kor = b.mqKor && h && h.wk === b.mqKor ? h : null, pw = A.prevWeek(A.isoWeek());
  const rows = Object.keys(MQ).map(k => { const x = MQ[k], lw = x.val(b, pw), d = x.d(lw); let tv = d.findIndex(v => v > lw); if (tv < 0) tv = d.length - 1;
    return `<div class="mqr"><div class="mqh">${x.ic} <b>${esc(x.nom)}</b><small>o'tgan hafta: ${lw}</small></div><div class="mqo">${d.map((v, i) => `<button class="btn ${i === tv ? '' : 'ghost'}" data-mq="${k}|${v}">${v}${i === tv ? ' 👍' : ''}</button>`).join('')}</div></div>`; }).join('');
  sheet(`<h2>🎯 Bu hafta maqsading</h2>${kor ? `<div class="note kn${kor.ok ? ' gold' : ''}">O'tgan hafta: ${MQ[kor.tur].ic} ${kor.v}/${kor.n} — ${kor.ok ? '✅ bajarding! 🏆' : "deyarli! Bu hafta yana urinamiz 💪"}</div>` : ''}
  <p class="sm">O'zing tanla — yakshanbagacha bajarasan. 👍 — o'tgan haftadan bir qadam yuqori.</p>${rows}<button class="btn ghost" data-x>Keyinroq</button>`, el => {
    $$('[data-mq]', el).forEach(bt => bt.onclick = () => { const [tur, n] = bt.dataset.mq.split('|'); b.maqsad = { wk: A.isoWeek(), tur, n: +n, ts: Date.now(), yetdi: null }; delete b.mqKor; A.save(true);
      A.pushLog(b.id, { t: 'maqsad', ts: Date.now(), bola: b.id, hodisa: 'tanladi', tur, n: +n }); closeSheets(); play('ding'); toast(`🎯 Maqsad: ${n} ${MQ[tur].bir} — omad!`); A.go('uy'); });
  });
  if (kor) { delete b.mqKor; A.save(); }
}
function mqOyna(b) {
  const h = mqHolat(b); if (h.yoq) return mqTanla(b);
  const tar = (b.mqTarix || []).slice(-4).reverse().map(y => `<div class="mqtr"><span>${esc(String(y.wk).slice(5))}</span><span>${MQ[y.tur] ? MQ[y.tur].ic : ''} ${y.v}/${y.n}</span><span>${y.ok ? '✅' : '—'}</span></div>`).join('');
  const kunlar = h.m.tur === 'kun' ? haftaQator(b, (k, t) => ok1(b, k) ? ['ok', '✅'] : k === t ? ['bugun', '⏳'] : k > t ? ['kel', '·'] : ['yoq', '–']) : '';
  sheet(`<h2>🎯 Maqsadim</h2><div class="mqbig">${h.x.ic} <b>${h.v}</b> / ${h.m.n} <small>${h.x.bir}</small></div><div class="mqbar"><i style="width:${h.p}%"></i></div>${kunlar}
  <p class="sm">${h.ok ? '🏆 Maqsadingga yetding! Haftaning qolganida ham davom et.' : A.isSunday() ? 'Bugun yakshanba — hafta tugayapti. Oxirgi kuch!' : `Yana ${h.m.n - h.v} ${h.x.bir} — yakshanbagacha ulgurasan!`}</p>
  ${tar ? `<div class="sm mut">Oldingi haftalar</div>${tar}` : ''}<button class="btn big" data-x>Davom etamiz</button>`);
}

/* ===================== 🃏 KASHFIYOT ALBOMI ===================== */
const KATN = { kosmos: '🔭 Koinot', osmon: '☁️ Osmon', suv: '🌊 Suv olami', tabiat: '🌿 Tabiat', hayvon: '🐾 Hayvonlar', tana: '🫀 Tanamiz', texnika: '⚙️ Texnika', yer: '🌋 Yer sirlari' };
function alSt(b) {
  if (b.albom && typeof b.albom === 'object' && b.albom._b) return b.albom;
  const al = { _b: T() }, t = (b.tugun || {}).KASHF, bosh = b.boshlandi;
  if (t && t.kun && bosh) Object.keys(t.kun).sort().forEach(k => { if (k >= al._b) return; const D = A.dayDiff(bosh, k) + 1; if (D < 1) return; const kk = A.kashfOfDay(b, D); if (!kk) return;
    const kd = t.kun[k] || [0, 0], x = al[kk.id] || (al[kk.id] = { s: k, ok: 0, t: 0 }); x.ok += +kd[1] || 0; });
  b.albom = al; return al;
}
function alJavob(b, id, ok) { if (!id || !B.kashf.some(k => k.id === id)) return; const al = alSt(b), x = al[id] || (al[id] = { s: T(), ok: 0, t: 0 }); if (ok) x.ok = (x.ok || 0) + 1; }
const alYulduz = x => !x ? 0 : (x.t || 0) >= 1 ? 3 : (x.ok || 0) >= 2 ? 2 : 1;
function alHisob(b) { const al = alSt(b); let n = 0, y = 0; B.kashf.forEach(k => { const s = alYulduz(al[k.id]); if (s) { n++; y += s; } }); return { n, y, jami: B.kashf.length }; }
function alKeyin(b, id) { const i = B.kashf.findIndex(k => k.id === id), D = A.dayNo(b), L = B.kashf.length; return ((i - (D - 1)) % L + L) % L; }
const yulduzlar = s => `<i class="als">${'★'.repeat(s)}<u>${'☆'.repeat(3 - s)}</u></i>`;
function albomScreen(b) {
  A.theme(b.dunyo); const al = alSt(b), H = alHisob(b);
  const kart = B.kashf.map((k, i) => { const s = alYulduz(al[k.id]);
    if (!s) { const kn = alKeyin(b, k.id); return `<div class="alk yop"><span class="ale">❔</span><b>${i + 1}-karta</b><small>${kn === 0 ? 'bugun ochiladi' : `🔒 ${kn} kundan keyin`}</small></div>`; }
    return `<button class="alk s${s}" data-al="${k.id}"><span class="alsc">${ART.kashfSahna(k.kat)}</span><span class="ale">${k.em}</span><b>${esc(k.nom)}</b>${yulduzlar(s)}</button>`; }).join('');
  app().innerHTML = `<div class="wrap kidw alw"><div class="top"><button class="ib" data-back aria-label="Orqaga">←</button><div class="ttl">🃏 Kashfiyot albomi</div><span class="sp"></span><span class="pill">${H.n}/${H.jami}</span></div>
  <div class="card alhd"><div class="albar"><i style="width:${Math.round(100 * H.n / H.jami)}%"></i></div><div class="sm">📒 <b>${H.n}</b> ta karta · ⭐ ${H.y}/${H.jami * 3}. Har kunlik kashfiyot — yangi karta. Kartani bosib, 🔁 savol bilan uni ★★★ oltin qil!</div></div>
  <div class="alg">${kart}</div></div>`;
  $('[data-back]').onclick = () => A.go('uy');
  $$('[data-al]').forEach(el => el.onclick = () => alKarta(b, el.dataset.al));
}
function alKarta(b, id) {
  const k = B.kashf.find(x => x.id === id); if (!k) return; const s = alYulduz(alSt(b)[id]), q = A.qOfGrade(b), d = k.d[Math.min(q, k.d.length) - 1];
  sheet(`<div class="kcard k2 alkc"><div class="ksc low">${ART.kashfSahna(k.kat)}<div class="kmed"><span>${k.em}</span></div>${k.kat ? `<div class="kkat">${esc(KATN[k.kat] || '')}</div>` : ''}</div>
  <h2>${esc(k.nom)}</h2><div class="alst">${yulduzlar(s)}</div><p class="ktxt">${esc(d.t)}</p>
  <div class="row"><button class="btn ghost" data-en>🔊 ${k.en[1]} ${esc(k.en[0])}</button></div><div id="alq"></div>
  <div class="row" data-alr><button class="btn big" data-alq>🔁 Savol${s < 3 ? ' — oltin qil!' : ''}</button><button class="btn ghost" data-x>Yopish</button></div></div>`, el => {
    $('[data-en]', el).onclick = e => A.speak(k.en[0], 0, e.currentTarget);
    $('[data-alq]', el).onclick = () => alSavol(b, k, el);
  });
}
function alSavol(b, k, el) {
  const it = A.makeItem(A.clone(b), { tugun: 'KASHF', q: A.qOfGrade(b), tur: 'kashf', kashfId: k.id, kashfSavol: Math.floor(Math.random() * 9) });
  const st0 = { shown: Date.now(), first: null, urinish: 1, maslahat: 0, ovoz: 0 }, w = $('#alq', el), qator = $('[data-alr]', el);
  w.innerHTML = `<div class="item t-tanla alqi">${A.headHTML(b, it)}<div data-alqb></div><div data-alqf></div></div>`; qator.style.display = 'none';
  const f = $('[data-alqf]', w);
  (A.RENDER[it.t] || A.RENDER.tanla)($('[data-alqb]', w), it, b, r => {
    if (r.togri) { play('ding'); const x = alSt(b)[k.id] || (alSt(b)[k.id] = { s: T(), ok: 0, t: 0 }); x.ok = (x.ok || 0) + 1; x.t = (x.t || 0) + 1; A.save(true);
      f.innerHTML = `<div class="note kn gold">🌟 To'g'ri! Karta ★★★ — oltin</div>`; setTimeout(() => { closeSheets(); if (location.hash === '#albom') albomScreen(b); }, 1300); return; }
    if (st0.urinish < 2) { st0.urinish = 2; play('yumshoq'); f.innerHTML = `<div class="hint">💡 Matnni yana bir o'qib chiq — javob o'sha yerda</div>`; return; }
    f.innerHTML = `<div class="note">To'g'ri javob: <b>${esc(it.a)}</b>. Keyinroq yana urinib ko'r!</div>`; setTimeout(() => { qator.style.display = ''; }, 500);
  }, st0);
  try { if (A.ovoz && A.ovoz.bind) A.ovoz.bind(b, it, st0, $('.alqi', el), {}); } catch (e) {}
}

/* ===================== 📖 HIKOYA ===================== */
const FON = { bog: ['#8EC9F2', '#DDF1FF', '#6FAE52', '#4E8A3A'], mahalla: ['#F3C98B', '#FFF0D6', '#B79A7C', '#8E7258'], tun: ['#071230', '#1F3A6B', '#18291C', '#0E1A12'], stadion: ['#79C0F3', '#E3F3FF', '#C4553B', '#9E3B26'] };
const HK = [
  { id: 'h1', nom: "Kichkina urug'", em: '🌱', fon: 'bog', s: [
    ['👴🌰🧒', "Bahor kuni bobosi Sardorga kichkina o'rik danagini berdi. «Buni yerga ek, — dedi bobosi. — Bir kun u katta daraxt bo'ladi». Sardor hayron bo'ldi: shunday kichkina danakdan qanday qilib daraxt o'sadi?"],
    ['🧒🪴💧', "Sardor bog'ning quyoshli burchagini tanladi. Kurakcha bilan chuqurcha qazidi, danakni ichiga qo'ydi va ustini yumshoq tuproq bilan yopdi. Keyin «Bismillah» deb, ustidan suv quydi."],
    ['🧒🟫⏳', "Ertasi kuni Sardor yugurib bog'ga chiqdi. Hech narsa ko'rinmadi. Indiniga ham tuproq jim edi. «Balki u o'smas?» — deb xafa bo'ldi Sardor. Bobosi kulib: «Sabr qil, urug' yer ostida ishlayapti», — dedi."],
    ['🌱✨😃', "Bir hafta o'tdi. Bir kuni ertalab Sardor tuproqdan chiqib turgan yashil nihol ko'rdi! Uning ikkita kichkina bargi bor edi. Sardor quvonib qichqirdi: «Bobo, o'sdi! Urug'im o'sdi!»"],
    ['☀️🌿🪣', "Yoz keldi, havo juda issiq bo'ldi. Nihol boshini egib qoldi. Sardor har kuni ertalab va kechqurun unga suv olib keldi. Echki niholni yeb qo'ymasligi uchun atrofiga kichkina to'siq ham qildi."],
    ['🌸🌳🐝', "Yillar o'tdi. Sardor ham, daraxt ham o'sdi. Endi o'rik daraxti Sardordan ham baland edi. Bahorda u oppoq gullar bilan qoplandi, asalarilar uning atrofida g'uvillab uchib yurdi."],
    ['🍑🧺👴', "Yozda daraxt shoxlari sariq o'riklarga to'ldi. Sardor eng shirin o'riklarni terib, avval bobosiga, keyin qo'shnilarga ulashdi. Bobosi uni quchoqlab: «Ko'rdingmi, sabr va mehnat shirin meva beradi», — dedi."]] },
  { id: 'h2', nom: "Kumush kalit", em: '🔑', fon: 'mahalla', s: [
    ['🎒🔑✨', "Maktabdan qaytayotganda Zarina yo'l chetida yaltirab turgan narsani ko'rdi. Bu kichkina kumush kalit edi! Kalitga qizil ip bog'langan edi. «Bu kimniki ekan?» — deb o'yladi Zarina."],
    ['👧🔍🧵', "Uyda Zarina kalitni ukasi Bekzodga ko'rsatdi. «Keling, egasini topamiz!» — dedi Bekzod. U lupa olib, kalitni diqqat bilan ko'zdan kechirdi. Qizil ipga mayda oq iplar ilashib qolgan edi."],
    ['🤔🧵🏠', "«Ko'p oq iplar… Demak, egasi kiyim tikadi!» — dedi Zarina. Oyisi: «Mahallamizda bitta tikuvchi bor — Malika opa», — dedi. Bolalar kiyinib, yo'lga tushishdi."],
    ['🚪😟👗', "Malika opaning ustaxonasi yopiq edi. Eshik oldida u xafa holda o'tirardi. «Kalitimni yo'qotib qo'ydim, — dedi u. — Ichkarida bugun berishim kerak bo'lgan to'y libosi qoldi»."],
    ['🔑🚪🎉', "Zarina cho'ntagidan kumush kalitni chiqardi: «Shu emasmi?» Malika opaning ko'zlari porladi. U kalitni qulfga soldi va burab ko'rdi — eshik «chiq» etib ochildi!"],
    ['🙏🍬🤝', "Malika opa bolalarga rahmat aytib, ularga shirinlik bermoqchi bo'ldi. Zarina: «Rahmat, lekin biz buni sovg'a uchun qilmadik, — dedi. — Topilgan narsa egasiga qaytishi kerak»."],
    ['👜👜😊', "Kechqurun Malika opa bolalarning uyiga keldi. U Zarina va Bekzodga o'zi tikkan ikkita chiroyli sumka sovg'a qildi. «Halol bolalar — mahallaning chirog'i», — dedi u. O'sha kecha bolalar kulimsirab uxlashdi."]] },
  { id: 'h3', nom: 'Yulduzli tun', em: '🔭', fon: 'tun', s: [
    ['🌌✨👦', "Yozda Laylo va Jasur dadasi bilan qishloqqa borishdi. Kechasi hovliga chiqib, osmonga qarashdi va hayratda qolishdi: osmon son-sanoqsiz yulduzlarga to'la edi! «Shaharda nega bunchalik ko'p yulduz ko'rinmaydi?» — so'radi Jasur."],
    ['🏙️💡🌃', "«Shaharda chiroqlar juda ko'p, — dedi dadasi. — Ularning yorug'i osmonni oqartirib yuboradi. Bu yerda esa qorong'i, shuning uchun xira yulduzlar ham ko'rinadi». Laylo pichirladi: «Osmon xuddi qora baxmalga sochilgan marjonga o'xshaydi»."],
    ['✨🥄✨', "Dadasi qo'li bilan ko'rsatdi: «Ana u yettita yorqin yulduzni ko'ryapsizmi? Ular cho'michga o'xshaydi. Bu — Katta Ayiq yulduz turkumi». Jasur barmog'i bilan yulduzlarni sanab chiqdi: rostdan ham yettita!"],
    ['⭐🧭🐫', "«Cho'mich chetidagi ikki yulduzdan yuqoriga chiziq torting, — dedi dadasi. — Yorqin yulduzga yetasiz. U — Qutb yulduzi. Qadimda karvonlar kechasi yo'lni shu yulduzga qarab topishgan». Laylo: «Demak, u osmondagi kompas ekan!» — dedi."],
    ['☄️👀✨', "To'satdan osmonda yorug' chiziq chaqnab o'tdi va g'oyib bo'ldi. «Yulduz uchdi!» — qichqirdi Jasur. Dadasi tushuntirdi: «Bu yulduz emas, kichkina tosh — meteor. U havoda juda tez uchib, qizib ketadi va yonib tugaydi»."],
    ['🌕🪞🌙', "Keyin oy chiqdi. U katta va sarg'ish edi. «Oy o'zi nur sochadimi?» — so'radi Laylo. «Yo'q, — dedi dadasi. — Oy quyosh nurini qaytaradi, xuddi oyna kabi. Shuning uchun u har kecha har xil shaklda ko'rinadi»."],
    ['🌙🛌✨', "Bolalar ko'rpaga o'ranib, uzoq vaqt osmonga qarab yotishdi. «Bu osmonni, yulduzlarni kim yaratgan?» — so'radi Jasur. Dadasi mehr bilan: «Ularni Alloh yaratgan, biz esa ularni o'rganib, hayratlanamiz», — dedi. O'sha kecha bolalar yulduzlarni tushida ham ko'rishdi."]] },
  { id: 'h4', nom: 'Eng muhim musobaqa', em: '🏅', fon: 'stadion', s: [
    ['🏃📣🏆', "Maktabda katta yugurish musobaqasi e'lon qilindi. Doniyor sinfdagi eng tez bola edi va g'olib bo'lishni juda xohlardi. U har kuni ertalab hovlida yugurib, mashq qila boshladi."],
    ['🧍😔🤝', "Uning do'sti Aziz esa sekin yugurardi. «Men baribir oxirgi bo'laman», — dedi u ma'yus bo'lib. Doniyor: «Kel, birga mashq qilamiz! Har kuni ozgina tezroq yugurasan», — dedi."],
    ['🏃🏃🌅', "Ular har kuni birga yugurishdi. Doniyor Azizga to'g'ri nafas olishni o'rgatdi: burun bilan olib, og'iz bilan chiqarish. Bir haftadan keyin Aziz charchamasdan uzoqroq yugura boshladi."],
    ['🏁📯💨', "Musobaqa kuni keldi. Hushtak chalindi va bolalar oldinga otildi! Doniyor hammadan oldinda ketardi. Marraga ozgina qolganda u orqasidan «voy!» degan ovoz eshitdi."],
    ['🤕🤝🏃', "Doniyor o'girildi: Aziz yiqilib, tizzasini ushlab o'tirardi. Doniyor bir lahza o'ylandi. Keyin orqaga qaytib, do'stiga qo'lini cho'zdi: «Tur, birga marraga boramiz!»"],
    ['👏🏁👏', "Ular qo'l ushlashib marraga yetib kelishdi — eng oxirida. Lekin butun maktab o'rnidan turib, ularga qarsak chaldi! Ustoz Doniyorning yelkasiga qo'lini qo'ydi: «Bugun sen eng muhim musobaqada g'olib bo'lding»."],
    ['🏅🎨😊', "Kechqurun Doniyor dadasiga hammasini aytib berdi. «Birinchi bo'lolmadim», — dedi u. Dadasi uni quchoqladi: «Yiqilganga qo'l cho'zish — eng katta g'alaba. Do'stlik har qanday medaldan qimmat». Ertasi kuni Aziz Doniyorga o'zi chizgan medal sovg'a qildi."]] }
];
function hkSt(b) { if (b.hikoya && typeof b.hikoya === 'object' && b.hikoya.n != null) return b.hikoya; b.hikoya = { i: 0, n: 1, kun: '', o: 0, yangi: 1 }; return b.hikoya; }
const hkOf = i => HK[((i % HK.length) + HK.length) % HK.length];
function hkMissiya(b) { const h = hkSt(b), t = T(); if (h.kun === t) return null; if (h.n >= 7) { h.i++; h.n = 0; h.o = 0; } h.n++; h.kun = t; h.yangi = 1; return { nom: hkOf(h.i).nom, n: h.n }; }
const hkMatnlar = () => [].concat(...HK.map(x => x.s.map(p => p[1])));
let HKP = null;   /* ochiq sahifa: { i: hikoya, p: sahifa } — javondan o'qilsa ham */
function hkSahna(x, p) {
  const f = FON[x.fon] || FON.bog, e = Array.from(x.s[p - 1][0].matchAll ? x.s[p - 1][0].matchAll(/\p{Extended_Pictographic}(?:️|‍\p{Extended_Pictographic})*/gu) : []).map(m => m[0]);
  const yul = x.fon === 'tun' ? Array.from({ length: 22 }, (_, k) => `<i style="left:${(k * 37) % 100}%;top:${(k * 23) % 55}%;animation-delay:${(k % 5) * 0.4}s"></i>`).join('') : '';
  return `<div class="hksc ${x.fon}" style="--a:${f[0]};--b:${f[1]};--c:${f[2]};--d:${f[3]}">${yul}<div class="hkyer"></div><div class="hkem">${(e.length ? e : [x.em]).map((c, k) => `<span style="animation-delay:${k * 0.25}s">${c}</span>`).join('')}</div></div>`;
}
function hikoyaScreen(b, oqi) {
  A.theme(b.dunyo); const h = hkSt(b), joriy = hkOf(h.i);
  let P = HKP && (HKP.i !== h.i ? HKP.i < h.i : true) ? HKP : { i: h.i, p: h.yangi ? h.n : Math.max(1, Math.min(h.n, h.o || 1)) };
  const x = hkOf(P.i), max = P.i < h.i ? 7 : h.n; P.p = Math.max(1, Math.min(max, P.p)); HKP = P;
  if (P.i === h.i) { if (P.p > (h.o || 0)) h.o = P.p; if (P.p === h.n) h.yangi = 0; A.save(); }
  const tugadi = P.i === h.i && h.n >= 7 && P.p === 7, javon = Array.from({ length: Math.min(h.i, 12) }, (_, k) => h.i - 1 - k).filter(i => i >= 0);
  app().innerHTML = `<div class="wrap kidw hkw"><div class="top"><button class="ib" data-back aria-label="Orqaga">←</button><div class="ttl">📖 ${esc(x.nom)}</div><span class="sp"></span><span class="pill">${P.p}/7</span></div>
  <div class="hkb${oqi ? ' flip' : ''}">${hkSahna(x, P.p)}<div class="hkpg"><div class="hkno">${x.em} ${P.p}-sahifa</div><p class="hktx">${esc(x.s[P.p - 1][1])}</p></div>
  <div class="hkd">${Array.from({ length: 7 }, (_, k) => `<i class="${k + 1 === P.p ? 'on' : k + 1 <= max ? 'ok' : ''}"></i>`).join('')}</div></div>
  <div class="row hknav"><button class="btn ghost" data-hp ${P.p <= 1 ? 'disabled' : ''}>‹ Oldingi</button><button class="btn ghost" data-hs hidden>🔊 Eshit</button><button class="btn ghost" data-hn ${P.p >= max ? 'disabled' : ''}>Keyingi ›</button></div>
  ${P.i === h.i && P.p === h.n && h.n < 7 ? `<div class="note kn">🔒 ${h.n + 1}-sahifa — keyingi missiyadan keyin ochiladi. Nima bo'larkin?</div>` : ''}
  ${tugadi ? `<div class="note kn gold">🏁 Hikoya tugadi! Keyingi missiya — yangi hikoya boshlaydi.</div>` : ''}
  ${P.i < h.i ? `<div class="row"><button class="btn" data-hj="${h.i}">📖 Hozirgi hikoyaga qaytish</button></div>` : ''}
  ${javon.length ? `<div class="card hkj"><h3>📚 Javon — o'qilgan hikoyalar</h3>${javon.map(i => `<button class="btn ghost" data-hj="${i}">${hkOf(i).em} ${esc(hkOf(i).nom)}</button>`).join('')}</div>` : ''}
  <div class="card sm">📖 Har kunlik missiya — bitta yangi sahifa. 7 sahifa — bitta hikoya. Kichkintoylarga kattalar o'qib bersin.</div></div>`;
  $('[data-back]').onclick = () => { HKP = null; A.go('uy'); };
  const pp = $('[data-hp]'), pn = $('[data-hn]'); if (pp) pp.onclick = () => { P.p--; play('bosish'); hikoyaScreen(b, 1); }; if (pn) pn.onclick = () => { P.p++; play('bosish'); hikoyaScreen(b, 1); };
  $$('[data-hj]').forEach(bt => bt.onclick = () => { const i = +bt.dataset.hj; HKP = { i, p: i === h.i ? Math.max(1, h.o || 1) : 1 }; hikoyaScreen(b, 1); });
  try { const O = A.ovoz, r = O && O.reja ? O.reja(x.s[P.p - 1][1]) : null, sb = $('[data-hs]'); if (r && r.length && O.manba(r) && sb) { sb.hidden = false; sb.onclick = () => O.oqi(r, sb); } } catch (e) {}
}

/* ===================== 👏 OLQISH ===================== */
const OLQ = ['👏 Barakalla!', '🏃 Yetib olaman!', "🔥 Zo'r ketyapsan!", '🤝 Birga marraga!', '🌟 Sen kuchlisan!', '😊 Ertaga yana yuguramiz!'];
const OLQ_KUN = 5, OLQ_UMR = 3 * 864e5;
function olqSt(b) { const o = b.olq && typeof b.olq === 'object' ? b.olq : (b.olq = { y: [], k: [] }); if (!Array.isArray(o.y)) o.y = []; if (!Array.isArray(o.k)) o.k = []; return o; }
function olqMumkin(b, to) { const o = olqSt(b), t = T(), bu = o.y.filter(x => x.k === t); return bu.some(x => x.to === to) ? 'bir' : bu.length >= OLQ_KUN ? 'kun' : null; }
function olqYubor(b, x, i) {
  if (!x || !x.id || x.id === b.id || !(i >= 0 && i < OLQ.length) || olqMumkin(b, x.id)) return false;
  const o = olqSt(b), now = Date.now(); o.y.push({ to: x.id, i, ts: now, k: T(), nom: tozala(x.laqab).slice(0, 24), av: tozala(x.av).slice(0, 8) }); o.y = o.y.filter(y => now - y.ts < 7 * 864e5).slice(-20);
  const r = A.bola(x.id); if (r) { const ro = olqSt(r); ro.k.push({ f: b.id, nom: tozala(b.laqab).slice(0, 24), av: tozala(b.avatar).slice(0, 8), i, ts: now, yangi: 1 }); ro.k = ro.k.slice(-20); }
  A.pushLog(b.id, { t: 'olqish', ts: now, bola: b.id, kimga: x.id, i }); A.save(true); return true;
}
/* guruh a'zo yozuviga: boshqa oila bolalariga yuborilganlar (shu oila bolalari — mahalliy, bulutga chiqmaydi) */
function olqBulut(b) { const now = Date.now(); return olqSt(b).y.filter(y => !A.bola(y.to) && now - y.ts < OLQ_UMR && /^[A-Za-z0-9_-]{1,40}$/.test(y.to)).slice(-10).map(y => `${y.to}|${y.i}|${y.ts}`); }
/* boshqa oila a'zo yozuvidan (x — hujjat ma'lumoti, fid — yuboruvchi bola id) — faqat o'z bolalarimizga */
function olqQabul(fid, x, mening) {
  if (!x || !Array.isArray(x.ol)) return 0; let n = 0; const now = Date.now();
  x.ol.slice(0, 10).forEach(s => { const m = /^([A-Za-z0-9_-]{1,40})\|([0-5])\|(\d{12,14})$/.exec(String(s || '')); if (!m) return; const to = m[1], i = +m[2], ts = +m[3];
    if (!mening.has(to) || now - ts > OLQ_UMR || ts > now + 6e5) return; const r = A.bola(to); if (!r) return; const o = olqSt(r);
    if (o.k.some(k => k.f === fid && k.ts === ts)) return; o.k.push({ f: String(fid).slice(0, 40), nom: tozala(x.laqab).slice(0, 24) || 'Do\'st', av: tozala(x.av).slice(0, 8) || '🙂', oila: tozala(x.oila).slice(0, 24), i, ts, yangi: 1 }); o.k = o.k.slice(-20); n++; });
  return n;
}
function olqTanla(b, x, keyin) {
  const m = olqMumkin(b, x.id); if (m) return toast(m === 'bir' ? `👏 ${x.laqab}ga bugun olqish yubording — ertaga yana!` : '👏 Bugun 5 ta olqish yubording — ertaga yana!');
  sheet(`<h2>👏 ${esc(x.av)} ${esc(x.laqab)}ga olqish</h2><p class="sm">Birini tanla — do'sting telefonida ko'radi.</p><div class="olqg">${OLQ.map((t, i) => `<button class="btn ghost" data-oi="${i}">${esc(t)}</button>`).join('')}</div><button class="btn ghost" data-x>Bekor</button>`, el => {
    $$('[data-oi]', el).forEach(bt => bt.onclick = () => { if (olqYubor(b, x, +bt.dataset.oi)) { closeSheets(); play('ding'); toast(`👏 Yuborildi: ${OLQ[+bt.dataset.oi]}`); if (keyin) keyin(); } });
  });
}
function olqKelgan(b) { const now = Date.now(); return olqSt(b).k.filter(k => k.yangi && now - k.ts < 7 * 864e5); }
function olqHTML(b) {
  const L = olqKelgan(b).slice(-3).reverse(); if (!L.length) return '';
  return L.map(k => `<div class="olqk"><span class="olqa">${esc(k.av)}</span><div class="olqt"><b>${esc(k.nom)} senga:</b><span>«${esc(OLQ[k.i] || OLQ[0])}»</span></div><button class="btn sm" data-olqr="${esc(k.f)}|${k.ts}">😊 Rahmat</button>${olqMumkin(b, k.f) ? '' : `<button class="ib" data-olqj="${esc(k.f)}|${k.ts}" aria-label="Javob">↩️</button>`}</div>`).join('');
}
function olqBind(b) {
  const top = s => { const [f, ts] = s.split('|'); return olqSt(b).k.find(k => k.f === f && String(k.ts) === ts); };
  $$('[data-olqr]').forEach(bt => bt.onclick = () => { const k = top(bt.dataset.olqr); if (k) { k.yangi = 0; A.save(true); } play('bosish'); A.go('uy'); A.render(); });
  $$('[data-olqj]').forEach(bt => bt.onclick = () => { const k = top(bt.dataset.olqj); if (!k) return; olqTanla(b, { id: k.f, laqab: k.nom, av: k.av }, () => { k.yangi = 0; A.save(true); A.render(); }); });
}

/* ===================== 👨‍👩‍👧 OILAVIY VIKTORINA ===================== */
const VK_VAQT = { bola: { tez: 12000, max: 25000 }, katta: { tez: 5000, max: 10000 } };
const KATTA = [{ id: 'ota', av: '👨', nom: 'Dada' }, { id: 'ona', av: '👩', nom: 'Oyi' }];
let VK = null;
const vkOchiq = () => { if (A.TEZ) return true; const d = new Date().getDay(); return d === 0 || d === 6 || S().viktOchiq === T(); };
function vkKirish() {
  if (vkOchiq()) return A.go('viktorina');
  sheet(`<h2>👨‍👩‍👧 Oilaviy viktorina</h2><p>Dam olish kunlari — shanba va yakshanba ochiladi: butun oila bitta telefonda navbatma-navbat savol yechadi.</p><p class="sm">Bugun ochish — ota-ona PIN kodi bilan.</p>
  <input id="vkp" class="inp mono" type="password" inputmode="numeric" maxlength="4" autocomplete="off" placeholder="PIN"><div class="row"><button class="btn" data-ok>🔑 Bugun ochish</button><button class="btn ghost" data-x>Keyinroq</button></div>`, el => {
    $('[data-ok]', el).onclick = () => { const s = S(), hh = A.pinHash($('#vkp', el).value.trim()); if (!hh || (hh !== s.pin && !(s.pinOta && hh === s.pinOta))) return toast("PIN noto'g'ri"); s.viktOchiq = T(); A.save(true); closeSheets(); A.go('viktorina'); };
  });
}
const glN = b => +String(A.gl(b.daraja)).slice(1) || 0;
function vkScreen(b) {
  if (VK && VK.faol) { if (!$('.vkw')) vkNavbat(b); return; }
  if (!vkOchiq()) return A.go('uy');
  A.theme(b.dunyo); const L = A.bolalar(), s = S(), oxir = (s.vikt || []).slice(-1)[0];
  app().innerHTML = `<div class="wrap kidw vkw"><div class="top"><button class="ib" data-back aria-label="Orqaga">←</button><div class="ttl">👨‍👩‍👧 Oilaviy viktorina</div></div>
  <div class="card vkhero"><div class="vkh">🏆</div><p>Bitta telefonda navbatma-navbat! Bolalar — o'z darajasida, kattalar — qiyinroq va vaqti kam. To'g'ri javob — <b>10</b> ball, tez javob — yana <b>+5</b>.</p></div>
  <div class="card"><h3>Kim o'ynaydi?</h3><div class="vkp">${L.map(x => `<label class="vko"><input type="checkbox" data-vo="b:${esc(x.id)}" checked><span>${esc(x.avatar)}</span><b>${esc(x.laqab)}</b></label>`).join('')}${KATTA.map(x => `<label class="vko"><input type="checkbox" data-vo="k:${x.id}" checked><span>${x.av}</span><b>${x.nom}</b></label>`).join('')}</div>
  <h3>Nechta aylana?</h3><div class="row vkr">${[3, 5].map(n => `<button class="btn ${n === 3 ? '' : 'ghost'}" data-vr="${n}">${n} aylana</button>`).join('')}</div><button class="btn big" data-vgo>▶ Boshlash</button></div>
  ${oxir ? `<div class="card sm">🏆 Oxirgi o'yin (${sana2(oxir.sana)}): ${oxir.o.map(([n, bl], i) => `${['🥇', '🥈', '🥉'][i] || '·'} ${esc(n)} ${bl}`).join('  ')}</div>` : ''}</div>`;
  let R = 3; $('[data-back]').onclick = () => A.go('uy');
  $$('[data-vr]').forEach(x => x.onclick = () => { R = +x.dataset.vr; $$('[data-vr]').forEach(y => y.classList.toggle('ghost', y !== x)); });
  $('[data-vgo]').onclick = () => {
    const oy = $$('[data-vo]').filter(i => i.checked).map(i => { const [t, id] = i.dataset.vo.split(':'); if (t === 'b') { const x = A.bola(id); return x ? { id, nom: x.laqab, av: x.avatar, bid: id, katta: false, ball: 0, ok: 0 } : null; } const k = KATTA.find(y => y.id === id); return { id, nom: k.nom, av: k.av, katta: true, ball: 0, ok: 0 }; }).filter(Boolean);
    if (oy.length < 2) return toast('Kamida 2 kishi kerak'); if (!oy.some(x => !x.katta)) return toast('Kamida 1 bola kerak');
    const kat = L.slice().sort((p, q) => glN(q) - glN(p))[0];
    VK = { faol: 1, oy, R, i: 0, n: oy.length * R, kat: kat.id }; A.pushLog(b.id, { t: 'vikt', ts: Date.now(), bola: b.id, hodisa: 'boshlandi', n: oy.length, R }); vkNavbat(b);
  };
}
function vkJadval(V, top) { const L = V.oy.slice().sort((x, y) => y.ball - x.ball); return `<div class="card vkj">${L.map((x, i) => `<div class="vkjr${top && i === 0 ? ' g' : ''}"><span class="vkn">${i + 1}</span><span>${esc(x.av)}</span><b>${esc(x.nom)}</b><span class="sp"></span><b>${x.ball}</b></div>`).join('')}</div>`; }
function vkChiq(b) { sheet(`<h2>O'yinni to'xtatamizmi?</h2><p class="sm">Ballar saqlanmaydi.</p><div class="row"><button class="btn danger" data-ok>⏹ To'xtatish</button><button class="btn ghost" data-x>Davom</button></div>`, el => { $('[data-ok]', el).onclick = () => { closeSheets(); vkTozala(); A.go('uy'); }; }); }
function vkTozala() { if (VK && VK.tm) clearInterval(VK.tm); VK = null; }
function vkNavbat(b) {
  const V = VK; if (!V) return A.go('viktorina'); if (V.i >= V.n) return vkYakun(b);
  const p = V.oy[V.i % V.oy.length], ay = Math.floor(V.i / V.oy.length) + 1;
  app().innerHTML = `<div class="wrap kidw vkw"><div class="top"><button class="ib" data-vx aria-label="Chiqish">✕</button><div class="ttl">👨‍👩‍👧 ${ay}/${V.R}-aylana</div><span class="sp"></span><span class="pill">${V.i + 1}/${V.n}</span></div>
  <div class="vknav"><div class="vkav">${esc(p.av)}</div><h2>Navbat: ${esc(p.nom)}</h2><p>${p.katta ? 'Kattalar savoli — qiyinroq, vaqt kam! ⚡' : 'Telefonni ' + esc(p.nom) + 'ga bering 📱'}</p><button class="btn big" data-vt>✋ Tayyorman</button></div>${vkJadval(V)}</div>`;
  $('[data-vx]').onclick = () => vkChiq(b); $('[data-vt]').onclick = () => vkSavol(b, p);
}
function vkItem(V, p) {
  const yaroq = it => it && (!it.t || it.t === 'tanla') && Array.isArray(it.o) && it.o.length >= 2 && typeof it.matn !== 'string';
  const kat = A.bola(V.kat) || A.bolalar()[0];
  for (let k = 0; k < 12; k++) {
    let it = null; try {
      if (p.katta) { const kb = A.clone(kat);
        if (k % 3 === 0 || Math.random() < 0.35) { const kk = B.kashf[Math.floor(Math.random() * B.kashf.length)]; it = A.makeItem(kb, { tugun: 'KASHF', q: 3, tur: 'vikt', kashfId: kk.id, kashfSavol: Math.floor(Math.random() * 9) }); }
        else { const ids = (A.ZANJIR.mat || []).filter(id => /^M2\./.test(id) && BJ.gen.reg[id] && !A.UZUN[id]); const id = ids[Math.floor(Math.random() * ids.length)]; it = A.makeItem(kb, { tugun: id, q: 3, tur: 'vikt' }); } }
      else { const kb = A.clone(A.bola(p.bid)); const ids = Object.keys(kb.tugun || {}).filter(id => BJ.gen.reg[id] && kb.tugun[id].n > 0 && !A.UZUN[id] && !/^(KASHF|OL|Y\d)/.test(id) && BJ.gen.reg[id].fan !== 'yoz');
        if (ids.length && Math.random() < 0.75) { const id = ids[Math.floor(Math.random() * ids.length)]; it = A.makeItem(kb, { tugun: id, q: Math.max(1, kb.tugun[id].q || 1), tur: 'vikt' }); }
        else { const kk = B.kashf[Math.floor(Math.random() * B.kashf.length)]; it = A.makeItem(kb, { tugun: 'KASHF', q: A.qOfGrade(kb), tur: 'vikt', kashfId: kk.id, kashfSavol: Math.floor(Math.random() * 9) }); }
        it.__b = kb; }
    } catch (e) { it = null; }
    if (yaroq(it)) { if (!it.__b) it.__b = A.clone(kat); return it; }
  }
  const it = A.makeItem(A.clone(kat), { tugun: 'M1.1', q: 1, tur: 'vikt' }); it.__b = A.clone(kat); return it;
}
function vkSavol(b, p) {
  const V = VK; if (!V) return; const it = vkItem(V, p), kb = it.__b, lim = p.katta ? VK_VAQT.katta : VK_VAQT.bola, st0 = { shown: Date.now(), first: null, urinish: 2, maslahat: 0, ovoz: 0 };
  app().innerHTML = `<div class="wrap play vkw"><div class="top"><button class="ib" data-vx aria-label="Chiqish">✕</button><div class="ttl">${esc(p.av)} ${esc(p.nom)}</div><span class="sp"></span><span class="pill">🏅 ${p.ball}</span></div>
  <div class="vkt"><i data-vtb></i></div><div class="item t-tanla">${A.headHTML(kb, it)}<div id="body"></div><div id="fb"></div></div></div>`;
  let tugadi = false; const t0 = Date.now(), bar = $('[data-vtb]');
  const fin = r => {
    if (tugadi || VK !== V) return; tugadi = true; clearInterval(V.tm); const ms = Date.now() - t0, ok = !!r.togri, tez = ok && ms <= lim.tez, ball = ok ? 10 + (tez ? 5 : 0) : 0; p.ball += ball; if (ok) p.ok++;
    $$('.opt').forEach(x => { x.disabled = true; if (!ok && x.dataset.v === String(it.a)) x.classList.add('ok'); });
    const o = (it.o || []).find(y => y.v === String(it.a)), jt = o && !o.vis ? String(o.h != null ? o.h : o.v) : '';
    play(ok ? 'ding' : 'yumshoq'); $('#fb').innerHTML = `<div class="note kn${ok ? ' gold' : ''}">${ok ? `✅ +${ball}${tez ? ' ⚡ tez!' : ''}` : r.vaqt ? '⏰ Vaqt tugadi' : '❌ Bu safar emas'}${!ok && jt ? ` · to'g'risi: <b>${esc(jt)}</b>` : ''}</div><button class="btn big" data-vn>Keyingi ➜</button>`;
    $('[data-vn]').onclick = () => { V.i++; vkNavbat(b); };
  };
  V.tm = setInterval(() => { const e = Date.now() - t0; if (bar) { bar.style.width = Math.max(0, 100 - 100 * e / lim.max) + '%'; bar.classList.toggle('tez', e <= lim.tez); } if (e >= lim.max) fin({ togri: false, vaqt: 1 }); }, 120);
  (A.RENDER[it.t] || A.RENDER.tanla)($('#body'), it, kb, r => fin(r), st0);
  $('[data-vx]').onclick = () => vkChiq(b);
  try { if (A.ovoz && A.ovoz.bind && !p.katta) A.ovoz.bind(kb, it, st0, $('.item'), {}); } catch (e) {}
}
function vkYakun(b) {
  const V = VK, L = V.oy.slice().sort((x, y) => y.ball - x.ball), s = S(), g = L[0];
  s.vikt = (Array.isArray(s.vikt) ? s.vikt : []).concat([{ sana: T(), n: V.R, o: L.map(x => [x.nom, x.ball]) }]).slice(-10); A.save(true);
  L.forEach((x, i) => { if (x.bid) A.pushLog(x.bid, { t: 'vikt', ts: Date.now(), bola: x.bid, hodisa: 'tugadi', ball: x.ball, orin: i + 1, n: L.length }); });
  const katta = L.filter(x => x.katta), yengdi = L.filter(x => !x.katta && katta.length && katta.some(k => k.ball < x.ball));
  const kat = A.bola(V.kat) || b; vkTozala();
  app().innerHTML = `<div class="wrap kidw vkw"><div class="oyfin vkfin"><div class="q3t">🏆</div><h2>${esc(g.av)} ${esc(g.nom)} — g'olib!</h2>
  <div class="vkpod">${L.slice(0, 3).map((x, i) => `<div class="vkpd p${i + 1}"><span>${esc(x.av)}</span><b>${esc(x.nom)}</b><i>${x.ball}</i><u>${i + 1}</u></div>`).join('')}</div>
  ${yengdi.length ? `<div class="note kn gold">🎉 ${yengdi.map(x => esc(x.nom)).join(', ')} kattalardan o'zib ketdi!</div>` : ''}${vkJadval({ oy: L }, true)}
  <p class="sm">Keyingi dam olish kunida yana o'ynaymiz!</p><div class="row"><button class="btn big" data-vq>🔁 Yana bir o'yin</button><button class="btn big alt" data-home>🏠 Uyga</button></div></div></div>`;
  play('fanfar'); burst(kat);
  $('[data-vq]').onclick = () => vkScreen(b); $('[data-home]').onclick = () => A.go('uy');
}

/* ===================== 🎤 OVOZIM ===================== */
const OV_AR = { id: 'ar1', nom: 'Arabcha matn', ar: 1, t: 'ذَهَبَ أَحْمَدُ إِلَى الْمَدْرَسَةِ. فِي الْمَدْرَسَةِ مُعَلِّمٌ وَطُلَّابٌ. يَقْرَأُ أَحْمَدُ كِتَابًا جَمِيلًا. ثُمَّ يَرْجِعُ إِلَى الْبَيْتِ وَيُسَاعِدُ أُمَّهُ.' };
const OV_G0 = { id: 'uz0', nom: "So'zlar", t: "Ona. Ota. Olma. Bola. Non. Suv. Gul. Uy. Ari. Kun. Mushuk. Qalam." };
function ovMatn(b, til) {
  if (til === 'ar') return OV_AR; const L = A.gl(b.daraja); if (L === 'g0') return OV_G0;
  const m = (B.matn || []).find(x => x.id === (L === 'g1' ? 'm2' : 'm5')) || (B.matn || [])[0]; return m ? { id: m.id, nom: m.nom, t: m.t } : OV_G0;
}
const IDB_NOM = 'bilimjon-ovozim', IDB_OS = 'yozuv'; let IDBp = null;
function idb() {
  if (IDBp) return IDBp;
  IDBp = new Promise((res, rej) => { try { const r = indexedDB.open(IDB_NOM, 1); r.onupgradeneeded = () => { const db = r.result; if (!db.objectStoreNames.contains(IDB_OS)) db.createObjectStore(IDB_OS, { keyPath: 'id' }); }; r.onsuccess = () => res(r.result); r.onerror = () => rej(r.error); } catch (e) { rej(e); } });
  IDBp.catch(() => { IDBp = null; }); return IDBp;
}
function idbIsh(mode, fn) { return idb().then(db => new Promise((res, rej) => { const tx = db.transaction(IDB_OS, mode), rq = fn(tx.objectStore(IDB_OS)); tx.oncomplete = () => res(rq ? rq.result : undefined); tx.onerror = () => rej(tx.error); tx.onabort = () => rej(tx.error); })); }
const idbPut = r => idbIsh('readwrite', st => st.put(r)), idbGet = id => idbIsh('readonly', st => st.get(id)), idbDel = id => idbIsh('readwrite', st => st.delete(id));
let REC = null, OVTIL = 'uz', OVURL = [];
function ovRoyxat(b, til, mid) { return (Array.isArray(b.ovozYoz) ? b.ovozYoz : []).filter(x => x.til === til && (!mid || x.m === mid)).sort((p, q) => p.ts - q.ts); }
function ovSolishtir(b, til, mid) { const L = ovRoyxat(b, til, mid); if (L.length < 2) return { L }; const y = L[L.length - 1], e = L.filter(x => x.ts <= y.ts - 25 * 864e5).pop() || null; return { L, yangi: y, eski: e, birinchi: L[0] }; }
const sozSoni = t => String(t).split(/\s+/).filter(Boolean).length;
function ovTozala() { OVURL.forEach(u => { try { URL.revokeObjectURL(u); } catch (e) {} }); OVURL = []; }
function recTugat(saqlama) {
  const R = REC; if (!R) return; R.on = false; clearInterval(R.tm); if (saqlama) R.bekor = 1;
  try { if (R.mr && R.mr.state !== 'inactive') R.mr.stop(); } catch (e) {}
  try { R.st.getTracks().forEach(t => t.stop()); } catch (e) {} try { if (R.ac) R.ac.close(); } catch (e) {}
}
async function recBosh(b) {
  if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia || typeof MediaRecorder === 'undefined') return toast("Bu brauzerda ovoz yozib bo'lmaydi — Safari yoki Chrome'ni yangilang");
  let st; try { st = await navigator.mediaDevices.getUserMedia({ audio: { echoCancellation: true, noiseSuppression: true } }); }
  catch (e) { return sheet(`<h2>🎤 Mikrofonga ruxsat kerak</h2><p>Telefon mikrofonni bermadi.</p><p class="sm">iPhone: Настройки → Приложения → Safari → Микрофон → «Разрешить» (eski iOS: Настройки → Safari → Микрофон).<br>Android: Chrome → ⋮ → Настройки → Настройки сайтов → Микрофон → ruxsat.</p><button class="btn big" data-x>Tushunarli</button>`); }
  if (location.hash !== '#ovozim') { try { st.getTracks().forEach(t => t.stop()); } catch (e) {} return; }
  const mt = ['audio/mp4', 'audio/webm;codecs=opus', 'audio/webm', 'audio/ogg;codecs=opus'].find(t => { try { return MediaRecorder.isTypeSupported(t); } catch (e) { return false; } }) || '';
  let mr; try { mr = mt ? new MediaRecorder(st, { mimeType: mt }) : new MediaRecorder(st); } catch (e) { mr = new MediaRecorder(st); }
  const matn = ovMatn(b, OVTIL), R = REC = { mr, st, ch: [], t0: Date.now(), til: OVTIL, matn, on: true, mt: mr.mimeType || mt || 'audio/webm' };
  mr.ondataavailable = e => { if (e.data && e.data.size) R.ch.push(e.data); };
  mr.onstop = () => { R.sek = Math.max(1, Math.round((Date.now() - R.t0) / 100) / 10); if (R.bekor) { REC = null; return; } R.blob = new Blob(R.ch, { type: R.mt.split(';')[0] }); ovKorib(b, R); };
  try { const AC = window.AudioContext || window.webkitAudioContext; const ac = new AC(), an = ac.createAnalyser(); an.fftSize = 256; ac.createMediaStreamSource(st).connect(an); R.ac = ac; R.an = an; R.buf = new Uint8Array(an.fftSize); } catch (e) {}
  mr.start(1000); play('bosish'); ovScreen(b);
  R.tm = setInterval(() => { const s = (Date.now() - R.t0) / 1000, tm = $('[data-rt]'); if (tm) tm.textContent = fmtS(s);
    if (R.an) { R.an.getByteTimeDomainData(R.buf); let m = 0; for (let k = 0; k < R.buf.length; k++) m = Math.max(m, Math.abs(R.buf[k] - 128)); const lv = $('[data-rl]'); if (lv) lv.style.setProperty('--l', Math.min(1, m / 60).toFixed(2)); }
    if (s >= 180) recTugat(); }, 100);
}
function ovKorib(b, R) {
  const u = URL.createObjectURL(R.blob); OVURL.push(u); const w = $('[data-ovst]'); if (!w) { REC = null; return; }
  w.innerHTML = `<div class="ovrv"><div class="sm mut">⏱ ${fmtS(R.sek)} · ${Math.round(sozSoni(R.matn.t) * 60 / R.sek)} so'z/daqiqa</div><audio controls src="${u}" preload="auto"></audio><div class="row"><button class="btn big" data-ovs>💾 Saqlash</button><button class="btn ghost" data-ovq>🔁 Qayta yozish</button></div></div>`;
  $('[data-ovq]', w).onclick = () => { REC = null; ovScreen(b); };
  $('[data-ovs]', w).onclick = async () => {
    const id = 'oz' + Date.now().toString(36), rec = { id, bid: b.id, til: R.til, m: R.matn.id, sana: T(), ts: Date.now(), sek: R.sek, mime: R.blob.type || 'audio/webm' };
    try { rec.buf = await R.blob.arrayBuffer(); await idbPut(rec); } catch (e) { return toast("Saqlab bo'lmadi — telefon xotirasi to'lgan bo'lishi mumkin"); }
    const L = Array.isArray(b.ovozYoz) ? b.ovozYoz : (b.ovozYoz = []); L.push({ id, til: rec.til, m: rec.m, sana: rec.sana, ts: rec.ts, sek: rec.sek });
    /* har (til, matn) uchun: eng birinchisi + oxirgi 10 ta qoladi */
    const bir = ovRoyxat(b, rec.til, rec.m); if (bir.length > 11) bir.slice(1, bir.length - 10).forEach(x => { const j = L.indexOf(x); if (j >= 0) L.splice(j, 1); idbDel(x.id).catch(() => {}); });
    A.pushLog(b.id, { t: 'ovozim', ts: Date.now(), bola: b.id, til: rec.til, matn: rec.m, sek: rec.sek }); A.save(true); REC = null; play('ding'); toast('💾 Ovozing saqlandi!'); ovScreen(b);
  };
}
async function ovIjro(id, el) {
  try { const r = await idbGet(id); if (!r || !r.buf) return toast("Bu yozuv boshqa telefonda qolgan"); const u = URL.createObjectURL(new Blob([r.buf], { type: r.mime || 'audio/webm' })); OVURL.push(u);
    document.querySelectorAll('audio.ovpl').forEach(a => { try { a.pause(); } catch (e) {} }); const au = el.parentNode.querySelector('audio.ovpl') || Object.assign(document.createElement('audio'), { className: 'ovpl' });
    au.src = u; au.controls = true; if (!au.isConnected) el.parentNode.appendChild(au); await au.play().catch(() => {}); } catch (e) { toast("Ijro etib bo'lmadi"); }
}
function ovScreen(b) {
  if (REC && REC.on && $('.ovw')) return;
  A.theme(b.dunyo); const m = ovMatn(b, OVTIL), C = ovSolishtir(b, OVTIL, m.id), W = sozSoni(m.t), tez = x => Math.round(W * 60 / Math.max(1, x.sek)), yoz = !!(REC && REC.on);
  let cmp = '';
  if (C.eski) { const f = Math.round(100 * (C.eski.sek - C.yangi.sek) / C.eski.sek), kun = A.dayDiff(C.eski.sana, C.yangi.sana);
    cmp = `<div class="card ovcmp"><h3>⚖️ ${kun} kun oldin va hozir</h3><div class="ovc"><div><small>${sana2(C.eski.sana)}</small><b>${fmtS(C.eski.sek)}</b><span>${tez(C.eski)} so'z/daq</span><button class="btn sm ghost" data-ovp="${C.eski.id}">▶ Oldin</button></div><div class="ovar">➜</div><div><small>${sana2(C.yangi.sana)}</small><b>${fmtS(C.yangi.sek)}</b><span>${tez(C.yangi)} so'z/daq</span><button class="btn sm" data-ovp="${C.yangi.id}">▶ Hozir</button></div></div>
    <div class="note kn${f > 0 ? ' gold' : ''}">${f > 0 ? `🚀 ${f}% tezroq o'qiyapsan! O'z qulog'ing bilan eshitib ko'r.` : f < 0 ? "Bugun sekinroq — lekin aniq o'qish ham muhim. Ovozlarni eshitib solishtir." : 'Xuddi o\'sha tezlikda — eshitib solishtir!'}</div></div>`; }
  else if (C.L.length) { const kun = A.dayDiff(C.L[0].sana, T()); cmp = `<div class="card sm">📅 Birinchi yozuving: ${sana2(C.L[0].sana)} (${kun} kun oldin). Har hafta bir marta yoz — 1 oydan keyin o'sganingni eshitib, solishtirasan.</div>`; }
  app().innerHTML = `<div class="wrap kidw ovw"><div class="top"><button class="ib" data-back aria-label="Orqaga">←</button><div class="ttl">🎤 Ovozim</div></div>
  <div class="row ovtab"><button class="btn ${OVTIL === 'uz' ? '' : 'ghost'}" data-ovt="uz" ${yoz ? 'disabled' : ''}>📖 O'zbekcha</button><button class="btn ${OVTIL === 'ar' ? '' : 'ghost'}" data-ovt="ar" ${yoz ? 'disabled' : ''}>🕌 Arabcha</button></div>
  <div class="card ovm"><div class="sm mut">O'lchov matni: ${esc(m.nom)} · ${W} so'z</div><p class="ovtx${m.ar ? ' arab' : ''}"${m.ar ? ' dir="rtl" lang="ar"' : ''}>${esc(m.t)}</p></div>
  <div class="card ovrec" data-ovst>${yoz ? `<div class="ovmic on" data-rl><span>🎤</span></div><div class="ovtm mono" data-rt>0:00</div><button class="btn big danger" data-ovstop>⏹ To'xtatish</button>`
    : `<button class="ovmic" data-ovgo aria-label="Yozishni boshlash"><span>🎤</span></button><div class="sm">Tugmani bos va matnni ovoz chiqarib o'qi. Tugatgach — ⏹.</div>`}</div>
  ${cmp}${C.L.length ? `<div class="card ovl"><h3>🗂 Yozuvlarim</h3>${C.L.slice().reverse().map(x => `<div class="ovli"><span>${sana2(x.sana)}</span><b>${fmtS(x.sek)}</b><span class="mut">${tez(x)} so'z/daq</span><span class="sp"></span><button class="btn sm ghost" data-ovp="${x.id}">▶</button></div>`).join('')}</div>` : ''}
  <div class="card sm">🔒 Ovoz faqat shu telefonda saqlanadi — internetga yuborilmaydi.</div></div>`;
  $('[data-back]').onclick = () => { recTugat(true); REC = null; A.go('uy'); };
  $$('[data-ovt]').forEach(x => x.onclick = () => { OVTIL = x.dataset.ovt; ovScreen(b); });
  const g = $('[data-ovgo]'); if (g) g.onclick = () => recBosh(b);
  const sp = $('[data-ovstop]'); if (sp) sp.onclick = () => recTugat();
  $$('[data-ovp]').forEach(x => x.onclick = () => ovIjro(x.dataset.ovp, x));
}

/* ===================== 🏠 UY EKRANI, YAKUN, OTA-ONA ===================== */
function holatHTML(b) {
  const o = olov(b), h = mqHolat(b);
  const mq = h.yoq ? `<button class="t9c mqc yangi" data-maqsad>🎯 <b>Hafta maqsadini tanla</b></button>`
    : `<button class="t9c mqc${h.ok ? ' ok' : ''}" data-maqsad>🎯 <b>${h.v}/${h.m.n}</b> <small>${esc(h.x.bir)}${h.ok ? ' ✅' : ''}</small><i style="width:${h.p}%"></i></button>`;
  return `<div class="t9s"><button class="t9c olc${o.n ? '' : ' off'}${o.xavf ? ' xavf' : ''}" data-olov>🔥 <b>${o.n}</b> <small>kun</small></button>${mq}</div>${olqHTML(b)}`;
}
function tilesHTML(b) {
  const h = hkSt(b), x = hkOf(h.i), al = alHisob(b), oy = ovRoyxat(b, 'uz').concat(ovRoyxat(b, 'ar')).sort((p, q) => p.ts - q.ts).pop(), vo = vkOchiq();
  return `<div class="t9g">
  <button class="t9t${h.yangi ? ' hot' : ''}" data-hikoya><i>📖</i><b>Hikoya</b><small>${h.yangi ? '🆕 ' : ''}${h.n}/7 · ${esc(x.nom)}</small></button>
  <button class="t9t" data-albom><i>🃏</i><b>Albom</b><small>${al.n}/${al.jami} karta</small></button>
  <button class="t9t" data-ovozim><i>🎤</i><b>Ovozim</b><small>${oy ? 'oxirgi: ' + sana2(oy.sana) : "o'qishimni yozay"}</small></button>
  <button class="t9t${vo ? ' hot' : ''}" data-vikt><i>👨‍👩‍👧</i><b>Viktorina</b><small>${vo ? 'oila bilan!' : '🔒 Sh–Ya'}</small></button></div>`;
}
function uyBind(b) {
  const q = (s, f) => { const el = $(s); if (el) el.onclick = f; };
  q('[data-olov]', () => olovOyna(b)); q('[data-maqsad]', () => mqOyna(b));
  q('[data-hikoya]', () => A.go('hikoya')); q('[data-albom]', () => A.go('albom')); q('[data-ovozim]', () => A.go('ovozim')); q('[data-vikt]', () => vkKirish());
  olqBind(b);
  if (mqTekshir(b)) setTimeout(() => { play('fanfar'); burst(b); toast('🎯 Maqsadingga yetding! Barakalla! 🏆'); }, 500);
}
/* missiya yakuni (stepYakun, kuniga bir marta): hikoya sahifasi + olov */
function missiya(b) { const r = { hk: hkMissiya(b), ol: olovMissiya(b) }; A.save(true); return r; }
function natijaHTML(b, r) {
  if (!r) return ''; let s = '';
  if (r.ol && r.ol.n) s += `<div class="note kn${r.ol.bos ? ' gold' : ''}">🔥 ${r.ol.bos ? `${r.ol.n} kun ketma-ket — yangi marra!` : `Olov: ${r.ol.n} kun ketma-ket`}</div>`;
  if (r.hk) s += `<div class="row"><button class="btn big alt hkbtn" data-hkn>📖 Hikoyaning ${r.hk.n}-sahifasi ochildi!</button></div>`;
  return s;
}
function natijaBind() { const x = $('[data-hkn]'); if (x) x.onclick = () => { HKP = null; A.go('hikoya'); }; }
function otaQator(b) {
  try { const o = olov(b), h = mqHolat(b), hk = hkSt(b), al = alHisob(b), oy = (b.ovozYoz || []).length;
    return `<div class="sm mut">🔥 olov ${o.n} kun${h.yoq ? '' : ` · 🎯 ${h.x.ic} ${h.v}/${h.m.n}${h.ok ? ' ✅' : ''}`} · 📖 «${esc(hkOf(hk.i).nom)}» ${hk.n}/7 · 🃏 ${al.n}/${al.jami}${oy ? ` · 🎤 ${oy} yozuv` : ''}</div>`; } catch (e) { return ''; }
}
addEventListener('hashchange', () => { const h = location.hash.slice(1); if (h !== 'viktorina' && VK) vkTozala(); if (h !== 'ovozim') { if (REC) { recTugat(true); REC = null; } ovTozala(); } if (h !== 'hikoya') HKP = null; });

const css = `.t9s{display:flex;gap:8px;margin:8px 0}.t9c{flex:1;min-width:0;position:relative;overflow:hidden;display:flex;align-items:center;justify-content:center;gap:5px;min-height:48px;border-radius:16px;border:1px solid var(--line);background:var(--card);color:var(--ink);font:inherit;font-size:1rem;padding:6px 10px;cursor:pointer;white-space:nowrap}
.t9c small{color:var(--mut);font-size:.8rem;overflow:hidden;text-overflow:ellipsis}.t9c i{position:absolute;left:0;bottom:0;height:4px;background:linear-gradient(90deg,#FFB020,#FF6B3D);border-radius:0 4px 0 0}.olc{flex:0 0 auto;min-width:92px}.olc.off{filter:grayscale(1);opacity:.75}.olc b{font-size:1.15rem}
.olc.xavf{box-shadow:inset 0 0 0 2px rgba(255,140,0,.6)}.mqc.ok{box-shadow:inset 0 0 0 2px rgba(46,158,68,.55)}.mqc.yangi{background:linear-gradient(135deg,rgba(255,176,32,.22),rgba(255,61,113,.14));border-color:rgba(255,176,32,.6)}
.t9g{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:8px 0}.t9t{position:relative;display:flex;flex-direction:column;align-items:flex-start;gap:1px;min-height:74px;padding:10px 12px;border-radius:18px;border:1px solid var(--line);background:linear-gradient(160deg,var(--card),rgba(127,127,127,.06));color:var(--ink);font:inherit;text-align:left;cursor:pointer;box-shadow:0 3px 0 var(--line)}
.t9t i{font-style:normal;font-size:1.6rem;line-height:1}.t9t b{font-size:1rem}.t9t small{color:var(--mut);font-size:.78rem;max-width:100%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.t9t.hot{border-color:rgba(255,176,32,.7);box-shadow:0 3px 0 rgba(255,140,0,.45)}
.t9t:active,.t9c:active{transform:translateY(2px)}[data-hikoya],[data-albom],[data-ovozim],[data-vikt],[data-maqsad]{position:relative}
.olh{display:flex;align-items:center;gap:12px}.olf{font-size:3.2rem;filter:drop-shadow(0 4px 10px rgba(255,120,0,.55));animation:olf 1.6s ease-in-out infinite alternate}.olf.off{filter:grayscale(1);animation:none}@keyframes olf{to{transform:scale(1.08) rotate(-3deg)}}
.olw{display:grid;grid-template-columns:repeat(7,1fr);gap:4px;margin:10px 0}.olk{display:flex;flex-direction:column;align-items:center;gap:2px;padding:6px 0;border-radius:12px;background:rgba(127,127,127,.1);font-size:.8rem}.olk span{font-size:1.1rem}.olk.ok{background:rgba(255,140,0,.18)}.olk.muz{background:rgba(86,204,242,.2)}.olk.bugun{outline:2px solid #FFB020}
.mqr{margin:8px 0}.mqh{display:flex;align-items:baseline;gap:6px;flex-wrap:wrap}.mqh small{color:var(--mut);margin-left:auto}.mqo{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;margin-top:4px}.mqo .btn{min-height:46px;padding:4px}
.mqbig{font-size:2.2rem;text-align:center;margin:6px 0}.mqbig small{font-size:1rem;color:var(--mut)}.mqbar,.albar{height:12px;border-radius:8px;background:var(--line);overflow:hidden}.mqbar i,.albar i{display:block;height:100%;background:linear-gradient(90deg,#43A047,#9CCC65)}
.mqtr{display:flex;justify-content:space-between;padding:4px 2px;border-bottom:1px solid var(--line);font-size:.9rem}
.alg{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}.alk{position:relative;overflow:hidden;display:flex;flex-direction:column;align-items:center;justify-content:flex-end;gap:2px;aspect-ratio:3/4;border-radius:14px;border:2px solid rgba(255,255,255,.18);background:#1B2333;color:#fff;font:inherit;padding:6px 4px;text-align:center;cursor:pointer;box-shadow:0 4px 10px rgba(0,0,0,.25)}
.alsc{position:absolute;inset:0;pointer-events:none}.alsc svg{width:100%;height:100%;display:block}.alsc *{animation:none!important}.alk::after{content:'';position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,0) 35%,rgba(0,0,0,.7));pointer-events:none}
.ale{position:relative;z-index:1;font-size:2rem;margin-bottom:auto;margin-top:12%;filter:drop-shadow(0 3px 6px rgba(0,0,0,.5))}.alk b{position:relative;z-index:1;font-size:.72rem;line-height:1.15;text-shadow:0 1px 3px #000}.alk small{position:relative;z-index:1;font-size:.68rem;opacity:.8}
.als{position:relative;z-index:1;font-style:normal;color:#FFD54F;font-size:.8rem;letter-spacing:1px}.als u{text-decoration:none;opacity:.45}.alk.s3{border-color:#FFD54F;box-shadow:0 0 0 1px #FFB300,0 4px 14px rgba(255,193,7,.45)}.alk.s2{border-color:rgba(176,190,197,.8)}
.alk.yop{background:repeating-linear-gradient(135deg,#2A3142 0 10px,#252B3A 10px 20px);cursor:default;justify-content:center}.alk.yop::after{display:none}.alk.yop .ale{margin:0 0 4px;opacity:.6}.alst{text-align:center;font-size:1.2rem}.alst .als{font-size:1.2rem}.alqi{margin-top:8px}
.hkb{border-radius:20px;overflow:hidden;background:#FFFDF6;color:#2B2117;box-shadow:0 8px 22px rgba(0,0,0,.28);margin:8px 0}.hkb.flip{animation:hkf .45s ease-out}@keyframes hkf{from{transform:perspective(900px) rotateY(-14deg);opacity:.4}to{transform:none;opacity:1}}
.hksc{position:relative;height:150px;overflow:hidden;background:linear-gradient(180deg,var(--a),var(--b))}.hkyer{position:absolute;left:-10%;right:-10%;bottom:-40px;height:84px;border-radius:50%;background:linear-gradient(180deg,var(--c),var(--d))}
.hkem{position:absolute;left:0;right:0;bottom:22px;display:flex;justify-content:center;gap:14px;font-size:3rem;filter:drop-shadow(0 6px 8px rgba(0,0,0,.3))}.hkem span{display:inline-block;animation:hkem 2.6s ease-in-out infinite alternate}@keyframes hkem{to{transform:translateY(-6px)}}
.hksc.tun i{position:absolute;width:3px;height:3px;border-radius:50%;background:#fff;box-shadow:0 0 6px #fff;animation:hkyu 2s ease-in-out infinite alternate}@keyframes hkyu{from{opacity:.25}to{opacity:1}}
.hkpg{padding:12px 16px 4px}.hkno{font-size:.8rem;font-weight:800;color:#9C7A4E;letter-spacing:.04em}.hktx{font-family:Georgia,'Times New Roman',serif;font-size:1.13rem;line-height:1.6;margin:6px 0 10px}.hktx::first-letter{font-size:1.9em;float:left;line-height:.9;margin:4px 6px 0 0;color:#B5651D}
.hkd{display:flex;justify-content:center;gap:6px;padding:0 0 12px}.hkd i{width:9px;height:9px;border-radius:50%;background:#E0D5C3}.hkd i.ok{background:#C9A36B}.hkd i.on{background:#B5651D;transform:scale(1.3)}
.hknav{display:grid;grid-template-columns:1fr auto 1fr;gap:6px}.hknav .btn[disabled]{opacity:.4}.hkj .btn{display:block;width:100%;margin:6px 0;text-align:left}
@media (prefers-reduced-motion:reduce){.hkem span,.hksc.tun i,.olf,.hkb.flip{animation:none}}
.olqk{display:flex;align-items:center;gap:8px;background:linear-gradient(135deg,rgba(67,160,71,.18),rgba(30,136,229,.12));border:1px solid rgba(67,160,71,.5);border-radius:16px;padding:8px 10px;margin:6px 0}.olqa{font-size:1.8rem}.olqt{flex:1;min-width:0;display:flex;flex-direction:column;font-size:.9rem}.olqt span{font-weight:700}
.olqg{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:8px 0}.olqg .btn{min-height:52px;font-size:.95rem}.esolq{min-width:40px;min-height:40px;padding:2px 8px;font-size:1.1rem}.esolq[disabled]{opacity:.45}
.vkhero{display:flex;gap:12px;align-items:center}.vkh{font-size:2.6rem}.vkp{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin:6px 0 10px}.vko{display:flex;align-items:center;gap:6px;padding:8px 10px;border:1px solid var(--line);border-radius:14px;min-height:48px}.vko span{font-size:1.4rem}.vko input{width:20px;height:20px}
.vkr .btn{flex:1}.vknav{text-align:center;padding:24px 8px}.vkav{font-size:4.2rem;animation:olf 1.2s ease-in-out infinite alternate}.vkt{height:10px;border-radius:6px;background:var(--line);overflow:hidden;margin:4px 0 8px}.vkt i{display:block;height:100%;width:100%;background:#E53935;transition:width .12s linear}.vkt i.tez{background:#43A047}
.vkj{padding:6px 12px}.vkjr{display:flex;align-items:center;gap:8px;padding:6px 0;border-bottom:1px solid var(--line)}.vkjr:last-child{border-bottom:0}.vkjr.g{font-size:1.1rem}.vkn{width:20px;color:var(--mut);font-weight:800}
.vkpod{display:flex;justify-content:center;align-items:flex-end;gap:8px;margin:10px 0}.vkpd{display:flex;flex-direction:column;align-items:center;gap:2px;width:30%;border-radius:12px 12px 0 0;background:linear-gradient(180deg,#FFE082,#FFB300);color:#3E2723;padding:6px 4px}.vkpd span{font-size:1.8rem}.vkpd i{font-style:normal;font-weight:900}.vkpd u{text-decoration:none;font-size:1.4rem;font-weight:900}
.vkpd.p1{order:2;min-height:150px}.vkpd.p2{order:1;min-height:120px;background:linear-gradient(180deg,#ECEFF1,#B0BEC5)}.vkpd.p3{order:3;min-height:100px;background:linear-gradient(180deg,#FFCCBC,#D7A07A)}
.ovtab .btn{flex:1}.ovtx{font-size:1.25rem;line-height:1.7;margin:6px 0 2px}.ovtx.arab{font-size:1.6rem;line-height:2.1;font-family:'Amiri','Scheherazade New','Noto Naskh Arabic',serif}
.ovrec{display:flex;flex-direction:column;align-items:center;gap:8px;text-align:center}.ovmic{position:relative;width:104px;height:104px;border-radius:50%;border:0;background:radial-gradient(circle at 35% 30%,#FF8A80,#D32F2F 60%,#8E0000);box-shadow:0 8px 20px rgba(211,47,47,.45),inset 0 -4px 8px rgba(0,0,0,.3);display:flex;align-items:center;justify-content:center;cursor:pointer}
.ovmic span{font-size:2.8rem;filter:drop-shadow(0 2px 3px rgba(0,0,0,.4))}.ovmic.on{--l:0;box-shadow:0 0 0 calc(6px + var(--l) * 26px) rgba(211,47,47,.25),0 8px 20px rgba(211,47,47,.45);transition:box-shadow .1s}.ovtm{font-size:1.6rem;font-weight:800}
.ovrv{width:100%;display:flex;flex-direction:column;gap:8px}.ovrv audio,.ovl audio{width:100%}.ovc{display:grid;grid-template-columns:1fr auto 1fr;gap:6px;align-items:center;text-align:center}.ovc>div{display:flex;flex-direction:column;gap:2px}.ovc b{font-size:1.3rem}.ovc span{font-size:.8rem;color:var(--mut)}.ovar{font-size:1.4rem}
.ovli{display:flex;align-items:center;gap:8px;padding:6px 0;border-bottom:1px solid var(--line);flex-wrap:wrap}.ovli:last-child{border-bottom:0}`;
if (typeof document !== 'undefined') { const st = document.createElement('style'); st.textContent = css; document.head.appendChild(st); }
A.t91 = { holatHTML, tilesHTML, uyBind, missiya, natijaHTML, natijaBind, otaQator };
A.olov = { hisob: olov, missiya: olovMissiya, oyna: olovOyna, BOS: OLOV_BOS };
A.maqsad = { holat: mqHolat, tekshir: mqTekshir, tanla: mqTanla, oyna: mqOyna, MQ };
A.albom = { st: alSt, javob: alJavob, hisob: alHisob, yulduz: alYulduz, keyin: alKeyin, screen: albomScreen, karta: alKarta };
A.hikoya = { st: hkSt, missiya: hkMissiya, screen: b => hikoyaScreen(b), HK, matnlar: hkMatnlar, of: hkOf };
A.olqish = { OLQ, mumkin: olqMumkin, yubor: olqYubor, bulut: olqBulut, qabul: olqQabul, tanla: olqTanla, kelgan: olqKelgan, st: olqSt };
A.viktorina = { screen: vkScreen, ochiq: vkOchiq, kirish: vkKirish, item: vkItem, holat: () => VK, VAQT: VK_VAQT };
A.ovozim = { screen: ovScreen, matn: ovMatn, solishtir: ovSolishtir, royxat: ovRoyxat, idbGet, idbPut, holat: () => REC, til: t => { OVTIL = t; } };
})(typeof window !== 'undefined' ? window : globalThis);
</script>
