// Soxta Auth: uid = email'dan; holat localStorage'da (haqiqiy SDK ham IndexedDB'da saqlaydi)
let cbs = [];
const cur = () => { try { return JSON.parse(localStorage.getItem('fake_user') || 'null'); } catch (e) { return null; } };
const fire = () => cbs.forEach(f => f(cur()));
export function getAuth() { return {}; }
export function onAuthStateChanged(a, f) { cbs.push(f); setTimeout(() => f(cur()), 10); return () => { cbs = cbs.filter(x => x !== f); }; }
async function login(email, p) { if (!email || !p || p.length < 6) throw { code: 'auth/invalid-credential' }; const u = { uid: 'U_' + email.replace(/\W/g, ''), email }; localStorage.setItem('fake_user', JSON.stringify(u)); fire(); return { user: u }; }
export const signInWithEmailAndPassword = (a, e, p) => login(e, p);
export const createUserWithEmailAndPassword = (a, e, p) => login(e, p);
export class GoogleAuthProvider {}
export const signInWithPopup = () => login('google@test.uz', 'xxxxxx');
export async function sendPasswordResetEmail() {}
export async function signOut() { localStorage.removeItem('fake_user'); fire(); }
