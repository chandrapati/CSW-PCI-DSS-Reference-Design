"""Cisco light-theme diagram palette, sampled from the CSW workflow and
differentiation infographics in the project assets folder.

Everything sits in the Cisco blue family (hue 205-212) with light-green
success callouts and amber for the boundary/caution column.
"""

PALETTE = {
    # navy header gradient, deepest to lightest
    "navy_deep": "#022B57",
    "navy": "#0B2D52",
    "navy_mid": "#0F3056",
    "navy_light": "#033565",
    # mid blues for badges, rules and arrows
    "blue_700": "#044678",
    "blue_600": "#024A84",
    "blue_500": "#0A5991",
    "blue_400": "#185589",
    # tints for pills and card headers
    "blue_tint": "#B3D3ED",
    "blue_wash": "#EAF8FF",
    "blue_wash_2": "#F4FAFE",
    # success / evidence-present
    "green_border": "#AFD199",
    "green_wash": "#EEF8E2",
    "green_text": "#2F6B1F",
    # boundary / supplied-outside
    "amber_border": "#E8C79A",
    "amber_wash": "#FDF6EC",
    "amber_text": "#8A5A14",
    # ink and neutrals
    "ink": "#141823",
    "ink_soft": "#2A3340",
    "muted": "#575D66",
    "muted_blue": "#5D738D",
    "rule": "#D8E3EE",
    "card_border": "#C9D9E8",
    "page": "#FFFFFF",
}

FONT_STACK = '"Helvetica Neue", Helvetica, -apple-system, "Segoe UI", Arial, sans-serif'


def base_css(p=PALETTE) -> str:
    return f"""
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{
  font-family:{FONT_STACK};
  background:{p['page']};
  color:{p['ink']};
  -webkit-font-smoothing:antialiased;
}}
.sheet {{ position:relative; overflow:hidden; background:{p['page']}; }}

/* ---- header ---- */
.hdr {{
  background:linear-gradient(100deg,{p['navy_deep']} 0%,{p['navy_light']} 55%,{p['blue_500']} 100%);
  display:flex; align-items:center; gap:22px;
}}
.hdr .mark {{ display:flex; align-items:flex-end; gap:3px; flex:0 0 auto; }}
.hdr .mark i {{ display:block; width:4px; background:#9FD9F6; border-radius:2px; }}
.hdr .wordmark {{
  color:#FFFFFF; font-size:13px; letter-spacing:.16em; font-weight:600;
  border-left:1px solid rgba(255,255,255,.34); padding-left:18px;
}}
.hdr .wordmark small {{ display:block; font-size:10px; letter-spacing:.1em;
  color:#B5E2FF; font-weight:400; margin-top:3px; }}
.hdr .titles {{ flex:1 1 auto; }}
.hdr h1 {{ color:#FFFFFF; font-weight:600; letter-spacing:-.01em; }}
.hdr h1 em {{ font-style:normal; color:#9FD9F6; font-weight:400; }}
.hdr p {{ color:#C9E6FA; font-weight:400; }}

/* ---- cards ---- */
.card {{
  background:{p['page']}; border:1px solid {p['card_border']}; border-radius:9px;
  display:flex; flex-direction:column; overflow:hidden;
}}
.card header {{ display:flex; align-items:center; gap:11px; }}
.badge {{
  flex:0 0 auto; border-radius:50%; background:{p['blue_700']}; color:#fff;
  display:flex; align-items:center; justify-content:center; font-weight:700;
}}
.card h2 {{ color:{p['navy']}; font-weight:700; letter-spacing:-.005em; }}
.card .goal {{ color:{p['muted']}; font-weight:400; }}

.pill {{
  display:inline-block; border-radius:999px; font-weight:600;
  background:{p['blue_wash']}; color:{p['blue_600']};
  border:1px solid {p['blue_tint']};
}}
.pill.green {{ background:{p['green_wash']}; color:{p['green_text']}; border-color:{p['green_border']}; }}
.pill.amber {{ background:{p['amber_wash']}; color:{p['amber_text']}; border-color:{p['amber_border']}; }}

ul.acts {{ list-style:none; }}
ul.acts li {{ position:relative; color:{p['ink_soft']}; }}
ul.acts li:before {{
  content:""; position:absolute; left:0; top:.46em;
  width:5px; height:5px; border-radius:50%;
  background:{p['blue_500']};
}}

/* flow arrow between cards */
.flow {{ position:absolute; top:50%; transform:translateY(-50%);
  display:flex; align-items:center; z-index:3; }}
.flow i {{ display:block; height:3px; width:8px; background:{p['blue_tint']}; }}
.flow b {{ display:block; width:0; height:0;
  border-left:8px solid {p['blue_500']};
  border-top:5.5px solid transparent; border-bottom:5.5px solid transparent; }}

.note {{ border-radius:7px; border:1px solid {p['green_border']};
  background:{p['green_wash']}; color:{p['green_text']}; }}
.note.amber {{ border-color:{p['amber_border']}; background:{p['amber_wash']}; color:{p['amber_text']}; }}
.note .lbl {{ font-weight:700; }}

/* ---- footer ---- */
.ftr {{
  background:linear-gradient(100deg,{p['navy_deep']} 0%,{p['navy_light']} 70%,{p['blue_500']} 100%);
  display:flex; align-items:center; gap:20px;
}}
.ftr .tag {{
  flex:0 0 auto; color:#FFFFFF; font-weight:700; letter-spacing:.02em;
  display:flex; align-items:center; gap:9px;
}}
.ftr .tag svg {{ flex:0 0 auto; }}
.ftr .body {{ flex:1 1 auto; color:#DCEEFA; font-weight:400; }}
.ftr .body b {{ color:#FFFFFF; font-weight:700; }}
.ftr .rail {{ flex:0 0 auto; border-left:1px solid rgba(255,255,255,.3); }}
.ftr .rail div {{ color:#CDEBFF; display:flex; align-items:flex-start; gap:7px; }}
.ftr .rail div span.ck {{ color:#B7E892; font-weight:700; }}
"""


def mark_html(bar_h=(7, 12, 17, 12, 7), unit=1.0) -> str:
    bars = "".join(f'<i style="height:{round(h * unit)}px"></i>' for h in bar_h)
    return f'<div class="mark">{bars}</div>'
