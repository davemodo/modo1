#!/usr/bin/env python3
"""Write ANIMATED B-roll mockups as self-contained HTML exposing window.renderAt(t).
capture.js drives these frame-by-frame via Playwright for deterministic motion:
 - m1_freeze : blinking caret on a blank doc
 - m2_record : live waveform + counting timer + transcript typing in
 - m3_ai     : prompt types in, then a thinking indicator
 - m4_steps  : numbered checklist builds in item-by-item
A subtle push-in (scale ramp) is baked into renderAt so no ffmpeg zoom is needed."""
import pathlib
ROOT = pathlib.Path(__file__).parent.parent   # project root (mockups/ -> reel-pipeline/)
FONTS = ROOT / "fonts"
OUT = ROOT / "build" / "broll_anim"; OUT.mkdir(parents=True, exist_ok=True)
ACCENT = "#f5a623"

def ff(file, w, style="normal"):
    return (f"@font-face{{font-family:'Mont';src:url('file://{FONTS/file}') format('woff2');"
            f"font-weight:{w};font-style:{style};}}")
CSS = f"""
{ff('montserrat-latin-500-normal.woff2',500)}{ff('montserrat-latin-600-normal.woff2',600)}
{ff('montserrat-latin-700-normal.woff2',700)}{ff('montserrat-latin-800-normal.woff2',800)}
*{{margin:0;padding:0;box-sizing:border-box;font-family:'Mont',sans-serif;-webkit-font-smoothing:antialiased}}
html,body{{width:720px;height:1280px;overflow:hidden;background:#08080a}}
.stage{{position:relative;width:720px;height:1280px;transform-origin:50% 46%;
 background:radial-gradient(120% 90% at 50% 42%, rgba(245,166,35,.22) 0%, rgba(245,166,35,.06) 34%, rgba(8,8,10,0) 62%), #08080a}}
.card{{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);background:#141417;
 border:1px solid rgba(255,255,255,.08);border-radius:26px;overflow:hidden;
 box-shadow:0 0 0 1px rgba(245,166,35,.10),0 30px 80px rgba(0,0,0,.6),0 0 90px rgba(245,166,35,.18)}}
.bar{{height:52px;display:flex;align-items:center;gap:8px;padding:0 18px;background:#1b1b1f;border-bottom:1px solid rgba(255,255,255,.06)}}
.dot{{width:11px;height:11px;border-radius:50%}}
.muted{{color:#8a8a92}}.white{{color:#f4f4f6}}.amber{{color:{ACCENT}}}
"""
PUSH = "var s=document.querySelector('.stage');s.style.transform='scale('+(1+0.006*t).toFixed(4)+')';"

def page(body, js):
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head>"
            f"<body><div class='stage'>{body}</div>"
            f"<script>window.renderAt=function(t){{{PUSH}{js}}};window.renderAt(0);</script></body></html>")

# ---- m1 freeze ----
m1 = page(
 f"""<div class='card' style='width:560px;height:520px'>
   <div class='bar'><div class='dot' style='background:#ff5f57'></div><div class='dot' style='background:#febc2e'></div><div class='dot' style='background:#28c840'></div>
     <div class='muted' style='margin-left:14px;font-size:15px;font-weight:600'>My Process — Untitled</div></div>
   <div style='padding:40px 44px'>
     <div class='muted' style='font-size:16px;font-weight:600'>Document how you do it:</div>
     <div style='margin-top:28px;display:flex;align-items:center;gap:2px'>
       <span id='car' style='display:inline-block;width:3px;height:26px;background:{ACCENT}'></span></div>
     <div style='margin-top:64px;display:flex;flex-direction:column;gap:20px;opacity:.15'>
       <div style='height:12px;width:70%;background:#fff;border-radius:6px'></div>
       <div style='height:12px;width:52%;background:#fff;border-radius:6px'></div>
       <div style='height:12px;width:60%;background:#fff;border-radius:6px'></div></div></div></div>""",
 "document.getElementById('car').style.opacity=(Math.floor(t*1.6)%2)?0.12:1;")

# ---- m2 record ----
BARS = "".join(f"<span class='wb' style='width:6px;border-radius:3px;background:{ACCENT}'></span>" for _ in range(22))
m2 = page(
 f"""<div class='card' style='width:360px;height:720px;border-radius:44px'>
   <div style='padding:28px 26px 0;display:flex;justify-content:space-between;align-items:center'>
     <div class='white' style='font-weight:700;font-size:18px'>Voice Memo</div>
     <div style='display:flex;align-items:center;gap:8px'><span id='rd' class='dot' style='background:#ff3b30;width:9px;height:9px'></span><span class='muted' style='font-size:14px;font-weight:600'>REC</span></div></div>
   <div class='wave' style='display:flex;align-items:center;justify-content:center;gap:5px;height:170px;margin-top:130px'>{BARS}</div>
   <div id='tm' class='white' style='text-align:center;font-size:40px;font-weight:700;margin-top:22px;letter-spacing:1px'>0:00</div>
   <div style='margin:64px 26px 0;padding:16px 18px;background:#0f0f12;border-radius:16px;border:1px solid rgba(255,255,255,.06);min-height:96px'>
     <div class='muted' style='font-size:13px;font-weight:600;margin-bottom:8px'>Live transcript</div>
     <div id='tr' class='white' style='font-size:16px;line-height:1.5'></div></div>
   <div style='display:flex;justify-content:center;margin-top:40px'><div id='rb' style='width:78px;height:78px;border-radius:50%;background:#ff3b30'></div></div></div>""",
 """var bars=document.querySelectorAll('.wb');
    for(var i=0;i<bars.length;i++){var ph=i*0.7;var h=40+55*Math.abs(Math.sin(t*3.2+ph))+30*Math.abs(Math.sin(t*7.1+ph*1.7));bars[i].style.height=Math.min(150,h).toFixed(0)+'px';}
    var sec=Math.min(12,Math.floor(t));document.getElementById('tm').textContent='0:'+(sec<10?'0':'')+sec;
    var full="\\u201cFirst I do this, because\\u2026 then I check this\\u2026\\u201d";var n=Math.min(full.length,Math.floor(Math.max(0,t-0.6)*13));
    document.getElementById('tr').textContent=full.slice(0,n)+((Math.floor(t*1.8)%2)&&n<full.length?'|':'');
    var pulse=0.5+0.5*Math.abs(Math.sin(t*3.5));document.getElementById('rb').style.boxShadow='0 0 0 '+(6+8*pulse).toFixed(0)+'px rgba(255,59,48,.18)';
    document.getElementById('rd').style.opacity=(Math.floor(t*2)%2)?0.3:1;""")

# ---- m3 ai ----
m3 = page(
 f"""<div class='card' style='width:580px;height:560px'>
   <div class='bar'><div class='amber' style='font-weight:800;font-size:16px'>&#10022; AI Assistant</div></div>
   <div style='padding:30px 30px;display:flex;flex-direction:column;gap:20px'>
     <div style='align-self:flex-start;max-width:82%;background:#1e1e23;border:1px solid rgba(255,255,255,.06);border-radius:16px 16px 16px 4px;padding:16px 18px'>
       <div class='muted' style='font-size:13px;font-weight:700;margin-bottom:6px'>Pasted recording (transcript)</div>
       <div class='white' style='font-size:15px;line-height:1.55;opacity:.85'>&#8220;Okay so first I open the file, then I check the numbers, then I send it to&#8230;&#8221;</div></div>
     <div id='ub' style='align-self:flex-end;max-width:80%;background:{ACCENT};color:#141417;border-radius:16px 16px 4px 16px;padding:16px 18px;font-weight:700;font-size:17px;min-height:20px'></div>
     <div id='think' style='align-self:flex-start;display:flex;gap:8px;align-items:center;opacity:0'>
       <span class='td' style='width:9px;height:9px;border-radius:50%;background:#8a8a92'></span>
       <span class='td' style='width:9px;height:9px;border-radius:50%;background:#8a8a92'></span>
       <span class='td' style='width:9px;height:9px;border-radius:50%;background:#8a8a92'></span></div></div></div>""",
 """var full="Turn this into clear, numbered steps.";var n=Math.min(full.length,Math.floor(t*17));
    document.getElementById('ub').textContent=full.slice(0,n)+((Math.floor(t*1.8)%2)&&n<full.length?'|':'');
    var th=document.getElementById('think');th.style.opacity=(n>=full.length)?1:0;
    var d=document.querySelectorAll('.td');for(var i=0;i<d.length;i++){d[i].style.transform='translateY('+(-4*Math.max(0,Math.sin(t*6-i*0.9))).toFixed(1)+'px)';}""")

# ---- m4 steps ----
STEPS = ["Open the file and pull the latest data","Check the key numbers for anything off",
         "Flag exceptions and note the reason","Format and package the summary","Send it out and log it as done"]
rows = "".join(f"""<div class='row' data-i='{i}' style='display:flex;align-items:center;gap:16px;padding:15px 0;border-bottom:1px solid rgba(255,255,255,.05);opacity:0;transform:translateY(10px)'>
  <div style='min-width:34px;height:34px;border-radius:10px;background:rgba(245,166,35,.16);color:{ACCENT};font-weight:800;display:flex;align-items:center;justify-content:center;font-size:16px'>{i+1}</div>
  <div class='white' style='font-size:16px;font-weight:500;flex:1'>{t}</div>
  <div class='ck' style='color:{ACCENT};font-size:18px;opacity:0'>&#10003;</div></div>""" for i,t in enumerate(STEPS))
m4 = page(
 f"""<div class='card' style='width:600px;height:620px'>
   <div class='bar'><div class='amber' style='font-weight:800;font-size:16px'>&#10022; AI Assistant</div><div class='muted' style='margin-left:10px;font-size:14px;font-weight:600'>Steps generated</div></div>
   <div style='padding:24px 34px'><div class='white' style='font-weight:800;font-size:24px'>Your Process</div>
     <div style='margin-top:8px'>{rows}</div></div></div>""",
 """var rows=document.querySelectorAll('.row');for(var i=0;i<rows.length;i++){var st=0.35+i*0.55;var p=Math.max(0,Math.min(1,(t-st)/0.35));
    rows[i].style.opacity=p;rows[i].style.transform='translateY('+(10*(1-p)).toFixed(1)+'px)';
    rows[i].querySelector('.ck').style.opacity=(t>st+0.4)?1:0;}""")

for name, html in {"m1_freeze":m1,"m2_record":m2,"m3_ai":m3,"m4_steps":m4}.items():
    (OUT / f"{name}.html").write_text(html); print("wrote", name)
