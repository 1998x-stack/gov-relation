#!/usr/bin/env python3
"""芦山县领导班子工作关系网络 — 数据构建脚本

Research sources:
- 网易新闻: 2021年芦山县委换届报道 (source: 川观新闻)
- 网易新闻: 郑胡勇任芦山县委书记报道 (2021-05-17)
- 网易新闻: 芦山县委书记杨俊调研 (2024-04-09, 2024-12-28)
- 环球网: 芦山县委书记率队赴湖北开展招商 (2025-01-09)
- 雅安市人民政府官网 (www.yaan.gov.cn) 领导之窗 (2026-07)
"""

import sys
from pathlib import Path
import sqlite3  # noqa: used via runner

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "芦山县"
STAGING_DIR = Path(__file__).parent
DB_PATH = DATABASE_DIR / f"{SLUG}_network.db"
GEXF_PATH = GRAPH_DIR / f"{SLUG}_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────────────

persons = [
    # 县委书记
    {
        "id": 1,
        "name": "杨俊",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "芦山县委书记",
        "current_org": "中共芦山县委员会",
        "source": "https://www.163.com/dy/article/GNM12AEU0545GBDX.html",
    },
    # 县长 (身份待确认 — 杨俊升任县委书记后，县长空缺或由他人接任)
    {
        "id": 2,
        "name": "王东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "芦山县委副书记",
        "current_org": "中共芦山县委员会",
        "source": "https://www.163.com/dy/article/GNM12AEQ0545GBDX.html",
    },
    # 前任县委书记
    {
        "id": 3,
        "name": "郑胡勇",
        "gender": "男",
        "ethnicity": "羌族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "1997-09",
        "current_post": "雅安市人民政府领导（副厅级）",
        "current_org": "雅安市人民政府",
        "source": "https://www.163.com/dy/article/GA7RPBAQ0545GBEB.html",
    },
    # 常务副县长
    {
        "id": 4,
        "name": "杨本涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "芦山县委常委、常务副县长",
        "current_org": "芦山县人民政府",
        "source": "https://www.163.com/dy/article/JKGC6EEL0545GBDX.html",
    },
    # 县委常委、统战部部长
    {
        "id": 5,
        "name": "张泓",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "芦山县委常委、统战部部长",
        "current_org": "中共芦山县委统战部",
        "source": "https://www.163.com/dy/article/IVB5B312053489NB.html",
    },
    # 县委常委、政法委书记 (2021届)
    {
        "id": 6,
        "name": "郑华东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "芦山县委常委、政法委书记",
        "current_org": "中共芦山县委政法委员会",
        "source": "https://www.163.com/dy/article/GNM12AEQ0545GBDX.html",
    },
    # 县委常委、县纪委书记
    {
        "id": 7,
        "name": "吴晓俊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "芦山县委常委、县纪委书记",
        "current_org": "中共芦山县纪律检查委员会",
        "source": "https://www.163.com/dy/article/GNM12AEQ0545GBDX.html",
    },
    # 县委常委、组织部部长
    {
        "id": 8,
        "name": "刘永虎",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "芦山县委常委、组织部部长",
        "current_org": "中共芦山县委组织部",
        "source": "https://www.163.com/dy/article/GNM12AEQ0545GBDX.html",
    },
    # 县委常委
    {
        "id": 9,
        "name": "黄哲",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "芦山县委常委",
        "current_org": "中共芦山县委员会",
        "source": "https://www.163.com/dy/article/GNM12AEQ0545GBDX.html",
    },
    # 县委常委
    {
        "id": 10,
        "name": "莫定军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "芦山县委常委",
        "current_org": "中共芦山县委员会",
        "source": "https://www.163.com/dy/article/GNM12AEQ0545GBDX.html",
    },
    # 县委常委
    {
        "id": 11,
        "name": "黄杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "芦山县委常委",
        "current_org": "中共芦山县委员会",
        "source": "https://www.163.com/dy/article/GNM12AEQ0545GBDX.html",
    },
    # 县委常委、宣传部部长
    {
        "id": 12,
        "name": "郑国君",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "芦山县委常委、宣传部部长",
        "current_org": "中共芦山县委宣传部",
        "source": "https://www.163.com/dy/article/GNM12AEQ0545GBDX.html",
    },
    # 县领导张帆（报道提及）
    {
        "id": 13,
        "name": "张帆",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "芦山县领导",
        "current_org": "芦山县人民政府",
        "source": "https://www.163.com/dy/article/JKGC6O2EL0545GBDX.html",
    },
    # 县领导周静（报道提及）
    {
        "id": 14,
        "name": "周静",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "芦山县领导",
        "current_org": "芦山县人民政府",
        "source": "https://www.163.com/dy/article/IVB5B0S312053489NB.html",
    },
    # 县领导杨宗才（2021报道提及）
    {
        "id": 15,
        "name": "杨宗才",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "芦山县领导",
        "current_org": "芦山县人民政府",
        "source": "https://www.163.com/dy/article/GHKJ7FN0545GBDX.html",
    },
    # 县领导陈菊丽（2021报道提及）
    {
        "id": 16,
        "name": "陈菊丽",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "芦山县领导",
        "current_org": "芦山县人民政府",
        "source": "https://www.163.com/dy/article/GHKJ7FN0545GBDX.html",
    },
    # 前任县委书记周建华
    {
        "id": 17,
        "name": "周建华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "雅安市人大常委会副主任",
        "current_org": "雅安市人大常委会",
        "source": "https://www.163.com/dy/article/GA7RPBXQ0545GBDX.html",
    },
    # 前任县委副书记朱玉超
    {
        "id": 18,
        "name": "朱玉超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（原）芦山县委副书记",
        "current_org": "中共芦山县委员会",
        "source": "https://www.163.com/dy/article/GA7RPBXQ0545GBDX.html",
    },
]

# ── Organizations ────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共芦山县委员会", "type": "党委", "level": "县处级", "parent": "中共雅安市委", "location": "四川省雅安市芦山县"},
    {"id": 2, "name": "芦山县人民政府", "type": "政府", "level": "县处级", "parent": "雅安市人民政府", "location": "四川省雅安市芦山县"},
    {"id": 3, "name": "雅安市人民政府", "type": "政府", "level": "地厅级", "parent": "四川省人民政府", "location": "四川省雅安市"},
    {"id": 4, "name": "中共芦山县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共雅安市纪委", "location": "四川省雅安市芦山县"},
    {"id": 5, "name": "中共芦山县委政法委员会", "type": "党委", "level": "县处级", "parent": "中共雅安市委政法委", "location": "四川省雅安市芦山县"},
    {"id": 6, "name": "中共芦山县委组织部", "type": "党委", "level": "县处级", "parent": "中共雅安市委组织部", "location": "四川省雅安市芦山县"},
    {"id": 7, "name": "中共芦山县委宣传部", "type": "党委", "level": "县处级", "parent": "中共雅安市委宣传部", "location": "四川省雅安市芦山县"},
    {"id": 8, "name": "中共芦山县委统战部", "type": "党委", "level": "县处级", "parent": "中共雅安市委统战部", "location": "四川省雅安市芦山县"},
    {"id": 9, "name": "雅安市人大常委会", "type": "人大", "level": "地厅级", "parent": "四川省人大常委会", "location": "四川省雅安市"},
    {"id": 10, "name": "天全县人民政府", "type": "政府", "level": "县处级", "parent": "雅安市人民政府", "location": "四川省雅安市天全县"},
    {"id": 11, "name": "宝兴县人民政府", "type": "政府", "level": "县处级", "parent": "雅安市人民政府", "location": "四川省雅安市宝兴县"},
    {"id": 12, "name": "中共天全县委", "type": "党委", "level": "县处级", "parent": "中共雅安市委", "location": "四川省雅安市天全县"},
]

# ── Positions ────────────────────────────────────────────────────────────────

positions = [
    # 杨俊
    {"person_id": 1, "org_id": 1, "title": "芦山县委书记", "start": "2024", "end": "present", "rank": "县处级正职", "note": "2023年底/2024年初接任，此前为县长"},
    {"person_id": 1, "org_id": 2, "title": "芦山县县长", "start": "", "end": "2024", "rank": "县处级正职", "note": "2021年4月前即担任县长，2024年初转任县委书记"},
    {"person_id": 1, "org_id": 1, "title": "芦山县委副书记", "start": "2017?", "end": "2024", "rank": "县处级副职", "note": "任县长期间兼任县委副书记"},

    # 王东
    {"person_id": 2, "org_id": 1, "title": "芦山县委副书记", "start": "2021-10", "end": "present", "rank": "县处级副职", "note": "2021年10月当选县委副书记"},

    # 郑胡勇
    {"person_id": 3, "org_id": 1, "title": "芦山县委书记", "start": "2021-05", "end": "2023", "rank": "县处级正职", "note": "2021年5月任县委书记"},
    {"person_id": 3, "org_id": 10, "title": "天全县县长", "start": "2016-12", "end": "2021-04", "rank": "县处级正职", "note": ""},
    {"person_id": 3, "org_id": 12, "title": "天全县委副书记", "start": "2016-10", "end": "2016-12", "rank": "县处级副职", "note": ""},
    {"person_id": 3, "org_id": 3, "title": "雅安市人民政府副市长", "start": "2024?", "end": "present", "rank": "地厅级副职", "note": "从芦山县委书记晋升市领导"},

    # 杨本涛
    {"person_id": 4, "org_id": 2, "title": "芦山县委常委、常务副县长", "start": "2021-10?", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "芦山县委常委", "start": "2021-10", "end": "present", "rank": "县处级副职", "note": ""},

    # 张泓
    {"person_id": 5, "org_id": 8, "title": "芦山县委常委、统战部部长", "start": "2024?", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "芦山县委常委", "start": "2024?", "end": "present", "rank": "县处级副职", "note": ""},

    # 郑华东
    {"person_id": 6, "org_id": 5, "title": "芦山县委常委、政法委书记", "start": "2021-10", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "芦山县委常委", "start": "2021-10", "end": "present", "rank": "县处级副职", "note": ""},

    # 吴晓俊
    {"person_id": 7, "org_id": 4, "title": "芦山县委常委、县纪委书记", "start": "2021-10", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "芦山县委常委", "start": "2021-10", "end": "present", "rank": "县处级副职", "note": ""},

    # 刘永虎
    {"person_id": 8, "org_id": 6, "title": "芦山县委常委、组织部部长", "start": "2021-10", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "芦山县委常委", "start": "2021-10", "end": "present", "rank": "县处级副职", "note": ""},

    # 黄哲
    {"person_id": 9, "org_id": 1, "title": "芦山县委常委", "start": "2021-10", "end": "present", "rank": "县处级副职", "note": ""},

    # 莫定军
    {"person_id": 10, "org_id": 1, "title": "芦山县委常委", "start": "2021-10", "end": "present", "rank": "县处级副职", "note": ""},

    # 黄杰
    {"person_id": 11, "org_id": 1, "title": "芦山县委常委", "start": "2021-10", "end": "present", "rank": "县处级副职", "note": ""},

    # 郑国君（女）
    {"person_id": 12, "org_id": 7, "title": "芦山县委常委、宣传部部长", "start": "2021-10", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 12, "org_id": 1, "title": "芦山县委常委", "start": "2021-10", "end": "present", "rank": "县处级副职", "note": ""},

    # 张帆（县领导）
    {"person_id": 13, "org_id": 2, "title": "芦山县领导", "start": "2024?", "end": "present", "rank": "", "note": "具体职务待查"},

    # 周静（县领导）
    {"person_id": 14, "org_id": 2, "title": "芦山县领导", "start": "2024?", "end": "present", "rank": "", "note": "具体职务待查"},

    # 杨宗才
    {"person_id": 15, "org_id": 2, "title": "芦山县领导", "start": "2021?", "end": "present", "rank": "", "note": ""},

    # 陈菊丽
    {"person_id": 16, "org_id": 2, "title": "芦山县领导", "start": "2021?", "end": "present", "rank": "", "note": ""},

    # 周建华（前任书记）
    {"person_id": 17, "org_id": 1, "title": "芦山县委书记", "start": "2013?", "end": "2021-04", "rank": "县处级正职", "note": "任职芦山约8年"},
    {"person_id": 17, "org_id": 9, "title": "雅安市人大常委会副主任", "start": "2021?", "end": "present", "rank": "地厅级副职", "note": ""},

    # 朱玉超
    {"person_id": 18, "org_id": 1, "title": "芦山县委副书记", "start": "2020?", "end": "2021-10?", "rank": "县处级副职", "note": "2021年10月后未再当选新一届县委副书记"},
]

# ── Relationships ────────────────────────────────────────────────────────────

relationships = [
    # 杨俊 ↔ 郑胡勇（书记/县长搭档+前后任）
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor", "context": "杨俊接替郑胡勇任县委书记", "overlap_org": "中共芦山县委员会", "overlap_period": "2021-2023"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "杨俊任县长时在郑胡勇领导下工作", "overlap_org": "中共芦山县委员会/芦山县人民政府", "overlap_period": "2021-2023"},

    # 郑胡勇 ↔ 杨本涛
    {"person_a": 3, "person_b": 4, "type": "superior_subordinate", "context": "杨本涛在郑胡勇任书记期间任县委常委", "overlap_org": "中共芦山县委员会", "overlap_period": "2021-2023"},

    # 杨俊 ↔ 杨本涛
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "杨俊任书记后杨本涛为常务副县长", "overlap_org": "中共芦山县委员会/芦山县人民政府", "overlap_period": "2021-现在"},

    # 杨俊 ↔ 王东
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "杨俊任书记、王东任副书记", "overlap_org": "中共芦山县委员会", "overlap_period": "2021-现在"},

    # 郑胡勇 ↔ 周建华
    {"person_a": 3, "person_b": 17, "type": "predecessor_successor", "context": "郑胡勇接替周建华任芦山县委书记，周建华此前在芦山任职约8年", "overlap_org": "中共芦山县委员会", "overlap_period": "2021"},

    # 杨俊 ↔ 周建华
    {"person_a": 1, "person_b": 17, "type": "superior_subordinate", "context": "杨俊在周建华任书时担任县长", "overlap_org": "中共芦山县委员会/芦山县人民政府", "overlap_period": "2021前"},

    # 朱玉超 ↔ 杨俊
    {"person_a": 1, "person_b": 18, "type": "coordinate", "context": "朱玉超任县委副书记时杨俊任县长", "overlap_org": "中共芦山县委员会", "overlap_period": "2020-2021"},

    # 县委常委之间的工作关系（2021届常委会全体成员）
    {"person_a": 4, "person_b": 6, "type": "coordinate", "context": "杨本超与郑华东同为县委常委", "overlap_org": "中共芦山县委员会", "overlap_period": "2021-现在"},
    {"person_a": 4, "person_b": 7, "type": "coordinate", "context": "杨本超与吴昭俊同为县委常委", "overlap_org": "中共芦山县委员会", "overlap_period": "2021-现在"},
    {"person_a": 4, "person_b": 8, "type": "coordinate", "context": "杨本超与刘永虎同为县委常委", "overlap_org": "中共芦山县委员会", "overlap_period": "2021-现在"},
    {"person_a": 6, "person_b": 7, "type": "coordinate", "context": "同为县委常委", "overlap_org": "中共芦山县委员会", "overlap_period": "2021-现在"},
    {"person_a": 6, "person_b": 8, "type": "coordinate", "context": "同为县委常委", "overlap_org": "中共芦山县委员会", "overlap_period": "2021-现在"},
    {"person_a": 7, "person_b": 8, "type": "coordinate", "context": "同为县委常委", "overlap_org": "中共芦山县委员会", "overlap_period": "2021-现在"},
]

# ── Build ────────────────────────────────────────────────────────────────────

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

    print(f"✅ Build complete: {DB_PATH}, {GEXF_PATH}")
    print(f"   Persons: {len(persons)}")
    print(f"   Organizations: {len(organizations)}")
    print(f"   Positions: {len(positions)}")
    print(f"   Relationships: {len(relationships)}")