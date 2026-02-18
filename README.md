# farhaan.bukh.sh

Minecraft ambience + Hitchhiker whimsy in a lightweight static site, built with Python and deployed to GitHub Pages.

## Features

- **Markdown-driven content** — edit `content/index.md` and `content/talks.md`, build, deploy.
- **Python build pipeline** — Jinja2 templates + `markdown` + PyYAML; no client-side JS libraries for content.
- **Sleek typography baseline** — Chakra Petch + Space Grotesk via Google Fonts.
- **Minecraft + Hitchhiker palette** — custom gradient background with neon accents.
- **uv** for dependency management, **just** as the task runner.
- **GitHub Pages workflow** deploys `dist/` on every push to `main`.

## Quick start

```bash
# Prerequisites: uv, just
just build        # install deps + generate dist/
just serve        # build + preview at http://localhost:5000
just check        # smoke-test that dist/ has expected files
just clean        # remove dist/
```

## Palette

| Token | Hex | Inspiration |
| --- | --- | --- |
| `--color-night` | `#041019` | Deep cosmic sky |
| `--color-space` | `#030B12` | Infinite void |
| `--color-forest` | `#0D2818` | Minecraft canopy shadows |
| `--color-leaf` | `#3BA55D` | Creeper/grass highlight |
| `--color-coil` | `#1DD3B0` | Hitchhiker teal neon |
| `--color-lime` | `#B5F44A` | Pixelated sunlit grass |
| `--color-amber` | `#F5DF4D` | "Don't Panic" book cover |
| `--color-soil` | `#5A3E2B` | Minecraft dirt blocks |
| `--color-nebula` | `#7F5AF0` | Galactic purple accent |
| `--color-ice` | `#F4F9FF` | Text / starlight |
| `--color-cloud` | `#9FB3C8` | Muted copy |

## Project structure

```
.
├── .github/workflows/deploy.yml   # CI: uv + just build → deploy dist/
├── assets/                        # Static (copied verbatim to dist/)
│   ├── css/style.css
│   ├── img/avatar.png
│   └── js/main.js
├── content/                       # Editable markdown sources
│   ├── index.md                   # Home page (YAML frontmatter)
│   └── talks.md                   # Talks list (pure markdown)
├── templates/                     # Jinja2 HTML templates
│   ├── base.html
│   ├── index.html
│   └── talks.html
├── build.py                       # Python build script
├── justfile                       # Task runner
├── pyproject.toml                 # uv project + deps
├── .python-version
├── CNAME                          # farhaan.bukh.sh
├── agents.md
├── prompt.md
└── README.md
```

## Updating content

### Home page
Edit `content/index.md`. YAML frontmatter controls structured data (headline, bio, links, CTAs, meta). Run `just build` to regenerate.

### Talks
Edit `content/talks.md` with standard Markdown. Use sections (`## Upcoming`, `## 2024`, `## Archive`), lists, and links.

### Workflow
1. Edit markdown in `content/`.
2. `just build` → preview `dist/` locally.
3. Commit & push to `main`.
4. GitHub Actions runs `just build` → deploys `dist/` to Pages.

## Deployment

1. Create a GitHub repo and push this directory.
2. Enable Actions + Pages in repo settings.
3. The workflow installs uv + just, runs `just build`, uploads `dist/`, and deploys.
4. Set custom domain to `farhaan.bukh.sh` in Pages settings. DNS `CNAME` → `<username>.github.io`.
