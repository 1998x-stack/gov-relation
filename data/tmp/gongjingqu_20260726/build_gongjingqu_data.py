#!/usr/bin/env python3
"""Build 贡井区 leadership network: SQLite + GEXF."""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "贡井区"

PERSONS = [
    {"id": 1, "name": "方矛", "gender": "男", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "区长", "current_org": "贡井区政府", "source": "https://www.gj.gov.cn/"},
    {"id": 2, "name": "刘远初", "gender": "男", "birth": "1975-04",
     "birthplace": "", "education": "省委党校大学", "party_join": "中共党员", "work_start": "",
     "current_post": "常务副区长", "current_org": "贡井区政府", "source": "https://www.gj.gov.cn/"},
    {"id": 3, "name": "李敏", "gender": "女", "birth": "1975-02",
     "birthplace": "", "education": "党校大学", "party_join": "中共党员", "work_start": "",
     "current_post": "副区长", "current_org": "贡井区委宣传部", "source": "https://www.gj.gov.cn/"},
    {"id": 4, "name": "李丰波", "gender": "男", "birth": "1985-09",
     "birthplace": "", "education": "博士研究生", "party_join": "中共党员", "work_start": "",
     "current_post": "副区长", "current_org": "贡井区政府", "source": "https://www.gj.gov.cn/"},
    {"id": 5, "name": "刘鹏程", "gender": "男", "birth": "1984-01",
     "birthplace": "", "education": "大学", "party_join": "中共党员", "work_start": "",
     "current_post": "副区长", "current_org": "贡井区政府", "source": "https://www.gj.gov.cn/"},
    {"id": 6, "name": "钟昕", "gender": "男", "birth": "1986-11",
     "birthplace": "", "education": "大学", "party_join": "中共党员", "work_start": "",
     "current_post": "副区长", "current_org": "贡井区政府", "source": "https://www.gj.gov.cn/"},
    {"id": 7, "name": "但唐杰", "gender": "男", "birth": "1988-10",
     "birthplace": "", "education": "法律硕士", "party_join": "中共党员", "work_start": "",
     "current_post": "副区长", "current_org": "贡井区政府", "source": "https://www.gj.gov.cn/"},
    {"id": 8, "name": "陈英", "gender": "女", "birth": "1976-09",
     "birthplace": "", "education": "在职研究生", "party_join": "中共党员", "work_start": "",
     "current_post": "副区长", "current_org": "贡井区政府", "source": "https://www.gj.gov.cn/"},
]

ORGANIZATIONS = [
    {"id": 101, "name": "贡井区人民政府", "type": "政府", "level": "县级", "parent": "自贡市人民政府", "location": "四川省自贡市贡井区"},
    {"id": 102, "name": "贡井区委", "type": "党委", "level": "县级", "parent": "中共自贡市委", "location": "四川省自贡市贡井区"},
    {"id": 103, "name": "自贡市公安局贡井区分局", "type": "政府部门", "level": "科级", "parent": "贡井区人民政府", "location": "四川省自贡市贡井区"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 101, "title": "区长", "start": "", "end": "", "rank": "正处级", "note": "区委副书记"},
    {"person_id": 2, "org_id": 101, "title": "常务副区长", "start": "", "end": "", "rank": "副处级", "note": "区委常委"},
    {"person_id": 3, "org_id": 101, "title": "副区长", "start": "", "end": "", "rank": "副处级", "note": "区委常委、宣传部部长"},
    {"person_id": 4, "org_id": 101, "title": "副区长", "start": "2025", "end": "", "rank": "副处级", "note": "区委常委"},
    {"person_id": 5, "org_id": 101, "title": "副区长", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 101, "title": "副区长", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 101, "title": "副区长", "start": "2025-12", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 101, "title": "副区长", "start": "", "end": "", "rank": "副处级", "note": "区公安分局局长"},
    {"person_id": 8, "org_id": 103, "title": "党委书记、局长", "start": "", "end": "", "rank": "正科级", "note": ""},
    {"person_id": 3, "org_id": 102, "title": "区委常委、宣传部部长", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 102, "title": "区委常委", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 102, "title": "区委常委", "start": "", "end": "", "rank": "副处级", "note": ""},
]

RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "上下级", "context": "区长-常务副区长", "overlap_org": "贡井区政府", "overlap_period": "2026至今"},
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "区长-副区长", "overlap_org": "贡井区政府", "overlap_period": "2026至今"},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "区长-副区长", "overlap_org": "贡井区政府", "overlap_period": "2026至今"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "区长-副区长", "overlap_org": "贡井区政府", "overlap_period": "2026至今"},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "区长-副区长", "overlap_org": "贡井区政府", "overlap_period": "2026至今"},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "区长-副区长", "overlap_org": "贡井区政府", "overlap_period": "2025-12至今"},
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "区长-副区长", "overlap_org": "贡井区政府", "overlap_period": "2026至今"},
    {"person_a": 2, "person_b": 3, "type": "同僚", "context": "同为区委常委、副区长", "overlap_org": "贡井区委/区政府", "overlap_period": "2025至今"},
    {"person_a": 2, "person_b": 4, "type": "同僚", "context": "同为区委常委、副区长", "overlap_org": "贡井区委/区政府", "overlap_period": "2025至今"},
    {"person_a": 3, "person_b": 4, "type": "同僚", "context": "同为区委常委", "overlap_org": "贡井区委", "overlap_period": "2025至今"},
]

if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DATABASE_DIR / f"{SLUG}_network.db",
        gexf_path=GRAPH_DIR / f"{SLUG}_network.gexf",
        overwrite=True,
    )
