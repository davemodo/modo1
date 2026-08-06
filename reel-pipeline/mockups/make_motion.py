#!/usr/bin/env python3
"""Pure motion-graphics scenes (NO text, no brand) for the "2 types of labor" reel.
Each beat is an abstract animation that embodies the idea. Cinematic dark palette,
bone-white forms, a single coral accent + a mint counter-tone. Every scene exposes
window.renderAt(t) and fades its content in/out to the bg so clips concatenate
seamlessly. JS lives in raw strings (no f-string brace escaping); colors are injected
via token replacement.

usage: python3 mockups/make_motion.py <storyboard.json>
"""
import json, pathlib, sys
ROOT = pathlib.Path(__file__).parent.parent
OUT = ROOT/"build"/"motion_slides"; OUT.mkdir(parents=True, exist_ok=True)
SB = json.loads(pathlib.Path(sys.argv[1] if len(sys.argv)>1 else ROOT/"storyboards"/"motion_labor.json").read_text())

BG="#0C0D10"; BONE="#ECE8DC"; DIM="#2C2D34"; DIM2="#484A54"; CORAL="#FF5A36"; MINT="#4BC7A0"
W,H=720,1280

def tokens(js):
    return (js.replace("__CORAL__",CORAL).replace("__BONE__",BONE).replace("__MINT__",MINT)
              .replace("__DIM__",DIM).replace("__DIM2__",DIM2).replace("__BG__",BG))

def doc(svg, js, dur):
    css = "html,body{margin:0;width:720px;height:1280px;background:__BG__;overflow:hidden}.scene{position:absolute;inset:0;width:720px;height:1280px;transform-origin:50% 50%}svg{position:absolute;inset:0}".replace("__BG__",BG)
    wrap = ("var sc=document.querySelector('.scene');"
            "var fi=Math.max(0,Math.min(1,t/0.45)),fo=Math.max(0,Math.min(1,(DUR-t)/0.4));"
            "sc.style.opacity=(fi*fo).toFixed(3);"
            "sc.style.transform='scale('+(1+0.02*Math.min(1,t/DUR)).toFixed(4)+')';")
    return ("<!doctype html><html><head><meta charset='utf-8'><style>"+css+"</style></head><body>"
            "<div class='scene'>"+svg+"</div><script>var DUR="+str(dur)+";"
            "window.renderAt=function(t){"+wrap+tokens(js)+"};window.renderAt(0);</script></body></html>")

# ---------- 1. two spinners (busy, going in circles) ----------
def gears(dur):
    svg=f'''<svg viewBox="0 0 {W} {H}">
      <g id="s1"><circle cx="270" cy="600" r="92" fill="none" stroke="{BONE}" stroke-width="16" stroke-dasharray="360 130" stroke-linecap="round"/></g>
      <g id="s2"><circle cx="450" cy="720" r="72" fill="none" stroke="{CORAL}" stroke-width="16" stroke-dasharray="270 100" stroke-linecap="round"/></g>
      <circle id="o1" cx="270" cy="508" r="9" fill="{BONE}"/><circle id="o2" cx="450" cy="648" r="9" fill="{CORAL}"/></svg>'''
    js='''document.getElementById('s1').setAttribute('transform','rotate('+(t*200)+' 270 600)');
    document.getElementById('s2').setAttribute('transform','rotate('+(-t*270)+' 450 720)');
    var a1=(t*200-90)*Math.PI/180;document.getElementById('o1').setAttribute('cx',270+92*Math.cos(a1));document.getElementById('o1').setAttribute('cy',600+92*Math.sin(a1));
    var a2=(-t*270-90)*Math.PI/180;document.getElementById('o2').setAttribute('cx',450+72*Math.cos(a2));document.getElementById('o2').setAttribute('cy',720+72*Math.sin(a2));'''
    return doc(svg,js,dur)

# ---------- 2. build a tower no one asked for ----------
def tower(dur):
    blocks="".join(f'<rect id="b{i}" x="{260}" y="{770-(i+1)*66}" width="200" height="58" rx="6" fill="{BONE}"/>' for i in range(5))
    aud="".join(f'<circle class="aud" cx="{150+i*70}" cy="980" r="12" fill="{DIM2}"/>' for i in range(6))
    svg=f'<svg viewBox="0 0 {W} {H}">{blocks}<line x1="200" y1="828" x2="520" y2="828" stroke="{DIM}" stroke-width="3"/>{aud}</svg>'
    js='''for(var i=0;i<5;i++){var b=document.getElementById('b'+i);var st=0.3+i*0.42;var p=Math.max(0,Math.min(1,(t-st)/0.4));
    var e=1-Math.pow(1-p,3);b.style.opacity=p.toFixed(2);b.setAttribute('transform','translate(0,'+(-70*(1-e)).toFixed(1)+')');}
    var built=Math.max(0,Math.min(1,(t-2.6)/0.6));
    var sway=built*2.2*Math.sin(t*2.0);document.querySelectorAll('rect').forEach(function(r){r.setAttribute('transform',(r.style.opacity>0.9?'rotate('+sway.toFixed(2)+' 360 770)':r.getAttribute('transform')||''));});
    var dim=1-0.55*Math.max(0,Math.min(1,(t-(DUR-1.2))/0.9));document.querySelectorAll('rect').forEach(function(r){if(r.style.opacity>0.9)r.setAttribute('fill-opacity',dim.toFixed(2));});'''
    return doc(svg,js,dur)

# ---------- 3. perfect something no one will see ----------
def gem(dur):
    sp="".join(f'<circle class="sp" data-i="{i}" cx="360" cy="540" r="5" fill="{BONE}"/>' for i in range(7))
    svg=f'''<svg viewBox="0 0 {W} {H}">
      <g id="gem"><polygon points="360,470 430,540 360,650 290,540" fill="{CORAL}"/>
      <polygon points="360,470 430,540 360,540" fill="{BONE}" fill-opacity="0.18"/></g>{sp}
      <rect id="lidT" x="230" y="300" width="260" height="130" rx="8" fill="{DIM}"/>
      <rect id="lidB" x="230" y="650" width="260" height="130" rx="8" fill="{DIM}"/></svg>'''
    js='''document.getElementById('gem').setAttribute('transform','rotate('+(t*55)+' 360 555)');
    var sps=document.querySelectorAll('.sp');for(var i=0;i<sps.length;i++){var ang=(t*90+i*51)*Math.PI/180;var rad=95+18*Math.sin(t*3+i);
    sps[i].setAttribute('cx',360+rad*Math.cos(ang));sps[i].setAttribute('cy',555+rad*Math.sin(ang));
    sps[i].setAttribute('opacity',(0.4+0.6*Math.abs(Math.sin(t*4+i))).toFixed(2));}
    var c=Math.max(0,Math.min(1,(t-(DUR-1.7))/1.1));var e=1-Math.pow(1-c,3);
    document.getElementById('lidT').setAttribute('transform','translate(0,'+(e*130).toFixed(0)+')');
    document.getElementById('lidB').setAttribute('transform','translate(0,'+(-e*130).toFixed(0)+')');
    document.getElementById('gem').setAttribute('opacity',(1-0.9*c).toFixed(2));'''
    return doc(svg,js,dur)

# ---------- 4. false progress (fills, resets, loops) ----------
def progress(dur):
    import math
    r=140; circ=2*math.pi*r
    svg=f'''<svg viewBox="0 0 {W} {H}">
      <circle cx="360" cy="600" r="{r}" fill="none" stroke="{DIM}" stroke-width="18"/>
      <circle id="arc" cx="360" cy="600" r="{r}" fill="none" stroke="{CORAL}" stroke-width="18" stroke-linecap="round"
        stroke-dasharray="{circ:.1f}" stroke-dashoffset="{circ:.1f}" transform="rotate(-90 360 600)"/>
      <circle id="run" cx="360" cy="460" r="13" fill="{BONE}"/></svg>'''
    js=('var CIRC=__CIRC__;var cyc=2.1;var fr=(t-cyc*Math.floor(t/cyc))/cyc;'
        'document.getElementById("arc").setAttribute("stroke-dashoffset",(CIRC*(1-fr)).toFixed(1));'
        'var ang=(fr*360-90)*Math.PI/180;document.getElementById("run").setAttribute("cx",360+140*Math.cos(ang));'
        'document.getElementById("run").setAttribute("cy",600+140*Math.sin(ang));').replace("__CIRC__",f"{circ:.1f}")
    return doc(svg,js,dur)

# ---------- 5. seesaw (product <-> marketing) ----------
def seesaw(dur):
    svg=f'''<svg viewBox="0 0 {W} {H}">
      <g id="beam">
        <rect x="150" y="592" width="420" height="16" rx="8" fill="{BONE}"/>
        <circle id="oL" cx="170" cy="560" r="40" fill="{CORAL}"/>
        <circle id="oR" cx="550" cy="560" r="40" fill="{MINT}"/></g>
      <polygon points="360,600 320,700 400,700" fill="{DIM2}"/></svg>'''
    js='''var a=11*Math.sin((t-0.4)*1.15);if(t<0.4)a=0;
    document.getElementById('beam').setAttribute('transform','rotate('+a.toFixed(2)+' 360 600)');
    var gl=Math.max(0,Math.sin((t-0.4)*1.15)),gr=Math.max(0,-Math.sin((t-0.4)*1.15));
    document.getElementById('oL').setAttribute('r',(40+8*gl).toFixed(1));
    document.getElementById('oR').setAttribute('r',(40+8*gr).toFixed(1));'''
    return doc(svg,js,dur)

# ---------- 6. long slow line -> fast spinning loop ----------
def loop(dur):
    lt="".join(f'<circle class="lt" cx="{140+i*88}" cy="600" r="9" fill="{DIM2}"/>' for i in range(6))
    ct="".join(f'<circle class="ct" data-i="{i}" cx="360" cy="600" r="9" fill="{MINT}"/>' for i in range(4))
    svg=f'''<svg viewBox="0 0 {W} {H}">
      <g id="gLine"><line x1="140" y1="600" x2="580" y2="600" stroke="{DIM}" stroke-width="4"/>{lt}
        <circle id="ld" cx="140" cy="600" r="14" fill="{CORAL}"/></g>
      <g id="gCirc" opacity="0"><circle cx="360" cy="600" r="150" fill="none" stroke="{DIM}" stroke-width="4"/>{ct}
        <circle id="cd" cx="510" cy="600" r="14" fill="{CORAL}"/></g></svg>'''
    js='''var s=Math.max(0,Math.min(1,(t-3.0)/1.0));
    document.getElementById('gLine').setAttribute('opacity',(1-s).toFixed(2));
    document.getElementById('gCirc').setAttribute('opacity',s.toFixed(2));
    var fr=Math.max(0,Math.min(1,t/2.8));document.getElementById('ld').setAttribute('cx',(140+440*fr).toFixed(1));
    var cts=document.querySelectorAll('.ct');for(var i=0;i<cts.length;i++){var ang=(i*90-90)*Math.PI/180;
      cts[i].setAttribute('cx',360+150*Math.cos(ang));cts[i].setAttribute('cy',600+150*Math.sin(ang));}
    var la=((t-3.0)*300-90)*Math.PI/180;document.getElementById('cd').setAttribute('cx',360+150*Math.cos(la));
    document.getElementById('cd').setAttribute('cy',600+150*Math.sin(la));'''
    return doc(svg,js,dur)

# ---------- 7. the market votes (eyes open, fix on a trembling shape) ----------
def eyes(dur):
    import math
    n=14; ring=""
    for i in range(n):
        ang=i*(360/n)*math.pi/180; x=360+260*math.cos(ang); y=600+300*math.sin(ang)
        ring+=f'<circle class="eye" data-x="{x:.0f}" data-y="{y:.0f}" cx="{x:.0f}" cy="{y:.0f}" r="0" fill="{BONE}"/>'
        ring+=f'<line class="ray" x1="{x:.0f}" y1="{y:.0f}" x2="360" y2="600" stroke="{DIM2}" stroke-width="2" opacity="0"/>'
    svg=f'<svg viewBox="0 0 {W} {H}">{ring}<circle id="core" cx="360" cy="600" r="46" fill="{BONE}"/></svg>'
    js='''var eyes=document.querySelectorAll('.eye');for(var i=0;i<eyes.length;i++){var st=0.2+i*0.06;var p=Math.max(0,Math.min(1,(t-st)/0.4));
    eyes[i].setAttribute('r',(13*p).toFixed(1));}
    var look=Math.max(0,Math.min(1,(t-1.7)/0.7));document.querySelectorAll('.ray').forEach(function(r){r.setAttribute('opacity',(0.35*look).toFixed(2));});
    var core=document.getElementById('core');var jt=look*4*Math.sin(t*22);core.setAttribute('cx',(360+jt).toFixed(1));
    core.setAttribute('r',(46-18*look).toFixed(1));core.setAttribute('fill',look>0.5?'__CORAL__':'__BONE__');'''
    return doc(svg,js,dur)

# ---------- 8. waveform decays to a flatline (silence) ----------
def wave(dur):
    svg=f'''<svg viewBox="0 0 {W} {H}">
      <polyline id="wf" fill="none" stroke="{BONE}" stroke-width="5" stroke-linecap="round" points=""/>
      <circle id="blip" cx="360" cy="600" r="0" fill="{CORAL}"/></svg>'''
    js='''var A=46;if(t>1.9)A=46*Math.max(0,1-(t-1.9)/1.3);
    var pts="";for(var x=60;x<=660;x+=6){var y=600+A*Math.sin(x*0.05+t*7)*Math.exp(-Math.pow((x-360)/300,2)*0.2);pts+=x+","+y.toFixed(1)+" ";}
    document.getElementById('wf').setAttribute('points',pts);
    var b=0;if(t>3.5&&t<4.3){b=1-Math.abs((t-3.9)/0.4);}document.getElementById('blip').setAttribute('r',(Math.max(0,b)*16).toFixed(1));'''
    return doc(svg,js,dur)

# ---------- 9. take the reps (repeated launches, momentum) ----------
def reps(dur):
    tallies="".join(f'<rect class="tal" data-i="{i}" x="{200+i*30}" y="980" width="10" height="34" rx="3" fill="{BONE}" opacity="0"/>' for i in range(8))
    svg=f'''<svg viewBox="0 0 {W} {H}">
      <circle id="mom" cx="360" cy="600" r="60" fill="none" stroke="{DIM2}" stroke-width="4"/>
      <g id="plane"><polygon points="0,-20 16,14 0,4 -16,14" fill="{CORAL}"/></g>{tallies}</svg>'''
    js='''var repI=0.62;var idx=Math.floor(t/repI);var fr=t/repI-idx;
    var sx=360,sy=740;var ex=360+300*Math.cos(-1.05),ey=740+300*Math.sin(-1.05);
    var x=sx+(ex-sx)*fr, y=sy+(ey-sy)*fr;var op=Math.max(0,1-fr*0.9);
    var pl=document.getElementById('plane');pl.setAttribute('transform','translate('+x.toFixed(1)+','+y.toFixed(1)+') rotate(35) scale('+(1+idx*0.06)+')');
    pl.setAttribute('opacity',op.toFixed(2));
    var tal=document.querySelectorAll('.tal');for(var i=0;i<tal.length;i++){tal[i].setAttribute('opacity', (i<idx?1:0));}
    document.getElementById('mom').setAttribute('r',(60+idx*9).toFixed(0));
    document.getElementById('mom').setAttribute('opacity',(0.3+0.09*idx).toFixed(2));'''
    return doc(svg,js,dur)

SCENES={"gears":gears,"tower":tower,"gem":gem,"progress":progress,"seesaw":seesaw,
        "loop":loop,"eyes":eyes,"wave":wave,"reps":reps}
manifest=[]
for b in SB["beats"]:
    d=round(b["end"]-b["start"],3)
    (OUT/f"{b['id']}.html").write_text(SCENES[b["scene"]](d))
    manifest.append(f"{b['id']} {d}")
    print("wrote scene", b["id"], b["scene"])
(OUT/"manifest.txt").write_text("\n".join(manifest)+"\n")
