#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 大庆市 (Daqing), 黑龙江省.

Task ID: heilongjiang_大庆市
Level: 地级市
Targets: 市委书记 & 市长
Investigation date: 2026-08-05

Primary source: 大庆市人民政府 领导之窗 (www.daqing.gov.cn) — official current leadership roster
+ individual bio pages:
- 市委领导: /daqing/c100349/ldzc.shtml
- 市政府领导: /daqing/c100353/ldzc.shtml
- 李世峰: /daqing/c100350/202107/c05_75313.shtml
- 李岩松: /daqing/c100351/202104/c05_81509.shtml (市委) & /daqing/c100354/202108/c05_87279.shtml (政府)
- 孙永刚: /daqing/c100351/202412/c05_365328.shtml
- 罗海涛: /daqing/c100352/202412/c05_365535.shtml
- 朱德锋: /daqing/c100352/202506/c05_381998.shtml
- 王绪新: /daqing/c100352/202211/c05_87495.shtml
- 徐童: /daqing/c100352/202511/c05_396579.shtml
- 韩云: /daqing/c100352/202407/c05_345857.shtml & /daqing/c100355/202407/c05_345859.shtml
- 孙坤: /daqing/c100352/202507/c05_384143.shtml & /daqing/c100355/202409/c05_353334.shtml
- 邹发林: /daqing/c100352/202606/c05_414271.shtml
- 朱清霞: /daqing/c100355/202009/c05_87281.shtml
- 杨春发: /daqing/c100355/202606/c05_414201.shtml
- 张雨: /daqing/c100355/202604/c05_408492.shtml
- 吕航: /daqing/c100355/202411/c05_360444.shtml
- 卜启军: /daqing/c100355/202607/c05_416358.shtml
- 田震: /daqing/c100355/202507/c05_383233.shtml
- 徐东伟: /daqing/c100356/202103/c05_87289.shtml

Confidence notes:
- 班子名单: confirmed (official 领导之窗 + 个人简介页)。
- 姓名/性别/民族/职务分工: confirmed (官网逐人页面)。
- 出生年月、籍贯、教育、入党时间、任职起止: 官网个人页未展示，网络降级无法补全 → open_questions。
- 李世峰（书记）、李岩松（市长）核心主官的任前完整履历未证 → open_questions，不臆造。
- 前任市委书记/市长身份与去向未确认。
- Web 环境退化：Exa 限流、百度百科安全验证、搜狗/人网/Jina/澎湃不可达。采用官网一手来源。
"""

import json
import os
from datetime import datetime
from pathlib import Path

BASE = os.path.dirname(os.path.abspath(__file__))
SLUG = "大庆市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-05"

DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")
PERSONS_DIR = Path(BASE)

LDZC_SW = "https://www.daqing.gov.cn/daqing/c100349/ldzc.shtml"
LDZC_ZF = "https://www.daqing.gov.cn/daqing/c100353/ldzc.shtml"

# ══════════════════════════════════════════════════════════════════════════
# Data
# ══════════════════════════════════════════════════════════════════════════

persons = [
    # ── 市委核心 ──
    {"id": 1, "name": "李世峰", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "", "current_post": "市委书记",
     "current_org": "中共大庆市委员会", "source": "https://www.daqing.gov.cn/daqing/c100350/202107/c05_75313.shtml"},
    {"id": 2, "name": "李岩松", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "", "current_post": "市委副书记、市长",
     "current_org": "大庆市人民政府", "source": "https://www.daqing.gov.cn/daqing/c100354/202108/c05_87279.shtml"},
    {"id": 3, "name": "孙永刚", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "", "current_post": "市委副书记、政法委书记",
     "current_org": "中共大庆市委员会", "source": "https://www.daqing.gov.cn/daqing/c100351/202412/c05_365328.shtml"},
    {"id": 4, "name": "罗海涛", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "", "current_post": "市委常委、宣传部部长",
     "current_org": "中共大庆市委员会", "source": "https://www.daqing.gov.cn/daqing/c100352/202412/c05_365535.shtml"},
    {"id": 5, "name": "朱德锋", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "", "current_post": "市委常委、纪委书记、监委主任",
     "current_org": "中共大庆市纪律检查委员会", "source": "https://www.daqing.gov.cn/daqing/c100352/202506/c05_381998.shtml"},
    {"id": 6, "name": "王绪新", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "", "current_post": "市委常委、组织部部长",
     "current_org": "中共大庆市委员会", "source": "https://www.daqing.gov.cn/daqing/c100352/202211/c05_87495.shtml"},
    {"id": 7, "name": "徐童", "gender": "女", "ethnicity": "锡伯族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "", "current_post": "市委常委、统战部部长",
     "current_org": "中共大庆市委员会", "source": "https://www.daqing.gov.cn/daqing/c100352/202511/c05_396579.shtml"},
    {"id": 8, "name": "韩云", "gender": "男", "ethnicity": "朝鲜族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "", "current_post": "市委常委、常务副市长",
     "current_org": "大庆市人民政府", "source": "https://www.daqing.gov.cn/daqing/c100355/202407/c05_345859.shtml"},
    {"id": 9, "name": "孙坤", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "", "current_post": "市委常委、副市长",
     "current_org": "大庆市人民政府", "source": "https://www.daqing.gov.cn/daqing/c100355/202409/c05_353334.shtml"},
    {"id": 10, "name": "邹发林", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "", "current_post": "市委常委、大庆军分区司令员",
     "current_org": "中国人民解放军大庆军分区", "source": "https://www.daqing.gov.cn/daqing/c100352/202606/c05_414271.shtml"},

    # ── 市政府（其余副市长 + 秘书长）──
    {"id": 11, "name": "朱清霞", "gender": "女", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "", "current_post": "市政府副市长",
     "current_org": "大庆市人民政府", "source": "https://www.daqing.gov.cn/daqing/c100355/202009/c05_87281.shtml"},
    {"id": 12, "name": "杨春发", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "", "current_post": "市政府副市长",
     "current_org": "大庆市人民政府", "source": "https://www.daqing.gov.cn/daqing/c100355/202606/c05_414201.shtml"},
    {"id": 13, "name": "张雨", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "", "current_post": "市政府副市长",
     "current_org": "大庆市人民政府", "source": "https://www.daqing.gov.cn/daqing/c100355/202604/c05_408492.shtml"},
    {"id": 14, "name": "吕航", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "", "current_post": "市政府副市长",
     "current_org": "大庆市人民政府", "source": "https://www.daqing.gov.cn/daqing/c100355/202411/c05_360444.shtml"},
    {"id": 15, "name": "卜启军", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "", "current_post": "市政府副市长、市公安局局长",
     "current_org": "大庆市公安局", "source": "https://www.daqing.gov.cn/daqing/c100355/202607/c05_416358.shtml"},
    {"id": 16, "name": "田震", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "", "current_post": "市政府副市长",
     "current_org": "大庆市人民政府", "source": "https://www.daqing.gov.cn/daqing/c100355/202507/c05_383233.shtml"},
    {"id": 17, "name": "徐东伟", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "", "current_post": "市政府秘书长",
     "current_org": "大庆市人民政府", "source": "https://www.daqing.gov.cn/daqing/c100356/202103/c05_87289.shtml"},
]

organizations = [
    {"id": 1, "name": "中共大庆市委员会", "type": "党委", "level": "地级", "parent": "中共黑龙江省委员会", "location": "大庆市"},
    {"id": 2, "name": "大庆市人民政府", "type": "政府", "level": "地级", "parent": "黑龙江省人民政府", "location": "大庆市"},
    {"id": 3, "name": "中共大庆市纪律检查委员会", "type": "纪检监察", "level": "地级", "parent": "中共黑龙江省纪律检查委员会", "location": "大庆市"},
    {"id": 4, "name": "中国人民政治协商会议大庆市委员会", "type": "政协", "level": "地级", "parent": "中国人民政治协商会议黑龙江省委员会", "location": "大庆市"},
    {"id": 5, "name": "大庆市公安局", "type": "政府", "level": "地级", "parent": "大庆市人民政府", "location": "大庆市"},
    {"id": 6, "name": "中国人民解放军大庆军分区", "type": "军队", "level": "地级", "parent": "", "location": "大庆市"},
    {"id": 7, "name": "中共黑龙江省委员会", "type": "党委", "level": "省级", "parent": "", "location": "哈尔滨市"},
    {"id": 8, "name": "黑龙江省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "哈尔滨市"},
    {"id": 9, "name": "大庆油田有限责任公司（大庆油田）", "type": "国有大型企业", "level": "企业", "parent": "中国石油天然气集团有限公司", "location": "大庆市"},
]

positions = [
    # 李世峰 (1)
    {"person_id": 1, "org_id": 1, "title": "大庆市委书记", "start": "", "end": "present", "rank": "副省级（正厅级）", "note": "现任市委书记；官方个人页2021-07发布，显示此时已任书记；任命年月待核"},
    {"person_id": 1, "org_id": 7, "title": "大庆市委书记前任职（待核）", "start": "", "end": "", "rank": "", "note": "任职元年与前任职务未公开确认→open_questions"},

    # 李岩松 (2)
    {"person_id": 2, "org_id": 1, "title": "大庆市委副书记", "start": "", "end": "present", "rank": "正厅级", "note": "现任市委副书记（官方2021-04简介起）"},
    {"person_id": 2, "org_id": 2, "title": "大庆市市长、市政府党组书记", "start": "", "end": "present", "rank": "正厅级", "note": "主持市政府全面工作，分管市审计局；官方2024-12简介确认"},
    {"person_id": 2, "org_id": 8, "title": "市长任前职务（待核）", "start": "", "end": "", "rank": "", "note": "任市长前履历未确认→open_questions"},

    # 孙永刚 (3)
    {"person_id": 3, "org_id": 1, "title": "大庆市委副书记、政法委书记", "start": "", "end": "present", "rank": "副厅级", "note": "现任（官方2024-12）"},
    {"person_id": 3, "org_id": 2, "title": "政法委（市政府/法务系统关联）", "start": "", "end": "present", "rank": "", "note": "分管政法系统"},

    # 罗海涛 (4)
    {"person_id": 4, "org_id": 1, "title": "大庆市委常委、宣传部部长", "start": "", "end": "present", "rank": "副厅级", "note": "现任（官方2024-12）"},

    # 朱德锋 (5)
    {"person_id": 5, "org_id": 3, "title": "大庆市委常委、纪委书记、监委主任", "start": "", "end": "present", "rank": "副厅级", "note": "现任；二级高级监察官"},

    # 王绪新 (6)
    {"person_id": 6, "org_id": 1, "title": "大庆市委常委、组织部部长", "start": "", "end": "present", "rank": "副厅级", "note": "现任（官方2022-11）"},

    # 徐童 (7)
    {"person_id": 7, "org_id": 1, "title": "大庆市委常委、统战部部长", "start": "", "end": "present", "rank": "副厅级", "note": "现任；兼市政协党组副书记（官方2025-11）"},
    {"person_id": 7, "org_id": 4, "title": "大庆市政协党组副书记（兼）", "start": "", "end": "present", "rank": "", "note": "兼任"},

    # 韩云 (8)
    {"person_id": 8, "org_id": 2, "title": "大庆市委常委、常务副市长(党组副书记)", "start": "", "end": "present", "rank": "副厅级", "note": "分管市政府常务工作、综合经济、地企合作、安全生产；协助分管审计"},
    {"person_id": 8, "org_id": 1, "title": "大庆市委常委", "start": "", "end": "present", "rank": "副厅级", "note": "市委班子（官方2024-07）"},

    # 孙坤 (9)
    {"person_id": 9, "org_id": 2, "title": "大庆市委常委、副市长", "start": "", "end": "present", "rank": "副厅级", "note": "现任（官方2025-07）"},
    {"person_id": 9, "org_id": 1, "title": "大庆市委常委", "start": "", "end": "present", "rank": "副厅级", "note": "市委班子"},

    # 邹发林 (10)
    {"person_id": 10, "org_id": 6, "title": "大庆市委常委、大庆军分区司令员", "start": "", "end": "present", "rank": "副厅级", "note": "现任（官方2026-06）"},

    # 朱清霞 (11)
    {"person_id": 11, "org_id": 2, "title": "大庆副市长、农工党大庆市委主委", "start": "", "end": "present", "rank": "副厅级", "note": "分管文教卫生（教育局/卫健委/医保局）"},

    # 杨春发 (12)
    {"person_id": 12, "org_id": 2, "title": "大庆副市长、党组成员", "start": "", "end": "present", "rank": "副厅级", "note": "分管退役军人、外事"},

    # 张雨 (13)
    {"person_id": 13, "org_id": 2, "title": "大庆副市长、党组成员", "start": "", "end": "present", "rank": "副厅级", "note": "现任；分工详情待核"},

    # 吕航 (14)
    {"person_id": 14, "org_id": 2, "title": "大庆副市长、党组成员", "start": "", "end": "present", "rank": "副厅级", "note": "分管民政、自然资源、交通运输、市场监管"},

    # 卜启军 (15)
    {"person_id": 15, "org_id": 5, "title": "大庆市公安局局长、党委书记、督察长", "start": "", "end": "present", "rank": "副厅级", "note": "兼市政府副市长、市委政法委副书记"},
    {"person_id": 15, "org_id": 2, "title": "大庆副市长、党组成员", "start": "", "end": "present", "rank": "副厅级", "note": "负责公共安全工作，分管市公安局、市司法局"},

    # 田震 (16)
    {"person_id": 16, "org_id": 2, "title": "大庆副市长、党组成员", "start": "", "end": "present", "rank": "副厅级", "note": "分管人社、城乡建设、生态环境"},

    # 徐东伟 (17)
    {"person_id": 17, "org_id": 2, "title": "大庆市政府秘书长、党组成员", "start": "", "end": "present", "rank": "正处级/副厅级", "note": "协助李瑞市长、韩云常务副市长处理市政府机关日常工作"},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "李世峰（市委书记）与李岩松（市长、市委副书记）为现行党政一把手搭档",
     "overlap_org": "大庆市党政班子", "overlap_period": "近年来（李岩松任市长起）"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "李世峰（书记）与孙永刚（副书记、政法委书记）党委班子搭档",
     "overlap_org": "中共大庆市委员会", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "李世峰（书记）与朱德锋（纪委书记）同级党委班子内上下级纪检监督关系",
     "overlap_org": "中共大庆市委员会", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "李世峰（书记）与王绪新（组织部长）党委班子搭档",
     "overlap_org": "中共大庆市委员会", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate",
     "context": "李岩松（市长）与韩云（常务副市长）政府班子正副职搭档",
     "overlap_org": "大庆市人民政府", "overlap_period": "现任（韩云任常务副市长起）"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate",
     "context": "李岩松（市长）与孙坤（市委常委、副市长）政府班子搭档",
     "overlap_org": "大庆市人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate",
     "context": "李岩松（市长）与卜启军（副市长、公安局长）政府班子上下级",
     "overlap_org": "大庆市人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate",
     "context": "李岩松（市长）与朱清霞（副市长）政府班子搭档",
     "overlap_org": "大庆市人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 17, "type": "superior_subordinate",
     "context": "李岩松（市长）与徐东伟（秘书长，协助市长）密切工作搭档",
     "overlap_org": "大庆市人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 16, "type": "superior_subordinate",
     "context": "李岩松（市长）与田震（副市长）政府班子搭档",
     "overlap_org": "大庆市人民政府", "overlap_period": "现任"},
    {"person_a": 8, "person_b": 2, "type": "superior_subordinate",
     "context": "韩云（常务副市长）协助李岩松（市长）分管市审计局",
     "overlap_org": "大庆市人民政府", "overlap_period": "现任"},
]


# ══════════════════════════════════════════════════════════════════════════
# XML helper
# ══════════════════════════════════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


# ══════════════════════════════════════════════════════════════════════════
# Database
# ══════════════════════════════════════════════════════════════════════════

def build_db():
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS persons;
        DROP TABLE IF EXISTS organizations;
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        );
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER, org_id INTEGER,
            title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id), FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT, person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id), FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)
    for p in persons:
        cur.execute("INSERT INTO persons (id,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                    (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"],
                     p["education"], p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]))
    for o in organizations:
        cur.execute("INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)",
                    (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))
    for pos in positions:
        cur.execute("INSERT INTO positions (person_id,org_id,title,start,end,rank,note) VALUES (?,?,?,?,?,?,?)",
                    (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))
    for r in relationships:
        cur.execute("INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)",
                    (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))
    conn.commit()
    conn.close()
    print(f"  DB: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")


# ══════════════════════════════════════════════════════════════════════════
# GEXF
# ══════════════════════════════════════════════════════════════════════════

def person_color(name):
    if name in ("李世峰",):
        return "255,50,50"        # 市委书记 — 红
    if name == "李岩松":
        return "50,100,255"       # 市长 — 蓝
    if name in ("孙永刚",):
        return "255,165,0"        # 副书记 — 橙
    if name in ("朱德锋",):
        return "255,165,0"        # 纪委书记 — 橙
    if name in ("徐童",):
        return "255,220,255"      # 统战/党外 — 浅紫
    if name in ("罗海涛", "王绪新"):
        return "150,150,255"      # 宣传/组织 — 紫蓝
    if name in ("朱清霞",):
        return "150,230,150"      # 非党干部 — 绿
    return "100,100,100"          # 其他 — 灰


def person_size(name):
    if name in ("李世峰", "李岩松"):
        return "20.0"
    if name == "孙永刚":
        return "15.0"
    return "12.0"


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>china-gov-network research agent</creator>')
    lines.append('    <description>大庆市（黑龙江省，地级市）领导班子工作关系网络，2026-08-05</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p["name"]); sz = person_size(p["name"])
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    for o in organizations:
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append('        <viz:color r="200" g="200" b="200"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1
    for r in relationships:
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1
    lines.append('    </edges>')

    lines.append('  </graph>')
    lines.append('</gexf>')
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  OK GEXF: {len(persons)} person nodes, {len(organizations)} org nodes, {len(positions)+len(relationships)} edges")


# ══════════════════════════════════════════════════════════════════════════
# Person JSON
# ══════════════════════════════════════════════════════════════════════════

SOURCES = [
    {"id": "S001", "title": "大庆市人民政府——市委领导", "url": LDZC_SW,
     "publisher": "大庆市人民政府", "published_at": "", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "现任市委班子名单"},
    {"id": "S002", "title": "大庆市人民政府——市政府领导", "url": LDZC_ZF,
     "publisher": "大庆市人民政府", "published_at": "", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "现任市政府班子名单"},
    {"id": "S003", "title": "李世峰——领导简介", "url": "https://www.daqing.gov.cn/daqing/c100350/202107/c05_75313.shtml",
     "publisher": "大庆市人民政府", "published_at": "2021-07-03", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "市委书记简介（官方当前版本）"},
    {"id": "S004", "title": "李岩松——领导简介（市政府）", "url": "https://www.daqing.gov.cn/daqing/c100354/202108/c05_87279.shtml",
     "publisher": "大庆市人民政府", "published_at": "", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "市长简介"},
    {"id": "S005", "title": "孙永刚——领导简介", "url": "https://www.daqing.gov.cn/daqing/c100351/202412/c05_365328.shtml",
     "publisher": "大庆市委办公室", "published_at": "2024-12-31", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "市委副书记、政法委书记"},
    {"id": "S006", "title": "韩云——领导简介（市政府）", "url": "https://www.daqing.gov.cn/daqing/c100355/202407/c05_345859.shtml",
     "publisher": "大庆市人民政府", "published_at": "2024-07", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "常务副市长、党组副书记"},
    {"id": "S007", "title": "卜启军——领导简介", "url": "https://www.daqing.gov.cn/daqing/c100355/202607/c05_416358.shtml",
     "publisher": "大庆市人民政府", "published_at": "2026-07-20", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "副市长、市公安局局长"},
    {"id": "S008", "title": "罗海涛——领导简介", "url": "https://www.daqing.gov.cn/daqing/c100352/202412/c05_365535.shtml",
     "publisher": "大庆市人民政府", "published_at": "2024-12", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "市委常委、宣传部部长"},
    {"id": "S009", "title": "徐童——领导简介", "url": "https://www.daqing.gov.cn/daqing/c100352/202511/c05_396579.shtml",
     "publisher": "大庆市人民政府", "published_at": "2025-11", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "市委常委、统战部长（女，锡伯族）"},
    {"id": "S010", "title": "朱德锋——领导简介", "url": "https://www.daqing.gov.cn/daqing/c100352/202506/c05_381998.shtml",
     "publisher": "大庆市人民政府", "published_at": "2026-06-22", "accessed_at": AS_OF,
     "source_type": "official", "reliability": "high", "notes": "市委常委、纪委书记、监委主任"},
]

# 各人来源
PERSON_SOURCE = {
    1: ["S001", "S003"], 2: ["S001", "S002", "S004"], 3: ["S001", "S005"],
    4: ["S001", "S008"], 5: ["S001", "S010"], 6: ["S001"], 7: ["S001", "S009"],
    8: ["S001", "S006"], 9: ["S001", "S002"], 10: ["S001"], 11: ["S002"],
    12: ["S002"], 13: ["S002"], 14: ["S002"], 15: ["S002", "S007"], 16: ["S002"], 17: ["S002"],
}
GOV_NAME = {1, 2, 8, 9, 11, 12, 13, 14, 15, 16, 17}


def person_json(p):
    is_top = p["id"] in (1, 2)
    is_core = p["id"] in (1, 2, 3, 8, 15)
    rank = "正厅级" if p["id"] in (1, 2, 3) else "副厅级"
    if p["id"] in (17,):
        rank = "正处级"
    url = p["source"]
    sid = PERSON_SOURCE.get(p["id"], ["S001"])
    sources = [s for s in SOURCES if s["id"] in sid] or SOURCES
    current_post = p["current_post"].split("（")[0]
    current_post_prose = current_post

    timeline = [{"start": "", "end": "present", "org": p["current_org"], "title": p["current_post"],
                 "level": "地级市", "location": "大庆市", "system": "other", "rank": rank,
                 "is_key_promotion": is_top, "notes": "现任（官方 2026-08-05）",
                 "confidence": "confirmed", "source_ids": sid}]
    if p["id"] == 1:
        timeline.insert(0, {"start": "", "end": "", "org": "（任大庆市委书记前职务待查）",
                            "title": "前任职务（待核）", "level": "", "location": "",
                            "system": "other", "rank": "", "is_key_promotion": False,
                            "notes": "官网个人页未展示完整履历；网络降级未再证", "confidence": "unverified", "source_ids": []})
    if p["id"] == 2:
        timeline.insert(0, {"start": "", "end": "", "org": "（任大庆市长前职务待查）",
                            "title": "前任职务（待核）", "level": "", "location": "",
                            "system": "other", "rank": "", "is_key_promotion": False,
                            "notes": "官网个人页未展示完整履历", "confidence": "unverified", "source_ids": []})
    if p["id"] == 3:
        timeline.append({"start": "", "end": "present", "org": "大庆市委政法委",
                         "title": "市委政法委书记", "level": "地级市", "location": "大庆市",
                         "system": "政法", "rank": "副厅级", "is_key_promotion": False,
                         "notes": "负责政法维稳工作", "confidence": "confirmed", "source_ids": ["S005"]})
    if p["id"] == 8:
        timeline.append({"start": "", "end": "present", "org": "大庆市人民政府",
                         "title": "党组书记（市政府党组）", "level": "地级市", "location": "大庆市",
                         "system": "government", "rank": "副厅级", "is_key_promotion": False,
                         "notes": "市政府党组副书记、协助市长主持市政府常务工作", "confidence": "confirmed", "source_ids": ["S006"]})

    identity = {
        "person_id": f"daqing_{p['name']}",
        "name": p["name"], "aliases": [], "gender": p["gender"], "ethnicity": p["ethnicity"] or "",
        "birth": p["birth"], "birthplace": p["birthplace"], "native_place": "",
        "education": [], "party_join": p["party_join"], "work_start": p["work_start"],
        "dedupe_keys": {"name_birth": f"{p['name']}_{p['birth']}", "name_birthplace": p["birthplace"], "official_profile_url": url},
    }

    data = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "黑龙江省", "city": "大庆市", "region": "大庆市",
            "job": current_post_prose, "task_id": "heilongjiang_大庆市", "time_focus": "current as of 2026-08",
        },
        "identity": identity,
        "current_status": {
            "current_post": p["current_post"], "current_org": p["current_org"],
            "administrative_rank": rank, "as_of": AS_OF, "is_current_confirmed": True, "source_ids": sid,
        },
        "career_timeline": timeline,
        "organizations": [p["current_org"]],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {"primary_specializations": [], "secondary_specializations": [],
                                  "career_pattern": "unknown", "systems_experience": [], "geographic_pattern": [],
                                  "promotion_velocity": {"summary": "", "notable_fast_promotions": []}},
        "work_style_and_personality": {"public_style_indicators": [], "speech_themes": [], "management_signals": [],
                                        "caveat": "Work style is inferred from public records only; not a private assessment."},
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found",
                                        "description": "本轮（2026-08-05）调查未发现公开负面/纪律线索", "date": "",
                                        "confidence": "unverified", "source_ids": []}],
        "source_register": sources,
        "confidence_summary": {"identity": "confirmed", "current_role": "confirmed",
                               "career_completeness": "partial", "relationship_confidence": "low", "biggest_gap": ""},
        "open_questions": [],
    }

    if p["id"] == 1:
        data["confidence_summary"]["biggest_gap"] = "李世峰任市委书记前的完整履历与任命年月"
        data["open_questions"] = [
            {"priority": "critical", "question": "李世峰任大庆市委书记前的任职轨迹与任命年月", "why_it_matters": "晋升路径与省—市干部交流逻辑", "suggested_queries": ["李世峰 大庆市委书记 前任", "李世峰 简历 任职"], "last_attempted": AS_OF},
            {"priority": "high", "question": "李世峰出生年月/籍贯/教育/入党时间", "why_it_matters": "身份标签", "suggested_queries": ["李世峰 出生"], "last_attempted": AS_OF},
        ]
    elif p["id"] == 2:
        data["confidence_summary"]["biggest_gap"] = "李岩松任市长前的职务轨迹与任命年月"
        data["open_questions"] = [
            {"priority": "critical", "question": "李岩松任大庆市长前的任职轨迹与任命年月", "why_it_matters": "晋升路径与系统来源", "suggested_queries": ["李岩松 大庆市长 简历", "李岩松 任前公示"], "last_attempted": AS_OF},
            {"priority": "high", "question": "李岩松出生年月/籍贯/教育细节", "why_it_matters": "身份标签", "suggested_queries": [], "last_attempted": AS_OF},
        ]
    elif p["id"] == 3:
        data["confidence_summary"]["biggest_gap"] = "孙永刚任前履历"
        data["open_questions"] = [{"priority": "high", "question": "孙永刚任大庆市委副书记前的任职轨迹", "why_it_matters": "", "suggested_queries": [], "last_attempted": AS_OF}]
    elif p["id"] == 8:
        data["confidence_summary"]["biggest_gap"] = "韩云任常务副市长前的任职轨迹"
        data["open_questions"] = [{"priority": "high", "question": "韩云（朝鲜族）任常务副市长前的任职轨迹", "why_it_matters": "", "suggested_queries": [], "last_attempted": AS_OF}]

    job = p["current_post"].split("、")[0].split("（")[0]
    out = PERSONS_DIR / f"{TODAY}-黑龙江省-大庆市-{job}-{p['name']}.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ══════════════════════════════════════════════════════════════════════════
# main
# ══════════════════════════════════════════════════════════════════════════

def main():
    print(f"Building {SLUG} network...")
    build_db()
    build_gexf()
    for p in persons:
        person_json(p)
    print("  Person JSONs written to", PERSONS_DIR)
    print("Done.")


if __name__ == "__main__":
    main()