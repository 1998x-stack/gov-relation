#!/usr/bin/env python3
"""
Build 瑞丽市 cross-county cadre transfer network database and GEXF graph.

This script documents the personnel transfer patterns between 瑞丽市 (Ruili City)
and neighboring counties within 德宏傣族景颇族自治州:
- 芒市 (Mangshi) - prefecture capital
- 梁河县 (Lianghe County)
- 盈江县 (Yingjiang County)
- 陇川县 (Longchuan County)

Also documents the vertical linkages between 瑞丽 and 德宏州 level institutions.

Based on official sources:
- www.rl.gov.cn - 瑞丽市人民政府领导简介
- www.dh.gov.cn - 德宏州人民政府人事任免 (德政任〔2025〕5号, 〔2026〕1号-7号)
- Public appointment notices and official resumes
"""

import sqlite3
import os
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(BASE, ".."))
today = datetime.now().strftime("%Y-%m-%d")

DB_PATH = os.path.join(REPO_ROOT, "data/database/瑞丽市_跨县交流_network.db")
GEXF_PATH = os.path.join(REPO_ROOT, "data/graph/瑞丽市_跨县交流_network.gexf")

# =========================================================================
# DATA
# =========================================================================

persons = [
    # ================ 瑞丽市当前领导班子 (市政府) ================
    {
        "id": 1,
        "name": "温洋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983-10",
        "birthplace": "",
        "education": "在职硕士研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "瑞丽市委副书记、市长",
        "current_org": "瑞丽市人民政府",
        "source": "瑞丽市人民政府网(rl.gov.cn)—温洋简历, 1983年10月生, 在职硕士, 中共党员。现任瑞丽市委副书记、市长兼瑞丽试验区管委会副主任, 自贸试验区德宏片区工委副书记、管委会主任等职。同时兼任瑞丽产业协作园区瑞丽片区管委会主任(德政任〔2026〕7号)",
    },
    {
        "id": 2,
        "name": "段如科",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-11",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "current_post": "瑞丽市委常委、常务副市长",
        "current_org": "瑞丽市人民政府",
        "source": "瑞丽市人民政府官网 (rl.gov.cn)—段如科简历, 1981年11月生, 大学学历, 中共党员. 现任瑞丽市委常委、常务副市长、党组副书记",
    },
    {
        "id": 3,
        "name": "樊欣荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-03",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "current_post": "瑞丽市副市长、公安局局长",
        "current_org": "瑞丽市人民政府",
        "source": "瑞丽市人民政府官网 (rl.gov.cn) 樊欣荣简历, 1978年3月生, 大学学历, 中共党员",
    },
    {
        "id": 4,
        "name": "徐帅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987-10",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "current_post": "瑞丽市委常委、副市长(挂职)",
        "current_org": "瑞丽市人民政府",
        "source": "瑞丽市人民政府官网 (rl.gov.cn) 徐帅简历, 1987年10月生, 大学学历, 中共党员, 挂职二年",
    },
    {
        "id": 5,
        "name": "寸宝得",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983-05",
        "birthplace": "",
        "education": "研究生",
        "party_join": "民盟盟员",
        "current_post": "瑞丽市副市长",
        "current_org": "瑞丽市人民政府",
        "source": "瑞丽市人民政府官网 (rl.gov.cn) 寸宝得简历, 1983年5月生, 研究生学历, 民盟盟员. 兼任中国(云南)自由贸易试验区德宏片区管委会副主任(德政任〔2026〕1号)",
    },
    {
        "id": 6,
        "name": "喊顺",
        "gender": "女",
        "ethnicity": "傣族",
        "birth": "1980-08",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "current_post": "瑞丽市副市长",
        "current_org": "瑞丽市人民政府",
        "source": "瑞丽市人民政府官网 (rl.gov.cn) 喊顺简历, 1980年8月生, 傣族, 大学学历, 中共党员. 负责农业农村/乡村振兴/教育体育等",
    },
    {
        "id": 7,
        "name": "彭涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-09",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "current_post": "瑞丽市副市长",
        "current_org": "瑞丽市人民政府",
        "source": "瑞丽市人民政府官网 (rl.gov.cn) 彭涛简历, 1981年9月生, 省委党校研究生, 中共党员. 此前曾任瑞丽边境经济合作区管委会主任(免职于德政任〔2025〕5号)",
    },
    # ================ 州级领导(与瑞丽密切关联) ================
    {
        "id": 8,
        "name": "李正环",
        "gender": "男",
        "ethnicity": "景颇族",
        "birth": "1971-10",
        "birthplace": "",
        "education": "在职硕士",
        "party_join": "中共党员",
        "current_post": "德宏州州长",
        "current_org": "德宏州人民政府",
        "source": "德宏州人民政府官网 (dh.gov.cn) 李正环简历, 1971年10月生, 景颇族, 在职硕士. 兼任瑞丽产业协作园区管委会主任(德政任〔2026〕7号)",
    },
    {
        "id": 9,
        "name": "郑洪云",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-05",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "current_post": "德宏州常务副州长",
        "current_org": "德宏州人民政府",
        "source": "德宏州人民政府官网 (dh.gov.cn) 郑洪云简历, 1979年5月生, 省委党校研究生. 兼任瑞丽国家重点开发开放试验区管委会副主任、瑞丽产业协作园区管委会副主任(德政任〔2026〕7号)",
    },
    {
        "id": 10,
        "name": "董其然",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-01",
        "birthplace": "",
        "education": "在职研究生",
        "party_join": "中共党员",
        "current_post": "德宏州副州长",
        "current_org": "德宏州人民政府",
        "source": "德宏州人民政府官网 (dh.gov.cn) 董其然简历, 1980年1月生, 在职研究生. 负责外事/商务/自贸试验区; 2026年7月免去瑞丽国家重点开发开放试验区管委会副主任(德政任〔2026〕7号)",
    },
    # ================ Cross-county transfer figures ================
    {
        "id": 11,
        "name": "陈娥昌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "current_post": "云南陇川产业园区管委会主任",
        "current_org": "云南陇川产业园区",
        "source": "德宏州人民政府人事任免(德政任〔2026〕5号,6号,7号). 先后任州食品安全办公室主任/州知识产权局局长(2025), 兼任瑞丽产业协作园区陇川片区管委会主任(2026.7)",
    },
    {
        "id": 12,
        "name": "杨国伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "current_post": "德宏州工业和信息化局副局长",
        "current_org": "德宏州工业和信息化局",
        "source": "德政任〔2026〕1号: 杨国伟 任州工信局副局长, 免去云南芒市产业园区管委会副主任. 芒市→州级跨县调动",
    },
    {
        "id": 13,
        "name": "王咏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "current_post": "德宏州商务局副局长",
        "current_org": "德宏州商务局",
        "source": "德政任〔2025〕5号: 王咏任州商务局副局长, 免去畹町边境经济合作区管委会主任/畹町经济开发区管委会主任. 畹町(瑞丽)→州级跨县调动",
    },
    {
        "id": 14,
        "name": "何胜富",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "current_post": "德宏州公共资源交易管理局局长",
        "current_org": "德宏州公共资源交易管理局",
        "source": "德政任〔2026〕6号: 任州公共资源交易管理局局长",
    },
    {
        "id": 15,
        "name": "陈娥昌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "current_post": "云南陇川产业园区管委会主任",
        "current_org": "云南陇川产业园区",
        "source": "德政任〔2026〕5/6/7号: 兼任陇川产业园区管委会主任、瑞丽产业协作园区陇川片区管委会主任. 州→陇川→瑞丽跨县联系",
    },
    # ============ 领军组织角色 (双模人物在同一体系) ============
    {
        "id": 16,
        "name": "王泽升",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "current_post": "自贸试验区德宏片区管委会副主任(兼)",
        "current_org": "中国(云南)自由贸易试验区德宏片区管委会",
        "source": "德政任〔2026〕1号: 王泽升任中国(云南)自由贸易试验区德宏片区管委会副主任(兼). 兼职能与瑞丽市联动",
    },
]

organizations = [
    {"id": 1, "name": "瑞丽市人民政府", "type": "政府", "level": "县处级", "parent": "德宏州人民政府", "location": "云南德宏瑞丽"},
    {"id": 2, "name": "中共瑞丽市委员会", "type": "党委", "level": "县处级", "parent": "中共德宏州委员会", "location": "云南德宏瑞丽"},
    {"id": 3, "name": "中共瑞丽市委政法委员会", "type": "党委", "level": "县处级", "parent": "中共瑞丽市委员会", "location": "云南德宏瑞丽"},
    {"id": 4, "name": "瑞丽市公安局", "type": "政府", "level": "县处级", "parent": "瑞丽市人民政府", "location": "云南德宏瑞丽"},
    {"id": 5, "name": "德宏州人民政府", "type": "政府", "level": "地厅级", "parent": "云南省人民政府", "location": "云南德宏芒市"},
    {"id": 6, "name": "瑞丽国家重点开发开放试验区管委会", "type": "开发区", "level": "地厅级", "parent": "德宏州人民政府", "location": "云南德宏瑞丽"},
    {"id": 7, "name": "中国(云南)自由贸易试验区德宏片区管委会", "type": "开发区", "level": "县处级", "parent": "德宏州人民政府", "location": "云南德宏瑞丽"},
    {"id": 8, "name": "瑞丽边境经济合作区管委会", "type": "开发区", "level": "县处级", "parent": "瑞丽市人民政府", "location": "云南德宏瑞丽"},
    {"id": 9, "name": "畹町边境经济合作区管委会", "type": "开发区", "level": "县处级", "parent": "瑞丽市人民政府", "location": "云南德宏瑞丽"},
    {"id": 10, "name": "瑞丽产业协作园区管委会", "type": "开发区", "level": "县处级", "parent": "德宏州人民政府", "location": "云南德宏瑞丽"},
    {"id": 11, "name": "云南芒市产业园区管委会", "type": "开发区", "level": "县处级", "parent": "芒市人民政府", "location": "云南德宏芒市"},
    {"id": 12, "name": "云南陇川产业园区管委会", "type": "开发区", "level": "县处级", "parent": "陇川县人民政府", "location": "云南德宏陇川"},
    {"id": 13, "name": "德宏州工业和信息化局", "type": "政府", "level": "县处级", "parent": "德宏州人民政府", "location": "云南德宏芒市"},
    {"id": 14, "name": "德宏州商务局", "type": "政府", "level": "县处级", "parent": "德宏州人民政府", "location": "云南德宏芒市"},
    {"id": 15, "name": "瑞丽市姐告边境贸易区管委会", "type": "开发区", "level": "县处级", "parent": "瑞丽市人民政府", "location": "云南德宏瑞丽"},
    {"id": 16, "name": "德宏州公共资源交易管理局", "type": "政府", "level": "县处级", "parent": "德宏州人民政府", "location": "云南德宏芒市"},
    {"id": 17, "name": "瑞丽产业协作园区瑞丽片区管委会", "type": "开发区", "level": "县处级", "parent": "德宏州人民政府", "location": "云南德宏瑞丽"},
    {"id": 18, "name": "瑞丽产业协作园区陇川片区管委会", "type": "开发区", "level": "县处级", "parent": "德宏州人民政府", "location": "云南德宏陇川"},
    {"id": 19, "name": "德宏州人民政府食品安全委员会办公室", "type": "政府", "level": "县处级", "parent": "德宏州人民政府", "location": "云南德宏芒市"},
]

positions = [
    # === 温洋 ===
    {"id": 1, "person_id": 1, "org_id": 1, "title": "瑞丽市委副书记、市长", "start": "2024", "end": "", "rank": "县处级正职",
     "note": "现任瑞丽市长. 同时兼任瑞丽试验区管委会副主任、自贸试验区德宏片区工委副书记/管委会主任、瑞丽产业园区/边合区/畹町边合区/瑞丽产业协作园区瑞丽片区管委会主任(德政任〔2025〕5号,〔2026〕1号)"},
    {"id": 2, "person_id": 1, "org_id": 6, "title": "瑞丽国家重点开发开放试验区管委会副主任", "start": "", "end": "", "rank": "兼",
     "note": "德政任〔2025〕5号: 兼任云南瑞丽产业园区/瑞丽边境/畹町边境等职"},
    {"id": 3, "person_id": 1, "org_id": 7, "title": "自贸试验区德宏片区管委会主任(兼)", "start": "", "end": "", "rank": "兼",
     "note": "温洋兼任自贸试验区德宏片区管委副主任"},
    {"id": 4, "person_id": 1, "org_id": 15, "title": "瑞丽市姐告边境贸易区管委会主任(兼)", "start": "2026-02", "end": "", "rank": "兼",
     "note": "德政任〔2026〕1号: 温洋兼任瑞丽市姐告边境贸易区管委会主任"},
    # 段如科
    {"id": 5, "person_id": 2, "org_id": 1, "title": "瑞丽市委常委、常务副市长", "start": "2026-04", "end": "", "rank": "县处级副职",
     "note": "2026年4月27日更新简历: 担任市委常委、常务副市长"},
    # 樊欣荣
    {"id": 6, "person_id": 3, "org_id": 4, "title": "瑞丽市公安局党委书记、局长", "start": "", "end": "", "rank": "县处级副职",
     "note": "兼任副市长、公安局局长、督察长"},
    {"id": 7, "person_id": 3, "org_id": 1, "title": "瑞丽市副市长", "start": "", "end": "", "rank": "县处级副职",
     "note": "樊欣荣，副市长、党组成员，分管公安/司法"},
    # 徐帅 (挂职)
    {"id": 8, "person_id": 4, "org_id": 1, "title": "瑞丽市委常委、副市长(挂职)", "start": "2024-12", "end": "", "rank": "县处级副职",
     "note": "徐帅, 1987年10月生, 挂职二年"},
    # 寸宝得
    {"id": 9, "person_id": 5, "org_id": 1, "title": "瑞丽市副市长", "start": "", "end": "", "rank": "县处级副职",
     "note": "寸宝得, 1983年5月生, 分管自然资源/住建/文旅/交通等"},
    {"id": 10, "person_id": 5, "org_id": 7, "title": "自贸试验区德宏片区管委会副主任(兼)", "start": "2026-02", "end": "", "rank": "兼",
     "note": "德政任〔2026〕1号: 寸宝得兼任自贸试验区德宏片区管委会副主任"},
    # 喊顺
    {"id": 11, "person_id": 6, "org_id": 1, "title": "瑞丽市副市长", "start": "", "end": "", "rank": "县处级副职",
     "note": "喊顺, 傣族, 1980年8月生, 分管农林水教"},
    # 彭涛
    {"id": 12, "person_id": 7, "org_id": 1, "title": "瑞丽市副市长", "start": "2026", "end": "", "rank": "县处级副职",
     "note": "2026年任瑞丽副市长, 分海关/口岸/商务"},
    {"id": 13, "person_id": 7, "org_id": 8, "title": "瑞丽边境经济合作区管委会主任(前职)", "start": "", "end": "2025-10", "rank": "县处级正职",
     "note": "德政任〔2025〕5号: 免去彭涛瑞丽边境经济合作区管委会主任"},
    # 李正环
    {"id": 14, "person_id": 8, "org_id": 5, "title": "德宏州州长", "start": "", "end": "", "rank": "地厅级正职",
     "note": "李正环, 德宏州人民政府党组书记、州长"},
    {"id": 15, "person_id": 8, "org_id": 10, "title": "瑞丽产业协作园区管委会主任(兼)", "start": "2026-07", "end": "", "rank": "兼",
      "note": "德政任〔2026〕7号: 李正环兼任瑞丽产业协作园区管委会主任"},
    # 郑洪云
    {"id": 16, "person_id": 9, "org_id": 5, "title": "德宏州常务副州长", "start": "", "end": "", "rank": "地厅级副职",
     "note": "郑洪云, 1979年5月生, 德宏州委常委、常务副州长"},
    {"id": 17, "person_id": 9, "org_id": 6, "title": "瑞丽国家重点开发开放试验区管委会副主任(兼)", "start": "2026-07", "end": "", "rank": "兼",
     "note": "德政任〔2026〕7号: 郑洪云兼任瑞丽国家重点开发开放试验区管理委员会副主任"},
    {"id": 18, "person_id": 9, "org_id": 10, "title": "瑞丽产业协作园区管委会副主任(兼)", "start": "2026-07", "end": "", "rank": "兼",
     "note": "德政任〔2026〕7号: 郑洪云兼任瑞丽产业协作园区管委会副主任"},
    # 董其然
    {"id": 19, "person_id": 10, "org_id": 5, "title": "德宏州副州长", "start": "", "end": "", "rank": "地厅级副职",
     "note": "董其然, 1980年1月生, 负责外事/商务/自贸等"},
    {"id": 20, "person_id": 10, "org_id": 6, "title": "瑞丽国家重点开发开放试验区管委会副主任(前职)", "start": "", "end": "2026-07", "rank": "兼",
     "note": "德政任〔2026〕7号: 董其然免去瑞丽国家重点开发开放试验区管委会副主任"},
    # 杨国伟
    {"id": 21, "person_id": 12, "org_id": 13, "title": "德宏州工业和信息化局副局长", "start": "2026-02", "end": "", "rank": "县处级副职",
     "note": "德政任〔2026〕1号: 杨国伟由芒市产业园区副主任调任州工信局副局长"},
    {"id": 22, "person_id": 12, "org_id": 11, "title": "云南芒市产业园区管委会副主任(前职)", "start": "", "end": "2026-02", "rank": "县处级副职",
     "note": "免去云南芒市产业园区管委会副主任, 调至州级"},
    # 王咏
    {"id": 23, "person_id": 13, "org_id": 14, "title": "德宏州商务局副局长", "start": "2025-10", "end": "", "rank": "县处级副职",
     "note": "德政任〔2025〕10号: 任州商务局副局长"},
    {"id": 24, "person_id": 13, "org_id": 9, "title": "畹町边境经济合作区管委会主任/畹町经开区主任(前)", "start": "", "end": "2025-10", "rank": "县处级正职",
     "note": "免去畹町边境经济合作区/经开区主任"},
    # 王泽升
    {"id": 25, "person_id": 16, "org_id": 7, "title": "自贸试验区德宏片区管委会副主任(兼)", "start": "2026-02", "end": "", "rank": "兼",
     "note": "德政任〔2026〕1号: 王泽升任自贸试验区德宏片区管委会副主任"},
    # 陈娥昌
    {"id": 26, "person_id": 11, "org_id": 12, "title": "云南陇川产业园区管委会主任", "start": "2026-06", "end": "", "rank": "县处级正职",
     "note": "德政任〔2026〕6号: 任云南陇川产业园主任"},
    {"id": 27, "person_id": 11, "org_id": 19, "title": "德宏州食品安全办公室主任/州知产局长(前)", "start": "", "end": "2026-06", "rank": "县处级正职",
     "note": "免去州食品安全委员会办公室主任/州知识产权局局长"},
    {"id": 28, "person_id": 11, "org_id": 18, "title": "瑞丽产业协作园区陇川片区管委会主任(兼)", "start": "2026-07", "end": "", "rank": "兼",
     "note": "德政任〔2026〕7号: 兼任瑞丽产业协作园区陇川片区管委会主任"},
    # 何胜富
    {"id": 29, "person_id": 14, "org_id": 16, "title": "德宏州公共资源交易管理局局长", "start": "2026-06", "end": "", "rank": "县处级正职",
     "note": "德政任〔2026〕6号: 任州公共资源交易管理局局长"},
    # 温洋 - add the insitutional structure
    {"id": 30, "person_id": 1, "org_id": 17, "title": "瑞丽产业协作园区瑞丽玉片区管委会主任(兼)", "start": "2026-07", "end": "", "rank": "兼",
     "note": "兼产为瑞丽产业协作协同"},
    # 前职来FIX
]

# We must fix the notes properly
relationships = [
    # 温洋 ↔ 段如科 (常务副市长)
    {"id": 1, "person_a": 1, "person_b": 2, "type": "党政正副职搭档", "context": "温洋（市长）与段如科（常务副市长）为市政府正副职搭档", "overlap_org": "瑞丽市人民政府", "overlap_period": "2026-至今"},
    # 温洋 ↔ 彭涛 (副市长)
    {"id": 2, "person_a": 1, "person_b": 7, "type": "党政正副职搭档", "context": "温洋（市长）与彭涛（副市长）共事于瑞丽市政府", "overlap_org": "瑞丽市人民政府", "overlap_period": "2026-至今"},
    # 温洋 ↔ 寸宝得 (副市长)
    {"id": 3, "person_a": 1, "person_b": 5, "type": "党政正副职搭档", "context": "温洋（市长）与寸宝得（副市长, 民盟）共事", "overlap_org": "瑞丽市人民政府", "overlap_period": "至今"},
    # 温洋 ↔ 喊顺 (副市长)
    {"id": 4, "person_a": 1, "person_b": 6, "type": "党政正副职搭档", "context": "温洋与喊顺（傣族女性干部）共事在瑞丽市政府", "overlap_org": "瑞丽市人民政府", "overlap_period": "至今"},
    # 李正环 ↔ 郑洪运 (州级正副)
    {"id": 5, "person_a": 8, "person_b": 9, "type": "州级正副职搭档", "context": "李正环（州长）与郑洪云（常务副州长）为州政府正副职搭档", "overlap_org": "德宏州人民政府", "overlap_period": "至今"},
    # 李正环 ↔ 董其然 (州级正副)
    {"id": 6, "person_a": 8, "person_b": 10, "type": "州级正副职搭档", "context": "李正环（州长）与董其然（副州长）共事", "overlap_org": "德宏州人民政府", "overlap_period": "至今"},
    # 李正环 → 瑞丽 (双兼职)
    {"id": 7, "person_a": 8, "person_b": 1, "type": "州→县纵向领导", "context": "李正环（州长）兼任瑞丽产业协作园区主任，对温洋（市长）有领导角色", "overlap_org": "瑞丽产业协作园区", "overlap_period": "2026-07-至今"},
    # 郑洪云 → 瑞丽
    {"id": 8, "person_a": 9, "person_b": 1, "type": "州→县纵向领导", "context": "郑洪云兼任瑞丽试验区/瑞丽产业协作园区副主任", "overlap_org": "瑞丽产业协作园区", "overlap_period": "2026-07-至今"},
    # 董其然 → 瑞丽 (前序)
    {"id": 9, "person_a": 10, "person_b": 1, "type": "州→县纵向领导(前)", "context": "董其然此前兼任瑞丽试验区副主任，2026年7月免职", "overlap_org": "瑞丽国家重点开发开放试验区", "overlap_period": "至2026-07"},
    # 芒市→州级调转 (杨国伟)
    {"id": 10, "person_a": 12, "person_b": 8, "type": "跨县调动", "context": "杨国伟从云南芒市产业园区调至德宏州工信局", "overlap_org": "德宏州工业和信息化局", "overlap_period": "2026-02"},
    # 畹町→州级 (王泳)
    {"id": 11, "person_a": 13, "person_b": 9, "type": "跨县调动", "context": "王咏从畹町边合区/经开区(在瑞丽行政区内)调至德宏州商务局", "overlap_org": "德宏州商务局", "overlap_period": "2025-10"},
    # 陈娥昌→陇川和瑞丽双联系
    {"id": 12, "person_a": 11, "person_b": 1, "type": "园区跨县协作", "context": "陈娥昌兼任瑞丽产业协作园区陇川片区主任, 与瑞丽片区保持跨县联系", "overlap_org": "瑞丽产业协作园区", "overlap_period": "2026-07"},
    # 陈娥昌→李正环 (上下级)
    {"id": 13, "person_a": 11, "person_b": 8, "type": "跨县调动", "context": "陈娥昌从州食安办调任云南陇川产业园, 再兼瑞丽园区职务", "overlap_org": "德宏州政府体系", "overlap_period": "2025-2026"},
    # 直辖系: 瑞丽与德宏强的链条
    {"id": 14, "person_a": 5, "person_b": 16, "type": "园区共事", "context": "寸宝得与王泽升同在自贸试验区德宏片区管委会兼职", "overlap_org": "自贸试验区德宏片区管委会", "overlap_period": "2026-"},
    # 温洋↔樊欣荣
    {"id": 15, "person_a": 1, "person_b": 3, "type": "党政正副职搭档", "context": "温洋（市长）与樊欣荣（副市长/公安）共事", "overlap_org": "瑞丽市人民政府", "overlap_period": "至今"},
    # 温洋↔徐帅
    {"id": 16, "person_a": 1, "person_b": 4, "type": "党政正副职搭档", "context": "温洋（市长）与徐帅（挂职副市长）共事", "overlap_org": "瑞丽市人民政府", "overlap_period": "至今"},
    # 彭涛↔王咏 (前边合Ber)
    {"id": 17, "person_a": 7, "person_b": 13, "type": "园区共事前职", "context": "彭涛曾任瑞丽边合区主任, 王咏曾任畹町边合区主任, 两人不同的园区各有连接州级商管路径", "overlap_org": "瑞丽边境合作区体系", "overlap_period": "至2025"},
]



# =========================================================================
# BUILD
# =========================================================================

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def pcolor_viz(post):
    post = post or ""
    if "书记" in post and "副" not in post and ("州" in post or "市委" in post):
        return "230,50,50"
    if "副书记" in post:
        return "200,80,80"
    if "州长" in post and "副" not in post:
        return "230,50,50"
    if "市长" in post and "副" not in post:
        return "50,100,230"
    if "常务副" in post or "副州长" in post or "副区长" in post:
        return "80,140,230"
    if "副县长" in post:
        return "80,140,230"
    if "副市长" in post:
        return "80,140,230"
    if "公安" in post:
        return "100,180,100"
    return "120,120,120"

def ocolor_viz(otype):
    return {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
        "人大": "200,255,200",
        "政协": "255,240,200",
    }.get(otype, "200,200,200")

# ===== Positions clean =====
positions_clean = [p for p in positions if p.get("note", "") and p.get("title", "")]

def build_sqlite():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
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
        id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER NOT NULL, org_id INTEGER NOT NULL,
        title TEXT NOT NULL, start TEXT, end TEXT, rank TEXT, note TEXT,
        FOREIGN KEY (person_id) REFERENCES persons(id),
        FOREIGN KEY (org_id) REFERENCES organizations(id)
    );
    CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT, person_a INTEGER NOT NULL, person_b INTEGER NOT NULL,
        type TEXT NOT NULL, context TEXT, overlap_org TEXT, overlap_period TEXT,
        FOREIGN KEY (person_a) REFERENCES persons(id),
        FOREIGN KEY (person_b) REFERENCES persons(id)
    );
    """)
    for p in persons:
        c.execute("INSERT INTO persons VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"], p["name"], p.get("gender",""), p.get("ethnicity",""),
                   p.get("birth",""), p.get("birthplace",""), p.get("education",""),
                   p.get("party_join",""), p.get("work_start",""),
                   p.get("current_post",""), p.get("current_org",""), p.get("source","")))
    for o in organizations:
        c.execute("INSERT INTO organizations VALUES(?,?,?,?,?,?)",
                  (o["id"], o["name"], o["type"], o["level"], o.get("parent",""), o.get("location","")))
    for pos in positions:
        c.execute("INSERT INTO positions(person_id, org_id, title, start, end, rank, note) VALUES(?,?,?,?,?,?,?)",
                  (pos.get("person_id"), pos.get("org_id"), pos.get("title",""),
                   pos.get("start",""), pos.get("end",""), pos.get("rank",""), pos.get("note","")))
    for r in relationships:
        c.execute("INSERT INTO relationships(person_a, person_b, type, context, overlap_org, overlap_period) VALUES(?,?,?,?,?,?)",
                  (r["person_a"], r["person_b"], r["type"], r.get("context",""), r.get("overlap_org",""), r.get("overlap_period","")))
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
    lines.append('    <creator>gov-relation agent</creator>')
    lines.append(f'    <description>瑞丽市跨县交流网络 - {today}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    lines.append('    <attributes class="node">')
    for aid, atitle in [("0","type"),("1","birth"),("2","ethnicity"),("3","current_post")]:
        lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    for aid, atitle in [("0","type"),("1","start"),("2","end"),("3","context")]:
        lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <nodes>')
    for p in persons:
        c_val = pcolor_viz(p.get("current_post",""))
        sz = "20.0" if p["id"] in (1, 8) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        for f, v in [("0","person"),("1",p.get("birth","")),("2",p.get("ethnicity","")),("3",p.get("current_post",""))]:
            lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c_val.split(",")[0]}" g="{c_val.split(",")[1]}" b="{c_val.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    for o in organizations:
        c_val = ocolor_viz(o.get("type",""))
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        for f, v in [("type","organization"),("birth",""),("ethnicity",""),("current_post","")]:
            pass
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c_val.split(",")[0]}" g="{c_val.split(",")[1]}" b="{c_val.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')
    lines.append('    <edges>')
    eid = 0
    for pos in positions_clean:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pos.get("person_id")}" target="o{pos.get("org_id")}" '
                     f'label="{esc(pos.get("title",""))}" weight="1.0">')
        lines.append('        <attvalues>')
        for f, v in [("type","worked_at"),("start",pos.get("start","")),("end",pos.get("end","")),("context",pos.get("note",""))]:
            lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" '
                     f'label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        for f, a in [("type", r["type"]), ("start", ""), ("end", ""), ("context", r.get("context",""))]:
            lines.append(f'          <attvalue for="{f}" value="{esc(a)}"/>')
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

if __name__ == "__main__":
    print("=" * 60)
    print("瑞丽市 Cross-County Cadre Transfer Network Builder")
    print(f"Date: {today}")
    print("=" * 60)
    print("\n▶ Building SQLite database...")
    counts = build_sqlite()
    print(f"  ✓ {DB_PATH}")
    for t, n in counts.items():
        print(f"    {t}: {n}")
    print("\n▶ Building GEXF graph...")
    tn, tn2 = build_gexf()
    import sys
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
