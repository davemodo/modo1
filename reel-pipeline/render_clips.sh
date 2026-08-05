#!/bin/bash
# Reel #1 ("document your process"): generate animated mockups -> capture -> clips.
set -e
cd "$(dirname "$0")"
python3 mockups/make_broll_anim.py
mkdir -p build/broll_clips
declare -A DUR=( [m1_freeze]=4.7 [m2_record]=9.1 [m3_ai]=5.6 [m4_steps]=4.9 )
for name in m1_freeze m2_record m3_ai m4_steps; do
  echo ">> $name (${DUR[$name]}s)"
  rm -rf build/_frames_$name
  node mockups/capture.js build/broll_anim/$name.html "${DUR[$name]}" 30 build/_frames_$name
  ffmpeg -y -hide_banner -loglevel error -framerate 30 -i build/_frames_$name/f%04d.png \
    -c:v libx264 -pix_fmt yuv420p -preset medium -crf 18 build/broll_clips/$name.mp4
  rm -rf build/_frames_$name
done
echo "REEL #1 CLIPS DONE"
