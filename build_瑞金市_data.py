#!/usr/bin/env python3
"""
瑞金市领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Ruijin City (瑞金市, 赣州市, 江西省) leadership.

Research date: 2026-07-15
Research method: ruijin.gov.cn, Baidu search, news reports (汲古新知, 澎湃新闻, 人民网, etc.)

Key findings as of July 2026:
- Major leadership change in July 2026:
  - 蓝贤林 (from 寻乌县委书记) appointed 瑞金市委书记, 瑞金经开区党工委书记
  - 彭民生 (from 赣州市供销联社) appointed 瑞金市委副书记、市长候选人
  - 尹忠 (former 瑞金市委书记) promoted to 赣州市委常委
  - 刘春林 (former 瑞金市长) transferred to 崇义县委书记

Sources:
  - https://www.ruijin.gov.cn (瑞金市人民政府)
  - https://www.ruijin.gov.cn/zwgk/ldzc/ (领导之窗)
  - https://ruijin.gov.cn/ (瑞金党务公开网)
  - Baidu Baike: 尹忠, 蓝贤林, 刘春林, 彭民生
  - News reports: 汲古新知, 澎湃新闻, 人民网, 中国青年网
  - 瑞金市第七届人民代表大会第六次会议政府工作报告 (2026-01-16)
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/tmp/jiangxi_瑞金市/瑞金市_network.db")
GEXF_PATH = os.path.join(BASE, "data/tmp/jiangxi_瑞金市/瑞金市_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ══ Current Party Secretary (市委书记) — 蓝贤林 (NEW July 2026) ══
    {"id": 1, "name": "蓝贤林", "gender": "男", "ethnicity": "畲族",
     "birth": "1979-10", "birthplace": "江西南康", "education": "硕士研究生，法学硕士",
     "party_join": "2001-12", "work_start": "2005-09",
     "current_post": "瑞金市委书记、瑞金经开区党工委书记", "current_org": "中共瑞金市委员会",
     "source": "ruijin.gov.cn; 百度百科; 汲古新知; 寻乌县人民政府"},

    # ══ Current Mayor Candidate (市长候选人) — 彭民生 (NEW July 2026) ══
    {"id": 2, "name": "彭民生", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-12", "birthplace": "江西大余", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "1992-08",
     "current_post": "瑞金市委副书记、市长候选人, 瑞金经开区党工委副书记、管委会主任提名人选",
     "current_org": "瑞金市人民政府",
     "source": "ruijin.gov.cn; 百度百科; 赣州市人民政府"},

    # ══ Previous Party Secretary (前任市委书记, 已升赣州市委常委) — 尹忠 ══
    {"id": 3, "name": "尹忠", "gender": "男", "ethnicity": "汉族",
     "birth": "1969-01", "birthplace": "江西赣县", "education": "大学本科，法学学士（南昌大学）",
     "party_join": "1992-03", "work_start": "1989-07",
     "current_post": "赣州市委常委", "current_org": "中共赣州市委员会",
     "source": "百度百科; 人民网; 中国经济网; 北青政知新媒体"},

    # ══ Previous Mayor (前任市长, 已调崇义县委书记) — 刘春林 ══
    {"id": 4, "name": "刘春林", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-01", "birthplace": "江西会昌", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "崇义县委书记", "current_org": "中共崇义县委员会",
     "source": "ruijin.gov.cn; 百度百科; 汲古新知; 瑞金网"},

    # ══ Previous Party Secretary (前任市委书记) — 吴建平 ══
    {"id": 5, "name": "吴建平", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "（原瑞金市委书记，已调离）", "current_org": "",
     "source": "百度百科; 中国青年网"},

    # ══市委副书记 — 李志坚 ══
    {"id": 6, "name": "李志坚", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瑞金市委副书记", "current_org": "中共瑞金市委员会",
     "source": "瑞金党务公开网"},

    # ══市委副书记 — 张雷 ══
    {"id": 7, "name": "张雷", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瑞金市委副书记（分管群团、旅游）", "current_org": "中共瑞金市委员会",
     "source": "瑞金党务公开网"},

    # ══市委常委、纪委书记 — 温秋宁 ══
    {"id": 8, "name": "温秋宁", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瑞金市委常委、市纪委书记、市监委代理主任", "current_org": "中共瑞金市纪律检查委员会",
     "source": "瑞金党务公开网"},

    # ══市委常委、宣传部长 — 陈建伟 ══
    {"id": 9, "name": "陈建伟", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瑞金市委常委、宣传部部长", "current_org": "中共瑞金市委宣传部",
     "source": "瑞金党务公开网; 百度百科"},

    # ══市委常委、统战部长 — 蒋小英 ══
    {"id": 10, "name": "蒋小英", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瑞金市委常委、统战部部长", "current_org": "中共瑞金市委统战部",
     "source": "瑞金党务公开网"},

    # ══市委常委、组织部长 — 刘新远 ══
    {"id": 11, "name": "刘新远", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瑞金市委常委、组织部部长", "current_org": "中共瑞金市委组织部",
     "source": "瑞金党务公开网; 百度百科"},

    # ══市委常委、政法委书记 — 涂佐明 ══
    {"id": 12, "name": "涂佐明", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瑞金市委常委、政法委书记", "current_org": "中共瑞金市委政法委员会",
     "source": "瑞金党务公开网"},

    # ══市委常委、副市长 — 黄发亮 ══
    {"id": 13, "name": "黄发亮", "gender": "男", "ethnicity": "汉族",
     "birth": "1977-07", "birthplace": "江西于都", "education": "省委党校研究生",
     "party_join": "1999-01", "work_start": "1999-08",
     "current_post": "瑞金市委常委、副市长", "current_org": "瑞金市人民政府",
     "source": "瑞金市人民政府"},

    # ══市委常委、人武部政委 — 魏红军 ══
    {"id": 14, "name": "魏红军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瑞金市委常委、人武部政委", "current_org": "瑞金市人民武装部",
     "source": "瑞金党务公开网"},

    # ══市委常委 — 吴迪 ══
    {"id": 15, "name": "吴迪", "gender": "男", "ethnicity": "汉族",
     "birth": "1983-03", "birthplace": "黑龙江庆安", "education": "研究生学历",
     "party_join": "2002-12", "work_start": "2008-08",
     "current_post": "瑞金市委常委、市政府党组成员、副市长", "current_org": "瑞金市人民政府",
     "source": "百度百科"},

    # ══市政府副市长 — 刘方淼 ══
    {"id": 16, "name": "刘方淼", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瑞金市政府副市长、党组成员", "current_org": "瑞金市人民政府",
     "source": "瑞金市人民政府"},

    # ══市政府副市长 — 许毅 ══
    {"id": 17, "name": "许毅", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瑞金市政府副市长、党组成员", "current_org": "瑞金市人民政府",
     "source": "瑞金市人民政府"},

    # ══市政府副市长 — 何世泽 ══
    {"id": 18, "name": "何世泽", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瑞金市政府副市长、党组成员", "current_org": "瑞金市人民政府",
     "source": "瑞金市人民政府"},

    # ══市政府副市长 — 王林 ══
    {"id": 19, "name": "王林", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瑞金市政府副市长、党组成员", "current_org": "瑞金市人民政府",
     "source": "瑞金市人民政府"},

    # ══市人大常委会主任 — 谢志斌 ══
    {"id": 20, "name": "谢志斌", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瑞金市人大常委会主任", "current_org": "瑞金市人民代表大会常务委员会",
     "source": "瑞金市人民政府; 瑞金网"},

    # ══市政协主席 — 刘红敏 ══
    {"id": 21, "name": "刘红敏", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瑞金市政协主席", "current_org": "中国人民政治协商会议瑞金市委员会",
     "source": "瑞金市人民政府"},

    # ══瑞金经开区党工委原副书记 — 罗林生 ══
    {"id": 22, "name": "罗林生", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "瑞金市委常委、瑞金市人民政府副市长、瑞金经开区党工委副书记", "current_org": "瑞金经济技术开发区",
     "source": "百度百科; 瑞金网"},

    # ══前任市长 — 蓝贤林（已任市委书记，重复ID的合并） ══
    # 蓝贤林 is id 1 — both as current secretary AND former mayor

    # ══原瑞金市委书记 — 许锐 ══
    {"id": 23, "name": "许锐", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "（原瑞金市委书记，已调离）", "current_org": "",
     "source": "公开报道"},
]

organizations = [
    {"id": 1, "name": "中共瑞金市委员会", "type": "党委", "level": "县处级", "parent": "中共赣州市委员会", "location": "江西赣州瑞金"},
    {"id": 2, "name": "瑞金市人民政府", "type": "政府", "level": "县处级", "parent": "赣州市人民政府", "location": "江西赣州瑞金"},
    {"id": 3, "name": "瑞金经济技术开发区", "type": "开发区", "level": "国家级经开区", "parent": "瑞金市人民政府", "location": "江西赣州瑞金"},
    {"id": 4, "name": "中共赣州市委员会", "type": "党委", "level": "地厅级", "parent": "中共江西省委员会", "location": "江西赣州"},
    {"id": 5, "name": "赣州市人民政府", "type": "政府", "level": "地厅级", "parent": "江西省人民政府", "location": "江西赣州"},
    {"id": 6, "name": "中共崇义县委员会", "type": "党委", "level": "县处级", "parent": "中共赣州市委员会", "location": "江西赣州崇义"},
    {"id": 7, "name": "中共寻乌县委员会", "type": "党委", "level": "县处级", "parent": "中共赣州市委员会", "location": "江西赣州寻乌"},
    {"id": 8, "name": "中共瑞金市纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共瑞金市委员会", "location": "江西赣州瑞金"},
    {"id": 9, "name": "中共瑞金市委宣传部", "type": "党委", "level": "县处级", "parent": "中共瑞金市委员会", "location": "江西赣州瑞金"},
    {"id": 10, "name": "中共瑞金市委统战部", "type": "党委", "level": "县处级", "parent": "中共瑞金市委员会", "location": "江西赣州瑞金"},
    {"id": 11, "name": "中共瑞金市委组织部", "type": "党委", "level": "县处级", "parent": "中共瑞金市委员会", "location": "江西赣州瑞金"},
    {"id": 12, "name": "中共瑞金市委政法委员会", "type": "党委", "level": "县处级", "parent": "中共瑞金市委员会", "location": "江西赣州瑞金"},
    {"id": 13, "name": "瑞金市人民武装部", "type": "事业单位", "level": "县处级", "parent": "赣州军分区", "location": "江西赣州瑞金"},
    {"id": 14, "name": "瑞金市人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "瑞金市", "location": "江西赣州瑞金"},
    {"id": 15, "name": "中国人民政治协商会议瑞金市委员会", "type": "政协", "level": "县处级", "parent": "瑞金市", "location": "江西赣州瑞金"},
    {"id": 16, "name": "赣州市供销合作社联合社", "type": "事业单位", "level": "地厅级", "parent": "赣州市人民政府", "location": "江西赣州"},
    {"id": 17, "name": "中共石城县委员会", "type": "党委", "level": "县处级", "parent": "中共赣州市委员会", "location": "江西赣州石城"},
]

positions = [
    # 蓝贤林
    {"id": 1, "person_id": 1, "org_id": 1, "title": "瑞金市委书记、瑞金经开区党工委书记", "start": "2026-07", "end": "present", "rank": "县处级正职", "note": "2026年7月从寻乌县委书记调任"},
    {"id": 2, "person_id": 1, "org_id": 7, "title": "寻乌县委书记", "start": "2021-08", "end": "2026-07", "rank": "县处级正职", "note": ""},
    {"id": 3, "person_id": 1, "org_id": 2, "title": "瑞金市人民政府市长", "start": "2021-03", "end": "2021-08", "rank": "县处级正职", "note": "2021年3月当选瑞金市长，8月调任寻乌县委书记"},

    # 彭民生
    {"id": 4, "person_id": 2, "org_id": 2, "title": "瑞金市委副书记、市长候选人", "start": "2026-07", "end": "present", "rank": "县处级正职", "note": ""},
    {"id": 5, "person_id": 2, "org_id": 16, "title": "赣州市供销联社党组书记、理事会主任", "start": "", "end": "2026-07", "rank": "县处级正职", "note": ""},

    # 尹忠
    {"id": 6, "person_id": 3, "org_id": 4, "title": "赣州市委常委", "start": "2024", "end": "present", "rank": "地厅级副职", "note": "2024年5月任前公示拟任设区市委常委"},
    {"id": 7, "person_id": 3, "org_id": 1, "title": "瑞金市委书记", "start": "2021-08", "end": "2026-07", "rank": "县处级正职", "note": ""},
    {"id": 8, "person_id": 3, "org_id": 17, "title": "石城县委书记", "start": "2016", "end": "2021-08", "rank": "县处级正职", "note": ""},
    {"id": 9, "person_id": 3, "org_id": 17, "title": "石城县委副书记、县长", "start": "2013", "end": "2016", "rank": "县处级副职", "note": ""},

    # 刘春林
    {"id": 10, "person_id": 4, "org_id": 6, "title": "崇义县委书记", "start": "2026-07", "end": "present", "rank": "县处级正职", "note": "2026年7月从瑞金市长调任"},
    {"id": 11, "person_id": 4, "org_id": 2, "title": "瑞金市人民政府市长", "start": "2021-08", "end": "2026-07", "rank": "县处级正职", "note": ""},

    # 吴建平
    {"id": 12, "person_id": 5, "org_id": 1, "title": "瑞金市委书记", "start": "", "end": "2021-08", "rank": "县处级正职", "note": ""},

    # 市委班子成员
    {"id": 13, "person_id": 6, "org_id": 1, "title": "瑞金市委副书记", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"id": 14, "person_id": 7, "org_id": 1, "title": "瑞金市委副书记", "start": "", "end": "present", "rank": "县处级副职", "note": "分管群团、旅游"},
    {"id": 15, "person_id": 8, "org_id": 8, "title": "瑞金市委常委、市纪委书记、市监委代理主任", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"id": 16, "person_id": 9, "org_id": 9, "title": "瑞金市委常委、宣传部部长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"id": 17, "person_id": 10, "org_id": 10, "title": "瑞金市委常委、统战部部长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"id": 18, "person_id": 11, "org_id": 11, "title": "瑞金市委常委、组织部部长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"id": 19, "person_id": 12, "org_id": 12, "title": "瑞金市委常委、政法委书记", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"id": 20, "person_id": 13, "org_id": 2, "title": "瑞金市委常委、副市长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"id": 21, "person_id": 14, "org_id": 13, "title": "瑞金市委常委、人武部政委", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"id": 22, "person_id": 15, "org_id": 2, "title": "瑞金市委常委、市政府党组成员、副市长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},

    # 其他副市长
    {"id": 23, "person_id": 16, "org_id": 2, "title": "瑞金市政府副市长、党组成员", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"id": 24, "person_id": 17, "org_id": 2, "title": "瑞金市政府副市长、党组成员", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"id": 25, "person_id": 18, "org_id": 2, "title": "瑞金市政府副市长、党组成员", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"id": 26, "person_id": 19, "org_id": 2, "title": "瑞金市政府副市长、党组成员", "start": "", "end": "present", "rank": "县处级副职", "note": ""},

    # 人大、政协
    {"id": 27, "person_id": 20, "org_id": 14, "title": "瑞金市人大常委会主任", "start": "", "end": "present", "rank": "县处级正职", "note": ""},
    {"id": 28, "person_id": 21, "org_id": 15, "title": "瑞金市政协主席", "start": "", "end": "present", "rank": "县处级正职", "note": ""},

    # 罗林生
    {"id": 29, "person_id": 22, "org_id": 3, "title": "瑞金市委常委、副市长、瑞金经开区党工委副书记", "start": "", "end": "present", "rank": "县处级副职", "note": ""},

    # 许锐
    {"id": 30, "person_id": 23, "org_id": 1, "title": "原瑞金市委书记", "start": "", "end": "", "rank": "县处级正职", "note": "更早的瑞金市委书记"},
]

relationships = [
    # 蓝贤林 ←→ 彭民生 (现在搭档)
    {"id": 1, "person_a_id": 1, "person_b_id": 2, "type": "superior_subordinate",
     "context": "蓝贤林任市委书记，彭民生任市长候选人，党政正职搭档", "overlap_org": "瑞金市委/市政府", "overlap_period": "2026-07至今"},

    # 蓝贤林 ←→ 尹忠 (前后任书记)
    {"id": 2, "person_a_id": 1, "person_b_id": 3, "type": "predecessor_successor",
     "context": "蓝贤林接替尹忠担任瑞金市委书记", "overlap_org": "中共瑞金市委员会", "overlap_period": "2026-07"},

    # 刘春林 ←→ 彭民生 (前后任市长)
    {"id": 3, "person_a_id": 4, "person_b_id": 2, "type": "predecessor_successor",
     "context": "刘春林调任崇义县委书记，彭民生接任市长候选人", "overlap_org": "瑞金市人民政府", "overlap_period": "2026-07"},

    # 尹忠 ←→ 刘春林 (前任搭档)
    {"id": 4, "person_a_id": 3, "person_b_id": 4, "type": "overlap",
     "context": "尹忠任瑞金市委书记期间，刘春林任瑞金市长", "overlap_org": "瑞金市委/市政府", "overlap_period": "2021-08至2024"},

    # 蓝贤林 ←→ 刘春林 (前后任市长)
    {"id": 5, "person_a_id": 1, "person_b_id": 4, "type": "predecessor_successor",
     "context": "蓝贤林2021年3月至8月任瑞金市长，后刘春林接任", "overlap_org": "瑞金市人民政府", "overlap_period": "2021-08"},

    # 尹忠 ←→ 吴建平 (前后任书记)
    {"id": 6, "person_a_id": 3, "person_b_id": 5, "type": "predecessor_successor",
     "context": "尹忠接替吴建平担任瑞金市委书记", "overlap_org": "中共瑞金市委员会", "overlap_period": "2021-08"},

    # 尹忠 ←→ 蓝贤林 (前任搭档时期 — 尹忠任书记、蓝贤林任市长)
    {"id": 7, "person_a_id": 3, "person_b_id": 1, "type": "superior_subordinate",
     "context": "2019-2021年尹忠任瑞金市委书记期间，蓝贤林任瑞金市长", "overlap_org": "瑞金市委/市政府", "overlap_period": "2019-11至2021-08"},

    # 刘春林 → 瑞金市委常委班子
    {"id": 8, "person_a_id": 4, "person_b_id": 6, "type": "overlap",
     "context": "刘春林任市长期间与李志坚同为市委班子成员", "overlap_org": "中共瑞金市委员会", "overlap_period": ""},

    # 黄发亮与刘春林搭档
    {"id": 9, "person_a_id": 13, "person_b_id": 4, "type": "overlap",
     "context": "黄发亮任市委常委、副市长期间与刘春林市长共事", "overlap_org": "瑞金市人民政府", "overlap_period": ""},
]

# ── BUILD FUNCTIONS ─────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Return 'r,g,b' string for person node color by role."""
    name = p["name"]
    current = p["current_post"]
    if "书记" in current and "市委" in current:
        return "255,50,50"
    elif "市长" in current or "市长候选人" in current:
        return "50,100,255"
    elif "纪委" in current:
        return "255,165,0"
    elif "人大" in current:
        return "200,255,255"
    elif "政协" in current:
        return "255,240,200"
    else:
        return "100,100,100"

def org_color(o):
    t = o["type"]
    if t == "党委":
        return "255,200,200"
    elif t == "政府":
        return "200,200,255"
    elif t == "开发区":
        return "200,255,200"
    elif t == "人大":
        return "200,255,255"
    elif t == "政协":
        return "255,240,200"
    elif t == "事业单位":
        return "220,220,220"
    else:
        return "200,200,200"

def is_top_leader(p):
    current = p["current_post"]
    return "市委书记" in current or "市长" in current or "市长候选人" in current

def build_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS relationships")
    cur.execute("DROP TABLE IF EXISTS positions")
    cur.execute("DROP TABLE IF EXISTS organizations")
    cur.execute("DROP TABLE IF EXISTS persons")

    cur.execute("""
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
            name TEXT,
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
        )
    """)

    cur.execute("""
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)

    cur.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY,
            person_a_id INTEGER,
            person_b_id INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a_id) REFERENCES persons(id),
            FOREIGN KEY (person_b_id) REFERENCES persons(id)
        )
    """)

    for p in persons:
        cur.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education,
                                 party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
              p["birthplace"], p["education"], p["party_join"], p["work_start"],
              p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        cur.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        cur.execute("""
            INSERT INTO positions (id, person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
              pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        cur.execute("""
            INSERT INTO relationships (id, person_a_id, person_b_id, type, context,
                                       overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (r["id"], r["person_a_id"], r["person_b_id"], r["type"],
              r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()

    # Stats
    print(f"  Persons: {cur.execute('SELECT COUNT(*) FROM persons').fetchone()[0]}")
    print(f"  Organizations: {cur.execute('SELECT COUNT(*) FROM organizations').fetchone()[0]}")
    print(f"  Positions: {cur.execute('SELECT COUNT(*) FROM positions').fetchone()[0]}")
    print(f"  Relationships: {cur.execute('SELECT COUNT(*) FROM relationships').fetchone()[0]}")

    conn.close()

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Sisyphus Research Agent</creator>')
    lines.append('    <description>瑞金市领导班子工作关系网络 - 2026-07-15</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="birth" type="string"/>')
    lines.append('      <attribute id="2" title="birthplace" type="string"/>')
    lines.append('      <attribute id="3" title="current_post" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="start" type="string"/>')
    lines.append('      <attribute id="2" title="end" type="string"/>')
    lines.append('      <attribute id="3" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["birthplace"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["current_post"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["location"])}"/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # person → organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["start"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos["end"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # person ↔ person (relationship)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a_id"]}" target="p{r["person_b_id"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["overlap_period"])}"/>')
        lines.append(f'          <attvalue for="2" value="present"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"  GEXF edges: {eid}")

# ── MAIN ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    print("Building 瑞金市 network database...")
    build_db()
    print(f"  DB: {DB_PATH}")

    print("Building GEXF graph...")
    build_gexf()
    print(f"  GEXF: {GEXF_PATH}")

    print("\nDone. Summary:")
    print(f"  {len(persons)} persons")
    print(f"  {len(organizations)} organizations")
    print(f"  {len(positions)} positions")
    print(f"  {len(relationships)} relationships")
