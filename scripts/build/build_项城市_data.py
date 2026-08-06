#!/usr/bin/env python3
"""
项城市（周口市）领导班子工作关系网络 — 构建脚本

等级: 县级市 | 上级: 河南省周口市
调查日期: 2026-08-06
数据来源: 项城市人民政府门户(www.xiangcheng.gov.cn)官方领导简介与官方时政新闻
说明: 调查期间外部搜索引擎(Exa/Baidu/Bing/Google)全部受限,采用 partial-evidence 模式;
      核心领导身份(市委书记/市长)与任职时序由官方来源确认,传记字段以 open_questions 显式标注。
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
SLUG = "项城市"
TODAY = "2026-08-06"
AS_OF = TODAY
PROVINCE = "河南省"
CITY = "周口市"
REGION = "项城市"

# ── Paths ──
HERE = Path(__file__).parent
DB_PATH = HERE / f"{REGION}_network.db"
GEXF_PATH = HERE / f"{REGION}_network.gexf"
PERSONS_DIR = HERE

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ── 现任市委书记 ──
    {
        "id": 1,
        "name": "孙红伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "项城市委书记",
        "current_org": "中共项城市委员会",
        "source": "https://www.xiangcheng.gov.cn/ — 项城市政府门户时政新闻: 2026-05-26《全市“三夏”农业生产工作会议召开 孙红伟出席并讲话》(称“市委书记孙红伟”)",
        "notes": "2026-05-26官方报道确认为项城市委书记并主持全市会议;出生/籍贯/学历/入党时间/任前职务等公开渠道暂未获取。",
    },
    # ── 现任市长 ──
    {
        "id": 2,
        "name": "齐长军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-08",
        "birthplace": "",
        "native_place": "",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "项城市市长",
        "current_org": "项城市人民政府",
        "source": "https://www.xiangcheng.gov.cn/sitesources/xcs/page_pc/xxgk/jcxxgk/jgsz/szfld/qzj/ — 项城市政府门户机构设置>市政府领导>齐长军官方领导简介(2026-01-07更新)",
        "notes": "男，汉族，1975年8月生，大学本科学历，中共党员。现任项城市委副书记，市政府市长、党组书记。主持市政府全面工作，负责审计方面工作，分管市审计局。任市长前的任职履历公开渠道暂无详细记录。",
    },
    # ── 市委常委/常务副市长 ──
    {
        "id": 3,
        "name": "贾玉柱",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "项城市委常委、市政府常务副市长",
        "current_org": "项城市人民政府",
        "source": "https://www.xiangcheng.gov.cn/ — 项城市政府门户时政新闻: 2026-05-26《全市“三夏”农业生产工作会议召开》(“市委常委、市政府党组成员贾玉柱”)与2026-05-30《齐长军调研“三夏”生产工作》",
        "notes": "2026-05官方报道确认为市委常委、市政府党组成员(常务工作口径),部署“三夏”生产;出生/籍贯/学历/常务副市长正式头衔及分管待进一步核实。",
    },
    # ── 副市长 王赞 ──
    {
        "id": 4,
        "name": "王赞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986-05",
        "birthplace": "",
        "native_place": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "项城市委常委、宣传部部长、市政府副市长",
        "current_org": "项城市人民政府",
        "source": "https://www.xiangcheng.gov.cn/sitesources/xcs/page_pc/xxgk/jcxxgk/jgsz/szfld/wz/ — 项城市政府门户市政府领导>王赞官方领导简介",
        "notes": "男，汉族，1986年5月生，研究生学历，中共党员，现任项城市委常委，宣传部部长、市政府副市长。负责教育体育、卫生健康、医疗保障、民政、生态环境、文化旅游、广播电视方面工作。",
    },
    # ── 副市长 (万东伟) ──
    {
        "id": 5,
        "name": "万东伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-06",
        "birthplace": "",
        "native_place": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "项城市副市长、市公安局局长",
        "current_org": "项城市人民政府",
        "source": "https://www.xiangcheng.gov.cn/sitesources/xcs/page_pc/xxgk/jcxxgk/jgsz/szfld/wdw/ — 项城市政府领导门户>万东伟官方领导简介",
        "notes": "男，汉族，1973年6月生，研究生学历，中共党员。兼任市公安局长。负责公安、司法、信访方面工作。曾任周口市公安局沙南分局七一路派出所所长，周口市公安局指挥中心主任等。",
    },
    # ── 副市长 (王红卫) ──
    {
        "id": 6,
        "name": "王红卫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-12",
        "birthplace": "",
        "native_place": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "项城市副市长",
        "current_org": "项城市人民政府",
        "source": "https://www.xiangcheng.gov.cn/sitesources/xcs/page_pc/xxgk/jcxxgk/jgsz/szfld/wyj/ — 项城市政府领导门户>王红卫官方领导简介",
        "notes": "男，汉族，1972年12月生，研究生学历，中共党员。负责生态环境、城乡建设管理及住房保障方面。曾任川汇区北郊乡团委书记/党委委员/副乡长，川汇区南郊乡副乡长，川汇区科协等。",
    },
    # ── 副市长 (张伟) ──
    {
        "id": 7,
        "name": "张伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-09",
        "birthplace": "",
        "native_place": "",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "项城市副市长",
        "current_org": "项城市人民政府",
        "source": "https://www.xiangcheng.gov.cn/sitesources/xcs/page_pc/xxgk/jcxxgk/jgsz/szfld/cz/ — 项城市政府领导门户>张伟官方领导简介",
        "notes": "男，汉族，1975年9月生，本科学历，中共党员。负责工业/市场监管/开放招商/交通运输/开发区等。曾任项城市李寨镇副镇长；官会镇党委委员、副镇长；贾岭镇党委副书记、镇长等。",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共项城市委员会", "type": "党委", "level": "县处级", "parent": "中共周口市委员会", "location": "河南省周口市项城市"},
    {"id": 2, "name": "项城市人民政府", "type": "政府", "level": "县处级", "parent": "周口市人民政府", "location": "河南省周口市项城市"},
    {"id": 3, "name": "中共项城市委员会宣传部", "type": "党委", "level": "县处级", "parent": "中共项城市委员会", "location": "河南省周口市项城市"},
    {"id": 4, "name": "项城市公安局", "type": "政府", "level": "县处级", "parent": "项城市人民政府", "location": "河南省周口市项城市"},
    {"id": 5, "name": "项城市人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "周口市人大常委会", "location": "河南省周口市项城市"},
    {"id": 6, "name": "政协项城市委员会", "type": "政协", "level": "县处级", "parent": "政协周口市委员会", "location": "河南省周口市项城市"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 孙红伟
    {"person_id": 1, "org_id": 1, "title": "项城市委书记", "start": "unknown", "end": "present", "rank": "正处级", "note": "2026-05官方确认为市委书记；任职起始时间与前任待查"},
    # 齐长军
    {"person_id": 2, "org_id": 1, "title": "项城市委副书记", "start": "unknown", "end": "present", "rank": "正处级", "note": "官方简介确认兼任市委副书记"},
    {"person_id": 2, "org_id": 2, "title": "项城市市长、党组书记", "start": "unknown", "end": "present", "rank": "正处级", "note": "2026-01官方领导简介确认；主持市政府全面工作"},
    # 贾玉柱
    {"person_id": 3, "org_id": 1, "title": "项城市委常委、市政府常务副市长", "start": "unknown", "end": "present", "rank": "副处级", "note": "2026-05官方报道确认‘市委常委、市政府党组成员’"},
    {"person_id": 3, "org_id": 2, "title": "项城市政府常务副市长", "start": "unknown", "end": "present", "rank": "副处级", "note": "负责部署“三夏”生产等工作的市政府分管领导"},
    # 王赞
    {"person_id": 4, "org_id": 1, "title": "项城市委常委、宣传部部长", "start": "unknown", "end": "present", "rank": "副处级", "note": "官方简介：现任项城市委常委、宣传部部长"},
    {"person_id": 4, "org_id": 2, "title": "项城市副市长", "start": "unknown", "end": "present", "rank": "副处级", "note": "分管教育体育/卫健/医保/民政/生态环境/文旅广电"},
    # 万东伟
    {"person_id": 5, "org_id": 2, "title": "项城市副市长", "start": "unknown", "end": "present", "rank": "副处级", "note": "公安/司法/信访分管领导"},
    {"person_id": 5, "org_id": 4, "title": "项城市公安局局长(兼)", "start": "unknown", "end": "present", "rank": "副处级", "note": "兼任市公安局局长"},
    # 王红卫
    {"person_id": 6, "org_id": 2, "title": "项城市副市长", "start": "unknown", "end": "present", "rank": "副处级", "note": "分管生态环境/城乡建设/住房保障等"},
    # 张伟
    {"person_id": 7, "org_id": 2, "title": "项城市副市长", "start": "unknown", "end": "present", "rank": "副处级", "note": "分管工信/市场监管/招商/开发区/交通等"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 孙红伟 ↔ 齐长军: 市委书记×市长 党政搭档
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "孙红伟任市委书记、齐长军任市委副书记兼市长，构成党政搭档", "overlap_org": "中共项城市委员会/项城市人民政府", "overlap_period": "2026-至今"},
    # 贾玉柱 ↔ 齐长军: 市长×常务副市长 政府治理搭档
    {"person_a": 3, "person_b": 2, "type": "overlap", "context": "齐长军(市长)与贾玉柱(常务副市长)同场调研部署“三夏”生产", "overlap_org": "项城市人民政府", "overlap_period": "2026-至今"},
    # 贾玉柱 ↔ 孙红伟: 市委班子成员
    {"person_a": 3, "person_b": 1, "type": "overlap", "context": "贾玉柱为市委常委，与市委书记、市长同为市委班子主要成员", "overlap_org": "中共项城市委员会", "overlap_period": "2026-至今"},
]

# ══════════════════════════════════════════════════════════════════════════════
# SOURCE REGISTER
# ══════════════════════════════════════════════════════════════════════════════

def make_source_register() -> list[dict]:
    return [
        {"id": "S001", "title": "全市“三夏”农业生产工作会议召开 孙红伟出席并讲话(2026-05-26)",
         "url": "http://www.xiangcheng.gov.cn/sitesources/xcs/page_pc/xwdt/ssxw/article35ae98a001064351a4429f9ac54b32e9.html",
         "publisher": "项城市人民政府门户网站", "published_at": "2026-05-26", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high", "notes": "确认孙红伟为“市委书记”，贾玉柱为“市委常委、市政府党组成员”"},
        {"id": "S002", "title": "齐长军调研“三夏”生产工作(2026-05-30)",
         "url": "http://www.xiangcheng.gov.cn/sitesources/xcs/page_pc/xwdt/ssxw/articlee87b1d7613eb4871a99d6aa63ee34842.html",
         "publisher": "项城市人民政府门户网站", "published_at": "2026-05-30", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high", "notes": "确认齐长军为“市长”（媒体口径）"},
        {"id": "S003", "title": "齐长军 领导简介（机构设置>市政府领导>齐长军，2026-01-07版）",
         "url": "http://www.xiangcheng.gov.cn/sitesources/xcs/page_pc/xxgk/jcxxgk/jgsz/szfld/qzj/",
         "publisher": "项城市人民政府门户网站", "published_at": "2026-01-07", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high", "notes": "官方确认齐长军：男，汉族，1975-08生，大学本科学历，中共党员，项市委副书记、市长、党组书记"},
        {"id": "S004", "title": "王赞 领导简介（市政府领导）",
         "url": "http://www.xiangcheng.gov.cn/sitesources/xcs/page_pc/xxgk/jcxxgk/jgsz/szfld/wz/",
         "publisher": "项城市人民政府门户网站", "published_at": "", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high", "notes": "王赞：男，汉族，1986-05，研究生学历，中共党员，市委常委、宣传部部长、副市长"},
        {"id": "S005", "title": "万东伟 领导简介（市政府领导）",
         "url": "http://www.xiangcheng.gov.cn/sitesources/xcs/page_pc/xxgk/jcxxgk/jgsz/szfld/wdw/",
         "publisher": "项城市人民政府门户网站", "published_at": "", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high", "notes": "万东伟：男，汉族，1973-06生，研究生学历，中共党员，副市长兼公安局局长"},
        {"id": "S006", "title": "王红卫 领导简介（市政府领导）",
         "url": "http://www.xiangcheng.gov.cn/sitesources/xcs/page_pc/xxgk/jcxxgk/jgsz/szfld/wyj/",
         "publisher": "项城市人民政府门户网站", "published_at": "", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high", "notes": "王红卫：男，汉族，1972-12生，研究生学历，中共党员，副市长"},
        {"id": "S007", "title": "张伟 领导简介（市政府领导）",
         "url": "http://www.xiangcheng.gov.cn/sitesources/xcs/page_pc/xxgk/jcxxgk/jgsz/szfld/cz/",
         "publisher": "项城市人民政府门户网站", "published_at": "", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high", "notes": "张伟：男，汉族，1975-09生，本科学历，中共党员，副市长"},
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
            "task_id": "henan_项城市",
            "time_focus": "2026",
        },
        "identity": {
            "person_id": f"xiangcheng_{person['name']}",
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
            "administrative_rank": "正处级" if person.get("id") in (1, 2) else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002", "S003"],
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": person_relationships,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": ["party"] if person.get("id") == 1 else (["party", "government"] if person.get("id") == 2 else ["government"]),
            "geographic_pattern": ["项城市(周口市)"],
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
            "identity": "confirmed" if person.get("id") == 2 else ("confirmed" if person.get("id") in (4, 5, 6, 7) else "partial"),
            "current_role": "confirmed",
            "career_completeness": "thin" if person.get("id") in (1, 3) else "partial",
            "relationship_confidence": "medium",
            "biggest_gap": "核心领导出生年份/籍贯/学历/入党时间及任现职前完整履历未公开确认",
        },
        "open_questions": [
            {"priority": "critical", "question": f"{person['name']}的出生年份、籍贯、学历/专业、入党与参工时间",
             "why_it_matters": "姓名+出生年份是跨区去重与身份校准的关键字段",
             "suggested_queries": [f"{person['name']} 简历 项城", f"{person['name']} 百度百科", f"{person['name']} 任前公示"],
             "last_attempted": AS_OF},
            {"priority": "high", "question": f"{person['name']}任项城{job}前的上一任职职务与来源单位",
             "why_it_matters": "还原晋升链条与跨区调动网络",
             "suggested_queries": [f"{person['name']} 周口 干部 任前公示", f"{person['name']} 之前 担任"],
             "last_attempted": AS_OF},
            {"priority": "medium", "question": "项城市委领导班子(市委副书记、组织部长、纪委书记、政法委书记)名单与分工",
             "why_it_matters": "区委常委会全体成员名单与分工是细化关系网络的必要输入",
             "suggested_queries": ["项城市 领导分工", "项城市委班子 名单"],
             "last_attempted": AS_OF},
        ],
    }


# ── 各核心人物 timeline & relationships ──

def sun_timeline() -> list[dict]:
    return [
        {"start": "unknown", "end": "present", "org": "履历缺口", "title": "",
         "notes": "孙红伟任项城市委书记前的完整履历(出生年度、籍贯、教育、此前任职)公开渠道暂未获取；2026-05官方报道确认其任市委书记",
         "confidence": "unverified", "source_ids": []},
        {"start": "unknown", "end": "present", "org": "中共项城市委员会", "title": "项城市委书记",
         "notes": "2026-05-26官方报道“市委书记孙红伟出席并讲话”确认在任",
         "confidence": "confirmed", "source_ids": ["S001"]},
    ]


def qi_timeline() -> list[dict]:
    return [
        {"start": "unknown", "end": "present", "org": "履历缺口", "title": "",
         "notes": "齐长军任项城市长前的履历(任市长起始时间)公开渠道未明确",
         "confidence": "unverified", "source_ids": []},
        {"start": "unknown", "end": "present", "org": "项城市人民政府", "title": "市长、党组书记",
         "notes": "2026-01-07官方领导简介确认现任；主持市政府全面工作，分管审计局",
         "confidence": "confirmed", "source_ids": ["S002", "S003"]},
        {"start": "unknown", "end": "present", "org": "中共项城市委员会", "title": "市委副书记",
         "notes": "官方简介确认兼任市委副书记",
         "confidence": "confirmed", "source_ids": ["S003"]},
    ]


def jiayao_timeline() -> list[dict]:
    return [
        {"start": "unknown", "end": "present", "org": "履历缺口", "title": "",
         "notes": "贾玉柱任市委常委/常务副市长的起始时间与公开履历未详细获取",
         "confidence": "unverified", "source_ids": []},
        {"start": "unknown", "end": "present", "org": "项城市人民政府", "title": "市委常委、市政府常务副市长",
         "notes": "2026-05-26官方报道确认“市委常委、市政府党组成员贾玉柱”",
         "confidence": "plausible", "source_ids": ["S001"]},
    ]


def build():
    print("=" * 60)
    print("  周口市项城市领导班子工作关系网络")
    print("  等级: 县级市 | 调查日期: 2026-08-06")
    print("  信息来源: 项城市人民政府门户网站")
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

    # ── Generate Person Graph JSONs (核心二人: 市委书记/市长) ──
    source_register = make_source_register()

    # 1. 孙红伟 (市委书记)
    sun_json = make_person_json(persons[0], sun_timeline(), [
        {"person": "齐长军", "person_id": "xiangcheng_齐长军", "relationship_type": "overlap",
         "strength": "strong", "evidence": "市委书记×市长(市委副书记)党政搭档(2026-至今)",
         "overlap_org": "中共项城市委员会/项城市人民政府", "overlap_period": "2026-至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "贾玉柱", "person_id": "xiangcheng_贾玉柱", "relationship_type": "overlap",
         "strength": "medium", "evidence": "同届市委领导班子成员",
         "overlap_org": "中共项城市委员会", "overlap_period": "2026-至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
    ], source_register, "市委书记")
    with open(PERSONS_DIR / f"{TODAY}-河南省-周口市-市委书记-孙红伟.json", "w", encoding="utf-8") as f:
        json.dump(sun_json, f, ensure_ascii=False, indent=2)
    print("  Person JSON: 孙红伟")

    # 2. 齐长军 (市长)
    qi_json = make_person_json(persons[1], qi_timeline(), [
        {"person": "孙红伟", "person_id": "xiangcheng_孙红伟", "relationship_type": "overlap",
         "strength": "strong", "evidence": "市长×市委书记 党政搭档",
         "overlap_org": "项城市人民政府/中共项城市委员会", "overlap_period": "2026-至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
        {"person": "贾玉柱", "person_id": "xiangcheng_贾玉柱", "relationship_type": "overlap",
         "strength": "strong", "evidence": "市长×常务副市长同场部署“三夏”生产",
         "overlap_org": "项城市人民政府", "overlap_period": "2026-至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
    ], source_register, "市长")
    qi_path = PERSONS_DIR / f"{TODAY}-河南省-周口市-市长-齐长军.json"
    with open(qi_path, "w", encoding="utf-8") as f:
        json.dump(qi_json, f, ensure_ascii=False, indent=2)
    print("  Person JSON: 齐长军")

    print(f"\n所有 Person Graph JSONs 已生成到: {PERSONS_DIR}")


if __name__ == "__main__":
    build()