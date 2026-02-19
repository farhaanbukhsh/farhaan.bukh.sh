# Prompt Log

Chronological record of user prompts accepted in this project.

## 2026-02-18 15:03 IST — Project Brief
```
You are a website designer and developer plan to build a website for me, my current website https://farhaan.me/ which is outdated, I want a simple webiste which has a
link to my social, my blog and resume. I want to host this on github pages and need to add a workflow to  deploy this website. The website should also have a page to link
to all the talks that presented. The website needs to have a minecraft like theme in the background the colours being used, with a hint of hitchhikers guide to the galaxy.
You can ask me follow-up questions, make sure the plan is compatible for a ai agent to execute.
```

## 2026-02-18 15:20 IST — Repo & Domain Clarification
```
I answered your questions in the following way:

Q: Do you already have a GitHub repo to use, or should I initialize a new one?
A: I will need a new github repo which I can initialize. you need to just create a local directory which can be pushed.

Q: Do you have existing DNS/Pages config info for the desired custom domain setup (currently farhaan.me)?
> Desired custom domain setup is currently farhaan.me.
A: new domain will be farhaan.bukh.sh
```

## 2026-02-18 15:32 IST — Content & Assets Direction
```
Most of the socials are present at farhaan.me, create placeholder for the talk, make sure it's a markdown file so that I can update it easily which then translates in the webpage. Develop the hexcode from scratch and research I will approve them on reviewing it, let's try out different fonts as well. Right now I just want my picture to be used as avatar
```

## 2026-02-18 16:10 IST — Font Preference & Agent Docs
```
I like the sleek font better lets keep that. Also create a agents.md file which should have all the build steps for helping agents. Create a prompt.md file as well which should have the prompts accepted till now.
```

## 2026-02-18 16:25 IST — Remove Font Toggle
```
Remove the font toggle and make sleek as the defualt font, update agents.md and prompts.md for the same.
```

## 2026-02-18 16:45 IST — Python Build Pipeline Plan
```
Read the agents.md file and prompts.md file to get the context of the website. Don't make any changes now, I want you to plan the website such a way that all the styling and html remains the same but I am going to customize the data through markdown file. I don't want to use markdown.js library instead we can write python scripts which consumes these markdown files and build the website. Use virtualenv and use uv for dependency management.
```
**Outcome**: Plan only — no files changed. Proposed converting the site from client-side JS markdown rendering to a build-time Python pipeline (uv + jinja2 + markdown + pyyaml). Content moves to `content/` markdown files, templates to `templates/`, build output to `dist/`. GitHub Actions workflow to be updated to run `uv sync` + `build.py` and deploy `dist/`.

## 2026-02-18 17:00 IST — Add Justfile & Update Docs
```
Add creating a justfile and using just to build. Update the prompts.md and agents.md for the this and previous plan.
```
**Outcome**: Created `justfile` with recipes (setup, build, serve, dev, clean, check). Updated `agents.md` to reflect the full planned architecture (Python build, uv, just, content/, templates/, dist/). Updated `prompt.md` (this file) with both prompts.

## 2026-02-18 17:15 IST — Execute the Plan
```
execute the plan
```
**Outcome**: Full migration executed:
- `uv init` + added jinja2/pyyaml/markdown deps → `uv sync` created venv.
- Created `content/index.md` (YAML frontmatter with all home page data) and `content/talks.md` (moved from root).
- Created Jinja2 templates: `templates/base.html`, `templates/index.html`, `templates/talks.html` — extracted from the original static HTML, identical visual output.
- Wrote `build.py` — parses frontmatter, renders markdown, fills templates, copies assets+CNAME to `dist/`.
- `just build` + `just check` pass successfully, `dist/` contains pixel-identical HTML.
- Removed old files: root `index.html`, `talks.html`, `talks.md`, `assets/js/talks.js`.
- Updated `.github/workflows/deploy.yml` to install uv + just, run `just build`, deploy `dist/`.
- Updated `README.md`, `agents.md`, `prompt.md`.

## 2026-02-18 17:30 IST — Remove Talks Preview from Home
```
remove the talk and workshop section from the front page run the changes before making it.
```
**Outcome**: Removed the `talks-preview` section from `templates/index.html`, dropped the three `talks_preview_*` frontmatter fields from `content/index.md`, and cleaned up the corresponding render args in `build.py`. Rebuilt with `just clean && just build && just check` — all passing, section confirmed absent from `dist/index.html`. Talks page (`talks.html`) and nav link remain intact.

## 2026-02-18 17:50 IST — Minecraft Inventory Tray for Signal Relays
```
I need to change the signal relay section to look like an item selection tray where each item is the card displaying it. Use icons for each of the sections in the minecraft pixelated way. The tray will open when the user click a button, which has the mincraft sword icon.
```
**Outcome**: Replaced the card grid with a Minecraft-style inventory UI:
- Created 9 pixel-art SVG icons (`assets/img/icons/`): sword (toggle button), book (blog), scroll (resume), pickaxe (GitHub), feather (Twitter), diamond (LinkedIn), redstone (Stack Overflow), envelope (email), disc (talks). Generated via a temporary Python script using 16×16 grids.
- Added `icon` field to each link in `content/index.md`.
- Rewrote the links section in `templates/index.html` as a sword-button → overlay → inventory tray with slotted grid.
- Added full inventory CSS to `assets/css/style.css`: Minecraft beveled borders (`#c6c6c6` stone panel, `#8b8b8b` slots, 3D border colors), floating sword animation, overlay backdrop, responsive 2-column on mobile.
- Updated `assets/js/main.js` with open/close/ESC/backdrop-click handlers for the tray overlay.
- Build passes: `just clean && just build && just check` all green.

## 2026-02-19 00:00 IST — Remove Signal Relay nav, hero CTAs/meta, and center avatar
```
Plan to remove the "Signal Relay" from the header, the next set of tasks are 1. Remove Open Comms and View talks button. 2. Remove "Now", "Previous" and "Keyword Section". 3. Move the Picture and tag, to the center just above "I'm Farhaan" para.
```
**Outcome**:
- Removed “Signal relays” link from the header nav.
- Removed hero CTAs (Open comms, View talks) and meta list (Now/Previously/Keywords) from `templates/index.html`; removed meta/cta entries from `content/index.md`.
- Reflowed hero to a single stacked column: eyebrow → centered avatar + status chip → headline → paragraph. Updated CSS for center layout.
- Rebuilt: `just clean && just build && just check` (all green).

## 2026-02-19 00:30 IST — Minecraft backdrop items
```
Plan to add minecraft item in the backdrop of the website, like minecraft flowers, tnt, axe etc.
```
**Outcome**:
- Created 8 new 16×16 pixel-art SVGs in `assets/img/icons/`: flower (red poppy), tnt, axe (iron), grass-block, creeper (face), potion (purple bottle), heart, star.
- Added a `<div class="backdrop-items">` layer in `templates/base.html` containing 18 `<img>` elements (mix of new + existing icons), all `aria-hidden="true"`.
- Added CSS in `assets/css/style.css`: `.backdrop-items` is fixed fullscreen, z-index: -1, pointer-events: none. Each `.backdrop-item--N` (1–18) is absolutely positioned with unique top/left/right, width (34–56px), rotation via `--rot` custom property, and staggered `animation-delay` on a gentle `backdrop-float` keyframe (translateY ±10px, 10s infinite alternate). Opacity set to 0.07 for subtlety.
- 9 of 18 items hidden on mobile (<640px) to reduce clutter.
- No JS needed — pure CSS animations with `will-change: transform` for GPU compositing.
- Updated `agents.md` (repo layout, backdrop docs, QA checklist).
- Rebuilt: `just clean && just build && just check` (all green).

## 2026-02-19 01:00 IST — Backdrop items visibility & colour pop
```
Bring them in front so that they are visible and their colour pops
```
**Outcome**:
- Changed `.backdrop-items` z-index from `-1` to `0` so items render in front of the background.
- Increased `.backdrop-item` opacity from `0.07` to `0.35`.
- Added `filter: saturate(1.6) brightness(1.3) drop-shadow(0 0 6px rgba(255,255,255,0.15))` for vivid colours and subtle glow.
- Rebuilt: `just clean && just build && just check` (all green).

## 2026-02-19 01:15 IST — Inventory button: 3D wooden box look
```
Plan to make the Open Inventory button stand out, it should have the wooden box look and 3d visual.
```
**Outcome**:
- Restyled `.inventory-toggle` as a raised wooden block: wood background (`#6b4322`) with grain gradient, thick beveled border (`#c08a52` / `#3a2514`), 3D lift via `box-shadow: 0 6px 0`, inset highlights.
- Added hover (float up, brighter), active (press down, shadow flattens) states.
- Recoloured label to warm cream (`#f3e3c8`) with engraved text-shadow.
- Changed sword icon glow from teal to warm amber.
- Rebuilt: `just clean && just build && just check` (all green).

## 2026-02-19 01:30 IST — Minecraft chocolate bar button with wrapper
```
The button looks good, I want to turn the button to look like minecraft choclate, where the button remains the same but it will have choclate wrapper in the bottom of pink shade.
```
**Outcome**:
- Restyled button as dark chocolate (`#1c1008`) with grid-square pattern.
- Added `::before` pseudo-element: white paper/foil strip across the middle, extends beyond button edges.
- Added `::after` pseudo-element: pink wrapper covering bottom 55% with concentric pink/white/pink banding.
- On hover: wrapper and foil slide down and fade out (0.4s ease) revealing the chocolate.
- Rebuilt: `just clean && just build && just check` (all green).

## 2026-02-19 02:00 IST — Wrapper hover refinement, sword removal, label placement
```
Take inspiration from "~/Documents/Screenshot 2026-02-19 at 12.16.35 PM.png" the wrapper should be on and when the user hover it should come off.
```
```
Remove the sword icon from the button, animate the whole button to wiggle just like how sword is wiggling now, move the text "Open Inventory" to the top of the choclate bar.
```
```
The wrapper should not dissapear but move a bit down, the "Open Inventory" text should be on the brown area of choclate. The animation is fine, on hover the wrapper needs to move down a bit but not disappear. The size of the button can be a bit bigger.
```
**Outcome**:
- Removed sword `<img>` from `templates/index.html`; removed `.inventory-toggle__icon` CSS and `@keyframes sword-bob`.
- Added `@keyframes choco-bob` on the whole button (±2° rotation, 6px float, 2.5s loop); pauses on hover with `animation: none`.
- Moved "Open Inventory" label onto the chocolate face (normal flow, `position: relative`, z-index 3) — no longer floating above.
- Wrapper hover changed from fade-out to gentle peek-down: pink wrapper slides 18px, foil strip slides 14px, both stay fully visible.
- Button enlarged: `padding: 1.8rem 3.2rem 3rem`, `min-width: 240px`, `min-height: 130px`.
- Rebuilt: `just clean && just build && just check` (all green).
