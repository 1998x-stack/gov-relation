#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
德庆县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 广东省
Parent City: 肇庆市
Region: 德庆县
Targets: 县委书记 & 县长

Research Sources:
- Baidu Baike: 德庆县词条 — 黎晓、伍剑伟、周间仪、孙燕鹏、廖建洪（confirmed）
- Baidu Baike: 黎晓词条（item/黎晓/20319066）— 完整履历（confirmed）
- Baidu Baike: 伍剑伟词条（item/伍剑伟/23485286）— 身份信息（confirmed）
- 德庆县政府门户网站 (www.gddq.gov.cn) — 领导之窗页面（confirmed via librarian agent）
- 德庆县政府新闻页面 — 各类会议报道（confirmed via librarian agent）

Current status (as of 2026-07-22):
- 县委书记: 黎晓（confirmed from Baidu Baike & gov website, since at least Jan 2026）
- 县长: 伍剑伟（confirmed from Baidu Baike & gov website, since at least Jan 2023）
- 常务副县长: 张周兴
- 县委常委、组织部长: 陈善军
- 县委常委、宣传部长: 罗有茂
- 县委常委、纪委书记: 李军
- 县人大常委会主任: 张建球
- 县政协主席: 简文英

Research Date: 2026-07-22

Note: 周间仪、廖建洪 may no longer be in office as of 2026 (not on current gov website leadership page)
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
import sqlite3  # noqa: F401 — keep import for process_tmp.py detection

# ── Slug & Paths (for staging) ──
SLUG = "德庆县"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

# ── Data ──

# 1. Persons
persons = [
    # ═══════════════════ 县委领导 ═══════════
    {
        "id": 1,
        "name": "黎晓",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1976年3月",
        "birthplace": "广东省肇庆市",
        "native_place": "广东省肇庆市",
        "education": "函授大学（华中师范大学网络教育学院汉语言文学专业）",
        "party_join": "1995年5月",
        "work_start": "1996年7月",
        "current_post": "中共德庆县委书记、县人武部党委第一书记",
        "current_org": "中共德庆县委员会",
        "source": "Confirmed from Baidu Baike (item/黎晓/20319066) & gov website news."
    },
    {
        "id": 2,
        "name": "伍剑伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年4月",
        "birthplace": "广东高要",
        "native_place": "广东高要",
        "education": "大学本科（中山大学毕业）",
        "party_join": "2007年6月",
        "work_start": "1999年7月",
        "current_post": "中共德庆县委副书记、县政府党组书记、县长",
        "current_org": "德庆县人民政府",
        "source": "Confirmed from Baidu Baike & gov website. In office since at least Jan 2023."
    },
    # ═══ 县委常委 ═══
    {
        "id": 3,
        "name": "张周兴",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年11月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "德庆县委常委、常务副县长",
        "current_org": "德庆县人民政府",
        "source": "Confirmed from gov website leadership page."
    },
    {
        "id": 4,
        "name": "陈善军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "德庆县委常委、组织部部长",
        "current_org": "中共德庆县委组织部",
        "source": "Confirmed from gov website news (2026-07)."
    },
    {
        "id": 5,
        "name": "罗有茂",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "德庆县委常委、宣传部部长",
        "current_org": "中共德庆县委宣传部",
        "source": "Confirmed from gov website news (2026-06-24)."
    },
    {
        "id": 6,
        "name": "李军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "德庆县委常委、纪委书记、县监委主任",
        "current_org": "中共德庆县纪律检查委员会",
        "source": "Confirmed from gov website news (2026-01)."
    },
    # ═══ 县政府领导 ═══
    {
        "id": 7,
        "name": "肖尊明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年10月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "硕士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "德庆县副县长",
        "current_org": "德庆县人民政府",
        "source": "Confirmed from gov website. 分管卫健、医保、市场监管."
    },
    {
        "id": 8,
        "name": "梁衍光",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年12月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "德庆县副县长",
        "current_org": "德庆县人民政府",
        "source": "Confirmed from gov website. 分管农业农村、水利、林业、乡村振兴."
    },
    {
        "id": 9,
        "name": "许亦光",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年6月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "德庆县副县长、县公安局局长",
        "current_org": "德庆县公安局",
        "source": "Confirmed from gov website. 分管公安、信访、维稳."
    },
    {
        "id": 10,
        "name": "范梦婷",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1988年3月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "德庆县副县长",
        "current_org": "德庆县人民政府",
        "source": "Confirmed from gov website. 分管教育、民政、残联. 2026年7月最新任命."
    },
    {
        "id": 11,
        "name": "欧立欢",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年11月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "德庆县副县长",
        "current_org": "德庆县人民政府",
        "source": "Confirmed from gov website. 分管工信、商务、环保、工业园区."
    },
    {
        "id": 12,
        "name": "孙燕鹏",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1986年9月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "德庆县副县长（挂职）",
        "current_org": "德庆县人民政府",
        "source": "Confirmed from gov website. 协助乡村振兴、招商."
    },
    # ═══ 人大、政协 ═══
    {
        "id": 13,
        "name": "张建球",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "德庆县人大常委会主任",
        "current_org": "德庆县人民代表大会常务委员会",
        "source": "Confirmed from gov website news (2026-01 人大会议)."
    },
    {
        "id": 14,
        "name": "简文英",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "德庆县政协主席",
        "current_org": "中国人民政治协商会议德庆县委员会",
        "source": "Confirmed from gov website news (2026-01 纪委全会)."
    },
]

# 2. Organizations
organizations = [
    {"id": 1, "name": "中共德庆县委员会", "type": "党委", "level": "县级", "parent": "中共肇庆市委员会", "location": "广东省肇庆市德庆县"},
    {"id": 2, "name": "德庆县人民政府", "type": "政府", "level": "县级", "parent": "肇庆市人民政府", "location": "广东省肇庆市德庆县"},
    {"id": 3, "name": "德庆县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "肇庆市人民代表大会常务委员会", "location": "广东省肇庆市德庆县"},
    {"id": 4, "name": "中国人民政治协商会议德庆县委员会", "type": "政协", "level": "县级", "parent": "中国人民政治协商会议肇庆市委员会", "location": "广东省肇庆市德庆县"},
    {"id": 5, "name": "中共德庆县纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共德庆县委员会", "location": "广东省肇庆市德庆县"},
    {"id": 6, "name": "中共德庆县委组织部", "type": "党委", "level": "县级", "parent": "中共德庆县委员会", "location": "广东省肇庆市德庆县"},
    {"id": 7, "name": "中共德庆县委宣传部", "type": "党委", "level": "县级", "parent": "中共德庆县委员会", "location": "广东省肇庆市德庆县"},
    {"id": 8, "name": "德庆县公安局", "type": "政府", "level": "县级", "parent": "德庆县人民政府", "location": "广东省肇庆市德庆县"},
    {"id": 9, "name": "德庆县审计局", "type": "政府", "level": "县级", "parent": "德庆县人民政府", "location": "广东省肇庆市德庆县"},
    {"id": 10, "name": "德庆县官圩镇人民政府", "type": "政府", "level": "乡镇级", "parent": "德庆县人民政府", "location": "广东省肇庆市德庆县官圩镇"},
    {"id": 11, "name": "中共端州区纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共肇庆市纪律检查委员会", "location": "广东省肇庆市端州区"},
    {"id": 12, "name": "肇庆市端州区黄岗镇人民政府", "type": "政府", "level": "乡镇级", "parent": "端州区人民政府", "location": "广东省肇庆市端州区"},
    {"id": 13, "name": "端州区城西街道办事处", "type": "政府", "level": "乡镇级", "parent": "端州区人民政府", "location": "广东省肇庆市端州区"},
    {"id": 14, "name": "端州区人民政府", "type": "政府", "level": "县级", "parent": "肇庆市人民政府", "location": "广东省肇庆市端州区"},
    {"id": 15, "name": "肇庆市信访局", "type": "政府", "level": "地市级", "parent": "肇庆市人民政府", "location": "广东省肇庆市"},
    {"id": 16, "name": "中共肇庆市委社会工作部", "type": "党委", "level": "地市级", "parent": "中共肇庆市委员会", "location": "广东省肇庆市"},
]

# 3. Positions
positions = [
    # 黎晓
    {"person_id": 1, "org_id": 11, "title": "端州区纪委科员", "start_date": "1996年7月", "end_date": "2002年3月", "rank": "科员", "note": "其间: 1998.06-1999.06 挂任端州区黄岗镇厚岗管理区党支部副书记"},
    {"person_id": 1, "org_id": 11, "title": "端州区纪委宣教调研室副主任", "start_date": "2002年3月", "end_date": "2006年8月", "rank": "副股级", "note": ""},
    {"person_id": 1, "org_id": 12, "title": "端州区黄岗镇镇委委员", "start_date": "2006年8月", "end_date": "2007年9月", "rank": "副科级", "note": ""},
    {"person_id": 1, "org_id": 12, "title": "端州区黄岗镇镇委委员、妇联主席", "start_date": "2007年9月", "end_date": "2010年4月", "rank": "副科级", "note": ""},
    {"person_id": 1, "org_id": 12, "title": "端州区黄岗镇委委员、纪委书记、妇联主席", "start_date": "2010年4月", "end_date": "2010年10月", "rank": "副科级", "note": ""},
    {"person_id": 1, "org_id": 13, "title": "端州区黄岗街道党工委委员、纪委书记、妇联主席", "start_date": "2010年10月", "end_date": "2011年3月", "rank": "副科级", "note": "其间: 2008.09-2011.01 华中师范大学网络教育学院汉语言文学专业学习"},
    {"person_id": 1, "org_id": 13, "title": "端州区城西街道党工委副书记、办事处主任", "start_date": "2011年3月", "end_date": "2012年4月", "rank": "正科级", "note": ""},
    {"person_id": 1, "org_id": 13, "title": "端州区城西街道党工委书记、综治委主任", "start_date": "2012年4月", "end_date": "2016年9月", "rank": "正科级", "note": "期间挂任肇庆市商务局局长助理、珠海市香洲区前山街道书记助理"},
    {"person_id": 1, "org_id": 14, "title": "端州区政府副区长（兼城西街道书记）", "start_date": "2016年9月", "end_date": "2016年11月", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 14, "title": "端州区政府副区长、党组成员", "start_date": "2016年11月", "end_date": "2022年3月", "rank": "副处级", "note": ""},
    {"person_id": 1, "org_id": 15, "title": "肇庆市信访局（具体职务待确认）", "start_date": "2022年3月", "end_date": "2024年11月", "rank": "待查", "note": ""},
    {"person_id": 1, "org_id": 16, "title": "肇庆市委社会工作部部长、市委两新工委书记、市政府副秘书长", "start_date": "约2024年11月", "end_date": "约2025年", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "中共德庆县委书记、县人武部党委第一书记", "start_date": "约2025年", "end_date": "现在", "rank": "正处级", "note": "2026年1月28日任县人武部党委第一书记"},
    # 伍剑伟
    {"person_id": 2, "org_id": 2, "title": "德庆县县长", "start_date": "至少2023年1月", "end_date": "现在", "rank": "正处级", "note": "主持县政府全面工作；分管审计局；挂点官圩镇"},
    {"person_id": 2, "org_id": 1, "title": "德庆县委副书记", "start_date": "至少2023年1月", "end_date": "现在", "rank": "副处级", "note": ""},
    # 张周兴
    {"person_id": 3, "org_id": 2, "title": "德庆县常务副县长", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": "分管发改、财政、应急、自然资源"},
    {"person_id": 3, "org_id": 1, "title": "德庆县委常委", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},
    # 陈善军
    {"person_id": 4, "org_id": 6, "title": "德庆县委组织部部长", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "德庆县委常委", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},
    # 罗有茂
    {"person_id": 5, "org_id": 7, "title": "德庆县委宣传部部长", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "德庆县委常委", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},
    # 李军
    {"person_id": 6, "org_id": 5, "title": "德庆县纪委书记、监委主任", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "德庆县委常委", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},
    # 肖尊明
    {"person_id": 7, "org_id": 2, "title": "德庆县副县长", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": "分管卫健、医保、市场监管"},
    # 梁衍光
    {"person_id": 8, "org_id": 2, "title": "德庆县副县长", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": "分管农业农村、水利、林业、乡村振兴"},
    # 许亦光
    {"person_id": 9, "org_id": 2, "title": "德庆县副县长", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": "分管公安、信访、维稳"},
    {"person_id": 9, "org_id": 8, "title": "德庆县公安局局长", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": ""},
    # 范梦婷
    {"person_id": 10, "org_id": 2, "title": "德庆县副县长", "start_date": "2026年7月", "end_date": "现在", "rank": "副处级", "note": "分管教育、民政、残联"},
    # 欧立欢
    {"person_id": 11, "org_id": 2, "title": "德庆县副县长", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": "分管工信、商务、环保、工业园区"},
    # 孙燕鹏
    {"person_id": 12, "org_id": 2, "title": "德庆县副县长（挂职）", "start_date": "待查", "end_date": "现在", "rank": "副处级", "note": "协助乡村振兴、招商"},
    # 张建球
    {"person_id": 13, "org_id": 3, "title": "德庆县人大常委会主任", "start_date": "待查", "end_date": "现在", "rank": "正处级", "note": ""},
    # 简文英
    {"person_id": 14, "org_id": 4, "title": "德庆县政协主席", "start_date": "待查", "end_date": "现在", "rank": "正处级", "note": ""},
]

# 4. Relationships
relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记与县长搭档", "overlap_org": "中共德庆县委员会/德庆县人民政府", "overlap_period": "约2025-至今"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县委书记与常务副县长", "overlap_org": "中共德庆县委员会", "overlap_period": "待确认"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "县委书记与组织部长", "overlap_org": "中共德庆县委员会", "overlap_period": "待确认"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "县委书记与宣传部长", "overlap_org": "中共德庆县委员会", "overlap_period": "待确认"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "县委书记与纪委书记", "overlap_org": "中共德庆县委员会", "overlap_period": "待确认"},
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "县长与常务副县长", "overlap_org": "德庆县人民政府", "overlap_period": "待确认"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "德庆县人民政府", "overlap_period": "待确认"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "德庆县人民政府", "overlap_period": "待确认"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "县长与公安局长", "overlap_org": "德庆县人民政府", "overlap_period": "待确认"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "德庆县人民政府", "overlap_period": "2026年7月-至今"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "德庆县人民政府", "overlap_period": "待确认"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "县长与挂职副县长", "overlap_org": "德庆县人民政府", "overlap_period": "待确认"},
    {"person_a": 1, "person_b": 13, "type": "overlap", "context": "县委书记与人大主任", "overlap_org": "德庆县四套班子", "overlap_period": "待确认"},
    {"person_a": 1, "person_b": 14, "type": "overlap", "context": "县委书记与政协主席", "overlap_org": "德庆县四套班子", "overlap_period": "待确认"},
]


if __name__ == "__main__":
    db = DB_PATH
    gexf = GEXF_PATH
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=db,
        gexf_path=gexf,
        overwrite=True,
    )
    print(f"\nDone. Database: {db}")
    print(f"GEXF: {gexf}")
