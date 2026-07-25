#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 淄川区, 淄博市, 山东省.

Investigation date: 2026-07-25
Task ID: shandong_淄川区
Level: 市辖区
Targets: 区委书记 & 区长

Key findings:
- 区委书记 程勤 — 现任 (as of July 2026, confirmed from 区委理论学习中心组 news)
- 区长 冯炳涛 — 区委副书记、区长 (as of July 2026)
- 区委副书记 刘鸿智
- 区人大常委会主任 周恒学
- 区政协主席 李庭
- 常务副区长 张刚 (区委常委、副区长、开发区党工委书记)
- 区委常委、副区长 冯明
- 区委常委、副区长 王倩雯
- 区委常委、组织部部长 刘胜虎
- 区委常委、办公室主任 张山山
- 区委常委、宣传部部长、统战部部长 穆立华
- 区委常委、政法委书记 周克聪

Research sources:
- 淄川区人民政府网站 (www.zichuan.gov.cn) — multiple news articles confirming current leadership (2026年7月)
- 淄川区融媒体中心 — official news reports

Confidence notes:
- 程勤当前职务已确认 (区委书记, as of 2026年7月)
- 冯炳涛当前职务已确认 (区委副书记、区长, as of 2026年7月)
- 大部分区委常委和区级领导已通过新闻参会名单确认
- 早期履历信息暂缺，待查
- 淄川区纪委书记暂未从公开新闻中确认
"""

import json
import os
import sqlite3  # noqa: F401
import sys
from datetime import datetime
from pathlib import Path

BASE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from gov_relation.runner import run_build  # noqa: E402

SLUG = "淄川区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

STAGING_DIR = Path(BASE)
DB_PATH = str(STAGING_DIR / f"{SLUG}_network.db")
GEXF_PATH = str(STAGING_DIR / f"{SLUG}_network.gexf")

# ═══════════════════════════════════════════════════════════════════════════════
# Data
# ═══════════════════════════════════════════════════════════════════════════════

persons_data = [
    # ══════════════════════════════════════════════════════════════════════════
    # Party Committee (区委) Leadership — Core
    # ══════════════════════════════════════════════════════════════════════════

    # 程勤 — 淄川区委书记 (现任)
    {
        "id": 1,
        "name": "程勤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "淄川区委书记",
        "current_org": "中共淄川区委员会",
        "source": "淄川区人民政府网站 (zichuan.gov.cn), confirmed from 区委理论学习中心组 and multiple news (2026年7月)"
    },
    # 冯炳涛 — 淄川区委副书记、区长 (现任)
    {
        "id": 2,
        "name": "冯炳涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "淄川区委副书记、区长",
        "current_org": "淄川区人民政府",
        "source": "淄川区人民政府网站 (zichuan.gov.cn), 百名专家淄博行等新闻确认 (2026年7月)"
    },

    # ══════════════════════════════════════════════════════════════════════════
    # 区人大 / 区政协 / 区委副职
    # ══════════════════════════════════════════════════════════════════════════

    # 周恒学 — 区人大常委会主任
    {
        "id": 3,
        "name": "周恒学",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "淄川区人大常委会主任",
        "current_org": "淄川区人民代表大会常务委员会",
        "source": "淄川区人民政府网站, 人大会议和慰问活动报道 (2026年7月)"
    },
    # 李庭 — 区政协主席
    {
        "id": 4,
        "name": "李庭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "淄川区政协主席",
        "current_org": "中国人民政治协商会议淄川区委员会",
        "source": "淄川区人民政府网站, 政协活动报道 (2026年6月-7月)"
    },
    # 刘鸿智 — 区委副书记
    {
        "id": 5,
        "name": "刘鸿智",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "淄川区委副书记",
        "current_org": "中共淄川区委员会",
        "source": "淄川区人民政府网站, 理论学习中心组和慰问活动报道 (2026年7月)"
    },

    # ══════════════════════════════════════════════════════════════════════════
    # 区委常委 (区委领导班子)
    # ══════════════════════════════════════════════════════════════════════════

    # 刘胜虎 — 区委常委、组织部部长
    {
        "id": 6,
        "name": "刘胜虎",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "淄川区委常委、组织部部长",
        "current_org": "中共淄川区委员会",
        "source": "淄川区人民政府网站, 人才座谈会和干部进修班报道 (2026年7月)"
    },
    # 张山山 — 区委常委、区委办公室主任
    {
        "id": 7,
        "name": "张山山",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "淄川区委常委、区委办公室主任",
        "current_org": "中共淄川区委员会",
        "source": "淄川区人民政府网站, 人才座谈会和调研活动报道 (2026年7月)"
    },
    # 张刚 — 区委常委、副区长、开发区党工委书记
    {
        "id": 8,
        "name": "张刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "淄川区委常委、副区长、淄川经济开发区党工委书记",
        "current_org": "淄川区人民政府",
        "source": "淄川区人民政府网站, 巡察和项目推进会报道 (2026年7月)"
    },
    # 冯明 — 区委常委、副区长
    {
        "id": 9,
        "name": "冯明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "淄川区委常委、副区长",
        "current_org": "淄川区人民政府",
        "source": "淄川区人民政府网站, 干部讲堂和项目推进会报道 (2026年7月)"
    },
    # 王倩雯 — 区委常委、副区长
    {
        "id": 10,
        "name": "王倩雯",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "淄川区委常委、副区长",
        "current_org": "淄川区人民政府",
        "source": "淄川区人民政府网站, 生物质基地启用和电力设施报道 (2026年6月-7月)"
    },
    # 周克聪 — 区委常委、政法委书记
    {
        "id": 11,
        "name": "周克聪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "淄川区委常委、政法委书记",
        "current_org": "中共淄川区委员会",
        "source": "淄川区人民政府网站, 煤矿检测创新交流会致辞 (2026年7月)"
    },
    # 穆立华 — 区委常委、宣传部部长、统战部部长
    {
        "id": 12,
        "name": "穆立华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "淄川区委常委、宣传部部长、统战部部长",
        "current_org": "中共淄川区委员会",
        "source": "淄川区人民政府网站, 慰问困难党员报道 (2026年7月)"
    },

    # ══════════════════════════════════════════════════════════════════════════
    # 副区长
    # ══════════════════════════════════════════════════════════════════════════

    # 赵聪 — 副区长
    {
        "id": 13,
        "name": "赵聪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "淄川区副区长",
        "current_org": "淄川区人民政府",
        "source": "淄川区人民政府网站, 矿山安全和项目推进报道 (2026年7月)"
    },
    # 王林 — 副区长
    {
        "id": 14,
        "name": "王林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "淄川区副区长",
        "current_org": "淄川区人民政府",
        "source": "淄川区人民政府网站, 执法检查和产学研对接报道 (2026年6月-7月)"
    },
    # 刘鹏飞 — 副区长
    {
        "id": 15,
        "name": "刘鹏飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "淄川区副区长",
        "current_org": "淄川区人民政府",
        "source": "淄川区人民政府网站, 生态环境和防汛调研报道 (2026年7月)"
    },

    # ══════════════════════════════════════════════════════════════════════════
    # 人大 / 政协 副职
    # ══════════════════════════════════════════════════════════════════════════

    # 李洁 — 区人大常委会副主任
    {
        "id": 16,
        "name": "李洁",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "淄川区人大常委会副主任",
        "current_org": "淄川区人民代表大会常务委员会",
        "source": "淄川区人民政府网站, 人大会议报道 (2026年6月-7月)"
    },
    # 赵长浩 — 区人大常委会副主任
    {
        "id": 17,
        "name": "赵长浩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "淄川区人大常委会副主任",
        "current_org": "淄川区人民代表大会常务委员会",
        "source": "淄川区人民政府网站, 人大会议报道 (2026年6月-7月)"
    },
    # 张学文 — 区人大常委会副主任
    {
        "id": 18,
        "name": "张学文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "淄川区人大常委会副主任",
        "current_org": "淄川区人民代表大会常务委员会",
        "source": "淄川区人民政府网站, 人大会议报道 (2026年6月-7月)"
    },
    # 张立冬 — 区人大常委会副主任
    {
        "id": 19,
        "name": "张立冬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "淄川区人大常委会副主任",
        "current_org": "淄川区人民代表大会常务委员会",
        "source": "淄川区人民政府网站, 人大会议和调研报道 (2026年6月-7月)"
    },
    # 唐凤德 — 区政协副主席
    {
        "id": 20,
        "name": "唐凤德",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "淄川区政协副主席",
        "current_org": "中国人民政治协商会议淄川区委员会",
        "source": "淄川区人民政府网站, 城管进社区提案督办报道 (2026年6月)"
    },
    # 张继波 — 区政协副主席
    {
        "id": 21,
        "name": "张继波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "淄川区政协副主席",
        "current_org": "中国人民政治协商会议淄川区委员会",
        "source": "淄川区人民政府网站, 食品安全监督和农业调研报道 (2026年6月-7月)"
    },
    # 单志革 — 区政协副主席
    {
        "id": 22,
        "name": "单志革",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "淄川区政协副主席",
        "current_org": "中国人民政治协商会议淄川区委员会",
        "source": "淄川区人民政府网站, 夏日送清凉活动报道 (2026年7月)"
    },
    # 王利民 — 区政协秘书长
    {
        "id": 23,
        "name": "王利民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "淄川区政协秘书长",
        "current_org": "中国人民政治协商会议淄川区委员会",
        "source": "淄川区人民政府网站, 政协活动报道 (2026年6月-7月)"
    },
]

organizations_data = [
    {
        "id": 1,
        "name": "中共淄川区委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共淄博市委",
        "location": "山东淄博淄川"
    },
    {
        "id": 2,
        "name": "淄川区人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "淄博市人民政府",
        "location": "山东淄博淄川"
    },
    {
        "id": 3,
        "name": "淄川区人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "parent": "淄川区",
        "location": "山东淄博淄川"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议淄川区委员会",
        "type": "政协",
        "level": "县级",
        "parent": "淄川区",
        "location": "山东淄博淄川"
    },
    {
        "id": 5,
        "name": "淄川经济开发区",
        "type": "开发区",
        "level": "省级",
        "parent": "淄川区",
        "location": "山东淄博淄川"
    },
    {
        "id": 6,
        "name": "淄川区",
        "type": "政府",
        "level": "县级",
        "parent": "淄博市",
        "location": "山东淄博淄川"
    },
]

positions_data = [
    # 程勤 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "淄川区委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "区委书记"},
    # 冯炳涛 — 区长
    {"person_id": 2, "org_id": 2, "title": "淄川区委副书记、区长", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "淄川区委副书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 周恒学 — 区人大主任
    {"person_id": 3, "org_id": 3, "title": "淄川区人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": "区人大常委会党组书记"},
    # 李庭 — 区政协主席
    {"person_id": 4, "org_id": 4, "title": "淄川区政协主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": "区政协党组书记"},
    # 刘鸿智 — 区委副书记
    {"person_id": 5, "org_id": 1, "title": "淄川区委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 刘胜虎 — 组织部部长
    {"person_id": 6, "org_id": 1, "title": "淄川区委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 张山山 — 区委办公室主任
    {"person_id": 7, "org_id": 1, "title": "淄川区委常委、区委办公室主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 张刚 — 副区长兼开发区书记
    {"person_id": 8, "org_id": 2, "title": "淄川区委常委、副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 5, "title": "淄川经济开发区党工委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 冯明 — 副区长
    {"person_id": 9, "org_id": 2, "title": "淄川区委常委、副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 王倩雯 — 副区长
    {"person_id": 10, "org_id": 2, "title": "淄川区委常委、副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 周克聪 — 政法委书记
    {"person_id": 11, "org_id": 1, "title": "淄川区委常委、政法委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 穆立华 — 宣传部部长
    {"person_id": 12, "org_id": 1, "title": "淄川区委常委、宣传部部长、统战部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 赵聪 — 副区长
    {"person_id": 13, "org_id": 2, "title": "淄川区副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 王林 — 副区长
    {"person_id": 14, "org_id": 2, "title": "淄川区副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 刘鹏飞 — 副区长
    {"person_id": 15, "org_id": 2, "title": "淄川区副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 人大副主任
    {"person_id": 16, "org_id": 3, "title": "淄川区人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 17, "org_id": 3, "title": "淄川区人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 18, "org_id": 3, "title": "淄川区人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 19, "org_id": 3, "title": "淄川区人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 政协副主席/秘书长
    {"person_id": 20, "org_id": 4, "title": "淄川区政协副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 21, "org_id": 4, "title": "淄川区政协副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 22, "org_id": 4, "title": "淄川区政协副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 23, "org_id": 4, "title": "淄川区政协秘书长", "start_date": "", "end_date": "present", "rank": "正科级", "note": ""},
]

relationships_data = [
    # 程勤 <-> 冯炳涛 — 书记和区长工作搭档
    {
        "person_a": 1,
        "person_b": 2,
        "type": "overlap",
        "context": "淄川区委书记与区长工作搭档",
        "overlap_org": "淄川区",
        "overlap_period": "2026-",
    },
    # 程勤 <-> 刘鸿智 — 区委正副书记
    {
        "person_a": 1,
        "person_b": 5,
        "type": "superior_subordinate",
        "context": "淄川区委书记与副书记",
        "overlap_org": "中共淄川区委员会",
        "overlap_period": "2026-",
    },
    # 程勤 <-> 刘胜虎 — 书记与组织部部长
    {
        "person_a": 1,
        "person_b": 6,
        "type": "superior_subordinate",
        "context": "区委书记与组织部部长",
        "overlap_org": "中共淄川区委员会",
        "overlap_period": "2026-",
    },
    # 程勤 <-> 张山山 — 书记与办公室主任
    {
        "person_a": 1,
        "person_b": 7,
        "type": "superior_subordinate",
        "context": "区委书记与区委办公室主任",
        "overlap_org": "中共淄川区委员会",
        "overlap_period": "2026-",
    },
    # 程勤 <-> 穆立华 — 书记与宣传部部长
    {
        "person_a": 1,
        "person_b": 12,
        "type": "superior_subordinate",
        "context": "区委书记与宣传部部长",
        "overlap_org": "中共淄川区委员会",
        "overlap_period": "2026-",
    },
    # 程勤 <-> 周克聪 — 书记与政法委书记
    {
        "person_a": 1,
        "person_b": 11,
        "type": "superior_subordinate",
        "context": "区委书记与政法委书记",
        "overlap_org": "中共淄川区委员会",
        "overlap_period": "2026-",
    },
    # 冯炳涛 <-> 张刚 — 区长与常务副区长
    {
        "person_a": 2,
        "person_b": 8,
        "type": "superior_subordinate",
        "context": "区长与副区长（开发区党工委书记）",
        "overlap_org": "淄川区人民政府",
        "overlap_period": "2026-",
    },
    # 冯炳涛 <-> 冯明 — 区长与副区长
    {
        "person_a": 2,
        "person_b": 9,
        "type": "superior_subordinate",
        "context": "区长与副区长",
        "overlap_org": "淄川区人民政府",
        "overlap_period": "2026-",
    },
    # 冯炳涛 <-> 王倩雯 — 区长与副区长
    {
        "person_a": 2,
        "person_b": 10,
        "type": "superior_subordinate",
        "context": "区长与副区长",
        "overlap_org": "淄川区人民政府",
        "overlap_period": "2026-",
    },
    # 冯炳涛 <-> 赵聪 — 区长与副区长
    {
        "person_a": 2,
        "person_b": 13,
        "type": "superior_subordinate",
        "context": "区长与副区长",
        "overlap_org": "淄川区人民政府",
        "overlap_period": "2026-",
    },
    # 冯炳涛 <-> 王林 — 区长与副区长
    {
        "person_a": 2,
        "person_b": 14,
        "type": "superior_subordinate",
        "context": "区长与副区长",
        "overlap_org": "淄川区人民政府",
        "overlap_period": "2026-",
    },
    # 冯炳涛 <-> 刘鹏飞 — 区长与副区长
    {
        "person_a": 2,
        "person_b": 15,
        "type": "superior_subordinate",
        "context": "区长与副区长",
        "overlap_org": "淄川区人民政府",
        "overlap_period": "2026-",
    },
    # 周恒学 <-> 冯炳涛 — 人大主任与区长
    {
        "person_a": 3,
        "person_b": 2,
        "type": "overlap",
        "context": "人大主任与区长（监督与被监督关系）",
        "overlap_org": "淄川区",
        "overlap_period": "2026-",
    },
    # 李庭 <-> 程勤 — 政协主席与书记
    {
        "person_a": 4,
        "person_b": 1,
        "type": "overlap",
        "context": "政协主席与区委书记",
        "overlap_org": "淄川区",
        "overlap_period": "2026-",
    },
    # 张刚 <-> 张山山 — 同为常委
    {
        "person_a": 8,
        "person_b": 7,
        "type": "overlap",
        "context": "区委常委班子成员",
        "overlap_org": "中共淄川区委员会",
        "overlap_period": "2026-",
    },
    # 刘胜虎 <-> 张山山 — 常委间工作配合
    {
        "person_a": 6,
        "person_b": 7,
        "type": "overlap",
        "context": "区委常委班子成员，参与同一慰问活动",
        "overlap_org": "中共淄川区委员会",
        "overlap_period": "2026-",
    },
]


# ═══════════════════════════════════════════════════════════════════════════════
# Main
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"Building {SLUG} network...")
    print(f"  Persons: {len(persons_data)}")
    print(f"  Organizations: {len(organizations_data)}")
    print(f"  Positions: {len(positions_data)}")
    print(f"  Relationships: {len(relationships_data)}")

    run_build(
        slug=SLUG,
        persons=persons_data,
        organizations=organizations_data,
        positions=positions_data,
        relationships=relationships_data,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print("Done.")
