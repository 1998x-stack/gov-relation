#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 八公山区 (Bagongshan District, Huainan, Anhui) leadership network.
Generated: 2026-07-15
Task: anhui_八公山区 - 区委书记 & 区长
Sources: bagongshan.gov.cn 领导之窗 (official, accessed 2026-07-15)
"""

import sqlite3
import os
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
# If running from staging temp dir (data/tmp/anhui_八公山区/), go up to repo root
if "data/tmp" in BASE:
    BASE = os.path.dirname(os.path.dirname(os.path.dirname(BASE)))
STAGING = os.path.join(BASE, "data/tmp/anhui_八公山区")
DB_PATH = os.path.join(STAGING, "八公山区_network.db")
GEXF_PATH = os.path.join(STAGING, "八公山区_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Core Leaders ──
    {"id": 1, "name": "朱杰", "gender": "男", "ethnicity": "回族",
     "birth": "1973-12", "birthplace": "安徽长丰", "education": "省委党校研究生学历",
     "party_join": "1995-07", "work_start": "1993-11",
     "current_post": "八公山区委书记", "current_org": "中共八公山区委员会",
     "source": "http://www.bagongshan.gov.cn/zwgk/ldzc/"},
    {"id": 2, "name": "李旭", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-04", "birthplace": "安徽凤台", "education": "大学学历，公共管理硕士",
     "party_join": "1996-06", "work_start": "1996-08",
     "current_post": "八公山区委副书记、区长、区政府党组书记", "current_org": "八公山区人民政府",
     "source": "http://www.bagongshan.gov.cn/zwgk/ldzc/"},

    # ── 区委领导 ──
    {"id": 3, "name": "姚保斌", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "八公山区委副书记", "current_org": "中共八公山区委员会",
     "source": "http://www.bagongshan.gov.cn/zwgk/ldzc/"},
    {"id": 4, "name": "周辛", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "八公山区委常委、纪委书记、监委主任", "current_org": "中共八公山区纪律检查委员会",
     "source": "http://www.bagongshan.gov.cn/zwgk/ldzc/"},
    {"id": 5, "name": "陈进", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "八公山区委常委、政法委书记", "current_org": "中共八公山区委员会政法委员会",
     "source": "http://www.bagongshan.gov.cn/zwgk/ldzc/"},
    {"id": 6, "name": "葛广起", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "八公山区委常委、区政府常务副区长、党组副书记", "current_org": "八公山区人民政府",
     "source": "http://www.bagongshan.gov.cn/zwgk/ldzc/"},
    {"id": 7, "name": "许荻", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "八公山区委常委、宣传部部长", "current_org": "中共八公山区委员会宣传部",
     "source": "http://www.bagongshan.gov.cn/zwgk/ldzc/"},
    {"id": 8, "name": "夏国俊", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "八公山区委常委、人武部部长", "current_org": "八公山区人民武装部",
     "source": "http://www.bagongshan.gov.cn/zwgk/ldzc/"},
    {"id": 9, "name": "曹立慧", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "八公山区委常委、统战部部长", "current_org": "中共八公山区委员会统战部",
     "source": "http://www.bagongshan.gov.cn/zwgk/ldzc/"},
    {"id": 10, "name": "高云鹤", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "八公山区委常委、组织部部长", "current_org": "中共八公山区委员会组织部",
     "source": "http://www.bagongshan.gov.cn/zwgk/ldzc/"},

    # ── 人大领导 ──
    {"id": 11, "name": "杨斌", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "八公山区人大常委会党组书记、主任", "current_org": "八公山区人民代表大会常务委员会",
     "source": "http://www.bagongshan.gov.cn/zwgk/ldzc/"},
    {"id": 12, "name": "陈运煜", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "八公山区人大常委会副主任", "current_org": "八公山区人民代表大会常务委员会",
     "source": "http://www.bagongshan.gov.cn/zwgk/ldzc/"},
    {"id": 13, "name": "陈福建", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "八公山区人大常委会副主任", "current_org": "八公山区人民代表大会常务委员会",
     "source": "http://www.bagongshan.gov.cn/zwgk/ldzc/"},
    {"id": 14, "name": "韩露", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "八公山区人大常委会副主任、三级调研员", "current_org": "八公山区人民代表大会常务委员会",
     "source": "http://www.bagongshan.gov.cn/zwgk/ldzc/"},
    {"id": 15, "name": "刘志勇", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "八公山区人大常委会副主任", "current_org": "八公山区人民代表大会常务委员会",
     "source": "http://www.bagongshan.gov.cn/zwgk/ldzc/"},

    # ── 政府领导 (副区长) ──
    {"id": 16, "name": "管迎悦", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "八公山区政府副区长", "current_org": "八公山区人民政府",
     "source": "http://www.bagongshan.gov.cn/zwgk/ldzc/"},
    {"id": 17, "name": "马健", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "八公山区政府副区长", "current_org": "八公山区人民政府",
     "source": "http://www.bagongshan.gov.cn/zwgk/ldzc/"},
    {"id": 18, "name": "李茂", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "八公山区政府副区长、八公山公安分局局长、三级高级警长", "current_org": "八公山区人民政府",
     "source": "http://www.bagongshan.gov.cn/zwgk/ldzc/"},
    {"id": 19, "name": "孙大权", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "八公山区政府副区长", "current_org": "八公山区人民政府",
     "source": "http://www.bagongshan.gov.cn/zwgk/ldzc/"},

    # ── 政协领导 ──
    {"id": 20, "name": "余刚", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-03", "birthplace": "安徽定远", "education": "中央党校本科学历",
     "party_join": "1994-09", "work_start": "1989-06",
     "current_post": "八公山区政协党组书记、主席", "current_org": "政协八公山区委员会",
     "source": "http://www.bagongshan.gov.cn/zwgk/ldzc/"},
    {"id": 21, "name": "洪德萍", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "八公山区政协副主席、区工商联主席、二级调研员", "current_org": "政协八公山区委员会",
     "source": "http://www.bagongshan.gov.cn/zwgk/ldzc/"},
    {"id": 22, "name": "段传新", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "八公山区政协党组副书记、副主席、三级调研员", "current_org": "政协八公山区委员会",
     "source": "http://www.bagongshan.gov.cn/zwgk/ldzc/"},
    {"id": 23, "name": "彭华玉", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "八公山区政协副主席、区工会主席", "current_org": "政协八公山区委员会",
     "source": "http://www.bagongshan.gov.cn/zwgk/ldzc/"},
    {"id": 24, "name": "蔡升", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "八公山区政协副主席、区残联理事长、区工业集聚区服务中心主任", "current_org": "政协八公山区委员会",
     "source": "http://www.bagongshan.gov.cn/zwgk/ldzc/"},
    {"id": 25, "name": "贾莉", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "八公山区政协副主席", "current_org": "政协八公山区委员会",
     "source": "http://www.bagongshan.gov.cn/zwgk/ldzc/"},
]

organizations = [
    {"id": 1, "name": "中共八公山区委员会", "type": "党委", "level": "县处级", "parent": "中共淮南市委", "location": "安徽省淮南市八公山区"},
    {"id": 2, "name": "八公山区人民政府", "type": "政府", "level": "县处级", "parent": "淮南市人民政府", "location": "安徽省淮南市八公山区"},
    {"id": 3, "name": "八公山区人民武装部", "type": "政府", "level": "县处级", "parent": "淮南军分区", "location": "安徽省淮南市八公山区"},
    {"id": 4, "name": "中共八公山区纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共八公山区委员会", "location": "安徽省淮南市八公山区"},
    {"id": 5, "name": "中共八公山区委员会政法委员会", "type": "党委", "level": "乡科级", "parent": "中共八公山区委员会", "location": "安徽省淮南市八公山区"},
    {"id": 6, "name": "中共八公山区委员会宣传部", "type": "党委", "level": "乡科级", "parent": "中共八公山区委员会", "location": "安徽省淮南市八公山区"},
    {"id": 7, "name": "中共八公山区委员会统战部", "type": "党委", "level": "乡科级", "parent": "中共八公山区委员会", "location": "安徽省淮南市八公山区"},
    {"id": 8, "name": "中共八公山区委员会组织部", "type": "党委", "level": "乡科级", "parent": "中共八公山区委员会", "location": "安徽省淮南市八公山区"},
    {"id": 9, "name": "八公山区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "淮南市人大常委会", "location": "安徽省淮南市八公山区"},
    {"id": 10, "name": "八公山区政协委员会", "type": "政协", "level": "县处级", "parent": "政协淮南市委员会", "location": "安徽省淮南市八公山区"},
]

positions = [
    # 朱杰 - full career from official bio
    {"id": 1, "person_id": 1, "org_id": 1, "title": "八公山区委书记",
     "start": "", "end": "present", "rank": "正县级", "note": "现任"},
    {"id": 2, "person_id": 1, "org_id": 2, "title": "八公山区委副书记、区长、区政府党组书记",
     "start": "", "end": "", "rank": "正县级", "note": "前职，由区长升书记"},
    {"id": 3, "person_id": 1, "org_id": 1, "title": "八公山区委副书记",
     "start": "", "end": "", "rank": "副县级", "note": "前职"},
    {"id": 4, "person_id": 1, "org_id": 2, "title": "谢家集区委常委、常务副区长",
     "start": "", "end": "", "rank": "副县级", "note": "前职"},
    {"id": 5, "person_id": 1, "org_id": 2, "title": "谢家集区政府副区长",
     "start": "", "end": "", "rank": "副县级", "note": "前职"},
    {"id": 6, "person_id": 1, "org_id": 11, "title": "谢家集区孤堆回族乡党委副书记、乡长",
     "start": "", "end": "", "rank": "正科级", "note": "前职"},
    {"id": 7, "person_id": 1, "org_id": 12, "title": "长丰县孤堆回族乡党委委员、副乡长、武装部部长（副科）、党委副书记、乡长",
     "start": "", "end": "", "rank": "副科-正科", "note": "早年乡镇经历，孤堆回族乡最初属长丰县后划转谢家集区"},
    {"id": 8, "person_id": 1, "org_id": 13, "title": "长丰县义井乡办事员、计生专干、团委副书记、计生办副主任、主任",
     "start": "1993-11", "end": "", "rank": "办事员-正股级", "note": "早期基层工作"},

    # 李旭 - full career from official bio
    {"id": 10, "person_id": 2, "org_id": 2, "title": "八公山区委副书记、区长、区政府党组书记",
     "start": "", "end": "present", "rank": "正县级", "note": "现任"},
    {"id": 11, "person_id": 2, "org_id": 14, "title": "市投资促进局党组书记、局长",
     "start": "", "end": "", "rank": "正县级", "note": "前职，原市招商服务中心更名"},
    {"id": 12, "person_id": 2, "org_id": 15, "title": "市招商服务中心党组书记、主任",
     "start": "2022-01", "end": "", "rank": "正县级", "note": "前职"},
    {"id": 13, "person_id": 2, "org_id": 16, "title": "潘集区委常委、副区长（常务）、党组副书记、三级调研员",
     "start": "2018-08", "end": "2022-01", "rank": "副县级", "note": "常务副区长"},
    {"id": 14, "person_id": 2, "org_id": 16, "title": "潘集区政府副区长",
     "start": "2012-05", "end": "2018-08", "rank": "副县级", "note": ""},
    {"id": 15, "person_id": 2, "org_id": 16, "title": "潘集区政府副区长（挂职）、市人口计生委副调研员",
     "start": "2011-04", "end": "2012-05", "rank": "副县级", "note": "挂职副区长"},
    {"id": 16, "person_id": 2, "org_id": 17, "title": "市人口和计划生育委员会副调研员、发展规划科科长、计划统计科科长",
     "start": "2004-02", "end": "2011-04", "rank": "正科级", "note": "市计生委机关晋升"},
    {"id": 17, "person_id": 2, "org_id": 17, "title": "市计划生育委员会流动办副主任（副科）、计划统计科副科长",
     "start": "1996-08", "end": "2004-02", "rank": "副科级", "note": "1996年8月参加工作"},

    # 姚保斌
    {"id": 20, "person_id": 3, "org_id": 1, "title": "八公山区委副书记",
     "start": "", "end": "present", "rank": "副县级", "note": ""},

    # 周辛
    {"id": 21, "person_id": 4, "org_id": 4, "title": "八公山区委常委、纪委书记、监委主任",
     "start": "", "end": "present", "rank": "副县级", "note": ""},

    # 陈进
    {"id": 22, "person_id": 5, "org_id": 5, "title": "八公山区委常委、政法委书记",
     "start": "", "end": "present", "rank": "副县级", "note": ""},

    # 葛广起
    {"id": 23, "person_id": 6, "org_id": 2, "title": "八公山区委常委、常务副区长、党组副书记",
     "start": "", "end": "present", "rank": "副县级", "note": ""},

    # 许荻
    {"id": 24, "person_id": 7, "org_id": 6, "title": "八公山区委常委、宣传部部长",
     "start": "", "end": "present", "rank": "副县级", "note": ""},

    # 夏国俊
    {"id": 25, "person_id": 8, "org_id": 3, "title": "八公山区委常委、人武部部长",
     "start": "", "end": "present", "rank": "副县级", "note": ""},

    # 曹立慧
    {"id": 26, "person_id": 9, "org_id": 7, "title": "八公山区委常委、统战部部长",
     "start": "", "end": "present", "rank": "副县级", "note": ""},

    # 高云鹤
    {"id": 27, "person_id": 10, "org_id": 8, "title": "八公山区委常委、组织部部长",
     "start": "", "end": "present", "rank": "副县级", "note": ""},

    # 杨斌 - 人大
    {"id": 28, "person_id": 11, "org_id": 9, "title": "八公山区人大常委会党组书记、主任",
     "start": "", "end": "present", "rank": "正县级", "note": ""},
    {"id": 29, "person_id": 11, "org_id": 2, "title": "八公山区委常委、常务副区长",
     "start": "", "end": "", "rank": "副县级", "note": "前职"},
    {"id": 30, "person_id": 11, "org_id": 18, "title": "市城乡建设局党组副书记、副局长、三级调研员",
     "start": "", "end": "", "rank": "副县级", "note": "前职"},

    # 人大副主任
    {"id": 31, "person_id": 12, "org_id": 9, "title": "八公山区人大常委会副主任",
     "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"id": 32, "person_id": 13, "org_id": 9, "title": "八公山区人大常委会副主任",
     "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"id": 33, "person_id": 14, "org_id": 9, "title": "八公山区人大常委会副主任、三级调研员",
     "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"id": 34, "person_id": 15, "org_id": 9, "title": "八公山区人大常委会副主任",
     "start": "", "end": "present", "rank": "副县级", "note": ""},

    # 副区长
    {"id": 35, "person_id": 16, "org_id": 2, "title": "八公山区政府副区长",
     "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"id": 36, "person_id": 17, "org_id": 2, "title": "八公山区政府副区长",
     "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"id": 37, "person_id": 18, "org_id": 2, "title": "八公山区政府副区长、公安分局局长",
     "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"id": 38, "person_id": 19, "org_id": 2, "title": "八公山区政府副区长",
     "start": "", "end": "present", "rank": "副县级", "note": ""},

    # 余刚 - 政协
    {"id": 39, "person_id": 20, "org_id": 10, "title": "八公山区政协党组书记、主席",
     "start": "", "end": "present", "rank": "正县级", "note": ""},
    {"id": 40, "person_id": 20, "org_id": 1, "title": "谢家集区委副书记、三级调研员",
     "start": "", "end": "", "rank": "副县级", "note": "前职"},
    {"id": 41, "person_id": 20, "org_id": 1, "title": "谢家集区委常委、组织部长、宣传部长",
     "start": "", "end": "", "rank": "副县级", "note": "前职"},
    {"id": 42, "person_id": 20, "org_id": 19, "title": "市供销合作社党委委员、副主任",
     "start": "", "end": "", "rank": "副县级", "note": "前职"},
    {"id": 43, "person_id": 20, "org_id": 20, "title": "西藏山南地区行署副秘书长（援藏）",
     "start": "", "end": "", "rank": "副县级", "note": "援藏经历"},
    {"id": 44, "person_id": 20, "org_id": 21, "title": "市委办公室接待处副主任科员、副处长、市委办公室副主任",
     "start": "", "end": "", "rank": "副县级", "note": "市委办系统"},

    # 政协副主席
    {"id": 45, "person_id": 21, "org_id": 10, "title": "八公山区政协副主席、区工商联主席、二级调研员",
     "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"id": 46, "person_id": 22, "org_id": 10, "title": "八公山区政协党组副书记、副主席、三级调研员",
     "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"id": 47, "person_id": 23, "org_id": 10, "title": "八公山区政协副主席、区工会主席",
     "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"id": 48, "person_id": 24, "org_id": 10, "title": "八公山区政协副主席、区残联理事长、区工业集聚区服务中心主任",
     "start": "", "end": "present", "rank": "副县级", "note": ""},
    {"id": 49, "person_id": 25, "org_id": 10, "title": "八公山区政协副主席",
     "start": "", "end": "present", "rank": "副县级", "note": ""},
]

# Additional organizations referenced in career histories
extra_orgs = [
    {"id": 11, "name": "谢家集区孤堆回族乡", "type": "乡镇/街道", "level": "乡科级", "parent": "谢家集区", "location": "安徽省淮南市谢家集区"},
    {"id": 12, "name": "长丰县孤堆回族乡（已划归谢家集区）", "type": "乡镇/街道", "level": "乡科级", "parent": "", "location": "安徽省合肥市长丰县"},
    {"id": 13, "name": "长丰县义井乡", "type": "乡镇/街道", "level": "乡科级", "parent": "长丰县", "location": "安徽省合肥市长丰县"},
    {"id": 14, "name": "淮南市投资促进局", "type": "政府", "level": "县处级", "parent": "淮南市人民政府", "location": "安徽省淮南市"},
    {"id": 15, "name": "淮南市招商服务中心", "type": "事业单位", "level": "县处级", "parent": "淮南市人民政府", "location": "安徽省淮南市"},
    {"id": 16, "name": "潘集区人民政府/中共潘集区委员会", "type": "政府", "level": "县处级", "parent": "淮南市人民政府", "location": "安徽省淮南市潘集区"},
    {"id": 17, "name": "淮南市人口和计划生育委员会", "type": "政府", "level": "县处级", "parent": "淮南市人民政府", "location": "安徽省淮南市"},
    {"id": 18, "name": "淮南市城乡建设局", "type": "政府", "level": "县处级", "parent": "淮南市人民政府", "location": "安徽省淮南市"},
    {"id": 19, "name": "淮南市供销合作社", "type": "群团", "level": "县处级", "parent": "淮南市人民政府", "location": "安徽省淮南市"},
    {"id": 20, "name": "西藏山南地区行署", "type": "政府", "level": "地厅级", "parent": "西藏自治区人民政府", "location": "西藏自治区山南市"},
    {"id": 21, "name": "中共淮南市委办公室", "type": "党委", "level": "县处级", "parent": "中共淮南市委", "location": "安徽省淮南市"},
]
for org in extra_orgs:
    if org["id"] not in [o["id"] for o in organizations]:
        organizations.append(org)

relationships = [
    # 朱杰与李旭 - 党政主官
    {"id": 1, "person_a_id": 1, "person_b_id": 2, "type": "superior_subordinate",
     "context": "区委书记与区长党政主官关系", "overlap_org": "中共八公山区委员会/八公山区人民政府",
     "overlap_period": "至今（区长时与前任书记搭档，现为党政主官）"},

    # 朱杰与姚保斌
    {"id": 2, "person_a_id": 1, "person_b_id": 3, "type": "superior_subordinate",
     "context": "区委书记与区委副书记", "overlap_org": "中共八公山区委员会",
     "overlap_period": "至今"},

    # 朱杰与周辛
    {"id": 3, "person_a_id": 1, "person_b_id": 4, "type": "superior_subordinate",
     "context": "区委书记与纪委书记", "overlap_org": "中共八公山区委员会",
     "overlap_period": "至今"},

    # 朱杰与高云鹤
    {"id": 4, "person_a_id": 1, "person_b_id": 10, "type": "superior_subordinate",
     "context": "区委书记与组织部部长", "overlap_org": "中共八公山区委员会",
     "overlap_period": "至今"},

    # 李旭与葛广起 - 区长与常务副区长
    {"id": 5, "person_a_id": 2, "person_b_id": 6, "type": "superior_subordinate",
     "context": "区长与常务副区长", "overlap_org": "八公山区人民政府",
     "overlap_period": "至今"},

    # 朱杰与葛广起 - 区委书记与常务副区长
    {"id": 6, "person_a_id": 1, "person_b_id": 6, "type": "superior_subordinate",
     "context": "区委书记与常务副区长", "overlap_org": "中共八公山区委员会/八公山区人民政府",
     "overlap_period": "至今"},

    # 朱杰与杨斌 - 前任搭档（朱杰曾任区长，杨斌曾当常务副区长）
    {"id": 7, "person_a_id": 1, "person_b_id": 11, "type": "overlap",
     "context": "朱杰任八公山区长时，杨斌曾任八公山区常务副区长", "overlap_org": "八公山区人民政府",
     "overlap_period": "前些年"},

    # 朱杰与陈进
    {"id": 8, "person_a_id": 1, "person_b_id": 5, "type": "superior_subordinate",
     "context": "区委书记与政法委书记", "overlap_org": "中共八公山区委员会",
     "overlap_period": "至今"},

    # 朱杰与许荻
    {"id": 9, "person_a_id": 1, "person_b_id": 7, "type": "superior_subordinate",
     "context": "区委书记与宣传部部长", "overlap_org": "中共八公山区委员会",
     "overlap_period": "至今"},

    # 朱杰与曹立慧
    {"id": 10, "person_a_id": 1, "person_b_id": 9, "type": "superior_subordinate",
     "context": "区委书记与统战部部长", "overlap_org": "中共八公山区委员会",
     "overlap_period": "至今"},

    # 余刚与朱杰 - 余刚从谢家集区调来，朱杰曾在谢家集区任职
    {"id": 11, "person_a_id": 20, "person_b_id": 1, "type": "overlap",
     "context": "余刚曾任谢家集区委副书记等职，朱杰曾任谢家集区副区长、常务副区长，两人在谢家集区有重合", "overlap_org": "谢家集区",
     "overlap_period": "过去"},

    # 朱杰与陈福建（人大副主任）
    {"id": 12, "person_a_id": 1, "person_b_id": 13, "type": "overlap",
     "context": "区委书记与人大常委会副主任", "overlap_org": "八公山区",
     "overlap_period": "至今"},
]

# ── HELPERS ──────────────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    post = p["current_post"]
    if "书记" in post and "区委书记" in post:
        return "255,50,50"
    if "区长" in post and ("区委副书记" in post or "区长" in post):
        return "50,100,255"
    if "纪委书记" in post:
        return "255,165,0"
    if "人大" in post:
        return "200,100,100"
    if "政协" in post:
        return "100,100,200"
    return "100,100,100"

def org_color(o):
    t = o["type"]
    if t == "党委":
        return "255,200,200"
    if t == "政府":
        return "200,200,255"
    if t == "人大":
        return "200,255,255"
    if t == "政协":
        return "255,240,200"
    if t == "乡镇/街道":
        return "255,255,200"
    if t == "事业单位":
        return "220,220,220"
    if t == "群团":
        return "255,220,255"
    return "200,200,200"

def is_top_leader(p):
    return p["id"] in (1, 2)

# ── BUILD DB ─────────────────────────────────────────────────────────

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
    print(f"  Persons: {cur.execute('SELECT COUNT(*) FROM persons').fetchone()[0]}")
    print(f"  Organizations: {cur.execute('SELECT COUNT(*) FROM organizations').fetchone()[0]}")
    print(f"  Positions: {cur.execute('SELECT COUNT(*) FROM positions').fetchone()[0]}")
    print(f"  Relationships: {cur.execute('SELECT COUNT(*) FROM relationships').fetchone()[0]}")
    conn.close()


# ── BUILD GEXF ───────────────────────────────────────────────────────

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>八公山区（安徽省淮南市）领导关系网络 - 2026年7月</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="gender" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="level" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Nodes - Persons
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["gender"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
        lines.append(f'          <attvalue for="4" value="县处级"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes - Organizations
    for o in organizations:
        c = org_color(o)
        oid = o["id"] + 100
        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(o["level"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person -> Organization (worked_at)
    for pos in positions:
        eid += 1
        oid = pos["org_id"] + 100
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person <-> Person relationships
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a_id"]}" target="p{r["person_b_id"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF: {len(persons)} persons, {len(organizations)} orgs, {eid} edges")


# ── MAIN ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    os.makedirs(STAGING, exist_ok=True)
    print("Building 八公山区 (Bagongshan District, Huainan) network...")
    print(f"  DB path: {DB_PATH}")
    print(f"  GEXF path: {GEXF_PATH}")
    build_db()
    build_gexf()
    print("Done.")
