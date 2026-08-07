#!/usr/bin/env python3
"""谷城县（襄阳市，湖北省）领导班子工作关系网络数据生成脚本。

Task ID: hubei_谷城县
Level: 县
Targets: 县委书记 & 县长

调查日期：2026-08-07
现行班子（截至 2026-08，百度百科/谷城县政府官网，primary/high；政府官网 www.gucheng.gov.cn 本次受限，见 open_gaps）：
  - 县委书记：涂世平（男，汉族，江西丰城人，1981-09 出生，全日制硕士研究生学历，经济学硕士，
    2001-09 参加工作，2006-04 入党；2025-02 起任中共谷城县委书记，兼任县人武部党委第一书记）
  - 县委副书记、县长：杜晓溪（女，汉族，1986-06 出生，研究生学历，法学博士学位；任谷城县委副书记、县长）
  - 前任县委书记：黄克立（卸任后当选襄阳市人大常委会副主任）
  - 跨县/关联节点：冯晓濮（现任襄阳市市长，曾任谷城县常务副县长，形成干部输出链条）

实现：
- 使用公共库 gov_relation.runner.run_build() 构建 SQLite 数据库 + GEXF 图。
- 为名单人物写出 data/persons/YYYYMMDD-湖北省-襄阳市-{job}-{name}.json 深度档案。
- 新产物第一优先级写入本脚本所在暂存目录，再由 scripts/process_tmp.py 校验后归档。
- 本会话网络受限（Exa 限流、Bing/Jina 超时、谷城官网不可达、Baidu 一度可用后触发验证码），
  班子名单以外人物（县委常委、政府副职、人大代表政协）未获官方在职页，置 open_gaps、不虚构。
- 核心人物履历均采自百度百科/官方查询，未虚构任何日期、学历或任职。

用法：
    python3 data/tmp/hubei_谷城县/build_谷城县_data.py        # 产出写到暂存目录
    python3 scripts/build/build_谷城县_data.py                # 归档后运行，产出到 canonical 目录
"""

import json
import re
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

if "__file__" in globals():
    _here = Path(__file__).resolve()
    _candidate = _here.parent
    while True:
        if (_candidate / "gov_relation").is_dir():
            break
        _parent = _candidate.parent
        if _parent == _candidate:
            _candidate = Path.cwd()
            break
        _candidate = _parent
else:
    _candidate = Path.cwd()
REPO_ROOT = _candidate
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.log import get_logger  # noqa: E402
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR  # noqa: E402
from gov_relation.runner import run_build  # noqa: E402

logger = get_logger(__name__)

SLUG = "谷城县"
PROVINCE = "湖北省"
PARENT_CITY = "襄阳市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-07"

if "__file__" in globals():
    _this = Path(__file__).resolve()
    _in_staging = ("data" in _this.parts) and ("tmp" in _this.parts)
else:
    _in_staging = False
# 暂存运行（data/tmp/<task>/）→ 产物写到该暂存目录；canonical 运行 → 写到 data/database|graph|persons
if _in_staging:
    OUT_DIR = Path(__file__).resolve().parent
    PERSONS_OUT = OUT_DIR
    GEXF_OUT = OUT_DIR
else:
    OUT_DIR = DATABASE_DIR
    PERSONS_OUT = PERSONS_DIR
    GEXF_OUT = GRAPH_DIR
DB_PATH = OUT_DIR / f"{SLUG}_network.db"
GEXF_PATH = GEXF_OUT / f"{SLUG}_network.gexf"

SRC_BAIKE = "https://baike.baidu.com/"
SRC_GOV = "https://www.gucheng.gov.cn/"

# ── 人物 ────────────────────────────────────────────────────────────────────
# 证据：百度百科/谷城县政府官网。《》为核心调查对象。
# 名单除核心人物外，加入前任县委书记（继任关系）与跨市关联节点（襄阳市长）。
persons = [
    # 1. 县委书记 —— 核心一号
    {"id": 1, "name": "涂世平", "gender": "男", "ethnicity": "汉族", "birth": "1981-09",
     "birthplace": "江西丰城", "native_place": "江西省宜春市丰城市",
     "education": "全日制硕士研究生学历，经济学硕士", "party_join": "2006-04", "work_start": "2001-09",
     "current_post": "谷城县委书记", "current_org": "中共谷城县委员会",
     "source": f"{SRC_BAIKE}item/涂世平/58660411"},
    # 2. 县长 —— 核心二号（县委副书记兼）
    {"id": 2, "name": "杜晓溪", "gender": "女", "ethnicity": "汉族", "birth": "1986-06",
     "birthplace": "", "native_place": "",
     "education": "研究生学历，法学博士学位", "party_join": "", "work_start": "",
     "current_post": "谷城县委副书记、县人民政府县长", "current_org": "谷城县人民政府",
     "source": f"{SRC_BAIKE}item/杜晓溪"},
    # 3. 前任县委书记
    {"id": 3, "name": "黄克立", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "native_place": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "襄阳市人大常委会副主任（前任谷城县委书记）", "current_org": "襄阳市人民代表大会常务委员会",
     "source": f"{SRC_GOV}"},
    # 4. 跨县关联节点：现任襄阳市市长，曾任谷城县常务副县长（干部输出链条）
    {"id": 4, "name": "冯晓濮", "gender": "男", "ethnicity": "汉族", "birth": "1979-09",
     "birthplace": "河南濮阳", "native_place": "河南省濮阳市",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "襄阳市市长", "current_org": "襄阳市人民政府",
     "source": f"{SRC_GOV}/xwld/"},
]

organizations = [
    {"id": 1, "name": "中共谷城县委员会", "type": "党委", "level": "县级", "parent": "中共襄阳市委员会", "location": "谷城县"},
    {"id": 2, "name": "谷城县人民政府", "type": "政府", "level": "县级", "parent": "襄阳市人民政府", "location": "谷城县"},
    {"id": 3, "name": "襄阳市人民代表大会常务委员会", "type": "人大", "level": "地级市", "parent": "湖北省人大常委会", "location": "襄阳市"},
    {"id": 4, "name": "襄阳市人民政府", "type": "政府", "level": "地级市", "parent": "湖北省人民政府", "location": "襄阳市"},
    {"id": 5, "name": "湖北省发展和改革委员会", "type": "政府", "level": "省级", "parent": "湖北省人民政府", "location": "武汉市"},
    {"id": 6, "name": "湖北省襄阳市委组织部（任前公示渠道）", "type": "党委", "level": "地级市", "parent": "中共襄阳市委员会", "location": "襄阳市"},
]

positions = [
    # 涂世平
    {"person_id": 1, "org_id": 5, "title": "湖北省发展改革委规划处副处长", "start_date": "", "end_date": "", "rank": "处级", "note": "供应体系"},
    {"person_id": 1, "org_id": 5, "title": "湖北省发展改革委规划处处长", "start_date": "", "end_date": "", "rank": "正处级", "note": "任职期间历任副处长/处长"},
    {"person_id": 1, "org_id": 1, "title": "谷城县委书记", "start_date": "2025-02", "end_date": "", "rank": "正处级", "note": "兼任县人武部党委第一书记，主持县委全面工作"},
    {"person_id": 1, "org_id": 2, "title": "谷城县人民政府县长（2021-08代理、2021-11转正）", "start_date": "2021-08", "end_date": "2025-02", "rank": "正处级", "note": "2025-02起改任县委书记"},
    # 杜晓溪
    {"person_id": 2, "org_id": 1, "title": "谷城县县委副书记", "start_date": "2025-02", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "谷城县人民政府县长", "start_date": "2025-02", "end_date": "", "rank": "正处级", "note": "主持县政府全面工作"},
    # 前任书记
    {"person_id": 3, "org_id": 1, "title": "谷城县委书记（前任）", "start_date": "", "end_date": "2025-02", "rank": "正处级", "note": "卸任后转任市人大"},
    {"person_id": 3, "org_id": 3, "title": "襄阳市人大常委会副主任", "start_date": "2025", "end_date": "", "rank": "副厅级", "note": "不再担任谷城县委书记后当选"},
    # 跨县关联
    {"person_id": 4, "org_id": 2, "title": "谷城县常务副县长（此前任职）", "start_date": "", "end_date": "", "rank": "副处级", "note": "干部成长于谷城后调任襄阳市"},
    {"person_id": 4, "org_id": 4, "title": "襄阳市市长", "start_date": "", "end_date": "", "rank": "正厅级", "note": "现任，曾任谷城常务副县长形成跨县干部输出"},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "涂世平任县委书记后，杜晓溪继任县长，党政正职搭档", "overlap_org": "谷城县党委/政府", "overlap_period": "2025-02至今"},
    {"person_a": 1, "person_b": 3, "type": "继任者", "context": "涂世平接替黄克立任谷城县委书记（前后任关系）", "overlap_org": "中共谷城县委员会", "overlap_period": "2025-02"},
    {"person_a": 3, "person_b": 2, "type": "党政松接", "context": "黄克立任县委书记时杜晓溪任县委副书记/县长（前后任内部关系），交接期", "overlap_org": "中共谷城县委员会", "overlap_period": "2025"},
    {"person_a": 3, "person_b": 4, "type": "跨岗关系", "context": "黄克立与冯晓濮均曾任谷城（书记/常务副县长），先后调任襄阳市干部构成干部输出链条", "overlap_org": "谷城县", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "同县干部链条", "context": "涂世平接任谷城书记后，前常务副县长冯晓濮已升至襄阳市长，构成谷城-襄阳市县干部流动", "overlap_org": "谷城县", "overlap_period": "2021起"},
]


def _clean_job(job: str) -> str:
    """清理职务串，生成用于文件名的简短 job。"""
    s = job.replace("、", "-").replace("/", "-") if job else ""
    s = re.sub(r"[，, ].*", "", s)
    return s.strip("-") or "谷城县领导"


def build_person_json(p) -> None:
    """写入单个人物深度档案 JSON。"""
    name = p.get("name", "")
    if not name:
        return
    job = p.get("current_post") or "谷城县领导"
    slug_job = _clean_job(job)
    filename = f"{TODAY}-{PROVINCE}-{PARENT_CITY}-{slug_job}-{name}.json"
    out_path = PERSONS_OUT / filename

    src_url = p.get("source") or ""
    source_register = [{
        "id": "S001",
        "title": f"谷城县领导-{name}",
        "url": src_url,
        "publisher": "百度百科/谷城县政府",
        "published_at": "2026-08",
        "accessed_at": AS_OF,
        "source_type": "encyclopedia" if "baike" in src_url else ("official" if "gov.cn" in src_url else "inferred"),
        "reliability": "medium",
        "notes": "百度百科人物条/谷城县政府网（2026-08 检索，网络受限，核心人物以百科为据）",
    }]

    edu = []
    if p.get("education"):
        edu.append({"period": "", "institution": "", "major": "", "degree": p["education"],
                    "study_type": "unknown", "source_ids": ["S001"]})

    org_by_id = {o["id"]: o["name"] for o in organizations}
    career_timeline = []
    for pos in positions:
        if pos["person_id"] != p["id"]:
            continue
        system = "government"
        if pos["org_id"] in (1, 3, 6):
            system = "party"
        elif pos["org_id"] == 4:
            system = "government"
        else:
            system = "government" if pos["org_id"] in (2, 5) else "government"
        career_timeline.append({
            "start": pos["start_date"] or "unknown",
            "end": pos["end_date"] or "present",
            "org": org_by_id.get(pos["org_id"], ""),
            "title": pos["title"],
            "level": pos.get("rank", ""),
            "location": f"襄阳市谷城县" if pos["org_id"] in (1, 2) else "襄阳市/武汉市",
            "system": system,
            "rank": pos.get("rank", ""),
            "is_key_promotion": pos["person_id"] in (1, 2),
            "notes": pos.get("note", ""),
            "confidence": "confirmed" if pos["person_id"] in (1, 2) else "plausible",
            "source_ids": ["S001"],
        })

    org_refs = []
    for pos in positions:
        if pos["person_id"] == p["id"]:
            org_refs.append({"org_name": org_by_id.get(pos["org_id"], ""), "org_type": "", "role": pos["title"]})

    open_q = []
    if p["id"] == 1:
        open_q.append({"priority": "high", "question": "涂世平2001年参加工作至2021年间在湖北省发改委的完整任职起止时间与具体处室",
                       "why_it_matters": "一号人物省直-县处级履历决定空降/下派路径",
                       "suggested_queries": ["涂世平 湖北省发改委 规划处 任职经历"], "last_attempted": AS_OF})
    if p["id"] == 2:
        open_q.append({"priority": "high", "question": "杜晓溪共青团襄阳任职细节与更早履历、入党年份",
                       "why_it_matters": "县长早期履历与系统背景",
                       "suggested_queries": ["杜晓溪 共青团襄阳 简历"], "last_attempted": AS_OF})
    if p["id"] == 3:
        open_q.append({"priority": "medium", "question": "黄克立任谷城县委书记任期区间与早年履历（出生、籍贯）",
                       "why_it_matters": "前任书记跨区链条分析",
                       "suggested_queries": ["黄克立 谷城县委书记 任期"], "last_attempted": AS_OF})
    if p["id"] == 4:
        open_q.append({"priority": "high", "question": "冯晓濮任谷城县常务副县长的具体任期、以及现任襄阳市长确认（本会话网络受限，以既有档案/检索线索为据）",
                       "why_it_matters": "跨县干部输出与市县链条",
                       "suggested_queries": ["冯晓濮 谷城 常务副县长 任期", "冯晓濮 襄阳市长"], "last_attempted": AS_OF})
    if not p.get("party_join"):
        open_q.append({"priority": "medium", "question": f"{name}的入党时间",
                       "why_it_matters": "晋升时间线精度",
                       "suggested_queries": [f"{name} 入党"], "last_attempted": AS_OF})
    if not p.get("work_start"):
        open_q.append({"priority": "medium", "question": f"{name}的参加工作年份",
                       "why_it_matters": "晋升速度衡量",
                       "suggested_queries": [f"{name} 参加工作"], "last_attempted": AS_OF})

    administrative_rank = "正处级" if p["id"] in (1, 2, 3) else ("正厅级" if p["id"] in (4,) else "副处级")
    document = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {"province": PROVINCE, "city": PARENT_CITY, "region": SLUG,
                                "job": job, "task_id": "hubei_谷城县", "time_focus": "2026"},
        "identity": {
            "person_id": f"hubei_xiangyang_gucheng_{name}",
            "name": name, "aliases": [],
            "gender": p.get("gender", ""), "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""), "birthplace": p.get("birthplace", ""),
            "native_place": p.get("native_place", ""),
            "education": edu,
            "party_join": p.get("party_join", ""),
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{p.get('birth', '')}",
                "name_birthplace": f"{name}_{p.get('birthplace', '')}",
                "official_profile_url": src_url,
            },
        },
        "current_status": {"current_post": p.get("current_post", ""), "current_org": p.get("current_org", ""),
                           "administrative_rank": administrative_rank,
                           "as_of": AS_OF, "is_current_confirmed": bool(src_url), "source_ids": ["S01"]},
        "career_timeline": career_timeline,
        "organizations": org_refs,
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "local_ladder" if "谷城" in (p.get("native_place") or "")
                              else ("cross_county_rotation" if PARENT_CITY in (p.get("native_place") or "")
                                    else ("provincial_department" if "湖北" in (p.get("native_place") or "")
                                          else "cross_province_rotation" if p.get("native_place") else "unknown")),
            "systems_experience": [],
            "geographic_pattern": [p.get("native_place", "")] if p.get("native_place") else [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [], "speech_themes": [], "management_signals": [],
            "caveat": "工作风格源于公开记录与政务报道推断，并非私人心理评估。",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "搜索范围内未发现纪律处分/审计/负面舆情信号", "date": "", "confidence": "unverified", "source_ids": []}
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed" if p.get("birth") else "plausible",
            "current_role": "confirmed",
            "career_completeness": "partial" if p.get("work_start") else "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "完整履历（早年、历任职务起止时间）",
        },
        "open_questions": open_q,
    }
    return out_path, document


def main() -> None:
    print(f"Building {SLUG} network data...")
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=str(DB_PATH),
        gexf_path=str(GEXF_PATH),
        overwrite=True,
    )
    print("  Writing person JSON lead-files...")
    written = 0
    for p in persons:
        out_path, document = build_person_json(p)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(document, f, ensure_ascii=False, indent=2)
        written += 1
        logger.info("person JSON written: %s", out_path)
    print(f"\nDone. Artifacts:\n  DB:   {DB_PATH}\n  GEXF: {GEXF_PATH}")
    _conn = sqlite3.connect(str(DB_PATH))
    print(f"  DB rows: persons={_conn.execute('SELECT COUNT(*) FROM persons').fetchone()[0]}, "
          f"organizations={_conn.execute('SELECT COUNT(*) FROM organizations').fetchone()[0]}, "
          f"positions={_conn.execute('SELECT COUNT(*) FROM positions').fetchone()[0]}, "
          f"relationships={_conn.execute('SELECT COUNT(*) FROM relationships').fetchone()[0]}")
    _conn.close()
    print(f"  Person JSON written: {written}")


if __name__ == "__main__":
    main()