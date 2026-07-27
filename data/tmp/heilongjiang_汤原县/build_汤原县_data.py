#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 汤原县 (Tangyuan County), 佳木斯市, 黑龙江省.

Investigation date: 2026-07-24
Task ID: heilongjiang_汤原县
Level: 县
Research sources:
  - Tangyuan County Government Website (www.tangyuan.gov.cn) — leadership page
  - Government news articles (杨宏志 presiding, 王威 inspecting)
  - Baidu Baike/web search: blocked/403; Exa: rate-limited

Research Note:
  Web access to Chinese sources was partially degraded.
  - tangyuan.gov.cn: Accessible — confirmed full leadership roster (县委, 人大, 政府, 政协)
  - 县委书记: 杨宏志 confirmed from official news article (2026-07-20)
  - 县长: 王威 (县委副书记、县长) confirmed from official news article (2026-07-13)
  - Full leadership team listed on 领导之窗 page
  - Baidu Baike: 403 blocked
  - Exa search: rate-limited

Under the source_fallbacks.md guidelines, this run produces structurally valid
artifacts with explicit uncertainty markers for biographical details.
"""

import json
import sqlite3
import os
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

BASE = os.path.dirname(os.path.abspath(__file__))
SLUG = "汤原县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = TODAY

DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")
PERSONS_DIR_PATH = Path(BASE)

# Also produce canonical destination paths
CANONICAL_DB = DATABASE_DIR / f"{SLUG}_network.db"
CANONICAL_GEXF = GRAPH_DIR / f"{SLUG}_network.gexf"
CANONICAL_PERSONS = PERSONS_DIR

# ── Persons ──────────────────────────────────────────────────────────────────

# Person ID convention: tangyuan_{name_pinyin}
# Person IDs are sequential for DB; keep mapping for relationships

persons = [
    # ══════════════════════════════════════════════════════════════════════════
    # Core Leadership — Party Committee
    # ══════════════════════════════════════════════════════════════════════════

    {
        "id": 1,
        "name": "杨宏志",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共汤原县委员会",
        "source": "tangyuan.gov.cn 领导之窗 + news article 2026-07-20",
    },
    {
        "id": 2,
        "name": "王威",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "中共汤原县委员会 / 汤原县人民政府",
        "source": "tangyuan.gov.cn 领导之窗 + news article 2026-07-13",
    },
    {
        "id": 3,
        "name": "路云强",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共汤原县委员会",
        "source": "tangyuan.gov.cn 领导之窗",
    },
    {
        "id": 4,
        "name": "刘礼富",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共汤原县委员会",
        "source": "tangyuan.gov.cn 领导之窗",
    },
    {
        "id": 5,
        "name": "赵毅",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共汤原县委员会",
        "source": "tangyuan.gov.cn 领导之窗",
    },
    {
        "id": 6,
        "name": "段长山",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共汤原县委员会",
        "source": "tangyuan.gov.cn 领导之窗",
    },
    {
        "id": 7,
        "name": "刘宏年",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "中共汤原县委员会 / 汤原县人民政府",
        "source": "tangyuan.gov.cn 领导之窗",
    },
    {
        "id": 8,
        "name": "宋俊儒",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共汤原县委员会",
        "source": "tangyuan.gov.cn 领导之窗",
    },
    {
        "id": 9,
        "name": "刘继君",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共汤原县委员会",
        "source": "tangyuan.gov.cn 领导之窗",
    },
    {
        "id": 10,
        "name": "万美娇",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共汤原县委员会",
        "source": "tangyuan.gov.cn 领导之窗",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # County Government — Deputy Mayors (副县长)
    # ══════════════════════════════════════════════════════════════════════════

    {
        "id": 11,
        "name": "王毓水",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "汤原县人民政府",
        "source": "tangyuan.gov.cn 领导之窗",
    },
    {
        "id": 12,
        "name": "徐政华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "汤原县人民政府",
        "source": "tangyuan.gov.cn 领导之窗",
    },
    {
        "id": 13,
        "name": "杨冰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "汤原县人民政府",
        "source": "tangyuan.gov.cn 领导之窗 + news article 2026-07-13",
    },
    {
        "id": 14,
        "name": "白玉石",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "汤原县人民政府",
        "source": "tangyuan.gov.cn 领导之窗",
    },
    {
        "id": 15,
        "name": "王春阳",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "汤原县人民政府",
        "source": "tangyuan.gov.cn 领导之窗",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # County People's Congress (县人大)
    # ══════════════════════════════════════════════════════════════════════════

    {
        "id": 16,
        "name": "张志文",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "汤原县人民代表大会常务委员会",
        "source": "tangyuan.gov.cn 领导之窗",
    },
    {
        "id": 17,
        "name": "姚青敏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "汤原县人民代表大会常务委员会",
        "source": "tangyuan.gov.cn 领导之窗",
    },
    {
        "id": 18,
        "name": "李玉英",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "汤原县人民代表大会常务委员会",
        "source": "tangyuan.gov.cn 领导之窗",
    },
    {
        "id": 19,
        "name": "欧喜东",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "汤原县人民代表大会常务委员会",
        "source": "tangyuan.gov.cn 领导之窗",
    },
    {
        "id": 20,
        "name": "孙建军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "汤原县人民代表大会常务委员会",
        "source": "tangyuan.gov.cn 领导之窗",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # County Political Consultative Conference (县政协)
    # ══════════════════════════════════════════════════════════════════════════

    {
        "id": 21,
        "name": "马广胜",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "中国人民政治协商会议汤原县委员会",
        "source": "tangyuan.gov.cn 领导之窗",
    },
    {
        "id": 22,
        "name": "王玉平",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协副主席",
        "current_org": "中国人民政治协商会议汤原县委员会",
        "source": "tangyuan.gov.cn 领导之窗",
    },
    {
        "id": 23,
        "name": "张英杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协副主席",
        "current_org": "中国人民政治协商会议汤原县委员会",
        "source": "tangyuan.gov.cn 领导之窗",
    },
    {
        "id": 24,
        "name": "孔霞",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协副主席",
        "current_org": "中国人民政治协商会议汤原县委员会",
        "source": "tangyuan.gov.cn 领导之窗",
    },

    # ══════════════════════════════════════════════════════════════════════════
    # Other leaders mentioned in news
    # ══════════════════════════════════════════════════════════════════════════

    {
        "id": 25,
        "name": "孙群",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "汤原县",
        "source": "news article 2026-07-13 (accompanied 王威 inspection)",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────

organizations = [
    # Party Committee
    {"id": 1, "name": "中共汤原县委员会", "type": "党委", "level": "县", "parent": "中共佳木斯市委员会", "location": "汤原县"},
    # Government
    {"id": 2, "name": "汤原县人民政府", "type": "政府", "level": "县", "parent": "佳木斯市人民政府", "location": "汤原县"},
    # People's Congress
    {"id": 3, "name": "汤原县人民代表大会常务委员会", "type": "人大", "level": "县", "parent": "", "location": "汤原县"},
    # Political Consultative Conference
    {"id": 4, "name": "中国人民政治协商会议汤原县委员会", "type": "政协", "level": "县", "parent": "", "location": "汤原县"},
]

# ── Positions ────────────────────────────────────────────────────────────────

positions = [
    # Party Committee leaders
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "", "end": "", "rank": "正处级", "note": "县委书记，主持县委全面工作"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "", "end": "", "rank": "正处级", "note": "同时任县长"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "", "end": "", "rank": "正处级", "note": "县人民政府县长"},
    {"person_id": 3, "org_id": 1, "title": "县委常委", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start": "", "end": "", "rank": "副处级", "note": "同时任副县长"},
    {"person_id": 7, "org_id": 2, "title": "副县长", "start": "", "end": "", "rank": "副处级", "note": "县委常委、副县长"},
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start": "", "end": "", "rank": "副处级", "note": ""},

    # Government deputy leaders
    {"person_id": 11, "org_id": 2, "title": "副县长", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "副县长", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "副县长", "start": "", "end": "", "rank": "副处级", "note": "news article 2026-07-13 confirms accompanies 王威"},
    {"person_id": 14, "org_id": 2, "title": "副县长", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "副县长", "start": "", "end": "", "rank": "副处级", "note": ""},

    # People's Congress
    {"person_id": 16, "org_id": 3, "title": "县人大常委会主任", "start": "", "end": "", "rank": "正处级", "note": ""},
    {"person_id": 17, "org_id": 3, "title": "县人大常委会副主任", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 18, "org_id": 3, "title": "县人大常委会副主任", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 19, "org_id": 3, "title": "县人大常委会副主任", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 20, "org_id": 3, "title": "县人大常委会副主任", "start": "", "end": "", "rank": "副处级", "note": ""},

    # Political Consultative Conference
    {"person_id": 21, "org_id": 4, "title": "县政协主席", "start": "", "end": "", "rank": "正处级", "note": ""},
    {"person_id": 22, "org_id": 4, "title": "县政协副主席", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 23, "org_id": 4, "title": "县政协副主席", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": 24, "org_id": 4, "title": "县政协副主席", "start": "", "end": "", "rank": "副处级", "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────────────
# 杨宏志 and 王威 are the top two leaders, working together as secretary-mayor

relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "党政搭档",
        "context": "杨宏志任县委书记，王威任县委副书记、县长，构成汤原县党政主要领导工作搭档",
        "overlap_org": "中共汤原县委员会",
        "overlap_period": "至2026-07",
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "上下级",
        "context": "县委书记与县委常委班子成员",
        "overlap_org": "中共汤原县委员会",
        "overlap_period": "",
    },
    {
        "person_a": 1,
        "person_b": 4,
        "type": "上下级",
        "context": "县委书记与县委常委班子成员",
        "overlap_org": "中共汤原县委员会",
        "overlap_period": "",
    },
    {
        "person_a": 1,
        "person_b": 5,
        "type": "上下级",
        "context": "县委书记与县委常委班子成员",
        "overlap_org": "中共汤原县委员会",
        "overlap_period": "",
    },
    {
        "person_a": 1,
        "person_b": 6,
        "type": "上下级",
        "context": "县委书记与县委常委班子成员",
        "overlap_org": "中共汤原县委员会",
        "overlap_period": "",
    },
    {
        "person_a": 1,
        "person_b": 7,
        "type": "上下级",
        "context": "县委书记与县委常委班子成员",
        "overlap_org": "中共汤原县委员会",
        "overlap_period": "",
    },
    {
        "person_a": 1,
        "person_b": 8,
        "type": "上下级",
        "context": "县委书记与县委常委班子成员",
        "overlap_org": "中共汤原县委员会",
        "overlap_period": "",
    },
    {
        "person_a": 1,
        "person_b": 9,
        "type": "上下级",
        "context": "县委书记与县委常委班子成员",
        "overlap_org": "中共汤原县委员会",
        "overlap_period": "",
    },
    {
        "person_a": 1,
        "person_b": 10,
        "type": "上下级",
        "context": "县委书记与县委常委班子成员",
        "overlap_org": "中共汤原县委员会",
        "overlap_period": "",
    },
    {
        "person_a": 2,
        "person_b": 7,
        "type": "上下级",
        "context": "县长与副县长（县委常委兼）工作搭档",
        "overlap_org": "汤原县人民政府",
        "overlap_period": "",
    },
    {
        "person_a": 2,
        "person_b": 11,
        "type": "上下级",
        "context": "县长与副县长工作搭档",
        "overlap_org": "汤原县人民政府",
        "overlap_period": "",
    },
    {
        "person_a": 2,
        "person_b": 12,
        "type": "上下级",
        "context": "县长与副县长工作搭档",
        "overlap_org": "汤原县人民政府",
        "overlap_period": "",
    },
    {
        "person_a": 2,
        "person_b": 13,
        "type": "上下级",
        "context": "县长与副县长工作搭档，共同参与调研活动",
        "overlap_org": "汤原县人民政府",
        "overlap_period": "至2026-07",
    },
    {
        "person_a": 2,
        "person_b": 14,
        "type": "上下级",
        "context": "县长与副县长工作搭档",
        "overlap_org": "汤原县人民政府",
        "overlap_period": "",
    },
    {
        "person_a": 2,
        "person_b": 15,
        "type": "上下级",
        "context": "县长与副县长工作搭档",
        "overlap_org": "汤原县人民政府",
        "overlap_period": "",
    },
]

# ── Source Register ──────────────────────────────────────────────────────────

source_register = [
    {
        "id": "S001",
        "title": "汤原县人民政府 领导之窗",
        "url": "https://www.tangyuan.gov.cn/tyx/c101879/ldzc.shtml",
        "publisher": "汤原县人民政府",
        "published_at": "",
        "accessed_at": "2026-07-24",
        "source_type": "official",
        "reliability": "high",
        "notes": "完整领导班子名单（县委、人大、政府、政协）",
    },
    {
        "id": "S002",
        "title": "杨宏志主持召开全县群众身边不正之风和腐败问题集中整治工作领导小组第3次会议",
        "url": "https://www.tangyuan.gov.cn/tyx/c101874/202607/c04_306269.shtml",
        "publisher": "汤原县人民政府",
        "published_at": "2026-07-20",
        "accessed_at": "2026-07-24",
        "source_type": "official",
        "reliability": "high",
        "notes": "确认杨宏志为县委书记",
    },
    {
        "id": "S003",
        "title": "王威调研督导防汛备汛和群众身边不正之风和腐败问题集中整治等重点工作",
        "url": "https://www.tangyuan.gov.cn/tyx/c101874/202607/c04_305774.shtml",
        "publisher": "汤原县人民政府",
        "published_at": "2026-07-13",
        "accessed_at": "2026-07-24",
        "source_type": "official",
        "reliability": "high",
        "notes": "确认王威为县委副书记、县长；确认杨冰、孙群参加调研",
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# Person JSON generation helper
# ══════════════════════════════════════════════════════════════════════════════

def make_person_json(person, timeline, rels, sources):
    """Create a person graph JSON following the schema in person_graph_json.md."""
    return {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "黑龙江省",
            "city": "佳木斯市",
            "region": "汤原县",
            "job": person["current_post"],
            "task_id": "heilongjiang_汤原县",
            "time_focus": "2026-07",
        },
        "identity": {
            "person_id": f"tangyuan_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person.get('birth','')}",
                "name_birthplace": f"{person['name']}_{person.get('birthplace','')}",
                "official_profile_url": "https://www.tangyuan.gov.cn/tyx/c101879/ldzc.shtml",
            },
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "正处级" if "书记" in person["current_post"] or "县长" in person["current_post"] or "主任" in person["current_post"] or "主席" in person["current_post"] else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"],
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": rels,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "公开资料不足，无法评估晋升速度",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "此评估基于有限公开记录，不代表私人心理评估",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "截至2026年7月，公开渠道未发现违纪违法通报或负面舆情",
                "date": "",
                "confidence": "unverified",
                "source_ids": [],
            }
        ],
        "source_register": sources,
        "confidence_summary": {
            "identity": "unverified",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "公开资料未找到出生年月、籍贯、教育背景及完整履历",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{person['name']}的出生年月、籍贯、教育背景",
                "why_it_matters": "用于人员去重和身份确认",
                "suggested_queries": [f"{person['name']} 简历", f"{person['name']} 百度百科", f"{person['name']} 任前公示"],
                "last_attempted": "2026-07-24",
            },
            {
                "priority": "critical",
                "question": f"{person['name']}的完整职业履历",
                "why_it_matters": "用于时间线分析和工作关系网络构建",
                "suggested_queries": [f"{person['name']} 汤原县 任职经历", f"{person['name']} 历任"],
                "last_attempted": "2026-07-24",
            },
            {
                "priority": "high",
                "question": f"{person['name']}的入党时间和参加工作时间",
                "why_it_matters": "用于评估职业阶段和晋升路径",
                "suggested_queries": [f"{person['name']} 参加工作", f"{person['name']} 入党"],
                "last_attempted": "2026-07-24",
            },
        ],
    }


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def build():
    print("=" * 60)
    print("  汤原县领导班子工作关系网络")
    print("  等级: 县")
    print("  调查日期: 2026-07-24")
    print("  信息来源: 汤原县政府网站 + 新闻公告")
    print("=" * 60)

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
    print(f"\n✅ 汤原县数据构建完成。")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

    # ── Generate Person Graph JSONs ──
    print("\n--- 生成个人图谱 JSON ---")

    # 1. 杨宏志 (县委书记)
    yang_timeline = [
        {"start": "", "end": "", "org": "中共汤原县委员会", "title": "汤原县委书记",
         "notes": "2026年7月仍以县委书记身份主持会议",
         "confidence": "confirmed", "source_ids": ["S001", "S002"]},
    ]
    yang_relationships = [
        {"person": "王威", "person_id": "tangyuan_王威", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "县委书记与县长党政工作搭档",
         "overlap_org": "中共汤原县委员会",
         "overlap_period": "至2026-07",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S002", "S003"]},
    ]
    yang_json = make_person_json(persons[0], yang_timeline, yang_relationships, source_register)
    yang_path = PERSONS_DIR_PATH / f"{TODAY}-黑龙江省-佳木斯市-县委书记-杨宏志.json"
    with open(yang_path, "w", encoding="utf-8") as f:
        json.dump(yang_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {yang_path.name}")

    # 2. 王威 (县长)
    wang_timeline = [
        {"start": "", "end": "", "org": "中共汤原县委员会", "title": "汤原县委副书记、县长",
         "notes": "2026年7月仍以县委副书记、县长身份开展工作",
         "confidence": "confirmed", "source_ids": ["S001", "S003"]},
    ]
    wang_relationships = [
        {"person": "杨宏志", "person_id": "tangyuan_杨宏志", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "县长与县委书记党政工作搭档",
         "overlap_org": "中共汤原县委员会",
         "overlap_period": "至2026-07",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S002", "S003"]},
        {"person": "杨冰", "person_id": "tangyuan_杨冰", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "县长与副县长共同开展调研",
         "overlap_org": "汤原县人民政府",
         "overlap_period": "至2026-07",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]},
        {"person": "孙群", "person_id": "tangyuan_孙群", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "县长与县领导共同开展调研",
         "overlap_org": "汤原县",
         "overlap_period": "至2026-07",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]},
    ]
    wang_json = make_person_json(persons[1], wang_timeline, wang_relationships, source_register)
    wang_path = PERSONS_DIR_PATH / f"{TODAY}-黑龙江省-佳木斯市-县长-王威.json"
    with open(wang_path, "w", encoding="utf-8") as f:
        json.dump(wang_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {wang_path.name}")

    print(f"\n所有 Person Graph JSONs 已生成到: {PERSONS_DIR_PATH}")


if __name__ == "__main__":
    build()
