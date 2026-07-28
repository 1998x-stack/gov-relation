#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 陆良县 leadership network."""

import sys
import os
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "陆良县"
TASK_ID = "yunnan_陆良县"
TMP = os.path.dirname(os.path.abspath(__file__))

# ── ORGANIZATIONS ─────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中国共产党陆良县委员会", "type": "党委", "level": "县处级",
     "parent": "中共曲靖市委", "location": "云南省曲靖市陆良县"},
    {"id": 2, "name": "陆良县人民政府", "type": "政府", "level": "县处级",
         "parent": "曲靖市人民政府", "location": "云南省曲靖市陆良县"},
    {"id": 3, "name": "中共陆良县纪律检查委员会", "type": "纪律检查", "level": "县处级",
         "parent": "中共曲靖市纪委", "location": "云南省曲靖市陆良县"},
    {"id": 4, "name": "中共陆良县委组织部", "type": "党委部门", "level": "乡科级",
         "parent": "中共陆良县委员会", "location": "云南省曲靖市陆良县"},
    {"id": 5, "name": "中共陆良县委宣传部", "type": "党委部门", "level": "乡科级",
         "parent": "中共陆良县委员会", "location": "云南省曲靖市陆良县"},
    {"id": 6, "name": "中共陆良县委政法委员会", "type": "党委部门", "level": "乡科级",
         "parent": "中共陆良县委员会", "location": "云南省曲靖市陆良县"},
    {"id": 7, "name": "中共陆良县委统战部", "type": "党委部门", "level": "乡科级",
         "parent": "中共陆良县委员会", "location": "云南省曲靖市陆良县"},
    {"id": 8, "name": "陆良县人民代表大会常务委员会", "type": "人大", "level": "县处级",
         "parent": "曲靖市人大常委会", "location": "云南省曲靖市陆良县"},
    {"id": 9, "name": "中国人民政治协商会议陆良县委员会", "type": "政协", "level": "县处级",
         "parent": "曲靖市政协", "location": "云南省曲靖市陆良县"},
    {"id": 10, "name": "陆良县公安局", "type": "政府", "level": "乡科级",
          "parent": "陆良县人民政府", "location": "云南省曲靖市陆良县"},
    {"id": 11, "name": "陆良县人民法院", "type": "司法", "level": "县处级",
          "parent": "曲靖市中级人民法院", "location": "云南省曲靖市陆良县"},
    {"id": 12, "name": "陆良县人民检察院", "type": "司法", "level": "县处级",
          "parent": "曲靖市人民检察院", "location": "云南省曲靖市陆良县"},
    {"id": 13, "name": "云南陆良产业园区管委会", "type": "开发区", "level": "县处级",
          "parent": "陆良县人民政府", "location": "云南省曲靖市陆良县"},
]

# ── PERSONS ───────────────────────────────────────────────────────────

persons = [
    # ── County Party Committee ──
    {"id": 1, "name": "曹维", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "中共陆良县委书记", "current_org": "中共陆良县委员会",
     "source": "https://www.luliang.gov.cn/news/zwdt/67165.html"},
    {"id": 2, "name": "查智昌", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "中共陆良县委副书记、县委统战部部长",
     "current_org": "中共陆良县委员会",
     "source": "https://www.luliang.gov.cn/news/zwdt/67165.html"},

    # ── County Government ──
    {"id": 3, "name": "李维", "gender": "男", "ethnicity": "汉族",
     "birth": "1974-10", "birthplace": "云南富源", "education": "省委党校研究生",
     "party_join": "1996-05", "work_start": "1997-07",
     "current_post": "中共陆良县委副书记、县长",
     "current_org": "陆良县人民政府",
     "source": "https://www.luliang.gov.cn/pub/description/17558.html"},
    {"id": 4, "name": "杨俊", "gender": "男", "ethnicity": "汉族",
     "birth": "1982-06", "birthplace": "云南陆良", "education": "大学",
     "party_join": "2003-12", "work_start": "2000-12",
     "current_post": "县委常委、常务副县长",
     "current_org": "陆良县人民政府",
     "source": "https://www.luliang.gov.cn/pub/description/25322.html"},
    {"id": 5, "name": "张正礼", "gender": "男", "ethnicity": "汉族",
     "birth": "1977-08", "birthplace": "云南沾益", "education": "大专",
     "party_join": "2006-08", "work_start": "1997-09",
     "current_post": "县委常委、副县长",
     "current_org": "陆良县人民政府",
     "source": "https://www.luliang.gov.cn/pub/description/32500.html"},
    {"id": 6, "name": "冯小雷", "gender": "男", "ethnicity": "汉族",
     "birth": "1984-08", "birthplace": "贵州遵义", "education": "大学",
     "party_join": "", "work_start": "2002-09",
     "current_post": "县委常委、副县长（挂职）",
     "current_org": "陆良县人民政府",
     "source": "https://www.luliang.gov.cn/pub/description/35442.html"},
    {"id": 7, "name": "史红祥", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-02", "birthplace": "云南陆良", "education": "在职研究生",
     "party_join": "2005-08", "work_start": "1994-07",
     "current_post": "副县长", "current_org": "陆良县人民政府",
     "source": "https://www.luliang.gov.cn/pub/description/17552.html"},
    {"id": 8, "name": "王云武", "gender": "男", "ethnicity": "汉族",
     "birth": "1988-09", "birthplace": "云南富源", "education": "大学",
     "party_join": "2008-07", "work_start": "2012-12",
     "current_post": "副县长、县公安局局长",
     "current_org": "陆良县人民政府",
     "source": "https://www.luliang.gov.cn/pub/description/17555.html"},
    {"id": 9, "name": "刘婕", "gender": "女", "ethnicity": "汉族",
     "birth": "1980-05", "birthplace": "云南宣威", "education": "大学",
     "party_join": "2020-08", "work_start": "2000-08",
     "current_post": "副县长", "current_org": "陆良县人民政府",
     "source": "https://www.luliang.gov.cn/pub/description/45644.html"},
    {"id": 10, "name": "李勇", "gender": "男", "ethnicity": "汉族",
     "birth": "1986-09", "birthplace": "云南沾益", "education": "大学",
     "party_join": "2014-09", "work_start": "2009-10",
     "current_post": "副县长", "current_org": "陆良县人民政府",
     "source": "https://www.luliang.gov.cn/pub/description/22245.html"},
    {"id": 11, "name": "张健", "gender": "男", "ethnicity": "汉族",
     "birth": "1989-10", "birthplace": "云南会泽", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "2012-09",
     "current_post": "副县长", "current_org": "陆良县人民政府",
     "source": "https://www.luliang.gov.cn/pub/description/17554.html"},
]

# ── POSITIONS ─────────────────────────────────────────────────────────

positions = [
    # 曹维
    {"id": 1, "person_id": 1, "org_id": 1,
     "title": "中共陆良县委书记", "start": "", "end": "present",
     "rank": "正处级", "note": ""},

    # 查智昌
    {"id": 2, "person_id": 2, "org_id": 1,
     "title": "陆良县委副书记、县委统战部部长", "start": "", "end": "present",
     "rank": "副处级", "note": ""},

    # 李维
    {"id": 3, "person_id": 3, "org_id": 2,
     "title": "县委副书记、县长，县政府党组书记", "start": "", "end": "present",
     "rank": "正处级", "note": "主持县政府全面工作；主持云南陆良产业园区管委会全面工作"},
    {"id": 4, "person_id": 3, "org_id": 1,
     "title": "中共陆良县委副书记", "start": "", "end": "present",
     "rank": "正处级", "note": ""},

    # 杨俊
    {"id": 5, "person_id": 4, "org_id": 2,
     "title": "县委常委、常务副县长，县政府党组副书记", "start": "", "end": "present",
     "rank": "副处级", "note": "分管发改、财政、应急等工作"},
    {"id": 6, "person_id": 4, "org_id": 1,
     "title": "中共陆良县委常委", "start": "", "end": "present",
     "rank": "副处级", "note": ""},

    # 张正礼
    {"id": 7, "person_id": 5, "org_id": 2,
     "title": "县委常委、副县长", "start": "", "end": "present",
     "rank": "副处级", "note": "分管生态环境、民政、水利等工作"},
    {"id": 8, "person_id": 5, "org_id": 1,
     "title": "中共陆良县委常委", "start": "", "end": "present",
     "rank": "副处级", "note": ""},

    # 冯小雷
    {"id": 9, "person_id": 6, "org_id": 2,
     "title": "县委常委、副县长（挂职）", "start": "", "end": "present",
     "rank": "副处级", "note": "负责交通、文化旅游、广电等工作"},
    {"id": 10, "person_id": 6, "org_id": 1,
     "title": "中共陆良县委常委", "start": "", "end": "present",
     "rank": "副处级", "note": ""},

    # 史红祥
    {"id": 11, "person_id": 7, "org_id": 2,
     "title": "副县长", "start": "", "end": "present",
     "rank": "副处级", "note": "负责自然资源、住建、市场监管等工作"},

    # 王云武
    {"id": 12, "person_id": 8, "org_id": 2,
     "title": "副县长、县公安局局长", "start": "", "end": "present",
     "rank": "副处级", "note": "负责公安、司法、信访、维稳等工作"},
    {"id": 13, "person_id": 8, "org_id": 10,
     "title": "陆良县公安局局长", "start": "", "end": "present",
     "rank": "乡科级", "note": ""},

    # 刘婕
    {"id": 14, "person_id": 9, "org_id": 2,
     "title": "副县长", "start": "", "end": "present",
     "rank": "副处级", "note": "负责农业农村、乡村振兴、水利等工作；致公党党员"},

    # 李勇
    {"id": 15, "person_id": 10, "org_id": 2,
     "title": "副县长", "start": "", "end": "present",
     "rank": "副处级", "note": "负责教育体育、商贸流通、招商引资等工作"},

    # 张健
    {"id": 16, "person_id": 11, "org_id": 2,
     "title": "副县长", "start": "", "end": "present",
     "rank": "副处级", "note": "负责民族宗教、人社、自然资源、住建、林业等工作"},
]

# ── RELATIONSHIPS ─────────────────────────────────────────────────────

relationships = [
    # 曹维 <-> 李维：书记+县长搭档
    {"id": 1, "person_a": 1, "person_b": 3,
     "type": "overlap", "context": "县委书记与县长搭档",
     "overlap_org": "中共陆良县委员会、陆良县人民政府",
     "overlap_period": "present"},
    # 曹维 <-> 查智昌：书记+专职副书记
    {"id": 2, "person_a": 1, "person_b": 2,
     "type": "overlap", "context": "县委书记与专职副书记",
     "overlap_org": "中共陆良县委员会",
     "overlap_period": "present"},
    # 曹维 <-> 杨俊：书记+常委
    {"id": 3, "person_a": 1, "person_b": 4,
     "type": "overlap", "context": "县委书记与县委常委（常务副县长）",
     "overlap_org": "中共陆良县委员会",
     "overlap_period": "present"},
    # 曹维 <-> 张正礼：书记+常委
    {"id": 4, "person_a": 1, "person_b": 5,
     "type": "overlap", "context": "县委书记与县委常委",
     "overlap_org": "中共陆良县委员会",
     "overlap_period": "present"},
    # 曹维 <-> 冯小雷：书记+挂职常委
    {"id": 5, "person_a": 1, "person_b": 6,
     "type": "overlap", "context": "县委书记与挂职常委",
     "overlap_org": "中共陆良县委员会",
     "overlap_period": "present"},
    # 李维 <-> 杨俊：县长+常务副县长
    {"id": 6, "person_a": 3, "person_b": 4,
     "type": "overlap", "context": "县长与常务副县长",
     "overlap_org": "陆良县人民政府",
     "overlap_period": "present"},
    # 李维 <-> 其他副县长：县政府班子
    {"id": 7, "person_a": 3, "person_b": 5,
     "type": "overlap", "context": "县长与副县长",
     "overlap_org": "陆良县人民政府",
     "overlap_period": "present"},
    {"id": 8, "person_a": 3, "person_b": 7,
     "type": "overlap", "context": "县长与副县长",
     "overlap_org": "陆良县人民政府",
     "overlap_period": "present"},
    {"id": 9, "person_a": 3, "person_b": 8,
     "type": "overlap", "context": "县长与副县长兼公安局长",
     "overlap_org": "陆良县人民政府",
     "overlap_period": "present"},
    {"id": 10, "person_a": 3, "person_b": 9,
     "type": "overlap", "context": "县长与副县长",
     "overlap_org": "陆良县人民政府",
     "overlap_period": "present"},
    {"id": 11, "person_a": 3, "person_b": 10,
     "type": "overlap", "context": "县长与副县长",
     "overlap_org": "陆良县人民政府",
     "overlap_period": "present"},
    {"id": 12, "person_a": 3, "person_b": 11,
     "type": "overlap", "context": "县长与副县长",
     "overlap_org": "陆良县人民政府",
     "overlap_period": "present"},
]

# ── BUILD ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    db_path = os.path.join(TMP, "陆良县_network.db")
    gexf_path = os.path.join(TMP, "陆良县_network.gexf")

    run_build(
        slug="陆良县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=db_path,
        gexf_path=gexf_path,
    )

    print(f"\nSummary:")
    print(f"  Persons:       {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions:     {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  DB:            {db_path}")
    print(f"  GEXF:          {gexf_path}")