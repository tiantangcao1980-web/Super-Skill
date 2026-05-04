from __future__ import annotations

import json
from pathlib import Path


def load_tokens(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def render_dashboard(tokens: dict) -> str:
    colors = tokens["colors"]
    radius = int(tokens["radius"])
    spacing = int(tokens["spacing"])
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{tokens['brand']} Dashboard</title>
  <style>
    :root {{
      --bg: {colors['background']};
      --surface: {colors['surface']};
      --text: {colors['text']};
      --accent: {colors['accent']};
      --warning: {colors['warning']};
      --radius: {radius}px;
      --space: {spacing}px;
    }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--text);
      font-family: system-ui, sans-serif;
      letter-spacing: 0;
    }}
    main {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: var(--space);
      padding: calc(var(--space) * 2);
    }}
    section {{
      background: var(--surface);
      border: 1px solid #d8dee9;
      border-radius: var(--radius);
      min-height: 120px;
      padding: var(--space);
    }}
  </style>
</head>
<body>
  <main aria-label="DesignDNA brand dashboard">
    <section aria-label="Conversion health"><h1>{tokens['brand']}</h1><p>Conversion is stable.</p></section>
    <section aria-label="Delivery quality"><h2>Quality</h2><p>Checks are passing.</p></section>
    <section aria-label="Operational warning"><h2>Guardrail</h2><p>No rollback needed.</p></section>
  </main>
</body>
</html>"""
