# Examples

Four complete deliverables generated following the exact contracts of the kits in this repository, so reviewers can judge output quality across multiple sectors and visual themes without installing anything.

Every business and creator shown here is **fictional** (*KURO Omakase & Robata*, *Valeria Méndez `@valeriamendez.design`*, and *Clínica Dental Sonrisa Norte*). All figures, reviews, prices and photography are synthetic.

Browse them live at [`examples/index.html`](https://anas12bs-arch.github.io/claude-skill-factory-es/examples/).

---

## 1. Luxury restaurant landing page — `kit-web-scrolling` (dark theme)

| File | Format | Description |
|---|---|---|
| [`web-kuro-omakase.html`](./web-kuro-omakase.html) | Self-contained HTML + local photography | Dark luxury Japanese restaurant in Madrid: full-bleed parallax hero, interactive tabbed menu, bento gallery, reviews and reservation form |

**Highlights:**

- Warm obsidian (`#0A0908`), brushed gold (`#C8A252`) and vermilion hanko accents paired with `Cormorant Garamond` + `Plus Jakarta Sans`.
- Top scroll-progress bar, sticky glass navigation, native `IntersectionObserver` staggered reveals, animated counters and `requestAnimationFrame` parallax.
- Interactive three-tab menu (*Omakase*, *Robata & Nigiri*, *Sake & Bodega*) and reservation form with instant confirmation state.
- Full `prefers-reduced-motion` support and responsive mobile menu.

---

## 2. Personal brand site from Instagram — `kit-instagram-web`

| File | Format | Description |
|---|---|---|
| [`web-valeria-mendez-ig.html`](./web-valeria-mendez-ig.html) | Self-contained HTML + local photography | Personal brand site for fictional creative director `@valeriamendez.design` in Barcelona |

**Highlights:**

- Implements the full `02-instagram-a-web.md` contract: elevated Instagram profile card with animated rotating story ring, blue verified badge, instant visible profile stats (`318 · 84,2K · 412`), bio, IG-style actions and 6-tile visual mini-grid.
- Multi-platform community breakdown (`142.300` total audience across Instagram, YouTube, LinkedIn and Newsletter).
- Filterable portfolio grid (*Todos*, *Packaging*, *Branding*, *Editorial*) with an interactive lightbox modal.

---

## 3. Clinical landing page — `kit-web-scrolling` (light theme)

| File | Format | Description |
|---|---|---|
| [`web-clinica-sonrisa-norte.html`](./web-clinica-sonrisa-norte.html) | Self-contained HTML + local photography | Boutique dental clinic in Ruzafa, Valencia, demonstrating the skill's light healthcare theme |

**Highlights:**

- Warm alabaster and botanical teal palette with architectural arched photography frame, floating glass KPI cards, custom SVG treatment icons and transparent pricing consistent with the audit report.
- Native `IntersectionObserver` reveals and counters, parallax background blobs and interactive appointment request form.

---

## 4. Business audit report — `kit-auditoria-negocio`

| File | Format | Description |
|---|---|---|
| [`auditoria-negocio-clinica-sonrisa-norte.html`](./auditoria-negocio-clinica-sonrisa-norte.html) | Self-contained HTML | Interactive 58/100 executive audit report: score rings, animated bars, sticky navigation |
| [`auditoria-negocio-clinica-sonrisa-norte.pdf`](./auditoria-negocio-clinica-sonrisa-norte.pdf) | PDF, A4 | Print export of the same report, generated with headless Chrome |

To regenerate the PDF:

```bash
chrome --headless --no-pdf-header-footer \
  --print-to-pdf=auditoria-negocio-clinica-sonrisa-norte.pdf \
  auditoria-negocio-clinica-sonrisa-norte.html
```

---

## Preview captures

All preview screenshots in [`../assets`](../assets) (`preview-kuro-omakase.png`, `preview-valeria-instagram.png`, `preview-landing-hero.png`, `preview-audit-report.png`) were captured directly from these HTML files using headless Chrome at `1440×900` (2× Retina supersampled).
