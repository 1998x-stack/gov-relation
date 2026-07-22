#!/usr/bin/env python3
"""Build Dongzhi County (东至县) leadership network database and GEXF graph.

Targets: 县委书记王朝东, 县长詹丛辉
Research date: 2026-07-15
Sources:
  - www.dongzhi.gov.cn (official county government website) - 领导之窗
  - www.dongzhi.gov.cn/Leader/ (Party committee leadership page)
  - www.dongzhi.gov.cn/Leader/showList/3/0.html (Government leadership page)
  - www.dongzhi.gov.cn/Leader/showList/1/3234.html (县委书记王朝东 profile)
  - www.dongzhi.gov.cn/Leader/showList/3/1727.html (县长詹丛辉 profile)
  - www.dongzhi.gov.cn government news articles (2026-07)

Confidence: Current roles confirmed from official county government website leadership page.
  Biographical details sourced from official profiles.
  Career timelines for deputy figures are partial where noted.
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "东至县_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "东至县_network.gexf")

TODAY = datetime.now().strftime("%Y-%m-%d")

# ── research data ────────────────────────────────────────────────────────

persons = [
    # === 1. Party Secretary (县委书记) ===
    {
        "id": 1,
        "name": "王朝东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-05",
        "birthplace": "",
        "native_place": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共东至县委员会",
        "source": "https://www.dongzhi.gov.cn/Leader/showList/1/3234.html (东至县政府领导之窗); https://www.dongzhi.gov.cn/Content/show/782425.html (2026-07-15 主持县委常委会会议)",
        "notes": "王朝东，男，汉族，1972年5月出生，省委党校研究生学历，中共党员，现任东至县委书记。曾任副乡镇长，区群团组织正职，区政府组成部门正职，乡镇党政正职，区政府副区长，区委常委、常务副区长，区委副书记，地级市政府组成部门正职。主持县委全面工作。",
        "confidence": "confirmed"
    },
    # === 2. County Magistrate (县长) ===
    {
        "id": 2,
        "name": "詹丛辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984-08",
        "birthplace": "",
        "native_place": "",
        "education": "大学学历，经济学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县政府党组书记、县长",
        "current_org": "东至县人民政府",
        "source": "https://www.dongzhi.gov.cn/Leader/showList/3/1727.html (东至县政府领导之窗); https://www.dongzhi.gov.cn/Leader/showList/1/2767.html (县委领导页面)",
        "notes": "詹丛辉，男，汉族，1984年8月出生，大学学历，经济学学士，中共党员。现任东至县委副书记、县政府党组书记、县长。曾任地级市政府组成部门科员，市政府办公室主任科员、科长，市政府办公室党组成员、副主任，市政府机关党组成员、办公室副主任，县委统战部部长，县政协党组副书记，省级经济开发区党委书记、党工委第一书记，县政府党组副书记、常务副县长等职。领导县政府全面工作，分管县审计局。",
        "confidence": "confirmed"
    },
    # === 3. Deputy Party Secretary (县委副书记) ===
    {
        "id": 3,
        "name": "程良才",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县委党校校长",
        "current_org": "中共东至县委员会",
        "source": "https://www.dongzhi.gov.cn/Leader/ (东至县委领导页面)",
        "notes": "程良才，现任东至县委副书记、县委党校校长。负责党校工作。",
        "confidence": "confirmed"
    },
    # === 4. Political and Legal Affairs Secretary (政法委书记) ===
    {
        "id": 4,
        "name": "郭宏盛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县委政法委书记",
        "current_org": "中共东至县委政法委员会",
        "source": "https://www.dongzhi.gov.cn/Leader/ (东至县委领导页面)",
        "notes": "郭宏盛，现任东至县委常委、县委政法委书记。主持县委政法委工作。",
        "confidence": "confirmed"
    },
    # === 5. Propaganda Department Head (宣传部部长) ===
    {
        "id": 5,
        "name": "唐传华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县委宣传部部长",
        "current_org": "中共东至县委宣传部",
        "source": "https://www.dongzhi.gov.cn/Leader/ (东至县委领导页面)",
        "notes": "唐传华，现任东至县委常委、县委宣传部部长。主持县委宣传部工作。",
        "confidence": "confirmed"
    },
    # === 6. Deputy Magistrate (县委常委、副县长) ===
    {
        "id": 6,
        "name": "张柏春",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "东至县人民政府",
        "source": "https://www.dongzhi.gov.cn/Leader/ (东至县委/政府领导页面); https://www.dongzhi.gov.cn/Leader/showList/3/2054.html",
        "notes": "张柏春，现任东至县委常委、副县长。",
        "confidence": "confirmed"
    },
    # === 7. Discipline Inspection Secretary (纪委书记) ===
    {
        "id": 7,
        "name": "何争明",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县纪委书记、县监委主任",
        "current_org": "中共东至县纪律检查委员会",
        "source": "https://www.dongzhi.gov.cn/Leader/ (东至县委领导页面)",
        "notes": "何争明，现任东至县委常委、县纪委书记、县监委主任。主持县纪委、县监委工作。",
        "confidence": "confirmed"
    },
    # === 8. Deputy Magistrate (县委常委、副县长) ===
    {
        "id": 8,
        "name": "费飞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "东至县人民政府",
        "source": "https://www.dongzhi.gov.cn/Leader/ (东至县委/政府领导页面); https://www.dongzhi.gov.cn/Leader/showList/3/2768.html",
        "notes": "费飞，现任东至县委常委、副县长。",
        "confidence": "confirmed"
    },
    # === 9. Development Zone Head (开发区党工委第一书记) ===
    {
        "id": 9,
        "name": "施为国",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、东至经济开发区党工委第一书记",
        "current_org": "东至经济开发区",
        "source": "https://www.dongzhi.gov.cn/Leader/ (东至县委领导页面)",
        "notes": "施为国，现任东至县委常委、东至经济开发区党工委第一书记。负责开发区党建工作。",
        "confidence": "confirmed"
    },
    # === 10. Organization Department Head (组织部部长) ===
    {
        "id": 10,
        "name": "钱芳",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县委组织部部长",
        "current_org": "中共东至县委组织部",
        "source": "https://www.dongzhi.gov.cn/Leader/ (东至县委领导页面)",
        "notes": "钱芳，现任东至县委常委、县委组织部部长。主持县委组织部工作。",
        "confidence": "confirmed"
    },
    # === 11. Party Standing Committee Member (县委常委) ===
    {
        "id": 11,
        "name": "阮剑辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共东至县委员会",
        "source": "https://www.dongzhi.gov.cn/Leader/ (东至县委领导页面)",
        "notes": "阮剑辉，现任东至县委常委。",
        "confidence": "confirmed"
    },
    # === 12. Deputy Magistrate (副县长) ===
    {
        "id": 12,
        "name": "许家旺",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "东至县人民政府",
        "source": "https://www.dongzhi.gov.cn/Leader/showList/3/1953.html (东至县政府领导页面)",
        "notes": "许家旺，现任东至县副县长。",
        "confidence": "confirmed"
    },
    # === 13. Deputy Magistrate (副县长) ===
    {
        "id": 13,
        "name": "陆林",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "东至县人民政府",
        "source": "https://www.dongzhi.gov.cn/Leader/showList/3/2055.html (东至县政府领导页面)",
        "notes": "陆林，现任东至县副县长。",
        "confidence": "confirmed"
    },
    # === 14. Deputy Magistrate (挂职副县长) ===
    {
        "id": 14,
        "name": "王琼",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长（挂职）",
        "current_org": "东至县人民政府",
        "source": "https://www.dongzhi.gov.cn/Leader/showList/3/2786.html (东至县政府领导页面)",
        "notes": "王琼，现任东至县副县长（挂职）。",
        "confidence": "confirmed"
    },
    # === 15. Deputy Magistrate (副县长) ===
    {
        "id": 15,
        "name": "钱张红",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "东至县人民政府",
        "source": "https://www.dongzhi.gov.cn/Leader/showList/3/3269.html (东至县政府领导页面)",
        "notes": "钱张红，现任东至县副县长。",
        "confidence": "confirmed"
    },
    # === 16. Deputy Magistrate (副县长) ===
    {
        "id": 16,
        "name": "杨艳",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "东至县人民政府",
        "source": "https://www.dongzhi.gov.cn/Leader/showList/3/2829.html (东至县政府领导页面)",
        "notes": "杨艳，现任东至县副县长。",
        "confidence": "confirmed"
    },
    # === 17. Deputy Magistrate (挂职副县长) ===
    {
        "id": 17,
        "name": "侯军伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长（挂职）",
        "current_org": "东至县人民政府",
        "source": "https://www.dongzhi.gov.cn/Leader/showList/3/2833.html (东至县政府领导页面)",
        "notes": "侯军伟，现任东至县副县长（挂职）。",
        "confidence": "confirmed"
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共东至县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共池州市委员会",
        "location": "安徽省池州市东至县"
    },
    {
        "id": 2,
        "name": "东至县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "池州市人民政府",
        "location": "安徽省池州市东至县"
    },
    {
        "id": 3,
        "name": "中共东至县委政法委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共东至县委员会",
        "location": "安徽省池州市东至县"
    },
    {
        "id": 4,
        "name": "中共东至县委宣传部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共东至县委员会",
        "location": "安徽省池州市东至县"
    },
    {
        "id": 5,
        "name": "中共东至县纪律检查委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共东至县委员会",
        "location": "安徽省池州市东至县"
    },
    {
        "id": 6,
        "name": "东至经济开发区",
        "type": "开发区",
        "level": "县处级",
        "parent": "东至县人民政府",
        "location": "安徽省池州市东至县"
    },
    {
        "id": 7,
        "name": "中共东至县委组织部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共东至县委员会",
        "location": "安徽省池州市东至县"
    },
    {
        "id": 8,
        "name": "中共东至县委党校",
        "type": "事业单位",
        "level": "乡科级",
        "parent": "中共东至县委员会",
        "location": "安徽省池州市东至县"
    },
]

positions = [
    # Person 1: 王朝东
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "unknown", "end": "present", "rank": "正处级", "note": "主持县委全面工作"},
    # Person 2: 詹丛辉
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "unknown", "end": "present", "rank": "正处级", "note": "领导县政府全面工作，分管审计局"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记、县政府党组书记", "start": "unknown", "end": "present", "rank": "正处级", "note": "县委副书记"},
    # Person 3: 程良才
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 8, "title": "县委党校校长", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    # Person 4: 郭宏盛
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 3, "title": "县委政法委书记", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    # Person 5: 唐传华
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 4, "title": "县委宣传部部长", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    # Person 6: 张柏春
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    # Person 7: 何争明
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 5, "title": "县纪委书记、县监委主任", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    # Person 8: 费飞
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    # Person 9: 施为国
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 6, "title": "东至经济开发区党工委第一书记", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    # Person 10: 钱芳
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 7, "title": "县委组织部部长", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    # Person 11: 阮剑辉
    {"person_id": 11, "org_id": 1, "title": "县委常委", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    # Person 12: 许家旺
    {"person_id": 12, "org_id": 2, "title": "副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    # Person 13: 陆林
    {"person_id": 13, "org_id": 2, "title": "副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    # Person 14: 王琼
    {"person_id": 14, "org_id": 2, "title": "副县长（挂职）", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    # Person 15: 钱张红
    {"person_id": 15, "org_id": 2, "title": "副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    # Person 16: 杨艳
    {"person_id": 16, "org_id": 2, "title": "副县长", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
    # Person 17: 侯军伟
    {"person_id": 17, "org_id": 2, "title": "副县长（挂职）", "start": "unknown", "end": "present", "rank": "副处级", "note": ""},
]

relationships = [
    # Core team: 王朝东 + 詹丛辉
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记与县长，东至县党政主要领导搭档", "overlap_org": "东至县", "overlap_period": "至今"},
    # 王朝东 + 程良才
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县委书记与县委副书记", "overlap_org": "中共东至县委员会", "overlap_period": "至今"},
    # 王朝东 + 郭宏盛
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "县委书记与政法委书记", "overlap_org": "中共东至县委员会", "overlap_period": "至今"},
    # 王朝东 + 何争明
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "县委书记与纪委书记", "overlap_org": "中共东至县委员会", "overlap_period": "至今"},
    # 王朝东 + 钱芳
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate", "context": "县委书记与组织部部长", "overlap_org": "中共东至县委员会", "overlap_period": "至今"},
    # 詹丛辉 + 张柏春 (政府班子)
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "县长与县委常委、副县长", "overlap_org": "东至县人民政府", "overlap_period": "至今"},
    # 詹丛辉 + 费飞 (政府班子)
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "县长与县委常委、副县长", "overlap_org": "东至县人民政府", "overlap_period": "至今"},
    # 詹丛辉 + 程良才
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "县长与县委副书记", "overlap_org": "东至县", "overlap_period": "至今"},
    # 王朝东 + 詹丛辉 + 全体县委常委
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "县委书记与宣传部部长", "overlap_org": "中共东至县委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "县委书记与县委常委、副县长", "overlap_org": "中共东至县委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "县委书记与县委常委、副县长", "overlap_org": "中共东至县委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "县委书记与开发区党工委第一书记", "overlap_org": "中共东至县委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "县委书记与县委常委", "overlap_org": "中共东至县委员会", "overlap_period": "至今"},
]


def build_db():
    """Create and populate SQLite database."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, native_place TEXT, education TEXT,
            party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT,
            source TEXT, notes TEXT, confidence TEXT
        );
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        );
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER,
            title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    # Insert persons
    for p in persons:
        c.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace,
                native_place, education, party_join, work_start,
                current_post, current_org, source, notes, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
              p["birthplace"], p["native_place"], p["education"],
              p["party_join"], p["work_start"],
              p["current_post"], p["current_org"],
              p["source"], p["notes"], p["confidence"]))

    # Insert organizations
    for o in organizations:
        c.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    # Insert positions
    for pos in positions:
        c.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos["title"],
              pos["start"], pos["end"], pos["rank"], pos["note"]))

    # Insert relationships
    for r in relationships:
        c.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r["type"],
              r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    """Return 'r,g,b' for a person based on role."""
    post = p.get("current_post", "")
    if "书记" in post and "县委" in post:
        return "255,50,50"
    elif "县长" in post or "区长" in post:
        return "50,100,255"
    elif "纪委书记" in post or "监委" in post:
        return "255,165,0"
    elif "政法委" in post:
        return "255,165,0"
    elif "政协" in post:
        return "200,255,255"
    elif "人大" in post:
        return "200,255,255"
    else:
        return "100,100,100"


def build_gexf():
    """Generate GEXF graph file using string formatting."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>东至县领导班子工作关系网络 - 中共东至县委、东至县人民政府领导班子成员</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('    </attributes>')

    # ── Nodes: Persons ──
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        is_top = any(kw in p["current_post"] for kw in ["县委书记", "县长"])
        sz = "20.0" if is_top else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # ── Nodes: Organizations ──
    org_colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
        "事业单位": "220,220,220",
    }
    for o in organizations:
        c = org_colors.get(o["type"], "200,200,200")
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["level"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # ── Edges ──
    eid = 0
    lines.append('    <edges>')

    # Person -> Organization (worked_at)
    for pos in positions:
        eid += 1
        w = "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos["start"])} → {esc(pos["end"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person <-> Person (relationship)
    for r in relationships:
        eid += 1
        w = "2.0"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF graph created: {GEXF_PATH}")


def print_summary():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    print("\n── Summary ────────────────────────────────────────────────────")
    c.execute("SELECT COUNT(*) FROM persons")
    print(f"  Persons: {c.fetchone()[0]}")
    c.execute("SELECT COUNT(*) FROM organizations")
    print(f"  Organizations: {c.fetchone()[0]}")
    c.execute("SELECT COUNT(*) FROM positions")
    print(f"  Positions: {c.fetchone()[0]}")
    c.execute("SELECT COUNT(*) FROM relationships")
    print(f"  Relationships: {c.fetchone()[0]}")

    print("\n  Top leaders:")
    c.execute("SELECT name, current_post FROM persons WHERE id IN (1,2)")
    for row in c.fetchall():
        print(f"    {row[0]} — {row[1]}")

    print("\n  Party Standing Committee:")
    c.execute("SELECT name, current_post FROM persons WHERE id >= 3 AND id <= 11")
    for row in c.fetchall():
        print(f"    {row[0]} — {row[1]}")

    print("\n  Government deputies:")
    c.execute("SELECT name, current_post FROM persons WHERE id >= 12")
    for row in c.fetchall():
        print(f"    {row[0]} — {row[1]}")

    conn.close()


if __name__ == "__main__":
    build_db()
    build_gexf()
    print_summary()

    print(f"\n── Files ─────────────────────────────────────────────────────")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print("✅ Done.")
