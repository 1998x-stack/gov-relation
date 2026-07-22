#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 益阳市 (Yiyang City) leadership network."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/yiyang_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/yiyang_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ═══════════════════════════════════════════════════════════════
    # A. CITY LEVEL (市级领导)
    # ═══════════════════════════════════════════════════════════════

    # ── 1. 市委书记 ──
    {"id": 1, "name": "向世聪", "gender": "男", "ethnicity": "汉族",
     "birth": "1971-12", "birthplace": "湖南省隆回县", "education": "在职研究生，管理学博士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "益阳市委书记", "current_org": "中共益阳市委",
     "source": "https://zh.wikipedia.org/wiki/%E7%9B%8A%E9%98%B3%E5%B8%82,http://district.ce.cn/newarea/sddy/202605/t20260516_2970838.shtml"},

    # ── 2. 市长(代) ──
    {"id": 2, "name": "刘勇会", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-05", "birthplace": "湖南省永州市", "education": "研究生（零陵师范专科学校/湖南科技学院）",
     "party_join": "中共党员", "work_start": "",
     "current_post": "益阳市代市长", "current_org": "益阳市人民政府",
     "source": "https://zh.wikipedia.org/wiki/%E5%88%98%E5%8B%87%E4%BC%9A,http://district.ce.cn/newarea/sddy/202604/t20260423_2922443.shtml"},

    # ── 3. 人大主任 ──
    {"id": 3, "name": "刘泽友", "gender": "男", "ethnicity": "汉族",
     "birth": "1966-11", "birthplace": "湖南省新邵县", "education": "【待查】",
     "party_join": "中共党员", "work_start": "",
     "current_post": "益阳市人大常委会主任", "current_org": "益阳市人大常委会",
     "source": "https://zh.wikipedia.org/wiki/%E7%9B%8A%E9%98%B3%E5%B8%82"},

    # ── 4. 政协主席 ──
    {"id": 4, "name": "胡立安", "gender": "男", "ethnicity": "汉族",
     "birth": "1966-04", "birthplace": "湖南省安化县", "education": "【待查】",
     "party_join": "中共党员", "work_start": "",
     "current_post": "益阳市政协主席", "current_org": "益阳市政协",
     "source": "https://zh.wikipedia.org/wiki/%E7%9B%8A%E9%98%B3%E5%B8%82"},

    # ── 5. 市委副书记、统战部长 ──
    {"id": 5, "name": "邓斌", "gender": "男", "ethnicity": "汉族",
     "birth": "1977", "birthplace": "【待查】", "education": "【待查】",
     "party_join": "中共党员", "work_start": "",
     "current_post": "益阳市委副书记、统战部长", "current_org": "中共益阳市委",
     "source": "https://zh.wikipedia.org/wiki/%E4%B8%AD%E5%9B%BD%E5%85%B1%E4%BA%A7%E5%85%9A%E7%9B%8A%E9%98%B3%E5%B8%82%E5%A7%94%E5%91%98%E4%BC%9A"},

    # ── 6. 前任市委书记→副省长→长沙书记 ──
    {"id": 6, "name": "陈竞", "gender": "男", "ethnicity": "汉族",
     "birth": "1971-02", "birthplace": "湖南省长沙市", "education": "大学学历，公共管理硕士（省委党校）",
     "party_join": "1993-12", "work_start": "1990-07",
     "current_post": "湖南省副省长、长沙市委书记", "current_org": "中共长沙市委",
     "source": "https://zh.wikipedia.org/wiki/%E9%99%88%E7%AB%9E_(1971%E5%B9%B4)"},

    # ── 7. 前任市委书记 (2016-2023) ──
    {"id": 7, "name": "瞿海", "gender": "男", "ethnicity": "苗族",
     "birth": "1966-01", "birthplace": "湖南省沅陵县", "education": "【待查】",
     "party_join": "中共党员", "work_start": "",
     "current_post": "前益阳市委书记（2016-2023）", "current_org": "中共益阳市委（前任）",
     "source": "https://zh.wikipedia.org/wiki/%E7%9E%BF%E6%B5%B7"},

    # ── 8. 前任市长→省政府副秘书长 ──
    {"id": 8, "name": "熊炜", "gender": "男", "ethnicity": "汉族",
     "birth": "1975", "birthplace": "【待查】", "education": "【待查】",
     "party_join": "中共党员", "work_start": "",
     "current_post": "湖南省人民政府副秘书长", "current_org": "湖南省人民政府",
     "source": "益阳市人大决定、湖南高校官宣新闻"},

    # ═══════════════════════════════════════════════════════════════
    # B. DISTRICT/COUNTY LEVEL — 6 regions, 12 positions
    # ═══════════════════════════════════════════════════════════════

    # ── 资阳区 ──
    {"id": 11, "name": "付振南", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "【待查】", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "资阳区委书记", "current_org": "中共资阳区委",
     "source": "资阳区人民政府网站2026新年贺词"},
    {"id": 12, "name": "黄瑛", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "【待查】", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "资阳区区长", "current_org": "资阳区人民政府",
     "source": "资阳区人民政府2025年政府工作报告"},

    # ── 赫山区 ──
    {"id": 13, "name": "李丰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "【待查】", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "赫山区委书记、区长", "current_org": "中共赫山区委/赫山区人民政府",
     "source": "https://baike.baidu.com/item/%E8%B5%AB%E5%B1%B1%E5%8C%BA"},

    # ── 南县 ──
    {"id": 14, "name": "钟剑波", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-11", "birthplace": "湖南省桃江县", "education": "【待查】",
     "party_join": "", "work_start": "",
     "current_post": "南县县委书记、县长", "current_org": "中共南县县委/南县人民政府",
     "source": "https://zh.wikipedia.org/wiki/%E5%8D%97%E5%8E%BF"},

    # ── 桃江县 ──
    {"id": 15, "name": "向荣", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-09", "birthplace": "湖南省沅江市", "education": "【待查】",
     "party_join": "", "work_start": "",
     "current_post": "桃江县委书记", "current_org": "中共桃江县委",
     "source": "https://zh.wikipedia.org/wiki/%E6%A1%83%E6%B1%9F%E5%8E%BF"},
    {"id": 16, "name": "周登高", "gender": "男", "ethnicity": "汉族",
     "birth": "1982-09", "birthplace": "湖南省宁乡市", "education": "湘潭大学行政管理专业管理学硕士",
     "party_join": "2004-12", "work_start": "2000-07",
     "current_post": "桃江县县长", "current_org": "桃江县人民政府",
     "source": "https://zh.wikipedia.org/wiki/%E5%91%A8%E7%99%BB%E9%AB%98"},

    # ── 安化县 ──
    {"id": 17, "name": "石录明", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-10", "birthplace": "湖南省益阳市资阳区", "education": "【待查】",
     "party_join": "", "work_start": "",
     "current_post": "安化县委书记", "current_org": "中共安化县委",
     "source": "https://zh.wikipedia.org/wiki/%E5%AE%89%E5%8C%96%E5%8E%BF,澎湃新闻2022-01-16"},
    {"id": 18, "name": "潘文剑", "gender": "男", "ethnicity": "汉族",
     "birth": "1984-07", "birthplace": "湖南省南县", "education": "【待查】",
     "party_join": "", "work_start": "",
     "current_post": "安化县县长", "current_org": "安化县人民政府",
     "source": "https://zh.wikipedia.org/wiki/%E5%AE%89%E5%8C%96%E5%8E%BF"},

    # ── 沅江市 ──
    {"id": 19, "name": "杨智勇", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-11", "birthplace": "湖南省宁乡市", "education": "湖南师范大学历史系历史学学士/硕士/博士",
     "party_join": "1995-12", "work_start": "1997",
     "current_post": "沅江市委书记", "current_org": "中共沅江市委",
     "source": "https://zh.wikipedia.org/wiki/%E6%9D%A8%E6%99%BA%E5%8B%87"},
    {"id": 20, "name": "罗必胜", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-04", "birthplace": "湖南省安化县", "education": "【待查】",
     "party_join": "", "work_start": "",
     "current_post": "沅江市市长", "current_org": "沅江市人民政府",
     "source": "https://zh.wikipedia.org/wiki/%E6%B2%85%E6%B1%9F%E5%B8%82"},
]

# ═══════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ═══════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共益阳市委", "type": "党委", "level": "地市级", "parent": "中共湖南省委", "location": "益阳市"},
    {"id": 2, "name": "益阳市人民政府", "type": "政府", "level": "地市级", "parent": "湖南省人民政府", "location": "益阳市"},
    {"id": 3, "name": "益阳市人大常委会", "type": "人大", "level": "地市级", "parent": "湖南省人大常委会", "location": "益阳市"},
    {"id": 4, "name": "益阳市政协", "type": "政协", "level": "地市级", "parent": "湖南省政协", "location": "益阳市"},
    {"id": 5, "name": "中共资阳区委", "type": "党委", "level": "县级", "parent": "中共益阳市委", "location": "资阳区"},
    {"id": 6, "name": "资阳区人民政府", "type": "政府", "level": "县级", "parent": "益阳市人民政府", "location": "资阳区"},
    {"id": 7, "name": "中共赫山区委", "type": "党委", "level": "县级", "parent": "中共益阳市委", "location": "赫山区"},
    {"id": 8, "name": "赫山区人民政府", "type": "政府", "level": "县级", "parent": "益阳市人民政府", "location": "赫山区"},
    {"id": 9, "name": "中共南县县委", "type": "党委", "level": "县级", "parent": "中共益阳市委", "location": "南县"},
    {"id": 10, "name": "南县人民政府", "type": "政府", "level": "县级", "parent": "益阳市人民政府", "location": "南县"},
    {"id": 11, "name": "中共桃江县委", "type": "党委", "level": "县级", "parent": "中共益阳市委", "location": "桃江县"},
    {"id": 12, "name": "桃江县人民政府", "type": "政府", "level": "县级", "parent": "益阳市人民政府", "location": "桃江县"},
    {"id": 13, "name": "中共安化县委", "type": "党委", "level": "县级", "parent": "中共益阳市委", "location": "安化县"},
    {"id": 14, "name": "安化县人民政府", "type": "政府", "level": "县级", "parent": "益阳市人民政府", "location": "安化县"},
    {"id": 15, "name": "中共沅江市委", "type": "党委", "level": "县级", "parent": "中共益阳市委", "location": "沅江市"},
    {"id": 16, "name": "沅江市人民政府", "type": "政府", "level": "县级", "parent": "益阳市人民政府", "location": "沅江市"},
    {"id": 17, "name": "湖南省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "长沙市"},
    {"id": 18, "name": "中共长沙市委", "type": "党委", "level": "副省级", "parent": "中共湖南省委", "location": "长沙市"},
]

# ═══════════════════════════════════════════════════════════════════
# POSITIONS (person_id, org_id, title, start, end, rank, note)
# ═══════════════════════════════════════════════════════════════════

positions = [
    # ── 向世聪 ──
    {"person_id": 1, "org_id": 1, "title": "益阳市委书记", "start": "2026-05", "end": "", "rank": "正厅", "note": "现任"},
    {"person_id": 1, "org_id": 17, "title": "省统计局党组书记、局长", "start": "", "end": "2026-05", "rank": "正厅", "note": "此前职务"},

    # ── 刘勇会 ──
    {"person_id": 2, "org_id": 2, "title": "益阳市代市长", "start": "2026-04", "end": "", "rank": "正厅", "note": "现任"},
    {"person_id": 2, "org_id": 1, "title": "益阳市委副书记", "start": "2026-04", "end": "", "rank": "正厅", "note": "现任"},
    {"person_id": 2, "org_id": 2, "title": "益阳市副市长", "start": "2022-01", "end": "2026-04", "rank": "副厅", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "益阳市委常委", "start": "2021-10", "end": "2026-04", "rank": "副厅", "note": ""},
    {"person_id": 2, "org_id": 13, "title": "安化县委书记", "start": "2019-04", "end": "2021-10", "rank": "正处", "note": "全国优秀县委书记2021"},
    {"person_id": 2, "org_id": 1, "title": "道县县委书记", "start": "2016-08", "end": "2019-03", "rank": "正处", "note": "道县属永州市"},
    {"person_id": 2, "org_id": 1, "title": "道县县长", "start": "", "end": "2016-07", "rank": "正处", "note": ""},

    # ── 刘泽友 ──
    {"person_id": 3, "org_id": 3, "title": "益阳市人大常委会主任", "start": "2024-12", "end": "", "rank": "正厅", "note": "现任"},

    # ── 胡立安 ──
    {"person_id": 4, "org_id": 4, "title": "益阳市政协主席", "start": "2022-01", "end": "", "rank": "正厅", "note": "现任"},

    # ── 邓斌 ──
    {"person_id": 5, "org_id": 1, "title": "益阳市委副书记、统战部长", "start": "", "end": "", "rank": "副厅", "note": "现任"},

    # ── 陈竞 ──
    {"person_id": 6, "org_id": 18, "title": "长沙市委书记", "start": "2026-06", "end": "", "rank": "副部", "note": "现任"},
    {"person_id": 6, "org_id": 17, "title": "湖南省副省长", "start": "2025-07", "end": "", "rank": "副部", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "益阳市委书记", "start": "2023-02", "end": "2026-05", "rank": "正厅", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "益阳市市长", "start": "2021-08", "end": "2023-02", "rank": "正厅", "note": ""},

    # ── 瞿海 ──
    {"person_id": 7, "org_id": 1, "title": "益阳市委书记", "start": "2016-12", "end": "2023-02", "rank": "正厅", "note": ""},

    # ── 熊炜 ──
    {"person_id": 8, "org_id": 17, "title": "省政府副秘书长", "start": "2026-04", "end": "", "rank": "副厅", "note": "现任"},
    {"person_id": 8, "org_id": 2, "title": "益阳市市长", "start": "2023-02", "end": "2026-04", "rank": "正厅", "note": ""},

    # ── 付振南 ──
    {"person_id": 11, "org_id": 5, "title": "资阳区委书记", "start": "", "end": "", "rank": "正处", "note": "现任"},

    # ── 黄瑛 ──
    {"person_id": 12, "org_id": 6, "title": "资阳区区长", "start": "", "end": "", "rank": "正处", "note": "现任"},

    # ── 李丰 ──
    {"person_id": 13, "org_id": 7, "title": "赫山区委书记", "start": "", "end": "", "rank": "正处", "note": "现任"},
    {"person_id": 13, "org_id": 8, "title": "赫山区区长", "start": "", "end": "", "rank": "正处", "note": "兼任"},

    # ── 钟剑波 ──
    {"person_id": 14, "org_id": 9, "title": "南县县委书记", "start": "2025-02", "end": "", "rank": "正处", "note": "现任"},
    {"person_id": 14, "org_id": 10, "title": "南县县长", "start": "2021-10", "end": "", "rank": "正处", "note": "兼任"},

    # ── 向荣 ──
    {"person_id": 15, "org_id": 11, "title": "桃江县委书记", "start": "2021-07", "end": "", "rank": "正处", "note": "现任"},

    # ── 周登高 ──
    {"person_id": 16, "org_id": 12, "title": "桃江县县长", "start": "2021-07", "end": "", "rank": "正处", "note": "现任"},
    {"person_id": 16, "org_id": 13, "title": "安化县委副书记", "start": "2020-04", "end": "2021-07", "rank": "副处", "note": ""},
    {"person_id": 16, "org_id": 13, "title": "安化县副县长", "start": "2012-11", "end": "2016-08", "rank": "副处", "note": ""},

    # ── 石录明 ──
    {"person_id": 17, "org_id": 13, "title": "安化县委书记", "start": "2022-01", "end": "", "rank": "正处", "note": "现任"},

    # ── 潘文剑 ──
    {"person_id": 18, "org_id": 14, "title": "安化县县长", "start": "2022-06", "end": "", "rank": "正处", "note": "现任"},

    # ── 杨智勇 ──
    {"person_id": 19, "org_id": 15, "title": "沅江市委书记", "start": "2021-07", "end": "", "rank": "正处", "note": "现任"},
    {"person_id": 19, "org_id": 16, "title": "沅江市市长", "start": "2017-12", "end": "2021-07", "rank": "正处", "note": ""},
    {"person_id": 19, "org_id": 5, "title": "资阳区委副书记", "start": "2016-08", "end": "2017-05", "rank": "副处", "note": ""},

    # ── 罗必胜 ──
    {"person_id": 20, "org_id": 16, "title": "沅江市市长", "start": "2021-10", "end": "", "rank": "正处", "note": "现任"},
]

# ═══════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ═══════════════════════════════════════════════════════════════════

relationships = [
    # 陈竞 → 刘勇会：益阳市委/市政府共事关系
    {"person_a": 6, "person_b": 2, "type": "上下级", "context": "陈竞任益阳市委书记期间，刘勇会先后任副市长、代市长", "overlap_org": "益阳市委/市政府", "overlap_period": "2021-2026"},

    # 刘勇会 → 石录明：安化县前后任书记
    {"person_a": 2, "person_b": 17, "type": "前后任", "context": "刘勇会2021年离任安化县委书记后，石录明2022年接任", "overlap_org": "安化县委", "overlap_period": "2019-2022"},

    # 刘勇会 → 潘文剑：安化县同僚
    {"person_a": 2, "person_b": 18, "type": "间接上下级", "context": "刘勇会任安化书记期间(2019-2021)，潘文剑当时可能已在该体系", "overlap_org": "安化县", "overlap_period": "2019-2021"},

    # 周登高 → 刘勇会：安化县前后工作交集
    {"person_a": 16, "person_b": 2, "type": "间接共事", "context": "周登高任安化副县长(2012-2016)、县委副书记(2020-2021)，与刘勇会安化书记任期部分重叠", "overlap_org": "安化县", "overlap_period": "2020-2021"},

    # 杨智勇 → 付振南：资阳区先后任职
    {"person_a": 19, "person_b": 11, "type": "前后任", "context": "杨智勇曾任资阳区委副书记(2016-2017)，付振南现任资阳区委书记", "overlap_org": "资阳区委", "overlap_period": "2016-至今"},

    # 陈竞 → 熊炜：市委/市政府共事
    {"person_a": 6, "person_b": 8, "type": "上下级", "context": "陈竞任书记期间，熊炜任市长", "overlap_org": "益阳市委/市政府", "overlap_period": "2023-2026"},

    # 向荣 → 周登高：桃江县委/县政府正职搭档
    {"person_a": 15, "person_b": 16, "type": "搭档", "context": "向荣(书记)+周登高(县长)为桃江县党政正职搭档", "overlap_org": "桃江县", "overlap_period": "2021-至今"},

    # 杨智勇 → 罗必胜：沅江市前后任市长
    {"person_a": 19, "person_b": 20, "type": "前后任", "context": "杨智勇任沅江市长(2017-2021)后升书记，罗必胜接任市长(2021.10)", "overlap_org": "沅江市", "overlap_period": "2021-至今"},
]


# ── BUILD DATABASE ─────────────────────────────────────────────────

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS relationships")
c.execute("DROP TABLE IF EXISTS positions")
c.execute("DROP TABLE IF EXISTS organizations")
c.execute("DROP TABLE IF EXISTS persons")

c.execute("""
CREATE TABLE persons (
    id INTEGER PRIMARY KEY,
    name TEXT, gender TEXT, ethnicity TEXT,
    birth TEXT, birthplace TEXT, education TEXT,
    party_join TEXT, work_start TEXT,
    current_post TEXT, current_org TEXT, source TEXT,
    notes TEXT DEFAULT ''
)
""")
c.execute("""
CREATE TABLE organizations (
    id INTEGER PRIMARY KEY,
    name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
)
""")
c.execute("""
CREATE TABLE positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER, org_id INTEGER,
    title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
)
""")
c.execute("""
CREATE TABLE relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a INTEGER, person_b INTEGER,
    type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT,
    FOREIGN KEY (person_a) REFERENCES persons(id),
    FOREIGN KEY (person_b) REFERENCES persons(id)
)
""")

for p in persons:
    c.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
              (p["id"], p["name"], p["gender"], p["ethnicity"],
               p["birth"], p["birthplace"], p["education"],
               p["party_join"], p["work_start"],
               p["current_post"], p["current_org"], p["source"], ""))

for o in organizations:
    c.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)",
              (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for pos in positions:
    c.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)",
              (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))

for r in relationships:
    c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
              (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

conn.commit()
conn.close()
print(f"✅ Database created: {DB_PATH}")
print(f"   Persons: {len(persons)}")
print(f"   Organizations: {len(organizations)}")
print(f"   Positions: {len(positions)}")
print(f"   Relationships: {len(relationships)}")

# ── BUILD GEXF ─────────────────────────────────────────────────────

os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

def color_hex(r, g, b):
    """Return hex color string for GEXF viz."""
    return f"#{r:02x}{g:02x}{b:02x}"

# Determine node colors by role
node_colors = {}
for p in persons:
    post = p["current_post"]
    pid = p["id"]
    if "书记" in post and "副" not in post and "总" not in post:
        node_colors[pid] = color_hex(220, 50, 50)  # Red for party secretary
    elif "市长" in post or "区长" in post or "县长" in post:
        node_colors[pid] = color_hex(50, 120, 220)  # Blue for gov head
    elif "人大" in post:
        node_colors[pid] = color_hex(50, 180, 100)  # Green for NPC
    elif "政协" in post:
        node_colors[pid] = color_hex(180, 130, 50)  # Gold for CPPCC
    elif "副" in post:
        node_colors[pid] = color_hex(220, 150, 50)  # Orange for deputy
    else:
        node_colors[pid] = color_hex(150, 150, 150)  # Grey for others

org_ids = {o["id"] for o in organizations}
org_names = {o["id"]: o["name"] for o in organizations}
collected_person_ids = set()
for pos in positions:
    collected_person_ids.add(pos["person_id"])

gexf_parts = []
gexf_parts.append('<?xml version="1.0" encoding="UTF-8"?>')
gexf_parts.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
gexf_parts.append('  <graph mode="static" defaultedgetype="undirected">')

# ── Nodes ──
gexf_parts.append('    <nodes>')

# Person nodes
for p in persons:
    pid = p["id"]
    label = f'{p["name"]}\\n{p["current_post"]}'
    color = node_colors.get(pid, "#969696")
    # Size based on role importance
    if any(p["current_post"].startswith(x) for x in ["益阳市委书记", "益阳市代市长", "湖南省副省长"]):
        size = 20.0
    elif any(p["current_post"].startswith(x) for x in ["人大主任", "政协主席", "副书记"]):
        size = 15.0
    elif any(p["current_post"].startswith(x) for x in ["前任", "区委书记", "县委书记", "市委书记", "区长", "市长", "县长"]):
        size = 12.0
    else:
        size = 10.0
    gexf_parts.append(f'      <node id="person_{pid}" label="{label}">')
    gexf_parts.append(f'        <attvalues>')
    gexf_parts.append(f'          <attvalue for="type" value="person"/>')
    gexf_parts.append(f'          <attvalue for="name" value="{p["name"]}"/>')
    gexf_parts.append(f'          <attvalue for="role" value="{p["current_post"]}"/>')
    gexf_parts.append(f'          <attvalue for="birth" value="{p["birth"]}"/>')
    gexf_parts.append(f'          <attvalue for="birthplace" value="{p["birthplace"]}"/>')
    gexf_parts.append(f'        </attvalues>')
    gexf_parts.append(f'        <viz:color r="{int(color[1:3],16)}" g="{int(color[3:5],16)}" b="{int(color[5:7],16)}"/>')
    gexf_parts.append(f'        <viz:size value="{size}"/>')
    gexf_parts.append(f'      </node>')

# Organization nodes
for o in organizations:
    oid = o["id"]
    label = o["name"]
    gexf_parts.append(f'      <node id="org_{oid}" label="{label}">')
    gexf_parts.append(f'        <attvalues>')
    gexf_parts.append(f'          <attvalue for="type" value="organization"/>')
    gexf_parts.append(f'          <attvalue for="name" value="{o["name"]}"/>')
    gexf_parts.append(f'          <attvalue for="org_type" value="{o["type"]}"/>')
    gexf_parts.append(f'        </attvalues>')
    gexf_parts.append(f'        <viz:color r="100" g="100" b="100"/>')
    gexf_parts.append(f'        <viz:size value="8.0"/>')
    gexf_parts.append(f'      </node>')

gexf_parts.append('    </nodes>')

# ── Edges ──
gexf_parts.append('    <edges>')

edge_id = 0

# Person → Organization edges (worked_at)
for pos in positions:
    pid = pos["person_id"]
    oid = pos["org_id"]
    if pid not in collected_person_ids:
        continue
    edge_id += 1
    label = f'{pos["title"]} ({pos["start"]}-{pos["end"] or "今"})'
    gexf_parts.append(f'      <edge id="e{edge_id}" source="person_{pid}" target="org_{oid}" label="{label}" type="directed">')
    gexf_parts.append(f'        <attvalues>')
    gexf_parts.append(f'          <attvalue for="edge_type" value="worked_at"/>')
    gexf_parts.append(f'          <attvalue for="title" value="{pos["title"]}"/>')
    gexf_parts.append(f'          <attvalue for="start" value="{pos["start"]}"/>')
    gexf_parts.append(f'          <attvalue for="end" value="{pos["end"] or "present"}"/>')
    gexf_parts.append(f'        </attvalues>')
    gexf_parts.append(f'        <viz:color r="180" g="180" b="180"/>')
    gexf_parts.append(f'        <viz:thickness value="1.0"/>')
    gexf_parts.append(f'      </edge>')

# Person ↔ Person edges (relationship)
for r in relationships:
    edge_id += 1
    label = f'{r["type"]}: {r["context"]}'
    gexf_parts.append(f'      <edge id="e{edge_id}" source="person_{r["person_a"]}" target="person_{r["person_b"]}" label="{label}">')
    gexf_parts.append(f'        <attvalues>')
    gexf_parts.append(f'          <attvalue for="edge_type" value="relationship"/>')
    gexf_parts.append(f'          <attvalue for="rel_type" value="{r["type"]}"/>')
    gexf_parts.append(f'          <attvalue for="context" value="{r["context"]}"/>')
    gexf_parts.append(f'          <attvalue for="overlap_org" value="{r["overlap_org"]}"/>')
    gexf_parts.append(f'          <attvalue for="overlap_period" value="{r["overlap_period"]}"/>')
    gexf_parts.append(f'        </attvalues>')
    # Strong relationships (上下级, 搭档) = gold, weak (前后任) = blue
    if r["type"] in ("上下级", "搭档"):
        gexf_parts.append(f'        <viz:color r="201" g="169" b="78"/>')
        gexf_parts.append(f'        <viz:thickness value="3.0"/>')
    elif r["type"] == "前后任":
        gexf_parts.append(f'        <viz:color r="100" g="150" b="220"/>')
        gexf_parts.append(f'        <viz:thickness value="1.5"/>')
    else:
        gexf_parts.append(f'        <viz:color r="150" g="150" b="200"/>')
        gexf_parts.append(f'        <viz:thickness value="1.0"/>')
    gexf_parts.append(f'      </edge>')

gexf_parts.append('    </edges>')

# ── Attributes ──
gexf_parts.append('    <attributes class="node">')
gexf_parts.append('      <attribute id="type" title="Type" type="string"/>')
gexf_parts.append('      <attribute id="name" title="Name" type="string"/>')
gexf_parts.append('      <attribute id="role" title="Role" type="string"/>')
gexf_parts.append('      <attribute id="birth" title="Birth" type="string"/>')
gexf_parts.append('      <attribute id="birthplace" title="Birthplace" type="string"/>')
gexf_parts.append('      <attribute id="org_type" title="Org Type" type="string"/>')
gexf_parts.append('    </attributes>')
gexf_parts.append('    <attributes class="edge">')
gexf_parts.append('      <attribute id="edge_type" title="Edge Type" type="string"/>')
gexf_parts.append('      <attribute id="title" title="Title" type="string"/>')
gexf_parts.append('      <attribute id="start" title="Start" type="string"/>')
gexf_parts.append('      <attribute id="end" title="End" type="string"/>')
gexf_parts.append('      <attribute id="rel_type" title="Relation Type" type="string"/>')
gexf_parts.append('      <attribute id="context" title="Context" type="string"/>')
gexf_parts.append('      <attribute id="overlap_org" title="Overlap Org" type="string"/>')
gexf_parts.append('      <attribute id="overlap_period" title="Overlap Period" type="string"/>')
gexf_parts.append('    </attributes>')

gexf_parts.append('  </graph>')
gexf_parts.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(gexf_parts))

print(f"✅ GEXF created: {GEXF_PATH}")
print(f"   Nodes: {len(persons) + len(organizations)}")
print(f"   Edges: {edge_id}")
print()
print("📊 Summary:")
print(f"   Person nodes: {len(persons)}")
print(f"   Organization nodes: {len(organizations)}")
print(f"   Position edges: {len(positions)}")
print(f"   Relationship edges: {len(relationships)}")
