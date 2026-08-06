#!/usr/bin/env python3
"""Render every slide of a reel in the Globalmodo brand system (light editorial:
warm off-white bg, Fraunces + Inter, one amber accent per slide, eyebrow rules,
G-mark, amber baseline). Silent, no captions — each slide carries its own words.

Reads a brand storyboard; writes build/brand_slides/<id>.html for every beat plus
a manifest of "<id> <duration>" lines. Every slide exposes window.renderAt(t).
Text emphasis is marked with [brackets] -> amber.

usage: python3 mockups/make_brand.py <storyboard.json>
"""
import json, pathlib, sys, html as H, re
ROOT = pathlib.Path(__file__).parent.parent
FONTS = ROOT/"fonts"
GMARK = (ROOT/"assets"/"gmark.txt").read_text().strip()
OUT = ROOT/"build"/"brand_slides"; OUT.mkdir(parents=True, exist_ok=True)
SB = json.loads(pathlib.Path(sys.argv[1] if len(sys.argv)>1 else ROOT/"storyboards"/"week_brand.json").read_text())
C = SB["meta"]["brand"]

def wf(fam, file, w, style="normal"):
    return f"@font-face{{font-family:'{fam}';src:url('file://{FONTS/file}') format('woff2');font-weight:{w};font-style:{style};}}"

CSS = f"""
{wf('Fraunces','fraunces-latin-300-normal.woff2',300)}{wf('Fraunces','fraunces-latin-400-normal.woff2',400)}
{wf('Fraunces','fraunces-latin-500-normal.woff2',500)}{wf('Fraunces','fraunces-latin-400-italic.woff2',400,'italic')}
{wf('Inter','inter-latin-400-normal.woff2',400)}{wf('Inter','inter-latin-500-normal.woff2',500)}{wf('Inter','inter-latin-600-normal.woff2',600)}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:720px;height:1280px;overflow:hidden;background:{C['bg']}}}
.slide{{position:relative;width:720px;height:1280px;background:{C['bg']};transform-origin:50% 50%;
  font-family:'Inter',sans-serif;color:{C['ink']};padding:96px 72px;display:flex;flex-direction:column}}
.baseline{{position:absolute;left:0;right:0;bottom:0;height:6px;background:{C['amber']};transform:scaleX(0);transform-origin:left}}
.gmark{{position:absolute;right:60px;bottom:44px;width:46px;height:46px;background:{C['white']};
  border:0.5px solid {C['hairline']};border-radius:8px;display:flex;align-items:center;justify-content:center;opacity:0}}
.gmark img{{width:34px;height:34px;border-radius:5px}}
.eyebrow{{display:flex;align-items:center;gap:14px;opacity:0}}
.eyebrow .rule{{width:0;height:2px;background:{C['amber']}}}
.eyebrow .lbl{{font-size:15px;font-weight:500;letter-spacing:.16em;text-transform:uppercase;color:{C['muted']}}}
.h{{font-family:'Fraunces',serif;font-weight:400;color:{C['ink']};letter-spacing:-1.2px;line-height:1.08}}
.h.gr{{color:{C['green']}}}
.am{{color:{C['amber']}}}
.w{{display:inline-block;opacity:0;transform:translateY(14px)}}
.card{{background:{C['white']};border:0.5px solid {C['hairline']};border-radius:8px;box-shadow:0 18px 50px rgba(31,58,46,.06)}}
.ftitle{{font-family:'Fraunces',serif;font-weight:400;color:{C['green']}}}
.imut{{color:{C['muted']}}}.igreen{{color:{C['green']}}}
"""

GMARK_HTML = f"<div class='gmark'><img src='{GMARK}'></div>"
PUSH = ("var s=document.querySelector('.slide');s.style.transform='scale('+(1+0.014*Math.min(1,t/3)).toFixed(4)+')';"
        "var g=document.querySelector('.gmark');if(g)g.style.opacity=Math.max(0,Math.min(1,(t-0.5)/0.5));"
        "var b=document.querySelector('.baseline');if(b)b.style.transform='scaleX('+Math.max(0,Math.min(1,(t-0.2)/0.9)).toFixed(3)+')';"
        "var e=document.querySelector('.eyebrow');if(e){var p=Math.max(0,Math.min(1,(t-0.15)/0.5));e.style.opacity=p;var r=e.querySelector('.rule');if(r)r.style.width=(46*p).toFixed(0)+'px';}")

def emph(text):
    # [word] -> amber span ; keep \n as <br>
    out=[]
    for li,line in enumerate(text.split("\n")):
        if li>0: out.append("<br>")
        # split into tokens preserving [..]
        for tok in re.split(r'(\[[^\]]+\])', line):
            if not tok: continue
            if tok.startswith("[") and tok.endswith("]"):
                for w in tok[1:-1].split(" "):
                    out.append(f"<span class='w am'>{H.escape(w)}</span> ")
            else:
                for w in tok.split(" "):
                    if w=="": continue
                    out.append(f"<span class='w'>{H.escape(w)}</span> ")
    return "".join(out)

def eyebrow(label):
    return f"<div class='eyebrow'><span class='rule'></span><span class='lbl'>{H.escape(label)}</span></div>" if label else "<div class='eyebrow' style='opacity:0'></div>"

def reveal_words_js(start=0.45, step=0.10):
    return (f"var ws=document.querySelectorAll('.h .w');for(var i=0;i<ws.length;i++){{"
            f"var st={start}+i*{step};var p=Math.max(0,Math.min(1,(t-st)/0.34));"
            f"ws[i].style.opacity=p;ws[i].style.transform='translateY('+(14*(1-p)).toFixed(1)+'px)';}}")

def html_doc(body, js, extra_css=""):
    return (f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}{extra_css}</style></head>"
            f"<body><div class='slide'>{body}{GMARK_HTML}<div class='baseline'></div></div>"
            f"<script>window.renderAt=function(t){{{PUSH}{js}}};window.renderAt(0);</script></body></html>")

# ---------------- TEXT SLIDE ----------------
def text_slide(b):
    kick = eyebrow(b.get("kicker"))
    cta = (f"<div class='cta' style='margin-top:44px;align-self:flex-start;background:{C['green']};color:{C['bg']};"
           f"font-family:Inter;font-weight:600;font-size:22px;padding:16px 26px;border-radius:6px;opacity:0'>"
           f"{H.escape(b['cta'])}</div>") if b.get("cta") else ""
    body = (f"{kick}<div style='margin-top:auto;margin-bottom:auto'>"
            f"<div class='h' style='font-size:72px'>{emph(b['text'])}</div>{cta}</div>")
    js = reveal_words_js() + (
        "var c=document.querySelector('.cta');if(c){var ws=document.querySelectorAll('.h .w');"
        "var st=0.45+ws.length*0.10+0.3;var p=Math.max(0,Math.min(1,(t-st)/0.35));"
        "c.style.opacity=p;c.style.transform='translateY('+(10*(1-p)).toFixed(1)+'px)';}")
    return html_doc(body, js)

# ---------------- MOCKUP HEADER (shared) ----------------
def mock_header(b):
    return (f"<div class='eyebrow'><span class='rule'></span><span class='lbl'>{H.escape(b['step'])}</span></div>"
            f"<div class='h gr' style='font-size:46px;margin-top:18px'>{emph(b['title'])}</div>")

MHEAD_JS = reveal_words_js(0.45, 0.08)

# ---------------- MOCKUP: w1 voice ----------------
def w1(b):
    traits=[("Tone","warm & direct"),("Rhythm","short, punchy lines"),
            ("Vocabulary","the words you use"),("Structure","hook · value · CTA")]
    rows="".join(f"""<div class='tr' data-i='{i}' style='padding:16px 0;border-bottom:0.5px solid {C['hairline']}'>
      <div style='display:flex;justify-content:space-between;font-size:16px;margin-bottom:9px'>
        <span class='igreen' style='font-weight:600'>{a}</span><span class='imut'>{d}</span></div>
      <div style='height:8px;background:{C['bg']};border-radius:5px;overflow:hidden'>
        <div class='fill' style='height:100%;width:0;background:{C['amber']};border-radius:5px'></div></div></div>"""
      for i,(a,d) in enumerate(traits))
    body=(f"{mock_header(b)}<div style='margin-top:auto;margin-bottom:auto'>"
          f"<div class='card' style='padding:30px 34px'>"
          f"<div class='ftitle' style='font-size:26px;margin-bottom:6px'>Your Brand Voice</div>"
          f"<div class='imut' style='font-size:14px;margin-bottom:14px'>Learned from your 5 best posts</div>{rows}</div></div>")
    js=MHEAD_JS+(f"var tr=document.querySelectorAll('.tr');for(var i=0;i<tr.length;i++){{"
                 f"var st=1.0+i*0.5;var p=Math.max(0,Math.min(1,(t-st)/0.7));"
                 f"tr[i].querySelector('.fill').style.width=(p*100).toFixed(0)+'%';}}")
    return html_doc(body, js)

# ---------------- MOCKUP: w2 idea ----------------
def w2(b):
    body=(f"{mock_header(b)}<div style='margin-top:auto;margin-bottom:auto'>"
          f"<div class='card' style='padding:32px 34px'>"
          f"<div class='imut' style='font-size:13px;font-weight:600;letter-spacing:.12em;text-transform:uppercase;margin-bottom:14px'>Your one idea</div>"
          f"<div style='border-bottom:2px solid {C['hairline']};padding-bottom:14px'>"
          f"<span id='idea' class='ftitle' style='font-size:28px'></span></div>"
          f"<div id='cmd' style='margin-top:24px;background:{C['amber_light']};border:1px solid {C['amber']};border-radius:6px;"
          f"padding:16px 18px;color:{C['green']};font-weight:600;font-size:17px;opacity:0'></div></div></div>")
    js=MHEAD_JS+("""var idea="The 3-second hook that stops the scroll.";var ni=Math.min(idea.length,Math.floor(Math.max(0,t-0.8)*17));
      document.getElementById('idea').innerHTML=idea.slice(0,ni)+((Math.floor(t*1.8)%2)&&ni<idea.length?"<span style='color:__AMBER__'>|</span>":'');
      var cmd="Turn this into a week of posts, in my voice.";var t2=t-0.8-(idea.length/17)-0.4;var el=document.getElementById('cmd');
      if(t2>0){el.style.opacity=1;var nc=Math.min(cmd.length,Math.floor(t2*24));el.textContent=cmd.slice(0,nc)+((Math.floor(t*1.8)%2)&&nc<cmd.length?'|':'');}""".replace("__AMBER__", C['amber']))
    return html_doc(body, js)

# ---------------- MOCKUP: w3 week ----------------
def w3(b):
    days=["MON","TUE","WED","THU","FRI"]
    rows="".join(f"""<div class='dr' data-i='{i}' style='display:flex;align-items:center;gap:16px;padding:15px 20px;
      border-bottom:0.5px solid {C['hairline']};opacity:0;transform:translateX(-10px)'>
      <span class='igreen' style='font-family:Fraunces;font-weight:500;font-size:15px;letter-spacing:1px;min-width:52px'>{d}</span>
      <div style='flex:1'><div style='height:9px;width:78%;background:{C['hairline']};border-radius:5px;margin-bottom:7px'></div>
        <div style='height:8px;width:56%;background:{C['bg']};border:0.5px solid {C['hairline']};border-radius:5px'></div></div>
      <span style='width:9px;height:9px;border-radius:50%;background:{C['amber']}'></span></div>"""
      for i,d in enumerate(days))
    body=(f"{mock_header(b)}<div style='margin-top:auto;margin-bottom:auto'>"
          f"<div class='card' style='overflow:hidden'>"
          f"<div style='padding:18px 20px;border-bottom:0.5px solid {C['hairline']};background:{C['green_light']}'>"
          f"<span class='ftitle' style='font-size:20px'>This week — generated</span></div>{rows}</div></div>")
    js=MHEAD_JS+(f"var dr=document.querySelectorAll('.dr');for(var i=0;i<dr.length;i++){{"
                 f"var st=0.9+i*0.55;var p=Math.max(0,Math.min(1,(t-st)/0.4));"
                 f"dr[i].style.opacity=p;dr[i].style.transform='translateX('+(-10*(1-p)).toFixed(1)+'px)';}}")
    return html_doc(body, js)

# ---------------- MOCKUP: w4 schedule ----------------
def w4(b):
    days=["MON","TUE","WED","THU","FRI"]
    cols="".join(f"""<div style='flex:1;display:flex;flex-direction:column;gap:10px;align-items:center'>
      <div class='igreen' style='font-family:Fraunces;font-size:14px;letter-spacing:1px'>{d}</div>
      <div style='width:100%;height:150px;background:{C['bg']};border:1px dashed {C['hairline']};border-radius:8px;position:relative'>
        <div class='chip' data-i='{i}' style='position:absolute;left:6px;right:6px;top:6px;height:138px;background:{C['amber']};border-radius:6px;opacity:0;transform:scale(.9)'></div></div></div>"""
      for i,d in enumerate(days))
    body=(f"{mock_header(b)}<div style='margin-top:auto;margin-bottom:auto'>"
          f"<div class='card' style='padding:26px 22px'>"
          f"<div class='ftitle' style='font-size:22px;margin-bottom:18px'>Content scheduler</div>"
          f"<div style='display:flex;gap:10px'>{cols}</div></div></div>")
    js=MHEAD_JS+(f"var ch=document.querySelectorAll('.chip');for(var i=0;i<ch.length;i++){{"
                 f"var st=1.0+i*0.5;var p=Math.max(0,Math.min(1,(t-st)/0.35));"
                 f"ch[i].style.opacity=(p*0.92).toFixed(3);ch[i].style.transform='scale('+(0.9+0.1*p).toFixed(3)+')';}}")
    return html_doc(body, js)

MOCKS={"w1_voice":w1,"w2_idea":w2,"w3_week":w3,"w4_schedule":w4}
manifest=[]
for b in SB["beats"]:
    if b["type"]=="text": doc=text_slide(b)
    else: doc=MOCKS[b["asset"]](b)
    (OUT/f"{b['id']}.html").write_text(doc)
    manifest.append(f"{b['id']} {round(b['end']-b['start'],3)}")
    print("wrote slide", b["id"], b.get("asset") or "text")
(OUT/"manifest.txt").write_text("\n".join(manifest)+"\n")
