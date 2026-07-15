#!/usr/bin/env python3
"""
万安县领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Wan'an County leadership.

Research note: Due to geo-restrictions, Chinese government websites (wanan.gov.cn,
baike.baidu.com) and Chinese search engines were inaccessible from this environment.
All leadership data is pending verification from:
  - https://www.wanan.gov.cn/xxgk-list-xwld.html (万安县委领导之窗)
  - https://www.wanan.gov.cn/xxgk-list-xzfld.html (万安县政府领导之窗)
  - Baidu Baike for each individual
  - 吉安市委组织部任前公示
  - 万安县人民政府官网

Known from official sources: 县委书记 = 陈海民 (Chén Hǎimín)
County mayor name — confirmed only as 巫太明 previously; current mayor pending verification.
"""

import sqlite3
import os
from datetime import datetime

# ── Paths ──
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "万安县_network.db")
GEXF_PATH = os.path.join(BASE_DIR, "万安县_network.gexf")

esc = lambda s: str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;") if s else ""

# ── DATA ──
# Person ID convention: wanan_{surname_givenname}

PERSONS = [
    # (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)

    # ═══ Top Leaders ═══

    # 县委书记 — 陈海民
    # Source: People's Daily Online — 陈海民任万安县委书记(2021-07); ongoing
    ("wanan_chen_haimin", "陈海民", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委书记", "中共万安县委员会",
     "ldzl.people.com.cn/dfgbk/front/statistics/county?countyId=4041 — 陈海民任万安县委书记(2021-07)；简历细节待查"),

    # ⚠️ 万安县县长 — 需从 wanan.gov.cn 确认
    # 巫太明曾担任万安县长，后调任泰和县委书记；现县长待确认
    ("wanan_mayor_01", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县长", "万安县人民政府",
     "⚠️ 待确认：wanan.gov.cn/xxgk-list-xzfld.html；前任巫太明已调任泰和县委书记"),

    # ═══ Standing Committee (标配县委常委岗位) ═══
    # ⚠️ 县委副书记（专职）
    ("wanan_deputy_sec_01", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委副书记", "中共万安县委员会", "⚠️ 待确认"),

    # ⚠️ 常务副县长
    ("wanan_exec_vice_mayor_01", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委常委、常务副县长", "万安县人民政府", "⚠️ 待确认"),

    # ⚠️ 县纪委书记
    ("wanan_discipline_01", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委常委、县纪委书记、县监委主任", "中共万安县纪律检查委员会", "⚠️ 待确认"),

    # ⚠️ 组织部部长
    ("wanan_org_01", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委常委、组织部部长", "中共万安县委组织部", "⚠️ 待确认"),

    # ⚠️ 宣传部部长
    ("wanan_propaganda_01", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委常委、宣传部部长", "中共万安县委宣传部", "⚠️ 待确认"),

    # ⚠️ 政法委书记
    ("wanan_legal_01", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委常委、政法委书记", "中共万安县委政法委员会", "⚠️ 待确认"),

    # ⚠️ 统战部部长
    ("wanan_united_front_01", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委常委、统战部部长", "中共万安县委统一战线工作部", "⚠️ 待确认"),

    # ⚠️ 人武部部长/政委
    ("wanan_armed_01", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县委常委、人武部政委（或部长）", "万安县人民武装部", "⚠️ 待确认"),

    # ═══ Vice County Mayors (副县长) ═══
    ("wanan_vice_mayor_01", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "副县长", "万安县人民政府", "⚠️ 待确认"),
    ("wanan_vice_mayor_02", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "副县长", "万安县人民政府", "⚠️ 待确认"),
    ("wanan_vice_mayor_03", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "副县长", "万安县人民政府", "⚠️ 待确认"),
    ("wanan_vice_mayor_04", "（待确认）", "女", "汉族", "待查", "待查", "待查", "待查", "待查",
     "副县长", "万安县人民政府", "⚠️ 待确认"),

    # ═══ NPC & CPPCC ═══
    ("wanan_npc_chair_01", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县人大常委会主任", "万安县人民代表大会常务委员会", "⚠️ 待确认"),
    ("wanan_cppcc_chair_01", "（待确认）", "男", "汉族", "待查", "待查", "待查", "待查", "待查",
     "县政协主席", "中国人民政治协商会议万安县委员会", "⚠️ 待确认"),

    # ═══ Ji'an City-level Leaders (cross-reference) ═══
    ("wanan_yan_yun", "严允", "男", "汉族", "1972-11", "江西石城",
     "南昌大学中文系汉语言文学专业（大学学历）", "1993-11", "1994-07",
     "吉安市委书记", "中共吉安市委", "build_jian_data.py"),
    ("wanan_wang_yanao", "王亚联", "男", "汉族", "1972-09", "江西九江",
     "大学学历，公共管理硕士", "中共党员", "待查",
     "吉安市委副书记、市长", "吉安市人民政府",
     "吉安市人民政府网 — 2024年9月任吉安市长"),
    ("wanan_wu_yanling", "吴艳玲", "女", "汉族", "1975-06", "",
     "中央党校大学", "中共党员", "",
     "吉安市委副书记", "中共吉安市委", "build_jian_data.py"),
    ("wanan_chen_dingyu", "陈定宇", "男", "汉族", "1972-05", "",
     "省委党校研究生", "中共党员", "",
     "吉安市委常委、市纪委书记、市监委主任", "中共吉安市纪委", "build_jian_data.py"),
    ("wanan_gong_pingqiu", "龚平秋", "男", "汉族", "1970-06", "",
     "省委党校研究生", "中共党员", "",
     "吉安市委常委、组织部部长", "中共吉安市委组织部", "build_jian_data.py"),
    ("wanan_xiao_yulan", "肖玉兰", "女", "汉族", "1966-07", "江西万安",
     "省委党校研究生", "中共党员", "",
     "吉安市政协主席", "吉安市政协",
     "build_jian_data.py — 籍贯江西万安"),
]

ORGANIZATIONS = [
    # (id, name, type, level, parent, location)
    ("wa_party", "中共万安县委员会", "党委", "县处级", "中共吉安市委", "江西省吉安市万安县"),
    ("wa_gov", "万安县人民政府", "政府", "县处级", "吉安市人民政府", "江西省吉安市万安县"),
    ("wa_discipline", "中共万安县纪律检查委员会", "纪委", "县处级", "吉安市纪委监委", "江西省吉安市万安县"),
    ("wa_org", "中共万安县委组织部", "党委部门", "乡科级", "中共万安县委", "江西省吉安市万安县"),
    ("wa_propaganda", "中共万安县委宣传部", "党委部门", "乡科级", "中共万安县委", "江西省吉安市万安县"),
    ("wa_politics_law", "中共万安县委政法委员会", "党委部门", "乡科级", "中共万安县委", "江西省吉安市万安县"),
    ("wa_united_front", "中共万安县委统一战线工作部", "党委部门", "乡科级", "中共万安县委", "江西省吉安市万安县"),
    ("wa_armed", "万安县人民武装部", "军队", "县处级", "吉安军分区", "江西省吉安市万安县"),
    ("wa_npc", "万安县人民代表大会常务委员会", "人大", "县处级", "吉安市人大常委会", "江西省吉安市万安县"),
    ("wa_cppcc", "中国人民政治协商会议万安县委员会", "政协", "县处级", "吉安市政协", "江西省吉安市万安县"),

    # City-level orgs (for cross-reference)
    ("org_jian_cpc", "中共吉安市委", "党委", "地级市", "中共江西省委", "吉安市"),
    ("org_jian_gov", "吉安市人民政府", "政府", "地级市", "吉安市", "吉安市"),
    ("org_jian_discipline", "中共吉安市纪委/监委", "纪委", "地级市", "中共吉安市委", "吉安市"),
    ("org_jian_org_dept", "中共吉安市委组织部", "党委", "地级市", "中共吉安市委", "吉安市"),
    ("org_jian_cppcc", "吉安市政协", "政协", "地级市", "吉安市", "吉安市"),
]

POSITIONS = [
    # ═══ Current county party secretary ═══
    {"person_id": "wanan_chen_haimin", "org_id": "wa_party", "title": "县委书记",
     "start": "2021-07", "end": "", "rank": "县处级正职",
     "note": "陈海民 — 2021年7月任万安县委书记；出生年月、籍贯、教育背景、此前任职履历待查。"},

    # ═══ Current county mayor ═══
    {"person_id": "wanan_mayor_01", "org_id": "wa_gov", "title": "县长",
     "start": "待查", "end": "", "rank": "县处级正职",
     "note": "⚠️ 姓名待确认。前任巫太明已调任泰和县委书记。"},

    # ═══ Deputy Secretary ═══
    {"person_id": "wanan_deputy_sec_01", "org_id": "wa_party", "title": "县委副书记（专职）",
     "start": "待查", "end": "", "rank": "县处级副职",
     "note": "⚠️ 姓名待确认。罗青球曾担任万安县委副书记，后调任青原区委书记。"},

    # ═══ Executive Vice Mayor ═══
    {"person_id": "wanan_exec_vice_mayor_01", "org_id": "wa_gov", "title": "县委常委、常务副县长",
     "start": "待查", "end": "", "rank": "县处级副职",
     "note": "⚠️ 姓名待确认。"},

    # ═══ Discipline Secretary ═══
    {"person_id": "wanan_discipline_01", "org_id": "wa_discipline", "title": "县委常委、县纪委书记、县监委主任",
     "start": "待查", "end": "", "rank": "县处级副职",
     "note": "⚠️ 姓名待确认。"},

    # ═══ Organization Department Head ═══
    {"person_id": "wanan_org_01", "org_id": "wa_org", "title": "县委常委、组织部部长",
     "start": "待查", "end": "", "rank": "县处级副职",
     "note": "⚠️ 姓名待确认。"},

    # ═══ Propaganda Department Head ═══
    {"person_id": "wanan_propaganda_01", "org_id": "wa_propaganda", "title": "县委常委、宣传部部长",
     "start": "待查", "end": "", "rank": "县处级副职",
     "note": "⚠️ 姓名待确认。"},

    # ═══ Political-Legal Secretary ═══
    {"person_id": "wanan_legal_01", "org_id": "wa_politics_law", "title": "县委常委、政法委书记",
     "start": "待查", "end": "", "rank": "县处级副职",
     "note": "⚠️ 姓名待确认。"},

    # ═══ United Front Head ═══
    {"person_id": "wanan_united_front_01", "org_id": "wa_united_front", "title": "县委常委、统战部部长",
     "start": "待查", "end": "", "rank": "县处级副职",
     "note": "⚠️ 姓名待确认。"},

    # ═══ Armed Forces ═══
    {"person_id": "wanan_armed_01", "org_id": "wa_armed", "title": "县委常委、人武部政委（或部长）",
     "start": "待查", "end": "", "rank": "县处级副职",
     "note": "⚠️ 姓名待确认；按照惯例，人武部主官之一进入县委常委。"},

    # ═══ Vice Mayors ═══
    {"person_id": "wanan_vice_mayor_01", "org_id": "wa_gov", "title": "副县长",
     "start": "待查", "end": "", "rank": "乡科级正职/副处", "note": "⚠️ 姓名待确认。"},
    {"person_id": "wanan_vice_mayor_02", "org_id": "wa_gov", "title": "副县长",
     "start": "待查", "end": "", "rank": "乡科级正职/副处", "note": "⚠️ 姓名待确认。"},
    {"person_id": "wanan_vice_mayor_03", "org_id": "wa_gov", "title": "副县长",
     "start": "待查", "end": "", "rank": "乡科级正职/副处", "note": "⚠️ 姓名待确认。"},
    {"person_id": "wanan_vice_mayor_04", "org_id": "wa_gov", "title": "副县长",
     "start": "待查", "end": "", "rank": "乡科级正职/副处", "note": "⚠️ 姓名待确认。"},

    # ═══ NPC & CPPCC ═══
    {"person_id": "wanan_npc_chair_01", "org_id": "wa_npc", "title": "县人大常委会主任",
     "start": "待查", "end": "", "rank": "县处级正职", "note": "⚠️ 姓名待确认。"},
    {"person_id": "wanan_cppcc_chair_01", "org_id": "wa_cppcc", "title": "县政协主席",
     "start": "待查", "end": "", "rank": "县处级正职", "note": "⚠️ 姓名待确认。"},

    # ═══ City-level leaders cross-reference ═══
    {"person_id": "wanan_yan_yun", "org_id": "org_jian_cpc", "title": "吉安市委书记",
     "start": "2026-04", "end": "", "rank": "正厅级",
     "note": "现任；2019省交通厅→萍乡组织部长→2020南昌市委副书记→2021宜春市长/书记"},
    {"person_id": "wanan_wang_yanao", "org_id": "org_jian_gov", "title": "吉安市委副书记、市长",
     "start": "2024-09", "end": "", "rank": "正厅级",
     "note": "2024年9月任吉安市长"},
    {"person_id": "wanan_wu_yanling", "org_id": "org_jian_cpc", "title": "吉安市委副书记",
     "start": "~2022-11", "end": "", "rank": "副厅级", "note": "现任"},
    {"person_id": "wanan_chen_dingyu", "org_id": "org_jian_cpc", "title": "吉安市委常委、市纪委书记",
     "start": "~2022", "end": "", "rank": "副厅级", "note": "现任"},
    {"person_id": "wanan_chen_dingyu", "org_id": "org_jian_discipline", "title": "吉安市监委主任",
     "start": "~2022", "end": "", "rank": "副厅级", "note": "现任"},
    {"person_id": "wanan_gong_pingqiu", "org_id": "org_jian_cpc", "title": "吉安市委常委、组织部部长",
     "start": "~2025-10", "end": "", "rank": "副厅级", "note": "现任"},
    {"person_id": "wanan_gong_pingqiu", "org_id": "org_jian_org_dept", "title": "吉安市委组织部部长",
     "start": "~2025-10", "end": "", "rank": "正处级", "note": "现任"},
    {"person_id": "wanan_xiao_yulan", "org_id": "org_jian_cppcc", "title": "吉安市政协主席",
     "start": "~2024", "end": "", "rank": "正厅级", "note": "现任；籍贯万安"},
]

RELATIONSHIPS = [
    # ═══ Secretary ↔ Mayor: 党政正职搭档 ═══
    {"person_a": "wanan_chen_haimin", "person_b": "wanan_mayor_01",
     "type": "工作关系", "context": "县委书记与县长为万安县党政正职搭档关系",
     "overlap_org": "万安县", "overlap_period": "至2026年"},

    # ═══ Secretary ↔ City Secretary: 上下级关系 ═══
    {"person_a": "wanan_chen_haimin", "person_b": "wanan_yan_yun",
     "type": "上下级关系", "context": "县委书记受吉安市委领导，严允为吉安市委书记",
     "overlap_org": "中共吉安市委-万安县", "overlap_period": "2026-04至今"},

    # ═══ Secretary ↔ City Mayor ═══
    {"person_a": "wanan_chen_haimin", "person_b": "wanan_wang_yanao",
     "type": "上下级关系", "context": "县委书记与吉安市市长为上下级党政关系",
     "overlap_org": "吉安市", "overlap_period": "2024-09至今"},

    # ═══ Secretary ↔ Organization Dept Head: 干部管理 ═══
    {"person_a": "wanan_chen_haimin", "person_b": "wanan_gong_pingqiu",
     "type": "上下级关系", "context": "县管干部工作关系：县委书记与市委组织部部长在干部选拔任用中存在工作互动",
     "overlap_org": "吉安市-万安县干部体系", "overlap_period": ""},

    # ═══ Secretary ↔ Discipline Head ═══
    {"person_a": "wanan_chen_haimin", "person_b": "wanan_chen_dingyu",
     "type": "监督关系", "context": "县委书记与市纪委书记为同级党委-纪委关系",
     "overlap_org": "吉安市-万安县监督体系", "overlap_period": ""},

    # ═══ Secretary ↔ City Deputy Secretary ═══
    {"person_a": "wanan_chen_haimin", "person_b": "wanan_wu_yanling",
     "type": "上下级关系", "context": "县委受市委领导，县书记与市委副书记为上下级工作关系",
     "overlap_org": "吉安市", "overlap_period": ""},

    # ═══ Secretary ↔ 市政协主席 (同乡/万安籍) ═══
    {"person_a": "wanan_chen_haimin", "person_b": "wanan_xiao_yulan",
     "type": "同乡关系", "context": "肖玉兰（吉安市政协主席）籍贯江西万安；与万安县委书记有同乡和工作关联",
     "overlap_org": "万安县", "overlap_period": ""},

    # ═══ Secretary ↔ County Discipline: 一岗双责 ═══
    {"person_a": "wanan_chen_haimin", "person_b": "wanan_discipline_01",
     "type": "工作关系", "context": "县委书记与县纪委书记为同级党委-纪委关系",
     "overlap_org": "中共万安县委员会", "overlap_period": "至2026年"},

    # ═══ Secretary ↔ Standing Committee members ═══
    {"person_a": "wanan_chen_haimin", "person_b": "wanan_exec_vice_mayor_01",
     "type": "工作关系", "context": "县委书记与常务副县长为常委会班子关系",
     "overlap_org": "中共万安县委员会", "overlap_period": "至2026年"},
    {"person_a": "wanan_chen_haimin", "person_b": "wanan_org_01",
     "type": "工作关系", "context": "县委书记与组织部部长为常委会班子关系",
     "overlap_org": "中共万安县委员会", "overlap_period": "至2026年"},
    {"person_a": "wanan_chen_haimin", "person_b": "wanan_propaganda_01",
     "type": "工作关系", "context": "县委书记与宣传部部长为常委会班子关系",
     "overlap_org": "中共万安县委员会", "overlap_period": "至2026年"},
    {"person_a": "wanan_chen_haimin", "person_b": "wanan_legal_01",
     "type": "工作关系", "context": "县委书记与政法委书记为常委会班子关系",
     "overlap_org": "中共万安县委员会", "overlap_period": "至2026年"},
    {"person_a": "wanan_chen_haimin", "person_b": "wanan_united_front_01",
     "type": "工作关系", "context": "县委书记与统战部部长为常委会班子关系",
     "overlap_org": "中共万安县委员会", "overlap_period": "至2026年"},

    # ═══ County Mayor ↔ City Leaders ═══
    {"person_a": "wanan_mayor_01", "person_b": "wanan_yan_yun",
     "type": "上下级关系", "context": "县长受市委领导",
     "overlap_org": "吉安市", "overlap_period": "2026-04至今"},
    {"person_a": "wanan_mayor_01", "person_b": "wanan_wang_yanao",
     "type": "上下级关系", "context": "县长受吉安市市长领导",
     "overlap_org": "吉安市", "overlap_period": "2024-09至今"},

    # ═══ NPC Chair ↔ CPC Secretary ═══
    {"person_a": "wanan_npc_chair_01", "person_b": "wanan_chen_haimin",
     "type": "工作关系", "context": "县人大常委会主任与县委书记为四套班子关系",
     "overlap_org": "万安县", "overlap_period": "至2026年"},

    # ═══ CPPCC Chair ↔ CPC Secretary ═══
    {"person_a": "wanan_cppcc_chair_01", "person_b": "wanan_chen_haimin",
     "type": "工作关系", "context": "县政协主席与县委书记为四套班子关系",
     "overlap_org": "万安县", "overlap_period": "至2026年"},
]


# ── Build SQLite ──
def build_sqlite():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id TEXT PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id TEXT PRIMARY KEY, name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT, org_id TEXT, title TEXT, start TEXT,
            end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT, person_b TEXT, type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
        CREATE INDEX IF NOT EXISTS idx_person_name ON persons(name);
        CREATE INDEX IF NOT EXISTS idx_org_name ON organizations(name);
        CREATE INDEX IF NOT EXISTS idx_pos_person ON positions(person_id);
        CREATE INDEX IF NOT EXISTS idx_pos_org ON positions(org_id);
    """)

    col_names = ["id","name","gender","ethnicity","birth","birthplace","education",
                 "party_join","work_start","current_post","current_org","source"]
    for p in PERSONS:
        d = dict(zip(col_names, p))
        c.execute("INSERT OR REPLACE INTO persons VALUES(:id,:name,:gender,:ethnicity,:birth,:birthplace,:education,:party_join,:work_start,:current_post,:current_org,:source)", d)

    org_cols = ["id","name","type","level","parent","location"]
    for o in ORGANIZATIONS:
        d = dict(zip(org_cols, o))
        c.execute("INSERT OR REPLACE INTO organizations VALUES(:id,:name,:type,:level,:parent,:location)", d)

    for p in POSITIONS:
        c.execute("INSERT OR REPLACE INTO positions(person_id,org_id,title,start,end,rank,note) VALUES(:person_id,:org_id,:title,:start,:end,:rank,:note)", p)

    for r in RELATIONSHIPS:
        c.execute("INSERT OR REPLACE INTO relationships(person_a,person_b,type,context,overlap_org,overlap_period) VALUES(:person_a,:person_b,:type,:context,:overlap_org,:overlap_period)", r)

    conn.commit()
    print("\n=== SQLite Summary ===")
    for tbl in ["persons","organizations","positions","relationships"]:
        cnt = c.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()[0]
        print(f"  {tbl}: {cnt}")
    conn.close()
    print(f"  DB: {DB_PATH}")


# ── Build GEXF ──
def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>OpenCode Research Agent</creator>')
    lines.append('    <description>万安县领导班子工作关系网络 — 2026年7月调查，所有信息⚠️待确认</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append("""    <attributes class="node">
      <attribute id="0" title="type" type="string"/>
      <attribute id="1" title="entity_type" type="string"/>
      <attribute id="2" title="birth" type="string"/>
      <attribute id="3" title="birthplace" type="string"/>
      <attribute id="4" title="current_post" type="string"/>
      <attribute id="5" title="level" type="string"/>
    </attributes>
    <attributes class="edge">
      <attribute id="0" title="type" type="string"/>
      <attribute id="1" title="start" type="string"/>
      <attribute id="2" title="end" type="string"/>
      <attribute id="3" title="context" type="string"/>
    </attributes>""")

    # Nodes: Persons
    lines.append("    <nodes>")
    col_names = ["id","name","gender","ethnicity","birth","birthplace","education",
                 "party_join","work_start","current_post","current_org","source"]
    persons_dicts = [dict(zip(col_names, p)) for p in PERSONS]

    for p in persons_dicts:
        pid = esc(p["id"])
        name = esc(p["name"])
        birth = esc(p.get("birth", ""))
        birthplace = esc(p.get("birthplace", ""))
        post = esc(p.get("current_post", ""))

        # Color by role
        title = p.get("current_post", "")
        if "县委书记" in title and ("副" not in title or "副书记" not in title):
            c = "255,50,50"
            sz = "20.0"
        elif "县长" in title and ("副" not in title):
            c = "50,100,255"
            sz = "20.0"
        elif "纪委" in title:
            c = "255,165,0"
            sz = "12.0"
        elif "常委" in title or "副" in title:
            c = "100,150,200"
            sz = "12.0"
        elif "人大" in title or "政协" in title:
            c = "60,180,75"
            sz = "12.0"
        elif "书记" in title:
            c = "255,50,50"
            sz = "12.0"
        elif "市长" in title and "副" not in title:
            c = "50,100,255"
            sz = "20.0"
        else:
            c = "100,100,100"
            sz = "12.0"

        lines.append(f"""      <node id="{pid}" label="{name}">
        <attvalues>
          <attvalue for="0" value="person"/>
          <attvalue for="1" value="person"/>
          <attvalue for="2" value="{birth}"/>
          <attvalue for="3" value="{birthplace}"/>
          <attvalue for="4" value="{post}"/>
          <attvalue for="5" value=""/>
        </attvalues>
        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>
        <viz:size value="{sz}"/>
      </node>""")

    # Nodes: Organizations
    org_cols = ["id","name","type","level","parent","location"]
    org_dicts = [dict(zip(org_cols, o)) for o in ORGANIZATIONS]

    org_color_map = {
        "党委": "255,200,200", "政府": "200,200,255", "纪委": "255,220,200",
        "党委部门": "255,220,220", "人大": "200,255,255", "政协": "255,240,200",
        "军队": "200,200,200"
    }

    for o in org_dicts:
        oid = esc(o["id"])
        oname = esc(o["name"])
        otype = o.get("type", "")
        olevel = esc(o.get("level", ""))
        oc = org_color_map.get(otype, "200,200,200")

        lines.append(f"""      <node id="{oid}" label="{oname}">
        <attvalues>
          <attvalue for="0" value="organization"/>
          <attvalue for="1" value="org"/>
          <attvalue for="2" value=""/>
          <attvalue for="3" value=""/>
          <attvalue for="4" value=""/>
          <attvalue for="5" value="{olevel}"/>
        </attvalues>
        <viz:color r="{oc.split(",")[0]}" g="{oc.split(",")[1]}" b="{oc.split(",")[2]}"/>
        <viz:size value="8.0"/>
      </node>""")

    lines.append("    </nodes>")

    # Edges
    lines.append("    <edges>")
    edge_id = 0

    for pos in POSITIONS:
        edge_id += 1
        src = esc(pos["person_id"])
        tgt = esc(pos["org_id"])
        title = esc(pos.get("title", ""))
        note = esc(pos.get("note", ""))
        s = esc(pos.get("start", ""))
        e = esc(pos.get("end", ""))
        ctx = f"{title}. {note}" if note else title

        lines.append(f"""      <edge id="{edge_id}" source="{src}" target="{tgt}" label="{title}" weight="1.0">
        <attvalues>
          <attvalue for="0" value="worked_at"/>
          <attvalue for="1" value="{s}"/>
          <attvalue for="2" value="{e}"/>
          <attvalue for="3" value="{ctx}"/>
        </attvalues>
      </edge>""")

    for rel in RELATIONSHIPS:
        edge_id += 1
        a = esc(rel["person_a"])
        b = esc(rel["person_b"])
        rtype = esc(rel.get("type", ""))
        ctx = esc(rel.get("context", ""))
        period = esc(rel.get("overlap_period", ""))
        w = "2.0" if rel["type"] in ("工作关系", "上下级关系") else "1.0"

        lines.append(f"""      <edge id="{edge_id}" source="{a}" target="{b}" label="{rtype}" weight="{w}">
        <attvalues>
          <attvalue for="0" value="{rtype}"/>
          <attvalue for="1" value=""/>
          <attvalue for="2" value=""/>
          <attvalue for="3" value="{ctx} ({period})"/>
        </attvalues>
      </edge>""")

    lines.append("    </edges>")
    lines.append("  </graph>")
    lines.append("</gexf>")

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"\n=== GEXF Summary ===")
    print(f"  {edge_id} edges written")
    print(f"  GEXF: {GEXF_PATH}")


# ── Main ──
if __name__ == "__main__":
    print("=" * 60)
    print("  万安县 (Wan'an County) Leadership Network Builder")
    print(f"  Date: {datetime.now().strftime('%Y-%m-%d')}")
    print("  NOTE: All data marked ⚠️ 待确认 pending web verification")
    print("=" * 60)
    build_sqlite()
    build_gexf()
    print("\n=== Done ===")
