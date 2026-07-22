#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 南城县 (抚州市, 江西省) leadership network.

Data sourced from official 南城县政府网站 (www.jxnc.gov.cn), verified news reports,
and public government announcements. Where information is incomplete, it is marked
with explicit confidence levels.

南城县概况: 南城县是江西省抚州市下辖的一个县,位于江西省东部,抚州市中部。
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/jiangxi_南城县")
DB_PATH = os.path.join(STAGING, "南城县_network.db")
GEXF_PATH = os.path.join(STAGING, "南城县_network.gexf")

os.makedirs(STAGING, exist_ok=True)

# =========================================================================
# DATA
# =========================================================================

# Data as-of: 2026-07-15
# Last updated: 2026-07-15

persons = [
    # ── 1: Current Party Secretary ──
    {
        "id": 1,
        "name": "郑锦锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",           # 待查 — Baidu Baike blocked
        "birthplace": "",      # 待查
        "education": "",       # 待查
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南城县委书记",
        "current_org": "中共南城县委员会",
        "source": "https://www.jxnc.gov.cn — 南城县政府网站, 2026年7月确认在职"
    },

    # ── 2: County Mayor Candidate ──
    {
        "id": 2,
        "name": "易建文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",           # 待查
        "birthplace": "",      # 待查
        "education": "",       # 待查
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南城县委副书记、县长候选人",
        "current_org": "南城县人民政府",
        "source": "https://www.jxnc.gov.cn/art/2026/7/14/art_7184_4461731.html"
    },

    # ── 3: Former County Mayor (until ~June 2026) ──
    {
        "id": 3,
        "name": "颜萍",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",           # 待查
        "birthplace": "",      # 待查
        "education": "",       # 待查
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前南城县委副书记、县长",
        "current_org": "南城县人民政府",
        "source": "https://www.jxnc.gov.cn — 2026年6月仍在任,7月由易建文接任"
    },

    # ── 4: Deputy Party Secretary ──
    {
        "id": 4,
        "name": "杨越武",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",           # 待查
        "birthplace": "",      # 待查
        "education": "",       # 待查
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南城县委副书记",
        "current_org": "中共南城县委员会",
        "source": "https://www.jxnc.gov.cn/art/2026/7/9/art_7184_4461086.html"
    },

    # ── 5: 人大常委会主任 ──
    {
        "id": 5,
        "name": "章燕萍",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",           # 待查
        "birthplace": "",      # 待查
        "education": "",       # 待查
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南城县人大常委会主任",
        "current_org": "南城县人民代表大会常务委员会",
        "source": "https://www.jxnc.gov.cn/art/2026/7/9/art_7184_4461086.html"
    },

    # ── 6: 政协主席 ──
    {
        "id": 6,
        "name": "刘凯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",           # 待查
        "birthplace": "",      # 待查
        "education": "",       # 待查
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南城县政协主席",
        "current_org": "中国人民政治协商会议南城县委员会",
        "source": "https://www.jxnc.gov.cn/art/2026/7/9/art_7184_4461086.html"
    },

    # ── 7: 县委常委、副县长 ──
    {
        "id": 7,
        "name": "张家佳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987年1月",
        "birthplace": "",      # 待查
        "education": "大学本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南城县委常委、副县长",
        "current_org": "南城县人民政府",
        "source": "https://www.jxnc.gov.cn/art/2024/5/21/art_24586_1929.html"
    },

    # ── 8: 县委常委、宣传部部长 ──
    {
        "id": 8,
        "name": "徐建平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",           # 待查
        "birthplace": "",      # 待查
        "education": "",       # 待查
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南城县委常委、宣传部部长",
        "current_org": "中共南城县委宣传部",
        "source": "https://www.jxnc.gov.cn/art/2026/4/8/art_7184_4438908.html"
    },

    # ── 9: 县委常委、统战部部长 ──
    {
        "id": 9,
        "name": "覃莉芸",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",           # 待查
        "birthplace": "",      # 待查
        "education": "",       # 待查
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南城县委常委、统战部部长",
        "current_org": "中共南城县委统战部",
        "source": "https://www.jxnc.gov.cn/art/2026/4/8/art_7184_4438908.html"
    },

    # ── 10: 县委常委、政法委书记 ──
    {
        "id": 10,
        "name": "艾胜群",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",           # 待查
        "birthplace": "",      # 待查
        "education": "",       # 待查
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南城县委常委、政法委书记",
        "current_org": "中共南城县委政法委员会",
        "source": "https://www.jxnc.gov.cn/art/2026/3/3/art_7184_4429551.html"
    },

    # ── 11: 副县长 (分管教育/卫生/民政等) ──
    {
        "id": 11,
        "name": "徐祯",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",           # 待查
        "birthplace": "",      # 待查
        "education": "",       # 待查
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南城县副县长",
        "current_org": "南城县人民政府",
        "source": "https://www.jxnc.gov.cn/art/2026/7/14/art_7184_4461731.html"
    },

    # ── 12: 副县长、公安局局长 ──
    {
        "id": 12,
        "name": "胡晓伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",           # 待查
        "birthplace": "",      # 待查
        "education": "",       # 待查
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南城县副县长、县公安局局长",
        "current_org": "南城县公安局",
        "source": "https://www.jxnc.gov.cn — 2026年7月确认在职 (col7188)"
    },

    # ── 13: 县委常委、纪委书记 (熊枝星 - 推测为纪委书记) ──
    {
        "id": 13,
        "name": "熊枝星",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",           # 待查
        "birthplace": "",      # 待查
        "education": "",       # 待查
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南城县委常委",  # 推测可能为纪委书记
        "current_org": "中共南城县委员会",
        "source": "https://www.jxnc.gov.cn/art/2026/5/13/art_7184_4446950.html"
    },

    # ── 14: 县领导 (谢少华 - 可能是人武部长或其他常委) ──
    {
        "id": 14,
        "name": "谢少华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",           # 待查
        "birthplace": "",      # 待查
        "education": "",       # 待查
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南城县领导",  # 具体职务待查
        "current_org": "中共南城县委员会",
        "source": "https://www.jxnc.gov.cn/art/2026/5/13/art_7184_4446950.html"
    },

    # ── 15: 县领导 (章带荣 - 可能是组织部长或其他) ──
    {
        "id": 15,
        "name": "章带荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",           # 待查
        "birthplace": "",      # 待查
        "education": "",       # 待查
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南城县领导",  # 具体职务待查
        "current_org": "中共南城县委员会",
        "source": "https://www.jxnc.gov.cn/art/2026/5/13/art_7184_4446950.html"
    },

    # ── 16: 县人民法院院长 ──
    {
        "id": 16,
        "name": "谭文强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",           # 待查
        "birthplace": "",      # 待查
        "education": "",       # 待查
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南城县人民法院院长",
        "current_org": "南城县人民法院",
        "source": "https://www.jxnc.gov.cn/art/2026/3/3/art_7184_4429551.html"
    },

    # ── 17: 县人民检察院检察长 ──
    {
        "id": 17,
        "name": "潘前进",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",           # 待查
        "birthplace": "",      # 待查
        "education": "",       # 待查
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "南城县人民检察院检察长",
        "current_org": "南城县人民检察院",
        "source": "https://www.jxnc.gov.cn/art/2026/3/3/art_7184_4429551.html"
    },

    # ── 18: 抚州市委书记 ──
    {
        "id": 18,
        "name": "范小林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-12",
        "birthplace": "江西宜丰",
        "education": "中央党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "抚州市委书记",
        "current_org": "中共抚州市委员会",
        "source": "https://www.jxfz.gov.cn — 2026年7月确认在职"
    },

    # ── 19: 抚州市长 ──
    {
        "id": 19,
        "name": "胡剑飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",           # 待查
        "birthplace": "",      # 待查
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "抚州市委副书记、市长",
        "current_org": "抚州市人民政府",
        "source": "https://www.jxfz.gov.cn — 2026年7月确认在职"
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共南城县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共抚州市委员会",
        "location": "江西省抚州市南城县"
    },
    {
        "id": 2,
        "name": "南城县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "抚州市人民政府",
        "location": "江西省抚州市南城县"
    },
    {
        "id": 3,
        "name": "南城县人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "抚州市人民代表大会常务委员会",
        "location": "江西省抚州市南城县"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议南城县委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "中国人民政治协商会议抚州市委员会",
        "location": "江西省抚州市南城县"
    },
    {
        "id": 5,
        "name": "中共南城县委宣传部",
        "type": "党委部门",
        "level": "乡科级",
        "parent": "中共南城县委员会",
        "location": "江西省抚州市南城县"
    },
    {
        "id": 6,
        "name": "中共南城县委统战部",
        "type": "党委部门",
        "level": "乡科级",
        "parent": "中共南城县委员会",
        "location": "江西省抚州市南城县"
    },
    {
        "id": 7,
        "name": "中共南城县委政法委员会",
        "type": "党委部门",
        "level": "乡科级",
        "parent": "中共南城县委员会",
        "location": "江西省抚州市南城县"
    },
    {
        "id": 8,
        "name": "南城县公安局",
        "type": "政府",
        "level": "乡科级",
        "parent": "南城县人民政府",
        "location": "江西省抚州市南城县"
    },
    {
        "id": 9,
        "name": "南城县人民法院",
        "type": "事业单位",
        "level": "县处级",
        "parent": "抚州市中级人民法院",
        "location": "江西省抚州市南城县"
    },
    {
        "id": 10,
        "name": "南城县人民检察院",
        "type": "事业单位",
        "level": "县处级",
        "parent": "抚州市人民检察院",
        "location": "江西省抚州市南城县"
    },
    {
        "id": 11,
        "name": "中共抚州市委员会",
        "type": "党委",
        "level": "地级",
        "parent": "中共江西省委",
        "location": "江西省抚州市"
    },
    {
        "id": 12,
        "name": "抚州市人民政府",
        "type": "政府",
        "level": "地级",
        "parent": "江西省人民政府",
        "location": "江西省抚州市"
    },
]

positions = [
    # 郑锦锋 — 县委书记
    {"id": 1, "person_id": 1, "org_id": 1, "title": "南城县委书记",
     "start": "", "end": "", "rank": "县处级正职",
     "note": "现任 — 确认至2026年7月在职"},

    # 易建文 — 县长候选人
    {"id": 2, "person_id": 2, "org_id": 2, "title": "南城县委副书记、县长候选人",
     "start": "2026-07", "end": "", "rank": "县处级正职",
     "note": "2026年7月13日以县长候选人身份公开活动"},

    # 颜萍 — 前县长
    {"id": 3, "person_id": 3, "org_id": 2, "title": "南城县委副书记、县长",
     "start": "", "end": "2026-06", "rank": "县处级正职",
     "note": "截至2026年6月仍在任县长; 7月由易建文接任"},

    # 杨越武 — 县委副书记
    {"id": 4, "person_id": 4, "org_id": 1, "title": "南城县委副书记",
     "start": "", "end": "", "rank": "县处级副职",
     "note": "现任专职副书记"},

    # 章燕萍 — 人大主任
    {"id": 5, "person_id": 5, "org_id": 3, "title": "南城县人大常委会主任",
     "start": "", "end": "", "rank": "县处级正职",
     "note": ""},

    # 刘凯 — 政协主席
    {"id": 6, "person_id": 6, "org_id": 4, "title": "南城县政协主席",
     "start": "", "end": "", "rank": "县处级正职",
     "note": ""},

    # 张家佳 — 县委常委、副县长
    {"id": 7, "person_id": 7, "org_id": 2, "title": "南城县委常委、副县长",
     "start": "", "end": "", "rank": "县处级副职",
     "note": "1987年1月生; 分管住建、城管、自然资源、生态环境等"},

    # 徐建平 — 宣传部部长
    {"id": 8, "person_id": 8, "org_id": 5, "title": "南城县委常委、宣传部部长",
     "start": "", "end": "", "rank": "县处级副职",
     "note": ""},

    # 覃莉芸 — 统战部部长
    {"id": 9, "person_id": 9, "org_id": 6, "title": "南城县委常委、统战部部长",
     "start": "", "end": "", "rank": "县处级副职",
     "note": ""},

    # 艾胜群 — 政法委书记
    {"id": 10, "person_id": 10, "org_id": 7, "title": "南城县委常委、政法委书记",
     "start": "", "end": "", "rank": "县处级副职",
     "note": ""},

    # 徐祯 — 副县长
    {"id": 11, "person_id": 11, "org_id": 2, "title": "南城县副县长",
     "start": "", "end": "", "rank": "县处级副职",
     "note": ""},

    # 胡晓伟 — 副县长、公安局局长
    {"id": 12, "person_id": 12, "org_id": 8, "title": "南城县副县长、县公安局局长",
     "start": "", "end": "", "rank": "县处级副职",
     "note": ""},

    # 熊枝星 — 县委常委（推测纪委书记）
    {"id": 13, "person_id": 13, "org_id": 1, "title": "南城县委常委",
     "start": "", "end": "", "rank": "县处级副职",
     "note": "具体职务待核实 — 可能为纪委书记"},

    # 谢少华 — 县领导
    {"id": 14, "person_id": 14, "org_id": 1, "title": "南城县领导",
     "start": "", "end": "", "rank": "县处级副职",
     "note": "具体职务待核实 — 可能为县人武部长或县委办主任"},

    # 章带荣 — 县领导
    {"id": 15, "person_id": 15, "org_id": 1, "title": "南城县领导",
     "start": "", "end": "", "rank": "县处级副职",
     "note": "具体职务待核实"},

    # 谭文强 — 法院院长
    {"id": 16, "person_id": 16, "org_id": 9, "title": "南城县人民法院院长",
     "start": "", "end": "", "rank": "县处级副职",
     "note": ""},

    # 潘前进 — 检察院检察长
    {"id": 17, "person_id": 17, "org_id": 10, "title": "南城县人民检察院检察长",
     "start": "", "end": "", "rank": "县处级副职",
     "note": ""},

    # 范小林 — 抚州市委书记
    {"id": 18, "person_id": 18, "org_id": 11, "title": "抚州市委书记",
     "start": "2024-10", "end": "", "rank": "正厅级",
     "note": "2024年10月省委任命"},

    # 胡剑飞 — 抚州市长
    {"id": 19, "person_id": 19, "org_id": 12, "title": "抚州市委副书记、市长",
     "start": "", "end": "", "rank": "正厅级",
     "note": "2026年7月确认在职"},
]

relationships = [
    # 郑锦锋 ↔ 易建文 (党政搭档: 书记—县长候选人)
    {"id": 1, "person_a_id": 1, "person_b_id": 2, "type": "党政搭档",
     "context": "郑锦锋（县委书记）与易建文（县长候选人）为南城县党政一把手关系",
     "overlap_org": "南城县",
     "overlap_period": "2026-07至今"},

    # 郑锦锋 ↔ 颜萍 (前党政搭档)
    {"id": 2, "person_a_id": 1, "person_b_id": 3, "type": "前党政搭档",
     "context": "郑锦锋（县委书记）与颜萍（前县长）曾为党政一把手搭档",
     "overlap_org": "南城县",
     "overlap_period": "至2026-06"},

    # 郑锦锋 ↔ 杨越武 (上下级)
    {"id": 3, "person_a_id": 1, "person_b_id": 4, "type": "上下级",
     "context": "郑锦锋（县委书记）直接领导县委副书记杨越武",
     "overlap_org": "中共南城县委员会",
     "overlap_period": "至今"},

    # 郑锦锋 ↔ 张家佳 (上下级)
    {"id": 4, "person_a_id": 1, "person_b_id": 7, "type": "上下级",
     "context": "郑锦锋（县委书记）与县委常委、副县长张家佳的上下级关系",
     "overlap_org": "中共南城县委员会",
     "overlap_period": "至今"},

    # 郑锦锋 ↔ 徐建平 (上下级)
    {"id": 5, "person_a_id": 1, "person_b_id": 8, "type": "上下级",
     "context": "郑锦锋（县委书记）与宣传部部长徐建平的上下级关系",
     "overlap_org": "中共南城县委员会",
     "overlap_period": "至今"},

    # 郑锦锋 ↔ 覃莉芸 (上下级)
    {"id": 6, "person_a_id": 1, "person_b_id": 9, "type": "上下级",
     "context": "郑锦锋（县委书记）与统战部部长覃莉芸的上下级关系",
     "overlap_org": "中共南城县委员会",
     "overlap_period": "至今"},

    # 郑锦锋 ↔ 艾胜群 (上下级)
    {"id": 7, "person_a_id": 1, "person_b_id": 10, "type": "上下级",
     "context": "郑锦锋（县委书记）与政法委书记艾胜群的上下级关系",
     "overlap_org": "中共南城县委员会",
     "overlap_period": "至今"},

    # 范小林 ↔ 郑锦锋 (上下级: 市委书记—县委书记)
    {"id": 8, "person_a_id": 18, "person_b_id": 1, "type": "上下级",
     "context": "范小林（抚州市委书记）直接领导南城县委书记郑锦锋",
     "overlap_org": "抚州市",
     "overlap_period": "2024-10至今"},

    # 胡剑飞 ↔ 易建文 (上下级: 市长—县长)
    {"id": 9, "person_a_id": 19, "person_b_id": 2, "type": "上下级",
     "context": "胡剑飞（抚州市长）与南城县县长候选人易建文为政府系统上下级关系",
     "overlap_org": "抚州市",
     "overlap_period": "2026-07至今"},

    # 委员之间共事关系
    {"id": 10, "person_a_id": 7, "person_b_id": 8, "type": "常委同事",
     "context": "同为南城县委常委班子成员",
     "overlap_org": "中共南城县委员会",
     "overlap_period": "至今"},

    {"id": 11, "person_a_id": 7, "person_b_id": 9, "type": "常委同事",
     "context": "同为南城县委常委班子成员",
     "overlap_org": "中共南城县委员会",
     "overlap_period": "至今"},

    {"id": 12, "person_a_id": 7, "person_b_id": 10, "type": "常委同事",
     "context": "同为南城县委常委班子成员",
     "overlap_org": "中共南城县委员会",
     "overlap_period": "至今"},

    {"id": 13, "person_a_id": 8, "person_b_id": 9, "type": "常委同事",
     "context": "同在警示教育会等会议中共同出席",
     "overlap_org": "中共南城县委员会",
     "overlap_period": "至今"},

    {"id": 14, "person_a_id": 10, "person_b_id": 12, "type": "工作关系",
     "context": "政法委书记艾胜群与公安局长胡晓伟在政法工作中紧密协作",
     "overlap_org": "南城县政法系统",
     "overlap_period": "至今"},
]

# =========================================================================
# BUILD SQLite DATABASE
# =========================================================================

if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
CREATE TABLE persons (
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

CREATE TABLE organizations (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT,
    level TEXT,
    parent TEXT,
    location TEXT
);

CREATE TABLE positions (
    id INTEGER PRIMARY KEY,
    person_id INTEGER NOT NULL,
    org_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    start TEXT,
    end TEXT,
    rank TEXT,
    note TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);

CREATE TABLE relationships (
    id INTEGER PRIMARY KEY,
    person_a_id INTEGER NOT NULL,
    person_b_id INTEGER NOT NULL,
    type TEXT NOT NULL,
    context TEXT,
    overlap_org TEXT,
    overlap_period TEXT,
    FOREIGN KEY (person_a_id) REFERENCES persons(id),
    FOREIGN KEY (person_b_id) REFERENCES persons(id)
);
""")

for p in persons:
    cur.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                 p["birthplace"], p["education"], p["party_join"], p["work_start"],
                 p["current_post"], p["current_org"], p["source"]))

for o in organizations:
    cur.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""",
                (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for pos in positions:
    cur.execute("""INSERT INTO positions VALUES (?,?,?,?,?,?,?,?)""",
                (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
                 pos["start"], pos["end"], pos["rank"], pos["note"]))

for r in relationships:
    cur.execute("""INSERT INTO relationships VALUES (?,?,?,?,?,?,?)""",
                (r["id"], r["person_a_id"], r["person_b_id"], r["type"],
                 r["context"], r["overlap_org"], r["overlap_period"]))

conn.commit()

cur.execute("SELECT COUNT(*) FROM persons")
person_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM organizations")
org_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM positions")
pos_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM relationships")
rel_count = cur.fetchone()[0]

conn.close()
print(f"SQLite database written: {DB_PATH}")
print(f"  Persons: {person_count}")
print(f"  Organizations: {org_count}")
print(f"  Positions: {pos_count}")
print(f"  Relationships: {rel_count}")

# =========================================================================
# BUILD GEXF GRAPH
# =========================================================================

today = datetime.now().strftime("%Y-%m-%d")


def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    post = p.get("current_post", "") or ""
    if "县委书记" in post:
        return (255, 50, 50)     # Red — Party Secretary
    if "县长" in post and "副" not in post:
        return (50, 100, 255)    # Blue — Gov Leader
    if "县长候选人" in post:
        return (50, 100, 255)    # Blue — Gov Leader designate
    if "人大常委会主任" in post:
        return (200, 255, 255)   # Cyan — People's Congress
    if "政协主席" in post:
        return (255, 240, 200)   # Cream — Political Consultative
    if "政法委" in post:
        return (150, 200, 230)   # Light blue-gray
    if "宣传" in post:
        return (200, 200, 100)   # Yellow
    if "统战" in post:
        return (200, 150, 200)   # Purple
    if "公安局" in post:
        return (180, 180, 220)   # Blue-gray
    if "法院" in post or "检察院" in post:
        return (180, 200, 180)   # Green-gray
    if "市委书记" in post:
        return (255, 50, 50)     # Red — Prefecture Party Secretary
    if "市长" in post and "副" not in post:
        return (50, 100, 255)    # Blue — Prefecture Mayor
    return (100, 100, 100)


def person_size(p):
    """Top leaders larger."""
    if p["id"] in [1, 2, 3, 18, 19]:
        return 20.0
    if p["id"] in [4, 5, 6, 7]:
        return 15.0
    return 12.0


def org_color(o):
    colors = {
        "党委": (255, 200, 200),     # Pink
        "政府": (200, 200, 255),     # Light blue
        "党委部门": (255, 200, 200),  # Pink
        "人大": (200, 255, 255),     # Cyan
        "政协": (255, 240, 200),     # Cream
        "事业单位": (220, 220, 220), # Light grey
    }
    return colors.get(o["type"], (200, 200, 200))


lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{today}">')
lines.append('    <creator>china-gov-network skill</creator>')
lines.append('    <description>江西省抚州市南城县领导班子工作关系网络 - 2026年7月15日生成</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# ── Attributes ──
lines.append('    <attributes class="node">')
lines.append('      <attribute id="type" title="Type" type="string"/>')
lines.append('      <attribute id="category" title="Category" type="string"/>')
lines.append('      <attribute id="birth" title="Birth" type="string"/>')
lines.append('      <attribute id="birthplace" title="Birthplace" type="string"/>')
lines.append('      <attribute id="education" title="Education" type="string"/>')
lines.append('      <attribute id="current_post" title="Current Post" type="string"/>')
lines.append('      <attribute id="source" title="Source" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="type" title="Type" type="string"/>')
lines.append('      <attribute id="context" title="Context" type="string"/>')
lines.append('      <attribute id="period" title="Period" type="string"/>')
lines.append('    </attributes>')

# ── Nodes: Persons ──
lines.append('    <nodes>')
for p in persons:
    r, g, b = person_color(p)
    sz = person_size(p)
    lines.append(f'      <node id="{p["id"]}" label="{esc(p["name"])}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="person"/>')
    lines.append(f'          <attvalue for="category" value="person"/>')
    lines.append(f'          <attvalue for="birth" value="{esc(p["birth"])}"/>')
    lines.append(f'          <attvalue for="birthplace" value="{esc(p["birthplace"])}"/>')
    lines.append(f'          <attvalue for="education" value="{esc(p["education"])}"/>')
    lines.append(f'          <attvalue for="current_post" value="{esc(p["current_post"])}"/>')
    lines.append(f'          <attvalue for="source" value="{esc(p["source"])}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append(f'      </node>')

# ── Nodes: Organizations ──
for o in organizations:
    oid = 1000 + o["id"]
    r, g, b = org_color(o)
    lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="org"/>')
    lines.append(f'          <attvalue for="category" value="{esc(o["type"])}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append(f'      </node>')
lines.append('    </nodes>')

# ── Edges ──
lines.append('    <edges>')
edge_id = 1

# person→organization (worked_at)
for pos in positions:
    oid = 1000 + pos["org_id"]
    lines.append(f'      <edge id="{edge_id}" source="{pos["person_id"]}" target="{oid}" label="worked_at">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="worked_at"/>')
    lines.append(f'          <attvalue for="context" value="{esc(pos["title"])}"/>')
    lines.append(f'          <attvalue for="period" value="{pos["start"] or "?"} → {pos["end"] or "今"}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')
    edge_id += 1

# person↔person (relationships)
for r in relationships:
    lines.append(f'      <edge id="{edge_id}" source="{r["person_a_id"]}" target="{r["person_b_id"]}" label="{esc(r["type"])}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="{esc(r["type"])}"/>')
    lines.append(f'          <attvalue for="context" value="{esc(r["context"])}"/>')
    lines.append(f'          <attvalue for="period" value="{r["overlap_period"]}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')
    edge_id += 1

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

total_nodes = len(persons) + len(organizations)
total_edges = len(positions) + len(relationships)
print(f"\nGEXF graph written: {GEXF_PATH}")
print(f"  Nodes: {len(persons)} persons + {len(organizations)} organizations = {total_nodes} total")
print(f"  Edges: {len(positions)} worked_at + {len(relationships)} relationships = {total_edges} total")
print("\nDone!")
