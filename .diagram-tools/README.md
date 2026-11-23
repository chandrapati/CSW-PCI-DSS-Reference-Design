# Diagram tools

Regenerates the diagrams in `../assets/` so they stay in step with the
reference design rather than drifting from it.

```bash
cd .diagram-tools && python3 build.py
```

Requirements: Python 3 with Pillow, and Google Chrome at the path in
`render.py`. Rendering happens at `deviceScaleFactor=2` and downsamples to the
logical size, which keeps text sharp at a file size reasonable to commit.

## Files

| File | Purpose |
|---|---|
| `theme.py` | Palette and base CSS, sampled from the Cisco CSW infographics. |
| `diagrams.py` | Layout builders. |
| `extract.py` | Reads the phase or step content out of the reference design. |
| `spec.py` | The framing text for this framework. |
| `build.py` | Renders this repo's diagrams. |

## Conventions

Phase content is **extracted from the reference design**, not retyped here, so
a diagram cannot state something the document does not. Edit the document and
re-run; only the framing text in `spec.py` is authored.

PNG rather than Mermaid for these section-level graphics: PNGs embed in the
pandoc-generated DOCX and PDF exports, and they render the same wherever the
markdown is read. The smaller inline `flowchart LR` diagrams elsewhere in this
document stay as Mermaid.

Keep these diagrams free of competitive comparison. This is a public,
customer-facing repository, so positioning belongs on Cisco capability and the
evidence boundary; competitive material belongs in internal battle cards.
