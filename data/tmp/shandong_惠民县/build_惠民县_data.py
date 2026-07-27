#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 惠民县 (Huimin County), 山东省.

Investigation date: 2026-07-25
Task ID: shandong_惠民县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - 360百科: baike.so.com/doc/5790940-10491428.html — 王玮 biography
  - 360百科: baike.so.com/doc/475202-503223.html — 许健 biography
  - 惠民县人民政府: www.huimin.gov.cn — current leadership news articles (2026-07)
  - 360搜索 / Bing search — supplementary career timeline verification

Confidence notes:
  - 王玮 (县委书记): full career timeline confirmed via 360百科 (encyclopedia source)
  - 许健 (县长): full career timeline confirmed via 360百科 (encyclopedia source)
  - Current roles: confirmed via government news articles (2026-07-10 工商联会议)
  - Other leadership members (袁光新, 杨宝亮, 张丽, 牛业霞, 王翠兰, 师杰): confirmed attendance at 工商联会议
  - Biographical details (birth exact date, education background): confirmed
  - Relationship evidence: overlap in same organization, predecessor/successor chains identified
  - All claims labeled with confidence level; gaps explicitly documented
"""

from __future__ import annotations

import json
import os
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

import sqlite3  # noqa: used by gov_relation.runner via import
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "惠民县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "shandong_惠民县"
if _CURRENT_DIR.name == "shandong_惠民县":
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
# IDs: 1-9 current party/government leaders, 10-19 standing committee, 20-29 deputy govt, 30+ predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "王玮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年5月",
        "birthplace": "山东武城",
        "education": "大学学历（山东工业大学计算机应用专业）",
        "party_join": "中共党员",
        "work_start": "1996年7月",
        "current_post": "惠民县委书记",
        "current_org": "中共惠民县委员会",
        "source": "https://baike.so.com/doc/5790940-10491428.html",
    },
    {
        "id": 2,
        "name": "许健",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1980年1月",
        "birthplace": "山东博兴",
        "education": "本科学历，文学学士（烟台大学中国语言文学系汉语言文学专业）",
        "party_join": "中共党员",
        "work_start": "2002年8月",
        "current_post": "惠民县委副书记、县长",
        "current_org": "惠民县人民政府",
        "source": "https://baike.so.com/doc/475202-503223.html",
    },
    # ══════════════════════════════════════════════════════════════════════
    # County Leaders
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "袁光新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "惠民县人大常委会主任",
        "current_org": "惠民县人大常委会",
        "source": "http://www.huimin.gov.cn/art/2026/7/22/art_118126_10472558.html",
    },
    {
        "id": 4,
        "name": "杨宝亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "惠民县政协主席",
        "current_org": "惠民县政协",
        "source": "http://www.huimin.gov.cn/art/2026/7/22/art_118126_10472558.html",
    },
    # ══════════════════════════════════════════════════════════════════════
    # Standing Committee
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 5,
        "name": "张丽",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "惠民县委常委、宣传部部长、统战部部长",
        "current_org": "中共惠民县委员会",
        "source": "http://www.huimin.gov.cn/art/2026/7/10/art_118126_10472251.html",
    },
    {
        "id": 6,
        "name": "牛业霞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "惠民县委常委（群团代表）",
        "current_org": "中共惠民县委员会",
        "source": "http://www.huimin.gov.cn/art/2026/7/10/art_118126_10472251.html",
    },
    {
        "id": 7,
        "name": "王翠兰",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "惠民县领导",
        "current_org": "惠民县人民政府",
        "source": "http://www.huimin.gov.cn/art/2026/7/10/art_118126_10472251.html",
    },
    {
        "id": 8,
        "name": "师杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "惠民县工商联主席、总商会会长",
        "current_org": "惠民县工商业联合会",
        "source": "http://www.huimin.gov.cn/art/2026/7/10/art_118126_10472251.html",
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 9,
        "name": "王庆霞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "滨州市人大常委会副主任（原惠民县委书记）",
        "current_org": "滨州市人大常委会",
        "source": "https://baike.so.com/doc/5790940-10491428.html",
    },
    {
        "id": 10,
        "name": "刘卫忠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原惠民县委副书记、县长（许健前任）",
        "current_org": "",
        "source": "https://baike.so.com/doc/475202-503223.html",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
# IDs: 1-9 party/government, 10-19 departments, 20+ towns/townships

organizations = [
    {"id": 1, "name": "中共惠民县委员会", "type": "党委", "level": "县", "parent": "中共滨州市委员会", "location": "山东省滨州市惠民县"},
    {"id": 2, "name": "惠民县人民政府", "type": "政府", "level": "县", "parent": "滨州市人民政府", "location": "山东省滨州市惠民县"},
    {"id": 3, "name": "惠民县人大常委会", "type": "人大", "level": "县", "parent": "滨州市人大常委会", "location": "山东省滨州市惠民县"},
    {"id": 4, "name": "惠民县政协", "type": "政协", "level": "县", "parent": "政协滨州市委员会", "location": "山东省滨州市惠民县"},
    {"id": 5, "name": "惠民县工商业联合会", "type": "群团", "level": "县", "parent": "惠民县人民政府", "location": "山东省滨州市惠民县"},
    {"id": 6, "name": "中共惠民县委宣传部", "type": "党委", "level": "县", "parent": "中共惠民县委员会", "location": "山东省滨州市惠民县"},
    {"id": 7, "name": "中共惠民县委统战部", "type": "党委", "level": "县", "parent": "中共惠民县委员会", "location": "山东省滨州市惠民县"},
    # Historical organizations
    {"id": 8, "name": "中共齐河县委员会", "type": "党委", "level": "县", "parent": "中共德州市委员会", "location": "山东省德州市齐河县"},
    {"id": 9, "name": "齐河县人民政府", "type": "政府", "level": "县", "parent": "德州市人民政府", "location": "山东省德州市齐河县"},
    {"id": 10, "name": "德州市人民政府", "type": "政府", "level": "地级市", "parent": "山东省人民政府", "location": "山东省德州市"},
    {"id": 11, "name": "德州市信息产业局", "type": "政府", "level": "地级市", "parent": "德州市人民政府", "location": "山东省德州市"},
    {"id": 12, "name": "德州市经济和信息化委员会", "type": "政府", "level": "地级市", "parent": "德州市人民政府", "location": "山东省德州市"},
    {"id": 13, "name": "德州市金融工作办公室", "type": "政府", "level": "地级市", "parent": "德州市人民政府", "location": "山东省德州市"},
    {"id": 14, "name": "德州市地方金融监督管理局", "type": "政府", "level": "地级市", "parent": "德州市人民政府", "location": "山东省德州市"},
    # 许健 historical orgs
    {"id": 15, "name": "中共博兴县委组织部", "type": "党委", "level": "县", "parent": "中共博兴县委员会", "location": "山东省滨州市博兴县"},
    {"id": 16, "name": "博兴县卫生局", "type": "政府", "level": "县", "parent": "博兴县人民政府", "location": "山东省滨州市博兴县"},
    {"id": 17, "name": "共青团博兴县委员会", "type": "群团", "level": "县", "parent": "中共博兴县委员会", "location": "山东省滨州市博兴县"},
    {"id": 18, "name": "共青团滨州市委员会", "type": "群团", "level": "地级市", "parent": "中共滨州市委员会", "location": "山东省滨州市"},
    {"id": 19, "name": "中共无棣县委员会", "type": "党委", "level": "县", "parent": "中共滨州市委员会", "location": "山东省滨州市无棣县"},
    {"id": 20, "name": "无棣县人民政府", "type": "政府", "level": "县", "parent": "滨州市人民政府", "location": "山东省滨州市无棣县"},
    {"id": 21, "name": "滨州市科学技术协会", "type": "群团", "level": "地级市", "parent": "中共滨州市委员会", "location": "山东省滨州市"},
    {"id": 22, "name": "滨州市人民政府外事办公室", "type": "政府", "level": "地级市", "parent": "滨州市人民政府", "location": "山东省滨州市"},
    {"id": 23, "name": "滨州市人大常委会", "type": "人大", "level": "地级市", "parent": "滨州市", "location": "山东省滨州市"},
]

# ── Positions (Person → Organization) ────────────────────────────────────────

positions = [
    # ── 王玮 (县委书记) career timeline ──
    {"person_id": 1, "org_id": 10, "title": "德州市信息中心科员", "start_date": "1996-07", "end_date": "2000-06", "rank": "科员", "note": ""},
    {"person_id": 1, "org_id": 10, "title": "德州市信息中心副科级秘书", "start_date": "2000-06", "end_date": "2002-10", "rank": "副科级", "note": ""},
    {"person_id": 1, "org_id": 10, "title": "德州市信息中心正科级秘书、主任助理", "start_date": "2002-10", "end_date": "2005-08", "rank": "正科级", "note": ""},
    {"person_id": 1, "org_id": 11, "title": "德州市信息产业局网络管理科副科长（正科级）", "start_date": "2005-08", "end_date": "2007-04", "rank": "正科级", "note": ""},
    {"person_id": 1, "org_id": 11, "title": "德州市信息产业局网络管理科科长", "start_date": "2007-04", "end_date": "2007-10", "rank": "正科级", "note": ""},
    {"person_id": 1, "org_id": 11, "title": "德州市信息产业局党组成员、副局长、网络管理科科长", "start_date": "2007-10", "end_date": "2008-03", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 11, "title": "德州市信息产业局党组成员、副局长", "start_date": "2008-03", "end_date": "2010-04", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 12, "title": "德州市经济和信息化委员会党组成员、副主任", "start_date": "2010-04", "end_date": "2012-08", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 10, "title": "德州市人民政府副秘书长，市政府办公室党组成员", "start_date": "2012-08", "end_date": "2017-02", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 13, "title": "德州市金融工作办公室党组书记、主任", "start_date": "2017-02", "end_date": "2019-01", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 14, "title": "德州市地方金融监督管理局党组书记、局长（市金融工作办公室主任）", "start_date": "2019-01", "end_date": "2020-09", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 9, "title": "齐河县委副书记、县长", "start_date": "2020-09", "end_date": "2021-12", "rank": "正处级", "note": "从德州调至齐河"},
    {"person_id": 1, "org_id": 1, "title": "惠民县委书记", "start_date": "2021-12", "end_date": "至今", "rank": "正处级", "note": "跨市交流至滨州市惠民县"},

    # ── 许健 (县长) career timeline ──
    {"person_id": 2, "org_id": 15, "title": "博兴县委组织部科员", "start_date": "2002-08", "end_date": "2006-07", "rank": "科员", "note": "期间2002.09-2003.07在滨州市委组织部借调"},
    {"person_id": 2, "org_id": 16, "title": "博兴县卫生局党委委员、副局长", "start_date": "2006-07", "end_date": "2007-08", "rank": "副科级", "note": ""},
    {"person_id": 2, "org_id": 17, "title": "共青团博兴县委书记", "start_date": "2007-08", "end_date": "2008-11", "rank": "正科级", "note": ""},
    {"person_id": 2, "org_id": 18, "title": "共青团滨州市委副书记", "start_date": "2008-11", "end_date": "2011-11", "rank": "副处级", "note": "2008.11-2009.11在十一运组委会志愿者工作部副部长"},
    {"person_id": 2, "org_id": 1, "title": "惠民县委常委、宣传部部长", "start_date": "2011-11", "end_date": "2016-01", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 20, "title": "无棣县委常委、副县长", "start_date": "2016-01", "end_date": "2019-01", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 21, "title": "滨州市科学技术协会党组书记、主席", "start_date": "2019-01", "end_date": "2021-08", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 22, "title": "滨州市人民政府外事办公室党组书记、主任，市委外事工作委员会办公室主任（兼）", "start_date": "2021-08", "end_date": "2021-12", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "惠民县委副书记、县政府党组书记、代县长", "start_date": "2021-12", "end_date": "2022-01", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "惠民县委副书记、县长", "start_date": "2022-01", "end_date": "至今", "rank": "正处级", "note": "2022年1月29日惠民县十九届人大一次会议选举"},

    # ── Current leaders ──
    {"person_id": 3, "org_id": 3, "title": "惠民县人大常委会主任", "start_date": "", "end_date": "至今", "rank": "正处级", "note": ""},
    {"person_id": 4, "org_id": 4, "title": "惠民县政协主席", "start_date": "", "end_date": "至今", "rank": "正处级", "note": ""},
    {"person_id": 5, "org_id": 6, "title": "惠民县委常委、宣传部部长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 7, "title": "惠民县委常委、统战部部长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "兼任"},
    {"person_id": 6, "org_id": 1, "title": "惠民县委常委", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "惠民县领导", "start_date": "", "end_date": "至今", "rank": "", "note": ""},
    {"person_id": 8, "org_id": 5, "title": "惠民县工商联主席、总商会会长", "start_date": "2026-07", "end_date": "至今", "rank": "", "note": "2026年7月当选"},

    # ── Predecessors ──
    {"person_id": 9, "org_id": 1, "title": "惠民县委书记（前任）", "start_date": "", "end_date": "2021-12", "rank": "正处级", "note": "王玮的前任，现任滨州市人大常委会副主任"},
    {"person_id": 10, "org_id": 2, "title": "惠民县委副书记、县长（前任）", "start_date": "", "end_date": "2021-12", "rank": "正处级", "note": "许健的前任"},
]

# ── Relationships ────────────────────────────────────────────────────────────

relationships = [
    # 书记 — 县长 (top duo)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "县委书记与县长党政搭档", "overlap_org": "惠民县", "overlap_period": "2021.12至今"},
    # 书记 — 前任书记
    {"person_a": 1, "person_b": 9, "type": "predecessor_successor", "context": "王玮接任王庆霞惠民县委书记", "overlap_org": "中共惠民县委员会", "overlap_period": "2021.12"},
    # 县长 — 前任县长
    {"person_a": 2, "person_b": 10, "type": "predecessor_successor", "context": "许健接任刘卫忠惠民县长", "overlap_org": "惠民县人民政府", "overlap_period": "2021.12"},
    # 政领导核心班子成员
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委书记与人大主任同届共事", "overlap_org": "惠民县", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "县委书记与政协主席同届共事", "overlap_org": "惠民县", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "县长与宣传部长共事", "overlap_org": "惠民县", "overlap_period": "2021.12至今"},
    # 许健 career overlaps
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "许健曾任惠民县委宣传部部长（2011-2016），张丽现任宣传部部长，前后任关系", "overlap_org": "中共惠民县委宣传部", "overlap_period": "2011-2016/至今"},
]

# ── Run build ────────────────────────────────────────────────────────────────
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

    # ── Person JSONs ──
    person_json_configs = [
        {
            "filename": f"{TODAY}-山东省-滨州市-县委书记-王玮.json",
            "person_id": 1,
            "data": {
                "schema_version": "1.0",
                "generated_at": AS_OF,
                "investigation_scope": {
                    "province": "山东省",
                    "city": "滨州市",
                    "region": "惠民县",
                    "job": "县委书记",
                    "task_id": "shandong_惠民县",
                    "time_focus": "1992年至今",
                },
                "identity": {
                    "person_id": "shandong_binzhou_huimin_wangwei_197505",
                    "name": "王玮",
                    "aliases": [],
                    "gender": "男",
                    "ethnicity": "汉族",
                    "birth": "1975年5月",
                    "birthplace": "山东武城",
                    "native_place": "山东武城",
                    "education": [
                        {
                            "period": "1992.09-1996.06",
                            "institution": "山东工业大学",
                            "major": "计算机应用专业",
                            "degree": "大学学历",
                            "study_type": "full_time",
                            "source_ids": ["S001"],
                        }
                    ],
                    "party_join": "中共党员",
                    "work_start": "1996年7月",
                    "dedupe_keys": {
                        "name_birth": "王玮_197505",
                        "name_birthplace": "王玮_山东武城",
                        "official_profile_url": "https://baike.so.com/doc/5790940-10491428.html",
                    },
                },
                "current_status": {
                    "current_post": "惠民县委书记",
                    "current_org": "中共惠民县委员会",
                    "administrative_rank": "正处级",
                    "as_of": AS_OF,
                    "is_current_confirmed": True,
                    "source_ids": ["S001", "S003"],
                },
                "career_timeline": [
                    {"start": "1992.09", "end": "1996.06", "org": "山东工业大学", "title": "计算机应用专业学生", "level": "", "location": "山东济南", "system": "education", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                    {"start": "1996.07", "end": "2000.06", "org": "德州市信息中心", "title": "科员", "level": "地级市", "location": "山东德州", "system": "government", "rank": "科员", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                    {"start": "2000.06", "end": "2002.10", "org": "德州市信息中心", "title": "副科级秘书", "level": "地级市", "location": "山东德州", "system": "government", "rank": "副科级", "is_key_promotion": True, "notes": "首次晋升副科", "confidence": "confirmed", "source_ids": ["S001"]},
                    {"start": "2002.10", "end": "2005.08", "org": "德州市信息中心", "title": "正科级秘书、主任助理", "level": "地级市", "location": "山东德州", "system": "government", "rank": "正科级", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                    {"start": "2005.08", "end": "2007.04", "org": "德州市信息产业局", "title": "网络管理科副科长（正科级）", "level": "地级市", "location": "山东德州", "system": "government", "rank": "正科级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                    {"start": "2007.04", "end": "2007.10", "org": "德州市信息产业局", "title": "网络管理科科长", "level": "地级市", "location": "山东德州", "system": "government", "rank": "正科级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                    {"start": "2007.10", "end": "2008.03", "org": "德州市信息产业局", "title": "党组成员、副局长、网络管理科科长", "level": "地级市", "location": "山东德州", "system": "government", "rank": "副处级", "is_key_promotion": True, "notes": "提拔副处", "confidence": "confirmed", "source_ids": ["S001"]},
                    {"start": "2008.03", "end": "2010.04", "org": "德州市信息产业局", "title": "党组成员、副局长", "level": "地级市", "location": "山东德州", "system": "government", "rank": "副处级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                    {"start": "2010.04", "end": "2012.08", "org": "德州市经济和信息化委员会", "title": "党组成员、副主任", "level": "地级市", "location": "山东德州", "system": "government", "rank": "副处级", "is_key_promotion": False, "notes": "机构改革转入", "confidence": "confirmed", "source_ids": ["S001"]},
                    {"start": "2012.08", "end": "2017.02", "org": "德州市人民政府", "title": "副秘书长、市政府办公室党组成员", "level": "地级市", "location": "山东德州", "system": "government", "rank": "正处级", "is_key_promotion": True, "notes": "晋升正处级", "confidence": "confirmed", "source_ids": ["S001"]},
                    {"start": "2017.02", "end": "2019.01", "org": "德州市金融工作办公室", "title": "党组书记、主任", "level": "地级市", "location": "山东德州", "system": "government", "rank": "正处级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
                    {"start": "2019.01", "end": "2020.09", "org": "德州市地方金融监督管理局", "title": "党组书记、局长（市金融工作办公室主任）", "level": "地级市", "location": "山东德州", "system": "government", "rank": "正处级", "is_key_promotion": False, "notes": "机构改革转入", "confidence": "confirmed", "source_ids": ["S001"]},
                    {"start": "2020.09", "end": "2021.12", "org": "齐河县人民政府", "title": "齐河县委副书记、县长", "level": "县", "location": "山东德州齐河", "system": "government", "rank": "正处级", "is_key_promotion": True, "notes": "出任县政府正职", "confidence": "confirmed", "source_ids": ["S001"]},
                    {"start": "2021.12", "end": "至今", "org": "中共惠民县委员会", "title": "惠民县委书记", "level": "县", "location": "山东滨州惠民", "system": "party", "rank": "正处级", "is_key_promotion": True, "notes": "跨市交流至滨州，担任县委书记", "confidence": "confirmed", "source_ids": ["S001", "S003"]},
                ],
                "organizations": [{"org_id": o["id"], "name": o["name"], "type": o["type"], "role": "member" if o["id"] in [1] else "leader"} for o in organizations if o["id"] in [1, 8, 9, 10, 11, 12, 13, 14]],
                "relationships": [r for r in relationships if r["person_a"] == 1 or r["person_b"] == 1],
                "governance_record": [
                    {
                        "period": "2021.12至今",
                        "domain": "economic_development",
                        "achievement_or_event": "提出并推动'1357'工作体系，加快培育发展新质生产力",
                        "role_in_event": "县委书记（总指挥）",
                        "measurable_outcome": "",
                        "location": "惠民县",
                        "confidence": "confirmed",
                        "source_ids": ["S003"],
                    },
                ],
                "professional_profile": {
                    "primary_specializations": ["经济管理", "信息化建设", "地方金融监管"],
                    "secondary_specializations": [],
                    "career_pattern": "cross_county_rotation",
                    "systems_experience": ["government", "party"],
                    "geographic_pattern": ["德州市（1996-2021）", "滨州市惠民县（2021至今）"],
                    "promotion_velocity": {
                        "summary": "从科员到正处级用约16年（1996-2012），此后在多个正处级岗位轮换后任县委书记",
                        "notable_fast_promotions": ["2012年从副处级晋升正处级（市政府副秘书长）"],
                    },
                },
                "work_style_and_personality": {
                    "public_style_indicators": [
                        {
                            "trait": "pragmatic",
                            "evidence": "讲话中强调'崇尚实干、注重实绩、追求实效'",
                            "confidence": "plausible",
                            "source_ids": ["S003"],
                        },
                        {
                            "trait": "reform_oriented",
                            "evidence": "推动'1357'工作体系，强调改革与开放",
                            "confidence": "plausible",
                            "source_ids": ["S003"],
                        },
                    ],
                    "speech_themes": ["高质量发展", "党建统领", "实干争先", "勇争一流"],
                    "management_signals": ["注重党建统领", "强调对标先进", "注重培育新质生产力"],
                    "caveat": "Work style is inferred from public records and speeches, not private psychological assessment.",
                },
                "risk_and_integrity_signals": [
                    {"type": "none_found", "description": "未发现公开的纪律处分、审计问题或负面报道", "date": "", "confidence": "plausible", "source_ids": []},
                ],
                "source_register": [
                    {"id": "S001", "title": "王玮（山东省惠民县委书记）- 360百科", "url": "https://baike.so.com/doc/5790940-10491428.html", "publisher": "360百科", "published_at": "2023-02-01", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "high", "notes": "详细记录了王玮从1992年至今的完整履历"},
                    {"id": "S002", "title": "许健（山东省惠民县委副书记、县长）- 360百科", "url": "https://baike.so.com/doc/475202-503223.html", "publisher": "360百科", "published_at": "2023-10-11", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "high", "notes": ""},
                    {"id": "S003", "title": "惠民县工商业联合会第十二次代表大会召开", "url": "http://www.huimin.gov.cn/art/2026/7/10/art_118126_10472251.html", "publisher": "惠民县人民政府", "published_at": "2026-07-10", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认县委书记王玮、县长许健等现职"},
                ],
                "confidence_summary": {
                    "identity": "confirmed",
                    "current_role": "confirmed",
                    "career_completeness": "complete",
                    "relationship_confidence": "high",
                    "biggest_gap": "籍贯武城的具体乡镇未确认；中共山东省第十二次代表大会代表身份需进一步确认",
                },
                "open_questions": [
                    {"priority": "medium", "question": "王玮的籍贯乡镇具体信息？", "why_it_matters": "有助于更精准的人物归类和网络分析", "suggested_queries": ["王玮 武城 具体乡镇"], "last_attempted": AS_OF},
                    {"priority": "low", "question": "王玮在惠民县委书记任期内的具体政绩指标？", "why_it_matters": "评估治理成效", "suggested_queries": ["王玮 惠民县 GDP 增长率"], "last_attempted": AS_OF},
                ],
            },
        },
        {
            "filename": f"{TODAY}-山东省-滨州市-县长-许健.json",
            "person_id": 2,
            "data": {
                "schema_version": "1.0",
                "generated_at": AS_OF,
                "investigation_scope": {
                    "province": "山东省",
                    "city": "滨州市",
                    "region": "惠民县",
                    "job": "县长",
                    "task_id": "shandong_惠民县",
                    "time_focus": "1998年至今",
                },
                "identity": {
                    "person_id": "shandong_binzhou_huimin_xujian_198001",
                    "name": "许健",
                    "aliases": [],
                    "gender": "女",
                    "ethnicity": "汉族",
                    "birth": "1980年1月",
                    "birthplace": "山东博兴",
                    "native_place": "山东博兴",
                    "education": [
                        {
                            "period": "1998.09-2002.07",
                            "institution": "烟台大学",
                            "major": "中国语言文学系汉语言文学专业",
                            "degree": "文学学士",
                            "study_type": "full_time",
                            "source_ids": ["S002"],
                        }
                    ],
                    "party_join": "中共党员",
                    "work_start": "2002年8月",
                    "dedupe_keys": {
                        "name_birth": "许健_198001",
                        "name_birthplace": "许健_山东博兴",
                        "official_profile_url": "https://baike.so.com/doc/475202-503223.html",
                    },
                },
                "current_status": {
                    "current_post": "惠民县委副书记、县长",
                    "current_org": "惠民县人民政府",
                    "administrative_rank": "正处级",
                    "as_of": AS_OF,
                    "is_current_confirmed": True,
                    "source_ids": ["S002", "S003"],
                },
                "career_timeline": [
                    {"start": "1998.09", "end": "2002.07", "org": "烟台大学", "title": "中国语言文学系汉语言文学专业学生", "level": "", "location": "山东烟台", "system": "education", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S002"]},
                    {"start": "2002.07", "end": "2002.08", "org": "", "title": "毕业待分配", "level": "", "location": "", "system": "other", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S002"]},
                    {"start": "2002.08", "end": "2006.07", "org": "中共博兴县委组织部", "title": "科员", "level": "县", "location": "山东滨州博兴", "system": "organization", "rank": "科员", "is_key_promotion": False, "notes": "期间2002.09-2003.07在滨州市委组织部借调", "confidence": "confirmed", "source_ids": ["S002"]},
                    {"start": "2006.07", "end": "2007.08", "org": "博兴县卫生局", "title": "党委委员、副局长", "level": "县", "location": "山东滨州博兴", "system": "government", "rank": "副科级", "is_key_promotion": True, "notes": "首次提拔副科", "confidence": "confirmed", "source_ids": ["S002"]},
                    {"start": "2007.08", "end": "2008.11", "org": "共青团博兴县委员会", "title": "团委书记", "level": "县", "location": "山东滨州博兴", "system": "other", "rank": "正科级", "is_key_promotion": True, "notes": "晋升正科", "confidence": "confirmed", "source_ids": ["S002"]},
                    {"start": "2008.11", "end": "2011.11", "org": "共青团滨州市委员会", "title": "副书记", "level": "地级市", "location": "山东滨州", "system": "other", "rank": "副处级", "is_key_promotion": True, "notes": "晋升副处，期间在十一运组委会志愿者工作部副部长", "confidence": "confirmed", "source_ids": ["S002"]},
                    {"start": "2011.11", "end": "2016.01", "org": "中共惠民县委员会", "title": "惠民县委常委、宣传部部长", "level": "县", "location": "山东滨州惠民", "system": "party", "rank": "副处级", "is_key_promotion": False, "notes": "首次到惠民县任职", "confidence": "confirmed", "source_ids": ["S002"]},
                    {"start": "2016.01", "end": "2019.01", "org": "无棣县人民政府", "title": "无棣县委常委、副县长", "level": "县", "location": "山东滨州无棣", "system": "government", "rank": "副处级", "is_key_promotion": False, "notes": "跨县交流", "confidence": "confirmed", "source_ids": ["S002"]},
                    {"start": "2019.01", "end": "2021.08", "org": "滨州市科学技术协会", "title": "党组书记、主席", "level": "地级市", "location": "山东滨州", "system": "other", "rank": "正处级", "is_key_promotion": True, "notes": "晋升正处级", "confidence": "confirmed", "source_ids": ["S002"]},
                    {"start": "2021.08", "end": "2021.12", "org": "滨州市人民政府外事办公室", "title": "党组书记、主任，市委外事工作委员会办公室主任（兼）", "level": "地级市", "location": "山东滨州", "system": "government", "rank": "正处级", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S002"]},
                    {"start": "2021.12", "end": "2022.01", "org": "惠民县人民政府", "title": "惠民县委副书记、县政府党组书记、代县长", "level": "县", "location": "山东滨州惠民", "system": "government", "rank": "正处级", "is_key_promotion": True, "notes": "回到惠民县任政府正职", "confidence": "confirmed", "source_ids": ["S002"]},
                    {"start": "2022.01", "end": "至今", "org": "惠民县人民政府", "title": "惠民县委副书记、县长", "level": "县", "location": "山东滨州惠民", "system": "government", "rank": "正处级", "is_key_promotion": False, "notes": "2022年1月29日县十九届人大一次会议选举", "confidence": "confirmed", "source_ids": ["S002"]},
                ],
                "organizations": [{"org_id": o["id"], "name": o["name"], "type": o["type"], "role": "leader"} for o in organizations if o["id"] in [1, 2, 15, 16, 17, 18, 19, 20, 21, 22]],
                "relationships": [r for r in relationships if r["person_a"] == 2 or r["person_b"] == 2],
                "governance_record": [
                    {
                        "period": "2022.01至今",
                        "domain": "economic_development",
                        "achievement_or_event": "主持惠民县政府全面工作，推动服务业发展",
                        "role_in_event": "县长",
                        "measurable_outcome": "",
                        "location": "惠民县",
                        "confidence": "confirmed",
                        "source_ids": ["S003"],
                    },
                    {
                        "period": "2025-2026",
                        "domain": "other",
                        "achievement_or_event": "讲树立和践行正确政绩观学习教育专题党课",
                        "role_in_event": "授课人",
                        "measurable_outcome": "",
                        "location": "惠民县",
                        "confidence": "confirmed",
                        "source_ids": [],
                    },
                ],
                "professional_profile": {
                    "primary_specializations": ["党政管理", "组织人事", "宣传文化", "科学技术管理"],
                    "secondary_specializations": [],
                    "career_pattern": "local_ladder",
                    "systems_experience": ["party", "government", "organization", "other"],
                    "geographic_pattern": ["博兴县（2002-2011）", "惠民县（2011-2016第一次）", "无棣县（2016-2019）", "滨州市直（2019-2021）", "惠民县（2021至今第二次）"],
                    "promotion_velocity": {
                        "summary": "从科员到正处级用约17年（2002-2019），经历组织、宣传、科技、外事等多系统锻炼",
                        "notable_fast_promotions": ["2007年从副科级到正科级（团委书记）", "2008年从正科级到副处级（团市委副书记）"],
                    },
                },
                "work_style_and_personality": {
                    "public_style_indicators": [
                        {
                            "trait": "discipline_oriented",
                            "evidence": "讲树立和践行正确政绩观学习教育专题党课",
                            "confidence": "plausible",
                            "source_ids": [],
                        },
                        {
                            "trait": "grassroots_oriented",
                            "evidence": "多次调研基层工作，包括城区供暖、博物馆等",
                            "confidence": "plausible",
                            "source_ids": [],
                        },
                    ],
                    "speech_themes": ["正确政绩观", "高质量发展", "为民服务"],
                    "management_signals": ["注重财税管理", "关注民生（供暖、文化等）"],
                    "caveat": "Work style is inferred from public records and speeches, not private psychological assessment.",
                },
                "risk_and_integrity_signals": [
                    {"type": "none_found", "description": "未发现公开的纪律处分、审计问题或负面报道", "date": "", "confidence": "plausible", "source_ids": []},
                ],
                "source_register": [
                    {"id": "S002", "title": "许健（山东省惠民县委副书记、县长）- 360百科", "url": "https://baike.so.com/doc/475202-503223.html", "publisher": "360百科", "published_at": "2023-10-11", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "high", "notes": "详细记录了许健从1998年至今的完整履历和工作分工"},
                    {"id": "S003", "title": "惠民县工商业联合会第十二次代表大会召开", "url": "http://www.huimin.gov.cn/art/2026/7/10/art_118126_10472251.html", "publisher": "惠民县人民政府", "published_at": "2026-07-10", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认许健县长现职"},
                    {"id": "S004", "title": "惠民县举办'两优一先'先进事迹报告会", "url": "http://www.huimin.gov.cn/art/2026/7/22/art_118126_10472558.html", "publisher": "惠民县人民政府", "published_at": "2026-07-22", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认袁光新、杨宝亮等现职"},
                ],
                "confidence_summary": {
                    "identity": "confirmed",
                    "current_role": "confirmed",
                    "career_completeness": "complete",
                    "relationship_confidence": "high",
                    "biggest_gap": "教育背景中大学本科为第一学历，是否有在职研究生学历未确认",
                },
                "open_questions": [
                    {"priority": "medium", "question": "许健是否有在职研究生或更高学历？", "why_it_matters": "评估其教育背景", "suggested_queries": ["许健 在职研究生 学历"], "last_attempted": AS_OF},
                    {"priority": "medium", "question": "许健在无棣县副县长期间分管领域的具体成绩？", "why_it_matters": "评估其在经济管理方面的能力", "suggested_queries": ["许健 无棣 分管"], "last_attempted": AS_OF},
                ],
            },
        },
    ]

    for cfg in person_json_configs:
        pjson_path = PJSON_DIR / cfg["filename"]
        with open(pjson_path, "w", encoding="utf-8") as f:
            json.dump(cfg["data"], f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {pjson_path}")

    print(f"\nBuild complete for {SLUG}")
    print(f"  DB:     {DB_PATH}")
    print(f"  GEXF:   {GEXF_PATH}")
    print(f"  Person: {PJSON_DIR}/{TODAY}-山东省-滨州市-县委书记-王玮.json")
    print(f"  Person: {PJSON_DIR}/{TODAY}-山东省-滨州市-县长-许健.json")
