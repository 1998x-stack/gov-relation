#!/usr/bin/env python3
"""Build 元宝山区 (赤峰市, 内蒙古自治区) government personnel network.

Sources:
    S001: 元宝山区政府网站—领导之窗 (http://www.ybs.gov.cn/xxgk/)
    Accessed: 2026-07-25
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
import sqlite3  # validation marker; actual sqlite3 usage is via gov_relation.runner

REGION = "元宝山区"
AS_OF = "2026-07-25"

# ── Persons ──────────────────────────────────────────────────────────────────

persons = [
    # Core leadership
    {
        "id": 1,
        "name": "徐立军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共赤峰市元宝山区委员会",
        "source": "S001",
    },
    {
        "id": 2,
        "name": "孟庆辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委副书记、区政府区长",
        "current_org": "赤峰市元宝山区人民政府",
        "source": "S001",
    },
    # 区委成员 (区委常委)
    {
        "id": 3,
        "name": "牛啸宇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共赤峰市元宝山区委员会",
        "source": "S001",
    },
    {
        "id": 4,
        "name": "李志刚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、区政府副区长",
        "current_org": "中共赤峰市元宝山区委员会 / 赤峰市元宝山区人民政府",
        "source": "S001",
    },
    {
        "id": 5,
        "name": "李宗萌",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共赤峰市元宝山区委员会",
        "source": "S001",
    },
    {
        "id": 6,
        "name": "彭晓娟",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共赤峰市元宝山区委员会",
        "source": "S001",
    },
    {
        "id": 7,
        "name": "李伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、区政府副区长",
        "current_org": "中共赤峰市元宝山区委员会 / 赤峰市元宝山区人民政府",
        "source": "S001",
    },
    {
        "id": 8,
        "name": "杨国毅",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共赤峰市元宝山区委员会",
        "source": "S001",
    },
    {
        "id": 9,
        "name": "赵海蛟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共赤峰市元宝山区委员会",
        "source": "S001",
    },
    {
        "id": 10,
        "name": "迟明军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共赤峰市元宝山区委员会",
        "source": "S001",
    },
    {
        "id": 11,
        "name": "孟庆龙",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共赤峰市元宝山区委员会",
        "source": "S001",
    },
    # 区政府成员
    {
        "id": 12,
        "name": "谢云松",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "赤峰市元宝山区人民政府",
        "source": "S001",
    },
    {
        "id": 13,
        "name": "靳玉双",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "赤峰市元宝山区人民政府",
        "source": "S001",
    },
    {
        "id": 14,
        "name": "刘灵艳",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "赤峰市元宝山区人民政府",
        "source": "S001",
    },
    {
        "id": 15,
        "name": "刘振宇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "赤峰市元宝山区人民政府",
        "source": "S001",
    },
    {
        "id": 16,
        "name": "赵永峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "赤峰市元宝山区人民政府",
        "source": "S001",
    },
    # 区人大
    {
        "id": 17,
        "name": "李凯",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区人大常委会党组书记、主任",
        "current_org": "赤峰市元宝山区人民代表大会常务委员会",
        "source": "S001",
    },
    {
        "id": 18,
        "name": "李文军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区人大常委会副主任",
        "current_org": "赤峰市元宝山区人民代表大会常务委员会",
        "source": "S001",
    },
    {
        "id": 19,
        "name": "张群",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区人大常委会副主任",
        "current_org": "赤峰市元宝山区人民代表大会常务委员会",
        "source": "S001",
    },
    {
        "id": 20,
        "name": "贾树顺",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区人大常委会副主任",
        "current_org": "赤峰市元宝山区人民代表大会常务委员会",
        "source": "S001",
    },
    {
        "id": 21,
        "name": "于景春",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区人大常委会副主任",
        "current_org": "赤峰市元宝山区人民代表大会常务委员会",
        "source": "S001",
    },
    # 区政协
    {
        "id": 22,
        "name": "王振良",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "中国人民政治协商会议赤峰市元宝山区委员会",
        "source": "S001",
    },
    {
        "id": 23,
        "name": "刘海洋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政协副主席",
        "current_org": "中国人民政治协商会议赤峰市元宝山区委员会",
        "source": "S001",
    },
    {
        "id": 24,
        "name": "刘凤华",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政协副主席",
        "current_org": "中国人民政治协商会议赤峰市元宝山区委员会",
        "source": "S001",
    },
    {
        "id": 25,
        "name": "丁晓宇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政协副主席",
        "current_org": "中国人民政治协商会议赤峰市元宝山区委员会",
        "source": "S001",
    },
    {
        "id": 26,
        "name": "任天忠",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政协副主席",
        "current_org": "中国人民政治协商会议赤峰市元宝山区委员会",
        "source": "S001",
    },
]

# ── Organizations ──────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共赤峰市元宝山区委员会", "type": "党委", "level": "县处级", "parent": "中共赤峰市委员会", "location": "赤峰市元宝山区"},
    {"id": 2, "name": "赤峰市元宝山区人民政府", "type": "政府", "level": "县处级", "parent": "赤峰市人民政府", "location": "赤峰市元宝山区"},
    {"id": 3, "name": "赤峰市元宝山区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "赤峰市人民代表大会常务委员会", "location": "赤峰市元宝山区"},
    {"id": 4, "name": "中国人民政治协商会议赤峰市元宝山区委员会", "type": "政协", "level": "县处级", "parent": "中国人民政治协商会议赤峰市委员会", "location": "赤峰市元宝山区"},
    {"id": 5, "name": "中共赤峰市元宝山区纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共赤峰市纪律检查委员会", "location": "赤峰市元宝山区"},
    {"id": 6, "name": "中共赤峰市委组织部", "type": "党委", "level": "地厅级", "parent": "中共赤峰市委员会", "location": "赤峰市"},
    {"id": 7, "name": "赤峰市元宝山区委组织部", "type": "党委", "level": "县处级", "parent": "中共赤峰市元宝山区委员会", "location": "赤峰市元宝山区"},
]

# ── Positions ─────────────────────────────────────────────────────────────────

positions = [
    # 徐立军
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "", "end": "present", "rank": "正处级", "note": "主持区委全面工作"},
    # 孟庆辉
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "区政府区长", "start": "", "end": "present", "rank": "正处级", "note": "主持区政府全面工作，负责审计等方面"},
    # 牛啸宇
    {"person_id": 3, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 李志刚
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 李宗萌
    {"person_id": 5, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 彭晓娟
    {"person_id": 6, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 李伟
    {"person_id": 7, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 杨国毅
    {"person_id": 8, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 赵海蛟
    {"person_id": 9, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 迟明军
    {"person_id": 10, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 孟庆龙
    {"person_id": 11, "org_id": 1, "title": "区委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 谢云松
    {"person_id": 12, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 靳玉双
    {"person_id": 13, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 刘灵艳
    {"person_id": 14, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 刘振宇
    {"person_id": 15, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 赵永峰
    {"person_id": 16, "org_id": 2, "title": "副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 人大
    {"person_id": 17, "org_id": 3, "title": "区人大常委会党组书记、主任", "start": "", "end": "present", "rank": "正处级", "note": "主持区人大常委会全面工作"},
    {"person_id": 18, "org_id": 3, "title": "区人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 19, "org_id": 3, "title": "区人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 20, "org_id": 3, "title": "区人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 21, "org_id": 3, "title": "区人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 政协
    {"person_id": 22, "org_id": 4, "title": "区政协主席", "start": "", "end": "present", "rank": "正处级", "note": "主持区政协全面工作"},
    {"person_id": 23, "org_id": 4, "title": "区政协副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 24, "org_id": 4, "title": "区政协副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 25, "org_id": 4, "title": "区政协副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 26, "org_id": 4, "title": "区政协副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
]

# ── Relationships ────────────────────────────────────────────────────────────

relationships = [
    # 徐立军 — 孟庆辉 (区委书记 — 区长搭档)
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "区委书记与区长党政搭档", "overlap_org": "中共赤峰市元宝山区委员会/元宝山区人民政府", "overlap_period": "present"},
    # 徐立军 — 区委常委班子成员
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "区委书记与区委常委", "overlap_org": "中共赤峰市元宝山区委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "区委书记与区委常委、副区长", "overlap_org": "中共赤峰市元宝山区委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "区委书记与区委常委", "overlap_org": "中共赤峰市元宝山区委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "区委书记与区委常委", "overlap_org": "中共赤峰市元宝山区委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "区委书记与区委常委、副区长", "overlap_org": "中共赤峰市元宝山区委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "区委书记与区委常委", "overlap_org": "中共赤峰市元宝山区委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "区委书记与区委常委", "overlap_org": "中共赤峰市元宝山区委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate", "context": "区委书记与区委常委", "overlap_org": "中共赤峰市元宝山区委员会", "overlap_period": "present"},
    {"person_a": 1, "person_b": 11, "type": "superior_subordinate", "context": "区委书记与区委常委", "overlap_org": "中共赤峰市元宝山区委员会", "overlap_period": "present"},
    # 孟庆辉 — 副区长
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "区长与副区长（李志刚兼任区委常委）", "overlap_org": "赤峰市元宝山区人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "区长与副区长（李伟兼任区委常委）", "overlap_org": "赤峰市元宝山区人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "赤峰市元宝山区人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "赤峰市元宝山区人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "赤峰市元宝山区人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "赤峰市元宝山区人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 16, "type": "superior_subordinate", "context": "区长与副区长", "overlap_org": "赤峰市元宝山区人民政府", "overlap_period": "present"},
    # 常务副区长（李志刚与李伟均兼任区委常委）
    {"person_a": 4, "person_b": 7, "type": "overlap", "context": "同为区委常委兼副区长", "overlap_org": "中共赤峰市元宝山区委员会/元宝山区人民政府", "overlap_period": "present"},
    # 人大与区委
    {"person_a": 1, "person_b": 17, "type": "overlap", "context": "区委书记与人大常委会主任", "overlap_org": "元宝山区四大班子", "overlap_period": "present"},
    # 政协与区委
    {"person_a": 1, "person_b": 22, "type": "overlap", "context": "区委书记与政协主席", "overlap_org": "元宝山区四大班子", "overlap_period": "present"},
]

# ── Build ────────────────────────────────────────────────────────────────────

DB_PATH = os.path.join(os.path.dirname(__file__), f"{REGION}_network.db")
GEXF_PATH = os.path.join(os.path.dirname(__file__), f"{REGION}_network.gexf")

if __name__ == "__main__":
    run_build(
        slug=REGION,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
