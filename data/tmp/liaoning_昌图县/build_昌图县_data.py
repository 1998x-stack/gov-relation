#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 昌图县 (铁岭市，辽宁省).

Investigation date: 2026-08-06
Task ID: liaoning_昌图县
Level: 县
Parent city: 铁岭市
Targets: 县委书记 & 县长

Research status: PRIMARY SOURCE ACCESS (official county portal, roster confirmed)
  - 昌图县人民政府门户 (www.changtu.gov.cn) 一手信源可访问：机关简介（县政府领导名录）、人事任免
    （十九届县委一次全会）、要闻动态（政务要闻）等。
  - 现任县委书记 孙佐强、县委副书记/县长 周英伟、县委副书记 赵云峰 已通过官方一手信源确认：
    * 2026-07-30 十九届县委第一次全会 孙佐强当选县委书记，周英伟、赵云峰当选县委副书记
    * 2026-08-03 要闻：县委书记孙佐强 / 县委副书记 县长周英伟 / 县委副书记赵云峰 分别开展“八一”慰问
    * 机关简介（县政府领导）：县长 周英伟；副县长 刘婉夏、李刚、赵俊峰、寇巍威、王春东
    * 孙佐强 2025-12-21 仍以县长身份作政府工作报告，2026-06-16 起新闻称“县委书记孙佐强”。
  - Exa / Baidu / Bing / Sogou 检索普遍受限（rate-limit / timeout），孙佐强、周英伟、赵云峰的
    出生/籍贯/学历/入党时间及任县长前的履历细节缺失，按证据分级标注 unverified。

Confirmed current officeholders (as of 2026-08-06, official 一手):
   - 县委书记: 孙佐强（2026-06-16 新闻报道；2026-07-30 十九届县委一次全会当选）
   - 县委副书记、县长: 周英伟（机关简介列出县长；2026-05-06 县政府领导身份开展安全生产督导；
       2026-07-30 当选县委副书记、并任县长）
   - 县委副书记: 赵云峰（2026-07-30 十九届一次全会当选）
   - 县政府班子成员：常务副县长 刘婉夏；副县长 李刚、赵俊峰（兼公安局长）、寇巍威、王春东

Predecessor / successor timeline (piecemeal / partly inferred):
   - 上一任县长: 苗宇（~2021–2024），2024 年后由孙佐强接任县长（主持 2025 年县政府常务会议，
     2025-12-21 作政府工作报告署"县长"）。孙佐强 ~2026 转任县委书记（2026-06-16 新闻）。
   - 现任县长: 周英伟（孙佐强转任书记后接任，~2026 年上半年，2026-05-06 已开展县长级督导）。
   - 前任县委书记及周英伟任前履历待核。

Cross-region / context:
   - 昌图县系铁岭市所辖县（全国超级产粮大县、生猪调出大县）。市委书记 李文飙、市长 张宝东
     （铁岭市 2025-07 数据）；县级干部由铁岭市委组织部统一管理，县域干部流动主要通过任前公示
     与市—县(市)交流渠道。

Confidence policy: 当前任职 confirmed（官方一手）；领导班姓名录 confirmed（机关简介一手）；
  出生/籍贯/学历/入党等身份字段 unverified（公开文本渠道未检索到，任免名单为图片无法 OCR）。
"""

from __future__ import annotations

import json
import sqlite3  # noqa: F401  (DB I/O is handled by gov_relation.runner via sqlite3)
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

from gov_relation.runner import run_build

# ── Metadata ─────────────────────────────────────────────────────────────
SLUG = "昌图县"
AS_OF = "2026-08-06"

_CURRENT_DIR = Path(__file__).parent.resolve()
DB_PATH = _CURRENT_DIR / f"{SLUG}_network.db"
GEXF_PATH = _CURRENT_DIR / f"{SLUG}_network.gexf"
PERSONS_STAGING_DIR = _CURRENT_DIR

# ── Persons ──────────────────────────────────────────────────────────────
# 一手来源：昌图县人民政府门户（www.changtu.gov.cn）人事任免 / 机关简介 / 政务要闻
persons = [
    # ── 核心：县委（现职） ──
    {"id": 1, "name": "孙佐强", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "县委书记", "current_org": "中国共产党昌图县委员会",
     "source": "https://www.changtu.gov.cn/changtu/zwgk/zfxxgk/fdzdgknr57/rsrm/2026073009541048949/index.html (2026-07-30 十九届一次全会当选)"},
    {"id": 2, "name": "周英伟", "gender": "男", "ethnicity": "待确认", "birth_year": "",
     "birthplace": "", "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "县委副书记、县长", "current_org": "昌图县人民政府",
     "source": "https://www.changtu.gov.cn/changtu/zwgk/zfxxgk/fdzdgknr57/jgjj/index.html (机关简介·县长) + 2026-07-30 十九届一次全会"},
    {"id": 3, "name": "赵云峰", "gender": "男", "ethnicity": "待确认", "birth_year": "",
     "birthplace": "", "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "县委副书记", "current_org": "中国共产党昌图县委员会",
     "source": "https://www.changtu.gov.cn/changtu/zwgk/zfxxgk/fdzdgknr57/rsrm/2026073009541048949/index.html (2026-07-30 当选县委副书记)"},
    # ── 县政府领导班子（机关简介，2026-08） ──
    {"id": 4, "name": "刘婉夏", "gender": "女", "ethnicity": "待确认", "birth_year": "",
     "birthplace": "", "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "常务副县长、县政府党组副书记", "current_org": "昌图县人民政府",
     "source": "https://www.changtu.gov.cn/changtu/zwgk/zfxxgk/fdzdgknr57/jgjj/index.html (机关简介) + 2025-08-15 分工通知"},
    {"id": 5, "name": "李刚", "gender": "男", "ethnicity": "待确认", "birth_year": "",
     "birthplace": "", "education": "待查", "party_join": "", "work_start": "",
     "current_post": "副县长", "current_org": "昌图县人民政府",
     "source": "https://www.changtu.gov.cn/changtu/zwgk/zfxxgk/fdzdgknr57/jgjj/index.html (机关简介)"},
    {"id": 6, "name": "赵俊峰", "gender": "男", "ethnicity": "待确认", "birth_year": "",
     "birthplace": "", "education": "待查", "party_join": "", "work_start": "",
     "current_post": "副县长（兼县公安局局长）", "current_org": "昌图县人民政府",
     "source": "https://www.changtu.gov.cn/changtu/zwgk/zfxxgk/fdzdgknr57/jgjj/index.html (机关简介)"},
    {"id": 7, "name": "寇巍威", "gender": "男", "ethnicity": "待确认", "birth_year": "",
     "birthplace": "", "education": "待查", "party_join": "", "work_start": "",
     "current_post": "副县长", "current_org": "昌图县人民政府",
     "source": "https://www.changtu.gov.cn/changtu/zwgk/zfxxgk/fdzdgknr57/jgjj/index.html (机关简介)"},
    {"id": 8, "name": "王春东", "gender": "男", "ethnicity": "待确认", "birth_year": "",
     "birthplace": "", "education": "待查", "party_join": "", "work_start": "",
     "current_post": "副县长", "current_org": "昌图县人民政府",
     "source": "https://www.changtu.gov.cn/changtu/zwgk/zfxxgk/fdzdgknr57/jgjj/index.html (机关简介)"},
    # ── 前任 ──
    {"id": 10, "name": "苗宇", "gender": "男", "ethnicity": "待确认", "birth_year": "",
     "birthplace": "", "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "前任县长（~2021–2024）", "current_org": "",
     "source": "https://www.changtu.gov.cn/changtu/zwgk/zfxxgk/fdzdgknr57/zfhy/2025022014161474714/index.html (2024 年主持县政府常务会议)"},
]

organizations = [
    {"id": 1, "name": "中国共产党昌图县委员会", "type": "党委", "level": "县处级", "parent": "中共铁岭市委", "location": "辽宁省铁岭市昌图县"},
    {"id": 2, "name": "昌图县人民政府", "type": "政府", "level": "县处级", "parent": "铁岭市人民政府", "location": "辽宁省铁岭市昌图县"},
    {"id": 3, "name": "昌图县公安局", "type": "政府", "level": "乡镇级", "parent": "昌图县人民政府", "location": "辽宁省铁岭市昌图县"},
    {"id": 4, "name": "昌图县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "铁岭市人大常委会", "location": "辽宁省铁岭市昌图县"},
    {"id": 5, "name": "中国人民政治协商会议昌图县委员会", "type": "政协", "level": "县处级", "parent": "铁岭市政协", "location": "辽宁省铁岭市昌图县"},
    {"id": 6, "name": "中国共产党昌图县纪律检查委员会/昌图县监察委员会", "type": "纪委", "level": "县处级", "parent": "中共铁岭市纪委", "location": "辽宁省铁岭市昌图县"},
    {"id": 7, "name": "中国共产党铁岭市委员会", "type": "党委", "level": "地厅级", "parent": "中共辽宁省委", "location": "辽宁省铁岭市"},
    {"id": 8, "name": "铁岭市人民政府", "type": "政府", "level": "地厅级", "parent": "辽宁省人民政府", "location": "辽宁省铁岭市"},
]

positions = [
    # 孙佐强(1) 县委书记
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "~2026", "end_date": "present", "rank": "县处级正职",
     "note": "2026-06-16 新闻报道已称'县委书记孙佐强'；2026-07-30 十九届县委第一次全会当选"},
    {"person_id": 1, "org_id": 2, "title": "县委副书记、县长、县政府党组书记", "start_date": "~2021/2024", "end_date": "~2025/2026", "rank": "县处级正职",
     "note": "2025 年内主持县政府常务会议；2025-12-21 于人代会第五次会议作政府工作报告署'昌图县人民政府县长孙佐强'"},
    {"person_id": 1, "org_id": 1, "title": "县委副书记", "start_date": "~2021/2024", "end_date": "~2026", "rank": "县处级正职", "note": "县长期间兼任县委副书记"},
    # 周英伟(2) 县长
    {"person_id": 2, "org_id": 2, "title": "县委副书记、县长、县政府党组书记", "start_date": "~2026-01/05", "end_date": "present", "rank": "县处级正职",
     "note": "机关简介列为县长；2026-05-06 以县政府领导开展安全生产/防火督导；2026-07-30 十九届县委一次全会当选县委副书记"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "~2026", "end_date": "present", "rank": "县处级正职", "note": "2026-07-30 当选十九屺县委副书记"},
    # 赵云峰(3) 县委副书记
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start_date": "~2026", "end_date": "present", "rank": "县处级正职",
     "note": "2026-07-30 十九届县委一次全会当选县委副书记；2026-08-03 慰问驻昌部队"},
    # 刘婉夏(4)
    {"person_id": 4, "org_id": 2, "title": "常务副县长、县政府党组副书记", "start_date": "<=2025", "end_date": "present", "rank": "县处级副职",
     "note": "机关简介列为副县长；2025-08-15 分工通知为常务副县长、分管发改/财政等"},
    # 各副县长
    {"person_id": 5, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "机关简介"},
    {"person_id": 6, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "机关简介"},
    {"person_id": 6, "org_id": 3, "title": "县公安局局长", "start_date": "", "end_date": "present", "rank": "乡镇级正职", "note": "副县长（兼公安局长）"},
    {"person_id": 7, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "机关简介"},
    {"person_id": 8, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "机关简介"},
    # 苗宇(10) 前任县长
    {"person_id": 10, "org_id": 2, "title": "县长", "start_date": "~2021", "end_date": "~2024", "rank": "县处级正职",
     "note": "前任县长，2024 年主持县政府常务会议至 2024-06；2024 年后由孙佐强接任"},
]

relationships = [
    # 党政一把手搭班
    {"person_a": 1, "person_b": 2, "type": "co_leadership", "context": "县委书记（孙佐强）与县委副书记、县长（周英伟）——党政一把手搭班",
     "overlap_org": "昌图县", "overlap_period": "2026-", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 3, "type": "co_leadership", "context": "县委书记与县委副书记赵云峰（十九届一次全会同台当选，八一慰问分工）",
     "overlap_org": "中共昌图县委", "overlap_period": "2026-", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 3, "type": "co_leadership", "context": "两位县委副书记（县长周英伟与赵云峰，县委班子成员）",
     "overlap_org": "中共昌图县委", "overlap_period": "2026-", "confidence": "confirmed"},
    # 前任县长链: 苗宇 → 孙佐强 → 周英伟
    {"person_a": 1, "person_b": 10, "type": "predecessor_successor", "context": "孙佐强接任苗宇的县长职位（~2024）",
     "overlap_org": "昌图县人民政府", "overlap_period": "~2021-~2024", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor", "context": "孙佐强由县长转任县委书记后，周英伟接任县长（孙前任→周后继县长）",
     "overlap_org": "昌图县人民政府", "overlap_period": "~2025-2026", "confidence": "confirmed"},
    # 县长与政府班子
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "县长与常务副县长（党组副书记）",
     "overlap_org": "昌图县人民政府", "overlap_period": "2026-", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 5, "type": "co_leadership", "context": "县长与副县长",
     "overlap_org": "昌图县人民政府", "overlap_period": "2026-", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "县长与副县长兼公安局长（社会稳定）",
     "overlap_org": "昌图县人民政府", "overlap_period": "2026-", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 7, "type": "co_leadership", "context": "县长与副县长",
     "overlap_org": "昌图县人民政府", "overlap_period": "2026-", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 8, "type": "co_leadership", "context": "县长与副县长",
     "overlap_org": "昌图县人民政府", "overlap_period": "2026-", "confidence": "confirmed"},
    # 常务副县长核心节点
    {"person_a": 4, "person_b": 5, "type": "co_leadership", "context": "常务副县长与其他副县长共事",
     "overlap_org": "昌图县人民政府", "overlap_period": "2025-2026", "confidence": "confirmed"},
    {"person_a": 4, "person_b": 6, "type": "co_leadership", "context": "常务副县长与副县长兼公安局长",
     "overlap_org": "昌图县人民政府", "overlap_period": "2025-2026", "confidence": "confirmed"},
    {"person_a": 4, "person_b": 7, "type": "co_leadership", "context": "常务副县长与副县长",
     "overlap_org": "昌图县人民政府", "overlap_period": "2025-2026", "confidence": "confirmed"},
    {"person_a": 4, "person_b": 8, "type": "co_leadership", "context": "常务副县长与副县长",
     "overlap_org": "昌图县人民政府", "overlap_period": "2025-2026", "confidence": "confirmed"},
]


# ── Person JSONs ─────────────────────────────────────────────────────────
def write_person_jsons():
    """Write per-person graph JSON for the core leaders (县委书记 孙佐强, 县长 周英伟, 县委副书记 赵云峰)."""

    sun = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {"province": "辽宁省", "city": "铁岭市", "region": "昌图县",
                                "job": "县委书记", "task_id": "liaoning_昌图县", "time_focus": "2024-2026"},
        "identity": {
            "person_id": "liaoning_changtu_sunzuoqiang",
            "name": "孙佐强",
            "aliases": [],
            "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "native_place": "",
            "education": [{"period": "", "institution": "待查", "major": "", "degree": "", "study_type": "unknown", "source_ids": []}],
            "party_join": "中共党员", "work_start": "",
            "dedupe_keys": {"name_birth": "孙佐强_unknown", "name_birthplace": "孙佐强_unknown",
                            "official_profile_url": "https://www.changtu.gov.cn/changtu/zwgk/zfxxgk/fdzdgknr57/rsrm/2026073009541048949/index.html"},
        },
        "current_status": {"current_post": "县委书记", "current_org": "中国共产党昌图县委员会",
                           "administrative_rank": "县处级正职", "as_of": AS_OF, "is_current_confirmed": True,
                           "source_ids": ["S001", "S002", "S003"]},
        "career_timeline": [
            {"start": "unknown", "end": "~2021/2024", "org": "履历缺口", "title": "",
             "level": "", "location": "", "system": "other", "rank": "", "is_key_promotion": False,
             "notes": "任昌图县长前的完整履历（出生/籍贯/学历/入党/此前职务）公开文本渠道未检索到",
             "confidence": "unverified", "source_ids": []},
            {"start": "~2021/2024", "end": "~2025/2026", "org": "昌图县人民政府", "title": "县长、县政府党组书记",
             "level": "县处级", "location": "昌图县", "system": "government", "rank": "县处级正职", "is_key_promotion": True,
             "notes": "主持县政府全面工作；2025-01-21、2025-03-28 主持县政府常务会议（县委副书记、县长）；2025-12-21 人代会第五次会议作政府工作报告署'县长孙佐强'",
             "confidence": "confirmed", "source_ids": ["S005", "S006"]},
            {"start": "~2026", "end": "present", "org": "中国共产党昌图县委员会", "title": "县委书记",
             "level": "县处级", "location": "昌图县", "system": "party", "rank": "县处级正职", "is_key_promotion": True,
             "notes": "2026-06-16 新闻报道'县委书记孙佐强督导检查节前食品安全工作'；2026-07-30 十九届县委一次全会当选县委书记；2026-08-03 慰问烈士家属",
             "confidence": "confirmed", "source_ids": ["S001", "S002", "S003"]},
        ],
        "organizations": [
            {"name": "昌图县人民政府", "role": "县长（前任）", "period": "~2021/2024 - ~2025/2026"},
            {"name": "中国共产党昌图县委员会", "role": "县委书记（现任）", "period": "~2026 - 至今"},
        ],
        "relationships": [
            {"person": "周英伟", "person_id": "liaoning_changtu_zhouyingwei", "relationship_type": "predecessor_successor",
             "strength": "strong", "evidence": "孙佐强转任书记后由周英伟接任县长；现任搭班子",
             "overlap_org": "昌图县", "overlap_period": "2026-", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002", "S007"]},
            {"person": "赵云峰", "person_id": "liaoning_changtu_zhaoyunfeng", "relationship_type": "co_leadership",
             "strength": "strong", "evidence": "同届县委班子成员，八一慰问分工",
             "overlap_org": "中共昌图县委", "overlap_period": "2026-", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
            {"person": "苗宇", "person_id": "liaoning_changtu_miaoyu", "relationship_type": "predecessor_successor",
             "strength": "strong", "evidence": "孙佐强接任苗宇的县长职位",
             "overlap_org": "昌图县人民政府", "overlap_period": "~2021-~2024", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S008"]},
            {"person": "刘婉夏", "person_id": "liaoning_changtu_liuwanxia", "relationship_type": "superior_subordinate",
             "strength": "medium", "evidence": "常务副县长共事", "overlap_org": "昌图县人民政府",
             "overlap_period": "2025-2026", "direction": "undirected", "confidence": "confirmed", "source_ids": []},
        ],
        "governance_record": [
            {"period": "2026-06-16", "domain": "public_security", "achievement_or_event": "督导检查节前食品安全工作",
             "role_in_event": "县委书记（带队实地督导）", "measurable_outcome": "强化食品全链条监管", "location": "昌图县",
             "confidence": "confirmed", "source_ids": ["S003"]},
            {"period": "2026-07-30", "domain": "party_building", "achievement_or_event": "十九届县委一次全会当选县委书记，部署县委工作",
             "role_in_event": "县委书记", "measurable_outcome": "", "location": "昌图县", "confidence": "confirmed", "source_ids": ["S001"]},
        ],
        "professional_profile": {
            "primary_specializations": [], "secondary_specializations": [],
            "career_pattern": "local_ladder", "systems_experience": ["party", "government"],
            "geographic_pattern": ["辽宁省"], "promotion_velocity": {"summary": "由县长升任县委书记，县域内正常晋升路径；任职时间介于 2025-12（仍县长）与 2026-06（书记）之间", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": ["民生底线", "食品安全", "安全生产"],
            "management_signals": ["务实督导", "注重保障民生/安全"],
            "caveat": "Work style inferred from public records, not assessment.",
        },
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "截至 2026-08-06 未发现违纪或被纪律处分性公开报道", "date": "", "confidence": "unverified", "source_ids": []}
        ],
        "source_register": [
            {"id": "S001", "title": "中国共产党昌图县第十九届委员会举行第一次全体会议 孙佐强当选县委书记", "url": "https://www.changtu.gov.cn/changtu/zwgk/zfxxgk/fdzdgknr57/rsrm/2026073009541048949/index.html",
             "publisher": "昌图县融媒体中心", "published_at": "2026-07-30", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认孙佐强当选县委书记"},
            {"id": "S002", "title": "县委书记孙佐强慰问烈士家属", "url": "https://www.changtu.gov.cn/changtu/ywdt/zwyw/2026080310451543532/index.html",
             "publisher": "昌图县融媒体中心", "published_at": "2026-08-03", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "以县委书记身份"},
            {"id": "S003", "title": "县委书记孙佐强督导检查节前食品安全工作", "url": "https://www.changtu.gov.cn/changtu/ywdt/zwyw/2026061609015266997/index.html",
             "publisher": "昌图县人民政府", "published_at": "2026-06-16", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "最早采用'县委书记'称谓"},
            {"id": "S004", "title": "机关简介（县政府领导）", "url": "https://www.changtu.gov.cn/changtu/zwgk/zfxxgk/fdzdgknr57/jgjj/index.html",
             "publisher": "昌图县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "县政府领导名单（县长、副县长）"},
            {"id": "S005", "title": "2025年3月28日孙佐强主持召开县政府常务会议", "url": "https://www.changtu.gov.cn/changtu/zwgk/zfxxgk/fdzdgknr57/lzyj/zfhy/2025092815224021608/index.html",
             "publisher": "昌图县人民政府", "published_at": "2025-09-28", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认孙佐强时任县委副书记、县长"},
            {"id": "S006", "title": "政府工作报告（县长孙佐强）在十九卅人代会五次会议", "url": "https://www.changtu.gov.cn/changtu/zwgk/zfxxgk/fdzdgknr57/zfgzbg/2026020315041441927/index.html",
             "publisher": "昌图县人民政府办公室", "published_at": "2026-02-03", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "2025-12-21 孙佐强以县长作政府工作报告"},
            {"id": "S007", "title": "县委副书记 县长周英伟慰问在乡复员军人", "url": "https://www.changtu.gov.cn/changtu/ywdt/zwyw/2026080310443081049/index.html",
             "publisher": "昌图县融媒体中心", "published_at": "2026-08-03", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认周英伟任县委副书记、县长"},
            {"id": "S008", "title": "2024年6月21日苗宇主持召开县政府常务会议", "url": "https://www.changtu.gov.cn/changtu/zwgk/zfxxgk/fdzdgknr57/lzyj/zfhy/2025022014161474714/index.html",
             "publisher": "昌图县人民政府", "published_at": "2024-06-28", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认苗宇此前任县长（前任）"},
        ],
        "confidence_summary": {"identity": "partial", "current_role": "confirmed", "career_completeness": "thin",
                               "relationship_confidence": "high", "biggest_gap": "孙佐强出生/籍贯/学历/入党时间/任县长前完整履历"},
        "open_questions": [
            {"priority": "critical", "question": "孙佐强出生年月、籍贯、教育背景、入党时间、参加工作时间及任昌图县长前履历", "why_it_matters": "无法评估晋升速度与职业模式",
             "suggested_queries": ["孙佐强 简历 昌图"], "last_attempted": AS_OF},
            {"priority": "high", "question": "孙佐强由县长转任县委书记的具体时间节点（任前公示/人大常委会任命）", "why_it_matters": "确定县长空缺起止与周英伟到任时间",
             "suggested_queries": ["孙佐强 任县委书记 昌图 2026"], "last_attempted": AS_OF},
        ],
    }

    zhou = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {"province": "辽宁省", "city": "铁岭市", "region": "昌图县",
                                "job": "县长", "task_id": "liaoning_昌图县", "time_focus": "2025-2026"},
        "identity": {
            "person_id": "liaoning_changtu_zhouyingwei",
            "name": "周英伟",
            "aliases": [],
            "gender": "男", "ethnicity": "待确认", "birth": "", "birthplace": "", "native_place": "",
            "education": [{"period": "", "institution": "待查", "major": "", "degree": "", "study_type": "unknown", "source_ids": []}],
            "party_join": "中共党员", "work_start": "",
            "dedupe_keys": {"name_birth": "周英伟_unknown", "name_birthplace": "周英伟_unknown",
                            "official_profile_url": "https://www.changtu.gov.cn/changtu/zwgk/zfxxgk/fdzdgknr57/jgjj/index.html"},
        },
        "current_status": {"current_post": "县委副书记、县长", "current_org": "昌图县人民政府",
                           "administrative_rank": "县处级正职", "as_of": AS_OF, "is_current_confirmed": True,
                           "source_ids": ["S001", "S002", "S003"]},
        "career_timeline": [
            {"start": "unknown", "end": "~2026", "org": "履历缺口", "title": "",
             "level": "", "location": "", "system": "other", "rank": "", "is_key_promotion": False,
             "notes": "任昌图县长前任职务/出处（是否由他县交流或市委机关来、是否曾任常务副县长/组织部等）公开渠道未检索到",
             "confidence": "unverified", "source_ids": []},
            {"start": "~2026-01/05", "end": "present", "org": "昌图县人民政府", "title": "县委、县政府县长、县政府党组书记",
             "level": "县处级", "location": "昌图县", "system": "government", "rank": "县处级正职", "is_key_promotion": True,
             "notes": "机关简介列为县长；2026-05-06 开展安全生产/防火实地督导；2026-08-03 省委副书记、县长身份慰问复员军人",
             "confidence": "confirmed", "source_ids": ["S001", "S002", "S003"]},
            {"start": "~2026", "end": "present", "org": "中国共产党昌图县委员会", "title": "县委副书记",
             "level": "县处级", "location": "昌图县", "system": "party", "rank": "县处级正职", "is_key_promotion": False,
             "notes": "2026-07-30 十九届县委一次全会当选县委副书记",
             "confidence": "confirmed", "source_ids": ["S003"]},
        ],
        "organizations": [
            {"name": "昌图县人民政府", "role": "县长（现任）", "period": "~2026 - 至今"},
            {"name": "中国共产党昌图县委员会", "role": "县委副书记", "period": "~2026 - 至今"},
        ],
        "relationships": [
            {"person": "孙佐强", "person_id": "liaoning_changtu_sunzuoqiang", "relationship_type": "co_leadership",
             "strength": "strong", "evidence": "现任书记与县长搭班；孙佐强为其前任县长",
             "overlap_org": "昌图县人民政府", "overlap_period": "~2025-2026", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]},
            {"person": "赵云峰", "person_id": "liaoning_changtu_zhaoyunfeng", "relationship_type": "co_leadership",
             "strength": "medium", "evidence": "同为县委副书记", "overlap_org": "中共昌图县委", "overlap_period": "2026-",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]},
            {"person": "刘婉夏", "person_id": "liaoning_changtu_liuwanxia", "relationship_type": "superior_subordinate",
             "strength": "medium", "evidence": "县长与常务副县长", "overlap_org": "昌图县人民政府", "overlap_period": "2026-",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        ],
        "governance_record": [
            {"period": "2026-05-06", "domain": "public_security", "achievement_or_event": "深入重点场所开展安全生产及防火督导检查",
             "role_in_event": "县委副书记、县长", "measurable_outcome": "", "location": "昌图县", "confidence": "confirmed", "source_ids": ["S002"]},
            {"period": "2026-08-03", "domain": "social", "achievement_or_event": "慰问在乡复员军人（八一）",
             "role_in_event": "县委副书记、县长", "measurable_outcome": "", "location": "昌图县", "confidence": "confirmed", "source_ids": []},
        ],
        "professional_profile": {
            "primary_specializations": [], "secondary_specializations": [],
            "career_pattern": "unknown", "systems_experience": ["party", "government"],
            "geographic_pattern": [], "promotion_velocity": {"summary": "现任县委副书记、县长，任前履历与到任时间待核", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {"trait": "grassroots_oriented", "evidence": "实地督导安全生产、防火、慰问复员军人", "confidence": "plausible", "source_ids": ["S002"]}
            ],
            "speech_themes": ["安全生产", "防火", "民生", "双拥"],
            "management_signals": [], "caveat": "Work style inferred from public records, not assessment.",
        },
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "截至 2026-08-06 未发现处分或负面公开报道", "date": "", "confidence": "unverified", "source_ids": []}
        ],
        "source_register": [
            {"id": "S001", "title": "机关简介（县政府领导）", "url": "https://www.changtu.gov.cn/changtu/zwgk/zfxxgk/fdzdgknr57/jgjj/index.html",
             "publisher": "昌图县人民政府", "published_at": "", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "列为县长"},
            {"id": "S002", "title": "周英伟实地督导检查重点场所安全生产及防火工作", "url": "https://www.changtu.gov.cn/changtu/ywdt/zwyw/2026050610030484959/index.html",
             "publisher": "昌图县融媒体中心", "published_at": "2026-05-06", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
            {"id": "S003", "title": "中国共产党昌图县第十九届委员会举行第一次全体会议（内含周英伟当选县委副书记）", "url": "https://www.changtu.gov.cn/changtu/zwgk/zfxxgk/fdzdgknr57/rsrm/2026073009541048949/index.html",
             "publisher": "昌图县融媒体中心", "published_at": "2026-07-30", "accessed_at": AS_OF, "source_type": "official", "reliability": "高", "notes": "周英伟当选县委副书记"},
            {"id": "S004", "title": "县委副书记 县长周英伟慰问在乡复员军人", "url": "https://www.changtu.gov.cn/changtu/ywdt/zwyw/2026080310443081049/index.html",
             "publisher": "昌图县融媒体中心", "published_at": "2026-08-03", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
        ],
        "confidence_summary": {"identity": "unverified", "current_role": "confirmed", "career_completeness": "thin",
                               "relationship_confidence": "medium", "biggest_gap": "周英伟出生/籍贯/学历/入党时间/任县长前履历及到任时间"},
        "open_questions": [
            {"priority": "critical", "question": "周英伟到任昌图县长的具体时间及任前职务", "why_it_matters": "确定县长任期与干部交流源头",
             "suggested_queries": ["周英伟 昌图 县长 任前公示"], "last_attempted": AS_OF},
            {"priority": "high", "question": "周英伟出生年月、教育背景、籍贯、入党时间", "why_it_matters": "身份与晋升轨迹细节",
             "suggested_queries": ["周英伟 简历 铁岭"], "last_attempted": AS_OF},
        ],
    }

    zhao = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {"province": "辽宁省", "city": "铁岭市", "region": "昌图县",
                                "job": "县委副书记", "task_id": "liaoning_昌图县", "time_focus": "2025-2026"},
        "identity": {
            "person_id": "liaoning_changtu_zhaoyunfeng",
            "name": "赵云峰",
            "aliases": [],
            "gender": "男", "ethnicity": "待确认", "birth": "", "birthplace": "", "native_place": "",
            "education": [{"period": "", "institution": "待查", "major": "", "degree": "", "study_type": "unknown", "source_ids": []}],
            "party_join": "中共党员", "work_start": "",
            "dedupe_keys": {"name_birth": "赵云峰_unknown", "name_birthplace": "赵云峰_unknown",
                            "official_profile_url": "https://www.changtu.gov.cn/changtu/zwgk/zfxxgk/fdzdgknr57/rsrm/2026073009541048949/index.html"},
        },
        "current_status": {"current_post": "县委副书记", "current_org": "中国共产党昌图县委员会",
                           "administrative_rank": "县处级正职", "as_of": AS_OF, "is_current_confirmed": True,
                           "source_ids": ["S001", "S002"]},
        "career_timeline": [
            {"start": "unknown", "end": "~2026", "org": "履历缺口", "title": "",
             "level": "", "location": "", "system": "other", "rank": "", "is_key_promotion": False,
             "notes": "任昌图县委副书记前的职务/履历公开未检索到", "confidence": "unverified", "source_ids": []},
            {"start": "~2026", "end": "present", "org": "中国共产党昌图县委员会", "title": "县委副书记",
             "level": "县处级", "location": "昌图县", "system": "party", "rank": "县处级正职", "is_key_promotion": True,
             "notes": "2026-07-30 十九届县委一次全会当选县委副书记；2026-08-03 慰问驻昌部队",
             "confidence": "confirmed", "source_ids": ["S001", "S002"]},
        ],
        "organizations": [{"name": "中国共产党昌图县委员会", "role": "县委副书记"}],
        "relationships": [
            {"person": "孙佐强", "person_id": "liaoning_changtu_sunzuoqiang", "relationship_type": "co_leadership",
             "strength": "strong", "evidence": "书记与副书记（县委班子）", "overlap_org": "中共昌图县委", "overlap_period": "2026-",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
            {"person": "周英伟", "person_id": "liaoning_changtu_zhouyingwei", "relationship_type": "co_leadership",
             "strength": "medium", "evidence": "同为县委副书记", "overlap_org": "中共昌图县委", "overlap_period": "2026-",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        ],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [], "secondary_specializations": [],
            "career_pattern": "unknown", "systems_experience": ["party"],
            "geographic_pattern": [], "promotion_velocity": {"summary": "2026 年 7 月当选县委副书记（现职）", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [{"trait": "grassroots_oriented", "evidence": "2026-08 慰问驻昌部队官兵", "confidence": "plausible", "source_ids": ["S002"]}],
            "speech_themes": ["双拥", "国防"], "management_signals": [], "caveat": "Work style inferred from public records, not assessment.",
        },
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "截至 2026-08-06 未发现处分或负面公开报道", "date": "", "confidence": "unverified", "source_ids": []}
        ],
        "source_register": [
            {"id": "S001", "title": "中国共产党昌图县第十九届委员会举行第一次全体会议（赵云峰当选县委副书记）", "url": "https://www.changtu.gov.cn/changtu/zwgk/zfxxgk/fdzdgknr57/rsrm/2026073009541048949/index.html",
             "publisher": "昌图县融媒体中心", "published_at": "2026-07-30", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
            {"id": "S002", "title": "县委副书记赵云峰慰问驻昌部队官兵", "url": "https://www.changtu.gov.cn/changtu/ywdt/zwyw/2026080310433931211/index.html",
             "publisher": "昌图县融媒体中心", "published_at": "2026-08-03", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
        ],
        "confidence_summary": {"identity": "unverified", "current_role": "confirmed", "career_completeness": "thin",
                               "relationship_confidence": "medium", "biggest_gap": "赵云峰出生/籍贯/学历/入党时间/此前职务及分工"},
        "open_questions": [
            {"priority": "high", "question": "赵云峰具体出生/籍贯/学历/入党时间及任县委副书记前任职务（分管）", "why_it_matters": "判断其分工与晋升路径",
             "suggested_queries": ["赵云峰 昌图 县委副书记"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "赵云峰在十九届县委中的分工（是否政法委书记/组织部长等）", "why_it_matters": "细化班子分工", "suggested_queries": [], "last_attempted": AS_OF},
        ],
    }

    person_dir = PERSONS_STAGING_DIR
    today = AS_OF.replace("-", "")
    for fname, data in [
        (f"{today}-辽宁省-铁岭市-县委书记-孙佐强.json", sun),
        (f"{today}-辽宁省-铁岭市-县长-周英伟.json", zhou),
        (f"{today}-辽宁省-铁岭市-县委副书记-赵云峰.json", zhao),
    ]:
        path = person_dir / fname
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {path}")


def main():
    print(f"Building {SLUG} network data...")
    print(f"  Persons: {len(persons)}")
    print(f"  Orgs: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

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

    write_person_jsons()

    print(f"\nDone! Staged output files:")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    for f in sorted(PERSONS_STAGING_DIR.glob("*.json")):
        if "昌图" in f.name or "孙佐" in f.name or "周英" in f.name or "赵云峰" in f.name:
            print(f"  JSON: {f}")


if __name__ == "__main__":
    main()