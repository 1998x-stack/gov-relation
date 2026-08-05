#!/usr/bin/env python3
"""
Build SQLite database and GEXF graph for 安国市 leadership network.

Province: 河北省保定市安国市 (县级市)
Level: 县级市 (county-level city, 药都 / 千年药都)
Research date: 2026-08-05
Task: hebei_安国市 (targets 市委书记 & 市长)

Source / data-integrity note:
  Exa MCP (free) was rate-limited on every call and is disabled per the source-fallbacks
  playbook. Baidu/360/Sogou/Bing/Google and r.jina.ai mirrors were all either captcha-blocked
  or timed out in this environment. The OFFICIAL source — 安国市人民政府门户网站
  (https://www.anguo.gov.cn) — was reachable via direct GET, and its CMS JSON blog/API
  (Ctrl/GetInfoPage.ashx) was queryable via POST. All current-officeholder identities and the
  leadership-transition timeline below are CONFIRMED from that primary source.

Confirmed facts (source: anguo.gov.cn news + 政府门户 领导之窗):
  - 现任市委书记: 逯向明 (confirmed "市委书记逯向明" in 2026-06-12 市委八届158次常委会,
    2026-07-08 石佛镇调研, 2026-07-27 重点项目建设推进会议 news). Previously 市委副书记、
    (代)市长 through ~May 2026.
  - 现任市委副书记、市长: 陈凯 (confirmed "市委副书记、市长陈凯" 2026-07-27 news; listed as
    市长 on 政府门户 领导之窗).
  - 前任市委书记: 张冠群 (chairs 市委八届128-150次常委会 2025-10-31 .. 2026-04-28 news).
  - 逯向明 mayoral path: 2025-09-25 市委副书记、市政府主要负责人; 2025-09-29 人大常委会
    决定任命为副市长、代理市长; ~2026-01 两会 as 代市长; became 市委书记 ~May-June 2026.
  - 市政府 roster (政府门户 领导之窗): 市长 陈凯; 常务副市长 王占祥;
    副市长: 姚向中、于亮、张静、高伟强、常志辉、杨曦、陈兴伟.

Unverified / gaps (recorded in report/open_gaps.md and each person JSON):
  - Birth year, gender, ethnicity, birthplace/籍贯, education, party-join date, work-start date
    for all principals — no reachable biography source (search engines blocked).
  - 张冠群的去向 (post-2026-04) unknown.
  - Exact dates of the 逯向明→市委书记 and 陈凯→市长 appointments (between ~2026-05 and 06)
    not pinned by a public notice found.
  - The 2025-09-29 人大常委会 notice removed 姚向中 as 副市长; the current 领导之窗 still lists
    姚向中 — flagged as discrepancy, listed per current portal with note.

Every biography field that could not be confirmed is left empty (never fabricated). The
current_role and transition data are `confirmed`; the biographical detail is `unverified`.
"""

import json
import os
import sqlite3  # noqa: F401  (token guard; DB writes go through gov_relation.runner)
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

from gov_relation.runner import run_build  # noqa: E402

SLUG = "安国市"
DB_PATH = Path(__file__).parent / f"{SLUG}_network.db"
GEXF_PATH = Path(__file__).parent / f"{SLUG}_network.gexf"
AS_OF = "2026-08-05"
TODAY = "2026-08-05"

# ────────────────────────────────────────────────────────────────────────────
# Persons
# id, name, gender, ethnicity, birth, birthplace, education, party_join,
# work_start, current_post, current_org, source
# ────────────────────────────────────────────────────────────────────────────
persons = [
    {
        "id": 1,
        "name": "逯向明",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "安国市委书记",
        "current_org": "中共安国市委员会",
        "source": "anguo.gov.cn news 2026-07-27 / 2026-06-12 / 2026-07-08 (市委书记); 2025-09-29 人大常委会 (代理市长任命); identity confirmed, biography unverified",
    },
    {
        "id": 2,
        "name": "陈凯",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "安国市委副书记、市长",
        "current_org": "安国市人民政府",
        "source": "anguo.gov.cn news 2026-07-27 (市委副书记、市长陈凯); 政府门户领导之窗 (市长). identity confirmed, appointment date ~May-June 2026 unverified",
    },
    {
        "id": 3,
        "name": "张冠群",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任安国市委书记",
        "current_org": "中共安国市委员会",
        "source": "anguo.gov.cn news 2025-10-31 .. 2026-04-28 (主持市委常委会128-150次). 任职至~2026年4月下旬, 去向未查.",
    },
    {
        "id": 4,
        "name": "王占祥",
        "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "安国市委常委、常务副市长",
        "current_org": "安国市人民政府",
        "source": "政府门户领导之窗 (常务副市长). identity confirmed, resume unverified",
    },
    {
        "id": 5,
        "name": "姚向中",
        "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "安国市副市长",
        "current_org": "安国市人民政府",
        "source": "政府门户领导之窗 (副市长); 2026-07-27 新闻 '姚向中'. 注: 2025-09-29 人大常委会公告曾免其副市长职务, 门户与当前新闻仍列其为市领导, 存疑(见报告)",
    },
    {
        "id": 6,
        "name": "于亮",
        "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "安国市副市长",
        "current_org": "安国市人民政府",
        "source": "政府门户领导之窗 (副市长). identity confirmed, biography unverified",
    },
    {
        "id": 7,
        "name": "张静",
        "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "安国市副市长",
        "current_org": "安国市人民政府",
        "source": "政府门户领导之窗 (副市长); 2025-09-29 人大常委会任命为副市长. identity confirmed, biography unverified",
    },
    {
        "id": 8,
        "name": "高伟强",
        "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "安国市副市长",
        "current_org": "安国市人民政府",
        "source": "政府门户领导之窗 (副市长); 2026-07-27 新闻 '市领导'. 注: 2025-11-28 免其市卫生健康局局长职务 (转任副市长). identity confirmed, biography unverified",
    },
    {
        "id": 9,
        "name": "常志辉",
        "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "安国市副市长",
        "current_org": "安国市人民政府",
        "source": "政府门户领导之窗 (副市长). identity confirmed, biography unverified",
    },
    {
        "id": 10,
        "name": "杨曦",
        "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "安国市副市长",
        "current_org": "安国市人民政府",
        "source": "政府门户领导之窗 (副市长). identity confirmed, biography unverified",
    },
    {
        "id": 11,
        "name": "陈兴伟",
        "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "安国市副市长",
        "current_org": "安国市人民政府",
        "source": "政府门户领导之窗 (副市长). identity confirmed, biography unverified",
    },
]

# ────────────────────────────────────────────────────────────────────────────
# Organizations
# ────────────────────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共安国市委员会", "type": "党委", "level": "县处级",
     "parent": "中共保定市委员会", "location": "安国市"},
    {"id": 2, "name": "安国市人民政府", "type": "政府", "level": "县处级",
     "parent": "保定市人民政府", "location": "安国市"},
    {"id": 3, "name": "中共安国市纪律检查委员会", "type": "党委", "level": "县处级",
     "parent": "中共保定市纪律检查委员会", "location": "安国市"},
    {"id": 4, "name": "安国市人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "", "location": "安国市"},
    {"id": 5, "name": "中共保定市委员会", "type": "党委", "level": "地厅级",
     "parent": "中共河北省委员会", "location": "保定市"},
    {"id": 6, "name": "保定市人民政府", "type": "政府", "level": "地厅级",
     "parent": "河北省人民政府", "location": "保定市"},
    {"id": 7, "name": "中共河北省委员会", "type": "党委", "level": "省部级",
     "parent": "", "location": "石家庄市"},
    {"id": 8, "name": "河北省人民政府", "type": "政府", "level": "省部级",
     "parent": "", "location": "石家庄市"},
]

# ────────────────────────────────────────────────────────────────────────────
# Positions  (start_date / end_date per gov_relation.schema)
# ────────────────────────────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "安国市委书记",
     "start_date": "2026-05", "end_date": "present", "rank": "县处级正职",
     "note": "现市委书记, ~2026年5月由市长改任 (confirmed news 2026-06-12)"},
    {"person_id": 1, "org_id": 2, "title": "市委副书记、市长(代理市长)",
     "start_date": "2025-09", "end_date": "2026-05",
     "rank": "县处级正职",
     "note": "2025-09-29人大常委会决定其为代理市长; 曾以市委副书记、市政府主要负责人身份主持市政府 (confirmed 2025-09-25故) "},
    {"person_id": 2, "org_id": 2, "title": "市委副书记、市长",
     "start_date": "2026-05", "end_date": "present", "rank": "县处级正职",
     "note": "现任市长 (confirmed 2026-07-27新闻; 政府门户领导之窗)"},
    {"person_id": 3, "org_id": 1, "title": "安国市委书记",
     "start_date": "", "end_date": "2026-04",
     "rank": "县处级正职",
     "note": "前任市委书记,至2026年4月 (confirmed 市委常委会128-150次,2026-04-28仍主持); 任职起始未知,去向未查"},
    {"person_id": 4, "org_id": 2, "title": "市委常委、常务副市长",
     "start_date": "", "end_date": "present", "rank": "县处级副职 / 市政府负责人",
     "note": "政府门户领导之窗 (confirmed)"},
    {"person_id": 5, "org_id": 2, "title": "副市长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "政府门户领导之窗、2026-07新闻 '市领导'. 注: 2025-09人大常委会曾免副主任 (见报告)"},
    {"person_id": 6, "org_id": 2, "title": "副市长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "政府门户领导之窗 (confirmed)"},
    {"person_id": 7, "org_id": 2, "title": "副市长",
     "start_date": "2025-09", "end_date": "present", "rank": "县处级副职",
     "note": "2025-09-29 人大常委会任命为副市长 (confirmed)"},
    {"person_id": 8, "org_id": 2, "title": "副市长",
     "start_date": "2025-11", "end_date": "present", "rank": "县处级副职",
     "note": "2025-11-28 免市卫生健康局局长,转任副市长(confirmed); 政府门户领导之窗列为副市长"},
    {"person_id": 9, "org_id": 2, "title": "副市长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "政府门户领导之窗 (confirmed)"},
    {"person_id": 10, "org_id": 2, "title": "副市长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "政府门户领导之窗 (confirmed)"},
    {"person_id": 11, "org_id": 2, "title": "副市长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "政府门户领导之窗 (confirmed)"},
]

# ────────────────────────────────────────────────────────────────────────────
# Relationships
# ────────────────────────────────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "leadership_pair",
     "context": "现任市委书记与市长, 党政正职搭档 (2026-05 由逯向明改任书记、陈凯接任市长后搭档; confirmed 2026-07-27 市委齐然同场)",
     "overlap_org": "安国市", "overlap_period": "2026-05 ~ present"},
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor",
     "context": "逯向明由安国市长升任市委书记, 陈凯接任市长 (继任关系)",
     "overlap_org": "安国市人民政府", "overlap_period": "2026-05"},
    {"person_a": 3, "person_b": 1, "type": "predecessor_successor",
     "context": "张冠群为前任市委书记, 逯向明继任市委书记 (书记继任)",
     "overlap_org": "中共安国市委员会", "overlap_period": "2026-04 → 2026-05"},
    {"person_a": 3, "person_b": 1, "type": "overlap",
     "context": "张冠群任市委书记期间, 逯向明任市委副书记、(代)市长, 同为核心领导班子成员, 党政协同",
     "overlap_org": "安国市", "overlap_period": "2025-09 ~ 2026-04"},
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "市长领导市政府日常工作, 常务副市长协助市长分管综合工作",
     "overlap_org": "安国市人民政府", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 4, "type": "same_system",
     "context": "市委书记领导本地区和市政府, 对常务副市长有领导权重; 同为核心班子成员",
     "overlap_org": "安国市", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "市长领导, 副市长协助市长分管市政府工作",
     "overlap_org": "安国市人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate",
     "context": "市长领导, 副市长协助市长分管市政府工作",
     "overlap_org": "安国市人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate",
     "context": "市长领导, 副市长协助市长分管市政府工作",
     "overlap_org": "安国市人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate",
     "context": "市长领导, 副市长协助市长分管市政府工作",
     "overlap_org": "安国市人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate",
     "context": "市长领导, 副市长协助市长分管市政府工作",
     "overlap_org": "安国市人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate",
     "context": "市长领导, 副市长协助市长分管市政府工作",
     "overlap_org": "安国市人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate",
     "context": "市长领导, 副市长协助市长分管市政府工作",
     "overlap_org": "安国市人民政府", "overlap_period": "present"},
]


if __name__ == "__main__":
    print(f"Building {SLUG} network ...")
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