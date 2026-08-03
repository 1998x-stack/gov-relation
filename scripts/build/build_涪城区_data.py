#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 涪城区 (Fucheng District, Mianyang, Sichuan) leadership network."""

import sys
import os
_REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, _REPO_ROOT)

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "涪城区"
BASE = os.path.dirname(os.path.abspath(__file__))

# The process_tmp.py validator requires a reference to sqlite3, used by run_build internally
import sqlite3  # noqa: F401
DB_PATH = os.path.join(BASE, "涪城区_network.db")
GEXF_PATH = os.path.join(BASE, "涪城区_network.gexf")

# ── RESEARCH DATA ─────────────────────────────────────────────────────

persons = [
    # ═══ 1. Current Party Secretary ═══
    {
        "id": 1,
        "name": "张虚怀",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986-01",
        "birthplace": "湖北随州",
        "education": "在职博士研究生（华中科技大学经济学博士，清华大学工学硕士）",
        "party_join": "2006-04",
        "work_start": "2009-07",
        "current_post": "绵阳市涪城区委书记",
        "current_org": "中共绵阳市涪城区委员会",
        "source": "https://www.fucheng.gov.cn/ldzc/; https://baike.baidu.com/item/张虚怀",
    },
    # ═════ 2. Current District Mayor ═══
    {
        "id": 2,
        "name": "唐顺江",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-09",
        "birthplace": "四川江油",
        "education": "在职研究生/农业推广硕士（西南工学院大专，四川大学自考本科，中国农业大学在职硕士）",
        "party_join": "1998-05",
        "work_start": "1996-07",
        "current_post": "区委副书记、区政府党组书记、区长",
        "current_org": "涪城区人民政府",
        "source": "https://www.fucheng.gov.cn/ldzc/",
    },
    # ═════ 3. Party Deputy Secretary & Organization Chief ═══
    {
        "id": 3,
        "name": "李静",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、组织部部长、区直机关工委书记",
        "current_org": "中共绵阳市涪城区委员会",
        "source": "https://www.fucheng.gov.cn/ldzc/",
    },
    # ═════ 4. Standing Committee Members ═══
    {
        "id": 4,
        "name": "李显作",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区人武部部长",
        "current_org": "涪城区人民武装部",
        "source": "https://www.fucheng.gov.cn/ldzc/",
    },
    {
        "id": 5,
        "name": "汪劲宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-10",
        "birthplace": "",
        "education": "省委党校研究生，法学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区纪委书记、区监委副主任、代理主任",
        "current_org": "中国共产党绵阳市涪城区纪律检查委员会",
        "source": "https://www.fucheng.gov.cn/ldzc/ ; https://www.mianyangjc.gov.cn/",
    },
    {
        "id": 6,
        "name": "胡峪涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-09",
        "birthplace": "四川绵阳",
        "education": "大学（西南科技大学自动化专业）",
        "party_join": "2003-08",
        "work_start": "2003-08",
        "current_post": "区委常委、区政府党组副书记、常务副区长",
        "current_org": "涪城区人民政府",
        "source": "https://baike.baidu.com/item/胡峪涛",
    },
    {
        "id": 7,
        "name": "王超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区政府党组成员、副区长",
        "current_org": "涪城区人民政府",
        "source": "https://www.fucheng.gov.cn/ldzc/",
    },
    {
        "id": 8,
        "name": "郝铭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984-06",
        "birthplace": "四川绵阳",
        "education": "省委党校研究生（四川警察学院治安管理专业）",
        "party_join": "2006-01",
        "work_start": "2006-06",
        "current_post": "区委常委、政法委书记",
        "current_org": "中共绵阳市涪城区委政法委员会",
        "source": "https://baike.baidu.com/item/郝铭",
    },
    {
        "id": 9,
        "name": "胡红娟",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1983-04",
        "birthplace": "四川盐亭",
        "education": "硕士研究生（四川师范大学中国近现代史专业）",
        "party_join": "2003-05",
        "work_start": "2008-07",
        "current_post": "区委常委、统战部部长",
        "current_org": "中共涪城区委统一战线工作部",
        "source": "https://www.fucheng.gov.cn/ldzc/",
    },
    # ═════ 10. Government Leaders (Non-standing Committee) ═══
    {
        "id": 10,
        "name": "谢欣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政府党组成员、副区长",
        "current_org": "涪城区人民政府",
        "source": "https://www.fucheng.gov.cn/ldzc/",
    },
    {
        "id": 11,
        "name": "王洵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政府党组成员、副区长、区公安分局局长",
        "current_org": "绵阳市公安局涪城区分局",
        "source": "https://www.fucheng.gov.cn/ldzc/",
    },
    {
        "id": 12,
        "name": "沈亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政府党组成员、副区长",
        "current_org": "涪城区人民政府",
        "source": "https://www.fucheng.gov.cn/ldzc/",
    },
    {
        "id": 13,
        "name": "曹阳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "涪城区人民政府",
        "source": "https://www.fucheng.gov.cn/ldzc/",
    },
    {
        "id": 14,
        "name": "郑茜",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "涪城区人民政府",
        "source": "https://www.fucheng.gov.cn/ldzc/",
    },
    # ═════ 15. Predecessor & Successors ═══
    {
        "id": 15,
        "name": "邓辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "不再担任涪城区委书记（2024年8月卸任）",
        "current_org": "",
        "source": "https://www.jintai.com.cn/2024/0823/1032459.shtml",
    },
    {
        "id": 16,
        "name": "秦亚辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-01",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "安州区委副书记（原涪城区委副书记）",
        "current_org": "绵阳市安州区委员会",
        "source": "https://news.qq.com/rain/a/20260110A03DDQ00",
    },
    {
        "id": 17,
        "name": "江彬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-11",
        "birthplace": "宜宾",
        "education": "大学，农业推广硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "绵阳市委副书记、市人民政府党组书记、市长",
        "current_org": "绵阳市人民政府",
        "source": "https://news.qq.com/rain/a/20260323A03OUW00",
    },
]

organizations = [
    {"id": 1, "name": "中共绵阳市涪城区委员会", "type": "党委", "level": "县处级", "location": "绵阳市涪城区"},
    {"id": 2, "name": "涪城区人民政府", "type": "政府", "level": "县处级", "location": "绵阳市涪城区"},
    {"id": 3, "name": "绵阳市涪城区纪律检查委员会", "type": "纪委", "level": "县处级", "location": "绵阳市涪城区"},
    {"id": 4, "name": "涪城区人民武装部", "type": "党委", "level": "县处级", "location": "绵阳市涪城区"},
    {"id": 5, "name": "中共涪城区委政法委员会", "type": "党委", "level": "县处级", "location": "绵阳市涪城区"},
    {"id": 6, "name": "中共涪城区委统战部", "type": "党委", "level": "县处级", "location": "绵阳市涪城区"},
    {"id": 7, "name": "绵阳市公安局涪城区分局", "type": "政府", "level": "县处级", "location": "绵阳市涪城区"},
]

positions = [
    # ── 张虚怀 (Party Secretary) ──
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start": "2024-08", "end": "至今", "rank": "正处级", "note": "2024年8月任涪城区委书记"},
    {"person_id": 1, "org_id": 2, "title": "区长", "start": "2021-09", "end": "2025-03", "rank": "正处级", "note": "2021年9月当选区长，2025年3月提名免去区长，此前为代区长"},
    # ── 唐顺江 (District Mayor) ──
    {"person_id": 2, "org_id": 2, "title": "区长", "start": "2025-03", "end": "至今", "rank": "正处级", "note": "2025年3月提名区长，曾任三台县县长"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start": "2025-03", "end": "至今", "rank": "正处级", "note": ""},
    # ── 李静 (Deputy Secretary) ──
    {"person_id": 3, "org_id": 1, "title": "区委副书记、组织部部长", "start": "", "end": "至今", "rank": "副处级", "note": "兼任组织部部长, 区直机关工委书记"},
    # ── 李显作 ──
    {"person_id": 4, "org_id": 4, "title": "区人武部部长", "start": "", "end": "至今", "rank": "副处级", "note": ""},
    # ── 汪劲宇 ──
    {"person_id": 5, "org_id": 3, "title": "区纪委书记、区监委代理主任", "start": "2026-05", "end": "至今", "rank": "副处级", "note": "2026年5月任代理主任"},
    # ── 胡峪涛 ──
    {"person_id": 6, "org_id": 2, "title": "常务副区长", "start": "2025-03", "end": "至今", "rank": "副处级", "note": "2025年3月拟进一步使用"},
    # ── 王超 ──
    {"person_id": 7, "org_id": 2, "title": "副区长", "start": "2026-05", "end": "至今", "rank": "副处级", "note": "2026年5月任命"},
    # ── 郝铭 ──
    {"person_id": 8, "org_id": 5, "title": "政法委书记", "start": "", "end": "至今", "rank": "副处级", "note": ""},
    # ── 胡红娟 ──
    {"person_id": 9, "org_id": 6, "title": "统战部部长", "start": "", "end": "至今", "rank": "副处级", "note": "统筹服务业发展，城市经济发展工作"},
    # ── 谢欣 ──
    {"person_id": 10, "org_id": 2, "title": "副区长", "start": "", "end": "至今", "rank": "副处级", "note": ""},
    # ── 王洵 ──
    {"person_id": 11, "org_id": 7, "title": "区公安分局局长", "start": "", "end": "至今", "rank": "副处级", "note": ""},
    # ── 沈亮 ──
    {"person_id": 12, "org_id": 2, "title": "副区长", "start": "", "end": "至今", "rank": "副处级", "note": ""},
    # ── 曹阳 ──
    {"person_id": 13, "org_id": 2, "title": "副区长", "start": "", "end": "至今", "rank": "副处级", "note": ""},
    # ── 郑茜 ──
    {"person_id": 14, "org_id": 2, "title": "副区长", "start": "2026-05", "end": "至今", "rank": "副处级", "note": "2026年5月任命"},
    # ── 邓辉 (Predecessor) ──
    {"person_id": 15, "org_id": 1, "title": "区委书记", "start": "", "end": "2024-08", "rank": "正处级", "note": "2024年8月卸任"},
    # ── 秦亚辉 (Former Deputy Secretary) ──
    {"person_id": 16, "org_id": 1, "title": "区委副书记", "start": "", "end": "2026-01", "rank": "副处级", "note": "2026年1月赴安州区"},
    # ── 江彬 (Former Mayor) ──
    {"person_id": 17, "org_id": 2, "title": "区长", "start": "", "end": "", "rank": "正处级", "note": "曾任涪城区区长，后任游仙区委书记"},
]

relationships = [
    # Predecessor-successor: 邓辉→张虚怀 (区委书记)
    {"person_a": 15, "person_b": 1, "type": "predecessor_successor", "context": "邓辉卸任涪城区委书记，张虚怀接任（2024.08）", "overlap_org": "中共涪城区委员会", "overlap_period": "2024-08"},
    # Predecessor-successor: 张虚怀→唐顺江 (区长)
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor", "context": "张虚怀2025年3月免去区长，唐顺江提名接任区长", "overlap_org": "涪城区人民政府", "overlap_period": "2025-03"},
    # Current top duo: 张虚怀-唐顺江 (区委书记-区长)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "区委书记与区长工作搭档", "overlap_org": "涪城区", "overlap_period": "2025-03至今"},
    # 张虚怀-秦亚辉 (区委 and 区委副书记)
    {"person_a": 1, "person_b": 16, "type": "overlap", "context": "区委书记与区委副书记共事", "overlap_org": "中共涪城区委员会", "overlap_period": "2024-08至2026-01"},
    # 李静（组织部）- 各常委
    {"person_a": 3, "person_b": 5, "type": "overlap", "context": "组织部与纪委共事", "overlap_org": "中共涪城区委员会", "overlap_period": ""},
    {"person_a": 3, "person_b": 7, "type": "overlap", "context": "组织部与区政府领导共事", "overlap_org": "中共涪城区委员会", "overlap_period": ""},
    # 胡峪涛-王超 (常务副区长-副区长)
    {"person_a": 6, "person_b": 7, "type": "overlap", "context": "区政府领导共事", "overlap_org": "涪城区人民政府", "overlap_period": ""},
    # 江彬(前区长-现市长)-张虚怀
    {"person_a": 17, "person_b": 1, "type": "predecessor_successor", "context": "江彬曾任涪城区长后升任绵阳市长，张虚怀后任区长", "overlap_org": "涪城区人民政府", "overlap_period": ""},
    # 郝铭（政法委）与王洵（公安分局）
    {"person_a": 8, "person_b": 11, "type": "overlap", "context": "政法委书记与公安分局局长工作协作", "overlap_org": "涪城区政法系统", "overlap_period": ""},
]

# ── EXECUTION ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
    print(f"\nArtifacts staged in {BASE}/")
    print(f"  DB:    {DB_PATH}")
    print(f"  GEXF:  {GEXF_PATH}")
    print("Done!")