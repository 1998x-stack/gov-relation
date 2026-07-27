#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 依兰县 leadership network.

依兰县隶属黑龙江省哈尔滨市。

Current leadership as of 2026-07 (source: http://www.hrbyl.gov.cn/):
- 县委书记: 张焱煜
- 县委副书记/县长: 王彦辉
- 县委副书记: 何洪千
- 县委常委: 宁军昌, 郭惠科, 薛春林, 秦洪波, 孙国强, 赵淑芳
- 县人大主任: 刘国胜
- 县政府副县长: 郭惠科, 赵汉夫, 李宏声, 徐立星, 张蕾, 易治
- 县政协主席候选人: 杜建国
"""

import sqlite3
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "依兰县"
DB_PATH = DATABASE_DIR / "依兰县_network.db"
GEXF_PATH = GRAPH_DIR / "依兰县_network.gexf"

# ── ORGANIZATIONS ───────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共依兰县委员会", "type": "党委", "level": "县处级", "parent": "中共哈尔滨市委", "location": "黑龙江省哈尔滨市依兰县"},
    {"id": 2, "name": "依兰县人民政府", "type": "政府", "level": "县处级", "parent": "哈尔滨市人民政府", "location": "黑龙江省哈尔滨市依兰县"},
    {"id": 3, "name": "依兰县人大常委会", "type": "人大", "level": "县处级", "parent": "哈尔滨市人大常委会", "location": "黑龙江省哈尔滨市依兰县"},
    {"id": 4, "name": "依兰县政协", "type": "政协", "level": "县处级", "parent": "哈尔滨市政协", "location": "黑龙江省哈尔滨市依兰县"},
    {"id": 5, "name": "中共依兰县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共哈尔滨市纪委", "location": "黑龙江省哈尔滨市依兰县"},
    {"id": 6, "name": "中共依兰县委政法委员会", "type": "党委", "level": "县处级", "parent": "中共依兰县委员会", "location": "黑龙江省哈尔滨市依兰县"},
    {"id": 7, "name": "中共依兰县委组织部", "type": "党委", "level": "县处级", "parent": "中共依兰县委员会", "location": "黑龙江省哈尔滨市依兰县"},
    {"id": 8, "name": "中共依兰县委宣传部", "type": "党委", "level": "县处级", "parent": "中共依兰县委员会", "location": "黑龙江省哈尔滨市依兰县"},
    {"id": 9, "name": "中共依兰县委统战部", "type": "党委", "level": "县处级", "parent": "中共依兰县委员会", "location": "黑龙江省哈尔滨市依兰县"},
]

# ── PERSONS ─────────────────────────────────────────────────────────

persons = [
    # ── 县委领导 ──
    {"id": 1, "name": "张焱煜", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "中共依兰县委书记", "current_org": "中共依兰县委员会",
     "source": "http://www.hrbyl.gov.cn/"},
    {"id": 2, "name": "王彦辉", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "依兰县委副书记、县政府县长", "current_org": "依兰县人民政府",
     "source": "http://www.hrbyl.gov.cn/"},
    {"id": 3, "name": "何洪千", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "依兰县委副书记", "current_org": "中共依兰县委员会",
     "source": "http://www.hrbyl.gov.cn/"},
    {"id": 4, "name": "宁军昌", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "依兰县委常委", "current_org": "中共依兰县委员会",
     "source": "http://www.hrbyl.gov.cn/"},
    {"id": 5, "name": "郭惠科", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "依兰县委常委、县政府常务副县长", "current_org": "依兰县人民政府",
     "source": "http://www.hrbyl.gov.cn/"},
    {"id": 6, "name": "薛春林", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "依兰县委常委", "current_org": "中共依兰县委员会",
     "source": "http://www.hrbyl.gov.cn/"},
    {"id": 7, "name": "秦洪波", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "依兰县委常委", "current_org": "中共依兰县委员会",
     "source": "http://www.hrbyl.gov.cn/"},
    {"id": 8, "name": "孙国强", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "依兰县委常委", "current_org": "中共依兰县委员会",
     "source": "http://www.hrbyl.gov.cn/"},
    {"id": 9, "name": "赵淑芳", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "依兰县委常委", "current_org": "中共依兰县委员会",
     "source": "http://www.hrbyl.gov.cn/"},
    # ── 县人大领导 ──
    {"id": 10, "name": "刘国胜", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "依兰县人大常委会主任", "current_org": "依兰县人大常委会",
     "source": "http://www.hrbyl.gov.cn/"},
    {"id": 11, "name": "张淑秋", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "依兰县人大常委会副主任", "current_org": "依兰县人大常委会",
     "source": "http://www.hrbyl.gov.cn/"},
    {"id": 12, "name": "张兵", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "依兰县人大常委会副主任", "current_org": "依兰县人大常委会",
     "source": "http://www.hrbyl.gov.cn/"},
    {"id": 13, "name": "刘志伟", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "依兰县人大常委会副主任", "current_org": "依兰县人大常委会",
     "source": "http://www.hrbyl.gov.cn/"},
    {"id": 14, "name": "方占昌", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "依兰县人大常委会副主任", "current_org": "依兰县人大常委会",
     "source": "http://www.hrbyl.gov.cn/"},
    # ── 县政府领导 ──
    {"id": 15, "name": "赵汉夫", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "依兰县政府副县长", "current_org": "依兰县人民政府",
     "source": "http://www.hrbyl.gov.cn/"},
    {"id": 16, "name": "李宏声", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "依兰县政府副县长", "current_org": "依兰县人民政府",
     "source": "http://www.hrbyl.gov.cn/"},
    {"id": 17, "name": "徐立星", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "依兰县政府副县长", "current_org": "依兰县人民政府",
     "source": "http://www.hrbyl.gov.cn/"},
    {"id": 18, "name": "张蕾", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "依兰县政府副县长", "current_org": "依兰县人民政府",
     "source": "http://www.hrbyl.gov.cn/"},
    {"id": 19, "name": "易治", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "依兰县政府副县长", "current_org": "依兰县人民政府",
     "source": "http://www.hrbyl.gov.cn/"},
    # ── 县政协领导 ──
    {"id": 20, "name": "杜建国", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "依兰县政协主席候选人", "current_org": "依兰县政协",
     "source": "http://www.hrbyl.gov.cn/"},
    {"id": 21, "name": "史宝强", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "依兰县政协副主席", "current_org": "依兰县政协",
     "source": "http://www.hrbyl.gov.cn/"},
    {"id": 22, "name": "王守君", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "依兰县政协副主席", "current_org": "依兰县政协",
     "source": "http://www.hrbyl.gov.cn/"},
    {"id": 23, "name": "陈建忠", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "依兰县政协副主席", "current_org": "依兰县政协",
     "source": "http://www.hrbyl.gov.cn/"},
]

# ── POSITIONS ──────────────────────────────────────────────────────

positions = [
    # 张焱煜
    {"person_id": 1, "org_id": 1, "title": "中共依兰县委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 王彦辉
    {"person_id": 2, "org_id": 1, "title": "依兰县委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "依兰县政府县长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 何洪千
    {"person_id": 3, "org_id": 1, "title": "依兰县委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 宁军昌
    {"person_id": 4, "org_id": 1, "title": "依兰县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 郭惠科
    {"person_id": 5, "org_id": 1, "title": "依兰县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "依兰县政府常务副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 薛春林
    {"person_id": 6, "org_id": 1, "title": "依兰县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 秦洪波
    {"person_id": 7, "org_id": 1, "title": "依兰县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 孙国强
    {"person_id": 8, "org_id": 1, "title": "依兰县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 赵淑芳
    {"person_id": 9, "org_id": 1, "title": "依兰县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 刘国胜
    {"person_id": 10, "org_id": 3, "title": "依兰县人大常委会主任", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 张淑秋
    {"person_id": 11, "org_id": 3, "title": "依兰县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 张兵
    {"person_id": 12, "org_id": 3, "title": "依兰县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 刘志伟
    {"person_id": 13, "org_id": 3, "title": "依兰县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 方占昌
    {"person_id": 14, "org_id": 3, "title": "依兰县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 赵汉夫
    {"person_id": 15, "org_id": 2, "title": "依兰县政府副县长", "start_date": "", "end_date": "2026-04", "rank": "县处级副职", "note": "2026年4月29日县人大常委会免职"},
    # 李宏声
    {"person_id": 16, "org_id": 2, "title": "依兰县政府副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 徐立星
    {"person_id": 17, "org_id": 2, "title": "依兰县政府副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 张蕾
    {"person_id": 18, "org_id": 2, "title": "依兰县政府副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 易治
    {"person_id": 19, "org_id": 2, "title": "依兰县政府副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 杜建国
    {"person_id": 20, "org_id": 4, "title": "依兰县政协主席候选人", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 史宝强
    {"person_id": 21, "org_id": 4, "title": "依兰县政协副主席", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 王守君
    {"person_id": 22, "org_id": 4, "title": "依兰县政协副主席", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 陈建忠
    {"person_id": 23, "org_id": 4, "title": "依兰县政协副主席", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────────

relationships = [
    # 张焱煜 — 王彦辉（党政正职搭档）
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "县委班子党政正职搭档", "overlap_org": "中共依兰县委员会/依兰县人民政府", "overlap_period": ""},
    # 张焱煜 — 何洪千（县委正副书记）
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委正副书记工作关系", "overlap_org": "中共依兰县委员会", "overlap_period": ""},
    # 王彦辉 — 郭惠科（县长—常务副县长）
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "县政府正副职工作关系", "overlap_org": "依兰县人民政府", "overlap_period": ""},
    # 郭惠科 — 赵汉夫 李宏声 徐立星 张蕾 易治（副县长之间）
    {"person_a": 5, "person_b": 15, "type": "overlap", "context": "县政府副县长班子成员", "overlap_org": "依兰县人民政府", "overlap_period": ""},
    {"person_a": 5, "person_b": 16, "type": "overlap", "context": "县政府副县长班子成员", "overlap_org": "依兰县人民政府", "overlap_period": ""},
    {"person_a": 5, "person_b": 17, "type": "overlap", "context": "县政府副县长班子成员", "overlap_org": "依兰县人民政府", "overlap_period": ""},
    {"person_a": 5, "person_b": 18, "type": "overlap", "context": "县政府副县长班子成员", "overlap_org": "依兰县人民政府", "overlap_period": ""},
    {"person_a": 5, "person_b": 19, "type": "overlap", "context": "县政府副县长班子成员", "overlap_org": "依兰县人民政府", "overlap_period": ""},
    # 县委常委会成员之间的关系
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "县委常委会共事", "overlap_org": "中共依兰县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "县委常委会共事", "overlap_org": "中共依兰县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "县委常委会共事", "overlap_org": "中共依兰县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "县委常委会共事", "overlap_org": "中共依兰县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "县委常委会共事", "overlap_org": "中共依兰县委员会", "overlap_period": ""},
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "县委常委会共事", "overlap_org": "中共依兰县委员会", "overlap_period": ""},
    {"person_a": 2, "person_b": 6, "type": "overlap", "context": "县委常委会共事", "overlap_org": "中共依兰县委员会", "overlap_period": ""},
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "县委常委会共事", "overlap_org": "中共依兰县委员会", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "overlap", "context": "县委常委会共事", "overlap_org": "中共依兰县委员会", "overlap_period": ""},
    {"person_a": 2, "person_b": 9, "type": "overlap", "context": "县委常委会共事", "overlap_org": "中共依兰县委员会", "overlap_period": ""},
    # 人大—党委关系
    {"person_a": 10, "person_b": 1, "type": "overlap", "context": "人大主任与县委书记工作关系", "overlap_org": "依兰县", "overlap_period": ""},
    # 政协—党委关系
    {"person_a": 20, "person_b": 1, "type": "overlap", "context": "政协主席候选人与县委书记工作关系", "overlap_org": "依兰县", "overlap_period": ""},
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
        overwrite=True,
    )
    print("Build complete.")
