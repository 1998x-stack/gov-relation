#!/usr/bin/env python3
"""Build 威信县 (Weixin County) 领导班子工作关系网络.

云南省昭通市下辖县. 数据来源: 威信县人民政府网站 (weixin.gov.cn), 百度百科.
调查日期: 2026-07-28.
"""

import sqlite3
from pathlib import Path

# ── Metadata ─────────────────────────────────────────────────────────────
SLUG = "威信县"
TODAY = "2026-07-28"
PROVINCE = "云南省"
CITY = "昭通市"

# ── Paths ────────────────────────────────────────────────────────────────
BASE = Path(__file__).resolve().parent
DB_PATH = BASE / f"{SLUG}_network.db"
GEXF_PATH = BASE / f"{SLUG}_network.gexf"
REPORT_PATH = BASE / f"{TODAY}-{PROVINCE}-{CITY}-{SLUG}-领导班子调查报告.md"

# ── Data: Persons ────────────────────────────────────────────────────────
# id: unique int per person
persons = [
    # -- 县委常委 --
    {
        "id": 1,
        "name": "陇俊伟",
        "gender": "男",
        "ethnicity": "彝族",
        "birth": "1983年8月",
        "birthplace": "云南镇雄",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "2004年6月",
        "current_post": "县委书记",
        "current_org": "中共威信县委",
        "source": "https://baike.baidu.com/item/%E9%99%87%E4%BF%8A%E4%BC%9F",
    },
    {
        "id": 2,
        "name": "赵红",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1980年9月",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "威信县人民政府",
        "source": "https://www.weixin.gov.cn/contents/5700/12607.html",
    },
    {
        "id": 3,
        "name": "曾武红",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共威信县委",
        "source": "https://www.weixin.gov.cn/contents/5569/34115.html",
    },
    {
        "id": 4,
        "name": "康伟",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共威信县委",
        "source": "https://www.weixin.gov.cn/contents/5569/34115.html",
    },
    {
        "id": 5,
        "name": "熊良纯",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "威信县人民政府",
        "source": "https://www.weixin.gov.cn/contents/5701/20388.html",
    },
    {
        "id": 6,
        "name": "田井东",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共威信县委",
        "source": "https://www.weixin.gov.cn/contents/5569/34115.html",
    },
    {
        "id": 7,
        "name": "方成仲",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共威信县委",
        "source": "https://www.weixin.gov.cn/contents/5569/34115.html",
    },
    {
        "id": 8,
        "name": "朱相海",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共威信县委",
        "source": "https://www.weixin.gov.cn/contents/5569/34115.html",
    },
    {
        "id": 9,
        "name": "庄文峰",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "威信县人民政府",
        "source": "https://www.weixin.gov.cn/contents/5701/30820.html",
    },
    {
        "id": 10,
        "name": "芦阳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "威信县人民政府",
        "source": "https://www.weixin.gov.cn/contents/5701/20393.html",
    },
    {
        "id": 11,
        "name": "吴淑荣",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共威信县委",
        "source": "https://www.weixin.gov.cn/contents/5569/34115.html",
    },
    {
        "id": 12,
        "name": "周小平",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县监委副主任",
        "current_org": "威信县监察委员会",
        "source": "https://www.weixin.gov.cn/contents/5569/33921.html",
    },
    # -- 县政府领导 --
    {
        "id": 13,
        "name": "袁昊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年2月",
        "birthplace": "云南彝良",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "2006年",
        "current_post": "副县长",
        "current_org": "威信县人民政府",
        "source": "https://www.weixin.gov.cn/contents/5701/23333.html",
    },
    {
        "id": 14,
        "name": "双家祥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年1月",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、公安局长",
        "current_org": "威信县公安局",
        "source": "https://www.weixin.gov.cn/contents/5701/20390.html",
    },
    {
        "id": 15,
        "name": "陈宇",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "威信县人民政府",
        "source": "https://www.weixin.gov.cn/contents/5701/20392.html",
    },
    {
        "id": 16,
        "name": "马正宇",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "威信县人民政府",
        "source": "https://www.weixin.gov.cn/contents/5701/33902.html",
    },
    {
        "id": 17,
        "name": "罗迅",
        "gender": "男",
        "ethnicity": "白族",
        "birth": "1990年",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "威信县人民政府",
        "source": "https://www.weixin.gov.cn/contents/5701/33832.html",
    },
    {
        "id": 18,
        "name": "王宗刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "四级调研员",
        "current_org": "威信县人民政府",
        "source": "https://www.weixin.gov.cn/contents/5701/20391.html",
    },
    # -- 人大政协 --
    {
        "id": 19,
        "name": "叶昌书",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "威信县人大常委会",
        "source": "https://www.weixin.gov.cn/contents/5569/34115.html",
    },
    {
        "id": 20,
        "name": "陶勇",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "政协威信县委员会",
        "source": "https://www.weixin.gov.cn/contents/5569/34115.html",
    },
    {
        "id": 21,
        "name": "张祖林",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县监察委员会主任",
        "current_org": "威信县监察委员会",
        "source": "https://www.weixin.gov.cn/contents/5569/33921.html",
    },
]

# ── Data: Organizations ──────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共威信县委", "type": "党委", "level": "县", "parent": "中共昭通市委", "location": "威信县"},
    {"id": 2, "name": "威信县人民政府", "type": "政府", "level": "县", "parent": "昭通市人民政府", "location": "威信县"},
    {"id": 3, "name": "威信县人大常委会", "type": "人大", "level": "县", "parent": "", "location": "威信县"},
    {"id": 4, "name": "政协威信县委员会", "type": "政协", "level": "县", "parent": "", "location": "威信县"},
    {"id": 5, "name": "威信县监察委员会", "type": "纪委", "level": "县", "parent": "", "location": "威信县"},
    {"id": 6, "name": "威信县公安局", "type": "政法机关", "level": "县", "parent": "威信县人民政府", "location": "威信县"},
]

# ── Data: Positions (person_id, org_id, title, start, end, rank, note) ───
positions = [
    # 陇俊伟
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "2026-05", "end_date": "", "rank": "正处级", "note": "2026年5月27日任，6月28日党代会当选"},
    {"person_id": 1, "org_id": 1, "title": "县人武部党委第一书记", "start_date": "2026-06", "end_date": "", "rank": "", "note": "2026年6月12日任职"},
    # 赵红
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "", "end_date": "", "rank": "正处级", "note": "县政府党组书记"},
    # 曾武红
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "", "rank": "副处级", "note": "第十四届留任"},
    # 康伟
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 熊良纯
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "常务副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 田井东
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 方成仲
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 朱相海
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 庄文峰
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "协助乡村振兴"},
    # 芦阳
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "协助乡村振兴"},
    # 吴淑荣
    {"person_id": 11, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 周小平
    {"person_id": 12, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 5, "title": "县监委副主任", "start_date": "2026-06", "end_date": "", "rank": "副处级", "note": ""},
    # 袁昊
    {"person_id": 13, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 双家祥
    {"person_id": 14, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 6, "title": "公安局长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 陈宇
    {"person_id": 15, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 马正宇
    {"person_id": 16, "org_id": 2, "title": "副县长", "start_date": "2026-06", "end_date": "", "rank": "副处级", "note": "2026年6月30日任命"},
    # 罗迅
    {"person_id": 17, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 王宗刚
    {"person_id": 18, "org_id": 2, "title": "四级调研员", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 叶昌书
    {"person_id": 19, "org_id": 3, "title": "县人大常委会主任", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    # 陶勇
    {"person_id": 20, "org_id": 4, "title": "县政协主席", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    # 张祖林
    {"person_id": 21, "org_id": 5, "title": "县监察委员会主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
]

# ── Data: Relationships (person_a, person_b, type, context, overlap_org, overlap_period) ──
relationships = [
    # 县委常委会同僚关系
    {"person_a": 1, "person_b": 2, "type": "党政同僚", "context": "党政一把手搭档", "overlap_org": "威信县委/县政府", "overlap_period": "2026-05至今"},
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "书记与副书记", "overlap_org": "威信县委", "overlap_period": "2026-06至今"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "书记与常务副县长", "overlap_org": "威信县委", "overlap_period": "2026-06至今"},
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "县长与常务副县长", "overlap_org": "威信县政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 3, "type": "同僚", "context": "县长与副书记", "overlap_org": "威信县委", "overlap_period": ""},
    # 副县长同僚关系
    {"person_a": 13, "person_b": 14, "type": "同僚", "context": "副县长同僚", "overlap_org": "威信县政府", "overlap_period": ""},
    {"person_a": 13, "person_b": 15, "type": "同僚", "context": "副县长同僚", "overlap_org": "威信县政府", "overlap_period": ""},
    {"person_a": 13, "person_b": 17, "type": "同僚", "context": "副县长同僚", "overlap_org": "威信县政府", "overlap_period": ""},
    {"person_a": 14, "person_b": 17, "type": "同僚", "context": "副县长同僚", "overlap_org": "威信县政府", "overlap_period": ""},
    {"person_a": 15, "person_b": 17, "type": "同僚", "context": "副县长同僚", "overlap_org": "威信县政府", "overlap_period": ""},
    # 人大政协
    {"person_a": 19, "person_b": 20, "type": "同僚", "context": "人大主任与政协主席", "overlap_org": "威信县", "overlap_period": ""},
    # 纪监委
    {"person_a": 12, "person_b": 21, "type": "上下级", "context": "监委副主任与监委主任", "overlap_org": "威信县监察委员会", "overlap_period": "2026-06至今"},
    # 挂职副县长与帮扶
    {"person_a": 9, "person_b": 17, "type": "同僚", "context": "挂职副县长协助乡村振兴", "overlap_org": "威信县政府", "overlap_period": ""},
    {"person_a": 10, "person_b": 17, "type": "同僚", "context": "挂职副县长协助乡村振兴", "overlap_org": "威信县政府", "overlap_period": ""},
]


# ═══════════════════════════════════════════════════════════════════════
# BUILD FUNCTIONS
# ═══════════════════════════════════════════════════════════════════════

def create_tables(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT DEFAULT '',
            ethnicity TEXT DEFAULT '',
            birth TEXT DEFAULT '',
            birthplace TEXT DEFAULT '',
            education TEXT DEFAULT '',
            party_join TEXT DEFAULT '',
            work_start TEXT DEFAULT '',
            current_post TEXT DEFAULT '',
            current_org TEXT DEFAULT '',
            source TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT DEFAULT '',
            start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '',
            note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER NOT NULL,
            person_b INTEGER NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)
    conn.commit()


def run_build():
    print("=" * 60)
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  等级: 县")
    print(f"  调查日期: {TODAY}")
    print(f"  信息来源: 威信县人民政府网站 (weixin.gov.cn)")
    print("=" * 60)

    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)

    # Insert persons
    cols_p = ["id","name","gender","ethnicity","birth","birthplace","education",
              "party_join","work_start","current_post","current_org","source"]
    for p in persons:
        vals = [p.get(c,"") for c in cols_p]
        conn.execute(f"INSERT INTO persons ({','.join(cols_p)}) VALUES ({','.join(['?']*len(cols_p))})", vals)

    # Insert organizations
    cols_o = ["id","name","type","level","parent","location"]
    for o in organizations:
        vals = [o.get(c,"") for c in cols_o]
        conn.execute(f"INSERT INTO organizations ({','.join(cols_o)}) VALUES ({','.join(['?']*len(cols_o))})", vals)

    # Insert positions
    cols_pos = ["person_id","org_id","title","start_date","end_date","rank","note"]
    for pos in positions:
        vals = [pos.get(c,"") for c in cols_pos]
        conn.execute(f"INSERT INTO positions ({','.join(cols_pos)}) VALUES ({','.join(['?']*len(cols_pos))})", vals)

    # Insert relationships
    cols_r = ["person_a","person_b","type","context","overlap_org","overlap_period"]
    for r in relationships:
        vals = [r.get(c,"") for c in cols_r]
        conn.execute(f"INSERT INTO relationships ({','.join(cols_r)}) VALUES ({','.join(['?']*len(cols_r))})", vals)

    conn.commit()
    conn.close()

    print(f"\n  DB: {DB_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

    # ── GEXF ──────────────────────────────────────────────────────
    print("\n--- Building GEXF graph ---")

    def esc(s):
        if s is None: return ""
        return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

    def person_color(post):
        if "县委书记" in post and "副书记" not in post:
            return ("255,50,50", 20.0)
        elif "县长" in post and "副书记" in post:
            return ("50,100,255", 20.0)
        elif "常务" in post:
            return ("50,100,255", 15.0)
        elif "副书记" in post:
            return ("50,100,255", 14.0)
        elif "副县长" in post or "常委" in post:
            return ("100,100,255", 12.0)
        elif "人大主任" in post:
            return ("200,255,255", 15.0)
        elif "政协主席" in post:
            return ("200,255,200", 15.0)
        elif "监委" in post:
            return ("255,180,50", 12.0)
        elif "公安" in post:
            return ("100,150,255", 12.0)
        elif "调研员" in post:
            return ("150,150,150", 10.0)
        else:
            return ("100,100,100", 12.0)

    def org_color(typ):
        return {
            "党委": ("255,200,200"),
            "政府": ("200,200,255"),
            "人大": ("200,255,255"),
            "政协": ("200,255,200"),
            "纪委": ("255,200,100"),
            "政法机关": ("200,200,200"),
        }.get(typ, ("200,200,200"))

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">',
        f'  <meta lastmodifieddate="{TODAY}">',
        '    <creator>Gov-Relation Research Agent</creator>',
        f'    <description>{SLUG} 领导班子关系网络</description>',
        '  </meta>',
        '  <graph mode="static" defaultedgetype="undirected">',
        '    <attributes class="node">',
        '      <attribute id="0" title="type" type="string"/>',
        '      <attribute id="1" title="current_post" type="string"/>',
        '      <attribute id="2" title="current_org" type="string"/>',
        '      <attribute id="3" title="birth" type="string"/>',
        '      <attribute id="4" title="source" type="string"/>',
        '    </attributes>',
        '    <attributes class="edge">',
        '      <attribute id="0" title="type" type="string"/>',
        '      <attribute id="1" title="context" type="string"/>',
        '      <attribute id="2" title="overlap_org" type="string"/>',
        '      <attribute id="3" title="overlap_period" type="string"/>',
        '    </attributes>',
        '    <nodes>',
    ]

    for p in persons:
        c, sz = person_color(p["current_post"])
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
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
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

    print(f"  GEXF: {GEXF_PATH}")
    print(f"  节点: {len(persons) + len(organizations)} 个")
    print(f"  边: {eid} 条")
    print(f"\n✅ {SLUG} 数据构建完成。")


if __name__ == "__main__":
    run_build()
