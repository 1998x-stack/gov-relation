#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 延边朝鲜族自治州 (Yanbian), 吉林省.

Task ID: jilin_延边朝鲜族自治州 | Level: 地级市(自治州) | Targets: 州委书记 & 州长 | Date: 2026-08-06

Note on target titles:
  A 自治州's two core leaders are 中共延边朝鲜族自治州委员会书记（州委书记）and
  延边朝鲜族自治州人民政府州长（州长）. The automatic task template said "市委书记/市长"
  which does not fit a 自治州; the two targets here are translated to 州委书记 & 州长.

Sources:
  - Wikipedia zh《胡家福》《洪庆 (1976年)》《延边朝鲜族自治州》 (官方任免时间线/籍贯/履历，二级)
  - 延边朝鲜族自治州人民政府官网 http://www.yanbian.gov.cn/zwgk_83/zzfld/ (州政府领导在挂名单，一级)
  - 央广网 2026-07-23（胡家福 2026 年仍任州委书记）
  - 南方都市报《洪庆履新吉林省政府秘书长》、城市晚报 2026-05（洪庆 2026.04 卸任州长）

Confidence:
  - 胡家福（州委书记）：Confirmed（Wikipedia 任免时间线 + 央广网 2026-07 仍为州委书记）
  - 洪庆（州长 2022-2026，现任吉林省秘书长）：Confirmed
  - 刘新钢（常务副州长）、胡福君（副州长）：Confirmed（州府官网简历）
  - 上官红君、段于建、尹朝晖、文金哲、郑权、窦庆国（副州长）：Confirmed（州府官网名单，简历不全）
  - 金寿浩（前任州长、2026 主动投案）：Confirmed（新华社/媒体）
  - 苏景华（原副州长，被查）：Confirmed（媒体）
  - 2026 现任州长继承人：Unverified（公开检索中州长一职未见在挂；州府官网副州长栏外无州长简历）
"""

import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

BASE = Path(__file__).resolve().parent
# Locate repo root from data/tmp/<id>/ build script (parents[0..3]) 
_REPO = BASE
for _ in range(3):
    if (_REPO / "gov_relation").is_dir():
        break
    _REPO = _REPO.parent
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from gov_relation.runner import run_build

SLUG = "延边朝鲜族自治州"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"
DB_PATH = str(BASE / f"{SLUG}_network.db")
GEXF_PATH = str(BASE / f"{SLUG}_network.gexf")

# ═══════════════════════════ Persons ═══════════════════════════
persons = [
    {"id": 1, "name": "胡家福", "gender": "男", "ethnicity": "汉族", "birth": "1967年10月",
     "birthplace": "山东省昌乐县", "education": "山东大学汉语言文学本科",
     "party_join": "1993年11月", "work_start": "1990年7月",
     "current_post": "州委书记", "current_org": "中共延边朝鲜族自治州委员会",
     "source": "https://zh.wikipedia.org/wiki/胡家福; http://www.yanbian.gov.cn/"},
    {"id": 2, "name": "洪庆", "gender": "男", "ethnicity": "朝鲜族", "birth": "1976年11月",
     "birthplace": "", "education": "东北师范大学经济学博士",
     "party_join": "2000年7月", "work_start": "1999年9月",
     "current_post": "州长（2022-2026，现已调任吉林省人民政府秘书长）", "current_org": "延边朝鲜族自治州人民政府",
     "source": "https://zh.wikipedia.org/wiki/洪庆_(1976年)"},
    {"id": 3, "name": "刘新钢", "gender": "男", "ethnicity": "汉族", "birth": "1974年10月",
     "birthplace": "", "education": "", "party_join": "2000年10月", "work_start": "1997年7月",
     "current_post": "州委常委、州政府党组副书记、常务副州长", "current_org": "延边朝鲜族自治州人民政府",
     "source": "http://www.yanbian.gov.cn/zwgk_83/zzfld/fzz/"},
    {"id": 4, "name": "胡福君", "gender": "男", "ethnicity": "汉族", "birth": "1973年10月",
     "birthplace": "", "education": "北京师范大学文学博士",
     "party_join": "1998年5月", "work_start": "2001年6月",
     "current_post": "州委常委、副州长", "current_org": "延边朝鲜族自治州人民政府",
     "source": "http://www.yanbian.gov.cn/zwgk_83/zzfld/zzfd/fzz/"},
    {"id": 5, "name": "上官红君", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "副州长", "current_org": "延边朝鲜族自治州人民政府",
     "source": "http://www.yanbian.gov.cn/zwgk_83/zzfld/zzfd/"},
    {"id": 6, "name": "段于建", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "副州长、州公安局局长", "current_org": "延边朝鲜族自治州人民政府",
     "source": "http://www.yanbian.gov.cn/zwgk_83/zzfld/zzfd/"},
    {"id": 7, "name": "尹朝晖", "gender": "女", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "副州长", "current_org": "延边朝鲜族自治州人民政府",
     "source": "http://www.yanbian.gov.cn/zwgk_83/zzfld/zzfd/"},
    {"id": 8, "name": "文金哲", "gender": "男", "ethnicity": "朝鲜族", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "副州长", "current_org": "延边朝鲜族自治州人民政府",
     "source": "http://www.yanbian.gov.cn/zwgk_83/zzfld/zzfd/"},
    {"id": 9, "name": "郑权", "gender": "男", "ethnicity": "朝鲜族", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "副州长", "current_org": "延边朝鲜族自治州人民政府",
     "source": "http://www.yanbian.gov.cn/zwgk_83/zzfld/zzfd/"},
    {"id": 10, "name": "窦庆国", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "副州长", "current_org": "延边朝鲜族自治州人民政府",
     "source": "http://www.yanbian.gov.cn/zwgk_83/zzfld/zzfd/"},
    {"id": 11, "name": "金寿浩", "gender": "男", "ethnicity": "朝鲜族", "birth": "1962年8月",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "前任州长（2019-2021，2026年主动投案被查）", "current_org": "",
     "source": "https://zh.wikipedia.org/wiki/延边朝鲜族自治州; 新华社/红星新闻 2026"},
    {"id": 12, "name": "苏景华", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "原副州长（2022名单成员，涉嫌违纪被审查）", "current_org": "",
     "source": "中国新闻网 2026（苏景华受查报道）"},
]

# ═══════════════════════════ Organizations ═══════════════════════════
organizations = [
    {"id": 1, "name": "中共延边朝鲜族自治州委员会", "type": "党委", "level": "地级(州)", "parent": "中共吉林省委员会", "location": "延边州"},
    {"id": 2, "name": "延边朝鲜族自治州人民政府", "type": "政府", "level": "地级(州)", "parent": "吉林省人民政府", "location": "延边州"},
    {"id": 3, "name": "延边朝鲜族自治州人民代表大会常务委员会", "type": "人大", "level": "地级(州)", "parent": "吉林省人大常委会", "location": "延边州"},
    {"id": 4, "name": "中国人民政治协商会议延边朝鲜族自治州委员会", "type": "政协", "level": "地级(州)", "parent": "吉林省政协", "location": "延边州"},
    {"id": 5, "name": "延边朝鲜族自治州公安局（州公安厅级）", "type": "政府", "level": "地级(州)", "parent": "延边朝鲜族自治州人民政府", "location": "延边州"},
    {"id": 6, "name": "中共延吉市委员会（州首府）", "type": "党委", "level": "县级", "parent": "中共延边朝鲜族自治州委员会", "location": "延吉市"},
    {"id": 7, "name": "中共吉林省委员会", "type": "党委", "level": "省级", "parent": "", "location": "长春市"},
    {"id": 8, "name": "吉林省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "长春市"},
    {"id": 9, "name": "吉林省公安厅", "type": "政府", "level": "省级", "parent": "吉林省人民政府", "location": "长春市"},
    {"id": 10, "name": "中共吉林省委政法委员会", "type": "党委", "level": "省级", "parent": "中共吉林省委员会", "location": "长春市"},
    {"id": 11, "name": "中华人民共和国公安部", "type": "党委/国务院部门", "level": "中央", "parent": "", "location": "北京"},
    {"id": 12, "name": "中国共产主义青年团吉林省委员会", "type": "群团", "level": "省级", "parent": "", "location": "长春市"},
]

# ═══════════════════════════ Positions ═══════════════════════════
positions = [
    # 胡家福
    {"person_id": 1, "org_id": 1, "title": "州委书记", "start_date": "2022-06", "end_date": "present", "rank": "正厅级/州委书记", "note": "吉林省委常委兼，2022年6月到任，2026-07仍任（央广网）"},
    {"person_id": 1, "org_id": 7, "title": "省委常委", "start_date": "2018-01", "end_date": "present", "rank": "副部级", "note": "吉林省委常委"},
    {"person_id": 1, "org_id": 7, "title": "省委常委、政法委书记、省公安厅厅长", "start_date": "2018-01", "end_date": "2020-03", "rank": "副部级", "note": "不再兼任省公安厅厅长为2020"},
    {"person_id": 1, "org_id": 7, "title": "省委常委、省委秘书长", "start_date": "2020-03", "end_date": "2022-06", "rank": "副部级", "note": ""},
    {"person_id": 1, "org_id": 8, "title": "副省长兼省公安厅党委书记、厅长", "start_date": "2015-08", "end_date": "2018-01", "rank": "副部级", "note": ""},
    {"person_id": 1, "org_id": 11, "title": "公安部办公厅主任、研究室主任", "start_date": "2011-09", "end_date": "2015-08", "rank": "正局级", "note": "公安部办公厅工作30余年"},
    {"person_id": 1, "org_id": 11, "title": "公安部办公厅副主任兼研究室主任", "start_date": "2006-09", "end_date": "2011-09", "rank": "", "note": ""},
    # 洪庆
    {"person_id": 2, "org_id": 2, "title": "州长", "start_date": "2022-01", "end_date": "2026-04", "rank": "州长（正厅级）", "note": "2022-01十四届州人大当选；2026-04卸任调省委办"},
    {"person_id": 2, "org_id": 2, "title": "州委副书记、州长", "start_date": "2021-11", "end_date": "2026-04", "rank": "州委副书记", "note": "2021-11代州长"},
    {"person_id": 2, "org_id": 6, "title": "州首府延吉市委书记（兼）", "start_date": "2019-07", "end_date": "2021-11", "rank": "县级正职", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "州委常委、州纪委书记、州监委主任", "start_date": "2016", "end_date": "2021-11", "rank": "州级", "note": "并任州委副书记"},
    {"person_id": 2, "org_id": 2, "title": "副州长", "start_date": "2012-2013", "end_date": "2016", "rank": "州级副职", "note": "36岁任延边州副州长"},
    {"person_id": 2, "org_id": 12, "title": "共青团吉林省委副书记", "start_date": "2011", "end_date": "2012-2013", "rank": "副厅级", "note": "2011-11选副书记"},
    {"person_id": 2, "org_id": 12, "title": "共青团吉林省委统战联络部部长", "start_date": "2007", "end_date": "2011", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 8, "title": "吉林省人民政府秘书长", "start_date": "2026-05", "end_date": "present", "rank": "正厅级", "note": "2026-04省政府党组成员，2026-05省政府秘书长"},
    # 刘新钢
    {"person_id": 3, "org_id": 2, "title": "常务副州长、州政府党组副书记", "start_date": "unknown", "end_date": "present", "rank": "副厅级", "note": "州委常委，主持州政府常务工作"},
    {"person_id": 3, "org_id": 1, "title": "州委常委", "start_date": "unknown", "end_date": "present", "rank": "州委()", "note": ""},
    # 胡福君
    {"person_id": 4, "org_id": 2, "title": "副州长", "start_date": "unknown", "end_date": "present", "rank": "副厅级", "note": "分管民生"},
    {"person_id": 4, "org_id": 1, "title": "州委常委", "start_date": "unknown", "end_date": "present", "rank": "州委()", "note": ""},
    # 其他副州长
    {"person_id": 5, "org_id": 2, "title": "副州长", "start_date": "unknown", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副州长", "start_date": "unknown", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 6, "org_id": 5, "title": "州公安局局长", "start_date": "unknown", "end_date": "present", "rank": "副厅级", "note": "公安"},
    {"person_id": 7, "org_id": 2, "title": "副州长", "start_date": "unknown", "end_date": "present", "rank": "副厅级", "note": "女"},
    {"person_id": 8, "org_id": 2, "title": "副州长", "start_date": "unknown", "end_date": "present", "rank": "副厅级", "note": "朝鲜族"},
    {"person_id": 9, "org_id": 2, "title": "副州长", "start_date": "unknown", "end_date": "present", "rank": "副厅级", "note": "朝鲜族"},
    {"person_id": 10, "org_id": 2, "title": "副州长", "start_date": "unknown", "end_date": "present", "rank": "副厅级", "note": ""},
    # 金寿浩
    {"person_id": 11, "org_id": 2, "title": "州长", "start_date": "2019-01", "end_date": "2021-10", "rank": "州长（正厅级）", "note": "前任州长，后任州人大常委会主任"},
    {"person_id": 11, "org_id": 3, "title": "州人大常委会主任", "start_date": "2021-11", "end_date": "2023", "rank": "正厅级", "note": "2021-11转任，2023不再"},
    # 苏景华
    {"person_id": 12, "org_id": 2, "title": "副州长", "start_date": "unknown", "end_date": "unknown", "rank": "副厅级", "note": "被查，涉嫌违纪"},
]

# ═══════════════════════════ Relationships ═══════════════════════════
relationships = [
    {"person_a": 1, "person_b": 2, "type": "决策搭档", "context": "州委书记与州长，党政班子搭档（2022-2026）", "overlap_org": "中共延边州委/延边州人民政府", "overlap_period": "2022-2026"},
    {"person_a": 2, "person_b": 11, "type": "前任-继任", "context": "金寿浩（2019-2021州长）后洪庆接任，二人素不相干但走同一条州长位", "overlap_org": "延边州人民政府", "overlap_period": "2021-2022"},
    {"person_a": 1, "person_b": 3, "type": "班子/上下级", "context": "刘新钢（州委常委、常务副州长）在州委常委会上与州委书记胡家福有直接上下级", "overlap_org": "中共延边州委", "overlap_period": "present"},
    {"person_a": 2, "person_b": 3, "type": "班子/上下级", "context": "刘新钢（常务副州长）协助州长洪庆主持州政府日常", "overlap_org": "延边州人民政府", "overlap_period": "2022-2026"},
    {"person_a": 1, "person_b": 4, "type": "班子交集", "context": "胡福君任州委常委、属州委常委会，与州委书记胡家福同班子", "overlap_org": "中共延边州委", "overlap_period": "present"},
    {"person_a": 2, "person_b": 4, "type": "班子交集", "context": "胡福君为州政府副市长，与州长洪庆日常工作交集", "overlap_org": "延边州人民政府", "overlap_period": "2022-2026"},
    {"person_a": 6, "person_b": 12, "type": "前任-继任/班子", "context": "段于建（公安）与苏景华（原副州长）同曾在州政府班子（2022），苏景华被查", "overlap_org": "延边州人民政府", "overlap_period": "2022"},
    {"person_a": 1, "person_b": 12, "type": "工作交集", "context": "苏景华曾任副州长（延边州班子），与州委书记胡家福工作关系，2026年被查", "overlap_org": "延边州人民政府", "overlap_period": "2022"},
]

# ═══════════════════════════ Person JSON ═══════════════════════════
SOURCE_REGISTER = [
    {"id": "S001", "title": "Wikipedia zh《胡家福》", "url": "https://zh.wikipedia.org/wiki/胡家福", "publisher": "Wikipedia", "published_at": "", "accessed_at": AS_OF, "source_type": "database", "reliability": "medium", "notes": "州委书记；现状经央广网2026-07核实"},
    {"id": "S002", "title": "Wikipedia zh《洪庆 (1976年)》", "url": "https://zh.wikipedia.org/wiki/洪庆_(1976年)", "publisher": "Wikipedia", "published_at": "", "accessed_at": AS_OF, "source_type": "database", "reliability": "medium", "notes": "州长 2021-2026，2026-05省政府秘书长"},
    {"id": "S003", "title": "延边州人民政府·州政府领导", "url": "http://www.yanbian.gov.cn/zwgk_83/zzfld/", "publisher": "延边朝鲜族自治州人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "在任州级领导班子+副州长名单（刘新钢等8人）"},
    {"id": "S004", "title": "州政府 副州长简历页", "url": "http://www.yanbian.gov.cn/zwgk_83/zzfld/", "publisher": "延边州人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "刘新钢/胡福君 简历"},
    {"id": "S005", "title": "央广网 2026-07-23 胡家福调研", "url": "https://www.cnr.cn/", "publisher": "中央人民广播电台", "published_at": "2026-07-23", "accessed_at": AS_OF, "source_type": "media", "reliability": "high", "notes": "胡家福2026-07仍任州委书记"},
    {"id": "S006", "title": "南方都市报/城市晚报：洪庆履新省政府秘书长", "url": "https://www.sohu.com/", "publisher": "南方都市报/城市晚报", "published_at": "2026-05", "accessed_at": AS_OF, "source_type": "media", "reliability": "medium", "notes": "洪庆2026-04任省政府党组成员，2026-05任省政府秘书长"},
    {"id": "S007", "title": "新华社/红星新闻：金寿浩主动投案", "url": "", "publisher": "新华社/红星新闻", "published_at": "2026", "accessed_at": AS_OF, "source_type": "media", "reliability": "medium", "notes": "前任州长金寿浩2026被查/主动投案"},
]

def build_person_file(name, current_post, identity, timeline, relations, orgs, big_gap, qs=None):
    p = BASE / f"{TODAY}-吉林省-延边朝鲜族自治州-{current_post}-{name}.json"
    data = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {"province": "吉林省", "city": "延边朝鲜族自治州", "region": "延边朝鲜族自治州",
                                "job": current_post, "task_id": "jilin_延边朝鲜族自治州", "time_focus": "2022-2026"},
        "identity": {"person_id": f"yanbian_{name}", "name": name, "aliases": [],
                     "gender": identity.get("gender", ""), "ethnicity": identity.get("ethnicity", ""),
                     "birth": identity.get("birth", ""), "birthplace": identity.get("birth", ""),
                     "native_place": identity.get("native_place", ""),
                     "education": identity.get("education", []),
                     "party_join": identity.get("party_join", ""), "work_start": identity.get("work_start", ""),
                     "dedupe_keys": {"name_birth": f"{name}_{identity.get('birth','')}",
                                     "name_birthplace": f"{name}_{identity.get('birthplace','')}",
                                     "official_profile_url": ""}},
        "current_status": {"current_post": current_post, "current_org": identity.get("current_org", ""),
                           "administrative_rank": identity.get("rank", ""), "as_of": AS_OF,
                           "is_current_confirmed": identity.get("is_current_confirmed", True),
                           "source_ids": identity.get("source_ids", ["S001", "S003"])},
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
                               "current_role": identity.get("current_role_conf", "confirmed"),
                               "career_completeness": "complete" if len(timeline or []) > 5 else ("partial" if timeline else "thin"),
                               "relationship_confidence": "medium", "biggest_gap": big_gap},
        "open_questions": qs or [{"priority": "critical", "question": big_gap, "why_it_matters": "任职网络分析",
                                  "suggested_queries": [f"{name} 简历"], "last_attempted": AS_OF}],
    }
    with open(p, "w", encoding="utf-8") as fp:
        json.dump(data, fp, ensure_ascii=False, indent=2)
    print("  person JSON:", p.name)


def write_persons_files():
    # ── 胡家福（州委书记） ──
    build_person_file(
        "胡家福", "州委书记",
        {"gender": "男", "ethnicity": "汉族", "birth": "1967年10月", "birthplace": "山东省昌乐县",
         "native_place": "山东昌乐",
         "education": [{"period": "1986-1990", "institution": "山东大学", "major": "汉语言文学", "degree": "大学文学学士", "study_type": "full_time", "source_ids": ["S001"]}],
         "party_join": "1993年11月", "work_start": "1990年7月", "current_org": "中共延边朝鲜族自治州委员会",
         "rank": "州委书记（省委常委兼）", "is_current_confirmed": True, "source_ids": ["S001", "S005"]},
        [{"start": "2022-06", "end": "present", "org": "中共延边朝鲜族自治州委员会", "title": "州委书记", "level": "地级(州)", "system": "party", "rank": "正厅级", "is_key_promotion": True, "notes": "2022-06调任，2026-07仍任（央广网）", "confidence": "confirmed", "source_ids": ["S001", "S005"]},
         {"start": "2018-01", "end": "present", "org": "中共吉林省委", "title": "省委常委（政法委书记→省委秘书长）", "level": "省级", "system": "party", "rank": "副部级", "is_key_promotion": True, "notes": "2020-03后兼省委秘书长", "confidence": "confirmed", "source_ids": ["S001"]},
         {"start": "2015-08", "end": "2018-01", "org": "吉林省人民政府·吉林省公安厅", "title": "副省长兼省公安厅党委书记、厅长", "level": "省级", "system": "government", "rank": "副部级", "is_key_promotion": True, "notes": "2017-07兼省委政法委书记", "confidence": "confirmed", "source_ids": ["S001"]},
         {"start": "2011-09", "end": "2015-08", "org": "中华人民共和国公安部", "title": "公安部办公厅主任兼研究室主任", "level": "中央", "system": "party", "rank": "正局级", "is_key_promotion": True, "notes": "公安系统深耕", "confidence": "confirmed", "source_ids": ["S001"]},
         {"start": "1990-07", "end": "2011-09", "org": "中华人民共和国公安部办公厅", "title": "办公厅副主任/研究室主任/第四研究所副所长等", "level": "中央", "system": "party", "rank": "", "notes": "公安部办公厅工作21年", "confidence": "confirmed", "source_ids": ["S001"]}],
        [{"person": "洪庆", "person_id": "yanbian_洪庆", "relationship_type": "overlap", "strength": "strong", "evidence": "州委书记与州长，党政班子搭档", "overlap_org": "中共延边州委/延边州人民政府", "overlap_period": "2022-2026", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
         {"person": "刘新钢", "person_id": "yanbian_刘新钢", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "刘新钢州委常委，直接接受州委书记领导", "overlap_org": "中共延边州委", "overlap_period": "present", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S003"]},
         {"person": "苏景华", "person_id": "yanbian_苏景华", "relationship_type": "work_intersection", "strength": "medium", "evidence": "原副州长调查中被发现", "overlap_org": "延边州人民政府", "overlap_period": "2022", "direction": "undirected", "confidence": "plausible", "source_ids": ["S007"]}],
        [{"id": "yanbian_州委", "name": "中共延边朝鲜族自治州委员会", "type": "党委", "level": "地级(州)", "location": "延边州"},
         {"id": "yanbian_州政府", "name": "延边朝鲜族自治州人民政府", "type": "政府", "level": "地级(州)", "location": "延边州"}],
        "胡家福完整教育背景与公安部21年晋升的具体时间节点；前任职去向（是否仍在书记位截至2026-08）",
        [{"priority": "medium", "question": "胡家福在延边州委书记任上的具体分工与离开中央政法委后的省级角色", "why_it_matters": "晋升路径与省级网络", "suggested_queries": ["胡家福 延边 分工"], "last_attempted": AS_OF}],
    )

    # ── 洪庆（州长 2022-2026，现任吉林省秘书长） ──
    build_person_file(
        "洪庆", "州长",
        {"gender": "男", "ethnicity": "朝鲜族", "birth": "1976年11月", "birthplace": "",
         "native_place": "",
         "education": [{"period": "1995-1999", "institution": "东北师范大学", "major": "", "degree": "本科", "study_type": "full_time", "source_ids": ["S002"]},
                       {"period": "", "institution": "东北师范大学", "major": "政治学理论", "degree": "法学硕士（在职）", "study_type": "part_time", "source_ids": ["S002"]},
                       {"period": "", "institution": "东北师范大学", "major": "世界经济", "degree": "经济学博士（在职）", "study_type": "part_time", "source_ids": ["S002"]}],
         "party_join": "2000年7月", "work_start": "1999年9月", "current_org": "延边朝鲜族自治州人民政府",
         "rank": "州长（正厅级），现任吉林省人民政府秘书长", "is_current_confirmed": False, "source_ids": ["S002", "S006"]},
        [{"start": "2026-05", "end": "present", "org": "吉林省人民政府", "title": "省政府秘书长、省政府党组成员", "level": "省级", "system": "government", "rank": "正厅级", "is_key_promotion": True, "notes": "2026-04任省政府党组成员，2026-05任秘书长", "confidence": "confirmed", "source_ids": ["S006"]},
         {"start": "2021-11", "end": "2026-04", "org": "延边朝鲜族自治州人民政府", "title": "州长（州委副书记、州政府党组书记）", "level": "地级(州)", "system": "government", "rank": "州长", "is_key_promotion": True, "notes": "2022-01州人代会当选；2026-04卸任", "confidence": "confirmed", "source_ids": ["S002", "S006"]},
         {"start": "2019-07", "end": "2021-11", "org": "中共延吉市委员会", "title": "州首府延吉市委书记（州委常委兼）", "level": "县级", "system": "party", "rank": "县级正职", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S002"]},
         {"start": "2012-2013", "end": "2019-07", "org": "中共延边州委/延边州人民政府", "title": "州委常委、州纪委书记、州监委主任、副州长、州委副书记", "level": "地级(州)", "system": "party", "rank": "州级", "notes": "36岁任副州长", "confidence": "confirmed", "source_ids": ["S002"]},
         {"start": "2011", "end": "2012-2013", "org": "共青团吉林省委", "title": "团省委副书记、省青联常务副主席", "level": "省级", "system": "organization", "rank": "副厅级", "is_key_promotion": True, "notes": "团干部成长路径", "confidence": "confirmed", "source_ids": ["S002"]},
         {"start": "2006", "end": "2011", "org": "共青团吉林省委", "title": "少年部部长→统战联络部部长", "level": "省级", "system": "organization", "rank": "正处级", "notes": "", "confidence": "confirmed", "source_ids": ["S002"]},
         {"start": "1999-09", "end": "2006", "org": "东北师范大学", "title": "团委书记/辅导员/校团委副书记", "level": "", "system": "education", "rank": "", "notes": "高校团干部出身", "confidence": "confirmed", "source_ids": ["S002"]}],
        [{"person": "胡家福", "person_id": "yanbian_胡家福", "relationship_type": "overlap", "strength": "strong", "evidence": "州委书记与州长搭档", "overlap_org": "中共延边州委/延边州政府", "overlap_period": "2022-2026", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
         {"person": "金寿浩", "person_id": "yanbian_金寿浩", "relationship_type": "predecessor_successor", "strength": "medium", "evidence": "洪庆2021-11接任金寿浩州长位", "overlap_org": "延边州人民政府", "overlap_period": "2021", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
         {"person": "刘新钢", "person_id": "yanbian_刘新钢", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "常务副州长协助州长主持州政府工作", "overlap_org": "延边州人民政府", "overlap_period": "2022-2026", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S003"]}],
        [{"id": "yanbian_州政府", "name": "延边朝鲜族自治州人民政府", "type": "政府", "level": "地级(州)", "location": "延边州"},
         {"id": "yanbian_州委", "name": "中共延边朝鲜族自治州委员会", "type": "党委", "level": "地级(州)", "location": "延边州"},
         {"id": "jilin_省政府", "name": "吉林省人民政府", "type": "政府", "level": "省级", "location": "长春市"}],
        "洪庆出生地/籍贯；延边州委常委→纪委书记的确切时间；省委秘书长任上作为",
        )

    # ── 刘新钢（常务副州长，现任州政府实际运行核心） ──
    build_person_file(
        "刘新钢", "常务副州长",
        {"gender": "男", "ethnicity": "汉族", "birth": "1974年10月", "birthplace": "",
         "education": [], "party_join": "2000年10月", "work_start": "1997年7月",
         "current_org": "延边朝鲜族自治州人民政府", "rank": "副厅级（常务）", "is_current_confirmed": True, "source_ids": ["S003", "S004"]},
        [{"start": "unknown", "end": "present", "org": "延边朝鲜族自治州人民政府", "title": "常务副州长、州政府党组副书记", "level": "地级(州)", "system": "government", "rank": "副厅级", "is_key_promotion": True, "notes": "州委常委，主持州政府常务工作", "confidence": "confirmed", "source_ids": ["S004"]},
         {"start": "unknown", "end": "present", "org": "中共延边州委", "title": "州委常委", "level": "地级(州)", "system": "party", "rank": "", "confidence": "confirmed", "source_ids": ["S003"]}],
        [{"person": "胡家福", "person_id": "yanbian_胡家福", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "州委常委直接受州委书记领导", "overlap_org": "中共延边州委", "overlap_period": "present", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S003"]},
         {"person": "洪庆", "person_id": "yanbian_洪庆", "relationship_type": "overlap", "strength": "strong", "evidence": "常务副州长协助州长，州长离任后代管州政府运行", "overlap_org": "延边州人民政府", "overlap_period": "2022-2026", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]}],
        [{"id": "yanbian_州政府", "name": "延边朝鲜族自治州人民政府", "type": "政府", "level": "地级(州)", "location": "延边州"}],
        "刘新钢任常务副州长前履历；其是否在新州长到任前暂行州长职权",
        )

    # ── 金寿浩（前任州长，2026被查） ──
    build_person_file(
        "金寿浩", "前任州长",
        {"gender": "男", "ethnicity": "朝鲜族", "birth": "1962年8月", "birthplace": "",
         "education": [], "party_join": "中共党员", "work_start": "",
         "current_org": "", "rank": "州长（正厅级，已卸任）",
         "is_current_confirmed": False, "source_ids": ["S002", "S007"]},
        [{"start": "2019-01", "end": "2021-10", "org": "延边朝鲜族自治州人民政府", "title": "州长", "level": "地级(州)", "system": "government", "rank": "州长", "is_key_promotion": True, "notes": "前任州长", "confidence": "confirmed", "source_ids": ["S002"]},
         {"start": "2021-11", "end": "2023", "org": "延边朝鲜族自治州人民代表大会", "title": "州人大常委会主任", "level": "地级(州)", "system": "party", "rank": "正厅级", "notes": "转任人大", "confidence": "plausible", "source_ids": ["S002"]},
         {"start": "2026", "end": "", "org": "", "title": "主动投案、接受审查调查", "level": "", "system": "", "rank": "", "notes": "辞去州长近三年后2026年主动投案（纪检）", "confidence": "confirmed", "source_ids": ["S007"]}],
        [{"person": "洪庆", "person_id": "yanbian_洪庆", "relationship_type": "predecessor_successor", "strength": "medium", "evidence": "州长交接", "overlap_org": "延边州人民政府", "overlap_period": "2021", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S007"]}],
        [{"id": "yanbian_州政府", "name": "延边朝鲜族自治州人民政府", "type": "政府", "level": "地级(州)", "location": "延边州"}],
        "金寿浩完整履历、出生地籍贯，及其被查的具体案由",
    )


def main():
    print(f"[{SLUG}] 构建 SQLite DB + GEXF ...")
    run_build(slug=SLUG, persons=persons, organizations=organizations,
              positions=positions, relationships=relationships,
              db_path=DB_PATH, gexf_path=GEXF_PATH)
    _verify_db()
    write_persons_files()
    print(f"[{SLUG}] 完成：{DB_PATH}\n{GEXF_PATH}\npersons JSON 若干")


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
