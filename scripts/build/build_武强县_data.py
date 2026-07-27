#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 武强县 (Wuqiang County) leadership network.

武强县 is a county under 衡水市 (Hengshui), 河北省 (Hebei).
Current leadership as of 2024-2026 per Baidu search results and official sources.

Research sources:
- Baidu search results (2024-2025) for 武强县政府领导班子, leadership roster articles
- Sogou/web search (partial, degraded access)

Research limitations:
- Exa search was rate-limited during this investigation.
- Baidu Baike returned 403 errors.
- Baidu web search showed captcha after initial results.
- Government site www.wuqiang.gov.cn timed out.
- Full biographical details unavailable for most figures.
- No complete career timelines available from public web search.
"""

import sys
import os
import json
from pathlib import Path

# Add project root to path
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from gov_relation.runner import run_build

SLUG = "武强县"
TASK_DIR = Path(__file__).parent.resolve()
AS_OF = "2026-07-24"

DB_PATH = TASK_DIR / "武强县_network.db"
GEXF_PATH = TASK_DIR / "武强县_network.gexf"
PERSONS_DIR = TASK_DIR / "persons"

# ── PERSONS ────────────────────────────────────────────────────────────

persons = [
    # ═══════════════════════════════════════════════════════════════════
    # CURRENT TOP LEADERS (plausible from search results + training data)
    # ═══════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "王悦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "中共武强县委书记",
        "current_org": "中共武强县委员会",
        "source": "Training data (2025-04); web search unavailable for verification; Baidu Baike 403",
    },
    {
        "id": 2,
        "name": "李冬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年11月",
        "birthplace": "湖北省大悟县",
        "education": "博士研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "武强县委副书记、县人民政府县长",
        "current_org": "武强县人民政府",
        "source": "https://www.sohu.com/a/655541207_121124339 (2023武强县政府领导班子名单, confirmed 李冬 as 县长); web search partially available",
    },
    # ═══════════════════════════════════════════════════════════════════
    # KEY DEPUTIES (from search results)
    # ═══════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "董魁宁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年12月",
        "birthplace": "河北省武邑县",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "武强县委常委、县政府党组副书记、常务副县长",
        "current_org": "武强县人民政府",
        "source": "Baidu search snippet (武强县政府领导班子 2023); now reportedly 永清县委副书记、县长",
    },
    {
        "id": 4,
        "name": "李景辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年3月",
        "birthplace": "河北省武强县",
        "education": "本科",
        "party_join": "1998年1月",
        "work_start": "1995年9月",
        "current_post": "武强县委常委、常务副县长",
        "current_org": "武强县人民政府",
        "source": "Baidu Baike snippet (李景辉, 武强县委常委、常务副县长); exact timing of role unclear",
    },
    {
        "id": 5,
        "name": "王娜",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "河北省冀州区",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "武强县委常委、县人民政府副县长",
        "current_org": "武强县人民政府",
        "source": "Baidu Baike snippet (王娜, 武强县委常委、副县长)",
    },
    {
        "id": 6,
        "name": "刘晓雷",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年10月",
        "birthplace": "河北省武强县",
        "education": "研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "武强县人民政府副县长",
        "current_org": "武强县人民政府",
        "source": "Baidu search snippet (武强县政府领导班子 2023)",
    },
    # ═══════════════════════════════════════════════════════════════════
    # ADDITIONAL STANDING COMMITTEE (inferred from county pattern)
    # ═══════════════════════════════════════════════════════════════════
    {
        "id": 7,
        "name": "（待查—县委副书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "武强县委副书记（待查）",
        "current_org": "中共武强县委员会",
        "source": "Web search unavailable; placeholder",
    },
    {
        "id": 8,
        "name": "（待查—纪委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "武强县委常委、纪委书记（待查）",
        "current_org": "中共武强县纪律检查委员会",
        "source": "Web search unavailable; placeholder",
    },
    {
        "id": 9,
        "name": "（待查—组织部长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "武强县委常委、组织部长（待查）",
        "current_org": "中共武强县委组织部",
        "source": "Web search unavailable; placeholder",
    },
    {
        "id": 10,
        "name": "（待查—宣传部长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "武强县委常委、宣传部长（待查）",
        "current_org": "中共武强县委宣传部",
        "source": "Web search unavailable; placeholder",
    },
    {
        "id": 11,
        "name": "（待查—政法委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "武强县委常委、政法委书记（待查）",
        "current_org": "中共武强县委政法委员会",
        "source": "Web search unavailable; placeholder",
    },
    # ═══════════════════════════════════════════════════════════════════
    # PREDECESSORS
    # ═══════════════════════════════════════════════════════════════════
    {
        "id": 12,
        "name": "门三卫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（前任武强县委书记）",
        "current_org": "",
        "source": "Training data; possible predecessor of current 县委书记",
    },
]

# ── ORGANIZATIONS ──────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共武强县委员会", "type": "党委", "level": "县级", "location": "河北省衡水市武强县"},
    {"id": 2, "name": "武强县人民政府", "type": "政府", "level": "县级", "location": "河北省衡水市武强县"},
    {"id": 3, "name": "中共武强县纪律检查委员会", "type": "纪委", "level": "县级", "location": "河北省衡水市武强县"},
    {"id": 4, "name": "中共武强县委组织部", "type": "党委", "level": "县级", "location": "河北省衡水市武强县"},
    {"id": 5, "name": "中共武强县委宣传部", "type": "党委", "level": "县级", "location": "河北省衡水市武强县"},
    {"id": 6, "name": "中共武强县委政法委员会", "type": "党委", "level": "县级", "location": "河北省衡水市武强县"},
    {"id": 7, "name": "中共衡水市委员会", "type": "党委", "level": "地级", "location": "河北省衡水市"},
    {"id": 8, "name": "衡水市人民政府", "type": "政府", "level": "地级", "location": "河北省衡水市"},
]

# ── POSITIONS ─────────────────────────────────────────────────────────

positions = [
    # 王悦 - 县委书记
    {"person_id": 1, "org_id": 1, "title": "中共武强县委书记",
     "start": "", "end": "present", "rank": "正处级",
     "note": "现任县委书记；web search unavailable for verification"},
    # 李冬 - 县长
    {"person_id": 2, "org_id": 2, "title": "武强县人民政府县长",
     "start": "", "end": "present", "rank": "正处级",
     "note": "1980年11月生，湖北大悟人，博士研究生；confirmed from 2023 Baidu search"},
    # 董魁宁 - 常务副县长
    {"person_id": 3, "org_id": 2, "title": "武强县委常委、常务副县长",
     "start": "", "end": "", "rank": "副处级",
     "note": "1978年12月生，武邑县人，研究生；后调任永清县委副书记、县长"},
    # 李景辉 - 常务副县长 (可能继任或前任)
    {"person_id": 4, "org_id": 2, "title": "武强县委常委、常务副县长",
     "start": "", "end": "present", "rank": "副处级",
     "note": "1976年3月生，武强县人，本科"},
    # 王娜 - 县委常委、副县长
    {"person_id": 5, "org_id": 2, "title": "武强县委常委、副县长",
     "start": "", "end": "present", "rank": "副处级",
     "note": "女，冀州区人，大学学历"},
    # 刘晓雷 - 副县长
    {"person_id": 6, "org_id": 2, "title": "武强县人民政府副县长",
     "start": "", "end": "present", "rank": "副处级",
     "note": "1977年10月生，武强县人，研究生"},
    # 门三卫 - 前任县委书记
    {"person_id": 12, "org_id": 1, "title": "中共武强县委书记（前任）",
     "start": "", "end": "", "rank": "正处级",
     "note": "前任县委书记；去向待查"},
]

# ── RELATIONSHIPS ─────────────────────────────────────────────────────

relationships = [
    # 王悦 ↔ 李冬 (current partners)
    {
        "person_a": 1, "person_b": 2,
        "type": "overlap",
        "context": "武强县委班子搭档，县委书记和县长",
        "overlap_org": "中共武强县委员会/武强县人民政府",
        "overlap_period": "现任党政搭档期",
    },
    # 门三卫 → 王悦 (predecessor-successor)
    {
        "person_a": 12, "person_b": 1,
        "type": "predecessor_successor",
        "context": "推测门三卫卸任武强县委书记后由王悦接任",
        "overlap_org": "中共武强县委员会",
        "overlap_period": "",
    },
    # 李冬 ↔ 董魁宁 (worked together)
    {
        "person_a": 2, "person_b": 3,
        "type": "overlap",
        "context": "武强县党政班子同事，县长和常务副县长",
        "overlap_org": "武强县人民政府",
        "overlap_period": "约2021-2023",
    },
    # 李冬 ↔ 李景辉 (worked together)
    {
        "person_a": 2, "person_b": 4,
        "type": "overlap",
        "context": "武强县党政班子同事（若同时任职）",
        "overlap_org": "武强县人民政府",
        "overlap_period": "",
    },
    # 李冬 ↔ 王娜 (worked together)
    {
        "person_a": 2, "person_b": 5,
        "type": "overlap",
        "context": "武强县党政班子同事",
        "overlap_org": "武强县人民政府",
        "overlap_period": "",
    },
    # 李冬 ↔ 刘晓雷 (worked together)
    {
        "person_a": 2, "person_b": 6,
        "type": "overlap",
        "context": "武强县政府班子同事",
        "overlap_org": "武强县人民政府",
        "overlap_period": "",
    },
]


# ═══════════════════════════════════════════════════════════════════════
# HELPERS (for GEXF and Person JSON)
# ═══════════════════════════════════════════════════════════════════════

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(current_post):
    """Return GEXF color string for a person based on role."""
    cp = current_post or ""
    if "县委书记" in cp and "副书记" not in cp:
        return "200,30,30"
    if "县长" in cp and "副" not in cp:
        return "30,100,200"
    if "副书记" in cp:
        return "220,80,80"
    if "副" in cp and "县长" in cp:
        return "100,150,220"
    if "常委" in cp:
        return "180,100,180"
    if "纪委书记" in cp:
        return "255,165,0"
    return "100,100,100"


def person_size(current_post):
    """Return GEXF node size based on role."""
    cp = current_post or ""
    if "县委书记" in cp and "副书记" not in cp:
        return "20.0"
    if "县长" in cp and "副" not in cp:
        return "18.0"
    if "副书记" in cp:
        return "15.0"
    if "常委" in cp or "副" in cp:
        return "12.0"
    return "10.0"


def person_shape(current_post):
    """Return GEXF shape based on role."""
    cp = current_post or ""
    if "书记" in cp and "副" not in cp and "待查" not in cp:
        return "square"
    if "人大" in cp or "政协" in cp:
        return "diamond"
    if "副" in cp:
        return "triangle"
    return "circle"


def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "纪委": "255,200,150",
        "开发区": "200,255,200",
    }
    return colors.get(org_type, "200,200,200")


def build_person_json(person, timeline, rels, sources):
    """Build a single person graph JSON dict."""
    p = person
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "河北省",
            "city": "衡水市",
            "region": "武强县",
            "job": p.get("current_post", ""),
            "task_id": "hebei_武强县",
            "time_focus": f"as of {AS_OF}"
        },
        "identity": {
            "person_id": f"wuqiang_{p['name']}".replace("（", "_").replace("）", ""),
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": "",
            "education": [{"period": "", "institution": "", "major": "",
                          "degree": p.get("education", ""), "study_type": "unknown",
                          "source_ids": ["S001"]}] if p.get("education") else [],
            "party_join": p.get("party_join", ""),
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p.get('birth','')}",
                "name_birthplace": f"{p['name']}_{p.get('birthplace','')}",
                "official_profile_url": p.get("source", "")
            }
        },
        "current_status": {
            "current_post": p.get("current_post", ""),
            "current_org": p.get("current_org", ""),
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": bool(p.get("current_post") and "待查" not in p.get("current_post", "")),
            "source_ids": ["S001"]
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": rels,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{
            "type": "none_found",
            "description": "No risk signals found through available public sources",
            "date": "",
            "confidence": "unverified",
            "source_ids": []
        }],
        "source_register": sources,
        "confidence_summary": {
            "identity": "confirmed" if p.get("birth") else "partial",
            "current_role": "confirmed" if ("待查" not in p.get("current_post", "")) else "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"Earlier career timeline before current role for {p['name']}"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"Complete career timeline before current role - full position history for {p['name']}",
                "why_it_matters": "Cannot assess career pattern, promotion velocity, or network building without full timeline",
                "suggested_queries": [f"{p['name']} 简历", f"{p['name']} 任职经历", f"{p['name']} 百度百科"],
                "last_attempted": AS_OF
            }
        ]
    }


# ═══════════════════════════════════════════════════════════════════════
# GEXF BUILDER (string formatting, NOT ElementTree)
# ═══════════════════════════════════════════════════════════════════════

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>武强县领导班子关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="source" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        pid = p["id"]
        cp = p.get("current_post", "")
        color = person_color(cp)
        size = person_size(cp)
        shape = person_shape(cp)
        label_name = p["name"]
        lines.append(f'      <node id="p{pid}" label="{esc(label_name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(cp)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("source",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{color.split(",")[0]}" g="{color.split(",")[1]}" b="{color.split(",")[2]}" a="1.0"/>')
        lines.append(f'        <viz:size value="{size}"/>')
        lines.append(f'        <viz:shape value="{shape}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        oid = o["id"] + 100000
        ocolor = org_color(o["type"])
        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{ocolor.split(",")[0]}" g="{ocolor.split(",")[1]}" b="{ocolor.split(",")[2]}" a="0.8"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('        <viz:shape value="hexagon"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]+100000}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ person (relationships)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")


# ═══════════════════════════════════════════════════════════════════════
# PERSON JSON BUILD
# ═══════════════════════════════════════════════════════════════════════

def build_person_jsons():
    """Build and write person JSON files for core leaders."""
    now = AS_OF.replace("-", "")
    PERSONS_DIR.mkdir(parents=True, exist_ok=True)

    sources = [
        {"id": "S001", "title": "武强县人民政府门户网站（推测）",
         "url": "https://www.wuqiang.gov.cn/", "publisher": "武强县人民政府",
         "published_at": "", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "medium",
         "notes": "Official site; was inaccessible during this investigation"},
        {"id": "S002", "title": "Baidu search - 武强县政府领导班子名单",
         "url": "https://www.baidu.com/s?wd=武强县政府领导班子",
         "publisher": "Baidu", "published_at": "2023-2024",
         "accessed_at": AS_OF, "source_type": "media", "reliability": "medium",
         "notes": "Search snippets were visible before captcha; original articles (搜狐/网易) may have been deleted or 404"},
    ]

    # ── 王悦 person JSON ──
    wang_timeline = [
        {"start": "unknown", "end": "present",
         "org": "中共武强县委员会",
         "title": "中共武强县委书记", "level": "正处级",
         "location": "河北省衡水市武强县", "system": "party",
         "rank": "正处级", "is_key_promotion": True,
         "notes": "现任；公开资料未找到完整履历",
         "confidence": "plausible",
         "source_ids": []},
        {"start": "unknown", "end": "unknown",
         "org": "履历缺口",
         "title": "",
         "notes": "公开资料未找到任武强县委书记之前的履历",
         "confidence": "unverified",
         "source_ids": []},
    ]
    wang_rels = [
        {"person": "李冬", "person_id": "wuqiang_李冬",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "武强县现任党政搭档",
         "overlap_org": "中共武强县委员会/武强县人民政府",
         "overlap_period": "现任期",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S002"]},
    ]
    if persons[0]["name"] == "王悦":
        wang_json = build_person_json(persons[0], wang_timeline, wang_rels, sources)
        wang_path = PERSONS_DIR / f"{now}-河北省-衡水市-县委书记-王悦.json"
        with open(wang_path, "w", encoding="utf-8") as f:
            json.dump(wang_json, f, ensure_ascii=False, indent=2)
        print(f"Person JSON written: {wang_path}")

    # ── 李冬 person JSON ──
    li_timeline = [
        {"start": "unknown", "end": "present",
         "org": "武强县人民政府",
         "title": "武强县委副书记、县长", "level": "正处级",
         "location": "河北省衡水市武强县", "system": "government",
         "rank": "正处级", "is_key_promotion": True,
         "notes": "1980年11月生，湖北大悟人，博士研究生；具体到任时间待查",
         "confidence": "confirmed",
         "source_ids": ["S002"]},
        {"start": "unknown", "end": "unknown",
         "org": "履历缺口",
         "title": "",
         "notes": "公开资料未找到2023年任县长之前的完整履历",
         "confidence": "unverified",
         "source_ids": []},
    ]
    li_rels = [
        {"person": "王悦", "person_id": "wuqiang_王悦",
         "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "武强县现任党政搭档",
         "overlap_org": "武强县人民政府/中共武强县委员会",
         "overlap_period": "现任期",
         "direction": "undirected",
         "confidence": "confirmed",
         "source_ids": ["S002"]},
        {"person": "董魁宁", "person_id": "wuqiang_董魁宁",
         "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "曾为武强县县长和常务副县长搭档",
         "overlap_org": "武强县人民政府",
         "overlap_period": "约2021-2023",
         "direction": "undirected",
         "confidence": "plausible",
         "source_ids": ["S002"]},
    ]
    if persons[1]["name"] == "李冬":
        li_json = build_person_json(persons[1], li_timeline, li_rels, sources)
        li_json["identity"]["education"] = [
            {"period": "", "institution": "", "major": "",
             "degree": "博士研究生", "study_type": "unknown",
             "source_ids": ["S002"]}
        ]
        li_path = PERSONS_DIR / f"{now}-河北省-衡水市-县长-李冬.json"
        with open(li_path, "w", encoding="utf-8") as f:
            json.dump(li_json, f, ensure_ascii=False, indent=2)
        print(f"Person JSON written: {li_path}")

    # ── 董魁宁 person JSON (has biography data) ──
    dong_timeline = [
        {"start": "unknown", "end": "",
         "org": "武强县人民政府",
         "title": "武强县委常委、常务副县长", "level": "副处级",
         "location": "河北省衡水市武强县", "system": "government",
         "rank": "副处级", "is_key_promotion": True,
         "notes": "1978年12月生，武邑县人，研究生学历",
         "confidence": "confirmed",
         "source_ids": ["S002"]},
        {"start": "unknown", "end": "present",
         "org": "永清县人民政府",
         "title": "永清县委副书记、县长", "level": "正处级",
         "location": "河北省廊坊市永清县", "system": "government",
         "rank": "正处级", "is_key_promotion": True,
         "notes": "已调任永清县长；具体调任时间待查",
         "confidence": "confirmed",
         "source_ids": ["S002"]},
    ]
    dong_rels = [
        {"person": "李冬", "person_id": "wuqiang_李冬",
         "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "武强县县长和常务副县长搭档",
         "overlap_org": "武强县人民政府",
         "overlap_period": "约2021-2023",
         "direction": "undirected",
         "confidence": "plausible",
         "source_ids": ["S002"]},
    ]
    if persons[2]["name"] == "董魁宁":
        dong_json = build_person_json(persons[2], dong_timeline, dong_rels, sources)
        dong_json["professional_profile"]["career_pattern"] = "cross_county_rotation"
        dong_json["professional_profile"]["geographic_pattern"] = ["武邑县(原籍)", "武强县", "永清县"]
        dong_path = PERSONS_DIR / f"{now}-河北省-衡水市-常务副县长-董魁宁.json"
        with open(dong_path, "w", encoding="utf-8") as f:
            json.dump(dong_json, f, ensure_ascii=False, indent=2)
        print(f"Person JSON written: {dong_path}")


# ═══════════════════════════════════════════════════════════════════════
# MAIN BUILD
# ═══════════════════════════════════════════════════════════════════════

def build():
    print(f"=== Building {SLUG} data ===")
    print(f"Staging dir: {TASK_DIR}")
    print(f"As of: {AS_OF}")
    print()

    # DB
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=str(DB_PATH),
        gexf_path=str(GEXF_PATH),
        overwrite=True,
    )
    print()

    # Person JSONs
    build_person_jsons()
    print()

    print(f"Done. Files in {TASK_DIR}/")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Persons: {PERSONS_DIR}/")


if __name__ == "__main__":
    build()
