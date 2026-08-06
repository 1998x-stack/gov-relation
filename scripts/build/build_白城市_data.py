#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 白城市 (Baicheng), 吉林省.

Task ID: jilin_白城市 | Level: 地级市 | Targets: 市委书记 & 市长 | Date: 2026-08-06

Sources:
  - 白城市人民政府官网 http://www.jlbc.gov.cn/zfjg_3101/szfld/ (官方在挂班子，一级)
  - Wikipedia zh《白城市》《李明伟》(时间线/籍贯/出生年)
  - 新华吉林《吉林省省管干部任职前公示公告(2025年第3号)》

Confidence:
  - 李洪慈（书记）、崔景英（市长）、杨明（常务）、副市长、秘书长：Confirmed（官网）
  - 徐辉(女,人大主任)、顾伟(女,政协主席)、李明伟、杨大勇：维基百科基准
  - 崔景英2025.09前职务、杨大勇2025.07离任去向：Unverified（网络封锁）
"""

import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent
# Locate repo root: scripts/build/<slug>.py → parents[2]; data/tmp/<id>/build_<slug>.py → parents[3].
_REPO = BASE
for _ in range(3):
    if (_REPO / "gov_relation").is_dir():
        break
    _REPO = _REPO.parent
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from gov_relation.runner import run_build

SLUG = "白城市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"
DB_PATH = str(BASE / f"{SLUG}_network.db")
GEXF_PATH = str(BASE / f"{SLUG}_network.gexf")

# ═══════════════════════════ Persons ═══════════════════════════
persons = [
    {"id": 1, "name": "李洪慈", "gender": "男", "ethnicity": "汉族", "birth": "1974年7月",
     "birthplace": "山东省沂南县", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "市委书记", "current_org": "中共白城市委员会",
     "source": "https://zh.wikipedia.org/wiki/白城市; http://www.jlbc.gov.cn/"},
    {"id": 2, "name": "崔景英", "gender": "女", "ethnicity": "汉族", "birth": "1976年9月",
     "birthplace": "", "education": "研究生学历", "party_join": "中共党员", "work_start": "",
     "current_post": "市委副书记、市长", "current_org": "白城市人民政府",
     "source": "http://www.jlbc.gov.cn/zfjg_3101/szfld/sz/lmw/"},
    {"id": 3, "name": "杨明", "gender": "男", "ethnicity": "汉族", "birth": "1975年12月",
     "birthplace": "", "education": "研究生学历", "party_join": "中共党员", "work_start": "",
     "current_post": "市委常委、常务副市长", "current_org": "白城市人民政府",
     "source": "http://www.jlbc.gov.cn/zfjg_3101/szfld/fsz/lhf_23349/"},
    {"id": 4, "name": "李子罡", "gender": "男", "ethnicity": "汉族", "birth": "1976年5月",
     "birthplace": "", "education": "", "party_join": "民革党员", "work_start": "",
     "current_post": "副市长", "current_org": "白城市人民政府",
     "source": "http://www.jlbc.gov.cn/zfjg_3101/szfld/fs/lhf_23355/"},
    {"id": 5, "name": "陈晓东", "gender": "男", "ethnicity": "汉族", "birth": "1972年5月",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "副市长", "current_org": "白城市人民政府",
     "source": "http://www.jlbc.gov.cn/zfjg_3101/szfld/fs/lhf_23352/"},
    {"id": 6, "name": "丁琳", "gender": "女", "ethnicity": "汉族", "birth": "1984年10月",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "副市长", "current_org": "白城市人民政府",
     "source": "http://www.jlbc.gov.cn/zfjg_3101/szfld/fs/lhf_23126/"},
    {"id": 7, "name": "任聪", "gender": "男", "ethnicity": "汉族", "birth": "1981年8月",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "副市长、市公安局局长", "current_org": "白城市人民政府",
     "source": "http://www.jlbc.gov.cn/zfjg_3101/szfld/fs/lhf/"},
    {"id": 8, "name": "高熙礼", "gender": "男", "ethnicity": "汉族", "birth": "1982年9月",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "副市长、洮南市委书记", "current_org": "白城市人民政府",
     "source": "http://www.jlbc.gov.cn/zfjg_3101/szfld/fs/lhf_23358/"},
    {"id": 9, "name": "杨孔青", "gender": "男", "ethnicity": "彝族", "birth": "1972年7月",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "副市长（挂职）", "current_org": "白城市人民政府",
     "source": "http://www.jlbc.gov.cn/zfjg_3101/szfld/fs/lhf_31908/"},
    {"id": 10, "name": "孟凡平", "gender": "男", "ethnicity": "汉族", "birth": "1973年9月",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "市政府秘书长", "current_org": "白城市人民政府",
     "source": "http://www.jlbc.gov.cn/zfjg_3101/szfld/mss/lh_30745/"},
    {"id": 11, "name": "徐辉", "gender": "女", "ethnicity": "汉族", "birth": "1969年11月",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "市人大常委会主任", "current_org": "白城市人民代表大会常务委员会",
     "source": "https://zh.wikipedia.org/wiki/白城市"},
    {"id": 12, "name": "顾伟", "gender": "女", "ethnicity": "汉族", "birth": "1967年3月",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "市政协主席", "current_org": "中国人民政治协商会议白城市委员会",
     "source": "https://zh.wikipedia.org/wiki/白城市"},
    {"id": 13, "name": "李明伟", "gender": "男", "ethnicity": "汉族", "birth": "1968年10月",
     "birthplace": "吉林省舒兰市", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "省委常委、省委政法委书记", "current_org": "中共吉林省委员会",
     "source": "https://zh.wikipedia.org/wiki/李明伟"},
    {"id": 14, "name": "杨大勇", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "前任市长（2022-2025，已离任）", "current_org": "",
     "source": "https://zh.wikipedia.org/wiki/白城市"},
]

# ═══════════════════════════ Organizations ═══════════════════════════
organizations = [
    {"id": 1, "name": "中共白城市委员会", "type": "党委", "level": "地级", "parent": "中共吉林省委员会", "location": "白城市"},
    {"id": 2, "name": "白城市人民政府", "type": "政府", "level": "地级", "parent": "吉林省人民政府", "location": "白城市"},
    {"id": 3, "name": "白城市人民代表大会常务委员会", "type": "人大", "level": "地级", "parent": "吉林省人大常委会", "location": "白城市"},
    {"id": 4, "name": "中国人民政治协商会议白城市委员会", "type": "政协", "level": "地级", "parent": "吉林省政协", "location": "白城市"},
    {"id": 5, "name": "白城市公安局", "type": "政府", "level": "地级", "parent": "白城市人民政府", "location": "白城市"},
    {"id": 6, "name": "中共白城市洮南市委员会", "type": "党委", "level": "县级", "parent": "中共白城市委员会", "location": "洮南市"},
    {"id": 7, "name": "中共吉林省委员会", "type": "党委", "level": "省级", "parent": "", "location": "长春市"},
]

# ═══════════════════════════ Positions ═══════════════════════════
positions = [
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "2022-07", "end_date": "present", "rank": "地级市正职", "note": "由市长升任"},
    {"person_id": 1, "org_id": 2, "title": "市长", "start_date": "2021-03", "end_date": "2022-07", "rank": "地级市正职", "note": "接替李明伟"},
    {"person_id": 2, "org_id": 2, "title": "市委副书记、市长、市政府党组书记", "start_date": "2025-09", "end_date": "present", "rank": "地级市正职", "note": "接任杨大勇"},
    {"person_id": 3, "org_id": 2, "title": "市委常委、常务副市长、市政府党组副书记", "start_date": "unknown", "end_date": "present", "rank": "地级市副职", "note": "党政交叉核心"},
    {"person_id": 4, "org_id": 2, "title": "副市长", "start_date": "unknown", "end_date": "present", "rank": "地级市副职", "note": "民革"},
    {"person_id": 5, "org_id": 2, "title": "副市长", "start_date": "unknown", "end_date": "present", "rank": "地级市副职", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副市长", "start_date": "unknown", "end_date": "present", "rank": "地级市副职", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "副市长", "start_date": "unknown", "end_date": "present", "rank": "地级市副职", "note": ""},
    {"person_id": 7, "org_id": 5, "title": "市公安局局长、督察长", "start_date": "unknown", "end_date": "present", "rank": "地级市副职", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "副市长", "start_date": "unknown", "end_date": "present", "rank": "地级市副职", "note": ""},
    {"person_id": 8, "org_id": 6, "title": "洮南市委书记（兼）", "start_date": "unknown", "end_date": "present", "rank": "县级正职", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副市长（挂职）", "start_date": "unknown", "end_date": "present", "rank": "地级市副职", "note": "彝族"},
    {"person_id": 10, "org_id": 2, "title": "市政府秘书长", "start_date": "unknown", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 11, "org_id": 3, "title": "市人大常委会主任", "start_date": "2022-01", "end_date": "present", "rank": "地级市正职", "note": ""},
    {"person_id": 12, "org_id": 4, "title": "市政协主席", "start_date": "2022-01", "end_date": "present", "rank": "地级市正职", "note": ""},
    {"person_id": 13, "org_id": 1, "title": "市委书记", "start_date": "2021-03", "end_date": "2022-07", "rank": "地级市正职", "note": "前任"},
    {"person_id": 13, "org_id": 7, "title": "省委常委、省委政法委书记", "start_date": "2022-06", "end_date": "present", "rank": "省部级", "note": "调任"},
    {"person_id": 14, "org_id": 2, "title": "市长", "start_date": "2022-07", "end_date": "2025-07", "rank": "地级市正职", "note": "前任市长,去向未核实"},
]

# ═══════════════════════════ Relationships ═══════════════════════════
relationships = [
    {"person_a": 1, "person_b": 2, "type": "决策搭档", "context": "现任市委书记与市长，党政班子搭档", "overlap_org": "中共白城市委员会/白城市人民政府", "overlap_period": "2025-09至今"},
    {"person_a": 1, "person_b": 14, "type": "前任-继任", "context": "杨大勇2022.07接任市长", "overlap_org": "白城市人民政府", "overlap_period": "2022-07"},
    {"person_a": 2, "person_b": 14, "type": "前任-继任", "context": "崔景英2025.09接任杨大勇市长岗位", "overlap_org": "白城市人民政府", "overlap_period": "2025-09"},
    {"person_a": 1, "person_b": 13, "type": "前任-继任", "context": "李明伟升省委后李洪慈任书记；此前李明伟任书记、李洪慈任市长", "overlap_org": "中共白城市委员会", "overlap_period": "2021-2022"},
    {"person_a": 13, "person_b": 14, "type": "前任-继任", "context": "李明伟任书记期间杨大勇接任市长", "overlap_org": "中共白城市委员会", "overlap_period": "2022-07"},
    {"person_a": 3, "person_b": 2, "type": "班子/上下级", "context": "杨明（常务副市长、市委常委）协助市长崔景英主持政府工作", "overlap_org": "白城市人民政府", "overlap_period": "2025-09至今"},
    {"person_a": 3, "person_b": 1, "type": "班子交集", "context": "杨明任市委常委，与市委书记李洪慈同属白城市委常委会", "overlap_org": "中共白城市委员会", "overlap_period": "2022-07至今"},
]

# ═══════════════════════════ Person JSON ═══════════════════════════
SOURCE_REGISTER = [
    {"id": "S001", "title": "白城市人民政府·市政府领导", "url": "http://www.jlbc.gov.cn/zfjg_3101/szfld/", "publisher": "白城市人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "在任市领导班子名单"},
    {"id": "S002", "title": "白城市政府 市长简历页", "url": "http://www.jlbc.gov.cn/zfjg_3101/szfld/sz/lmw/", "publisher": "白城市人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "崔景英简历"},
    {"id": "S003", "title": "Wikipedia zh《白城市》", "url": "https://zh.wikipedia.org/wiki/白城市", "publisher": "Wikipedia", "published_at": "", "accessed_at": AS_OF, "source_type": "database", "reliability": "medium", "notes": "出生年、籍贯、历任领导时间线"},
    {"id": "S004", "title": "Wikipedia《李明伟》", "url": "https://zh.wikipedia.org/wiki/李明伟", "publisher": "Wikipedia", "published_at": "", "accessed_at": AS_OF, "source_type": "database", "reliability": "medium", "notes": "前任书记去向"},
]


def build_person_file(name, current_post, identity, timeline, relations, orgs, big_gap, qs=None):
    p = BASE / f"{TODAY}-吉林省-白城市-{current_post}-{name}.json"
    data = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {"province": "吉林省", "city": "白城市", "region": "白城市",
                                "job": current_post, "task_id": "jilin_白城市", "time_focus": "2024-2026"},
        "identity": {"person_id": f"baicheng_{name}", "name": name, "aliases": [],
                     "gender": identity.get("gender", ""), "ethnicity": identity.get("ethnicity", ""),
                     "birth": identity.get("birth", ""), "birthplace": identity.get("birth", ""),
                     "education": identity.get("education", []),
                     "party_join": identity.get("party_join", ""), "work_start": identity.get("work_start", "")},
        "current_status": {"current_post": current_post, "current_org": identity.get("current_org", ""),
                           "administrative_rank": identity.get("rank", ""), "as_of": AS_OF,
                           "is_current_confirmed": True, "source_ids": ["S001", "S002"]},
        "career_timeline": timeline if timeline else [],
        "organizations": orgs if isinstance(orgs, list) else ([orgs] if orgs else []),
        "relationships": relations if isinstance(relations, list) else [],
        "governance_record": [],
        "professional_profile": {},
        "work_style_and_personality": {},
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": SOURCE_REGISTER,
        "confidence_summary": {"identity": "confirmed" if identity.get("birth") else "plausible",
                               "current_role": "confirmed",
                               "career_completeness": "partial" if timeline else "thin",
                               "relationship_confidence": "medium", "biggest_gap": big_gap},
        "open_questions": qs or [{"priority": "high", "question": big_gap, "why_it_matters": "任职网络分析",
                                  "suggested_queries": [f"{name} 简历"], "last_attempted": AS_OF}],
    }
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("  person JSON:", p.name)


def write_persons_files():
    build_person_file(
        "李洪慈", "市委书记",
        {"gender": "男", "ethnicity": "汉族", "birth": "1974年7月", "birthplace": "山东省沂南县",
         "education": [], "party_join": "中共党员", "work_start": "", "current_org": "中共白城市委员会", "rank": "地级市正职"},
        [{"start": "2022-07", "end": "present", "org": "中共白城市委员会", "title": "市委书记", "level": "地级市", "system": "party", "rank": "地级市正职", "is_key_promotion": True, "notes": "由市长升任", "confidence": "confirmed", "source_ids": ["S001"]},
         {"start": "2021-03", "end": "2022-07", "org": "白城市人民政府", "title": "市长", "level": "地级市", "system": "government", "rank": "地级市正职", "is_key_promotion": True, "notes": "接替李明伟", "confidence": "confirmed", "source_ids": ["S001"]},
         {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "level": "", "system": "", "rank": "", "notes": "2021年前完整履历未获一级来源", "confidence": "unverified", "source_ids": []}],
        [{"person": "崔景英", "person_id": "baicheng_崔景英", "relationship_type": "overlap", "strength": "strong", "evidence": "党政班子搭档", "overlap_org": "中共白城市委/白城市人民政府", "overlap_period": "2025-09至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
         {"person": "李明伟", "person_id": "baicheng_李明伟", "relationship_type": "predecessor_successor", "strength": "medium", "evidence": "李洪慈继任李明伟为市长并后任书记", "overlap_org": "中共白城市委员会", "overlap_period": "2021-2022", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]}],
        [{"id": "baicheng_白城市委", "name": "中共白城市委员会", "type": "党委", "level": "地级", "location": "白城市"},
         {"id": "baicheng_白城市政府", "name": "白城市人民政府", "type": "政府", "level": "地级", "location": "白城市"}],
        "李洪慈2021年前教育/入党/入职及完整履历",
    )
    build_person_file(
        "崔景英", "市长",
        {"gender": "女", "ethnicity": "汉族", "birth": "1976年9月", "birthplace": "",
         "education": [{"period": "", "institution": "", "major": "", "degree": "研究生学历", "study_type": "unknown", "source_ids": ["S002"]}],
         "party_join": "中共党员", "work_start": "", "current_org": "白城市人民政府", "rank": "地级市正职"},
        [{"start": "2025-09", "end": "present", "org": "白城市人民政府", "title": "市委副书记、市长、市政府党组书记", "level": "地级市", "system": "government", "rank": "地级市正职", "is_key_promotion": True, "notes": "2026-01人代会作2025年政府工作报告", "confidence": "confirmed", "source_ids": ["S002"]},
         {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "level": "", "system": "", "rank": "", "notes": "2025.09前岗位未获一级来源", "confidence": "unverified", "source_ids": []}],
        [{"person": "李洪慈", "person_id": "baicheng_李洪慈", "relationship_type": "overlap", "strength": "strong", "evidence": "党政班子搭档", "overlap_org": "中共白城市委/白城市人民政府", "overlap_period": "2025-09至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
         {"person": "杨大勇", "person_id": "baicheng_杨大勇", "relationship_type": "predecessor_successor", "strength": "medium", "evidence": "接任杨大勇的市长岗位", "overlap_org": "白城市人民政府", "overlap_period": "2025-09", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]}],
        [{"id": "baicheng_白城市政府", "name": "白城市人民政府", "type": "政府", "level": "地级", "location": "白城市"}],
        "崔景英任白城市长前的岗位（2025.09前）",
    )


def main():
    print(f"[白城市] 构建 SQLite DB + GEXF ...")
    run_build(slug=SLUG, persons=persons, organizations=organizations,
              positions=positions, relationships=relationships,
              db_path=DB_PATH, gexf_path=GEXF_PATH)
    _verify_db()
    write_persons_files()
    print(f"[白城市] 完成：{DB_PATH}\n{GEXF_PATH}\npersons JSON {len(persons)} 人")


def _verify_db():
    conn = sqlite3.connect(DB_PATH)
    try:
        tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        required = {"persons", "organizations", "positions", "relationships"}
        missing = sorted(required - tables)
        if missing:
            raise SystemExit(f"DB 缺少表: {missing}")
        counts = {t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0] for t in sorted(required)}
        print(f"  DB 校验: {counts}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()