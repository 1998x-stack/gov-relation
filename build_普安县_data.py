#!/usr/bin/env python3
"""Build script for 普安县 (Pu'an County, Qianxinan, Guizhou) leadership network.

Generated: 2026-07-23
Level: 县
Province: 贵州省
Parent City: 黔西南布依族苗族自治州
Targets: 县委书记 & 县长

Research Note (2026-07-23):
  Web sources were accessible:
  - Official site www.puan.gov.cn: fully accessible
  - Leadership page (/zwgk/ldzc/): lists 县长、副县长
  - News articles (xwfb/payw/): multiple articles through 2026-07-23

  Key findings:
  - 县委书记: 黄其兴 — confirmed as 县委书记 via multiple official news
  - 县长: 郭媛媛 — confirmed as 县委副书记、县长 via leadership page and news
  - 县委副书记: 江洪涛, 陈玉祥
  - 常务副县长: 付忠文 (县委常委、副县长、党组副书记)
  - 县委常委/副县长: 邬淑娴, 马新, 李秀松
  - 政协主席: 蔡洪斌
  - 人大党组书记/主任候选人: 戴松
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from gov_relation.runner import run_build

# ═══════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════

PERSONS = [
    # ── Core Leaders ──
    {
        "id": 1,
        "name": "黄其兴",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "普安县委书记",
        "current_org": "中共普安县委员会",
        "source": "普安县政府网 新闻《普安县委专题会议召开》(2026-07-13); 《十三届普安县委常委会第159次会议召开》(2026-07-15). 受县委书记黄其兴委托主持会议.",
    },
    {
        "id": 2,
        "name": "郭媛媛",
        "gender": "女",
        "ethnicity": "布依族",
        "birth": "1982年12月",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "普安县委副书记、县人民政府县长",
        "current_org": "普安县人民政府",
        "source": "普安县政府网 领导之窗; 《十三届普安县委常委会第159次会议召开》等新闻报道.",
    },
    {
        "id": 3,
        "name": "付忠文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年6月",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "普安县委常委、县人民政府副县长（常务）",
        "current_org": "普安县人民政府",
        "source": "普安县政府网 领导之窗 付忠文简历页.",
    },
    {
        "id": 4,
        "name": "江洪涛",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "普安县委副书记",
        "current_org": "中共普安县委员会",
        "source": "普安县政府网 新闻《十三届普安县委常委会第159次会议召开》.",
    },
    {
        "id": 5,
        "name": "陈玉祥",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "普安县委副书记",
        "current_org": "中共普安县委员会",
        "source": "普安县政府网 新闻《十三届普安县委常委会第159次会议召开》.",
    },
    {
        "id": 6,
        "name": "戴松",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "普安县人大常委会党组书记、主任候选人",
        "current_org": "普安县人大常委会",
        "source": "普安县政府网 新闻《十三届普安县委常委会第159次会议召开》《普安县第十八届人大常委会第四十次会议召开》.",
    },
    {
        "id": 7,
        "name": "蔡洪斌",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "普安县政协主席",
        "current_org": "政协普安县委员会",
        "source": "普安县政府网 新闻《十三届普安县委常委会第159次会议召开》.",
    },
    {
        "id": 8,
        "name": "邬淑娴",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1976年3月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "普安县委常委、县人民政府副县长",
        "current_org": "普安县人民政府",
        "source": "普安县政府网 领导之窗 邬淑娴简历页.",
    },
    {
        "id": 9,
        "name": "马新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年12月",
        "birthplace": "",
        "education": "复旦大学理学博士",
        "party_join": "中共党员",
        "work_start": "2014年7月",
        "current_post": "普安县委常委、县人民政府副县长",
        "current_org": "普安县人民政府",
        "source": "普安县政府网 领导之窗 马新简历页.",
    },
    {
        "id": 10,
        "name": "李秀松",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年8月",
        "birthplace": "",
        "education": "农业推广硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "普安县委常委、县人民政府副县长",
        "current_org": "普安县人民政府",
        "source": "普安县政府网 领导之窗 李秀松简历页.",
    },
    {
        "id": 11,
        "name": "王彪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年9月",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "普安县人民政府副县长",
        "current_org": "普安县人民政府",
        "source": "普安县政府网 领导之窗 王彪简历页.",
    },
    {
        "id": 12,
        "name": "刘金",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年9月",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "普安县人民政府副县长",
        "current_org": "普安县人民政府",
        "source": "普安县政府网 领导之窗 刘金简历页.",
    },
    {
        "id": 13,
        "name": "沈健",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年9月",
        "birthplace": "",
        "education": "大学，工程硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "普安县人民政府副县长",
        "current_org": "普安县人民政府",
        "source": "普安县政府网 领导之窗 沈健简历页.",
    },
    {
        "id": 14,
        "name": "周直",
        "gender": "男",
        "ethnicity": "布依族",
        "birth": "1984年1月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "普安县人民政府副县长",
        "current_org": "普安县人民政府",
        "source": "普安县政府网 领导之窗 周直简历页.",
    },
    {
        "id": 15,
        "name": "王国元",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年8月",
        "birthplace": "",
        "education": "大学工科学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "普安县人民政府副县长人选",
        "current_org": "普安县人民政府",
        "source": "普安县政府网 领导之窗 王国元简历页; 县十八届人大常委会第四十次会议任命.",
    },
    {
        "id": 16,
        "name": "陈太阳",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "普安县人大常委会副主任",
        "current_org": "普安县人大常委会",
        "source": "普安县政府网 新闻《普安县第十八届人大常委会第四十次会议召开》.",
    },
    {
        "id": 17,
        "name": "李国奉",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "普安县人大常委会副主任",
        "current_org": "普安县人大常委会",
        "source": "同上.",
    },
    {
        "id": 18,
        "name": "黄玉能",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "普安县人大常委会副主任",
        "current_org": "普安县人大常委会",
        "source": "同上.",
    },
    {
        "id": 19,
        "name": "董艳均",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "普安县人大常委会副主任",
        "current_org": "普安县人大常委会",
        "source": "同上.",
    },
    {
        "id": 20,
        "name": "周灿",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "普安县人大常委会副主任",
        "current_org": "普安县人大常委会",
        "source": "同上.",
    },
    {
        "id": 21,
        "name": "张钧",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "普安县人大常委会副主任",
        "current_org": "普安县人大常委会",
        "source": "同上.",
    },
    {
        "id": 22,
        "name": "李兆丰",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "普安县领导",
        "current_org": "普安县人民政府",
        "source": "普安县政府网 新闻《普安县第十八届人大常委会第四十次会议召开》.",
    },
]

ORGANIZATIONS = [
    {
        "id": 1,
        "name": "中共普安县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共黔西南州委员会",
        "location": "贵州省黔西南州普安县",
    },
    {
        "id": 2,
        "name": "普安县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "黔西南州人民政府",
        "location": "贵州省黔西南州普安县",
    },
    {
        "id": 3,
        "name": "普安县人大常委会",
        "type": "人大",
        "level": "县",
        "parent": "黔西南州人大常委会",
        "location": "贵州省黔西南州普安县",
    },
    {
        "id": 4,
        "name": "政协普安县委员会",
        "type": "政协",
        "level": "县",
        "parent": "政协黔西南州委员会",
        "location": "贵州省黔西南州普安县",
    },
]

POSITIONS = [
    # 黄其兴 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "普安县委书记", "start_date": "", "end_date": "present", "rank": "正县级", "note": "current as of 2026-07; confirmed via multiple official news"},
    # 郭媛媛 — 县长
    {"person_id": 2, "org_id": 1, "title": "普安县委副书记", "start_date": "", "end_date": "present", "rank": "正县级", "note": "concurrent with 县长 role"},
    {"person_id": 2, "org_id": 2, "title": "普安县人民政府县长", "start_date": "", "end_date": "present", "rank": "正县级", "note": "current as of 2026-07"},
    # 付忠文 — 常务副县长
    {"person_id": 3, "org_id": 1, "title": "普安县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "普安县人民政府副县长（常务）", "start_date": "", "end_date": "present", "rank": "副县级", "note": "党组副书记"},
    # 江洪涛 — 县委副书记
    {"person_id": 4, "org_id": 1, "title": "普安县委副书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 陈玉祥 — 县委副书记
    {"person_id": 5, "org_id": 1, "title": "普安县委副书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 戴松 — 人大
    {"person_id": 6, "org_id": 3, "title": "普安县人大常委会党组书记、主任候选人", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
    # 蔡洪斌 — 政协
    {"person_id": 7, "org_id": 4, "title": "普安县政协主席", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
    # 邬淑娴 — 县委常委、副县长
    {"person_id": 8, "org_id": 1, "title": "普安县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "普安县人民政府副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 马新 — 县委常委、副县长
    {"person_id": 9, "org_id": 1, "title": "普安县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "普安县人民政府副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 李秀松 — 县委常委、副县长
    {"person_id": 10, "org_id": 1, "title": "普安县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "普安县人民政府副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 王彪 — 副县长
    {"person_id": 11, "org_id": 2, "title": "普安县人民政府副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 刘金 — 副县长
    {"person_id": 12, "org_id": 2, "title": "普安县人民政府副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 沈健 — 副县长（兼公安局长）
    {"person_id": 13, "org_id": 2, "title": "普安县人民政府副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "主持公安局全面工作"},
    # 周直 — 副县长
    {"person_id": 14, "org_id": 2, "title": "普安县人民政府副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 王国元 — 副县长（新任）
    {"person_id": 15, "org_id": 2, "title": "普安县人民政府副县长人选", "start_date": "2026-07", "end_date": "present", "rank": "副县级", "note": "2026年7月县人大常委会第四十次会议任命"},
    # 人大副主任们
    {"person_id": 16, "org_id": 3, "title": "普安县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 17, "org_id": 3, "title": "普安县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 18, "org_id": 3, "title": "普安县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 19, "org_id": 3, "title": "普安县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 20, "org_id": 3, "title": "普安县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 21, "org_id": 3, "title": "普安县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 李兆丰 — 县领导
    {"person_id": 22, "org_id": 2, "title": "普安县领导", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
]

RELATIONSHIPS = [
    # 黄其兴与郭媛媛（书记-县长搭班子）
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记—县长搭班子",
        "overlap_org": "中共普安县委员会/普安县人民政府",
        "overlap_period": "current（截至2026-07）",
    },
    # 黄其兴与付忠文
    {
        "person_a": 1, "person_b": 3,
        "type": "superior_subordinate",
        "context": "县委—政府常务副县长",
        "overlap_org": "中共普安县委员会",
        "overlap_period": "current（截至2026-07）",
    },
    # 黄其兴与江洪涛
    {
        "person_a": 1, "person_b": 4,
        "type": "superior_subordinate",
        "context": "县委正副书记",
        "overlap_org": "中共普安县委员会",
        "overlap_period": "current（截至2026-07）",
    },
    # 黄其兴与陈玉祥
    {
        "person_a": 1, "person_b": 5,
        "type": "superior_subordinate",
        "context": "县委正副书记",
        "overlap_org": "中共普安县委员会",
        "overlap_period": "current（截至2026-07）",
    },
    # 黄其兴与戴松
    {
        "person_a": 1, "person_b": 6,
        "type": "overlap",
        "context": "县委—人大",
        "overlap_org": "普安县四大班子",
        "overlap_period": "current（截至2026-07）",
    },
    # 黄其兴与蔡洪斌
    {
        "person_a": 1, "person_b": 7,
        "type": "overlap",
        "context": "县委—政协",
        "overlap_org": "普安县四大班子",
        "overlap_period": "current（截至2026-07）",
    },
    # 郭媛媛与付忠文（县长-常务副县长）
    {
        "person_a": 2, "person_b": 3,
        "type": "superior_subordinate",
        "context": "县长—常务副县长",
        "overlap_org": "普安县人民政府",
        "overlap_period": "current（截至2026-07）",
    },
    # 郭媛媛与江洪涛
    {
        "person_a": 2, "person_b": 4,
        "type": "overlap",
        "context": "政府—县委",
        "overlap_org": "中共普安县委员会",
        "overlap_period": "current（截至2026-07）",
    },
    # 郭媛媛与戴松
    {
        "person_a": 2, "person_b": 6,
        "type": "overlap",
        "context": "政府—人大",
        "overlap_org": "普安县四大班子",
        "overlap_period": "current（截至2026-07）",
    },
    # 郭媛媛与蔡洪斌
    {
        "person_a": 2, "person_b": 7,
        "type": "overlap",
        "context": "政府—政协",
        "overlap_org": "普安县四大班子",
        "overlap_period": "current（截至2026-07）",
    },
    # 付忠文与各副县长
    {"person_a": 3, "person_b": 8, "type": "overlap", "context": "县政府班子共事", "overlap_org": "普安县人民政府", "overlap_period": "current"},
    {"person_a": 3, "person_b": 9, "type": "overlap", "context": "县政府班子共事", "overlap_org": "普安县人民政府", "overlap_period": "current"},
    {"person_a": 3, "person_b": 10, "type": "overlap", "context": "县政府班子共事", "overlap_org": "普安县人民政府", "overlap_period": "current"},
    {"person_a": 3, "person_b": 11, "type": "overlap", "context": "县政府班子共事", "overlap_org": "普安县人民政府", "overlap_period": "current"},
    {"person_a": 3, "person_b": 12, "type": "overlap", "context": "县政府班子共事", "overlap_org": "普安县人民政府", "overlap_period": "current"},
    {"person_a": 3, "person_b": 13, "type": "overlap", "context": "县政府班子共事", "overlap_org": "普安县人民政府", "overlap_period": "current"},
    {"person_a": 3, "person_b": 14, "type": "overlap", "context": "县政府班子共事", "overlap_org": "普安县人民政府", "overlap_period": "current"},
    # 县委常委之间
    {"person_a": 8, "person_b": 9, "type": "overlap", "context": "县委常委班子共事", "overlap_org": "中共普安县委员会", "overlap_period": "current"},
    {"person_a": 8, "person_b": 10, "type": "overlap", "context": "县委常委班子共事", "overlap_org": "中共普安县委员会", "overlap_period": "current"},
    {"person_a": 9, "person_b": 10, "type": "overlap", "context": "县委常委班子共事", "overlap_org": "中共普安县委员会", "overlap_period": "current"},
    # 人大-政协
    {"person_a": 6, "person_b": 7, "type": "overlap", "context": "人大—政协", "overlap_org": "普安县四大班子", "overlap_period": "current"},
]

# ═══════════════════════════════════════════════════
# PERSON JSON HELPERS
# ═══════════════════════════════════════════════════

import json
import sqlite3  # noqa: used by process_tmp.py validator
import sys
from datetime import datetime
from pathlib import Path

AS_OF = "2026-07-23"
AS_OF_SHORT = AS_OF.replace("-", "")
SLUG = "普安县"
PROVINCE = "贵州省"
PARENT_CITY = "黔西南布依族苗族自治州"
TASK_ID = "guizhou_普安县"

TMP_DIR = Path(__file__).resolve().parent
DB_PATH = TMP_DIR / f"{SLUG}_network.db"
GEXF_PATH = TMP_DIR / f"{SLUG}_network.gexf"

SOURCE_REGISTER = [
    {
        "id": "S001",
        "title": "普安县人民政府门户网 — 领导之窗",
        "url": "https://www.puan.gov.cn/zwgk/ldzc/",
        "publisher": "普安县人民政府",
        "published_at": "",
        "accessed_at": "2026-07-23",
        "source_type": "official",
        "reliability": "high",
        "notes": "郭媛媛、付忠文、邬淑娴、马新、李秀松、王彪、刘金、沈健、周直、王国元等领导简历页",
    },
    {
        "id": "S002",
        "title": "普安县人民政府 — 政务要闻《普安县委专题会议召开》",
        "url": "https://www.puan.gov.cn/xwfb/payw/202607/t20260713_90611229.html",
        "publisher": "普安县融媒体中心",
        "published_at": "2026-07-13",
        "accessed_at": "2026-07-23",
        "source_type": "official",
        "reliability": "high",
        "notes": "受县委书记黄其兴委托，郭媛媛主持会议",
    },
    {
        "id": "S003",
        "title": "普安县人民政府 — 政务要闻《十三届普安县委常委会第159次会议召开》",
        "url": "https://www.puan.gov.cn/xwfb/payw/202607/t20260715_90621510.html",
        "publisher": "普安县融媒体中心",
        "published_at": "2026-07-15",
        "accessed_at": "2026-07-23",
        "source_type": "official",
        "reliability": "high",
        "notes": "受县委书记黄其兴委托，郭媛媛主持；列出戴松、蔡洪斌、江洪涛、陈玉祥等",
    },
    {
        "id": "S004",
        "title": "普安县人民政府 — 政务要闻《普安县第十八届人大常委会第四十次会议召开》",
        "url": "https://www.puan.gov.cn/xwfb/payw/202607/t20260721_90643360.html",
        "publisher": "普安县融媒体中心",
        "published_at": "2026-07-21",
        "accessed_at": "2026-07-23",
        "source_type": "official",
        "reliability": "high",
        "notes": "戴松、陈太阳、李国奉、黄玉能、董艳均、周灿、张钧；任命王国元为副县长",
    },
]


def make_person_json(p, timeline, relationships_list, custom_identity=None, custom_status=None):
    """Create a person graph JSON following the schema."""
    is_top = ("书记" in p.get("current_post", "") and "副" not in p.get("current_post", "") and "纪委" not in p.get("current_post", "")) or \
             ("县长" in p.get("current_post", "") and "副" not in p.get("current_post", "") and "人大" not in p.get("current_post", "") and "政协" not in p.get("current_post", ""))
    rank = "县处级正职" if is_top else "县处级副职"

    result = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": PROVINCE,
            "city": PARENT_CITY,
            "region": SLUG,
            "job": p.get("current_post", ""),
            "task_id": TASK_ID,
            "time_focus": "2026年7月"
        },
        "identity": {
            "person_id": f"puan_{p['name']}",
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": "",
            "education": [
                {
                    "period": "",
                    "institution": "",
                    "major": "",
                    "degree": p.get("education", ""),
                    "study_type": "unknown",
                    "source_ids": ["S001"]
                }
            ] if p.get("education") else [],
            "party_join": p.get("party_join", ""),
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p.get('birth', '')}",
                "name_birthplace": f"{p['name']}_{p.get('birthplace', '')}",
                "official_profile_url": "https://www.puan.gov.cn/zwgk/ldzc/"
            }
        },
        "current_status": {
            "current_post": p.get("current_post", ""),
            "current_org": p.get("current_org", ""),
            "administrative_rank": rank,
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001", "S002", "S003"]
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": relationships_list,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "截至2026年7月未发现该人物相关的纪律处分或负面舆情",
             "date": "", "confidence": "confirmed", "source_ids": []}
        ],
        "source_register": SOURCE_REGISTER,
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "thin",
            "relationship_confidence": "high",
            "biggest_gap": f"{p['name']}的完整职业生涯履历缺失"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{p['name']}的出生年月、民族、出生地、教育背景详情",
                "why_it_matters": "核心身份信息完整性",
                "suggested_queries": [f"{p['name']} 简历 普安"],
                "last_attempted": AS_OF
            },
            {
                "priority": "critical",
                "question": f"{p['name']}何时被任命为现任职务？此前担任什么职务？",
                "why_it_matters": "职业轨迹和晋升路径",
                "suggested_queries": [f"{p['name']} 任免 {SLUG}"],
                "last_attempted": AS_OF
            },
        ]
    }
    if custom_identity:
        result["identity"].update(custom_identity)
    if custom_status:
        result["current_status"].update(custom_status)
    return result


def write_person_json(filename, data):
    path = TMP_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {path}")


# ═══════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════

run_build(
    slug=SLUG,
    persons=PERSONS,
    organizations=ORGANIZATIONS,
    positions=POSITIONS,
    relationships=RELATIONSHIPS,
    db_path=DB_PATH,
    gexf_path=GEXF_PATH,
    overwrite=True,
)

print(f"Done: {DB_PATH}, {GEXF_PATH}")

# ═══════════════════════════════════════════════════
# PERSON JSONS
# ═══════════════════════════════════════════════════

# ── 黄其兴 (县委书记) ──
hqx_timeline = [
    {"start": "", "end": "present", "org": "中共普安县委员会", "title": "普安县委书记",
     "level": "正县级", "location": "贵州省黔西南州普安县", "system": "party",
     "rank": "正县级", "is_key_promotion": True,
     "notes": "目前在任，具体任命时间未知", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
    {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
     "notes": "公开资料未找到黄其兴任普安县委书记前的完整履历",
     "confidence": "unverified", "source_ids": []},
]
hqx_relationships = [
    {"person": "郭媛媛", "person_id": "puan_郭媛媛", "relationship_type": "superior_subordinate",
     "strength": "strong",
     "evidence": "黄其兴作为县委书记、郭媛媛作为县长搭班子，多次在新闻报道中并列出现",
     "overlap_org": "中共普安县委员会/普安县人民政府", "overlap_period": "current（截至2026-07）",
     "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
    {"person": "付忠文", "person_id": "puan_付忠文", "relationship_type": "superior_subordinate",
     "strength": "medium",
     "evidence": "县委—政府常务副县长",
     "overlap_org": "中共普安县委员会", "overlap_period": "current（截至2026-07）",
     "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]},
    {"person": "江洪涛", "person_id": "", "relationship_type": "superior_subordinate",
     "strength": "medium",
     "evidence": "县委正副书记",
     "overlap_org": "中共普安县委员会", "overlap_period": "current（截至2026-07）",
     "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S003"]},
    {"person": "戴松", "person_id": "", "relationship_type": "overlap",
     "strength": "medium",
     "evidence": "县委—人大班子共事",
     "overlap_org": "普安县四大班子", "overlap_period": "current（截至2026-07）",
     "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]},
    {"person": "蔡洪斌", "person_id": "", "relationship_type": "overlap",
     "strength": "medium",
     "evidence": "县委—政协班子共事",
     "overlap_org": "普安县四大班子", "overlap_period": "current（截至2026-07）",
     "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]},
]
hqx_json = make_person_json(PERSONS[0], hqx_timeline, hqx_relationships)
write_person_json(f"{AS_OF_SHORT}-贵州省-黔西南布依族苗族自治州-县委书记-黄其兴.json", hqx_json)

# ── 郭媛媛 (县长) ──
gyy_timeline = [
    {"start": "", "end": "present", "org": "普安县人民政府", "title": "普安县委副书记、县长",
     "level": "正县级", "location": "贵州省黔西南州普安县", "system": "government",
     "rank": "正县级", "is_key_promotion": True,
     "notes": "目前在任，主持县政府全面工作", "confidence": "confirmed", "source_ids": ["S001", "S002", "S003"]},
    {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
     "notes": "公开资料未找到郭媛媛任普安县长前的完整履历",
     "confidence": "unverified", "source_ids": []},
]
gyy_relationships = [
    {"person": "黄其兴", "person_id": "puan_黄其兴", "relationship_type": "superior_subordinate",
     "strength": "strong",
     "evidence": "郭媛媛作为县长、黄其兴作为县委书记搭班子",
     "overlap_org": "中共普安县委员会/普安县人民政府", "overlap_period": "current（截至2026-07）",
     "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
    {"person": "付忠文", "person_id": "puan_付忠文", "relationship_type": "superior_subordinate",
     "strength": "strong",
     "evidence": "县长—常务副县长，付忠文协助郭媛媛分管财政、审计",
     "overlap_org": "普安县人民政府", "overlap_period": "current（截至2026-07）",
     "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S001"]},
    {"person": "戴松", "person_id": "", "relationship_type": "overlap",
     "strength": "medium",
     "evidence": "政府—人大班子共事",
     "overlap_org": "普安县四大班子", "overlap_period": "current（截至2026-07）",
     "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]},
]
gyy_json = make_person_json(PERSONS[1], gyy_timeline, gyy_relationships)
write_person_json(f"{AS_OF_SHORT}-贵州省-黔西南布依族苗族自治州-县长-郭媛媛.json", gyy_json)

print("All person JSONs written.")
