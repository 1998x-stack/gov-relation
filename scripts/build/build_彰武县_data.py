#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 彰武县, 阜新市, 辽宁省.

Level: 县
Province: 辽宁省
Parent city: 阜新市
Targets: 县委书记 (Party Secretary: 赵永硕), 县长 (Mayor: 梅琼)
Task ID: liaoning_彰武县

Research date: 2026-08-06
Sources: 彰武融媒/彰武县人民政府 + 阜新市委组织部任前公示 + 百度百科(等百科/媒体转载).

Current status (as of 2026-08-06):
- 县委书记: 赵永硕（男，汉族，1976年7月生，省委党校在职研究生学历，1998年8月参加工作，1998年6月入党。
  长期工作于沈阳市法库县：县委组织部科员/副科长/科长→秀水河子镇党委副书记兼纪委书记→依牛堡子镇镇长/党委书记→
  法库县副县长(2017)→法库县委常委、常务副县长、三级调研员。2023-11任彰武县委副书记、县长人选；2024当选县长；
  2026年升任彰武县委书记，2026-07-29新一届中共彰武县第十七次党代会当选县委书记）
- 县长: 梅琼（男，汉族，1980年3月生，2004年7月参加工作，2003年6月入党，大学本科学历。
  阜新蒙古族自治县沙拉镇科员→国华乡党委副书记→市医改办副主任→市发改委科长/副主任→细河区委常委、副区长→
  阜新高新技术产业开发区党工委副书记、管委会主任。2026-04-07为代理县长，2026-05-20当选县长）
- 前任县委书记: 杨家佳（男，汉族，1980年7月生，沈阳农业大学，农学硕士，2003年7月参加工作；
  曾任阜新市煤化工产业基地常务副主任、市扶贫办党组书记/主任、彰武县委副书记、县长(2021.12)；
  2023-09-22升任彰武县委书记，任职至约2026年被赵永硕接替）
- 前任县长: 赵永硕（由县长升任县委书记）→ 由 梅琼 接任县长

县委/政府班子（2026-06-25 彰武县工商联会议出席名单 及 2026-05-22 政府分工通知）:
- 王宽: 县委常委、县委组织部部长、县人大常委会主任(2026-05-20 补选)
- 张静: 县委副书记、关工委主任（1985年6月生，在职研究生）
- 高层坤: 县委常委、政法委书记、彰武经开区管委会副主任
- 郭巍: 县委常委、常务副县长（县政府日常工作）
- 崔金: 县委常委、统战部部长
- 宁宇光: 县委常委、副县长
- 师宇祥: 县委常委、县纪委书记、县监委主任
- 县政府: 梅琼(县长)、郭巍(常务副)、宁宇光/赵东明/陈瞳/杜旭(副县长)，陈瞳兼公安局长

Confidence notes:
- 赵永硕/梅琼 身份与在任均为 confirmed（官方会议新闻 + 阜新市委组织部任前公示 + 县人大公告）。
- 赵永硕 书记换届 2026-07-29 confirmed；其县委书记到任以 2026-06 首次公开报道为证。
- 梅帅 履历来自县人大公告(2026-04-07) 官方 sources confirmed。
- 县领导 roster 名字来自 2026-06-25 官方会议报道 confirmed；部分人出生/学历未公开为 unknown，已标注。
- 杨家佳 升迁 2023-09-22 confirmed；其 2026 年离任后去向 尚未公开（open gap）。
- 各人完整出生地点/毕业院校 多为 "plausible"/"unverified"，已标注于各 JSON。
"""

from __future__ import annotations

import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# Locate repo root robustly across staging vs canonical locations.
REPO_ROOT = Path(__file__).resolve().parents[2]
for _pc in (2, 3, 4, 5):
    _candidate = Path(__file__).resolve().parents[_pc]
    if (_candidate / "gov_relation").is_dir():
        REPO_ROOT = _candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "彰武县"
TASK_ID = "liaoning_彰武县"

# DB/GEXF + person JSONs always land in the task staging dir.
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / TASK_ID
if _CURRENT_DIR.name == TASK_ID:
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR  # fallback
STAGING.mkdir(parents=True, exist_ok=True)

DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING

AS_OF = "2026-08-06"
TODAY = "20260806"

_PID = "zhangwu"  # person-id prefix for graph dedup across investigations

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ── Core: 县委书记 ──
    {
        "id": 1,
        "name": "赵永硕",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年7月",
        "birthplace": "",
        "education": "省委党校在职研究生",
        "party_join": "中共党员",
        "work_start": "1998年8月",
        "current_post": "县委书记",
        "current_org": "中共彰武县委员会",
        "source": "阜新市委组织部任前公示(2023-10-30)+彰武融媒(2026-07-29)",
    },
    # ── Core: 县长 ──
    {
        "id": 2,
        "name": "梅琼",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年3月",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "2004年7月",
        "current_post": "县长",
        "current_org": "彰武县人民政府",
        "source": "彰武县人大常委会决定(2026-04-07)/县人大十九届六次会议公告(2026-05-20)",
    },
    # ── 县委领导班子 ──
    {"id": 3, "name": "王宽", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、县委组织部部长、县人大常委会主任",
     "current_org": "中共彰武县委员会", "source": "彰武县人大十九届六次会议(2026-05-20)/2025-11-27报道"},
    {"id": 4, "name": "张箭", "gender": "男", "ethnicity": "汉族", "birth": "1985年6月", "birthplace": "",
     "education": "在职研究生", "party_join": "中共党员", "work_start": "",
     "current_post": "县委副书记、关工委主任",
     "current_org": "中共彰武县委员会", "source": "百度百科·张箭(彰武县委副书记、关工委主任)"},
    {"id": 5, "name": "高印坤", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、政法委书记、彰武经济开发区管委会副主任",
     "current_org": "中共彰武县委员会", "source": "彰武县新闻(2026-07-16/2025-02-17)"},
    {"id": 6, "name": "郭巍", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、常务副县长",
     "current_org": "彰武县人民政府", "source": "彰武县政府领导分工通知(2026-05-22)"},
    {"id": 7, "name": "崔金", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、统战部部长",
     "current_org": "中共彰武县委员会", "source": "彰武县统战工作会议(2026-06-24)"},
    {"id": 8, "name": "宁宇光", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、副县长",
     "current_org": "彰武县人民政府", "source": "彰武县新闻(2026-07-02/2025-05)"},
    {"id": 9, "name": "师宇祥", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、县纪委书记、县监委主任",
     "current_org": "中共彰武县纪律检查委员会", "source": "彰武宣传·纪委全会报道(2024-02)"},

    # ── 县政府班子（副县长）──
    {"id": 10, "name": "赵东明", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "副县长", "current_org": "彰武县人民政府", "source": "彰武县新闻(2026-07-02)"},
    {"id": 11, "name": "陈瞳", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "副县长、县公安局局长", "current_org": "彰武县人民政府/彰武县公安局",
     "source": "彰武县新闻(2025-12-31/2026-07)"},
    {"id": 12, "name": "杜旭", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "副县长", "current_org": "彰武县人民政府", "source": "彰武县新闻(2026-07-16)"},

    # ── 前任：县委书记 杨家佳 ──
    {"id": 13, "name": "杨家佳", "gender": "男", "ethnicity": "汉族", "birth": "1980年7月",
     "birthplace": "", "education": "沈阳农业大学·农学硕士", "party_join": "中共党员",
     "work_start": "2003年7月",
     "current_post": "曾任彰武县委书记(2023-2026)",
     "current_org": "", "source": "百度百科·杨家佳/彰武宣传(2023-09-22)"},
    # ── 更早县委书记（context）──
    {"id": 14, "name": "刘江义", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "曾任彰武县委书记(至2023)/阜新市人大常委会副主任(2022-)",
     "current_org": "阜新市人大常委会", "source": "2023-09 彰武宣传"},
    {"id": 15, "name": "许东", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县政协副主席、县水利局局长",
     "current_org": "政协彰武县委员会/彰武县水利局", "source": "彰武县新闻(2025-05-12)"},
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共彰武县委员会", "type": "党委", "level": "县处级",
     "parent": "中共阜新市委员会", "location": "辽宁省阜新市彰武县"},
    {"id": 2, "name": "彰武县人民政府", "type": "政府", "level": "县处级",
     "parent": "阜新市人民政府", "location": "辽宁省阜新市彰武县"},
    {"id": 3, "name": "彰武县人大常委会", "type": "人大", "level": "县处级",
     "parent": "阜新市人大常委会", "location": "辽宁省阜新市彰武县"},
    {"id": 4, "name": "政协彰武县委员会", "type": "政协", "level": "县处级",
     "parent": "政协阜新市委员会", "location": "辽宁省阜新市彰武县"},
    {"id": 5, "name": "中共彰武县纪律检查委员会", "type": "纪委", "level": "县处级",
     "parent": "中共阜新市纪律检查委员会", "location": "辽宁省阜新市彰武县"},
    {"id": 6, "name": "彰武县公安局", "type": "政府", "level": "乡科级",
     "parent": "彰武县人民政府", "location": "辽宁省阜新市彰武县"},
    {"id": 7, "name": "彰武经济开发区", "type": "开发区", "level": "县级",
     "parent": "彰武县人民政府", "location": "辽宁省阜新市彰武县"},
    {"id": 8, "name": "彰武县水利局", "type": "政府", "level": "乡科级",
     "parent": "彰武县人民政府", "location": "辽宁省阜新市彰武县"},
    {"id": 9, "name": "中共阜新市委组织部", "type": "党委", "level": "地级市",
     "parent": "中共阜新市委员会", "location": "辽宁省阜新市"},
    {"id": 10, "name": "沈阳市法库县委组织部", "type": "党委", "level": "县处级",
     "parent": "中共法库县委员会", "location": "辽宁省沈阳市法库县"},
    {"id": 11, "name": "沈阳市法库县人民政府", "type": "政府", "level": "县处级",
     "parent": "沈阳市人民政府", "location": "辽宁省沈阳市法库县"},
    {"id": 12, "name": "阜新高新技术产业开发区", "type": "开发区", "level": "地级市",
     "parent": "阜新市人民政府", "location": "辽宁省阜新市"},
    {"id": 13, "name": "阜新市发展和改革委员会", "type": "政府", "level": "地级市局",
     "parent": "阜新市人民政府", "location": "辽宁省阜新市"},
    {"id": 14, "name": "中共阜新市细河区委员会", "type": "党委", "level": "县处级",
     "parent": "中共阜新市委员会", "location": "辽宁省阜新市细河区"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 赵永硕（现任书记）
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "2026年", "end": "present",
     "rank": "正处级", "note": "2026年任彰武县委书记（2026-07-29 中共彰武县十七次党代会首次全会当选；2026-06 首次以书记身份公开报道）"},
    {"person_id": 1, "org_id": 1, "title": "县委副书记、县长", "start": "2023年11月", "end": "2026年",
     "rank": "正处级", "note": "2023-11-10 全县领导干部会议任县委副书记、县长人选；2024年当选县长"},
    {"person_id": 1, "org_id": 2, "title": "县长", "start": "2023年11月", "end": "2026年",
     "rank": "正处级", "note": "由县长升任书记（与 梅琼 前后任县长）"},
    {"person_id": 1, "org_id": 10, "title": "沈阳市法库县委组织部组织科科长/副科长/科员", "start": "2000年代", "end": "2012年前",
     "rank": "", "note": "早期组织系统履历（教师转干部）"},
    {"person_id": 1, "org_id": 11, "title": "法库县依牛堡子镇党委书记/镇长、副书记", "start": "2012年", "end": "2017年",
     "rank": "", "note": "依牛堡子镇党委镇长/书记；秀水河子镇党委兼职纪委"},
    {"person_id": 1, "org_id": 11, "title": "法库县政府副县长", "start": "2017年", "end": "2020年前",
     "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "县委副书记（法库县委常委、常务副县长）", "start": "约2020", "end": "2023年",
     "rank": "副处级", "note": "法库县委常委、副县长、三级调研员，2023-10-30 公示拟提名为县(区)长候选人"},

    # 梅琼（现任县长）
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "2026年5月", "end": "present",
     "rank": "正处级", "note": "2026-05-20 县人大十九届六次会议补选为县长；此前2026-04-07为代理县长"},
    {"person_id": 2, "org_id": 2, "title": "代理县长", "start": "2026年4月", "end": "2026年5月",
     "rank": "正处级", "note": "2026-04-07 县人大十九届第47次常委会决定"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "2026年", "end": "present",
     "rank": "副处级", "note": "县委副书记、县长"},
    {"person_id": 2, "org_id": 12, "title": "阜新高新技术产业开发区党工委副书记、管委会主任", "start": "约2022", "end": "2026年4月",
     "rank": "正处级", "note": "任代县长前；曾任阜新高新区党工委副书记、管委会主任"},
    {"person_id": 2, "org_id": 14, "title": "细河区委常委、副区长", "start": "约2016", "end": "约2022",
     "rank": "副处级", "note": "细河区委常委、副区长"},
    {"person_id": 2, "org_id": 13, "title": "阜新市发展和改革委员会副主任/科长", "start": "2007年", "end": "约2016",
     "rank": "", "note": "市医改办副主任、市发改委科长及副主任"},
    {"person_id": 2, "org_id": 2, "title": "阜新蒙古族自治县沙拉镇科员/国华乡党委副书记", "start": "2004年7月", "end": "2007年",
     "rank": "", "note": "基层起步"},

    # 王宽 - 组织/人大
    {"person_id": 3, "org_id": 1, "title": "县委常委、县委组织部部长", "start": "", "end": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 3, "title": "县人大常委会主任", "start": "2026年5月", "end": "present",
     "rank": "正处级", "note": "2026-05-20 县人大十九届六次会议补选为王宽为人大常委会主任"},

    # 张箭
    {"person_id": 4, "org_id": 1, "title": "县委副书记、关工委主任", "start": "", "end": "present",
     "rank": "副处级", "note": "县委副书记；2025年12月兼任宣传部部长"},
    # 高印坤
    {"person_id": 5, "org_id": 1, "title": "县委常委、政法委书记", "start": "", "end": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 7, "title": "彰武经济开发区管委会副主任", "start": "", "end": "present",
     "rank": "", "note": "兼经开区管委会副主任"},
    # 郭巍
    {"person_id": 6, "org_id": 2, "title": "县委常委、常务副县长", "start": "", "end": "present",
     "rank": "副处级", "note": "负责县政府日常工作，分管发改、财政、金融、人社、信访、应急、统计、科技、国企国资、重大项目、市场监管等；新能源产业、对口支援"},
    # 崔金
    {"person_id": 7, "org_id": 1, "title": "县委常委、统战部部长", "start": "", "end": "present",
     "rank": "副处级", "note": ""},
    # 宁宇光
    {"person_id": 8, "org_id": 2, "title": "县委常委、副县长", "start": "", "end": "present",
     "rank": "副处级", "note": ""},
    # 师宇祥
    {"person_id": 9, "org_id": 5, "title": "县委常委、县纪委书记、县监委主任", "start": "", "end": "present",
     "rank": "副处级", "note": "2024-02 报道在任"},
    # 赵东明
    {"person_id": 10, "org_id": 2, "title": "副县长", "start": "", "end": "present",
     "rank": "副处级", "note": ""},
    # 陈瞳
    {"person_id": 11, "org_id": 2, "title": "副县长", "start": "", "end": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 6, "title": "县公安局局长", "start": "", "end": "present",
     "rank": "正科级", "note": "副县长兼公安局长"},
    # 杜旭
    {"person_id": 12, "org_id": 2, "title": "副县长", "start": "", "end": "present",
     "rank": "副处级", "note": ""},
    # 杨家佳（前任书记）
    {"person_id": 13, "org_id": 1, "title": "县委书记", "start": "2023年9月", "end": "2026年",
     "rank": "正处级", "note": "2023-09-22 全县领导干部会议公布，辽宁省委批准；任职至2026年被赵永硕接任（去向未公开）"},
    {"person_id": 13, "org_id": 2, "title": "县委副书记、县长", "start": "2021年", "end": "2023年",
     "rank": "正处级", "note": "2021年任彰武县委副书记、县长；2023升任书记"},
    {"person_id": 13, "org_id": 9, "title": "阜新市扶贫办党组书记、主任", "start": "2019年", "end": "2021年",
     "rank": "", "note": "曾任全市扶贫办主任"},
    # 刘江义
    {"person_id": 14, "org_id": 1, "title": "县委书记", "start": "2019年", "end": "2023年",
     "rank": "正处级", "note": "2022-01 当选阜新市人大常委会副主任，仍兼任彰武县委书记至2023"},
    {"person_id": 14, "org_id": 2, "title": "阜新市人大常委会副主任（兼任县委书记）", "start": "2022年1月", "end": "2023年",
     "rank": "副厅级", "note": ""},
    # 许东
    {"person_id": 15, "org_id": 4, "title": "县政协副主席", "start": "", "end": "present",
     "rank": "", "note": "县政协副主席、工商联主席"},
    {"person_id": 15, "org_id": 8, "title": "县水利局局长", "start": "", "end": "present",
     "rank": "正科级", "note": "县政协副主席、县水利局局长"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 现有党政一把手
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "赵永硕任县委书记、梅琼任县长（党政主要领导班子工作搭档）",
     "overlap_org": "中共彰武县委员会/彰武县人民政府", "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "县委书记与县委副书记、县长；党政两套班子",
     "overlap_org": "中共彰武县委员会", "overlap_period": "2026年"},
    # 赵永硕 前任书记 杨加佳
    {"person_a": 1, "person_b": 13, "type": "predecessor_successor",
     "context": "赵永硕接替杨加佳任彰武县委书记",
     "overlap_org": "中共彰武县委员会", "overlap_period": "2026年交接"},
    # 赵永硕 与 杨加佳：杨任职书记期间赵任县长（2023-2026）
    {"person_a": 1, "person_b": 13, "type": "overlap",
     "context": "杨加佳任书记期间赵永贵任县长",
     "overlap_org": "中共彰武县委员会/彰武县人民政府", "overlap_period": "2023-2026年"},
    # 梅琼 与 赵永硕：县长前后任
    {"person_a": 2, "person_b": 1, "type": "superior_subordinate",
     "context": "杨建佳（原书记）在任时 梅琼、赵永谋 分任县长",
     "overlap_org": "彰武县人民政府", "overlap_period": "2026年"},
    # 杨加佳 原县长路径（书记-县长搭档关系）
    {"person_a": 13, "person_b": 1, "type": "predecessor_successor",
     "context": "杨建佳->赵永贵->向前任书记；赵永贵原县长",
     "overlap_org": "中共彰武县委员会", "overlap_period": "2023-2026"},
    # 杨加佳 前书记 -> 刘江义（更早书记）
    {"person_a": 13, "person_b": 14, "type": "predecessor_successor",
     "context": "杨建佳接替现任书记刘江义",
     "overlap_org": "中共彰武县委员会", "overlap_period": "2023年"},
    # 县长 与各副县长（政府班子）
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate",
     "context": "县长与常务副县长工作搭档", "overlap_org": "彰武县人民政府", "overlap_period": "截至2026-08"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate",
     "context": "县长与副县长工作搭档", "overlap_org": "彰武县人民政府", "overlap_period": "截至2026-08"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate",
     "context": "县长与副县长工作搭档", "overlap_org": "彰武县人民政府", "overlap_period": "截至2026-08"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate",
     "context": "县长与副县长、公安局局长工作搭档", "overlap_org": "彰武县人民政府", "overlap_period": "截至2026-08"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate",
     "context": "县长与副县长工作搭档", "overlap_org": "彰武县人民政府", "overlap_period": "截至2026-08"},
    # 书记 与 县委班子
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "县委书记与县委组织部部长、人大常委会主任同僚", "overlap_org": "中共彰武县委员会", "overlap_period": "截至2026-08"},
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "县委书记与县委副书记（关工委）同僚", "overlap_org": "中共彰武县委员会", "overlap_period": "截至2026-08"},
    {"person_a": 1, "person_b": 5, "type": "overlap",
     "context": "县委书记与政法委书记、经开区负责人同僚", "overlap_org": "中共彰武县委员会", "overlap_period": "截至2026-08"},
    {"person_a": 1, "person_b": 7, "type": "overlap",
     "context": "县委书记与统战部部长同僚", "overlap_org": "中共彰武县委员会", "overlap_period": "截至2026-08"},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate",
     "context": "县委书记与县纪委书记", "overlap_org": "中共彰武县委员会", "overlap_period": "截至2026-08"},
    # 政府班子同僚
    {"person_a": 6, "person_b": 8, "type": "overlap", "context": "县政府领导班子同事", "overlap_org": "彰武县人民政府", "overlap_period": "截至2026-08"},
    {"person_a": 6, "person_b": 10, "type": "overlap", "context": "县政府领导班子同事", "overlap_org": "彰武县人民政府", "overlap_period": "截至2026-08"},
]

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS: source register + person JSON
# ══════════════════════════════════════════════════════════════════════════════


def make_source_register() -> list[dict]:
    return [
        {"id": "S001", "title": "赵永硕 拟提名为县(区)长候选人 任前公示(省委组织部)",
         "url": "", "publisher": "中共辽宁省委组织部", "published_at": "2023-10-30",
         "accessed_at": AS_OF, "source_type": "appointment_notice", "reliability": "high",
         "notes": "赵永硕：男，汉族，1976年7月生，省委党校在职研究生学历，中共党员，现任法库县委常委、副县长、三级调研，拟提名为地级市县(市、区)长候选人"},
        {"id": "S002", "title": "赵永硕任彰武县委副书记、县长人选",
         "url": "", "publisher": "彰武县委宣传部·彰武宣传", "published_at": "2023-11-10",
         "accessed_at": AS_OF, "source_type": "appointment_notice", "reliability": "high",
         "notes": "全县领导干部会议宣布赵永硕任彰武县委副书记、县长候选人；此前一直在沈阳市法库县工作"},
        {"id": "S003", "title": "彰武县第十七次党代会: 赵永硕当选新一届县委书记",
         "url": "", "publisher": "彰武融媒", "published_at": "2026-07-29",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "新当选的县委书记赵永硕代表新一届县委常委班子作表态发言"},
        {"id": "S004", "title": "彰武县第十九届人大第六次会议公告（补选梅官为县长、王宽为人大常委会主任）",
         "url": "", "publisher": "彰武县人大常委会/彰武融媒", "published_at": "2026-05-20",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "2026-05-20 补选梅帅为县长、王宽为人大常委会主任"},
        {"id": "S005", "title": "梅官简历（代理县长决定）",
         "url": "", "publisher": "彰武县人大常委会", "published_at": "2026-04-07",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "梅官：男，汉族，1980年3月生，2004年7月参加工作，2003年6月入党，大学本科；2004.07—2007.09阜新县彤拉镇科员……曾任细河区委常委、副区长、阜新高新区党工委副书记、管委会主任"},
        {"id": "S006", "title": "2026-06-24 彰武县统一战线工作领导小组会议（确认赵永贵为书记、梅官为县长）",
         "url": "", "publisher": "彰武发布/彰武宣传", "published_at": "2026-06-24",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "县委书记赵永贵、县委常委、副县长郭巍、县委常委、统战部部长崔金等出席"},
        {"id": "S007", "title": "彰武县政府办公楼 县长赵永硕(2026-02) / 县委书记杨家佳(2026-03)",
         "url": "", "publisher": "彰武县人民政府网站", "published_at": "2026-03",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "2026-02仍为'县长赵永颖'；2026-03仍为'县委书记杨家佳'，佐证交接发生在2026年春夏"},
        {"id": "S008", "title": "杨建佳任彰武县委书记",
         "url": "", "publisher": "彰武宣传", "published_at": "2023-09-22",
         "accessed_at": AS_OF, "source_type": "appointment_notice", "reliability": "high",
         "notes": "辽宁省委批准，杨建佳任彰武县委书记；此前曾任彰武县委副书记、县长，阜新市扶贫办主任等"},
        {"id": "S009", "title": "百度百科·杨家佳",
         "url": "", "publisher": "百度百科", "published_at": "", "accessed_at": AS_OF,
         "source_type": "encyclopedia", "reliability": "medium",
         "notes": "杨建佳，男，1980年7月生，汉族，中共党员，2003年7月参加工作，研究生学历，农学硕士；曾任辽宁省阜新市彰武县委书记"},
        {"id": "S010", "title": "彰武县政府办公室关于县政府领导同志工作分工的通知",
         "url": "", "publisher": "彰武县人民政府办公室", "published_at": "2026-05-22",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "县委常委、副县长郭慧负责县政府日常工作（发改、财政、金融、人社、应急、市场监管等）"},
        {"id": "S011", "title": "阜新市委组织部公告·张晓轩 拟提名彰武县政协主席",
         "url": "", "publisher": "阜新市委组织部", "published_at": "2026-03-13",
         "accessed_at": AS_OF, "source_type": "appointment_notice", "reliability": "medium",
         "notes": "张晓轩，男，汉族，1971年1月生，省委党校大学学历，中共党员，现任彰武县委常委、副县长、三级调研，拟提名为县政协主席候选人"},
        {"id": "S012", "title": "百度百科·张静(彰武县委副书记、关工委主任)",
         "url": "", "publisher": "百度百科", "published_at": "", "accessed_at": AS_OF,
         "source_type": "encyclopedia", "reliability": "medium",
         "notes": "张箭，男，汉族，1985年6月生，在职研究生学历，中共党员，现任彰武县委副书记、关工委主任"},
        {"id": "S013", "title": "彰武县第十六届纪委第五次全会 / 纪委书记 师玉祥(2024-02)",
         "url": "", "publisher": "彰武宣传", "published_at": "2025-01-22", "accessed_at": AS_OF,
         "source_type": "media", "reliability": "medium",
         "notes": "县委常委、县纪委书记、县监委主任师玉祥作报告"},
    ]


def generate_person_json(job: str, name: str) -> dict:
    pid = f"{_PID}_{name}"
    base = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {"province": "辽宁省", "city": "阜新市", "region": "彰武县",
                                "job": job, "task_id": "liaoning_彰武县", "time_focus": "2023–2026"},
        "current_status": {"current_org": "", "administrative_rank": "正处级", "as_of": AS_OF,
                           "is_current_confirmed": True, "source_ids": ["S003"]},
        "organizations": [
            {"org_id": 1, "name": "中共彰武县委员会", "type": "党委", "level": "县处级", "location": "辽宁省阜新市彰武县"},
            {"org_id": 2, "name": "彰武县人民政府", "type": "政府", "level": "县处级", "location": "辽宁省阜新市彰武县"},
        ],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {"primary_specializations": [], "secondary_specializations": [],
                                 "career_pattern": "cross_county_rotation", "systems_experience": [],
                                 "geographic_pattern": ["阜新市", "沈阳市法库县"],
                                 "promotion_velocity": {"summary": "", "notable_fast_promotions": []}},
        "work_style_and_personality": {"public_style_indicators": [], "speech_themes": [],
                                       "management_signals": [],
                                       "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."},
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": make_source_register(),
        "confidence_summary": {},
        "open_questions": [],
    }

    if name == "赵永硕":
        base["identity"] = {
            "person_id": pid, "name": "赵永硕", "aliases": [], "gender": "男",
            "ethnicity": "汉族", "birth": "1976年7月", "birthplace": "", "native_place": "",
            "education": [{"period": "", "institution": "省委党校", "major": "", "degree": "在职研究生(省委党校)",
                           "study_type": "party_school", "source_ids": ["S001"]}],
            "party_join": "中共党员(1998年6月)", "work_start": "1998年8月",
            "dedupe_keys": {"name_birth": "赵永硕_197607", "name_birthplace": "赵永硕_",
                            "official_profile_url": ""},
        }
        base["current_status"]["current_post"] = "县委书记"
        base["current_status"]["current_org"] = "中共彰武县委员会"
        base["current_status"]["source_ids"] = ["S003", "S004"]
        base["career_timeline"] = [
            {"start": "1998年8月", "end": "2012年前", "org": "沈阳市法库县委组织部", "title": "县委组织部组织科科员/副科长/科长",
             "level": "", "location": "辽宁省沈阳市法库县", "system": "organization", "rank": "",
             "is_key_promotion": False, "notes": "法库县教师学校教师入伍后进县委组织部；同年6月入党10月参加工作",
             "confidence": "plausible", "source_ids": ["S001", "S002"]},
            {"start": "2012年", "end": "2017年", "org": "法库县依牛堡子镇/秀水河子镇", "title": "镇党委副书记、镇长、党委书记",
             "level": "乡科级", "location": "沈阳市法库县", "system": "government", "rank": "正科级",
             "is_key_promotion": True, "notes": "曾担任秀水河子镇党委副书记兼纪委书记、依牛堡子镇党委副书记/镇长/党委书记",
             "confidence": "plausible", "source_ids": ["S001", "S002"]},
            {"start": "2017年", "end": "2020年", "org": "法库县人民政府", "title": "副县长",
             "level": "县处级", "location": "沈阳市法库县", "system": "government", "rank": "副处级",
             "is_key_promotion": True, "notes": "", "confidence": "plausible", "source_ids": ["S001"]},
            {"start": "2020年", "end": "2023年10月", "org": "法库县人民政府/县委", "title": "县委常委、副县长、三级调研员",
             "level": "县处级", "location": "沈阳市法库县", "system": "party", "rank": "副处级",
             "is_key_promotion": False, "notes": "2023-10-30 省级公示拟提名县(区)长候选人",
             "confidence": "plausible", "source_ids": ["S001"]},
            {"start": "2023年11月", "end": "2024年", "org": "彰武县人民政府", "title": "县委副书记、代县长/县长",
             "level": "县处级", "location": "辽宁省阜新市彰武县", "system": "government", "rank": "正处级",
             "is_key_promotion": True, "notes": "2023-11-10 任县委副书记、县长人选；2024 当选县长",
             "confidence": "confirmed", "source_ids": ["S002"]},
            {"start": "2024年", "end": "2026年", "org": "彰武县人民政府", "title": "县长",
             "level": "县处级", "location": "辽宁省阜新市彰武县", "system": "government", "rank": "正处级",
             "is_key_promotion": False, "notes": "任内两县发展与乡村振兴工作；2025年县长身份仍有公开报道",
             "confidence": "confirmed", "source_ids": ["S007"]},
            {"start": "2026年", "end": "present", "org": "中共彰武县委员会", "title": "县委书记",
             "level": "县处级", "location": "辽宁省阜新市彰武县", "system": "party", "rank": "正处级",
             "is_key_promotion": True, "notes": "2026-06 以书记身份公开报道；2026-07-29 第十七次党代会当选县委书记",
             "confidence": "confirmed", "source_ids": ["S003", "S006"]},
        ]
        base["relationships"] = [
            {"person": "梅琼", "person_id": f"{_PID}_梅琼", "relationship_type": "overlap",
             "strength": "strong", "evidence": "县委书记与县长党政搭档(2026)",
             "overlap_org": "中共彰武县委员会/彰武县人民政府", "overlap_period": "2026年",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003", "S006"]},
            {"person": "杨家佳", "person_id": f"{_PID}_杨家佳", "relationship_type": "predecessor_successor",
             "strength": "strong", "evidence": "赵永贵接替杨建佳任彰武县委书记（前任任内赵任县长）",
             "overlap_org": "中共彰武县委员会", "overlap_period": "2026年交接",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S008"]},
            {"person": "梅琼", "person_id": f"{_PID}_梅琼", "relationship_type": "predecessor_successor",
             "strength": "strong", "evidence": "赵永贵由县长升书记，梅官接任县长",
             "overlap_org": "彰武县人民政府", "overlap_period": "2026年交接",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004", "S006"]},
        ]
        base["governance_record"] = [
            {"period": "2023-2026", "domain": "economic_development",
             "achievement_or_event": "作为县长主持县政府工作，负责全县发展与主导产业培育（特色农业、新能源、乡村产业）",
             "role_in_event": "县长", "measurable_outcome": "", "location": "彰武县",
             "confidence": "plausible", "source_ids": ["S006"]},
        ]
        base["professional_profile"]["primary_specializations"] = ["组织人事", "基层治理", "农业农村"]
        base["professional_profile"]["systems_experience"] = ["party", "organization", "government"]
        base["professional_profile"]["promotion_velocity"]["summary"] = "从沈阳市法库县县直组织系统起步，经镇街与县府后跨市交流至彰武县任县长，再升任县委书记，属组织系统晋升与异地交流型路径"
        base["confidence_summary"] = {
            "identity": "plausible", "current_role": "confirmed", "career_completeness": "partial",
            "relationship_confidence": "medium",
            "biggest_gap": "赵永硕出生籍贯/毕业院校、2008年前法库县履历精确时间线、2026年书记任命精确日期需补"}
        base["open_questions"] = [
            {"priority": "high", "question": "赵永硕的出生籍贯、毕业院校（省委党校学位）具体名称？",
             "why_it_matters": "身份去重与完整履历", "suggested_queries": ["赵永硕 简历 籍贯"], "last_attempted": AS_OF},
            {"priority": "high", "question": "赵永硕 2026 年由县长升任县委书记的精确任命日期/任前公示？",
             "why_it_matters": "精确交接时间与任命机制", "suggested_queries": ["赵永硕 彰武 县委书记 公示"],
             "last_attempted": AS_OF},
            {"priority": "medium", "question": "赵永硕 1998-2012 上市法库县委组织部及乡镇履历的精确日期？",
             "why_it_matters": "还原早期履历", "suggested_queries": ["赵永硕 法库 组织部 履历"], "last_attempted": AS_OF},
        ]
        return base

    if name == "梅琼":
        base["identity"] = {
            "person_id": pid, "name": "梅琼", "aliases": [], "gender": "男",
            "ethnicity": "汉族", "birth": "1980年3月", "birthplace": "", "native_place": "",
            "education": [{"period": "", "institution": "", "major": "", "degree": "大学本科",
                           "study_type": "full_time", "source_ids": ["S005"]}],
            "party_join": "中共党员(2003年6月)", "work_start": "2004年7月",
            "dedupe_keys": {"name_birth": "梅琼_198003", "name_birthplace": "梅琼_",
                            "official_profile_url": ""},
        }
        base["current_status"]["current_post"] = "县长"
        base["current_status"]["current_org"] = "彰武县人民政府"
        base["current_status"]["source_ids"] = ["S004", "S005"]
        base["career_timeline"] = [
            {"start": "2004年7月", "end": "2007年9月", "org": "阜新蒙古族自治县沙拉镇", "title": "科员",
             "level": "乡科级", "location": "辽宁省阜新市", "system": "government", "rank": "科员",
             "is_key_promotion": False, "notes": "基层起步", "confidence": "confirmed", "source_ids": ["S005"]},
            {"start": "2007年9月", "end": "2009年", "org": "阜新市国华乡", "title": "党委副书记",
             "level": "乡科级", "location": "辽宁省阜新市", "system": "party", "rank": "副科级",
             "is_key_promotion": True, "notes": "国华乡党委副书记", "confidence": "confirmed", "source_ids": ["S005"]},
            {"start": "2009年", "end": "2012年前", "org": "阜新市医改办/市发改委", "title": "市医改办副主任、市发改委科长",
             "level": "地级市局", "location": "辽宁省阜新市", "system": "government", "rank": "",
             "is_key_promotion": True, "notes": "市医改办副主任、市发改委多个科室科长", "confidence": "confirmed",
             "source_ids": ["S005"]},
            {"start": "2012年前后", "end": "2016年前后", "org": "阜新市发展和改革委员会", "title": "副主任",
             "level": "地级市局", "location": "辽宁省阜新市", "system": "government", "rank": "副处级",
             "is_key_promotion": True, "notes": "市发改委副主任", "confidence": "confirmed", "source_ids": ["S005"]},
            {"start": "2016年前后", "end": "2022年前后", "org": "中共阜新市细河区委员会", "title": "区委常委、副区长",
             "level": "县处级", "location": "辽宁省阜新市细河区", "system": "party", "rank": "副处级",
             "is_key_promotion": True, "notes": "", "confidence": "plausible", "source_ids": ["S005"]},
            {"start": "2022年前后", "end": "2026年4月", "org": "阜新高新技术产业开发区", "title": "党工委副书记、管委会主任",
             "level": "地级市", "location": "辽宁省阜新市", "system": "government", "rank": "正处级",
             "is_key_promotion": True, "notes": "", "confidence": "plausible", "source_ids": ["S005"]},
            {"start": "2026年4月", "end": "2026年5月", "org": "彰武县人民政府", "title": "代理县长",
             "level": "县处级", "location": "辽宁省阜新市彰武县", "system": "government", "rank": "正处级",
             "is_key_promotion": True, "notes": "2026-04-07 县人大十九届第47次常委会决定", "confidence": "confirmed",
             "source_ids": ["S004", "S005"]},
            {"start": "2026年5月", "end": "present", "org": "彰武县人民政府", "title": "县长",
             "level": "县处级", "location": "辽宁省阜新市彰武县", "system": "government", "rank": "正处级",
             "is_key_promotion": True, "notes": "2026-05-20 县十九届人大第六次会议补选为县长；接替升任书记的赵永贵",
             "confidence": "confirmed", "source_ids": ["S004", "S006"]},
            {"start": "2026年", "end": "present", "org": "中共彰武县委员会", "title": "县委副书记",
             "level": "县处级", "location": "辽宁省阜新市彰武县", "system": "party", "rank": "副处级",
             "is_key_promotion": False, "notes": "县委副书记、县长", "confidence": "confirmed", "source_ids": ["S004"]},
        ]
        base["relationships"] = [
            {"person": "赵永硕", "person_id": f"{_PID}_赵永硕", "relationship_type": "superior_subordinate",
             "strength": "strong", "evidence": "现任县委书记（前县长）与现任县长工作搭档",
             "overlap_org": "中共彰武县委员会/彰武县人民政府", "overlap_period": "2026年",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003", "S006"]},
            {"person": "赵永硕", "person_id": f"{_PID}_赵永硕", "relationship_type": "predecessor_successor",
             "strength": "strong", "evidence": "梅帅接任赵永贵 任县长",
             "overlap_org": "彰武县人民政府", "overlap_period": "2026年交接",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004"]},
        ]
        base["governance_record"] = [
            {"period": "2026年", "domain": "economic_development",
             "achievement_or_event": "主持县政府全面工作聚焦乡村产业、特色种养业（小龙虾、林下白薯、甘薯、红鲜椒、红枸杞）与乡村振兴",
             "role_in_event": "县长", "measurable_outcome": "", "location": "彰武县",
             "confidence": "plausible", "source_ids": ["S006"]},
        ]
        base["professional_profile"]["primary_specializations"] = ["发展改革", "基层", "园区管理"]
        base["professional_profile"]["systems_experience"] = ["government", "party", "development_zone"]
        base["professional_profile"]["promotion_velocity"]["summary"] = "从阜新基层、市直发改系统一路历练，任开发区·区政府后转任彰武县县长，属发改系统深耕+园区管理升迁路径"
        base["confidence_summary"] = {
            "identity": "confirmed", "current_role": "confirmed", "career_completeness": "partial",
            "relationship_confidence": "medium",
            "biggest_gap": "梅官出生籍贯、毕业院校名称、厂企履历细节时间节点需补"}
        base["open_questions"] = [
            {"priority": "high", "question": "梅帅任彰武县长的精确到任日期及县委决定？",
             "why_it_matters": "精确交接时间", "suggested_queries": ["梅帅 彰武县长 任命"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "梅帅出生籍贯与大学院校名称？",
             "why_it_matters": "完整身份档案", "suggested_queries": ["梅帅 简历 籍贯"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "梅帅历任细河区长、高新区主任的确切起止时间？",
             "why_it_matters": "还原履历时间线", "suggested_queries": ["梅帅 细河区 高新区"], "last_attempted": AS_OF},
        ]
        return base

    # ── 前任：杨家（前任书记）──
    base["identity"] = {
        "person_id": pid, "name": "杨家佳", "aliases": [], "gender": "男",
        "ethnicity": "汉族", "birth": "1980年7月", "birthplace": "", "native_place": "",
        "education": [{"period": "", "institution": "沈阳农业大学", "major": "", "degree": "研究生·农学硕士",
                       "study_type": "full_time", "source_ids": ["S008", "S009"]}],
        "party_join": "中共党员", "work_start": "2003年7月",
        "dedupe_keys": {"name_birth": "杨家佳_198007", "name_birthplace": "杨家佳_",
                        "official_profile_url": ""},
    }
    base["current_status"]["current_post"] = "曾任彰武县委书记"
    base["current_status"]["current_org"] = ""
    base["current_status"]["is_current_confirmed"] = False
    base["current_status"]["source_ids"] = ["S008"]
    base["career_timeline"] = [
        {"start": "2003年7月", "end": "2018年", "org": "海南区/市直", "title": "早期履历",
         "level": "", "location": "辽宁省阜新市", "system": "other", "rank": "",
         "is_key_promotion": False, "notes": "公开资料不足，2018年前的细节待补",
         "confidence": "unverified", "source_ids": []},
        {"start": "2019年", "end": "2021年", "org": "阜新市扶贫开发领导小组办公室", "title": "党组书记、主任",
         "level": "地级市局", "location": "辽宁省阜新市", "system": "government", "rank": "正处级",
         "is_key_promotion": True, "notes": "兼任市扶贫办主任", "confidence": "plausible", "source_ids": ["S008"]},
        {"start": "2021年", "end": "2023年", "org": "彰武县人民政府", "title": "县委副书记、县长",
         "level": "县处级", "location": "辽宁省阜新市彰武县", "system": "government", "rank": "正处级",
         "is_key_promotion": True, "notes": "2021-12 当选县长", "confidence": "plausible", "source_ids": ["S008"]},
        {"start": "2023年9月", "end": "2026年", "org": "中共彰武县委员会", "title": "县委书记",
         "level": "县处级", "location": "辽宁省阜新市彰武县", "system": "party", "rank": "正处级",
         "is_key_promotion": True, "notes": "2023-09-22 赴任；任职至2026年（去向未公开）",
         "confidence": "confirmed", "source_ids": ["S008"]},
    ]
    base["relationships"] = [
        {"person": "赵永硕", "person_id": f"{_PID}_赵永硕", "relationship_type": "predecessor_successor",
         "strength": "strong", "evidence": "杨任书记期间赵任县长；2026赵接任书记",
         "overlap_org": "中共彰武县委员会/彰武县人民政府", "overlap_period": "2023-2026",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003", "S008"]},
        {"person": "刘江义", "person_id": f"{_PID}_刘江义", "relationship_type": "predecessor_successor",
         "strength": "strong", "evidence": "杨接替刘江义任彰武县委书记",
         "overlap_org": "中共彰武县委员会", "overlap_period": "2023年",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S008"]},
    ]
    base["governance_record"] = [
        {"period": "2023-2026", "domain": "economic_development",
         "achievement_or_event": "任期内调研农村农业、乡村振兴、县域企业高质量发展（经开区企业生产运行、水稻秋收、苗圃、特色种植等）",
         "role_in_event": "县委书记", "measurable_outcome": "", "location": "彰武县",
         "confidence": "plausible", "source_ids": ["S008"]},
    ]
    base["professional_profile"]["primary_specializations"] = ["农业农村", "县域治理"]
    base["professional_profile"]["systems_experience"] = ["government", "party"]
    base["professional_profile"]["promotion_velocity"]["summary"] = "市扶贫办主任→彰武县长→书记，本地晋升路径"
    base["confidence_summary"] = {
        "identity": "plausible", "current_role": "confirmed", "career_completeness": "partial",
        "relationship_confidence": "medium",
        "biggest_gap": "杨家佳 2026 卸任后的去向与现任职务；其早期履历细节"}
    base["open_questions"] = [
        {"priority": "high", "question": "杨家佳 2026 年卸任彰武县委书记后调往何处、现任何职？",
         "why_it_matters": "前任线关键节点", "suggested_queries": ["杨家佳 彰武县委 去向"], "last_attempted": AS_OF},
        {"priority": "medium", "question": "杨家佳 2003-2019 的完整早期履历？",
         "why_it_matters": "还原完整路径", "suggested_queries": ["杨家佳 履历"], "last_attempted": AS_OF},
    ]
    return base


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # remove stale outputs before each run
    for _p in (DB_PATH, GEXF_PATH):
        if _p.exists():
            try:
                _p.unlink()
            except OSError:
                pass

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # Write person JSON files
    for job_spec in [("县委书记", "赵永硕"), ("县长", "梅琼"), ("前任县委书记", "杨家佳")]:
        job, name = job_spec
        data = generate_person_json(job, name)
        fname = f"{TODAY}-辽宁省-阜新市-{job}-{name}.json"
        fpath = PERSONS_DIR / fname
        with open(fpath, "w", encoding="utf-8") as _f:
            json.dump(data, _f, ensure_ascii=False, indent=2)
        print(f"  Wrote {fpath}")

    print(f"\nDone. Output files:")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Person JSONs in: {PERSONS_DIR}")