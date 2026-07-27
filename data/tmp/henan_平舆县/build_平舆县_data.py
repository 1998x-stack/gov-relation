#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 平舆县 (Pingyu County), 河南省.

Investigation date: 2026-07-24
Task ID: henan_平舆县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - www.pingyu.gov.cn — 平舆县人民政府网站 (primary)
  - Multiple official news articles from July 2026 confirming 县委副书记、县长李磊
  - 平舆县政府领导信息页: 李磊、韩靖、邢攀、张岩、赵志龙、刘涵斌
  - 县委副书记乔景周深入重点项目一线现场办公 (2026-07-24) — confirmed 乔景周 as 县委副书记
  - 关心下一代工作会议 (2026-07-02) — confirmed 焦中丽 as 组织部部长
  - 主体培训班 (2025-10) — confirmed 代向阳 as 政法委书记, 王娟 as 宣传部部长/副县长
  - 平舆县委统战部部务会 (2026-03) — confirmed 统战部 reported but 马全丽 no longer present

Confidence notes:
  - 县委书记 position: unverified — no individual identified as 县委书记 in any official
    government website article from 2025年9月至2026年7月. The government website only reports
    on government-side officials (县长, 副县长) and 县委副书记. The party secretary and
    party committee activities may be covered on a separate party website.
  - 李磊: confirmed as 县委副书记、县长 via multiple official articles (2026-07-24, etc.)
    Birth: 1982年3月, 男, 汉族, 研究生学历, 中共党员
  - 乔景周: confirmed as 县委副书记 via official article (2026-07-24)
  - 韩靖: confirmed as 县委常委、常务副县长 (profile: 1984年5月, 女, 汉族, 研究生, 党员)
  - 邢攀: confirmed as 副县长 (profile: 1987年5月, 男, 汉族, 研究生, 党员)
  - 张岩: confirmed as 副县长 (profile: 1980年12月, 男, 汉族, 本科, 党员)
  - 赵志龙: confirmed as 副县长 (profile: 1970年2月, 男, 汉族, 研究生/工学硕士, 党员)
  - 刘涵斌: confirmed as 副县长 (profile: 1987年10月, 男, 汉族, 省委党校在职研究生, 党员)
  - Full career timelines for main targets could not be verified from web sources
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING = os.path.dirname(os.path.abspath(__file__))
SLUG = "平舆县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

DB_PATH = os.path.join(STAGING, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING, f"{SLUG}_network.gexf")
PERSONS_DIR = Path(STAGING)

# ── Persons ──────────────────────────────────────────────────────────────────

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership
    # ══════════════════════════════════════════════════════════════════════

    {
        "id": 1,
        "name": "县委书记（待查）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共平舆县委员会",
        "source": "https://www.pingyu.gov.cn/",
        "notes": "截至2026年7月，平舆县政府网站上未出现任何以'县委书记'身份报道的个人。县委书记身份待进一步调查。建议通过驻马店市委组织部任前公示等渠道核实。"
    },
    {
        "id": 2,
        "name": "李磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年3月",
        "birthplace": "待查",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委副书记、县长",
        "current_org": "平舆县人民政府",
        "source": "http://www.pingyu.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202410/t20241022_319936.html",
        "notes": "1982年3月生，汉族，研究生学历，中共党员。任县委副书记、县长，主持县政府全面工作。公开活动频繁，2026年7月多次督导调研。"
    },

    # ══════════════════════════════════════════════════════════════════════
    # Leadership Team (县委/县政府)
    # ══════════════════════════════════════════════════════════════════════

    {
        "id": 3,
        "name": "乔景周",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委副书记",
        "current_org": "中共平舆县委员会",
        "source": "https://www.pingyu.gov.cn/zwyw/ttxw/202607/t20260724_714550.html",
        "notes": "2026年7月20日带队深入重点项目一线现场办公。"
    },
    {
        "id": 4,
        "name": "韩靖",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1984年5月",
        "birthplace": "待查",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委常委、常务副县长",
        "current_org": "平舆县人民政府",
        "source": "http://www.pingyu.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202410/t20241022_319942.html",
        "notes": "1984年5月生，汉族，研究生学历，中共党员。县委常委、常务副县长。"
    },
    {
        "id": 5,
        "name": "焦中丽",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共平舆县委员会",
        "source": "https://www.pingyu.gov.cn/zwyw/zwyw/202607/t20260706_709480.html",
        "notes": "2026年7月2日出席关心下一代工作会议。"
    },
    {
        "id": 6,
        "name": "代向阳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共平舆县委员会",
        "source": "https://www.pingyu.gov.cn/zwyw/zwyw/202605/t20260509_699890.html",
        "notes": "2026年5月为春季主体培训班学员讲党课。"
    },
    {
        "id": 7,
        "name": "王娟",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委常委、宣传部部长、副县长",
        "current_org": "中共平舆县委员会、平舆县人民政府",
        "source": "https://www.pingyu.gov.cn/zwyw/zwyw/202509/t20250911_653496.html",
        "notes": "2025年9月带队赴温州开展招商活动。近期活动较少，职务可能已有变动。"
    },
    {
        "id": 8,
        "name": "邢攀",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987年5月",
        "birthplace": "待查",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副县长",
        "current_org": "平舆县人民政府",
        "source": "http://www.pingyu.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202504/t20250410_552630.html",
        "notes": "1987年5月生，汉族，研究生学历，中共党员。副县长。"
    },
    {
        "id": 9,
        "name": "张岩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年12月",
        "birthplace": "待查",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副县长",
        "current_org": "平舆县人民政府",
        "source": "http://www.pingyu.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202504/t20250410_552625.html",
        "notes": "1980年12月生，汉族，本科学历，中共党员。副县长。"
    },
    {
        "id": 10,
        "name": "赵志龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年2月",
        "birthplace": "待查",
        "education": "研究生，工学硕士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副县长",
        "current_org": "平舆县人民政府",
        "source": "http://www.pingyu.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202504/t20250410_552626.html",
        "notes": "1970年2月生，汉族，研究生学历，工学硕士，中共党员。副县长。"
    },
    {
        "id": 11,
        "name": "刘涵斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987年10月",
        "birthplace": "待查",
        "education": "省委党校在职研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副县长",
        "current_org": "平舆县人民政府",
        "source": "http://www.pingyu.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202504/t20250410_552631.html",
        "notes": "1987年10月生，汉族，省委党校在职研究生，中共党员。副县长，分管教育等领域。"
    },
    {
        "id": 12,
        "name": "张世霞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县人大常委会党组书记、主任",
        "current_org": "平舆县人大常委会",
        "source": "https://www.pingyu.gov.cn/zwyw/zwyw/202604/t20260427_698369.html",
        "notes": "曾任县人大常委会党组书记、主任候选人，2026年4月参加庙湾代表团审议。"
    },
    {
        "id": 13,
        "name": "李志娴",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县政协主席",
        "current_org": "政协平舆县委员会",
        "source": "https://www.pingyu.gov.cn/zwyw/zwyw/202604/t20260427_698374.html",
        "notes": "2026年4月以县政协主席身份参加县政协十届五次会议。"
    },
    {
        "id": 14,
        "name": "代广红",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县领导",
        "current_org": "平舆县",
        "source": "https://www.pingyu.gov.cn/zwyw/zwyw/202607/t20260724_714552.html",
        "notes": "2026年7月随李磊督导调研。"
    },
    {
        "id": 15,
        "name": "王明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县领导",
        "current_org": "平舆县",
        "source": "https://www.pingyu.gov.cn/zwyw/zwyw/202607/t20260724_714552.html",
        "notes": "2026年7月随李磊督导调研。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中共平舆县委员会",
        "type": "党委",
        "level": "县级",
        "location": "河南省驻马店市平舆县"
    },
    {
        "id": 2,
        "name": "平舆县人民政府",
        "type": "政府",
        "level": "县级",
        "location": "河南省驻马店市平舆县"
    },
    {
        "id": 3,
        "name": "平舆县人大常委会",
        "type": "人大",
        "level": "县级",
        "location": "河南省驻马店市平舆县"
    },
    {
        "id": 4,
        "name": "政协平舆县委员会",
        "type": "政协",
        "level": "县级",
        "location": "河南省驻马店市平舆县"
    },
    {
        "id": 5,
        "name": "中共平舆县委组织部",
        "type": "党委",
        "level": "县级",
        "location": "河南省驻马店市平舆县"
    },
    {
        "id": 6,
        "name": "中共平舆县委政法委",
        "type": "党委",
        "level": "县级",
        "location": "河南省驻马店市平舆县"
    },
    {
        "id": 7,
        "name": "中共平舆县委宣传部",
        "type": "党委",
        "level": "县级",
        "location": "河南省驻马店市平舆县"
    },
]

# ── Positions ─────────────────────────────────────────────────────────────

positions = [
    # 县委书记（待查）
    {"person_id": "p1", "org_id": 1, "title": "县委书记", "start": "?",
     "end": "present", "rank": "正处级", "note": "身份待核实"},
    # 李磊
    {"person_id": "p2", "org_id": 2, "title": "县长", "start": "?",
     "end": "present", "rank": "正处级", "note": "县委副书记、县长，主持县政府全面工作"},
    {"person_id": "p2", "org_id": 1, "title": "县委副书记", "start": "?",
     "end": "present", "rank": "正处级", "note": "县委副书记"},
    # 乔景周
    {"person_id": "p3", "org_id": 1, "title": "县委副书记", "start": "?",
     "end": "present", "rank": "副处级", "note": "分管党建、重点项目等"},
    # 韩靖
    {"person_id": "p4", "org_id": 2, "title": "常务副县长", "start": "?",
     "end": "present", "rank": "副处级", "note": "县委常委、常务副县长"},
    {"person_id": "p4", "org_id": 1, "title": "县委常委", "start": "?",
     "end": "present", "rank": "副处级", "note": ""},
    # 焦中丽
    {"person_id": "p5", "org_id": 5, "title": "组织部部长", "start": "?",
     "end": "present", "rank": "副处级", "note": "县委常委、组织部部长"},
    {"person_id": "p5", "org_id": 1, "title": "县委常委", "start": "?",
     "end": "present", "rank": "副处级", "note": ""},
    # 代向阳
    {"person_id": "p6", "org_id": 6, "title": "政法委书记", "start": "?",
     "end": "present", "rank": "副处级", "note": "县委常委、政法委书记"},
    {"person_id": "p6", "org_id": 1, "title": "县委常委", "start": "?",
     "end": "present", "rank": "副处级", "note": ""},
    # 王娟
    {"person_id": "p7", "org_id": 7, "title": "宣传部部长", "start": "?",
     "end": "present", "rank": "副处级", "note": "县委常委、宣传部部长"},
    {"person_id": "p7", "org_id": 2, "title": "副县长", "start": "?",
     "end": "present", "rank": "副处级", "note": "兼任副县长"},
    {"person_id": "p7", "org_id": 1, "title": "县委常委", "start": "?",
     "end": "present", "rank": "副处级", "note": ""},
    # 邢攀
    {"person_id": "p8", "org_id": 2, "title": "副县长", "start": "?",
     "end": "present", "rank": "副处级", "note": "副县长"},
    # 张岩
    {"person_id": "p9", "org_id": 2, "title": "副县长", "start": "?",
     "end": "present", "rank": "副处级", "note": "副县长"},
    # 赵志龙
    {"person_id": "p10", "org_id": 2, "title": "副县长", "start": "?",
     "end": "present", "rank": "副处级", "note": "副县长"},
    # 刘涵斌
    {"person_id": "p11", "org_id": 2, "title": "副县长", "start": "?",
     "end": "present", "rank": "副处级", "note": "副县长，分管教育"},
    # 张世霞
    {"person_id": "p12", "org_id": 3, "title": "县人大常委会党组书记、主任",
     "start": "?", "end": "present", "rank": "正处级",
     "note": "曾任主任候选人，2026年4月审议政府工作报告"},
    # 李志娴
    {"person_id": "p13", "org_id": 4, "title": "县政协主席", "start": "?",
     "end": "present", "rank": "正处级", "note": ""},
    # 代广红
    {"person_id": "p14", "org_id": 2, "title": "县领导", "start": "?",
     "end": "present", "rank": "副处级", "note": ""},
    # 王明
    {"person_id": "p15", "org_id": 2, "title": "县领导", "start": "?",
     "end": "present", "rank": "副处级", "note": ""},
]

# ── Relationships ──────────────────────────────────────────────────────────

relationships = [
    {
        "person_a": "p1", "person_b": "p2",
        "type": "superior_subordinate",
        "context": "县委书记（待查）与县长李磊为党政主要领导搭档关系",
        "overlap_org": "平舆县", "overlap_period": "待查",
        "confidence": "unverified"
    },
    {
        "person_a": "p2", "person_b": "p3",
        "type": "superior_subordinate",
        "context": "县委副书记、县长李磊与县委副书记乔景周为领导班子同事",
        "overlap_org": "中共平舆县委员会", "overlap_period": "2026年至今",
        "confidence": "confirmed"
    },
    {
        "person_a": "p2", "person_b": "p4",
        "type": "superior_subordinate",
        "context": "县长李磊与常务副县长韩靖为党政领导班子搭档",
        "overlap_org": "平舆县人民政府", "overlap_period": "2026年至今",
        "confidence": "confirmed"
    },
    {
        "person_a": "p2", "person_b": "p5",
        "type": "superior_subordinate",
        "context": "李磊与组织部部长焦中丽为县委领导班子同事",
        "overlap_org": "中共平舆县委员会", "overlap_period": "2026年至今",
        "confidence": "confirmed"
    },
    {
        "person_a": "p2", "person_b": "p6",
        "type": "superior_subordinate",
        "context": "李磊与政法委书记代向阳为县委领导班子同事",
        "overlap_org": "中共平舆县委员会", "overlap_period": "2026年至今",
        "confidence": "confirmed"
    },
    {
        "person_a": "p3", "person_b": "p5",
        "type": "overlap",
        "context": "乔景周与焦中丽共同出席关心下一代工作会议",
        "overlap_org": "中共平舆县委员会", "overlap_period": "2026年7月",
        "confidence": "confirmed"
    },
    {
        "person_a": "p2", "person_b": "p8",
        "type": "superior_subordinate",
        "context": "县长李磊与副县长邢攀为政府领导班子成员",
        "overlap_org": "平舆县人民政府", "overlap_period": "2026年至今",
        "confidence": "confirmed"
    },
    {
        "person_a": "p2", "person_b": "p11",
        "type": "superior_subordinate",
        "context": "县长李磊与副县长刘涵斌为政府领导班子成员",
        "overlap_org": "平舆县人民政府", "overlap_period": "2026年至今",
        "confidence": "confirmed"
    },
    {
        "person_a": "p2", "person_b": "p14",
        "type": "overlap",
        "context": "李磊与代广红共同调研乡镇工作",
        "overlap_org": "平舆县", "overlap_period": "2026年7月",
        "confidence": "confirmed"
    },
    {
        "person_a": "p2", "person_b": "p15",
        "type": "overlap",
        "context": "李磊与王明共同调研乡镇工作",
        "overlap_org": "平舆县", "overlap_period": "2026年7月",
        "confidence": "confirmed"
    },
]

# ── Build ──────────────────────────────────────────────────────────────────

def build():
    """Run database + GEXF build."""
    import sqlite3

    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT,
            notes TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            confidence TEXT DEFAULT 'unverified',
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    # Normalize person ids: strip "p" prefix for DB
    def pid(s):
        return int(s[1:])

    for p in persons:
        cur.execute(
            "INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, "
            "party_join, work_start, current_post, current_org, source, notes) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (pid("p" + str(p["id"])), p["name"], p.get("gender", ""), p.get("ethnicity", ""),
             p.get("birth", ""), p.get("birthplace", ""), p.get("education", ""),
             p.get("party_join", ""), p.get("work_start", ""),
             p["current_post"], p["current_org"], p.get("source", ""), p.get("notes", ""))
        )

    for o in organizations:
        cur.execute(
            "INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?, ?, ?, ?, ?, ?)",
            (o["id"], o["name"], o.get("type", ""), o.get("level", ""),
             o.get("parent", ""), o.get("location", ""))
        )

    for pos in positions:
        cur.execute(
            "INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (pid(pos["person_id"]), pos["org_id"], pos["title"],
             pos.get("start", ""), pos.get("end", "present"),
             pos.get("rank", ""), pos.get("note", ""))
        )

    for r in relationships:
        cur.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, confidence) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (pid(r["person_a"]), pid(r["person_b"]), r["type"], r.get("context", ""),
             r.get("overlap_org", ""), r.get("overlap_period", ""),
             r.get("confidence", "unverified"))
        )

    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")
    print(f"   {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

    # ── GEXF ────────────────────────────────────────────────────────────

    def esc(s):
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    def person_color_and_size(post):
        if "县委书记" in post and "副" not in post:
            return ("255,50,50", 20.0)
        elif "县长" in post and "副" not in post and "委" not in post:
            return ("50,100,255", 20.0)
        elif "县委副书记" in post:
            return ("50,100,255", 15.0)
        elif "常委" in post and ("副" in post or "组织" in post or "政法" in post or "宣传" in post or "统战" in post):
            return ("100,150,255", 12.0)
        elif "副" in post and ("县长" in post):
            return ("100,150,255", 12.0)
        elif "人大" in post or "政协" in post:
            return ("200,255,255", 12.0)
        else:
            return ("100,100,100", 12.0)

    org_colors = {
        "党委": ("255,200,200", 8.0),
        "政府": ("200,200,255", 8.0),
        "人大": ("200,255,255", 8.0),
        "政协": ("255,240,200", 8.0),
    }

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append(f'    <description>平舆县领导班子工作关系网络 - {AS_OF}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c, sz = person_color_and_size(p["current_post"])
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        oc, osz = org_colors.get(o["type"], ("200,200,200", 8.0))
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{oc.split(",")[0]}" g="{oc.split(",")[1]}" b="{oc.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{osz}"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    # Person -> Organization (worked_at)
    for pos in positions:
        eid += 1
        pid_val = int(pos["person_id"][1:])
        lines.append(f'      <edge id="e{eid}" source="p{pid_val}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person <-> Person (relationship)
    for r in relationships:
        eid += 1
        a = int(r["person_a"][1:])
        b = int(r["person_b"][1:])
        lines.append(f'      <edge id="e{eid}" source="p{a}" target="p{b}" label="{esc(r.get("context",""))}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF created: {GEXF_PATH}")

    # ── Summary ────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"平舆县 Network Build Complete")
    print(f"{'='*60}")
    print(f"Persons:     {len(persons)}")
    print(f"Orgs:        {len(organizations)}")
    print(f"Positions:   {len(positions)}")
    print(f"Edges:       {eid}")
    print(f"DB:          {DB_PATH}")
    print(f"GEXF:        {GEXF_PATH}")


if __name__ == "__main__":
    build()
