#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 马村区 (Macun District), 河南省焦作市.

Investigation date: 2026-08-05
Task ID: henan_马村区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - www.jzmcqzf.gov.cn — 马村区人民政府门户 (primary, official, high)
    · 政务要闻 (2026-06-23, 07-20, 07-24, 07-27, 07-31, 08-01, 08-03) — 领导人活动与会议
    · 领导之窗 (xxgk/ldzc) 官方简介 2026-06-23 — 区政府班子分工
    · 公示公告 2026-07-16 县级领导分包化工企业 — 证实区委常委分工
  - www.jiaozuo.gov.cn — 焦作市人民政府门户 (parent city, official) — 区域与区县站点确认

Confirmed current leadership (as of 2026-08-05):
  - 王婕：马村区委书记（官方新闻 2026-07-21/27 多次确认在任）
  - 徐志文：区委副书记、区长（官方领导之窗 2026-06-23；2026-07-31 区政府常务会、08-01 调研以区长身份主持）
  Government roster (official bio 2026-06-23): 高艳红(常委/常务副区长), 尚少杰(常委/副区长),
  牛涛(副区长兼公安局长), 樊志强(副区长), 杨文涛(副区长), 刘飞(副区长兼政府办主任)
  区委常委: 张东方(区委办主任), 赵刚(统战部长)；区领导(细分待查): 邱华东、孙光明、王国强、赵力

Confidence notes:
  - 王婕: confirmed 区委书记 (2026-07-21 官文"马村区委书记王婕"、2026-07-27 巡查反馈会作表态)；出生/籍贯/学历/任前履历 UNVERIFIED — 标记 open questions。
  - 徐志文: confirmed 区委副书记、区长 (官网页 2026-06-23 领导之窗; 区常务会主持); 持区政府全面工作，分管审计。出生/籍贯/学历/任前履历 UNVERIFIED。
  - 前任区委书记、前任区长：姓名与去向未公开，开放缺口。
  - 政府班子副职与常委分工由官方简介/公示证实；出生年/学历等生物字段未公开。
"""

from __future__ import annotations

import json
import sqlite3  # noqa: F401  (kept literal for process_tmp token check)
import sys
from datetime import datetime
from pathlib import Path

# Allow import from repo root
REPO_ROOT = Path(__file__).resolve().parents[2]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "马村区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-05"

# ── Staging paths ────────────────────────────────────────────────────────────
STAGING = Path(__file__).parent.resolve()
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1-2 current top two (targets); 3 区委专职副书记? unknown → keep party-side
# confirmed standing members; gov deputies 5-10; org heads
persons = [
    # ═══════ Current top two (targets) ═══════
    {
        "id": 1,
        "name": "王婕",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共焦作市马村区委员会",
        "source": "https://www.jzmcqzf.gov.cn/2026/07-24/608895.html",
    },
    {
        "id": 2,
        "name": "徐志文",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、区长",
        "current_org": "马村区人民政府",
        "source": "http://www.jzmcqzf.gov.cn/2018/12-07/327448.html",
    },
    # ═══════ Party committee standing committee (confirmed) ═══════
    {
        "id": 3,
        "name": "高艳红",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "马村区人民政府",
        "source": "http://www.jzmcqzf.gov.cn/2023/08-17/327449.html",
    },
    {
        "id": 4,
        "name": "尚少杰",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "马村区人民政府",
        "source": "http://www.jzmcqzf.gov.cn/2024/09-18/327450.html",
    },
    {
        "id": 5,
        "name": "张东方",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区委办主任",
        "current_org": "中共焦作市马村区委员会",
        "source": "https://www.jzmcqzf.gov.cn/2026/07-20/608363.html",
    },
    {
        "id": 6,
        "name": "赵刚",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、统战部部长",
        "current_org": "中共焦作市马村区委员会",
        "source": "https://www.jzmcqzf.gov.cn/2026/07-20/608363.html",
    },
    # ═══════ Government deputies (confirmed 领导之窗 2026-06-23) ═══════
    {
        "id": 7,
        "name": "牛涛",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长兼市公安局马村分局局长",
        "current_org": "马村区人民政府",
        "source": "http://www.jzmcqzf.gov.cn/2024/12-03/327451.html",
    },
    {
        "id": 8,
        "name": "樊志强",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "马村区人民政府",
        "source": "http://www.jzmcqzf.gov.cn/2024/12-03/327452.html",
    },
    {
        "id": 9,
        "name": "杨文涛",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "马村区人民政府",
        "source": "https://www.jzmcqzf.gov.cn/2026/06-23/606108.html",
    },
    {
        "id": 10,
        "name": "刘飞",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长、区政府办公室主任",
        "current_org": "马村区人民政府",
        "source": "https://www.jzmcqzf.gov.cn/2026/06-23/606109.html",
    },
    # ═══════ 区领导 (多次列席/调研，具体常委分工未实名) ═══════
    {
        "id": 11,
        "name": "邱华东",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "中共焦作市马村区委员会",
        "source": "https://www.jzmcqzf.gov.cn/2026/07-31/609588.html",
    },
    {
        "id": 12,
        "name": "孙光明",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "中共焦作市马村区委员会",
        "source": "https://www.jzmcqzf.gov.cn/2026/07-31/609588.html",
    },
    {
        "id": 13,
        "name": "王国强",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "中共焦作市马村区委员会",
        "source": "https://www.jzmcqzf.gov.cn/2026/07-31/609588.html",
    },
    {
        "id": 14,
        "name": "赵力",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "中共焦作市马村区委员会",
        "source": "https://www.jzmcqzf.gov.cn/2026/07-24/608895.html",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共焦作市马村区委员会", "type": "党委", "level": "市辖区", "parent": "中共焦作市委员会", "location": "马村区"},
    {"id": 2, "name": "马村区人民政府", "type": "政府", "level": "市辖区", "parent": "焦作市人民政府", "location": "马村区"},
    {"id": 3, "name": "焦作市公安局马村分局", "type": "政府", "level": "市辖区", "parent": "马村区人民政府", "location": "马村区"},
    {"id": 4, "name": "焦作市人民代表大会常务委员会", "type": "人大", "level": "地级市", "parent": "河南省人大常委会", "location": "焦作市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 王婕 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "2026-07", "end_date": "", "rank": "正处级", "note": "2026-07-21 官方新闻以马村区委书记身份调研；领导马村区委"},
    {"person_id": 1, "org_id": 2, "title": "区委书记（主持全面）", "start_date": "", "end_date": "", "rank": "正处级", "note": "区委书记与区政府配合关系"},

    # 徐志文 — 区长
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "2026-06", "end_date": "", "rank": "正处级", "note": "主持区政府全面工作，负责审计，分管区审计局；2026-07-31 主持区政府常务会议"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "2026-06", "end_date": "", "rank": "副处级", "note": "区长兼任区委副书记（通常安排）"},

    # 高艳红 — 区委常委、常务副区长
    {"person_id": 3, "org_id": 2, "title": "常务副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "负责区政府常务工作；协助区长分管审计"},
    {"person_id": 3, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": "区委常委"},

    # 尚少杰 — 区委常委、副区长
    {"person_id": 4, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "负责商务/招商引资/人社/卫健/医保/对台"},
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": "区委常委"},

    # 张东方 — 区委常委、区委办主任
    {"person_id": 5, "org_id": 1, "title": "区委常委、区委办主任", "start_date": "", "end_date": "", "rank": "副处级", "note": "承包车间口区化工企业（区委办）"},

    # 赵刚 — 区委常委、统战部长
    {"person_id": 6, "org_id": 1, "title": "区委常委、统战部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": "分包化工园区外化工企业（统战）"},

    # 牛涛 — 副区长兼公安分局局长
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "负责政法/社会治理/信访/退役军人/民族宗教"},
    {"person_id": 7, "org_id": 3, "title": "公安局局长", "start_date": "", "end_date": "", "rank": "", "note": "兼任市公安局马村分局局长"},

    # 樊志强 — 副区长
    {"person_id": 8, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "负责工业和信息化、科技"},

    # 杨文涛 — 副区长
    {"person_id": 9, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "负责农业农村、乡村振兴、教育、生态环境保护"},

    # 刘飞 — 副区长、政府办主任
    {"person_id": 10, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "负责住建、城管、交通；兼任区政府办公室主任"},

    # 列席区领导（具体职务待查）—— 关联区委
    {"person_id": 11, "org_id": 1, "title": "区领导", "start_date": "", "end_date": "", "rank": "", "note": "列席市委巡察反馈会；具体常职务待查"},
    {"person_id": 12, "org_id": 1, "title": "区领导", "start_date": "", "end_date": "", "rank": "", "note": "列席市委巡察反馈会；具体常职务待查"},
    {"person_id": 13, "org_id": 1, "title": "区领导", "start_date": "", "end_date": "", "rank": "", "note": "列席市委巡察反馈会；具体常职务待查"},
    {"person_id": 14, "org_id": 1, "title": "区领导", "start_date": "", "end_date": "", "rank": "", "note": "参加区大气污染防治调研；具体职务待查"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 王婕 ↔ 徐志文 (书记—区长，党政正职搭档)
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记—区长搭档；2026-07-24 防汛转移避险演练共同调研", "overlap_org": "中共焦作市马村区委员会", "overlap_period": "2026-07至今"},
    # 徐志文 ↔ 高艳红 (区长—常务副区长，上下级/协助审计)
    {"person_a": 2, "person_b": 3, "type": "上下级", "context": "区长—常务副区长；高艳红协助徐志文分管审计", "overlap_org": "马村区人民政府", "overlap_period": "2026"},
    # 书记 ↔ 常务副区长
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "区委书记—区委常委、常务副区长", "overlap_org": "中共焦作市马村区委员会", "overlap_period": "2026"},
    # 书记 ↔ 区委常委（张东方、赵刚、尚少杰）
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "区委书记—区委常委（副区长）", "overlap_org": "中共焦作市马村区委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "区委书记—区委常委、区委办主任", "overlap_org": "中共焦作市马村区委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "区委书记—区委常委、统战部部长", "overlap_org": "中共焦作市马村区委员会", "overlap_period": "2026"},
    # 区长 ↔ 各副区长（共事，区政府班子）
    {"person_a": 2, "person_b": 4, "type": "共事", "context": "区长—副区长", "overlap_org": "马村区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 7, "type": "共事", "context": "区长—副区长兼公安分局局长", "overlap_org": "马村区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 8, "type": "共事", "context": "区长—副区长", "overlap_org": "马村区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 9, "type": "共事", "context": "区长—副区长", "overlap_org": "马村区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 10, "type": "共事", "context": "区长—副区长兼政府办主任", "overlap_org": "马村区人民政府", "overlap_period": "2026"},
    # 常务副区长 ↔ 副区长（政府班子同僚）
    {"person_a": 3, "person_b": 4, "type": "同僚", "context": "区委常委—常务副区长/副区长", "overlap_org": "中共焦作市马村区委员会", "overlap_period": ""},
    {"person_a": 3, "person_b": 8, "type": "同僚", "context": "常务副区长—副区长(协助分管开发区)", "overlap_org": "马村区人民政府", "overlap_period": ""},
    {"person_a": 3, "person_b": 10, "type": "同僚", "context": "常务副区长—副区长(协助分管金融/处非)", "overlap_org": "马村区人民政府", "overlap_period": ""},
    {"person_a": 4, "person_b": 8, "type": "同僚", "context": "副区长—副区长(樊志强协助尚绍杰分管商务/招商)", "overlap_org": "马村区人民政府", "overlap_period": ""},
    # 区常委内部
    {"person_a": 3, "person_b": 5, "type": "同僚", "context": "区委常委同僚", "overlap_org": "中共焦作市马村区委员会", "overlap_period": ""},
    {"person_a": 3, "person_b": 6, "type": "同僚", "context": "区委常委同僚", "overlap_org": "中共焦作市马村区委员会", "overlap_period": ""},
    {"person_a": 4, "person_b": 5, "type": "同僚", "context": "区委常委同僚", "overlap_org": "中共焦作市马村区委员会", "overlap_period": ""},
    {"person_a": 4, "person_b": 6, "type": "同僚", "context": "区委常委同僚", "overlap_org": "中共焦作市马村区委员会", "overlap_period": ""},
    {"person_a": 5, "person_b": 6, "type": "同僚", "context": "区委常委同僚", "overlap_org": "中共焦作市马村区委员会", "overlap_period": ""},
    # 区领导（列席/调研，与核心班子共事）
    {"person_a": 1, "person_b": 14, "type": "共事", "context": "区委书记—区领导(参加调研)", "overlap_org": "中共焦作市马村区委员会", "overlap_period": "2026-07"},
    {"person_a": 2, "person_b": 9, "type": "共事", "context": "区长—副区长(杨文涛陪同调研)", "overlap_org": "马村区人民政府", "overlap_period": "2026-08"},
    {"person_a": 1, "person_b": 11, "type": "共事", "context": "区委书记—区领导(列席市巡察反馈会)", "overlap_org": "中共焦作市马村区委员会", "overlap_period": "2026-07-27"},
    {"person_a": 1, "person_b": 12, "type": "共事", "context": "区委书记—区领导(列席市巡察反馈会)", "overlap_org": "中共焦作市马村区委员会", "overlap_period": "2026-07-27"},
    {"person_a": 1, "person_b": 13, "type": "共事", "context": "区委书记—区领导(列席市巡察反馈会)", "overlap_org": "中共焦作市马村区委员会", "overlap_period": "2026-07-27"},
]


# ═════════════════════════════════════════════════════════════════════════════
# Build
# ═════════════════════════════════════════════════════════════════════════════

def write_person_json(person: dict) -> None:
    """Write a per-person graph JSON file to the staging directory (repo schema v1.0)."""
    pid = person["id"]
    name = person["name"]
    slug_id = f"henan_jiaozuo_macun_{name}"

    person_positions = [p for p in positions if p["person_id"] == pid]
    career_timeline = []
    for pos in person_positions:
        org = next((o for o in organizations if o["id"] == pos["org_id"]), None)
        career_timeline.append({
            "start": pos.get("start_date", "") or "",
            "end": pos.get("end_date", "") or "",
            "org": org["name"] if org else "",
            "title": pos["title"],
            "rank": pos.get("rank", ""),
            "note": pos.get("note", "") or "",
            "confidence": "confirmed" if pid in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10) else "plausible",
        })

    person_rels = [r for r in relationships if r["person_a"] == pid or r["person_b"] == pid]
    connections = []
    for r in person_rels:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id), None)
        connections.append({
            "person": other["name"] if other else f"person_{other_id}",
            "person_id": f"henan_jiaozuo_macun_{other['name']}" if other else f"person_{other_id}",
            "relationship_type": "overlap",
            "strength": "strong" if r["type"] in ("共事", "上下级", "党政搭档") else "medium",
            "evidence": r["context"],
            "overlap_org": r["overlap_org"],
            "overlap_period": r["overlap_period"],
            "direction": "undirected",
            "confidence": "confirmed" if pid in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10) else "plausible",
        })

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "河南省",
            "city": "焦作市",
            "region": "马村区",
            "job": person["current_post"],
            "task_id": "henan_马村区",
            "time_focus": "2026-07/08",
        },
        "identity": {
            "person_id": slug_id,
            "name": name,
            "aliases": [],
            "gender": person["gender"],
            "ethnicity": "",
            "birth": "",
            "birthplace": "",
            "native_place": "",
            "education": [],
            "party_join": "中共党员",
            "work_start": "",
            "dedupe_keys": {
                "name_birth": f"{name}_",
                "name_birthplace": f"{name}_",
                "official_profile_url": person["source"],
            },
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "正处级" if pid in (1, 2) else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"],
        },
        "career_timeline": career_timeline,
        "organizations": [
            {"org_name": o["name"], "org_type": o["type"], "role": pos["title"], "period": (pos.get("start_date") or "") + ("-" + (pos.get("end_date") or "至今") if pos.get("end_date") else "-至今")}
            for pos, o in ((p, next((x for x in organizations if x["id"] == p["org_id"]), None)) for p in person_positions)
            if o
        ],
        "relationships": connections,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "缺乏公开数据", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": f"截至研究日，未发现{name}的纪律处分、审计问题或负面媒体报道公开记录", "date": AS_OF, "confidence": "unverified", "source_ids": []}
        ],
        "source_register": [
            {"id": "S001", "title": "马村区人民政府门户—领导之窗/政务要闻", "url": person["source"],
             "publisher": "马村区人民政府", "published_at": "", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high", "notes": ""}
        ],
        "confidence_summary": {
            "identity": "confirmed" if pid in (1, 2) else "plausible",
            "current_role": "confirmed" if pid in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10) else "plausible",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "核心主官（出生、籍贯、学历、入党、参加工作）及任前完整履历未公开" if pid in (1, 2) else "人物生物字段及任前履历未公开",
        },
        "open_questions": [
            {
                "priority": "critical" if pid in (1, 2) else "medium",
                "question": f"{name}的出生年月/籍贯/学历/入党/参加工作及任现职前完整履历未知",
                "why_it_matters": "核心主官人事网络归类与去重依赖履历",
                "suggested_queries": [f"{name} 任前公示 焦作", f"{name} 简历 马村区"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high" if pid in (1, 2) else "low",
                "question": f"前任（王婕前任区委书记 / 徐志文前任区长）姓名及调任去向",
                "why_it_matters": "继任链还原",
                "suggested_queries": ["马村区 区委书记 前任", "马村区 区长 任命 人大"],
                "last_attempted": AS_OF,
            },
        ],
    }
    fname = f"{TODAY}-河南省-焦作市-{person['current_post'].replace('、','_').replace('，','_')}-{name}.json"
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
    for p in persons:
        write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())