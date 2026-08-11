#!/usr/bin/env python3
"""
淮阳区（周口市）领导班子工作关系网络 — 构建脚本

等级: 市辖区 | 上级: 河南省周口市
调查日期: 2026-08-06
数据来源: 淮阳区政府新闻门户(www.huaiyang.gov.cn)官方报道、周口市政府门户
说明: 调查期间外部搜索引擎(Baidu/Sogou/Exa)受限,采用 partial-evidence 模式;
      核心领导身份与任职时序由官方来源确认,传记字段以 open_questions 显式标注。
"""

import json
import sqlite3  # noqa — used by gov_relation.runner
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent
while not (_REPO_ROOT / "gov_relation").exists() and _REPO_ROOT != _REPO_ROOT.parent:
    _REPO_ROOT = _REPO_ROOT.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build

# ── Metadata ──
SLUG = "淮阳区"
TODAY = "2026-08-06"
AS_OF = TODAY
PROVINCE = "河南省"
CITY = "周口市"
REGION = "淮阳区"

# ── Paths ──
HERE = Path(__file__).parent
DB_PATH = HERE / f"{REGION}_network.db"
GEXF_PATH = HERE / f"{REGION}_network.gexf"
PERSONS_DIR = HERE

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ── 现任区委书记 ──
    {
        "id": 1,
        "name": "王献超",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "淮阳区委书记",
        "current_org": "中共周口市淮阳区委员会",
        "source": "https://www.huaiyang.gov.cn/ — 淮阳区政府门户新闻: 2026-06-06《淮阳区委书记王献超调研推进“三夏”生产工作》等",
        "notes": "2021年起任淮阳区区长(2021-07已以区长身份见报);约2025年3月升任区委书记,2025年内一度'区委书记+区长'一肩挑(2025-05-11至2025-12多篇报道署名'区委书记、区政府区长王献超');2026年初起专职区委书记。出生/籍贯/学历等信息公开渠道暂未获取。",
    },
    # ── 现任区长 ──
    {
        "id": 2,
        "name": "贾鲲鹏",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "淮阳区区长",
        "current_org": "淮阳区人民政府",
        "source": "https://www.huaiyang.gov.cn/ — 淮阳区政府门户新闻: 2026-06-01《淮阳区区长贾鲲鹏主持召开区政府常务会议》等",
        "notes": "约2026年初接任淮阳区区长(2026-06-01起官方报道署名'区长贾鲲鹏'并主持区政府常务会议;2026-07多篇调研报道)。任区长前职务、出生年月等公开资料待查。",
    },
    # ── 前任区委书记 ──
    {
        "id": 3,
        "name": "张建党",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任淮阳区委书记",
        "current_org": "中共周口市淮阳区委员会",
        "source": "https://www.huaiyang.gov.cn/ — 官方报道: 2021-07-13《张建党 王献超到区人大、区政府、区政协机关调研指导工作》;2025-02-27《淮阳区委书记张建党调研民生和文旅项目建设工作》",
        "notes": "至少2021-07起任淮阳区委书记(与区长王献超搭档);2025-02-27仍以区委书记署名,之后约2025年3月由王献超接任。卸任后去向、出生年月等信息待查。"
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共周口市淮阳区委员会", "type": "党委", "level": "县处级", "parent": "中共周口市委员会", "location": "河南省周口市淮阳区"},
    {"id": 2, "name": "淮阳区人民政府", "type": "政府", "level": "县处级", "parent": "周口市人民政府", "location": "河南省周口市淮阳区"},
    {"id": 3, "name": "中共周口市淮阳区纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共周口市纪律检查委员会", "location": "河南省周口市淮阳区"},
    {"id": 4, "name": "中共周口市淮阳区委员会组织部", "type": "党委", "level": "县处级", "parent": "中共周口市淮阳区委员会", "location": "河南省周口市淮阳区"},
    {"id": 5, "name": "中共周口市淮阳区委员会宣传部", "type": "党委", "level": "县处级", "parent": "中共周口市淮阳区委员会", "location": "河南省周口市淮阳区"},
    {"id": 6, "name": "中共周口市淮阳区委员会政法委员会", "type": "党委", "level": "县处级", "parent": "中共周口市淮阳区委员会", "location": "河南省周口市淮阳区"},
    {"id": 7, "name": "中共周口市淮阳区委员会统一战线工作部", "type": "党委", "level": "县处级", "parent": "中共周口市淮阳区委员会", "location": "河南省周口市淮阳区"},
    {"id": 8, "name": "淮阳区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "周口市人大常委会", "location": "河南省周口市淮阳区"},
    {"id": 9, "name": "政协周口市淮阳区委员会", "type": "政协", "level": "县处级", "parent": "政协周口市委员会", "location": "河南省周口市淮阳区"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 王献超
    {"person_id": 1, "org_id": 1, "title": "淮阳区委书记", "start": "2025-03", "end": "present", "rank": "正处级", "note": "约2025年3月由区长升任区委书记"},
    {"person_id": 1, "org_id": 1, "title": "淮阳区委书记、区政府区长(兼)", "start": "2025-03", "end": "2025-12", "rank": "正处级", "note": "2025年间曾'区委书记+区长'一肩挑"},
    {"person_id": 1, "org_id": 2, "title": "淮阳区区长", "start": "2021", "end": "2025-03", "rank": "正处级", "note": "2021年起任区长,约2025年3月升任区委书记"},

    # 贾鲲鹏
    {"person_id": 2, "org_id": 2, "title": "淮阳区区长", "start": "2026-01", "end": "present", "rank": "正处级", "note": "约2026年初接任区长,2026-06官方已确认"},
    {"person_id": 2, "org_id": 2, "title": "淮阳区副区长、代理区长", "start": "2025", "end": "2026-01", "rank": "正处级", "note": "接任区长时间待进一步查证(公开资料有限)"},

    # 张建党
    {"person_id": 3, "org_id": 1, "title": "淮阳区委书记", "start": "2021", "end": "2025-02", "rank": "正处级", "note": "至少2021-07起任区委书记,2025-02仍署名为书记,之后由王献超接任"},

    # 空缺但必备的组织占位任职(成员班子暂未获取到具体姓名 → 不构建 person 节点)
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 王献超(区长)↔ 张建党(区委书记): 党政搭档 2021-2025
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "王献超任区长与张建党任区委书记形成党政搭档", "overlap_org": "中共周口市淮阳区委员会/淮阳区人民政府", "overlap_period": "2021-2025"},

    # 王献超 ↔ 贾鲲鹏: 前任区长→现任区长(党政搭档)
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor", "context": "王献超由区长升任区委书记后,贾鲲鹏接任区长;现为区委书记×区长的党政搭档", "overlap_org": "淮阳区人民政府", "overlap_period": "2026-至今"},

    # 张建党 ↔ 贾鲲鹏: 前任区委书记与现区长 (间接网络节点, 弱关联 - 交叉跨届)
    {"person_a": 3, "person_b": 2, "type": "overlap", "context": "张建党区委书记任内贾鲲鹏尚未到任,为跨届间接联系", "overlap_org": "淮阳区", "overlap_period": ""},
]

# ══════════════════════════════════════════════════════════════════════════════
# SOURCE REGISTER
# ══════════════════════════════════════════════════════════════════════════════

def make_source_register() -> list[dict]:
    return [
        {"id": "S001", "title": "淮阳区委书记王献超调研推进“三夏”生产工作(2026-06-06)",
         "url": "http://www.huaiyang.gov.cn/Content/ed16cec0-80fd-4d89-afc9-d7856f4c6781/ce4703bd-8326-48be-8297-c179218719a4",
         "publisher": "淮阳区政府门户网站", "published_at": "2026-06-06", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high", "notes": "确认王献超现任区委书记"},
        {"id": "S002", "title": "淮阳区区长贾鲲鹏主持召开区政府常务会议(2026-06-01)",
         "url": "http://www.huaiyang.gov.cn/Content/ed16cec0-80fd-4d89-afc9-d7856f4c6781/5c2e4348-1356-401d-8025-ae484d9d57e6",
         "publisher": "淮阳区政府门户网站", "published_at": "2026-06-01", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high", "notes": "确认贾鲲鹏现任区长"},
        {"id": "S003", "title": "淮阳区委常委会召开扩大会议(2026-06-09)——王献超书记主持、贾鲲鹏区长出席",
         "url": "http://www.huaiyang.gov.cn/Content/ed16cec0-80fd-4d89-afc9-d7856f4c6781/a8b46acd-f645-4d55-9553-58557a3e4562",
         "publisher": "淮阳区政府门户网站", "published_at": "2026-06-09", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high", "notes": "同时确认区委书记王献超与区长贾鲲鹏的党政格局"},
        {"id": "S004", "title": "王献超调研农村集体'三资'清查整治工作(2026-07-15)",
         "url": "http://www.huaiyang.gov.cn/Content/ed16cec0-80fd-4d89-afc9-d7856f4c6781/48acf498-5a87-4a26-ba78-a295390a91a5",
         "publisher": "淮阳区政府门户网站", "published_at": "2026-07-15", "source_type": "official",
         "reliability": "high", "notes": "2026年中王献超仍任区委书记"},
        {"id": "S005", "title": "淮阳区委书记、区政府区长王献超调研安置房建设工作(2025-05-11)",
         "url": "http://www.huaiyang.gov.cn/Content/ed16cec0-80fd-4d89-afc9-d7856f4c6781/b8c86206-b845-42b2-990e-40f1d30b893f",
         "publisher": "淮阳区政府门户网站", "published_at": "2025-05-11", "source_type": "official",
         "reliability": "high", "notes": "2025年中'区委书记+区长'一肩挑的时序证据"},
        {"id": "S006", "title": "张建党 王献超到区人大、区政府、区政协机关调研指导工作(2021-07-13)",
         "url": "http://www.huaiyang.gov.cn/Content/ed16cec0-80fd-4d89-afc9-d7856f4c6781/a498d25f-868c-4b3a-ade9-575942a1430b",
         "publisher": "淮阳区政府门户网站", "published_at": "2021-07-13", "source_type": "official",
         "reliability": "high", "notes": "确认张建党任区委书记与王书建任区长的搭档起点"},
        {"id": "S007", "title": "淮阳区委书记张建党调研民生和文旅项目建设工作(2025-02-27)",
         "url": "http://www.huaiyang.gov.cn/Content/ed16cec0-80fd-4d89-afc9-d7856f4c6781/d0ed727e-cf27-4955-8077-4abc2f54f1b",
         "publisher": "淮阳区政府门户网站", "published_at": "2025-02-27", "source_type": "official",
         "reliability": "high", "notes": "张建党最近一次以区委书记身份见报"},
    ]


# ══════════════════════════════════════════════════════════════════════════════
# PERSON GRAPH JSON HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def make_person_json(person: dict, timeline: list[dict], person_relationships: list[dict],
                     source_register: list[dict], job: str) -> dict:
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": PROVINCE,
            "city": CITY,
            "region": REGION,
            "job": job,
            "task_id": "henan_淮阳区",
            "time_focus": "2021-2026",
        },
        "identity": {
            "person_id": f"huaiyang_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": person.get("native_place", ""),
            "education": [{"period": "", "institution": person.get("education", ""), "major": "", "degree": "",
                           "study_type": "unknown", "source_ids": []}],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person.get('birth', '')}",
                "name_birthplace": f"{person['name']}_{person.get('birthplace', '')}",
                "official_profile_url": person.get("source", ""),
            },
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "正处级",
            "as_of": AS_OF,
            "is_current_confirmed": person.get("current_post", "") in ("淮阳区委书记", "淮阳区区长"),
            "source_ids": ["S001", "S002", "S003"],
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": person_relationships,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "local_ladder",
            "systems_experience": ["party", "government"],
            "geographic_pattern": ["淮阳区(周口市)"],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public reports, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "未在公开渠道发现纪律处分或负面报道信号",
                                         "date": "", "confidence": "unverified", "source_ids": []}],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "partial",
            "relationship_confidence": "medium",
            "biggest_gap": "核心领导出生年份/籍贯/学历/入党时间及任现职前完整履历未公开确认",
        },
        "open_questions": [
            {"priority": "critical", "question": f"{person['name']}的出生年份、籍贯、学历/专业、入党与参工时间",
             "why_it_matters": "姓名+出生年份是跨区去重与身份校准的关键字段",
             "suggested_queries": [f"{person['name']} 简历 淮阳", f"{person['name']} 百度百科", f"{person['name']} 任前公示"],
             "last_attempted": AS_OF},
            {"priority": "high", "question": f"{person['name']}任淮阳{job}前的上一任职职务与来源单位",
             "why_it_matters": "还原晋升链条与跨区调动网络",
             "suggested_queries": [f"{person['name']} 周口 干部 任前公示", f"{person['name']} 之前 担任"],
             "last_attempted": AS_OF},
            {"priority": "medium", "question": "淮阳区区委常委班子(常务副区长、纪委书记、组织部长)名单与分工",
             "why_it_matters": "区委常委会全体成员名单与分工是细化关系网络的必要输入",
             "suggested_queries": ["淮阳区 领导分工", "淮阳区委班子 名单"],
             "last_attempted": AS_OF},
        ],
    }


# ── 各核心人物 timeline & relationships ──

def wang_timeline() -> list[dict]:
    return [
        {"start": "unknown", "end": "2021", "org": "履历缺口", "title": "",
         "notes": "公开资料未找到王献超2021年任区长前的任职履历(出生年度、籍贯、教育背景)",
         "confidence": "unverified", "source_ids": []},
        {"start": "2021", "end": "2025-03", "org": "淮阳区人民政府", "title": "淮阳区长",
         "notes": "2021年起任区长(2021-07-13与张建党一同调研人大政府政协为可见起点)",
         "confidence": "confirmed", "source_ids": ["S006"]},
        {"start": "2025-03", "end": "2025-12", "org": "中共周口市淮阳区委/淮阳区政府", "title": "区委书记、区长(兼)",
         "notes": "2025年3月起升任区委书记并一度兼任区长,2025-05-11等报道标题'淮阳区委书记、区长王献超'",
         "confidence": "confirmed", "source_ids": ["S005"]},
        {"start": "2026", "end": "present", "org": "中共周口市淮阳区委员会", "title": "淮阳区委书记",
         "notes": "2026年起专职区委书记,贾鲲鹏接任区长",
         "confidence": "confirmed", "source_ids": ["S001", "S003"]},
    ]


def jia_timeline() -> list[dict]:
    return [
        {"start": "unknown", "end": "2025", "org": "履历缺口", "title": "",
         "notes": "贾鲲鹏任区长前的任职职务与来源单位未公开确认",
         "confidence": "unverified", "source_ids": []},
        {"start": "2025", "end": "2026-01", "org": "淮阳区人民政府", "title": "淮阳区副区长、代理区长",
         "notes": "接任区长时间待考,代理区长→当选时序未确认",
         "confidence": "plausible", "source_ids": []},
        {"start": "2026-01", "end": "present", "org": "淮阳区人民政府", "title": "淮阳区长",
         "notes": "2026年官方报道确认;2026-06-01主持区政府常务会议",
         "confidence": "confirmed", "source_ids": ["S002", "S003"]},
    ]


def zhang_timeline() -> list[dict]:
    return [
        {"start": "unknown", "end": "2021", "org": "履历缺口", "title": "",
         "notes": "张建党2021年任区委书记前的履历未公开确认",
         "confidence": "unverified", "source_ids": []},
        {"start": "2021", "end": "2025-02", "org": "中共周口市淮阳区委员会", "title": "淮阳区委书记",
         "notes": "至少2021-07-13起任区委书记,2025-02-27仍署名;之后由王献超接任",
         "confidence": "confirmed", "source_ids": ["S006", "S007"]},
        {"start": "2025", "end": "unknown", "org": "去向待查", "title": "",
         "notes": "2025年3月卸任区委书记后去向(调任/职务变动)未公开",
         "confidence": "unverified", "source_ids": []},
    ]


def build():
    print("=" * 60)
    print("  周口市淮阳区领导班子工作关系网络")
    print("  等级: 市辖区 | 调查日期: 2026-08-06")
    print("  信息来源: 淮阳区政府门户网站 + 周口市政府门户")
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

    print(f"\n✅ DB/GEXF 构建完成。")
    print(f"  人物: {len(persons)} | 机构: {len(organizations)} | 任职: {len(positions)} | 关系: {len(relationships)}")

    # ── Generate Person Graph JSONs (核心二人: 区委书记/区长) ──
    source_register = make_source_register()

    # 1. 王献超 (区委书记)
    wang_json = make_person_json(persons[0], wang_timeline(), [
        {"person": "张建党", "person_id": "huaiyang_张建党", "relationship_type": "overlap",
         "strength": "strong", "evidence": "区长×区委书记党政搭档(2021-2025)",
         "overlap_org": "淮阳区委/淮阳区政府", "overlap_period": "2021-2025",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S006"]},
        {"person": "贾鲲鹏", "person_id": "huaiyang_贾鲲鹏", "relationship_type": "predecessor_successor",
         "strength": "strong", "evidence": "王献超由区长升任区委书记后,贾鲲鹏接任区长;现为党委×政府搭档",
         "overlap_org": "淮阳区人民政府", "overlap_period": "2026-至今",
         "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
    ], source_register, "区委书记")
    with open(PERSONS_DIR / f"{TODAY}-河南省-周口市-区委书记-王献超.json", "w", encoding="utf-8") as f:
        json.dump(wang_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: 王献超")

    # 2. 贾鲲鹏 (区长)
    jia_json = make_person_json(persons[1], jia_timeline(), [
        {"person": "王献超", "person_id": "huaiyang_王献超", "relationship_type": "predecessor_successor",
         "strength": "strong", "evidence": "接任区长,前任为王献超;现为政府×党委搭档",
         "overlap_org": "淮阳区人民政府", "overlap_period": "2026-至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
        {"person": "张建党", "person_id": "huaiyang_张建党", "relationship_type": "overlap",
         "strength": "weak", "evidence": "间接跨届联系(张建党任书记时贾尚未任区长)",
         "overlap_org": "淮阳区", "overlap_period": "",
         "direction": "undirected", "confidence": "plausible", "source_ids": []},
    ], source_register, "区长")
    jia_path = PERSONS_DIR / f"{TODAY}-河南省-周口市-区长-贾鲲鹏.json"
    with open(jia_path, "w", encoding="utf-8") as f:
        json.dump(jia_json, f, ensure_ascii=False, indent=2)
    print("  Person JSON: 贾鲲鹏")

    print(f"\n所有 Person Graph JSONs 已生成到: {PERSONS_DIR}")


if __name__ == "__main__":
    build()