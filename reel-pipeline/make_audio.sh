#!/bin/bash
# Regenerate all audio (100% synthesized with ffmpeg — no third-party samples).
# Outputs: assets/music_bed.wav, sfx/whoosh.wav, sfx/pop.wav, sfx/riser.wav
set -e
cd "$(dirname "$0")"
mkdir -p assets sfx

# Ambient music bed (~40s): four detuned sine partials -> tremolo -> low-pass -> echo.
ffmpeg -y -hide_banner -loglevel error \
 -f lavfi -i "sine=frequency=110:duration=40" \
 -f lavfi -i "sine=frequency=164.81:duration=40" \
 -f lavfi -i "sine=frequency=220:duration=40" \
 -f lavfi -i "sine=frequency=277.18:duration=40" \
 -filter_complex "[0][1][2][3]amix=inputs=4:normalize=0,tremolo=f=0.18:d=0.35,lowpass=f=760,aecho=0.8:0.75:120:0.28,volume=0.32,afade=t=in:st=0:d=2,afade=t=out:st=37:d=3" \
 assets/music_bed.wav

# Whoosh (transition): pink noise -> band-pass -> swell envelope.
ffmpeg -y -hide_banner -loglevel error -f lavfi -i "anoisesrc=color=pink:d=0.5:amplitude=0.7" \
 -af "bandpass=f=1400:width_type=o:w=2.2,afade=t=in:st=0:d=0.10:curve=exp,afade=t=out:st=0.18:d=0.30,volume=1.6" sfx/whoosh.wav

# Pop / tick (element reveal): short sine blip, fast decay.
ffmpeg -y -hide_banner -loglevel error -f lavfi -i "sine=f=740:d=0.14" \
 -af "afade=t=out:st=0.012:d=0.12:curve=exp,volume=0.45" sfx/pop.wav

# Riser (into first cut): rising brown noise.
ffmpeg -y -hide_banner -loglevel error -f lavfi -i "anoisesrc=color=brown:d=0.9:amplitude=0.5" \
 -af "highpass=f=200,lowpass=f=4000,volume='min(1,t*1.1)':eval=frame,afade=t=out:st=0.75:d=0.15,volume=0.8" sfx/riser.wav

echo "audio regenerated: assets/music_bed.wav + sfx/{whoosh,pop,riser}.wav"
