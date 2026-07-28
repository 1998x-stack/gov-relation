#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 布拖县 leadership network."""

import sqlite3
import os
from datetime import datetime

# ── PATHS ─────────────────────────────────────────────────────────
STAGING = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.abspath(os.path.join(STAGING, "..", ".."))
DB_PATH = os.path.join(STAGING, "布拖县_network.db")
GEXF_PATH = os.path.join(STAGING, "布拖县_network.gexf")
SLUG = "布拖县"
TODAY = datetime.now().strftime("%Y-%m-%d")

# ── PERSONS ───────────────────────────────────────────────────────
persons = [
    # ── Current Top Leaders ──
    {
        "id": 1, "name": "李剑", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共布拖县委员会",
        "source": "https://www.bt.gov.cn/zfxxgk/zfxxgknr/gbrm/202304/t20230418_2469853.html"
    },
    {
        "id": 2, "name": "邓兴伟", "gender": "男", "ethnicity": "汉族",
        "birth": "1975-11", "birthplace": "", "education": "本科",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "布拖县人民政府",
        "source": "https://www.bt.gov.cn/zfxxgk/zfxxgknr/zfld/202403/t20240312_2644464.html"
    },
    # ── Predecessors ──
    {
        "id": 3, "name": "罗古阿吉", "gender": "男", "ethnicity": "彝族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "前任县委书记",
        "current_org": "中共布拖县委员会(前任)",
        "source": "https://www.bt.gov.cn/zfxxgk/zfxxgknr/gbrm/202107/t20210713_1962525.html"
    },
    {
        "id": 4, "name": "沙文", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "前任县委书记",
        "current_org": "中共布拖县委员会(前任)",
        "source": "https://www.bt.gov.cn/zfxxgk/zfxxgknr/gbrm/202107/t20210713_1962525.html"
    },
    # ── Key Deputies: Party Committee (Standing) ──
    {
        "id": 5, "name": "付开文", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共布拖县委员会",
        "source": "https://www.bt.gov.cn/btxw/jrbt/202605/t20260514_2981065.html"
    },
    {
        "id": 6, "name": "的日阿体", "gender": "男", "ethnicity": "彝族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共布拖县委员会",
        "source": "https://www.bt.gov.cn/btxw/jrbt/202607/t20260715_3001505.html"
    },
    # ── County Government Leaders ──
    {
        "id": 7, "name": "刘国安", "gender": "男", "ethnicity": "彝族",
        "birth": "1979-06", "birthplace": "", "education": "本科",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "布拖县人民政府",
        "source": "https://www.bt.gov.cn/zfxxgk/zfxxgknr/zfld/202403/t20240312_2644465.html"
    },
    {
        "id": 8, "name": "杨少贵", "gender": "男", "ethnicity": "汉族",
        "birth": "1982-07", "birthplace": "", "education": "中国农业大学农业推广硕士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "布拖县人民政府",
        "source": "https://www.bt.gov.cn/zfxxgk/zfxxgknr/zfld/202403/t20240312_2644481.html"
    },
    {
        "id": 9, "name": "高露", "gender": "男", "ethnicity": "汉族",
        "birth": "1980-10", "birthplace": "", "education": "工程硕士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委、副县长（挂职）",
        "current_org": "布拖县人民政府",
        "source": "https://www.bt.gov.cn/zfxxgk/zfxxgknr/zfld/202403/t20240312_2644474.html"
    },
    {
        "id": 10, "name": "黄河", "gender": "男", "ethnicity": "汉族",
        "birth": "1971-05", "birthplace": "", "education": "本科",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "布拖县人民政府",
        "source": "https://www.bt.gov.cn/zfxxgk/zfxxgknr/zfld/202510/t20251013_2892891.html"
    },
    {
        "id": 11, "name": "付华", "gender": "男", "ethnicity": "汉族",
        "birth": "1983-05", "birthplace": "", "education": "本科",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委、副县长（挂职）",
        "current_org": "布拖县人民政府",
        "source": "https://www.bt.gov.cn/zfxxgk/zfxxgknr/zfld/202403/t20240313_2645583.html"
    },
    {
        "id": 12, "name": "王敏", "gender": "女", "ethnicity": "彝族",
        "birth": "1979-08", "birthplace": "", "education": "在职大专",
        "party_join": "无党派人士", "work_start": "",
        "current_post": "副县长",
        "current_org": "布拖县人民政府",
        "source": "https://www.bt.gov.cn/zfxxgk/zfxxgknr/zfld/202403/t20240312_2644486.html"
    },
    {
        "id": 13, "name": "吉康", "gender": "男", "ethnicity": "彝族",
        "birth": "1985-12", "birthplace": "", "education": "本科",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副县长",
        "current_org": "布拖县人民政府",
        "source": "https://www.bt.gov.cn/zfxxgk/zfxxgknr/zfld/202403/t20240312_2644489.html"
    },
    {
        "id": 14, "name": "日黑此哈", "gender": "男", "ethnicity": "彝族",
        "birth": "1978-10", "birthplace": "", "education": "四川省委党校行政管理大专",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副县长",
        "current_org": "布拖县人民政府",
        "source": "https://www.bt.gov.cn/zfxxgk/zfxxgknr/zfld/202410/t20241015_2741441.html"
    },
    {
        "id": 15, "name": "张泽华", "gender": "男", "ethnicity": "彝族",
        "birth": "1983-09", "birthplace": "", "education": "党校研究生",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副县长",
        "current_org": "布拖县人民政府",
        "source": "https://www.bt.gov.cn/zfxxgk/zfxxgknr/zfld/202403/t20240312_2644498.html"
    },
    {
        "id": 16, "name": "苏军", "gender": "男", "ethnicity": "彝族",
        "birth": "1976-09", "birthplace": "", "education": "本科",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副县长、县公安局局长",
        "current_org": "布拖县人民政府",
        "source": "https://www.bt.gov.cn/zfxxgk/zfxxgknr/zfld/202403/t20240312_2644507.html"
    },
    {
        "id": 17, "name": "赵建忠", "gender": "男", "ethnicity": "汉族",
        "birth": "1979-07", "birthplace": "", "education": "西昌学院行政管理在职大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副县长",
        "current_org": "布拖县人民政府",
        "source": "https://www.bt.gov.cn/zfxxgk/zfxxgknr/zfld/202506/t20250612_2844370.html"
    },
    {
        "id": 18, "name": "陈友兴", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县领导",
        "current_org": "布拖县人民政府",
        "source": "https://www.bt.gov.cn/btxw/jrbt/202607/t20260708_2999317.html"
    },
    # ── 人大, 政协, 法检 ──
    {
        "id": 19, "name": "吉地你聪", "gender": "男", "ethnicity": "彝族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "布拖县人大常委会",
        "source": "https://www.bt.gov.cn/btxw/jrbt/202605/t20260514_2981065.html"
    },
    {
        "id": 20, "name": "黄西虎", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县政协主席",
        "current_org": "布拖县政协",
        "source": "https://www.bt.gov.cn/btxw/jrbt/202605/t20260514_2981065.html"
    },
    {
        "id": 21, "name": "阿加拉铁", "gender": "男", "ethnicity": "彝族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县人民法院院长",
        "current_org": "布拖县人民法院",
        "source": "https://www.bt.gov.cn/btxw/jrbt/202605/t20260514_2981065.html"
    },
    {
        "id": 22, "name": "潘志伟", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县人民检察院检察长",
        "current_org": "布拖县人民检察院",
        "source": "https://www.bt.gov.cn/btxw/jrbt/202605/t20260514_2981065.html"
    },
]

# ── ORGANIZATIONS ────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共布拖县委员会", "type": "党委", "level": "县", "parent": "凉山彝族自治州委", "location": "四川省凉山州布拖县"},
    {"id": 2, "name": "布拖县人民政府", "type": "政府", "level": "县", "parent": "凉山彝族自治州人民政府", "location": "四川省凉山州布拖县"},
    {"id": 3, "name": "布拖县人大常委会", "type": "人大", "level": "县", "parent": "凉山州人大常委会", "location": "四川省凉山州布拖县"},
    {"id": 4, "name": "布拖县政协", "type": "政协", "level": "县", "parent": "凉山州政协", "location": "四川省凉山州布拖县"},
    {"id": 5, "name": "布拖县人民法院", "type": "政府", "level": "县", "parent": "凉山州中级人民法院", "location": "四川省凉山州布拖县"},
    {"id": 6, "name": "布拖县人民检察院", "type": "政府", "level": "县", "parent": "凉山州人民检察院", "location": "四川省凉山州布拖县"},
    {"id": 7, "name": "布拖县公安局", "type": "政府", "level": "县", "parent": "布拖县人民政府", "location": "四川省凉山州布拖县"},
]

# ── POSITIONS ───────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "2023-04", "end_date": "现任", "rank": "正处级", "note": "2023年4月12日任布拖县委书记"},
    {"person_id": 2, "org_id": 2, "title": "县委副书记、县长", "start_date": "", "end_date": "现任", "rank": "正处级", "note": "主持县政府全面工作"},
    {"person_id": 3, "org_id": 1, "title": "前任县委书记", "start_date": "2021-07", "end_date": "2023-04", "rank": "正处级", "note": "2021年7月至2023年4月任布拖县委书记"},
    {"person_id": 4, "org_id": 1, "title": "前任县委书记", "start_date": "", "end_date": "2021-07", "rank": "正处级", "note": "免职于2021年7月"},
    {"person_id": 5, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "现任", "rank": "副处级", "note": "县委副书记"},
    {"person_id": 6, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "现任", "rank": "副处级", "note": "县委副书记"},
    {"person_id": 7, "org_id": 2, "title": "县委常委、常务副县长", "start_date": "", "end_date": "现任", "rank": "副处级", "note": "负责政府常务工作"},
    {"person_id": 8, "org_id": 2, "title": "县委常委、副县长", "start_date": "", "end_date": "现任", "rank": "副处级", "note": "负责水利、林业、森林草原防灭火"},
    {"person_id": 9, "org_id": 2, "title": "县委常委、副县长（挂职）", "start_date": "", "end_date": "现任", "rank": "副处级", "note": "东西部协作挂职"},
    {"person_id": 10, "org_id": 2, "title": "县委常委、副县长", "start_date": "", "end_date": "现任", "rank": "副处级", "note": "建行四川省分行托底性帮扶"},
    {"person_id": 11, "org_id": 2, "title": "县委常委、副县长（挂职）", "start_date": "", "end_date": "现任", "rank": "副处级", "note": "央企定点帮扶挂职"},
    {"person_id": 12, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "现任", "rank": "副处级", "note": "负责民族宗教、民政、退役军人事务"},
    {"person_id": 13, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "现任", "rank": "副处级", "note": "负责农业农村、市场监管、水利"},
    {"person_id": 14, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "现任", "rank": "副处级", "note": "负责文化广电旅游、市场监管"},
    {"person_id": 15, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "现任", "rank": "副处级", "note": "负责教育体育、卫健、林业草原"},
    {"person_id": 16, "org_id": 2, "title": "副县长、县公安局局长", "start_date": "", "end_date": "现任", "rank": "副处级", "note": "负责公安、司法、禁毒信访"},
    {"person_id": 16, "org_id": 7, "title": "县公安局局长", "start_date": "", "end_date": "现任", "rank": "正科级", "note": "一级警长"},
    {"person_id": 17, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "现任", "rank": "副处级", "note": "负责自然资源、交通、环保"},
    {"person_id": 18, "org_id": 2, "title": "县领导", "start_date": "", "end_date": "现任", "rank": "", "note": "参加调研活动"},
    {"person_id": 19, "org_id": 3, "title": "县人大常委会主任", "start_date": "", "end_date": "现任", "rank": "正处级", "note": "主持人大工作"},
    {"person_id": 20, "org_id": 4, "title": "县政协主席", "start_date": "", "end_date": "现任", "rank": "正处级", "note": "主持政协工作"},
    {"person_id": 21, "org_id": 5, "title": "县人民法院院长", "start_date": "", "end_date": "现任", "rank": "副处级", "note": "法院工作报告"},
    {"person_id": 22, "org_id": 6, "title": "县人民检察院检察长", "start_date": "", "end_date": "现任", "rank": "副处级", "note": "检察院工作报告"},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "县委书记与县长搭档工作", "overlap_org": "布拖县委/县政府", "overlap_period": "2023-04至今"},
    {"person_a": 1, "person_b": 3, "type": "前任继任", "context": "李剑接替罗古阿吉任县委书记", "overlap_org": "中共布拖县委员会", "overlap_period": "2023-04"},
    {"person_a": 3, "person_b": 4, "type": "前任继任", "context": "罗古阿吉接替沙文任县委书记", "overlap_org": "中共布拖县委员会", "overlap_period": "2021-07"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "李剑与付开文为书记和副书记关系", "overlap_org": "布拖县委", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "李剑与的日阿体为书记和副书记关系", "overlap_org": "布拖县委", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "县长和常务副县长工作关系", "overlap_org": "布拖县政府", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 7, "type": "领导班子", "context": "县委常委会同班", "overlap_org": "布拖县领导班子", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 8, "type": "领导班子", "context": "县委常委会同班", "overlap_org": "布拖县领导班子", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 9, "type": "领导班子", "context": "县委常委会同班", "overlap_org": "布拖县领导班子", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 10, "type": "领导班子", "context": "县委常委会同班", "overlap_org": "布拖县领导班子", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 11, "type": "领导班子", "context": "县委常委会同班", "overlap_org": "布拖县领导班子", "overlap_period": "现任"},
    {"person_a": 5, "person_b": 6, "type": "同级", "context": "同为县委副书记", "overlap_org": "布拖县委", "overlap_period": "现任"},
    {"person_a": 7, "person_b": 8, "type": "领导班子", "context": "同为县委常委和政府领导", "overlap_org": "布拖县政府", "overlap_period": "现任"},
    {"person_a": 7, "person_b": 12, "type": "领导班子", "context": "常务副县长和副县长工作关系", "overlap_org": "布拖县政府", "overlap_period": "现任"},
    {"person_a": 7, "person_b": 13, "type": "领导班子", "context": "常务副县长和副县长工作关系", "overlap_org": "布拖县政府", "overlap_period": "现任"},
    {"person_a": 7, "person_b": 14, "type": "领导班子", "context": "常务副县长和副县长工作关系", "overlap_org": "布拖县政府", "overlap_period": "现任"},
    {"person_a": 7, "person_b": 15, "type": "领导班子", "context": "常务副县长和副县长工作关系", "overlap_org": "布拖县政府", "overlap_period": "现任"},
    {"person_a": 7, "person_b": 16, "type": "领导班子", "context": "常务副县长和副县长工作关系", "overlap_org": "布拖县政府", "overlap_period": "现任"},
    {"person_a": 7, "person_b": 17, "type": "领导班子", "context": "常务副县长和副县长工作关系", "overlap_org": "布拖县政府", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 19, "type": "党政军领导", "context": "县委书记和人大主任同班", "overlap_org": "布拖县四套班子", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 20, "type": "党政军领导", "context": "县委书记和政协主席同班", "overlap_org": "布拖县四套班子", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 21, "type": "党政军领导", "context": "县委书记和法院院长", "overlap_org": "布拖县", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 22, "type": "党政军领导", "context": "县委书记和检察院检察长", "overlap_org": "布拖县", "overlap_period": "现任"},
]


# ===== MAIN =====
def main():
    print("=" * 60)
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  等级: 县")
    print(f"  调查日期: {TODAY}")
    print(f"  信息来源: 布拖县人民政府网站 (bt.gov.cn)")
    print("=" * 60)

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("DROP TABLE IF EXISTS relationships")
    conn.execute("DROP TABLE IF EXISTS positions")
    conn.execute("DROP TABLE IF EXISTS organizations")
    conn.execute("DROP TABLE IF EXISTS persons")

    conn.execute("""
        CREATE TABLE persons(
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, education TEXT,
            party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT,
            source TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE organizations(
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE positions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER,
            title TEXT, start TEXT, end TEXT,
            rank TEXT, note TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE relationships(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT
        )
    """)

    cols_p = ["id","name","gender","ethnicity","birth","birthplace","education",
              "party_join","work_start","current_post","current_org","source"]
    for p in persons:
        vals = [p.get(c, "") for c in cols_p]
        conn.execute(f"INSERT INTO persons ({','.join(cols_p)}) VALUES ({','.join(['?']*len(cols_p))})", vals)

    cols_o = ["id","name","type","level","parent","location"]
    for o in organizations:
        vals = [o.get(c, "") for c in cols_o]
        conn.execute(f"INSERT INTO organizations ({','.join(cols_o)}) VALUES ({','.join(['?']*len(cols_o))})", vals)

    cols_pos = ["person_id","org_id","title","start","end","rank","note"]
    for pos in positions:
        vals = [pos.get(c, "") for c in cols_pos]
        conn.execute(f"INSERT INTO positions ({','.join(cols_pos)}) VALUES ({','.join(['?']*len(cols_pos))})", vals)

    cols_r = ["person_a","person_b","type","context","overlap_org","overlap_period"]
    for r in relationships:
        vals = [r.get(c, "") for c in cols_r]
        conn.execute(f"INSERT INTO relationships ({','.join(cols_r)}) VALUES ({','.join(['?']*len(cols_r))})", vals)

    conn.commit()
    conn.close()

    print(f"\n  DB: {DB_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

    # ── GEXF ──
    print("\n--- Building GEXF graph ---")

    def esc(s):
        if s is None: return ""
        return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

    def person_color_and_size(post):
        if "县委书记" in post and "前任" not in post:
            return ("255,50,50", 20.0)
        elif "县长" in post and "副" not in post and "前任" not in post:
            return ("50,100,255", 20.0)
        elif "县委副书记" in post:
            return ("150,50,50", 15.0)
        elif "县政协主席" in post:
            return ("255,240,200", 15.0)
        elif "县人大常委会主任" in post:
            return ("200,255,255", 15.0)
        elif "纪委书记" in post:
            return ("255,165,0", 12.0)
        elif "县委常委" in post:
            return ("100,150,255", 12.0)
        elif "副县长" in post or "副县长" in post:
            return ("100,100,255", 12.0)
        elif "检察长" in post or "法院院长" in post:
            return ("150,150,255", 12.0)
        elif "前任" in post:
            return ("150,150,150", 10.0)
        elif "县领导" in post:
            return ("100,150,100", 12.0)
        else:
            return ("100,100,100", 12.0)

    def org_color(typ):
        return {
            "党委": ("255,200,200"),
            "政府": ("200,200,255"),
            "人大": ("200,255,255"),
            "政协": ("255,240,200"),
        }.get(typ, ("200,200,200"))

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append(f'    <description>{SLUG} 领导班子关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="source" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <nodes>')

    for p in persons:
        c, sz = person_color_and_size(p["current_post"])
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p["source"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')
    lines.append('    <edges>')

    eid = 0
    for pos in positions:
        eid += 1
        lines.append(
            f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" '
            f'label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        lines.append(
            f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" '
            f'label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    persons_node_count = len(persons)
    orgs_node_count = len(organizations)
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  节点: {persons_node_count + orgs_node_count} 个")
    print(f"  边: {eid} 条")
    print(f"\n✅ {SLUG} 数据构建完成。")


if __name__ == "__main__":
    main()