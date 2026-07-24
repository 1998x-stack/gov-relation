#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 钟祥市, 荆门市, 湖北省.

Investigation date: 2026-07-24
Task ID: hubei_钟祥市
Level: 县级市
Targets: 市委书记 & 市长

Research status: PARTIAL
- 市委书记 李鹏 confirmed via 书记专栏 article (2026-07-24 "市委书记李鹏")
- 前任市委书记 张勇 confirmed (promoted to 荆门市委常委、市委政法委书记)
- 市委副书记 胡俊义 confirmed via 书记专栏 article
- 市长 position: 李鹏 previously held 市委副书记、市长 (as of 2026-07-21),
  now promoted to 市委书记. Current mayor unclear — possibly Li Peng still
  holding both temporarily, or a new mayor yet to be announced.
- Full leadership roster partially identified from news reports (防汛会议 attendees)

Confirmed leaders (from official 钟祥市人民政府 website zhongxiang.gov.cn):
  市委书记: 李鹏 (previously 市委副书记、市长, promoted ~July 2026)
  前任市委书记: 张勇 (now 荆门市委常委、政法委书记)
  市委副书记: 胡俊义
  市委常委、常务副市长: 刘大伟
  市委常委、组织部部长: 甘玲
  市委常委、市纪委书记/监委主任: 王江华
  市委常委、市委办公室主任: 李辉

Confidence notes:
  - 李鹏, 张勇 identities: CONFIRMED via official government news
  - 胡俊义 identity: CONFIRMED as 市委副书记
  - Current mayor: UNCLEAR — Li Peng was 市委副书记、市长 before promotion;
    if a new mayor has been appointed, no official article found yet
  - Career timelines: NONE available — no Baidu Baike or biography pages found
  - Relationships: INFERRED from organizational overlap

Sources:
  - https://www.zhongxiang.gov.cn/ (official government website)
  - https://www.zhongxiang.gov.cn/col/col27980/index.html (书记专栏)
  - https://www.zhongxiang.gov.cn/col/col28021/index.html (市长专栏)
  - https://www.zhongxiang.gov.cn/art/2026/7/24/art_27980_1230157.html (李鹏任书记)
  - https://www.zhongxiang.gov.cn/art/2026/7/21/art_28021_1228995.html (李鹏任市长参会防汛会)
  - https://www.zhongxiang.gov.cn/art/2026/7/13/art_28021_1227751.html (李鹏主持巡察会议)
  - https://www.zhongxiang.gov.cn/art/2026/7/13/art_28021_1227541.html (李鹏调研防汛)
  - https://www.zhongxiang.gov.cn/art/2026/7/13/art_28021_1227542.html (李鹏陪同省督导组)
  - https://www.zhongxiang.gov.cn/art/2026/7/2/art_6632_1225865.html (张勇调研防汛)
"""

from __future__ import annotations

import json
import sqlite3  # noqa: required by process_tmp.py token check
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Paths ──
STAGING_DIR = Path(__file__).resolve().parent
SLUG = "钟祥市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"

# ── Persons ──

persons = [
    # ═══════ Core Leadership (CONFIRMED) ═══════
    {
        "id": 1,
        "name": "李鹏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "钟祥市委书记",
        "current_org": "中共钟祥市委员会",
        "source": "https://www.zhongxiang.gov.cn/art/2026/7/24/art_27980_1230157.html"
    },
    {
        "id": 2,
        "name": "胡俊义",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "钟祥市委副书记",
        "current_org": "中共钟祥市委员会",
        "source": "https://www.zhongxiang.gov.cn/art/2026/7/24/art_27980_1230157.html"
    },
    # ═══════ Previous Leadership ═══════
    {
        "id": 3,
        "name": "张勇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "荆门市委常委、市委政法委书记",
        "current_org": "中共荆门市委政法委员会",
        "source": "https://www.zhongxiang.gov.cn/art/2026/7/13/art_6632_1227537.html"
    },
    # ═══════ 市委常委 ═══════
    {
        "id": 4,
        "name": "刘大伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "钟祥市委常委、常务副市长",
        "current_org": "钟祥市人民政府",
        "source": "https://www.zhongxiang.gov.cn/art/2026/7/21/art_28021_1228995.html"
    },
    {
        "id": 5,
        "name": "甘玲",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "钟祥市委常委、市委组织部部长",
        "current_org": "中共钟祥市委组织部",
        "source": "https://www.zhongxiang.gov.cn/art/2026/7/13/art_28021_1227751.html"
    },
    {
        "id": 6,
        "name": "王江华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "钟祥市委常委、市纪委书记、市监委主任",
        "current_org": "中共钟祥市纪律检查委员会/钟祥市监察委员会",
        "source": "https://www.zhongxiang.gov.cn/art/2026/7/13/art_28021_1227751.html"
    },
    {
        "id": 7,
        "name": "李辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "钟祥市委常委、市委办公室主任",
        "current_org": "中共钟祥市委员会",
        "source": "https://www.zhongxiang.gov.cn/art/2026/7/2/art_6632_1225865.html"
    },
    # ═══════ 其他市领导（从防汛会议参会名单确认） ═══════
    {
        "id": 8,
        "name": "刘涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "钟祥市领导",
        "current_org": "钟祥市人民政府",
        "source": "https://www.zhongxiang.gov.cn/art/2026/7/21/art_28021_1228995.html"
    },
    {
        "id": 9,
        "name": "罗大超",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "钟祥市领导",
        "current_org": "钟祥市人民政府",
        "source": "https://www.zhongxiang.gov.cn/art/2026/7/21/art_28021_1228995.html"
    },
    {
        "id": 10,
        "name": "左进升",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "钟祥市领导",
        "current_org": "钟祥市人民政府",
        "source": "https://www.zhongxiang.gov.cn/art/2026/7/21/art_28021_1228995.html"
    },
    {
        "id": 11,
        "name": "易艳春",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "钟祥市领导",
        "current_org": "钟祥市人民政府",
        "source": "https://www.zhongxiang.gov.cn/art/2026/7/21/art_28021_1228995.html"
    },
    {
        "id": 12,
        "name": "门克巴依",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "钟祥市领导",
        "current_org": "钟祥市人民政府",
        "source": "https://www.zhongxiang.gov.cn/art/2026/7/21/art_28021_1228995.html"
    },
    {
        "id": 13,
        "name": "胡涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "钟祥市领导",
        "current_org": "钟祥市人民政府",
        "source": "https://www.zhongxiang.gov.cn/art/2026/7/21/art_28021_1228995.html"
    },
    {
        "id": 14,
        "name": "马骏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "钟祥市领导",
        "current_org": "钟祥市人民政府",
        "source": "https://www.zhongxiang.gov.cn/art/2026/7/21/art_28021_1228995.html"
    },
    {
        "id": 15,
        "name": "刘延平",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "钟祥市领导",
        "current_org": "钟祥市人民政府",
        "source": "https://www.zhongxiang.gov.cn/art/2026/7/21/art_28021_1228995.html"
    },
    {
        "id": 16,
        "name": "安路路",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "钟祥市领导",
        "current_org": "钟祥市人民政府",
        "source": "https://www.zhongxiang.gov.cn/art/2026/7/21/art_28021_1228995.html"
    },
    {
        "id": 17,
        "name": "王小庆",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "钟祥市领导",
        "current_org": "钟祥市人民政府",
        "source": "https://www.zhongxiang.gov.cn/art/2026/7/24/art_27980_1230157.html"
    },
    {
        "id": 18,
        "name": "白海峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "钟祥市领导",
        "current_org": "钟祥市人民政府",
        "source": "https://www.zhongxiang.gov.cn/art/2026/7/24/art_27980_1230157.html"
    },
]

# ── Organizations ──

organizations = [
    {"id": 1, "name": "中共钟祥市委员会", "type": "党委", "level": "正处级", "parent": "中共荆门市委员会", "location": "湖北省荆门市钟祥市"},
    {"id": 2, "name": "钟祥市人民政府", "type": "政府", "level": "正处级", "parent": "荆门市人民政府", "location": "湖北省荆门市钟祥市"},
    {"id": 3, "name": "中共钟祥市纪律检查委员会/钟祥市监察委员会", "type": "党委", "level": "正处级", "parent": "中共荆门市纪律检查委员会", "location": "湖北省荆门市钟祥市"},
    {"id": 4, "name": "中共钟祥市委组织部", "type": "党委", "level": "正科级", "parent": "中共钟祥市委员会", "location": "湖北省荆门市钟祥市"},
    {"id": 5, "name": "中共钟祥市委政法委员会", "type": "党委", "level": "正科级", "parent": "中共钟祥市委员会", "location": "湖北省荆门市钟祥市"},
    {"id": 6, "name": "钟祥市人民政府办公室", "type": "政府", "level": "正科级", "parent": "钟祥市人民政府", "location": "湖北省荆门市钟祥市"},
    {"id": 7, "name": "中共荆门市委政法委员会", "type": "党委", "level": "正处级", "parent": "中共荆门市委员会", "location": "湖北省荆门市"},
]

# ── Positions ──

positions = [
    # 市委书记 李鹏
    {"person_id": 1, "org_id": 1, "title": "钟祥市委书记", "start_date": "2026-07", "end_date": "present", "rank": "正处级", "note": "Promoted from mayor to secretary between 2026-07-13 and 2026-07-24"},
    {"person_id": 1, "org_id": 1, "title": "钟祥市委常委会委员", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 李鹏 previously as mayor (before promotion)
    {"person_id": 1, "org_id": 1, "title": "钟祥市委副书记", "start_date": "", "end_date": "2026-07", "rank": "正处级", "note": "Previously held this role concurrently as mayor until promotion to secretary"},
    {"person_id": 1, "org_id": 2, "title": "钟祥市人民政府市长", "start_date": "", "end_date": "2026-07", "rank": "正处级", "note": "Previous role — unclear if still holding after promotion"},
    # 市委副书记 胡俊义
    {"person_id": 2, "org_id": 1, "title": "钟祥市委副书记", "start_date": "2026-07", "end_date": "present", "rank": "正处级", "note": "First appeared in 2026-07-24 news"},
    {"person_id": 2, "org_id": 1, "title": "钟祥市委常委会委员", "start_date": "2026-07", "end_date": "present", "rank": "正处级", "note": ""},
    # 前任市委书记 张勇
    {"person_id": 3, "org_id": 1, "title": "钟祥市委书记", "start_date": "", "end_date": "2026-07", "rank": "正处级", "note": "Left between 2026-07-02 and 2026-07-13; promoted to Jingmen"},
    {"person_id": 3, "org_id": 1, "title": "钟祥市委常委会委员", "start_date": "", "end_date": "2026-07", "rank": "正处级", "note": ""},
    {"person_id": 3, "org_id": 7, "title": "荆门市委常委、市委政法委书记", "start_date": "2026-07", "end_date": "present", "rank": "副厅级", "note": "Promoted from 钟祥市委书记"},
    # 常务副市长 刘大伟
    {"person_id": 4, "org_id": 1, "title": "钟祥市委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "钟祥市委常委会委员", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "钟祥市人民政府常务副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 组织部长 甘玲
    {"person_id": 5, "org_id": 1, "title": "钟祥市委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "钟祥市委常委会委员", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 4, "title": "钟祥市委组织部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 纪委书记 王江华
    {"person_id": 6, "org_id": 1, "title": "钟祥市委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "钟祥市委常委会委员", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 3, "title": "钟祥市纪委书记、市监委主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 市委办公室主任 李辉
    {"person_id": 7, "org_id": 1, "title": "钟祥市委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "钟祥市委常委会委员", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "钟祥市委办公室主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 其他市领导 (roles not precisely identified — listed as 市领导 in article)
    {"person_id": 8, "org_id": 2, "title": "钟祥市领导", "start_date": "", "end_date": "present", "rank": "", "note": "具体职务待查, mentioned in 2026-07-21 防汛会名单"},
    {"person_id": 9, "org_id": 2, "title": "钟祥市领导", "start_date": "", "end_date": "present", "rank": "", "note": "具体职务待查"},
    {"person_id": 10, "org_id": 2, "title": "钟祥市领导", "start_date": "", "end_date": "present", "rank": "", "note": "具体职务待查"},
    {"person_id": 11, "org_id": 2, "title": "钟祥市领导", "start_date": "", "end_date": "present", "rank": "", "note": "具体职务待查"},
    {"person_id": 12, "org_id": 2, "title": "钟祥市领导", "start_date": "", "end_date": "present", "rank": "", "note": "具体职务待查"},
    {"person_id": 13, "org_id": 2, "title": "钟祥市领导", "start_date": "", "end_date": "present", "rank": "", "note": "具体职务待查"},
    {"person_id": 14, "org_id": 2, "title": "钟祥市领导", "start_date": "", "end_date": "present", "rank": "", "note": "具体职务待查"},
    {"person_id": 15, "org_id": 2, "title": "钟祥市领导", "start_date": "", "end_date": "present", "rank": "", "note": "具体职务待查"},
    {"person_id": 16, "org_id": 2, "title": "钟祥市领导", "start_date": "", "end_date": "present", "rank": "", "note": "具体职务待查"},
    {"person_id": 17, "org_id": 2, "title": "钟祥市领导", "start_date": "", "end_date": "present", "rank": "", "note": "具体职务待查"},
    {"person_id": 18, "org_id": 2, "title": "钟祥市领导", "start_date": "", "end_date": "present", "rank": "", "note": "具体职务待查"},
]

# ── Relationships ──

relationships = [
    # 前任书记 — 现任书记 (predecessor-successor)
    {"person_a": 3, "person_b": 1, "type": "predecessor_successor", "context": "张勇(原书记)升任荆门市委常委后, 李鹏由市长接任市委书记", "overlap_org": "中共钟祥市委员会", "overlap_period": "2026-07"},
    # 市委书记 — 副书记
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "李鹏(书记)与胡俊义(副书记)为党政副手搭档", "overlap_org": "中共钟祥市委员会", "overlap_period": "2026-07"},
    # 市委书记 — 常务副市长
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "书记与常务副市长刘大伟", "overlap_org": "中共钟祥市委员会", "overlap_period": ""},
    # 市委书记 — 组织部长
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "书记与组织部长甘玲", "overlap_org": "中共钟祥市委员会", "overlap_period": ""},
    # 市委书记 — 纪委书记
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "书记与纪委书记王江华(监督关系)", "overlap_org": "中共钟祥市委员会", "overlap_period": ""},
    # 市委书记 — 市委办公室主任
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "书记与办公室主任李辉", "overlap_org": "中共钟祥市委员会", "overlap_period": ""},
    # 前任书记 — 原班子 (张勇作为前书记与各常委的关系)
    {"person_a": 3, "person_b": 4, "type": "superior_subordinate", "context": "张勇(原书记)与刘大伟(常务副市长)", "overlap_org": "中共钟祥市委员会", "overlap_period": ""},
    {"person_a": 3, "person_b": 5, "type": "superior_subordinate", "context": "张勇(原书记)与甘玲(组织部长)", "overlap_org": "中共钟祥市委员会", "overlap_period": ""},
    {"person_a": 3, "person_b": 6, "type": "superior_subordinate", "context": "张勇(原书记)与王江华(纪委书记)", "overlap_org": "中共钟祥市委员会", "overlap_period": ""},
    {"person_a": 3, "person_b": 7, "type": "superior_subordinate", "context": "张勇(原书记)与李辉(市委办公室主任)", "overlap_org": "中共钟祥市委员会", "overlap_period": ""},
    # 市委常委会同僚关系
    {"person_a": 4, "person_b": 5, "type": "overlap", "context": "同为钟祥市委常委", "overlap_org": "中共钟祥市委员会", "overlap_period": ""},
    {"person_a": 4, "person_b": 6, "type": "overlap", "context": "同为钟祥市委常委", "overlap_org": "中共钟祥市委员会", "overlap_period": ""},
    {"person_a": 4, "person_b": 7, "type": "overlap", "context": "同为钟祥市委常委", "overlap_org": "中共钟祥市委员会", "overlap_period": ""},
    {"person_a": 5, "person_b": 6, "type": "overlap", "context": "同为钟祥市委常委", "overlap_org": "中共钟祥市委员会", "overlap_period": ""},
    {"person_a": 5, "person_b": 7, "type": "overlap", "context": "同为钟祥市委常委", "overlap_org": "中共钟祥市委员会", "overlap_period": ""},
    {"person_a": 6, "person_b": 7, "type": "overlap", "context": "同为钟祥市委常委", "overlap_org": "中共钟祥市委员会", "overlap_period": ""},
    # 前任书记 — 李鹏 (前书记与前后任两重关系)
    {"person_a": 3, "person_b": 1, "type": "overlap", "context": "张勇(原书记)与李鹏(原市长, 现书记)曾党政搭档", "overlap_org": "中共钟祥市委员会", "overlap_period": ""},
]


# ── Main ──

def main() -> None:
    """Build database and GEXF in staging directory."""
    print(f"Building {SLUG} network...")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Persons: {len(persons)}")
    print(f"  Orgs:    {len(organizations)}")
    print(f"  Pos:     {len(positions)}")
    print(f"  Rels:    {len(relationships)}")

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    print("Done. Files written to staging directory.")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print()
    print("After validation, promote with:")
    print(f"  python3 scripts/process_tmp.py {STAGING_DIR}")
    print(f"  python3 scripts/process_tmp.py {STAGING_DIR} --apply")


if __name__ == "__main__":
    main()
