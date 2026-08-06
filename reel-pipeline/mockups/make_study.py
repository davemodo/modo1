#!/usr/bin/env python3
"""Original animated B-roll + intro spark + dummy talking-head for the recreated
'free AI study tool' reel. Dark product-UI aesthetic (amber glow), NOT the
reference's Google/Gemini screenshots. Each exposes window.renderAt(t)."""
import pathlib, subprocess
ROOT = pathlib.Path(__file__).parent.parent   # project root (mockups/ -> reel-pipeline/)
FONTS = ROOT/"fonts"
OUTH = ROOT/"build"/"broll_anim"; OUTH.mkdir(parents=True, exist_ok=True)
A="#f5a623"
def ff(f,w,s="normal"): return f"@font-face{{font-family:'Mont';src:url('file://{FONTS/f}') format('woff2');font-weight:{w};font-style:{s};}}"
CSS=f"""{ff('montserrat-latin-500-normal.woff2',500)}{ff('montserrat-latin-600-normal.woff2',600)}{ff('montserrat-latin-700-normal.woff2',700)}{ff('montserrat-latin-800-normal.woff2',800)}
*{{margin:0;padding:0;box-sizing:border-box;font-family:'Mont',sans-serif;-webkit-font-smoothing:antialiased}}
html,body{{width:720px;height:1280px;overflow:hidden;background:#08080a}}
.stage{{position:relative;width:720px;height:1280px;transform-origin:50% 46%;background:radial-gradient(120% 90% at 50% 42%, rgba(245,166,35,.22) 0%, rgba(245,166,35,.06) 34%, rgba(8,8,10,0) 62%), #08080a}}
.card{{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);background:#141417;border:1px solid rgba(255,255,255,.08);border-radius:26px;overflow:hidden;box-shadow:0 0 0 1px rgba(245,166,35,.10),0 30px 80px rgba(0,0,0,.6),0 0 90px rgba(245,166,35,.18)}}
.bar{{height:52px;display:flex;align-items:center;gap:8px;padding:0 18px;background:#1b1b1f;border-bottom:1px solid rgba(255,255,255,.06)}}
.muted{{color:#8a8a92}}.white{{color:#f4f4f6}}.amber{{color:{A}}}"""
PUSH="var s=document.querySelector('.stage');s.style.transform='scale('+(1+0.006*t).toFixed(4)+')';"
def page(body,js): return f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body><div class='stage'>{body}</div><script>window.renderAt=function(t){{{PUSH}{js}}};window.renderAt(0);</script></body></html>"

# spark (intro)
spark=page(f"""<svg style='position:absolute;left:50%;top:44%;transform:translate(-50%,-50%)' width='340' height='340' viewBox='0 0 200 200'>
  <g id='st'><path d='M100 8 C108 60 140 92 192 100 C140 108 108 140 100 192 C92 140 60 108 8 100 C60 92 92 60 100 8 Z' fill='{A}'/></g>
  <circle id='ring' cx='100' cy='100' r='70' fill='none' stroke='{A}' stroke-width='2' opacity='.5'/></svg>""",
 """var sc=Math.min(1,t/0.7),e=1-Math.pow(1-sc,3);var st=document.getElementById('st');
    st.setAttribute('transform','translate(100,100) scale('+(e*1).toFixed(3)+') rotate('+(t*40)+') translate(-100,-100)');
    st.setAttribute('opacity',e.toFixed(2));var r=document.getElementById('ring');r.setAttribute('r',(70+16*Math.sin(t*3)).toFixed(1));r.setAttribute('opacity',(0.15+0.25*Math.abs(Math.sin(t*3))).toFixed(2));""")

# m_notes (The Chaos)
frags="".join(f"<div class='fr' data-i='{i}' style='position:absolute;height:12px;border-radius:6px;background:rgba(255,255,255,.22)' ></div>" for i in range(9))
m_notes=page(f"""<div class='card' style='width:590px;height:540px'>
  <div class='bar'><div class='dot' style='width:11px;height:11px;border-radius:50%;background:#ff5f57'></div><div class='muted' style='margin-left:8px;font-size:15px;font-weight:600'>Notes — a mess</div></div>
  <div id='cv' style='position:relative;height:470px'>{frags}
   <div class='tag' style='position:absolute;left:60px;top:300px;background:rgba(245,166,35,.16);color:{A};font-size:13px;font-weight:700;padding:6px 12px;border-radius:20px'>lecture.pdf</div>
   <div class='tag' style='position:absolute;left:330px;top:360px;background:rgba(255,255,255,.08);color:#f4f4f6;font-size:13px;font-weight:700;padding:6px 12px;border-radius:20px'>screenshot</div></div></div>""",
 """var fr=document.querySelectorAll('.fr');var W=[70,52,60,44,66,50,72,40,58];var X=[50,60,44,300,320,54,64,330,58];var Y=[70,110,150,80,120,210,250,210,300];var R=[-4,3,-2,5,-3,2,-5,4,-2];
    for(var i=0;i<fr.length;i++){var p=Math.max(0,Math.min(1,(t-0.15-i*0.12)/0.35));fr[i].style.width=(W[i]*3)+'px';fr[i].style.left=X[i]+'px';fr[i].style.top=Y[i]+'px';
    fr[i].style.opacity=p.toFixed(2);fr[i].style.transform='rotate('+(R[i]*p).toFixed(1)+'deg) translateY('+(10*(1-p)).toFixed(1)+'px)';}
    var tg=document.querySelectorAll('.tag');for(var j=0;j<tg.length;j++){tg[j].style.opacity=Math.max(0,Math.min(1,(t-1.4-j*0.3)/0.4)).toFixed(2);}""")

# m_ai (One Prompt)
m_ai=page(f"""<div class='card' style='width:590px;height:560px'>
  <div class='bar'><div class='amber' style='font-weight:800;font-size:16px'>&#10022; AI Tutor</div></div>
  <div style='padding:28px 30px;display:flex;flex-direction:column;gap:18px'>
   <div style='align-self:flex-start;max-width:82%;background:#1e1e23;border:1px solid rgba(255,255,255,.06);border-radius:16px 16px 16px 4px;padding:15px 17px'>
    <div class='muted' style='font-size:13px;font-weight:700;margin-bottom:6px'>Your notes (pasted)</div>
    <div class='white' style='font-size:15px;line-height:1.5;opacity:.85'>&#8220;photosynthesis&#8230; mitochondria&#8230; the krebs cycle&#8230; ???&#8221;</div></div>
   <div id='ub' style='align-self:flex-end;max-width:80%;background:{A};color:#141417;border-radius:16px 16px 4px 16px;padding:15px 17px;font-weight:700;font-size:17px;min-height:20px'></div>
   <div id='think' style='align-self:flex-start;display:flex;gap:8px;opacity:0'><span class='td' style='width:9px;height:9px;border-radius:50%;background:#8a8a92'></span><span class='td' style='width:9px;height:9px;border-radius:50%;background:#8a8a92'></span><span class='td' style='width:9px;height:9px;border-radius:50%;background:#8a8a92'></span></div></div></div>""",
 """var full="Turn my notes into a clean study guide.";var n=Math.min(full.length,Math.floor(Math.max(0,t-0.5)*20));
    document.getElementById('ub').textContent=full.slice(0,n)+((Math.floor(t*1.8)%2)&&n<full.length?'|':'');
    document.getElementById('think').style.opacity=(n>=full.length)?1:0;
    var d=document.querySelectorAll('.td');for(var i=0;i<d.length;i++){d[i].style.transform='translateY('+(-4*Math.max(0,Math.sin(t*6-i*0.9))).toFixed(1)+'px)';}""")

# m_guide (Perfect Guide)
secs=["Overview","Key concepts","Worked examples","Summary","Practice quiz"]
rows="".join(f"""<div class='gr' data-i='{i}' style='display:flex;align-items:center;gap:14px;padding:14px 0;border-bottom:1px solid rgba(255,255,255,.05);opacity:0;transform:translateY(10px)'>
  <div style='min-width:30px;height:30px;border-radius:9px;background:rgba(245,166,35,.16);color:{A};font-weight:800;display:flex;align-items:center;justify-content:center;font-size:14px'>{i+1}</div>
  <div class='white' style='font-size:16px;font-weight:500;flex:1'>{s}</div><div class='ck' style='color:{A};font-size:17px;opacity:0'>&#10003;</div></div>""" for i,s in enumerate(secs))
m_guide=page(f"""<div class='card' style='width:600px;height:600px'>
  <div class='bar'><div class='amber' style='font-weight:800;font-size:16px'>&#10022; AI Tutor</div><div class='muted' style='margin-left:10px;font-size:14px;font-weight:600'>Study guide ready</div></div>
  <div style='padding:24px 34px'><div class='white' style='font-weight:800;font-size:23px'>Your Study Guide</div><div style='margin-top:6px'>{rows}</div></div></div>""",
 """var gr=document.querySelectorAll('.gr');for(var i=0;i<gr.length;i++){var st=0.35+i*0.5;var p=Math.max(0,Math.min(1,(t-st)/0.4));gr[i].style.opacity=p;gr[i].style.transform='translateY('+(10*(1-p)).toFixed(1)+'px)';gr[i].querySelector('.ck').style.opacity=(t>st+0.35)?1:0;}""")

# m_cards (Flashcards)
m_cards=page(f"""<div style='position:absolute;left:50%;top:48%;transform:translate(-50%,-50%);width:420px;height:300px'>
  <div style='position:absolute;inset:0;transform:translate(26px,26px) rotate(6deg);background:#17171b;border:1px solid rgba(255,255,255,.06);border-radius:20px'></div>
  <div style='position:absolute;inset:0;transform:translate(13px,13px) rotate(3deg);background:#1b1b20;border:1px solid rgba(255,255,255,.07);border-radius:20px'></div>
  <div id='fc' style='position:absolute;inset:0;background:#141417;border:1px solid rgba(245,166,35,.25);border-radius:20px;box-shadow:0 20px 60px rgba(0,0,0,.5),0 0 70px rgba(245,166,35,.16);display:flex;flex-direction:column;align-items:center;justify-content:center;padding:30px;text-align:center'>
    <div id='fcl' class='amber' style='font-weight:800;font-size:14px;letter-spacing:2px;margin-bottom:14px'>Q</div>
    <div id='fct' class='white' style='font-size:22px;font-weight:600;line-height:1.35'></div></div></div>""",
 """var cyc=2.6;var ph=t-cyc*Math.floor(t/cyc);var sx=Math.abs(Math.cos(ph/cyc*Math.PI*2));
    var fc=document.getElementById('fc');fc.style.transform='scaleX('+Math.max(0.02,sx).toFixed(3)+')';
    var back=(ph/cyc)>0.5;var idx=Math.floor(t/cyc)%2;
    var qs=['What is the Krebs cycle?','Define photosynthesis.'];var as=['It releases energy from glucose in mitochondria.','How plants turn light into chemical energy.'];
    document.getElementById('fcl').textContent=back?'A':'Q';document.getElementById('fcl').style.color=back?'#f4f4f6':'__A__';
    document.getElementById('fct').textContent=back?as[idx]:qs[idx];""".replace("__A__",A))

for n,h in {"spark":spark,"m_notes":m_notes,"m_ai":m_ai,"m_guide":m_guide,"m_cards":m_cards}.items():
    (OUTH/f"{n}.html").write_text(h); print("wrote",n)

# dummy talking-head still (illustrated placeholder — not a real person)
head_html=f"""<!doctype html><html><head><meta charset='utf-8'><style>
*{{margin:0;box-sizing:border-box}}html,body{{width:720px;height:1280px;overflow:hidden}}
.bg{{width:720px;height:1280px;background:linear-gradient(160deg,#aeb7b0,#c7cbc4 55%,#b7bcb5);position:relative}}
.torso{{position:absolute;left:50%;bottom:0;transform:translateX(-50%);width:460px;height:520px;background:#2b2f2c;border-radius:230px 230px 0 0}}
.head{{position:absolute;left:50%;top:300px;transform:translateX(-50%);width:250px;height:300px;background:#d9b79a;border-radius:50% 50% 46% 46%}}
.hair{{position:absolute;left:50%;top:270px;transform:translateX(-50%);width:266px;height:150px;background:#4b3a2e;border-radius:50% 50% 0 0}}
.mic{{position:absolute;left:50%;bottom:0;transform:translateX(-50%);width:120px;height:300px;background:#111;border-radius:60px 60px 0 0}}
.badge{{position:absolute;left:50%;top:70px;transform:translateX(-50%);font-family:sans-serif;font-size:20px;color:rgba(20,20,20,.35);letter-spacing:2px}}</style></head>
<body><div class='bg'><div class='torso'></div><div class='hair'></div><div class='head'></div><div class='mic'></div>
<div class='badge'>◍ PLACEHOLDER PRESENTER</div></div></body></html>"""
(OUTH/"head.html").write_text(head_html); print("wrote head.html")
