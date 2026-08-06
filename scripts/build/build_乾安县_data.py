#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 乾安县, 松原市, 吉林省.

Level: 县
Province: 吉林省
Parent city: 松原市
Targets: 县委书记 (Party Secretary: 陈锐, 兼县长一肩挑), 县长 (Mayor: 陈锐兼任; 待县委副书记/县长候选人东 踵查)
Task ID: jilin_乾安县

Research date: 2026-08-07
Official source: http://www.jlqa.gov.cn/ (乾安县人民政府官网 政府机构 + 政务要闻 + 县融媒体中心新闻)

Current status (as of 2026-08-07, verified via 乾安县人民政府官网 政务要闻 + 政府机构页):
- 县委书记: 陈锐 (兼县长，党政一肩挑; 2026-07-13/08-04 主持县委常委会, 2026-06~08 多篇官方要闻)
- 县委副书记: 刘小刚 (专职副书记; 2026-06-30 文艺汇演出席, 2026-07-22 陪同陈锐调研)
- 县人大常委会主任: 邹立辉 (2026-06-30 文艺汇演出席)
- 县委常委、常务副县长: 吴迪 (2026-08 政府机构页)
- 县委常委、副县长: 吴海涛 (2026-07-22 陪同陈锐调研)
- 副县长: 许鑫、周志军、李环宇、朱子岩、丁凯 (2026-08 政府机构页)
- 县人民法院党组书记、代院长: 丛峰 (2026-07-25 报道)

Leadership roster evolution (2021-2026, 官方政府机构页历史快照):
- 2021-02 县长: 王立国; 常务: 黄举明; 副县长: 袁向江、于振军、刁安恒、于健、曲志涛、张喜军
- 2023-03 县长: 王立国; 常务: 徐兴文; 副县长: 于振军、于健、曲志涛、张喜军、于静涛、王军
- 2026-06 常务: 于振军; (过渡期)
- 2026-08 县长: 陈锐(兼); 常务: 吴迪; 副县长: 许鑫、吴海涛、周志军、李环宇、朱子岩、丁凯

Predecessor chain (县委书记): 陈锐 (2025-2026在任) → 前书记身份待查 (公开渠道未获取, unverified)

Confidence notes:
  陈锐/刘小刚/邹立辉/吴迪/吴海涛/丛峰 身份与在任均为 confirmed (官方县官网 2026).
  政府班子 roster 为官方政府机构页一手数据 confirmed.
  王立国为前任县长 confirmed (2021-2023 官方要闻); 于静涛为乾安副县长(2023) 且由扶余市报告证实.
  陈锐 出生/籍贯/学历/入党参工/任书记前职/前任书记身份/各副县长履历 多为 plausible/unverified, 已标注 each JSON open_questions.
  跨县交流节点 (于静涛/郭丽明/孙鹏) 为 confirmed (扶余市调查报告).
"""

from __future__ import annotations

import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# Locate repo root robustly across staging vs canonical locations.
REPO_ROOT = Path(__file__).resolve().parents[2]
for _pc in (2, 3, 4, 5):
    _candidate = Path(__file__).resolve().parents[_pc]
    if (_candidate / "gov_relation").is_dir():
        REPO_ROOT = _candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "乾安县"
TASK_ID = "jilin_乾安县"

# DB/GEXF + person JSONs always land in the task staging dir.
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / TASK_ID
if _CURRENT_DIR.name == TASK_ID:
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR  # fallback
STAGING.mkdir(parents=True, exist_ok=True)

DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING

AS_OF = "2026-08-07"
TODAY = "20260807"

_PID = "qian-an"  # person-id prefix for graph dedup across investigations

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ── Core: 县委书记 (兼县长, 一肩挑) ──
    {
        "id": 1,
        "name": "陈锐",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记（兼县长，党政一肩挑）",
        "current_org": "中共乾安县委员会",
        "source": "http://www.jlqa.gov.cn/zwgk/zwdt/202608/t20260806_576628.html",
    },
    # ── 县委副书记 (专职) ──
    {
        "id": 2,
        "name": "刘小刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共乾安县委员会",
        "source": "http://www.jlqa.gov.cn/zwgk/zwdt/202607/t20260703_574946.html",
    },
    # ── 县政府班子: 常务副县长 / 副县长 ──
    {
        "id": 3,
        "name": "吴迪",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "乾安县人民政府",
        "source": "http://www.jlqa.gov.cn/",
    },
    {
        "id": 4,
        "name": "吴海涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "乾安县人民政府",
        "source": "http://www.jlqa.gov.cn/zwgk/zwdt/202607/t20260722_575919.html",
    },
    {
        "id": 5,
        "name": "许鑫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "乾安县人民政府",
        "source": "http://www.jlqa.gov.cn/",
    },
    {
        "id": 6,
        "name": "周志军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "乾安县人民政府",
        "source": "http://www.jlqa.gov.cn/",
    },
    {
        "id": 7,
        "name": "李环宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "乾安县人民政府",
        "source": "http://www.jlqa.gov.cn/",
    },
    {
        "id": 8,
        "name": "朱子岩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "乾安县人民政府",
        "source": "http://www.jlqa.gov.cn/",
    },
    {
        "id": 9,
        "name": "丁凯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "乾安县人民政府",
        "source": "http://www.jlqa.gov.cn/",
    },
    # ── 人大 / 法院 ──
    {
        "id": 10,
        "name": "邹立辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "乾安县人大常委会",
        "source": "http://www.jlqa.gov.cn/zwgk/zwdt/20260701/t20260701_574629.html",
    },
    {
        "id": 11,
        "name": "丛峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人民法院党组书记、代院长",
        "current_org": "乾安县人民法院",
        "source": "http://www.jlqa.gov.cn/zwgk/zwdt/202607/t20260730_576287.html",
    },
    # ── 前任 / 历史 ──
    {
        "id": 12,
        "name": "王立国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "曾任乾安县县长 (2021-2023)",
        "current_org": "",
        "source": "http://www.jlqa.gov.cn/",
    },
    # ── 跨县交流节点 (扶余市报告证实) ──
    {
        "id": 13,
        "name": "于静涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "曾在乾安县挂职副县长 (2023)",
        "current_org": "",
        "source": "report/20260725-扶余市-领导班子工作关系网络调查报告.md",
    },
    {
        "id": 14,
        "name": "郭丽明",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1980.08",
        "birthplace": "吉林省松原市长岭县",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "曾在乾安县人大副主任；现任扶余市副市长（省工信厅挂职）",
        "current_org": "扶余市人民政府",
        "source": "report/20260725-扶余市-领导班子工作关系网络调查报告.md",
    },
    {
        "id": 15,
        "name": "孙鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "曾在乾安县驻村第一书记",
        "current_org": "",
        "source": "report/20260725-扶余市-领导班子工作关系网络调查报告.md",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共乾安县委员会", "type": "党委", "level": "县处级",
     "parent": "中共松原市委员会", "location": "吉林省松原市乾安县"},
    {"id": 2, "name": "乾安县人民政府", "type": "政府", "level": "县处级",
     "parent": "松原市人民政府", "location": "吉林省松原市乾安县"},
    {"id": 3, "name": "乾安县人大常委会", "type": "人大", "level": "县处级",
     "parent": "松原市人大常委会", "location": "吉林省松原市乾安县"},
    {"id": 4, "name": "乾安县人民法院", "type": "政法", "level": "县处级",
     "parent": "松原市中级人民法院", "location": "吉林省松原市乾安县"},
    {"id": 5, "name": "扶余市人民政府", "type": "政府", "level": "县处级",
     "parent": "松原市人民政府", "location": "吉林省松原市扶余市"},
    {"id": 6, "name": "松原市人民政府", "type": "政府", "level": "地级市",
     "parent": "吉林省人民政府", "location": "吉林省松原市"},
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 陈锐_县委书记兼县长
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "约2025年", "end_date": "present",
     "rank": "正处级", "note": "主持乾安县委常委会 (2026-07-13, 2026-08-04 官方要闻); 党政一肩挑"},
    {"person_id": 1, "org_id": 2, "title": "县长 (兼)", "start_date": "约2025年", "end_date": "present",
     "rank": "正处级", "note": "政府机构页列县长; 2026年面向县府工作亲自督导防汛/民生/集中整治"},
    # 刘小刚_县委副书记
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present",
     "rank": "副处级", "note": "2026-06-30 文艺汇演出席; 2026-07-22 陪同陈锐调研集中整治"},
    # 吴迪_常务副县长
    {"person_id": 3, "org_id": 2, "title": "县委常委、常务副县长", "start_date": "2026年", "end_date": "present",
     "rank": "副处级", "note": "2026-08 政府机构页常务副县长; 于振军离任后接任"},
    # 吴海涛_常委副县长
    {"person_id": 4, "org_id": 2, "title": "县委常委、副县长", "start_date": "2026年", "end_date": "present",
     "rank": "副处级", "note": "2026-07-22 陪同陈锐调研集中整治"},
    # 各副县长
    {"person_id": 5, "org_id": 2, "title": "副县长", "start_date": "2026年", "end_date": "present",
     "rank": "副处级", "note": "2026-08 政府机构页"},
    {"person_id": 6, "org_id": 2, "title": "副县长", "start_date": "2026年", "end_date": "present",
     "rank": "副处级", "note": "2026-08 政府机构页"},
    {"person_id": 7, "org_id": 2, "title": "副县长", "start_date": "2026年", "end_date": "present",
     "rank": "副处级", "note": "2026-08 政府机构页"},
    {"person_id": 8, "org_id": 2, "title": "副县长", "start_date": "2026年", "end_date": "present",
     "rank": "副处级", "note": "2026-08 政府机构页"},
    {"person_id": 9, "org_id": 2, "title": "副县长", "start_date": "2026年", "end_date": "present",
     "rank": "副处级", "note": "2026-08 政府机构页"},
    # 人大 / 法院
    {"person_id": 10, "org_id": 3, "title": "县人大常委会主任", "start_date": "", "end_date": "present",
     "rank": "正处级", "note": "2026-06-30 文艺汇演出席"},
    {"person_id": 11, "org_id": 4, "title": "县人民法院党组书记、代院长", "start_date": "2026年", "end_date": "present",
     "rank": "副处级", "note": "2026-07-22 接待松原中院调研"},
    # 前任县长
    {"person_id": 12, "org_id": 2, "title": "县长", "start_date": "2021年前", "end_date": "2023年及以后",
     "rank": "正处级", "note": "2021-02 至 2023-03 可考在任县长"},
    # 跨县交流
    {"person_id": 13, "org_id": 2, "title": "挂职副县长", "start_date": "2023年", "end_date": "2023年", "rank": "副处级",
     "note": "省委办→乾安挂职副县长→松原市委办→扶余市"},
    {"person_id": 14, "org_id": 3, "title": "县人大副主任 (曾任) / 扶余市副市长",
     "start_date": "", "end_date": "", "rank": "副处级", "note": "乾安人大副主任→(省工信厅挂职)→扶余市政府"},
    {"person_id": 15, "org_id": 2, "title": "驻村第一书记 (曾在乾安)", "start_date": "", "end_date": "",
     "rank": "", "note": "乾安驻村第一书记→扶余市"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 陈锐 ↔ 刘小刚 (县委班子核心)
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "县委书记与专职县委副书记，县委班子核心成员",
     "overlap_org": "中共乾安县委员会", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "县委书记与县委副书记工作搭档", "overlap_org": "中共乾安县委员会", "overlap_period": "2025-2026"},
    # 陈锐 ↔ 县政府班子
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "县长(兼)与常务副县长工作搭档", "overlap_org": "乾安县人民政府", "overlap_period": "截至2026-08"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "县长(兼)与常委副县长工作搭档", "overlap_org": "乾安县人民政府", "overlap_period": "截至2026-08"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "县长(兼)与副县长", "overlap_org": "乾安县人民政府", "overlap_period": "截至2026-08"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "县长(兼)与副县长", "overlap_org": "乾安县人民政府", "overlap_period": "截至2026-08"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "县长(兼)与副县长", "overlap_org": "乾安县人民政府", "overlap_period": "截至2026-08"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "县长(兼)与副县长", "overlap_org": "乾安县人民政府", "overlap_period": "截至2026-08"},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "县长(兼)与副县长", "overlap_org": "乾安县人民政府", "overlap_period": "截至2026-08"},
    # 常务副县长 ↔ 各副 (县政府班子同僚)
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "县政府领导班子同事", "overlap_org": "乾安县人民政府", "overlap_period": "截至2026-08"},
    {"person_a": 3, "person_b": 5, "type": "overlap", "context": "县政府领导班子同事", "overlap_org": "乾安县人民政府", "overlap_period": "截至2026-08"},
    {"person_a": 3, "person_b": 6, "type": "overlap", "context": "县政府领导班子同事", "overlap_org": "乾安县人民政府", "overlap_period": "截至2026-08"},
    {"person_a": 3, "person_b": 7, "type": "overlap", "context": "县政府领导班子同事", "overlap_org": "乾安县人民政府", "overlap_period": "截至2026-08"},
    {"person_a": 3, "person_b": 8, "type": "overlap", "context": "县政府领导班子同事", "overlap_org": "乾安县人民政府", "overlap_period": "截至2026-08"},
    {"person_a": 3, "person_b": 9, "type": "overlap", "context": "县政府领导班子同事", "overlap_org": "乾安县人民政府", "overlap_period": "截至2026-08"},
    # 陈锐 ↔ 人大主任
    {"person_a": 1, "person_b": 10, "type": "overlap",
     "context": "县四家班子主要成员(党政+人大)", "overlap_org": "中共乾安县委员会/乾安县人大常委会", "overlap_period": "截至2026-08"},
    # 前任交接: 县长 王立国 → 陈锐 (党政权力交接, 一肩挑过渡)
    {"person_a": 1, "person_b": 12, "type": "predecessor_successor",
     "context": "陈锐接任一肩挑前曾任县长的王立国所担县令序 (县令交接链条)", "overlap_org": "乾安县人民政府",
     "overlap_period": "2023-2025 过渡", "confidence": "plausible"},
    # 跨县交流: 于静涛/郭丽明/孙鹏 与 乾安
    {"person_a": 13, "person_b": 1, "type": "overlap",
     "context": "于静涛曾在乾安挂职副县长, 与乾安县班子共事", "overlap_org": "乾安县人民政府",
     "overlap_period": "2023", "confidence": "confirmed"},
    {"person_a": 14, "person_b": 1, "type": "overlap",
     "context": "郭丽明曾任乾安人大副主任, 与乾安县班子共事", "overlap_org": "乾安县人大常委会",
     "overlap_period": "2020s", "confidence": "confirmed"},
    {"person_a": 15, "person_b": 1, "type": "overlap",
     "context": "孙鹏曾在乾安驻村第一书记, 乾与基层协同", "overlap_org": "乾安县", "overlap_period": "2020s",
     "confidence": "confirmed"},
    # 跨县交流 (扶余→乾安, 突出交流节点) — 反映松原市县际干部池
    {"person_a": 14, "person_b": 15, "type": "overlap",
     "context": "郭丽明(乾安人大+) 与 孙鹏(乾安驻村+) 同有乾安经历, 且先后到扶余市", "overlap_org": "松原市(扶余/乾安)",
     "overlap_period": "2020s", "confidence": "confirmed"},
]

# ══════════════════════════════════════════════════════════════════════════════
# HELPERS: source register + person JSON
# ══════════════════════════════════════════════════════════════════════════════


def make_source_register() -> list[dict]:
    return [
        {"id": "S001", "title": "乾安县人民政府官网·政府机构(班子清单)",
         "url": "http://www.jlqa.gov.cn/", "publisher": "乾安县人民政府", "published_at": "",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "县长: 陈锐; 常务副县长: 吴迪; 副县长: 许鑫/吴海涛/周志军/李环宇/朱子岩/丁凯"},
        {"id": "S002", "title": "县委常委会召开会议 (2026-08-06)",
         "url": "http://www.jlqa.gov.cn/zwgk/zwdt/202608/t20260806_576628.html", "publisher": "乾安县融媒体中心",
         "published_at": "2026-08-04", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "''8月4日，县委书记陈锐主持召开县委常委会会议''"},
        {"id": "S003", "title": "县委常委会召开会议 (2026-07-14)",
         "url": "http://www.jlqa.gov.cn/zwgk/zwdt/202607/t20260714_575527.html", "publisher": "乾安县融媒体中心",
         "published_at": "2026-07-13", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "''7月13日，县委书记陈锐主持召开县委常委会会议''"},
        {"id": "S004", "title": "陈锐调研督导群众身边不正之风和腐败问题集中整治工作",
         "url": "http://www.jlqa.gov.cn/zwgk/zwdt/202607/t20260722_575919.html", "publisher": "乾安县融媒体中心",
         "published_at": "2026-07-22", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "''县委书记陈锐...县委副书记刘小刚，县委常委、副县长吴海涛陪同调研''"},
        {"id": "S005", "title": "乾安举办庆祝建党105周年文艺汇演",
         "url": "http://www.jlqa.gov.cn/zwgk/zwdt/202607/t20260701_574629.shtml", "publisher": "乾安县融媒体中心",
         "published_at": "2026-07-01", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "''县委书记陈锐，县人大常委会主任邹立辉，县委副书记刘小刚及在家县级领导'' 出席"},
        {"id": "S006", "title": "松原市中级人民法院党组书记、院长周兴志到乾安县人民法院调研",
         "url": "http://www.jlqa.gov.cn/zwgk/zwdt/202607/t20260730_576287.html", "publisher": "乾安县融媒体中心",
         "published_at": "2026-07-25", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "''乾安县人民法院党组书记、代院长丛峰陪同调研''"},
        {"id": "S007", "title": "王立国检查乾安县征兵体检工作 (2021)",
         "url": "http://www.jlqa.gov.cn/tpxw1/202102/t20210225_424800.html", "publisher": "乾安县融媒体中心",
         "published_at": "2021-02-24", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "2021-02 县长王立国活动; 政府机构页列县长王立国/常务黄举明/副县长袁向江等"},
        {"id": "S008", "title": "乾安县第十九届人大常委会第七次会议召开 (2023)",
         "url": "http://www.jlqa.gov.cn/tpxw1/202307/t20230711_500367.html", "publisher": "乾安县融媒体中心",
         "published_at": "2023-03-18", "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "2023-03 政府机构页: 县长王立国/常务徐兴文/副县长于振军/于健/曲志涛/张喜军/于静涛/王军"},
        {"id": "S009", "title": "扶余市领导班子工作关系网络调查报告",
         "url": "report/20260725-扶余市-领导班子工作关系网络调查报告.md", "publisher": "gov-relation 内部报告",
         "published_at": "2026-07-25", "accessed_at": AS_OF, "source_type": "database", "reliability": "medium",
         "notes": "证实 于静涛(乾安挂职副县长)→扶余; 郭丽明(乾安人大副主任)→扶余; 孙鹏(乾安驻村)→扶余; 乾安为扶余首位交流节点"},
        {"id": "S010", "title": "松原市人民政府网·县区动态",
         "url": "https://www.jlsy.gov.cn/", "publisher": "松原市人民政府", "published_at": "",
         "accessed_at": AS_OF, "source_type": "official", "reliability": "high",
         "notes": "乾安县/大布苏镇 农业品牌动态; 确认乾安为松原市辖县"},
    ]


def generate_person_json(job: str, name: str) -> dict:
    pid = f"{_PID}_{name}"
    base = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {"province": "吉林省", "city": "松原市", "region": "乾安县",
                                "job": job, "task_id": "jilin_乾安县", "time_focus": "2023–2026"},
        "current_status": {"current_org": "", "administrative_rank": "正处级", "as_of": AS_OF,
                           "is_current_confirmed": True, "source_ids": ["S001"]},
        "organizations": [
            {"org_id": 1, "name": "中共乾安县委员会", "type": "党委", "level": "县处级",
             "location": "吉林省松原市乾安县"},
            {"org_id": 2, "name": "乾安县人民政府", "type": "政府", "level": "县处级",
             "location": "吉林省松原市乾安县"},
        ],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {"primary_specializations": [], "secondary_specializations": [],
                                 "career_pattern": "cross_county_rotation", "systems_experience": [],
                                 "geographic_pattern": ["松原市"],
                                 "promotion_velocity": {"summary": "", "notable_fast_promotions": []}},
        "work_style_and_personality": {"public_style_indicators": [], "speech_themes": [],
                                       "management_signals": [],
                                       "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."},
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": make_source_register(),
        "open_questions": [],
    }
    base["identity"] = {}
    base["career_timeline"] = []

    if name == "陈锐":
        base["identity"] = {
            "person_id": pid, "name": "陈锐", "aliases": [], "gender": "男",
            "ethnicity": "汉族", "birth": "", "birthplace": "", "native_place": "",
            "education": [], "party_join": "中共党员", "work_start": "",
            "dedupe_keys": {"name_birth": "陈锐_", "name_birthplace": "陈锐_",
                            "official_profile_url": ""},
        }
        base["current_status"]["current_post"] = "县委书记（兼县长，党政一肩挑）"
        base["current_status"]["current_org"] = "中共乾安县委员会"
        base["current_status"]["source_ids"] = ["S001", "S002", "S003"]
        base["career_timeline"] = [
            {"start": "unknown", "end": "2025年前", "org": "", "title": "陈锐任乾安县委书记前职务",
             "level": "", "location": "", "system": "party", "rank": "",
             "is_key_promotion": False, "notes": "公开资料未还原到任前履历 (疑为松原市直或松原其他县区交流干部)", "confidence": "unverified",
             "source_ids": []},
            {"start": "约2025年", "end": "present", "org": "中共乾安县委员会", "title": "县委书记",
             "level": "正处级", "location": "吉林省松原市乾安县", "system": "party", "rank": "正处级",
             "is_key_promotion": True, "notes": "党政一肩挑(兼县长); 2026-06/07/08 主持县委常委会、督导集中整治/防汛/民生", "confidence": "confirmed",
             "source_ids": ["S002", "S003", "S004"]},
        ]
        base["relationships"] = [
            {"person": "刘小刚", "person_id": f"{_PID}_刘小刚", "relationship_type": "superior_subordinate",
             "strength": "medium", "evidence": "县委书记与县委副书记, 同框出席县委会议/调研", "overlap_org": "中共乾安县委员会",
             "overlap_period": "2025-2026", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004"]},
            {"person": "王立国", "person_id": f"{_PID}_王立国", "relationship_type": "predecessor_successor",
             "strength": "medium", "evidence": "陈锐接任县长一职前, 王立国曾任县长 (2021-2023)", "overlap_org": "乾安县人民政府",
             "overlap_period": "2023-2025 过渡", "direction": "undirected", "confidence": "plausible", "source_ids": ["S007", "S008"]},
        ]
        base["governance_record"] = [
            {"period": "2026年7月", "domain": "discipline",
             "achievement_or_event": "调研督导群众身边不正之风和腐败问题集中整治工作, 严查农村集体'三资'管理、信访化解",
             "role_in_event": "县委书记", "measurable_outcome": "部署高标准农田长效管护与信访实质性化解", "location": "乾安县",
             "confidence": "confirmed", "source_ids": ["S004"]},
            {"period": "2026年7月", "domain": "other",
             "achievement_or_event": "带领县委常委会传达贯彻中央政治局会议精神, 研究基础教育布局/改革发展",
             "role_in_event": "县委书记", "measurable_outcome": "部署县域教育资源配置与核心机制", "location": "乾安县",
             "confidence": "confirmed", "source_ids": ["S002"]},
        ]
        base["professional_profile"]["career_pattern"] = "cross_county_rotation"
        base["professional_profile"]["geographic_pattern"] = ["松原市"]
        base["professional_profile"]["primary_specializations"] = ["党的建设", "县域治理", "纪检监察/民生整治"]
        base["work_style_and_personality"]["public_style_indicators"] = [
            {"trait": "discipline_oriented", "evidence": "多次亲自抓群众身边不正之风和腐败问题集中整治、'三资'管理", "confidence": "confirmed", "source_ids": ["S004"]}
        ]
        base["risk_and_integrity_signals"] = [
            {"type": "none_found", "description": "至 2026-08 未检索到陈锐的纪律处分/审计/负面报道信号", "date": AS_OF,
             "confidence": "confirmed", "source_ids": []}
        ]
        base["confidence_summary"] = {
            "identity": "unverified", "current_role": "confirmed", "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "陈锐的出生/籍贯/学历/入党与参工时间、任县委书记前履历、精确到任时间节点"}
        base["open_questions"] = [
            {"priority": "critical", "question": "陈锐任乾安县委书记兼县长前的完整履历与职务？",
             "why_it_matters": "还原核心一把手履历", "suggested_queries": ["陈锐 简历 乾安", "陈锐 任前公示"],
             "last_attempted": AS_OF},
            {"priority": "high", "question": "陈锐何时兼县长/接任县委书记？前任县委书记(一肩挑前)是谁、去向？",
             "why_it_matters": "精确交接与权力结构", "suggested_queries": ["乾安县 前任县委书记 卸任", "乾安县 县委书记 任命 2025"],
             "last_attempted": AS_OF},
            {"priority": "high", "question": "陈锐出生/籍贯/毕业院校？",
             "why_it_matters": "身份去重与完整档案", "suggested_queries": ["陈锐 简历"], "last_attempted": AS_OF},
        ]
        return base

    # ── 吴迪 / 刘小刚 / 邹立辉 (核心副职 - 用精简字段)
    base["identity"] = {
        "person_id": pid, "name": name, "aliases": [], "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "native_place": "",
        "education": [], "party_join": "中共党员", "work_start": "",
        "dedupe_keys": {"name_birth": f"{name}_", "name_birthplace": f"{name}_",
                        "official_profile_url": ""},
    }
    base["current_status"]["source_ids"] = ["S001"]

    if name == "刘小刚":
        base["current_status"]["current_post"] = "县委副书记"
        base["current_status"]["current_org"] = "中共乾安县委员会"
        base["career_timeline"] = [
            {"start": "unknown", "end": "present", "org": "中共乾安县委员会", "title": "县委副书记",
             "level": "副处级", "location": "吉林省松原市乾安县", "system": "party", "rank": "副处级",
             "is_key_promotion": False, "notes": "2026-06/07 官方要闻可考在任 (专职副书记)", "confidence": "confirmed",
             "source_ids": ["S005", "S004"]},
        ]
        base["relationships"] = [
            {"person": "陈锐", "person_id": f"{_PID}_陈锐", "relationship_type": "superior_subordinate",
             "strength": "medium", "evidence": "县委副书记与县委书记工作搭档", "overlap_org": "中共乾安县委员会",
             "overlap_period": "2025-2026", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004"]},
        ]
        base["professional_profile"]["career_pattern"] = "party"
        base["confidence_summary"] = {"identity": "unverified", "current_role": "confirmed",
                                      "career_completeness": "thin", "relationship_confidence": "medium",
                                      "biggest_gap": "刘小刚完整履历与到任前职务"}
        base["open_questions"] = [
            {"priority": "high", "question": "刘小刚任乾安县委副书记前职务与完整履历?", "why_it_matters": "还原核心副书记轨迹",
             "suggested_queries": ["乾安县 县委副书记 刘小刚"], "last_attempted": AS_OF},
        ]
        return base

    if name == "吴迪":
        base["identity"]["gender"] = "男"
        base["current_status"]["current_post"] = "县委常委、常务副县长"
        base["current_status"]["current_org"] = "乾安县人民政府"
        base["current_status"]["administrative_rank"] = "副处级"
        base["career_timeline"] = [
            {"start": "2026年", "end": "present", "org": "乾安县人民政府", "title": "县委常委、常务副县长",
             "level": "副处级", "location": "吉林省松原市乾安县", "system": "government", "rank": "副处级",
             "is_key_promotion": True, "notes": "2026-08 政府机构页常务副县长", "confidence": "confirmed", "source_ids": ["S001"]},
        ]
        base["relationships"] = [
            {"person": "陈锐", "person_id": f"{_PID}_陈锐", "relationship_type": "superior_subordinate",
             "strength": "medium", "evidence": "常务副县长与县长(兼)工作搭档", "overlap_org": "乾安县人民政府",
             "overlap_period": "截至2026-08", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
        ]
        base["confidence_summary"] = {"identity": "unverified", "current_role": "confirmed",
                                      "career_completeness": "thin", "relationship_confidence": "medium",
                                      "biggest_gap": "吴迪出生/籍贯/履历及任常务前职务"}
        base["open_questions"] = [
            {"priority": "high", "question": "吴迪任常务副县长前职务与完整履历?", "why_it_matters": "还原政府常务与前任权属",
             "suggested_queries": ["乾安县 常务副县长 吴迪"], "last_attempted": AS_OF},
        ]
        return base

    if name == "邹立辉":
        base["identity"]["gender"] = "男"
        base["current_status"]["current_post"] = "县人大常委会主任"
        base["current_status"]["current_org"] = "乾安县人大常委会"
        base["current_status"]["administrative_rank"] = "正处级"
        base["current_status"]["source_ids"] = ["S005"]
        base["career_timeline"] = [
            {"start": "unknown", "end": "present", "org": "乾安县人大常委会", "title": "县人大常委会主任",
             "level": "正处级", "location": "吉林省松原市乾安县", "system": "人大", "rank": "正处级",
             "is_key_promotion": False, "notes": "2026-06-30 文艺汇演出席", "confidence": "confirmed", "source_ids": ["S005"]},
        ]
        base["confidence_summary"] = {"identity": "unverified", "current_role": "confirmed",
                                      "career_completeness": "thin", "relationship_confidence": "low",
                                      "biggest_gap": "邹立辉履历/出生"}
        base["open_questions"] = [
            {"priority": "medium", "question": "邹立辉任县人大常委会主任前履历?", "why": "还原四大班子",
             "suggested_queries": ["乾安县 人大常委会主任 邹立辉"], "last_attempted": AS_OF},
        ]
        return base

    # fallback (副县长/其他) - 精简
    base["current_status"]["source_ids"] = ["S001"]
    base["career_timeline"] = [
        {"start": "2026年", "end": "present", "org": "乾安县人民政府", "title": "副县长",
         "level": "副处级", "location": "吉林省松原市乾安县", "system": "government", "rank": "副处级",
         "is_key_promotion": False, "notes": "2026-08 政府机构页", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    base["confidence_summary"] = {"identity": "unverified", "current_role": "confirmed",
                                  "career_completeness": "thin", "relationship_confidence": "low",
                                  "biggest_gap": f"{name} 出生/籍贯/履历"}
    base["open_questions"] = [
        {"priority": "medium", "question": f"{name}任乾安县副县长前履历与身份?", "why": "完整政府班子档案",
         "suggested_queries": [f"乾安县 副县长 {name}"], "last_attempted": AS_OF},
    ]
    return base


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import os
    # remove stale outputs before each run
    for p in (DB_PATH, GEXF_PATH):
        if p.exists():
            try:
                p.unlink()
            except OSError:
                pass

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # Write person JSON files (核心一把手陈锐 + 2-3 班子成员)
    for job, name in [("县委书记", "陈锐"), ("县委副书记", "刘小刚"), ("常务副县长", "吴迪"), ("县人大常委会主任", "邹立辉")]:
        data = generate_person_json(job, name)
        fname = f"{TODAY}-吉林省-松原市-{job}-{name}.json"
        fpath = PERSONS_DIR / fname
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"  Wrote {fpath}")

    print(f"\nDone. Output files:")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Person JSONs in: {PERSONS_DIR}")