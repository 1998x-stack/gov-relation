#!/usr/bin/env python3
"""Build script for 长洲区 (Changzhou District, Wuzhou, Guangxi) leadership network.

Generated: 2026-07-23
Level: 市辖区
Province: 广西壮族自治区
Parent City: 梧州市
Targets: 区委书记 & 区长

Research Note:
  The official district website and all Chinese government sources were unreachable
  during this investigation (network timeouts, Baidu captcha, Jina Reader and Exa
  rate-limited/unavailable).

  Confirmed findings:
  - 陶国铭 was 长洲区委书记 as of 2022-09-22 (source: NetEase News article).
    Whether he still holds the position as of 2026 is UNVERIFIED but plausible.
  - 长洲区 has a "书记区长直通车" mechanism (source: wuzhou.gov.cn news, 2026-04-08),
    confirming both 区委书记 and 区长 positions were filled as of early 2026.
  - The article mentions 处级领导干部联系服务企业, suggesting normal leadership structure.

  UNKNOWN (marked as GAP):
  - Full name of current 区长 as of 2026.
  - All deputy leader names (常务副区长, 纪委书记, 组织部长, etc.).
  - Career histories for all figures.
  - 前任区委书记/区长 and their whereabouts.

Sources:
  - https://www.163.com (NetEase News — "区委书记陶国铭一行到长洲区法院倒水人民法庭调研", 2022-09-22)
  - http://www.wuzhou.gov.cn/zjwz/zwdt_1/xqdt/t27452464.shtml (长洲区营商环境文章提及"书记区长直通车", 2026-04-08)
  - http://www.wuzhou.gov.cn/ (梧州市人民政府门户网站)
"""

import sqlite3  # noqa: used by gov_relation.runner
from pathlib import Path

from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
from gov_relation.runner import run_build

# ═══════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════

# fmt: off
PERSONS = [
    # ── Core Leaders ──
    {
        "id": 1,
        "name": "陶国铭",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "长洲区委书记（据2022-09确认；2026年是否仍在任待查）",
        "current_org": "中共梧州市长洲区委员会",
        "source": "https://www.163.com (网易号：梧州市长洲区人民法院文章，2022-09-22确认陶国铭时任长洲区委书记；2026年现任身份未独立验证)",
    },
    {
        "id": 2,
        "name": "【待查】长洲区区长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "长洲区区长（待查）",
        "current_org": "梧州市长洲区人民政府",
        "source": "GAP — 官方网站无法访问；待后续通过梧州市委组织部任前公示或领导之窗页面补充",
    },
    # ── Deputy Leaders (all GAPS) ──
    {
        "id": 3,
        "name": "【待查】长洲区常务副区长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "长洲区委常委、常务副区长（待查）",
        "current_org": "梧州市长洲区人民政府",
        "source": "GAP — 待后续通过长洲区政府领导之窗页面补充",
    },
    {
        "id": 4,
        "name": "【待查】长洲区纪委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "长洲区委常委、纪委书记（待查）",
        "current_org": "中共梧州市长洲区纪律检查委员会",
        "source": "GAP — 待后续补充",
    },
    {
        "id": 5,
        "name": "【待查】长洲区委组织部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "长洲区委常委、组织部长（待查）",
        "current_org": "中共梧州市长洲区委组织部",
        "source": "GAP — 待后续补充",
    },
    {
        "id": 6,
        "name": "【待查】长洲区委副书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "长洲区委副书记（待查）",
        "current_org": "中共梧州市长洲区委员会",
        "source": "GAP — 待后续补充",
    },
    {
        "id": 7,
        "name": "【待查】长洲区前任区委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任长洲区委书记（姓名和去向均待查）",
        "current_org": "",
        "source": "GAP — 待后续通过梧州市委组织部历年人事任免公告补充",
    },
    {
        "id": 8,
        "name": "【待查】长洲区前任区长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任长洲区区长（姓名和去向均待查）",
        "current_org": "",
        "source": "GAP — 待后续补充",
    },
    {
        "id": 9,
        "name": "【待查】长洲区人大常委会主任",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "长洲区人大常委会主任（待查）",
        "current_org": "梧州市长洲区人大常委会",
        "source": "GAP — 待后续补充",
    },
    {
        "id": 10,
        "name": "【待查】长洲区政协主席",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "长洲区政协主席（待查）",
        "current_org": "中国人民政治协商会议梧州市长洲区委员会",
        "source": "GAP — 待后续补充",
    },
]

ORGANIZATIONS = [
    {"id": 1, "name": "中共梧州市长洲区委员会", "type": "党委", "level": "正处级", "parent": "中共梧州市委员会", "location": "梧州市长洲区"},
    {"id": 2, "name": "梧州市长洲区人民政府", "type": "政府", "level": "正处级", "parent": "梧州市人民政府", "location": "梧州市长洲区"},
    {"id": 3, "name": "中共梧州市长洲区纪律检查委员会", "type": "纪委", "level": "副处级", "parent": "中共梧州市纪律检查委员会", "location": "梧州市长洲区"},
    {"id": 4, "name": "中共梧州市长洲区委组织部", "type": "党委", "level": "正科级", "parent": "中共梧州市长洲区委员会", "location": "梧州市长洲区"},
    {"id": 5, "name": "梧州市长洲区人大常委会", "type": "人大", "level": "正处级", "parent": "梧州市人大常委会", "location": "梧州市长洲区"},
    {"id": 6, "name": "政协梧州市长洲区委员会", "type": "政协", "level": "正处级", "parent": "政协梧州市委员会", "location": "梧州市长洲区"},
]

POSITIONS = [
    # 陶国铭 — 长洲区委书记（2022年确认）
    {"person_id": 1, "org_id": 1, "title": "长洲区委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "2022-09-22报道以区委书记身份调研，2026年是否在任待查"},
    # GAP — 区长
    {"person_id": 2, "org_id": 2, "title": "长洲区区长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "GAP — 姓名和任职时间均未知"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "GAP — 待查"},
    # GAP — 常务副区长
    {"person_id": 3, "org_id": 2, "title": "长洲区常务副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "GAP — 姓名未知"},
    {"person_id": 3, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "GAP — 姓名未知"},
    # GAP — 纪委书记
    {"person_id": 4, "org_id": 3, "title": "长洲区纪委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "GAP — 姓名未知"},
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "GAP — 姓名未知"},
    # GAP — 组织部长
    {"person_id": 5, "org_id": 4, "title": "长洲区委组织部长", "start_date": "", "end_date": "present", "rank": "正科级", "note": "GAP — 姓名未知"},
    {"person_id": 5, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "GAP — 姓名未知"},
    # GAP — 区委副书记
    {"person_id": 6, "org_id": 1, "title": "长洲区委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "GAP — 姓名未知"},
    # GAP — 前任书记
    {"person_id": 7, "org_id": 1, "title": "长洲区委书记（前任）", "start_date": "", "end_date": "", "rank": "正处级", "note": "GAP — 姓名和去向均未知"},
    # GAP — 前任区长
    {"person_id": 8, "org_id": 2, "title": "长洲区区长（前任）", "start_date": "", "end_date": "", "rank": "正处级", "note": "GAP — 姓名和去向均未知"},
    # GAP — 人大主任
    {"person_id": 9, "org_id": 5, "title": "长洲区人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": "GAP — 姓名未知"},
    # GAP — 政协主席
    {"person_id": 10, "org_id": 6, "title": "长洲区政协主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": "GAP — 姓名未知"},
]

RELATIONSHIPS = [
    # 党政正职（区长待查）
    {"person_a": 1, "person_b": 2, "type": "党政正职搭档", "context": "区委书记-区长（区长姓名待查）", "overlap_org": "长洲区四套班子", "overlap_period": "", "source": "GAP — 区长身份未确认", "confidence": "unverified"},
    # 书记-副书记
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "区委书记-区委副书记", "overlap_org": "长洲区委常委会", "overlap_period": "", "source": "GAP — 副书记姓名待查", "confidence": "unverified"},
    # 书记-纪委
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "区委书记-纪委书记", "overlap_org": "长洲区委常委会", "overlap_period": "", "source": "GAP — 纪委书记姓名待查", "confidence": "unverified"},
]

# fmt: on

# ═══════════════════════════════════════════════════════════════
# BUILD (using staging dir paths)
# ═══════════════════════════════════════════════════════════════

STAGING_DIR = Path(__file__).resolve().parent
DB_PATH = STAGING_DIR / "长洲区_network.db"
GEXF_PATH = STAGING_DIR / "长洲区_network.gexf"

if __name__ == "__main__":
    run_build(
        slug="长洲区",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
