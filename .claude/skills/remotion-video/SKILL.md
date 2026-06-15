---
name: remotion-video
description: Create programmatic videos with React using Remotion. Use when user asks to make videos, animations, motion graphics, product showcases, social media reels, animated infographics, or video content.
metadata:
  author: remotion-dev
  version: 1.0.0
  github: https://github.com/remotion-dev/remotion
  skills-repo: https://github.com/remotion-dev/skills
  docs: https://www.remotion.dev/docs
---

# Remotion Video Creation

## Installation
```bash
npx skills add remotion-dev/skills
npx create-video@latest --yes --blank --no-tailwind my-video
cd my-video && npm install
```

## Quick Commands
```bash
npx remotion studio                                # Preview
npx remotion still MyComp --scale=0.25 --frame=30  # Single frame test
npx remotion render MyComp out/video.mp4           # Full render
```

## Capabilities
- Programmatic video creation with React components, multiple compositions, dynamic metadata
- Zod-parametrized videos, still frame & transparent video rendering
- Animations: interpolation, springs, text effects, transitions, sequencing, Lottie, light leaks
- Media: video, audio, images, GIFs, fonts, FFmpeg integration
- Audio: visualization, sound effects, silence detection, AI voiceover (ElevenLabs)
- Data viz: charts, maps, 3D (Three.js / R3F)
- Rendering: MP4 export, server-side rendering, CLI rendering, Studio preview

## Rule Files (consult as needed)
`rules/animations.md`, `rules/audio.md`, `rules/charts.md`, `rules/3d.md`, `rules/video.md`, `rules/subtitles.md`, `rules/ffmpeg.md`, `rules/tailwind.md`, `rules/text-animations.md`, `rules/transitions.md`, `rules/voiceover.md`, `rules/sequencing.md`, `rules/maps.md`
