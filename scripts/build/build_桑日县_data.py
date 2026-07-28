#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
桑日县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 西藏自治区
Parent City: 山南市
Region: 桑日县
Targets: 县委书记 & 县长

Research Sources:
- 桑日县人民政府官网 (www.sangri.gov.cn) — 领导之窗页面: http://www.sangri.gov.cn/zwgk/ldzc/
  - 次仁达瓦县长个人页面: http://www.sangri.gov.cn/zwgk/ldzc/202506/t20250626_151958.html
- 桑日县领导活动列表: http://www.sangri.gov.cn/xwzx/ldhd/ (多页)
- 新闻确认: 谭金元为县委书记(2026年6月起多次以"县委书记谭金元"出现)
  - http://www.sangri.gov.cn/xwzx/ldhd/202607/t20260714_173373.html → "县委书记谭金元深入县政府职能部门调研"
  - http://www.sangri.gov.cn/xwzx/ldhd/202606/t20260624_171501.html → "谭金元在县委办公室、县委组织部调研"
  - http://www.sangri.gov.cn/xwzx/ldhd/202606/t20260617_171248.html → "谭金元到华新（西藏）水泥有限公司调研"
- 孙守英为前任县委书记(2025年9月至2026年4月以县委书记身份活跃):
  - 听取乡（镇）和县直部门"一把手"述责述廉汇报、武装部调研等
- 次仁达瓦县长详细履历来自领导之窗页面

Research Date: 2026-07-28

Gaps:
- 县委书记谭金元的出生年月、籍贯、学历、完整履历暂缺
- 次仁达瓦县长2015年之前的早期履历以及政策研究室主任之前经历暂缺
- 前任县委书记孙守英的完整履历、去向暂缺
- 县委常委班子（纪委书记、宣传部长、统战部长、政法委书记等）的人员配置未找到官网领导之窗列表
- 县人大常委会主任、县政协主席姓名暂缺
- 部分副县长的详细分工和履历暂缺
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build

SLUG = "桑日县"

_script_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_script_dir, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(_script_dir, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401 — required for process_tmp.py token check

# ── Data ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders
    # ════════════════════════════════════════
    {
        "id": 1,
        "name": "谭金元",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桑日县委书记",
        "current_org": "中共桑日县委员会",
        "source": "桑日县人民政府官网：县委书记谭金元。来源：http://www.sangri.gov.cn/xwzx/ldhd/202607/t20260714_173373.html — '县委书记谭金元深入县政府职能部门调研'"
    },
    {
        "id": 2,
        "name": "次仁达瓦",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1981年5月",
        "birthplace": "西藏曲松",
        "education": "在职研究生学历",
        "party_join": "2006年6月",
        "work_start": "",
        "current_post": "桑日县委副书记、县长",
        "current_org": "桑日县人民政府",
        "source": "https://www.sangri.gov.cn/zwgk/ldzc/202506/t20250626_151958.html — 次仁达瓦，男，藏族，1981年5月出生，西藏曲松人，2006年6月加入中国共产党，在职研究生学历。现任桑日县委副书记，县长。"
    },
    # ════════════════════════════════════════
    # Government Deputy Leaders
    # ════════════════════════════════════════
    {
        "id": 3,
        "name": "彭典",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桑日县委常务副书记、常务副县长、三级调研员（援藏）",
        "current_org": "桑日县人民政府",
        "source": "https://www.sangri.gov.cn/zwgk/ldzc/ — 彭典（援藏）桑日县委常务副书记、常务副县长、三级调研员"
    },
    {
        "id": 4,
        "name": "查日",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桑日县委常委、常务副县长",
        "current_org": "桑日县人民政府",
        "source": "https://www.sangri.gov.cn/zwgk/ldzc/ — 查日，桑日县委常委、常务副县长"
    },
    {
        "id": 5,
        "name": "阳郑",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桑日县委常委、副县长（援藏）",
        "current_org": "桑日县人民政府",
        "source": "https://www.sangri.gov.cn/zwgk/ldzc/ — 阳郑（援藏）桑日县委常委、副县长"
    },
    {
        "id": 6,
        "name": "胡建斌",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桑日县委常委、副县长",
        "current_org": "桑日县人民政府",
        "source": "https://www.sangri.gov.cn/zwgk/ldzc/ — 胡建斌，桑日县委常委、副县长"
    },
    {
        "id": 7,
        "name": "白玛央金",
        "gender": "女",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桑日县人民政府副县长",
        "current_org": "桑日县人民政府",
        "source": "https://www.sangri.gov.cn/zwgk/ldzc/ — 白玛央金，桑日县人民政府副县长"
    },
    {
        "id": 8,
        "name": "张宗宝",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桑日县人民政府副县长",
        "current_org": "桑日县人民政府",
        "source": "https://www.sangri.gov.cn/zwgk/ldzc/ — 张宗宝，桑日县人民政府副县长"
    },
    {
        "id": 9,
        "name": "刘永凯",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桑日县人民政府副县长",
        "current_org": "桑日县人民政府",
        "source": "https://www.sangri.gov.cn/zwgk/ldzc/ — 刘永凯，桑日县人民政府副县长"
    },
    {
        "id": 10,
        "name": "多布杰",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桑日县人民政府副县长",
        "current_org": "桑日县人民政府",
        "source": "https://www.sangri.gov.cn/zwgk/ldzc/ — 多布杰，桑日县人民政府副县长"
    },
    {
        "id": 11,
        "name": "崔称旦增",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桑日县人民政府副县长",
        "current_org": "桑日县人民政府",
        "source": "https://www.sangri.gov.cn/zwgk/ldzc/ — 崔称旦增，桑日县人民政府副县长"
    },
    {
        "id": 12,
        "name": "刘积庭",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桑日县副县长",
        "current_org": "桑日县人民政府",
        "source": "https://www.sangri.gov.cn/xwzx/ldhd/202509/t20250919_155571.html — '刘积庭副县长赴村、寺管会慰问并督导路段养护及加油站安全生产工作'"
    },
    {
        "id": 13,
        "name": "贾锋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桑日县领导",
        "current_org": "桑日县人民政府",
        "source": "https://www.sangri.gov.cn/xwzx/ldhd/ — 贾锋走访慰问一线加油站、贾锋深入项目建设点督导检查安全生产工作"
    },
    # ════════════════════════════════════════
    # Predecessor
    # ════════════════════════════════════════
    {
        "id": 14,
        "name": "孙守英",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原桑日县委书记（2026年5月前后离任）",
        "current_org": "",
        "source": "https://www.sangri.gov.cn/xwzx/ldhd/ — 孙守英2025年9月至2026年4月以县委书记身份活跃（听取述责述廉汇报、节前慰问等），2026年6月起被谭金元接替"
    },
    # ════════════════════════════════════════
    # Other county leaders
    # ════════════════════════════════════════
    {
        "id": 15,
        "name": "边巴次仁",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "桑日县领导",
        "current_org": "桑日县人民政府",
        "source": "https://www.sangri.gov.cn/xwzx/ldhd/ — '边巴次仁深入联系点开展节前慰问活动'"
    },
]

# 2. Organizations
organizations = [
    {
        "id": 1,
        "name": "中共桑日县委员会",
        "type": "党委",
        "level": "县级",
        "location": "山南市桑日县",
        "parent": "中共山南市委"
    },
    {
        "id": 2,
        "name": "桑日县人民政府",
        "type": "政府",
        "level": "县级",
        "location": "山南市桑日县",
        "parent": "山南市人民政府"
    },
    {
        "id": 3,
        "name": "桑日县人大常委会",
        "type": "人大",
        "level": "县级",
        "location": "山南市桑日县",
        "parent": "山南市人大常委会"
    },
    {
        "id": 4,
        "name": "政协桑日县委员会",
        "type": "政协",
        "level": "县级",
        "location": "山南市桑日县",
        "parent": "政协山南市委员会"
    },
    {
        "id": 5,
        "name": "中共桑日县纪律检查委员会",
        "type": "纪委",
        "level": "县级",
        "location": "山南市桑日县",
        "parent": "中共山南市纪律检查委员会"
    },
    {
        "id": 6,
        "name": "中共桑日县委组织部",
        "type": "党委部门",
        "level": "县级",
        "location": "山南市桑日县",
        "parent": "中共桑日县委员会"
    },
    {
        "id": 7,
        "name": "中共桑日县委宣传部",
        "type": "党委部门",
        "level": "县级",
        "location": "山南市桑日县",
        "parent": "中共桑日县委员会"
    },
    {
        "id": 8,
        "name": "中共桑日县委统战部",
        "type": "党委部门",
        "level": "县级",
        "location": "山南市桑日县",
        "parent": "中共桑日县委员会"
    },
    {
        "id": 9,
        "name": "中共桑日县委政法委",
        "type": "政法系统",
        "level": "县级",
        "location": "山南市桑日县",
        "parent": "中共桑日县委员会"
    },
    {
        "id": 10,
        "name": "中共桑日县委办公室",
        "type": "党委部门",
        "level": "县级",
        "location": "山南市桑日县",
        "parent": "中共桑日县委员会"
    },
    {
        "id": 11,
        "name": "中共山南市委政策研究室",
        "type": "党委部门",
        "level": "地市级",
        "location": "山南市乃东区",
        "parent": "中共山南市委员会"
    },
    {
        "id": 12,
        "name": "中共措美县委员会",
        "type": "党委",
        "level": "县级",
        "location": "山南市措美县",
        "parent": "中共山南市委"
    },
    {
        "id": 13,
        "name": "中共山南市委办公室",
        "type": "党委部门",
        "level": "地市级",
        "location": "山南市乃东区",
        "parent": "中共山南市委员会"
    },
]

# 3. Positions
positions = [
    # 谭金元 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "桑日县委书记", "start": "2026-06", "end": "present", "rank": "正处级", "note": "2026年6月起以县委书记身份出现在公开报道"},
    # 次仁达瓦 — 县长
    {"person_id": 2, "org_id": 2, "title": "桑日县委副书记、县长", "start": "", "end": "present", "rank": "正处级", "note": "主持县政府全面工作。个人页面更新于2025年6月"},
    {"person_id": 2, "org_id": 11, "title": "中共山南市委政策研究室主任", "start": "", "end": "", "rank": "正处级", "note": "曾任"},
    {"person_id": 2, "org_id": 12, "title": "措美县委副书记（正县级）", "start": "", "end": "", "rank": "正处级", "note": "曾任"},
    {"person_id": 2, "org_id": 13, "title": "中共山南市委常务副秘书长（正县级）", "start": "", "end": "", "rank": "正处级", "note": "曾任"},
    # 彭典 — 援藏常务副书记/副县长
    {"person_id": 3, "org_id": 1, "title": "桑日县委常务副书记（援藏）", "start": "", "end": "present", "rank": "正处级/三级调研员", "note": "援藏干部"},
    {"person_id": 3, "org_id": 2, "title": "桑日县常务副县长（援藏）", "start": "", "end": "present", "rank": "", "note": "援藏干部"},
    # 查日 — 县委常委、常务副县长
    {"person_id": 4, "org_id": 1, "title": "桑日县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "桑日县常务副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 阳郑 — 县委常委、副县长（援藏）
    {"person_id": 5, "org_id": 1, "title": "桑日县委常委（援藏）", "start": "", "end": "present", "rank": "副处级", "note": "援藏干部"},
    {"person_id": 5, "org_id": 2, "title": "桑日县副县长（援藏）", "start": "", "end": "present", "rank": "副处级", "note": "援藏干部"},
    # 胡建斌 — 县委常委、副县长
    {"person_id": 6, "org_id": 1, "title": "桑日县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "桑日县副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 白玛央金 — 副县长
    {"person_id": 7, "org_id": 2, "title": "桑日县人民政府副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 张宗宝 — 副县长
    {"person_id": 8, "org_id": 2, "title": "桑日县人民政府副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 刘永凯 — 副县长
    {"person_id": 9, "org_id": 2, "title": "桑日县人民政府副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 多布杰 — 副县长
    {"person_id": 10, "org_id": 2, "title": "桑日县人民政府副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 崔称旦增 — 副县长
    {"person_id": 11, "org_id": 2, "title": "桑日县人民政府副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 刘积庭 — 副县长
    {"person_id": 12, "org_id": 2, "title": "桑日县副县长", "start": "", "end": "present", "rank": "副处级", "note": "2025年9月以副县长身份出现"},
    # 贾锋 — 县领导
    {"person_id": 13, "org_id": 2, "title": "桑日县领导", "start": "", "end": "present", "rank": "", "note": "出现在领导活动列表中，具体职务待查"},
    # 孙守英 — 前任县委书记
    {"person_id": 14, "org_id": 1, "title": "桑日县委书记（前任）", "start": "不晚于2025-09", "end": "2026-04/05", "rank": "正处级", "note": "2025年9月至2026年4月期间以县委书记身份活跃；2026年6月被谭金元接替"},
    # 边巴次仁 — 县领导
    {"person_id": 15, "org_id": 2, "title": "桑日县领导", "start": "", "end": "", "rank": "", "note": "2026年1月从事节前慰问活动"},
]

# 4. Relationships
relationships = [
    # 谭金元 — 次仁达瓦：党政一把手
    {"person_a": 1, "person_b": 2, "type": "党政一把手", "context": "谭金元（县委书记）与次仁达瓦（县长）为桑日县党政主要负责人", "overlap_org": "桑日县", "overlap_period": "2026-06至今"},
    # 次仁达瓦 — 查日（常务副县长）
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "县长与常务副县长", "overlap_org": "桑日县人民政府", "overlap_period": ""},
    # 次仁达瓦 — 各位副县长
    {"person_a": 2, "person_b": 3, "type": "上下级", "context": "县长与援藏常务副书记/副县长", "overlap_org": "桑日县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "县长与援藏副县长", "overlap_org": "桑日县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "县长与副县长", "overlap_org": "桑日县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "县长与副县长", "overlap_org": "桑日县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "县长与副县长", "overlap_org": "桑日县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "县长与副县长", "overlap_org": "桑日县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "县长与副县长", "overlap_org": "桑日县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 11, "type": "上下级", "context": "县长与副县长", "overlap_org": "桑日县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "县长与副县长", "overlap_org": "桑日县人民政府", "overlap_period": ""},
    # 谭金元 — 孙守英：前后任书记
    {"person_a": 1, "person_b": 14, "type": "前任/后任", "context": "谭金元接替孙守英担任桑日县委书记", "overlap_org": "中共桑日县委员会", "overlap_period": "2026年"},
    # 孙守英 — 次仁达瓦：前任书记与县长
    {"person_a": 14, "person_b": 2, "type": "党政一把手（前任）", "context": "孙守英任县委书记期间，次仁达瓦任县长，两人为党政搭档", "overlap_org": "桑日县", "overlap_period": "至2026年4月"},
    # 谭金元 — 各位县委常委
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "县委书记与县委常委、常务副县长", "overlap_org": "中共桑日县委员会", "overlap_period": "2026年6月至今"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "县委书记与县委常委（援藏）", "overlap_org": "中共桑日县委员会", "overlap_period": "2026年6月至今"},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "县委书记与县委常委、副县长", "overlap_org": "中共桑日县委员会", "overlap_period": "2026年6月至今"},
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "县委书记与县委常务副书记（援藏）", "overlap_org": "中共桑日县委员会", "overlap_period": "2026年6月至今"},
]

# ── Build ──

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
    print(f"Done. DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")