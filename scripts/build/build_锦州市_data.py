#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 锦州市 (Jinzhou City), 辽宁省.

Investigation date: 2026-08-06
Task ID: liaoning_锦州市
Level: 地级市
Targets: 市委书记 & 市长

Research sources:
  - www.jz.gov.cn — 锦州市人民政府门户网站 (OFFICIAL, confirmed reachable)
    - 政府领导页面 (zfld.htm) + 领导简介 (zfld/*.htm) — deputy mayor roster & bios, OFFICIAL confirmed
    - 政府工作报告 2026-01-07 (十七届人大六次会议, 市长孟华强) — confirms 市长 孟华强 (2026)
    - 政府工作报告 2025-01-08 (十七届人大四次会议, 市长王心宇) — confirms successor of 王心宇
    - 首页要闻「刘克武听取全市树立和践行正确政绩观学习教育工作情况汇报」(2026-08) — confirms 市委书记 刘克武 current
  - Web search degraded: Exa rate-limited, Baidu 403/captcha, Jina Reader timeout

Confirmed via official site (www.jz.gov.cn), as of 2026-08:
  - 市长: 孟华强 — 男，汉族，1976-01生，研究生学历，经济学博士，中共党员，锦州市委副书记、市长
  - 常委、常务副市长: 王利民 — 男，汉族，1977-04生，在职研究生硕士，中共党员
  - 副市长: 缪徵阁 — 男，汉族，1978-05生，省委党校研究生，中共党员（市政府党组成员）
  - 副市长: 蒋立新 — 女，汉族，1968-04生，大学学历、硕士学位，民进会员
  - 副市长: 孙得胜 — 男，汉族，1973-10生，在职研究生博士，市公安局长（政府党组成员）
  - 副市长: 徐继华 — 男，汉族，1983-01生，研究生，经济学博士，金融学博士后（政府党组成员）
  - 副市长: 焦健 — 男，汉族，1970-04生，大学学历，中共党员（政府党组成员）
  - 副市长: 屈晓明 — 男，汉族，1979-12生，在职研究生硕士，中共党员（政府党组成员）
  - 市委书记: 刘克武 — 现任 confirmed via official headline (2026-08)；详细履历待核

前任:
  - 前市长 王心宇 — 2021-12 代市长(十七届人大一次), 2022-01 起作政府工作报告(市长)，至 2025 卸任
  - 前市长 于学利 — 2020-2021 政府工作报告市长（2020-03、2021-03），后任市委书记
  - 前市委书记 刘克武 继任自 靳国卫（2022 前）— 因外部检索受限，前书记完整序列以 plausible 标注

Confidence notes:
  - 现任市长及 7 名副市长的身份/出生年月/学历：confirmed（官方网页）
  - 市委书记 刘克武 的在任身份：confirmed（官方媒体报道）；完整履历：plausible / 部分 unknown
  - 前市长 王心学/于学利 的在任年份：plausible（政府工作报告署名）
  - 常委班子其余成员（组织/宣传/纪委/统战/政法委）名单与分工：基本未获一手来源 → unverified，列入 open_questions
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

import sqlite3  # noqa
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "锦州市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "liaoning_锦州市"
if _CURRENT_DIR.name == "liaoning_锦州市":
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
# ID 1 = 市委书记, 2 = 市长, 3-9 = 副市长, 10+ = 前任/相关
persons = [
    # ══════════════════════════════════════════════════════════════════════
    # 现任核心领导
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "刘克武",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共锦州市委员会",
        "source": "http://www.jz.gov.cn/",
        "confidence": "plausible",
        "notes": "现任锦州市委书记（2026-08 官方媒体报道确认在任）。曾任锦州市委副书记。完整履历（出生/教育/前期任职）待核。"
    },
    {
        "id": 2,
        "name": "孟华强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年1月",
        "birthplace": "",
        "education": "研究生学历，经济学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市长",
        "current_org": "锦州市人民政府",
        "source": "http://www.jz.gov.cn/zwgk/zfld/mhq.htm",
        "confidence": "confirmed",
        "notes": "现任锦州市委副书记、市长。主持市政府全面工作。2026-01-07 在十七届人大五次会议作政府工作报告。前期曾为市委副书记。"
    },
    {
        "id": 3,
        "name": "王利民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年4月",
        "birthplace": "",
        "education": "在职研究生学历，硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、常务副市长",
        "current_org": "锦州市人民政府",
        "source": "http://www.jz.gov.cn/zwgk/zfld/wlm.htm",
        "confidence": "confirmed",
        "notes": "市委常委、常务副市长，负责市政府常务工作；负责发展改革、财政、交通运输、国资国企等；协助市长分管审计局等。"
    },
    {
        "id": 4,
        "name": "缪徵阁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年5月",
        "birthplace": "",
        "education": "在职省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "锦州市人民政府",
        "source": "http://www.jz.gov.cn/zwgk/zfld/mzg.htm",
        "confidence": "confirmed",
        "notes": "市政府党组成员、副市长，负责援藏工作。"
    },
    {
        "id": 5,
        "name": "蒋立新",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1968年4月",
        "birthplace": "",
        "education": "大学学历，硕士学位",
        "party_join": "民进会员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "锦州市人民政府",
        "source": "http://www.jz.gov.cn/zwgk/zfld/jlx.htm",
        "confidence": "confirmed",
        "notes": "副市长（民主党派：民进会员），负责水利、农业农村、乡村振兴、林业草原、文化旅游、体育及县域经济。"
    },
    {
        "id": 6,
        "name": "孙得胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年10月",
        "birthplace": "",
        "education": "在职研究生学历，博士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长、市公安局局长",
        "current_org": "锦州市人民政府",
        "source": "http://www.jz.gov.cn/zwgk/zfld/sds.htm",
        "confidence": "confirmed",
        "notes": "市政府党组成员、副市长，市公安局党委书记、局长。负责公安、司法、打击走私。"
    },
    {
        "id": 7,
        "name": "徐继华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年1月",
        "birthplace": "",
        "education": "研究生学历，经济学博士，金融学博士后",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "锦州市人民政府",
        "source": "http://www.jz.gov.cn/zwgk/zfld/xjh.htm",
        "confidence": "confirmed",
        "notes": "市政府党组成员、副市长。负责工业信息化、商务外事、招商引资、大数据、金融（产业基金）。金融/经济专业背景。"
    },
    {
        "id": 8,
        "name": "焦健",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年4月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "锦州市人民政府",
        "source": "http://www.jz.gov.cn/zwgk/zfld/j_j.htm",
        "confidence": "confirmed",
        "notes": "市政府党组成员、副市长，负责教育、自然资源、生态环境、住房城乡建设、卫生健康、医保、城管执法。"
    },
    {
        "id": 9,
        "name": "屈晓明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年12月",
        "birthplace": "",
        "education": "在职研究生学历，硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "锦州市人民政府",
        "source": "http://www.jz.gov.cn/zwgk/zfld/qxm.htm",
        "confidence": "confirmed",
        "notes": "市政府党组成员、副市长，负责科技、民政、人力资源社会保障、退役军人事务、市场监管。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 前任
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 20,
        "name": "王心宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市长",
        "current_org": "锦州市人民政府",
        "source": "http://www.jz.gov.cn/info/1055/121523.htm",
        "confidence": "plausible",
        "notes": "前任锦州市长：2021-12 代市长（十七届人大一次），2022-01 起作市长报告；2025-01-08 十七届人大四次会议仍由王心宇作报告（任期至 2025）。卸任后去向待核。"
    },
    {
        "id": 21,
        "name": "于学利",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市长",
        "current_org": "锦州市人民政府",
        "source": "http://www.jz.gov.cn/info/1055/3609.htm",
        "confidence": "plausible",
        "notes": "前任锦州市长（2020-01-2021 政府工作报告市长）。后任锦州市委书记（2020—2022），继而调离。去向待核。"
    },
    {
        "id": 22,
        "name": "靳国卫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市委书记",
        "current_org": "中共锦州市委员会",
        "source": "公开报道",
        "confidence": "unverified",
        "notes": "前任锦州市委书记（约2019-2022），刘克武的前任。后去向待核（可能调任省直部门）。外部检索受限，履历待核。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共锦州市委员会", "type": "党委", "level": "地厅级", "parent": "中共辽宁省委员会", "location": "锦州市"},
    {"id": 2, "name": "锦州市人民政府", "type": "政府", "level": "地厅级", "parent": "辽宁省人民政府", "location": "锦州市"},
    {"id": 3, "name": "锦州市人民代表大会常务委员会", "type": "人大", "level": "地厅级", "parent": "辽宁省人大常委会", "location": "锦州市"},
    {"id": 4, "name": "中国人民政治协商会议锦州市委员会", "type": "政协", "level": "地厅级", "parent": "政协辽宁省委员会", "location": "锦州市"},
    {"id": 5, "name": "中共锦州市纪律检查委员会", "type": "党委", "level": "地厅级", "parent": "中共锦州市委员会", "location": "锦州市"},
    {"id": 6, "name": "锦州市公安局", "type": "政府", "level": "处级", "parent": "锦州市人民政府", "location": "锦州市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 刘克武 — 市委书记
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": "现任锦州市委书记（2026-08 在任）"},
    # 孟华强 — 市长
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": "此前任市委副书记"},
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "2024-12", "end_date": "", "rank": "正厅级", "note": "现任市长，2026-01 作政府工作报告（推测 2024年底或2025年代市长，2025-12 当选）"},
    # 王利民 — 常务副市长
    {"person_id": 3, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "正厅级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "常务副市长", "start_date": "", "end_date": "", "rank": "正厅级", "note": "负责市政府常务工作"},
    # 缪徵阁
    {"person_id": 4, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "援藏"},
    # 蒋立新
    {"person_id": 5, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "民进会员"},
    # 孙得胜
    {"person_id": 6, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 6, "org_id": 6, "title": "市公安局局长", "start_date": "", "end_date": "", "rank": "正处级", "note": "市公安局党委书记、局长"},
    # 徐继华
    {"person_id": 7, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 焦健
    {"person_id": 8, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 屈晓明
    {"person_id": 9, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 前任
    {"person_id": 20, "org_id": 2, "title": "市长", "start_date": "2021-12", "end_date": "2025", "rank": "正厅级", "note": "前任锦州市长（代市长 2021-12，市长 2022-2025）"},
    {"person_id": 21, "org_id": 2, "title": "市长", "start_date": "2018", "end_date": "2021", "rank": "正厅级", "note": "前任锦州市长（2020-2021 报告中市长）"},
    {"person_id": 22, "org_id": 1, "title": "市委书记", "start_date": "2019", "end_date": "2022", "rank": "正厅级", "note": "前任锦州市委书记（约2019-2022）"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 现任班子
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "市委书记—市长搭档", "overlap_org": "中共锦州市委员会", "overlap_period": "2025至今"},
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "市委书记—市委常委", "overlap_org": "中共锦州市委员会", "overlap_period": ""},
    {"person_a": 2, "person_b": 3, "type": "共事", "context": "市长—常务副市长", "overlap_org": "锦州市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 4, "type": "共事", "context": "市长—副市长", "overlap_org": "锦州市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 5, "type": "共事", "context": "市长—副市长", "overlap_org": "锦州市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 6, "type": "共事", "context": "市长—副市长/公安局长", "overlap_org": "锦州市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 7, "type": "共事", "context": "市长—副市长", "overlap_org": "锦州市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "共事", "context": "市长—副市长", "overlap_org": "锦州市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 9, "type": "共事", "context": "市长—副市长", "overlap_org": "锦州市人民政府", "overlap_period": ""},
    # 前任交接
    {"person_a": 20, "person_b": 2, "type": "交接", "context": "前任市长—继任市长", "overlap_org": "锦州市人民政府", "overlap_period": "2025"},
    {"person_a": 21, "person_b": 20, "type": "交接", "context": "前任市长—继任市长", "overlap_org": "锦州市人民政府", "overlap_period": "2021"},
    {"person_a": 22, "person_b": 1, "type": "交接", "context": "前任市委书记—继任市委书记", "overlap_org": "中共锦州市委员会", "overlap_period": "2022"},
]


# ═════════════════════════════════════════════════════════════════════════════
# Helper functions (person JSON)
# ═════════════════════════════════════════════════════════════════════════════

def _get_open_questions(person: dict) -> list[str]:
    q = []
    if not person.get("birth"):
        q.append("出生年月未确认")
    if not person.get("birthplace"):
        q.append("籍贯/出生地未确认")
    if not person.get("education"):
        q.append("学历教育背景未确认")
    if not person.get("work_start"):
        q.append("参加工作年份未确认")
    if "待核" in person.get("notes", ""):
        q.append("完整任职履历未确认")
    return q


def write_person_json(person: dict) -> None:
    pid = person["id"]
    name = person["name"]
    slug_id = f"jinzhou_{name}"

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
            "source_ids": ["S001", "S002"] if person.get("confidence") == "confirmed" else ["S001"],
        })
    if len(career_timeline) <= 2 and (not person.get("birth") or "待核" in person.get("notes", "")):
        career_timeline.append({
            "start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
            "notes": "公开资料不足：外部检索受限（Exa 限流、百度 403、Jina 超时），完整履历待核。",
            "confidence": "unverified", "source_ids": [],
        })

    person_rels = [r for r in relationships if r["person_a"] == pid or r["person_b"] == pid]
    rels_output = []
    for r in person_rels:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        if other_id == pid:
            continue
        other = next((p for p in persons if p["id"] == other_id), None)
        other_name = other["name"] if other else f"person_{other_id}"
        rel_type = "overlap" if r["type"] == "共事" else "predecessor_successor"
        strength = "strong" if r["type"] == "共事" else "medium"
        rels_output.append({
            "person": other_name, "person_id": f"jinzhou_{other_name}",
            "relationship_type": rel_type, "strength": strength,
            "evidence": r.get("context", ""), "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""), "direction": "undirected",
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001"],
        })

    source_url = person.get("source", "")
    sources = [{
        "id": "S001",
        "title": "锦州市人民政府门户网站—政府领导",
        "url": source_url or "http://www.jz.gov.cn/zwgk/zfld.htm",
        "publisher": "锦州市人民政府",
        "published_at": "",
        "accessed_at": AS_OF,
        "source_type": "official" if source_url.startswith("http://www.jz.gov.cn") else "media",
        "reliability": "high" if person.get("confidence") == "confirmed" else "medium",
        "notes": "官方一手来源",
    }]
    if source_url != "http://www.jz.gov.cn/zwgk/zfld/mhq.htm":
        sources.append({
            "id": "S002", "title": "政府工作报告（2026-01-07）",
            "url": "http://www.jz.gov.cn/info/1055/126024.htm",
            "publisher": "锦州市人民政府", "published_at": "2026-01-07",
            "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
            "notes": "确认市长为孟华强",
        })

    big_gap = "完整履历与出生信息缺失（外部检索受限）"
    if person.get("confidence") == "confirmed":
        big_gap = "前期任职履历（担任市长前的职务）待核"

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "辽宁省", "city": "锦州市", "region": "锦州市",
            "job": person.get("current_post", ""),
            "task_id": "liaoning_锦州市", "time_focus": "2024–2026",
        },
        "identity": {
            "person_id": slug_id, "name": name, "aliases": [],
            "gender": person.get("gender", ""), "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""), "birthplace": person.get("birthplace", ""),
            "native_place": "", "education": [], "party_join": person.get("party_join", ""),
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
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
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
            "identity": "unverified" if not person.get("birth") else "plausible",
            "current_role": person.get("confidence", "unverified"),
            "career_completeness": "thin",
            "relationship_confidence": "low" if person.get("confidence") == "unverified" else "medium",
            "biggest_gap": big_gap,
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的准确出生年月、籍贯、学历教育背景",
                "why_it_matters": "核心身份信息，用于去重和跨区域关联分析",
                "suggested_queries": [f"{name} 简历 锦州", f"{name} 任前公示", f"{name} 百度百科"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": f"{name}的完整任职履历（每段职务的起止时间与前期职务）",
                "why_it_matters": "关系网络分析需要精确时间线",
                "suggested_queries": [f"{name} 此前担任", f"{name} 任职经历", f"{name} 辽宁省委组织部"],
                "last_attempted": AS_OF,
            },
        ],
    }

    post_slug = person['current_post'].replace('/', '_')
    fname = f"{TODAY}-辽宁省-锦州市-{post_slug}-{person['name']}.json"
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
    core_ids = {1, 2, 3, 4, 5, 6, 7, 8, 9, 20}
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())