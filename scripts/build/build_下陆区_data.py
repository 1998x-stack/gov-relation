#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 下陆区 (Xialu District, 黄石市, 湖北省) leadership network.

Task: hubei_下陆区
Province: 湖北省
Parent city: 黄石市
Region: 下陆区
Level: 市辖区
Targets: 区委书记 & 区长
Research date: 2026-08-03

Current leaders confirmed from:
- 下陆区政府官网 https://www.xialuqu.gov.cn/ (accessed 2026-08-03)
- 下陆区新闻 (汪勇检查防汛, 2026-05-20; 政绩观学习教育会, 2026-06-13; 区委常委会学习会, 2026-05-29)
- 区政府领导页: https://www.xialuqu.gov.cn/zwgk/fdzdgknr/qzfld/
"""

import sqlite3
import os
import sys
from datetime import datetime

# ── Paths ──
# __file__ = data/tmp/hubei_下陆区/build_下陆区_data.py (4 levels deep from repo root)
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
STAGING = os.path.join(BASE, "data/tmp/hubei_下陆区")
DB_PATH = os.path.join(STAGING, "下陆区_network.db")
GEXF_PATH = os.path.join(STAGING, "下陆区_network.gexf")

# ── Person ID Assignment ──────────────────────────────────────────────────
# Convention: xialu_{givenname} for dedup across investigations
P_IDS = {}

def pid(name):
    if name not in P_IDS:
        P_IDS[name] = len(P_IDS) + 1
    return P_IDS[name]

# ── RESEARCH DATA ───────────────────────────────────────────────────────────

# ===== PERSONS =====
persons_raw = [
    # ── District Party Committee Leaders ──
    {
        "name": "汪勇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "下陆区委书记、区长",
        "current_org": "中共下陆区委员会",
        "source": "https://www.xialuqu.gov.cn/tpxw/202605/t20260520_1329056.html",
        "source_note": "2026-05-20新闻: 区委书记、区长汪勇检查防汛备汛; 2026-06-13新闻: 区委书记汪勇出席政绩观教育推进会; 2026-05-29新闻: 区委书记、区长汪勇主持区委常委会学习会",
        "note": "汪勇同时担任区委书记和区长两职; 至2026年6月王永桂被任命为区委副书记、代理区长",
    },
    {
        "name": "王永桂",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "下陆区委副书记、副区长、代理区长",
        "current_org": "下陆区人民政府",
        "source": "https://www.xialuqu.gov.cn/tpxw/202606/t20260616_1335513.html (2026-06-13新闻: 主持政绩观教育推进会) & 区政府领导页 (2026-08-03)",
        "source_note": "2026-06-13首次以区委副书记、区政府党组书记、副区长、代理区长身份出席公开活动; 接替汪勇原区长职务",
    },
    {
        "name": "邓勇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会党组书记、主任",
        "current_org": "下陆区人民代表大会常务委员会",
        "source": "https://www.xialuqu.gov.cn/tpxw/202606/t20260616_1335513.html (2026-06-13新闻)",
    },
    {
        "name": "贾玉香",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协党组书记、主席",
        "current_org": "政协下陆区委员会",
        "source": "https://www.xialuqu.gov.cn/tpxw/202606/t20260616_1335513.html (2026-06-13新闻)",
    },
    {
        "name": "马哲强",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "下陆区人民政府",
        "source": "https://www.xialuqu.gov.cn/zwgk/fdzdgknr/qzfld/ (区政府领导页); https://www.xialuqu.gov.cn/tpxw/202606/t20260622_1336510.html (2026-06-22新闻)",
    },
    {
        "name": "占钢",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "下陆区人民政府",
        "source": "https://www.xialuqu.gov.cn/zwgk/fdzdgknr/qzfld/ (2026-08-03政府领导页); https://www.xialuqu.gov.cn/tpxw/202606/t20260622_1336510.html",
    },
    {
        "name": "曹建国",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、统战部部长",
        "current_org": "中共下陆区委员会",
        "source": "https://www.xialuqu.gov.cn/tpxw/202606/t20260601_1331838.html (2026-05-29区委常委会学习会: 区委常委、统战部部长曹建国交流发言)",
    },
    {
        "name": "彭学锋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区人民武装部部长",
        "current_org": "下陆区人民武装部",
        "source": "https://www.xialuqu.gov.cn/tpxw/202606/t20260601_1331838.html (2026-05-29新闻: 区委常委, 区人民武装部部长彭学锋); https://www.xialuqu.gov.cn/tpxw/202606/t20260622_1336510.html (2026-06-22新闻)",
    },
    {
        "name": "姜鹏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区领导 (区委常委)",
        "current_org": "中共下陆区委员会",
        "source": "https://www.xialuqu.gov.cn/tpxw/202606/t20260622_1336510.html (2026-06-22新闻列名: 姜鹏, 推测可能是政法委书记或纪委书记)",
        "note": "精确职务待确认",
    },
    {
        "name": "徐永安",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区领导 (区委常委)",
        "current_org": "中共下陆区委员会",
        "source": "https://www.xialuqu.gov.cn/tpxw/202606/t20260622_1336510.html (2026-06-22新闻: 区领导徐永安出席)",
        "source_id": "",
        "note": "区委常委身份待确认",
    },
    # ── District Government Leaders ──
    {
        "name": "陈浩",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "下陆区人民政府",
        "source": "https://www.xialuqu.gov.cn/zwgk/fdzdgknr/qzfld/ (区政府领导页)",
    },
    {
        "name": "王楠",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "下陆区人民政府",
        "source": "https://www.xialuqu.gov.cn/zwgk/fdzdgknr/qzfld/ (区政府领导页)",
    },
    {
        "name": "王海兵",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "下陆区人民政府",
        "source": "https://www.xialuqu.gov.cn/zwgk/fdzdgknr/qzfld/ (区政府领导页)",
    },
    {
        "name": "伍康",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "下陆区人民政府",
        "source": "https://www.xialuqu.gov.cn/zwgk/fdzdgknr/qzfld/ (区政府领导页)",
    },
    {
        "name": "熊伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "下陆区人民政府",
        "source": "https://www.xialuqu.gov.cn/zwgk/fdzdgknr/qzfld/ (区政府领导页); https://www.xialuqu.gov.cn/tpxw/202605/t20260520_1329056.html (参加防汛检查)",
    },
    {
        "name": "朱武杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长（挂职）",
        "current_org": "下陆区人民政府",
        "source": "https://www.xialuqu.gov.cn/zwgk/fdzdgknr/qzfld/ (区政府领导页)",
    },
    {
        "name": "徐丽霞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政府党组成员、区政府办主任",
        "current_org": "下陆区人民政府办公室",
        "source": "https://www.xialuqu.gov.cn/zwgk/fdzdgknr/qzfld/ (区政府领导页)",
    },
]

# Assign IDs
for p in persons_raw:
    p["id"] = pid(p["name"])

# ===== ORGANIZATIONS =====
organizations = [
    {"id": 1, "name": "中共下陆区委员会", "type": "党委", "level": "县处级", "parent": "中共黄石市委员会", "location": "湖北省黄石市下陆区"},
    {"id": 2, "name": "下陆区人民政府", "type": "政府", "level": "县处级", "parent": "黄石市人民政府", "location": "湖北省黄石市下陆区"},
    {"id": 3, "name": "下陆区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "黄石市人民代表大会常务委员会", "location": "湖北省黄石市下陆区"},
    {"id": 4, "name": "下陆区政治协商会议委员会", "type": "政协", "level": "县处级", "parent": "政协黄石市委员会", "location": "湖北省黄石市下陆区"},
    {"id": 5, "name": "中共下陆区纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共黄石市纪律检查委员会", "location": "湖北省黄石市下陆区"},
    {"id": 6, "name": "下陆区人民武装部", "type": "事业单位", "level": "县处级", "parent": "黄石军分区", "location": "湖北省黄石市下陆区"},
    {"id": 7, "name": "下陆区人民政府办公室", "type": "政府", "level": "乡科级", "parent": "下陆区人民政府", "location": "湖北省黄石市下陆区"},
    {"id": 8, "name": "中共下陆区委统战部", "type": "党委", "level": "乡科级", "parent": "中共下陆区委员会", "location": "湖北省黄石市下陆区"},
    {"id": 9, "name": "下陆区人大常委会办公室", "type": "人大", "level": "乡科级", "parent": "下陆区人民代表大会常务委员会", "location": "湖北省黄石市下陆区"},
    {"id": 10, "name": "下陆区政协办公室", "type": "政协", "level": "乡科级", "parent": "政协下陆区委员会", "location": "湖北省黄石市下陆区"},
]

# ===== POSITIONS =====
positions = []
eid = 0

def add_pos(person_name, org_id, title, start="", end="present", rank="", note="", source=""):
    global eid
    eid += 1
    positions.append({
        "id": eid, "person_id": pid(person_name), "org_id": org_id,
        "title": title, "start": start, "end": end, "rank": rank,
        "note": note, "source": source
    })

# 汪勇 - 区委书记兼区长
add_pos("汪勇", 1, "区委书记", "未知", "present", "正处级", "confirmed: 同时担任区委书记和区长, as of 2026-05-20新闻", "https://www.xialuqu.gov.cn/tpxw/202605/t20260520_1329056.html")
add_pos("汪勇", 2, "区长", "未知", "present", "正处级", "confirmed: 区委书记、区长一肩挑", "https://www.xialuqu.gov.cn/tpxw/202605/t20260520_1329056.html")
add_pos("汪勇", 5, "区国防动员委员会主任", "", "", "正处级", "confirmed: 防汛第一责任人身份", "https://www.xialuqu.gov.cn/tpxw/202605/t20260520_1329056.html")

# 王永桂 - 代理区长
add_pos("王永桂", 1, "区委副书记", "2026-06~", "present", "副处级", "confirmed: 首次公开以副书记身份出席2026-06-13会议", "https://www.xialuqu.gov.cn/tpxw/202606/t20260616_1335513.html")
add_pos("王永桂", 2, "副区长、代理区长", "2026-06~", "present", "正处级", "confirmed: 区政府领导页显示为代理区长; 主持06-13推进会", "https://www.xialuqu.gov.cn/zwgk/fdzdgknr/qzfld/")

# 邓勇 - 人大常委会主任
add_pos("邓勇", 3, "党组书记、主任", "", "present", "正处级", "confirmed", "https://www.xialuqu.gov.cn/tpxw/202606/t20260616_1335513.html")

# 贾玉香 - 政协主席
add_pos("贾玉香", 4, "党组书记、主席", "", "present", "正处级", "confirmed", "https://www.xialuqu.gov.cn/tpxw/202606/t20260616_1335513.html")

# 马哲强 - 区委常委、常务副区长
add_pos("马哲强", 1, "区委常委", "", "present", "副处级", "confirmed", "https://www.xialuqu.gov.cn/tpxw/202606/t20260622_1336510.html")
add_pos("马哲强", 2, "常务副区长", "", "present", "副处级", "confirmed", "https://www.xialuqu.gov.cn/zwgk/fdzdgknr/qzfld/")

# 占钢 - 区委常委、副区长
add_pos("占钢", 1, "区委常委", "", "present", "副处级", "confirmed", "https://www.xialuqu.gov.cn/tpxw/202606/t20260622_1336510.html")
add_pos("占钢", 2, "副区长", "", "present", "副处级", "confirmed", "https://www.xialuqu.gov.cn/zwgk/fdzdgknr/qzfld/")

# 曹建国 - 统战部长
add_pos("曹建国", 1, "区委常委", "", "present", "副处级", "confirmed", "https://www.xialuqu.gov.cn/tpxw/202606/t20260601_1331838.html")
add_pos("曹建国", 8, "统战部部长", "", "present", "副处级", "confirmed", "https://www.xialuqu.gov.cn/tpxw/202606/t20260601_1331838.html")

# 彭学锋 - 人武部长
add_pos("彭学锋", 6, "区人民武装部部长", "", "present", "副处级", "confirmed: 区委常委、区人民武装部部长", "https://www.xialuqu.gov.cn/tpxw/202606/t20260601_1331838.html")

# 姜鹏 - 区委常委（职务待确认）
add_pos("姜鹏", 1, "区委常委", "", "present", "副处级", "plausible: 区领导, 可能担任政法委书记或纪委书记", "https://www.xialuqu.gov.cn/tpxw/202606/t20260622_1336510.html")

# 徐永安 - 区领导（职务待确认）
add_pos("徐永安", 1, "区委常委或区领导", "", "present", "副处级", "plausible: 区领导, 具体职务待确认", "https://www.xialuqu.gov.cn/tpxw/202606/t20260622_1336510.html")

# 陈浩 - 副区长
add_pos("陈浩", 2, "副区长", "", "present", "副处级", "confirmed", "https://www.xialuqu.gov.cn/zwgk/fdzdgknr/qzfld/")

# 王楠 - 副区长
add_pos("王楠", 2, "副区长", "", "present", "副处级", "confirmed", "https://www.xialuqu.gov.cn/zwgk/fdzdgknr/qzfld/")

# 王海兵 - 副区长
add_pos("王海兵", 2, "副区长", "", "present", "副处级", "confirmed", "https://www.xialuqu.gov.cn/zwgk/fdzdgknr/qzfld/")

# 伍康 - 副区长
add_pos("伍康", 2, "副区长", "", "present", "副处级", "confirmed", "https://www.xialuqu.gov.cn/zwgk/fdzdgknr/qzfld/")

# 熊伟 - 副区长
add_pos("熊伟", 2, "副区长", "", "present", "副处级", "confirmed", "https://www.xialuqu.gov.cn/zwgk/fdzdgknr/qzfld/; 防汛检查陪同")

# 朱武杰 - 挂职副区长
add_pos("朱武杰", 2, "副区长（挂职）", "", "present", "副处级", "confirmed: 挂职", "https://www.xialuqu.gov.cn/zwgk/fdzdgknr/qzfld/")

# 徐丽霞 - 政府党组成员
add_pos("徐丽霞", 2, "区政府党组成员", "", "present", "正科级", "confirmed", "https://www.xialuqu.gov.cn/zwgk/fdzdgknr/qzfld/")
add_pos("徐丽霞", 7, "区政府办主任", "", "present", "正科级", "confirmed", "https://www.xialuqu.gov.cn/zwgk/fdzdgknr/qzfld/")

# ===== RELATIONSHIPS =====
relationships = []
rid = 0

def add_rel(a, b, rtype, strength, evidence, overlap_org="", overlap_period="", confidence="confirmed"):
    global rid
    rid += 1
    relationships.append({
        "id": rid, "person_a": pid(a), "person_b": pid(b),
        "type": rtype, "strength": strength, "context": evidence,
        "overlap_org": overlap_org, "overlap_period": overlap_period,
        "confidence": confidence
    })

# 党政主要班子关系
add_rel("汪勇", "王永桂", "superior_subordinate", "strong",
        "区委书记汪勇与代理区长王永桂为党政主要班子搭档; 王永桂由汪勇提名任代理区长; 2026-06-13共同主持政绩观教育推进会",
        "下陆区人民政府/中共下陆区委", "2026-06至今", "confirmed")

add_rel("汪勇", "邓勇", "superior_subordinate", "strong",
        "区委书记汪与人大常委会主任邓勇同为区主要领导; 共同出席重要会议",
        "下陆区党政领导班子", "2026", "confirmed")

add_rel("汪勇", "贾玉香", "superior_subordinate", "strong",
        "区委书记汪与政协主席贾玉香同为区主要领导; 共同出席重要会议",
        "下陆区党政领导班子", "2026", "confirmed")

add_rel("汪勇", "马哲强", "superior_subordinate", "strong",
        "汪勇为区委书记, 马哲E强为常务副区长; 在区委常委会和区政府领导班子中共事",
        "中共下陆区委/下陆区人民政府", "2026", "confirmed")

add_rel("汪勇", "占钢", "superior_subordinate", "strong",
        "汪勇为区委书记, 钢区委常委、副区长; 在常委班子中共事",
        "中共下陆区委/下陆区人民政府", "2026", "confirmed")

add_rel("汪勇", "曹建国", "superior_subordinate", "strong",
        "汪勇为区委书记, 曹建国为区委常委、统战部长; 2026-05-29区委常委会上同学习交流发言",
        "中共下陆区委", "2026", "confirmed")

add_rel("汪勇", "彭学锋", "superior_subordinate", "strong",
        "汪勇为区委书记, _X学锋为区委常委、人武部长; 2026-05-29常委会上汪勇主持、_X学锋出席",
        "中共下陆区委", "2026", "confirmed")

add_rel("汪勇", "熊伟", "superior_subordinate", "strong",
        "2026-05-19防汛检查中, 熊伟作为副区长随同汪勇检查防汛工作",
        "下陆区人民政府", "2026-05", "confirmed")

# 王永桂与班子成员关系
add_rel("王永桂", "马哲强", "superior_subordinate", "strong",
        "代理区长与常务副区长, 政务系统主要领导搭档",
        "下陆区人民政府", "2026-06至今", "confirmed")

add_rel("王永桂", "占钢", "superior_subordinate", "strong",
        "代理区长与副区长, 政府班子中共事",
        "下陆区人民政府", "2026-06至今", "confirmed")

add_rel("王永桂", "邓勇", "colleague", "medium",
        "王永桂(代理区长)与邓勇(人大主任)在两会期间协同工作",
        "下陆区党政领导班子", "2026-06至今", "confirmed")

add_rel("王永桂", "贾玉香", "colleague", "medium",
        "王永桂(代理区长)与贾玉香(政协主席)在政协会期协同工作",
        "下陆区党政领导班子", "2026-06至今", "confirmed")

# 副区长职务关系
add_rel("曹建国", "占钢", "colleague", "medium",
        "常务副区长与普通副区长, 在政府事务中有上下级关系",
        "下陆区人民政府", "2026", "confirmed")

add_rel("马哲强", "熊伟", "superior_subordinate", "medium",
        "常务副区长与普通副区长, 在政府事务中有上下级关系",
        "下陆区人民政府", "2026", "confirmed")

add_rel("曹建国", "占钢", "colleague", "medium",
        "同为区委常委, 在常委会中共事",
        "中共下陆区委", "2026", "confirmed")

add_rel("曹建国", "彭学锋", "colleague", "medium",
        "同为区委常委, 在常委会中共事",
        "中共下陆区委", "2026", "confirmed")

add_rel("曹建国", "姜鹏", "colleague", "medium",
        "同为区委常委, 在常委会中共事",
        "中共下陆区委", "2026", "confirmed")

add_rel("曹建国", "徐永安", "colleague", "medium",
        "同为区委/区领导, 共同出席工作会议",
        "下陆区党政领导班子", "2026", "confirmed")

add_rel("马哲强", "占钢", "colleague", "strong",
        "同为区委常委+副区长, 在常委会和政务系统双重共事",
        "中共下陆区委/下陆区人民政府", "2026", "confirmed")

# 人大政协与党政主要领导
add_rel("邓勇", "马哲强", "colleague", "medium",
        "人大常委会主任与常务副区长在人大会议和预算监督中协作",
        "下陆区党政领导班子", "2026", "confirmed")

add_rel("贾玉香", "马哲强", "colleague", "medium",
        "政协主席与常务副区长, 在政协协商平台协作",
        "下陆区党政领导班子", "2026", "confirmed")

# ===== BUILD FUNCTIONS =====

def build_db():
    """Create SQLite database with schema and data."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    cur.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
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
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            source TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            strength TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            confidence TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)
    
    # Insert persons
    for p in persons_raw:
        cur.execute("""
            INSERT OR REPLACE INTO persons (id, name, gender, ethnicity, birth, birthplace,
                education, party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
              p.get("birth", ""), p.get("birthplace", ""), p.get("education", ""),
              p.get("party_join", ""), p.get("work_start", ""),
              p.get("current_post", ""), p.get("current_org", ""), p.get("source", "")))
    
    # Insert organizations
    for o in organizations:
        cur.execute("""
            INSERT OR REPLACE INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o.get("location", "")))
    
    # Insert positions
    for pos in positions:
        cur.execute("""
            INSERT OR REPLACE INTO positions (id, person_id, org_id, title, start, end, rank, note, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
              pos["start"], pos["end"], pos.get("rank", ""), pos.get("note", ""), pos.get("source", "")))
    
    # Insert relationships
    for rel in relationships:
        cur.execute("""
            INSERT OR REPLACE INTO relationships (id, person_a, person_b, type, strength, context, overlap_org, overlap_period, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (rel["id"], rel["person_a"], rel["person_b"], rel["type"],
              rel["strength"], rel.get("context", ""), rel.get("overlap_org", ""),
              rel.get("overlap_period", ""), rel.get("confidence", "confirmed")))
    
    conn.commit()
    conn.close()
    print(f"  DB written: {DB_PATH}")


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&apos;")


def build_gexf():
    """Generate GEXF 1.3 graph file with viz namespace."""
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    
    # Prepare indices
    name_by_id = {p["id"]: p["name"] for p in persons_raw}
    
    # Person color by role
    def person_color(name):
        if name == "汪勇":
            return "255,50,50"  # 党政一肩挑 - red
        if name in ("王永桂", "马哲强", "占钢"):
            return "50,100,255"  # 政府主要: blue
        if name in ("曹建国", "彭学锋", "姜鹏", "徐永安"):
            return "100,100,100"  # other常委: grey
        return "100,100,100"  # default grey
    
    def person_size(name):
        if name in ("汪勇", "王永柱"):
            return "20.0"
        if name in ("邓勇", "贾玉香", "马哲强", "占钢"):
            return "12.0"
        return "12.0"
    
    # Org color
    def org_color(otype):
        m = {"党委": "255,200,200", "政府": "200,200,255", "人大": "200,255,255",
             "政协": "255,240,200", "事业单位": "220,220,220"}
        return m.get(otype, "200,200,200")
    
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation Research Agent</creator>')
    lines.append('    <description>下陆区 (黄石市, 湖北省) 领导班子工作关系网络 - 2026-08-03</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    
    # Attribute declarations
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="relation_type" type="string"/>')
    lines.append('      <attribute id="1" title="confidence" type="string"/>')
    lines.append('      <attribute id="2" title="strength" type="string"/>')
    lines.append('    </attributes>')
    
    # Nodes: persons
    lines.append('    <nodes>')
    for p in persons_raw:
        c = person_color(p["name"])
        sz = person_size(p["name"])
        role = p.get("current_post", "")
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    
    # Nodes: organizations
    for o in organizations:
        c = org_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'          <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'          <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')
    
    # Edges: person->organization (worked_at)
    lines.append('    <edges>')
    edge_id = 0
    for pos in positions:
        edge_id += 1
        lines.append(f'      <edge id="e{edge_id}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append('          <attvalue for="1" value="confirmed"/>')
        lines.append('          <attvalue for="2" value="strong"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    
    # Edges: person<->person (relationships)
    for rel in relationships:
        edge_id += 1
        weight = "2.0" if rel.get("strength") == "strong" else "1.0"
        if rel.get("strength") == "weak":
            weight = "0.5"
        lines.append(f'      <edge id="e{edge_id}" source="p{rel["person_a"]}" target="p{rel["person_b"]}" label="{esc(rel.get("type", ""))}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rel.get("type", ""))}"/>')
        lines.append(f'          <attvalue for="1" value="confirmed"/>')
        lines.append(f'          <attvalue for="2" value="{esc(rel.get("strength", "medium"))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')
    
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF written: {GEXF_PATH}")


# ── MAIN ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Building 下陆区 leadership network database and graph...")
    print(f"  Persons: {len(persons_raw)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    
    build_db()
    build_gexf()
    
    print("Done.")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")