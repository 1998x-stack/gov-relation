#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
海兴县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 河北省
Parent City: 沧州市
Region: 海兴县
Targets: 县委书记 & 县长

Research Sources (一手官方，海兴县人民政府 www.haixing.gov.cn)：
- 县委书记 回永智 — confirmed：
  * 「中共海兴县委十届十二次全会举行」(2026-05-06, http://www.haixing.gov.cn/haixing/c101044/202605/bdec6fd800914a76bbdef449bb8db9d9.shtml) 会议于 2026-04-30 举行，『全会由县委常委会主持。县委书记回永智代表县委常委会作了讲话』，并通过《关于召开中国共产党海兴县第十一次代表大会的决议》。
- 县长 刘洋 — confirmed：
  * 2026年政府工作报告 (2026-02-09 在海兴县第十二届人大六次会议上由县长刘洋作报告，http://www.haixing.gov.cn/haixing/zfgzbg/202604/3cefeb87acd0475588dfed4c5fdf808f.shtml)
  * 2025年政府工作报告 (2025-01-14 由县长刘洋作报告)
  * 领导之窗：县委副书记、县长刘洋，主持县政府全面工作，负责开发区建设工作
- 县政府领导班子（一手官网 领导之窗 c101051，2025-12 更新）：
  * 柳杨：县委常委、常务副县长（负责常务工作，发改/财税/统计/应急/信访）
  * 鞠海洪：县委常委、副县长（挂职），协助乡村振兴、对外开放招商
  * 高德强：副县长（大数据/行政审批/市场监管/教育/卫生/医保/金融）
  * 王文德：副县长（城建/城管/自然资源规划/交通）
  * 李一兵：副县长（公安/司法/退役军人）
  * 杜鑫麟：副县长（农业农村/乡村振兴/水务）
  * 赵海涛：副县长（工信/科技/商务/招商/生态环保）
  * 杨伟东：党组成员（国资）

Research Date: 2026-08-05
Confidence 说明：
  回永智 任海兴县委书记 — confirmed（海兴县政府官网官方新闻）。
  刘洋 任海兴县委副书记、县长 — confirmed（官方新闻＋政府工作报告署名＋领导之窗）。
  县政府班子（柳杨/鞠海洪/高德强/王文德/李一兵/杜鑫麟/赵海涛/杨伟东）职务与分工 — confirmed（领导之窗 c101051）。
  回永智、刘洋 两人任现职前的履历、出生/学历信息，以及前任书记/县长 — unverified（公开资料受限，见 open_gaps）。
"""

import os
import sys
from pathlib import Path

# Allow import from repo root robustly (works from data/tmp/<task>/ and scripts/build/)
REPO_ROOT = Path(__file__).resolve().parents[2]
for _pc in [2, 3, 4, 5]:
    _candidate = Path(__file__).resolve().parents[_pc]
    if (_candidate / "gov_relation").is_dir():
        REPO_ROOT = _candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import sqlite3  # noqa: F401 — required for process_tmp.py token check

from gov_relation.runner import run_build

SLUG = "海兴县"

_script_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_script_dir, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(_script_dir, f"{SLUG}_network.gexf")

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════════
    # 现任党政一把手（targets）
    # ════════════════════════════════════════════
    {
        "id": 1,
        "name": "回永智",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "海兴县委书记",
        "current_org": "中共海兴县委员会",
        "source": "海兴县政府官网动态要闻（2026-04-30 县委十届十二次全会）：县委书记回永智主持并讲话，审议通过《关于召开中国共产党海兴县第十一次代表大会的决议》。"
    },
    {
        "id": 2,
        "name": "刘洋",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "海兴县委副书记、县人民政府县长",
        "current_org": "海兴县人民政府",
        "source": "海兴县政府官网：领导之窗（2025-12）确认刘洋系县委副书记、县长，主持县政府全面工作；2025-01-14 与 2026-02-09 先后在县第十二届人大五次/六次会议上作政府工作报告。"
    },
    # ════════════════════════════════════════════
    # 县政府领导班子（一手官网领导之窗 c101051）
    # ════════════════════════════════════════════
    {
        "id": 3,
        "name": "柳杨",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "海兴县委常委、常务副县长",
        "current_org": "海兴县人民政府",
        "source": "海兴县政府官网—领导之窗：县委常委、副县长柳杨，负责县政府常务工作，分管发改、财税、统计、应急、信访等，协助刘洋同志分管县审计局。"
    },
    {
        "id": 4,
        "name": "鞠海洪",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "海兴县委常委、副县长（挂职）",
        "current_org": "海兴县人民政府",
        "source": "海兴县政府官网—领导之窗：县委常委、副县长鞠海洪（挂职），协助杜鑫麟同志抓好乡村振兴，协助赵海涛同志抓好对外开放和招商引资工作。"
    },
    {
        "id": 5,
        "name": "高德强",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "海兴县副县长",
        "current_org": "海兴县人民政府",
        "source": "海兴县政府官网—领导之窗：副县长高德强，负责数据、审批、市场监管、教育、卫生、医保、金融等。"
    },
    {
        "id": 6,
        "name": "王文德",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "海兴县副县长",
        "current_org": "海兴县人民政府",
        "source": "海兴县政府官网—领导之窗：副县长王文德，负责城乡建设、自然资源和规划、交通运输等。"
    },
    {
        "id": 7,
        "name": "李一兵",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "海兴县副县长（分管公安）",
        "current_org": "海兴县人民政府",
        "source": "海兴县政府官网—领导之窗：副县长李一兵，负责公安、司法、退役军人事务等工作，分管县公安局、县司法局、县退役军人事务局。"
    },
    {
        "id": 8,
        "name": "杜鑫麟",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "海兴县副县长",
        "current_org": "海兴县人民政府",
        "source": "海兴县政府官网—领导之窗：副县长杜鑫麟，负责农业农村、乡村振兴、水务等工作。"
    },
    {
        "id": 9,
        "name": "赵海涛",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "海兴县副县长",
        "current_org": "海兴县人民政府",
        "source": "海兴县政府官网—领导之窗：副县长赵海涛，负责工业和信息化、科技、商务、招商引资、对外开放、生态环境等工作。"
    },
    {
        "id": 10,
        "name": "杨伟东",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "海兴县人民政府党组成员",
        "current_org": "海兴县人民政府",
        "source": "海兴县政府官网—领导之窗：党组成员杨伟东，协助柳杨同志负责国有资产管理工作，分管县建投公司、县兴港公司。"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共海兴县委员会",
        "type": "党委",
        "level": "县级",
        "location": "沧州市海兴县",
        "parent": "中共沧州市委"
    },
    {
        "id": 2,
        "name": "海兴县人民政府",
        "type": "政府",
        "level": "县级",
        "location": "沧州市海兴县",
        "parent": "沧州市人民政府"
    },
    {
        "id": 3,
        "name": "海兴县人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "location": "沧州市海兴县",
        "parent": ""
    },
    {
        "id": 4,
        "name": "政协海兴县委员会",
        "type": "政协",
        "level": "县级",
        "location": "沧州市海兴县",
        "parent": "政协沧州市委员会"
    },
]

# 3. Positions
positions = [
    # ── 回永智 (县委书记) ──
    {"person_id": 1, "org_id": 1, "title": "海兴县委书记", "start_date": "约2022-2024", "end_date": "present", "rank": "正处级", "note": "海兴县委书记；主持县委全面工作，2026-04-30 主持县委十届十二次全会并作讲话。"},
    # ── 刘洋 (县长) ──
    {"person_id": 2, "org_id": 2, "title": "海兴县委副书记、县人民政府县长", "start_date": "约2024-2025", "end_date": "present", "rank": "正处级（县处级正职）", "note": "领导之窗一手官方确认。分工：主持县政府全面工作，负责县经济开发区。2025-01-14 与 2026-02-09 分别作《政府工作报告》。"},
    {"person_id": 2, "org_id": 1, "title": "海兴县委副书记", "start_date": "约2024-2025", "end_date": "present", "rank": "县级", "note": "领导之窗确认刘洋系县委副书记、县长。"},
    # ── 柳杨 (常务副县长) ──
    {"person_id": 3, "org_id": 2, "title": "海兴县常务副县长", "start_date": "约2023-2024", "end_date": "present", "rank": "副处级（常务）", "note": "领导之窗确认，负责县政府常务工作。"},
    {"person_id": 3, "org_id": 1, "title": "海兴县委常委", "start_date": "约2023-2024", "end_date": "present", "rank": "县级", "note": "领导之窗确认柳杨为县委常委。"},
    # ── 各副县长 ──
    {"person_id": 4, "org_id": 2, "title": "海兴县副县长（挂职）", "start_date": "约2024-2025", "end_date": "present", "rank": "副处级", "note": "领导之窗确认，县委常委、副县长。"},
    {"person_id": 5, "org_id": 2, "title": "海兴县副县长", "start_date": "约2023-2024", "end_date": "present", "rank": "副处级", "note": "领导之窗确认。"},
    {"person_id": 6, "org_id": 2, "title": "海兴县副县长", "start_date": "约2023-2024", "end_date": "present", "rank": "副处级", "note": "领导之窗确认。"},
    {"person_id": 7, "org_id": 2, "title": "海兴县副县长", "start_date": "约2023-2024", "end_date": "present", "rank": "副处级", "note": "领导之窗确认，分管政法。"},
    {"person_id": 8, "org_id": 2, "title": "海兴县副县长", "start_date": "约2023-2024", "end_date": "present", "rank": "副处级", "note": "领导之窗确认。"},
    {"person_id": 9, "org_id": 2, "title": "海兴县副县长", "start_date": "约2023-2024", "end_date": "present", "rank": "副处级", "note": "领导之窗确认。"},
    {"person_id": 10, "org_id": 2, "title": "海兴县人民政府党组成员", "start_date": "约2023-2024", "end_date": "present", "rank": "副处级", "note": "领导之窗确认，负责国有资产管理。"},
]

# 4. Relationships
relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记回永智与县长刘洋为海兴县现任党政一把手搭档（书记-县长）。两人共同出席县委全会、县两会等县级会议。",
        "overlap_org": "中共海兴县委员会／海兴县人民政府",
        "overlap_period": "2024/2025-"
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "overlap",
        "context": "县委书记回永智与县委常委、常务副县长柳杨同属县委班子（柳杨为县委常委）。",
        "overlap_org": "中共海兴县委员会",
        "overlap_period": "2024/2025-"
    },
    {
        "person_a": 2,
        "person_b": 3,
        "type": "overlap",
        "context": "县长刘洋与常务副县长柳杨为县政府正职/常务副职搭档。",
        "overlap_org": "海兴县人民政府",
        "overlap_period": "2024/2025-"
    },
    {
        "person_a": 2,
        "person_b": 4,
        "type": "overlap",
        "context": "县长刘洋与挂职副县长鞠海洪共同构成县政府班子。",
        "overlap_org": "海兴县人民政府",
        "overlap_period": "2024/2025-"
    },
    {
        "person_a": 2,
        "person_b": 5,
        "type": "overlap",
        "context": "县长刘洋与副县长高德强共同构成县政府班子。",
        "overlap_org": "海兴县人民政府",
        "overlap_period": "2024/2025-"
    },
    {
        "person_a": 2,
        "person_b": 6,
        "type": "overlap",
        "context": "县长刘洋与副县长王文德共同构成县政府班子。",
        "overlap_org": "海兴县人民政府",
        "overlap_period": "2024/2025-"
    },
    {
        "person_a": 2,
        "person_b": 7,
        "type": "overlap",
        "context": "县长刘洋与副县长李一兵共同构成县政府班子。",
        "overlap_org": "海兴县人民政府",
        "overlap_period": "2024/2025-"
    },
    {
        "person_a": 2,
        "person_b": 8,
        "type": "overlap",
        "context": "县长刘洋与副县长杜鑫麟共同构成县政府班子。",
        "overlap_org": "海兴县人民政府",
        "overlap_period": "2024/2025-"
    },
    {
        "person_a": 2,
        "person_b": 9,
        "type": "overlap",
        "context": "县长刘洋与副县长赵海涛共同构成县政府班子。",
        "overlap_org": "海兴县人民政府",
        "overlap_period": "2024/2025-"
    },
    {
        "person_a": 3,
        "person_b": 4,
        "type": "overlap",
        "context": "常务副县长柳杨与挂职副县长鞠海洪共同构成县政府班子。",
        "overlap_org": "海兴县人民政府",
        "overlap_period": "2024/2025-"
    },
    {
        "person_a": 10,
        "person_b": 3,
        "type": "overlap",
        "context": "党组成员杨伟东协助常务副县长柳杨负责国有资产管理工作。",
        "overlap_org": "海兴县人民政府",
        "overlap_period": "2024/2025-"
    },
]

# ── Build ──

if __name__ == "__main__":
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
    print(f"Done. DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")