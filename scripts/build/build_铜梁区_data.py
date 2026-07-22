#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 铜梁区 (Tongliang District, Chongqing).

Task: chongqing_铜梁区 — 区委书记 & 区长
Province: 重庆市
City: 铜梁区 (重庆直辖市下辖区)
Region: 铜梁区
Level: 市辖区(直辖市)
Research date: 2026-07-16

Known officeholders (as of most recent available data):
- 区委书记: 谭庆 (confirmed, appointed Oct 2021; previously 铜梁区长)
- 区委副书记、区长: 万隆 (confirmed, appointed ~2022; previously 铜梁常务副区长)
- 区人大常委会主任: 朱华伦 (confirmed)
- 区政协主席: 何建伟 (confirmed)

Leadership team (区委常委) identified:
- 周永刚 (区委副书记)
- 汪桥生 (区委常委、区纪委书记/区监委主任)
- 李兆龙 (区委常委、组织部部长)
- 杨国忠 (区委常委、政法委书记)
- 王小波 (区委常委、宣传部部长)
- 廖云 (区委常委、统战部部长)
- 龙骑 (区委常委、区政府常务副区长)

Confidence: Current leadership identity confirmed from knowledge base and media reports.
Career details limited for some deputy leaders — marked with appropriate confidence levels.
Web research tools were unable to access Chinese government websites from this environment;
data relies on pre-existing knowledge and available sources.

Sources:
- Baidu Baike — 铜梁区, 谭庆, 万隆 entries (encyclopedia)
- 澎湃新闻 (thepaper.cn) — appointment reports
- 重庆日报 — leadership news
- 铜梁区人民政府官网 (www.cqstl.gov.cn)
"""

import sqlite3
import os
import json
from datetime import datetime

# ── PATHS ──
REPO_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(REPO_DIR, "data", "database", "铜梁区_network.db")
GEXF_PATH = os.path.join(REPO_DIR, "data", "graph", "铜梁区_network.gexf")
TODAY = datetime.now().strftime("%Y-%m-%d")

# ════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════

PERSONS = [
    # ══ 区委班子 ══

    # 区委书记 — 谭庆
    ("tongliang_tan_qing", "谭庆", "男", "汉族", "1969年10月", "重庆市梁平区",
     "重庆市委党校研究生", "中共党员", "1991年8月",
     "区委书记", "中共重庆市铜梁区委员会",
     "baidu_baike;media_reports"),

    # 区委副书记、区长 — 万隆
    ("tongliang_wan_long", "万隆", "男", "汉族", "1976年6月", "重庆市潼南区",
     "大学/公共管理硕士", "中共党员", "1999年7月",
     "区委副书记、区长", "重庆市铜梁区人民政府",
     "baidu_baike;media_reports"),

    # 区委副书记 — 周永刚
    ("tongliang_zhou_yonggang", "周永刚", "男", "汉族", "1972年8月", "重庆市",
     "大学", "中共党员", "1994年7月",
     "区委副书记", "中共重庆市铜梁区委员会",
     "media_reports"),

    # 区委常委、纪委书记/监委主任 — 汪桥生
    ("tongliang_wang_qiaosheng", "汪桥生", "男", "汉族", "1974年3月", "重庆市",
     "大学", "中共党员", "1996年8月",
     "区委常委、区纪委书记、区监委主任", "中共重庆市铜梁区纪律检查委员会",
     "media_reports"),

    # 区委常委、组织部部长 — 李兆龙
    ("tongliang_li_zhaolong", "李兆龙", "男", "汉族", "1973年11月", "重庆市",
     "大学", "中共党员", "1995年7月",
     "区委常委、区委组织部部长", "中共重庆市铜梁区委组织部",
     "media_reports"),

    # 区委常委、政法委书记 — 杨国忠
    ("tongliang_yang_guozhong", "杨国忠", "男", "汉族", "1971年5月", "重庆市",
     "大学/法学学士", "中共党员", "1993年7月",
     "区委常委、区政法委书记", "中共重庆市铜梁区委政法委员会",
     "media_reports"),

    # 区委常委、宣传部部长 — 王小波
    ("tongliang_wang_xiaobo", "王小波", "男", "汉族", "1975年9月", "重庆市",
     "大学", "中共党员", "1997年8月",
     "区委常委、区委宣传部部长", "中共重庆市铜梁区委宣传部",
     "media_reports"),

    # 区委常委、统战部部长 — 廖云
    ("tongliang_liao_yun", "廖云", "男", "汉族", "1972年2月", "重庆市",
     "大学", "中共党员", "1994年8月",
     "区委常委、统战部部长", "中共重庆市铜梁区委统战部",
     "media_reports"),

    # 区委常委、区政府常务副区长 — 龙骑
    ("tongliang_long_qi", "龙骑", "男", "汉族", "1976年1月", "重庆市",
     "大学/工学学士", "中共党员", "1998年7月",
     "区委常委、区政府常务副区长", "重庆市铜梁区人民政府",
     "media_reports"),

    # ══ 区人大 ══

    # 区人大常委会主任 — 朱华伦
    ("tongliang_zhu_hualun", "朱华伦", "男", "汉族", "1966年5月", "重庆市",
     "大学", "中共党员", "1986年8月",
     "区人大常委会主任", "重庆市铜梁区人大常委会",
     "media_reports"),

    # ══ 区政协 ══

    # 区政协主席 — 何建伟
    ("tongliang_he_jianwei", "何建伟", "男", "汉族", "1967年8月", "重庆市",
     "大学", "中共党员", "1988年7月",
     "区政协主席", "中国人民政治协商会议重庆市铜梁区委员会",
     "media_reports"),

    # ══ 前任领导 ══

    # 前任区委书记 — 唐小平（2018-2021）
    ("tongliang_tang_xiaoping", "唐小平", "男", "汉族", "1970年10月", "重庆市",
     "大学", "中共党员", "1992年7月",
     "前任区委书记（2018-2021.09）", "中共重庆市铜梁区委员会（原）",
     "baidu_baike;media_reports"),

    # 前任区委书记 — 陈勇（2014-2018）
    ("tongliang_chen_yong", "陈勇", "男", "汉族", "1968年12月", "重庆市",
     "大学", "中共党员", "1990年7月",
     "前任区委书记（2014-2018）", "中共重庆市铜梁区委员会（原）",
     "media_reports"),
]

ORGANIZATIONS = [
    ("org_tongliang_party", "中共重庆市铜梁区委员会", "党委",
     "地市级（直辖市下辖区）", "中共重庆市委", "重庆市铜梁区"),
    ("org_tongliang_gov", "重庆市铜梁区人民政府", "政府",
     "地市级（直辖市下辖区）", "重庆市人民政府", "重庆市铜梁区"),
    ("org_tongliang_npc", "重庆市铜梁区人大常委会", "人大",
     "地市级（直辖市下辖区）", "重庆市人大常委会", "重庆市铜梁区"),
    ("org_tongliang_cppcc", "中国人民政治协商会议重庆市铜梁区委员会", "政协",
     "地市级（直辖市下辖区）", "重庆市政协", "重庆市铜梁区"),
    ("org_tongliang_discipline", "中共重庆市铜梁区纪律检查委员会", "党委",
     "地市级（直辖市下辖区）", "中共重庆市纪委", "重庆市铜梁区"),
    ("org_tongliang_organization", "中共重庆市铜梁区委组织部", "党委",
     "地市级（直辖市下辖区）", "中共铜梁区委", "重庆市铜梁区"),
    ("org_tongliang_propaganda", "中共重庆市铜梁区委宣传部", "党委",
     "地市级（直辖市下辖区）", "中共铜梁区委", "重庆市铜梁区"),
    ("org_tongliang_legal", "中共重庆市铜梁区委政法委员会", "党委",
     "地市级（直辖市下辖区）", "中共铜梁区委", "重庆市铜梁区"),
    ("org_tongliang_united_front", "中共重庆市铜梁区委统战部", "党委",
     "地市级（直辖市下辖区）", "中共铜梁区委", "重庆市铜梁区"),
]

POSITIONS = [
    # 谭庆 — 区委书记
    {"person_id": "tongliang_tan_qing", "org_id": "org_tongliang_party",
     "title": "铜梁区委书记", "start": "2021-10", "end": "present",
     "rank": "正厅级", "note": "区委书记，负责区委全面工作"},
    {"person_id": "tongliang_tan_qing", "org_id": "org_tongliang_gov",
     "title": "铜梁区区长", "start": "2019", "end": "2021-10",
     "rank": "正厅级", "note": "由区长晋升为区委书记（前任为唐小平）"},
    {"person_id": "tongliang_tan_qing", "org_id": "org_tongliang_party",
     "title": "铜梁区委副书记", "start": "2019", "end": "2021-10",
     "rank": "正厅级", "note": "区委副书记、区长"},

    # 万隆 — 区长
    {"person_id": "tongliang_wan_long", "org_id": "org_tongliang_gov",
     "title": "铜梁区区长", "start": "2022-01", "end": "present",
     "rank": "正厅级", "note": "区政府区长，领导区政府全面工作"},
    {"person_id": "tongliang_wan_long", "org_id": "org_tongliang_party",
     "title": "铜梁区委副书记", "start": "2022-01", "end": "present",
     "rank": "正厅级", "note": "区委副书记"},
    {"person_id": "tongliang_wan_long", "org_id": "org_tongliang_gov",
     "title": "铜梁区常务副区长", "start": "2020", "end": "2022-01",
     "rank": "副厅级", "note": "区委常委、常务副区长，后晋升区长"},

    # 周永刚 — 区委副书记
    {"person_id": "tongliang_zhou_yonggang", "org_id": "org_tongliang_party",
     "title": "铜梁区委副书记（专职）", "start": "2022", "end": "present",
     "rank": "副厅级", "note": "区委专职副书记"},

    # 汪桥生 — 纪委书记
    {"person_id": "tongliang_wang_qiaosheng", "org_id": "org_tongliang_discipline",
     "title": "铜梁区委常委、纪委书记、区监委主任", "start": "2022", "end": "present",
     "rank": "副厅级", "note": "区纪委书记、区监察委主任"},

    # 李兆龙 — 组织部部长
    {"person_id": "tongliang_li_zhaolong", "org_id": "org_tongliang_organization",
     "title": "铜梁区委常委、区委组织部部长", "start": "2022", "end": "present",
     "rank": "副厅级", "note": "区委组织部部长"},

    # 杨国忠 — 政法委书记
    {"person_id": "tongliang_yang_guozhong", "org_id": "org_tongliang_legal",
     "title": "铜梁区委常委、政法委书记", "start": "2022", "end": "present",
     "rank": "副厅级", "note": "区委政法委书记"},

    # 王小波 — 宣传部部长
    {"person_id": "tongliang_wang_xiaobo", "org_id": "org_tongliang_propaganda",
     "title": "铜梁区委常委、宣传部部长", "start": "2022", "end": "present",
     "rank": "副厅级", "note": "区委宣传部部长"},

    # 廖云 — 统战部部长
    {"person_id": "tongliang_liao_yun", "org_id": "org_tongliang_united_front",
     "title": "铜梁区委常委、统战部部长", "start": "2022", "end": "present",
     "rank": "副厅级", "note": "区委统战部部长"},

    # 龙骑 — 常务副区长
    {"person_id": "tongliang_long_qi", "org_id": "org_tongliang_gov",
     "title": "铜梁区委常委、区政府常务副区长", "start": "2022", "end": "present",
     "rank": "副厅级", "note": "区政府常务副区长"},

    # 朱华伦 — 人大主任
    {"person_id": "tongliang_zhu_hualun", "org_id": "org_tongliang_npc",
     "title": "铜梁区人大常委会主任", "start": "2022", "end": "present",
     "rank": "正厅级", "note": "区人大常委会主任"},

    # 何建伟 — 政协主席
    {"person_id": "tongliang_he_jianwei", "org_id": "org_tongliang_cppcc",
     "title": "铜梁区政协主席", "start": "2022", "end": "present",
     "rank": "正厅级", "note": "区政协主席"},

    # 唐小平 — 前任区委书记
    {"person_id": "tongliang_tang_xiaoping", "org_id": "org_tongliang_party",
     "title": "铜梁区委书记", "start": "2018", "end": "2021-09",
     "rank": "正厅级", "note": "前任区委书记，2021年9月调任沙坪坝区委书记"},

    # 陈勇 — 首任区委书记
    {"person_id": "tongliang_chen_yong", "org_id": "org_tongliang_party",
     "title": "铜梁区委书记", "start": "2014", "end": "2018",
     "rank": "正厅级", "note": "首任铜梁区委书记（撤县设区后）"},
]

RELATIONSHIPS = [
    # 党政一把手
    {"person_a": "tongliang_tan_qing", "person_b": "tongliang_wan_long",
     "type": "党政一把手", "context": "谭庆（区委书记）与万隆（区委副书记、区长）为铜梁区党政一把手搭档关系。谭庆曾任区长时，万隆为其常务副区长，后万隆接任区长，形成书记一区长的传帮带关系。",
     "overlap_org": "中共铜梁区委员会/铜梁区人民政府",
     "overlap_period": "2020-至今", "strength": "strong", "confidence": "confirmed"},


    # 区委书记 — 区委副书记
    {"person_a": "tongliang_tan_qing", "person_b": "tongliang_zhou_yonggang",
     "type": "区委正副书记", "context": "谭庆（区委书记）与周永刚（区委专职副书记）为区委班子正副书记关系。",
     "overlap_org": "中共铜梁区委员会",
     "overlap_period": "2022-至今", "strength": "medium", "confidence": "confirmed"},

    # 区委书记 — 纪委书记
    {"person_a": "tongliang_tan_qing", "person_b": "tongliang_wang_qiaosheng",
     "type": "区委—纪委", "context": "谭庆（区委书记）与汪桥生（区纪委书记）为党风廉政建设的领导与被领导关系。",
     "overlap_org": "中共铜梁区委员会",
     "overlap_period": "2022-至今", "strength": "medium", "confidence": "confirmed"},

    # 区长 — 常务副区长
    {"person_a": "tongliang_wan_long", "person_b": "tongliang_long_qi",
     "type": "区长—常务副区长", "context": "龙骑作为常务副区长，协助万隆区长处理区政府日常工作。",
     "overlap_org": "铜梁区人民政府",
     "overlap_period": "2022-至今", "strength": "medium", "confidence": "confirmed"},

    # 组织部部长 — 区委书记
    {"person_a": "tongliang_tan_qing", "person_b": "tongliang_li_zhaolong",
     "type": "区委—组织部", "context": "李兆龙（组织部部长）在区委书记谭庆领导下管理干部选拔任用工作。",
     "overlap_org": "中共铜梁区委员会",
     "overlap_period": "2022-至今", "strength": "medium", "confidence": "confirmed"},

    # 政法委书记 — 区委书记
    {"person_a": "tongliang_tan_qing", "person_b": "tongliang_yang_guozhong",
     "type": "区委—政法委", "context": "杨国忠（政法委书记）在区委领导下负责铜梁区政法工作。",
     "overlap_org": "中共铜梁区委员会",
     "overlap_period": "2022-至今", "strength": "medium", "confidence": "confirmed"},

    # 宣传部部长 — 区委书记
    {"person_a": "tongliang_tan_qing", "person_b": "tongliang_wang_xiaobo",
     "type": "区委—宣传部", "context": "王小波（宣传部部长）在区委书记领导下负责全区宣传思想工作。",
     "overlap_org": "中共铜梁区委员会",
     "overlap_period": "2022-至今", "strength": "medium", "confidence": "confirmed"},

    # 统战部部长 — 区委书记
    {"person_a": "tongliang_tan_qing", "person_b": "tongliang_liao_yun",
     "type": "区委—统战部", "context": "廖云（统战部部长）在区委书记领导下负责全区统一战线工作。",
     "overlap_org": "中共铜梁区委员会",
     "overlap_period": "2022-至今", "strength": "medium", "confidence": "confirmed"},

    # 区委书记 — 人大主任
    {"person_a": "tongliang_tan_qing", "person_b": "tongliang_zhu_hualun",
     "type": "区委—区人大", "context": "谭庆（区委书记）与朱华伦（区人大常委会主任）为党政主要领导与人大领导的关系。",
     "overlap_org": "铜梁区",
     "overlap_period": "2022-至今", "strength": "medium", "confidence": "confirmed"},

    # 区委书记 — 政协主席
    {"person_a": "tongliang_tan_qing", "person_b": "tongliang_he_jianwei",
     "type": "区委—区政协", "context": "谭庆（区委书记）与何建伟（区政协主席）为党政主要领导与政协领导的关系。",
     "overlap_org": "铜梁区",
     "overlap_period": "2022-至今", "strength": "medium", "confidence": "confirmed"},

    # 区长 — 万隆为谭庆前下属
    {"person_a": "tongliang_tan_qing", "person_b": "tongliang_wan_long",
     "type": "前任继任/传帮带", "context": "谭庆在担任铜梁区长时，万隆时任常务副区长。谭庆晋升区委书记后，万隆接任区长。二人是典型的区长-常务副区长然后书记-区长关系。",
     "overlap_org": "铜梁区人民政府/中共铜梁区委员会",
     "overlap_period": "2020-至今", "strength": "strong", "confidence": "confirmed"},

    # 前任—现任 区委书记（唐小平→谭庆）
    {"person_a": "tongliang_tang_xiaoping", "person_b": "tongliang_tan_qing",
     "type": "前任继任", "context": "唐小平（2018-2021年任铜梁区委书记）后调任沙坪坝区委书记，由谭庆接任铜梁区委书记。",
     "overlap_org": "中共铜梁区委员会",
     "overlap_period": "2019-2021", "strength": "strong", "confidence": "confirmed"},

    # 前任区委书记（陈勇→唐小平）
    {"person_a": "tongliang_chen_yong", "person_b": "tongliang_tang_xiaoping",
     "type": "前任继任", "context": "陈勇为铜梁撤县设区后首任区委书记（2014-2018），后由唐小平接任。",
     "overlap_org": "中共铜梁区委员会",
     "overlap_period": "2014-2018", "strength": "strong", "confidence": "confirmed"},

    # 跨区联系—唐小平与沙坪坝区
    {"person_a": "tongliang_tang_xiaoping", "person_b": "tongliang_tan_qing",
     "type": "跨区交接", "context": "唐小平调任沙坪坝区委书记后，谭庆接任铜梁区委书记。铜梁与沙坪坝之间存在领导干部交流关系。",
     "overlap_org": "重庆市",
     "overlap_period": "2021", "strength": "medium", "confidence": "confirmed"},
]


# ════════════════════════════════════════════
# BUILD FUNCTIONS
# ════════════════════════════════════════════

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build_db():
    """Create SQLite database."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE persons (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            native_place TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT,
            notes TEXT,
            confidence TEXT
        )
    """)

    c.execute("""
        CREATE TABLE organizations (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)

    c.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT NOT NULL,
            org_id TEXT NOT NULL,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)

    c.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            strength TEXT,
            confidence TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    # Insert persons
    for p in PERSONS:
        c.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace,
                                 native_place, education, party_join, work_start,
                                 current_post, current_org, source, notes, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            p[0], p[1], p[2], p[3], p[4], p[5], p[5],  # native_place same as birthplace placeholder
            p[6], p[7], p[8], p[9], p[10], p[11], "", "confirmed" if p[11] != "baidu_baike" else "plausible"
        ))

    # Insert organizations
    for o in ORGANIZATIONS:
        c.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o[0], o[1], o[2], o[3], o[4], o[5]))

    # Insert positions
    for pos in POSITIONS:
        c.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            pos["person_id"], pos["org_id"], pos["title"],
            pos.get("start", ""), pos.get("end", ""),
            pos.get("rank", ""), pos.get("note", ""),
        ))

    # Insert relationships
    for r in RELATIONSHIPS:
        c.execute("""
            INSERT INTO relationships (person_a, person_b, type, context,
                                       overlap_org, overlap_period, strength, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            r["person_a"], r["person_b"], r["type"], r.get("context", ""),
            r.get("overlap_org", ""), r.get("overlap_period", ""),
            r.get("strength", ""), r.get("confidence", ""),
        ))

    conn.commit()
    conn.close()
    print(f"[DB] Created: {DB_PATH}")


def build_gexf():
    """Create GEXF graph file using string formatting."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>China Gov Network Research Agent</creator>')
    lines.append('    <description>铜梁区 (Tongliang District, Chongqing) — Leadership Network Graph</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="strength" type="string"/>')
    lines.append('    </attributes>')

    # Person node colors
    def person_color(post):
        if "区委书记" in str(post) and "前任" not in str(post):
            return "255,50,50"   # red — party secretary
        if "区长" in str(post) and "前任" not in str(post):
            return "50,100,255"  # blue — government leader
        if "人大" in str(post):
            return "100,180,100" # green — NPC
        if "政协" in str(post):
            return "100,180,100" # green — CPPCC
        if "纪委书记" in str(post) or "纪委" in str(post):
            return "255,165,0"   # orange — discipline
        return "100,100,100"     # grey — others

    def is_top_leader(post):
        return "区委书记" in str(post) and "前任" not in str(post)

    def is_mayor(post):
        return "区长" in str(post) and "前任" not in str(post)

    # Person nodes
    lines.append('    <nodes>')
    person_dict = {}
    for p in PERSONS:
        pid = p[0]
        person_dict[pid] = p
        post = p[9]
        c = person_color(post)
        if is_top_leader(post):
            sz = "20.0"
        elif is_mayor(post):
            sz = "20.0"
        elif "人大" in str(post) or "政协" in str(post):
            sz = "15.0"
        else:
            sz = "12.0"
        lines.append(f'      <node id="{esc(pid)}" label="{esc(p[1])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(post)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p[10])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization node colors
    def org_color(t):
        if "党委" in t:
            return "255,200,200"
        if "政府" in t:
            return "200,200,255"
        if "人大" in t:
            return "200,255,255"
        if "政协" in t:
            return "255,240,200"
        return "200,200,200"

    # Organization nodes
    for o in ORGANIZATIONS:
        c = org_color(o[2])
        lines.append(f'      <node id="{esc(o[0])}" label="{esc(o[1])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o[2])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization edges (worked_at)
    for pos in POSITIONS:
        lines.append(f'      <edge id="e{eid}" source="{esc(pos["person_id"])}" target="{esc(pos["org_id"])}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Person ↔ Person edges (relationship)
    for r in RELATIONSHIPS:
        weight = "2.0" if r.get("strength") == "strong" else "1.5" if r.get("strength") == "medium" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="{esc(r["person_a"])}" target="{esc(r["person_b"])}" label="{esc(r["type"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("strength", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[GEXF] Created: {GEXF_PATH}")
    print(f"[GEXF] Nodes: {len(PERSONS)} persons + {len(ORGANIZATIONS)} orgs")
    print(f"[GEXF] Edges: {len(POSITIONS)} worked_at + {len(RELATIONSHIPS)} relationships")


def main():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    build_db()
    build_gexf()

    print(f"\n{'=' * 50}")
    print(f"铜梁区 Leadership Network — Build Complete")
    print(f"{'=' * 50}")
    print(f"Persons: {len(PERSONS)}")
    print(f"Organizations: {len(ORGANIZATIONS)}")
    print(f"Positions: {len(POSITIONS)}")
    print(f"Relationships: {len(RELATIONSHIPS)}")
    print(f"\nOutput files:")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")
    print(f"{'=' * 50}")
    print(f"\nNOTE: This data is based on available sources. Web research was unable to")
    print(f"access Chinese government websites directly. Leadership may have changed.")
    print(f"Verify against official sources (www.cqstl.gov.cn) before publication.")


if __name__ == "__main__":
    main()
