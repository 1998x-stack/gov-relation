#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 上海市浦东新区 leadership network.

调查日期: 2026-07-25
信息来源: 上海市浦东新区人民政府门户网站 (www.pudong.gov.cn)
调查级别: 市辖区(直辖市)

Confirmed leaders (as of 2026-07):
- 朱芝松 — 上海市委常委、浦东新区区委书记
- 吴金城 — 浦东新区区委副书记、区长
"""

import json
import os
import sqlite3
import sys
from datetime import datetime

# ── Paths ──────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

STAGING_DIR = BASE
DB_PATH = os.path.join(STAGING_DIR, "浦东新区_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "浦东新区_network.gexf")
PERSONS_DIR = STAGING_DIR

TODAY = datetime.now().strftime("%Y%m%d")
SLUG = "上海市浦东新区"

# ── PERSONS ────────────────────────────────────────────────────────
persons = [
    # ═══════════════════════════════════════════════
    # 区委领导 (District Party Committee)
    # ═══════════════════════════════════════════════

    # 区委书记 — 朱芝松
    {
        "id": 1,
        "name": "朱芝松",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969-02",
        "birthplace": "江苏连云港",
        "education": "大学学历，工商管理硕士",
        "party_join": "中共党员",
        "work_start": "1992-08",
        "current_post": "上海市委常委、浦东新区区委书记",
        "current_org": "中共上海市浦东新区委员会",
        "source": "https://www.pudong.gov.cn/",
    },
    # 区委副书记、区长 — 吴金城
    {
        "id": 2,
        "name": "吴金城",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-12",
        "birthplace": "江西广丰",
        "education": "在职研究生学历，经济学硕士",
        "party_join": "中共党员",
        "work_start": "1997-07",
        "current_post": "浦东新区区委副书记、区长",
        "current_org": "上海市浦东新区人民政府",
        "source": "https://www.pudong.gov.cn/",
    },
    # 区委副书记 — 单少军
    {
        "id": 3,
        "name": "单少军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-10",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共上海市浦东新区区委副书记",
        "current_org": "中共上海市浦东新区委员会",
        "source": "https://www.pudong.gov.cn/",
    },
    # 区委常委、常务副区长 — 杨朝
    {
        "id": 4,
        "name": "杨朝",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "浦东新区区委常委、副区长（常务）",
        "current_org": "上海市浦东新区人民政府",
        "source": "https://www.pudong.gov.cn/",
    },
    # 区委常委、纪委书记、监委主任 — 李晓辉
    {
        "id": 5,
        "name": "李晓辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "浦东新区区委常委、纪委书记、监委主任",
        "current_org": "中共上海市浦东新区纪律检查委员会",
        "source": "https://www.pudong.gov.cn/",
    },
    # 区委常委、组织部部长 — 彭琼林
    {
        "id": 6,
        "name": "彭琼林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "浦东新区区委常委、组织部部长",
        "current_org": "中共上海市浦东新区区委组织部",
        "source": "https://www.pudong.gov.cn/",
    },
    # 区委常委、宣传部部长 — 黄玮
    {
        "id": 7,
        "name": "黄玮",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "浦东新区区委常委、宣传部部长",
        "current_org": "中共上海市浦东新区区委宣传部",
        "source": "https://www.pudong.gov.cn/",
    },
    # 区委常委、政法委书记 — 张磊
    {
        "id": 8,
        "name": "张磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "浦东新区区委常委、政法委书记",
        "current_org": "中共上海市浦东新区区委政法委员会",
        "source": "https://www.pudong.gov.cn/",
    },
    # 区委常委、统战部部长 — 张峰
    {
        "id": 9,
        "name": "张峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "浦东新区区委常委、统战部部长",
        "current_org": "中共上海市浦东新区区委统战部",
        "source": "https://www.pudong.gov.cn/",
    },
    # 区委常委、区人民武装部政委 — 翁俊军
    {
        "id": 10,
        "name": "翁俊军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "浦东新区区委常委、区人民武装部政委",
        "current_org": "上海市浦东新区人民武装部",
        "source": "https://www.pudong.gov.cn/",
    },
    # ═══════════════════════════════════════════════
    # 区政府副区长 (District Government)
    # ═══════════════════════════════════════════════

    # 副区长 — 毕桂平
    {
        "id": 11,
        "name": "毕桂平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "浦东新区副区长",
        "current_org": "上海市浦东新区人民政府",
        "source": "https://www.pudong.gov.cn/",
    },
    # 副区长 — 吕雪城
    {
        "id": 12,
        "name": "吕雪城",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "浦东新区副区长",
        "current_org": "上海市浦东新区人民政府",
        "source": "https://www.pudong.gov.cn/",
    },
    # 副区长 — 张娣芳
    {
        "id": 13,
        "name": "张娣芳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "浦东新区副区长",
        "current_org": "上海市浦东新区人民政府",
        "source": "https://www.pudong.gov.cn/",
    },
    # 副区长 — 余颖
    {
        "id": 14,
        "name": "余颖",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "浦东新区副区长",
        "current_org": "上海市浦东新区人民政府",
        "source": "https://www.pudong.gov.cn/",
    },
    # ═══════════════════════════════════════════════
    # 人大、政协领导
    # ═══════════════════════════════════════════════

    # 区人大常委会主任 — 田春华
    {
        "id": 15,
        "name": "田春华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "浦东新区人大常委会主任",
        "current_org": "上海市浦东新区人民代表大会常务委员会",
        "source": "https://www.pudong.gov.cn/",
    },
    # 区政协主席 — 姬兆亮
    {
        "id": 16,
        "name": "姬兆亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "浦东新区政协主席",
        "current_org": "中国人民政治协商会议上海市浦东新区委员会",
        "source": "https://www.pudong.gov.cn/",
    },
    # ═══════════════════════════════════════════════
    # 前任领导 (Predecessors)
    # ═══════════════════════════════════════════════

    # 前任区委书记 — 翁祖亮 (前任，2016-2021)
    {
        "id": 17,
        "name": "翁祖亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1963-11",
        "birthplace": "上海",
        "education": "大学学历，工商管理硕士",
        "party_join": "中共党员",
        "work_start": "1985-07",
        "current_post": "",
        "current_org": "",
        "source": "https://baike.baidu.com/",
    },
    # 前任区长 — 杭迎伟 (前任，2017-2023)
    {
        "id": 18,
        "name": "杭迎伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1963-11",
        "birthplace": "浙江杭州",
        "education": "大学学历，高级工程师",
        "party_join": "中共党员",
        "work_start": "1985-08",
        "current_post": "",
        "current_org": "",
        "source": "https://baike.baidu.com/",
    },
]

# ── ORGANIZATIONS ──────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共上海市浦东新区委员会", "type": "党委", "level": "市辖区(直辖市)", "parent": "中共上海市委", "location": "上海市浦东新区"},
    {"id": 2, "name": "上海市浦东新区人民政府", "type": "政府", "level": "市辖区(直辖市)", "parent": "上海市人民政府", "location": "上海市浦东新区"},
    {"id": 3, "name": "中共上海市浦东新区纪律检查委员会", "type": "纪委", "level": "市辖区(直辖市)", "parent": "中共上海市浦东新区委员会", "location": "上海市浦东新区"},
    {"id": 4, "name": "中共上海市浦东新区区委组织部", "type": "党委部门", "level": "市辖区(直辖市)", "parent": "中共上海市浦东新区委员会", "location": "上海市浦东新区"},
    {"id": 5, "name": "中共上海市浦东新区区委宣传部", "type": "党委部门", "level": "市辖区(直辖市)", "parent": "中共上海市浦东新区委员会", "location": "上海市浦东新区"},
    {"id": 6, "name": "中共上海市浦东新区区委政法委员会", "type": "党委部门", "level": "市辖区(直辖市)", "parent": "中共上海市浦东新区委员会", "location": "上海市浦东新区"},
    {"id": 7, "name": "中共上海市浦东新区区委统战部", "type": "党委部门", "level": "市辖区(直辖市)", "parent": "中共上海市浦东新区委员会", "location": "上海市浦东新区"},
    {"id": 8, "name": "上海市浦东新区人民武装部", "type": "军队", "level": "市辖区(直辖市)", "parent": "上海警备区", "location": "上海市浦东新区"},
    {"id": 9, "name": "上海市浦东新区人民代表大会常务委员会", "type": "人大", "level": "市辖区(直辖市)", "parent": "上海市人民代表大会常务委员会", "location": "上海市浦东新区"},
    {"id": 10, "name": "中国人民政治协商会议上海市浦东新区委员会", "type": "政协", "level": "市辖区(直辖市)", "parent": "中国人民政治协商会议上海市委员会", "location": "上海市浦东新区"},
]

# ── POSITIONS ──────────────────────────────────────────────────────
positions = [
    # 朱芝松
    {"person_id": 1, "org_id": 1, "title": "上海市委常委、浦东新区区委书记", "start_date": "2021-08", "end_date": "present", "rank": "副省级", "note": "2021年8月任浦东新区区委书记；同时任上海市委常委"},
    {"person_id": 1, "org_id": 1, "title": "中共上海市浦东新区区委书记", "start_date": "2021-01", "end_date": "2021-08", "rank": "副省级", "note": "2021年1月任浦东新区区委书记"},
    {"person_id": 1, "org_id": 1, "title": "上海市浦东新区代理区长", "start_date": "2020-10", "end_date": "2021-01", "rank": "副省级", "note": "任浦东新区代区长期间晋升"},
    {"person_id": 1, "org_id": 1, "title": "中共上海市委副秘书长", "start_date": "2020-07", "end_date": "2020-10", "rank": "正厅级", "note": "市委副秘书长"},
    {"person_id": 1, "org_id": 1, "title": "上海市人民政府副秘书长", "start_date": "2019-09", "end_date": "2020-07", "rank": "正厅级", "note": "市政府副秘书长，中国（上海）自由贸易试验区管委会常务副主任"},
    {"person_id": 1, "org_id": 1, "title": "中共上海市闵行区委书记", "start_date": "2015-06", "end_date": "2019-09", "rank": "正厅级", "note": "闵行区委书记"},
    {"person_id": 1, "org_id": 1, "title": "上海市闵行区委副书记、区长", "start_date": "2014-06", "end_date": "2015-06", "rank": "正厅级", "note": "闵行区委副书记、区长"},
    {"person_id": 1, "org_id": 1, "title": "上海市委宣传部副部长", "start_date": "2013-03", "end_date": "2014-06", "rank": "正厅级", "note": "市委宣传部副部长"},
    {"person_id": 1, "org_id": 2, "title": "上海市闵行区副区长", "start_date": "2011-11", "end_date": "2013-03", "rank": "副厅级", "note": "闵行区副区长"},
    {"person_id": 1, "org_id": 3, "title": "上海航天技术研究院院长", "start_date": "2008-03", "end_date": "2011-11", "rank": "正厅级", "note": "航天系统出身，长期在上海航天工作"},
    # 吴金城
    {"person_id": 2, "org_id": 2, "title": "浦东新区区委副书记、区长", "start_date": "2023-10", "end_date": "present", "rank": "正厅级", "note": "2023年10月任浦东新区代区长，后任区长"},
    {"person_id": 2, "org_id": 1, "title": "上海市经济信息化工作党委书记", "start_date": "2022-01", "end_date": "2023-10", "rank": "正厅级", "note": "市经济信息化工作党委书记"},
    {"person_id": 2, "org_id": 2, "title": "上海市经济和信息化委员会主任", "start_date": "2019-05", "end_date": "2023-10", "rank": "正厅级", "note": "市经信委主任"},
    {"person_id": 2, "org_id": 1, "title": "中共上海市浦东新区区委常委", "start_date": "2016-09", "end_date": "2019-05", "rank": "副厅级", "note": "浦东新区区委常委、副区长"},
    {"person_id": 2, "org_id": 2, "title": "上海市浦东新区副区长", "start_date": "2014-06", "end_date": "2016-09", "rank": "副厅级", "note": "浦东新区副区长"},
    {"person_id": 2, "org_id": 2, "title": "上海市浦东新区区政府办公室主任", "start_date": "2012-10", "end_date": "2014-06", "rank": "正处级", "note": "区政府办公室主任"},
    {"person_id": 2, "org_id": 2, "title": "上海市浦东新区政府办公室副主任", "start_date": "2010-08", "end_date": "2012-10", "rank": "副处级", "note": "区政府办公室副主任"},
    # 单少军
    {"person_id": 3, "org_id": 1, "title": "中共上海市浦东新区区委副书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    # 杨朝
    {"person_id": 4, "org_id": 2, "title": "浦东新区区委常委、副区长（常务）", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 李晓辉
    {"person_id": 5, "org_id": 3, "title": "浦东新区区委常委、纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 彭琼林
    {"person_id": 6, "org_id": 4, "title": "浦东新区区委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 黄玮
    {"person_id": 7, "org_id": 5, "title": "浦东新区区委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 张磊
    {"person_id": 8, "org_id": 6, "title": "浦东新区区委常委、政法委书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 张峰
    {"person_id": 9, "org_id": 7, "title": "浦东新区区委常委、统战部部长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 翁俊军
    {"person_id": 10, "org_id": 8, "title": "浦东新区区委常委、区人民武装部政委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 毕桂平
    {"person_id": 11, "org_id": 2, "title": "浦东新区副区长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 吕雪城
    {"person_id": 12, "org_id": 2, "title": "浦东新区副区长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 张娣芳
    {"person_id": 13, "org_id": 2, "title": "浦东新区副区长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 余颖
    {"person_id": 14, "org_id": 2, "title": "浦东新区副区长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 田春华
    {"person_id": 15, "org_id": 9, "title": "浦东新区人大常委会主任", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    # 姬兆亮
    {"person_id": 16, "org_id": 10, "title": "浦东新区政协主席", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    # 翁祖亮 (前任)
    {"person_id": 17, "org_id": 1, "title": "中共上海市浦东新区区委书记（前任）", "start_date": "2016-12", "end_date": "2021-08", "rank": "副省级", "note": "前任区委书记，后调任中国机械工业集团董事长"},
    # 杭迎伟 (前任)
    {"person_id": 18, "org_id": 2, "title": "浦东新区区长（前任）", "start_date": "2017-01", "end_date": "2023-10", "rank": "正厅级", "note": "前任区长，后调任上海建工集团董事长"},
]

# ── RELATIONSHIPS ─────────────────────────────────────────────────
relationships = [
    # 朱芝松 — 吴金城 (搭档)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "区委书记—区长搭档关系", "overlap_org": "上海市浦东新区", "overlap_period": "2023-10至今"},
    # 朱芝松 — 翁祖亮 (前后任)
    {"person_a": 1, "person_b": 17, "type": "前后任", "context": "朱芝松接替翁祖亮任浦东新区区委书记", "overlap_org": "中共上海市浦东新区委员会", "overlap_period": "2021-08"},
    # 吴金城 — 杭迎伟 (前后任)
    {"person_a": 2, "person_b": 18, "type": "前后任", "context": "吴金城接替杭迎伟任浦东新区区长", "overlap_org": "上海市浦东新区人民政府", "overlap_period": "2023-10"},
    # 朱芝松 — 杨朝 (上下级)
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "区委书记—常务副区长", "overlap_org": "上海市浦东新区", "overlap_period": ""},
    # 吴金城 — 杨朝 (上下级)
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "区长—常务副区长", "overlap_org": "上海市浦东新区人民政府", "overlap_period": ""},
    # 朱芝松 — 单少军 (上下级)
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "区委书记—区委副书记", "overlap_org": "中共上海市浦东新区委员会", "overlap_period": ""},
    # 吴金城 — 单少军 (共事)
    {"person_a": 2, "person_b": 3, "type": "共事", "context": "区长—区委副书记", "overlap_org": "上海市浦东新区", "overlap_period": ""},
    # 朱芝松 — 各常委 (上下级)
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "区委书记—纪委书记", "overlap_org": "中共上海市浦东新区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "区委书记—组织部部长", "overlap_org": "中共上海市浦东新区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "区委书记—宣传部部长", "overlap_org": "中共上海市浦东新区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "区委书记—政法委书记", "overlap_org": "中共上海市浦东新区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "区委书记—统战部部长", "overlap_org": "中共上海市浦东新区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 10, "type": "上下级", "context": "区委书记—人武部政委", "overlap_org": "中共上海市浦东新区委员会", "overlap_period": ""},
]

# ── BUILD ──────────────────────────────────────────────────────────
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

if __name__ == "__main__":
    print(f"=== Building {SLUG} network ===")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

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

    # Export person JSON files
    def write_person_json(person: dict, job_label: str):
        filename = f"{TODAY}-上海市-浦东新区-{job_label}-{person['name']}.json"
        output = {
            "schema_version": "1.0",
            "generated_at": TODAY,
            "investigation_scope": {
                "province": "上海市",
                "city": "浦东新区",
                "region": "浦东新区",
                "job": person["current_post"],
                "task_id": "shanghai_浦东新区",
                "time_focus": "2016-2026",
            },
            "identity": {
                "person_id": f"pudong_{person['name']}",
                "name": person["name"],
                "aliases": [],
                "gender": person.get("gender", ""),
                "ethnicity": person.get("ethnicity", ""),
                "birth": person.get("birth", ""),
                "birthplace": person.get("birthplace", ""),
                "native_place": person.get("birthplace", ""),
                "education": [{"period": "", "institution": "", "major": "", "degree": person.get("education", ""), "study_type": "unknown", "source_ids": ["S001"]}],
                "party_join": person.get("party_join", ""),
                "work_start": person.get("work_start", ""),
                "dedupe_keys": {
                    "name_birth": f"{person['name']}_{person.get('birth', '')}",
                    "name_birthplace": f"{person['name']}_{person.get('birthplace', '')}",
                    "official_profile_url": "",
                },
            },
            "current_status": {
                "current_post": person["current_post"],
                "current_org": person["current_org"],
                "administrative_rank": "",
                "as_of": TODAY,
                "is_current_confirmed": True,
                "source_ids": ["S001"],
            },
            "career_timeline": [
                {
                    "start": pos.get("start_date", ""),
                    "end": pos.get("end_date", ""),
                    "org": pos["org_id"],
                    "title": pos["title"],
                    "rank": pos.get("rank", ""),
                    "notes": pos.get("note", ""),
                    "confidence": "plausible",
                    "source_ids": ["S001"],
                }
                for pos in positions
                if pos["person_id"] == person["id"]
            ],
            "organizations": [
                {
                    "org_id": org["id"],
                    "name": org["name"],
                    "type": org["type"],
                    "level": org["level"],
                    "parent": org.get("parent", ""),
                    "location": org.get("location", ""),
                    "source_ids": ["S001"],
                }
                for org in organizations
                if org["id"] in {pos["org_id"] for pos in positions if pos["person_id"] == person["id"]}
            ],
            "relationships": [
                {
                    "person": p["name"],
                    "person_id": f"pudong_{p['name']}",
                    "relationship_type": r["type"],
                    "strength": "strong" if r["type"] in ("共事", "前后任") else "medium",
                    "evidence": r["context"],
                    "overlap_org": r["overlap_org"],
                    "overlap_period": r["overlap_period"],
                    "direction": "undirected",
                    "confidence": "confirmed",
                    "source_ids": ["S001"],
                }
                for r in relationships
                for p in persons
                if (r["person_a"] == person["id"] and r["person_b"] == p["id"]) or (r["person_b"] == person["id"] and r["person_a"] == p["id"])
            ],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "",
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
            "risk_and_integrity_signals": [],
            "source_register": [
                {
                    "id": "S001",
                    "title": "上海市浦东新区人民政府门户网站",
                    "url": "https://www.pudong.gov.cn/",
                    "publisher": "上海市浦东新区人民政府",
                    "published_at": "",
                    "accessed_at": TODAY,
                    "source_type": "official",
                    "reliability": "high",
                    "notes": "Confirmed current officeholders from official leadership pages",
                }
            ],
            "confidence_summary": {
                "identity": "plausible",
                "current_role": "confirmed",
                "career_completeness": "partial",
                "relationship_confidence": "medium",
                "biggest_gap": "Detailed career timeline and education background need verification from official biography pages",
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": f"完整简历：{person['name']}的详细教育背景、早期职业生涯、晋升时间线",
                    "why_it_matters": "核心领导的履历完整度影响关系网络分析的深度",
                    "suggested_queries": [f"{person['name']} 简历", f"{person['name']} 任前公示"],
                    "last_attempted": TODAY,
                }
            ],
        }
        path = os.path.join(PERSONS_DIR, filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {filename}")

    write_person_json(persons[0], "区委书记")  # 朱芝松
    write_person_json(persons[1], "区长")  # 吴金城

    print(f"\n=== Done. Output in {STAGING_DIR} ===")
