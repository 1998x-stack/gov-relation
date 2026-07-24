#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 拜泉县 leadership network.

拜泉县隶属黑龙江省齐齐哈尔市。

Current leadership as of 2026-07-24 (source: http://www.baiquan.gov.cn/baiquan/c101112/szf.shtml):
- 县委书记: 荣军
- 县长: 王其林

All biographical data sourced from official government leadership pages on www.baiquan.gov.cn.
"""

import sqlite3
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "拜泉县"
DB_PATH = DATABASE_DIR / "拜泉县_network.db"
GEXF_PATH = GRAPH_DIR / "拜泉县_network.gexf"

# ── ORGANIZATIONS ───────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共拜泉县委员会", "type": "党委", "level": "县处级", "parent": "中共齐齐哈尔市委", "location": "黑龙江省齐齐哈尔市拜泉县"},
    {"id": 2, "name": "拜泉县人民政府", "type": "政府", "level": "县处级", "parent": "齐齐哈尔市人民政府", "location": "黑龙江省齐齐哈尔市拜泉县"},
    {"id": 3, "name": "拜泉县人大常委会", "type": "人大", "level": "县处级", "parent": "齐齐哈尔市人大常委会", "location": "黑龙江省齐齐哈尔市拜泉县"},
    {"id": 4, "name": "拜泉县政协", "type": "政协", "level": "县处级", "parent": "齐齐哈尔市政协", "location": "黑龙江省齐齐哈尔市拜泉县"},
    {"id": 5, "name": "中共拜泉县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共齐齐哈尔市纪委", "location": "黑龙江省齐齐哈尔市拜泉县"},
    {"id": 6, "name": "中共拜泉县委政法委员会", "type": "党委", "level": "县处级", "parent": "中共拜泉县委员会", "location": "黑龙江省齐齐哈尔市拜泉县"},
    {"id": 7, "name": "中共拜泉县委组织部", "type": "党委", "level": "县处级", "parent": "中共拜泉县委员会", "location": "黑龙江省齐齐哈尔市拜泉县"},
    {"id": 8, "name": "中共拜泉县委宣传部", "type": "党委", "level": "县处级", "parent": "中共拜泉县委员会", "location": "黑龙江省齐齐哈尔市拜泉县"},
    {"id": 9, "name": "中共拜泉县委统战部", "type": "党委", "level": "县处级", "parent": "中共拜泉县委员会", "location": "黑龙江省齐齐哈尔市拜泉县"},
    {"id": 10, "name": "拜泉县人民武装部", "type": "事业单位", "level": "县处级", "parent": "齐齐哈尔军分区", "location": "黑龙江省齐齐哈尔市拜泉县"},
    {"id": 11, "name": "拜泉县公安局", "type": "政府", "level": "县处级", "parent": "拜泉县人民政府", "location": "黑龙江省齐齐哈尔市拜泉县"},
    {"id": 12, "name": "黑龙江省拜泉经济开发区", "type": "开发区", "level": "县处级", "parent": "拜泉县人民政府", "location": "黑龙江省齐齐哈尔市拜泉县"},
    {"id": 13, "name": "中共拜泉县委办公室", "type": "党委", "level": "县处级", "parent": "中共拜泉县委员会", "location": "黑龙江省齐齐哈尔市拜泉县"},
]

# ── PERSONS ─────────────────────────────────────────────────────────

persons = [
    # ═══ 县委领导 ═══
    # 1 — 荣军 — 县委书记
    {"id": 1, "name": "荣军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "省委党校大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "拜泉县委书记", "current_org": "中共拜泉县委员会",
     "source": "http://www.baiquan.gov.cn/baiquan/c101113/202006/c02_222520.shtml"},
    # 2 — 王其林 — 县长
    {"id": 2, "name": "王其林", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "大专",
     "party_join": "中共党员", "work_start": "",
     "current_post": "拜泉县委副书记、县政府党组书记、县长", "current_org": "拜泉县人民政府",
     "source": "http://www.baiquan.gov.cn/baiquan/c101113/202108/c02_222535.shtml"},
    # 3 — 梁宏宇 — 副书记
    {"id": 3, "name": "梁宏宇", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "大专",
     "party_join": "中共党员", "work_start": "",
     "current_post": "拜泉县委副书记、统战部部长、县政协党组副书记", "current_org": "中共拜泉县委员会",
     "source": "http://www.baiquan.gov.cn/baiquan/c101113/202009/c02_222531.shtml"},
    # 4 — 娄显刚 — 常务副县长
    {"id": 4, "name": "娄显刚", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "省委党校大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "拜泉县委常委、常务副县长、县政府党组副书记", "current_org": "拜泉县人民政府",
     "source": "http://www.baiquan.gov.cn/baiquan/c101113/202006/c02_222523.shtml"},
    # 5 — 李国权 — 政法委书记
    {"id": 5, "name": "李国权", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "拜泉县委常委、政法委书记", "current_org": "中共拜泉县委政法委员会",
     "source": "http://www.baiquan.gov.cn/baiquan/c101113/202009/c02_222532.shtml"},
    # 6 — 付邦才 — 人武部长
    {"id": 6, "name": "付邦才", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "大专",
     "party_join": "中共党员", "work_start": "",
     "current_post": "拜泉县委常委、人武部部长", "current_org": "拜泉县人民武装部",
     "source": "http://www.baiquan.gov.cn/baiquan/c101113/202405/c02_472093.shtml"},
    # 7 — 陈胜禹 — 副县长
    {"id": 7, "name": "陈胜禹", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "大专",
     "party_join": "中共党员", "work_start": "",
     "current_post": "拜泉县委常委、副县长、县政府党组成员", "current_org": "拜泉县人民政府",
     "source": "http://www.baiquan.gov.cn/baiquan/c101113/202401/c02_443960.shtml"},
    # 8 — 常亮亮 — 宣传部长
    {"id": 8, "name": "常亮亮", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "拜泉县委常委、宣传部部长", "current_org": "中共拜泉县委宣传部",
     "source": "http://www.baiquan.gov.cn/baiquan/c101113/202109/c02_222536.shtml"},
    # 9 — 申利君 — 组织部长
    {"id": 9, "name": "申利君", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "拜泉县委常委、组织部部长", "current_org": "中共拜泉县委组织部",
     "source": "http://www.baiquan.gov.cn/baiquan/c101113/202110/c02_222538.shtml"},
    # 10 — 李凤龙 — 县委办主任
    {"id": 10, "name": "李凤龙", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "拜泉县委常委、县委办主任", "current_org": "中共拜泉县委办公室",
     "source": "http://www.baiquan.gov.cn/baiquan/c101113/202110/c02_222539.shtml"},
    # 11 — 徐席伟 — 纪委书记
    {"id": 11, "name": "徐席伟", "gender": "男", "ethnicity": "达斡尔族",
     "birth": "", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "拜泉县委常委、纪委书记、监委主任、四级高级监察官", "current_org": "中共拜泉县纪律检查委员会",
     "source": "http://www.baiquan.gov.cn/baiquan/c101113/202507/c02_561603.shtml"},

    # ═══ 县政府领导 ═══
    # 12 — 王晓金 — 挂职副县长
    {"id": 12, "name": "王晓金", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "拜泉县副县长人选（挂职）、中储粮北方农业开发有限公司科技园区副主任", "current_org": "拜泉县人民政府",
     "source": "http://www.baiquan.gov.cn/baiquan/c101115/202507/c02_561622.shtml"},
    # 13 — 梁鑫 — 副县长
    {"id": 13, "name": "梁鑫", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "大专",
     "party_join": "中共党员", "work_start": "",
     "current_post": "拜泉县政府党组成员、副县长", "current_org": "拜泉县人民政府",
     "source": "http://www.baiquan.gov.cn/baiquan/c101115/202309/c02_307273.shtml"},
    # 14 — 张立军 — 副县长
    {"id": 14, "name": "张立军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "省委党校大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "拜泉县政府党组成员、副县长", "current_org": "拜泉县人民政府",
     "source": "http://www.baiquan.gov.cn/baiquan/c101115/202108/c02_222592.shtml"},
    # 15 — 张文凯 — 副县长
    {"id": 15, "name": "张文凯", "gender": "男", "ethnicity": "满族",
     "birth": "", "birthplace": "", "education": "省委党校大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "拜泉县政府党组成员、副县长", "current_org": "拜泉县人民政府",
     "source": "http://www.baiquan.gov.cn/baiquan/c101115/202109/c02_222594.shtml"},
    # 16 — 路宝玲 — 副县长
    {"id": 16, "name": "路宝玲", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "拜泉县政府党组成员、副县长", "current_org": "拜泉县人民政府",
     "source": "http://www.baiquan.gov.cn/baiquan/c101115/202109/c02_222595.shtml"},
    # 17 — 徐少佳 — 副县长、公安局长（新任命2026-07）
    {"id": 17, "name": "徐少佳", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "拜泉县政府副县长、县政府党组成员、县公安局长", "current_org": "拜泉县公安局",
     "source": "http://www.baiquan.gov.cn/baiquan/c101115/202607/c02_633162.shtml"},

    # ═══ 人大领导 ═══
    # 18 — 荀章河 — 人大主任
    {"id": 18, "name": "荀章河", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "省委党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "拜泉县人大常委会主任", "current_org": "拜泉县人大常委会",
     "source": "http://www.baiquan.gov.cn/baiquan/c101114/202006/c02_222541.shtml"},

    # ═══ 政协领导 ═══
    # 19 — 李颖 — 政协主席
    {"id": 19, "name": "李颖", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "省委党校大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "拜泉县政协主席", "current_org": "拜泉县政协",
     "source": "http://www.baiquan.gov.cn/baiquan/c101116/202006/c02_222599.shtml"},
]

# ── POSITIONS ──────────────────────────────────────────────────────

positions = [
    # 荣军
    {"person_id": 1, "org_id": 1, "title": "拜泉县委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "主持县委全面工作"},

    # 王其林
    {"person_id": 2, "org_id": 1, "title": "拜泉县委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "拜泉县政府党组书记、县长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "主持县政府全面工作，分管审计局、黑龙江省拜泉经济开发区管委会"},

    # 梁宏宇
    {"person_id": 3, "org_id": 1, "title": "拜泉县委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "协助县委书记抓党的建设工作、社会建设工作、深化改革工作"},
    {"person_id": 3, "org_id": 9, "title": "拜泉县委统战部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "兼任县政协党组副书记"},

    # 娄显刚
    {"person_id": 4, "org_id": 1, "title": "拜泉县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "拜泉县政府党组副书记、常务副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "协助县长抓好政府管理、财政、审计工作"},

    # 李国权
    {"person_id": 5, "org_id": 6, "title": "拜泉县委常委、政法委书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责政法、社会治安综合治理和信访维稳工作"},

    # 付邦才
    {"person_id": 6, "org_id": 1, "title": "拜泉县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 10, "title": "拜泉县人武部部长", "start_date": "", "end_date": "present", "rank": "", "note": ""},

    # 陈胜禹
    {"person_id": 7, "org_id": 1, "title": "拜泉县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "拜泉县政府党组成员、副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责经济运行、交通运输、招商引资、市场监管、统计、金融"},

    # 常亮亮
    {"person_id": 8, "org_id": 8, "title": "拜泉县委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责宣传思想文化工作"},

    # 申利君
    {"person_id": 9, "org_id": 7, "title": "拜泉县委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责组织、干部、人才工作"},

    # 李凤龙
    {"person_id": 10, "org_id": 13, "title": "拜泉县委常委、县委办主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责县委机关工作"},

    # 徐席伟
    {"person_id": 11, "org_id": 5, "title": "拜泉县委常委、纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "四级高级监察官"},

    # 王晓金
    {"person_id": 12, "org_id": 2, "title": "拜泉县副县长（挂职）", "start_date": "", "end_date": "present", "rank": "", "note": "中储粮北方农业开发有限公司挂职，负责供销工作"},

    # 梁鑫
    {"person_id": 13, "org_id": 2, "title": "拜泉县政府党组成员、副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责自然资源、住建、城管、营商环境、信访"},

    # 张立军
    {"person_id": 14, "org_id": 2, "title": "拜泉县政府党组成员、副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责农业农村、乡村振兴、农村防汛抗旱"},

    # 张文凯
    {"person_id": 15, "org_id": 2, "title": "拜泉县政府党组成员、副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责医疗保障、教育、卫生健康、体育和旅游"},

    # 路宝玲
    {"person_id": 16, "org_id": 2, "title": "拜泉县政府党组成员、副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责民政、生态环境工作"},

    # 徐少佳
    {"person_id": 17, "org_id": 11, "title": "拜泉县政府副县长、党组成员、县公安局长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责公安、司法行政和法治政府建设"},

    # 荀章河
    {"person_id": 18, "org_id": 3, "title": "拜泉县人大常委会主任", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "负责人大常委会全面工作"},

    # 李颖
    {"person_id": 19, "org_id": 4, "title": "拜泉县政协主席", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "主持县政协及政协党组全面工作"},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────────

relationships = [
    # 党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "拜泉县党政正职搭档: 县委书记与县长", "overlap_org": "中共拜泉县委员会/拜泉县人民政府", "overlap_period": "current"},
    # 县委副书记搭档关系
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委书记与专职副书记", "overlap_org": "中共拜泉县委员会", "overlap_period": "current"},
    # 县长与常务副县长
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "县长与常务副县长", "overlap_org": "拜泉县人民政府", "overlap_period": "current"},
    # 县委常委班子
    {"person_a": 4, "person_b": 5, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共拜泉县委员会", "overlap_period": "current"},
    {"person_a": 4, "person_b": 6, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共拜泉县委员会", "overlap_period": "current"},
    {"person_a": 4, "person_b": 7, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共拜泉县委员会", "overlap_period": "current"},
    {"person_a": 4, "person_b": 8, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共拜泉县委员会", "overlap_period": "current"},
    {"person_a": 4, "person_b": 9, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共拜泉县委员会", "overlap_period": "current"},
    {"person_a": 4, "person_b": 10, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共拜泉县委员会", "overlap_period": "current"},
    {"person_a": 4, "person_b": 11, "type": "overlap", "context": "县委常委班子成员：常务副县长与纪委书记", "overlap_org": "中共拜泉县委员会", "overlap_period": "current"},
    {"person_a": 5, "person_b": 7, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共拜泉县委员会", "overlap_period": "current"},
    {"person_a": 5, "person_b": 8, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共拜泉县委员会", "overlap_period": "current"},
    {"person_a": 5, "person_b": 9, "type": "overlap", "context": "县委常委班子成员：政法委书记与组织部长", "overlap_org": "中共拜泉县委员会", "overlap_period": "current"},
    {"person_a": 5, "person_b": 11, "type": "overlap", "context": "县委常委班子成员：政法委书记与纪委书记", "overlap_org": "中共拜泉县委员会", "overlap_period": "current"},
    {"person_a": 7, "person_b": 8, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共拜泉县委员会", "overlap_period": "current"},
    {"person_a": 7, "person_b": 9, "type": "overlap", "context": "县委常委班子成员：副县长与组织部长", "overlap_org": "中共拜泉县委员会", "overlap_period": "current"},
    {"person_a": 9, "person_b": 10, "type": "overlap", "context": "县委常委班子成员：组织部长与县委办主任", "overlap_org": "中共拜泉县委员会", "overlap_period": "current"},
    {"person_a": 10, "person_b": 1, "type": "overlap", "context": "县委办主任与县委书记", "overlap_org": "中共拜泉县委员会", "overlap_period": "current"},
    # 县政府班子
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "县政府班子成员", "overlap_org": "拜泉县人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 13, "type": "overlap", "context": "县政府班子成员", "overlap_org": "拜泉县人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 14, "type": "overlap", "context": "县政府班子成员", "overlap_org": "拜泉县人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 15, "type": "overlap", "context": "县政府班子成员", "overlap_org": "拜泉县人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 16, "type": "overlap", "context": "县政府班子成员", "overlap_org": "拜泉县人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 17, "type": "overlap", "context": "县政府班子成员：县长与新任公安局长", "overlap_org": "拜泉县人民政府", "overlap_period": "current"},
    {"person_a": 4, "person_b": 13, "type": "overlap", "context": "县政府班子成员：常务副县长与副县长梁鑫", "overlap_org": "拜泉县人民政府", "overlap_period": "current"},
    {"person_a": 4, "person_b": 14, "type": "overlap", "context": "县政府班子成员", "overlap_org": "拜泉县人民政府", "overlap_period": "current"},
    {"person_a": 4, "person_b": 15, "type": "overlap", "context": "县政府班子成员", "overlap_org": "拜泉县人民政府", "overlap_period": "current"},
    {"person_a": 4, "person_b": 16, "type": "overlap", "context": "县政府班子成员", "overlap_org": "拜泉县人民政府", "overlap_period": "current"},
    # 梁宏宇兼任统战部长
    {"person_a": 3, "person_b": 9, "type": "overlap", "context": "县委副书记与组织部长：党建工作协作", "overlap_org": "中共拜泉县委员会", "overlap_period": "current"},
]


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
    print("Build complete.")
