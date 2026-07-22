#!/usr/bin/env python3
"""
肃州区（酒泉市）领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Suzhou District leadership.

Level: 市辖区 — 县级
Province: 甘肃省
Parent City: 酒泉市
Region: 肃州区
Targets: 区委书记 & 区长

Research Sources:
- 肃州区人民政府官网 (www.jqsz.gov.cn) — 领导简历页 (primary, 2026-07确认)
- 酒泉市人民政府官网 (www.jiuquan.gov.cn) — 领导之窗
- build_酒泉市_data.py — 市级已有数据
- 百度百科 — 李生潜履历 (确认)
- 新闻报道 (腾讯新闻、澎湃新闻、每日甘肃网等)
- 任前公示

Research Date: 2026-07-22
"""

import sqlite3
import os
import json
from datetime import datetime

# ── PATHS ──
BASE = "/workspace/data/xieming/other-codes/gov-relation"
STAGING = os.path.join(BASE, "data/tmp/gansu_肃州区")
os.makedirs(STAGING, exist_ok=True)

DB_PATH = os.path.join(STAGING, "肃州区_network.db")
GEXF_PATH = os.path.join(STAGING, "肃州区_network.gexf")

# ════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════

# Person IDs use format: szq_{surname}{givenname} (szq = SuzhouQu)
PERSONS = [
    # id, name, gender, ethnicity, birth, birthplace, native_place,
    # education, party_join, work_start, current_post, current_org, source

    # ═══════════════════════════════════
    # 区委领导班子
    # ═══════════════════════════════════

    # 李生潜 — 市委常委、区委书记 (as of 2026-07)
    ("szq_li_shengqian", "李生潜", "男", "汉族", "1980年12月", "甘肃民乐", "甘肃民乐",
     "全日制本科学历，工学学士（甘肃农业大学农田水利工程专业）", "中共党员", "2004年7月",
     "酒泉市委常委、肃州区委书记",
     "中共肃州区委员会",
     "jqsz.gov.cn;baike.baidu.com;qq.com"),

    # 何正军 — 前任区委书记 (approx 2019-2024), 现任酒泉市人大常委会副主任
    ("szq_he_zhengjun", "何正军", "男", "汉族", "1967年12月", "甘肃金塔", "甘肃金塔",
     "省委党校研究生/文学学士", "中共党员", "1987年7月",
     "酒泉市人大常委会副主任",
     "酒泉市人民代表大会常务委员会",
     "build_酒泉市_data.py;thepaper.cn"),

    # 张鸿 — 更早前任区委书记 (~2015-2019), 现任甘肃省民政厅副厅长
    ("szq_zhang_hong", "张鸿", "男", "汉族", "1968年11月", "甘肃张掖", "甘肃张掖",
     "待查", "中共党员", "待查",
     "甘肃省民政厅党组成员、副厅长",
     "甘肃省民政厅",
     "baike.baidu.com"),

    # ═══════════════════════════════════
    # 区政府领导班子
    # ═══════════════════════════════════

    # 宋济民 — 区委副书记、区长 (as of 2026-07)
    ("szq_song_jimin", "宋济民", "男", "汉族", "1981年1月", "甘肃敦煌", "甘肃敦煌",
     "在职研究生学历", "中共党员", "待查",
     "肃州区委副书记、区长",
     "肃州区人民政府",
     "jqsz.gov.cn"),

    # 王永宏 — 前任区长 (2019.02-2023.07), 去向未公开
    ("szq_wang_yonghong", "王永宏", "男", "汉族", "待查", "甘肃金塔", "甘肃金塔",
     "待查", "中共党员", "待查",
     "（前任肃州区区长，2023年7月调离，去向待查）",
     "待查",
     "百度;搜狐;酒泉市人大常委会公告"),

    # ═══════════════════════════════════
    # 区政府副区长（7人）
    # ═══════════════════════════════════

    # 赵占龙 — 区委常委、常务副区长
    ("szq_zhao_zhanlong", "赵占龙", "男", "汉族", "1979年1月", "待查", "待查",
     "在职研究生学历", "中共党员", "待查",
     "肃州区委常委、区政府党组副书记、常务副区长",
     "肃州区人民政府",
     "jqsz.gov.cn"),

    # 高明 — 区委常委、副区长
    ("szq_gao_ming", "高明", "男", "汉族", "1975年1月", "待查", "待查",
     "在职研究生学历", "中共党员", "待查",
     "肃州区委常委、区政府党组成员",
     "肃州区人民政府",
     "jqsz.gov.cn"),

    # 乔世祥 — 副区长
    ("szq_qiao_shixiang", "乔世祥", "男", "汉族", "1979年5月", "待查", "待查",
     "在职大学学历", "中共党员", "待查",
     "肃州区政府党组成员、副区长",
     "肃州区人民政府",
     "jqsz.gov.cn"),

    # 张建武 — 副区长、公安分局局长
    ("szq_zhang_jianwu", "张建武", "男", "汉族", "1977年5月", "待查", "待查",
     "在职大学学历", "中共党员", "待查",
     "肃州区政府党组成员、副区长、酒泉市公安局肃州分局局长",
     "酒泉市公安局肃州分局",
     "jqsz.gov.cn"),

    # 刘琨 — 副区长
    ("szq_liu_kun", "刘琨", "男", "汉族", "1985年4月", "待查", "待查",
     "大学本科学历，理学学士", "中共党员", "待查",
     "肃州区政府党组成员、副区长",
     "肃州区人民政府",
     "jqsz.gov.cn"),

    # 崔丰玲 — 副区长（女）
    ("szq_cui_fengling", "崔丰玲", "女", "汉族", "1981年9月", "待查", "待查",
     "在职大学学历", "中共党员", "待查",
     "肃州区人民政府副区长",
     "肃州区人民政府",
     "jqsz.gov.cn"),

    # 马立山 — 副区长
    ("szq_ma_lishan", "马立山", "男", "汉族", "1985年12月", "待查", "待查",
     "全日制大学学历，管理学学士", "中共党员", "待查",
     "肃州区政府党组成员、副区长",
     "肃州区人民政府",
     "jqsz.gov.cn"),

    # ═══════════════════════════════════
    # 区委常委（从新闻报道中提取）
    # ═══════════════════════════════════

    # 周开东 — 区委领导（具体职务待确认）
    ("szq_zhou_kaidong", "周开东", "男", "汉族", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "肃州区委领导（常委）",
     "中共肃州区委员会",
     "jqsz.gov.cn会议报道"),

    # 詹青芳 — 区纪委书记（通报政绩观偏差典型案例）
    ("szq_zhan_qingfang", "詹青芳", "男", "汉族", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "肃州区委常委、纪委书记、监委主任",
     "中共肃州区纪律检查委员会",
     "jqsz.gov.cn"),

    # 李玉 — 区委领导（常委）
    ("szq_li_yu", "李玉", "男", "汉族", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "肃州区委领导（常委）",
     "中共肃州区委员会",
     "jqsz.gov.cn会议报道"),

    # 王斌 — 区委领导（常委）
    ("szq_wang_bin", "王斌", "男", "汉族", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "肃州区委领导（常委）",
     "中共肃州区委员会",
     "jqsz.gov.cn会议报道"),

    # 武占鑫 — 区委领导（常委）
    ("szq_wu_zhanxin", "武占鑫", "男", "汉族", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "肃州区委领导（常委）",
     "中共肃州区委员会",
     "jqsz.gov.cn会议报道"),

    # 程景峰 — 区委领导（常委）
    ("szq_cheng_jingfeng", "程景峰", "男", "汉族", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "肃州区委领导（常委）",
     "中共肃州区委员会",
     "jqsz.gov.cn会议报道"),

    # ═══════════════════════════════════
    # 人大、政协
    # ═══════════════════════════════════

    # 王德文 — 区人大常委会党组书记、主任候选人
    ("szq_wang_edewen", "王德文", "男", "汉族", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "肃州区人大常委会党组书记、主任候选人",
     "肃州区人民代表大会常务委员会",
     "jqsz.gov.cn"),

    # 裴青山 — 区领导（可能是区政协主席）
    ("szq_pei_qingshan", "裴青山", "男", "汉族", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "肃州区领导（主席/政协？）",
     "肃州区",
     "jqsz.gov.cn会议报道"),

    # 王立明 — 区领导
    ("szq_wang_liming", "王立明", "男", "汉族", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "肃州区领导",
     "肃州区",
     "jqsz.gov.cn会议报道"),

    # 刘倩 — 区委领导（常委、宣传部部长推测）
    ("szq_liu_qian", "刘倩", "女", "汉族", "待查", "待查", "待查",
     "待查", "中共党员", "待查",
     "肃州区委领导（常委）",
     "中共肃州区委员会",
     "2026年区委党的建设工作领导小组会议"),
]

ORGANIZATIONS = [
    # id, name, type, level, parent, location
    ("szq_party_committee", "中共肃州区委员会", "党委", "县级", "中共酒泉市委员会", "酒泉市肃州区"),
    ("szq_gov", "肃州区人民政府", "政府", "县级", "酒泉市人民政府", "酒泉市肃州区"),
    ("szq_discipline", "中共肃州区纪律检查委员会", "纪委", "县级", "中共酒泉市纪律检查委员会", "酒泉市肃州区"),
    ("szq_public_security", "酒泉市公安局肃州分局", "政府", "正科级", "酒泉市公安局", "酒泉市肃州区"),
    ("szq_people_congress", "肃州区人民代表大会常务委员会", "人大", "县级", "酒泉市人大常委会", "酒泉市肃州区"),
    ("szq_cppcc", "中国人民政治协商会议肃州区委员会", "政协", "县级", "酒泉市政协", "酒泉市肃州区"),
    ("szq_party_org", "中共肃州区委组织部", "党委部门", "正科级", "中共肃州区委员会", "酒泉市肃州区"),
    ("szq_propaganda", "中共肃州区委宣传部", "党委部门", "正科级", "中共肃州区委员会", "酒泉市肃州区"),
    ("szq_united_front", "中共肃州区委统一战线工作部", "党委部门", "正科级", "中共肃州区委员会", "酒泉市肃州区"),
    ("szq_political_legal", "中共肃州区委政法委员会", "党委部门", "正科级", "中共肃州区委员会", "酒泉市肃州区"),
]

POSITIONS = [
    # person_id, org_id, title, start, end, rank, note

    # ═══ 李生潜 — 区委书记 ═══
    ("szq_li_shengqian", "szq_party_committee", "肃州区委书记", "2024-01", "至今", "副厅级", "兼任酒泉市委常委；主持区委全面工作"),
    ("szq_li_shengqian", "", "酒泉市委常委", "2022-11", "至今", "副厅级", "晋升市委常委"),
    ("szq_li_shengqian", "", "酒泉市委秘书长", "2022-11", "2024-01", "副厅级", "兼任市委秘书长"),
    ("szq_li_shengqian", "", "酒泉市副市长", "2021-09", "2022-11", "副厅级", "从省水利厅空降酒泉"),
    ("szq_li_shengqian", "", "甘肃省水利厅河湖管理处处长", "2020-02", "2021-09", "正处级", ""),
    ("szq_li_shengqian", "", "甘肃省水利厅水资源处处长", "2019-05", "2020-02", "正处级", ""),
    ("szq_li_shengqian", "", "石羊河流域水资源局党委书记、局长", "2017-07", "2019-05", "正处级", "2019.03-05省委党校中青班"),
    ("szq_li_shengqian", "", "石羊河流域水资源局局长", "2017-03", "2017-07", "正处级", ""),
    ("szq_li_shengqian", "", "甘肃省水利厅财务处副处长", "2012-11", "2017-03", "副处级", ""),
    ("szq_li_shengqian", "", "甘肃省水利厅造价规费中心计划统计科科长", "2010-02", "2012-11", "正科级", ""),
    ("szq_li_shengqian", "", "甘肃省水利厅牧区水利工作队助理工程师/工程师", "2004-07", "2010-02", "", "省水利系统"),

    # ═══ 何正军 — 前任区委书记 ═══
    ("szq_he_zhengjun", "szq_people_congress", "酒泉市人大常委会副主任", "2025-10", "至今", "副厅级", "现任"),
    ("szq_he_zhengjun", "", "酒泉市委常委、常务副市长", "2023-12", "2025-09", "副厅级", ""),
    ("szq_he_zhengjun", "szq_party_committee", "肃州区委书记", "2019?", "2024-01", "副厅级", "兼任市委常委"),
    ("szq_he_zhengjun", "", "玉门市委副书记、市长", "?", "?", "正处级", "前职"),
    ("szq_he_zhengjun", "", "阿克塞县委副书记、人大常委会主任", "?", "?", "正处级", "前职"),

    # ═══ 张鸿 — 更早前任区委书记 ═══
    ("szq_zhang_hong", "", "甘肃省民政厅党组成员、副厅长", "?", "至今", "副厅级", "现任"),
    ("szq_zhang_hong", "", "酒泉市委常委、常务副市长", "?", "?", "副厅级", ""),
    ("szq_zhang_hong", "szq_party_committee", "肃州区委书记", "~2015", "~2019", "副厅级", ""),

    # ═══ 宋济民 — 区长 ═══
    ("szq_song_jimin", "szq_gov", "肃州区委副书记、区长", "2023-07", "至今", "正处级", "主持区政府全面工作"),
    ("szq_song_jimin", "", "酒泉市水务局局长", "2022-03", "2023-07", "正处级", "前职"),
    ("szq_song_jimin", "", "敦煌市委常委、统战部部长", "2020", "2022", "副处级", ""),
    ("szq_song_jimin", "", "敦煌市副市长", "2016", "2020", "副处级", ""),

    # ═══ 王永宏 — 前任区长 ═══
    ("szq_wang_yonghong", "szq_gov", "肃州区区长", "2019-02", "2023-07", "正处级", "2023年7月调离，去向待查"),

    # ═══ 赵占龙 — 常务副区长 ═══
    ("szq_zhao_zhanlong", "szq_gov", "肃州区委常委、常务副区长", "", "至今", "副处级", "负责政府常务工作"),

    # ═══ 高明 — 副区长 ═══
    ("szq_gao_ming", "szq_gov", "肃州区委常委、副区长", "", "至今", "副处级", "负责农业农村等工作"),

    # ═══ 乔世祥 — 副区长 ═══
    ("szq_qiao_shixiang", "szq_gov", "肃州区政府党组成员、副区长", "", "至今", "副处级", "负责自然资源、城建、民政等"),

    # ═══ 张建武 — 副区长、公安局长 ═══
    ("szq_zhang_jianwu", "szq_public_security", "肃州区政府党组成员、副区长、公安分局局长", "", "至今", "副处级", "负责公安、司法、信访等"),
    ("szq_zhang_jianwu", "szq_gov", "肃州区政府党组成员、副区长", "", "至今", "副处级", ""),

    # ═══ 刘琨 — 副区长 ═══
    ("szq_liu_kun", "szq_gov", "肃州区政府党组成员、副区长", "", "至今", "副处级", "负责人社、教育、卫健、文旅等"),

    # ═══ 崔丰玲 — 副区长 ═══
    ("szq_cui_fengling", "szq_gov", "肃州区人民政府副区长", "", "至今", "副处级", "负责发改、工信、商务等"),

    # ═══ 马立山 — 副区长 ═══
    ("szq_ma_lishan", "szq_gov", "肃州区政府党组成员、副区长", "", "至今", "副处级", "负责环保、政务公开、数据等"),

    # ═══ 区委常委 ═══
    ("szq_zhan_qingfang", "szq_discipline", "肃州区委常委、纪委书记、监委主任", "", "至今", "副处级", ""),
    ("szq_zhou_kaidong", "szq_party_committee", "肃州区委常委", "", "至今", "副处级", ""),
    ("szq_li_yu", "szq_party_committee", "肃州区委常委", "", "至今", "副处级", ""),
    ("szq_wang_bin", "szq_party_committee", "肃州区委常委", "", "至今", "副处级", ""),
    ("szq_wu_zhanxin", "szq_party_committee", "肃州区委常委", "", "至今", "副处级", ""),
    ("szq_cheng_jingfeng", "szq_party_committee", "肃州区委常委", "", "至今", "副处级", ""),

    # ═══ 人大、政协 ═══
    ("szq_wang_edewen", "szq_people_congress", "肃州区人大常委会党组书记、主任候选人", "", "至今", "正处级", ""),
    ("szq_pei_qingshan", "szq_cppcc", "肃州区领导（推测政协主席）", "", "至今", "正处级", "待确认具体职务"),
    ("szq_wang_liming", "szq_party_committee", "肃州区领导", "", "至今", "", "待确认具体职务"),
    ("szq_liu_qian", "szq_propaganda", "肃州区委常委、宣传部部长(推测)", "", "至今", "副处级", "待确认"),
]

RELATIONSHIPS = [
    # person_a, person_b, type, context, overlap_org, overlap_period

    # 党政搭档
    ("szq_li_shengqian", "szq_song_jimin", "党政搭档", "区委书记与区长，共同领导肃州区", "肃州区委/区政府", "2024-至今"),

    # 继任关系
    ("szq_li_shengqian", "szq_he_zhengjun", "继任", "接替何正军任肃州区委书记", "肃州区委", "2024-01"),
    ("szq_he_zhengjun", "szq_zhang_hong", "继任", "接替张鸿任肃州区委书记", "肃州区委", "~2019"),
    ("szq_song_jimin", "szq_wang_yonghong", "继任", "接替王永宏任肃州区区长", "肃州区政府", "2023-07"),

    # 上下级关系
    ("szq_song_jimin", "szq_zhao_zhanlong", "上下级", "区长与常务副区长", "肃州区政府", ""),
    ("szq_song_jimin", "szq_gao_ming", "上下级", "区长与副区长", "肃州区政府", ""),
    ("szq_song_jimin", "szq_qiao_shixiang", "上下级", "区长与副区长", "肃州区政府", ""),
    ("szq_song_jimin", "szq_zhang_jianwu", "上下级", "区长与副区长", "肃州区政府", ""),
    ("szq_song_jimin", "szq_liu_kun", "上下级", "区长与副区长", "肃州区政府", ""),
    ("szq_song_jimin", "szq_cui_fengling", "上下级", "区长与副区长", "肃州区政府", ""),
    ("szq_song_jimin", "szq_ma_lishan", "上下级", "区长与副区长", "肃州区政府", ""),

    # 常委同僚
    ("szq_li_shengqian", "szq_zhan_qingfang", "同僚", "区委书记与纪委书记", "肃州区委", ""),
    ("szq_li_shengqian", "szq_zhou_kaidong", "同僚", "区委书记与区委常委", "肃州区委", ""),
    ("szq_li_shengqian", "szq_li_yu", "同僚", "区委书记与区委常委", "肃州区委", ""),
    ("szq_li_shengqian", "szq_wang_bin", "同僚", "区委书记与区委常委", "肃州区委", ""),
    ("szq_li_shengqian", "szq_wu_zhanxin", "同僚", "区委书记与区委常委", "肃州区委", ""),
    ("szq_li_shengqian", "szq_cheng_jingfeng", "同僚", "区委书记与区委常委", "肃州区委", ""),

    # 跨区调动 — 李生潜从省水利厅空降酒泉
    ("szq_li_shengqian", "", "省厅到地方", "从省水利厅调任酒泉市副市长", "酒泉市", "2021-09"),
    # 宋济民从敦煌调任肃州
    ("szq_song_jimin", "", "跨区调动", "从敦煌市调任酒泉市水务局，后任肃州区区长", "酒泉市", "2022-2023"),
    # 何正军从玉门调任肃州
    ("szq_he_zhengjun", "", "跨区调动", "从玉门市长调任肃州区委书记", "酒泉市", "2019"),
    # 张鸿从肃州到酒泉市再到省厅
    ("szq_zhang_hong", "", "跨区调动", "肃州区委书记→酒泉市委常委→甘肃省民政厅", "酒泉市/甘肃省", ""),
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
    top_leaders = ["szq_li_shengqian", "szq_he_zhengjun", "szq_zhang_hong"]
    gov_leaders = ["szq_song_jimin", "szq_wang_yonghong"]
    discipline = ["szq_zhan_qingfang"]

    if person_id in top_leaders:
        return "255,50,50"  # Red - Party Secretary
    elif person_id in gov_leaders:
        return "50,100,255"  # Blue - Government
    elif person_id in discipline:
        return "255,165,0"  # Orange - Discipline
    else:
        return "100,100,100"  # Grey - Others

def is_top_leader(person_id):
    return person_id in ["szq_li_shengqian", "szq_song_jimin", "szq_he_zhengjun"]

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
    lines.append('    <description>肃州区（酒泉市）领导班子工作关系网络 — 2026年7月</description>')
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
    print("肃州区领导班子工作关系网络 — 数据构建")
    print("=" * 50)
    create_database()
    create_gexf()
    print("\n✅ Done. All artifacts generated in staging:")
    print(f"   DB:    {DB_PATH}")
    print(f"   GEXF:  {GEXF_PATH}")
