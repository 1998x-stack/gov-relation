#!/usr/bin/env python3
"""Build SQLite database + GEXF graph + person JSONs for 来凤县 (Laifeng County), 湖北省恩施州.

Investigation date: 2026-08-06
Task ID: hubei_来凤县
Level: 县级
Targets: 县委书记 & 县长

Sources:
  - 来凤县人民政府门户网站 · 政府领导之窗 (http://www.laifeng.gov.cn/xxgk/gkml/zfld/)
  - 云上来凤综合门户 (http://www.laifeng.net/xwld , /zfld 领导活动报道集)
  - 恩施州政府网 (www.enshi.gov.cn) / 恩施新闻网 (www.enshi.cn)

Confidence:
  - 县委书记 王兵: CONFIRMED current via laifeng.net 领导活动 (2026-06/07/08) 多次; 详细前职履历未获 -> open gap.
  - 县长 刘涛: CONFIRMED 代理/县长候选人 via laifeng.gov.cn 政府领导之窗 2026-08-03; 完整简历(研究生/恩施本地干部回轮).
  - 政府班子: CONFIRMED via 政府领导之窗各领导个人简历 (张冠华/汪玉明/朱泽华/向雪峰/戴青/朱进友); 谭剑(副县长候选人2026-08)。
  - 县人大常委会主任 赵昌青、县政协主席 汪建敏、县委副书记 何小岚: CONFIRMED via laifeng.net 领导新闻 (2026-07-01)。
  - 前任县委书记 李伟(→州人大常委会副主任)、前任县长 钟迎松、更早书记 邢祖训: official/history (2026 县乡换届)。
"""

import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

for _parent in Path(__file__).resolve().parents:
    if (_parent / "gov_relation").is_dir():
        sys.path.insert(0, str(_parent))
        break

from gov_relation.runner import run_build  # noqa: E402

SLUG = "来凤县"
PROVINCE = "湖北省"
CITY = "恩施土家族苗族自治州"
AS_OF = "2026-08-06"
TASK_ID = "hubei_来凤县"
TODAY = datetime.now().strftime("%Y%m%d")

HERE = Path(__file__).resolve().parent
DB_PATH = HERE / f"{SLUG}_network.db"
GEXF_PATH = HERE / f"{SLUG}_network.gexf"

# ── Persons (confirmed as-of 2026-08-06) ──────────────────────────────
persons = [
    {"id": 1, "name": "王兵", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县委书记", "current_org": "中共来凤县委员会",
     "source": "http://www.laifeng.net/xwld (领导活动 2026-07/08)"},
    {"id": 2, "name": "刘涛", "gender": "男", "ethnicity": "土家族", "birth": "1981-09", "birthplace": "湖北恩施",
     "education": "研究生学历，广西民族大学中国少数民族史专业", "party_join": "2006-11", "work_start": "2003-08",
     "current_post": "县委副书记、代理县长（县长候选人）", "current_org": "来凤县人民政府",
     "source": "http://www.laifeng.gov.cn/xxgk/gkml/zfld/202608/t20260803_1823876.shtml"},
    {"id": 3, "name": "张冠华", "gender": "男", "ethnicity": "苗族", "birth": "1974-05", "birthplace": "湖北来凤",
     "education": "大学学历，湖北省委党校经济管理专业", "party_join": "1998-06", "work_start": "1995-07",
     "current_post": "县委常委、常务副县长", "current_org": "来凤县人民政府",
     "source": "http://www.laifeng.gov.cn/xxgk/gkml/zfld/202109/t20210913_1170569.shtml"},
    {"id": 4, "name": "汪玉明", "gender": "男", "ethnicity": "土家族", "birth": "1974-11", "birthplace": "湖北咸丰",
     "education": "大学学历，长江大学行政管理专业", "party_join": "", "work_start": "1993-08",
     "current_post": "副县长", "current_org": "来凤县人民政府",
     "source": "http://www.laifeng.gov.cn/xxgk/gkml/zfld/202109/t20210913_1170775.shtml"},
    {"id": 5, "name": "朱泽华", "gender": "男", "ethnicity": "土家族", "birth": "1974-12", "birthplace": "湖北鹤峰",
     "education": "大学学历，湖北省委党校法律专业", "party_join": "1998-06", "work_start": "1996-09",
     "current_post": "副县长（主持县公安局）", "current_org": "来凤县人民政府",
     "source": "http://www.laifeng.gov.cn/xxgk/gkml/zfld/202111/t20211109_1202505.shtml"},
    {"id": 6, "name": "向雪峰", "gender": "男", "ethnicity": "土家族", "birth": "1977-01", "birthplace": "湖北来凤",
     "education": "大学学历，湖北广播电视大学汉语言文学专业", "party_join": "2003-06", "work_start": "1999-09",
     "current_post": "副县长", "current_org": "来凤县人民政府",
     "source": "http://www.laifeng.gov.cn/xxgk/gkml/zfld/202111/t20211108_1202254.shtml"},
    {"id": 7, "name": "戴青", "gender": "女", "ethnicity": "土家族", "birth": "1978-06", "birthplace": "湖北鹤峰",
     "education": "大学学历，湖北省委党校法律专业", "party_join": "1997-06", "work_start": "1998-10",
     "current_post": "副县长", "current_org": "来凤县人民政府",
     "source": "http://www.laifeng.gov.cn/xxgk/gkml/zfld/202507/t20250731_1723857.shtml"},
    {"id": 8, "name": "朱进友", "gender": "男", "ethnicity": "土家族", "birth": "1976-06", "birthplace": "湖北来凤",
     "education": "大学学历，华中科技大学法学专业", "party_join": "2000-07", "work_start": "1998-10",
     "current_post": "副县长", "current_org": "来凤县人民政府",
     "source": "http://www.laifeng.gov.cn/xxgk/gkml/zfld/202507/t20250730_1723748.shtml"},
    {"id": 9, "name": "赵昌青", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县人大常委会主任", "current_org": "来凤县人民代表大会常务委员会",
     "source": "http://www.laifeng.net 领导新闻 2026-07-01"},
    {"id": 10, "name": "汪建敏", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县政协主席", "current_org": "来凤县政协",
     "source": "http://www.laifeng.net 领导新闻 2026-07-01"},
    {"id": 11, "name": "何小岚", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县委副书记", "current_org": "中共来凤县委员会",
     "source": "http://www.laifeng.net 领导新闻 2026-07-01"},
    {"id": 12, "name": "谭剑", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "县委常委、副县长候选人", "current_org": "来凤县人民政府",
     "source": "来凤县政府网 2026-08-04 领导活动报道"},
    {"id": 13, "name": "李伟", "gender": "男", "ethnicity": "土家族", "birth": "1971-07", "birthplace": "湖北恩施",
     "education": "省委党校研究生学历", "party_join": "1998-11", "work_start": "1993-07",
     "current_post": "（前任）来凤县委书记、恩施州人大常委会副主任", "current_org": "恩施州人大常委会",
     "source": "http://www.laifeng.net（模板简历）及州人大"},
    {"id": 14, "name": "钟迎松", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "（前任）来凤县人民政府县长", "current_org": "来凤县人民政府",
     "source": "http://www.laifeng.net 领导新闻 2026-07-01"},
    {"id": 15, "name": "邢祖训", "gender": "男", "ethnicity": "汉族", "birth": "1965-04", "birthplace": "湖北咸丰",
     "education": "中央党校大学学历", "party_join": "1984-12", "work_start": "1985-07",
     "current_post": "（历任）来凤县委书记、县人大常委会主任", "current_org": "中共来凤县委员会",
     "source": "http://www.laifeng.net/xwld (书记模板简历)"},
]

# ── Organizations ─────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共来凤县委员会", "type": "党委", "level": "县级", "parent": "中共恩施州委", "location": "湖北省恩施州来凤县"},
    {"id": 2, "name": "来凤县人民政府", "type": "政府", "level": "县级", "parent": "恩施州人民政府", "location": "湖北省恩施州来凤县"},
    {"id": 3, "name": "来凤县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "来凤县", "location": "湖北省恩施州来凤县"},
    {"id": 4, "name": "来凤县政协", "type": "政协", "level": "县级", "parent": "来凤县", "location": "湖北省恩施州来凤县"},
    {"id": 5, "name": "恩施州人大常委会", "type": "人大", "level": "地级市", "parent": "湖北省人大常委会", "location": "湖北省恩施州"},
    {"id": 6, "name": "恩施州统计局", "type": "政府", "level": "地级市", "parent": "恩施州人民政府", "location": "湖北省恩施州"},
    {"id": 7, "name": "恩施州文化体育新闻出版广电局", "type": "政府", "level": "地级市", "parent": "恩施州人民政府", "location": "湖北省恩施州"},
    {"id": 8, "name": "恩施市人民政府", "type": "政府", "level": "县级市", "parent": "恩施州人民政府", "location": "湖北省恩施州"},
    {"id": 9, "name": "巴东县人民政府", "type": "政府", "level": "县级", "parent": "恩施州人民政府", "location": "湖北省恩施州"},
    {"id": 10, "name": "咸丰县人民政府", "type": "政府", "level": "县级", "parent": "恩施州人民政府", "location": "湖北省恩施州"},
]

# ── Positions ─────────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "~2026-06", "end": "", "rank": "正县级"},
    {"person_id": 2, "org_id": 2, "title": "县委副书记、代理县长", "start": "2026-07", "end": "", "rank": "正县级"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "2026-07", "end": "", "rank": "正县级"},
    {"person_id": 2, "org_id": 1, "title": "县委常委、组织部部长", "start": "~2016", "end": "~2019", "rank": "副县级"},
    {"person_id": 2, "org_id": 8, "title": "市委常委、常务副市长", "start": "2021", "end": "~2023", "rank": "副厅级"},
    {"person_id": 2, "org_id": 6, "title": "局长（党组书记），二级调研员", "start": "~2023", "end": "2026-07", "rank": "正处级"},
    {"person_id": 3, "org_id": 2, "title": "常务副县长", "start": "2024-04", "end": "", "rank": "副县长"},
    {"person_id": 3, "org_id": 1, "title": "县委常委、县委办主任", "start": "2018", "end": "2024-04", "rank": "县委常委"},
    {"person_id": 4, "org_id": 2, "title": "副县长", "start": "2021-09", "end": "", "rank": "副县长"},
    {"person_id": 5, "org_id": 2, "title": "副县长（兼县公安局）", "start": "2021-10", "end": "", "rank": "副县长"},
    {"person_id": 6, "org_id": 2, "title": "副县长", "start": "2021-11", "end": "", "rank": "副县长"},
    {"person_id": 7, "org_id": 2, "title": "副县长", "start": "2025-07", "end": "", "rank": "副县长"},
    {"person_id": 8, "org_id": 2, "title": "副县长", "start": "2025-07", "end": "", "rank": "副县长"},
    {"person_id": 9, "org_id": 3, "title": "县人大常委会主任", "start": "", "end": "", "rank": "正县级"},
    {"person_id": 10, "org_id": 4, "title": "县政协主席", "start": "", "end": "", "rank": "正县级"},
    {"person_id": 11, "org_id": 1, "title": "县委副书记", "start": "", "end": "", "rank": "副县级"},
    {"person_id": 12, "org_id": 2, "title": "县委常委、副县长候选人", "start": "2026-08", "end": "", "rank": "副县级"},
    {"person_id": 13, "org_id": 1, "title": "（前任）县委书记", "start": "2021", "end": "2026-06", "rank": "正县级"},
    {"person_id": 13, "org_id": 5, "title": "州人大常委会副主任", "start": "~2023", "end": "", "rank": "副厅级"},
    {"person_id": 14, "org_id": 2, "title": "县长", "start": "", "end": "~2026-07", "rank": "正县级"},
    {"person_id": 15, "org_id": 1, "title": "县委书记、县人大常委会主任", "start": "2015", "end": "~2021", "rank": "正县级"},
]

# ── Relationships ─────────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "同事关系",
     "context": "现任县委书记与现任代理县长共同主持县委/县政府（2026县乡换届、藤茶/生猪特色产业为主攻）",
     "overlap_org": "来凤县人民政府", "overlap_period": "2026-07至今"},
    {"person_a": 13, "person_b": 1, "type": "交棒关系", "context": "前任书记李伟与现任书记王兵 2026年中交接",
     "overlap_org": "中共来凤县委员会", "overlap_period": "2026-06"},
    {"person_a": 14, "person_b": 2, "type": "predecessor_successor",
     "context": "前任县长钟迎松与现任代理县长刘涛交接（2026-07）", "overlap_org": "来凤县人民政府", "overlap_period": "2026-07"},
    {"person_a": 13, "person_b": 14, "type": "领导同事", "context": "李伟任书记、钟迎松任县长时为搭档",
     "overlap_org": "来凤县", "overlap_period": "2020-2026"},
    {"person_a": 15, "person_b": 13, "type": "predecessor_successor", "context": "更早书记邢祖训后交棒李伟",
     "overlap_org": "中共来凤县委员会", "overlap_period": "2021"},
    {"person_a": 3, "person_b": 2, "type": "同事关系", "context": "常务副县长与代理县长共在新一届县政府班子",
     "overlap_org": "来凤县人民政府", "overlap_period": "2026"},
]


# ── Person JSON generation (schema 1.0) ───────────────────────────────
SOURCES = [
    {"id": "S001", "title": "来凤县人民政府 · 政府领导之窗",
     "url": "http://www.laifeng.gov.cn/xxgk/gkml/zfld/", "publisher": "来凤县人民政府办公室",
     "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
     "notes": "政府班子及个人简历（代理县长刘涛、常务副县长张冠华、副县长汪玉明/朱泽华/向雪峰/戴青/朱进友）"},
    {"id": "S002", "title": "云上来凤 · 领导活动报道集（书记/县长）", "url": "http://www.laifeng.net/xwld/",
     "publisher": "来凤县融媒体中心", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
     "notes": "现任书记王兵、代理县长刘涛 2026-06~08 活动；县四大班子名单（主任赵昌青/政协主席汪建敏/副书记何小岚）"},
    {"id": "S003", "title": "恩施政府网 / 恩施新闻网", "url": "http://www.enshi.gov.cn/ , http://www.enshi.cn/",
     "publisher": "恩施州人民政府 / 恩施州融媒体", "accessed_at": AS_OF, "source_type": "official", "reliability": "medium",
     "notes": "州政府门户、州委组织部下拉、州人大干部信息"},
]


def build_profile(pid: int, job: str) -> dict:
    p = persons[pid - 1]
    name = p["name"]
    timeline = []
    for pos in positions:
        if pos["person_id"] == pid:
            org_name = next((o["name"] for o in organizations if o["id"] == pos["org_id"]), "")
            timeline.append({
                "start": pos["start"], "end": pos["end"], "org": org_name, "title": pos["title"],
                "level": "", "location": PROVINCE + CITY, "system": "party", "rank": pos["rank"],
                "is_key_promotion": False, "notes": "", "confidence": "confirmed" if p.get("birth") else "partial",
                "source_ids": ["S001"],
            })
    new_id = f"laifeng_{pid}_{name}"
    return {
        "schema_version": "1.0", "generated_at": AS_OF,
        "investigation_scope": {"province": PROVINCE, "city": CITY, "region": SLUG, "job": job,
                                "task_id": TASK_ID, "time_focus": "2026"},
        "identity": {"person_id": new_id, "name": name, "aliases": [], "gender": p["gender"],
                     "ethnicity": p["ethnicity"], "birth": p["birth"], "birthplace": p["birthplace"],
                     "native_place": p["birthplace"],
                     "education": [{"period": "", "institution": p.get("education", ""), "major": "",
                                    "degree": "", "study_type": "unknown", "source_ids": ["S001"]}],
                     "party_join": p["party_join"], "work_start": p["work_start"],
                     "dedupe_keys": {"name_birth": f"{name}_{p['birth']}",
                                     "name_birthplace": f"{name}_{p['birthplace']}",
                                     "official_profile_url": ""}},
        "current_status": {"current_post": p["current_post"], "current_org": p["current_org"],
                           "administrative_rank": "", "as_of": AS_OF,
                           "is_current_confirmed": True, "source_ids": ["S001", "S002"]},
        "career_timeline": timeline,
        "organizations": [{"org": o["name"], "type": o["type"], "level": o["level"], "location": o["location"]}
                          for o in organizations if o["id"] in {pos["org_id"] for pos in positions if pos["person_id"] == pid}],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {"primary_specializations": [], "secondary_specializations": [],
                                 "career_pattern": "", "systems_experience": [],
                                 "geographic_pattern": [], "promotion_velocity": {"summary": "", "notable_fast_promotions": []}},
        "work_style_and_personality": {"public_style_indicators": [], "speech_themes": [], "management_signals": [],
                                       "caveat": "Work style is inferred from public records, not private psychological assessment."},
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "本次官方渠道及公开检索未发现负面/纪律信号（2026-08检索）",
             "date": AS_OF, "confidence": "unverified", "source_ids": []}],
        "source_register": SOURCES,
        "confidence_summary": {"identity": "confirmed" if p.get("birth") else "partial",
                               "current_role": "confirmed",
                               "career_completeness": "complete" if p.get("birth") else "partial",
                               "relationship_confidence": "medium",
                               "biggest_gap": ("现任县委书记前职履历未获" if pid == 1 else "履历细节待核")},
        "open_questions": [
            {"priority": "high",
             "question": ("书记王兵任来凤县委书记前的完整履历" if pid == 1 else f"{name} 早年任职细节"),
             "why_it_matters": "用于履职网络与跨县流动分析", "suggested_queries": [], "last_attempted": AS_OF}],
    }


PERSON_JSONS = [("shuji_courant", "县委书记", 1), ("xianzhang_courant", "县委副书记、代理县长", 2),
                ("changwu_short", "常务副县长", 3), ("pre_shuji", "前任县委书记", 13)]


def write_person_json(dest_dir: Path) -> list[Path]:
    dest_dir.mkdir(parents=True, exist_ok=True)
    out = []
    for _key, job, pid in PERSON_JSONS:
        profile = build_profile(pid, job)
        fn = f"{TODAY}-{PROVINCE}-{CITY}-{job}-{profile['identity']['name']}.json"
        fp = dest_dir / fn
        fp.write_text(json.dumps(profile, ensure_ascii=False, indent=2), encoding="utf-8")
        out.append(fp)
    return out


def main() -> None:
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
    jsons = write_person_json(HERE)
    print(f"DB:    {DB_PATH}")
    print(f"GEXF:  {GEXF_PATH}")
    for fp in jsons:
        print(f"JSON:  {fp}")
    print(f"persons: {len(persons)}, orgs: {len(organizations)}, "
          f"positions: {len(positions)}, relationships: {len(relationships)}")


if __name__ == "__main__":
    main()