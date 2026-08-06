#!/usr/bin/env python3
"""武汉市江岸区领导班子工作关系网络 — 数据构建脚本。

等级: 市辖区
调查日期: 2026-08-06
信息来源: 江岸区人民政府门户网 (www.jiangan.gov.cn, 官方, 可访问)
          江岸要闻媒体报道、长江日报专访、区两会新闻
备注: 区委书记李世涛同时兼任武汉市经济和信息化局党组书记、局长（2026 年 4 月起在报道中列明）。
      前任区委书记姚彬 2026-02-26 仍任，约 2026-03~04 交任李世涛。
"""

from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

# Ensure gov_relation package is importable
_repo_root = Path(__file__).resolve().parents[3]
if str(_repo_root) not in sys.path:
    sys.path.insert(0, str(_repo_root))

from gov_relation.runner import run_build

# ── Config ────────────────────────────────────────────────────────────────────
SLUG = "江岸区"
TODAY = "2026-08-06"
STAGING = Path(__file__).resolve().parent

DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────────────
# 1xxx = 区委（含 书记/副书记/常委）, 2xxx = 区政府, 3xxx = 人大/政协
persons = [
    # ══════════════════════ 1. 现任区委书记 ══════════════════════
    {
        "id": 1001,
        "name": "李世涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委书记，武汉市经济和信息化局党组书记、局长",
        "current_org": "中共武汉市江岸区委员会（兼任武汉市经济和信息化局）",
        "source": "https://www.jiangan.gov.cn/jaxxw/jazx/jayw_1/202604/t20260421_2755488.shtml",
    },
    # ══════════════════════ 2. 现任区长 ══════════════════════
    {
        "id": 2001,
        "name": "陈荃",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年12月",
        "birthplace": "湖北武汉",
        "education": "大学学历、工程硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "区委副书记，区人民政府党组书记、区长",
        "current_org": "中共武汉市江岸区委员会 / 江岸区人民政府",
        "source": "https://www.jiangan.gov.cn/jaxxw/zfxxgk/fdzdgk/ldjj_41351/202405/t20240506_2397376.shtml",
    },
    # ══════════════════════ 3. 区委副书记、政法委书记 ══════════════════════
    {
        "id": 1002,
        "name": "李辉",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委副书记、区委政法委员会书记",
        "current_org": "中共武汉市江岸区委员会 / 江岸区委政法委员会",
        "source": "https://www.jiangan.gov.cn/jaxxw/jazx/jayw_1/202604/t20260421_2758768.shtml",
    },
    # ══════════════════════ 4. 区委副书记（推定） ══════════════════════
    {
        "id": 1003,
        "name": "陈伟",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委副书记（推定）",
        "current_org": "中共武汉市江岸区委员会",
        "source": "https://www.jiangan.gov.cn/jaxxw/jazx/jayw_1/202607/t20260713_2820050.shtml（防汛检查排位推定）",
    },
    # ══════════════════════ 5. 区委常委、常务副区长 ══════════════════════
    {
        "id": 2002,
        "name": "王丰伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年12月",
        "birthplace": "湖北天门",
        "education": "硕士研究生，管理学硕士",
        "party_join": "2013年10月",
        "work_start": "2007年7月",
        "current_post": "区委常委、区人民政府副区长（分管日常工作）、党组副书记",
        "current_org": "中共江岸区委员会 / 江岸区人民政府",
        "source": "https://www.jiangan.gov.cn/jaxxw/zfxxgk/fdzdgk/ldjj_41351/202505/t20250528_2587205.shtml",
    },
    # ══════════════════════ 6. 区委常委、副区长 ══════════════════════
    {
        "id": 2003,
        "name": "吴江",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年2月",
        "birthplace": "湖北红安",
        "education": "在职硕士研究生，公共管理学硕士",
        "party_join": "2002年12月",
        "work_start": "2004年8月",
        "current_post": "区委常委、副区长",
        "current_org": "中共江岸区委员会 / 江岸区人民政府",
        "source": "https://www.jiangan.gov.cn/jaxxw/zfxxgk/fdzdgk/ldjj_41351/202112/t20211229_1884111.shtml",
    },
    # ══════════════════════ 7. 区委常委、组织部长 ══════════════════════
    {
        "id": 1004,
        "name": "郑东",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、区委组织部部长",
        "current_org": "中共武汉市江岸区委员会",
        "source": "https://www.jiangan.gov.cn/jaxxw/jazx/jayw_1/202606/t20260629_2814196.shtml",
    },
    # ══════════════════════ 8. 区委常委、纪委书记 ══════════════════════
    {
        "id": 1005,
        "name": "张显军",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、区纪委书记、区监察委员会主任",
        "current_org": "中共江岸区纪律检查委员会（区监委）",
        "source": "https://www.jiangan.gov.cn/jaxxw/jazx/jayw_1/202602/t20260228_2733295.shtml",
    },
    # ══════════════════════ 9. 副区长（公安） ══════════════════════
    {
        "id": 2004,
        "name": "周文化",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966年11月",
        "birthplace": "湖北松滋",
        "education": "大学学历",
        "party_join": "1995年10月",
        "work_start": "1987年10月",
        "current_post": "区人民政府副区长、党组成员，区公安分局局长、督察长（兼）",
        "current_org": "江岸区人民政府 / 武汉市公安局江岸区分局",
        "source": "https://www.jiangan.gov.cn/jaxxw/zfxxgk/fdzdgk/ldjj_41351/202504/t20250409_2564196.shtml",
    },
    # ══════════════════════ 10. 副区长 ══════════════════════
    {
        "id": 2005,
        "name": "严松毅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年4月",
        "birthplace": "湖北武汉",
        "education": "大学学历",
        "party_join": "1997年6月",
        "work_start": "1991年7月",
        "current_post": "区人民政府副区长",
        "current_org": "江岸区人民政府",
        "source": "https://www.jiangan.gov.cn/jaxxw/zfxxgk/fdzdgk/ldjj_41351/202212/t20221219_2116378.shtml",
    },
    # ══════════════════════ 11. 副区长 ══════════════════════
    {
        "id": 2006,
        "name": "邓军林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年9月",
        "birthplace": "湖北武汉",
        "education": "大学，法学学士",
        "party_join": "1996年4月",
        "work_start": "1996年7月",
        "current_post": "区人民政府副区长",
        "current_org": "江岸区人民政府",
        "source": "https://www.jiangan.gov.cn/jaxxw/zfxxgk/fdzdgk/ldjj_41351/202308/t20230828_2254195.shtml",
    },
    # ══════════════════════ 12. 副区长（民主党派） ══════════════════════
    {
        "id": 2007,
        "name": "肖美华",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1979年12月",
        "birthplace": "湖北罗田",
        "education": "研究生学历，经济学硕士",
        "party_join": "（九三学社社员）",
        "work_start": "2001年8月",
        "current_post": "区人民政府副区长",
        "current_org": "江岸区人民政府",
        "source": "https://www.jiangan.gov.cn/jaxxw/zfxxgk/fdzdgk/ldjj_41351/202312/t20231225_2328209.shtml",
    },
    # ══════════════════════ 13. 副区长（待查） ══════════════════════
    {
        "id": 2008,
        "name": "李绪杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区人民政府副区长",
        "current_org": "江岸区人民政府",
        "source": "https://www.jiangan.gov.cn/jaxxw/zfxxgk/fdzdgk/ldjj_41351/（专家团队建设待查）",
    },
    # ══════════════════════ 14. 区人大常委会主任 ══════════════════════
    {
        "id": 3001,
        "name": "黄胜林",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "江岸区人民代表大会常务委员会",
        "source": "https://www.jiangan.gov.cn/jaxxw/zfxxgk/fdzdgk/ldjj_41351/（区十六届人大六次会议）",
    },
    # ══════════════════════ 15. 区政协主席 ══════════════════════
    {
        "id": 3002,
        "name": "许光辉",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "政协江岸区委员会",
        "source": "https://www.jiangan.gov.cn/jaxxw/zfxxgk/drdgk/ldjj_41351/（政协十六届五次会议）",
    },
    # ══════════════════════ 16. 前任区委书记 ══════════════════════
    {
        "id": 1006,
        "name": "姚彬",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任区委书记（2026-02 仍在任，约 2026-03~04 交任）",
        "current_org": "中共武汉市江岸区委员会",
        "source": "https://www.jiangan.gov.cn/jaxxw/jazx/jayw_1/202602/t20260228_2733295.shtml",
    },
]

# ── Organizations ────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共武汉市江岸区委员会", "type": "党委", "level": "县处级", "parent": "中共武汉市委", "location": "武汉市江岸区"},
    {"id": 2, "name": "江岸区人民政府", "type": "政府", "level": "县处级", "parent": "武汉市人民政府", "location": "武汉市江岸区"},
    {"id": 3, "name": "武汉市经济和信息化局", "type": "政府机构", "level": "县处级", "parent": "武汉市人民政府", "location": "武汉市"},
    {"id": 4, "name": "江岸区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "", "location": "武汉市江岸区"},
    {"id": 5, "name": "政协江岸区委员会", "type": "政协", "level": "县处级", "parent": "", "location": "武汉市江岸区"},
    {"id": 6, "name": "中共江岸区纪律检查委员会（区监委）", "type": "纪委", "level": "县处级", "parent": "中共武汉市纪委", "location": "武汉市江岸区"},
    {"id": 7, "name": "江岸区委政法委员会", "type": "党委", "level": "县处级", "parent": "中共江岸区委", "location": "武汉市江岸区"},
    {"id": 8, "name": "市公安局江岸区分局", "type": "公安", "level": "县处级", "parent": "武汉市公安局", "location": "武汉市江岸区"},
]

# ── Positions (任职) ────────────────────────────────────────────────────
positions = [
    # 区委书记/副书记/常委
    {"person_id": 1001, "org_id": 1, "title": "区委书记", "start_date": "约2026-04", "end_date": "", "rank": "县处级", "note": "兼市经信局党组书记、局长"},
    {"person_id": 1001, "org_id": 3, "title": "市经济信息化局党组书记、局长", "start_date": "", "end_date": "", "rank": "县处级", "note": "兼"},
    {"person_id": 2001, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "", "rank": "县处级", "note": ""},
    {"person_id": 2001, "org_id": 2, "title": "区政府党组书记、区长", "start_date": "", "end_date": "", "rank": "县处级", "note": "领导区政府全面工作"},
    {"person_id": 1002, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "", "rank": "县处级", "note": ""},
    {"person_id": 1002, "org_id": 7, "title": "区委政法委书记", "start_date": "", "end_date": "", "rank": "县处级", "note": ""},
    {"person_id": 1003, "org_id": 1, "title": "区委副书记（推定）", "start_date": "", "end_date": "", "rank": "县处级", "note": ""},
    {"person_id": 1004, "org_id": 1, "title": "区委常委、组织部长", "start_date": "", "end_date": "", "rank": "县处级", "note": ""},
    {"person_id": 1005, "org_id": 1, "title": "区委常委、纪委书记", "start_date": "", "end_date": "", "rank": "县处级", "note": ""},
    {"person_id": 1005, "org_id": 6, "title": "区纪委书记、监委主任", "start_date": "", "end_date": "", "rank": "县处级", "note": ""},
    # 政府
    {"person_id": 2002, "org_id": 2, "title": "常务副区长、党组副书记", "start_date": "", "end_date": "", "rank": "县处级", "note": "分管日常、发改、经信科技、财政、应急等"},
    {"person_id": 2003, "org_id": 2, "title": "副区长（常委）", "start_date": "", "end_date": "", "rank": "县处级", "note": "城建、规划"},
    {"person_id": 2004, "org_id": 2, "title": "副区长、区公安分局局长", "start_date": "", "end_date": "", "rank": "县处级", "note": "公安、信访"},
    {"person_id": 2004, "org_id": 8, "title": "区公安分局局长", "start_date": "", "end_date": "", "rank": "县处级", "note": ""},
    {"person_id": 2005, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级", "note": "教育、卫生"},
    {"person_id": 2006, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级", "note": "城管、水务"},
    {"person_id": 2007, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级", "note": "商务、统计"},
    {"person_id": 2008, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级", "note": ""},
    # 人大/政协
    {"person_id": 3001, "org_id": 4, "title": "区人大常委会主任", "start_date": "", "end_date": "", "rank": "县处级", "note": ""},
    {"person_id": 3002, "org_id": 5, "title": "区政协主席", "start_date": "", "end_date": "", "rank": "县处级", "note": ""},
    # 前任书记
    {"person_id": 1006, "org_id": 1, "title": "区委书记（前任）", "start_date": "", "end_date": "约2026-03", "rank": "县处级", "note": "2026-02-26 仍在任，约2026-03~04 交任李世涛"},
]

# ── relationships (关系) ────────────────────────────────────────
relationships = [
    # 现任党政一把手搭档
    {"person_a": 1001, "person_b": 2001, "type": "同班子", "context": "区党政一把手搭档，共同主持全区重大工作", "overlap_org": "中共江岸区委/区政府", "overlap_period": "2026-至今"},
    {"person_a": 1001, "person_b": 2001, "type": "工作交叠", "context": "二人共同带队检查防汛、走访三峡集团等", "overlap_org": "江岸区", "overlap_period": "2026-04~07"},
    # 书记 与 副职
    {"person_a": 1001, "person_b": 1002, "type": "上下级", "context": "区委书记-区委副书记（分管组织、政法）", "overlap_org": "中共江岸区委", "overlap_period": "2026-至今"},
    {"person_a": 1001, "person_b": 1005, "type": "上下级", "context": "区委书记-纪委书记（纪委全会）", "overlap_org": "中共江岸区委", "overlap_period": "2026-至今"},
    {"person_a": 1001, "person_b": 2002, "type": "上下级", "context": "区委书记-常务副区长（涉务、防汛）", "overlap_org": "江岸区委/区政府", "overlap_period": "2026-至今"},
    # 区长-副区长
    {"person_a": 2001, "person_b": 2002, "type": "上下级", "context": "区长-常务副区长", "overlap_org": "江岸区人民政府", "overlap_period": "至今"},
    {"person_a": 2001, "person_b": 2007, "type": "共事", "context": "区长-副区长（政府班子）", "overlap_org": "江岸区人民政府", "overlap_period": "至今"},
    # 政法委
    {"person_a": 1002, "person_b": 2004, "type": "系统", "context": "区委政法委书记-公安局长（政法系统）", "overlap_org": "江岸区政法系统", "overlap_period": "至今"},
    # 前任接班
    {"person_a": 1006, "person_b": 1001, "type": "前任接任", "context": "前任区委书记姚彬 → 李世涛", "overlap_org": "中共江岸区委", "overlap_period": "2026-03~04"},
    # 人大常委会/政协 关系
    {"person_a": 1001, "person_b": 3001, "type": "工作联系", "context": "区委书记-人大主任（两会）", "overlap_org": "江岸区", "overlap_period": "2026"},
    {"person_a": 1001, "person_b": 3002, "type": "工作联系", "context": "区委书记-政协主席（两会）", "overlap_org": "江岸区", "overlap_period": "2026"},
]

# ── Main ─────────────────────────────────────────────────────────────────────

def person_json(person: dict) -> None:
    from gov_relation.paths import PERSONS_DIR
    safe_name = person["name"]
    # Short, canonical job labels for clean filename (task-required pattern).
    short_job = {
        1001: "区委书记", 2001: "区长", 1002: "区委副书记兼政法委书记",
        1003: "区委副书记", 2002: "常务副区长", 2003: "副区长（常委）",
        1004: "组织部长", 1005: "纪委书记", 2004: "副区长（公安局长）",
        2005: "副区长", 2006: "副区长", 2007: "副区长", 2008: "副区长",
        3001: "人大主任", 3002: "政协主席", 1006: "前任区委书记",
    }
    job_slug = short_job.get(person["id"], person["current_post"])
    filename = f"{TODAY.replace('-', '')}-湖北省-武汉市-{job_slug}-{safe_name}.json"
    filepath = STAGING / filename

    person_json = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "湖北省", "city": "武汉市", "region": "江岸区",
            "job": person["current_post"], "task_id": "hubei_江岸区", "time_focus": "2024-2026",
        },
        "identity": {
            "person_id": f"hubei_wuhan_jiangan_{safe_name}",
            "name": safe_name, "aliases": [], "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""), "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""), "native_place": "",
            "education": [{"period": "", "institution": "", "major": "",
                           "degree": person.get("education", ""), "study_type": "unknown", "source_ids": []}],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {"name_birth": f"{safe_name}_{person.get('birth', '')}",
                            "name_birthplace": f"{safe_name}_{person.get('birthplace', '')}",
                            "official_profile_url": person.get("source", "")},
        },
        "current_status": {
            "current_post": person["current_post"], "current_org": person["current_org"],
            "administrative_rank": "县处级", "as_of": TODAY, "is_current_confirmed": True,
            "source_ids": ["S001"],
        },
        "career_timeline": [
            {"start": "unknown", "end": "present", "org": person["current_org"],
             "title": person["current_post"], "level": "县处级", "location": "武汉市江岸区",
             "system": "party" if "书记" in person["current_post"] else "government",
             "rank": "县处级", "is_key_promotion": False, "notes": "关键履历待补充",
             "confidence": "plausible", "source_ids": ["S001"]},
        ],
        "organizations": [], "relationships": [],
        "governance_record": [], "professional_profile": {},
        "work_style_and_personality": {}, "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "未发现已公开的负面纪律或审计信号", "date": TODAY,
             "confidence": "unverified", "source_ids": []}],
        "source_register": [
            {"id": "S001", "title": "江岸区人民政府门户网", "url": "https://www.jiangan.gov.cn/",
             "publisher": "江岸区人民政府", "published_at": "", "accessed_at": TODAY,
             "source_type": "official", "reliability": "high", "notes": "政府领导信息 + 融媒体时政新闻"}],
        "confidence_summary": {
            "identity": "confirmed" if person.get("birth") else "plausible",
            "current_role": "confirmed" if person.get("birth") else "plausible",
            "career_completeness": "complete" if person.get("birth") else "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "李世涛、姚彬等核心人物的出生信息、完整履历、入党/参工时间尚未获取"},
        "open_questions": [
            {"priority": "high", "question": f"{safe_name} 的出生年月、籍贯、教育、入党/参工时间",
             "why_it_matters": "构建完整个人图谱基础", "suggested_queries": [f"{safe_name} 简历 任前公示"],
             "last_attempted": TODAY},
        ],
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(person_json, f, ensure_ascii=False, indent=2)
    print(f"  Wrote {filepath}")


def main():
    print("=" * 60)
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  等级: 市辖区")
    print(f"  调查日期: {TODAY}")
    print(f"  信息来源: 江岸区人民政府网站 (www.jiangan.gov.cn)")
    print("=" * 60)

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=[r for r in relationships if r.get("person_b")],
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    # Person JSON (core figures only)
    core = [p for p in persons if p["id"] in (1001, 2001, 1002, 2002, 1003, 1004, 1005, 2003, 2004, 2005, 2006, 2007)]
    for p in core:
        person_json(p)

    print(f"\n  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  人物: {len(persons)} 人  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条  关系: {len(relationships)} 条")

    conn = sqlite3.connect(DB_PATH)
    for tab in ("persons", "organizations", "positions", "relationships"):
        n = conn.execute(f"SELECT COUNT(*) FROM {tab}").fetchone()[0]
        print(f"    {tab}: {n}")
    conn.close()

    print(f"\n✅ {SLUG} 数据构建完成。")


if __name__ == "__main__":
    main()