# Modo — AI Reel Generation Pipeline

Generate vertical (9:16) short-form reels in the style of the reference competitor
reels, **fully with AI and zero manual editing**. A talking-head avatar (HeyGen)
carries the voiceover; everything else — animated B-roll mockups, serif chapter
titles, word-by-word captions, brand glow, music bed and SFX — is generated and
composited programmatically.

See **[ANALYSIS.md](./ANALYSIS.md)** for the deconstruction of the reference reels
that this pipeline reproduces.

---

## How it works

```
topic ─▶ script ─▶ [HeyGen] avatar clip (face + voice, lip-synced)
                          │
storyboard.json ──────────┼─▶ beat timings snapped to the VO's real pauses
                          │
mockups (HTML+JS) ─▶ [Playwright] deterministic frames ─▶ animated B-roll clips
                          │
                          ▼
                    compose.py  ──▶  final_reel.mp4
       (avatar + B-roll + serif titles + karaoke captions + glow + music + SFX)
```

The **only per-reel inputs** are: a script, a `storyboard.json`, and a set of
mockups. Everything else (fonts, glow, caption engine, music, SFX, master levels)
is fixed template — that is what makes the output consistent with zero editing.

### Why mockups instead of AI-generated B-roll
The two recurring failure modes with AI B-roll are (1) misaligned/warped assets
and (2) visuals that don't match the script. Here every B-roll shot is an
**original HTML mockup pinned to one script line**, captured deterministically —
so the picture can never drift from the words, and there is no third-party
footage to license.

---

## Layout

```
reel-pipeline/
  compose.py              # the composite engine (avatar + B-roll + titles + captions + audio)
  mockups/
    make_broll_anim.py    # reel #1 mockups (blank doc / recorder / AI chat / checklist)
    make_broll_week.py    # reel #2 mockups (voice profile / one idea / week cards / scheduler)
    capture.js            # Playwright deterministic frame capture (renderAt(t) -> frames)
  render_clips.sh         # reel #1: generate mockups -> capture -> clips
  render_clips_week.sh    # reel #2: generate mockups -> capture -> clips
  make_audio.sh           # regenerate the (synthesized) music bed + SFX
  storyboards/
    process.json          # reel #1 storyboard
    week.json             # reel #2 storyboard
  fonts/                  # Playfair Display (titles) + Montserrat (captions/UI) — OFL
  sfx/                    # whoosh / pop / riser  (synthesized)
  assets/music_bed.wav    # ambient bed          (synthesized)
  build/                  # runtime working dir (gitignored)
```

## Requirements
- `ffmpeg` / `ffprobe`
- `python3`
- `node` + `npm install` (Playwright; uses the pre-installed Chromium via
  `PLAYWRIGHT_BROWSERS_PATH`, or set `CHROME_PATH`)

## Run a reel

```bash
npm install                      # once
./make_audio.sh                  # once (or whenever you retune the sound)

# 1) B-roll clips for the reel you want
./render_clips_week.sh           # -> build/broll_clips/w*.mp4

# 2) render the avatar on HeyGen with the reel's script, download the MP4 to build/avatar.mp4
#    (the voice carries the whole VO; B-roll overlays it on demo beats)

# 3) composite:  compose.py  AVATAR_MP4  OUT_MP4  STORYBOARD
python3 compose.py build/avatar.mp4 build/reel2.mp4 storyboards/week.json
```

`compose.py` reads the avatar's real duration and **scales/snaps every beat
boundary to the measured silence gaps in the voiceover**, so visuals stay locked
to the script regardless of small VO length differences.

## Storyboard format
Each beat: `type` (`avatar` | `broll`), `start`/`end` (seconds; estimates are fine —
they get snapped to the VO), `title` (serif chapter title, optional), `caption`
(word-by-word karaoke text). Optional flags:
- `"split": true` — split a long (>6s) B-roll beat into a wide → zoomed sub-cut (pacing)
- `"reveal_pops": N` — N soft "pop" SFX on staggered element reveals (e.g. checklist)
- `"send_pop": true` — a single "sent" tick

## Notes / known constraints
- **HeyGen egress**: some networks block `files2.heygen.ai`; if the sandbox can't
  download the render, fetch it from the HeyGen video page and drop it at
  `build/avatar.mp4`.
- **HeyGen credits**: Avatar IV has a monthly minute cap; Avatar III needs paid
  credits. Pick an engine you have quota for when rendering.
- **ffmpeg gotchas encoded here** (already handled in `compose.py`): don't combine
  `subtitles` (libass) with `amix` in one filtergraph (threading stall — stages are
  separated); don't drive `zoompan` from a looped image or on video (pathologically
  slow — B-roll push-in is baked into the mockups, talking-head uses a moving crop).

## Licensing
Fonts are Google Fonts under the SIL Open Font License. Music and SFX are
synthesized here (no third-party samples). Mockups are original.
```
