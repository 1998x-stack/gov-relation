#!/usr/bin/env python3
"""Build 互助土族自治县 leadership network database and GEXF graph."""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path

# Ensure the project root is on sys.path so gov_relation can be imported
_HERE = Path(__file__).resolve().parent
_PROJECT_ROOT = (_HERE / "../../..").resolve()
sys.path.insert(0, str(_PROJECT_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "互助土族自治县"

DB_PATH = _HERE / f"{SLUG}_network.db"
GEXF_PATH = _HERE / f"{SLUG}_network.gexf"

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------

persons = [
    # --- Top leaders ---
    {
        "id": 1,
        "name": "萨尔娜",
        "gender": "女",
        "ethnicity": "待查(疑似蒙古族/土族)",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "县委书记",
        "current_org": "中共互助县委",
        "source": "https://www.huzhu.gov.cn/info/1005/86340.htm",
    },
    {
        "id": 2,
        "name": "朱育海",
        "gender": "男",
        "ethnicity": "土族",
        "birth": "1977年9月",
        "birthplace": "青海省(待查)",
        "education": "中央党校大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委副书记、县长",
        "current_org": "互助县人民政府",
        "source": "https://www.huzhu.gov.cn/info/1036/69147.htm",
    },
    # --- 县委副书记 ---
    {
        "id": 3,
        "name": "石建军",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "县委副书记、教育工作领导小组组长",
        "current_org": "中共互助县委",
        "source": "https://www.huzhu.gov.cn/info/1005/84383.htm",
    },
    {
        "id": 4,
        "name": "田林海",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "县委副书记",
        "current_org": "中共互助县委",
        "source": "https://www.huzhu.gov.cn/info/1005/86340.htm",
    },
    # --- 县委常委 ---
    {
        "id": 5,
        "name": "时盛利",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年2月",
        "birthplace": "青海乐都",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委常委、副县长",
        "current_org": "互助县人民政府",
        "source": "https://www.huzhu.gov.cn/info/1036/56435.htm",
    },
    {
        "id": 6,
        "name": "谢振胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年1月",
        "birthplace": "江西于都",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委常委、副县长(挂职)",
        "current_org": "互助县人民政府",
        "source": "https://www.huzhu.gov.cn/info/1036/59008.htm",
    },
    {
        "id": 7,
        "name": "魏胜业",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共互助县委",
        "source": "https://www.huzhu.gov.cn/info/1005/86340.htm",
    },
    {
        "id": 8,
        "name": "苏成福",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "县委常委、县纪委书记、监委主任",
        "current_org": "中共互助县纪律检查委员会",
        "source": "https://www.huzhu.gov.cn/info/1005/86340.htm",
    },
    # --- 县政府副县长 ---
    {
        "id": 9,
        "name": "丁莹",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1982年11月",
        "birthplace": "青海西宁",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副县长",
        "current_org": "互助县人民政府",
        "source": "https://www.huzhu.gov.cn/info/1036/17524.htm",
    },
    {
        "id": 10,
        "name": "杨启林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年2月",
        "birthplace": "青海互助",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副县长",
        "current_org": "互助县人民政府",
        "source": "https://www.huzhu.gov.cn/info/1036/17525.htm",
    },
    {
        "id": 11,
        "name": "师存锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年10月",
        "birthplace": "青海互助",
        "education": "大学本科学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副县长",
        "current_org": "互助县人民政府",
        "source": "https://www.huzhu.gov.cn/info/1036/65449.htm",
    },
    {
        "id": 12,
        "name": "吴鸿强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年8月",
        "birthplace": "青海乐都",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副县长、县公安局局长",
        "current_org": "互助县公安局",
        "source": "https://www.huzhu.gov.cn/info/1036/45372.htm",
    },
    {
        "id": 13,
        "name": "侯恩奇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985年5月",
        "birthplace": "山东曹县",
        "education": "大学本科学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副县长(挂职)",
        "current_org": "互助县人民政府",
        "source": "https://www.huzhu.gov.cn/info/1036/83247.htm",
    },
    {
        "id": 14,
        "name": "石成鹏",
        "gender": "男",
        "ethnicity": "土族",
        "birth": "1979年12月",
        "birthplace": "青海海东",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副县长",
        "current_org": "互助县人民政府",
        "source": "https://www.huzhu.gov.cn/info/1036/56434.htm",
    },
    # --- 其他县领导(角色待确认) ---
    {
        "id": 15,
        "name": "多巴",
        "gender": "待查",
        "ethnicity": "待查(疑似藏族/土族)",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "县领导(角色待确认)",
        "current_org": "互助县",
        "source": "https://www.huzhu.gov.cn/info/1005/84383.htm",
    },
    {
        "id": 16,
        "name": "侯元秀",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "县领导(角色待确认)",
        "current_org": "互助县",
        "source": "https://www.huzhu.gov.cn/info/1005/84383.htm",
    },
    {
        "id": 17,
        "name": "刘宝尧",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "县领导(角色待确认)",
        "current_org": "互助县",
        "source": "https://www.huzhu.gov.cn/info/1005/84383.htm",
    },
]

organizations = [
    {"id": 1, "name": "中共互助县委", "type": "党委", "level": "县级", "parent": "中共海东市委", "location": "青海省海东市互助县"},
    {"id": 2, "name": "互助县人民政府", "type": "政府", "level": "县级", "parent": "海东市人民政府", "location": "青海省海东市互助县"},
    {"id": 3, "name": "互助县纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共互助县委", "location": "青海省海东市互助县"},
    {"id": 4, "name": "互助县委组织部", "type": "党委", "level": "县级", "parent": "中共互助县委", "location": "青海省海东市互助县"},
    {"id": 5, "name": "互助县委教育工作领导小组", "type": "党委", "level": "县级", "parent": "中共互助县委", "location": "青海省海东市互助县"},
    {"id": 6, "name": "互助县公安局", "type": "政府", "level": "县级", "parent": "互助县人民政府", "location": "青海省海东市互助县"},
    {"id": 7, "name": "互助县人大", "type": "人大", "level": "县级", "parent": "海东市人大", "location": "青海省海东市互助县"},
    {"id": 8, "name": "互助县政协", "type": "政协", "level": "县级", "parent": "海东市政协", "location": "青海省海东市互助县"},
]

positions = [
    # 萨尔娜
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "待查", "end_date": "现任", "rank": "正县级", "note": "主持县委全面工作"},
    # 朱育海
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "待查", "end_date": "现任", "rank": "正县级", "note": "主持县政府全面工作"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "待查", "end_date": "现任", "rank": "副县级", "note": ""},
    # 石建军
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start_date": "待查", "end_date": "现任", "rank": "副县级", "note": "兼任教育工作领导小组组长"},
    {"person_id": 3, "org_id": 5, "title": "教育工作领导小组组长", "start_date": "待查", "end_date": "现任", "rank": "副县级", "note": ""},
    # 田林海
    {"person_id": 4, "org_id": 1, "title": "县委副书记", "start_date": "待查", "end_date": "现任", "rank": "副县级", "note": "分管领域见相关会议报道"},
    # 时盛利
    {"person_id": 5, "org_id": 2, "title": "副县长", "start_date": "待查", "end_date": "现任", "rank": "副县级", "note": "负责发改、数据、应急、财政等"},
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start_date": "待查", "end_date": "现任", "rank": "副县级", "note": ""},
    # 谢振胜
    {"person_id": 6, "org_id": 2, "title": "副县长(挂职)", "start_date": "待查", "end_date": "现任", "rank": "副县级", "note": "东西部协作挂职，负责广播电视"},
    {"person_id": 6, "org_id": 1, "title": "县委常委(挂职)", "start_date": "待查", "end_date": "现任", "rank": "副县级", "note": ""},
    # 魏胜业
    {"person_id": 7, "org_id": 4, "title": "组织部部长", "start_date": "待查", "end_date": "现任", "rank": "副县级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start_date": "待查", "end_date": "现任", "rank": "副县级", "note": ""},
    # 苏成福
    {"person_id": 8, "org_id": 3, "title": "县纪委书记、监委主任", "start_date": "待查", "end_date": "现任", "rank": "副县级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start_date": "待查", "end_date": "现任", "rank": "副县级", "note": ""},
    # 丁莹
    {"person_id": 9, "org_id": 2, "title": "副县长", "start_date": "待查", "end_date": "现任", "rank": "副县级", "note": "负责土族故土园、卫健、文旅、教育、医保"},
    # 杨启林
    {"person_id": 10, "org_id": 2, "title": "副县长", "start_date": "待查", "end_date": "现任", "rank": "副县级", "note": "负责人社、民政、工业、交通、市场监管"},
    # 师存锋
    {"person_id": 11, "org_id": 2, "title": "副县长", "start_date": "待查", "end_date": "现任", "rank": "副县级", "note": "负责自然资源、农业农村、水利、林草、乡村振兴"},
    # 吴鸿强
    {"person_id": 12, "org_id": 2, "title": "副县长", "start_date": "待查", "end_date": "现任", "rank": "副县级", "note": "负责公安、司法、信访、退役军人"},
    {"person_id": 12, "org_id": 6, "title": "县公安局局长", "start_date": "待查", "end_date": "现任", "rank": "副县级", "note": ""},
    # 侯恩奇
    {"person_id": 13, "org_id": 2, "title": "副县长(挂职)", "start_date": "待查", "end_date": "现任", "rank": "副县级", "note": "挂职，负责市场监管、供销合作"},
    # 石成鹏
    {"person_id": 14, "org_id": 2, "title": "副县长", "start_date": "待查", "end_date": "现任", "rank": "副县级", "note": "负责住建、城管、生态环保、临空经济区"},
    # 多巴 (角色待确认)
    {"person_id": 15, "org_id": 1, "title": "县领导(角色待确认)", "start_date": "待查", "end_date": "现任", "rank": "县级", "note": "出现在县领导名单中，具体职务待确认"},
    # 侯元秀 (角色待确认)
    {"person_id": 16, "org_id": 1, "title": "县领导(角色待确认)", "start_date": "待查", "end_date": "现任", "rank": "县级", "note": "出现在县领导名单中，具体职务待确认"},
    # 刘宝尧 (角色待确认)
    {"person_id": 17, "org_id": 1, "title": "县领导(角色待确认)", "start_date": "待查", "end_date": "现任", "rank": "县级", "note": "出现在县领导名单中，具体职务待确认"},
]

relationships = [
    # 萨尔娜 ↔ 朱育海 (党政一把手搭档)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "县委书记与县长党政搭档", "overlap_org": "中共互助县委/互助县人民政府", "overlap_period": "现任"},
    # 萨尔娜 ↔ 石建军 (上下级关系)
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县委书记与专职副书记", "overlap_org": "中共互助县委", "overlap_period": "现任"},
    # 萨尔娜 ↔ 田林海 (上下级关系)
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "县委书记与县委副书记", "overlap_org": "中共互助县委", "overlap_period": "现任"},
    # 朱育海 ↔ 时盛利 (上下级-协助县长工作)
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "县长与常务副县长", "overlap_org": "互助县人民政府", "overlap_period": "现任"},
    # 朱育海 ↔ 石成鹏 (上下级)
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "互助县人民政府", "overlap_period": "现任"},
    # 魏胜业 ↔ 苏成福 (常委同僚)
    {"person_a": 7, "person_b": 8, "type": "overlap", "context": "县委常委同僚", "overlap_org": "中共互助县委", "overlap_period": "现任"},
    # 师存锋 ↔ 杨启林 (副县长同僚，均本地成长)
    {"person_a": 11, "person_b": 10, "type": "overlap", "context": "副县长同僚，均为互助本地人", "overlap_org": "互助县人民政府", "overlap_period": "现任"},
    # 谢振胜 ↔ 侯恩奇 (挂职副县长同僚)
    {"person_a": 6, "person_b": 13, "type": "overlap", "context": "挂职副县长同僚", "overlap_org": "互助县人民政府", "overlap_period": "现任"},
]


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

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
    print(f"Done. DB: {DB_PATH}, GEXF: {GEXF_PATH}")
