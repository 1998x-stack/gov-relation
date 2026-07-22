#!/usr/bin/env python3
"""
福建省莆田市领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Putian City leadership.

Level: 地级市
Province: 福建省
Targets: 市委书记 & 市长

Research Notes:
- Current 市委书记: 付朝阳 (appointed December 2021, previously 福建省生态环境厅厅长)
- Current 市长: 戴龙成 (appointed October 2024, previously unknown —江苏盐城人)
- Leadership data compiled from Wikipedia (zh.wikipedia.org), putian.gov.cn official website, and public media reports (2026-07-16)
- Career timeline for 付朝阳 from Wikipedia / Baidu Baike / public media reports
- Career timeline for 戴龙成 partially sourced from Wikipedia; some early career details need verification
- Some deputy positions may have gaps; official sources as primary

Sources:
- https://www.putian.gov.cn — official government website (primary)
- https://zh.wikipedia.org/wiki/莆田市 — Wikipedia city page (leadership roster)
- https://zh.wikipedia.org/wiki/付朝阳 — Wikipedia biography
- 中国经济网 — leadership database
- 澎湃新闻 — media reports
"""

import sqlite3
import os
from datetime import datetime

# ── PATHS ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "莆田市_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "莆田市_network.gexf")

# ════════════════════════════════════════════
# DATA
# ════════════════════════════════════════════

PERSONS = [
    # id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source

    # ══ 市委班子 (Party Committee) ══
    ("pt_fu_zhaoyang", "付朝阳", "男", "汉族", "1972年10月", "湖南攸县",
     "中南林学院/清华大学（校友）", "中共党员", "1993年？",
     "市委书记", "中共莆田市委员会",
     "wikipedia;putian.gov.cn;media_reports"),

    ("pt_dai_longcheng", "戴龙成", "男", "汉族", "1976年5月", "江苏盐城",
     "待查", "中共党员", "待查",
     "市委副书记、市长", "莆田市人民政府",
     "wikipedia;putian.gov.cn;media_reports"),

    ("pt_guo_songyu", "郭宋玉", "女", "汉族", "1973年5月", "待查",
     "待查", "中共党员", "待查",
     "市委副书记（专职）", "中共莆田市委员会",
     "wikipedia"),

    ("pt_huang_zhenyao", "黄珍耀", "男", "汉族", "1974年7月", "待查",
     "待查", "中共党员", "待查",
     "市委常委、统战部部长、市总工会主席", "中共莆田市委统战部",
     "wikipedia"),

    ("pt_li_shaoqun", "李少群", "男", "汉族", "1975年1月", "待查",
     "待查", "中共党员", "待查",
     "市委常委、组织部部长、市直机关工委书记", "中共莆田市委组织部",
     "wikipedia"),

    ("pt_chen_huqian", "陈惠黔", "男", "汉族", "1965年10月", "待查",
     "待查", "中共党员", "待查",
     "市委常委、宣传部部长", "中共莆田市委宣传部",
     "wikipedia"),

    ("pt_gao_yu", "高宇", "男", "汉族", "1974年8月", "待查",
     "待查", "中共党员", "待查",
     "市委常委、常务副市长", "莆田市人民政府",
     "wikipedia"),

    ("pt_zheng_jiaqing", "郑加清", "男", "汉族", "1967年1月", "待查",
     "待查", "中共党员", "待查",
     "市委常委、政法委书记", "中共莆田市委政法委员会",
     "wikipedia"),

    ("pt_lin_jianwei", "林建伟", "男", "汉族", "1976年9月", "福建福州",
     "待查", "中共党员", "待查",
     "市委常委、市纪委书记、市监委主任", "中共莆田市纪律检查委员会",
     "wikipedia"),

    ("pt_zhu_zhengyang", "朱正扬", "男", "汉族", "1975年1月", "待查",
     "待查", "中共党员", "待查",
     "市委常委、秘书长", "中共莆田市委办公室",
     "wikipedia;putian.gov.cn"),

    # ══ 人大班子 ══
    ("pt_su_yongge", "苏永革", "男", "汉族", "1966年12月", "福建福安",
     "待查", "中共党员", "待查",
     "市人大常委会主任", "莆田市人大常委会",
     "wikipedia"),

    # ══ 政协班子 ══
    ("pt_shen_mengya", "沈萌芽", "女", "汉族", "1966年11月", "江苏常州",
     "待查", "中共党员", "待查",
     "市政协主席", "政协莆田市委员会",
     "wikipedia"),

    # ══ 前任领导 ══
    ("pt_liu_jianyang", "刘建洋", "男", "汉族", "1966年4月", "待查",
     "待查", "中共党员", "待查",
     "前任市委书记", "中共莆田市委员会（原）",
     "wikipedia;media_reports"),

    ("pt_lin_xuyang", "林旭阳", "男", "汉族", "1975年5月", "福建莆田（福建安溪出生）",
     "在职研究生/经济学硕士（厦门大学）", "中共党员", "1998年？",
     "前任市长", "莆田市人民政府（原）",
     "wikipedia;media_reports;沙坪坝区_data"),
]

ORGANIZATIONS = [
    # id, name, type, level, parent, location

    # ══ 党政机构 ══
    ("pt_party_committee", "中共莆田市委员会", "党委", "地厅级", "中共福建省委员会", "福建省莆田市"),
    ("pt_gov", "莆田市人民政府", "政府", "地厅级", "福建省人民政府", "福建省莆田市"),
    ("pt_discipline", "中共莆田市纪律检查委员会", "纪委", "地厅级", "中共福建省纪律检查委员会", "福建省莆田市"),

    # ══ 职能部门 ══
    ("pt_organization", "中共莆田市委组织部", "党委部门", "正处级", "中共莆田市委员会", "福建省莆田市"),
    ("pt_propaganda", "中共莆田市委宣传部", "党委部门", "正处级", "中共莆田市委员会", "福建省莆田市"),
    ("pt_united_front", "中共莆田市委统战部", "党委部门", "正处级", "中共莆田市委员会", "福建省莆田市"),
    ("pt_political_legal", "中共莆田市委政法委员会", "党委部门", "正处级", "中共莆田市委员会", "福建省莆田市"),
    ("pt_general_office", "中共莆田市委办公室", "党委部门", "正处级", "中共莆田市委员会", "福建省莆田市"),

    # ══ 人大/政协 ══
    ("pt_npc", "莆田市人大常委会", "人大", "地厅级", "福建省人大常委会", "福建省莆田市"),
    ("pt_cppcc", "政协莆田市委员会", "政协", "地厅级", "福建省政协", "福建省莆田市"),

    # ══ 前任关联机构 ══
    ("fj_eco_environment", "福建省生态环境厅", "政府组成部门", "正厅级", "福建省人民政府", "福建省福州市"),
    ("fj_env_protection", "福建省环境保护厅", "政府组成部门", "正厅级", "福建省人民政府", "福建省福州市"),
    ("fj_gov_office", "福建省人民政府办公厅", "政府组成部门", "正厅级", "福建省人民政府", "福建省福州市"),
    ("min_environ_protection", "中华人民共和国环境保护部", "中央政府组成部门", "正部级", "中华人民共和国国务院", "北京市"),
    ("ndrc", "中华人民共和国国家发展和改革委员会", "中央政府组成部门", "正部级", "中华人民共和国国务院", "北京市"),
    ("forestry_ministry", "中华人民共和国林业部", "中央政府组成部门", "正部级", "中华人民共和国国务院", "北京市"),
    ("csfu", "中南林学院", "事业单位/高校", "待查", "湖南省", "湖南省株洲市"),
]

POSITIONS = [
    # person_id, org_id, title, start, end, rank, note

    # ══ 付朝阳 ══
    ("pt_fu_zhaoyang", "pt_party_committee", "市委书记", "2021-12", "present", "正厅级",
     "莆田军分区党委第一书记。前任：刘建洋"),

    ("pt_fu_zhaoyang", "fj_eco_environment", "厅长", "2018-10", "2021-12", "正厅级",
     "福建省生态环境厅首任厅长（由省环保厅更名而来）"),
    ("pt_fu_zhaoyang", "fj_env_protection", "党组书记、厅长", "2018-03", "2018-10", "正厅级",
     "福建省环境保护厅最后一任厅长"),
    ("pt_fu_zhaoyang", "fj_gov_office", "副主任、省金融办主任", "2016", "2018-03", "副厅级",
     "福建省人民政府办公厅副主任、党组成员，省金融办主任"),
    ("pt_fu_zhaoyang", "fj_env_protection", "副厅长", "2013", "2016", "副厅级",
     "福建省环境保护厅副厅长、党组成员"),
    ("pt_fu_zhaoyang", "min_environ_protection", "办公厅副主任", "待查", "2013", "副司级",
     "挂职任中共福建省泉州市委常委、副市长"),
    ("pt_fu_zhaoyang", "ndrc", "干部", "待查", "待查", "待查",
     "在国家发改委任职"),
    ("pt_fu_zhaoyang", "forestry_ministry", "干部", "待查", "待查", "待查",
     "在林业部任职"),
    ("pt_fu_zhaoyang", "csfu", "助理工程师", "待查", "待查", "待查",
     "中南林学院研究室任助理工程师"),

    # ══ 戴龙成 ══
    ("pt_dai_longcheng", "pt_party_committee", "市委副书记", "2024-10", "present", "正厅级",
     "兼任市长"),
    ("pt_dai_longcheng", "pt_gov", "市长", "2024-10", "present", "正厅级",
     "前任：林旭阳（2024年10月跨省交流至重庆）"),

    # ══ 郭宋玉（专职副书记） ══
    ("pt_guo_songyu", "pt_party_committee", "市委副书记", "至今", "present", "副厅级",
     "专职副书记"),

    # ══ 黄珍耀（统战部长） ══
    ("pt_huang_zhenyao", "pt_united_front", "市委常委、统战部部长、市总工会主席", "至今", "present", "副厅级", ""),

    # ══ 李少群（组织部长） ══
    ("pt_li_shaoqun", "pt_organization", "市委常委、组织部部长、市直机关工委书记", "至今", "present", "副厅级", ""),

    # ══ 陈惠黔（宣传部长） ══
    ("pt_chen_huqian", "pt_propaganda", "市委常委、宣传部部长", "至今", "present", "副厅级", ""),

    # ══ 高宇（常务副市长） ══
    ("pt_gao_yu", "pt_gov", "市委常委、常务副市长", "至今", "present", "副厅级", ""),

    # ══ 郑加清（政法委书记） ══
    ("pt_zheng_jiaqing", "pt_political_legal", "市委常委、政法委书记", "至今", "present", "副厅级", ""),

    # ══ 林建伟（纪委书记） ══
    ("pt_lin_jianwei", "pt_discipline", "市委常委、市纪委书记、市监委主任", "2024-01", "present", "副厅级", ""),

    # ══ 朱正扬（秘书长） ══
    ("pt_zhu_zhengyang", "pt_general_office", "市委常委、秘书长", "至今", "present", "副厅级", ""),

    # ══ 苏永革（人大主任） ══
    ("pt_su_yongge", "pt_npc", "市人大常委会主任", "2022-01", "present", "正厅级", ""),

    # ══ 沈萌芽（政协主席） ══
    ("pt_shen_mengya", "pt_cppcc", "市政协主席", "2022-01", "present", "正厅级", ""),

    # ══ 前任领导 ══
    ("pt_liu_jianyang", "pt_party_committee", "市委书记", "2019-12", "2021-12", "正厅级",
     "前任书记，后调任（去向待查）"),
    ("pt_lin_xuyang", "pt_gov", "市长", "2021-08", "2024-10", "正厅级",
     "前任市长，2024年10月跨省交流至重庆任沙坪坝区委书记"),
]

RELATIONSHIPS = [
    # person_a, person_b, type, context, overlap_org, overlap_period

    # ══ 付朝阳与前书记 ══
    ("pt_fu_zhaoyang", "pt_liu_jianyang", "predecessor_successor",
     "刘建洋2019年12月至2021年12月任莆田市委书记，付朝阳接任",
     "中共莆田市委员会", "2019-12至2021-12"),

    # ══ 戴龙成与前市长 ══
    ("pt_dai_longcheng", "pt_lin_xuyang", "predecessor_successor",
     "林旭阳2021年8月至2024年10月任莆田市长，戴龙成接任",
     "莆田市人民政府", "2021-08至2024-10"),

    # ══ 付朝阳与戴龙成（当前党政一把手） ══
    ("pt_fu_zhaoyang", "pt_dai_longcheng", "overlap",
     "2024年10月起共同担任莆田市党政一把手",
     "中共莆田市委员会、莆田市人民政府", "2024-10至今"),

    # ══ 付朝阳与人大主任 ══
    ("pt_fu_zhaoyang", "pt_su_yongge", "overlap",
     "2022年起在莆田市党政班子和人大班子共同工作",
     "中共莆田市委员会", "2022-01至今"),

    # ══ 付朝阳与朱正扬 ══
    ("pt_fu_zhaoyang", "pt_zhu_zhengyang", "superior_subordinate",
     "朱正扬作为市委常委、秘书长，在工作上直接服务付朝阳",
     "中共莆田市委员会", "至今"),

    # ══ 林旭阳与付朝阳（短暂共事） ══
    ("pt_lin_xuyang", "pt_fu_zhaoyang", "overlap",
     "付朝阳任市委书记期间，林旭阳先任市长约3年",
     "中共莆田市委员会、莆田市人民政府", "2021-12至2024-10"),
]


# ════════════════════════════════════════════
# BUILD
# ════════════════════════════════════════════

def build_sqlite():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute('''CREATE TABLE persons(
        id TEXT PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
    )''')
    c.execute('''CREATE TABLE organizations(
        id TEXT PRIMARY KEY, name TEXT, type TEXT, level TEXT,
        parent TEXT, location TEXT
    )''')
    c.execute('''CREATE TABLE positions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id TEXT, org_id TEXT, title TEXT, start TEXT,
        "end" TEXT, rank TEXT, note TEXT,
        FOREIGN KEY(person_id) REFERENCES persons(id),
        FOREIGN KEY(org_id) REFERENCES organizations(id)
    )''')
    c.execute('''CREATE TABLE relationships(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a TEXT, person_b TEXT, type TEXT, context TEXT,
        overlap_org TEXT, overlap_period TEXT,
        FOREIGN KEY(person_a) REFERENCES persons(id),
        FOREIGN KEY(person_b) REFERENCES persons(id)
    )''')

    for p in PERSONS:
        c.execute("INSERT INTO persons VALUES(?,?,?,?,?,?,?,?,?,?,?,?)", p)
    for o in ORGANIZATIONS:
        c.execute("INSERT INTO organizations VALUES(?,?,?,?,?,?)", o)
    for pos in POSITIONS:
        c.execute("INSERT INTO positions(person_id,org_id,title,start,\"end\",rank,note) VALUES(?,?,?,?,?,?,?)",
                  pos)
    for r in RELATIONSHIPS:
        c.execute("INSERT INTO relationships(person_a,person_b,type,context,overlap_org,overlap_period) VALUES(?,?,?,?,?,?)",
                  r)

    conn.commit()
    conn.close()
    print(f"SQLite database written: {DB_PATH}")


def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(name):
    """Return GEXF color by role."""
    color_map = {
        "付朝阳": "255,50,50",
        "戴龙成": "50,100,255",
        "刘建洋": "100,100,100",
        "林旭阳": "100,100,255",
    }
    return color_map.get(name, "100,100,100")


def org_color(org_type):
    cm = {
        "党委": "255,200,200",
        "党委部门": "255,200,200",
        "政府": "200,200,255",
        "政府组成部门": "200,200,255",
        "纪委": "255,165,0",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "事业单位": "220,220,220",
        "中央政府组成部门": "200,200,255",
    }
    return cm.get(org_type, "200,200,200")


def is_top_leader(name):
    return name in ("付朝阳", "戴龙成")


def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append(
        '<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(
        f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Claude Code Research Agent</creator>')
    lines.append(
        '    <description>福建省莆田市领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append(
        '  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org_type" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes: persons
    person_ids = {}
    lines.append('    <nodes>')
    for p in PERSONS:
        pid = p[0]
        name = p[1]
        person_ids[pid] = name
        c = person_color(name)
        sz = "20.0" if is_top_leader(name) else "12.0"
        role = p[9]  # current_post
        lines.append(f'      <node id="{pid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
        lines.append('        </attvalues>')
        lines.append(
            f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes: organizations
    org_ids = {}
    for o in ORGANIZATIONS:
        oid = o[0]
        org_ids[oid] = o[1]
        c = org_color(o[2])
        lines.append(f'      <node id="{oid}" label="{esc(o[1])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(
            f'          <attvalue for="2" value="{esc(o[2])}"/>')
        lines.append('        </attvalues>')
        lines.append(
            f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges: person -> organization (worked_at)
    eid = 0
    lines.append('    <edges>')
    for pos in POSITIONS:
        pid = pos[0]
        oid = pos[1]
        title = pos[2]
        period = f"{pos[3]}-{pos[4]}"
        lines.append(
            f'      <edge id="e{eid}" source="{pid}" target="{oid}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(
            f'          <attvalue for="1" value="{esc(period)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Edges: person <-> person (relationship)
    for r in RELATIONSHIPS:
        pa, pb = r[0], r[1]
        rtype = r[2]
        period = r[5] or ""
        lines.append(
            f'      <edge id="e{eid}" source="{pa}" target="{pb}" label="{esc(rtype)}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(
            f'          <attvalue for="0" value="{esc(rtype)}"/>')
        lines.append(
            f'          <attvalue for="1" value="{esc(period)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF graph written: {GEXF_PATH}")


if __name__ == "__main__":
    build_sqlite()
    build_gexf()
    print("Done.")
