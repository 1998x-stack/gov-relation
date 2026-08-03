#!/usr/bin/env python3
"""
遂平县（驻马店市）领导班子工作关系网络 — 构建脚本
等级: 县 | 上级: 河南省驻马店市
调查日期: 2026-08-03
"""

import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
from gov_relation.runner import run_build

SLUG = "遂平县"
TODAY = "2026-08-03"
AS_OF = TODAY
PROVINCE = "河南省"
CITY = "驻马店市"
REGION = "遂平县"

HERE = Path(__file__).resolve().parent
DB_PATH = HERE / f"{REGION}_network.db"
GEXF_PATH = HERE / f"{REGION}_network.gexf"
PERSONS_DIR = HERE


# ──────────────────────────────────────────────
# PERSONS
# ──────────────────────────────────────────────

persons = [
    {"id": 1, "name": "李振南", "gender": "女", "ethnicity": "汉族",
     "birth": "1977-07", "birthplace": "河南省泌阳县", "education": "",
     "party_join": "中共党员", "work_start": "1995-09",
     "current_post": "遂平县委书记", "current_org": "中共遂平县委员会",
     "source": "https://www.163.com/dy/article/J24U78A2051998HK.html",
     "notes": "1977年7月生，河南泌阳人。1995年9月参加工作。2024年5月起任县委书记。"},

    {"id": 2, "name": "郭帅", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "遂平县委副书记、县长", "current_org": "遂平县人民政府",
     "source": "https://www.suiping.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202408/t20240813_107123.html",
     "notes": "本科学历。主持县政府全面工作。"},

    {"id": 3, "name": "郭战辉", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "遂平县委副书记（专职）", "current_org": "中共遂平县委员会",
     "source": "https://www.suiping.gov.cn/zwyw/sylbt/202607/t20260706_709341.html",
     "notes": "2026年6月当选第十四届县委副书记。"},

    {"id": 4, "name": "王宁", "gender": "男", "ethnicity": "回族",
     "birth": "1986-06", "birthplace": "", "education": "本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "遂平县委常委、常务副县长", "current_org": "遂平县人民政府",
     "source": "https://www.suiping.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202408/t20240813_107129.html",
     "notes": "1986年6月生，回族，本科学历。负责发改、财政、金融等。"},

    {"id": 5, "name": "冯颖颖", "gender": "女", "ethnicity": "汉族",
     "birth": "1983-01", "birthplace": "", "education": "本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "遂平县委常委、宣传部部长、副县长", "current_org": "中共遂平县委员会宣传部",
     "source": "https://www.suiping.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202408/t20240813_107128.html",
     "notes": "1983年1月生，本科学历。负责教育、融媒体等。"},

    {"id": 6, "name": "冯浩", "gender": "男", "ethnicity": "汉族",
     "birth": "1982-03", "birthplace": "", "education": "本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "遂平县副县长", "current_org": "遂平县人民政府",
     "source": "https://www.zmd.gov.cn/zwgk/zdgk/jzdgk/szfld/sfzszn/202408/t20240813_107125.html",
     "notes": "1982年3月生，本科学历。负责司法、信访、农业农村等。"},

    {"id": 7, "name": "周倜", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-05", "birthplace": "", "education": "本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "遂平县副县长（四级调研员）", "current_org": "遂平县人民政府",
     "source": "https://www.suiping.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202408/t20240813_107124.html",
     "notes": "1981年5月生，本科学历。负责卫生健康、医保、自然资源等。"},

    {"id": 8, "name": "张乐乐", "gender": "女", "ethnicity": "汉族",
     "birth": "1987-08", "birthplace": "", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "遂平县副县长", "current_org": "遂平县人民政府",
     "source": "https://www.suiping.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/202411/t20241120_411876.html",
     "notes": "1987年8月生，研究生学历。负责城市建设、环保等。"},

    {"id": 9, "name": "张卫东", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "遂平县人大常委会主任", "current_org": "遂平县人民代表大会常务委员会",
     "source": "https://www.suiping.gov.cn/zwyw/tpxw/202608/t20260803_717291.html",
     "notes": "公开履历信息有限。"},

    {"id": 10, "name": "史光辉", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "遂平县政协主席", "current_org": "政协遂平县委员会",
     "source": "https://www.suiping.gov.cn/zwyw/tpxw/202608/t20260803_717291.html",
     "notes": "公开履历信息有限。"},

    {"id": 11, "name": "皇甫永强", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "遂平县委常委", "current_org": "中共遂平县委员会",
     "source": "https://www.suiping.gov.cn/zwyw/sylbt/202607/t20260706_709341.html",
     "notes": "2026年6月当选县委常委。具体职务待确认。"},

    {"id": 12, "name": "王娟", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "遂平县委常委", "current_org": "中共遂平县委员会",
     "source": "https://www.suiping.gov.cn/zwyw/sylbt/202607/t20260706_709341.html",
     "notes": "2026年6月当选县委常委。推测为组织部长或统战部长。"},

    {"id": 13, "name": "徐伟远", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "遂平县委常委", "current_org": "中共遂平县委员会",
     "source": "https://www.suiping.gov.cn/zwyw/sylbt/202607/t20260706_709341.html",
     "notes": "2026年6月当选县委常委。"},

    {"id": 14, "name": "郭俊峰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "遂平县委常委", "current_org": "中共遂平县委员会",
     "source": "https://www.suiping.gov.cn/zwyw/sylbt/202607/t20260706_709341.html",
     "notes": "2026年6月当选县委常委。"},

    {"id": 15, "name": "冯全敬", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "遂平县委常委", "current_org": "中共遂平县委员会",
     "source": "https://www.suiping.gov.cn/zwyw/tpxw/202607/t20260731_716838.html",
     "notes": "推测担任政法委书记或统战部长。"},

    {"id": 16, "name": "侯蕴", "gender": "男", "ethnicity": "汉族",
     "birth": "1967-03", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "驻马店市人大常委会副主任", "current_org": "驻马店市人大常委会",
     "source": "https://www.163.com/dy/article/J24H9A205M498HK.html",
     "notes": "1967年3月生。2024年2月当选市人大副主任，5月底卸任县委书记。"},
]

# ──────────────────────────────────────────────────
# ORGANIZATIONS
# ──────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共遂平县委员会", "type": "党委", "level": "县处级",
     "parent": "驻马店市委员会", "location": "河南省驻马店市遂平县"},
    {"id": 2, "name": "遂平县人民政府", "type": "政府", "level": "县处级",
     "parent": "驻马店市人民政府", "location": "河南省驻马店市遂平县"},
    {"id": 3, "name": "遂平县人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "遂平县委员会", "location": "河南省驻马店市遂平县"},
    {"id": 4, "name": "政协遂平县委员会", "type": "政协", "level": "县处级",
     "parent": "政协遂平县委员会", "location": "河南省驻马店市遂平县"},
    {"id": 5, "name": "中共遂平县纪律检查委员会", "type": "纪委", "level": "县处级",
     "parent": "中共遂平县委员会", "location": "河南省驻马店市遂平县"},
    {"id": 6, "name": "中共遂平县委员会组织部", "type": "党委", "level": "县处级",
     "parent": "中共遂平县委员会", "location": "河南省驻马店市遂平县"},
    {"id": 7, "name": "中共遂平县委员会宣传部", "type": "党委", "level": "县处级",
     "parent": "中共遂平县委员会", "location": "河南省驻马店市遂平县"},
]

# ──────────────────────────────────────────────────
# POSITIONS
# ──────────────────────────────────────────────────

positions = [
    # 李振南
    {"person_id": 1, "org_id": 2, "title": "驻马店市橡林乡干部",
     "start": "1995-09", "end": "2002", "rank": "科员", "note": ""},
    {"person_id": 1, "org_id": 2, "title": "驻马店市驿城区西园街道党工委宣传委员",
     "start": "2002", "end": "2005", "rank": "乡镇级", "note": ""},
    {"person_id": 1, "org_id": 2, "title": "驻马店市驿城区区直工委副书记",
     "start": "2005", "end": "2007", "rank": "副科级", "note": ""},
    {"person_id": 1, "org_id": 2, "title": "驻马店市驿城区人大常委会法工委主任",
     "start": "2007", "end": "2012", "rank": "正科级", "note": "兼任办公室主任、党组成员"},
    {"person_id": 1, "org_id": 2, "title": "驻马店市残疾人联合会副理事长",
     "start": "2012", "end": "2013-12", "rank": "正科级", "note": ""},
    {"person_id": 1, "org_id": 2, "title": "驻马店市商务局党组成员、纪检组组长",
     "start": "2013-12", "end": "2016-07", "rank": "正科级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "新蔡县委常委、宣传部长",
     "start": "2016-07", "end": "2020-10", "rank": "副处级", "note": "兼任龙口镇党委书记"},
    {"person_id": 1, "org_id": 1, "title": "新蔡县委常委、副县长",
     "start": "2020-10", "end": "2022-03", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "遂平县委副书记、代县长",
     "start": "2022-03", "end": "2022-04", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 2, "title": "遂平县县长",
     "start": "2022-04", "end": "2024-05", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "遂平县委书记",
     "start": "2024-05", "end": "present", "rank": "正处级", "note": "县人武部党委第一书记"},

    # 郭帅
    {"person_id": 2, "org_id": 1, "title": "遂平县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "遂平县委副书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "遂平县县长", "start": "", "end": "present", "rank": "正处级", "note": ""},

    # 郭战辉
    {"person_id": 3, "org_id": 1, "title": "遂平县委副书记（专职）", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 王宁
    {"person_id": 4, "org_id": 1, "title": "遂平县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "遂平县常务副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 冯颖颖
    {"person_id": 5, "org_id": 1, "title": "遂平县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 7, "title": "遂平县委宣传部部长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "遂平县副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 冯浩
    {"person_id": 6, "org_id": 2, "title": "遂平县副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 周倜
    {"person_id": 7, "org_id": 2, "title": "遂平县副县长（四级调研员）", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 张乐乐
    {"person_id": 8, "org_id": 2, "title": "遂平县副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 张卫东
    {"person_id": 9, "org_id": 3, "title": "遂平县人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": ""},

    # 史光辉
    {"person_id": 10, "org_id": 4, "title": "遂平县政协主席", "start": "", "end": "present", "rank": "正处级", "note": ""},

    # 皇甫永强/王娟/徐伟远/郭俊峰/冯全敬
    {"person_id": 11, "org_id": 1, "title": "遂平县委常委", "start": "", "end": "present", "rank": "副处级", "note": "具体职务待确认"},
    {"person_id": 12, "org_id": 1, "title": "遂平县委常委", "start": "", "end": "present", "rank": "副处级", "note": "具体职务待确认"},
    {"person_id": 13, "org_id": 1, "title": "遂平县委常委", "start": "", "end": "present", "rank": "副处级", "note": "具体职务待确认"},
    {"person_id": 14, "org_id": 1, "title": "遂平县委常委", "start": "", "end": "present", "rank": "副处级", "note": "具体职务待确认"},
    {"person_id": 15, "org_id": 1, "title": "遂平县委常委", "start": "", "end": "present", "rank": "副处级", "note": "具体职务待确认"},

    # 侯蕴
    {"person_id": 16, "org_id": 1, "title": "遂平县委书记", "start": "", "end": "2024-05", "rank": "正处级", "note": "前任县委书记"},
    {"person_id": 16, "org_id": 2, "title": "驻马店市人大常委会副主任", "start": "2024-02", "end": "present", "rank": "副厅级", "note": "2024年2月起任现职"},
]

# ──────────────────────────────────────────────────
# RELATIONSHIPS
# ──────────────────────────────────────────────────

relationships = [
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "县委书记与县长党政工作搭档", "overlap_org": "遂平县委县政府", "overlap_period": "2024-至今"},
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "县委书记与县委专职副书记", "overlap_org": "中共遂平县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "县委书记与常务副县长", "overlap_org": "中共遂平县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "overlap",
     "context": "县委书记与宣传部长", "overlap_org": "中共遂平县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 11, "type": "overlap",
     "context": "县委书记与县委常委皇甫永强", "overlap_org": "中共遂平县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 12, "type": "overlap",
     "context": "县委书记与县委常委王娟", "overlap_org": "中共遂平县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 13, "type": "overlap",
     "context": "县委书记与县委常委徐伟远", "overlap_org": "中共遂平县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 14, "type": "overlap",
     "context": "县委书记与县委常委郭俊峰", "overlap_org": "中共遂平县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 15, "type": "overlap",
     "context": "县委书记与县委常委冯全敬", "overlap_org": "中共遂平县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "overlap",
     "context": "县委书记与人大常委会主任", "overlap_org": "遂平县四套班子", "overlap_period": ""},
    {"person_a": 1, "person_b": 10, "type": "overlap",
     "context": "县委书记与政协主席", "overlap_org": "遂平县四套班子", "overlap_period": ""},
    {"person_a": 2, "person_b": 4, "type": "overlap",
     "context": "县长与常务副县长", "overlap_org": "遂平县政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 6, "type": "overlap",
     "context": "县长与副县长冯浩", "overlap_org": "遂平县政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 7, "type": "overlap",
     "context": "县长与副县长周倜", "overlap_org": "遂平县政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "overlap",
     "context": "县长与副县长张乐乐", "overlap_org": "遂平县政府", "overlap_period": ""},
    {"person_a": 16, "person_b": 1, "type": "predecessor_successor",
     "context": "侯蕴任遂平县委书记后升任市人大副主任，李振南接任", "overlap_org": "中共遂平县委", "overlap_period": "2024"},
]

# ──────────────────────────────────────────────────
# SOURCE REGISTER
# ──────────────────────────────────────────────────

def make_source_register():
    return [
        {"id": "S001", "title": "遂平县人民政府官网", "url": "https://www.suiping.gov.cn/",
         "publisher": "遂平县人民政府", "published_at": "", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high", "notes": ""},
        {"id": "S002", "title": "遂平县政府领导信息页", "url": "https://www.suiping.gov.cn/zwgk/zfxxgk/fdzdgknr/jgjs/szfld/",
         "publisher": "遂平县人民政府", "published_at": "", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high", "notes": "政府领导信息"},
        {"id": "S003", "title": "网易新闻：李振南任遂平县委书记（含简历）",
         "url": "https://www.163.com/dy/article/J24H9A205KOLHK.html",
         "publisher": "河南经济网", "published_at": "2024-05-14", "accessed_at": AS_OF,
         "source_type": "media", "reliability": "high", "notes": "李振南全简历"},
        {"id": "S004", "title": "遂平县第十四次党代会报道",
         "url": "https://www.suiping.gov.cn/zwyw/sylbt/202607/t20260706_709341.html",
         "publisher": "遂平县政府", "published_at": "2026-07-06", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high", "notes": "县委常委名单"},
        {"id": "S005", "title": "遂平县2026年经济运行会议",
         "url": "https://www.suiping.gov.cn/zwyw/tpxw/202608/t20260803_717291.html",
         "publisher": "遂平县政府", "published_at": "2026-08-03", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high", "notes": "领导机构确认"},
        {"id": "S006", "title": "县委议军会议报道",
         "url": "https://www.suiping.gov.cn/zwyw/tpxw/202607/t20260731_716835.html",
         "publisher": "遂平县政府", "published_at": "2026-07-31", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high", "notes": "出席领导名单"},
    ]


# ──────────────────────────────────────────────────
# PERSON GRAPH JSON
# ──────────────────────────────────────────────────

def make_person_json(person, timeline, person_relationships, source_register):
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": PROVINCE, "city": CITY, "region": REGION,
            "job": person.get("current_post", ""), "task_id": "henan_遂平县",
            "time_focus": "2015-2026",
        },
        "identity": {
            "person_id": f"suiping_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "education": [{"period": "", "institution": person.get("education", ""), "major": "",
                           "degree": "", "study_type": "unknown", "source_ids": []}],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person.get('birth', '')}",
                "name_birthplace": f"{person['name']}_{person.get('birthplace', '')}",
                "official_profile_url": person.get("source", ""),
            },
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"],
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": person_relationships,
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
            "caveat": "Work style is inferred from public records, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "未发现公开的纪律处分或负面报道", "date": "",
             "confidence": "unverified", "source_ids": []}
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "多人的早期履历和具体职务分工未公开确认",
        },
        "open_questions": [
            {"priority": "critical", "question": f"{person['name']}的完整履历",
             "why_it_matters": "全面了解晋升路径",
             "suggested_queries": [f"{person['name']} 简历"],
             "last_attempted": AS_OF},
        ],
    }


# ──────────────────────────────────────────────────
# MAIN
# ──────────────────────────────────────────────────

def build():
    print("=" * 60)
    print("  驻马店市遂平县领导班子工作关系网络")
    print("  等级: 县")
    print("  调查日期: 2026-08-03")
    print("=" * 60)

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
    print(f"\n✅ 遂平县数据构建完成")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

    # Person JSONs
    print("\n--- 生成 Person Graph JSONs ---")
    src_reg = make_source_register()

    # 李振南
    lizn_timeline = [
        {"start": "1995-09", "end": "2002", "org": "驻马店市橡林乡",
         "title": "乡干部", "notes": "1995年9月参加工作", "confidence": "confirmed", "source_ids": ["S003"]},
        {"start": "2002", "end": "2005", "org": "驻马店市驿城区西园街道",
         "title": "党工委宣传委员", "notes": "", "confidence": "confirmed", "source_ids": ["S003"]},
        {"start": "2005", "end": "2007", "org": "驿城区区直工委",
         "title": "副书记", "notes": "", "confidence": "confirmed", "source_ids": ["S003"]},
        {"start": "2007", "end": "2012", "org": "驿城区人大常委会",
         "title": "法工委主任", "notes": "兼任办公室主任、党组成员", "confidence": "confirmed", "source_ids": ["S003"]},
        {"start": "2012", "end": "2013-12", "org": "驻马店市残疾人联合会",
         "title": "副理事长", "notes": "", "confidence": "confirmed", "source_ids": ["S003"]},
        {"start": "2013-12", "end": "2016-07", "org": "驻马店市商务局",
         "title": "党组成员、纪检组组长", "notes": "", "confidence": "confirmed", "source_ids": ["S003"]},
        {"start": "2016-07", "end": "2020-10", "org": "新蔡县委",
         "title": "县委常委、宣传部长", "notes": "兼任龙口镇党委书记", "confidence": "confirmed", "source_ids": ["S003"]},
        {"start": "2020-10", "end": "2022-03", "org": "新蔡县委",
         "title": "县委常委、副县长", "notes": "", "confidence": "confirmed", "source_ids": ["S003"]},
        {"start": "2022-03", "end": "2022-04", "org": "中共遂平县委员会",
         "title": "县委副书记、代县长", "notes": "", "confidence": "confirmed", "source_ids": ["S003", "S001"]},
        {"start": "2022-04", "end": "2024-05", "org": "遂平县人民政府",
         "title": "遂平县县长", "notes": "", "confidence": "confirmed", "source_ids": ["S003", "S001"]},
        {"start": "2024-05", "end": "present", "org": "中共遂平县委员会",
         "title": "遂平县委书记", "notes": "县人武部党委第一书记", "confidence": "confirmed", "source_ids": ["S003", "S001"]},
    ]
    lizn_rels = [
        {"person": "郭帅", "person_id": "suiping_郭帅", "relationship_type": "overlap",
         "strength": "strong", "evidence": "县委书记与县长党政工作搭档",
         "overlap_org": "遂平县委县政府", "overlap_period": "2024-至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "侯蕴", "person_id": "suiping_侯蕴", "relationship_type": "predecessor_successor",
         "strength": "strong", "evidence": "侯蕴曾任县委书记，李振南接任",
         "overlap_org": "中共遂平县委", "overlap_period": "2024",
         "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S003"]},
    ]
    lizn_json = make_person_json(persons[0], lizn_timeline, lizn_rels, src_reg)
    lj_path = PERSONS_DIR / f"{TODAY}-河南省-驻马店市-县委书记-李振南.json"
    with open(lj_path, "w", encoding="utf-8") as f:
        json.dump(lizn_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {lj_path.name}")

    # 郭帅
    gs_timeline = [
        {"start": "", "end": "", "org": "（履历待查）",
         "title": "公开资料未找到郭帅任现职前的任职履历",
         "notes": "现任遂平县委副书记、县长。此前经历待查。",
         "confidence": "unverified", "source_ids": []},
        {"start": "", "end": "present", "org": "遂平县人民政府",
         "title": "遂平县县长", "notes": "", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
    ]
    gs_rels = [
        {"person": "李振南", "person_id": "suiping_李振南", "relationship_type": "overlap",
         "strength": "strong", "evidence": "县长与县委书记党政工作搭档",
         "overlap_org": "遂平县委县政府", "overlap_period": "2024-至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    gs_json = make_person_json(persons[1], gs_timeline, gs_rels, src_reg)
    gs_path = PERSONS_DIR / f"{TODAY}-河南省-驻马店市-县长-郭帅.json"
    with open(gs_path, "w", encoding="utf-8") as f:
        json.dump(gs_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {gs_path.name}")

    print(f"\n  所有 Person Graph JSONs 已生成到: {PERSONS_DIR}")


if __name__ == "__main__":
    build()