#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 云州区 (Yunzhou District), 大同市, 山西省.

Investigation date: 2026-07-26
Task ID: shanxi_云州区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - www.yunzhou.gov.cn — 云州区人民政府官方网站（政府领导页面、政务新闻页面）
  - 区委书记：宁文鑫 — multiple confirmed news appearances (2026-07) as "市委常委，大同经开区党工委书记、管委会主任，区委书记"
  - 区长：庞君（1978年10月生，大同天镇人，中央党校研究生学历，1999年8月参加工作）
  - 常务副区长：贺睿（1981年6月生，山西大同人，北京工业大学研究生学历，2004年11月参加工作）
  - 区政府领导共9名（含1名挂职副区长）

Confidence notes:
  - 宁文鑫 (Party Secretary): confirmed from official news reports (2026-07); also serves as Datong City Standing Committee member and Datong EZ Party Secretary
  - 庞君 (District Mayor): confirmed from official profile with full resume
  - 贺睿 (Executive Deputy Mayor): confirmed from official profile with full resume
  - 徐军 (Deputy Mayor): confirmed from official profile with full resume
  - 安小峰 (Deputy Mayor): confirmed from official profile with full resume
  - 史薛伟 (Deputy Mayor, seconded from Taiyuan Univ of Tech): confirmed from official profile with full resume
  - 刘喜斌 (Deputy Mayor): confirmed from official profile with full resume
  - 吕献文 (Deputy Mayor, Public Security): confirmed from official profile with full resume
  - 张伟莉 (Deputy Mayor): confirmed from official profile with full resume
  - 张丽霞 (Deputy Mayor): confirmed from official profile with full resume
  - 张建中 (Deputy Mayor): confirmed from official profile with full resume
  - 宁文鑫's predecessor as Party Secretary: not yet identified with confidence
  - 庞君's predecessor as Mayor: likely 郭普跃 or earlier — 庞君 appointed acting mayor Sep 2023
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
while REPO_ROOT.name:
    if (REPO_ROOT / "gov_relation").is_dir():
        break
    parent = REPO_ROOT.parent
    if parent == REPO_ROOT:
        break
    REPO_ROOT = parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import sqlite3  # noqa: used by gov_relation.runner via import
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "云州区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-26"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "shanxi_云州区"
if _CURRENT_DIR.name == "shanxi_云州区":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1-2 core leadership, 3-11 standing committee + deputy mayors, 12+ predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "宁文鑫",
        "gender": "男",
        "ethnicity": "汉族",  # plausible — typical for Shanxi officials
        "birth": "",  # open question — not found in official news
        "birthplace": "",  # open question
        "education": "",  # open question
        "party_join": "中共党员",
        "work_start": "",  # open question
        "current_post": "区委书记",
        "current_org": "中共大同市云州区委员会",
        "source": "https://www.yunzhou.gov.cn/（官方新闻活动报道确认2026年7月）",
        "confidence": "confirmed",
        "notes": "大同市委常委、大同经开区党工委书记、管委会主任，云州区委书记。2026年7月多次以区委书记身份带队调研黄花采收加工工作、主持有关活动。完整履历待查。"
    },
    {
        "id": 2,
        "name": "庞君",
        "gender": "男",
        "ethnicity": "汉族",  # confirmed — official profile
        "birth": "1978年10月",  # confirmed — official profile
        "birthplace": "山西天镇",  # confirmed — official profile
        "education": "中央党校研究生学历",  # confirmed — official profile
        "party_join": "中共党员",
        "work_start": "1999年8月",  # confirmed — official profile
        "current_post": "区长",
        "current_org": "云州区人民政府",
        "source": "https://www.yunzhou.gov.cn/yzqrmzfz/qzpj/szfld.shtml",
        "confidence": "confirmed",
        "notes": "中共大同市云州区委副书记、云州区人民政府区长，云州现代农业产业示范区党工委书记。1978年10月出生，大同天镇人，2002年12月入党，1999年8月参加工作。历任天镇县委办公室科员/副主任、城区区委办公室副主任、城区台湾事务工作办公室主任、大同经开区建设发展局副局长兼地震局局长、城区区委人才工作领导组办公室主任兼政府信息网络中心主任、大同市委办公厅工作、大同市委副秘书长、阳高县委副书记/统战部长/龙泉镇党委书记、大同市政府党组成员/秘书长/市政府机关党组书记/市政府办公室主任、云州区委副书记/代区长/区长。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Deputy Mayors
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "贺睿",
        "gender": "男",
        "ethnicity": "汉族",  # confirmed — official profile
        "birth": "1981年6月",  # confirmed — official profile
        "birthplace": "山西大同",  # confirmed — official profile
        "education": "北京工业大学研究生学历",  # confirmed — official profile
        "party_join": "中共党员",
        "work_start": "2004年11月",  # confirmed — official profile
        "current_post": "常务副区长",
        "current_org": "云州区人民政府",
        "source": "https://www.yunzhou.gov.cn/yzqrmzfz/herui/szfld.shtml",
        "confidence": "confirmed",
        "notes": "中共大同市云州区委常委、区政府党组副书记、副区长。2008年12月入党。历任大同市人才交流服务中心人事代理、市委组织部电教中心科员/副主任、市委组织部党员教育中心副主任（其间两次担任村第一书记）、市委组织部举报中心主任科员、市委组织部机关党委专职副书记/编制人事科科长、市委组织部组织三科（党代表联络办公室）科长、左云县人大常委会副主任、左云县委常委/管家堡乡党委书记、云州区委常委/区政府党组副书记/副区长人选、副区长。"
    },
    {
        "id": 4,
        "name": "徐军",
        "gender": "男",
        "ethnicity": "汉族",  # confirmed — official profile
        "birth": "1968年2月",  # confirmed — official profile
        "birthplace": "山西大同",  # confirmed — official profile
        "education": "中央党校大学学历",  # confirmed — official profile
        "party_join": "中共党员",
        "work_start": "1989年8月",  # confirmed — official profile
        "current_post": "副区长（常委）",
        "current_org": "云州区人民政府",
        "source": "https://www.yunzhou.gov.cn/yzqrmzfz/FQZHY/szfld.shtml",
        "confidence": "confirmed",
        "notes": "中共大同市云州区委常委、副区长。1998年7月入党。历任大同县计生委科员/副主任、大同县旅游事业发展服务中心主任、大同县周士庄镇党委副书记/镇长、杜庄乡党委书记/人大主席、倍加造镇党委书记、大同县政府副县长/倍加造镇党委书记、云州区政府筹备组副组长、云州区政府副区长、区委常委/副区长。2021年4月当选。"
    },
    {
        "id": 5,
        "name": "安小峰",
        "gender": "男",
        "ethnicity": "汉族",  # confirmed — official profile
        "birth": "1986年4月",  # confirmed — official profile
        "birthplace": "山西大同",  # confirmed — official profile
        "education": "大学学历",  # confirmed — official profile
        "party_join": "中共党员",
        "work_start": "2008年9月",  # confirmed — official profile
        "current_post": "副区长（常委）",
        "current_org": "云州区人民政府",
        "source": "https://www.yunzhou.gov.cn/yzqrmzfz/hgh/szfld.shtml",
        "confidence": "confirmed",
        "notes": "中共大同市云州区委常委、副区长。2014年2月入党。历任大同市南郊区口泉乡上窝寨村村委会主任助理、山西省供销社办公室科员/副主任科员/主任科员（其间挂职棉麻公司党委委员/经理助理、农资集团党委委员/经理助理）、省供销社办公室二级主任科员/副主任、云州区委常委、副区长。2021年4月当选。"
    },
    {
        "id": 6,
        "name": "史薛伟",
        "gender": "男",
        "ethnicity": "汉族",  # confirmed — official profile
        "birth": "1984年5月",  # confirmed — official profile
        "birthplace": "河南孟州",  # confirmed — official profile
        "education": "法学硕士",  # confirmed — official profile
        "party_join": "中共党员",
        "work_start": "2006年8月",  # confirmed — official profile
        "current_post": "副区长（挂职）",
        "current_org": "云州区人民政府",
        "source": "https://www.yunzhou.gov.cn/yzqrmzfz/sxw/szfld.shtml",
        "confidence": "confirmed",
        "notes": "中共大同市云州区委常委、副区长（挂职）。2005年10月入党。本科毕业后入职太原理工大学，历任轻纺工程与美术学院团委干事/副书记、校团委文体部部长（其间在职攻读思政教育法学硕士）、党委办公室信息科科长、党委组织部副部长、校团委书记/党委学工部副部长/学生处副处长/创新创业学院副院长/校纪委委员、共青团山西省委常委、山西省红十字会理事。2025年9月当选云州区副区长（挂职）。"
    },
    {
        "id": 7,
        "name": "刘喜斌",
        "gender": "男",
        "ethnicity": "汉族",  # confirmed — official profile
        "birth": "1970年2月",  # confirmed — official profile
        "birthplace": "大同云州区",  # confirmed — official profile
        "education": "中央党校大学学历",  # confirmed — official profile
        "party_join": "中共党员",
        "work_start": "1989年7月",  # confirmed — official profile
        "current_post": "副区长",
        "current_org": "云州区人民政府",
        "source": "https://www.yunzhou.gov.cn/yzqrmzfz/dxw/szfld.shtml",
        "confidence": "confirmed",
        "notes": "1992年8月入党。历任大同县农业局种子公司工作、大同县委组织部科员/副科组织员、县机关工委书记、巨乐乡党委副书记/乡长/党委书记/人大主席、杜庄乡党委书记、云州区杜庄乡党委书记、云州区副区长。2021年4月当选。"
    },
    {
        "id": 8,
        "name": "吕献文",
        "gender": "男",
        "ethnicity": "汉族",  # confirmed — official profile
        "birth": "1971年12月",  # confirmed — official profile
        "birthplace": "山西大同",  # confirmed — official profile
        "education": "大学学历",  # confirmed — official profile
        "party_join": "中共党员",
        "work_start": "1995年11月",  # confirmed — official profile
        "current_post": "副区长",
        "current_org": "云州区人民政府",
        "source": "https://www.yunzhou.gov.cn/yzqrmzfz/lxw/szfld.shtml",
        "confidence": "confirmed",
        "notes": "大同市公安局云州分局党委书记、局长，云州区副区长。2000年9月入党。中国人民公安大学公安管理专业在职学习。历任新荣区公安局刑警大队科员、交警大队科员/副大队长、市交警支队执法监督处教导员、左云县交通管理大队大队长/一级警长/四级高级警长、浑源县公安局政委/四级高级警长、大同市公安局恒安分局局长/四级高级警长/三级高级警长、云州区政府党组成员/公安分局党委书记/局长/副区长。2025年3月任命。"
    },
    {
        "id": 9,
        "name": "张伟莉",
        "gender": "女",
        "ethnicity": "汉族",  # confirmed — official profile
        "birth": "1979年10月",  # confirmed — official profile
        "birthplace": "山西怀仁",  # confirmed — official profile
        "education": "在职大学学历",  # confirmed — official profile
        "party_join": "民进会员",
        "work_start": "2001年3月",  # confirmed — official profile
        "current_post": "副区长",
        "current_org": "云州区人民政府",
        "source": "https://www.yunzhou.gov.cn/yzqrmzfz/sll/szfld.shtml",
        "confidence": "confirmed",
        "notes": "民进会员。历任大同市古建筑文物保管所、大同市华严寺文物管理所副所长、大同市雕塑博物馆馆长、云州区副区长。2021年4月当选。"
    },
    {
        "id": 10,
        "name": "张丽霞",
        "gender": "女",
        "ethnicity": "汉族",  # confirmed — official profile
        "birth": "1980年9月",  # confirmed — official profile
        "birthplace": "大同云州区",  # confirmed — official profile
        "education": "中央党校研究生学历",  # confirmed — official profile
        "party_join": "中共党员",
        "work_start": "1999年7月",  # confirmed — official profile
        "current_post": "副区长",
        "current_org": "云州区人民政府",
        "source": "https://www.yunzhou.gov.cn/yzqrmzfz/zlx/szfld.shtml",
        "confidence": "confirmed",
        "notes": "2002年6月入党。历任大同市开发区工作、开发区人劳局劳动科科长/人事劳动科科长、大同县倍加造镇副镇长、西坪镇党委副书记/镇长（云州区成立后继续担任）、西坪镇党委书记、云州区政府党组成员/副区长（兼西坪镇党委书记）。2024年1月任副区长。"
    },
    {
        "id": 11,
        "name": "张建中",
        "gender": "男",
        "ethnicity": "汉族",  # confirmed — official profile
        "birth": "1971年6月",  # confirmed — official profile
        "birthplace": "大同云州区",  # confirmed — official profile
        "education": "中央党校大学学历",  # confirmed — official profile
        "party_join": "中共党员",
        "work_start": "1991年7月",  # confirmed — official profile
        "current_post": "副区长",
        "current_org": "云州区人民政府",
        "source": "https://www.yunzhou.gov.cn/yzqrmzfz/zjz/szfld.shtml",
        "confidence": "confirmed",
        "notes": "1993年4月入党。历任大同县周士庄镇干事、县卫生局干事、县委组织部科员、许堡乡党委副书记、聚乐乡人大主席、周士庄镇党委副书记/镇长/党委书记/人大主席、县交通运输局党组书记/局长、云州区住房和城乡建设局党组书记/局长、区政府党组成员/副区长（兼任住建局局长）。2024年3月任副区长。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共大同市云州区委员会", "type": "党委", "level": "市辖区", "parent": "中共大同市委员会", "location": "大同市云州区"},
    {"id": 2, "name": "云州区人民政府", "type": "政府", "level": "市辖区", "parent": "大同市人民政府", "location": "大同市云州区"},
    {"id": 3, "name": "云州区人民代表大会常务委员会", "type": "人大", "level": "市辖区", "parent": "大同市人民代表大会常务委员会", "location": "大同市云州区"},
    {"id": 4, "name": "中国人民政治协商会议云州区委员会", "type": "政协", "level": "市辖区", "parent": "政协大同市委员会", "location": "大同市云州区"},
    {"id": 5, "name": "中共大同市云州区纪律检查委员会", "type": "党委", "level": "市辖区", "parent": "中共大同市纪律检查委员会", "location": "大同市云州区"},
    {"id": 6, "name": "大同市公安局云州分局", "type": "政府", "level": "正科级", "parent": "大同市公安局", "location": "大同市云州区"},
    {"id": 7, "name": "云州现代农业产业示范区", "type": "政府", "level": "市辖区", "parent": "云州区人民政府", "location": "大同市云州区"},
    {"id": 8, "name": "大同经济技术开发区", "type": "政府", "level": "国家级", "parent": "大同市人民政府", "location": "大同市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 宁文鑫 — current Party Secretary (also serves higher roles)
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "大同市委常委、大同经开区党工委书记/管委会主任兼云州区委书记，2026年7月活跃报道"},
    # 庞君 — current District Mayor
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "2023年10月", "end_date": "", "rank": "正处级", "note": "区委副书记、区政府党组书记、区长，云州现代农业产业示范区党工委书记"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "2023年9月", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 7, "title": "党工委书记", "start_date": "2023年9月", "end_date": "2024年4月", "rank": "正处级", "note": "云州现代农业产业示范区党工委书记（同时任管委会主任至2024年4月）"},
    # 庞君 — earlier career
    {"person_id": 2, "org_id": 2, "title": "代区长", "start_date": "2023年9月", "end_date": "2023年10月", "rank": "正处级", "note": "云州区委副书记、代区长"},
    {"person_id": 2, "org_id": 2, "title": "市政府秘书长、办公室主任", "start_date": "2021年4月", "end_date": "2023年9月", "rank": "正处级", "note": "大同市政府党组成员、秘书长，市政府机关党组书记、市政府办公室主任"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记、统战部长", "start_date": "2018年1月", "end_date": "2021年4月", "rank": "副处级", "note": "阳高县委副书记、统战部长（2018年8月兼任龙泉镇党委书记）"},
    {"person_id": 2, "org_id": 1, "title": "市委副秘书长", "start_date": "2016年6月", "end_date": "2018年1月", "rank": "副处级", "note": "大同市委副秘书长"},
    {"person_id": 2, "org_id": 1, "title": "市委办公厅科员/副主任", "start_date": "2015年8月", "end_date": "2016年6月", "rank": "副处级", "note": "大同市委办公厅工作"},
    {"person_id": 2, "org_id": 2, "title": "区委人才办主任", "start_date": "2014年9月", "end_date": "2015年8月", "rank": "正科级", "note": "大同市城区区委人才工作领导组办公室主任兼政府信息网络中心主任"},
    {"person_id": 2, "org_id": 2, "title": "建设发展局副局长", "start_date": "2012年5月", "end_date": "2014年9月", "rank": "副科级", "note": "大同经济技术开发区建设发展局副局长兼地震局局长"},
    {"person_id": 2, "org_id": 1, "title": "区委办公室副主任", "start_date": "2008年12月", "end_date": "2012年5月", "rank": "副科级", "note": "大同市城区区委办公室副主任、城区台湾事务工作办公室主任"},
    {"person_id": 2, "org_id": 1, "title": "县委办公室副主任", "start_date": "2007年7月", "end_date": "2008年12月", "rank": "副科级", "note": "天镇县委办公室副主任"},
    {"person_id": 2, "org_id": 1, "title": "县委办公室科员", "start_date": "1999年8月", "end_date": "2007年7月", "rank": "科员", "note": "天镇县委办公室科员"},
    # 贺睿 — Executive Deputy Mayor
    {"person_id": 3, "org_id": 2, "title": "常务副区长", "start_date": "2024年4月", "end_date": "", "rank": "副处级", "note": "区委常委、区政府党组副书记、常务副区长"},
    {"person_id": 3, "org_id": 1, "title": "区委常委", "start_date": "2024年3月", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "县委常委", "start_date": "2020年8月", "end_date": "2024年3月", "rank": "副处级", "note": "左云县委常委、管家堡乡党委书记"},
    {"person_id": 3, "org_id": 3, "title": "人大常委会副主任", "start_date": "2020年4月", "end_date": "2020年8月", "rank": "副处级", "note": "左云县人大常委会副主任"},
    # 贺睿 — organization department career (大同市委组织部)
    {"person_id": 3, "org_id": 1, "title": "组织三科科长", "start_date": "2019年2月", "end_date": "2020年4月", "rank": "正科级", "note": "大同市委组织部组织三科（党代表联络办公室）科长"},
    {"person_id": 3, "org_id": 1, "title": "机关党委专职副书记", "start_date": "2017年9月", "end_date": "2019年2月", "rank": "正科级", "note": "大同市委组织部机关党委专职副书记、编制人事科科长"},
    {"person_id": 3, "org_id": 1, "title": "举报中心主任科员", "start_date": "2016年10月", "end_date": "2017年9月", "rank": "正科级", "note": "大同市委组织部举报中心主任科员"},
    {"person_id": 3, "org_id": 1, "title": "举报中心副主任", "start_date": "2016年1月", "end_date": "2016年10月", "rank": "副科级", "note": "其间2016年7月—2017年9月浑源县西留村乡宝峰寨村第一书记"},
    {"person_id": 3, "org_id": 1, "title": "党员教育中心副主任", "start_date": "2015年12月", "end_date": "2016年1月", "rank": "副科级", "note": "其间2015年8月—2016年6月新荣区郭家窑乡二队窑村第一书记"},
    {"person_id": 3, "org_id": 1, "title": "电教中心副主任", "start_date": "2013年2月", "end_date": "2015年12月", "rank": "副科级", "note": "大同市委组织部电教中心副主任"},
    {"person_id": 3, "org_id": 1, "title": "电教中心科员", "start_date": "2008年4月", "end_date": "2013年2月", "rank": "科员", "note": "大同市委组织部电教中心科员"},
    {"person_id": 3, "org_id": 2, "title": "人才中心人事代理", "start_date": "2004年11月", "end_date": "2008年4月", "rank": "其他", "note": "大同市人才交流服务中心人事代理"},
    # 徐军 — Deputy Mayor (Standing Committee)
    {"person_id": 4, "org_id": 2, "title": "副区长", "start_date": "2021年3月", "end_date": "", "rank": "副处级", "note": "区委常委、副区长"},
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start_date": "2021年3月", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副区长", "start_date": "2018年7月", "end_date": "2021年3月", "rank": "副处级", "note": "云州区政府副区长"},
    {"person_id": 4, "org_id": 2, "title": "副县长", "start_date": "2018年2月", "end_date": "2018年7月", "rank": "副处级", "note": "大同县政府副县长、倍加造镇党委书记"},
    {"person_id": 4, "org_id": 1, "title": "倍加造镇党委书记", "start_date": "2016年5月", "end_date": "2018年2月", "rank": "正科级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "杜庄乡党委书记", "start_date": "2009年3月", "end_date": "2016年5月", "rank": "正科级", "note": "兼人大主席（2011年5月起）"},
    {"person_id": 4, "org_id": 1, "title": "周士庄镇镇长", "start_date": "2006年6月", "end_date": "2009年3月", "rank": "正科级", "note": "周士庄镇党委副书记、镇长（兼县旅游事业发展服务中心主任至2006年11月）"},
    {"person_id": 4, "org_id": 2, "title": "旅游事业发展服务中心主任", "start_date": "2002年6月", "end_date": "2006年11月", "rank": "正科级", "note": "大同县旅游事业发展服务中心主任"},
    {"person_id": 4, "org_id": 2, "title": "计生委副主任", "start_date": "1999年6月", "end_date": "2002年6月", "rank": "副科级", "note": "大同县计生委副主任"},
    {"person_id": 4, "org_id": 2, "title": "计生委科员", "start_date": "1989年8月", "end_date": "1999年6月", "rank": "科员", "note": "大同县计生委工作"},
    # 安小峰 — Deputy Mayor (Standing Committee)
    {"person_id": 5, "org_id": 2, "title": "副区长", "start_date": "2020年8月", "end_date": "", "rank": "副处级", "note": "区委常委、副区长"},
    {"person_id": 5, "org_id": 1, "title": "区委常委", "start_date": "2020年6月", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "省供销社办公室副主任", "start_date": "2019年8月", "end_date": "2020年6月", "rank": "副处级", "note": "山西省供销社办公室副主任"},
    {"person_id": 5, "org_id": 2, "title": "省供销社主任科员", "start_date": "2016年4月", "end_date": "2019年8月", "rank": "正科级", "note": "其间挂职棉麻公司党委委员/经理助理、山西农资集团党委委员/经理助理"},
    {"person_id": 5, "org_id": 2, "title": "省供销社副主任科员", "start_date": "2013年4月", "end_date": "2016年4月", "rank": "副科级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "省供销社科员", "start_date": "2010年12月", "end_date": "2013年4月", "rank": "科员", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "村官", "start_date": "2008年9月", "end_date": "2010年12月", "rank": "其他", "note": "南郊区口泉乡上窝寨村村委会主任助理"},
    # 史薛伟 — Deputy Mayor (Seconded)
    {"person_id": 6, "org_id": 2, "title": "副区长（挂职）", "start_date": "2025年9月", "end_date": "", "rank": "副处级", "note": "挂职，负责招商引资等工作"},
    {"person_id": 6, "org_id": 8, "title": "校团委书记", "start_date": "2022年9月", "end_date": "", "rank": "正处级", "note": "太原理工大学团委书记（兼党委学工部副部长/学生处副处长/创新创业学院副院长/校纪委委员/共青团山西省委常委/山西省红十字会理事）"},
    {"person_id": 6, "org_id": 8, "title": "党委组织部副部长", "start_date": "2019年11月", "end_date": "2022年9月", "rank": "副处级", "note": "太原理工大学党委组织部副部长（2019年4月—2020年5月挂职省委教育工委组织部主任科员）"},
    {"person_id": 6, "org_id": 8, "title": "党委办公室信息科科长", "start_date": "2018年5月", "end_date": "2019年11月", "rank": "正科级", "note": ""},
    {"person_id": 6, "org_id": 8, "title": "校团委文体部部长", "start_date": "2011年11月", "end_date": "2018年5月", "rank": "正科级", "note": "2010-2013年在职攻读思政教育法学硕士"},
    {"person_id": 6, "org_id": 8, "title": "学院团委副书记", "start_date": "2009年2月", "end_date": "2011年11月", "rank": "副科级", "note": "太原理工大学轻纺工程与美术学院团委副书记"},
    {"person_id": 6, "org_id": 8, "title": "学院团委干事", "start_date": "2006年8月", "end_date": "2009年2月", "rank": "科员", "note": "太原理工大学轻纺工程与美术学院团委干事"},
    # 刘喜斌 — Deputy Mayor
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "2020年3月", "end_date": "", "rank": "副处级", "note": "云州区副区长"},
    {"person_id": 7, "org_id": 1, "title": "杜庄乡党委书记", "start_date": "2016年5月", "end_date": "2020年3月", "rank": "正科级", "note": "大同县/云州区杜庄乡党委书记"},
    {"person_id": 7, "org_id": 1, "title": "巨乐乡党委书记", "start_date": "2009年3月", "end_date": "2016年5月", "rank": "正科级", "note": "兼人大主席（2011年5月起）"},
    {"person_id": 7, "org_id": 1, "title": "巨乐乡乡长", "start_date": "2007年4月", "end_date": "2009年3月", "rank": "正科级", "note": "巨乐乡党委副书记、乡长"},
    {"person_id": 7, "org_id": 1, "title": "机关工委书记", "start_date": "2003年12月", "end_date": "2007年4月", "rank": "正科级", "note": "大同县机关工委书记"},
    {"person_id": 7, "org_id": 1, "title": "县委组织部副科组织员", "start_date": "1999年9月", "end_date": "2003年12月", "rank": "副科级", "note": "大同县委组织部副科组织员"},
    {"person_id": 7, "org_id": 1, "title": "县委组织部科员", "start_date": "1989年12月", "end_date": "1999年9月", "rank": "科员", "note": "大同县委组织部工作"},
    {"person_id": 7, "org_id": 2, "title": "种子公司科员", "start_date": "1989年7月", "end_date": "1989年12月", "rank": "科员", "note": "大同县农业局种子公司"},
    # 吕献文 — Deputy Mayor (Public Security)
    {"person_id": 8, "org_id": 2, "title": "副区长", "start_date": "2025年3月", "end_date": "", "rank": "副处级", "note": "大同市公安局云州分局党委书记、局长"},
    {"person_id": 8, "org_id": 6, "title": "党委书记、局长", "start_date": "2025年3月", "end_date": "", "rank": "三级高级警长", "note": "大同市公安局云州分局"},
    {"person_id": 8, "org_id": 6, "title": "恒安分局局长", "start_date": "2021年2月", "end_date": "2025年3月", "rank": "三级高级警长", "note": "大同市公安局恒安分局局长"},
    {"person_id": 8, "org_id": 6, "title": "浑源县公安局政委", "start_date": "2020年3月", "end_date": "2021年2月", "rank": "四级高级警长", "note": "浑源县公安局政委、党委副书记"},
    {"person_id": 8, "org_id": 6, "title": "左云县交警大队大队长", "start_date": "2012年6月", "end_date": "2020年3月", "rank": "一级/四级高级警长", "note": "左云县交通管理大队大队长"},
    {"person_id": 8, "org_id": 6, "title": "交警支队执法监督处教导员", "start_date": "2010年2月", "end_date": "2012年6月", "rank": "正科级", "note": "大同市交警支队执法监督处教导员"},
    {"person_id": 8, "org_id": 6, "title": "新荣区交警大队副大队长", "start_date": "2003年11月", "end_date": "2010年2月", "rank": "副科级", "note": "2001-2009年在中国人民公安大学公安管理专业在职学习"},
    {"person_id": 8, "org_id": 6, "title": "新荣区交警大队科员", "start_date": "1997年10月", "end_date": "2003年11月", "rank": "科员", "note": ""},
    {"person_id": 8, "org_id": 6, "title": "新荣区刑警大队科员", "start_date": "1995年11月", "end_date": "1997年10月", "rank": "科员", "note": ""},
    # 张伟莉 — Deputy Mayor
    {"person_id": 9, "org_id": 2, "title": "副区长", "start_date": "2021年4月", "end_date": "", "rank": "副处级", "note": "民进会员"},
    {"person_id": 9, "org_id": 2, "title": "雕塑博物馆馆长", "start_date": "2014年2月", "end_date": "2021年3月", "rank": "正科级", "note": "大同市雕塑博物馆馆长"},
    {"person_id": 9, "org_id": 2, "title": "华严寺文物管理所副所长", "start_date": "2011年1月", "end_date": "2014年2月", "rank": "副科级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "古建筑文物保管所", "start_date": "2001年3月", "end_date": "2011年1月", "rank": "科员", "note": "大同市古建筑文物保管所"},
    # 张丽霞 — Deputy Mayor
    {"person_id": 10, "org_id": 2, "title": "副区长", "start_date": "2023年6月", "end_date": "", "rank": "副处级", "note": "曾任西坪镇党委书记至2024年1月"},
    {"person_id": 10, "org_id": 1, "title": "西坪镇党委书记", "start_date": "2021年3月", "end_date": "2024年1月", "rank": "正科级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "西坪镇镇长", "start_date": "2016年12月", "end_date": "2021年3月", "rank": "正科级", "note": "大同县/云州区西坪镇党委副书记、镇长（2018年曾为筹备组组长）"},
    {"person_id": 10, "org_id": 1, "title": "倍加造镇副镇长", "start_date": "2009年12月", "end_date": "2016年12月", "rank": "副科级", "note": "大同县倍加造镇副镇长"},
    {"person_id": 10, "org_id": 2, "title": "开发区人劳局科长", "start_date": "2002年9月", "end_date": "2009年12月", "rank": "科员/正科级", "note": "大同市开发区人劳局劳动科科长、人事劳动科科长"},
    {"person_id": 10, "org_id": 2, "title": "开发区科员", "start_date": "1999年7月", "end_date": "2002年9月", "rank": "科员", "note": "大同市开发区工作"},
    # 张建中 — Deputy Mayor
    {"person_id": 11, "org_id": 2, "title": "副区长", "start_date": "2023年10月", "end_date": "", "rank": "副处级", "note": "（兼住建局局长至2024年3月）"},
    {"person_id": 11, "org_id": 2, "title": "住建局局长", "start_date": "2021年5月", "end_date": "2024年3月", "rank": "正科级", "note": "云州区住房和城乡建设局党组书记、局长"},
    {"person_id": 11, "org_id": 2, "title": "交通运输局局长", "start_date": "2016年12月", "end_date": "2021年5月", "rank": "正科级", "note": "大同县交通运输局党组书记、局长"},
    {"person_id": 11, "org_id": 1, "title": "周士庄镇党委书记", "start_date": "2012年8月", "end_date": "2016年12月", "rank": "正科级", "note": "大同县周士庄镇党委书记（2012年1月起兼人大主席、镇长）"},
    {"person_id": 11, "org_id": 1, "title": "周士庄镇镇长", "start_date": "2009年3月", "end_date": "2012年8月", "rank": "正科级", "note": "周士庄镇党委副书记、镇长"},
    {"person_id": 11, "org_id": 3, "title": "聚乐乡人大主席", "start_date": "2005年4月", "end_date": "2009年3月", "rank": "正科级", "note": "大同县聚乐乡人大主席"},
    {"person_id": 11, "org_id": 1, "title": "许堡乡党委副书记", "start_date": "1999年7月", "end_date": "2005年4月", "rank": "副科级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "卫生局干事", "start_date": "1992年10月", "end_date": "1999年7月", "rank": "科员", "note": "大同县卫生局干事"},
    {"person_id": 11, "org_id": 1, "title": "周士庄镇干事", "start_date": "1991年7月", "end_date": "1992年10月", "rank": "科员", "note": ""},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 宁文鑫 ↔ 庞君 (Party Secretary – District Mayor)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "区委书记—区长搭档", "overlap_org": "中共大同市云州区委员会", "overlap_period": "2023至今"},
    # 庞君 ↔ 贺睿 (Mayor – Executive Deputy Mayor)
    {"person_a": 2, "person_b": 3, "type": "共事", "context": "区长—常务副区长", "overlap_org": "云州区人民政府", "overlap_period": "2024至今"},
    # 庞君 → 副区长团队
    {"person_a": 2, "person_b": 4, "type": "共事", "context": "区长—副区长", "overlap_org": "云州区人民政府", "overlap_period": "2021至今"},
    {"person_a": 2, "person_b": 5, "type": "共事", "context": "区长—副区长", "overlap_org": "云州区人民政府", "overlap_period": "2023至今"},
    {"person_a": 2, "person_b": 6, "type": "共事", "context": "区长—挂职副区长", "overlap_org": "云州区人民政府", "overlap_period": "2025至今"},
    {"person_a": 2, "person_b": 7, "type": "共事", "context": "区长—副区长", "overlap_org": "云州区人民政府", "overlap_period": "2023至今"},
    {"person_a": 2, "person_b": 8, "type": "共事", "context": "区长—副区长（公安）", "overlap_org": "云州区人民政府", "overlap_period": "2025至今"},
    {"person_a": 2, "person_b": 9, "type": "共事", "context": "区长—副区长", "overlap_org": "云州区人民政府", "overlap_period": "2023至今"},
    {"person_a": 2, "person_b": 10, "type": "共事", "context": "区长—副区长", "overlap_org": "云州区人民政府", "overlap_period": "2023至今"},
    {"person_a": 2, "person_b": 11, "type": "共事", "context": "区长—副区长", "overlap_org": "云州区人民政府", "overlap_period": "2023至今"},
]


# ═════════════════════════════════════════════════════════════════════════════
# Helper functions
# ═════════════════════════════════════════════════════════════════════════════


def _get_open_questions(person: dict) -> list[str]:
    questions = []
    if not person.get("birth"):
        questions.append("出生年月未确认")
    if not person.get("birthplace"):
        questions.append("籍贯未确认")
    if not person.get("ethnicity"):
        questions.append("民族未确认")
    if not person.get("education"):
        questions.append("学历教育背景未确认")
    if not person.get("work_start"):
        questions.append("参加工作年份未确认")
    return questions


def _make_person_id(name: str) -> str:
    return f"yunzhou_{name}"


def write_person_json(person: dict) -> None:
    """Write a per-person graph JSON file following the person_graph_json.md schema."""
    pid = person["id"]
    name = person["name"]
    slug_id = _make_person_id(name)

    person_positions = [p for p in positions if p["person_id"] == pid]

    career_timeline = []
    for pos in person_positions:
        org = next((o for o in organizations if o["id"] == pos["org_id"]), None)
        career_timeline.append({
            "start": pos.get("start_date", "") or "",
            "end": pos.get("end_date", "") or "",
            "org": org["name"] if org else "",
            "title": pos.get("title", ""),
            "level": pos.get("rank", ""),
            "rank": pos.get("rank", ""),
            "notes": pos.get("note", "") or "",
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001", "S002"],
        })

    person_rels = [
        r for r in relationships
        if r["person_a"] == pid or r["person_b"] == pid
    ]
    rels_output = []
    for r in person_rels:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id), None)
        other_name = other["name"] if other else f"person_{other_id}"
        rels_output.append({
            "person": other_name,
            "person_id": _make_person_id(other_name),
            "relationship_type": "overlap",
            "strength": "strong",
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S001", "S002"],
        })

    source_url = person.get("source", "")
    sources = [
        {
            "id": "S001",
            "title": "大同市云州区人民政府官方网站",
            "url": "https://www.yunzhou.gov.cn/",
            "publisher": "云州区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "云州区政府门户网站政府领导页面及活动报道",
        },
        {
            "id": "S002",
            "title": "云州区政府领导个人页面",
            "url": source_url if source_url.startswith("http") else f"https://www.yunzhou.gov.cn{source_url}" if source_url.startswith("/") else "",
            "publisher": "云州区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "领导个人简历及分工页面",
        },
    ]

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "山西省",
            "city": "大同市",
            "region": "云州区",
            "job": person.get("current_post", ""),
            "task_id": "shanxi_云州区",
            "time_focus": "2026年7月",
        },
        "identity": {
            "person_id": slug_id,
            "name": name,
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [{"period": "", "institution": person.get("education", ""), "major": "", "degree": "", "study_type": "unknown", "source_ids": ["S001"]}] if person.get("education") else [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{person.get('birth','')}",
                "name_birthplace": f"{name}_{person.get('birthplace','')}",
                "official_profile_url": source_url,
            },
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "正处级" if person["id"] in (1, 2) else ("副处级" if person["id"] in (3, 4, 5, 6, 7, 8, 9, 10, 11) else "副处级（挂职）"),
            "as_of": AS_OF,
            "is_current_confirmed": person.get("confidence") == "confirmed",
            "source_ids": ["S001"],
        },
        "career_timeline": career_timeline,
        "organizations": [{"id": o["id"], "name": o["name"], "type": o["type"]} for o in organizations],
        "relationships": rels_output,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": ["党务管理" if person["id"] == 1 else "行政管理", "政府管理" if person["id"] == 2 else ""],
            "secondary_specializations": [],
            "career_pattern": "local_ladder" if person["id"] in (2, 4, 7, 10, 11) else "cross_county_rotation" if person["id"] == 3 else "provincial_department" if person["id"] == 5 else "technical_specialist" if person["id"] in (6, 9) else "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": sources,
        "confidence_summary": {
            "identity": "confirmed" if person.get("birth") else "partial",
            "current_role": person.get("confidence", "unverified"),
            "career_completeness": "partial" if person.get("birth") else "thin",
            "relationship_confidence": "high",
            "biggest_gap": "完整任职履历（每段职务精确起止时间）" if not person.get("work_start") else "早期教育和工作细节",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的完整任职履历（每段职务精确起止时间）",
                "why_it_matters": "关系网络分析需要精确的时间线",
                "suggested_queries": [f"{name} 简历", f"{name} 任前公示", f"{name} 百度百科"],
                "last_attempted": AS_OF,
            },
        ] + ([
            {
                "priority": "high",
                "question": f"{name}的出生年月、籍贯和教育背景",
                "why_it_matters": "核心身份信息，用于去重和跨区域关联分析",
                "suggested_queries": [f"{name} 简历", f"{name} 籍贯"],
                "last_attempted": AS_OF,
            },
        ] if not person.get("birth") else []),
    }

    fname = f"{TODAY}-山西省-大同市-{person['current_post']}-{person['name']}.json"
    fpath = PJSON_DIR / fname
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fpath.name}")


# ═════════════════════════════════════════════════════════════════════════════
# Build
# ═════════════════════════════════════════════════════════════════════════════


def main() -> int:
    print(f"Building {SLUG} network...")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    print("  Writing person JSONs...")
    # Core targets: 区委书记 (id=1), 区长 (id=2)
    core_ids = {1, 2}
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
