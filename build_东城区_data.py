#!/usr/bin/env python3
"""
北京市东城区领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Dongcheng District leadership.

Level: 市辖区(直辖市) — 正厅级
Province: 北京市
Targets: 区委书记 & 区长

Sources:
- bjdch.gov.cn (official leadership pages)
- Baidu Baike (access via engine bypass)
"""

import sqlite3
import os
from datetime import datetime

# ── PATHS ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "东城区_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "东城区_network.gexf")

# ════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════

PERSONS = [
    # id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source
    # ── 区委班子（11人） ──
    ("dc_sun_xinjun", "孙新军", "男", "汉族", "1968年10月", "浙江天台",
     "在职研究生/工商管理硕士", "1988年6月", "1990年7月",
     "区委书记", "中共北京市东城区委员会",
     "bjdch.gov.cn/official;baidu.baike"),
    ("dc_chen_xiansen", "陈献森", "男", "汉族", "1972年9月", "河南内黄",
     "大学(中国人民公安大学)/公共管理硕士(北京大学)", "1994年10月", "1996年7月",
     "区委副书记、区长", "北京市东城区人民政府",
     "bjdch.gov.cn/official;baidu.baike"),
    ("dc_sang_pengfei", "桑硼飞", "男", "汉族", "1980年2月", "待查",
     "在职研究生", "中共党员", "待查",
     "区委副书记、区委党校校长", "中共北京市东城区委员会",
     "bjdch.gov.cn/official"),
    ("dc_xue_guoqiang", "薛国强", "男", "汉族", "1973年3月", "待查",
     "中央党校研究生", "中共党员", "待查",
     "区委常委、统战部部长", "中共北京市东城区委统战部",
     "bjdch.gov.cn/official"),
    ("dc_wang_huawei", "王华伟", "男", "汉族", "1970年9月", "待查",
     "研究生", "中共党员", "待查",
     "区委常委、常务副区长", "北京市东城区人民政府",
     "bjdch.gov.cn/official"),
    ("dc_wang_yongmin", "王永民", "男", "汉族", "1978年12月", "待查",
     "大学", "中共党员", "待查",
     "区委常委、纪委书记、监委主任", "中共北京市东城区纪律检查委员会",
     "bjdch.gov.cn/official"),
    ("dc_li_qiang", "李强", "男", "汉族", "1976年10月", "待查",
     "大学", "中共党员", "待查",
     "区委常委", "中共北京市东城区委员会",
     "bjdch.gov.cn/official"),
    ("dc_sun_yang", "孙扬", "男", "汉族", "1979年2月", "待查",
     "研究生", "中共党员", "待查",
     "区委常委、政法委书记", "中共北京市东城区委政法委员会",
     "bjdch.gov.cn/official"),
    ("dc_huang_dan", "黄丹", "女", "汉族", "1977年2月", "待查",
     "研究生", "中共党员", "待查",
     "区委常委、组织部部长", "中共北京市东城区委组织部",
     "bjdch.gov.cn/official"),
    ("dc_su_hao", "苏昊", "男", "汉族", "1980年5月", "待查",
     "在职研究生", "中共党员", "待查",
     "区委常委、副区长", "北京市东城区人民政府",
     "bjdch.gov.cn/official"),
    ("dc_wang_zhiyong", "王智勇", "男", "满族", "1983年8月", "待查",
     "研究生", "中共党员", "待查",
     "区委常委、宣传部部长", "中共北京市东城区委宣传部",
     "bjdch.gov.cn/official"),
    # ── 副区长（除常委外） ──
    ("dc_ren_jianghao", "任江浩", "男", "汉族", "待查", "待查",
     "待查", "九三学社", "待查",
     "副区长", "北京市东城区人民政府",
     "bjdch.gov.cn/official"),
    ("dc_deng_huimin", "邓慧敏", "女", "回族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长", "北京市东城区人民政府",
     "bjdch.gov.cn/official"),
    ("dc_xiao_song", "肖松", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长、区公安分局局长", "北京市公安局东城分局",
     "bjdch.gov.cn/official"),
    ("dc_wang_youming", "王佑明", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长", "北京市东城区人民政府",
     "bjdch.gov.cn/official"),
    ("dc_zhang_xiaofeng", "张晓峰", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长", "北京市东城区人民政府",
     "bjdch.gov.cn/official"),
    ("dc_hu_yifeng", "胡异峰", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长", "北京市东城区人民政府",
     "bjdch.gov.cn/official"),
    ("dc_zhang_yanguo", "张艳国", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长（挂职）", "北京市东城区人民政府",
     "bjdch.gov.cn/official"),
    ("dc_lin_yanhong", "林艳红", "女", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副区长（挂职）", "北京市东城区人民政府",
     "bjdch.gov.cn/official"),
    # ── 前主要领导 ──
    ("dc_zhou_jinxing", "周金星", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "前区长（现任昌平区委书记）", "昌平区（已离任）",
     "bjdch.gov.cn/official"),
    # ── 人大主要领导 ──
    ("dc_xiao_zhigang", "肖志刚", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区人大常委会主任", "北京市东城区人民代表大会常务委员会",
     "bjdch.gov.cn/official"),
    ("dc_bai_jingtao", "白京涛", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区人大常委会副主任", "北京市东城区人民代表大会常务委员会",
     "bjdch.gov.cn/official"),
    # ── 政协主要领导 ──
    ("dc_tang_qinfei", "汤钦飞", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "区政协主席", "中国人民政治协商会议北京市东城区委员会",
     "bjdch.gov.cn/official"),
]

ORGANIZATIONS = [
    # id, name, type, level, parent, location
    ("dc_party_committee", "中共北京市东城区委员会", "党委", "地厅级", "中共北京市委", "北京市东城区"),
    ("dc_gov", "北京市东城区人民政府", "政府", "地厅级", "北京市人民政府", "北京市东城区"),
    ("dc_org_department", "中共北京市东城区委组织部", "党委部门", "正处级", "东城区委", "北京市东城区"),
    ("dc_discipline", "中共北京市东城区纪律检查委员会", "纪委", "地厅级", "北京市纪委监委", "北京市东城区"),
    ("dc_propaganda", "中共北京市东城区委宣传部", "党委部门", "正处级", "东城区委", "北京市东城区"),
    ("dc_united_front", "中共北京市东城区委统战部", "党委部门", "正处级", "东城区委", "北京市东城区"),
    ("dc_political_legal", "中共北京市东城区委政法委员会", "党委部门", "正处级", "东城区委", "北京市东城区"),
    ("dc_party_school", "中共北京市东城区委党校", "党委部门", "正处级", "东城区委", "北京市东城区"),
    ("dc_public_security", "北京市公安局东城分局", "公安", "正处级", "北京市公安局", "北京市东城区"),
    ("dc_peoples_congress", "北京市东城区人民代表大会常务委员会", "人大", "地厅级", "北京市人大常委会", "北京市东城区"),
    ("dc_cppcc", "中国人民政治协商会议北京市东城区委员会", "政协", "地厅级", "北京市政协", "北京市东城区"),
    ("dc_procuratorate", "北京市东城区人民检察院", "政法", "地厅级", "北京市人民检察院", "北京市东城区"),
    ("dc_court", "北京市东城区人民法院", "政法", "地厅级", "北京市高级人民法院", "北京市东城区"),
]

POSITIONS = [
    # person_id, org_id, title, start, end, rank, note

    # ═══ 孙新军 — 区委书记 ═══
    ("dc_sun_xinjun", "dc_party_committee", "区委书记", "2022-04", "至今", "正厅级", "主持区委全面工作"),
    # 孙新军32年履历空白（1990-2022），已知曾担任北京市政协副主席
    ("dc_sun_xinjun", "dc_cppcc", "北京市政协副主席", "2021", "2022-04", "副部级（政协）", "兼任"),
    ("dc_sun_xinjun", "dc_gov", "东城区区长", "2017-09", "2021", "正厅级", "前职"),
    ("dc_sun_xinjun", "dc_gov", "东城区常务副区长", "2015-06", "2017-09", "副厅级", ""),
    ("dc_sun_xinjun", "dc_party_committee", "东城区委常委", "2015-06", "2022-04", "副厅级→正厅级", ""),
    # 履历缺口
    ("dc_sun_xinjun", "dc_org_department", "履历缺口（1990-2015年约25年）", "1990-07", "2015-06", "未知", "公开资料完全缺失"),

    # ═══ 陈献森 — 区长 ═══
    ("dc_chen_xiansen", "dc_gov", "区长", "2024-12", "至今", "正厅级", "2024.12代理，2025.01.10正式当选"),
    ("dc_chen_xiansen", "dc_party_committee", "区委副书记", "2024-12", "至今", "正厅级", "兼任"),
    ("dc_chen_xiansen", "dc_party_school", "区行政学院院长（兼）", "2024-12", "至今", "正厅级", "兼任"),
    ("dc_chen_xiansen", "dc_political_legal", "区委常委、政法委书记", "2021-12", "2024-01", "副厅级", "东城区"),
    ("dc_chen_xiansen", "dc_gov", "副区长", "2020-06", "2024-12", "副厅级", "东城区副区长"),
    ("dc_chen_xiansen", "dc_party_committee", "区委常委", "2020-06", "2024-12", "副厅级", "入常"),
    # 履历空白 2016.04-2020.06
    ("dc_chen_xiansen", "dc_org_department", "履历缺口（2016.04-2020.06）", "2016-04", "2020-06", "未知", "4年职务空白"),
    # 援藏经历
    ("dc_chen_xiansen", "dc_org_department", "援藏：堆龙德庆县委书记", "2013-07", "2016-04", "正处级", "西藏拉萨市"),
    ("dc_chen_xiansen", "dc_party_committee", "北京市对口支援指挥部", "2013-07", "2016-04", "正处级", "援藏"),
    # 西城区时期
    ("dc_chen_xiansen", "dc_org_department", "西城区德胜街道工委书记", "2011-08", "2013-07", "正处级", "西城区"),
    ("dc_chen_xiansen", "dc_org_department", "西城区德胜街道工委副书记、办事处主任", "2010-10", "2011-08", "正处级", "西城区"),
    ("dc_chen_xiansen", "dc_org_department", "共青团西城区委书记", "2005-05", "2010-10", "正处级", "西城区共青团系统"),
    ("dc_chen_xiansen", "dc_org_department", "共青团西城区委副书记", "2002-04", "2005-05", "副处级", ""),
    ("dc_chen_xiansen", "dc_public_security", "北京市公安局西城分局法制处副处长", "2000-12", "2002-04", "副处级", "公安法制系统"),
    ("dc_chen_xiansen", "dc_public_security", "北京市公安局西城分局法制处科员", "1996-07", "2000-12", "科员", "参加公安工作"),
    # 教育背景
    ("dc_chen_xiansen", "dc_org_department", "北京大学公共管理硕士（MPA）", "2005", "2008", "硕士", "在职攻读"),
    ("dc_chen_xiansen", "dc_org_department", "中国人民公安大学安全防范专业学生", "1992-09", "1996-07", "本科", "大学学历"),

    # ═══ 桑硼飞 — 区委副书记 ═══
    ("dc_sang_pengfei", "dc_party_committee", "区委副书记", "2026-04", "至今", "正厅级", "兼区委党校校长"),
    ("dc_sang_pengfei", "dc_party_school", "区委党校校长（兼）", "2026-04", "至今", "正厅级", ""),

    # ═══ 薛国强 — 统战部长 ═══
    ("dc_xue_guoqiang", "dc_united_front", "区委常委、统战部部长", "2024", "至今", "副厅级", "兼政协党组副书记"),
    ("dc_xue_guoqiang", "dc_cppcc", "区政协党组副书记（兼）", "2024", "至今", "副厅级", ""),

    # ═══ 王华伟 — 常务副区长 ═══
    ("dc_wang_huawei", "dc_gov", "常务副区长", "2023", "至今", "副厅级", "区委常委/区政府党组副书记"),

    # ═══ 王永民 — 纪委书记 ═══
    ("dc_wang_yongmin", "dc_discipline", "区委常委、纪委书记、监委主任", "2023", "至今", "副厅级", ""),

    # ═══ 李强 — 区委常委 ═══
    ("dc_li_qiang", "dc_party_committee", "区委常委", "2024", "至今", "副厅级", "具体分管职务未明确"),

    # ═══ 孙扬 — 政法委书记 ═══
    ("dc_sun_yang", "dc_political_legal", "区委常委、政法委书记", "2023", "至今", "副厅级", ""),

    # ═══ 黄丹 — 组织部长 ═══
    ("dc_huang_dan", "dc_org_department", "区委常委、组织部部长", "2023", "至今", "副厅级", ""),

    # ═══ 苏昊 — 副区长（常委） ═══
    ("dc_su_hao", "dc_gov", "区委常委、副区长", "2025-04", "至今", "副厅级", "双肩挑"),
    ("dc_su_hao", "dc_gov", "副区长", "2024", "2025-04", "副厅级", "晋升常委"),

    # ═══ 王智勇 — 宣传部长 ═══
    ("dc_wang_zhiyong", "dc_propaganda", "区委常委、宣传部部长", "2025-05", "至今", "副厅级", ""),

    # ═══ 副区长们 ═══
    ("dc_ren_jianghao", "dc_gov", "副区长", "2024-12", "至今", "副厅级", "九三学社，分管商务/文旅/体育"),
    ("dc_deng_huimin", "dc_gov", "副区长", "2025-06", "至今", "副厅级", "女/回族，分管科技/卫健/市场监管"),
    ("dc_xiao_song", "dc_gov", "副区长、区公安分局局长", "2025-12", "至今", "副厅级", "分管公安"),
    ("dc_wang_youming", "dc_gov", "副区长", "2024", "至今", "副厅级", "分管教育/民政"),
    ("dc_zhang_xiaofeng", "dc_gov", "副区长", "2024", "至今", "副厅级", "分管司法/国资/信访"),
    ("dc_hu_yifeng", "dc_gov", "副区长", "2025-06", "至今", "副厅级", "分管生态环境/城市管理"),
    ("dc_zhang_yanguo", "dc_gov", "副区长（挂职）", "2026-02", "至今", "副厅级", "国开行挂职"),
    ("dc_lin_yanhong", "dc_gov", "副区长（挂职）", "2026-02", "至今", "副厅级", "国家外汇管理局挂职"),

    # ═══ 前主要领导 ═══
    ("dc_zhou_jinxing", "dc_gov", "区长", "2022", "2024-12", "正厅级", "调任昌平区委书记"),
    ("dc_zhou_jinxing", "dc_party_committee", "区委副书记", "2022", "2024-12", "正厅级", ""),

    # ═══ 人大 ═══
    ("dc_xiao_zhigang", "dc_peoples_congress", "区人大常委会主任", "2022", "至今", "正厅级", ""),
    ("dc_bai_jingtao", "dc_peoples_congress", "区人大常委会副主任", "2022", "至今", "副厅级", ""),

    # ═══ 政协 ═══
    ("dc_tang_qinfei", "dc_cppcc", "区政协主席", "2022", "至今", "正厅级", ""),
]

# ── RELATIONSHIPS ──
# person_a, person_b, type, context, overlap_org, overlap_period

RELATIONSHIPS = [
    # 孙新军 ↔ 陈献森 — 党政正职搭档
    ("dc_sun_xinjun", "dc_chen_xiansen", "superior_subordinate",
     "区委书记与区长党政正职搭档",
     "中共北京市东城区委员会/东城区人民政府", "2024-12至今"),

    # 孙新军 ↔ 桑硼飞 — 书记-副书记
    ("dc_sun_xinjun", "dc_sang_pengfei", "superior_subordinate",
     "区委书记与专职副书记",
     "中共北京市东城区委员会", "2026-04至今"),

    # 陈献森 ↔ 桑硼飞 — 区长-副书记
    ("dc_chen_xiansen", "dc_sang_pengfei", "overlap",
     "区长与专职副书记在区委常委会共事",
     "中共北京市东城区委员会", "2026-04至今"),

    # 孙新军 ↔ 王华伟 — 书记-常务副区长
    ("dc_sun_xinjun", "dc_wang_huawei", "superior_subordinate",
     "区委书记与常务副区长",
     "中共北京市东城区委员会", "2023至今"),
    ("dc_chen_xiansen", "dc_wang_huawei", "superior_subordinate",
     "区长与常务副区长（区政府日常运作）",
     "北京市东城区人民政府", "2024-12至今"),

    # 孙新军 ↔ 黄丹 — 书记-组织部长
    ("dc_sun_xinjun", "dc_huang_dan", "superior_subordinate",
     "区委书记与组织部部长（干部管理）",
     "中共北京市东城区委员会", "2023至今"),

    # 孙新军 ↔ 王永民 — 书记-纪委书记
    ("dc_sun_xinjun", "dc_wang_yongmin", "superior_subordinate",
     "区委书记与纪委书记（从严治党主体责任）",
     "中共北京市东城区委员会", "2023至今"),

    # 孙新军 ↔ 孙扬 — 书记-政法委书记
    ("dc_sun_xinjun", "dc_sun_yang", "superior_subordinate",
     "区委书记与政法委书记",
     "中共北京市东城区委员会", "2023至今"),

    # 陈献森 ↔ 肖松 — 区长-公安分局长
    ("dc_chen_xiansen", "dc_xiao_song", "superior_subordinate",
     "区长与公安分局局长（安全稳定）",
     "北京市东城区人民政府", "2025-12至今"),

    # 陈献森 ↔ 苏昊 — 区长-副区长（常委兼任）
    ("dc_chen_xiansen", "dc_su_hao", "superior_subordinate",
     "区长与常委副区长",
     "北京市东城区人民政府", "2024至今"),

    # 黄丹 ↔ 王永民 — 组织部长-纪委书记（干部选任监督）
    ("dc_huang_dan", "dc_wang_yongmin", "overlap",
     "组织部与纪委在干部监督方面的协作",
     "中共北京市东城区委员会", "2023至今"),

    # 孙扬 ↔ 肖松 — 政法委书记-公安分局长
    ("dc_sun_yang", "dc_xiao_song", "overlap",
     "政法委书记与公安分局局长的政法系统协作",
     "中共北京市东城区委政法委员会", "2025-12至今"),

    # 陈献森 ↔ 周金星 — 前后任区长
    ("dc_chen_xiansen", "dc_zhou_jinxing", "predecessor_successor",
     "陈献森接替周金星任区长（周金星调任昌平区委书记）",
     "北京市东城区人民政府", "2024-12"),
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
        "政法": "200,200,255",
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
    lines.append('    <description>北京市东城区领导班子工作关系网络</description>')
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
