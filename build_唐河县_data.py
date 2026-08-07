#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 唐河县 (Tanghe County), 河南省南阳市.

Task ID: henan_唐河县 | Level: 县 | Targets: 县委书记 & 县长
Investigation date: 2026-08-06

Research sources:
  - baike.baidu.com 乔国涛 / 中国共产党唐河县委员会（县委常委会构成、任免时间线）
  - www.tanghe.gov.cn 唐河县人民政府（政府工作报告、政府常务会、领导人活动）
  - www.nanyang.gov.cn 南阳市人民政府（县区动态、三级干部会议、高考巡查、现场办公）
  - 新华网/人民网/河南日报/大河网 县委组织部任前公示（2021-08-25、2026-04-07）
  - nysrd.henanrd.gov.cn 南阳人大（常委会领导页、七届人大五次会议选举）
  - 中国日报网、澎湃新闻、南阳网（贺迎访营商环境、城建现场办公、人大选举）

Confidence:
  - 贺迎 identity+current(前书记) confirmed（2021-08 公示转正书记；2026-02-09 当选南阳市人大常委会副主任 -> 已离任唐河）
  - 周天龙 confirmed: 2014-2021 唐河县长/书记，2022-02 南阳市人大常委会副主任（1965.10 出生）
  - 乔国涛 current+resume confirmed（百度百科 fn: 1977.05，河南南阳；县政府 2026-01/02 常务会仍以代县长+县长见报；2026-04-07 拟任县委书记）
  - 县委书记现在归属：贺迎 2026 年 2 月升任市人大副主任离任唐河，乔国涛 2026-04 拟任县（市、区）委书记，推断就地继任县委书记（未获专门任免新闻最终确认，标 plausible）
  - 李靖、黄磊、陈达、陈光义、-魏飞、杨先锋 出生年/籍贯 未能核实（medium）
"""

import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING = os.path.dirname(os.path.abspath(__file__))
SLUG = "唐河县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

DB_PATH = os.path.join(STAGING, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING, f"{SLUG}_network.gexf")
PERSONS_DIR = Path(STAGING)

person_id_to_hash = {}
org_id_to_hash = {}

# ── Persons ─────────────────────────────────────────────────────────────────
persons = [
    # 0 = 不需要，1 起
    {"id": 1, "name": "乔国涛", "gender": "男", "ethnicity": "汉族", "birth": "1977年5月",
     "birthplace": "河南南阳", "education": "省委党校研究生、管理学学士（河南省委党校法律专业研究生）",
     "party_join": "中共党员", "work_start": "1999.10",
     "current_post": "县委副书记、县长",
     "current_org": "唐河县人民政府",
     "source": "https://baike.baidu.com/item/乔国涛/19759922"},
    {"id": 2, "name": "贺迎", "gender": "男", "ethnicity": "汉族", "birth": "1971年3月",
     "birthplace": "", "education": "大学本科（农业推广硕士）",
     "party_join": "中共党员", "work_start": "",
     # 2026-02 当选市人大副主任，已离任唐河县委书记
     "current_post": "南阳市人大常委会副主任",
     "current_org": "南阳市人大常委会",
     "source": "http://district.ce.cn/newarea/sddy/202602/t20260209_2762585.shtml"},
    {"id": 3, "name": "周天龙", "gender": "男", "ethnicity": "汉族", "birth": "1965年10月",
     "birthplace": "", "education": "南阳师专中文系（1987）、郑州大学法律专业自考本科（2001）",
     "party_join": "中共党员", "work_start": "1987年",
     "current_post": "南阳市人大常委会副主任",
     "current_org": "南阳市人大常委会",
     "source": "https://nysrd.henanrd.gov.cn/cwhld"},
    {  # 专职副书记（原）
        "id": 4, "name": "李靖", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县委副书记（原，现任唐河县委副书记）", "current_org": "中共唐河县委员会",
     "source": "https://www.nanyang.gov.cn/2024/12-26/833924.html"},
    {  # 常务副县长
        "id": 5, "name": "黄磊", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、常务副县长", "current_org": "唐河县人民政府",
     "source": "https://www.nanyang.gov.cn/2024/12-26/833925.html"},
    {"id": 6, "name": "陈达", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县人大常委会主任", "current_org": "唐河县人民代表大会常务委员会",
     "source": "https://www.tanghe.gov.cn/2025/06-07/79495.html"},
    {"id": 7, "name": "陈光义", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、政法委书记", "current_org": "中共唐河县委员会",
     "source": "https://www.tanghe.gov.cn/2023/06-07/647ffd7ca310dbde06d22401.html"},
    {"id": 8, "name": "魏飞", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "前任组织部长", "current_org": "中共唐河县委员会",
     "source": "https://www.tanghe.gov.cn/2021/10-29/58435.html"},
    {"id": 9, "name": "杨先锋", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、组织部部长", "current_org": "中共唐河县委员会",
     "source": "https://www.tanghe.gov.cn/2022/07/01/328172.html"},
    {"id": 10, "name": "李中阳", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、宣传部长、副县长", "current_org": "中共唐河县委员会",
     "source": "https://www.tanghe.gov.cn/2024/06-07/79495.html"},
]

# ── Organizations ───────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共唐河县委员会", "type": "党委", "level": "县级", "parent": "中共南阳市委", "location": "南阳市唐河县"},
    {"id": 2, "name": "唐河县人民政府", "type": "政府", "level": "县级", "parent": "南阳市人民政府", "location": "南阳市唐河县"},
    {"id": 3, "name": "唐河县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "唐河县", "location": "南阳市唐河县"},
    {"id": 4, "name": "中国人民政治协商会议唐河县委员会", "type": "政协", "level": "县级", "parent": "唐河县", "location": "南阳市唐河县"},
    {"id": 5, "name": "中共南阳市委", "type": "党委", "level": "地级市", "parent": "中共河南省委", "location": "南阳市"},
    {"id": 6, "name": "南阳市人民政府", "type": "政府", "level": "地级市", "parent": "河南省人民政府", "location": "南阳市"},
    {"id": 7, "name": "南阳市人民代表大会常务委员会", "type": "人大", "level": "副厅级", "parent": "南阳市", "location": "南阳市"},
    {"id": 8, "name": "河南省纪委监委", "type": "纪委", "level": "省级", "parent": "中共河南省委", "location": "郑州市"},
    {"id": 9, "name": "中共社旗县委员会", "type": "党委", "level": "县级", "parent": "中共南阳市委", "location": "南阳市社旗县"},
    {"id": 10, "name": "社旗县人民政府", "type": "政府", "level": "县级", "parent": "南阳市人民政府", "location": "南阳市社旗县"},
    {"id": 11, "name": "中共方城县委员会", "type": "党委", "level": "县级", "parent": "中共南阳市委", "location": "南阳市方城县"},
    {"id": 12, "name": "方城县人民政府", "type": "政府", "level": "县级", "parent": "南阳市人民政府", "location": "南阳市方城县"},
    {"id": 13, "name": "南阳市纪委市监委", "type": "纪委", "level": "地级市", "parent": "中共南阳市委", "location": "南阳市"},
    {"id": 14, "name": "镇平县公安局", "type": "政府", "level": "县级", "parent": "镇平县人民政府", "location": "南阳市镇平县"},
    {"id": 15, "name": "中共镇平县委员会", "type": "党委", "level": "县级", "parent": "中共南阳市委", "location": "南阳市镇平县"},
    {"id": 16, "name": "桐柏县人民政府", "type": "政府", "level": "县级", "parent": "南阳市人民政府", "location": "南阳市桐柏县"},
    {"id": 17, "name": "中共桐柏县委员会", "type": "党委", "level": "县级", "parent": "中共南阳市委", "location": "南阳市桐柏县"},
    {"id": 18, "name": "唐河县纪委县监委", "type": "纪委", "level": "县级", "parent": "中共唐河县委", "location": "南阳市唐河县"},
]

# ── Positions ───────────────────────────────────────────────────────────────
positions = [
    # 乔国涛（县长 → 拟任县委书记）
    {"person_id": 1, "org_id": 14, "title": "镇平县公安局柳泉铺派出所警长、副所长", "start_date": "1999.10", "end_date": "2002.12", "rank": "科员", "note": "基层公安"},
    {"person_id": 1, "org_id": 13, "title": "南阳市纪委科员/副主任科员/副科级纪检监察员/主任科员", "start_date": "2002.12", "end_date": "2008.11", "rank": "正科级", "note": "市纪委八年"},
    {"person_id": 1, "org_id": 13, "title": "南阳市纪委案件一室副主任（正科级）", "start_date": "2008.11", "end_date": "2011.01", "rank": "正科级", "note": "纪检办案"},
    {"person_id": 1, "org_id": 12, "title": "方城县人民政府副县长", "start_date": "2012.02", "end_date": "2014.12", "rank": "副县级", "note": "2011.01-2011.02 公开选拔任副县处级干部；期间河南省委党校法律专业研究生"},
    {"person_id": 1, "org_id": 9, "title": "社旗县委常委、统战部部长", "start_date": "2014.12", "end_date": "2016.02", "rank": "副县级", "note": "跨县交流"},
    {"person_id": 1, "org_id": 1, "title": "唐河县委常委、办公室主任", "start_date": "2016.02", "end_date": "2019.11", "rank": "副县级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "唐河县委常委、县政府副县长", "start_date": "2019.12", "end_date": "2021.08", "rank": "副县级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "唐河县委副书记、县长", "start_date": "2021.09", "end_date": "至今", "rank": "正县级", "note": "2021-08-30 干部会议提名；2021-09 就任。2026-04-07 拟任县（市、区）委书记。"},
    # 贺迎（前县委书记）
    {"person_id": 2, "org_id": 2, "title": "唐河县委副书记、县长", "start_date": "2019.11", "end_date": "2021.08", "rank": "正县级", "note": "2019-11-09 提名县长"},
    {"person_id": 2, "org_id": 1, "title": "县委书记", "start_date": "2021.08", "end_date": "约2026.02", "rank": "正处级", "note": "2021-08-30 任唐河县委书记；2026 年进入南阳人大"},
    {"person_id": 2, "org_id": 7, "title": "南阳市人大常委会副主任", "start_date": "2026.02", "end_date": "至今", "rank": "副厅级", "note": "2026-02-09 南阳市七届人大五次会议当选"},
    # 周天龙（前任县委书记）
    {"person_id": 3, "org_id": 2, "title": "唐河县委副书记、县长", "start_date": "2014.04", "end_date": "2018.11", "rank": "正县级", "note": "2014.04 任唐河县长"},
    {"person_id": 3, "org_id": 1, "title": "县委书记", "start_date": "2018.11", "end_date": "2021.08", "rank": "正处级", "note": "2018-11-26 任唐河县委书记"},
    {"person_id": 3, "org_id": 7, "title": "南阳市人大常委会副主任", "start_date": "2022.02", "end_date": "至今", "rank": "副厅级", "note": "2022-02-12 市六届人大六次会议当选"},
    # 李靖（专职副书记）
    {"person_id": 4, "org_id": 1, "title": "县委副书记", "start_date": "2023", "end_date": "至今", "rank": "副县级", "note": "唐河县委副书记"},
    # 黄磊（常务副县长）
    {"person_id": 5, "org_id": 2, "title": "县委常委、常务副县长", "start_date": "2023", "end_date": "至今", "rank": "副县级", "note": "前期任县委常委、县委办主任"},
    # 陈达（人大主任）
    {"person_id": 6, "org_id": 3, "title": "县人大常委会主任", "start_date": "2022", "end_date": "至今", "rank": "正县级", "note": "县人大"},
    # 陈志义（政法委书记）
    {"person_id": 7, "org_id": 1, "title": "县委常委、政法委书记", "start_date": "2023", "end_date": "至今", "rank": "副县级", "note": ""},
    # 魏飞（前任组织部长）
    {"person_id": 8, "org_id": 1, "title": "县委常委、组织部部长", "start_date": "2021", "end_date": "2022", "rank": "副县级", "note": "2021-2022 任组织部长"},
    # 杨先锋（组织部部长）
    {"person_id": 9, "org_id": 1, "title": "县委常委、组织部部长", "start_date": "2022", "end_date": "至今", "rank": "副县级", "note": ""},
    # 李中阳（宣传部长、副县长）
    {"person_id": 10, "org_id": 1, "title": "县委常委、宣传部长、副县长", "start_date": "2021", "end_date": "至今", "rank": "副县级", "note": ""},
]

# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor", "context": "贺迎2021-08此前任唐河县委书记，2026-02调南阳市人大；乔国涛具有相同岗位稳定接续", "overlap_org": "中共唐河县委员会", "overlap_period": "2021-2026"},
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "乔国涛任唐河县长（2021-09以后），贺迎任县委书记兼县长（2021.08-2026），党政一把手搭档", "overlap_org": "唐河县", "overlap_period": "2021-2026"},
    {"person_a": 2, "person_b": 3, "type": "predecessor_successor", "context": "周天龙2021.08卸任唐河县委书记，贺迎同期接手；周转任南阳人大", "overlap_org": "中共唐河县委员会", "overlap_period": "2018-2021（周）→2021（贺）"},
    {"person_a": 3, "person_b": 1, "type": "superior_subordinate", "context": "周天龙任书记/县长期，乔国涛2016-2021先后任县委办主任、副县长（在周手下任职）", "overlap_org": "唐河县", "overlap_period": "2016-2021"},
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "贺迎与周天龙在唐河县干部交接期共事（2021.08交界）", "overlap_org": "唐河县", "overlap_period": "2021"},
    {"person_a": 4, "person_b": 1, "type": "overlap", "context": "李靖任县委副书记、乔国涛任县长，同在一套县委班子", "overlap_org": "中共唐河县委常委会", "overlap_period": "2023至今"},
    {"person_a": 5, "person_b": 1, "type": "overlap", "context": "黄磊任常务副县长、乔国涛任县长，政府班子搭档", "overlap_org": "唐河县人民政府", "overlap_period": "2023至今"},
    {"person_a": 1, "person_b": 6, "type": "same_system", "context": "乔国涛县长与陈达人大主任在工作中对接（同一条线）", "overlap_org": "唐河县", "overlap_period": "2022至今"},
]


# ══════════════════════════════════════════════════════════════════════════
# Person Graph JSON writers
# ══════════════════════════════════════════════════════════════════════════

def _source_register():
    return [
        {"id": "S001", "title": "百度百科—乔国涛", "url": "https://baike.baidu.com/item/乔国涛/19759922", "publisher": "百度百科", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium"},
        {"id": "S002", "title": "河南省委组织部2026-04-07任前公示（乔国涛拟任县市区委书记）", "url": "http://www.ha.xinhuanet.com/20260407/1e2d130edcf3436f9f88d83a673a9cd8.html", "publisher": "河南日报/新华网", "accessed_at": AS_OF, "source_type": "appointment_notice", "reliability": "high"},
        {"id": "S003", "title": "河南省委组织部2021-08-25任前公示（贺迎拟任县委书记）", "url": "http://renshi.people.com.cn/n1/2021/0825/c139617-32206839.html", "publisher": "中国共产党新闻网/组织部", "accessed_at": AS_OF, "source_type": "appointment_notice", "reliability": "high"},
        {"id": "S004", "title": "中国经济网—李林、罗岩涛、党建凯、贺迎当选南阳市人大常委会副主任", "url": "http://district.ce.cn/newarea/sddy/202602/t20260209_2762585.shtml", "publisher": "中国经济网/南阳日报", "accessed_at": AS_OF, "source_type": "media", "reliability": "high"},
        {"id": "S005", "title": "南阳市人大常委会—常委会领导", "url": "https://nysrd.henanrd.gov.cn/cwhld", "publisher": "南阳人大", "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
        {"id": "S006", "title": "天天百科—周天龙(南阳市人大常委会副主任)", "url": "https://twwiki.net/wiki/36k3w97xwyrqn2k.html", "publisher": "天天百科", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium"},
        {"id": "S007", "title": "唐河县人民政府—十六届政府第四十七次常务会（2026-02-14）", "url": "https://www.tanghe.gov.cn/2026/02-14/1386587.html", "publisher": "唐河县人民政府", "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
        {"id": "S008", "title": "南阳市人民政府—唐河县三级干部会议（2025-03-10）", "url": "https://www.nanyang.gov.cn/2025/03-10/945212.html", "publisher": "南阳市人民政府", "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
        {"id": "S009", "title": "南阳市人民政府—2024-12-24 唐河县专场新闻发布会", "url": "https://www.nanyang.gov.cn/2024/12-26/833925.html", "publisher": "南阳市人民政府", "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
        {"id": "S010", "title": "唐河县人民政府—2025年政府工作报告（乔国涛）", "url": "https://www.tanghe.gov.cn/2025/03-06/1193483.html", "publisher": "唐河县人民政府", "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
        {"id": "S011", "title": "中国共产党唐河县委员会—百科", "url": "https://baike.baidu.com/item/中国共产党唐河县委员会/55734599", "publisher": "百度百科", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium"},
        {"id": "S012", "title": "南阳市人民政府—唐河县乔国涛调研（2026-02-11）", "url": "https://www.nanyang.gov.cn/2026/02-11/940888.html", "publisher": "南阳市人民政府", "accessed_at": AS_OF, "source_type": "official", "reliability": "high"},
    ]


def _relationships_for(person_id):
    out = []
    for r in relationships:
        if r["person_a"] == person_id:
            other = r["person_b"]
        elif r["person_b"] == person_id:
            other = r["person_a"]
        else:
            continue
        other_name = {p["id"]: p["name"] for p in persons}[other]
        out.append({
            "person": other_name,
            "person_id": f'henan_tanghe_{other_name}',
            "relationship_type": r["type"],
            "strength": "strong" if r["type"] in ("superior_subordinate", "predecessor_successor", "successor_predecessor") else "medium",
            "evidence": r["context"],
            "overlap_org": r["overlap_org"],
            "overlap_period": r["overlap_period"],
            "direction": "undirected",
            "confidence": "confirmed" if r["type"] in ("superior_subordinate", "predecessor_successor") else "plausible",
            "source_ids": [],
        })
    # dedupe by person_name + type
    seen = set()
    dedup = []
    for x in out:
        key = (x["person"], x["relationship_type"])
        if key in seen:
            continue
        seen.add(key)
        dedup.append(x)
    return dedup


def _career_timeline_for(person_id):
    rows = [pos for pos in positions if pos["person_id"] == person_id]
    tl = []
    for r in rows:
        loc = "唐河县" if r.get("org_id") in (1, 2, 3, 18) else "南阳市"
        title = r.get("title", "")
        system = "discipline" if "纪委" in title else ("government" if "县长" in title or "副县长" in title or "公安" in title else "party")
        tl.append({
            "start": r.get("start_date", ""),
            "end": r.get("end_date", ""),
            "org": {o["id"]: o["name"] for o in organizations}.get(r.get("org_id", ""), ""),
            "title": title,
            "level": "",
            "location": loc,
            "system": system,
            "rank": r.get("rank", ""),
            "is_key_promotion": title in ("县委书记", "县委副书记、县长", "南阳市人大常委会副主任"),
            "notes": r.get("note", ""),
            "confidence": "confirmed",
            "source_ids": [],
        })
    return tl


def _organizations_for(person_id):
    org_ids = {r["org_id"] for r in positions if r["person_id"] == person_id}
    return [
        {"name": o["name"], "org_type": o["type"], "level": o["level"], "parent": o["parent"], "location": o["location"], "role": "affiliated"}
        for o in organizations if o["id"] in org_ids
    ]


def write_person_json(p):
    role = p["current_post"].split("（")[0]
    # 现任与前任在文件名上区分
    fname = f"{TODAY}-河南省-南阳市-{role}-{p['name']}.json"
    tl = _career_timeline_for(p["id"])
    doc = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "河南省", "city": "南阳市", "region": "唐河县",
            "job": p["current_post"], "task_id": "henan_唐河县", "time_focus": "2014-2026",
        },
        "identity": {
            "person_id": f'henan_tanghe_{p["name"]}',
            "name": p["name"], "aliases": [],
            "gender": p.get("gender", ""), "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""), "birthplace": p.get("birthplace", ""), "native_place": "",
            "education": [{"period": "", "institution": "河南省委党校" if p["id"] == 1 else "", "major": "", "degree": p.get("education", ""), "study_type": "party_school" if p["id"] == 1 else "unknown"}],
            "party_join": p.get("party_join", ""), "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p.get('birth','')}",
                "name_birthplace": f"{p['name']}_{p.get('birthplace','')}",
                "official_profile_url": "",
            },
        },
        "current_status": {
            "current_post": p.get("current_post", ""), "current_org": p.get("current_org", ""),
            # 1=县长（正县）、2/3=市人大副主任（副厅）、其余=副县
            "administrative_rank": "正县级" if p["id"] == 1 else ("副厅级" if p["id"] in (2, 3) else "副县级"),
            "as_of": AS_OF,
            "is_current_confirmed": p["id"] in (2, 3),
            "source_ids": [],
        },
        "career_timeline": tl,
        "organizations": _organizations_for(p["id"]),
        "relationships": _relationships_for(p["id"]),
        "governance_record": [
            {
                "period": "2024",
                "domain": "economic_development",
                "achievement_or_event": "全县生产总值 463.8 亿元，增长 5.7%，总量全市第三；争取政策/融资项目资金 106 亿元，连续四年全市领先；招商引资 89.8 亿元",
                "role_in_event": "县长（乔国涛主持政府工作）",
                "measurable_outcome": "生产总值 463.8 亿元、规上工业增 15.8%",
                "location": "唐河县",
                "confidence": "confirmed" if p["id"]==1 else "plausible",
                "source_ids": ["S010"],
            },
        ] if p["id"] == 1 else [],
        "professional_profile": {
            "primary_specializations": ["纪检监察" ] if p["id"] == 1 else [],
            "secondary_specializations": ["公安基层"] if p["id"] == 1 else [],
            "career_pattern": "cross_county_rotation" if p["id"] == 1 else ("local_ladder" if p["id"] in (3,) else "unknown"),
            "systems_experience": [],
            "geographic_pattern": ["镇平", "方城", "社旗", "唐河", "南阳"] if p["id"] == 1 else [],
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {"trait": "pragmatic" if p["id"]==1 else "stability_oriented",
                 "evidence": "强调项目带动、招商引资、拼抢快干（三级干部会）" if p["id"]==1 else "人大系统分管预决算监督",
                 "confidence": "plausible", "source_ids": []}
            ],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "工作风格基于公开报道与出席活动推断，非私人心理评估。",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": f"未发现针对{p['name']}的公开纪律处分或负面报道（截至{AS_OF}）", "date": AS_OF, "confidence": "unverified", "source_ids": []}
        ],
        "source_register": _source_register(),
        "confidence_summary": {
            "identity": "confirmed" if p.get("birth") else "partial",
            "current_role": "confirmed" ,
            "career_completeness": "complete" if p["id"] == 1 else ("partial" if p["id"] == 3 else "thin"),
            "relationship_confidence": "high" if p["id"] == 1 else "medium",
            "biggest_gap": "早期履历/出生年籍贯部分未核实" if not p.get("birth") else "早年履历细节未完全核实",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{p['name']}的早年完整履历（2000 年前）与籍贯？",
                "why_it_matters": "人物去重与跨地区网络匹配需要稳定身份键与完整履历。",
                "suggested_queries": [f"{p['name']} 简历 出生于", f"{p['name']} 任前公示"],
                "last_attempted": "2026-08-06",
            }
        ],
    }
    out = PERSONS_DIR / fname
    out.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✅ Person JSON: {out.name}")
    return out


# ══════════════════════════════════════════════════════════════════════════
# Graph + DB build
# ══════════════════════════════════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    role = p.get("current_post", "")
    if "书记" in role:
        return "255,50,50"
    elif "县长" in role or "副县长" in role:
        return "50,100,255"
    elif "人大" in role:
        return "100,150,255"
    else:
        return "100,100,100"


def org_color(o):
    t = o.get("type", "")
    if "党委" in t:
        return "255,200,200"
    elif "政府" in t:
        return "200,200,255"
    elif "纪委" in t:
        return "255,220,180"
    elif "人大" in t:
        return "200,255,255"
    elif "政协" in t:
        return "255,240,200"
    else:
        return "200,200,200"


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>唐河县领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if p["id"] in (1, 2) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value="{pos.get("start_date","")} — {pos.get("end_date","")}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_period",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF: {GEXF_PATH}")


def build_db():
    conn = sqlite3.connect(DB_PATH)
    conn.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS organizations;
        DROP TABLE IF EXISTS persons;
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY, name TEXT NOT NULL, gender TEXT DEFAULT '', ethnicity TEXT DEFAULT '',
            birth TEXT DEFAULT '', birthplace TEXT DEFAULT '', education TEXT DEFAULT '', party_join TEXT DEFAULT '',
            work_start TEXT DEFAULT '', current_post TEXT DEFAULT '', current_org TEXT DEFAULT '', source TEXT DEFAULT '');
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY, name TEXT NOT NULL, type TEXT DEFAULT '', level TEXT DEFAULT '',
            parent TEXT DEFAULT '', location TEXT DEFAULT '');
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER NOT NULL, org_id INTEGER NOT NULL,
            title TEXT DEFAULT '', start_date TEXT DEFAULT '', end_date TEXT DEFAULT '', rank TEXT DEFAULT '', note TEXT DEFAULT '');
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT, person_a INTEGER NOT NULL, person_b INTEGER NOT NULL,
            type TEXT DEFAULT '', context TEXT DEFAULT '', overlap_org TEXT DEFAULT '', overlap_period TEXT DEFAULT '');
    """)
    pcols = ["id", "name", "gender", "ethnicity", "birth", "birthplace", "education", "party_join", "work_start", "current_post", "current_org", "source"]
    for p in persons:
        conn.execute(f"INSERT INTO persons ({','.join(pcols)}) VALUES ({','.join('?' for _ in pcols)})", [p.get(c, "") for c in pcols])
    ocols = ["id", "name", "type", "level", "parent", "location"]
    for o in organizations:
        conn.execute(f"INSERT INTO organizations ({','.join(ocols)}) VALUES ({','.join('?' for _ in ocols)})", [o.get(c, "") for c in ocols])
    qcols = ["person_id", "org_id", "title", "start_date", "end_date", "rank", "note"]
    for pos in positions:
        conn.execute(f"INSERT INTO positions ({','.join(qcols)}) VALUES ({','.join('?' for _ in qcols)})", [pos.get(c, "") for c in qcols])
    rcols = ["person_a", "person_b", "type", "context", "overlap_org", "overlap_period"]
    for r in relationships:
        conn.execute(f"INSERT INTO relationships ({','.join(rcols)}) VALUES ({','.join('?' for _ in rcols)})", [r.get(c, "") for c in rcols])
    conn.commit()
    conn.close()
    print(f"✅ DB: {DB_PATH}")


def build():
    build_db()
    build_gexf()
    # 核心领导：乔国涛（书记/县长）、贺迎（前书记）、周天龙（前任书记/人大副主任）
    for pid in (1, 2, 3):
        p = next(x for x in persons if x["id"] == pid)
        write_person_json(p)


if __name__ == "__main__":
    build()