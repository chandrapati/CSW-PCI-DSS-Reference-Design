"""Diagram builders for the CSW compliance reference-design series.

Content is data-driven so a framework supplies its own spec and gets the same
visual treatment. Nothing here invents capability claims: every string is
supplied by the caller from its reference design.
"""
from __future__ import annotations

from theme import PALETTE as P, base_css, mark_html

W, H = 1600, 900


# ----------------------------------------------------------------- shared bits
def _header(kicker: str, title: str, title_tail: str, sub: str, pad: int = 34) -> str:
    return f"""
<div class="hdr" style="height:96px;padding:0 {pad}px">
  {mark_html(unit=1.45)}
  <div class="wordmark">CISCO<small>SECURE WORKLOAD</small></div>
  <div class="titles">
    <h1 style="font-size:28px">{title} <em>{title_tail}</em></h1>
    <p style="font-size:13.5px;margin-top:5px">{sub}</p>
  </div>
  <div style="flex:0 0 auto;text-align:right">
    <div class="pill" style="background:rgba(255,255,255,.12);border-color:rgba(255,255,255,.35);
         color:#EAF8FF;font-size:11px;padding:6px 13px">{kicker}</div>
  </div>
</div>"""


def _footer(tag: str, body: str, rail: list[str], pad: int = 34) -> str:
    items = "".join(
        f'<div style="font-size:11px;line-height:1.45;margin:3px 0">'
        f'<span class="ck">&#10003;</span><span>{r}</span></div>'
        for r in rail
    )
    return f"""
<div class="ftr" style="height:92px;padding:0 {pad}px">
  <div class="tag" style="font-size:17px">
    <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
      <circle cx="12" cy="12" r="10" stroke="#9FD9F6" stroke-width="2"/>
      <path d="M7.5 12.4l3 3 6-6.4" stroke="#B7E892" stroke-width="2.3"
            stroke-linecap="round" stroke-linejoin="round"/>
    </svg>{tag}
  </div>
  <div class="body" style="font-size:12.5px;line-height:1.5;max-width:720px">{body}</div>
  <div class="rail" style="padding-left:22px;width:390px">{items}</div>
</div>"""


# -------------------------------------------------------- 1. evidence workflow
def evidence_workflow(spec: dict) -> str:
    """Numbered phase cards, in the style of the CSW policy-workflow deck.

    Handles 4-phase and 6-step documents. `when` and `exit` are optional, so a
    framework that records exit criteria instead of durations still renders.
    """
    n = len(spec["phases"])
    w = spec.get("width", W)
    gap, pad = (26, 28) if n <= 4 else (16, 24)
    cw = (w - 2 * pad - (n - 1) * gap) / n
    fs = 12.0 if n <= 4 else 10.8      # body text shrinks as cards narrow
    hs = 16.5 if n <= 4 else 14.0

    cards = []
    for i, ph in enumerate(spec["phases"], 1):
        acts = "".join(
            f'<li style="font-size:{fs}px;line-height:1.42;padding-left:14px;margin:6px 0">'
            f"{a}</li>"
            for a in ph["actions"]
        )
        when = (f'<div class="pill" style="font-size:10px;padding:3px 10px;margin-top:10px">'
                f'{ph["when"]}</div>') if ph.get("when") else ""
        exit_note = (f"""
    <div class="pill" style="display:block;font-size:9.8px;line-height:1.35;padding:7px 10px;
         margin-bottom:7px;font-weight:400">
      <b>Exit&nbsp;&rsaquo;</b> {ph['exit']}
    </div>""") if ph.get("exit") else ""
        cards.append(f"""
<div class="card" style="width:{cw:.1f}px;padding:0">
  <div style="background:{P['blue_wash_2']};border-bottom:1px solid {P['rule']};
       padding:13px 14px 12px">
    <header>
      <div class="badge" style="width:30px;height:30px;font-size:15px">{i}</div>
      <div style="flex:1 1 auto">
        <h2 style="font-size:{hs}px;line-height:1.15">{ph['name']}</h2>
        <div class="goal" style="font-size:10.8px;line-height:1.35;margin-top:4px">{ph['goal']}</div>
      </div>
    </header>
    {when}
  </div>
  <ul class="acts" style="flex:1 1 auto;padding:11px 14px 5px">{acts}</ul>
  <div style="padding:0 12px 12px">{exit_note}
    <div class="note" style="padding:9px 11px;font-size:10.2px;line-height:1.4">
      <span class="lbl">Evidence&nbsp;&rsaquo;</span> {ph['export']}
    </div>
  </div>
</div>""")

    arrows = "".join(
        f'<div class="flow" style="left:{pad + cw * k + gap * (k - 1) + (gap - 16) / 2:.1f}px">'
        f"<i></i><b></b></div>"
        for k in range(1, n)
    )

    body = (
        _header(spec["kicker"], spec["title"], spec["title_tail"], spec["sub"], pad)
        + f"""
<div style="position:relative;padding:22px {pad}px 0">
  <div style="display:flex;gap:{gap}px;align-items:stretch;height:382px">{''.join(cards)}</div>
  {arrows}
</div>
<div style="padding:16px {pad}px 0">
  <div class="note amber" style="padding:11px 15px;font-size:12px;line-height:1.5">
    <span class="lbl">{spec['caution_label']}</span> {spec['caution']}
  </div>
</div>"""
        + _footer(spec["takeaway_tag"], spec["takeaway"], spec["rail"], pad)
    )
    return body


# ------------------------------------------------------------ 2. scope boundary
def scope_boundary(spec: dict) -> str:
    """Two-column reach / out-of-reach, with the headline exclusions called out."""
    pad = 28

    excl = "".join(f"""
<div class="card" style="flex:1 1 0;border-color:{P['amber_border']};
     background:{P['amber_wash']};padding:12px 14px">
  <div style="display:flex;align-items:center;gap:9px;margin-bottom:6px">
    <svg width="17" height="17" viewBox="0 0 24 24" fill="none">
      <circle cx="12" cy="12" r="9.3" stroke="{P['amber_text']}" stroke-width="2"/>
      <path d="M8.3 15.7L15.7 8.3" stroke="{P['amber_text']}" stroke-width="2.2"
            stroke-linecap="round"/>
    </svg>
    <div style="font-size:13px;font-weight:700;color:{P['amber_text']}">{e['head']}</div>
  </div>
  <div style="font-size:11px;line-height:1.45;color:{P['ink_soft']}">{e['body']}</div>
</div>""" for e in spec["exclusions"])

    # Fixed row box so the sheet height is arithmetic rather than an estimate:
    # box-sizing is border-box globally, so ROW_BOX includes the border.
    ROW_BOX, ROW_GAP, HEAD_H, COL_PAD = 29.0, 5.0, 44.0, 24.0
    ROW_H = ROW_BOX + ROW_GAP

    def col(items, tone):
        wash = P["green_wash"] if tone == "in" else P["amber_wash"]
        border = P["green_border"] if tone == "in" else P["amber_border"]
        txt = P["green_text"] if tone == "in" else P["amber_text"]
        glyph = "&#10003;" if tone == "in" else "&ndash;"
        return "".join(f"""
<div style="display:flex;gap:9px;align-items:center;height:{ROW_BOX:.0f}px;padding:0 11px;
     background:{wash};border:1px solid {border};border-radius:6px;margin-bottom:{ROW_GAP:.0f}px">
  <span style="color:{txt};font-weight:700;font-size:11px">{glyph}</span>
  <span style="font-size:11.5px;line-height:1.3;color:{P['ink_soft']}">{i}</span>
</div>""" for i in items)

    rows = max(len(spec["in_reach"]), len(spec["out_reach"]))
    col_h = HEAD_H + rows * ROW_H + COL_PAD
    # A diagram that silently drops a row of in-scope estate is worse than no
    # diagram, so assert the column can hold every row it was given.
    assert col_h - HEAD_H - COL_PAD >= rows * ROW_H, "column would clip rows"
    spec["_col_h"] = col_h   # the build script reads this to size the sheet

    body = (
        _header(spec["kicker"], spec["title"], spec["title_tail"], spec["sub"])
        + f"""
<div style="padding:18px {pad}px 0;display:flex;gap:14px">{excl}</div>

<div style="padding:16px {pad}px 18px;display:flex;gap:18px;height:{col_h + 34:.0f}px">
  <div class="card" style="flex:1 1 0;padding:0">
    <div style="background:{P['green_wash']};border-bottom:1px solid {P['green_border']};
         padding:11px 16px;display:flex;align-items:center;gap:10px;height:{HEAD_H:.0f}px">
      <div style="font-size:14.5px;font-weight:700;color:{P['green_text']}">
        {spec['in_head']}</div>
      <div class="pill green" style="font-size:10px;padding:3px 9px">{spec['in_tag']}</div>
    </div>
    <div style="padding:12px 14px">{col(spec['in_reach'], 'in')}</div>
  </div>
  <div class="card" style="flex:1 1 0;padding:0">
    <div style="background:{P['amber_wash']};border-bottom:1px solid {P['amber_border']};
         padding:11px 16px;display:flex;align-items:center;gap:10px;height:{HEAD_H:.0f}px">
      <div style="font-size:14.5px;font-weight:700;color:{P['amber_text']}">
        {spec['out_head']}</div>
      <div class="pill amber" style="font-size:10px;padding:3px 9px">{spec['out_tag']}</div>
    </div>
    <div style="padding:12px 14px">{col(spec['out_reach'], 'out')}</div>
  </div>
</div>"""
        + _footer(spec["takeaway_tag"], spec["takeaway"], spec["rail"])
    )
    return body


BUILDERS = {"evidence_workflow": evidence_workflow, "scope_boundary": scope_boundary}


def build(kind: str, spec: dict, out_png, css: str | None = None):
    from render import page, render
    body = BUILDERS[kind](spec)
    return render(page(body, css or base_css(), W, H), out_png, W, H)
