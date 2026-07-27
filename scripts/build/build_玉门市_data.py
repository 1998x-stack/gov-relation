#!/usr/bin/env python3
"""
玉门市（酒泉市）领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Yumen City leadership.

Level: 县级市
Province: 甘肃省
Parent City: 酒泉市

Research Sources:
- yumen.gov.cn — 官方网站新闻报道 (primary, 2026-07确认)
- yumen.gov.cn 领导之窗 (市政府领导名单)
- 百度百科 — 李应伟履历
- 庆阳市/肃州区 build 脚本 — 胡志勇(前任书记)、何正军(前任市长)数据
- 新闻报道 (中国经济网、澎湃新闻、每日甘肃网等)

Research Date: 2026-07-22
"""

import json
import os
import sqlite3
from datetime import datetime

# ── PATHS ──
BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/gansu_玉门市")
os.makedirs(STAGING, exist_ok=True)

DB_PATH = os.path.join(STAGING, "玉门市_network.db")
GEXF_PATH = os.path.join(STAGING, "玉门市_network.gexf")

# ════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════

# Person ID format: ym_{surname}{givenname} (ym = YuMen)

PERSONS = [
    # ══════════════════════════════════════
    # 市委领导
    # ══════════════════════════════════════

    # 李应伟 — 市委书记
    ("ym_li_yingwei", "李应伟", "男", "汉族", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "玉门市委书记",
     "中共玉门市委员会",
     "yumen.gov.cn新闻报道（2026年7月多篇）; yumen.gov.cn首页头条"),

    # 王迎军 — 市委副书记、市长
    ("ym_wang_yingjun", "王迎军", "男", "汉族", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "玉门市委副书记、市长",
     "玉门市人民政府",
     "yumen.gov.cn领导之窗; yumen.gov.cn新闻报道（2026年7月多篇）"),

    # 赵超 — 市委常委、常务副市长
    ("ym_zhao_chao", "赵超", "男", "汉族", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "玉门市委常委、常务副市长",
     "玉门市人民政府",
     "yumen.gov.cn领导之窗; yumen.gov.cn矿山应急演练报道2026-07-10"),

    # 张继 — 市委常委、纪委书记、监委代主任
    ("ym_zhang_ji", "张继", "男", "汉族", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "玉门市委常委、纪委书记、监委代主任",
     "中共玉门市纪律检查委员会",
     "yumen.gov.cn李应伟调研廉洁文化建设报道2026-07-10"),

    # 白雪瑞 — 市领导（职务待确认）
    ("ym_bai_xuerui", "白雪瑞", "男", "汉族", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "玉门市领导",
     "玉门市",
     "yumen.gov.cn中心组学习会议报道2026-07-21"),

    # 谢祥 — 市领导（职务待确认）
    ("ym_xie_xiang", "谢祥", "男", "汉族", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "玉门市领导",
     "玉门市",
     "yumen.gov.cn中心组学习会议报道2026-07-21; 矿山应急演练报道2026-07-10"),

    # 范志俊 — 市领导（职务待确认）
    ("ym_fan_zhijun", "范志俊", "男", "汉族", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "玉门市领导",
     "玉门市",
     "yumen.gov.cn中心组学习会议报道2026-07-21; 矿山应急演练报道2026-07-10"),

    # 王菲 — 市领导（职务待确认，可能是市委常委或副市长）
    ("ym_wang_fei", "王菲", "女", "汉族", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "玉门市领导",
     "玉门市",
     "yumen.gov.cn中心组学习会议报道2026-07-21; 矿山应急演练报道2026-07-10"),

    # ══════════════════════════════════════
    # 市政府副市长（领导之窗确认）
    # ══════════════════════════════════════

    # 史先勇 — 副市长
    ("ym_shi_xianyong", "史先勇", "男", "汉族", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "玉门市人民政府副市长",
     "玉门市人民政府",
     "yumen.gov.cn领导之窗; yumen.gov.cn氟硅新材料招商推介会报道2026-07-10; 兰洽会巡馆报道2026-07-09"),

    # 王涛 — 副市长
    ("ym_wang_tao", "王涛", "男", "汉族", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "玉门市人民政府副市长",
     "玉门市人民政府",
     "yumen.gov.cn领导之窗; yumen.gov.cn矿山应急演练报道2026-07-10"),

    # 张晓芸 — 副市长
    ("ym_zhang_xiaoyun", "张晓芸", "女", "汉族", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "玉门市人民政府副市长",
     "玉门市人民政府",
     "yumen.gov.cn领导之窗; yumen.gov.cn中心组学习会议报道2026-07-21; 矿山应急演练报道2026-07-10"),

    # 岳建强 — 副市长
    ("ym_yue_jianqiang", "岳建强", "男", "汉族", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "玉门市人民政府副市长",
     "玉门市人民政府",
     "yumen.gov.cn领导之窗"),

    # 张桐 — 副市长
    ("ym_zhang_tong", "张桐", "男", "汉族", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "玉门市人民政府副市长",
     "玉门市人民政府",
     "yumen.gov.cn领导之窗"),

    # 马玉军 — 副市长
    ("ym_ma_yujun", "马玉军", "男", "汉族", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "玉门市人民政府副市长",
     "玉门市人民政府",
     "yumen.gov.cn领导之窗"),

    # ══════════════════════════════════════
    # 人大、政协
    # ══════════════════════════════════════

    # 李红 — 市人大常委会主任
    ("ym_li_hong", "李红", "男", "汉族", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "玉门市人大常委会主任",
     "玉门市人民代表大会常务委员会",
     "yumen.gov.cn中心组学习会议报道2026-07-21; 矿山应急演练报道2026-07-10"),

    # 周勤 — 市政协主席
    ("ym_zhou_qin", "周勤", "男", "汉族", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "玉门市政协主席",
     "中国人民政治协商会议玉门市委员会",
     "yumen.gov.cn中心组学习会议报道2026-07-21"),

    # 张存明 — 市政协党组书记
    ("ym_zhang_cunming", "张存明", "男", "汉族", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "玉门市政协党组书记",
     "中国人民政治协商会议玉门市委员会",
     "yumen.gov.cn中心组学习会议报道2026-07-21; 矿山应急演练报道2026-07-10"),

    # ══════════════════════════════════════
    # 前任主要领导
    # ══════════════════════════════════════

    # 胡志勇 — 前任玉门市委书记 (2019-2021), 现任庆阳市长
    ("ym_hu_zhiyong", "胡志勇", "男", "汉族", "1974年2月", "甘肃省金塔县", "甘肃金塔",
     "大专(甘肃政法学院)/在职研究生(兰州大学法律专业)", "1999年6月", "1995年7月",
     "庆阳市委副书记、市政府党组书记、市长",
     "庆阳市人民政府",
     "庆阳市build脚本; 庆阳市person档案; Wikipedia; 中国经济网"),

    # 何正军 — 前任玉门市长, 现任酒泉市人大常委会副主任
    ("ym_he_zhengjun", "何正军", "男", "汉族", "1967年12月", "甘肃金塔", "甘肃金塔",
     "省委党校研究生/文学学士", "中共党员", "1987年7月",
     "酒泉市人大常委会副主任",
     "酒泉市人民代表大会常务委员会",
     "肃州区build脚本; 酒泉市build脚本; thepaper.cn; 中国经济网"),

    # 陈炎人 — 更早前任玉门市委书记
    ("ym_chen_yanren", "陈炎人", "男", "汉族", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "（原玉门市委书记，去向待查）",
     "待查",
     "Wikipedia（玉门市条目，显示陈炎人为书记，但已过时）; 需进一步确认"),
]

ORGANIZATIONS = [
    # id, name, type, level, parent, location
    ("ym_party_committee", "中共玉门市委员会", "党委", "县级", "中共酒泉市委员会", "酒泉市玉门市"),
    ("ym_gov", "玉门市人民政府", "政府", "县级", "酒泉市人民政府", "酒泉市玉门市"),
    ("ym_discipline", "中共玉门市纪律检查委员会", "纪委", "县级", "中共酒泉市纪律检查委员会", "酒泉市玉门市"),
    ("ym_people_congress", "玉门市人民代表大会常务委员会", "人大", "县级", "酒泉市人大常委会", "酒泉市玉门市"),
    ("ym_cppcc", "中国人民政治协商会议玉门市委员会", "政协", "县级", "酒泉市政协", "酒泉市玉门市"),
    ("ym_party_org", "中共玉门市委组织部", "党委部门", "正科级", "中共玉门市委员会", "酒泉市玉门市"),
    ("ym_propaganda", "中共玉门市委宣传部", "党委部门", "正科级", "中共玉门市委员会", "酒泉市玉门市"),
    ("ym_united_front", "中共玉门市委统一战线工作部", "党委部门", "正科级", "中共玉门市委员会", "酒泉市玉门市"),
    ("ym_political_legal", "中共玉门市委政法委员会", "党委部门", "正科级", "中共玉门市委员会", "酒泉市玉门市"),
]

POSITIONS = [
    # person_id, org_id, title, start, end, rank, note

    # ═══ 李应伟 — 市委书记 ═══
    ("ym_li_yingwei", "ym_party_committee", "玉门市委书记", "?", "至今", "正处级", "主持市委全面工作。系县级市书记，可能兼任酒泉市委常委"),

    # ═══ 王迎军 — 市长 ═══
    ("ym_wang_yingjun", "ym_gov", "玉门市委副书记、市长", "?", "至今", "正处级", "主持市政府全面工作"),

    # ═══ 赵超 — 常务副市长 ═══
    ("ym_zhao_chao", "ym_gov", "玉门市委常委、常务副市长", "?", "至今", "副处级", "负责市政府常务工作；兼任市抗震救灾、防汛抗洪、矿山应急指挥部总指挥"),

    # ═══ 张继 — 纪委书记 ═══
    ("ym_zhang_ji", "ym_discipline", "玉门市委常委、纪委书记、监委代主任", "?", "至今", "副处级", "分管纪检监察工作"),

    # ═══ 白雪瑞 — 市领导 ═══
    ("ym_bai_xuerui", "ym_party_committee", "玉门市领导（疑似常委）", "?", "至今", "副处级", "参加市委理论学习中心组会议；具体职务待确认"),

    # ═══ 谢祥 — 市领导 ═══
    ("ym_xie_xiang", "ym_party_committee", "玉门市领导（疑似常委）", "?", "至今", "副处级", "参加市委理论学习中心组会议和矿山演练观摩；具体职务待确认"),

    # ═══ 范志俊 — 市领导 ═══
    ("ym_fan_zhijun", "ym_party_committee", "玉门市领导（疑似常委）", "?", "至今", "副处级", "参加市委理论学习中心组会议和矿山演练观摩；具体职务待确认"),

    # ═══ 王菲 — 市领导 ═══
    ("ym_wang_fei", "ym_party_committee", "玉门市领导（疑似常委）", "?", "至今", "副处级", "参加市委理论学习中心组会议和矿山演练观摩；具体职务待确认"),

    # ═══ 史先勇 — 副市长 ═══
    ("ym_shi_xianyong", "ym_gov", "玉门市人民政府副市长", "?", "至今", "副处级", "分管领域待确认；参加兰洽会和氟硅新材料招商推介会"),

    # ═══ 王涛 — 副市长 ═══
    ("ym_wang_tao", "ym_gov", "玉门市人民政府副市长", "?", "至今", "副处级", "分管领域待确认"),

    # ═══ 张晓芸 — 副市长 ═══
    ("ym_zhang_xiaoyun", "ym_gov", "玉门市人民政府副市长", "?", "至今", "副处级", "分管领域待确认"),

    # ═══ 岳建强 — 副市长 ═══
    ("ym_yue_jianqiang", "ym_gov", "玉门市人民政府副市长", "?", "至今", "副处级", "分管领域待确认；可能兼任公安局长"),

    # ═══ 张桐 — 副市长 ═══
    ("ym_zhang_tong", "ym_gov", "玉门市人民政府副市长", "?", "至今", "副处级", "分管领域待确认"),

    # ═══ 马玉军 — 副市长 ═══
    ("ym_ma_yujun", "ym_gov", "玉门市人民政府副市长", "?", "至今", "副处级", "分管领域待确认"),

    # ═══ 李红 — 人大主任 ═══
    ("ym_li_hong", "ym_people_congress", "玉门市人大常委会主任", "?", "至今", "正处级", "主持市人大常委会工作"),

    # ═══ 周勤 — 政协主席 ═══
    ("ym_zhou_qin", "ym_cppcc", "玉门市政协主席", "?", "至今", "正处级", "主持市政协全面工作"),

    # ═══ 张存明 — 政协党组书记 ═══
    ("ym_zhang_cunming", "ym_cppcc", "玉门市政协党组书记", "?", "至今", "正处级", "主持市政协党组工作"),

    # ═══ 胡志勇 — 前任书记 ═══
    ("ym_hu_zhiyong", "ym_party_committee", "玉门市委书记", "2019-06", "2021-10", "正处级", "前任玉门市委书记，2021年调任天水市副市长"),
    ("ym_hu_zhiyong", "", "酒泉市工业和信息化局局长", "~2019-02", "2019-06", "正处级", "任玉门市委书记前职"),
    ("ym_hu_zhiyong", "", "天水市人民政府副市长", "2021-10", "2024-02", "副厅级", "从天水副市长晋升"),
    ("ym_hu_zhiyong", "", "天水市委常委、政法委书记", "~2024-02", "~2026-04", "副厅级", "在天水晋升常委"),
    ("ym_hu_zhiyong", "", "庆阳市委副书记、市长", "~2026-04", "至今", "正厅级", "现任"),

    # ═══ 何正军 — 前任市长 ═══
    ("ym_he_zhengjun", "ym_gov", "玉门市委副书记、市长", "?", "?", "正处级", "前职；具体任期待确认"),
    ("ym_he_zhengjun", "", "阿克塞县委副书记、人大常委会主任", "?", "?", "正处级", "前职"),
    ("ym_he_zhengjun", "", "肃州区委书记", "~2019?", "~2024-01", "副厅级", "兼任酒泉市委常委"),
    ("ym_he_zhengjun", "", "酒泉市委常委、常务副市长", "2023-12", "2025-09", "副厅级", ""),
    ("ym_he_zhengjun", "ym_people_congress", "酒泉市人大常委会副主任", "2025-10", "至今", "副厅级", "现任"),

    # ═══ 陈炎人 — 更早前任书记 ═══
    ("ym_chen_yanren", "ym_party_committee", "玉门市委书记", "?", "?", "正处级", "Wikipedia仍显示（信息可能已过时）；去向待查"),
]

RELATIONSHIPS = [
    # person_a, person_b, type, context, overlap_org, overlap_period

    # 党政搭档
    ("ym_li_yingwei", "ym_wang_yingjun", "党政搭档", "市委书记与市长，共同领导玉门市", "玉门市委/市政府", "至今"),

    # 上下级关系（书记与常委/副市长）
    ("ym_li_yingwei", "ym_zhao_chao", "上下级", "市委书记与常务副市长", "玉门市委/市政府", ""),
    ("ym_li_yingwei", "ym_zhang_ji", "上下级", "市委书记与纪委书记", "玉门市委", ""),
    ("ym_li_yingwei", "ym_shi_xianyong", "上下级", "市委书记与副市长", "玉门市委/市政府", ""),
    ("ym_li_yingwei", "ym_wang_tao", "上下级", "市委书记与副市长", "玉门市委/市政府", ""),
    ("ym_li_yingwei", "ym_zhang_xiaoyun", "上下级", "市委书记与副市长", "玉门市委/市政府", ""),
    ("ym_li_yingwei", "ym_yue_jianqiang", "上下级", "市委书记与副市长", "玉门市委/市政府", ""),
    ("ym_li_yingwei", "ym_zhang_tong", "上下级", "市委书记与副市长", "玉门市委/市政府", ""),
    ("ym_li_yingwei", "ym_ma_yujun", "上下级", "市委书记与副市长", "玉门市委/市政府", ""),
    ("ym_li_yingwei", "ym_bai_xuerui", "上下级", "市委书记与市领导", "玉门市委", ""),
    ("ym_li_yingwei", "ym_xie_xiang", "上下级", "市委书记与市领导", "玉门市委", ""),
    ("ym_li_yingwei", "ym_fan_zhijun", "上下级", "市委书记与市领导", "玉门市委", ""),
    ("ym_li_yingwei", "ym_wang_fei", "上下级", "市委书记与市领导", "玉门市委", ""),

    # 市长与副市长
    ("ym_wang_yingjun", "ym_zhao_chao", "上下级", "市长与常务副市长", "玉门市政府", ""),
    ("ym_wang_yingjun", "ym_shi_xianyong", "上下级", "市长与副市长", "玉门市政府", ""),
    ("ym_wang_yingjun", "ym_wang_tao", "上下级", "市长与副市长", "玉门市政府", ""),
    ("ym_wang_yingjun", "ym_zhang_xiaoyun", "上下级", "市长与副市长", "玉门市政府", ""),
    ("ym_wang_yingjun", "ym_yue_jianqiang", "上下级", "市长与副市长", "玉门市政府", ""),
    ("ym_wang_yingjun", "ym_zhang_tong", "上下级", "市长与副市长", "玉门市政府", ""),
    ("ym_wang_yingjun", "ym_ma_yujun", "上下级", "市长与副市长", "玉门市政府", ""),

    # 人大、政协与主要领导
    ("ym_li_yingwei", "ym_li_hong", "同僚", "市委书记与人大主任", "玉门市", ""),
    ("ym_li_yingwei", "ym_zhou_qin", "同僚", "市委书记与政协主席", "玉门市", ""),
    ("ym_li_yingwei", "ym_zhang_cunming", "同僚", "市委书记与政协党组书记", "玉门市", ""),

    # 继任关系
    ("ym_li_yingwei", "ym_hu_zhiyong", "继任", "接替胡志勇任玉门市委书记", "玉门市委", "2021-10"),
    ("ym_hu_zhiyong", "ym_chen_yanren", "继任", "接替陈炎人任玉门市委书记", "玉门市委", "2019-06"),
    ("ym_wang_yingjun", "ym_he_zhengjun", "继任", "接替何正军任玉门市长", "玉门市政府", "?"),

    # 跨地区干部流动
    ("ym_hu_zhiyong", "ym_he_zhengjun", "overlap", "胡志勇(书记)与何正军(市长): 党政搭档", "玉门市委/市政府", "2019-2021"),

    # 何正军跨区调动
    ("ym_he_zhengjun", "", "跨区调动", "从玉门市长调任肃州区委书记", "酒泉市", "~2019"),
    ("ym_he_zhengjun", "", "跨区调动", "从肃州区委书记升任酒泉市常务副市长", "酒泉市", "2023-12"),

    # 胡志勇跨市调动
    ("ym_hu_zhiyong", "", "跨市调动", "从玉门市委书记调任天水市副市长", "甘肃省", "2021-10"),
    ("ym_hu_zhiyong", "", "跨市调动", "从天水调任庆阳市长", "甘肃省", "2026"),
]


# ════════════════════════════════════════════
# CREATE DATABASE
# ════════════════════════════════════════════

def create_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE persons (
        id TEXT PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, native_place TEXT, education TEXT,
        party_join TEXT, work_start TEXT, current_post TEXT,
        current_org TEXT, source TEXT
    )""")
    c.execute("""CREATE TABLE organizations (
        id TEXT PRIMARY KEY, name TEXT, type TEXT, level TEXT,
        parent TEXT, location TEXT
    )""")
    c.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT, person_id TEXT, org_id TEXT,
        title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
        FOREIGN KEY(person_id) REFERENCES persons(id),
        FOREIGN KEY(org_id) REFERENCES organizations(id)
    )""")
    c.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT, person_a TEXT, person_b TEXT,
        type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT,
        FOREIGN KEY(person_a) REFERENCES persons(id),
        FOREIGN KEY(person_b) REFERENCES persons(id)
    )""")

    for p in PERSONS:
        c.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", p)

    for o in ORGANIZATIONS:
        c.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)", o)

    for pos in POSITIONS:
        # unpack: person_id, org_id, title, start, end, rank, note
        c.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)",
                  (pos[0], pos[1] if pos[1] else None, pos[2], pos[3], pos[4], pos[5], pos[6]))

    for r in RELATIONSHIPS:
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
                  (r[0], r[1] if r[1] else None, r[2], r[3], r[4], r[5]))

    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")

    # Stats
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for table in ["persons", "organizations", "positions", "relationships"]:
        c.execute(f"SELECT COUNT(*) FROM {table}")
        count = c.fetchone()[0]
        print(f"   {table}: {count} rows")
    conn.close()


# ════════════════════════════════════════════
# CREATE GEXF GRAPH
# ════════════════════════════════════════════

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(person_id):
    """Color by role."""
    top_leaders = ["ym_li_yingwei", "ym_wang_yingjun", "ym_hu_zhiyong", "ym_he_zhengjun"]
    gov_leaders = ["ym_zhao_chao", "ym_shi_xianyong", "ym_wang_tao", "ym_zhang_xiaoyun",
                   "ym_yue_jianqiang", "ym_zhang_tong", "ym_ma_yujun"]
    discipline = ["ym_zhang_ji"]
    congress = ["ym_li_hong"]
    cppcc = ["ym_zhou_qin", "ym_zhang_cunming"]

    if person_id in top_leaders:
        return "255,50,50"  # Red - Party Secretary / Government Head
    elif person_id in gov_leaders:
        return "100,100,200"  # Light blue - Deputy Mayor
    elif person_id in discipline:
        return "255,165,0"  # Orange - Discipline
    elif person_id in congress:
        return "200,255,255"  # Cyan - People's Congress
    elif person_id in cppcc:
        return "255,240,200"  # Cream - CPPCC
    else:
        return "200,100,100"  # Pink - Other Standing Committee


def is_top_leader(person_id):
    return person_id in ["ym_li_yingwei", "ym_wang_yingjun", "ym_li_hong", "ym_zhou_qin"]


def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "纪委": "255,200,200",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "党委部门": "255,200,200",
    }
    return colors.get(org_type, "200,200,200")


def create_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>玉门市（酒泉市）领导班子工作关系网络 — 2026年7月</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('    </attributes>')

    # Persons as nodes
    lines.append('    <nodes>')
    for p in PERSONS:
        pid = p[0]
        name = p[1]
        role = p[10]  # current_post
        c = person_color(pid)
        sz = "20.0" if is_top_leader(pid) else "12.0"
        lines.append(f'      <node id="p{pid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    # Orgs as nodes
    for o in ORGANIZATIONS:
        oid = o[0]
        oname = o[1]
        otype = o[2]
        c = org_color(otype)
        lines.append(f'      <node id="o{oid}" label="{esc(oname)}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(otype)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization (worked_at)
    for pos in POSITIONS:
        pid = pos[0]
        oid = pos[1]
        title = pos[2]
        if not oid:
            continue
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pid}" target="o{oid}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ Person (relationship)
    for r in RELATIONSHIPS:
        pa = r[0]
        pb = r[1]
        rtype = r[2]
        context = r[3]
        if not pb:
            continue
        eid += 1
        weight = "2.0"
        lines.append(f'      <edge id="e{eid}" source="p{pa}" target="p{pb}" label="{esc(rtype)}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF created: {GEXF_PATH}")


# ════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 50)
    print("玉门市领导班子工作关系网络 — 数据构建")
    print("=" * 50)
    create_database()
    create_gexf()
    print("\n✅ Done. All artifacts generated in staging:")
    print(f"   DB:    {DB_PATH}")
    print(f"   GEXF:  {GEXF_PATH}")
