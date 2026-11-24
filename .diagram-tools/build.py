"""Regenerate this repo's diagram.

Usage:  python3 build.py
Step content is extracted from the reference design itself, so editing the
document and re-running keeps the diagram honest.
"""
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import diagrams
import render
from extract import step_spec
from spec import SIX_STEP
from theme import base_css

REPO = Path(__file__).resolve().parent.parent
MD = REPO / "CSW-PCI-DSS-Reference-Design.md"
OUT = REPO / "assets"

spec = step_spec(MD, **SIX_STEP)
rows = max(len(p["actions"]) for p in spec["phases"])
w = spec.get("width", diagrams.W)
h = int(96 + 22 + (300 + rows * 26 + 62) + 16 + 58 + 92)
body = diagrams.evidence_workflow(spec)
p = render.render(render.page(body, base_css(), w, h),
                  OUT / "csw-six-step-build.png", w, h)
print(f"  csw-six-step-build.png  {w}x{h}  {os.path.getsize(p) // 1024} KB")
