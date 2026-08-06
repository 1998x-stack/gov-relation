#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 公主岭市 (Gongzhuling), 吉林省.

Investigation date: 2026-08-06
Task ID: jilin_公主岭市
Level: 县级市
Targets: 市委书记 & 市长

Research sources:
  - Official government site (live, HTTP): http://www.gongzhuling.gov.cn/
    - Leader index (/szf/zfld/), per-leader resume pages (/wdjl/), leader activity
      (/zw/dzxx/ldhd/), 重要会议 (/jyhy/), 市委常委会/理论学习中心组 articles.
  - Leader activity archives across 2025–2026 (to establish roster & governance evidence).

Confidence notes:
  - 赵师骐 (市委书记): confirmed — official bio (born 1981-04, 满族, 吉林长春, 研究生, 2003-09 参加工作).
  - 王贺军 (市长): confirmed — official bio (born 1979-07, 汉族, 大学本科/工学学士).
  - 常务副市长 牟兆彬: confirmed — official bio + 市委理论学习中心组成员 (常委).
  - Full 副市长 roster & 人大/政协 leadership: confirmed via official leaderboard pages.
  - Predecessor 市委书记 & definite 常委 department head roles (纪委书记/宣传部长/统战部长)
    not enumerable from official pages under degraded web search (engines blocked); encoded as
    open gaps rather than fabricated.
  - All claims labeled with confidence; gaps explicitly documented.
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import sqlite3  # noqa: used by gov_relation.runner via import
from gov_relation.runner import run_build

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "公主岭市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "jilin_公主岭市"
if _CURRENT_DIR.name == "jilin_公主岭市":
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
persons = [
    # ══════════════ Core (current) ══════════════
    {
        "id": 1, "name": "赵师骐", "gender": "男", "ethnicity": "满族",
        "birth": "1981-04", "birthplace": "吉林长春", "education": "研究生",
        "party_join": "中共党员", "work_start": "2003-09",
        "current_post": "市委书记", "current_org": "中共公主岭市委",
        "source": "http://www.gongzhuling.gov.cn/szf/zfld/swsj/zsq/",
        "confidence": "confirmed",
        "notes": "现任中共公主岭市委书记、中共吉林长春国家农业高新技术产业示范区工作委员会书记。曾任长春市财政局粮食贸易处副处长；长春市委办公厅常委工作办公室正处级秘书（其间2010.10--2012.10挂职德惠市财政局副局长）；长春市政府办公厅秘书处处长；长春市政府办公厅副主任；双阳区委常委、副区长；公主岭市委副书记、市长。跨区（长春市直/双阳区→公主岭市）调任并本地晋升。2003年9月参加工作，2006年9月入党。",
    },
    {
        "id": 2, "name": "王贺军", "gender": "男", "ethnicity": "汉族",
        "birth": "1979-07", "birthplace": "", "education": "大学本科（工学学士）",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市长", "current_org": "公主岭市人民政府",
        "source": "http://www.gongzhuling.gov.cn/sz/wdjl/",
        "confidence": "confirmed",
        "notes": "现任中共公主岭市委副书记、公主岭市人民政府市长、中共吉林长春国家农业高新技术产业示范区工作委员会副书记。曾任长春市发展和改革委员会高技术处副处长、(大项目办)重大项目谋划处副处长/处长、高技术产业处处长、能源交通处(市国防动员委员会交通战备办公室)处长、高技术产业处处长、服务业发展办公室主任；长春市绿园区人民政府副区长；公主岭市副市长、代市长。跨市(长春市直/绿园区→公主岭市)调任。",
    },
    # ══════════════ 市委班子 ══════════════
    {
        "id": 10, "name": "牟兆彬", "gender": "男", "ethnicity": "汉族",
        "birth": "1982-06", "birthplace": "吉林榆树", "education": "研究生",
        "party_join": "中共党员", "work_start": "2002-08",
        "current_post": "市委常委、常务副市长", "current_org": "公主岭市人民政府",
        "source": "http://www.gongzhuling.gov.cn/szf/zfld/fsz/mzb/",
        "confidence": "confirmed",
        "notes": "现任中共公主岭市委常委、副市长，吉林长春国家农业高新技术产业示范区工作委员会委员、管委会副主任。曾任榆树市环城乡副乡长，共青团榆树市委副书记，榆树市五棵树镇党委副书记、人大主席，榆树市育民乡党委书记，榆树市委办公室主任，榆树市副市长，德惠市委常委、副市长，农高区管委会副主任。跨县(榆树/德惠→公主岭)调任。",
    },
    {
        "id": 3, "name": "杨诠湧", "gender": "男", "ethnicity": "汉族",
        "birth": "1976-08", "birthplace": "辽宁黑山", "education": "大学本科",
        "party_join": "中共党员", "work_start": "1995-05",
        "current_post": "副市长", "current_org": "公主岭市人民政府",
        "source": "http://www.gongzhuling.gov.cn/szf/zfld/fsz/yqy/",
        "confidence": "confirmed",
        "notes": "曾任青崴子街道办事主任、党委书记、人大工委主任，龙山区镇党委书记，工信局党组书记、局长，发改局党组书记、局长。现任公主岭市副市长。本地成长（镇街→局办→市政府）。",
    },
    {
        "id": 4, "name": "王志刚", "gender": "男", "ethnicity": "汉族",
        "birth": "1982-03", "birthplace": "吉林松原", "education": "大学",
        "party_join": "中共党员", "work_start": "2003-07",
        "current_post": "副市长、市公安局党委书记、局长", "current_org": "公主岭市人民政府",
        "source": "http://www.gongzhuling.gov.cn/szf/zfld/fsz/wzg/",
        "confidence": "confirmed",
        "notes": "现任公主岭副市长、市公安局党委书记、局长、督察长。2006年6月入党。公安系统。",
    },
    {
        "id": 5, "name": "王永恒", "gender": "男", "ethnicity": "汉族",
        "birth": "1981-05", "birthplace": "吉林公主岭", "education": "本科",
        "party_join": "中共党员", "work_start": "2000-07",
        "current_post": "副市长", "current_org": "公主岭市人民政府",
        "source": "http://www.gongzhuling.gov.cn/szf/zfld/fsz/wyh/",
        "confidence": "confirmed",
        "notes": "现任公主岭市副市长、公主岭经济开发区党工委副书记、范家屯镇党委书记。本地成长。",
    },
    {
        "id": 6, "name": "曾剑", "gender": "男", "ethnicity": "汉族",
        "birth": "1987-06", "birthplace": "四川遂宁", "education": "在职研究生",
        "party_join": "中共党员", "work_start": "2008-12",
        "current_post": "副市长", "current_org": "公主岭市人民政府",
        "source": "http://www.gongzhuling.gov.cn/szf/zfld/fsz/zjh/",
        "confidence": "confirmed",
        "notes": "现任公主岭市副市长。2006年6月入党。年轻干部。",
    },
    {
        "id": 7, "name": "范庆庆", "gender": "女", "ethnicity": "汉族",
        "birth": "1986-10", "birthplace": "吉林长春", "education": "大学本科",
        "party_join": "中共党员", "work_start": "2009-07",
        "current_post": "市委常委、副市长", "current_org": "公主岭市人民政府",
        "source": "http://www.gongzhuling.gov.cn/szf/zfld/fsz/fqq/",
        "confidence": "confirmed",
        "notes": "市委理论学习中心组成员（常委）。现任公主岭市委常委、副市长。2007年5月入党。长春干部。",
    },
    {
        "id": 8, "name": "赵明", "gender": "男", "ethnicity": "汉族",
        "birth": "1982-06", "birthplace": "吉林榆树", "education": "研究生",
        "party_join": "中共党员", "work_start": "2007-09",
        "current_post": "副市长", "current_org": "公主岭市人民政府",
        "source": "http://www.gongzhuling.gov.cn/sz/zfld/fsz/zm/",
        "confidence": "confirmed",
        "notes": "现任公主岭市副市长。2006年5月入党。",
    },
    {
        "id": 9, "name": "黄利", "gender": "男", "ethnicity": "汉族",
        "birth": "1981-05", "birthplace": "湖北黄冈", "education": "大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副市长", "current_org": "公主岭市人民政府",
        "source": "http://www.gongzhuling.gov.cn/szf/zfld/fsz/hl/",
        "confidence": "confirmed",
        "notes": "现任公主岭市副市长。跨省(湖北→吉林)干部。",
    },
    {
        "id": 11, "name": "孙昊", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委常委、组织部部长", "current_org": "中共公主岭市委组织部",
        "source": "http://www.gongzhuling.gov.cn/zw/dzxx/ldhd/ (buyi活动归档)",
        "confidence": "plausible",
        "notes": "任前公示/活动归档确认：因仪式、走访慰问等活动中以'市委常委、组织部部长'身份出现。履历细节待查。",
    },
    # ══════════════ 人大 / 政协 ══════════════
    {
        "id": 30, "name": "孙胜军", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市人大常委会党组书记、主任", "current_org": "公主岭市人大常委会",
        "source": "http://www.gongzhuling.gov.cn/zw/dzxx/ldhd/ (领导活动归档)",
        "confidence": "plausible",
        "notes": "任市人大常委会主任，多次在领导慰问/重要会议中以'市人大常委会主任'身份与市委书记、市长并列出现。履历待查。",
    },
    {
        "id": 40, "name": "董华", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市政协党组书记、主席", "current_org": "政协公主岭市委员会",
        "source": "http://www.gongzhuling.gov.cn/zw/dzxx/ldhd/ (领导活动归档)",
        "confidence": "plausible",
        "notes": "任市政协主席，在'八一'慰问等活动中以'市政协主席董华'身份带队。履历待查。",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共公主岭市委", "type": "党委", "level": "县级", "parent": "中共长春市委", "location": "公主岭市"},
    {"id": 2, "name": "公主岭市人民政府", "type": "政府", "level": "县级", "parent": "长春市人民政府", "location": "公主岭市"},
    {"id": 3, "name": "中共公主岭市委组织部", "type": "党委部门", "level": "县级", "parent": "中共公主岭市委", "location": "公主岭市"},
    {"id": 8, "name": "公主岭市人大常委会", "type": "人大", "level": "县级", "parent": "长春市人大常委会", "location": "公主岭市"},
    {"id": 9, "name": "中国人民政治协商会议公主岭市委员会", "type": "政协", "level": "县级", "parent": "政协长春市委员会", "location": "公主岭市"},
    {"id": 10, "name": "吉林长春国家农业高新技术产业示范区", "type": "开发区", "level": "副处级", "parent": "长春市人民政府", "location": "公主岭市"},
    {"id": 11, "name": "中共长春市委", "type": "党委", "level": "副省级", "parent": "中共吉林省委", "location": "长春市"},
    {"id": 12, "name": "长春市人民政府", "type": "政府", "level": "副省级", "parent": "吉林省人民政府", "location": "长春市"},
    {"id": 13, "name": "中共长春市双阳区委", "type": "党委", "level": "县级", "parent": "中共长春市委", "location": "长春市双阳区"},
    {"id": 14, "name": "长春市双阳区人民政府", "type": "政府", "level": "县级", "parent": "长春市人民政府", "location": "长春市双阳区"},
    {"id": 15, "name": "中共长春市绿园区委员会", "type": "党委", "level": "县级", "parent": "中共长春市委", "location": "长春市绿园区"},
    {"id": 16, "name": "长春市绿园区人民政府", "type": "政府", "level": "县级", "parent": "长春市人民政府", "location": "长春市绿园区"},
    ]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 赵师骐
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "2023", "end_date": "present", "rank": "正处", "note": "现任中共公主岭市委书记、农高区党工委书记"},
    {"person_id": 1, "org_id": 1, "title": "市委副书记、市长", "start_date": "2021", "end_date": "2023", "rank": "正处", "note": "历任公主岭市长"},
    {"person_id": 1, "org_id": 14, "title": "双阳区委常委、副区长", "start_date": "", "end_date": "2021", "rank": "副处", "note": ""},
    {"person_id": 1, "org_id": 11, "title": "长春市政府办公厅副主任", "start_date": "", "end_date": "", "rank": "副处", "note": ""},
    {"person_id": 1, "org_id": 11, "title": "长春市政府办公厅秘书处处长", "start_date": "", "end_date": "", "rank": "正处", "note": ""},
    {"person_id": 1, "org_id": 11, "title": "长春市委办公厅常委工作办公室正处级秘书", "start_date": "", "end_date": "", "rank": "正处", "note": "2010.10--2012.10 挂职德惠市财政局副局长"},
    {"person_id": 1, "org_id": 12, "title": "长春市财政局粮食贸易处副处长", "start_date": "", "end_date": "", "rank": "副处", "note": ""},
    # 王贺军
    {"person_id": 2, "org_id": 2, "title": "市长(市政府党组书记)", "start_date": "2024", "end_date": "present", "rank": "正处", "note": "现任公主岭市委副书记、市长"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记(兼)", "start_date": "2024", "end_date": "present", "rank": "正处", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "副市长、代市长", "start_date": "2023", "end_date": "2024", "rank": "副处", "note": ""},
    {"person_id": 2, "org_id": 16, "title": "长春市绿园区人民政府副区长", "start_date": "", "end_date": "2023", "rank": "副处", "note": ""},
    {"person_id": 2, "org_id": 12, "title": "长春市发改委服务业发展办公室主任", "start_date": "", "end_date": "", "rank": "正处", "note": ""},
    {"person_id": 2, "org_id": 12, "title": "长春市发改委高技术产业发展处处长", "start_date": "", "end_date": "", "rank": "正处", "note": ""},
    {"person_id": 2, "org_id": 12, "title": "长春市发改委重大项目谋划处处长", "start_date": "", "end_date": "", "rank": "正处", "note": ""},
    # 牟兆彬
    {"person_id": 10, "org_id": 2, "title": "市委常委、常务副市长", "start_date": "", "end_date": "present", "rank": "副处", "note": ""},
    {"person_id": 10, "org_id": 10, "title": "吉林长春国家农业高新技术产业示范区管委会副主任", "start_date": "", "end_date": "present", "rank": "副处", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副处", "note": ""},
    # 副市长
    {"person_id": 3, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副处", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副市长、市公安局局长", "start_date": "", "end_date": "present", "rank": "副处", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副处", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副处", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "市委常委、副市长", "start_date": "", "end_date": "present", "rank": "副处", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副处", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副处", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副处", "note": ""},
    # 组织部长
    {"person_id": 11, "org_id": 3, "title": "市委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "副处", "note": ""},
    # 人大 / 政协
    {"person_id": 30, "org_id": 8, "title": "市人大常委会党组书记、主任", "start_date": "", "end_date": "present", "rank": "正处", "note": ""},
    {"person_id": 40, "org_id": 9, "title": "市政协党组书记、主席", "start_date": "", "end_date": "present", "rank": "正处", "note": ""},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "市委书记—市长搭档(现任班子)", "overlap_org": "公主岭市", "overlap_period": "2023-至今"},
    {"person_a": 1, "person_b": 10, "type": "共事", "context": "书记—常务副市长(牟兆彬)", "overlap_org": "中共公主岭市委", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "共事", "context": "书记—市委常委(范庆庆)", "overlap_org": "中共公主岭市委", "overlap_period": ""},
    {"person_a": 1, "person_b": 11, "type": "共事", "context": "书记—组织部长(孙昊)", "overlap_org": "中共公主岭市委", "overlap_period": ""},
    {"person_a": 1, "person_b": 30, "type": "共事", "context": "书记—人大主任(孙胜军)", "overlap_org": "公主岭市", "overlap_period": ""},
    {"person_a": 1, "person_b": 40, "type": "共事", "context": "书记—政协主席(董华)", "overlap_org": "公主岭市", "overlap_period": ""},
    {"person_a": 2, "person_b": 10, "type": "共事", "context": "市长—常务副市长(牟兆彬)", "overlap_org": "公主岭市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 7, "type": "共事", "context": "市长—副市长(范庆庆)", "overlap_org": "公主岭市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 30, "type": "共事", "context": "市长—人大主任", "overlap_org": "公主岭市", "overlap_period": ""},
    {"person_a": 2, "person_b": 40, "type": "共事", "context": "市长—政协主席", "overlap_org": "公主岭市", "overlap_period": ""},
    # 市委班子内部(常委)
    {"person_a": 10, "person_b": 7, "type": "同僚", "context": "市委常委同僚(常务副市长—副市长)", "overlap_org": "中共公主岭市委", "overlap_period": ""},
    {"person_a": 10, "person_b": 11, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共公主岭市委", "overlap_period": ""},
    {"person_a": 7, "person_b": 11, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共公主岭市委", "overlap_period": ""},
    # 前任交接
    {"person_a": 1, "person_b": 2, "type": "交接", "context": "前任市长(赵师骐就地晋升书记)→现任市长(王贺军)", "overlap_org": "公主岭市人民政府", "overlap_period": "2023"},
    # 跨市交流
    {"person_a": 1, "person_b": 2, "type": "跨市交流", "context": "赵师骐(长春市直/双阳区)与王贺军(绿园区)先后调公主岭，长春市直区干部跨市厅制交流", "overlap_org": "长春市", "overlap_period": "2021-2024"},
    {"person_a": 1, "person_b": 10, "type": "跨县交流", "context": "牟兆彬(榆树/德惠)自长春市辖县调公主岭，县市委班子异地任职", "overlap_org": "长春市", "overlap_period": ""},
]


def _get_open_questions(person: dict) -> list[str]:
    questions = []
    if not person.get("birth"):
        questions.append("出生年月未确认")
    if not person.get("birthplace"):
        questions.append("籍贯未确认")
    if not person.get("education"):
        questions.append("学历教育背景未确认")
    if not person.get("work_start"):
        questions.append("参加工作年份未确认")
    return questions


def write_person_json(person: dict) -> None:
    """Write a per-person graph JSON file following the person_graph_json.md schema."""
    pid = person["id"]
    name = person["name"]
    slug_id = f"gongzhuling_{name}"

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
            "source_ids": ["S001"],
        })

    person_rels = [r for r in relationships if r["person_a"] == pid or r["person_b"] == pid]
    rels_output = []
    for r in person_rels:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id), None)
        other_name = other["name"] if other else f"person_{other_id}"
        rels_output.append({
            "person": other_name,
            "person_id": f"gongzhuling_{other_name}",
            "relationship_type": "overlap" if r["type"] in ("共事", "同僚", "跨市交流", "跨县交流") else "predecessor_successor",
            "strength": "strong" if r["type"] in ("共事", "跨市交流") else ("medium" if r["type"] in ("同僚", "交接", "跨县交流") else "weak"),
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001"],
        })

    sources = [{
        "id": "S001",
        "title": "公主岭市人民政府领导简介（官方）",
        "url": person.get("source", "") or "http://www.gongzhuling.gov.cn/szf/zfld/",
        "publisher": "公主岭市人民政府",
        "published_at": "",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high" if person.get("confidence") == "confirmed" else "medium",
        "notes": "官方县级政府网领导简介页面 + 领导活动/重要会议归档；前任及部分常委履历基于活动归档推断",
    }]

    is_core = pid in {1, 2}
    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "吉林省", "city": "长春市", "region": "公主岭市",
            "job": person.get("current_post", ""),
            "task_id": "jilin_公主岭市", "time_focus": "2026年8月",
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
            "education": [{"period": "", "institution": "", "major": "", "degree": person.get("education", ""), "study_type": "unknown"}],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{person.get('birth','')}",
                "name_birthplace": f"{name}_{person.get('birthplace','')}",
                "official_profile_url": person.get("source", ""),
            },
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "正处" if pid in {1, 2, 30, 40} else "副处",
            "as_of": AS_OF,
            "is_current_confirmed": person.get("confidence") == "confirmed",
            "source_ids": ["S001"],
        },
        "career_timeline": career_timeline,
        "organizations": [{"id": o["id"], "name": o["name"], "type": o["type"]} for o in organizations],
        "relationships": rels_output,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "cross_county_rotation" if pid in {1, 2, 10} else ("local_ladder" if pid in {3, 5} else "cross_county_rotation"),
            "systems_experience": [],
            "geographic_pattern": ["公主岭市", "长春市"],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{
            "type": "none_found",
            "description": "未在公开官方页面发现针对赵师骐/王贺军等现任领导的违纪线索；未检索到公开纪律处分或负面报道。搜索受限于官方档案（外部检索引擎受限）。",
            "date": "",
            "confidence": "plausible",
            "source_ids": ["S001"],
        }],
        "source_register": sources,
        "confidence_summary": {
            "identity": "confirmed" if person.get("birth") else "unverified",
            "current_role": person.get("confidence", "unverified"),
            "career_completeness": "partial" if is_core else "thin",
            "relationship_confidence": "medium" if is_core else "low",
            "biggest_gap": "核心人物部分职务起止时间未公开标注（官网仅列现任与前职摘要）；部分常委会副职（纪检/政法/宣传）身份及前任书记去向待查",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的完整任职履历（每段职务起止时间）",
                "why_it_matters": "关系网络时间线需要的精确起止信息",
                "suggested_queries": [f"{name} 简历", f"{name} 任前公示", f"{name} 任职经历"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": "前任市委书记（赵师骐之前任）的去向与完整履历",
                "why_it_matters": "前任领导交接与跨区网络分析",
                "suggested_queries": ["公主岭 前任 市委书记 去向", "公主岭 市委书记 张维亮", "公主岭 市委书记 闫旭"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": "公城市委班中纪委书记/政法委书记/宣传部长等余下常委部门负责人身份",
                "why_it_matters": "全国县市委班子图谱完整度",
                "suggested_queries": ["公主岭 纪委书记", "公主岭 政法委书记", "公主岭 宣传部长"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "medium",
                "question": "公主岭市跨县域干部交流的完整模式",
                "why_it_matters": "县域班子整体调任（长春市属）的人事关系图谱",
                "suggested_queries": ["公主岭 长春 县市干部 交流", "公主岭 榆树 德惠 干部交流"],
                "last_attempted": AS_OF,
            },
        ],
    }

    job_for_name = person.get("current_post", "").split("、")[0]
    fname = f"{TODAY}-吉林省-长春市-{job_for_name}-{name}.json"
    fpath = PJSON_DIR / fname
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fpath.name}")


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
    core_ids = {1, 2, 10, 30, 40}
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())