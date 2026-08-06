#!/usr/bin/env python3
"""Kinetic text cards for the no-voiceover / no-talking-head visual reel.
Reads a storyboard and, for every beat of type "text", writes an animated HTML card
exposing window.renderAt(t): a small serif kicker fades in, the statement's words
reveal in sequence, and an optional CTA pops in at the end. A manifest of
"t<id> <duration>" lines is written to build/text_cards/manifest.txt for capture.

usage: python3 mockups/make_text_cards.py <storyboard.json>
"""
import json, pathlib, sys, html as _html
ROOT = pathlib.Path(__file__).parent.parent
FONTS = ROOT/"fonts"
OUT = ROOT/"build"/"text_cards"; OUT.mkdir(parents=True, exist_ok=True)
ACCENT = "#f5a623"
SB = json.loads(pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ROOT/"storyboards"/"week_visual.json").read_text())

def ff(f,w,s="normal"): return f"@font-face{{font-family:'Mont';src:url('file://{FONTS/f}') format('woff2');font-weight:{w};font-style:{s};}}"
def ffs(f,w,s): return f"@font-face{{font-family:'Playf';src:url('file://{FONTS/f}') format('woff2');font-weight:{w};font-style:{s};}}"
CSS=f"""{ff('montserrat-latin-600-normal.woff2',600)}{ff('montserrat-latin-700-normal.woff2',700)}{ff('montserrat-latin-800-normal.woff2',800)}{ffs('playfair-display-latin-700-italic.woff2',700,'italic')}
*{{margin:0;padding:0;box-sizing:border-box;font-family:'Mont',sans-serif;-webkit-font-smoothing:antialiased}}
html,body{{width:720px;height:1280px;overflow:hidden;background:#08080a}}
.stage{{position:relative;width:720px;height:1280px;transform-origin:50% 50%;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:0 72px;text-align:center;
 background:radial-gradient(120% 80% at 50% 46%, rgba(245,166,35,.20) 0%, rgba(245,166,35,.05) 36%, rgba(8,8,10,0) 64%), #08080a}}
.kick{{font-family:'Playf',serif;font-style:italic;font-weight:700;color:{ACCENT};font-size:30px;letter-spacing:2px;margin-bottom:26px;opacity:0}}
.stmt{{color:#f6f6f8;font-weight:800;font-size:56px;line-height:1.16;letter-spacing:-0.5px}}
.w{{display:inline-block;opacity:0;transform:translateY(16px)}}
.cta{{margin-top:40px;display:inline-block;background:{ACCENT};color:#141417;font-weight:800;font-size:24px;padding:16px 26px;border-radius:16px;opacity:0;transform:scale(.92)}}"""

def words_html(text):
    # keep explicit line breaks; wrap each word in a reveal span
    out=[];
    for li,line in enumerate(text.split("\n")):
        if li>0: out.append("<br>")
        for w in line.split(" "):
            out.append(f"<span class='w'>{_html.escape(w)}</span> ")
    return "".join(out)

manifest=[]
for b in SB["beats"]:
    if b.get("type")!="text": continue
    kick = f"<div class='kick'>{_html.escape(b['kicker'])}</div>" if b.get("kicker") else ""
    cta  = f"<div class='cta'>{_html.escape(b['cta'])}</div>" if b.get("cta") else ""
    body = f"{kick}<div class='stmt'>{words_html(b['text'])}</div>{cta}"
    js = """
    var s=document.querySelector('.stage');s.style.transform='scale('+(1+0.004*t).toFixed(4)+')';
    var k=document.querySelector('.kick');if(k){k.style.opacity=Math.max(0,Math.min(1,(t-0.05)/0.4));k.style.transform='translateY('+(8*(1-Math.min(1,(t-0.05)/0.4))).toFixed(1)+'px)';}
    var ws=document.querySelectorAll('.w');for(var i=0;i<ws.length;i++){var st=0.35+i*0.11;var p=Math.max(0,Math.min(1,(t-st)/0.32));ws[i].style.opacity=p;ws[i].style.transform='translateY('+(16*(1-p)).toFixed(1)+'px)';}
    var c=document.querySelector('.cta');if(c){var st=0.35+ws.length*0.11+0.25;var p=Math.max(0,Math.min(1,(t-st)/0.3));c.style.opacity=p;c.style.transform='scale('+(0.92+0.08*p).toFixed(3)+')';}
    """
    doc=f"<!doctype html><html><head><meta charset='utf-8'><style>{CSS}</style></head><body><div class='stage'>{body}</div><script>window.renderAt=function(t){{{js}}};window.renderAt(0);</script></body></html>"
    (OUT/f"t{b['id']}.html").write_text(doc)
    manifest.append(f"t{b['id']} {round(b['end']-b['start'],3)}")
    print("wrote", f"t{b['id']}.html", f"({round(b['end']-b['start'],2)}s)")
(OUT/"manifest.txt").write_text("\n".join(manifest)+"\n")
