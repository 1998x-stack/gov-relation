#!/usr/bin/env python3
"""
建宁县领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Jianning County leadership.

Overview:
    建宁县 is a county under 三明市 (Sanming City), Fujian Province.
    Administrative code: 350430
    Population (2020 census): 114,400
    Area: 1,716.34 km²
    County seat: 濉溪镇
    Government website: www.fjjn.gov.cn

Sources:
    - 建宁县人民政府官网 (www.fjjn.gov.cn) — accessible, 2026-07-16
    - Multiple official news articles confirming leadership

Current Leadership (as of 2026-07-16):
    - 县委书记: 冯彰云 — confirmed 2026-07-16 news article
    - 县委副书记、代县长: 徐婷 — confirmed 2026-07-16 news article
    - Previous 县委书记: 温欣传 — served until ~2026-05/06
    - Previous 县长: 伍小兰 — served until ~2026-06/07
    - Earlier 县长: 陈显卿 — served until ~2021

Known gaps:
    - 冯彰云 full biography (birth, education, early career) unknown
    - 徐婷 full biography (birth, education, early career) unknown
    - Exact promotion dates for 冯彰云 and 徐婷 unknown
    - 温欣传's destination after leaving unknown
    - 伍小兰's destination after leaving unknown

Generated: 2026-07-16
"""

import sqlite3, os, json
from datetime import datetime

# ── Paths ──
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, "建宁县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "建宁县_network.gexf")
PERSONS_DIR = STAGING_DIR


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# ═══════════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════════

AS_OF = "2026-07-16"

# Person ID convention: jianning_{role}_{name}
PERSONS = [
    # (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)

    # ═══ Current Top Leaders ═══
    # 县委书记
    ("jianning_secretary_fengzy", "冯彰云", "男", "待查", "待查", "待查", "待查", "待查", "待查",
     "县委书记", "中共建宁县委员会",
     "建宁县人民政府官网 — 建宁县委树立和践行正确政绩观学习教育专题党课暨全县警示教育会召开 (2026-07-16)"),

    # 县委副书记、代县长
    ("jianning_mayor_xuting", "徐婷", "待查", "待查", "待查", "待查", "待查", "待查", "待查",
     "县委副书记、代县长", "建宁县人民政府",
     "建宁县人民政府官网 — 建宁县委树立和践行正确政绩观学习教育专题党课暨全县警示教育会召开 (2026-07-16)"),

    # ═══ Known County Leaders ═══
    ("jianning_leader_lianyj", "连云进", "待查", "待查", "待查", "待查", "待查", "待查", "待查",
     "县领导", "中共建宁县委员会/建宁县人民政府",
     "建宁县人民政府官网 — 2026-07-16 article"),

    ("jianning_leader_huanglj", "黄立辉", "待查", "待查", "待查", "待查", "待查", "待查", "待查",
     "县领导", "中共建宁县委员会/建宁县人民政府",
     "建宁县人民政府官网 — 安全生产暨防汛防台工作部署会 (2026-07-10)"),

    ("jianning_leader_huangxr", "黄小荣", "待查", "待查", "待查", "待查", "待查", "待查", "待查",
     "县领导", "中共建宁县委员会/建宁县人民政府",
     "建宁县人民政府官网 — 安全生产暨防汛防台工作部署会 (2026-07-10)"),

    ("jianning_leader_jiangwg", "姜炜根", "待查", "待查", "待查", "待查", "待查", "待查", "待查",
     "县领导", "建宁县人民政府",
     "建宁县人民政府官网 — 安全检查和防汛活动 (2026-07-10)"),

    ("jianning_leader_liys", "李样生", "待查", "待查", "待查", "待查", "待查", "待查", "待查",
     "县领导", "建宁县人民政府",
     "建宁县人民政府官网 — 防汛防台风检查 (2026-07-10)"),

    # ═══ Predecessors ═══
    # 原县委书记
    ("jianning_ex_secretary_wenxc", "温欣传", "待查", "待查", "待查", "待查", "待查", "待查", "待查",
     "（原县委书记）", "中共建宁县委员会",
     "建宁县人民政府官网 — 对台工作会议 (2026-05-10) — 最后一次以县委书记身份出席"),

    # 原县长
    ("jianning_ex_mayor_wuxl", "伍小兰", "待查", "待查", "待查", "待查", "待查", "待查", "待查",
     "（原县长）", "建宁县人民政府",
     "建宁县人民政府官网 — 五一节前安全生产检查 (2026-04-29); 人事任免 (2021-07-05)"),

    # 更早原县长
    ("jianning_ex2_mayor_chenxq", "陈显卿", "待查", "待查", "待查", "待查", "待查", "待查", "待查",
     "（原县长）", "建宁县人民政府",
     "建宁县人民政府人事任免 — 伍小兰等职务任免通知 (2021-07-05)"),
]

ORGANIZATIONS = [
    # (id, name, type, level, parent, location)
    ("org_cpc_jianning", "中共建宁县委员会", "党委", "县级", "中共三明市委员会", "福建省三明市建宁县"),
    ("org_gov_jianning", "建宁县人民政府", "政府", "县级", "三明市人民政府", "福建省三明市建宁县"),
    ("org_cpc_jianning_discipline", "中共建宁县纪律检查委员会/建宁县监察委员会", "纪委", "县级", "中共三明市纪律检查委员会", "福建省三明市建宁县"),
    ("org_cpc_jianning_org", "中共建宁县委组织部", "组织", "县级", "中共建宁县委员会", "福建省三明市建宁县"),
    ("org_cpc_jianning_propaganda", "中共建宁县委宣传部", "宣传", "县级", "中共建宁县委员会", "福建省三明市建宁县"),
    ("org_cpc_jianning_legal", "中共建宁县委政法委员会", "政法", "县级", "中共建宁县委员会", "福建省三明市建宁县"),
]

POSITIONS = [
    # (person_id, org_id, title, start, end, rank, note)

    # 冯彰云
    ("jianning_secretary_fengzy", "org_cpc_jianning", "县委书记", "未知（约2026-05/06）", "任职中", "正处级",
     "首次公开露面估计为2026年5月底/6月初；2026-07-16以县委书记身份主持全县警示教育会"),

    # 徐婷
    ("jianning_mayor_xuting", "org_gov_jianning", "县委副书记、代县长", "未知（约2026-06/07）", "任职中", "正处级（代）",
     "2026-07-16首次以代县长身份公开露面"),

    # 温欣传 — 原县委书记
    ("jianning_ex_secretary_wenxc", "org_cpc_jianning", "县委书记", "未知", "约2026-05", "正处级",
     "2026-05-10最后一次以县委书记身份出席对台工作会议；此前2026-05-21陪同中粮集团调研仍以县领导身份参与"),

    # 伍小兰 — 原县长
    ("jianning_ex_mayor_wuxl", "org_gov_jianning", "县长", "约2021-07（兼任经开区主任）", "约2026-06", "正处级",
     "2021-07-05获任命兼任建宁经济开发区管委会主任；2026-04-29仍以县长身份开展安全检查"),

    # 陈显卿 — 更早原县长
    ("jianning_ex2_mayor_chenxq", "org_gov_jianning", "县长", "未知", "约2021-07", "正处级",
     "2021-07-05免去建宁经济开发区管委会主任职务（伍小兰接任）"),

    # 连云进
    ("jianning_leader_lianyj", "org_cpc_jianning", "县领导", "未知", "任职中", "副处级/待查",
     "2026-07-16参加全县警示教育会"),

    # 黄立辉
    ("jianning_leader_huanglj", "org_gov_jianning", "县领导", "未知", "任职中", "副处级/待查",
     "2026-07-10参加安全生产暨防汛防台工作部署会"),

    # 黄小荣
    ("jianning_leader_huangxr", "org_gov_jianning", "县领导", "未知", "任职中", "副处级/待查",
     "2026-07-10参加安全生产暨防汛防台工作部署会"),

    # 姜炜根
    ("jianning_leader_jiangwg", "org_gov_jianning", "县领导", "未知", "任职中", "副处级/待查",
     "2026-07-10带队安全检查；2026-05-21陪同中粮集团调研"),

    # 李样生
    ("jianning_leader_liys", "org_gov_jianning", "县领导", "未知", "任职中", "副处级/待查",
     "2026-07-10参加防汛防台风检查"),
]

RELATIONSHIPS = [
    # (person_a, person_b, type, context, overlap_org, overlap_period)

    # 冯彰云 ↔ 徐婷 (上下级, 当前班子)
    ("jianning_secretary_fengzy", "jianning_mayor_xuting", "superior_subordinate",
     "冯彰云任县委书记，徐婷任代县长，构成当前县委-政府主要领导搭班关系",
     "中共建宁县委员会/建宁县人民政府", "2026-06/07至今"),

    # 冯彰云 ← 温欣传 (前任-继任)
    ("jianning_secretary_fengzy", "jianning_ex_secretary_wenxc", "predecessor_successor",
     "冯彰云接替温欣传担任建宁县委书记",
     "中共建宁县委员会", "约2026-05/06"),

    # 徐婷 ← 伍小兰 (前任-继任, 代县长)
    ("jianning_mayor_xuting", "jianning_ex_mayor_wuxl", "predecessor_successor",
     "徐婷以代县长身份接替伍小兰的县长职务",
     "建宁县人民政府", "约2026-06/07"),

    # 伍小兰 ← 陈显卿 (前任-继任)
    ("jianning_ex_mayor_wuxl", "jianning_ex2_mayor_chenxq", "predecessor_successor",
     "伍小兰接替陈显卿担任建宁县县长（兼任经开区主任）",
     "建宁县人民政府", "约2021-07"),

    # 温欣传 ↔ 伍小兰 (搭班)
    ("jianning_ex_secretary_wenxc", "jianning_ex_mayor_wuxl", "overlap",
     "温欣传任县委书记期间伍小兰任县长，构成党政搭班",
     "中共建宁县委员会/建宁县人民政府", "未知至约2026-05"),

    # 温欣传 ↔ 徐婷 — 徐婷在温欣传时期已是县领导
    ("jianning_ex_secretary_wenxc", "jianning_mayor_xuting", "overlap",
     "温欣传任县委书记时期徐婷已以县领导身份参与工作（对台工作会议）",
     "中共建宁县委员会", "约2026-05"),
]

# ═══════════════════════════════════════════════════════════════
# SQLite Database
# ═══════════════════════════════════════════════════════════════

def create_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
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
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT NOT NULL,
            org_id TEXT NOT NULL,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    for p in PERSONS:
        c.execute(
            "INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            p
        )

    for o in ORGANIZATIONS:
        c.execute(
            "INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?,?,?,?,?,?)",
            o
        )

    for pos in POSITIONS:
        c.execute(
            "INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)",
            pos
        )

    for r in RELATIONSHIPS:
        c.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
            r
        )

    conn.commit()
    conn.close()
    print(f"[OK] Database created: {DB_PATH}")


# ═══════════════════════════════════════════════════════════════
# GEXF Graph
# ═══════════════════════════════════════════════════════════════

def color_for_person(pid):
    """Return r,g,b string for person node."""
    # Party Secretary (县委书记)
    if "secretary" in pid and "ex" not in pid:
        return "255,50,50"
    # Mayor (县长)
    if "mayor" in pid and "ex" not in pid:
        return "50,100,255"
    # Former leaders
    if "ex_" in pid:
        return "150,150,150"
    # Other leaders
    return "100,100,100"


def size_for_person(pid):
    """Return node size."""
    if "secretary" in pid and "ex" not in pid:
        return "20.0"
    if "mayor" in pid and "ex" not in pid:
        return "20.0"
    return "12.0"


def color_for_org(oid):
    """Return r,g,b string for org node."""
    org_map = {
        "org_cpc": "255,200,200",     # 党委 — pink
        "org_gov": "200,200,255",     # 政府 — light blue
    }
    for key, color in org_map.items():
        if key in oid:
            return color
    return "200,200,200"


def create_gexf():
    lines = []

    today = datetime.now().strftime("%Y-%m-%d")
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{today}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append('    <description>建宁县领导班子工作关系网络 — 福建省三明市建宁县领导关系图谱</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('    </attributes>')

    # ── Person Nodes ──
    lines.append('    <nodes>')
    for p in PERSONS:
        pid = p[0]
        name = p[1]
        role = p[9]
        c = color_for_person(pid)
        sz = size_for_person(pid)
        lines.append(f'      <node id="p{pid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # ── Organization Nodes ──
    lines.append('    <nodes>')
    for o in ORGANIZATIONS:
        oid = o[0]
        name = o[1]
        otype = o[2]
        c = color_for_org(oid)
        lines.append(f'      <node id="o{oid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(otype)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # ── Edges ──
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked_at)
    for pos in POSITIONS:
        eid += 1
        pid = pos[0]
        oid = pos[1]
        title = pos[2]
        lines.append(f'      <edge id="e{eid}" source="p{pid}" target="o{oid}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationship)
    for r in RELATIONSHIPS:
        eid += 1
        pa = r[0]
        pb = r[1]
        rtype = r[2]
        lines.append(f'      <edge id="e{eid}" source="p{pa}" target="p{pb}" label="{esc(rtype)}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rtype)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[OK] GEXF graph created: {GEXF_PATH}")


# ═══════════════════════════════════════════════════════════════
# Person JSON
# ═══════════════════════════════════════════════════════════════

def write_person_json(person, career_entries, rel_entries, org_entries, gov_entries, style_entries):
    """Write a per-person graph JSON file following the schema from person_graph_json.md."""
    pid, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source = person

    filename = f"20260716-福建省-三明市-{current_post}-{name}.json"
    filepath = os.path.join(PERSONS_DIR, filename)

    # Build person_id
    safe_name = name.replace("（", "_").replace("）", "").replace(" ", "_")
    person_id = f"jianning_{safe_name}"

    data = {
        "schema_version": "1.0",
        "generated_at": "2026-07-16",
        "investigation_scope": {
            "province": "福建省",
            "city": "三明市",
            "region": "建宁县",
            "job": current_post,
            "task_id": "fujian_建宁县",
            "time_focus": "2024-2026"
        },
        "identity": {
            "person_id": person_id,
            "name": name,
            "aliases": [],
            "gender": gender if gender != "待查" else "",
            "ethnicity": ethnicity if ethnicity != "待查" else "",
            "birth": birth if birth != "待查" else "",
            "birthplace": birthplace if birthplace != "待查" else "",
            "native_place": "",
            "education": [],
            "party_join": party_join if party_join != "待查" else "",
            "work_start": work_start if work_start != "待查" else "",
            "dedupe_keys": {
                "name_birth": f"{name}_{birth}" if birth and birth != "待查" else f"{name}_unknown",
                "name_birthplace": f"{name}_{birthplace}" if birthplace and birthplace != "待查" else "",
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": current_post,
            "current_org": current_org,
            "administrative_rank": "正处级" if "书记" in current_post or "县长" in current_post else "待查",
            "as_of": "2026-07-16",
            "is_current_confirmed": "（待查）" not in name,
            "source_ids": ["S001"]
        },
        "career_timeline": career_entries,
        "organizations": org_entries,
        "relationships": rel_entries,
        "governance_record": gov_entries,
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "公开履历不足，无法评估",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": style_entries,
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": f"截至2026年7月，未发现{name}的相关负面报道或纪律处分信息。信息来源限于建宁县人民政府官网公开报道，未进行全网搜索。",
                "date": "",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "建宁县人民政府官网 — 相关新闻报道",
                "url": "https://www.fjjn.gov.cn/",
                "publisher": "建宁县人民政府",
                "published_at": "2026-07-16",
                "accessed_at": "2026-07-16",
                "source_type": "official",
                "reliability": "high",
                "notes": "建宁县人民政府门户网站，确认了当前领导班子成员"
            }
        ],
        "confidence_summary": {
            "identity": "plausible",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"{name}的出生年月、籍贯、教育背景和完整履历均公开缺位——建宁县政府官网未提供领导之窗/个人简历页面"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的出生年月、籍贯、教育背景？",
                "why_it_matters": "身份识别和人员去重所需的核心字段",
                "suggested_queries": [f"{name} 简历", f"{name} 出生", f"{name} 百度百科"],
                "last_attempted": "2026-07-16"
            },
            {
                "priority": "critical",
                "question": f"{name}在担任{current_post}前的完整履历是什么？",
                "why_it_matters": "评估干部晋升路径和可能的人脉网络",
                "suggested_queries": [f"{name} 任职", f"{name} 三明"],
                "last_attempted": "2026-07-16"
            }
        ]
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[OK] Person JSON created: {filepath}")


def create_person_jsons():
    today = "2026-07-16"
    as_of = "2026-07-16"

    # ── 冯彰云 ──
    write_person_json(
        PERSONS[0],
        career_entries=[
            {
                "start": "未知（约2026-05/06）",
                "end": "present",
                "org": "中共建宁县委员会",
                "title": "县委书记",
                "level": "正处级",
                "location": "福建省三明市建宁县",
                "system": "party",
                "rank": "正处级",
                "is_key_promotion": True,
                "notes": "2026-07-16以县委书记身份主持全县警示教育会；此前约2026年5月左右接替温欣传",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            },
            {
                "start": "未知",
                "end": "约2026-05",
                "org": "履历缺口",
                "title": "",
                "notes": "冯彰云在担任建宁县委书记前的完整履历未知",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        rel_entries=[
            {
                "person": "徐婷",
                "person_id": "jianning_徐婷",
                "relationship_type": "superior_subordinate",
                "strength": "strong",
                "evidence": "冯彰云任县委书记，徐婷任代县长，构成当前党政搭班",
                "overlap_org": "中共建宁县委员会/建宁县人民政府",
                "overlap_period": "2026-06/07至今",
                "direction": "person_to_other",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            },
            {
                "person": "温欣传",
                "person_id": "jianning_温欣传",
                "relationship_type": "predecessor_successor",
                "strength": "strong",
                "evidence": "冯彰云接替温欣传担任建宁县委书记",
                "overlap_org": "中共建宁县委员会",
                "overlap_period": "约2026-05/06",
                "direction": "person_to_other",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            }
        ],
        org_entries=[
            {
                "org": "中共建宁县委员会",
                "type": "党委",
                "level": "县级",
                "parent": "中共三明市委员会",
                "location": "福建省三明市建宁县",
                "source_ids": ["S001"]
            }
        ],
        gov_entries=[
            {
                "period": "2026-07",
                "domain": "other",
                "achievement_or_event": "主持建宁县委树立和践行正确政绩观学习教育专题党课暨全县警示教育会",
                "role_in_event": "主讲人",
                "measurable_outcome": "强调深化思想认识、主动对标检视、强化担当作为，统筹安全稳定和集中换届工作",
                "location": "建宁县",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            },
            {
                "period": "2026-07",
                "domain": "public_security",
                "achievement_or_event": "主持召开建宁县安全生产暨防汛防台工作部署会",
                "role_in_event": "主持人",
                "measurable_outcome": "部署安全生产重点领域排查、防汛防台预警、应急机制建设和值班值守",
                "location": "建宁县",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            }
        ],
        style_entries=[
            {
                "trait": "pragmatic",
                "evidence": "在安全生产会上强调'以时时放心不下的责任感'、'建立问题清单'、'即查即改'",
                "confidence": "plausible",
                "source_ids": ["S001"]
            },
            {
                "trait": "discipline_oriented",
                "evidence": "主持警示教育会，强调'守住纪律底线'、'系好从政履职的第一粒扣子'",
                "confidence": "plausible",
                "source_ids": ["S001"]
            }
        ]
    )

    # ── 徐婷 ──
    write_person_json(
        PERSONS[1],
        career_entries=[
            {
                "start": "未知（约2026-06/07）",
                "end": "present",
                "org": "建宁县人民政府",
                "title": "县委副书记、代县长",
                "level": "正处级",
                "location": "福建省三明市建宁县",
                "system": "government",
                "rank": "正处级（代）",
                "is_key_promotion": True,
                "notes": "2026-07-16首次以代县长身份公开露面；此前以县领导身份参与工作",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            },
            {
                "start": "未知",
                "end": "约2026-05",
                "org": "履历缺口",
                "title": "",
                "notes": "徐婷在担任代县长前的职务和履历完全未知。2026-05-10对台工作会议已以县领导身份参加",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        rel_entries=[
            {
                "person": "冯彰云",
                "person_id": "jianning_冯彰云",
                "relationship_type": "superior_subordinate",
                "strength": "strong",
                "evidence": "作为代县长在县委书记冯彰云领导下工作",
                "overlap_org": "中共建宁县委员会/建宁县人民政府",
                "overlap_period": "2026-06/07至今",
                "direction": "other_to_person",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            },
            {
                "person": "伍小兰",
                "person_id": "jianning_伍小兰",
                "relationship_type": "predecessor_successor",
                "strength": "strong",
                "evidence": "徐婷以代县长身份接替伍小兰的县长职务",
                "overlap_org": "建宁县人民政府",
                "overlap_period": "约2026-06/07",
                "direction": "person_to_other",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            },
            {
                "person": "温欣传",
                "person_id": "jianning_温欣传",
                "relationship_type": "overlap",
                "strength": "medium",
                "evidence": "温欣传任县委书记期间，徐婷已以县领导身份参加对台工作会议",
                "overlap_org": "中共建宁县委员会",
                "overlap_period": "约2026-05",
                "direction": "person_to_other",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            }
        ],
        org_entries=[
            {
                "org": "建宁县人民政府",
                "type": "政府",
                "level": "县级",
                "parent": "三明市人民政府",
                "location": "福建省三明市建宁县",
                "source_ids": ["S001"]
            }
        ],
        gov_entries=[
            {
                "period": "2026-07",
                "domain": "public_security",
                "achievement_or_event": "带队开展防汛防台风、安全生产督导检查",
                "role_in_event": "带队领导",
                "measurable_outcome": "检查地灾点、水利设施、在建工地、旅游景区等重点部位",
                "location": "建宁县",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            }
        ],
        style_entries=[
            {
                "trait": "pragmatic",
                "evidence": "在防汛督导中深入一线检查重点部位",
                "confidence": "plausible",
                "source_ids": ["S001"]
            }
        ]
    )

    # ── 温欣传（原县委书记）──
    write_person_json(
        PERSONS[6],
        career_entries=[
            {
                "start": "未知",
                "end": "约2026-05",
                "org": "中共建宁县委员会",
                "title": "县委书记",
                "level": "正处级",
                "location": "福建省三明市建宁县",
                "system": "party",
                "rank": "正处级",
                "is_key_promotion": True,
                "notes": "2026-05-10最后一次以县委书记身份公开出席对台工作会议；2026-05-21陪同中粮集团调研时仅以'县领导'身份出现",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            },
            {
                "start": "未知",
                "end": "未知",
                "org": "履历缺口",
                "title": "",
                "notes": "温欣传在担任建宁县委书记前的完整履历未知；离任后的去向未知",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        rel_entries=[
            {
                "person": "冯彰云",
                "person_id": "jianning_冯彰云",
                "relationship_type": "predecessor_successor",
                "strength": "strong",
                "evidence": "冯彰云接替温欣传担任建宁县委书记",
                "overlap_org": "中共建宁县委员会",
                "overlap_period": "约2026-05/06",
                "direction": "other_to_person",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            },
            {
                "person": "伍小兰",
                "person_id": "jianning_伍小兰",
                "relationship_type": "overlap",
                "strength": "strong",
                "evidence": "温欣传任县委书记期间伍小兰任县长",
                "overlap_org": "中共建宁县委员会/建宁县人民政府",
                "overlap_period": "至约2026-05",
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            },
            {
                "person": "徐婷",
                "person_id": "jianning_徐婷",
                "relationship_type": "overlap",
                "strength": "medium",
                "evidence": "温欣传任县委书记期间徐婷以县领导身份参与工作",
                "overlap_org": "中共建宁县委员会",
                "overlap_period": "约2026-05",
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            }
        ],
        org_entries=[
            {
                "org": "中共建宁县委员会",
                "type": "党委",
                "level": "县级",
                "parent": "中共三明市委员会",
                "location": "福建省三明市建宁县",
                "source_ids": ["S001"]
            }
        ],
        gov_entries=[
            {
                "period": "2026-05",
                "domain": "other",
                "achievement_or_event": "主持召开建宁县对台工作会议",
                "role_in_event": "主持人",
                "measurable_outcome": "部署2026年对台工作重点任务",
                "location": "建宁县",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            }
        ],
        style_entries=[
            {
                "trait": "pragmatic",
                "evidence": "在对台工作会议上强调'主动融入和服务全国全省全市对台工作大局'、'立足建宁资源禀赋'",
                "confidence": "plausible",
                "source_ids": ["S001"]
            }
        ]
    )

    # ── 伍小兰（原县长）──
    write_person_json(
        PERSONS[7],
        career_entries=[
            {
                "start": "约2021-07",
                "end": "约2026-06",
                "org": "建宁县人民政府",
                "title": "县长（兼建宁经济开发区管委会主任）",
                "level": "正处级",
                "location": "福建省三明市建宁县",
                "system": "government",
                "rank": "正处级",
                "is_key_promotion": True,
                "notes": "2021-07-05获任命兼任建宁经济开发区管委会主任；2026-04-29以县长身份开展节前安全检查",
                "confidence": "confirmed",
                "source_ids": ["S001", "S002"]
            },
            {
                "start": "未知",
                "end": "约2021-07",
                "org": "履历缺口",
                "title": "",
                "notes": "伍小兰在担任建宁县县长前的完整履历未知",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        rel_entries=[
            {
                "person": "徐婷",
                "person_id": "jianning_徐婷",
                "relationship_type": "predecessor_successor",
                "strength": "strong",
                "evidence": "徐婷以代县长身份接替伍小兰的县长职务",
                "overlap_org": "建宁县人民政府",
                "overlap_period": "约2026-06/07",
                "direction": "other_to_person",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            },
            {
                "person": "温欣传",
                "person_id": "jianning_温欣传",
                "relationship_type": "overlap",
                "strength": "strong",
                "evidence": "温欣传任县委书记期间伍小兰任县长",
                "overlap_org": "中共建宁县委员会/建宁县人民政府",
                "overlap_period": "至约2026-05",
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            },
            {
                "person": "陈显卿",
                "person_id": "jianning_陈显卿",
                "relationship_type": "predecessor_successor",
                "strength": "strong",
                "evidence": "伍小兰接替陈显卿兼任建宁经济开发区管委会主任",
                "overlap_org": "建宁县人民政府/建宁经济开发区",
                "overlap_period": "2021-07",
                "direction": "person_to_other",
                "confidence": "confirmed",
                "source_ids": ["S002"]
            }
        ],
        org_entries=[
            {
                "org": "建宁县人民政府",
                "type": "政府",
                "level": "县级",
                "parent": "三明市人民政府",
                "location": "福建省三明市建宁县",
                "source_ids": ["S001", "S002"]
            },
            {
                "org": "建宁经济开发区",
                "type": "开发区",
                "level": "县级",
                "parent": "建宁县人民政府",
                "location": "福建省三明市建宁县",
                "source_ids": ["S002"]
            }
        ],
        gov_entries=[
            {
                "period": "2026-04",
                "domain": "public_security",
                "achievement_or_event": "带队开展五一节前安全生产检查",
                "role_in_event": "带队领导",
                "measurable_outcome": "检查体育馆改造项目、酒店、超市、工业企业等重点场所",
                "location": "建宁县",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            }
        ],
        style_entries=[
            {
                "trait": "pragmatic",
                "evidence": "在安全生产检查中强调'建立发现、整改、验收、销号闭环机制'、'即查即改、立行立改'",
                "confidence": "plausible",
                "source_ids": ["S001"]
            }
        ]
    )

    # ── 陈显卿（更早原县长）──
    write_person_json(
        PERSONS[8],
        career_entries=[
            {
                "start": "未知",
                "end": "约2021-07",
                "org": "建宁县人民政府",
                "title": "县长（兼建宁经济开发区管委会主任）",
                "level": "正处级",
                "location": "福建省三明市建宁县",
                "system": "government",
                "rank": "正处级",
                "is_key_promotion": False,
                "notes": "2021年7月免去建宁经济开发区管委会主任职务（由伍小兰接任）",
                "confidence": "confirmed",
                "source_ids": ["S002"]
            },
            {
                "start": "未知",
                "end": "未知",
                "org": "履历缺口",
                "title": "",
                "notes": "陈显卿在建宁县任职前的完整履历未知；离任后的去向未知",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        rel_entries=[
            {
                "person": "伍小兰",
                "person_id": "jianning_伍小兰",
                "relationship_type": "predecessor_successor",
                "strength": "strong",
                "evidence": "伍小兰接替陈显卿兼任建宁经济开发区管委会主任",
                "overlap_org": "建宁县人民政府/建宁经济开发区",
                "overlap_period": "2021-07",
                "direction": "other_to_person",
                "confidence": "confirmed",
                "source_ids": ["S002"]
            }
        ],
        org_entries=[
            {
                "org": "建宁县人民政府",
                "type": "政府",
                "level": "县级",
                "parent": "三明市人民政府",
                "location": "福建省三明市建宁县",
                "source_ids": ["S002"]
            }
        ],
        gov_entries=[],
        style_entries=[]
    )


# ═══════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    create_database()
    create_gexf()
    create_person_jsons()
    print("\n[DONE] All artifacts generated.")
