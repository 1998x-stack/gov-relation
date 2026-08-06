#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 宽甸满族自治县 (丹东市，辽宁省).

Investigation date: 2026-08-06
Task ID: liaoning_宽甸满族自治县
Level: 县
Parent city: 丹东市
Targets: 县委书记 & 县长

Research status: PRIMARY SOURCE ACCESS (www.lnkd.gov.cn)
  - 宽甸满族自治县人民政府门户网站 (www.lnkd.gov.cn): 可访问，主要来源
  - www.kuandian.gov.cn 域名不可达；改经父站 dandong.gov.cn 与官方域名 lnkd.gov.cn 获取
  - 县委书记、县长、人大主任、政协主席、县委常委会、县纪委、副县长名单均已通过官方新闻/领导页确认
  - Exa 检索限流、Baidu/Bing 不可用；由远飞(书记)完整履历缺失，按证据分级标注

Current officeholders (as of 2026-08-06, confirmed by official www.lnkd.gov.cn):
   - 县委书记: 由远飞（2026-07-30/31 第十七次党代会当选连任县委书记；2026-07/08 多次主持/带队活动）
   - 县委副书记、县长: 王茜（女，满族，1987-01生，2025-12-26 八届人大五次会议当选县长）
   - 县委副书记: 吴成福
   - 县人大常委会主任: 高芳华（2025-12-26 当选）
   - 县政协主席: 原宝忠

17届县委常委会(2026-07-30 全会): 书记 由远飞；副书记 王茜、吴成福；常委 刘汝江、刘大彦、
宋剑锋、孙洋、原野、倪振超、卢景一、康平金。县纪委书记 刘汝江。

Predecessor / 换届线索:
   - 前任县委书记: 倪志新（2025-12 县人大会议仍居前排的关键岗位，第十七届党代会前卸任，由远飞接任）
   - 王茜 2025-12-26 在八届人大五次会议上当选县长。

Cross-region / context:
   - 宽甸满族自治县为丹东市下辖县，丹东本轮换届（2026年）多县同步更新班子
   - 县纪委一次全会选举 刘汝江(书记)、洪艺玮/戴兵(副书记)
"""

from __future__ import annotations

import json
import sqlite3
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
SLUG = "宽甸满族自治县"
AS_OF = "2026-08-06"

_CURRENT_DIR = Path(__file__).parent.resolve()
DB_PATH = _CURRENT_DIR / f"{SLUG}_network.db"
GEXF_PATH = _CURRENT_DIR / f"{SLUG}_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────────
persons = [
    # ── 县委书记 ──
    {
        "id": 1,
        "name": "由远飞",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "",
        "birthplace": "",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共宽甸满族自治县委员会",
        "source": "https://www.lnkd.gov.cn/html/KDXZF/202607/0178545928874517.html (十七次党代会, 2026-07-30/31)",
    },
    # ── 县委副书记、县长 ──
    {
        "id": 2,
        "name": "王茜",
        "gender": "女",
        "ethnicity": "满族",
        "birth": "1987年1月",
        "birthplace": "",
        "education": "在职研究生学历，工商管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "宽甸满族自治县人民政府",
        "source": "https://www.lnkd.gov.cn/html/KDXZF/202512/0176483070074477.html (政府领导简历)",
    },
    # ── 县委副书记 ──
    {
        "id": 3,
        "name": "吴成福",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "",
        "birthplace": "",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共宽甸满族自治县委员会",
        "source": "https://www.lnkd.gov.cn/html/KDXZF/202607/0178545928874510.html (十七届一次全会, 2026-07-30)",
    },
    # ── 县纪委书记 ──
    {
        "id": 4,
        "name": "刘汝江",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "",
        "birthplace": "",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、纪委书记",
        "current_org": "中共宽甸满族自治县纪律检查委员会",
        "source": "https://www.lnkd.gov.cn/html/KDXZF/202607/0178545801849082.html (纪委一次全会, 2026-07-30)",
    },
    # ── 县人大常委会主任 ──
    {
        "id": 5,
        "name": "高芳华",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "",
        "birthplace": "",
        "education": "待查",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "宽甸满族自治县人民代表大会常务委员会",
        "source": "https://www.lnkd.gov.cn/html/KDXZF/202512/0176674383048451.html (八届人大五次会议, 2025-12)",
    },
    # ── 县政协主席 ──
    {
        "id": 6,
        "name": "原宝忠",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "",
        "birthplace": "",
        "education": "待查",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "中国人民政治协商会议宽甸满族自治县委员会",
        "source": "https://www.lnkd.gov.cn/html/KDXZF/202608/0178571858761522.html (走访慰问, 2026-08-03)",
    },
    # ── 县委常委会其他成员（17届） ──
    {
        "id": 7,
        "name": "刘大彦",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共宽甸满族自治县委员会",
        "source": "https://www.lnkd.gov.cn/html/KDXZF/202607/0178545928874510.html",
    },
    {
        "id": 8,
        "name": "宋剑锋",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "宽甸满族自治县人民政府",
        "source": "https://www.lnkd.gov.cn/kdxzf/zfxxgk/fdzdgknr/jgjj/index.html",
    },
    {
        "id": 9,
        "name": "孙洋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共宽甸满族自治县委员会",
        "source": "https://www.lnkd.gov.cn/html/KDXZF/202607/0178545928874510.html",
    },
    {
        "id": 10,
        "name": "原野",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "宽甸满族自治县人民政府",
        "source": "https://www.lnkd.gov.cn/html/KDXZF/202607/0178545928874510.html",
    },
    {
        "id": 11,
        "name": "倪振超",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共宽甸满族自治县委员会",
        "source": "https://www.lnkd.gov.cn/html/KDXZF/202607/0178545928874510.html",
    },
    {
        "id": 12,
        "name": "卢景一",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共宽甸满族自治县委员会",
        "source": "https://www.lnkd.gov.cn/html/KDXZF/202607/0178545928874510.html",
    },
    {
        "id": 13,
        "name": "康平金",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共宽甸满族自治县委员会",
        "source": "https://www.lnkd.gov.cn/html/KDXZF/202607/0178545928874510.html",
    },
    # ── 副县长（政府序列，含非常委） ──
    {
        "id": 14,
        "name": "陆伟权",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "宽甸满族自治县人民政府",
        "source": "https://www.lnkd.gov.cn/kdxzf/zfxxgk/fdzdgknr/jgjj/index.html",
    },
    {
        "id": 15,
        "name": "迟景瑞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "宽甸满族自治县人民政府",
        "source": "https://www.lnkd.gov.cn/kdxzf/zfxxgk/fdzdgknr/jgjj/index.html",
    },
    {
        "id": 16,
        "name": "郑新春",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "宽甸满族自治县人民政府",
        "source": "https://www.lnkd.gov.cn/kdxzf/zfxxgk/fdzdgknr/jgjj/index.html",
    },
    {
        "id": 17,
        "name": "韩帅",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "宽甸满族自治县人民政府",
        "source": "https://www.lnkd.gov.cn/kdxzf/zfxxgk/fdzdgknr/jgjj/index.html",
    },
    # ── 前任县委书记（交接线索） ──
    {
        "id": 18,
        "name": "倪志新",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任县委书记（已卸任）",
        "current_org": "中共宽甸满族自治县委员会",
        "source": "https://www.lnkd.gov.cn/html/KDXZF/202512/0176674383048451.html (八届人大五次会议前排, 2025-12)",
    },
]

organizations = [
    {"id": 1, "name": "中共宽甸满族自治县委员会", "type": "党委", "level": "县处级", "parent": "中共丹东市委", "location": "宽甸满族自治县"},
    {"id": 2, "name": "宽甸满族自治县人民政府", "type": "政府", "level": "县处级", "parent": "丹东市人民政府", "location": "宽甸满族自治县"},
    {"id": 3, "name": "中共宽甸满族自治县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共宽甸满族自治县委员会", "location": "宽甸满族自治县"},
    {"id": 4, "name": "宽甸满族自治县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "宽甸满族自治县", "location": "宽甸满族自治县"},
    {"id": 5, "name": "中国人民政治协商会议宽甸满族自治县委员会", "type": "政协", "level": "县处级", "parent": "宽甸满族自治县", "location": "宽甸满族自治县"},
    {"id": 6, "name": "中央丹东市委员会", "type": "党委", "level": "地厅级", "parent": "中共辽宁省委", "location": "丹东市"},
]

positions = [
    # 由远飞（书记）
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "<=2026-07", "end_date": "present", "rank": "县处级正职",
     "note": "2026-07-30/31 十七次党代会连任县委书记；2026-07/08 主持县委多项工作"},
    # 王茜（县长）
    {"person_id": 2, "org_id": 2, "title": "县长、县政府党组书记", "start_date": "2025-12", "end_date": "present", "rank": "县处级正职",
     "note": "2025-12-26 八届人大五次会议当选县长"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "<=2025-12", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 吴成智（副书记）
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start_date": "<=2026-07", "end_date": "present", "rank": "县处级副职", "note": "十七届一次全会当选副书记"},
    # 刘雓江（纪委书记）
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start_date": "<=2026-07", "end_date": "present", "rank": "县处级副职", "note": "十七届一次全会常委"},
    {"person_id": 4, "org_id": 3, "title": "县纪委书记", "start_date": "<=2026-07-30", "end_date": "present", "rank": "县处级副职", "note": "十七届纪委一次全会当选书记"},
    # 高芳华（人大主任）
    {"person_id": 5, "org_id": 4, "title": "县人大常委会主任", "start_date": "2025-12-26", "end_date": "present", "rank": "县处级正职", "note": "八届人大五次会议当选"},
    # 原育忠（政协主席）
    {"person_id": 6, "org_id": 5, "title": "县政协主席", "start_date": "unknown", "end_date": "present", "rank": "县处级正职", "note": "2026-08-03 走访部队活动出席"},
    # 县委常委会其他成员
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start_date": "<=2026-07", "end_date": "present", "rank": "县处级副职", "note": "十七届一次全会常委"},
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start_date": "<=2026-07", "end_date": "present", "rank": "县处级副职", "note": "十七届一次全会常委"},
    {"person_id": 8, "org_id": 2, "title": "副县长", "start_date": "unknown", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start_date": "<=2026-07", "end_date": "present", "rank": "县处级副职", "note": "十七届一次全会常委"},
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start_date": "<=2026-07", "end_date": "present", "rank": "县处级副职", "note": "十七届一次全会常委"},
    {"person_id": 10, "org_id": 2, "title": "副县长", "start_date": "unknown", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "县委常委", "start_date": "<=2026-07", "end_date": "present", "rank": "县处级副职", "note": "十七届一次全会常委"},
    {"person_id": 12, "org_id": 1, "title": "县委常委", "start_date": "<=2026-07", "end_date": "present", "rank": "县处级副职", "note": "十七届一次全会常委"},
    {"person_id": 13, "org_id": 1, "title": "县委常委", "start_date": "<=2026-07", "end_date": "present", "rank": "县处级副职", "note": "十七届一次全会常委"},
    # 副县长
    {"person_id": 14, "org_id": 2, "title": "副县长", "start_date": "unknown", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "副县长", "start_date": "unknown", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "副县长", "start_date": "unknown", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "副县长", "start_date": "unknown", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 前任书记
    {"person_id": 18, "org_id": 1, "title": "县委书记（前任，已卸任）", "start_date": "unknown", "end_date": "<=2026-07", "rank": "县处级正职",
     "note": "2025-12 县八届人大五次会议前排就座；第十七届换届前卸任"},
]

relationships = [
    # 由远飞 与 王茜 (党政搭档)
    {"person_a": 1, "person_b": 2, "type": "co_leadership", "context": "县委书记与县长党政搭班（十七次党代会、走访慰问、防汛等共同履职）",
     "overlap_org": "宽甸满族自治县", "overlap_period": "2025-present", "confidence": "confirmed"},
    # 由远飞 与 吴成智 (书记+副书记)
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县委常委会：书记+副书记", "overlap_org": "中共宽甸县委",
     "overlap_period": "2026-07-present", "confidence": "confirmed"},
    # 王茜 与 高芳华 / 原育忠 (县长与人大/政协)
    {"person_a": 2, "person_b": 5, "type": "co_leadership", "context": "县长与县人大主任，2025-12 八届人大五次会议同期当选", "overlap_org": "宽甸县",
     "overlap_period": "2025-12-present", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 6, "type": "co_leadership", "context": "县长与县政协主席同届县领导", "overlap_org": "宽甸县",
     "overlap_period": "2025-present", "confidence": "confirmed"},
    # 由远飞 与 刘汝江 (书记+纪委书记)
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "县委常委会：县委书记与纪委书记", "overlap_org": "中共宽甸县委",
     "overlap_period": "2026-07-present", "confidence": "confirmed"},
    # 前任书记交接 (倪志新 → 由远飞)
    {"person_a": 18, "person_b": 1, "type": "predecessor_successor", "context": "倪志新任县委书记至第十七届换届前，由远飞接任书记",
     "overlap_org": "中共宽甸县委", "overlap_period": "~2025-2026-07", "confidence": "plausible"},
    # 由远飞 与 其他常委 (常委会同班子)
    {"person_a": 1, "person_b": 7, "type": "co_leadership", "context": "十七届县委常委会委员", "overlap_org": "中共宽甸县委", "overlap_period": "2026-07-present", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 8, "type": "co_leadership", "context": "十七届县委常委会委员", "overlap_org": "中共宽甸县委", "overlap_period": "2026-07-present", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 9, "type": "co_leadership", "context": "十七届县委常委会委员", "overlap_org": "中共宽甸县委", "overlap_period": "2026-07-present", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 10, "type": "co_leadership", "context": "十七届县委常委会委员", "overlap_org": "中共宽甸县委", "overlap_period": "2026-07-present", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 11, "type": "co_leadership", "context": "十七届县委常委会委员", "overlap_org": "中共宽甸县委", "overlap_period": "2026-07-present", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 12, "type": "co_leadership", "context": "十七届县委常委会委员", "overlap_org": "中共宽甸县委", "overlap_period": "2026-07-present", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 13, "type": "co_leadership", "context": "十七届县委常委会委员", "overlap_org": "中共宽甸县委", "overlap_period": "2026-07-present", "confidence": "confirmed"},
]


# ── Person JSONs ────────────────────────────────────────────────────────
def write_person_jsons():
    """Write per-person graph JSON for the two core leaders (书记 & 县长)."""

    youyuanfei = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "辽宁省", "city": "丹东市", "region": "宽甸满族自治县",
            "job": "县委书记", "task_id": "liaoning_宽甸满族自治县", "time_focus": "2025-2026",
        },
        "identity": {
            "person_id": "dandong_kuandian_youyuanfei",
            "name": "由远飞",
            "aliases": [],
            "gender": "男",
            "ethnicity": "待查",
            "birth": "",
            "birthplace": "",
            "native_place": "",
            "education": [{"period": "", "institution": "待查", "major": "", "degree": "", "study_type": "unknown", "source_ids": []}],
            "party_join": "中共党员",
            "work_start": "",
            "dedupe_keys": {"name_birth": "由远飞_unknown", "name_birthplace": "由远飞_unknown",
                            "official_profile_url": "https://www.lnkd.gov.cn/html/KDXZF/202607/0178545928874510.html"},
        },
        "current_status": {
            "current_post": "县委书记", "current_org": "中共宽甸满族自治县委员会",
            "administrative_rank": "县处级正职", "as_of": AS_OF, "is_current_confirmed": True,
            "source_ids": ["S004", "S002", "S006"],
        },
        "career_timeline": [
            {"start": "<=2026-07", "end": "present", "org": "中共宽甸满族自治县委员会", "title": "县委书记",
             "level": "县处级", "location": "丹东市宽甸县", "system": "party", "rank": "县处级正职",
             "is_key_promotion": True, "notes": "2026-07-30/31 第十七次党代会连任（选举），并主持十七届一次全会；2026-07-14 调研督导城市防汛",
             "confidence": "confirmed", "source_ids": ["S004", "S006"]},
            {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
             "level": "", "location": "", "system": "other", "rank": "", "is_key_promotion": False,
             "notes": "任县委书记之前（出生、籍贯、学历、入党时间、此前职务）官方公开资料缺失，属待查", "confidence": "unverified", "source_ids": []},
        ],
        "organizations": [{"name": "中共宽甸满族自治县委员会", "role": "县委书记"}],
        "relationships": [
            {"person": "王茜", "person_id": "dandong_kuandian_wangdi", "relationship_type": "co_leadership",
             "strength": "strong", "evidence": "现任搭班：县委书记+县长（十七次党代会、走访慰问共同出席）", "overlap_org": "宽甸县",
             "overlap_period": "2025-", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
            {"person": "吴成福", "person_id": "dandong_kuandian_wuchenengfu", "relationship_type": "superior_subordinate",
             "strength": "medium", "evidence": "县委副书记（大会主席团及全会）", "overlap_org": "中共宽甸县委",
             "overlap_period": "2026-07-", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S004"]},
            {"person": "倪志新", "person_id": "dandong_kuandian_nizhixin", "relationship_type": "predecessor_successor",
             "strength": "medium", "evidence": "倪志新任至第十七届换届前，由远飞接任", "overlap_org": "中共宽甸县委",
             "overlap_period": "~2025-2026-07", "direction": "other_to_person", "confidence": "plausible", "source_ids": ["S005"]},
        ],
        "governance_record": [
            {"period": "2026-07", "domain": "public_security", "achievement_or_event": "调研督导城市防汛（北山公园、东滨河、万江首府、八一水库、物资储备库、消防大队）",
             "role_in_event": "县委书记带队", "measurable_outcome": "", "location": "宽甸县", "confidence": "confirmed", "source_ids": ["S006"]},
            {"period": "2026-07", "domain": "rural_revitalization", "achievement_or_event": "召开全县蓝莓产业发展研讨会，部署特色农业产业",
             "role_in_event": "县委书记主持", "measurable_outcome": "", "location": "宽甸县", "confidence": "confirmed", "source_ids": ["S008"]},
        ],
        "professional_profile": {
            "primary_specializations": [], "secondary_specializations": [],
            "career_pattern": "unknown", "systems_experience": ["party"],
            "geographic_pattern": [], "promotion_velocity": {"summary": "现任县委书记，初始履历未知", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {"trait": "grassroots_oriented", "evidence": "多次带队督导防汛、安全生产、特色产业", "confidence": "plausible", "source_ids": ["S006", "S008"]}
            ],
            "speech_themes": ["人民至上", "防汛安全", "特色农业", "作风整顿", "一流营商环境"],
            "management_signals": ["部署\"推靠、穿透、一线、闭环\"工作法"],
            "caveat": "Work style inferred from public records, not assessment.",
        },
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "截至2026-08-06未检索到违纪或负面舆情（公开来源）", "date": "", "confidence": "unverified", "source_ids": []}
        ],
        "source_register": [
            {"id": "S002", "title": "由远飞、王茜走访慰问驻宽某部官兵", "url": "https://www.lnkd.gov.cn/html/KDXZF/202608/0178571858761522.html",
             "publisher": "宽甸满族自治县人民政府", "published_at": "2026-08-03", "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
            {"id": "S004", "title": "十七届委员会第一次全体会议", "url": "https://www.lnkd.gov.cn/html/KDXZF/202607/0178545928874510.html",
             "publisher": "宽甸发布", "published_at": "2026-07-31", "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
            {"id": "S005", "title": "八届人大五次会议闭幕（含前任书记倪志新、新任县长、人大主任）", "url": "https://www.lnkd.gov.cn/html/KDXZF/202512/0176674383048451.html",
             "publisher": "宽甸发布", "published_at": "2025-12-29", "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
            {"id": "S006", "title": "县委书记由远飞调研督导城市防汛工作", "url": "https://www.lnkd.gov.cn/html/KDXZF/202607/0178393348402478.html",
             "publisher": "宽甸发布", "published_at": "2026-07-14", "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
            {"id": "S008", "title": "宽甸县蓝莓产业发展研讨会召开", "url": "https://www.dandong.gov.cn/html/DDSZF/202607/0178476777496964.html",
             "publisher": "丹东市人民政府", "published_at": "2026-07-23", "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
        ],
        "confidence_summary": {
            "identity": "unverified", "current_role": "confirmed", "career_completeness": "thin",
            "relationship_confidence": "high", "biggest_gap": "由远飞完整履历（出生/籍贯/学历/入党/此前职务）",
        },
        "open_questions": [
            {"priority": "critical", "question": "由远飞出生年月、籍贯、教育背景、入党时间、参加工作时间", "why_it_matters": "基本身份信息缺失",
             "suggested_queries": ["由远飞 简历 宽甸 书记"], "last_attempted": AS_OF},
            {"priority": "high", "question": "由远飞何时何地调任宽甸县委书记，此前担任何职", "why_it_matters": "判断干部交流/晋升源头",
             "suggested_queries": ["由远飞 任前公示 丹东 市委书记"], "last_attempted": AS_OF},
            {"priority": "high", "question": "前任书记骰志新卸任时间与去向", "why_it_matters": "交接时间与去向线索",
             "suggested_queries": ["倪志新 宽甸 卸任 去向"], "last_attempted": AS_OF},
        ],
    }

    wangdi = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "辽宁省", "city": "丹东市", "region": "宽甸满族自治县",
            "job": "县长", "target": "政府一把手", "task_id": "liaoning_宽甸满族自治县", "time_focus": "2025-2026",
        },
        "identity": {
            "person_id": "dandong_kuandian_wangdi",
            "name": "王茜",
            "aliases": [],
            "gender": "女",
            "ethnicity": "满族",
            "birth": "1987年1月",
            "birthplace": "",
            "native_place": "",
            "education": [{"period": "", "institution": "在职研究生", "major": "工商管理", "degree": "硕士", "study_type": "part_time", "source_ids": ["S001"]}],
            "party_join": "中共党员",
            "work_start": "",
            "dedupe_keys": {"name_birth": "王茜_1987", "name_birthplace": "王茜_unknown", "official_profile_url": "https://www.lnkd.gov.cn/html/KDXZF/202512/0176483070074477.html"},
        },
        "current_status": {
            "current_post": "县委副书记、县长", "current_org": "宽甸满族自治县人民政府",
            "administrative_rank": "县处级正职", "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S001", "S003"],
        },
        "career_timeline": [
            {"start": "2025-12-26", "end": "present", "org": "宽甸满族自治县人民政府", "title": "县长、县政府党组书记",
             "level": "县处级", "location": "丹东市宽甸县", "system": "government", "rank": "县处级正职", "is_key_promotion": True,
             "notes": "2025-12-26 八届人大五次会议当选；分管审计局，主持县政府党组全面工作", "confidence": "confirmed", "source_ids": ["S001", "S003"]},
            {"start": "<=2025-12", "end": "present", "org": "中共宽甸满族自治县委员会", "title": "县委副书记",
             "level": "县处级", "location": "宽甸县", "system": "party", "rank": "县处级正职", "is_key_promotion": False,
             "notes": "兼任县政府党组书记", "confidence": "confirmed", "source_ids": ["S003"]},
            {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
             "level": "", "location": "", "system": "other", "rank": "", "is_key_promotion": False,
             "notes": "任县长前的早年履历（此前职务、参加工作时间）官方资料未展开", "confidence": "unverified", "source_ids": []},
        ],
        "organizations": [{"name": "宽甸满族自治县人民政府", "role": "县长"}],
        "relationships": [
            {"person": "由远飞", "person_id": "dandong_kuandian_niyuanfei", "relationship_type": "co_leadership",
             "strength": "strong", "evidence": "现任搭班：县委书记+县长", "overlap_org": "宽甸县", "overlap_period": "2025-",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]},
            {"person": "高芳华", "person_id": "dandong_kuandian_gaofanghua", "relationship_type": "co_leadership",
             "strength": "medium", "evidence": "县人大主任，2025-12 同届当选", "overlap_org": "宽甸县", "overlap_period": "2025-12-",
             "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]},
        ],
        "governance_record": [
            {"period": "2025-12", "domain": "economic_development", "achievement_or_event": "当选后讲话强调产业发展、项目建设、招商引资、民生兜底、依法行政",
             "role_in_event": "县长", "measurable_outcome": "", "location": "宽甸县", "confidence": "confirmed", "source_ids": ["S003"]},
        ],
        "professional_profile": {
            "primary_specializations": ["工商管理"], "secondary_specializations": [],
            "career_pattern": "unknown", "systems_experience": ["government"],
            "geographic_pattern": ["宽甸县"], "promotion_velocity": {"summary": "1987年生，2025-12 当选县长（较年轻），晋升路径待查", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {"trait": "pragmatic", "evidence": "当选讲话强调产业、项目、招商、民生、法治、廉洁", "confidence": "plausible", "source_ids": ["S003"]}
            ],
            "speech_themes": ["高质量发展", "项目建设", "招商引资", "民生", "依法行政", "清正廉洁"],
            "management_signals": [],
            "caveat": "Work style inferred from public records, not assessment.",
        },
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "截至2026-08-06未检索到违纪或负面记录", "date": "", "confidence": "unverified", "source_ids": []}
        ],
        "source_register": [
            {"id": "S001", "title": "王茜 - 政府领导简历", "url": "https://www.lnkd.gov.cn/html/KDXZF/202512/0176483070074477.html",
             "publisher": "宽甸满族自治县人民政府", "published_at": "2025-12-15", "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
            {"id": "S003", "title": "八届人大五次会议胜利闭幕（王茜当选县长）", "url": "https://www.lnkd.gov.cn/html/KDXZF/202512/0176674383048451.html",
             "publisher": "宽甸发布", "published_at": "2025-12-29", "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
        ],
        "confidence_summary": {
            "identity": "confirmed", "current_role": "confirmed", "career_completeness": "thin",
            "relationship_confidence": "high", "biggest_gap": "王茜任县长前的更履历",
        },
        "open_questions": [
            {"priority": "high", "question": "王茜任县长前担任何职、何时进入县委/县政府", "why_it_matters": "判断成长轨迹与干部来源",
             "suggested_queries": ["王茜 宽甸 此前 任职"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "王茜加入工作与入党时间、籍贯", "why_it_matters": "身份档案补充", "suggested_queries": ["王茜 1987 宽甸 县长 简历"], "last_attempted": AS_OF},
        ],
    }

    person_dir = _CURRENT_DIR
    today = AS_OF.replace("-", "")
    for fname, data in [
        (f"{today}-辽宁省-丹东市-县委书记-由远飞.json", youyuanfei),
        (f"{today}-辽宁省-丹东市-县长-王茜.json", wangdi),
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
    for f in sorted(_CURRENT_DIR.glob("*.json")):
        if "宽甸满族自治县" in f.name and ("县委书记" in f.name or "县长" in f.name):
            print(f"  JSON: {f}")


if __name__ == "__main__":
    main()