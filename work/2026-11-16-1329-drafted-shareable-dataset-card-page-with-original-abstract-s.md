# Drafted shareable dataset-card page with original abstract SVG diagram and Media Studio prompt for fixtures-index-v4 4-file inventory.

**Done**

2026-11-16 13:29 UTC, spent $0.02 on Explain its work in a picture or a short video

Thought with meta/muse-ember (7 calls): tokens not reported. Known cost $0.0178; gas and the on-chain cap are not counted here.

- https://hivemindos.app/bee/547

# fixtures-index-v4-files-inventory — 4-row tool files inventory

**One-line caption:** One row per tool file, built from the files themselves, ready to publish.

**Media Studio prompt (standard tier):**
> Clean flat diagram on a plain light background, original abstract geometric icons only, no people, no likeness, no logos, no brand marks. Left: an open folder icon labelled `tools/fixtures-index-v4` with four small file icons labelled `inventory.py`, `self_test.py`, `README.md`, `INVENTORY.md`. Four thin arrows flow right into a striped table icon labelled `data.csv` with header `file_name | source_url | description` and 4 rows. Right of the table: a document icon labelled `README dataset card`. Simple sans-serif labels, teal and slate palette, generous white space, no photorealism.

**Shareable page draft — image + text for the dataset card:**

```html
<figure>
  <svg viewBox="0 0 960 420" role="img" aria-label="Diagram: fixtures-index-v4 folder with four files flowing into a four-row data.csv and a README dataset card">
    <rect width="960" height="420" fill="#f7fafc"/>
    <!-- source folder -->
    <rect x="30" y="90" width="260" height="240" rx="14" fill="#ffffff" stroke="#2a9d8f" stroke-width="3"/>
    <text x="160" y="120" text-anchor="middle" font-family="sans-serif" font-size="16" font-weight="700" fill="#1d3557">SOURCE FOLDER</text>
    <text x="160" y="144" text-anchor="middle" font-family="sans-serif" font-size="13" fill="#334155">tools/fixtures-index-v4</text>
    <!-- 4 file chips -->
    <g font-family="sans-serif" font-size="14" fill="#1d3557">
      <rect x="55" y="160" width="210" height="36" rx="8" fill="#e6f4f1"/><text x="70" y="183">▤ inventory.py</text>
      <rect x="55" y="204" width="210" height="36" rx="8" fill="#e6f4f1"/><text x="70" y="227">▤ self_test.py</text>
      <rect x="55" y="248" width="210" height="36" rx="8" fill="#e6f4f1"/><text x="70" y="271">▤ README.md</text>
      <rect x="55" y="292" width="210" height="36" rx="8" fill="#e6f4f1"/><text x="70" y="315">▤ INVENTORY.md</text>
    </g>
    <!-- arrows -->
    <g stroke="#2a9d8f" stroke-width="3" marker-end="url(#a)">
      <line x1="290" y1="178" x2="365" y2="178"/><line x1="290" y1="222" x2="365" y2="222"/>
      <line x1="290" y1="266" x2="365" y2="266"/><line x1="290" y1="310" x2="365" y2="310"/>
    </g>
    <defs><marker id="a" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto"><path d="M0,0 L7,3 L0,6" fill="none" stroke="#2a9d8f"/></marker></defs>
    <!-- data.csv -->
    <rect x="370" y="90" width="280" height="240" rx="14" fill="#ffffff" stroke="#1d3557" stroke-width="3"/>
    <text x="510" y="120" text-anchor="middle" font-family="sans-serif" font-size="16" font-weight="700" fill="#1d3557">data.csv — 4 ROWS</text>
    <g font-family="monospace" font-size="12" fill="#334155">
      <rect x="385" y="135" width="250" height="28" fill="#1d3557"/><text x="395" y="153" fill="#ffffff">file_name | source_url | description</text>
      <rect x="385" y="165" width="250" height="36" fill="#eef2f7"/><text x="395" y="188">1  inventory.py</text>
      <rect x="385" y="203" width="250" height="36" fill="#ffffff"/><text x="395" y="226">2  self_test.py</text>
      <rect x="385" y="241" width="250" height="36" fill="#eef2f7"/><text x="395" y="264">3  README.md</text>
      <rect x="385" y="279" width="250" height="36" fill="#ffffff"/><text x="395" y="302">4  INVENTORY.md</text>
    </g>
    <!-- card -->
    <line x1="650" y1="210" x2="700" y2="210" stroke="#2a9d8f" stroke-width="3" marker-end="url(#a)"/>
    <rect x="705" y="120" width="225" height="180" rx="14" fill="#fff7e6" stroke="#e9c46a" stroke-width="3"/>
    <text x="817" y="150" text-anchor="middle" font-family="sans-serif" font-size="15" font-weight="700" fill="#1d3557">README</text>
    <text x="817" y="172" text-anchor="middle" font-family="sans-serif" font-size="15" font-weight="700" fill="#1d3557">dataset card</text>
    <text x="817" y="200" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#334155">source · method · columns</text>
    <text x="817" y="222" text-anchor="middle" font-family="sans-serif" font-size="12" fill="#334155">1 row per file</text>
    <text x="480" y="380" text-anchor="middle" font-family="sans-serif" font-size="15" fill="#1d3557">fixtures-index-v4-files-inventory — 4-row tool files inventory</text>
    <text x="480" y="404" text-anchor="middle" font-family="sans-serif" font-size="13" fill="#475569">One row per tool file, built from the files themselves, ready to publish.</text>
  </svg>
  <figcaption>Source: https://github.com/HivemindOS-Agents/hivepunk-547/tree/main/tools/fixtures-index-v4 — 4 files → data.csv (file_name, source_url, description) → README dataset card.</figcaption>
</figure>
```

**What it shows:** The source folder contains exactly the four files listed in the built tool (`inventory.py`, `self_test.py`, `README.md`, `INVENTORY.md`); each becomes one row in `data.csv` with columns `file_name`, `source_url`, `description`; the README dataset card documents the source and method. No people, likeness, or external logos are used — all elements are original abstract diagram shapes.

**Could not confirm:** The Media Studio standard-tier render itself was not regenerated in this step; the SVG above is a draft image in the same specification, ready to replace with the standard-tier output on the dataset card.

Left for owner: paste this figure into the dataset README card and, if desired, swap the SVG for the Media Studio standard-tier PNG.
