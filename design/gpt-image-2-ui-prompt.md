# GPT Image 2 UI Reference Prompt

Use case: ui-mockup
Asset type: high-fidelity desktop reference for a research engineer portfolio
Primary request: Design a polished personal portfolio for a computer science researcher working on language agents, multi-agent systems, and evaluation. The page must feel like a precise field notebook and evidence ledger, not a startup landing page.
Scene/backdrop: full-width browser viewport, bright cool-neutral background, real portrait photography used as the first-viewport background with text over negative space
Style/medium: editorial research portfolio, Swiss information design, restrained industrial details, production-ready web UI
Composition/framing: 16:9 desktop screenshot; compact sticky navigation; first viewport shows the literal name "Bowei Xia", short research statement, Paper / Code / CV commands, and a visible hint of the next evidence section; below it show selected research, open-source work, and a compact dated timeline
Color palette: deep charcoal, clean white, cool gray, teal green, vermilion accent, restrained cobalt blue; no purple and no beige-dominant palette
Typography: distinctive editorial serif for the name paired with a clean grotesk body; no oversized marketing headline
Text (verbatim): "Bowei Xia"; "Language agents · Multi-agent systems · Evaluation"; "Selected evidence"; "Publications"; "Open source"; "CV"; "For agents"
Constraints: 8px maximum card radius; no cards inside cards; dense but calm information hierarchy; accessible contrast; familiar icons only; stable responsive dimensions; real data-oriented page rather than feature marketing
Avoid: gradients, decorative blobs, glassmorphism, purple palettes, dark navy dashboard styling, beige editorial styling, giant empty hero, split hero card, fake charts, testimonials, pricing, stock-photo atmosphere, illegible generated body copy, watermark

Intended CLI command once `OPENAI_API_KEY` is available:

```bash
python "$HOME/.codex/skills/.system/imagegen/scripts/image_gen.py" generate \
  --model gpt-image-2 \
  --prompt-file design/gpt-image-2-ui-prompt.md \
  --use-case ui-mockup \
  --quality high \
  --size 2048x1152 \
  --out design/gpt-image-2-portfolio-reference.png
```
