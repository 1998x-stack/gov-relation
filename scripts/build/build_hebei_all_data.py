#!/usr/bin/env python3
"""
build_hebei_all_data.py — Batch build script generator for Hebei county/district investigations.

Reads per-city research JSON data, generates individual build_{slug}_data.py scripts
for each district/county under a Hebei prefecture city, optionally executes them,
and marks tasks complete via run_todo_loop.py.

Usage:
    python3 build_hebei_all_data.py --city 石家庄市 --input shijiazhuang_research.json
    python3 build_hebei_all_data.py --city 石家庄市 --input shijiazhuang_research.json --run
    python3 build_hebei_all_data.py --help
"""

import json
import os
import sqlite3
import subprocess
import sys
from datetime import date

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SLUG_MAP: dict[str, str] = {}


def load_administrative_divisions() -> dict:
    """Load hebei_administrative_divisions.json to get city→regions mapping."""
    path = os.path.join(PROJECT_ROOT, "data/json/hebei_administrative_divisions.json")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    city_map: dict[str, list[dict]] = {}
    for city in data["cities"]:
        name = city["name"]
        regions: list[dict] = []
        kind_map = {"districts": "市辖区", "counties": "县", "county_level_cities": "县级市"}
        for key, level_label in kind_map.items():
            for r in city.get(key, []):
                regions.append({"region": r, "level": level_label, "parent_city": name})
        city_map[name] = regions
    return city_map


def region_slug(region: str) -> str:
    """Generate a slug for a region name.

    Uses the SLUG_MAP if populated. Otherwise:
    - Chinese characters in region name are kept as-is (consistent with existing files
      like build_渝水区_data.py, build_上栗县_data.py)
    """
    if region in SLUG_MAP:
        return SLUG_MAP[region]
    return region


def esc_xml(s: str | None) -> str:
    """Escape XML special characters."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace(
        '"', "&quot;"
    ).replace("'", "&apos;")


def person_color_by_role(role: str) -> tuple[int, int, int]:
    """Return (r,g,b) for a person based on their current_post."""
    s = str(role)
    if "党委书记" in s or "书记" in s:
        return (220, 30, 30)   # red = party secretary
    if "市长" in s or "区长" in s or "县长" in s:
        return (40, 100, 220)  # blue = government head
    if "副市长" in s or "副区长" in s or "副县长" in s:
        return (40, 140, 220)  # light blue = deputy
    if "纪委书记" in s or "纪检" in s:
        return (180, 130, 50)  # orange = discipline
    if "人大" in s or "政协" in s:
        return (220, 160, 40)  # orange = NPC/CPPCC
    if "副书记" in s:
        return (180, 60, 180)  # purple = deputy secretary
    if "部长" in s or "政法委" in s:
        return (120, 120, 120)  # grey = standing committee
    return (160, 160, 160)  # grey = other


def org_color_by_type(org_type: str) -> tuple[int, int, int]:
    t = str(org_type)
    if "党委" in t:
        return (200, 60, 60)
    if "政府" in t or "公安" in t:
        return (60, 100, 200)
    if "人大" in t:
        return (200, 150, 40)
    if "政协" in t:
        return (200, 150, 40)
    if "纪委" in t:
        return (160, 120, 40)
    if "纪委" in t:
        return (160, 120, 40)
    return (120, 120, 120)


def generate_build_script(
    slug: str,
    region: str,
    parent_city: str,
    level: str,
    findings: str,
    persons: list[dict],
    task_id: str,
) -> str:
    """Generate a complete build_{slug}_data.py script as a string.

    Follows the exact pattern of build_湘东区_data.py and build_anyuan_data.py.
    """
    slug_id = slug  # used for prefixing IDs
    db_path = os.path.join(PROJECT_ROOT, f"data/database/{slug}_network.db")
    gexf_path = os.path.join(PROJECT_ROOT, f"data/graph/{slug}_network.gexf")

    # Build PERSONS list
    persons_tuples = []
    org_map: dict[str, str] = {}  # org_name -> org_id
    positions_list: list[tuple] = []
    relationships_list: list[tuple] = []

    if not persons:
        # Placeholder: at least one entry
        persons_tuples.append(
            (
                f"{slug_id}_sec_01",
                "（待确认）",
                "男",
                "汉族",
                "待查",
                "待查",
                "待查",
                "待查",
                "待查",
                f"{region}委书记（待确认）",
                f"中共{parent_city}{region}委员会",
                f"⚠️ 待确认：{region}暂无公开数据",
            )
        )

    for i, p in enumerate(persons):
        pid = f"{slug_id}_p{i + 1:02d}"
        persons_tuples.append(
            (
                pid,
                p.get("name", "（待确认）"),
                p.get("gender", ""),
                p.get("ethnicity", ""),
                p.get("birth", ""),
                p.get("birthplace", ""),
                p.get("education", ""),
                p.get("party_join", ""),
                p.get("work_start", ""),
                p.get("current_post", ""),
                p.get("current_org", ""),
                p.get("source", ""),
            )
        )

        # Auto-create org from current_org if present
        current_org = p.get("current_org", "")
        if current_org and current_org not in org_map:
            org_key = f"{slug_id}_org_{len(org_map) + 1}"
            org_map[current_org] = org_key

        # Auto-generate position from current_post/current_org
        cpost = p.get("current_post", "")
        corg = p.get("current_org", "")
        if cpost and corg and corg in org_map:
            positions_list.append(
                (
                    pid,
                    org_map[corg],
                    cpost,
                    p.get("work_start", ""),
                    "至今",
                    "",
                    p.get("source", ""),
                )
            )
            # If this person has a party-related role, link to party org
            party_org_key = f"{slug_id}_party"
            if "书记" in cpost or "区长" in cpost or "县长" in cpost:
                positions_list.append(
                    (
                        pid,
                        party_org_key,
                        cpost,
                        p.get("work_start", ""),
                        "至今",
                        "",
                        "兼任" if "书记" not in cpost else "主要负责人",
                    )
                )

    # Build ORGANIZATIONS list with auto-detected orgs
    orgs_list: list[tuple] = []
    # Standard orgs for the region
    party_org = f"中共{parent_city}{region}委员会" if parent_city else f"中共{region}委员会"
    gov_org = f"{region}人民政府"
    standard_orgs = [
        (f"{slug_id}_party", party_org, "党委", level, f"中共{parent_city}委员会" if parent_city else "", f"河北省{parent_city}{region}" if parent_city else f"河北省{region}"),
        (f"{slug_id}_gov", gov_org, "政府", level, f"{parent_city}人民政府" if parent_city else "", f"河北省{parent_city}{region}" if parent_city else f"河北省{region}"),
    ]
    orgs_list.extend(standard_orgs)

    for org_name, org_key in org_map.items():
        if org_key not in [o[0] for o in orgs_list]:
            org_type = "党委部门" if "委员会" in org_name or "委" in org_name else "政府"
            orgs_list.append(
                (org_key, org_name, org_type, level, f"{parent_city}人民政府" if parent_city else "", f"河北省{parent_city}{region}" if parent_city else f"河北省{region}")
            )

    # Escape helper
    def pyesc(s: str) -> str:
        return s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")

    today_str = date.today().isoformat()
    description = f"{parent_city}{region}领导班子工作关系网络 — {today_str}"
    if not persons:
        description += "（⚠️ 数据待补充）"

    # Build the org/positions/relationships sections as JSON strings
    persons_json = json.dumps(
        [[pyesc(str(x)) for x in pt] for pt in persons_tuples],
        ensure_ascii=False,
        indent=4,
    )
    orgs_json = json.dumps(
        [[pyesc(str(x)) for x in ot] for ot in orgs_list],
        ensure_ascii=False,
        indent=4,
    )
    positions_json = json.dumps(
        [[pyesc(str(x)) for x in pt] for pt in positions_list],
        ensure_ascii=False,
        indent=4,
    )
    relationships_json = json.dumps(
        [[pyesc(str(x)) for x in rt] for rt in relationships_list],
        ensure_ascii=False,
        indent=4,
    )

    gexf_description = f"{parent_city}{region}领导班子工作关系网络"
    parentheses_title = f"{parent_city}{region}领导班子工作关系网络"

    # Template with placeholder markers for baking in values
    TEMPLATE = '''#!/usr/bin/env python3
"""
__DESCRIPTION__
Build script generated by build_hebei_all_data.py

Generated from: __PARENT_CITY__ research data
Number of persons sourced: __PERSONS_COUNT__
"""

import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data/database/__SLUG___network.db")
GEXF_PATH = os.path.join(BASE_DIR, "data/graph/__SLUG___network.gexf")

# ── PERSONS ──
# (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
PERSONS = __PERSONS_JSON__

# ── ORGANIZATIONS ──
# (id, name, type, level, parent, location)
ORGANIZATIONS = __ORGS_JSON__

# ── POSITIONS ──
# (person_id, org_id, title, start, end, rank, note)
POSITIONS = __POSITIONS_JSON__

# ── RELATIONSHIPS ──
# (person_a, person_b, type, context, overlap_org, overlap_period)
RELATIONSHIPS = __RELATIONSHIPS_JSON__


# ── HELPERS ──

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&apos;")


def person_color(p):
    name = p[0]
    role = p[9] or ""
    if "书记" in role and "纪委" not in role and "副书记" not in role:
        return "220,30,30"
    if "区长" in role or "县长" in role or "市长" in role:
        return "40,100,220"
    if "副区长" in role or "副县长" in role or "副市长" in role:
        return "40,140,220"
    if "纪委书记" in role:
        return "180,130,50"
    if "人大" in role or "政协" in role:
        return "220,160,40"
    if "副书记" in role:
        return "180,60,180"
    if "部长" in role or "政法委" in role:
        return "120,120,120"
    return "160,160,160"


def person_size(p):
    role = p[9] or ""
    if "区委书记" in role or "县委书记" in role or "市委书记" in role:
        return "20.0"
    if "区长" in role or "县长" in role or "市长" in role:
        return "18.0"
    if "副书记" in role:
        return "16.0"
    if "人大" in role or "政协" in role:
        return "14.0"
    return "12.0"


def org_color(o):
    t = o[2] or ""
    if "党委" in t: return "200,60,60"
    if "政府" in t or "公安" in t: return "60,100,200"
    if "人大" in t or "政协" in t: return "200,150,40"
    if "纪委" in t: return "160,120,40"
    return "120,120,120"


# ── BUILD DATABASE ──

def create_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id TEXT PRIMARY KEY,
            name TEXT,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id TEXT PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT NOT NULL,
            org_id TEXT NOT NULL,
            title TEXT NOT NULL,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT NOT NULL,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in PERSONS:
        c.execute("""
            INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, p)

    for o in ORGANIZATIONS:
        c.execute("""
            INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, o)

    for pos in POSITIONS:
        c.execute("""
            INSERT INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, pos)

    for r in RELATIONSHIPS:
        c.execute("""
            INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?)
        """, r)

    conn.commit()
    conn.close()
    print(f"\\u2705 Database created: {DB_PATH}")


# ── BUILD GEXF ──

def generate_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3"')
    lines.append('      xmlns:viz="http://gexf.net/1.3/viz"')
    lines.append('      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"')
    lines.append('      xsi:schemaLocation="http://gexf.net/1.3 http://gexf.net/1.3/gexf.xsd"')
    lines.append('      version="1.3">')
    lines.append('  <meta>')
    lines.append('    <creator>China-Gov-Network Investigation</creator>')
    lines.append(f'    <description>{esc("__GEXF_DESCRIPTION__")}</description>')
    lines.append(f'    <date>__DATE__</date>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="type" title="Node Type" type="string"/>')
    lines.append('      <attribute id="role" title="Role" type="string"/>')
    lines.append('      <attribute id="org_type" title="Org Type" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="type" title="Edge Type" type="string"/>')
    lines.append('      <attribute id="start" title="Start Date" type="string"/>')
    lines.append('      <attribute id="end" title="End Date" type="string"/>')
    lines.append('      <attribute id="rank" title="Rank" type="string"/>')
    lines.append('      <attribute id="strength" title="Strength" type="string"/>')
    lines.append('      <attribute id="context" title="Context" type="string"/>')
    lines.append('    </attributes>')

    # Nodes - Persons
    lines.append('    <nodes>')
    for p in PERSONS:
        pid = p[0]
        label = p[1]
        role = p[9] or ""
        birth = p[4] or ""
        birthplace = p[5] or ""
        c = person_color(p)
        sz = person_size(p)
        rgb = c.split(",")
        lines.append(f'      <node id="__PID__" label="__LABEL__">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="type" value="person"/>')
        lines.append(f'          <attvalue for="role" value="__ROLE__"/>')
        lines.append(f'          <attvalue for="birth" value="__BIRTH__"/>')
        lines.append(f'          <attvalue for="birthplace" value="__BIRTHPLACE__"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="__R__" g="__G__" b="__B__" a="1.0"/>')
        lines.append(f'        <viz:size value="__SZ__"/>')
        lines.append('      </node>')

    # Nodes - Organizations
    for o in ORGANIZATIONS:
        oid = o[0]
        label = o[1]
        c = org_color(o)
        rgb = c.split(",")
        lines.append(f'      <node id="__OID__" label="__OLABEL__">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="type" value="org"/>')
        lines.append(f'          <attvalue for="org_type" value="__OTYPE__"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="__OR__" g="__OG__" b="__OB__" a="1.0"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('        <viz:shape value="square"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')
    for pos in POSITIONS:
        eid += 1
        pid, oid, title, start, end, rank, note = pos
        lines.append(f'      <edge id="e__EID__" source="__EPID__" target="__EOID__" type="directed" label="__ETITLE__">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="type" value="worked_at"/>')
        lines.append(f'          <attvalue for="start" value="__ESTART__"/>')
        lines.append(f'          <attvalue for="end" value="__EEND__"/>')
        lines.append(f'          <attvalue for="rank" value="__ERANK__"/>')
        lines.append('        </attvalues>')
        lines.append('        <viz:color r="80" g="80" b="80" a="0.5"/>')
        lines.append('        <viz:thickness value="1.0"/>')
        lines.append('      </edge>')

    for r in RELATIONSHIPS:
        eid += 1
        a, b, typ, context, overlap_org, overlap_period = r
        is_strong = "强关系" in str(typ)
        cr, cg_val, cb = (184, 149, 62) if is_strong else (91, 139, 192)
        thickness = 2.5 if is_strong else 1.5
        lines.append(f'      <edge id="e__EID__" source="__ERA__" target="__ERB__" type="undirected" label="__ERCONTEXT__">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="type" value="relationship"/>')
        lines.append(f'          <attvalue for="strength" value="__ERTYP__"/>')
        lines.append(f'          <attvalue for="context" value="__ERCONTEXT2__"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="__CR__" g="__CG__" b="__CB__" a="0.8"/>')
        lines.append(f'        <viz:thickness value="__THICK__"/>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\\n".join(lines))
    print(f"\\u2705 GEXF graph created: {GEXF_PATH}")


# ── STATS ──

def print_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for table in ["persons", "organizations", "positions", "relationships"]:
        c.execute(f"SELECT COUNT(*) FROM {{table}}")
        cnt = c.fetchone()[0]
        print(f"  {{table}}: {{cnt}}")
        if table == "persons":
            c.execute("SELECT COUNT(*) FROM persons WHERE source LIKE '%待确认%'")
            pending = c.fetchone()[0]
            print(f"    └─ 待确认: {{pending}}, 已确认: {{cnt - pending}}")
    conn.close()


if __name__ == "__main__":
    print("=" * 60)
    print(f"  __PARENTHESES_TITLE__")
    print(f"  等级: __LEVEL__")
    print("=" * 60)
    create_db()
    generate_gexf()
    print("\\n\\U0001f4ca Summary:")
    print_stats()
    print("\\n\\u2705 Done.")
'''

    # Bake in values
    script = (
        TEMPLATE
        .replace("__DESCRIPTION__", description)
        .replace("__PARENT_CITY__", parent_city)
        .replace("__PERSONS_COUNT__", str(len(persons)))
        .replace("__SLUG__", slug)
        .replace("__PERSONS_JSON__", persons_json)
        .replace("__ORGS_JSON__", orgs_json)
        .replace("__POSITIONS_JSON__", positions_json)
        .replace("__RELATIONSHIPS_JSON__", relationships_json)
        .replace("__GEXF_DESCRIPTION__", gexf_description)
        .replace("__DATE__", today_str)
        .replace("__PARENTHESES_TITLE__", parentheses_title)
        .replace("__LEVEL__", level)
    )

    return script


def generate_region_scripts(
    city_name: str,
    regions: list[dict],
    research_data: list[dict],
    do_run: bool,
) -> list[dict]:
    """Generate build scripts for all regions of a city.

    Args:
        city_name: City name in Chinese (e.g., 石家庄市)
        regions: List of {region, level, parent_city} dicts from admin divisions
        research_data: JSON research data list (from --input file)
        do_run: If True, also execute each generated script

    Returns:
        List of result dicts with region, script_path, success status
    """
    # Build research lookup: region_name -> research entry
    research_lookup: dict[str, dict] = {}
    for entry in research_data:
        rname = entry.get("region", "")
        research_lookup[rname] = entry

    results: list[dict] = []

    for ri, region_info in enumerate(regions):
        region = region_info["region"]
        level = region_info["level"]
        slug = region_slug(region)
        research_entry = research_lookup.get(region, {})
        persons = research_entry.get("persons", [])
        task_id = research_entry.get("task_id", f"hebei_{region}")
        findings = research_entry.get("findings", "")

        script_content = generate_build_script(
            slug=slug,
            region=region,
            parent_city=city_name,
            level=level,
            findings=findings,
            persons=persons,
            task_id=task_id,
        )

        script_path = os.path.join(PROJECT_ROOT, f"build_{slug}_data.py")

        # Check for overwrite
        if os.path.exists(script_path):
            print(f"⚠️  WARNING: {script_path} already exists. Overwriting.")

        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script_content)
        print(f"✅ Generated: build_{slug}_data.py ({region})")

        result = {
            "region": region,
            "slug": slug,
            "script_path": script_path,
            "persons_count": len(persons),
            "task_id": task_id,
        }

        if do_run:
            print(f"\n  ▶ Running build_{slug}_data.py ...")
            try:
                proc = subprocess.run(
                    [sys.executable, script_path],
                    cwd=PROJECT_ROOT,
                    capture_output=False,
                    timeout=300,
                )
                result["run_success"] = proc.returncode == 0
                if proc.returncode != 0:
                    print(f"  ❌ Script failed with exit code {proc.returncode}")
                    result["run_error"] = proc.stderr.decode("utf-8", errors="replace") if proc.stderr else ""
                else:
                    print(f"  ✅ Script completed successfully")
                    # Mark task done in TODO.json
                    subprocess.run(
                        [sys.executable, "run_todo_loop.py", "--mark-done", task_id],
                        cwd=PROJECT_ROOT,
                        capture_output=True,
                    )
                    print(f"  ✅ Marked task '{task_id}' as done")
            except subprocess.TimeoutExpired:
                print(f"  ⏰ Script timed out after 300s")
                result["run_success"] = False
                result["run_error"] = "Timeout expired"
            except Exception as e:
                print(f"  ❌ Script execution error: {e}")
                result["run_success"] = False
                result["run_error"] = str(e)

        results.append(result)

    return results


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="Build Hebei batch scripts — generate build_{slug}_data.py scripts "
                    "for every district/county of a Hebei prefecture city, optionally execute them."
    )
    parser.add_argument(
        "--city",
        required=True,
        help="City name in Chinese (e.g., 石家庄市, 唐山市)",
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Path to JSON research data file for this city",
    )
    parser.add_argument(
        "--run",
        action="store_true",
        help="Also execute each generated build script",
    )
    args = parser.parse_args()

    city_name: str = args.city
    input_path: str = args.input
    do_run: bool = args.run

    # Load administrative divisions
    city_region_map = load_administrative_divisions()

    if city_name not in city_region_map:
        print(f"❌ City '{city_name}' not found in Hebei administrative divisions.")
        print(f"   Available cities: {', '.join(city_region_map.keys())}")
        sys.exit(1)

    regions = city_region_map[city_name]

    # Load research JSON
    if not os.path.exists(input_path):
        print(f"❌ Input file not found: {input_path}")
        sys.exit(1)

    with open(input_path, encoding="utf-8") as f:
        research_data = json.load(f)

    if not isinstance(research_data, list):
        print("❌ Input JSON must be a top-level array of research entries.")
        sys.exit(1)

    print(f"\n{'=' * 60}")
    print(f"  Hebei Batch Builder — {city_name}")
    print(f"  Regions to process: {len(regions)}")
    print(f"  Research entries:   {len(research_data)}")
    print(f"  Execute scripts:    {'Yes' if do_run else 'No (--run not set)'}")
    print(f"{'=' * 60}\n")

    results = generate_region_scripts(city_name, regions, research_data, do_run)

    # Print summary
    print(f"\n{'=' * 60}")
    print(f"  SUMMARY — {city_name}")
    print(f"{'=' * 60}")
    generated = len(results)
    persons_total = sum(r["persons_count"] for r in results)
    success_count = sum(1 for r in results if r.get("run_success"))
    fail_count = sum(1 for r in results if r.get("run_success") is False)
    not_run = sum(1 for r in results if "run_success" not in r)

    print(f"  Scripts generated: {generated}")
    print(f"  Total persons:     {persons_total}")
    if do_run:
        print(f"  Executed:          {success_count} ✅ / {fail_count} ❌")
    else:
        print(f"  Executed:          {not_run} (skipped, use --run)")

    if not_run > 0:
        print(f"\n  To execute: python3 {os.path.basename(__file__)} --city {city_name} --input {input_path} --run")

    print()


if __name__ == "__main__":
    main()
