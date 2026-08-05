# Reference reel deconstruction

Findings from analyzing 6 competitor reels (frames, scene-cuts, and audio levels).
This is the template the pipeline reproduces.

## Format constants (identical across all 6 reels)

| Layer | Fixed recipe | Per-video input |
|---|---|---|
| Canvas | 720×1280, 9:16, 24–30fps | — |
| Structure | cold-open hook → body → talking-head CTA | script |
| Chapter titles | elegant **serif italic** (Playfair/Didone), centered upper third, fade per section | the words + color |
| Captions | **word-by-word**, bold sans (Montserrat), white on translucent dark pill, lower third | VO text |
| B-roll | screen/app content inside a rounded device frame with a **colored glow border**, slow push-in | screenshots + glow color |
| Color grade | dark (or white) bg with a **radial brand-color glow** tying scenes together | accent color |
| Presenter | tight close-up, mic in frame, soft key light, casual/UGC | avatar/person |
| Voice | single confident VO, ~140 wpm | script |
| Sound | continuous **music bed** under the VO, **mastered to ~−17 dB**, no silent gaps, whoosh on cuts | track |
| CTA | *"comment 'KEYWORD' and I'll DM/send you the link"* | keyword |

## Key insight
Across the 6 reels there are **two different presenters using the exact same
template** — which proves the style is a detachable *format*, not one person's
talent. That is precisely why it is reproducible, and why a HeyGen avatar drops
into the "presenter" slot with no loss of quality.

## What varies per video (the only real inputs)
`topic → script → accent glow color → B-roll content → CTA keyword`. Everything
else is baked template.

## Measurements that drove the pipeline defaults
- Vertical 720×1280, ~24–30fps, 20–57s.
- Audio: mean ≈ **−17 dB**, peaks near 0 dB, **zero silent gaps** → a music bed runs
  under the entire VO (compose.py masters to −14 LUFS for social, which lands ≈ −16.7 dB
  mean, matching the reference).
- Hard cuts every ~2–4s with soft whoosh transitions → the pipeline splits long beats
  and places a synthesized whoosh on every cut.

## How each layer maps to a tool
| Reel layer | Tool in this pipeline |
|---|---|
| Face + voice | HeyGen avatar (`create_video_from_avatar`), lip-synced |
| Word-by-word captions | forced to the VO's silence gaps → ASS/libass karaoke |
| Serif chapter titles | ASS/libass (Playfair Display italic) |
| Device-frame B-roll + push-in | original HTML mockups, Playwright deterministic capture |
| Brand glow / grade | baked into the mockups (radial amber) |
| Music bed + SFX | synthesized with ffmpeg (`make_audio.sh`) |
| Final assembly | `compose.py` (ffmpeg) — no manual timeline |
