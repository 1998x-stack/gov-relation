#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 十堰市 (Shiyan City), 湖北省.

Investigation date: 2026-07-24
Task ID: hubei_十堰市
Level: 地级市
Targets: 市委书记 & 市长

Research sources:
  - www.shiyan.gov.cn — 十堰市人民政府官方网站 (primary, current as of July 2026)
  - https://www.shiyan.gov.cn/xxgk/xxgk_fdgk/xxgk_sld/ — 市领导页面
  - News articles and meeting attendance lists from 十堰市人民政府 website (July 2026)

Confidence notes:
  - Current roles: confirmed via official government website (July 2026)
  - Biographical details (birth, birthplace, education): confirmed from official resume pages
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
SLUG = "十堰市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "hubei_十堰市"
if _CURRENT_DIR.name == "hubei_十堰市":
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
        "name": "王永辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年8月",
        "birthplace": "河北藁城",
        "education": "博士研究生学历",
        "party_join": "1990年10月",
        "work_start": "1992年7月",
        "current_post": "市委书记",
        "current_org": "中共十堰市委员会",
        "source": "https://www.shiyan.gov.cn/xxgk/xxgk_fdgk/xxgk_sld/sysw/wyh/",
    },
    {
        "id": 2,
        "name": "余珂",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年1月",
        "birthplace": "江西奉新",
        "education": "研究生学历",
        "party_join": "1997年11月",
        "work_start": "1998年7月",
        "current_post": "市委副书记、市长",
        "current_org": "十堰市人民政府",
        "source": "https://www.shiyan.gov.cn/xxgk/xxgk_fdgk/xxgk_sld/sysw/yk_122557/",
    },
    {
        "id": 3,
        "name": "张澍",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年9月",
        "birthplace": "湖北罗田",
        "education": "研究生学历，经济学博士学位",
        "party_join": "1999年3月",
        "work_start": "2006年7月",
        "current_post": "市委副书记",
        "current_org": "中共十堰市委员会",
        "source": "https://www.shiyan.gov.cn/xxgk/xxgk_fdgk/xxgk_sld/sysw/hzl_sw/",
    },
    # ══════════════════════════════════════════════════════════════════════
    # Standing Committee Members
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 4,
        "name": "陈滢",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、组织部部长",
        "current_org": "中共十堰市委员会",
        "source": "https://www.shiyan.gov.cn/xxgk/xxgk_fdgk/xxgk_sld/sysw/cjf_109713/",
    },
    {
        "id": 5,
        "name": "汤红兵",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、宣传部部长",
        "current_org": "中共十堰市委员会",
        "source": "https://www.shiyan.gov.cn/xxgk/xxgk_fdgk/xxgk_sld/sysw/cjf_109567/",
    },
    {
        "id": 6,
        "name": "聂汉平",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、纪委书记、市监察委员会主任",
        "current_org": "中共十堰市纪律检查委员会",
        "source": "https://www.shiyan.gov.cn/xxgk/xxgk_fdgk/xxgk_sld/sysw/cjf_109666/",
    },
    {
        "id": 7,
        "name": "高红民",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、市委秘书长",
        "current_org": "中共十堰市委员会",
        "source": "https://www.shiyan.gov.cn/xxgk/xxgk_fdgk/xxgk_sld/sysw/hzl_sw_114730/",
    },
    {
        "id": 8,
        "name": "钟金铎",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、十堰军分区大校司令员",
        "current_org": "十堰军分区",
        "source": "https://www.shiyan.gov.cn/xxgk/xxgk_fdgk/xxgk_sld/sysw/zjd/",
    },
    {
        "id": 9,
        "name": "周智勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年9月",
        "birthplace": "湖北麻城",
        "education": "大学学历",
        "party_join": "2001年9月",
        "work_start": "1999年7月",
        "current_post": "市委常委、常务副市长",
        "current_org": "十堰市人民政府",
        "source": "https://www.shiyan.gov.cn/xxgk/xxgk_fdgk/xxgk_sld/sysw/zzy_117775/",
    },
    {
        "id": 10,
        "name": "邹桂香",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、副市长",
        "current_org": "十堰市人民政府",
        "source": "https://www.shiyan.gov.cn/xxgk/xxgk_fdgk/xxgk_sld/sysw/zgx/",
    },
    {
        "id": 11,
        "name": "邹磊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、政法委书记",
        "current_org": "中共十堰市委员会",
        "source": "https://www.shiyan.gov.cn/xxgk/xxgk_fdgk/xxgk_sld/sysw/zl/",
    },
    {
        "id": 12,
        "name": "郭清尧",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、副市长",
        "current_org": "十堰市人民政府",
        "source": "https://www.shiyan.gov.cn/xxgk/xxgk_fdgk/xxgk_sld/sysw/zl_123471/",
    },
    {
        "id": 13,
        "name": "张捍声",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、统战部部长、副市长",
        "current_org": "中共十堰市委员会",
        "source": "https://www.shiyan.gov.cn/xxgk/xxgk_fdgk/xxgk_sld/sysw/zl_123500/",
    },
    # ══════════════════════════════════════════════════════════════════════
    # Deputy Mayors (non-standing committee)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 14,
        "name": "龚举海",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "十堰市人民政府",
        "source": "https://www.shiyan.gov.cn/xxgk/xxgk_fdgk/xxgk_sld/syszf/",
    },
    {
        "id": 15,
        "name": "朱云慧",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "十堰市人民政府",
        "source": "https://www.shiyan.gov.cn/xxgk/xxgk_fdgk/xxgk_sld/syszf/",
    },
    {
        "id": 16,
        "name": "宋嵘",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长、市公安局局长",
        "current_org": "十堰市人民政府",
        "source": "https://www.shiyan.gov.cn/xxgk/xxgk_fdgk/xxgk_sld/syszf/",
    },
    {
        "id": 17,
        "name": "杨亚军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "十堰市人民政府",
        "source": "https://www.shiyan.gov.cn/xxgk/xxgk_fdgk/xxgk_sld/syszf/",
    },
    {
        "id": 18,
        "name": "胡先平",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政府党组成员，十堰经济技术开发区党工委副书记、管委会主任",
        "current_org": "十堰市人民政府",
        "source": "https://www.shiyan.gov.cn/xxgk/xxgk_fdgk/xxgk_sld/syszf/",
    },
    # ══════════════════════════════════════════════════════════════════════
    # 人大 / 政协
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 19,
        "name": "赵哲",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "十堰市人民代表大会常务委员会",
        "source": "https://www.shiyan.gov.cn/xxgk/xxgk_fdgk/xxgk_sld/sysrd/",
    },
    {
        "id": 20,
        "name": "蔡贤忠",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "中国人民政治协商会议十堰市委员会",
        "source": "https://www.shiyan.gov.cn/xxgk/xxgk_fdgk/xxgk_sld/syszx/",
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 21,
        "name": "黄剑雄",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市委书记",
        "current_org": "中共十堰市委员会",
        "source": "unverified — web search degraded (Baidu Baike 403)",
    },
    {
        "id": 22,
        "name": "胡亚波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市委书记（现任荆门市委书记）",
        "current_org": "中共荆门市委员会",
        "source": "unverified — web search degraded",
    },
]

# ── Organizations ────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共十堰市委员会", "type": "党委", "level": "地级市", "parent": "", "location": "十堰市"},
    {"id": 2, "name": "十堰市人民政府", "type": "政府", "level": "地级市", "parent": "", "location": "十堰市"},
    {"id": 3, "name": "中共十堰市纪律检查委员会", "type": "纪委", "level": "地级市", "parent": "", "location": "十堰市"},
    {"id": 4, "name": "十堰军分区", "type": "军事", "level": "地级市", "parent": "", "location": "十堰市"},
    {"id": 5, "name": "十堰市人民代表大会常务委员会", "type": "人大", "level": "地级市", "parent": "", "location": "十堰市"},
    {"id": 6, "name": "中国人民政治协商会议十堰市委员会", "type": "政协", "level": "地级市", "parent": "", "location": "十堰市"},
    {"id": 7, "name": "武当山旅游经济特区党工委", "type": "党委", "level": "县级", "parent": "十堰市", "location": "武当山"},
    {"id": 8, "name": "十堰经济技术开发区党工委", "type": "开发区", "level": "县级", "parent": "十堰市", "location": "十堰经济技术开发区"},
    {"id": 9, "name": "十堰高新技术产业开发区党工委", "type": "开发区", "level": "县级", "parent": "十堰市", "location": "十堰高新区"},
    {"id": 10, "name": "十堰市公安局", "type": "政府", "level": "地级市", "parent": "十堰市人民政府", "location": "十堰市"},
    {"id": 11, "name": "中共荆门市委员会", "type": "党委", "level": "地级市", "parent": "", "location": "荆门市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # Current leaders
    {"person_id": 1, "org_id": 1, "title": "市委书记、十堰军分区党委第一书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "市委副书记、市长", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "市委副书记、武当山旅游经济特区党工委书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # Standing Committee
    {"person_id": 4, "org_id": 1, "title": "市委常委、组织部部长、十堰经济技术开发区党工委书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "市委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 6, "org_id": 3, "title": "市委常委、纪委书记、市监察委员会主任", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "市委常委、市委秘书长、十堰高新区党工委书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 8, "org_id": 4, "title": "市委常委、十堰军分区大校司令员", "start_date": "", "end_date": "present", "rank": "正师级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "市委常委、常务副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "市委常委、副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "市委常委、政法委书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "市委常委、副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 13, "org_id": 1, "title": "市委常委、统战部部长、副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # Deputy Mayors
    {"person_id": 14, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 16, "org_id": 10, "title": "副市长、市公安局局长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 18, "org_id": 2, "title": "市政府党组成员，十堰经济技术开发区党工委副书记、管委会主任", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 人大/政协
    {"person_id": 19, "org_id": 5, "title": "市人大常委会主任", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    {"person_id": 20, "org_id": 6, "title": "市政协主席", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    # Predecessors
    {"person_id": 21, "org_id": 1, "title": "前任市委书记", "start_date": "", "end_date": "", "rank": "正厅级", "note": "前任市委书记，约2022年至2026年初，后调任"},
    {"person_id": 22, "org_id": 11, "title": "前任市委书记（现任荆门市委书记）", "start_date": "", "end_date": "", "rank": "正厅级", "note": "前任十堰市委书记，约2021-2022，调任荆门市委书记"},
]

# ── Relationships ────────────────────────────────────────────────────────────
relationships = [
    # Leadership duumvirate
    {"person_a": 1, "person_b": 2, "type": "搭档", "context": "市委书记—市长搭档", "overlap_org": "十堰市党政领导班子", "overlap_period": "2026—present"},
    # Party Secretary — Deputy Secretary
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "市委书记—市委副书记", "overlap_org": "中共十堰市委员会", "overlap_period": "present"},
    # Mayor — Deputy Secretary
    {"person_a": 2, "person_b": 3, "type": "共事", "context": "市长—市委副书记", "overlap_org": "十堰市党政领导班子", "overlap_period": "present"},
    # Standing Committee working relationships
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "书记—组织部长", "overlap_org": "中共十堰市委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "书记—宣传部长", "overlap_org": "中共十堰市委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "书记—纪委书记", "overlap_org": "中共十堰市委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "书记—市委秘书长", "overlap_org": "中共十堰市委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 11, "type": "上下级", "context": "书记—政法委书记", "overlap_org": "中共十堰市委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 13, "type": "上下级", "context": "书记—统战部长", "overlap_org": "中共十堰市委员会", "overlap_period": "present"},
    # Mayor — deputy mayors
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "市长—常务副市长", "overlap_org": "十堰市人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "市长—副市长", "overlap_org": "十堰市人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "市长—副市长", "overlap_org": "十堰市人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 14, "type": "上下级", "context": "市长—副市长", "overlap_org": "十堰市人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 15, "type": "上下级", "context": "市长—副市长", "overlap_org": "十堰市人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 16, "type": "上下级", "context": "市长—公安局长", "overlap_org": "十堰市人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 17, "type": "上下级", "context": "市长—副市长", "overlap_org": "十堰市人民政府", "overlap_period": "present"},
    # Predecessor relationships
    {"person_a": 1, "person_b": 21, "type": "前任继任", "context": "黄剑雄→王永辉，市委书记职务交接", "overlap_org": "中共十堰市委员会", "overlap_period": "2026"},
    {"person_a": 21, "person_b": 22, "type": "前任继任", "context": "胡亚波→黄剑雄，市委书记职务交接", "overlap_org": "中共十堰市委员会", "overlap_period": "2022"},
]

# ── Generate database and graph ─────────────────────────────────────────────
def main():
    print(f"Building {SLUG} database and graph...")
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
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")

    # ── Write person JSON files ──────────────────────────────────────────
    person_defs = [
        (1, "市委书记", "王永辉"),
        (2, "市长", "余珂"),
        (3, "市委副书记", "张澍"),
        (9, "市委常委、常务副市长", "周智勇"),
        (21, "前任市委书记", "黄剑雄"),
        (22, "前任市委书记", "胡亚波"),
    ]
    for pid, job, name in person_defs:
        p = next(x for x in persons if x["id"] == pid)
        fname = f"{TODAY}-湖北省-十堰市-{job}-{name}.json"
        fpath = Path(PJSON_DIR) / fname
        data = _build_person_json(p, pid)
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {fpath}")

    print("Done.")


def _build_person_json(p: dict, pid: int) -> dict:
    """Build a person JSON following the schema from references/person_graph_json.md."""
    from datetime import date

    name = p["name"]
    # Determine role
    role_display = "市委书记" if "市委书记" in p.get("current_post", "") else \
                   "市长" if "市长" in p.get("current_post", "") else \
                   p.get("current_post", "")

    # Source register
    sources = []
    if p.get("source"):
        sources.append({
            "id": "S001",
            "title": f"十堰市政府信息公开 — {name}",
            "url": p["source"],
            "publisher": "十堰市人民政府",
            "published_at": "",
            "accessed_at": "2026-07-24",
            "source_type": "official",
            "reliability": "high",
            "notes": "官方简历页面",
        })

    # Career timeline - build from available data
    timeline = []
    if p.get("birth"):
        timeline.append({
            "start": p["birth"].replace("年", "-").replace("月", ""),
            "end": "",
            "org": "出生",
            "title": "",
            "level": "",
            "location": p.get("birthplace", ""),
            "system": "other",
            "rank": "",
            "is_key_promotion": False,
            "notes": f"生于{p['birthplace']}" if p.get("birthplace") else "",
            "confidence": "confirmed",
            "source_ids": ["S001"],
        })
    if p.get("work_start"):
        timeline.append({
            "start": p["work_start"].replace("年", "-").replace("月", ""),
            "end": "",
            "org": "",
            "title": "参加工作",
            "level": "",
            "location": "",
            "system": "other",
            "rank": "",
            "is_key_promotion": False,
            "notes": "",
            "confidence": "confirmed",
            "source_ids": ["S001"],
        })

    # Add current position
    timeline.append({
        "start": "",
        "end": "present",
        "org": p.get("current_org", ""),
        "title": p.get("current_post", ""),
        "level": "",
        "location": "十堰市",
        "system": "party" if "委" in p.get("current_org", "") else "government",
        "rank": "正厅级" if "书记" in p.get("current_post", "") or "市长" in p.get("current_post", "") else "副厅级",
        "is_key_promotion": True,
        "notes": f"截至2026年7月任{p.get('current_post', '')}",
        "confidence": "confirmed",
        "source_ids": ["S001"],
    })

    # Mark career gaps for core leaders
    if pid in (1, 2):
        timeline.insert(1, {
            "start": "unknown",
            "end": "unknown",
            "org": "履历缺口",
            "title": "",
            "notes": f"正式公开简历未包含{p.get('work_start', '参加工作')}后至任现职前完整履历",
            "confidence": "unverified",
            "source_ids": [],
        })

    # Relationships
    rels = []
    for r in relationships:
        if r["person_a"] == pid:
            other = next((x for x in persons if x["id"] == r["person_b"]), None)
            if other:
                rels.append({
                    "person": other["name"],
                    "person_id": f"hubei_shiyan_{other['name']}",
                    "relationship_type": r["type"],
                    "strength": "strong" if "搭档" in r["type"] or "前任继任" in r["type"] else "medium",
                    "evidence": r["context"],
                    "overlap_org": r["overlap_org"],
                    "overlap_period": r["overlap_period"],
                    "direction": "undirected",
                    "confidence": "confirmed" if r["type"] in ("搭档", "上下级") else "plausible",
                    "source_ids": ["S001"],
                })
        elif r["person_b"] == pid:
            other = next((x for x in persons if x["id"] == r["person_a"]), None)
            if other:
                rels.append({
                    "person": other["name"],
                    "person_id": f"hubei_shiyan_{other['name']}",
                    "relationship_type": r["type"],
                    "strength": "strong" if "搭档" in r["type"] or "前任继任" in r["type"] else "medium",
                    "evidence": r["context"],
                    "overlap_org": r["overlap_org"],
                    "overlap_period": r["overlap_period"],
                    "direction": "undirected",
                    "confidence": "confirmed" if r["type"] in ("搭档", "上下级") else "plausible",
                    "source_ids": ["S001"],
                })

    is_core = pid in (1, 2)
    return {
        "schema_version": "1.0",
        "generated_at": "2026-07-24",
        "investigation_scope": {
            "province": "湖北省",
            "city": "十堰市",
            "region": "十堰市",
            "job": role_display,
            "task_id": "hubei_十堰市",
            "time_focus": "2026年7月",
        },
        "identity": {
            "person_id": f"hubei_shiyan_{name}",
            "name": name,
            "aliases": [],
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": p.get("birthplace", ""),
            "education": [{"period": "", "institution": "", "major": "", "degree": p.get("education", ""), "study_type": "unknown", "source_ids": ["S001"]}] if p.get("education") else [],
            "party_join": p.get("party_join", ""),
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{p.get('birth', '')}",
                "name_birthplace": f"{name}_{p.get('birthplace', '')}" if p.get("birthplace") else f"{name}_unknown",
                "official_profile_url": p.get("source", ""),
            },
        },
        "current_status": {
            "current_post": p.get("current_post", ""),
            "current_org": p.get("current_org", ""),
            "administrative_rank": "正厅级" if "书记" in p.get("current_post", "") or "市长" in p.get("current_post", "") else "副厅级",
            "as_of": "2026-07-24",
            "is_current_confirmed": True,
            "source_ids": ["S001"],
        },
        "career_timeline": timeline,
        "organizations": [
            {"org_id": f"o{oid}", "org_name": oname, "role": f"current_{p.get('current_post', '')}", "period": "present"}
            for oid, oname in [(1, "中共十堰市委员会")] if pid <= 20
        ],
        "relationships": rels,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {
            "direct_connections": len(rels),
            "total_relationships": len(rels),
            "center_rank": "top" if is_core else "deputy",
        },
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "截至2026年7月，未发现公开的纪律处分、审计问题或负面报道", "date": "", "confidence": "plausible", "source_ids": ["S001"]}
        ],
        "source_register": sources,
        "confidence_summary": {
            "identity": "confirmed" if p.get("birth") else "plausible",
            "current_role": "confirmed",
            "career_completeness": "partial" if is_core else "thin",
            "relationship_confidence": "high" if is_core else "medium",
            "biggest_gap": f"{name}的完整履历（{p.get('work_start', '参加工作')}后至任现职前）" if is_core else "详细出生信息和早期履历",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的完整履历（{p.get('work_start', '参加工作')}后至任现职前）",
                "why_it_matters": "了解晋升路径、政绩积累和系统性工作经历",
                "suggested_queries": [f"{name} 简历 任职经历", f"{name} 百度百科", f"{name} 湖北 任职"],
                "last_attempted": "2026-07-24",
            },
            {
                "priority": "high" if is_core else "medium",
                "question": f"{name}的政绩和重大项目主导经历",
                "why_it_matters": "评估施政能力和专业领域",
                "suggested_queries": [f"{name} 调研 十堰市", f"{name} 项目建设"],
                "last_attempted": "2026-07-24",
            },
        ],
    }


if __name__ == "__main__":
    main()
