"""Render an HTML string to a crisp PNG via headless Chrome, then downsample.

Renders at deviceScaleFactor=2 and resizes back to logical size with LANCZOS,
which gives sharp text at a file size that is reasonable to commit.
"""
from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

from PIL import Image

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def render(html: str, out_png: Path, width: int, height: int, scale: int = 2) -> Path:
    out_png = Path(out_png)
    out_png.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        src = Path(td) / "d.html"
        src.write_text(html)
        raw = Path(td) / "raw.png"
        cmd = [
            CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
            "--force-device-scale-factor=%d" % scale,
            "--default-background-color=00000000",
            f"--window-size={width},{height}",
            f"--screenshot={raw}",
            f"--user-data-dir={td}/prof",
            src.as_uri(),
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if not raw.exists():
            raise RuntimeError(f"chrome produced no image\n{res.stderr[-1500:]}")
        im = Image.open(raw).convert("RGB")
        if im.size != (width, height):
            im = im.resize((width, height), Image.LANCZOS)
        im.save(out_png, "PNG", optimize=True)
    return out_png


def page(body: str, css: str, width: int, height: int) -> str:
    return (
        "<!doctype html><html><head><meta charset='utf-8'><style>"
        + css
        + f"\n.sheet{{width:{width}px;height:{height}px;}}\n"
        + "</style></head><body>"
        + f"<div class='sheet'>{body}</div>"
        + "</body></html>"
    )
