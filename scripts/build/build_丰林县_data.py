#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 丰林县 (Fenglin County), 伊春市, 黑龙江省.

Investigation date: 2026-08-05
Task ID: heilongjiang_丰林县
Level: 县
Targets: 县委书记 (栾皓) & 县长 (原浩东)

Research sources (official, primary):
  - 丰林县人民政府官网 http://www.ycfl.gov.cn/  (政府领导栏目，公开于2026-05-26，提供县政府班子名单及分管)
  - 丰林发布官方微信公众号 (县委常委会/理论学习中心组/警示教育会/统战会议/八一慰问报道, 2026-05〜07)
  - 伊春市人民政府县区动态 (2025 依法治县会议等)
  - 百度检索快照 (姜治富去向/栾皓任职背景)

Research Note (partial-evidence artifact mode, source_fallbacks.md):
  www.ycfl.gov.cn 完整可访问，确认核心党政一把手、县政府班子及分管分工、县人大常委会主任、政协主席更替。
  - 现任县委书记：栾皓（新任，2026年7月下旬到任；官方微信2026-07-31称"县委书记栾皓"；1982年生；
    历岗：铁力市委常委、常务副市长 → 伊春市委副秘书长、办公室主任 → 丰林县委书记）
  - 现任县委副书记、县长：原浩东（政府领导栏目确认；多次主持县委常委会、县政府全面工作，主管县审计局）
  - 前任县委书记：姜治富（1974年生；2020-2026任书记；2025-12升任伊春市副市长；2026-05-26仍以
    "市政府副市长、丰林县委书记"主持113次常委会，至2026年7月由栾皓接任）
  - 县委班子：县委副书记（专职）张强（兼红星镇党委书记）；县委常委：伊琳娜（常委/常务副县长）、
    秦瑞红（常委/新任县政协主席候选人）、朱松岩、张鹏宇、许志坚、祝磊、赵覃、于兴生、颜承君。
    各常委具体"部长/书记"（组织/纪检/政法/宣传/统战/人武）未从已取官方内容唯一判定 —— 履历缺口。
  - 人大常委会主任陈春东；副主任商继荣、肖永成。政协主席候选人秦瑞红（前任徐长伟）。
    法院院长张紫微；检察院检察长李大刚。
  - 前任县长（原浩东前任职）、历任县长：公开资料未确认，履历缺口。
  依 partial-evidence artifact mode，仍产出结构有效产物，并以 confidence/open_questions/report 标记不确定性。
"""

import json
import sqlite3
import os
from datetime import datetime
from pathlib import Path

BASE = os.path.dirname(os.path.abspath(__file__))
SLUG = "丰林县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = TODAY

DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")
PERSONS_DIR = Path(BASE)

# ── Persons ────────────────────────────────────────────────────────────────

persons = [
    # 核心党政一把手
    {"id": 1, "name": "栾皓", "gender": "男", "ethnicity": "", "birth": "1982年",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县委书记", "current_org": "中共丰林县委员会",
     "source": "丰林县委员会门户新闻/官方微信公众号（2026-07-31）"},
    {"id": 2, "name": "原浩东", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县委副书记、县长", "current_org": "丰林县人民政府",
     "source": "http://www.ycfl.gov.cn/flxrmzf/c101439/202205/31639.shtml"},
    # 县委班子
    {"id": 3, "name": "张强", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县委副书记（专职）、红星镇党委书记", "current_org": "中共丰林县委员会",
     "source": "丰林县委理论学习中心组报道（2026-07）"},
    {"id": 4, "name": "伊琳娜", "gender": "女", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、常务副县长", "current_org": "丰林县人民政府",
     "source": "http://www.ycfl.gov.cn/flxrmzf/c1026/202205/31630.shtml"},
    {"id": 5, "name": "秦瑞红", "gender": "女", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、县政协主席", "current_org": "政协丰林县委员会",
     "source": "丰林发布'八一'慰问报道（2026-07-31）"},
    {"id": 6, "name": "朱松岩", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委（职务待细分）", "current_org": "中共丰林县委员会",
     "source": "丰林县委118次常委会报道（2026-07）"},
    {"id": 7, "name": "张鹏宇", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委（职务待细分）", "current_org": "中共丰林县委员会",
     "source": "丰林县委113/118次常委会报道（2026）"},
    {"id": 8, "name": "许志坚", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委（职务待细分）", "current_org": "中共丰林县委员会",
     "source": "丰林县委统一战线工作领导小组/中心组报道（2026）"},
    {"id": 9, "name": "祝磊", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委（职务待细分）", "current_org": "中共丰林县委员会",
     "source": "丰林县委中心组/警示教育会报道（2026）"},
    {"id": 10, "name": "赵覃", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委（职务待细分）", "current_org": "中共丰林县委员会",
     "source": "丰林县委118次常委会报道（2026）"},
    {"id": 11, "name": "于兴生", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委（职务待细分）", "current_org": "中共丰林县委员会",
     "source": "丰林县委113/118次常委会报道（2026）"},
    {"id": 12, "name": "颜承君", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委（职务待细分）", "current_org": "中共丰林县委员会",
     "source": "丰林县委中心组/常委会报道（2026）"},
    # 县政府班子
    {"id": 13, "name": "梁爽", "gender": "女", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县政府副县长", "current_org": "丰林县人民政府",
     "source": "http://www.ycfl.gov.cn/flxrmzf/cfg0/202205/31603.shtml"},
    {"id": 14, "name": "李国平", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县政府副县长（公安、司法）", "current_org": "丰林县人民政府",
     "source": "http://www.ycfl.gov.cn/flxrmzf/cfg0/202205/31611.shtml"},
    {"id": 15, "name": "蒋焕鑫", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县政府副县长", "current_org": "丰林县人民政府",
     "source": "http://www.ycfl.gov.cn/flxrmzf/cfg0/202205/31593.shtml"},
    {"id": 16, "name": "刘宇", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县政府副县长", "current_org": "丰林县人民政府",
     "source": "http://www.ycfl.gov.cn/flxrmzf/cfg0/202205/31620.shtml"},
    {"id": 17, "name": "程楠", "gender": "女", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县政府副县长", "current_org": "丰林县人民政府",
     "source": "http://www.ycfl.gov.cn/flxrmzf/cfg0/202206/31657.shtml"},
    # 人大 / 政协
    {"id": 18, "name": "陈春东", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县人大常委会主任", "current_org": "丰林县人民代表大会常务委员会",
     "source": "丰林县二届人大常委会第24次会议报道（2025）"},
    {"id": 19, "name": "商继荣", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县人大常委会副主任", "current_org": "丰林县人民代表大会常务委员会",
     "source": "丰林县人大常委会会议报道（2025）"},
    {"id": 20, "name": "肖永成", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县人大常委会副主任", "current_org": "丰林县人民代表大会常务委员会",
     "source": "丰林县人大常委会会议报道（2025）"},
    {"id": 21, "name": "徐长伟", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县政协主席（前任，2026-07卸任）", "current_org": "政协丰林县委员会",
     "source": "丰林县一次会议报道（2026-07-10）"},
    # 法检
    {"id": 22, "name": "张紫微", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县人民法院院长", "current_org": "丰林县人民法院",
     "source": "丰林县人大常委会会议报道（2025-03）"},
    {"id": 23, "name": "李大刚", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县人民检察院检察长", "current_org": "丰林县人民检察院",
     "source": "丰林县依法治县会议/人大常委会报道（2026）"},
    # 前任县委书记（继任链上下文）
    {"id": 24, "name": "姜治富", "gender": "男", "ethnicity": "汉族", "birth": "1974年",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "伊春市副市长（曾任丰林县委书记）", "current_org": "伊春市人民政府",
     "source": "百度检索快讯/丰林县委常委会报道（2025-2026）"},
    # 伊春市级领导（跨区域上下文）
    {"id": 25, "name": "董文琴", "gender": "女", "ethnicity": "汉族", "birth": "1972年10月",
     "birthplace": "黑龙江省宾县", "education": "省委党校研究生", "party_join": "中共党员", "work_start": "",
     "current_post": "伊春市委书记、市人大常委会主任", "current_org": "中共伊春市委员会",
     "source": "伊春市政务信息"},
    {"id": 26, "name": "苑芳江", "gender": "男", "ethnicity": "汉族", "birth": "1977年3月",
     "birthplace": "黑龙江省穆棱市", "education": "研究生", "party_join": "中共党员", "work_start": "",
     "current_post": "伊春市委副书记、市长", "current_org": "伊春市人民政府",
     "source": "伊春市政务信息"},
]

# ── Organizations ──────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共丰林县委员会", "type": "党委", "level": "县处级", "parent": "中共伊春市委员会", "location": "黑龙江省伊春市丰林县"},
    {"id": 2, "name": "丰林县人民政府", "type": "政府", "level": "县处级", "parent": "伊春市人民政府", "location": "黑龙江省伊春市丰林县"},
    {"id": 3, "name": "丰林县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "伊春市人大常委会", "location": "黑龙江省伊春市丰林县"},
    {"id": 4, "name": "政协丰林县委员会", "type": "政协", "level": "县处级", "parent": "政协伊春市委员会", "location": "黑龙江省伊春市丰林县"},
    {"id": 5, "name": "中共丰林县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共伊春市纪律检查委员会", "location": "黑龙江省伊春市丰林县"},
    {"id": 6, "name": "丰林县人民法院", "type": "司法", "level": "县处级", "parent": "伊春市中级人民法院", "location": "黑龙江省伊春市丰林县"},
    {"id": 7, "name": "丰林县人民检察院", "type": "司法", "level": "县处级", "parent": "伊春市人民检察院", "location": "黑龙江省伊春市丰林县"},
    {"id": 8, "name": "中共丰林县红星镇委员会", "type": "乡镇", "level": "乡科级", "parent": "中共丰林县委员会", "location": "黑龙江省伊春市丰林县红星镇"},
    {"id": 9, "name": "中共伊春市委员会", "type": "党委", "level": "地市级", "parent": "中共黑龙江省委员会", "location": "黑龙江省伊春市"},
    {"id": 10, "name": "伊春市人民政府", "type": "政府", "level": "地市级", "parent": "黑龙江省人民政府", "location": "黑龙江省伊春市"},
]

# ── Positions ──────────────────────────────────────────────────────────────

positions = [
    {"person_id": 1, "org_id": 1, "title": "丰林县委书记", "start": "2026-07", "end": "", "rank": "县处级正职", "note": "新任；2026-07-31官方微信称县委书记；1982年生，历岗铁力常务副市长→市委副秘书长"},
    {"person_id": 2, "org_id": 1, "title": "丰林县委副书记", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "丰林县长", "start": "", "end": "", "rank": "县处级正职", "note": "主持县政府全面；主管县审计局"},
    {"person_id": 3, "org_id": 1, "title": "丰林县委副书记（专职）", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 3, "org_id": 8, "title": "红星镇党委书记", "start": "", "end": "", "rank": "乡科级正职", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "丰林县委常委", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "丰林县常务副县长", "start": "", "end": "", "rank": "县处级副职", "note": "分管政府常务，协助审计"},
    {"person_id": 5, "org_id": 1, "title": "丰林县委常委", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 4, "title": "丰林县政协主席", "start": "2026-07", "end": "", "rank": "县处级正职", "note": "2026-07-31称'主席候选人'，接替徐长伟"},
    {"person_id": 6, "org_id": 1, "title": "丰林县委常委（职务待细分）", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "丰林县委常委（职务待细分）", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "丰林县委常委（职务待细分）", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "丰林县委常委（职务待细分）", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "丰林县委常委（职务待细分）", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "丰林县委常委（职务待细分）", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 12, "org_id": 1, "title": "丰林县委常委（职务待细分）", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "丰林县副县长（教育文旅）", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "丰林县副县长（公安司法）", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "丰林县副县长（民政农林交通）", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "丰林县副县长（自然资源城建）", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "丰林县副县长（人社卫健医保）", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 18, "org_id": 3, "title": "丰林县人大常委会主任", "start": "", "end": "", "rank": "县处级正职", "note": ""},
    {"person_id": 19, "org_id": 3, "title": "丰林县人大常委会副主任", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 20, "org_id": 3, "title": "丰林县人大常委会副主任", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"person_id": 21, "org_id": 4, "title": "丰林县政协主席（前任）", "start": "", "end": "2026-07", "rank": "县处级正职", "note": "2026-07-10仍列；后由秦瑞红接替"},
    {"person_id": 22, "org_id": 6, "title": "丰林县人民法院院长", "start": "", "end": "", "rank": "县处级正职", "note": ""},
    {"person_id": 23, "org_id": 7, "title": "丰林县人民检察院检察长", "start": "", "end": "", "rank": "县处级正职", "note": ""},
    {"person_id": 24, "org_id": 9, "title": "伊春市副市长", "start": "2025-12", "end": "", "rank": "地厅级副职", "note": "曾任丰林县委书记"},
    {"person_id": 24, "org_id": 1, "title": "丰林县委书记（前任）", "start": "2020-07", "end": "2026-07", "rank": "县处级正职", "note": ""},
    {"person_id": 25, "org_id": 9, "title": "伊春市委书记", "start": "2024-09", "end": "", "rank": "地厅级正职", "note": ""},
    {"person_id": 25, "org_id": 9, "title": "伊春市人大常委会主任", "start": "2025-01", "end": "", "rank": "地厅级正职", "note": ""},
    {"person_id": 26, "org_id": 10, "title": "伊春市市长", "start": "2024-09", "end": "", "rank": "地厅级正职", "note": ""},
    {"person_id": 26, "org_id": 9, "title": "伊春市委副书记", "start": "2024-09", "end": "", "rank": "地厅级副职", "note": ""},
]

# ── Relationships ──────────────────────────────────────────────────────────

relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政同僚", "context": "县委书记栾皓与县长原浩东党政搭档", "overlap_org": "丰林县", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 24, "type": "继任者", "context": "栾皓接替姜治富任丰林县委书记", "overlap_org": "中共丰林县委员会", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "县委书记领导专职副书记张强", "overlap_org": "中共丰林县委员会", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "县委书记领导县委常委会成员伊琳娜", "overlap_org": "中共丰林县委员会", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "县委书记与县政协主席秦瑞红协作", "overlap_org": "丰林县", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "县长领导常务副县长伊琳娜", "overlap_org": "丰林县人民政府", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 14, "type": "上下级", "context": "县长领导分管公安司法副县长李国平", "overlap_org": "丰林县人民政府", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 13, "type": "上下级", "context": "县长领导副县长梁爽", "overlap_org": "丰林县人民政府", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 18, "type": "同僚", "context": "县人大主任陈春东监督县政府工作", "overlap_org": "丰林县", "overlap_period": "2026-"},
    {"person_a": 5, "person_b": 21, "type": "继任者", "context": "秦瑞红继任徐长伟任县政协主席", "overlap_org": "政协丰林县委员会", "overlap_period": "2026-07"},
    {"person_a": 1, "person_b": 25, "type": "上下级", "context": "伊春市委书记董文琴领导丰林县委书记", "overlap_org": "伊春市", "overlap_period": "2024-"},
    {"person_a": 2, "person_b": 26, "type": "上下级", "context": "伊春市市长苑芳江领导丰林县长", "overlap_org": "伊春市人民政府", "overlap_period": "2024-"},
    {"person_a": 24, "person_b": 25, "type": "上下级", "context": "姜治富(副市长)在伊春市委领导下工作", "overlap_org": "伊春市人民政府", "overlap_period": "2025-"},
    {"person_a": 25, "person_b": 26, "type": "党政同僚", "context": "伊春市委书记与市长党政搭档", "overlap_org": "中共伊春市委员会", "overlap_period": "2024-"},
    {"person_a": 1, "person_b": 22, "type": "同僚", "context": "县法院院长张紫微与县委书记栾皓同县工作", "overlap_org": "丰林县", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 23, "type": "同僚", "context": "县检察院检察长与县长同县工作", "overlap_org": "丰林县", "overlap_period": "2026-"},
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
    if "县长" in post and "副" not in post:
        return ("50,100,255", 20.0)
    if "县委副书记" in post or "常务副县长" in post:
        return ("100,150,255", 12.0)
    if "副县长" in post:
        return ("100,150,255", 12.0)
    if "常委" in post:
        return ("120,120,120", 12.0)
    if "政协" in post or "人大常委会" in post:
        return ("120,180,120", 12.0)
    if "院长" in post or "检察长" in post:
        return ("200,120,120", 12.0)
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
    L.append(f'    <description>丰林县领导班子工作关系网络 - {AS_OF}</description>')
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
    print(f"  GEXF: {GEXF_PATH}")


if __name__ == "__main__":
    print(f"Building {SLUG} network ({AS_OF})")
    build_db()
    build_gexf()
    print("Done.")