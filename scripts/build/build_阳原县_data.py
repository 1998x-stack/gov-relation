#!/usr/bin/env python3
"""
Build SQLite database and GEXF graph for 阳原县 leadership network.

Province: 河北省张家口市阳原县
Level: 县 (county)
Research date: 2026-08-05
Task: hebei_阳原县 (targets 县委书记 & 县长)

Environment / data-integrity note:
  External web-search engines (Exa/Baidu/Bing) were rate-limited or blocked in this
  environment. Per source_fallbacks.md, the investigation succeeded through DIRECT
  probing of the official county site (http://www.zjkyy.gov.cn/, confirmed working
  on HTTP) and the official 张家口新闻网 (www.zjknews.com).

Confirmed facts (confidence=confirmed, official source):
  - 阳原县 is a county-level division of 张家口市, 河北省.
  - Current 县委书记: 何景明. Confirmed via multiple official county articles:
      * 2026-04-30 京张体育文化旅游带建设领导小组会议 ("县委书记何景明指出")
      * 2026-06 基层办实事专题会 ("县委书记何景明主持会议")
      * 2026-04-21 联合办学签约仪式 ("县委书记何景明出席")
      * 2026-01 赴张家口 市政协 政银企座谈会 ("县委书记何景明在会上指出")
    He previously served as 县长 under predecessor 郝燕飞 (confirmed as "县长何景明"
    in 2024-12/2025-01 official articles) and was promoted to 县委书记 no later than
    Spring 2025 (first confirmed "县委书记何景明" 2025-04/05 and 2025-07-18 防汛调研).
  - Predecessor 县委书记: 郝燕飞 (confirmed "县委书记郝燕飞" in 2024-2025 official
    articles alongside "县长何景明").
  - 张家口市委书记: 赵文锋 (confirmed "市委书记赵文锋" in official county notice on
    学习教育工作, 2025).
  - 县委常委、常务副县长: 王建江 (confirmed 2024-12 / 2025-12 official 人大常委会
    reports and 县长何景明 安全生产 article).
  - 县人大常委会主任: 张建斌 (confirmed repeatedly chairing 人大常委会).
  - 副县长、公安局长: 郝文海 (official profile 2026-07-27: 男汉族1976年6月生,
    河北霸州人, 2004年8月入党, 大学学历, 1999年6月毕业于中国刑事警察学院).
  - 副县长: 唐玉德 (agriculture, confirmed 2025 农业数智化观摩报道), 孙志君
    (confirmed 2026-01-16 寒假校园安全部署会主持).
  - 河北阳原经济开发区 党工委副书记、管委会常务副主任: 谢海峰 (official 政府领导
    页面 2026-07-20).
  - 县委理论学习中心组在册成员(2025-12): 刘峰、郝崭文、杨婷婷 (分管论述发言).
  - 县检察院代理检察长: 董静; 县法院代理院长: 张黎蕾 (2025-03 人大五次会议).
  - 张家口市委书记: 赵文锋 confirmed.

Unverified (confidence=unverified, must be resolved):
  - Current 县长姓名. The official county news after 何景明's promotion to 书记
    consistently reports government activity under 何景明/常务副县 而不点名县长, and
    the 政府领导 channel (channel 21) currently lists only 郝海文/谢海峰. No
    accessible official notice names the current 县长. Recorded as 待查_县长 with a
    critical open_question. (Existing repo convention for unresolved identities.)

Cross-region / relationship evidence:
  - 中央和国家机关工委 (China NPC Party Org Work Committee, 中直机关工委) 定点帮扶
    阳原县 since 2015 (选派8名挂职干部、投入/引进帮扶资金16亿余元).
  - 左克平 (现 桥西区委书记), 籍贯 河北阳原 — a native-region connection between 阳原
    and 桥西区 leadership (from existing repo person JSON 20260724-…-左克平.json).

County profile (for governance context):
  - Area 1849 km²; 辖5镇9乡、301个行政村; 总人口27.45万; 平均值是深度贫困县
    (2012 国家贫困县, 2017 河北省十个深度贫困县之一); 中国毛皮碎料加工基地;
    泥河湾遗址 = "东方人类的故乡" (early-Pleistocene Paleolithic site cluster 举世).
"""

import json  # noqa: F401
import os
import sys
from pathlib import Path


def _find_repo_root(start: Path) -> Path:
    cur = start.resolve()
    for _ in range(6):
        if (cur / "gov_relation").is_dir():
            return cur
        nxt = cur.parent
        if nxt == cur:
            break
        cur = nxt
    raise RuntimeError(f"could not locate repo root from {start}")


_REPO_ROOT = _find_repo_root(Path(__file__).parent)
for _p in (_REPO_ROOT, os.path.join(_REPO_ROOT, "scripts")):
    if _p not in sys.path:
        sys.path.insert(0, str(_p))

import sqlite3  # noqa: E402

from gov_relation.runner import run_build  # noqa: E402

SLUG = "阳原县"
DB_PATH = Path(__file__).parent / f"{SLUG}_network.db"
GEXF_PATH = Path(__file__).parent / f"{SLUG}_network.gexf"
AS_OF = "2026-08-05"

# ────────────────────────────────────────────────────────────────────────────
# Persons
# ────────────────────────────────────────────────────────────────────────────
persons = [
    # ── 县委书记 (Party Secretary) — CONFIRMED ──
    {
        "id": 1,
        "name": "何景明",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共阳原县委员会",
        "source": "government-official yk.gov.cn; @www.zjkyy.gov.cn single pages 2025-2026 (confirmed)",
    },
    # ── 县委副书记、县长 — Identity not confirmed in accessible sources ──
    {
        "id": 2,
        "name": "待查_县长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "阳原县人民政府",
        "source": "current 县长 name not confirmed from accessible official sources; see report/open_gaps.md (unverified)",
    },
    # ── 前任县委书记 (Predecessor Party Secretary) — CONFIRMED name ──
    {
        "id": 3,
        "name": "郝燕飞",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任县委书记",
        "current_org": "中共阳原县委员会",
        "source": "government:gov yk.gov.cn single/22 (2024-2025) as 县委书记 (confirmed name, dates unconfirmed)",
    },
    # ── 县委常委、常务副县长 ── CONFIRMED name ──
    {
        "id": 4,
        "name": "王建江",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "阳原县人民政府",
        "source": "government:gov.cn 人大常委会会议 2025-12 / 何景明 安全生产 article 2025-01 (confirmed name)",
    },
    # ── 副县长（公安局长）── CONFIRMED (full profile) ──
    {
        "id": 5,
        "name": "郝文海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年6月",
        "birthplace": "河北霸州",
        "education": "大学（中国刑事警察学院）",
        "party_join": "2004年8月入党",
        "work_start": "1999年6月",
        "current_post": "副县长、公安局党委书记局长、督察长",
        "current_org": "阳原县人民政府 / 阳原县公安局",
        "source": "government:gov.cn single/21/89076.html 2026-07-27 (confirmed)",
    },
    # ── 县人大常委会主任 ── CONFIRMED name
    {
        "id": 6,
        "name": "张建斌",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "阳原县人民代表大会常务委员会",
        "source": "government:gov.cn 人大会议报道 2025-03 / 2025-12 (confirmed)",
    },
    # ── 副县长（教育）── CONFIRMED name
    {
        "id": 7,
        "name": "孙志君",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "阳原县人民政府",
        "source": "government:gov.cn single/22/89074.html 2026-01-20 (confirmed)",
    },
    # ── 副县长（农业）── CONFIRMED name
    {
        "id": 8,
        "name": "唐玉德",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "阳原县人民政府",
        "source": "government:gov.cn 2025 农业数智化观摩会 (confirmed)",
    },
    # ── 经开区常务副主任 ── CONFIRMED name
    {
        "id": 9,
        "name": "谢海峰",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "经开区管委会常务副主任",
        "current_org": "河北阳原经济开发区管委会",
        "source": "government:gov.cn single/21/92006.html 2026-07-20 (confirmed)",
    },
    # ── 县委领导（中心组学习成员）── CONFIRMED name
    {
        "id": 10,
        "name": "刘峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委理论学习中心组成员",
        "current_org": "中共阳原县委员会",
        "source": "government:gov.cn 理论学习中心组报道 2025-12 (confirmed name, role unverified)",
    },
    # ── 张家口市委书记（上级，context）── CONFIRMED name
    {
        "id": 11,
        "name": "赵文锋",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "张家口市委书记",
        "current_org": "中共张家口市委员会",
        "source": "government/official notice citing '市委书记赵文锋' (confirmed name)",
    },
]

# ────────────────────────────────────────────────────────────────────────────
# Organizations
# ────────────────────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共阳原县委员会", "type": "党委", "level": "县处级",
     "parent": "中共张家口市委员会", "location": "阳原县"},
    {"id": 2, "name": "阳原县人民政府", "type": "政府", "level": "县处级",
     "parent": "张家口市人民政府", "location": "阳原县"},
    {"id": 3, "name": "中共阳原县纪律检查委员会", "type": "纪律检查", "level": "县处级",
     "parent": "中共张家口市纪律检查委员会", "location": "阳原县"},
    {"id": 4, "name": "阳原县人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "", "location": "阳原县"},
    {"id": 5, "name": "阳原县人民检察院", "type": "司法", "level": "县处级",
     "parent": "张家口市人民检察院", "location": "阳原县"},
    {"id": 6, "name": "阳原县人民法院", "type": "司法", "level": "县处级",
     "parent": "张家口市中级人民法院", "location": "阳原县"},
    {"id": 7, "name": "河北阳原经济开发区管委会", "type": "开发区", "level": "县处级",
     "parent": "河北省人民政府", "location": "阳原县"},
    {"id": 8, "name": "阳原县公安局", "type": "政府", "level": "正科级",
     "parent": "阳原县人民政府", "location": "阳原县"},
    {"id": 9, "name": "中共张家口市委员会", "type": "党委", "level": "地厅级",
     "parent": "中共河北省委员会", "location": "张家口市"},
    {"id": 10, "name": "张家口市人民政府", "type": "政府", "level": "地厅级",
     "parent": "河北省人民政府", "location": "张家口市"},
    {"id": 11, "name": "中央和国家机关工委", "type": "党委（中央直属）", "level": "省部级",
     "parent": "中共中央", "location": "北京", "note": "定点帮扶阳原县（2015年起）"},
]

# ────────────────────────────────────────────────────────────────────────────
# Positions
# ────────────────────────────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "县委书记",
     "start_date": "2025-03", "end_date": "present", "rank": "县处级正职",
     "note": "由县长转任；2025年4月起确认以县委书记身份公开活动；2026年7月十三届县委连任。confidence: confirmed"},
    {"person_id": 1, "org_id": 2, "title": "县委副书记、县长",
     "start_date": "", "end_date": "2025-03", "rank": "县处级正职",
     "note": "前任县长（2024-12/2025-01 多篇官方报道）。转任县委书记后卸任。confidence: confirmed"},
    {"person_id": 2, "org_id": 2, "title": "县委副书记、县长",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": "姓名待确认（unverified）。现任县长，据 2026-07 十八届人大选举产生，须通过张家口市委组织部予以公示确认。"},
    {"person_id": 3, "org_id": 1, "title": "县委书记",
     "start_date": "", "end_date": "2025", "rank": "县处级正职",
     "note": "前任县委书记。2024-2025 期间以县委书记身份公开活动；如何景明接任。confidence: confirmed(name)"},
    {"person_id": 4, "org_id": 2, "title": "县委常委、常务副县长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "2024-2025 期间在人大常委会、安全生产工作中公开出现。confidence: confirmed(name)"},
    {"person_id": 5, "org_id": 2, "title": "副县长、县公安局长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "县公安局党委书记、局长、督察长，负责政法、信访等。confidence: confirmed"},
    {"person_id": 5, "org_id": 8, "title": "县公安局党委书记、局长",
     "start_date": "", "end_date": "present", "rank": "正科级",
     "note": "公安局长。confidence: confirmed"},
    {"person_id": 6, "org_id": 4, "title": "县人大常委会主任",
     "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": "2025-03 起主持县人大会议。confidence: confirmed"},
    {"person_id": 7, "org_id": 2, "title": "副县长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "负责教育体育等（2026-01 寒假校园安全部署会主持）。confidence: confirmed"},
    {"person_id": 8, "org_id": 2, "title": "副县长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "负责农业（2025 农业数智化观摩）。confidence: confirmed"},
    {"person_id": 9, "org_id": 7, "title": "经开区管委会常务副主任",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "河北阳原经济开发区 党工委副书记、管委会常务副主任。confidence: confirmed"},
    {"person_id": 10, "org_id": 1, "title": "县委理论学习中心组成员",
     "start_date": "", "end_date": "present", "rank": "县处级",
     "note": "2025-12 中心组学习会发言。confidence: unverified(role)"},
    {"person_id": 11, "org_id": 9, "title": "张家口市委书记",
     "start_date": "", "end_date": "present", "rank": "地厅级正职",
     "note": "上级市委主要领导（context）。confidence: confirmed"},
]

# ────────────────────────────────────────────────────────────────────────────
# Relationships
# ────────────────────────────────────────────────────────────────────────────
relationships = [
    {
        "person_a": 1, "person_b": 3,
        "type": "predecessor_successor",
        "context": "何景明接任郝燕飞任阳原县委书记",
        "overlap_org": "中共阳原县委", "overlap_period": "2025",
    },
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记与县长（党政正职搭配，职务结构上的双核心）",
        "overlap_org": "阳原县", "overlap_period": "",
    },
    {
        "person_a": 1, "person_b": 4,
        "type": "superior_subordinate",
        "context": "县委书记与常务副县长（何景明任县长期 王建江已任常务副县长）",
        "overlap_org": "阳原县人民政府", "overlap_period": "2024-2025",
    },
    {
        "person_a": 1, "person_b": 5,
        "type": "superior_subordinate",
        "context": "县委书记与副县长兼公安局长（政法系统直接领导关系）",
        "overlap_org": "阳原县人民政府", "overlap_period": "",
    },
    {
        "person_a": 4, "person_b": 2,
        "type": "superior_subordinate",
        "context": "常务副县长协助县长（县政府内部层级）",
        "overlap_org": "阳原县人民政府", "overlap_period": "",
    },
    {
        "person_a": 6, "person_b": 1,
        "type": "same_system",
        "context": "县人大常委会主任与县委书记（四大班子协调关系）",
        "overlap_org": "阳原县", "overlap_period": "",
    },
    {
        "person_a": 11, "person_b": 1,
        "type": "superior_subordinate",
        "context": "张家口市委书记与阳原县委书记（市委-县委领导关系）",
        "overlap_org": "张家口市", "overlap_period": "",
    },
    {
        "person_a": 9, "person_b": 1,
        "type": "same_org",
        "context": "经开区管委会与县委、县政府（园区经济治理协作）",
        "overlap_org": "河北阳原经开区", "overlap_period": "",
    },
]

if __name__ == "__main__":
    print(f"Building {SLUG} network...")
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
    print(f"Done. Wrote {DB_PATH.relative_to(Path.cwd())} and {GEXF_PATH.relative_to(Path.cwd())}")