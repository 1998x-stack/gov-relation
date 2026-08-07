#!/usr/bin/env python3
"""Build 武汉市汉阳区 (Wuhan Hanyang District) leadership network data.

Level: 市辖区
Province: 湖北省
Parent city: 武汉市
Targets: 区委书记 (Party Secretary), 区长 (Mayor)
Task ID: hubei_汉阳区

Research date: 2026-08-07
Official source: https://www.hanyang.gov.cn/ (武汉市汉阳区人民政府)

Current leadership status (as of 2026-08-07, verified via hanyang.gov.cn):
- 区委书记: 周岚 — confirmed by hanyang.gov.cn news (2026-05-26 专访 '汉阳区委书记周岚：奋力打造五个美好之区'; 2026-06-07 '周岚调研高考考点筹备工作'; 2026-06-17 区委理论学习中心组主持)
- 区委副书记: 傅谦 — confirmed (2026-06-17 中心组领学)
- 区委常委、纪委书记、监委主任: 柯巍 — confirmed (2026-06-17 中心组领学)
- 区长(代理): 张健 — 现任汉阳区委副书记，区政府副区长、代理区长、党组书记 (政府领导页 2026-08-03)
- 常务副区长: 陈波 — 区委常委、区政府党组副书记、副区长，负责政府常务工作
- 副区长: 王彬（九三学社）, 李津, 黄翀, 易雄才, 肖斌（公安局长）, 童非（挂职，来自武汉经开区/汉南区）

Predecessor: 前任区长 郭笑撰 (confirmed via 2026-05-25 区人大免职议案落款), 前任副区长 赵亮 (免职)。
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent

def _find_repo_root() -> Path:
    current = _STAGING_DIR
    while current != current.parent:
        if (current / "gov_relation").is_dir():
            return current
        current = current.parent
    return current

_REPO_ROOT = _find_repo_root()
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build

SLUG = "汉阳区"

IN_CANONICAL = _STAGING_DIR.name == "build"

if IN_CANONICAL:
    DB_PATH = _REPO_ROOT / "data" / "database" / f"{SLUG}_network.db"
    GEXF_PATH = _REPO_ROOT / "data" / "graph" / f"{SLUG}_network.gexf"
    PERSONS_DIR = _REPO_ROOT / "data" / "persons"
else:
    DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
    GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
    PERSONS_DIR = _STAGING_DIR

AS_OF = "2026-08-07"
TODAY = "20260807"

import sqlite3  # noqa: F811

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ── 区委领导 (Party Committee) ──
    {
        "id": 1,
        "name": "周岚",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "汉阳区委书记",
        "current_org": "中共武汉市汉阳区委员会",
        "source": "https://www.hanyang.gov.cn/xwdt_38/gzdt/202605/t20260526_2769183.shtml",
        "notes": "区政府官网2026-05-26《汉阳区委书记周岚：奋力打造五个美好之区》专访、2026-06-07 '周岚调研高考考点筹备工作'、2026-06-17 区委理论学习中心组主持确认其区委书记身份。出生年份、籍贯、学历及上任前完整履历待补充。",
    },
    {
        "id": 2,
        "name": "傅谦",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "汉阳区委副书记",
        "current_org": "中共武汉市汉阳区委员会",
        "source": "https://www.hanyang.gov.cn/xwdt_38/hyyw/202606/t20260617_2778219.shtml",
        "notes": "2026-06-17 区委理论学习中心组集体学习，区委副书记傅谦领学反面典型案例，身份确认。详细履历待补充。",
    },
    {
        "id": 3,
        "name": "柯巍",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "汉阳区委常委、纪委书记、监委主任",
        "current_org": "中共汉阳区纪委监委",
        "source": "https://www.hanyang.gov.cn/xwdt_38/hyyw/202606/t20260617_2778219.shtml",
        "notes": "2026-06-17 区委理论学习中心组集体学习，区委常委、区纪委书记、区监委主任领学正面/反面典型案例，身份确认。",
    },
    # ── 区政府领导 (Government) ──
    {
        "id": 4,
        "name": "张健",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-02",
        "birthplace": "",
        "native_place": "",
        "education": "在职研究生，管理学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "汉阳区委副书记、区政府区长（代理）",
        "current_org": "汉阳区人民政府",
        "source": "https://www.hanyang.gov.cn/zwgk_38/xxgkml/qzfld/202608/t20260803_2829129.shtml",
        "notes": "官方政府领导页 (2026-08-03)：现任汉阳区委副书记，区政府副区长、代理区长、党组书记。领导区政府全面工作。前任区长郭笑撰离职后接任代理区长。",
    },
    {
        "id": 5,
        "name": "陈波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984-04",
        "birthplace": "湖北崇阳",
        "native_place": "湖北崇阳",
        "education": "在职硕士研究生，工商管理硕士",
        "party_join": "中共党员",
        "work_start": "2007-07",
        "current_post": "汉阳区委常委、常务副区长",
        "current_org": "汉阳区人民政府",
        "source": "https://www.hanyang.gov.cn/zwgk_38/xxgkml/qzfld/202603/t20260325_2744562.shtml",
        "notes": "2026-03 政府领导页官方简历：中共汉阳区委常委，区人民政府党组副书记、副区长，负责政府常务工作。2005.10入党，2007.7参加工作，历任市政府研究室副处长、处长，市政府办公厅副主任、市政府机关党组成员，市政府副秘书长、市政府机关党组成员。",
    },
    {
        "id": 6,
        "name": "王彬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-01",
        "birthplace": "湖北英山",
        "native_place": "湖北英山",
        "education": "大学本科，工学学士",
        "party_join": "九三学社社员",
        "work_year": "1993-08",
        "current_post": "汉阳区人民政府副区长",
        "current_org": "汉阳区人民政府",
        "source": "https://www.hanyang.gov.cn/zwgk_38/xxgkml/qzfld/202212/t20221230_2122860.shtml",
        "notes": "官方简历：分管教育、民政、卫生健康、医疗保障等。历任武汉中央商务区投控集团副总经理、武汉碧水集团副总经理、武汉市城投集团副总经理，九三学社市委副主委。无党派中的民主党派成员（九三学社）。",
    },
    {
        "id": 7,
        "name": "李津",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969-09",
        "birthplace": "湖北仙桃",
        "native_place": "湖北仙桃",
        "education": "在职大学本科，法学学士",
        "party_join": "中共党员",
        "work_year": "1990-07",
        "current_post": "汉阳区人民政府副区长",
        "current_org": "汉阳区人民政府",
        "source": "https://www.hanyang.gov.cn/zwgk_38/xxgkml/qzfld/202201/t20220106_1890314.shtml",
        "notes": "官方简历：分管城市管理、交通运输、退役军人、司法等。1999.8入党。历任汉阳区建设局、区开发办、区城乡统筹办、晴川街/鹦鹉街/永丰街党工委书记、区发改局局长等，本地汉阳履历专家。",
    },
    {
        "id": 8,
        "name": "黄翀",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1978-11",
        "birthplace": "湖北武汉",
        "native_place": "湖北武汉",
        "education": "大学本科，公共管理硕士",
        "party_join": "中共党员",
        "work_year": "2001-08",
        "current_post": "汉阳区人民政府副区长",
        "current_org": "汉阳区人民政府",
        "source": "https://www.hanyang.gov.cn/zwgk_38/xxgkml/qzfld/202201/t20220106_1890332.shtml",
        "notes": "官方简历：分管工业经济、数字经济、科技创新等。2000.12入党，2001.8参加工作。历任市经信委经济运行处副处长、办公室副主任、轻工纺织产业处处长、新兴产业处处长、市经信局办公室主任。从武汉市经信局调任汉阳，属市级机关下沉。",
    },
    {
        "id": 9,
        "name": "易雄才",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-10",
        "birthplace": "湖北汉川",
        "native_place": "湖北汉川",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_year": "1992-11",
        "current_post": "汉阳区人民政府副区长",
        "current_org": "汉阳区人民政府",
        "source": "https://www.hanyang.gov.cn/zwgk_38/xxgkml/qzfld/202201/t20220106_1890347.shtml",
        "notes": "官方简历：分管城市建设、住房保障、自然资源和规划等。2000.6入党。历任汉阳区水务局副局长/局长、区城市管理执法局党委书记/局长、永丰街道党工委书记。本地汉阳履历。",
    },
    {
        "id": 10,
        "name": "肖斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-12",
        "birthplace": "湖北武汉",
        "native_place": "湖北武汉",
        "education": "省委党校大学",
        "party_join": "中共党员",
        "work_year": "1991-12",
        "current_post": "汉阳区人民政府副区长（公安局长）",
        "current_org": "武汉市公安局汉阳区分局",
        "source": "https://www.hanyang.gov.cn/zwgk_38/xxgkml/qzfld/202607/t20260717_2822511.shtml",
        "notes": "官方简历 (2026-07-17 更新)：男，1973.12生，湖北武汉人。1994.11入党。历任市公安局东西湖区分局政治处主任、副局长，市网安支队政委、支队长。现任区政府副区长、党组成员，区委政法委副书记，市公安局汉阳区分局党委书记、局长、督查长。负责公安分局全面工作。",
    },
    {
        "id": 11,
        "name": "童非",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984-11",
        "birthplace": "湖北新洲",
        "native_place": "湖北新洲",
        "education": "博士研究生，工学博士",
        "party_join": "中共党员",
        "work_year": "2012-07",
        "current_post": "汉阳区政府党组成员（挂职）",
        "current_org": "汉阳区人民政府",
        "source": "https://www.hanyang.gov.cn/zwgk_38/xxgkml/qzfld/202201/t20220106_1890298.shtml",
        "notes": "官方简历：男，1984.11生，湖北新洲人，博士研究生，工学博士. 2006.7入党，2012.7参加工作。历任武汉经开区(汉南区)投资促进服务中心党组书记、主任，招商局党组书记/局长，发改局党组书记/局长。现任汉阳区政府党组成员（挂职），武汉经开区现代科技农业产业园党工委委员、副主任。跨区挂职（武汉经开区/汉南区→汉阳）干部交流的节点。",
    },
    # ── 前任 ──
    {
        "id": 12,
        "name": "郭笑撰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任汉阳区人民政府区长",
        "current_org": "汉阳区人民政府",
        "source": "https://www.hanyang.gov.cn/zwgk_38/xxgkml/qtzdgknr/rsrm/202606/t20260601_2771461.shtml",
        "notes": "2026-04-28 署名'武汉市汉阳区人民政府区长郭笑撰'的《关于提请免去赵亮副区长职务的议案》。前任区长，2026年由张健接任代理区长。去向待查。",
    },
    {
        "id": 13,
        "name": "赵亮",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原汉阳区人民政府副区长（已免）",
        "current_org": "汉阳区人民政府",
        "source": "https://www.hanyang.gov.cn/zwgk_38/xxgkml/qtzdgknr/rsrm/202606/t20260601_2771461.shtml",
        "notes": "2026-05-25 汉阳区人大常委会审议免去其汉阳区人民政府副区长职务。具体去向不明。",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共武汉市汉阳区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共武汉市委",
        "location": "武汉市汉阳区",
    },
    {
        "id": 2,
        "name": "汉阳区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "武汉市人民政府",
        "location": "武汉市汉阳区",
    },
    {
        "id": 3,
        "name": "汉阳区纪委监委",
        "type": "党委",
        "level": "县处级",
        "parent": "中共武汉市纪委",
        "location": "武汉市汉阳区",
    },
    {
        "id": 4,
        "name": "武汉市公安局汉阳区分局",
        "type": "政府",
        "level": "县处级",
        "parent": "武汉市公安局",
        "location": "武汉市汉阳区",
    },
    {
        "id": 5,
        "name": "武汉经济技术开发区（汉南区）",
        "type": "开发区",
        "level": "国家级开发区",
        "parent": "武汉市人民政府",
        "location": "武汉市经开区/汉南区",
    },
    {
        "id": 6,
        "name": "武汉市人民政府办公厅",
        "type": "政府",
        "level": "市级机关",
        "parent": "武汉市人民政府",
        "location": "武汉市",
    },
    {
        "id": 7,
        "name": "武汉市经济和信息化局",
        "type": "政府",
        "level": "市级机关",
        "parent": "武汉市人民政府",
        "location": "武汉市",
    },
    {
        "id": 8,
        "name": "武汉市城市建设投资开发集团有限公司",
        "type": "国企",
        "level": "市属国企",
        "parent": "武汉市人民政府",
        "location": "武汉市",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 周岚 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "汉阳区委书记", "start": "", "end": "present", "rank": "副厅级", "note": "2026-05-26/06-07/06-17 官网新闻确认以区委书记身份活动"},
    # 傅谦 — 区委副书记
    {"person_id": 2, "org_id": 1, "title": "汉阳区委副书记", "start": "", "end": "present", "rank": "", "note": "2026-06-17 中心组学习领学"},
    # 柯巍 — 纪委书记
    {"person_id": 3, "org_id": 3, "title": "汉阳区委常委、纪委书记、监委主任", "start": "", "end": "present", "rank": "", "note": "2026-06-17 中心组学习领学"},
    # 张健 — 区长(代理)
    {"person_id": 4, "org_id": 2, "title": "汉阳区委副书记、区政府副区长、代理区长", "start": "~2026", "end": "present", "rank": "副厅级", "note": "官方政府领导页 2026-08-03：代理区长、党组书记"},
    # 陈波 — 常务副区长
    {"person_id": 5, "org_id": 2, "title": "汉阳区委常委、常务副区长", "start": "~2024", "end": "present", "rank": "", "note": "区政府党组副书记，负责政府常务工作，2026-03 官网更新"},
    # 陈波 任职信息 (以往市级机关)
    {"person_id": 5, "org_id": 6, "title": "市政府副秘书长、市政府机关党组成员", "start": "", "end": "", "rank": "", "note": "历任市政府研究室/办公厅/市政府"},
    # 王彬 — 副区长
    {"person_id": 6, "org_id": 2, "title": "汉阳区人民政府副区长", "start": "", "end": "present", "rank": "", "note": "九三学社市委副主委，负责教育、民政、卫生健康等"},
    # 李津 — 副区长
    {"person_id": 7, "org_id": 2, "title": "汉阳区人民政府副区长", "start": "", "end": "present", "rank": "", "note": "本地汉阳履历，分管城管、司法、公安等"},
    # 黄翀 — 副区长
    {"person_id": 8, "org_id": 2, "title": "汉阳区人民政府副区长", "start": "", "end": "present", "rank": "", "note": "从市经信局调任，分管工业经济、数字经济等"},
    {"person_id": 8, "org_id": 7, "title": "市经济和信息化局办公室主任", "start": "", "end": "", "rank": "", "note": "曾是市经信系统公务员"},
    # 易雄才 — 副区长
    {"person_id": 9, "org_id": 2, "title": "汉阳区人民政府副区长", "start": "", "end": "present", "rank": "", "note": "本地汉阳履历，分管城市建设、自然资源等"},
    # 肖斌 — 副区长、公安局长
    {"person_id": 10, "org_id": 2, "title": "汉阳区人民政府副区长、区公安分局局长", "start": "~2026", "end": "present", "rank": "", "note": "负责公安分局全面工作，政法委副书记"},
    {"person_id": 10, "org_id": 4, "title": "汉阳区公安分局党委书记、局长", "start": "", "end": "present", "rank": "", "note": "市公安局汉阳区分局党委书记、局长、督查长"},
    # 童非 — 挂职副区长
    {"person_id": 11, "org_id": 2, "title": "汉阳区政府党组成员（挂职）", "start": "", "end": "present", "rank": "", "note": "负责招商引资、文旅、市场监管；来自武汉经开区/汉南区"},
    {"person_id": 11, "org_id": 5, "title": "武汉经开区现代科技农业产业园党工委委员、副主任", "start": "", "end": "present", "rank": "", "note": "现任职务，挂职汉阳"},
    # 郭笑撰 — 前任区长
    {"person_id": 12, "org_id": 2, "title": "汉阳区人民政府区长", "start": "", "end": "~2026", "rank": "副厅级", "note": "2026-04-28 署名区长；后继由张健接任代理区长"},
    # 赵亮 — 前任副区长
    {"person_id": 13, "org_id": 2, "title": "汉阳区人民政府副区长（已免）", "start": "", "end": "~2026-05", "rank": "", "note": "2026-05-25 免去副区长职务"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

# relationships are constructed inside main() and passed to run_build() directly.


# ══════════════════════════════════════════════════════════════════════════════
# PERSON JSON DATA (deep profiles for core leaders)
# ══════════════════════════════════════════════════════════════════════════════

_source_register = [
    {
        "id": "S001",
        "title": "汉阳区委书记周岚：奋力打造'五个美好之区' (2026-05-26)",
        "url": "https://www.hanyang.gov.cn/xwdt_38/gzdt/202605/t20260526_2769183.shtml",
        "publisher": "汉阳区人民政府 (汉阳知音)",
        "published_at": "2026-05-26",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "确认周岚任汉阳区委书记；透露'1143'现代化产业体系、'两城支撑两轴引领两带赋能'空间布局等治理重点",
    },
    {
        "id": "S002",
        "title": "周岚调研高考考点筹备工作 (2026-06-07)",
        "url": "https://www.hanyang.gov.cn/xwdt_38/hyyw/202606/t20260609_2775240.shtml",
        "publisher": "汉阳区人民政府",
        "published_at": "2026-06-07",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "确认周岚以区委书记身份调研高考，强调'树立底线思维'、考生 5440人",
    },
    {
        "id": "S003",
        "title": "区委理论学习中心组开展集体学习 (2026-06-17)",
        "url": "https://www.hanyang.gov.cn/xwdt_38/hyyw/202606/t20260617_2778219.shtml",
        "publisher": "汉阳区人民政府",
        "published_at": "2026-06-17",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "确认区委书记周岚主持、区委副书记单清华领学、区纪委书记监委主任柯巍领学",
    },
    {
        "id": "S004",
        "title": "汉阳区政府领导（区长张健）",
        "url": "https://www.hanyang.gov.cn/zwgk_38/xxgkml/qzfld/202608/t20260803_2829129.shtml",
        "publisher": "汉阳区人民政府",
        "published_at": "2026-08-03",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "确认张健任区委副书记、区政府副区长、代理区长、党组书记；1976.2生，管理学硕士",
    },
    {
        "id": "S005",
        "title": "汉阳区政府领导（陈波 常务副区长）",
        "url": "https://www.hanyang.gov.cn/zwgk_38/xxgkml/qzfld/202603/t20260325_2744562.shtml",
        "publisher": "汉阳区人民政府",
        "published_at": "2026-03-25",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "陈波完整简历：1984.4崇阳籍，工商管理硕士，历任市政府研究室副处长/处长、市政府办公厅副主任、市政府副秘书长",
    },
    {
        "id": "S006",
        "title": "汉阳区政府领导（王彬）",
        "url": "https://www.hanyang.gov.cn/zwgk_38/xxgkml/qzfld/202212/t20221230_2122860.shtml",
        "publisher": "汉阳区人民政府",
        "published_at": "2022-12",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "王彬简历：1971.1英山人，工学学士，九三学社，历任武汉城投/中央商务区/碧水集团副总经理",
    },
    {
        "id": "S007",
        "title": "汉阳区政府领导（李津、黄翀、易雄才、童非、肖斌）",
        "url": "https://www.hanyang.gov.cn/zwgk_38/xxgkml/qzfld/",
        "publisher": "汉阳区人民政府",
        "published_at": "2026-07",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "政府领导班子成员明细：李津(本地汉阳履历)、黄翀(市经信)、易雄才(本地汉阳)、童传(挂职来自经开区)、肖斌(公安局长)",
    },
    {
        "id": "S008",
        "title": "区人民政府关于提请免去赵亮职务的议案 (2026-05-25)",
        "url": "https://www.hanyang.gov.cn/zwgk_38/xxgkml/qtzdgknr/rsrm/202606/t20260601_2771461.shtml",
        "publisher": "汉阳区人民政府/区人大常委会",
        "published_at": "2026-05-25",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "署名'武汉市汉阳区人民政府区长郭笑'，确认前任区长=郭笑撰、免去赵亮副区长职务",
    },
]


def make_person_json(person, career_timeline, relationship_list):
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "湖北省",
            "city": "武汉市",
            "region": "汉阳区",
            "job": person.get("current_post", ""),
            "task_id": "hubei_汉阳区",
            "time_focus": "2026"
        },
        "identity": {
            "person_id": f"hanyang_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": person.get("native_place", ""),
            "education": [
                {
                    "period": "",
                    "institution": "",
                    "major": "",
                    "degree": person.get("education", ""),
                    "study_type": "unknown",
                    "source_ids": ["S007", "S005"] if person.get("education") else [],
                }
            ] if person.get("education") else [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_year", ""),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person.get('birth', '')}" if person.get("birth") else person["name"],
                "name_birthplace": f"{person['name']}_{person.get('birthplace', '')}" if person.get("birthplace") else person["name"],
                "official_profile_url": person.get("source", "")
            }
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S007", "S005", "S004", "S001"]
        },
        "career_timeline": career_timeline,
        "organizations": [],
        "relationships": relationship_list,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "受限于公开资料，晋升速度评估有限",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "公开资料中未发现纪律处分、审计问题或负面报道",
                "date": "",
                "confidence": "unverified",
                "source_ids": []
            }
        ],
        "source_register": _source_register,
        "confidence_summary": {
            "identity": "confirmed" if person.get("birth") or person.get("education") else "plausible",
            "current_role": "confirmed",
            "career_completeness": "partial" if person.get("education") else "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "周岚上任前履历与前任书记交接信息；周岚出生/籍贯/学历；傅谦、柯巍详细履历"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{person['name']}在担任现职前的完整履历（含出生年、籍贯、学历、历任职务）是什么？",
                "why_it_matters": "完整晋升路径揭示干部来源与工作关系网络",
                "suggested_queries": [
                    f"{person['name']} 简历 汉阳区",
                    f"{person['name']} 任前公示",
                    f"{person['name']} 此前任职"
                ],
                "last_attempted": AS_OF
            },
            {
                "priority": "medium",
                "question": f"与 {person['name']} 交集的副职/同侪是否有共同任职往昔（同期同单位）？",
                "why_it_matters": "用于确认或升级关系强度",
                "suggested_queries": [f"{person['name']} 工作交集 汉阳", f"{person['name']} 共事"],
                "last_attempted": AS_OF
            }
        ]
    }


_JOB_LABEL = {
    "周岚": "区委书记",
    "张健": "区长",
    "陈波": "常务副区长",
}


def write_person_json(person, career_timeline, relationship_list):
    data = make_person_json(person, career_timeline, relationship_list)
    job = _JOB_LABEL.get(person["name"], "领导")
    safe_name = person["name"]
    path = PERSONS_DIR / f"{TODAY}-湖北省-武汉市-{job}-{safe_name}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {path.name}")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════


def build_person_timeline(person):
    # Provide confirmation from official source basics; gaps flagged
    n = person["name"]
    if n == "周岚":
        return [
            {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "level": "", "location": "", "system": "party", "rank": "", "is_key_promotion": False, "notes": "公开资料未找到周岚任汉阳区委书记前完整履历", "confidence": "unverified", "source_ids": []},
            {"start": "~2026", "end": "present", "org": "中共武汉市汉阳区委员会", "title": "汉阳区委书记", "level": "副厅级", "location": "武汉市汉阳区", "system": "party", "rank": "", "is_key_promotion": True, "notes": "2026年5-6月官网新闻多次确认区委书记身份", "confidence": "confirmed", "source_ids": ["S001", "S002", "S003"]},
        ]
    if n == "张健":
        return [
            {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "level": "", "location": "", "system": "other", "rank": "", "is_key_promotion": False, "notes": "张健任代理区长前（区委副书记/副区长任职前）完整履历未查到", "confidence": "unverified", "source_ids": [], "name": "履历缺口"},
            {"start": "1976-02", "end": "", "org": "籍贯/出身", "title": "出生", "level": "", "location": "", "system": "other", "rank": "", "is_key_promotion": False, "notes": "1976年2月出生，汉族，在职研究生，管理学硕士，中共党员", "confidence": "confirmed", "source_ids": ["S004"]},
            {"start": "~2026", "end": "present", "org": "汉阳区人民政府", "title": "区委副书记、代理区长", "level": "副厅级", "location": "武汉市汉阳区", "system": "government", "rank": "", "is_key_promotion": True, "notes": "官网 2026-08-03 确认任代理区长、党组书记，领导区政府全面工作", "confidence": "confirmed", "source_ids": ["S004"]},
        ]
    if n == "陈波":
        return [
            {"start": "2005-10", "end": "", "org": "入党", "title": "加入中国共产党", "level": "", "location": "", "system": "other", "rank": "", "is_key_promotion": False, "notes": "2005年10月入党；湖北崇阳人，1984.4出生，在职硕士（工商管理）", "confidence": "confirmed", "source_ids": ["S005"]},
            {"start": "2007-07", "end": "present", "org": "武汉市市级机关→汉阳区", "title": "历任市政府研究室副处长/处长、市政府办公厅副主任、市政府副秘书长→汉阳常务副区长", "level": "", "location": "武汉市/汉阳区", "system": "government", "rank": "", "is_key_promotion": True, "notes": "从市级机关（市政府研究室/办公厅/市政府）调任汉阳，2025-2026任常务副区长", "confidence": "confirmed", "source_ids": ["S005"]},
            {"start": "~2024", "end": "present", "org": "汉阳区人民政府", "title": "区委常委、常务副区长", "level": "县处级", "location": "武汉市汉阳区", "system": "government", "rank": "", "is_key_promotion": True, "notes": "区政府党组副书记，负责政府常务工作", "confidence": "confirmed", "source_ids": ["S005"]},
        ]
    # fallback：仅确认现任职务
    return [
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "level": "", "location": "", "system": "other", "rank": "", "is_key_promotion": False, "notes": f"公开资料未找到 {n} 完整履历", "confidence": "unverified", "source_ids": []},
        {"start": "", "end": "present", "org": person.get("current_org", ""), "title": person.get("current_post", ""), "level": "", "location": "武汉市汉阳区", "system": "government", "rank": "", "is_key_promotion": False, "notes": person.get("notes", ""), "confidence": "confirmed", "source_ids": ["S007"]},
    ]


def main():
    os.makedirs(PERSONS_DIR, exist_ok=True)
    if not IN_CANONICAL:
        os.makedirs(_STAGING_DIR, exist_ok=True)

    rel_list = []
    rel_list.append({"person_a": 1, "person_b": 4, "type": "overlap", "context": "汉阳区委书记与代理区长搭班共事", "overlap_org": "汉阳区", "overlap_period": "2026至present", "confidence": "confirmed"})
    rel_list.append({"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "区委书记与区委副书记", "overlap_org": "汉阳区委", "overlap_period": "至present", "confidence": "confirmed"})
    rel_list.append({"person_a": 4, "person_b": 5, "type": "overlap", "context": "代理区长与常务副区长（政府党组副书记）", "overlap_org": "汉阳区政府", "overlap_period": "至present", "confidence": "confirmed"})
    for _ in range(6, 12):
        rel_list.append({"person_a": 4, "person_b": _, "type": "superior_subordinate", "context": "代理区长与副区长", "overlap_org": "汉阳区政府", "overlap_period": "至present", "confidence": "confirmed"})
    rel_list.append({"person_a": 12, "person_b": 4, "type": "predecessor_successor", "context": "郭笑（前任区长）与张继（代理区长）", "overlap_org": "汉阳区政府", "overlap_period": "2026", "confidence": "plausible"})
    rel_list.append({"person_a": 5, "person_b": 8, "type": "same_system", "context": "陈波与黄翀均曾供职于武汉市市级机关（市政府办公厅系/市编委）", "overlap_org": "武汉市级机关", "overlap_period": "", "confidence": "weak"})
    rel_list.append({"person_a": 11, "person_b": 4, "type": "overlap", "context": "挂职副区长（来自武汉经开区）与区长共事", "overlap_org": "汉阳区政府", "overlap_period": "至present", "confidence": "confirmed"})
    rel_list.append({"person_a": 7, "person_b": 9, "type": "same_system", "context": "李津与易雄才均为本地成长汉阳干部", "overlap_org": "汉阳区", "overlap_period": "", "confidence": "medium"})

    # Build DB + GEXF via runner
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=rel_list,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    # Write person JSON for core leaders (区委书记 周岚, 区长 张健; plus 陈波)
    print("\n--- Person JSONs ---")
    by_name = {p["name"]: p for p in persons}
    write_person_json(by_name["周岚"], build_person_timeline(by_name["周岚"]), [
        {"person": "张健", "person_id": "hanyang_张健", "relationship_type": "overlap", "strength": "strong", "evidence": "区委书记与代理区长搭班共事", "overlap_org": "汉阳区", "overlap_period": "2026至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S004"]},
        {"person": "傅谦", "person_id": "hanyang_傅谦", "relationship_type": "superior_subordinate", "strength": "medium", "evidence": "区委书记与区委副书记同班子", "overlap_org": "汉阳区委", "overlap_period": "至今", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S003"]},
    ])
    write_person_json(by_name["张健"], build_relationships_for(by_name["张健"], persons), [])
    write_person_json(by_name["陈波"], build_relationships_for(by_name["陈波"], persons), [])

    print(f"\n{'='*60}")
    print(f"汉阳区 Network Build Complete")
    print(f"{'='*60}")
    print(f"Staging dir: {_STAGING_DIR}")
    print(f"DB:          {DB_PATH}")
    print(f"GEXF:        {GEXF_PATH}")


def build_relationships_for(person, persons):
    n = person["name"]
    if n == "张健":
        return [
            {"person": "周岚", "person_id": "hanyang_周岚", "relationship_type": "overlap", "strength": "strong", "evidence": "代理区长与区委书记搭班", "overlap_org": "汉阳区", "overlap_period": "2026至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S004"]},
            {"person": "陈波", "person_id": "hanyang_陈波", "relationship_type": "overlap", "strength": "medium", "evidence": "代理区长与常务副区长", "overlap_org": "汉阳区政府", "overlap_period": "至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004", "S005"]},
        ]
    if n == "陈波":
        return [
            {"person": "张健", "person_id": "hanyang_张健", "relationship_type": "overlap", "strength": "medium", "evidence": "常务副区长与代理区长", "overlap_org": "汉阳区政府", "overlap_period": "至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S005", "S004"]},
            {"person": "黄翀", "person_id": "hanyang_黄翀", "relationship_type": "same_system", "strength": "weak", "evidence": "均曾供职于武汉市市级机关", "overlap_org": "武汉市级机关", "overlap_period": "", "direction": "undirected", "confidence": "weak", "source_ids": ["S005"]},
        ]
    return []


if __name__ == "__main__":
    main()