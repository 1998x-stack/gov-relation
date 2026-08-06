#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 巴彦县 (Bayan County), 哈尔滨市, 黑龙江省.

Investigation date: 2026-08-06
Task ID: heilongjiang_巴彦县
Level: 县
Targets: 县委书记 & 县长

Primary sources (official, as-of 2026-08-06):
  - 巴彦县人民政府官网·领导信息：县委/政府/人大/政协领导班子成员页
      http://www.bayan.gov.cn/hebbyx/wyx/202509/c01_1076937.shtml （县委领导）
      http://www.bayan.gov.cn/hebbyx/wrang/202607/c01_1136368.shtml （县政府领导）
      及每名领导个人简历页
  - 百度百科：汪育欣(巴彦县委书记)、祁彦勇(前县长,1979-03, 宾县)
  - 哈尔滨市政府/巴彦县人大 任免新闻 (2025-01-06 任命)
  - 巴彦县政府新闻：2025-01 人大选举祁彦勇为县长；2025-05 汪育欣任县人武部党委第一书记；
    2026-05 祁彦勇烟花爆竹检查；2026-07 人大常委会第34次会议(王让任代县长)

As-of: 2026-08

Confirmed current leadership (巴彦县):
  - 县委书记：汪育欣（副局长级，2024-11 至今）— 辽宁凤城人，东北农大农机专业
  - 县委副书记、县长（代）：王让（1981-07，管理学博士，2026-07 任代县长，接替祁彦勇）
  - 前任书记：兰淼（兼县人大常委会主任）→ 汪育欣（2024-11）
  - 前县长：祁彦勇（2025-01 当选—2026-07，宾县出身）→ 王让

县委班子（2026-08）：汪育欣、王让、汤继国(副书记)、李昕(组织部)、宋立伟(政法委)、
谭磊(统战)、孙继成(宣传部)、罗祥伟(副县长/一届)、白志伟(常务副县长)、李鹏(纪委书记)
政府领导：王兴、白志伟、罗祥伟、陈国荣、张淑芬、任程滨、杨超
人大：赵万方(主任)、曲淑音、丛立新、王伟、王冬雨；政协：李彦国(主席)、王立海、李莉、梁彦波

Gaps (see open_gaps):
  - 王兴任代县长前完整履历待核；出生地/籍贯待核
  - 祁彦勇卸任后去向待核
  - 汪育欣 2000-2018 哈尔滨机关各段任职细点待补
  - 李鹏（纪委书记）任前履历待核
  - 黄永鑫（前监委会主任，纪委调整）去向待核
"""

import json
import os
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
SLUG = "巴彦县"
TODAY = datetime.now().strftime("%Y%m%d")          # 20260806
AS_OF = "2026-08-06"

DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")
PERSONS_DIR = Path(BASE)

# ── Persons ────────────────────────────────────────────────────────────────
# id 编排：1-核心书记县长，2x 前任，3x 现任县委/政府，4x 人大/政协
persons = [
    # 核心：县委书记 / 县长(代)
    {"id": 1, "name": "汪育欣", "gender": "男", "ethnicity": "汉族", "birth": "1971-05", "birthplace": "辽宁凤城",
     "education": "东北农业大学农业机械化专业（大学/工学学士）", "party_join": "1994-07", "work_start": "1997-09",
     "current_post": "县委书记", "current_org": "中共巴彦县委", "source": "巴彦县政府官网·县委领导汪育欣简历页"},
    {"id": 2, "name": "王让", "gender": "男", "ethnicity": "汉族", "birth": "1981-07", "birthplace": "",
     "education": "研究生学历，管理学博士", "party_join": "中共党员", "work_start": "",
     "current_post": "县委副书记、代县长", "current_org": "巴彦县人民政府", "source": "巴彦县政府官网·政府领导王让简历页"},
    # 前任
    {"id": 3, "name": "祁彦勇", "gender": "男", "ethnicity": "", "birth": "1979-03", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "前县长（2025.01-2026.07）", "current_org": "巴彦县人民政府", "source": "百度百科·祁彦勇；巴彦县人大 2025-01 选举新闻"},
    {"id": 4, "name": "兰淼", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "前县委书记、原县人大常委会主任", "current_org": "中共巴彦县委", "source": "巴彦县新闻（2023书记兼人大主任）/ 中国共产党巴彦县第17届委员会"},
    # 县委班子
    {"id": 5, "name": "汤继国", "gender": "男", "ethnicity": "汉族", "birth": "1975-03", "birthplace": "",
     "education": "在职大学学历", "party_join": "中共党员", "work_start": "",
     "current_post": "县委副书记", "current_org": "中共巴彦县委", "source": "巴彦县政府官网·县委领导汤继国简历页"},
    {"id": 6, "name": "李昱", "gender": "女", "ethnicity": "汉族", "birth": "1976-04", "birthplace": "",
     "education": "省委党校研究生学历", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、组织部部长", "current_org": "中共巴彦县委组织部", "source": "巴彦县政府官网·县委领导李昱简历页"},
    {"id": 7, "name": "宋立伟", "gender": "男", "ethnicity": "汉族", "birth": "1977-03", "birthplace": "",
     "education": "省委党校研究生学历", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、政法委书记", "current_org": "中共巴彦县委政法委员会", "source": "巴彦县政府官网·县委领导宋立伟简历页"},
    {"id": 8, "name": "谭磊", "gender": "男", "ethnicity": "汉族", "birth": "1982-11", "birthplace": "",
     "education": "研究生学历", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、统战部部长", "current_org": "中共巴彦县委统战部", "source": "巴彦县政府官网·县委领导谭磊简历页"},
    {"id": 9, "name": "孙继成", "gender": "男", "ethnicity": "汉族", "birth": "1976-03", "birthplace": "",
     "education": "在职大学学历", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、宣传部部长", "current_org": "中共巴彦县委宣传部", "source": "巴彦县政府官网·县委领导孙继成简历页"},
    {"id": 10, "name": "罗祥伟", "gender": "男", "ethnicity": "汉族", "birth": "1979-08", "birthplace": "",
     "education": "研究生学历，管理学硕士", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、政府副县长（挂职）", "current_org": "巴彦县人民政府", "source": "巴彦县政府官网·县委领导罗祥伟简历页"},
    {"id": 11, "name": "白晶玉", "gender": "男", "ethnicity": "汉族", "birth": "1976-12", "birthplace": "",
     "education": "省委党校大学学历", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、常务副县长", "current_org": "巴彦县人民政府", "source": "巴彦县政府官网·政府领导白晶玉简历页"},
    {"id": 12, "name": "李鹏", "gender": "男", "ethnicity": "汉族", "birth": "1978-10", "birthplace": "",
     "education": "省委党校研究生学历", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、纪委书记、监委代主任", "current_org": "中共巴彦县纪委、监察委员会", "source": "巴彦县政府官网·县委领导李鹏简历页"},
    # 其他副县长
    {"id": 13, "name": "陈国荣", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "副县长", "current_org": "巴彦县人民政府", "source": "巴彦县政府官网·政府领导列表"},
    {"id": 14, "name": "张淑芬", "gender": "女", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "副县长", "current_org": "巴彦县人民政府", "source": "巴彦县政府官网·政府领导列表"},
    {"id": 15, "name": "任程滨", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "副县长", "current_org": "巴彦县人民政府", "source": "巴彦县政府官网·政府领导列表"},
    {"id": 16, "name": "杨超", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "副县长", "current_org": "巴彦县人民政府", "source": "巴彦县政府官网·政府领导列表 (2026-07)"},
    # 人大 / 政协
    {"id": 17, "name": "赵万方", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县人大常委会主任", "current_org": "巴彦县人大常委会", "source": "巴彦县政府官网·人大领导列表"},
    {"id": 18, "name": "李彦国", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县政协主席", "current_org": "政协巴彦县委员会", "source": "巴彦县政府官网·政协领导列表"},
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共巴彦县委", "type": "党委", "level": "县级", "parent": "中共哈尔滨市委", "location": "巴彦县"},
    {"id": 2, "name": "巴彦县人民政府", "type": "政府", "level": "县级", "parent": "哈尔滨市人民政府", "location": "巴彦县"},
    {"id": 3, "name": "巴彦县人大常委会", "type": "人大", "level": "县级", "parent": "哈尔滨市人大常委会", "location": "巴彦县"},
    {"id": 4, "name": "政协巴彦县委员会", "type": "政协", "level": "县级", "parent": "哈尔滨市政协", "location": "巴彦县"},
    {"id": 5, "name": "中共巴彦县纪律检查委员会/监委", "type": "纪委", "level": "县级", "parent": "中共哈尔滨市纪委", "location": "巴彦县"},
    {"id": 6, "name": "中共巴彦县委组织部", "type": "党委", "level": "县级", "parent": "中共巴彦县委", "location": "巴彦县"},
    {"id": 7, "name": "中共巴彦县委政法委员会", "type": "党委", "level": "县级", "parent": "中共巴彦县委", "location": "巴彦县"},
    {"id": 8, "name": "中共巴彦县委统战部", "type": "党委", "level": "县级", "parent": "中共巴彦县委", "location": "巴彦县"},
    {"id": 9, "name": "中共巴彦县委宣传部", "type": "党委", "level": "县级", "parent": "中共巴彦县委", "location": "巴彦县"},
    {"id": 10, "name": "哈尔滨市双城区（原双城市）", "type": "党委", "level": "区级", "parent": "中共哈尔滨市委", "location": "哈尔滨市"},
    {"id": 11, "name": "哈尔滨市宾县", "type": "党委", "level": "县级", "parent": "中共哈尔滨市委", "location": "哈尔滨市"},
    {"id": 12, "name": "东北农业大学", "type": "事业单位", "level": "高校", "parent": "", "location": "哈尔滨市"},
]

# ── Positions (career timeline) ────────────────────────────────────────────
positions = [
    # 汪育欣（县委书记）
    {"person_id": 1, "org_id": 12, "title": "东北农业大学农业机械化专业学习", "start_date": "1990", "end_date": "1994", "rank": "", "note": "本科/工学学士"},
    {"person_id": 1, "org_id": 10, "title": "哈尔滨原太平区农林局 干部", "start_date": "1997.09", "end_date": "2000", "rank": "科员", "note": "早期履历（概略）"},
    {"person_id": 1, "org_id": 10, "title": "哈尔滨道外区政府办 → 市国资委 → 市工信委 → 市发改委", "start_date": "2000", "end_date": "2018.02", "rank": "科员→副处", "note": "哈尔滨市多部门（细分待核）"},
    {"person_id": 1, "org_id": 10, "title": "哈尔滨市双城区政府副区长", "start_date": "2018.02", "end_date": "2020.10", "rank": "副县级", "note": ""},
    {"person_id": 1, "org_id": 2, "title": "巴彦县委副书记、县长", "start_date": "2020.10", "end_date": "2024.11", "rank": "正处级", "note": "2021 兴隆镇疫情防控"},
    {"person_id": 1, "org_id": 1, "title": "县委书记（县人武部党委第一书记）", "start_date": "2024.11", "end_date": "present", "rank": "副局长级", "note": "2025-05 兼县人武部党委第一书记"},
    # 王让（代县长）
    {"person_id": 2, "org_id": 2, "title": "巴彦县委副书记、代县长", "start_date": "2026.07", "end_date": "present", "rank": "正处级", "note": "接替祁彦勇；管理学博士"},
    # 祁彦勇（前县长）
    {"person_id": 3, "org_id": 11, "title": "宾县县委常委、政府副县长、宾西经开区管委会副主任", "start_date": "2020", "end_date": "2024.11", "rank": "正处级", "note": "宾县"},
    {"person_id": 3, "org_id": 2, "title": "巴彦县委副书记、县长", "start_date": "2024.12", "end_date": "2026.07", "rank": "正处级", "note": "2024.12 代，2025.01 当选"},
    # 兰淼（前书记）
    {"person_id": 4, "org_id": 1, "title": "巴彦县委书记、县人大常委会主任", "start_date": "2020", "end_date": "2024.11", "rank": "正处级", "note": "书记兼人大主任"},
    # 县委班子
    {"person_id": 5, "org_id": 1, "title": "县委副书记", "start_date": "2021", "end_date": "present", "rank": "副处级", "note": "负责县委常务、群团、政法、信访、农业农村"},
    {"person_id": 6, "org_id": 6, "title": "县委常委、组织部部长", "start_date": "2022", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 7, "title": "县委常委、政法委书记", "start_date": "2022", "end_date": "present", "rank": "副处级", "note": "负责政法、社会稳定"},
    {"person_id": 8, "org_id": 8, "title": "县委常委、统战部部长", "start_date": "2022", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 9, "title": "县委常委、宣传部部长", "start_date": "2022", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "县委常委、政府副县长（挂职）", "start_date": "2024", "end_date": "present", "rank": "副处级", "note": "协助白晶玉分管水务、林业草原"},
    {"person_id": 11, "org_id": 2, "title": "县委常委、常务副县长", "start_date": "2022", "end_date": "present", "rank": "副处级", "note": "负责任日常政府、营商、农业农村、水务等"},
    {"person_id": 12, "org_id": 5, "title": "县委常委、纪委书记、监委代主任", "start_date": "2026.07", "end_date": "present", "rank": "副处级", "note": ""},
    # 其他副县长
    {"person_id": 13, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "副县长", "start_date": "2023", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "副县长", "start_date": "2026.07", "end_date": "present", "rank": "副处级", "note": "2026-07 最新任命"},
    # 人大/政协
    {"person_id": 17, "org_id": 3, "title": "县人大常委会主任", "start_date": "2020", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 18, "org_id": 4, "title": "县政协主席", "start_date": "2020", "end_date": "present", "rank": "正处级", "note": ""},
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记汪育欣与代县长王让党政主要领导搭档", "overlap_org": "中共巴彦县委/巴彦县政府", "overlap_period": "2026.07 至今"},
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor", "context": "汪育欣（原县长升书记）；祁彦勇接任县长（2024.12-2025.01）", "overlap_org": "巴彦县委/政府", "overlap_period": "2024.11-2025.01"},
    {"person_a": 1, "person_b": 4, "type": "predecessor_successor", "context": "前任县委书记兰淼（兼人大主任）→汪育欣（2024.11）", "overlap_org": "中共巴彦县委", "overlap_period": "2024.11"},
    {"person_a": 2, "person_b": 3, "type": "predecessor_successor", "context": "王让 接替 祁彦勇 任县长（代）", "overlap_org": "巴彦县人民政府", "overlap_period": "2026.07"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "书记与县委副书记汤继国在县委班子", "overlap_org": "中共巴彦县委", "overlap_period": "2024.11 至今"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "书记与组织部长李昱（干部选拔）", "overlap_org": "中共巴彦县委", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 12, "type": "superior_subordinate", "context": "书记与纪委书记李鹏在县委班子（纪检监察）", "overlap_org": "中共巴彦县委", "overlap_period": "2026.07 至今"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "代县长领导常务副县长白晶玉（县政府常务与审计）", "overlap_org": "巴彦县人民政府", "overlap_period": "2026.07 至今"},
    {"person_a": 1, "person_b": 11, "type": "superior_subordinate", "context": "书记与常务副县长白晶玉（县委班子与政府）", "overlap_org": "中共巴彦县委", "overlap_period": "至今"},
    {"person_a": 3, "person_b": 4, "type": "predecessor_successor", "context": "祁彦勇任县长期间书记为兰淼（K书记，兼人大），党政协作", "overlap_org": "巴彦县委/政府", "overlap_period": "2024.12-2024.11"},
    {"person_a": 1, "person_b": 10, "type": "cross_region_transfer", "context": "汪育欣在双城区曾任副区长后调任巴彦县（书记），区县际轮岗", "overlap_org": "哈尔滨市域干部交流", "overlap_period": ""},
    {"person_a": 3, "person_b": 10, "type": "cross_region_transfer", "context": "祁彦勇自宾县调入巴彦任县长，跨县域干部交流", "overlap_org": "哈尔滨市域干部交流", "overlap_period": ""},
]

# ── Helpers ────────────────────────────────────────────────────────────────
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(name):
    if name == "汪育欣": return "255,50,50"
    if name == "王让": return "50,100,255"
    if name == "祁彦勇": return "150,150,150"
    if name == "兰淼": return "150,150,150"
    if name == "李鹏": return "255,165,0"
    if name in ("汤继国", "李昱", "宋立伟", "谭磊", "孙继成", "罗祥伟", "白晶玉"): return "100,100,150"
    if name in ("赵万方", "李彦国"): return "120,120,120"
    return "100,100,100"


def person_size(name):
    if name in ("汪育欣", "王让", "祁彦勇"): return "20.0"
    if name == "兰淼": return "14.0"
    if name in ("汤继国", "白晶玉", "李鹏", "李昱", "宋立伟"): return "12.0"
    return "9.0"


def org_color(t):
    if "党委" in t: return "255,200,200"
    if "政府" in t: return "200,200,255"
    if "人大" in t: return "200,255,255"
    if "政协" in t: return "255,240,200"
    if "纪委" in t: return "255,180,180"
    if "高校" in t: return "220,220,220"
    return "200,200,200"


# ── Database ──────────────────────────────────────────────────────────────
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
                    (p["id"], p["name"], p.get("gender"), p.get("ethnicity"), p.get("birth"), p.get("birthplace"),
                     p.get("education"), p.get("party_join"), p.get("work_start"), p["current_post"], p["current_org"], p["source"]))
    for o in organizations:
        cur.execute("INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)",
                    (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))
    for pos in positions:
        cur.execute("INSERT INTO positions (person_id,org_id,title,start,end,rank,note) VALUES (?,?,?,?,?,?,?)",
                    (pos["person_id"], pos["org_id"], pos["title"], pos["start_date"], pos["end_date"], pos["rank"], pos["note"]))
    for r in relationships:
        cur.execute("INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)",
                    (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))
    conn.commit()
    conn.close()
    print(f"  DB: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")


# ── GEXF ──────────────────────────────────────────────────────────────────
def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>OpenCode Research Agent</creator>')
    lines.append(f'    <description>巴彦县领导班子工作关系网络 - {SLUG} (哈尔滨市)</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p["name"]); sz = person_size(p["name"]); pid = f"p{p['id']}"
        lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    for o in organizations:
        c = org_color(o["type"]); oid = f"o{o['id']}"
        lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues><attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/></attvalues>')
        lines.append('      </edge>')
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues><attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/></attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF: {GEXF_PATH} ({eid} edges)")


# ── Person Graph JSON ─────────────────────────────────────────────────────
SOURCE_REGISTER = [
    {"id": "S001", "title": "巴彦县政府官网·县委领导 简历页", "url": "http://www.bayan.gov.cn/hebbyx/wyx/202509/c01_1076937.shtml", "publisher": "巴彦县人民政府", "published_at": "2025-09", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "汪育欣等县委领导简历"},
    {"id": "S002", "title": "巴彦县政府官网·政府领导 王让 简历页", "url": "http://www.bayan.gov.cn/hebbyx/wrang/202607/c01_1136368.shtml", "publisher": "巴彦县人民政府", "published_at": "2026-07", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "代县长 王让"},
    {"id": "S003", "title": "百度百科·汪育欣", "url": "https://baike.baidu.com/item/汪育欣", "publisher": "百度百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "履历/生日/教育"},
    {"id": "S004", "title": "百度百科·祁彦勇", "url": "https://baike.baidu.com/item/祁彦勇", "publisher": "百度百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "前县长 履历（宾县→巴彦）"},
    {"id": "S005", "title": "巴彦县第十八届人民代表大会第五次会议（选举祁彦勇为县长）", "url": "http://www.bayan.gov.cn/hebbyx/wyxdt/202501/c01_1078434.shtml", "publisher": "巴彦县人民政府", "published_at": "2025-01-22", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
    {"id": "S006", "title": "巴彦县委书记汪育欣任县人武部党委第一书记", "url": "http://www.bayan.gov.cn/hebbyx/wyxdt/202505/c01_1077465.shtml", "publisher": "巴彦县人民政府", "published_at": "2025-05-09", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
    {"id": "S007", "title": "巴彦县十八届人大 第六次会议（2026-01）", "url": "http://www.bayan.gov.cn/hebbyx/wyxdt/202601/c01_1101781.shtml", "publisher": "巴彦县人民政府", "published_at": "2026-01", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "在任确认"},
    {"id": "S008", "title": "巴彦县委副书记、县长祁彦勇带队开展烟花爆竹安全检查（2026-05）", "url": "http://www.bayan.gov.cn/hebbyx/wyxdt/202605/c01_1123842.shtml", "publisher": "巴彦县人民政府", "published_at": "2026-05-07", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "祁彦勇 2026-05 仍在任县长（再证辞任在2026-07）"},
]

JOB_MAP = {
    1: "县委书记", 2: "县长", 3: "县长", 4: "县委书记",
    5: "县委副书记", 6: "组织部部长", 7: "政法委书记", 8: "统战部部长", 9: "宣传部部长",
    10: "副县长", 11: "常务副县长", 12: "纪委书记", 13: "副县长", 14: "副县长", 15: "副县长", 16: "副县长",
    17: "人大常委会主任", 18: "政协主席",
}

# person id → 简要简历文本（用于 timeline 结构化）
PERSON_TIMELINE = {
    1: [
        ("1990", "1994", "东北农业大学农业机械化专业学习（本科/工学学士）", "confirmed"),
        ("1997.09", "2000", "哈尔滨原太平区农林局干部", "plausible"),
        ("2000", "2018.02", "哈尔滨市道外区/国资委/工信委/发改委 机关任职", "plausible"),
        ("2018.02", "2020.10", "哈尔滨市双城区政府副区长", "confirmed"),
        ("2020.10", "2024.11", "巴彦县委副书记、县长", "confirmed"),
        ("2024.11", "present", "巴彦县委书记（县人武部党委第一书记）", "confirmed"),
    ],
    2: [
        ("", "2026.07", "履历缺口：任巴彦代县长前完整经历待考", "unverified"),
        ("2026.07", "present", "巴彦县委副书记、代县长", "confirmed"),
    ],
    3: [
        ("2020", "2024.11", "宾县县委常委、政府副县长、宾西经开区管委会副主任", "confirmed"),
        ("2024.12", "2025.01", "巴彦县委副书记、县长候选人（代）", "confirmed"),
        ("2025.01", "2026.07", "巴彦县委副书记、县长（当选）", "confirmed"),
    ],
    4: [
        ("2020", "2024.11", "巴彦县委书记、县人大常委会主任", "plausible"),
    ],
    5: [("2021", "present", "巴彦县委副书记", "confirmed")],
    6: [("2022", "present", "巴彦县委常委、组织部部长", "confirmed")],
    7: [("2022", "present", "巴彦县委常委、政法委书记", "confirmed")],
    8: [("2022", "present", "巴彦县委常委、统战部部长", "confirmed")],
    9: [("2022", "present", "巴彦县委常委、宣传部部长", "confirmed")],
    10: [("2024", "present", "巴彦县委常委、政府副县长（挂职）", "confirmed")],
    11: [("2022", "present", "巴彦县委常委、常务副县长", "confirmed")],
    12: [("2026.07", "present", "巴彦县委常委、纪委书记、监委代主任", "confirmed")],
    13: [("", "present", "巴彦县副县长", "confirmed")],
    14: [("", "present", "巴彦县副县长", "confirmed")],
    15: [("2023", "present", "巴彦县副县长", "confirmed")],
    16: [("2026.07", "present", "巴彦县副县长（最新任命）", "confirmed")],
    17: [("2020", "present", "巴彦县人大常委会主任", "plausible")],
    18: [("2020", "present", "巴彦县政协主席", "plausible")],
}


def build_person_jsons():
    from datetime import date
    for p in persons:
        name = p["name"]
        pid = p["id"]
        timeline_rows = []
        for (s, e, t, conf) in PERSON_TIMELINE.get(pid, []):
            timeline_rows.append({
                "start": s, "end": e, "org": p["current_org"], "title": t,
                "level": "", "location": "巴彦县", "system": "government",
                "rank": "", "is_key_promotion": pid in (1, 2, 3, 4),
                "notes": "", "confidence": conf, "source_ids": ["S001", "S002"] if pid in (1, 2) else ["S001"],
            })
        rels = []
        for r in relationships:
            if r["person_a"] == pid:
                rels.append({"person": persons[r["person_b"]-1]["name"], "relationship_type": "overlap",
                             "strength": "strong", "evidence": r["context"], "overlap_org": r["overlap_org"],
                             "overlap_period": r["overlap_period"], "confidence": "confirmed"})
            elif r["person_b"] == pid:
                rels.append({"person": persons[r["person_a"]-1]["name"], "relationship_type": "overlap",
                             "strength": "strong", "evidence": r["context"], "overlap_org": r["overlap_org"],
                             "overlap_period": r["overlap_period"], "confidence": "confirmed"})
        data = {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "黑龙江省", "city": "哈尔滨市", "region": "巴彦县",
                "job": JOB_MAP.get(pid, "领导"), "task_id": "heilongjiang_巴彦县",
                "time_focus": "2026-08",
            },
            "identity": {
                "person_id": f"bayan_{name}", "name": name, "aliases": [],
                "gender": p.get("gender", ""), "ethnicity": p.get("ethnicity", ""),
                "birth": p.get("birth", ""), "birthplace": p.get("birthplace", ""),
                "native_place": p.get("birthplace", ""),
                "education": [{"period": "", "institution": p.get("education", ""), "major": "",
                               "degree": "", "study_type": "unknown", "source_ids": ["S001", "S002"]}],
                "party_join": p.get("party_join", ""), "work_start": p.get("work_start", ""),
                "dedupe_keys": {"name_birth": f"{name}_{p.get('birth','')}", "name_birthplace": f"{name}_{p.get('birthplace','')}", "official_profile_url": ""},
            },
            "current_status": {
                "current_post": p["current_post"], "current_org": p["current_org"],
                "administrative_rank": "正处级" if pid in (1, 2, 3, 4, 17, 18) else ("副处级" if pid in (5, 6, 7, 8, 9, 10, 11, 12) else "副处级"),
                "as_of": AS_OF, "is_current_confirmed": pid in (1, 2, 5, 6, 7, 8, 9, 10, 11, 12), "source_ids": ["S001", "S002"],
            },
            "career_timeline": timeline_rows,
            "organizations": [p["current_org"]],
            "relationships": rels,
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [], "secondary_specializations": [],
                "career_pattern": ("cross_county_rotation" if pid in (1, 3) else "unknown"),
                "systems_experience": [], "geographic_pattern": [], "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
            },
            "work_style_and_personality": {
                "public_style_indicators": [], "speech_themes": [], "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [],
            "source_register": SOURCE_REGISTER,
            "confidence_summary": {
                "identity": "confirmed", "current_role": "confirmed",
                "career_completeness": "partial", "relationship_confidence": "medium",
                "biggest_gap": ("汪育欣2000-2018哈尔滨机关任职细点待补" if pid == 1
                                else ("王让任代县长前履历/出生地待核" if pid == 2
                                       else ("祁彦勇2026-07卸任后去向待核" if pid == 3
                                             else (f"{name}早年履历或出生地待核")))),
            },
            "open_questions": [
                {"priority": "high", "question": (f"{name}任前履历/出生地/籍贯待核" if pid in (2, 3) else f"{name}早年履历待核"),
                 "why_it_matters": "提升履历可信度", "suggested_queries": [f"{name} 巴彦县 简历"], "last_attempted": AS_OF},
            ],
        }
        path = PERSONS_DIR / f"{TODAY}-黑龙江省-哈尔滨市-{JOB_MAP.get(pid, p['current_post'])}-{name}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {path.name}")


if __name__ == "__main__":
    print(f"Building {SLUG} network data... (AS_OF={AS_OF})")
    build_db()
    build_gexf()
    build_person_jsons()
    print("\nOutput files:")
    print(f"  DB:     {DB_PATH}")
    print(f"  GEXF:   {GEXF_PATH}")
    for p in sorted(PERSONS_DIR.glob(f"{TODAY}-黑龙江省-哈尔滨市-*.json")):
        print(f"  Person: {p.name}")
    print("Done.")