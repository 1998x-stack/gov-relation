#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Yingtan Yuehu District leadership network."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/yuehu_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/yuehu_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current & Recent Leaders ──
    {"id": 1, "name": "黄海有", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-09", "birthplace": "江西余江", "education": "在职大专",
     "party_join": "中共党员", "work_start": "1996-08",
     "current_post": "月湖区委书记", "current_org": "中共月湖区委员会",
     "source": "https://wapbaike.baidu.com/item/%E9%BB%84%E6%B5%B7%E6%9C%89"},
    {"id": 2, "name": "曹玉臣", "gender": "女", "ethnicity": "汉族",
     "birth": "1980-11", "birthplace": "江西万年", "education": "在职大学",
     "party_join": "2006-07", "work_start": "2000-07",
     "current_post": "月湖区委副书记、区长", "current_org": "月湖区人民政府",
     "source": "https://wapbaike.baidu.com/item/%E6%9B%B9%E7%8E%89%E8%87%A3"},
    {"id": 3, "name": "敖捷", "gender": "男", "ethnicity": "汉族",
     "birth": "1985-06", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "九江市柴桑区委书记", "current_org": "中共九江市柴桑区委员会",
     "source": "https://wapbaike.baidu.com/item/%E6%95%96%E6%8D%B7"},
    {"id": 4, "name": "方璐", "gender": "女", "ethnicity": "汉族",
     "birth": "1979-06", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "2000-07",
     "current_post": "（去向待查）", "current_org": "",
     "source": "https://www.yuehu.gov.cn"},
    {"id": 5, "name": "胡永生", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-06", "birthplace": "湖北郧西", "education": "中央党校大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "月湖区委副书记", "current_org": "中共月湖区委员会",
     "source": "鹰潭日报2024年4月30日任前公示"},
    {"id": 6, "name": "江俊", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "月湖区委常委、纪委书记、监委主任", "current_org": "中共月湖区纪律检查委员会",
     "source": "月湖区第十届人大第七次会议公告(2025.10)"},
    {"id": 7, "name": "梁锋", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "月湖区委常委、组织部部长", "current_org": "中共月湖区委员会组织部",
     "source": "月湖区政府网站"},
    {"id": 8, "name": "周先才", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-10", "birthplace": "", "education": "大学（江西农业大学林学）",
     "party_join": "中共党员", "work_start": "",
     "current_post": "月湖区委常委、宣传部部长", "current_org": "中共月湖区委员会宣传部",
     "source": "https://baike.baidu.com/item/%E5%91%A8%E5%85%88%E6%89%8D"},
    {"id": 9, "name": "冯发茂", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "月湖区委常委、政法委书记", "current_org": "中共月湖区委员会政法委员会",
     "source": "月湖区政府网站(2023.07起)"},
    {"id": 10, "name": "彭科", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "月湖区委常委、人武部政委", "current_org": "月湖区人民武装部",
     "source": "月湖区政府网站(2026.03)"},
    {"id": 11, "name": "陶君喜", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "月湖区委常委、常务副区长", "current_org": "月湖区人民政府",
     "source": "月湖区政府网站(2025.05起)"},
    {"id": 12, "name": "张利虹", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "月湖区政府党组成员", "current_org": "月湖区人民政府",
     "source": "月湖区政府网站"},
    {"id": 13, "name": "吴后启", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "月湖区副区长", "current_org": "月湖区人民政府",
     "source": "月湖区政府网站"},
    {"id": 14, "name": "钱小飞", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "月湖区副区长、党组成员", "current_org": "月湖区人民政府",
     "source": "月湖区政府网站"},
    {"id": 15, "name": "官正强", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "月湖区副区长、党组成员", "current_org": "月湖区人民政府",
     "source": "月湖区政府网站"},
    {"id": 16, "name": "黄斌", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "月湖区副区长、党组成员", "current_org": "月湖区人民政府",
     "source": "月湖区政府网站"},
    {"id": 17, "name": "吴嘉玮", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "月湖区副区长、党组成员、月湖公安分局局长", "current_org": "月湖公安分局",
     "source": "月湖区政府网站"},
    {"id": 18, "name": "王晓柯", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "月湖区副区长、党组成员", "current_org": "月湖区人民政府",
     "source": "月湖区政府网站"},
    {"id": 19, "name": "张朝洋", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "月湖区副区长、党组成员", "current_org": "月湖区人民政府",
     "source": "月湖区政府网站"},
    {"id": 20, "name": "张强", "gender": "男", "ethnicity": "汉族",
     "birth": "1979-09", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "（月湖区原纪委书记，2025年调离）", "current_org": "",
     "source": "鹰潭市纪委网站"},
    # ── Cross-city corridor figures ──
    {"id": 21, "name": "钟志生", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "（原景德镇市委书记，被查）", "current_org": "",
     "source": "https://zh.wikipedia.org/wiki/%E9%92%9F%E5%BF%97%E7%94%9F"},
    {"id": 22, "name": "鄢华", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "景德镇市人大常委会主任", "current_org": "景德镇市人大常委会",
     "source": "景德镇市调研报告"},
    {"id": 23, "name": "郭安", "gender": "男", "ethnicity": "汉族",
     "birth": "1962", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "（原鹰潭市委书记，被查）", "current_org": "",
     "source": "https://zh.wikipedia.org/wiki/%E9%83%AD%E5%AE%89_(1962%E5%B9%B4)"},
    {"id": 24, "name": "乐文红", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "南昌市委常委、统战部部长", "current_org": "中共南昌市委统战部",
     "source": "进贤县调研数据"},
    {"id": 25, "name": "李志兵", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "（月湖区原区委书记，~2021离任）", "current_org": "",
     "source": "月湖区政府网站"},
]

organizations = [
    {"id": 1, "name": "中共月湖区委员会", "type": "党委", "level": "县级", "parent": "中共鹰潭市委", "location": "鹰潭市月湖区"},
    {"id": 2, "name": "月湖区人民政府", "type": "政府", "level": "县级", "parent": "鹰潭市人民政府", "location": "鹰潭市月湖区"},
    {"id": 3, "name": "中共月湖区纪律检查委员会", "type": "纪委", "level": "县级", "parent": "中共鹰潭市纪委", "location": "鹰潭市月湖区"},
    {"id": 4, "name": "中共月湖区委组织部", "type": "党委", "level": "县级", "parent": "中共月湖区委员会", "location": "鹰潭市月湖区"},
    {"id": 5, "name": "中共月湖区委宣传部", "type": "党委", "level": "县级", "parent": "中共月湖区委员会", "location": "鹰潭市月湖区"},
    {"id": 6, "name": "中共月湖区委政法委员会", "type": "党委", "level": "县级", "parent": "中共月湖区委员会", "location": "鹰潭市月湖区"},
    {"id": 7, "name": "月湖区人民武装部", "type": "军队", "level": "正团级", "parent": "鹰潭军分区", "location": "鹰潭市月湖区"},
    {"id": 8, "name": "鹰潭市发展和改革委员会", "type": "政府", "level": "正处级", "parent": "鹰潭市人民政府", "location": "鹰潭市"},
    {"id": 9, "name": "鹰潭市生态环境局", "type": "政府", "level": "正处级", "parent": "鹰潭市人民政府", "location": "鹰潭市"},
    {"id": 10, "name": "鹰潭市人民政府办公室", "type": "政府", "level": "正处级", "parent": "鹰潭市人民政府", "location": "鹰潭市"},
    {"id": 11, "name": "鹰潭市工业和信息化局", "type": "政府", "level": "正处级", "parent": "鹰潭市人民政府", "location": "鹰潭市"},
    {"id": 12, "name": "鹰潭市铜产业发展中心", "type": "事业单位", "level": "正处级", "parent": "鹰潭市工信局", "location": "鹰潭市"},
    {"id": 13, "name": "共青团鹰潭市委", "type": "群团", "level": "正处级", "parent": "中共鹰潭市委", "location": "鹰潭市"},
    {"id": 14, "name": "贵溪市", "type": "政府", "level": "县级市", "parent": "鹰潭市", "location": "鹰潭市贵溪市"},
    {"id": 15, "name": "余江区", "type": "政府", "level": "县级", "parent": "鹰潭市", "location": "鹰潭市余江区"},
    {"id": 16, "name": "月湖公安分局", "type": "政府", "level": "正科级", "parent": "鹰潭市公安局", "location": "鹰潭市月湖区"},
]

positions = [
    # 黄海有
    {"person_id": 1, "org_id": 15, "title": "余江县黄庄乡乡长助理、副乡长、常务副乡长、纪委书记", "start": "1996", "end": "", "rank": "副科-正科", "note": "余江基层20+年"},
    {"person_id": 1, "org_id": 15, "title": "余江县春涛乡乡长、党委书记、春涛镇党委书记", "start": "", "end": "", "rank": "正科", "note": ""},
    {"person_id": 1, "org_id": 2, "title": "月湖区副区长", "start": "", "end": "", "rank": "副处", "note": ""},
    {"person_id": 1, "org_id": 10, "title": "鹰潭市政府副秘书长", "start": "", "end": "2024", "rank": "正处", "note": ""},
    {"person_id": 1, "org_id": 9, "title": "鹰潭市生态环境局党组书记、局长", "start": "", "end": "2024-05", "rank": "正处", "note": ""},
    {"person_id": 1, "org_id": 8, "title": "鹰潭市发改委党组书记、主任（兼市数据局局长）", "start": "2024-04", "end": "2026-06", "rank": "正处", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "月湖区委书记、区人武部党委第一书记", "start": "2026-07", "end": "", "rank": "副厅", "note": ""},
    # 曹玉臣
    {"person_id": 2, "org_id": 11, "title": "鹰潭市经贸委投资与技术科副科长", "start": "", "end": "", "rank": "副科", "note": ""},
    {"person_id": 2, "org_id": 11, "title": "鹰潭市工信局科技与投资科科长", "start": "", "end": "", "rank": "正科", "note": ""},
    {"person_id": 2, "org_id": 11, "title": "鹰潭市工信局党委委员、市铜产业发展局专职副局长", "start": "2019", "end": "2021", "rank": "副处", "note": ""},
    {"person_id": 2, "org_id": 12, "title": "鹰潭市铜产业发展中心主任（市铜产业发展局局长）", "start": "2021", "end": "2022-03", "rank": "正处", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "月湖区副区长", "start": "2022-03", "end": "2024", "rank": "副处", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "月湖区委常委、常务副区长", "start": "2024", "end": "2025-09", "rank": "副处", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "月湖区委副书记、代区长→区长", "start": "2025-09", "end": "", "rank": "正处", "note": ""},
    # 敖捷
    {"person_id": 3, "org_id": 2, "title": "月湖区正科级干部→区委委员/常委", "start": "", "end": "", "rank": "正科", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "信江新区党工委副书记、管委会主任", "start": "", "end": "", "rank": "副厅", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "月湖区委书记", "start": "2021-09", "end": "2026-06", "rank": "副厅", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "九江市柴桑区委书记", "start": "2026-07", "end": "", "rank": "副厅", "note": "跨市平调"},
    # 方璐
    {"person_id": 4, "org_id": 13, "title": "共青团鹰潭市委干部", "start": "2000-07", "end": "2004-03", "rank": "", "note": "期间在白露镇、高公寨乡挂职"},
    {"person_id": 4, "org_id": 14, "title": "贵溪市（历任副市长等职）", "start": "2004-03", "end": "2020", "rank": "副处", "note": "具体职务阶梯待查"},
    {"person_id": 4, "org_id": 14, "title": "贵溪市委副书记（正县级）", "start": "2020", "end": "2021-01", "rank": "正处", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "月湖区委副书记、区长", "start": "2021-01", "end": "2025-08", "rank": "正处", "note": ""},
    # 胡永生
    {"person_id": 5, "org_id": 14, "title": "贵溪市委常委、宣传部部长", "start": "", "end": "2024-04", "rank": "副处", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "月湖区委副书记", "start": "2024-04", "end": "", "rank": "副处", "note": "2024年4月任前公示"},
    # 江俊
    {"person_id": 6, "org_id": 3, "title": "月湖区委常委、纪委书记、监委主任", "start": "2025-10", "end": "", "rank": "副处", "note": "接替张强"},
    # 张强
    {"person_id": 20, "org_id": 3, "title": "月湖区委常委、纪委书记、监委主任", "start": "2021-08", "end": "2025", "rank": "副处", "note": ""},
    # 梁锋
    {"person_id": 7, "org_id": 4, "title": "月湖区委常委、组织部部长", "start": "2023", "end": "", "rank": "副处", "note": ""},
    # 周先才
    {"person_id": 8, "org_id": 5, "title": "月湖区委常委、宣传部部长", "start": "2022-05", "end": "", "rank": "副处", "note": ""},
    # 冯发茂
    {"person_id": 9, "org_id": 6, "title": "月湖区委常委、政法委书记", "start": "2023-07", "end": "", "rank": "副处", "note": ""},
    # 彭科
    {"person_id": 10, "org_id": 7, "title": "月湖区委常委、人武部政委", "start": "", "end": "", "rank": "正团", "note": ""},
    # 陶君喜
    {"person_id": 11, "org_id": 2, "title": "月湖区委常委、常务副区长", "start": "2025-05", "end": "", "rank": "副处", "note": "接替升任区长的曹玉臣"},
    # Other deputies
    {"person_id": 12, "org_id": 2, "title": "月湖区政府党组成员", "start": "", "end": "", "rank": "副处", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "月湖区副区长", "start": "", "end": "", "rank": "副处", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "月湖区副区长、党组成员", "start": "", "end": "", "rank": "副处", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "月湖区副区长、党组成员", "start": "", "end": "", "rank": "副处", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "月湖区副区长、党组成员", "start": "", "end": "", "rank": "副处", "note": ""},
    {"person_id": 17, "org_id": 16, "title": "月湖区副区长、党组成员、月湖公安分局局长", "start": "", "end": "", "rank": "副处", "note": ""},
    {"person_id": 18, "org_id": 2, "title": "月湖区副区长、党组成员", "start": "", "end": "", "rank": "副处", "note": ""},
    {"person_id": 19, "org_id": 2, "title": "月湖区副区长、党组成员", "start": "", "end": "", "rank": "副处", "note": ""},
    # Cross-city corridor
    {"person_id": 21, "org_id": 2, "title": "鹰潭市长→景德镇市委书记", "start": "2008", "end": "2021", "rank": "正厅", "note": "鹰潭-景德镇走廊"},
    {"person_id": 22, "org_id": 2, "title": "鹰潭市纪委书记→景德镇市人大常委会主任", "start": "", "end": "2026", "rank": "正厅", "note": "鹰潭-景德镇走廊"},
    {"person_id": 23, "org_id": 2, "title": "南昌市长→鹰潭市委书记（被查）", "start": "2018", "end": "2021", "rank": "正厅", "note": "南昌-鹰潭走廊"},
    {"person_id": 24, "org_id": 2, "title": "月湖区委副书记、区长→月湖区委书记", "start": "2009", "end": "2013", "rank": "正处", "note": "较早时期的月湖区长"},
    {"person_id": 25, "org_id": 1, "title": "月湖区委书记", "start": "", "end": "2021-09", "rank": "副厅", "note": "敖捷的前任"},
]

relationships = [
    # 党政一把手搭档
    {"person_a": 1, "person_b": 2, "type": "strong", "context": "区委书记-区长搭档（2026.07起）", "overlap_org": "月湖区", "overlap_period": "2026.07-至今"},
    {"person_a": 3, "person_b": 4, "type": "strong", "context": "区委书记-区长搭档（2021-2025）", "overlap_org": "月湖区", "overlap_period": "2021-2025"},
    {"person_a": 1, "person_b": 3, "type": "weak", "context": "前后任区委书记", "overlap_org": "月湖区", "overlap_period": "2026.07"},
    # 区长交接
    {"person_a": 2, "person_b": 4, "type": "weak", "context": "前后任区长（曹玉臣接替方璐）", "overlap_org": "月湖区", "overlap_period": "2025.09"},
    # 曹玉臣与前任搭档黄海有（曾同任副区长）
    {"person_a": 1, "person_b": 2, "type": "weak", "context": "黄海有曾任月湖副区长，曹玉臣后任月湖副区长", "overlap_org": "月湖区", "overlap_period": "不同期"},
    # 胡永生与敖捷/方璐搭档
    {"person_a": 5, "person_b": 3, "type": "weak", "context": "区委副书记与区委书记搭档", "overlap_org": "月湖区", "overlap_period": "2024-2026"},
    {"person_a": 5, "person_b": 4, "type": "weak", "context": "区委副书记与区长搭档", "overlap_org": "月湖区", "overlap_period": "2024-2025"},
    # 贵溪系连接
    {"person_a": 5, "person_b": 4, "type": "weak", "context": "方璐曾任贵溪市委副书记，胡永生曾任贵溪市委常委", "overlap_org": "贵溪市", "overlap_period": "可能同期"},
    # 梁锋贵溪连接(需核实)
    {"person_a": 7, "person_b": 4, "type": "weak", "context": "方璐贵溪市委副书记，梁锋可能曾任贵溪副市长", "overlap_org": "贵溪市（待核实）", "overlap_period": ""},
    # 江俊接替张强
    {"person_a": 6, "person_b": 20, "type": "weak", "context": "前后任纪委书记", "overlap_org": "月湖区纪委", "overlap_period": "2025.10"},
    # 鹰潭-景德镇走廊
    {"person_a": 21, "person_b": 22, "type": "weak", "context": "同属鹰潭-景德镇走廊", "overlap_org": "鹰潭市", "overlap_period": ""},
    # 乐文红(较早月湖区长)连接
    {"person_a": 24, "person_b": 25, "type": "weak", "context": "乐文红任月湖区长时间在李志兵任书记前", "overlap_org": "月湖区", "overlap_period": ""},
]

# ── BUILD SQLite ──────────────────────────────────────────────────────

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS persons (
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

CREATE TABLE IF NOT EXISTS organizations (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT,
    level TEXT,
    parent TEXT,
    location TEXT
);

CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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

CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a INTEGER NOT NULL,
    person_b INTEGER NOT NULL,
    type TEXT NOT NULL,
    context TEXT,
    overlap_org TEXT,
    overlap_period TEXT,
    FOREIGN KEY (person_a) REFERENCES persons(id),
    FOREIGN KEY (person_b) REFERENCES persons(id)
);
""")

# Insert persons
for p in persons:
    cur.execute("""
        INSERT OR REPLACE INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p["birthplace"], p["education"],
          p["party_join"], p["work_start"], p["current_post"], p["current_org"], p["source"]))

for o in organizations:
    cur.execute("""
        INSERT OR REPLACE INTO organizations (id, name, type, level, parent, location)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for pos in positions:
    cur.execute("""
        INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos["rank"], pos["note"]))

for r in relationships:
    cur.execute("""
        INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"]))

conn.commit()
conn.close()
print(f"✅ SQLite database written: {DB_PATH}")

# ── BUILD GEXF ────────────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    name = p["name"]
    # Red for party secretary
    if name in ("黄海有", "敖捷", "李志兵", "乐文红"):
        return "255,50,50"
    # Blue for government leaders
    if name in ("曹玉臣", "方璐", "陶君喜"):
        return "50,100,255"
    # Orange for discipline
    if name in ("江俊", "张强"):
        return "255,165,0"
    # Others grey
    return "100,100,100"

def is_top_leader(p):
    return p["name"] in ("黄海有", "曹玉臣", "敖捷", "方璐")

def org_color(o):
    t = o["type"]
    if t == "党委": return "255,200,200"
    if t == "政府": return "200,200,255"
    if t == "纪委": return "255,220,180"
    if t == "军队": return "200,255,200"
    if t == "事业单位": return "220,220,220"
    if t == "群团": return "255,220,255"
    return "200,200,200"

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>China Gov Network Research Agent</creator>')
lines.append('    <description>鹰潭市月湖区领导班子工作关系网络</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Node attributes
lines.append('    <attributes class="node">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="role" type="string"/>')
lines.append('      <attribute id="2" title="organization" type="string"/>')
lines.append('    </attributes>')

# Edge attributes
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="context" type="string"/>')
lines.append('      <attribute id="2" title="period" type="string"/>')
lines.append('    </attributes>')

# Person nodes
lines.append('    <nodes>')
for p in persons:
    c = person_color(p)
    sz = "20.0" if is_top_leader(p) else "12.0"
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="person"/>')
    lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append(f'        <viz:position x="0.0" y="0.0" z="0.0"/>')
    lines.append('      </node>')

# Organization nodes
for o in organizations:
    c = org_color(o)
    lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="organization"/>')
    lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(o["location"])}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append('      </node>')

lines.append('    </nodes>')

# Edges
lines.append('    <edges>')
eid = 0

# Person→Organization (worked_at)
for pos in positions:
    eid += 1
    lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="worked_at"/>')
    lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(pos["start"])}-{esc(pos["end"])}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

# Person↔Person (relationship)
for r in relationships:
    eid += 1
    w = "2.0" if r["type"] == "strong" else "1.0"
    lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="{w}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="relationship"/>')
    lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(r["overlap_period"])}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print(f"✅ GEXF graph written: {GEXF_PATH}")

# ── STATS ─────────────────────────────────────────────────────────────

print(f"\n📊 数据统计:")
print(f"  人物: {len(persons)} 人")
print(f"  机构: {len(organizations)} 个")
print(f"  任职记录: {len(positions)} 条")
print(f"  关系: {len(relationships)} 条")
