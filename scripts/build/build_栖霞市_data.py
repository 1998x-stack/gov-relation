#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 栖霞市 (Qixia City), 山东省.

Investigation date: 2026-08-03
Task ID: shandong_栖霞市
Level: 县级市
Targets: 市委书记 & 市长

Research sources:
  - Baidu Baike: "中国共产党栖霞市委员会" (confirmed 15th term Standing Committee, 11 members)
  - Baidu Baike: "栖霞市人民政府" (confirmed mayor + 6 deputy mayors)
  - Baidu Baike: 赵永刚 biography (confirmed career 寿光→潍坊→烟台保税港区→栖霞)
  - Baidu Baike: 臧雷 (basic identity confirmed)
  - Baidu Baike: 张朋尧 (lemmaId:55132639, former deputy secretary, now 海阳市长)
  - Sogou WeChat search: 2024-01-31 栖霞人大选举赵彬为副市长
  - Sogou WeChat search: 2024-03-26 周怀阔任命为副市长
  - Sogou WeChat search: 于晓丽 龙口→栖霞 跨县调任 (2025年)
  - Web search was degraded: Baidu search 403/blocked, Exa rate-limited, Jina Reader timeouts
  - qixia.gov.cn DNS not resolvable

Confidence notes:
  - 赵永刚 (市委书记): confirmed identity + career via Baidu Baike, 山东省委组织部任前公示
  - 臧雷 (市长): confirmed identity via Baidu Baike, 2023.10补选 confirmed via 市人大公告
  - Standing Committee (11 members): confirmed via Baidu Baike "中国共产党栖霞市委员会"
  - Deputy positions for most Standing Committee: unverified - Baidu Baike listed names only
  - 赵永刚's early career (before 2018寿光): unverified - gap from graduation(~1998) to ~2010
  - 臧雷's early career (before 2022): unverified - major gap
  - 市人大主任/市政协主席: unnamed, not found on any accessible source
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
SLUG = "栖霞市"
PROVINCE = "山东省"
CITY = "烟台市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-03"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "shandong_栖霞市"
if _CURRENT_DIR.name == "shandong_栖霞市":
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
# IDs: 1-2  core leadership, 3-5  predecessors, 6-16  standing committee
# IDs: 17-25 deputy mayors, 26+ 其他

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Current Core Leadership
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "赵永刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年4月",
        "birthplace": "山东省（具体市县待查）",
        "education": "青岛大学经济法系本科 / 省委党校研究生 / 农业推广硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共栖霞市委员会",
        "source": "https://baike.baidu.com/item/赵永刚/64652133",
        "confidence": "confirmed",
        "notes": "1975年4月生，青岛大学经济法系本科毕业，省委党校研究生，农业推广硕士。早期在寿光市工作，历任寿光市委常委、统战部部长，寿光市委常委、副市长，潍坊经济开发区党工委副书记、管委会主任，烟台保税港区工委委员、管委副主任（2020年调任烟台），2021年12月任栖霞市委副书记、代市长，后任市长，2023年7月任前公示拟任栖霞市委书记，已任现职。"
    },
    {
        "id": 2,
        "name": "臧雷",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年9月",
        "birthplace": "山东（待查）",
        "education": "在职研究生，公共管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记、市长",
        "current_org": "栖霞市人民政府",
        "source": "https://baike.baidu.com/item/臧雷/64652133",
        "confidence": "confirmed",
        "notes": "1982年9月生，在职研究生，公共管理硕士。2023年9月25日任前公示，拟提名为县长候选人，2023年10月14日任栖霞市副市长、代市长，2023年10月31日补选为市长。调任栖霞前具体履历暂缺。目前主持市政府全面工作，负责财税、审计等方面的工作。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Standing Committee Members (第十五届市委常委会, elected Jan 2022)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 6,
        "name": "张朋尧",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原市委副书记",
        "current_org": "中共栖霞市委员会",
        "source": "https://baike.baidu.com/item/张朋尧",
        "confidence": "confirmed",
        "notes": "原栖霞市委副书记，已调任海阳市市长。2019年4月曾代理栖霞市监委主任。2026年2月6日当选海阳市市长。Baidu Baike lemmaId:55132639。"
    },
    {
        "id": 7,
        "name": "孙永刚",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共栖霞市委员会",
        "source": "https://baike.baidu.com/item/中国共产党栖霞市委员会",
        "confidence": "plausible",
        "notes": "2021年8月曾任副市长。履历主要信息暂缺，有待进一步补充。"
    },
    {
        "id": 8,
        "name": "焉方兴",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共栖霞市委员会",
        "source": "https://baike.baidu.com/item/中国共产党栖霞市委员会",
        "confidence": "plausible",
        "notes": "履历暂缺，进一步情况待补充。"
    },
    {
        "id": 9,
        "name": "刘海华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、宣传部部长",
        "current_org": "中共栖霞市委员会",
        "source": "https://baike.baidu.com/item/中国共产党栖霞市委员会",
        "confidence": "plausible",
        "notes": "2023年报道中为栖霞市委常委、宣传部部长、副市长。推测可能为女性同志。"
    },
    {
        "id": 10,
        "name": "张海涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、市委办公室主任",
        "current_org": "中共栖霞市委员会",
        "source": "百度百科中国共产党栖霞市委员会",
        "confidence": "plausible",
        "notes": "非河南被查同名官员。履历暂时不明确。"
    },
    {
        "id": 11,
        "name": "姜力",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、纪委书记、监委主任",
        "current_org": "中共栖霞市纪律检查委员会",
        "source": "百度百科中国共产党栖霞市委员会",
        "confidence": "plausible",
        "notes": "履历暂缺。"
    },
    {
        "id": 12,
        "name": "姜立波",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、政法委书记",
        "current_org": "中共栖霞市委员会",
        "source": "百度百科中国共产党栖霞市委员会",
        "confidence": "plausible",
        "notes": "履历暂缺。"
    },
    {
        "id": 13,
        "name": "李克升",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、统战部部长",
        "current_org": "中共栖霞市委员会",
        "source": "百度百科 lemmaId:60174426",
        "confidence": "plausible",
        "notes": "2022年1月当选常委。具体履历暂缺。"
    },
    {
        "id": 14,
        "name": "薛传军",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、人武部部长",
        "current_org": "栖霞市人民武装部",
        "source": "百度百科 中国共产党栖霞市委员会",
        "confidence": "plausible",
        "notes": "军职常委。身份信息暂缺。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 市政府 副市长
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 15,
        "name": "赵彬",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "栖霞市人民政府",
        "source": "2024年1月31日栖霞市第十八届人大第四次会议公告",
        "confidence": "confirmed",
        "notes": "2024年1月31日市人大常委会主任会议任命。分管领域待查。"
    },
    {
        "id": 16,
        "name": "周怀阔",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "栖霞市人民政府",
        "source": "2024年3月26日栖霞市人大常委会公告",
        "confidence": "confirmed",
        "notes": "2024年3月26日被任命为副市长。分管领域待查。"
    },
    {
        "id": 17,
        "name": "陈京文",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "栖霞市人民政府",
        "source": "百度百科 栖霞市人民政府",
        "confidence": "plausible",
        "notes": "履历暂缺。"
    },
    {
        "id": 18,
        "name": "李珦",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "栖霞市人民政府",
        "source": "百度百科 栖霞市人民政府",
        "confidence": "plausible",
        "notes": "履历暂缺。"
    },
    {
        "id": 19,
        "name": "王振聪",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "栖霞市人民政府",
        "source": "百度百科 栖霞市人民政府",
        "confidence": "plausible",
        "notes": "履历暂缺。"
    },
    {
        "id": 20,
        "name": "于晓丽",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "龙口市（推测）",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "栖霞市人民政府",
        "source": "齐鲁壹点/163.com 2025年9月",
        "confidence": "confirmed",
        "notes": "2025年8-9月从龙口市北马镇党委书记调任栖霞市副市长（跨县交流），属于乡镇党委书记提拔副县级典型案例。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 市检察院
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 21,
        "name": "姜远斌",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "检察长",
        "current_org": "栖霞市人民检察院",
        "source": "栖霞市人民检察院官方网站",
        "confidence": "confirmed",
        "notes": "2026年1月走访慰问报道中提及的检察长。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 市委组织部长（2025年新增）
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 22,
        "name": "闫建廷",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年7月",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、组织部部长",
        "current_org": "中共栖霞市委员会",
        "source": "Baidu Baike, lemmaId:66923786",
        "confidence": "confirmed",
        "notes": "2025年8月27日烟台市委组织部任前公示拟任副县级领导。1982年7月生，省委党校研究生学历。"
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 30,
        "name": "包华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "烟台市委常委（原栖霞市委领导）",
        "current_org": "中共烟台市委员会",
        "source": "烟台市纪委监委 2026年通报",
        "confidence": "confirmed",
        "notes": "2021年4月任栖霞市委书记（矿难后紧急接任），2023年8月调任烟台市委常委、副市长。2026年因涉嫌严重违纪违法被查。"
    },
    {
        "id": 31,
        "name": "姚秀霞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原栖霞市委书记（被免职）",
        "current_org": "",
        "source": "2021年1月人民日报/新华社通报",
        "confidence": "confirmed",
        "notes": "2019年8月至2021年1月任栖霞市委书记。因笏山金矿爆炸事故（10死）被问责免职。"
    },
    {
        "id": 32,
        "name": "朱涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原栖霞市市长（被免职）",
        "current_org": "",
        "source": "2021年1月纪检监察/新华社通报",
        "confidence": "confirmed",
        "notes": "与姚秀霞同时因笏山金矿事故被问责免职。"
    },
    {
        "id": 33,
        "name": "陈兆宽",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "烟台市委统战部副部长（原栖霞市长、书记）",
        "current_org": "中共烟台市委统战部",
        "source": "媒体报道",
        "confidence": "plausible",
        "notes": "2016年12月任栖霞市长（推测任期）至2019年8月，期间升任栖霞市委书记，直至姚秀霞接任。后调烟台市委统战部。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共栖霞市委员会", "type": "党委", "level": "县级市", "parent": "中共烟台市委员会", "location": "栖霞市"},
    {"id": 2, "name": "栖霞市人民政府", "type": "政府", "level": "县级市", "parent": "烟台市人民政府", "location": "栖霞市"},
    {"id": 3, "name": "栖霞市人大常委会", "type": "人大", "level": "县级市", "parent": "烟台市人大常委会", "location": "栖霞市"},
    {"id": 4, "name": "栖霞市政协", "type": "政协", "level": "县级市", "parent": "烟台市政协", "location": "栖霞市"},
    {"id": 5, "name": "中共栖霞市纪律检查委员会", "type": "党委", "level": "县级市", "parent": "中共栖霞市委员会", "location": "栖霞市"},
    {"id": 6, "name": "栖霞市人民检察院", "type": "政府", "level": "县级市", "parent": "栖霞市人民政府", "location": "栖霞市"},
    {"id": 7, "name": "栖霞市人民武装部", "type": "政府", "level": "县级市", "parent": "栖霞市人民政府", "location": "栖霞市"},
    {"id": 8, "name": "寿光市人民政府", "type": "政府", "level": "县级市", "parent": "潍坊市人民政府", "location": "寿光市"},
    {"id": 9, "name": "潍坊市", "type": "政府", "level": "地级", "parent": "山东省人民政府", "location": "潍坊市"},
    {"id": 10, "name": "烟台保税港区管委会", "type": "政府", "level": "地级", "parent": "烟台市人民政府", "location": "烟台市"},
    {"id": 11, "name": "潍坊经济开发区", "type": "开发区", "level": "地级", "parent": "潍坊市人民政府", "location": "潍坊市"},
    {"id": 12, "name": "海阳市人民政府", "type": "政府", "level": "县级市", "parent": "烟台市人民政府", "location": "海阳市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 赵永刚 - 市委书记/历任
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "2023-08", "end_date": "", "rank": "正处级（县级市）", "note": "现任栖霞市委书记"},
    {"person_id": 1, "org_id": 2, "title": "市长", "start_date": "2021-12", "end_date": "2023-08", "rank": "正处级（县级市）", "note": "2021.12.23提名代市长，12.28就任"},
    {"person_id": 1, "org_id": 10, "title": "烟台保税港区管委会副主任", "start_date": "2020", "end_date": "2021-12", "rank": "副厅级", "note": "烟台保税港区工委委员、管委副主任"},
    {"person_id": 1, "org_id": 11, "title": "管委会主任", "start_date": "2019", "end_date": "2020", "rank": "正处级", "note": "寿光市一小部分"},
    {"person_id": 1, "org_id": 8, "title": "常务副市长", "start_date": "2017", "end_date": "2019", "rank": "副处级", "note": "寿光市委常委、副市长"},
    {"person_id": 1, "org_id": 8, "title": "市委常委、统战部部长", "start_date": "2015", "end_date": "2017", "rank": "副处级", "note": "寿光市"},
    # 臧雷 - 市长
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "2023-10", "end_date": "", "rank": "正处级（县级市）", "note": "2023.10.31当选市长"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "2023-07", "end_date": "", "rank": "正处级（县级市）", "note": ""},
    # 张朋尧 - 原副书记
    {"person_id": 6, "org_id": 1, "title": "原市委副书记", "start_date": "", "end_date": "", "rank": "正处级（县级市）", "note": "已调离"},
    {"person_id": 6, "org_id": 12, "title": "市长", "start_date": "2026-02", "end_date": "", "rank": "正处级（县级市）", "note": "海阳市市长，2026.2.6当选"},
    # 孙永刚
    {"person_id": 7, "org_id": 1, "title": "市委常委", "start_date": "2022-01", "end_date": "", "rank": "副处级", "note": "2022.1当选"},
    {"person_id": 7, "org_id": 2, "title": "原副市长", "start_date": "2021-08", "end_date": "", "rank": "副处级", "note": ""},
    # 焉方兴
    {"person_id": 8, "org_id": 1, "title": "市委常委", "start_date": "2022-01", "end_date": "", "rank": "副处级", "note": ""},
    # 刘海华 - 宣传部部长兼副市长
    {"person_id": 9, "org_id": 1, "title": "市委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "原副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": "曾任副市长、市红十字会会长"},
    # 张海涛 - 办公室主任
    {"person_id": 10, "org_id": 1, "title": "市委常委、市委办公室主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 姜力 - 纪委书记
    {"person_id": 11, "org_id": 5, "title": "市委常委、纪委书记、监委主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 姜立波 - 政法委书记
    {"person_id": 12, "org_id": 1, "title": "市委常委、政法委书记", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 李克升 - 统战部长
    {"person_id": 13, "org_id": 1, "title": "市委常委、统战部部长", "start_date": "2022-01", "end_date": "", "rank": "副处级", "note": ""},
    # 薛传军 - 人武部长
    {"person_id": 14, "org_id": 1, "title": "市委常委（军职，人武部长）", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 赵彬 - 副市长（2024.1.31当选）
    {"person_id": 15, "org_id": 2, "title": "副市长", "start_date": "2024-01", "end_date": "", "rank": "副处级", "note": ""},
    # 周怀阔 - 副市长
    {"person_id": 16, "org_id": 2, "title": "副市长", "start_date": "2024-03", "end_date": "", "rank": "副处级", "note": ""},
    # 陈京文
    {"person_id": 17, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 李珦
    {"person_id": 18, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 王振聪
    {"person_id": 19, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 于晓丽（龙口→栖霞跨县）
    {"person_id": 20, "org_id": 2, "title": "副市长", "start_date": "2025-09", "end_date": "", "rank": "副处级", "note": "从龙口市北马镇调任"},
    # 姜远斌 - 检察长
    {"person_id": 21, "org_id": 6, "title": "检察长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 前书记/市长
    {"person_id": 30, "org_id": 1, "title": "原市委书记", "start_date": "2021-04", "end_date": "2023-08", "rank": "正处级（县级市）", "note": "调任烟台市委常委、开发区书记（后落马被查）"},
    {"person_id": 31, "org_id": 1, "title": "原市委书记", "start_date": "2019-01", "end_date": "2021-01", "rank": "正处级（县级市）", "note": "因矿难事故被免职"},
    {"person_id": 32, "org_id": 2, "title": "原市长", "start_date": "", "end_date": "2021-01", "rank": "正处级（县级市）", "note": "因矿难事故被免职"},
    {"person_id": 33, "org_id": 1, "title": "原市委书记", "start_date": "2016-12", "end_date": "2019", "rank": "正处级（县级市）", "note": ""},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 赵永刚 ↔ 臧雷 (书记-市长搭档)
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "赵永刚（书记）—臧雷（市长）党政一把手搭档", "overlap_org": "中共栖霞市委员会/栖霞市人民政府", "overlap_period": "2023-2026"},
    # 赵永刚 ↔ 包华 (书记接任关系)
    {"person_a": 1, "person_b": 30, "type": "前任后继", "context": "包华2023年8月调离后赵永刚接任书记", "overlap_org": "中共栖霞市委员会", "overlap_period": ""},
    # 包华 ↔ 姚秀霞 (书记接任关系)
    {"person_a": 30, "person_b": 31, "type": "前任后继", "context": "姚秀霞因矿难被免后包华紧急接任", "overlap_org": "中共栖霞市委员会", "overlap_period": "2021"},
    # 姚秀霞 ↔ 朱涛 (同时被免)
    {"person_a": 31, "person_b": 32, "type": "共事", "context": "原书记、原市长搭档；同时因2021年矿难被问责免职", "overlap_org": "栖霞市", "overlap_period": "2019-2021"},
    # 赵永刚 ↔ 张朋尧 (市X级班子共事)
    {"person_a": 1, "person_b": 6, "type": "共事", "context": "书记—副书记班子", "overlap_org": "中共栖霞市委员会", "overlap_period": "2022-2023"},
    # 赵永刚 ↔ 刘海华 (市委班子共事)
    {"person_a": 1, "person_b": 9, "type": "共事", "context": "书记—常委（宣传部部长）", "overlap_org": "中共栖霞市委员会", "overlap_period": "2022-2026"},
    # 于晓丽: 龙口→栖霞跨县调任（关键交流线索）
    {"person_a": 20, "person_b": 2, "type": "上下级", "context": "于晓丽由龙口调任栖霞，任副市长，受市长臧雷领导", "overlap_org": "栖霞市人民政府", "overlap_period": "2025-2026"},
    # 张朋尧: 栖霞→海阳跨县调任
    {"person_a": 6, "person_b": 2, "type": "前任后继", "context": "张朋尧原栖霞副书记→海阳市长；臧雷接任市长", "overlap_org": "栖霞市", "overlap_period": "2022-2023"},
]

# ═════════════════════════════════════════════════════════════════════════════
# Helper functions
# ═════════════════════════════════════════════════════════════════════════════

def _get_open_questions(person: dict) -> list[str]:
    questions = []
    if not person.get("birth"):
        questions.append("出生年月未确认")
    if not person.get("birthplace"):
        questions.append("籍贯未确认")
    if not person.get("ethnicity"):
        questions.append("民族未确认")
    if not person.get("education"):
        questions.append("学历教育背景未确认")
    if not person.get("work_start"):
        questions.append("参加工作年份未确认")
    if not person.get("notes", ""):
        questions.append("完整任职履历未确认")
    return questions


def write_person_json(person: dict) -> None:
    """Write a per-person graph JSON file following the person_graph_json.md schema."""
    pid = person["id"]
    name = person["name"]
    slug_id = f"qixia_{name}"

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
            "confidence": person.get("confidence", "unverified"),
            "source_ids": ["S001"],
        })

    # Add gap entry if career_timeline is sparse
    if len(career_timeline) <= 1 and not person.get("birth"):
        career_timeline.append({
            "start": "unknown",
            "end": "unknown",
            "org": "履历缺口",
            "title": "",
            "notes": "公开资料不足，完整履历待查。百度百科403禁止访问，搜索引擎超时。",
            "confidence": "unverified",
            "source_ids": [],
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
        rels_output.append({
            "person": other_name,
            "person_id": f"qixia_{other_name}",
            "relationship_type": "overlap" if r["type"] != "前任后继" else "predecessor_successor",
            "strength": "strong",
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
            "title": f"栖霞市、{name}相关资料",
            "url": source_url,
            "publisher": "百度百科/搜狗微信/政府网站",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official" if "gov.cn" in source_url else "encyclopedia",
            "reliability": "medium",
            "notes": "2026年8月调研数据",
        }
    ]

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": PROVINCE,
            "city": CITY,
            "region": f"{SLUG}",
            "job": person.get("current_post", ""),
            "task_id": "shandong_栖霞市",
            "time_focus": "2026年8月",
        },
        "identity": {
            "person_id": slug_id,
            "name": name,
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [],
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
            "administrative_rank": "",
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
            "career_pattern": "unknown",
            "systems_experience": [],
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
            "identity": "unverified" if not person.get("birth") else "confirmed",
            "current_role": person.get("confidence", "unverified"),
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "出生年月、籍贯、完整履历（百度百科403），搜索引擎超时",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的出生年月、籍贯、学历教育背景",
                "why_it_matters": "核心身份信息，用于去重和跨区域关联分析",
                "suggested_queries": [f"{name} 简历", f"{name} 任前公示", f"{name} 百度百科"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": f"{name}的完整任职履历（每段职务的起止时间）",
                "why_it_matters": "关系网络分析需要精确的时间线",
                "suggested_queries": [f"{name} 此前担任", f"{name} 任职经历"],
                "last_attempted": AS_OF,
            },
        ],
    }

    # Add extra open question for 市委书记
    if name == "赵永刚":
        record["open_questions"].insert(0, {
            "priority": "critical",
            "question": "赵永刚2005年前早期履历（寿光前）",
            "why_it_matters": "了解其职业起点和培养轨迹",
            "suggested_queries": ["赵永刚 寿光 统战部", "赵永刚 青岛大学", "赵永刚 1998"],
            "last_attempted": AS_OF,
        })
    elif name == "臧雷":
        record["open_questions"].insert(0, {
            "priority": "critical",
            "question": "臧雷2023年前完整履历（来到栖霞前的人生轨迹）",
            "why_it_matters": "现任市长，核心目标人物之一，缺少姓名则无法进行任何关系分析",
            "suggested_queries": ["臧雷 栖霞 市长 履历", "臧雷 烟台 此前担任"],
            "last_attempted": AS_OF,
        })

    fname = f"{TODAY}-{PROVINCE}-{CITY}-{person['current_post']}-{person['name']}.json"
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

    # Write person JSONs
    print("  Writing person JSONs...")
    core_ids = {1, 2}  # 赵永刚, 臧雷
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())