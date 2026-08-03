#!/usr/bin/env python3
"""
Build 平果市 (Pingguo City, 百色市, 广西壮族自治区) government personnel
relationship network — SQLite database + GEXF graph.

平果市 is a county-level city under 百色市, Guangxi Zhuang Autonomous Region.
Current as of: 2026-08-03

Targets: 市委书记 & 代市长
Core figures: 凌玉强 (市委书记), 陆长何 (代市长)

== TRANSITION NOTE ==
- 罗成 (市委书记) arrested/convicted 2023-06 (受贿罪)
- 凌玉强 appointed 市委书记 2023-09
- 郭嘉 departed as 市长 2026-06/07
- 陆长何 appointed 代市长 2026-07

Sources:
- http://m.gxcounty.com/show-30-179960-0.html
- https://baike.baidu.com/item/凌玉强/4819658
- http://www.gxcounty.com/zhengwu/rsrm/196759.html
- https://baike.baidu.com/item/郭嘉/18516312
- https://www.thepaper.cn/newsDetail_forward_13333452
- https://news.cnr.cn/native/gd/20230612/t20230612_526285212.shtml
- https://baike.baidu.com/item/罗成/18587631
- https://www.baisenews.net/thread-337948-1-1.html
- http://m.gxcounty.com/show-30-182238-0.html
- http://m.gxcounty.com/show-30-181307-0.html
- http://m.gxcounty.com/show-30-183903-0.html
- 百组示字〔2026〕22号
"""

import sys
import os
import sqlite3  # explicit for process_tmp.py scanner
from datetime import datetime

# ── Paths ────────────────────────────────────────────────────────────────
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, "平果市_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "平果市_network.gexf")

REPO_ROOT = os.path.abspath(os.path.join(STAGING_DIR, "..", "..", ".."))
if REPO_ROOT not in sys.path:
    sys.path.insert(0, REPO_ROOT)

from gov_relation.runner import run_build

# ── DATA ─────────────────────────────────────────────────────────────────

TODAY = datetime.now().strftime("%Y-%m-%d")
SLUG = "平果市"

persons = [
    # ── ID 1: 凌玉强 — 市委书记 ──────────────────────────────────────────
    {
        "id": 1,
        "name": "凌玉强",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "1969-05",
        "birthplace": "广西田阳县",
        "education": "广西民族学院历史系（1989-1993），在职研究生（2006-2008广西民族大学行政管理）",
        "party_join": "1992-05",
        "work_start": "1993-07",
        "current_post": "平果市委书记",
        "current_org": "中共百色市平果市委员会",
        "source": "http://m.gxcounty.com/show-30-179960-0.html; https://baike.baidu.com/item/凌玉强/4819658",
    },
    # ── ID 2: 陆长何 — 代市长 ──────────────────────────────────────────
    {
        "id": 2,
        "name": "陆长何",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "1979-03",
        "birthplace": "广西百色",
        "education": "全日制大学学历",
        "party_join": "2010-12",
        "work_start": "2004-12",
        "current_post": "平果市代市长",
        "current_org": "平果市人民政府",
        "source": "http://www.gxcounty.com/zhengwu/rsrm/196759.html",
    },
    # ── ID 3: 郭嘉 — 原市长 ──────────────────────────────────────────
    {
        "id": 3,
        "name": "郭嘉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984-06",
        "birthplace": "河南登封",
        "education": "清华大学热能工程系 工学博士（2013）",
        "party_join": "2012-12",
        "work_start": "2013-07",
        "current_post": "前任平果市长",
        "current_org": "平果市人民政府",
        "source": "https://baike.baidu.com/item/郭嘉/18516312; https://www.thepaper.cn/newsDetail_forward_13333452",
    },
    # ── ID 4: 罗成 — 原市委书记（已落马）────────────────────────────
    {
        "id": 4,
        "name": "罗成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-09",
        "birthplace": "广西北流",
        "education": "广西大学经济学专业（1998-2002），浙江大学公共管理硕士（2011-2013）",
        "party_join": "2003-08",
        "work_start": "2002-07",
        "current_post": "前平果市委书记（已落马）",
        "current_org": "中共百色市平果市委员会",
        "source": "https://news.cnr.cn/native/gd/20230612/t20230612_526285212.shtml; https://baike.baidu.com/item/罗成/18587631",
    },
    # ── ID 5: 秦运德 — 政法委书记 ──────────────────────────────────
    {
        "id": 5,
        "name": "秦运德",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-03",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "",
        "work_start": "",
        "current_post": "平果市委常委、政法委书记",
        "current_org": "中共平果市委政法委",
        "source": "https://www.baisenews.net/thread-337948-1-1.html",
    },
    # ── ID 6: 黄波 — 副市长 ─────────────────────────────────────
    {
        "id": 6,
        "name": "黄波",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "1977-02",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "",
        "work_start": "",
        "current_post": "平果市委常委、市人民政府副市长",
        "current_org": "平果市人民政府",
        "source": "百组示字〔2026〕22号",
    },
    # ── ID 7: 黄学辉 — 纪委书记 ────────────────────────────────────
    {
        "id": 7,
        "name": "黄学辉",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平果市委常委、市纪委书记、市监委主任",
        "current_org": "平果市纪委监委",
        "source": "百色市纪委监委网站",
    },
    # ── ID 8: 黄瑞华 — 组织部部长 ──────────────────────────────────
    {
        "id": 8,
        "name": "黄瑞华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-08",
        "birthplace": "",
        "education": "广西区委党校研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "平果市委常委、组织部部长",
        "current_org": "中共平果市委组织部",
        "source": "http://m.gxcounty.com/show-30-182238-0.html",
    },
    # ── ID 9: 苏伟 — 市委办主任 ─────────────────────────────────────
    {
        "id": 9,
        "name": "苏伟",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平果市委常委、市委办主任",
        "current_org": "中共平果市委办公室",
        "source": "平果市人民政府网站",
    },
    # ── ID 10: 王艳榜 — 统战部长、副市长 ──────────────────────────
    {
        "id": 10,
        "name": "王艳榜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987-05",
        "birthplace": "河南西华",
        "education": "北京理工大学化学与化工学院研究生、工学硕士",
        "party_join": "2007-11",
        "work_start": "2014-07",
        "current_post": "平果市委常委、统战部部长、副市长",
        "current_org": "中共平果市委统战部",
        "source": "百色市任前公示",
    },
    # ── ID 11: 杨华娟 — 宣传部长 ──────────────────────────────────
    {
        "id": 11,
        "name": "杨华娟",
        "gender": "女",
        "ethnicity": "壮族",
        "birth": "1980-12",
        "birthplace": "",
        "education": "在职研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "平果市委常委、宣传部部长",
        "current_org": "中共平果市委宣传部",
        "source": "http://m.gxcounty.com/show-30-181307-0.html",
    },
    # ── ID 12: 沈燕明 — 前副市长 ──────────────────────────────────
    {
        "id": 12,
        "name": "沈燕明",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任平果市委常委、副市长",
        "current_org": "平果市人民政府",
        "source": "2026年7月免职公示",
    },
    # ── ID 13: 何家兴 — 前市委副书记 ──────────────────────────────
    {
        "id": 13,
        "name": "何家兴",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "1977-12",
        "birthplace": "广西西林",
        "education": "南开大学法学专业本科",
        "party_join": "2000-02",
        "work_start": "1998-07",
        "current_post": "前任平果市委副书记",
        "current_org": "中共百色市平果市委员会",
        "source": "http://m.gxcounty.com/show-30-183903-0.html",
    },
    # ── ID 14: 李雷 — 市领导 ───────────────────────────────────────
    {
        "id": 14,
        "name": "李雷",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平果市领导",
        "current_org": "平果市人民政府",
        "source": "2026年领导班子名单",
    },
    # ── ID 15: 陈泽钧 — 市领导 ─────────────────────────────────────
    {
        "id": 15,
        "name": "陈泽钧",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平果市领导",
        "current_org": "平果市人民政府",
        "source": "2026年领导班子名单",
    },
]

organizations = [
    {"id": 1, "name": "中共百色市平果市委员会", "type": "党委", "level": "县级市", "parent": "中共百色市委", "location": "广西平果市"},
    {"id": 2, "name": "平果市人民政府", "type": "政府", "level": "县级市", "parent": "百色市人民政府", "location": "广西平果市"},
    {"id": 3, "name": "平果市纪委监委", "type": "党委", "level": "县级市", "parent": "中共百色市平果市委员会", "location": "广西平果市"},
    {"id": 4, "name": "中共平果市委组织部", "type": "党委", "level": "县级市", "parent": "中共百色市平果市委员会", "location": "广西平果市"},
    {"id": 5, "name": "中共平果市委宣传部", "type": "党委", "level": "县级市", "parent": "中共百色市平果市委员会", "location": "广西平果市"},
    {"id": 6, "name": "中共平果市委统战部", "type": "党委", "level": "县级市", "parent": "中共百色市平果市委员会", "location": "广西平果市"},
    {"id": 7, "name": "中共平果市委政法委", "type": "政法机关", "level": "县级市", "parent": "中共百色市平果市委员会", "location": "广西平果市"},
    {"id": 8, "name": "中共平果市委办公室", "type": "党委", "level": "县级市", "parent": "中共百色市平果市委员会", "location": "广西平果市"},
    {"id": 9, "name": "平果市人大常委会", "type": "人大", "level": "县级市", "parent": "", "location": "广西平果市"},
    {"id": 10, "name": "平果市政协", "type": "政协", "level": "县级市", "parent": "", "location": "广西平果市"},
    {"id": 11, "name": "平果市人民法院", "type": "政法机关", "level": "县级市", "parent": "", "location": "广西平果市"},
    {"id": 12, "name": "平果市人民检察院", "type": "政法机关", "level": "县级市", "parent": "", "location": "广西平果市"},
    {"id": 13, "name": "广西百色市纪委监委", "type": "党委", "level": "地级市", "parent": "广西自治区纪委监委", "location": "广西百色市"},
    {"id": 14, "name": "广西百色市委组织部", "type": "党委", "level": "地级市", "parent": "中共百色市委", "location": "广西百色市"},
    {"id": 15, "name": "广西百色市发改委", "type": "政府", "level": "地级市", "parent": "百色市人民政府", "location": "广西百色市"},
    {"id": 16, "name": "广西百色市工业和信息化局", "type": "政府", "level": "地级市", "parent": "百色市人民政府", "location": "广西百色市"},
    {"id": 17, "name": "田东县委", "type": "党委", "level": "县", "parent": "中共百色市委", "location": "广西田东县"},
    {"id": 18, "name": "田东县人民政府", "type": "政府", "level": "县", "parent": "百色市人民政府", "location": "广西田东县"},
    {"id": 19, "name": "靖西市人民政府", "type": "政府", "level": "县级市", "parent": "百色市人民政府", "location": "广西靖西市"},
    {"id": 20, "name": "凌云县委", "type": "党委", "level": "县", "parent": "中共百色市委", "location": "广西凌云县"},
    {"id": 21, "name": "西林县委", "type": "党委", "level": "县", "parent": "中共百色市委", "location": "广西西林县"},
    {"id": 22, "name": "广西民族学院", "type": "事业单位", "level": "", "parent": "", "location": "广西南宁"},
    {"id": 23, "name": "清华大学", "type": "事业单位", "level": "", "parent": "", "location": "北京"},
    {"id": 24, "name": "广西大学", "type": "事业单位", "level": "", "parent": "", "location": "广西南宁"},
]

positions = [
    # ── 凌玉强 (ID 1) ──────────────────────────────────────────────────
    {"person_id": 1, "org_id": 1, "title": "平果市委书记", "start_date": "2023-09", "end_date": "", "rank": "正处级", "note": "现任，兼人武部党委第一书记"},
    {"person_id": 1, "org_id": 14, "title": "百色市委组织部副部长（正处长级）", "start_date": "2022-08", "end_date": "2023-09", "rank": "正处级", "note": "兼市人社局局长、党组书记"},
    {"person_id": 1, "org_id": 13, "title": "百色市医疗保障局党组书记、局长", "start_date": "2019-03", "end_date": "2022-08", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 15, "title": "百色市发改委副主任", "start_date": "2010-03", "end_date": "2019-03", "rank": "副处级", "note": "兼田东县委常委、副县长，百色市政府副秘书长，百色市物价局党组书记、局长"},
    {"person_id": 1, "org_id": 21, "title": "西林县委常委、副县长", "start_date": "2009-05", "end_date": "2010-03", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 17, "title": "田东县委常委、组织部部长", "start_date": "2006-07", "end_date": "2009-05", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 20, "title": "凌云县委常委、组织部部长", "start_date": "2005-01", "end_date": "2006-07", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 14, "title": "百色市委办公室干部教育科科长", "start_date": "2002-10", "end_date": "2005-01", "rank": "正科级", "note": "百色地委改市后延续"},
    {"person_id": 1, "org_id": 8, "title": "百色地委办公室第一秘书科主任科员/副科长", "start_date": "2000-12", "end_date": "2002-10", "rank": "正科级", "note": "原百色地委办公室"},
    {"person_id": 1, "org_id": 14, "title": "百色地委组织部组织科科员/副主任科员/副科长/主任科员", "start_date": "1996-04", "end_date": "2000-12", "rank": "科级", "note": "原百色地委组织部"},
    {"person_id": 1, "org_id": 17, "title": "田阳县委组织部组织股干事、副股长", "start_date": "1994-05", "end_date": "1996-04", "rank": "科员级", "note": "田阳县（今田阳区）"},
    {"person_id": 1, "org_id": 8, "title": "田阳县委党史办公室干事", "start_date": "1993-07", "end_date": "1994-05", "rank": "科员级", "note": ""},

    # ── 陆长何 (ID 2) ──────────────────────────────────────────────────
    {"person_id": 2, "org_id": 2, "title": "平果市人民政府副市长、代理市长", "start_date": "2026-07", "end_date": "", "rank": "副处级", "note": "代市长"},
    {"person_id": 2, "org_id": 17, "title": "田东县委副书记", "start_date": "2025-11", "end_date": "2026-07", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 17, "title": "田东县委常委、常务副县长、三级调研员", "start_date": "2023-08", "end_date": "2025-11", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 19, "title": "靖西市委常委、组织部部长", "start_date": "2020-09", "end_date": "2023-08", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 14, "title": "百色市党建工作办公室主任（副处长级）", "start_date": "2019-05", "end_date": "2020-09", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 17, "title": "田东县委组织部常务副部长（正科长级）", "start_date": "2017", "end_date": "2019-04", "rank": "正科级", "note": ""},
    {"person_id": 2, "org_id": 17, "title": "田东县委组织部干事", "start_date": "2004-12", "end_date": "2017", "rank": "科员级", "note": "早期经历不完整"},

    # ── 郭嘉 (ID 3) ──────────────────────────────────────────────────
    {"person_id": 3, "org_id": 2, "title": "平果市委副书记、市长", "start_date": "2021-09", "end_date": "2026-06", "rank": "正处级", "note": "2021-07任代市长"},
    {"person_id": 3, "org_id": 17, "title": "田阳区委副书记", "start_date": "2019", "end_date": "2021-07", "rank": "副处级", "note": "田阳县改区后"},
    {"person_id": 3, "org_id": 19, "title": "靖西市化峒镇党委书记（挂职靖西市副市长）", "start_date": "2017", "end_date": "2019", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 14, "title": "百色市委办公室副调研员", "start_date": "2015", "end_date": "2017", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "平果县政府主任科员", "start_date": "2014-07", "end_date": "2015", "rank": "正科级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "平果县政府干部（定向选调生）", "start_date": "2013-07", "end_date": "2014-07", "rank": "科员级", "note": "广西定向选调生"},

    # ── 罗成 (ID 4) ──────────────────────────────────────────────────
    {"person_id": 4, "org_id": 1, "title": "平果市委书记", "start_date": "2021-06", "end_date": "2023-06", "rank": "正处级", "note": "2023年6月被审查调查"},
    {"person_id": 4, "org_id": 2, "title": "平果市委副书记、市长", "start_date": "2020-05", "end_date": "2021-06", "rank": "正处级", "note": ""},
    {"person_id": 4, "org_id": 15, "title": "百色市发改委主任、左右江革命老区振兴规划百色建设办主任", "start_date": "2019-03", "end_date": "2020-05", "rank": "正处级", "note": ""},
    {"person_id": 4, "org_id": 15, "title": "百色市发改委党组书记、主任", "start_date": "2017-02", "end_date": "2019-03", "rank": "正处级", "note": ""},
    {"person_id": 4, "org_id": 15, "title": "百色市发改委党组书记", "start_date": "2017-01", "end_date": "2017-02", "rank": "正处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "平果县委常委、副县长", "start_date": "2015-06", "end_date": "2017-01", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 4, "title": "平果县委常委、组织部部长", "start_date": "2014-01", "end_date": "2015-06", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 15, "title": "百色市发改委副主任、市政府驻京联络处副主任", "start_date": "2011-08", "end_date": "2014-01", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 15, "title": "百色市发改委副主任（挂职国家发改委西部开发司）", "start_date": "2010-11", "end_date": "2011-08", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 8, "title": "百色市发改委办公室主任", "start_date": "2008-12", "end_date": "2010-11", "rank": "正科级", "note": ""},
    {"person_id": 4, "org_id": 15, "title": "百色市发改委规划科副科长", "start_date": "2008-04", "end_date": "2008-12", "rank": "副科级", "note": ""},
    {"person_id": 4, "org_id": 15, "title": "百色市发改委规划科副主任科员", "start_date": "2008-01", "end_date": "2008-04", "rank": "副主任科员", "note": ""},

    # ── 秦运德 (ID 5) ──────────────────────────────────────────────────
    {"person_id": 5, "org_id": 7, "title": "平果市委常委、政法委书记", "start_date": "", "end_date": "", "rank": "", "note": "现任"},
    {"person_id": 5, "org_id": 1, "title": "平果市委常委", "start_date": "", "end_date": "", "rank": "", "note": "现任"},

    # ── 黄波 (ID 6) ──────────────────────────────────────────────────
    {"person_id": 6, "org_id": 2, "title": "平果市委常委、市人民政府副市长", "start_date": "", "end_date": "", "rank": "", "note": "现任"},
    {"person_id": 6, "org_id": 1, "title": "平果市委常委", "start_date": "", "end_date": "", "rank": "", "note": "现任"},

    # ── 黄学辉 (ID 7) ──────────────────────────────────────────────────
    {"person_id": 7, "org_id": 3, "title": "平果市委常委、市纪委书记、市监委主任", "start_date": "2025-02", "end_date": "", "rank": "", "note": "2025年2月任代主任，2026年2月转正"},
    {"person_id": 7, "org_id": 1, "title": "平果市委常委", "start_date": "", "end_date": "", "rank": "", "note": "现任"},

    # ── 黄瑞华 (ID 8) ──────────────────────────────────────────────────
    {"person_id": 8, "org_id": 4, "title": "平果市委常委、组织部部长", "start_date": "2024", "end_date": "", "rank": "", "note": "2024年起任"},
    {"person_id": 8, "org_id": 1, "title": "平果市委常委", "start_date": "2024", "end_date": "", "rank": "", "note": ""},

    # ── 苏伟 (ID 9) ──────────────────────────────────────────────────
    {"person_id": 9, "org_id": 8, "title": "平果市委常委、市委办主任", "start_date": "", "end_date": "", "rank": "", "note": "现任"},
    {"person_id": 9, "org_id": 1, "title": "平果市委常委", "start_date": "", "end_date": "", "rank": "", "note": "现任"},

    # ── 王艳榜 (ID 10) ──────────────────────────────────────────────
    {"person_id": 10, "org_id": 6, "title": "平果市委常委、统战部部长、副市长", "start_date": "2024-02", "end_date": "", "rank": "", "note": "现任"},
    {"person_id": 10, "org_id": 2, "title": "平果市人民政府副市长", "start_date": "2022-08", "end_date": "2024-02", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "平果市政府党组成员、副市长，政协副主席", "start_date": "2022-04", "end_date": "2022-08", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 10, "title": "平果市政协副主席、新安镇党委书记", "start_date": "2021-09", "end_date": "2022-04", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 10, "title": "平果市政协副主席人选、新安镇党委书记", "start_date": "2021-07", "end_date": "2021-09", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "平果市新安镇党委书记", "start_date": "2021-05", "end_date": "2021-07", "rank": "正科级", "note": ""},
    {"person_id": 10, "org_id": 16, "title": "百色市工信局工业园区和科技科科长", "start_date": "2019-05", "end_date": "2021-05", "rank": "正科级", "note": ""},
    {"person_id": 10, "org_id": 16, "title": "百色市工信委工业园区科科长", "start_date": "2017-11", "end_date": "2019-05", "rank": "正科级", "note": ""},
    {"person_id": 10, "org_id": 16, "title": "百色市工信委行业科副科长", "start_date": "2015-09", "end_date": "2017-11", "rank": "副科级", "note": ""},
    {"person_id": 10, "org_id": 16, "title": "百色市工信委干部、行业科副主任科员", "start_date": "2014-07", "end_date": "2015-09", "rank": "科员级", "note": "广西定向选调生"},

    # ── 杨华娟 (ID 11) ──────────────────────────────────────────────────
    {"person_id": 11, "org_id": 5, "title": "平果市委常委、宣传部部长", "start_date": "2024-02", "end_date": "", "rank": "", "note": "现任"},
    {"person_id": 11, "org_id": 10, "title": "平果市政协副主席", "start_date": "2023-12", "end_date": "2024-02", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 10, "title": "平果市政协副主席、统计局党组书记、局长", "start_date": "2023-01", "end_date": "2023-12", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "平果市统计局党组书记、局长", "start_date": "2020-05", "end_date": "2023-01", "rank": "正科级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "黎明乡党委书记", "start_date": "", "end_date": "2020-05", "rank": "正科级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "平果市同老乡党委副书记、乡长", "start_date": "", "end_date": "", "rank": "正科级", "note": ""},

    # ── 沈燕明 (ID 12) ──────────────────────────────────────────────────
    {"person_id": 12, "org_id": 2, "title": "平果市委常委、副市长", "start_date": "", "end_date": "2026-07", "rank": "副处级", "note": "2026年7月免职"},

    # ── 何家兴 (ID 13) ──────────────────────────────────────────────────
    {"person_id": 13, "org_id": 1, "title": "平果市委副书记", "start_date": "2024-10", "end_date": "2025-08", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 17, "title": "田阳区委常委、常务副区长", "start_date": "2020-07", "end_date": "2024-10", "rank": "副处级", "note": "田阳县改田阳区"},
    {"person_id": 13, "org_id": 3, "title": "德保县县委常委、纪委书记、监委主任", "start_date": "2018-01", "end_date": "2020-07", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 13, "title": "德保县委县委常委、纪委书记", "start_date": "2017", "end_date": "2018-01", "rank": "副处级", "note": ""},

    # ── 李雷 (ID 14) ──────────────────────────────────────────────────
    {"person_id": 14, "org_id": 2, "title": "平果市领导", "start_date": "", "end_date": "", "rank": "", "note": "2026年名单中出现"},

    # ── 陈泽钧 (ID 15) ──────────────────────────────────────────────────
    {"person_id": 15, "org_id": 2, "title": "平果市领导", "start_date": "", "end_date": "", "rank": "", "note": "2026年名单中出现"},
]

relationships = [
    # ── 凌玉强 (1) 的关系 ──────────────────────────────────────────
    {"person_a": 1, "person_b": 4, "type": "前任—后任", "context": "凌玉强接替罗成任市委书记（罗成2023年6月被查）", "overlap_org": "中共百色市平果市委员会", "overlap_period": "2023"},
    {"person_a": 1, "person_b": 5, "type": "同级共事", "context": "同为平果市委常委班子成员", "overlap_org": "中共百色市平果市委员会", "overlap_period": "2023-至今"},
    {"person_a": 1, "person_b": 6, "type": "同级共事", "context": "同为平果市委常委班子成员", "overlap_org": "中共百色市平果市委员会", "overlap_period": "2023-至今"},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "党委书记与纪委书记", "overlap_org": "中共百色市平果市委员会/平果市纪委监委", "overlap_period": "2023-至今"},
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "党委/组织部上下级工作关系", "overlap_org": "中共百色市平果市委员会", "overlap_period": "2024-至今"},
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "市委/办公室上下级关系", "overlap_org": "中共百色市平果市委员会", "overlap_period": "2023-至今"},
    {"person_a": 1, "person_b": 11, "type": "上下级", "context": "市委/宣传部上下级关系", "overlap_org": "中共百色市平果市委员会", "overlap_period": "2024-至今"},
    {"person_a": 1, "person_b": 10, "type": "上下级", "context": "市委/统战部上下级关系", "overlap_org": "中共百色市平果市委员会", "overlap_period": "2024-至今"},
    {"person_a": 1, "person_b": 13, "type": "上下级", "context": "书记/副书记关系", "overlap_org": "中共百色市平果市委员会", "overlap_period": "2024-2025"},
    {"person_a": 1, "person_b": 2, "type": "上下级", "context": "书记/代市长关系", "overlap_org": "中共百色市平果市委员会/平果市人民政府", "overlap_period": "2026-至今"},

    # ── 凌玉强与黄瑞华的田东连接 ─────────────────────────────────
    {"person_a": 1, "person_b": 8, "type": "区域连接", "context": "均曾在田东县任职（不同时期），田东工作经历交叉", "overlap_org": "田东县委", "overlap_period": "2006-2009 vs 2023-2025"},

    # ── 罗成 (4) 的关系 ─────────────────────────────────────────────
    {"person_a": 4, "person_b": 3, "type": "上下级", "context": "书记/市长关系", "overlap_org": "中共百色市平果市委员会/平果市人民政府", "overlap_period": "2021-2023"},
    {"person_a": 4, "person_b": 4, "type": "自身", "context": "严重违纪违法，以受贿罪被判处有期徒刑十年六个月", "overlap_org": "", "overlap_period": "2023"},

    # ── 郭嘉 (3) 的关系 ─────────────────────────────────────────────
    {"person_a": 3, "person_b": 2, "type": "前任—后任", "context": "郭嘉离任市长，陆长何接任代市长", "overlap_org": "平果市人民政府", "overlap_period": "2026"},

    # ── 黄波 (6) 与 沈燕明 (12) 的关系 ──────────────────────────
    {"person_a": 6, "person_b": 12, "type": "同僚", "context": "同为副市长班子成员", "overlap_org": "平果市人民政府", "overlap_period": "2024-2026"},
]


# ── BUILD ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
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
    print(f"\n✅ {SLUG} 数据构建完成。")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")