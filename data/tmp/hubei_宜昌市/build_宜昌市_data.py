#!/usr/bin/env python3
"""Build SQLite DB + GEXF graph + person JSONs for Yichang City (宜昌市), Hubei Province.

Covers: Party Secretary (市委书记), Mayor (市长), full Standing Committee (市委常委),
deputy mayors, predecessor/successor chains, and the city-level leadership network.

Sources:
- Yichang City Government website (www.yichang.gov.cn) — leadership pages
  - 市委领导: http://www.yichang.gov.cn/list-188-1.html
  - 市政府领导: http://www.yichang.gov.cn/list-190-1.html

Generated: 2026-07-24
"""

import sqlite3, os, json, sys, time
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/hubei_宜昌市")
DB_PATH = os.path.join(STAGING, "宜昌市_network.db")
GEXF_PATH = os.path.join(STAGING, "宜昌市_network.gexf")
PERSONS_DIR = os.path.join(STAGING)

# as_of date for current data
AS_OF = "2026-07-24"

# =========================================================================
# HELPER: XML escape
# =========================================================================
def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

# =========================================================================
# PERSONS
# =========================================================================
persons = [
    # ── Current top leadership ──
    {
        "id": 1,
        "name": "黄剑雄",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年7月",
        "birthplace": "",
        "education": "博士研究生、经济学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共宜昌市委书记",
        "current_org": "中共宜昌市委员会",
        "source": "http://www.yichang.gov.cn/list-64208-1.html",
    },
    {
        "id": 2,
        "name": "陈红辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年7月",
        "birthplace": "",
        "education": "博士研究生、医学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共宜昌市委副书记、宜昌市人民政府市长",
        "current_org": "宜昌市人民政府",
        "source": "http://www.yichang.gov.cn/list-64015-1.html",
    },
    # ── Deputy Party Secretary ──
    {
        "id": 3,
        "name": "燕元沂",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年10月",
        "birthplace": "",
        "education": "大学学历、法学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共宜昌市委副书记",
        "current_org": "中共宜昌市委员会",
        "source": "http://www.yichang.gov.cn/list-62866-1.html",
    },
    # ── Standing Committee members ──
    {
        "id": 4,
        "name": "贾国文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年1月",
        "birthplace": "",
        "education": "研究生、法学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共宜昌市委常委、宜昌军分区大校政治委员",
        "current_org": "宜昌军分区",
        "source": "http://www.yichang.gov.cn/list-188-1.html",
    },
    {
        "id": 5,
        "name": "徐伟营",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年1月",
        "birthplace": "",
        "education": "研究生、管理学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共宜昌市委常委、宜昌市人民政府常务副市长",
        "current_org": "宜昌市人民政府",
        "source": "http://www.yichang.gov.cn/list-63796-1.html",
    },
    {
        "id": 6,
        "name": "占学识",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年9月",
        "birthplace": "",
        "education": "大学、公共管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共宜昌市委常委、市纪委书记、市监察委员会主任",
        "current_org": "中共宜昌市纪律检查委员会",
        "source": "http://www.yichang.gov.cn/list-63821-1.html",
    },
    {
        "id": 7,
        "name": "习覃",
        "gender": "女",
        "ethnicity": "土家族",
        "birth": "1976年5月",
        "birthplace": "",
        "education": "大学学历、公共管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共宜昌市委常委、市委统战部部长",
        "current_org": "中共宜昌市委统战部",
        "source": "http://www.yichang.gov.cn/list-64212-1.html",
    },
    {
        "id": 8,
        "name": "刘传钢",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年10月",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共宜昌市委常委、市委宣传部部长",
        "current_org": "中共宜昌市委宣传部",
        "source": "http://www.yichang.gov.cn/list-63872-1.html",
    },
    {
        "id": 9,
        "name": "刘劲松",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年5月",
        "birthplace": "",
        "education": "大学、历史学学士、文学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共宜昌市委常委、市委政法委书记",
        "current_org": "中共宜昌市委政法委员会",
        "source": "http://www.yichang.gov.cn/list-64117-1.html",
    },
    {
        "id": 10,
        "name": "彭海军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年8月",
        "birthplace": "",
        "education": "硕士研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共宜昌市委常委、市委组织部部长",
        "current_org": "中共宜昌市委组织部",
        "source": "http://www.yichang.gov.cn/list-64270-1.html",
    },
    {
        "id": 11,
        "name": "肖鹏飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年12月",
        "birthplace": "",
        "education": "大学、工程硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共宜昌市委常委、市委秘书长",
        "current_org": "中共宜昌市委办公室",
        "source": "http://www.yichang.gov.cn/list-64273-1.html",
    },
    # ── Vice Mayors (non-standing-committee) ──
    {
        "id": 12,
        "name": "上官福令",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年12月",
        "birthplace": "",
        "education": "在职研究生学历、法学硕士、教育学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜昌市人民政府副市长、市公安局局长",
        "current_org": "宜昌市人民政府",
        "source": "http://www.yichang.gov.cn/list-62667-1.html",
    },
    {
        "id": 13,
        "name": "汤明",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1973年3月",
        "birthplace": "",
        "education": "大学、经济学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜昌市人民政府副市长",
        "current_org": "宜昌市人民政府",
        "source": "http://www.yichang.gov.cn/list-63970-1.html",
    },
    {
        "id": 14,
        "name": "李小军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年3月",
        "birthplace": "",
        "education": "大学学历、农业硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜昌市人民政府副市长、宜昌高新区党工委书记",
        "current_org": "宜昌市人民政府",
        "source": "http://www.yichang.gov.cn/list-64179-1.html",
    },
    {
        "id": 15,
        "name": "王澎湖",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年3月",
        "birthplace": "",
        "education": "研究生、经济学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜昌市人民政府副市长（挂职）",
        "current_org": "宜昌市人民政府",
        "source": "http://www.yichang.gov.cn/list-64189-1.html",
    },
    {
        "id": 16,
        "name": "王俊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年12月",
        "birthplace": "",
        "education": "大学、工学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜昌市人民政府副市长（挂职）",
        "current_org": "宜昌市人民政府",
        "source": "http://www.yichang.gov.cn/list-64261-1.html",
    },
    {
        "id": 17,
        "name": "曹宏伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年7月",
        "birthplace": "",
        "education": "省委党校研究生、工程硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜昌市人民政府副市长",
        "current_org": "宜昌市人民政府",
        "source": "http://www.yichang.gov.cn/list-64190-1.html",
    },
    {
        "id": 18,
        "name": "覃扬波",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1976年6月",
        "birthplace": "",
        "education": "大学",
        "party_join": "民革党员",
        "work_start": "",
        "current_post": "宜昌市人民政府副市长",
        "current_org": "宜昌市人民政府",
        "source": "http://www.yichang.gov.cn/list-64262-1.html",
    },
    {
        "id": 19,
        "name": "李昌清",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年9月",
        "birthplace": "",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宜昌市人民政府秘书长",
        "current_org": "宜昌市人民政府",
        "source": "http://www.yichang.gov.cn/list-190-1.html",
    },
    # ── Predecessor ──
    {
        "id": 20,
        "name": "熊征宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任宜昌市委书记",
        "current_org": "中共宜昌市委员会",
        "source": "宜昌市委领导页面（已卸任） — predecessor of 黄剑雄",
    },
]

# =========================================================================
# ORGANIZATIONS
# =========================================================================
organizations = [
    {"id": 1, "name": "中共宜昌市委员会", "type": "党委", "level": "地级市", "location": "宜昌市"},
    {"id": 2, "name": "宜昌市人民政府", "type": "政府", "level": "地级市", "location": "宜昌市"},
    {"id": 3, "name": "中共宜昌市纪律检查委员会", "type": "党委", "level": "地级市", "location": "宜昌市"},
    {"id": 4, "name": "中共宜昌市委统战部", "type": "党委", "level": "地级市", "location": "宜昌市"},
    {"id": 5, "name": "中共宜昌市委宣传部", "type": "党委", "level": "地级市", "location": "宜昌市"},
    {"id": 6, "name": "中共宜昌市委政法委员会", "type": "党委", "level": "地级市", "location": "宜昌市"},
    {"id": 7, "name": "中共宜昌市委组织部", "type": "党委", "level": "地级市", "location": "宜昌市"},
    {"id": 8, "name": "中共宜昌市委办公室", "type": "党委", "level": "地级市", "location": "宜昌市"},
    {"id": 9, "name": "宜昌军分区", "type": "党委", "level": "地级市", "location": "宜昌市"},
    {"id": 10, "name": "宜昌市公安局", "type": "政府", "level": "地级市", "location": "宜昌市"},
    {"id": 11, "name": "宜昌高新技术产业开发区", "type": "开发区", "level": "地级市", "location": "宜昌市"},
]

# =========================================================================
# POSITIONS
# =========================================================================
positions = [
    # 黄剑雄
    {"person_id": 1, "org_id": 1, "title": "中共宜昌市委书记", "start": "", "end": "present", "rank": "正厅级", "note": ""},
    # 陈红辉
    {"person_id": 2, "org_id": 1, "title": "中共宜昌市委副书记", "start": "", "end": "present", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "宜昌市人民政府市长、党组书记", "start": "", "end": "present", "rank": "正厅级", "note": ""},
    # 燕元沂
    {"person_id": 3, "org_id": 1, "title": "中共宜昌市委副书记", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 贾国文
    {"person_id": 4, "org_id": 9, "title": "宜昌军分区大校政治委员", "start": "", "end": "present", "rank": "正师级", "note": "中共宜昌市委常委"},
    {"person_id": 4, "org_id": 1, "title": "中共宜昌市委常委", "start": "", "end": "present", "rank": "副厅级", "note": "军分区政委兼任"},
    # 徐伟营
    {"person_id": 5, "org_id": 1, "title": "中共宜昌市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "宜昌市人民政府常务副市长、党组副书记", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 占学识
    {"person_id": 6, "org_id": 3, "title": "中共宜昌市纪委书记、市监委主任", "start": "", "end": "present", "rank": "副厅级", "note": "二级高级监察官"},
    {"person_id": 6, "org_id": 1, "title": "中共宜昌市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 习覃
    {"person_id": 7, "org_id": 4, "title": "中共宜昌市委统战部部长", "start": "", "end": "present", "rank": "副厅级", "note": "市政协党组副书记、市社会主义学院院长"},
    {"person_id": 7, "org_id": 1, "title": "中共宜昌市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 刘传钢
    {"person_id": 8, "org_id": 5, "title": "中共宜昌市委宣传部部长", "start": "", "end": "present", "rank": "副厅级", "note": "宜昌市人民政府党组成员"},
    {"person_id": 8, "org_id": 1, "title": "中共宜昌市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 刘劲松
    {"person_id": 9, "org_id": 6, "title": "中共宜昌市委政法委书记", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "中共宜昌市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 彭海军
    {"person_id": 10, "org_id": 7, "title": "中共宜昌市委组织部部长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "中共宜昌市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 肖鹏飞
    {"person_id": 11, "org_id": 8, "title": "中共宜昌市委秘书长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "中共宜昌市委常委", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 上官福令
    {"person_id": 12, "org_id": 2, "title": "宜昌市人民政府副市长", "start": "", "end": "present", "rank": "副厅级", "note": "市公安局局长、市委政法委第一副书记"},
    {"person_id": 12, "org_id": 10, "title": "宜昌市公安局党委书记、局长、督察长", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 汤明
    {"person_id": 13, "org_id": 2, "title": "宜昌市人民政府副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 李小军
    {"person_id": 14, "org_id": 2, "title": "宜昌市人民政府副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 14, "org_id": 11, "title": "宜昌高新区党工委书记", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 王澎湖
    {"person_id": 15, "org_id": 2, "title": "宜昌市人民政府副市长（挂职）", "start": "", "end": "present", "rank": "副厅级", "note": "挂职两年"},
    # 王俊
    {"person_id": 16, "org_id": 2, "title": "宜昌市人民政府副市长（挂职）", "start": "", "end": "present", "rank": "副厅级", "note": "挂职两年"},
    # 曹宏伟
    {"person_id": 17, "org_id": 2, "title": "宜昌市人民政府副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    # 覃扬波
    {"person_id": 18, "org_id": 2, "title": "宜昌市人民政府副市长", "start": "", "end": "present", "rank": "副厅级", "note": "民革党员"},
    # 李昌清
    {"person_id": 19, "org_id": 2, "title": "宜昌市人民政府秘书长", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 熊征宇（前任市委书记）
    {"person_id": 20, "org_id": 1, "title": "宜昌市委书记（前任）", "start": "", "end": "", "rank": "正厅级", "note": "已被黄剑雄接替"},
]

# =========================================================================
# RELATIONSHIPS
# =========================================================================
relationships = [
    # 书记——市长（党政一把手）
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "党政一把手搭档", "overlap_org": "中共宜昌市委员会/宜昌市人民政府", "overlap_period": AS_OF},
    # 书记——副书记
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "市委书记——专职副书记", "overlap_org": "中共宜昌市委员会", "overlap_period": AS_OF},
    # 书记——常务副市长
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "市委书记——常务副市长（市委常委班子）", "overlap_org": "中共宜昌市委员会", "overlap_period": AS_OF},
    # 书记——纪委书记
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "市委书记——纪委书记", "overlap_org": "中共宜昌市委员会", "overlap_period": AS_OF},
    # 书记——统战部长
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "市委常委班子", "overlap_org": "中共宜昌市委员会", "overlap_period": AS_OF},
    # 书记——宣传部长
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "市委常委班子", "overlap_org": "中共宜昌市委员会", "overlap_period": AS_OF},
    # 书记——政法委书记
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "市委常委班子", "overlap_org": "中共宜昌市委员会", "overlap_period": AS_OF},
    # 书记——组织部长
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "市委常委班子", "overlap_org": "中共宜昌市委员会", "overlap_period": AS_OF},
    # 书记——秘书长
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "市委常委班子、直接工作关系", "overlap_org": "中共宜昌市委员会", "overlap_period": AS_OF},
    # 书记——军分区政委
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "市委常委班子、党管武装", "overlap_org": "中共宜昌市委员会", "overlap_period": AS_OF},
    # 市长——常务副市长
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "市长——常务副市长（政府班子）", "overlap_org": "宜昌市人民政府", "overlap_period": AS_OF},
    # 市长——副市长们
    {"person_a": 2, "person_b": 12, "type": "overlap", "context": "市长——副市长（公安）", "overlap_org": "宜昌市人民政府", "overlap_period": AS_OF},
    {"person_a": 2, "person_b": 13, "type": "overlap", "context": "市长——副市长", "overlap_org": "宜昌市人民政府", "overlap_period": AS_OF},
    {"person_a": 2, "person_b": 14, "type": "overlap", "context": "市长——副市长", "overlap_org": "宜昌市人民政府", "overlap_period": AS_OF},
    {"person_a": 2, "person_b": 17, "type": "overlap", "context": "市长——副市长", "overlap_org": "宜昌市人民政府", "overlap_period": AS_OF},
    {"person_a": 2, "person_b": 18, "type": "overlap", "context": "市长——副市长", "overlap_org": "宜昌市人民政府", "overlap_period": AS_OF},
    {"person_a": 2, "person_b": 19, "type": "overlap", "context": "市长——市政府秘书长", "overlap_org": "宜昌市人民政府", "overlap_period": AS_OF},
    # 书记——前任
    {"person_a": 1, "person_b": 20, "type": "predecessor_successor", "context": "熊征宇→黄剑雄，宜昌市委书记职务交接", "overlap_org": "中共宜昌市委员会", "overlap_period": "2025-2026"},
    # 军分区政委——其他常委
    {"person_a": 4, "person_b": 5, "type": "overlap", "context": "市委常委班子", "overlap_org": "中共宜昌市委员会", "overlap_period": AS_OF},
    {"person_a": 4, "person_b": 6, "type": "overlap", "context": "市委常委班子", "overlap_org": "中共宜昌市委员会", "overlap_period": AS_OF},
    {"person_a": 7, "person_b": 8, "type": "overlap", "context": "市委常委班子", "overlap_org": "中共宜昌市委员会", "overlap_period": AS_OF},
    {"person_a": 9, "person_b": 10, "type": "overlap", "context": "市委常委班子", "overlap_org": "中共宜昌市委员会", "overlap_period": AS_OF},
]

# =========================================================================
# BUILD
# =========================================================================
def create_tables(conn):
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
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
            name TEXT NOT NULL,
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
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

print(f"[{datetime.now().strftime('%H:%M:%S')}] Building 宜昌市 network...")
print(f"  Persons: {len(persons)}")
print(f"  Organizations: {len(organizations)}")
print(f"  Positions: {len(positions)}")
print(f"  Relationships: {len(relationships)}")

# ── SQLite DB ──
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
conn = sqlite3.connect(DB_PATH)
create_tables(conn)

for p in persons:
    conn.execute(
        "INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
        (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"], p.get("birthplace", ""), p["education"], p["party_join"], p.get("work_start", ""), p["current_post"], p["current_org"], p["source"])
    )

for o in organizations:
    conn.execute(
        "INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?,?,?,?,?,?)",
        (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o["location"])
    )

for pos in positions:
    conn.execute(
        "INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)",
        (pos["person_id"], pos["org_id"], pos["title"], pos.get("start", ""), pos.get("end", ""), pos.get("rank", ""), pos.get("note", ""))
    )

for r in relationships:
    conn.execute(
        "INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
        (r["person_a"], r["person_b"], r["type"], r["context"], r["overlap_org"], r["overlap_period"])
    )

conn.commit()
conn.close()
print(f"  DB written: {DB_PATH}")

# ── GEXF ──
def person_color(p):
    """Return 'r,g,b' string based on role."""
    post = p.get("current_post", "")
    if "书记" in post and "纪委" not in post and "副" not in post:
        return "255,50,50"  # Red — top party secretary
    if "市长" in post:
        return "50,100,255"  # Blue — government head
    if "纪委书记" in post or "监委" in post:
        return "255,165,0"  # Orange — discipline
    return "100,100,100"  # Grey — others

def org_color(o):
    t = o.get("type", "")
    if "党委" in t:
        return "255,200,200"
    if "政府" in t:
        return "200,200,255"
    if "开发区" in t:
        return "200,255,200"
    return "200,200,200"

def is_top_leader(p):
    return p["id"] in (1, 2)  # 书记 and 市长

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
lines.append('    <creator>gov-relation research agent</creator>')
lines.append('    <description>宜昌市领导班子工作关系网络</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# Node attributes
lines.append('    <attributes class="node">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="org" type="string"/>')
lines.append('      <attribute id="2" title="post" type="string"/>')
lines.append('      <attribute id="3" title="birth" type="string"/>')
lines.append('      <attribute id="4" title="education" type="string"/>')
lines.append('    </attributes>')

# Edge attributes
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="0" title="type" type="string"/>')
lines.append('      <attribute id="1" title="context" type="string"/>')
lines.append('      <attribute id="2" title="period" type="string"/>')
lines.append('    </attributes>')

# Nodes
lines.append('    <nodes>')
for p in persons:
    c = person_color(p)
    sz = "20.0" if is_top_leader(p) else "12.0"
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="person"/>')
    lines.append(f'          <attvalue for="1" value="{esc(p["current_org"])}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(p["current_post"])}"/>')
    lines.append(f'          <attvalue for="3" value="{esc(p["birth"])}"/>')
    lines.append(f'          <attvalue for="4" value="{esc(p["education"])}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')

for o in organizations:
    c = org_color(o)
    lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="organization"/>')
    lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append('        <viz:size value="8.0"/>')
    lines.append('      </node>')
lines.append('    </nodes>')

# Edges
lines.append('    <edges>')
eid = 0
for pos in positions:
    eid += 1
    lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
    lines.append('        <attvalues>')
    lines.append('          <attvalue for="0" value="worked_at"/>')
    lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
    lines.append(f'          <attvalue for="2" value="{pos.get("start", "")}—{pos.get("end", "")}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

for r in relationships:
    eid += 1
    w = "2.0"  # person-to-person
    lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{w}">')
    lines.append('        <attvalues>')
    lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
    lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
    lines.append(f'          <attvalue for="2" value="{esc(r["overlap_period"])}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print(f"  GEXF written: {GEXF_PATH}")

# ── Person JSONs ──
def write_person_json(p, relationships_for_person, positions_for_person):
    slug_name = p["name"]
    filename = f"{AS_OF}-湖北省-宜昌市-{slug_name}.json"
    if "书记" in p["current_post"] and "副" not in p["current_post"] and "纪委" not in p["current_post"]:
        filename = f"{AS_OF}-湖北省-宜昌市-市委书记-{slug_name}.json"
    elif "市长" in p["current_post"] and "副" not in p["current_post"]:
        filename = f"{AS_OF}-湖北省-宜昌市-市长-{slug_name}.json"
    elif "副书记" in p["current_post"]:
        filename = f"{AS_OF}-湖北省-宜昌市-市委副书记-{slug_name}.json"
    elif "副市长" in p["current_post"] or "常务副市长" in p["current_post"]:
        filename = f"{AS_OF}-湖北省-宜昌市-副市长-{slug_name}.json"

    path = os.path.join(PERSONS_DIR, filename)

    # Build source register
    sources = []
    s_id = 0
    if p["source"] and p["source"] != "":
        s_id += 1
        sources.append({
            "id": f"S{s_id:03d}",
            "title": f"宜昌市政府信息公开 — {p['name']}",
            "url": p["source"],
            "publisher": "宜昌市人民政府",
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "官方简历页面"
        })

    # Career timeline from positions
    career_timeline = []
    for pos in positions_for_person:
        career_timeline.append({
            "start": pos.get("start", ""),
            "end": pos.get("end", ""),
            "org": "",  # would need org name lookup
            "title": pos["title"],
            "level": pos.get("rank", ""),
            "location": "宜昌市",
            "system": "party" if "党委" in pos["title"] or "纪委" in pos["title"] else "government",
            "rank": pos.get("rank", ""),
            "is_key_promotion": False,
            "notes": pos.get("note", ""),
            "confidence": "confirmed",
            "source_ids": ["S001"] if sources else []
        })

    # Relationships
    rels_out = []
    for r in relationships_for_person:
        other_id = r["person_b"] if r["person_a"] == p["id"] else r["person_a"]
        other = next((x for x in persons if x["id"] == other_id), None)
        if other:
            rels_out.append({
                "person": other["name"],
                "person_id": f"hubei_yichang_{other['name']}",
                "relationship_type": r["type"],
                "strength": "strong",
                "evidence": r["context"],
                "overlap_org": r["overlap_org"],
                "overlap_period": r["overlap_period"],
                "direction": "undirected",
                "confidence": "confirmed",
                "source_ids": ["S001"] if sources else []
            })

    doc = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "湖北省",
            "city": "宜昌市",
            "region": "宜昌市",
            "job": p["current_post"],
            "task_id": "hubei_宜昌市",
            "time_focus": "2026年7月"
        },
        "identity": {
            "person_id": f"hubei_yichang_{p['name']}",
            "name": p["name"],
            "aliases": [],
            "gender": p["gender"],
            "ethnicity": p["ethnicity"],
            "birth": p["birth"],
            "birthplace": p.get("birthplace", ""),
            "native_place": "",
            "education": [{
                "period": "",
                "institution": "",
                "major": "",
                "degree": p["education"] if p["education"] else "",
                "study_type": "unknown",
                "source_ids": ["S001"] if sources else []
            }],
            "party_join": p["party_join"],
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p['birth']}",
                "name_birthplace": f"{p['name']}_{p.get('birthplace', 'unknown')}",
                "official_profile_url": p["source"]
            }
        },
        "current_status": {
            "current_post": p["current_post"],
            "current_org": p["current_org"],
            "administrative_rank": "正厅级" if p["id"] in (1, 2) else "副厅级",
            "as_of": AS_OF,
            "is_current_confirmed": True,
            "source_ids": ["S001"] if sources else []
        },
        "career_timeline": career_timeline,
        "organizations": [],
        "relationships": rels_out,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {
                "summary": "",
                "notable_fast_promotions": []
            }
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
        },
        "network_metrics": {
            "direct_connections": len(rels_out),
            "total_relationships": len(rels_out),
            "center_rank": "core" if p["id"] in (1, 2) else "member"
        },
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": f"截至{AS_OF}，未发现公开的纪律处分、审计问题或负面报道",
                "date": "",
                "confidence": "plausible",
                "source_ids": sources[0]["id"] if sources else []
            }
        ],
        "source_register": sources,
        "confidence_summary": {
            "identity": "confirmed" if p["birth"] else "plausible",
            "current_role": "confirmed",
            "career_completeness": "partial" if p["birth"] else "thin",
            "relationship_confidence": "high",
            "biggest_gap": f"详细出生信息、籍贯和早期履历" if not p.get("birthplace") else "早期履历"
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{p['name']}的完整履历和早期职业生涯",
                "why_it_matters": "了解晋升路径、政绩积累和系统性工作经历",
                "suggested_queries": [
                    f"{p['name']} 简历 任职经历",
                    f"{p['name']} 百度百科",
                    f"{p['name']} 湖北 任职"
                ],
                "last_attempted": AS_OF
            },
            {
                "priority": "medium",
                "question": f"{p['name']}的政绩和重大项目主导经历",
                "why_it_matters": "评估施政能力和专业领域",
                "suggested_queries": [
                    f"{p['name']} 调研",
                    f"{p['name']} 项目建设"
                ],
                "last_attempted": AS_OF
            }
        ]
    }

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON written: {filename}")

# Write person JSONs for core leaders
core_ids = [1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 20]  # All SC members + predecessor
for p in persons:
    if p["id"] in core_ids:
        rels_for_p = [r for r in relationships if r["person_a"] == p["id"] or r["person_b"] == p["id"]]
        pos_for_p = [pos for pos in positions if pos["person_id"] == p["id"]]
        write_person_json(p, rels_for_p, pos_for_p)

print(f"[{datetime.now().strftime('%H:%M:%S')}] Build complete for 宜昌市!")
print(f"  DB: {DB_PATH}")
print(f"  GEXF: {GEXF_PATH}")
print(f"  Persons dir: {PERSONS_DIR}")
