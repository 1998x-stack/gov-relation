#!/usr/bin/env python3
"""
九江市浔阳区领导班子工作关系网络 — 数据构建脚本
Generates SQLite database + GEXF graph for Xunyang District leadership.
"""

import sqlite3
import os

# ── DATA ──
# Person ID convention: xunyang_{surname_givenname}

PERSONS = [
    # id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source
    # ═══ Top leaders ═══
    ("xunyang_zhou_rongqing", "周荣卿", "男", "汉族", "1974年?月", "未知", "未知", "中共党员", "未知",
     "区委书记", "中共九江市浔阳区委员会", "https://www.xunyang.gov.cn (区委主要领导)"),
    ("xunyang_tang_jianyu", "唐建宇", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区委副书记、区长候选人", "九江市浔阳区人民政府", "https://www.xunyang.gov.cn (区长候选人)"),
    ("xunyang_zha_zhongping", "查忠平", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区委副书记", "中共九江市浔阳区委员会", "https://www.xunyang.gov.cn (区委副书记)"),

    # ═══ Standing committee / 区委常委 ═══
    ("xunyang_ding_yonghao", "丁永豪", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区委常委、常务副区长(推测)", "九江市浔阳区人民政府", "https://www.xunyang.gov.cn (防汛报道)"),
    ("xunyang_li_qifang", "李奇芳", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区委常委、组织部部长(推测)", "中共九江市浔阳区委组织部", "https://www.xunyang.gov.cn (人大换届工作会)"),
    ("xunyang_liu_guodong", "刘国栋", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区委常委(推测)", "中共九江市浔阳区委员会", "https://www.xunyang.gov.cn (防汛报道)"),
    ("xunyang_huang_he", "黄河", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区委常委(推测)", "中共九江市浔阳区委员会", "https://www.xunyang.gov.cn (防汛报道)"),
    ("xunyang_xiong_yan", "熊燕", "女", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区委常委(推测)", "中共九江市浔阳区委员会", "https://www.xunyang.gov.cn (防汛会商会)"),

    # ═══ District leaders ═══
    ("xunyang_leiting_jun", "雷霆钧", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "副区长（推测）", "九江市浔阳区人民政府", "https://www.xunyang.gov.cn (防汛会商会)"),
    ("xunyang_wang_jing", "王静", "女", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "副区长（推测）", "九江市浔阳区人民政府", "https://www.xunyang.gov.cn (防汛会商会)"),
    ("xunyang_hu_hao", "胡皓", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "副区长（推测）", "九江市浔阳区人民政府", "https://www.xunyang.gov.cn (防汛会商会)"),

    # ═══ NPC / 人大 ═══
    ("xunyang_xu_liwen", "徐礼文", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区人大常委会主任", "九江市浔阳区人民代表大会常务委员会", "https://www.xunyang.gov.cn (人大换届工作会)"),
    ("xunyang_luo_zejun", "骆泽君", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区人大常委会副主任（推测）", "九江市浔阳区人民代表大会常务委员会", "https://www.xunyang.gov.cn (人大换届工作会)"),
    ("xunyang_qin_yonghong", "秦永红", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区人大常委会副主任（推测）", "九江市浔阳区人民代表大会常务委员会", "https://www.xunyang.gov.cn (人大换届工作会)"),
    ("xunyang_xu_yanting", "徐艳婷", "女", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区人大常委会副主任（推测）", "九江市浔阳区人民代表大会常务委员会", "https://www.xunyang.gov.cn (人大换届工作会)"),
    ("xunyang_pan_junjun", "潘俊俊", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "区人大常委会副主任（推测）", "九江市浔阳区人民代表大会常务委员会", "https://www.xunyang.gov.cn (人大换届工作会)"),

    # ═══ Historical predecessors ═══
    ("xunyang_zhang_ning", "张宁", "男", "汉族", "1974年", "未知", "未知", "中共党员", "未知",
     "前任区委书记(2024年前)", "中共九江市浔阳区委员会（已离任）", "https://zh.wikipedia.org/wiki/张宁_(1974年)"),
    ("xunyang_qian_zhimin", "钱志敏", "男", "汉族", "未知", "未知", "未知", "中共党员", "未知",
     "前任区长（推测）", "九江市浔阳区人民政府（已离任）", "https://www.xunyang.gov.cn (历史报道)"),

    # ═══ Cross‑district connections ═══
    ("xunyang_chen_yun", "陈云", "男", "汉族", "1976-12", "江西南昌", "江西师范大学", "中共党员", "",
     "九江市委书记", "中共九江市委员会", "https://zh.wikipedia.org/wiki/陈云_(1976年)"),
    ("xunyang_deng_yongxiang", "邓永翔", "男", "汉族", "1977-02", "江西南昌", "", "中共党员", "",
     "九江市委副书记、市长", "九江市人民政府", "https://zh.wikipedia.org/wiki/九江市"),
]

ORGANIZATIONS = [
    # id, name, type, level, parent, location
    ("xunyang_party_committee", "中共九江市浔阳区委员会", "党委", "县级", "中共九江市委", "九江市浔阳区"),
    ("xunyang_gov", "九江市浔阳区人民政府", "政府", "县级", "九江市人民政府", "九江市浔阳区"),
    ("xunyang_org_department", "中共九江市浔阳区委组织部", "党委部门", "正科级", "浔阳区委", "九江市浔阳区"),
    ("xunyang_discipline", "中共九江市浔阳区纪律检查委员会", "纪委", "县级", "九江市纪委", "九江市浔阳区"),
    ("xunyang_propaganda", "中共九江市浔阳区委宣传部", "党委部门", "正科级", "浔阳区委", "九江市浔阳区"),
    ("xunyang_political_legal", "中共九江市浔阳区委政法委员会", "党委部门", "正科级", "浔阳区委", "九江市浔阳区"),
    ("xunyang_armed_forces", "九江市浔阳区人民武装部", "军队", "县级", "九江军分区", "九江市浔阳区"),
    ("xunyang_npc", "九江市浔阳区人民代表大会常务委员会", "人大", "县级", "九江市人大常委会", "九江市浔阳区"),
    ("xunyang_cppcc", "中国人民政治协商会议九江市浔阳区委员会", "政协", "县级", "九江市政府", "九江市浔阳区"),
    ("xunyang_public_security", "九江市公安局浔阳分局", "公安", "正科级", "九江市公安局", "九江市浔阳区"),
    # City-level orgs
    ("jiujiang_party", "中共九江市委员会", "党委", "地市级", "中共江西省委员会", "江西省九江市"),
    ("jiujiang_gov", "九江市人民政府", "政府", "地市级", "江西省人民政府", "江西省九江市"),
    # Neighboring districts
    ("lianxi_party", "中共九江市濂溪区委员会", "党委", "县级", "中共九江市委", "九江市濂溪区"),
    ("chaishang_party", "中共九江市柴桑区委员会", "党委", "县级", "中共九江市委", "九江市柴桑区"),
]

POSITIONS = [
    # person_id, org_id, title, start, end, rank, note

    # ═══ 周荣卿 — 区委书记 ═══
    ("xunyang_zhou_rongqing", "xunyang_party_committee", "区委书记", "~2024", "至今", "正县级", "主持区委全面工作"),
    ("xunyang_zhou_rongqing", "xunyang_gov", "区长（推测）", "~2021", "~2024", "正县级", "从区长升任书记"),
    ("xunyang_zhou_rongqing", "jiujiang_party", "市委部门任职（推测）", "~2016", "~2021", "副县级", "具体职务待查"),

    # ═══ 唐建宇 — 区长候选人 ═══
    ("xunyang_tang_jianyu", "xunyang_party_committee", "区委副书记", "2026-07", "至今", "正县级", "兼任区长候选人"),
    ("xunyang_tang_jianyu", "xunyang_gov", "区长候选人", "2026-07", "至今", "正县级", "待人大选举"),
    ("xunyang_tang_jianyu", "jiujiang_party", "市委部门任职（推测）", "未知", "2026-07", "未知", "来浔阳区前职务待查"),

    # ═══ 查忠平 — 区委副书记 ═══
    ("xunyang_zha_zhongping", "xunyang_party_committee", "区委副书记", "~2024", "至今", "副县级", "分管党务/政法/信访/群团"),

    # ═══ 丁永豪 — 常务副区长(推测) ═══
    ("xunyang_ding_yonghao", "xunyang_gov", "常务副区长(推测)", "~2024", "至今", "副县级", "在防汛报道中排位靠前"),

    # ═══ 李奇芳 — 组织部部长(推测) ═══
    ("xunyang_li_qifang", "xunyang_org_department", "组织部部长(推测)", "~2024", "至今", "副县级", "区人大换届工作会排位靠前"),

    # ═══ 刘国栋 ═══
    ("xunyang_liu_guodong", "xunyang_party_committee", "区委常委", "~2024", "至今", "副县级", "具体职务待查"),

    # ═══ 黄河 ═══
    ("xunyang_huang_he", "xunyang_party_committee", "区委常委", "~2024", "至今", "副县级", "具体职务待查"),

    # ═══ 熊燕 ═══
    ("xunyang_xiong_yan", "xunyang_party_committee", "区委常委", "~2024", "至今", "副县级", "具体职务待查"),

    # ═══ 雷霆钧 ═══
    ("xunyang_leiting_jun", "xunyang_gov", "副区长(推测)", "~2024", "至今", "副县级", "区领导"),

    # ═══ 王静 ═══
    ("xunyang_wang_jing", "xunyang_gov", "副区长(推测)", "~2024", "至今", "副县级", "区领导"),

    # ═══ 胡皓 ═══
    ("xunyang_hu_hao", "xunyang_gov", "副区长(推测)", "~2024", "至今", "副县级", "区领导"),

    # ═══ 徐礼文 — 人大主任 ═══
    ("xunyang_xu_liwen", "xunyang_npc", "区人大常委会主任", "~2021", "至今", "正县级", "区人大主任"),

    # ═══ 骆泽君 ═══
    ("xunyang_luo_zejun", "xunyang_npc", "区人大常委会副主任(推测)", "~2024", "至今", "副县级", ""),

    # ═══ 秦永红 ═══
    ("xunyang_qin_yonghong", "xunyang_npc", "区人大常委会副主任(推测)", "~2024", "至今", "副县级", ""),

    # ═══ 徐艳婷 ═══
    ("xunyang_xu_yanting", "xunyang_npc", "区人大常委会副主任(推测)", "~2024", "至今", "副县级", ""),

    # ═══ 潘俊俊 ═══
    ("xunyang_pan_junjun", "xunyang_npc", "区人大常委会副主任(推测)", "~2024", "至今", "副县级", ""),

    # ═══ 前任 ═══
    ("xunyang_zhang_ning", "xunyang_party_committee", "区委书记(前任)", "~2021", "~2024", "正县级", "前任区委书记，去向待查"),
    ("xunyang_qian_zhimin", "xunyang_gov", "区长(前任推测)", "~2016", "~2021", "正县级", "前任区长，去向待查"),

    # ═══ Cross-district connections ═══
    ("xunyang_chen_yun", "jiujiang_party", "九江市委书记", "2026-05", "至今", "正厅级", "2026年5月上任"),
    ("xunyang_deng_yongxiang", "jiujiang_gov", "九江市委副书记、市长", "2026-05", "至今", "正厅级", "2026年5月上任"),
]

RELATIONSHIPS = [
    # person_a, person_b, type, context, overlap_org, overlap_period

    # ═══ Strong relationships (confirmed co-workers) ═══
    ("xunyang_zhou_rongqing", "xunyang_tang_jianyu", "强关系", "党政搭档（书记+区长候选人）", "浔阳区", "2026-07至今"),
    ("xunyang_zhou_rongqing", "xunyang_zha_zhongping", "强关系", "书记+副书记搭班子", "浔阳区", "~2024至今"),
    ("xunyang_zhou_rongqing", "xunyang_xu_liwen", "强关系", "区委+人大负责人共事", "浔阳区", "~2024至今"),
    ("xunyang_zhou_rongqing", "xunyang_zhang_ning", "强关系", "前后任区委书记", "浔阳区", "~2024（交接）"),

    # ═══ Weak relationships (current co-workers) ═══
    ("xunyang_zhou_rongqing", "xunyang_ding_yonghao", "弱关系", "现任班子共事", "浔阳区", "~2024至今"),
    ("xunyang_zhou_rongqing", "xunyang_li_qifang", "弱关系", "现任班子共事", "浔阳区", "~2024至今"),
    ("xunyang_zhou_rongqing", "xunyang_liu_guodong", "弱关系", "现任班子共事", "浔阳区", "~2024至今"),
    ("xunyang_zhou_rongqing", "xunyang_huang_he", "弱关系", "现任班子共事", "浔阳区", "~2024至今"),
    ("xunyang_zhou_rongqing", "xunyang_xiong_yan", "弱关系", "现任班子共事", "浔阳区", "~2024至今"),
    ("xunyang_tang_jianyu", "xunyang_zha_zhongping", "弱关系", "现任班子共事", "浔阳区", "2026-07至今"),
    ("xunyang_tang_jianyu", "xunyang_ding_yonghao", "弱关系", "现任班子共事（政府线）", "浔阳区人民政府", "2026-07至今"),
    ("xunyang_ding_yonghao", "xunyang_leiting_jun", "弱关系", "政府班子共事", "浔阳区人民政府", "~2024至今"),
    ("xunyang_ding_yonghao", "xunyang_wang_jing", "弱关系", "政府班子共事", "浔阳区人民政府", "~2024至今"),
    ("xunyang_ding_yonghao", "xunyang_hu_hao", "弱关系", "政府班子共事", "浔阳区人民政府", "~2024至今"),

    # ═══ Cross-district connections ═══
    ("xunyang_zhou_rongqing", "xunyang_chen_yun", "弱关系", "区县干部与市委领导上下级", "九江市", "~2024至今"),
    ("xunyang_tang_jianyu", "xunyang_chen_yun", "弱关系", "新任区长候选人与市委领导", "九江市", "2026-07至今"),
]

# ── BUILD DATABASE ──

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "data/database/xunyang_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/xunyang_network.gexf")


def create_db():
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
            title TEXT NOT NULL,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT NOT NULL,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    # Insert persons
    for p in PERSONS:
        c.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", p)

    # Insert organizations
    for o in ORGANIZATIONS:
        c.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)", o)

    # Insert positions
    for pos in POSITIONS:
        c.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)", pos)

    # Insert relationships
    for r in RELATIONSHIPS:
        c.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)", r)

    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")


def generate_gexf():
    """Generate GEXF 1.3 with viz namespace using string formatting."""

    # Color scheme
    node_colors = {
        # Roles -> (r,g,b) for party, gov, discipline, other
        "party": (212, 52, 46),       # red
        "gov_leader": (51, 102, 204),  # blue
        "gov_deputy": (80, 130, 200),  # lighter blue
        "discipline": (204, 119, 34),  # orange
        "other": (102, 102, 102),      # grey
        "org_party": (85, 51, 51),     # dark red
        "org_gov": (51, 68, 85),       # dark blue
        "org_other": (68, 68, 68),     # dark grey
    }

    def color_for_person(pid):
        """Determine node color based on person's role."""
        for p in PERSONS:
            if p[0] == pid:
                post = p[9] or ""
                if "书记" in post and "区委" in post:
                    return "party", 20.0
                elif "代区长" in post or "区长候选人" in post or "区长" in post:
                    return "gov_leader", 20.0
                elif "常务副区长" in post:
                    return "gov_leader", 16.0
                elif "副区长" in post:
                    return "gov_deputy", 14.0
                elif "人大常委会主任" in post:
                    return "gov_leader", 16.0
                elif "人大常委会副主任" in post:
                    return "gov_deputy", 14.0
                elif "区委副书记" in post:
                    return "gov_leader", 16.0
                elif "纪委书记" in post:
                    return "discipline", 14.0
                elif "组织部部长" in post:
                    return "other", 14.0
                elif "委常委" in post:
                    return "other", 14.0
                else:
                    return "other", 12.0
        return "other", 12.0

    def color_for_org(oid):
        for o in ORGANIZATIONS:
            if o[0] == oid:
                tp = o[2]
                if "党委" in tp:
                    return "org_party", 8.0
                elif "政府" in tp or "公安" in tp:
                    return "org_gov", 8.0
                else:
                    return "org_other", 8.0
        return "org_other", 8.0

    # Build XML parts
    nodes_xml = []
    edges_xml = []

    # Person nodes
    for p in PERSONS:
        pid = p[0]
        label = p[1]
        g, sz = color_for_person(pid)
        r, gb, b = node_colors[g]
        title = f"{p[1]}\\n{p[9]}\\n{p[3]}·{p[4] if p[4] else '未知'}\\n籍贯: {p[5] if p[5] else '未知'}"
        nodes_xml.append(f"""\
    <node id="{pid}" label="{label}">
      <attvalues>
        <attvalue for="type" value="person"/>
        <attvalue for="role" value="{p[9]}"/>
      </attvalues>
      <viz:color r="{r}" g="{gb}" b="{b}" a="1.0"/>
      <viz:size value="{sz}"/>
      <viz:position x="0" y="0" z="0"/>
    </node>""")

    # Organization nodes
    for o in ORGANIZATIONS:
        oid = o[0]
        label = o[1]
        g, sz = color_for_org(oid)
        r, gb, b = node_colors[g]
        nodes_xml.append(f"""\
    <node id="{oid}" label="{label}">
      <attvalues>
        <attvalue for="type" value="org"/>
        <attvalue for="org_type" value="{o[2]}"/>
      </attvalues>
      <viz:color r="{r}" g="{gb}" b="{b}" a="1.0"/>
      <viz:size value="{sz}"/>
      <viz:shape value="square"/>
      <viz:position x="0" y="0" z="0"/>
    </node>""")

    # work_at edges (person -> org)
    edge_id = 0
    for pos in POSITIONS:
        pid, oid, title, start, end, rank, note = pos
        label = f"{title} ({start}-{end or '至今'})"
        edge_id += 1
        edges_xml.append(f"""\
    <edge id="e{edge_id}" source="{pid}" target="{oid}" type="directed" label="{title}">
      <attvalues>
        <attvalue for="type" value="worked_at"/>
        <attvalue for="start" value="{start or ''}"/>
        <attvalue for="end" value="{end or ''}"/>
        <attvalue for="rank" value="{rank or ''}"/>
      </attvalues>
      <viz:color r="80" g="80" b="80" a="0.5"/>
      <viz:thickness value="1.0"/>
    </edge>""")

    # relationship edges (person <-> person)
    for r in RELATIONSHIPS:
        a, b, typ, context, overlap_org, overlap_period = r
        edge_id += 1
        is_strong = typ == "强关系"
        cr, cg, cb = (184, 149, 62) if is_strong else (91, 139, 192)
        thickness = 2.5 if is_strong else 1.5
        edges_xml.append(f"""\
    <edge id="e{edge_id}" source="{a}" target="{b}" type="undirected" label="{context}">
      <attvalues>
        <attvalue for="type" value="relationship"/>
        <attvalue for="strength" value="{typ}"/>
        <attvalue for="context" value="{context}"/>
        <attvalue for="overlap_org" value="{overlap_org}"/>
        <attvalue for="overlap_period" value="{overlap_period}"/>
      </attvalues>
      <viz:color r="{cr}" g="{cg}" b="{cb}" a="0.8"/>
      <viz:thickness value="{thickness}"/>
    </edge>""")

    nodes_block = "\n".join(nodes_xml)
    edges_block = "\n".join(edges_xml)

    gexf = f"""<?xml version="1.0" encoding="UTF-8"?>
<gexf xmlns="http://gexf.net/1.3"
      xmlns:viz="http://gexf.net/1.3/viz"
      xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:schemaLocation="http://gexf.net/1.3 http://gexf.net/1.3/gexf.xsd"
      version="1.3">
  <meta>
    <creator>China-Gov-Network Investigation</creator>
    <description>九江市浔阳区领导班子工作关系网络 — 2026年7月</description>
    <date>2026-07-14</date>
  </meta>
  <graph mode="static" defaultedgetype="undirected">
    <attributes class="node">
      <attribute id="type" title="Node Type" type="string"/>
      <attribute id="role" title="Role" type="string"/>
      <attribute id="org_type" title="Org Type" type="string"/>
    </attributes>
    <attributes class="edge">
      <attribute id="type" title="Edge Type" type="string"/>
      <attribute id="start" title="Start Date" type="string"/>
      <attribute id="end" title="End Date" type="string"/>
      <attribute id="rank" title="Rank" type="string"/>
      <attribute id="strength" title="Strength" type="string"/>
      <attribute id="context" title="Context" type="string"/>
      <attribute id="overlap_org" title="Overlap Org" type="string"/>
      <attribute id="overlap_period" title="Overlap Period" type="string"/>
    </attributes>
    <nodes>
{nodes_block}
    </nodes>
    <edges>
{edges_block}
    </edges>
  </graph>
</gexf>"""

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write(gexf)
    print(f"✅ GEXF graph created: {GEXF_PATH}")


def print_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for table in ["persons", "organizations", "positions", "relationships"]:
        c.execute(f"SELECT COUNT(*) FROM {table}")
        cnt = c.fetchone()[0]
        print(f"  {table}: {cnt}")
    conn.close()


if __name__ == "__main__":
    print("Building 九江市浔阳区 network data...")
    create_db()
    generate_gexf()
    print("\n📊 Summary:")
    print_stats()
    print("Done.")
