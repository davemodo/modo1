#!/bin/bash
# Reel #2 ("one idea -> a week of content"): generate animated mockups -> capture -> clips.
# Captured a little long (9.5s) so any beat length / split sub-shot fits.
set -e
cd "$(dirname "$0")"
python3 mockups/make_broll_week.py
mkdir -p build/broll_clips
for name in w1_voice w2_idea w3_week w4_schedule; do
  echo ">> $name"
  rm -rf build/_frames_$name
  node mockups/capture.js build/broll_anim/$name.html 9.5 30 build/_frames_$name
  ffmpeg -y -hide_banner -loglevel error -framerate 30 -i build/_frames_$name/f%04d.png \
    -c:v libx264 -pix_fmt yuv420p -preset medium -crf 18 build/broll_clips/$name.mp4
  rm -rf build/_frames_$name
done
echo "REEL #2 CLIPS DONE"
