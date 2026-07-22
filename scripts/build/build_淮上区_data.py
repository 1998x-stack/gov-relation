#!/usr/bin/env python3
"""Build 淮上区 (Huaishang District, Bengbu City) leadership network: SQLite DB + GEXF graph.

Research date: 2026-07-15
Sources:
  - www.huaishang.gov.cn/zjhs/ldzchuang/index.html (official leadership page, accessed 2026-07-15)
  - www.huaishang.gov.cn/lddt/5094363.html (5th Party Congress opening, 2026-06-26)
  - www.huaishang.gov.cn/lddt/5094426.html (5th Party Committee 1st Plenary, 2026-06-29)
  - www.huaishang.gov.cn/lddt/5094429.html (5th Discipline Commission 1st Plenary, 2026-06-29)
  - www.huaishang.gov.cn/lddt/5093607.html (史法勇 inspects safety/environment, 2026-06-03)
  - www.huaishang.gov.cn/lddt/5093976.html (Investment promotion meeting, 2026-06-12)
  - www.huaishang.gov.cn/lddt/5093601.html (龙晓娣 chairs training meeting, 2026-06-05)
  - www.huaishang.gov.cn/lddt/5094240.html (Party committee study meeting, 2026-06-23)

Confidence: Current roles confirmed from official Huaishang district government website;
  biographical details are from official profiles (birth year, education) but full career
  histories are limited for some figures.
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
DB_PATH = os.path.join(SCRIPT_DIR, "淮上区_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "淮上区_network.gexf")

# ── research data ────────────────────────────────────────────────────────

persons = [
    # ── Party Committee ──
    {
        "id": 1,
        "name": "史法勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年10月",
        "birthplace": "",
        "education": "中央党校大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共蚌埠市淮上区委员会",
        "source": "https://www.huaishang.gov.cn/zjhs/ldzchuang/index.html",
        "notes": "1976年10月生，中央党校大学学历。2026年6月26日淮上区第五次党代会连任区委书记。",
        "confidence": "confirmed"
    },
    {
        "id": 2,
        "name": "龙晓娣",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1979年10月",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、区长",
        "current_org": "蚌埠市淮上区人民政府",
        "source": "https://www.huaishang.gov.cn/zjhs/ldzchuang/index.html",
        "notes": "1979年10月生，省委党校研究生学历。主持区政府全面工作。",
        "confidence": "confirmed"
    },
    {
        "id": 3,
        "name": "刘冰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年5月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记",
        "current_org": "中共蚌埠市淮上区委员会",
        "source": "https://www.huaishang.gov.cn/zjhs/ldzchuang/index.html",
        "notes": "1978年5月生，大学学历。协助区委书记抓党的建设工作，负责农业农村、群团工作。",
        "confidence": "confirmed"
    },
    {
        "id": 4,
        "name": "王雪",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、宣传部部长",
        "current_org": "中共蚌埠市淮上区委员会",
        "source": "https://www.huaishang.gov.cn/zjhs/ldzchuang/index.html",
        "notes": "履历细节待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 5,
        "name": "刘锐",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987年8月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "蚌埠市淮上区人民政府",
        "source": "https://www.huaishang.gov.cn/zjhs/ldzchuang/index.html",
        "notes": "1987年8月生，大学学历。负责区政府常务工作。",
        "confidence": "confirmed"
    },
    {
        "id": 6,
        "name": "邵于洋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "蚌埠市淮上区人民政府",
        "source": "https://www.huaishang.gov.cn/zjhs/ldzchuang/index.html",
        "notes": "履历细节待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 7,
        "name": "黄冬生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年7月",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、纪委书记、监委主任",
        "current_org": "中共蚌埠市淮上区纪律检查委员会",
        "source": "https://www.huaishang.gov.cn/zjhs/ldzchuang/index.html",
        "notes": "1981年7月生，省委党校研究生学历。负责纪检监察和区委巡察工作。",
        "confidence": "confirmed"
    },
    {
        "id": 8,
        "name": "茹卫东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区人武部部长",
        "current_org": "淮上区人民武装部",
        "source": "https://www.huaishang.gov.cn/zjhs/ldzchuang/index.html",
        "notes": "履历细节待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 9,
        "name": "葛素强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、组织部部长、统战部部长、党校校长",
        "current_org": "中共蚌埠市淮上区委员会",
        "source": "https://www.huaishang.gov.cn/zjhs/ldzchuang/index.html",
        "notes": "履历细节待补充。",
        "confidence": "confirmed"
    },
    {
        "id": 10,
        "name": "郑兴方",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、沫河口镇党委书记",
        "current_org": "中共沫河口镇委员会",
        "source": "https://www.huaishang.gov.cn/zjhs/ldzchuang/index.html",
        "notes": "淮上区沫河口镇党委书记，同时任区委常委。",
        "confidence": "confirmed"
    },
    {
        "id": 11,
        "name": "刘国强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、政法委书记",
        "current_org": "中共蚌埠市淮上区委员会",
        "source": "https://www.huaishang.gov.cn/zjhs/ldzchuang/index.html",
        "notes": "履历细节待补充。",
        "confidence": "confirmed"
    },
    # ── District Government (additional, not already listed as party committee) ──
    {
        "id": 12,
        "name": "刘言广",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长、区公安分局局长",
        "current_org": "蚌埠市淮上区人民政府",
        "source": "https://www.huaishang.gov.cn/zjhs/ldzchuang/index.html",
        "notes": "区政府党组成员、副区长，区公安分局党委书记、局长。",
        "confidence": "confirmed"
    },
    {
        "id": 13,
        "name": "巴桑卓嘎",
        "gender": "女",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长（挂职）",
        "current_org": "蚌埠市淮上区人民政府",
        "source": "https://www.huaishang.gov.cn/zjhs/ldzchuang/index.html",
        "notes": "挂职时间一年。西藏交流干部。",
        "confidence": "confirmed"
    },
    {
        "id": 14,
        "name": "牛毅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "蚌埠市淮上区人民政府",
        "source": "https://www.huaishang.gov.cn/zjhs/ldzchuang/index.html",
        "notes": "区政府党组成员、副区长。",
        "confidence": "confirmed"
    },
    {
        "id": 15,
        "name": "汤瑞瑞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "蚌埠市淮上区人民政府",
        "source": "https://www.huaishang.gov.cn/zjhs/ldzchuang/index.html",
        "notes": "区政府党组成员、副区长。",
        "confidence": "confirmed"
    },
    {
        "id": 16,
        "name": "苏凌寒",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "蚌埠市淮上区人民政府",
        "source": "https://www.huaishang.gov.cn/zjhs/ldzchuang/index.html",
        "notes": "区政府副区长。",
        "confidence": "confirmed"
    },
]

organizations = [
    {"id": 1, "name": "中共蚌埠市淮上区委员会", "type": "党委", "level": "县级", "parent": "中共蚌埠市委", "location": "蚌埠市淮上区"},
    {"id": 2, "name": "蚌埠市淮上区人民政府", "type": "政府", "level": "县级", "parent": "蚌埠市人民政府", "location": "蚌埠市淮上区"},
    {"id": 3, "name": "中共蚌埠市淮上区纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共蚌埠市淮上区委员会", "location": "蚌埠市淮上区"},
    {"id": 4, "name": "淮上区人民武装部", "type": "事业单位", "level": "县级", "parent": "蚌埠军分区", "location": "蚌埠市淮上区"},
    {"id": 5, "name": "中共沫河口镇委员会", "type": "党委", "level": "乡镇级", "parent": "中共蚌埠市淮上区委员会", "location": "蚌埠市淮上区沫河口镇"},
    {"id": 6, "name": "蚌埠市淮上区人大常委会", "type": "人大", "level": "县级", "parent": "蚌埠市淮上区", "location": "蚌埠市淮上区"},
    {"id": 7, "name": "政协蚌埠市淮上区委员会", "type": "政协", "level": "县级", "parent": "蚌埠市淮上区", "location": "蚌埠市淮上区"},
]

positions = [
    # 史法勇
    {"id": 1, "person_id": 1, "org_id": 1, "title": "淮上区委书记", "start": "", "end": "present", "rank": "正处", "note": "2026年6月26日淮上区第五次党代会连任区委书记"},
    # 龙晓娣
    {"id": 2, "person_id": 2, "org_id": 2, "title": "淮上区区长", "start": "", "end": "present", "rank": "正处", "note": "区委副书记、区政府党组书记、区长，主持区政府全面工作"},
    {"id": 3, "person_id": 2, "org_id": 1, "title": "淮上区委副书记", "start": "", "end": "present", "rank": "正处", "note": "区委副书记"},
    # 刘冰
    {"id": 4, "person_id": 3, "org_id": 1, "title": "淮上区委副书记", "start": "", "end": "present", "rank": "副处（正处级）", "note": "协助书记抓党建，分管农业农村、群团"},
    # 王雪
    {"id": 5, "person_id": 4, "org_id": 1, "title": "淮上区委常委、宣传部部长", "start": "", "end": "present", "rank": "副处", "note": ""},
    # 刘锐
    {"id": 6, "person_id": 5, "org_id": 2, "title": "淮上区委常委、常务副区长", "start": "", "end": "present", "rank": "副处", "note": "区政府党组副书记"},
    {"id": 7, "person_id": 5, "org_id": 1, "title": "淮上区委常委", "start": "", "end": "present", "rank": "副处", "note": ""},
    # 邵于洋
    {"id": 8, "person_id": 6, "org_id": 2, "title": "淮上区委常委、副区长", "start": "", "end": "present", "rank": "副处", "note": "区政府党组成员"},
    {"id": 9, "person_id": 6, "org_id": 1, "title": "淮上区委常委", "start": "", "end": "present", "rank": "副处", "note": ""},
    # 黄冬生
    {"id": 10, "person_id": 7, "org_id": 3, "title": "淮上区委常委、纪委书记、监委主任", "start": "", "end": "present", "rank": "副处", "note": "2026年6月29日五届区纪委第一次全体会议选举产生"},
    {"id": 11, "person_id": 7, "org_id": 1, "title": "淮上区委常委", "start": "", "end": "present", "rank": "副处", "note": ""},
    # 茹卫东
    {"id": 12, "person_id": 8, "org_id": 4, "title": "淮上区人武部部长", "start": "", "end": "present", "rank": "正团", "note": "区委常委"},
    {"id": 13, "person_id": 8, "org_id": 1, "title": "淮上区委常委", "start": "", "end": "present", "rank": "副处", "note": ""},
    # 葛素强
    {"id": 14, "person_id": 9, "org_id": 1, "title": "淮上区委常委、组织部部长、统战部部长、党校校长", "start": "", "end": "present", "rank": "副处", "note": ""},
    # 郑兴方
    {"id": 15, "person_id": 10, "org_id": 5, "title": "沫河口镇党委书记", "start": "", "end": "present", "rank": "正科", "note": "区委常委兼任"},
    {"id": 16, "person_id": 10, "org_id": 1, "title": "淮上区委常委", "start": "", "end": "present", "rank": "副处", "note": ""},
    # 刘国强
    {"id": 17, "person_id": 11, "org_id": 1, "title": "淮上区委常委、政法委书记", "start": "", "end": "present", "rank": "副处", "note": ""},
    # 刘言广
    {"id": 18, "person_id": 12, "org_id": 2, "title": "淮上区副区长、区公安分局局长", "start": "", "end": "present", "rank": "副处", "note": "区政府党组成员"},
    # 巴桑卓嘎
    {"id": 19, "person_id": 13, "org_id": 2, "title": "淮上区副区长（挂职）", "start": "", "end": "present", "rank": "副处", "note": "挂职时间一年"},
    # 牛毅
    {"id": 20, "person_id": 14, "org_id": 2, "title": "淮上区副区长", "start": "", "end": "present", "rank": "副处", "note": "区政府党组成员"},
    # 汤瑞瑞
    {"id": 21, "person_id": 15, "org_id": 2, "title": "淮上区副区长", "start": "", "end": "present", "rank": "副处", "note": "区政府党组成员"},
    # 苏凌寒
    {"id": 22, "person_id": 16, "org_id": 2, "title": "淮上区副区长", "start": "", "end": "present", "rank": "副处", "note": ""},
]

relationships = [
    # 党政搭档
    {"id": 1, "person_a": 1, "person_b": 2, "type": "overlap", "context": "史法勇（区委书记）与龙晓娣（区长）为淮上区党政一把手搭档", "overlap_org": "淮上区", "overlap_period": "2026"},
    # 副书记与书记
    {"id": 2, "person_a": 3, "person_b": 1, "type": "superior_subordinate", "context": "刘冰（区委副书记）协助史法勇（区委书记）抓党的建设工作", "overlap_org": "淮上区委", "overlap_period": "2026"},
    # 常务副区长与区长
    {"id": 3, "person_a": 5, "person_b": 2, "type": "superior_subordinate", "context": "刘锐（常务副区长）协助龙晓娣（区长）分管区审计局", "overlap_org": "淮上区政府", "overlap_period": "2026"},
    # 区委常委内部关系（同届领导班子）
    {"id": 4, "person_a": 1, "person_b": 3, "type": "overlap", "context": "史法勇与刘冰同为淮上区第五届区委领导班子成员", "overlap_org": "淮上区委", "overlap_period": "2026-"},
    {"id": 5, "person_a": 1, "person_b": 4, "type": "overlap", "context": "史法勇与王雪同为淮上区第五届区委领导班子成员", "overlap_org": "淮上区委", "overlap_period": "2026-"},
    {"id": 6, "person_a": 1, "person_b": 5, "type": "overlap", "context": "史法勇与刘锐同为淮上区第五届区委领导班子成员", "overlap_org": "淮上区委", "overlap_period": "2026-"},
    {"id": 7, "person_a": 1, "person_b": 6, "type": "overlap", "context": "史法勇与邵于洋同为淮上区第五届区委领导班子成员", "overlap_org": "淮上区委", "overlap_period": "2026-"},
    {"id": 8, "person_a": 1, "person_b": 7, "type": "overlap", "context": "史法勇与黄冬生同为淮上区第五届区委领导班子成员", "overlap_org": "淮上区委", "overlap_period": "2026-"},
    {"id": 9, "person_a": 1, "person_b": 8, "type": "overlap", "context": "史法勇与茹卫东同为淮上区第五届区委领导班子成员", "overlap_org": "淮上区委", "overlap_period": "2026-"},
    {"id": 10, "person_a": 1, "person_b": 9, "type": "overlap", "context": "史法勇与葛素强同为淮上区第五届区委领导班子成员", "overlap_org": "淮上区委", "overlap_period": "2026-"},
    {"id": 11, "person_a": 1, "person_b": 10, "type": "overlap", "context": "史法勇与郑兴方同为淮上区第五届区委领导班子成员", "overlap_org": "淮上区委", "overlap_period": "2026-"},
    {"id": 12, "person_a": 1, "person_b": 11, "type": "overlap", "context": "史法勇与刘国强同为淮上区第五届区委领导班子成员", "overlap_org": "淮上区委", "overlap_period": "2026-"},
    # 区长与副区长
    {"id": 13, "person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "龙晓娣（区长）与刘言广（副区长、公安分局局长）为区政府领导班子成员", "overlap_org": "淮上区政府", "overlap_period": "2026"},
    {"id": 14, "person_a": 2, "person_b": 13, "type": "superior_subordinate", "context": "龙晓娣（区长）与巴桑卓嘎（挂职副区长）为区政府领导班子成员", "overlap_org": "淮上区政府", "overlap_period": "2026"},
    {"id": 15, "person_a": 2, "person_b": 14, "type": "superior_subordinate", "context": "龙晓娣（区长）与牛毅（副区长）为区政府领导班子成员", "overlap_org": "淮上区政府", "overlap_period": "2026"},
    {"id": 16, "person_a": 2, "person_b": 15, "type": "superior_subordinate", "context": "龙晓娣（区长）与汤瑞瑞（副区长）为区政府领导班子成员", "overlap_org": "淮上区政府", "overlap_period": "2026"},
    {"id": 17, "person_a": 2, "person_b": 16, "type": "superior_subordinate", "context": "龙晓娣（区长）与苏凌寒（副区长）为区政府领导班子成员", "overlap_org": "淮上区政府", "overlap_period": "2026"},
    # 纪委与区委
    {"id": 18, "person_a": 7, "person_b": 1, "type": "superior_subordinate", "context": "黄冬生（纪委书记）对区委负责并报告工作", "overlap_org": "淮上区", "overlap_period": "2026"},
    # 组织部与区委
    {"id": 19, "person_a": 9, "person_b": 1, "type": "superior_subordinate", "context": "葛素强（组织部部长）作为区委常委协助书记抓干部工作", "overlap_org": "淮上区委", "overlap_period": "2026"},
    # 政法委与区委
    {"id": 20, "person_a": 11, "person_b": 1, "type": "superior_subordinate", "context": "刘国强（政法委书记）作为区委常委负责政法工作", "overlap_org": "淮上区委", "overlap_period": "2026"},
    # 宣传与区委
    {"id": 21, "person_a": 4, "person_b": 1, "type": "superior_subordinate", "context": "王雪（宣传部部长）作为区委常委负责宣传工作", "overlap_org": "淮上区委", "overlap_period": "2026"},
    # 常务副区长与副区长
    {"id": 22, "person_a": 5, "person_b": 6, "type": "superior_subordinate", "context": "刘锐（常务副区长）与邵于洋（副区长）同为区政府领导班子", "overlap_org": "淮上区政府", "overlap_period": "2026"},
    {"id": 23, "person_a": 5, "person_b": 12, "type": "superior_subordinate", "context": "刘锐（常务副区长）与刘言广（副区长）同为区政府领导班子", "overlap_org": "淮上区政府", "overlap_period": "2026"},
    {"id": 24, "person_a": 5, "person_b": 14, "type": "superior_subordinate", "context": "刘锐（常务副区长）与牛毅（副区长）同为区政府领导班子", "overlap_org": "淮上区政府", "overlap_period": "2026"},
    {"id": 25, "person_a": 5, "person_b": 15, "type": "superior_subordinate", "context": "刘锐（常务副区长）与汤瑞瑞（副区长）同为区政府领导班子", "overlap_org": "淮上区政府", "overlap_period": "2026"},
    {"id": 26, "person_a": 5, "person_b": 16, "type": "superior_subordinate", "context": "刘锐（常务副区长）与苏凌寒（副区长）同为区政府领导班子", "overlap_org": "淮上区政府", "overlap_period": "2026"},
]

# ── BUILD SQLite ────────────────────────────────────────────────────────

def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY,
            person_id INTEGER, org_id INTEGER, title TEXT,
            start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY,
            person_a INTEGER, person_b INTEGER, type TEXT,
            context TEXT, overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                   p["birthplace"], p["education"], p["party_join"],
                   p["work_start"], p["current_post"], p["current_org"], p["source"]))

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
    conn.close()
    print(f"✅ SQLite DB written: {DB_PATH}")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")


# ── BUILD GEXF ──────────────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Return 'r,g,b' string based on role."""
    post = p["current_post"]
    if "书记" in post and "纪委" not in post:
        return "255,50,50"        # Red - party secretary
    if "区长" in post or "市长" in post or "县长" in post:
        return "50,100,255"       # Blue - government head
    if "纪委" in post or "监委" in post:
        return "255,165,0"        # Orange - discipline
    if "人大" in post:
        return "200,255,255"      # Cyan - people's congress
    if "政协" in post:
        return "255,240,200"      # Cream - CPPCC
    return "100,100,100"          # Grey - others

def org_color(o):
    """Return 'r,g,b' string based on organization type."""
    t = o["type"]
    if t == "党委":
        return "255,200,200"
    if t == "政府":
        return "200,200,255"
    if t == "人大":
        return "200,255,255"
    if t == "政协":
        return "255,240,200"
    if t == "事业单位":
        return "220,220,220"
    return "200,200,200"

def is_top_leader(p):
    return "区委书记" in p["current_post"] or "区长" in p["current_post"]

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>淮上区领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Nodes: persons
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
        lines.append('      </node>')

    # Nodes: organizations
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["level"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    # person -> organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # person <-> person (relationship)
    for r in relationships:
        eid += 1
        weight = "2.0"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF graph written: {GEXF_PATH}")


# ── MAIN ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("  蚌埠市淮上区领导关系网络数据库构建")
    print(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    build_db()
    build_gexf()
    print("\n[DONE] Build complete.")
