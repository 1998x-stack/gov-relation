#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 站前区, 营口市, 辽宁省.

Investigation date: 2026-08-06
Task ID: liaoning_站前区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources (all accessed 2026-08-06):
  - www.ykzq.gov.cn — 站前区人民政府领导之窗 (official, primary — 区长/副区长班子成员简历)
  - www.yingkou.gov.cn — 营口市政府门户 + 营口市委组织部任前公示归档 (official — 前任与跨区调动)
  - 辽宁省管干部任前公示 (观八闽等转载) — 张杨拟任站前区委书记、王正刚拟任副市长
  - 站前区政府分工通知〔2026〕1号 (2026-05-14) — 区公安条线交接 (郭善琦→张彬)

Confidence notes:
  - 现任区委书记张杨、区长王石成 — confirmed (省管公示 + 区政府领导之窗)
  - 区政府领导之窗全名单 confirmed（1区长+7副区长）
  - 前任区委书记实王正刚→副市长 confirmed；前区长黄宇光调离去向待查
  - 部分区委常委（组织/宣传/纪委/政法/统战）及区政协现任主席在可达来源未完整确证
"""

from __future__ import annotations

import json
import os
import re
import sqlite3
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

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "站前区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "liaoning_站前区"
if _CURRENT_DIR.name == "liaoning_站前区":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ─────────────────────────────────────────────────────────────────
# IDs: 1=区委书记, 2=区长, 3=区委常委&常务副区长, 4-8=区委常委/副区长
#      9=区人大主任, 10=区政协主席, 11-17=前任/跨区
persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (现任)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "张杨",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1979-03",
        "birthplace": "",
        "education": "在职研究生学历，硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "站前区委书记",
        "current_org": "中共站前区委员会",
        "source": "https://www.yingkou.gov.cn/ (辽宁省管干部任前公示：张杨，女，1979.03，现任站前区委副书记、区长，拟任县（市、区）委书记；2026-07 十五次党代会当选)"
    },
    {
        "id": 2,
        "name": "王石成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-10",
        "birthplace": "",
        "education": "在职研究生学历，硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "站前区委副书记、区政府党组书记、区长",
        "current_org": "站前区人民政府",
        "source": "http://www.ykzq.gov.cn/ldzc/017001/017001001/leader.html"
    },
    {
        "id": 3,
        "name": "李禹霖",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985-02",
        "birthplace": "",
        "education": "在职研究生学历，硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "站前区委常委、区政府党组副书记、副区长（常务）",
        "current_org": "站前区人民政府",
        "source": "http://www.ykzq.gov.cn/ldzc/017002/017002001/leader.html"
    },
    {
        "id": 4,
        "name": "张彬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "站前区政府党组成员、副区长、区公安分局党组书记、局长",
        "current_org": "站前区人民政府 / 营口市公安局站前分局",
        "source": "http://www.ykzq.gov.cn/ldzc/017002/017002003/leader.html"
    },
    {
        "id": 5,
        "name": "李雪冬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984-12",
        "birthplace": "",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "站前区委常委、区政府党组成员、副区长",
        "current_org": "站前区人民政府",
        "source": "http://www.ykzq.gov.cn/ldzc/017002/017002007/leader.html"
    },
    {
        "id": 6,
        "name": "张哲",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1977-06",
        "birthplace": "",
        "education": "大学本科，学士学位",
        "party_join": "民进会员",
        "work_start": "",
        "current_post": "站前区政府副区长",
        "current_org": "站前区人民政府",
        "source": "http://www.ykzq.gov.cn/ldzc/017002/017002006/leader.html"
    },
    {
        "id": 7,
        "name": "马拓",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1977-09",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "站前区政府副区长",
        "current_org": "站前区人民政府",
        "source": "http://www.ykzq.gov.cn/ldzc/017002/017002005/leader.html"
    },
    {
        "id": 8,
        "name": "刘峥嵘",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-11",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "站前区政府副区长",
        "current_org": "站前区人民政府",
        "source": "http://www.ykzq.gov.cn/ldzc/017002/017002004/leader.html"
    },
    {
        "id": 9,
        "name": "贾楠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983-11",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "站前区政府副区长（苏辽对口合作）",
        "current_org": "站前区人民政府",
        "source": "http://www.ykzq.gov.cn/ldzc/017002/017002002/leader.html"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 区人大 / 政协
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 10,
        "name": "董恩思",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "站前区人大常委会主任（区委常委、常务副区长升任）",
        "current_org": "站前区人大常委会",
        "source": "https://www.yingkou.gov.cn/ 人事任免公示（2025-10-24：现任站前区委常委、区政府党组副书记、副区长，拟提名为县（市）区人大常委会主任候选人）"
    },
    {
        "id": 11,
        "name": "韩跃",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "站前区政协主席",
        "current_org": "政协站前区委员会",
        "source": "https://www.yingkou.gov.cn/ （2021 年政协署名报道）"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 前任 / 跨区 (网络节点)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 12,
        "name": "王正刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-01",
        "birthplace": "",
        "education": "中央党校大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "营口市副市长（前任站前区委书记）",
        "current_org": "营口市人民政府",
        "source": "https://www.yingkou.gov.cn/zfxxgk/ 领导之窗 + 省管干部任免公示：现任营口市站前区委书记、一级调研员，拟提名为地级市副市长人选"
    },
    {
        "id": 13,
        "name": "黄宇光",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "https://www.yingkou.gov.cn/ 2024-01 报道（时任站前区区长）；2026-04-01 市人大常委会公告（站前区选出的代表黄宇光、马震调离营口行政区）"
    },
    {
        "id": 14,
        "name": "高洪涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "https://www.yingkou.gov.cn/ 2015-2017 党课报道（时任站前区委书记）；2020 人大文件接受高洪涛辞职"
    },
    {
        "id": 15,
        "name": "李宏振",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "https://www.yingkou.gov.cn/ 2020-2021 疫情慰问、招商报道（时任站前区委书记）"
    },
    # 跨区调入调出线索（营口市委组织部任前公示）
    {
        "id": 16,
        "name": "郭善琦",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "http://www.ykzq.gov.cn/govxxgk/zqqrmzf/2026-05-14/a43d2005-3969-4306-a3d6-f87be1263ef4.html （分工通知〔2026〕1号：郭善琦分管公安/司法→2026 后被张彬接任）"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共站前区委员会", "type": "party_committee", "level": "县处级", "parent": "中共营口市委", "location": "站前区"},
    {"id": 2, "name": "站前区人民政府", "type": "government", "level": "县处级", "parent": "营口市人民政府", "location": "站前区"},
    {"id": 3, "name": "站前区人大常委会", "type": "npc", "level": "县处级", "parent": "", "location": "站前区"},
    {"id": 4, "name": "政协站前区委员会", "type": "cppcc", "level": "县处级", "parent": "", "location": "站前区"},
    {"id": 5, "name": "站前区纪委监委", "type": "discipline", "level": "县处级", "parent": "营口市纪委监委", "location": "站前区"},
    {"id": 6, "name": "营口市公安局站前分局", "type": "government", "level": "乡科级", "parent": "营口市公安局", "location": "站前区"},
    {"id": 7, "name": "营口市人民政府", "type": "government", "level": "地厅级", "parent": "辽宁省人民政府", "location": "营口市"},
    {"id": 8, "name": "中共营口市委", "type": "party_committee", "level": "地厅级", "parent": "中共辽宁省委", "location": "营口市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 张杨 (区委书记，前区长)
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "2026", "end_date": "present", "rank": "正处级", "note": "2026-07-24 十五次党代会当选"},
    {"person_id": 1, "org_id": 2, "title": "区长（曾任）", "start_date": "", "end_date": "2026", "rank": "正处级", "note": "由区委副书记、区长转任区委书记"},
    {"person_id": 1, "org_id": 1, "title": "区委副书记（曾任）", "start_date": "", "end_date": "2026", "rank": "副处级", "note": ""},
    # 王石成 (区长)
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "2026-03", "end_date": "present", "rank": "正处级", "note": "2026-03 代理区长，后转正；主持区政令全面工作"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "2026", "end_date": "present", "rank": "副处级", "note": ""},
    # 李禹霖 (常务副区长)
    {"person_id": 3, "org_id": 2, "title": "常务副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "负责发改、财税、应急等"},
    {"person_id": 3, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 张彬 (公安局长)
    {"person_id": 4, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管公安、司法"},
    {"person_id": 4, "org_id": 6, "title": "局长", "start_date": "", "end_date": "present", "rank": "正科级", "note": "兼任区公安分局党组书记、局长"},
    # 李雪冬
    {"person_id": 5, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "负责营商环境、数据、商务、市场监管等"},
    {"person_id": 5, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 张哲 (民进)
    {"person_id": 6, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管教育、科技、卫生健康"},
    # 马拓
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管农业、民政、退役军人"},
    # 刘峥嵘
    {"person_id": 8, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管工信、住建、生态"},
    # 贾楠
    {"person_id": 9, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "苏辽对口合作"},
    # 人大 / 政协
    {"person_id": 10, "org_id": 3, "title": "主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": "区人大常委会主任（2025-10 拟任）"},
    {"person_id": 11, "org_id": 4, "title": "主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 前任 / 跨区
    {"person_id": 12, "org_id": 7, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "前任站前区委书记升任"},
    {"person_id": 12, "org_id": 1, "title": "区委书记（前任）", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "区长（前任）", "start_date": "", "end_date": "", "rank": "正处级", "note": "2024 在任，2026 前调离"},
    {"person_id": 14, "org_id": 1, "title": "区委书记（更早）", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 15, "org_id": 1, "title": "区委书记（更早）", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 现任核心（区委—政府）
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "区委书记—区长", "overlap_org": "中共站前区委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "区委书记—常务副区长（常委）", "overlap_org": "中共站前区委员会", "overlap_period": ""},
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "区长—常务副区长", "overlap_org": "站前区人民政府", "overlap_period": ""},
    # 政府班子
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "区长—副区长（公安局长）", "overlap_org": "站前区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "区长—副区长", "overlap_org": "站前区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "区长—副区长", "overlap_org": "站前区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "区长—副区长", "overlap_org": "站前区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "区长—副区长", "overlap_org": "站前区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "区长—副区长", "overlap_org": "站前区人民政府", "overlap_period": ""},
    {"person_a": 3, "person_b": 5, "type": "overlap", "context": "常务副区长—副区长（同为区委常委）", "overlap_org": "中共站前区委员会", "overlap_period": ""},
    # 人大 / 政协
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "区委书记—人大常委会主任", "overlap_org": "站前区", "overlap_period": ""},
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "区委书记—政协主席", "overlap_org": "站前区", "overlap_period": ""},
    # 区委书记继任链
    {"person_a": 14, "person_b": 15, "type": "predecessor_successor", "context": "区委书记继任", "overlap_org": "中共站前区委员会", "overlap_period": ""},
    {"person_a": 15, "person_b": 12, "type": "predecessor_successor", "context": "区委书记继任", "overlap_org": "中共站前区委员会", "overlap_period": ""},
    {"person_a": 12, "person_b": 1, "type": "predecessor_successor", "context": "前任区委书记(王正刚升任副市长)—现任区委书记(张杨)", "overlap_org": "中共站前区委员会", "overlap_period": "2026"},
    # 区长继任
    {"person_a": 13, "person_b": 1, "type": "predecessor_successor", "context": "前区长(黄宇光)—曾任区长转任书记(张杨)", "overlap_org": "站前区人民政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor", "context": "张杨由区长转任区委书记，王石成接任区长", "overlap_org": "站前区人民政府", "overlap_period": "2026-03"},
    # 公安条线交接
    {"person_a": 16, "person_b": 4, "type": "predecessor_successor", "context": "公安分局负责人交接（郭善琦→张彬）", "overlap_org": "营口市公安局站前分局", "overlap_period": "2026"},
]

# ── Person JSON(s) ────────────────────────────────────────────────────────────
def _write_person_json(person: dict, out_dir: Path) -> None:
    """Write a person graph JSON for the person."""
    job_tag = person["current_post"] or person["name"]
    raw_name = f"{TODAY}-辽宁省-营口市-{job_tag}-{person['name']}.json"
    safe_name = re.sub(r"[^\u4e00-\u9fff\w\-. ]", "_", raw_name)
    filepath = out_dir / safe_name

    pjson = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "辽宁省",
            "city": "营口市",
            "region": "站前区",
            "job": person["current_post"],
            "task_id": "liaoning_站前区",
            "time_focus": AS_OF,
        },
        "identity": {
            "person_id": f"zhanqian_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person["gender"],
            "ethnicity": person["ethnicity"],
            "birth": person["birth"],
            "birthplace": person["birthplace"],
            "native_place": "",
            "education": [{"period": "", "institution": "", "major": "", "degree": person["education"], "study_type": "unknown", "source_ids": []}],
            "party_join": person["party_join"],
            "work_start": person["work_start"],
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person['birth']}",
                "official_profile_url": person["source"],
            },
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": bool(person["source"]),
            "source_ids": [],
        },
        "career_timeline": [
            {
                "start": "",
                "end": "present" if person["current_post"] else "",
                "org": person["current_org"],
                "title": person["current_post"],
                "confidence": "confirmed" if person["source"] else "plausible",
                "source_ids": [],
            }
        ],
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {},
        "work_style_and_personality": {},
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "本轮调查未发现不良记录信号。", "confidence": "unverified"}],
        "source_register": [
            {"id": "S001", "title": "站前区政府领导之窗 / 营口党务公开（当前官员基本信息）", "url": person["source"], "publisher": "站前区人民政府 / 营口市人民政府", "source_type": "official", "reliability": "high"},
        ],
        "confidence_summary": {
            "identity": "partial" if not person["birth"] else "confirmed",
            "current_role": "confirmed" if person["current_post"] else "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": "完整履历（出生年月至今的全部职务变动）",
        },
        "open_questions": [
            {"priority": "high", "question": f"{person['name']}的完整工作履历", "why_it_matters": "了解晋升路径和人际网络", "suggested_queries": [f"{person['name']} 简历", f"{person['name']} 此前担任"], "last_attempted": TODAY}
        ],
    }
    filepath.write_text(json.dumps(pjson, ensure_ascii=False, indent=2), encoding="utf-8")
    return filepath


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"═══ Building {SLUG} network ═══")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Persons: {len(persons)}")
    print(f"  Orgs:   {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

    # Write person JSON files for the two core leaders and their deputy-level confirmed officials
    key_people = [
        {"id": 1, "name": "张杨", "current_post": "区委书记", "current_post_tag": "区委书记", "current_org": "中共站前区委员会", "gender": "女", "ethnicity": "汉族", "birth": "1979-03", "birthplace": "", "education": "在职研究生学历，硕士学位", "party_join": "中共党员", "work_start": "", "source": "https://www.yingkou.gov.cn/ （省管干部任免公示，2026-07 十五次党代会当选区委书记）"},
        {"id": 2, "name": "王石成", "current_post": "区委副书记、区政府区长", "current_post_tag": "区长", "current_org": "站前区人民政府", "gender": "男", "ethnicity": "汉族", "birth": "1978-10", "birthplace": "", "education": "在职研究生学历，硕士学位", "party_join": "中共党员", "work_start": "", "source": "http://www.ykzq.gov.cn/ldzc/017001/017001001/leader.html"},
        {"id": 3, "name": "李禹霖", "current_post": "区委常委、常务副区长", "current_post_tag": "常务副区长", "current_org": "站前区人民政府", "gender": "男", "ethnicity": "汉族", "birth": "1985-02", "birthplace": "", "education": "在职研究生学历，硕士学位", "party_join": "中共党员", "work_start": "", "source": "http://www.ykzq.gov.cn/ldzc/017002/017002001/leader.html"},
        {"id": 5, "name": "李雪冬", "current_post": "区委常委、副区长", "current_post_tag": "副区长", "current_org": "站前区人民政府", "gender": "男", "ethnicity": "汉族", "birth": "1984-12", "birthplace": "", "education": "在职研究生学历", "party_join": "中共党员", "work_start": "", "source": "http://www.ykzq.gov.cn/ldzc/017002/017002007/leader.html"},
    ]

    for kp in key_people:
        # 补全字段默认
        kp.setdefault("current_org", "")
        kp.setdefault("aliases", [])
        fpath = _write_person_json(kp, PJSON_DIR)
        print(f"  Person JSON: {fpath.name}")

    # Build DB + GEXF
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

    # Verify
    conn = sqlite3.connect(str(DB_PATH))
    cur = conn.execute("SELECT COUNT(*) FROM persons")
    p_count = cur.fetchone()[0]
    cur = conn.execute("SELECT COUNT(*) FROM organizations")
    o_count = cur.fetchone()[0]
    cur = conn.execute("SELECT COUNT(*) FROM positions")
    pos_count = cur.fetchone()[0]
    cur = conn.execute("SELECT COUNT(*) FROM relationships")
    r_count = cur.fetchone()[0]
    conn.close()

    print(f"\n  DB written: {DB_PATH.exists()}, size={DB_PATH.stat().st_size} bytes")
    print(f"    Persons: {p_count}, Orgs: {o_count}, Positions: {pos_count}, Relations: {r_count}")
    print(f"  GEXF written: {GEXF_PATH.exists()}, size={GEXF_PATH.stat().st_size} bytes")
    print(f"═══ Done ═══")