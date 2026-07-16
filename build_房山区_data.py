#!/usr/bin/env python3
"""
北京市房山区领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Fangshan District leadership.

Data sources:
- bjfsh.gov.cn/zwgk/ldjs/ (official leadership page, accessed 2026-07-16)
- Baidu Baike (阳波, 底志欣, accessed 2026-07-16)
"""

import sqlite3
import os
from datetime import datetime

# ── PATHS ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "房山区_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "房山区_network.gexf")

# ════════════════════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════════════════════

# Person ID convention: fangshan_{surname_givenname}
PERSONS = [
    # id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source

    # ── Top leaders ──
    ("fangshan_yang_bo", "阳波", "男", "汉族", "1980年5月", "未知", "研究生/工学博士", "中共党员", "2008年6月",
     "区委书记", "中共北京市房山区委员会", "bjfsh.gov.cn/zwgk/ldjs/"),

    ("fangshan_di_zhixin", "底志欣", "男", "回族", "1975年7月", "河北无极", "在职研究生/经济学博士", "中共党员", "1998年6月",
     "区委副书记、区长", "北京市房山区人民政府", "bjfsh.gov.cn/zwgk/ldjs/"),

    # ── Standing Committee ──
    ("fangshan_wang_hongtao", "王洪涛", "男", "汉族", "1980年10月", "未知", "研究生", "中共党员", "未知",
     "区委常委、组织部部长", "中共北京市房山区委组织部", "bjfsh.gov.cn/zwgk/ldjs/"),

    ("fangshan_tong_gang", "佟刚", "男", "满族", "1971年8月", "未知", "市委党校研究生", "中共党员", "未知",
     "区委常委、区纪委书记、区监委主任", "中共北京市房山区纪律检查委员会", "bjfsh.gov.cn/zwgk/ldjs/"),

    ("fangshan_he_jingtao", "何景涛", "男", "汉族", "1971年12月", "未知", "在职研究生", "中共党员", "未知",
     "区委常委、常务副区长", "北京市房山区人民政府", "bjfsh.gov.cn/zwgk/ldjs/"),

    ("fangshan_lei_huan", "雷寰", "女", "苗族", "1974年10月", "未知", "研究生", "中共党员", "未知",
     "区委常委、宣传部部长", "中共北京市房山区委宣传部", "bjfsh.gov.cn/zwgk/ldjs/"),

    ("fangshan_li_jinwei", "李进伟", "男", "汉族", "1976年9月", "未知", "市委党校研究生", "中共党员", "未知",
     "区委常委、政法委书记", "中共北京市房山区委政法委员会", "bjfsh.gov.cn/zwgk/ldjs/"),

    ("fangshan_jin_lu", "靳璐", "女", "汉族", "1984年7月", "未知", "研究生", "中共党员", "未知",
     "区委常委、副区长", "北京市房山区人民政府", "bjfsh.gov.cn/zwgk/ldjs/"),

    ("fangshan_han_xiangjun", "韩向军", "男", "汉族", "1972年12月", "未知", "中央党校大学", "中共党员", "未知",
     "区委常委、区人武部部长", "北京市房山区人民武装部", "bjfsh.gov.cn/zwgk/ldjs/"),

    ("fangshan_zheng_haitao", "郑海涛", "女", "汉族", "1973年3月", "未知", "大学", "中共党员", "未知",
     "区委常委、统战部部长，区政协党组副书记（兼）", "中共北京市房山区委统战部", "bjfsh.gov.cn/zwgk/ldjs/"),

    # ── District Government Vice Heads ──
    ("fangshan_gao_wujun", "高武军", "男", "汉族", "1975年11月", "未知", "市委党校研究生", "民建会员", "未知",
     "副区长", "北京市房山区人民政府", "bjfsh.gov.cn/zwgk/ldjs/"),

    ("fangshan_zhu_feng", "朱峰", "男", "汉族", "1971年3月", "未知", "中央党校研究生", "中共党员", "未知",
     "副区长、公安分局局长", "北京市公安局房山分局", "bjfsh.gov.cn/zwgk/ldjs/"),

    ("fangshan_li_guangming", "李光明", "男", "汉族", "1967年8月", "未知", "市委党校研究生", "中共党员", "未知",
     "副区长（兼），燕山工委书记", "北京市房山区人民政府", "bjfsh.gov.cn/zwgk/ldjs/"),

    ("fangshan_liu_jinhui", "刘金辉", "男", "汉族", "1979年9月", "未知", "研究生", "中共党员", "未知",
     "副区长（赴辽宁沈阳挂职）", "北京市房山区人民政府", "bjfsh.gov.cn/zwgk/ldjs/"),

    ("fangshan_zhang_qi", "张奇", "男", "汉族", "1976年2月", "未知", "研究生", "中共党员", "未知",
     "副区长", "北京市房山区人民政府", "bjfsh.gov.cn/zwgk/ldjs/"),

    ("fangshan_su_zhenyu", "苏震宇", "男", "汉族", "1980年2月", "未知", "研究生", "中共党员", "未知",
     "副区长", "北京市房山区人民政府", "bjfsh.gov.cn/zwgk/ldjs/"),

    ("fangshan_zhao_jinlong", "赵金龙", "男", "汉族", "1978年1月", "未知", "市委党校大学", "中共党员", "未知",
     "副区长", "北京市房山区人民政府", "bjfsh.gov.cn/zwgk/ldjs/"),

    ("fangshan_gao_lichun", "高利春", "男", "汉族", "1984年4月", "未知", "在职研究生", "中共党员", "未知",
     "副区长（挂职）", "北京市房山区人民政府", "bjfsh.gov.cn/zwgk/ldjs/"),

    # ── People's Congress ──
    ("fangshan_liu_bing", "刘兵", "男", "汉族", "1966年8月", "未知", "大学", "中共党员", "未知",
     "区人大常委会党组书记、主任", "北京市房山区人民代表大会常务委员会", "bjfsh.gov.cn/zwgk/ldjs/"),

    ("fangshan_chen_guangli", "陈广利", "男", "汉族", "1969年3月", "未知", "中央党校大学", "中共党员", "未知",
     "区人大常委会党组副书记、副主任、一级巡视员", "北京市房山区人民代表大会常务委员会", "bjfsh.gov.cn/zwgk/ldjs/"),

    ("fangshan_fang_yuxiang", "方玉祥", "男", "满族", "1968年9月", "未知", "市委党校研究生", "中共党员", "未知",
     "区人大常委会副主任", "北京市房山区人民代表大会常务委员会", "bjfsh.gov.cn/zwgk/ldjs/"),

    ("fangshan_hu_jianguang", "胡建光", "男", "汉族", "1969年11月", "未知", "市委党校研究生", "中共党员", "未知",
     "区人大常委会副主任", "北京市房山区人民代表大会常务委员会", "bjfsh.gov.cn/zwgk/ldjs/"),

    ("fangshan_wang_geng", "王耕", "男", "汉族", "1972年6月", "未知", "市委党校研究生", "中共党员", "未知",
     "区人大常委会副主任", "北京市房山区人民代表大会常务委员会", "bjfsh.gov.cn/zwgk/ldjs/"),

    ("fangshan_guo_yanhong", "郭艳红", "女", "汉族", "1969年3月", "未知", "大学", "农工党党员", "未知",
     "区人大常委会副主任（不驻会）、良乡医院院长", "北京市房山区人民代表大会常务委员会", "bjfsh.gov.cn/zwgk/ldjs/"),

    # ── CPPCC ──
    ("fangshan_zhang_houming", "张厚明", "男", "汉族", "1972年4月", "未知", "大学", "中共党员", "未知",
     "区政协党组书记、主席", "中国人民政治协商会议北京市房山区委员会", "bjfsh.gov.cn/zwgk/ldjs/"),

    ("fangshan_yang_dongli", "杨冬立", "男", "汉族", "1969年11月", "未知", "大学", "中共党员", "未知",
     "区政协党组副书记、副主席", "中国人民政治协商会议北京市房山区委员会", "bjfsh.gov.cn/zwgk/ldjs/"),

    ("fangshan_wang_hongying", "王红英", "女", "汉族", "1969年11月", "未知", "市委党校研究生", "中共党员", "未知",
     "区政协副主席", "中国人民政治协商会议北京市房山区委员会", "bjfsh.gov.cn/zwgk/ldjs/"),

    ("fangshan_wang_chunnian", "王春年", "男", "汉族", "1969年2月", "未知", "市委党校大学", "中共党员", "未知",
     "区政协副主席", "中国人民政治协商会议北京市房山区委员会", "bjfsh.gov.cn/zwgk/ldjs/"),

    ("fangshan_xie_baoyuan", "谢宝元", "男", "汉族", "1968年5月", "未知", "大学", "无党派人士", "未知",
     "区政协副主席（不驻会）、区第一医院院长", "中国人民政治协商会议北京市房山区委员会", "bjfsh.gov.cn/zwgk/ldjs/"),

    ("fangshan_liu_qiong", "刘琼", "女", "汉族", "1966年10月", "未知", "在职研究生", "九三学社社员", "未知",
     "区政协副主席（不驻会）", "中国人民政治协商会议北京市房山区委员会", "bjfsh.gov.cn/zwgk/ldjs/"),

    ("fangshan_wang_qing", "王擎", "女", "汉族", "1972年11月", "未知", "在职研究生", "民盟盟员", "未知",
     "区政协副主席（不驻会）", "中国人民政治协商会议北京市房山区委员会", "bjfsh.gov.cn/zwgk/ldjs/"),

    # ── Predecessors ──
    ("fangshan_wei_guangxun", "魏广勋", "男", "汉族", "1965年9月", "未知", "市委党校研究生", "中共党员", "未知",
     "区政协原主席", "中国人民政治协商会议北京市房山区委员会（已离任）", "bjfsh.gov.cn/zwgk/ldjs/"),

    ("fangshan_yan_liping", "晏利平", "男", "汉族", "1972年9月", "未知", "市委党校研究生", "中共党员", "未知",
     "区政协党组成员、机关党组书记", "中国人民政治协商会议北京市房山区委员会", "bjfsh.gov.cn/zwgk/ldjs/"),
]

ORGANIZATIONS = [
    # id, name, type, level, parent, location
    ("fangshan_party_committee", "中共北京市房山区委员会", "党委", "正厅级", "中共北京市委", "北京市房山区"),
    ("fangshan_gov", "北京市房山区人民政府", "政府", "正厅级", "北京市人民政府", "北京市房山区"),
    ("fangshan_discipline", "中共北京市房山区纪律检查委员会", "纪委", "正厅级", "北京市纪委", "北京市房山区"),
    ("fangshan_org_department", "中共北京市房山区委组织部", "党委部门", "正处级", "房山区委", "北京市房山区"),
    ("fangshan_propaganda", "中共北京市房山区委宣传部", "党委部门", "正处级", "房山区委", "北京市房山区"),
    ("fangshan_united_front", "中共北京市房山区委统战部", "党委部门", "正处级", "房山区委", "北京市房山区"),
    ("fangshan_political_legal", "中共北京市房山区委政法委员会", "党委部门", "正处级", "房山区委", "北京市房山区"),
    ("fangshan_armed_forces", "北京市房山区人民武装部", "军队", "正师级", "北京卫戍区", "北京市房山区"),
    ("fangshan_public_security", "北京市公安局房山分局", "公安", "正处级", "北京市公安局", "北京市房山区"),
    ("fangshan_peoples_congress", "北京市房山区人民代表大会常务委员会", "人大", "正厅级", "北京市人大常委会", "北京市房山区"),
    ("fangshan_cppcc", "中国人民政治协商会议北京市房山区委员会", "政协", "正厅级", "北京市政协", "北京市房山区"),
]

# Person → Organization positions
POSITIONS = [
    # person_id, org_id, title, start, end, rank, note

    # ── 阳波（区委书记）──
    ("fangshan_yang_bo", "fangshan_party_committee", "区委书记", "2024-04", "至今", "正厅级", "主持区委全面工作"),
    ("fangshan_yang_bo", "fangshan_gov", "区长", "2022-02", "2024-04", "正厅级", "前任区长职务"),
    ("fangshan_yang_bo", "fangshan_party_committee", "区委副书记", "2021-09", "2024-04", "正厅级", "调任房山区"),
    # 阳波此前在通州区任职

    # ── 底志欣（区长）──
    ("fangshan_di_zhixin", "fangshan_gov", "区长", "2024-06", "至今", "正厅级", "区政府全面工作"),
    ("fangshan_di_zhixin", "fangshan_gov", "代区长", "2024-04", "2024-06", "正厅级", "过渡期"),
    ("fangshan_di_zhixin", "fangshan_party_committee", "区委副书记", "2024-04", "至今", "正厅级", ""),
    # 底志欣此前在丰台区委副书记

    # ── 王洪涛（组织部部长）──
    ("fangshan_wang_hongtao", "fangshan_org_department", "组织部部长", "unknown", "至今", "副厅级", "区委常委"),

    # ── 佟刚（纪委书记）──
    ("fangshan_tong_gang", "fangshan_discipline", "区纪委书记/监委主任", "unknown", "至今", "正厅级", "二级高级监察官"),

    # ── 何景涛（常务副区长）──
    ("fangshan_he_jingtao", "fangshan_gov", "常务副区长", "unknown", "至今", "副厅级", "区委常委、党组副书记"),

    # ── 雷寰（宣传部部长）──
    ("fangshan_lei_huan", "fangshan_propaganda", "宣传部部长", "unknown", "至今", "副厅级", ""),

    # ── 李进伟（政法委书记）──
    ("fangshan_li_jinwei", "fangshan_political_legal", "政法委书记", "unknown", "至今", "副厅级", ""),

    # ── 靳璐（副区长）──
    ("fangshan_jin_lu", "fangshan_gov", "副区长", "unknown", "至今", "副厅级", "区委常委"),

    # ── 韩向军（人武部部长）──
    ("fangshan_han_xiangjun", "fangshan_armed_forces", "人武部部长", "unknown", "至今", "副师级", ""),

    # ── 郑海涛（统战部部长）──
    ("fangshan_zheng_haitao", "fangshan_united_front", "统战部部长", "unknown", "至今", "副厅级", "兼任区政协党组副书记"),

    # ── 区政府副区长 ──
    ("fangshan_gao_wujun", "fangshan_gov", "副区长", "unknown", "至今", "副厅级", "民建会员"),
    ("fangshan_zhu_feng", "fangshan_gov", "副区长", "unknown", "至今", "副厅级", "兼任公安分局局长"),
    ("fangshan_zhu_feng", "fangshan_public_security", "公安分局局长", "unknown", "至今", "正处级", ""),
    ("fangshan_li_guangming", "fangshan_gov", "副区长（兼）", "unknown", "至今", "副厅级", "燕山工委书记"),
    ("fangshan_liu_jinhui", "fangshan_gov", "副区长（挂职）", "unknown", "至今", "副厅级", "赴辽宁沈阳挂职"),
    ("fangshan_zhang_qi", "fangshan_gov", "副区长", "unknown", "至今", "副厅级", ""),
    ("fangshan_su_zhenyu", "fangshan_gov", "副区长", "unknown", "至今", "副厅级", ""),
    ("fangshan_zhao_jinlong", "fangshan_gov", "副区长", "unknown", "至今", "副厅级", ""),
    ("fangshan_gao_lichun", "fangshan_gov", "副区长（挂职）", "unknown", "至今", "副厅级", ""),

    # ── 人大 ──
    ("fangshan_liu_bing", "fangshan_peoples_congress", "主任", "unknown", "至今", "正厅级", ""),
    ("fangshan_chen_guangli", "fangshan_peoples_congress", "副主任", "unknown", "至今", "副厅级", "一级巡视员"),
    ("fangshan_fang_yuxiang", "fangshan_peoples_congress", "副主任", "unknown", "至今", "副厅级", ""),
    ("fangshan_hu_jianguang", "fangshan_peoples_congress", "副主任", "unknown", "至今", "副厅级", ""),
    ("fangshan_wang_geng", "fangshan_peoples_congress", "副主任", "unknown", "至今", "副厅级", ""),
    ("fangshan_guo_yanhong", "fangshan_peoples_congress", "副主任（不驻会）", "unknown", "至今", "副厅级", "良乡医院院长"),

    # ── 政协 ──
    ("fangshan_zhang_houming", "fangshan_cppcc", "主席", "unknown", "至今", "正厅级", ""),
    ("fangshan_yang_dongli", "fangshan_cppcc", "副主席", "unknown", "至今", "副厅级", ""),
    ("fangshan_wang_hongying", "fangshan_cppcc", "副主席", "unknown", "至今", "副厅级", ""),
    ("fangshan_wang_chunnian", "fangshan_cppcc", "副主席", "unknown", "至今", "副厅级", ""),
    ("fangshan_xie_baoyuan", "fangshan_cppcc", "副主席（不驻会）", "unknown", "至今", "副厅级", ""),
    ("fangshan_liu_qiong", "fangshan_cppcc", "副主席（不驻会）", "unknown", "至今", "副厅级", ""),
    ("fangshan_wang_qing", "fangshan_cppcc", "副主席（不驻会）", "unknown", "至今", "副厅级", ""),
    ("fangshan_wei_guangxun", "fangshan_cppcc", "原主席", "unknown", "unknown", "正厅级", "已离任"),
    ("fangshan_yan_liping", "fangshan_cppcc", "机关党组书记", "unknown", "至今", "正处级", ""),
]

RELATIONSHIPS = [
    # person_a, person_b, type, context, overlap_org, overlap_period

    # Top leadership dyads
    ("fangshan_yang_bo", "fangshan_di_zhixin", "predecessor_successor", "前任区长→现任区长（阳波升书记后底志欣接任区长）", "房山区政府", "2024"),
    ("fangshan_yang_bo", "fangshan_di_zhixin", "superior_subordinate", "区委书记→区长，党政一把手搭档", "房山区委/区政府", "2024-至今"),

    # Standing committee working relationships
    ("fangshan_di_zhixin", "fangshan_he_jingtao", "superior_subordinate", "区长→常务副区长", "房山区政府", "至今"),
    ("fangshan_yang_bo", "fangshan_wang_hongtao", "superior_subordinate", "区委书记→组织部部长", "房山区委", "至今"),
    ("fangshan_yang_bo", "fangshan_tong_gang", "superior_subordinate", "区委书记→纪委书记", "房山区委", "至今"),
    ("fangshan_he_jingtao", "fangshan_jin_lu", "overlap", "常务副区长和副区长（区委常委）", "房山区政府", "至今"),
]


# ════════════════════════════════════════════════════════════
# SQLITE BUILD
# ════════════════════════════════════════════════════════════

def build_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE persons (
            id TEXT PRIMARY KEY,
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
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        );
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT NOT NULL,
            org_id TEXT NOT NULL,
            title TEXT,
            start TEXT,
            "end" TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in PERSONS:
        c.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", p)
    for o in ORGANIZATIONS:
        c.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)", o)
    for pos in POSITIONS:
        c.execute("INSERT INTO positions (person_id, org_id, title, start, \"end\", rank, note) VALUES (?,?,?,?,?,?,?)", pos)
    for r in RELATIONSHIPS:
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)", r)

    conn.commit()
    conn.close()


# ════════════════════════════════════════════════════════════
# GEXF BUILD
# ════════════════════════════════════════════════════════════

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def is_top_leader(p):
    return "区委书记" in p[9] and "副书记" not in p[9] or ("区委副书记" in p[9] and "区长" in p[9]) or ("区长" in p[9] and "副书记" in p[9])

def person_color(p):
    role = p[9]
    if "区委书记" in role and "副书记" not in role:
        return "255,50,50"
    if "区长" in role:
        return "50,100,255"
    if "纪委书记" in role or "监委" in role:
        return "255,165,0"
    return "100,100,100"

def org_color(org_type):
    t = org_type or ""
    if "党委" in t:
        return "255,200,200"
    if "政府" in t:
        return "200,200,255"
    if "人大" in t:
        return "200,255,255"
    if "政协" in t:
        return "255,240,200"
    if "纪委" in t:
        return "255,165,0"
    return "200,200,200"

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>北京市房山区领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org_type" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <nodes>')
    for p in PERSONS:
        pid = p[0]
        name = esc(p[1])
        role = esc(p[9])
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="{pid}" label="{name}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{role}"/>')
        lines.append('        </attvalues>')
        cs = c.split(",")
        lines.append(f'        <viz:color r="{cs[0]}" g="{cs[1]}" b="{cs[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in ORGANIZATIONS:
        oid = o[0]
        name = esc(o[1])
        otype = esc(o[2] or "")
        c = org_color(otype)
        lines.append(f'      <node id="{oid}" label="{name}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="2" value="{otype}"/>')
        lines.append('        </attvalues>')
        cs = c.split(",")
        lines.append(f'        <viz:color r="{cs[0]}" g="{cs[1]}" b="{cs[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    for pos in POSITIONS:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="{pos[0]}" target="{pos[1]}" label="{esc(pos[2])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos[5] or "")}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in RELATIONSHIPS:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="{r[0]}" target="{r[1]}" label="{esc(r[3])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r[3])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


# ════════════════════════════════════════════════════════════
# MAIN
# ════════════════════════════════════════════════════════════

def main():
    print("Building 房山区 network database...")
    build_database()
    print(f"  DB: {DB_PATH}")

    print("Building 房山区 network graph...")
    build_gexf()
    print(f"  GEXF: {GEXF_PATH}")

    # Summary stats
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    print()
    print("Summary:")
    for table in ["persons", "organizations", "positions", "relationships"]:
        count = c.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"  {table}: {count}")
    conn.close()
    print()
    print("Done.")


if __name__ == "__main__":
    main()
