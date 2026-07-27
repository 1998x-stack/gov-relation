#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 连南瑶族自治县 leadership network.

Data source: www.liannan.gov.cn (official government website)
Information currency: 2026-07-22 (current as of July 2026)
"""
# (uses gov_relation.runner which internally uses sqlite3)
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, REPO_ROOT

SLUG = "连南瑶族自治县"

# ── Paths for staging ──
TMP = REPO_ROOT / "data/tmp/guangdong_连南瑶族自治县"
DB_PATH = TMP / "连南瑶族自治县_network.db"
GEXF_PATH = TMP / "连南瑶族自治县_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────────
persons = [
    # === 县政府领导 (County Government Leadership) ===
    {
        "id": 1, "name": "蓝涛", "gender": "男", "ethnicity": "瑶族",
        "birth": "1977年8月", "birthplace": "", "education": "研究生",
        "party_join": "中共党员", "work_start": "",
        "current_post": "连南瑶族自治县委副书记，县政府党组书记、县长",
        "current_org": "连南瑶族自治县人民政府",
        "source": "http://www.liannan.gov.cn/zwgk/ldzc/zf/content/post_2095522.html",
    },
    {
        "id": 2, "name": "李万全", "gender": "男", "ethnicity": "汉族",
        "birth": "1975年7月", "birthplace": "", "education": "大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "连南瑶族自治县委常委、副县长（常务）",
        "current_org": "连南瑶族自治县人民政府",
        "source": "http://www.liannan.gov.cn/zwgk/ldzc/zf/content/post_1454067.html",
    },
    {
        "id": 3, "name": "马海荣", "gender": "男", "ethnicity": "汉族",
        "birth": "1977年6月", "birthplace": "广东连南", "education": "大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "连南瑶族自治县人民政府党组成员、副县长",
        "current_org": "连南瑶族自治县人民政府",
        "source": "http://www.liannan.gov.cn/zwgk/ldzc/zf/content/post_1900306.html",
    },
    {
        "id": 4, "name": "陈清", "gender": "男", "ethnicity": "汉族",
        "birth": "1978年2月", "birthplace": "", "education": "大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "连南瑶族自治县人民政府副县长、公安局局长",
        "current_org": "连南瑶族自治县人民政府",
        "source": "http://www.liannan.gov.cn/zwgk/ldzc/zf/content/post_1763802.html",
    },
    {
        "id": 5, "name": "洪裕山", "gender": "男", "ethnicity": "汉族",
        "birth": "1977年10月", "birthplace": "", "education": "大学，公共管理硕士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "连南瑶族自治县人民政府党组成员、副县长（挂职）",
        "current_org": "连南瑶族自治县人民政府",
        "source": "http://www.liannan.gov.cn/zwgk/ldzc/zf/content/post_1797616.html",
    },
    {
        "id": 6, "name": "朱振飞", "gender": "男", "ethnicity": "汉族",
        "birth": "1983年9月", "birthplace": "广东清远", "education": "大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "连南瑶族自治县人民政府党组成员、副县长",
        "current_org": "连南瑶族自治县人民政府",
        "source": "http://www.liannan.gov.cn/zwgk/ldzc/zf/content/post_1936178.html",
    },
    # === 前任领导 (Predecessors) ===
    {
        "id": 7, "name": "房志荣", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "前任县长",
        "current_org": "连南瑶族自治县人民政府",
        "source": "http://www.liannan.gov.cn/zwgk/rsxx/content/post_2096087.html",
    },
]

# ── Organizations ────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "连南瑶族自治县人民政府", "type": "政府", "level": "县", "parent": "清远市人民政府", "location": "广东省清远市连南瑶族自治县"},
    {"id": 2, "name": "连南瑶族自治县公安局", "type": "政府", "level": "县", "parent": "连南瑶族自治县人民政府", "location": "广东省清远市连南瑶族自治县"},
    {"id": 3, "name": "广州对口帮扶清远指挥部驻连南工作队", "type": "事业单位", "level": "县", "parent": "广州市花都区人民政府", "location": "广东省清远市连南瑶族自治县"},
]

# ── Positions ───────────────────────────────────────────────────────────
positions = [
    # 蓝涛
    {"person_id": 1, "org_id": 1, "title": "连南瑶族自治县委副书记、县长", "start_date": "2025-12", "end_date": "", "rank": "正处级", "note": "2025年12月任副县长、代县长，后当选县长"},
    {"person_id": 1, "org_id": 1, "title": "县政府党组书记", "start_date": "2025-12", "end_date": "", "rank": "正处级", "note": ""},
    # 李万全
    {"person_id": 2, "org_id": 1, "title": "县委常委、常务副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "协助县长负责县政府日常工作"},
    # 马海荣
    {"person_id": 3, "org_id": 1, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "负责农业农村、乡村振兴、水利、生态环境"},
    # 陈清
    {"person_id": 4, "org_id": 1, "title": "副县长、公安局局长", "start_date": "", "end_date": "", "rank": "副处级", "note": "负责公安、司法、打私、维稳"},
    {"person_id": 4, "org_id": 2, "title": "县公安局局长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 洪裕山
    {"person_id": 5, "org_id": 1, "title": "副县长（挂职）", "start_date": "", "end_date": "", "rank": "副处级", "note": "广州对口帮扶清远驻连南工作队队长"},
    {"person_id": 5, "org_id": 3, "title": "广州对口帮扶清远指挥部驻连南工作队队长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 朱振飞
    {"person_id": 6, "org_id": 1, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "负责住建、市场监管、城管、政务服务、招商引资"},
    # 前任
    {"person_id": 7, "org_id": 1, "title": "连南瑶族自治县县长（前任）", "start_date": "~2021", "end_date": "~2025", "rank": "正处级", "note": "蓝涛的前任"},
]

# ── Relationships ───────────────────────────────────────────────────────
relationships = [
    # 县长—副县长（政府班子）
    {"person_a": 1, "person_b": 2, "type": "上下级", "context": "县长—常务副县长", "overlap_org": "连南瑶族自治县人民政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "县长—副县长", "overlap_org": "连南瑶族自治县人民政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "县长—副县长兼公安局长", "overlap_org": "连南瑶族自治县人民政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "县长—副县长（挂职）", "overlap_org": "连南瑶族自治县人民政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "县长—副县长", "overlap_org": "连南瑶族自治县人民政府", "overlap_period": ""},
    # 前任—现任
    {"person_a": 7, "person_b": 1, "type": "前后任", "context": "前任县长→现任县长", "overlap_org": "连南瑶族自治县人民政府", "overlap_period": "~2025交接"},
]

# ── Run Build ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print("Done: 连南瑶族自治县 network built.")
