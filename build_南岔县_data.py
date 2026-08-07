#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 南岔县 (Nanchang County), 伊春市, 黑龙江省.

Investigation date: 2026-08-05
Task ID: heilongjiang_南岔县
Level: 县
Targets: 县委书记 (段红波) & 县长 (赵磊)

Research sources (official, primary, nancha.gov.cn — all reachable):
  - 南岔县人民政府官网 http://www.nancha.gov.cn/  (领导信息/机构简介栏目, 更新2026-01-06)
  - 2026年度县级河湖长工作分工 (官网通知公告 2026-07-29, URL c100686/202607/431144.shtml) — 确认
    县委书记段红波(总河长)、县委副书记县长赵磊(总河长)及全部县处级河长分工，即完整县领导班子名册
  - 南岔县人民政府官网政府信息公开年报/政策文件 (2026)
  - 搜狗检索快照 (张巍曾任南岔县委书记, 2021-2022; 2022高考巡视报道)

Research Note (partial-evidence artifact mode, source_fallbacks.md):
  www.nancha.gov.cn 完整可访问，确认核心党政一把手、县委班子、县政府班子及人大/政协副职。
  - 现任县委书记：段红波（官方河湖长分工2026-07-29确认"县委书记段红波（总河长）"）
  - 现任县委副书记、县长：赵磊（官方河长分工确认"县委副书记、县长赵磊"；原县委常委、常务副县长，
    2026年由段红波升任县委书记后接任县委副书记、县长）
  - 前任县委书记：张巍（女，2021-2022年在任；2026年现任状态未从一手源核实，履历缺口）
  - 县委班子：专职副书记李晶才；常委王丽娜(政法委)、郑海涛(常务副县)、徐金明(纪委)、
    孙召军(组织)、公芷(宣传)、高明达(副县)
  - 县政府：县长赵磊；副县长李凯峰(公安)、张猛、许斌、于莹、高明达；党组成员杨恒
  - 县人大：副主任马曙光、郝玉彬、刘玉海（主任未确认）；县政协：副主席曹淑红、林淑梅、曹德顺（主席未确认）
  依 partial-evidence artifact mode，仍产出结构有效产物，并以 confidence/open_questions/report 标记不确定性。
"""

import json
import sqlite3
import os
from datetime import datetime
from pathlib import Path

BASE = os.path.dirname(os.path.abspath(__file__))
SLUG = "南岔县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = TODAY

DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")
PERSONS_DIR = Path(BASE)

# ── Persons ────────────────────────────────────────────────────────────────

persons = [
    # 核心党政一把手
    {"id": 1, "name": "段红波", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县委书记", "current_org": "中共南岔县委员会",
     "source": "南岔县人民政府官网河湖长分工（2026-07-29），原文《县委书记段红波（总河长）》"},
    {"id": 2, "name": "赵磊", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县委副书记、县长", "current_org": "南岔县人民政府",
     "source": "南岔县人民政府官网河湖长分工（2026-07-29），原文《县委副书记、县长（总河长）赵磊》"},
    # 县委班子
    {"id": 3, "name": "李晶才", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县委副书记（专职）", "current_org": "中共南岔县委员会",
     "source": "南岔县河湖长分工（2026-07-29）"},
    {"id": 4, "name": "王丽娜", "gender": "女", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、政法委书记", "current_org": "中共南岔县委员会",
     "source": "南岔县河湖长分工（2026-07-29）"},
    {"id": 5, "name": "郑海涛", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、常务副县长", "current_org": "南岔县人民政府",
     "source": "南岔县河湖长分工（2026-07-29）"},
    {"id": 6, "name": "徐金明", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、纪委书记、监委主任", "current_org": "中共南岔县纪律检查委员会",
     "source": "南岔县河湖长分工（2026-07-29）"},
    {"id": 7, "name": "孙召军", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、组织部部长", "current_org": "中共南岔县委员会",
     "source": "南岔县河湖长分工（2026-07-29）"},
    {"id": 8, "name": "公正", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、宣传部部长", "current_org": "中共南岔县委员会",
     "source": "南岔县河湖长分工（2026-07-29）"},
    {"id": 9, "name": "高明达", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、县政府副县长", "current_org": "南岔县人民政府",
     "source": "南岔县河湖长分工（2026-07-29）"},
    # 县政府班子
    {"id": 10, "name": "李凯峰", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县政府副县长、公安局局长", "current_org": "南岔县人民政府",
     "source": "南岔县河湖长分工（2026-07-29）；政府领导信息页（2026-01-06）"},
    {"id": 11, "name": "张猛", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县政府副县长", "current_org": "南岔县人民政府",
     "source": "南岔县河湖长分工（2026-07-29）"},
    {"id": 13, "name": "于莹", "gender": "女", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县政府副县长", "current_org": "南岔县人民政府",
     "source": "南岔县河湖长分工（2026-07-29）"},
    {"id": 14, "name": "许斌", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县政府副县长", "current_org": "南岔县人民政府",
     "source": "南岔县河湖长分工（2026-07-29）；领导信息页（2024-05）"},
    {"id": 15, "name": "杨恒", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县政府党组成员", "current_org": "南岔县人民政府",
     "source": "南岔县河湖长分工（2026-07-29）"},
    # 人大 / 政协
    {"id": 16, "name": "马曙光", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县人大常委会副主任", "current_org": "南岔县人民代表大会常务委员会",
     "source": "南岔县河湖长分工（2026-07-29）"},
    {"id": 17, "name": "郝玉彬", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县人大常委会副主任", "current_org": "南岔县人民代表大会常务委员会",
     "source": "南岔县河湖长分工（2026-07-29）"},
    {"id": 18, "name": "刘玉海", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县人大常委会副主任", "current_org": "南岔县人民代表大会常务委员会",
     "source": "南岔县河湖长分工（2026-07-29）"},
    {"id": 19, "name": "马淑红", "gender": "女", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县政协副主席", "current_org": "政协南岔县委员会",
     "source": "南岔县河湖长分工（2026-07-29）"},
    {"id": 20, "name": "林淑梅", "gender": "女", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县政协副主席", "current_org": "政协南岔县委员会",
     "source": "南岔县河湖长分工（2026-07-29）"},
    {"id": 21, "name": "曹德顺", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县政协副主席", "current_org": "政协南岔县委员会",
     "source": "南岔县河湖长分工（2026-07-29）"},
    # 前任县委书记（继任链上下文）
    {"id": 22, "name": "张巍", "gender": "女", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "前任南岔县委书记（2021-2022在任，现任去向待查）", "current_org": "中共南岔县委员会",
     "source": "搜狗检索稿件（2022高考巡视报道：县委书记张巍深入南岔考区；2021-08 疫情防控会议《张巍指出》）"},
    # 伊春市级领导（跨区域上下文）
    {"id": 23, "name": "董文琴", "gender": "女", "ethnicity": "汉族", "birth": "1972年10月",
     "birthplace": "黑龙江省宾县", "education": "省委党校研究生", "party_join": "中共党员", "work_start": "",
     "current_post": "伊春市委书记、市人大常委会主任", "current_org": "中共伊春市委员会",
     "source": "伊春市政务信息（同仓 20260805-heilongjiang伊春市）"},
    {"id": 24, "name": "苑芳江", "gender": "男", "ethnicity": "汉族", "birth": "1977年3月",
     "birthplace": "黑龙江省穆棱市", "education": "在职研究生，法学博士", "party_join": "中共党员", "work_start": "",
     "current_post": "伊春市委副书记、市长", "current_org": "伊春市人民政府",
     "source": "伊春市政务信息（同仓 20260805-heilongjiang伊春市）"},
]

# ── Organizations ──────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共南岔县委员会", "type": "党委", "level": "县处级", "parent": "中共伊春市委员会", "location": "黑龙江省伊春市南岔县"},
    {"id": 2, "name": "南岔县人民政府", "type": "政府", "level": "县处级", "parent": "伊春市人民政府", "location": "黑龙江省伊春市南岔县"},
    {"id": 3, "name": "南岔县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "伊春市人大常委会", "location": "黑龙江省伊春市南岔县"},
    {"id": 4, "name": "政协南岔县委员会", "type": "政协", "level": "县处级", "parent": "政协伊春市委员会", "location": "黑龙江省伊春市南岔县"},
    {"id": 5, "name": "中共南岔县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共伊春市纪律检查委员会", "location": "黑龙江省伊春市南岔县"},
    {"id": 6, "name": "南岔县公安局", "type": "政府", "level": "乡科级", "parent": "南岔县人民政府", "location": "黑龙江省伊春市南岔县"},
    {"id": 7, "name": "中共伊春市委员会", "type": "党委", "level": "地市级", "parent": "中共黑龙江省委员会", "location": "黑龙江省伊春市"},
    {"id": 8, "name": "伊春市人民政府", "type": "政府", "level": "地市级", "parent": "黑龙江省人民政府", "location": "黑龙江省伊春市"},
]

# ── Positions ──────────────────────────────────────────────────────────────

positions = [
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "", "end": "", "rank": "县处级正职", "note": "官方2026-07-29河湖长分工《县书记段红波（总河长）》；曾任县长（2026-01-06领导信息页列《县长段红波》），2026年升任县委书记"},
    {"person_id": 1, "org_id": 2, "title": "县长（前任职）", "start": "", "end": "2026", "rank": "县处级正职", "note": "2026-01-06领导信息页列县长段红波；后升任县委书记"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "", "end": "", "rank": "县处级副职", "note": "河长分工确认县委副书记"},
    {"person_id": 2, "org_id": 2, "title": "南岔县长", "start": "", "end": "", "rank": "县处级正职", "note": "河长分工《县长赵磊（总河长）》；分管政府全面工作（沿前述分工）"},
    {"person_id": 2, "org_id": 1, "title": "（曾任）县委常委、副县长", "start": "", "end": "2026", "rank": "县处级副职", "note": "2026-01-06领导信息页列县委常委、副县长；后接任县长"},
    {"person_id": 3, "org_id": 1, "title": "县委副书记（专职）", "start": "", "end": "", "rank": "县处级副职", "note": "河湖长分工：县委常委、县委副书记"},
    {"person_id": 4, "org_id": 1, "title": "县委常委、政法委书记", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start": "", "end": "", "rank": "县处级副职", "note": "河长分工：县委常委"},
    {"person_id": 5, "org_id": 2, "title": "常务副县长", "start": "", "end": "", "rank": "县处级副职", "note": "分管政府常务"},
    {"person_id": 6, "org_id": 1, "title": "县委常委、纪委书记", "start": "", "end": "", "rank": "县处级副职", "note": "兼监委主任"},
    {"person_id": 6, "org_id": 5, "title": "县纪委书记、监委主任", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "县委常委、组织部部长", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "县委常委、宣传部部长", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副县长", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副县长", "start": "", "end": "", "rank": "县处级副职", "note": "负责公共安全、社会稳定、城镇防火；分管县信访局、县公安局、消防救援大队"},
    {"person_id": 10, "org_id": 6, "title": "公安局长", "start": "", "end": "", "rank": "正科级", "note": "副县长兼公安局长"},
    {"person_id": 11, "org_id": 2, "title": "副县长", "start": "", "end": "", "rank": "县处级副职", "note": "负责交通运输、农业水利、司法行政；分管县交通局、县农业农村局、县司法局"},
    {"person_id": 13, "org_id": 2, "title": "副县长", "start": "", "end": "", "rank": "县处级副职", "note": "负责人事社保、教育卫生、医疗保障；分管县人社局、教育局、卫健局、医保局"},
    {"person_id": 14, "org_id": 2, "title": "副县长", "start": "", "end": "", "rank": "县处级副职", "note": "负责退役军人、市场监管、营商环境；分管退役军人事务局、市监局、营商局"},
    {"person_id": 15, "org_id": 2, "title": "县政府党组成员", "start": "", "end": "", "rank": "县处级", "note": ""},
    {"person_id": 16, "org_id": 3, "title": "县人大常委会副主任", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 17, "org_id": 3, "title": "县人大常委会副主任", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 18, "org_id": 3, "title": "县人大常委会副主任", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 19, "org_id": 4, "title": "县政协副主席", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 20, "org_id": 4, "title": "县政协副主席", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 21, "org_id": 4, "title": "县政协副主席", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 22, "org_id": 1, "title": "南岔县委书记（前任）", "start": "2021", "end": "2022", "rank": "县处级正职", "note": "2021-08疫情防控会议、2022高考巡视均称县委书记；现任去向待查"},
    {"person_id": 23, "org_id": 7, "title": "伊春市委书记", "start": "2024-09", "end": "", "rank": "地厅级正职", "note": "市人大常委会主任"},
    {"person_id": 24, "org_id": 8, "title": "伊春市市长", "start": "2024-09", "end": "", "rank": "地厅级正职", "note": ""},
]

# ── Relationships ──────────────────────────────────────────────────────────

relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "县委书记段红波与县委副书记、县长赵磊党政一把手搭档", "overlap_org": "南岔县", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 2, "type": "继任链", "context": "段红波由县长升任县委书记，赵磊由常务副县长接任县长——正副县长上行继任", "overlap_org": "南岔县人民政府", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 22, "type": "继任链", "context": "段红波接替前任书记（张巍为2021-2022在任者）", "overlap_org": "中共南岔县委员会", "overlap_period": "2021-2026"},
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "县委书记领导专职副书记李晶才", "overlap_org": "中共南岔县委员会", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "县委书记领导政法委书记王丽娜", "overlap_org": "中共南岔县委员会", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "县委书记领导常务副县长郑海涛", "overlap_org": "中共南岔县委员会", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "县委书记领导纪委书记徐金明", "overlap_org": "中共南岔县委员会", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "县委书记领导组织部长孙召军", "overlap_org": "中共南岔县委员会", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "县长领导常务副县长郑海涛", "overlap_org": "南岔县人民政府", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "县长领导公安副县长李凯峰", "overlap_org": "南岔县人民政府", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 11, "type": "上下级", "context": "县长领导副县长张猛", "overlap_org": "南岔县人民政府", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 13, "type": "上下级", "context": "县长领导副县长于莹", "overlap_org": "南岔县人民政府", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 14, "type": "上下级", "context": "县长领导副县长许斌", "overlap_org": "南岔县人民政府", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 23, "type": "上下级", "context": "伊春市委书记董文琴领导南岔县委书记", "overlap_org": "伊春市", "overlap_period": "2024-"},
    {"person_a": 2, "person_b": 24, "type": "上下级", "context": "伊春市市长苑芳江领导南岔县长", "overlap_org": "伊春市人民政府", "overlap_period": "2024-"},
    {"person_a": 1, "person_b": 16, "type": "同僚", "context": "县委书记与县人大副主任马曙光同县工作", "overlap_org": "南岔县", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 19, "type": "同僚", "context": "县长与县政协副主席马淑红同县工作", "overlap_org": "南岔县", "overlap_period": "2026-"},
]


# ══════════════════════════════════════════════════════════════════════════
# SQLite DB Builder
# ══════════════════════════════════════════════════════════════════════════

esc = lambda s: (str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;") if s is not None else "")

def build_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    for t in ("relationships","positions","organizations","persons"):
        cur.execute(f"DROP TABLE IF EXISTS {t}")
    cur.execute("""CREATE TABLE persons (
        id INTEGER PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
        birthplace TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT, source TEXT)""")
    cur.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT)""")
    cur.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER, org_id INTEGER,
        title TEXT, start_date TEXT, end_date TEXT, rank TEXT, note TEXT)""")
    cur.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT, person_a INTEGER, person_b INTEGER,
        type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT)""")
    for p in persons:
        cur.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                    (p["id"],p["name"],p["gender"],p["ethnicity"],p["birth"],p["birthplace"],
                     p["education"],p["party_join"],p["work_start"],p["current_post"],p["current_org"],p["source"]))
    for o in organizations:
        cur.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)",
                    (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"]))
    for pos in positions:
        cur.execute("INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)",
                    (pos["person_id"],pos["org_id"],pos["title"],pos.get("start",""),pos.get("end",""),pos.get("rank",""),pos.get("note","")))
    for r in relationships:
        cur.execute("INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)",
                    (r["person_a"],r["person_b"],r["type"],r["context"],r["overlap_org"],r["overlap_period"]))
    conn.commit(); conn.close()
    print(f"  DB: {DB_PATH} ({len(persons)}p, {len(organizations)}o, {len(positions)}pos, {len(relationships)}rel)")


# ══════════════════════════════════════════════════════════════════════════
# GEXF Graph Builder
# ══════════════════════════════════════════════════════════════════════════

def person_color(post):
    if post and post.strip() == "县委书记":
        return ("255,50,50", 20.0)
    if "县长" in post and "副" not in post and post.strip() != "县长（前任职）":
        return ("50,100,255", 20.0)
    if "县委副书记" in post or "常务副县长" in post:
        return ("100,150,255", 12.0)
    if "副县长" in post:
        return ("100,150,255", 12.0)
    if "常委" in post:
        return ("120,120,120", 12.0)
    if "政协" in post or "人大常委会" in post:
        return ("120,180,120", 12.0)
    return ("100,100,100", 12.0)

def org_color(t):
    colors = {"党委":("255,200,200",8.0),"政府":("200,200,255",8.0),"纪委":("255,200,200",8.0),
              "人大":("200,255,255",8.0),"政协":("255,240,200",8.0),"乡镇":("255,255,200",8.0),
              "司法":("220,200,220",8.0)}
    return colors.get(t, ("200,200,200", 8.0))


def build_gexf():
    from datetime import datetime as _dt
    L = []
    L.append('<?xml version="1.0" encoding="UTF-8"?>')
    L.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    L.append(f'  <meta lastmodifieddate="{_dt.now().strftime("%Y-%m-%d")}">')
    L.append('    <creator>Sisyphus Research Agent</creator>')
    L.append(f'    <description>南岔县领导班子工作关系网络 - {AS_OF}</description>')
    L.append('  </meta>')
    L.append('  <graph mode="static" defaultedgetype="undirected">')
    L.append('    <attributes class="node">')
    L.append('      <attribute id="0" title="type" type="string"/>')
    L.append('      <attribute id="1" title="current_post" type="string"/>')
    L.append('      <attribute id="2" title="current_org" type="string"/>')
    L.append('      <attribute id="3" title="birth" type="string"/>')
    L.append('    </attributes>')
    L.append('    <attributes class="edge">')
    L.append('      <attribute id="0" title="type" type="string"/>')
    L.append('      <attribute id="1" title="context" type="string"/>')
    L.append('    </attributes>')
    L.append('    <nodes>')
    for p in persons:
        c, sz = person_color(p["current_post"])
        L.append(f'      <node id="{p["id"]}" label="{esc(p["name"])}">')
        L.append('        <attvalues>')
        L.append(f'          <attvalue for="0" value="person"/>')
        L.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        L.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        L.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        L.append('        </attvalues>')
        L.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        L.append(f'        <viz:size value="{sz}"/>')
        L.append('      </node>')
    for o in organizations:
        c, sz = org_color(o["type"])
        L.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        L.append('        <attvalues>')
        L.append('          <attvalue for="0" value="organization"/>')
        for i in (1, 2, 3):
            L.append(f'          <attvalue for="{i}" value=""/>')
        L.append('        </attvalues>')
        L.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        L.append(f'        <viz:size value="{sz}"/>')
        L.append('      </node>')
    L.append('    </nodes>')
    L.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        L.append(f'      <edge id="{eid}" source="{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        L.append('        <attvalues>')
        L.append(f'          <attvalue for="0" value="worked_at"/>')
        L.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        L.append('        </attvalues>')
        L.append('      </edge>')
    for r in relationships:
        eid += 1
        L.append(f'      <edge id="{eid}" source="{r["person_a"]}" target="{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        L.append('        <attvalues>')
        L.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        L.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        L.append('        </attvalues>')
        L.append('      </edge>')
    L.append('    </edges>')
    L.append('  </graph>')
    L.append('</gexf>')
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print(f"GEXF: {GEXF_PATH}")


if __name__ == "__main__":
    print(f"Building {SLUG} network ({AS_OF})")
    build_db()
    build_gexf()
    print("Done.")