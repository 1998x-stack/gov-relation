#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 裕华区 leadership network.

Data source: www.yuhuaqu.gov.cn (official government website)
Information currency: 2026-07-23 (current as of July 2026)

Sources:
- 裕政〔2026〕3号 关于区政府领导工作分工调整的通知 (2026-02-09)
- 2025年政府工作报告 (2026-02-11 in 区六届人大七次会议)
- www.yuhuaqu.gov.cn 政府信息公开-领导简介
"""

import sqlite3  # noqa: used by runner
from gov_relation.runner import run_build
from gov_relation.paths import DATA_DIR
from pathlib import Path
from datetime import datetime

SLUG = "裕华区"

# Staging paths
TMP_DIR = DATA_DIR / "tmp" / "hebei_裕华区"
DB_PATH = TMP_DIR / "裕华区_network.db"
GEXF_PATH = TMP_DIR / "裕华区_network.gexf"

# ═══════════════════════════════════════════════════════════════════════════════
# Persons
# ═══════════════════════════════════════════════════════════════════════════════
# NOTE: 区委书记 name could not be confirmed via web-accessible government pages
# (site leadership section for party committee not reachable). Only 白玉春 (区长)
# is confirmed via 裕政〔2026〕3号. 区委书记 entry is a placeholder pending
# further research.
persons = [
    # ── District Party Secretary (区委书记) ──
    # ⚠️ 区委书记 - name unconfirmed from web-accessible government portal.
    # Typical pattern: 裕华区区委书记 (separate from 区长 白玉春).
    # To be updated when official leadership page is reachable.
    {
        "id": 1,
        "name": "（待确认-区委书记）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "裕华区委书记（待确认）",
        "current_org": "中共石家庄市裕华区委员会",
        "source": "http://www.yuhuaqu.gov.cn/",
    },
    # ── District Mayor (区长) ──
    {
        "id": 2,
        "name": "白玉春",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "裕华区委副书记、区长",
        "current_org": "裕华区人民政府",
        "source": "http://www.yuhuaqu.gov.cn/columns/5be93982-3c33-4df5-9156-77e3b51de97f/index.html",
    },
    # ── Executive Deputy Mayor (常务副区长) ──
    {
        "id": 3,
        "name": "洪威",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "裕华区委常委、副区长（分工政府常务工作）",
        "current_org": "裕华区人民政府",
        "source": "http://www.yuhuaqu.gov.cn/columns/5be93982-3c33-4df5-9156-77e3b51de97f/index.html",
    },
    # ── Deputy Mayor & Public Security Bureau Chief ──
    {
        "id": 4,
        "name": "葛江涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "裕华区副区长、公安分局局长",
        "current_org": "石家庄市公安局裕华分局",
        "source": "http://www.yuhuaqu.gov.cn/columns/5be93982-3c33-4df5-9156-77e3b51de97f/index.html",
    },
    # ── Deputy Mayor (潘峰) ──
    {
        "id": 5,
        "name": "潘峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "裕华区副区长",
        "current_org": "裕华区人民政府",
        "source": "http://www.yuhuaqu.gov.cn/columns/5be93982-3c33-4df5-9156-77e3b51de97f/index.html",
    },
    # ── Deputy Mayor (于彦军) ──
    {
        "id": 6,
        "name": "于彦军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "裕华区副区长",
        "current_org": "裕华区人民政府",
        "source": "http://www.yuhuaqu.gov.cn/columns/5be93982-3c33-4df5-9156-77e3b51de97f/index.html",
    },
    # ── Deputy Mayor (崔秋生) ──
    {
        "id": 7,
        "name": "崔秋生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "裕华区副区长",
        "current_org": "裕华区人民政府",
        "source": "http://www.yuhuaqu.gov.cn/columns/5be93982-3c33-4df5-9156-77e3b51de97f/index.html",
    },
    # ── Party Group Member (邱水, 挂职) ──
    {
        "id": 8,
        "name": "邱水",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "裕华区政府党组成员、区政府办副主任（挂职）",
        "current_org": "裕华区人民政府",
        "source": "http://www.yuhuaqu.gov.cn/columns/5be93982-3c33-4df5-9156-77e3b51de97f/index.html",
    },
]

# ═══════════════════════════════════════════════════════════════════════════════
# Organizations
# ═══════════════════════════════════════════════════════════════════════════════
organizations = [
    {
        "id": 1,
        "name": "中共石家庄市裕华区委员会",
        "type": "党委",
        "level": "市辖区",
        "parent": "中共石家庄市委员会",
        "location": "河北省石家庄市裕华区",
    },
    {
        "id": 2,
        "name": "裕华区人民政府",
        "type": "政府",
        "level": "市辖区",
        "parent": "石家庄市人民政府",
        "location": "河北省石家庄市裕华区",
    },
    {
        "id": 3,
        "name": "石家庄市公安局裕华分局",
        "type": "政府",
        "level": "市辖区",
        "parent": "裕华区人民政府",
        "location": "河北省石家庄市裕华区",
    },
    {
        "id": 4,
        "name": "裕华区审计局",
        "type": "政府",
        "level": "市辖区",
        "parent": "裕华区人民政府",
        "location": "河北省石家庄市裕华区",
    },
    {
        "id": 5,
        "name": "裕华区财政局",
        "type": "政府",
        "level": "市辖区",
        "parent": "裕华区人民政府",
        "location": "河北省石家庄市裕华区",
    },
    {
        "id": 6,
        "name": "裕华区发展和改革局",
        "type": "政府",
        "level": "市辖区",
        "parent": "裕华区人民政府",
        "location": "河北省石家庄市裕华区",
    },
    {
        "id": 7,
        "name": "裕华区人力资源和社会保障局",
        "type": "政府",
        "level": "市辖区",
        "parent": "裕华区人民政府",
        "location": "河北省石家庄市裕华区",
    },
    {
        "id": 8,
        "name": "裕华区住房和城区建设局",
        "type": "政府",
        "level": "市辖区",
        "parent": "裕华区人民政府",
        "location": "河北省石家庄市裕华区",
    },
    {
        "id": 9,
        "name": "裕华区数据和政务服务局",
        "type": "政府",
        "level": "市辖区",
        "parent": "裕华区人民政府",
        "location": "河北省石家庄市裕华区",
    },
    {
        "id": 10,
        "name": "裕华区统计局",
        "type": "政府",
        "level": "市辖区",
        "parent": "裕华区人民政府",
        "location": "河北省石家庄市裕华区",
    },
    {
        "id": 11,
        "name": "裕华区应急管理局",
        "type": "政府",
        "level": "市辖区",
        "parent": "裕华区人民政府",
        "location": "河北省石家庄市裕华区",
    },
    {
        "id": 12,
        "name": "裕华区教育局",
        "type": "政府",
        "level": "市辖区",
        "parent": "裕华区人民政府",
        "location": "河北省石家庄市裕华区",
    },
    {
        "id": 13,
        "name": "裕华区民政局",
        "type": "政府",
        "level": "市辖区",
        "parent": "裕华区人民政府",
        "location": "河北省石家庄市裕华区",
    },
    {
        "id": 14,
        "name": "裕华区商务局",
        "type": "政府",
        "level": "市辖区",
        "parent": "裕华区人民政府",
        "location": "河北省石家庄市裕华区",
    },
    {
        "id": 15,
        "name": "裕华区城管局",
        "type": "政府",
        "level": "市辖区",
        "parent": "裕华区人民政府",
        "location": "河北省石家庄市裕华区",
    },
    {
        "id": 16,
        "name": "裕华区市场监督管理局",
        "type": "政府",
        "level": "市辖区",
        "parent": "裕华区人民政府",
        "location": "河北省石家庄市裕华区",
    },
    {
        "id": 17,
        "name": "裕华区农业农村局",
        "type": "政府",
        "level": "市辖区",
        "parent": "裕华区人民政府",
        "location": "河北省石家庄市裕华区",
    },
    {
        "id": 18,
        "name": "裕华区卫健局",
        "type": "政府",
        "level": "市辖区",
        "parent": "裕华区人民政府",
        "location": "河北省石家庄市裕华区",
    },
    {
        "id": 19,
        "name": "裕华区司法局",
        "type": "政府",
        "level": "市辖区",
        "parent": "裕华区人民政府",
        "location": "河北省石家庄市裕华区",
    },
    {
        "id": 20,
        "name": "裕华区科技局",
        "type": "政府",
        "level": "市辖区",
        "parent": "裕华区人民政府",
        "location": "河北省石家庄市裕华区",
    },
    {
        "id": 21,
        "name": "裕华区退役军人事务局",
        "type": "政府",
        "level": "市辖区",
        "parent": "裕华区人民政府",
        "location": "河北省石家庄市裕华区",
    },
    {
        "id": 22,
        "name": "裕华区文化广电体育和旅游局",
        "type": "政府",
        "level": "市辖区",
        "parent": "裕华区人民政府",
        "location": "河北省石家庄市裕华区",
    },
    {
        "id": 23,
        "name": "裕华区医疗保障局",
        "type": "政府",
        "level": "市辖区",
        "parent": "裕华区人民政府",
        "location": "河北省石家庄市裕华区",
    },
]

# ═══════════════════════════════════════════════════════════════════════════════
# Positions (current roles, as of 2026-07)
# ═══════════════════════════════════════════════════════════════════════════════
positions = [
    # 区委书记
    {"person_id": 1, "org_id": 1, "title": "裕华区委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "待确认姓名（区委书记≠区长白玉春）"},
    # 白玉春 - 区长
    {"person_id": 2, "org_id": 2, "title": "裕华区委副书记、区长", "start_date": "", "end_date": "", "rank": "正处级", "note": "主持区政府全面工作，分管审计局"},
    {"person_id": 2, "org_id": 1, "title": "裕华区委副书记", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    # 洪威 - 常务副区长
    {"person_id": 3, "org_id": 2, "title": "裕华区委常委、副区长（常务）", "start_date": "", "end_date": "", "rank": "副处级", "note": "负责财政、发改、人社、住建、应急、统计、数政、自然资源等"},
    {"person_id": 3, "org_id": 1, "title": "裕华区委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 葛江涛 - 副区长/公安分局局长
    {"person_id": 4, "org_id": 2, "title": "裕华区副区长、公安分局局长", "start_date": "", "end_date": "", "rank": "副处级", "note": "负责公安、退役军人、司法、交通等"},
    {"person_id": 4, "org_id": 3, "title": "裕华公安分局局长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 潘峰 - 副区长
    {"person_id": 5, "org_id": 2, "title": "裕华区副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "负责招商、商贸、文体、科技、城管、园林等"},
    # 于彦军 - 副区长
    {"person_id": 6, "org_id": 2, "title": "裕华区副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "负责教育、民政、农业农村、卫健、医保等"},
    # 崔秋生 - 副区长
    {"person_id": 7, "org_id": 2, "title": "裕华区副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "负责工业、食品安全、市场监管等"},
    # 邱水 - 挂职
    {"person_id": 8, "org_id": 2, "title": "裕华区政府党组成员、区政府办副主任（挂职）", "start_date": "", "end_date": "", "rank": "", "note": "协助洪威抓好地方金融管理"},
]

# ═══════════════════════════════════════════════════════════════════════════════
# Relationships
# ═══════════════════════════════════════════════════════════════════════════════
# Core: 区委书记—区长（党政一把手搭档）
# 区长—副区长（上下级）
# Note: 区委书记姓名未确认，相关的党政关系暂不纳入可靠graph edges
relationships = [
    # 区长—常务副区长
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate",
     "context": "区长—常务副区长", "overlap_org": "裕华区人民政府", "overlap_period": "2026-"},
    # 区长—副区长葛江涛
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "区长—副区长", "overlap_org": "裕华区人民政府", "overlap_period": "2026-"},
    # 区长—副区长潘峰
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "区长—副区长", "overlap_org": "裕华区人民政府", "overlap_period": "2026-"},
    # 区长—副区长于彦军
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate",
     "context": "区长—副区长", "overlap_org": "裕华区人民政府", "overlap_period": "2026-"},
    # 区长—副区长崔秋生
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate",
     "context": "区长—副区长", "overlap_org": "裕华区人民政府", "overlap_period": "2026-"},
    # 常务副区长—挂职党组成员
    {"person_a": 3, "person_b": 8, "type": "superior_subordinate",
     "context": "常务副区长—挂职副主任（协助金融工作）", "overlap_org": "裕华区人民政府", "overlap_period": "2026-"},
]

# ═══════════════════════════════════════════════════════════════════════════════
# Run Build
# ═══════════════════════════════════════════════════════════════════════════════
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
    print("Done: 裕华区 network built.")
