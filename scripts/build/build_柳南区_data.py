#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 柳南区 leadership network.

Data source: Baidu Baike (柳南区条目), liunan.gov.cn
Information currency: 2026-07-22
⚠️ Major gaps: 肖源's full career history is unknown - need deeper investigation
"""
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "柳南区"

# ── Persons ──────────────────────────────────────────────────────────────
persons = [
    # === 区委书记 (Party Secretary) ===
    {
        "id": 1, "name": "肖源", "gender": "男", "ethnicity": "汉族",
        "birth": "待查", "birthplace": "待查", "education": "待查",
        "party_join": "待查", "work_start": "待查",
        "current_post": "柳南区委书记",
        "current_org": "中共柳南区委员会",
        "source": "百度百科-柳南区条目 (lemmaId: 9849476, leadership table)",
    },
    # === 区人大常委会主任 ===
    {
        "id": 2, "name": "龙庆革", "gender": "男", "ethnicity": "汉族",
        "birth": "待查", "birthplace": "待查", "education": "待查",
        "party_join": "中共党员", "work_start": "待查",
        "current_post": "柳南区人大常委会主任",
        "current_org": "柳南区人大常委会",
        "source": "百度百科-柳南区条目 (lemmaId: 9849476, leadership table)",
    },
    # === 区政协主席 ===
    {
        "id": 3, "name": "韦寒", "gender": "男", "ethnicity": "壮族",
        "birth": "待查", "birthplace": "待查", "education": "待查",
        "party_join": "中共党员", "work_start": "待查",
        "current_post": "柳南区政协主席",
        "current_org": "政协柳南区委员会",
        "source": "百度百科-柳南区条目 (lemmaId: 9849476, leadership table)",
    },
    # === 代理区长 (Acting District Mayor) ===
    {
        "id": 4, "name": "贾红玉", "gender": "女", "ethnicity": "汉族",
        "birth": "待查", "birthplace": "待查", "education": "待查",
        "party_join": "待查", "work_start": "待查",
        "current_post": "柳南区代理区长",
        "current_org": "柳南区人民政府",
        "source": "百度百科-柳南区条目 (lemmaId: 9849476, leadership table)",
    },
]

# ── Organizations ────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共柳南区委员会", "type": "党委", "level": "市辖区", "parent": "中共柳州市委", "location": "广西柳州市柳南区"},
    {"id": 2, "name": "柳南区人民政府", "type": "政府", "level": "市辖区", "parent": "柳州市人民政府", "location": "广西柳州市柳南区"},
    {"id": 3, "name": "柳南区人大常委会", "type": "人大", "level": "市辖区", "parent": "柳州市人大常委会", "location": "广西柳州市柳南区"},
    {"id": 4, "name": "政协柳南区委员会", "type": "政协", "level": "市辖区", "parent": "政协柳州市委员会", "location": "广西柳州市柳南区"},
]

# ── Positions ────────────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "柳南区委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "当前在任"},
    {"person_id": 2, "org_id": 3, "title": "柳南区人大常委会主任", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 3, "org_id": 4, "title": "柳南区政协主席", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "柳南区代理区长", "start_date": "", "end_date": "", "rank": "正处级", "note": "代理区长"},
]

# ── Relationships ────────────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 4, "type": "党政搭档", "context": "区委书记—代理区长", "overlap_org": "柳南区四套班子", "overlap_period": ""},
    {"person_a": 1, "person_b": 2, "type": "列席监督", "context": "区委书记—人大常委会主任", "overlap_org": "柳南区四套班子", "overlap_period": ""},
    {"person_a": 1, "person_b": 3, "type": "列席监督", "context": "区委书记—政协主席", "overlap_org": "柳南区四套班子", "overlap_period": ""},
]

# ── Run Build ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DATABASE_DIR / "柳南区_network.db",
        gexf_path=GRAPH_DIR / "柳南区_network.gexf",
        overwrite=True,
    )
    print("Done: 柳南区 network built.")
