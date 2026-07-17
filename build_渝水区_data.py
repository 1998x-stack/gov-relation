#!/usr/bin/env python3
"""
渝水区（新余市市辖区）领导班子工作关系网络 — 数据构建脚本
Builds SQLite DB + GEXF graph for Yushui District leadership network.

Research date: 2026-07-15
Task ID: jiangxi_渝水区

Sources:
  - jxxy.jxnews.com.cn (大江网新余频道) — 区重点项目调度会报道等
  - district.ce.cn (中国经济网)
  - thepaper.cn/thebjnews.com.cn (澎湃新闻/新京报)
  - zh.wikipedia.org (维基百科)
"""

import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data/database/渝水区_network.db")
GEXF_PATH = os.path.join(BASE_DIR, "data/graph/渝水区_network.gexf")

# ── PERSONS ──
# (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
PERSONS = [
    # ═══ Current Top Leaders ═══
    # 区委书记 — 彭勇 (据新京报2024年9月报道：彭勇履新渝水区委书记；公示期间曾有质疑，组织部门回应)
    ("ys_peng_yong", "彭勇", "男", "汉族", "1970-09", "江西新余",
     "中央党校大学/在职研究生", "中共党员", "1992-?",
     "渝水区委书记", "中共新余市渝水区委员会",
     "https://m.bjnews.com.cn/detail/1725515956129896.html; 新京报2024-09-05"),

    # 区长 — 郭峰 (据大江网2025年8月：区委副书记、区长郭峰出席重点项目调度会)
    ("ys_guo_feng", "郭峰", "男", "汉族", "1972-?", "江西",
     "大学学历", "中共党员", "?",
     "渝水区委副书记、区长", "渝水区人民政府",
     "https://jxxy.jxnews.com.cn/system/2025/08/20/020962105.shtml"),

    # 区委副书记（常务副区长） — 傅倩
    ("ys_fu_qian", "傅倩", "女", "汉族", "?", "江西",
     "?", "中共党员", "?",
     "渝水区委常委、常务副区长", "渝水区人民政府",
     "https://jxxy.jxnews.com.cn/system/2025/08/20/020962105.shtml"),

    # 区委常委、副区长 — 龚小华
    ("ys_gong_xiaohua", "龚小华", "男", "汉族", "?", "江西",
     "?", "中共党员", "?",
     "渝水区委常委、副区长", "渝水区人民政府",
     "https://jxxy.jxnews.com.cn/system/2025/08/20/020962105.shtml"),

    # ═══ Predecessors ═══
    # 前任区委书记 — 刘颖豪（渝水区前任区委书记，后另有任用）
    ("ys_liu_yinghao", "刘颖豪", "男", "汉族", "?", "江西",
     "?", "中共党员", "?",
     "（原渝水区委书记）", "",
     "zh.wikipedia.org/wiki/渝水区"),

    # 前任区长 — 简华锋（2024年前区长，后调离）
    ("ys_jian_huafeng", "简华锋", "男", "汉族", "?", "江西",
     "?", "中共党员", "?",
     "（原渝水区长/市商务局）", "新余市商务局",
     "zh.wikipedia.org/wiki/渝水区"),

    # ═══ Other Standing Committee Members (based on typical district structure) ═══
    # 区委副书记 (专职副书记)
    ("ys_deputy_secretary", "（专职副书记）", "男", "汉族", "?", "",
     "?", "中共党员", "?",
     "渝水区委副书记", "中共新余市渝水区委员会",
     "待查"),

    # 区纪委书记/监委主任
    ("ys_jiwei_head", "（纪委书记）", "男", "汉族", "?", "",
     "?", "中共党员", "?",
     "渝水区委常委、纪委书记、区监委主任", "中共新余市渝水区纪律检查委员会",
     "待查"),

    # 区委组织部部长
    ("ys_org_head", "（组织部部长）", "男", "汉族", "?", "",
     "?", "中共党员", "?",
     "渝水区委常委、组织部部长", "中共新余市渝水区委组织部",
     "待查"),

    # 区委宣传部部长
    ("ys_propaganda_head", "（宣传部部长）", "男", "汉族", "?", "",
     "?", "中共党员", "?",
     "渝水区委常委、宣传部部长", "中共新余市渝水区委宣传部",
     "待查"),

    # 区人武部部长
    ("ys_military_head", "（人武部部长）", "男", "汉族", "?", "",
     "?", "中共党员", "?",
     "渝水区委常委、人武部部长", "新余市渝水区人民武装部",
     "待查"),

    # ═══ 区人大常委会/政协 ═══
    # 区人大常委会主任
    ("ys_npc_head", "（区人大常委会主任）", "男", "汉族", "?", "",
     "?", "中共党员", "?",
     "渝水区人大常委会主任", "渝水区人民代表大会常务委员会",
     "待查"),

    # 区政协主席
    ("ys_cppcc_head", "（区政协主席）", "男", "汉族", "?", "",
     "?", "中共党员", "?",
     "渝水区政协主席", "中国人民政治协商会议新余市渝水区委员会",
     "待查"),

    # ═══ 副区长 ═══
    # 其他副区长（根据典型配置）
    ("ys_vice_mayor_a", "（副区长A）", "男", "汉族", "?", "",
     "?", "中共党员", "?",
     "渝水区副区长", "渝水区人民政府",
     "待查"),

    ("ys_vice_mayor_b", "（副区长B）", "男", "汉族", "?", "",
     "?", "中共党员", "?",
     "渝水区副区长", "渝水区人民政府",
     "待查"),

    ("ys_vice_mayor_c", "（副区长C）", "男", "汉族", "?", "",
     "?", "中共党员", "?",
     "渝水区副区长", "渝水区人民政府",
     "待查"),

    # ═══ Connections to City Level ═══
    # 方向军 — 新余市委书记（渝水区归属新余市管辖）
    ("xy_fang_xiangjun", "方向军", "男", "汉族", "1970-10", "浙江淳安",
     "大学学历/工商管理硕士", "中共党员", "1996-07",
     "新余市委书记", "中共新余市委",
     "build_xinyu_data.py（同项目）"),

    # 廖良生 — 新余市常务副市长
    ("xy_liao_liangsheng", "廖良生", "男", "汉族", "1975-09", "江西石城",
     "在职大学/工商管理硕士", "1997-08", "1993-07",
     "新余市委常委、常务副市长", "新余市人民政府",
     "build_xinyu_data.py（同项目）"),
]

# ── ORGANIZATIONS ──
ORGANIZATIONS = [
    ("org_yushui_district", "渝水区", "行政区域", "市辖区", "新余市", "江西省新余市"),
    ("org_yushui_cpc", "中共新余市渝水区委员会", "党委", "市辖区", "中共新余市委", "新余市渝水区"),
    ("org_yushui_gov", "渝水区人民政府", "政府", "市辖区", "渝水区", "新余市渝水区"),
    ("org_yushui_npc", "渝水区人民代表大会常务委员会", "人大", "市辖区", "渝水区", "新余市渝水区"),
    ("org_yushui_cppcc", "中国人民政治协商会议新余市渝水区委员会", "政协", "市辖区", "渝水区", "新余市渝水区"),
    ("org_yushui_jiwei", "中共新余市渝水区纪律检查委员会", "纪委", "市辖区", "中共新余市渝水区委员会", "新余市渝水区"),
    ("org_yushui_org", "中共新余市渝水区委组织部", "党委部门", "市辖区部门", "中共新余市渝水区委员会", "新余市渝水区"),
    ("org_yushui_propaganda", "中共新余市渝水区委宣传部", "党委部门", "市辖区部门", "中共新余市渝水区委员会", "新余市渝水区"),
    ("org_yushui_military", "新余市渝水区人民武装部", "军事", "市辖区", "新余军分区", "新余市渝水区"),
    ("org_xy_cpc", "中共新余市委", "党委", "地级市", "中共江西省委", "新余市"),
    ("org_xy_gov", "新余市人民政府", "政府", "地级市", "新余市", "新余市"),
    ("org_xy_bureau_commerce", "新余市商务局", "政府", "地级市部门", "新余市人民政府", "新余市"),
    ("org_unknown", "（待查）", "其他", "未知", "", "未知"),
]

# ── POSITIONS ──
POSITIONS = [
    # 彭勇 — 区委书记
    ("ys_peng_yong", "org_yushui_cpc", "渝水区委书记", "2024-09", "", "正处级", "现任；2024年9月公示任职"),
    ("ys_peng_yong", "org_unknown", "（此前职务）", "", "2024-09", "?", "待查"),

    # 郭峰 — 区长
    ("ys_guo_feng", "org_yushui_gov", "渝水区委副书记、区长", "2024/2025?", "", "正处级", "现任"),
    ("ys_guo_feng", "org_unknown", "（此前职务）", "", "", "?", "待查"),

    # 傅倩 — 常务副区长
    ("ys_fu_qian", "org_yushui_gov", "渝水区委常委、常务副区长", "~2024", "", "副处级", "现任"),

    # 龚小华 — 区委常委、副区长
    ("ys_gong_xiaohua", "org_yushui_gov", "渝水区委常委、副区长", "~2024", "", "副处级", "现任"),

    # 前任区委书记
    ("ys_liu_yinghao", "org_yushui_cpc", "渝水区委书记", "~2022", "2024-08", "正处级", "离任"),
    ("ys_liu_yinghao", "org_unknown", "（调任）", "2024-08", "", "?", "另有任用"),

    # 前任区长
    ("ys_jian_huafeng", "org_yushui_gov", "渝水区长", "~2021", "2024", "正处级", "离任"),
    ("ys_jian_huafeng", "org_xy_bureau_commerce", "新余市商务局局长", "2024", "", "正处级", "现任"),

    # 专职副书记
    ("ys_deputy_secretary", "org_yushui_cpc", "渝水区委副书记", "", "", "副处级", "待确认"),

    # 纪委书记
    ("ys_jiwei_head", "org_yushui_jiwei", "渝水区委常委、纪委书记、区监委主任", "", "", "副处级", "待确认"),

    # 组织部部长
    ("ys_org_head", "org_yushui_org", "渝水区委常委、组织部部长", "", "", "副处级", "待确认"),

    # 宣传部部长
    ("ys_propaganda_head", "org_yushui_propaganda", "渝水区委常委、宣传部部长", "", "", "副处级", "待确认"),

    # 人武部部长
    ("ys_military_head", "org_yushui_military", "渝水区委常委、人武部部长", "", "", "副处级", "待确认"),

    # 人大主任
    ("ys_npc_head", "org_yushui_npc", "渝水区人大常委会主任", "", "", "正处级", "待确认"),

    # 政协主席
    ("ys_cppcc_head", "org_yushui_cppcc", "渝水区政协主席", "", "", "正处级", "待确认"),

    # 副区长们
    ("ys_vice_mayor_a", "org_yushui_gov", "渝水区副区长", "", "", "副处级", "待确认"),
    ("ys_vice_mayor_b", "org_yushui_gov", "渝水区副区长", "", "", "副处级", "待确认"),
    ("ys_vice_mayor_c", "org_yushui_gov", "渝水区副区长", "", "", "副处级", "待确认"),
]

# ── RELATIONSHIPS ──
RELATIONSHIPS = [
    # 彭勇 ← 市委领导
    ("ys_peng_yong", "xy_fang_xiangjun", "隶属关系",
     "彭勇任渝水区委书记，受新余市委领导；方为市委书记",
     "新余市", "2024-"),

    # 彭勇 → 刘颖豪（职位交接）
    ("ys_peng_yong", "ys_liu_yinghao", "职位接替",
     "彭勇接替刘颖豪任渝水区委书记",
     "中共新余市渝水区委员会", "2024"),

    # 郭峰 ↔ 彭勇（党政正副手）
    ("ys_guo_feng", "ys_peng_yong", "工作关系",
     "郭峰任区委副书记、区长，在彭勇领导下工作",
     "渝水区", "2024-"),

    # 郭峰 → 简华锋（职位接替）
    ("ys_guo_feng", "ys_jian_huafeng", "职位接替",
     "郭峰接替简华锋任渝水区长",
     "渝水区人民政府", "2024"),

    # 傅倩 ↔ 郭峰（正副手）
    ("ys_fu_qian", "ys_guo_feng", "工作关系",
     "傅倩任常务副区长，协助郭峰主持区政府日常工作",
     "渝水区人民政府", "2024-"),

    # 龚小华 ↔ 郭峰
    ("ys_gong_xiaohua", "ys_guo_feng", "工作关系",
     "龚小华任区委常委、副区长，协助区长工作",
     "渝水区人民政府", "2024-"),

    # 傅倩 ↔ 龚小华
    ("ys_fu_qian", "ys_gong_xiaohua", "同事关系",
     "同为渝水区委常委、区政府副职领导",
     "渝水区委/区政府", "2024-"),

    # 彭勇 ← 市领导分管
    ("ys_peng_yong", "xy_liao_liangsheng", "间接关系",
     "彭勇任渝水区委书记，廖良生为新余市委常委/常务副市长，合作关系",
     "新余市", "2025-"),

    # 渝水区 ← 新余市
    ("ys_guo_feng", "xy_fang_xiangjun", "隶属关系",
     "郭峰任渝水区长，受新余市委市政府领导",
     "新余市", "2024-"),
]

# ── Helper for esc in GEXF ──
esc = lambda s: str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

# ── Build SQLite ──
def build_sqlite():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id TEXT PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id TEXT PRIMARY KEY, name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT, org_id TEXT, title TEXT, start TEXT,
            end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT, person_b TEXT, type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
        CREATE INDEX IF NOT EXISTS idx_ys_person_name ON persons(name);
        CREATE INDEX IF NOT EXISTS idx_ys_org_name ON organizations(name);
        CREATE INDEX IF NOT EXISTS idx_ys_pos_person ON positions(person_id);
    """)
    for p in PERSONS:
        c.execute("""INSERT OR REPLACE INTO persons(id,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source)
            VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""", p)
    for o in ORGANIZATIONS:
        c.execute("INSERT OR REPLACE INTO organizations(id,name,type,level,parent,location) VALUES(?,?,?,?,?,?)", o)
    for pos in POSITIONS:
        c.execute("INSERT OR REPLACE INTO positions(person_id,org_id,title,start,end,rank,note) VALUES(?,?,?,?,?,?,?)", pos)
    for r in RELATIONSHIPS:
        c.execute("INSERT OR REPLACE INTO relationships(person_a,person_b,type,context,overlap_org,overlap_period) VALUES(?,?,?,?,?,?)", r)
    conn.commit()
    for tbl in ["persons","organizations","positions","relationships"]:
        cnt = c.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()[0]
        print(f"  {tbl}: {cnt}")
    conn.close()

# ── Build GEXF (string concat, NOT ElementTree) ──
def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    def color(r,g,b):
        return f'<viz:color r="{r}" g="{g}" b="{b}" a="1.0"/>'

    def node_size(p):
        title = p[8]
        if p[9] == "" and not title.startswith("（"):
            return "8.0"
        if "书记" in title and "副" not in title and "副书记" not in title:
            return "20.0"
        if "区长" in title and "副" not in title and "副书记" not in title:
            return "16.0"
        if "人大" in title or "政协" in title:
            return "14.0"
        if "常务" in title:
            return "14.0"
        if "常委" in title:
            return "12.0"
        return "10.0"

    def person_color(p):
        title = p[8]
        if "书记" in title and "副" not in title and "副书记" not in title:
            return color(220,50,50)
        if "区长" in title and "副" not in title:
            return color(50,100,220)
        if "常务" in title:
            return color(50,150,255)
        if "副书记" in title:
            return color(200,100,50)
        if "人大" in title or "政协" in title:
            return color(60,180,75)
        if "常委" in title:
            return color(100,120,255)
        if "副" in title:
            return color(160,130,80)
        return color(100,100,100)

    def org_color(o):
        otype = o[2]
        if "党委" in otype: return color(240,120,120)
        if "政府" in otype or "行政" in otype: return color(120,180,240)
        if "人大" in otype or "政协" in otype: return color(120,220,140)
        if "纪委" in otype: return color(255,165,0)
        if "军事" in otype: return color(180,180,100)
        return color(180,180,180)

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append('<graph mode="static" defaultedgetype="undirected">')
    lines.append("""<attributes class="node">
        <attribute id="type" title="type" type="string"/>
        <attribute id="birth" title="birth" type="string"/>
        <attribute id="birthplace" title="birthplace" type="string"/>
        <attribute id="current_post" title="current_post" type="string"/>
        <attribute id="entity_type" title="entity_type" type="string"/>
        <attribute id="level" title="level" type="string"/>
    </attributes>
    <attributes class="edge">
        <attribute id="type" title="type" type="string"/>
        <attribute id="start" title="start" type="string"/>
        <attribute id="end" title="end" type="string"/>
        <attribute id="context" title="context" type="string"/>
    </attributes>""")
    lines.append("<nodes>")
    for p in PERSONS:
        sz = node_size(p)
        c = person_color(p)
        cur_org = esc(p[9]) if p[9] else "N/A"
        lines.append(f"""<node id="{esc(p[0])}" label="{esc(p[1])}">
        {c}
        <viz:size value="{sz}"/>
        <attvalues>
            <attvalue for="type" value="person"/>
            <attvalue for="birth" value="{esc(p[4])}"/>
            <attvalue for="birthplace" value="{esc(p[5])}"/>
            <attvalue for="current_post" value="{esc(p[8])}"/>
            <attvalue for="entity_type" value="person"/>
            <attvalue for="level" value=""/>
        </attvalues>
    </node>""")
    for o in ORGANIZATIONS:
        c = org_color(o)
        lines.append(f"""<node id="{esc(o[0])}" label="{esc(o[1])}">
        {c}
        <viz:size value="8.0"/>
        <attvalues>
            <attvalue for="type" value="organization"/>
            <attvalue for="birth" value=""/>
            <attvalue for="birthplace" value=""/>
            <attvalue for="current_post" value=""/>
            <attvalue for="entity_type" value="org"/>
            <attvalue for="level" value="{esc(o[3])}"/>
        </attvalues>
    </node>""")
    lines.append("</nodes>")
    lines.append("<edges>")
    edge_id = 0
    for pos in POSITIONS:
        edge_id += 1
        lines.append(f"""<edge id="{edge_id}" source="{esc(pos[0])}" target="{esc(pos[1])}" weight="1.0">
        <attvalues>
            <attvalue for="type" value="worked_at"/>
            <attvalue for="start" value="{esc(pos[3] or '')}"/>
            <attvalue for="end" value="{esc(pos[4] or '')}"/>
            <attvalue for="context" value="{esc(pos[2])}. {esc(pos[6] or '')}"/>
        </attvalues>
    </edge>""")
    for r in RELATIONSHIPS:
        edge_id += 1
        w = "2.0" if r[2] in ("工作关系","职位接替","隶属关系") else "1.0"
        lines.append(f"""<edge id="{edge_id}" source="{esc(r[0])}" target="{esc(r[1])}" weight="{w}">
        <attvalues>
            <attvalue for="type" value="{esc(r[2])}"/>
            <attvalue for="start" value=""/>
            <attvalue for="end" value=""/>
            <attvalue for="context" value="{esc(r[3])} ({esc(r[5] or '')})"/>
        </attvalues>
    </edge>""")
    lines.append("</edges>")
    lines.append("</graph></gexf>")
    with open(GEXF_PATH,"w",encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF: {edge_id} edges written")

if __name__ == "__main__":
    print("=== 渝水区 Leadership Network ===")
    print("[SQLite]")
    build_sqlite()
    print("[GEXF]")
    build_gexf()
    print("Done.")
