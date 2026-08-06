#!/bin/bash
# Pure motion-graphics reel (no text, no brand): render each scene -> clip -> composite.
# usage: ./render_motion.sh [storyboard.json]
set -e
cd "$(dirname "$0")"
SB="${1:-storyboards/motion_labor.json}"
python3 mockups/make_motion.py "$SB"
mkdir -p build/motion_slides
while read -r id d; do
  [ -z "$id" ] && continue
  echo ">> motion scene $id (${d}s)"
  rm -rf build/_ms_$id
  node mockups/capture.js build/motion_slides/$id.html "$d" 30 build/_ms_$id
  ffmpeg -nostdin -y -hide_banner -loglevel error -framerate 30 -i build/_ms_$id/f%04d.png \
    -c:v libx264 -pix_fmt yuv420p -preset medium -crf 18 build/motion_slides/$id.mp4
  rm -rf build/_ms_$id
done < build/motion_slides/manifest.txt
python3 compose.py none build/reel_motion.mp4 "$SB"
echo "DONE -> build/reel_motion.mp4"
