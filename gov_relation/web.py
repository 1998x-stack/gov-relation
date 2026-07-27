"""Read-only web helpers for local API and static site data."""

from __future__ import annotations

import json
import re
import sqlite3
from dataclasses import asdict
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

from .inventory import collect_inventory
from .log import get_logger
from .paths import DATABASE_DIR, DOCS_DIR, GRAPH_DIR, PERSONS_DIR, REPORT_DIR, REPO_ROOT

logger = get_logger(__name__)

# Regex used by md_to_html — compiled once at module load.
_RE_H1 = re.compile(r"^# (.+)$", re.MULTILINE)
_RE_H2 = re.compile(r"^## (.+)$", re.MULTILINE)
_RE_H3 = re.compile(r"^### (.+)$", re.MULTILINE)
_RE_H4 = re.compile(r"^#### (.+)$", re.MULTILINE)
_RE_H5 = re.compile(r"^##### (.+)$", re.MULTILINE)
_RE_H6 = re.compile(r"^###### (.+)$", re.MULTILINE)
_RE_BLOCKQUOTE = re.compile(r"^> (.+)$", re.MULTILINE)
_RE_HORIZONTAL_RULE = re.compile(r"^---+\s*$", re.MULTILINE)
_RE_BOLD = re.compile(r"\*\*(.+?)\*\*")
_RE_ITALIC = re.compile(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)")
_RE_LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
_RE_IMAGE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
_RE_TABLE_ROW = re.compile(r"^\|(.+)\|\s*$")
_RE_TABLE_SEP = re.compile(r"^\|[\s\-:|+]+\|\s*$")


def _table_row_to_html(line: str) -> str:
    cells = [cell.strip() for cell in line.strip("|").split("|")]
    cols = "".join(f"<td>{c}</td>" for c in cells)
    return f"<tr>{cols}</tr>"


def md_to_html(md_text: str, title: str = "") -> str:
    """Convert a subset of Markdown to a standalone HTML page.

    Supports: H1-H6, blockquotes, horizontal rules, bold, italic,
    links, images, bullet/unordered lists, tables, and paragraph wrapping.

    Uses only Python stdlib — no third-party dependencies.
    """
    if not title:
        m = _RE_H1.search(md_text)
        title = m.group(1).strip() if m else "Report"

    # inline formatting (skip hr — handled at block level)
    text = md_text
    text = _RE_IMAGE.sub(r'<img src="\2" alt="\1">', text)
    text = _RE_LINK.sub(r'<a href="\2">\1</a>', text)
    text = _RE_BOLD.sub(r"<strong>\1</strong>", text)
    text = _RE_ITALIC.sub(r"<em>\1</em>", text)

    # --- block-level conversion ---
    lines = text.split("\n")
    out: list[str] = []
    in_table = False
    in_list = False
    list_type: str | None = None
    in_blockquote = False

    def _close_blockquote() -> None:
        nonlocal in_blockquote
        if in_blockquote:
            out.append("</blockquote>")
            in_blockquote = False

    def _close_list() -> None:
        nonlocal in_list, list_type
        if in_list:
            out.append(f"</{list_type}>")
            in_list = False
            list_type = None

    def _close_table() -> None:
        nonlocal in_table
        if in_table:
            out.append("</table>")
            in_table = False

    for raw_line in lines:
        line = raw_line.strip()

        # Horizontal rule
        if _RE_HORIZONTAL_RULE.match(line):
            _close_blockquote()
            _close_list()
            _close_table()
            out.append("<hr>")
            continue

        # Headings
        heading = None
        for level, regex in [(6, _RE_H6), (5, _RE_H5), (4, _RE_H4), (3, _RE_H3), (2, _RE_H2), (1, _RE_H1)]:
            m = regex.search(raw_line)
            if m:
                heading = (level, m.group(1).strip())
                break
        if heading:
            _close_blockquote()
            _close_list()
            _close_table()
            out.append(f"<h{heading[0]}>{heading[1]}</h{heading[0]}>")
            continue

        # Empty line — close open blocks
        if not line:
            _close_blockquote()
            _close_list()
            _close_table()
            out.append("")
            continue

        # Blockquote
        bq_match = _RE_BLOCKQUOTE.match(raw_line)
        if bq_match:
            _close_list()
            _close_table()
            if not in_blockquote:
                out.append("<blockquote>")
                in_blockquote = True
            out.append(f"<p>{bq_match.group(1).strip()}</p>")
            continue
        else:
            _close_blockquote()

        # Table separator row (|------|) — skip
        if _RE_TABLE_SEP.match(line):
            if not in_table:
                out.append("<table>")
                in_table = True
            # Don't emit separator row
            continue

        # Table row
        tbl_match = _RE_TABLE_ROW.match(line)
        if tbl_match:
            _close_list()
            if not in_table:
                out.append("<table>")
                in_table = True
            out.append(_table_row_to_html(line))
            continue
        else:
            _close_table()

        # Unordered list
        if line.startswith("- "):
            _close_blockquote()
            _close_table()
            if not in_list or list_type != "ul":
                _close_list()
                out.append("<ul>")
                in_list = True
                list_type = "ul"
            out.append(f"<li>{line[2:]}</li>")
            continue
        # Ordered list
        ol_match = re.match(r"^\d+\.\s+(.+)$", line)
        if ol_match:
            _close_blockquote()
            _close_table()
            if not in_list or list_type != "ol":
                _close_list()
                out.append("<ol>")
                in_list = True
                list_type = "ol"
            out.append(f"<li>{ol_match.group(1)}</li>")
            continue

        # Close list if we hit non-list content
        _close_list()

        # Default: paragraph
        _close_blockquote()
        _close_table()
        out.append(f"<p>{line}</p>")

    # Close any remaining open tags
    _close_blockquote()
    _close_list()
    _close_table()

    body_html = "\n".join(out)

    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} · 政府关系</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{
    background: #0d0d0d;
    color: #e8e0d0;
    font-family: 'Inter', -apple-system, 'Noto Sans SC', sans-serif;
    line-height: 1.8;
    padding: 2rem 1.5rem;
    max-width: 880px;
    margin: 0 auto;
  }}
  h1 {{ font-size: 1.5rem; font-weight: 700; color: #f0e8d8; margin: 1.5rem 0 0.75rem; font-family: 'Noto Serif SC', serif; border-bottom: 1px solid #2a2a2a; padding-bottom: 0.4rem; }}
  h2 {{ font-size: 1.2rem; font-weight: 700; color: #e0d8c8; margin: 1.2rem 0 0.5rem; font-family: 'Noto Serif SC', serif; }}
  h3 {{ font-size: 1.05rem; font-weight: 600; color: #d0c8b8; margin: 1rem 0 0.4rem; }}
  h4, h5, h6 {{ font-size: 0.95rem; font-weight: 600; color: #c8c0b0; margin: 0.8rem 0 0.3rem; }}
  p {{ margin: 0.5rem 0; }}
  a {{ color: #C9A94E; text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  strong {{ color: #f0e8d8; }}
  em {{ color: #c8c0b0; }}
  blockquote {{
    margin: 0.6rem 0; padding: 0.5rem 1rem;
    border-left: 3px solid #C9A94E;
    background: rgba(201,169,78,0.06);
    color: #b8b0a0;
    font-size: 0.9rem;
  }}
  blockquote p {{ margin: 0.2rem 0; }}
  hr {{ border: none; border-top: 1px solid #2a2a2a; margin: 1.5rem 0; }}
  ul, ol {{ margin: 0.4rem 0 0.4rem 1.2rem; padding-left: 0.4rem; }}
  li {{ margin: 0.2rem 0; }}
  table {{
    width: 100%; border-collapse: collapse;
    margin: 0.6rem 0; font-size: 0.85rem;
  }}
  th, td {{
    border: 1px solid #2a2a2a;
    padding: 0.35rem 0.6rem;
    text-align: left;
    vertical-align: top;
  }}
  th {{ background: rgba(201,169,78,0.1); color: #d0c8b8; font-weight: 600; }}
  td {{ background: rgba(255,255,255,0.02); }}
  img {{ max-width: 100%; border-radius: 4px; margin: 0.6rem 0; }}
  code {{
    background: rgba(255,255,255,0.06);
    padding: 0.1rem 0.3rem;
    border-radius: 3px;
    font-family: 'JetBrains Mono', 'Fira Code', monospace;
    font-size: 0.85rem;
  }}
  pre code {{
    display: block;
    padding: 0.6rem 0.8rem;
    overflow-x: auto;
  }}
  .footer {{
    margin-top: 2rem; padding-top: 0.8rem;
    border-top: 1px solid #2a2a2a;
    font-size: 0.75rem; color: #6a6458;
  }}
  .footer a {{ color: #8a8478; }}
</style>
</head>
<body>
{body_html}
</body>
</html>"""

    return html


def list_databases() -> list[dict]:
    rows = []
    for path in sorted(DATABASE_DIR.glob("*.db")):
        rows.append({"name": path.name, "stem": path.stem, "path": str(path.relative_to(REPO_ROOT)), "size": path.stat().st_size})
    return rows


def list_graphs() -> list[dict]:
    rows = []
    for path in sorted(GRAPH_DIR.glob("*.gexf")):
        rows.append({"name": path.name, "stem": path.stem, "path": str(path.relative_to(REPO_ROOT)), "size": path.stat().st_size})
    return rows


def list_reports() -> list[dict]:
    rows = []
    for path in sorted(REPORT_DIR.glob("*")):
        if path.is_file() and path.suffix.lower() in {".md", ".html"}:
            row: dict = {"name": path.name, "path": str(path.relative_to(REPO_ROOT)), "type": path.suffix.lstrip("."), "size": path.stat().st_size}
            html_path = DOCS_DIR / "reports" / f"{path.stem}.html"
            if html_path.exists():
                row["html_path"] = str(html_path.relative_to(REPO_ROOT))
            rows.append(row)
    return rows


def list_person_profiles() -> list[dict]:
    rows = []
    if not PERSONS_DIR.exists():
        return rows
    for path in sorted(PERSONS_DIR.glob("*.json")):
        record = {"name": path.name, "path": str(path.relative_to(REPO_ROOT)), "size": path.stat().st_size}
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            identity = data.get("identity", {})
            scope = data.get("investigation_scope", {})
            record.update(
                {
                    "person": identity.get("name", ""),
                    "job": scope.get("job", ""),
                    "province": scope.get("province", ""),
                    "city": scope.get("city", ""),
                    "current_post": data.get("current_status", {}).get("current_post", ""),
                }
            )
        except Exception as exc:  # keep inventory robust for partially written files
            record["error"] = str(exc)
        rows.append(record)
    return rows


def database_summary(name: str) -> dict:
    path = DATABASE_DIR / name
    if not path.exists() or path.suffix != ".db":
        raise FileNotFoundError(name)
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    try:
        cur = conn.cursor()
        counts = {}
        for table in ["persons", "organizations", "positions", "relationships"]:
            try:
                counts[table] = cur.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            except sqlite3.Error:
                counts[table] = None
        return {"name": name, "path": str(path.relative_to(REPO_ROOT)), "counts": counts}
    finally:
        conn.close()


def database_rows(name: str, table: str, limit: int = 500) -> list[dict]:
    if table not in {"persons", "organizations", "positions", "relationships"}:
        raise ValueError(table)
    path = DATABASE_DIR / name
    if not path.exists() or path.suffix != ".db":
        raise FileNotFoundError(name)
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    try:
        return [dict(row) for row in conn.execute(f"SELECT * FROM {table} LIMIT ?", (limit,))]
    finally:
        conn.close()


def static_payload() -> dict:
    inv = collect_inventory()
    dbs = list_databases()
    summaries = []
    for db in dbs:
        try:
            summaries.append(database_summary(db["name"]))
        except Exception as exc:
            summaries.append({"name": db["name"], "error": str(exc)})
    return {
        "inventory": asdict(inv),
        "databases": dbs,
        "database_summaries": summaries,
        "graphs": list_graphs(),
        "reports": list_reports(),
        "person_profiles": list_person_profiles(),
    }


def write_static_site_data(output_dir: Path = DOCS_DIR / "assets" / "data") -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    payload = static_payload()
    for key, value in payload.items():
        (output_dir / f"{key}.json").write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
    index_html = generate_index_html()
    (DOCS_DIR / "index.html").write_text(index_html, encoding="utf-8")
    logger.info("Wrote docs/index.html (auto-generated dashboard)")

    # --- Render Markdown reports to HTML ---
    reports_dir = DOCS_DIR / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for path in sorted(REPORT_DIR.glob("*.md")):
        md_text = path.read_text(encoding="utf-8")
        title = path.stem  # fallback
        m = _RE_H1.search(md_text)
        if m:
            title = m.group(1).strip()
        html = md_to_html(md_text, title)
        out_path = reports_dir / f"{path.stem}.html"
        out_path.write_text(html, encoding="utf-8")
        count += 1
    if count:
        logger.info("Rendered %d Markdown reports to docs/reports/*.html", count)


def _count_todo_tasks(tasks: list[dict]) -> tuple[int, int]:
    """Recursively count (done, total) tasks including sub_tasks."""
    done = 0
    total = 0
    for t in tasks:
        total += 1
        if t.get("done"):
            done += 1
        if "sub_tasks" in t:
            sd, st = _count_todo_tasks(t["sub_tasks"])
            done += sd
            total += st
    return done, total


def generate_index_html(todo_path: str = "data/TODO.json") -> str:
    """Generate a self-contained dark-mode dashboard HTML from TODO.json + live inventory data."""
    todo_full = json.loads((REPO_ROOT / todo_path).read_text(encoding="utf-8"))
    inv = collect_inventory()
    dbs = list_databases()
    graphs = list_graphs()
    reports = list_reports()
    profiles = list_person_profiles()

    meta = todo_full.get("meta", {})

    # --- Stat cards ---
    stat_rows = [
        ("数据库", str(len(dbs)), "个 SQLite"),
        ("关系图", str(len(graphs)), "个 GEXF"),
        ("人物档案", str(len(profiles)), "个 JSON"),
        ("报告", str(len(reports)), "篇 MD/HTML"),
    ]
    stat_cards_html = ""
    for label, value, unit in stat_rows:
        stat_cards_html += f'\n      <div class="stat-card"><b>{value}</b><span>{label} · {unit}</span></div>'

    # --- Province list ---
    provinces = todo_full.get("provinces", [])
    province_cards_html = ""
    for p in provinces:
        pname = p["province"]
        done, total = _count_todo_tasks(p["tasks"])
        pct = done * 100 // total if total else 0
        pct_str = f"{pct}%"
        bar_color = "#D4342E" if pct < 30 else "#B8953E" if pct < 80 else "#6B8FA3"
        province_cards_html += f"""
    <div class="card">
      <div class="label">{pname}</div>
      <div class="title">{done} / {total} 任务</div>
      <div class="bar-wrap"><div class="bar-fill" style="width:{pct_str};background:{bar_color};"></div></div>
      <div class="sub" style="text-align:right;margin-top:0.15rem;">{pct_str}</div>
    </div>"""

    # --- Recent activity (last 10 done tasks, newest first) ---
    recent: list[tuple[str, str, str]] = []  # (province, region, level)
    for p in provinces:
        pname = p["province"]
        for t in p["tasks"]:
            if t.get("done"):
                recent.append((pname, t.get("region", ""), t.get("level", "")))
            for st in t.get("sub_tasks", []):
                if st.get("done"):
                    recent.append((pname, st.get("region", ""), st.get("level", "")))
    recent.sort(key=lambda r: r[1], reverse=False)
    recent = recent[-10:][::-1]
    recent_html = ""
    for pname, region, level in recent:
        recent_html += f"""
      <div class="recent-row"><span class="recent-province">{pname}</span><span class="recent-region">{region}</span><span class="recent-level">{level}</span></div>"""

    if not recent_html:
        recent_html = """      <div class="recent-row" style="color:var(--ink-dim);">暂无完成记录</div>"""

    todo_pct = 0
    if meta.get("total_items"):
        todo_pct = meta.get("finished_items", 0) * 100 // meta["total_items"]

    # ── Build HTML ──
    html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Gov Relation · 政府人员关系网络调研总览</title>
<style>
:root {{
  --surface: #0D0E10;
  --card: #16171B;
  --border: #262830;
  --ink: #E3DFD8;
  --ink-dim: #8A8680;
  --cinnabar: #D4342E;
  --gold: #B8953E;
  --blue: #6B8FA3;
}}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  background: var(--surface); color: var(--ink);
  font-family: system-ui, -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif;
  min-height: 100vh; line-height: 1.6;
}}
.container {{ max-width: 960px; margin: 0 auto; padding: 0 1.5rem; }}

header {{
  padding: 3rem 0 2rem; border-bottom: 1px solid var(--border);
  position: relative;
}}
header::before {{ content: ''; position: absolute; left: 0; top: 0; width: 3px; height: 100%; background: var(--cinnabar); }}
h1 {{ font-size: 1.8rem; font-weight: 800; letter-spacing: 0.03em; }}
header p {{ color: var(--ink-dim); font-size: 0.9rem; margin-top: 0.3rem; }}

.section {{ padding: 2.5rem 0; border-bottom: 1px solid var(--border); }}
h2 {{ font-size: 1.2rem; font-weight: 700; margin-bottom: 1rem; color: var(--gold); }}

.card-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 0.75rem; }}
.card {{
  background: var(--card); border: 1px solid var(--border); border-radius: 2px;
  padding: 1rem 1.2rem; text-decoration: none; color: var(--ink);
  transition: background 0.2s, border-color 0.2s;
}}
.card:hover {{ background: #1E1F24; border-color: #3A3B40; }}
.card .label {{ font-size: 0.6rem; letter-spacing: 0.12em; color: var(--cinnabar); margin-bottom: 0.25rem; }}
.card .title {{ font-size: 0.95rem; font-weight: 700; }}
.card .sub {{ font-size: 0.75rem; color: var(--ink-dim); margin-top: 0.15rem; }}

.bar-wrap {{ background: var(--border); border-radius: 4px; height: 6px; margin-top: 0.4rem; overflow: hidden; }}
.bar-fill {{ height: 100%; border-radius: 4px; transition: width 0.4s; }}

.stat-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 0.75rem; margin-top: 1.5rem; }}
.stat-card {{
  background: var(--card); border: 1px solid var(--border); border-radius: 2px;
  padding: 1rem; text-align: center;
}}
.stat-card b {{ display: block; font-size: 1.5rem; font-weight: 800; color: var(--gold); }}
.stat-card span {{ font-size: 0.62rem; color: var(--ink-dim); letter-spacing: 0.06em; }}

.link-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 0.75rem; }}
.link-card {{
  background: var(--card); border: 1px solid var(--border); border-radius: 2px; border-left: 3px solid var(--blue);
  padding: 1rem 1.2rem; text-decoration: none; color: var(--ink);
  transition: background 0.2s, border-color 0.2s; display: block;
}}
.link-card:hover {{ background: #1E1F24; border-color: #3A3B40; }}
.link-card .label {{ font-size: 0.6rem; letter-spacing: 0.12em; color: var(--blue); margin-bottom: 0.25rem; }}
.link-card .title {{ font-size: 0.95rem; font-weight: 700; }}
.link-card .sub {{ font-size: 0.75rem; color: var(--ink-dim); margin-top: 0.15rem; }}

.recent-list {{ display: flex; flex-direction: column; gap: 0.35rem; }}
.recent-row {{
  display: flex; gap: 1rem; padding: 0.4rem 0.8rem;
  background: var(--card); border: 1px solid var(--border); border-radius: 2px;
  font-size: 0.82rem;
}}
.recent-province {{ color: var(--gold); min-width: 5em; }}
.recent-region {{ flex: 1; }}
.recent-level {{ color: var(--ink-dim); min-width: 4em; text-align: right; }}

.progress-summary {{
  display: flex; gap: 2rem; flex-wrap: wrap; margin: 0.5rem 0 1.5rem;
  font-size: 0.85rem; color: var(--ink-dim);
}}
.progress-summary b {{ color: var(--gold); }}

footer {{ padding: 2rem 0; color: var(--ink-dim); font-size: 0.7rem; }}
footer a {{ color: var(--blue); }}

@media (max-width: 600px) {{
  h1 {{ font-size: 1.3rem; }}
  .card-grid {{ grid-template-columns: 1fr; }}
  .stat-grid {{ grid-template-columns: repeat(2, 1fr); }}
  .link-grid {{ grid-template-columns: 1fr; }}
}}
</style>
</head>
<body>

<header>
  <div class="container">
    <h1>政府人员关系网络 — 调研总览</h1>
    <p>Government Personnel Network Investigation · 多辖区追踪 · 数据驱动</p>
    <div class="stat-grid">
      {stat_cards_html}
    </div>
  </div>
</header>

<!-- Quick Links -->
<section class="section">
  <div class="container">
    <h2>快捷入口</h2>
    <div class="link-grid">
      <a href="app.html" class="link-card">
        <div class="label">EXPLORER</div>
        <div class="title">数据浏览 Explorer</div>
        <div class="sub">浏览数据库、关系图和报告</div>
      </a>
      <a href="../report/graph.html" class="link-card">
        <div class="label">INTERACTIVE GRAPH</div>
        <div class="title">全量关系图谱</div>
        <div class="sub">vis.js 交互网络图</div>
      </a>
    </div>
  </div>
</section>

<!-- Overall Progress -->
<section class="section">
  <div class="container">
    <h2>总体进度</h2>
    <div class="progress-summary">
      <span>总任务: <b>{meta.get("total_items", 0)}</b></span>
      <span>已完成: <b>{meta.get("finished_items", 0)}</b></span>
      <span>剩余: <b>{meta.get("remaining_items", 0)}</b></span>
    </div>
    <div class="bar-wrap" style="height:12px;"><div class="bar-fill" style="width:{todo_pct}%;background:var(--gold);height:12px;"></div></div>
    <div class="sub" style="text-align:right;margin-top:0.25rem;">{todo_pct}%</div>
  </div>
</section>

<!-- Province List -->
<section class="section">
  <div class="container">
    <h2>省份任务进度</h2>
    <div class="card-grid">
      {province_cards_html}
    </div>
  </div>
</section>

<!-- Recent Activity -->
<section class="section">
  <div class="container">
    <h2>最近完成</h2>
    <div class="recent-list">
      {recent_html}
    </div>
  </div>
</section>

<footer>
  <div class="container">
    <p>Government Personnel Network Investigation · 自动生成 · 数据来源 data/TODO.json + 实时盘点</p>
    <p style="margin-top:0.3rem;"><a href="open_gaps.md">Open Gaps Registry</a></p>
  </div>
</footer>

</body>
</html>"""
    return html


class GovRelationHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, directory: str | None = None, **kwargs):
        super().__init__(*args, directory=directory or str(DOCS_DIR), **kwargs)

    def _send_json(self, data: object, status: int = 200) -> None:
        raw = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = unquote(parsed.path)
        try:
            if path == "/api/inventory":
                return self._send_json(asdict(collect_inventory()))
            if path == "/api/databases":
                return self._send_json(list_databases())
            if path.startswith("/api/database/"):
                parts = path.split("/")
                name = parts[3]
                if len(parts) == 5 and parts[4] in {"persons", "organizations", "positions", "relationships"}:
                    return self._send_json(database_rows(name, parts[4]))
                return self._send_json(database_summary(name))
            if path == "/api/graphs":
                return self._send_json(list_graphs())
            if path == "/api/reports":
                return self._send_json(list_reports())
            if path == "/api/person-profiles":
                return self._send_json(list_person_profiles())
        except Exception as exc:
            return self._send_json({"error": str(exc)}, status=404)
        return super().do_GET()


def serve(host: str = "127.0.0.1", port: int = 8000) -> ThreadingHTTPServer:
    server = ThreadingHTTPServer((host, port), GovRelationHandler)
    return server

