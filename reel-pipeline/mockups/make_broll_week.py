#!/usr/bin/env python3
"""Animated B-roll mockups for the "one idea -> a week of content" reel.
 w1_voice   : AI learns your voice from pasted posts (voice-profile bars fill)
 w2_idea    : one-line idea + the prompt typing in
 w3_week    : Mon-Fri post cards generate in, staggered
 w4_schedule: a weekly scheduler fills Mon-Fri, staggered
Each exposes window.renderAt(t); capture.js drives frames deterministically."""
import pathlib
ROOT = pathlib.Path(__file__).parent.parent   # project root (mockups/ -> reel-pipeline/)
FONTS = ROOT/"fonts"
OUT = ROOT/"build"/"broll_anim"; OUT.mkdir(parents=True, exist_ok=True)
ACCENT="#f5a623"
def ff(f,w,s="normal"): return f"@font-face{{font-family:'Mont';src:url('file://{FONTS/f}') format('woff2');font-weight:{w};font-style:{s};}}"
CSS=f"""{ff('montserrat-latin-500-normal.woff2',500)}{ff('montserrat-latin-600-normal.woff2',600)}{ff('montserrat-latin-700-normal.woff2',700)}{ff('montserrat-latin-800-normal.woff2',800)}
*{{margin:0;padding:0;box-sizing:border-box;font-family:'Mont',sans-serif;-webkit-font-smoothing:antialiased}}
html,body{{width:720px;height:1280px;overflow:hidden;background:#08080a}}
.stage{{position:relative;width:720px;height:1280px;transform-origin:50% 46%;background:radial-gradient(120% 90% at 50% 42%, rgba(245,166,35,.22) 0%, rgba(245,166,35,.06) 34%, rgba(8,8,10,0) 62%), #08080a}}
.card{{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);background:#141417;border:1px solid rgba(255,255,255,.08);border-radius:26px;overflow:hidden;box-shadow:0 0 0 1px rgba(245,166,35,.10),0 30px 80px rgba(0,0,0,.6),0 0 90px rgba(245,166,35,.18)}}
.bar{{height:52px;display:flex;align-items:center;gap:8px;padding:0 18px;background:#1b1b1f;border-bottom:1px solid rgba(255,255,255,.06)}}
.muted{{color:#8a8a92}}.white{{color:#f4f4f6}}.amber{{color:{ACCENT}}}"""
PUSH="var s=document.querySelector('.stage');s.style.transform='scale('+(1+0.006*t).toFixed(4)+')';"
def page(body,js): return f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body><div class='stage'>{body}</div><script>window.renderAt=function(t){{{PUSH}{js}}};window.renderAt(0);</script></body></html>"

# w1_voice
traits=[("Tone","warm & direct"),("Rhythm","short, punchy lines"),("Vocabulary","the words you use"),("Structure","hook - value - CTA")]
trows="".join(f"""<div class='tr' data-i='{i}' style='margin:14px 0'>
  <div style='display:flex;justify-content:space-between;font-size:15px;margin-bottom:7px'><span class='white' style='font-weight:600'>{a}</span><span class='muted'>{b}</span></div>
  <div style='height:9px;background:#0f0f12;border-radius:6px;overflow:hidden'><div class='fill' style='height:100%;width:0;background:{ACCENT};border-radius:6px'></div></div></div>""" for i,(a,b) in enumerate(traits))
w1=page(f"""<div class='card' style='width:600px;height:640px'>
  <div class='bar'><div class='amber' style='font-weight:800;font-size:16px'>&#10022; AI Assistant</div><div class='muted' style='margin-left:10px;font-size:14px;font-weight:600'>Analyzing 5 posts</div></div>
  <div style='padding:26px 34px'>
    <div id='posts' style='display:flex;gap:8px;margin-bottom:20px'></div>
    <div class='white' style='font-weight:800;font-size:22px;margin-bottom:6px'>Your Brand Voice</div>{trows}</div></div>""",
 """var pw=document.getElementById('posts');if(!pw.dataset.done){for(var j=0;j<5;j++){var d=document.createElement('div');d.className='pc';d.style.cssText='flex:1;height:54px;background:#1e1e23;border:1px solid rgba(255,255,255,.06);border-radius:10px;opacity:0';pw.appendChild(d);}pw.dataset.done=1;}
    var pcs=document.querySelectorAll('.pc');for(var j=0;j<pcs.length;j++){pcs[j].style.opacity=(t>0.15+j*0.14)?1:0;}
    var tr=document.querySelectorAll('.tr');for(var i=0;i<tr.length;i++){var st=1.4+i*0.5;var p=Math.max(0,Math.min(1,(t-st)/0.7));tr[i].querySelector('.fill').style.width=(p*100).toFixed(0)+'%';}""")

# w2_idea
w2=page(f"""<div class='card' style='width:600px;height:420px'>
  <div class='bar'><div class='amber' style='font-weight:800;font-size:16px'>&#10022; AI Assistant</div></div>
  <div style='padding:34px 34px'>
    <div class='muted' style='font-size:14px;font-weight:700;letter-spacing:.4px;margin-bottom:10px'>YOUR ONE IDEA</div>
    <div style='background:#0f0f12;border:1px solid rgba(255,255,255,.08);border-radius:14px;padding:18px 20px;min-height:60px'>
      <span id='idea' class='white' style='font-size:20px;font-weight:600'></span></div>
    <div id='cmd' style='margin-top:22px;align-self:flex-start;background:{ACCENT};color:#141417;border-radius:14px;padding:16px 18px;font-weight:700;font-size:17px;opacity:0'></div></div></div>""",
 """var idea="Why now is the smartest time to make your move.";var ni=Math.min(idea.length,Math.floor(t*20));
    document.getElementById('idea').textContent=idea.slice(0,ni)+((Math.floor(t*1.8)%2)&&ni<idea.length?'|':'');
    var cmd="Turn this into a week of posts, in my voice.";var t2=t-(idea.length/20)-0.4;var el=document.getElementById('cmd');
    if(t2>0){el.style.opacity=1;var nc=Math.min(cmd.length,Math.floor(t2*22));el.textContent=cmd.slice(0,nc)+((Math.floor(t*1.8)%2)&&nc<cmd.length?'|':'');}else{el.style.opacity=0;}""")

# w3_week
days=["MON","TUE","WED","THU","FRI"]
dcards="".join(f"""<div class='dc' data-i='{i}' style='opacity:0;transform:translateY(12px);background:#1a1a1f;border:1px solid rgba(255,255,255,.07);border-radius:14px;padding:14px 16px;display:flex;flex-direction:column;gap:9px'>
  <div style='display:flex;justify-content:space-between;align-items:center'><span class='amber' style='font-weight:800;font-size:13px;letter-spacing:1px'>{d}</span><span style='width:8px;height:8px;border-radius:50%;background:{ACCENT}'></span></div>
  <div style='height:11px;width:82%;background:rgba(255,255,255,.22);border-radius:5px'></div>
  <div style='height:9px;width:64%;background:rgba(255,255,255,.12);border-radius:5px'></div></div>""" for i,d in enumerate(days))
w3=page(f"""<div class='card' style='width:610px;height:660px'>
  <div class='bar'><div class='amber' style='font-weight:800;font-size:16px'>&#10022; AI Assistant</div><div class='muted' style='margin-left:10px;font-size:14px;font-weight:600'>Generating this week</div></div>
  <div style='padding:22px 30px;display:flex;flex-direction:column;gap:12px'>{dcards}</div></div>""",
 """var dc=document.querySelectorAll('.dc');for(var i=0;i<dc.length;i++){var st=0.4+i*0.6;var p=Math.max(0,Math.min(1,(t-st)/0.4));dc[i].style.opacity=p;dc[i].style.transform='translateY('+(12*(1-p)).toFixed(1)+'px)';}""")

# w4_schedule
scols="".join(f"""<div style='flex:1;display:flex;flex-direction:column;gap:10px'>
  <div class='amber' style='text-align:center;font-weight:800;font-size:13px;letter-spacing:1px'>{d}</div>
  <div class='slot' data-i='{i}' style='height:120px;background:#131317;border:1px dashed rgba(255,255,255,.10);border-radius:12px;position:relative'>
    <div class='chip' style='position:absolute;left:8px;right:8px;top:8px;height:104px;background:linear-gradient(180deg,rgba(245,166,35,.9),rgba(245,166,35,.6));border-radius:9px;opacity:0;transform:scale(.9)'></div></div></div>""" for i,d in enumerate(days))
w4=page(f"""<div class='card' style='width:640px;height:420px'>
  <div class='bar'><div class='white' style='font-weight:800;font-size:16px'>&#128197; Content Scheduler</div><div class='muted' style='margin-left:10px;font-size:14px;font-weight:600'>This week</div></div>
  <div style='padding:24px 22px;display:flex;gap:10px'>{scols}</div></div>""",
 """var ch=document.querySelectorAll('.chip');for(var i=0;i<ch.length;i++){var st=0.5+i*0.5;var p=Math.max(0,Math.min(1,(t-st)/0.35));ch[i].style.opacity=p;ch[i].style.transform='scale('+(0.9+0.1*p).toFixed(3)+')';}""")

for n,h in {"w1_voice":w1,"w2_idea":w2,"w3_week":w3,"w4_schedule":w4}.items():
    (OUT/f"{n}.html").write_text(h); print("wrote", n)
