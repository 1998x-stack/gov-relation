#!/usr/bin/env python3
"""山西省大同市灵丘县领导班子工作关系网络 — 数据构建脚本。

等级: 县
调查日期: 2026-07-26
信息来源: 灵丘县人民政府网站 (www.lingqiu.gov.cn)
"""

from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

import sqlite3  # noqa: used indirectly via runner

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Config ────────────────────────────────────────────────────────────────────
SLUG = "灵丘县"
TODAY = "2026-07-26"
STAGING = Path(__file__).resolve().parent

DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# ── Persons ────────────────────────────────────────────────────────────────────
# Person IDs: 1xxx = party committee, 2xxx = government

persons = [
    # ═══════════════════════════════════════════════════════════════════════
    # 1. 周鹏 — 市委常委、县委书记
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1001,
        "name": "周鹏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、县委书记",
        "current_org": "中共灵丘县委员会 / 中共大同市委",
        "source": "https://www.lingqiu.gov.cn/lqxrmzfz/dtyw/202607/f9d301ac3e074e33a4773d51f9a713dd.shtml",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 2. 陈月祥 — 县委副书记、县政府党组书记、代县长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1002,
        "name": "陈月祥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年12月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记、县政府党组书记、代县长",
        "current_org": "中共灵丘县委员会 / 灵丘县人民政府",
        "source": "https://www.lingqiu.gov.cn/lqxrmzfz/llx/szfld.shtml",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 3. 李灵杰 — 县委常委、县政府党组副书记、副县长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1003,
        "name": "李灵杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年8月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县政府党组副书记、副县长",
        "current_org": "中共灵丘县委员会 / 灵丘县人民政府",
        "source": "https://www.lingqiu.gov.cn/lqxrmzfz/szf/zfld.shtml",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 4. 李文杰 — 县委常委、县政府党组成员、副县长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1004,
        "name": "李文杰",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1976年6月",
        "birthplace": "",
        "education": "在职研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县政府党组成员、副县长",
        "current_org": "中共灵丘县委员会 / 灵丘县人民政府",
        "source": "https://www.lingqiu.gov.cn/lqxrmzfz/szf/zfld.shtml",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 5. 张洪玉 — 县委常委、县政府党组成员、副县长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1005,
        "name": "张洪玉",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1984年4月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县政府党组成员、副县长",
        "current_org": "中共灵丘县委员会 / 灵丘县人民政府",
        "source": "https://www.lingqiu.gov.cn/lqxrmzfz/szf/zfld.shtml",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 6. 钟灵臣 — 县政府副县长（无党派）
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 2001,
        "name": "钟灵臣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年8月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府副县长",
        "current_org": "灵丘县人民政府",
        "source": "https://www.lingqiu.gov.cn/lqxrmzfz/szf/zfld.shtml",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 7. 赵斌 — 县政府党组成员、副县长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 2002,
        "name": "赵斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年9月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府党组成员、副县长",
        "current_org": "灵丘县人民政府",
        "source": "https://www.lingqiu.gov.cn/lqxrmzfz/szf/zfld.shtml",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 8. 武文成 — 县政府党组成员、副县长，县公安局党委书记、局长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 2003,
        "name": "武文成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年10月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府党组成员、副县长，县公安局党委书记、局长",
        "current_org": "灵丘县人民政府 / 灵丘县公安局",
        "source": "https://www.lingqiu.gov.cn/lqxrmzfz/szf/zfld.shtml",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 9. 任亮 — 县政府党组成员、副县长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 2004,
        "name": "任亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1989年1月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府党组成员、副县长",
        "current_org": "灵丘县人民政府",
        "source": "https://www.lingqiu.gov.cn/lqxrmzfz/szf/zfld.shtml",
    },
]

# ── Organizations ──────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共灵丘县委员会", "type": "党委", "level": "县处级", "parent": "中共大同市委", "location": "大同市灵丘县"},
    {"id": 2, "name": "灵丘县人民政府", "type": "政府", "level": "县处级", "parent": "大同市人民政府", "location": "大同市灵丘县"},
    {"id": 3, "name": "中共灵丘县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共大同市纪律检查委员会 / 中共灵丘县委员会", "location": "大同市灵丘县"},
    {"id": 4, "name": "灵丘县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "", "location": "大同市灵丘县"},
    {"id": 5, "name": "政协灵丘县委员会", "type": "政协", "level": "县处级", "parent": "", "location": "大同市灵丘县"},
    {"id": 6, "name": "灵丘县公安局", "type": "政府", "level": "乡科级", "parent": "灵丘县人民政府 / 大同市公安局", "location": "大同市灵丘县"},
    {"id": 7, "name": "中共大同市委", "type": "党委", "level": "地厅级", "parent": "中共山西省委", "location": "大同市"},
]

# ── Positions ──────────────────────────────────────────────────────────────────

positions = [
    # 周鹏
    {"person_id": 1001, "org_id": 7, "title": "市委常委", "start": "", "end": "", "rank": "副厅级", "note": "大同市委常委"},
    {"person_id": 1001, "org_id": 1, "title": "县委书记", "start": "", "end": "", "rank": "正县处级", "note": "主持县委全面工作"},
    # 陈月祥
    {"person_id": 1002, "org_id": 1, "title": "县委副书记", "start": "", "end": "", "rank": "副县处级", "note": ""},
    {"person_id": 1002, "org_id": 2, "title": "县政府党组书记、代县长", "start": "", "end": "", "rank": "正县处级", "note": "主持县人民政府全面工作，负责审计方面的工作"},
    # 李灵杰
    {"person_id": 1003, "org_id": 1, "title": "县委常委", "start": "", "end": "", "rank": "副县处级", "note": ""},
    {"person_id": 1003, "org_id": 2, "title": "县政府党组副书记、副县长", "start": "", "end": "", "rank": "副县处级", "note": "协助县长主持县人民政府日常工作"},
    # 李文杰
    {"person_id": 1004, "org_id": 1, "title": "县委常委", "start": "", "end": "", "rank": "副县处级", "note": ""},
    {"person_id": 1004, "org_id": 2, "title": "县政府党组成员、副县长", "start": "", "end": "", "rank": "副县处级", "note": "负责文化旅游、卫健体育、市场监管等"},
    # 张洪玉
    {"person_id": 1005, "org_id": 1, "title": "县委常委", "start": "", "end": "", "rank": "副县处级", "note": ""},
    {"person_id": 1005, "org_id": 2, "title": "县政府党组成员、副县长", "start": "", "end": "", "rank": "副县处级", "note": "负责民政、人社、退役军人事务等"},
    # 钟灵臣
    {"person_id": 2001, "org_id": 2, "title": "副县长", "start": "", "end": "", "rank": "副县处级", "note": "无党派；负责交通、能源、通用航空、生态环境等"},
    # 赵斌
    {"person_id": 2002, "org_id": 2, "title": "党组成员、副县长", "start": "", "end": "", "rank": "副县处级", "note": "负责国土空间规划、城乡建设、城市管理等"},
    # 武文成
    {"person_id": 2003, "org_id": 2, "title": "党组成员、副县长", "start": "", "end": "", "rank": "副县处级", "note": ""},
    {"person_id": 2003, "org_id": 6, "title": "党委书记、局长", "start": "", "end": "", "rank": "乡科级正职", "note": "主持县公安局全面工作"},
    # 任亮
    {"person_id": 2004, "org_id": 2, "title": "党组成员、副县长", "start": "", "end": "", "rank": "副县处级", "note": "负责数据、工信、商务、国企国资监管等"},
]

# ── Relationships ──────────────────────────────────────────────────────────────

relationships = [
    # 周鹏 ↔ 陈月祥: 党政一把手搭档
    {"person_a": 1001, "person_b": 1002, "type": "overlap", "context": "县委书记与代县长党政工作搭档", "overlap_org": "灵丘县", "overlap_period": ""},
    # 周鹏 ↔ 李灵杰: 书记与常委副县长（陪同防汛调研）
    {"person_a": 1001, "person_b": 1003, "type": "overlap", "context": "县委书记与县委常委、副县长工作搭档；周鹏调研防汛时李灵杰参加", "overlap_org": "中共灵丘县委/县政府", "overlap_period": ""},
    # 陈月祥 ↔ 李灵杰: 代县长与党组副书记
    {"person_a": 1002, "person_b": 1003, "type": "overlap", "context": "代县长与县政府党组副书记工作搭档", "overlap_org": "灵丘县人民政府", "overlap_period": ""},
    # 周鹏 ↔ 李文杰: 书记与女常委
    {"person_a": 1001, "person_b": 1004, "type": "overlap", "context": "县委书记与县委常委工作搭档", "overlap_org": "中共灵丘县委", "overlap_period": ""},
    # 陈月祥 ↔ 李文杰: 代县长与女副县长
    {"person_a": 1002, "person_b": 1004, "type": "overlap", "context": "代县长与副县长工作搭档", "overlap_org": "灵丘县人民政府", "overlap_period": ""},
    # 周鹏 ↔ 张洪玉: 书记与女常委
    {"person_a": 1001, "person_b": 1005, "type": "overlap", "context": "县委书记与县委常委工作搭档", "overlap_org": "中共灵丘县委", "overlap_period": ""},
    # 陈月祥 ↔ 张洪玉: 代县长与副县长
    {"person_a": 1002, "person_b": 1005, "type": "overlap", "context": "代县长与副县长工作搭档", "overlap_org": "灵丘县人民政府", "overlap_period": ""},
    # 陈月祥 ↔ 钟灵臣: 代县长与无党派副县长
    {"person_a": 1002, "person_b": 2001, "type": "overlap", "context": "代县长与副县长工作搭档", "overlap_org": "灵丘县人民政府", "overlap_period": ""},
    # 陈月祥 ↔ 赵斌: 代县长与副县长
    {"person_a": 1002, "person_b": 2002, "type": "overlap", "context": "代县长与副县长工作搭档", "overlap_org": "灵丘县人民政府", "overlap_period": ""},
    # 陈月祥 ↔ 武文成: 代县长与公安局长
    {"person_a": 1002, "person_b": 2003, "type": "overlap", "context": "代县长与副县长、公安局长工作搭档", "overlap_org": "灵丘县人民政府", "overlap_period": ""},
    # 陈月祥 ↔ 任亮: 代县长与副县长
    {"person_a": 1002, "person_b": 2004, "type": "overlap", "context": "代县长与副县长工作搭档", "overlap_org": "灵丘县人民政府", "overlap_period": ""},
    # 李灵杰 ↔ 李文杰: 两位常委副县长
    {"person_a": 1003, "person_b": 1004, "type": "overlap", "context": "两位县委常委、副县长工作搭档", "overlap_org": "中共灵丘县委/县政府", "overlap_period": ""},
    # 李灵杰 ↔ 张洪玉: 两位常委副县长
    {"person_a": 1003, "person_b": 1005, "type": "overlap", "context": "两位县委常委、副县长工作搭档", "overlap_org": "中共灵丘县委/县政府", "overlap_period": ""},
]


# ═══════════════════════════════════════════════════════════════════════════════
# Person JSON helpers
# ═══════════════════════════════════════════════════════════════════════════════

def make_source_register():
    return [
        {"id": "S001", "title": "灵丘县政府网站-县长页-陈月祥", "url": "https://www.lingqiu.gov.cn/lqxrmzfz/llx/szfld.shtml", "publisher": "灵丘县人民政府", "published_at": "", "accessed_at": TODAY, "source_type": "official", "reliability": "high", "notes": "陈月祥官方简历"},
        {"id": "S002", "title": "灵丘县政府网站-县政府领导页", "url": "https://www.lingqiu.gov.cn/lqxrmzfz/szf/zfld.shtml", "publisher": "灵丘县人民政府", "published_at": "", "accessed_at": TODAY, "source_type": "official", "reliability": "high", "notes": "确认县政府领导构成"},
        {"id": "S003", "title": "周鹏调研督导防汛工作", "url": "https://www.lingqiu.gov.cn/lqxrmzfz/dtyw/202607/f9d301ac3e074e33a4773d51f9a713dd.shtml", "publisher": "灵丘县人民政府", "published_at": "2026-07-23", "accessed_at": TODAY, "source_type": "official", "reliability": "high", "notes": "确认周鹏为市委常委、县委书记；李灵杰以县委常委、副县长身份参加"},
        {"id": "S004", "title": "周鹏\"七一\"前夕走访慰问生活困难党员", "url": "https://www.lingqiu.gov.cn/lqxrmzfz/tpxw/202607/8f9a9cb6e34c4577bd155a1596def60c.shtml", "publisher": "灵丘县人民政府", "published_at": "2026-07", "accessed_at": TODAY, "source_type": "official", "reliability": "high", "notes": "确认周鹏为市委常委、县委书记"},
        {"id": "S005", "title": "张强调研广灵灵丘", "url": "https://www.lingqiu.gov.cn/lqxrmzfz/dtyw/202606/bbf8f2422b80417e979b6307bf700964.shtml", "publisher": "灵丘县人民政府", "published_at": "2026-06", "accessed_at": TODAY, "source_type": "official", "reliability": "high", "notes": "确认周鹏为市委常委、灵丘县委书记"},
        {"id": "S006", "title": "灵丘县人民政府首页", "url": "https://www.lingqiu.gov.cn/", "publisher": "灵丘县人民政府", "published_at": "", "accessed_at": TODAY, "source_type": "official", "reliability": "high", "notes": "页面顶部确认领导信息"},
    ]


def make_person_json(person, timeline, rels, source_register):
    """Create a person graph JSON following the person_graph_json.md schema."""
    today_short = TODAY.replace("-", "")
    return {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "山西省",
            "city": "大同市",
            "region": "灵丘县",
            "job": person["current_post"],
            "task_id": "shanxi_灵丘县",
            "time_focus": "2026"
        },
        "identity": {
            "person_id": f"lingqiuxian_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [{"period": "", "institution": "", "major": "", "degree": person.get("education", ""), "study_type": "unknown", "source_ids": []}] if person.get("education") else [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person.get('birth', '')}",
                "name_birthplace": f"{person['name']}_{person.get('birthplace', '')}",
                "official_profile_url": person.get("source", "")
            }
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "副厅级" if person["id"] == 1001 else "正县处级" if person["id"] == 1002 else "副县处级",
            "as_of": TODAY,
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002", "S003"]
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": rels,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "partial",
            "relationship_confidence": "medium",
            "biggest_gap": "详细履历（早期职业经历、教育背景、政治面貌时间等）尚未获取"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{person['name']}的完整履历（早期职业经历、教育背景、入党时间、历任职务及起止时间）",
                "why_it_matters": "核心领导的履历是关系网络分析的基础",
                "suggested_queries": [f"{person['name']} 简历 灵丘"],
                "last_attempted": TODAY
            }
        ]
    }


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("  山西省大同市灵丘县领导班子工作关系网络")
    print("  等级: 县")
    print("  调查日期: 2026-07-26（首次调查）")
    print("  信息来源: 灵丘县政府网站")
    print("=" * 60)

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
    print(f"\n✅ 灵丘县数据构建完成。")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

    # ── Generate Person Graph JSONs ──
    print("\n--- Generating Person Graph JSONs ---")
    source_register = make_source_register()

    # 1. 周鹏 (市委书记、县委书记)
    zp_timeline = [
        {"start": "", "end": "", "org": "中共大同市委", "title": "市委常委", "notes": "兼任灵丘县委书记", "confidence": "confirmed", "source_ids": ["S003", "S005"]},
        {"start": "", "end": "", "org": "中共灵丘县委员会", "title": "县委书记", "notes": "主持县委全面工作", "confidence": "confirmed", "source_ids": ["S003", "S004"]},
    ]
    zp_relationships = [
        {"person": "陈月祥", "person_id": "lingqiuxian_陈月祥", "relationship_type": "overlap", "strength": "strong", "evidence": "县委书记与代县长党政工作搭档", "overlap_org": "灵丘县", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
        {"person": "李灵杰", "person_id": "lingqiuxian_李灵杰", "relationship_type": "overlap", "strength": "strong", "evidence": "县委书记与县委常委、副县长工作搭档；周鹏调研防汛时李灵杰参加", "overlap_org": "中共灵丘县委/县政府", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]},
    ]
    zp_json = make_person_json(persons[0], zp_timeline, zp_relationships, source_register)
    zp_path = STAGING / f"{TODAY}-山西省-大同市-县委书记-周鹏.json"
    with open(zp_path, "w", encoding="utf-8") as f:
        json.dump(zp_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {zp_path.name}")

    # 2. 陈月祥 (代县长)
    cyx_timeline = [
        {"start": "", "end": "", "org": "中共灵丘县委员会", "title": "县委副书记", "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
        {"start": "", "end": "", "org": "灵丘县人民政府", "title": "县政府党组书记、代县长", "notes": "主持县人民政府全面工作，负责审计方面的工作；1978年12月生，汉族，大学学历，中共党员", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
    ]
    cyx_relationships = [
        {"person": "周鹏", "person_id": "lingqiuxian_周鹏", "relationship_type": "overlap", "strength": "strong", "evidence": "代县长与县委书记党政工作搭档", "overlap_org": "灵丘县", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
        {"person": "李灵杰", "person_id": "lingqiuxian_李灵杰", "relationship_type": "overlap", "strength": "strong", "evidence": "代县长与县政府党组副书记工作搭档", "overlap_org": "灵丘县人民政府", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
        {"person": "李文杰", "person_id": "lingqiuxian_李文杰", "relationship_type": "overlap", "strength": "strong", "evidence": "代县长与副县长工作搭档", "overlap_org": "灵丘县人民政府", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
        {"person": "张洪玉", "person_id": "lingqiuxian_张洪玉", "relationship_type": "overlap", "strength": "strong", "evidence": "代县长与副县长工作搭档", "overlap_org": "灵丘县人民政府", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
        {"person": "钟灵臣", "person_id": "lingqiuxian_钟灵臣", "relationship_type": "overlap", "strength": "strong", "evidence": "代县长与副县长工作搭档", "overlap_org": "灵丘县人民政府", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
        {"person": "赵斌", "person_id": "lingqiuxian_赵斌", "relationship_type": "overlap", "strength": "strong", "evidence": "代县长与副县长工作搭档", "overlap_org": "灵丘县人民政府", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
        {"person": "武文成", "person_id": "lingqiuxian_武文成", "relationship_type": "overlap", "strength": "strong", "evidence": "代县长与副县长、公安局长工作搭档", "overlap_org": "灵丘县人民政府", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
        {"person": "任亮", "person_id": "lingqiuxian_任亮", "relationship_type": "overlap", "strength": "strong", "evidence": "代县长与副县长工作搭档", "overlap_org": "灵丘县人民政府", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
    ]
    cyx_json = make_person_json(persons[1], cyx_timeline, cyx_relationships, source_register)
    cyx_path = STAGING / f"{TODAY}-山西省-大同市-代县长-陈月祥.json"
    with open(cyx_path, "w", encoding="utf-8") as f:
        json.dump(cyx_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {cyx_path.name}")

    print(f"\n所有 Person Graph JSONs 已生成到: {STAGING}")


if __name__ == "__main__":
    main()
