#!/usr/bin/env python3
"""Original animated B-roll + intro spark + dummy talking-head for the recreated
'free AI study tool' reel. Visual language derived from the REFERENCE reel only:
light/white backgrounds, clean colourful app-card mockups (varied accents, no
single brand colour), neutral studio head. Original content — not the reference's
screenshots/branding. Each exposes window.renderAt(t)."""
import pathlib
ROOT = pathlib.Path(__file__).parent.parent   # project root (mockups/ -> reel-pipeline/)
FONTS = ROOT/"fonts"
OUTH = ROOT/"build"/"broll_anim"; OUTH.mkdir(parents=True, exist_ok=True)

BG="#FAF9F6"; CARD="#FFFFFF"; INK="#161512"; MUT="#6E6C66"; LINE="#E9E6DE"
BLU="#2F6BFF"; GRN="#17A25C"; COR="#F0603A"; VIO="#7A5AF0"   # generic app-UI accents

def ff(f,w,s="normal"): return f"@font-face{{font-family:'Inter';src:url('file://{FONTS/f}') format('woff2');font-weight:{w};font-style:{s};}}"
CSS=f"""{ff('inter-latin-400-normal.woff2',400)}{ff('inter-latin-500-normal.woff2',500)}{ff('inter-latin-600-normal.woff2',600)}
*{{margin:0;padding:0;box-sizing:border-box;font-family:'Inter',sans-serif;-webkit-font-smoothing:antialiased}}
html,body{{width:720px;height:1280px;overflow:hidden;background:{BG}}}
.stage{{position:relative;width:720px;height:1280px;transform-origin:50% 46%;background:{BG}}}
.card{{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);background:{CARD};border:1px solid {LINE};border-radius:22px;overflow:hidden;box-shadow:0 24px 60px rgba(20,20,15,.10)}}
.bar{{height:52px;display:flex;align-items:center;gap:8px;padding:0 18px;border-bottom:1px solid {LINE}}}
.ink{{color:{INK}}}.mut{{color:{MUT}}}"""
PUSH="var s=document.querySelector('.stage');s.style.transform='scale('+(1+0.006*t).toFixed(4)+')';"
def page(body,js): return f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body><div class='stage'>{body}</div><script>window.renderAt=function(t){{{PUSH}{js}}};window.renderAt(0);</script></body></html>"

# spark (intro) — clean dark ink sparkle on white, with a soft grey ring
spark=page(f"""<svg style='position:absolute;left:50%;top:44%;transform:translate(-50%,-50%)' width='330' height='330' viewBox='0 0 200 200'>
  <circle id='ring' cx='100' cy='100' r='70' fill='none' stroke='{LINE}' stroke-width='3'/>
  <g id='st'><path d='M100 10 C108 60 140 92 190 100 C140 108 108 140 100 190 C92 140 60 108 10 100 C60 92 92 60 100 10 Z' fill='{INK}'/></g></svg>""",
 """var sc=Math.min(1,t/0.7),e=1-Math.pow(1-sc,3);var st=document.getElementById('st');
    st.setAttribute('transform','translate(100,100) scale('+e.toFixed(3)+') rotate('+(t*30)+') translate(-100,-100)');
    st.setAttribute('opacity',e.toFixed(2));var r=document.getElementById('ring');r.setAttribute('r',(70+14*Math.sin(t*3)).toFixed(1));""")

# m_notes (The Chaos) — light Notes window, scattered grey fragments + colour tags
frags="".join(f"<div class='fr' style='position:absolute;height:12px;border-radius:6px;background:#D9D6CE'></div>" for _ in range(9))
m_notes=page(f"""<div class='card' style='width:590px;height:540px'>
  <div class='bar'><span style='width:11px;height:11px;border-radius:50%;background:#FF5F57'></span><span style='width:11px;height:11px;border-radius:50%;background:#FEBC2E'></span><span style='width:11px;height:11px;border-radius:50%;background:#28C840'></span><div class='mut' style='margin-left:10px;font-size:15px;font-weight:600'>Notes — a mess</div></div>
  <div id='cv' style='position:relative;height:470px'>{frags}
   <div class='tag' style='position:absolute;left:60px;top:300px;background:{BLU};color:#fff;font-size:13px;font-weight:600;padding:6px 12px;border-radius:20px'>lecture.pdf</div>
   <div class='tag' style='position:absolute;left:330px;top:360px;background:{COR};color:#fff;font-size:13px;font-weight:600;padding:6px 12px;border-radius:20px'>screenshot.png</div></div></div>""",
 """var fr=document.querySelectorAll('.fr');var W=[70,52,60,44,66,50,72,40,58];var X=[50,60,44,300,320,54,64,330,58];var Y=[70,110,150,80,120,210,250,210,300];var R=[-4,3,-2,5,-3,2,-5,4,-2];
    for(var i=0;i<fr.length;i++){var p=Math.max(0,Math.min(1,(t-0.15-i*0.12)/0.35));fr[i].style.width=(W[i]*3)+'px';fr[i].style.left=X[i]+'px';fr[i].style.top=Y[i]+'px';
    fr[i].style.opacity=p.toFixed(2);fr[i].style.transform='rotate('+(R[i]*p).toFixed(1)+'deg) translateY('+(10*(1-p)).toFixed(1)+'px)';}
    var tg=document.querySelectorAll('.tag');for(var j=0;j<tg.length;j++){tg[j].style.opacity=Math.max(0,Math.min(1,(t-1.4-j*0.3)/0.4)).toFixed(2);}""")

# m_ai (One Prompt) — light chat, blue user prompt bubble
m_ai=page(f"""<div class='card' style='width:590px;height:560px'>
  <div class='bar'><div class='ink' style='font-weight:700;font-size:16px'>&#10022; AI Tutor</div></div>
  <div style='padding:28px 30px;display:flex;flex-direction:column;gap:18px'>
   <div style='align-self:flex-start;max-width:82%;background:#F3F1EB;border-radius:16px 16px 16px 4px;padding:15px 17px'>
    <div class='mut' style='font-size:13px;font-weight:700;margin-bottom:6px'>Your notes (pasted)</div>
    <div class='ink' style='font-size:15px;line-height:1.5;opacity:.8'>&#8220;photosynthesis&#8230; mitochondria&#8230; the krebs cycle&#8230; ???&#8221;</div></div>
   <div id='ub' style='align-self:flex-end;max-width:80%;background:{BLU};color:#fff;border-radius:16px 16px 4px 16px;padding:15px 17px;font-weight:600;font-size:17px;min-height:20px'></div>
   <div id='think' style='align-self:flex-start;display:flex;gap:8px;opacity:0'><span class='td' style='width:9px;height:9px;border-radius:50%;background:#C7C4BC'></span><span class='td' style='width:9px;height:9px;border-radius:50%;background:#C7C4BC'></span><span class='td' style='width:9px;height:9px;border-radius:50%;background:#C7C4BC'></span></div></div></div>""",
 """var full="Turn my notes into a clean study guide.";var n=Math.min(full.length,Math.floor(Math.max(0,t-0.5)*20));
    document.getElementById('ub').textContent=full.slice(0,n)+((Math.floor(t*1.8)%2)&&n<full.length?'|':'');
    document.getElementById('think').style.opacity=(n>=full.length)?1:0;
    var d=document.querySelectorAll('.td');for(var i=0;i<d.length;i++){d[i].style.transform='translateY('+(-4*Math.max(0,Math.sin(t*6-i*0.9))).toFixed(1)+'px)';}""")

# m_guide (Perfect Guide) — white card, green number badges + checks
secs=["Overview","Key concepts","Worked examples","Summary","Practice quiz"]
rows="".join(f"""<div class='gr' style='display:flex;align-items:center;gap:14px;padding:14px 0;border-bottom:1px solid {LINE};opacity:0;transform:translateY(10px)'>
  <div style='min-width:30px;height:30px;border-radius:9px;background:rgba(23,162,92,.12);color:{GRN};font-weight:700;display:flex;align-items:center;justify-content:center;font-size:14px'>{i+1}</div>
  <div class='ink' style='font-size:16px;font-weight:500;flex:1'>{s}</div><div class='ck' style='color:{GRN};font-size:17px;opacity:0'>&#10003;</div></div>""" for i,s in enumerate(secs))
m_guide=page(f"""<div class='card' style='width:600px;height:600px'>
  <div class='bar'><div class='ink' style='font-weight:700;font-size:16px'>&#10022; AI Tutor</div><div class='mut' style='margin-left:10px;font-size:14px;font-weight:500'>Study guide ready</div></div>
  <div style='padding:24px 34px'><div class='ink' style='font-weight:700;font-size:23px'>Your Study Guide</div><div style='margin-top:6px'>{rows}</div></div></div>""",
 """var gr=document.querySelectorAll('.gr');for(var i=0;i<gr.length;i++){var st=0.35+i*0.5;var p=Math.max(0,Math.min(1,(t-st)/0.4));gr[i].style.opacity=p;gr[i].style.transform='translateY('+(10*(1-p)).toFixed(1)+'px)';gr[i].querySelector('.ck').style.opacity=(t>st+0.35)?1:0;}""")

# m_cards (Flashcards) — white card with violet top stripe, Q/A flip, light stack
m_cards=page(f"""<div style='position:absolute;left:50%;top:48%;transform:translate(-50%,-50%);width:420px;height:300px'>
  <div style='position:absolute;inset:0;transform:translate(26px,26px) rotate(6deg);background:#F1EEE7;border:1px solid {LINE};border-radius:20px'></div>
  <div style='position:absolute;inset:0;transform:translate(13px,13px) rotate(3deg);background:#F6F4EE;border:1px solid {LINE};border-radius:20px'></div>
  <div id='fc' style='position:absolute;inset:0;background:{CARD};border:1px solid {LINE};border-radius:20px;box-shadow:0 20px 50px rgba(20,20,15,.12);overflow:hidden;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:30px 34px;text-align:center'>
    <div style='position:absolute;top:0;left:0;right:0;height:8px;background:{VIO}'></div>
    <div id='fcl' style='color:{VIO};font-weight:700;font-size:14px;letter-spacing:2px;margin-bottom:14px'>Q</div>
    <div id='fct' class='ink' style='font-size:22px;font-weight:600;line-height:1.35'></div></div></div>""",
 """var cyc=2.6;var ph=t-cyc*Math.floor(t/cyc);var sx=Math.abs(Math.cos(ph/cyc*Math.PI*2));
    document.getElementById('fc').style.transform='scaleX('+Math.max(0.02,sx).toFixed(3)+')';
    var back=(ph/cyc)>0.5;var idx=Math.floor(t/cyc)%2;
    var qs=['What is the Krebs cycle?','Define photosynthesis.'];var as=['Releases energy from glucose in the mitochondria.','How plants turn light into chemical energy.'];
    document.getElementById('fcl').textContent=back?'A':'Q';
    document.getElementById('fct').textContent=back?as[idx]:qs[idx];""")

for n,h in {"spark":spark,"m_notes":m_notes,"m_ai":m_ai,"m_guide":m_guide,"m_cards":m_cards}.items():
    (OUTH/f"{n}.html").write_text(h); print("wrote",n)

# dummy talking-head still (illustrated placeholder — not a real person), neutral studio bg
head_html=f"""<!doctype html><html><head><meta charset='utf-8'><style>
*{{margin:0;box-sizing:border-box}}html,body{{width:720px;height:1280px;overflow:hidden}}
.bg{{width:720px;height:1280px;background:linear-gradient(160deg,#aeb7b0,#c7cbc4 55%,#b7bcb5);position:relative}}
.torso{{position:absolute;left:50%;bottom:0;transform:translateX(-50%);width:460px;height:520px;background:#2b2f2c;border-radius:230px 230px 0 0}}
.head{{position:absolute;left:50%;top:300px;transform:translateX(-50%);width:250px;height:300px;background:#d9b79a;border-radius:50% 50% 46% 46%}}
.hair{{position:absolute;left:50%;top:270px;transform:translateX(-50%);width:266px;height:150px;background:#4b3a2e;border-radius:50% 50% 0 0}}
.mic{{position:absolute;left:50%;bottom:0;transform:translateX(-50%);width:120px;height:300px;background:#111;border-radius:60px 60px 0 0}}
.badge{{position:absolute;left:50%;top:70px;transform:translateX(-50%);font-family:sans-serif;font-size:20px;color:rgba(20,20,20,.35);letter-spacing:2px}}</style></head>
<body><div class='bg'><div class='torso'></div><div class='hair'></div><div class='head'></div><div class='mic'></div>
<div class='badge'>&#9678; PLACEHOLDER PRESENTER</div></div></body></html>"""
(OUTH/"head.html").write_text(head_html); print("wrote head.html")
