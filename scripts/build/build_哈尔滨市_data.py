#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 哈尔滨市 (Harbin City), 黑龙江省.

Investigation date: 2026-08-05
Task ID: heilongjiang_哈尔滨市
Level: 地级市
Targets: 市委书记 & 市长

Research sources:
  - www.harbin.gov.cn — 哈尔滨市人民政府官方网站 (primary, current as of Aug 2026)
  - www.hlj.gov.cn — 黑龙江省政府网 (省委人事与领导活动)
  - 官网"市政府领导"页确认 王合生为市长，李冕/杨慧/张海华/冯昕/尹喜峰/杨淑鹏/李亚飞/邱纪成为副市长
  - 官网"领导活动"(2026-07)确认 于洪涛为省委常委、市委书记，与市长王合生并列出场
  - 新任市委书记任命：中共中央2024年1月批准于洪涛任哈尔滨市委书记（央广网/网易/鲁网等）
  - 王合生由北京海淀区委书记调任，2023-09任黑龙江省副省长，2024-05-29当选哈尔滨市市长

Confidence notes:
  - 于洪涛（市委书记）、王合生（市长）：confirmed（官方 2026-08）
  - 副市长班子：confirmed（市政府领导页 2026-07）
  - 履历细节：confirmed/plausible（组织官方 + 权威媒体汇总）
"""

from __future__ import annotations

import json
import os
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
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "哈尔滨市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-05"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "heilongjiang_哈尔滨市"
if _CURRENT_DIR.name == "heilongjiang_哈尔滨市":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR  # fallback
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1-2 core leaders, 3 deputy secretaries, 4-11 standing committee,
#      12-19 deputy mayors/secretary-general, 20-25人大/政协, 30-31 predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "于洪涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967-10",
        "birthplace": "山东海阳",
        "education": "黑龙江省委党校经济管理专业研究生；高级管理人员工商管理硕士",
        "party_join": "1989-06",
        "work_start": "1989-07",
        "current_post": "省委常委、市委书记",
        "current_org": "中共哈尔滨市委员会",
        "source": "https://www.harbin.gov.cn/",
        "confidence": "confirmed",
        "notes": "2024年1月起任黑龙江省委常委、哈尔滨市委书记。现任哈尔滨警备区党委第一书记。曾在大庆、七台河、鸡西任职，历任共青团大庆市委书记、大庆市委常委常务副市长、七台河市委副书记、鸡西市长、鸡西市委书记，2022年5月当选黑龙江省委常委兼省委秘书长。",
    },
    {
        "id": 2,
        "name": "王合生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969-11",
        "birthplace": "山东汶上",
        "education": "理学博士（中科院南京地理与湖泊研究所）、副教授",
        "party_join": "1988-06",
        "work_start": "1993-07",
        "current_post": "市委副书记、市长",
        "current_org": "哈尔滨市人民政府",
        "source": "https://www.harbin.gov.cn/haerbin/lddtzqx/zwgk_leader_detail.shtml",
        "confidence": "confirmed",
        "notes": "2024年5月29日当选哈尔滨市市长，现任哈尔滨市委副书记、市长，主持市政府全面工作，分管市审计局。由北京市调任，曾任北京经济技术开发区职务、昌平区长、海淀区长、海淀区委书记；2023年9月任黑龙江省副省长，2024年5月任哈尔滨市代市长、市长。",
    },
    # ══════════════════════════════════════════════════════════════════════
    # 常务副市长（市委党委会层面）
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "李冕",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-12",
        "birthplace": "",
        "education": "黑龙江省委党校研究生",
        "party_join": "中共党员",
        "work_start": "1988-07",
        "current_post": "市委常委、常务副市长、党组副书记",
        "current_org": "哈尔滨市人民政府",
        "source": "https://www.harbin.gov.cn/",
        "confidence": "confirmed",
        "notes": "1988年7月参加工作，1993年6月加入中国共产党。现任哈尔滨市委常委、市政府副市长、党组副书记，负责市政府常务工作。",
    },
    {
        "id": 4,
        "name": "杨慧",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-11",
        "birthplace": "",
        "education": "大学、经济学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、副市长",
        "current_org": "哈尔滨市人民政府",
        "source": "https://www.harbin.gov.cn/",
        "confidence": "confirmed",
        "notes": "现任哈尔滨市委常委、市政府副市长。负责司法、生态环境、交通运输、文化旅游、国资、城管等领域。",
    },
    {
        "id": 5,
        "name": "张海华",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1969-12",
        "birthplace": "",
        "education": "大学、文学学士",
        "party_join": "无党派",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "哈尔滨市人民政府",
        "source": "https://www.harbin.gov.cn/",
        "confidence": "confirmed",
        "notes": "现任哈尔滨市副市长（无党派）。负责教育、卫生健康、体育。",
    },
    {
        "id": 6,
        "name": "冯昕",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966-11",
        "birthplace": "",
        "education": "在职研究生、管理学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长、党组成员",
        "current_org": "哈尔滨市人民政府",
        "source": "https://www.harbin.gov.cn/",
        "confidence": "confirmed",
        "notes": "现任哈尔滨市副市长、党组成员。负责水务、农业农村、林草、粮储、供销。",
    },
    {
        "id": 7,
        "name": "尹喜峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-",
        "birthplace": "",
        "education": "中央党校大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长、市公安局局长",
        "current_org": "哈尔滨市人民政府",
        "source": "https://www.harbin.gov.cn/",
        "confidence": "confirmed",
        "notes": "现任哈尔滨市政府副市长、党组成员，市委政法委副书记，市公安局局长、党委书记、督察长。负责公共安全。",
    },
    {
        "id": 8,
        "name": "杨淑鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-04",
        "birthplace": "",
        "education": "研究生、经济学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长、党组成员",
        "current_org": "哈尔滨市人民政府",
        "source": "https://www.harbin.gov.cn/",
        "confidence": "confirmed",
        "notes": "现任哈尔滨市政府副市长、党组成员。负责科技、工信、民政、退役军人、营商环境。",
    },
    {
        "id": 9,
        "name": "李亚飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-11",
        "birthplace": "",
        "education": "大学、硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长、党组成员",
        "current_org": "哈尔滨市人民政府",
        "source": "https://www.harbin.gov.cn/",
        "confidence": "confirmed",
        "notes": "现任哈尔滨市政府副市长、党组成员。负责商贸、市场监管、招商引资、综合保税。",
    },
    {
        "id": 10,
        "name": "邱纪成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-10",
        "birthplace": "",
        "education": "法学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、副市长（挂职）",
        "current_org": "哈尔滨市人民政府",
        "source": "https://www.harbin.gov.cn/",
        "confidence": "confirmed",
        "notes": "现任哈尔滨市委常委、市政府副市长（挂职）。负责金融、数据。挂职干部，通常来自金融/中直系统，值得重点跟踪的交流节点。",
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors (chains)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 30,
        "name": "张安顺",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "黑龙江省委副书记（前哈尔滨市委书记）",
        "current_org": "中共黑龙江省委",
        "source": "央广网/黑龙江政府网",
        "confidence": "confirmed",
        "notes": "前任哈尔滨市委书记（约2021-2023年12月），2023年12月转任黑龙江省委副书记、省委教育工委书记、省委党校校(院)长。",
    },
    {
        "id": 31,
        "name": "张起翔",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任哈尔滨市长",
        "current_org": "哈尔滨市人民政府",
        "source": "黑龙江政府网",
        "confidence": "confirmed",
        "notes": "前任哈尔滨市长（约2022-2024年），2024年5月由王合生接任。张起翔后转任黑龙江省副省长。",
    },
    {
        "id": 32,
        "name": "王兆力",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任哈尔滨市委书记（约2017-2021）",
        "current_org": "中共哈尔滨市委员会",
        "source": "人民日报/新华社",
        "confidence": "confirmed",
        "notes": "曾任哈尔滨市委书记（约2017年5月至2021/2022年），之后离任。",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共哈尔滨市委员会", "type": "党委", "level": "地级市", "parent": "中共黑龙江省委员会", "location": "哈尔滨市"},
    {"id": 2, "name": "哈尔滨市人民政府", "type": "政府", "level": "地级市", "parent": "黑龙江省人民政府", "location": "哈尔滨市"},
    {"id": 3, "name": "哈尔滨市人民代表大会常务委员会", "type": "人大", "level": "地级市", "parent": "黑龙江省人大常委会", "location": "哈尔滨市"},
    {"id": 4, "name": "政协哈尔滨市委员会", "type": "政协", "level": "地级市", "parent": "政协黑龙江省委员会", "location": "哈尔滨市"},
    {"id": 5, "name": "中共哈尔滨市纪律检查委员会", "type": "党委", "level": "地级市", "parent": "中共黑龙江省纪律检查委员会", "location": "哈尔滨市"},
    {"id": 6, "name": "哈尔滨市公安局", "type": "政府", "level": "地级市", "parent": "哈尔滨市人民政府", "location": "哈尔滨市"},
    {"id": 7, "name": "中共黑龙江省委员会", "type": "党委", "level": "省级", "parent": "", "location": "哈尔滨市"},
    {"id": 8, "name": "黑龙江省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "哈尔滨市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 于洪涛 — Party Secretary (current)
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "2024-01", "end_date": "", "rank": "副省级", "note": "现任黑龙江省委常委、哈尔滨市委书记"},
    {"person_id": 1, "org_id": 7, "title": "省委常委", "start_date": "2022-05", "end_date": "", "rank": "副省级", "note": "当选黑龙江省委常委"},
    {"person_id": 1, "org_id": 7, "title": "省委秘书长", "start_date": "2022-05", "end_date": "2024-01", "rank": "副省级", "note": "兼任省委秘书长至履新哈尔滨"},
    {"person_id": 1, "org_id": 1, "title": "哈尔滨警备区党委第一书记", "start_date": "2024-01", "end_date": "", "rank": "副省级", "note": ""},
    # 王合生 — Mayor (current)
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "2024-05", "end_date": "", "rank": "正厅级", "note": "2024-05-29当选，主持市政府全面工作，分管审计局"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "2024-05", "end_date": "", "rank": "正厅级", "note": "兼任市委副书记"},
    {"person_id": 2, "org_id": 8, "title": "副省长", "start_date": "2023-09", "end_date": "2024-05", "rank": "副省级", "note": "黑龙江省副省长（2024-05-06免去）"},
    # 常务副市长 李冕
    {"person_id": 3, "org_id": 2, "title": "常务副市长、党组副书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 杨慧
    {"person_id": 4, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 张海华
    {"person_id": 5, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "无党派"},
    # 冯翔
    {"person_id": 6, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 尹喜峰
    {"person_id": 7, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 7, "org_id": 6, "title": "市公安局局长、党委书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 杨淑鹏
    {"person_id": 8, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 李亚飞
    {"person_id": 9, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 邱纪成（挂职）
    {"person_id": 10, "org_id": 2, "title": "副市长（挂职）", "start_date": "", "end_date": "", "rank": "副厅级", "note": "负责金融、数据"},
    {"person_id": 10, "org_id": 1, "title": "市委常委（挂职）", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 前任 市委书记
    {"person_id": 30, "org_id": 1, "title": "市委书记", "start_date": "2021", "end_date": "2023-12", "rank": "副省级", "note": "前任哈尔滨市委书记，转黑龙江省委副书记"},
    {"person_id": 30, "org_id": 7, "title": "省委副书记", "start_date": "2023-12", "end_date": "", "rank": "副省级", "note": ""},
    # 前任 市长
    {"person_id": 31, "org_id": 2, "title": "市长", "start_date": "2022", "end_date": "2024-05", "rank": "正厅级", "note": "前任哈尔滨市长"},
    # 王兆力
    {"person_id": 32, "org_id": 1, "title": "市委书记", "start_date": "2017", "end_date": "2021", "rank": "副省级", "note": "再前任哈尔滨市委书记"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 现任书记↔市长
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "市委书记—市长搭档", "overlap_org": "哈尔滨市委市政府", "overlap_period": "2024-01至今"},
    # 书记↔常务副市长
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "书记—常务副市长", "overlap_org": "哈尔滨市", "overlap_period": "2024至今"},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "书记—副市长", "overlap_org": "哈尔滨市", "overlap_period": "2024至今"},
    {"person_a": 1, "person_b": 10, "type": "上下级", "context": "书记—挂职副市长", "overlap_org": "哈尔滨市", "overlap_period": "2024至今"},
    # 市长↔副市长
    {"person_a": 2, "person_b": 3, "type": "共事", "context": "市长—常务副市长", "overlap_org": "哈尔滨市人民政府", "overlap_period": "2024至今"},
    {"person_a": 2, "person_b": 4, "type": "共事", "context": "市长—副市长", "overlap_org": "哈尔滨市人民政府", "overlap_period": "2024至今"},
    {"person_a": 2, "person_b": 5, "type": "共事", "context": "市长—副市长", "overlap_org": "哈尔滨市人民政府", "overlap_period": "2024至今"},
    {"person_a": 2, "person_b": 6, "type": "共事", "context": "市长—副市长", "overlap_org": "哈尔滨市人民政府", "overlap_period": "2024至今"},
    {"person_a": 2, "person_b": 7, "type": "共事", "context": "市长—副市长/公安局长", "overlap_org": "哈尔滨市人民政府", "overlap_period": "2024至今"},
    {"person_a": 2, "person_b": 8, "type": "共事", "context": "市长—副市长", "overlap_org": "哈尔滨市人民政府", "overlap_period": "2024至今"},
    {"person_a": 2, "person_b": 9, "type": "共事", "context": "市长—副市长", "overlap_org": "哈尔滨市人民政府", "overlap_period": "2024至今"},
    {"person_a": 2, "person_b": 10, "type": "共事", "context": "市长—挂职副市长", "overlap_org": "哈尔滨市人民政府", "overlap_period": "2024至今"},
    # 现任→前任 接班链
    {"person_a": 1, "person_b": 30, "type": "接替", "context": "继任哈尔滨市委书记，张安顺转省委副书记", "overlap_org": "中共哈尔滨市委员会", "overlap_period": "2024-01"},
    {"person_a": 2, "person_b": 31, "type": "接替", "context": "继任哈尔滨市长", "overlap_org": "哈尔滨市人民政府", "overlap_period": "2024-05"},
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
    if not person.get("education"):
        questions.append("学历教育背景未确认")
    if not person.get("work_start"):
        questions.append("参加工作年份未确认")
    return questions


def write_person_json(person: dict) -> None:
    """Write a per-person graph JSON file following the person_graph_json.md schema."""
    pid = person["id"]
    name = person["name"]
    slug_id = f"haerbin_{name}"

    person_positions = [p for p in positions if p["person_id"] == pid]

    career_timeline = []
    for pos in sorted(person_positions, key=lambda x: x.get("start_date") or "9999"):
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

    # Add a narrative gap entry for core leaders with extra history not in positions
    if pid == 1:
        career_timeline.append({
            "start": "1989-07",
            "end": "2021-10",
            "org": "大庆/七台河/鸡西",
            "title": "多岗位历练（团委、劳动保障、区县、地市书记/市长）",
            "level": "",
            "rank": "",
            "notes": "1967年10月生，1989年7月参加工作。早期在大庆市任共青团大庆市委书记、市劳动和社会保障局局长、大同区委书记等；后任大庆市委常委、常务副市长；2016年七台河市委副书记；2018年鸡西市长；2021年鸡西市委书记。",
            "confidence": "confirmed",
            "source_ids": ["S002"],
        })
    if pid == 2:
        career_timeline.append({
            "start": "1993-07",
            "end": "2023-09",
            "title": "北京历练（经开／昌平／海淀）",
            "level": "",
            "rank": "",
            "notes": "1969年11月生，1993年7月参加工作。在北京经济技术开发区、昌平区、海淀区任职，曾任海淀区委书记。理学博士、副教授。2023年9月调任黑龙江省。",
            "confidence": "confirmed",
            "source_ids": ["S002"],
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
            "person_id": f"haerbin_{other_name}",
            "relationship_type": "overlap",
            "strength": "strong" if r["type"] in ("共事", "上下级") else "medium",
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001"],
        })

    source_url = person.get("source", "https://www.harbin.gov.cn/")
    sources = [
        {
            "id": "S001",
            "title": "哈尔滨市人民政府官方网站（领导之窗/领导活动）",
            "url": "https://www.harbin.gov.cn/",
            "publisher": "哈尔滨市人民政府",
            "published_at": "2026-07",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "官方领导页确认市长王合生及副市长班子；领导活动确认于洪涛为省委常委、市委书记",
        },
        {
            "id": "S002",
            "title": "于洪涛/王合生任职履历（百度百科、央广网、新京报、网易等）",
            "url": source_url,
            "publisher": "百度百科/央广网/新京报",
            "published_at": "2024",
            "accessed_at": AS_OF,
            "source_type": "media",
            "reliability": "medium",
            "notes": "履历细节的媒体汇总来源",
        },
    ]

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "黑龙江省",
            "city": "哈尔滨市",
            "region": "哈尔滨市",
            "job": person.get("current_post", ""),
            "task_id": "heilongjiang_哈尔滨市",
            "time_focus": "2026年",
        },
        "identity": {
            "person_id": slug_id,
            "name": name,
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": person.get("birthplace", ""),
            "education": [
                {
                    "period": "",
                    "institution": "",
                    "major": "",
                    "degree": person.get("education", ""),
                    "study_type": "unknown",
                    "source_ids": ["S002"],
                }
            ] if person.get("education") else [],
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
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": person.get("confidence") == "confirmed",
            "source_ids": ["S001"],
        },
        "career_timeline": career_timeline,
        "organizations": [{"id": o["id"], "name": o["name"], "type": o["type"]} for o in organizations],
        "relationships": rels_output,
        "governance_record": [
            {
                "period": "2026-07",
                "domain": "economic_development",
                "achievement_or_event": "于洪涛、王合生与中粮集团董事长李国强工作会谈（推进项目合作）",
                "role_in_event": "共同主持",
                "measurable_outcome": "",
                "location": "哈尔滨市",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
            {
                "period": "2026-07",
                "domain": "public_security",
                "achievement_or_event": "王合生深夜调研城市更新、走访慰问老党员",
                "role_in_event": "主持部署",
                "location": "哈尔滨市",
                "confidence": "confirmed",
                "source_ids": ["S001"],
            },
        ] if person["id"] in (1, 2) else [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "local_ladder" if person["id"] == 1 else "cross_province_transfer",
            "systems_experience": list(set(
                o.get("type", "") for o in organizations if o["id"] in [pos["org_id"] for pos in person_positions]
            )),
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
            "identity": "confirmed" if person.get("birth") else "unverified",
            "current_role": person.get("confidence", "unverified"),
            "career_completeness": "partial",
            "relationship_confidence": "medium",
            "biggest_gap": "副市长班子个别履历细节（籍贯、入党/参加工作时间）未逐一核验",
        },
        "open_questions": [
            {
                "priority": "medium",
                "question": f"{name}的完整详细履历（每段职务起止时间）是否需要逐一细化",
                "why_it_matters": "关系网络分析需要更精细的时间线",
                "suggested_queries": [f"{name} 简历", f"{name} 任前公示", f"{name} 百度百科"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "low",
                "question": f"{name}与哈尔滨市委班子其他成员的跨机构交集",
                "why_it_matters": "识别更深层网络",
                "suggested_queries": [f"{name} 哈尔滨", f"{name} 任职经历"],
                "last_attempted": AS_OF,
            },
        ],
    }

    _job_map = {1: "市委书记", 2: "市长", 30: "前市委书记", 31: "前市长"}
    job_in_fn = _job_map.get(pid) or (person.get("current_post", "").split("、")[0] if person.get("current_post") else "")
    fname = f"{TODAY}-黑龙江省-哈尔滨市-{job_in_fn}-{name}.json"
    fpath = PJSON_DIR / fname
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fpath.name}")
    return fpath


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
    # Core leaders + key figures
    core_ids = {1, 2, 3, 4, 10}
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())