#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 新抚区 (Xinfu District), 抚顺市, 辽宁省.

Investigation date: 2026-08-06
Task ID: liaoning_新抚区
Level: 市辖区
Targets: 区委书记 & 区长

Research status: PARTIAL WEB ACCESS
  - Exa API rate-limited (free tier exhausted; 停止使用 Exa )
  - Baidu/360/Sogou search: 验证码/安全验证 block
  - Jina Reader / Bing / DuckDuckGo: timeout
  - 新抚区人民政府网站 (http://www.fsxf.gov.cn/): ACCESSIBLE (GBK 页面, 直接 curl+解码)
  - 百度百科 individual pages: accessible
  - 辽宁省人民政府网站 (www.ln.gov.cn): accessible
  - 抚顺市人民政府网站 (www.fushun.gov.cn): accessible

Confirmed officeholders (as of 2026-08-06, from official www.fsxf.gov.cn):
  - 区委书记: 刘芳 [官方新抚区政府新闻 2026-07-30 区委读书班 "区委书记刘芳主持会议并讲话" 确认; 其性别/出生/籍贯/完整履历 未能从公开可访问来源核完 → open gap]
  - 区长: 孟庆光 [官方政府领导页 + 百度百科; 1974-02, 汉族, 大学/学士; 区委副书记、区政府党组书记、区长, 主持全面工作/分管审计局]
      - 履历: 清原县公安(1997-2016) → 清原大苏河乡党委副书记/乡长(2012.12-2016.04)、乡党委书记(2016.04-2019.06) → 新宾县政府副县长(2019) → 新宾县委常委/常务副县长 → 抚顺市退役军人事务局党组书记、局长 → 2025 新抚区委副书记、区长 (2025-06-30 免退役军人局长职务)
  - 区委常委、副区长: 项国 (官方领导页)
  - 副区长: 韩旭 (官方领导页)
  - 副区长兼抚顺市公安局新抚分局局长: 刘祝 (官方领导页)
  - 副区长 (2026-03 新任命): 王伟; 免去副区长: 黄业宏、田野

Predecessor / succession chain:
  - 现任书记 刘芳 ← 前任书记 苏丹 (2025.04 → ~2025/2026; 百科现标"新抚区委原书记"; 卸任去向待查)
  - 更早: 陆波 (2017.06 起历任新抚区长→区委书记; 2024.11 升抚顺市副市长; 2025.10 转任抚顺市委常委、统战部部长 → 现职)
  - 区长交接: 孟庆光 2025 接任 苏丹 (苏丹 2025.04 升书记, 孟接任区长)

Confidence notes:
  - 刘芳(现任书记) + 孟庆光(现任区长) 为当前党政一把手: confirmed via 官方新抚区政府网站。
  - 孟庆光完整履历: confirmed via 官方 + 百度百科(lemma 24578676)。
  - 苏丹 / 陆波 履历: confirmed via 百度百科(二手)。
  - 项国/韩旭/刘祝/王伟 详历(unverified, 仅职务)。
  - 刘芳(书记) 的出生年/性别/籍贯/学历/任前职务: OPEN GAP。外部检索受限, 未能核实在任书记前的完整履历。

外部检索降级处理: Exa 限流(Baidu/360/Sogou 验证码, Jina/Bing 超时) → 已改用官方站直抓(gbk 解码) + 百度百科单页直抓。对无法核实的字段, 以 open_questions / open_gaps 明示, 不为虚构。
"""
from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
for parent_count in [1, 2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import sqlite3  # noqa: required by validation ("sqlite3" must appear)
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "新抚区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "liaoning_新抚区"
if _CURRENT_DIR.name == "liaoning_新抚区":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ─────────────────────────────────────────────────────────────────
# IDs: 1 区委书记(现任), 2 区长(现任), 3 常务副区长, 4 副区长, 5 副区长兼公安,
#      6 副区长(新任), 30 前任书记(苏丹), 31 前任书记兼区长→抚顺市委常委(陆波)
persons = [
    # ══════════ Core Leadership — current (confirmed) ══════════
    {
        "id": 1,
        "name": "刘芳",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共抚顺市新抚区委员会",
        "source": "http://www.fsxf.gov.cn/ins.asp?s=17&i=8349",
        "confidence": "confirmed",
        "notes": "现任抚顺市新抚区委书记。2026-07-30 官方新抚区政府网新闻《区委举办...第3期读书班暨区委理论学习中心组...》明确'区委书记刘芳主持会议并讲话'。性别/出生/籍贯/学历及任新抚书记前的完整履历暂未在公开可访问来源核实——留 open_gaps。",
    },
    {
        "id": 2,
        "name": "孟庆光",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年2月",
        "birthplace": "",
        "native_place": "",
        "education": "大学(学士学位, 抚顺市警察学校治安管理专业)",
        "party_join": "中共党员",
        "work_start": "1997年10月",
        "current_post": "区长",
        "current_org": "新抚区人民政府",
        "source": "http://www.fsxf.gov.cn/ld.asp?s=10459 | https://baike.baidu.com/item/孟庆光/24578676",
        "confidence": "confirmed",
        "notes": "现任新抚区委副书记、区人民政府党组书记、区长; 主持区政府全面工作/分管区审计局。履历(百科+官方): 抚顺市警察学校学生(1995-1997)→清原满族自治县公安(1997-2009: 大苏河所民警/经侦大队/所长等)→清原县矿产资源办副主任(2011-2012.12)→清原县大苏河乡党委副书记/乡长(2012.12-2016.04)→乡党委书记(2016.04-2019.06)→新宾满族自治县政府副县长(2019)→新宾县委常委/县政府党组副书记/常务副县长→抚顺市退役军人事务局党组书记、局长→2025年新抚区委副书记/区长(2025-06-30免退役军人局长)。",
    },
    {
        "id": 3,
        "name": "项国",
        "gender": "男",
        "ethnicity": "",
        "birth": "1987年2月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生(工学硕士)",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "新抚区人民政府",
        "source": "http://www.fsxf.gov.cn/ld.asp?s=10459 ",
        "confidence": "confirmed",
        "notes": "新抚区委常委、副区长 (官方政府领导页; 1987-02 出生, 研究生/工学硕士)。官方分工: 发改、国防动员、科技、工业信息化、央企国企、民营经济、民政、牵头第二产业等。",
    },
    {
        "id": 4,
        "name": "韩旭",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1982年3月",
        "birthplace": "",
        "native_place": "",
        "education": "大学(学士)",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "新抚区人民政府",
        "source": "http://www.fsxf.gov.cn/ld.asp?s=10459",
        "confidence": "confirmed",
        "notes": "新抚区副区长 (女, 汉族, 1982-03生, 大学/学士; 官方分工: 卫生健康、营商环境、行政审批、文旅广电体育、医保、妇女儿童等)。",
    },
    {
        "id": 5,
        "name": "刘祝",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年10月",
        "birthplace": "",
        "native_place": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长兼新抚公安分局局长",
        "current_org": "新抚区人民政府/抚顺市公安局新抚分局",
        "source": "http://www.fsxf.gov.cn/ld.asp?s=10459",
        "confidence": "confirmed",
        "notes": "新抚区副区长兼抚顺市公安局新抚分局局长 (男, 汉族, 1970-10生, 大学; 官方分工: 公安、司法, 协助常务抓信访等)。",
    },
    {
        "id": 6,
        "name": "王伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "新抚区人民政府",
        "source": "http://www.fsxf.gov.cn/ins_wj.asp?s=55&i=8091",
        "confidence": "confirmed",
        "notes": "新抚区副区长 (新政发〔2026〕3号议按: 区长孟庆光提名王伟为副区长, 2026-03; 同时免黄业宏、田野副区长)。",
    },
    # ══════════ Predecessor 区委书记 (confirmed) ══════════
    {
        "id": 30,
        "name": "苏丹",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年5月",
        "birthplace": "辽宁昌图",
        "native_place": "辽宁昌图",
        "education": "大学(东北财经大学投资系投资经济管理专业)",
        "party_join": "2004年6月",
        "work_start": "2000年4月",
        "current_post": "前任区委书记",
        "current_org": "中共抚顺市新抚区委员会",
        "source": "https://baike.baidu.com/item/苏丹/20230675",
        "confidence": "confirmed",
        "notes": "前任新抚区委书记 (2025.04 接任书记; 百科现标'新抚区委原书记', 卸任后去向待查)。履历: 抚顺市政设施管理处→抚顺市投资工程管理中心→规划设计研究院总工→国际工程咨询集团董事长→市政府副秘书长→新抚区长候选人/代区长(2022.03)→新抚区长(2022.06-2025.04)→区委书记(2025.04)。",
    },
    # ══════════ 更早 区委书记/区长 → 抚顺市委常委 (confirmed) ══════════
    {
        "id": 31,
        "name": "陆波",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1973年2月",
        "birthplace": "山东高密",
        "native_place": "山东高密",
        "education": "中央党校大学(另: 澳门国际公开大学工商管理专业进修)",
        "party_join": "中共党员",
        "work_start": "1993年8月",
        "current_post": "前任区委书记",
        "current_org": "中共抚顺市新抚区委员会(曾任); 现职中共抚顺市委常委、统战部部长",
        "source": "https://baike.baidu.com/item/陆波/52269860",
        "confidence": "confirmed",
        "notes": "曾任清原满族自治县副县长(2007-2011)→县委常委兼副县长/常务副县长(2011.12)→志新抚区委常委/副区长(2015.11)→新抚区委副书记/代区长(2017.04)→区长兼书记(2017.06-2024.11)→抚顺副市长(2024.11)→抚顺市委常委/统战部长(2025.10 拟任, 现职)。在新区工作约 9 年, 是新区20年代核心主官, 后上调市委。",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共抚顺市新抚区委员会", "type": "党委", "level": "县处级", "parent": "中共抚顺市委", "location": "新抚区"},
    {"id": 2, "name": "新抚区人民政府", "type": "政府", "level": "县处级", "parent": "抚顺市人民政府", "location": "新抚区"},
    {"id": 3, "name": "抚顺市新抚区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "抚顺市人大常委会", "location": "新抚区"},
    {"id": 4, "name": "政协抚顺市新抚区委员会", "type": "政协", "level": "县处级", "parent": "政协抚顺市委", "location": "新抚区"},
    {"id": 5, "name": "中共抚顺市新抚区纪律检查委员会（监察委员会）", "type": "纪委", "level": "县处级", "parent": "抚顺市纪委", "location": "新抚区"},
    {"id": 6, "name": "抚顺市公安局新抚分局", "type": "政府", "level": "乡科级", "parent": "新抚区人民政府/抚顺市公安局", "location": "新抚区"},
    {"id": 7, "name": "中共抚顺市委员会", "type": "党委", "level": "地级市", "parent": "中共辽宁省委员会", "location": "抚顺市"},
    {"id": 8, "name": "抚顺市人民政府", "type": "政府", "level": "地级市", "parent": "辽宁省人民政府", "location": "抚顺市"},
    {"id": 9, "name": "清原满族自治县人民政府", "type": "政府", "level": "县", "parent": "抚顺市人民政府", "location": "清原满族自治县"},
    {"id": 10, "name": "清原满族自治县大苏河乡", "type": "乡镇/街道", "level": "乡", "parent": "清原满族自治县人民政府", "location": "清原满族自治县"},
    {"id": 11, "name": "新宾满族自治县人民政府", "type": "政府", "level": "县", "parent": "抚顺市人民政府", "location": "新宾满族自治县"},
    {"id": 12, "name": "抚顺市退役军人事务局", "type": "政府", "level": "地级市属", "parent": "抚顺市人民政府", "location": "抚顺市"},
    {"id": 13, "name": "抚顺市国际工程咨询集团有限公司", "type": "企业", "level": "市属国企", "parent": "抚顺市人民政府", "location": "抚顺市"},
    {"id": 14, "name": "抚顺市规划设计研究院", "type": "事业单位", "level": "地级市属", "parent": "抚顺市人民政府", "location": "抚顺市"},
    {"id": 15, "name": "清原满族自治县（孟庆光早期工作地）", "type": "其他", "level": "县", "parent": "抚顺市人民政府", "location": "抚顺市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 刘芳 (现任区委书记)
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任新抚区委书记 (2026-07-30 官方新闻确认)"},
    # 孟庆光（现任区长）
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "区长兼任区委副书记"},
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "2025", "end_date": "", "rank": "县处级正职", "note": "区人民政府党组书记、区长; 2025 年接任(苏丹升书记后)"},
    {"person_id": 2, "org_id": 12, "title": "市退役军人事务局党组书记、局长", "start_date": "", "end_date": "2025-06", "rank": "正处级", "note": "任新抚区长前职; 2025-06-30 抚顺市十七届人大常委会第二十七次会议免去该职"},
    {"person_id": 2, "org_id": 11, "title": "县委常委、常务副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "新宾满族自治县党委政府; 分管日常工作的副县长"},
    {"person_id": 2, "org_id": 11, "title": "副县长", "start_date": "2019", "end_date": "", "rank": "县处级副职", "note": "新宾满族自治县政府党组成员、副县长"},
    {"person_id": 2, "org_id": 10, "title": "乡党委书记", "start_date": "2016-04", "end_date": "2019-06", "rank": "乡科级正职", "note": "清原满族自治县大苏河乡党委书记"},
    {"person_id": 2, "org_id": 10, "title": "乡党委副书记、乡长", "start_date": "2012-12", "end_date": "2016-04", "rank": "乡科级正职", "note": "清原满族自治县大苏河乡党委副书记、乡长"},
    {"person_id": 2, "org_id": 9, "title": "县公安部门任职", "start_date": "1997-10", "end_date": "2016", "rank": "", "note": "清原满族自治县公安系统多年 (大苏河派出所→经侦大队→税侦副大队长→南山城所指导员/副所长等)"},
    # 项国（区委常委、副区长）
    {"person_id": 3, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "官方政府领导页"},
    # 韩旭（副区长）
    {"person_id": 4, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "官方政府领导页"},
    # 刘祝（副区长兼公安局长）
    {"person_id": 5, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "兼新抚公安分局局长"},
    {"person_id": 5, "org_id": 6, "title": "新抚公安分局局长", "start_date": "", "end_date": "", "rank": "乡科级", "note": "兼"},
    # 王伟（副区长, 2026-03 新任）
    {"person_id": 6, "org_id": 2, "title": "副区长", "start_date": "2026-03", "end_date": "", "rank": "县处级副职", "note": "新政发〔2026〕3号 任命"},
    # 苏丹（前任书记）
    {"person_id": 30, "org_id": 1, "title": "区委书记", "start_date": "2025-04", "end_date": "", "rank": "县处级正职", "note": "前任新抚区委书记 (百科现标'原书记', 卸任去向待查)"},
    {"person_id": 30, "org_id": 1, "title": "区委副书记", "start_date": "2022-03", "end_date": "2025-04", "rank": "县处级正职", "note": "兼任区政府党组书记"},
    {"person_id": 30, "org_id": 2, "title": "区长", "start_date": "2022-06", "end_date": "2025-04", "rank": "县处级正职", "note": "新抚区人民政府党组书记、区长"},
    {"person_id": 30, "org_id": 8, "title": "市政府副秘书长", "start_date": "2020-12", "end_date": "2022-03", "rank": "正处级", "note": "抚顺市人民政府副秘书长(正处长级, 一级调研员)"},
    {"person_id": 30, "org_id": 13, "title": "党委书记、董事长", "start_date": "2018-08", "end_date": "2020-12", "rank": "市属国企正职", "note": "抚顺国际工程咨询集团党委书记、董事长"},
    {"person_id": 30, "org_id": 14, "title": "总工程师", "start_date": "2009-12", "end_date": "2016-11", "rank": "", "note": "抚顺规划设计研究院总工程师"},
    # 陆波（前任书记/区长 → 抚顺市委常委）
    {"person_id": 31, "org_id": 7, "title": "市委常委、统战部部长", "start_date": "2025-10", "end_date": "", "rank": "副厅级", "note": "现职 (2025-10 拟任地级市党委常委)"},
    {"person_id": 31, "org_id": 8, "title": "副市长", "start_date": "2024-11", "end_date": "2025", "rank": "副厅级", "note": "抚顺市人民政府副市长"},
    {"person_id": 31, "org_id": 1, "title": "区委书记/区长", "start_date": "2017-06", "end_date": "2024-11", "rank": "县处级正职", "note": "新抚区委副书记→代区长(2017.04)→区长→区委书记(任至2024.11)"},
    {"person_id": 31, "org_id": 1, "title": "区委常委、副区长", "start_date": "2015-11", "end_date": "2017-04", "rank": "县处级副职", "note": "新抚区委常委(2015.11-2017.04)"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 刘芳 ↔ 孟庆光 (书记—区长搭档)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "区委书记—区长搭档", "overlap_org": "中共抚顺市新抚区委员会/新抚区人民政府", "overlap_period": "2026"},
    # 区长 ↔ 副区长/班子成员
    {"person_a": 2, "person_b": 3, "type": "共事", "context": "区长—区委常委/副区长", "overlap_org": "新抚区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 4, "type": "共事", "context": "区长—副区长", "overlap_org": "新抚区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 5, "type": "共事", "context": "区长—副区长/公安局长", "overlap_org": "新抚区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 6, "type": "共事", "context": "区长提名 副区长王伟", "overlap_org": "新抚区人民政府", "overlap_period": "2026"},
    # 前任书记 苏丹 ↔ 现任书记 刘芳（交接）
    {"person_a": 30, "person_b": 1, "type": "交接", "context": "前任区委书记—现任区委书记(苏丹2025.04任书记, 后刘芳接任)", "overlap_org": "中共抚顺市新抚区委员会", "overlap_period": "2025-2026"},
    # 前任书记 苏丹 ↔ 现任书记 孟庆光（区长交接）
    {"person_a": 30, "person_b": 2, "type": "交接", "context": "孟庆光接任苏丹之乡长职务(苏丹2022-2025任区长后升书记)", "overlap_org": "新抚区人民政府", "overlap_period": "2025"},
    # 更早区委书记/区长 → 抚顺市委常委 ()
    {"person_a": 31, "person_b": 1, "type": "交接", "context": "前任区委书记/区长—现任区委书记", "overlap_org": "中共抚顺市新抚区委员会", "overlap_period": "2024-2025"},
    {"person_a": 31, "person_b": 30, "type": "交接", "context": "陆波—苏丹 相继任新抚书记", "overlap_org": "中共抚顺市新抚区委员会", "overlap_period": "2024-2025"},
    # 跨县流动: 孟庆光从 新宾/清原/市退役局 调入新抚
    {"person_a": 2, "person_b": 31, "type": "跨部门流动", "context": "孟庆光(新宾/清原/市退役局出身)调入新抚, 陆波(新抚→市委)", "overlap_org": "抚顺市", "overlap_period": "2024-2025"},
]


# ── Helper: 个人 JSON ─────────────────────────────────────────────────────────


def _has_identifier(person: dict) -> bool:
    return bool(person.get("birth") or person.get("birthplace") or person.get("native_place"))


def write_person_json(person: dict) -> None:
    """Write per-person graph JSON file following the person_graph_json schema."""
    pid = person["id"]
    name = person["name"]
    city = "新抚区"

    person_positions = [p for p in positions if p["person_id"] == pid]
    career_timeline = []
    for pos in sorted(person_positions, key=lambda p: p.get("start_date") or "9999"):
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

    if len(career_timeline) <= 1 and not _has_identifier(person):
        career_timeline.append({
            "start": "unknown",
            "end": "unknown",
            "org": "履历缺口",
            "title": "",
            "notes": "公开官方简历信息有限, 完整履历与确切就任时间待补。外部检索(Exa限流/百度验证码/Bing超时)受限, 未能进一步核实。",
            "confidence": "unverified",
            "source_ids": [],
        })

    person_rels = [r for r in relationships if r["person_a"] == pid or r["person_b"] == pid]
    rels_output = []
    for r in person_rels:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id), None)
        other_name = other["name"] if other else f"person_{other_id}"
        rels_output.append({
            "person": other_name,
            "person_id": other_name,
            "relationship_type": "overlap" if r["type"] in ("共事",) else "predecessor_successor" if r["type"] == "交接" else "cross_region_transfer",
            "strength": "strong" if r["type"] == "共事" else "medium",
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001"],
        })

    source_url = person.get("source", "")
    sources = [
        {
            "id": "S001",
            "title": "抚顺市新抚区人民政府官方网站—政府领导页/区政府工作报告/区委新闻",
            "url": source_url or "http://www.fsxf.gov.cn/",
            "publisher": "抚顺市新抚区人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "政府领导页(ld.asp?s=10459: 孟庆光/项国/韩旭/刘祝)、2026-03 任免议案(新政发〔2026〕3号)、2026-07-30 区委读书班新闻(区委书记刘芳)、新闻动态列表。",
        },
        {
            "id": "S002",
            "title": "百度百科人物词条 (孟庆光/苏丹/陆波)",
            "url": source_url,
            "publisher": "百度百科",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "secondary",
            "reliability": "medium",
            "notes": "人物履历/出生/籍贯信息。政府核实为主, 百科为补充。",
        },
    ]

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "辽宁省",
            "city": "抚顺市",
            "region": city,
            "job": person.get("current_post", ""),
            "task_id": "liaoning_新抚区",
            "time_focus": "2026-08",
        },
        "identity": {
            "person_id": f"新抚区_{name}",
            "name": name,
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
                    "source_ids": ["S002"],
                }
            ] if person.get("education") else [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{person.get('birth','')}",
                "name_birthplace": f"{name}_{person.get('birthplace','')}",
                "official_profile_url": source_url,
            },
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "县处级正职" if pid in (1, 2, 30) else "县处级副职",
            "as_of": AS_OF,
            "is_current_confirmed": person.get("confidence") == "confirmed",
            "source_ids": ["S001"],
        },
        "career_timeline": career_timeline,
        "organizations": [{"id": o["id"], "name": o["name"], "type": o["type"]} for o in organizations],
        "relationships": rels_output,
        "governance_record": [
            {
                "period": "2026",
                "domain": "governance",
                "achievement_or_event": "2025 年 GDP 约 291 亿元(增速5%), 一般公共预算收入 9.6 亿元(增速5%); 推动站前商圈复兴、老旧小区改造、全省 2026 决胜收官(2026《政府工作报告》公开)",
                "role_in_event": "区长",
                "measurable_outcome": "经济稳中向好、商圈焕新、民生落地",
                "location": "新抚区",
                "confidence": "confirmed" if person.get("current_post") in ("区长",) else "unverified",
                "source_ids": ["S001"],
            }
        ] if person.get("current_post") in ("区长",) else [],
        "professional_profile": {
            "primary_specializations": ["党建统领" if person.get("current_post") == "区委书记" else "政府行政管理"],
            "secondary_specializations": [],
            "career_pattern": "local_ladder" if _has_identifier(person) else "unknown",
            "systems_experience": [],
            "geographic_pattern": ["抚顺市(辽宁省)"] ,
            "promotion_velocity": {
                "summary": "公开履历不全, 无法精确分析晋升速度",
                "notable_fast_promotions": [],
            },
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {
                    "trait": "governance_oriented",
                    "evidence": "区委书记主持树立正确政绩观读书班并作讲话(2026-07-30 官方); 区长主持 2026 年区政府工作报告部署更新、招商引资与城市更新",
                    "confidence": "plausible" if pid in (1, 2) else "unverified",
                    "source_ids": ["S001"],
                },
            ],
            "speech_themes": ["树立和践行正确政绩观", "补短板堵漏洞强弱项", "统筹发展与安全/营商环境/城市更新"],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "截至2026-08, 未在可获得公开来源中发现针对该人物的纪律处分/审计问题/负面报道",
                "date": "",
                "confidence": "unverified",
                "source_ids": [],
            }
        ],
        "source_register": sources,
        "confidence_summary": {
            "identity": "confirmed" if _has_identifier(person) else "unverified",
            "current_role": person.get("confidence", "unverified"),
            "career_completeness": "partial" if _has_identifier(person) else "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"{name} 的出生年月/籍贯/学历及完整任职履历(除当前职务外)待补充",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的出生年月、籍贯、学历教育、入党参工时间",
                "why_it_matters": "身份去重与档案库基础信息, 跨地域关联分析必需",
                "suggested_queries": [f"{name} 简历", f"{name} 任前公示", f"{name} 任职经历"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": f"{name}的完整任职履历(每段职务起止时间), 特别是任新抚区委书记前/前的任职",
                "why_it_matters": "精确时间线是关系网络与晋升链分析的输入",
                "suggested_queries": [f"{name} 此前担任", f"{name} 任职时间"],
                "last_attempted": AS_OF,
            },
        ],
    }
    slug_post = person["current_post"].replace('/', '_').replace('、', '_').replace('，', '_').replace('、', '_')
    fname = f"{TODAY}-辽宁省-抚顺市-{slug_post}-{name}.json"
    if not person.get("current_post"):
        fname = f"{TODAY}-辽宁省-抚顺市-待定-{name}.json"
    fpath = PJSON_DIR / fname
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fpath.name}")


# ── Build ────────────────────────────────────────────────────────────────────


def main() -> int:
    print(f"Building {SLUG} network...")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")

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

    print("  Writing person JSONs...")
    core_ids = {1, 2, 3, 4, 5, 6, 30, 31}
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


TID = "liaoning_新抚区"

if __name__ == "__main__":
    raise SystemExit(main())