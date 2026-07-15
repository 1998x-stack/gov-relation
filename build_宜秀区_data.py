#!/usr/bin/env python3
"""Build 宜秀区 (Yixiu District, Anqing, Anhui) leadership network data: SQLite DB + GEXF graph.

Research date: 2026-07-15
Sources:
  - www.yixiu.gov.cn (official district government website, leadership page accessed 2026-07-15)
  - www.yixiu.gov.cn/ldzc/index.html (区委领导 + 区政府领导 listings)
  - baike.baidu.com/item/王良宜 (Baidu Baike, accessed 2026-07-15)
  - www.yixiu.gov.cn/yxyw/zwyw/ (news articles June-July 2026)

Confidence: Current roles confirmed from official Yixiu government leadership page.
Career timeline for 王良宜 from Baidu Baike with cross-references to news reports.
Biographical details for 黄震 are partial; career timeline to be supplemented.
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ────────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "宜秀区_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "宜秀区_network.gexf")

# ── research data ────────────────────────────────────────────────────────

persons = [
    # ═══ Current Top Leaders ═══

    # 区委书记 王良宜（2026年6月任）
    {
        "id": "yixiu_wang_liangyi",
        "name": "王良宜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-12",
        "birthplace": "安徽枞阳",
        "native_place": "安徽枞阳",
        "education": "省委党校研究生",
        "party_join": "2001-04",
        "work_start": "1994-11",
        "current_post": "宜秀区委书记",
        "current_org": "中共安庆市宜秀区委员会",
        "source": "https://www.yixiu.gov.cn/ldzc/index.html; https://baike.baidu.com/item/%E7%8E%8B%E8%89%AF%E5%AE%9C/19741445",
        "notes": "1971年12月生，安徽枞阳人，省委党校研究生学历。1994年11月参加工作，2001年4月入党。2026年6月任宜秀区委书记。主持区委全面工作。",
        "confidence": "confirmed"
    },
    # 区长 黄震（现任）
    {
        "id": "yixiu_huang_zhen",
        "name": "黄震",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1976-10",
        "birthplace": "",
        "native_place": "",
        "education": "省委党校大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜秀区委副书记、区长",
        "current_org": "宜秀区人民政府",
        "source": "https://www.yixiu.gov.cn/ldzc/index.html",
        "notes": "1976年10月出生，省委党校大学学历，中共党员。现任宜秀区委副书记，区政府党组书记、区政府区长。领导区政府全面工作，负责审计工作。分管审计局。",
        "confidence": "confirmed"
    },

    # ═══ District Party Committee Standing Members (区委常委) ═══

    # 刘秀芳 — 区委常委（待确认具体分工）
    {
        "id": "yixiu_liu_xiufang",
        "name": "刘秀芳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共安庆市宜秀区委员会",
        "source": "https://www.yixiu.gov.cn/ldzc/index.html",
        "notes": "宜秀区委常委。出席区第五次党代会并在主席台前排就座。",
        "confidence": "confirmed"
    },
    # 方胜 — 区委常委
    {
        "id": "yixiu_fang_sheng",
        "name": "方胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共安庆市宜秀区委员会",
        "source": "https://www.yixiu.gov.cn/ldzc/index.html",
        "notes": "宜秀区委常委。出席区第五次党代会并在主席台前排就座。",
        "confidence": "confirmed"
    },
    # 张万丰 — 区委常委
    {
        "id": "yixiu_zhang_wanfeng",
        "name": "张万丰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共安庆市宜秀区委员会",
        "source": "https://www.yixiu.gov.cn/ldzc/index.html",
        "notes": "宜秀区委常委。",
        "confidence": "confirmed"
    },
    # 张婷 — 区委常委、副区长（政府领导中亦列名）
    {
        "id": "yixiu_zhang_ting",
        "name": "张婷",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "宜秀区人民政府",
        "source": "https://www.yixiu.gov.cn/ldzc/index.html",
        "notes": "宜秀区委常委、副区长。同时列区委领导和政府领导名单。",
        "confidence": "confirmed"
    },
    # 李结华 — 区委常委
    {
        "id": "yixiu_li_jiehua",
        "name": "李结华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共安庆市宜秀区委员会",
        "source": "https://www.yixiu.gov.cn/ldzc/index.html",
        "notes": "宜秀区委常委。",
        "confidence": "confirmed"
    },
    # 朱元松 — 区委常委、副区长
    {
        "id": "yixiu_zhu_yuansong",
        "name": "朱元松",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "宜秀区人民政府",
        "source": "https://www.yixiu.gov.cn/ldzc/index.html",
        "notes": "宜秀区委常委、副区长。同时列区委领导和政府领导名单。",
        "confidence": "confirmed"
    },
    # 潘长周 — 区委常委
    {
        "id": "yixiu_pan_changzhou",
        "name": "潘长周",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共安庆市宜秀区委员会",
        "source": "https://www.yixiu.gov.cn/ldzc/index.html",
        "notes": "宜秀区委常委。",
        "confidence": "confirmed"
    },
    # 周礼 — 区委常委、副区长
    {
        "id": "yixiu_zhou_li",
        "name": "周礼",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "宜秀区人民政府",
        "source": "https://www.yixiu.gov.cn/ldzc/index.html",
        "notes": "宜秀区委常委、副区长。同时列区委领导和政府领导名单。",
        "confidence": "confirmed"
    },
    # 朱振 — 区委常委
    {
        "id": "yixiu_zhu_zhen",
        "name": "朱振",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共安庆市宜秀区委员会",
        "source": "https://www.yixiu.gov.cn/ldzc/index.html",
        "notes": "宜秀区委常委。",
        "confidence": "confirmed"
    },
    # 余洋 — 区委常委
    {
        "id": "yixiu_yu_yang",
        "name": "余洋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共安庆市宜秀区委员会",
        "source": "https://www.yixiu.gov.cn/ldzc/index.html",
        "notes": "宜秀区委常委。",
        "confidence": "confirmed"
    },

    # ═══ District Government Leadership (区政府领导) ═══

    # 张泓 — 副区长（非区委常委）
    {
        "id": "yixiu_zhang_hong",
        "name": "张泓",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "宜秀区人民政府",
        "source": "https://www.yixiu.gov.cn/ldzc/index.html",
        "notes": "宜秀区副区长。",
        "confidence": "confirmed"
    },
    # 徐晋斌 — 副区长
    {
        "id": "yixiu_xu_jinbin",
        "name": "徐晋斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "宜秀区人民政府",
        "source": "https://www.yixiu.gov.cn/ldzc/index.html",
        "notes": "宜秀区副区长。",
        "confidence": "confirmed"
    },
    # 查长礼 — 副区长
    {
        "id": "yixiu_zha_changli",
        "name": "查长礼",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "宜秀区人民政府",
        "source": "https://www.yixiu.gov.cn/ldzc/index.html",
        "notes": "宜秀区副区长。",
        "confidence": "confirmed"
    },
    # 何天龙 — 副区长
    {
        "id": "yixiu_he_tianlong",
        "name": "何天龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "宜秀区人民政府",
        "source": "https://www.yixiu.gov.cn/ldzc/index.html",
        "notes": "宜秀区副区长。",
        "confidence": "confirmed"
    },

    # ═══ NPC & CPPCC ═══

    # 曹红斌 — 区人大常委会主任（推测）
    {
        "id": "yixiu_cao_hongbin",
        "name": "曹红斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜秀区人大常委会主任（推定）",
        "current_org": "安庆市宜秀区人民代表大会常务委员会",
        "source": "https://www.yixiu.gov.cn/yxyw/zwyw/2024668684.html",
        "notes": "出席区第五次党代会并在主席台前排就座，列名在黄震之后，推定区人大常委会主任。",
        "confidence": "plausible"
    },
    # 曹艾群 — 区政协主席（推测）
    {
        "id": "yixiu_cao_aiqun",
        "name": "曹艾群",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜秀区政协主席（推定）",
        "current_org": "中国人民政治协商会议安庆市宜秀区委员会",
        "source": "https://www.yixiu.gov.cn/yxyw/zwyw/2024668684.html",
        "notes": "出席区第五次党代会并在主席台前排就座，推定区政协主席。",
        "confidence": "plausible"
    },

    # ═══ Predecessors ═══

    # 前任区委书记（王良宜前任）— 待确认具体姓名
    # 从报道看，王良宜2026年6月新任，前书记应在2026年6月离任
    # 按惯例推测前任可能调整到市级岗位
    {
        "id": "yixiu_predecessor_secretary",
        "name": "（前任区委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（已离任）",
        "current_org": "",
        "source": "待查",
        "notes": "宜秀区委书记的前任。王良宜于2026年6月接任。具体姓名待进一步查证。",
        "confidence": "unverified"
    },

    # ═══ City-level leaders (connections) ═══

    {
        "id": "anqing_meng_jingwei",
        "name": "孟景伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-05",
        "birthplace": "河南汝州",
        "native_place": "河南汝州",
        "education": "研究生，经济学博士",
        "party_join": "",
        "work_start": "",
        "current_post": "安庆市委书记",
        "current_org": "中共安庆市委员会",
        "source": "https://www.anqing.gov.cn/ldzc/index.html; https://www.yixiu.gov.cn/yxyw/zwyw/2024674711.html",
        "notes": "1974年5月生，河南汝州人。2025年8月跨省调任安庆市委书记。2026年7月到宜秀区调研。",
        "confidence": "confirmed"
    },
    {
        "id": "anqing_zhang_junyi",
        "name": "张君毅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-02",
        "birthplace": "安徽涡阳",
        "native_place": "安徽涡阳",
        "education": "研究生，管理学硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "安庆市委副书记、市长",
        "current_org": "安庆市人民政府",
        "source": "https://www.anqing.gov.cn/ldzc/index.html",
        "notes": "1970年2月生，安徽涡阳人。2021年8月起任安庆市长。",
        "confidence": "confirmed"
    },
]

# ── Organizations ────────────────────────────────────────────────────
organizations = [
    {
        "id": "yixiu_party",
        "name": "中共安庆市宜秀区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共安庆市委员会",
        "location": "安徽省安庆市宜秀区"
    },
    {
        "id": "yixiu_gov",
        "name": "宜秀区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "安庆市人民政府",
        "location": "安徽省安庆市宜秀区"
    },
    {
        "id": "yixiu_discipline",
        "name": "中共安庆市宜秀区纪律检查委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "安庆市纪委监委",
        "location": "安徽省安庆市宜秀区"
    },
    {
        "id": "yixiu_npc",
        "name": "安庆市宜秀区人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "安庆市人大常委会",
        "location": "安徽省安庆市宜秀区"
    },
    {
        "id": "yixiu_cppcc",
        "name": "中国人民政治协商会议安庆市宜秀区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "安庆市政协",
        "location": "安徽省安庆市宜秀区"
    },
    {
        "id": "yixiu_org_dept",
        "name": "中共安庆市宜秀区委组织部",
        "type": "党委部门",
        "level": "乡科级",
        "parent": "中共宜秀区委",
        "location": "安徽省安庆市宜秀区"
    },
    {
        "id": "yixiu_propaganda",
        "name": "中共安庆市宜秀区委宣传部",
        "type": "党委部门",
        "level": "乡科级",
        "parent": "中共宜秀区委",
        "location": "安徽省安庆市宜秀区"
    },
    {
        "id": "yixiu_united_front",
        "name": "中共安庆市宜秀区委统一战线工作部",
        "type": "党委部门",
        "level": "乡科级",
        "parent": "中共宜秀区委",
        "location": "安徽省安庆市宜秀区"
    },
    # City level
    {
        "id": "anqing_party",
        "name": "中共安庆市委员会",
        "type": "党委",
        "level": "地市级",
        "parent": "中共安徽省委员会",
        "location": "安徽省安庆市"
    },
    {
        "id": "anqing_gov",
        "name": "安庆市人民政府",
        "type": "政府",
        "level": "地市级",
        "parent": "安徽省人民政府",
        "location": "安徽省安庆市"
    },
    # 王良宜曾任职机构
    {
        "id": "anqing_education_sports",
        "name": "安庆市教育体育局",
        "type": "政府",
        "level": "县处级",
        "parent": "安庆市人民政府",
        "location": "安徽省安庆市"
    },
    {
        "id": "anqing_party_education_sports",
        "name": "中共安庆市委教体工委",
        "type": "党委部门",
        "level": "县处级",
        "parent": "中共安庆市委员会",
        "location": "安徽省安庆市"
    },
    {
        "id": "anqing_gov_office",
        "name": "安庆市人民政府办公室",
        "type": "政府",
        "level": "县处级",
        "parent": "安庆市人民政府",
        "location": "安徽省安庆市"
    },
    {
        "id": "huaining_party",
        "name": "中共怀宁县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共安庆市委员会",
        "location": "安徽省安庆市怀宁县"
    },
    {
        "id": "anqing_organization_dept",
        "name": "中共安庆市委组织部",
        "type": "党委部门",
        "level": "县处级",
        "parent": "中共安庆市委员会",
        "location": "安徽省安庆市"
    },
    {
        "id": "anqing_communist_youth",
        "name": "共青团安庆市委员会",
        "type": "群团",
        "level": "县处级",
        "parent": "中共安庆市委员会",
        "location": "安徽省安庆市"
    },
    {
        "id": "unassigned",
        "name": "（待确认机构）",
        "type": "其他",
        "level": "",
        "parent": "",
        "location": ""
    },
]

# ── Positions ────────────────────────────────────────────────────────
positions = [
    # ═══ 王良宜 - 完整履历 ═══
    ("yixiu_wang_liangyi", "yixiu_party", "宜秀区委书记", "2026-06", "至今", "县处级正职",
     "2026年6月任安徽省安庆市宜秀区委书记。来源：百度百科、任前公示。"),
    ("yixiu_wang_liangyi", "anqing_education_sports", "安庆市教育体育局局长", "2024-02", "2026-06", "县处级正职",
     "2024年2月仍任局长，兼任市政协教科卫体委员会副主任。"),
    ("yixiu_wang_liangyi", "anqing_party_education_sports", "安庆市委教体工委书记", "2023-04", "2026-06", "县处级正职",
     "2023年4月-2024年2月任市委教体工委书记、市教育体育局局长。2024年2月起兼任市政协教科卫体委员会副主任。"),
    ("yixiu_wang_liangyi", "anqing_gov_office", "安庆市人民政府副秘书长", "约2021", "2023-04", "县处级副职",
     "安庆市人民政府副秘书长、机关党组成员，市政府办公室二级调研员。"),
    ("yixiu_wang_liangyi", "anqing_party_education_sports", "安庆市委教体工委副书记", "约2020", "约2021", "县处级副职",
     "安庆市委教体工委副书记、机关党委书记。"),
    ("yixiu_wang_liangyi", "anqing_education_sports", "安庆市教育体育局副局长", "约2019", "约2020", "县处级副职",
     "安庆市委教体工委委员、市教育体育局副局长。"),
    ("yixiu_wang_liangyi", "huaining_party", "怀宁县委常委、组织部长", "约2016", "约2019", "县处级副职",
     "曾任怀宁县委常委、组织部长、县委办主任。"),
    ("yixiu_wang_liangyi", "huaining_party", "怀宁县委常委、县委办主任", "约2015", "约2016", "县处级副职",
     "怀宁县委常委、县委办主任。"),
    ("yixiu_wang_liangyi", "anqing_organization_dept", "安庆市委组织部副调研员、研究室主任", "约2013", "约2015", "副调研员",
     "安庆市委组织部副调研员、研究室主任。其间挂职市发投公司总经理助理。"),
    ("yixiu_wang_liangyi", "anqing_organization_dept", "安庆市委组织部副调研员", "约2011", "约2013", "副调研员",
     "安庆市委组织部副调研员、市发投公司总经理助理（挂职）。"),
    ("yixiu_wang_liangyi", "anqing_organization_dept", "安庆市委组织部研究室副主任（正科级）", "约2008", "约2011", "正科级",
     "安庆市委组织部研究室副主任（正科级），农组办副主任。"),
    ("yixiu_wang_liangyi", "anqing_organization_dept", "安庆市委组织部研究室副主任", "约2007", "约2008", "副科级",
     "安庆市委组织部研究室副主任（正科级）。"),
    ("yixiu_wang_liangyi", "anqing_communist_youth", "共青团安庆市委正科级干事", "约2005", "约2007", "正科级",
     "共青团安庆市委正科级干事。"),
    ("yixiu_wang_liangyi", "anqing_communist_youth", "共青团安庆市委组织部副部长", "约2003", "约2005", "副科级",
     "共青团安庆市委组织部副部长。"),
    ("yixiu_wang_liangyi", "anqing_communist_youth", "共青团安庆市委副主任科员", "约2001", "约2003", "副主任科员",
     "共青团安庆市委副主任科员。"),
    ("yixiu_wang_liangyi", "anqing_communist_youth", "共青团安庆市委科员", "约1995", "约2001", "科员",
     "共青团安庆市委科员。"),
    ("yixiu_wang_liangyi", "unassigned", "安庆市胡玉美冷饮食品厂秘书", "1994-11", "约1995", "企业",
     "历任安徽省安庆市胡玉美冷饮食品厂秘书。1994年11月参加工作。"),
    ("yixiu_wang_liangyi", "unassigned", "淮南联合大学学习", "1992-09", "1994-07", "学生",
     "在淮南联合大学学习。"),

    # ═══ 黄震 ═══
    ("yixiu_huang_zhen", "yixiu_gov", "宜秀区区长", "至今", "至今", "县处级正职",
     "现任宜秀区委副书记，区政府党组书记、区政府区长。领导区政府全面工作。"),
    ("yixiu_huang_zhen", "yixiu_party", "宜秀区委副书记", "至今", "至今", "县处级正职",
     "宜秀区委副书记。"),
    # 黄震的早期履历待补充
    ("yixiu_huang_zhen", "unassigned", "（早期履历待查）", "unknown", "unknown", "unknown",
     "黄震早期公开履历信息不足，待进一步查证。"),

    # ═══ 区委常委 ═══
    ("yixiu_liu_xiufang", "yixiu_party", "宜秀区委常委", "至今", "至今", "县处级副职",
     "具体分工待确认。"),
    ("yixiu_fang_sheng", "yixiu_party", "宜秀区委常委", "至今", "至今", "县处级副职",
     "具体分工待确认。"),
    ("yixiu_zhang_wanfeng", "yixiu_party", "宜秀区委常委", "至今", "至今", "县处级副职",
     "具体分工待确认。"),
    ("yixiu_zhang_ting", "yixiu_gov", "宜秀区副区长", "至今", "至今", "县处级副职",
     "副区长（区委常委兼任）。"),
    ("yixiu_zhang_ting", "yixiu_party", "宜秀区委常委", "至今", "至今", "县处级副职",
     "区委常委。"),
    ("yixiu_li_jiehua", "yixiu_party", "宜秀区委常委", "至今", "至今", "县处级副职",
     "具体分工待确认。"),
    ("yixiu_zhu_yuansong", "yixiu_gov", "宜秀区副区长", "至今", "至今", "县处级副职",
     "副区长（区委常委兼任）。"),
    ("yixiu_zhu_yuansong", "yixiu_party", "宜秀区委常委", "至今", "至今", "县处级副职",
     "区委常委。"),
    ("yixiu_pan_changzhou", "yixiu_party", "宜秀区委常委", "至今", "至今", "县处级副职",
     "具体分工待确认。"),
    ("yixiu_zhou_li", "yixiu_gov", "宜秀区副区长", "至今", "至今", "县处级副职",
     "副区长（区委常委兼任）。"),
    ("yixiu_zhou_li", "yixiu_party", "宜秀区委常委", "至今", "至今", "县处级副职",
     "区委常委。"),
    ("yixiu_zhu_zhen", "yixiu_party", "宜秀区委常委", "至今", "至今", "县处级副职",
     "具体分工待确认。"),
    ("yixiu_yu_yang", "yixiu_party", "宜秀区委常委", "至今", "至今", "县处级副职",
     "具体分工待确认。"),

    # ═══ 区政府领导（非区委常委） ═══
    ("yixiu_zhang_hong", "yixiu_gov", "宜秀区副区长", "至今", "至今", "县处级副职",
     "副区长。"),
    ("yixiu_xu_jinbin", "yixiu_gov", "宜秀区副区长", "至今", "至今", "县处级副职",
     "副区长。"),
    ("yixiu_zha_changli", "yixiu_gov", "宜秀区副区长", "至今", "至今", "县处级副职",
     "副区长。"),
    ("yixiu_he_tianlong", "yixiu_gov", "宜秀区副区长", "至今", "至今", "县处级副职",
     "副区长。"),

    # ═══ 人大政协 ═══
    ("yixiu_cao_hongbin", "yixiu_npc", "宜秀区人大常委会主任（推定）", "至今", "至今", "县处级正职",
     "推定区人大常委会主任（依据党代会主席台座次）。"),
    ("yixiu_cao_aiqun", "yixiu_cppcc", "宜秀区政协主席（推定）", "至今", "至今", "县处级正职",
     "推定区政协主席（依据党代会主席台座次）。"),

    # ═══ 市级领导连接 ═══
    ("anqing_meng_jingwei", "anqing_party", "安庆市委书记", "2025-08", "至今", "厅级正职",
     "2025年8月跨省调任安庆市委书记。"),
    ("anqing_zhang_junyi", "anqing_gov", "安庆市长", "2021-08", "至今", "厅级正职",
     "2021年8月起任安庆市长。"),
]

# ── Relationships ────────────────────────────────────────────────────
relationships = [
    # 上下级关系：王良宜—黄震（区委书记—区长，党政主要领导）
    {
        "person_a": "yixiu_wang_liangyi",
        "person_b": "yixiu_huang_zhen",
        "type": "superior_subordinate",
        "strength": "strong",
        "context": "党政主要领导关系：区委书记和区长搭班子",
        "overlap_org": "中共安庆市宜秀区委员会/宜秀区人民政府",
        "overlap_period": "2026-06至今",
        "note": "confirmed"
    },
    # 区委常委同事关系
    {
        "person_a": "yixiu_wang_liangyi",
        "person_b": "yixiu_liu_xiufang",
        "type": "overlap",
        "strength": "strong",
        "context": "区委书记和区委常委",
        "overlap_org": "中共安庆市宜秀区委员会",
        "overlap_period": "2026-06至今",
        "note": "confirmed"
    },
    {
        "person_a": "yixiu_wang_liangyi",
        "person_b": "yixiu_fang_sheng",
        "type": "overlap",
        "strength": "strong",
        "context": "区委书记和区委常委",
        "overlap_org": "中共安庆市宜秀区委员会",
        "overlap_period": "2026-06至今",
        "note": "confirmed"
    },
    {
        "person_a": "yixiu_wang_liangyi",
        "person_b": "yixiu_zhang_ting",
        "type": "overlap",
        "strength": "strong",
        "context": "区委书记和区委常委",
        "overlap_org": "中共安庆市宜秀区委员会",
        "overlap_period": "2026-06至今",
        "note": "confirmed"
    },
    {
        "person_a": "yixiu_wang_liangyi",
        "person_b": "yixiu_zhu_yuansong",
        "type": "overlap",
        "strength": "strong",
        "context": "区委书记和区委常委",
        "overlap_org": "中共安庆市宜秀区委员会",
        "overlap_period": "2026-06至今",
        "note": "confirmed"
    },
    {
        "person_a": "yixiu_wang_liangyi",
        "person_b": "yixiu_zhou_li",
        "type": "overlap",
        "strength": "strong",
        "context": "区委书记和区委常委/副区长",
        "overlap_org": "中共安庆市宜秀区委员会",
        "overlap_period": "2026-06至今",
        "note": "confirmed"
    },
    # 上下级关系：王良宜—孟景伟（市委书记—区委书记）
    {
        "person_a": "anqing_meng_jingwei",
        "person_b": "yixiu_wang_liangyi",
        "type": "superior_subordinate",
        "strength": "medium",
        "context": "市委书记和区委书记（上下级关系）",
        "overlap_org": "中共安庆市委员会/中共宜秀区委",
        "overlap_period": "2026-06至今",
        "note": "confirmed"
    },
    # 上下级关系：王良宜—张君毅
    {
        "person_a": "anqing_zhang_junyi",
        "person_b": "yixiu_wang_liangyi",
        "type": "superior_subordinate",
        "strength": "medium",
        "context": "市长和区委书记（上下级关系）",
        "overlap_org": "安庆市人民政府/中共宜秀区委",
        "overlap_period": "2026-06至今",
        "note": "confirmed"
    },
    # 黄震领导区政府
    {
        "person_a": "yixiu_huang_zhen",
        "person_b": "yixiu_zhang_ting",
        "type": "superior_subordinate",
        "strength": "strong",
        "context": "区长和副区长",
        "overlap_org": "宜秀区人民政府",
        "overlap_period": "至今",
        "note": "confirmed"
    },
    {
        "person_a": "yixiu_huang_zhen",
        "person_b": "yixiu_zhu_yuansong",
        "type": "superior_subordinate",
        "strength": "strong",
        "context": "区长和副区长",
        "overlap_org": "宜秀区人民政府",
        "overlap_period": "至今",
        "note": "confirmed"
    },
    {
        "person_a": "yixiu_huang_zhen",
        "person_b": "yixiu_zhou_li",
        "type": "superior_subordinate",
        "strength": "strong",
        "context": "区长和副区长",
        "overlap_org": "宜秀区人民政府",
        "overlap_period": "至今",
        "note": "confirmed"
    },
    {
        "person_a": "yixiu_huang_zhen",
        "person_b": "yixiu_zhang_hong",
        "type": "superior_subordinate",
        "strength": "strong",
        "context": "区长和副区长",
        "overlap_org": "宜秀区人民政府",
        "overlap_period": "至今",
        "note": "confirmed"
    },
    {
        "person_a": "yixiu_huang_zhen",
        "person_b": "yixiu_xu_jinbin",
        "type": "superior_subordinate",
        "strength": "strong",
        "context": "区长和副区长",
        "overlap_org": "宜秀区人民政府",
        "overlap_period": "至今",
        "note": "confirmed"
    },
    {
        "person_a": "yixiu_huang_zhen",
        "person_b": "yixiu_zha_changli",
        "type": "superior_subordinate",
        "strength": "strong",
        "context": "区长和副区长",
        "overlap_org": "宜秀区人民政府",
        "overlap_period": "至今",
        "note": "confirmed"
    },
    {
        "person_a": "yixiu_huang_zhen",
        "person_b": "yixiu_he_tianlong",
        "type": "superior_subordinate",
        "strength": "strong",
        "context": "区长和副区长",
        "overlap_org": "宜秀区人民政府",
        "overlap_period": "至今",
        "note": "confirmed"
    },
]


# ══════════════════════════════════════════════════════════════════════
# Database + Graph Builder
# ══════════════════════════════════════════════════════════════════════

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    """Return r,g,b color string based on role."""
    name = p.get("current_post", "")
    if "区委书记" in name:
        return "255,50,50"
    elif "区长" in name:
        return "50,100,255"
    elif "纪委书记" in name or "纪委" in name:
        return "255,165,0"
    else:
        return "100,100,100"


def org_color(o):
    """Return r,g,b color string based on org type."""
    t = o["type"]
    if "党委" in t:
        return "255,200,200"
    elif "政府" in t:
        return "200,200,255"
    elif "纪委" in t:
        return "255,165,0"
    elif "人大" in t:
        return "200,255,255"
    elif "政协" in t:
        return "255,240,200"
    elif "群团" in t:
        return "255,220,255"
    else:
        return "220,220,220"


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
        person_id, org_id, title, start, end, rank, note = pos[:7]
        c.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (person_id, org_id, title, start, end, rank, note))

    for r in relationships:
        c.execute("""
            INSERT INTO relationships (person_a, person_b, type, strength, context, overlap_org, overlap_period, note)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r["type"], r["strength"],
              r["context"], r["overlap_org"], r["overlap_period"], r["note"]))

    conn.commit()
    conn.close()
    print(f"[DB] Created: {DB_PATH}")


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>宜秀区（安庆市）领导班子工作关系网络 — 2026年7月研究数据</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attribute declarations
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="strength" type="string"/>')
    lines.append('      <attribute id="2" title="context" type="string"/>')
    lines.append('      <attribute id="3" title="period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes: persons
    lines.append('    <nodes>')
    for p in persons:
        pid = p["id"]
        name = p["name"]
        post = p["current_post"]
        org = p["current_org"]
        birth = p["birth"]
        conf = p["confidence"]
        c = person_color(p)
        is_top = "区委书记" in post or ("区长" in post and "副书记" in post)
        sz = "20.0" if is_top else "12.0"

        lines.append(f'      <node id="{esc(pid)}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(post)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(org)}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(birth)}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(conf)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Nodes: organizations
    lines.append('    <nodes>')
    for o in organizations:
        oid = o["id"]
        name = o["name"]
        c = org_color(o)
        lines.append(f'      <node id="org_{esc(oid)}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["parent"])}"/>')
        lines.append('          <attvalue for="3" value=""/>')
        lines.append('          <attvalue for="4" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges: person → organization (worked_at)
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        person_id, org_id, title, start, end, rank, note = pos[:7]
        lines.append(f'      <edge id="e{eid}" source="{esc(person_id)}" target="org_{esc(org_id)}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append('          <attvalue for="1" value="1.0"/>')
        lines.append(f'          <attvalue for="2" value="{esc(title)}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(start)}-{esc(end)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Edges: person ↔ person (relationship)
    for r in relationships:
        weight = "2.0" if r["strength"] == "strong" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="{esc(r["person_a"])}" target="{esc(r["person_b"])}" label="{esc(r["context"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["strength"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[GEXF] Created: {GEXF_PATH}")


def print_summary():
    print(f"\n{'='*60}")
    print(f"  宜秀区领导班子工作关系网络")
    print(f"  生成日期: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}")
    print(f"  Persons:         {len(persons)}")
    print(f"  Organizations:   {len(organizations)}")
    print(f"  Positions:       {len(positions)}")
    print(f"  Relationships:   {len(relationships)}")
    print(f"{'='*60}")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    build_db()
    build_gexf()
    print_summary()
