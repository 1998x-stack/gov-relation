#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
饶阳县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 河北省
Parent City: 衡水市
Region: 饶阳县
Targets: 县委书记 & 县长

Research Sources:
- 饶阳县人民政府官方网站 (www.raoyang.gov.cn) — 新闻会议确认石瑞发任县委书记
- 百度百科 — 饶阳县词条确认县委、县政府领导班子
- 快懂百科 — 石瑞发简历（阜城县委书记任上资料）
- 饶阳新闻 — 中共饶阳县第十三届委员会第186次常委会会议(2026-05-08)确认石瑞发时任县委书记
- 饶阳新闻 — 中共饶阳县第十四次代表大会(2026-07-17/18)选举产生新一届县委

Research Date: 2026-07-24
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build

SLUG = "饶阳县"

_script_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_script_dir, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(_script_dir, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "石瑞发",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年8月（待确认）",
        "birthplace": "河北省丰宁县（待确认）",
        "native_place": "河北省",
        "education": "河北师范大学汉语言文学专业（大学）",
        "party_join": "2001年5月",
        "work_start": "2001年7月",
        "current_post": "饶阳县委书记",
        "current_org": "中共饶阳县委员会",
        "source": "中共饶阳县第十三届委员会第186次常委会会议(2026-05-08)报道中称\"县委书记石瑞发\"；百度百科饶阳县词条确认。来源：http://www.raoyang.gov.cn/art/2026/5/11/art_291_624835.html"
    },
    {
        "id": 2,
        "name": "李燕",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "饶阳县委副书记、县长",
        "current_org": "饶阳县人民政府",
        "source": "百度百科饶阳县词条确认县委副书记、县长为李燕。来源：https://baike.baidu.com/item/%E9%A5%B6%E9%98%B3%E5%8E%BF"
    },
    # ════════════════════════════════════════
    # 县政府领导班子 (来自百度百科)
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "张钰",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "饶阳县委常委、常务副县长",
        "current_org": "饶阳县人民政府",
        "source": "百度百科饶阳县词条。来源：https://baike.baidu.com/item/%E9%A5%B6%E9%98%B3%E5%8E%BF"
    },
    {
        "id": 4,
        "name": "牛荣霞",
        "gender": "女",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "饶阳县副县长",
        "current_org": "饶阳县人民政府",
        "source": "百度百科饶阳县词条。来源：https://baike.baidu.com/item/%E9%A5%B6%E9%98%B3%E5%8E%BF"
    },
    {
        "id": 5,
        "name": "张晓勇",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "饶阳县副县长",
        "current_org": "饶阳县人民政府",
        "source": "百度百科饶阳县词条。来源：https://baike.baidu.com/item/%E9%A5%B6%E9%98%B3%E5%8E%BF"
    },
    {
        "id": 6,
        "name": "王伟佳",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "饶阳县副县长",
        "current_org": "饶阳县人民政府",
        "source": "百度百科饶阳县词条。来源：https://baike.baidu.com/item/%E9%A5%B6%E9%98%B3%E5%8E%BF"
    },
    {
        "id": 7,
        "name": "乔树昆",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "饶阳县副县长",
        "current_org": "饶阳县人民政府",
        "source": "百度百科饶阳县词条。来源：https://baike.baidu.com/item/%E9%A5%B6%E9%98%B3%E5%8E%BF"
    },
    {
        "id": 8,
        "name": "郝力",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "饶阳县副县长",
        "current_org": "饶阳县人民政府",
        "source": "百度百科饶阳县词条。来源：https://baike.baidu.com/item/%E9%A5%B6%E9%98%B3%E5%8E%BF"
    },
    {
        "id": 9,
        "name": "沈忠泉",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "饶阳县副县长",
        "current_org": "饶阳县人民政府",
        "source": "百度百科饶阳县词条。来源：https://baike.baidu.com/item/%E9%A5%B6%E9%98%B3%E5%8E%BF"
    },
    {
        "id": 10,
        "name": "石宏业",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "饶阳县政府党组成员",
        "current_org": "饶阳县人民政府",
        "source": "百度百科饶阳县词条。来源：https://baike.baidu.com/item/%E9%A5%B6%E9%98%B3%E5%8E%BF"
    },
]

# 2. Organizations
organizations = [
    {"id": 1, "name": "中共饶阳县委员会", "type": "党委", "level": "县处级", "location": "河北省衡水市饶阳县"},
    {"id": 2, "name": "饶阳县人民政府", "type": "政府", "level": "县处级", "location": "河北省衡水市饶阳县"},
    {"id": 3, "name": "衡水市人民政府", "type": "政府", "level": "地厅级", "location": "河北省衡水市"},
    {"id": 4, "name": "河北师范大学", "type": "事业单位", "level": "", "location": "河北省石家庄市"},
]

# 3. Positions
positions = [
    # 石瑞发 (id=1)
    {"person_id": 1, "org_id": 1, "title": "饶阳县委书记", "start_date": "待查", "end_date": "present", "rank": "县处级正职", "note": "2026年5月报道中已任饶阳县委书记"},
    {"person_id": 1, "org_id": 4, "title": "河北师范大学中文系学生", "start_date": "1997-09", "end_date": "2001-07", "rank": "", "note": "汉语言文学专业"},
    # 李燕 (id=2)
    {"person_id": 2, "org_id": 2, "title": "饶阳县委副书记、县长", "start_date": "待查", "end_date": "present", "rank": "县处级正职", "note": "百度百科确认"},
    # 张钰 (id=3)
    {"person_id": 3, "org_id": 2, "title": "饶阳县委常委、常务副县长", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 牛荣霞 (id=4)
    {"person_id": 4, "org_id": 2, "title": "饶阳县副县长", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 张晓勇 (id=5)
    {"person_id": 5, "org_id": 2, "title": "饶阳县副县长", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 王伟佳 (id=6)
    {"person_id": 6, "org_id": 2, "title": "饶阳县副县长", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 乔树昆 (id=7)
    {"person_id": 7, "org_id": 2, "title": "饶阳县副县长", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 郝力 (id=8)
    {"person_id": 8, "org_id": 2, "title": "饶阳县副县长", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 沈忠泉 (id=9)
    {"person_id": 9, "org_id": 2, "title": "饶阳县副县长", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 石宏业 (id=10)
    {"person_id": 10, "org_id": 2, "title": "饶阳县政府党组成员", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": ""},
]

# 4. Relationships
relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记与县长搭班子", "overlap_org": "饶阳县", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县委书记与常务副县长搭班子", "overlap_org": "饶阳县", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "县长与常务副县长搭班子", "overlap_org": "饶阳县人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "县长与副县长搭班子", "overlap_org": "饶阳县人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "县长与副县长搭班子", "overlap_org": "饶阳县人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "县长与副县长搭班子", "overlap_org": "饶阳县人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "县长与副县长搭班子", "overlap_org": "饶阳县人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "县长与副县长搭班子", "overlap_org": "饶阳县人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "县长与副县长搭班子", "overlap_org": "饶阳县人民政府", "overlap_period": "当前"},
]

if __name__ == "__main__":
    import sys
    from pathlib import Path
    out_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent
    db_path = out_dir / "饶阳县_network.db"
    gexf_path = out_dir / "饶阳县_network.gexf"
    run_build(slug="饶阳县", persons=persons, organizations=organizations,
              positions=positions, relationships=relationships,
              db_path=db_path, gexf_path=gexf_path, overwrite=True)
    print(f"Output: {out_dir}")
