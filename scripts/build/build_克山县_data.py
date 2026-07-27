#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 克山县 leadership network.

克山县隶属黑龙江省齐齐哈尔市。

Current leadership as of 2026-07 (source: www.keshan.gov.cn, Baidu Baike):
- 县委书记: 赵迪 (女，原县长，2026年6月接替宋阳)
- 县委副书记、代县长: 于振伟 (2026年7月到任)
- 县人大常委会主任: 韩伟国
- 县政协主席: 王昕

Leadership transition timeline (confirmed from official news):
- To 2026-06-07: 宋阳任市人大常委会副主任、县委书记
- 2026-06-26: 赵迪以"县委书记、县长"身份主持县委常委会
- 2026-07-17: 于振伟以"县委副书记、代县长"身份调研
- 2026-07-24: 赵迪以县委书记身份、于振伟以代县长身份分头开展工作

Note: Due to degraded web access (Exa rate-limited, Baidu captcha-blocked),
detailed biographical data (birth, birthplace, education, full career timeline)
for most figures could not be obtained. The database and graph encode the confirmed
leadership roster with gaps explicitly marked.
"""

import sqlite3
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "克山县"
DB_PATH = DATABASE_DIR / "克山县_network.db"
GEXF_PATH = GRAPH_DIR / "克山县_network.gexf"

# ── ORGANIZATIONS ───────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共克山县委员会", "type": "党委", "level": "县处级", "parent": "中共齐齐哈尔市委", "location": "黑龙江省齐齐哈尔市克山县"},
    {"id": 2, "name": "克山县人民政府", "type": "政府", "level": "县处级", "parent": "齐齐哈尔市人民政府", "location": "黑龙江省齐齐哈尔市克山县"},
    {"id": 3, "name": "克山县人大常委会", "type": "人大", "level": "县处级", "parent": "齐齐哈尔市人大常委会", "location": "黑龙江省齐齐哈尔市克山县"},
    {"id": 4, "name": "政协克山县委员会", "type": "政协", "level": "县处级", "parent": "政协齐齐哈尔市委员会", "location": "黑龙江省齐齐哈尔市克山县"},
    {"id": 5, "name": "中共克山县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共齐齐哈尔市纪委", "location": "黑龙江省齐齐哈尔市克山县"},
    {"id": 6, "name": "中共克山县委政法委员会", "type": "党委", "level": "县处级", "parent": "中共克山县委员会", "location": "黑龙江省齐齐哈尔市克山县"},
    {"id": 7, "name": "中共克山县委组织部", "type": "党委", "level": "县处级", "parent": "中共克山县委员会", "location": "黑龙江省齐齐哈尔市克山县"},
    {"id": 8, "name": "中共克山县委宣传部", "type": "党委", "level": "县处级", "parent": "中共克山县委员会", "location": "黑龙江省齐齐哈尔市克山县"},
    {"id": 9, "name": "中共克山县委统战部", "type": "党委", "level": "县处级", "parent": "中共克山县委员会", "location": "黑龙江省齐齐哈尔市克山县"},
    {"id": 10, "name": "齐齐哈尔市人大常委会", "type": "人大", "level": "地厅级", "parent": "", "location": "黑龙江省齐齐哈尔市"},
]

# ── PERSONS ─────────────────────────────────────────────────────────

persons = [
    # ── 县委领导（当前）──
    {"id": 1, "name": "赵迪", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "克山县委书记", "current_org": "中共克山县委员会",
     "source": "https://www.keshan.gov.cn/keshan/c100232/202607/c02_633043.shtml"},

    # ── 县政府领导（当前）──
    {"id": 2, "name": "于振伟", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "克山县委副书记、代县长", "current_org": "克山县人民政府",
     "source": "https://www.keshan.gov.cn/keshan/c100232/202607/c02_632712.shtml"},

    # ── 县人大 ──
    {"id": 3, "name": "韩伟国", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "克山县人大常委会主任", "current_org": "克山县人大常委会",
     "source": "https://baike.baidu.com/item/%E5%85%8B%E5%B1%B1%E5%8E%BF/1834965"},

    # ── 县政协 ──
    {"id": 4, "name": "王昕", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "政协克山县委员会主席", "current_org": "政协克山县委员会",
     "source": "https://baike.baidu.com/item/%E5%85%8B%E5%B1%B1%E5%8E%BF/1834965"},

    # ── 县委领导（前任）──
    {"id": 5, "name": "宋阳", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "齐齐哈尔市人大常委会副主任", "current_org": "齐齐哈尔市人大常委会",
     "source": "https://www.keshan.gov.cn/keshan/c100232/202606/c02_626648.shtml"},

    # ── 其他县委常委（从常委会会议新闻中提取）──
    {"id": 6, "name": "李涛", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "克山县委常委", "current_org": "中共克山县委员会",
     "source": "https://www.keshan.gov.cn/keshan/c100232/202607/c02_631427.shtml"},

    {"id": 7, "name": "董理", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "克山县委常委", "current_org": "中共克山县委员会",
     "source": "https://www.keshan.gov.cn/keshan/c100232/202607/c02_631427.shtml"},

    {"id": 8, "name": "李艳军", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "克山县委常委、常务副县长", "current_org": "克山县人民政府",
     "source": "https://www.keshan.gov.cn/keshan/c100232/202607/c02_630539.shtml"},

    {"id": 9, "name": "王卓民", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "克山县委常委", "current_org": "中共克山县委员会",
     "source": "https://www.keshan.gov.cn/keshan/c100232/202607/c02_633043.shtml"},

    {"id": 10, "name": "赵德平", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "克山县委常委", "current_org": "中共克山县委员会",
     "source": "https://www.keshan.gov.cn/keshan/c100232/202607/c02_633043.shtml"},

    {"id": 11, "name": "孙丹妮", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "克山县委常委", "current_org": "中共克山县委员会",
     "source": "https://www.keshan.gov.cn/keshan/c100232/202607/c02_633043.shtml"},

    {"id": 12, "name": "马明", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "克山县委常委", "current_org": "中共克山县委员会",
     "source": "https://www.keshan.gov.cn/keshan/c100232/202607/c02_633043.shtml"},

    {"id": 13, "name": "王高峰", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "克山县委常委、县委办主任", "current_org": "中共克山县委员会",
     "source": "https://www.keshan.gov.cn/keshan/c100232/202607/c02_630539.shtml"},

    {"id": 14, "name": "张红岩", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "克山县副县长", "current_org": "克山县人民政府",
     "source": "https://www.keshan.gov.cn/keshan/c100232/202607/c02_630539.shtml"},

    {"id": 15, "name": "宫庆", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "克山县副县长", "current_org": "克山县人民政府",
     "source": "https://www.keshan.gov.cn/keshan/c100232/202607/c02_632712.shtml"},

    {"id": 16, "name": "宁洪波", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "克山县委常委", "current_org": "中共克山县委员会",
     "source": "https://www.keshan.gov.cn/keshan/c100232/202607/c02_631427.shtml"},
]

# ── POSITIONS ──────────────────────────────────────────────────────

positions = [
    # 赵迪
    {"person_id": 1, "org_id": 1, "title": "克山县委书记", "start_date": "2026-06", "end_date": "present", "rank": "县处级正职", "note": "接替宋阳"},
    {"person_id": 1, "org_id": 1, "title": "克山县委副书记", "start_date": "", "end_date": "2026-06", "rank": "县处级副职", "note": "任县长期间"},
    {"person_id": 1, "org_id": 2, "title": "克山县县长", "start_date": "", "end_date": "2026-07", "rank": "县处级正职", "note": "于振伟接替任代县长"},
    # 于振伟
    {"person_id": 2, "org_id": 1, "title": "克山县委副书记", "start_date": "2026-07", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "克山县代县长", "start_date": "2026-07", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 韩伟国
    {"person_id": 3, "org_id": 3, "title": "克山县人大常委会主任", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 王昕
    {"person_id": 4, "org_id": 4, "title": "政协克山县委员会主席", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 宋阳
    {"person_id": 5, "org_id": 10, "title": "齐齐哈尔市人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副厅局级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "克山县委书记（前任）", "start_date": "", "end_date": "2026-06", "rank": "县处级正职", "note": "赵迪接任"},
    # 李涛
    {"person_id": 6, "org_id": 1, "title": "克山县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 董理
    {"person_id": 7, "org_id": 1, "title": "克山县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 李艳军
    {"person_id": 8, "org_id": 1, "title": "克山县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "克山县常务副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 王卓民
    {"person_id": 9, "org_id": 1, "title": "克山县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 赵德平
    {"person_id": 10, "org_id": 1, "title": "克山县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 孙丹妮
    {"person_id": 11, "org_id": 1, "title": "克山县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 马明
    {"person_id": 12, "org_id": 1, "title": "克山县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 王高峰
    {"person_id": 13, "org_id": 1, "title": "克山县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 13, "org_id": 1, "title": "县委办主任", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    # 张红岩
    {"person_id": 14, "org_id": 2, "title": "克山县副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 宫庆
    {"person_id": 15, "org_id": 2, "title": "克山县副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 宁洪波
    {"person_id": 16, "org_id": 1, "title": "克山县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────────

relationships = [
    # 赵迪 — 于振伟（党政正职搭档）
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "县委班子党政正职搭档", "overlap_org": "中共克山县委员会/克山县人民政府", "overlap_period": "2026-07至今"},
    # 赵迪 — 宋阳（前后任）
    {"person_a": 1, "person_b": 5, "type": "predecessor_successor", "context": "赵迪接替宋阳任县委书记", "overlap_org": "中共克山县委员会", "overlap_period": ""},
    # 赵迪 — 韩伟国
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委与人大常委会正职同届班子", "overlap_org": "克山县", "overlap_period": ""},
    # 赵迪 — 王昕
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "县委与政协正职同届班子", "overlap_org": "克山县", "overlap_period": ""},
    # 赵迪 — 李艳军（常务副县长）
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "政府班子正副职", "overlap_org": "克山县人民政府", "overlap_period": ""},
    # 张红岩 — 宫庆（副县长同事）
    {"person_a": 14, "person_b": 15, "type": "overlap", "context": "县政府班子副职", "overlap_org": "克山县人民政府", "overlap_period": ""},
    # 宋阳 — 赵迪（上下级）
    {"person_a": 5, "person_b": 1, "type": "superior_subordinate", "context": "宋阳任县委书记时，赵迪为县长", "overlap_org": "中共克山县委员会", "overlap_period": ""},
]

if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
