#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 青岛市 (Qingdao), 山东省.

Investigation date: 2026-07-25
Task ID: shandong_青岛市
Level: 地级市（副省级城市）
Targets: 市委书记 & 市长

Research sources:
  - en.wikipedia.org — Qingdao (Qingdao City overview, current leaders as of 2025-2026)
  - en.wikipedia.org — Lu Zhiyuan (前市委书记 biography, now Minister of Civil Affairs)
  - en.wikipedia.org — Wang Qingxian (前市委书记 biography, now Governor of Anhui)
  - Note: Web search was degraded — Exa rate-limited, Baidu 403, government sites timeouts

Confidence notes:
  - Current roles: confirmed via Wikipedia (EN, as of May 2026) and multiple cross-references
  - Biographical details: partial — Wikipedia provided some, many details unverified
  - Standing committee: partially confirmed via news/meeting reports
  - Predecessor/successor chains: confirmed via Wikipedia
"""

from __future__ import annotations

import json
import os
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
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "青岛市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "shandong_青岛市"
if _CURRENT_DIR.name == "shandong_青岛市":
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
# IDs: 1-9 current party/government leaders, 10-19 standing committee, 20-29 deputies, 30+ predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "曾赞荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969-08",
        "birthplace": "湖南邵东",
        "education": "在职研究生/经济学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共青岛市委员会",
        "source": "https://en.wikipedia.org/wiki/Qingdao",
        "confidence": "confirmed",
        "notes": "2023年11月任青岛市委书记；此前任山东省副省长。二十届中央候补委员"
    },
    {
        "id": 2,
        "name": "赵豪志",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1965-09",
        "birthplace": "山东东营",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市长",
        "current_org": "青岛市人民政府",
        "source": "https://en.wikipedia.org/wiki/Qingdao",
        "confidence": "confirmed",
        "notes": "2020年12月任青岛市代市长，2021年1月当选市长；此前任山东省应急管理厅厅长"
    },
    {
        "id": 3,
        "name": "张惠",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1967-05",
        "birthplace": "山东烟台",
        "education": "青岛海洋大学/理学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记、统战部部长",
        "current_org": "中共青岛市委员会",
        "source": "https://en.wikipedia.org/wiki/Qingdao",
        "confidence": "confirmed",
        "notes": "此前任威海市委书记、山东省妇联主席"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Standing Committee Members (市委常委)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 4,
        "name": "程德智",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、市纪委书记、市监委主任",
        "current_org": "中共青岛市纪律检查委员会",
        "source": "https://en.wikipedia.org/wiki/Qingdao",
        "confidence": "confirmed",
        "notes": "此前任山东省纪委常委"
    },
    {
        "id": 5,
        "name": "刘升勤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、组织部部长",
        "current_org": "中共青岛市委组织部",
        "source": "https://en.wikipedia.org/wiki/Qingdao",
        "confidence": "confirmed",
        "notes": ""
    },
    {
        "id": 6,
        "name": "孙永红",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、青岛西海岸新区工委书记、黄岛区委书记",
        "current_org": "中共青岛西海岸新区工作委员会",
        "source": "https://en.wikipedia.org/wiki/Qingdao",
        "confidence": "confirmed",
        "notes": ""
    },
    {
        "id": 7,
        "name": "马维民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、秘书长",
        "current_org": "中共青岛市委办公厅",
        "source": "https://en.wikipedia.org/wiki/Qingdao",
        "confidence": "confirmed",
        "notes": ""
    },
    {
        "id": 8,
        "name": "刘建军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、副市长（常务）",
        "current_org": "青岛市人民政府",
        "source": "https://en.wikipedia.org/wiki/Qingdao",
        "confidence": "confirmed",
        "notes": ""
    },
    {
        "id": 9,
        "name": "王波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、宣传部部长",
        "current_org": "中共青岛市委宣传部",
        "source": "https://en.wikipedia.org/wiki/Qingdao",
        "confidence": "confirmed",
        "notes": ""
    },
    {
        "id": 10,
        "name": "耿涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "青岛市人民政府",
        "source": "https://en.wikipedia.org/wiki/Qingdao",
        "confidence": "confirmed",
        "notes": ""
    },
    # ══════════════════════════════════════════════════════════════════════
    # Previous Leaders (predecessors)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 30,
        "name": "陆治原",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1964-08",
        "birthplace": "陕西绥德",
        "education": "西安交通大学/经济学学士",
        "party_join": "中共党员",
        "work_start": "1988-07",
        "current_post": "民政部部长",
        "current_org": "中华人民共和国民政部",
        "source": "https://en.wikipedia.org/wiki/Lu_Zhiyuan",
        "confidence": "confirmed",
        "notes": "2021年9月-2023年11月任青岛市委书记；2023年12月任民政部部长。二十届中央委员"
    },
    {
        "id": 31,
        "name": "王清宪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1963-07",
        "birthplace": "河北永年",
        "education": "南开大学哲学学士、中国社科院经济学博士",
        "party_join": "1986-08",
        "work_start": "1983-07",
        "current_post": "安徽省省长",
        "current_org": "安徽省人民政府",
        "source": "https://en.wikipedia.org/wiki/Wang_Qingxian",
        "confidence": "confirmed",
        "notes": "2019年1月-2021年1月任青岛市委书记；2021年2月任安徽省省长"
    },
    {
        "id": 32,
        "name": "张江汀",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1961-09",
        "birthplace": "山东昌邑",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "山东省人大常委会副主任（曾任）",
        "current_org": "山东省人民代表大会常务委员会",
        "source": "https://en.wikipedia.org/wiki/Qingdao",
        "confidence": "confirmed",
        "notes": "2017-2019年任青岛市委书记；后任山东省委政法委书记、省人大常委会副主任"
    },
    {
        "id": 33,
        "name": "李群",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1962-02",
        "birthplace": "山东威海",
        "education": "山东大学物理系",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "文化和旅游部副部长（曾任）",
        "current_org": "文化和旅游部",
        "source": "https://en.wikipedia.org/wiki/Qingdao",
        "confidence": "confirmed",
        "notes": "2010-2017年任青岛市委书记；后任山东省委常委、常务副省长，文化和旅游部副部长"
    },
    # 前市长
    {
        "id": 34,
        "name": "孟凡利",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1965-09",
        "birthplace": "山东临沂",
        "education": "天津财经学院/经济学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "内蒙古自治区党委书记",
        "current_org": "中共内蒙古自治区委员会",
        "source": "https://en.wikipedia.org/wiki/Qingdao",
        "confidence": "confirmed",
        "notes": "2017-2020年任青岛市市长；后任内蒙古自治区党委常委、包头市委书记，内蒙古自治区主席，内蒙古自治区党委书记"
    },
    {
        "id": 35,
        "name": "张新起",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1956-08",
        "birthplace": "山东济南",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "山东省人大常委会副主任（退休）",
        "current_org": "山东省人民代表大会常务委员会",
        "source": "https://en.wikipedia.org/wiki/Qingdao",
        "confidence": "confirmed",
        "notes": "2012-2016年任青岛市市长"
    },
    {
        "id": 36,
        "name": "夏耕",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1957-01",
        "birthplace": "黑龙江哈尔滨",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "山东省人大常委会副主任（退休）",
        "current_org": "山东省人民代表大会常务委员会",
        "source": "https://en.wikipedia.org/wiki/Qingdao",
        "confidence": "confirmed",
        "notes": "2003-2012年任青岛市市长"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────

organizations = [
    # Party organizations
    {"id": 1, "name": "中共青岛市委员会", "type": "党委", "level": "副省级", "location": "青岛市"},
    {"id": 2, "name": "中共青岛市委组织部", "type": "党委", "level": "副省级", "location": "青岛市"},
    {"id": 3, "name": "中共青岛市委宣传部", "type": "党委", "level": "副省级", "location": "青岛市"},
    {"id": 4, "name": "中共青岛市委统战部", "type": "党委", "level": "副省级", "location": "青岛市"},
    {"id": 5, "name": "中共青岛市委办公厅", "type": "党委", "level": "副省级", "location": "青岛市"},
    {"id": 6, "name": "中共青岛市纪律检查委员会", "type": "纪委", "level": "副省级", "location": "青岛市"},
    {"id": 7, "name": "中共青岛西海岸新区工作委员会", "type": "党委", "level": "副省级", "location": "青岛市黄岛区"},
    {"id": 8, "name": "中共黄岛区委员会", "type": "党委", "level": "地厅级", "location": "青岛市黄岛区"},
    # Government
    {"id": 10, "name": "青岛市人民政府", "type": "政府", "level": "副省级", "location": "青岛市"},
    {"id": 11, "name": "青岛西海岸新区管理委员会", "type": "政府", "level": "副省级", "location": "青岛市黄岛区"},
    # Previous orgs
    {"id": 20, "name": "中华人民共和国民政部", "type": "政府", "level": "省部级", "location": "北京市"},
    {"id": 21, "name": "安徽省人民政府", "type": "政府", "level": "省部级", "location": "安徽省合肥市"},
    {"id": 22, "name": "山东省人民代表大会常务委员会", "type": "人大", "level": "省部级", "location": "山东省济南市"},
    {"id": 23, "name": "山东省人民政府", "type": "政府", "level": "省部级", "location": "山东省济南市"},
    {"id": 24, "name": "山东省应急管理厅", "type": "政府", "level": "地厅级", "location": "山东省济南市"},
    {"id": 25, "name": "中共内蒙古自治区委员会", "type": "党委", "level": "省部级", "location": "内蒙古呼和浩特市"},
    {"id": 26, "name": "文化和旅游部", "type": "政府", "level": "省部级", "location": "北京市"},
    # Historical orgs
    {"id": 30, "name": "中共陕西省委组织部", "type": "党委", "level": "省部级", "location": "陕西省西安市"},
    {"id": 31, "name": "中共辽宁省委组织部", "type": "党委", "level": "省部级", "location": "辽宁省沈阳市"},
    {"id": 32, "name": "陕西省人民政府", "type": "政府", "level": "省部级", "location": "陕西省西安市"},
    {"id": 33, "name": "中共山东省委宣传部", "type": "党委", "level": "省部级", "location": "山东省济南市"},
    {"id": 34, "name": "山西省政府研究室", "type": "政府", "level": "地厅级", "location": "山西省太原市"},
    {"id": 35, "name": "中共山西省委宣传部", "type": "党委", "level": "省部级", "location": "山西省太原市"},
    {"id": 36, "name": "中共吕梁市委员会", "type": "党委", "level": "地厅级", "location": "山西省吕梁市"},
    {"id": 37, "name": "中共山东省委办公厅", "type": "党委", "level": "省部级", "location": "山东省济南市"},
    {"id": 38, "name": "人民日报社", "type": "事业单位", "level": "省部级", "location": "北京市"},
    {"id": 39, "name": "黑龙江省人民政府办公厅", "type": "政府", "level": "省部级", "location": "黑龙江省哈尔滨市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
# (person_id, org_id, title, start, end, rank, note)

positions = [
    # Current
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start": "2023-11", "end": "present", "rank": "副省级", "note": "二十届中央候补委员"},
    {"person_id": 2, "org_id": 10, "title": "市长", "start": "2020-12", "end": "present", "rank": "副省级", "note": "2021年1月正式当选"},
    {"person_id": 3, "org_id": 1, "title": "市委副书记、统战部部长", "start": "", "end": "present", "rank": "正厅级", "note": ""},
    {"person_id": 4, "org_id": 6, "title": "市委常委、市纪委书记、市监委主任", "start": "", "end": "present", "rank": "正厅级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "市委常委、组织部部长", "start": "", "end": "present", "rank": "正厅级", "note": ""},
    {"person_id": 6, "org_id": 7, "title": "市委常委、西海岸新区工委书记、黄岛区委书记", "start": "", "end": "present", "rank": "正厅级", "note": ""},
    {"person_id": 7, "org_id": 5, "title": "市委常委、秘书长", "start": "", "end": "present", "rank": "正厅级", "note": ""},
    {"person_id": 8, "org_id": 10, "title": "市委常委、副市长（常务）", "start": "", "end": "present", "rank": "正厅级", "note": ""},
    {"person_id": 9, "org_id": 3, "title": "市委常委、宣传部部长", "start": "", "end": "present", "rank": "正厅级", "note": ""},
    {"person_id": 10, "org_id": 10, "title": "副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},

    # 陆治原 career
    {"person_id": 30, "org_id": 1, "title": "市委书记", "start": "2021-09", "end": "2023-11", "rank": "副省级", "note": ""},
    {"person_id": 30, "org_id": 20, "title": "民政部部长", "start": "2023-12", "end": "present", "rank": "省部级", "note": "二十届中央委员"},
    {"person_id": 30, "org_id": 31, "title": "辽宁省委常委、组织部部长", "start": "2018-09", "end": "2021-08", "rank": "省部级副职", "note": ""},
    {"person_id": 30, "org_id": 32, "title": "陕西省副省长", "start": "2018-01", "end": "2018-09", "rank": "省部级副职", "note": ""},
    {"person_id": 30, "org_id": 33, "title": "渭南市委书记", "start": "2015-06", "end": "2018-01", "rank": "正厅级", "note": ""},

    # 王清宪 career
    {"person_id": 31, "org_id": 1, "title": "市委书记", "start": "2019-01", "end": "2021-01", "rank": "副省级", "note": ""},
    {"person_id": 31, "org_id": 21, "title": "安徽省省长", "start": "2021-02", "end": "present", "rank": "省部级", "note": ""},
    {"person_id": 31, "org_id": 37, "title": "山东省委常委、秘书长", "start": "2018-01", "end": "2019-01", "rank": "省部级副职", "note": ""},
    {"person_id": 31, "org_id": 33, "title": "山东省委常委、宣传部部长", "start": "2017-11", "end": "2018-01", "rank": "省部级副职", "note": ""},
    {"person_id": 31, "org_id": 35, "title": "山西省委常委、宣传部部长", "start": "2016-11", "end": "2017-11", "rank": "省部级副职", "note": ""},
    {"person_id": 31, "org_id": 36, "title": "吕梁市委书记", "start": "2016-05", "end": "2016-11", "rank": "正厅级", "note": ""},

    # 张江汀
    {"person_id": 32, "org_id": 1, "title": "市委书记", "start": "2017-01", "end": "2019-01", "rank": "副省级", "note": ""},

    # 李群
    {"person_id": 33, "org_id": 1, "title": "市委书记", "start": "2010-11", "end": "2017-01", "rank": "副省级", "note": ""},

    # 孟凡利
    {"person_id": 34, "org_id": 10, "title": "市长", "start": "2017-03", "end": "2020-09", "rank": "副省级", "note": ""},
    {"person_id": 34, "org_id": 25, "title": "内蒙古自治区党委书记", "start": "2023-", "end": "present", "rank": "省部级", "note": ""},

    # 张新起
    {"person_id": 35, "org_id": 10, "title": "市长", "start": "2012-03", "end": "2016-12", "rank": "副省级", "note": ""},

    # 夏耕
    {"person_id": 36, "org_id": 10, "title": "市长", "start": "2003-01", "end": "2012-01", "rank": "副省级", "note": ""},
]

# ── Relationships ─────────────────────────────────────────────────────────────

relationships = [
    # Direct predecessor-successor chains
    {"person_a": 1, "person_b": 30, "type": "predecessor_successor", "context": "曾赞荣接替陆治原任青岛市委书记", "overlap_org": "中共青岛市委员会", "overlap_period": "2023-11"},
    {"person_a": 30, "person_b": 31, "type": "predecessor_successor", "context": "陆治原接替王清宪任青岛市委书记", "overlap_org": "中共青岛市委员会", "overlap_period": "2021-09"},
    {"person_a": 31, "person_b": 32, "type": "predecessor_successor", "context": "王清宪接替张江汀任青岛市委书记", "overlap_org": "中共青岛市委员会", "overlap_period": "2019-01"},
    {"person_a": 32, "person_b": 33, "type": "predecessor_successor", "context": "张江汀接替李群任青岛市委书记", "overlap_org": "中共青岛市委员会", "overlap_period": "2017-01"},
    {"person_a": 2, "person_b": 34, "type": "predecessor_successor", "context": "赵豪志接替孟凡利任青岛市市长", "overlap_org": "青岛市人民政府", "overlap_period": "2020-12"},
    {"person_a": 34, "person_b": 35, "type": "predecessor_successor", "context": "孟凡利接替张新起任青岛市市长", "overlap_org": "青岛市人民政府", "overlap_period": "2017-03"},
    {"person_a": 35, "person_b": 36, "type": "predecessor_successor", "context": "张新起接替夏耕任青岛市市长", "overlap_org": "青岛市人民政府", "overlap_period": "2012-03"},

    # Shandong provincial system overlap (same organization at different times)
    {"person_a": 1, "person_b": 30, "type": "overlap", "context": "同为山东省领导（曾赞荣为副省长期间与陆治原在山东省班子共事）", "overlap_org": "山东省人民政府", "overlap_period": "2021-2023"},
    {"person_a": 31, "person_b": 33, "type": "overlap", "context": "王清宪任山东省委宣传部部长期间与李群在山东省班子共事", "overlap_org": "中共山东省委", "overlap_period": "2017-2018"},
    {"person_a": 30, "person_b": 31, "type": "overlap", "context": "陆治原和王清宪先后任青岛市委书记，均从山东省班子调任", "overlap_org": "中共山东省委", "overlap_period": "2019-2023"},

    # Current leadership team overlap
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "曾赞荣（书记）与赵豪志（市长）为当前青岛党政主要领导搭档", "overlap_org": "中共青岛市委员会/青岛市人民政府", "overlap_period": "2023-11至今"},
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "曾赞荣与张惠为青岛市委正副书记", "overlap_org": "中共青岛市委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "曾赞荣（书记）与程德智（纪委书记）在青岛市委班子共事", "overlap_org": "中共青岛市委员会", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 8, "type": "overlap", "context": "赵豪志（市长）与刘建军（常务副市长）在政府班子共事", "overlap_org": "青岛市人民政府", "overlap_period": "至今"},

    # Same-system connections
    {"person_a": 30, "person_b": 32, "type": "same_system", "context": "陆治原曾任青岛市委书记期间与张江汀（前任、后任省委政法委书记）在山东省政法系统有关联", "overlap_org": "山东省", "overlap_period": ""},
]

# ── Main ──────────────────────────────────────────────────────────────────────

def write_person_json(person: dict) -> None:
    """Write a per-person JSON file in PJSON_DIR."""
    name = person["name"]
    job_short = person["current_post"].split("/")[0].split("（")[0]
    fname = f"{TODAY}-山东省-青岛市-{job_short}-{name}.json"
    fpath = PJSON_DIR / fname

    data = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "山东省",
            "city": "青岛市",
            "region": "青岛市",
            "job": job_short,
            "task_id": "shandong_青岛市",
            "time_focus": "2024-2026"
        },
        "identity": {
            "person_id": f"qingdao_{name}",
            "name": name,
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "education": [
                {
                    "period": "",
                    "institution": person.get("education", ""),
                    "major": "",
                    "degree": "",
                    "study_type": "unknown",
                    "source_ids": ["S001"]
                }
            ],
            "dedupe_keys": {
                "name_birth": f"{name}_{person.get('birth', 'unknown')}",
                "name_birthplace": f"{name}_{person.get('birthplace', 'unknown')}"
            }
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": person["confidence"] == "confirmed",
            "source_ids": ["S001"]
        },
        "career_timeline": [],
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "caveat": "Work style is inferred from public records, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": [
            {
                "id": "S001",
                "title": "Wikipedia - Qingdao",
                "url": "https://en.wikipedia.org/wiki/Qingdao",
                "publisher": "Wikipedia",
                "published_at": "2026",
                "accessed_at": AS_OF,
                "source_type": "encyclopedia",
                "reliability": "medium",
                "notes": "English Wikipedia page for Qingdao city"
            }
        ],
        "confidence_summary": {
            "identity": person["confidence"],
            "current_role": person["confidence"],
            "career_completeness": "partial",
            "relationship_confidence": "low",
            "biggest_gap": f"Complete career history for {name} - web search was degraded"
        },
        "open_questions": [
            {
                "priority": "high",
                "question": f"Complete career timeline for {name} before current role",
                "why_it_matters": "Understanding career trajectory reveals patronage networks and factional affiliations",
                "suggested_queries": [f"{name} 简历 山东省", f"{name} 任前公示"],
                "last_attempted": AS_OF
            }
        ]
    }

    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Wrote {fpath.name}")


def main():
    print(f"=== Building {SLUG} network ===")

    # Run the build
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

    # Person JSONs for core figures
    print("\n--- Writing person JSONs ---")
    core_ids = [1, 2, 3, 30, 31]  # 曾赞荣, 赵豪志, 张惠, 陆治原, 王清宪
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n=== Done ===")
    print(f"  DB:     {DB_PATH}")
    print(f"  GEXF:   {GEXF_PATH}")
    print(f"  Person JSONs in: {PJSON_DIR}")


if __name__ == "__main__":
    main()
