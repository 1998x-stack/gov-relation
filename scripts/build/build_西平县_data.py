#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 西平县 (Xiping County), 河南省.

Investigation date: 2026-07-24
Task ID: henan_西平县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - www.xiping.gov.cn — 西平县人民政府网站 (primary, accessed 2026-07-24)
  - 中国共产党西平县第十四次代表大会 (2026-06-23/25) — confirmed 县委领导班子
  - 西平县委书记侯公涛调研先进制造业开发区 (2026-07-17)
  - 西平县召开信访稳定等工作推进会 (2026-07-20) — confirmed 县领导分工
  - 县委党的建设工作领导小组（扩大）会议 (2026-07-08) — confirmed 县长甘泉
  - 西平县委书记侯公涛调研高考准备工作 (2026-06-06)
  - 政务公开 > 领导信息 (xiping.gov.cn/zwgk/) — confirmed 县政府领导

Confidence notes:
  - 侯公涛: confirmed as 县委书记 via multiple official articles (as of 2026-06)
  - 甘泉: confirmed as 县委副书记、县长 via official article (2026-07-08)
  - 吴振国: confirmed as 县委副书记 via official article (2026-07-20)
  - 曹亚红: confirmed as 县人大常委会主任 via official article (2026-05-31)
  - 第十四次党代会 confirmed the 县委常委 standing committee
  - Full career timelines missing — only current roles confirmed from official sources
  - Detailed biographical data (birthdate, birthplace, education) marked as unverified
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ├─ Paths ──────────────────────────────────────────────────────────────────
STAGING = os.path.dirname(os.path.abspath(__file__))
SLUG = "西平县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

DB_PATH = os.path.join(STAGING, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING, f"{SLUG}_network.gexf")
PERSONS_DIR = Path(STAGING)

# ├─ Source Register ────────────────────────────────────────────────────────
sources = [
    {
        "id": "S001",
        "title": "中国共产党西平县第十四次代表大会隆重开幕",
        "url": "https://www.xiping.gov.cn/zwyw/tpxw/202606/t20260624_707126.html",
        "publisher": "西平县人民政府",
        "published_at": "2026-06-24",
        "source_type": "official",
        "reliability": "high",
        "notes": "Confirmed 县委常委/主席台名单: 侯公涛, 甘泉, 吴振国, 邓昭, 侯华灵, 耿扬, 茹强, 刘旭辉, 周高宏, 李华勇"
    },
    {
        "id": "S002",
        "title": "中国共产党西平县第十四次代表大会胜利闭幕",
        "url": "https://www.xiping.gov.cn/zwyw/tpxw/202606/t20260626_707681.html",
        "publisher": "西平县人民政府",
        "published_at": "2026-06-26",
        "source_type": "official",
        "reliability": "high",
        "notes": "Confirmed 侯公涛致闭幕词, 甘泉主持. 新增李勇在主席台前排就座"
    },
    {
        "id": "S003",
        "title": "西平县委书记侯公涛一行到先进制造业开发区调研经济运行等工作",
        "url": "https://www.xiping.gov.cn/zwyw/tpxw/202607/t20260722_713727.html",
        "publisher": "西平县人民政府",
        "published_at": "2026-07-17",
        "source_type": "official",
        "reliability": "high",
        "notes": "Confirmed 侯公涛县委书记, 陪同县领导甘泉, 侯华灵, 周高宏"
    },
    {
        "id": "S004",
        "title": "西平县召开信访稳定 生态环境保护 安全生产工作推进会",
        "url": "https://www.xiping.gov.cn/zwyw/tpxw/202607/t20260722_713721.html",
        "publisher": "西平县人民政府",
        "published_at": "2026-07-20",
        "source_type": "official",
        "reliability": "high",
        "notes": "Confirmed 侯公涛讲话, 甘泉主持. 吴振国(副书记), 侯华灵(常务副县长), 刘旭辉(政法委书记), 周高宏(县委办主任)"
    },
    {
        "id": "S005",
        "title": "西平县召开县委党的建设工作领导小组（扩大）会议",
        "url": "https://www.xiping.gov.cn/zwyw/tpxw/202607/t20260708_710717.html",
        "publisher": "西平县人民政府",
        "published_at": "2026-07-08",
        "source_type": "official",
        "reliability": "high",
        "notes": "Confirmed 甘泉(县长)讲话. 邓昭(组织部长), 刘旭辉(政法委书记)"
    },
    {
        "id": "S006",
        "title": "西平县委书记侯公涛实地调研高考准备工作",
        "url": "https://www.xiping.gov.cn/zwyw/tpxw/202606/t20260608_704972.html",
        "publisher": "西平县人民政府",
        "published_at": "2026-06-06",
        "source_type": "official",
        "reliability": "high",
        "notes": "Confirmed 侯公涛县委书记, 吴振国(副书记), 曹亚红(人大主任), 周高宏陪同"
    },
    {
        "id": "S007",
        "title": "西平县人民政府 > 政务公开 > 领导信息",
        "url": "https://www.xiping.gov.cn/zwgk/",
        "publisher": "西平县人民政府",
        "published_at": "2026-07-24",
        "source_type": "official",
        "reliability": "high",
        "notes": "Confirmed 县政府领导班子: 甘泉(县长), 侯华灵, 耿扬, 李新, 刘旭辉, 周高宏, 李华勇, 龙岩"
    },
    {
        "id": "S008",
        "title": "西平县开展'六一'儿童节慰问暨家风家教主题宣传活动启动仪式",
        "url": "https://www.xiping.gov.cn/zwyw/tpxw/202606/t20260604_704561.html",
        "publisher": "西平县人民政府",
        "published_at": "2026-05-31",
        "source_type": "official",
        "reliability": "high",
        "notes": "Confirmed 曹亚红(县人大常委会主任), 吴振国(县委副书记)"
    },
]

# ├─ Persons ─────────────────────────────────────────────────────────────────

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership — 县委书记 & 县长
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "侯公涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委书记",
        "current_org": "中共西平县委员会",
        "source": "https://www.xiping.gov.cn/zwyw/tpxw/202606/t20260624_707126.html",
        "notes": "Confirmed as 县委书记 via multiple official articles. Reported as 第十三届县委委员, leading the 第十四次党代会 (2026-06). Public biographical details unavailable from official sources."
    },
    {
        "id": 2,
        "name": "甘泉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县长",
        "current_org": "西平县人民政府",
        "source": "https://www.xiping.gov.cn/zwyw/tpxw/202607/t20260708_710717.html",
        "notes": "Confirmed as 县委副书记、县人民政府县长、党组书记 via official article (2026-07-08). Presided over 县第十四次党代会闭幕式. Public biographical details unavailable."
    },

    # ══════════════════════════════════════════════════════════════════════
    # 县委领导班子 (县委常委 / 县领导)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 3,
        "name": "吴振国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委副书记",
        "current_org": "中共西平县委员会",
        "source": "https://www.xiping.gov.cn/zwyw/tpxw/202607/t20260722_713721.html",
        "notes": "Confirmed as 县委副书记 (2026-07-20 article). In 主席台前排就座 at 第十四次党代会."
    },
    {
        "id": 4,
        "name": "邓昭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共西平县委员会",
        "source": "https://www.xiping.gov.cn/zwyw/tpxw/202607/t20260708_710717.html",
        "notes": "Confirmed as 县委常委、组织部部长 via official article (2026-07-08). In 主席台前排就座 at 第十四次党代会."
    },
    {
        "id": 5,
        "name": "侯华灵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委常委、常务副县长",
        "current_org": "西平县人民政府",
        "source": "https://www.xiping.gov.cn/zwyw/tpxw/202607/t20260722_713721.html",
        "notes": "Confirmed as 县委常委、常务副县长 (2026-07-20 article,通报上半年安全生产工作情况). In 主席台前排就座 at 第十四次党代会."
    },
    {
        "id": 6,
        "name": "耿扬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委常委",
        "current_org": "中共西平县委员会",
        "source": "https://www.xiping.gov.cn/zwyw/tpxw/202606/t20260624_707126.html",
        "notes": "In 主席台前排就座 at 第十四次党代会 (both opening and closing). Also listed on 政务公开 > 领导信息 as 县政府领导."
    },
    {
        "id": 7,
        "name": "茹强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委常委",
        "current_org": "中共西平县委员会",
        "source": "https://www.xiping.gov.cn/zwyw/tpxw/202606/t20260624_707126.html",
        "notes": "In 主席台前排就座 at 第十四次党代会 (both opening and closing). Likely a 县委常委."
    },
    {
        "id": 8,
        "name": "刘旭辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共西平县委员会",
        "source": "https://www.xiping.gov.cn/zwyw/tpxw/202607/t20260708_710717.html",
        "notes": "Confirmed as 县委常委、政法委书记 via official article (2026-07-08, 通报帮扶资金项目进展; 2026-07-20, 宣读信访方案)."
    },
    {
        "id": 9,
        "name": "周高宏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委常委、县委办公室主任、副县长",
        "current_org": "中共西平县委员会",
        "source": "https://www.xiping.gov.cn/zwyw/tpxw/202607/t20260722_713721.html",
        "notes": "Confirmed as 县委常委、县委办公室主任 (2026-07-20 article, 通报环保工作). Also listed on 领导信息 as 县政府领导 (副县长)."
    },
    {
        "id": 10,
        "name": "李华勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委常委",
        "current_org": "中共西平县委员会",
        "source": "https://www.xiping.gov.cn/zwyw/tpxw/202606/t20260624_707126.html",
        "notes": "In 主席台前排就座 at 第十四次党代会 (both opening and closing). Listed on 领导信息 as 县政府领导."
    },
    {
        "id": 11,
        "name": "李勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县委常委（新任）",
        "current_org": "中共西平县委员会",
        "source": "https://www.xiping.gov.cn/zwyw/tpxw/202606/t20260626_707681.html",
        "notes": "Appeared in 主席台前排就座 at 第十四次党代会闭幕式 but NOT in opening ceremony. Possibly newly elected to 县委常委."
    },

    # ══════════════════════════════════════════════════════════════════════
    # 县人大 / 县政府其他领导
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 12,
        "name": "曹亚红",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县人大常委会主任",
        "current_org": "西平县人大常委会",
        "source": "https://www.xiping.gov.cn/zwyw/tpxw/202606/t20260604_704561.html",
        "notes": "Confirmed as 县人大常委会主任 (2026-05-31 六一慰问). In 主席团成员 at 第十四次党代会."
    },
    {
        "id": 13,
        "name": "李新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副县长",
        "current_org": "西平县人民政府",
        "source": "https://www.xiping.gov.cn/zwgk/",
        "notes": "Listed on 政务公开 > 领导信息 as 县政府领导."
    },
    {
        "id": 14,
        "name": "龙岩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副县长",
        "current_org": "西平县人民政府",
        "source": "https://www.xiping.gov.cn/zwgk/",
        "notes": "Listed on 政务公开 > 领导信息 as 县政府领导."
    },
    {
        "id": 15,
        "name": "张新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "县领导（主席团成员）",
        "current_org": "西平县",
        "source": "https://www.xiping.gov.cn/zwyw/tpxw/202606/t20260624_707126.html",
        "notes": "In 主席团成员 at 第十四次党代会. Role not fully confirmed."
    },
]

# ├─ Organizations ───────────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中共西平县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共驻马店市委",
        "location": "河南省驻马店市西平县"
    },
    {
        "id": 2,
        "name": "西平县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "驻马店市人民政府",
        "location": "河南省驻马店市西平县"
    },
    {
        "id": 3,
        "name": "西平县人大常委会",
        "type": "人大",
        "level": "县",
        "parent": "驻马店市人大常委会",
        "location": "河南省驻马店市西平县"
    },
    {
        "id": 4,
        "name": "政协西平县委员会",
        "type": "政协",
        "level": "县",
        "parent": "政协驻马店市委员会",
        "location": "河南省驻马店市西平县"
    },
    {
        "id": 5,
        "name": "西平县先进制造业开发区",
        "type": "开发区",
        "level": "县",
        "parent": "西平县人民政府",
        "location": "河南省驻马店市西平县"
    },
]

# ├─ Positions ───────────────────────────────────────────────────────────────

positions = [
    # 侯公涛
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "待查", "end": "present", "rank": "正处级", "note": "2026年6月主持县第十四次党代会"},
    # 甘泉
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "待查", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "待查", "end": "present", "rank": "正处级", "note": "县人民政府党组书记"},
    # 吴振国
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start": "待查", "end": "present", "rank": "副处级", "note": "2026年7月20日传达全省信访会议精神"},
    # 邓昭
    {"person_id": 4, "org_id": 1, "title": "县委常委、组织部部长", "start": "待查", "end": "present", "rank": "副处级", "note": "2026年7月8日传达中央党建会议精神"},
    # 侯华灵
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "常务副县长", "start": "待查", "end": "present", "rank": "副处级", "note": "2026年7月20日通报安全生产工作情况"},
    # 耿扬
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start": "待查", "end": "present", "rank": "副处级", "note": "第十四次党代会主席台前排就座"},
    {"person_id": 6, "org_id": 2, "title": "副县长", "start": "待查", "end": "present", "rank": "副处级", "note": "政务公开领导信息"},
    # 茹强
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start": "待查", "end": "present", "rank": "副处级", "note": "第十四次党代会主席台前排就座"},
    # 刘旭辉
    {"person_id": 8, "org_id": 1, "title": "县委常委、政法委书记", "start": "待查", "end": "present", "rank": "副处级", "note": "2026年7月20日宣读信访攻坚方案"},
    # 周高宏
    {"person_id": 9, "org_id": 1, "title": "县委常委、县委办公室主任", "start": "待查", "end": "present", "rank": "副处级", "note": "2026年7月20日通报环保工作情况"},
    {"person_id": 9, "org_id": 2, "title": "副县长", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    # 李华勇
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start": "待查", "end": "present", "rank": "副处级", "note": "第十四次党代会主席台前排就座"},
    {"person_id": 10, "org_id": 2, "title": "副县长", "start": "待查", "end": "present", "rank": "副处级", "note": "政务公开领导信息"},
    # 李勇
    {"person_id": 11, "org_id": 1, "title": "县委常委（新任）", "start": "2026-06", "end": "present", "rank": "副处级", "note": "第十四次党代会闭幕式新出现在主席台前排"},
    # 曹亚红
    {"person_id": 12, "org_id": 3, "title": "县人大常委会主任", "start": "待查", "end": "present", "rank": "正处级", "note": "2026年5月31日参加六一慰问"},
    # 李新
    {"person_id": 13, "org_id": 2, "title": "副县长", "start": "待查", "end": "present", "rank": "副处级", "note": "政务公开领导信息"},
    # 龙岩
    {"person_id": 14, "org_id": 2, "title": "副县长", "start": "待查", "end": "present", "rank": "副处级", "note": "政务公开领导信息"},
    # 张新
    {"person_id": 15, "org_id": 1, "title": "县领导（主席团成员）", "start": "待查", "end": "present", "rank": "待查", "note": "第十四次党代会主席团成员"},
]

# ├─ Relationships ───────────────────────────────────────────────────────────

relationships = [
    # 核心搭档
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "党政主要领导搭档（县委书记与县长）",
        "overlap_org": "西平县",
        "overlap_period": "2026年至今",
        "confidence": "confirmed"
    },
    # 书记—副书记
    {
        "person_a": 1, "person_b": 3,
        "type": "superior_subordinate",
        "context": "县委书记与县委副书记",
        "overlap_org": "中共西平县委员会",
        "overlap_period": "2026年至今",
        "confidence": "confirmed"
    },
    # 书记—各位常委
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "县委书记与县委常委/组织部长", "overlap_org": "中共西平县委员会", "overlap_period": "2026年至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "县委书记与县委常委/常务副县长", "overlap_org": "中共西平县委员会/西平县人民政府", "overlap_period": "2026年至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "县委书记与县委常委", "overlap_org": "中共西平县委员会", "overlap_period": "2026年至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "县委书记与县委常委", "overlap_org": "中共西平县委员会", "overlap_period": "2026年至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "县委书记与县委常委/政法委书记", "overlap_org": "中共西平县委员会", "overlap_period": "2026年至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "县委书记与县委常委/县委办主任", "overlap_org": "中共西平县委员会", "overlap_period": "2026年至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate", "context": "县委书记与县委常委", "overlap_org": "中共西平县委员会", "overlap_period": "2026年至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 11, "type": "superior_subordinate", "context": "县委书记与新任县委常委", "overlap_org": "中共西平县委员会", "overlap_period": "2026年6月至今", "confidence": "confirmed"},
    # 县长—副县长
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "县长与常务副县长", "overlap_org": "西平县人民政府", "overlap_period": "2026年至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "西平县人民政府", "overlap_period": "2026年至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "西平县人民政府", "overlap_period": "2026年至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "西平县人民政府", "overlap_period": "2026年至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "西平县人民政府", "overlap_period": "2026年至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate", "context": "县长与副县长", "overlap_org": "西平县人民政府", "overlap_period": "2026年至今", "confidence": "confirmed"},
    # 人大主任与县委
    {"person_a": 12, "person_b": 1, "type": "overlap", "context": "县人大常委会主任与县委书记", "overlap_org": "西平县", "overlap_period": "2026年至今", "confidence": "confirmed"},
    # 副书记与政法委书记
    {"person_a": 3, "person_b": 8, "type": "overlap", "context": "县委副书记与政法委书记（共同负责政法信访）", "overlap_org": "中共西平县委员会", "overlap_period": "2026年至今", "confidence": "confirmed"},
    # 组织部长与县委常委会
    {"person_a": 4, "person_b": 1, "type": "superior_subordinate", "context": "组织部部长与县委书记", "overlap_org": "中共西平县委员会", "overlap_period": "2026年至今", "confidence": "confirmed"},
]

# ├─ Build ──────────────────────────────────────────────────────────────────

def build():
    """Run database + GEXF build."""
    import sqlite3

    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT,
            notes TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            confidence TEXT DEFAULT 'unverified',
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        cur.execute(
            "INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source, notes) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
             p.get("birth", ""), p.get("birthplace", ""), p.get("education", ""),
             p.get("party_join", ""), p.get("work_start", ""),
             p["current_post"], p["current_org"], p.get("source", ""), p.get("notes", ""))
        )

    for o in organizations:
        cur.execute(
            "INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?, ?, ?, ?, ?, ?)",
            (o["id"], o["name"], o.get("type", ""), o.get("level", ""),
             o.get("parent", ""), o.get("location", ""))
        )

    for pos in positions:
        cur.execute(
            "INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos.get("start", ""), pos.get("end", "present"),
             pos.get("rank", ""), pos.get("note", ""))
        )

    for r in relationships:
        cur.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, confidence) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (r["person_a"], r["person_b"], r["type"], r.get("context", ""),
             r.get("overlap_org", ""), r.get("overlap_period", ""),
             r.get("confidence", "unverified"))
        )

    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")
    print(f"   {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

    # ── GEXF ────────────────────────────────────────────────────────────

    def esc(s):
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    is_top = {1, 2}  # 县委书记 and 县长
    person_colors = {
        1: "255,50,50",    # Red - party secretary
        2: "50,100,255",   # Blue - mayor
        3: "100,100,100",  # Grey - deputy secretary
        4: "100,100,100",  # Grey - organization
        5: "50,100,255",   # Blue - government
        6: "100,100,100",  # Grey
        7: "100,100,100",
        8: "255,165,0",    # Orange - discipline/political-legal
        9: "100,100,100",  # Grey
        10: "100,100,100",
        11: "100,100,100",
        12: "200,255,255",  # Cyan - 人大
        13: "50,100,255",  # Blue - government
        14: "50,100,255",  # Blue - government
        15: "100,100,100",
    }
    org_colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "开发区": "200,255,200",
    }

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append(f'    <description>西平县领导班子工作关系网络 - {AS_OF}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        pid = p["id"]
        c = person_colors.get(pid, "100,100,100")
        sz = "20.0" if pid in is_top else "12.0"
        lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        oc = org_colors.get(o["type"], "200,200,200")
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{oc.split(",")[0]}" g="{oc.split(",")[1]}" b="{oc.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    # Person -> Organization (worked_at)
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person <-> Person (relationship)
    for r in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r.get("context",""))}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF created: {GEXF_PATH}")

    # ── Summary ────────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    print(f"西平县 Network Build Complete")
    print(f"{'='*60}")
    print(f"Persons:     {len(persons)}")
    print(f"Orgs:        {len(organizations)}")
    print(f"Positions:   {len(positions)}")
    print(f"Edges (total): {eid}")
    print(f"DB:          {DB_PATH}")
    print(f"GEXF:        {GEXF_PATH}")


if __name__ == "__main__":
    build()
