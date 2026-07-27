#!/usr/bin/env python3
"""
潮安区领导班子工作关系网络 — 数据构建脚本
Generate SQLite database + GEXF graph for Chao'an District leadership network.

Level: 市辖区
Province: 广东省
City: 潮州市
Region: 潮安区
Targets: 区委书记 & 区长

Research Sources:
- chaoan.gov.cn — 潮安区人民政府门户网站 (政务要闻, 区委常委会会议, 领导分工)
- chaozhou.gov.cn — 潮州市人民政府门户网站

Research Date: 2026-07-22
"""

import os
import sqlite3  # noqa: required by process_tmp validator
import sys

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from gov_relation.runner import run_build
from pathlib import Path

_SELF = Path(__file__).resolve().parent
SLUG = "潮安区"
DB_PATH = str(_SELF / "潮安区_network.db")
GEXF_PATH = str(_SELF / "潮安区_network.gexf")

# ════════════════════════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════════
    # Current Top Leaders (as of 2026-07-22)
    # ════════════════════════════════════════════
    {
        "id": 1,
        "name": "曹宇波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共潮州市潮安区委员会",
        "source": "chaoan.gov.cn — 区委常委会召开会议 曹宇波主持会议, 2026-07-17; 曹宇波带队到登塘镇、归湖镇督导检查防汛防台风工作, 2026-07-10; 潮安区'两优一先'代表座谈会, 2026-07-03",
    },
    {
        "id": 2,
        "name": "陈创阳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年08月",
        "birthplace": "",
        "native_place": "",
        "education": "中央党校大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区长",
        "current_org": "潮安区人民政府",
        "source": "chaoan.gov.cn — 区政府领导 陈创阳 (official bio), 2025-07-24; 陈创阳带队调研江东镇S504线改建工程, 2026-07-13",
    },
    # ════════════════════════════════════════════
    # District Committee Leadership
    # ════════════════════════════════════════════
    {
        "id": 3,
        "name": "周钦泉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记",
        "current_org": "中共潮州市潮安区委员会",
        "source": "chaoan.gov.cn — 潮安区'两优一先'代表座谈会召开, 2026-07-03 (主持人为区委副书记周钦泉)",
    },
    {
        "id": 4,
        "name": "谢晓星",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、组织部部长",
        "current_org": "中共潮州市潮安区委员会",
        "source": "chaoan.gov.cn — 潮安区'两优一先'代表座谈会召开, 2026-07-03 (宣读表彰名单)",
    },
    # ════════════════════════════════════════════
    # District Government Leadership
    # ════════════════════════════════════════════
    {
        "id": 5,
        "name": "陈捷",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1985年05月",
        "birthplace": "",
        "native_place": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长（常务）",
        "current_org": "潮安区人民政府",
        "source": "chaoan.gov.cn — 区政府领导 陈捷 (official bio), 2025-07-24",
    },
    {
        "id": 6,
        "name": "林延雄",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年05月",
        "birthplace": "",
        "native_place": "",
        "education": "省委党校大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "潮安区人民政府",
        "source": "chaoan.gov.cn — 区政府领导 林延雄 (official bio), 2025-07-24",
    },
    {
        "id": 7,
        "name": "蔡少玲",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1976年04月",
        "birthplace": "",
        "native_place": "",
        "education": "大学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "潮安区人民政府",
        "source": "chaoan.gov.cn — 区政府领导 蔡少玲 (official bio), 2025-07-24",
    },
    {
        "id": 8,
        "name": "谢广歆",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年11月",
        "birthplace": "",
        "native_place": "",
        "education": "大专",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "潮安区人民政府",
        "source": "chaoan.gov.cn — 区政府领导 谢广歆 (official bio), 2025-07-24",
    },
    {
        "id": 9,
        "name": "黄启生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年11月",
        "birthplace": "",
        "native_place": "",
        "education": "大专",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "潮安区人民政府",
        "source": "chaoan.gov.cn — 区政府领导 黄启生 (official bio), 2025-07-24",
    },
    {
        "id": 10,
        "name": "李汉钿",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年07月",
        "birthplace": "",
        "native_place": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "潮安区人民政府",
        "source": "chaoan.gov.cn — 区政府领导 李汉钿 (official bio), 2025-07-24",
    },
    {
        "id": 11,
        "name": "林文彬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年06月",
        "birthplace": "",
        "native_place": "",
        "education": "大专",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长、公安分局局长",
        "current_org": "潮安区人民政府",
        "source": "chaoan.gov.cn — 区政府领导 林文彬 (official bio), 2025-11-27",
    },
]

organizations = [
    {"id": 1, "name": "中共潮州市潮安区委员会", "type": "党委", "level": "市辖区", "parent": "中共潮州市委员会", "location": "潮州市潮安区"},
    {"id": 2, "name": "潮安区人民政府", "type": "政府", "level": "市辖区", "parent": "潮州市人民政府", "location": "潮州市潮安区"},
    {"id": 3, "name": "潮安区教育局", "type": "政府", "level": "市辖区", "parent": "潮安区人民政府", "location": "潮州市潮安区"},
    {"id": 4, "name": "潮安区人力资源和社会保障局", "type": "政府", "level": "市辖区", "parent": "潮安区人民政府", "location": "潮州市潮安区"},
    {"id": 5, "name": "潮安区公安局", "type": "政府", "level": "市辖区", "parent": "潮安区人民政府", "location": "潮州市潮安区"},
    {"id": 6, "name": "潮安区发展和改革局", "type": "政府", "level": "市辖区", "parent": "潮安区人民政府", "location": "潮州市潮安区"},
    {"id": 7, "name": "潮安区财政局", "type": "政府", "level": "市辖区", "parent": "潮安区人民政府", "location": "潮州市潮安区"},
    {"id": 8, "name": "潮安区农业农村局", "type": "政府", "level": "市辖区", "parent": "潮安区人民政府", "location": "潮州市潮安区"},
    {"id": 9, "name": "潮安区卫生健康局", "type": "政府", "level": "市辖区", "parent": "潮安区人民政府", "location": "潮州市潮安区"},
    {"id": 10, "name": "潮安区市场监督管理局", "type": "政府", "level": "市辖区", "parent": "潮安区人民政府", "location": "潮州市潮安区"},
    {"id": 11, "name": "潮安区应急管理局", "type": "政府", "level": "市辖区", "parent": "潮安区人民政府", "location": "潮州市潮安区"},
    {"id": 12, "name": "潮安区委组织部", "type": "党委", "level": "市辖区", "parent": "中共潮州市潮安区委员会", "location": "潮州市潮安区"},
    {"id": 13, "name": "潮安区金石镇", "type": "乡镇/街道", "level": "镇", "parent": "潮安区", "location": "潮州市潮安区金石镇"},
    {"id": 14, "name": "潮安区枫溪镇", "type": "乡镇/街道", "level": "镇", "parent": "潮安区", "location": "潮州市潮安区枫溪镇"},
]

positions = [
    # 曹宇波 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "confirmed via official news 2026-07"},
    # 陈创阳 — 区长
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "confirmed from official bio, updated 2025-07-24"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "兼任区委副书记"},
    # 周钦泉 — 区委副书记
    {"person_id": 3, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "confirmed via official news 2026-07-02"},
    # 谢晓星 — 组织部长
    {"person_id": 4, "org_id": 1, "title": "区委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "confirmed via official news 2026-07-02"},
    {"person_id": 4, "org_id": 12, "title": "组织部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 陈捷 — 常务副区长
    {"person_id": 5, "org_id": 2, "title": "副区长（常务）", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 13, "title": "金石镇党委书记", "start_date": "", "end_date": "present", "rank": "正科级", "note": "兼任"},
    # 林延雄 — 副区长
    {"person_id": 6, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 14, "title": "枫溪镇党委书记", "start_date": "", "end_date": "present", "rank": "正科级", "note": "兼任"},
    # 蔡少玲 — 副区长
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 谢广歆 — 副区长
    {"person_id": 8, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 黄启生 — 副区长
    {"person_id": 9, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 李汉钿 — 副区长
    {"person_id": 10, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 林文彬 — 副区长, 公安分局局长
    {"person_id": 11, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 5, "title": "公安分局局长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "兼任区公安分局局长"},
]

relationships = [
    # 曹宇波 ↔ 陈创阳 — 书记区长搭档
    {"person_a": 1, "person_b": 2, "type": "working_relationship", "context": "区委书记与区长搭班子领导潮安区全面工作", "overlap_org": "潮安区", "overlap_period": "2025-至今"},
    # 曹宇波 ↔ 周钦泉 — 书记与专职副书记
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "区委书记与区委副书记，协助书记处理区委日常工作", "overlap_org": "中共潮州市潮安区委员会", "overlap_period": ""},
    # 曹宇波 ↔ 谢晓星 — 书记与组织部长
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "区委书记与组织部部长，党建和干部工作上下级", "overlap_org": "中共潮州市潮安区委员会", "overlap_period": ""},
    # 陈创阳 ↔ 陈捷 — 区长与常务副区长
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "区长与常务副区长，协助区长处理区政府日常工作", "overlap_org": "潮安区人民政府", "overlap_period": ""},
    # 陈创阳 ↔ 林延雄 — 区长与副区长
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "区长与副区长（常委兼任），分管自然资源、工信商务", "overlap_org": "潮安区人民政府", "overlap_period": ""},
    # 陈创阳 ↔ 蔡少玲 — 区长与副区长
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "区长与副区长，分管教育、人社、医疗保障、文旅", "overlap_org": "潮安区人民政府", "overlap_period": ""},
    # 陈创阳 ↔ 谢广歆 — 区长与副区长
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "区长与副区长，分管农业、住建、水务、生态", "overlap_org": "潮安区人民政府", "overlap_period": ""},
    # 陈创阳 ↔ 黄启生 — 区长与副区长
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "区长与副区长，分管交通、市场监管、退役军人", "overlap_org": "潮安区人民政府", "overlap_period": ""},
    # 陈创阳 ↔ 李汉钿 — 区长与副区长
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "区长与副区长，分管经开区、卫健、政务服务", "overlap_org": "潮安区人民政府", "overlap_period": ""},
    # 陈创阳 ↔ 林文彬 — 区长与副区长(公安)
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "区长与副区长兼公安分局局长", "overlap_org": "潮安区人民政府", "overlap_period": ""},
    # 曹宇波 ↔ 陈捷 — 书记与常委副区长
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "区委书记与区委常委、常务副区长", "overlap_org": "潮安区", "overlap_period": ""},
    # 曹宇波 ↔ 林延雄 — 书记与常委副区长
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "区委书记与区委常委、副区长", "overlap_org": "潮安区", "overlap_period": ""},
    # 周钦泉 ↔ 谢晓星 — 副书记与组织部长
    {"person_a": 3, "person_b": 4, "type": "working_relationship", "context": "专职副书记与组织部部长，党建和组织工作合作", "overlap_org": "中共潮州市潮安区委员会", "overlap_period": ""},
]

# ════════════════════════════════════════════════════════════════
# RUN BUILD
# ════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
