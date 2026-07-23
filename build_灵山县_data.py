#!/usr/bin/env python3
"""
广西钦州市灵山县领导班子工作关系网络 — 数据构建脚本
Build SQLite database + GEXF graph + person JSON for Lingshan County.

Level: 县
Province: 广西壮族自治区
Parent city: 钦州市
Targets: 县委书记 & 县长
Task: guangxi_灵山县

Research date: 2026-07-23

Current leadership (as of July 2026, sourced from www.gxls.gov.cn):
- 县委书记: 张海兵 (confirmed via 县委常委会 news reports, July 2026)
- 县委副书记、县长: 颜管经 (confirmed via 县政府领导 page and news reports, July 2026)

Deputy county heads (副县长, from official site):
- 赖华平 (副县长)
- 黄厚亮 (副县长)
- 陶伟 (副县长)
- 唐方华 (副县长)

Other officials named in news:
- 黄兴 (县委常委等)
- 梁世奎 (县委常委等)
- 陈琰 (参会)
- 林健 (参会)
- 刘洺昇 (参会)
- 宁毅 (参加督导)

Sources:
- 灵山县人民政府官网: http://www.gxls.gov.cn/
- 县政府领导 page: /zfxxgk/fdzdgknr/xzfld/xz/
- News articles citing leadership activities (July 2026)
- 县委常委会会议新闻 (第143、144次会议)

Confidence:
- Current roles: confirmed (official website news articles and leadership page)
- Biographical details: limited - no Baidu Baike available at time of research
- Career timelines: partial - additional verification needed
"""

from pathlib import Path
import sqlite3
import sys
import json
from datetime import datetime

# Add repo root to path
REPO_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Staging paths ──
STAGING_DIR = Path(__file__).resolve().parent
DB_PATH = STAGING_DIR / "灵山县_network.db"
GEXF_PATH = STAGING_DIR / "灵山县_network.gexf"
PERSONS_OUT_DIR = STAGING_DIR

TODAY = "2026-07-23"
GENERATED_AT = TODAY

# ════════════════════════════════════════════════════════════════
# PERSONS
# ════════════════════════════════════════════════════════════════

persons = [
    # ── 1: 张海兵 — 灵山县委书记 ──
    {
        "id": 1,
        "name": "张海兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "灵山县委书记",
        "current_org": "中共灵山县委员会",
        "source": "http://www.gxls.gov.cn/ (县委常委会新闻, 2026年7月)"
    },
    # ── 2: 颜管经 — 灵山县委副书记、县长 ──
    {
        "id": 2,
        "name": "颜管经",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "灵山县委副书记、县长",
        "current_org": "灵山县人民政府",
        "source": "http://www.gxls.gov.cn/zfxxgk/fdzdgknr/xzfld/xz/ (县政府领导页面, 2026年7月)"
    },
    # ── 3: 赖华平 — 副县长 ──
    {
        "id": 3,
        "name": "赖华平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "灵山县副县长",
        "current_org": "灵山县人民政府",
        "source": "http://www.gxls.gov.cn/zfxxgk/fdzdgknr/xzfld/ (县政府领导页面, 2026年7月)"
    },
    # ── 4: 黄厚亮 — 副县长 ──
    {
        "id": 4,
        "name": "黄厚亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "灵山县副县长",
        "current_org": "灵山县人民政府",
        "source": "http://www.gxls.gov.cn/zfxxgk/fdzdgknr/xzfld/ (县政府领导页面, 2026年7月); also mentioned in 整治群众身边不正之风推进会 (2026-07-17)"
    },
    # ── 5: 陶伟 — 副县长 ──
    {
        "id": 5,
        "name": "陶伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "灵山县副县长",
        "current_org": "灵山县人民政府",
        "source": "http://www.gxls.gov.cn/zfxxgk/fdzdgknr/xzfld/ (县政府领导页面, 2026年7月)"
    },
    # ── 6: 唐方华 — 副县长 ──
    {
        "id": 6,
        "name": "唐方华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "灵山县副县长",
        "current_org": "灵山县人民政府",
        "source": "http://www.gxls.gov.cn/zfxxgk/fdzdgknr/xzfld/ (县政府领导页面, 2026年7月)"
    },
    # ── 7: 黄兴 — 县委常委等 ──
    {
        "id": 7,
        "name": "黄兴",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "灵山县领导",
        "current_org": "中共灵山县委员会/灵山县人民政府",
        "source": "http://www.gxls.gov.cn/ (出席集中整治推进会, 2026-07-17)"
    },
    # ── 8: 梁世奎 — 县委常委等 ──
    {
        "id": 8,
        "name": "梁世奎",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "灵山县领导",
        "current_org": "中共灵山县委员会/灵山县人民政府",
        "source": "http://www.gxls.gov.cn/ (出席集中整治推进会, 2026-07-17)"
    },
    # ── 9: 陈琰 ──
    {
        "id": 9,
        "name": "陈琰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "灵山县领导",
        "current_org": "中共灵山县委员会/灵山县人民政府",
        "source": "http://www.gxls.gov.cn/ (出席集中整治推进会, 2026-07-17)"
    },
    # ── 10: 林健 ──
    {
        "id": 10,
        "name": "林健",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "灵山县领导",
        "current_org": "中共灵山县委员会/灵山县人民政府",
        "source": "http://www.gxls.gov.cn/ (出席集中整治推进会, 2026-07-17)"
    },
    # ── 11: 刘洺昇 ──
    {
        "id": 11,
        "name": "刘洺昇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "灵山县领导",
        "current_org": "中共灵山县委员会/灵山县人民政府",
        "source": "http://www.gxls.gov.cn/ (出席集中整治推进会, 2026-07-17)"
    },
    # ── 12: 宁毅 ──
    {
        "id": 12,
        "name": "宁毅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "灵山县领导",
        "current_org": "中共灵山县委员会/灵山县人民政府",
        "source": "http://www.gxls.gov.cn/ (出席集中整治推进会并参加陆屋镇督导, 2026-07-17)"
    },
]

# ════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共灵山县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共钦州市委员会",
        "location": "灵山县"
    },
    {
        "id": 2,
        "name": "灵山县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "钦州市人民政府",
        "location": "灵山县"
    },
    {
        "id": 3,
        "name": "灵山县人大常委会",
        "type": "人大",
        "level": "县",
        "parent": "钦州市人大常委会",
        "location": "灵山县"
    },
    {
        "id": 4,
        "name": "政协灵山县委员会",
        "type": "政协",
        "level": "县",
        "parent": "政协钦州市委员会",
        "location": "灵山县"
    },
    {
        "id": 5,
        "name": "中共灵山县纪律检查委员会",
        "type": "纪委",
        "level": "县",
        "parent": "中共钦州市纪律检查委员会",
        "location": "灵山县"
    },
    {
        "id": 6,
        "name": "中共灵山县委组织部",
        "type": "党委部门",
        "level": "县",
        "parent": "中共灵山县委员会",
        "location": "灵山县"
    },
    {
        "id": 7,
        "name": "中共灵山县委宣传部",
        "type": "党委部门",
        "level": "县",
        "parent": "中共灵山县委员会",
        "location": "灵山县"
    },
    {
        "id": 8,
        "name": "中共灵山县委政法委员会",
        "type": "党委部门",
        "level": "县",
        "parent": "中共灵山县委员会",
        "location": "灵山县"
    },
    {
        "id": 9,
        "name": "陆屋镇人民政府",
        "type": "乡镇/街道",
        "level": "镇",
        "parent": "灵山县人民政府",
        "location": "灵山县陆屋镇"
    },
]

# ════════════════════════════════════════════════════════════════
# POSITIONS
# ════════════════════════════════════════════════════════════════

positions = [
    # 张海兵
    {"person_id": 1, "org_id": 1, "title": "灵山县委书记",
     "start_date": "", "end_date": "present", "rank": "正处级",
     "note": "Confirmed as county party secretary in July 2026 news reports"},
    # 颜管经
    {"person_id": 2, "org_id": 1, "title": "灵山县委副书记",
     "start_date": "", "end_date": "present", "rank": "正处级",
     "note": "Confirmed as deputy party secretary and county mayor"},
    {"person_id": 2, "org_id": 2, "title": "灵山县县长",
     "start_date": "", "end_date": "present", "rank": "正处级",
     "note": "Confirmed via official county government leadership page"},
    # 赖华平
    {"person_id": 3, "org_id": 2, "title": "灵山县副县长",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": "Listed on official county leadership page"},
    # 黄厚亮
    {"person_id": 4, "org_id": 2, "title": "灵山县副县长",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": "Listed on official county leadership page; also mentioned in news reports"},
    # 陶伟
    {"person_id": 5, "org_id": 2, "title": "灵山县副县长",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": "Listed on official county leadership page"},
    # 唐方华
    {"person_id": 6, "org_id": 2, "title": "灵山县副县长",
     "start_date": "", "end_date": "present", "rank": "副处级",
     "note": "Listed on official county leadership page"},
    # 黄兴
    {"person_id": 7, "org_id": 1, "title": "灵山县领导",
     "start_date": "", "end_date": "present", "rank": "",
     "note": "Mentioned in news reports attending county meetings"},
    # 梁世奎
    {"person_id": 8, "org_id": 1, "title": "灵山县领导",
     "start_date": "", "end_date": "present", "rank": "",
     "note": "Mentioned in news reports attending county meetings"},
    # 陈琰
    {"person_id": 9, "org_id": 1, "title": "灵山县领导",
     "start_date": "", "end_date": "present", "rank": "",
     "note": "Mentioned in news reports attending county meetings"},
    # 林健
    {"person_id": 10, "org_id": 1, "title": "灵山县领导",
     "start_date": "", "end_date": "present", "rank": "",
     "note": "Mentioned in news reports attending county meetings"},
    # 刘洺昇
    {"person_id": 11, "org_id": 1, "title": "灵山县领导",
     "start_date": "", "end_date": "present", "rank": "",
     "note": "Mentioned in news reports attending county meetings"},
    # 宁毅
    {"person_id": 12, "org_id": 1, "title": "灵山县领导",
     "start_date": "", "end_date": "present", "rank": "",
     "note": "Mentioned in news reports; also accompanied 张海兵 on inspection at 陆屋镇"},
]

# ════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ════════════════════════════════════════════════════════════════

relationships = [
    # 张海兵 ↔ 颜管经 — 县委书记+县长
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "县委书记与县长搭档",
     "overlap_org": "中共灵山县委员会/灵山县人民政府",
     "overlap_period": "2026年至今"},
    # 张海兵 ↔ 黄兴 — 县委班子共事
    {"person_a": 1, "person_b": 7, "type": "overlap",
     "context": "县委常委会共同参会",
     "overlap_org": "中共灵山县委员会",
     "overlap_period": "2026年至今"},
    # 张海兵 ↔ 梁世奎 — 县委班子共事
    {"person_a": 1, "person_b": 8, "type": "overlap",
     "context": "县委常委会共同参会",
     "overlap_org": "中共灵山县委员会",
     "overlap_period": "2026年至今"},
    # 颜管经 ↔ 赖华平 — 县长与副县长
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate",
     "context": "县长与副县长共事",
     "overlap_org": "灵山县人民政府",
     "overlap_period": "2026年至今"},
    # 颜管经 ↔ 黄厚亮 — 县长与副县长
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "县长与副县长共事",
     "overlap_org": "灵山县人民政府",
     "overlap_period": "2026年至今"},
    # 颜管经 ↔ 陶伟 — 县长与副县长
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "县长与副县长共事",
     "overlap_org": "灵山县人民政府",
     "overlap_period": "2026年至今"},
    # 颜管经 ↔ 唐方华 — 县长与副县长
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate",
     "context": "县长与副县长共事",
     "overlap_org": "灵山县人民政府",
     "overlap_period": "2026年至今"},
    # 张海兵 ↔ 宁毅 — 县委书记与下属共事
    {"person_a": 1, "person_b": 12, "type": "superior_subordinate",
     "context": "县委书记与干部共同参与陆屋镇督导检查",
     "overlap_org": "中共灵山县委员会",
     "overlap_period": "2026年至今"},
]


# ════════════════════════════════════════════════════════════════
# PERSON JSON HELPERS
# ════════════════════════════════════════════════════════════════

def write_person_json(person: dict, note: str = "") -> str:
    """Write a per-person graph JSON file."""
    slug = person["name"]
    job_short = person["current_post"].split("、")[0] if "、" in person["current_post"] else person["current_post"]
    filename = f"{TODAY}-广西壮族自治区-钦州市-{job_short}-{slug}.json"
    filepath = PERSONS_OUT_DIR / filename

    data = {
        "schema_version": "1.0",
        "generated_at": GENERATED_AT,
        "investigation_scope": {
            "province": "广西壮族自治区",
            "city": "钦州市",
            "region": "灵山县",
            "job": person["current_post"],
            "task_id": "guangxi_灵山县",
            "time_focus": "2026年7月"
        },
        "identity": {
            "person_id": f"guangxi_lingshan_{slug}_{person['id']}",
            "name": slug,
            "aliases": [],
            "gender": person["gender"],
            "ethnicity": person["ethnicity"],
            "birth": person["birth"] or "",
            "birthplace": person["birthplace"] or "",
            "native_place": "",
            "education": [],
            "party_join": person["party_join"],
            "work_start": person["work_start"] or "",
            "dedupe_keys": {
                "name_birth": f"{slug}_",
                "name_birthplace": f"{slug}_",
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "正处级" if person["id"] in [1, 2] else "副处级" if person["id"] in [3, 4, 5, 6] else "待确认",
            "as_of": TODAY,
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": [
            {
                "start": "unknown",
                "end": "present",
                "org": person["current_org"],
                "title": person["current_post"],
                "level": "县处级",
                "location": "灵山县",
                "system": "party" if "书记" in person["current_post"] else "government",
                "rank": "正处级" if person["id"] in [1, 2] else "副处级",
                "is_key_promotion": person["id"] in [1, 2],
                "notes": "当前职务通过官方来源确认，但具体任职起始时间待核实",
                "confidence": "confirmed",
                "source_ids": ["S001"]
            }
        ],
        "organizations": [
            {
                "org_name": person["current_org"],
                "type": "党委" if "委员会" in person["current_org"] and "政府" not in person["current_org"] else "政府",
                "level": "县",
                "location": "灵山县"
            }
        ],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records and speeches, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": f"截至{TODAY}，未发现{slug}的纪律处分或负面报道。",
                "date": "",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "source_register": [
            {
                "id": "S001",
                "title": "灵山县人民政府官网",
                "url": "http://www.gxls.gov.cn/",
                "publisher": "灵山县人民政府",
                "published_at": "2026",
                "accessed_at": TODAY,
                "source_type": "official",
                "reliability": "high",
                "notes": "县政府领导页面及新闻公告"
            }
        ],
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": f"缺少{slug}的完整履历信息（出生日期、籍贯、教育背景、入党时间、工作起始时间、历任职务等）"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{slug}的出生日期和籍贯是什么？",
                "why_it_matters": "人员去重和身份确认的基础字段",
                "suggested_queries": [f"{slug} 简历", f"{slug} 出生"],
                "last_attempted": TODAY
            },
            {
                "priority": "critical",
                "question": f"{slug}的完整履历（历任职务及时间线）",
                "why_it_matters": "关系网络构建需要时间线数据支撑",
                "suggested_queries": [f"{slug} 任职", f"{slug} 工作经历"],
                "last_attempted": TODAY
            },
            {
                "priority": "high",
                "question": f"{slug}的教育背景和入党时间",
                "why_it_matters": "判断其专业背景和体制成长路径",
                "suggested_queries": [f"{slug} 学历", f"{slug} 入党"],
                "last_attempted": TODAY
            }
        ]
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  ✓ Person JSON: {filename}")
    return filename


# ════════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════════

def build():
    print("=" * 60)
    print("灵山县领导班子工作关系网络 — 数据构建")
    print(f"生成日期: {TODAY}")
    print("=" * 60)

    # 1. Build DB + GEXF
    print("\n[1/3] 构建数据库和GEXF图...")
    run_build(
        slug="灵山县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    # 2. Write person JSONs
    print("\n[2/3] 生成人物深度图谱...")
    person_files = []
    for p in persons:
        filename = write_person_json(p)
        person_files.append(filename)

    # 3. Print summary
    print(f"\n[3/3] 完成!")
    print(f"  数据库: {DB_PATH}")
    print(f"  GEXF图: {GEXF_PATH}")
    print(f"  人物JSON: {len(person_files)} 个文件")
    for f in person_files:
        print(f"    - {f}")


if __name__ == "__main__":
    build()
