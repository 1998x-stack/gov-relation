#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 绥芬河市 (Suifenhe City), 黑龙江省.

Investigation date: 2026-07-24
Task ID: heilongjiang_绥芬河市
Level: 县级市
Targets: 市委书记 & 市长

Research sources:
  - suifenhe.gov.cn (绥芬河市政府官网) — 领导之窗 full roster
  - 王镭 detail page: https://www.suifenhe.gov.cn/sfh/c100952/202310/c03_270923.shtml
  - 康昊鹏 detail page: https://www.suifenhe.gov.cn/sfh/c100954/202310/c03_270938.shtml
  - Full leadership listing: https://www.suifenhe.gov.cn/sfh/c100951/ldzc.shtml

Confidence notes:
  - All current officeholders: confirmed via official government leadership page
  - Basic bio (name, gender, ethnicity, birth, education): confirmed via official detail pages
  - Detailed career histories: UNVERIFIED — only current position available from source
  - Web search (Exa) was rate-limited; Baidu returned 403; direct government site accessed successfully
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = STAGING_DIR.parents[2]  # repo root
SLUG = "绥芬河市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

# Staging paths
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR

# Canonical paths (after promotion)
CANONICAL_DB = BASE / "data" / "database" / f"{SLUG}_network.db"
CANONICAL_GEXF = BASE / "data" / "graph" / f"{SLUG}_network.gexf"
CANONICAL_BUILD = BASE / "scripts" / "build" / f"build_{SLUG}_data.py"
CANONICAL_PERSONS = BASE / "data" / "persons"

# ── Source register ─────────────────────────────────────────────────────────
SOURCES = {
    "S001": {
        "title": "绥芬河市领导之窗 - 市委",
        "url": "https://www.suifenhe.gov.cn/sfh/c100951/ldzc.shtml",
        "publisher": "绥芬河市人民政府",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
    },
    "S002": {
        "title": "王镭同志简历 - 绥芬河市委书记",
        "url": "https://www.suifenhe.gov.cn/sfh/c100952/202310/c03_270923.shtml",
        "publisher": "绥芬河市人民政府",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
    },
    "S003": {
        "title": "康昊鹏同志简历 - 绥芬河市长",
        "url": "https://www.suifenhe.gov.cn/sfh/c100954/202310/c03_270938.shtml",
        "publisher": "绥芬河市人民政府",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
    },
    "S004": {
        "title": "王耀同志简历 - 绥芬河市委常委、副市长",
        "url": "https://www.suifenhe.gov.cn/sfh/c100952/202310/c03_270933.shtml",
        "publisher": "绥芬河市人民政府",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
    },
    "S005": {
        "title": "邵云鹏同志简历 - 绥芬河市委常委、组织部部长",
        "url": "https://www.suifenhe.gov.cn/sfh/c100952/202310/c03_270926.shtml",
        "publisher": "绥芬河市人民政府",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
    },
    "S006": {
        "title": "李大鹏同志简历 - 绥芬河市委常委、纪委书记",
        "url": "https://www.suifenhe.gov.cn/sfh/c100952/202310/c03_270925.shtml",
        "publisher": "绥芬河市人民政府",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
    },
    "S007": {
        "title": "高俊同志简历 - 绥芬河市委副书记",
        "url": "https://www.suifenhe.gov.cn/sfh/c100952/202310/c03_270932.shtml",
        "publisher": "绥芬河市人民政府",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
    },
    "S008": {
        "title": "刘凤海同志简历 - 绥芬河市委常委、政法委书记",
        "url": "https://www.suifenhe.gov.cn/sfh/c100952/202310/c03_270948.shtml",
        "publisher": "绥芬河市人民政府",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
    },
    "S009": {
        "title": "柳秋晨同志简历 - 绥芬河市委常委、副市长",
        "url": "https://www.suifenhe.gov.cn/sfh/c100952/202310/c03_270944.shtml",
        "publisher": "绥芬河市人民政府",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
    },
    "S010": {
        "title": "绥芬河市人民政府 - 走进绥芬河",
        "url": "https://www.suifenhe.gov.cn/sfh/c100935/zjsfh.shtml",
        "publisher": "绥芬河市人民政府",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
    },
}

# ── Persons ─────────────────────────────────────────────────────────────────
persons = [
    # ═══════ Core Leadership ═══════
    {
        "id": 1,
        "name": "王镭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年6月",
        "birthplace": "",
        "education": "研究生学历，理学博士",
        "party_join": "",
        "work_start": "",
        "current_post": "牡丹江市委常委、绥芬河市委书记",
        "current_org": "中共绥芬河市委员会",
        "source": "S002",
    },
    {
        "id": 2,
        "name": "康昊鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年6月",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "市委副书记、市政府市长",
        "current_org": "绥芬河市人民政府",
        "source": "S003",
    },
    # ═══════ 市委常委会成员 ═══════
    {
        "id": 3,
        "name": "高俊",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1982年8月",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "市委副书记",
        "current_org": "中共绥芬河市委员会",
        "source": "S007",
    },
    {
        "id": 4,
        "name": "李铁东",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委副书记",
        "current_org": "中共绥芬河市委员会",
        "source": "S001",
    },
    {
        "id": 5,
        "name": "王耀",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年7月",
        "birthplace": "",
        "education": "大学文化，农业推广硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、市政府副市长、党组副书记",
        "current_org": "绥芬河市人民政府",
        "source": "S004",
    },
    {
        "id": 6,
        "name": "邵云鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1988年2月",
        "birthplace": "",
        "education": "研究生，公共管理硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、组织部部长",
        "current_org": "中共绥芬河市委员会",
        "source": "S005",
    },
    {
        "id": 7,
        "name": "李大鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年2月",
        "birthplace": "",
        "education": "法学硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、市纪委书记、市监委主任",
        "current_org": "中共绥芬河市纪律检查委员会",
        "source": "S006",
    },
    {
        "id": 8,
        "name": "冷智峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、市政府副市长、党组成员",
        "current_org": "绥芬河市人民政府",
        "source": "S001",
    },
    {
        "id": 9,
        "name": "刘凤海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年6月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、政法委书记",
        "current_org": "中共绥芬河市委员会",
        "source": "S008",
    },
    {
        "id": 10,
        "name": "袁兴宾",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、人武部政委",
        "current_org": "绥芬河市人民武装部",
        "source": "S001",
    },
    {
        "id": 11,
        "name": "柳秋晨",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1985年9月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、市政府副市长",
        "current_org": "绥芬河市人民政府",
        "source": "S009",
    },
    # ═══════ 市人大 ═══════
    {
        "id": 12,
        "name": "赵广友",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年3月",
        "birthplace": "",
        "education": "大专学历",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会党组书记、主任",
        "current_org": "绥芬河市人大常委会",
        "source": "S001",
    },
    {
        "id": 13,
        "name": "宋雪花",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会副主任",
        "current_org": "绥芬河市人大常委会",
        "source": "S001",
    },
    {
        "id": 14,
        "name": "李明雷",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会党组副书记、副主任",
        "current_org": "绥芬河市人大常委会",
        "source": "S001",
    },
    {
        "id": 15,
        "name": "高立彬",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会党组成员、副主任",
        "current_org": "绥芬河市人大常委会",
        "source": "S001",
    },
    {
        "id": 16,
        "name": "曲修季",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会党组成员、副主任候选人",
        "current_org": "绥芬河市人大常委会",
        "source": "S001",
    },
    # ═══════ 市政府班子成员 ═══════
    {
        "id": 17,
        "name": "岳强",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政府副市长、党组成员、市公安局局长",
        "current_org": "绥芬河市人民政府",
        "source": "S001",
    },
    {
        "id": 18,
        "name": "马刚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政府副市长、党组成员，自贸片区管委会副主任",
        "current_org": "绥芬河市人民政府",
        "source": "S001",
    },
    {
        "id": 19,
        "name": "韩冰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政府副市长、党组成员，自贸片区管委会副主任",
        "current_org": "绥芬河市人民政府",
        "source": "S001",
    },
    {
        "id": 20,
        "name": "黄绪忠",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政府副市长、党组成员，自贸片区管委会副主任",
        "current_org": "绥芬河市人民政府",
        "source": "S001",
    },
    # ═══════ 市政协 ═══════
    {
        "id": 21,
        "name": "刘在明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年2月",
        "birthplace": "",
        "education": "工程硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协党组书记、主席",
        "current_org": "绥芬河市政协",
        "source": "S001",
    },
    {
        "id": 22,
        "name": "叶剑波",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协副主席、民建市委主委、绥芬河海关副关长",
        "current_org": "绥芬河市政协",
        "source": "S001",
    },
    {
        "id": 23,
        "name": "柴桂荣",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协党组副书记、副主席",
        "current_org": "绥芬河市政协",
        "source": "S001",
    },
    {
        "id": 24,
        "name": "王强",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协副主席",
        "current_org": "绥芬河市政协",
        "source": "S001",
    },
    {
        "id": 25,
        "name": "桑志斌",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协党组成员、秘书长",
        "current_org": "绥芬河市政协",
        "source": "S001",
    },
    # ═══════ 自贸片区管委会 ═══════
    {
        "id": 26,
        "name": "郭振田",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年12月",
        "birthplace": "",
        "education": "研究生学历，哲学硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "自贸片区党工委委员、管委会专职副主任",
        "current_org": "中国（黑龙江）自由贸易试验区绥芬河片区管委会",
        "source": "S001",
    },
    {
        "id": 27,
        "name": "孙钰强",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "自贸片区管委会副主任",
        "current_org": "中国（黑龙江）自由贸易试验区绥芬河片区管委会",
        "source": "S001",
    },
    {
        "id": 28,
        "name": "吴庆勇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "自贸片区管委会副主任",
        "current_org": "中国（黑龙江）自由贸易试验区绥芬河片区管委会",
        "source": "S001",
    },
    {
        "id": 29,
        "name": "姜英",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "自贸片区管委会副主任",
        "current_org": "中国（黑龙江）自由贸易试验区绥芬河片区管委会",
        "source": "S001",
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共绥芬河市委员会", "type": "党委", "level": "县级", "parent": "中共牡丹江市委员会", "location": "绥芬河市"},
    {"id": 2, "name": "绥芬河市人民政府", "type": "政府", "level": "县级", "parent": "牡丹江市人民政府", "location": "绥芬河市"},
    {"id": 3, "name": "绥芬河市人大常委会", "type": "人大", "level": "县级", "parent": "牡丹江市人大常委会", "location": "绥芬河市"},
    {"id": 4, "name": "绥芬河市政协", "type": "政协", "level": "县级", "parent": "牡丹江市政协", "location": "绥芬河市"},
    {"id": 5, "name": "中共绥芬河市纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共牡丹江市纪律检查委员会", "location": "绥芬河市"},
    {"id": 6, "name": "绥芬河市人民武装部", "type": "事业单位", "level": "县级", "parent": "牡丹江军分区", "location": "绥芬河市"},
    {"id": 7, "name": "绥芬河市公安局", "type": "政府", "level": "县级", "parent": "绥芬河市人民政府", "location": "绥芬河市"},
    {"id": 8, "name": "中国（黑龙江）自由贸易试验区绥芬河片区管委会", "type": "开发区", "level": "县级", "parent": "黑龙江省人民政府", "location": "绥芬河市"},
    {"id": 9, "name": "绥芬河镇", "type": "乡镇/街道", "level": "乡镇", "parent": "绥芬河市人民政府", "location": "绥芬河市"},
    {"id": 10, "name": "阜宁镇", "type": "乡镇/街道", "level": "乡镇", "parent": "绥芬河市人民政府", "location": "绥芬河市"},
]

# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    # 王镭
    {"person_id": 1, "org_id": 1, "title": "牡丹江市委常委（兼）", "start": "", "end": "present", "rank": "副厅级", "note": "高配，牡丹江市委常委兼任绥芬河市委书记"},
    {"person_id": 1, "org_id": 1, "title": "绥芬河市委书记", "start": "2023年", "end": "present", "rank": "正处级", "note": "市委全面工作"},
    {"person_id": 1, "org_id": 8, "title": "自贸片区党工委副书记、管委会常务副主任", "start": "", "end": "present", "rank": "", "note": ""},
    # 康昊鹏
    {"person_id": 2, "org_id": 2, "title": "市政府市长", "start": "", "end": "present", "rank": "正处级", "note": "主持市政府全面工作"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start": "", "end": "present", "rank": "", "note": ""},
    {"person_id": 2, "org_id": 8, "title": "自贸片区党工委委员、管委会副主任", "start": "", "end": "present", "rank": "", "note": ""},
    # 高俊
    {"person_id": 3, "org_id": 1, "title": "市委副书记", "start": "", "end": "present", "rank": "副处级", "note": "受市委书记委托处理市委有关事宜"},
    {"person_id": 3, "org_id": 8, "title": "自贸片区党工委委员", "start": "", "end": "present", "rank": "", "note": ""},
    # 李铁东
    {"person_id": 4, "org_id": 1, "title": "市委副书记", "start": "2025", "end": "present", "rank": "副处级", "note": "2025年上任"},
    # 王耀
    {"person_id": 5, "org_id": 2, "title": "市委常委、市政府副市长、党组副书记", "start": "", "end": "present", "rank": "副处级", "note": "政府常务工作"},
    {"person_id": 5, "org_id": 8, "title": "自贸片区党工委委员、管委会副主任", "start": "", "end": "present", "rank": "", "note": ""},
    # 邵云鹏
    {"person_id": 6, "org_id": 1, "title": "市委常委、组织部部长", "start": "", "end": "present", "rank": "副处级", "note": "负责组织、干部、人才、党建"},
    # 李大鹏
    {"person_id": 7, "org_id": 5, "title": "市委常委、市纪委书记、市监委主任", "start": "", "end": "present", "rank": "副处级", "note": "负责纪检、监察、巡察"},
    # 冷智峰
    {"person_id": 8, "org_id": 2, "title": "市委常委、市政府副市长、党组成员", "start": "2025", "end": "present", "rank": "副处级", "note": "2025年8月上任"},
    # 刘凤海
    {"person_id": 9, "org_id": 1, "title": "市委常委、政法委书记", "start": "", "end": "present", "rank": "副处级", "note": "负责政法、社会稳定"},
    # 袁兴宾
    {"person_id": 10, "org_id": 6, "title": "市委常委、人武部政委", "start": "", "end": "present", "rank": "", "note": ""},
    # 柳秋晨
    {"person_id": 11, "org_id": 2, "title": "市委常委、市政府副市长", "start": "", "end": "present", "rank": "副处级", "note": "负责教育、医疗卫生、市场监管"},
    # 赵广友
    {"person_id": 12, "org_id": 3, "title": "市人大常委会党组书记、主任", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 宋雪花
    {"person_id": 13, "org_id": 3, "title": "市人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 李明雷
    {"person_id": 14, "org_id": 3, "title": "市人大常委会党组副书记、副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 高立彬
    {"person_id": 15, "org_id": 3, "title": "市人大常委会党组成员、副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 曲修季
    {"person_id": 16, "org_id": 3, "title": "市人大常委会党组成员、副主任候选人", "start": "", "end": "present", "rank": "副处级", "note": "候选人"},
    # 岳强
    {"person_id": 17, "org_id": 2, "title": "市政府副市长、党组成员", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 17, "org_id": 7, "title": "市公安局局长", "start": "", "end": "present", "rank": "", "note": ""},
    # 马刚
    {"person_id": 18, "org_id": 2, "title": "市政府副市长、党组成员", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 18, "org_id": 8, "title": "自贸片区管委会副主任", "start": "", "end": "present", "rank": "", "note": ""},
    # 韩冰
    {"person_id": 19, "org_id": 2, "title": "市政府副市长、党组成员", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 19, "org_id": 8, "title": "自贸片区管委会副主任", "start": "", "end": "present", "rank": "", "note": ""},
    # 黄绪忠
    {"person_id": 20, "org_id": 2, "title": "市政府副市长、党组成员", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 20, "org_id": 8, "title": "自贸片区管委会副主任", "start": "", "end": "present", "rank": "", "note": ""},
    # 刘在明
    {"person_id": 21, "org_id": 4, "title": "市政协党组书记、主席", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 叶剑波
    {"person_id": 22, "org_id": 4, "title": "市政协副主席", "start": "", "end": "present", "rank": "副处级", "note": "民建市委主委、绥芬河海关副关长兼"},
    # 柴桂荣
    {"person_id": 23, "org_id": 4, "title": "市政协党组副书记、副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 王强
    {"person_id": 24, "org_id": 4, "title": "市政协副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 桑志斌
    {"person_id": 25, "org_id": 4, "title": "市政协党组成员、秘书长", "start": "", "end": "present", "rank": "正科级", "note": ""},
    # 郭振田
    {"person_id": 26, "org_id": 8, "title": "自贸片区党工委委员、管委会专职副主任", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 孙钰强
    {"person_id": 27, "org_id": 8, "title": "自贸片区管委会副主任", "start": "", "end": "present", "rank": "", "note": ""},
    # 吴庆勇
    {"person_id": 28, "org_id": 8, "title": "自贸片区管委会副主任", "start": "", "end": "present", "rank": "", "note": ""},
    # 姜英
    {"person_id": 29, "org_id": 8, "title": "自贸片区管委会副主任", "start": "", "end": "present", "rank": "", "note": ""},
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    # 王镭 ↔ 康昊鹏 — 党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "市委书记与市长党政正职搭档", "overlap_org": "中共绥芬河市委员会", "overlap_period": "present"},
    # 王镭 ↔ 高俊 — 书记与副书记
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "市委书记与专职副书记", "overlap_org": "中共绥芬河市委员会", "overlap_period": "present"},
    # 王镭 ↔ 李铁东 — 书记与副书记
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "市委书记与副书记", "overlap_org": "中共绥芬河市委员会", "overlap_period": "present"},
    # 王镭 ↔ 邵云鹏 — 书记与组织部部长
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "市委书记与组织部部长", "overlap_org": "中共绥芬河市委员会", "overlap_period": "present"},
    # 王镭 ↔ 李大鹏 — 书记与纪委书记
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "市委书记与纪委书记", "overlap_org": "中共绥芬河市委员会", "overlap_period": "present"},
    # 王镭 ↔ 刘凤海 — 书记与政法委书记
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "市委书记与政法委书记", "overlap_org": "中共绥芬河市委员会", "overlap_period": "present"},
    # 王耀 ↔ 康昊鹏 — 常务副市长与市长
    {"person_a": 5, "person_b": 2, "type": "superior_subordinate", "context": "常务副市长协助市长工作", "overlap_org": "绥芬河市人民政府", "overlap_period": "present"},
    # 邵云鹏 ↔ 李大鹏 — 组织部长与纪委书记（常委同僚）
    {"person_a": 6, "person_b": 7, "type": "overlap", "context": "同为市委常委班子成员", "overlap_org": "中共绥芬河市委员会", "overlap_period": "present"},
    # 高俊 ↔ 王耀 — 副书记与常务副市长
    {"person_a": 3, "person_b": 5, "type": "overlap", "context": "市委副书记与常务副市长工作协作", "overlap_org": "中共绥芬河市委员会", "overlap_period": "present"},
    # 康昊鹏 ↔ 岳强 — 市长与公安局长
    {"person_a": 2, "person_b": 17, "type": "superior_subordinate", "context": "市长与公安局长", "overlap_org": "绥芬河市人民政府", "overlap_period": "present"},
    # 自贸片区领导层交集
    {"person_a": 1, "person_b": 26, "type": "overlap", "context": "同为自贸片区领导成员", "overlap_org": "中国（黑龙江）自由贸易试验区绥芬河片区管委会", "overlap_period": "present"},
    {"person_a": 2, "person_b": 26, "type": "overlap", "context": "同为自贸片区领导成员", "overlap_org": "中国（黑龙江）自由贸易试验区绥芬河片区管委会", "overlap_period": "present"},
    # 柳秋晨 ↔ 康昊鹏
    {"person_a": 11, "person_b": 2, "type": "superior_subordinate", "context": "副市长协助市长分管教育、医疗工作", "overlap_org": "绥芬河市人民政府", "overlap_period": "present"},
]


# ═══════════════════════════════════════════════════════════════════════════
# SQLite + GEXF Build
# ═══════════════════════════════════════════════════════════════════════════

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    """Return GEXF color for a person based on role."""
    post = p.get("current_post", "")
    if "书记" in post and "纪委" not in post:
        if "市委" in post or "县委书记" in post or "区委书记" in post:
            return "255,50,50"  # Red — party secretary
        return "255,50,50"
    if "市长" in post or "县长" in post or "区长" in post:
        return "50,100,255"  # Blue — government leader
    if "纪委" in post or "监委" in post:
        return "255,165,0"  # Orange — discipline
    if "副书记" in post:
        return "255,50,50"  # Red — deputy party secretary
    if "副市长" in post or "副区长" in post or "副镇长" in post:
        return "50,100,255"  # Blue — deputy government
    return "100,100,100"  # Grey — other


def org_color(o):
    t = o.get("type", "")
    return {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "开发区": "200,255,200",
        "乡镇/街道": "255,255,200",
        "事业单位": "220,220,220",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "群团": "255,220,255",
    }.get(t, "200,200,200")


def is_top_leader(p):
    name = p["name"]
    # 王镭 is 市委书记 (and 牡丹江市委常委), 康昊鹏 is 市长
    return name in ("王镭", "康昊鹏")


def build_sqlite(path):
    import sqlite3
    conn = sqlite3.connect(str(path))
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
            source TEXT
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
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        cur.execute(
            "INSERT OR REPLACE INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
            (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
             p.get("birth", ""), p.get("birthplace", ""), p.get("education", ""),
             p.get("party_join", ""), p.get("work_start", ""),
             p.get("current_post", ""), p.get("current_org", ""), p.get("source", "")),
        )

    for o in organizations:
        cur.execute(
            "INSERT OR REPLACE INTO organizations (id, name, type, level, parent, location) VALUES (?,?,?,?,?,?)",
            (o["id"], o["name"], o["type"], o.get("level", ""), o.get("parent", ""), o.get("location", "")),
        )

    for pos in positions:
        cur.execute(
            "INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)",
            (pos["person_id"], pos["org_id"], pos["title"], pos.get("start", ""),
             pos.get("end", ""), pos.get("rank", ""), pos.get("note", "")),
        )

    for r in relationships:
        cur.execute(
            "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
            (r["person_a"], r["person_b"], r["type"], r["context"],
             r.get("overlap_org", ""), r.get("overlap_period", "")),
        )

    conn.commit()
    conn.close()

    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")


def build_gexf(path):
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append(f'    <description>绥芬河市领导工作关系网络 - {AS_OF}</description>')
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
    lines.append('      <attribute id="2" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes: persons
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes: organizations
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o.get("level", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # person → organization (worked_at)
    for pos in positions:
        title = pos["title"]
        lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos.get("start", "") + "-" + pos.get("end", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # person ↔ person (relationship)
    for r in relationships:
        lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_period", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"  Nodes: {len(persons)} persons + {len(organizations)} orgs = {len(persons) + len(organizations)}")
    print(f"  Edges: {len(positions)} worked_at + {len(relationships)} relationship = {len(positions) + len(relationships)}")


def main():
    print(f"=== Building 绥芬河市 data ===")
    print(f"DB path: {DB_PATH}")
    print(f"GEXF path: {GEXF_PATH}")

    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    print("\n--- SQLite Database ---")
    build_sqlite(DB_PATH)
    db_size = DB_PATH.stat().st_size
    print(f"  DB file size: {db_size} bytes")

    print("\n--- GEXF Graph ---")
    build_gexf(GEXF_PATH)
    gexf_size = GEXF_PATH.stat().st_size
    print(f"  GEXF file size: {gexf_size} bytes")

    print("\n=== Done ===")


if __name__ == "__main__":
    main()
