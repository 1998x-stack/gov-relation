#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Anyi County cross-county cadre exchange network."""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/anyi_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/anyi_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Anyi County current and recent leaders ──
    {"id": 1, "name": "熊辉", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-03", "birthplace": "江西奉新", "education": "博士研究生",
     "party_join": "2006-05", "work_start": "2002-09",
     "current_post": "安义县委书记", "current_org": "中共安义县委员会",
     "source": "https://baike.baidu.com/item/%E7%86%8A%E8%BE%89/18041563"},
    {"id": 2, "name": "刘志伟", "gender": "男", "ethnicity": "汉族",
     "birth": "1984-07", "birthplace": "", "education": "大学，教育学学士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "安义县委常委（主持县政府日常工作）", "current_org": "中共安义县委员会",
     "source": "https://anyi.nc.gov.cn/ayxzf/ldzc/ldzc.shtml"},
    {"id": 3, "name": "罗国栋", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-10", "birthplace": "江西吉水", "education": "中央党校研究生",
     "party_join": "2001-06", "work_start": "2003-07",
     "current_post": "青云谱区委书记", "current_org": "中共南昌市青云谱区委员会",
     "source": "https://www.thepaper.cn/newsDetail_forward_13980548"},
    {"id": 4, "name": "谭伯乐", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-07", "birthplace": "", "education": "中央党校大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "南昌市政协副主席", "current_org": "南昌市政协",
     "source": "https://jx.sina.com.cn/news/b/2025-01-13/detail-ineeutxf9760625.shtml"},
    {"id": 5, "name": "彭开先", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "南昌市人民政府副市长", "current_org": "南昌市人民政府",
     "source": "https://m.thepaper.cn/newsDetail_forward_5459994"},
    {"id": 6, "name": "李松殿", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "南昌市委常委、宣传部部长兼新建区委书记", "current_org": "中共南昌市委宣传部",
     "source": "http://renshi.people.com.cn/n1/2019/0430/c139617-31060115.html"},
    {"id": 7, "name": "乐文红", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "南昌市委常委、统战部部长", "current_org": "中共南昌市委统战部",
     "source": "https://m.thepaper.cn/newsDetail_forward_4359283"},
    {"id": 8, "name": "周亮", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "原红谷滩区委书记（已退休被查）", "current_org": "",
     "source": "https://baike.baidu.com/item/%E5%91%A8%E4%BA%AE/8255243"},
    {"id": 9, "name": "梅梅", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "南昌市林业局党组书记", "current_org": "南昌市林业局",
     "source": "https://baike.baidu.com/item/%E6%A2%85%E6%A2%85/1030181"},
    {"id": 10, "name": "杨峻", "gender": "男", "ethnicity": "汉族",
     "birth": "1978-06", "birthplace": "江西南昌", "education": "研究生",
     "party_join": "中共党员", "work_start": "1996-09",
     "current_post": "安义县委常委、宣传部部长", "current_org": "中共安义县委员会",
     "source": "https://anyi.nc.gov.cn/ayxzf/xwld/202101/d0954437573a49b28a9ae7fe537c7ab9.shtml"},
    {"id": 11, "name": "余建国", "gender": "男", "ethnicity": "汉族",
     "birth": "1969-09", "birthplace": "江西安义", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "安义县委常委、政法委书记", "current_org": "中共安义县委员会",
     "source": "https://www.newton.com.tw/wiki/%E4%BD%99%E5%BB%BA%E5%9C%8B/23706003"},
    {"id": 12, "name": "张帆", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-09", "birthplace": "江西南昌", "education": "全日制大学，公共管理硕士",
     "party_join": "2007-09", "work_start": "2003-07",
     "current_post": "安义县委常委、统战部部长", "current_org": "中共安义县委员会",
     "source": "https://anyi.nc.gov.cn/ayxzf/xwld/202108/217fbf6d5eeb4c6386888ddbf4e9d403.shtml"},
    {"id": 13, "name": "谭翼直", "gender": "男", "ethnicity": "汉族",
     "birth": "1988-05", "birthplace": "江西都昌", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "安义县委常委、常务副县长", "current_org": "安义县人民政府",
     "source": "https://www.newton.com.tw/wiki/%E8%AD%9A%E7%BF%BC%E7%9B%B4/61754939"},
    {"id": 14, "name": "余超", "gender": "男", "ethnicity": "汉族",
     "birth": "1983-08", "birthplace": "江西都昌", "education": "硕士研究生",
     "party_join": "2004-05", "work_start": "2008-06",
     "current_post": "安义县委常委、副县长", "current_org": "安义县人民政府",
     "source": "https://anyi.nc.gov.cn/ayxzf/xwld/202504/db551054acbd43cea5283a58933dc8a7.shtml"},
    {"id": 15, "name": "金栋", "gender": "男", "ethnicity": "汉族",
     "birth": "1979-11", "birthplace": "江西乐平", "education": "在职研究生，法学硕士",
     "party_join": "2002-05", "work_start": "2002-07",
     "current_post": "安义县委常委、纪委书记、监委主任", "current_org": "中共安义县纪律检查委员会",
     "source": "https://baike.baidu.com/item/%E9%87%91%E6%A0%8B/57504166"},
    {"id": 16, "name": "万菁", "gender": "女", "ethnicity": "汉族",
     "birth": "1982-10", "birthplace": "江西南昌", "education": "大学本科",
     "party_join": "民盟", "work_start": "2003-11",
     "current_post": "安义县副县长", "current_org": "安义县人民政府",
     "source": "https://anyi.nc.gov.cn/ayxzf/govld/202503/6eb3b7908fb24f23a3e67d34eaf6a78e.shtml"},
    {"id": 17, "name": "刘彬", "gender": "男", "ethnicity": "汉族",
     "birth": "1978-10", "birthplace": "", "education": "在职大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "安义县副县长", "current_org": "安义县人民政府",
     "source": "https://anyi.nc.gov.cn/ayxzf/govld/202108/5de6e026465e4fc3aa4ba242db4216cc.shtml"},
    {"id": 18, "name": "赵伟", "gender": "男", "ethnicity": "汉族",
     "birth": "1982-02", "birthplace": "山东郓城", "education": "大学本科",
     "party_join": "中共党员", "work_start": "2004-07",
     "current_post": "安义县副县长、高新园区党工委书记", "current_org": "安义县人民政府",
     "source": "https://baike.baidu.com/item/%E8%B5%B5%E4%BC%9F/58349955"},
    {"id": 19, "name": "杨武", "gender": "男", "ethnicity": "汉族",
     "birth": "1984-11", "birthplace": "江西进贤", "education": "博士研究生",
     "party_join": "中共党员", "work_start": "2013-09",
     "current_post": "安义县副县长、县城投集团党委第一书记", "current_org": "安义县人民政府",
     "source": "https://baike.baidu.com/item/%E6%9D%A8%E6%AD%A6/64486336"},
    {"id": 20, "name": "邓梁", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-05", "birthplace": "江西南昌", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "安义县副县长、公安局局长", "current_org": "安义县人民政府",
     "source": "https://anyi.nc.gov.cn/ayxzf/govld/202507/4f9f341fe4f14f6d87a10f369605fa84.shtml"},
    {"id": 21, "name": "袁一旦", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "青山湖区委书记", "current_org": "中共南昌市青山湖区委员会",
     "source": "https://ncqsh.nc.gov.cn/ncqsh/qwsj/202104/67ea96ec2a1c48389c811a24fb312dd5.shtml"},
    {"id": 22, "name": "周荣卿", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "九江市浔阳区委书记", "current_org": "中共九江市浔阳区委员会",
     "source": "https://baike.baidu.com/item/%E5%91%A8%E8%8D%A3%E5%8D%BF/19864833"},
    {"id": 23, "name": "熊振强", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-03", "birthplace": "江西奉新", "education": "大学",
     "party_join": "1992-12", "work_start": "1991-09",
     "current_post": "进贤县委书记", "current_org": "中共进贤县委员会",
     "source": "https://baike.baidu.com/item/%E7%86%8A%E8%99%8E/"},
    {"id": 24, "name": "徐强", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-11", "birthplace": "江西南昌县", "education": "MPA硕士",
     "party_join": "1996-06", "work_start": "1996-09",
     "current_post": "新建区委书记", "current_org": "中共南昌市新建区委员会",
     "source": "https://baike.baidu.com/item/%E5%BE%90%E5%BC%BA/50081202"},
    {"id": 25, "name": "陈奕蒙", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "红谷滩区委书记", "current_org": "中共南昌市红谷滩区委员会",
     "source": "https://www.163.com/dy/article/L1LE2GI505563DJA.html"},
    {"id": 26, "name": "杨育星", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "青山湖区委书记", "current_org": "中共南昌市青山湖区委员会",
     "source": "https://www.163.com/dy/article/L1LE2GI505563DJA.html"},
    {"id": 27, "name": "郑绍", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "靖安县委书记（曾任永修县长）", "current_org": "中共靖安县委员会",
     "source": "https://m.thepaper.cn/newsDetail_forward_15055739"},
    {"id": 28, "name": "詹晓庆", "gender": "女", "ethnicity": "汉族",
     "birth": "1981-12", "birthplace": "江西丰城", "education": "研究生",
     "party_join": "2004-11", "work_start": "2006-06",
     "current_post": "安义县委常委、组织部部长", "current_org": "中共安义县委员会",
     "source": "https://anyi.nc.gov.cn/ayxzf/xwld/202603/e13250fcb2604e6ea392f1fe04c01804.shtml"},
    {"id": 29, "name": "吴威", "gender": "男", "ethnicity": "汉族",
     "birth": "1983", "birthplace": "河南遂平", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "安义县委常委、人武部部长", "current_org": "安义县人民武装部",
     "source": "https://anyi.nc.gov.cn/ayxzf/ldzc/ldzc.shtml"},
    {"id": 30, "name": "叶飞", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-03", "birthplace": "江西进贤", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "1996-09",
     "current_post": "进贤县委副书记（原安义县委副书记）", "current_org": "中共进贤县委员会",
     "source": "https://anyi.nc.gov.cn/ayxzf/xwld/"},
]

organizations = [
    # ── Anyi County orgs ──
    {"id": 1, "name": "中共安义县委员会", "type": "党委", "level": "县级",
     "parent": "中共南昌市委员会", "location": "江西省南昌市安义县"},
    {"id": 2, "name": "安义县人民政府", "type": "政府", "level": "县级",
     "parent": "南昌市人民政府", "location": "江西省南昌市安义县"},
    {"id": 3, "name": "中共安义县纪律检查委员会", "type": "党委", "level": "县级",
     "parent": "中共南昌市纪律检查委员会", "location": "江西省南昌市安义县"},
    {"id": 4, "name": "安义县人民武装部", "type": "政府", "level": "县级",
     "parent": "南昌警备区", "location": "江西省南昌市安义县"},
    {"id": 5, "name": "安义县高新园区", "type": "开发区", "level": "县级",
     "parent": "安义县人民政府", "location": "江西省南昌市安义县"},

    # ── Source counties/districts ──
    {"id": 6, "name": "中共进贤县委员会", "type": "党委", "level": "县级",
     "parent": "中共南昌市委员会", "location": "江西省南昌市进贤县"},
    {"id": 7, "name": "进贤县人民政府", "type": "政府", "level": "县级",
     "parent": "南昌市人民政府", "location": "江西省南昌市进贤县"},
    {"id": 8, "name": "进贤县白圩乡", "type": "乡镇", "level": "乡镇级",
     "parent": "进贤县人民政府", "location": "江西省南昌市进贤县"},
    {"id": 9, "name": "中共南昌县委员会", "type": "党委", "level": "县级",
     "parent": "中共南昌市委员会", "location": "江西省南昌市南昌县"},
    {"id": 10, "name": "南昌县人民政府", "type": "政府", "level": "县级",
     "parent": "南昌市人民政府", "location": "江西省南昌市南昌县"},
    {"id": 11, "name": "南昌县幽兰镇", "type": "乡镇", "level": "乡镇级",
     "parent": "南昌县人民政府", "location": "江西省南昌市南昌县"},
    {"id": 12, "name": "中共南昌市青云谱区委员会", "type": "党委", "level": "区级",
     "parent": "中共南昌市委员会", "location": "江西省南昌市青云谱区"},
    {"id": 13, "name": "中共南昌市青山湖区委员会", "type": "党委", "level": "区级",
     "parent": "中共南昌市委员会", "location": "江西省南昌市青山湖区"},
    {"id": 14, "name": "中共南昌市新建区委员会", "type": "党委", "level": "区级",
     "parent": "中共南昌市委员会", "location": "江西省南昌市新建区"},
    {"id": 15, "name": "中共南昌市红谷滩区委员会", "type": "党委", "level": "区级",
     "parent": "中共南昌市委员会", "location": "江西省南昌市红谷滩区"},
    {"id": 16, "name": "南昌市人民政府", "type": "政府", "level": "市级",
     "parent": "江西省人民政府", "location": "江西省南昌市"},
    {"id": 17, "name": "南昌市政协", "type": "政协", "level": "市级",
     "parent": "", "location": "江西省南昌市"},
    {"id": 18, "name": "南昌市委统战部", "type": "党委", "level": "市级",
     "parent": "中共南昌市委员会", "location": "江西省南昌市"},
    {"id": 19, "name": "南昌市财政局", "type": "政府", "level": "市级",
     "parent": "南昌市人民政府", "location": "江西省南昌市"},
    {"id": 20, "name": "南昌市公安局", "type": "政府", "level": "市级",
     "parent": "南昌市人民政府", "location": "江西省南昌市"},
    {"id": 21, "name": "南昌市林业局", "type": "政府", "level": "市级",
     "parent": "南昌市人民政府", "location": "江西省南昌市"},
    {"id": 22, "name": "中共南昌市委宣传部", "type": "党委", "level": "市级",
     "parent": "中共南昌市委员会", "location": "江西省南昌市"},
    {"id": 23, "name": "中共南昌市委办公室", "type": "党委", "level": "市级",
     "parent": "中共南昌市委员会", "location": "江西省南昌市"},
    {"id": 24, "name": "中共江西省委办公厅", "type": "党委", "level": "省级",
     "parent": "中共江西省委员会", "location": "江西省南昌市"},
    {"id": 25, "name": "江西省工业和信息化厅", "type": "政府", "level": "省级",
     "parent": "江西省人民政府", "location": "江西省南昌市"},
    {"id": 26, "name": "安义县长埠镇", "type": "乡镇", "level": "乡镇级",
     "parent": "安义县人民政府", "location": "江西省南昌市安义县"},
    {"id": 27, "name": "安义县乔乐乡", "type": "乡镇", "level": "乡镇级",
     "parent": "安义县人民政府", "location": "江西省南昌市安义县"},
    {"id": 28, "name": "安义县龙津镇", "type": "乡镇", "level": "乡镇级",
     "parent": "安义县人民政府", "location": "江西省南昌市安义县"},
    {"id": 29, "name": "安义县东阳镇", "type": "乡镇", "level": "乡镇级",
     "parent": "安义县人民政府", "location": "江西省南昌市安义县"},
    {"id": 30, "name": "安义县委办公室", "type": "党委", "level": "县级",
     "parent": "中共安义县委员会", "location": "江西省南昌市安义县"},
    {"id": 31, "name": "中共九江市浔阳区委员会", "type": "党委", "level": "区级",
     "parent": "中共九江市委员会", "location": "江西省九江市浔阳区"},
    {"id": 32, "name": "南昌市青山湖区人民政府", "type": "政府", "level": "区级",
     "parent": "南昌市人民政府", "location": "江西省南昌市青山湖区"},
    {"id": 33, "name": "南昌市西湖区人民政府", "type": "政府", "level": "区级",
     "parent": "南昌市人民政府", "location": "江西省南昌市西湖区"},
    {"id": 34, "name": "南昌市交通运输局", "type": "政府", "level": "市级",
     "parent": "南昌市人民政府", "location": "江西省南昌市"},
    {"id": 35, "name": "中共靖安县委员会", "type": "党委", "level": "县级",
     "parent": "中共宜春市委员会", "location": "江西省宜春市靖安县"},
    {"id": 36, "name": "南昌市公路事业发展中心", "type": "事业单位", "level": "市级",
     "parent": "南昌市人民政府", "location": "江西省南昌市"},
]

# Position data: person → org with time ranges
positions = [
    # ── 熊辉 (1) ──
    {"id": 1, "person_id": 1, "org_id": 23, "title": "南昌市委组织部调研处副处长/处长",
     "start": "2009", "end": "2016", "rank": "正科级", "note": ""},
    {"id": 2, "person_id": 1, "org_id": 12, "title": "青云谱区副区长",
     "start": "2016", "end": "2020", "rank": "副处级", "note": "后任区委常委、组织部长"},
    {"id": 3, "person_id": 1, "org_id": 6, "title": "进贤县委副书记、县长",
     "start": "2021", "end": "2026-07", "rank": "正处级",
     "note": "从青云谱区委常委/组织部长调任"},
    {"id": 4, "person_id": 1, "org_id": 1, "title": "安义县委书记",
     "start": "2026-07-05", "end": "", "rank": "正处级",
     "note": "2026年7月南昌6县区联动调整，从进贤县长调任安义县委书记"},

    # ── 刘志伟 (2) ──
    {"id": 5, "person_id": 2, "org_id": 11, "title": "南昌县幽兰镇党委书记",
     "start": "", "end": "2020-03", "rank": "正科级", "note": ""},
    {"id": 6, "person_id": 2, "org_id": 2, "title": "安义县副县长提名人选",
     "start": "2020-03", "end": "2020-05", "rank": "副处级",
     "note": "2020年3月南昌36名领导干部任前公示"},
    {"id": 7, "person_id": 2, "org_id": 2, "title": "安义县委常委、常务副县长",
     "start": "2021", "end": "2025-02", "rank": "副处级",
     "note": "2025年2月免去副县长职务（保留县委常委）"},
    {"id": 8, "person_id": 2, "org_id": 1, "title": "安义县委常委（主持政府日常工作）",
     "start": "2025-02", "end": "", "rank": "副处级",
     "note": "实际主持县政府日常工作"},

    # ── 罗国栋 (3) ──
    {"id": 9, "person_id": 3, "org_id": 25, "title": "省工信委对外交流合作处处长",
     "start": "", "end": "2020-06", "rank": "正处级", "note": ""},
    {"id": 10, "person_id": 3, "org_id": 9, "title": "南昌县委副书记",
     "start": "2020-06", "end": "2021-08", "rank": "正处级",
     "note": "省直机关下派"},
    {"id": 11, "person_id": 3, "org_id": 2, "title": "安义县委副书记、代县长→县长",
     "start": "2021-08", "end": "2026-07", "rank": "正处级", "note": ""},
    {"id": 12, "person_id": 3, "org_id": 12, "title": "青云谱区委书记",
     "start": "2026-07-07", "end": "", "rank": "正处级",
     "note": "2026年7月南昌6县区联动调整"},

    # ── 谭伯乐 (4) ──
    {"id": 13, "person_id": 4, "org_id": 9, "title": "南昌县委副书记",
     "start": "", "end": "2020-01", "rank": "正处级", "note": ""},
    {"id": 14, "person_id": 4, "org_id": 2, "title": "安义县委副书记、县长",
     "start": "2020-04", "end": "2021-08", "rank": "正处级", "note": ""},
    {"id": 15, "person_id": 4, "org_id": 1, "title": "安义县委书记",
     "start": "2021-08", "end": "2025-01", "rank": "正处级", "note": ""},
    {"id": 16, "person_id": 4, "org_id": 17, "title": "南昌市政协副主席（副厅级）",
     "start": "2025-01", "end": "", "rank": "副厅级", "note": ""},

    # ── 彭开先 (5) ──
    {"id": 17, "person_id": 5, "org_id": 2, "title": "安义县委常委、常务副县长",
     "start": "2011-07", "end": "2015-07", "rank": "副处级", "note": ""},
    {"id": 18, "person_id": 5, "org_id": 2, "title": "安义县委副书记、县长",
     "start": "2016-10", "end": "2020-01", "rank": "正处级", "note": ""},
    {"id": 19, "person_id": 5, "org_id": 1, "title": "安义县委书记",
     "start": "2020-01", "end": "2021-08", "rank": "正处级", "note": ""},
    {"id": 20, "person_id": 5, "org_id": 16, "title": "南昌市副市长",
     "start": "2021-08", "end": "", "rank": "副厅级", "note": ""},

    # ── 李松殿 (6) ──
    {"id": 21, "person_id": 6, "org_id": 13, "title": "青山湖区委副书记、区长",
     "start": "", "end": "2014-09", "rank": "正处级", "note": ""},
    {"id": 22, "person_id": 6, "org_id": 1, "title": "安义县委书记",
     "start": "2014-09", "end": "2019-04", "rank": "正处级", "note": ""},
    {"id": 23, "person_id": 6, "org_id": 16, "title": "南昌市副市长",
     "start": "2019-04", "end": "2023", "rank": "副厅级",
     "note": "后任市委常委/宣传部长/新建区委书记"},

    # ── 乐文红 (7) ──
    {"id": 24, "person_id": 7, "org_id": 18, "title": "南昌市委常委、统战部部长（兼任安义县委书记）",
     "start": "2019-09", "end": "2020-01", "rank": "副厅级", "note": "过渡性兼任约4个月"},

    # ── 周亮 (8) ──
    {"id": 25, "person_id": 8, "org_id": 2, "title": "安义县委副书记、县长",
     "start": "2005-05", "end": "2011", "rank": "正处级", "note": "后任新建县长/青云谱书记/红谷滩书记"},
    {"id": 26, "person_id": 8, "org_id": 14, "title": "新建县委副书记、县长",
     "start": "2011", "end": "", "rank": "正处级", "note": ""},
    {"id": 27, "person_id": 8, "org_id": 15, "title": "红谷滩区委书记",
     "start": "", "end": "2021-08", "rank": "副厅级", "note": "2021年8月退休后被查"},

    # ── 梅梅 (9) ──
    {"id": 28, "person_id": 9, "org_id": 2, "title": "安义县委副书记、县长",
     "start": "2011", "end": "2016-08", "rank": "正处级", "note": "此前任南昌市妇联主席"},
    {"id": 29, "person_id": 9, "org_id": 21, "title": "南昌市林业局党组书记",
     "start": "2019-02", "end": "", "rank": "正处级", "note": "此前任市外事侨务办主任"},

    # ── 杨峻 (10) ──
    {"id": 30, "person_id": 10, "org_id": 1, "title": "安义县委常委、宣传部部长",
     "start": "", "end": "", "rank": "副处级", "note": "此前履历未公开"},

    # ── 余建国 (11) ──
    {"id": 31, "person_id": 11, "org_id": 26, "title": "安义县长埠镇干部/党委委员/纪委书记",
     "start": "", "end": "", "rank": "科级", "note": "安义本地人，本土成长"},
    {"id": 32, "person_id": 11, "org_id": 27, "title": "安义县乔乐乡党委副书记/乡长",
     "start": "", "end": "", "rank": "正科级", "note": ""},
    {"id": 33, "person_id": 11, "org_id": 28, "title": "安义县龙津镇镇长",
     "start": "", "end": "", "rank": "正科级", "note": ""},
    {"id": 34, "person_id": 11, "org_id": 29, "title": "安义县东阳镇党委书记",
     "start": "", "end": "2016", "rank": "正科级", "note": ""},
    {"id": 35, "person_id": 11, "org_id": 2, "title": "安义县副县长",
     "start": "2016", "end": "", "rank": "副处级", "note": ""},
    {"id": 36, "person_id": 11, "org_id": 1, "title": "安义县委常委、政法委书记",
     "start": "", "end": "", "rank": "副处级", "note": ""},

    # ── 张帆 (12) ──
    {"id": 37, "person_id": 12, "org_id": 1, "title": "安义县委常委、统战部部长",
     "start": "", "end": "", "rank": "副处级", "note": "此前履历未公开"},

    # ── 谭翼直 (13) ──
    {"id": 38, "person_id": 13, "org_id": 24, "title": "江西省委办公厅干部",
     "start": "", "end": "", "rank": "科级",
     "note": "曾挂点赣州市兴国县方太乡副乡长"},
    {"id": 39, "person_id": 13, "org_id": 23, "title": "南昌市委办公室副主任",
     "start": "", "end": "2023-07", "rank": "副处级", "note": ""},
    {"id": 40, "person_id": 13, "org_id": 2, "title": "安义县委常委、常务副县长",
     "start": "2023-07", "end": "", "rank": "副处级",
     "note": "省委办公厅→南昌市委→安义"},

    # ── 余超 (14) ──
    {"id": 41, "person_id": 14, "org_id": 19, "title": "南昌市财政局党组成员、副局长",
     "start": "", "end": "", "rank": "副处级", "note": ""},
    {"id": 42, "person_id": 14, "org_id": 2, "title": "安义县委常委、副县长",
     "start": "", "end": "", "rank": "副处级",
     "note": "市财政局→安义"},

    # ── 金栋 (15) ──
    {"id": 43, "person_id": 15, "org_id": 26, "title": "安义县长埠镇党委副书记、镇长→党委书记",
     "start": "", "end": "", "rank": "正科级", "note": "从南昌市直下派至安义乡镇"},
    {"id": 44, "person_id": 15, "org_id": 30, "title": "安义县委办公室主任",
     "start": "", "end": "", "rank": "正科级", "note": ""},
    {"id": 45, "person_id": 15, "org_id": 3, "title": "安义县委常委、纪委书记、监委主任",
     "start": "2025-02", "end": "", "rank": "副处级", "note": ""},

    # ── 万菁 (16) ──
    {"id": 46, "person_id": 16, "org_id": 2, "title": "安义县副县长（民盟）",
     "start": "2025", "end": "", "rank": "副处级", "note": "此前履历未公开"},

    # ── 刘彬 (17) ──
    {"id": 47, "person_id": 17, "org_id": 30, "title": "安义县委办公室主任",
     "start": "", "end": "", "rank": "正科级", "note": ""},
    {"id": 48, "person_id": 17, "org_id": 2, "title": "安义县副县长",
     "start": "", "end": "", "rank": "副处级", "note": "从县委办主任晋升"},

    # ── 赵伟 (18) ──
    {"id": 49, "person_id": 18, "org_id": 2, "title": "安义县副县长、高新园区党工委书记",
     "start": "", "end": "", "rank": "副处级",
     "note": "山东郓城人，跨省来源，此前履历未公开"},

    # ── 杨武 (19) ──
    {"id": 50, "person_id": 19, "org_id": 8, "title": "进贤县白圩乡党委副书记/党委牵头人",
     "start": "", "end": "2024-05", "rank": "正科级", "note": ""},
    {"id": 51, "person_id": 19, "org_id": 2, "title": "安义县副县长",
     "start": "2024-05", "end": "", "rank": "副处级",
     "note": "进贤县→安义县跨县调动"},

    # ── 邓梁 (20) ──
    {"id": 52, "person_id": 20, "org_id": 20, "title": "南昌市公安局政策研究室主任",
     "start": "", "end": "2025-06", "rank": "正科级", "note": "四级高级警长"},
    {"id": 53, "person_id": 20, "org_id": 2, "title": "安义县副县长、公安局局长",
     "start": "2025-06", "end": "", "rank": "副处级",
     "note": "市公安局→安义"},

    # ── 袁一旦 (21) ──
    {"id": 54, "person_id": 21, "org_id": 2, "title": "安义县副县长",
     "start": "2006-06", "end": "2011-07", "rank": "副处级", "note": ""},
    {"id": 55, "person_id": 21, "org_id": 6, "title": "进贤县委常委、纪委书记→常务副县长",
     "start": "2011-07", "end": "2016", "rank": "副处级", "note": ""},
    {"id": 56, "person_id": 21, "org_id": 33, "title": "西湖区委副书记",
     "start": "2016", "end": "2020", "rank": "副处级", "note": ""},
    {"id": 57, "person_id": 21, "org_id": 13, "title": "青山湖区委书记",
     "start": "2020-04", "end": "", "rank": "正处级",
     "note": "从安义副县长→...→青山湖书记，16年跨4县区"},

    # ── 周荣卿 (22) ──
    {"id": 58, "person_id": 22, "org_id": 1, "title": "安义县委副书记",
     "start": "", "end": "2021-07", "rank": "副处级", "note": ""},
    {"id": 59, "person_id": 22, "org_id": 31, "title": "九江市浔阳区委副书记、区长→区委书记",
     "start": "2021-08", "end": "", "rank": "正处级",
     "note": "跨设区市交流（南昌→九江）"},

    # ── 熊振强 (23) ──
    {"id": 60, "person_id": 23, "org_id": 1, "title": "安义县委常委、工业园区党工委书记",
     "start": "2016-07", "end": "2019-06", "rank": "副处级", "note": ""},
    {"id": 61, "person_id": 23, "org_id": 1, "title": "安义县委常委、政法委书记",
     "start": "2019-07", "end": "2021-09", "rank": "副处级", "note": ""},
    {"id": 62, "person_id": 23, "org_id": 33, "title": "南昌市西湖区委副书记",
     "start": "2021-09", "end": "2024-12", "rank": "副处级", "note": ""},
    {"id": 63, "person_id": 23, "org_id": 36, "title": "南昌市公路事业发展中心主任",
     "start": "2024-12", "end": "2025-12", "rank": "正处级", "note": ""},
    {"id": 64, "person_id": 23, "org_id": 34, "title": "南昌市交通运输局局长",
     "start": "2025-12", "end": "2026-07", "rank": "正处级", "note": ""},
    {"id": 65, "person_id": 23, "org_id": 6, "title": "进贤县委书记",
     "start": "2026-07", "end": "", "rank": "正处级",
     "note": "2026年7月联动调整"},

    # ── 徐强 (24) ──
    {"id": 66, "person_id": 24, "org_id": 6, "title": "进贤县委书记",
     "start": "2021-08", "end": "2026-06", "rank": "正处级", "note": ""},
    {"id": 67, "person_id": 24, "org_id": 14, "title": "新建区委书记",
     "start": "2026-06", "end": "", "rank": "正处级", "note": "2026年7月联动调整"},

    # ── 陈奕蒙 (25) ──
    {"id": 68, "person_id": 25, "org_id": 14, "title": "新建区委书记",
     "start": "", "end": "2026-07", "rank": "正处级", "note": ""},
    {"id": 69, "person_id": 25, "org_id": 15, "title": "红谷滩区委书记",
     "start": "2026-07", "end": "", "rank": "正处级", "note": ""},

    # ── 杨育星 (26) ──
    {"id": 70, "person_id": 26, "org_id": 32, "title": "青山湖区区长",
     "start": "", "end": "2026-07", "rank": "正处级", "note": ""},
    {"id": 71, "person_id": 26, "org_id": 13, "title": "青山湖区委书记",
     "start": "2026-07", "end": "", "rank": "正处级", "note": ""},

    # ── 郑绍 (27) ──
    {"id": 72, "person_id": 27, "org_id": 10, "title": "永修县委副书记、县长",
     "start": "", "end": "2019-08", "rank": "正处级", "note": "永修属九江市"},
    {"id": 73, "person_id": 27, "org_id": 35, "title": "靖安县委书记",
     "start": "2019-08", "end": "", "rank": "正处级",
     "note": "跨设区市交流：九江→宜春"},

    # ── 詹晓庆 (28) ──
    {"id": 74, "person_id": 28, "org_id": 1, "title": "安义县委常委、组织部部长",
     "start": "", "end": "", "rank": "副处级",
     "note": "丰城籍（宜春市跨设区市交流至南昌）"},

    # ── 吴威 (29) ──
    {"id": 75, "person_id": 29, "org_id": 4, "title": "安义县委常委、人武部部长",
     "start": "", "end": "", "rank": "副处级", "note": "军队系统"},

    # ── 叶飞 (30) ──
    {"id": 76, "person_id": 30, "org_id": 1, "title": "安义县委常委、常务副县长→县委副书记",
     "start": "2021-08", "end": "2024-11", "rank": "副处级",
     "note": "从青山湖区调入安义，后调任进贤"},
    {"id": 77, "person_id": 30, "org_id": 6, "title": "进贤县委副书记",
     "start": "2024-11", "end": "", "rank": "副处级", "note": "跨县调动：安义→进贤"},
]

# Relationships: person↔person
relationships = [
    # ── 2026年7月联动调整关系 ──
    {"id": 1, "person_a": 1, "person_b": 3, "type": "职务交替",
     "context": "熊辉接任安义县委书记时，罗国栋已调任青云谱区委书记。二人职务交替：安义县长→青云谱书记 vs 进贤县长→安义书记",
     "overlap_org": "中共安义县委员会/安义县人民政府",
     "overlap_period": "2026-07（交接期）"},
    {"id": 2, "person_a": 1, "person_b": 23, "type": "进贤→安义→进贤循环",
     "context": "熊辉从进贤县长调任安义县委书记，熊振强从安义县委常委出身→西湖区委→南昌市直→进贤县委书记。二人形成进贤↔安义循环流动",
     "overlap_org": "进贤县/安义县",
     "overlap_period": "2026-07"},
    {"id": 3, "person_a": 1, "person_b": 4, "type": "职务接替",
     "context": "熊辉接替谭伯乐出任安义县委书记",
     "overlap_org": "中共安义县委员会",
     "overlap_period": "2026-07（前后任）"},
    {"id": 4, "person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "熊辉（县委书记）与刘志伟（主持政府工作）搭班子",
     "overlap_org": "安义县",
     "overlap_period": "2026-07至今"},
    {"id": 5, "person_a": 3, "person_b": 4, "type": "职务接替",
     "context": "罗国栋接替谭伯乐任安义县长？实际上是谭伯乐升书记后罗国栋由南昌县委副书记调任安义县长",
     "overlap_org": "安义县人民政府",
     "overlap_period": "2021-08（前后任）"},

    # ── 谭伯乐的入安路径 ──
    {"id": 6, "person_a": 4, "person_b": 3, "type": "南昌县委→安义县长通道",
     "context": "谭伯乐和罗国栋均从南昌县委副书记职位调任安义县长。这是安义县长最重要的跨县输送管道",
     "overlap_org": "中共南昌县委员会→安义县",
     "overlap_period": "2020和2021"},

    # ── 安义→进贤的人员流动 ──
    {"id": 7, "person_a": 19, "person_b": 30, "type": "进贤→安义",
     "context": "杨武从进贤县白圩乡调入安义县任副县长；叶飞从安义调任进贤县委副书记。二人反向流动",
     "overlap_org": "进贤县↔安义县",
     "overlap_period": "2024"},
    {"id": 8, "person_a": 30, "person_b": 23, "type": "安义→进贤",
     "context": "叶飞（安义县委副书记→进贤县委副书记）和熊振强（安义县委常委→进贤县委书记）均从安义调至进贤",
     "overlap_org": "安义县→进贤县",
     "overlap_period": "2024-2026"},

    # ── 安义→其他区县 ──
    {"id": 9, "person_a": 21, "person_b": 23, "type": "安义→多县区",
     "context": "袁一旦从安义副县长起步，经进贤、西湖区、市交通局，至青山湖区委书记。熊振强从安义县委常委起步，经西湖区、市公路中心、市交通局，至进贤县委书记。二人路径高度相似",
     "overlap_org": "安义县→西湖区",
     "overlap_period": "2006-2026"},

    # ── 省直/市直下派 ──
    {"id": 10, "person_a": 3, "person_b": 14, "type": "南昌县交集",
     "context": "罗国栋任南昌县委副书记时，余超曾在南昌县黄马乡挂职。二人可能在南昌县有交集",
     "overlap_org": "南昌县",
     "overlap_period": "2020（可能短暂重叠）"},
    {"id": 11, "person_a": 14, "person_b": 13, "type": "都昌同乡",
     "context": "余超（都昌人）和谭翼直（都昌人）同为九江都昌籍干部在安义任职。这是重要的地缘关系线索",
     "overlap_org": "安义县",
     "overlap_period": "2023至今"},

    # ── 省委办公厅下派 ──
    {"id": 12, "person_a": 13, "person_b": 24, "type": "省级机关→安义",
     "context": "谭翼直从省委办公厅→南昌市委→安义县委常委，是近年安义班子中唯一有省委机关工作经历的成员",
     "overlap_org": "省委→市委→安义",
     "overlap_period": "2023"},
    {"id": 13, "person_a": 15, "person_b": 11, "type": "安义同事",
     "context": "金栋（纪委书记）和余建国（政法委书记）均在安义县乡镇基层起步，同属安义本土成长干部",
     "overlap_org": "安义县乡镇",
     "overlap_period": ""},

    # ── 跨市交流 ──
    {"id": 14, "person_a": 22, "person_b": 27, "type": "跨设区市交流",
     "context": "周荣卿（安义县委副书记→九江市浔阳区委书记）和郑绍（永修县长→靖安县委书记）均为跨设区市干部交流案例",
     "overlap_org": "南昌→九江/九江→宜春",
     "overlap_period": "2019-2021"},

    # ── 2026六县区书记调整 ──
    {"id": 15, "person_a": 24, "person_b": 25, "type": "2026联动调整",
     "context": "徐强（进贤书记→新建书记）接替陈奕蒙（新建书记→红谷滩书记），二人为2026年南昌六县区书记联动调整的相邻环节",
     "overlap_org": "新建区",
     "overlap_period": "2026-07"},
    {"id": 16, "person_a": 25, "person_b": 26, "type": "2026联动调整",
     "context": "陈奕蒙和杨育星同为2026年7月联动调整的区委书记",
     "overlap_org": "南昌市",
     "overlap_period": "2026-07"},

    # ── An县本地帮 ──
    {"id": 17, "person_a": 11, "person_b": 15, "type": "安义本地系",
     "context": "余建国（安义人，全部职业生涯在安义）和金栋（乐平人，但在安义乡镇基层成长）分别为安义本土派和融入派",
     "overlap_org": "安义县",
     "overlap_period": ""},

    # ── 彭开先的安义根基 ──
    {"id": 18, "person_a": 5, "person_b": 11, "type": "安义旧部",
     "context": "彭开先（安义副县长→县长→书记）与余建国（安义本地成长干部）在安义有长期共事关系",
     "overlap_org": "安义县人民政府",
     "overlap_period": "2016-2020"},

    # ── 熊振强的安义根基 ──
    {"id": 19, "person_a": 23, "person_b": 1, "type": "安义同事",
     "context": "熊振强（安义县委常委2016-2021）在安义工作期间，熊辉（2026年新任书记）彼时尚在青云谱区/进贤县。但熊振强是奉新人，熊辉也是奉新人——二人同乡",
     "overlap_org": "奉新县（同乡）",
     "overlap_period": "奉新籍贯关系"},
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
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(post):
    post_str = str(post)
    if "县委书记" in post_str or "区委书记" in post_str:
        return "255,50,50"  # Red for party secretary
    elif "县长" in post_str and ("副书记" not in post_str):
        return "50,100,255"  # Blue for county magistrate
    elif "常务副" in post_str:
        return "50,150,255"  # Light blue for executive deputy
    elif "副县长" in post_str:
        return "100,100,255"  # Lighter blue for deputy
    elif "纪委书记" in post_str or "监委" in post_str:
        return "255,165,0"  # Orange for discipline
    elif "组织部" in post_str:
        return "200,100,200"  # Purple for org dept
    elif "副书记" in post_str:
        return "200,100,50"  # Brown for deputy secretary
    else:
        return "100,100,100"  # Grey


def org_color(otype):
    m = {"党委": "255,200,200", "政府": "200,200,255", "开发区": "200,255,200",
         "乡镇": "255,255,200", "事业单位": "220,220,220", "政协": "255,240,200",
         "人大": "200,255,255"}
    return m.get(otype, "200,200,200")


lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>Claude Code Research Agent</creator>')
lines.append('    <description>江西省南昌市安义县跨县干部交流网络 — 2026年7月14日生成</description>')
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
    sz = "20.0" if ("书记" in p.get("current_post", "") and "副" not in p.get("current_post", "")) else "12.0"
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
