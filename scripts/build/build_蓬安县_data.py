#!/usr/bin/env python3
"""
蓬安县 (Peng'an County, Nanchong City, Sichuan Province)
领导班子工作关系网络 — 数据构建脚本

调查日期: 2026-07-26
信息来源:
  - 蓬安县人民政府官网 (pengan.gov.cn) — 领导信息页面
  - 百度百科 — 唐方春履历
  - 南充市人民政府网站 (nanchong.gov.cn)
"""

import os
import sys
from datetime import datetime

TODAY = "2026-07-26"
SLUG = "蓬安县"
PROVINCE = "四川省"
PARENT_CITY = "南充市"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "蓬安县_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "蓬安县_network.gexf")

# ═══════════════════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════════════════

persons = [
    # ── 1. 县委书记 ──
    {
        "id": 1,
        "name": "唐方春",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-05",
        "birthplace": "",
        "native_place": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "1997-08",
        "current_post": "县委书记",
        "current_org": "中共蓬安县委员会",
        "source": "https://www.pengan.gov.cn/zwgk/fdzdgknr/jgzn/ldxx/xwld/czj/202205/t20220505_889959.html; https://baike.baidu.com/item/唐方春",
    },
    # ── 2. 县长 ──
    {
        "id": 2,
        "name": "邱跃峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "蓬安县人民政府",
        "source": "https://www.pengan.gov.cn/zwgk/fdzdgknr/jgzn/ldxx/xwld/fsj/202211/t20221109_1744227.html",
    },
    # ── 3. 县委专职副书记 ──
    {
        "id": 3,
        "name": "邱时荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共蓬安县委员会",
        "source": "https://www.pengan.gov.cn/zwgk/fdzdgknr/jgzn/ldxx/xwld/fsj/202205/t20220510_1157286.html",
    },
    # ── 4. 常务副县长/县委常委 ──
    {
        "id": 4,
        "name": "蒋鹏程",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "蓬安县人民政府",
        "source": "https://www.pengan.gov.cn/zwgk/fdzdgknr/jgzn/ldxx/xwld/cw/202205/t20220505_889963.html",
    },
    # ── 5. 政法委书记 ──
    {
        "id": 5,
        "name": "陈燕辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共蓬安县委员会",
        "source": "https://www.pengan.gov.cn/zwgk/fdzdgknr/jgzn/ldxx/xwld/cw/202205/t20220510_1157293.html",
    },
    # ── 6. 纪委书记 ──
    {
        "id": 6,
        "name": "刘凯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县纪委书记、监委主任",
        "current_org": "中共蓬安县纪律检查委员会",
        "source": "https://www.pengan.gov.cn/zwgk/fdzdgknr/jgzn/ldxx/xwld/cw/202205/t20220510_1157298.html",
    },
    # ── 7. 宣传部部长 ──
    {
        "id": 7,
        "name": "邓于伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共蓬安县委员会",
        "source": "https://www.pengan.gov.cn/zwgk/fdzdgknr/jgzn/ldxx/xwld/cw/202205/t20220510_1157291.html",
    },
    # ── 8. 人武部部长 ──
    {
        "id": 8,
        "name": "蒲申斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县人武部部长",
        "current_org": "蓬安县人民武装部",
        "source": "https://www.pengan.gov.cn/zwgk/fdzdgknr/jgzn/ldxx/xwld/cw/202205/t20220510_1157300.html",
    },
    # ── 9. 组织部部长 ──
    {
        "id": 9,
        "name": "郭进",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共蓬安县委员会",
        "source": "https://www.pengan.gov.cn/zwgk/fdzdgknr/jgzn/ldxx/xwld/cw/202508/t20250820_2246297.html",
    },
    # ── 10. 统战部部长 ──
    {
        "id": 10,
        "name": "龚红平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、统战部部长",
        "current_org": "中共蓬安县委员会",
        "source": "https://www.pengan.gov.cn/zwgk/fdzdgknr/jgzn/ldxx/xwld/cw/202508/t20250811_2239660.html",
    },
    # ── 11. 总工会主席 ──
    {
        "id": 11,
        "name": "陈雅麒",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县总工会主席",
        "current_org": "蓬安县总工会",
        "source": "https://www.pengan.gov.cn/zwgk/fdzdgknr/jgzn/ldxx/xwld/cw/202205/t20220510_1157299.html",
    },
    # ── 12. 挂职副县长（县委常委） ──
    {
        "id": 12,
        "name": "吴恒",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长（挂职）",
        "current_org": "蓬安县人民政府",
        "source": "https://www.pengan.gov.cn/zwgk/fdzdgknr/jgzn/ldxx/xwld/cw/202512/t20251215_2291971.html",
    },
    # ── 13. 副县长（公安局长） ──
    {
        "id": 13,
        "name": "罗长明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、公安局局长",
        "current_org": "蓬安县公安局",
        "source": "https://www.pengan.gov.cn/zwgk/fdzdgknr/jgzn/ldxx/xzfld/fxz/202205/t20220510_1157312.html",
    },
    # ── 14. 副县长 ──
    {
        "id": 14,
        "name": "邓小燕",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "蓬安县人民政府",
        "source": "https://www.pengan.gov.cn/zwgk/fdzdgknr/jgzn/ldxx/xzfld/fxz/202605/t20260512_2332299.html",
    },
    # ── 15. 副县长 ──
    {
        "id": 15,
        "name": "蒋熙平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "蓬安县人民政府",
        "source": "https://www.pengan.gov.cn/zwgk/fdzdgknr/jgzn/ldxx/xzfld/fxz/202512/t20251215_2291957.html",
    },
    # ── 16. 副县长 ──
    {
        "id": 16,
        "name": "王经纶",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "蓬安县人民政府",
        "source": "https://www.pengan.gov.cn/zwgk/fdzdgknr/jgzn/ldxx/xzfld/fxz/202605/t20260512_2332287.html",
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共蓬安县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共南充市委员会",
        "location": "四川省南充市蓬安县",
    },
    {
        "id": 2,
        "name": "蓬安县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "南充市人民政府",
        "location": "四川省南充市蓬安县",
    },
    {
        "id": 3,
        "name": "中共蓬安县纪律检查委员会",
        "type": "纪律检查",
        "level": "县",
        "parent": "中共南充市纪律检查委员会",
        "location": "四川省南充市蓬安县",
    },
    {
        "id": 4,
        "name": "蓬安县人民武装部",
        "type": "军事",
        "level": "县",
        "parent": "南充军分区",
        "location": "四川省南充市蓬安县",
    },
    {
        "id": 5,
        "name": "蓬安县总工会",
        "type": "群团",
        "level": "县",
        "parent": "南充市总工会",
        "location": "四川省南充市蓬安县",
    },
    {
        "id": 6,
        "name": "蓬安县公安局",
        "type": "政府",
        "level": "县",
        "parent": "蓬安县人民政府",
        "location": "四川省南充市蓬安县",
    },
    {
        "id": 7,
        "name": "蓬安县人大常委会",
        "type": "人大",
        "level": "县",
        "parent": "南充市人大常委会",
        "location": "四川省南充市蓬安县",
    },
    {
        "id": 8,
        "name": "蓬安县政协",
        "type": "政协",
        "level": "县",
        "parent": "南充市政协",
        "location": "四川省南充市蓬安县",
    },
    {
        "id": 9,
        "name": "中共蓬安县委政法委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共蓬安县委员会",
        "location": "四川省南充市蓬安县",
    },
    {
        "id": 10,
        "name": "中共蓬安县委组织部",
        "type": "党委",
        "level": "县",
        "parent": "中共蓬安县委员会",
        "location": "四川省南充市蓬安县",
    },
    {
        "id": 11,
        "name": "中共蓬安县委宣传部",
        "type": "党委",
        "level": "县",
        "parent": "中共蓬安县委员会",
        "location": "四川省南充市蓬安县",
    },
    {
        "id": 12,
        "name": "中共蓬安县委统一战线工作部",
        "type": "党委",
        "level": "县",
        "parent": "中共蓬安县委员会",
        "location": "四川省南充市蓬安县",
    },
]

positions = [
    # 唐方春 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "2022-08", "end": "present", "rank": "正处级", "note": "2022年8月任县委书记，同时任县人武部党委第一书记"},
    {"person_id": 1, "org_id": 1, "title": "县委副书记、县长", "start": "2020-06", "end": "2022-11", "rank": "正处级", "note": "2019.11任代县长，2020.06转正"},
    # 邱跃峰 — 县长
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "2022-11", "end": "", "rank": "正处级", "note": "蓬安县委副书记、县政府县长"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "2022-11", "end": "", "rank": "副厅级", "note": "兼任县长"},
    # 邱时荣 — 专职副书记
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start": "", "end": "", "rank": "", "note": "具体任职开始时间待查"},
    # 蒋鹏程 — 常务副县长
    {"person_id": 4, "org_id": 2, "title": "常务副县长", "start": "", "end": "", "rank": "副处级", "note": "县委常委、县政府党组副书记"},
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start": "", "end": "", "rank": "", "note": "同时担任常务副县长"},
    # 陈燕辉 — 政法委书记
    {"person_id": 5, "org_id": 9, "title": "政法委书记", "start": "", "end": "", "rank": "", "note": "县委常委"},
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start": "", "end": "", "rank": "", "note": ""},
    # 刘凯 — 纪委书记
    {"person_id": 6, "org_id": 3, "title": "县纪委书记、监委主任", "start": "", "end": "", "rank": "", "note": "县委常委"},
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start": "", "end": "", "rank": "", "note": ""},
    # 邓于伟 — 宣传部部长
    {"person_id": 7, "org_id": 11, "title": "宣传部部长", "start": "", "end": "", "rank": "", "note": "县委常委"},
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start": "", "end": "", "rank": "", "note": ""},
    # 蒲申斌 — 人武部部长
    {"person_id": 8, "org_id": 4, "title": "部长", "start": "", "end": "", "rank": "", "note": "县委常委"},
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start": "", "end": "", "rank": "", "note": ""},
    # 郭进 — 组织部部长
    {"person_id": 9, "org_id": 10, "title": "组织部部长", "start": "", "end": "", "rank": "", "note": "县委常委，2025.08上任"},
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start": "2025-08", "end": "", "rank": "", "note": ""},
    # 龚红平 — 统战部部长
    {"person_id": 10, "org_id": 12, "title": "统战部部长", "start": "", "end": "", "rank": "", "note": "县委常委，2025.08上任"},
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start": "2025-08", "end": "", "rank": "", "note": ""},
    # 陈雅麒 — 总工会主席
    {"person_id": 11, "org_id": 5, "title": "主席", "start": "", "end": "", "rank": "", "note": "县委常委"},
    {"person_id": 11, "org_id": 1, "title": "县委常委", "start": "", "end": "", "rank": "", "note": ""},
    # 吴恒 — 挂职副县长
    {"person_id": 12, "org_id": 2, "title": "副县长（挂职）", "start": "2025-12", "end": "", "rank": "", "note": "挂职，同时也为县委常委"},
    {"person_id": 12, "org_id": 1, "title": "县委常委", "start": "2025-12", "end": "", "rank": "", "note": "挂职"},
    # 罗长明 — 副县长/公安局长
    {"person_id": 13, "org_id": 2, "title": "副县长、公安局局长", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 13, "org_id": 6, "title": "公安局局长", "start": "", "end": "", "rank": "", "note": ""},
    # 邓小燕 — 副县长
    {"person_id": 14, "org_id": 2, "title": "副县长", "start": "2026-05", "end": "", "rank": "", "note": ""},
    # 蒋熙平 — 副县长
    {"person_id": 15, "org_id": 2, "title": "副县长", "start": "2025-12", "end": "", "rank": "", "note": ""},
    # 王经纶 — 副县长
    {"person_id": 16, "org_id": 2, "title": "副县长", "start": "2026-05", "end": "", "rank": "", "note": ""},
]

relationships = [
    # 唐方春 ↔ 邱跃峰 — 党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "strength": "strong", "context": "唐方春任县委书记、邱跃峰任县长，党政主要领导工作关系",
     "overlap_org": "蓬安县委/县政府", "overlap_period": "2022.11至今"},
    # 唐方春 ↔ 邱时荣 — 书记与专职副书记
    {"person_a": 1, "person_b": 3, "type": "上下级", "strength": "strong", "context": "县委正副书记配合同",
     "overlap_org": "中共蓬安县委员会", "overlap_period": "2024.07至今"},
    # 邱跃峰 ↔ 邱时荣 — 政府与党委之间
    {"person_a": 2, "person_b": 3, "type": "同级", "strength": "medium", "context": "政府主官与专职副书记", "overlap_org": "蓬安县", "overlap_period": "2024.07至今"},
    # 蒋鹏程 ↔ 唐方春 — 常务副县长与书记
    {"person_a": 4, "person_b": 1, "type": "上下级", "strength": "strong", "context": "常务副县长协助书记处理政府事务",
     "overlap_org": "蓬安县委/县政府", "overlap_period": ""},
    # 蒋鹏程 ↔ 邱跃峰 — 正副县长关系
    {"person_a": 4, "person_b": 2, "type": "上下级", "strength": "strong", "context": "常务副县长协助县长主持政府日常工作",
     "overlap_org": "蓬安县人民政府", "overlap_period": ""},
    # 刘凯 ↔ 唐方春 — 纪委书记与书记
    {"person_a": 6, "person_b": 1, "type": "上下级", "strength": "strong", "context": "纪委书记向县委书记负责",
     "overlap_org": "蓬安县委", "overlap_period": ""},
    # 郭进 ↔ 唐方春 — 组织部长与书记
    {"person_a": 9, "person_b": 1, "type": "上下级", "strength": "strong", "context": "组织部部长向县委书记报告干部工作",
     "overlap_org": "中共蓬安县委员会", "overlap_period": "2025.08至今"},
    # 陈燕辉 ↔ 罗长明 — 政法委与公安
    {"person_a": 5, "person_b": 13, "type": "工作关系", "strength": "medium", "context": "政法委书记与公安局局长在维稳、政法方面密切合作",
     "overlap_org": "蓬安县政法系统", "overlap_period": ""},
]


# ═══════════════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════════════

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def build_sqlite():
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS relationships")
    cur.execute("DROP TABLE IF EXISTS positions")
    cur.execute("DROP TABLE IF EXISTS organizations")
    cur.execute("DROP TABLE IF EXISTS persons")

    cur.execute("""
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, native_place TEXT, education TEXT,
            party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT, source TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER,
            title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)
    cur.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER,
            type TEXT, strength TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT
        )
    """)

    for p in persons:
        cur.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, native_place,
            education, party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"], p.get("native_place", ""),
              p["education"], p["party_join"], p.get("work_start", ""), p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        cur.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)
        """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        cur.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)
        """, (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        cur.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?,?,?,?,?,?)
        """, (r["person_a"], r["person_b"], r["type"], r["context"], r.get("overlap_org", ""), r.get("overlap_period", "")))

    conn.commit()

    print(f"Database: {DB_PATH}")
    print(f"  Persons: {cur.execute('SELECT COUNT(*) FROM persons').fetchone()[0]}")
    print(f"  Orgs:    {cur.execute('SELECT COUNT(*) FROM organizations').fetchone()[0]}")
    print(f"  Posit:   {cur.execute('SELECT COUNT(*) FROM positions').fetchone()[0]}")
    print(f"  Rels:    {cur.execute('SELECT COUNT(*) FROM relationships').fetchone()[0]}")

    conn.close()


def build_gexf():
    from datetime import datetime as dt

    def is_top_leader(name):
        return name in ("唐方春", "邱跃峰")

    def person_color(p):
        if p["current_post"] and "县委书记" in p["current_post"]:
            return "255,50,50"
        if p["current_post"] and "县长" in p["current_post"]:
            return "50,100,255"
        if p["current_post"] and "纪委书记" in p["current_post"]:
            return "255,165,0"
        return "100,100,100"

    def org_color(o):
        type_map = {
            "党委": "255,200,200",
            "政府": "200,200,255",
            "纪律检查": "255,200,200",
            "人大": "200,255,255",
            "政协": "255,240,200",
            "群团": "255,220,255",
            "军事": "200,200,200",
        }
        return type_map.get(o["type"], "200,200,200")

    def org_type_label(t):
        mapping = {"党委": "party_committee", "政府": "government", "纪律检查": "discipline",
                    "人大": "npc", "政协": "cppcc", "群团": "mass_org", "军事": "military"}
        return mapping.get(t, "other")

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{dt.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append(f'    <description>{SLUG} leadership network</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org_type" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('    </attributes>')

    # nodes - persons
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p["name"]) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # nodes - orgs
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="2" value="{org_type_label(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # edges
    eid = 0
    lines.append('    <edges>')
    # person -> org
    for pos in positions:
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1
    # person -> person
    for r in relationships:
        w = "2.0"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"✅ GEXF: {GEXF_PATH}")
    print(f"  Nodes: {len(persons) + len(organizations)}, Edges: {eid}")


if __name__ == "__main__":
    print(f"Building {SLUG} network data...")
    build_sqlite()
    build_gexf()
    print("Done.")