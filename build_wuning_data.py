#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Wuning County (武宁县) leadership network."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/wuning_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/wuning_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current and Recent Wuning County Party Secretaries ──
    {"id": 1, "name": "张宇峰", "gender": "男", "ethnicity": "汉族",
     "birth": "1984-03", "birthplace": "江西分宜", "education": "大学/工程硕士",
     "party_join": "2006-12", "work_start": "2005-07",
     "current_post": "中共武宁县委书记", "current_org": "中共武宁县委员会",
     "source": "https://baike.baidu.com/item/%E5%BC%A0%E5%AE%87%E5%B3%B0/64882479"},
    {"id": 2, "name": "洪碧霞", "gender": "女", "ethnicity": "汉族",
     "birth": "1974-07", "birthplace": "江西都昌", "education": "江西师范大学学士",
     "party_join": "2000-03", "work_start": "1997-08",
     "current_post": "原武宁县委书记（已免）", "current_org": "中共武宁县委员会",
     "source": "https://baike.baidu.com/item/%E6%B4%AA%E7%A2%A7%E9%9C%9E"},
    {"id": 3, "name": "杜少华", "gender": "男", "ethnicity": "汉族",
     "birth": "1969-06", "birthplace": "江西瑞昌", "education": "中央党校大学",
     "party_join": "1996-06", "work_start": "1988-07",
     "current_post": "九江市政府副市长、党组成员", "current_org": "九江市人民政府",
     "source": "https://baike.baidu.com/item/%E6%9D%9C%E5%B0%91%E5%8D%8E"},

    # ── Current Wuning County Government Leaders ──
    {"id": 4, "name": "陈磊", "gender": "男", "ethnicity": "汉族",
     "birth": "1982-07", "birthplace": "", "education": "在职研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武宁县委副书记、县人民政府代县长", "current_org": "武宁县人民政府",
     "source": "https://baike.baidu.com/item/%E9%99%88%E7%A3%8A(3)"},
    {"id": 5, "name": "伍术刚", "gender": "男", "ethnicity": "汉族",
     "birth": "1982-09", "birthplace": "江西都昌", "education": "研究生/管理学学士",
     "party_join": "2004-05", "work_start": "2005-08",
     "current_post": "武宁县委常委、常务副县长", "current_org": "武宁县人民政府",
     "source": "https://www.wuning.gov.cn"},
    {"id": 6, "name": "黄蓝", "gender": "女", "ethnicity": "汉族",
     "birth": "1981-08", "birthplace": "湖北黄梅", "education": "研究生/农业推广硕士",
     "party_join": "2006-10", "work_start": "1998-08",
     "current_post": "都昌县委常委、常务副县长", "current_org": "都昌县人民政府",
     "source": "https://baike.baidu.com/item/%E9%BB%84%E8%93%9D"},

    # ── Key Deputy Leaders ──
    {"id": 7, "name": "谢庆平", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武宁县委副书记", "current_org": "中共武宁县委员会",
     "source": "https://www.wuning.gov.cn"},
    {"id": 8, "name": "刘名寿", "gender": "男", "ethnicity": "汉族",
     "birth": "1982-03", "birthplace": "", "education": "在职研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "修水县委副书记、县政府代县长", "current_org": "修水县人民政府",
     "source": "https://www.xiushui.gov.cn"},

    # ── Current Standing Committee Members (2026) ──
    {"id": 9, "name": "帅中华", "gender": "男", "ethnicity": "汉族",
     "birth": "1980-07", "birthplace": "江西庐山", "education": "江西省委党校研究生",
     "party_join": "2006-02", "work_start": "1997-08",
     "current_post": "（原武宁县委常委、组织部部长，已调离）", "current_org": "",
     "source": "https://baike.baidu.com/item/%E5%B8%85%E4%B8%AD%E5%8D%8E"},
    {"id": 10, "name": "周雷生", "gender": "男", "ethnicity": "汉族",
     "birth": "1983-01", "birthplace": "", "education": "研究生/工学硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武宁县委常委、宣传部部长", "current_org": "中共武宁县委员会",
     "source": "https://www.wuning.gov.cn"},
    {"id": 11, "name": "陈绪洲", "gender": "男", "ethnicity": "汉族",
     "birth": "1969-12", "birthplace": "江西武宁", "education": "研究生",
     "party_join": "中共党员", "work_start": "1992-08",
     "current_post": "武宁县委常委、统战部部长", "current_org": "中共武宁县委员会",
     "source": "https://baike.baidu.com/item/%E9%99%88%E7%BB%AA%E6%B4%B2"},
    {"id": 12, "name": "马呈", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武宁县委常委", "current_org": "中共武宁县委员会",
     "source": "https://www.wuning.gov.cn"},
    {"id": 13, "name": "黄志", "gender": "男", "ethnicity": "汉族",
     "birth": "1979", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武宁县委常委、县纪委书记、县监委主任", "current_org": "中共武宁县纪律检查委员会",
     "source": "https://www.wuning.gov.cn"},
    {"id": 14, "name": "胡剑", "gender": "男", "ethnicity": "汉族",
     "birth": "1979-10", "birthplace": "江西永修", "education": "研究生",
     "party_join": "2001-07", "work_start": "1997-09",
     "current_post": "（原武宁县委常委、县纪委书记，已调离）", "current_org": "",
     "source": "https://baike.baidu.com/item/%E8%83%A1%E5%89%91"},
    {"id": 15, "name": "朱良光", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武宁县委常委、县人武部政委", "current_org": "武宁县人民武装部",
     "source": "https://www.wuning.gov.cn"},
    {"id": 16, "name": "颉勇军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武宁县委常委", "current_org": "中共武宁县委员会",
     "source": "https://www.wuning.gov.cn"},
    {"id": 17, "name": "冷碧滨", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武宁县委常委", "current_org": "中共武宁县委员会",
     "source": "https://www.wuning.gov.cn"},

    # ── Deputy Mayors ──
    {"id": 18, "name": "王静", "gender": "女", "ethnicity": "汉族",
     "birth": "1973-09", "birthplace": "", "education": "中央党校大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武宁县政府党组成员、副县长", "current_org": "武宁县人民政府",
     "source": "https://www.wuning.gov.cn"},
    {"id": 19, "name": "卢恒墀", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武宁县副县长", "current_org": "武宁县人民政府",
     "source": "https://www.wuning.gov.cn"},
    {"id": 20, "name": "武文斌", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武宁县副县长", "current_org": "武宁县人民政府",
     "source": "https://www.wuning.gov.cn"},
    {"id": 21, "name": "胡德玉", "gender": "男", "ethnicity": "汉族",
     "birth": "1980-09", "birthplace": "江西庐山", "education": "省委党校大专",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武宁县副县长", "current_org": "武宁县人民政府",
     "source": "https://www.wuning.gov.cn"},
    {"id": 22, "name": "艾志勇", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武宁县副县长", "current_org": "武宁县人民政府",
     "source": "https://www.wuning.gov.cn"},
    {"id": 23, "name": "匡志军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武宁县副县长、县公安局局长", "current_org": "武宁县人民政府",
     "source": "https://www.wuning.gov.cn"},
    {"id": 24, "name": "吴伟华", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武宁县副县长", "current_org": "武宁县人民政府",
     "source": "https://www.wuning.gov.cn"},
    {"id": 25, "name": "杨桦", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武宁县政府党组成员", "current_org": "武宁县人民政府",
     "source": "https://www.wuning.gov.cn"},

    # ── Predecessors (former mayors) ──
    {"id": 26, "name": "李广松", "gender": "男", "ethnicity": "汉族",
     "birth": "1966-03", "birthplace": "", "education": "大学/农业推广硕士",
     "party_join": "中共党员", "work_start": "1985-08",
     "current_post": "（原武宁县县长）", "current_org": "",
     "source": "https://www.wuning.gov.cn"},

    # ── Other notable figures ──
    {"id": 27, "name": "李立为", "gender": "男", "ethnicity": "汉族",
     "birth": "1966-10", "birthplace": "", "education": "中央党校大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武宁县人大常委会主任", "current_org": "武宁县人大常委会",
     "source": "https://www.wuning.gov.cn"},
    {"id": 28, "name": "王仁华", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "武宁县政协主席", "current_org": "武宁县政协",
     "source": "https://www.wuning.gov.cn"},
]

organizations = [
    {"id": 1, "name": "中共武宁县委员会", "type": "党委", "level": "县处级", "parent": "中共九江市委员会", "location": "江西九江武宁"},
    {"id": 2, "name": "武宁县人民政府", "type": "政府", "level": "县处级", "parent": "九江市人民政府", "location": "江西九江武宁"},
    {"id": 3, "name": "中共武宁县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共九江市纪律检查委员会", "location": "江西九江武宁"},
    {"id": 4, "name": "武宁县人民武装部", "type": "军事", "level": "县处级", "parent": "", "location": "江西九江武宁"},
    {"id": 5, "name": "武宁县人大常委会", "type": "人大", "level": "县处级", "parent": "", "location": "江西九江武宁"},
    {"id": 6, "name": "武宁县政协", "type": "政协", "level": "县处级", "parent": "", "location": "江西九江武宁"},
    {"id": 7, "name": "九江市人民政府", "type": "政府", "level": "厅级", "parent": "江西省人民政府", "location": "江西九江"},
    {"id": 8, "name": "修水县人民政府", "type": "政府", "level": "县处级", "parent": "九江市人民政府", "location": "江西九江修水"},
    {"id": 9, "name": "都昌县人民政府", "type": "政府", "level": "县处级", "parent": "九江市人民政府", "location": "江西九江都昌"},
    {"id": 10, "name": "中共修水县委员会", "type": "党委", "level": "县处级", "parent": "中共九江市委员会", "location": "江西九江修水"},
]

positions = [
    # ── Zhang Yufeng (张宇峰) career ──
    {"id": 1, "person_id": 1, "org_id": 1, "title": "中共武宁县委书记", "start": "2026-05", "end": "", "rank": "县处级正职", "note": "现任"},
    {"id": 2, "person_id": 1, "org_id": 2, "title": "武宁县人民政府县长", "start": "2021-08", "end": "2026-05", "rank": "县处级正职", "note": "前任职务"},
    {"id": 3, "person_id": 1, "org_id": 1, "title": "武宁县委副书记、县长候选人", "start": "2021-07", "end": "2021-08", "rank": "县处级正职", "note": ""},
    # ── Earlier career: Xinyu system ──
    {"id": 61, "person_id": 1, "org_id": 1, "title": "新余市应急管理局局长", "start": "", "end": "2021-07", "rank": "县处级正职", "note": "前任职务（新余市）"},
    {"id": 62, "person_id": 1, "org_id": 1, "title": "新余高新区党工委副书记", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"id": 63, "person_id": 1, "org_id": 2, "title": "新余市渝水区副区长", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"id": 64, "person_id": 1, "org_id": 1, "title": "分宜县操场乡乡长", "start": "", "end": "", "rank": "乡科级正职", "note": ""},
    {"id": 65, "person_id": 1, "org_id": 1, "title": "共青团分宜县委干部", "start": "", "end": "", "rank": "", "note": "早期任职"},
    {"id": 66, "person_id": 1, "org_id": 1, "title": "新余市纪委副科级纪检员", "start": "", "end": "", "rank": "乡科级副职", "note": ""},
    {"id": 67, "person_id": 1, "org_id": 1, "title": "新余市行政服务管理委员会干部", "start": "2005-07", "end": "", "rank": "", "note": "第一份工作"},

    # ── Hong Bixia (洪碧霞) career ──
    {"id": 4, "person_id": 2, "org_id": 1, "title": "中共武宁县委书记", "start": "2021-08", "end": "2026-05", "rank": "县处级正职", "note": ""},
    {"id": 5, "person_id": 2, "org_id": 1, "title": "九江市妇联党组书记、主席", "start": "", "end": "2021-07", "rank": "县处级正职", "note": "前任职务"},
    {"id": 6, "person_id": 2, "org_id": 1, "title": "九江市八里湖新区党工委副书记", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"id": 7, "person_id": 2, "org_id": 2, "title": "德安县委常委、副县长", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"id": 8, "person_id": 2, "org_id": 1, "title": "都昌县左里镇党委书记", "start": "", "end": "", "rank": "乡科级正职", "note": ""},
    {"id": 9, "person_id": 2, "org_id": 2, "title": "都昌县南峰镇副镇长", "start": "", "end": "", "rank": "乡科级副职", "note": ""},
    {"id": 10, "person_id": 2, "org_id": 1, "title": "都昌县职工学校教师", "start": "1997-08", "end": "", "rank": "", "note": "第一份工作"},

    # ── Du Shaohua (杜少华) career ──
    {"id": 11, "person_id": 3, "org_id": 7, "title": "九江市政府副市长、党组成员", "start": "2021-10", "end": "", "rank": "副厅级", "note": "现任"},
    {"id": 12, "person_id": 3, "org_id": 1, "title": "中共武宁县委书记", "start": "2016-08", "end": "2021-08", "rank": "县处级正职", "note": ""},
    {"id": 13, "person_id": 3, "org_id": 2, "title": "永修县委副书记、县长", "start": "", "end": "2016-08", "rank": "县处级正职", "note": ""},
    {"id": 14, "person_id": 3, "org_id": 1, "title": "九江市委市政府台办主任、经开区党工委副书记", "start": "", "end": "", "rank": "县处级正职", "note": ""},
    {"id": 15, "person_id": 3, "org_id": 1, "title": "九江市旅游局局长", "start": "", "end": "", "rank": "县处级正职", "note": ""},
    {"id": 16, "person_id": 3, "org_id": 7, "title": "九江市政府办公厅副主任", "start": "", "end": "", "rank": "县处级副职", "note": ""},
    {"id": 17, "person_id": 3, "org_id": 7, "title": "瑞昌市政府办公室秘书、副主任", "start": "", "end": "", "rank": "", "note": "瑞昌市教师起步"},

    # ── Chen Lei (陈磊) career ──
    {"id": 18, "person_id": 4, "org_id": 2, "title": "武宁县委副书记、县人民政府代县长", "start": "2026-07", "end": "", "rank": "县处级正职", "note": "新任代县长"},
    {"id": 19, "person_id": 4, "org_id": 1, "title": "武宁县委副书记、县长候选人", "start": "2026-05", "end": "2026-07", "rank": "县处级正职", "note": ""},

    # ── Wu Shugang (伍术刚) career ──
    {"id": 20, "person_id": 5, "org_id": 2, "title": "武宁县委常委、常务副县长", "start": "2024-11", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 21, "person_id": 5, "org_id": 9, "title": "都昌县委常委、常务副县长", "start": "2021", "end": "2024-11", "rank": "县处级副职", "note": "前任职务"},
    {"id": 22, "person_id": 5, "org_id": 1, "title": "共青城苏家垱乡党委书记", "start": "", "end": "", "rank": "乡科级正职", "note": ""},
    {"id": 23, "person_id": 5, "org_id": 1, "title": "共青城江益镇党委委员、镇长", "start": "", "end": "", "rank": "乡科级正职", "note": ""},
    {"id": 24, "person_id": 5, "org_id": 1, "title": "共青城开放开发区社会发展局干部", "start": "2005-08", "end": "", "rank": "", "note": "第一份工作"},

    # ── Huang Lan (黄蓝) career ──
    {"id": 25, "person_id": 6, "org_id": 9, "title": "都昌县委常委、常务副县长", "start": "2024-11", "end": "", "rank": "县处级副职", "note": "现任（由武宁调任）"},
    {"id": 26, "person_id": 6, "org_id": 2, "title": "武宁县委常委、常务副县长", "start": "2020-08", "end": "2024-11", "rank": "县处级副职", "note": ""},

    # ── Xie Qingping (谢庆平) career ──
    {"id": 27, "person_id": 7, "org_id": 1, "title": "武宁县委副书记", "start": "", "end": "", "rank": "县处级副职", "note": "现任，具体到任时间不详"},

    # ── Liu Mingshou (刘名寿) career ──
    {"id": 28, "person_id": 8, "org_id": 8, "title": "修水县委副书记、县政府代县长", "start": "2026-07", "end": "", "rank": "县处级正职", "note": "新任"},
    {"id": 29, "person_id": 8, "org_id": 1, "title": "武宁县委副书记", "start": "2021-08", "end": "2026-07", "rank": "县处级副职", "note": ""},

    # ── Standing Committee ──
    {"id": 30, "person_id": 9, "org_id": 1, "title": "武宁县委常委、组织部部长", "start": "2021-09", "end": "2026-01", "rank": "县处级副职", "note": "已调离武宁"},
    {"id": 31, "person_id": 10, "org_id": 1, "title": "武宁县委常委、宣传部部长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 32, "person_id": 11, "org_id": 1, "title": "武宁县委常委、统战部部长", "start": "2021-09", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 33, "person_id": 12, "org_id": 1, "title": "武宁县委常委", "start": "2021-09", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 34, "person_id": 13, "org_id": 3, "title": "武宁县委常委、县纪委书记、县监委主任", "start": "2024-05", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 35, "person_id": 14, "org_id": 3, "title": "武宁县委常委、县纪委书记", "start": "2021-09", "end": "2024-05", "rank": "县处级副职", "note": ""},
    {"id": 36, "person_id": 15, "org_id": 4, "title": "武宁县委常委、县人武部政委", "start": "2021-09", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 37, "person_id": 16, "org_id": 1, "title": "武宁县委常委", "start": "2021-09", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 38, "person_id": 17, "org_id": 1, "title": "武宁县委常委", "start": "2021-09", "end": "", "rank": "县处级副职", "note": "现任"},

    # ── Deputy Mayors ──
    {"id": 39, "person_id": 18, "org_id": 2, "title": "武宁县政府党组成员、副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 40, "person_id": 19, "org_id": 2, "title": "武宁县副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 41, "person_id": 20, "org_id": 2, "title": "武宁县副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 42, "person_id": 21, "org_id": 2, "title": "武宁县副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 43, "person_id": 22, "org_id": 2, "title": "武宁县副县长", "start": "2024-11", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 44, "person_id": 23, "org_id": 2, "title": "武宁县副县长、县公安局局长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 45, "person_id": 24, "org_id": 2, "title": "武宁县副县长", "start": "", "end": "", "rank": "县处级副职", "note": "现任"},
    {"id": 46, "person_id": 25, "org_id": 2, "title": "武宁县政府党组成员", "start": "", "end": "", "rank": "县处级", "note": "现任"},

    # ── Li Guangsong (李广松) career ──
    {"id": 47, "person_id": 26, "org_id": 2, "title": "武宁县人民政府县长", "start": "2016-08", "end": "2021-08", "rank": "县处级正职", "note": ""},
    {"id": 48, "person_id": 26, "org_id": 2, "title": "德安县委副书记", "start": "", "end": "2016-08", "rank": "县处级副职", "note": "拟任武宁县长前职务"},

    # ── Li Liwei (李立为) career ──
    {"id": 49, "person_id": 27, "org_id": 5, "title": "武宁县人大常委会主任", "start": "2021", "end": "", "rank": "县处级正职", "note": "现任"},
    {"id": 50, "person_id": 27, "org_id": 1, "title": "武宁县委常委、政法委书记", "start": "", "end": "2021", "rank": "县处级副职", "note": ""},

    # ── Wang Renhua (王仁华) career ──
    {"id": 51, "person_id": 28, "org_id": 6, "title": "武宁县政协主席", "start": "", "end": "", "rank": "县处级正职", "note": "现任"},
]

relationships = [
    # ── Predecessor-Successor (Party Secretaries) ──
    {"id": 1, "person_a_id": 2, "person_b_id": 1, "type": "交接", "context": "洪碧霞→张宇峰 武宁县委书记交接（2026年5月）", "overlap_org": "中共武宁县委员会", "overlap_period": "2026-05"},
    {"id": 2, "person_a_id": 3, "person_b_id": 2, "type": "交接", "context": "杜少华→洪碧霞 武宁县委书记交接（2021年8月）", "overlap_org": "中共武宁县委员会", "overlap_period": "2021-08"},

    # ── Predecessor-Successor (County Mayors) ──
    {"id": 3, "person_a_id": 26, "person_b_id": 1, "type": "交接", "context": "李广松→张宇峰 武宁县县长交接（2021年8月）", "overlap_org": "武宁县人民政府", "overlap_period": "2021-08"},
    {"id": 4, "person_a_id": 1, "person_b_id": 4, "type": "交接", "context": "张宇峰→陈磊 武宁县县长交接（2026年7月）", "overlap_org": "武宁县人民政府", "overlap_period": "2026-07"},

    # ── County Mayor-Secretary connections ──
    {"id": 5, "person_a_id": 2, "person_b_id": 1, "type": "党政搭档", "context": "洪碧霞任县委书记时，张宇峰任县长（2021.08-2026.05）", "overlap_org": "中共武宁县委员会", "overlap_period": "2021-2026"},
    {"id": 6, "person_a_id": 3, "person_b_id": 26, "type": "党政搭档", "context": "杜少华任县委书记时，李广松任县长（2016.08-2021.08）", "overlap_org": "中共武宁县委员会", "overlap_period": "2016-2021"},

    # ── Deputy transfers ──
    {"id": 7, "person_a_id": 6, "person_b_id": 5, "type": "职务交接", "context": "黄蓝→伍术刚 武宁县常务副县长交接（2024年11月）", "overlap_org": "武宁县人民政府", "overlap_period": "2024-11"},
    {"id": 8, "person_a_id": 6, "person_b_id": 5, "type": "跨县调任", "context": "黄蓝由武宁调任都昌常务副县长，伍术刚由都昌调任武宁常务副县长（对调模式）", "overlap_org": "", "overlap_period": "2024-11"},

    # ── Deputy Secretary transfers ──
    {"id": 9, "person_a_id": 8, "person_b_id": 7, "type": "职务交接", "context": "刘名寿→谢庆平 武宁县委副书记交接（2026年7月）", "overlap_org": "中共武宁县委员会", "overlap_period": "2026-07"},

    # ── Standing Committee coworkers ──
    {"id": 10, "person_a_id": 9, "person_b_id": 10, "type": "同僚", "context": "帅中华与周雷生均为武宁县委常委（组织、宣传）", "overlap_org": "中共武宁县委员会", "overlap_period": ""},
    {"id": 11, "person_a_id": 11, "person_b_id": 10, "type": "同僚", "context": "陈绪洲与周雷生均为武宁县委常委", "overlap_org": "中共武宁县委员会", "overlap_period": ""},
    {"id": 12, "person_a_id": 13, "person_b_id": 14, "type": "职务交接", "context": "黄志接替胡剑任武宁县纪委书记（2024年5月）", "overlap_org": "中共武宁县纪律检查委员会", "overlap_period": "2024-05"},

    # ── Cross-county exchanges ──
    {"id": 13, "person_a_id": 3, "person_b_id": 8, "type": "跨县关联", "context": "杜少华（瑞昌人）→刘名寿（调修水县长），武宁→修水人事通道", "overlap_org": "", "overlap_period": "2026"},
    {"id": 14, "person_a_id": 2, "person_b_id": 5, "type": "同乡关联", "context": "洪碧霞与伍术刚均为都昌人", "overlap_org": "", "overlap_period": ""},

    # ── Zhang Yufeng's cross-city background ──
    {"id": 15, "person_a_id": 1, "person_b_id": 3, "type": "跨市调任关联", "context": "张宇峰由新余市调任武宁县（2021年），属跨市交流", "overlap_org": "", "overlap_period": "2021"},
]

# ── BUILD SQLite DATABASE ────────────────────────────────────────────

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
CREATE TABLE persons (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    gender TEXT,
    ethnicity TEXT,
    birth TEXT,
    birthplace TEXT,
    education TEXT,
    party_join TEXT,
    work_start TEXT,
    current_post TEXT,
    current_org TEXT,
    source TEXT
);

CREATE TABLE organizations (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT,
    level TEXT,
    parent TEXT,
    location TEXT
);

CREATE TABLE positions (
    id INTEGER PRIMARY KEY,
    person_id INTEGER NOT NULL,
    org_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    start TEXT,
    end TEXT,
    rank TEXT,
    note TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);

CREATE TABLE relationships (
    id INTEGER PRIMARY KEY,
    person_a_id INTEGER NOT NULL,
    person_b_id INTEGER NOT NULL,
    type TEXT NOT NULL,
    context TEXT,
    overlap_org TEXT,
    overlap_period TEXT,
    FOREIGN KEY (person_a_id) REFERENCES persons(id),
    FOREIGN KEY (person_b_id) REFERENCES persons(id)
);
""")

for p in persons:
    cur.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                 p["birthplace"], p["education"], p["party_join"], p["work_start"],
                 p["current_post"], p["current_org"], p["source"]))

for o in organizations:
    cur.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""",
                (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for pos in positions:
    cur.execute("""INSERT INTO positions VALUES (?,?,?,?,?,?,?,?)""",
                (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
                 pos["start"], pos["end"], pos["rank"], pos["note"]))

for r in relationships:
    cur.execute("""INSERT INTO relationships VALUES (?,?,?,?,?,?,?)""",
                (r["id"], r["person_a_id"], r["person_b_id"], r["type"],
                 r["context"], r["overlap_org"], r["overlap_period"]))

conn.commit()

# Summary stats
cur.execute("SELECT COUNT(*) FROM persons")
person_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM organizations")
org_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM positions")
pos_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM relationships")
rel_count = cur.fetchone()[0]

conn.close()
print(f"SQLite database written: {DB_PATH}")
print(f"  Persons: {person_count}")
print(f"  Organizations: {org_count}")
print(f"  Positions: {pos_count}")
print(f"  Relationships: {rel_count}")


# ── BUILD GEXF GRAPH ────────────────────────────────────────────────

today = datetime.now().strftime("%Y-%m-%d")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append(f'<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{today}">')
lines.append('    <creator>china-gov-network skill</creator>')
lines.append(f'    <description>武宁县领导班子工作关系网络 - {today}</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# ── Attributes ──
lines.append('    <attributes class="node">')
lines.append('      <attribute id="type" title="Type" type="string"/>')
lines.append('      <attribute id="category" title="Category" type="string"/>')
lines.append('      <attribute id="birth" title="Birth" type="string"/>')
lines.append('      <attribute id="birthplace" title="Birthplace" type="string"/>')
lines.append('      <attribute id="education" title="Education" type="string"/>')
lines.append('      <attribute id="current_post" title="Current Post" type="string"/>')
lines.append('      <attribute id="source" title="Source" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="type" title="Type" type="string"/>')
lines.append('      <attribute id="context" title="Context" type="string"/>')
lines.append('      <attribute id="period" title="Period" type="string"/>')
lines.append('    </attributes>')

# ── Nodes: Persons ──
lines.append('    <nodes>')
for p in persons:
    if p["id"] in [1, 2, 3]:
        color = '#E03C31'  # red: Party Secretary
        size = 20.0
    elif p["id"] in [4, 5, 26]:
        color = '#2980B9'  # blue: government leader
        size = 18.0
    elif p["id"] in [6, 8]:
        color = '#8E44AD'  # purple: transferred out
        size = 14.0
    elif p["id"] in [13, 14]:
        color = '#E67E22'  # orange: discipline
        size = 16.0
    else:
        color = '#95A5A6'  # grey: others
        size = 12.0

    lines.append(f'      <node id="{p["id"]}" label="{p["name"]}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="person"/>')
    lines.append(f'          <attvalue for="category" value="person"/>')
    lines.append(f'          <attvalue for="birth" value="{p["birth"]}"/>')
    lines.append(f'          <attvalue for="birthplace" value="{p["birthplace"]}"/>')
    lines.append(f'          <attvalue for="education" value="{p["education"]}"/>')
    lines.append(f'          <attvalue for="current_post" value="{p["current_post"]}"/>')
    lines.append(f'          <attvalue for="source" value="{p["source"]}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{int(color[1:3], 16)}" g="{int(color[3:5], 16)}" b="{int(color[5:7], 16)}"/>')
    lines.append(f'        <viz:size value="{size}"/>')
    lines.append(f'      </node>')

# ── Nodes: Organizations ──
for o in organizations:
    oid = 1000 + o["id"]
    lines.append(f'      <node id="{oid}" label="{o["name"]}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="org"/>')
    lines.append(f'          <attvalue for="category" value="{o["type"]}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="44" g="62" b="80"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append(f'      </node>')
lines.append('    </nodes>')

# ── Edges ──
lines.append('    <edges>')
edge_id = 1

# person→organization (worked_at)
for pos in positions:
    oid = 1000 + pos["org_id"]
    lines.append(f'      <edge id="{edge_id}" source="{pos["person_id"]}" target="{oid}" label="worked_at">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="worked_at"/>')
    lines.append(f'          <attvalue for="context" value="{pos["title"]}"/>')
    lines.append(f'          <attvalue for="period" value="{pos["start"] or "?"} → {pos["end"] or "今"}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')
    edge_id += 1

# person↔person (relationships)
for r in relationships:
    lines.append(f'      <edge id="{edge_id}" source="{r["person_a_id"]}" target="{r["person_b_id"]}" label="{r["type"]}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="{r["type"]}"/>')
    lines.append(f'          <attvalue for="context" value="{r["context"]}"/>')
    lines.append(f'          <attvalue for="period" value="{r["overlap_period"]}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')
    edge_id += 1

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

total_nodes = len(persons) + len(organizations)
total_edges = len(positions) + len(relationships)
print(f"\nGEXF graph written: {GEXF_PATH}")
print(f"  Nodes: {len(persons)} persons + {len(organizations)} organizations = {total_nodes} total")
print(f"  Edges: {len(positions)} worked_at + {len(relationships)} relationships = {total_edges} total")
print("\nDone!")
