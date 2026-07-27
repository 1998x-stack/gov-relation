#!/usr/bin/env python3
"""新乡市红旗区领导班子工作关系网络 — 数据构建脚本。

等级: 市辖区
调查日期: 2026-07-24
信息来源:
  - 红旗区人民政府网站 (http://hqq.gov.cn)
  - 红旗区政府领导页面 (http://hqq.gov.cn/Leader)
  - 中国共产党新乡市红旗区第十五次代表大会新闻
  - 新乡市红旗区第十五届人民代表大会第八次会议新闻
"""

from __future__ import annotations

import sqlite3  # used by gov_relation.runner
import sys
from datetime import datetime
from pathlib import Path

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Config ────────────────────────────────────────────────────────────────────
SLUG = "红旗区"
TODAY = "2026-07-24"
STAGING = Path(__file__).resolve().parent

DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────────────
# Person IDs: 1xxx = party committee, 2xxx = government, 3xxx = other

persons = [
    # ═══════════════════════════════════════════════════════════════════════
    # 1. 刘怀斌 — 区委书记
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1001,
        "name": "刘怀斌",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "红旗区委书记",
        "current_org": "中共新乡市红旗区委员会",
        "source": "http://hqq.gov.cn/News/info/30021",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 2. 张明强 — 区委副书记、区长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1002,
        "name": "张明强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年3月",
        "birthplace": "",
        "education": "在职研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "红旗区委副书记、区政府区长、党组书记",
        "current_org": "红旗区人民政府",
        "source": "http://hqq.gov.cn/Leader",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 3. 李向军 — 区委副书记
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1003,
        "name": "李向军",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "红旗区委副书记",
        "current_org": "中共新乡市红旗区委员会",
        "source": "http://hqq.gov.cn/News/info/30021",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 4. 万鹏 — 区委常委、组织部部长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1004,
        "name": "万鹏",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "红旗区委常委、组织部部长",
        "current_org": "中共新乡市红旗区委员会组织部",
        "source": "http://hqq.gov.cn/News/info/30021",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 5. 宋红锦 — 区委常委、纪委书记、监委主任
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1005,
        "name": "宋红锦",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "红旗区委常委、纪委书记、区监察委员会主任",
        "current_org": "中共新乡市红旗区纪律检查委员会",
        "source": "http://hqq.gov.cn/News/info/30021",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 6. 张传涛 — 区委常委
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1006,
        "name": "张传涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "红旗区委常委",
        "current_org": "中共新乡市红旗区委员会",
        "source": "http://hqq.gov.cn/News/info/30021",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 7. 孙俊娅 — 区委常委
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1007,
        "name": "孙俊娅",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "红旗区委常委",
        "current_org": "中共新乡市红旗区委员会",
        "source": "http://hqq.gov.cn/News/info/30021",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 8. 朱林静 — 区委常委
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1008,
        "name": "朱林静",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "红旗区委常委",
        "current_org": "中共新乡市红旗区委员会",
        "source": "http://hqq.gov.cn/News/info/30021",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 9. 李军 — 区委常委
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1009,
        "name": "李军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "红旗区委常委",
        "current_org": "中共新乡市红旗区委员会",
        "source": "http://hqq.gov.cn/News/info/30021",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 10. 付中一 — 区委常委、常务副区长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1010,
        "name": "付中一",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1989年6月",
        "birthplace": "",
        "education": "博士研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "红旗区委常委、区政府常务副区长",
        "current_org": "红旗区人民政府",
        "source": "http://hqq.gov.cn/Leader",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 11. 李伟 — 区委常委、副区长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 1011,
        "name": "李伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1988年9月",
        "birthplace": "",
        "education": "本科",
        "party_join": "",
        "work_start": "",
        "current_post": "红旗区委常委、区政府副区长",
        "current_org": "红旗区人民政府",
        "source": "http://hqq.gov.cn/Leader",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 12. 张磊 — 副区长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 2001,
        "name": "张磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年11月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "红旗区政府副区长",
        "current_org": "红旗区人民政府",
        "source": "http://hqq.gov.cn/Leader",
        "note": "无党派",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 13. 孔祥 — 副区长、红旗公安分局局长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 2002,
        "name": "孔祥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年8月",
        "birthplace": "",
        "education": "大专",
        "party_join": "",
        "work_start": "",
        "current_post": "红旗区政府副区长、红旗公安分局局长",
        "current_org": "红旗区人民政府/新乡市公安局红旗分局",
        "source": "http://hqq.gov.cn/Leader",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 14. 陈理想 — 副区长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 2003,
        "name": "陈理想",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年5月",
        "birthplace": "",
        "education": "本科",
        "party_join": "",
        "work_start": "",
        "current_post": "红旗区政府副区长",
        "current_org": "红旗区人民政府",
        "source": "http://hqq.gov.cn/Leader",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 15. 张献莉 — 副区长
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 2004,
        "name": "张献莉",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1981年8月",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "红旗区政府副区长",
        "current_org": "红旗区人民政府",
        "source": "http://hqq.gov.cn/Leader",
    },
    # ═══════════════════════════════════════════════════════════════════════
    # 16. 郭潇漪 — 区人大常委会主任
    # ═══════════════════════════════════════════════════════════════════════
    {
        "id": 3001,
        "name": "郭潇漪",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "红旗区人大常委会主任",
        "current_org": "红旗区人民代表大会常务委员会",
        "source": "http://hqq.gov.cn/News/info/30024",
    },
]

# ── Organizations ────────────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中共新乡市红旗区委员会",
        "type": "党委",
        "level": "县处级",
        "location": "河南省新乡市红旗区",
    },
    {
        "id": 2,
        "name": "红旗区人民政府",
        "type": "政府",
        "level": "县处级",
        "location": "河南省新乡市红旗区",
    },
    {
        "id": 3,
        "name": "中共新乡市红旗区纪律检查委员会",
        "type": "党委",
        "level": "县处级",
        "location": "河南省新乡市红旗区",
    },
    {
        "id": 4,
        "name": "红旗区人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "location": "河南省新乡市红旗区",
    },
    {
        "id": 5,
        "name": "红旗区监察委员会",
        "type": "党委",
        "level": "县处级",
        "location": "河南省新乡市红旗区",
    },
    {
        "id": 6,
        "name": "中共新乡市红旗区委员会组织部",
        "type": "党委",
        "level": "乡科级",
        "location": "河南省新乡市红旗区",
    },
    {
        "id": 7,
        "name": "新乡市公安局红旗分局",
        "type": "政府",
        "level": "乡科级",
        "location": "河南省新乡市红旗区",
    },
    {
        "id": 8,
        "name": "红旗区政协",
        "type": "政协",
        "level": "县处级",
        "location": "河南省新乡市红旗区",
    },
    {
        "id": 9,
        "name": "红旗区先进制造业开发区",
        "type": "开发区",
        "level": "县处级",
        "location": "河南省新乡市红旗区",
    },
]

# ── Positions ────────────────────────────────────────────────────────────────

positions = [
    # 刘怀斌
    {"person_id": 1001, "org_id": 1, "title": "红旗区委书记", "start": "2026-06", "end": "present", "rank": "正处级", "note": "2026年6月25日区委十五届一次全会当选"},
    # 张明强
    {"person_id": 1002, "org_id": 2, "title": "红旗区区长", "start": "2026-06", "end": "present", "rank": "正处级", "note": "2026年6月29日区十五届人大八次会议当选"},
    {"person_id": 1002, "org_id": 1, "title": "红旗区委副书记", "start": "2026-06", "end": "present", "rank": "副处级", "note": "区委十五届一次全会当选副书记"},
    # 李向军
    {"person_id": 1003, "org_id": 1, "title": "红旗区委副书记", "start": "2026-06", "end": "present", "rank": "副处级", "note": "区委十五届一次全会当选"},
    # 万鹏
    {"person_id": 1004, "org_id": 1, "title": "红旗区委常委", "start": "2026-06", "end": "present", "rank": "副处级", "note": "区委十五届一次全会当选"},
    {"person_id": 1004, "org_id": 6, "title": "红旗区委组织部部长", "start": "", "end": "present", "rank": "乡科级", "note": "推定"},
    # 宋红锦
    {"person_id": 1005, "org_id": 1, "title": "红旗区委常委", "start": "2026-06", "end": "present", "rank": "副处级", "note": "区委十五届一次全会当选"},
    {"person_id": 1005, "org_id": 3, "title": "红旗区纪委书记", "start": "", "end": "present", "rank": "副处级"},
    {"person_id": 1005, "org_id": 5, "title": "红旗区监察委员会主任", "start": "2026-06", "end": "present", "rank": "副处级", "note": "2026年6月29日区十五届人大八次会议当选"},
    # 张传涛
    {"person_id": 1006, "org_id": 1, "title": "红旗区委常委", "start": "2026-06", "end": "present", "rank": "副处级", "note": "区委十五届一次全会当选"},
    # 孙俊娅
    {"person_id": 1007, "org_id": 1, "title": "红旗区委常委", "start": "2026-06", "end": "present", "rank": "副处级", "note": "区委十五届一次全会当选"},
    # 朱林静
    {"person_id": 1008, "org_id": 1, "title": "红旗区委常委", "start": "2026-06", "end": "present", "rank": "副处级", "note": "区委十五届一次全会当选"},
    # 李军
    {"person_id": 1009, "org_id": 1, "title": "红旗区委常委", "start": "2026-06", "end": "present", "rank": "副处级", "note": "区委十五届一次全会当选"},
    # 付中一
    {"person_id": 1010, "org_id": 1, "title": "红旗区委常委", "start": "2026-06", "end": "present", "rank": "副处级", "note": "区委十五届一次全会当选"},
    {"person_id": 1010, "org_id": 2, "title": "红旗区常务副区长", "start": "", "end": "present", "rank": "副处级"},
    # 李伟
    {"person_id": 1011, "org_id": 1, "title": "红旗区委常委", "start": "2026-06", "end": "present", "rank": "副处级", "note": "区委十五届一次全会当选"},
    {"person_id": 1011, "org_id": 2, "title": "红旗区副区长", "start": "2026-06", "end": "present", "rank": "副处级", "note": "2026年6月29日区十五届人大八次会议当选"},
    # 张磊
    {"person_id": 2001, "org_id": 2, "title": "红旗区副区长", "start": "", "end": "present", "rank": "副处级", "note": "无党派"},
    # 孔祥
    {"person_id": 2002, "org_id": 2, "title": "红旗区副区长", "start": "", "end": "present", "rank": "副处级"},
    {"person_id": 2002, "org_id": 7, "title": "红旗公安分局局长", "start": "", "end": "present", "rank": "乡科级"},
    # 陈理想
    {"person_id": 2003, "org_id": 2, "title": "红旗区副区长", "start": "2026-06", "end": "present", "rank": "副处级", "note": "2026年6月29日区十五届人大八次会议当选"},
    # 张献莉
    {"person_id": 2004, "org_id": 2, "title": "红旗区副区长", "start": "2026-06", "end": "present", "rank": "副处级", "note": "2026年6月29日区十五届人大八次会议当选"},
    # 郭潇漪
    {"person_id": 3001, "org_id": 4, "title": "红旗区人大常委会主任", "start": "", "end": "present", "rank": "正处级"},
]

# ── Relationships ────────────────────────────────────────────────────────────

relationships = [
    # 刘怀斌 — 张明强 (搭档: 书记+区长)
    {
        "person_a": 1001,
        "person_b": 1002,
        "type": "superior_subordinate",
        "context": "刘怀斌任区委书记，张明强任区委副书记、区长，为党政正职搭档",
        "overlap_org": "中共新乡市红旗区委员会/红旗区人民政府",
        "overlap_period": "2026-06至今",
    },
    # 刘怀斌 — 李向军 (书记+副书记)
    {
        "person_a": 1001,
        "person_b": 1003,
        "type": "superior_subordinate",
        "context": "刘怀斌任区委书记，李向军任区委副书记",
        "overlap_org": "中共新乡市红旗区委员会",
        "overlap_period": "2026-06至今",
    },
    # 刘怀斌 — 万鹏 (书记+组织部长)
    {
        "person_a": 1001,
        "person_b": 1004,
        "type": "superior_subordinate",
        "context": "万鹏任区委常委、组织部部长，在区委常委会中受刘怀斌领导",
        "overlap_org": "中共新乡市红旗区委员会",
        "overlap_period": "2026-06至今",
    },
    # 刘怀斌 — 宋红锦 (书记+纪委书记)
    {
        "person_a": 1001,
        "person_b": 1005,
        "type": "superior_subordinate",
        "context": "宋红锦任区委常委、纪委书记、监委主任",
        "overlap_org": "中共新乡市红旗区委员会",
        "overlap_period": "2026-06至今",
    },
    # 张明强 — 付中一 (区长+常务副区长)
    {
        "person_a": 1002,
        "person_b": 1010,
        "type": "superior_subordinate",
        "context": "付中一任区委常委、常务副区长，协助张明强分管审计等工作",
        "overlap_org": "红旗区人民政府",
        "overlap_period": "至今",
    },
    # 张明强 — 李伟 (区长+副区长)
    {
        "person_a": 1002,
        "person_b": 1011,
        "type": "superior_subordinate",
        "context": "李伟任区委常委、副区长，在区政府班子中受张明强领导",
        "overlap_org": "红旗区人民政府",
        "overlap_period": "2026-06至今",
    },
    # 张明强 — 郭潇漪 (区长+人大主任)
    {
        "person_a": 1002,
        "person_b": 3001,
        "type": "overlap",
        "context": "人大会议期间张明强当选区长，郭潇漪以人大主任身份主持会议",
        "overlap_org": "红旗区第十五届人民代表大会",
        "overlap_period": "2026-06",
    },
    # 区委常委会全体成员
    {
        "person_a": 1001,
        "person_b": 1010,
        "type": "overlap",
        "context": "付中一与刘怀斌同为新一届区委常委",
        "overlap_org": "中共新乡市红旗区第十五届委员会常务委员会",
        "overlap_period": "2026-06至今",
    },
    {
        "person_a": 1002,
        "person_b": 1004,
        "type": "overlap",
        "context": "张明强与万鹏同为新一届区委常委",
        "overlap_org": "中共新乡市红旗区第十五届委员会常务委员会",
        "overlap_period": "2026-06至今",
    },
    {
        "person_a": 1002,
        "person_b": 1005,
        "type": "overlap",
        "context": "张明强与宋红锦同为新一届区委常委",
        "overlap_org": "中共新乡市红旗区第十五届委员会常务委员会",
        "overlap_period": "2026-06至今",
    },
    {
        "person_a": 1003,
        "person_b": 1004,
        "type": "overlap",
        "context": "李向军与万鹏同为新一届区委常委",
        "overlap_org": "中共新乡市红旗区第十五届委员会常务委员会",
        "overlap_period": "2026-06至今",
    },
    # 区政府班子成员
    {
        "person_a": 1010,
        "person_b": 1011,
        "type": "overlap",
        "context": "付中一与李伟同为区政府班子成员（常务副区长+副区长）",
        "overlap_org": "红旗区人民政府",
        "overlap_period": "2026-06至今",
    },
    {
        "person_a": 1011,
        "person_b": 2003,
        "type": "overlap",
        "context": "李伟与陈理想同为2026年6月当选的副区长",
        "overlap_org": "红旗区人民政府",
        "overlap_period": "2026-06至今",
    },
    {
        "person_a": 1011,
        "person_b": 2004,
        "type": "overlap",
        "context": "李伟与张献莉同为2026年6月当选的副区长",
        "overlap_org": "红旗区人民政府",
        "overlap_period": "2026-06至今",
    },
    # 孔祥 — 公安局
    {
        "person_a": 2002,
        "person_b": 2003,
        "type": "overlap",
        "context": "孔祥与陈理想同为副区长",
        "overlap_org": "红旗区人民政府",
        "overlap_period": "至今",
    },
]


# ═══════════════════════════════════════════════════════════════════════════
# Build
# ═══════════════════════════════════════════════════════════════════════════

def main() -> None:
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )


if __name__ == "__main__":
    main()
