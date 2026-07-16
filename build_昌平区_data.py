#!/usr/bin/env python3
"""
北京市昌平区领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Changping District leadership.

Level: 市辖区(直辖市) — 正厅级
Province: 北京市
Targets: 区委书记 & 区长

Sources:
- bjchp.gov.cn (official leadership pages, accessed 2026-07-16)
- build_东城区_data.py (周金星 predecessor info)

Data as of: 2026-06-12 (official page update date: 2026-06-12)
"""

import sqlite3
import os
from datetime import datetime

# ── PATHS ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "昌平区_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "昌平区_network.gexf")

# ════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════

PERSONS = [
    # id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source

    # ── 区委班子（10人） ──
    ("cp_gan_jingzhong", "甘靖中", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委书记，未来科学城党工委书记（兼）", "中共北京市昌平区委员会",
     "bjchp.gov.cn/official"),

    ("cp_liu_xiaodong", "刘晓东", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委副书记，区政府党组书记、区长，未来科学城党工委副书记、管委会主任（兼）", "北京市昌平区人民政府",
     "bjchp.gov.cn/official"),

    ("cp_leng_qiangtian", "冷强田", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委副书记，区直机关工委书记，区委党校校长、区行政学院院长", "中共北京市昌平区委员会",
     "bjchp.gov.cn/official"),

    ("cp_chen_xiang", "陈祥", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、宣传部部长", "中共北京市昌平区委宣传部",
     "bjchp.gov.cn/official"),

    ("cp_zhang_qingwu", "张庆武", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、组织部部长", "中共北京市昌平区委组织部",
     "bjchp.gov.cn/official"),

    ("cp_ma_qiang", "马强", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、政法委书记", "中共北京市昌平区委政法委员会",
     "bjchp.gov.cn/official"),

    ("cp_guo_qingyao", "郭清尧", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、统战部部长，区政协党组副书记（兼）", "中共北京市昌平区委统战部",
     "bjchp.gov.cn/official"),

    ("cp_li_shugen", "李树根", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委，区人民武装部部长", "北京市昌平区人民武装部",
     "bjchp.gov.cn/official"),

    ("cp_liu_qiang", "柳强", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委，区政府党组成员、副区长，区委中关村科技园区昌平园工委书记", "北京市昌平区人民政府",
     "bjchp.gov.cn/official"),

    ("cp_ma_yajun", "马亚军", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区委常委、区纪委书记，区监察委员会主任，未来科学城党工委委员、纪检监察工委书记（兼）", "中共北京市昌平区纪律检查委员会",
     "bjchp.gov.cn/official"),

    # ── 区政府副区长（不含常委兼任） ──
    ("cp_ma_chunxiu", "马春秀", "女", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政府副区长，区工商联主席，区红十字会会长", "北京市昌平区人民政府",
     "bjchp.gov.cn/official"),

    ("cp_wang_weiguo", "王卫国", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政府党组成员、副区长，区委政法委副书记，市公安局昌平分局党委书记、局长", "北京市公安局昌平分局",
     "bjchp.gov.cn/official"),

    ("cp_lei_hailiang", "雷海良", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政府党组成员、副区长", "北京市昌平区人民政府",
     "bjchp.gov.cn/official"),

    ("cp_lin_yu", "林宇", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政府党组成员、副区长，区委政法委副书记", "北京市昌平区人民政府",
     "bjchp.gov.cn/official"),

    ("cp_zhang_shuo", "张硕", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政府党组成员、副区长", "北京市昌平区人民政府",
     "bjchp.gov.cn/official"),

    ("cp_zhao_shiwei", "赵仕伟", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "未来科学城党工委委员、管委会副主任，区政府党组成员、副区长（兼）", "北京未来科学城管理委员会",
     "bjchp.gov.cn/official"),

    ("cp_cui_di", "崔迪", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政府副区长（挂职）", "北京市昌平区人民政府",
     "bjchp.gov.cn/official"),

    ("cp_su_dalin", "苏大林", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政府副区长（挂职）", "北京市昌平区人民政府",
     "bjchp.gov.cn/official"),

    # ── 区人大主要领导 ──
    ("cp_wang_yanqing", "王燕庆", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区人大常委会党组书记、主任", "北京市昌平区人民代表大会常务委员会",
     "bjchp.gov.cn/official"),

    ("cp_bai_xiangjun", "白向军", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区人大常委会党组副书记、副主任，区总工会主席", "北京市昌平区人民代表大会常务委员会",
     "bjchp.gov.cn/official"),

    ("cp_shi_youmin", "史佑民", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区人大常委会党组成员、副主任，区委组织部分管日常工作的副部长", "北京市昌平区人民代表大会常务委员会",
     "bjchp.gov.cn/official"),

    ("cp_wang_jun", "王军", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区人大常委会党组成员、副主任", "北京市昌平区人民代表大会常务委员会",
     "bjchp.gov.cn/official"),

    ("cp_li_xin", "李欣", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区人大常委会党组成员、副主任", "北京市昌平区人民代表大会常务委员会",
     "bjchp.gov.cn/official"),

    ("cp_li_jiqing", "李继清", "女", "汉族", "待查", "待查",
     "待查", "民盟盟员", "待查",
     "区人大常委会副主任（不驻会）", "北京市昌平区人民代表大会常务委员会",
     "bjchp.gov.cn/official"),

    # ── 区政协主要领导 ──
    ("cp_jiang_dafeng", "蒋达峰", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政协党组书记、主席", "中国人民政治协商会议北京市昌平区委员会",
     "bjchp.gov.cn/official"),

    ("cp_wang_zhigang", "王志刚", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政协党组副书记、副主席", "中国人民政治协商会议北京市昌平区委员会",
     "bjchp.gov.cn/official"),

    ("cp_wang_jian2", "王建", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政协党组成员、副主席，区委教育工委书记", "中国人民政治协商会议北京市昌平区委员会",
     "bjchp.gov.cn/official"),

    ("cp_ning_che", "宁澈", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政协党组成员、副主席", "中国人民政治协商会议北京市昌平区委员会",
     "bjchp.gov.cn/official"),

    ("cp_li_xuehong", "李雪红", "女", "汉族", "待查", "待查",
     "待查", "民革党员", "待查",
     "区政协副主席（不驻会）", "中国人民政治协商会议北京市昌平区委员会",
     "bjchp.gov.cn/official"),

    ("cp_wang_libing", "王立兵", "男", "汉族", "待查", "待查",
     "待查", "农工党党员", "待查",
     "区政协副主席（不驻会）", "中国人民政治协商会议北京市昌平区委员会",
     "bjchp.gov.cn/official"),

    ("cp_bao_zhihua", "鲍志华", "男", "汉族", "待查", "待查",
     "待查", "民进会员", "待查",
     "区政协副主席（不驻会）", "中国人民政治协商会议北京市昌平区委员会",
     "bjchp.gov.cn/official"),

    # ── 前主要领导 ──
    ("cp_zhou_jinxing", "周金星", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "前任区委书记（原东城区区长调任）", "中共北京市昌平区委员会（已离任）",
     "build_东城区_data.py"),
]

ORGANIZATIONS = [
    # id, name, type, level, parent, location
    ("cp_party_committee", "中共北京市昌平区委员会", "党委", "地厅级", "中共北京市委", "北京市昌平区"),
    ("cp_gov", "北京市昌平区人民政府", "政府", "地厅级", "北京市人民政府", "北京市昌平区"),
    ("cp_org_department", "中共北京市昌平区委组织部", "党委部门", "正处级", "昌平区委", "北京市昌平区"),
    ("cp_discipline", "中共北京市昌平区纪律检查委员会", "纪委", "地厅级", "北京市纪委监委", "北京市昌平区"),
    ("cp_propaganda", "中共北京市昌平区委宣传部", "党委部门", "正处级", "昌平区委", "北京市昌平区"),
    ("cp_united_front", "中共北京市昌平区委统战部", "党委部门", "正处级", "昌平区委", "北京市昌平区"),
    ("cp_political_legal", "中共北京市昌平区委政法委员会", "党委部门", "正处级", "昌平区委", "北京市昌平区"),
    ("cp_party_school", "中共北京市昌平区委党校", "党委部门", "正处级", "昌平区委", "北京市昌平区"),
    ("cp_public_security", "北京市公安局昌平分局", "公安", "正处级", "北京市公安局", "北京市昌平区"),
    ("cp_military_department", "北京市昌平区人民武装部", "军队", "正处级", "北京卫戍区", "北京市昌平区"),
    ("cp_future_science_city", "北京未来科学城管理委员会", "开发区", "正厅级", "北京市人民政府", "北京市昌平区"),
    ("cp_peoples_congress", "北京市昌平区人民代表大会常务委员会", "人大", "地厅级", "北京市人大常委会", "北京市昌平区"),
    ("cp_cppcc", "中国人民政治协商会议北京市昌平区委员会", "政协", "地厅级", "北京市政协", "北京市昌平区"),
]

POSITIONS = [
    # person_id, org_id, title, start, end, rank, note

    # ═══ 甘靖中 — 区委书记 ═══
    ("cp_gan_jingzhong", "cp_party_committee", "区委书记", "待查", "至今", "正厅级", "主持区委全面工作，兼未来科学城党工委书记"),
    ("cp_gan_jingzhong", "cp_future_science_city", "未来科学城党工委书记（兼）", "待查", "至今", "正厅级", "兼任"),

    # ═══ 刘晓东 — 区长 ═══
    ("cp_liu_xiaodong", "cp_gov", "区长", "待查", "至今", "正厅级", "主持区政府全面工作"),
    ("cp_liu_xiaodong", "cp_party_committee", "区委副书记", "待查", "至今", "正厅级", "兼任"),
    ("cp_liu_xiaodong", "cp_future_science_city", "未来科学城党工委副书记、管委会主任（兼）", "待查", "至今", "正厅级", "兼任"),

    # ═══ 冷强田 — 区委副书记 ═══
    ("cp_leng_qiangtian", "cp_party_committee", "区委副书记", "待查", "至今", "正厅级", "分管党建/党校/机关工委"),
    ("cp_leng_qiangtian", "cp_party_school", "区委党校校长、区行政学院院长（兼）", "待查", "至今", "正厅级", "兼任"),

    # ═══ 陈祥 — 宣传部长 ═══
    ("cp_chen_xiang", "cp_propaganda", "区委常委、宣传部部长", "待查", "至今", "副厅级", ""),

    # ═══ 张庆武 — 组织部长 ═══
    ("cp_zhang_qingwu", "cp_org_department", "区委常委、组织部部长", "待查", "至今", "副厅级", ""),

    # ═══ 马强 — 政法委书记 ═══
    ("cp_ma_qiang", "cp_political_legal", "区委常委、政法委书记", "待查", "至今", "副厅级", ""),

    # ═══ 郭清尧 — 统战部长 ═══
    ("cp_guo_qingyao", "cp_united_front", "区委常委、统战部部长", "待查", "至今", "副厅级", "兼政协党组副书记"),
    ("cp_guo_qingyao", "cp_cppcc", "区政协党组副书记（兼）", "待查", "至今", "副厅级", ""),

    # ═══ 李树根 — 武装部长 ═══
    ("cp_li_shugen", "cp_military_department", "区委常委、区人民武装部部长", "待查", "至今", "正团级", ""),

    # ═══ 柳强 — 常委/副区长 ═══
    ("cp_liu_qiang", "cp_gov", "区委常委、副区长", "待查", "至今", "副厅级", "兼区委中关村科技园区昌平园工委书记"),

    # ═══ 马亚军 — 纪委书记 ═══
    ("cp_ma_yajun", "cp_discipline", "区委常委、区纪委书记、区监委主任", "待查", "至今", "副厅级", "兼未来科学城纪检监察工委书记"),
    ("cp_ma_yajun", "cp_future_science_city", "未来科学城党工委委员、纪检监察工委书记（兼）", "待查", "至今", "副厅级", ""),

    # ═══ 副区长们 ═══
    ("cp_ma_chunxiu", "cp_gov", "副区长", "待查", "至今", "副厅级", "兼区工商联主席、红十字会会长"),
    ("cp_wang_weiguo", "cp_gov", "副区长、区公安分局局长", "待查", "至今", "副厅级", "兼区委政法委副书记"),
    ("cp_wang_weiguo", "cp_public_security", "市公安局昌平分局党委书记、局长", "待查", "至今", "副厅级", ""),
    ("cp_lei_hailiang", "cp_gov", "副区长", "待查", "至今", "副厅级", ""),
    ("cp_lin_yu", "cp_gov", "副区长", "待查", "至今", "副厅级", "兼区委政法委副书记"),
    ("cp_zhang_shuo", "cp_gov", "副区长", "待查", "至今", "副厅级", ""),
    ("cp_zhao_shiwei", "cp_future_science_city", "未来科学城管委会副主任（兼）", "待查", "至今", "副厅级", ""),
    ("cp_zhao_shiwei", "cp_gov", "副区长（兼）", "待查", "至今", "副厅级", ""),
    ("cp_cui_di", "cp_gov", "副区长（挂职）", "待查", "至今", "副厅级", ""),
    ("cp_su_dalin", "cp_gov", "副区长（挂职）", "待查", "至今", "副厅级", ""),

    # ═══ 人大 ═══
    ("cp_wang_yanqing", "cp_peoples_congress", "区人大常委会主任", "待查", "至今", "正厅级", ""),
    ("cp_bai_xiangjun", "cp_peoples_congress", "区人大常委会副主任", "待查", "至今", "副厅级", "兼区总工会主席"),
    ("cp_shi_youmin", "cp_peoples_congress", "区人大常委会副主任", "待查", "至今", "副厅级", "兼区委组织部分管日常工作的副部长"),
    ("cp_wang_jun", "cp_peoples_congress", "区人大常委会副主任", "待查", "至今", "副厅级", ""),
    ("cp_li_xin", "cp_peoples_congress", "区人大常委会副主任", "待查", "至今", "副厅级", ""),
    ("cp_li_jiqing", "cp_peoples_congress", "区人大常委会副主任（不驻会）", "待查", "至今", "副厅级", "民盟/教授"),

    # ═══ 政协 ═══
    ("cp_jiang_dafeng", "cp_cppcc", "区政协主席", "待查", "至今", "正厅级", ""),
    ("cp_wang_zhigang", "cp_cppcc", "区政协副主席", "待查", "至今", "副厅级", ""),
    ("cp_wang_jian2", "cp_cppcc", "区政协副主席", "待查", "至今", "副厅级", "兼区委教育工委书记"),
    ("cp_ning_che", "cp_cppcc", "区政协副主席", "待查", "至今", "副厅级", ""),
    ("cp_li_xuehong", "cp_cppcc", "区政协副主席（不驻会）", "待查", "至今", "副厅级", "民革/科协"),
    ("cp_wang_libing", "cp_cppcc", "区政协副主席（不驻会）", "待查", "至今", "副厅级", "农工党/市场监管局"),
    ("cp_bao_zhihua", "cp_cppcc", "区政协副主席（不驻会）", "待查", "至今", "副厅级", "民进/未来科学城管委会"),

    # ═══ 前主要领导 ═══
    ("cp_zhou_jinxing", "cp_party_committee", "区委书记（前任）", "2024-12", "待查", "正厅级", "调任昌平区委书记（原东城区区长）"),
]

# ── RELATIONSHIPS ──
# person_a, person_b, type, context, overlap_org, overlap_period

RELATIONSHIPS = [
    # 甘靖中 ↔ 刘晓东 — 党政正职搭档
    ("cp_gan_jingzhong", "cp_liu_xiaodong", "superior_subordinate",
     "区委书记与区长党政正职搭档",
     "中共北京市昌平区委员会/昌平区人民政府", "当前"),

    # 甘靖中 ↔ 冷强田 — 书记-副书记
    ("cp_gan_jingzhong", "cp_leng_qiangtian", "superior_subordinate",
     "区委书记与专职副书记",
     "中共北京市昌平区委员会", "当前"),

    # 刘晓东 ↔ 冷强田 — 区长-副书记
    ("cp_liu_xiaodong", "cp_leng_qiangtian", "overlap",
     "区长与专职副书记在区委常委会共事",
     "中共北京市昌平区委员会", "当前"),

    # 甘靖中 ↔ 张庆武 — 书记-组织部长
    ("cp_gan_jingzhong", "cp_zhang_qingwu", "superior_subordinate",
     "区委书记与组织部部长（干部管理）",
     "中共北京市昌平区委员会", "当前"),

    # 甘靖中 ↔ 马亚军 — 书记-纪委书记
    ("cp_gan_jingzhong", "cp_ma_yajun", "superior_subordinate",
     "区委书记与纪委书记（从严治党主体责任）",
     "中共北京市昌平区委员会", "当前"),

    # 甘靖中 ↔ 马强 — 书记-政法委书记
    ("cp_gan_jingzhong", "cp_ma_qiang", "superior_subordinate",
     "区委书记与政法委书记",
     "中共北京市昌平区委员会", "当前"),

    # 刘晓东 ↔ 柳强 — 区长-副区长（常委兼任）
    ("cp_liu_xiaodong", "cp_liu_qiang", "superior_subordinate",
     "区长与常委副区长",
     "北京市昌平区人民政府", "当前"),

    # 刘晓东 ↔ 王卫国 — 区长-公安分局长
    ("cp_liu_xiaodong", "cp_wang_weiguo", "superior_subordinate",
     "区长与公安分局局长（安全稳定）",
     "北京市昌平区人民政府", "当前"),

    # 马强 ↔ 王卫国 — 政法委书记-公安分局长
    ("cp_ma_qiang", "cp_wang_weiguo", "overlap",
     "政法委书记与公安分局局长的政法系统协作",
     "中共北京市昌平区委政法委员会", "当前"),

    # 张庆武 ↔ 马亚军 — 组织部长-纪委书记
    ("cp_zhang_qingwu", "cp_ma_yajun", "overlap",
     "组织部与纪委在干部监督方面的协作",
     "中共北京市昌平区委员会", "当前"),

    # 陈祥 ↔ 张庆武 — 宣传部长-组织部长（常委协作）
    ("cp_chen_xiang", "cp_zhang_qingwu", "overlap",
     "宣传部与组织部在意识形态和干部教育方面的协作",
     "中共北京市昌平区委员会", "当前"),

    # 郭清尧 ↔ 蒋达峰 — 统战部长-政协主席
    ("cp_guo_qingyao", "cp_jiang_dafeng", "overlap",
     "统战部部长与政协主席的工作关系（兼政协党组副书记）",
     "中共北京市昌平区委统战部/区政协", "当前"),

    # 甘靖中 ↔ 周金星 — 前后任区委书记
    ("cp_gan_jingzhong", "cp_zhou_jinxing", "predecessor_successor",
     "甘靖中接替周金星任昌平区委书记（周金星原为东城区区长调任昌平）",
     "中共北京市昌平区委员会", "2024-2025"),
]


# ════════════════════════════════════════════
# DATABASE BUILDER
# ════════════════════════════════════════════

def create_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE persons(
        id TEXT PRIMARY KEY,
        name TEXT,
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
    )""")

    c.execute("""CREATE TABLE organizations(
        id TEXT PRIMARY KEY,
        name TEXT,
        type TEXT,
        level TEXT,
        parent TEXT,
        location TEXT
    )""")

    c.execute("""CREATE TABLE positions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id TEXT,
        org_id TEXT,
        title TEXT,
        start TEXT,
        end TEXT,
        rank TEXT,
        note TEXT
    )""")

    c.execute("""CREATE TABLE relationships(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a TEXT,
        person_b TEXT,
        type TEXT,
        context TEXT,
        overlap_org TEXT,
        overlap_period TEXT
    )""")

    for p in PERSONS:
        c.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", p)
    for o in ORGANIZATIONS:
        c.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)", o)
    for pos in POSITIONS:
        c.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)", pos)
    for r in RELATIONSHIPS:
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)", r)

    conn.commit()
    conn.close()
    print(f"[OK] Database created: {DB_PATH}")


# ════════════════════════════════════════════
# GEXF BUILDER
# ════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(post):
    if "书记" in post and "副" not in post and "副书记" not in post:
        return "255,50,50"
    if "区长" in post and "副" not in post:
        return "50,100,255"
    if "副书记" in post:
        return "255,100,100"
    if "纪委书记" in post or "监委" in post:
        return "255,165,0"
    if "常务副" in post:
        return "50,130,255"
    if "副区长" in post:
        return "100,130,255"
    if "部长" in post or "统战" in post or "组织" in post:
        return "180,100,200"
    if "政法委" in post:
        return "200,150,50"
    if "武装" in post:
        return "100,150,100"
    if "主任" in post or "人大" in post:
        return "200,255,255"
    if "政协" in post or "主席" in post:
        return "255,240,200"
    return "100,100,100"

def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "党委部门": "255,200,200",
        "政府": "200,200,255",
        "纪委": "255,165,0",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "公安": "200,200,255",
        "军队": "200,200,200",
        "开发区": "200,255,200",
    }
    return colors.get(org_type, "200,200,200")

def is_top_leader(post):
    post_clean = post.strip()
    if post_clean == "区委书记":
        return True
    if "区长" in post_clean and "副" not in post_clean and "副书记" not in post_clean:
        return True
    return False

def create_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>北京市昌平区领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role_or_type" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="edge_type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in PERSONS:
        pid, name, gender, eth, birth, bp, edu, party, work, post, org, src = p
        c = person_color(post)
        sz = "20.0" if is_top_leader(post) else "12.0"
        if "副书记" in post:
            sz = "15.0"
        lines.append(f'      <node id="p{pid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(post)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(org)}"/>')
        lines.append('        </attvalues>')
        parts = c.split(",")
        lines.append(f'        <viz:color r="{parts[0]}" g="{parts[1]}" b="{parts[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in ORGANIZATIONS:
        oid, name, otype, level, parent, loc = o
        c = org_color(otype)
        lines.append(f'      <node id="o{oid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(otype)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(parent)}"/>')
        lines.append('        </attvalues>')
        parts = c.split(",")
        lines.append(f'        <viz:color r="{parts[0]}" g="{parts[1]}" b="{parts[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    eid = 0
    lines.append('    <edges>')
    for pos in POSITIONS:
        pid, oid, title, start, end, rank, note = pos
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pid}" target="o{oid}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    for r in RELATIONSHIPS:
        pa, pb, rtype, context, overlap_org, overlap_period = r
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{pa}" target="p{pb}" label="{esc(rtype)}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(rtype)}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(context)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')

    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[OK] GEXF created: {GEXF_PATH}")


# ════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════

if __name__ == "__main__":
    create_database()
    create_gexf()
    print("[DONE] Build complete.")
