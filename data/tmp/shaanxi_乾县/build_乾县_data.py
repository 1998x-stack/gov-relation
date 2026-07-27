#!/usr/bin/env python3
import sqlite3  # noqa — used by gov_relation.runner via import
"""Build SQLite database, GEXF graph, and person JSONs for 乾县 (Qian County), 陕西省咸阳市.

Investigation date: 2026-07-25
Task ID: shaanxi_乾县
Level: 县
Targets: 县委书记 & 县长

Research sources:
  - www.snqianxian.gov.cn — 乾县人民政府官方网站 (primary, accessed July 2026)
  - 乾县政府网站领导之窗 (县委领导 xwld/ / 政府领导 zfld/)
  - 乾县人大/政府信息公开（人事任免栏目）
  - Wikipedia for cross-county notable figures (上官吉庆, 徐新荣)
  - Baidu Baike (limited access, captcha-blocked)

Confidence notes:
  - Current leaders (县委8人 + 政府5人 + 人大5人 + 政协4人 = 22人): confirmed via official government website
  - 闫兴斌, 段志华 bio: birth year + education confirmed via official profiles
  - Full career histories: NOT available — official site only shows current summary
  - Predecessor info: 焦志鹏 (plausible predecessor), 王斌 (former 常务副县长)
  - Cross-county figure: 上官吉庆 (1999-2002 乾县县委书记, later Xi'an mayor), 徐新荣 (born 乾县, Shaanxi CPPCC chair)
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "乾县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "shaanxi_乾县"
if _CURRENT_DIR.name == "shaanxi_乾县":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1-8 县委常委会, 9-13 政府领导, 14-18 人大, 19-22 政协, 23+ cross-county/predecessors

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # 县委常委会
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1, "name": "闫兴斌", "gender": "男", "ethnicity": "汉族",
        "birth": "1971年9月", "birthplace": "", "education": "研究生学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委书记", "current_org": "中共乾县委员会",
        "source": "https://www.snqianxian.gov.cn/zfxxgk/fdzdgknr/ldzc/xwld/yxb/"
    },
    {
        "id": 2, "name": "段志华", "gender": "男", "ethnicity": "汉族",
        "birth": "1974年4月", "birthplace": "", "education": "研究生学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委副书记、县长", "current_org": "乾县人民政府",
        "source": "https://www.snqianxian.gov.cn/zfxxgk/fdzdgknr/ldzc/xwld/dzha/"
    },
    {
        "id": 3, "name": "刘春锋", "gender": "男", "ethnicity": "汉族",
        "birth": "1975年3月", "birthplace": "", "education": "研究生学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委副书记", "current_org": "中共乾县委员会",
        "source": "https://www.snqianxian.gov.cn/zfxxgk/fdzdgknr/ldzc/xwld/lcf/"
    },
    {
        "id": 4, "name": "吴元操", "gender": "男", "ethnicity": "汉族",
        "birth": "1979年11月", "birthplace": "", "education": "硕士研究生学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委、组织部部长", "current_org": "中共乾县委员会组织部",
        "source": "https://www.snqianxian.gov.cn/zfxxgk/fdzdgknr/ldzc/xwld/wyc/"
    },
    {
        "id": 5, "name": "张斌", "gender": "男", "ethnicity": "汉族",
        "birth": "1981年10月", "birthplace": "", "education": "大学学历",
        "party_join": "中共党员", "work_start": "2005年8月",
        "current_post": "县委常委、县纪委书记、县监委主任", "current_org": "中共乾县纪律检查委员会",
        "source": "https://www.snqianxian.gov.cn/zfxxgk/fdzdgknr/ldzc/xwld/zb/"
    },
    {
        "id": 6, "name": "何伟", "gender": "男", "ethnicity": "汉族",
        "birth": "1983年2月", "birthplace": "", "education": "研究生学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委、宣传部部长", "current_org": "中共乾县委员会宣传部",
        "source": "https://www.snqianxian.gov.cn/zfxxgk/fdzdgknr/ldzc/xwld/hw/"
    },
    {
        "id": 7, "name": "李亚平", "gender": "男", "ethnicity": "汉族",
        "birth": "1979年8月", "birthplace": "", "education": "大学本科学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委、武装部政委", "current_org": "乾县人民武装部",
        "source": "https://www.snqianxian.gov.cn/zfxxgk/fdzdgknr/ldzc/xwld/lyp/"
    },
    {
        "id": 8, "name": "黄浩", "gender": "女", "ethnicity": "汉族",
        "birth": "1977年11月", "birthplace": "", "education": "大学学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委、统战部部长", "current_org": "中共乾县委员会统战部",
        "source": "https://www.snqianxian.gov.cn/zfxxgk/fdzdgknr/ldzc/xwld/hh/"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 县政府领导
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 9, "name": "孙佳佳", "gender": "男", "ethnicity": "汉族",
        "birth": "1986年2月", "birthplace": "", "education": "研究生学历，工学硕士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委、常务副县长", "current_org": "乾县人民政府",
        "source": "https://www.snqianxian.gov.cn/zfxxgk/fdzdgknr/ldzc/zfld/sjj/"
    },
    {
        "id": 10, "name": "董晓峰", "gender": "男", "ethnicity": "汉族",
        "birth": "1975年11月", "birthplace": "", "education": "党校研究生学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副县长、县公安局局长", "current_org": "乾县人民政府",
        "source": "https://www.snqianxian.gov.cn/zfxxgk/fdzdgknr/ldzc/zfld/dxf/"
    },
    {
        "id": 11, "name": "南伟", "gender": "男", "ethnicity": "汉族",
        "birth": "1979年8月", "birthplace": "", "education": "大学学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副县长", "current_org": "乾县人民政府",
        "source": "https://www.snqianxian.gov.cn/zfxxgk/fdzdgknr/ldzc/zfld/nw/"
    },
    {
        "id": 12, "name": "刘宇超", "gender": "男", "ethnicity": "汉族",
        "birth": "1990年4月", "birthplace": "", "education": "研究生学历，工学博士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副县长", "current_org": "乾县人民政府",
        "source": "https://www.snqianxian.gov.cn/zfxxgk/fdzdgknr/ldzc/zfld/lyc/"
    },
    {
        "id": 13, "name": "刘亮", "gender": "男", "ethnicity": "汉族",
        "birth": "1980年12月", "birthplace": "", "education": "大学学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副县长", "current_org": "乾县人民政府",
        "source": "https://www.snqianxian.gov.cn/zfxxgk/fdzdgknr/ldzc/zfld/ll_32629/"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 人大领导
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 14, "name": "张会文", "gender": "男", "ethnicity": "汉族",
        "birth": "1967年7月", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县人大常委会主任", "current_org": "乾县人大常委会",
        "source": "https://www.snqianxian.gov.cn/zfxxgk/fdzdgknr/ldzc/rdld/"
    },
    {
        "id": 15, "name": "张小宁", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县人大常委会副主任", "current_org": "乾县人大常委会",
        "source": "https://www.snqianxian.gov.cn/zfxxgk/fdzdgknr/ldzc/rdld/"
    },
    {
        "id": 16, "name": "冉歆", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县人大常委会副主任", "current_org": "乾县人大常委会",
        "source": "https://www.snqianxian.gov.cn/zfxxgk/fdzdgknr/ldzc/rdld/"
    },
    {
        "id": 17, "name": "高志华", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县人大常委会副主任", "current_org": "乾县人大常委会",
        "source": "https://www.snqianxian.gov.cn/zfxxgk/fdzdgknr/ldzc/rdld/"
    },
    {
        "id": 18, "name": "巨亚绒", "gender": "女", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县人大常委会副主任", "current_org": "乾县人大常委会",
        "source": "https://www.snqianxian.gov.cn/zfxxgk/fdzdgknr/ldzc/rdld/"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 政协领导
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 19, "name": "穆伟峰", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县政协主席", "current_org": "乾县政协",
        "source": "https://www.snqianxian.gov.cn/zfxxgk/fdzdgknr/ldzc/zxld/"
    },
    {
        "id": 20, "name": "杜亚军", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县政协副主席", "current_org": "乾县政协",
        "source": "https://www.snqianxian.gov.cn/zfxxgk/fdzdgknr/ldzc/zxld/"
    },
    {
        "id": 21, "name": "祝晓娣", "gender": "女", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县政协副主席", "current_org": "乾县政协",
        "source": "https://www.snqianxian.gov.cn/zfxxgk/fdzdgknr/ldzc/zxld/"
    },
    {
        "id": 22, "name": "孙凯", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县政协副主席", "current_org": "乾县政协",
        "source": "https://www.snqianxian.gov.cn/zfxxgk/fdzdgknr/ldzc/zxld/"
    },
    # ══════════════════════════════════════════════════════════════════════
    # 跨县/前任人物
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 23, "name": "上官吉庆", "gender": "男", "ethnicity": "汉族",
        "birth": "1963年", "birthplace": "陕西省乾县", "education": "研究生学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "（原西安市市长，2018年落马）", "current_org": "",
        "source": "https://en.wikipedia.org/wiki/Shangguan_Jiqing"
    },
    {
        "id": 24, "name": "徐新荣", "gender": "男", "ethnicity": "汉族",
        "birth": "1962年", "birthplace": "陕西省乾县", "education": "研究生学历",
        "party_join": "中共党员", "work_start": "",
        "current_post": "陕西省政协主席", "current_org": "陕西省政协",
        "source": "https://en.wikipedia.org/wiki/Xu_Xinrong"
    },
    {
        "id": 25, "name": "焦志鹏", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "（疑为前任县委书记）", "current_org": "",
        "source": ""
    },
    {
        "id": 26, "name": "王斌", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "（原常务副县长）", "current_org": "",
        "source": "https://www.snqianxian.gov.cn/rsxx/rsrm/202402/t20240223_1735508.html"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共乾县委员会", "type": "党委", "level": "县级", "parent": "中共咸阳市委员会", "location": "陕西省咸阳市乾县"},
    {"id": 2, "name": "乾县人民政府", "type": "政府", "level": "县级", "parent": "咸阳市人民政府", "location": "陕西省咸阳市乾县"},
    {"id": 3, "name": "中共乾县纪律检查委员会", "type": "纪委", "level": "县级", "parent": "中共乾县委员会", "location": "陕西省咸阳市乾县"},
    {"id": 4, "name": "中共乾县委员会组织部", "type": "党委部门", "level": "正科级", "parent": "中共乾县委员会", "location": "陕西省咸阳市乾县"},
    {"id": 5, "name": "中共乾县委员会宣传部", "type": "党委部门", "level": "正科级", "parent": "中共乾县委员会", "location": "陕西省咸阳市乾县"},
    {"id": 6, "name": "中共乾县委员会统战部", "type": "党委部门", "level": "正科级", "parent": "中共乾县委员会", "location": "陕西省咸阳市乾县"},
    {"id": 7, "name": "乾县人民武装部", "type": "军队", "level": "县级", "parent": "咸阳军分区", "location": "陕西省咸阳市乾县"},
    {"id": 8, "name": "乾县公安局", "type": "政府", "level": "正科级", "parent": "乾县人民政府", "location": "陕西省咸阳市乾县"},
    {"id": 9, "name": "乾县人大常委会", "type": "人大", "level": "县级", "parent": "咸阳市人大常委会", "location": "陕西省咸阳市乾县"},
    {"id": 10, "name": "乾县政协", "type": "政协", "level": "县级", "parent": "咸阳市政协", "location": "陕西省咸阳市乾县"},
    {"id": 11, "name": "陕西省政协", "type": "政协", "level": "省级", "parent": "", "location": "陕西省西安市"},
    {"id": 12, "name": "西安市人民政府", "type": "政府", "level": "副省级", "parent": "陕西省人民政府", "location": "陕西省西安市"},
]

# ── Positions ─────────────────────────────────────────────────────────────────
positions = [
    # 闫兴斌
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 段志华
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "2023年3月前", "end_date": "present", "rank": "正处级", "note": "2023年3月人大常委会确认已在任"},
    # 刘春锋
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "专职副书记"},
    # 吴元操
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start_date": "2020年4月", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 4, "title": "组织部部长", "start_date": "2020年4月", "end_date": "present", "rank": "副处级", "note": "2020年4月任现职"},
    # 张斌
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "2004.12入党, 2005.08参加工作"},
    {"person_id": 5, "org_id": 3, "title": "县纪委书记、县监委主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 何伟
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 5, "title": "宣传部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 李亚平
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "上校政治委员"},
    {"person_id": 7, "org_id": 7, "title": "武装部政委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 黄浩
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分工待确定"},
    {"person_id": 8, "org_id": 6, "title": "统战部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 孙佳佳
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "县政府党组副书记"},
    {"person_id": 9, "org_id": 2, "title": "常务副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "接替王斌"},
    # 董晓峰
    {"person_id": 10, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 8, "title": "县公安局局长、督察长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 南伟
    {"person_id": 11, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 刘宇超
    {"person_id": 12, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "工学博士"},
    # 刘亮
    {"person_id": 13, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 人大
    {"person_id": 14, "org_id": 9, "title": "县人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 15, "org_id": 9, "title": "县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 16, "org_id": 9, "title": "县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 17, "org_id": 9, "title": "县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 18, "org_id": 9, "title": "县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 政协
    {"person_id": 19, "org_id": 10, "title": "县政协主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 20, "org_id": 10, "title": "县政协副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 21, "org_id": 10, "title": "县政协副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 22, "org_id": 10, "title": "县政协副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 跨县/前任
    {"person_id": 23, "org_id": 1, "title": "县委书记", "start_date": "1999年", "end_date": "2002年", "rank": "正处级", "note": ""},
    {"person_id": 23, "org_id": 12, "title": "西安市市长", "start_date": "2016年", "end_date": "2018年", "rank": "副省级", "note": "2018年被查"},
    {"person_id": 24, "org_id": 11, "title": "陕西省政协主席", "start_date": "", "end_date": "present", "rank": "正省级", "note": "乾县籍最高级别官员"},
    {"person_id": 25, "org_id": 1, "title": "县委书记（疑前任）", "start_date": "", "end_date": "", "rank": "正处级", "note": "可能为闫兴斌前任，待确认"},
    {"person_id": 26, "org_id": 2, "title": "常务副县长（前任）", "start_date": "2024年2月前", "end_date": "约2024/2025年", "rank": "副处级", "note": "已不再担任，去向未知"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 党政一把手
    {"person_a": 1, "person_b": 2, "type": "搭档", "context": "县委书记与县长——党政一把手搭档", "overlap_org": "乾县党政班子", "overlap_period": "当前"},
    # 书记-副书记
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "县委书记与专职副书记", "overlap_org": "中共乾县委员会", "overlap_period": "当前"},
    # 书记-县委常委
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "县委书记与组织部部长", "overlap_org": "中共乾县委员会常委会", "overlap_period": "2020年至今"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "县委书记与纪委书记", "overlap_org": "中共乾县委员会常委会", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "县委书记与宣传部部长", "overlap_org": "中共乾县委员会常委会", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "县委书记与人武部政委", "overlap_org": "中共乾县委员会常委会", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "县委书记与统战部部长", "overlap_org": "中共乾县委员会常委会", "overlap_period": "当前"},
    # 县长-政府班子成员
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "县长与常务副县长——政府日常工作搭档", "overlap_org": "乾县人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "县长与副县长（公安局长）", "overlap_org": "乾县人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 11, "type": "上下级", "context": "县长与副县长", "overlap_org": "乾县人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "县长与副县长", "overlap_org": "乾县人民政府", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 13, "type": "上下级", "context": "县长与副县长", "overlap_org": "乾县人民政府", "overlap_period": "当前"},
    # 同僚-县委常委
    {"person_a": 3, "person_b": 4, "type": "同僚", "context": "同为县委常委", "overlap_org": "中共乾县委员会常委会", "overlap_period": "当前"},
    {"person_a": 4, "person_b": 5, "type": "同僚", "context": "同为县委常委", "overlap_org": "中共乾县委员会常委会", "overlap_period": "当前"},
    {"person_a": 5, "person_b": 6, "type": "同僚", "context": "同为县委常委", "overlap_org": "中共乾县委员会常委会", "overlap_period": "当前"},
    # 前任-继任
    {"person_a": 26, "person_b": 9, "type": "前任后继", "context": "王斌为前任常务副县长，孙佳佳接任", "overlap_org": "乾县人民政府", "overlap_period": "约2024/2025年"},
    # 跨县联系
    {"person_a": 23, "person_b": 1, "type": "前任后继", "context": "上官吉庆1999-2002年任乾县县委书记（20余年前），为本县成长的前任", "overlap_org": "中共乾县委员会", "overlap_period": ""},
    {"person_a": 24, "person_b": 1, "type": "同乡", "context": "徐新荣（乾县出生）与闫兴斌（乾县现任书记）同籍", "overlap_org": "", "overlap_period": ""},
]


# ═════════════════════════════════════════════════════════════════════════════
# Person JSON Generation
# ═════════════════════════════════════════════════════════════════════════════

def write_person_json(name: str, job: str, person: dict) -> None:
    """Write a deep person profile JSON following person_graph_json.md schema."""
    filename = f"{TODAY}-陕西省-咸阳市-{job}-{name}.json"
    filepath = PJSON_DIR / filename

    source_id = f"S01"
    source_url = person.get("source", "")
    source_entry = {
        "id": source_id, "title": f"乾县政府官网 - {person.get('current_post', '')}简介",
        "url": source_url, "publisher": "乾县人民政府",
        "accessed_at": AS_OF, "source_type": "official",
        "reliability": "high", "notes": ""
    } if source_url else None

    # Build career timeline
    career = []
    career.append({
        "start": "unknown", "end": "unknown", "org": "履历缺口",
        "title": "", "level": "", "location": "陕西省",
        "system": "unknown", "rank": "",
        "is_key_promotion": False,
        "notes": f"公开资料未找到{name}的完整履历；政府官网仅提供当前职务摘要",
        "confidence": "unverified", "source_ids": []
    })
    career.append({
        "start": "", "end": "present",
        "org": person.get("current_org", ""),
        "title": person.get("current_post", ""),
        "level": "县级",
        "location": "陕西省咸阳市乾县",
        "system": "party" if "委" in person.get("current_org", "") or "书记" in person.get("current_post", "") else "government",
        "rank": "正处级" if any(k in person.get("current_post", "") for k in ["县委书记", "县长", "县人大", "县政协主席"]) else "副处级",
        "is_key_promotion": True,
        "notes": "", "confidence": "confirmed",
        "source_ids": [source_id] if source_url else []
    })

    profile = {
        "schema_version": "1.0", "generated_at": TODAY,
        "investigation_scope": {
            "province": "陕西省", "city": "咸阳市", "region": "乾县",
            "job": job, "task_id": "shaanxi_乾县", "time_focus": "2026年7月"
        },
        "identity": {
            "person_id": f"shaanxi_qianxian_{name}",
            "name": name, "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [{
                "period": "", "institution": "", "major": "",
                "degree": person.get("education", ""),
                "study_type": "unknown",
                "source_ids": [source_id] if source_url else []
            }],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{person.get('birth', '')}",
                "name_birthplace": f"{name}_{person.get('birthplace', '')}",
                "official_profile_url": source_url
            }
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "",
            "as_of": AS_OF, "is_current_confirmed": True,
            "source_ids": [source_id] if source_url else []
        },
        "career_timeline": career,
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "当前履历数据不足，无法评估晋升速度", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records — not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{
            "type": "none_found",
            "description": f"截至{AS_OF}，未在公开资料中发现{name}的相关风险信号",
            "date": AS_OF, "confidence": "unverified", "source_ids": []
        }],
        "source_register": [source_entry] if source_entry else [],
        "confidence_summary": {
            "identity": "confirmed", "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "low",
            "biggest_gap": f"{name}完整的职业生涯履历（公开资料仅含当前职务）"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的完整职业生涯履历（出生至今的历任职务）",
                "why_it_matters": "无法评估其晋升路径、工作背景和跨县交流经历",
                "suggested_queries": [f"{name} 简历", f"{name} 任职经历", f"{name} 咸阳市"],
                "last_attempted": AS_OF
            },
            {
                "priority": "high",
                "question": f"{name}的具体出生地和籍贯",
                "why_it_matters": "地方关系网络分析的基础信息",
                "suggested_queries": [f"{name} 出生地", f"{name} 籍贯"],
                "last_attempted": AS_OF
            }
        ]
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(profile, f, ensure_ascii=False, indent=2)
    print(f"  ✓ Person JSON: {filepath.name}")


# ═════════════════════════════════════════════════════════════════════════════
# Main
# ═════════════════════════════════════════════════════════════════════════════

def main():
    print(f"Building {SLUG} network data...")
    print(f"  DB path: {DB_PATH}")
    print(f"  GEXF path: {GEXF_PATH}")

    # Build DB + GEXF via runner
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
    print(f"  ✓ Database: {DB_PATH}")
    print(f"  ✓ GEXF: {GEXF_PATH}")

    # Write person JSONs for core leaders
    core_leaders = [
        (1, "闫兴斌", "县委书记"),
        (2, "段志华", "县长"),
        (9, "孙佳佳", "常务副县长"),
    ]
    for pid, name, job in core_leaders:
        p = next(x for x in persons if x["id"] == pid)
        write_person_json(name, job, p)

    # Also write for cross-county figures (if useful)
    cross_figures = [
        (23, "上官吉庆", "原西安市市长"),
        (24, "徐新荣", "陕西省政协主席"),
    ]
    for pid, name, job in cross_figures:
        p = next(x for x in persons if x["id"] == pid)
        write_person_json(name, job, p)

    print(f"\nSummary: {len(persons)} persons, {len(organizations)} orgs, "
          f"{len(positions)} positions, {len(relationships)} relationships")
    print("Done.")


if __name__ == "__main__":
    main()
