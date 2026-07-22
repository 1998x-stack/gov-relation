#!/usr/bin/env python3
"""
Build 郁南县 (Yunan County) government personnel network database and GEXF graph.

郁南县 is a county under 云浮市, 广东省.
Current leadership as of 2026-07-22:
- 张春海: 郁南县委书记 (former 县长, promoted ~2025 to secretary)
- 县长: 空缺（待更新） — 潘宁（县委常委、常务副县长）主持县政府日常工作
- 郑辉亮: 郁南县委副书记、政法委书记
- 邹飞祥: 挂任郁南县委副书记（省文旅厅下派）
Based on official sources from www.gdyunan.gov.cn leadership pages.
"""
import os
import sys
from datetime import datetime

# Use gov_relation runner if available, otherwise fallback to inline build
try:
    from gov_relation.runner import run_build
    from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
    USE_RUNNER = True
except ImportError:
    USE_RUNNER = False

BASE = os.path.dirname(os.path.abspath(__file__))
if "data/tmp" in BASE:
    REPO_ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
else:
    REPO_ROOT = BASE

today = datetime.now().strftime("%Y-%m-%d")

DB_REL = "data/database/郁南县_network.db"
GEXF_REL = "data/graph/郁南县_network.gexf"

DB_PATH = os.path.join(REPO_ROOT, DB_REL)
GEXF_PATH = os.path.join(REPO_ROOT, GEXF_REL)

# =========================================================================
# DATA
# =========================================================================

persons = [
    # ---- Core Leaders ----
    {
        "id": 1,
        "name": "张春海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-03",
        "birthplace": "广东开平",
        "education": "大学",
        "party_join": "1995-05",
        "work_start": "1996-07",
        "current_post": "郁南县委书记",
        "current_org": "中共郁南县委员会",
        "source": "郁南县人民政府网（www.gdyunan.gov.cn）— 县委书记简历页；1996年7月参加工作，1995年5月加入中国共产党，大学学历",
    },
    {
        "id": 2,
        "name": "潘宁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-06",
        "birthplace": "广东罗定",
        "education": "大学",
        "party_join": "1996-07",
        "work_start": "1995-08",
        "current_post": "郁南县委常委、副县长（常务）",
        "current_org": "郁南县人民政府",
        "source": "郁南县人民政府网 — 县委常委、副县长简历页；1995年8月参加工作，1996年7月加入中国共产党",
    },
    # ---- 县委副书记 ----
    {
        "id": 3,
        "name": "郑辉亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-02",
        "birthplace": "广东电白",
        "education": "大学",
        "party_join": "2002-12",
        "work_start": "2006-04",
        "current_post": "郁南县委副书记、政法委书记",
        "current_org": "中共郁南县委员会",
        "source": "郁南县人民政府网 — 县委副书记简历页；2006年4月参加工作，2002年12月加入中国共产党",
    },
    {
        "id": 4,
        "name": "邹飞祥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-04",
        "birthplace": "广东兴宁",
        "education": "研究生",
        "party_join": "2004-10",
        "work_start": "2001-07",
        "current_post": "挂任郁南县委副书记",
        "current_org": "中共郁南县委员会",
        "source": "郁南县人民政府网 — 县委副书记（挂任）简历页；广东省文化和旅游发展与保障中心副主任，挂任郁南县委副书记",
    },
    # ---- 县委常委 ----
    {
        "id": 5,
        "name": "陈荣南",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-06",
        "birthplace": "广东信宜",
        "education": "大学",
        "party_join": "1999-06",
        "work_start": "1999-08",
        "current_post": "郁南县委常委、办公室主任、宣传部部长",
        "current_org": "中共郁南县委员会",
        "source": "郁南县人民政府网 — 县委常委简历页；1999年8月参加工作，1999年6月加入中国共产党",
    },
    {
        "id": 6,
        "name": "何毅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-05",
        "birthplace": "广东云安",
        "education": "研究生",
        "party_join": "2002-06",
        "work_start": "2006-08",
        "current_post": "郁南县委常委",
        "current_org": "中共郁南县委员会",
        "source": "郁南县人民政府网 — 县委常委简历页；2006年8月参加工作，2002年6月加入中国共产党",
    },
    {
        "id": 7,
        "name": "刘树良",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-08",
        "birthplace": "广东云安",
        "education": "大学",
        "party_join": "2013-08",
        "work_start": "2001-10",
        "current_post": "郁南县委常委、纪委书记、监委主任",
        "current_org": "中共郁南县纪律检查委员会",
        "source": "郁南县人民政府网 — 县委常委简历页；2001年10月参加工作，2013年8月加入中国共产党",
    },
    {
        "id": 8,
        "name": "彭家新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-12",
        "birthplace": "广东郁南",
        "education": "大学",
        "party_join": "2003-07",
        "work_start": "1999-09",
        "current_post": "郁南县委常委、统战部部长、都城镇党委书记",
        "current_org": "中共郁南县委统战部",
        "source": "郁南县人民政府网 — 县委常委简历页；1999年9月参加工作，2003年7月加入中国共产党",
    },
    {
        "id": 9,
        "name": "温伯荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985-07",
        "birthplace": "广东云城",
        "education": "大学",
        "party_join": "2007-07",
        "work_start": "2009-09",
        "current_post": "郁南县委常委、组织部部长、党校校长",
        "current_org": "中共郁南县委组织部",
        "source": "郁南县人民政府网 — 县委常委简历页；2009年9月参加工作，2007年7月加入中国共产党",
    },
    {
        "id": 10,
        "name": "叶茂",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-08",
        "birthplace": "湖南醴陵",
        "education": "大学",
        "party_join": "1996-05",
        "work_start": "1994-12",
        "current_post": "郁南县委常委、县人武部政委",
        "current_org": "郁南县人民武装部",
        "source": "郁南县人民政府网 — 县委常委简历页；1994年12月参加工作，1996年5月加入中国共产党",
    },
    # ---- 副县长 ----
    {
        "id": 11,
        "name": "刘炳荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "郁南县副县长",
        "current_org": "郁南县人民政府",
        "source": "郁南县人民政府网 — 县政府领导班子页",
    },
    {
        "id": 12,
        "name": "邱桂英",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "郁南县副县长",
        "current_org": "郁南县人民政府",
        "source": "郁南县人民政府网 — 县政府领导班子页",
    },
    {
        "id": 13,
        "name": "彭家文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "郁南县副县长",
        "current_org": "郁南县人民政府",
        "source": "郁南县人民政府网 — 县政府领导班子页",
    },
    {
        "id": 14,
        "name": "梁严方",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "郁南县副县长",
        "current_org": "郁南县人民政府",
        "source": "郁南县人民政府网 — 县政府领导班子页",
    },
    {
        "id": 15,
        "name": "麦伟业",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "郁南县副县长",
        "current_org": "郁南县人民政府",
        "source": "郁南县人民政府网 — 县政府领导班子页",
    },
    # ---- 人大 ----
    {
        "id": 16,
        "name": "彭永文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-05",
        "birthplace": "广东罗定",
        "education": "大学",
        "party_join": "1998-11",
        "work_start": "1996-10",
        "current_post": "郁南县人大常委会主任",
        "current_org": "郁南县人民代表大会常务委员会",
        "source": "郁南县人民政府网 — 县人大常委会主任简历页",
    },
    {
        "id": 17,
        "name": "杨桂平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "郁南县人大常委会副主任",
        "current_org": "郁南县人民代表大会常务委员会",
        "source": "郁南县人民政府网",
    },
    {
        "id": 18,
        "name": "林峻峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "郁南县人大常委会副主任",
        "current_org": "郁南县人民代表大会常务委员会",
        "source": "郁南县人民政府网",
    },
    {
        "id": 19,
        "name": "张桂泉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "郁南县人大常委会副主任",
        "current_org": "郁南县人民代表大会常务委员会",
        "source": "郁南县人民政府网",
    },
    # ---- 政协 ----
    {
        "id": 20,
        "name": "李永盈",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "郁南县政协主席",
        "current_org": "中国人民政治协商会议郁南县委员会",
        "source": "郁南县人民政府网 — 县政协主席页",
    },
    {
        "id": 21,
        "name": "朱永通",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "郁南县政协副主席",
        "current_org": "中国人民政治协商会议郁南县委员会",
        "source": "郁南县人民政府网",
    },
    {
        "id": 22,
        "name": "林景桐",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "郁南县政协副主席",
        "current_org": "中国人民政治协商会议郁南县委员会",
        "source": "郁南县人民政府网",
    },
    {
        "id": 23,
        "name": "陈丽华",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "郁南县政协副主席",
        "current_org": "中国人民政治协商会议郁南县委员会",
        "source": "郁南县人民政府网",
    },
    {
        "id": 24,
        "name": "莫容群",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "郁南县政协副主席",
        "current_org": "中国人民政治协商会议郁南县委员会",
        "source": "郁南县人民政府网",
    },
    {
        "id": 25,
        "name": "罗树灿",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "郁南县政协副主席",
        "current_org": "中国人民政治协商会议郁南县委员会",
        "source": "郁南县人民政府网",
    },
    # ---- Predecessors ----
    {
        "id": 26,
        "name": "梁世军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（原郁南县委书记、县长）",
        "current_org": "",
        "source": "公开报道 — 前任郁南县委书记、县长，约2024-2025年离任",
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共郁南县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共云浮市委员会",
        "location": "广东云浮郁南",
    },
    {
        "id": 2,
        "name": "郁南县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "云浮市人民政府",
        "location": "广东云浮郁南",
    },
    {
        "id": 3,
        "name": "郁南县人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "云浮市人民代表大会常务委员会",
        "location": "广东云浮郁南",
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议郁南县委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "中国人民政治协商会议云浮市委员会",
        "location": "广东云浮郁南",
    },
    {
        "id": 5,
        "name": "中共郁南县纪律检查委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共郁南县委员会",
        "location": "广东云浮郁南",
    },
    {
        "id": 6,
        "name": "中共郁南县委组织部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共郁南县委员会",
        "location": "广东云浮郁南",
    },
    {
        "id": 7,
        "name": "中共郁南县委政法委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共郁南县委员会",
        "location": "广东云浮郁南",
    },
    {
        "id": 8,
        "name": "中共郁南县委统战部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共郁南县委员会",
        "location": "广东云浮郁南",
    },
    {
        "id": 9,
        "name": "中共郁南县委宣传部",
        "type": "党委",
        "level": "县处级",
        "parent": "中共郁南县委员会",
        "location": "广东云浮郁南",
    },
    {
        "id": 10,
        "name": "郁南县人民武装部",
        "type": "事业单位",
        "level": "县处级",
        "parent": "云浮军分区",
        "location": "广东云浮郁南",
    },
]

positions = [
    # 张春海 — 县委书记（现任）
    {
        "person_id": 1,
        "org_id": 1,
        "title": "郁南县委书记",
        "start_date": "",
        "end_date": "",
        "rank": "县处级正职",
        "note": "现任。主持县委全面工作。1974年3月生，广东开平人，大学学历，1995年5月入党，1996年7月参加工作。此前曾任郁南县委副书记、县长。",
    },
    # 潘宁 — 常务副县长
    {
        "person_id": 2,
        "org_id": 2,
        "title": "郁南县委常委、副县长（常务）",
        "start_date": "",
        "end_date": "",
        "rank": "县处级副职",
        "note": "现任。协助县长处理县政府日常工作。1974年6月生，广东罗定人，大学学历，1996年7月入党，1995年8月参加工作。县长空缺期间主持县政府日常工作。",
    },
    {
        "person_id": 2,
        "org_id": 1,
        "title": "郁南县委常委",
        "start_date": "",
        "end_date": "",
        "rank": "县处级副职",
        "note": "现任县委常委，兼任县政府党组副书记、副县长。",
    },
    # 郑辉亮
    {
        "person_id": 3,
        "org_id": 1,
        "title": "郁南县委副书记",
        "start_date": "",
        "end_date": "",
        "rank": "县处级副职",
        "note": "现任。协助县委书记抓党的建设工作，处理县委日常事务。兼任县委政法委书记。1981年2月生，广东电白人。",
    },
    {
        "person_id": 3,
        "org_id": 7,
        "title": "郁南县委政法委书记",
        "start_date": "",
        "end_date": "",
        "rank": "县处级副职",
        "note": "兼任。负责政法、维护社会稳定工作。",
    },
    # 邹飞祥（挂职）
    {
        "person_id": 4,
        "org_id": 1,
        "title": "挂任郁南县委副书记",
        "start_date": "",
        "end_date": "",
        "rank": "县处级副职",
        "note": "挂任。广东省文化和旅游发展与保障中心副主任下派。1978年4月生，广东兴宁人，研究生学历。",
    },
    # 陈荣南
    {
        "person_id": 5,
        "org_id": 1,
        "title": "郁南县委常委",
        "start_date": "",
        "end_date": "",
        "rank": "县处级副职",
        "note": "现任。兼任县委办公室主任、宣传部部长。1976年6月生，广东信宜人。",
    },
    {
        "person_id": 5,
        "org_id": 9,
        "title": "郁南县委宣传部部长",
        "start_date": "",
        "end_date": "",
        "rank": "县处级副职",
        "note": "兼任。负责宣传思想、文化、意识形态工作。",
    },
    # 何毅
    {
        "person_id": 6,
        "org_id": 1,
        "title": "郁南县委常委",
        "start_date": "",
        "end_date": "",
        "rank": "县处级副职",
        "note": "现任。负责科技、工信、商务、市监、林业等工作。1982年5月生，广东云安人，研究生学历。",
    },
    # 刘树良
    {
        "person_id": 7,
        "org_id": 5,
        "title": "郁南县委常委、纪委书记、监委主任",
        "start_date": "",
        "end_date": "",
        "rank": "县处级副职",
        "note": "现任。负责纪检监察、党风廉政建设工作。1978年8月生，广东云安人。2013年8月入党，2001年10月参加工作。",
    },
    # 彭家新
    {
        "person_id": 8,
        "org_id": 8,
        "title": "郁南县委常委、统战部部长",
        "start_date": "",
        "end_date": "",
        "rank": "县处级副职",
        "note": "现任。兼任县政协党组副书记、都城镇党委书记。1977年12月生，广东郁南人。",
    },
    # 温伯荣
    {
        "person_id": 9,
        "org_id": 6,
        "title": "郁南县委常委、组织部部长",
        "start_date": "",
        "end_date": "",
        "rank": "县处级副职",
        "note": "现任。兼任县委党校校长、县直机关工委书记。1985年7月生，广东云城人。2009年9月参加工作。",
    },
    # 叶茂
    {
        "person_id": 10,
        "org_id": 10,
        "title": "郁南县委常委、县人武部政委",
        "start_date": "",
        "end_date": "",
        "rank": "县处级副职",
        "note": "现任。县人武部上校政治委员。1976年8月生，湖南醴陵人。1994年12月参加工作。",
    },
    # 副县长们
    {
        "person_id": 11,
        "org_id": 2,
        "title": "郁南县副县长",
        "start_date": "",
        "end_date": "",
        "rank": "县处级副职",
        "note": "现任郁南县副县长。",
    },
    {
        "person_id": 12,
        "org_id": 2,
        "title": "郁南县副县长",
        "start_date": "",
        "end_date": "",
        "rank": "县处级副职",
        "note": "现任郁南县副县长。",
    },
    {
        "person_id": 13,
        "org_id": 2,
        "title": "郁南县副县长",
        "start_date": "",
        "end_date": "",
        "rank": "县处级副职",
        "note": "现任郁南县副县长。",
    },
    {
        "person_id": 14,
        "org_id": 2,
        "title": "郁南县副县长",
        "start_date": "",
        "end_date": "",
        "rank": "县处级副职",
        "note": "现任郁南县副县长。",
    },
    {
        "person_id": 15,
        "org_id": 2,
        "title": "郁南县副县长",
        "start_date": "",
        "end_date": "",
        "rank": "县处级副职",
        "note": "现任郁南县副县长。",
    },
    # 人大
    {
        "person_id": 16,
        "org_id": 3,
        "title": "郁南县人大常委会主任",
        "start_date": "",
        "end_date": "",
        "rank": "县处级正职",
        "note": "现任。主持县人大常委会全面工作。1975年5月生，广东罗定人。",
    },
    {
        "person_id": 17,
        "org_id": 3,
        "title": "郁南县人大常委会副主任",
        "start_date": "",
        "end_date": "",
        "rank": "县处级副职",
        "note": "现任郁南县人大常委会副主任。",
    },
    {
        "person_id": 18,
        "org_id": 3,
        "title": "郁南县人大常委会副主任",
        "start_date": "",
        "end_date": "",
        "rank": "县处级副职",
        "note": "现任郁南县人大常委会副主任。",
    },
    {
        "person_id": 19,
        "org_id": 3,
        "title": "郁南县人大常委会副主任",
        "start_date": "",
        "end_date": "",
        "rank": "县处级副职",
        "note": "现任郁南县人大常委会副主任。",
    },
    # 政协
    {
        "person_id": 20,
        "org_id": 4,
        "title": "郁南县政协主席",
        "start_date": "",
        "end_date": "",
        "rank": "县处级正职",
        "note": "现任。主持县政协全面工作。",
    },
    {
        "person_id": 21,
        "org_id": 4,
        "title": "郁南县政协副主席",
        "start_date": "",
        "end_date": "",
        "rank": "县处级副职",
        "note": "现任郁南县政协副主席。",
    },
    {
        "person_id": 22,
        "org_id": 4,
        "title": "郁南县政协副主席",
        "start_date": "",
        "end_date": "",
        "rank": "县处级副职",
        "note": "现任郁南县政协副主席。",
    },
    {
        "person_id": 23,
        "org_id": 4,
        "title": "郁南县政协副主席",
        "start_date": "",
        "end_date": "",
        "rank": "县处级副职",
        "note": "现任郁南县政协副主席。",
    },
    {
        "person_id": 24,
        "org_id": 4,
        "title": "郁南县政协副主席",
        "start_date": "",
        "end_date": "",
        "rank": "县处级副职",
        "note": "现任郁南县政协副主席。",
    },
    {
        "person_id": 25,
        "org_id": 4,
        "title": "郁南县政协副主席",
        "start_date": "",
        "end_date": "",
        "rank": "县处级副职",
        "note": "现任郁南县政协副主席。",
    },
    # 前任梁世军
    {
        "person_id": 26,
        "org_id": 1,
        "title": "郁南县委书记（前任）",
        "start_date": "",
        "end_date": "",
        "rank": "县处级正职",
        "note": "前任郁南县委书记。此前曾任郁南县县长。约2024-2025年离任。去向待查。",
    },
    {
        "person_id": 26,
        "org_id": 2,
        "title": "郁南县县长（前任）",
        "start_date": "",
        "end_date": "",
        "rank": "县处级正职",
        "note": "此前曾任郁南县县长。后升任县委书记。",
    },
]

relationships = [
    # 张春海 ↔ 潘宁（党政正副职搭档）
    {
        "person_a": 1,
        "person_b": 2,
        "type": "党政正副职搭档",
        "context": "张春海（县委书记）与潘宁（县委常委、常务副县长）为县委县政府核心搭档。县长空缺期间，潘宁主持县政府日常工作。",
        "overlap_org": "郁南县党政班子",
        "overlap_period": "现任",
    },
    # 张春海 ↔ 郑辉亮
    {
        "person_a": 1,
        "person_b": 3,
        "type": "党政正副职搭档",
        "context": "张春海（县委书记）与郑辉亮（县委副书记、政法委书记）为县委正副书记搭档关系。",
        "overlap_org": "中共郁南县委员会",
        "overlap_period": "现任",
    },
    # 张春海 ↔ 邹飞祥
    {
        "person_a": 1,
        "person_b": 4,
        "type": "党政搭档（挂职）",
        "context": "张春海（县委书记）与邹飞祥（挂任县委副书记）为县委正副书记关系。邹飞祥由省文旅厅下派。",
        "overlap_org": "中共郁南县委员会",
        "overlap_period": "现任",
    },
    # 张春海 ↔ 陈荣南
    {
        "person_a": 1,
        "person_b": 5,
        "type": "党政搭档",
        "context": "张春海（县委书记）与陈荣南（县委常委、办公室主任）为县委领导与办公室负责人工作关系。",
        "overlap_org": "中共郁南县委员会",
        "overlap_period": "现任",
    },
    # 张春海 ↔ 刘树良
    {
        "person_a": 1,
        "person_b": 7,
        "type": "党政搭档",
        "context": "张春海（县委书记）与刘树良（县委常委、纪委书记）为县委领导与纪检监察负责人工作关系。",
        "overlap_org": "中共郁南县委员会",
        "overlap_period": "现任",
    },
    # 张春海 ↔ 温伯荣
    {
        "person_a": 1,
        "person_b": 9,
        "type": "党政搭档",
        "context": "张春海（县委书记）与温伯荣（县委常委、组织部部长）为县委领导与组织负责人工作关系。",
        "overlap_org": "中共郁南县委员会",
        "overlap_period": "现任",
    },
    # 张春海 ↔ 彭家新
    {
        "person_a": 1,
        "person_b": 8,
        "type": "党政搭档",
        "context": "张春海（县委书记）与彭家新（县委常委、统战部部长、都城镇党委书记）工作关系。",
        "overlap_org": "中共郁南县委员会",
        "overlap_period": "现任",
    },
    # 张春海 ↔ 何毅
    {
        "person_a": 1,
        "person_b": 6,
        "type": "党政搭档",
        "context": "张春海（县委书记）与何毅（县委常委）工作关系。",
        "overlap_org": "中共郁南县委员会",
        "overlap_period": "现任",
    },
    # 张春海 ↔ 彭永文
    {
        "person_a": 1,
        "person_b": 16,
        "type": "党政人大关系",
        "context": "张春海（县委书记）与彭永文（县人大常委会主任）为县委与人大领导关系。",
        "overlap_org": "郁南县",
        "overlap_period": "现任",
    },
    # 张春海 ↔ 李永盈
    {
        "person_a": 1,
        "person_b": 20,
        "type": "党政政协关系",
        "context": "张春海（县委书记）与李永盈（县政协主席）为县委与政协领导关系。",
        "overlap_org": "郁南县",
        "overlap_period": "现任",
    },
    # 张春海 ↔ 梁世军（前任）
    {
        "person_a": 1,
        "person_b": 26,
        "type": "前任接任",
        "context": "梁世军为前任郁南县委书记/县长，张春海接任县委书记职务（此前张春海为县长）。",
        "overlap_org": "中共郁南县委员会",
        "overlap_period": "",
    },
    # 潘宁 ↔ 郑辉亮
    {
        "person_a": 2,
        "person_b": 3,
        "type": "党政搭档",
        "context": "潘宁（县委常委、常务副县长）与郑辉亮（县委副书记、政法委书记）为县委常委班子同事。",
        "overlap_org": "中共郁南县委员会",
        "overlap_period": "现任",
    },
    # 潘宁 ↔ 刘炳荣
    {
        "person_a": 2,
        "person_b": 11,
        "type": "上下级关系",
        "context": "潘宁（常务副县长）与刘炳荣（副县长）为县政府正副职搭档。",
        "overlap_org": "郁南县人民政府",
        "overlap_period": "现任",
    },
    # 潘宁 ↔ 邱桂英
    {
        "person_a": 2,
        "person_b": 12,
        "type": "上下级关系",
        "context": "潘宁（常务副县长）与邱桂英（副县长）为县政府正副职搭档。",
        "overlap_org": "郁南县人民政府",
        "overlap_period": "现任",
    },
    # 彭家新 ↔ 李永盈
    {
        "person_a": 8,
        "person_b": 20,
        "type": "政协统战关系",
        "context": "彭家新（县委常委、统战部部长，兼县政协党组副书记）与李永盈（县政协主席）为政协党组搭档关系。",
        "overlap_org": "中国人民政治协商会议郁南县委员会",
        "overlap_period": "现任",
    },
    # 郑辉亮 ↔ 刘树良
    {
        "person_a": 3,
        "person_b": 7,
        "type": "党政搭档",
        "context": "郑辉亮（县委副书记、政法委书记）与刘树良（县委常委、纪委书记）为县委常委班子同事，共同负责政法与纪检工作配合。",
        "overlap_org": "中共郁南县委员会",
        "overlap_period": "现任",
    },
    # 温伯荣 ↔ 陈荣南
    {
        "person_a": 9,
        "person_b": 5,
        "type": "党政搭档",
        "context": "温伯荣（组织部部长）与陈荣南（宣传部部长）为县委常委中分管党务宣传的同僚。",
        "overlap_org": "中共郁南县委员会",
        "overlap_period": "现任",
    },
]

# =========================================================================
# BUILD FUNCTIONS
# =========================================================================

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def pcolor_viz(post):
    post = post or ""
    if "书记" in post and ("县委" in post or "党委" in post) and "副" not in post and "纪委" not in post:
        return "230,50,50"
    if "副书记" in post:
        return "200,80,80"
    if "县长" in post or "区长" in post:
        if "副" not in post:
            return "50,100,230"
        return "80,140,230"
    if "纪委书记" in post or "监委" in post:
        return "230,165,0"
    if "人大" in post:
        return "50,180,50"
    if "政协" in post:
        return "180,100,180"
    if "县委常委" in post:
        return "150,100,50"
    if "副县长" in post:
        return "80,140,230"
    return "120,120,120"


def ocolor_viz(otype):
    return {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,200",
        "政协": "255,240,200",
        "事业单位": "220,220,220",
    }.get(otype, "200,200,200")


def build_sqlite():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = __import__('sqlite3').connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
    CREATE TABLE persons (
        id INTEGER PRIMARY KEY, name TEXT NOT NULL, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, education TEXT, party_join TEXT, work_start TEXT,
        current_post TEXT, current_org TEXT, source TEXT
    );
    CREATE TABLE organizations (
        id INTEGER PRIMARY KEY, name TEXT NOT NULL, type TEXT, level TEXT, parent TEXT, location TEXT
    );
    CREATE TABLE positions (
        id INTEGER PRIMARY KEY, person_id INTEGER NOT NULL, org_id INTEGER NOT NULL,
        title TEXT NOT NULL, start TEXT, end TEXT, rank TEXT, note TEXT,
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    );
    CREATE TABLE relationships (
        id INTEGER PRIMARY KEY, person_a_id INTEGER NOT NULL, person_b_id INTEGER NOT NULL,
        type TEXT NOT NULL, context TEXT, overlap_org TEXT, overlap_period TEXT,
        FOREIGN KEY (person_a_id) REFERENCES persons(id),
        FOREIGN KEY (person_b_id) REFERENCES persons(id)
    );
    """)

    for p in persons:
        c.execute("INSERT INTO persons VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                   p["birthplace"], p["education"], p["party_join"], p["work_start"],
                   p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("INSERT INTO organizations VALUES(?,?,?,?,?,?)",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("INSERT INTO positions(person_id, org_id, title, start, end, rank, note) VALUES(?,?,?,?,?,?,?)",
                  (pos["person_id"], pos["org_id"], pos["title"],
                   pos.get("start_date", ""), pos.get("end_date", ""),
                   pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        c.execute("INSERT INTO relationships(person_a_id, person_b_id, type, context, overlap_org, overlap_period) VALUES(?,?,?,?,?,?)",
                  (r["person_a"], r["person_b"], r["type"],
                   r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()

    counts = {}
    for t in ["persons", "organizations", "positions", "relationships"]:
        c.execute(f"SELECT COUNT(*) FROM {t}")
        counts[t] = c.fetchone()[0]
    conn.close()

    return counts


def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{today}">')
    lines.append('    <creator>sisyphus-junior</creator>')
    lines.append(f'    <description>郁南县领导班子工作关系网络 - {today}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    lines.append('    <attributes class="node">')
    for aid, atitle in [("0", "type"), ("1", "birth"), ("2", "birthplace"), ("3", "current_post")]:
        lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    for aid, atitle in [("0", "type"), ("1", "start"), ("2", "end"), ("3", "context")]:
        lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
    lines.append('    </attributes>')

    # Nodes - persons
    lines.append('    <nodes>')
    for p in persons:
        c_val = pcolor_viz(p.get("current_post", ""))
        pid = p["id"]
        # Size: top leaders (书记=1, 常务副县长=2) size 20; 副书记/人大/政协 head = 15; rest = 12
        if pid in (1, 2):
            sz = "20.0"
        elif pid in (3, 4, 16, 20, 26):
            sz = "15.0"
        else:
            sz = "12.0"
        lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        for f, v in [("0", "person"), ("1", p.get("birth", "")), ("2", p.get("birthplace", "")),
                      ("3", p.get("current_post", ""))]:
            lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c_val.split(",")[0]}" g="{c_val.split(",")[1]}" b="{c_val.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes - organizations
    for o in organizations:
        c_val = ocolor_viz(o.get("type", ""))
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        for f, v in [("0", "organization"), ("1", ""), ("2", o.get("location", "")), ("3", "")]:
            lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c_val.split(",")[0]}" g="{c_val.split(",")[1]}" b="{c_val.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" '
                     f'label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        for f, v in [("0", "worked_at"), ("1", pos.get("start_date", "")), ("2", pos.get("end_date", "")),
                      ("3", pos.get("note", ""))]:
            lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" '
                     f'label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        for f, v in [("0", r["type"]), ("1", ""), ("2", ""), ("3", r.get("context", ""))]:
            lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')

    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    tn = len(persons) + len(organizations)
    te = len(positions) + len(relationships)
    return tn, te


# =========================================================================
# MAIN
# =========================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("郁南县 Government Personnel Network Builder")
    print(f"Date: {today}")
    print("=" * 60)

    print(f"\n▶ Building SQLite database...")
    counts = build_sqlite()
    print(f"  ✓ {DB_PATH}")
    for t, n in counts.items():
        print(f"    {t}: {n}")

    print(f"\n▶ Building GEXF graph...")
    tn, te = build_gexf()
    print(f"  ✓ {GEXF_PATH}")
    print(f"    Nodes: {tn}  |  Edges: {te}")

    # Verify
    errors = []
    if not os.path.exists(DB_PATH):
        errors.append(f"DB file not created: {DB_PATH}")
    if not os.path.exists(GEXF_PATH):
        errors.append(f"GEXF file not created: {GEXF_PATH}")

    if errors:
        print(f"\n✗ ERRORS:")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print(f"\n✓ BUILD COMPLETE - All artifacts created successfully")
