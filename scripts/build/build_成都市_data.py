#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 成都市 (Chengdu), Sichuan province.

Chengdu is the capital of Sichuan, a sub-provincial city (副省级城市).
Current leadership as of July 2026.
"""

import sqlite3
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# Staging directory
BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "成都市_network.db")
GEXF_PATH = os.path.join(BASE, "成都市_network.gexf")

# ── PERSONS ──────────────────────────────────────────────────────────
# ID scheme: 1-99 for current leaders, 100+ for historical/predecessors
# ID naming: 1-9 top leaders, 10-29 standing committee, 30-49 govt, 50-69 historical

persons = [
    # ── Current Top Leaders (Party + Government) ──
    {
        "id": 1,
        "name": "曹立军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-11",
        "birthplace": "湖南省长沙市望城区",
        "education": "湘潭师范学院汉语言文学学士、湖南大学管理科学与工程硕士",
        "party_join": "1992",
        "work_start": "1994",
        "current_post": "成都市委书记",
        "current_org": "中共成都市委员会",
        "source": "https://zh.wikipedia.org/wiki/曹立军",
    },
    {
        "id": 2,
        "name": "陈书平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969-10",
        "birthplace": "四川省荣县",
        "education": "在职硕士",
        "party_join": "中共党员",
        "work_start": "1990年代",
        "current_post": "成都市市长",
        "current_org": "成都市人民政府",
        "source": "https://zh.wikipedia.org/wiki/陈书平",
    },
    {
        "id": 3,
        "name": "何礼",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1965-09",
        "birthplace": "四川省大竹县",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "成都市人大常委会主任",
        "current_org": "成都市人民代表大会常务委员会",
        "source": "https://zh.wikipedia.org/wiki/成都市",
    },
    {
        "id": 4,
        "name": "曾卿",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969-06",
        "birthplace": "四川省遂宁市",
        "education": "南京航空航天大学机械工程学士、四川大学国民经济管理硕士",
        "party_join": "1995-12",
        "work_start": "1991",
        "current_post": "成都市政协主席",
        "current_org": "中国人民政治协商会议成都市委员会",
        "source": "https://zh.wikipedia.org/wiki/曾卿",
    },
    {
        "id": 5,
        "name": "刘光辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967-05",
        "birthplace": "安徽省太和县",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "成都市监察委员会主任",
        "current_org": "成都市监察委员会",
        "source": "https://zh.wikipedia.org/wiki/成都市",
    },
    # ── Predecessors (Historical) ──
    {
        "id": 50,
        "name": "施小琳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1969-05",
        "birthplace": "浙江省余姚县",
        "education": "上海大学工学院电气技术、同济大学工商管理硕士",
        "party_join": "1993-06",
        "work_start": "1990-07",
        "current_post": "四川省省长",
        "current_org": "四川省人民政府",
        "source": "https://zh.wikipedia.org/wiki/施小琳",
    },
    {
        "id": 51,
        "name": "范锐平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966-04",
        "birthplace": "湖北省钟祥市",
        "education": "武汉大学自修、华中科技大学行政管理硕士",
        "party_join": "1985-05",
        "work_start": "1984-08",
        "current_post": "吉林省人大常委会副主任",
        "current_org": "吉林省人民代表大会常务委员会",
        "source": "https://zh.wikipedia.org/wiki/范锐平",
    },
    {
        "id": 52,
        "name": "王凤朝",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1965",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任成都市市长（2020-2025）",
        "current_org": "",
        "source": "https://zh.wikipedia.org/wiki/王凤朝",
    },
    {
        "id": 53,
        "name": "罗增斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任绵阳市委书记（被曹立军接替）",
        "current_org": "",
        "source": "https://zh.wikipedia.org/wiki/曹立军",
    },
]

# ── ORGANIZATIONS ─────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共成都市委员会", "type": "党委", "level": "副省级", "parent": "中共四川省委", "location": "成都市"},
    {"id": 2, "name": "成都市人民政府", "type": "政府", "level": "副省级", "parent": "四川省人民政府", "location": "成都市"},
    {"id": 3, "name": "成都市人民代表大会常务委员会", "type": "人大", "level": "副省级", "parent": "", "location": "成都市"},
    {"id": 4, "name": "中国人民政治协商会议成都市委员会", "type": "政协", "level": "副省级", "parent": "", "location": "成都市"},
    {"id": 5, "name": "成都市监察委员会", "type": "政府", "level": "副省级", "parent": "", "location": "成都市"},
    {"id": 6, "name": "中共四川省委", "type": "党委", "level": "省级", "parent": "中共中央", "location": "成都市"},
    {"id": 7, "name": "四川省人民政府", "type": "政府", "level": "省级", "parent": "国务院", "location": "成都市"},
    {"id": 8, "name": "中共绵阳市委", "type": "党委", "level": "地级", "parent": "中共四川省委", "location": "绵阳市"},
    {"id": 9, "name": "吉林省人民代表大会常务委员会", "type": "人大", "level": "省级", "parent": "", "location": "长春市"},
    {"id": 10, "name": "四川省财政厅", "type": "政府", "level": "省级部门", "parent": "四川省人民政府", "location": "成都市"},
    {"id": 11, "name": "四川省交通运输厅", "type": "政府", "level": "省级部门", "parent": "四川省人民政府", "location": "成都市"},
    {"id": 12, "name": "四川省人民政府办公厅", "type": "政府", "level": "省级部门", "parent": "四川省人民政府", "location": "成都市"},
    {"id": 13, "name": "四川省商务厅", "type": "政府", "level": "省级部门", "parent": "四川省人民政府", "location": "成都市"},
    {"id": 14, "name": "中共广安市委", "type": "党委", "level": "地级", "parent": "中共四川省委", "location": "广安市"},
    {"id": 15, "name": "广安市人民政府", "type": "政府", "level": "地级", "parent": "四川省人民政府", "location": "广安市"},
    {"id": 16, "name": "中共湖南省委", "type": "党委", "level": "省级", "parent": "中共中央", "location": "长沙市"},
    {"id": 17, "name": "长沙市人民政府", "type": "政府", "level": "副省级", "parent": "湖南省人民政府", "location": "长沙市"},
    {"id": 18, "name": "中共常德市委", "type": "党委", "level": "地级", "parent": "中共湖南省委", "location": "常德市"},
    {"id": 19, "name": "常德市人民政府", "type": "政府", "level": "地级", "parent": "湖南省人民政府", "location": "常德市"},
    {"id": 20, "name": "四川省人民政府驻北京办事处", "type": "政府", "level": "省级部门", "parent": "四川省人民政府", "location": "北京市"},
    {"id": 21, "name": "四川省政协", "type": "政协", "level": "省级", "parent": "", "location": "成都市"},
]

# ── POSITIONS ─────────────────────────────────────────────────────────

positions = [
    # Current
    {"person_id": 1, "org_id": 1, "title": "成都市委书记", "start": "2024-08", "end": "present", "rank": "副省级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "成都市市长", "start": "2025-12", "end": "present", "rank": "副省级", "note": "2025年12月任代市长，2026年1月正式当选"},
    {"person_id": 3, "org_id": 3, "title": "成都市人大常委会主任", "start": "2026-01", "end": "present", "rank": "副省级", "note": ""},
    {"person_id": 4, "org_id": 4, "title": "成都市政协主席", "start": "2025-02", "end": "present", "rank": "副省级", "note": ""},
    {"person_id": 5, "org_id": 5, "title": "成都市监察委员会主任", "start": "2021-12", "end": "present", "rank": "副省级", "note": ""},

    # 曹立军 previous positions
    {"person_id": 1, "org_id": 6, "title": "四川省委常委", "start": "2022-03", "end": "present", "rank": "副省级", "note": ""},
    {"person_id": 1, "org_id": 8, "title": "绵阳市委书记", "start": "2022-01", "end": "2024-08", "rank": "地厅级", "note": "兼任四川省委常委从2022年3月开始"},
    {"person_id": 1, "org_id": 7, "title": "四川省副省长", "start": "2020-07", "end": "2022-03", "rank": "副省级", "note": ""},
    {"person_id": 1, "org_id": 19, "title": "常德市市长", "start": "2017-09", "end": "2020-07", "rank": "地厅级", "note": ""},
    {"person_id": 1, "org_id": 17, "title": "长沙市副市长兼浏阳市委书记", "start": "2013-01", "end": "2017-03", "rank": "副厅级", "note": ""},
    {"person_id": 1, "org_id": 17, "title": "浏阳市委书记（长沙市委常委兼任）", "start": "2015-08", "end": "2017-03", "rank": "副厅级", "note": "同时任长沙市委常委"},
    {"person_id": 1, "org_id": 17, "title": "浏阳市市长", "start": "2011-05", "end": "2012-12", "rank": "县处级", "note": "兼长沙国家生物产业基地党工委副书记"},
    {"person_id": 1, "org_id": 17, "title": "长沙市天心区区长", "start": "2008-04", "end": "2011-05", "rank": "县处级", "note": ""},
    {"person_id": 1, "org_id": 16, "title": "长沙市信访局局长、市政府副秘书长", "start": "2004-09", "end": "2008-04", "rank": "县处级", "note": ""},
    {"person_id": 1, "org_id": 17, "title": "长沙市政府办公厅副主任", "start": "2001-11", "end": "2004-09", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 17, "title": "长沙市政府办公厅秘书一处处长", "start": "2000-11", "end": "2001-11", "rank": "正科级", "note": ""},

    # 陈书平 previous positions
    {"person_id": 2, "org_id": 7, "title": "四川省副省长", "start": "2025-07", "end": "2025-12", "rank": "副省级", "note": ""},
    {"person_id": 2, "org_id": 7, "title": "四川省政府秘书长", "start": "2025-03", "end": "2025-09", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 10, "title": "四川省财政厅厅长", "start": "2022-07", "end": "2025-05", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 11, "title": "四川省交通运输厅厅长", "start": "2022-04", "end": "2022-07", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 12, "title": "四川省政府副秘书长", "start": "", "end": "2022-04", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 10, "title": "四川省财政厅副厅长", "start": "", "end": "", "rank": "副厅级", "note": ""},

    # 曾卿 previous positions
    {"person_id": 4, "org_id": 7, "title": "四川省政府秘书长", "start": "2022-09", "end": "2025-02", "rank": "正厅级", "note": ""},
    {"person_id": 4, "org_id": 13, "title": "四川省商务厅厅长", "start": "2021-05", "end": "2022-09", "rank": "正厅级", "note": ""},
    {"person_id": 4, "org_id": 14, "title": "广安市委书记（副书记）", "start": "2017-09", "end": "2021-05", "rank": "正厅级", "note": "广安市委副书记、市长"},
    {"person_id": 4, "org_id": 15, "title": "广安市市长", "start": "2017-09", "end": "2021-05", "rank": "正厅级", "note": ""},
    {"person_id": 4, "org_id": 6, "title": "四川省委副秘书长、政研室主任", "start": "2015-03", "end": "2017-09", "rank": "正厅级", "note": ""},
    {"person_id": 4, "org_id": 6, "title": "四川省委办公厅副主任、综合室主任", "start": "2010-01", "end": "2015-03", "rank": "副厅级", "note": ""},

    # 施小琳 — predecessor as Chengdu Party Secretary
    {"person_id": 50, "org_id": 7, "title": "四川省省长", "start": "2024-07", "end": "present", "rank": "正省级", "note": "2024年7月代理，2024年7月31日当选"},
    {"person_id": 50, "org_id": 6, "title": "四川省委副书记", "start": "2023-07", "end": "present", "rank": "副省级", "note": ""},
    {"person_id": 50, "org_id": 1, "title": "成都市委书记", "start": "2021-08", "end": "2024-06", "rank": "副省级", "note": ""},
    {"person_id": 50, "org_id": 6, "title": "四川省委常委", "start": "2021-08", "end": "2024-07", "rank": "副省级", "note": ""},
    {"person_id": 50, "org_id": 6, "title": "江西省委常委、宣传部部长", "start": "2018-05", "end": "2021-08", "rank": "副省级", "note": ""},
    {"person_id": 50, "org_id": 6, "title": "上海市委常委、统战部部长", "start": "2017-05", "end": "2018-05", "rank": "副省级", "note": ""},

    # 范锐平 -- predecessor
    {"person_id": 51, "org_id": 1, "title": "成都市委书记", "start": "2017-04", "end": "2021-08", "rank": "副省级", "note": ""},
    {"person_id": 51, "org_id": 6, "title": "四川省委组织部部长", "start": "2013-05", "end": "2017-04", "rank": "副省级", "note": ""},
    {"person_id": 51, "org_id": 6, "title": "湖北省委常委、襄阳市委书记", "start": "2011-08", "end": "2013-05", "rank": "副省级", "note": ""},

    # 王凤朝 -- predecessor mayor
    {"person_id": 52, "org_id": 2, "title": "成都市市长", "start": "2020", "end": "2025-12", "rank": "副省级", "note": ""},

    # 唐良智 -- 接替范锐平任前成都市委书记的前任
    # (Note: 唐良智 actually was mayor, then went to Chongqing -范锐平preceded him)
    {"person_id": 53, "org_id": 8, "title": "绵阳市委书记", "start": "", "end": "2022-01", "rank": "地厅级", "note": "被曹立军接替"},
]

# ── RELATIONSHIPS ─────────────────────────────────────────────────────

relationships = [
    # 曹立军 ↔ 陈书平 (current top duo)
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "市委书市与市长搭档", "overlap_org": "中共成都市委员会/成都市人民政府",
     "overlap_period": "2025-12至今", "confidence": "confirmed"},

    # 曹立军 → 施小琳 (predecessor-successor, Party Secretary)
    {"person_a": 1, "person_b": 50, "type": "predecessor_successor",
     "context": "曹立军接替施小琳任成都市委书记", "overlap_org": "中共成都市委员会",
     "overlap_period": "2024-08", "confidence": "confirmed"},

    # 施小琳 → 范锐平 (predecessor-successor, Party Secretary)
    {"person_a": 50, "person_b": 51, "type": "predecessor_successor",
     "context": "施小琳接替范锐平任成都市委书记", "overlap_org": "中共成都市委员会",
     "overlap_period": "2021-08", "confidence": "confirmed"},

    # 陈书平 → 王凤朝 (predecessor-successor, Mayor)
    {"person_a": 2, "person_b": 52, "type": "predecessor_successor",
     "context": "陈书平接替王凤朝任成都市市长", "overlap_org": "成都市人民政府",
     "overlap_period": "2025-12", "confidence": "confirmed"},

    # 曹立军 → 唐良斌 (predecessor, Mianyang)
    {"person_a": 1, "person_b": 53, "type": "predecessor_successor",
     "context": "曹立军接替罗增斌任绵阳市委书记", "overlap_org": "中共绵阳市委",
     "overlap_period": "2022-01", "confidence": "confirmed"},

    # 曾卿 → 陈书平 (省政府秘书长前后任)
    {"person_a": 4, "person_b": 2, "type": "predecessor_successor",
     "context": "曾卿任省政府秘书长、陈书平接任", "overlap_org": "四川省人民政府办公厅",
     "overlap_period": "2025-03", "confidence": "confirmed"},

    # 施小琳 ↔ 曾卿 (曾在省政府工作期间)
    {"person_a": 50, "person_b": 4, "type": "overlap",
     "context": "施小琳任省长、曾卿任省政府秘书长期间共事", "overlap_org": "四川省人民政府",
     "overlap_period": "2024-07至2025-02", "confidence": "confirmed"},
]


# ── BUILD ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    run_build(
        slug="成都市",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print("\nDone. Files created:")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")