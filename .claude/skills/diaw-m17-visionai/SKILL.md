---
name: diaw-m17-visionai
description: >
  VISION-AI: AI-powered image generation and visual content module. Creates
  marketing images, product photography, social media visuals, infographics,
  presentation graphics, and brand-consistent visual content at scale.
  Integrates with Stable Diffusion, DALL-E, and Midjourney APIs. Activates on
  VISION-AI, image generation, AI images, visual content, product photography,
  infographics, marketing visuals, DALL-E, Midjourney.
user-invocable: true
context: fork
effort: high
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - WebSearch
  - mcp__ruflo__*
---

# VISION-AI: Image Generation Module v3.0

## Agent Swarm Configuration
- **Topology**: Broadcast | **Max Agents**: 3 | **Quality Gate**: 0.90
- **Agents**: Creative Director, Generation Agent, Post-Processing Agent

## Image Generation Stack

### Model Selection Matrix
| Model | Best For | Style | Speed | Cost |
|-------|----------|-------|-------|------|
| DALL-E 3 (via API) | Photorealistic, text in images | Versatile | Fast | $0.04-0.08/image |
| Stable Diffusion XL | Custom styles, fine-tuning | Artistic | Fast (local) | Compute cost |
| Midjourney v6 | Aesthetic, artistic quality | Stylized | Medium | $10-60/mo |
| Flux 1.1 Pro | Photorealistic humans, products | Photographic | Fast | $0.03-0.05/image |
| Adobe Firefly | Commercial-safe, brand-consistent | Clean | Fast | Adobe CC |

### Prompt Engineering Framework
```
[Subject] + [Style] + [Lighting] + [Camera/Angle] + [Background] + [Quality modifiers]

Example:
"Professional product photography of a sleek smartphone on a minimalist white surface,
studio lighting with soft shadows, shot from 45-degree angle, clean background,
ultra-detailed, 8K resolution, commercial photography"

Brand-consistent modifiers for DIAW:
  Colors: deep navy #1a1a2e, vibrant red #e94560
  Style: "modern tech aesthetic", "minimalist", "professional"
  Mood: "confident", "innovative", "trustworthy"
```

### Visual Content Categories

**Marketing Images**
- Hero banner images (LinkedIn, website, email)
- Ad creatives (Facebook/Instagram/Google Display)
- Product feature illustrations
- Team and culture photos (AI-generated scenarios)

**Social Media Visuals**
- LinkedIn carousels (10-slide educational series)
- Instagram posts and stories
- Twitter/X header images
- YouTube thumbnails

**Infographics**
- Data visualizations (charts → designed graphics)
- Process flows (step-by-step illustrated guides)
- Comparison tables (styled for marketing use)
- Statistical highlights (key numbers highlighted)

**Brand Collateral**
- Trade show booth graphics
- Event backdrop designs
- Business card designs
- Presentation backgrounds

### Arabic Visual Design
- RTL-compatible image compositions
- Arabic calligraphy integration
- Islamic geometric patterns for decorative elements
- UAE landmarks and skyline incorporation (Dubai, Abu Dhabi)
- Culturally appropriate imagery (modest representation)

### Batch Generation Workflow
```python
# Generate 20 social media images in one command
python generate_batch.py \
  --prompt-template "social-media-linkedin" \
  --brand-kit diaw-brand-kit.json \
  --count 20 \
  --model flux-1.1-pro \
  --output ./output/social-batch/
```

### Copyright & Commercial Safety
- All generated images are commercial-use safe
- No training data from copyrighted sources (when using compliant models)
- Watermark removal and upscaling included
- IP-safe brand element generation

## Revenue Model
- **Subscription**: $100/mo (500 images/mo included)
- **Additional Images**: $0.10-$0.25 per image beyond plan
- **Brand Pack**: $500 one-time for custom style fine-tuning
- **Credits**: 10-40 per bulk generation job

## Example Invocations
- "VISION-AI: Generate 20 LinkedIn post images for our DIAW platform features"
- "Create a hero image for our landing page — navy blue, tech aesthetic, UAE skyline"
- "VISION-AI: Build a 10-slide visual carousel explaining how our agent swarms work"
