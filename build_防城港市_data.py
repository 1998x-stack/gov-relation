#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 防城港市 leadership network."""

import sqlite3
import sys
import os
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "防城港市"

# ── PERSONS ───────────────────────────────────────────────────────────
persons = [
    # 1 Party Secretary
    {"id": 1, "name": "黄江", "gender": "女", "ethnicity": "汉族",
     "birth": "1971-04", "birthplace": "广西桂林",
     "education": "研究生/文学硕士（广西师范大学外语系英美文学专业）",
     "party_join": "1993-05", "work_start": "1997-07",
     "current_post": "防城港市委书记", "current_org": "中共防城港市委员会",
     "source": "https://www.fcgs.gov.cn/zxzx/jrfcg/fcgyw/t27930434.shtml"},

    # 2 Mayor (departed June 2026 to 梧州)
    {"id": 2, "name": "邱明宏", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-08", "birthplace": "陕西宁强",
     "education": "陕西省委党校研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "梧州市委书记（原防城港市长）", "current_org": "中共梧州市委员会",
     "source": "https://www.fcgs.gov.cn/zfxxgk/zdzdgknr/ldjj/sz/"},

    # 3 Deputy Party Secretary
    {"id": 3, "name": "陆辉", "gender": "男", "ethnicity": "壮族",
     "birth": "1975-02", "birthplace": "广西武鸣",
     "education": "在职研究生/文学硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "防城港市委副书记", "current_org": "中共防城港市委员会",
     "source": "https://www.fcgs.gov.cn/zxzx/jrfcg/fcgyw/t27930434.shtml"},

    # 4 Standing Committee / Discipline Inspection
    {"id": 4, "name": "朱其东", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "防城港市委常委、市纪委书记、市监委主任", "current_org": "中共防城港市纪律检查委员会",
     "source": "https://www.fcgs.gov.cn/zxzx/jrfcg/fcgyw/t27894142.shtml"},

    # 5 Standing Committee / Executive Vice Mayor
    {"id": 5, "name": "陶德文", "gender": "男", "ethnicity": "汉族",
     "birth": "1977-08", "birthplace": "",
     "education": "在职研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "防城港市委常委、常务副市长", "current_org": "防城港市人民政府",
     "source": "https://www.fcgs.gov.cn/zfxxgk/zdzdgknr/ldjj/fsz/t19759442.shtml"},

    # 6 Standing Committee
    {"id": 6, "name": "黎家迎", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "防城港市委常委", "current_org": "中共防城港市委员会",
     "source": "https://www.fcgs.gov.cn/zxzx/jrfcg/fcgyw/t27894142.shtml"},

    # 7 Standing Committee / Organization Department
    {"id": 7, "name": "熊健", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "防城港市委常委、组织部部长", "current_org": "中共防城港市委组织部",
     "source": "https://www.fcgs.gov.cn/zxzx/jrfcg/fcgyw/t27905225.shtml"},

    # 8 Standing Committee
    {"id": 8, "name": "林春胜", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "防城港市委常委", "current_org": "中共防城港市委员会",
     "source": "https://www.fcgs.gov.cn/zxzx/jrfcg/fcgyw/t27898264.shtml"},

    # 9 Standing Committee
    {"id": 9, "name": "彭志杰", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "防城港市委常委", "current_org": "中共防城港市委员会",
     "source": "https://www.fcgs.gov.cn/zxzx/jrfcg/fcgyw/t27894142.shtml"},

    # 10 Standing Committee
    {"id": 10, "name": "容芳", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "防城港市委常委", "current_org": "中共防城港市委员会",
     "source": "https://www.fcgs.gov.cn/zxzx/jrfcg/fcgyw/t27894142.shtml"},

    # 11 Standing Committee
    {"id": 11, "name": "张建松", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "防城港市委常委", "current_org": "中共防城港市委员会",
     "source": "https://www.fcgs.gov.cn/zxzx/jrfcg/fcgyw/t27894142.shtml"},

    # 12 Standing Committee
    {"id": 12, "name": "陈佳鹏", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "防城港市委常委", "current_org": "中共防城港市委员会",
     "source": "https://www.fcgs.gov.cn/zxzx/jrfcg/fcgyw/t27898264.shtml"},

    # 13 Standing Committee
    {"id": 13, "name": "梁光", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "防城港市委常委", "current_org": "中共防城港市委员会",
     "source": "https://www.fcgs.gov.cn/zxzx/jrfcg/fcgyw/t27894142.shtml"},

    # 14 NPC Standing Committee Chair
    {"id": 14, "name": "孔建忠", "gender": "男", "ethnicity": "壮族",
     "birth": "1969-10", "birthplace": "广西河池",
     "education": "广西壮族自治区党委党校在职研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "防城港市人大常委会主任", "current_org": "防城港市人大常委会",
     "source": "https://www.fcgs.gov.cn/zxzx/jrfcg/fcgyw/t27930434.shtml"},

    # 15 CPPCC Chair
    {"id": 15, "name": "梁宗勇", "gender": "男", "ethnicity": "汉族",
     "birth": "1969-02", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "防城港市政协主席", "current_org": "中国人民政治协商会议防城港市委员会",
     "source": "https://www.fcgs.gov.cn/zxzx/jrfcg/fcgyw/t27930434.shtml"},

    # 16 Vice Mayor
    {"id": 16, "name": "廖云", "gender": "女", "ethnicity": "汉族",
     "birth": "1975-04", "birthplace": "",
     "education": "研究生/公共管理硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "防城港市副市长", "current_org": "防城港市人民政府",
     "source": "https://www.fcgs.gov.cn/zfxxgk/zdzdgknr/ldjj/fsz/t13855250.shtml"},

    # 17 Vice Mayor / Public Security
    {"id": 17, "name": "覃汇", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-04", "birthplace": "",
     "education": "中央党校大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "防城港市副市长、市公安局局长", "current_org": "防城港市人民政府",
     "source": "https://www.fcgs.gov.cn/zfxxgk/zdzdgknr/ldjj/fsz/t13755994.shtml"},

    # 18 Vice Mayor (non-CCP)
    {"id": 18, "name": "佟义东", "gender": "男", "ethnicity": "汉族",
     "birth": "1977-10", "birthplace": "",
     "education": "在职研究生/法学博士",
     "party_join": "民革党员", "work_start": "",
     "current_post": "防城港市副市长", "current_org": "防城港市人民政府",
     "source": "https://www.fcgs.gov.cn/zfxxgk/zdzdgknr/ldjj/fsz/t26110991.shtml"},

    # 19 Vice Mayor
    {"id": 19, "name": "禤东", "gender": "男", "ethnicity": "壮族",
     "birth": "1973-11", "birthplace": "",
     "education": "在职研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "防城港市副市长", "current_org": "防城港市人民政府",
     "source": "https://www.fcgs.gov.cn/zfxxgk/zdzdgknr/ldjj/fsz/t17255577.shtml"},

    # 20 Vice Mayor (seconded, PhD)
    {"id": 20, "name": "刘林", "gender": "男", "ethnicity": "汉族",
     "birth": "1982-03", "birthplace": "",
     "education": "研究生/工学博士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "防城港市副市长（挂职）", "current_org": "防城港市人民政府",
     "source": "https://www.fcgs.gov.cn/zfxxgk/zdzdgknr/ldjj/fsz/t26111019.shtml"},

    # 21 Secretary-General
    {"id": 21, "name": "梁家田", "gender": "男", "ethnicity": "壮族",
     "birth": "1974-08", "birthplace": "广西武宣",
     "education": "在职研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "防城港市政府秘书长", "current_org": "防城港市人民政府办公室",
     "source": "https://www.fcgs.gov.cn/zfxxgk/zdzdgknr/ldjj/msz/t27529335.shtml"},

    # 22 Previous Party Secretary (now at provincial level)
    {"id": 22, "name": "谭丕创", "gender": "男", "ethnicity": "汉族",
     "birth": "1968-10", "birthplace": "广西贵港",
     "education": "研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "广西壮族自治区党委常委、统战部部长", "current_org": "中共广西壮族自治区委员会统战部",
     "source": "https://zh.wikipedia.org/zh-cn/%E8%B0%AD%E4%B8%95%E5%88%9B"},

    # 23 Previous mayor before 黄江, earlier
    {"id": 23, "name": "唐轶昂", "gender": "女", "ethnicity": "汉族",
     "birth": "1975-01", "birthplace": "广西玉林",
     "education": "研究生/经济学博士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "", "current_org": "",
     "source": "https://baike.baidu.com/item/%E5%94%90%E8%BD%B6%E6%98%82"},
]

# ── ORGANIZATIONS ─────────────────────────────────────────────────────
organizations = [
    # 1-14: Party Committee, Government, NPC, CPPCC, and departments
    {"id": 1, "name": "中共防城港市委员会", "type": "党委", "level": "地级市", "parent": "中共广西壮族自治区委员会", "location": "广西防城港"},
    {"id": 2, "name": "防城港市人民政府", "type": "政府", "level": "地级市", "parent": "广西壮族自治区人民政府", "location": "广西防城港"},
    {"id": 3, "name": "防城港市人大常委会", "type": "人大", "level": "地级市", "parent": "", "location": "广西防城港"},
    {"id": 4, "name": "中国人民政治协商会议防城港市委员会", "type": "政协", "level": "地级市", "parent": "", "location": "广西防城港"},
    {"id": 5, "name": "中共防城港市纪律检查委员会", "type": "党委", "level": "地级市", "parent": "中共防城港市委员会", "location": "广西防城港"},
    {"id": 6, "name": "中共防城港市委组织部", "type": "党委", "level": "地级市", "parent": "中共防城港市委员会", "location": "广西防城港"},
    {"id": 7, "name": "防城港市人民政府办公室", "type": "政府", "level": "地级市", "parent": "防城港市人民政府", "location": "广西防城港"},
    {"id": 8, "name": "防城港市公安局", "type": "政府", "level": "地级市", "parent": "防城港市人民政府", "location": "广西防城港"},
    {"id": 9, "name": "东兴国家重点开发开放试验区管委会", "type": "开发区", "level": "地级市", "parent": "防城港市人民政府", "location": "广西东兴"},
    {"id": 10, "name": "中共广西壮族自治区委员会统战部", "type": "党委", "level": "省级", "parent": "中共广西壮族自治区委员会", "location": "广西南宁"},
    {"id": 11, "name": "中共梧州市委员会", "type": "党委", "level": "地级市", "parent": "中共广西壮族自治区委员会", "location": "广西梧州"},
    {"id": 12, "name": "中共防城港市委宣传部", "type": "党委", "level": "地级市", "parent": "中共防城港市委员会", "location": "广西防城港"},
    {"id": 13, "name": "中共防城港市委政法委员会", "type": "党委", "level": "地级市", "parent": "中共防城港市委员会", "location": "广西防城港"},
    {"id": 14, "name": "中国人民政治协商会议广西壮族自治区委员会", "type": "政协", "level": "省级", "parent": "", "location": "广西南宁"},
]

# ── POSITIONS ─────────────────────────────────────────────────────────
positions = [
    # 黄江
    {"person_id": 1, "org_id": 1, "title": "防城港市委书记", "start_date": "2024-09", "end_date": "present", "rank": "正厅级", "note": "由市长转任书记"},
    {"person_id": 1, "org_id": 2, "title": "防城港市市长", "start_date": "2021-08", "end_date": "2024-09", "rank": "正厅级", "note": "代市长转正"},
    {"person_id": 1, "org_id": 9, "title": "东兴试验区管委会主任（兼）", "start_date": "2021-08", "end_date": "2024-09", "rank": "正厅级", "note": ""},
    # 邱明宏
    {"person_id": 2, "org_id": 2, "title": "防城港市市长", "start_date": "2024-09", "end_date": "2026-06", "rank": "正厅级", "note": "调任梧州市委书记"},
    {"person_id": 2, "org_id": 11, "title": "梧州市委书记", "start_date": "2026-06", "end_date": "present", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 9, "title": "东兴试验区党工委书记、管委会主任（兼）", "start_date": "2024-09", "end_date": "2026-06", "rank": "正厅级", "note": ""},
    # 陆辉
    {"person_id": 3, "org_id": 1, "title": "防城港市委副书记", "start_date": "2025", "end_date": "present", "rank": "副厅级", "note": ""},
    # 朱其东
    {"person_id": 4, "org_id": 5, "title": "防城港市委常委、市纪委书记、市监委主任", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 陶德文
    {"person_id": 5, "org_id": 2, "title": "防城港市委常委、常务副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 黎家迎
    {"person_id": 6, "org_id": 1, "title": "防城港市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 熊健
    {"person_id": 7, "org_id": 6, "title": "防城港市委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 林春胜
    {"person_id": 8, "org_id": 1, "title": "防城港市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 彭志杰
    {"person_id": 9, "org_id": 1, "title": "防城港市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 容芳
    {"person_id": 10, "org_id": 1, "title": "防城港市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 张建松
    {"person_id": 11, "org_id": 1, "title": "防城港市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 陈佳鹏
    {"person_id": 12, "org_id": 1, "title": "防城港市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 梁光
    {"person_id": 13, "org_id": 1, "title": "防城港市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 孔建忠
    {"person_id": 14, "org_id": 3, "title": "防城港市人大常委会主任", "start_date": "2025-11", "end_date": "present", "rank": "正厅级", "note": "前河池市委副书记调任"},
    # 梁宗勇
    {"person_id": 15, "org_id": 4, "title": "防城港市政协主席", "start_date": "2024-02", "end_date": "present", "rank": "正厅级", "note": ""},
    # 廖云
    {"person_id": 16, "org_id": 2, "title": "防城港市副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 覃汇
    {"person_id": 17, "org_id": 8, "title": "防城港市副市长、市公安局局长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 佟义东
    {"person_id": 18, "org_id": 2, "title": "防城港市副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "民革党员"},
    # 禤东
    {"person_id": 19, "org_id": 2, "title": "防城港市副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 刘林
    {"person_id": 20, "org_id": 2, "title": "防城港市副市长（挂职）", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "中组部博士团挂职"},
    # 梁家田
    {"person_id": 21, "org_id": 7, "title": "防城港市政府秘书长", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 谭丕创
    {"person_id": 22, "org_id": 1, "title": "防城港市委书记", "start_date": "2021-03", "end_date": "2024-09", "rank": "正厅级", "note": ""},
    {"person_id": 22, "org_id": 10, "title": "广西壮族自治区党委常委、统战部部长", "start_date": "2025-10", "end_date": "present", "rank": "副省级", "note": ""},
    # 唐轶昂
    {"person_id": 23, "org_id": 2, "title": "防城港市市长", "start_date": "2020", "end_date": "2021", "rank": "正厅级", "note": ""},
]

# ── RELATIONSHIPS ─────────────────────────────────────────────────────
relationships = [
    # 黄江 ↔ 邱明宏：前后任（书记-市长搭班）
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor",
     "context": "黄江由市长转书记后，邱明宏接任市长，二人搭班约2年", "overlap_org": "防城港市人民政府", "overlap_period": "2024-09~2026-06"},
    # 黄江 ↔ 陆辉：上下级（书记-副书记）
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "黄江作为市委书记，陆辉作为市委副书记协助其工作", "overlap_org": "中共防城港市委员会", "overlap_period": "2025~present"},
    # 黄江 ↔ 陶德文：上下级（书记-常务副市长）
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "市委常委班子内共事", "overlap_org": "中共防城港市委员会", "overlap_period": "2024~present"},
    # 黄江 ↔ 谭丕创：前后任（书记交接）
    {"person_a": 1, "person_b": 22, "type": "predecessor_successor",
     "context": "谭丕创调任后，黄江由市长升任书记", "overlap_org": "中共防城港市委员会", "overlap_period": "2024-09"},
    # 邱明宏 ↔ 陆辉：上下级
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate",
     "context": "邱明宏任市长期间，陆辉为市委副书记", "overlap_org": "防城港市人民政府", "overlap_period": "2025~2026-06"},
    # 陶德文 ↔ 邱明宏：上下级（常务副市长-市长）
    {"person_a": 5, "person_b": 2, "type": "superior_subordinate",
     "context": "陶德文作为常务副市长协助邱明宏工作", "overlap_org": "防城港市人民政府", "overlap_period": "2024-09~2026-06"},
    # 孔建忠 ↔ 黄江：同级班子
    {"person_a": 14, "person_b": 1, "type": "overlap",
     "context": "人大主任与市委书记同城共事", "overlap_org": "防城港市", "overlap_period": "2025-11~present"},
    # 梁宗勇 ↔ 黄江：同级班子
    {"person_a": 15, "person_b": 1, "type": "overlap",
     "context": "政协主席与市委书记同城共事", "overlap_org": "防城港市", "overlap_period": "2024~present"},
    # 熊健 ↔ 黄江：上下级
    {"person_a": 7, "person_b": 1, "type": "superior_subordinate",
     "context": "组织部长在市委书记领导下工作", "overlap_org": "中共防城港市委员会", "overlap_period": ""},
    # 朱其东 ↔ 黄江：上下级
    {"person_a": 4, "person_b": 1, "type": "superior_subordinate",
     "context": "纪委书记在市委书记领导下工作", "overlap_org": "中共防城港市委员会", "overlap_period": ""},
    # 谭丕创 → 邱明宏：间接交接
    {"person_a": 22, "person_b": 2, "type": "predecessor_successor",
     "context": "谭丕创是前任书记，邱明宏是后来的市长，跨职位衔接", "overlap_org": "防城港市", "overlap_period": "2024"},
    # 谭丕创 ↔ 唐轶昂：前任搭班
    {"person_a": 22, "person_b": 23, "type": "overlap",
     "context": "谭丕创任书记时，唐轶昂曾任市长", "overlap_org": "防城港市", "overlap_period": "2021"},
]

# ── BUILD ─────────────────────────────────────────────────────────────
STAGING_DIR = os.path.join(os.path.dirname(__file__))
DB_PATH = os.path.join(STAGING_DIR, "防城港市_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "防城港市_network.gexf")

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
    print(f"Done. DB: {DB_PATH}, GEXF: {GEXF_PATH}")
