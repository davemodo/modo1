#!/bin/bash
# Fully-visual reel (no talking head, no VO): build kinetic text-card clips + ensure
# B-roll clips exist, then composite with compose.py in no-avatar mode.
# usage: ./render_visual.sh [storyboard.json]
set -e
cd "$(dirname "$0")"
SB="${1:-storyboards/week_visual.json}"

# 1) B-roll clips (reuse the week mockups)
[ -f build/broll_clips/w4_schedule.mp4 ] || ./render_clips_week.sh

# 2) kinetic text cards -> clips
python3 mockups/make_text_cards.py "$SB"
mkdir -p build/text_clips
while read -r id d; do
  [ -z "$id" ] && continue
  echo ">> text card $id (${d}s)"
  rm -rf build/_ft_$id
  node mockups/capture.js build/text_cards/$id.html "$d" 30 build/_ft_$id
  ffmpeg -nostdin -y -hide_banner -loglevel error -framerate 30 -i build/_ft_$id/f%04d.png \
    -c:v libx264 -pix_fmt yuv420p -preset medium -crf 18 build/text_clips/$id.mp4
  rm -rf build/_ft_$id
done < build/text_cards/manifest.txt

# 3) composite (no avatar / no VO)
python3 compose.py none build/reel_visual.mp4 "$SB"
echo "DONE -> build/reel_visual.mp4"
