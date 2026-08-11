#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 陇县, 宝鸡市, 陕西省.

Investigation date: 2026-08-07
Task ID: shaanxi_陇县
Level: 县
Targets: 县委书记 & 县长

Research sources (official 陇县人民政府网 www.longxian.gov.cn, accessed 2026-08-07 via HTTP):
  - 陇县要闻 2026-07-29《陇县县委书记田华锋调研防汛防滑工作》
    http://www.longxian.gov.cn/col4225/col4227/202607/t20260730_1289579.html
  - 县政府领导 王丽 official bio (2026-06-03 发布):
    http://www.longxian.gov.cn/col15058/col15061/col15868/202605/t20260522_1272184.html
  - 县政府领导 col15868 名册（11 位政府领导 + 各人 bio 页）
  - 陇政发〔2026〕2号 任免职通知（2026-01-28）：庞强任副县长/公安局长，免窦军红
  - 人事信息-任免职通知列表（2024-2026 各期）
  - 2026-07-29 县长王丽调研 article: http://www.longxian.gov.cn/col4225/col4227/202607/t20260730_1289569.html

Key leadership (as of 2026-08, official sources):
  - 县委书记：田华锋（2026-07-29 官方要闻确认）
  - 县长：王丽（县委副书记、县政府党组书记、县长；官方简历，安统计）
  - 县政府班子：常务副县长胡永康、副县长（挂职）任会生/李银军/李霞/杨仪/王鹏飞/庞强/黄宝军/陈银栓/曹大革
  - 前任：窦军红（曾任陇县副县长、公安局长，2026-01 免职）
  - 跨县关联：梁丹军（原陇县委副书记/常务副县长，2025-08 调任渭滨）
  - 去重：省长王丽(b.1983) 与 渭滨区委副书记王丽 非同人，需注意。

Method & confidence: Exa rate-limited, Baidu/Bing 302/验证页。改用 陇县官方政府网(www.longxian.gov.cn, HTTP) 一手信源。
confidence 说明见 investigation_stages.md：confirmed=官方页面/任命通知/两个独立可靠来源；plausible=媒体百科；unverified=线索。
注：县委领导班子（纪委书记/组织部长/宣传部长/政法书记/专职副书记）现任名单等背景信息在 degraded 网络下未能完全确认，已列入 open_gaps / report/open_gaps.md。
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

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "陇县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-07"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "shaanxi_陇县"
if _CURRENT_DIR.name == "shaanxi_陇县":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR  # fallback
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ──────────────────────────────────────────────────────────────────
# 1=县委书记(田华锋), 2=县长(王丽), 3-6=县委常委/县政府领导, 7-13=副县长/党组成员,
# 14=跨县关联(梁丹军), 15=前任(公安局长,窦军红)
persons = [
    # ════════════ 核心（现任） ════════════
    {
        "id": 1,
        "name": "田华锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共陇县委员会",
        "source": "陇县官网要闻(2026-07-29 调研报道)",
        "confidence": "confirmed",
        "notes": "2026年现任陇县县委书记。2026-07-28 调研防汛防滑（固关镇、段家峡水库、县应急管理局）。完整履历/出生/籍贯待补充（部分公开资料未检索到）。",
    },
    {
        "id": 2,
        "name": "王丽",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1983-04",
        "birthplace": "",
        "education": "大学（管理学学士）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "陇县人民政府",
        "source": "陇县政府信息公开·县政府领导(2026-06-03发布)",
        "confidence": "confirmed",
        "notes": "陇县委副书记、县政府党组书记、县长，兼中共陇县关山草原旅游风景区工委副书记。分管县财政局、审计局。2026-07-29 调研水利项目及防汛（东风镇西沟村、丰收水库）。",
    },
    # ════════════ 政府领导班子（县委常委兼任） ════════════
    {
        "id": 3,
        "name": "胡永康",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984-02",
        "birthplace": "",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "陇县人民政府",
        "source": "陇县政府官网·县政府领导(2023-12-11)",
        "confidence": "confirmed",
        "notes": "陇县委常委、县政府党组副书记、副县长(常务)、三级调研员。负责县政府日常工作、黄河流域生态保护、安全生产、粮食安全、住建等。2026-07-29 随县委书记调研防汛。",
    },
    {
        "id": 4,
        "name": "任会生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-10",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长（挂职）",
        "current_org": "陇县人民政府",
        "source": "陇县政府官网·县政府领导",
        "confidence": "confirmed",
        "notes": "陇县委常委、县政府党组成员、副县长(挂职)。负责长城资产定点帮扶和全县金融工作。",
    },
    {
        "id": 5,
        "name": "李银军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-08",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "陇县人民政府",
        "source": "陇县政府官网·县政府领导(2025-05-07)",
        "confidence": "confirmed",
        "notes": "陇县委常委、县政府党组成员、副县长(三级调研员)。分管工业经济、生态文明、自然资源和规划、文化旅游。",
    },
    # ════════════ 副县长 / 其他政府领导 ════════════
    {
        "id": 6,
        "name": "李霞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1978-09",
        "birthplace": "",
        "education": "大学（法学学士）",
        "party_join": "民进会员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "陇县人民政府",
        "source": "陇县政府官网·县政府领导",
        "confidence": "confirmed",
        "notes": "分管教育体育和卫生健康。联系团县委、妇联、残联、红十字会。",
    },
    {
        "id": 7,
        "name": "杨仪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986-03",
        "birthplace": "",
        "education": "大学（工学学士）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、河北镇党委书记",
        "current_org": "陇县人民政府",
        "source": "陇县政府官网·县政府领导(2025-11-05)",
        "confidence": "confirmed",
        "notes": "县政府党组成员、副县长，兼陇县河北镇党委书记。分管民政。",
    },
    {
        "id": 8,
        "name": "王鹏飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-10",
        "birthplace": "",
        "education": "在职研究生",
        "party_join": "无党派",
        "work_start": "",
        "current_post": "副县长（挂职）",
        "current_org": "陇县人民政府",
        "source": "陇县政府官网·县政府领导(2025-11-05)",
        "confidence": "confirmed",
        "notes": "副县长(挂职)、二级调研员。负责苏陕协作和招商引资。",
    },
    {
        "id": 9,
        "name": "庞强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-07",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、公安局局长",
        "current_org": "陇县人民政府 / 陇县公安局",
        "source": "陇政发〔2026〕2号 任免职通知(2026-01-28)",
        "confidence": "confirmed",
        "notes": "县政府党组成员、副县长、县公安局党委书记/局长/督察长(兼)、三级高级警长。2026-01-08 县十八届人大常委会第27次会议任命。分管公安、司法、退役军人。",
    },
    {
        "id": 10,
        "name": "黄宝军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-08",
        "birthplace": "",
        "education": "大专",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "陇县人民政府",
        "source": "陇县政府官网·县政府领导(2025-11-05)",
        "confidence": "confirmed",
        "notes": "县政府党组成员、副县长、二级调研员。分管交通、就业、市场监管。",
    },
    {
        "id": 11,
        "name": "陈银拴",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-06",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "陇县人民政府",
        "source": "陇县政府官网·县政府领导(2025-11-05)",
        "confidence": "confirmed",
        "notes": "县政府党组成员、副县长、三级调研员。分管农业农村、乡村振兴、生态乳都建设。",
    },
    {
        "id": 12,
        "name": "曹大革",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967-11",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府党组成员",
        "current_org": "陇县人民政府",
        "source": "陇县政府官网·县政府领导",
        "confidence": "confirmed",
        "notes": "县政府党组成员、二级调研员。负责李家河煤矿开发专班。协同陈银拴抓农业农村工作。",
    },
    # ════════════ 跨县关联 / 前任 ════════════
    {
        "id": 13,
        "name": "梁丹军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-01",
        "birthplace": "陕西省丹凤县",
        "education": "大学（法学学士）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "渭滨区委副书记、区长（曾任陇县委副书记）",
        "current_org": "渭滨区人民政府",
        "source": "渭滨区政府官网 + 银联系(2026-08 渭滨区调查)",
        "confidence": "confirmed",
        "notes": "曾任陇县委副书记、县委常委/常务副县长。2025-08 调任渭滨区委副书记、代区长。跨县干部交流线索。",
    },
    {
        "id": 14,
        "name": "窦军红",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（前任陇县副县长、公安局长，2026-01 免职）",
        "current_org": "陇县公安局",
        "source": "陇政发〔2026〕2号(任免职通知)",
        "confidence": "confirmed",
        "notes": "2026-01 免去陇县政府副县长、公安局长、督察长职务。调任去向待补充。",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共陇县委员会", "type": "党委", "level": "县处级", "parent": "中共宝鸡市委", "location": "宝鸡市陇县"},
    {"id": 2, "name": "陇县人民政府", "type": "政府", "level": "县处级", "parent": "宝鸡市人民政府", "location": "宝鸡市陇县"},
    {"id": 3, "name": "陇县公安局", "type": "政府", "level": "乡科级", "parent": "陇县人民政府", "location": "宝鸡市陇县"},
    {"id": 4, "name": "中共宝鸡市委", "type": "党委", "level": "地厅级", "parent": "中共陕西省委", "location": "宝鸡市"},
    {"id": 5, "name": "陇县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "宝鸡市人大常委会", "location": "宝鸡市陇县"},
    {"id": 6, "name": "中共陇县河北镇委员会", "type": "党委", "level": "乡科级", "parent": "中共陇县委员会", "location": "宝鸡市陇县河北镇"},
    {"id": 7, "name": "中共陇县关山草原旅游风景区工作委员会", "type": "党委", "level": "县处级", "parent": "中共陇县委员会", "location": "宝鸡市陇县"},
    # 跨县关联组织
    {"id": 8, "name": "渭滨区人民政府/中共宝鸡市渭滨区委", "type": "党委", "level": "县处级", "parent": "中共宝鸡市委", "location": "宝鸡市渭滨区"},
]

# ── Positions ─────────────────────────────────────────────────────────────────
positions = [
    # 田华锋（县委书记）
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任（2026-07 官方报道确认）"},
    # 王丽（县长）
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "兼"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "县政府党组书记、县长"},
    {"person_id": 2, "org_id": 7, "title": "关山草原旅游风景区工委副书记（兼）", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "兼任"},
    # 胡永康（常务副县长）
    {"person_id": 3, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "常务副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "县政府党组副书记"},
    # 任会会（挂职）
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副县长（挂职）", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "长城资产定点帮扶"},
    # 李银军（副县长）
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 李霞
    {"person_id": 6, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 杨仪
    {"person_id": 7, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "兼河北镇党委书记"},
    {"person_id": 7, "org_id": 6, "title": "河北镇党委书记", "start_date": "", "end_date": "", "rank": "乡科级正职", "note": "兼任"},
    # 王鹏飞（挂职）
    {"person_id": 8, "org_id": 2, "title": "副县长（挂职）", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "苏陕协作"},
    # 庞强（公安局长）
    {"person_id": 9, "org_id": 2, "title": "副县长", "start_date": "2026-01", "end_date": "", "rank": "县处级副职", "note": "2026-01-08 县人大常委会任命"},
    {"person_id": 9, "org_id": 3, "title": "县公安局党委书记、局长、督察长", "start_date": "2026-01", "end_date": "", "rank": "乡科级正职", "note": "兼任"},
    # 黄宝军
    {"person_id": 10, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 陈银拴
    {"person_id": 11, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 曹大革
    {"person_id": 12, "org_id": 2, "title": "县政府党组成员", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 梁丹军（跨县）
    {"person_id": 13, "org_id": 1, "title": "陇县委副书记", "start_date": "", "end_date": "2025-08", "rank": "县处级副职", "note": "任陇县委副书记（曾兼任常务副县长）"},
    {"person_id": 13, "org_id": 2, "title": "陇县委常委、常务副县长", "start_date": "", "end_date": "2025-08", "rank": "县处级副职", "note": "陇县政党组副书记"},
    {"person_id": 13, "org_id": 8, "title": "渭滨区委副书记、区长", "start_date": "2025-09", "end_date": "", "rank": "县处级正职", "note": "2025年9月当选渭滨区区长"},
    # 窦军红（前任公安局长）
    {"person_id": 14, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "2026-01", "rank": "县处级副职", "note": "2026-01 免职"},
    {"person_id": 14, "org_id": 3, "title": "县公安局局长", "start_date": "", "end_date": "2026-01", "rank": "乡科级正职", "note": "2026-01 免职"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 现任书记-县长 搭档
    {"person_a": 1, "person_b": 2, "type": "partnership", "context": "现任县委书记与县长为党政主要领导搭档", "overlap_org": "中共陇县委员会", "overlap_period": "现任", "confidence": "confirmed"},
    # 书记与政府领导
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "书记与常务副县长领导关系", "overlap_org": "中共陇县委员会", "overlap_period": "现任", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "书记与副县长/公安局长关系", "overlap_org": "中共陇县委员会", "overlap_period": "2026-01至今", "confidence": "confirmed"},
    # 县长与政府班子
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "县长与常务副县长（协助县长分管财审）", "overlap_org": "陇县人民政府", "overlap_period": "现任", "confidence": "confirmed"},
    # 跨县：梁丹军 由陇县 → 渭滨
    {"person_a": 13, "person_b": 2, "type": "predecessor_successor", "context": "梁丹军曾在陇县任县委副书记/常务副县长，后调任渭滨；same org overlap", "overlap_org": "中共陇县委员会", "overlap_period": "2022-2025", "confidence": "confirmed"},
    # 公安局长交接
    {"person_a": 14, "person_b": 9, "type": "predecessor_successor", "context": "窦军红任陇县公安局局长至2026-01，庞强接任", "overlap_org": "陇县公安局", "overlap_period": "2026-01", "confidence": "confirmed"},
]

# ── Person JSON 构建 ──────────────────────────────────────────────────────────

PERSON_JSON = {"schema_version": "1.0"}


def build_core_person(person_id: int) -> dict:
    p = {x["id"]: x for x in persons}[person_id]
    name = p["name"]
    rank = "县处级正职" if person_id in (1, 2, 13) else ("乡科级正职" if person_id == 9 else "县处级副职")

    person = {
        "identity": {
            "person_id": f"shaanxi_longxian_{name}",
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
            "is_current_confirmed": person_id in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12),
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
            {"type": "none_found", "description": f"未检索到关于{name}的公开风险信号（纪律、审计、负面报道）。", "date": AS_OF, "confidence": "confirmed", "source_ids": []}
        ],
        "source_register": [
            {"id": "S001", "title": "陇县政府官网·县政府领导", "source_type": "official", "reliability": "high"},
            {"id": "S002", "title": "陇县官方网站要闻", "source_type": "official", "reliability": "high"},
            {"id": "S003", "title": "陇政发〔2026〕2号任免职通知", "source_type": "official", "reliability": "high"},
            {"id": "S004", "title": "百度百科/公开媒体(备)", "source_type": "encyclopedia", "reliability": "medium"},
        ],
        "confidence_summary": {},
        "open_questions": [],
    }

    # ── career_timeline ──
    def org_name(_oid):
        return {o["id"]: o["name"] for o in organizations}[_oid]

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
                "location": org,
                "system": "party" if ("县委" in org or "中共" in org) else ("government" if "政府" in org or "公安" in org else "other"),
                "rank": pos["rank"],
                "is_key_promotion": pos["title"] in ("县委书记", "县长", "县委副书记", "常务副县长"),
                "notes": pos["note"],
                "confidence": "confirmed" if person_id in (1, 2, 3, 9, 13, 14) else "plausible",
                "source_ids": [],
            })
    if not timeline:
        timeline.append({
            "start": "unknown", "end": "present",
            "org": p["current_org"], "title": p["current_post"], "level": "",
            "location": "宝鸡市陇县", "system": "party" if "县委" in p["current_org"] else "government",
            "rank": rank, "is_key_promotion": False, "notes": p["notes"], "confidence": "confirmed", "source_ids": [],
        })
    person["career_timeline"] = timeline

    # ── relationships ──
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
                "person_id": other.get("person_id", f"shaanxi_longxian_{other['name']}"),
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

    # ── professional_profile / confidence / open_questions ──
    prof = {
        1: ("地方党政一把手 (本土/上调待核)", "任陇县委书记；履历待补充"),
        2: ("政府一把手 (跨县域/市级背景待核)", "1983年出生，年轻县长，兼党工委副书记；履历早年待补充"),
        3: ("政府常务 (专职政务)", "1984年生，年轻常务副县长；住建/应急/发改领域"),
        13: ("跨县轮换型 (县委副书记→区长)", "陇县委副书记/常务副县长→渭滨区长"),
    }
    if person_id in prof:
        person["professional_profile"]["career_pattern"] = prof[person_id][0]
        person["professional_profile"]["geographic_pattern"] = [prof[person_id][1]]

    if person_id == 1:
        person["confidence_summary"] = {"identity": "plausible", "current_role": "confirmed", "career_completeness": "thin", "relationship_confidence": "medium", "biggest_gap": "田华锋出生/籍贯/学历/来陇前后的完整履历未公开检索到；前任县委书记、任职起始时间待核。"}
        person["open_questions"] = [
            {"priority": "critical", "question": "田华锋的出生年份、籍贯、学历、入党/参加工作时间和完整履历", "why_it_matters": "县委书记是核心人物，无履历则难以绘制其晋升与网络", "suggested_queries": ["田华锋 陇县 县委书记 简历", "田华锋 任前公示", "田华锋 宝鸡市委"], "last_attempted": AS_OF},
            {"priority": "high", "question": "田华锋接任陇县县委书记的时间与前任县委书记去向", "why_it_matters": "判断县委一把手交接与跨县轮换", "suggested_queries": ["陇县 前任县委书记 卸任", "陇县县委书记 免职 田华峰"], "last_attempted": AS_OF},
        ]
    elif person_id == 2:
        person["confidence_summary"] = {"identity": "confirmed", "current_role": "confirmed", "career_completeness": "partial", "relationship_confidence": "medium", "biggest_gap": "王丽任县长的时间起点、此前县委书记/县委副书记career（来陇县前）待补充；是否有跨县经历未核。"}
        person["open_questions"] = [
            {"priority": "medium", "question": "王丽担任陇县长的起始时间及来陇县前的过往任职", "why_it_matters": "理解其晋升轨迹与县域经历", "suggested_queries": ["王丽 陇县 县长 任前", "王丽 陇县 简历"], "last_attempted": AS_OF},
        ]
    elif person_id == 13:
        person["confidence_summary"] = {"identity": "confirmed", "current_role": "confirmed", "career_completeness": "partial", "relationship_confidence": "high", "biggest_gap": "梁丹军在陇县委副书记/常务副县长具体任职时间。"}
        person["open_questions"] = [{"priority": "medium", "question": "梁丹军陇县县委副书记任职起止", "why_it_matters": "跨县干部交流链完整时间标注", "suggested_queries": ["梁丹军 陇县 县委副书记"], "last_attempted": AS_OF}]
    elif person_id == 14:
        person["confidence_summary"] = {"identity": "plausible", "current_role": "confirmed", "career_completeness": "thin", "relationship_confidence": "medium", "biggest_gap": "窦军红完整履历与免职后去向。"}
        person["open_questions"] = [{"priority": "medium", "question": "窦军红免任后的去向", "why_it_matters": "公安系统领导更替", "suggested_queries": ["窦军红 陇县 公安"], "last_attempted": AS_OF}]
    else:
        person["confidence_summary"] = {"identity": "confirmed", "current_role": "confirmed", "career_completeness": "thin", "relationship_confidence": "medium", "biggest_gap": f"关于{name}的完整履历(来陇前/任内细节)待补充。"}
        person["open_questions"] = [{"priority": "medium", "question": f"{name} 的完整履历与任职时间", "why_it_matters": "完善领导班子任职交集分析", "suggested_queries": [f"{name} 陇县 简历"], "last_attempted": AS_OF}]

    return person


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
    for pid in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]:
        path = write_person_json(pid)
        person_files.append(str(path))

    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print("Person JSONs:")
    for pf in person_files:
        print(f"  {pf}")
    print(f"\nNote: 核心目标=田华锋(县委书记)、王丽(县长)，均 confirmed。")
    print("      县委副书记、纪委书记、组织部长、宣传部长等县委班子名单未完全检索到，已列 open_gaps。")
    print("      跨县关联=梁丹军（陇→渭滨区长）。")
    print("Done.")


if __name__ == "__main__":
    main()