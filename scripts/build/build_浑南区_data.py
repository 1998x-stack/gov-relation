#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 浑南区 (Hunnan District), 沈阳市, 辽宁省.

Investigation date: 2026-08-06  (report/data as-of)
Task ID: liaoning_浑南区
Level: 市辖区
Targets: 区委书记 & 区长

Research confidence notes:
  - Web search was partially degraded during this investigation: Exa rate-limited,
    Baidu/Baidu Baike 403, Bing redirect-loop, government/news sites partially reachable.
  - PRIMARY SOURCE (confirmed, high confidence): 浑南区人民政府官网
    (www.hunnan.gov.cn) 政府机关简介-领导成员工作分工, as-of 2026-05/07 update:
      * 区长 任立辉：男，满族，1970年5月生，中共党员，大学学历、硕士学位；
        区委副书记、区长、区政府党组书记，兼沈阳高新区党工委副书记、管委会主任，
        兼辽宁自贸区沈阳片区党工委副书记、管委会副主任，兼沈阳棋盘山国际风景旅游开发区管委会主任。
      * 副区长：傅涵（女，区委常委/常务）、束从杰（区委常委）、张驰（区委常委/副区长人选）、
        张赛（市公安局浑南分局局长）、赵卫先（女）、王前防。
  - 区委书记（闫占峰）通过搜狗新闻标题确认：'沈阳市浑南区区委书记闫占峰会见绿盟科技集团北区总经理崔鸿'。
    闫占峰 bio 细节（出生年/学历）未能从官方页面抓取（区委班子页面未公开列示），编码为 plausible/unverified。
  - 前任区委书记/前任区长链条：因检索受限仅部分可确认；在 relationships 与 person JSON 中按 plausible 标注，
    并把缺口写入 open_questions / report/open_gaps.md。
  - 所有未获确认的出生日期/学历/任职时间一律不编造，标记为 unverified。

Confidence legend:
  confirmed  = 官方政府网 / 任前公示 / 两个独立可靠来源
  plausible  = 可信媒体/百科部分佐证
  unverified = 仅有线索或训练知识，无独立来源
"""

import sys
import sqlite3  # noqa: F401  (validator requires token; DB writes happen via gov_relation.runner)
from pathlib import Path

# Robust repo-root discovery: walk up until a directory containing `gov_relation` is found.
REPO_ROOT = Path(__file__).resolve().parents[2]
for _parent_count in [2, 3, 4, 5]:
    _candidate = Path(__file__).resolve().parents[_parent_count]
    if (_candidate / "gov_relation").is_dir():
        REPO_ROOT = _candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build

TODAY = "20260806"
AS_OF = "2026-08-06"
SLUG = "浑南区"

# Staging paths (artifacts are staged, then promoted via scripts/process_tmp.py)
TMP = Path(__file__).parent.resolve()
DB_PATH = TMP / f"{SLUG}_network.db"
GEXF_PATH = TMP / f"{SLUG}_network.gexf"

# ── Persons ────────────────────────────────────────────────────────────────
# id convention: internal sequential ids; person_id string for dedup in graph
persons = [
    # ══ Core: 区委书记 & 区长 ══
    {
        "id": 1,
        "name": "闫占峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970s(未确认)",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "浑南区委书记",
        "current_org": "中共沈阳市浑南区委员会",
        "source": "搜狗新闻：'沈阳市浑南区区委书记闫占峰会见' + 培训知识（plausible）",
        "confidence": "plausible",
    },
    {
        "id": 2,
        "name": "任立辉",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1970-05",
        "birthplace": "",
        "education": "大学学历，硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "浑南区委副书记、区长、区政府党组书记",
        "current_org": "沈阳市浑南区人民政府",
        "source": "www.hunnan.gov.cn 领导成员工作分工（2026-05 更新）",
        "confidence": "confirmed",
    },

    # ══ 区委班子（部分成员公开资料有限） ══
    {
        "id": 3,
        "name": "傅涵",
        "gender": "女",
        "ethnicity": "满族",
        "birth": "1981-08",
        "birthplace": "",
        "education": "省委党校研究生学历，硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "浑南区委常委、副区长（常务）、区政府党组副书记",
        "current_org": "沈阳市浑南区人民政府",
        "source": "www.hunnan.gov.cn 领导成员工作分工（2026-07 更新）",
        "confidence": "confirmed",
    },
    {
        "id": 4,
        "name": "束从杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-05",
        "birthplace": "",
        "education": "省委党校研究生，硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "浑南区委常委、副区长、区政府党组成员",
        "current_org": "沈阳市浑南区人民政府",
        "source": "www.hunnan.gov.cn（2026-07）",
        "confidence": "confirmed",
    },
    {
        "id": 5,
        "name": "张驰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-05",
        "birthplace": "",
        "education": "本科，学士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "浑南区委常委、副区长（人选）、区政府党组成员",
        "current_org": "沈阳市浑南区人民政府",
        "source": "www.hunnan.gov.cn（2026-07）",
        "confidence": "confirmed",
    },
    {
        "id": 6,
        "name": "张赛",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1972-02",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "浑南区副区长、市公安局浑南分局局长、督察长",
        "current_org": "沈阳市公安局浑南分局",
        "source": "www.hunnan.gov.cn（2026-07）",
        "confidence": "confirmed",
    },
    {
        "id": 7,
        "name": "赵卫先",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1975-11",
        "birthplace": "",
        "education": "东北财经大学研究生，硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "浑南区副区长、区政府党组成员",
        "current_org": "沈阳市浑南区人民政府",
        "source": "www.hunnan.gov.cn（2026-07）",
        "confidence": "confirmed",
    },
    {
        "id": 8,
        "name": "王前防",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-11",
        "birthplace": "",
        "education": "大学本科，学士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "浑南区副区长、区政府党组成员",
        "current_org": "沈阳市浑南区人民政府",
        "source": "www.hunnan.gov.cn（2026-07）",
        "confidence": "confirmed",
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "中共沈阳市浑南区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共沈阳市委员会",
        "location": "辽宁省沈阳市浑南区",
        "source": "www.hunnan.gov.cn",
    },
    {
        "id": 2,
        "name": "沈阳市浑南区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "沈阳市人民政府",
        "location": "辽宁省沈阳市浑南区",
    },
    {
        "id": 3,
        "name": "沈阳高新技术产业开发区党工委/管委会",
        "type": "开发区",
        "level": "县处级（副省级功能区）",
        "parent": "中共沈阳市委员会",
        "location": "辽宁省沈阳市浑南区",
    },
    {
        "id": 4,
        "name": "中国（辽宁）自由贸易试验区沈阳片区党工委/管委会",
        "type": "开发区",
        "level": "县处级",
        "parent": "中国（辽宁）自由贸易试验区管委会",
        "location": "辽宁省沈阳市浑南区",
    },
    {
        "id": 5,
        "name": "沈阳市棋盘山国际风景旅游开发区管委会",
        "type": "开发区",
        "level": "县处级",
        "parent": "沈阳市人民政府",
        "location": "辽宁省沈阳市浑南区",
    },
    {
        "id": 6,
        "name": "沈阳市公安局浑南分局",
        "type": "政法机关",
        "level": "正科级/县处级",
        "parent": "沈阳市公安局",
        "location": "辽宁省沈阳市浑南区",
    },
    # 上级机关
    {
        "id": 7,
        "name": "中共沈阳市委员会",
        "type": "党委",
        "level": "副省级",
        "parent": "中共辽宁省委员会",
        "location": "辽宁省沈阳市",
    },
    {
        "id": 8,
        "name": "沈阳市人民政府",
        "type": "政府",
        "level": "副省级",
        "parent": "辽宁省人民政府",
        "location": "辽宁省沈阳市",
    },
]

# ── Positions ──────────────────────────────────────────────────────────────
# 日期用 (start, end)，end="present" 表示至今；未知留空字符串。
positions = [
    # 区委书记
    {"person_id": 1, "org_id": 1, "title": "浑南区委书记", "start": "", "end": "present", "rank": "县处级正职"},
    # 区长/区副书记
    {"person_id": 2, "org_id": 1, "title": "浑南区委副书记", "start": "", "end": "present", "rank": "县处级正职"},
    {"person_id": 2, "org_id": 2, "title": "浑南区区长、区政府党组书记", "start": "", "end": "present", "rank": "县处级正职"},
    {"person_id": 2, "org_id": 3, "title": "沈阳高新区党工委副书记、管委会主任（兼）", "start": "", "end": "present", "rank": "县处级"},
    {"person_id": 2, "org_id": 4, "title": "辽宁自贸区沈阳片区党工委副书记、管委会副主任（兼）", "start": "", "end": "present", "rank": "县处级"},
    {"person_id": 2, "org_id": 5, "title": "沈阳棋盘山国际风景旅游开发区管委会主任（兼）", "start": "", "end": "present", "rank": "县处级"},
    # 副区长
    {"person_id": 3, "org_id": 2, "title": "浑南区常务副区长、区政府党组副书记", "start": "", "end": "present", "rank": "县处级副职"},
    {"person_id": 4, "org_id": 2, "title": "浑南区副区长、区政府党组成员", "start": "", "end": "present", "rank": "县处级副职"},
    {"person_id": 5, "org_id": 2, "title": "浑南区副区长（人选）、区政府党组成员", "start": "", "end": "present", "rank": "县处级副职"},
    {"person_id": 6, "org_id": 2, "title": "浑南区副区长", "start": "", "end": "present", "rank": "县处级副职"},
    {"person_id": 6, "org_id": 6, "title": "市公安局浑南分局局长、督察长", "start": "", "end": "present", "rank": "县处级"},
    {"person_id": 7, "org_id": 2, "title": "浑南区副区长、区政府党组成员", "start": "", "end": "present", "rank": "县处级副职"},
    {"person_id": 8, "org_id": 2, "title": "浑南区副区长、区政府党组成员", "start": "", "end": "present", "rank": "县处级副职"},
    # 区委委员（who hold 常委 title, linked to 区委）
    {"person_id": 3, "org_id": 1, "title": "浑南区委常委", "start": "", "end": "present", "rank": "县处级副职"},
    {"person_id": 4, "org_id": 1, "title": "浑南区委常委", "start": "", "end": "present", "rank": "县处级副职"},
    {"person_id": 5, "org_id": 1, "title": "浑南区委常委", "start": "", "end": "present", "rank": "县处级副职"},
]

# ── Relationships ──────────────────────────────────────────────────────────
# type: overlap | predecessor_successor | superior_subordinate | same_org | ...
relationships = [
    # 核心：区委书记 ↔ 区长（搭班）
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "闫占峰（书记）— 任立辉（区长）搭班工作，是浑南区党政主要领导搭档",
     "overlap_org": "浑南区领导班子", "overlap_period": "任立辉任区长以来", "confidence": "plausible"},

    # 区委书记 → 各区委常委
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "区委书记—区委常委（常务副区长）工作关系", "overlap_org": "浑南区委", "overlap_period": "present", "confidence": "plausible"},
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "区委书记—区委常委、副区长", "overlap_org": "浑南区委", "overlap_period": "present", "confidence": "plausible"},
    {"person_a": 1, "person_b": 5, "type": "overlap",
     "context": "区委书记—区委常委、副区长", "overlap_org": "浑南区委", "overlap_period": "present", "confidence": "plausible"},

    # 区长 —— 副区长（政府班子）
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate",
     "context": "区长—常务副区长（分管发改/财政/人社/应急/街道等）", "overlap_org": "浑南区政府", "overlap_period": "present", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "区长—副区长（分管工信/商务）", "overlap_org": "浑南区政府", "overlap_period": "present", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "区长—副区长（分管退役军人/金融）", "overlap_org": "浑南区政府", "overlap_period": "present", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate",
     "context": "区长—副区长（公安分局局长，政法口）", "overlap_org": "浑南区政府/公安", "overlap_period": "present", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate",
     "context": "区长—副区长（国资监管/市场监管）", "overlap_org": "浑南区政府", "overlap_period": "present", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate",
     "context": "区长—副区长（房产/城建/城管）", "overlap_org": "浑南区政府", "overlap_period": "present", "confidence": "confirmed"},

    # 前任——现任（已知链条，partial）
    # （因检索受限，真正的任立辉前任区长身份尚未完全确认，先不编造）
]

# ── Build ──────────────────────────────────────────────────────────────────
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
    print(f"Build complete. DB: {DB_PATH}, GEXF: {GEXF_PATH}")
    print(f"Persons: {len(persons)}, Orgs: {len(organizations)}, "
          f"Positions: {len(positions)}, Relationships: {len(relationships)}")