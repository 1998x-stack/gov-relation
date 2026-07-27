#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
惠东县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 广东省
Parent City: 惠州市
Region: 惠东县
Targets: 县委书记 & 县长

Research Sources:
- 惠东县人民政府门户网站 (www.huidong.gov.cn) — 领导之窗
  - 中共惠东县委: http://www.huidong.gov.cn/hdxwz/zwgk/zzjg/ldzc/zghdxw/
  - 惠东县人民政府: http://www.huidong.gov.cn/hdxwz/zwgk/zzjg/ldzc/hdxrmzf/
  - 惠东县政协: http://www.huidong.gov.cn/hdxwz/zwgk/zzjg/ldzc/zxhdwyh/
  - 惠东县纪委: http://www.huidong.gov.cn/hdxwz/zwgk/zzjg/ldzc/zghdjw/
- 惠州市政府官网领导之窗 (www.huizhou.gov.cn)
- 数据采集日期: 2026-07-22

Current status (as of 2026-07-22):
- 县委书记: 黎炳盛（惠州市委常委、惠东县委书记）
  - 男，汉族，1976年2月生，研究生，中共党员
  - 兼任惠州市委常委，confirmed from huidong.gov.cn 领导之窗
- 县长: 徐永强（惠东县委副书记、县政府党组书记、县长）
  - 男，汉族，1980年12月生，大学，中共党员
  - confirmed from huidong.gov.cn 领导之窗
- 县委副书记: 蔡柳锋（专职、政法委书记）、谭军（挂职）
- 县委常委: 黎炳盛、徐永强、蔡柳锋、谭军、陈永兵（常务副县长）、林锦来（宣传部部长）、
            黄艺（组织部部长）、黄钦（纪委书记）、张志勇（副县长）、廖高平（人武部政委）、
            张宁渤（县委办主任）、沈改（统战部部长）、白剑冰（副县长挂职）
- 副县长: 徐永强（县长）、陈永兵（常务）、张志勇、白剑冰（挂职）、周建方、黄卓豪（公安局长）、
          张海平、肖开斌、张焕俊（白花镇党委书记）

Evidence Note: Leadership roster confirmed from official government website (www.huidong.gov.cn)
leadership window pages. Biographical details from official resume snippets on the same site.
Detailed career timelines for most figures still need external source collection; marked accordingly.

Research Date: 2026-07-22
"""

import os
import sys
from datetime import datetime

# Allow import from repo root
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Slug & Paths (for staging) ──
SLUG = "惠东县"
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════════
    # 县委领导
    # ════════════════════════════════════════════
    {
        "id": 1,
        "name": "黎炳盛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年2月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "惠州市委常委、惠东县委书记",
        "current_org": "中共惠东县委员会",
        "source": "惠东县政府官网领导之窗 (confirmed) — 县委常委、县委书记，惠州市委常委"
    },
    {
        "id": 2,
        "name": "徐永强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年12月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "惠东县委副书记、县政府党组书记、县长",
        "current_org": "惠东县人民政府",
        "source": "惠东县政府官网领导之窗 (confirmed) — 县委副书记、县长"
    },
    {
        "id": 3,
        "name": "蔡柳锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年10月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "惠东县委副书记、政法委书记，二级调研员",
        "current_org": "中共惠东县委员会",
        "source": "惠东县政府官网领导之窗 (confirmed) — 县委副书记、政法委书记"
    },
    {
        "id": 4,
        "name": "谭军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年10月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "惠东县委副书记（挂职）",
        "current_org": "中共惠东县委员会",
        "source": "惠东县政府官网领导之窗 (confirmed) — 县委副书记（挂职）"
    },
    {
        "id": 5,
        "name": "陈永兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年10月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "惠东县委常委，县政府党组副书记、常务副县长，三级调研员",
        "current_org": "惠东县人民政府",
        "source": "惠东县政府官网领导之窗 (confirmed) — 县委常委、常务副县长"
    },
    {
        "id": 6,
        "name": "林锦来",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "1980年3月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "惠东县委常委、宣传部部长，三级调研员",
        "current_org": "中共惠东县委员会",
        "source": "惠东县政府官网领导之窗 (confirmed) — 县委常委、宣传部部长"
    },
    {
        "id": 7,
        "name": "黄艺",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年2月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "惠东县委常委、组织部部长、党校校长，三级调研员",
        "current_org": "中共惠东县委员会",
        "source": "惠东县政府官网领导之窗 (confirmed) — 县委常委、组织部部长"
    },
    {
        "id": 8,
        "name": "黄钦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年6月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "硕士研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "惠东县委常委、县纪委书记、县监委主任，四级高级监察官",
        "current_org": "中共惠东县纪律检查委员会",
        "source": "惠东县政府官网领导之窗 (confirmed) — 县委常委、县纪委书记"
    },
    {
        "id": 9,
        "name": "张志勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年10月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "惠东县委常委，县政府副县长，三级调研员",
        "current_org": "惠东县人民政府",
        "source": "惠东县政府官网领导之窗 (confirmed) — 县委常委、副县长（分管自然资源、交通）"
    },
    {
        "id": 10,
        "name": "廖高平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年1月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "惠东县委常委、县人武部上校政治委员",
        "current_org": "惠东县人民武装部",
        "source": "惠东县政府官网领导之窗 (confirmed) — 县委常委、人武部政委"
    },
    {
        "id": 11,
        "name": "张宁渤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年8月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "惠东县委常委、县委办公室主任、县直属机关工作委员会书记",
        "current_org": "中共惠东县委员会",
        "source": "惠东县政府官网领导之窗 (confirmed) — 县委常委、县委办主任"
    },
    {
        "id": 12,
        "name": "沈改",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1978年10月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大专",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "惠东县委常委、统战部部长，九龙峰旅游区党工委书记",
        "current_org": "中共惠东县委员会",
        "source": "惠东县政府官网领导之窗 (confirmed) — 县委常委、统战部部长"
    },
    {
        "id": 13,
        "name": "白剑冰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年4月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "惠东县委常委、副县长（挂职）",
        "current_org": "惠东县人民政府",
        "source": "惠东县政府官网领导之窗 (confirmed) — 县委常委、副县长（挂职）"
    },
    # ════════════════════════════════════════════
    # 县政府其他领导
    # ════════════════════════════════════════════
    {
        "id": 14,
        "name": "周建方",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年10月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "惠东县政府党组成员、副县长，三级调研员",
        "current_org": "惠东县人民政府",
        "source": "惠东县政府官网领导之窗 (confirmed) — 副县长（分管农业农村）"
    },
    {
        "id": 15,
        "name": "黄卓豪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年10月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "惠东县政府党组成员、副县长，县公安局党委书记、局长",
        "current_org": "惠东县人民政府",
        "source": "惠东县政府官网领导之窗 (confirmed) — 副县长、公安局长"
    },
    {
        "id": 16,
        "name": "张海平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年11月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "惠东县政府党组成员、副县长",
        "current_org": "惠东县人民政府",
        "source": "惠东县政府官网领导之窗 (confirmed) — 副县长（分管科工信息、招商）"
    },
    {
        "id": 17,
        "name": "肖开斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年8月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "惠东县政府党组成员、副县长",
        "current_org": "惠东县人民政府",
        "source": "惠东县政府官网领导之窗 (confirmed) — 副县长（分管教育、住建）"
    },
    {
        "id": 18,
        "name": "张焕俊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985年4月",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "惠东县政府党组成员、副县长，白花镇党委书记",
        "current_org": "惠东县人民政府",
        "source": "惠东县政府官网领导之窗 (confirmed) — 副县长、白花镇党委书记"
    },
    # ════════════════════════════════════════════
    # 县人大领导
    # ════════════════════════════════════════════
    {
        "id": 19,
        "name": "田建容",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "惠东县人大常委会主任",
        "current_org": "惠东县人大常委会",
        "source": "惠东县政府官网 (confirmed) — 县人大常委会主任（源自新闻提及及人大网页）"
    },
    # ════════════════════════════════════════════
    # 县政协领导
    # ════════════════════════════════════════════
    {
        "id": 20,
        "name": "钟东海",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "native_place": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "惠东县政协主席",
        "current_org": "政协惠东县委员会",
        "source": "惠东县政府官网领导之窗 (confirmed) — 县政协主席"
    },
]

# 2. Organizations
organizations = [
    {"id": 1, "name": "中共惠东县委员会", "type": "党委", "level": "县", "parent": "中共惠州市委员会", "location": "惠东县"},
    {"id": 2, "name": "惠东县人民政府", "type": "政府", "level": "县", "parent": "惠州市人民政府", "location": "惠东县"},
    {"id": 3, "name": "中共惠东县纪律检查委员会", "type": "党委", "level": "县", "parent": "中共惠东县委员会", "location": "惠东县"},
    {"id": 4, "name": "惠东县人大常委会", "type": "人大", "level": "县", "parent": "惠州市人大常委会", "location": "惠东县"},
    {"id": 5, "name": "政协惠东县委员会", "type": "政协", "level": "县", "parent": "政协惠州市委员会", "location": "惠东县"},
    {"id": 6, "name": "中共惠东县委政法委员会", "type": "党委", "level": "县", "parent": "中共惠东县委员会", "location": "惠东县"},
    {"id": 7, "name": "中共惠东县委宣传部", "type": "党委", "level": "县", "parent": "中共惠东县委员会", "location": "惠东县"},
    {"id": 8, "name": "中共惠东县委组织部", "type": "党委", "level": "县", "parent": "中共惠东县委员会", "location": "惠东县"},
    {"id": 9, "name": "中共惠东县委统一战线工作部", "type": "党委", "level": "县", "parent": "中共惠东县委员会", "location": "惠东县"},
    {"id": 10, "name": "中共惠东县委办公室", "type": "党委", "level": "县", "parent": "中共惠东县委员会", "location": "惠东县"},
    {"id": 11, "name": "惠东县人民武装部", "type": "政府", "level": "县", "parent": "惠州军分区", "location": "惠东县"},
    {"id": 12, "name": "惠东县公安局", "type": "政府", "level": "县", "parent": "惠东县人民政府", "location": "惠东县"},
    {"id": 13, "name": "白花镇人民政府", "type": "乡镇/街道", "level": "乡镇", "parent": "惠东县人民政府", "location": "惠东县白花镇"},
    {"id": 14, "name": "九龙峰旅游区", "type": "事业单位", "level": "乡镇", "parent": "惠东县人民政府", "location": "惠东县"},
    {"id": 15, "name": "中共惠州市委员会", "type": "党委", "level": "地级市", "parent": "中共广东省委员会", "location": "惠州市"},
]

# 3. Positions
positions = [
    # 黎炳盛 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "惠州市委常委、惠东县委书记", "start_date": "待查", "end_date": "至今", "rank": "副厅级", "note": "惠州市委常委兼任惠东县委书记"},
    # 徐永强 — 县长
    {"person_id": 2, "org_id": 2, "title": "惠东县委副书记、县政府党组书记、县长", "start_date": "待查", "end_date": "至今", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "惠东县委副书记", "start_date": "待查", "end_date": "至今", "rank": "正处级", "note": ""},
    # 蔡柳锋 — 专职副书记、政法委书记
    {"person_id": 3, "org_id": 1, "title": "惠东县委副书记、政法委书记", "start_date": "待查", "end_date": "至今", "rank": "正处级（二级调研员）", "note": ""},
    {"person_id": 3, "org_id": 6, "title": "惠东县委政法委书记", "start_date": "待查", "end_date": "至今", "rank": "正处级", "note": ""},
    # 谭军 — 挂职副书记
    {"person_id": 4, "org_id": 1, "title": "惠东县委副书记（挂职）", "start_date": "待查", "end_date": "至今", "rank": "正处级", "note": "挂职"},
    # 陈永兵 — 常务副县长
    {"person_id": 5, "org_id": 2, "title": "惠东县委常委、县政府党组副书记、常务副县长", "start_date": "待查", "end_date": "至今", "rank": "副处级（三级调研员）", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "惠东县委常委", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": ""},
    # 林锦来 — 宣传部部长
    {"person_id": 6, "org_id": 1, "title": "惠东县委常委、宣传部部长", "start_date": "待查", "end_date": "至今", "rank": "副处级（三级调研员）", "note": ""},
    {"person_id": 6, "org_id": 7, "title": "惠东县委宣传部部长", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": ""},
    # 黄艺 — 组织部部长
    {"person_id": 7, "org_id": 1, "title": "惠东县委常委、组织部部长、党校校长", "start_date": "待查", "end_date": "至今", "rank": "副处级（三级调研员）", "note": ""},
    {"person_id": 7, "org_id": 8, "title": "惠东县委组织部部长", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": ""},
    # 黄钦 — 纪委书记
    {"person_id": 8, "org_id": 3, "title": "惠东县委常委、县纪委书记、县监委主任", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": "四级高级监察官"},
    {"person_id": 8, "org_id": 1, "title": "惠东县委常委", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": ""},
    # 张志勇 — 副县长
    {"person_id": 9, "org_id": 2, "title": "惠东县委常委、县政府副县长", "start_date": "待查", "end_date": "至今", "rank": "副处级（三级调研员）", "note": "分管自然资源、交通"},
    {"person_id": 9, "org_id": 1, "title": "惠东县委常委", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": ""},
    # 廖高平 — 人武部政委
    {"person_id": 10, "org_id": 1, "title": "惠东县委常委、县人武部上校政治委员", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 11, "title": "惠东县人武部上校政治委员", "start_date": "待查", "end_date": "至今", "rank": "上校", "note": ""},
    # 张宁渤 — 县委办主任
    {"person_id": 11, "org_id": 1, "title": "惠东县委常委、县委办公室主任", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": "兼县直属机关工作委员会书记"},
    {"person_id": 11, "org_id": 10, "title": "惠东县委办公室主任", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": ""},
    # 沈改 — 统战部部长
    {"person_id": 12, "org_id": 1, "title": "惠东县委常委、统战部部长", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": "兼九龙峰旅游区党工委书记"},
    {"person_id": 12, "org_id": 9, "title": "惠东县委统战部部长", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 14, "title": "九龙峰旅游区党工委书记", "start_date": "待查", "end_date": "至今", "rank": "正科级", "note": ""},
    # 白剑冰 — 挂职副县长
    {"person_id": 13, "org_id": 2, "title": "惠东县委常委、副县长（挂职）", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": "挂职"},
    {"person_id": 13, "org_id": 1, "title": "惠东县委常委", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": "挂职"},
    # 周建方 — 副县长
    {"person_id": 14, "org_id": 2, "title": "惠东县政府党组成员、副县长", "start_date": "待查", "end_date": "至今", "rank": "副处级（三级调研员）", "note": "分管农业农村"},
    # 黄卓豪 — 副县长、公安局长
    {"person_id": 15, "org_id": 2, "title": "惠东县政府党组成员、副县长", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": "兼公安局党委书记、局长"},
    {"person_id": 15, "org_id": 12, "title": "惠东县公安局党委书记、局长", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": ""},
    # 张海平 — 副县长
    {"person_id": 16, "org_id": 2, "title": "惠东县政府党组成员、副县长", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": "分管科工信息、招商"},
    # 肖开斌 — 副县长
    {"person_id": 17, "org_id": 2, "title": "惠东县政府党组成员、副县长", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": "分管教育、住建"},
    # 张焕俊 — 副县长、白花镇党委书记
    {"person_id": 18, "org_id": 2, "title": "惠东县政府党组成员、副县长", "start_date": "待查", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 18, "org_id": 13, "title": "白花镇党委书记", "start_date": "待查", "end_date": "至今", "rank": "正科级", "note": ""},
    # 田建容 — 人大常委会主任
    {"person_id": 19, "org_id": 4, "title": "惠东县人大常委会主任", "start_date": "待查", "end_date": "至今", "rank": "正处级", "note": ""},
    # 钟东海 — 政协主席
    {"person_id": 20, "org_id": 5, "title": "惠东县政协主席", "start_date": "待查", "end_date": "至今", "rank": "正处级", "note": ""},
]

# 4. Relationships (person-to-person)
relationships = [
    # 黎炳盛 <-> 徐永强 — 党政一把手
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "县委书记与县长党政搭档", "overlap_org": "中共惠东县委员会/惠东县人民政府",
     "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    # 黎炳盛 <-> 蔡柳锋 — 书记与副书记
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "县委书记与专职副书记", "overlap_org": "中共惠东县委员会",
     "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    # 黎炳盛 <-> 陈永兵 — 书记与常务副县长
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "县委书记与县委常委、常务副县长", "overlap_org": "中共惠东县委员会",
     "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},
    # 徐永强 <-> 陈永兵 — 县长与常务副县长
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "县长与常务副县长（县政府党组正副书记）", "overlap_org": "惠东县人民政府",
     "overlap_period": "至今", "strength": "strong", "confidence": "confirmed"},
    # 黎炳盛 <-> 黄钦 — 书记与纪委书记
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate",
     "context": "县委书记与县纪委书记", "overlap_org": "中共惠东县委员会",
     "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},
    # 蔡柳锋 <-> 谭军 — 两位副书记
    {"person_a": 3, "person_b": 4, "type": "overlap",
     "context": "县委专职副书记与挂职副书记", "overlap_org": "中共惠东县委员会",
     "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},
    # 黄艺 <-> 林锦来 — 组织部与宣传部
    {"person_a": 7, "person_b": 6, "type": "overlap",
     "context": "县委常委、组织部部长与宣传部部长", "overlap_org": "中共惠东县委员会",
     "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},
    # 黎炳盛 <-> 田建容 — 县委与人大
    {"person_a": 1, "person_b": 19, "type": "overlap",
     "context": "县委书记与县人大常委会主任", "overlap_org": "惠东县",
     "overlap_period": "至今", "strength": "medium", "confidence": "plausible"},
    # 黎炳盛 <-> 钟东海 — 县委与政协
    {"person_a": 1, "person_b": 20, "type": "overlap",
     "context": "县委书记与县政协主席", "overlap_org": "惠东县",
     "overlap_period": "至今", "strength": "medium", "confidence": "plausible"},
    # 徐永强 <-> 黄卓豪 — 县长与公安局长
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate",
     "context": "县长与副县长、公安局长", "overlap_org": "惠东县人民政府",
     "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},
    # 张海平 <-> 陈永兵 — 协管关系
    {"person_a": 5, "person_b": 16, "type": "superior_subordinate",
     "context": "常务副县长与副县长（张海平协助陈永兵处理统计等工作）", "overlap_org": "惠东县人民政府",
     "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},
    # 徐永强 <-> 张焕俊 — 县长与副县长/镇委书记
    {"person_a": 2, "person_b": 18, "type": "superior_subordinate",
     "context": "县长与副县长（白花镇党委书记）", "overlap_org": "惠东县人民政府",
     "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},
    # 县委常委全体 — 常委会班子成员
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "县委常委班子成员", "overlap_org": "中共惠东县委员会常务委员会",
     "overlap_period": "至今", "strength": "medium", "confidence": "confirmed"},
]

# 5. Run Build
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
    print(f"✅ Build complete: {DB_PATH}")
    print(f"✅ Build complete: {GEXF_PATH}")
    print(f"   Persons: {len(persons)}")
    print(f"   Organizations: {len(organizations)}")
    print(f"   Positions: {len(positions)}")
    print(f"   Relationships: {len(relationships)}")
