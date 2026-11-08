"""Bilimjon 0.7.8 — 👆 ekran kattalashmaydi (u: «ekranni 2 marta bossa yaqinlashib qolyapti — har doim bir xil tursin»):
viewport maximum-scale=1 + user-scalable=no, html touch-action (ikki marta bosish zoom'i yo'q), iPhone gesture* to'xtatiladi,
textarea ≥ 16px (iPhone fokusda kattalashtirmasin); tez ketma-ket bosishlar (o'yinlar) yo'qolmaydi.
Ishga tushirish: python3 sinov/v078/sinov_zoom.py"""
import os, sys, time, subprocess
from playwright.sync_api import sync_playwright
D = os.path.dirname(os.path.abspath(__file__)); SITE = os.path.abspath(os.path.join(D, '..', '..'))
PORT = 8809; URL = f'http://localhost:{PORT}/'
srv = subprocess.Popen([sys.executable, '-m', 'http.server', str(PORT)], cwd=SITE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); time.sleep(1)
ERR = []; PE = []
def ok(c, m): print(('✅ ' if c else '❌ ') + m); (None if c else ERR.append(m))
try:
  with sync_playwright() as p:
    br = p.chromium.launch(); ctx = br.new_context(viewport={'width': 390, 'height': 844}, is_mobile=True, has_touch=True, service_workers='block')
    pg = ctx.new_page(); pg.on('pageerror', lambda e: PE.append(str(e))); ev = pg.evaluate
    pg.goto(URL + '?tez=1'); pg.wait_for_timeout(600)
    vp = ev("document.querySelector('meta[name=viewport]').content")
    ok('maximum-scale=1' in vp and 'user-scalable=no' in vp and 'viewport-fit=cover' in vp, f"viewport: {vp}")
    ta = ev("getComputedStyle(document.documentElement).touchAction")
    ok(ta in ('pan-x pan-y', 'manipulation'), f"html touch-action = {ta} (ikki marta bosish zoom'i yo'q)")
    ok(ev("(()=>{const e=new Event('gesturestart',{cancelable:true}); document.dispatchEvent(e); return e.defaultPrevented})()"), "iPhone gesturestart (chimchilash) to'xtatiladi")
    ok(ev("(()=>{const e=new Event('gesturechange',{cancelable:true}); document.body.dispatchEvent(new Event('x')); document.dispatchEvent(e); return e.defaultPrevented})()"), "gesturechange ham")
    # oila → ota-ona paneli → reyting: textarea shrifti
    pg.fill('#on', 'Sinov oila'); pg.fill('#p1', '1234'); pg.fill('#p2', '1234'); pg.click('#go'); pg.wait_for_timeout(300)
    ev("BJ.A.newBola({laqab:'Aziz',daraja:'g1',avatar:'🦊',dunyo:'garaj'}); BJ.A.otaOk={rol:'admin',t:Date.now()}; BJ.A.save(true)")
    pg.goto(URL + '?tez=1#ota-reyting'); pg.wait_for_timeout(500)
    fs = ev("Math.min(...[...document.querySelectorAll('input.inp,textarea.inp,select.inp')].map(x=>parseFloat(getComputedStyle(x).fontSize)))")
    ok(fs >= 16, f"Hamma kiritish maydonlari ≥ 16px (eng kichigi {fs}px) — iPhone fokusda kattalashtirmaydi")
    # tez ketma-ket bosish (ikki marta bosish) — ikkala bosish ham yetib boradi
    ev("window.__n=0; const b=document.createElement('button'); b.id='tb'; b.textContent='T'; b.style.cssText='position:fixed;left:20px;top:200px;width:120px;height:60px;z-index:999'; b.onclick=()=>window.__n++; document.body.appendChild(b)")
    pg.tap('#tb'); pg.tap('#tb'); pg.wait_for_timeout(400)
    ok(ev("window.__n") == 2, f"Tez 2 marta bosish — 2 ta bosish yetib bordi ({ev('window.__n')})")
    ok(ev("visualViewport ? visualViewport.scale : 1") == 1, "Ekran masshtabi 1 (kattalashmagan)")
    ok(ev("document.documentElement.scrollWidth<=390"), "390 px — gorizontal siljish yo'q")
    ok(not PE, f"JS xato yo'q {PE[:3]}")
finally:
  srv.terminate()
print('\nJAMI XATO:', len(ERR)); [print(' -', e) for e in ERR]; sys.exit(1 if ERR else 0)
