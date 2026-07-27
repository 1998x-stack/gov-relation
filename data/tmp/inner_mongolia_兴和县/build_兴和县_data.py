#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 兴和县 leadership network.

兴和县 (Xinghe County) is under 乌兰察布市 (Ulanqab City), 内蒙古自治区.

Data sources:
- 兴和县人民政府官网 (www.xinghe.gov.cn) 领导之窗 pages, accessed 2026-07-25
- 兴和县政府常务会议新闻报道

As-of date: 2026-07-25
"""

import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, BASE)

import sqlite3
from gov_relation.runner import run_build
from datetime import datetime

# Tokens for process_tmp.py validation
DB_PATH = ""
GEXF_PATH = ""

AS_OF = "2026-07-25"
SLUG = "兴和县"

# ── PERSONS ──────────────────────────────────────────────────────────

persons = [
    # ===== 县委领导 =====
    # 1. 县委书记
    {
        "id": 1,
        "name": "郭翔宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-11",
        "birthplace": "",
        "education": "中央党校研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "兴和县委书记",
        "current_org": "中共兴和县委员会",
        "source": "https://www.xinghe.gov.cn/swld/1973197.html",
    },
    # 2. 代县长
    {
        "id": 2,
        "name": "张雪春",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-01",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "兴和县委副书记、政府代理县长",
        "current_org": "兴和县人民政府",
        "source": "https://www.xinghe.gov.cn/swld/1981827.html",
    },
    # 3. 县委副书记、政法委书记
    {
        "id": 3,
        "name": "王学东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-08",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记、政法委书记",
        "current_org": "中共兴和县委员会政法委员会",
        "source": "https://www.xinghe.gov.cn/swld/1981819.html",
    },
    # 4. 县委常委、组织部长
    {
        "id": 4,
        "name": "周瑞君",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-07",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、组织部长",
        "current_org": "中共兴和县委组织部",
        "source": "https://www.xinghe.gov.cn/swld/1601955.html",
    },
    # 5. 县委常委、政府副县长（常务）
    {
        "id": 5,
        "name": "王建伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985-07",
        "birthplace": "",
        "education": "大学本科，管理学学士",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、政府副县长（负责政府常务工作）",
        "current_org": "兴和县人民政府",
        "source": "https://www.xinghe.gov.cn/swld/1740781.html",
    },
    # 6. 县委常委、纪委书记、监委主任候选人
    {
        "id": 6,
        "name": "董俊辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984-05",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "2015-06",
        "work_start": "2011-07",
        "current_post": "县委常委、纪委书记、监委主任候选人",
        "current_org": "中共兴和县纪律检查委员会",
        "source": "https://www.xinghe.gov.cn/swld/1988017.html",
    },
    # 7. 县委常委、政府副县长人选
    {
        "id": 7,
        "name": "陈国华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986-03",
        "birthplace": "",
        "education": "硕士研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、政府副县长人选",
        "current_org": "兴和县人民政府",
        "source": "https://www.xinghe.gov.cn/swld/1982299.html",
    },
    # 8. 县委常委、办公室主任
    {
        "id": 8,
        "name": "窦玉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1990-02",
        "birthplace": "",
        "education": "研究生学历，文学学士",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、办公室主任",
        "current_org": "中共兴和县委办公室",
        "source": "https://www.xinghe.gov.cn/swld/1812487.html",
    },
    # 9. 县委常委、宣传部部长
    {
        "id": 9,
        "name": "苗雨丰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986-10",
        "birthplace": "",
        "education": "湖南工业大学马克思主义中国化研究专业法学硕士研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共兴和县委宣传部",
        "source": "https://www.xinghe.gov.cn/swld/1981851.html",
    },
    # 10. 县委常委、统战部部长
    {
        "id": 10,
        "name": "张晶",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1988-06",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、统战部部长",
        "current_org": "中共兴和县委统战部",
        "source": "https://www.xinghe.gov.cn/swld/1859293.html",
    },

    # ===== 政府领导 =====
    # 11. 副县长、公安局长（已在常委列表中，这里补充）
    {
        "id": 11,
        "name": "孙海军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-06",
        "birthplace": "",
        "education": "大学本科学历",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府副县长、公安局党委书记、局长",
        "current_org": "兴和县公安局",
        "source": "https://www.xinghe.gov.cn/zfld/1601999.html",
    },
    # 12. 副县长
    {
        "id": 12,
        "name": "孙永春",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-03",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府副县长",
        "current_org": "兴和县人民政府",
        "source": "https://www.xinghe.gov.cn/zfld/1786741.html",
    },
    # 13. 副县长
    {
        "id": 13,
        "name": "刘阳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985-08",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府副县长",
        "current_org": "兴和县人民政府",
        "source": "https://www.xinghe.gov.cn/zfld/1601997.html",
    },
    # 14. 副县长人选
    {
        "id": 14,
        "name": "王慧霞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1982-02",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "政府副县长人选",
        "current_org": "兴和县人民政府",
        "source": "https://www.xinghe.gov.cn/zfld/1988027.html",
    },

    # ===== 人大领导 =====
    {
        "id": 15,
        "name": "赵瑞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-07",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会党组书记、主任",
        "current_org": "兴和县人大常委会",
        "source": "https://www.xinghe.gov.cn/zwgk/index.html",
    },
    {
        "id": 16,
        "name": "吉晓辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "兴和县人大常委会",
        "source": "https://www.xinghe.gov.cn/zwgk/index.html",
    },
    {
        "id": 17,
        "name": "乔嵘",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "兴和县人大常委会",
        "source": "https://www.xinghe.gov.cn/zwgk/index.html",
    },
    {
        "id": 18,
        "name": "袁义锦",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "兴和县人大常委会",
        "source": "https://www.xinghe.gov.cn/zwgk/index.html",
    },
    {
        "id": 19,
        "name": "李俊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "兴和县人大常委会",
        "source": "https://www.xinghe.gov.cn/zwgk/index.html",
    },

    # ===== 政协领导 =====
    {
        "id": 20,
        "name": "赵慧菊",
        "gender": "女",
        "ethnicity": "",
        "birth": "1970-10",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "",
        "work_start": "",
        "current_post": "政协主席候选人",
        "current_org": "政协兴和县委员会",
        "source": "https://www.xinghe.gov.cn/zxld/1981823.html",
    },
    {
        "id": 21,
        "name": "杜立新",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协委员会副主席",
        "current_org": "政协兴和县委员会",
        "source": "https://www.xinghe.gov.cn/zwgk/index.html",
    },
    {
        "id": 22,
        "name": "贺海燕",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协委员会副主席",
        "current_org": "政协兴和县委员会",
        "source": "https://www.xinghe.gov.cn/zwgk/index.html",
    },
    {
        "id": 23,
        "name": "魏军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协委员会党组成员、副主席",
        "current_org": "政协兴和县委员会",
        "source": "https://www.xinghe.gov.cn/zwgk/index.html",
    },
    {
        "id": 24,
        "name": "侯志勇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协委员会党组成员、副主席",
        "current_org": "政协兴和县委员会",
        "source": "https://www.xinghe.gov.cn/zwgk/index.html",
    },

    # ===== 前任县长 =====
    {
        "id": 25,
        "name": "李锴栋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前兴和县委副书记、县长（2026年6月前）",
        "current_org": "未知（已离任）",
        "source": "https://www.xinghe.gov.cn/zfcwh/1978201.html",
    },
]

# ── ORGANIZATIONS ──────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共兴和县委员会", "type": "党委", "level": "县处级", "parent": "中共乌兰察布市委员会", "location": "兴和县"},
    {"id": 2, "name": "兴和县人民政府", "type": "政府", "level": "县处级", "parent": "乌兰察布市人民政府", "location": "兴和县"},
    {"id": 3, "name": "中共兴和县委政法委员会", "type": "党委", "level": "县处级", "parent": "中共兴和县委员会", "location": "兴和县"},
    {"id": 4, "name": "中共兴和县委组织部", "type": "党委", "level": "乡科级", "parent": "中共兴和县委员会", "location": "兴和县"},
    {"id": 5, "name": "中共兴和县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共兴和县委员会", "location": "兴和县"},
    {"id": 6, "name": "中共兴和县委办公室", "type": "党委", "level": "乡科级", "parent": "中共兴和县委员会", "location": "兴和县"},
    {"id": 7, "name": "中共兴和县委宣传部", "type": "党委", "level": "乡科级", "parent": "中共兴和县委员会", "location": "兴和县"},
    {"id": 8, "name": "中共兴和县委统战部", "type": "党委", "level": "乡科级", "parent": "中共兴和县委员会", "location": "兴和县"},
    {"id": 9, "name": "兴和县公安局", "type": "政府", "level": "乡科级", "parent": "兴和县人民政府", "location": "兴和县"},
    {"id": 10, "name": "兴和县人大常委会", "type": "人大", "level": "县处级", "parent": "乌兰察布市人大常委会", "location": "兴和县"},
    {"id": 11, "name": "政协兴和县委员会", "type": "政协", "level": "县处级", "parent": "政协乌兰察布市委员会", "location": "兴和县"},
]

# ── POSITIONS ──────────────────────────────────────────────────────────

positions = [
    # 郭翔宇
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "截至2026年7月25日在任"},
    # 张雪春
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "2026年7月任代县长"},
    {"person_id": 2, "org_id": 2, "title": "政府代理县长", "start_date": "2026-07", "end_date": "present", "rank": "正处级", "note": "2026年7月6日以县长候选人身份活动，7月16日以代县长身份主持会议"},
    # 王学东
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "截至2026年7月25日在任"},
    {"person_id": 3, "org_id": 3, "title": "政法委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 周瑞君
    {"person_id": 4, "org_id": 4, "title": "县委常委、组织部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 王建伟
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "政府副县长（常务）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "负责政府常务工作"},
    # 董俊辉
    {"person_id": 6, "org_id": 5, "title": "县委常委、纪委书记、监委主任候选人", "start_date": "2026-07", "end_date": "present", "rank": "副处级", "note": "2026年7月新任职"},
    # 陈国华
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start_date": "2026-07", "end_date": "present", "rank": "副处级", "note": "2026年7月新任职"},
    {"person_id": 7, "org_id": 2, "title": "政府副县长人选", "start_date": "2026-07", "end_date": "present", "rank": "副处级", "note": "暂未分工"},
    # 窦玉
    {"person_id": 8, "org_id": 6, "title": "县委常委、办公室主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 苗雨丰
    {"person_id": 9, "org_id": 7, "title": "县委常委、宣传部部长", "start_date": "2026-07", "end_date": "present", "rank": "副处级", "note": "2026年7月新任职"},
    # 张晶
    {"person_id": 10, "org_id": 8, "title": "县委常委、统战部部长", "start_date": "2026-07", "end_date": "present", "rank": "副处级", "note": "前任为龚秀龙"},
    # 孙海军
    {"person_id": 11, "org_id": 9, "title": "县政府副县长、公安局党委书记、局长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "县政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 孙永春
    {"person_id": 12, "org_id": 2, "title": "县政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管城建、民政"},
    # 刘阳
    {"person_id": 13, "org_id": 2, "title": "县政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管教体、卫健、市场监管"},
    # 王慧霞
    {"person_id": 14, "org_id": 2, "title": "政府副县长人选", "start_date": "2026-07", "end_date": "present", "rank": "副处级", "note": "2026年7月新任职，暂未分工"},
    # 赵瑞
    {"person_id": 15, "org_id": 10, "title": "县人大常委会党组书记、主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 吉晓辉
    {"person_id": 16, "org_id": 10, "title": "县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 乔嵘
    {"person_id": 17, "org_id": 10, "title": "县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 袁义锦
    {"person_id": 18, "org_id": 10, "title": "县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 李俊
    {"person_id": 19, "org_id": 10, "title": "县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 赵慧菊
    {"person_id": 20, "org_id": 11, "title": "政协主席候选人", "start_date": "2026-07", "end_date": "present", "rank": "正处级", "note": "2026年7月新任职"},
    # 杜立新
    {"person_id": 21, "org_id": 11, "title": "县政协委员会副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 贺海燕
    {"person_id": 22, "org_id": 11, "title": "县政协委员会副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 魏军
    {"person_id": 23, "org_id": 11, "title": "县政协委员会党组成员、副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 侯志勇
    {"person_id": 24, "org_id": 11, "title": "县政协委员会党组成员、副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 李锴栋
    {"person_id": 25, "org_id": 2, "title": "前县长", "start_date": "", "end_date": "2026-06", "rank": "正处级", "note": "2026年6月前在任，2026年7月已离任"},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────────────

relationships = [
    # 党政一把手
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "县委书记与代县长党政搭档关系", "overlap_org": "中共兴和县委员会",
     "overlap_period": "2026-"},
    # 郭翔宇 ↔ 王学东
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "县委书记与分管政法副书记在常委会共事", "overlap_org": "中共兴和县委员会",
     "overlap_period": ""},
    # 郭翔宇 ↔ 周瑞君
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "县委书记与组织部长在常委会共事", "overlap_org": "中共兴和县委员会",
     "overlap_period": ""},
    # 郭翔宇 ↔ 王建伟
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "县委书记与常务副县长在常委会共事", "overlap_org": "中共兴和县委员会",
     "overlap_period": ""},
    # 郭翔宇 ↔ 董俊辉
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "县委书记与纪委书记在常委会共事", "overlap_org": "中共兴和县委员会",
     "overlap_period": "2026-07"},
    # 郭翔宇 ↔ 陈国华
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate",
     "context": "县委书记与新任常委在常委会共事", "overlap_org": "中共兴和县委员会",
     "overlap_period": "2026-07"},
    # 郭翔宇 ↔ 窦玉
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate",
     "context": "县委书记与办公室主任在常委会共事", "overlap_org": "中共兴和县委员会",
     "overlap_period": ""},
    # 郭翔宇 ↔ 苗雨丰
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate",
     "context": "县委书记与宣传部长在常委会共事", "overlap_org": "中共兴和县委员会",
     "overlap_period": "2026-07"},
    # 郭翔宇 ↔ 张晶
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate",
     "context": "县委书记与统战部长在常委会共事", "overlap_org": "中共兴和县委员会",
     "overlap_period": "2026-07"},

    # 张雪春 ↔ 王建伟
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "代县长与常务副县长在县政府共事", "overlap_org": "兴和县人民政府",
     "overlap_period": "2026-07"},
    # 张雪春 ↔ 孙海军
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate",
     "context": "代县长与公安局长在县政府共事", "overlap_org": "兴和县人民政府",
     "overlap_period": "2026-07"},
    # 张雪春 ↔ 孙永春
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate",
     "context": "代县长与分管城建副县长在县政府共事", "overlap_org": "兴和县人民政府",
     "overlap_period": "2026-07"},
    # 张雪春 ↔ 刘阳
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate",
     "context": "代县长与分管教卫副县长在县政府共事", "overlap_org": "兴和县人民政府",
     "overlap_period": "2026-07"},
    # 张雪春 ↔ 王慧霞
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate",
     "context": "代县长与新任副县长人选在县政府共事", "overlap_org": "兴和县人民政府",
     "overlap_period": "2026-07"},
    # 张雪春 ↔ 陈国华
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate",
     "context": "代县长与副县长人选在县政府共事", "overlap_org": "兴和县人民政府",
     "overlap_period": "2026-07"},

    # 王学东 ↔ 孙海军（政法系统）
    {"person_a": 3, "person_b": 11, "type": "superior_subordinate",
     "context": "政法委书记与公安局局长在政法系统共事", "overlap_org": "兴和县政法系统",
     "overlap_period": ""},

    # 王建伟 ↔ 孙永春（城建领域）
    {"person_a": 5, "person_b": 12, "type": "overlap",
     "context": "常务副县长与分管城建副县长在县政府共事", "overlap_org": "兴和县人民政府",
     "overlap_period": ""},

    # 前任-继任
    {"person_a": 25, "person_b": 2, "type": "predecessor_successor",
     "context": "李锴栋为前任县长，张雪春为继任代县长", "overlap_org": "兴和县人民政府",
     "overlap_period": "2026-06/07 交接期"},

    # 王建伟曾与李锴栋共事
    {"person_a": 5, "person_b": 25, "type": "superior_subordinate",
     "context": "王建伟在前任县长李锴栋任内已是常务副县长", "overlap_org": "兴和县人民政府",
     "overlap_period": "2025-2026"},

    # 孙永春曾与李锴栋共事
    {"person_a": 12, "person_b": 25, "type": "superior_subordinate",
     "context": "孙永春在前任县长李锴栋任内已是副县长", "overlap_org": "兴和县人民政府",
     "overlap_period": "2025-2026"},

    # 刘阳曾与李锴栋共事
    {"person_a": 13, "person_b": 25, "type": "superior_subordinate",
     "context": "刘阳在前任县长李锴栋任内已是副县长", "overlap_org": "兴和县人民政府",
     "overlap_period": "2025-2026"},
]


if __name__ == "__main__":
    db_path = os.path.join(BASE, "data/database/兴和县_network.db")
    gexf_path = os.path.join(BASE, "data/graph/兴和县_network.gexf")
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=db_path,
        gexf_path=gexf_path,
    )
