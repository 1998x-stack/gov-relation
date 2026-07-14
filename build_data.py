#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Jinxian County leadership network."""

import sqlite3
import os
from datetime import datetime
from xml.etree import ElementTree as ET
from xml.dom import minidom

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/jinxian_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/jinxian_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    {"id": 1, "name": "熊振强", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-03", "birthplace": "江西奉新", "education": "大学",
     "party_join": "1992-12", "work_start": "1991-09",
     "current_post": "中共进贤县委书记", "current_org": "中共进贤县委员会",
     "source": "https://baike.baidu.com/item/%E7%86%8A%E6%8C%AF%E5%BC%BA/7691320"},
    {"id": 2, "name": "雷桥亮", "gender": "男", "ethnicity": "汉族",
     "birth": "1980-11", "birthplace": "", "education": "研究生，经济学硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "进贤县委副书记、副县长、代理县长", "current_org": "进贤县人民政府",
     "source": "https://baike.baidu.com/item/%E9%9B%B7%E6%A1%A5%E4%BA%AE/61369190"},
    {"id": 3, "name": "徐强", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-11", "birthplace": "江西南昌县", "education": "MPA硕士",
     "party_join": "1996-06", "work_start": "1996-09",
     "current_post": "南昌市新建区委书记", "current_org": "中共南昌市新建区委员会",
     "source": "https://baike.baidu.com/item/%E5%BE%90%E5%BC%BA/50081202"},
    {"id": 4, "name": "钱太高", "gender": "男", "ethnicity": "汉族",
     "birth": "1977-04", "birthplace": "江西新建", "education": "在职研究生，工商管理硕士",
     "party_join": "1998-12", "work_start": "1999-09",
     "current_post": "进贤县委常委、常务副县长", "current_org": "进贤县人民政府",
     "source": "https://baike.baidu.com/item/%E9%92%B1%E5%A4%AA%E9%AB%98/22046978"},
    {"id": 5, "name": "聂红兵", "gender": "男", "ethnicity": "汉族",
     "birth": "1980-11", "birthplace": "江西南昌县", "education": "省委党校在职研究生",
     "party_join": "1999-05", "work_start": "1999-08",
     "current_post": "进贤县委常委、副县长，进贤产业园党工委书记", "current_org": "进贤县人民政府",
     "source": "https://baike.baidu.com/item/%E8%81%82%E7%BA%A2%E5%85%B5/64020468"},
    {"id": 6, "name": "叶飞", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-03", "birthplace": "江西进贤", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "1996-09",
     "current_post": "进贤县委副书记", "current_org": "中共进贤县委员会",
     "source": "https://jxx.nc.gov.cn/jxxrmzf/xwld/ldzc.shtml"},
    {"id": 7, "name": "徐永钢", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-04", "birthplace": "江西丰城", "education": "本科，经济学学士",
     "party_join": "中共党员", "work_start": "2004-04",
     "current_post": "进贤县委常委、组织部部长", "current_org": "中共进贤县委员会",
     "source": "https://baike.baidu.com/item/%E5%BE%90%E6%B0%B8%E9%92%A2/55600127"},
    {"id": 8, "name": "曾晋", "gender": "男", "ethnicity": "汉族",
     "birth": "1984-01", "birthplace": "", "education": "省委党校研究生，工学学士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "进贤县委常委、统战部部长", "current_org": "中共进贤县委员会",
     "source": "https://baike.baidu.com/item/%E6%9B%BE%E6%99%8B/19715734"},
    {"id": 9, "name": "张乐洋", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "进贤县委常委、纪委书记、监委代主任", "current_org": "中共进贤县委员会",
     "source": "https://jxx.nc.gov.cn/jxxrmzf/xwld/ldzc.shtml"},
    {"id": 10, "name": "舒丹", "gender": "女", "ethnicity": "汉族",
     "birth": "1982-01", "birthplace": "江西南昌", "education": "本科，法学学士",
     "party_join": "无党派", "work_start": "2003",
     "current_post": "进贤县副县长", "current_org": "进贤县人民政府",
     "source": "https://www.thepaper.cn/newsDetail_forward_10884789"},
    {"id": 11, "name": "熊军", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-05", "birthplace": "江西南昌县", "education": "省委党校研究生（MPA）",
     "party_join": "中共党员", "work_start": "1996-12",
     "current_post": "进贤县副县长", "current_org": "进贤县人民政府",
     "source": "https://baike.baidu.com/item/%E7%86%8A%E5%86%9B/58350224"},
    {"id": 12, "name": "熊伊晖", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-11", "birthplace": "", "education": "大学本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "进贤县副县长", "current_org": "进贤县人民政府",
     "source": "https://baike.baidu.com/item/%E7%86%8A%E4%BC%8A%E6%99%96/58349859"},
    {"id": 13, "name": "陶仲新", "gender": "男", "ethnicity": "汉族",
     "birth": "1978-02", "birthplace": "", "education": "中央党校大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "进贤县副县长", "current_org": "进贤县人民政府",
     "source": "https://jx.ifeng.com/c/8k7zKqGQFas"},
    {"id": 14, "name": "何勇", "gender": "男", "ethnicity": "汉族",
     "birth": "1973-06", "birthplace": "", "education": "在职大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "进贤县副县长、公安局局长", "current_org": "进贤县人民政府",
     "source": "https://baike.baidu.com/item/%E4%BD%95%E5%8B%87/64683574"},
    {"id": 15, "name": "谭伯乐", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-02", "birthplace": "江西进贤", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "南昌市政协副主席（曾任安义县委书记）", "current_org": "南昌市政协",
     "source": "https://baike.baidu.com/item/%E8%B0%AD%E4%BC%AF%E4%B9%90/275834"},
    {"id": 16, "name": "涂莉花", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "新建区人大常委会主任（原进贤县委常委/统战部长）", "current_org": "新建区人大常委会",
     "source": "https://www.jxxinjian.jcy.gov.cn/xjzc/202412/t20241220_6769537.shtml"},
    {"id": 17, "name": "邓之武", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "东湖区委副书记/区长提名人选（原进贤县委常委/常务副县长）", "current_org": "中共南昌市东湖区委员会",
     "source": "https://www.jxxinjian.jcy.gov.cn/xjzc/202412/t20241220_6769537.shtml"},
    {"id": 18, "name": "熊辉", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "安义县委书记（原进贤县县长）", "current_org": "中共安义县委员会",
     "source": "https://bkso.baidu.com/item/%E7%86%8A%E8%BE%89/18041563"},
    {"id": 19, "name": "杨武", "gender": "男", "ethnicity": "汉族",
     "birth": "1984", "birthplace": "江西进贤", "education": "博士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "安义县副县长（原进贤县白圩乡党委书记）", "current_org": "安义县人民政府",
     "source": "https://baike.baidu.com/item/%E6%9D%A8%E6%AD%A6/64486336"},
]

organizations = [
    {"id": 1, "name": "中共进贤县委员会", "type": "党委", "level": "县级",
     "parent": "中共南昌市委员会", "location": "江西省南昌市进贤县"},
    {"id": 2, "name": "进贤县人民政府", "type": "政府", "level": "县级",
     "parent": "南昌市人民政府", "location": "江西省南昌市进贤县"},
    {"id": 3, "name": "中共安义县委员会", "type": "党委", "level": "县级",
     "parent": "中共南昌市委员会", "location": "江西省南昌市安义县"},
    {"id": 4, "name": "安义县人民政府", "type": "政府", "level": "县级",
     "parent": "南昌市人民政府", "location": "江西省南昌市安义县"},
    {"id": 5, "name": "中共南昌市西湖区委员会", "type": "党委", "level": "区级",
     "parent": "中共南昌市委员会", "location": "江西省南昌市西湖区"},
    {"id": 6, "name": "南昌市交通运输局", "type": "政府", "level": "市级",
     "parent": "南昌市人民政府", "location": "江西省南昌市"},
    {"id": 7, "name": "南昌市公路事业发展中心", "type": "事业单位", "level": "市级",
     "parent": "南昌市人民政府", "location": "江西省南昌市"},
    {"id": 8, "name": "南昌市发展和改革委员会", "type": "政府", "level": "市级",
     "parent": "南昌市人民政府", "location": "江西省南昌市"},
    {"id": 9, "name": "南昌高新技术产业开发区", "type": "开发区", "level": "国家级",
     "parent": "南昌市人民政府", "location": "江西省南昌市"},
    {"id": 10, "name": "中共南昌市新建区委员会", "type": "党委", "level": "区级",
     "parent": "中共南昌市委员会", "location": "江西省南昌市新建区"},
    {"id": 11, "name": "南昌市市场监督管理局", "type": "政府", "level": "市级",
     "parent": "南昌市人民政府", "location": "江西省南昌市"},
    {"id": 12, "name": "南昌市食品药品监督管理局", "type": "政府", "level": "市级",
     "parent": "南昌市人民政府", "location": "江西省南昌市"},
    {"id": 13, "name": "南昌小蓝经济技术开发区", "type": "开发区", "level": "国家级",
     "parent": "南昌市人民政府", "location": "江西省南昌市南昌县"},
    {"id": 14, "name": "中共南昌市青云谱区委员会", "type": "党委", "level": "区级",
     "parent": "中共南昌市委员会", "location": "江西省南昌市青云谱区"},
    {"id": 15, "name": "中共南昌市青山湖区委员会", "type": "党委", "level": "区级",
     "parent": "中共南昌市委员会", "location": "江西省南昌市青山湖区"},
    {"id": 16, "name": "南昌市城乡建设局", "type": "政府", "level": "市级",
     "parent": "南昌市人民政府", "location": "江西省南昌市"},
    {"id": 17, "name": "南昌市红谷滩新区", "type": "新区", "level": "区级",
     "parent": "南昌市人民政府", "location": "江西省南昌市红谷滩区"},
    {"id": 18, "name": "安义县工业园区", "type": "开发区", "level": "县级",
     "parent": "安义县人民政府", "location": "江西省南昌市安义县"},
    {"id": 19, "name": "安义县万埠镇", "type": "乡镇", "level": "乡镇级",
     "parent": "安义县人民政府", "location": "江西省南昌市安义县"},
    {"id": 20, "name": "安义县长均乡", "type": "乡镇", "level": "乡镇级",
     "parent": "安义县人民政府", "location": "江西省南昌市安义县"},
    {"id": 21, "name": "安义县鼎湖镇", "type": "乡镇", "level": "乡镇级",
     "parent": "安义县人民政府", "location": "江西省南昌市安义县"},
    {"id": 22, "name": "共青团安义县委员会", "type": "群团", "level": "县级",
     "parent": "共青团南昌市委员会", "location": "江西省南昌市安义县"},
    {"id": 23, "name": "安义县招商局", "type": "政府", "level": "县级",
     "parent": "安义县人民政府", "location": "江西省南昌市安义县"},
    {"id": 24, "name": "新建县松湖镇", "type": "乡镇", "level": "乡镇级",
     "parent": "新建区人民政府", "location": "江西省南昌市新建区"},
    {"id": 25, "name": "南昌市药品监督管理局", "type": "政府", "level": "市级",
     "parent": "南昌市人民政府", "location": "江西省南昌市"},
    {"id": 26, "name": "南昌市青云谱区三店小学", "type": "事业单位", "level": "区级",
     "parent": "青云谱区教育体育局", "location": "江西省南昌市青云谱区"},
    {"id": 27, "name": "南昌市青云谱区外经贸委", "type": "政府", "level": "区级",
     "parent": "青云谱区人民政府", "location": "江西省南昌市青云谱区"},
    {"id": 28, "name": "南昌市青云谱区委办公室", "type": "党委", "level": "区级",
     "parent": "中共南昌市青云谱区委员会", "location": "江西省南昌市青云谱区"},
    {"id": 29, "name": "南昌市青云谱区重点项目办", "type": "政府", "level": "区级",
     "parent": "青云谱区人民政府", "location": "江西省南昌市青云谱区"},
    {"id": 30, "name": "南昌市青云谱区投资促进局", "type": "政府", "level": "区级",
     "parent": "青云谱区人民政府", "location": "江西省南昌市青云谱区"},
    {"id": 31, "name": "南昌小蓝经开区招商中心", "type": "事业单位", "level": "区级",
     "parent": "南昌小蓝经济技术开发区", "location": "江西省南昌市南昌县"},
    {"id": 32, "name": "南昌小蓝经开区招商局", "type": "政府", "level": "区级",
     "parent": "南昌小蓝经济技术开发区", "location": "江西省南昌市南昌县"},
    {"id": 33, "name": "进贤产业园（医科园）", "type": "开发区", "level": "县级",
     "parent": "进贤县人民政府", "location": "江西省南昌市进贤县"},
    {"id": 34, "name": "南昌市青山湖区人大常委会", "type": "人大", "level": "区级",
     "parent": "南昌市人大常委会", "location": "江西省南昌市青山湖区"},
    {"id": 35, "name": "南昌市青山湖区政府办公室", "type": "政府", "level": "区级",
     "parent": "青山湖区人民政府", "location": "江西省南昌市青山湖区"},
    {"id": 36, "name": "南昌市青山湖区扬子洲镇", "type": "乡镇", "level": "乡镇级",
     "parent": "青山湖区人民政府", "location": "江西省南昌市青山湖区"},
    {"id": 37, "name": "南昌市青山湖区南钢街道", "type": "街道", "level": "乡镇级",
     "parent": "青山湖区人民政府", "location": "江西省南昌市青山湖区"},
    {"id": 38, "name": "南昌县武阳镇", "type": "乡镇", "level": "乡镇级",
     "parent": "南昌县人民政府", "location": "江西省南昌市南昌县"},
    {"id": 39, "name": "南昌县委办公室", "type": "党委", "level": "县级",
     "parent": "中共南昌县委员会", "location": "江西省南昌市南昌县"},
    {"id": 40, "name": "南昌县黄马乡", "type": "乡镇", "level": "乡镇级",
     "parent": "南昌县人民政府", "location": "江西省南昌市南昌县"},
    {"id": 41, "name": "南昌县医疗保障局", "type": "政府", "level": "县级",
     "parent": "南昌县人民政府", "location": "江西省南昌市南昌县"},
    {"id": 42, "name": "南昌县莲塘镇", "type": "乡镇", "level": "乡镇级",
     "parent": "南昌县人民政府", "location": "江西省南昌市南昌县"},
    {"id": 43, "name": "南昌县社会科学界联合会", "type": "群团", "level": "县级",
     "parent": "南昌县委员会", "location": "江西省南昌市南昌县"},
    {"id": 44, "name": "南昌县委宣传部", "type": "党委", "level": "县级",
     "parent": "中共南昌县委员会", "location": "江西省南昌市南昌县"},
    {"id": 45, "name": "进贤县李渡镇", "type": "乡镇", "level": "乡镇级",
     "parent": "进贤县人民政府", "location": "江西省南昌市进贤县"},
    {"id": 46, "name": "南昌市公安局水上分局", "type": "政府", "level": "市级",
     "parent": "南昌市公安局", "location": "江西省南昌市"},
    {"id": 47, "name": "南昌市政协", "type": "政协", "level": "市级",
     "parent": "", "location": "江西省南昌市"},
    {"id": 48, "name": "南昌市进贤县白圩乡", "type": "乡镇", "level": "乡镇级",
     "parent": "进贤县人民政府", "location": "江西省南昌市进贤县"},
    {"id": 49, "name": "共青团南昌市委员会", "type": "群团", "level": "市级",
     "parent": "", "location": "江西省南昌市"},
    {"id": 50, "name": "中共南昌市东湖区委员会", "type": "党委", "level": "区级",
     "parent": "中共南昌市委员会", "location": "江西省南昌市东湖区"},
]

positions = [
    # ── 熊振强 (1) ──
    {"id": 1, "person_id": 1, "org_id": 3, "title": "安义县委办公室秘书",
     "start": "1991-09", "end": "1998-07", "rank": "科员", "note": "其间借调南昌市委办公厅"},
    {"id": 2, "person_id": 1, "org_id": 19, "title": "万埠镇纪委书记、党委副书记",
     "start": "1998-08", "end": "2002-08", "rank": "副科级", "note": ""},
    {"id": 3, "person_id": 1, "org_id": 22, "title": "共青团安义县委书记",
     "start": "2002-09", "end": "2004-01", "rank": "正科级", "note": ""},
    {"id": 4, "person_id": 1, "org_id": 23, "title": "安义县招商局局长、党组书记",
     "start": "2004-02", "end": "2005-09", "rank": "正科级", "note": ""},
    {"id": 5, "person_id": 1, "org_id": 20, "title": "长均乡党委副书记、乡长",
     "start": "2005-10", "end": "2010-04", "rank": "正科级", "note": ""},
    {"id": 6, "person_id": 1, "org_id": 20, "title": "长均乡党委书记",
     "start": "2010-05", "end": "2013-01", "rank": "正科级", "note": ""},
    {"id": 7, "person_id": 1, "org_id": 21, "title": "鼎湖镇党委书记",
     "start": "2013-02", "end": "2016-06", "rank": "正科级",
     "note": "2015.12被评为'龚全珍式好干部'——江西省优秀乡镇党委书记"},
    {"id": 8, "person_id": 1, "org_id": 18, "title": "安义县委常委、工业园区党工委书记",
     "start": "2016-07", "end": "2019-06", "rank": "副处级", "note": ""},
    {"id": 9, "person_id": 1, "org_id": 3, "title": "安义县委常委、政法委书记",
     "start": "2019-07", "end": "2021-09", "rank": "副处级", "note": ""},
    {"id": 10, "person_id": 1, "org_id": 5, "title": "南昌市西湖区委副书记",
     "start": "2021-09", "end": "2024-12", "rank": "副处级", "note": "2021.01已以副书记身份开展工作"},
    {"id": 11, "person_id": 1, "org_id": 7, "title": "南昌市公路事业发展中心党组书记、主任",
     "start": "2024-12", "end": "2025-12", "rank": "正处级", "note": "洪府字〔2024〕120号任命"},
    {"id": 12, "person_id": 1, "org_id": 6, "title": "南昌市交通运输局党组书记、局长",
     "start": "2025-12", "end": "2026-06", "rank": "正处级",
     "note": "2025.12.26 南昌市第十六届人大常委会第三十七次会议任命；兼市公路中心党组书记、主任"},
    {"id": 13, "person_id": 1, "org_id": 1, "title": "进贤县委书记",
     "start": "2026-06", "end": "", "rank": "正处级",
     "note": "约2026年6月/7月接替徐强；主持县委全面工作"},

    # ── 雷桥亮 (2) ──
    {"id": 14, "person_id": 2, "org_id": 9, "title": "南昌高新区党工委委员、管委会副主任",
     "start": "2022-05", "end": "2022-12", "rank": "副处级", "note": ""},
    {"id": 15, "person_id": 2, "org_id": 8, "title": "南昌市发改委党组书记、主任",
     "start": "2022-12", "end": "2026-06", "rank": "正处级", "note": ""},
    {"id": 16, "person_id": 2, "org_id": 1, "title": "进贤县委副书记",
     "start": "2026-06", "end": "", "rank": "正处级", "note": ""},
    {"id": 17, "person_id": 2, "org_id": 2, "title": "进贤县副县长、代理县长（县长提名人选）",
     "start": "2026-07-07", "end": "", "rank": "正处级",
     "note": "2026.07.07 进贤县人大常委会任命为副县长、代理县长"},

    # ── 徐强 (3) ──
    {"id": 18, "person_id": 3, "org_id": 17, "title": "红谷滩新区多个职务（街道办主任/书记、城管环保局局长、工委委员、管委会副主任）",
     "start": "2002-03", "end": "2020-10", "rank": "科级→副处级", "note": "期间曾挂职安义县黄洲镇科技副镇长（1999-2001）"},
    {"id": 19, "person_id": 3, "org_id": 16, "title": "南昌市城乡建设局党组书记、局长",
     "start": "2020-10", "end": "2021-09", "rank": "正处级", "note": ""},
    {"id": 20, "person_id": 3, "org_id": 1, "title": "进贤县委书记",
     "start": "2021-08", "end": "2026-06", "rank": "正处级",
     "note": "2021.08.01接替王强；2025.01兼南昌市政协常委"},
    {"id": 21, "person_id": 3, "org_id": 10, "title": "南昌市新建区委书记",
     "start": "2026-06", "end": "", "rank": "正处级", "note": "约2026年6月底/7月初到任"},

    # ── 钱太高 (4) ──
    {"id": 22, "person_id": 4, "org_id": 24, "title": "新建县松湖镇人民政府科员",
     "start": "1999-09", "end": "2002-12", "rank": "科员", "note": ""},
    {"id": 23, "person_id": 4, "org_id": 25, "title": "南昌市药品监督管理局科员",
     "start": "2002-12", "end": "2004-04", "rank": "科员", "note": ""},
    {"id": 24, "person_id": 4, "org_id": 12, "title": "南昌市食品药品监督管理局食品安全监察处负责人/副处长/处长",
     "start": "2004-04", "end": "2011-01", "rank": "科级", "note": ""},
    {"id": 25, "person_id": 4, "org_id": 12, "title": "南昌市食药监局保健食品化妆品监管处处长、稽查处处长、办公室主任",
     "start": "2011-01", "end": "2017-07", "rank": "正科级", "note": ""},
    {"id": 26, "person_id": 4, "org_id": 12, "title": "南昌市食药监局党组成员、食品药品安全总监",
     "start": "2017-07", "end": "2019-01", "rank": "副处级", "note": ""},
    {"id": 27, "person_id": 4, "org_id": 11, "title": "南昌市市场监督管理局党组成员（其间驻厦门、广州招商）",
     "start": "2019-01", "end": "2021-08", "rank": "副处级", "note": "机构改革，食药监局并入市管局"},
    {"id": 28, "person_id": 4, "org_id": 1, "title": "进贤县委常委、政法委书记",
     "start": "2021-09", "end": "2025-01", "rank": "副处级", "note": "三级调研员"},
    {"id": 29, "person_id": 4, "org_id": 2, "title": "进贤县委常委、常务副县长",
     "start": "2025-01-27", "end": "", "rank": "副处级",
     "note": "2025.01.27 县第十八届人大常委会第二十八次会议任命；分管发改、财政、税务等"},

    # ── 聂红兵 (5) ──
    {"id": 30, "person_id": 5, "org_id": 26, "title": "青云谱区三店小学教师（借调区委办/教科体局/外经贸委）",
     "start": "1999-08", "end": "2005-08", "rank": "", "note": ""},
    {"id": 31, "person_id": 5, "org_id": 27, "title": "青云谱区外经贸委副主任",
     "start": "2005-08", "end": "2007-02", "rank": "副科级", "note": ""},
    {"id": 32, "person_id": 5, "org_id": 28, "title": "青云谱区委办公室副主任/主任",
     "start": "2007-02", "end": "2011-04", "rank": "正科级",
     "note": "2011.04因拉票被免职，取消副县级后备干部资格"},
    {"id": 33, "person_id": 5, "org_id": 29, "title": "青云谱区重点项目办常务副主任/主任",
     "start": "2011-04", "end": "2017-05", "rank": "正科级", "note": ""},
    {"id": 34, "person_id": 5, "org_id": 30, "title": "青云谱区投资促进局负责人/副局长",
     "start": "2015-02", "end": "2017-05", "rank": "正科级", "note": ""},
    {"id": 35, "person_id": 5, "org_id": 31, "title": "南昌小蓝经开区招商中心主任",
     "start": "2017-05", "end": "2020-08", "rank": "正科级", "note": ""},
    {"id": 36, "person_id": 5, "org_id": 32, "title": "南昌小蓝经开区招商局局长",
     "start": "2020-08", "end": "2024-01", "rank": "副处级", "note": "其间2020.06-2022.05兼区党群部负责人"},
    {"id": 37, "person_id": 5, "org_id": 2, "title": "进贤县委常委、副县长，兼进贤产业园（医科园）党工委书记",
     "start": "2024-02-09", "end": "", "rank": "副处级",
     "note": "2024.01.30任前公示，02.09任命"},

    # ── 叶飞 (6) ──
    {"id": 38, "person_id": 6, "org_id": 15, "title": "青山湖区多岗位（教师→教育局→人大办→扬子洲镇长→南钢街道书记→区政府办主任→副区长→常委/宣传部长）",
     "start": "1996-09", "end": "2021-08", "rank": "科员→副处级", "note": "青山湖区工作25年"},
    {"id": 39, "person_id": 6, "org_id": 3, "title": "安义县委常委、常务副县长",
     "start": "2021-08", "end": "2023-01", "rank": "副处级", "note": ""},
    {"id": 40, "person_id": 6, "org_id": 3, "title": "安义县委副书记",
     "start": "2023-01", "end": "2024-11", "rank": "副处级", "note": ""},
    {"id": 41, "person_id": 6, "org_id": 1, "title": "进贤县委副书记",
     "start": "2024-11", "end": "", "rank": "副处级",
     "note": "协助县委书记分管党建、农业农村、乡村振兴、教育、群团等；兼县委党校校长"},

    # ── 徐永钢 (7) ──
    {"id": 42, "person_id": 7, "org_id": 38, "title": "南昌县武阳镇副镇长",
     "start": "2011-05", "end": "2015-01", "rank": "副科级", "note": "此前在南昌县政府办（2004-2011）"},
    {"id": 43, "person_id": 7, "org_id": 39, "title": "南昌县委办公室副主任",
     "start": "2015-01", "end": "2016-06", "rank": "副科级", "note": ""},
    {"id": 44, "person_id": 7, "org_id": 40, "title": "南昌县黄马乡党委副书记、乡长",
     "start": "2016-06", "end": "2019-03", "rank": "正科级", "note": ""},
    {"id": 45, "person_id": 7, "org_id": 41, "title": "南昌县医疗保障局党组书记",
     "start": "2019-03", "end": "2020-07", "rank": "正科级", "note": ""},
    {"id": 46, "person_id": 7, "org_id": 38, "title": "南昌县武阳镇党委书记",
     "start": "2020-11", "end": "2021-01", "rank": "正科级", "note": ""},
    {"id": 47, "person_id": 7, "org_id": 2, "title": "进贤县副县长",
     "start": "2021-01", "end": "2023-05", "rank": "副处级", "note": ""},
    {"id": 48, "person_id": 7, "org_id": 1, "title": "进贤县委常委、组织部部长",
     "start": "2023-05", "end": "", "rank": "副处级", "note": ""},

    # ── 熊军 (11) ──
    {"id": 49, "person_id": 11, "org_id": 42, "title": "南昌县莲塘镇政府工作",
     "start": "1996-12", "end": "2000-12", "rank": "科员", "note": ""},
    {"id": 50, "person_id": 11, "org_id": 43, "title": "南昌县社科联副主席",
     "start": "2000-12", "end": "2006-03", "rank": "副科级", "note": ""},
    {"id": 51, "person_id": 11, "org_id": 44, "title": "南昌县委宣传部副部长/常务副部长（兼文广旅游局局长）",
     "start": "2006-03", "end": "2016-06", "rank": "正科级", "note": ""},
    {"id": 52, "person_id": 11, "org_id": 40, "title": "南昌县黄马乡党委书记",
     "start": "2016-06", "end": "2021-03", "rank": "正科级", "note": ""},
    {"id": 53, "person_id": 11, "org_id": 39, "title": "南昌县委办公室主任",
     "start": "2021-03", "end": "2021-08", "rank": "正科级", "note": ""},
    {"id": 54, "person_id": 11, "org_id": 2, "title": "进贤县副县长",
     "start": "2021-10", "end": "", "rank": "副处级", "note": "分管自然资源、林业、住建、交通"},

    # ── 陶仲新 (13) ──
    {"id": 55, "person_id": 13, "org_id": 45, "title": "进贤县李渡镇党委书记",
     "start": "", "end": "2025-06", "rank": "正科级", "note": ""},
    {"id": 56, "person_id": 13, "org_id": 2, "title": "进贤县副县长",
     "start": "2025-06-27", "end": "", "rank": "副处级", "note": "2025.06.12公示，06.27任命"},

    # ── 何勇 (14) ──
    {"id": 57, "person_id": 14, "org_id": 46, "title": "南昌市公安局水上分局局长",
     "start": "", "end": "2025-08", "rank": "正科级", "note": ""},
    {"id": 58, "person_id": 14, "org_id": 2, "title": "进贤县副县长、公安局局长",
     "start": "2025-09-29", "end": "", "rank": "副处级", "note": "接替高波"},

    # ── 邓之武 (17) ──
    {"id": 59, "person_id": 17, "org_id": 1, "title": "进贤县委常委、常务副县长",
     "start": "", "end": "2024-12", "rank": "副处级", "note": "2024.12公示拟任县区委副书记"},
    {"id": 60, "person_id": 17, "org_id": 50, "title": "东湖区委副书记、区长提名人选",
     "start": "2025", "end": "", "rank": "正处级", "note": ""},

    # ── 涂莉花 (16) ──
    {"id": 61, "person_id": 16, "org_id": 1, "title": "进贤县委常委、统战部部长",
     "start": "", "end": "2024-12", "rank": "副处级",
     "note": "2024.12公示拟提名为县区人大常委会主任候选人"},
    {"id": 62, "person_id": 16, "org_id": 10, "title": "新建区人大常委会主任",
     "start": "2025", "end": "", "rank": "正处级", "note": ""},

    # ── 熊辉 (18) ──
    {"id": 63, "person_id": 18, "org_id": 2, "title": "进贤县县长",
     "start": "", "end": "2026", "rank": "正处级", "note": "雷桥亮接替"},
    {"id": 64, "person_id": 18, "org_id": 3, "title": "安义县委书记",
     "start": "2026", "end": "", "rank": "正处级", "note": ""},

    # ── 谭伯乐 (15) ──
    {"id": 65, "person_id": 15, "org_id": 4, "title": "安义县委副书记、县长",
     "start": "2020", "end": "2021", "rank": "正处级", "note": ""},
    {"id": 66, "person_id": 15, "org_id": 3, "title": "安义县委书记",
     "start": "2021", "end": "2025", "rank": "正处级", "note": ""},
    {"id": 67, "person_id": 15, "org_id": 47, "title": "南昌市政协副主席",
     "start": "2025-01", "end": "", "rank": "副厅级", "note": "兼任安义县委书记"},

    # ── 杨武 (19) ──
    {"id": 68, "person_id": 19, "org_id": 48, "title": "进贤县白圩乡党委书记",
     "start": "", "end": "2024-05", "rank": "正科级", "note": ""},
    {"id": 69, "person_id": 19, "org_id": 4, "title": "安义县副县长",
     "start": "2024-05", "end": "", "rank": "副处级", "note": "2024.05任前公示"},

    # ── 舒丹 (10) ──
    {"id": 70, "person_id": 10, "org_id": 49, "title": "共青团南昌市委多岗位",
     "start": "", "end": "", "rank": "科级", "note": "维权部副主任/办公室主任/青工部长"},
    {"id": 71, "person_id": 10, "org_id": 2, "title": "进贤县副县长",
     "start": "2021-01", "end": "", "rank": "副处级", "note": "无党派；分管卫健、医保、文旅、教体"},
    {"id": 72, "person_id": 12, "org_id": 47, "title": "南昌市政协办公厅秘书处处长、一级主任科员",
     "start": "", "end": "2021-08", "rank": "正科级", "note": ""},
    {"id": 73, "person_id": 12, "org_id": 2, "title": "进贤县副县长",
     "start": "2021", "end": "", "rank": "副处级", "note": "2021.08任前公示；分管环保、城管、市监等"},
    {"id": 74, "person_id": 8, "org_id": 49, "title": "共青团南昌市委统战部部长",
     "start": "", "end": "2016-06", "rank": "正科级", "note": "2016.06拟任团市委副书记"},
    {"id": 75, "person_id": 8, "org_id": 1, "title": "进贤县委常委、统战部部长",
     "start": "", "end": "", "rank": "副处级", "note": "兼县政协党组副书记、县民宗局局长"},
]

# ── Relationships: person-person edges with context ──
relationships = [
    {"id": 1, "person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "2026年7月起：熊振强（县委书记）与雷桥亮（县委副书记/县长提名人选）搭班子",
     "overlap_org": "中共进贤县委员会",
     "overlap_period": "2026-07至今"},
    {"id": 2, "person_a": 1, "person_b": 4, "type": "同县任职",
     "context": "熊振强（县委书记）与钱太高（县委常委/常务副县长）同在进贤县领导班子",
     "overlap_org": "中共进贤县委员会",
     "overlap_period": "2026-07至今"},
    {"id": 3, "person_a": 1, "person_b": 5, "type": "同县任职",
     "context": "熊振强（县委书记）与聂红兵（县委常委/副县长）同在进贤县领导班子",
     "overlap_org": "中共进贤县委员会",
     "overlap_period": "2026-07至今"},
    {"id": 4, "person_a": 1, "person_b": 6, "type": "同县任职",
     "context": "熊振强（县委书记）与叶飞（县委副书记）同在进贤县委班子",
     "overlap_org": "中共进贤县委员会",
     "overlap_period": "2026-07至今"},
    {"id": 5, "person_a": 1, "person_b": 3, "type": "职务接替",
     "context": "熊振强接替徐强出任进贤县委书记（2026年6/7月）",
     "overlap_org": "中共进贤县委员会",
     "overlap_period": "不重叠（前后任）"},
    {"id": 6, "person_a": 1, "person_b": 18, "type": "同期在安义",
     "context": "熊振强（安义县委常委2016-2021）与熊辉（安义县委书记2026-）无直接时间重叠；但熊振强在安义工作30年，与安义官场关系深厚",
     "overlap_org": "安义县",
     "overlap_period": "不确定"},
    {"id": 7, "person_a": 1, "person_b": 6, "type": "安义→进贤通道",
     "context": "熊振强和叶飞都曾长期在安义县任职：熊2016-2021（县委常委），叶2021-2024（县委常委→县委副书记）。二人在安义期间可能有工作交集（约2021年重叠）",
     "overlap_org": "安义县",
     "overlap_period": "2021（可能短暂重叠）"},
    {"id": 8, "person_a": 2, "person_b": 4, "type": "县政府搭档",
     "context": "雷桥亮（县长提名人选）与钱太高（常务副县长）搭档，钱协助雷处理县政府日常工作",
     "overlap_org": "进贤县人民政府",
     "overlap_period": "2026-07至今"},
    {"id": 9, "person_a": 2, "person_b": 5, "type": "县政府同事",
     "context": "雷桥亮（县长提名人选）与聂红兵（副县长）同在县政府班子，聂分管工业/招商",
     "overlap_org": "进贤县人民政府",
     "overlap_period": "2026-07至今"},
    {"id": 10, "person_a": 3, "person_b": 10, "type": "职务接替",
     "context": "前任县委书记徐强调任新建区委书记；涂莉花（进贤原统战部长）升任新建区人大常委会主任——徐强与涂莉花在新建区形成新的党政/人大交叉",
     "overlap_org": "进贤→新建",
     "overlap_period": "2025-2026（涂先到新建，徐后到新建）"},
    {"id": 11, "person_a": 4, "person_b": 17, "type": "职务接替",
     "context": "钱太高（2025.01起）接替邓之武担任进贤县常务副县长；邓之武调任东湖区委副书记",
     "overlap_org": "进贤县人民政府",
     "overlap_period": "不重叠（前后任）"},
    {"id": 12, "person_a": 6, "person_b": 1, "type": "安义连接",
     "context": "叶飞2021.08-2024.11在安义任职（县委常委/常务副县长→县委副书记）期间，熊振强已于2021.09调离安义去西湖区。二人交接期可能短暂重叠于2021年",
     "overlap_org": "安义县",
     "overlap_period": "2021.08-2021.09（可能短暂重叠）"},
    {"id": 13, "person_a": 7, "person_b": 11, "type": "南昌县→进贤通道",
     "context": "徐永钢和熊军都曾在南昌县黄马乡任职：徐2016-2019（乡长），熊2016-2021（党委书记）。二人在黄马乡有明确的共事关系，熊是徐的上级",
     "overlap_org": "南昌县黄马乡",
     "overlap_period": "2016-06至2019-03"},
    {"id": 14, "person_a": 7, "person_b": 11, "type": "进贤县同事",
     "context": "徐永钢（2021-2023副县长→2023至今组织部长）与熊军（2021至今副县长）同在进贤县任职约2年重叠",
     "overlap_org": "进贤县人民政府/中共进贤县委员会",
     "overlap_period": "2021-10至2023-05"},
    {"id": 15, "person_a": 15, "person_b": 19, "type": "进贤籍贯-安义任职",
     "context": "谭伯乐（进贤人，安义县委书记/县长）与杨武（进贤人，安义副县长）同为进贤籍干部在安义任职",
     "overlap_org": "安义县",
     "overlap_period": "2024-05至2025-01"},
    {"id": 16, "person_a": 18, "person_b": 1, "type": "间接接替",
     "context": "熊辉曾任进贤县长（雷桥亮前任）；熊振强现任进贤县委书记。两人同姓熊，但来自不同地方（熊振强奉新人，熊辉背景不明）",
     "overlap_org": "进贤县",
     "overlap_period": "无直接重叠"},
    {"id": 17, "person_a": 3, "person_b": 17, "type": "南昌县→进贤→新建/东湖",
     "context": "徐强（南昌县人）曾任进贤县委书记（2021-2026），邓之武曾任进贤县委常委/常务副县长（至2024.12），涂莉花曾任进贤县委常委/统战部长（至2024.12）。三人先后离开进贤，徐去了新建区，邓去了东湖区，涂去了新建区人大",
     "overlap_org": "进贤县",
     "overlap_period": "2021-2024"},
    {"id": 18, "person_a": 1, "person_b": 8, "type": "在进贤共事",
     "context": "熊振强任县委书记时，曾晋为县委常委/统战部长（仍在原位）",
     "overlap_org": "中共进贤县委员会",
     "overlap_period": "2026-07至今"},
]

# ── BUILD SQLITE ─────────────────────────────────────────────────────

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.executescript("""
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
    id INTEGER PRIMARY KEY,
    person_id INTEGER NOT NULL,
    org_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    start TEXT,
    "end" TEXT,
    rank TEXT,
    note TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);

CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY,
    person_a INTEGER NOT NULL,
    person_b INTEGER NOT NULL,
    type TEXT,
    context TEXT,
    overlap_org TEXT,
    overlap_period TEXT,
    FOREIGN KEY (person_a) REFERENCES persons(id),
    FOREIGN KEY (person_b) REFERENCES persons(id)
);

CREATE INDEX IF NOT EXISTS idx_positions_person ON positions(person_id);
CREATE INDEX IF NOT EXISTS idx_positions_org ON positions(org_id);
CREATE INDEX IF NOT EXISTS idx_rel_a ON relationships(person_a);
CREATE INDEX IF NOT EXISTS idx_rel_b ON relationships(person_b);
""")

for p in persons:
    c.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
              (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
               p["birthplace"], p["education"], p["party_join"], p["work_start"],
               p["current_post"], p["current_org"], p["source"]))

for o in organizations:
    c.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)",
              (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for pos in positions:
    c.execute("INSERT OR REPLACE INTO positions VALUES (?,?,?,?,?,?,?,?)",
              (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
               pos["start"], pos["end"], pos["rank"], pos["note"]))

for r in relationships:
    c.execute("INSERT OR REPLACE INTO relationships VALUES (?,?,?,?,?,?,?)",
              (r["id"], r["person_a"], r["person_b"], r["type"],
               r["context"], r["overlap_org"], r["overlap_period"]))

conn.commit()

# Verify
counts = {}
for t in ["persons", "organizations", "positions", "relationships"]:
    counts[t] = c.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
print(f"SQLite DB written: {DB_PATH}")
for t, n in counts.items():
    print(f"  {t}: {n} records")

conn.close()

# ── BUILD GEXF ───────────────────────────────────────────────────────

os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(post):
    if "书记" in post and "县委" in post:
        return "255,50,50"
    elif "县长" in post or "副县长" in post:
        return "50,100,255"
    elif "纪委书记" in post or "监委" in post:
        return "255,165,0"
    else:
        return "100,100,100"


def org_color(otype):
    m = {"党委": "255,200,200", "政府": "200,200,255", "开发区": "200,255,200",
         "乡镇": "255,255,200", "事业单位": "220,220,220", "群团": "255,220,255",
         "人大": "200,255,255", "政协": "255,240,200", "街道": "240,240,200",
         "新区": "255,220,220"}
    return m.get(otype, "200,200,200")


lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Claude Code Research Agent</creator>')
lines.append('    <description>江西省南昌市进贤县领导班子工作关系网络 — 2026年7月14日生成</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Node attributes
lines.append('    <attributes class="node">')
for aid, atitle, atype in [("0", "type", "string"), ("1", "birth", "string"),
                            ("2", "birthplace", "string"), ("3", "current_post", "string"),
                            ("4", "entity_type", "string"), ("5", "level", "string")]:
    lines.append(f'      <attribute id="{aid}" title="{atitle}" type="{atype}"/>')
lines.append('    </attributes>')

# Edge attributes
lines.append('    <attributes class="edge">')
for aid, atitle, atype in [("0", "type", "string"), ("1", "start", "string"),
                            ("2", "end", "string"), ("3", "context", "string")]:
    lines.append(f'      <attribute id="{aid}" title="{atitle}" type="{atype}"/>')
lines.append('    </attributes>')

# Nodes
lines.append('    <nodes>')
for p in persons:
    c = person_color(p.get("current_post", ""))
    sz = "20.0" if "书记" in p.get("current_post", "") else "12.0"
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="person"/>')
    lines.append(f'          <attvalue for="1" value="{esc(p.get("birth",""))}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(p.get("birthplace",""))}"/>')
    lines.append(f'          <attvalue for="3" value="{esc(p.get("current_post",""))}"/>')
    lines.append(f'          <attvalue for="4" value="person"/>')
    lines.append(f'          <attvalue for="5" value=""/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')

for o in organizations:
    c = org_color(o.get("type", ""))
    lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="organization"/>')
    lines.append(f'          <attvalue for="1" value=""/>')
    lines.append(f'          <attvalue for="2" value="{esc(o.get("location",""))}"/>')
    lines.append(f'          <attvalue for="3" value=""/>')
    lines.append(f'          <attvalue for="4" value="organization"/>')
    lines.append(f'          <attvalue for="5" value="{esc(o.get("level",""))}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append('      </node>')

lines.append('    </nodes>')

# Edges
lines.append('    <edges>')
edge_id = 0
for pos in positions:
    edge_id += 1
    lines.append(f'      <edge id="{edge_id}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="worked_at"/>')
    lines.append(f'          <attvalue for="1" value="{esc(pos.get("start",""))}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(pos.get("end",""))}"/>')
    lines.append(f'          <attvalue for="3" value="{esc(pos.get("note",""))}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

for r in relationships:
    edge_id += 1
    ov = r.get("overlap_period", "")
    ov_start = ov.split("至今")[0] if "至今" in ov else ov
    lines.append(f'      <edge id="{edge_id}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
    lines.append(f'          <attvalue for="1" value="{esc(ov_start)}"/>')
    lines.append(f'          <attvalue for="2" value=""/>')
    lines.append(f'          <attvalue for="3" value="{esc(r.get("context",""))}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

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
