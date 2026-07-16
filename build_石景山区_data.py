#!/usr/bin/env python3
"""
北京市石景山区领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Shijingshan District leadership.

Level: 市辖区(直辖市) — 正厅级
Province: 北京市
Targets: 区委书记 & 区长

Sources:
- bjsjs.gov.cn (official leadership pages, accessed 2026-07-16)
"""

import sqlite3
import os
from datetime import datetime

# ── PATHS ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "石景山区_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "石景山区_network.gexf")

# ════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════

PERSONS = [
    # id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source

    # ── 区委班子（10人） ──
    ("sjs_chang_wei", "常卫", "男", "汉族", "1966年9月", "待查",
     "在职研究生", "中共党员", "待查",
     "区委书记", "中共北京市石景山区委员会",
     "bjsjs.gov.cn/gongkai/zwgkpd/ldjs_1946/qw_1947/"),
    ("sjs_wan_long", "万隆", "男", "汉族", "1976年12月", "待查",
     "在职研究生", "中共党员", "待查",
     "区委副书记、区长", "北京市石景山区人民政府",
     "bjsjs.gov.cn/gongkai/zwgkpd/ldjs_1946/qw_1947/;qzf_1949/"),
    ("sjs_zhang_lijun", "张利军", "男", "汉族", "1971年6月", "待查",
     "在职研究生", "中共党员", "待查",
     "区委副书记、区委党校（行政学院）校（院）长", "中共北京市石景山区委员会",
     "bjsjs.gov.cn/gongkai/zwgkpd/ldjs_1946/qw_1947/"),
    ("sjs_wang_xiaodong", "王晓东", "男", "汉族", "1981年11月", "待查",
     "研究生", "中共党员", "待查",
     "区委常委、区纪委书记、区监察委员会主任", "中共北京市石景山区纪律检查委员会",
     "bjsjs.gov.cn/gongkai/zwgkpd/ldjs_1946/qw_1947/"),
    ("sjs_qian_xing", "钱行", "男", "蒙古族", "1975年2月", "待查",
     "大学", "中共党员", "待查",
     "区委常委、统战部部长，区政协党组副书记，区社会主义学院院长（兼）", "中共北京市石景山区委统战部",
     "bjsjs.gov.cn/gongkai/zwgkpd/ldjs_1946/qw_1947/"),
    ("sjs_chi_zhiyu", "迟志禹", "男", "汉族", "1974年2月", "待查",
     "在职研究生", "中共党员", "待查",
     "区委常委、政法委书记、区委办公室主任，区档案局局长（兼）", "中共北京市石景山区委政法委员会",
     "bjsjs.gov.cn/gongkai/zwgkpd/ldjs_1946/qw_1947/"),
    ("sjs_zhang_weixin", "张维新", "男", "汉族", "1978年3月", "待查",
     "大学", "中共党员", "待查",
     "区委常委、武装部政委", "北京市石景山区人民武装部",
     "bjsjs.gov.cn/gongkai/zwgkpd/ldjs_1946/qw_1947/"),
    ("sjs_shen_jian", "申键", "男", "汉族", "1975年5月", "待查",
     "研究生", "中共党员", "待查",
     "区委常委、宣传部部长", "中共北京市石景山区委宣传部",
     "bjsjs.gov.cn/gongkai/zwgkpd/ldjs_1946/qw_1947/"),
    ("sjs_li_wenhua", "李文化", "女", "汉族", "1976年5月", "待查",
     "大学", "中共党员", "待查",
     "区委常委，区政府党组副书记、副区长，中关村科技园区石景山园工委书记（兼）", "北京市石景山区人民政府",
     "bjsjs.gov.cn/gongkai/zwgkpd/ldjs_1946/qw_1947/;qzf_1949/"),
    ("sjs_wang_xin", "王昕", "女", "汉族", "1972年12月", "待查",
     "大学", "中共党员", "待查",
     "区委常委、组织部部长", "中共北京市石景山区委组织部",
     "bjsjs.gov.cn/gongkai/zwgkpd/ldjs_1946/qw_1947/"),

    # ── 副区长（非常委） ──
    ("sjs_hu_hao", "胡浩", "男", "汉族", "1978年11月", "待查",
     "大学", "无党派人士", "待查",
     "副区长", "北京市石景山区人民政府",
     "bjsjs.gov.cn/gongkai/zwgkpd/ldjs_1946/qzf_1949/"),
    ("sjs_zhong_mianmian", "钟棉棉", "女", "畲族", "1985年3月", "待查",
     "研究生", "中共党员", "待查",
     "副区长", "北京市石景山区人民政府",
     "bjsjs.gov.cn/gongkai/zwgkpd/ldjs_1946/qzf_1949/"),
    ("sjs_zhang_jingyuan", "张景渊", "男", "汉族", "1979年7月", "待查",
     "研究生", "中共党员", "待查",
     "副区长、区公安分局党委书记、局长、区委政法委副书记（兼）", "北京市公安局石景山分局",
     "bjsjs.gov.cn/gongkai/zwgkpd/ldjs_1946/qzf_1949/"),
    ("sjs_cao_shihui", "曹世辉", "男", "满族", "1975年7月", "待查",
     "在职研究生", "中共党员", "待查",
     "副区长", "北京市石景山区人民政府",
     "bjsjs.gov.cn/gongkai/zwgkpd/ldjs_1946/qzf_1949/"),
    ("sjs_ma_bin", "马斌", "男", "汉族", "1979年3月", "待查",
     "大学", "中共党员", "待查",
     "副区长、区红十字会会长（兼）", "北京市石景山区人民政府",
     "bjsjs.gov.cn/gongkai/zwgkpd/ldjs_1946/qzf_1949/"),
    ("sjs_zhang_shengjun", "张盛军", "男", "汉族", "1980年7月", "待查",
     "在职研究生", "中共党员", "待查",
     "副区长", "北京市石景山区人民政府",
     "bjsjs.gov.cn/gongkai/zwgkpd/ldjs_1946/qzf_1949/"),

    # ── 区人大主要领导 ──
    ("sjs_tian_liyue", "田利跃", "男", "汉族", "1967年1月", "待查",
     "中央党校研究生", "中共党员", "待查",
     "区人大常委会党组书记、主任", "北京市石景山区人民代表大会常务委员会",
     "bjsjs.gov.cn/gongkai/zwgkpd/ldjs_1946/qrd_1948/"),
    ("sjs_ning_huijuan", "宁慧娟", "女", "汉族", "1966年4月", "待查",
     "中央党校研究生", "中共党员", "待查",
     "区人大常委会党组副书记、副主任", "北京市石景山区人民代表大会常务委员会",
     "bjsjs.gov.cn/gongkai/zwgkpd/ldjs_1946/qrd_1948/"),
    ("sjs_zhang_yuguo", "张玉国", "男", "汉族", "1968年9月", "待查",
     "中央党校研究生", "中共党员", "待查",
     "区人大常委会党组成员、副主任，区总工会主席（兼）", "北京市石景山区人民代表大会常务委员会",
     "bjsjs.gov.cn/gongkai/zwgkpd/ldjs_1946/qrd_1948/"),
    ("sjs_shi_xianfu", "石显富", "男", "汉族", "1971年9月", "待查",
     "中央党校研究生", "中共党员", "待查",
     "区人大常委会党组成员、副主任", "北京市石景山区人民代表大会常务委员会",
     "bjsjs.gov.cn/gongkai/zwgkpd/ldjs_1946/qrd_1948/"),
    ("sjs_zhang_wei", "张伟", "男", "汉族", "1968年7月", "待查",
     "中央党校研究生", "中共党员", "待查",
     "区人大常委会党组成员、副主任", "北京市石景山区人民代表大会常务委员会",
     "bjsjs.gov.cn/gongkai/zwgkpd/ldjs_1946/qrd_1948/"),

    # ── 区政协主要领导 ──
    ("sjs_jin_xiubin", "金秀斌", "男", "汉族", "1970年3月", "待查",
     "市委党校研究生", "中共党员", "待查",
     "区政协党组书记、主席", "中国人民政治协商会议北京市石景山区委员会",
     "bjsjs.gov.cn/gongkai/zwgkpd/ldjs_1946/qzx_1950/"),
    ("sjs_ge_qiang", "葛强", "男", "汉族", "1966年9月", "待查",
     "大学", "中共党员", "待查",
     "区政协党组副书记、副主席", "中国人民政治协商会议北京市石景山区委员会",
     "bjsjs.gov.cn/gongkai/zwgkpd/ldjs_1946/qzx_1950/"),
    ("sjs_yang_guibao", "杨贵宝", "男", "汉族", "1970年4月", "待查",
     "大学", "中共党员", "待查",
     "区政协党组成员、副主席", "中国人民政治协商会议北京市石景山区委员会",
     "bjsjs.gov.cn/gongkai/zwgkpd/ldjs_1946/qzx_1950/"),
    ("sjs_ding_renmeng", "丁仁猛", "男", "汉族", "1970年6月", "待查",
     "中央党校研究生", "中共党员", "待查",
     "区政协党组成员、副主席", "中国人民政治协商会议北京市石景山区委员会",
     "bjsjs.gov.cn/gongkai/zwgkpd/ldjs_1946/qzx_1950/"),
    ("sjs_mao_xuan", "毛轩", "男", "汉族", "1973年6月", "待查",
     "大学", "民盟盟员", "待查",
     "区政协副主席（不驻会），民盟石景山区工委主委", "中国人民政治协商会议北京市石景山区委员会",
     "bjsjs.gov.cn/gongkai/zwgkpd/ldjs_1946/qzx_1950/"),
    ("sjs_wang_lijun", "汪礼俊", "男", "汉族", "1971年10月", "待查",
     "研究生", "民建会员", "待查",
     "区政协副主席（不驻会），民建石景山区工委主委", "中国人民政治协商会议北京市石景山区委员会",
     "bjsjs.gov.cn/gongkai/zwgkpd/ldjs_1946/qzx_1950/"),
    ("sjs_liu_tiejun", "刘铁军", "男", "汉族", "1967年12月", "待查",
     "研究生", "九三学社社员/中共党员", "待查",
     "区政协副主席（不驻会），九三学社石景山区工委主委", "中国人民政治协商会议北京市石景山区委员会",
     "bjsjs.gov.cn/gongkai/zwgkpd/ldjs_1946/qzx_1950/"),
]

ORGANIZATIONS = [
    # id, name, type, level, parent, location
    ("sjs_party_committee", "中共北京市石景山区委员会", "党委", "地厅级", "中共北京市委", "北京市石景山区"),
    ("sjs_gov", "北京市石景山区人民政府", "政府", "地厅级", "北京市人民政府", "北京市石景山区"),
    ("sjs_discipline", "中共北京市石景山区纪律检查委员会", "纪委", "地厅级", "北京市纪委监委", "北京市石景山区"),
    ("sjs_org_department", "中共北京市石景山区委组织部", "党委部门", "正处级", "石景山区委", "北京市石景山区"),
    ("sjs_propaganda", "中共北京市石景山区委宣传部", "党委部门", "正处级", "石景山区委", "北京市石景山区"),
    ("sjs_united_front", "中共北京市石景山区委统战部", "党委部门", "正处级", "石景山区委", "北京市石景山区"),
    ("sjs_political_legal", "中共北京市石景山区委政法委员会", "党委部门", "正处级", "石景山区委", "北京市石景山区"),
    ("sjs_party_school", "中共北京市石景山区委党校（行政学院）", "党委部门", "正处级", "石景山区委", "北京市石景山区"),
    ("sjs_military_department", "北京市石景山区人民武装部", "军事", "正处级", "北京卫戍区", "北京市石景山区"),
    ("sjs_public_security", "北京市公安局石景山分局", "公安", "正处级", "北京市公安局", "北京市石景山区"),
    ("sjs_zone_park", "中关村科技园区石景山园", "开发区", "正处级", "中关村科技园区管委会", "北京市石景山区"),
    ("sjs_peoples_congress", "北京市石景山区人民代表大会常务委员会", "人大", "地厅级", "北京市人大常委会", "北京市石景山区"),
    ("sjs_cppcc", "中国人民政治协商会议北京市石景山区委员会", "政协", "地厅级", "北京市政协", "北京市石景山区"),
]

POSITIONS = [
    # person_id, org_id, title, start, end, rank, note

    # ═══ 常卫 — 区委书记 ═══
    ("sjs_chang_wei", "sjs_party_committee", "区委书记", "待查", "至今", "正厅级", "主持区委全面工作"),

    # ═══ 万隆 — 区长 ═══
    ("sjs_wan_long", "sjs_gov", "区长", "待查", "至今", "正厅级", "主持区政府全面工作"),
    ("sjs_wan_long", "sjs_party_committee", "区委副书记", "待查", "至今", "正厅级", "兼任"),

    # ═══ 张利军 — 区委副书记 ═══
    ("sjs_zhang_lijun", "sjs_party_committee", "区委副书记", "待查", "至今", "正厅级", "兼区委党校校长"),
    ("sjs_zhang_lijun", "sjs_party_school", "区委党校（行政学院）校（院）长（兼）", "待查", "至今", "正厅级", ""),

    # ═══ 王晓东 — 纪委书记 ═══
    ("sjs_wang_xiaodong", "sjs_discipline", "区委常委、区纪委书记、区监委主任", "待查", "至今", "副厅级", ""),

    # ═══ 钱行 — 统战部长 ═══
    ("sjs_qian_xing", "sjs_united_front", "区委常委、统战部部长", "待查", "至今", "副厅级", "兼政协党组副书记、社会主义学院院长"),

    # ═══ 迟志禹 — 政法委书记 ═══
    ("sjs_chi_zhiyu", "sjs_political_legal", "区委常委、政法委书记、区委办公室主任", "待查", "至今", "副厅级", "兼区档案局局长"),

    # ═══ 张维新 — 武装部政委 ═══
    ("sjs_zhang_weixin", "sjs_military_department", "区委常委、武装部政委", "待查", "至今", "副厅级", ""),

    # ═══ 申键 — 宣传部长 ═══
    ("sjs_shen_jian", "sjs_propaganda", "区委常委、宣传部部长", "待查", "至今", "副厅级", ""),

    # ═══ 李文化 — 常务副区长 ═══
    ("sjs_li_wenhua", "sjs_gov", "区委常委、党组副书记、副区长", "待查", "至今", "副厅级", "兼中关村石景山园工委书记"),
    ("sjs_li_wenhua", "sjs_zone_park", "中关村科技园区石景山园工委书记（兼）", "待查", "至今", "副厅级", ""),

    # ═══ 王昕 — 组织部长 ═══
    ("sjs_wang_xin", "sjs_org_department", "区委常委、组织部部长", "待查", "至今", "副厅级", ""),

    # ═══ 副区长们 ═══
    ("sjs_hu_hao", "sjs_gov", "副区长", "待查", "至今", "副厅级", "无党派人士"),
    ("sjs_zhong_mianmian", "sjs_gov", "副区长", "待查", "至今", "副厅级", "畲族"),
    ("sjs_zhang_jingyuan", "sjs_gov", "副区长、区公安分局局长", "待查", "至今", "副厅级", "兼区委政法委副书记"),
    ("sjs_zhang_jingyuan", "sjs_public_security", "党委书记、局长", "待查", "至今", "副厅级", ""),
    ("sjs_cao_shihui", "sjs_gov", "副区长", "待查", "至今", "副厅级", ""),
    ("sjs_ma_bin", "sjs_gov", "副区长", "待查", "至今", "副厅级", "兼区红十字会会长"),
    ("sjs_zhang_shengjun", "sjs_gov", "副区长", "待查", "至今", "副厅级", ""),

    # ═══ 人大 ═══
    ("sjs_tian_liyue", "sjs_peoples_congress", "区人大常委会党组书记、主任", "待查", "至今", "正厅级", ""),
    ("sjs_ning_huijuan", "sjs_peoples_congress", "区人大常委会党组副书记、副主任", "待查", "至今", "副厅级", ""),
    ("sjs_zhang_yuguo", "sjs_peoples_congress", "区人大常委会党组成员、副主任", "待查", "至今", "副厅级", "兼区总工会主席"),
    ("sjs_shi_xianfu", "sjs_peoples_congress", "区人大常委会党组成员、副主任", "待查", "至今", "副厅级", ""),
    ("sjs_zhang_wei", "sjs_peoples_congress", "区人大常委会党组成员、副主任", "待查", "至今", "副厅级", ""),

    # ═══ 政协 ═══
    ("sjs_jin_xiubin", "sjs_cppcc", "区政协党组书记、主席", "待查", "至今", "正厅级", ""),
    ("sjs_ge_qiang", "sjs_cppcc", "区政协党组副书记、副主席", "待查", "至今", "副厅级", ""),
    ("sjs_yang_guibao", "sjs_cppcc", "区政协党组成员、副主席", "待查", "至今", "副厅级", ""),
    ("sjs_ding_renmeng", "sjs_cppcc", "区政协党组成员、副主席", "待查", "至今", "副厅级", ""),
    ("sjs_mao_xuan", "sjs_cppcc", "区政协副主席（不驻会）", "待查", "至今", "副厅级", "民盟石景山区工委主委"),
    ("sjs_wang_lijun", "sjs_cppcc", "区政协副主席（不驻会）", "待查", "至今", "副厅级", "民建石景山区工委主委"),
    ("sjs_liu_tiejun", "sjs_cppcc", "区政协副主席（不驻会）", "待查", "至今", "副厅级", "九三学社石景山区工委主委"),
]

# ── RELATIONSHIPS ──
# person_a, person_b, type, context, overlap_org, overlap_period

RELATIONSHIPS = [
    # 常卫 ↔ 万隆 — 党政正职搭档
    ("sjs_chang_wei", "sjs_wan_long", "superior_subordinate",
     "区委书记与区长党政正职搭档",
     "中共北京市石景山区委员会/石景山区人民政府", "至今"),

    # 常卫 ↔ 张利军 — 书记-副书记
    ("sjs_chang_wei", "sjs_zhang_lijun", "superior_subordinate",
     "区委书记与专职副书记",
     "中共北京市石景山区委员会", "至今"),

    # 万隆 ↔ 张利军 — 区长-副书记
    ("sjs_wan_long", "sjs_zhang_lijun", "overlap",
     "区长与专职副书记在区委常委会共事",
     "中共北京市石景山区委员会", "至今"),

    # 常卫 ↔ 李文化 — 书记-常务副区长
    ("sjs_chang_wei", "sjs_li_wenhua", "superior_subordinate",
     "区委书记与常务副区长",
     "中共北京市石景山区委员会", "至今"),
    ("sjs_wan_long", "sjs_li_wenhua", "superior_subordinate",
     "区长与常务副区长（区政府日常运作）",
     "北京市石景山区人民政府", "至今"),

    # 常卫 ↔ 王昕 — 书记-组织部长
    ("sjs_chang_wei", "sjs_wang_xin", "superior_subordinate",
     "区委书记与组织部部长（干部管理）",
     "中共北京市石景山区委员会", "至今"),

    # 常卫 ↔ 王晓东 — 书记-纪委书记
    ("sjs_chang_wei", "sjs_wang_xiaodong", "superior_subordinate",
     "区委书记与纪委书记（从严治党主体责任）",
     "中共北京市石景山区委员会", "至今"),

    # 常卫 ↔ 迟志禹 — 书记-政法委书记
    ("sjs_chang_wei", "sjs_chi_zhiyu", "superior_subordinate",
     "区委书记与政法委书记",
     "中共北京市石景山区委员会", "至今"),

    # 常卫 ↔ 申键 — 书记-宣传部长
    ("sjs_chang_wei", "sjs_shen_jian", "superior_subordinate",
     "区委书记与宣传部部长",
     "中共北京市石景山区委员会", "至今"),

    # 常卫 ↔ 钱行 — 书记-统战部长
    ("sjs_chang_wei", "sjs_qian_xing", "superior_subordinate",
     "区委书记与统战部部长",
     "中共北京市石景山区委员会", "至今"),

    # 万隆 ↔ 张景渊 — 区长-公安分局长
    ("sjs_wan_long", "sjs_zhang_jingyuan", "superior_subordinate",
     "区长与公安分局局长（安全稳定）",
     "北京市石景山区人民政府", "至今"),

    # 王晓东 ↔ 王昕 — 纪委书记-组织部长（干部选任监督）
    ("sjs_wang_xiaodong", "sjs_wang_xin", "overlap",
     "组织部与纪委在干部监督方面的协作",
     "中共北京市石景山区委员会", "至今"),

    # 迟志禹 ↔ 张景渊 — 政法委书记-公安分局长
    ("sjs_chi_zhiyu", "sjs_zhang_jingyuan", "overlap",
     "政法委书记与公安分局局长的政法系统协作",
     "中共北京市石景山区委政法委员会", "至今"),
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
    if "主任" in post or "人大" in post:
        return "200,255,255"
    if "政协" in post or "主席" in post:
        return "255,240,200"
    if "武装部" in post or "政委" in post:
        return "150,200,150"
    return "100,100,100"

def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "党委部门": "255,200,200",
        "政府": "200,200,255",
        "纪委": "255,165,0",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "军事": "200,255,200",
        "公安": "200,200,255",
        "开发区": "200,255,200",
    }
    return colors.get(org_type, "200,200,200")

def is_top_leader(post):
    post_clean = post.strip()
    if post_clean == "区委书记":
        return True
    if "区长" in post_clean and "副" not in post_clean:
        return True
    return False

def create_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>北京市石景山区领导班子工作关系网络</description>')
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
        p_pid, oid, title, start, end, rank, note = pos
        eid += 1
        lines.append(f'      <edge id="{eid}" source="p{p_pid}" target="o{oid}" label="{esc(title)}" weight="1.0">')
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
