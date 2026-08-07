#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 龙港区 (葫芦岛市，辽宁省).

Investigation date: 2026-08-07
Task ID: liaoning_龙港区
Level: 市辖区
Parent city: 葫芦岛市
Targets: 区委书记 & 区长

Research status: PRIMARY SOURCE ACCESS (official district portal lgq.gov.cn)
  - 葫芦岛市龙港区人民政府门户（www.lgq.gov.cn）一手信源可访问：政务要闻、区委理论学习中心组、
    区人大常委会人事任免等。当前可检索到的最新年份为 2025-02。
  - 现任区委书记 袁伶（葫芦岛市人民政府副市长兼龙港区委书记）、区委副书记/区长 曹亮 通过官方
    一手信源确认（2025-02 区政常务会议、2024 年度民主生活会）。
    * 2025-02-11 区委理论学习中心组学习会议 由副市长、区委书记袁伶主持
    * 2025-02-24 区政府第39次常务会议 区委副书记、区长曹亮主持
    * 2025-02-19 区委常委班子2024年度民主生活会：袁伶（书记）主持，曹亮（区长）、逯化生
      （区委副书记、社会工作部部长）出席，范立民（人大书记/主任）、李晓民（政协党组书记/主席）列席
    * 2024-12-27 袁伶等区领导看望与会人大代表；2024 全年区委常委会多场由袁伶主持
    * 曹亮 2021-12-08 以"代区长"作区六届人大一次会议政府工作报告并当选区长；2022/2023/2024
      区六届人大三/五/六次会议政府工作报告署"区长 曹亮"
  - 前任区委书记 王胜秋（2021年上半年仍在任）；前任区长 袁伶（袁凌由区长转任区委书记）。
  - Exa 检索可及一手信源，但公开文本渠道对袁凌/曹亮的出生/籍贯/学历/入党时间及任区委书记/
    区长前履历的完整细节有限；袁凌 2017 年葫芦岛市委组织部任前公示（妇联副主席拟任市政府法制办
    专职副主任）提供其出生/党派等身份信息（女，满族，1973-08 生），按 plausible 标注。

Confirmed current officeholders (as of 2025-02, official 一手):
   - 区委书记: 袁伶（葫芦岛市副市长兼龙港区委书记；2025-02 会议记录；区委书记自 ~2021 至今）
   - 区委副书记、区长、区政府党组书记: 曹亮（2021-12 起任代区长/区长至 2025-02，持续）
   - 区委副书记、社会工作部部长: 逯化生（2025-02 民主生活会）；前任区委副书记 刘剑（2024）
   - 区政府班子成员：区委常委、常务副区长、区政府党组副书记 夏爽（区委审计委员会副主任）；
     副区长 龚勋、叶强、高飞；2024-11 区人大常委会任命汪舟为副区长。
   - 区委常委（历届会议陆续出现）：李洪波、龚勋、叶强、关德权、马欢、高飞、夏爽、刘剑、逯化生
   - 区人大常委会主任：范立民；区政协党组书记、主席：李晓民

Predecessor / successor timeline:
   - 区委书记线：王胜秋（~2018–2021，2021-05 仍以区委书记开常委会）→ 袁伶（~2021 至今；
     同时于 ~2022 起兼葫芦岛市副市长）
   - 区长线：袁伶（区长，2020-12 作政府工作报告，~2018–2021）→ 曹亮（2021-07 代区长，
     2021-12 当选区长，至今）
   - 区委副书记线：刘剑（2024）→ 叶芳/逯化生？ → 逯化生（2025-02 区委副书记、社会工作部部长）

Cross-region / context:
   - 龙港区系葫芦岛市委、市政府、军分区等驻地，是全市的政治、经济、文化中心城区之一，
     下辖街道（龙湾、玉皇、马仗房等）。区委书记属县处级正职（由市级领导兼任市委常委/副市长高配）。
   - 袁凌由市政府办公厅（法制办）→ 龙港区长 → 区委书记 → 市委，履历体现市级机关与区级主官之间
     的上下交流模式；龙港区书记由副市长兼任，为辽市级领导兼任区委书记的典型安排。

Confidence policy: 当前任职 confirmed（官方一手，截至 2025-02）；领导班姓名录 confirmed（区政
  府/人大一手）；袁凌身份字段（出生年月、民族、学历）plausible（2017 市委组织部公示，姓名/
  地域一致）；曹强出生/籍贯/学历等身份字段 unverified（公开文本渠道未检索到）。
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
SLUG = "龙港区"
AS_OF = "2026-08-06"
AS_OF_CONFIRMED = "2025-02"  # 最新一手信源确认的在任时间点

_CURRENT_DIR = Path(__file__).parent.resolve()
DB_PATH = _CURRENT_DIR / f"{SLUG}_network.db"
GEXF_PATH = _CURRENT_DIR / f"{SLUG}_network.gexf"
PERSONS_STAGING_DIR = _CURRENT_DIR

# ── Persons ──────────────────────────────────────────────────────────────
# 一手来源：葫芦岛市龙港区人民政府门户（www.lgq.gov.cn）政务要闻 / 区人大 / 民主生活会；
#        2017 葫芦岛市委组织部任前公示（袁伶身份信息）
persons = [
    # ── 核心：区委（现职） ──
    {"id": 1, "name": "袁伶", "gender": "女", "ethnicity": "满族", "birth": "1973-08",
     "birthplace": "待查", "education": "研究生学历，理学硕士学位", "party_join": "中共党员", "work_start": "1997-08",
     "current_post": "区委书记（葫芦岛市副市长兼）", "current_org": "中国共产党龙港区委员会",
     "source": "https://www.lgq.gov.cn/xxzx/lgyw/ (2025-02 区委理论学习中心组学习会议) + 2017 葫芦岛市委组织部任前公示"},
    {"id": 2, "name": "曹亮", "gender": "男", "ethnicity": "待确认", "birth": "",
     "birthplace": "", "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "区委副书记、区长、区政府党组书记", "current_org": "龙港区人民政府",
     "source": "https://www.lgq.gov.cn/zwgk/jbxxgk/zfhy/cwhy/202502/t20250225_1200603.html (2025-02-24 常务会议) + 区六届人大一次会议选举"},
    # ── 区委（副书记） ──
    {"id": 3, "name": "逯化生", "gender": "男", "ethnicity": "待确认", "birth_year": "",
     "birthplace": "", "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "区委副书记、社会工作部部长", "current_org": "中国共产党龙港区委员会",
     "source": "https://www.lgq.gov.cn/xxzx/lgyw/202502/t20250219_1200071.html (2025-02-19 民主生活会)"},
    # ── 区政府领导班子（区委常委/副区长） ──
    {"id": 4, "name": "夏爽", "gender": "男", "ethnicity": "待确认", "birth_year": "",
     "birthplace": "", "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、常务副区长、区政府党组副书记", "current_org": "龙港区人民政府",
     "source": "https://sjj.ln.gov.cn/ (第十次区委审计委员会，副主任) + 区六届人大四次会议主席台名单"},
    {"id": 5, "name": "龚勋", "gender": "男", "ethnicity": "待确认", "birth_year": "",
     "birthplace": "", "education": "待查", "party_join": "", "work_start": "",
     "current_post": "区委常委、副区长", "current_org": "龙港区人民政府",
     "source": "https://www.lgq.gov.cn/xxzx/lgyw/202209/t20220930_1118042.html (2022-09 副区长) + 审计委员会委员"},
    {"id": 6, "name": "叶强", "gender": "男", "ethnicity": "待确认", "birth_year": "",
     "birthplace": "", "education": "待查", "party_join": "", "work_start": "",
     "current_post": "区委常委、副区长", "current_org": "龙港区人民政府",
     "source": "https://www.lgq.gov.cn/xxzx/lgyw/202401/t20240112_1164914.html (2024-01 区委常委领学)"},
    {"id": 7, "name": "高飞", "gender": "男", "ethnicity": "待确认", "birth_year": "",
     "birthplace": "", "education": "待查", "party_join": "", "work_start": "",
     "current_post": "副区长", "current_org": "龙港区人民政府",
     "source": "https://www.lgq.gov.cn/xxzx/lgyw/202404/t20240402_1171990.html (2024-04 人才工作领导小组) + 健康产业园调研"},
    {"id": 8, "name": "汪舟", "gender": "男", "ethnicity": "待确认", "birth_year": "",
     "birthplace": "", "education": "待查", "party_join": "", "work_start": "",
     "current_post": "副区长", "current_org": "龙港区人民政府",
     "source": "https://www.lgq.gov.cn/xxzx/lgyw/202411/t20241129_1193168.html (2024-11-28 区六届人大常委会第二十四次会议任命)"},
    # ── 人大/政协 ──
    {"id": 9, "name": "范立民", "gender": "男", "ethnicity": "待确认", "birth_year": "",
     "birthplace": "", "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "区人大常委会党组书记、主任", "current_org": "龙港区人民代表大会常务委员会",
     "source": "https://www.lgq.gov.cn/xxzx/lgyw/202502/t20250219_1200071.html (2025-02-19 民主生活会列席)"},
    {"id": 10, "name": "李晓民", "gender": "男", "ethnicity": "待确认", "birth_year": "",
     "birthplace": "", "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "区政协党组书记、主席", "current_org": "中国人民政治协商会议龙港区委员会",
     "source": "https://www.lgq.gov.cn/xxzx/lgyw/202502/t20250219_1200071.html (2025-02-19 民主生活会列席)"},
    # ── 前任 ──
    {"id": 11, "name": "王胜秋", "gender": "男", "ethnicity": "待确认", "birth_year": "",
     "birthplace": "", "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "前任区委书记（2018–2021）", "current_org": "",
     "source": "https://www.lgq.gov.cn/xxzx/tpxw/index_13.html (2021-05 中共龙港五届区委第205次常委会)"},
    {"id": 12, "name": "刘剑", "gender": "男", "ethnicity": "待确认", "birth_year": "",
     "birthplace": "", "education": "待查", "party_join": "中共党员", "work_start": "",
     "current_post": "前任区委副书记（2024）", "current_org": "",
     "source": "https://www.lgq.gov.cn/xxzx/lgyw/202401/t20240112_1164914.html (2024-01) + 2024-04 人才工作"},
]

organizations = [
    {"id": 1, "name": "中国共产党龙港区委员会", "type": "党委", "level": "县处级", "parent": "中共葫芦岛市委", "location": "辽宁省葫芦岛市龙港区"},
    {"id": 2, "name": "龙港区人民政府", "type": "政府", "level": "县处级", "parent": "葫芦岛市人民政府", "location": "辽宁省葫芦岛市龙港区"},
    {"id": 3, "name": "龙港区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "葫芦岛市人大常委会", "location": "辽宁省葫芦岛市龙港区"},
    {"id": 4, "name": "中国人民政治协商会议龙港区委员会", "type": "政协", "level": "县处级", "parent": "葫芦岛市政协", "location": "辽宁省葫芦岛市龙港区"},
    {"id": 5, "name": "中国共产党龙港区纪律检查委员会/龙港区监察委员会", "type": "纪委", "level": "县处级", "parent": "中共葫芦岛市纪委", "location": "辽宁省葫芦岛市龙港区"},
    {"id": 6, "name": "中国共产党葫芦岛市委员会", "type": "党委", "level": "地厅级", "parent": "中共辽宁省委", "location": "辽宁省葫芦岛市"},
    {"id": 7, "name": "葫芦岛市人民政府", "type": "政府", "level": "地厅级", "parent": "辽宁省人民政府", "location": "辽宁省葫芦岛市"},
]

positions = [
    # 袁伶(1) 区委书记
    {"person_id": 1, "org_id": 6, "title": "葫芦岛市人民政府副市长", "start_date": "~2022", "end_date": "present", "rank": "地厅级副职",
     "note": "2025-02-19 民主生活会'市政府副市长、区委书记袁伶'；2023-07 新闻多次以副市长兼区委书记出现"},
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "~2021", "end_date": "present", "rank": "县处级正职",
     "note": "2022-09 民主生活会'区委书记袁伶'主持；2021 王普秋仍任书记，袁凌 2021 下半年接任"},
    {"person_id": 1, "org_id": 2, "title": "区长", "start_date": "~2018", "end_date": "~2021", "rank": "县处级正职",
     "note": "2020-12-28 区五届人大四次会议作政府工作报告署'区长 袁伶'；2021-07 前后转任区委书记"},
    {"person_id": 1, "org_id": 7, "title": "葫芦岛市人民政府办公室/法制办公室（此前）", "start_date": "~2017", "end_date": "~2018", "rank": "县处级",
     "note": "2017 任前公示：市妇联党组成员、副主席 拟任市政府法制办公室专职副主任；后进入区级领导序列"},
    # 曹亮(2) 区长
    {"person_id": 2, "org_id": 2, "title": "区委副书记、区长、区政府党组书记", "start_date": "2021-12", "end_date": "present", "rank": "县处级正职",
     "note": "2021-07 以'代区长'赴乡街调研；2021-12 区六届人大一次会议作报告并当选；2022-2025 连续作政府工作报告"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "~2021", "end_date": "present", "rank": "县处级正职",
     "note": "区长期间兼区委副书记"},
    # 逯化生(3) 区委副书记
    {"person_id": 3, "org_id": 1, "title": "区委副书记、社会工作部部长", "start_date": "<=2025", "end_date": "present", "rank": "县处级副职",
     "note": "2025-02-19 民主生活会出席；此前区委副书记为刘剑（2024）"},
    # 夏爽(4) 常务副区长
    {"person_id": 4, "org_id": 2, "title": "区委常委、常务副区长、区政府党组副书记", "start_date": "<=2023", "end_date": "present", "rank": "县处级副职",
     "note": "2024-09 区委审计委员会副主任；区六届人大四次会议主席台"},
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start_date": "<=2023", "end_date": "present", "rank": "县处级副职", "note": "2024-01 区委常委会领学"},
    # 龚勋(5)
    {"person_id": 5, "org_id": 2, "title": "区委常委、副区长", "start_date": "<=2022", "end_date": "present", "rank": "县处级副职",
     "note": "2022-09 副区长龚勋；2024-09 区委审计委员会委员；2024-11 区人大常委会议"},
    {"person_id": 5, "org_id": 1, "title": "区委常委", "start_date": "<=2024", "end_date": "present", "rank": "县处级副职", "note": "2024-01 区委常委会领学"},
    # 叶强(6)
    {"person_id": 6, "org_id": 1, "title": "区委常委", "start_date": "<=2024", "end_date": "present", "rank": "县处级副职",
     "note": "2024-01 区委常委会领学"}, 
    # 高飞(7) 副区长
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "<=2024", "end_date": "present", "rank": "县处级副职",
     "note": "2024-04 人才工作领导小组参加；2023-07 健康产业园陪调研（副区长）"},
    # 汪舟(8) 副区长
    {"person_id": 8, "org_id": 2, "title": "副区长", "start_date": "2024-11", "end_date": "present", "rank": "县处级副职",
     "note": "2024-11-28 区六届人大常委会第二十四次会议任命"},
    # 范立民(9) 人大主任
    {"person_id": 9, "org_id": 3, "title": "区人大常委会党组书记、主任", "start_date": "<=2024", "end_date": "present", "rank": "县处级正职",
     "note": "2025-02-19 民主生活会列席；2024-11 主持区人大常委会会议"},
    # 李晓民(10) 政协主席
    {"person_id": 10, "org_id": 4, "title": "区政协党组书记、主席", "start_date": "<=2025", "end_date": "present", "rank": "县处级正职",
     "note": "2025-02-19 民主生活会列席"},
    # 王胜秋(11) 前任书记
    {"person_id": 11, "org_id": 1, "title": "区委书记", "start_date": "~2018", "end_date": "~2021", "rank": "县处级正职",
     "note": "2021-03-05 企业家早餐会、2021-05-28 区委常委会（仍为区委书记）；袁凌后接任"},
    # 刘剑(12) 前任副书记
    {"person_id": 12, "org_id": 1, "title": "区委副书记", "start_date": "2024", "end_date": "~2024/2025", "rank": "县处级副职",
     "note": "2024-01 区委常委会、2024-04 人才领导小组会议以区委副书记列席；2025 年后由逯化生接任"},
]

relationships = [
    # 党政一把手搭班
    {"person_a": 1, "person_b": 2, "type": "co_leadership", "context": "区委书记（袁伶）与区委副书记、区长（曹亮）——党政一把手搭班（龙港区）",
     "overlap_org": "龙港区", "overlap_period": "2021-2025", "confidence": "confirmed"},
    # 书记与副书记
    {"person_a": 1, "person_b": 3, "type": "co_leadership", "context": "区委书记与区委副书记、社会工作部部长逯化生",
     "overlap_org": "中共龙港区委", "overlap_period": "2025-", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 12, "type": "co_leadership", "context": "区委书记与前任区委副书记刘剑（2024 区委常委会同席）",
     "overlap_org": "中共龙港区委", "overlap_period": "2024", "confidence": "confirmed"},
    # 前任书记链: 王胜秋 → 袁伶
    {"person_a": 1, "person_b": 11, "type": "predecessor_successor", "context": "袁伶接任王胜秋的区委书记职位（~2021）",
     "overlap_org": "中共龙港区委", "overlap_period": "2018-~2021", "confidence": "confirmed"},
    # 区长前任链: 袁伶(区长) → 曹亮(区长)，袁伶(区长→书记) 与 曹亮搭班
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor", "context": "袁伶原任区长，转任区委书记后由曹亮接任区长",
     "overlap_org": "龙港区人民政府", "overlap_period": "2021", "confidence": "confirmed"},
    # 区长与政府班子
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "区长与常务副区长、区政府党组副书记",
     "overlap_org": "龙港区人民政府", "overlap_period": "2021-2025", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 5, "type": "co_leadership", "context": "区长与区委常委、副区长龚勋",
     "overlap_org": "龙港区人民政府", "overlap_period": "2022-2025", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 6, "type": "co_leadership", "context": "区长与区委常委叶强",
     "overlap_org": "龙港区人民政府", "overlap_period": "2024-2025", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 7, "type": "co_leadership", "context": "区长与副区长高飞（健康产业园陪调研）",
     "overlap_org": "龙港区人民政府", "overlap_period": "2023-2025", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "区长与副区长汪舟（2024-11 人大常委会任命）",
     "overlap_org": "龙港区人民政府", "overlap_period": "2024-", "confidence": "confirmed"},
    # 常务副区长核心节点
    {"person_a": 4, "person_b": 5, "type": "co_leadership", "context": "常务副区长与其他副区长（区委常委）共事",
     "overlap_org": "龙港区人民政府", "overlap_period": "2023-2025", "confidence": "confirmed"},
    {"person_a": 4, "person_b": 2, "type": "superior_subordinate", "context": "常务副区长协管区政府常务（审计委员会副主任）",
     "overlap_org": "龙港区人民政府", "overlap_period": "2023-2025", "confidence": "confirmed"},
    # 人大/政协领导层联系
    {"person_a": 1, "person_b": 9, "type": "co_leadership", "context": "区委书记与区人大常委会主任范立民（民主生活会列席）",
     "overlap_org": "龙港区", "overlap_period": "2024-2025", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 10, "type": "co_leadership", "context": "区委书记与区政协主席李晓民",
     "overlap_org": "龙港区", "overlap_period": "2025-", "confidence": "confirmed"},
]


# ── Person JSONs ─────────────────────────────────────────────────────────
def write_person_jsons():
    """Write per-person graph JSON for core leaders (区委书记 袁伶, 区长 曹亮, 区委副书记 逯化生)."""

    yuan = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {"province": "辽宁省", "city": "葫芦岛市", "region": "龙港区",
                                "job": "区委书记", "task_id": "liaoning_龙港区", "time_focus": "2021-2025"},
        "identity": {
            "person_id": "liaoning_huludao_yuanling",
            "name": "袁伶",
            "aliases": [],
            "gender": "女", "ethnicity": "满族", "birth": "1973-08", "birthplace": "待查", "native_place": "待查",
            "education": [{"period": "", "institution": "（研究生学历，理学硕士）", "major": "理学", "degree": "硕士",
                           "study_type": "unknown", "source_ids": ["S009"]}],
            "party_join": "中共党员（1995-12）", "work_start": "1997-08",
            "dedupe_keys": {"name_birth": "袁伶_1973-08", "name_birthplace": "袁伶_待查",
                            "official_profile_url": "https://sft.ln.gov.cn/sft/fzhyshj/2022120910553632766/index.shtml"},
        },
        "current_status": {"current_post": "区委书记（葫芦岛市副市长兼）", "current_org": "中国共产党龙港区委员会",
                           "administrative_rank": "县处级正职（同时任地厅级副职副市长）", "as_of": AS_OF,
                           "is_current_confirmed": True, "source_ids": ["S001", "S003", "S005"]},
        "career_timeline": [
            {"start": "unknown", "end": "~2017", "org": "履历成长段", "title": "",
             "level": "", "location": "葫芦岛市", "system": "other", "rank": "",
             "notes": "2017 年前在市妇联系统（党组成员、副主席）等任职；完整早年履历公开文本未检索到",
             "confidence": "unverified", "source_ids": []},
            {"start": "~2017", "end": "~2018", "org": "葫芦岛市人民政府", "title": "市政府法制办公室专职副主任（拟任）",
             "level": "县级", "location": "葫芦岛市", "system": "government", "rank": "县处级",
             "notes": "2017 市委组织部任前公示：市妇联党组成员、副主席 拟任市政府法制办公室专职副主任",
             "confidence": "plausible", "source_ids": ["S009"]},
            {"start": "~2018", "end": "~2021", "org": "龙港区人民政府", "title": "区长",
             "level": "县处级", "location": "龙港区", "system": "government", "rank": "县处级正职",
             "notes": "2020-12-28 区五届人大四次会议作政府工作报告署'区长 袁伶'",
             "confidence": "confirmed", "source_ids": ["S008"]},
            {"start": "~2021", "end": "present", "org": "中国共产党龙港区委员会", "title": "区委书记",
             "level": "县处级", "location": "龙港区", "system": "party", "rank": "县处级正职",
             "notes": "2022-09 民主生活会'区委书记袁伶'主持；2024/2025 区委常委会多次主持",
             "confidence": "confirmed", "source_ids": ["S001", "S003", "S005"]},
            {"start": "~2022", "end": "present", "org": "葫芦岛市人民政府", "title": "副市长",
             "level": "地厅级", "location": "葫芦岛市", "system": "government", "rank": "地厅级副职",
             "notes": "2025-02'市政府副市长、区委书记袁伶'；2023-07 多名新闻以副市长兼区委书记身份",
             "confidence": "confirmed", "source_ids": ["S001", "S003"]},
        ],
        "organizations": [
            {"name": "龙港区人民政府", "role": "区长（前任）", "period": "~2018 - ~2021"},
            {"name": "中国共产党龙港区委员会", "role": "区委书记（现任）", "period": "~2021 - 至今"},
            {"name": "葫芦岛市人民政府", "role": "副市长（兼任）", "period": "~2022 - 至今"},
        ],
        "relationships": [
            {"person": "曹亮", "person_id": "liaoning_huludao_caoliang", "relationship_type": "predecessor_successor",
             "strength": "strong", "evidence": "袁伶原任区长，转任区委书记后由曹亮接任区长并长期搭班",
             "overlap_org": "龙港区", "overlap_period": "2021-2025", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S008", "S010"]},
            {"person": "逯化生", "person_id": "liaoning_huludao_luhuasheng", "relationship_type": "co_leadership",
             "strength": "medium", "evidence": "现任区委副书记、社会工作部部长",
             "overlap_org": "中共龙港区委", "overlap_period": "2025-", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
            {"person": "王胜秋", "person_id": "liaoning_huludao_wangshengqiu", "relationship_type": "predecessor_successor",
             "strength": "strong", "evidence": "袁伶接任王胜秋的区委书记职位",
             "overlap_org": "中共龙港区委", "overlap_period": "2018-~2021", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S011"]},
            {"person": "范立民", "person_id": "liaoning_huludao_fanlimin", "relationship_type": "other",
             "strength": "medium", "evidence": "区人大常委会主任，民主生活会列席",
             "overlap_org": "龙港区", "overlap_period": "2024-2025", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        ],
        "governance_record": [
            {"period": "2025-02", "domain": "party_building", "achievement_or_event": "主持区委常委班子2024年度民主生活会，化作纪检要求",
             "role_in_event": "区委书记", "measurable_outcome": "", "location": "龙港区", "confidence": "confirmed", "source_ids": ["S001"]},
            {"period": "2024-12", "domain": "economic_development", "achievement_or_event": "推动'一区六园一港一带'建设、全面振兴新突破三年行动",
             "role_in_event": "区委书记（市政府副市长兼）", "measurable_outcome": "谋划'六个新城区'建设目标", "location": "龙港区",
             "confidence": "confirmed", "source_ids": ["S002"]},
        ],
        "professional_profile": {
            "primary_specializations": [], "secondary_specializations": [],
            "career_pattern": "local_ladder", "systems_experience": ["party", "government", "other"],
            "geographic_pattern": ["辽宁省", "葫芦岛市"], "promotion_velocity": {"summary": "区长→区委书记→兼副市长，区级主官正常晋升路径", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": ["全面振兴新突破", "改革创新", "民生保障", "法治建设"],
            "management_signals": ["统筹发展与安全", "抓项目促投资", "基层减负"],
            "caveat": "Work style inferred from public records, not assessment.",
        },
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "截至 2026-08-06 未发现违纪或被纪律处分性公开报道", "date": "", "confidence": "unverified", "source_ids": []}
        ],
        "source_register": [
            {"id": "S001", "title": "区委常委班子召开2024年度民主生活会", "url": "https://www.lgq.gov.cn/xxzx/lgyw/202502/t20250219_1200071.html",
             "publisher": "龙港区人民政府", "published_at": "2025-02-19", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "袁伶、曹亮、逯化生、范立民、李晓民身份确认"},
            {"id": "S002", "title": "副市长、区委书记袁伶领学区委常委会第138次会议", "url": "https://www.lgq.gov.cn/xxzx/lgyw/202401/t20240112_1164914.html",
             "publisher": "龙港区人民政府", "published_at": "2024-01-12", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "区委常委排名"},
            {"id": "S003", "title": "【市县党政主要负责人谈法治环境】袁伶", "url": "https://sft.ln.gov.cn/sft/fzhyshj/2022111810553632766/index.shtml",
             "publisher": "辽宁省司法厅", "published_at": "2024-12-18", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "市政府副市长、龙港区委书记"},
            {"id": "S008", "title": "2021年龙港区政府工作报告（区长袁伶）", "url": "https://www.lgq.gov.cn/zwgk/jbxxgk/gzbg/202101/t20210113_1017605.html",
             "publisher": "龙港区人民政府", "published_at": "2021-01-13", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "2020-12-28 区长袁伶作报告"},
            {"id": "S009", "title": "中共葫芦岛市委组织部公告(2017年第12号)", "url": "https://blog.hldhtys.com/archives/104716",
             "publisher": "葫芦岛市委组织部（转载）", "published_at": "2017", "accessed_at": AS_OF, "source_type": "appointment_notice", "reliability": "medium", "notes": "袁伶 女 满族 1973-08 研究生 理学 硕士 1997-08 工作 1995-12 入党"},
            {"id": "S010", "title": "2025年龙港区政府工作报告（区长 曹亮）", "url": "http://www.zgcounty.com/wap/news/66201.html",
             "publisher": "中国县域", "published_at": "2024-12-25", "accessed_at": AS_OF, "source_type": "media", "reliability": "medium", "notes": "区长 曹亮"},
            {"id": "S011", "title": "区委书记王普秋主持企业家早餐会/常委会", "url": "https://www.lgq.gov.cn/xxzx/tpxw/index_13.html",
             "publisher": "龙港区人民政府", "published_at": "2021", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "王普秋为前任区委书记"},
        ],
        "confidence_summary": {"identity": "partial", "current_role": "confirmed", "career_completeness": "partial",
                               "relationship_confidence": "high", "biggest_gap": "袁伶任教师/妇联前完整履历与转任区长的具体节点"},
        "open_questions": [
            {"priority": "critical", "question": "袁伶 2018 年前在市妇联/市政府任职的具体时间与职务节点", "why_it_matters": "评估晋升路径与跨系统履历",
             "suggested_queries": ["袁伶 葫芦岛 妇联 简历"], "last_attempted": AS_OF},
            {"priority": "high", "question": "袁伶由区长转任区委书记的具体时间（2021 任前公示/人大常委会）", "why_it_matters": "确定区长空缺与曹亮到任时间",
             "suggested_queries": ["袁伶 任区委书记 龙港 2021"], "last_attempted": AS_OF},
        ],
    }

    cao = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {"province": "辽宁省", "city": "葫芦岛市", "region": "龙港区",
                                "job": "区长", "task_id": "liaoning_龙港区", "time_focus": "2021-2025"},
        "identity": {
            "person_id": "liaoning_huludao_caoliang",
            "name": "曹亮",
            "aliases": [],
            "gender": "男", "ethnicity": "待确认", "birth": "", "birthplace": "", "native_place": "",
            "education": [{"period": "", "institution": "待查", "major": "", "degree": "", "study_type": "unknown", "source_ids": []}],
            "party_join": "中共党员", "work_start": "",
            "dedupe_keys": {"name_birth": "曹亮_unknown", "name_birthplace": "曹亮_unknown",
                            "official_profile_url": "https://www.lgq.gov.cn/zwgk/jbxxgk/zfhy/cwhy/202502/t20250225_1200603.html"},
        },
        "current_status": {"current_post": "区委副书记、区长、区政府党组书记", "current_org": "龙港区人民政府",
                           "administrative_rank": "县处级正职", "is_active": True, "as_of": AS_OF,
                           "is_current_confirmed": True, "source_ids": ["S001", "S004"]},
        "career_timeline": [
            {"start": "unknown", "end": "~2021", "org": "履历缺口", "title": "", "level": "县处级", "location": "葫芦岛市",
             "system": "other", "rank": "", "notes": "任龙港代区长前的完整履历（出生/籍贯/学历/此前职务/来源）公开文本渠道未检索到",
             "confidence": "unverified", "source_ids": []},
            {"start": "2021-07", "end": "2021-12", "org": "龙港区人民政府", "title": "代区长",
             "level": "县处级", "location": "龙港区", "system": "government", "rank": "县处级正职",
             "notes": "2021-07-08 区委副书记、代区长曹亮赴乡街调研社会治理/安全生产/防疫",
             "confidence": "confirmed", "source_ids": ["S007"]},
            {"start": "2021-12", "end": "present", "org": "龙港区人民政府", "title": "区委副书记、区长、区政府党组书记",
             "level": "县处级", "location": "龙港区", "system": "government", "rank": "县处级正职",
             "notes": "2021-12 区六届人大一次会议当选；2022/2023/2024 连续作政府工作报告；2025-02-24 常务会议主持",
             "confidence": "confirmed", "source_ids": ["S001", "S004", "S006"]},
        ],
        "organizations": [
            {"name": "龙港区人民政府", "role": "区长（现任）", "period": "2021-12 - 至今"},
        ],
        "relationships": [
            {"person": "袁伶", "person_id": "liaoning_huludao_yuanling", "relationship_type": "co_leadership",
             "strength": "strong", "evidence": "现任书记与区长搭班；袁伶为其前任区长",
             "overlap_org": "龙港区人民政府", "overlap_period": "2021-2025", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
            {"person": "夏爽", "person_id": "liaoning_huludao_xiashuang", "relationship_type": "superior_subordinate",
             "strength": "medium", "evidence": "区长与常务副区长（区政府党组副书记）",
             "overlap_org": "龙港区人民政府", "overlap_period": "2021-2025", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004"]},
            {"person": "龚勋", "person_id": "liaoning_huludao_gongxun", "relationship_type": "co_leadership",
             "strength": "medium", "evidence": "区长与副区长（区委常委）",
             "overlap_org": "龙港区人民政府", "overlap_period": "2022-2025", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004"]},
        ],
        "governance_record": [
            {"period": "2024-12", "domain": "economic_development", "achievement_or_event": "主持区政府常务会议部署2025年经济工作（GDP预计182亿元，增6%）",
             "role_in_event": "区长", "measurable_outcome": "", "location": "龙港区", "confidence": "confirmed", "source_ids": ["S004"]},
            {"period": "2025-01", "domain": "public_security", "achievement_or_event": "部署2025年一季度安全稳定工作会议",
             "role_in_event": "区长", "measurable_outcome": "", "location": "龙港区", "confidence": "confirmed", "source_ids": ["S012"]},
        ],
        "professional_profile": {
            "primary_specializations": [], "secondary_specializations": [],
            "career_pattern": "local_ladder", "systems_experience": ["government"],
            "geographic_pattern": ["辽宁省", "葫芦岛市"], "promotion_velocity": {"summary": "由代区长升任区长，2021-2025 任内连续多届换届获连任", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {"trait": "grassroots_oriented", "evidence": "代区长期间即赴乡街一线督导治理，部署高危场所安全稳定", "confidence": "plausible", "source_ids": ["S007", "S012"]}
            ],
            "speech_themes": ["开局问暖", "安全生产", "民生保障", "项目为王"],
            "management_signals": ["清单化推进", "压顶压实责任"],
            "caveat": "Work style inferred from public records, not assessment.",
        },
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "截至 2026-08-06 未发现处分或负面公开报道", "date": "", "confidence": "unverified", "source_ids": []}
        ],
        "source_register": [
            {"id": "S001", "title": "区委常委班子2024年度民主生活会", "url": "https://www.lgq.gov.cn/xxzx/lgyw/202502/t20250219_1200071.html",
             "publisher": "龙港区人民政府", "published_at": "2025-02-19", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "区长曹亮出席"},
            {"id": "S004", "title": "区政府第39次常务会议", "url": "https://www.lgq.gov.cn/zwgk/jbxxgk/zfhy/cwhy/202502/t20250225_1200603.html",
             "publisher": "龙港区人民政府", "published_at": "2025-02-25", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "区长曹亮主持"},
            {"id": "S006", "title": "葫芦岛市龙港区2022年政府工作报告", "url": "http://www.zgcounty.com/news/28159.html",
             "publisher": "中国县域", "published_at": "2021-12-08", "accessed_at": AS_OF, "source_type": "media", "reliability": "medium", "notes": "代会2021-12 当选"},
            {"id": "S007", "title": "区委副书记、代区长曹亮赴乡街调研", "url": "https://www.lgq.gov.cn/xxzx/tpxw/index_13.html",
             "publisher": "龙港区人民政府", "published_at": "2021-07", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
            {"id": "S012", "title": "区长曹亮主持召开龙港区2025年一季度安全稳定工作会议", "url": "https://www.lgq.gov.cn/xxzx/lgyw/202501/t20250106_1196183.html",
             "publisher": "龙港区人民政府", "published_at": "2025-01-06", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
            {"id": "S008", "title": "2021年龙港区政府工作报告（区长 袁伶）", "url": "https://www.lgq.gov.cn/zwgk/jbxxgk/gzbg/202101/t20210113_1017605.html",
             "publisher": "龙港区人民政府", "published_at": "2021-01-13", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "前任区长袁伶、继任曹亮"},
        ],
        "confidence_summary": {"identity": "unverified", "current_role": "confirmed", "career_completeness": "thin",
                               "relationship_confidence": "medium", "biggest_gap": "曹亮出生/籍贯/学历/入党时间及任区长前完整履历"},
        "open_questions": [
            {"priority": "critical", "question": "曹亮出生年月、教育背景、籍贯及任代区长前职务/来源", "why_it_matters": "身份与晋升轨迹细节",
             "suggested_queries": ["曹亮 龙港 区长 简历"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "2025 年下半年起龙港区委书记/区长是否发生调整", "why_it_matters": "确认当前（2026）在任情况", "suggested_queries": ["龙港区委书记2026"], "last_attempted": AS_OF},
        ],
    }

    lu = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {"province": "辽宁省", "city": "葫芦岛市", "region": "龙港区",
                                "job": "区委副书记", "task_id": "liaoning_龙港区", "time_focus": "2025"},
        "identity": {
            "person_id": "liaoning_huludao_luhuasheng",
            "name": "逯化生",
            "aliases": [],
            "gender": "男", "ethnicity": "待查", "birth": "", "birthplace": "", "native_place": "",
            "education": [{"period": "", "institution": "待查", "major": "", "degree": "", "study_type": "unknown", "source_ids": []}],
            "party_join": "中共党员", "work_start": "",
            "dedupe_keys": {"name_birth": "逯化生_unknown", "name_birthplace": "逯化生_unknown",
                            "official_profile_url": "https://www.lgq.gov.cn/xxzx/lgyw/202502/t20250219_1200071.html"},
        },
        "current_status": {"current_post": "区委副书记、社会工作部部长", "current_org": "中国共产党龙港区委员会",
                           "administrative_rank": "县处级副职", "is_active": True,
                           "is_current_confirmed": True, "source_ids": ["S001"]},
        "career_timeline": [
            {"start": "unknown", "end": "<=2025", "org": "简历缺口", "title": "", "level": "县处级", "location": "葫芦岛市",
             "system": "other", "rank": "", "notes": "任区委副书记前履历公开渠道未检索到",
             "confidence": "unverified", "source_ids": []},
            {"start": "2025-02", "end": "present", "org": "中国共产党龙港区委员会", "title": "区委副书记、社会工作部部长",
             "level": "县处级", "location": "龙港区", "system": "party", "rank": "县处级副职",
             "notes": "2025-02-19 区委班子民主生活会出席（列位在区长曹亮之后）",
             "confidence": "confirmed", "source_ids": ["S001"]},
        ],
        "organizations": [
            {"name": "中国共产党龙港区委员会", "role": "区委副书记、社会工作部部长（现任）", "period": "2025 - 至今"},
        ],
        "relationships": [
            {"person": "袁伶", "person_id": "liaoning_huludao_yuanling", "relationship_type": "co_leadership",
             "strength": "medium", "evidence": "区委书记与区委副书记",
             "overlap_org": "中共龙港区委", "overlap_period": "2025-", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
            {"person": "曹亮", "person_id": "liaoning_huludao_caoliang", "relationship_type": "co_leadership",
             "strength": "medium", "evidence": "同为区委班子（区长与区委副书记）",
             "overlap_org": "中共龙港区委", "overlap_period": "2025-", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        ],
        "professional_profile": {"primary_specializations": [], "secondary_specializations": [],
            "career_pattern": "unknown", "systems_experience": ["party"], "geographic_pattern": [],
            "promotion_velocity": {"summary": "现任区委副书记、社会工作部部长", "notable_fast_promotions": []}},
        "work_style_and_personality": {"public_style_indicators": [], "speech_themes": [], "management_signals": [],
            "caveat": "Work style inferred from public records, not assessment."},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "截至 2026-08-06 未发现负面公开报道", "date": "", "confidence": "unverified", "source_ids": []}
        ],
        "source_register": [
            {"id": "S001", "title": "区委常委班子召开2024年度民主生活会", "url": "https://www.lgq.gov.cn/xxzx/lgyw/202502/t20250219_1200071.html",
             "publisher": "龙港区人民政府", "published_at": "2025-02-19", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "区委副书记、社会工作部部长逯化生出席"},
        ],
        "confidence_summary": {"identity": "unverified", "current_role": "confirmed", "career_completeness": "thin",
                               "relationship_confidence": "medium", "biggest_gap": "逯化生出生/籍贯/学历/此前职务与分工"},
        "open_questions": [
            {"priority": "high", "question": "逯化生具体出生/籍贯/学历/入党时间及任区委副书记前任职务（分工）", "why_it_matters": "判断其分工与晋升路径",
             "suggested_queries": ["逯化生 龙港区 委副书记"], "last_attempted": AS_OF},
            {"priority": "medium", "question": "区委副书记由刘剑交至逯化生的具体节点", "why_it_matters": "细化班子调整时间线", "suggested_queries": [], "last_attempted": AS_OF},
        ],
    }

    person_dir = _CURRENT_DIR
    today = AS_OF.replace("-", "")
    for fname, data in [
        (f"{today}-辽宁省-葫芦岛市-区委书记-袁伶.json", yuan),
        (f"{today}-辽宁省-葫芦岛市-区长-曹亮.json", cao),
        (f"{today}-辽宁省-葫芦岛市-区委副书记-逯化生.json", lu),
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


if __name__ == "__main__":
    main()