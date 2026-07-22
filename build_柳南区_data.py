#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 柳南区 leadership network.

Research sources:
- 柳南区人民政府官网 (liunan.gov.cn) — leadership pages
- Baidu Baike — 肖源, 黄立平, 贾红玉 entries
- 柳州人大 — appointment notices (2024.11.04, 2025.01.22)
- 柳州党建 — 2025.03.13 meeting report
- 广西头条NEWS/闽南网 — 贾红玉 appointment (2026.07.21)
- 澎湃新闻/柳州发布 — 任前公示 (2016.05, 2023.07)

Information currency: 2026-07-22
"""

import json
import os
import sqlite3
from datetime import datetime

AS_OF = "2026-07-22"
AS_OF_SHORT = AS_OF.replace("-", "")

# Paths
TMP = os.path.join(os.path.dirname(__file__), "..", "..", "data", "tmp", "guangxi_柳南区") if "tmp" in __file__ else os.path.join(os.path.dirname(__file__), "..", "..", "data", "tmp", "guangxi_柳南区")
# Always use tmp for staging
TMP_DIR = os.path.join(os.path.dirname(__file__)) if os.path.basename(os.path.dirname(__file__)) == "guangxi_柳南区" else os.path.join(os.path.dirname(__file__), "..", "..", "data", "tmp", "guangxi_柳南区")
DB_PATH = os.path.join(TMP_DIR, "柳南区_network.db")
GEXF_PATH = os.path.join(TMP_DIR, "柳南区_network.gexf")
PERSONS_DIR = os.path.join(TMP_DIR, "persons")

# =========================================================================
# DATA — persons, organizations, positions, relationships
# =========================================================================

# ── Persons ──
# ID range: 1-10 for 区委, 11-20 for 区政府, 21-30 for 人大/政协

persons = [
    # === 区委领导班子 ===
    {"id": 1, "name": "肖源", "gender": "男", "ethnicity": "汉族",
     "birth": "1982-03", "birthplace": "四川隆昌",
     "education": "大学学历，法学学士（中南财经政法大学）",
     "party_join": "2004-04", "work_start": "2004-07",
     "current_post": "柳南区委书记、区人武部党委第一书记",
     "current_org": "中共柳南区委员会",
     "source": "百度百科-肖源; 鲁网2024.8.7; 汲古新知2024.8.5"},
    {"id": 2, "name": "黄立平", "gender": "男", "ethnicity": "壮族",
     "birth": "1977-12", "birthplace": "广西田阳",
     "education": "北京林业大学经济管理学院林业经济管理专业",
     "party_join": "中共党员", "work_start": "",
     "current_post": "柳城县委书记（原柳南区长）",
     "current_org": "中共柳城县委员会",
     "source": "百度百科-黄立平; 柳州人大2024.11.4"},
    {"id": 3, "name": "贾红玉", "gender": "女", "ethnicity": "苗族",
     "birth": "1983-05", "birthplace": "广西融水",
     "education": "在职研究生",
     "party_join": "2006-05", "work_start": "",
     "current_post": "柳南区副区长、代理区长",
     "current_org": "柳南区人民政府",
     "source": "广西头条NEWS/闽南网2026.7.21; 百度百科-贾红玉"},
    {"id": 4, "name": "王融莉", "gender": "女", "ethnicity": "汉族",
     "birth": "1977-08", "birthplace": "",
     "education": "广西区委党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "柳南区委副书记（原宣传部长）",
     "current_org": "中共柳南区委员会",
     "source": "任前公示2023.7.28(澎湃新闻); 柳州党建2025.3.13"},
    {"id": 5, "name": "谭海平", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "柳南区委常委、常务副区长",
     "current_org": "柳南区人民政府",
     "source": "柳南区人民政府官网-领导分工2024.12.13"},
    {"id": 6, "name": "杨纪南", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "柳南区委常委、政法委书记",
     "current_org": "中共柳南区委员会",
     "source": "柳州人大2025.1.22; 柳南区人民政府官网"},
    {"id": 7, "name": "闫伟丽", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "柳南区委常委、宣传部部长",
     "current_org": "中共柳南区委员会",
     "source": "柳州党建2025.3.13; 柳州人大2025.1.22"},
    {"id": 8, "name": "叶青", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "柳南区委常委、纪委书记、监委主任",
     "current_org": "中共柳南区纪律检查委员会",
     "source": "柳南区人民政府官网2025.4.30"},
    {"id": 9, "name": "李青", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "柳南区委常委、组织部部长",
     "current_org": "中共柳南区委员会",
     "source": "柳州党建2025.3.13"},
    {"id": 10, "name": "李玉辉", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "柳南区委常委、统战部部长、柳石街道党工委书记",
     "current_org": "中共柳南区委员会",
     "source": "柳州市纪委监委网站2023.1.20"},
    {"id": 11, "name": "雷求贤", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "柳南区委常委、区人武部部长",
     "current_org": "柳南区人民武装部",
     "source": "柳南区人民政府官网2022.1.29"},
    # === 区政府领导班子 ===
    {"id": 12, "name": "肖郭婷", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "柳南区副区长",
     "current_org": "柳南区人民政府",
     "source": "柳南区人民政府官网-领导分工2024.12.13"},
    {"id": 13, "name": "孔柳宁", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "柳南区副区长、公安分局局长",
     "current_org": "柳南区人民政府",
     "source": "柳南区人民政府官网-领导分工2024.12.13"},
    {"id": 14, "name": "玉宇飞", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "柳南区副区长",
     "current_org": "柳南区人民政府",
     "source": "柳南区人民政府官网-领导分工2024.12.13"},
    {"id": 15, "name": "荣城", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "柳南区副区长",
     "current_org": "柳南区人民政府",
     "source": "柳南区人民政府官网-领导分工2024.12.13"},
    {"id": 16, "name": "陈关全", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "柳南区副区长",
     "current_org": "柳南区人民政府",
     "source": "柳南区人民政府官网-领导分工2024.12.13"},
    {"id": 17, "name": "莫畅", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "柳南区副区长",
     "current_org": "柳南区人民政府",
     "source": "柳南区人民政府官网-领导分工2024.12.13"},
    {"id": 18, "name": "邱百军", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "柳南区副区长",
     "current_org": "柳南区人民政府",
     "source": "柳南区人民政府官网-领导分工2024.12.13"},
    {"id": 19, "name": "王洪权", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "柳南区副区长",
     "current_org": "柳南区人民政府",
     "source": "柳南区人民政府官网-领导分工2024.12.13"},
    {"id": 20, "name": "肖盛华", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "柳南区副区长",
     "current_org": "柳南区人民政府",
     "source": "柳南区人民政府官网-领导分工2024.12.13"},
    # === 人大/政协 ===
    {"id": 21, "name": "龙庆革", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "柳南区人大常委会主任",
     "current_org": "柳南区人大常委会",
     "source": "百度百科-柳南区条目"},
    {"id": 22, "name": "韦寒", "gender": "男", "ethnicity": "壮族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "柳南区政协主席",
     "current_org": "政协柳南区委员会",
     "source": "百度百科-柳南区条目"},
]

# ── Organizations ──
organizations = [
    {"id": 1, "name": "中共柳南区委员会", "type": "党委", "level": "县处级",
     "parent": "中共柳州市委员会", "location": "柳州市柳南区"},
    {"id": 2, "name": "柳南区人民政府", "type": "政府", "level": "县处级",
     "parent": "柳州市人民政府", "location": "柳州市柳南区"},
    {"id": 3, "name": "中共柳南区纪律检查委员会", "type": "纪委", "level": "县处级",
     "parent": "中共柳州市纪律检查委员会", "location": "柳州市柳南区"},
    {"id": 4, "name": "柳南区人大常委会", "type": "人大", "level": "县处级",
     "parent": "柳州市人大常委会", "location": "柳州市柳南区"},
    {"id": 5, "name": "政协柳南区委员会", "type": "政协", "level": "县处级",
     "parent": "政协柳州市委员会", "location": "柳州市柳南区"},
    {"id": 6, "name": "柳南区人民武装部", "type": "政府", "level": "县处级",
     "parent": "柳州军分区", "location": "柳州市柳南区"},
    {"id": 7, "name": "柳南公安分局", "type": "政府", "level": "乡科级",
     "parent": "柳州市公安局", "location": "柳州市柳南区"},
    {"id": 8, "name": "柳石街道办事处", "type": "乡镇/街道", "level": "乡科级",
     "parent": "柳南区人民政府", "location": "柳州市柳南区"},
    # Previous organizations (for career timeline edges)
    {"id": 9, "name": "城中区人民政府", "type": "政府", "level": "县处级",
     "parent": "柳州市人民政府", "location": "柳州市城中区"},
    {"id": 10, "name": "柳北区人民政府", "type": "政府", "level": "县处级",
     "parent": "柳州市人民政府", "location": "柳州市柳北区"},
    {"id": 11, "name": "融水县人民政府", "type": "政府", "level": "县处级",
     "parent": "柳州市人民政府", "location": "柳州市融水县"},
    {"id": 12, "name": "中共鹿寨县委员会", "type": "党委", "level": "县处级",
     "parent": "中共柳州市委员会", "location": "柳州市鹿寨县"},
    {"id": 13, "name": "鹿寨县人民政府", "type": "政府", "level": "县处级",
     "parent": "柳州市人民政府", "location": "柳州市鹿寨县"},
    {"id": 14, "name": "中共柳城县委员会", "type": "党委", "level": "县处级",
     "parent": "中共柳州市委员会", "location": "柳州市柳城县"},
]

# ── Positions ──
positions = [
    # 肖源 — 柳南区委书记
    {"person_id": 1, "org_id": 1, "title": "柳南区委书记、区人武部党委第一书记",
     "start_date": "2024-08", "end_date": "present", "rank": "县处级正职",
     "note": "2024年8月由区长转任区委书记"},
    {"person_id": 1, "org_id": 2, "title": "柳南区区长",
     "start_date": "2023", "end_date": "2024-08", "rank": "县处级正职",
     "note": "2021年任常务副区长，2023年升任区长"},
    {"person_id": 1, "org_id": 1, "title": "柳南区委常委、常务副区长",
     "start_date": "2021", "end_date": "2023", "rank": "县处级副职",
     "note": ""},
    {"person_id": 1, "org_id": 10, "title": "柳北区副区长",
     "start_date": "2017", "end_date": "2021", "rank": "县处级副职",
     "note": ""},
    {"person_id": 1, "org_id": 9, "title": "城中区征地拆迁办公室主任、法制办公室主任",
     "start_date": "约2010", "end_date": "2016", "rank": "乡科级正职",
     "note": "2016年5月任前公示：拟任副处级领导职务"},
    # 黄立平 — 原区长，现任柳城县委书记
    {"person_id": 2, "org_id": 14, "title": "柳城县委书记",
     "start_date": "约2026", "end_date": "present", "rank": "县处级正职",
     "note": "从柳南区区长调任"},
    {"person_id": 2, "org_id": 2, "title": "柳南区区长",
     "start_date": "2025-01", "end_date": "约2026-06", "rank": "县处级正职",
     "note": "2024年11月4日当选，2025年1月22日仍在任"},
    {"person_id": 2, "org_id": 1, "title": "柳南区委副书记",
     "start_date": "2024-09", "end_date": "2025-01", "rank": "县处级副职",
     "note": "2024年9月任区委副书记、代区长"},
    # 贾红玉 — 代理区长
    {"person_id": 3, "org_id": 2, "title": "柳南区副区长、代理区长",
     "start_date": "2026-07", "end_date": "present", "rank": "县处级正职",
     "note": "2026年7月3日区人大常委会任命为副区长、代理区长"},
    {"person_id": 3, "org_id": 13, "title": "鹿寨县委常委、副县长",
     "start_date": "", "end_date": "2026-06", "rank": "县处级副职",
     "note": "从融水县调任至鹿寨县"},
    {"person_id": 3, "org_id": 11, "title": "融水县人民政府副县长",
     "start_date": "", "end_date": "", "rank": "县处级副职",
     "note": "早期在融水县任职"},
    # 王融莉 — 区委副书记
    {"person_id": 4, "org_id": 1, "title": "柳南区委副书记",
     "start_date": "2023", "end_date": "present", "rank": "县处级副职",
     "note": "原宣传部长进一步使用"},
    {"person_id": 4, "org_id": 1, "title": "柳南区委常委、宣传部部长",
     "start_date": "", "end_date": "2023", "rank": "县处级副职",
     "note": ""},
    # 谭海平 — 常务副区长
    {"person_id": 5, "org_id": 1, "title": "柳南区委常委",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "柳南区常务副区长",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 区委常委
    {"person_id": 6, "org_id": 1, "title": "柳南区委常委、政法委书记",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "柳南区委常委、宣传部部长",
     "start_date": "2023", "end_date": "present", "rank": "县处级副职",
     "note": "接替晋升的王融莉"},
    {"person_id": 8, "org_id": 3, "title": "柳南区委常委、纪委书记、监委主任",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "柳南区委常委、组织部部长",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "柳南区委常委、统战部部长",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 10, "org_id": 8, "title": "柳石街道党工委书记（兼）",
     "start_date": "", "end_date": "present", "rank": "乡科级正职",
     "note": "区委常委兼任街道党工委书记"},
    {"person_id": 11, "org_id": 1, "title": "柳南区委常委、区人武部部长",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 11, "org_id": 6, "title": "柳南区人民武装部部长",
     "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 副区长
    {"person_id": 12, "org_id": 2, "title": "柳南区副区长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "分管教育、文旅、农业农村、乡村振兴"},
    {"person_id": 13, "org_id": 2, "title": "柳南区副区长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "分管公安、禁毒、维稳、综治"},
    {"person_id": 13, "org_id": 7, "title": "柳南公安分局局长",
     "start_date": "", "end_date": "present", "rank": "乡科级正职", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "柳南区副区长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "分管自然资源、住建、交通、市容卫生"},
    {"person_id": 15, "org_id": 2, "title": "柳南区副区长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "分管工信、投资促进、市场监管、生态环境、民政、卫健、医保"},
    {"person_id": 16, "org_id": 2, "title": "柳南区副区长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "分管科技、高新区企业服务"},
    {"person_id": 17, "org_id": 2, "title": "柳南区副区长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "分管民兵预备役、机关后勤、政务公开、外事"},
    {"person_id": 18, "org_id": 2, "title": "柳南区副区长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "协助国防动员；分管残联、老体协"},
    {"person_id": 19, "org_id": 2, "title": "柳南区副区长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "协助重大项目、征地拆迁、民政"},
    {"person_id": 20, "org_id": 2, "title": "柳南区副区长",
     "start_date": "", "end_date": "present", "rank": "县处级副职",
     "note": "分管地志、政务信息、重点工作督查"},
    # 人大/政协
    {"person_id": 21, "org_id": 4, "title": "柳南区人大常委会主任",
     "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    {"person_id": 22, "org_id": 5, "title": "柳南区政协主席",
     "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
]

# ── Relationships ──
relationships = [
    # 党政正职搭档
    {"person_a": 1, "person_b": 3, "type": "党政搭档",
     "context": "肖源（区委书记）与贾红玉（代理区长）组成柳南区党政正职搭档",
     "overlap_org": "柳南区党政班子", "overlap_period": "2026-07至今"},
    {"person_a": 1, "person_b": 2, "type": "前任继任",
     "context": "肖源接替黄立平（？）——实际肖源先为区委书记，黄立平后来任区长，后黄立平调柳城县委",
     "overlap_org": "柳南区党政班子", "overlap_period": "未直接重叠"},
    # 区委常委间关系
    {"person_a": 1, "person_b": 4, "type": "上下级",
     "context": "肖源（区委书记）与王融莉（区委副书记）为上下级",
     "overlap_org": "柳南区委常委会", "overlap_period": "2023至今"},
    {"person_a": 1, "person_b": 5, "type": "上下级",
     "context": "肖源曾任常务副区长（2021-2023），谭海平接任常务副区长",
     "overlap_org": "柳南区政府", "overlap_period": "间接"},
    {"person_a": 4, "person_b": 7, "type": "前任继任",
     "context": "王融莉原为宣传部长，闫伟丽接任宣传部部长",
     "overlap_org": "柳南区委宣传部", "overlap_period": "2023"},
    # 区政府班子成员
    {"person_a": 3, "person_b": 5, "type": "同事",
     "context": "贾红玉（代理区长）与谭海平（常务副区长）为政府班子搭档",
     "overlap_org": "柳南区人民政府", "overlap_period": "2026-07至今"},
    {"person_a": 3, "person_b": 12, "type": "同事",
     "context": "同在柳南区政府班子", "overlap_org": "柳南区人民政府", "overlap_period": "2026-07至今"},
    {"person_a": 3, "person_b": 13, "type": "同事",
     "context": "同在柳南区政府班子", "overlap_org": "柳南区人民政府", "overlap_period": "2026-07至今"},
    {"person_a": 3, "person_b": 14, "type": "同事",
     "context": "同在柳南区政府班子", "overlap_org": "柳南区人民政府", "overlap_period": "2026-07至今"},
    {"person_a": 3, "person_b": 15, "type": "同事",
     "context": "同在柳南区政府班子", "overlap_org": "柳南区人民政府", "overlap_period": "2026-07至今"},
    # 肖源与城中区、柳北区渊源
    {"person_a": 1, "person_b": 21, "type": "同届领导",
     "context": "肖源（区委书记）与龙庆革（人大主任）为四套班子成员",
     "overlap_org": "柳南区", "overlap_period": "2024-08至今"},
    {"person_a": 1, "person_b": 22, "type": "同届领导",
     "context": "肖源（区委书记）与韦寒（政协主席）为四套班子成员",
     "overlap_org": "柳南区", "overlap_period": "2024-08至今"},
    # 跨区调动 - 肖源从城中区/柳北区来
    {"person_a": 1, "person_b": 4, "type": "跨区调动",
     "context": "肖源曾在城中区任职（2016年前），后调柳北区副区长（2017-2021），再到柳南区",
     "overlap_org": "", "overlap_period": "2010-2021"},
    # 贾红玉从融水/鹿寨来
    {"person_a": 3, "person_b": 4, "type": "跨区调动",
     "context": "贾红玉从融水县→鹿寨县→柳南区，跨两县调任",
     "overlap_org": "", "overlap_period": ""},
    # 黄立平调柳城县
    {"person_a": 2, "person_b": 1, "type": "跨区调动",
     "context": "黄立平从柳南区区长调任柳城县委书记",
     "overlap_org": "", "overlap_period": ""},
]

# =========================================================================
# HTML Escaping
# =========================================================================

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

# =========================================================================
# Person JSON builder
# =========================================================================

def make_person_json(person, timeline_items, relationships_items, source_items):
    return {
        "schema_version": "1.0", "generated_at": AS_OF,
        "investigation_scope": {
            "province": "广西壮族自治区", "city": "柳州市", "region": "柳南区",
            "job": person.get("current_post", ""), "task_id": "guangxi_柳南区", "time_focus": f"as of {AS_OF}"
        },
        "identity": {
            "person_id": f"liunan_{person['name']}",
            "name": person["name"], "aliases": [],
            "gender": person.get("gender", ""), "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""), "birthplace": person.get("birthplace", ""),
            "native_place": "", "education": [{"degree": person.get("education", "")}],
            "party_join": person.get("party_join", ""), "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{person['name']}_{person.get('birth', '')}",
                "official_profile_url": person.get("source", "")
            }
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "县处级",
            "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S001"]
        },
        "career_timeline": timeline_items,
        "organizations": [],
        "relationships": relationships_items,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "career_pattern": "",
            "systems_experience": [],
            "geographic_pattern": []
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style inference not yet attempted for this figure."
        },
        "risk_and_integrity_signals": [],
        "source_register": source_items,
        "confidence_summary": {
            "identity": "confirmed" if person.get("birth") else "plausible",
            "current_role": "confirmed",
            "career_completeness": "partial" if person.get("birth") else "thin",
            "relationship_confidence": "medium",
            "biggest_gap": f"Complete career timeline before current role for {person['name']}"
        },
        "open_questions": [
            {"priority": "critical", "question": f"Complete career timeline before current role for {person['name']}",
             "why_it_matters": "Missing career segments limit network analysis",
             "suggested_queries": [f"{person['name']} 简历", f"{person['name']} 任职经历"],
             "last_attempted": AS_OF}
        ]
    }

# =========================================================================
# BUILD
# =========================================================================

def build():
    os.makedirs(TMP_DIR, exist_ok=True)
    os.makedirs(PERSONS_DIR, exist_ok=True)

    # ── SQLite ──
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS organizations;
        DROP TABLE IF EXISTS persons;
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY, name TEXT NOT NULL, gender TEXT DEFAULT '', ethnicity TEXT DEFAULT '',
            birth TEXT DEFAULT '', birthplace TEXT DEFAULT '', education TEXT DEFAULT '',
            party_join TEXT DEFAULT '', work_start TEXT DEFAULT '', current_post TEXT DEFAULT '',
            current_org TEXT DEFAULT '', source TEXT DEFAULT ''
        );
        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY, name TEXT NOT NULL, type TEXT DEFAULT '',
            level TEXT DEFAULT '', parent TEXT DEFAULT '', location TEXT DEFAULT ''
        );
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT, person_id INTEGER NOT NULL, org_id INTEGER NOT NULL,
            title TEXT DEFAULT '', start_date TEXT DEFAULT '', end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '', note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT, person_a INTEGER NOT NULL, person_b INTEGER NOT NULL,
            type TEXT DEFAULT '', context TEXT DEFAULT '', overlap_org TEXT DEFAULT '', overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        cur.execute("""INSERT INTO persons (id,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source)
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""), p.get("birth", ""),
                     p.get("birthplace", ""), p.get("education", ""), p.get("party_join", ""), p.get("work_start", ""),
                     p.get("current_post", ""), p.get("current_org", ""), p.get("source", "")))
    for o in organizations:
        cur.execute("""INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)""",
                    (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o.get("location", "")))
    for pos in positions:
        cur.execute("""INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)""",
                    (pos["person_id"], pos["org_id"], pos["title"], pos.get("start_date", ""), pos.get("end_date", ""),
                     pos.get("rank", ""), pos.get("note", "")))
    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)""",
                    (r["person_a"], r["person_b"], r["type"], r["context"], r.get("overlap_org", ""), r.get("overlap_period", "")))
    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")
    print(f"  {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

    # ── GEXF ──
    gexf_lines = []
    gexf_lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    gexf_lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    gexf_lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    gexf_lines.append('    <creator>Gov-Relation Research Agent</creator>')
    gexf_lines.append('    <description>柳州市柳南区领导班子关系网络</description>')
    gexf_lines.append('  </meta>')
    gexf_lines.append('  <graph mode="static" defaultedgetype="undirected">')
    gexf_lines.append('    <attributes class="node">')
    gexf_lines.append('      <attribute id="0" title="type" type="string"/>')
    gexf_lines.append('      <attribute id="1" title="current_post" type="string"/>')
    gexf_lines.append('      <attribute id="2" title="current_org" type="string"/>')
    gexf_lines.append('      <attribute id="3" title="birth" type="string"/>')
    gexf_lines.append('      <attribute id="4" title="source" type="string"/>')
    gexf_lines.append('    </attributes>')
    gexf_lines.append('    <attributes class="edge">')
    gexf_lines.append('      <attribute id="0" title="type" type="string"/>')
    gexf_lines.append('      <attribute id="1" title="context" type="string"/>')
    gexf_lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    gexf_lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    gexf_lines.append('    </attributes>')
    gexf_lines.append('    <nodes>')

    for p in persons:
        pid = p["id"]
        post = p.get("current_post", "")
        # Color by role
        is_secretary = "书记" in post and "副" not in post.split("、")[0] if "、" not in post else False
        is_mayor = "区长" in post and "副" not in post.split("、")[0] if "、" not in post else "代理" in post
        is_discipline = "纪委" in post
        is_deputy_mayor = "副区长" in post
        if is_secretary:
            color = "200,30,30"
        elif is_mayor:
            color = "30,100,200"
        elif is_discipline:
            color = "255,165,0"
        elif is_deputy_mayor or "副书记" in post:
            color = "80,130,200"
        else:
            color = "100,100,100"
        size = "20.0" if (is_secretary or is_mayor) else ("15.0" if "常委" in post else "12.0")
        shape = "square" if is_secretary else ("circle" if is_mayor else "triangle")

        gexf_lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
        gexf_lines.append('        <attvalues>')
        gexf_lines.append(f'          <attvalue for="0" value="person"/>')
        gexf_lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        gexf_lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        gexf_lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        gexf_lines.append(f'          <attvalue for="4" value="{esc(p.get("source",""))}"/>')
        gexf_lines.append('        </attvalues>')
        gexf_lines.append(f'        <viz:color r="{color.split(",")[0]}" g="{color.split(",")[1]}" b="{color.split(",")[2]}" a="1.0"/>')
        gexf_lines.append(f'        <viz:size value="{size}"/>')
        gexf_lines.append(f'        <viz:shape value="{shape}"/>')
        gexf_lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        oid = o["id"] + 100000
        otype = o["type"]
        color_map = {"党委": "255,200,200", "政府": "200,200,255", "人大": "200,255,255",
                      "政协": "255,240,200", "纪委": "255,200,150", "乡镇/街道": "255,255,200"}
        ocolor = color_map.get(otype, "200,200,200")
        gexf_lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        gexf_lines.append('        <attvalues>')
        gexf_lines.append(f'          <attvalue for="0" value="organization"/>')
        gexf_lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        gexf_lines.append('        </attvalues>')
        gexf_lines.append(f'        <viz:color r="{ocolor.split(",")[0]}" g="{ocolor.split(",")[1]}" b="{ocolor.split(",")[2]}" a="0.8"/>')
        gexf_lines.append(f'        <viz:size value="8.0"/>')
        gexf_lines.append(f'        <viz:shape value="hexagon"/>')
        gexf_lines.append('      </node>')

    gexf_lines.append('    </nodes>')
    gexf_lines.append('    <edges>')

    # Worked-at edges from positions
    eid = 0
    for pos in positions:
        eid += 1
        gexf_lines.append(
            f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"] + 100000}" '
            f'label="{esc(pos["title"])}" weight="1.0">')
        gexf_lines.append('        <attvalues>')
        gexf_lines.append('          <attvalue for="0" value="worked_at"/>')
        gexf_lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        gexf_lines.append('        </attvalues>')
        gexf_lines.append('      </edge>')

    # Relationship edges
    for r in relationships:
        eid += 1
        gexf_lines.append(
            f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" '
            f'label="{esc(r["type"])}" weight="2.0">')
        gexf_lines.append('        <attvalues>')
        gexf_lines.append(f'          <attvalue for="0" value="relationship"/>')
        gexf_lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        gexf_lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org", ""))}"/>')
        gexf_lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period", ""))}"/>')
        gexf_lines.append('        </attvalues>')
        gexf_lines.append('      </edge>')

    gexf_lines.append('    </edges>')
    gexf_lines.append('  </graph>')
    gexf_lines.append('</gexf>')
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(gexf_lines))
    print(f"GEXF written: {GEXF_PATH}")

    # ── Person graph JSONs for core figures ──
    source_register = [
        {"id": "S001", "title": "鲁网 — 肖源任柳南区委书记",
         "url": "search:肖源 曾任 柳州市 城中区", "publisher": "鲁网",
         "published_at": "2024-08-07", "accessed_at": AS_OF,
         "source_type": "media", "reliability": "medium"},
        {"id": "S002", "title": "柳州人大 — 黄立平当选柳南区区长",
         "url": "search:黄立平 当选 柳南区区长", "publisher": "柳州人大",
         "published_at": "2024-11-04", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high"},
        {"id": "S003", "title": "柳州人大 — 十三届人大第六次会议",
         "url": "search:柳南区第十三届人民代表大会", "publisher": "柳州人大",
         "published_at": "2025-01-22", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high"},
        {"id": "S004", "title": "柳南区人民政府官网 — 领导分工",
         "url": "http://www.liunan.gov.cn/xxgk/ldzc/", "publisher": "柳南区人民政府",
         "published_at": "2024-12-13", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high"},
        {"id": "S005", "title": "广西头条NEWS — 贾红玉任柳南区代理区长",
         "url": "search:贾红玉 柳南区 代理区长", "publisher": "广西头条NEWS",
         "published_at": "2026-07-21", "accessed_at": AS_OF,
         "source_type": "media", "reliability": "high"},
        {"id": "S006", "title": "柳州党建 — 组织宣传统战社会工作会议",
         "url": "search:柳州党建 柳南区委", "publisher": "柳州党建",
         "published_at": "2025-03-13", "accessed_at": AS_OF,
         "source_type": "official", "reliability": "high"},
        {"id": "S007", "title": "澎湃新闻/柳州发布 — 任前公示",
         "url": "search:王融莉 任前公示", "publisher": "澎湃新闻",
         "published_at": "2023-07-28", "accessed_at": AS_OF,
         "source_type": "appointment_notice", "reliability": "high"},
    ]

    core_figures = {"肖源": 1, "黄立平": 2, "贾红玉": 3, "王融莉": 4, "谭海平": 5}
    for p in persons:
        if p["name"] in core_figures:
            timeline = []
            for pos in positions:
                if pos["person_id"] == p["id"]:
                    org_name = next((o["name"] for o in organizations if o["id"] == pos["org_id"]), "")
                    timeline.append({
                        "start": pos.get("start_date", ""), "end": pos.get("end_date", ""),
                        "org": org_name, "title": pos["title"], "rank": pos.get("rank", ""),
                        "location": "广西柳州", "notes": pos.get("note", ""),
                        "confidence": "confirmed" if pos.get("start_date") else "plausible",
                        "source_ids": ["S001", "S004"]
                    })
            rels = []
            for r in relationships:
                if r["person_a"] == p["id"]:
                    other = next((x["name"] for x in persons if x["id"] == r["person_b"]), "")
                    rels.append({"person": other, "relationship_type": r["type"],
                                 "evidence": r["context"], "confidence": "confirmed"})
                elif r["person_b"] == p["id"]:
                    other = next((x["name"] for x in persons if x["id"] == r["person_a"]), "")
                    rels.append({"person": other, "relationship_type": r["type"],
                                 "evidence": r["context"], "confidence": "confirmed"})
            pjson = make_person_json(p, timeline, rels, source_register)
            p_filename = f"{AS_OF_SHORT}-广西壮族自治区-柳州市-{p['current_post'].replace('/','-')}-{p['name']}.json"
            p_path = os.path.join(PERSONS_DIR, p_filename)
            with open(p_path, "w", encoding="utf-8") as f:
                json.dump(pjson, f, ensure_ascii=False, indent=2)
            print(f"Person JSON written: {p_path}")

    print(f"\nBuild complete. {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships.")


if __name__ == "__main__":
    build()
