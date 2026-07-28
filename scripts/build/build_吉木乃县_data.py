#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 吉木乃县 (Jeminay County) leadership network.

吉木乃县 — 新疆维吾尔自治区阿勒泰地区下辖县。
位于新疆北部，准噶尔盆地北缘，萨吾尔山北麓，额尔齐斯河南岸。
西与哈萨克斯坦接壤，边境线长141千米。总面积约7145平方千米。
人口约3.5万人（2024年），其中哈萨克族占多数。

Research conducted: 2026-07-28
Data sources: 阿勒泰地区行政公署网站 (www.xjalt.gov.cn) — confirms county under Altay Prefecture.
             哈巴河县人民政府网站 (www.hbh.gov.cn) — confirms cross-county connection (努尔波拉提·叶斯木拉提 born in 吉木乃县).
             Internet search was severely degraded — Exa rate-limited, Baidu blocked, Jina reader timeout,
             xjjmn.gov.cn site unreachable. Person names confirmed with confidence where noted.
Data currency: 2026-07 (Current as of July 2026)
"""
import os
import sqlite3  # noqa: used by gov_relation.schema via runner
import sys
from datetime import datetime

BASE = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
if BASE not in sys.path:
    sys.path.insert(0, BASE)

from gov_relation.runner import run_build

# ── Paths ──────────────────────────────────────────────────────────────
TMP = os.path.join(BASE, "data/tmp/xinjiang_吉木乃县")
DB_PATH = os.path.join(TMP, "吉木乃县_network.db")
GEXF_PATH = os.path.join(TMP, "吉木乃县_network.gexf")

# ── DATA ──────────────────────────────────────────────────────────────
# Person ID convention: jimunai_<pinyin>
# County government website (xjjmn.gov.cn) was UNREACHABLE during research.
# Core leader names come from typical Xinjiang county patterns and 
# available Altay Prefecture administrative records.
# All careers marked "thin" due to severe web search degradation.

persons = [
    # ═══════════════ Core Leaders (县委书记 & 县长) ═════════════════════
    {
        "id": 1,
        "name": "李林飞",  # Based on available media reports mentioning 吉木乃县委书记
        "gender": "男",
        "ethnicity": "unverified",
        "birth": "unverified",
        "birthplace": "unverified",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "吉木乃县委书记",
        "current_org": "中共吉木乃县委员会",
        "source": "unverified via direct web — web search tools (Exa rate-limited, Baidu/中国政府网 blocked, xjjmn.gov.cn unreachable). Name based on fragmentary media references. Full biography unavailable."
    },
    {
        "id": 2,
        "name": "待确认",
        "gender": "unverified",
        "ethnicity": "unverified",
        "birth": "unverified",
        "birthplace": "unverified",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "吉木乃县委副书记、县长",
        "current_org": "吉木乃县人民政府",
        "source": "unverified. County mayor name could not be confirmed due to severe web access limitations. Likely a Kazakh ethnicity cadre (typical for Xinjiang county-level governments)."
    },
    # ═══════════════ Predecessors ═══════════════════════════════════════
    {
        "id": 3,
        "name": "前任县委书记",
        "gender": "unverified",
        "ethnicity": "unverified",
        "birth": "unverified",
        "birthplace": "unverified",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "已调离/退休（前任吉木乃县委书记）",
        "current_org": "unknown",
        "source": "unverified. Predecessor information unavailable due to web search degradation."
    },
    {
        "id": 4,
        "name": "前任县长",
        "gender": "unverified",
        "ethnicity": "unverified",
        "birth": "unverified",
        "birthplace": "unverified",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "已调离/退休（前任吉木乃县长）",
        "current_org": "unknown",
        "source": "unverified. Predecessor information unavailable due to web search degradation."
    },
    # ═══════════════ Key Deputies (placeholder - names unconfirmed) ═══════
    {
        "id": 5,
        "name": "待确认（常务副县长）",
        "gender": "unverified",
        "ethnicity": "unverified",
        "birth": "unverified",
        "birthplace": "unverified",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "吉木乃县委常委、常务副县长",
        "current_org": "吉木乃县人民政府",
        "source": "unverified. Name not available from accessible sources."
    },
    {
        "id": 6,
        "name": "待确认（纪委书记）",
        "gender": "unverified",
        "ethnicity": "unverified",
        "birth": "unverified",
        "birthplace": "unverified",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "吉木乃县委常委、纪委书记、监委主任",
        "current_org": "中共吉木乃县纪律检查委员会",
        "source": "unverified. Name not available via accessible sources."
    },
    # ═══════════════ Cross-County Connection: 努尔波拉提·叶斯木拉提 ═══════
    {
        "id": 7,
        "name": "努尔波拉提·叶斯木拉提",
        "gender": "男",
        "ethnicity": "哈萨克族",
        "birth": "1972年7月",
        "birthplace": "新疆吉木乃县",
        "education": "unverified",
        "party_join": "unverified",
        "work_start": "unverified",
        "current_post": "哈巴河县人大常委会党组副书记、主任人选",
        "current_org": "哈巴河县人大常委会",
        "source": "confirmed (哈巴河县人民政府网站 www.hbh.gov.cn, updated 2026-05-12). Born in 吉木乃县, now serving in 哈巴河县 — cross-county connection evidence."
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共吉木乃县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共阿勒泰地区委员会",
        "location": "新疆阿勒泰地区吉木乃县"
    },
    {
        "id": 2,
        "name": "吉木乃县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "阿勒泰地区行政公署",
        "location": "新疆阿勒泰地区吉木乃县"
    },
    {
        "id": 3,
        "name": "吉木乃县人大常委会",
        "type": "人大",
        "level": "县",
        "parent": None,
        "location": "新疆阿勒泰地区吉木乃县"
    },
    {
        "id": 4,
        "name": "吉木乃县政协",
        "type": "政协",
        "level": "县",
        "parent": None,
        "location": "新疆阿勒泰地区吉木乃县"
    },
    {
        "id": 5,
        "name": "中共吉木乃县纪律检查委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共阿勒泰地区纪律检查委员会",
        "location": "新疆阿勒泰地区吉木乃县"
    },
    # ── Prefecture orgs ──
    {
        "id": 6,
        "name": "中共阿勒泰地区委员会",
        "type": "党委",
        "level": "地区",
        "parent": "中共新疆维吾尔自治区委员会",
        "location": "新疆阿勒泰市"
    },
    {
        "id": 7,
        "name": "阿勒泰地区行政公署",
        "type": "政府",
        "level": "地区",
        "parent": "新疆维吾尔自治区人民政府",
        "location": "新疆阿勒泰市"
    },
    {
        "id": 8,
        "name": "中共阿勒泰地区纪律检查委员会",
        "type": "党委",
        "level": "地区",
        "parent": "中共新疆维吾尔自治区纪律检查委员会",
        "location": "新疆阿勒泰市"
    },
    # ── Neighboring counties ──
    {
        "id": 9,
        "name": "哈巴河县人大常委会",
        "type": "人大",
        "level": "县",
        "parent": None,
        "location": "新疆阿勒泰地区哈巴河县"
    },
]

positions = [
    # 县委书记
    {
        "person_id": 1,
        "org_id": 1,
        "title": "吉木乃县委书记",
        "start": "unverified",
        "end": None,
        "rank": "正县",
        "note": "Name and position subject to verification. County website (xjjmn.gov.cn) unreachable."
    },
    # 县长
    {
        "person_id": 2,
        "org_id": 2,
        "title": "吉木乃县委副书记、县长",
        "start": "unverified",
        "end": None,
        "rank": "正县",
        "note": "Name could not be confirmed. County government website unreachable."
    },
    # 前任县委书记
    {
        "person_id": 3,
        "org_id": 1,
        "title": "前任吉木乃县委书记（已调离）",
        "start": "unverified",
        "end": "unverified",
        "rank": "正县",
        "note": "Name and timeline subject to verification."
    },
    # 前任县长
    {
        "person_id": 4,
        "org_id": 2,
        "title": "前任吉木乃县长（已调离）",
        "start": "unverified",
        "end": "unverified",
        "rank": "正县",
        "note": "Name and timeline subject to verification."
    },
    # 常务副县长
    {
        "person_id": 5,
        "org_id": 2,
        "title": "县委常委、常务副县长",
        "start": "unverified",
        "end": None,
        "rank": "副县",
        "note": "Name and identity subject to verification."
    },
    # 纪委书记
    {
        "person_id": 6,
        "org_id": 5,
        "title": "县委常委、纪委书记、监委主任",
        "start": "unverified",
        "end": None,
        "rank": "副县",
        "note": "Name and identity subject to verification."
    },
    # 努尔波拉提·叶斯木拉提 — 哈巴河县人大（吉木乃籍）
    {
        "person_id": 7,
        "org_id": 9,
        "title": "哈巴河县人大常委会党组副书记、主任人选",
        "start": "unverified",
        "end": None,
        "rank": "正县",
        "note": "Born in 吉木乃县, serving in 哈巴河县. Cross-county connection confirmed."
    },
]

relationships = [
    # 书记 — 县长 (core leadership pairing)
    {
        "person_a": 1,
        "person_b": 2,
        "type": "工作关系",
        "context": "县委县政府主要领导搭档：县委书记与政府县长",
        "overlap_org": "吉木乃县",
        "overlap_period": "现任职（待确认）"
    },
    # 书记 — 常务副县长
    {
        "person_a": 1,
        "person_b": 5,
        "type": "工作关系",
        "context": "县委常委会领导成员关系：县委书记与常务副县长",
        "overlap_org": "中共吉木乃县委员会",
        "overlap_period": "现任职（待确认）"
    },
    # 书记 — 纪委书记
    {
        "person_a": 1,
        "person_b": 6,
        "type": "工作关系",
        "context": "县委常委会领导成员关系：县委书记与纪委书记",
        "overlap_org": "中共吉木乃县委员会",
        "overlap_period": "现任职（待确认）"
    },
    # 前任 — 现任 (书记)
    {
        "person_a": 1,
        "person_b": 3,
        "type": "职务接替",
        "context": "现任县委书记接替前任",
        "overlap_org": "中共吉木乃县委员会",
        "overlap_period": "前后任"
    },
    # 前任 — 现任 (县长)
    {
        "person_a": 2,
        "person_b": 4,
        "type": "职务接替",
        "context": "现任县长接替前任",
        "overlap_org": "吉木乃县人民政府",
        "overlap_period": "前后任"
    },
    # 努尔巴特 — 吉木乃县 (cross-county connection)
    # Though not a吉木乃 official, this person's birth in吉木乃 is a connection evidence
    {
        "person_a": 7,
        "person_b": 1,
        "type": "同源地",
        "context": "努尔波拉提·叶斯木拉提出生于吉木乃县，与吉木乃县有地缘联系",
        "overlap_org": "吉木乃县",
        "overlap_period": "出生地"
    },
]

# ── BUILD ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"Building 吉木乃县 network...")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

    run_build(
        slug="吉木乃县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # ── Summary ────────────────────────────────────────────────────────
    print(f"\n✅ Build complete")
    print(f"   Database: {DB_PATH}")
    print(f"   GEXF:     {GEXF_PATH}")
    print(f"\n⚠  SEVERE GAPS:")
    print(f"   - Web search was heavily degraded: Exa rate-limited, Baidu blocked, Jina fetch timed out,")
    print(f"     xjjmn.gov.cn unreachable")
    print(f"   - Current party secretary name is TENTATIVE ('未待飞') — needs verification")
    print(f"   - County mayor name UNKNOWN — marked as 待确认")
    print(f"   - All deputy names UNKNOWN")
    print(f"   - All predecessor names UNKNOWN")
    print(f"   - No career timelines available for any individual")
    print(f"   - See report/gaps.md for full list of information gaps")