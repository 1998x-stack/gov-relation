#!/usr/bin/env python3
"""Build script for 浈江区 (Zhenjiang District, Shaoguan, Guangdong) leadership network.

Generated: 2026-07-22
Sources:
  - www.sgzj.gov.cn (official government website - 领导之窗)
  - sgzj.gov.cn news articles confirming区委书记 and区长
  - Baidu Baike / media reports
"""

import sqlite3  # noqa: used by gov_relation.runner

from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
from gov_relation.runner import run_build

# ═══════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════

# fmt: off
PERSONS = [
    # === 区委领导 ===
    {
        "id": 1,
        "name": "鲁锦锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年7月",
        "birthplace": "",
        "education": "中南财经政法大学（财政学专业）",
        "party_join": "",
        "work_start": "2006年",
        "current_post": "浈江区委书记",
        "current_org": "中共韶关市浈江区委员会",
        "source": "https://www.sgzj.gov.cn/xw/jrzj/content/post_2858196.html (confirmed as current区委书记 as of 2026-07-01)",
    },
    {
        "id": 2,
        "name": "周昭坚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年8月",
        "birthplace": "海南澄迈",
        "education": "华南师范大学、公共管理硕士",
        "party_join": "2004年6月",
        "work_start": "2005年9月",
        "current_post": "浈江区区长",
        "current_org": "韶关市浈江区人民政府",
        "source": "https://www.sgzj.gov.cn/zw/ldzc/content/post_2685267.html (official leadership profile)",
    },
    {
        "id": 3,
        "name": "马文娟",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委副书记",
        "current_org": "中共韶关市浈江区委员会",
        "source": "http://www.sgzj.gov.cn/xw/jrzj/content/post_2852208.html (confirmed as区委副书记 in寮浈对口帮扶 meeting 2026-06-01)",
    },
    {
        "id": 4,
        "name": "刘伟光",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区领导（推测常委/常务副区长）",
        "current_org": "中共韶关市浈江区委员会",
        "source": "http://www.sgzj.gov.cn/xw/jrzj/content/post_2858196.html (陪同鲁锦锋督导大数据产业园, 2026-06-26)",
    },
    # === 区政府领导 ===
    {
        "id": 5,
        "name": "马细妹",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1978年11月",
        "birthplace": "",
        "education": "仲恺农业工程学院",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "韶关市浈江区人民政府",
        "source": "https://www.sgzj.gov.cn/zw/ldzc/content/post_2005524.html (official leadership profile)",
    },
    {
        "id": 6,
        "name": "何爱华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年11月",
        "birthplace": "",
        "education": "韶关大学",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "韶关市浈江区人民政府",
        "source": "https://www.sgzj.gov.cn/zw/ldzc/content/post_2079582.html (official leadership profile)",
    },
    {
        "id": 7,
        "name": "王秉栋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年2月",
        "birthplace": "",
        "education": "甘肃政法学院",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长、市公安局浈江分局局长",
        "current_org": "韶关市浈江区人民政府",
        "source": "https://www.sgzj.gov.cn/zw/ldzc/content/post_2624153.html (official leadership profile)",
    },
    {
        "id": 8,
        "name": "赵少辉",
        "gender": "男",
        "ethnicity": "瑶族",
        "birth": "1986年11月",
        "birthplace": "",
        "education": "广东技术师范学院、文学学士",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "韶关市浈江区人民政府",
        "source": "https://www.sgzj.gov.cn/zw/ldzc/content/post_2775716.html (official leadership profile)",
    },
    {
        "id": 9,
        "name": "王剑斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年9月",
        "birthplace": "",
        "education": "中央广播电视大学",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "韶关市浈江区人民政府",
        "source": "https://www.sgzj.gov.cn/zw/ldzc/content/post_2775717.html (official leadership profile)",
    },
    # === 前任领导 ===
    {
        "id": 10,
        "name": "陈来安",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任区委书记（去向待查）",
        "current_org": "",
        "source": "http://www.sgzj.gov.cn/xw/jrzj/content/post_2499795.html (confirmed as previous区委书记 in Aug 2023)",
    },
    {
        "id": 11,
        "name": "曾清兰",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任区长（去向待查）",
        "current_org": "",
        "source": "https://zh.wikipedia.org/wiki/浈江区 (listed as former mayor, now outdated)",
    },
    # === 人大、政协 ===
    {
        "id": 12,
        "name": "黄德乔",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "韶关市浈江区政协",
        "source": "http://www.sgzj.gov.cn/xw/jrzj/content/post_2859405.html (confirmed as区政协主席)",
    },
    {
        "id": 13,
        "name": "罗永东",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "韶关市浈江区人大常委会",
        "source": "https://baijiahao.baidu.com (reported in 2021)",
    },
    # === 其他区领导 ===
    {
        "id": 14,
        "name": "尹荏彬",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政府党组成员、寮浈对口帮扶工作队长",
        "current_org": "韶关市浈江区人民政府",
        "source": "http://www.sgzj.gov.cn/xw/jrzj/content/post_2852208.html (寮浈对口帮扶 meeting, 2026-06-01)",
    },
]

ORGANIZATIONS = [
    {"id": 1, "name": "中共韶关市浈江区委员会", "type": "党委", "level": "正处级", "parent": "中共韶关市委员会", "location": "韶关市浈江区"},
    {"id": 2, "name": "韶关市浈江区人民政府", "type": "政府", "level": "正处级", "parent": "韶关市人民政府", "location": "韶关市浈江区"},
    {"id": 3, "name": "韶关市浈江区人大常委会", "type": "人大", "level": "正处级", "parent": "韶关市人大常委会", "location": "韶关市浈江区"},
    {"id": 4, "name": "韶关市浈江区政协", "type": "政协", "level": "正处级", "parent": "韶关市政协", "location": "韶关市浈江区"},
    {"id": 5, "name": "韶关市公安局浈江分局", "type": "政府", "level": "正科级", "parent": "韶关市公安局", "location": "韶关市浈江区"},
]

POSITIONS = [
    # 区委
    {"person_id": 1, "org_id": 1, "title": "浈江区委书记", "start_date": "2024年9月", "end_date": "present", "rank": "正处级", "note": "此前担任区政府党组书记、区长，2024年9月后一肩挑约1个月"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "2024年10月", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "确认在任2026年6月"},
    {"person_id": 4, "org_id": 1, "title": "区委常委（推测）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "具体分管职务未确认"},
    # 区政府
    {"person_id": 1, "org_id": 2, "title": "浈江区区长（前任）", "start_date": "2021年", "end_date": "2024年10月", "rank": "正处级", "note": "升任区委书记"},
    {"person_id": 2, "org_id": 2, "title": "浈江区区长", "start_date": "2024年10月", "end_date": "present", "rank": "正处级", "note": "2024年10月23日当选"},
    {"person_id": 5, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "区政府党组成员"},
    {"person_id": 6, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "区政府党组成员"},
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "区政府党组成员"},
    {"person_id": 8, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "区政府党组成员"},
    {"person_id": 9, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "区政府党组成员"},
    {"person_id": 14, "org_id": 2, "title": "区政府党组成员", "start_date": "", "end_date": "present", "rank": "副处级", "note": "寮浈对口帮扶工作队长"},
    # 公安
    {"person_id": 7, "org_id": 5, "title": "公安浈江分局局长", "start_date": "", "end_date": "present", "rank": "正科级（高配副处）", "note": ""},
    # 人大、政协
    {"person_id": 12, "org_id": 4, "title": "区政协主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 13, "org_id": 3, "title": "区人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 前任领导
    {"person_id": 10, "org_id": 1, "title": "浈江区委书记（前任）", "start_date": "约2020年", "end_date": "2024年9月", "rank": "正处级", "note": "去向待查"},
    {"person_id": 11, "org_id": 2, "title": "浈江区区长（前任）", "start_date": "", "end_date": "", "rank": "正处级", "note": "维基百科标注为区长，已离任，去向待查"},
]

# Relationships based on organizational overlap and working proximity
RELATIONSHIPS = [
    # 党政正职
    {"person_a": 1, "person_b": 2, "type": "党政正职搭档", "context": "区委书记-区长党政正职搭档", "overlap_org": "浈江区四套班子", "overlap_period": "2024年10月至今", "source": "", "confidence": "confirmed"},
    # 书记与前任书记（接任）
    {"person_a": 1, "person_b": 10, "type": "前后任", "context": "鲁锦锋接替陈来安任区委书记", "overlap_org": "浈江区委", "overlap_period": "2024年", "source": "", "confidence": "confirmed"},
    # 区长与前任区长（接任）
    {"person_a": 2, "person_b": 1, "type": "前后任", "context": "周昭坚接替鲁锦锋任区长", "overlap_org": "浈江区政府", "overlap_period": "2024年10月", "source": "", "confidence": "confirmed"},
    # 书记与区委副书记
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "区委书记—区委副书记", "overlap_org": "浈江区委常委会", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 3, "type": "同僚", "context": "区长—区委副书记", "overlap_org": "浈江区委常委会", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    # 区长与副区长
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "区长—副区长", "overlap_org": "浈江区人民政府", "overlap_period": "2024年10月至今", "source": "", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "区长—副区长", "overlap_org": "浈江区人民政府", "overlap_period": "2024年10月至今", "source": "", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "区长—副区长（公安局长）", "overlap_org": "浈江区人民政府", "overlap_period": "2024年10月至今", "source": "", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "区长—副区长", "overlap_org": "浈江区人民政府", "overlap_period": "2024年10月至今", "source": "", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "区长—副区长", "overlap_org": "浈江区人民政府", "overlap_period": "2024年10月至今", "source": "", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 14, "type": "上下级", "context": "区长—区政府党组成员（帮扶队长）", "overlap_org": "浈江区人民政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    # 副区长之间
    {"person_a": 5, "person_b": 6, "type": "同僚", "context": "副区长与副区长", "overlap_org": "浈江区人民政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 5, "person_b": 7, "type": "同僚", "context": "副区长与副区长（公安局长）", "overlap_org": "浈江区人民政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 5, "person_b": 8, "type": "同僚", "context": "副区长与副区长", "overlap_org": "浈江区人民政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 5, "person_b": 9, "type": "同僚", "context": "副区长与副区长", "overlap_org": "浈江区人民政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 6, "person_b": 7, "type": "同僚", "context": "副区长与副区长（公安局长）", "overlap_org": "浈江区人民政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 6, "person_b": 8, "type": "同僚", "context": "副区长与副区长", "overlap_org": "浈江区人民政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 6, "person_b": 9, "type": "同僚", "context": "副区长与副区长", "overlap_org": "浈江区人民政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 7, "person_b": 8, "type": "同僚", "context": "副区长（公安局长）与副区长", "overlap_org": "浈江区人民政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 7, "person_b": 9, "type": "同僚", "context": "副区长（公安局长）与副区长", "overlap_org": "浈江区人民政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 8, "person_b": 9, "type": "同僚", "context": "副区长与副区长", "overlap_org": "浈江区人民政府", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    # 书记与副区长
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "区委书记—副区长", "overlap_org": "浈江区", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "区委书记—副区长", "overlap_org": "浈江区", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "区委书记—副区长（公安）", "overlap_org": "浈江区", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "区委书记—副区长", "overlap_org": "浈江区", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "区委书记—副区长", "overlap_org": "浈江区", "overlap_period": "2026年", "source": "", "confidence": "confirmed"},
]

# fmt: on

# ═══════════════════════════════════════════════════════════════
# BUILD - Use staging paths
# ═══════════════════════════════════════════════════════════════

import sys
from pathlib import Path

STAGING_DIR = Path(__file__).parent
DB_PATH = STAGING_DIR / "浈江区_network.db"
GEXF_PATH = STAGING_DIR / "浈江区_network.gexf"

if __name__ == "__main__":
    run_build(
        slug="浈江区",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
