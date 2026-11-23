"""Extract diagram content from a reference design's own markdown.

Nothing here authors compliance statements. It reads the Universal evidence
workflow table and the per-phase checklists that already exist in a document
and reshapes them into a diagram spec, so a diagram cannot say something the
document does not.
"""
from __future__ import annotations

import html
import re
from pathlib import Path

PHASE_ROW = re.compile(
    r"^\|\s*\*\*(?P<num>\d)\s*[—-]\s*(?P<name>[^*|]+?)\s*\*\*\s*\|"
    r"\s*(?P<goal>[^|]+?)\s*\|"
    r"\s*(?P<actions>[^|]+?)\s*\|"
    r"\s*(?P<when>[^|]+?)\s*\|\s*$",
    re.M,
)


def _md_to_html(s: str) -> str:
    """Minimal inline markdown -> HTML for diagram text.

    Links collapse to their label, because a PNG cannot carry one.
    """
    s = s.strip()
    s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)     # link -> label
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"`(.+?)`", r"<b>\1</b>", s)
    s = re.sub(r"(?<![\w*])\*([^*\n]+?)\*(?![\w*])", r"<i>\1</i>", s)
    s = s.rstrip(".") if s.endswith("..") else s
    return s


def phase_checklist(text: str, num: int) -> tuple[list[str], str]:
    """Return (checklist items without the Export line, export text)."""
    m = re.search(
        rf"^###\s+Phase {num} checklist[^\n]*\n(.*?)(?=^#{{2,3}}\s|\Z)",
        text, re.M | re.S,
    )
    if not m:
        return [], ""
    items, export = [], ""
    for line in m.group(1).splitlines():
        line = line.strip()
        if not line.startswith("- [ ]"):
            continue
        item = line[5:].strip()
        if re.match(r"\*\*Export:?\*\*", item, re.I):
            export = _md_to_html(re.sub(r"^\*\*Export:?\*\*\s*", "", item, flags=re.I))
        else:
            items.append(_md_to_html(item))
    return items, export


def workflow_spec(md: Path, *, kicker: str, title_tail: str, sub: str,
                  caution_label: str, caution: str, takeaway: str,
                  rail: list[str], max_actions: int = 4) -> dict:
    text = md.read_text()
    rows = list(PHASE_ROW.finditer(text))
    if len(rows) != 4:
        raise ValueError(f"{md.name}: expected 4 phase rows, found {len(rows)}")

    phases = []
    for r in rows:
        num = int(r.group("num"))
        checklist, export = phase_checklist(text, num)
        if not checklist:
            # fall back to the table's own action list
            checklist = [_md_to_html(a) for a in r.group("actions").split(";")]
        if not export:
            raise ValueError(f"{md.name}: phase {num} has no Export line")
        phases.append({
            "name": r.group("name").strip(),
            "goal": _md_to_html(r.group("goal")),
            "when": _md_to_html(r.group("when")),
            "actions": checklist[:max_actions],
            "export": export,
        })

    return {
        "kicker": kicker,
        "title": "CSW Evidence Workflow",
        "title_tail": title_tail,
        "sub": sub,
        "phases": phases,
        "caution_label": caution_label,
        "caution": caution,
        "takeaway_tag": "Key Takeaway",
        "takeaway": takeaway,
        "rail": rail,
    }


STEP_HEAD = re.compile(r"^###\s+Step (?P<num>\d)\s*[—-]\s*(?P<name>.+?)\s*$", re.M)


def step_spec(md: Path, *, kicker: str, title: str, title_tail: str, sub: str,
              caution_label: str, caution: str, takeaway: str, rail: list[str],
              names: dict[int, str] | None = None, width: int = 1900,
              max_actions: int = 3) -> dict:
    """Build a spec from a document that uses numbered Steps with exit criteria
    and evidence lines, rather than the four-phase workflow table."""
    text = md.read_text()
    heads = list(STEP_HEAD.finditer(text))
    if not heads:
        raise ValueError(f"{md.name}: no '### Step N' headings found")

    # Bound each step by the next heading of any level, not just the next Step.
    # The last step would otherwise run to end-of-file and swallow bullets from
    # whatever section follows it.
    next_head = re.compile(r"^#{1,6}\s", re.M)
    phases = []
    for i, h in enumerate(heads):
        nh = next_head.search(text, h.end())
        end = min(
            heads[i + 1].start() if i + 1 < len(heads) else len(text),
            nh.start() if nh else len(text),
        )
        block = text[h.end():end]
        acts, exit_c, evidence = [], "", ""
        for line in block.splitlines():
            line = line.strip()
            if not line.startswith("- "):
                continue
            item = line[2:].strip()
            if re.match(r"\*\*Exit criteria:?\*\*", item, re.I):
                exit_c = _md_to_html(re.sub(r"^\*\*Exit criteria:?\*\*\s*", "", item, flags=re.I))
            elif re.match(r"\*\*Evidence produced:?\*\*", item, re.I):
                evidence = _md_to_html(
                    re.sub(r"^\*\*Evidence produced:?\*\*\s*", "", item, flags=re.I))
            else:
                acts.append(_md_to_html(item))
        if not evidence:
            raise ValueError(f"{md.name}: step {h.group('num')} has no 'Evidence produced' line")
        num = int(h.group("num"))
        phases.append({
            "name": (names or {}).get(num) or h.group("name").strip(),
            "goal": "",
            "actions": acts[:max_actions],
            "exit": exit_c,
            "export": evidence,
        })

    return {
        "kicker": kicker,
        "title": title,
        "title_tail": title_tail,
        "sub": sub,
        "width": width,
        "phases": phases,
        "caution_label": caution_label,
        "caution": caution,
        "takeaway_tag": "Key Takeaway",
        "takeaway": takeaway,
        "rail": rail,
    }


def two_col_table(md: Path, header_left: str) -> tuple[list[str], list[str]]:
    """Pull a two-column 'in reach / outside' table out of the document."""
    text = md.read_text()
    m = re.search(
        rf"^\|[^\n]*{re.escape(header_left)}[^\n]*\|[^\n]*\|\s*\n\|[-\s|:]+\|\s*\n"
        r"(?P<body>(?:\|[^\n]*\|\s*\n)+)",
        text, re.M | re.I,
    )
    if not m:
        raise ValueError(f"{md.name}: no two-column table under {header_left!r}")
    left, right = [], []
    for line in m.group("body").strip().splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        if cells[0] and cells[0] != "—":
            left.append(_md_to_html(cells[0]))
        if cells[1] and cells[1] != "—":
            right.append(_md_to_html(cells[1]))
    return left, right
