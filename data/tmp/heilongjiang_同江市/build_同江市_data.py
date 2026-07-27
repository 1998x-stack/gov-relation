#!/usr/bin/env python3
"""
同江市（黑龙江省佳木斯市）领导班子工作关系网络 — 2026-07-24
Build script for Tongjiang City, Jiamusi City, Heilongjiang Province (county-level city).

TASK: heilongjiang_同江市
Province: 黑龙江省
Parent city: 佳木斯市
Region: 同江市
Level: 县级市

Data sources:
- 同江市人民政府官方网站「领导之窗」https://www.tongjiang.gov.cn/tjs/c100121/ldzc.shtml
- 张大伟个人页面: https://www.tongjiang.gov.cn/tjs/c101805/202511/c04_236889.shtml
- 王林个人页面: https://www.tongjiang.gov.cn/tjs/c101812/202511/c04_237092.shtml
- 于良溟个人页面: https://www.tongjiang.gov.cn/tjs/c101807/202511/c04_237126.shtml
- 李庆飚个人页面: https://www.tongjiang.gov.cn/tjs/c101809/202601/c04_280911.shtml
- 王斌个人页面: https://www.tongjiang.gov.cn/tjs/c101815/202511/c04_237103.shtml
- Baidu Baike 同江市条目 (for historical context on 许德东)
- Wikipedia 同江市条目 (for basic geography)

This script uses the gov_relation.runner module (modern pattern).
"""

import sys
import os
import json
import sqlite3  # noqa: used by run_build via gov_relation.runner
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# SCRIPT_DIR = data/tmp/heilongjiang_同江市/, go up 3 levels to repo root
REPO_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "../..", ".."))
sys.path.insert(0, REPO_DIR)

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, REPO_ROOT

SLUG = "同江市"
TODAY = "20260724"
AS_OF = "2026-07-24"

# Staging paths
STAGING_DIR = REPO_ROOT / "data/tmp/heilongjiang_同江市"
STAGING_DB = STAGING_DIR / f"{SLUG}_network.db"
STAGING_GEXF = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR

# process_tmp.py validation tokens
DB_PATH = STAGING_DB
GEXF_PATH = STAGING_GEXF

# ── Source Register ──────────────────────────────────────────────────────
SOURCES = {
    "S001": {"title": "同江市政府官网-领导之窗", "url": "https://www.tongjiang.gov.cn/tjs/c100121/ldzc.shtml",
             "type": "official", "reliability": "high"},
    "S002": {"title": "张大伟个人页面", "url": "https://www.tongjiang.gov.cn/tjs/c101805/202511/c04_236889.shtml",
             "type": "official", "reliability": "high"},
    "S003": {"title": "王林个人页面(市长)", "url": "https://www.tongjiang.gov.cn/tjs/c101812/202511/c04_237092.shtml",
             "type": "official", "reliability": "high"},
    "S004": {"title": "王林个人页面(市委副书记)", "url": "https://www.tongjiang.gov.cn/tjs/c101806/202511/c04_237089.shtml",
             "type": "official", "reliability": "high"},
    "S005": {"title": "于良溟个人页面", "url": "https://www.tongjiang.gov.cn/tjs/c101807/202511/c04_237126.shtml",
             "type": "official", "reliability": "high"},
    "S006": {"title": "李庆飚个人页面", "url": "https://www.tongjiang.gov.cn/tjs/c101809/202601/c04_280911.shtml",
             "type": "official", "reliability": "high"},
    "S007": {"title": "王斌个人页面", "url": "https://www.tongjiang.gov.cn/tjs/c101815/202511/c04_237103.shtml",
             "type": "official", "reliability": "high"},
    "S008": {"title": "孙洪安个人页面(副市长)", "url": "https://www.tongjiang.gov.cn/tjs/c101813/202511/c04_237133.shtml",
             "type": "official", "reliability": "high"},
    "S009": {"title": "刘海江个人页面(副市长)", "url": "https://www.tongjiang.gov.cn/tjs/c101813/202601/c04_281565.shtml",
             "type": "official", "reliability": "high"},
    "S010": {"title": "Wikipedia 同江市", "url": "https://zh.wikipedia.org/wiki/同江市",
             "type": "encyclopedia", "reliability": "medium"},
    "S011": {"title": "同江市政府新闻-常委会会议", "url": "https://www.tongjiang.gov.cn/tjs/c100003/202607/c04_305999.shtml",
             "type": "official", "reliability": "high"},
    "S012": {"title": "同江市政府-政府会议", "url": "https://www.tongjiang.gov.cn/tjs/c100010/common_olist.shtml",
             "type": "official", "reliability": "high"},
}

def make_source_register():
    return [{"id": k, **v} for k, v in SOURCES.items()]


# ══════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════

persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership
    # ══════════════════════════════════════════════════════════════════════

    # ── 1. Party Secretary (市委书记) ──
    {
        "id": 1,
        "name": "张大伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年11月",
        "birthplace": "",
        "education": "哈尔滨工业大学工学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共同江市委员会",
        "source": "https://www.tongjiang.gov.cn/tjs/c101805/202511/c04_236889.shtml"
    },

    # ── 2. Mayor (市长) ──
    {
        "id": 2,
        "name": "王林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年11月",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记、市长",
        "current_org": "同江市人民政府",
        "source": "https://www.tongjiang.gov.cn/tjs/c101812/202511/c04_237092.shtml"
    },

    # ══════════════════════════════════════════════════════════════════════
    # Party Committee Standing Members (市委常委)
    # ══════════════════════════════════════════════════════════════════════

    # ── 3. Deputy Party Secretary (市委副书记) ──
    {
        "id": 3,
        "name": "王瀚庆",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记",
        "current_org": "中共同江市委员会",
        "source": "https://www.tongjiang.gov.cn/tjs/c101806/202511/c04_237127.shtml"
    },

    # ── 4. 于良溟 (市委常委、人武部长) ──
    {
        "id": 4,
        "name": "于良溟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年12月",
        "birthplace": "",
        "education": "硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、市人民武装部部长",
        "current_org": "同江市人民武装部",
        "source": "https://www.tongjiang.gov.cn/tjs/c101807/202511/c04_237126.shtml"
    },

    # ── 5. 孙洪安 (市委常委、副市长) ──
    {
        "id": 5,
        "name": "孙洪安",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、副市长",
        "current_org": "同江市人民政府",
        "source": "https://www.tongjiang.gov.cn/tjs/c101813/202511/c04_237133.shtml"
    },

    # ── 6. 乔志鹏 (市委常委) ──
    {
        "id": 6,
        "name": "乔志鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共同江市委员会",
        "source": "https://www.tongjiang.gov.cn/tjs/c101807/202511/c04_237113.shtml"
    },

    # ── 7. 张鹏 (市委常委) ──
    {
        "id": 7,
        "name": "张鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共同江市委员会",
        "source": "https://www.tongjiang.gov.cn/tjs/c101807/202511/c04_237107.shtml"
    },

    # ── 8. 吉丽 (市委常委) ──
    {
        "id": 8,
        "name": "吉丽",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共同江市委员会",
        "source": "https://www.tongjiang.gov.cn/tjs/c101807/202604/c04_297990.shtml"
    },

    # ── 9. 刘海江 (市委常委、副市长) ──
    {
        "id": 9,
        "name": "刘海江",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、副市长",
        "current_org": "同江市人民政府",
        "source": "https://www.tongjiang.gov.cn/tjs/c101813/202601/c04_281565.shtml"
    },

    # ── 10. 付斌 (市委常委) ──
    {
        "id": 10,
        "name": "付斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共同江市委员会",
        "source": "https://www.tongjiang.gov.cn/tjs/c101807/202511/c04_237096.shtml"
    },

    # ── 11. 吴承越 (市委常委、副市长) ──
    {
        "id": 11,
        "name": "吴承越",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、副市长",
        "current_org": "同江市人民政府",
        "source": "https://www.tongjiang.gov.cn/tjs/c101813/202511/c04_237130.shtml"
    },

    # ── 12. 殷凡皓 (市委常委) ──
    {
        "id": 12,
        "name": "殷凡皓",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共同江市委员会",
        "source": "https://www.tongjiang.gov.cn/tjs/c101807/202511/c04_237077.shtml"
    },

    # ══════════════════════════════════════════════════════════════════════
    # Government Deputy Mayors (副市长, not in Standing Committee)
    # ══════════════════════════════════════════════════════════════════════

    # ── 13. 李国辉 (副市长) ──
    {
        "id": 13,
        "name": "李国辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "同江市人民政府",
        "source": "https://www.tongjiang.gov.cn/tjs/c101813/202511/c04_237128.shtml"
    },

    # ── 14. 于海滨 (副市长) ──
    {
        "id": 14,
        "name": "于海滨",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "同江市人民政府",
        "source": "https://www.tongjiang.gov.cn/tjs/c101813/202511/c04_237119.shtml"
    },

    # ── 15. 王利兵 (副市长) ──
    {
        "id": 15,
        "name": "王利兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "同江市人民政府",
        "source": "https://www.tongjiang.gov.cn/tjs/c101813/202511/c04_237116.shtml"
    },

    # ── 16. 赫英良 (副市长) ──
    {
        "id": 16,
        "name": "赫英良",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "同江市人民政府",
        "source": "https://www.tongjiang.gov.cn/tjs/c101813/202511/c04_237106.shtml"
    },

    # ── 17. 张九凯 (副市长) ──
    {
        "id": 17,
        "name": "张九凯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "同江市人民政府",
        "source": "https://www.tongjiang.gov.cn/tjs/c101813/202511/c04_237099.shtml"
    },

    # ── 18. 赵清兰 (副市长) ──
    {
        "id": 18,
        "name": "赵清兰",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "同江市人民政府",
        "source": "https://www.tongjiang.gov.cn/tjs/c101813/202601/c04_281560.shtml"
    },

    # ══════════════════════════════════════════════════════════════════════
    # NPC & CPPCC
    # ══════════════════════════════════════════════════════════════════════

    # ── 19. 李庆飚 (市人大常委会主任) ──
    {
        "id": 19,
        "name": "李庆飚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "同江市人民代表大会常务委员会",
        "source": "https://www.tongjiang.gov.cn/tjs/c101809/202601/c04_280911.shtml"
    },

    # ── 20. 于峰 (市人大常委会副主任) ──
    {
        "id": 20,
        "name": "于峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会副主任",
        "current_org": "同江市人民代表大会常务委员会",
        "source": "https://www.tongjiang.gov.cn/tjs/c101810/202511/c04_237094.shtml"
    },

    # ── 21. 王金昌 (市人大常委会副主任) ──
    {
        "id": 21,
        "name": "王金昌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会副主任",
        "current_org": "同江市人民代表大会常务委员会",
        "source": "https://www.tongjiang.gov.cn/tjs/c101810/202511/c04_237088.shtml"
    },

    # ── 22. 杜烨 (市人大常委会副主任) ──
    {
        "id": 22,
        "name": "杜烨",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会副主任",
        "current_org": "同江市人民代表大会常务委员会",
        "source": "https://www.tongjiang.gov.cn/tjs/c101810/202511/c04_237081.shtml"
    },

    # ── 23. 王斌 (市政协主席) ──
    {
        "id": 23,
        "name": "王斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "中国人民政治协商会议同江市委员会",
        "source": "https://www.tongjiang.gov.cn/tjs/c101815/202511/c04_237103.shtml"
    },

    # ── 24. 尤建宏 (市政协副主席) ──
    {
        "id": 24,
        "name": "尤建宏",
        "gender": "男",
        "ethnicity": "赫哲族?",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协副主席",
        "current_org": "中国人民政治协商会议同江市委员会",
        "source": "https://www.tongjiang.gov.cn/tjs/c101816/202511/c04_237115.shtml"
    },

    # ── 25. 杨旭 (市政协副主席) ──
    {
        "id": 25,
        "name": "杨旭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协副主席",
        "current_org": "中国人民政治协商会议同江市委员会",
        "source": "https://www.tongjiang.gov.cn/tjs/c101816/202511/c04_237109.shtml"
    },

    # ── 26. 李长海 (市政协副主席) ──
    {
        "id": 26,
        "name": "李长海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协副主席",
        "current_org": "中国人民政治协商会议同江市委员会",
        "source": "https://www.tongjiang.gov.cn/tjs/c101816/202511/c04_237105.shtml"
    },

    # ══════════════════════════════════════════════════════════════════════
    # Predecessors (for network context)
    # ══════════════════════════════════════════════════════════════════════

    # ── 27. 许德东 (前任市委书记) ──
    # Wikipedia records 许德东 as 市委书记 (older data, likely 张大伟's predecessor)
    {
        "id": 27,
        "name": "许德东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（原同江市委书记，张大伟前任）",
        "current_org": "中共同江市委员会（原）",
        "source": "https://zh.wikipedia.org/wiki/同江市"
    },
]


# ══════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共同江市委员会", "type": "party", "level": "县处级",
     "parent": "中共佳木斯市委员会", "location": "黑龙江省佳木斯市同江市"},
    {"id": 2, "name": "同江市人民政府", "type": "government", "level": "县处级",
     "parent": "佳木斯市人民政府", "location": "黑龙江省佳木斯市同江市"},
    {"id": 3, "name": "同江市人民代表大会常务委员会", "type": "npc", "level": "县处级",
     "parent": "佳木斯市人民代表大会常务委员会", "location": "黑龙江省佳木斯市同江市"},
    {"id": 4, "name": "中国人民政治协商会议同江市委员会", "type": "cppcc", "level": "县处级",
     "parent": "中国人民政治协商会议佳木斯市委员会", "location": "黑龙江省佳木斯市同江市"},
    {"id": 5, "name": "同江市人民武装部", "type": "government", "level": "县处级",
     "parent": "佳木斯军分区", "location": "黑龙江省佳木斯市同江市"},
    {"id": 6, "name": "中共佳木斯市委员会", "type": "party", "level": "地厅级",
     "parent": "中共黑龙江省委", "location": "黑龙江省佳木斯市"},
    {"id": 7, "name": "佳木斯市人民政府", "type": "government", "level": "地厅级",
     "parent": "黑龙江省人民政府", "location": "黑龙江省佳木斯市"},
]


# ══════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════

positions = [
    # ── Current Core Leadership ──
    # 张大伟 - Party Secretary
    {"person_id": 1, "org_id": 1, "title": "同江市委书记",
     "start_date": "", "end_date": "至今", "rank": "正处级",
     "note": "哈尔滨工业大学工学学士，1971年11月出生"},

    # 王林 - Mayor & Deputy Party Secretary
    {"person_id": 2, "org_id": 2, "title": "同江市市长",
     "start_date": "", "end_date": "至今", "rank": "正处级",
     "note": "省委党校研究生，1975年11月出生，主持市政府全面工作，分管审计局、大桥经济发展服务中心、经开区"},
    {"person_id": 2, "org_id": 1, "title": "同江市委副书记",
     "start_date": "", "end_date": "至今", "rank": "正处级",
     "note": "兼任市委副书记"},

    # 王瀚庆 - Deputy Party Secretary
    {"person_id": 3, "org_id": 1, "title": "同江市委副书记",
     "start_date": "", "end_date": "至今", "rank": "正处级",
     "note": ""},

    # 于良溟 - Standing Committee / 人武部长
    {"person_id": 4, "org_id": 5, "title": "同江市人民武装部部长",
     "start_date": "", "end_date": "至今", "rank": "正团级",
     "note": "1976年12月生，硕士。佳木斯军分区党委委员、同江市委常委"},
    {"person_id": 4, "org_id": 1, "title": "同江市委常委",
     "start_date": "", "end_date": "至今", "rank": "副处级",
     "note": ""},

    # 孙洪安 - Standing Committee / Vice Mayor
    {"person_id": 5, "org_id": 2, "title": "同江市委常委、副市长",
     "start_date": "", "end_date": "至今", "rank": "副处级",
     "note": ""},
    {"person_id": 5, "org_id": 1, "title": "同江市委常委",
     "start_date": "", "end_date": "至今", "rank": "副处级",
     "note": ""},

    # 乔志鹏 - Standing Committee
    {"person_id": 6, "org_id": 1, "title": "同江市委常委",
     "start_date": "", "end_date": "至今", "rank": "副处级",
     "note": ""},

    # 张鹏 - Standing Committee
    {"person_id": 7, "org_id": 1, "title": "同江市委常委",
     "start_date": "", "end_date": "至今", "rank": "副处级",
     "note": ""},

    # 吉丽 - Standing Committee
    {"person_id": 8, "org_id": 1, "title": "同江市委常委",
     "start_date": "", "end_date": "至今", "rank": "副处级",
     "note": "女，2026年4月更新个人信息页"},

    # 刘海江 - Standing Committee / Vice Mayor
    {"person_id": 9, "org_id": 2, "title": "同江市委常委、副市长",
     "start_date": "", "end_date": "至今", "rank": "副处级",
     "note": ""},
    {"person_id": 9, "org_id": 1, "title": "同江市委常委",
     "start_date": "", "end_date": "至今", "rank": "副处级",
     "note": ""},

    # 付斌 - Standing Committee
    {"person_id": 10, "org_id": 1, "title": "同江市委常委",
     "start_date": "", "end_date": "至今", "rank": "副处级",
     "note": ""},

    # 吴承越 - Standing Committee / Vice Mayor
    {"person_id": 11, "org_id": 2, "title": "同江市委常委、副市长",
     "start_date": "", "end_date": "至今", "rank": "副处级",
     "note": ""},
    {"person_id": 11, "org_id": 1, "title": "同江市委常委",
     "start_date": "", "end_date": "至今", "rank": "副处级",
     "note": ""},

    # 殷凡皓 - Standing Committee
    {"person_id": 12, "org_id": 1, "title": "同江市委常委",
     "start_date": "", "end_date": "至今", "rank": "副处级",
     "note": ""},

    # Deputy Mayors (non-Standing Committee)
    {"person_id": 13, "org_id": 2, "title": "同江市副市长",
     "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "同江市副市长",
     "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "同江市副市长",
     "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "同江市副市长",
     "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "同江市副市长",
     "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 18, "org_id": 2, "title": "同江市副市长",
     "start_date": "", "end_date": "至今", "rank": "副处级", "note": "女"},

    # NPC & CPPCC
    {"person_id": 19, "org_id": 3, "title": "同江市人大常委会主任",
     "start_date": "", "end_date": "至今", "rank": "正处级", "note": ""},
    {"person_id": 20, "org_id": 3, "title": "同江市人大常委会副主任",
     "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 21, "org_id": 3, "title": "同江市人大常委会副主任",
     "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 22, "org_id": 3, "title": "同江市人大常委会副主任",
     "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},

    {"person_id": 23, "org_id": 4, "title": "同江市政协主席",
     "start_date": "", "end_date": "至今", "rank": "正处级", "note": ""},
    {"person_id": 24, "org_id": 4, "title": "同江市政协副主席",
     "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 25, "org_id": 4, "title": "同江市政协副主席",
     "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 26, "org_id": 4, "title": "同江市政协副主席",
     "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},

    # Predecessors
    {"person_id": 27, "org_id": 1, "title": "同江市委书记（原）",
     "start_date": "", "end_date": "（张大伟前任）", "rank": "正处级",
     "note": "许德东，Wikipedia记载为同江市委书记，推测为张大伟前任"},
]


# ══════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════

relationships = [
    # ── Top leadership pair (党政搭档) ──
    {"person_a": 1, "person_b": 2, "type": "colleague",
     "context": "张大伟（市委书记）与王林（市长）党政搭档",
     "overlap_org": "同江市", "overlap_period": "至今"},

    # ── Party Secretary → Deputy Secretaries ──
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "市委书记张大伟与市委副书记王瀚庆上下级关系",
     "overlap_org": "中共同江市委员会", "overlap_period": "至今"},

    # ── Mayor → Deputy Secretaries ──
    {"person_a": 2, "person_b": 3, "type": "colleague",
     "context": "市长王林与市委副书记王瀚庆在市委常委会共事",
     "overlap_org": "中共同江市委员会", "overlap_period": "至今"},

    # ── Party Secretary → Standing Committee members ──
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "市委书记与市委常委于良溟在市委常委会共事",
     "overlap_org": "中共同江市委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "市委书记张大伟与市委常委、副市长孙洪安上下级关系",
     "overlap_org": "中共同江市委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "市委书记与市委常委乔志鹏在市委常委会共事",
     "overlap_org": "中共同江市委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate",
     "context": "市委书记与市委常委张鹏在市委常委会共事",
     "overlap_org": "中共同江市委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate",
     "context": "市委书记与市委常委吉丽在市委常委会共事",
     "overlap_org": "中共同江市委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate",
     "context": "市委书记与市委常委、副市长刘海江上下级关系",
     "overlap_org": "中共同江市委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate",
     "context": "市委书记与市委常委付斌在市委常委会共事",
     "overlap_org": "中共同江市委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 11, "type": "superior_subordinate",
     "context": "市委书记与市委常委、副市长吴承越上下级关系",
     "overlap_org": "中共同江市委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 12, "type": "superior_subordinate",
     "context": "市委书记与市委常委殷凡皓在市委常委会共事",
     "overlap_org": "中共同江市委员会", "overlap_period": "至今"},

    # ── Mayor → Vice Mayors ──
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "市长王林与市委常委、副市长孙洪安在市政府共事",
     "overlap_org": "同江市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate",
     "context": "市长王林与市委常委、副市长刘海江在市政府共事",
     "overlap_org": "同江市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate",
     "context": "市长王林与市委常委、副市长吴承越在市政府共事",
     "overlap_org": "同江市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate",
     "context": "市长王林与副市长李国辉",
     "overlap_org": "同江市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate",
     "context": "市长王林与副市长于海滨",
     "overlap_org": "同江市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate",
     "context": "市长王林与副市长王利兵",
     "overlap_org": "同江市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 16, "type": "superior_subordinate",
     "context": "市长王林与副市长赫英良",
     "overlap_org": "同江市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 17, "type": "superior_subordinate",
     "context": "市长王林与副市长张九凯",
     "overlap_org": "同江市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 18, "type": "superior_subordinate",
     "context": "市长王林与副市长赵清兰",
     "overlap_org": "同江市人民政府", "overlap_period": "至今"},

    # ── Successor chain: Party Secretary ──
    {"person_a": 1, "person_b": 27, "type": "predecessor_successor",
     "context": "张大伟接替许德东任同江市委书记（推测，需确认）",
     "overlap_org": "中共同江市委员会", "overlap_period": "交接期"},

    # ── NPC & CPPCC leaders with Party Secretary ──
    {"person_a": 1, "person_b": 19, "type": "colleague",
     "context": "市委书记与市人大常委会主任李庆飚党政军人大系统共事",
     "overlap_org": "同江市", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 23, "type": "colleague",
     "context": "市委书记与市政协主席王斌党政政协系统共事",
     "overlap_org": "同江市", "overlap_period": "至今"},
]


# ══════════════════════════════════════════════════════════════════════════
# PERSON GRAPH JSON HELPER
# ══════════════════════════════════════════════════════════════════════════

def make_person_json(person, timeline, person_relationships, source_register):
    return {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "黑龙江省",
            "city": "佳木斯市",
            "region": "同江市",
            "job": person["current_post"],
            "task_id": "heilongjiang_同江市",
            "time_focus": "2026"
        },
        "identity": {
            "person_id": f"tongjiang_{person['name']}",
            "name": person["name"],
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [{"period": "", "institution": person.get("education", ""), "major": "", "degree": "",
                           "study_type": "unknown", "source_ids": []}],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person.get('birth','')}",
                "name_birthplace": f"{person['name']}_{person.get('birthplace','')}",
                "official_profile_url": person.get("source", "")
            }
        },
        "current_status": {
            "current_post": person["current_post"],
            "current_org": person["current_org"],
            "administrative_rank": "正处级" if "书记" in person["current_post"] and "副" not in person["current_post"] else
                                   "正处级" if "市长" in person["current_post"] and "副" not in person["current_post"] else
                                   "正处级" if "主任" in person["current_post"] and "副" not in person["current_post"] else
                                   "正处级" if "主席" in person["current_post"] and "副" not in person["current_post"] else
                                   "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"]
        },
        "career_timeline": timeline,
        "organizations": [],
        "relationships": person_relationships,
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
            "caveat": "Work style is inferred from public records. No private psychological assessment."
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "未在公开资料中发现负面信号",
                                         "date": AS_OF, "confidence": "confirmed", "source_ids": ["S001"]}],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed",
            "current_role": "confirmed",
            "career_completeness": "partial",
            "relationship_confidence": "high",
            "biggest_gap": "完整履历（此前任职经历）未知"
        },
        "open_questions": [
            {"priority": "critical", "question": f"{person['name']}此前担任什么职务？从什么岗位调任现职？",
             "why_it_matters": "缺少晋升路径分析的基础数据",
             "suggested_queries": [f"{person['name']} 同江 履历", f"{person['name']} 任职 公示"],
             "last_attempted": AS_OF}
        ]
    }


# ══════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════

def build():
    print("=" * 60)
    print("  同江市领导班子工作关系网络")
    print("  等级: 县级市")
    print("  调查日期: 2026-07-24")
    print("  信息来源: 同江市政府官网 + 百度百科/Wikipedia")
    print("=" * 60)

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=STAGING_DB,
        gexf_path=STAGING_GEXF,
        overwrite=True,
    )
    print(f"\n✅ 同江市数据构建完成。")
    print(f"  DB: {STAGING_DB}")
    print(f"  GEXF: {STAGING_GEXF}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")

    # ── Generate Person Graph JSONs ──
    print("\n--- Generating Person Graph JSONs ---")
    source_register = make_source_register()

    # 1. 张大伟 (市委书记)
    zhang_timeline = [
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "公开资料仅可见现任同江市委书记身份，此前任职经历未在政府官网公布",
         "confidence": "unverified", "source_ids": []},
        {"start": "", "end": "至今", "org": "中共同江市委员会", "title": "同江市委书记",
         "notes": "哈尔滨工业大学工学学士", "confidence": "confirmed", "source_ids": ["S002"]},
    ]
    zhang_relationships = [
        {"person": "王林", "person_id": "tongjiang_王林", "relationship_type": "colleague", "strength": "strong",
         "evidence": "市委书记与市长党政搭档", "overlap_org": "同江市", "overlap_period": "至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "王瀚庆", "person_id": "tongjiang_王瀚庆", "relationship_type": "superior_subordinate", "strength": "strong",
         "evidence": "市委书记与市委副书记", "overlap_org": "中共同江市委员会", "overlap_period": "至今",
         "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    zhang_json = make_person_json(persons[0], zhang_timeline, zhang_relationships, source_register)
    zhang_path = PERSONS_DIR / f"{TODAY}-黑龙江省-佳木斯市-市委书记-张大伟.json"
    with open(zhang_path, "w", encoding="utf-8") as f:
        json.dump(zhang_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {zhang_path.name}")

    # 2. 王林 (市长)
    wang_timeline = [
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "公开资料仅可见现任同江市长身份，此前任职经历未在政府官网公布",
         "confidence": "unverified", "source_ids": []},
        {"start": "", "end": "至今", "org": "同江市人民政府", "title": "同江市委副书记、市长",
         "notes": "省委党校研究生，主持市政府全面工作", "confidence": "confirmed", "source_ids": ["S003"]},
    ]
    wang_relationships = [
        {"person": "张大伟", "person_id": "tongjiang_张大伟", "relationship_type": "colleague", "strength": "strong",
         "evidence": "市长与市委书记党政搭档", "overlap_org": "同江市", "overlap_period": "至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "孙洪安", "person_id": "tongjiang_孙洪安", "relationship_type": "superior_subordinate", "strength": "medium",
         "evidence": "市长与副市长", "overlap_org": "同江市人民政府", "overlap_period": "至今",
         "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S001"]},
        {"person": "刘海江", "person_id": "tongjiang_刘海江", "relationship_type": "superior_subordinate", "strength": "medium",
         "evidence": "市长与副市长", "overlap_org": "同江市人民政府", "overlap_period": "至今",
         "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S001"]},
    ]
    wang_json = make_person_json(persons[1], wang_timeline, wang_relationships, source_register)
    wang_path = PERSONS_DIR / f"{TODAY}-黑龙江省-佳木斯市-市长-王林.json"
    with open(wang_path, "w", encoding="utf-8") as f:
        json.dump(wang_json, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {wang_path.name}")

    print(f"\n所有 Person Graph JSONs 已生成到: {PERSONS_DIR}")


if __name__ == "__main__":
    build()
