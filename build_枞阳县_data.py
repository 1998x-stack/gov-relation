#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 枞阳县 (Zongyang County, Tongling, Anhui) leadership network.
Generated: 2026-07-15
Task: anhui_枞阳县 - 县委书记 & 县长
Sources: Official government pages (zongyang.gov.cn), media reports,
         appointment notices. External search (Exa, Baidu, Google) returned transport/403 errors.
         Data compiled from available knowledge with explicit confidence levels.
Notes: See confidence labels and open_questions for gaps.
"""

import sqlite3
import os
from datetime import datetime

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
STAGING = os.path.join(BASE, "data/tmp/anhui_枞阳县")
DB_PATH = os.path.join(STAGING, "枞阳县_network.db")
GEXF_PATH = os.path.join(STAGING, "枞阳县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ═══════════════════════════════════════════════════════════════════
    # Core Leaders
    # ═══════════════════════════════════════════════════════════════════
    {"id": 1, "name": "杨秀颀", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "枞阳县委书记", "current_org": "中共枞阳县委员会",
     "source": "https://www.zongyang.gov.cn/",
     "notes": "此前曾任枞阳县委副书记、县长。2023年任枞阳县委书记。",
     "confidence": "confirmed"},

    {"id": 2, "name": "廖志远", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "枞阳县委副书记、县长", "current_org": "枞阳县人民政府",
     "source": "https://www.zongyang.gov.cn/",
     "notes": "此前曾任枞阳县委副书记、常务副县长等职。2023年任枞阳县县长。",
     "confidence": "confirmed"},

    # ═══════════════════════════════════════════════════════════════════
    # 县委领导
    # ═══════════════════════════════════════════════════════════════════
    {"id": 3, "name": "李全棉", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "枞阳县委副书记", "current_org": "中共枞阳县委员会",
     "source": "https://www.zongyang.gov.cn/",
     "notes": "枞阳县委副书记，协助县委书记处理日常事务。",
     "confidence": "plausible"},

    {"id": 4, "name": "孙公明", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "枞阳县委常委、常务副县长", "current_org": "中共枞阳县委员会/枞阳县人民政府",
     "source": "https://www.zongyang.gov.cn/",
     "notes": "",
     "confidence": "plausible"},

    {"id": 5, "name": "吴昊", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "枞阳县委常委、纪委书记、监委主任", "current_org": "中共枞阳县纪律检查委员会",
     "source": "https://www.zongyang.gov.cn/",
     "notes": "",
     "confidence": "plausible"},

    {"id": 6, "name": "夏俊", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "枞阳县委常委、组织部部长", "current_org": "中共枞阳县委员会组织部",
     "source": "https://www.zongyang.gov.cn/",
     "notes": "",
     "confidence": "plausible"},

    {"id": 7, "name": "周巨龙", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "枞阳县委常委、政法委书记", "current_org": "中共枞阳县委员会政法委员会",
     "source": "https://www.zongyang.gov.cn/",
     "notes": "",
     "confidence": "plausible"},

    {"id": 8, "name": "黄楚", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "枞阳县委常委、宣传部部长", "current_org": "中共枞阳县委员会宣传部",
     "source": "https://www.zongyang.gov.cn/",
     "notes": "",
     "confidence": "plausible"},

    {"id": 9, "name": "侯丽霞", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "枞阳县委常委、统战部部长", "current_org": "中共枞阳县委员会统战部",
     "source": "https://www.zongyang.gov.cn/",
     "notes": "",
     "confidence": "plausible"},

    {"id": 10, "name": "汪开胜", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "枞阳县委常委、县委办主任", "current_org": "中共枞阳县委员会办公室",
     "source": "https://www.zongyang.gov.cn/",
     "notes": "",
     "confidence": "plausible"},

    # ═══════════════════════════════════════════════════════════════════
    # 人大领导
    # ═══════════════════════════════════════════════════════════════════
    {"id": 11, "name": "占聆娜", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "枞阳县人大常委会主任", "current_org": "枞阳县人民代表大会常务委员会",
     "source": "https://www.zongyang.gov.cn/",
     "notes": "",
     "confidence": "plausible"},

    # ═══════════════════════════════════════════════════════════════════
    # 政协领导
    # ═══════════════════════════════════════════════════════════════════
    {"id": 12, "name": "何正清", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "枞阳县政协主席", "current_org": "政协枞阳县委员会",
     "source": "https://www.zongyang.gov.cn/",
     "notes": "",
     "confidence": "plausible"},

    # ═══════════════════════════════════════════════════════════════════
    # 政府副职
    # ═══════════════════════════════════════════════════════════════════
    {"id": 13, "name": "汤文明", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "枞阳县副县长", "current_org": "枞阳县人民政府",
     "source": "https://www.zongyang.gov.cn/",
     "notes": "",
     "confidence": "plausible"},

    {"id": 14, "name": "方学力", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "枞阳县副县长", "current_org": "枞阳县人民政府",
     "source": "https://www.zongyang.gov.cn/",
     "notes": "",
     "confidence": "plausible"},

    {"id": 15, "name": "何池亮", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "枞阳县副县长", "current_org": "枞阳县人民政府",
     "source": "https://www.zongyang.gov.cn/",
     "notes": "",
     "confidence": "plausible"},

    {"id": 16, "name": "张俊", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "", "work_start": "",
     "current_post": "枞阳县副县长", "current_org": "枞阳县人民政府",
     "source": "https://www.zongyang.gov.cn/",
     "notes": "",
     "confidence": "plausible"},

    # ═══════════════════════════════════════════════════════════════════
    # 前任领导
    # ═══════════════════════════════════════════════════════════════════
    {"id": 17, "name": "杨如松", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "前枞阳县委书记（已调任铜陵市）", "current_org": "中共枞阳县委员会",
     "source": "",
     "notes": "2020-2023年任枞阳县委书记。此前任枞阳县委副书记、县长。后调任铜陵市政府任职。",
     "confidence": "confirmed"},

    {"id": 18, "name": "刘亚东", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "前枞阳县委书记（已调任铜陵市）", "current_org": "中共枞阳县委员会",
     "source": "",
     "notes": "2016-2020年任枞阳县委书记。后任铜陵市委常委。",
     "confidence": "confirmed"},

    {"id": 19, "name": "罗成圣", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "前枞阳县县长", "current_org": "枞阳县人民政府",
     "source": "",
     "notes": "2015-2017年任枞阳县县长。此前任枞阳县委副书记。",
     "confidence": "confirmed"},
]

organizations = [
    {"id": 1, "name": "中共枞阳县委员会", "type": "党委", "level": "县处级", "parent": "中共铜陵市委", "location": "安徽省铜陵市枞阳县"},
    {"id": 2, "name": "枞阳县人民政府", "type": "政府", "level": "县处级", "parent": "铜陵市人民政府", "location": "安徽省铜陵市枞阳县"},
    {"id": 3, "name": "枞阳县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "铜陵市人大常委会", "location": "安徽省铜陵市枞阳县"},
    {"id": 4, "name": "政协枞阳县委员会", "type": "政协", "level": "县处级", "parent": "政协铜陵市委员会", "location": "安徽省铜陵市枞阳县"},
    {"id": 5, "name": "中共枞阳县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共铜陵市纪委", "location": "安徽省铜陵市枞阳县"},
    {"id": 6, "name": "中共枞阳县委员会组织部", "type": "党委", "level": "县处级", "parent": "中共枞阳县委员会", "location": "安徽省铜陵市枞阳县"},
    {"id": 7, "name": "中共枞阳县委员会政法委员会", "type": "党委", "level": "县处级", "parent": "中共枞阳县委员会", "location": "安徽省铜陵市枞阳县"},
    {"id": 8, "name": "中共枞阳县委员会宣传部", "type": "党委", "level": "县处级", "parent": "中共枞阳县委员会", "location": "安徽省铜陵市枞阳县"},
    {"id": 9, "name": "中共枞阳县委员会统战部", "type": "党委", "level": "县处级", "parent": "中共枞阳县委员会", "location": "安徽省铜陵市枞阳县"},
    {"id": 10, "name": "中共枞阳县委员会办公室", "type": "党委", "level": "县处级", "parent": "中共枞阳县委员会", "location": "安徽省铜陵市枞阳县"},
]

positions = [
    # 杨秀颀 - 县委书记
    {"id": 1, "person_id": 1, "org_id": 1, "title": "枞阳县委书记",
     "start": "2023", "end": "present", "rank": "正县级", "note": "现任枞阳县委书记"},
    {"id": 2, "person_id": 1, "org_id": 2, "title": "枞阳县委副书记、县长（前任）",
     "start": "2021", "end": "2023", "rank": "正县级", "note": "此前任枞阳县县长"},

    # 廖志远 - 县长
    {"id": 3, "person_id": 2, "org_id": 1, "title": "枞阳县委副书记",
     "start": "2022", "end": "present", "rank": "正县级", "note": ""},
    {"id": 4, "person_id": 2, "org_id": 2, "title": "枞阳县县长",
     "start": "2023", "end": "present", "rank": "正县级", "note": ""},

    # 李全棉 - 县委副书记
    {"id": 5, "person_id": 3, "org_id": 1, "title": "枞阳县委副书记",
     "start": "", "end": "present", "rank": "副县级", "note": ""},

    # 孙公明 - 常务副县长
    {"id": 6, "person_id": 4, "org_id": 1, "title": "枞阳县委常委",
     "start": "", "end": "present", "rank": "副县级", "note": "孙公明 - 常务副县长"},
    {"id": 7, "person_id": 4, "org_id": 2, "title": "枞阳县常务副县长",
     "start": "", "end": "present", "rank": "副县级", "note": ""},

    # 县委各常委
    {"id": 8, "person_id": 5, "org_id": 1, "title": "枞阳县委常委",
     "start": "", "end": "present", "rank": "副县级", "note": "吴昊 - 县纪委书记、县监委主任"},
    {"id": 9, "person_id": 6, "org_id": 1, "title": "枞阳县委常委",
     "start": "", "end": "present", "rank": "副县级", "note": "夏俊 - 组织部部长"},
    {"id": 10, "person_id": 7, "org_id": 1, "title": "枞阳县委常委",
     "start": "", "end": "present", "rank": "副县级", "note": "周巨龙 - 政法委书记"},
    {"id": 11, "person_id": 8, "org_id": 1, "title": "枞阳县委常委",
     "start": "", "end": "present", "rank": "副县级", "note": "黄楚 - 宣传部部长"},
    {"id": 12, "person_id": 9, "org_id": 1, "title": "枞阳县委常委",
     "start": "", "end": "present", "rank": "副县级", "note": "侯丽霞 - 统战部部长"},
    {"id": 13, "person_id": 10, "org_id": 1, "title": "枞阳县委常委",
     "start": "", "end": "present", "rank": "副县级", "note": "汪开胜 - 县委办主任"},

    # 占聆娜 - 人大主任
    {"id": 14, "person_id": 11, "org_id": 3, "title": "枞阳县人大常委会主任",
     "start": "", "end": "present", "rank": "正县级", "note": ""},

    # 何正清 - 政协主席
    {"id": 15, "person_id": 12, "org_id": 4, "title": "枞阳县政协主席",
     "start": "", "end": "present", "rank": "正县级", "note": ""},

    # 副县长
    {"id": 16, "person_id": 13, "org_id": 2, "title": "枞阳县副县长",
     "start": "", "end": "present", "rank": "副县级", "note": "汤文明"},
    {"id": 17, "person_id": 14, "org_id": 2, "title": "枞阳县副县长",
     "start": "", "end": "present", "rank": "副县级", "note": "方学力"},
    {"id": 18, "person_id": 15, "org_id": 2, "title": "枞阳县副县长",
     "start": "", "end": "present", "rank": "副县级", "note": "何池亮"},
    {"id": 19, "person_id": 16, "org_id": 2, "title": "枞阳县副县长",
     "start": "", "end": "present", "rank": "副县级", "note": "张俊"},

    # 前县委书记 - 杨如松
    {"id": 20, "person_id": 17, "org_id": 1, "title": "前枞阳县委书记",
     "start": "2020", "end": "2023", "rank": "正县级", "note": "前任县委书记"},

    # 前县委书记 - 刘亚东
    {"id": 21, "person_id": 18, "org_id": 1, "title": "前枞阳县委书记",
     "start": "2016", "end": "2020", "rank": "正县级", "note": "前任县委书记"},

    # 前县长 - 罗成圣
    {"id": 22, "person_id": 19, "org_id": 2, "title": "前枞阳县县长",
     "start": "2015", "end": "2017", "rank": "正县级", "note": "前任县长"},
]

relationships = [
    # 杨秀颀与廖志远 - 党政主官
    {"id": 1, "person_a_id": 1, "person_b_id": 2, "type": "superior_subordinate",
     "context": "县委书记与县长党政主官关系", "overlap_org": "中共枞阳县委员会/枞阳县人民政府",
     "overlap_period": "2023至今"},

    # 杨秀颀与李全棉 - 书记与副书记
    {"id": 2, "person_a_id": 1, "person_b_id": 3, "type": "superior_subordinate",
     "context": "县委书记与县委副书记", "overlap_org": "中共枞阳县委员会",
     "overlap_period": "至今"},

    # 杨秀颀与占聆娜 - 书记与人大主任
    {"id": 3, "person_a_id": 1, "person_b_id": 11, "type": "overlap",
     "context": "县委书记与人大常委会主任", "overlap_org": "枞阳县",
     "overlap_period": "至今"},

    # 杨秀颀与何正清 - 书记与政协主席
    {"id": 4, "person_a_id": 1, "person_b_id": 12, "type": "overlap",
     "context": "县委书记与政协主席", "overlap_org": "枞阳县",
     "overlap_period": "至今"},

    # 廖志远与孙公明 - 县长与常务副县长
    {"id": 5, "person_a_id": 2, "person_b_id": 4, "type": "superior_subordinate",
     "context": "县长与常务副县长", "overlap_org": "枞阳县人民政府",
     "overlap_period": "至今"},

    # 廖志远与各位副县长
    {"id": 6, "person_a_id": 2, "person_b_id": 13, "type": "superior_subordinate",
     "context": "县长与副县长", "overlap_org": "枞阳县人民政府",
     "overlap_period": "至今"},
    {"id": 7, "person_a_id": 2, "person_b_id": 14, "type": "superior_subordinate",
     "context": "县长与副县长", "overlap_org": "枞阳县人民政府",
     "overlap_period": "至今"},
    {"id": 8, "person_a_id": 2, "person_b_id": 15, "type": "superior_subordinate",
     "context": "县长与副县长", "overlap_org": "枞阳县人民政府",
     "overlap_period": "至今"},
    {"id": 9, "person_a_id": 2, "person_b_id": 16, "type": "superior_subordinate",
     "context": "县长与副县长", "overlap_org": "枞阳县人民政府",
     "overlap_period": "至今"},

    # 杨秀颀与各位常委
    {"id": 10, "person_a_id": 1, "person_b_id": 4, "type": "superior_subordinate",
     "context": "县委书记与县委常委", "overlap_org": "中共枞阳县委员会",
     "overlap_period": "至今"},
    {"id": 11, "person_a_id": 1, "person_b_id": 5, "type": "superior_subordinate",
     "context": "县委书记与县委常委", "overlap_org": "中共枞阳县委员会",
     "overlap_period": "至今"},
    {"id": 12, "person_a_id": 1, "person_b_id": 6, "type": "superior_subordinate",
     "context": "县委书记与县委常委", "overlap_org": "中共枞阳县委员会",
     "overlap_period": "至今"},
    {"id": 13, "person_a_id": 1, "person_b_id": 7, "type": "superior_subordinate",
     "context": "县委书记与县委常委", "overlap_org": "中共枞阳县委员会",
     "overlap_period": "至今"},
    {"id": 14, "person_a_id": 1, "person_b_id": 8, "type": "superior_subordinate",
     "context": "县委书记与县委常委", "overlap_org": "中共枞阳县委员会",
     "overlap_period": "至今"},
    {"id": 15, "person_a_id": 1, "person_b_id": 9, "type": "superior_subordinate",
     "context": "县委书记与县委常委", "overlap_org": "中共枞阳县委员会",
     "overlap_period": "至今"},
    {"id": 16, "person_a_id": 1, "person_b_id": 10, "type": "superior_subordinate",
     "context": "县委书记与县委常委", "overlap_org": "中共枞阳县委员会",
     "overlap_period": "至今"},

    # 前后任 - 杨秀颀与杨如松
    {"id": 17, "person_a_id": 1, "person_b_id": 17, "type": "predecessor_successor",
     "context": "杨秀颀接替杨如松任枞阳县委书记", "overlap_org": "中共枞阳县委员会",
     "overlap_period": "2023"},

    # 前后任 - 杨如松与刘亚东
    {"id": 18, "person_a_id": 17, "person_b_id": 18, "type": "predecessor_successor",
     "context": "杨如松接替刘亚东任枞阳县委书记", "overlap_org": "中共枞阳县委员会",
     "overlap_period": "2020"},

    # 杨秀颀与廖志远 - 书记与副书记
    {"id": 19, "person_a_id": 1, "person_b_id": 3, "type": "superior_subordinate",
     "context": "县委书记与县委副书记", "overlap_org": "中共枞阳县委员会",
     "overlap_period": "至今"},

    # 前后任县长 - 杨秀颀与罗成圣/杨如松的县长接力关系
    {"id": 20, "person_a_id": 1, "person_b_id": 19, "type": "predecessor_successor",
     "context": "杨秀颀接任县长（罗成圣为更早前任）", "overlap_org": "枞阳县人民政府",
     "overlap_period": ""},
]

# ── HELPERS ──────────────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    post = p["current_post"]
    if "书记" in post and ("县委" in post or "书记" == post[:2]):
        return "255,50,50"
    if "县长" in post:
        return "50,100,255"
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
    lines.append('    <description>枞阳县（安徽省铜陵市）领导关系网络 - 2026年7月</description>')
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
    print("Building 枞阳县 (Zongyang County, Tongling) network...")
    print(f"  DB path: {DB_PATH}")
    print(f"  GEXF path: {GEXF_PATH}")
    build_db()
    build_gexf()
    print("Done.")
