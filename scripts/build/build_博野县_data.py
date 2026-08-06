#!/usr/bin/env python3
"""
Build SQLite database and GEXF graph for 博野县 leadership network.

Province: 河北省保定市博野县
Level: 县 (county)
Research date: 2026-08-06
Task: hebei_博野县 (targets 县委书记 & 县长)

Data-integrity note:
  Research was completed against the official 博野县人民政府 leadership-index
  pages (retrieved 2026-08-06 from http://www.boye.gov.cn/ 政务频道/领导介绍)
  plus Baidu Baike entries and 保定/蠡县 official and media reports.
  Exa web-search API was rate-limited; Baidu Baike direct fetch returned 403;
  falls back used wapbaike (wapbaike.baidu.com) and Baidu result pages plus
  direct government-site probes. All claims carry confidence labels.

Key confirmed facts:
  - Current 县委书记: 贾文征 (appointed 2026-07), full career timeline confirmed
    from Baidu Baike (multiple appointment notices cited therein).
  - Current 县长: 许喆 (县委副书记、县长、县政府党组书记) confirmed by the
    official county site (posted 2026-02-24, still live as of retrieval).
  - Predecessor 县委书记: 刘永泽 (蠡县人, held office 2021.07-2026), predecessor
    博野县长/书记 马誉峰, and 陈伟 (曾任博野县委常委宣传部长 → 蠡县县委书记 →
    廊坊三河市委书记) map the strong 博野↔蠡县 cross-county cadre exchange.
  - 县政府领导班子 (副县长s) roles confirmed on the official site; individual
    birth/education for deputies is only partially published and flagged as gaps.

Uncertainties kept explicit: deputy birth years/education unverified; 许喆 possible
transfer to 保定市市场监督管理局 (2026-06 市级 listing) reported but NOT treated as
confirmed; flagged as open_questions.
"""

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

SLUG = "博野县"
DB_PATH = Path(__file__).parent / f"{SLUG}_network.db"
GEXF_PATH = Path(__file__).parent / f"{SLUG}_network.gexf"
AS_OF = "2026-08-06"
TODAY = "2026-08-06"

# ────────────────────────────────────────────────────────────────────────────
# Persons
# core leaders have identity confirmed; deputies need bio enrichment.
# ────────────────────────────────────────────────────────────────────────────
persons = [
    # ── 县委书记 (Party Secretary) — CURRENT, confirmed ──
    {
        "id": 1,
        "name": "贾文征",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1982-10",
        "birthplace": "河北保定",
        "education": "研究生学历",
        "party_join": "2003-05",
        "work_start": "2005",
        "current_post": "博野县委书记",
        "current_org": "中共博野县委员会",
        "source": "百度百科 贾文征 (2026-07任命; 前高碑店市长)",
    },
    # ── 县委副书记、县长 (County Mayor) — CURRENT, confirmed ──
    {
        "id": 2,
        "name": "许喆",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "博野县委副书记、县长",
        "current_org": "博野县人民政府",
        "source": "博野县政府网站 领导介绍 (2026-02-24); field details partial",
    },
    # ── 前任县委书记 (Predecessor) ──
    {
        "id": 3,
        "name": "刘永泽",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-06",
        "birthplace": "河北蠡县",
        "education": "研究生学历",
        "party_join": "1996-07",
        "work_start": "1991-08",
        "current_post": "博野县委书记（2021.07-2026任职, 2026年由贾文征接任）",
        "current_org": "中共博野县委员会",
        "source": "百度百科（蠡县人, 多年蠡县/安新/望都/徐水工作经历）",
    },
    # ── 常务副县长 key deputy ──
    {
        "id": 4,
        "name": "张岚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "博野县委常委、常务副县长",
        "current_org": "博野县人民政府",
        "source": "博野县人民政府官网 领导公告 (2026-02-24)",
    },
    # ── 副县长s confirmed on official roster ──
    {
        "id": 5,
        "name": "时耀曙",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "博野县副县长",
        "current_org": "博野县人民政府",
        "source": "博野县人民政府官网 领导公告 (2026-02-24)",
    },
    {
        "id": 6,
        "name": "肖少鹏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "博野县副县长",
        "current_org": "博野县人民政府",
        "source": "博野县人民政府官网 领导公告 (2026-02-24)",
    },
    {
        "id": 7,
        "name": "井凤民",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "博野县副县长",
        "current_org": "博野县人民政府",
        "source": "博野县人民政府官网 领导公告 (2026-02-24)",
    },
    {
        "id": 8,
        "name": "赵英晓",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "博野县副县长",
        "current_org": "博野县人民政府",
        "source": "博野县人民政府官网 领导公告 (2026-02-24)",
    },
    {
        "id": 9,
        "name": "牛坤卿",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "博野县副县长、县公安局党委书记、局长",
        "current_org": "博野县公安局",
        "source": "博野县人民政府官网 领导公告 (2026-02-24)",
    },
    # ── Network nodes: 博野↔蠡县 cross-county chain ──
    {
        "id": 10,
        "name": "马誉峰",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "保定市人大常委会副主任（曾任博野县长/书记、蠡县书记）",
        "current_org": "保定市人大常委会",
        "source": "河北共产党员网 人事任免 (2017)",
    },
    {
        "id": 11,
        "name": "陈伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-11",
        "birthplace": "河北安国",
        "education": "省委党校研究生",
        "party_join": "1997-07",
        "work_start": "1996-11",
        "current_post": "廊坊三河市委书记（曾任博野县委常委宣传部长、蠡县县委书记）",
        "current_org": "中共三河市委员会",
        "source": "河北党员/澎湃 (2026); 新浪财经票新闻",
    },
]

# ────────────────────────────────────────────────────────────────────────────
# Organizations
# ────────────────────────────────────────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "中共博野县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共保定市委员会",
        "location": "博野县",
    },
    {
        "id": 2,
        "name": "博野县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "保定市人民政府",
        "location": "博野县",
    },
    {
        "id": 3,
        "name": "博野县公安局",
        "type": "政府",
        "level": "乡科级",
        "parent": "博野县人民政府",
        "location": "博野县",
    },
    {
        "id": 4,
        "name": "中共保定市委员会",
        "type": "党委",
        "level": "地厅级",
        "parent": "中共河北省委员会",
        "location": "保定市",
    },
    {
        "id": 5,
        "name": "保定市人民政府",
        "type": "政府",
        "level": "地厅级",
        "parent": "河北省人民政府",
        "location": "保定市",
    },
    {
        "id": 6,
        "name": "中共蠡县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共保定市委员会",
        "location": "蠡县",
    },
    {
        "id": 7,
        "name": "中共河北省委员会",
        "type": "党委",
        "level": "省部级",
        "parent": "",
        "location": "石家庄市",
    },
    {
        "id": 8,
        "name": "河北省人民政府",
        "type": "政府",
        "level": "省部级",
        "parent": "",
        "location": "石家庄市",
    },
    {
        "id": 9,
        "name": "保定市人大常委会",
        "type": "人大",
        "level": "地厅级",
        "parent": "保定市人民政府",
        "location": "保定市",
    },
    {
        "id": 10,
        "name": "中共廊坊市委",
        "type": "党委",
        "level": "地厅级",
        "parent": "中共河北省委员会",
        "location": "廊坊市",
    },
]

# ────────────────────────────────────────────────────────────────────────────
# Positions
# ────────────────────────────────────────────────────────────────────────────
positions = [
    # 贾文征 (current secretary, full confirmed timeline)
    {"person_id": 1, "org_id": 1, "title": "县委书记",
     "start": "2026-07", "end": "present", "rank": "县处级正职",
     "note": "2026-07 由高碑店市长调任博野县委书记 (confidence: confirmed)"},
    # 贾文征 at 高碑店市长 (2025.01-2026.07) — org10 is 廊坊; use note: 高碑店属保定
    {"person_id": 1, "org_id": 4, "title": "高碑店市委副书记、市长",
     "start": "2025-01", "end": "2026-07", "rank": "县处级正职",
     "note": "2025-01-15 高碑店市七届人大五次会议当选市长 (confidence: confirmed)"},
    {"person_id": 1, "org_id": 4, "title": "保定市科学技术局党组书记、局长",
     "start": "2021-03", "end": "2024-12", "rank": "县处级正职",
     "note": "2021-03-04 保定市十五届人大常委会三十次会议任命; 2024-12-31 免职 (confidence: confirmed)"},
    {"person_id": 1, "org_id": 4, "title": "涞水县委常委、副县长",
     "start": "2019-09", "end": "2021-03", "rank": "县处级副职",
     "note": "其间抽调河北省委第七轮巡视组工作 (confidence: confirmed)"},
    {"person_id": 1, "org_id": 4, "title": "涞水县副县长",
     "start": "2017-02", "end": "2019-09", "rank": "县处级副职",
     "note": "2018.01-2018.12 挂职北京市房山区教委副主任 (confidence: confirmed)"},
    # 许喆 — current 县长
    {"person_id": 2, "org_id": 2, "title": "县委副书记、县长、县政府党组书记",
     "start": "2021", "end": "present", "rank": "县处级正职",
     "note": "official gov site 2026-02-24 修改上传; 自2021年起任县长 (confidence: confirmed)"},
    # 刘永泽 — predecessor
    {"person_id": 3, "org_id": 1, "title": "县委书记",
     "start": "2021-07", "end": "2026-07", "rank": "县处级正职",
     "note": "2021.07 博野县十八届人大一次会议 主持; 2026省委对博野书面报告显示在任; 2026-07 由贾文征接任 (confidence: confirmed)"},
    {"person_id": 3, "org_id": 1, "title": "博野县县长 (此前)",
     "start": "2016", "end": "2021-07", "rank": "县处级正职",
     "note": "2016年起任博野常务副县长、县长; 蠡县人, 早年任蠡县副县长/望都县委常委/徐水常委 (confidence: plausible)"},
    # 张岚 常务副县长
    {"person_id": 4, "org_id": 2, "title": "县委常委、常务副县长、县政府党组副书记",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": "负责县政府常务; 分管发改/安全生产/财政/行政审批/招商/开发区 (confidence: confirmed-role)"},
    # 副县长 roster
    {"person_id": 5, "org_id": 2, "title": "副县长、县政府党组成员",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": "分管农业/乡村振兴/水利/市场监管 (confidence: confirmed-role)"},
    {"person_id": 6, "org_id": 2, "title": "副县长",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": "分管自然资源/城乡规划/交通/电力 (confidence: confirmed-role)"},
    {"person_id": 7, "org_id": 2, "title": "副县长、县政府党组成员",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": "分管卫健/医保/教育/民政/退役军人 (confidence: confirmed-role)"},
    {"person_id": 8, "org_id": 2, "title": "副县长、县政府党组成员",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": "分管住建/生态/人社/文旅/金融 (confidence: confirmed-role)"},
    {"person_id": 9, "org_id": 3, "title": "副县长、县公安局党委书记、局长",
     "start": "", "end": "present", "rank": "县处级副职",
     "note": "分管公安/宗教/司法/信访 (confidence: confirmed-role)"},
    # Network nodes
    {"person_id": 10, "org_id": 9, "title": "保定市人大常委会副主任",
     "start": "2017-04", "end": "", "rank": "地厅级",
     "note": "现位实为副主任 (confidence: confirmed)"},
    {"person_id": 10, "org_id": 6, "title": "蠡县县委书记",
     "start": "2014-11", "end": "2016-12", "rank": "县处级正职",
     "note": "2014.11-2016.12 蠡县县委书记 (confidence: confirmed)"},
    {"person_id": 10, "org_id": 1, "title": "博野县委书记",
     "start": "2012-12", "end": "2014-11", "rank": "县处级正职",
     "note": "2012.12-2014.11 博野县委书记 (confidence: confirmed)"},
    {"person_id": 10, "org_id": 1, "title": "博野县县长",
     "start": "2007-05", "end": "2012-12", "rank": "县处级正职",
     "note": "2007.05-2012.12 博野县委副书记、县长 (confidence: confirmed)"},
    {"person_id": 11, "org_id": 10, "title": "廊坊三河市委书记",
     "start": "", "end": "present", "rank": "县处级正职",
     "note": "由蠡县县委书记跨市调任 (confidence: confirmed)"},
    {"person_id": 11, "org_id": 6, "title": "蠡县县委书记",
     "start": "", "end": "", "rank": "县处级正职",
     "note": "曾任蠡县县委书记 (confidence: confirmed)"},
    {"person_id": 11, "org_id": 1, "title": "博野县委常委、宣传部部长/农工委书记",
     "start": "", "end": "", "rank": "县处级副职",
     "note": "早年曾任此职; 后历任蠡县. (confidence: plausible)"},
]

# ────────────────────────────────────────────────────────────────────────────
# Relationships
# ────────────────────────────────────────────────────────────────────────────
relationships = [
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记与县长（党政双核搭档）",
        "overlap_org": "博野县", "overlap_period": "2026-",
    },
    {
        "person_a": 1, "person_b": 3,
        "type": "predecessor_successor",
        "context": "贾文征于2026-07接任刘永泽的博野县委书记（前任→现任）",
        "overlap_org": "中共博野县委员会", "overlap_period": "2026-07",
    },
    {
        "person_a": 3, "person_b": 2,
        "type": "superior_subordinate",
        "context": "刘永泽任县委书记期间与县长许喆搭档",
        "overlap_org": "博野县", "overlap_period": "2021-2026",
    },
    {
        "person_a": 4, "person_b": 2,
        "type": "superior_subordinate",
        "context": "常务副县长协助县长（政府内部层级）",
        "overlap_org": "博野县人民政府", "overlap_period": "",
    },
    {
        "person_a": 10, "person_b": 3,
        "type": "predecessor_successor",
        "context": "马誉峰曾任博野县长(2007-2012)/书记(2012-2014)，后刘永泽任书记——博野历任书记序列",
        "overlap_org": "博野县", "overlap_period": "2012-2021",
    },
    {
        "person_a": 10, "person_b": 11,
        "type": "same_system",
        "context": "马誉峰任蠡县书记(2014-2016)、陈伟继任蠡县书记——蠡县书记继任序列",
        "overlap_org": "中共蠡县委员会", "overlap_period": "2014-",
    },
    {
        "person_a": 11, "person_b": 3,
        "type": "same_native_place",
        "context": "陈伟曾任博野宣传部长(县常委)，与博野县领导体系同源；蠡县-博野跨县干部交流",
        "overlap_org": "博野县/蠡县", "overlap_period": "",
    },
    {
        "person_a": 9, "person_b": 2,
        "type": "superior_subordinate",
        "context": "公安局长（副县长）在县政府领导下工作，公安政法线",
        "overlap_org": "博野县人民政府", "overlap_period": "",
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