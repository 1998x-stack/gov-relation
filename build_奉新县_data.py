#!/usr/bin/env python3
"""
奉新县领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Fengxin County leadership.

Research as of 2026-07-15:
- 县委书记: 黄为民 (since 2024.12)
- 县长: 陈伟 (appointed 2024.12,县委副书记、提名县长候选人)
- 前任县委书记: 陈志尧 (2021.08-2024.09, 调任宜春经济技术开发区管委会主任)
- 前任县长: 喻军 (2021.08-2024.12, 调任靖安县委书记)

Note: Full standing committee roster unavailable from open web (geoblocked from
Chinese government websites). Core positions are documented from appointment notices
and media reports (网易新闻, 五星党建, 搜狐新闻).
"""

import sqlite3
import os
from datetime import datetime

# ── Paths ──
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "奉新县_network.db")
GEXF_PATH = os.path.join(BASE_DIR, "奉新县_network.gexf")

esc = lambda s: str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;") if s else ""

# ── DATA ──
# Person ID convention: fengxin_{surname_givenname}

PERSONS = [
    # (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)

    # ═══ Top Leaders ═══

    # 县委书记 — 黄为民
    # Source: 网易新闻 (2024-12-24) — 宜丰人黄为民任奉新县委书记
    # Full career: 奉新干垦乡 → 团县委 → 上富镇 → 溜头乡(柳溪乡) → 宜丰花桥乡/新庄镇
    #   → 团市委副书记 → 袁州区委宣传部长 → 团市委书记 → 铜鼓县长 → 靖安县长 → 奉新县委书记
    ("fengxin_huang_weimin", "黄为民", "男", "汉族", "1978-01", "江西宜丰", "中专",
     "1997-05", "1996-07",
     "县委书记", "中共奉新县委员会",
     "网易新闻 https://www.163.com/dy/article/JKB05GCC05496YZA.html — 黄为民任奉新县委书记(2024-12); 五星党建; 人物履历全文"),

    # 县长 — 陈伟
    # Source: 网易新闻 (2024-12-24) — 陈伟同志任奉新县委副书记、提名为县长候选人
    # Note: Full biography pending — only appointment notice available
    ("fengxin_chen_wei", "陈伟", "男", "汉族", "待查", "待查", "待查",
     "待查", "待查",
     "县委副书记、县长", "奉新县人民政府",
     "网易新闻 https://www.163.com/dy/article/JK6SE53505500FOQ.html — 陈伟同志提名为奉新县政府县长候选人(2024-12); 五星党建"),

    # ═══ Predecessors ═══

    # 前任县委书记 — 陈志尧
    # Source: 网易新闻 (2024-09-10) — 陈志尧任宜春经开区管委会主任
    # Full career: 宜春林业局 → 宜春市政府办 → 袁州副区长 → 万载县委常委/副县长 → 靖安常务副县长
    #   → 万载县委副书记 → 奉新县长 → 奉新县委书记 → 宜春经开区管委会主任
    ("fengxin_chen_zhiyao", "陈志尧", "男", "汉族", "1972-04", "江西樟树", "大学",
     "1999-06", "1993-09",
     "宜春经济技术开发区管委会主任（原奉新县委书记）", "宜春经济技术开发区",
     "网易新闻 https://www.163.com/dy/article/JBNMDOS805496YZA.html — 陈志尧同志任宜春经济技术开发区管委会主任(2024-09); 南昌大学哲学系专业"),

    # 前任县长（调任靖安县委书记）— 喻军
    # Source: 网易新闻 (2024-12-24) — 喻军任靖安县委书记
    ("fengxin_yu_jun", "喻军", "男", "汉族", "1979-01", "江西高安", "研究生",
     "2001-12", "1999-10",
     "靖安县委书记（原奉新县长）", "中共靖安县委员会",
     "网易新闻 https://www.163.com/dy/article/JKB05GCC05496YZA.html — 喻军任靖安县委书记(2024-12); 五星党建"),

    # ═══ Other Key Positions (currently placeholder — need verification from fengxin.gov.cn) ═══
    # ⚠️ Full standing committee roster requires access to fengxin.gov.cn leadership page

    ("fengxin_deputy_sec_01", "（待确认）", "男", "汉族", "待查", "待查", "待查",
     "待查", "待查",
     "县委副书记（专职）", "中共奉新县委员会",
     "⚠️ 待确认: fengxin.gov.cn/xxgk/ — 因境外访问受限,常委班子名单待补充"),

    ("fengxin_exec_vice_mayor_01", "（待确认）", "男", "汉族", "待查", "待查", "待查",
     "待查", "待查",
     "县委常委、常务副县长", "奉新县人民政府",
     "⚠️ 待确认"),

    ("fengxin_discipline_01", "（待确认）", "男", "汉族", "待查", "待查", "待查",
     "待查", "待查",
     "县委常委、县纪委书记、县监委主任", "中共奉新县纪律检查委员会",
     "⚠️ 待确认"),

    ("fengxin_org_01", "（待确认）", "男", "汉族", "待查", "待查", "待查",
     "待查", "待查",
     "县委常委、组织部部长", "中共奉新县委组织部",
     "⚠️ 待确认"),

    ("fengxin_propaganda_01", "（待确认）", "男", "汉族", "待查", "待查", "待查",
     "待查", "待查",
     "县委常委、宣传部部长", "中共奉新县委宣传部",
     "⚠️ 待确认"),

    ("fengxin_legal_01", "（待确认）", "男", "汉族", "待查", "待查", "待查",
     "待查", "待查",
     "县委常委、政法委书记", "中共奉新县委政法委员会",
     "⚠️ 待确认"),

    ("fengxin_united_front_01", "（待确认）", "男", "汉族", "待查", "待查", "待查",
     "待查", "待查",
     "县委常委、统战部部长", "中共奉新县委统一战线工作部",
     "⚠️ 待确认"),

    # ═══ Cross-County Connections ═══

    # 熊辉 — 奉新人, 现任安义县委书记 (from Anyi data)
    ("anyi_xiong_hui", "熊辉", "男", "汉族", "1981-03", "江西奉新", "博士研究生",
     "待查", "待查",
     "安义县委书记", "中共安义县委员会",
     "安义县调查数据 build_anyi_data.py"),

    # 熊振强 — 奉新人, 曾任安义县委常委
    ("jinxian_xiong_zhenqiang", "熊振强", "男", "汉族", "1972-03", "江西奉新", "大学",
     "待查", "待查",
     "进贤县委副书记（原安义县委常委）", "中共进贤县委员会",
     "安义县调查数据 build_anyi_data.py"),
]

ORGANIZATIONS = [
    # (id, name, type, level, parent, location)
    (1, "中共奉新县委员会", "党委", "县处级", "中共宜春市委员会", "江西宜春奉新"),
    (2, "奉新县人民政府", "政府", "县处级", "宜春市人民政府", "江西宜春奉新"),
    (3, "中共奉新县纪律检查委员会", "纪委", "县处级", "中共宜春市纪律检查委员会", "江西宜春奉新"),
    (4, "中共奉新县委组织部", "党委部门", "县处级", "中共奉新县委员会", "江西宜春奉新"),
    (5, "中共奉新县委宣传部", "党委部门", "县处级", "中共奉新县委员会", "江西宜春奉新"),
    (6, "中共奉新县委政法委员会", "党委部门", "县处级", "中共奉新县委员会", "江西宜春奉新"),
    (7, "中共奉新县委统一战线工作部", "党委部门", "县处级", "中共奉新县委员会", "江西宜春奉新"),
    (8, "宜春经济技术开发区", "开发区", "厅级", "宜春市人民政府", "江西宜春"),
    (9, "中共靖安县委员会", "党委", "县处级", "中共宜春市委员会", "江西宜春靖安"),
    (10, "靖安县人民政府", "政府", "县处级", "宜春市人民政府", "江西宜春靖安"),
    (11, "中共铜鼓县委员会", "党委", "县处级", "中共宜春市委员会", "江西宜春铜鼓"),
    (12, "铜鼓县人民政府", "政府", "县处级", "宜春市人民政府", "江西宜春铜鼓"),
    (13, "共青团宜春市委员会", "群团", "县处级", "中共宜春市委员会", "江西宜春"),
    (14, "中共袁州区委宣传部", "党委部门", "县处级", "中共袁州区委员会", "江西宜春袁州"),
    (15, "中共宜丰县委员会", "党委", "县处级", "中共宜春市委员会", "江西宜春宜丰"),
    (16, "宜丰县人民政府", "政府", "县处级", "宜春市人民政府", "江西宜春宜丰"),
    (17, "中共安义县委员会", "党委", "县处级", "中共南昌市委员会", "江西南昌安义"),
    (18, "中共进贤县委员会", "党委", "县处级", "中共南昌市委员会", "江西南昌进贤"),
    (19, "宜春市人民政府办公室", "政府", "县处级", "宜春市人民政府", "江西宜春"),
    (20, "中共黄垦镇委员会（原干垦乡）", "党委", "乡科级", "中共奉新县委员会", "江西宜春奉新"),
    (21, "中共上富镇委员会", "党委", "乡科级", "中共奉新县委员会", "江西宜春奉新"),
    (22, "中共柳溪乡委员会", "党委", "乡科级", "中共奉新县委员会", "江西宜春奉新"),
]

POSITIONS = [
    # (person_id, org_id, title, start, end, rank, note)

    # 黄为民 - 县委书记
    ("fengxin_huang_weimin", 1, "县委书记", "2024-12", "至今", "县处级正职", "2024年12月任奉新县委书记"),
    ("fengxin_huang_weimin", 10, "靖安县县长", "2021-02", "2024-12", "县处级正职", "靖安县委副书记、县长"),
    ("fengxin_huang_weimin", 12, "铜鼓县县长", "2016-10", "2020-12", "县处级正职", "铜鼓县委副书记、县长"),
    ("fengxin_huang_weimin", 13, "共青团宜春市委书记", "2013-08", "2016-07", "县处级正职", "团市委书记、党组书记"),
    ("fengxin_huang_weimin", 14, "袁州区委宣传部长", "2011-06", "2013-06", "县处级副职", "区委常委、宣传部长; 兼机电产业基地党委书记"),
    ("fengxin_huang_weimin", 13, "共青团宜春市委副书记", "2009-04", "2011-06", "县处级副职", "团市委副书记、党组成员"),
    ("fengxin_huang_weimin", 15, "新庄镇党委书记", "2007-02", "2009-04", "乡科级正职", "宜丰县新庄镇党委书记、人大主席"),
    ("fengxin_huang_weimin", 16, "花桥乡党委书记", "2004-03", "2007-02", "乡科级正职", "宜丰县花桥乡党委书记、人大主席"),
    ("fengxin_huang_weimin", 22, "柳溪乡党委书记", "2002-12", "2004-03", "乡科级正职", "溜头乡(后更名柳溪乡)党委书记、人大主席"),
    ("fengxin_huang_weimin", 21, "上富镇党委副书记", "2001-12", "2002-12", "乡科级副职", "上富镇党委副书记、纪委书记"),
    ("fengxin_huang_weimin", 0, "共青团奉新县委书记", "1999-07", "2001-12", "副科级", "团县委书记(副科级后正科级)"),
    ("fengxin_huang_weimin", 0, "共青团奉新县委副书记", "1998-03", "1999-07", "副科级", ""),
    ("fengxin_huang_weimin", 20, "干垦乡工办副主任", "1996-08", "1998-03", "科员级", "干垦乡工办副主任、团委书记"),

    # 陈伟 - 县长 (appointed 2024.12, biography pending)
    ("fengxin_chen_wei", 2, "县委副书记、县长", "2024-12", "至今", "县处级正职", "2024年12月任奉新县委副书记、提名为县长候选人"),
    # Note: 陈伟's earlier career needs verification

    # 陈志尧 - 前任县委书记
    ("fengxin_chen_zhiyao", 8, "宜春经开区管委会主任", "2024-09", "至今", "厅级", "宜春经济技术开发区管委会主任"),
    ("fengxin_chen_zhiyao", 1, "奉新县委书记", "2021-08", "2024-09", "县处级正职", "奉新县委委员、常委、书记"),
    ("fengxin_chen_zhiyao", 2, "奉新县县长", "2021-01", "2021-08", "县处级正职", "奉新县委副书记、县人民政府县长"),
    ("fengxin_chen_zhiyao", 15, "万载县委副书记", "2017-12", "2021-01", "县处级副职", "万载县委副书记"),
    ("fengxin_chen_zhiyao", 3, "靖安县委常委、常务副县长", "2016-08", "2017-12", "县处级副职", "靖安县委常委、常务副县长"),
    ("fengxin_chen_zhiyao", 15, "万载县委常委、副县长", "2011-06", "2016-08", "县处级副职", "万载县委常委、副县长"),
    ("fengxin_chen_zhiyao", 14, "袁州区政府副区长", "2009-04", "2011-06", "县处级副职", "袁州区政府副区长(副县级)"),
    ("fengxin_chen_zhiyao", 19, "宜春市政府办督查科科长", "2002-10", "2009-04", "乡科级正职", "督查科科长"),
    ("fengxin_chen_zhiyao", 19, "宜春市政府办督查科副科长", "2002-03", "2002-10", "乡科级副职", ""),
    ("fengxin_chen_zhiyao", 19, "宜春市政府办副主任科员", "2001-01", "2002-03", "乡科级副职", ""),
    ("fengxin_chen_zhiyao", 19, "宜春市政府(行署)办公室干部", "1997-08", "2001-01", "科员级", ""),
    ("fengxin_chen_zhiyao", 0, "宜春市(行署)林业局干部", "1993-09", "1997-08", "科员级", ""),

    # 喻军 - 前任县长
    ("fengxin_yu_jun", 9, "靖安县委书记", "2024-12", "至今", "县处级正职", "靖安县委书记"),
    ("fengxin_yu_jun", 2, "奉新县县长", "2021-08", "2024-12", "县处级正职", "奉新县委副书记、县长"),
    ("fengxin_yu_jun", 15, "宜丰县委副书记", "2020-12", "2021-08", "县处级副职", "宜丰县委副书记"),
    ("fengxin_yu_jun", 15, "宜丰县委常委、常务副县长", "2019-07", "2020-12", "县处级副职", "宜丰县委常委、常务副县长"),
    ("fengxin_yu_jun", 3, "樟树市委常委、市政府党组成员", "2016-07", "2019-07", "县处级副职", "樟树市委常委、市政府党组成员"),
    ("fengxin_yu_jun", 0, "宜春市交通运输局副局长", "2014-07", "2016-07", "县处级副职", "挂任丰城市委常委、市政府副市长"),
    ("fengxin_yu_jun", 0, "高安市上湖乡党委书记", "2013-03", "2014-07", "乡科级正职", "上湖乡党委书记、人大主席"),
    ("fengxin_yu_jun", 0, "高安市相城镇党委副书记、镇长", "2009-04", "2013-03", "乡科级正职", ""),
    ("fengxin_yu_jun", 0, "高安市八景镇党委副书记", "2007-03", "2008-05", "乡科级副职", ""),
    ("fengxin_yu_jun", 0, "高安市委政法委综治办副主任", "2006-01", "2007-03", "乡科级副职", ""),
    ("fengxin_yu_jun", 0, "高安市委驻瑞州街道副科级维稳信息督查员", "2003-07", "2006-01", "副科级", ""),
    ("fengxin_yu_jun", 0, "高安市筠阳镇干部、党政办主任", "1999-10", "2003-07", "科员级", "宜春地委组织部公开选拔选调生"),

    # 熊辉 — 奉新籍, 安义县委书记 (cross-county reference)
    ("anyi_xiong_hui", 17, "安义县委书记", "2026-07", "至今", "县处级正职", "2026年新任安义县委书记; 奉新籍"),
    # 熊振强 — 奉新籍, 曾任安义县委常委
    ("jinxian_xiong_zhenqiang", 18, "进贤县委副书记", "2021", "至今", "县处级副职", "进贤县委副书记; 奉新籍"),
    ("jinxian_xiong_zhenqiang", 17, "安义县委常委", "2016", "2021", "县处级副职", "安义县委常委"),
]

RELATIONSHIPS = [
    # (person_a, person_b, type, context, overlap_org, overlap_period)

    # 黄为民 ↔ 陈志尧 (predecessor-successor)
    ("fengxin_huang_weimin", "fengxin_chen_zhiyao", "predecessor_successor",
     "陈志尧2024年9月调任宜春经开区主任,黄为民2024年12月接任奉新县委书记",
     "中共奉新县委员会", "2024-09/2024-12"),

    # 黄为民 ↔ 陈伟 (党政搭档)
    ("fengxin_huang_weimin", "fengxin_chen_wei", "党政搭档",
     "黄为民任县委书记,陈伟任县委副书记、县长候选人",
     "中共奉新县委员会", "2024-12至今"),

    # 黄为民 ↔ 喻军 (predecessor-successor at 靖安县长)
    ("fengxin_huang_weimin", "fengxin_yu_jun", "predecessor_successor",
     "黄为民任靖安县长(2021-2024)后,喻军接任奉新县长(2021-2024)后调任靖安县委书记;二人分别在靖安和奉新交叉",
     "靖安县人民政府", "2021-02/2024-12"),

    # 陈志尧 ↔ 喻军 (党政搭档)
    ("fengxin_chen_zhiyao", "fengxin_yu_jun", "党政搭档",
     "陈志尧任奉新县委书记期间,喻军任奉新县长(2021.08-2024.09)",
     "中共奉新县委员会", "2021-08/2024-09"),

    # 喻军 ↔ 陈志尧 (靖安—万载工作关联)
    ("fengxin_yu_jun", "fengxin_chen_zhiyao", "predecessor_successor",
     "陈志尧曾在万载担任县委副书记,喻军在宜丰担任县委副书记;二人在宜春市县级领导层面有交集",
     "", "2017-2021"),

    # 熊辉 ↔ 奉新 (籍贯关联 — 奉新人任安义县委书记)
    ("anyi_xiong_hui", "fengxin_huang_weimin", "same_native_place",
     "熊辉(奉新籍)任安义县委书记,黄为民(宜丰籍)任奉新县委书记;二人同为宜春市辖县委书记",
     "", ""),

    # 熊辉 ↔ 熊振强 (奉新籍关联)
    ("anyi_xiong_hui", "jinxian_xiong_zhenqiang", "same_native_place",
     "熊辉(奉新籍)、熊振强(奉新籍),二人均出生在奉新县,先后在安义县任职",
     "中共安义县委员会", "2016-2021"),
]


# ── Utility ──
def person_color(pid):
    """Return 'r,g,b' color string based on person's role."""
    if pid == "fengxin_huang_weimin":
        return "255,50,50"  # Red — Party Secretary
    elif pid == "fengxin_chen_wei":
        return "50,100,255"  # Blue — Government leader
    elif pid == "fengxin_chen_zhiyao":
        return "200,100,100"  # Dark pink — Former Party Secretary
    elif pid == "fengxin_yu_jun":
        return "100,100,200"  # Light blue — Former government leader
    elif pid in ("anyi_xiong_hui",):
        return "255,165,0"  # Orange — Cross-county connection (also a Party Secretary)
    elif pid == "jinxian_xiong_zhenqiang":
        return "150,100,50"  # Brown — Cross-county
    else:
        return "100,100,100"  # Grey — Others


def is_top_leader(pid):
    return pid in ("fengxin_huang_weimin", "fengxin_chen_wei",
                   "fengxin_chen_zhiyao", "fengxin_yu_jun",
                   "anyi_xiong_hui")


def person_size(pid):
    return "20.0" if is_top_leader(pid) else "12.0"


def org_color(otype):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
        "纪委": "255,200,150",
        "党委部门": "230,210,255",
        "群团": "255,220,255",
    }
    return colors.get(otype, "200,200,200")


# ── Build SQLite ──
def build_db():
    os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in PERSONS:
        c.execute(
            "INSERT OR REPLACE INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11])
        )
    for o in ORGANIZATIONS:
        c.execute(
            "INSERT OR REPLACE INTO organizations (id, name, type, level, parent, location) VALUES (?,?,?,?,?,?)",
            o
        )
    for pos in POSITIONS:
        c.execute(
            "INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)",
            (pos[0], pos[1], pos[2], pos[3], pos[4], pos[5], pos[6])
        )
    for r in RELATIONSHIPS:
        c.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
            (r[0], r[1], r[2], r[3], r[4], r[5])
        )

    conn.commit()
    conn.close()
    print(f"[DB] Wrote {len(PERSONS)} persons, {len(ORGANIZATIONS)} orgs, {len(POSITIONS)} positions, {len(RELATIONSHIPS)} relationships → {DB_PATH}")


# ── Build GEXF ──
def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append('    <description>奉新县领导班子工作关系网络 — 核心领导人物关系图</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="birthplace" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="start" type="string"/>')
    lines.append('      <attribute id="3" title="end" type="string"/>')
    lines.append('    </attributes>')

    # ── Nodes: Persons ──
    lines.append('    <nodes>')
    for p in PERSONS:
        pid = p[0]
        name = p[1]
        birthplace = p[5]
        role = p[9]
        c = person_color(pid)
        sz = person_size(pid)
        lines.append(f'      <node id="{esc(pid)}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(birthplace)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # ── Nodes: Organizations ──
    for o in ORGANIZATIONS:
        oid = o[0]
        oname = o[1]
        otype = o[2]
        c = org_color(otype)
        lines.append(f'      <node id="o{oid}" label="{esc(oname)}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(otype)}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # ── Edges ──
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked_at)
    for pos in POSITIONS:
        pid = pos[0]
        oid = pos[1]
        title = pos[2]
        start = pos[3] or ""
        end = pos[4] or ""
        if oid == 0:
            continue  # Skip org 0 (placeholder)
        lines.append(f'      <edge id="e{eid}" source="{esc(pid)}" target="o{oid}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(start)}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(end)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Person ↔ Person (relationships)
    for r in RELATIONSHIPS:
        pa, pb, rtype, context, oorg, operiod = r
        lines.append(f'      <edge id="e{eid}" source="{esc(pa)}" target="{esc(pb)}" label="{esc(rtype)}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rtype)}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(context)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(operiod.split("/")[0] if "/" in operiod else "")}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(operiod.split("/")[1] if "/" in operiod else "")}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    os.makedirs(os.path.dirname(GEXF_PATH) or ".", exist_ok=True)
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[GEXF] Wrote {eid} edges → {GEXF_PATH}")


# ── Summary ──
def print_summary():
    confirmed_persons = [p for p in PERSONS if "待确认" not in p[1] and "待查" not in p[9]]
    pending_persons = [p for p in PERSONS if "待确认" in p[1] or p[9].startswith("⚠️")]

    print()
    print("=" * 60)
    print("奉新县领导班子工作关系网络 — 构建完成")
    print("=" * 60)
    print(f"  人员总数: {len(PERSONS)}")
    print(f"    已确认: {len(confirmed_persons)}")
    print(f"    待补充: {len(pending_persons)}")
    print(f"  机构总数: {len(ORGANIZATIONS)}")
    print(f"  任职记录: {len(POSITIONS)}")
    print(f"  关系边数: {len(RELATIONSHIPS)}")
    print()
    print("  已确认核心人物:")
    for p in confirmed_persons:
        print(f"    - {p[1]} ({p[9]})")
    print()
    print("  待补充岗位:")
    for p in pending_persons:
        print(f"    - {p[9]}")
    print()
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print("=" * 60)


if __name__ == "__main__":
    build_db()
    build_gexf()
    print_summary()
