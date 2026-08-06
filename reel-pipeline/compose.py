#!/usr/bin/env python3
"""Composite pass v2: avatar + ANIMATED B-roll clips + serif titles + karaoke captions
+ music bed + SFX (whoosh on cuts, pops on element reveals) -> finished 9:16 reel.

Upgrades over v1:
  * pacing  : long beats are split into sub-shots; talking-head gets a gentle push-in
  * sound   : synthesized whoosh on every cut, soft pops on checklist reveals, a riser hook
  * motion  : B-roll comes from pre-rendered animated clips (build/broll_clips/*.mp4)

Usage: python3 compose.py AVATAR_MP4 [OUT_MP4]
"""
import json, subprocess, sys, pathlib

ROOT = pathlib.Path(__file__).parent
FONTS = ROOT / "fonts"
CLIPS = ROOT / "build" / "broll_clips"
TEXT_CLIPS = ROOT / "build" / "text_clips"   # kinetic text cards (no-VO visual reels)
BRAND_SLIDES = ROOT / "build" / "brand_slides"  # full-frame brand slides (brand mode)
MOTION_SLIDES = ROOT / "build" / "motion_slides"  # full-frame motion-graphics scenes (motion mode)
MUSIC = ROOT / "assets" / "music_bed.wav"
SFX = ROOT / "sfx"
WORK = ROOT / "build" / "work"; WORK.mkdir(parents=True, exist_ok=True)

AVATAR = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "build" / "avatar.mp4"
OUT = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "build" / "final_reel.mp4"
SB_PATH = pathlib.Path(sys.argv[3]) if len(sys.argv) > 3 else ROOT / "storyboards" / "process.json"
SB = json.loads(SB_PATH.read_text())
M = SB["meta"]; W, H, FPS = M["width"], M["height"], M["fps"]

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(" ".join(map(str, cmd))[:400] + "\n" + r.stderr[-1800:] + "\n"); raise SystemExit(1)
    return r.stdout

def dur(p): return float(run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(p)]).strip())

beats = [dict(b) for b in SB["beats"]]
BRAND = M.get("mode") == "brand"          # every beat is a full-frame brand slide
MOTION = M.get("mode") == "motion"        # every beat is a full-frame motion-graphics scene
SLIDES = BRAND or MOTION                  # all beats come from a pre-rendered full-frame clip dir
SLIDES_DIR = BRAND_SLIDES if BRAND else MOTION_SLIDES
CAPTIONS = M.get("captions", not SLIDES)   # slide modes default off, but a storyboard may opt in
AUDIO = M.get("audio", True) and not SLIDES
NO_AVATAR = (SLIDES or str(AVATAR).lower() in ("none", "-") or M.get("mode") == "no_avatar"
             or not any(b["type"] == "avatar" for b in beats))
if NO_AVATAR:
    # Fully visual reel: no talking head, no VO. Beat timings are authored as-is.
    real = beats[-1]["end"]
    print(f"visual reel (no avatar/VO)  total={real:.2f}s")
else:
    real = dur(AVATAR)
    k = real / beats[-1]["end"]
    for b in beats: b["start"] *= k; b["end"] *= k
    beats[-1]["end"] = real
    print(f"voiceover={real:.2f}s scale={k:.3f}")

# ---------- shot plan (drives the video track + cut list) ----------
FADE = 0.0 if SLIDES else 0.08   # slide modes bake their own in/out fades -> hard cuts
shots, cuts = [], []
for b in beats:
    length = b["end"] - b["start"]
    if SLIDES:
        shots.append({"kind":"clip","src":SLIDES_DIR / f"{b['id']}.mp4","in":0.0,"len":length,"zoom":1.0,"yf":0.5})
    elif b["type"] == "avatar":
        shots.append({"kind":"avatar","in":b["start"],"len":length,"push":True})
    elif b["type"] == "text":
        shots.append({"kind":"clip","src":TEXT_CLIPS / f"t{b['id']}.mp4","in":0.0,"len":length,"zoom":1.0,"yf":0.5})
    else:
        clip = CLIPS / f"{b['asset']}.mp4"
        # pacing: split a long beat (flag it with "split": true) into wide -> zoomed sub-shots
        if b.get("split") and length > 6:
            half = length/2
            shots.append({"kind":"clip","src":clip,"in":0.0,"len":half,"zoom":1.0,"yf":0.5})
            shots.append({"kind":"clip","src":clip,"in":half,"len":length-half,"zoom":1.34,"yf":0.64})
        else:
            shots.append({"kind":"clip","src":clip,"in":0.0,"len":length,"zoom":1.0,"yf":0.5})
# cut times = cumulative shot starts (skip 0)
acc = 0.0
for s in shots:
    if acc > 0.01: cuts.append(acc)
    acc += s["len"]

# ---------- render each shot ----------
segs = []
for i, s in enumerate(shots):
    seg = WORK / f"seg_{i:02d}.mp4"; L = s["len"]
    fade = ([f"fade=t=in:st=0:d={FADE}", f"fade=t=out:st={max(0,L-FADE):.3f}:d={FADE}"] if FADE > 0 else [])
    if s["kind"] == "avatar":
        # Gentle push-in via a moving crop window (fast; zoompan-on-video is pathologically slow).
        zf = 1.06
        filt = [f"scale={W}:{H}:force_original_aspect_ratio=increase", f"crop={W}:{H}", "setsar=1",
                f"scale=iw*{zf}:ih*{zf}",
                f"crop={W}:{H}:x='(iw-{W})/2':y='(ih-{H})*(0.5 - 0.12*min(1,t/{max(L,0.1):.3f}))'",
                *fade, f"fps={FPS}"]
        src = AVATAR
    else:
        filt = []
        if s["zoom"] > 1.001:
            filt += [f"scale=iw*{s['zoom']}:ih*{s['zoom']}", f"crop={W}:{H}:x=(iw-{W})/2:y=(ih-{H})*{s['yf']}", "setsar=1"]
        filt += [*fade, f"fps={FPS}"]
        src = s["src"]
    run(["ffmpeg","-y","-hide_banner","-loglevel","error","-ss",str(s["in"]),"-t",str(L),
         "-i",str(src),"-an","-vf",",".join(filt),"-r",str(FPS),
         "-c:v","libx264","-pix_fmt","yuv420p","-preset","veryfast",str(seg)])
    segs.append(seg)

cl = WORK / "concat.txt"; cl.write_text("".join(f"file '{s}'\n" for s in segs))
video_track = WORK / "video_track.mp4"
run(["ffmpeg","-y","-hide_banner","-loglevel","error","-f","concat","-safe","0","-i",str(cl),
     "-c:v","libx264","-pix_fmt","yuv420p","-preset","veryfast",str(video_track)])

# ---------- captions layer (optional) ----------
video_final = video_track   # video source going into the mux
if CAPTIONS:
    def ts(t):
        cs=int(round(t*100)); h=cs//360000; cs%=360000; m=cs//6000; cs%=6000; s=cs//100; cs%=100
        return f"{h}:{m:02d}:{s:02d}.{cs:02d}"
    def chunks(text,n=2):
        w=text.replace("—","-").split(); return [" ".join(w[i:i+n]) for i in range(0,len(w),n)]
    ass = WORK/"reel.ass"
    CAP_MV = M.get("caption_marginv", 235)   # distance of the caption pill from the bottom
    TITLE_COL = M.get("title_colour", "&H00FFFFFF")     # serif chapter-title fill (ASS &HAABBGGRR)
    TITLE_OUT = M.get("title_outline", "&H64000000")    # its outline colour
    head=f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Title,Playfair Display,58,{TITLE_COL},&H00FFFFFF,{TITLE_OUT},&H00000000,-1,-1,0,0,100,100,0,0,1,2,4,8,60,60,150,1
Style: Cap,Montserrat,44,&H00FFFFFF,&H00FFFFFF,&H00101010,&H90101010,-1,0,0,0,100,100,0.4,0,3,10,0,2,80,80,{CAP_MV},1
"""
    ev=["[Events]","Format: Layer, Start, End, Style, MarginL, MarginR, MarginV, Effect, Text"]
    for b in beats:
        if b.get("type") == "text":
            continue  # kinetic text card carries its own words
        if b.get("title"):
            ev.append(f"Dialogue: 0,{ts(b['start']+0.05)},{ts(b['end'])},Title,0,0,0,,{{\\fad(280,240)}}{b['title']}")
        cap = b.get("caption")
        if cap:
            cs = chunks(cap, 3 if NO_AVATAR else 2)
            span=(b["end"]-b["start"])/len(cs)
            for i,c in enumerate(cs):
                st=b["start"]+i*span
                ev.append(f"Dialogue: 1,{ts(st)},{ts(st+span)},Cap,0,0,0,,{{\\fad(60,60)}}{c.replace('{','(').replace('}',')')}")
    ass.write_text(head+"\n".join(ev)+"\n")
    subs=str(ass).replace(":",r"\:").replace(",",r"\,"); fdir=str(FONTS).replace(":",r"\:").replace(",",r"\,")
    vsub=WORK/"video_subbed.mp4"
    run(["ffmpeg","-y","-hide_banner","-loglevel","error","-i",str(video_track),
         "-vf",f"subtitles={subs}:fontsdir={fdir}","-an",
         "-c:v","libx264","-pix_fmt","yuv420p","-preset","veryfast","-crf","20","-r",str(FPS),str(vsub)])
    video_final = vsub

# ---------- audio layer (optional) ----------
mixaudio = None; pops = []
if AUDIO:
    for b in beats:
        for i in range(b.get("reveal_pops", 0)):
            pops.append(b["start"]+0.35+i*0.55)
        if b.get("send_pop"):
            pops.append(b["start"]+2.35)
    def delayed(idx,t,vol):
        ms=max(0,int(t*1000)); return f"[{idx}:a]adelay={ms}|{ms},volume={vol}[s{len(branches)}]"
    branches=[]; labels=[]
    for c in cuts:
        st=max(0.0,c-0.12); branches.append(delayed(0,st,1.0)); labels.append(f"[s{len(branches)-1}]")
    for p in pops:
        branches.append(delayed(1,p,0.9)); labels.append(f"[s{len(branches)-1}]")
    if cuts:
        branches.append(delayed(2,max(0.0,cuts[0]-0.9),0.7)); labels.append(f"[s{len(branches)-1}]")
    sfx_bed = WORK/"sfx_bed.wav"
    fc = ";".join(branches)+";"+"".join(labels)+f"amix=inputs={len(labels)}:normalize=0:dropout_transition=0,volume=0.9[sf]"
    run(["ffmpeg","-y","-hide_banner","-loglevel","error",
         "-i",str(SFX/"whoosh.wav"),"-i",str(SFX/"pop.wav"),"-i",str(SFX/"riser.wav"),
         "-filter_complex",fc,"-map","[sf]",str(sfx_bed)])
    have_a=(not NO_AVATAR) and bool(run(["ffprobe","-v","error","-select_streams","a","-show_entries","stream=codec_type","-of","csv=p=0",str(AVATAR)]).strip())
    mixaudio=WORK/"mixaudio.wav"
    if have_a:
        afc=("[1:a]aformat=sample_rates=44100:channel_layouts=stereo,volume=1.0[vo];"
             "[0:a]aformat=sample_rates=44100:channel_layouts=stereo,volume=0.20[mus];"
             "[2:a]aformat=sample_rates=44100:channel_layouts=stereo,volume=0.55[sfx];"
             "[vo][mus][sfx]amix=inputs=3:duration=first:dropout_transition=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]")
        ain=["-i",str(MUSIC),"-i",str(AVATAR),"-i",str(sfx_bed)]
    else:
        afc=("[0:a]volume=0.5[mus];[2:a]volume=0.6[sfx];[mus][sfx]amix=inputs=2:duration=longest,loudnorm=I=-15:TP=-1.5[a]")
        ain=["-stream_loop","-1","-i",str(MUSIC),"-i",str(MUSIC),"-i",str(sfx_bed)]
    run(["ffmpeg","-y","-hide_banner","-loglevel","error",*ain,"-filter_complex",afc,"-map","[a]","-t",str(real),str(mixaudio)])

# ---------- mux ----------
if mixaudio:
    run(["ffmpeg","-y","-hide_banner","-loglevel","error","-i",str(video_final),"-i",str(mixaudio),
         "-map","0:v","-map","1:a","-c:v","copy","-c:a","aac","-b:a","192k","-t",str(real),str(OUT)])
else:
    run(["ffmpeg","-y","-hide_banner","-loglevel","error","-i",str(video_final),
         "-an","-c:v","copy","-t",str(real),str(OUT)])
print("WROTE",OUT,f"{dur(OUT):.2f}s  brand={BRAND} captions={CAPTIONS} audio={AUDIO}")
