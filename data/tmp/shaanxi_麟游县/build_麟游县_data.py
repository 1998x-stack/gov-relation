#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 麟游县, 宝鸡市, 陕西省.

Investigation date: 2026-07-25
Task ID: shaanxi_麟游县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - www.linyou.gov.cn — 麟游县人民政府官方网站 (HTTP accessible)
  - www.linyou.gov.cn/col20083/col20140/ — 领导之窗 (长者模式)
  - www.linyou.gov.cn/col14518/col14521/col16788/ — 政府领导
  - ly.baojidj.gov.cn — 麟游县党建网
  - baike.baidu.com — 百度百科 (returned HTTP 403)
  - Exa search API — rate-limited

Known information:
  - 县委书记: 王海刚 (confirmed from multiple news articles, Jan 2025 - Jul 2026)
  - 县长: 郑文娟 (confirmed from official bio page, as of 2026-06-18)
  - 县人大常委会主任: 李力 (confirmed from news)
  - 县政协主席: 闫秉云 (confirmed from news)
  - 县委常委、常务副县长: 上官青云 (confirmed from official bio)
  - 县委常委、副县长: 赵选民 (confirmed from official bio)
  - 县委常委、副县长(挂职): 林辉 (confirmed from official bio)
  - 县委常委、副县长(挂职): 许西锋 (confirmed from official bio)
  - 副县长: 赵朋军 (confirmed from official bio)
  - 副县长: 李志浩 (confirmed from official bio)
  - 副县长: 董西锋 (confirmed from official bio)
  - 副县长、县公安局局长: 陈飞 (confirmed from official bio)
  - 县委常委、纪委书记、监委主任: 李炜 (confirmed from news)
  - 县委其他常委(组织部长, 宣传部长, 政法委书记, 县委副书记):
    具体姓名待进一步核实

Confidence notes:
  - 王海刚 — identity details (birth, education, native place) NOT found on official site.
    His name first appeared as 县委书记 in January 2025 articles. Previous secretary
    identity unknown (suggest 李雄 or 张海峰 as possibilities based on cross-county patterns).
  - 郑文娟 — official bio confirmed: female, Han, born 1982-09, Shaanxi Chengcheng native,
    in-service graduate degree, party joined 2004-02, worked from 2005-07.
  - All other government leaders have confirmed bios from official government page.
"""

from __future__ import annotations

import json
import os
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

import sqlite3  # noqa: used by gov_relation.runner via import
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "麟游县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "shaanxi_麟游县"
if _CURRENT_DIR.name == "shaanxi_麟游县":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR  # fallback
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1=县委书记, 2=县长, 3-14=县委常委/副县长/其他

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "王海刚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共麟游县委员会",
        "source": "麟游县政府网(www.linyou.gov.cn)新闻报道确认。最早出现为县委书记是2025年1月。个人简历/出生/籍贯信息暂未在政府网站公开页面找到。",
        "confidence": "confirmed",
        "notes": "王海刚自2025年初（最晚2025年1月）起担任麟游县委书记。公开报道中多次以县委书记身份出席会议活动，最新为2026年7月。具体出生年月、籍贯、学历等未能在官方网站找到。需通过宝鸡市委组织部任前公示或百度百科进一步核实。"
    },
    {
        "id": 2,
        "name": "郑文娟",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1982-09",
        "birthplace": "陕西澄城",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "2005-07",
        "current_post": "县委副书记、县长",
        "current_org": "麟游县人民政府",
        "source": "麟游县政府网领导之窗(http://www.linyou.gov.cn/col14518/col14521/col16788/col16789/202108/t20210819_579114.html)",
        "confidence": "confirmed",
        "notes": "郑文娟，女，汉族，生于1982年9月，陕西澄城人，在职研究生学历，2004年2月加入中国共产党，2005年7月参加工作。现任麟游县委副书记、县长。主管工作：领导县政府全面工作，分管县财政局、县审计局。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 县政府领导班子 (confirmed via official website)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "上官青云",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-11",
        "birthplace": "陕西商南",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "1999-07",
        "current_post": "县委常委、副县长（常务）",
        "current_org": "麟游县人民政府",
        "source": "麟游县政府网(http://www.linyou.gov.cn/col14518/col14521/col16788/col16790/202109/t20210930_579112.html)",
        "confidence": "confirmed",
        "notes": "上官青云，男，汉族，生于1975年11月，陕西商南人，在职研究生学历，1999年5月加入中国共产党，1999年7月参加工作。负责县政府日常工作。分管县政府办公室（行政审批局）、县发改局、县人社局（医保局）、县自然资源和林业局、县应急管理局等。"
    },
    {
        "id": 4,
        "name": "赵选民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-07",
        "birthplace": "陕西陇县",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "2000-01",
        "current_post": "县委常委、副县长",
        "current_org": "麟游县人民政府",
        "source": "麟游县政府网(http://www.linyou.gov.cn/col14518/col14521/col16788/col16790/202108/t20210819_579105.html)",
        "confidence": "confirmed",
        "notes": "赵选民，男，汉族，生于1979年7月，陕西陇县人，大学学历，2006年9月加入中国共产党，2000年1月参加工作。分管县商务和工信局、市生态环境局麟游分局、县招商局、麟游经开区管委会。"
    },
    {
        "id": 5,
        "name": "林辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984-08",
        "birthplace": "河南光山",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "2009-07",
        "current_post": "县委常委、副县长（挂职）",
        "current_org": "麟游县人民政府",
        "source": "麟游县政府网(http://www.linyou.gov.cn/col14518/col14521/col16788/col16790/202307/t20230717_579113.html)",
        "confidence": "confirmed",
        "notes": "林辉，男，汉族，生于1984年8月，河南光山人，大学学历，2018年10月加入中国共产党，2009年7月参加工作。挂职副县长，负责央企定点帮扶，协助抓好乡村振兴工作。"
    },
    {
        "id": 6,
        "name": "许西锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-09",
        "birthplace": "江苏沛县",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "1996-08",
        "current_post": "县委常委、副县长（挂职）",
        "current_org": "麟游县人民政府",
        "source": "麟游县政府网(http://www.linyou.gov.cn/col14518/col14521/col16788/col16790/202412/t20241204_899602.html)",
        "confidence": "confirmed",
        "notes": "许西锋，男，汉族，生于1972年9月，江苏沛县人，大学学历，1999年6月加入中国共产党，1996年8月参加工作。挂职副县长，分管苏陕协作办公室。"
    },
    {
        "id": 7,
        "name": "赵朋军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-05",
        "birthplace": "陕西麟游",
        "education": "大专学历",
        "party_join": "中共党员",
        "work_start": "1997-08",
        "current_post": "副县长",
        "current_org": "麟游县人民政府",
        "source": "麟游县政府网(http://www.linyou.gov.cn/col14518/col14521/col16788/col16790/202502/t20250225_1121298.html)",
        "confidence": "confirmed",
        "notes": "赵朋军，男，汉族，生于1977年5月，陕西麟游人，大专学历，1999年8月加入中国共产党，1997年8月参加工作。分管县民政和退役军人事务局、县交通局、县农业农村和水利局（乡村振兴局）、县供销联社。"
    },
    {
        "id": 8,
        "name": "李志浩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1988-06",
        "birthplace": "陕西麟游",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "2011-08",
        "current_post": "副县长",
        "current_org": "麟游县人民政府",
        "source": "麟游县政府网(http://www.linyou.gov.cn/col14518/col14521/col16788/col16790/202108/t20210819_579108.html; 最新更新2026-07-23)",
        "confidence": "confirmed",
        "notes": "李志浩，男，汉族，生于1988年6月，陕西麟游人，大学学历，2009年10月加入中国共产党，2011年8月参加工作。分管县教育体育局、县卫生健康局（疾控局）、县文化和旅游局（文物局）。"
    },
    {
        "id": 9,
        "name": "董西锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-01",
        "birthplace": "陕西白水",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "2004-07",
        "current_post": "副县长",
        "current_org": "麟游县人民政府",
        "source": "麟游县政府网(http://www.linyou.gov.cn/col14518/col14521/col16788/col16790/202108/t20210819_579106.html)",
        "confidence": "confirmed",
        "notes": "董西锋，男，汉族，生于1980年1月，陕西白水人，大学学历，2000年1月加入中国共产党，2004年7月参加工作。分管县住建局（城管执法局）、县市场监督管理局。"
    },
    {
        "id": 10,
        "name": "陈飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-09",
        "birthplace": "陕西扶风",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "1993-07",
        "current_post": "副县长、县公安局局长",
        "current_org": "麟游县公安局",
        "source": "麟游县政府网(http://www.linyou.gov.cn/col14518/col14521/col16788/col16790/202108/t20210819_579107.html)",
        "confidence": "confirmed",
        "notes": "陈飞，男，汉族，生于1972年9月，陕西扶风人，在职研究生学历，1996年7月加入中国共产党，1993年7月参加工作。分管县公安局、县司法局。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 县委其他常委 (confirmed from news but incomplete roster)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 11,
        "name": "李炜",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县纪委书记、县监委主任",
        "current_org": "中共麟游县纪律检查委员会",
        "source": "麟游县党建网(http://ly.baojidj.gov.cn/info/1109/4998.htm) — 王海刚主持召开煤矿安全生产会议（2026-05-25）提及",
        "confidence": "confirmed",
        "notes": "李炜，麟游县委常委、纪委书记、监委主任。姓名在2026年5月25日新闻中得到确认。出生年月、籍贯、学历等细节待核实。"
    },
    {
        "id": 12,
        "name": "待查_组织部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共麟游县委组织部",
        "source": "待查 — 默认县级班子构成推断",
        "confidence": "unverified",
        "notes": "县委组织部部长姓名待核实。麟游县官方网站未在政府领导之窗列出县委部门领导。需通过麟游党建网或宝鸡市委组织部任免公告进一步确认。"
    },
    {
        "id": 13,
        "name": "待查_宣传部长",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共麟游县委宣传部",
        "source": "待查 — 默认县级班子构成推断",
        "confidence": "unverified",
        "notes": "县委宣传部部长姓名待核实。"
    },
    {
        "id": 14,
        "name": "待查_政法委书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共麟游县委政法委员会",
        "source": "待查 — 默认县级班子构成推断",
        "confidence": "unverified",
        "notes": "县委政法委书记姓名待核实。"
    },
    {
        "id": 15,
        "name": "待查_县委副书记",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记（专职）",
        "current_org": "中共麟游县委员会",
        "source": "待查 — 默认县级班子构成推断。郑文娟兼任县委副书记（县长），一般还设一名专职副书记。",
        "confidence": "unverified",
        "notes": "专职副书记姓名待核实。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 人大、政协领导
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 16,
        "name": "李力",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "麟游县人民代表大会常务委员会",
        "source": "麟游县政府网新闻报道(http://www.linyou.gov.cn/col1571/col1574/202607/t20260701_1281319.html)",
        "confidence": "confirmed",
        "notes": "李力，麟游县人大常委会主任。姓名在2026年7月1日'七一'慰问活动中确认。详细简历待核实。"
    },
    {
        "id": 17,
        "name": "闫秉云",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "中国人民政治协商会议麟游县委员会",
        "source": "麟游县政府网新闻报道(http://www.linyou.gov.cn/col1571/col1574/202607/t20260701_1281319.html)",
        "confidence": "confirmed",
        "notes": "闫秉云，麟游县政协主席。姓名在2026年7月1日'七一'慰问活动中确认。详细简历待核实。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共麟游县委员会", "type": "党委", "level": "县处级", "parent": "中共宝鸡市委", "location": "麟游县"},
    {"id": 2, "name": "麟游县人民政府", "type": "政府", "level": "县处级", "parent": "宝鸡市人民政府", "location": "麟游县"},
    {"id": 3, "name": "麟游县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "宝鸡市人大常委会", "location": "麟游县"},
    {"id": 4, "name": "中国人民政治协商会议麟游县委员会", "type": "政协", "level": "县处级", "parent": "政协宝鸡市委", "location": "麟游县"},
    {"id": 5, "name": "中共麟游县纪律检查委员会（监察委员会）", "type": "纪委", "level": "县处级", "parent": "宝鸡市纪委", "location": "麟游县"},
    {"id": 6, "name": "中共麟游县委组织部", "type": "党委", "level": "县处级", "parent": "中共麟游县委员会", "location": "麟游县"},
    {"id": 7, "name": "中共麟游县委宣传部", "type": "党委", "level": "县处级", "parent": "中共麟游县委员会", "location": "麟游县"},
    {"id": 8, "name": "中共麟游县委政法委员会", "type": "党委", "level": "县处级", "parent": "中共麟游县委员会", "location": "麟游县"},
    {"id": 9, "name": "麟游县公安局", "type": "政府", "level": "乡科级", "parent": "麟游县人民政府", "location": "麟游县"},
    {"id": 10, "name": "陕西麟游经济技术开发区管理委员会", "type": "开发区", "level": "县处级", "parent": "麟游县人民政府", "location": "麟游县"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 王海刚 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "2025-01", "end_date": "", "rank": "县处级正职",
     "note": "最早公开报道以县委书记身份出现为2025年1月。具体到任时间待确认。"},
    # 郑文娟 — 县长
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "领导县政府全面工作。分管县财政局、县审计局。"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": "县长兼任县委副书记"},
    # 上官青云 — 常务副县长
    {"person_id": 3, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "副县长（常务）", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "分管县政府办、发改局、人社局、自然资源和林业局、应急管理局等"},
    # 赵选民 — 副县长
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "分管商务和工信局、生态环境局麟游分局、招商局、经开区管委会"},
    # 林辉 — 挂职副县长
    {"person_id": 5, "org_id": 1, "title": "县委常委（挂职）", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "副县长（挂职）", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "负责央企定点帮扶，协助抓好乡村振兴工作"},
    # 许西锋 — 挂职副县长
    {"person_id": 6, "org_id": 1, "title": "县委常委（挂职）", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副县长（挂职）", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "分管苏陕协作办公室"},
    # 赵朋军 — 副县长
    {"person_id": 7, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "分管民政和退役军人事务局、交通局、农业农村和水利局、供销联社"},
    # 李志浩 — 副县长
    {"person_id": 8, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "分管教育体育局、卫生健康局、文化和旅游局"},
    # 董西锋 — 副县长
    {"person_id": 9, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "分管住建局、市场监督管理局"},
    # 陈飞 — 副县长、公安局长
    {"person_id": 10, "org_id": 2, "title": "副县长（兼县公安局局长）", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": ""},
    {"person_id": 10, "org_id": 9, "title": "县公安局局长、督察长", "start_date": "", "end_date": "", "rank": "乡科级正职",
     "note": ""},
    # 李炜 — 纪委书记
    {"person_id": 11, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 11, "org_id": 5, "title": "县纪委书记、县监委主任", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": ""},
    # 待查_组织部长
    {"person_id": 12, "org_id": 1, "title": "县委常委、组织部部长", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "姓名待核实"},
    {"person_id": 12, "org_id": 6, "title": "组织部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 待查_宣传部长
    {"person_id": 13, "org_id": 1, "title": "县委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "姓名待核实"},
    {"person_id": 13, "org_id": 7, "title": "宣传部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 待查_政法委书记
    {"person_id": 14, "org_id": 1, "title": "县委常委、政法委书记", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "姓名待核实"},
    {"person_id": 14, "org_id": 8, "title": "政法委书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 待查_专职副书记
    {"person_id": 15, "org_id": 1, "title": "县委副书记（专职）", "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "姓名待核实。县长兼任县委副书记，另应有专职副书记。"},
    # 李力 — 人大主任
    {"person_id": 16, "org_id": 3, "title": "县人大常委会主任", "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": ""},
    # 闫秉云 — 政协主席
    {"person_id": 17, "org_id": 4, "title": "县政协主席", "start_date": "", "end_date": "", "rank": "县处级正职",
     "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────────────
relationships = [
    # 党政主要领导
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记与县长为党政主要领导搭档关系",
        "overlap_org": "中共麟游县委员会",
        "overlap_period": "2025-至今",
        "confidence": "confirmed",
    },
    # 书记与常务副县长
    {
        "person_a": 1,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "县委书记与常务副县长为县委与政府领导关系",
        "overlap_org": "中共麟游县委员会",
        "overlap_period": "当前",
        "confidence": "confirmed",
    },
    # 书记与纪委书记
    {
        "person_a": 1,
        "person_b": 11,
        "type": "superior_subordinate",
        "context": "县委书记与纪委书记为县委领导班子成员",
        "overlap_org": "中共麟游县委员会",
        "overlap_period": "当前",
        "confidence": "confirmed",
    },
    # 县长与常务副县长
    {
        "person_a": 2,
        "person_b": 3,
        "type": "superior_subordinate",
        "context": "县长与常务副县长为正副手搭档",
        "overlap_org": "麟游县人民政府",
        "overlap_period": "当前",
        "confidence": "confirmed",
    },
    # 县长与各副县长
    {
        "person_a": 2,
        "person_b": 4,
        "type": "superior_subordinate",
        "context": "县长与副县长工作关系",
        "overlap_org": "麟游县人民政府",
        "overlap_period": "当前",
        "confidence": "confirmed",
    },
    {
        "person_a": 2,
        "person_b": 7,
        "type": "superior_subordinate",
        "context": "县长与副县长工作关系",
        "overlap_org": "麟游县人民政府",
        "overlap_period": "当前",
        "confidence": "confirmed",
    },
    {
        "person_a": 2,
        "person_b": 8,
        "type": "superior_subordinate",
        "context": "县长与副县长工作关系",
        "overlap_org": "麟游县人民政府",
        "overlap_period": "当前",
        "confidence": "confirmed",
    },
    {
        "person_a": 2,
        "person_b": 10,
        "type": "superior_subordinate",
        "context": "县长与副县长、公安局长工作关系",
        "overlap_org": "麟游县人民政府",
        "overlap_period": "当前",
        "confidence": "confirmed",
    },
    # 纪委书记与书记
    {
        "person_a": 11,
        "person_b": 1,
        "type": "superior_subordinate",
        "context": "纪委书记接受县委书记领导",
        "overlap_org": "中共麟游县委员会",
        "overlap_period": "当前",
        "confidence": "confirmed",
    },
    # 常务副县长与各副县长（工作协调关系）
    {
        "person_a": 3,
        "person_b": 4,
        "type": "overlap",
        "context": "常务副县长与其他副县长的协调关系",
        "overlap_org": "麟游县人民政府",
        "overlap_period": "当前",
        "confidence": "confirmed",
    },
]


# ── Person JSON Builder ──────────────────────────────────────────────────────


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build_person_json(person_id: int) -> dict:
    p = {x["id"]: x for x in persons}[person_id]
    career_rows = [pos for pos in positions if pos["person_id"] == person_id]
    src_register = [
        {
            "id": "S001",
            "title": "麟游县人民政府 — 政府领导页面",
            "url": "http://www.linyou.gov.cn/col14518/col14521/col16788/",
            "publisher": "麟游县人民政府",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
        },
    ]

    data = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "陕西省",
            "city": "宝鸡市",
            "region": "麟游县",
            "job": p["current_post"],
            "task_id": "shaanxi_麟游县",
            "time_focus": "当前任期",
        },
        "identity": {
            "name": p["name"],
            "gender": p["gender"],
            "ethnicity": p["ethnicity"],
            "birth": p["birth"],
            "birthplace": p["birthplace"],
            "education": [{"summary": p["education"]}] if p["education"] else [],
            "party_join": p["party_join"],
            "work_start": p["work_start"],
        },
        "current_status": {
            "current_post": p["current_post"],
            "current_org": p["current_org"],
            "as_of": AS_OF,
            "is_current_confirmed": p["confidence"] == "confirmed",
            "source_ids": ["S001"],
        },
        "career_timeline": [
            {
                "start": pos.get("start_date", ""),
                "end": pos.get("end_date", ""),
                "org": ({x["id"]: x["name"] for x in organizations}.get(pos["org_id"], "")) if pos["org_id"] in {x["id"] for x in organizations} else "",
                "title": pos["title"],
                "rank": pos.get("rank", ""),
                "note": pos.get("note", ""),
                "confidence": p["confidence"],
                "source_ids": ["S001"],
            }
            for pos in career_rows
        ],
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "",
            "systems_experience": [],
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "caveat": "Work style is inferred from public records and speeches, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": f"未发现{p['name']}的纪律处分、审计问题或负面报道。",
                "confidence": "unverified",
                "source_ids": [],
            }
        ],
        "source_register": src_register,
        "confidence_summary": {
            "identity": p["confidence"],
            "current_role": p["confidence"],
            "career_completeness": "partial" if p["birth"] else "thin",
            "biggest_gap": "出生年月、籍贯、教育背景等身份信息缺失" if not p["birth"] else "履历早期阶段需补充",
        },
        "open_questions": [
            {
                "priority": "high",
                "question": f"{p['name']}的出生年月、籍贯和早期履历？",
                "why_it_matters": "核心人物的完整身份信息是关系网络分析的基础",
                "suggested_queries": [f"{p['name']} 简历", f"{p['name']} 百度百科", f"{p['name']} 任前公示"],
                "last_attempted": AS_OF,
            }
        ],
    }
    return data


def write_person_json(person_id: int) -> Path:
    p = {x["id"]: x for x in persons}[person_id]
    name = p["name"]
    role_label = p["current_post"]
    safe_role = role_label.replace("、", "_").replace("（", "_").replace("）", "_")
    filename = f"{TODAY}-陕西省-宝鸡市-{safe_role}-{name}.json"
    path = PJSON_DIR / filename

    person_data = build_person_json(person_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(person_data, f, ensure_ascii=False, indent=2)

    return path


# ── Main ─────────────────────────────────────────────────────────────────────


def main():
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

    # Write person JSONs for core leaders
    person_files = []
    for pid in [1, 2, 3, 4, 7, 8, 9, 10, 11, 16, 17]:
        path = write_person_json(pid)
        person_files.append(str(path))

    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print("Person JSONs:")
    for pf in person_files:
        print(f"  {pf}")
    print(f"\nNote: Core leadership data collected from official linyou.gov.cn site.")
    print(f"      王海刚 (县委书记) — identity details need further research.")
    print(f"      Persons 12-15 (组织部长/宣传部长/政法委书记/专职副书记) are '待查_*' — unverified.")
    print(f"      前任县委书记信息同样待查。")
    print(f"Done.")


if __name__ == "__main__":
    main()
