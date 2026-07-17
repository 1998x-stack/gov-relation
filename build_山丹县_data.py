#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 山丹县 (Shandan County, Zhangye, Gansu).

Task: gansu_山丹县 — 县委书记 & 县长
Province: 甘肃省
City: 张掖市
Region: 山丹县
Level: 县
Research date: 2026-07-17

Confirmed officeholders (as of 2026-07-17, from www.shandan.gov.cn 领导之窗):
- 县委书记: 张伟 (Zhang Wei)
- 县委副书记、县长: 黄国杰 (Huang Guojie)
- 县委副书记: 李发荣

县委常委:
- 郭强 (also 常务副县长)
- 高积鑫 (also 副县长)
- 赵学涛
- 安伟
- 曹海霞
- 张永盛
- 钱述华
- 展宏宙
- 杨从军 (also 副县长)

县政府:
- 县长: 黄国杰
- 副县长: 郭强, 高积鑫, 杨从军, 张剑波, 李辉, 石晶, 张克孟

县人大:
- 主任: 周祖国
- 副主任: 赵文成, 杜万善, 车明国, 李秀琴

县政协:
- 主席: 鲁维俭
- 副主席: 唐谦, 王雪云, 李凤武, 何跃

Sources:
- www.shandan.gov.cn (山丹县人民政府官网领导之窗), accessed 2026-07-17
- Various news reports and public records

Confidence: Leadership roster confirmed from official government website.
Career details for most figures are limited — full career histories mostly not found.
Marked gaps explicitly.
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ──────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
GOV_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))  # gov-relation/
DB_PATH = os.path.join(SCRIPT_DIR, "山丹县_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "山丹县_network.gexf")

TODAY = datetime.now().strftime("%Y-%m-%d")


# ── research data ──────────────────────────────────────────────────────

persons = [
    # ══════════════ Core Leaders ══════════════

    # 县委书记 — 张伟
    {
        "id": "shandan_zhang_wei",
        "name": "张伟",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "山丹县委书记",
        "current_org": "中共山丹县委员会",
        "source": "www.shandan.gov.cn (领导之窗), 2026-07-17",
        "notes": "平级从待查调任山丹县委书记。具体出生年份、履历待进一步查证。",
        "confidence": "confirmed",
    },

    # 县委副书记、县长 — 黄国杰
    {
        "id": "shandan_huang_guojie",
        "name": "黄国杰",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "山丹县委副书记、县长",
        "current_org": "山丹县人民政府",
        "source": "www.shandan.gov.cn (领导之窗), 2026-07-17",
        "notes": "主持县政府全面工作。2026年7月新闻报道显示其主持召开县政府常务会议。履历待查。",
        "confidence": "confirmed",
    },

    # 县委副书记 — 李发荣
    {
        "id": "shandan_li_farong",
        "name": "李发荣",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "山丹县委副书记",
        "current_org": "中共山丹县委员会",
        "source": "www.shandan.gov.cn (领导之窗), 2026-07-17",
        "notes": "县委专职副书记。履历待查。",
        "confidence": "confirmed",
    },

    # ══════════════ 县委常委 ══════════════

    # 郭强 — 县委常委、常务副县长
    {
        "id": "shandan_guo_qiang",
        "name": "郭强",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "山丹县委常委、常务副县长",
        "current_org": "山丹县人民政府",
        "source": "www.shandan.gov.cn (领导之窗), 2026-07-17",
        "notes": "县委常委、常务副县长。履历待查。",
        "confidence": "confirmed",
    },

    # 高积鑫 — 县委常委、副县长
    {
        "id": "shandan_gao_jixin",
        "name": "高积鑫",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "山丹县委常委、副县长",
        "current_org": "山丹县人民政府",
        "source": "www.shandan.gov.cn (领导之窗), 2026-07-17",
        "notes": "县委常委、副县长。履历待查。",
        "confidence": "confirmed",
    },

    # 赵学涛 — 县委常委
    {
        "id": "shandan_zhao_xuetao",
        "name": "赵学涛",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "山丹县委常委",
        "current_org": "中共山丹县委员会",
        "source": "www.shandan.gov.cn (领导之窗), 2026-07-17",
        "notes": "县委常委。具体分管领域待查。",
        "confidence": "confirmed",
    },

    # 安伟 — 县委常委
    {
        "id": "shandan_an_wei",
        "name": "安伟",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "山丹县委常委",
        "current_org": "中共山丹县委员会",
        "source": "www.shandan.gov.cn (领导之窗), 2026-07-17",
        "notes": "县委常委。具体分管领域待查。",
        "confidence": "confirmed",
    },

    # 曹海霞 — 县委常委
    {
        "id": "shandan_cao_haixia",
        "name": "曹海霞",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "山丹县委常委",
        "current_org": "中共山丹县委员会",
        "source": "www.shandan.gov.cn (领导之窗), 2026-07-17",
        "notes": "县委常委。女性领导。具体分管领域待查。",
        "confidence": "confirmed",
    },

    # 张永盛 — 县委常委
    {
        "id": "shandan_zhang_yongsheng",
        "name": "张永盛",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "山丹县委常委",
        "current_org": "中共山丹县委员会",
        "source": "www.shandan.gov.cn (领导之窗), 2026-07-17",
        "notes": "县委常委。具体分管领域待查。",
        "confidence": "confirmed",
    },

    # 钱述华 — 县委常委
    {
        "id": "shandan_qian_shuhua",
        "name": "钱述华",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "山丹县委常委",
        "current_org": "中共山丹县委员会",
        "source": "www.shandan.gov.cn (领导之窗), 2026-07-17",
        "notes": "县委常委。具体分管领域待查。",
        "confidence": "confirmed",
    },

    # 展宏宙 — 县委常委
    {
        "id": "shandan_zhan_hongzhou",
        "name": "展宏宙",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "山丹县委常委",
        "current_org": "中共山丹县委员会",
        "source": "www.shandan.gov.cn (领导之窗), 2026-07-17",
        "notes": "县委常委。具体分管领域待查。",
        "confidence": "confirmed",
    },

    # 杨从军 — 县委常委、副县长
    {
        "id": "shandan_yang_congjun",
        "name": "杨从军",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "山丹县委常委、副县长",
        "current_org": "山丹县人民政府",
        "source": "www.shandan.gov.cn (领导之窗), 2026-07-17",
        "notes": "县委常委、副县长。履历待查。",
        "confidence": "confirmed",
    },

    # ══════════════ 副县长（非县委常委） ══════════════

    # 张剑波 — 副县长
    {
        "id": "shandan_zhang_jianbo",
        "name": "张剑波",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "山丹县副县长",
        "current_org": "山丹县人民政府",
        "source": "www.shandan.gov.cn (领导之窗), 2026-07-17",
        "notes": "副县长。履历待查。",
        "confidence": "confirmed",
    },

    # 李辉 — 副县长
    {
        "id": "shandan_li_hui",
        "name": "李辉",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "山丹县副县长",
        "current_org": "山丹县人民政府",
        "source": "www.shandan.gov.cn (领导之窗), 2026-07-17",
        "notes": "副县长。履历待查。",
        "confidence": "confirmed",
    },

    # 石晶 — 副县长
    {
        "id": "shandan_shi_jing",
        "name": "石晶",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "山丹县副县长",
        "current_org": "山丹县人民政府",
        "source": "www.shandan.gov.cn (领导之窗), 2026-07-17",
        "notes": "副县长。女性领导。履历待查。",
        "confidence": "confirmed",
    },

    # 张克孟 — 副县长
    {
        "id": "shandan_zhang_kemeng",
        "name": "张克孟",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "山丹县副县长",
        "current_org": "山丹县人民政府",
        "source": "www.shandan.gov.cn (领导之窗), 2026-07-17",
        "notes": "副县长。履历待查。",
        "confidence": "confirmed",
    },

    # ══════════════ 人大领导 ══════════════

    # 周祖国 — 人大常委会主任
    {
        "id": "shandan_zhou_zuguo",
        "name": "周祖国",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "山丹县人大常委会主任",
        "current_org": "山丹县人大常委会",
        "source": "www.shandan.gov.cn (领导之窗), 2026-07-17",
        "notes": "人大常委会主任。履历待查。",
        "confidence": "confirmed",
    },

    # 赵文成 — 人大常委会副主任
    {
        "id": "shandan_zhao_wencheng",
        "name": "赵文成",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "山丹县人大常委会副主任",
        "current_org": "山丹县人大常委会",
        "source": "www.shandan.gov.cn (领导之窗), 2026-07-17",
        "notes": "人大常委会副主任。履历待查。",
        "confidence": "confirmed",
    },

    # 杜万善 — 人大常委会副主任
    {
        "id": "shandan_du_wanshan",
        "name": "杜万善",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "山丹县人大常委会副主任",
        "current_org": "山丹县人大常委会",
        "source": "www.shandan.gov.cn (领导之窗), 2026-07-17",
        "notes": "人大常委会副主任。履历待查。",
        "confidence": "confirmed",
    },

    # 车明国 — 人大常委会副主任
    {
        "id": "shandan_che_mingguo",
        "name": "车明国",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "山丹县人大常委会副主任",
        "current_org": "山丹县人大常委会",
        "source": "www.shandan.gov.cn (领导之窗), 2026-07-17",
        "notes": "人大常委会副主任。履历待查。",
        "confidence": "confirmed",
    },

    # 李秀琴 — 人大常委会副主任
    {
        "id": "shandan_li_xiuqin",
        "name": "李秀琴",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "山丹县人大常委会副主任",
        "current_org": "山丹县人大常委会",
        "source": "www.shandan.gov.cn (领导之窗), 2026-07-17",
        "notes": "人大常委会副主任。女性领导。履历待查。",
        "confidence": "confirmed",
    },

    # ══════════════ 政协领导 ══════════════

    # 鲁维俭 — 政协主席
    {
        "id": "shandan_lu_weijian",
        "name": "鲁维俭",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "山丹县政协主席",
        "current_org": "政协山丹县委员会",
        "source": "www.shandan.gov.cn (领导之窗), 2026-07-17",
        "notes": "政协主席。履历待查。",
        "confidence": "confirmed",
    },

    # 唐谦 — 政协副主席
    {
        "id": "shandan_tang_qian",
        "name": "唐谦",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "山丹县政协副主席",
        "current_org": "政协山丹县委员会",
        "source": "www.shandan.gov.cn (领导之窗), 2026-07-17",
        "notes": "政协副主席。履历待查。",
        "confidence": "confirmed",
    },

    # 王雪云 — 政协副主席
    {
        "id": "shandan_wang_xueyun",
        "name": "王雪云",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "山丹县政协副主席",
        "current_org": "政协山丹县委员会",
        "source": "www.shandan.gov.cn (领导之窗), 2026-07-17",
        "notes": "政协副主席。履历待查。",
        "confidence": "confirmed",
    },

    # 李凤武 — 政协副主席
    {
        "id": "shandan_li_fengwu",
        "name": "李凤武",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "山丹县政协副主席",
        "current_org": "政协山丹县委员会",
        "source": "www.shandan.gov.cn (领导之窗), 2026-07-17",
        "notes": "政协副主席。履历待查。",
        "confidence": "confirmed",
    },

    # 何跃 — 政协副主席
    {
        "id": "shandan_he_yue",
        "name": "何跃",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "山丹县政协副主席",
        "current_org": "政协山丹县委员会",
        "source": "www.shandan.gov.cn (领导之窗), 2026-07-17",
        "notes": "政协副主席。履历待查。",
        "confidence": "confirmed",
    },
]

organizations = [
    {"id": "cpc_shandan", "name": "中共山丹县委员会", "type": "党委", "level": "县", "parent": "中共张掖市委员会", "location": "甘肃省张掖市山丹县"},
    {"id": "gov_shandan", "name": "山丹县人民政府", "type": "政府", "level": "县", "parent": "张掖市人民政府", "location": "甘肃省张掖市山丹县"},
    {"id": "npc_shandan", "name": "山丹县人大常委会", "type": "人大", "level": "县", "parent": "", "location": "甘肃省张掖市山丹县"},
    {"id": "cppcc_shandan", "name": "政协山丹县委员会", "type": "政协", "level": "县", "parent": "", "location": "甘肃省张掖市山丹县"},
    {"id": "dis_shandan", "name": "中共山丹县纪律检查委员会", "type": "党委", "level": "县", "parent": "中共张掖市纪律检查委员会", "location": "甘肃省张掖市山丹县"},
    {"id": "org_shandan", "name": "中共山丹县委员会组织部", "type": "党委", "level": "县", "parent": "中共山丹县委员会", "location": "甘肃省张掖市山丹县"},
    {"id": "prop_shandan", "name": "中共山丹县委员会宣传部", "type": "党委", "level": "县", "parent": "中共山丹县委员会", "location": "甘肃省张掖市山丹县"},
    {"id": "ufw_shandan", "name": "中共山丹县委员会统战部", "type": "党委", "level": "县", "parent": "中共山丹县委员会", "location": "甘肃省张掖市山丹县"},
    {"id": "polit_shandan", "name": "中共山丹县委员会政法委员会", "type": "党委", "level": "县", "parent": "中共山丹县委员会", "location": "甘肃省张掖市山丹县"},
    {"id": "psb_shandan", "name": "山丹县公安局", "type": "政府", "level": "县", "parent": "山丹县人民政府", "location": "甘肃省张掖市山丹县"},
    {"id": "cpc_zhangye", "name": "中共张掖市委员会", "type": "党委", "level": "地级", "parent": "中共甘肃省委员会", "location": "甘肃省张掖市"},
    {"id": "gov_zhangye", "name": "张掖市人民政府", "type": "政府", "level": "地级", "parent": "甘肃省人民政府", "location": "甘肃省张掖市"},
]

positions = [
    # 张伟 — 县委书记
    {"person_id": "shandan_zhang_wei", "org_id": "cpc_shandan", "title": "山丹县委书记", "start": "", "end": "present", "rank": "正处级", "note": "主持县委全面工作"},

    # 黄国杰 — 县长
    {"person_id": "shandan_huang_guojie", "org_id": "gov_shandan", "title": "山丹县长", "start": "", "end": "present", "rank": "正处级", "note": "主持县政府全面工作"},
    {"person_id": "shandan_huang_guojie", "org_id": "cpc_shandan", "title": "山丹县委副书记", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 李发荣 — 县委副书记
    {"person_id": "shandan_li_farong", "org_id": "cpc_shandan", "title": "山丹县委副书记", "start": "", "end": "present", "rank": "副处级", "note": "专职副书记"},

    # 郭强 — 县委常委、常务副县长
    {"person_id": "shandan_guo_qiang", "org_id": "cpc_shandan", "title": "山丹县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "shandan_guo_qiang", "org_id": "gov_shandan", "title": "山丹县常务副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 高积鑫 — 县委常委、副县长
    {"person_id": "shandan_gao_jixin", "org_id": "cpc_shandan", "title": "山丹县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "shandan_gao_jixin", "org_id": "gov_shandan", "title": "山丹县副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 赵学涛 — 县委常委
    {"person_id": "shandan_zhao_xuetao", "org_id": "cpc_shandan", "title": "山丹县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 安伟 — 县委常委
    {"person_id": "shandan_an_wei", "org_id": "cpc_shandan", "title": "山丹县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 曹海霞 — 县委常委
    {"person_id": "shandan_cao_haixia", "org_id": "cpc_shandan", "title": "山丹县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 张永盛 — 县委常委
    {"person_id": "shandan_zhang_yongsheng", "org_id": "cpc_shandan", "title": "山丹县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 钱述华 — 县委常委
    {"person_id": "shandan_qian_shuhua", "org_id": "cpc_shandan", "title": "山丹县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 展宏宙 — 县委常委
    {"person_id": "shandan_zhan_hongzhou", "org_id": "cpc_shandan", "title": "山丹县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 杨从军 — 县委常委、副县长
    {"person_id": "shandan_yang_congjun", "org_id": "cpc_shandan", "title": "山丹县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "shandan_yang_congjun", "org_id": "gov_shandan", "title": "山丹县副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 张剑波 — 副县长
    {"person_id": "shandan_zhang_jianbo", "org_id": "gov_shandan", "title": "山丹县副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 李辉 — 副县长
    {"person_id": "shandan_li_hui", "org_id": "gov_shandan", "title": "山丹县副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 石晶 — 副县长
    {"person_id": "shandan_shi_jing", "org_id": "gov_shandan", "title": "山丹县副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 张克孟 — 副县长
    {"person_id": "shandan_zhang_kemeng", "org_id": "gov_shandan", "title": "山丹县副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 人大
    {"person_id": "shandan_zhou_zuguo", "org_id": "npc_shandan", "title": "山丹县人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": "shandan_zhao_wencheng", "org_id": "npc_shandan", "title": "山丹县人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "shandan_du_wanshan", "org_id": "npc_shandan", "title": "山丹县人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "shandan_che_mingguo", "org_id": "npc_shandan", "title": "山丹县人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "shandan_li_xiuqin", "org_id": "npc_shandan", "title": "山丹县人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 政协
    {"person_id": "shandan_lu_weijian", "org_id": "cppcc_shandan", "title": "山丹县政协主席", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": "shandan_tang_qian", "org_id": "cppcc_shandan", "title": "山丹县政协副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "shandan_wang_xueyun", "org_id": "cppcc_shandan", "title": "山丹县政协副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "shandan_li_fengwu", "org_id": "cppcc_shandan", "title": "山丹县政协副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": "shandan_he_yue", "org_id": "cppcc_shandan", "title": "山丹县政协副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
]


# ── Relationship edges ──────────────────────────────────────────────────

relationships = [
    # 张伟 ↔ 黄国杰 (书记↔县长，党政一把手搭档)
    {"person_a": "shandan_zhang_wei", "person_b": "shandan_huang_guojie",
     "type": "superior_subordinate", "strength": "strong",
     "context": "党政一把手搭档，张伟主持县委全面工作，黄国杰主持县政府全面工作",
     "overlap_org": "中共山丹县委员会/山丹县人民政府",
     "overlap_period": "至今", "confidence": "confirmed"},

    # 张伟 ↔ 李发荣 (书记↔副书记)
    {"person_a": "shandan_zhang_wei", "person_b": "shandan_li_farong",
     "type": "superior_subordinate", "strength": "strong",
     "context": "县委正副书记搭档",
     "overlap_org": "中共山丹县委员会",
     "overlap_period": "至今", "confidence": "confirmed"},

    # 黄国杰 ↔ 李发荣 (县长↔副书记)
    {"person_a": "shandan_huang_guojie", "person_b": "shandan_li_farong",
     "type": "overlap", "strength": "strong",
     "context": "县长与专职副书记共同在县委常委会工作",
     "overlap_org": "中共山丹县委员会",
     "overlap_period": "至今", "confidence": "confirmed"},

    # 黄国杰 ↔ 郭强 (县长↔常务副县长)
    {"person_a": "shandan_huang_guojie", "person_b": "shandan_guo_qiang",
     "type": "superior_subordinate", "strength": "strong",
     "context": "县长与常务副县长正副手关系",
     "overlap_org": "山丹县人民政府",
     "overlap_period": "至今", "confidence": "confirmed"},

    # 黄国杰 ↔ 高积鑫 (县长↔副县长)
    {"person_a": "shandan_huang_guojie", "person_b": "shandan_gao_jixin",
     "type": "superior_subordinate", "strength": "strong",
     "context": "县长与副县长正副手关系",
     "overlap_org": "山丹县人民政府",
     "overlap_period": "至今", "confidence": "confirmed"},

    # 黄国杰 ↔ 张剑波 (县长↔副县长)
    {"person_a": "shandan_huang_guojie", "person_b": "shandan_zhang_jianbo",
     "type": "superior_subordinate", "strength": "strong",
     "context": "县长与副县长正副手关系",
     "overlap_org": "山丹县人民政府",
     "overlap_period": "至今", "confidence": "confirmed"},

    # 黄国杰 ↔ 李辉 (县长↔副县长)
    {"person_a": "shandan_huang_guojie", "person_b": "shandan_li_hui",
     "type": "superior_subordinate", "strength": "strong",
     "context": "县长与副县长正副手关系",
     "overlap_org": "山丹县人民政府",
     "overlap_period": "至今", "confidence": "confirmed"},

    # 黄国杰 ↔ 石晶 (县长↔副县长)
    {"person_a": "shandan_huang_guojie", "person_b": "shandan_shi_jing",
     "type": "superior_subordinate", "strength": "strong",
     "context": "县长与副县长正副手关系",
     "overlap_org": "山丹县人民政府",
     "overlap_period": "至今", "confidence": "confirmed"},

    # 黄国杰 ↔ 张克孟 (县长↔副县长)
    {"person_a": "shandan_huang_guojie", "person_b": "shandan_zhang_kemeng",
     "type": "superior_subordinate", "strength": "strong",
     "context": "县长与副县长正副手关系",
     "overlap_org": "山丹县人民政府",
     "overlap_period": "至今", "confidence": "confirmed"},

    # 郭强 ↔ 高积鑫 (常务副县长↔副县长)
    {"person_a": "shandan_guo_qiang", "person_b": "shandan_gao_jixin",
     "type": "overlap", "strength": "strong",
     "context": "同为县政府党组班子成员",
     "overlap_org": "山丹县人民政府",
     "overlap_period": "至今", "confidence": "confirmed"},

    # 所有县委常委之间
    {"person_a": "shandan_guo_qiang", "person_b": "shandan_zhao_xuetao",
     "type": "overlap", "strength": "medium",
     "context": "同属中共山丹县常务委员会",
     "overlap_org": "中共山丹县委员会",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": "shandan_guo_qiang", "person_b": "shandan_an_wei",
     "type": "overlap", "strength": "medium",
     "context": "同属中共山丹县常务委员会",
     "overlap_org": "中共山丹县委员会",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": "shandan_guo_qiang", "person_b": "shandan_cao_haixia",
     "type": "overlap", "strength": "medium",
     "context": "同属中共山丹县常务委员会",
     "overlap_org": "中共山丹县委员会",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": "shandan_guo_qiang", "person_b": "shandan_zhang_yongsheng",
     "type": "overlap", "strength": "medium",
     "context": "同属中共山丹县常务委员会",
     "overlap_org": "中共山丹县委员会",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": "shandan_guo_qiang", "person_b": "shandan_qian_shuhua",
     "type": "overlap", "strength": "medium",
     "context": "同属中共山丹县常务委员会",
     "overlap_org": "中共山丹县委员会",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": "shandan_guo_qiang", "person_b": "shandan_zhan_hongzhou",
     "type": "overlap", "strength": "medium",
     "context": "同属中共山丹县常务委员会",
     "overlap_org": "中共山丹县委员会",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": "shandan_guo_qiang", "person_b": "shandan_yang_congjun",
     "type": "overlap", "strength": "medium",
     "context": "同属中共山丹县常务委员会",
     "overlap_org": "中共山丹县委员会",
     "overlap_period": "至今", "confidence": "confirmed"},
]


# ── BUILD ────────────────────────────────────────────────────────────

def build():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("PRAGMA foreign_keys = ON;")

    c.execute("""
        CREATE TABLE IF NOT EXISTS persons (
            id TEXT PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, native_place TEXT,
            education TEXT,
            party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT,
            source TEXT,
            notes TEXT, confidence TEXT
        );
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id TEXT PRIMARY KEY,
            name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        );
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT, org_id TEXT,
            title TEXT, start TEXT, end TEXT,
            rank TEXT, note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT, person_b TEXT,
            type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT,
            strength TEXT, confidence TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, native_place,
             education, party_join, work_start,
             current_post, current_org, source,
             notes, confidence)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"],
             p["birth"], p.get("birthplace", ""), p.get("native_place", ""),
             p.get("education", ""), p["party_join"], p.get("work_start", ""),
             p["current_post"], p["current_org"], p["source"],
             p.get("notes", ""), p["confidence"]))

    for o in organizations:
        c.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"],
             o["parent"], o["location"]))

    for pos in positions:
        c.execute("""INSERT INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start"], pos["end"], pos["rank"], pos["note"]))

    for rel in relationships:
        c.execute("""INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period,
             strength, confidence)
            VALUES (?,?,?,?,?,?,?,?)""",
            (rel["person_a"], rel["person_b"], rel["type"],
             rel["context"], rel["overlap_org"], rel["overlap_period"],
             rel["strength"], rel["confidence"]))

    conn.commit()
    conn.close()
    print(f"[DB] Wrote {DB_PATH}")


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    current = p.get("current_post", "")
    if "县委书记" in current:
        return "255,50,50"
    if "县长" in current or "副县长" in current or "常务副" in current:
        return "50,100,255"
    if "纪委书记" in current or "监委" in current:
        return "255,165,0"
    return "100,100,100"


def is_top_leader(p):
    current = p.get("current_post", "")
    return "县委书记" in current or "县长" in current


def org_color(o):
    t = o.get("type", "")
    if "党委" in t:
        return "255,200,200"
    if "政府" in t:
        return "200,200,255"
    if "人大" in t:
        return "200,255,255"
    if "政协" in t:
        return "255,240,200"
    if "开发区" in t:
        return "200,255,200"
    if "乡镇" in t:
        return "255,255,200"
    if "事业单位" in t:
        return "220,220,220"
    return "200,200,200"


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>山丹县领导班子工作关系网络 — 中共山丹县委员会、山丹县人民政府及关联组织</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="org_type" type="string"/>')
    lines.append('      <attribute id="2" title="birth" type="string"/>')
    lines.append('      <attribute id="3" title="title" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="strength" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="{esc(p["id"])}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("current_post",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="{esc(o["id"])}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 1
    for pos in positions:
        lines.append(f'      <edge id="e{eid}" source="{esc(pos["person_id"])}" target="{esc(pos["org_id"])}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    for rel in relationships:
        w = "2.0" if rel.get("strength") == "strong" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="{esc(rel["person_a"])}" target="{esc(rel["person_b"])}" label="{esc(rel["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(rel.get("context",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(rel.get("strength",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[GEXF] Wrote {GEXF_PATH}")


if __name__ == "__main__":
    build()
    build_gexf()

    # Summary
    print(f"\nSummary:")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
