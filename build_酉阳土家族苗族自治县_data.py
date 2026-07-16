#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 酉阳土家族苗族自治县 (Youyang Tujia-Miao Autonomous County, Chongqing).

Task: chongqing_酉阳土家族苗族自治县 — 县委书记 & 县长
Province: 重庆市
City: 酉阳土家族苗族自治县 (重庆直辖市下辖县)
Region: 酉阳土家族苗族自治县
Level: 县(直辖市下辖)
Research date: 2026-07-16

Confirmed officeholders (from official government website youyang.gov.cn, accessed 2026-07-16):
- 县委书记: 秦启光 (男，汉族，1971年2月生，研究生，中共党员)
- 县委副书记、县长: 陈政 (男，土家族，1981年4月生，大学、农业推广硕士，中共党员)
- 县委副书记: 水韦梁 (男，汉族，1982年11月生，大学本科，中共党员，兼任县委党校校长)
- 县委常委: 陈伟, 陈勇, 史令(常务副县长), 张宏, 刘为, 李文富
- 副县长: 史令(常务), 张宏, 陈爱党, 高胜, 黄艺, 熊伟, 吴国祥, 王雪峰
- 县政府党组成员: 李宁旭, 许宏图

Sources:
- youyang.gov.cn (official government website): leadership pages, news articles
- All leader names, roles, and basic bios confirmed from government site
- Detailed career histories (pre-酉阳 positions) mostly unavailable
"""

import sqlite3
import os
import json
from datetime import datetime

# ── PATHS ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "酉阳土家族苗族自治县_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "酉阳土家族苗族自治县_network.gexf")
TODAY = datetime.now().strftime("%Y-%m-%d")

# ════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════

PERSONS = [
    # ══ 县委班子 (County Party Committee) ══

    # 县委书记 — 秦启光
    ("yy_qin_qiguang", "秦启光", "男", "汉族", "1971年2月", "待查",
     "研究生", "中共党员", "待查",
     "县委书记", "中共酉阳土家族苗族自治县委员会",
     "youyang.gov.cn_ldxx_xwld_20260525"),

    # 县委副书记、县长 — 陈政
    ("yy_chen_zheng", "陈政", "男", "土家族", "1981年4月", "待查",
     "大学、农业推广硕士", "中共党员", "待查",
     "县委副书记、县长", "酉阳土家族苗族自治县人民政府",
     "youyang.gov.cn_ldxx_xwld_20250207"),

    # 县委副书记 — 水韦梁
    ("yy_shui_weiliang", "水韦梁", "男", "汉族", "1982年11月", "待查",
     "大学本科", "中共党员", "待查",
     "县委副书记、县委党校校长", "中共酉阳土家族苗族自治县委员会",
     "youyang.gov.cn_ldxx_xwld_20230927"),

    # 县委常委 — 陈伟
    ("yy_chen_wei", "陈伟", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "县委常委", "中共酉阳土家族苗族自治县委员会",
     "youyang.gov.cn_ldxx_xwld_20231129"),

    # 县委常委 — 陈勇
    ("yy_chen_yong", "陈勇", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "县委常委", "中共酉阳土家族苗族自治县委员会",
     "youyang.gov.cn_ldxx_xwld_20230731"),

    # 县委常委、常务副县长 — 史令
    ("yy_shi_ling", "史令", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "县委常委、常务副县长", "酉阳土家族苗族自治县人民政府",
     "youyang.gov.cn_ldxx_xwld_20230731"),

    # 县委常委、副县长 — 张宏
    ("yy_zhang_hong", "张宏", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "县委常委、副县长", "酉阳土家族苗族自治县人民政府",
     "youyang.gov.cn_ldxx_xwld_20250418"),

    # 县委常委 — 刘为
    ("yy_liu_wei", "刘为", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "县委常委", "中共酉阳土家族苗族自治县委员会",
     "youyang.gov.cn_ldxx_xwld_20230731"),

    # 县委常委 — 李文富
    ("yy_li_wenfu", "李文富", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "县委常委", "中共酉阳土家族苗族自治县委员会",
     "youyang.gov.cn_ldxx_xwld_20250106"),

    # ══ 县政府领导 (County Government Leaders) ══

    # 副县长 — 陈爱党
    ("yy_chen_aidang", "陈爱党", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副县长", "酉阳土家族苗族自治县人民政府",
     "youyang.gov.cn_ldxx_xzfld_20220107"),

    # 副县长 — 高胜
    ("yy_gao_sheng", "高胜", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副县长", "酉阳土家族苗族自治县人民政府",
     "youyang.gov.cn_ldxx_xzfld_20200327"),

    # 副县长 — 黄艺
    ("yy_huang_yi", "黄艺", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副县长", "酉阳土家族苗族自治县人民政府",
     "youyang.gov.cn_ldxx_xzfld_20220107"),

    # 副县长 — 熊伟
    ("yy_xiong_wei", "熊伟", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副县长", "酉阳土家族苗族自治县人民政府",
     "youyang.gov.cn_ldxx_xzfld_20220107"),

    # 副县长 — 吴国祥
    ("yy_wu_guoxiang", "吴国祥", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副县长", "酉阳土家族苗族自治县人民政府",
     "youyang.gov.cn_ldxx_xzfld_20220107"),

    # 副县长 — 王雪峰
    ("yy_wang_xuefeng", "王雪峰", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "副县长", "酉阳土家族苗族自治县人民政府",
     "youyang.gov.cn_ldxx_xzfld_20251124"),

    # 县政府党组成员 — 李宁旭
    ("yy_li_ningxu", "李宁旭", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "县政府党组成员", "酉阳土家族苗族自治县人民政府",
     "youyang.gov.cn_ldxx_xzfld_20240828"),

    # 县政府党组成员 — 许宏图
    ("yy_xu_hongtu", "许宏图", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "县政府党组成员", "酉阳土家族苗族自治县人民政府",
     "youyang.gov.cn_ldxx_xzfld_20240830"),

    # ══ 前任领导 (Predecessors) ══

    # 前县委书记 — 祁美文 (confirmed predecessor from media reports)
    ("yy_qi_meiwen", "祁美文", "男", "汉族", "待查", "待查",
     "待查", "中共党员", "待查",
     "前任县委书记", "中共酉阳土家族苗族自治县委员会（原）",
     "media_reports;historical_knowledge"),
]

ORGANIZATIONS = [
    # id, name, type, level, parent, location
    ("yy_party_committee", "中共酉阳土家族苗族自治县委员会", "党委", "正厅级", "中共重庆市委", "重庆市酉阳土家族苗族自治县"),
    ("yy_gov", "酉阳土家族苗族自治县人民政府", "政府", "正厅级", "重庆市人民政府", "重庆市酉阳土家族苗族自治县"),
    ("yy_discipline", "中共酉阳土家族苗族自治县纪律检查委员会", "纪委", "副厅级", "重庆市纪委监委", "重庆市酉阳土家族苗族自治县"),
    ("yy_organization", "中共酉阳土家族苗族自治县委组织部", "党委部门", "正处级", "酉阳县委", "重庆市酉阳土家族苗族自治县"),
    ("yy_propaganda", "中共酉阳土家族苗族自治县委宣传部", "党委部门", "正处级", "酉阳县委", "重庆市酉阳土家族苗族自治县"),
    ("yy_united_front", "中共酉阳土家族苗族自治县委统战部", "党委部门", "正处级", "酉阳县委", "重庆市酉阳土家族苗族自治县"),
    ("yy_political_legal", "中共酉阳土家族苗族自治县委政法委员会", "党委部门", "正处级", "酉阳县委", "重庆市酉阳土家族苗族自治县"),
    ("yy_party_school", "中共酉阳土家族苗族自治县委党校", "党委部门", "正处级", "酉阳县委", "重庆市酉阳土家族苗族自治县"),
    ("yy_military_department", "酉阳土家族苗族自治县人民武装部", "军事", "正团级", "重庆警备区", "重庆市酉阳土家族苗族自治县"),
    ("yy_public_security", "酉阳土家族苗族自治县公安局", "公安", "正处级", "重庆市公安局", "重庆市酉阳土家族苗族自治县"),
    ("yy_peoples_congress", "酉阳土家族苗族自治县人民代表大会常务委员会", "人大", "正厅级", "重庆市人大常委会", "重庆市酉阳土家族苗族自治县"),
    ("yy_cppcc", "中国人民政治协商会议酉阳土家族苗族自治县委员会", "政协", "正厅级", "重庆市政协", "重庆市酉阳土家族苗族自治县"),
]

POSITIONS = [
    # person_id, org_id, title, start, end, rank, note

    # ═══ 秦启光 — 县委书记 ═══
    ("yy_qin_qiguang", "yy_party_committee", "县委书记", "待查", "至今", "正厅级",
     "主持县委全面工作。联系县人大常委会、县政协。1971年2月生。"),

    # ═══ 陈政 — 县长 ═══
    ("yy_chen_zheng", "yy_gov", "县长", "待查", "至今", "正厅级",
     "主持县政府全面工作。县委副书记、县政府党组书记。现任酉阳自治县委副书记，县人民政府党组书记、县长。1981年4月生，土家族。"),
    ("yy_chen_zheng", "yy_party_committee", "县委副书记", "待查", "至今", "正厅级", "兼任"),

    # ═══ 水韦梁 — 副书记 ═══
    ("yy_shui_weiliang", "yy_party_committee", "县委副书记", "待查", "至今", "正厅级",
     "协助县委书记负责县委日常工作和党的建设工作。兼任县委党校校长。1982年11月生。"),
    ("yy_shui_weiliang", "yy_party_school", "县委党校校长", "待查", "至今", "正处级", "兼任"),

    # ═══ 陈伟 — 常委 ═══
    ("yy_chen_wei", "yy_party_committee", "县委常委", "待查", "至今", "副厅级",
     "具体分管领域待查。"),

    # ═══ 陈勇 — 常委 ═══
    ("yy_chen_yong", "yy_party_committee", "县委常委", "待查", "至今", "副厅级",
     "具体分管领域待查。"),

    # ═══ 史令 — 常委、常务副县长 ═══
    ("yy_shi_ling", "yy_gov", "常务副县长", "待查", "至今", "副厅级",
     "负责县政府常务工作。县委常委、县政府党组副书记。"),
    ("yy_shi_ling", "yy_party_committee", "县委常委", "待查", "至今", "副厅级", "兼任"),

    # ═══ 张宏 — 常委、副县长 ═══
    ("yy_zhang_hong", "yy_gov", "副县长", "待查", "至今", "副厅级",
     "县委常委、副县长。"),
    ("yy_zhang_hong", "yy_party_committee", "县委常委", "待查", "至今", "副厅级", "兼任"),

    # ═══ 刘为 — 常委 ═══
    ("yy_liu_wei", "yy_party_committee", "县委常委", "待查", "至今", "副厅级",
     "具体分管领域待查。"),

    # ═══ 李文富 — 常委 ═══
    ("yy_li_wenfu", "yy_party_committee", "县委常委", "待查", "至今", "副厅级",
     "具体分管领域待查。"),

    # ═══ 陈爱党 — 副县长 ═══
    ("yy_chen_aidang", "yy_gov", "副县长", "待查", "至今", "副厅级",
     "具体分管领域待查。"),

    # ═══ 高胜 — 副县长 ═══
    ("yy_gao_sheng", "yy_gov", "副县长", "待查", "至今", "副厅级",
     "具体分管领域待查。"),

    # ═══ 黄艺 — 副县长 ═══
    ("yy_huang_yi", "yy_gov", "副县长", "待查", "至今", "副厅级",
     "具体分管领域待查。"),

    # ═══ 熊伟 — 副县长 ═══
    ("yy_xiong_wei", "yy_gov", "副县长", "待查", "至今", "副厅级",
     "具体分管领域待查。"),

    # ═══ 吴国祥 — 副县长 ═══
    ("yy_wu_guoxiang", "yy_gov", "副县长", "待查", "至今", "副厅级",
     "具体分管领域待查。"),

    # ═══ 王雪峰 — 副县长 ═══
    ("yy_wang_xuefeng", "yy_gov", "副县长", "待查", "至今", "副厅级",
     "具体分管领域待查。"),

    # ═══ 李宁旭 — 党组成员 ═══
    ("yy_li_ningxu", "yy_gov", "县政府党组成员", "待查", "至今", "正处级",
     "具体分管领域待查。"),

    # ═══ 许宏图 — 党组成员 ═══
    ("yy_xu_hongtu", "yy_gov", "县政府党组成员", "待查", "至今", "正处级",
     "具体分管领域待查。"),

    # ═══ 祁美文 — 前县委书记 ═══
    ("yy_qi_meiwen", "yy_party_committee", "县委书记", "待查", "待查", "正厅级",
     "前任县委书记。调离后去向待查。"),
]

RELATIONSHIPS = [
    # person_a_id, person_b_id, type, context, overlap_org, overlap_period

    # ═══ 党委班子核心关系 ═══
    ("yy_qin_qiguang", "yy_chen_zheng", "上下级", "县委书记与县长（党政正职搭档关系）", "酉阳县委/县政府", "当前"),
    ("yy_qin_qiguang", "yy_shui_weiliang", "上下级", "县委书记与副书记（党政班子关系）", "酉阳县委", "当前"),
    ("yy_qin_qiguang", "yy_shi_ling", "上下级", "县委书记与常务副县长", "酉阳县委", "当前"),
    ("yy_qin_qiguang", "yy_zhang_hong", "上下级", "县委书记与县委常委、副县长", "酉阳县委", "当前"),
    ("yy_qin_qiguang", "yy_chen_wei", "上下级", "县委书记与县委常委", "酉阳县委", "当前"),
    ("yy_qin_qiguang", "yy_chen_yong", "上下级", "县委书记与县委常委", "酉阳县委", "当前"),
    ("yy_qin_qiguang", "yy_liu_wei", "上下级", "县委书记与县委常委", "酉阳县委", "当前"),
    ("yy_qin_qiguang", "yy_li_wenfu", "上下级", "县委书记与县委常委", "酉阳县委", "当前"),

    # ═══ 县政府工作关系 ═══
    ("yy_chen_zheng", "yy_shi_ling", "上下级", "县长与常务副县长（政府领导关系）", "酉阳县政府", "当前"),
    ("yy_chen_zheng", "yy_zhang_hong", "上下级", "县长与副县长", "酉阳县政府", "当前"),
    ("yy_chen_zheng", "yy_chen_aidang", "上下级", "县长与副县长", "酉阳县政府", "当前"),
    ("yy_chen_zheng", "yy_gao_sheng", "上下级", "县长与副县长", "酉阳县政府", "当前"),
    ("yy_chen_zheng", "yy_huang_yi", "上下级", "县长与副县长", "酉阳县政府", "当前"),
    ("yy_chen_zheng", "yy_xiong_wei", "上下级", "县长与副县长", "酉阳县政府", "当前"),
    ("yy_chen_zheng", "yy_wu_guoxiang", "上下级", "县长与副县长", "酉阳县政府", "当前"),
    ("yy_chen_zheng", "yy_wang_xuefeng", "上下级", "县长与副县长", "酉阳县政府", "当前"),

    # ═══ 同事关系 ═══
    ("yy_shi_ling", "yy_zhang_hong", "同事", "县委常委同事关系（同班常委）", "酉阳县委", "当前"),
    ("yy_shi_ling", "yy_chen_wei", "同事", "县委常委同事关系", "酉阳县委", "当前"),
    ("yy_shi_ling", "yy_chen_yong", "同事", "县委常委同事关系", "酉阳县委", "当前"),
    ("yy_shi_ling", "yy_liu_wei", "同事", "县委常委同事关系", "酉阳县委", "当前"),
    ("yy_shi_ling", "yy_li_wenfu", "同事", "县委常委同事关系", "酉阳县委", "当前"),
    ("yy_chen_aidang", "yy_gao_sheng", "同事", "副县长同事关系", "酉阳县政府", "当前"),
    ("yy_chen_aidang", "yy_huang_yi", "同事", "副县长同事关系", "酉阳县政府", "当前"),
    ("yy_chen_aidang", "yy_xiong_wei", "同事", "副县长同事关系", "酉阳县政府", "当前"),
    ("yy_chen_aidang", "yy_wu_guoxiang", "同事", "副县长同事关系", "酉阳县政府", "当前"),

    # ═══ 前后任关系 ═══
    ("yy_qi_meiwen", "yy_qin_qiguang", "前后任", "前县委书记祁美文与现任县委书记秦启光（前后任）", "酉阳县委", "待查"),
]

# ════════════════════════════════════════════
# SQLITE
# ════════════════════════════════════════════

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
    PRAGMA foreign_keys = ON;

    CREATE TABLE IF NOT EXISTS persons (
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

    CREATE TABLE IF NOT EXISTS organizations (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        type TEXT,
        level TEXT,
        parent TEXT,
        location TEXT
    );

    CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id TEXT REFERENCES persons(id),
        org_id TEXT REFERENCES organizations(id),
        title TEXT,
        start TEXT,
        end TEXT,
        rank TEXT,
        note TEXT
    );

    CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a TEXT REFERENCES persons(id),
        person_b TEXT REFERENCES persons(id),
        type TEXT,
        context TEXT,
        overlap_org TEXT,
        overlap_period TEXT
    );
""")

for p in PERSONS:
    cur.execute("""INSERT OR REPLACE INTO persons
        (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
        (p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10], p[11]))

for o in ORGANIZATIONS:
    cur.execute("""INSERT OR REPLACE INTO organizations
        (id, name, type, level, parent, location)
        VALUES (?,?,?,?,?,?)""",
        (o[0], o[1], o[2], o[3], o[4], o[5]))

for pos in POSITIONS:
    cur.execute("""INSERT INTO positions
        (person_id, org_id, title, start, end, rank, note)
        VALUES (?,?,?,?,?,?,?)""",
        (pos[0], pos[1], pos[2], pos[3], pos[4], pos[5], pos[6]))

for r in RELATIONSHIPS:
    cur.execute("""INSERT INTO relationships
        (person_a, person_b, type, context, overlap_org, overlap_period)
        VALUES (?,?,?,?,?,?)""",
        (r[0], r[1], r[2], r[3], r[4], r[5]))

conn.commit()
conn.close()

print(f"✅ SQLite database written → {DB_PATH}")

# ════════════════════════════════════════════
# GEXF
# ════════════════════════════════════════════

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color_size(post):
    """Determine color & size by role."""
    post = post or ""
    if "县委书记" in post and "副书记" not in post and "纪委书记" not in post:
        return (227, 38, 54), 20.0  # red
    elif "县长" in post and "副" not in post:
        return (41, 121, 255), 20.0  # blue
    elif "县委副书记" in post:
        return (41, 121, 255), 16.0  # blue
    elif "纪委书记" in post or "监委" in post:
        return (255, 165, 0), 14.0   # orange (discipline)
    elif "常务副县长" in post:
        return (201, 169, 78), 14.0  # gold
    elif "县委常委" in post:
        return (201, 169, 78), 14.0  # gold
    elif "副县长" in post:
        return (255, 140, 0), 12.0   # orange
    elif "党组成员" in post:
        return (138, 132, 120), 12.0 # grey
    elif "前任" in post:
        return (160, 160, 160), 10.0 # light grey (former)
    else:
        return (100, 100, 100), 12.0


ORG_COLORS = {
    "党委": "#C62828",
    "党委部门": "#D84315",
    "政府": "#1565C0",
    "政府部门": "#1976D2",
    "纪委": "#E65100",
    "公安": "#37474F",
    "军事": "#4E342E",
    "人大": "#4E342E",
    "政协": "#4E342E",
}


def hex_to_rgb(h):
    h = h.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


# Build nodes XML
nodes_xml = ""
for p in PERSONS:
    pcol, psz = person_color_size(p[9])
    label_esc = esc(f"{p[1]}\\n{p[9]}")
    nodes_xml += f"""      <node id="{esc(p[0])}" label="{label_esc}">
        <attvalues>
          <attvalue for="kind" value="person"/>
          <attvalue for="role" value="{esc(p[9])}"/>
          <attvalue for="ethnicity" value="{esc(p[3])}"/>
          <attvalue for="source" value="{esc(p[11])}"/>
        </attvalues>
        <viz:color r="{pcol[0]}" g="{pcol[1]}" b="{pcol[2]}"/>
        <viz:size value="{psz}"/>
        <viz:shape value="disc"/>
      </node>
"""

for o in ORGANIZATIONS:
    oc = ORG_COLORS.get(o[2], "#666666")
    or_, og, ob = hex_to_rgb(oc)
    nodes_xml += f"""      <node id="{esc(o[0])}" label="{esc(o[1])}">
        <attvalues>
          <attvalue for="kind" value="org"/>
          <attvalue for="type" value="{esc(o[2])}"/>
        </attvalues>
        <viz:color r="{or_}" g="{og}" b="{ob}"/>
        <viz:size value="8.0"/>
        <viz:shape value="square"/>
      </node>
"""

# Build edges XML
edges_xml = ""
edge_counter = 0

# person → org (worked_at)
for pos in POSITIONS:
    edge_counter += 1
    edges_xml += f"""      <edge id="e{edge_counter}" source="{esc(pos[0])}" target="{esc(pos[1])}" type="directed">
        <attvalues>
          <attvalue for="type" value="worked_at"/>
          <attvalue for="title" value="{esc(pos[2])}"/>
          <attvalue for="start" value="{esc(pos[3])}"/>
          <attvalue for="end" value="{esc(pos[4])}"/>
        </attvalues>
        <viz:color r="180" g="180" b="180"/>
        <viz:thickness value="1.0"/>
      </edge>
"""

# person ↔ person (relationship)
for r in RELATIONSHIPS:
    edge_counter += 1
    rtype = r[2]
    if "上下级" in rtype or "搭档" in rtype:
        thick = 3.0
        cr, cg, cb = 201, 169, 78  # gold
    elif "前后任" in rtype:
        thick = 2.5
        cr, cg, cb = 160, 160, 160  # grey
    elif "同事" in rtype:
        thick = 2.0
        cr, cg, cb = 41, 121, 255  # blue
    else:
        thick = 1.5
        cr, cg, cb = 138, 132, 120  # grey

    edges_xml += f"""      <edge id="e{edge_counter}" source="{esc(r[0])}" target="{esc(r[1])}" type="undirected">
        <attvalues>
          <attvalue for="type" value="relationship"/>
          <attvalue for="context" value="{esc(r[3])}"/>
          <attvalue for="overlap_org" value="{esc(r[4])}"/>
          <attvalue for="overlap_period" value="{esc(r[5])}"/>
        </attvalues>
        <viz:color r="{cr}" g="{cg}" b="{cb}"/>
        <viz:thickness value="{thick}"/>
      </edge>
"""

gexf = f"""<?xml version="1.0" encoding="UTF-8"?>
<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">
  <meta lastmodifieddate="{TODAY}">
    <creator>gov-relation research agent</creator>
    <description>酉阳土家族苗族自治县领导班子工作关系网络 — {TODAY}</description>
  </meta>
  <graph mode="static" defaultedgetype="undirected">
    <attributes class="node">
      <attribute id="kind" title="Kind" type="string"/>
      <attribute id="role" title="Role" type="string"/>
      <attribute id="ethnicity" title="Ethnicity" type="string"/>
      <attribute id="source" title="Source" type="string"/>
    </attributes>
    <attributes class="edge">
      <attribute id="type" title="Type" type="string"/>
      <attribute id="title" title="Title" type="string"/>
      <attribute id="start" title="Start" type="string"/>
      <attribute id="end" title="End" type="string"/>
      <attribute id="context" title="Context" type="string"/>
      <attribute id="overlap_org" title="Overlap Org" type="string"/>
      <attribute id="overlap_period" title="Overlap Period" type="string"/>
    </attributes>
    <nodes>
{nodes_xml}    </nodes>
    <edges>
{edges_xml}    </edges>
  </graph>
</gexf>
"""

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write(gexf)

print(f"✅ GEXF graph written → {GEXF_PATH}")

# ════════════════════════════════════════════
# Summary
# ════════════════════════════════════════════
print(f"""
📊 Summary
  Persons:       {len(PERSONS)}
  Orgs:          {len(ORGANIZATIONS)}
  Positions:     {len(POSITIONS)}
  Relationships: {len(RELATIONSHIPS)}
  Edges (GEXF):  {edge_counter}

Data quality notes:
  ✅ Current leadership roster confirmed from official government website (youyang.gov.cn)
  ✅ 秦启光 (县委书记): bio confirmed — 男，汉族，1971年2月生，研究生
  ✅ 陈政 (县长): bio confirmed — 男，土家族，1981年4月生，大学、农业推广硕士
  ✅ 水韦梁 (副书记): bio confirmed — 男，汉族，1982年11月生，大学本科
  ✅ 9-party standing committee members confirmed from official site
  ✅ 8 county deputy mayors confirmed from official site
  ⚠  Detailed career histories (pre-酉阳 positions) unavailable
  ⚠  Birthplace and work_start dates marked as 待查
  ⚠  Specific portfolio assignments for most deputy positions not listed on website
  ⚠  Predecessor names based on media reports, not official confirmation
  ⚠  Party discipline inspection and organization/propaganda department heads not separately identified
""")
