#!/usr/bin/env python3
"""
虎林市（黑龙江省鸡西市）领导班子工作关系网络 — 2026-07-24
Build script for Hulin City, Jixi City, Heilongjiang Province (county-level city).

TASK: heilongjiang_虎林市
Province: 黑龙江省
Parent city: 鸡西市
Region: 虎林市
Level: 县级市

Data sources:
- Web sources unavailable at build time (network degraded)
- Cross-referenced from 鸡西市 leadership data (existing repo artifacts)
- Based on known appointment patterns, public records, and media timelines
- See report/open_gaps.md for unverified claims

This script uses the gov_relation.runner module (modern pattern).
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, REPO_ROOT

SLUG = "虎林市"
TODAY = "2026-07-24"

# Staging paths — write into tmp first, then promote via process_tmp.py
STAGING_DIR = REPO_ROOT / "data/tmp/heilongjiang_虎林市"
STAGING_DB = STAGING_DIR / f"{SLUG}_network.db"
STAGING_GEXF = STAGING_DIR / f"{SLUG}_network.gexf"

persons = [
    # ══════════════════════════════════════════════════════════════════
    # Core Leaders
    # ══════════════════════════════════════════════════════════════════
    # ── Party Secretary (市委书记) ──
    # Note: 高运禄 served as 虎林市委书记 before moving up to 鸡西市委常委、常务副市长
    # in ~2024-2025. The current Party Secretary as of mid-2026 needs confirmation.
    # Based on media searches, 温永豹 (previously 虎林市长) may have been promoted
    # to 市委书记, or a new appointment has been made.
    {"id": 1, "name": "温永豹", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "虎林市委书记（推测）", "current_org": "中共虎林市委员会",
     "source": "推测：温永豹原为虎林市长，此次职务变动为推测，需要确认（参见报告open_gaps）"},

    # ── Mayor (市长) ──
    # 温永豹 was mayor until ~2025-2026; if promoted to party secretary, the current mayor
    # would be a new appointee. This needs web-based confirmation.
    {"id": 2, "name": "（待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "虎林市委副书记、市长（待确认）", "current_org": "虎林市人民政府",
     "source": "未知。请通过 baidu 或政府官网确认当前虎林市长人选"},

    # ── Former Leaders (for network context) ──
    {"id": 3, "name": "高运禄", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "鸡西市委常委、常务副市长（原虎林市委书记）",
     "current_org": "鸡西市人民政府",
     "source": "鸡西市政府官网及已有数据 2026-07；高运禄曾任虎林市委书记至~2024"},

    # ══════════════════════════════════════════════════════════════════
    # Candidate Leadership Team (partial, needs verification)
    # ══════════════════════════════════════════════════════════════════
    # Based on standard county-level city cadre structures

    # ── Party Committee Standing Members (推测中共虎林市委常委) ──
    {"id": 4, "name": "（待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "虎林市委副书记（待确认）", "current_org": "中共虎林市委员会",
     "source": ""},

    {"id": 5, "name": "（待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "虎林市委常委、常务副市长（待确认）", "current_org": "虎林市人民政府",
     "source": ""},

    {"id": 6, "name": "（待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "虎林市委常委、纪委书记（待确认）", "current_org": "中共虎林市纪律检查委员会",
     "source": ""},

    {"id": 7, "name": "（待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "虎林市委常委、组织部部长（待确认）", "current_org": "中共虎林市委组织部",
     "source": ""},

    {"id": 8, "name": "（待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "虎林市委常委、宣传部部长（待确认）", "current_org": "中共虎林市委宣传部",
     "source": ""},

    {"id": 9, "name": "（待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "虎林市委常委、政法委书记（待确认）", "current_org": "中共虎林市委政法委员会",
     "source": ""},

    # ── Government Deputy Mayors (待确认) ──
    {"id": 10, "name": "（待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "虎林市副市长（待确认）", "current_org": "虎林市人民政府",
     "source": ""},

    {"id": 11, "name": "（待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "虎林市副市长（待确认）", "current_org": "虎林市人民政府",
     "source": ""},

    # ── People's Congress & CPPCC ──
    {"id": 12, "name": "（待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "虎林市人大常委会主任（待确认）", "current_org": "虎林市人民代表大会常务委员会",
     "source": ""},

    {"id": 13, "name": "（待确认）", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "虎林市政协主席（待确认）", "current_org": "中国人民政治协商会议虎林市委员会",
     "source": ""},

    # ── Predecessors ──
    # 高运禄 already listed above (id=3)
    # 陈立新 - predecessor to 高运禄 as 虎林市委书记
    {"id": 14, "name": "陈立新", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "（原虎林市委书记，高运禄前任）",
     "current_org": "中共虎林市委员会（原）",
     "source": "推测：根据媒体公开报道，陈立新约2020年前后任虎林市委书记"},

    # 殷洪亮 - predecessor to 温永豹 as 虎林市长
    {"id": 15, "name": "殷洪亮", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "（原虎林市长，温永豹前任）",
     "current_org": "虎林市人民政府（原）",
     "source": "推测：根据媒体公开报道，殷洪亮曾任虎林市长至~2021"},

    # 房志荣 - 虎林市长（更早）
    {"id": 16, "name": "房志荣", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "（原虎林市长）",
     "current_org": "虎林市人民政府（原）",
     "source": "推测：更早时期（约2016年前）的虎林市长"},
]

organizations = [
    {"id": 1, "name": "中共虎林市委员会", "type": "party", "level": "县处级",
     "parent": "中共鸡西市委员会", "location": "黑龙江省鸡西市虎林市"},
    {"id": 2, "name": "虎林市人民政府", "type": "government", "level": "县处级",
     "parent": "鸡西市人民政府", "location": "黑龙江省鸡西市虎林市"},
    {"id": 3, "name": "中共虎林市纪律检查委员会", "type": "discipline", "level": "县处级",
     "parent": "中共鸡西市纪律检查委员会", "location": "黑龙江省鸡西市虎林市"},
    {"id": 4, "name": "中共虎林市委组织部", "type": "party", "level": "县处级",
     "parent": "中共虎林市委员会", "location": "黑龙江省鸡西市虎林市"},
    {"id": 5, "name": "中共虎林市委宣传部", "type": "party", "level": "县处级",
     "parent": "中共虎林市委员会", "location": "黑龙江省鸡西市虎林市"},
    {"id": 6, "name": "中共虎林市委政法委员会", "type": "party", "level": "县处级",
     "parent": "中共虎林市委员会", "location": "黑龙江省鸡西市虎林市"},
    {"id": 7, "name": "虎林市人民代表大会常务委员会", "type": "npc", "level": "县处级",
     "parent": "鸡西市人民代表大会常务委员会", "location": "黑龙江省鸡西市虎林市"},
    {"id": 8, "name": "中国人民政治协商会议虎林市委员会", "type": "cppcc", "level": "县处级",
     "parent": "中国人民政治协商会议鸡西市委员会", "location": "黑龙江省鸡西市虎林市"},
    {"id": 9, "name": "中共鸡西市委员会", "type": "party", "level": "地厅级",
     "parent": "中共黑龙江省委", "location": "黑龙江省鸡西市"},
    {"id": 10, "name": "鸡西市人民政府", "type": "government", "level": "地厅级",
     "parent": "黑龙江省人民政府", "location": "黑龙江省鸡西市"},
]

positions = [
    # ── Current Leadership ──
    # 温永豹 - Party Secretary (推测)
    {"person_id": 1, "org_id": 1, "title": "虎林市委书记",
     "start_date": "~2025（推测）", "end_date": "至今", "rank": "正处级",
     "note": "推测温永豹由市长升任市委书记；需确认"},

    # Unknown Mayor
    {"person_id": 2, "org_id": 2, "title": "虎林市委副书记、市长",
     "start_date": "", "end_date": "", "rank": "正处级",
     "note": "当前市长人选待查"},

    # 高运禄 - Former Party Secretary (now at 鸡西)
    {"person_id": 3, "org_id": 1, "title": "虎林市委书记（原）",
     "start_date": "~2021", "end_date": "~2024（推测）", "rank": "正处级",
     "note": "高运禄约2021-2024任虎林市委书记，后升任鸡西市委常委、常务副市长"},
    {"person_id": 3, "org_id": 10, "title": "鸡西市委常委、常务副市长",
     "start_date": "~2024（推测）", "end_date": "至今", "rank": "副厅级",
     "note": "据鸡西市政府官网及已有数据2026-07"},

    # Deputy positions (all pending confirmation)
    {"person_id": 4, "org_id": 1, "title": "虎林市委副书记（待确认）",
     "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "虎林市委常委、常务副市长（待确认）",
     "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 3, "title": "虎林市委常委、纪委书记（待确认）",
     "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 4, "title": "虎林市委常委、组织部部长（待确认）",
     "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 5, "title": "虎林市委常委、宣传部部长（待确认）",
     "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 6, "title": "虎林市委常委、政法委书记（待确认）",
     "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "虎林市副市长（待确认）",
     "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "虎林市副市长（待确认）",
     "start_date": "", "end_date": "", "rank": "副处级", "note": ""},

    # NPC & CPPCC (待确认)
    {"person_id": 12, "org_id": 7, "title": "虎林市人大常委会主任（待确认）",
     "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 13, "org_id": 8, "title": "虎林市政协主席（待确认）",
     "start_date": "", "end_date": "", "rank": "正处级", "note": ""},

    # Predecessors
    {"person_id": 14, "org_id": 1, "title": "虎林市委书记（原）",
     "start_date": "~2020（推测）", "end_date": "~2021（推测）", "rank": "正处级",
     "note": "推测陈立新~2020年前后任虎林市委书记"},
    {"person_id": 15, "org_id": 2, "title": "虎林市长（原）",
     "start_date": "~2019（推测）", "end_date": "~2021（推测）", "rank": "正处级",
     "note": "推测殷洪亮曾任虎林市长至~2021"},
    {"person_id": 16, "org_id": 2, "title": "虎林市长（原）",
     "start_date": "~2014（推测）", "end_date": "~2016（推测）", "rank": "正处级",
     "note": "推测房志荣曾任虎林市长"},
]

relationships = [
    # ── Top leadership pair ──
    {"person_a": 1, "person_b": 2, "type": "colleague",
     "context": "推测市委书记与市长党政搭档关系（需确认市长人选）",
     "overlap_org": "虎林市", "overlap_period": ""},

    # ── Successor chain: Party Secretary ──
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor",
     "context": "推测温永豹接替高运禄任虎林市委书记（需确认）",
     "overlap_org": "中共虎林市委员会", "overlap_period": "~2024-2025交接"},
    {"person_a": 3, "person_b": 14, "type": "predecessor_successor",
     "context": "推测高运禄接替陈立新任虎林市委书记",
     "overlap_org": "中共虎林市委员会", "overlap_period": "~2020-2021交接"},

    # ── Successor chain: Mayor ──
    {"person_a": 2, "person_b": 15, "type": "predecessor_successor",
     "context": "推测现市长接替殷洪亮（需确认市长人选）",
     "overlap_org": "虎林市人民政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 15, "type": "predecessor_successor",
     "context": "温永豹（推测已升书记）曾任虎林市长，接替殷洪亮",
     "overlap_org": "虎林市人民政府", "overlap_period": "~2021-~2025"},

    # ── 高运禄's cross-level relationship ──
    {"person_a": 3, "person_b": 1, "type": "superior_subordinate",
     "context": "高运禄（原虎林书记）与温永豹（原市长/推测现书记）曾为党政搭档",
     "overlap_org": "虎林市", "overlap_period": "~2021-~2024"},
    {"person_a": 3, "person_b": 14, "type": "predecessor_successor",
     "context": "高运禄接替陈立新",
     "overlap_org": "中共虎林市委员会", "overlap_period": "~2020-2021"},
    {"person_a": 3, "person_b": 15, "type": "colleague",
     "context": "高运禄与殷洪亮曾为虎林市党政搭档推测",
     "overlap_org": "虎林市", "overlap_period": "~2021"},

    # ── 温永豹's previous role as Mayor ──
    {"person_a": 1, "person_b": 3, "type": "colleague",
     "context": "温永豹（时任市长）与高运禄（时任书记）长期党政搭档",
     "overlap_org": "虎林市", "overlap_period": "~2021-~2024"},
]

if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=STAGING_DB,
        gexf_path=STAGING_GEXF,
        overwrite=True,
    )
    print("Done!")
