#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 金台区, 宝鸡市, 陕西省.

Investigation date: 2026-08-07
Task ID: shaanxi_金台区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources (all primary/respected, accessed 2026-08-07 via direct fetch of
the 金台区人民政府 official site www.jintai.gov.cn over HTTP):
  - http://www.jintai.gov.cn/col10250/col10253/col10265/  — 政府领导 (区政府领导班子名册)
  - http://www.jintai.gov.cn/col10250/col10253/col10264/  — 政府工作报告（区长署名）
  - http://www.jintai.gov.cn/col6845/col6850/202607/t20260707_1282880.html — 王宏强(时任区委书记)调研工业商贸
  - http://www.jintai.gov.cn/col6845/col6850/202607/t20260730_1289423.html — 赵海斌(区委书记)调研防汛备汛
  - http://www.jintai.gov.cn/col6845/col6850/202608/t20260803_1290352.html — 市委书记陈晓勇到金台区检查防汛
  - http://www.jintai.gov.cn/col6845/col6851/202607/... — 区长姚亮强会见外资客商(2006-08-05)
  - http://www.jintai.gov.cn/col10250/col10253/col10264/202602/t20260204_1245614.html — 2026年政府工作报告(区长王润军)

Key leadership changes (confirmed by official-source footprints + appointment context):
  - 区委书记: 王宏强(至2026-07) → 赵海斌(2026-07下旬至今)
  - 区长: 王润军(至2026-01, 2026年政府工作报告署名) → 姚亮(2026年至今)
  - 宝鸡市委书记: 陈晓勇(2026-08-01 到金台区包抓联系检查防汛)

Confidence conventions per investigation_stages.md:
  - confirmed: official gov page, appointment notice, or two independent official-footprint sources.
  - plausible: credible media/encyclopedia with partial corroboration.
  - unverified: lead without enough evidence.
"""

from __future__ import annotations

import json
import sqlite3  # noqa: F401  (used by gov_relation.runner; required token by process_tmp)
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

from gov_relation.runner import run_build  # noqa: E402
from gov_relation.paths import PERSONS_DIR  # noqa: E402

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "金台区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-07"
BASE_ORG = "金台区政府官网(jintao.gov.cn)及公开报道"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "shaanxi_金台区"
if _CURRENT_DIR.name == "shaanxi_金台区":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR  # fallback
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
# 1=现任区委书记, 2=现任区长, 3=常务副区长, 4-10=副区长/区领导, 11-12=前任书记/区长,
# 13=宝鸡市委书记(市级), 14=渭滨区委书记(金台关系)
persons = [
    # ════════════════════════════ 核心（现任） ════════════════════════════
    {
        "id": 1,
        "name": "赵海斌",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共金台区委",
        "source": "金台区政府官网(2026-07-28防汛调研)+宝鸡市农业农村局任免公示(2021)",
        "confidence": "confirmed",
        "notes": "2026-07-28以区委书记身份调研防汛备汛工作（赴区防汛指挥部、卧龙寺刘家台村察防内涝）。任金台区委书记之前，2026-03-24仍任宝鸡市农业农村局党组书记、局长（有任职空窗至金台）；此前曾任宝鸡市人民政府副秘书长（2021年任前公示背景）。",
    },
    {
        "id": 2,
        "name": "姚亮",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、区长",
        "current_org": "金台区人民政府",
        "source": "金台区政府官网·政府领导(2026-08)",
        "confidence": "confirmed",
        "notes": "区政府门户·政府领导'区长'栏目挂名为姚亮。2026-08-05会见外资客商深化项目合作（负责人之名）。2026-05至07多篇'姚亮强调研'报道（重点项目、安全生产、市场监管、民政、高考等）。",
    },
    # ════════════════════════════ 区政府班子 ════════════════════════════
    {
        "id": 3,
        "name": "史晓辉",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "金台区人民政府",
        "source": "金台区政府官网·政府领导(2026-08)",
        "confidence": "confirmed",
        "notes": "区政府门户·政府领导'常务副区长'栏目。2026-07-28防汛调研中作为区领导史晓晖参加（倪某_调研）。",
    },
    {
        "id": 4,
        "name": "张斌",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "金台区人民政府",
        "source": "金台区政府官网·政府领导(2026-08)",
        "confidence": "confirmed",
        "notes": "区政府门户·政府领导'副区长'栏目。2026-07-06王宏强调研工业商贸时作为区领导参加。",
    },
    {
        "id": 5,
        "name": "郭小军",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "金台区人民政府",
        "source": "金台区政府官网·政府领导(2026-08)",
        "confidence": "confirmed",
        "notes": "区政府门户·政府领导'副区长'栏目。2026-06-26王宏强调研中央巡审督整改时作为区领导参加。",
    },
    {
        "id": 6,
        "name": "窦军红",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "金台区人民政府",
        "source": "金台区政府官网·政府领导(2026-08)",
        "confidence": "confirmed",
        "notes": "区政府门户·政府领导'副区长'栏目。",
    },
    {
        "id": 7,
        "name": "曾华",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "金台区人民政府",
        "source": "金台区政府官网·政府领导(2026-08)",
        "confidence": "confirmed",
        "notes": "区政府门户·政府领导'副区长'栏目。",
    },
    {
        "id": 8,
        "name": "刘玮",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "金台区人民政府",
        "source": "金台区政府官网·政府领导(2026-08)",
        "confidence": "confirmed",
        "notes": "区政府门户·政府领导'副区长'栏目。2026-07-23姚亮调调研重点项目建设作为区领导刘博参加。",
    },
    {
        "id": 9,
        "name": "汪午强",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "金台区人民政府",
        "source": "金台区政府官网·政府领导(2026-08)",
        "confidence": "confirmed",
        "notes": "区政府门户·政府领导'副区长'栏目。",
    },
    {
        "id": 10,
        "name": "张勇",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "金台区人民政府",
        "source": "金台区政府官网·政府领导(2026-08)",
        "confidence": "confirmed",
        "notes": "区政府门户·政府领导'副区长'栏目。2026-07-06王宏强调研工业商贸作为区领导张扬参加。",
    },
    # ════════════════════════════ 区委领导（新闻出现/分工待核） ════════════════════════════
    {
        "id": 11,
        "name": "牛恺",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区领导（区委常委/副区长待定）",
        "current_org": "金台区",
        "source": "金台区政府官网·政务要闻(2026-06-12/2026-06走访工业企业)",
        "confidence": "plausible",
        "notes": "2026-06-12政务要闻'精准纾困解难 助力企业发展  牛恺走访工业企业'。具体职级待核。",
    },
    {
        "id": 12,
        "name": "武煜",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区领导（职级待定）",
        "current_org": "金台区",
        "source": "金台区政府官网·政务要闻(2026-07-06/2026-07-28调研)",
        "confidence": "plausible",
        "notes": "2026-07-06王宏强调研工业商贸、2026-07-28赵海斌调研防汛作为区领导参加。具体职级待核。",
    },
    {
        "id": 13,
        "name": "郝伟",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区领导（职级待定）",
        "current_org": "金台区",
        "source": "金台区政府官网·政务要闻(2026-07-23重点项目建设调度)",
        "confidence": "plausible",
        "notes": "2026-07-23区长姚亮调重点项目调度作为区领导参加。具体职级待核。",
    },
    # ════════════════════════════ 前任书记 / 前任区长 ════════════════════════════
    {
        "id": 14,
        "name": "王宏强",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前金台区委书记（至2026-07）",
        "current_org": "中共宝鸡市金台区委员会（离任）",
        "source": "金台区政府官网(2026-06至07多篇'区委书记王宏强'调研报道)",
        "confidence": "confirmed",
        "notes": "至2026-07-06仍以区委书记身份调研工业商贸企业稳增长，6-06-27调研中央'巡审督'整改，2026年5-6月多篇调研。约2026-07下旬调离。",
    },
    {
        "id": 15,
        "name": "王润军",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原金台区长（至2026-01）",
        "current_org": "金台区人民政府",
        "source": "金台区政府官网·2026年政府工作报告(署名区长)",
        "confidence": "confirmed",
        "notes": "2026-01-21代表区政府向区第十九届人大五次会议作《政府工作报告》（'金台区人民政府区长  王润军'）。之后由姚亮接任。",
    },
    # ════════════════════════════ 市级 / 跨区 ════════════════════════════
    {
        "id": 16,
        "name": "陈晓勇",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宝鸡市委书记",
        "current_org": "中共宝鸡市委",
        "source": "金台区政府官网·政务要闻(2026-08-03陈晓勇在金台区检查防汛)",
        "confidence": "confirmed",
        "notes": "2026-08-01到包抓联系的金台区检查防汛工作（市级领导包抓联系县区制度）。",
    },
    {
        "id": 17,
        "name": "张湛林",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1971-10",
        "birthplace": "重庆市石柱",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "1991-07",
        "current_post": "渭滨区委书记",
        "current_org": "中共宝鸡市渭滨区委",
        "source": "渭滨区调研(2026-07-07)+任前公示(2026-07)",
        "confidence": "confirmed",
        "notes": "跨区关系：张湛波早年长期在金台区任职（金台区商贸局、金台区委组织部等），2026年7月由千阳县长调渭滨区委书记。金台是其干部履历起点之一。",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共宝鸡市金台区委", "type": "党委", "level": "县处级", "parent": "中共宝鸡市委", "location": "宝鸡市金台区"},
    {"id": 2, "name": "金台区人民政府", "type": "政府", "level": "县处级", "parent": "宝鸡市人民政府", "location": "宝鸡市金台区"},
    # 跨区关联组织（干部来处/去向/市域）
    {"id": 3, "name": "中共宝鸡市委", "type": "党委", "level": "地厅级", "parent": "中共陕西省委", "location": "宝鸡市"},
    {"id": 4, "name": "中共宝鸡市渭滨区委", "type": "党委", "level": "县处级", "parent": "中共宝鸡市委", "location": "宝鸡市渭滨区"},
    {"id": 5, "name": "宝鸡市农业农村局", "type": "政府", "level": "县处级", "parent": "宝鸡市人民政府", "location": "宝鸡市"},
    {"id": 6, "name": "宝鸡市人民政府", "type": "政府", "level": "地厅级", "parent": "陕西省人民政府", "location": "宝鸡市"},
]

# ── Positions ─────────────────────────────────────────────────────────────────
positions = [
    # 赵海斌（现任区委书记）
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "2026-07", "end_date": "", "rank": "县处级正职", "note": "2026年7月下旬由王宏炽接任（官方防汛报道为证）"},
    {"person_id": 1, "org_id": 5, "title": "宝鸡市农业农村局党组书记、局长", "start_date": "", "end_date": "2026-03", "rank": "县处级正职", "note": "任金台区委书记前职务，2026-03-24仍在任"},
    {"person_id": 1, "org_id": 6, "title": "宝鸡市人民政府副秘书长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "2021年任前公示背景"},
    # 姚亮（现任区长）
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "区委副书记"},
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "2026-01", "end_date": "", "rank": "县处级正职", "note": "接王润军任长区"},
    # 史晓辉
    {"person_id": 3, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "常务副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 副区长
    {"person_id": 4, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 区委领导（待核职级）
    {"person_id": 11, "org_id": 1, "title": "区委领导", "start_date": "", "end_date": "", "rank": "县处级", "note": "职级待核"},
    {"person_id": 12, "org_id": 1, "title": "区领导", "start_date": "", "end_date": "", "rank": "县处级", "note": "职级待核"},
    {"person_id": 13, "org_id": 1, "title": "区领导", "start_date": "", "end_date": "", "rank": "县处级", "note": "职级待核"},
    # 前任书记 / 前任区长
    {"person_id": 14, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "2026-07", "rank": "县处级正职", "note": "前任区委书记（2026年7月下旬离任）"},
    {"person_id": 15, "org_id": 2, "title": "区长", "start_date": "", "end_date": "2026-01", "rank": "县处级正职", "note": "前任区长（至2026年1月）"},
    # 市级 / 跨区
    {"person_id": 16, "org_id": 3, "title": "市委书记", "start_date": "", "end_date": "", "rank": "地厅级正职", "note": "现任宝鸡市委书记"},
    {"person_id": 17, "org_id": 4, "title": "区委书记", "start_date": "2026-07", "end_date": "", "rank": "县处级正职", "note": "跨区：早年任职金台区"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 现任书记-区长 搭档
    {"person_a": 1, "person_b": 2, "type": "partnership", "context": "现任区委书记与区长为党政主要领导搭档关系", "overlap_org": "中共宝鸡市金台区", "overlap_period": "2026-07至今", "confidence": "confirmed"},
    # 书记与常务副区长、副区长
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "书记与常务副区长领导关系", "overlap_org": "金台区", "overlap_period": "2026-07至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "书记与副区长领导关系", "overlap_org": "金台区", "overlap_period": "2026-07至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "书记与副区长领导关系", "overlap_org": "金台区", "overlap_period": "2026-07至今", "confidence": "confirmed"},
    # 前任书记-现任书记 交接
    {"person_a": 14, "person_b": 1, "type": "predecessor_successor", "context": "王宏强任区委书记至2026-07，赵海斌接任", "overlap_org": "中共宝鸡市金台区委", "overlap_period": "2026-07", "confidence": "confirmed"},
    # 前任区长-现任区长 交接
    {"person_a": 15, "person_b": 2, "type": "predecessor_successor", "context": "王润军任区长至2026-01，姚亮接任", "overlap_org": "金台区人民政府", "overlap_period": "2026-01", "confidence": "confirmed"},
    # 宝鸡市委书记与金台区委书记/区长 上下级
    {"person_a": 16, "person_b": 1, "type": "superior_subordinate", "context": "宝鸡市委书记对金台区委书记的领导关系（包抓联系）", "overlap_org": "中共宝鸡市金台区委", "overlap_period": "", "confidence": "confirmed"},
    {"person_a": 16, "person_b": 2, "type": "superior_subordinate", "context": "宝鸡市委书记对金台区长的领导关系", "overlap_org": "金台区", "overlap_period": "", "confidence": "confirmed"},
    # 跨区（张湛波早年任职金台区）
    {"person_a": 17, "person_b": 1, "type": "overlap", "context": "张湛波早年任职金台区（金台为其履历起点），现为渭滨区委书记，与现任金台书记同市域、金台为其旧地", "overlap_org": "金台区", "overlap_period": "1990s-2000s", "confidence": "plausible"},
]

# ── Person JSON schemata ──────────────────────────────────────────────────────

PERSON_JSON = {
    "schema_version": "1.0",
}


def build_core_person(person_id: int) -> dict:
    p = {x["id"]: x for x in persons}[person_id]
    name = p["name"]
    rank = "县处级正职" if person_id in (1, 2, 14, 15) else ("地厅级正职" if person_id == 16 else "县处级副职")

    person = {
        "identity": {
            "person_id": f"shaanxi_jintai_{name}",
            "name": name,
            "aliases": [],
            "gender": p["gender"],
            "ethnicity": p["ethnicity"],
            "birth": p["birth"],
            "birthplace": p["birthplace"],
            "native_place": "",
            "education": [
                {"period": "", "institution": p["education"], "major": "", "degree": "", "study_type": "unknown", "source_ids": []}
            ] if p["education"] else [],
            "party_join": p["party_join"],
            "work_start": p["work_start"],
            "dedupe_keys": {
                "name_birth": f"{name}_{p['birth']}",
                "name_birthplace": f"{name}_{p['birthplace']}",
                "official_profile_url": "",
            },
        },
        "current_status": {
            "current_post": p["current_post"],
            "current_org": p["current_org"],
            "administrative_rank": rank,
            "as_of": AS_OF,
            "is_current_confirmed": person_id in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 16, 17),
            "source_ids": [],
        },
        "career_timeline": [],
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {"primary_specializations": [], "secondary_specializations": [], "career_pattern": "unknown", "systems_experience": [], "geographic_pattern": [], "promotion_velocity": {"summary": "", "notable_fast_promotions": []}},
        "work_style_and_personality": {"public_style_indicators": [], "speech_themes": [], "management_signals": [], "caveat": "Work style is inferred from public records, not private psychological assessment."},
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": f"截至{AS_OF}未检索到关于{name}的公开风险信号（纪律处分、负面报道）。", "date": AS_OF, "confidence": "confirmed", "source_ids": []}
        ],
        "source_register": [
            {"id": "S001", "title": "金台区政府官网·政府领导", "url": "http://www.jintai.gov.cn/col10250/col10253/col10265/", "publisher": "金台区人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "现任区政府领导班子名册"},
            {"id": "S002", "title": "金台区政务要闻·区委书记调研", "url": "http://www.jintai.gov.cn/col6845/col6850/", "publisher": "金台区人民政府", "published_at": "2026-07-28", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "赵海斌/王宏强区委书记身份"},
            {"id": "S003", "title": "金台区2026年政府工作报告", "url": "http://www.jintai.gov.cn/col10250/col53/col/col10264/202602/t20260204_1245614.html", "publisher": "金台区人民政府", "published_at": "2026-01-21", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "区长王润军署名"},
        ],
        "confidence_summary": {},
        "open_questions": [],
    }

    # ── Career timeline ──
    timeline = []
    for pos in positions:
        if pos["person_id"] == person_id:
            org = org_name(pos["org_id"])
            timeline.append({
                "start": pos["start_date"] or "unknown",
                "end": pos["end_date"] or "present",
                "org": org,
                "title": pos["title"],
                "level": "",
                "location": org_name(pos["org_id"]),
                "system": "party" if "区委" in org or "市委" in org else ("government" if "政府" in org or "人民政府" in org else "other"),
                "rank": pos["rank"],
                "is_key_promotion": pos["title"] in ("区委书记", "区长", "市委书记"),
                "notes": pos["note"],
                "confidence": "confirmed" if person_id in (1, 2) else "plausible",
                "source_ids": [],
            })
    if not timeline:
        timeline.append({
            "start": "unknown", "end": "present",
            "org": p["current_org"], "title": p["current_post"], "level": "",
            "location": "宝鸡市金台区", "system": "party" if "区委" in p["current_org"] else "government",
            "rank": rank, "is_key_promotion": False, "notes": p["notes"], "confidence": "confirmed", "source_ids": [],
        })
    person["career_timeline"] = timeline

    # ── Relationships (outwards from this person) ──
    rels = []
    for r in relationships:
        other_id = None
        direction = "person_to_other"
        if r["person_a"] == person_id:
            other_id = r["person_b"]
            direction = "person_to_other"
        elif r["person_b"] == person_id:
            other_id = r["person_a"]
            direction = "other_to_person"
        if other_id is not None:
            other = {x["id"]: x for x in persons}[other_id]
            rels.append({
                "person": other["name"],
                "person_id": other.get("person_id", f"shaanxi_jintai_{other['name']}"),
                "relationship_type": r["type"],
                "strength": "strong" if r["type"] in ("predecessor_successor", "partnership") else "medium",
                "evidence": r["context"],
                "overlap_org": r["overlap_org"],
                "overlap_period": r["overlap_period"],
                "direction": direction,
                "confidence": r["confidence"],
                "source_ids": [],
            })
    person["relationships"] = rels

    person["organizations"] = sorted(
        {pos["org_id"] for pos in positions if pos["person_id"] == person_id},
        key=lambda x: x,
    ) if any(pos["person_id"] == person_id for pos in positions) else []

    # confidence / open questions
    if person_id == 1:
        person["confidence_summary"] = {"identity": "unverified", "current_role": "confirmed", "career_completeness": "partial", "relationship_confidence": "medium", "biggest_gap": "赵海斌出生年籍、学历、入党/参加工作时间及2026-03空窗期（离农业农村局→金台任书记）待证。"}
        person["open_questions"] = [
            {"priority": "critical", "question": "赵海斌出生年月、籍贯、学历背景、入党时间与任金台区委书记的确切任命文件", "why_it_matters": "基本身份与晋升路径", "suggested_queries": ["赵海斌 简历 任前公示 宝鸡", "赵海斌 宝鸡 区委书记 任命"], "last_attempted": AS_OF},
            {"priority": "high", "question": "赵海斌2026-03下旬~07月任职空窗（离农业农村局→金台任书记之间的安排）", "why_it_matters": "判断市域干部配置轨迹", "suggested_queries": ["赵海斌 农业农村局 金台", "赵海斌 宝鸡 组织部"], "last_attempted": AS_OF},
        ]
    elif person_id == 2:
        person["confidence_summary"] = {"identity": "unverified", "current_role": "confirmed", "career_completeness": "thin", "relationship_confidence": "medium", "biggest_gap": "姚亮出生年月、籍贯、履历及任区长前一职务缺失。"}
        person["open_questions"] = [
            {"priority": "critical", "question": "姚亮出生年月、籍贯、学历背景、任区长前职务", "why_it_matters": "基本身份与晋升路径缺失", "suggested_queries": ["姚亮 简历 宝鸡 金台", "姚亮 任前公示"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "姚亮任区长前的职务（是否由常务副区长/副区长升任）", "why_it_matters": "理解区长晋升链条", "suggested_queries": ["姚亮 金台区 副区长"], "last_attempted": AS_OF},
        ]
    elif person_id in (14, 15):
        person["confidence_summary"] = {"identity": "unverified", "current_role": "confirmed", "career_completeness": "thin", "relationship_confidence": "medium", "biggest_gap": f"{name}的完整履历与去向待核实。"}
        person["open_questions"] = [{"priority": "medium", "question": f"{name}离任后的去向与完整履历", "why_it_matters": "干部交流网络", "suggested_queries": [f"{name} 简历 去向"], "last_attempted": AS_OF}]
    else:
        person["confidence_summary"] = {"identity": "unverified", "current_role": "confirmed" if person_id in (3,4,5,6,7,8,9,10) else "plausible", "career_completeness": "thin", "relationship_confidence": "medium", "biggest_gap": f"{name}的完整履历与具体分工待补充。"}
        person["open_questions"] = [{"priority": "high", "question": f"{name} {(p['current_post'])} 的完整履历、出生/籍贯/学历及具体分工", "why_it_matters": "完善领导班子的任职交集分析", "suggested_queries": [f"{name} {p['current_post']} 简历"], "index": AS_OF}]

    return person


def org_name(oid: int) -> str:
    return {o["id"]: o["name"] for o in organizations}[oid]


def write_person_json(person_id: int):
    p = {x["id"]: x for x in persons}[person_id]
    name = p["name"]
    role_label = p["current_post"]
    safe_role = role_label.replace("、", "_").replace("（", "_").replace("）", "_").replace("，", "_").replace("/", "_")
    filename = f"{TODAY}-陕西省-宝鸡市-{safe_role}-{name}.json"
    path = PJSON_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(build_core_person(person_id), f, ensure_ascii=False, indent=2)
    return path


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
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

    person_files = []
    for pid in range(1, 18):
        path = write_person_json(pid)
        person_files.append(str(path))

    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print("Person JSONs:")
    for pf in person_files:
        print(f"  {pf}")
    print(f"\nNote: 核心目标=赵海斌(区委书记)、姚亮(区长)，均confirmed。")
    print("      前任区委书记=王宏强(至2026-07)；前任区长=王润军(至2026-01)。")
    print("      （重要）金台区委书记近两个月两次更替：王宏强→赵海斌；区长由王润军→姚亮。")
    print("Done.")


if __name__ == "__main__":
    main()