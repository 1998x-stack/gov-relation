#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Lin'an District (临安区), Hangzhou, Zhejiang."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "临安区"

# ── DATA ─────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共杭州市临安区委员会", "type": "党委", "level": "副厅级", "parent": "", "location": "杭州市临安区"},
    {"id": 2, "name": "杭州市临安区人民政府", "type": "政府", "level": "副厅级", "parent": "", "location": "杭州市临安区"},
    {"id": 3, "name": "杭州市临安区人民代表大会常务委员会", "type": "人大", "level": "副厅级", "parent": "", "location": "杭州市临安区"},
    {"id": 4, "name": "中国人民政治协商会议杭州市临安区委员会", "type": "政协", "level": "副厅级", "parent": "", "location": "杭州市临安区"},
    {"id": 5, "name": "中共杭州市临安区纪律检查委员会", "type": "纪委", "level": "副处级", "parent": "", "location": "杭州市临安区"},
    {"id": 6, "name": "中共杭州市临安区委组织部", "type": "党委部门", "level": "正处级", "parent": "", "location": "杭州市临安区"},
    {"id": 7, "name": "中共杭州市临安区委宣传部", "type": "党委部门", "level": "正处级", "parent": "", "location": "杭州市临安区"},
    {"id": 8, "name": "中共杭州市临安区委统一战线工作部", "type": "党委部门", "level": "正处级", "parent": "", "location": "杭州市临安区"},
    {"id": 9, "name": "中共杭州市临安区委政法委员会", "type": "党委部门", "level": "正处级", "parent": "", "location": "杭州市临安区"},
    {"id": 10, "name": "杭州市公安局临安分局", "type": "政府部门", "level": "正处级", "parent": "", "location": "杭州市临安区"},
    {"id": 11, "name": "杭州市临安区发展和改革局", "type": "政府部门", "level": "正处级", "parent": "", "location": "杭州市临安区"},
    {"id": 12, "name": "杭州市临安区财政局", "type": "政府部门", "level": "正处级", "parent": "", "location": "杭州市临安区"},
    {"id": 13, "name": "杭州市临安区审计局", "type": "政府部门", "level": "正处级", "parent": "", "location": "杭州市临安区"},
    {"id": 14, "name": "杭州市临安区人民武装部", "type": "军事", "level": "正团级", "parent": "", "location": "杭州市临安区"},
]

orgs_size = len(organizations)
org_offset = 100000
persons = [
    # ── Party Committee ──
    {"id": 1, "name": "惠海涛", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "中共杭州市临安区委书记", "current_org": "中共杭州市临安区委员会",
     "source": "https://www.linan.gov.cn/col/col1366281/art/2026/art_082ea41ee8ae46778bbdb19aa40e7970.html"},
    {"id": 2, "name": "沈建", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "中共临安区委副书记、区长", "current_org": "杭州市临安区人民政府",
     "source": "https://www.linan.gov.cn/col/col1229288891/art/2025/art_0ba5edbb975e47a1b1dfed964757eede.html"},
    {"id": 3, "name": "汤丽玉", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "中共临安区委副书记", "current_org": "中共杭州市临安区委员会",
     "source": "https://www.linan.gov.cn/col/col1366281/art/2026/art_082ea41ee8ae46776bbdb19aa40e7970.html"},
    {"id": 4, "name": "唐锋", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "临安区委常委、常务副区长", "current_org": "杭州市临安区人民政府",
     "source": "https://www.linan.gov.cn/col/col1229288891/art/2025/art_0ba5edbb975e47a1b1dfed964757eede.html"},
    {"id": 5, "name": "陈立群", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "临安区副区长", "current_org": "杭州市临安区人民政府",
     "source": "https://www.linan.gov.cn/col/col1229288891/art/2025/art_0ba5edbb975e47a1b1dfed964757eede.html"},
    {"id": 6, "name": "洪亮", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "临安区副区长", "current_org": "杭州市临安区人民政府",
     "source": "https://www.linan.gov.cn/col/col1229288891/art/2025/art_0ba5edbb975e47a1b1dfed964757eede.html"},
    {"id": 7, "name": "田江波", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "临安区副区长", "current_org": "杭州市临安区人民政府",
     "source": "https://www.linan.gov.cn/col/col1229288891/art/2025/art_0ba5edbb975e47a1b1dfed964757eede.html"},
    {"id": 8, "name": "罗爱芬", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "临安区副区长", "current_org": "杭州市临安区人民政府",
     "source": "https://www.linan.gov.cn/col/col1229288891/art/2025/art_0ba5edbb975e47a1b1dfed964757eede.html"},
    {"id": 9, "name": "张凯", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "临安区副区长", "current_org": "杭州市临安区人民政府",
     "source": "https://www.linan.gov.cn/col/col1229288891/art/2025/art_0ba5edbb975e47a1b1dfed964757eede.html"},
    {"id": 10, "name": "黄品", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "临安区副区长、公安分局局长", "current_org": "杭州市公安局临安分局",
     "source": "https://www.linan.gov.cn/col/col1229288891/art/2025/art_0ba5edbb975e47a1b1dfed964757eede.html"},
    # ── NPC Standing Committee ──
    {"id": 11, "name": "钱美仙", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "临安区人大常委会主任", "current_org": "杭州市临安区人民代表大会常务委员会",
     "source": "https://www.linan.gov.cn/col/col1366281/art/2026/art_082ea41ee8ae46776bbdb19aa40e7970.html"},
    {"id": 12, "name": "李赛文", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "临安区政协主席", "current_org": "中国人民政治委员会临安区委员会",
     "source": "https://www.linan.gov.cn/col/col1366281/art/2026/art_082ea41ee8ae46776bbdb19aa40e7970.html"},
    {"id": 13, "name": "高吉亚", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "临安区人大常委会副主任", "current_org": "杭州市临安区人民代表大会常务委员会",
     "source": "https://www.linan.gov.cn/col/col1366281/art/2026/art_04b189d708d448c48304f3d3448b4775.html"},
    {"id": 14, "name": "陈国权", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "临安区人大常委会副主任", "current_org": "杭州市临安区人民代表大会常务委员会",
     "source": "https://www.linan.gov.cn/col/col1366281/art/2026/art_04b189d708d448c48304f3d3448b4775.html"},
    {"id": 15, "name": "鲁一成", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "临安区人大常委会副主任", "current_org": "杭州市临安区人民代表大会常务委员会",
     "source": "https://www.linan.gov.cn/col/col1366281/art/2026/art_04b189d708d448c48304f3d3448b4775.html"},
    {"id": 16, "name": "张勤", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "临安区人大常委会副主任", "current_org": "杭州市临安区人民代表大会常务委员会",
     "source": "https://www.linan.gov.cn/col/col1366281/art/2026/art_04b189d708d448c48304f3d3448b4775.html"},
    {"id": 17, "name": "陈栋", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "临安区人大常委会副主任", "current_org": "杭州市临安区人民代表大会常务委员会",
     "source": "https://www.linan.gov.cn/col/col1366281/art/2026/art_04b189d708d448c48304f3d3448b4775.html"},
    {"id": 18, "name": "黄寅", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "临安区人大常委会副主任", "current_org": "杭州市临安区人民代表大会常务委员会",
     "source": "https://www.linan.gov.cn/col/col1366281/art/2026/art_04b189d708d448c48304f3d3448b4775.html"},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记—区长", "overlap_org": "临安区党政班子", "overlap_period": "2025至今"},
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "书记—副书记", "overlap_org": "临安区委常委会", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "书记—常委", "overlap_org": "临安区委常委会", "overlap_period": ""},
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "区长—常务副区长", "overlap_org": "临安区政府", "overlap_period": "2025至今"},
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "区长—副区长", "overlap_org": "临安区政府", "overlap_period": "2025至今"},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "区长—副区长", "overlap_org": "临安区政府", "overlap_period": "2025至今"},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "区长—副区长", "overlap_org": "临安区政府", "overlap_period": "2025至今"},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "区长—副区长", "overlap_org": "临安区政府", "overlap_period": "2025至今"},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "区长—副区长", "overlap_org": "临安区政府", "overlap_period": "2025至今"},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "区长—副区长（公安局长）", "overlap_org": "临安区政府", "overlap_period": "2025至今"},
]

positions = [
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": "兼常务副区长"},
    {"person_id": 4, "org_id": 2, "title": "常务副区长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "经信、科技、环保、商务、数据资源"},
    {"person_id": 6, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "交通、市场监管、人社、司法、退役军人"},
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "城乡建设、住房保障、城管、征地拆迁"},
    {"person_id": 8, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "农业农村、水利、民政、供销"},
    {"person_id": 9, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "教育、卫健、医保、文化旅游、体育"},
    {"person_id": 10, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "公安，主持公安分局全面工作"},
    {"person_id": 10, "org_id": 10, "title": "公安分局局长", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 11, "org_id": 3, "title": "人大常委会主任", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 12, "org_id": 4, "title": "政协主席", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 13, "org_id": 3, "title": "人大常委会副主任", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 14, "org_id": 3, "title": "人大常委会副主任", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 15, "org_id": 3, "title": "人大常委会副主任", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 16, "org_id": 3, "title": "人大常委会副主任", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 17, "org_id": 3, "title": "人大常委会副主任", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 18, "org_id": 3, "title": "人大常委会副主任", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
]

# ── ORCHESTRATION ─────────────────────────────────────────────────

if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DATABASE_DIR / "linan_network.db",
        gexf_path=GRAPH_DIR / "linan_network.gexf",
        overwrite=True,
    )
    print("Done: linan_network.db + linan_network.gexf")