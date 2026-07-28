#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 瓯海区 (Ouhai District) leadership network."""

import sqlite3
import sys
import os
from pathlib import Path

HERE = Path(__file__).resolve().parent
# Resolve repo root: scripts/build/ -> repo root, or data/tmp/... -> data -> .. -> repo root
if HERE.name == "build" and HERE.parents[0].name == "scripts":
    BASE = HERE.parents[1]  # scripts/build/*.py -> repo root
else:
    BASE = HERE.parents[2]  # data/tmp/<task>/*.py -> repo root
STAGING = str(HERE)
DB_PATH = os.path.join(os.path.join(BASE, "data/database"), "瓯海区_network.db")
GEXF_PATH = os.path.join(os.path.join(BASE, "data/graph"), "瓯海区_network.gexf")
sys.path.insert(0, str(BASE))

from gov_relation.runner import run_build

# ═══════════════════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════════════════

persons = [
    # ── 1. CURRENT LEADERSHIP ──
    {"id": 1, "name": "刘云峰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瓯海区委书记", "current_org": "中共瓯海区委员会",
     "source": "https://www.ouhai.gov.cn/col/col1248633/art/2026/art_d5dfbcbdf80f4fb6803688c63054086f.html"},
    {"id": 2, "name": "季湘荣", "gender": "男", "ethnicity": "汉族",
     "birth": "1982-10", "birthplace": "", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瓯海区委副书记、区长", "current_org": "瓯海区人民政府",
     "source": "https://www.ouhai.gov.cn/col/col1229692832/index.html"},
    {"id": 3, "name": "邵建乐", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瓯海区委副书记（专职）", "current_org": "中共瓯海区委员会",
     "source": "https://www.ouhai.gov.cn/col/col1248633/art/2026/art_80e09fd1f13c404aa037815f8f3e1933.html"},
    {"id": 4, "name": "林蔓", "gender": "女", "ethnicity": "汉族",
     "birth": "1982-06", "birthplace": "", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瓯海区委常委、常务副区长", "current_org": "瓯海区人民政府",
     "source": "https://www.ouhai.gov.cn/col/col1229696175/index.html"},
    {"id": 5, "name": "吴雪梅", "gender": "女", "ethnicity": "汉族",
     "birth": "1972-03", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瓯海区委常委、副区长", "current_org": "瓯海区人民政府",
     "source": "https://www.ouhai.gov.cn/col/col1229696177/index.html"},
    {"id": 6, "name": "张昶", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-05", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瓯海区委常委、区政府党组成员", "current_org": "瓯海区人民政府",
     "source": "https://www.ouhai.gov.cn/col/col1229696206/index.html"},
    {"id": 7, "name": "巴桑卓嘎", "gender": "女", "ethnicity": "藏族",
     "birth": "1985-08", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瓯海区委常委（挂职）、区政府党组成员", "current_org": "瓯海区人民政府",
     "source": "https://www.ouhai.gov.cn/col/col1229692831/zcqwcwqzfdzcyfb/index.html"},
    {"id": 8, "name": "杜潘祚", "gender": "男", "ethnicity": "汉族",
     "birth": "1977-10", "birthplace": "", "education": "大学/经济学学士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瓯海区副区长（外出挂职）", "current_org": "瓯海区人民政府",
     "source": "https://www.ouhai.gov.cn/col/col1229696188/index.html"},
    {"id": 9, "name": "寿宇飞", "gender": "男", "ethnicity": "汉族",
     "birth": "1989-05", "birthplace": "", "education": "研究生/理学硕士",
     "party_join": "民革党员", "work_start": "",
     "current_post": "瓯海区副区长", "current_org": "瓯海区人民政府",
     "source": "https://www.ouhai.gov.cn/col/col1229711393/index.html"},
    {"id": 10, "name": "张露阳", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-08", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瓯海区副区长、区公安分局局长", "current_org": "瓯海区人民政府",
     "source": "https://www.ouhai.gov.cn/col/col1229696190/index.html"},
    {"id": 11, "name": "郑益群", "gender": "男", "ethnicity": "汉族",
     "birth": "1977-10", "birthplace": "", "education": "大学/工程硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瓯海区副区长", "current_org": "瓯海区人民政府",
     "source": "https://www.ouhai.gov.cn/col/col16b5a36e627e40bd1b3403ac4ab10d/index.html"},
    {"id": 12, "name": "陈澄博", "gender": "男", "ethnicity": "汉族",
     "birth": "1986-08", "birthplace": "", "education": "大学/工程硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瓯海区副区长", "current_org": "瓯海区人民政府",
     "source": "https://www.ouhai.gov.cn/col/col1229696210/index.html"},
    {"id": 13, "name": "王世昌", "gender": "男", "ethnicity": "汉族",
     "birth": "1978-10", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瓯海区副区长", "current_org": "瓯海区人民政府",
     "source": "https://www.ouhai.gov.cn/col/col1229696213/index.html"},
    {"id": 14, "name": "董一男", "gender": "男", "ethnicity": "满族",
     "birth": "1990-01", "birthplace": "", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瓯海区副区长（挂职）", "current_org": "瓯海区人民政府",
     "source": "https://www.ouhai.gov.cn/col/col1229692831/lqcwcwfqzfb/index.html"},
    {"id": 15, "name": "朱小恭", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-04", "birthplace": "", "education": "中央党校大学",
     "party_join": "", "work_start": "",
     "current_post": "瓯海区政府党组成员（兼）", "current_org": "瓯海区人民政府",
     "source": "https://www.ouhai.gov.cn/col/col1229696183/index.html"},
    {"id": 16, "name": "林国锋", "gender": "男", "ethnicity": "汉族",
     "birth": "1978-10", "birthplace": "", "education": "本科/教育硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瓯海区政府党组成员、温州铁路南站综管中心主任", "current_org": "瓯海区人民政府",
     "source": "https://www.ouhai.gov.cn/col/col1229696212/index.html"},
    {"id": 17, "name": "卢旭帆", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瓯海区人大常委会主任", "current_org": "瓯海区人大常委会",
     "source": "https://www.ouhai.gov.cn/col/col1248633/art/2026/art_80e09fd3813c404aa017815f8f3e1933.html"},
    {"id": 18, "name": "金衍光", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瓯海区政协主席", "current_org": "瓯海区政协",
     "source": "https://www.ouhai.gov.cn/col/col1248633/art/2026/art_0e09fd1f13c409aa03707f8f3e1933.html"},
    # ── 2. PREDECESSORS ──
    {"id": 19, "name": "曾瑞华", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "温州市副市长（曾任瓯海区委书记）", "current_org": "温州市人民政府",
     "source": "https://www.ouhai.gov.cn/"},
    {"id": 20, "name": "王振勇", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "温州市副市长（前瓯海区委书记/区长）", "current_org": "温州市人民政府",
     "source": "https://www.ouhai.gov.cn/"},
]

organizations = [
    {"id": 1, "name": "中共瓯海区委员会", "type": "党委", "level": "县处级",
     "parent": "中共温州市委员会", "location": "浙江省温州市瓯海区"},
    {"id": 2, "name": "瓯海区人民政府", "type": "政府", "level": "县处级",
     "parent": "温州市人民政府", "location": "浙江省温州市瓯海区"},
    {"id": 3, "name": "瓯海区人大常委会", "type": "人大", "level": "县处级",
     "parent": "温州市人大常委会", "location": "浙江省温州市瓯海区"},
    {"id": 4, "name": "瓯海区政协", "type": "政协", "level": "县处级",
     "parent": "温州市政协", "location": "浙江省温州市瓯海区"},
    {"id": 5, "name": "瓯海区公安分局", "type": "政府", "level": "县处级",
     "parent": "温州市公安局", "location": "浙江省温州市瓯海区"},
    {"id": 6, "name": "温州铁路南站综管中心", "type": "事业单位", "level": "县处级",
     "parent": "温州市人民政府", "location": "浙江省温州市瓯海区"},
    {"id": 7, "name": "温州市人民政府", "type": "政府", "level": "厅级",
     "parent": "浙江省人民政府", "location": "浙江省温州市"},
]

positions = [
    {"person_id": 1, "org_id": 1, "title": "瓯海区委书记", "start_date": "2025?", "end_date": "", "rank": "县处级正职", "note": "现任"},
    {"person_id": 2, "org_id": 1, "title": "瓯海区委副书记（兼职）", "start_date": "2023?", "end_date": "", "rank": "县处级正职", "note": "现任"},
    {"person_id": 2, "org_id": 2, "title": "瓯海区区长/区政府党组书记", "start_date": "2023?", "end_date": "", "rank": "县处级正职", "note": "现任"},
    {"person_id": 3, "org_id": 1, "title": "瓯海区委副书记（专职）", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 4, "org_id": 1, "title": "瓯海区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 4, "org_id": 2, "title": "常务副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 5, "org_id": 1, "title": "瓯海区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 5, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 6, "org_id": 1, "title": "瓯海区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 6, "org_id": 2, "title": "区政府党组成员", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 7, "org_id": 1, "title": "区委常委（挂职）", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "挂职"},
    {"person_id": 7, "org_id": 2, "title": "区政府党组成员（挂职）", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "挂职"},
    {"person_id": 8, "org_id": 2, "title": "副区长（外出挂职）", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "省外挂职学习"},
    {"person_id": 9, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任，民革"},
    {"person_id": 10, "org_id": 2, "title": "副区长、区公安分局局长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 11, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 12, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 13, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 14, "org_id": 2, "title": "副区长（挂职）", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "挂职"},
    {"person_id": 15, "org_id": 2, "title": "区政府党组成员（兼）", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "协调生态园"},
    {"person_id": 16, "org_id": 2, "title": "区政府党组成员", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 16, "org_id": 6, "title": "温州铁路南站综管中心主任", "start_date": "", "end_date": "", "rank": "正处长级", "note": "兼任"},
    {"person_id": 17, "org_id": 3, "title": "瓯海区人大常委会主任", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任"},
    {"person_id": 18, "org_id": 4, "title": "瓯海区政协主席", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任"},
    {"person_id": 19, "org_id": 1, "title": "瓯海区委书记", "start_date": "2021-11?", "end_date": "2025?", "rank": "县处级正职", "note": "后任温州市副市长"},
    {"person_id": 19, "org_id": 2, "title": "瓯海区区长", "start_date": "2019?", "end_date": "2021?", "rank": "县处级正职", "note": "前任区长"},
    {"person_id": 19, "org_id": 7, "title": "温州市副市长", "start_date": "2025?", "end_date": "", "rank": "副厅级", "note": "现任"},
    {"person_id": 20, "org_id": 1, "title": "瓯海区委书记", "start_date": "2016?", "end_date": "2019?", "rank": "县处级正职", "note": "更早前任"},
    {"person_id": 20, "org_id": 2, "title": "瓯海区区长", "start_date": "2014?", "end_date": "2016?", "rank": "县处级正职", "note": "历任"},
    {"person_id": 20, "org_id": 7, "title": "温州市副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "刘云峰（区委书记）与季湘荣（区长）党政搭档",
     "overlap_org": "中共瓯海区委员会", "overlap_period": "2025-至今"},
    {"person_a": 1, "person_b": 3, "type": "同僚",
     "context": "邵建乐系专职副书记，配合刘云峰处理区委日常事务",
     "overlap_org": "中共瓯海区委员会", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 3, "type": "同僚",
     "context": "季湘荣与邵建乐均为区委副书记",
     "overlap_org": "中共瓯海区委员会", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 4, "type": "上下级",
     "context": "林蔓（常务副区长）协助季湘荣",
     "overlap_org": "瓯海区人民政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 17, "type": "同僚",
     "context": "刘云峰与区人大主任卢旭帆四套班子共事",
     "overlap_org": "", "overlap_period": "2025-至今"},
    {"person_a": 1, "person_b": 18, "type": "同僚",
     "context": "刘云峰与政协主席金衍光四套班子共事",
     "overlap_org": "", "overlap_period": "2025-至今"},
    {"person_a": 2, "person_b": 17, "type": "同僚",
     "context": "季湘荣与区人大主任卢旭帆四套班子共事",
     "overlap_org": "", "overlap_period": ""},
    {"person_a": 2, "person_b": 18, "type": "同僚",
     "context": "季湘荣与政协主席金衍光四套班子共事",
     "overlap_org": "", "overlap_period": ""},
    {"person_a": 3, "person_b": 17, "type": "同僚",
     "context": "邵建乐与人大主任卢旭帆四套班子共事",
     "overlap_org": "", "overlap_period": "2026-至今"},
    {"person_a": 3, "person_b": 18, "type": "同僚",
     "context": "邵建乐与政协主席金衍光四套班子共事",
     "overlap_org": "", "overlap_period": "2026-至今"},
    {"person_a": 4, "person_b": 5, "type": "同僚",
     "context": "林蔓与吴雪梅均为区委常委",
     "overlap_org": "中共瓯海区委员会", "overlap_period": ""},
    {"person_a": 4, "person_b": 6, "type": "同僚",
     "context": "林蔓与张昶均为区委常委",
     "overlap_org": "中共瓯海区委员会", "overlap_period": ""},
    {"person_a": 5, "person_b": 6, "type": "同僚",
     "context": "吴雪梅与张昶均为区委常委",
     "overlap_org": "中共瓯海区委员会", "overlap_period": ""},
    {"person_a": 19, "person_b": 1, "type": "交接",
     "context": "曾瑞华→刘云峰 交接",
     "overlap_org": "中共瓯海区委员会", "overlap_period": "2025"},
    {"person_a": 19, "person_b": 2, "type": "交接",
     "context": "曾瑞华与季湘荣 区长交接",
     "overlap_org": "瓯海区人民政府", "overlap_period": "2023?"},
    {"person_a": 20, "person_b": 19, "type": "交接",
     "context": "王振勇→曾瑞华 交接",
     "overlap_org": "中共瓯海区委员会", "overlap_period": "2019?"},
]

# ═══════════════════════════════════════════════════════════════════════
# BUILD - use DATABASE_DIR/GRAPH_DIR for canonical paths
# ═══════════════════════════════════════════════════════════════════════

from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

_db_path = os.path.join(str(DATABASE_DIR), "瓯海区_network.db")
_gx_path = os.path.join(str(GRAPH_DIR), "瓯海区_network.gexf")

run_build(
    slug="瓯海区领导班子关系图",
    persons=persons,
    organizations=organizations,
    positions=positions,
    relationships=relationships,
    db_path=_db_path,
    gexf_path=_gx_path,
    overwrite=True,
)

print(f"\nBuild complete!")
print(f"  DB:  {_db_path}")
print(f"  GEXF:{_gx_path}")
print(f"Total: {len(persons)} persons, {len(organizations)} orgs, "
      f"{len(positions)} positions, {len(relationships)} relationships")