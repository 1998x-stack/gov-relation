#!/usr/bin/env python3
"""昌宁县（保山市·云南省）领导班子工作关系网络 — 数据构建脚本

Data sources:
- yncn.gov.cn: 昌宁县人民政府门户网 (县政府领导页 xzf.htm, 新闻报道)
- Baidu Baike: 昌宁县词条
- 保山市人民政府门户网 (baoshan.gov.cn)

Confidence:
- 县委书记杨斌斌: confirmed (Baidu Baike + yncn.gov.cn news)
- 县长范正建: confirmed (gov leadership page) 
- 常务副县长刘志刚等: confirmed from gov leadership page
- 县委常委会其他成员(纪委、组织、宣传等): not listed on gov page
- Birth dates from government page
- Predecessor info/完整履历: partially available, gaps flagged

Targets: 县委书记 (一把手), 县长 (二把手)
Level: 县
Province: 云南省 保山市
"""

import sqlite3
import os
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(HERE, "昌宁县_network.db")
GEXF_PATH = os.path.join(HERE, "昌宁县_network.gexf")

# ── numeric IDs ──
PID = {k: i+1 for i, k in enumerate([
    "changning_secretary",   # 1 — 杨斌斌 (县委书记)
    "changning_mayor",       # 2 — 范正建 (县长)
    "changning_deputy_sec",  # 3 — 杨佳座 (副书记)
    "changning_exec_v",      # 4 — 刘志刚 (常务副县长)
    "changning_vice_xu",     # 5 — 徐喜瑛 (常委/副县长)
    "changning_vice_huang",  # 6 — 黄威 (挂职/常委)
    "changning_vice_duan",   # 7 — 段连卫 (副县长/公安)
    "changning_vice_zhao",   # 8 — 赵阳阳 (副县长)
    "changning_vice_liao",   # 9 — 廖明才 (副县长)
    "changning_vice_wang",   # 10 — 王国相 (副县长)
    "changning_vice_wangy",  # 11 — 王颖 (挂职副县长)
    "changning_vice_zhang",  # 12 — 张强中 (挂职副县长)
    "changning_office_d",    # 13 — 谢斌 (办公室主任)
    "changning_npc",         # 14 — 字庆明 (人大主任)
    "changning_cppcc",       # 15 — 王飞 (政协副主席)
])}

OID = {k: 1 + i for i, k in enumerate([
    "changning_party", "changning_gov", "changning_psb",
    "changning_gov_off", "changning_npc_org", "changning_cppcc_org",
    "baoshan_party", "baoshan_gov",
])}

PERSONS = [
    (PID["changning_secretary"], "杨斌斌", "男", "汉族", "", "", "", "中共党员", "", "县委书记", "中国共产党昌宁县委员会", "Baidu Baike昌宁县词条 + yncn.gov.cn新闻 (2026-08-03)"),
    (PID["changning_mayor"], "范正建", "男", "汉族", "1982.06", "", "", "中共党员", "", "县委副书记、县长", "昌宁县人民政府", "yncn.gov.cn/xzf.htm 县政府领导页"),
    (PID["changning_deputy_sec"], "杨佳座", "男", "汉族", "", "", "", "中共党员", "", "县委副书记", "中国共产党昌宁县委员会", "yncn.gov.cn新闻 (2026.05, 2026.06)"),
    (PID["changning_exec_v"], "刘志刚", "男", "汉族", "1979.09", "", "", "中共党员", "", "县委常委、常务副县长", "昌宁县人民政府", "yncn.gov.cn/xzf.htm"),
    (PID["changning_vice_xu"], "徐喜瑛", "男", "汉族", "1980.12", "", "", "中共党员", "", "县委常委、副县长", "昌宁县人民政府", "yncn.gov.cn/xzf.htm"),
    (PID["changning_vice_huang"], "黄威", "男", "汉族", "1979.09", "", "", "中共党员", "", "县委常委、副县长（挂职三年）", "昌宁县人民政府", "yncn.gov.cn/xzf.htm"),
    (PID["changning_vice_duan"], "段连卫", "男", "汉族", "1983.12", "", "", "中共党员", "", "副县长、公安局长", "昌宁县人民政府", "yncn.gov.cn/xzf.htm"),
    (PID["changning_vice_zhao"], "赵阳阳", "女", "汉族", "1983.10", "", "", "中共党员", "", "副县长", "昌宁县人民政府", "yncn.gov.cn/xzf.htm"),
    (PID["changning_vice_liao"], "廖明才", "男", "汉族", "1986.11", "", "", "中共党员", "", "副县长", "昌宁县人民政府", "yncn.gov.cn/xzf.htm"),
    (PID["changning_vice_wang"], "王国相", "男", "汉族", "1983.08", "", "", "中共党员", "", "副县长", "昌宁县人民政府", "yncn.gov.cn/xzf.htm"),
    (PID["changning_vice_wangy"], "王颖", "男", "汉族", "1966.05", "", "", "中共党员", "", "副县长（挂职二年）", "昌宁县人民政府", "yncn.gov.cn/xzf.htm"),
    (PID["changning_vice_zhang"], "张强中", "男", "汉族", "1975.11", "", "", "中共党员", "", "副县长（挂职二年）", "昌宁县人民政府", "yncn.gov.cn/xzf.htm"),
    (PID["changning_office_d"], "谢斌", "男", "彝族", "1981.03", "", "", "中共党员", "", "县政府办公室主任", "昌宁县人民政府办公室", "yncn.gov.cn/xzf.htm"),
    (PID["changning_npc"], "字庆明", "男", "汉族", "", "", "", "中共党员", "", "县人大常委会主任", "昌宁县人民代表大会常务委员会", "yncn.gov.cn新闻报道"),
    (PID["changning_cppcc"], "王飞", "男", "汉族", "", "", "", "中共党员", "", "县政协副主席", "中国人民政治协商会议昌宁县委员会", "yncn.gov.cn新闻报道"),
]

ORGANIZATIONS = [
    (OID["changning_party"], "中国共产党昌宁县委员会", "党委", "县级", "中国共产党保山市委员会", "云南省保山市昌宁县"),
    (OID["changning_gov"], "昌宁县人民政府", "政府", "县级", "保山市人民政府", "云南省保山市昌宁县"),
    (OID["changning_psb"], "昌宁县公安局", "公安", "乡科级", "保山市公安局", "云南省保山市昌宁县"),
    (OID["changning_gov_off"], "昌宁县人民政府办公室", "政府", "乡科级", "昌宁县人民政府", "云南省保山市昌宁县"),
    (OID["changning_npc_org"], "昌宁县人民代表大会常务委员会", "人大", "县级", "保山市人大常委会", "云南省保山市昌宁县"),
    (OID["changning_cppcc_org"], "中国人民政治协商会议昌宁县委员会", "政协", "县级", "保山市政协", "云南省保山市昌宁县"),
    (OID["baoshan_party"], "中国共产党保山市委员会", "党委", "地市级", "中国共产党云南省委员会", "云南省保山市"),
    (OID["baoshan_gov"], "保山市人民政府", "政府", "地市级", "云南省人民政府", "云南省保山市"),
]

POSITIONS = [
    (PID["changning_secretary"], OID["changning_party"], "县委书记", "待查", "至今", "县级正职", "主持县委全面工作"),
    (PID["changning_mayor"], OID["changning_gov"], "县长、县政府党组书记", "待查", "至今", "县级正职", "主持县政府全面工作"),
    (PID["changning_mayor"], OID["changning_party"], "县委副书记", "", "至今", "县级正职", "兼任"),
    (PID["changning_deputy_sec"], OID["changning_party"], "县委专职副书记", "待查", "至今", "县级副职", ""),
    (PID["changning_exec_v"], OID["changning_gov"], "常务副县长", "待查", "至今", "县级副职", "协管常务工作"),
    (PID["changning_exec_v"], OID["changning_party"], "县委常委", "待查", "至今", "县级副职", "兼任"),
    (PID["changning_vice_xu"], OID["changning_gov"], "副县长", "待查", "至今", "县级副职", "民族宗教、自然资源等"),
    (PID["changning_vice_xu"], OID["changning_party"], "县委常委", "待查", "至今", "县级副职", "兼任"),
    (PID["changning_vice_huang"], OID["changning_gov"], "副县长（挂职三年）", "待查", "至今", "县级副职", "沪滇协作"),
    (PID["changning_vice_huang"], OID["changning_party"], "县委常委（挂职）", "待查", "至今", "县级副职", ""),
    (PID["changning_vice_duan"], OID["changning_gov"], "副县长", "待查", "至今", "县级副职", "兼任公安局长"),
    (PID["changning_vice_duan"], OID["changning_psb"], "县公安局党委书记、局长", "待查", "至今", "乡科级正职", ""),
    (PID["changning_vice_zhao"], OID["changning_gov"], "副县长", "待查", "至今", "县级副职", "民政、人社、卫健"),
    (PID["changning_vice_liao"], OID["changning_gov"], "副县长", "待查", "至今", "县级副职", "工业经济、招商"),
    (PID["changning_vice_wang"], OID["changning_gov"], "副县长", "待查", "至今", "县级副职", "城建、交通、市场监管"),
    (PID["changning_vice_wangy"], OID["changning_gov"], "副县长（挂职二年）", "待查", "至今", "县级副职", "科技"),
    (PID["changning_vice_zhang"], OID["changning_gov"], "副县长（挂职二年）", "待查", "至今", "县级副职", "茶产业"),
    (PID["changning_office_d"], OID["changning_gov_off"], "县政府办公室主任", "待查", "至今", "乡科级正职", ""),
    (PID["changning_npc"], OID["changning_npc_org"], "县人大常委会主任", "待查", "至今", "县级正职", ""),
    (PID["changning_cppcc"], OID["changning_cppcc_org"], "县政协副主席", "待查", "至今", "县级正职", ""),
]

RELATIONSHIPS = [
    (PID["changning_secretary"], PID["changning_mayor"], "党政搭档", "县委书记与县长党政工作搭档", "昌宁县", "至今"),
    (PID["changning_secretary"], PID["changning_deputy_sec"], "领导与被领导", "县委书记与专职副书记", "中共昌宁县委", "至今"),
    (PID["changning_mayor"], PID["changning_exec_v"], "领导与被领导", "县长与常务副县长", "昌宁县政府", "至今"),
    (PID["changning_secretary"], PID["changning_exec_v"], "共事", "县委常委班子共事", "中共昌宁县委", "至今"),
    (PID["changning_mayor"], PID["changning_vice_xu"], "领导与被领导", "县长与副县长", "昌宁县政府", "至今"),
    (PID["changning_mayor"], PID["changning_vice_duan"], "领导与被领导", "县长与副县长(公安)", "昌宁县政府", "至今"),
    (PID["changning_mayor"], PID["changning_vice_zhao"], "领导与被领导", "县长与副县长", "昌宁县政府", "至今"),
    (PID["changning_mayor"], PID["changning_vice_liao"], "领导与被领导", "县长与副县长", "昌宁县政府", "至今"),
    (PID["changning_mayor"], PID["changning_vice_wang"], "领导与被领导", "县长与副县长", "昌宁县政府", "至今"),
    (PID["changning_exec_v"], PID["changning_vice_xu"], "协作", "常务与副县长协作", "昌宁县政府", "至今"),
    (PID["changning_exec_v"], PID["changning_vice_huang"], "协作", "常务与挂职副县长", "昌宁县政府", "至今"),
]


def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def create_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS persons (id INTEGER PRIMARY KEY,name TEXT,gender TEXT,ethnicity TEXT,birth TEXT,birthplace TEXT,education TEXT,party_join TEXT,work_start TEXT,current_post TEXT,current_org TEXT,source TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS organizations (id INTEGER PRIMARY KEY,name TEXT,type TEXT,level TEXT,parent TEXT,location TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS positions (person_id INTEGER,org_id INTEGER,title TEXT,start_date TEXT,end_date TEXT,rank TEXT,note TEXT,FOREIGN KEY(person_id) REFERENCES persons(id),FOREIGN KEY(org_id) REFERENCES organizations(id))")
    c.execute("CREATE TABLE IF NOT EXISTS relationships (person_a INTEGER,person_b INTEGER,type TEXT,context TEXT,overlap_org TEXT,overlap_period TEXT,FOREIGN KEY(person_a) REFERENCES persons(id),FOREIGN KEY(person_b) REFERENCES persons(id))")
    for p in PERSONS:
        c.execute("INSERT OR REPLACE INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", p)
    for o in ORGANIZATIONS:
        c.execute("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)", o)
    for pos in POSITIONS:
        c.execute("INSERT INTO positions VALUES (?,?,?,?,?,?,?)", pos)
    for r in RELATIONSHIPS:
        c.execute("INSERT INTO relationships VALUES (?,?,?,?,?,?)", r)
    conn.commit()
    conn.close()
    print(f"✅ Database: {DB_PATH}")


def person_color_sz(p):
    post = p[9]
    if "书记" in post and "副" not in post and "纪委" not in post:
        return "200,50,50", 20.0
    elif "县长" in post and "副" not in post:
        return "50,100,255", 20.0
    elif "副书记" in post:
        return "220,80,80", 16.0
    elif "常务副" in post:
        return "50,100,255", 16.0
    elif "副" in post:
        return "100,150,220", 14.0
    elif "主任" in post:
        return "60,180,60", 14.0
    else:
        return "180,180,180", 12.0


def org_color_sz(o):
    tp = o[2]
    if "党委" in tp:
        return "255,200,200", 8.0
    elif "政府" in tp:
        return "200,200,255", 8.0
    elif "人大" in tp:
        return "200,255,255", 8.0
    elif "政协" in tp:
        return "255,240,200", 8.0
    else:
        return "200,200,200", 8.0


def generate_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>China-Gov-Network Investigation Agent</creator>')
    lines.append('    <description>昌宁县领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="type" title="Node Type" type="string"/>')
    lines.append('      <attribute id="role" title="Role" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="type" title="Edge Type" type="string"/>')
    lines.append('      <attribute id="context" title="Context" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <nodes>')
    for p in PERSONS:
        pid, label = p[0], esc(p[1])
        cstr, sz = person_color_sz(p)
        r, g, b = cstr.split(",")
        lines.append(f'      <node id="p{pid}" label="{label}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p[9])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    for o in ORGANIZATIONS:
        oid, label = o[0], esc(o[1])
        cstr, sz = org_color_sz(o)
        r, g, b = cstr.split(",")
        lines.append(f'      <node id="o{oid}" label="{label}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')
    lines.append('    <edges>')
    eid = 0
    for pos in POSITIONS:
        eid += 1
        pid, oid, title = pos[0], pos[1], pos[2]
        lines.append(f'      <edge id="e{eid}" source="p{pid}" target="o{oid}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    for r in RELATIONSHIPS:
        eid += 1
        a, b, ctx = r[0], r[1], r[3]
        lines.append(f'      <edge id="e{eid}" source="p{a}" target="p{b}" label="{esc(ctx)}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(ctx)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF: {GEXF_PATH}")


def print_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for t in ["persons", "organizations", "positions", "relationships"]:
        cnt = c.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"  {t}: {cnt}")
    conn.close()


if __name__ == "__main__":
    print("=" * 60)
    print("  昌宁县领导班子工作关系网络")
    print("  云南省·保山市")
    print(f"  日期: {datetime.now().strftime('%Y-%m-%d')}")
    print("=" * 60)
    create_db()
    generate_gexf()
    print("\n📊 统计:")
    print_stats()
    print("Done.")