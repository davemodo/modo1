#!/bin/bash
# Recreated "free AI study tool" reel: talking-head FORMAT with a dummy placeholder
# head (no HeyGen), original animated B-roll, serif chapter titles, captions, music+SFX.
# usage: ./render_study.sh [storyboard.json]
set -e
cd "$(dirname "$0")"
SB="${1:-storyboards/study.json}"
CHROME="${CHROME_PATH:-$(ls /opt/pw-browsers/chromium-*/chrome-linux/chrome 2>/dev/null | head -1)}"

python3 mockups/make_study.py            # writes build/broll_anim/{spark,m_notes,m_ai,m_guide,m_cards,head}.html
mkdir -p build/broll_clips

# dummy talking-head: static PNG -> 6s clip with a slow push-in
"$CHROME" --headless --no-sandbox --disable-gpu --screenshot=build/head.png --window-size=720,1280 build/broll_anim/head.html >/dev/null 2>&1
ffmpeg -nostdin -y -hide_banner -loglevel error -i build/head.png \
  -vf "scale=1440:-1,zoompan=z='min(1.0+0.0009*on,1.09)':d=180:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=720x1280:fps=30,trim=end_frame=180,setsar=1" \
  -frames:v 180 -r 30 -c:v libx264 -pix_fmt yuv420p -preset medium -crf 18 build/broll_clips/head.mp4

# animated mockups
declare -A D=( [spark]=2.4 [m_notes]=6 [m_ai]=6 [m_guide]=6 [m_cards]=6 )
for n in spark m_notes m_ai m_guide m_cards; do
  rm -rf build/_st_$n
  node mockups/capture.js build/broll_anim/$n.html "${D[$n]}" 30 build/_st_$n
  ffmpeg -nostdin -y -hide_banner -loglevel error -framerate 30 -i build/_st_$n/f%04d.png \
    -c:v libx264 -pix_fmt yuv420p -preset medium -crf 18 build/broll_clips/$n.mp4
  rm -rf build/_st_$n
done

python3 compose.py none build/reel_study.mp4 "$SB"
echo "DONE -> build/reel_study.mp4"
