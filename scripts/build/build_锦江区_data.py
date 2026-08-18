#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 锦江区 (Jinjiang District), Chengdu, Sichuan.

Jinjiang (锦江区) is a central urban district of Chengdu (行政区划代码 510104), located in
the southeast of the city core (成都中心城区东南部), 62 km², 11 streets (街道), ~93.10万
resident population (2025末), GDP ~1574.86亿元 (2025).

Target leadership: 区委书记 (District Party Secretary) + 区长 (District Mayor).
Research cut-off: 2026-08-17.

Key findings (sourced):
- 池勇 : 锦江区委书记, appointed 2024-03-01 (source: 锦江发布 via 四川在线/成都广播电视台,
  plus Baidu Baike). 男, 汉族, 1977-01, 四川简阳人, 党校研究生/在职硕士. Career from
  珙县→青羊区→成都市投促委/驻沪→成都市委办公厅→青白江区(区长/区委书记)→锦江区委书记.
- 陈华 : 锦江区人民政府区长, elected by 锦江区第八届人民代表大会第七次会议 on 2026-05-20
  (source: 锦江发布 / 四川在线, official announcement). Previous: 锦江区委副书记 → 代理区长.
- 陈志勇 : former 锦江区委书记, succeeded by 池勇 (2024-03); now 成都市副市长.
- 王乾 : former 锦江区区长 (布依族), later 成都市副市长; exact departure/tenure window to be
  verified (name has multiple holders in Chengdu media).

Confidence notes: exact months for some early 池勇 roles come from 360百科 (good quality,
moderate confidence); 陈华 and 王乾 biographical details (birth, education) are not yet
publicly indexed — left empty / unverified. Do not infer.
"""

import sqlite3
import sys
import os
from pathlib import Path

# Add project root to path (this file lives under data/tmp/锦江区/, repo root is ../../..)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from gov_relation.runner import run_build

# ── Paths ─────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "锦江区_network.db")
GEXF_PATH = os.path.join(BASE, "锦江区_network.gexf")

# ── PERSONS ───────────────────────────────────────────────────────────
# ID scheme: 1-9 top leaders, 10-29 government, 50+ predecessors
persons = [
    # ── Current top leaders ──
    {
        "id": 1,
        "name": "池勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-01",
        "birthplace": "四川省简阳市",
        "education": "西南师范大学资源环境科学学院经济地理学与城乡区域规划学士; 四川省委党校经济学研究生(在职)",
        "party_join": "1998-06",
        "work_start": "2000-07",
        "current_post": "锦江区委书记",
        "current_org": "中共成都市锦江区委员会",
        "source": "https://baike.baidu.com/item/池勇;  https://baike.so.com/doc/4859176-5076622.html; https://sichuan.scol.com.cn/spsc/202403/82476035.html",
    },
    {
        "id": 2,
        "name": "陈华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "锦江区人民政府区长",
        "current_org": "锦江区人民政府",
        "source": "https://sichuan.scol.com.cn/ggxw/202605/83257669.html; https://www.cdjinjiang.gov.cn/gkml/ldcy/1504074705315823616.shtml",
    },
    # ── Predecessors ──
    {
        "id": 3,
        "name": "陈志勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "成都市人民政府副市长",
        "current_org": "成都市人民政府",
        "source": "https://www.cdjinjiang.gov.cn/; https://www.thepaper.cn/newsDetail_forward_16011100",
    },
    {
        "id": 4,
        "name": "王乾",
        "gender": "男",
        "ethnicity": "布依族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "成都市人民政府副市长",
        "current_org": "成都市人民政府",
        "source": "http://renshi.people.com.cn/ ; 中国青年网(任前公示已含简历)",
    },
]

# ── ORGANIZATIONS ─────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共成都市锦江区委员会", "type": "党委", "level": "区级(正处级)", "parent": "中共成都市委", "location": "成都市锦江区"},
    {"id": 2, "name": "锦江区人民政府", "type": "政府", "level": "区级(正处级)", "parent": "成都市人民政府", "location": "成都市锦江区"},
    {"id": 3, "name": "成都市锦江区人民代表大会常务委员会", "type": "人大", "level": "区级", "parent": "", "location": "成都市锦江区"},
    {"id": 4, "name": "中共成都市青羊区委员会", "type": "党委", "level": "区级(正处级)", "parent": "中共成都市委", "location": "成都市青羊区"},
    {"id": 5, "name": "成都市投资促进委员会", "type": "政府", "level": "局级", "parent": "成都市人民政府", "location": "成都市"},
    {"id": 6, "name": "中共成都市委办公厅", "type": "党委", "level": "副省级机构", "parent": "中共成都市委", "location": "成都市"},
    {"id": 7, "name": "中共成都市青白江区委员会", "type": "党委", "level": "区级(正处级)", "parent": "中共成都市委", "location": "成都市青白江区"},
    {"id": 8, "name": "青白江区人民政府", "type": "政府", "level": "区级(正处级)", "parent": "成都市人民政府", "location": "成都市青白江区"},
    {"id": 9, "name": "中国(四川)自由贸易试验区成都青白江铁路港片区管理局", "type": "政府", "level": "片区(厅级以下)", "parent": "", "location": "成都市青白江区"},
    {"id": 10, "name": "中共成都市委", "type": "党委", "level": "副省级", "parent": "中共四川省委", "location": "成都市"},
    {"id": 11, "name": "成都市人民政府", "type": "政府", "level": "副省级", "parent": "四川省人民政府", "location": "成都市"},
    {"id": 12, "name": "宜宾市珙县(含乡镇、县委办等)", "type": "政府", "level": "县处级", "parent": "宜宾市人民政府", "location": "宜宾市珙县"},
]

# ── POSITIONS (use start_date / end_date to match schema) ─────────────
positions = [
    # 池勇 — 当前
    {"person_id": 1, "org_id": 1, "title": "锦江区委书记", "start_date": "2024-03", "end_date": "present",
     "rank": "区级正职(正处级)", "note": "2024-02-01 领导干部大会宣布省委、市委决定(来源: 锦江发布/成都广播电视台)"},
    # 池勇 — 青白江区
    {"person_id": 1, "org_id": 7, "title": "青白江区委书记", "start_date": "2020-11", "end_date": "2024-03",
     "rank": "区级正职(正处级)", "note": "360百科: 2020.11-2020.12任青白江区委书记(兼自贸区); 后继续任至2024-03"},
    {"person_id": 1, "org_id": 8, "title": "青白江区区长", "start_date": "2017-07", "end_date": "2020-11",
     "rank": "区级正职", "note": "360百科: 2017.03提名为区长人选; 2017.04-07副区长/代区长; 2017.07-2018.06区长; 2018.06-2020.11区长兼自贸区局长"},
    {"person_id": 1, "org_id": 8, "title": "青白江区委副书记、代区长/副区长", "start_date": "2017-04", "end_date": "2017-07",
     "rank": "区级副职→正职", "note": "360百科分段: 2017.03-04副书记+区长人选; 2017.04-07区委副书记、区政府党组书记/副区长/代理区长"},
    {"person_id": 1, "org_id": 9, "title": "自贸区成都青白江铁路港片区管理局局长", "start_date": "2018-06", "end_date": "2020-12", "rank": "", "note": "兼任"},
    # 池勇 — 成都市级
    {"person_id": 1, "org_id": 6, "title": "成都市委副秘书长、市委办公厅主任", "start_date": "2016-09", "end_date": "2017-03", "rank": "局级", "note": "360百科"},
    {"person_id": 1, "org_id": 5, "title": "成都市投资促进委员会党组成员、驻上海中心主任", "start_date": "2015-03", "end_date": "2016-09", "rank": "局级(副局级)", "note": "360百科: 市投促委驻上海投资促进中心(市政府驻上海办事处)主任"},
    # 青羊区
    {"person_id": 1, "org_id": 4, "title": "青羊区副区长等(团区委→区委办→街道→副区长)", "start_date": "2005-12", "end_date": "2015-03", "rank": "区级", "note": "360百科: 青羊区团委书记、区委办副主任(正局级)、金沙街道办事处主任/党工委书记、区政府党组成员/副区长"},
    # 珙县基层
    {"person_id": 1, "org_id": 12, "title": "珙县巡场镇、县委办、文化体育局、王家镇等基层工作", "start_date": "2000-07", "end_date": "2005-12", "rank": "基层", "note": "360百科; 2000.07-2005.12"},

    # 陈华 — 锦江区区长
    {"person_id": 2, "org_id": 2, "title": "锦江区人民政府区长", "start_date": "2026-05", "end_date": "present",
     "rank": "区级正职(正处级)", "note": "2026-05-20 锦江区八届人大七次会议公告选举(锦江发布/四川在线)"},
    {"person_id": 2, "org_id": 2, "title": "锦江区委副书记、代理区长", "start_date": "2025", "end_date": "2026-05",
     "rank": "区级正职(副), 代区长", "note": "成都市锦江区人民代表大会常务委员会关于陈华代理区长的决定; 具体月份待核"},
    {"person_id": 2, "org_id": 1, "title": "锦江区委副书记", "start_date": "2025", "end_date": "present",
     "rank": "区级副职", "note": "陈华同志任中共成都市锦江区委副书记(人事公告); 确切到任日期待核"},

    # 陈志勇 — 前锦江区委书记
    {"person_id": 3, "org_id": 1, "title": "锦江区委书记", "start_date": "", "end_date": "2024-03",
     "rank": "区级正职", "note": "2024-03-01 离任(成都市政府副市长陈志勇不再担任锦江区委书记)"},
    {"person_id": 3, "org_id": 11, "title": "成都市人民政府副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "任渝/换届后持续在任"},

    # 王乾 — 前锦江区区长
    {"person_id": 4, "org_id": 2, "title": "锦江区区长", "start_date": "", "end_date": "", "rank": "区级正职",
     "note": "干部任前公示: 王乾(布依族)任成都市锦江区区长; 随后转任成都市副市长(任期/去职窗口待核)"},
    {"person_id": 4, "org_id": 11, "title": "成都市人民政府副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
]

# ── RELATIONSHIPS ─────────────────────────────────────────────────────
relationships = [
    # 区委书记 ↔ 区长 (current top duo)
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "锦江区委书记—区长搭档（党政一把手）", "overlap_org": "锦江区区委/区政府",
     "overlap_period": "2026-05至今", "confidence": "confirmed"},

    # 区委书记 前任/继任: 陈志勇 → 池勇
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor",
     "context": "池勇接替陈志勇任锦江区委书记(2024-03)", "overlap_org": "中共成都市锦江区委员会",
     "overlap_period": "2024-03", "confidence": "confirmed"},

    # 区长 前任/继任: 王乾 → 陈华
    {"person_a": 2, "person_b": 4, "type": "predecessor_successor",
     "context": "陈华接任锦江区区长；王乾曾任锦江区区长后转任成都市副市长", "overlap_org": "锦江区人民政府",
     "overlap_period": "2020s(窗口待核)", "confidence": "plausible"},

    # 池勇 与 陈志勇 均任 成都市政府相关(王乾/陈志勇 皆成都市副市长) — weak network
    {"person_a": 3, "person_b": 4, "type": "overlap",
     "context": "陈志勇、王乾同为成都市人民政府副市长", "overlap_org": "成都市人民政府",
     "overlap_period": "", "confidence": "plausible"},
]

# ── BUILD ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_build(
        slug="锦江区",
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
