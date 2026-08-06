#!/bin/bash
# Globalmodo BRAND reel (silent, no captions): render every brand slide -> clip -> composite.
# usage: ./render_brand.sh [storyboard.json]
set -e
cd "$(dirname "$0")"
SB="${1:-storyboards/week_brand.json}"
python3 mockups/make_brand.py "$SB"
mkdir -p build/brand_slides
while read -r id d; do
  [ -z "$id" ] && continue
  echo ">> brand slide $id (${d}s)"
  rm -rf build/_bs_$id
  node mockups/capture.js build/brand_slides/$id.html "$d" 30 build/_bs_$id
  ffmpeg -nostdin -y -hide_banner -loglevel error -framerate 30 -i build/_bs_$id/f%04d.png \
    -c:v libx264 -pix_fmt yuv420p -preset medium -crf 18 build/brand_slides/$id.mp4
  rm -rf build/_bs_$id
done < build/brand_slides/manifest.txt
python3 compose.py none build/reel_brand.mp4 "$SB"
echo "DONE -> build/reel_brand.mp4"
