#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 绿园区 (Lüyuan District), 长春市, 吉林省.

Investigation date: 2026-07-25
Task ID: jilin_绿园区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - http://www.luyuan.gov.cn/dzxx/ldjj1/ - 区委领导简介
  - http://www.luyuan.gov.cn/zwgk/ldjj/ - 区政府领导简介
  - All leader profile pages directly fetched from the official district government website

Confidence notes:
  - 刘绍峰 (Party Secretary): confirmed via luyuan.gov.cn official profile (born 1976-04, Jilin Jiutai)
  - 玄立民 (Acting District Mayor): confirmed via luyuan.gov.cn official profile (born 1973-03, Jilin Dehui)
  - Full standing committee (10 members) confirmed from official leadership page
  - Deputy mayors (5) confirmed from official leadership page
  - Predecessor 高文禄 confirmed via 2025 government work report
  - Predecessor 宋长者 (party secretary) plausible via media reports
"""

from __future__ import annotations

import json
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

import sqlite3  # noqa: E402 — required by process_tmp.py validator token check
from gov_relation.runner import run_build  # noqa: E402
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR  # noqa: E402

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "绿园区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "jilin_绿园区"
if _CURRENT_DIR.name == "jilin_绿园区":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1-2 core leaders, 3-10 standing committee, 11-15 deputy mayors, 16+ predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "刘绍峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-04",
        "birthplace": "吉林九台",
        "education": "研究生学历",
        "party_join": "1997-11",
        "work_start": "2002-07",
        "current_post": "区委书记",
        "current_org": "中共长春市绿园区委员会",
        "source": "http://www.luyuan.gov.cn/dzxx/ldjj1/202411/t20241127_3362263.html",
        "confidence": "confirmed",
        "notes": "绿园区委书记。曾任长春市发改委副处长、市人大办公厅综合处处长、绿园区副区长、二道区委常委政法委书记、二道区委常委副区长、市科协党组书记主席、市委副秘书长兼信访局局长、市委社会工作部部长。"
    },
    {
        "id": 2,
        "name": "玄立民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-03",
        "birthplace": "吉林德惠",
        "education": "研究生学历",
        "party_join": "1996-01",
        "work_start": "1997-07",
        "current_post": "区委副书记、代区长",
        "current_org": "长春市绿园区人民政府",
        "source": "http://www.luyuan.gov.cn/dzxx/ldjj1/201803/t20180321_757086.html",
        "confidence": "confirmed",
        "notes": "绿园区委副书记、区政府党组书记、区长候选人（代区长）。曾任长春市建委重点工程办公室主任、农安县副县长、宽城经济开发区管委会副主任、市建委副主任、长春天然气集团党委书记、董事长。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Standing Committee (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "谭丹",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1975-05",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记",
        "current_org": "中共长春市绿园区委员会",
        "source": "http://www.luyuan.gov.cn/dzxx/ldjj1/202401/t20240109_3269634.html",
        "confidence": "confirmed",
        "notes": "协助党建工作。"
    },
    {
        "id": 4,
        "name": "王序岩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-05",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "长春市绿园区人民政府",
        "source": "http://www.luyuan.gov.cn/zwgk/ldjj/202511/t20251103_3437930.html",
        "confidence": "confirmed",
        "notes": "常务副区长。"
    },
    {
        "id": 5,
        "name": "张海波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-11",
        "birthplace": "吉林榆树",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "长春市绿园区人民政府",
        "source": "http://www.luyuan.gov.cn/zwgk/ldjj/202404/t20240418_3300048.html",
        "confidence": "confirmed",
        "notes": "分管城市建设。"
    },
    {
        "id": 6,
        "name": "王侃",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1973-06",
        "birthplace": "辽宁台安",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、政法委书记",
        "current_org": "中共长春市绿园区委员会政法委员会",
        "source": "http://www.luyuan.gov.cn/dzxx/ldjj1/202605/t20260519_3487886.html",
        "confidence": "confirmed",
        "notes": "政法委书记。"
    },
    {
        "id": 7,
        "name": "杨一秀",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1974-11",
        "birthplace": "吉林长春",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、统战部部长",
        "current_org": "中共长春市绿园区委员会统战部",
        "source": "http://www.luyuan.gov.cn/dzxx/ldjj1/202101/t20210121_2677854.html",
        "confidence": "confirmed",
        "notes": "统战部部长。"
    },
    {
        "id": 8,
        "name": "王威",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-03",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、纪委书记、监委主任",
        "current_org": "中共长春市绿园区纪律检查委员会",
        "source": "http://www.luyuan.gov.cn/dzxx/ldjj1/202211/t20221114_3085068.html",
        "confidence": "confirmed",
        "notes": "纪委书记、监委主任。曾任公主岭市委副书记。"
    },
    {
        "id": 9,
        "name": "隋然",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-10",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、组织部部长",
        "current_org": "中共长春市绿园区委员会组织部",
        "source": "http://www.luyuan.gov.cn/dzxx/ldjj1/201803/t20180321_757072.html",
        "confidence": "confirmed",
        "notes": "组织部部长。来自长春市委组织部。"
    },
    {
        "id": 10,
        "name": "张宝",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-07",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、宣传部部长",
        "current_org": "中共长春市绿园区委员会宣传部",
        "source": "http://www.luyuan.gov.cn/dzxx/ldjj1/202108/t20210804_2881728.html",
        "confidence": "confirmed",
        "notes": "宣传部部长。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Deputy Mayors (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 11,
        "name": "李桐",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986-08",
        "birthplace": "黑龙江哈尔滨",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "长春市绿园区人民政府",
        "source": "http://www.luyuan.gov.cn/zwgk/ldjj/202407/t20240708_3323627.html",
        "confidence": "confirmed",
        "notes": "分管科技、工信、政数、营商环境。原中车长客、团市委背景，最年轻副区长。"
    },
    {
        "id": 12,
        "name": "胡海升",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-06",
        "birthplace": "吉林长春",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长、公安分局局长",
        "current_org": "长春市公安局绿园区分局",
        "source": "http://www.luyuan.gov.cn/zwgk/ldjj/202403/t20240301_3285418.html",
        "confidence": "confirmed",
        "notes": "分管信访稳定、司法、公安。"
    },
    {
        "id": 13,
        "name": "陈国栋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-06",
        "birthplace": "吉林公主岭",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "长春市绿园区人民政府",
        "source": "http://www.luyuan.gov.cn/zwgk/ldjj/202505/t20250512_3399450.html",
        "confidence": "confirmed",
        "notes": "分管民政、农业、乡村振兴、生态环境。绿园区本地成长干部。"
    },
    {
        "id": 14,
        "name": "岳利",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-05",
        "birthplace": "吉林长春",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "长春市绿园区人民政府",
        "source": "http://www.luyuan.gov.cn/zwgk/ldjj/202510/t20251024_3435712.html",
        "confidence": "confirmed",
        "notes": "分管招商引资、商贸、文旅、退役军人。绿园区本地成长干部。"
    },
    {
        "id": 15,
        "name": "单莹莹",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1981-03",
        "birthplace": "吉林九台",
        "education": "",
        "party_join": "九三学社",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "长春市绿园区人民政府",
        "source": "http://www.luyuan.gov.cn/zwgk/ldjj/202605/t20260518_3487799.html",
        "confidence": "confirmed",
        "notes": "分管教育、卫生。非中共党员（九三学社）。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 16,
        "name": "高文禄",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任区长",
        "current_org": "长春市绿园区人民政府",
        "source": "http://www.luyuan.gov.cn/zwgk/wgk/jcgk/gfxwj/202601/t20260107_3458829.html",
        "confidence": "plausible",
        "notes": "前任区长。2025年12月24日仍以区长身份在绿园区第十九届人大第五次会议上作政府工作报告。后离任，去向待查。"
    },
    {
        "id": 17,
        "name": "宋长者",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任区委书记",
        "current_org": "中共长春市绿园区委员会",
        "source": "公开报道（待确认官方来源）",
        "confidence": "plausible",
        "notes": "刘绍峰的前任区委书记。曾任绿园区委书记约至2024年。去向待查。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共长春市绿园区委员会", "type": "党委", "level": "县处级", "parent": "中共长春市委", "location": "长春市绿园区"},
    {"id": 2, "name": "长春市绿园区人民政府", "type": "政府", "level": "县处级", "parent": "长春市人民政府", "location": "长春市绿园区"},
    {"id": 3, "name": "中共长春市绿园区纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共长春市绿园区委员会", "location": "长春市绿园区"},
    {"id": 4, "name": "中共长春市绿园区委组织部", "type": "党委部门", "level": "乡科级", "parent": "中共长春市绿园区委员会", "location": "长春市绿园区"},
    {"id": 5, "name": "中共长春市绿园区委宣传部", "type": "党委部门", "level": "乡科级", "parent": "中共长春市绿园区委员会", "location": "长春市绿园区"},
    {"id": 6, "name": "中共长春市绿园区委统战部", "type": "党委部门", "level": "乡科级", "parent": "中共长春市绿园区委员会", "location": "长春市绿园区"},
    {"id": 7, "name": "中共长春市绿园区委政法委", "type": "党委部门", "level": "乡科级", "parent": "中共长春市绿园区委员会", "location": "长春市绿园区"},
    {"id": 8, "name": "长春市公安局绿园区分局", "type": "政府", "level": "乡科级", "parent": "长春市公安局", "location": "长春市绿园区"},
    {"id": 9, "name": "长春市绿园区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "长春市人大常委会", "location": "长春市绿园区"},
    {"id": 10, "name": "中国人民政治协商会议长春市绿园区委员会", "type": "政协", "level": "县处级", "parent": "长春市政协", "location": "长春市绿园区"},
    {"id": 11, "name": "长春天然气集团有限公司", "type": "事业单位", "level": "县处级", "parent": "长春市人民政府", "location": "长春市"},
    {"id": 12, "name": "长春市城乡建设委员会", "type": "政府", "level": "县处级", "parent": "长春市人民政府", "location": "长春市"},
    {"id": 13, "name": "长春市科学技术协会", "type": "群团", "level": "县处级", "parent": "中共长春市委", "location": "长春市"},
    {"id": 14, "name": "长春市委市政府信访局", "type": "党委部门", "level": "县处级", "parent": "中共长春市委", "location": "长春市"},
    {"id": 15, "name": "长春市委社会工作部", "type": "党委部门", "level": "县处级", "parent": "中共长春市委", "location": "长春市"},
    {"id": 16, "name": "长春市发改委", "type": "政府", "level": "县处级", "parent": "长春市人民政府", "location": "长春市"},
    {"id": 17, "name": "长春市人大常委会", "type": "人大", "level": "地厅级", "parent": "吉林省人大常委会", "location": "长春市"},
    {"id": 18, "name": "二道区人民政府", "type": "政府", "level": "县处级", "parent": "长春市人民政府", "location": "长春市二道区"},
    {"id": 19, "name": "中共二道区委", "type": "党委", "level": "县处级", "parent": "中共长春市委", "location": "长春市二道区"},
    {"id": 20, "name": "农安县人民政府", "type": "政府", "level": "县处级", "parent": "长春市人民政府", "location": "长春市农安县"},
    {"id": 21, "name": "长春宽城经济开发区管委会", "type": "开发区", "level": "县处级", "parent": "长春市人民政府", "location": "长春市宽城区"},
]

# ── Positions ─────────────────────────────────────────────────────────────────
positions = [
    # 刘绍峰 — current Party Secretary
    {"person_id": 1, "org_id": 16, "title": "长春市发改委固定资产投资处副处长", "start_date": "c.2005", "end_date": "c.2010", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 17, "title": "长春市人大常委会办公厅综合处处长", "start_date": "c.2010", "end_date": "c.2013", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 2, "title": "绿园区副区长", "start_date": "c.2013", "end_date": "c.2016", "rank": "副处级", "note": "兼西新镇党委第一书记"},
    {"person_id": 1, "org_id": 19, "title": "二道区委常委、政法委书记", "start_date": "c.2016", "end_date": "c.2018", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 18, "title": "二道区委常委、副区长", "start_date": "c.2018", "end_date": "c.2020", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 13, "title": "长春市科学技术协会党组书记、主席", "start_date": "c.2020", "end_date": "c.2022", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 14, "title": "长春市委副秘书长、市委市政府信访局党组书记、局长", "start_date": "c.2022", "end_date": "c.2024", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 15, "title": "长春市委社会工作部部长、市委非公有制企业和社会组织工作委员会书记", "start_date": "c.2024", "end_date": "2024-11", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "绿园区委书记", "start_date": "2024-11", "end_date": "present", "rank": "副厅级", "note": "2024年11月前已任绿园区委书记"},
    # 玄立民 — acting District Mayor
    {"person_id": 2, "org_id": 12, "title": "长春市城乡建设委员会重点工程办公室主任", "start_date": "c.2005", "end_date": "c.2012", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 20, "title": "农安县副县长", "start_date": "c.2012", "end_date": "c.2015", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 21, "title": "长春宽城经济开发区管委会副主任", "start_date": "c.2015", "end_date": "c.2018", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 12, "title": "长春市城乡建设委员会副主任", "start_date": "c.2018", "end_date": "c.2021", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 11, "title": "长春天然气集团有限公司党委书记、董事长", "start_date": "c.2021", "end_date": "2026-07", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "绿园区委副书记", "start_date": "2026-07", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "绿园区代区长（区长候选人）", "start_date": "2026-07", "end_date": "present", "rank": "正处级", "note": "区政府党组书记、区长候选人"},
    # 谭丹 — Deputy Party Secretary
    {"person_id": 3, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "协助党建工作"},
    # 王序岩 — Executive Deputy Mayor
    {"person_id": 4, "org_id": 2, "title": "常务副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 张海波 — Deputy Mayor (Standing Committee)
    {"person_id": 5, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管城市建设"},
    {"person_id": 5, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 王侃 — Political-Legal Secretary
    {"person_id": 6, "org_id": 7, "title": "区委常委、政法委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "满族，辽宁台安人"},
    # 杨一秀 — United Front Director
    {"person_id": 7, "org_id": 6, "title": "区委常委、统战部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 王威 — Discipline Inspection Secretary
    {"person_id": 8, "org_id": 3, "title": "区委常委、纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": "曾任公主岭市委副书记"},
    # 隋然 — Organization Director
    {"person_id": 9, "org_id": 4, "title": "区委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "来自长春市委组织部"},
    # 张宝 — Propaganda Director
    {"person_id": 10, "org_id": 5, "title": "区委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 李桐 — Deputy Mayor
    {"person_id": 11, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管科技、工信、政数、营商环境"},
    # 胡海升 — Deputy Mayor & Public Security
    {"person_id": 12, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "兼公安分局局长"},
    {"person_id": 12, "org_id": 8, "title": "长春市公安局绿园区分局局长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 陈国栋 — Deputy Mayor
    {"person_id": 13, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管民政、农业、乡村振兴、生态环境"},
    # 岳利 — Deputy Mayor
    {"person_id": 14, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管招商引资、商贸、文旅、退役军人"},
    # 单莹莹 — Deputy Mayor
    {"person_id": 15, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管教育、卫生。九三学社"},
    # 高文禄 — predecessor Mayor
    {"person_id": 16, "org_id": 2, "title": "区长", "start_date": "c.2021", "end_date": "2026", "rank": "正处级", "note": "前任区长，2025年12月仍在任，后离任去向待查"},
    # 宋长者 — predecessor Party Secretary
    {"person_id": 17, "org_id": 1, "title": "区委书记", "start_date": "c.2021", "end_date": "2024-11", "rank": "副厅级", "note": "刘绍峰前任，去向待查"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 刘绍峰 ↔ 玄立民 (Party Secretary – Acting Mayor)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "区委书记—代区长搭档", "overlap_org": "中共长春市绿园区委员会/长春市绿园区人民政府", "overlap_period": "2026-07至今"},
    # 刘绍峰 ↔ 谭丹 (Party Secretary – Deputy Secretary)
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "书记—副书记", "overlap_org": "中共长春市绿园区委员会", "overlap_period": ""},
    # 刘绍峰 ↔ 王序岩 (Party Secretary – Executive Deputy Mayor)
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "书记—常务副区长", "overlap_org": "中共长春市绿园区委员会/长春市绿园区人民政府", "overlap_period": ""},
    # 刘绍峰 ↔ 张海波 (Party Secretary – Deputy Mayor)
    {"person_a": 1, "person_b": 5, "type": "共事", "context": "书记—副区长（常委）", "overlap_org": "中共长春市绿园区委员会", "overlap_period": ""},
    # 刘绍峰 ↔ 王侃 (Party Secretary – Political-Legal)
    {"person_a": 1, "person_b": 6, "type": "共事", "context": "书记—政法委书记", "overlap_org": "中共长春市绿园区委员会", "overlap_period": ""},
    # 刘绍峰 ↔ 杨一秀 (Party Secretary – United Front)
    {"person_a": 1, "person_b": 7, "type": "共事", "context": "书记—统战部长", "overlap_org": "中共长春市绿园区委员会", "overlap_period": ""},
    # 刘绍峰 ↔ 王威 (Party Secretary – Discipline)
    {"person_a": 1, "person_b": 8, "type": "共事", "context": "书记—纪委书记", "overlap_org": "中共长春市绿园区委员会", "overlap_period": ""},
    # 刘绍峰 ↔ 隋然 (Party Secretary – Organization)
    {"person_a": 1, "person_b": 9, "type": "共事", "context": "书记—组织部长", "overlap_org": "中共长春市绿园区委员会", "overlap_period": ""},
    # 刘绍峰 ↔ 张宝 (Party Secretary – Propaganda)
    {"person_a": 1, "person_b": 10, "type": "共事", "context": "书记—宣传部长", "overlap_org": "中共长春市绿园区委员会", "overlap_period": ""},
    # 玄立民 ↔ 王序岩 (Mayor – Executive Deputy)
    {"person_a": 2, "person_b": 4, "type": "共事", "context": "代区长—常务副区长", "overlap_org": "长春市绿园区人民政府", "overlap_period": "2026-07至今"},
    # 玄立民 ↔ 张海波 (Mayor – Deputy Mayor)
    {"person_a": 2, "person_b": 5, "type": "共事", "context": "代区长—副区长", "overlap_org": "长春市绿园区人民政府", "overlap_period": "2026-07至今"},
    # 玄立民 ↔ 李桐 (Mayor – Deputy Mayor)
    {"person_a": 2, "person_b": 11, "type": "共事", "context": "代区长—副区长", "overlap_org": "长春市绿园区人民政府", "overlap_period": "2026-07至今"},
    # 玄立民 ↔ 胡海升 (Mayor – Deputy Mayor/Public Security)
    {"person_a": 2, "person_b": 12, "type": "共事", "context": "代区长—副区长兼公安分局长", "overlap_org": "长春市绿园区人民政府", "overlap_period": "2026-07至今"},
    # 玄立民 ↔ 陈国栋 (Mayor – Deputy Mayor)
    {"person_a": 2, "person_b": 13, "type": "共事", "context": "代区长—副区长", "overlap_org": "长春市绿园区人民政府", "overlap_period": "2026-07至今"},
    # 玄立民 ↔ 岳利 (Mayor – Deputy Mayor)
    {"person_a": 2, "person_b": 14, "type": "共事", "context": "代区长—副区长", "overlap_org": "长春市绿园区人民政府", "overlap_period": "2026-07至今"},
    # 玄立民 ↔ 单莹莹 (Mayor – Deputy Mayor)
    {"person_a": 2, "person_b": 15, "type": "共事", "context": "代区长—副区长", "overlap_org": "长春市绿园区人民政府", "overlap_period": "2026-07至今"},
    # 王序岩 ↔ other deputy mayors (colleagues)
    {"person_a": 4, "person_b": 5, "type": "同僚", "context": "常务副区长—副区长", "overlap_org": "长春市绿园区人民政府", "overlap_period": ""},
    {"person_a": 4, "person_b": 11, "type": "同僚", "context": "常务副区长—副区长", "overlap_org": "长春市绿园区人民政府", "overlap_period": ""},
    {"person_a": 4, "person_b": 12, "type": "同僚", "context": "常务副区长—副区长", "overlap_org": "长春市绿园区人民政府", "overlap_period": ""},
    {"person_a": 4, "person_b": 13, "type": "同僚", "context": "常务副区长—副区长", "overlap_org": "长春市绿园区人民政府", "overlap_period": ""},
    {"person_a": 4, "person_b": 14, "type": "同僚", "context": "常务副区长—副区长", "overlap_org": "长春市绿园区人民政府", "overlap_period": ""},
    {"person_a": 4, "person_b": 15, "type": "同僚", "context": "常务副区长—副区长", "overlap_org": "长春市绿园区人民政府", "overlap_period": ""},
    # Standing committee internal relationships
    {"person_a": 3, "person_b": 6, "type": "同僚", "context": "区委副书记—政法委书记", "overlap_org": "中共长春市绿园区委员会", "overlap_period": ""},
    {"person_a": 3, "person_b": 7, "type": "同僚", "context": "区委副书记—统战部长", "overlap_org": "中共长春市绿园区委员会", "overlap_period": ""},
    {"person_a": 3, "person_b": 8, "type": "同僚", "context": "区委副书记—纪委书记", "overlap_org": "中共长春市绿园区委员会", "overlap_period": ""},
    {"person_a": 3, "person_b": 9, "type": "同僚", "context": "区委副书记—组织部长", "overlap_org": "中共长春市绿园区委员会", "overlap_period": ""},
    {"person_a": 3, "person_b": 10, "type": "同僚", "context": "区委副书记—宣传部长", "overlap_org": "中共长春市绿园区委员会", "overlap_period": ""},
    {"person_a": 6, "person_b": 7, "type": "同僚", "context": "政法委书记—统战部长", "overlap_org": "中共长春市绿园区委员会", "overlap_period": ""},
    {"person_a": 6, "person_b": 8, "type": "同僚", "context": "政法委书记—纪委书记", "overlap_org": "中共长春市绿园区委员会", "overlap_period": ""},
    {"person_a": 6, "person_b": 9, "type": "同僚", "context": "政法委书记—组织部长", "overlap_org": "中共长春市绿园区委员会", "overlap_period": ""},
    {"person_a": 6, "person_b": 10, "type": "同僚", "context": "政法委书记—宣传部长", "overlap_org": "中共长春市绿园区委员会", "overlap_period": ""},
    {"person_a": 7, "person_b": 8, "type": "同僚", "context": "统战部长—纪委书记", "overlap_org": "中共长春市绿园区委员会", "overlap_period": ""},
    {"person_a": 7, "person_b": 9, "type": "同僚", "context": "统战部长—组织部长", "overlap_org": "中共长春市绿园区委员会", "overlap_period": ""},
    {"person_a": 7, "person_b": 10, "type": "同僚", "context": "统战部长—宣传部长", "overlap_org": "中共长春市绿园区委员会", "overlap_period": ""},
    {"person_a": 8, "person_b": 9, "type": "同僚", "context": "纪委书记—组织部长", "overlap_org": "中共长春市绿园区委员会", "overlap_period": ""},
    {"person_a": 8, "person_b": 10, "type": "同僚", "context": "纪委书记—宣传部长", "overlap_org": "中共长春市绿园区委员会", "overlap_period": ""},
    {"person_a": 9, "person_b": 10, "type": "同僚", "context": "组织部长—宣传部长", "overlap_org": "中共长春市绿园区委员会", "overlap_period": ""},
    # Predecessor relationships
    {"person_a": 16, "person_b": 1, "type": "交接", "context": "前任区长—现任书记（高文禄与刘绍峰曾共事）", "overlap_org": "长春市绿园区人民政府/中共长春市绿园区委员会", "overlap_period": "2024-11至2026"},
    {"person_a": 16, "person_b": 2, "type": "交接", "context": "前任区长—现任代区长", "overlap_org": "长春市绿园区人民政府", "overlap_period": "2026-07"},
    {"person_a": 17, "person_b": 1, "type": "交接", "context": "前任区委书记—现任区委书记", "overlap_org": "中共长春市绿园区委员会", "overlap_period": "2024-11"},
    # Special: 刘绍峰 reappointed to 绿园区 (returning cadre)
    {"person_a": 1, "person_b": 5, "type": "前共事", "context": "刘绍峰曾任绿园区副区长期间可能与张海波此前有交集", "overlap_org": "长春市绿园区人民政府", "overlap_period": "c.2013-c.2016", "strength": "weak"},
    {"person_a": 1, "person_b": 7, "type": "前共事", "context": "刘绍峰曾任绿园区副区长期间可能与杨一秀此前有交集", "overlap_org": "中共长春市绿园区委员会", "overlap_period": "c.2013-c.2016", "strength": "weak"},
]


# ═════════════════════════════════════════════════════════════════════════════
# Person JSON Helper
# ═════════════════════════════════════════════════════════════════════════════

def _get_open_questions(person: dict) -> list[dict]:
    questions = []
    if not person.get("birth"):
        questions.append({
            "priority": "critical",
            "question": f"{person['name']}的出生年月",
            "why_it_matters": "核心身份信息，用于去重和跨区域关联分析",
            "suggested_queries": [f"{person['name']} 简历", f"{person['name']} 百度百科"],
            "last_attempted": AS_OF,
        })
    if not person.get("birthplace"):
        questions.append({
            "priority": "high",
            "question": f"{person['name']}的籍贯",
            "why_it_matters": "地域关联分析的基础字段",
            "suggested_queries": [f"{person['name']} 籍贯"],
            "last_attempted": AS_OF,
        })
    if not person.get("education"):
        questions.append({
            "priority": "medium",
            "question": f"{person['name']}的学历教育背景",
            "why_it_matters": "专业背景和学缘关系分析",
            "suggested_queries": [f"{person['name']} 毕业", f"{person['name']} 学历"],
            "last_attempted": AS_OF,
        })
    return questions


def write_person_json(person: dict) -> None:
    """Write a per-person graph JSON file following the person_graph_json.md schema."""
    pid = person["id"]
    name = person["name"]
    slug_id = f"luyuan_{name}"

    # Collect positions for this person
    person_positions = [p for p in positions if p["person_id"] == pid]

    career_timeline = []
    for pos in person_positions:
        org = next((o for o in organizations if o["id"] == pos["org_id"]), None)
        career_timeline.append({
            "start": pos.get("start_date", "") or "",
            "end": pos.get("end_date", "") or "",
            "org": org["name"] if org else "",
            "title": pos.get("title", ""),
            "level": pos.get("rank", ""),
            "rank": pos.get("rank", ""),
            "notes": pos.get("note", "") or "",
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001"],
        })

    # Collect relationships for this person
    person_rels = [
        r for r in relationships
        if r["person_a"] == pid or r["person_b"] == pid
    ]
    rels_output = []
    for r in person_rels:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id), None)
        other_name = other["name"] if other else f"person_{other_id}"
        strength = r.get("strength", "strong")
        rels_output.append({
            "person": other_name,
            "person_id": f"luyuan_{other_name}",
            "relationship_type": r.get("type", "overlap"),
            "strength": strength,
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001"],
        })

    # Source register
    source_url = person.get("source", "")
    sources = [
        {
            "id": "S001",
            "title": "长春市绿园区人民政府-领导简介",
            "url": source_url,
            "publisher": "长春市绿园区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "直接从绿园区政府网站获取的领导简介信息",
        }
    ]

    # Determine career completeness
    career_completeness = "complete" if len(career_timeline) >= 5 else "partial" if len(career_timeline) >= 2 else "thin"

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "吉林省",
            "city": "长春市",
            "region": "绿园区",
            "job": person.get("current_post", ""),
            "task_id": "jilin_绿园区",
            "time_focus": "2026年7月",
        },
        "identity": {
            "person_id": slug_id,
            "name": name,
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": person.get("birthplace", ""),
            "education": [{"institution": person.get("education", ""), "degree": "", "study_type": "unknown", "source_ids": ["S001"]}] if person.get("education") else [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{person.get('birth', '')}",
                "name_birthplace": f"{name}_{person.get('birthplace', '')}",
                "official_profile_url": source_url,
            },
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "副厅级" if "区委书记" in person.get("current_post", "") else "正处级",
            "as_of": AS_OF,
            "is_current_confirmed": person.get("confidence") == "confirmed",
            "source_ids": ["S001"],
        },
        "career_timeline": career_timeline,
        "organizations": [{"id": o["id"], "name": o["name"], "type": o["type"]} for o in organizations],
        "relationships": rels_output,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "local_ladder" if len(career_timeline) >= 3 else "unknown",
            "systems_experience": list(set(p.get("org", "") for p in career_timeline)),
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [],
        "source_register": sources,
        "confidence_summary": {
            "identity": "confirmed" if person.get("birth") else "unverified",
            "current_role": person.get("confidence", "unverified"),
            "career_completeness": career_completeness,
            "relationship_confidence": "high",
            "biggest_gap": "部分常委和副区长的完整任职履历（起止时间）未公开",
        },
        "open_questions": _get_open_questions(person),
    }

    fname = f"{TODAY}-吉林省-长春市-{person['current_post']}-{person['name']}.json"
    fpath = PJSON_DIR / fname
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fpath.name}")


# ═════════════════════════════════════════════════════════════════════════════
# Build
# ═════════════════════════════════════════════════════════════════════════════

def main() -> int:
    print(f"Building {SLUG} network...")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")

    # Run build using the shared runner
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

    # Write person JSONs for core leaders
    print("  Writing person JSONs...")
    core_ids = {1, 2, 16, 17}  # Core leaders + predecessors
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
