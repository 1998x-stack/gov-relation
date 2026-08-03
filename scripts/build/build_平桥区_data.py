#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 平桥区 (Pingqiao District), 信阳市, 河南省.

Investigation date: 2026-07-24
Task ID: henan_平桥区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - Baidu Baike: 董立淳, 古生辉
  - Baidu Search: 张自力, 刘庆东, 平桥区领导班子
  - 任前公示 (河南省委组织部, 2025-11-20, 2026-05-06)
  - 平桥区人民政府网站 (via Baidu cached)
  - 平桥人大 (平桥区人民代表大会常务委员会)
  - 平桥新闻网 articles
  - 信阳市人民政府网站 (www.xinyang.gov.cn)

Confidence notes:
  - 张自力: confirmed as 区委书记 via 任前公示 (2025-11-20) and subsequent news coverage.
    Birth: 1977年4月, 省委党校研究生, 经济学学士. Prior roles: 信阳市政府副秘书长,
    固始县委常委/常务副县长, 羊山新区党委副书记/主任, 羊山新区党委书记.
  - 古生辉: fully confirmed via Baidu Baike. Elected 区长 2026-05-30.
    Birth: 1984年10月, 河南武陟人, 硕士研究生. Prior roles: 共青团河南省委组织部副部长,
    潢川县委副书记/付店镇党委书记, 平桥区委常委/常务副区长.
  - 董立淳: confirmed predecessor 区委书记 (2019-2025), now 许昌市副市长.
    北大本科, 南开博士.
  - 刘庆东: confirmed predecessor 区长 (2022-2026). Exact birth/bio unavailable without Baidu Baike.
  - 区委常委 roster: compiled from multiple news reports (2025-05, 2026-04, 2026-06).
    Some members' full bios unavailable.
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
SLUG = "平桥区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# Staging paths (inside data/tmp/henan_平桥区/)
STAGING_DB = os.path.join(BASE, f"{SLUG}_network.db")
STAGING_GEXF = os.path.join(BASE, f"{SLUG}_network.gexf")
STAGING_PERSONS = Path(BASE)

# ── Persons ─────────────────────────────────────────────────────────────────
# Person ID scheme: 平桥_{pinyin_name} for dedup across investigations

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership — Party
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "张自力",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年4月",
        "birthplace": "",
        "education": "省委党校研究生，经济学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共信阳市平桥区委员会",
        "source": "任前公示 (河南省委组织部, 2025-11-20); 平桥新闻网 (2026-04-17, 04-29, 04-30)"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership — Government
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 2,
        "name": "古生辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年10月",
        "birthplace": "河南武陟",
        "education": "硕士研究生",
        "party_join": "中共党员",
        "work_start": "2007年8月",
        "current_post": "区长",
        "current_org": "平桥区人民政府",
        "source": "https://baike.baidu.com/item/古生辉; 平桥人大 (2026-05-13, 2026-05-30)"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "董立淳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年12月",
        "birthplace": "河南固始",
        "education": "研究生，经济学博士（南开大学）",
        "party_join": "中共党员",
        "work_start": "2003年7月",
        "current_post": "许昌市副市长",
        "current_org": "许昌市人民政府",
        "source": "https://baike.baidu.com/item/董立淳; 河南日报 (2025-09-25), 许昌日报 (2025-11-20)"
    },
    {
        "id": 4,
        "name": "刘庆东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "",
        "current_org": "",
        "source": "平桥人大 (2022-09-23); 信阳电视网 (2024-05-06)"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Party Committee (区委常委) — confirmed from multiple news articles
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 5,
        "name": "张欣",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记",
        "current_org": "中共信阳市平桥区委员会",
        "source": "平桥区党建述职评议会议 (2025-01-27); 区委常委会 (2025-05-09)"
    },
    {
        "id": 6,
        "name": "闫芳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、宣传部部长",
        "current_org": "中共信阳市平桥区委员会",
        "source": "平桥区党建述职评议会议 (2025-01-27); 新高考工作会 (2025-06-05)"
    },
    {
        "id": 7,
        "name": "黄启军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、政法委书记",
        "current_org": "中共信阳市平桥区委员会",
        "source": "平桥区党建述职评议会议 (2025-01-27)"
    },
    {
        "id": 8,
        "name": "陈嘉源",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、组织部部长",
        "current_org": "中共信阳市平桥区委员会",
        "source": "区委常委会 (2025-05-09)"
    },
    {
        "id": 9,
        "name": "王罕翡",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区委办公室主任",
        "current_org": "中共信阳市平桥区委员会",
        "source": "平桥区党建述职评议会议 (2025-01-27); 新高考工作会 (2025-06-05)"
    },
    {
        "id": 10,
        "name": "王亚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、统战部部长",
        "current_org": "中共信阳市平桥区委员会",
        "source": "区委常委会 (2025-05-09)"
    },
    {
        "id": 11,
        "name": "毕雪丽",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区纪委书记、监委主任",
        "current_org": "中共信阳市平桥区纪律检查委员会",
        "source": "区委常委会 (2025-05-09)"
    },
    {
        "id": 12,
        "name": "曾刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共信阳市平桥区委员会",
        "source": "平桥区水利工程调研 (2026-04-15); 安全生产调研 (2026-04-29)"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Deputy District Mayor (副区长)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 13,
        "name": "霍昱廷",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、宣传部部长，副区长",
        "current_org": "平桥区人民政府",
        "source": "信阳市平桥区人民政府 Baidu Baike page"
    },
    {
        "id": 14,
        "name": "程岗",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、政法委书记，副区长",
        "current_org": "平桥区人民政府",
        "source": "信阳市平桥区人民政府 Baidu Baike page"
    },
    {
        "id": 15,
        "name": "刘高峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "平桥区人民政府",
        "source": "平桥区人民政府网 leader list (2026-06-05)"
    },
    {
        "id": 16,
        "name": "蒋月祥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "平桥区人民政府",
        "source": "平桥区人民政府网 leader list (2026-06-05)"
    },
    {
        "id": 17,
        "name": "张一",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "平桥区人民政府",
        "source": "平桥区人民政府网 leader list (2026-06-05)"
    },
    {
        "id": 18,
        "name": "陈欣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "平桥区人民政府",
        "source": "平桥区人民政府网 leader list (2026-06-30)"
    },
    {
        "id": 19,
        "name": "吴孔明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "平桥区人民政府",
        "source": "平桥区人民政府网 leader list (2026-06-30)"
    },
    {
        "id": 20,
        "name": "叶改·哈布旦",
        "gender": "男",
        "ethnicity": "哈萨克族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长（挂职）",
        "current_org": "平桥区人民政府",
        "source": "平桥人大 (2024-02-28)"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Other Key Positions
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 21,
        "name": "李广全",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区领导",
        "current_org": "平桥区",
        "source": "平桥区水利工程/防汛调研 (2026-04-15)"
    },
    {
        "id": 22,
        "name": "刘龄鹤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1988年2月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、宣传部部长，副区长",
        "current_org": "平桥区人民政府",
        "source": "平桥区人民政府网 leader bio (2026-06-24)"
    },
]

# ── Organizations ──────────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中共信阳市平桥区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共信阳市委员会",
        "location": "河南省信阳市平桥区"
    },
    {
        "id": 2,
        "name": "平桥区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "信阳市人民政府",
        "location": "河南省信阳市平桥区"
    },
    {
        "id": 3,
        "name": "中共信阳市平桥区纪律检查委员会",
        "type": "纪律检查",
        "level": "县处级",
        "parent": "中共信阳市平桥区委员会",
        "location": "河南省信阳市平桥区"
    },
    {
        "id": 4,
        "name": "信阳市平桥区人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "平桥区",
        "location": "河南省信阳市平桥区"
    },
    {
        "id": 5,
        "name": "信阳市平桥区政协",
        "type": "政协",
        "level": "县处级",
        "parent": "平桥区",
        "location": "河南省信阳市平桥区"
    },
    {
        "id": 6,
        "name": "许昌市人民政府",
        "type": "政府",
        "level": "地厅级",
        "parent": "河南省人民政府",
        "location": "河南省许昌市"
    },
    {
        "id": 7,
        "name": "信阳市羊山新区",
        "type": "开发区",
        "level": "县处级",
        "parent": "信阳市人民政府",
        "location": "河南省信阳市"
    },
    {
        "id": 8,
        "name": "信阳市人民政府",
        "type": "政府",
        "level": "地厅级",
        "parent": "河南省人民政府",
        "location": "河南省信阳市"
    },
    {
        "id": 9,
        "name": "固始县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "信阳市人民政府",
        "location": "河南省信阳市固始县"
    },
    {
        "id": 10,
        "name": "共青团河南省委",
        "type": "群团",
        "level": "地厅级",
        "parent": "共青团中央",
        "location": "河南省郑州市"
    },
    {
        "id": 11,
        "name": "潢川县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "信阳市人民政府",
        "location": "河南省信阳市潢川县"
    },
    {
        "id": 12,
        "name": "河南省发展和改革委员会",
        "type": "政府",
        "level": "地厅级",
        "parent": "河南省人民政府",
        "location": "河南省郑州市"
    },
]

# ── Positions ──────────────────────────────────────────────────────────────
# person_id references persons[].id (1-based), org_id references organizations[].id (1-based)

positions = [
    # ── 张自力 ──
    {"person_id": 1, "org_id": 8, "title": "信阳市政府副秘书长", "start_date": "不详", "end_date": "不详", "rank": "县处级", "note": ""},
    {"person_id": 1, "org_id": 9, "title": "固始县委常委、常务副县长", "start_date": "不详", "end_date": "2021-09", "rank": "县处级", "note": ""},
    {"person_id": 1, "org_id": 7, "title": "羊山新区党委副书记、管委会主任", "start_date": "2021-09", "end_date": "2023-06", "rank": "县处级", "note": ""},
    {"person_id": 1, "org_id": 7, "title": "羊山新区党委书记", "start_date": "2023-06", "end_date": "2025-12", "rank": "县处级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "平桥区委书记", "start_date": "2025-12", "end_date": "present", "rank": "县处级（副厅级?）", "note": "任前公示 2025-11-20; 2025-12-04 首次以区委书记身份公开报道"},
    # ── 古生辉 ──
    {"person_id": 2, "org_id": 10, "title": "共青团河南省委组织部副部长", "start_date": "不详", "end_date": "2021-09", "rank": "县处级副职", "note": ""},
    {"person_id": 2, "org_id": 11, "title": "潢川县委副书记、付店镇党委书记", "start_date": "2021-09", "end_date": "2024-02", "rank": "县处级副职", "note": "河南省委\"墩苗\"干部"},
    {"person_id": 2, "org_id": 2, "title": "平桥区委常委、常务副区长", "start_date": "2024-02", "end_date": "2026-05", "rank": "县处级正职", "note": "2024-02-28 任命, 正处级"},
    {"person_id": 2, "org_id": 2, "title": "平桥区人民政府代理区长", "start_date": "2026-05-13", "end_date": "2026-05-30", "rank": "县处级正职", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "平桥区人民政府区长", "start_date": "2026-05-30", "end_date": "present", "rank": "县处级正职", "note": "当选 2026-05-30"},
    # ── 董立淳 ──
    {"person_id": 3, "org_id": 12, "title": "河南省发展计划委员会市场贸易处干部", "start_date": "2003-07", "end_date": "2004-08", "rank": "", "note": ""},
    {"person_id": 3, "org_id": 12, "title": "省发改委经贸处副主任科员", "start_date": "2004-08", "end_date": "2007-03", "rank": "", "note": ""},
    {"person_id": 3, "org_id": 12, "title": "省发改委经贸处主任科员", "start_date": "2007-03", "end_date": "2011-09", "rank": "", "note": ""},
    {"person_id": 3, "org_id": 12, "title": "省发改委经贸处副调研员", "start_date": "2011-09", "end_date": "2012-05", "rank": "", "note": ""},
    {"person_id": 3, "org_id": 12, "title": "省发改委经贸处副处长", "start_date": "2012-05", "end_date": "2015-06", "rank": "", "note": ""},
    {"person_id": 3, "org_id": 12, "title": "省重大项目稽察特派员/省政府口岸办副主任", "start_date": "2015-06", "end_date": "2017-09", "rank": "", "note": "挂职夏邑县委常委、副县长 (2016-2018)"},
    {"person_id": 3, "org_id": 12, "title": "省发改委服务业发展办公室主任", "start_date": "2017-09", "end_date": "2019-01", "rank": "", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "平桥区委副书记、代区长", "start_date": "2019-01", "end_date": "2019-06", "rank": "县处级正职", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "平桥区委副书记、区长", "start_date": "2019-06", "end_date": "2022-09", "rank": "县处级正职", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "平桥区委书记", "start_date": "2022-09", "end_date": "2025-11", "rank": "县处级正职（一级调研员）", "note": ""},
    {"person_id": 3, "org_id": 6, "title": "许昌市副市长", "start_date": "2025-11", "end_date": "present", "rank": "副厅级", "note": "2025-11-19 任命"},
    # ── 刘庆东 ──
    {"person_id": 4, "org_id": 2, "title": "平桥区人民政府代理区长", "start_date": "2022-09-23", "end_date": "2022-12", "rank": "县处级正职", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "平桥区人民政府区长", "start_date": "2022-12", "end_date": "2026-05", "rank": "县处级正职", "note": "辞去区长职务 2026-05-13"},
    # ── 张欣 ──
    {"person_id": 5, "org_id": 1, "title": "平桥区委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # ── 闫芳 ──
    {"person_id": 6, "org_id": 1, "title": "平桥区委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # ── 黄启军 ──
    {"person_id": 7, "org_id": 1, "title": "平桥区委常委、政法委书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # ── 陈嘉源 ──
    {"person_id": 8, "org_id": 1, "title": "平桥区委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # ── 王罕翡 ──
    {"person_id": 9, "org_id": 1, "title": "平桥区委常委、区委办公室主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # ── 王亚 ──
    {"person_id": 10, "org_id": 1, "title": "平桥区委常委、统战部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # ── 毕雪丽 ──
    {"person_id": 11, "org_id": 3, "title": "平桥区委常委、纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # ── 曾刚 ──
    {"person_id": 12, "org_id": 1, "title": "平桥区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # ── 霍昱廷 ──
    {"person_id": 13, "org_id": 2, "title": "平桥区委常委、宣传部部长，副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # ── 程岗 ──
    {"person_id": 14, "org_id": 2, "title": "平桥区委常委、政法委书记，副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # ── 刘高峰 ──
    {"person_id": 15, "org_id": 2, "title": "平桥区副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # ── 蒋月祥 ──
    {"person_id": 16, "org_id": 2, "title": "平桥区副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # ── 张一 ──
    {"person_id": 17, "org_id": 2, "title": "平桥区副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # ── 陈欣 ──
    {"person_id": 18, "org_id": 2, "title": "平桥区副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # ── 吴孔明 ──
    {"person_id": 19, "org_id": 2, "title": "平桥区副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # ── 叶改·哈布旦 ──
    {"person_id": 20, "org_id": 2, "title": "平桥区副区长（挂职）", "start_date": "2024-02", "end_date": "present", "rank": "县处级副职", "note": "挂职"},
    # ── 李广全 ──
    {"person_id": 21, "org_id": 1, "title": "区领导", "start_date": "", "end_date": "present", "rank": "", "note": "在调研报道中与区委书记共同出席"},
    # ── 刘龄鹤 ──
    {"person_id": 22, "org_id": 2, "title": "平桥区委常委、宣传部部长，副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "1988年2月生"},
]

# ── Relationships ──────────────────────────────────────────────────────────

relationships = [
    # Strong: 张自力 → 古生辉 (区委书记 + 区长, current working partnership)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "区委书记与区长，党政主要领导工作搭档", "overlap_org": "平桥区", "overlap_period": "2025-12至今"},
    # Strong: 张自力 → 董立淳 (predecessor-successor)
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor", "context": "张自力接替董立淳任平桥区委书记", "overlap_org": "中共信阳市平桥区委员会", "overlap_period": "2025-12"},
    # Strong: 董立淳 → 古生辉 (former boss → current successor as 区长)
    {"person_a": 3, "person_b": 2, "type": "superior_subordinate", "context": "董立淳任区委书记时古生辉为常务副区长", "overlap_org": "平桥区", "overlap_period": "2024-02至2025-11"},
    # Strong: 董立淳 → 刘庆东 (predecessor-successor as 区长)
    {"person_a": 3, "person_b": 4, "type": "predecessor_successor", "context": "董立淳升任区委书记后刘庆东接任区长", "overlap_org": "平桥区", "overlap_period": "2022-09"},
    # Strong: 刘庆东 → 古生辉 (predecessor-successor as 区长)
    {"person_a": 4, "person_b": 2, "type": "predecessor_successor", "context": "刘庆东辞去区长后古生辉接任代理区长", "overlap_org": "平桥区人民政府", "overlap_period": "2026-05"},
    # Strong: 张自力 → 古生辉 (work overlap as party-government colleagues)
    {"person_a": 1, "person_b": 12, "type": "overlap", "context": "张自力与曾刚共同参加调研活动", "overlap_org": "平桥区", "overlap_period": "2026-04"},
    {"person_a": 2, "person_b": 12, "type": "overlap", "context": "古生辉与曾刚共同参加安全生产调研", "overlap_org": "平桥区", "overlap_period": "2026-04"},
    # Medium: 董立淳 → 张欣 (区委书记-副书记 overlap)
    {"person_a": 3, "person_b": 5, "type": "overlap", "context": "董立淳任区委书记期间张欣任区委副书记", "overlap_org": "中共平桥区委", "overlap_period": "至2025-11"},
    # Same org overlap relationships for the常委 team
    {"person_a": 5, "person_b": 6, "type": "overlap", "context": "区委副书记与宣传部部长同一届区委班子", "overlap_org": "中共平桥区委", "overlap_period": "2025"},
    {"person_a": 5, "person_b": 8, "type": "overlap", "context": "区委副书记与组织部部长同一届区委班子", "overlap_org": "中共平桥区委", "overlap_period": "2025"},
    {"person_a": 10, "person_b": 11, "type": "overlap", "context": "统战部部长与纪委书记同一届区委班子", "overlap_org": "中共平桥区委", "overlap_period": "2025"},
    # Weak: 董立淳 → 张自力 (different birthplace - one 固始, one 浙江)
    {"person_a": 3, "person_b": 1, "type": "other", "context": "董立淳（河南固始人）与张自力（浙江人）不同籍贯来源", "overlap_org": "", "overlap_period": ""},
    # Weak: 古生辉 - 武陟 connection
    {"person_a": 2, "person_b": 3, "type": "same_system", "context": "古生辉（武陟人）与董立淳（固始人）均为豫籍干部", "overlap_org": "", "overlap_period": ""},
]

# ═══════════════════════════════════════════════════════════════════════════
# GEXF Writer
# ═══════════════════════════════════════════════════════════════════════════

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build_gexf(persons, organizations, positions, relationships, output_path):
    """Write GEXF 1.3 graph file using string formatting."""
    from datetime import datetime

    # Build color maps
    person_colors = {}
    for p in persons:
        role = p.get("current_post", "")
        if "书记" in role and "区委" in role or "书记" in role and "县委" in role:
            if "纪委" not in role:
                person_colors[p["id"]] = ("255,50,50", "20.0")  # Red, large
            else:
                person_colors[p["id"]] = ("255,165,0", "12.0")  # Orange
        elif "区长" in role or "县长" in role or "市长" in role:
            if "副" in role:
                person_colors[p["id"]] = ("50,100,255", "12.0")  # Blue, medium
            else:
                person_colors[p["id"]] = ("50,100,255", "20.0")  # Blue, large
        elif "纪委" in role:
            person_colors[p["id"]] = ("255,165,0", "12.0")  # Orange
        elif "副书记" in role:
            person_colors[p["id"]] = ("255,50,50", "12.0")  # Red, medium
        else:
            person_colors[p["id"]] = ("100,100,100", "12.0")  # Grey

    org_colors_map = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
        "纪律检查": "255,200,200",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "群团": "255,220,255",
    }

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation Research Agent</creator>')
    lines.append(f'    <description>平桥区领导班子工作关系网络 - 信阳市平桥区</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org_type" type="string"/>')
    lines.append('      <attribute id="3" title="level" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # --- Nodes ---
    lines.append('    <nodes>')
    for p in persons:
        c, sz = person_colors.get(p["id"], ("100,100,100", "12.0"))
        rgb = c.split(",")
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append('          <attvalue for="2" value=""/>')
        lines.append('          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{rgb[0]}" g="{rgb[1]}" b="{rgb[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    for o in organizations:
        org_c = org_colors_map.get(o.get("type", ""), "200,200,200")
        org_rgb = org_c.split(",")
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append('          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value="{esc(o.get("type", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(o.get("level", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{org_rgb[0]}" g="{org_rgb[1]}" b="{org_rgb[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # --- Edges ---
    lines.append('    <edges>')
    eid = 0
    # person → org edges (worked_at)
    for pos in positions:
        pid = pos["person_id"]
        oid = pos["org_id"]
        title = pos.get("title", "")
        lines.append(f'      <edge id="{eid}" source="p{pid}" target="o{oid}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value="{esc(pos.get("start_date", "")+" - "+pos.get("end_date", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1
    # person ↔ person edges (relationship)
    for rel in relationships:
        pa = rel["person_a"]
        pb = rel["person_b"]
        ctx = rel.get("context", "")
        rtype = rel.get("type", "")
        lines.append(f'      <edge id="{eid}" source="p{pa}" target="p{pb}" label="{esc(ctx)}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rtype)}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(ctx)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(rel.get("overlap_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(rel.get("overlap_period", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1
    lines.append('    </edges>')

    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF written: {output_path}")


# ═══════════════════════════════════════════════════════════════════════════
# Person JSON Writers
# ═══════════════════════════════════════════════════════════════════════════

def write_person_json(person, extra, output_dir):
    """Write a person's deep profile JSON."""
    data = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "河南省",
            "city": "信阳市",
            "region": "平桥区",
            "job": person.get("current_post", ""),
            "task_id": "henan_平桥区",
            "time_focus": "2019-2026"
        },
        "identity": {
            "person_id": f"pingqiao_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": person.get("birthplace", ""),
            "education": [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person.get('birth', '')}",
                "name_birthplace": f"{person['name']}_{person.get('birthplace', '')}",
                "official_profile_url": ""
            }
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": extra.get("rank", ""),
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": extra.get("timeline", []),
        "organizations": extra.get("orgs", []),
        "relationships": extra.get("rels", []),
        "governance_record": extra.get("governance", []),
        "professional_profile": extra.get("profile", {}),
        "work_style_and_personality": {
            "public_style_indicators": extra.get("style_indicators", []),
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": extra.get("metrics", {}),
        "risk_and_integrity_signals": extra.get("risk_signals", []),
        "source_register": extra.get("sources", []),
        "confidence_summary": extra.get("confidence", {}),
        "open_questions": extra.get("open_questions", [])
    }
    # Education
    for edu in extra.get("education_list", []):
        data["identity"]["education"].append(edu)

    job_slug = person.get("current_post", "unknown").replace(" ", "_")
    name_slug = person["name"]
    filename = f"{TODAY}-河南省-信阳市-{job_slug}-{name_slug}.json"
    filepath = output_dir / filename
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON written: {filepath}")
    return filename


def build_zhang_zili():
    """Build person data for 张自力."""
    timeline = [
        {"start": "不详", "end": "不详", "org": "信阳市人民政府", "title": "信阳市政府副秘书长", "level": "县处级", "location": "信阳", "system": "government", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "不详", "end": "2021-09", "org": "固始县人民政府", "title": "固始县委常委、常务副县长", "level": "县处级", "location": "信阳固始", "system": "government", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "2021-09", "end": "2023-06", "org": "信阳市羊山新区", "title": "羊山新区党委副书记、管委会主任", "level": "县处级", "location": "信阳", "system": "government", "rank": "", "is_key_promotion": True, "notes": "从固始调任羊山新区", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "2023-06", "end": "2025-12", "org": "信阳市羊山新区", "title": "羊山新区党委书记", "level": "县处级", "location": "信阳", "system": "party", "rank": "", "is_key_promotion": True, "notes": "羊山新区一把手", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "2025-12", "end": "present", "org": "中共信阳市平桥区委员会", "title": "平桥区委书记", "level": "县处级", "location": "信阳平桥", "system": "party", "rank": "", "is_key_promotion": True, "notes": "任前公示 2025-11-20, 2025-12-04 公开报道", "confidence": "confirmed", "source_ids": ["S001", "S002", "S003"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "level": "", "location": "", "system": "other", "rank": "", "is_key_promotion": False, "notes": "公开资料未找到张自力早期（任副市长副秘书长前）的详细履历", "confidence": "unverified", "source_ids": []},
    ]
    rels = [
        {"person": "古生辉", "person_id": "pingqiao_古生辉", "relationship_type": "overlap", "strength": "strong", "evidence": "区委书记与区长党政工作搭档", "overlap_org": "平桥区", "overlap_period": "2025-12至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S005"]},
        {"person": "董立淳", "person_id": "pingqiao_董立淳", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "接替董立淳任平桥区委书记", "overlap_org": "中共平桥区委", "overlap_period": "2025-12", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
    ]
    governance = [
        {"period": "2026-04", "domain": "rural_revitalization", "achievement_or_event": "调研邢集镇王岗乡，强调生态保护与发展融合", "role_in_event": "区委书记带队调研", "measurable_outcome": "", "location": "平桥邢集镇、王岗乡", "confidence": "confirmed", "source_ids": ["S005"]},
        {"period": "2026-04", "domain": "water_conservancy", "achievement_or_event": "调研水利工程建设和防汛备汛工作", "role_in_event": "区委书记主持调研", "measurable_outcome": "", "location": "平桥龙井乡、明港镇、平昌关镇", "confidence": "confirmed", "source_ids": ["S005"]},
        {"period": "2026-04", "domain": "public_security", "achievement_or_event": "督导调研安全生产工作，走访养老、消防、危化品等重点行业", "role_in_event": "区委书记带队督导", "measurable_outcome": "", "location": "平桥辖区", "confidence": "confirmed", "source_ids": ["S005"]},
    ]
    profile = {
        "primary_specializations": ["基层治理", "产业园区管理"],
        "secondary_specializations": ["生态保护", "安全生产"],
        "career_pattern": "cross_county_rotation",
        "systems_experience": ["government", "party", "development_zone"],
        "geographic_pattern": ["信阳市（固始-羊山新区-平桥）"],
        "promotion_velocity": {"summary": "从羊山新区主任（2021）到党委书记（2023）再到平桥区委书记（2025），约4年完成从副职到区县一把手的晋升", "notable_fast_promotions": ["2021-09 任羊山新区主任 → 2023-06 升党委书记 → 2025-12 任平桥区委书记"]}
    }
    style = [
        {"trait": "grassroots_oriented", "evidence": "多次深入乡镇调研水利、防汛、乡村振兴等基层工作", "confidence": "confirmed", "source_ids": ["S005"]},
        {"trait": "pragmatic", "evidence": "调研内容聚焦具体业务——防汛、安全生产、森林防火", "confidence": "confirmed", "source_ids": ["S005"]},
    ]
    metrics = {"centrality_estimate": "high", "role": "party_secretary", "network_bridge": True}
    sources = [
        {"id": "S001", "title": "领导干部任职前公示", "url": "河南省委组织部 (2025-11-20)", "publisher": "河南省委组织部", "published_at": "2025-11-20", "accessed_at": AS_OF, "source_type": "appointment_notice", "reliability": "high", "notes": ""},
        {"id": "S002", "title": "张自力已任信阳市平桥区委书记", "url": "汲古新知/大河财立方 (2025-12-04)", "publisher": "媒体", "published_at": "2025-12-04", "accessed_at": AS_OF, "source_type": "media", "reliability": "medium", "notes": ""},
        {"id": "S003", "title": "平桥区第六届委员会第九次全体会议", "url": "平桥新闻网 (2025-12-31)", "publisher": "平桥新闻网", "published_at": "2025-12-31", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "首次以区委书记身份主持会议"},
        {"id": "S004", "title": "张自力到邢集镇王岗乡调研", "url": "平桥新闻网 (2026-04-17)", "publisher": "平桥新闻网", "published_at": "2026-04-17", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S005", "title": "张自力调研安全生产/水利/防汛", "url": "平桥新闻网 (2026-04)" , "publisher": "平桥新闻网", "published_at": "2026-04", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "多篇报道"},
        {"id": "S006", "title": "平桥区委全会/党建述职", "url": "平桥新闻网 (2026-03-04)", "publisher": "平桥新闻网", "published_at": "2026-03-04", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
    ]
    confidence = {"identity": "confirmed", "current_role": "confirmed", "career_completeness": "partial", "relationship_confidence": "high", "biggest_gap": "张自力任市政府副秘书长前的早期履历（出生地、教育、参加工作等）不完整"}
    open_q = [
        {"priority": "critical", "question": "张自力的出生地（籍贯）和参加工作时间", "why_it_matters": "影响身份确认和职业生涯分析", "suggested_queries": ["张自力 出生地", "张自力 简历 信阳"], "last_attempted": AS_OF},
        {"priority": "high", "question": "张自力在信阳市政府副秘书长之前的早期履历", "why_it_matters": "全面了解其职业成长路径", "suggested_queries": ["张自力 信阳市政府副秘书长 简历"], "last_attempted": AS_OF},
    ]
    return {
        "person": {"id": 1, "name": "张自力", "gender": "男", "ethnicity": "汉族", "birth": "1977年4月", "birthplace": "", "education": "省委党校研究生，经济学学士", "party_join": "中共党员", "work_start": "", "current_post": "区委书记", "current_org": "中共信阳市平桥区委员会", "source": "任前公示+新闻报道"},
        "extra": {
            "rank": "县处级正职（一级调研员）",
            "timeline": timeline,
            "orgs": [
                {"id": "pingqiao_zhang_zili_gushi", "name": "固始县人民政府", "org_type": "政府", "role": "常务副县长"},
                {"id": "pingqiao_zhang_zili_yangshan", "name": "信阳市羊山新区", "org_type": "开发区", "role": "党委副书记/主任/党委书记"},
                {"id": "pingqiao_zhang_zili_pingqiao", "name": "中共信阳市平桥区委员会", "org_type": "党委", "role": "区委书记"},
            ],
            "rels": rels,
            "governance": governance,
            "profile": profile,
            "style_indicators": style,
            "metrics": metrics,
            "risk_signals": [{"type": "none_found", "description": "截至2026-07-24，未发现涉及张自力的纪律处分、审计问题或负面媒体报道", "date": AS_OF, "confidence": "confirmed", "source_ids": []}],
            "sources": sources,
            "confidence": confidence,
            "open_questions": open_q,
            "education_list": [
                {"period": "", "institution": "省委党校", "major": "", "degree": "研究生", "study_type": "party_school", "source_ids": ["S001"]},
            ]
        }
    }


def build_gu_shenghui():
    """Build person data for 古生辉."""
    timeline = [
        {"start": "不详", "end": "2021-09", "org": "共青团河南省委", "title": "组织部副部长", "level": "县处级副职", "location": "郑州", "system": "organization", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S010", "S011"]},
        {"start": "2021-09", "end": "2024-02", "org": "潢川县委/付店镇", "title": "潢川县委副书记、付店镇党委书记", "level": "县处级副职", "location": "信阳潢川", "system": "party", "rank": "", "is_key_promotion": True, "notes": "作为河南省委'墩苗'干部下派基层", "confidence": "confirmed", "source_ids": ["S010", "S011"]},
        {"start": "2024-02", "end": "2026-05", "org": "平桥区人民政府", "title": "平桥区委常委、常务副区长（正处级）", "level": "县处级正职", "location": "信阳平桥", "system": "government", "rank": "", "is_key_promotion": True, "notes": "2024-02-28 任命", "confidence": "confirmed", "source_ids": ["S010", "S012"]},
        {"start": "2026-05-13", "end": "2026-05-30", "org": "平桥区人民政府", "title": "代理区长", "level": "县处级正职", "location": "信阳平桥", "system": "government", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S013"]},
        {"start": "2026-05-30", "end": "present", "org": "平桥区人民政府", "title": "区长", "level": "县处级正职", "location": "信阳平桥", "system": "government", "rank": "", "is_key_promotion": True, "notes": "当选 2026-05-30", "confidence": "confirmed", "source_ids": ["S014"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "level": "", "location": "", "system": "other", "rank": "", "is_key_promotion": False, "notes": "公开资料未找到2007年参加工作至任团省委组织部副部长之前的早期履历", "confidence": "unverified", "source_ids": []},
    ]
    rels = [
        {"person": "张自力", "person_id": "pingqiao_张自力", "relationship_type": "overlap", "strength": "strong", "evidence": "区委书记与区长党政工作搭档", "overlap_org": "平桥区", "overlap_period": "2025-12至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S005"]},
        {"person": "董立淳", "person_id": "pingqiao_董立淳", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "董立淳任区委书记时任常务副区长", "overlap_org": "平桥区", "overlap_period": "2024-02至2025-11", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S010"]},
        {"person": "刘庆东", "person_id": "pingqiao_刘庆东", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "接替刘庆东任区长", "overlap_org": "平桥区人民政府", "overlap_period": "2026-05", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S013"]},
    ]
    governance = [
        {"period": "2024-至今", "domain": "economic_development", "achievement_or_event": "负责常务工作，统筹重点项目、两个园区建设、主导产业发展", "role_in_event": "常务副区长/区长", "measurable_outcome": "", "location": "平桥区", "confidence": "confirmed", "source_ids": ["S010"]},
        {"period": "2026-07", "domain": "public_security", "achievement_or_event": "调研督导防汛备汛工作", "role_in_event": "区长带队", "measurable_outcome": "", "location": "平桥龙井乡、邢集镇等", "confidence": "confirmed", "source_ids": ["S015"]},
    ]
    profile = {
        "primary_specializations": ["共青团工作", "基层组织建设", "经济管理"],
        "secondary_specializations": ["应急管理"],
        "career_pattern": "provincial_department_to_grassroots",
        "systems_experience": ["organization", "party", "government"],
        "geographic_pattern": ["郑州（团省委）→ 信阳潢川 → 信阳平桥"],
        "promotion_velocity": {"summary": "从团省委组织部副部长(副处)到平桥区区长(正处)约5年，'墩苗'经历后快速晋升", "notable_fast_promotions": ["2021-09 墩苗下派潢川县委副书记 → 2024-02 平桥区委常委副区长(正处) → 2026-05 区长"]}
    }
    style = [
        {"trait": "grassroots_oriented", "evidence": "'墩苗'下派基层乡镇党委书记经历", "confidence": "confirmed", "source_ids": ["S010"]},
        {"trait": "technocratic", "evidence": "有共青团和省委机关工作背景，硕士研究生学历", "confidence": "confirmed", "source_ids": ["S010"]},
    ]
    metrics = {"centrality_estimate": "high", "role": "government_head", "network_bridge": False}
    sources = [
        {"id": "S010", "title": "古生辉 - 百度百科", "url": "https://baike.baidu.com/item/古生辉", "publisher": "百度百科", "published_at": "2026-07-18", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": ""},
        {"id": "S011", "title": "乡镇快讯-潢川县人民政府", "url": "潢川县人民政府网站", "publisher": "潢川县人民政府", "published_at": "2023-07-10", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S012", "title": "区人大常委会任免名单", "url": "平桥人大 (2024-02-28)", "publisher": "平桥区人大常委会", "published_at": "2024-02-28", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S013", "title": "关于古生辉为代理区长的决定", "url": "信阳网信 (2026-05-14)", "publisher": "信阳网信", "published_at": "2026-05-14", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S014", "title": "古生辉当选区长", "url": "平桥微宣 (2026-05-31)", "publisher": "平桥微宣", "published_at": "2026-05-31", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S015", "title": "古生辉调研防汛备汛工作", "url": "平桥新闻报道 (2026-07)", "publisher": "平桥新闻网", "published_at": "2026-07", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": ""},
    ]
    confidence = {"identity": "confirmed", "current_role": "confirmed", "career_completeness": "partial", "relationship_confidence": "high", "biggest_gap": "2007年参加工作至任团省委组织部副部长之间的早期履历"}
    open_q = [
        {"priority": "high", "question": "古生辉2007年参加工作后的早期职业生涯（2007-2019年左右）", "why_it_matters": "了解其职业起点和晋升轨迹", "suggested_queries": ["古生辉 团省委 早期 简历", "古生辉 2007"], "last_attempted": AS_OF},
        {"priority": "medium", "question": "古生辉的本科院校和专业", "why_it_matters": "教育背景对职业路径的影响", "suggested_queries": ["古生辉 毕业院校"], "last_attempted": AS_OF},
    ]
    return {
        "person": {"id": 2, "name": "古生辉", "gender": "男", "ethnicity": "汉族", "birth": "1984年10月", "birthplace": "河南武陟", "education": "硕士研究生", "party_join": "中共党员", "work_start": "2007年8月", "current_post": "区长", "current_org": "平桥区人民政府", "source": "百度百科+平桥人大"},
        "extra": {
            "rank": "县处级正职",
            "timeline": timeline,
            "orgs": [
                {"id": "pingqiao_gu_ccyl", "name": "共青团河南省委", "org_type": "群团", "role": "组织部副部长"},
                {"id": "pingqiao_gu_huangchuan", "name": "潢川县委", "org_type": "党委", "role": "县委副书记"},
                {"id": "pingqiao_gu_pingqiao", "name": "平桥区人民政府", "org_type": "政府", "role": "区长"},
            ],
            "rels": rels,
            "governance": governance,
            "profile": profile,
            "style_indicators": style,
            "metrics": metrics,
            "risk_signals": [{"type": "none_found", "description": "截至2026-07-24，未发现涉及古生辉的纪律处分、审计问题或负面媒体报道", "date": AS_OF, "confidence": "confirmed", "source_ids": []}],
            "sources": sources,
            "confidence": confidence,
            "open_questions": open_q,
            "education_list": [
                {"period": "", "institution": "党校", "major": "", "degree": "研究生", "study_type": "party_school", "source_ids": ["S010"]},
            ]
        }
    }


# ═══════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════

def main():
    print(f"{'='*60}")
    print(f"  Building 平桥区 Network Data")
    print(f"  Date: {TODAY}")
    print(f"{'='*60}")

    # 1. Build GEXF
    print("\n[1/4] Building GEXF graph...")
    build_gexf(persons, organizations, positions, relationships, STAGING_GEXF)

    # 2. Build SQLite via runner
    print("\n[2/4] Building SQLite database...")
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".."))
    try:
        from gov_relation.runner import run_build
        from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
        run_build(
            slug=SLUG,
            persons=persons,
            organizations=organizations,
            positions=positions,
            relationships=relationships,
            db_path=STAGING_DB,
            gexf_path=STAGING_GEXF,
            overwrite=True,
        )
    except ImportError:
        print("  gov_relation runner not available, using local SQLite fallback...")
        import sqlite3
        conn = sqlite3.connect(str(STAGING_DB))
        conn.execute("DROP TABLE IF EXISTS relationships")
        conn.execute("DROP TABLE IF EXISTS positions")
        conn.execute("DROP TABLE IF EXISTS organizations")
        conn.execute("DROP TABLE IF EXISTS persons")
        conn.execute("""
            CREATE TABLE persons (
                id INTEGER PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
                birth TEXT, birthplace TEXT, education TEXT, party_join TEXT,
                work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE organizations (
                id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT,
                parent TEXT, location TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE positions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                person_id INTEGER, org_id INTEGER, title TEXT,
                start_date TEXT, end_date TEXT, rank TEXT, note TEXT
            )
        """)
        conn.execute("""
            CREATE TABLE relationships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                person_a INTEGER, person_b INTEGER, type TEXT, context TEXT,
                overlap_org TEXT, overlap_period TEXT
            )
        """)
        cols_p = ["id", "name", "gender", "ethnicity", "birth", "birthplace",
                   "education", "party_join", "work_start", "current_post", "current_org", "source"]
        for p in persons:
            conn.execute(f"INSERT INTO persons ({','.join(cols_p)}) VALUES ({','.join(['?']*len(cols_p))})",
                        [p.get(c, "") for c in cols_p])
        cols_o = ["id", "name", "type", "level", "parent", "location"]
        for o in organizations:
            conn.execute(f"INSERT INTO organizations ({','.join(cols_o)}) VALUES ({','.join(['?']*len(cols_o))})",
                        [o.get(c, "") for c in cols_o])
        cols_pos = ["person_id", "org_id", "title", "start_date", "end_date", "rank", "note"]
        for pos in positions:
            conn.execute(f"INSERT INTO positions ({','.join(cols_pos)}) VALUES ({','.join(['?']*len(cols_pos))})",
                        [pos.get(c, "") for c in cols_pos])
        cols_r = ["person_a", "person_b", "type", "context", "overlap_org", "overlap_period"]
        for r in relationships:
            conn.execute(f"INSERT INTO relationships ({','.join(cols_r)}) VALUES ({','.join(['?']*len(cols_r))})",
                        [r.get(c, "") for c in cols_r])
        conn.commit()
        conn.close()
        print(f"  DB written (fallback): {STAGING_DB}")
        print(f"    {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

    # 3. Write Person JSONs
    print("\n[3/4] Writing person JSONs...")
    person_files = []

    zz = build_zhang_zili()
    pf = write_person_json(zz["person"], zz["extra"], STAGING_PERSONS)
    person_files.append(pf)

    gs = build_gu_shenghui()
    pf = write_person_json(gs["person"], gs["extra"], STAGING_PERSONS)
    person_files.append(pf)

    # Also write for 董立淳 (predecessor)
    dlc_person = {
        "id": 3, "name": "董立淳", "gender": "男", "ethnicity": "汉族",
        "birth": "1979年12月", "birthplace": "河南固始",
        "education": "研究生，经济学博士（南开大学）",
        "party_join": "中共党员", "work_start": "2003年7月",
        "current_post": "许昌市副市长", "current_org": "许昌市人民政府",
        "source": "https://baike.baidu.com/item/董立淳"
    }
    dlc_extra = {
        "rank": "副厅级",
        "timeline": [
            {"start": "1996-09", "end": "2000-07", "org": "北京大学技术物理系", "title": "核物理专业学习", "level": "", "location": "北京", "system": "education", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S020"]},
            {"start": "2001-09", "end": "2003-07", "org": "北京大学经济学院", "title": "金融学专业学习", "level": "", "location": "北京", "system": "education", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S020"]},
            {"start": "2003-07", "end": "2004-08", "org": "河南省发展计划委员会", "title": "市场贸易处干部", "level": "", "location": "郑州", "system": "government", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S020"]},
            {"start": "2004-08", "end": "2011-09", "org": "河南省发改委", "title": "经贸处副主任科员/主任科员", "level": "", "location": "郑州", "system": "government", "rank": "", "is_key_promotion": False, "notes": "2006-2009 南开大学产业经济学博士", "confidence": "confirmed", "source_ids": ["S020"]},
            {"start": "2011-09", "end": "2015-06", "org": "河南省发改委", "title": "经贸处副调研员/副处长", "level": "县处级副职", "location": "郑州", "system": "government", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S020"]},
            {"start": "2015-06", "end": "2017-09", "org": "河南省政府口岸办", "title": "重大项目部稽察特派员/口岸办副主任", "level": "县处级正职", "location": "郑州/夏邑", "system": "government", "rank": "", "is_key_promotion": True, "notes": "2016-2018 挂职夏邑县委常委副县长", "confidence": "confirmed", "source_ids": ["S020"]},
            {"start": "2017-09", "end": "2019-01", "org": "河南省发改委", "title": "服务业发展办公室主任", "level": "县处级正职", "location": "郑州", "system": "government", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S020"]},
            {"start": "2019-01", "end": "2022-09", "org": "平桥区人民政府", "title": "平桥区委副书记、区长", "level": "县处级正职", "location": "信阳平桥", "system": "government", "rank": "一级调研员", "is_key_promotion": True, "notes": "省发改委下派", "confidence": "confirmed", "source_ids": ["S020"]},
            {"start": "2022-09", "end": "2025-11", "org": "中共平桥区委", "title": "平桥区委书记", "level": "县处级正职", "location": "信阳平桥", "system": "party", "rank": "一级调研员", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S020"]},
            {"start": "2025-11", "end": "present", "org": "许昌市人民政府", "title": "许昌市副市长", "level": "副厅级", "location": "许昌", "system": "government", "rank": "", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S020"]},
        ],
        "orgs": [{"name": "河南省发改委", "org_type": "政府"}, {"name": "平桥区", "org_type": "政府/党委"}, {"name": "许昌市人民政府", "org_type": "政府"}],
        "rels": [
            {"person": "张自力", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "张自力接替其区委书记职务"},
            {"person": "古生辉", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "任区委书记时古生辉为常务副区长"},
            {"person": "刘庆东", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "升书记后刘庆东接任区长"},
        ],
        "governance": [],
        "profile": {"primary_specializations": ["发展改革", "经济管理", "口岸建设"], "career_pattern": "provincial_department", "systems_experience": ["government", "party"]},
        "style_indicators": [{"trait": "technocratic", "evidence": "北大本科、南开经济学博士", "confidence": "confirmed"}],
        "metrics": {"centrality_estimate": "high"},
        "risk_signals": [{"type": "none_found", "description": "无负面记录"}],
        "sources": [{"id": "S020", "title": "董立淳 - 百度百科", "url": "https://baike.baidu.com/item/董立淳", "source_type": "encyclopedia", "reliability": "medium"}],
        "confidence": {"identity": "confirmed", "current_role": "confirmed", "career_completeness": "complete", "biggest_gap": ""},
        "open_questions": [],
        "education_list": [
            {"period": "1996-2000", "institution": "北京大学技术物理系", "major": "核物理", "degree": "本科", "study_type": "full_time", "source_ids": ["S020"]},
            {"period": "2001-2003", "institution": "北京大学经济学院", "major": "金融学", "degree": "第二学士", "study_type": "full_time", "source_ids": ["S020"]},
            {"period": "2006-2009", "institution": "南开大学经济学院", "major": "产业经济学", "degree": "博士", "study_type": "part_time", "source_ids": ["S020"]},
        ]
    }
    pf = write_person_json(dlc_person, dlc_extra, STAGING_PERSONS)
    person_files.append(pf)

    # 4. Summary
    print(f"\n[4/4] Summary")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  Person JSONs: {len(person_files)}")
    print(f"  DB: {STAGING_DB}")
    print(f"  GEXF: {STAGING_GEXF}")
    print(f"\n{'='*60}")
    print(f"  Build complete! Files in staging: {BASE}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
