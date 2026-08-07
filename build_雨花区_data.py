#!/usr/bin/env python3
"""Build script for 雨花区 (Yuhua District, Changsha, Hunan) leadership network.

Generated: 2026-08-06
Level: 市辖区
Province: 湖南省
Parent City: 长沙市
Targets: 区委书记 & 区长

Research Note:
  Current officeholders confirmed via the official district portal www.yuhua.gov.cn
  (领导之窗 + 政务要闻):
    - 区委书记: 蔡锋 (in office from ~2026-06, chairs 第七次党代会 2026-07-30)
    - 区长: 李磊 (男/汉/1981-05生/湖南浏阳人/2005-05入党/党校研究生+法学学士, confirmed official bio)
  Succession:
    区委书记: 张敏(~2020-21) → 刘素月(2021-~23) → 黄军其(~23-2026-05,一段一肩挑区长) → 蔡锋(2026-06-今)
    区长: 刘素月(2020) → 黄军其(代2021-08、区长2022-24) → 李磊(2024-今)
  Government roster (官方领导之窗): 刘振乾(常务副区长)、高蒙、邓波、肖向东、彭婷婷、龙峥嵘、陈功(公安局长)。

  Biographies that could NOT be confirmed (蔡锋 出生/籍贯/学历 and pre-2024 timelines)
  are flagged as gaps and recorded in report/open_gaps.md and person JSON open_questions.

Sources:
  - http://www.yuhua.gov.cn/ 领导之窗 (official leadership bios) & 政务要闻
"""

import sqlite3  # noqa: used by gov_relation.runner
import sys
from pathlib import Path

# Locate repo root so `gov_relation` is importable whether staged (data/tmp/<id>/)
# or promoted (scripts/build/).
_HERE = Path(__file__).resolve().parent
_found = False
for _up in range(0, 7):
    _cand = _HERE
    for _ in range(_up):
        _cand = _cand.parent
    if (_cand / "gov_relation" / "runner.py").exists():
        if str(_cand) not in sys.path:
            sys.path.insert(0, str(_cand))
        _found = True
        break

from gov_relation.paths import DATABASE_DIR, GRAPH_DIR  # noqa: E402
from gov_relation.runner import run_build  # noqa: E402

# ═══════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════

PERSONS = [
    # ── 现任区委书记 ──
    {
        "id": 1,
        "name": "蔡锋",
        "gender": "男(推测)",
        "ethnicity": "汉族(推测)",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共长沙市雨花区委书记",
        "current_org": "中共长沙市雨花区委员会",
        "source": "http://www.yuhua.gov.cn/zwgk97/jcxxgk/qtfdxx/gzdt59_1/zwdt/202607/t20260731_12514546.html (第七次党代会主持) ; GAP: 2026-06前履历身份未公开",
    },
    # ── 现任区长 ──
    {
        "id": 2,
        "name": "李磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年5月",
        "birthplace": "湖南浏阳",
        "education": "党校研究生学历，法学学士",
        "party_join": "2005年5月",
        "work_start": "未知",
        "current_post": "区委副书记、区人民政府党组书记、区长",
        "current_org": "长沙市雨花区人民政府",
        "source": "http://www.yuhua.gov.cn/zwgk97/jcxxgk/ldzc/ldxx77/202412/t20241227_11699389.html (官方领导信息)",
    },
    # ── 常务副区长 ──
    {
        "id": 3,
        "name": "刘振乾",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年7月",
        "birthplace": "湖南常德",
        "education": "研究生学历",
        "party_join": "2003年6月",
        "work_start": "2004年7月",
        "current_post": "区委常委、区人民政府党组副书记、常务副区长",
        "current_org": "长沙市雨花区人民政府",
        "source": "http://www.yuhua.gov.cn/zwgk97/jcxxgk/ldzc/ldxx77/202412/t20241227_11699505.html (官方领导信息)",
    },
    # ── 分管工信副区长 ──
    {
        "id": 4,
        "name": "高蒙",
        "gender": "男(推测)",
        "ethnicity": "汉族(推测)",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区人民政府党组成员、副区长",
        "current_org": "长沙市雨花区人民政府",
        "source": "http://www.yuhua.gov.cn/zwgk97/jcxxgk/ldzc/ldxx77/202507/t20250730_11934377.html (官方领导信息)",
    },
    # ── 副区长(农业农村) ──
    {
        "id": 5,
        "name": "邓波",
        "gender": "男(推测)",
        "ethnicity": "汉族(推测)",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人民政府党组成员、副区长",
        "current_org": "长沙市雨花区人民政府",
        "source": "http://www.yuhua.gov.cn/zwgk97/jcxxgk/ldzc/ldxx77/202110/t20211026_10296700.html (官方领导信息)",
    },
    # ── 副区长(城管) ──
    {
        "id": 6,
        "name": "肖向东",
        "gender": "男(推测)",
        "ethnicity": "汉族(推测)",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人民政府党组成员、副区长",
        "current_org": "长沙市雨花区人民政府",
        "source": "http://www.yuhua.gov.cn/zwgk97/jcxxgk/ldzc/ldxx77/202308/t20230822_11198332.html (官方领导信息)",
    },
    # ── 副区长(商务) ──
    {
        "id": 7,
        "name": "彭婷婷",
        "gender": "女(推测)",
        "ethnicity": "汉族(推测)",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "长沙市雨花区人民政府",
        "source": "http://www.yuhua.gov.cn/zwgk97/jcxxgk/ldzc/ldxx77/202405/t20240511_11439091.html (官方领导信息)",
    },
    # ── 副区长(教育卫健) ──
    {
        "id": 8,
        "name": "龙峥嵘",
        "gender": "男(推测)",
        "ethnicity": "汉族(推测)",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人民政府党组成员、副区长",
        "current_org": "长沙市雨花区人民政府",
        "source": "http://www.yuhua.gov.cn/zwgk97/jcxxgk/ldzc/ldxx77/202412/t20241227_11699408.html (官方领导信息)",
    },
    # ── 副区长/公安分局局长 ──
    {
        "id": 9,
        "name": "陈功",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年8月",
        "birthplace": "湖南茶陵",
        "education": "大学学历",
        "party_join": "2003年12月",
        "work_start": "2005年11月",
        "current_post": "区人民政府党组成员、副区长，区公安分局党委书记、局长",
        "current_org": "长沙市雨花区人民政府",
        "source": "http://www.yuhua.gov.cn/zwgk97/jcxxgk/ldzc/ldxx77/202507/t20250730_11934379.html (官方领导信息)",
    },
    # ── 前任区委书记/区长 ──
    {
        "id": 10,
        "name": "黄军其",
        "gender": "男(推测)",
        "ethnicity": "汉族(推测)",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "未知",
        "current_post": "前任雨花区委书记（2026-05卸任，去向待查）",
        "current_org": "(待查)",
        "source": "http://www.yuhua.gov.cn/ 政务要闻(2021代理区长、2022区长、2024书记兼区长、2026-05讲话)；GAP去向未公开",
    },
    # ── 更早前任书记 ──
    {
        "id": 11,
        "name": "刘素月",
        "gender": "女",
        "ethnicity": "汉族(推测)",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "未知",
        "current_post": "前任雨花区委书记/区长（去向待查）",
        "current_org": "待查",
        "source": "http://www.yuhua.gov.cn/ 政务要闻(2020区长、2021-2022区委书记报道)",
    },
]

ORGANIZATIONS = [
    {"id": 1, "name": "中共长沙市雨花区委员会", "type": "党委", "level": "正处级", "parent": "中共长沙市委", "location": "长沙市雨花区"},
    {"id": 2, "name": "长沙市雨花区人民政府", "type": "政府", "level": "正处级", "parent": "长沙市人民政府", "location": "长沙市雨花区"},
    {"id": 3, "name": "长沙市雨花区公安分局", "type": "政府", "level": "正科级", "parent": "长沙市公安局", "location": "长沙市雨花区"},
]

POSITIONS = [
    {"person_id": 1, "org_id": 1, "title": "雨花区委书记", "start_date": "2026-06", "end_date": "present", "rank": "正处级", "note": "2026-06-11首次讲话，2026-07-30当选第七届区委书记"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "present", "rank": "副厅级委员", "note": "区委副书记"},
    {"person_id": 2, "org_id": 2, "title": "区人民政府党组书记、区长", "start_date": "2024-12", "end_date": "present", "rank": "副厅长级(正处级区令)", "note": "official bio页面2024-12-27在任"},
    {"person_id": 3, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "official bio"},
    {"person_id": 3, "org_id": 2, "title": "区政府党组副书记、常务副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "official bio 1981-07生湖南常德"},
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "official bio"},
    {"person_id": 4, "org_id": 2, "title": "副区长(党组成员)", "start_date": "", "end_date": "present", "rank": "副处级", "note": "official bio"},
    {"person_id": 5, "org_id": 2, "title": "副区长(农业农村)", "start_date": "", "end_date": "present", "rank": "副处级", "note": "official bio"},
    {"person_id": 6, "org_id": 2, "title": "副区长(生态环境/城管)", "start_date": "", "end_date": "present", "rank": "副处级", "note": "official bio"},
    {"person_id": 7, "org_id": 2, "title": "副区长(商务/自贸)", "start_date": "", "end_date": "present", "rank": "副处级", "note": "official bio"},
    {"person_id": 8, "org_id": 2, "title": "副区长(教育/文旅/卫健)", "start_date": "", "end_date": "present", "rank": "副处级", "note": "official bio"},
    {"person_id": 9, "org_id": 2, "title": "副区长(公安/信访)", "start_date": "", "end_date": "present", "rank": "副处级", "note": "official bio"},
    {"person_id": 9, "org_id": 3, "title": "区公安分局党委书记、局长", "start_date": "", "end_date": "present", "rank": "正科级", "note": "official bio"},
    {"person_id": 10, "org_id": 2, "title": "区委副书记、区人民政府区长（曾任代理区长）", "start_date": "2021-08", "end_date": "~2024", "rank": "正处级", "note": "2021代理区长、2022区长"},
    {"person_id": 10, "org_id": 1, "title": "区委书记（兼区长时期）", "start_date": "~2023", "end_date": "2026-05", "rank": "正处级", "note": "2024-06报道为区委书记、区长一肩挑；2026-05末讲话"},
    {"person_id": 11, "org_id": 2, "title": "区长", "start_date": "2020", "end_date": "2021", "rank": "正处级", "note": "2020-06报道为区长"},
    {"person_id": 11, "org_id": 1, "title": "区委书记", "start_date": "2021", "end_date": "~2023", "rank": "正处级", "note": "2021-07、2022-05报道为区委书记"},
]

RELATIONSHIPS = [
    {"person_a": 1, "person_b": 2, "type": "党政正职搭档", "context": "区委书记蔡锋-区长李磊，现任搭档(2026-06起)", "overlap_org": "雨花区四套班子", "overlap_period": "2026-06-今"},
    {"person_a": 1, "person_b": 10, "type": "前后任同事", "context": "黄军其卸任区委书记(约2026-05)后蔡锋接任", "overlap_org": "中共雨花区委", "overlap_period": "2026-05至06"},
    {"person_a": 2, "person_b": 10, "type": "上下级/前后任", "context": "黄军其任区长时李磊接任；2025年多篇'受黄军其委托区长李磊主持区委常委会'", "overlap_org": "雨花区人民政府/区委", "overlap_period": "2024-2025"},
    {"person_a": 10, "person_b": 11, "type": "前继同事", "context": "刘素月任区委书记时黄军其任区长(2021-2023)", "overlap_org": "雨花区委区政府", "overlap_period": "2021-2023"},
    {"person_a": 2, "person_b": 3, "type": "政府班子同事", "context": "区长李磊与常务副区长刘振乾,现职政府班子成员", "overlap_org": "雨花区人民政府", "overlap_period": "2024-今"},
]

# fmt: on

# ═══════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════

STAGING_DIR = Path(__file__).resolve().parent
DB_PATH = STAGING_DIR / "雨花区_network.db"
GEXF_PATH = STAGING_DIR / "雨花区_network.gexf"

if __name__ == "__main__":
    run_build(
        slug="雨花区",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )