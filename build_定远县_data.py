#!/usr/bin/env python3
"""Build 定远县 (Dingyuan County, Chuzhou, Anhui) leadership network data: SQLite DB + GEXF graph.

Research date: 2026-07-15
Task: anhui_定远县 - 县委书记 & 县长
Province: 安徽省
City: 滁州市
Region: 定远县
Level: 县

Data sources:
- dingyuan.gov.cn (official government website, 2026-07-15) — confirmed current leaders
  via news articles: 县委常委会全面从严治党专题会, 十六届县委常委会第1次会议,
  县委理论学习中心组学习会议, 全县"两优一先"表彰大会, 县第十六次党代会等

Confirmed from dingyuan.gov.cn as of 2026-07-15:
- 汪国玲: 县委书记 (confirmed: 主持县委常委会、县委理论学习中心组学习会, 党代会作报告)
- 杨新成: 县委副书记、县长 (confirmed: 主持全县"两优一先"表彰大会, 参加党代会分组讨论)
- 韩淑君: 县委副书记（专职）(confirmed: 宣读表彰决定, 传达学习文件)
- 第十六届县委常委会11人: 汪国玲, 杨新成, 韩淑君, 刘星, 赵开俊, 许倩, 樊红兵,
  章恒芝, 程永峰, 何世斌(组织部长), 姚亮亮(宣传部长)
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ──────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Detect if running from staging
if "data/tmp" in SCRIPT_DIR:
    STAGING = SCRIPT_DIR
else:
    STAGING = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(SCRIPT_DIR))),
                           "data/tmp/anhui_定远县")
DB_PATH = os.path.join(STAGING, "定远县_network.db")
GEXF_PATH = os.path.join(STAGING, "定远县_network.gexf")

# ── research data ──────────────────────────────────────────────────────

persons = [
    # ═══ Current Top Leaders ═══

    # 县委书记 — 汪国玲 (confirmed from dingyuan.gov.cn news articles, 2026-06/07)
    {
        "id": "dingyuan_wang_guoling",
        "name": "汪国玲",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "定远县委书记",
        "current_org": "中共定远县委员会",
        "source": "dingyuan.gov.cn 政务要闻 (2026-07-15 县委常委会全面从严治党专题会; 2026-07-01 十六届县委常委会第1次会议; 2026-06-27 十六届县委第一次全会)",
        "notes": "confirmed from dingyuan.gov.cn: 主持县委常委会、县委理论学习中心组学习会，在第十六次党代会作报告，当选十六届县委书记。调研防汛防台风、耕地保护、生态环境整改等工作。",
        "confidence": "confirmed"
    },

    # 县长 — 杨新成 (confirmed from dingyuan.gov.cn news articles, 2026-06/07)
    {
        "id": "dingyuan_yang_xincheng",
        "name": "杨新成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "定远县委副书记、县长",
        "current_org": "定远县人民政府",
        "source": "dingyuan.gov.cn 政务要闻 (2026-07-03 全县'两优一先'表彰大会; 2026-06-27 十六届县委第一次全会; 2026-06-26 党代会分组讨论)",
        "notes": "confirmed from dingyuan.gov.cn: 主持全县'两优一先'表彰大会（县委副书记、县长身份），参加县第十六次党代会第四代表团讨论，当选十六届县委副书记。",
        "confidence": "confirmed"
    },

    # ═══ County Party Committee Standing Members (县委常委会) ═══
    # Confirmed from dingyuan.gov.cn: 十六届县委第一次全体会议选举结果 (2026-06-26)

    # 专职副书记 — 韩淑君
    {
        "id": "dingyuan_han_shujun",
        "name": "韩淑君",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "定远县委副书记（专职）",
        "current_org": "中共定远县委员会",
        "source": "dingyuan.gov.cn (2026-06-27 十六届县委第一次全会; 2026-07-08 县委理论学习中心组学习会; 2026-07-03 全县'两优一先'表彰大会)",
        "notes": "confirmed from dingyuan.gov.cn: 当选十六届县委副书记。在县委理论学习中心组学习会上传达学习文件，在'两优一先'表彰大会上宣读表彰决定。",
        "confidence": "confirmed"
    },

    # 县委常委 — 刘星
    {
        "id": "dingyuan_liu_xing",
        "name": "刘星",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共定远县委员会",
        "source": "dingyuan.gov.cn (2026-06-27 十六届县委第一次全会; 2026-06-26 十六次党代会开幕)",
        "notes": "confirmed from dingyuan.gov.cn: 当选十六届县委常委。在党代会开幕式主席台前排就座。具体分工待确认。",
        "confidence": "confirmed"
    },

    # 县委常委 — 赵开俊
    {
        "id": "dingyuan_zhao_kaijun",
        "name": "赵开俊",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共定远县委员会",
        "source": "dingyuan.gov.cn (2026-06-27 十六届县委第一次全会; 2026-07-15 县委常委会全面从严治党专题会)",
        "notes": "confirmed from dingyuan.gov.cn: 当选十六届县委常委。参加县委常委会会议。具体分工待确认。",
        "confidence": "confirmed"
    },

    # 县委常委 — 许倩
    {
        "id": "dingyuan_xu_qian",
        "name": "许倩",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共定远县委员会",
        "source": "dingyuan.gov.cn (2026-06-27 十六届县委第一次全会; 2026-07-15 县委常委会全面从严治党专题会)",
        "notes": "confirmed from dingyuan.gov.cn: 当选十六届县委常委。参加县委常委会会议。具体分工待确认。",
        "confidence": "confirmed"
    },

    # 县委常委 — 樊红兵
    {
        "id": "dingyuan_fan_hongbing",
        "name": "樊红兵",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共定远县委员会",
        "source": "dingyuan.gov.cn (2026-06-27 十六届县委第一次全会; 2026-07-15 县委常委会全面从严治党专题会)",
        "notes": "confirmed from dingyuan.gov.cn: 当选十六届县委常委。参加县委常委会会议。具体分工待确认。",
        "confidence": "confirmed"
    },

    # 县委常委 — 章恒芝
    {
        "id": "dingyuan_zhang_hengzhi",
        "name": "章恒芝",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共定远县委员会",
        "source": "dingyuan.gov.cn (2026-06-27 十六届县委第一次全会; 2026-07-15 县委常委会全面从严治党专题会)",
        "notes": "confirmed from dingyuan.gov.cn: 当选十六届县委常委。参加县委常委会会议。具体分工待确认。",
        "confidence": "confirmed"
    },

    # 县委常委 — 程永峰
    {
        "id": "dingyuan_cheng_yongfeng",
        "name": "程永峰",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共定远县委员会",
        "source": "dingyuan.gov.cn (2026-06-27 十六届县委第一次全会; 2026-07-15 县委常委会全面从严治党专题会)",
        "notes": "confirmed from dingyuan.gov.cn: 当选十六届县委常委。参加县委常委会会议。具体分工待确认。新闻中有时写作'程永锋'。",
        "confidence": "confirmed"
    },

    # 县委常委、组织部部长 — 何世斌
    {
        "id": "dingyuan_he_shibin",
        "name": "何世斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共定远县委员会组织部",
        "source": "dingyuan.gov.cn (2026-06-27 十六届县委第一次全会; 2026-07-08 县委理论学习中心组学习会; 2026-07-01 老年大学文艺汇演)",
        "notes": "confirmed from dingyuan.gov.cn: 当选十六届县委常委。在县委理论学习中心组学习会上传达学习文件，以'县委常委、组织部部长'身份出席老年大学活动。",
        "confidence": "confirmed"
    },

    # 县委常委、宣传部部长 — 姚亮亮
    {
        "id": "dingyuan_yao_liangliang",
        "name": "姚亮亮",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共定远县委员会宣传部",
        "source": "dingyuan.gov.cn (2026-06-27 十六届县委第一次全会; 2026-07-14 汪国玲深入乡镇查看防汛防台风防溺水工作)",
        "notes": "confirmed from dingyuan.gov.cn: 当选十六届县委常委。在防汛调研中以'县委常委、宣传部部长姚亮亮'身份陪同参加。",
        "confidence": "confirmed"
    },

    # ═══ Other Key Leaders ═══

    # 县政协主席 — 黄保云
    {
        "id": "dingyuan_huang_baoyun",
        "name": "黄保云",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "中国人民政治协商会议定远县委员会",
        "source": "dingyuan.gov.cn (2026-07-01 县政协调研养老服务中心老年助餐点建设工作)",
        "notes": "confirmed from dingyuan.gov.cn: 以'县政协主席'身份率队调研养老服务中心。原十五届县委常委，十六届未入选常委班子，转任政协。",
        "confidence": "confirmed"
    },

    # 副县长 — 陈琪瑶
    {
        "id": "dingyuan_chen_qiyao",
        "name": "陈琪瑶",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "定远县人民政府",
        "source": "dingyuan.gov.cn (2026-07-09 吴劲来我县调研水生态环境; 2026-07-06 汪国玲调研督导突出生态环境问题整改)",
        "notes": "confirmed from dingyuan.gov.cn: 以'副县长'身份陪同市委书记吴劲调研水生态环境，陪同县委书记调研生态环境整改。",
        "confidence": "confirmed"
    },

    # 副县长 — 徐盛
    {
        "id": "dingyuan_xu_sheng",
        "name": "徐盛",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "定远县人民政府",
        "source": "dingyuan.gov.cn (2026-07-06 汪国玲调研督导突出生态环境问题整改)",
        "notes": "confirmed from dingyuan.gov.cn: 以'副县长'身份陪同县委书记调研。具体分管领域待确认。",
        "confidence": "confirmed"
    },

    # 史新荣 — 前县委常委/重要县领导
    {
        "id": "dingyuan_shi_xinrong",
        "name": "史新荣",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县领导（职务待确认）",
        "current_org": "定远县",
        "source": "dingyuan.gov.cn (2026-06-27 十六次党代会闭幕; 2026-07-01 县委常委会扩大会议)",
        "notes": "confirmed from dingyuan.gov.cn: 多次在县重要活动中在主席台前排就座（党代会开幕式、闭幕式），排序在汪国玲、杨新成之后。未当选十六届县委常委，具体现职务待确认（可能为人大主任或保留正县级待遇）。",
        "confidence": "plausible"
    },

    # 李文书 — 十五届县委常委（已退出十六届常委班子）
    {
        "id": "dingyuan_li_wenshu",
        "name": "李文书",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（职务待确认，已退出十六届常委班子）",
        "current_org": "",
        "source": "dingyuan.gov.cn (2026-06-26 十六次党代会开幕)",
        "notes": "在十六次党代会开幕式主席台前排就座，列为大会执行主席。未当选十六届县委常委。现职务变动待确认。",
        "confidence": "plausible"
    },
]


# ── Organizations ──────────────────────────────────────────────────────

organizations = [
    {
        "id": "org_cpc_dingyuan",
        "name": "中共定远县委员会",
        "type": "党委",
        "level": "county",
        "parent": "中共滁州市委员会",
        "location": "安徽省滁州市定远县",
    },
    {
        "id": "org_gov_dingyuan",
        "name": "定远县人民政府",
        "type": "政府",
        "level": "county",
        "parent": "滁州市人民政府",
        "location": "安徽省滁州市定远县",
    },
    {
        "id": "org_cppcc_dingyuan",
        "name": "中国人民政治协商会议定远县委员会",
        "type": "政协",
        "level": "county",
        "parent": "中国人民政治协商会议滁州市委员会",
        "location": "安徽省滁州市定远县",
    },
    {
        "id": "org_org_dept_dingyuan",
        "name": "中共定远县委员会组织部",
        "type": "党委",
        "level": "county",
        "parent": "中共定远县委员会",
        "location": "安徽省滁州市定远县",
    },
    {
        "id": "org_propaganda_dept_dingyuan",
        "name": "中共定远县委员会宣传部",
        "type": "党委",
        "level": "county",
        "parent": "中共定远县委员会",
        "location": "安徽省滁州市定远县",
    },
]


# ── Positions ──────────────────────────────────────────────────────────

positions = [
    # 汪国玲
    {"person_id": "dingyuan_wang_guoling", "org_id": "org_cpc_dingyuan",
     "title": "县委书记", "start": "2026-06（十六届一次全会当选）", "end": "", "rank": "1",
     "note": "此前为十五届县委书记，十六届连任"},
    # 杨新成
    {"person_id": "dingyuan_yang_xincheng", "org_id": "org_cpc_dingyuan",
     "title": "县委副书记", "start": "2026-06（十六届一次全会当选）", "end": "", "rank": "2",
     "note": "十六届县委副书记"},
    {"person_id": "dingyuan_yang_xincheng", "org_id": "org_gov_dingyuan",
     "title": "县长", "start": "", "end": "", "rank": "1",
     "note": "县委副书记、县长"},
    # 韩淑君
    {"person_id": "dingyuan_han_shujun", "org_id": "org_cpc_dingyuan",
     "title": "县委副书记（专职）", "start": "2026-06（十六届一次全会当选）", "end": "", "rank": "3",
     "note": "十六届县委副书记"},
    # 刘星
    {"person_id": "dingyuan_liu_xing", "org_id": "org_cpc_dingyuan",
     "title": "县委常委", "start": "2026-06（十六届一次全会当选）", "end": "", "rank": "4",
     "note": "十六届县委常委"},
    # 赵开俊
    {"person_id": "dingyuan_zhao_kaijun", "org_id": "org_cpc_dingyuan",
     "title": "县委常委", "start": "2026-06（十六届一次全会当选）", "end": "", "rank": "5",
     "note": "十六届县委常委"},
    # 许倩
    {"person_id": "dingyuan_xu_qian", "org_id": "org_cpc_dingyuan",
     "title": "县委常委", "start": "2026-06（十六届一次全会当选）", "end": "", "rank": "6",
     "note": "十六届县委常委"},
    # 樊红兵
    {"person_id": "dingyuan_fan_hongbing", "org_id": "org_cpc_dingyuan",
     "title": "县委常委", "start": "2026-06（十六届一次全会当选）", "end": "", "rank": "7",
     "note": "十六届县委常委"},
    # 章恒芝
    {"person_id": "dingyuan_zhang_hengzhi", "org_id": "org_cpc_dingyuan",
     "title": "县委常委", "start": "2026-06（十六届一次全会当选）", "end": "", "rank": "8",
     "note": "十六届县委常委"},
    # 程永峰
    {"person_id": "dingyuan_cheng_yongfeng", "org_id": "org_cpc_dingyuan",
     "title": "县委常委", "start": "2026-06（十六届一次全会当选）", "end": "", "rank": "9",
     "note": "十六届县委常委"},
    # 何世斌
    {"person_id": "dingyuan_he_shibin", "org_id": "org_cpc_dingyuan",
     "title": "县委常委", "start": "2026-06（十六届一次全会当选）", "end": "", "rank": "10",
     "note": "十六届县委常委"},
    {"person_id": "dingyuan_he_shibin", "org_id": "org_org_dept_dingyuan",
     "title": "组织部部长", "start": "", "end": "", "rank": "1",
     "note": "县委常委兼任组织部部长"},
    # 姚亮亮
    {"person_id": "dingyuan_yao_liangliang", "org_id": "org_cpc_dingyuan",
     "title": "县委常委", "start": "2026-06（十六届一次全会当选）", "end": "", "rank": "11",
     "note": "十六届县委常委"},
    {"person_id": "dingyuan_yao_liangliang", "org_id": "org_propaganda_dept_dingyuan",
     "title": "宣传部部长", "start": "", "end": "", "rank": "1",
     "note": "县委常委兼任宣传部部长"},
    # 黄保云
    {"person_id": "dingyuan_huang_baoyun", "org_id": "org_cppcc_dingyuan",
     "title": "县政协主席", "start": "", "end": "", "rank": "1",
     "note": "此前为十五届县委常委，十六届转任政协主席"},
    # 陈琪瑶
    {"person_id": "dingyuan_chen_qiyao", "org_id": "org_gov_dingyuan",
     "title": "副县长", "start": "", "end": "", "rank": "2",
     "note": "分管领域待确认"},
    # 徐盛
    {"person_id": "dingyuan_xu_sheng", "org_id": "org_gov_dingyuan",
     "title": "副县长", "start": "", "end": "", "rank": "3",
     "note": "分管领域待确认"},
]


# ── Relationships ──────────────────────────────────────────────────────

relationships = [
    # 县委书记 vs 县长 (党政正职)
    {"person_a": "dingyuan_wang_guoling", "person_b": "dingyuan_yang_xincheng",
     "type": "colleague", "strength": "strong",
     "context": "县委书记与县长搭档（党政正职关系）",
     "overlap_org": "org_cpc_dingyuan",
     "overlap_period": "2026年6月至今",
     "note": "confirmed"},
    # 县委书记 vs 专职副书记
    {"person_a": "dingyuan_wang_guoling", "person_b": "dingyuan_han_shujun",
     "type": "colleague", "strength": "strong",
     "context": "县委书记与专职副书记",
     "overlap_org": "org_cpc_dingyuan",
     "overlap_period": "2026年6月至今",
     "note": "confirmed"},
    # 县长 vs 专职副书记
    {"person_a": "dingyuan_yang_xincheng", "person_b": "dingyuan_han_shujun",
     "type": "colleague", "strength": "strong",
     "context": "县长与专职副书记",
     "overlap_org": "org_cpc_dingyuan",
     "overlap_period": "2026年6月至今",
     "note": "confirmed"},
    # 县委常委同事关系（同届常委班子）
    {"person_a": "dingyuan_wang_guoling", "person_b": "dingyuan_liu_xing",
     "type": "colleague", "strength": "strong",
     "context": "县委书记与县委常委（同届常委班子）",
     "overlap_org": "org_cpc_dingyuan",
     "overlap_period": "2026年6月至今",
     "note": "confirmed"},
    {"person_a": "dingyuan_wang_guoling", "person_b": "dingyuan_zhao_kaijun",
     "type": "colleague", "strength": "strong",
     "context": "县委书记与县委常委",
     "overlap_org": "org_cpc_dingyuan",
     "overlap_period": "2026年6月至今",
     "note": "confirmed"},
    {"person_a": "dingyuan_wang_guoling", "person_b": "dingyuan_xu_qian",
     "type": "colleague", "strength": "strong",
     "context": "县委书记与县委常委",
     "overlap_org": "org_cpc_dingyuan",
     "overlap_period": "2026年6月至今",
     "note": "confirmed"},
    {"person_a": "dingyuan_wang_guoling", "person_b": "dingyuan_fan_hongbing",
     "type": "colleague", "strength": "strong",
     "context": "县委书记与县委常委",
     "overlap_org": "org_cpc_dingyuan",
     "overlap_period": "2026年6月至今",
     "note": "confirmed"},
    {"person_a": "dingyuan_wang_guoling", "person_b": "dingyuan_zhang_hengzhi",
     "type": "colleague", "strength": "strong",
     "context": "县委书记与县委常委",
     "overlap_org": "org_cpc_dingyuan",
     "overlap_period": "2026年6月至今",
     "note": "confirmed"},
    {"person_a": "dingyuan_wang_guoling", "person_b": "dingyuan_cheng_yongfeng",
     "type": "colleague", "strength": "strong",
     "context": "县委书记与县委常委",
     "overlap_org": "org_cpc_dingyuan",
     "overlap_period": "2026年6月至今",
     "note": "confirmed"},
    {"person_a": "dingyuan_wang_guoling", "person_b": "dingyuan_he_shibin",
     "type": "colleague", "strength": "strong",
     "context": "县委书记与组织部部长",
     "overlap_org": "org_cpc_dingyuan",
     "overlap_period": "2026年6月至今",
     "note": "confirmed"},
    {"person_a": "dingyuan_wang_guoling", "person_b": "dingyuan_yao_liangliang",
     "type": "colleague", "strength": "strong",
     "context": "县委书记与宣传部部长",
     "overlap_org": "org_cpc_dingyuan",
     "overlap_period": "2026年6月至今",
     "note": "confirmed"},
    # 副县长与县长关系
    {"person_a": "dingyuan_yang_xincheng", "person_b": "dingyuan_chen_qiyao",
     "type": "colleague", "strength": "strong",
     "context": "县长与副县长",
     "overlap_org": "org_gov_dingyuan",
     "overlap_period": "",
     "note": "confirmed"},
    {"person_a": "dingyuan_yang_xincheng", "person_b": "dingyuan_xu_sheng",
     "type": "colleague", "strength": "strong",
     "context": "县长与副县长",
     "overlap_org": "org_gov_dingyuan",
     "overlap_period": "",
     "note": "confirmed"},
    # 黄保云（政协主席）与班子成员关系
    {"person_a": "dingyuan_wang_guoling", "person_b": "dingyuan_huang_baoyun",
     "type": "colleague", "strength": "medium",
     "context": "县委书记与政协主席（此前为县委常委同事）",
     "overlap_org": "org_cpc_dingyuan",
     "overlap_period": "2026年6月前（十五届常委班子同事）",
     "note": "plausible"},
]


# ── HELPERS ────────────────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    post = p["current_post"]
    if "县委书记" in post:
        return "255,50,50"
    if "县长" in post:
        return "50,100,255"
    if "纪委书记" in post:
        return "255,165,0"
    if "人大" in post:
        return "200,100,100"
    if "政协" in post:
        return "100,100,200"
    if "组织" in post:
        return "150,50,150"
    if "宣传" in post:
        return "50,150,150"
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
    return "200,200,200"


def is_top_leader(p):
    return p["id"] in ("dingyuan_wang_guoling", "dingyuan_yang_xincheng")


# ── BUILD DB ───────────────────────────────────────────────────────────

def build_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("PRAGMA foreign_keys = ON;")

    c.execute("DROP TABLE IF EXISTS relationships;")
    c.execute("DROP TABLE IF EXISTS positions;")
    c.execute("DROP TABLE IF EXISTS organizations;")
    c.execute("DROP TABLE IF EXISTS persons;")

    c.execute("""
        CREATE TABLE persons (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            native_place TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT,
            notes TEXT,
            confidence TEXT DEFAULT 'unverified'
        )
    """)

    c.execute("""
        CREATE TABLE organizations (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)

    c.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT NOT NULL,
            org_id TEXT NOT NULL,
            title TEXT NOT NULL,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)

    c.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT,
            strength TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            note TEXT DEFAULT 'unverified',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    for p in persons:
        c.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, native_place,
                                 education, party_join, work_start, current_post, current_org,
                                 source, notes, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
            p["birthplace"], p["native_place"], p["education"],
            p["party_join"], p["work_start"], p["current_post"], p["current_org"],
            p["source"], p["notes"], p["confidence"]
        ))

    for o in organizations:
        c.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos["title"],
              pos["start"], pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("""
            INSERT INTO relationships (person_a, person_b, type, strength, context, overlap_org, overlap_period, note)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r["type"], r["strength"],
              r["context"], r["overlap_org"], r["overlap_period"], r["note"]))

    conn.commit()
    print(f"  Persons: {c.execute('SELECT COUNT(*) FROM persons').fetchone()[0]}")
    print(f"  Orgs: {c.execute('SELECT COUNT(*) FROM organizations').fetchone()[0]}")
    print(f"  Positions: {c.execute('SELECT COUNT(*) FROM positions').fetchone()[0]}")
    print(f"  Relationships: {c.execute('SELECT COUNT(*) FROM relationships').fetchone()[0]}")
    conn.close()


# ── BUILD GEXF ─────────────────────────────────────────────────────────

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>定远县（安徽省滁州市）领导关系网络 - 2026年7月</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="gender" type="string"/>')
    lines.append('      <attribute id="3" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="strength" type="string"/>')
    lines.append('    </attributes>')

    # Nodes - Persons
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="{esc(p["id"])}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["gender"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p["confidence"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes - Organizations
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="{esc(o["id"])}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('          <attvalue for="3" value="confirmed"/>')
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
        lines.append(f'      <edge id="e{eid}" source="{esc(pos["person_id"])}" target="{esc(pos["org_id"])}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person <-> Person relationships
    for r in relationships:
        eid += 1
        w = "2.0" if r["strength"] == "strong" else "1.5"
        lines.append(f'      <edge id="e{eid}" source="{esc(r["person_a"])}" target="{esc(r["person_b"])}" label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["strength"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF: {len(persons)} persons, {len(organizations)} orgs, {eid} edges")


# ── MAIN ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    print("Building 定远县 (Dingyuan County, Chuzhou, Anhui) network...")
    print(f"  DB path: {DB_PATH}")
    print(f"  GEXF path: {GEXF_PATH}")
    print("  NOTE: Core leaders confirmed from dingyuan.gov.cn news articles (2026-06/07).")
    print("  Biographical details (birth, birthplace, education) need live verification.")
    build_db()
    build_gexf()
    print("Done.")
