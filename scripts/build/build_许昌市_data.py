#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 许昌市 leadership network.

调查日期: 2026-07-24
信息来源: 维基百科、澎湃新闻、中国经济网、许昌市人民政府网站
调查级别: 地级市
"""

import json
import os
import sys
from datetime import datetime

# ── Paths ──────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(BASE, "..", ".."))
sys.path.insert(0, REPO_ROOT)

STAGING_DIR = BASE
DB_PATH = os.path.join(STAGING_DIR, "许昌市_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "许昌市_network.gexf")
PERSONS_DIR = STAGING_DIR

TODAY = datetime.now().strftime("%Y%m%d")
SLUG = "河南省许昌市"

# ── PERSONS ────────────────────────────────────────────────────────
persons = [
    # ═══════════════════════════════
    # 市委领导 (Party Committee)
    # ═══════════════════════════════

    # 市委书记 — 杨小菁
    {
        "id": 1,
        "name": "杨小菁",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1977-03",
        "birthplace": "江苏无锡",
        "education": "华东政法学院法学本科，在职法学硕士",
        "party_join": "1996-11",
        "work_start": "1999-07",
        "current_post": "中共许昌市委书记",
        "current_org": "中共许昌市委员会",
        "source": "https://zh.wikipedia.org/wiki/杨小菁",
    },
    # 市长 — 张庆一
    {
        "id": 2,
        "name": "张庆一",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969-03",
        "birthplace": "河南鲁山",
        "education": "中共河南省委党校研究生，理学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "许昌市人民政府市长",
        "current_org": "许昌市人民政府",
        "source": "https://zh.wikipedia.org/wiki/张庆一",
    },
    # 市人大常委会主任 — 王志宏
    {
        "id": 3,
        "name": "王志宏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1965-04",
        "birthplace": "河南长葛",
        "education": "北京大学思想政治教育专业在职学习",
        "party_join": "1987-12",
        "work_start": "1983-08",
        "current_post": "许昌市人大常委会主任、党组书记",
        "current_org": "许昌市人大常委会",
        "source": "https://zh.wikipedia.org/wiki/王志宏_(1965年)",
    },
    # 市政协主席 — 刘保新
    {
        "id": 4,
        "name": "刘保新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1963-09",
        "birthplace": "河南南阳",
        "education": "郑州大学哲学系本科",
        "party_join": "1985-09",
        "work_start": "1986-07",
        "current_post": "许昌市政协主席",
        "current_org": "政协许昌市委员会",
        "source": "https://zh.wikipedia.org/wiki/刘保新",
    },

    # ═══════════════════════════════
    # 前任领导 (Predecessors)
    # ═══════════════════════════════

    # 前任市委书记 — 史根治（被查）
    {
        "id": 5,
        "name": "史根治",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1965-01",
        "birthplace": "河南尉氏",
        "education": "中央党校政治经济学研究生",
        "party_join": "1983-10",
        "work_start": "1981-09",
        "current_post": "（原许昌市委书记，2025年1月被查）",
        "current_org": "",
        "source": "https://zh.wikipedia.org/wiki/史根治",
    },
    # 前任市委书记 — 胡五岳
    {
        "id": 6,
        "name": "胡五岳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1963-06",
        "birthplace": "河南伊川",
        "education": "郑州大学经济系本科",
        "party_join": "1984-05",
        "work_start": "1984-07",
        "current_post": "河南省委副秘书长、办公厅主任",
        "current_org": "中共河南省委办公厅",
        "source": "https://zh.wikipedia.org/wiki/胡五岳",
    },
    # 前任市委书记 — 武国定
    {
        "id": 7,
        "name": "武国定",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1963-06",
        "birthplace": "河南舞钢",
        "education": "百泉农业专科学校园林系",
        "party_join": "1984-12",
        "work_start": "1983-07",
        "current_post": "（原河南省副省长，已卸任）",
        "current_org": "",
        "source": "https://zh.wikipedia.org/wiki/武国定",
    },
    # 前市长 — 刘涛（跨省调任湘西）
    {
        "id": 8,
        "name": "刘涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-06",
        "birthplace": "河南方城",
        "education": "河南大学中文系本科、文学院中国现代文学硕士",
        "party_join": "1996-11",
        "work_start": "1997-07",
        "current_post": "中共湘西土家族苗族自治州委书记",
        "current_org": "中共湘西土家族苗族自治州委员会",
        "source": "https://zh.wikipedia.org/wiki/刘涛_(1971年)",
    },
    # 前市长/书记 — 张国晖
    {
        "id": 9,
        "name": "张国晖",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（原许昌市长，2010-2015）",
        "current_org": "",
        "source": "https://zh.wikipedia.org/wiki/许昌市",
    },
    # 前市委书记 — 王树山
    {
        "id": 10,
        "name": "王树山",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（原许昌市委书记，2013-2016）",
        "current_org": "",
        "source": "https://zh.wikipedia.org/wiki/许昌市",
    },
    # 前市委书记 — 李亚
    {
        "id": 11,
        "name": "李亚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1963",
        "birthplace": "河南永城",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "河南省人大常委会副主任、党组书记（原许昌市委书记）",
        "current_org": "河南省人大常委会",
        "source": "https://zh.wikipedia.org/wiki/许昌市",
    },
]

# ── ORGANIZATIONS ──────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共许昌市委员会", "type": "党委", "level": "地级", "parent": "中共河南省委员会", "location": "河南省许昌市魏都区"},
    {"id": 2, "name": "许昌市人民政府", "type": "政府", "level": "地级", "parent": "河南省人民政府", "location": "河南省许昌市魏都区"},
    {"id": 3, "name": "许昌市人大常委会", "type": "人大", "level": "地级", "parent": "河南省人大常委会", "location": "河南省许昌市魏都区"},
    {"id": 4, "name": "政协许昌市委员会", "type": "政协", "level": "地级", "parent": "政协河南省委员会", "location": "河南省许昌市魏都区"},
    {"id": 5, "name": "中共许昌市纪律检查委员会", "type": "党委", "level": "地级", "parent": "中共许昌市委员会", "location": "河南省许昌市"},
    {"id": 6, "name": "中共河南省委办公厅", "type": "党委", "level": "省级", "parent": "中共河南省委员会", "location": "河南省郑州市"},
    {"id": 7, "name": "河南省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "河南省郑州市"},
    {"id": 8, "name": "河南省人大常委会", "type": "人大", "level": "省级", "parent": "", "location": "河南省郑州市"},
    {"id": 9, "name": "中共湘西土家族苗族自治州委员会", "type": "党委", "level": "地级", "parent": "中共湖南省委员会", "location": "湖南省湘西州吉首市"},
    {"id": 10, "name": "中共上海市青浦区委员会", "type": "党委", "level": "地级（直辖市区）", "parent": "中共上海市委员会", "location": "上海市青浦区"},
    {"id": 11, "name": "上海市青浦区人民政府", "type": "政府", "level": "地级（直辖市区）", "parent": "上海市人民政府", "location": "上海市青浦区"},
    {"id": 12, "name": "上海市委组织部", "type": "党委", "level": "省级", "parent": "中共上海市委员会", "location": "上海市"},
    {"id": 13, "name": "上海市静安区人民检察院", "type": "政府", "level": "地级（直辖市区）", "parent": "上海市人民检察院", "location": "上海市静安区"},
    {"id": 14, "name": "中共周口市委员会", "type": "党委", "level": "地级", "parent": "中共河南省委员会", "location": "河南省周口市"},
    {"id": 15, "name": "周口市人民政府", "type": "政府", "level": "地级", "parent": "河南省人民政府", "location": "河南省周口市"},
    {"id": 16, "name": "中共商丘市委员会", "type": "党委", "level": "地级", "parent": "中共河南省委员会", "location": "河南省商丘市"},
    {"id": 17, "name": "商丘市人民政府", "type": "政府", "level": "地级", "parent": "河南省人民政府", "location": "河南省商丘市"},
    {"id": 18, "name": "中共焦作市委员会", "type": "党委", "level": "地级", "parent": "中共河南省委员会", "location": "河南省焦作市"},
    {"id": 19, "name": "焦作市人民政府", "type": "政府", "level": "地级", "parent": "河南省人民政府", "location": "河南省焦作市"},
    {"id": 20, "name": "中共驻马店市委员会", "type": "党委", "level": "地级", "parent": "中共河南省委员会", "location": "河南省驻马店市"},
    {"id": 21, "name": "驻马店市人民政府", "type": "政府", "level": "地级", "parent": "河南省人民政府", "location": "河南省驻马店市"},
    {"id": 22, "name": "河南省发展和改革委员会", "type": "政府", "level": "省级", "parent": "河南省人民政府", "location": "河南省郑州市"},
    {"id": 23, "name": "河南省统计局", "type": "政府", "level": "省级", "parent": "河南省人民政府", "location": "河南省郑州市"},
    {"id": 24, "name": "河南省劳动和社会保障厅", "type": "政府", "level": "省级", "parent": "河南省人民政府", "location": "河南省郑州市"},
    {"id": 25, "name": "中共鄢陵县委员会", "type": "党委", "level": "县级", "parent": "中共许昌市委员会", "location": "河南省许昌市鄢陵县"},
    {"id": 26, "name": "禹州市人民政府", "type": "政府", "level": "县级", "parent": "许昌市人民政府", "location": "河南省许昌市禹州市"},
    {"id": 27, "name": "中共禹州市委员会", "type": "党委", "level": "县级", "parent": "中共许昌市委员会", "location": "河南省许昌市禹州市"},
    {"id": 28, "name": "中共宝丰县委员会", "type": "党委", "level": "县级", "parent": "中共平顶山市委员会", "location": "河南省平顶山市宝丰县"},
    {"id": 29, "name": "宝丰县人民政府", "type": "政府", "level": "县级", "parent": "平顶山市人民政府", "location": "河南省平顶山市宝丰县"},
    {"id": 30, "name": "平顶山市人民政府", "type": "政府", "level": "地级", "parent": "河南省人民政府", "location": "河南省平顶山市"},
]

# ── POSITIONS ──────────────────────────────────────────────────────
positions = [
    # 杨小菁
    {"person_id": 1, "org_id": 13, "title": "上海市静安区人民检察院干部", "start": "1999-07", "end": "2009-06", "rank": "科级→正科级", "note": ""},
    {"person_id": 1, "org_id": 12, "title": "上海市委组织部新闻和网络宣传处处长", "start": "2009-06", "end": "2016-09", "rank": "副处级→正处级", "note": "2009年通过上海市选人用人改革选拔提任副处级"},
    {"person_id": 1, "org_id": 12, "title": "上海市委组织部部务委员", "start": "2016-09", "end": "2019-03", "rank": "副厅级", "note": "后兼任组织一处处长"},
    {"person_id": 1, "org_id": 10, "title": "青浦区委副书记", "start": "2019-03", "end": "2021-09", "rank": "正厅级", "note": ""},
    {"person_id": 1, "org_id": 11, "title": "青浦区代区长、区长", "start": "2021-09", "end": "2024-10", "rank": "正厅级", "note": "2022年1月正式当选，当时上海最年轻区政府主官"},
    {"person_id": 1, "org_id": 1, "title": "许昌市委副书记、市政府党组书记", "start": "2024-10", "end": "2024-10", "rank": "正厅级", "note": "2024年10月跨省调任"},
    {"person_id": 1, "org_id": 2, "title": "许昌市人民政府市长", "start": "2024-10", "end": "2025-02", "rank": "正厅级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "中共许昌市委书记", "start": "2025-02", "end": "至今", "rank": "正厅级", "note": "接替被查的史根治"},

    # 张庆一
    {"person_id": 2, "org_id": 29, "title": "宝丰县县长", "start": "", "end": "", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 28, "title": "宝丰县委书记", "start": "", "end": "", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 30, "title": "平顶山市副市长", "start": "", "end": "2021", "rank": "副厅级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "许昌市委常委、统战部部长", "start": "2021", "end": "2023", "rank": "副厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "许昌市委常委、常务副市长", "start": "2023", "end": "2024-09", "rank": "副厅级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "许昌市委副书记、政法委书记", "start": "2024-09", "end": "2025-02", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "许昌市人民政府市长", "start": "2025-02", "end": "至今", "rank": "正厅级", "note": "接替升任书记的杨小菁"},

    # 王志宏
    {"person_id": 3, "org_id": 25, "title": "鄢陵县县长", "start": "2011-05", "end": "2013-09", "rank": "正处级", "note": ""},
    {"person_id": 3, "org_id": 26, "title": "禹州市市长", "start": "2013-09", "end": "2014-03", "rank": "正处级", "note": ""},
    {"person_id": 3, "org_id": 27, "title": "禹州市委书记", "start": "2014-03", "end": "2016-03", "rank": "正处级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "许昌市副市长", "start": "2016-03", "end": "2017-05", "rank": "副厅级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "许昌市委常委、秘书长", "start": "2017-05", "end": "2021-09", "rank": "副厅级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "许昌市委常委、常务副市长", "start": "2021-09", "end": "2023-01", "rank": "副厅级", "note": ""},
    {"person_id": 3, "org_id": 3, "title": "许昌市人大常委会主任、党组书记", "start": "2023-01", "end": "至今", "rank": "正厅级", "note": ""},

    # 刘保新
    {"person_id": 4, "org_id": 22, "title": "河南省政协副秘书长、机关党组成员", "start": "2010-07", "end": "2014-02", "rank": "副厅级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "许昌市委常委、统战部部长", "start": "2014-02", "end": "2017-05", "rank": "副厅级", "note": ""},
    {"person_id": 4, "org_id": 4, "title": "许昌市政协主席", "start": "2017-05", "end": "至今", "rank": "正厅级", "note": ""},

    # 史根治
    {"person_id": 5, "org_id": 14, "title": "周口市副市长", "start": "2006-03", "end": "2011-04", "rank": "副厅级", "note": ""},
    {"person_id": 5, "org_id": 14, "title": "周口市委常委、副市长", "start": "2011-04", "end": "2011-08", "rank": "副厅级", "note": ""},
    {"person_id": 5, "org_id": 14, "title": "周口市委常委、秘书长", "start": "2011-08", "end": "2014-03", "rank": "副厅级", "note": ""},
    {"person_id": 5, "org_id": 16, "title": "商丘市委常委、常务副市长", "start": "2014-03", "end": "2018-01", "rank": "副厅级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "许昌市委副书记", "start": "2018-01", "end": "2019-03", "rank": "正厅级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "许昌市人民政府市长", "start": "2019-03", "end": "2021-07", "rank": "正厅级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "中共许昌市委书记", "start": "2021-07", "end": "2025-01", "rank": "正厅级", "note": "2025年1月因涉嫌严重违纪违法被查"},

    # 胡五岳
    {"person_id": 6, "org_id": 22, "title": "河南省发改委副主任", "start": "2006-06", "end": "2011-04", "rank": "副厅级", "note": ""},
    {"person_id": 6, "org_id": 23, "title": "河南省统计局局长", "start": "2013-04", "end": "2016-05", "rank": "正厅级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "许昌市委副书记、市长", "start": "2016-05", "end": "2019-03", "rank": "正厅级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "中共许昌市委书记", "start": "2018-10", "end": "2021-07", "rank": "正厅级", "note": ""},
    {"person_id": 6, "org_id": 6, "title": "河南省委副秘书长、办公厅主任", "start": "2021-07", "end": "至今", "rank": "正厅级", "note": ""},

    # 武国定
    {"person_id": 7, "org_id": 20, "title": "驻马店市副市长", "start": "2006-02", "end": "2008-09", "rank": "副厅级", "note": ""},
    {"person_id": 7, "org_id": 20, "title": "驻马店市委常委、秘书长", "start": "2008-09", "end": "2011-09", "rank": "副厅级", "note": ""},
    {"person_id": 7, "org_id": 20, "title": "驻马店市委常委、常务副市长", "start": "2011-09", "end": "2013-04", "rank": "副厅级", "note": ""},
    {"person_id": 7, "org_id": 21, "title": "驻马店市市长", "start": "2013-05", "end": "2015-03", "rank": "正厅级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "许昌市人民政府市长", "start": "2015-03", "end": "2016-05", "rank": "正厅级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "中共许昌市委书记", "start": "2016-05", "end": "2018-01", "rank": "正厅级", "note": ""},
    {"person_id": 7, "org_id": 7, "title": "河南省副省长", "start": "2018-01", "end": "2023-01", "rank": "副省级", "note": ""},

    # 刘涛
    {"person_id": 8, "org_id": 24, "title": "河南省劳动和社会保障厅副厅长", "start": "2008-10", "end": "2015-02", "rank": "副厅级", "note": ""},
    {"person_id": 8, "org_id": 18, "title": "焦作市委常委、组织部部长", "start": "2015-02", "end": "2017-12", "rank": "副厅级", "note": ""},
    {"person_id": 8, "org_id": 18, "title": "焦作市委副书记（兼统战部长）", "start": "2017-12", "end": "2021-07", "rank": "正厅级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "许昌市人民政府市长", "start": "2021-07", "end": "2024-10", "rank": "正厅级", "note": "跨省调任"},
    {"person_id": 8, "org_id": 9, "title": "湘西州委书记", "start": "2024-10", "end": "至今", "rank": "正厅级", "note": ""},

    # 张国晖
    {"person_id": 9, "org_id": 2, "title": "许昌市人民政府市长", "start": "2010-10", "end": "2015-03", "rank": "正厅级", "note": ""},

    # 王树山
    {"person_id": 10, "org_id": 1, "title": "中共许昌市委书记", "start": "2013-04", "end": "2016-05", "rank": "正厅级", "note": ""},

    # 李亚
    {"person_id": 11, "org_id": 1, "title": "中共许昌市委书记", "start": "2010-07", "end": "2013-04", "rank": "正厅级", "note": ""},
    {"person_id": 11, "org_id": 8, "title": "河南省人大常委会副主任、党组书记", "start": "", "end": "至今", "rank": "副省级", "note": ""},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────────
relationships = [
    # 职业重叠关系
    {"person_a": 1, "person_b": 5, "type": "predecessor_successor", "context": "杨小菁接替被查的史根治任许昌市委书记", "overlap_org": "中共许昌市委员会", "overlap_period": "2025-01至2025-02"},
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "杨小菁任市委书记、张庆一任市长，党政搭档", "overlap_org": "许昌市四大班子", "overlap_period": "2025-02至今"},
    {"person_a": 5, "person_b": 8, "type": "overlap", "context": "史根治任市委书记期间刘涛任市长", "overlap_org": "许昌市四大班子", "overlap_period": "2021-07至2024-10"},
    {"person_a": 5, "person_b": 6, "type": "predecessor_successor", "context": "史根治接替胡五岳任许昌市委书记", "overlap_org": "中共许昌市委员会", "overlap_period": "2021-07"},
    {"person_a": 6, "person_b": 7, "type": "predecessor_successor", "context": "胡五岳接替武国定任许昌市委书记", "overlap_org": "中共许昌市委员会", "overlap_period": "2018-10"},
    {"person_a": 7, "person_b": 10, "type": "predecessor_successor", "context": "武国定接替王树山任许昌市委书记", "overlap_org": "中共许昌市委员会", "overlap_period": "2016-05"},
    {"person_a": 10, "person_b": 11, "type": "predecessor_successor", "context": "王树山接替李亚任许昌市委书记", "overlap_org": "中共许昌市委员会", "overlap_period": "2013-04"},
    {"person_a": 5, "person_b": 6, "type": "predecessor_successor", "context": "史根治接替胡五岳任许昌市长", "overlap_org": "许昌市人民政府", "overlap_period": "2019-03"},
    {"person_a": 6, "person_b": 7, "type": "predecessor_successor", "context": "胡五岳接替武国定任许昌市长", "overlap_org": "许昌市人民政府", "overlap_period": "2016-05"},
    {"person_a": 7, "person_b": 9, "type": "predecessor_successor", "context": "武国定接替张国晖任许昌市长", "overlap_org": "许昌市人民政府", "overlap_period": "2015-03"},
    {"person_a": 8, "person_b": 1, "type": "predecessor_successor", "context": "刘涛调任湘西后杨小菁接任许昌市长", "overlap_org": "许昌市人民政府", "overlap_period": "2024-10"},
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor", "context": "杨小菁升任书记后张庆一接任许昌市长", "overlap_org": "许昌市人民政府", "overlap_period": "2025-02"},

    # 王志宏与许昌领导的关系
    {"person_a": 3, "person_b": 5, "type": "overlap", "context": "王志宏任市委常委、常务副市长期间史根治任市委书记", "overlap_org": "许昌市四大班子", "overlap_period": "2021-09至2023-01"},
    {"person_a": 3, "person_b": 1, "type": "overlap", "context": "王志宏任人大主任期间与杨小菁（书记）共事", "overlap_org": "许昌市四大班子", "overlap_period": "2025-01至今"},

    # 跨省/跨市交流
    {"person_a": 1, "person_b": 8, "type": "same_pattern", "context": "两人均为跨省交流干部（杨小菁上海→河南，刘涛河南→湖南）", "overlap_org": "", "overlap_period": ""},

    # 系统内关系
    {"person_a": 3, "person_b": 7, "type": "same_system", "context": "同属许昌市领导交接，武国定任书记时王志宏任副市长/市委常委", "overlap_org": "许昌市四大班子", "overlap_period": "2016-03至2018-01"},
]


# ══════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════
def main():
    """Run the full build pipeline."""
    from gov_relation.runner import run_build
    from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

    db_path = DB_PATH
    gexf_path = GEXF_PATH

    print(f"[许昌市] Building database → {db_path}")
    print(f"[许昌市] Building GEXF    → {gexf_path}")
    print(f"[许昌市] Persons: {len(persons)}, Orgs: {len(organizations)}, "
          f"Positions: {len(positions)}, Relationships: {len(relationships)}")

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=db_path,
        gexf_path=gexf_path,
        overwrite=True,
    )

    # ── 输出 ISO 时间戳 ──
    print(f"[许昌市] Build complete at {datetime.now().isoformat()}")

    # ── 输出 person JSON files ──
    person_json_files = write_person_json_files()
    print(f"[许昌市] Person JSON files written: {len(person_json_files)}")
    for pjf in person_json_files:
        print(f"         {pjf}")

    return 0


def write_person_json_files():
    """Write individual person JSON files for core leaders."""
    files_written = []

    # ── 杨小菁 ──
    yangxj = {
        "schema_version": "1.0",
        "generated_at": "2026-07-24",
        "investigation_scope": {
            "province": "河南省",
            "city": "许昌市",
            "region": "许昌市",
            "job": "市委书记",
            "task_id": "henan_许昌市",
            "time_focus": "2025-2026"
        },
        "identity": {
            "person_id": "henan_xuchang_yang_xiaojing",
            "name": "杨小菁",
            "aliases": [],
            "gender": "女",
            "ethnicity": "汉族",
            "birth": "1977-03",
            "birthplace": "江苏无锡",
            "native_place": "江苏无锡",
            "education": [
                {"period": "1995-1999", "institution": "华东政法学院（现华东政法大学）", "major": "法学", "degree": "本科", "study_type": "full_time", "source_ids": ["S001"]},
                {"period": "", "institution": "", "major": "法学", "degree": "在职法学硕士", "study_type": "part_time", "source_ids": ["S001"]}
            ],
            "party_join": "1996-11",
            "work_start": "1999-07",
            "dedupe_keys": {
                "name_birth": "杨小菁_1977-03",
                "name_birthplace": "杨小菁_江苏无锡",
                "official_profile_url": "https://www.xuchang.gov.cn"
            }
        },
        "current_status": {
            "current_post": "中共许昌市委书记",
            "current_org": "中共许昌市委员会",
            "administrative_rank": "正厅级",
            "as_of": "2026-07-24",
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002", "S003"]
        },
        "career_timeline": [
            {"start": "1999-07", "end": "2009-06", "org": "上海市静安区人民检察院", "title": "干部/书记员", "level": "科级→正科级", "location": "上海静安区", "system": "government", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001"]},
            {"start": "2009-06", "end": "2016-09", "org": "上海市委组织部", "title": "新闻和网络宣传处处长/研究室主任", "level": "副处级→正处级", "location": "上海", "system": "organization", "rank": "", "is_key_promotion": True, "notes": "2009年通过上海市选人用人改革选拔从正科提任副处", "confidence": "confirmed", "source_ids": ["S001", "S004"]},
            {"start": "2016-09", "end": "2019-03", "org": "上海市委组织部", "title": "部务委员（兼组织一处处长）", "level": "副厅级", "location": "上海", "system": "organization", "rank": "", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S001", "S005"]},
            {"start": "2019-03", "end": "2021-09", "org": "中共上海市青浦区委员会", "title": "青浦区委副书记", "level": "正厅级", "location": "上海青浦区", "system": "party", "rank": "", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S001", "S004"]},
            {"start": "2021-09", "end": "2024-10", "org": "上海市青浦区人民政府", "title": "青浦区代区长、区长", "level": "正厅级", "location": "上海青浦区", "system": "government", "rank": "", "is_key_promotion": True, "notes": "当时上海最年轻的区政府主官", "confidence": "confirmed", "source_ids": ["S001", "S006"]},
            {"start": "2024-10", "end": "2024-10", "org": "许昌市人民政府", "title": "许昌市委副书记、市政府党组书记", "level": "正厅级", "location": "河南许昌", "system": "government", "rank": "", "is_key_promotion": True, "notes": "跨省调任", "confidence": "confirmed", "source_ids": ["S001", "S007"]},
            {"start": "2024-10", "end": "2025-02", "org": "许昌市人民政府", "title": "许昌市人民政府市长", "level": "正厅级", "location": "河南许昌", "system": "government", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001", "S008"]},
            {"start": "2025-02", "end": "present", "org": "中共许昌市委员会", "title": "中共许昌市委书记", "level": "正厅级", "location": "河南许昌", "system": "party", "rank": "", "is_key_promotion": True, "notes": "接替被查的史根治", "confidence": "confirmed", "source_ids": ["S001", "S002"]}
        ],
        "organizations": [8],
        "relationships": [
            {"person": "史根治", "person_id": "henan_xuchang_shi_genzhi", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "杨小菁接替被查的史根治任许昌市委书记", "overlap_org": "中共许昌市委员会", "overlap_period": "2025-01至2025-02", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S002"]},
            {"person": "张庆一", "person_id": "henan_xuchang_zhang_qingyi", "relationship_type": "overlap", "strength": "strong", "evidence": "杨小菁任书记、张庆一任市长，党政班子搭档", "overlap_org": "许昌市四大班子", "overlap_period": "2025-02至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
            {"person": "刘涛", "person_id": "henan_xuchang_liu_tao", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "杨小菁接替刘涛任许昌市长", "overlap_org": "许昌市人民政府", "overlap_period": "2024-10", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S001"]}
        ],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": ["组织人事", "党的建设"],
            "secondary_specializations": ["地方治理", "法治建设"],
            "career_pattern": "cross_provincial_rotation",
            "systems_experience": ["organization", "government", "procuratorate", "party"],
            "geographic_pattern": ["上海", "河南"],
            "promotion_velocity": {"summary": "跨省交流干部，从上海青浦区长到许昌市委书记仅用4个月", "notable_fast_promotions": ["2009年从正科提任副处（通过竞争性选拔）", "2024年跨省调任许昌市长，4个月后升任书记"]}
        },
        "work_style_and_personality": {
            "public_style_indicators": [
                {"trait": "technocratic", "evidence": "长期在组织系统工作，法学背景", "confidence": "plausible", "source_ids": ["S001"]}
            ],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, not private psychological assessment."
        },
        "network_metrics": {"cross_province_connections": ["上海-河南"], "key_mentors": []},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "未发现任何纪律处分或负面报道", "date": "2026-07-24", "confidence": "confirmed", "source_ids": []}
        ],
        "source_register": [
            {"id": "S001", "title": "Wikipedia - 杨小菁", "url": "https://zh.wikipedia.org/wiki/杨小菁", "publisher": "Wikipedia", "published_at": "2026-03-22", "accessed_at": "2026-07-24", "source_type": "encyclopedia", "reliability": "medium", "notes": ""},
            {"id": "S002", "title": "澎湃新闻 - 75后杨小菁出任河南许昌市委书记", "url": "https://www.thepaper.cn/newsDetail_forward_30159402", "publisher": "澎湃新闻", "published_at": "2025-02-14", "accessed_at": "2026-07-24", "source_type": "media", "reliability": "high", "notes": ""},
            {"id": "S003", "title": "许昌市人民政府网站", "url": "https://www.xuchang.gov.cn", "publisher": "许昌市人民政府", "published_at": "", "accessed_at": "2026-07-24", "source_type": "official", "reliability": "high", "notes": "网站可访问，领导活动报道确认杨小菁为书记、张庆一为市长"},
            {"id": "S004", "title": "新浪 - 75后上海女厅官履新", "url": "https://news.sina.cn/gn/2019-03-18/detail-ihrfqzkc4910994.d.html", "publisher": "新浪", "published_at": "2019-03-18", "accessed_at": "2026-07-24", "source_type": "media", "reliability": "high", "notes": ""},
            {"id": "S005", "title": "人民网 - 上海市发布四名市管干部提任前公示", "url": "http://renshi.people.com.cn/n1/2016/0926/c139617-28739782.html", "publisher": "人民网", "published_at": "2016-09-26", "accessed_at": "2026-07-24", "source_type": "appointment_notice", "reliability": "high", "notes": ""},
            {"id": "S006", "title": "上观新闻 - 杨小菁任青浦区代区长", "url": "https://web.shobserver.com/wx/detail.do?id=406501", "publisher": "上观新闻", "published_at": "2021-09-17", "accessed_at": "2026-07-24", "source_type": "media", "reliability": "high", "notes": ""},
            {"id": "S007", "title": "上观新闻 - 上海青浦区长杨小菁跨省履新", "url": "https://www.jfdaily.com/news/detail?id=806410", "publisher": "上观新闻", "published_at": "2024-10-12", "accessed_at": "2026-07-24", "source_type": "media", "reliability": "high", "notes": ""},
            {"id": "S008", "title": "中国经济网 - 杨小菁当选许昌市市长", "url": "http://district.ce.cn/newarea/sddy/202410/24/t20241024_39180069.shtml", "publisher": "中国经济网", "published_at": "2024-10-24", "accessed_at": "2026-07-24", "source_type": "media", "reliability": "high", "notes": ""}
        ],
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "partial",
            "relationship_confidence": "high",
            "biggest_gap": "杨小菁1999-2009年在静安区检察院及上海市委组织部的十年详细岗位层级不明确"
        },
        "open_questions": [
            {"priority": "medium", "question": "杨小菁1999-2009年十年间具体职务晋升路径", "why_it_matters": "了解其早期职业基础", "suggested_queries": ["杨小菁 静安区检察院 职务", "杨小菁 上海市委组织部 处长"], "last_attempted": "2026-07-24"},
            {"priority": "low", "question": "杨小菁籍贯具体到镇/街道", "why_it_matters": "更精确的籍贯信息有助于身份溯源", "suggested_queries": ["杨小菁 无锡 出生"], "last_attempted": "2026-07-24"}
        ]
    }

    # ── 张庆一 ──
    zhangqy = {
        "schema_version": "1.0",
        "generated_at": "2026-07-24",
        "investigation_scope": {
            "province": "河南省",
            "city": "许昌市",
            "region": "许昌市",
            "job": "市长",
            "task_id": "henan_许昌市",
            "time_focus": "2025-2026"
        },
        "identity": {
            "person_id": "henan_xuchang_zhang_qingyi",
            "name": "张庆一",
            "aliases": [],
            "gender": "男",
            "ethnicity": "汉族",
            "birth": "1969-03",
            "birthplace": "河南鲁山",
            "native_place": "河南鲁山",
            "education": [
                {"period": "", "institution": "", "major": "理学", "degree": "学士", "study_type": "full_time", "source_ids": ["S010"]},
                {"period": "", "institution": "中共河南省委党校", "major": "", "degree": "研究生", "study_type": "party_school", "source_ids": ["S010"]}
            ],
            "party_join": "中共党员",
            "work_start": "",
            "dedupe_keys": {
                "name_birth": "张庆一_1969-03",
                "name_birthplace": "张庆一_河南鲁山",
                "official_profile_url": "https://www.xuchang.gov.cn"
            }
        },
        "current_status": {
            "current_post": "许昌市人民政府市长",
            "current_org": "许昌市人民政府",
            "administrative_rank": "正厅级",
            "as_of": "2026-07-24",
            "is_current_confirmed": True,
            "source_ids": ["S010", "S011"]
        },
        "career_timeline": [
            {"start": "", "end": "", "org": "宝丰县人民政府", "title": "宝丰县县长", "level": "正处级", "location": "河南平顶山宝丰县", "system": "government", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S010"]},
            {"start": "", "end": "", "org": "中共宝丰县委员会", "title": "宝丰县委书记", "level": "正处级", "location": "河南平顶山宝丰县", "system": "party", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S010"]},
            {"start": "", "end": "2021", "org": "平顶山市人民政府", "title": "平顶山市副市长", "level": "副厅级", "location": "河南平顶山", "system": "government", "rank": "", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S010"]},
            {"start": "2021", "end": "2023", "org": "中共许昌市委员会", "title": "许昌市委常委、统战部部长", "level": "副厅级", "location": "河南许昌", "system": "party", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S010"]},
            {"start": "2023", "end": "2024-09", "org": "许昌市人民政府", "title": "许昌市委常委、常务副市长", "level": "副厅级", "location": "河南许昌", "system": "government", "rank": "", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S010"]},
            {"start": "2024-09", "end": "2025-02", "org": "中共许昌市委员会", "title": "许昌市委副书记、政法委书记", "level": "正厅级", "location": "河南许昌", "system": "party", "rank": "", "is_key_promotion": True, "notes": "", "confidence": "confirmed", "source_ids": ["S010"]},
            {"start": "2025-02", "end": "present", "org": "许昌市人民政府", "title": "许昌市人民政府市长", "level": "正厅级", "location": "河南许昌", "system": "government", "rank": "", "is_key_promotion": True, "notes": "接替升任市委书记的杨小菁", "confidence": "confirmed", "source_ids": ["S010", "S011"]}
        ],
        "organizations": [],
        "relationships": [
            {"person": "杨小菁", "person_id": "henan_xuchang_yang_xiaojing", "relationship_type": "overlap", "strength": "strong", "evidence": "张庆一任市长、杨小菁任书记，党政搭档", "overlap_org": "许昌市四大班子", "overlap_period": "2025-02至今", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S010"]}
        ],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": ["地方治理", "经济管理"],
            "secondary_specializations": [],
            "career_pattern": "local_ladder",
            "systems_experience": ["party", "government"],
            "geographic_pattern": ["河南平顶山", "河南许昌"],
            "promotion_velocity": {"summary": "从平顶山到许昌，逐步晋升至市长", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "未发现任何纪律处分或负面报道", "date": "2026-07-24", "confidence": "confirmed", "source_ids": []}
        ],
        "source_register": [
            {"id": "S010", "title": "Wikipedia - 张庆一", "url": "https://zh.wikipedia.org/wiki/张庆一", "publisher": "Wikipedia", "published_at": "2025-05-12", "accessed_at": "2026-07-24", "source_type": "encyclopedia", "reliability": "medium", "notes": ""},
            {"id": "S011", "title": "腾讯新闻 - 张庆一当选许昌市市长，和杨小菁搭班", "url": "https://news.qq.com", "publisher": "腾讯新闻", "published_at": "2025-02-22", "accessed_at": "2026-07-24", "source_type": "media", "reliability": "high", "notes": ""}
        ],
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "partial",
            "relationship_confidence": "high",
            "biggest_gap": "张庆一早年履历（任宝丰县长之前）不明确，部分岗位具体起止时间缺失"
        },
        "open_questions": [
            {"priority": "high", "question": "张庆一早年职业起点及宝丰县长前的履历", "why_it_matters": "了解其职业根基", "suggested_queries": ["张庆一 简历 宝丰", "张庆一 早期 工作"], "last_attempted": "2026-07-24"},
            {"priority": "medium", "question": "张庆一在宝丰县和平顶山市各具体岗位的起止时间", "why_it_matters": "补充精确的时间线", "suggested_queries": ["张庆一 宝丰 县长 任命", "张庆一 平顶山 副市长 任职时间"], "last_attempted": "2026-07-24"}
        ]
    }

    # Write files
    persons_config = [
        ("20260724-河南省-许昌市-市委书记-杨小菁.json", yangxj),
        ("20260724-河南省-许昌市-市长-张庆一.json", zhangqy),
    ]

    for fname, data in persons_config:
        fpath = os.path.join(PERSONS_DIR, fname)
        with open(fpath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        files_written.append(fpath)

    return files_written


if __name__ == "__main__":
    raise SystemExit(main())
