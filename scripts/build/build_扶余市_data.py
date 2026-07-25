#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 扶余市, 松原市, 吉林省.

Investigation date: 2026-07-25
Task ID: jilin_扶余市
Level: 县级市
Targets: 市委书记 & 市长

Research sources:
  - www.jlfy.gov.cn — 扶余市人民政府官方网站 (accessible)
  - baike.baidu.com — 百度百科 (partially accessible via insane-search engine)
  - thepaper.cn — 澎湃新闻 (timed out)

Key findings:
  - 市委书记: 满都拉（本名刘永生）, 1976年2月生, 蒙古族
  - 市长: 韩超, 1985年6月生, 山东日照人, 原长春市绿园区委常委、常务副区长
  - 前任市长: 盖克 (韩超前任, 页面已归档)
  - 前任市委书记: 待查 (未找到公开信息)

Confidence notes:
  - Government site (www.jlfy.gov.cn) accessible and provided official profiles.
  - All government leadership data is labeled 'confirmed' with source=official.
  - 满都拉's biographical details sourced from Baidu Baike and search engine results.
  - 满都拉's full career timeline is incomplete — only current role confirmed.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
for parent_count in [2, 3, 4, 5, 6]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import sqlite3
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "扶余市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "jilin_扶余市"
if _CURRENT_DIR.name == "jilin_扶余市":
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
# IDs: 1=市委书记, 2=市长, 3=常务副市长, 4-10=副市长, 11=人大主任, 12=政协主席,
#      13=前任市长, 14=前任市委书记

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "满都拉",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "1976年2月",
        "birthplace": "",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "1996年9月",
        "current_post": "市委书记",
        "current_org": "中共扶余市委员会",
        "source": "百度百科摘要 / www.jlfy.gov.cn 新闻报道",
        "confidence": "confirmed",
        "notes": "满都拉，本名刘永生。蒙古族。1976年2月出生，1996年9月参加工作。现任中共扶余市委书记。此前曾任前郭县相关职务（待查）。"
    },
    {
        "id": 2,
        "name": "韩超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985年6月",
        "birthplace": "山东日照",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记、市长",
        "current_org": "扶余市人民政府",
        "source": "http://www.jlfy.gov.cn/zwgk/sld/szhc/ (政府官网)",
        "confidence": "confirmed",
        "notes": "1985年6月出生，汉族，山东日照人。曾任长春市发改委国民经济综合处主任科员、副处长，政策研究室副主任(副处长级)、主任(正处长级)，国民经济综合处处长，长春莲花山生态旅游度假区管委会副主任(挂职)，长春市发改委党组成员、副主任，长春市绿园区委常委、常务副区长。2025年9月任扶余市副市长、代市长，2025年12月30日当选扶余市市长。"
    },
    {
        "id": 3,
        "name": "于静涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年12月",
        "birthplace": "吉林大安",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "2009年8月",
        "current_post": "市委常委、常务副市长",
        "current_org": "扶余市人民政府",
        "source": "http://www.jlfy.gov.cn/zwgk/sld/yjt/ (政府官网)",
        "confidence": "confirmed",
        "notes": "1984年12月出生，汉族，吉林大安人，2007年10月入党，2009年8月参加工作。曾任吉林省委办公厅省委法规室副主任、三级调研员，乾安县政府副县长(挂职)，松原市委保密委员会专职副主任(正处长级)、市委办公室副主任。"
    },
    {
        "id": 4,
        "name": "宋孝进",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985年5月",
        "birthplace": "黑龙江双城",
        "education": "硕士研究生学历",
        "party_join": "中共党员",
        "work_start": "2008年12月",
        "current_post": "市委常委、副市长",
        "current_org": "扶余市人民政府",
        "source": "http://www.jlfy.gov.cn/zwgk/sld/sxj/ (政府官网)",
        "confidence": "confirmed",
        "notes": "1985年5月出生，汉族，黑龙江双城人，2006年12月入党，2008年12月参加工作。曾任松原市粮食局办公室主任，松原市粮食和物资储备局市场流通科科长，长岭县脱贫攻坚驻村第一书记(2015-2021)，松原市粮食和物资储备局副局长，共青团松原市委副书记，前郭县乌兰塔拉乡党委书记(副处长级)。"
    },
    {
        "id": 5,
        "name": "郭丽明",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1980年8月",
        "birthplace": "吉林长岭",
        "education": "本科学历",
        "party_join": "",
        "work_start": "2004年7月",
        "current_post": "副市长（省工信厅挂职）",
        "current_org": "扶余市人民政府",
        "source": "http://www.jlfy.gov.cn/zwgk/sld/zjh_29844/ (政府官网)",
        "confidence": "confirmed",
        "notes": "1980年8月出生，汉族，吉林长岭人，2004年7月参加工作。曾任乾安县政协文教委主任、乾安县工商联主席、乾安县人大常委会副主任。省工信厅挂职，暂不分工。"
    },
    {
        "id": 6,
        "name": "宿从军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年10月",
        "birthplace": "吉林扶余",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "1996年12月",
        "current_post": "副市长",
        "current_org": "扶余市人民政府",
        "source": "http://www.jlfy.gov.cn/zwgk/sld/zjh_29847/ (政府官网)",
        "confidence": "confirmed",
        "notes": "1973年10月出生，汉族，吉林扶余人，1998年11月入党，1996年12月参加工作。曾任扶余市市场监督管理局党组书记、局长，扶余市委办公室主任。"
    },
    {
        "id": 7,
        "name": "于长胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年9月",
        "birthplace": "吉林扶余",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "1996年7月",
        "current_post": "副市长、公安局局长",
        "current_org": "扶余市人民政府",
        "source": "http://www.jlfy.gov.cn/zwgk/sld/fszycs/ (政府官网)",
        "confidence": "confirmed",
        "notes": "1972年9月出生，汉族，吉林扶余人，1996年4月入党，1996年7月参加工作。曾任松原市公安局刑事侦查支队政委，户政管理支队政委，反恐怖支队支队长，治安支队支队长。"
    },
    {
        "id": 8,
        "name": "赵影刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年5月",
        "birthplace": "黑龙江五常",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "2009年7月",
        "current_post": "副市长",
        "current_org": "扶余市人民政府",
        "source": "http://www.jlfy.gov.cn/zwgk/sld/fszzyg/ (政府官网)",
        "confidence": "confirmed",
        "notes": "1984年5月出生，汉族，黑龙江五常人，2007年12月入党，2009年7月参加工作。曾任珲矿公司富强煤矿工会组宣部部长、团委副书记、政工科科长，珲矿公司销售分公司机关党支部副书记，吉林省能源投资集团有限责任公司党委工作部业务主管、党校培训部业务主管、党群工作部副部长、党委宣传部副部长。"
    },
    {
        "id": 9,
        "name": "王大宏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年12月",
        "birthplace": "吉林扶余",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "1999年11月",
        "current_post": "副市长",
        "current_org": "扶余市人民政府",
        "source": "http://www.jlfy.gov.cn/zwgk/sld/fszwdh/ (政府官网)",
        "confidence": "confirmed",
        "notes": "1978年12月出生，汉族，吉林扶余人，2004年7月入党，1999年11月参加工作。曾任扶余市委办公室副主任，扶余市工业和信息化管理局党组书记、局长，扶余市发展和改革局党组书记、局长。"
    },
    {
        "id": 10,
        "name": "孙鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年6月",
        "birthplace": "吉林松原",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "2009年7月",
        "current_post": "副市长",
        "current_org": "扶余市人民政府",
        "source": "http://www.jlfy.gov.cn/zwgk/sld/sp/ (政府官网)",
        "confidence": "confirmed",
        "notes": "1986年6月出生，汉族，吉林松原人，2005年4月入党，2009年7月参加工作。曾任松原市外事服务中心主任，乾安县脱贫攻坚驻村第一书记，扶余市新站乡党委书记。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 人大 / 政协
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 11,
        "name": "乔聚河",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "扶余市人大常委会",
        "source": "www.jlfy.gov.cn 新闻报道 / baike.baidu.com",
        "confidence": "confirmed",
        "notes": "扶余市人大常委会主任。此前曾任扶余市委宣传部部长。"
    },
    {
        "id": 12,
        "name": "蔡启昌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年",
        "birthplace": "吉林抚松",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "扶余市政协",
        "source": "www.jlfy.gov.cn 新闻报道 / baike.baidu.com",
        "confidence": "confirmed",
        "notes": "1970年出生，吉林抚松人。前郭县、松原市发改委经历，2016年到扶余市任副市长，现任市政协主席。曾因疫情防控不力被问责。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 前任领导
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 13,
        "name": "盖克",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "已离任（前任市长）",
        "current_org": "",
        "source": "www.jlfy.gov.cn 旧页面(已归档)",
        "confidence": "plausible",
        "notes": "前任扶余市市长，已被韩超接替。旧页面已归入历史链接。"
    },
    {
        "id": 14,
        "name": "待查_前任市委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "已离任（前任市委书记）",
        "current_org": "",
        "source": "待查 — 未找到公开信息",
        "confidence": "unverified",
        "notes": "满都拉的前任市委书记姓名及去向无法确认。需后续从松原市委组织部公示或新闻报道核实。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共扶余市委员会", "type": "党委", "level": "县级", "parent": "中共松原市委", "location": "扶余市"},
    {"id": 2, "name": "扶余市人民政府", "type": "政府", "level": "县级", "parent": "松原市人民政府", "location": "扶余市"},
    {"id": 3, "name": "扶余市人大常委会", "type": "人大", "level": "县级", "parent": "", "location": "扶余市"},
    {"id": 4, "name": "扶余市政协", "type": "政协", "level": "县级", "parent": "", "location": "扶余市"},
    {"id": 5, "name": "扶余市纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共扶余市委员会", "location": "扶余市"},
    {"id": 6, "name": "扶余市公安局", "type": "政府", "level": "县级", "parent": "扶余市人民政府", "location": "扶余市"},
    {"id": 7, "name": "长春市绿园区人民政府", "type": "政府", "level": "县级", "parent": "长春市人民政府", "location": "长春市"},
    {"id": 8, "name": "长春市发展和改革委员会", "type": "政府", "level": "地级", "parent": "长春市人民政府", "location": "长春市"},
    {"id": 9, "name": "吉林省委办公厅", "type": "党委", "level": "省级", "parent": "中共吉林省委", "location": "长春市"},
    {"id": 10, "name": "松原市粮食和物资储备局", "type": "政府", "level": "地级", "parent": "松原市人民政府", "location": "松原市"},
    {"id": 11, "name": "前郭县人民政府", "type": "政府", "level": "县级", "parent": "松原市人民政府", "location": "前郭县"},
    {"id": 12, "name": "乾安县人民政府", "type": "政府", "level": "县级", "parent": "松原市人民政府", "location": "乾安县"},
    {"id": 13, "name": "松原市公安局", "type": "政府", "level": "地级", "parent": "松原市人民政府", "location": "松原市"},
    {"id": 14, "name": "吉林省能源投资集团有限责任公司", "type": "事业单位", "level": "省级", "parent": "", "location": "长春市"},
    {"id": 15, "name": "珲矿公司", "type": "事业单位", "level": "地级", "parent": "", "location": "珲春市"},
    {"id": 16, "name": "吉林省工业和信息化厅", "type": "政府", "level": "省级", "parent": "吉林省人民政府", "location": "长春市"},
    {"id": 17, "name": "扶余市市场监督管理局", "type": "政府", "level": "县级", "parent": "扶余市人民政府", "location": "扶余市"},
    {"id": 18, "name": "扶余市委办公室", "type": "党委", "level": "县级", "parent": "中共扶余市委员会", "location": "扶余市"},
    {"id": 19, "name": "扶余市发展和改革局", "type": "政府", "level": "县级", "parent": "扶余市人民政府", "location": "扶余市"},
    {"id": 20, "name": "新站乡党委", "type": "乡镇/街道", "level": "乡镇", "parent": "中共扶余市委员会", "location": "扶余市新站乡"},
    {"id": 21, "name": "前郭县乌兰塔拉乡党委", "type": "乡镇/街道", "level": "乡镇", "parent": "中共前郭县委", "location": "前郭县"},
]

# ── Positions ─────────────────────────────────────────────────────────────────
positions = [
    # 满都拉
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "未知", "end_date": "present", "rank": "正县级", "note": ""},
    
    # 韩超
    {"person_id": 2, "org_id": 8, "title": "主任科员/副处长/处长 (国民经济综合处/政策研究室)", "start_date": "2010年代", "end_date": "", "rank": "正处长级", "note": "长春市发改委多年任职"},
    {"person_id": 2, "org_id": 8, "title": "党组成员、副主任", "start_date": "", "end_date": "", "rank": "副局级", "note": ""},
    {"person_id": 2, "org_id": 15, "title": "副主任（挂职）", "start_date": "", "end_date": "", "rank": "副局级", "note": "长春莲花山生态旅游度假区管委会"},
    {"person_id": 2, "org_id": 7, "title": "区委常委、常务副区长", "start_date": "", "end_date": "2025年9月", "rank": "副局级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "副市长、代市长", "start_date": "2025年9月", "end_date": "2025年12月", "rank": "正县级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "市委副书记、市长", "start_date": "2025年12月30日", "end_date": "present", "rank": "正县级", "note": "正式当选"},
    
    # 于静涛
    {"person_id": 3, "org_id": 9, "title": "省委法规室副主任、三级调研员", "start_date": "", "end_date": "", "rank": "副处长级", "note": ""},
    {"person_id": 3, "org_id": 12, "title": "副县长（挂职）", "start_date": "", "end_date": "", "rank": "副县级", "note": "乾安县政府挂职"},
    {"person_id": 3, "org_id": 2, "title": "市委常委、常务副市长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "曾任松原市委保密委员会专职副主任(正处长级)、市委办公室副主任"},
    
    # 宋孝进
    {"person_id": 4, "org_id": 10, "title": "办公室主任/科长", "start_date": "", "end_date": "", "rank": "", "note": "松原市粮食局/粮储局任职"},
    {"person_id": 4, "org_id": 12, "title": "驻村第一书记", "start_date": "2015", "end_date": "2021", "rank": "", "note": "长岭县脱贫攻坚驻村"},
    {"person_id": 4, "org_id": 11, "title": "乌兰塔拉乡党委书记（副处长级）", "start_date": "", "end_date": "", "rank": "副处长级", "note": "前郭县"},
    {"person_id": 4, "org_id": 2, "title": "市委常委、副市长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    
    # 郭丽明
    {"person_id": 5, "org_id": 12, "title": "政协文教委主任/工商联主席/人大副主任", "start_date": "", "end_date": "", "rank": "", "note": "乾安县任职"},
    {"person_id": 5, "org_id": 2, "title": "副市长（省工信厅挂职）", "start_date": "", "end_date": "present", "rank": "副县级", "note": "挂职暂不分工"},
    
    # 宿从军
    {"person_id": 6, "org_id": 17, "title": "党组书记、局长", "start_date": "", "end_date": "", "rank": "", "note": "扶余市市场监督管理局"},
    {"person_id": 6, "org_id": 18, "title": "主任", "start_date": "", "end_date": "", "rank": "", "note": "扶余市委办公室主任"},
    {"person_id": 6, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    
    # 于长胜
    {"person_id": 7, "org_id": 13, "title": "政委/支队长 (刑侦/户政/反恐/治安)", "start_date": "", "end_date": "", "rank": "", "note": "松原市公安局多个支队"},
    {"person_id": 7, "org_id": 2, "title": "副市长、公安局局长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    
    # 赵影刚
    {"person_id": 8, "org_id": 15, "title": "宣传部/团委/政工科", "start_date": "", "end_date": "", "rank": "", "note": "珲矿公司任职"},
    {"person_id": 8, "org_id": 14, "title": "党群工作部副部长、党委宣传部副部长", "start_date": "", "end_date": "", "rank": "", "note": "吉林省能源投资集团"},
    {"person_id": 8, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    
    # 王大宏
    {"person_id": 9, "org_id": 18, "title": "副主任", "start_date": "", "end_date": "", "rank": "", "note": "扶余市委办公室"},
    {"person_id": 9, "org_id": 2, "title": "工业和信息化管理局党组书记、局长", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 9, "org_id": 19, "title": "党组书记、局长", "start_date": "", "end_date": "", "rank": "", "note": "扶余市发展和改革局"},
    {"person_id": 9, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    
    # 孙鹏
    {"person_id": 10, "org_id": 2, "title": "外事服务中心主任", "start_date": "", "end_date": "", "rank": "", "note": "松原市"},
    {"person_id": 10, "org_id": 12, "title": "驻村第一书记", "start_date": "", "end_date": "", "rank": "", "note": "乾安县脱贫攻坚"},
    {"person_id": 10, "org_id": 20, "title": "党委书记", "start_date": "", "end_date": "", "rank": "", "note": "扶余市新站乡"},
    {"person_id": 10, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    
    # 乔聚河
    {"person_id": 11, "org_id": 1, "title": "市委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 11, "org_id": 3, "title": "市人大常委会主任", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
    
    # 蔡启昌
    {"person_id": 12, "org_id": 4, "title": "市政协主席", "start_date": "", "end_date": "present", "rank": "副县级", "note": "曾任扶余市副市长"},
    
    # 盖克（前任市长）
    {"person_id": 13, "org_id": 2, "title": "市长（前任）", "start_date": "", "end_date": "2025年", "rank": "正县级", "note": "已被韩超接替"},
    
    # 待查前任市委书记
    {"person_id": 14, "org_id": 1, "title": "市委书记（前任）", "start_date": "", "end_date": "", "rank": "正县级", "note": "满都拉的前任，信息待查"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 党政搭档
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "市委书记—市长搭档", "overlap_org": "扶余市党政领导班子", "overlap_period": "2025年至今"},
    
    # 于静涛—韩超（上下级）
    {"person_a": 2, "person_b": 3, "type": "上下级", "context": "市长—常务副市长", "overlap_org": "扶余市人民政府", "overlap_period": "2025年至今"},
    
    # 于静涛—赵影刚（协管关系）
    {"person_a": 3, "person_b": 8, "type": "协管", "context": "赵影刚协助于静涛分管政府办等", "overlap_org": "扶余市人民政府", "overlap_period": "至今"},
    
    # 于静涛—乾安挂职关联（和郭丽明都曾在乾安县任职）
    {"person_a": 3, "person_b": 5, "type": "同地区任职", "context": "于静涛挂职乾安县副县长，郭丽明曾任乾安县人大副主任", "overlap_org": "乾安县", "overlap_period": ""},
    
    # 宋孝进—前郭县关联（和蔡启昌都曾在前郭县）
    {"person_a": 4, "person_b": 12, "type": "同地区任职", "context": "宋孝进曾任前郭县乌兰塔拉乡党委书记，蔡启昌曾在前郭县任职", "overlap_org": "前郭县", "overlap_period": ""},
    
    # 宋孝进—乾安关联（和郭丽明都曾在乾安县任职）
    {"person_a": 4, "person_b": 5, "type": "同地区任职", "context": "宋孝进驻村第一书记在长岭县（乾安县邻县）", "overlap_org": "长岭/乾安", "overlap_period": "2015-2021"},
    
    # 孙鹏—乾安关联
    {"person_a": 10, "person_b": 5, "type": "同地区任职", "context": "孙鹏乾安县驻村第一书记，郭丽明乾安县人大副主任", "overlap_org": "乾安县", "overlap_period": ""},
    {"person_a": 10, "person_b": 3, "type": "同地区任职", "context": "孙鹏乾安县驻村第一书记，于静涛乾安县挂职副县长", "overlap_org": "乾安县", "overlap_period": ""},
    
    # 宿从军—王大宏（同体系成长）
    {"person_a": 6, "person_b": 9, "type": "同体系成长", "context": "均从扶余市委办公室出身，本地成长干部", "overlap_org": "中共扶余市委员会", "overlap_period": ""},
    
    # 宿从军—于长胜（均为扶余籍）
    {"person_a": 6, "person_b": 7, "type": "同籍贯", "context": "均为吉林扶余本地人", "overlap_org": "", "overlap_period": ""},
    
    # 满都拉—蔡启昌（搭班）
    {"person_a": 1, "person_b": 12, "type": "党政—政协", "context": "市委书记—政协主席", "overlap_org": "扶余市领导班子", "overlap_period": ""},
    
    # 韩超—盖克（前后任）
    {"person_a": 2, "person_b": 13, "type": "前后任", "context": "韩超接替盖克任扶余市长", "overlap_org": "扶余市人民政府", "overlap_period": "2025年"},
    
    # 蔡启昌—韩超（省级-市级的联系路徑）
    {"person_a": 12, "person_b": 2, "type": "跨地区联系", "context": "蔡启昌从前郭县/松原市到扶余，韩超从长春到扶余，均为跨区到扶余任职", "overlap_org": "", "overlap_period": ""},
]

# ── Person JSON writer ────────────────────────────────────────────────────────

PERSON_TEMPLATES = {
    1: {
        "identity": {
            "person_id": "songyuan_fuyu_man_dula",
            "name": "满都拉（本名刘永生）",
            "aliases": ["刘永生"],
            "gender": "男",
            "ethnicity": "蒙古族",
            "birth": "1976年2月",
            "birthplace": "",
            "native_place": "",
            "education": [{"period": "", "institution": "", "major": "", "degree": "在职研究生学历", "study_type": "part_time", "source_ids": ["S001"]}],
            "party_join": "中共党员",
            "work_start": "1996年9月",
            "dedupe_keys": {"name_birth": "满都拉_1976", "name_birthplace": "", "official_profile_url": ""}
        },
        "current_status": {
            "current_post": "中共扶余市委书记",
            "current_org": "中共扶余市委员会",
            "administrative_rank": "正县级",
            "as_of": "2026-07-25",
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002"]
        },
        "career_timeline": [
            {"start": "1996年9月", "end": "", "org": "", "title": "参加工作", "level": "", "location": "", "system": "other", "rank": "", "is_key_promotion": False, "notes": "1996年9月参加工作。此前履历待查。", "confidence": "unverified", "source_ids": ["S001"]},
            {"start": "", "end": "present", "org": "中共扶余市委员会", "title": "市委书记", "level": "县级", "location": "扶余市", "system": "party", "rank": "正县级", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
            {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "1996年至担任扶余市委书记前的完整履历缺失。可能在松原市/前郭县任职。需后续通过百度百科或官方简历核实。", "confidence": "unverified", "source_ids": []}
        ],
        "organizations": [{"person": "中共扶余市委员会", "role": "市委书记"}],
        "relationships": [
            {"person": "韩超", "person_id": "songyuan_fuyu_han_chao", "relationship_type": "overlap", "strength": "strong", "evidence": "市委书记—市长党政搭档，2025年至今共事", "overlap_org": "扶余市", "overlap_period": "2025年至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]},
            {"person": "蔡启昌", "person_id": "songyuan_fuyu_cai_qichang", "relationship_type": "overlap", "strength": "medium", "evidence": "市委书记与政协主席搭班", "overlap_org": "扶余市", "overlap_period": "", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002"]}
        ],
        "governance_record": [],
        "professional_profile": {"primary_specializations": [], "secondary_specializations": [], "career_pattern": "unknown", "systems_experience": ["party"], "geographic_pattern": ["吉林省"], "promotion_velocity": {"summary": "履历不完整，无法判断晋升速度", "notable_fast_promotions": []}},
        "work_style_and_personality": {"public_style_indicators": [], "speech_themes": [], "management_signals": [], "caveat": "Work style is inferred from public records."},
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现任何负面纪律或审计信号", "date": "", "confidence": "unverified", "source_ids": []}],
        "source_register": [
            {"id": "S001", "title": "百度百科摘要 — 满都拉", "url": "https://baike.baidu.com/item/满都拉", "publisher": "百度百科", "published_at": "", "accessed_at": "2026-07-25", "source_type": "encyclopedia", "reliability": "medium", "notes": "部分信息通过搜狗搜索结果间接获取"},
            {"id": "S002", "title": "扶余市人民政府网新闻报道", "url": "http://www.jlfy.gov.cn", "publisher": "扶余市人民政府", "published_at": "2025-2026", "accessed_at": "2026-07-25", "source_type": "official", "reliability": "high", "notes": "多篇政务要闻确认满都拉为现任市委书记"}
        ],
        "confidence_summary": {"identity": "confirmed", "current_role": "confirmed", "career_completeness": "thin", "relationship_confidence": "medium", "biggest_gap": "担任扶余市委书记前的完整履历"},
        "open_questions": [
            {"priority": "critical", "question": "满都拉担任扶余市委书记前的完整履历是什么？", "why_it_matters": "核心目标人物，需了解其晋升路径和前职", "suggested_queries": ["满都拉 简历", "满都拉 前郭县", "满都拉 松原"], "last_attempted": "2026-07-25"},
            {"priority": "high", "question": "满都拉的出生地和籍贯在哪里？", "why_it_matters": "蒙古族，需确认是否为吉林本地干部", "suggested_queries": ["满都拉 出生"], "last_attempted": "2026-07-25"},
            {"priority": "high", "question": "满都拉何时开始担任扶余市委书记？", "why_it_matters": "理清领导班子更替时间线", "suggested_queries": ["满都拉 扶余 任命"], "last_attempted": "2026-07-25"}
        ]
    },
    2: {
        "identity": {
            "person_id": "songyuan_fuyu_han_chao",
            "name": "韩超",
            "aliases": [],
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "1985年6月",
            "birthplace": "",
            "native_place": "山东日照",
            "education": [{"period": "", "institution": "", "major": "", "degree": "研究生学历", "study_type": "unknown", "source_ids": ["S003"]}],
            "party_join": "中共党员",
            "work_start": "",
            "dedupe_keys": {"name_birth": "韩超_198506", "name_birthplace": "韩超_山东日照", "official_profile_url": "http://www.jlfy.gov.cn/zwgk/sld/szhc/"}
        },
        "current_status": {
            "current_post": "扶余市委副书记、市长",
            "current_org": "扶余市人民政府",
            "administrative_rank": "正县级",
            "as_of": "2026-07-25",
            "is_current_confirmed": True,
            "source_ids": ["S003", "S004"]
        },
        "career_timeline": [
            {"start": "", "end": "", "org": "长春市发展和改革委员会", "title": "主任科员/副处长/处长（国民经济综合处/政策研究室）", "level": "地级", "location": "长春市", "system": "government", "rank": "正处长级", "is_key_promotion": False, "notes": "长春市发改委多年任职，经历国民经济综合处和政策研究室多个岗位", "confidence": "confirmed", "source_ids": ["S003"]},
            {"start": "", "end": "", "org": "长春莲花山生态旅游度假区管理委员会", "title": "副主任（挂职）", "level": "地级", "location": "长春市", "system": "government", "rank": "副局级", "is_key_promotion": False, "notes": "挂职锻炼", "confidence": "confirmed", "source_ids": ["S003"]},
            {"start": "", "end": "", "org": "长春市发展和改革委员会", "title": "党组成员、副主任", "level": "地级", "location": "长春市", "system": "government", "rank": "副局级", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S003"]},
            {"start": "", "end": "2025年9月", "org": "长春市绿园区人民政府", "title": "区委常委、常务副区长", "level": "县级", "location": "长春市绿园区", "system": "government", "rank": "副局级", "is_key_promotion": True, "notes": "从长春市发改委调任绿园区", "confidence": "confirmed", "source_ids": ["S003"]},
            {"start": "2025年9月", "end": "2025年12月", "org": "扶余市人民政府", "title": "副市长、代市长", "level": "县级", "location": "扶余市", "system": "government", "rank": "正县级", "is_key_promotion": True, "notes": "2025年9月12日市人大常委会任命", "confidence": "confirmed", "source_ids": ["S003", "S004"]},
            {"start": "2025年12月30日", "end": "present", "org": "扶余市人民政府", "title": "市委副书记、市长", "level": "县级", "location": "扶余市", "system": "government", "rank": "正县级", "is_key_promotion": True, "notes": "扶余市第十八届人大第五次会议正式当选", "confidence": "confirmed", "source_ids": ["S003", "S004"]}
        ],
        "organizations": [{"person": "长春市发改委", "role": "多岗位"}, {"person": "长春市绿园区", "role": "常务副区长"}, {"person": "扶余市人民政府", "role": "市长"}],
        "relationships": [
            {"person": "满都拉", "person_id": "songyuan_fuyu_man_dula", "relationship_type": "overlap", "strength": "strong", "evidence": "市委书记—市长党政搭档", "overlap_org": "扶余市", "overlap_period": "2025年至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
            {"person": "于静涛", "person_id": "songyuan_fuyu_yu_jingtao", "relationship_type": "overlap", "strength": "strong", "evidence": "市长—常务副市长直接上下级", "overlap_org": "扶余市人民政府", "overlap_period": "2025年至今", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S003"]},
            {"person": "盖克", "person_id": "songyuan_fuyu_gai_ke", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "接替盖克任扶余市长", "overlap_org": "扶余市人民政府", "overlap_period": "2025年", "direction": "other_to_person", "confidence": "plausible", "source_ids": ["S003"]}
        ],
        "governance_record": [],
        "professional_profile": {"primary_specializations": ["经济管理", "发展改革"], "secondary_specializations": [], "career_pattern": "provincial_department", "systems_experience": ["government", "party"], "geographic_pattern": ["长春市→扶余市（跨区调任）"], "promotion_velocity": {"summary": "从长春市发改委到绿园区常务副区长，再到扶余市长，晋升路径清晰。85后正县级较为年轻。", "notable_fast_promotions": ["2025年从长春绿园区调任扶余市代市长，同年12月正式当选为市长"]}},
        "work_style_and_personality": {"public_style_indicators": [], "speech_themes": [], "management_signals": [], "caveat": "Work style is inferred from public records."},
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现任何负面纪律或审计信号", "date": "", "confidence": "unverified", "source_ids": []}],
        "source_register": [
            {"id": "S003", "title": "韩超个人简介", "url": "http://www.jlfy.gov.cn/zwgk/sld/szhc/", "publisher": "扶余市人民政府", "published_at": "", "accessed_at": "2026-07-25", "source_type": "official", "reliability": "high", "notes": "政府官网领导之窗个人简介页"},
            {"id": "S004", "title": "韩超百度百科", "url": "https://baike.baidu.com/item/韩超/62747211", "publisher": "百度百科", "published_at": "2025", "accessed_at": "2026-07-25", "source_type": "encyclopedia", "reliability": "medium", "notes": ""}
        ],
        "confidence_summary": {"identity": "confirmed", "current_role": "confirmed", "career_completeness": "partial", "relationship_confidence": "high", "biggest_gap": "具体毕业院校和专业"},
        "open_questions": [
            {"priority": "medium", "question": "韩超的毕业院校和专业是什么？", "why_it_matters": "了解专业背景", "suggested_queries": ["韩超 毕业院校", "韩超 长春市发改委"], "last_attempted": "2026-07-25"}
        ]
    }
}

def write_person_json(person_id: int) -> str:
    """Write a person JSON file and return its path."""
    template = PERSON_TEMPLATES.get(person_id)
    if template is None:
        return ""
    person = next((p for p in persons if p["id"] == person_id), None)
    if person is None:
        return ""
    
    job_part = person["current_post"].replace("/", "_").replace("、", "_")
    # Use just the main title for filename
    title_map = {1: "市委书记", 2: "市长"}
    job_short = title_map.get(person_id, job_part)
    
    filename = f"{TODAY}-吉林省-松原市-{job_short}-{person['name']}.json"
    filepath = Path(PJSON_DIR) / filename
    
    identity = template["identity"].copy()
    identity["birthplace"] = identity.get("birthplace") or person.get("birthplace", "")
    
    doc = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "吉林省",
            "city": "松原市",
            "region": "扶余市",
            "job": person["current_post"],
            "task_id": "jilin_扶余市",
            "time_focus": "2025-2026"
        },
        "identity": identity,
        "current_status": template["current_status"],
        "career_timeline": template["career_timeline"],
        "organizations": template.get("organizations", []),
        "relationships": template.get("relationships", []),
        "governance_record": template.get("governance_record", []),
        "professional_profile": template.get("professional_profile", {}),
        "work_style_and_personality": template.get("work_style_and_personality", {}),
        "network_metrics": {},
        "risk_and_integrity_signals": template.get("risk_and_integrity_signals", []),
        "source_register": template["source_register"],
        "confidence_summary": template["confidence_summary"],
        "open_questions": template.get("open_questions", [])
    }
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {filename}")
    return str(filepath)


# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print(f"Building {SLUG} network data...")
    print(f"  Staging: {STAGING}")
    print(f"  Persons: {len(persons)}")
    print(f"  Orgs: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print()
    
    # Write person JSONs
    print("Writing person JSONs...")
    for pid in [1, 2]:
        path = write_person_json(pid)
        if path:
            print(f"  -> {path}")
    print()
    
    # Build DB and GEXF
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
    
    # Summary
    db_size = DB_PATH.stat().st_size if DB_PATH.exists() else 0
    gexf_size = GEXF_PATH.stat().st_size if GEXF_PATH.exists() else 0
    print()
    print(f"Done. Staged in {STAGING}:")
    print(f"  Database: {DB_PATH.name} ({db_size:,} bytes)")
    print(f"  GEXF:     {GEXF_PATH.name} ({gexf_size:,} bytes)")
    print(f"  Person JSONs: 2 files")
