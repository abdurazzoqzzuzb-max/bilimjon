// Soxta Firestore: hamma telefonlar uchun umumiy ombor Python tomonida (window.__fs)
export function getFirestore() { return {}; }
const P = a => a.join('/');
export function doc(db, ...p) { return { path: P(p), id: p[p.length - 1] }; }
export function collection(db, ...p) { return { path: P(p), col: true }; }
export function where(f, op, v) { return { f, op, v }; }
export function query(c, ...w) { return { path: c.path, col: true, w }; }
export function arrayUnion(...v) { return { __au: v }; }
const snapDoc = (path, d) => ({ id: path.split('/').pop(), exists: () => d != null, data: () => d == null ? undefined : JSON.parse(JSON.stringify(d)), metadata: { hasPendingWrites: false } });
async function call(...a) { const r = await window.__fs(JSON.stringify(a)); return r == null ? null : JSON.parse(r); }
export async function getDoc(ref) { return snapDoc(ref.path, await call('get', ref.path)); }
export async function setDoc(ref, data, opt) { if (window.__fsFail) throw { code: 'unavailable' }; await call('set', ref.path, data, !!(opt && opt.merge)); }
export async function deleteDoc(ref) { await call('del', ref.path); }
function filt(rows, w) { return rows.filter(([p, d]) => (w || []).every(c => c.op === '>=' ? d[c.f] >= c.v : c.op === '==' ? d[c.f] === c.v : true)); }
export async function getDocs(q) { const rows = filt(await call('list', q.path), q.w); return { size: rows.length, forEach: f => rows.forEach(([p, d]) => f(snapDoc(p, d))) }; }
export function onSnapshot(ref, cb, err) {
  let prev = null, stop = false;
  const run = async () => { if (stop) return; try {
    if (!ref.col) { const d = await call('get', ref.path), j = JSON.stringify(d); if (j !== prev) { prev = j; cb(snapDoc(ref.path, d)); } }
    else { const rows = await call('list', ref.path), cur = {}; rows.forEach(([p, d]) => cur[p] = JSON.stringify(d)); const old = prev ? JSON.parse(prev) : {}, ch = [];
      Object.keys(cur).forEach(p => { if (!(p in old)) ch.push({ type: 'added', doc: snapDoc(p, JSON.parse(cur[p])) }); else if (old[p] !== cur[p]) ch.push({ type: 'modified', doc: snapDoc(p, JSON.parse(cur[p])) }); });
      Object.keys(old).forEach(p => { if (!(p in cur)) ch.push({ type: 'removed', doc: snapDoc(p, null) }); });
      const nj = JSON.stringify(cur); if (nj !== prev) { prev = nj; cb({ size: rows.length, docChanges: () => ch, forEach: f => rows.forEach(([p, d]) => f(snapDoc(p, d))) }); } }
  } catch (e) { err && err(e); } setTimeout(run, 300); };
  run(); return () => { stop = true; };
}
