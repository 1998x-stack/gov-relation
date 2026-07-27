#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 南雄市 leadership."""
import sqlite3, os, json

DB = "data/database/nanxiong_network.db"
GFX = "data/graph/nanxiong_network.gexf"

os.makedirs(os.path.dirname(DB), exist_ok=True)
os.makedirs(os.path.dirname(GFX), exist_ok=True)

# ──────────────────────────────────────────────
# DATA — sourced from gdnx.gov.cn (南雄市政府官方)
# ──────────────────────────────────────────────

persons = [
    # id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source
    ("nanxiong_ke_jianzhong",  "柯建忠", "男", "汉族", "1977-02", None, "中央党校研究生", None, None, "市委书记", "中共南雄市委", "https://www.gdnx.gov.cn/zwgk/ldzc/zgnxsw/content/post_236246.html"),
    ("nanxiong_chen_bing",    "陈冰",   "男", "汉族", "1981-02", None, "研究生/理学硕士", None, None, "市长/市委副书记", "南雄市人民政府", "https://www.gdnx.gov.cn/zwgk/ldzc/zgnxsw/content/post_2685777.html"),
    ("nanxiong_lin_jun",      "林军",   "男", "汉族", "1977-08", None, "中央党校大学", None, None, "市委副书记", "中共南雄市委", "https://www.gdnx.gov.cn/zwgk/ldzc/zgnxsw/content/post_236243.html"),
    ("nanxiong_lei_wei",      "雷伟",   "男", "汉族", "1984-10", None, "大学本科", None, None, "市委副书记（挂职）", "中共南雄市委", "https://www.gdnx.gov.cn/zwgk/ldzc/zgnxsw/content/post_2686909.html"),
    ("nanxiong_wen_chunhua",  "温春花", "女", "汉族", "1978-04", None, "中央党校大学", None, None, "市委常委/宣传部部长", "中共南雄市委", "https://www.gdnx.gov.cn/zwgk/ldzc/zgnxsw/content/post_236248.html"),
    ("nanxiong_ye_zhiming",   "叶志明", "男", "汉族", "1973-11", None, "大学/工学学士", None, None, "市纪委书记/监委主任", "中共南雄市纪委", "https://www.gdnx.gov.cn/zwgk/ldzc/zgnxsw/content/post_2721719.html"),
    ("nanxiong_yang_yaoxuan", "杨耀轩", "男", "汉族", "1979-10", None, "大学/工程硕士", None, None, "市委常委/统战部部长", "中共南雄市委", "https://www.gdnx.gov.cn/zwgk/ldzc/zgnxsw/content/post_2049516.html"),
    ("nanxiong_shi_wei",      "石为",   "男", "汉族", "1982-04", None, "大学/文学学士", None, None, "市委常委/办公室主任", "中共南雄市委", "https://www.gdnx.gov.cn/zwgk/ldzc/zgnxsw/content/post_2058516.html"),
    ("nanxiong_wu_hongwen",   "吴宏文", "男", "汉族", "1981-08", None, "大学/法学学士", None, None, "市委组织部部长/党校校长", "中共南雄市委组织部", "https://www.gdnx.gov.cn/zwgk/ldzc/zgnxsw/content/post_2777189.html"),
    ("nanxiong_hu_chunling",  "胡春陵", "男", "汉族", "1983-11", None, "哈师大/理学学士", None, None, "市委常委/政法委书记", "中共南雄市委政法委", "https://www.gdnx.gov.cn/zwgk/ldzc/zgnxsw/content/post_2815434.html"),
    ("nanxiong_lai_yongxing", "赖永兴", "男", "汉族", "1974-12", None, "省委党校大专", None, None, "副市长", "南雄市人民政府", "https://www.gdnx.gov.cn/zwgk/ldzc/nxsrmzf/content/post_2157851.html"),
    ("nanxiong_zhu_hui",      "朱慧",   "女", "汉族", "1985-05", None, "大学/农业推广硕士", None, None, "副市长", "南雄市人民政府", "https://www.gdnx.gov.cn/zwgk/ldzc/nxsrmzf/content/post_1993446.html"),
    ("nanxiong_xu_hong",      "许洪",   "男", "汉族", "1978-01", None, "中央党校大学", None, None, "副市长/公安局长", "南雄市人民政府", "https://www.gdnx.gov.cn/zwgk/ldzc/nxsrmzf/content/post_2527546.html"),
    ("nanxiong_liu_chunwei",  "刘春伟", "男", "汉族", "1982-11", None, "大学", None, None, "副市长", "南雄市人民政府", "https://www.gdnx.gov.cn/zwgk/ldzc/nxsrmzf/content/post_2754526.html"),
    ("nanxiong_zhai_puyao",   "翟普尧", "男", "汉族", "1980-10", None, "中央党校经济学研究生", None, None, "市政府党组成员/帮扶队长", "南雄市人民政府", "https://www.gdnx.gov.cn/zwgk/ldzc/nxsrmzf/content/post_2643658.html"),
    ("nanxiong_zeng_wenhui",  "曾文辉", "男", "汉族", "1968-10", None, "省委党校大学", None, None, "市人大常委会主任", "南雄市人大常委会", "https://www.gdnx.gov.cn/zwgk/ldzc/nxrdcwh/content/post_236254.html"),
    ("nanxiong_liu_guanghao", "刘光浩", "男", "汉族", "1969-05", None, "省委党校大学", None, None, "市政协主席", "南雄市政协", "https://www.gdnx.gov.cn/zwgk/ldzc/nxszx/content/post_2083736.html"),
]

orgs = [
    ("org_nanxiong_psc",  "中共南雄市委", "党委", "县级", "org_shaoguan_city", "南雄"),
    ("org_nanxiong_gov",  "南雄市人民政府", "政府", "县级", "org_shaoguan_gov", "南雄"),
    ("org_nanxiong_cdc",  "南雄市人大常委会", "人大", "县级", "org_shaoguan_city", "南雄"),
    ("org_nanxiong_cppcc","南雄市政协", "政协", "县级", "org_shaoguan_city", "南雄"),
    ("org_nanxiong_disc", "南雄市纪委监委", "纪委", "县级", "org_nanxiong_psc", "南雄"),
    ("org_nanxiong_org",  "南雄市委组织部", "党委部门", "县级", "org_nanxiong_psc", "南雄"),
    ("org_nanxiong_pub",  "南雄市委宣传部", "党委部门", "县级", "org_nanxiong_psc", "南雄"),
    ("org_nanxiong_ufw",  "南雄市委统战部", "党委部门", "县级", "org_nanxiong_psc", "南雄"),
    ("org_nanxiong_off",  "南雄市委办公室", "党委部门", "县级", "org_nanxiong_psc", "南雄"),
    ("org_nanxiong_pol",  "南雄市委政法委", "党委部门", "县级", "org_nanxiong_psc", "南雄"),
    ("org_nanxiong_psb",  "南雄市公安局", "政府机构", "县级", "org_nanxiong_gov", "南雄"),
]

positions = [
    # (person_id, org_id, title, start, end, rank, note)
    ("nanxiong_ke_jianzhong", "org_nanxiong_psc", "市委书记", "2021-??", None, "正处级", None),
    ("nanxiong_chen_bing", "org_nanxiong_psc", "市委副书记", "2024-??", None, "正处级", "同时任市政府党组书记、市长"),
    ("nanxiong_chen_bing", "org_nanxiong_gov", "市长", "2024-??", None, "正处级", "市政府党组书记"),
    ("nanxiong_lin_jun", "org_nanxiong_psc", "市委副书记", None, None, "副处级", None),
    ("nanxiong_lei_wei", "org_nanxiong_psc", "市委副书记（挂职）", None, None, "副处级", "挂职"),
    ("nanxiong_wen_chunhua", "org_nanxiong_pub", "宣传部部长", None, None, "副处级", "市委常委"),
    ("nanxiong_ye_zhiming", "org_nanxiong_disc", "市纪委书记/监委主任", None, None, "副处级", "市委常委"),
    ("nanxiong_yang_yaoxuan", "org_nanxiong_ufw", "统战部部长", None, None, "副处级", "市委常委"),
    ("nanxiong_shi_wei", "org_nanxiong_off", "市委办公室主任", None, None, "副处级", "市委常委"),
    ("nanxiong_wu_hongwen", "org_nanxiong_org", "组织部部长", None, None, "副处级", "市委常委/党校校长"),
    ("nanxiong_hu_chunling", "org_nanxiong_pol", "政法委书记", None, None, "副处级", "市委常委"),
    ("nanxiong_lai_yongxing", "org_nanxiong_gov", "副市长", None, None, "副处级", "市政府党组成员"),
    ("nanxiong_zhu_hui", "org_nanxiong_gov", "副市长", None, None, "副处级", "市政府党组成员"),
    ("nanxiong_xu_hong", "org_nanxiong_gov", "副市长", None, None, "副处级", "市公安局长/市政府党组成员"),
    ("nanxiong_liu_chunwei", "org_nanxiong_gov", "副市长", None, None, "副处级", "市政府党组成员"),
    ("nanxiong_zhai_puyao", "org_nanxiong_gov", "市政府党组成员", None, None, "副处级", "南城-南雄对口帮扶工作队队长"),
    ("nanxiong_zeng_wenhui", "org_nanxiong_cdc", "市人大常委会主任", None, None, "正处级", "党组书记"),
    ("nanxiong_liu_guanghao", "org_nanxiong_cppcc", "市政协主席", None, None, "正处级", "党组书记"),
]

relationships = [
    # person_a, person_b, type, context, overlap_org, overlap_period
    ("nanxiong_ke_jianzhong", "nanxiong_chen_bing", "正副搭档", "市委书记与市长搭档", "中共南雄市委/南雄市政府", "2024-至今"),
    ("nanxiong_ke_jianzhong", "nanxiong_lin_jun", "正副搭档", "市委书记与专职副书记", "中共南雄市委", "至今"),
    ("nanxiong_lin_jun", "nanxiong_lei_wei", "同级", "两名副书记", "中共南雄市委", "至今"),
    ("nanxiong_chen_bing", "nanxiong_lai_yongxing", "上下级", "市长与副市长", "南雄市人民政府", "至今"),
    ("nanxiong_chen_bing", "nanxiong_zhu_hui", "上下级", "市长与副市长", "南雄市人民政府", "至今"),
    ("nanxiong_chen_bing", "nanxiong_xu_hong", "上下级", "市长与副市长", "南雄市人民政府", "至今"),
    ("nanxiong_chen_bing", "nanxiong_liu_chunwei", "上下级", "市长与副市长", "南雄市人民政府", "至今"),
]

# ──────────────────────────────────────────────
# SQLite
# ──────────────────────────────────────────────
if os.path.exists(DB):
    os.remove(DB)
conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.executescript("""
CREATE TABLE persons (
    id TEXT PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
    birthplace TEXT, education TEXT, party_join TEXT, work_start TEXT,
    current_post TEXT, current_org TEXT, source TEXT
);
CREATE TABLE organizations (
    id TEXT PRIMARY KEY, name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
);
CREATE TABLE positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT, person_id TEXT, org_id TEXT, title TEXT,
    start TEXT, end TEXT, rank TEXT, note TEXT,
    FOREIGN KEY(person_id) REFERENCES persons(id),
    FOREIGN KEY(org_id) REFERENCES organizations(id)
);
CREATE TABLE relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT, person_a TEXT, person_b TEXT,
    type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT,
    FOREIGN KEY(person_a) REFERENCES persons(id),
    FOREIGN KEY(person_b) REFERENCES persons(id)
);
""")

for p in persons:
    cur.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)", p)
for o in orgs:
    cur.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)", o)
for po in positions:
    cur.execute("INSERT INTO positions (person_id,org_id,title,start,end,rank,note) VALUES (?,?,?,?,?,?,?)", po)
for r in relationships:
    cur.execute("INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)", r)

conn.commit()
conn.close()
print(f"[DB] {DB} created — {len(persons)} persons, {len(orgs)} orgs, {len(positions)} positions, {len(relationships)} relationships")

# ──────────────────────────────────────────────
# GEXF
# ──────────────────────────────────────────────
import xml.sax.saxutils as saxutils

def esc(s):
    return saxutils.escape(str(s or ""))

lines = ['<?xml version="1.0" encoding="UTF-8"?>']
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# attributes
lines.append('    <attributes class="node">')
lines.append('      <attribute id="type" title="type" type="string"/>')
lines.append('      <attribute id="birth" title="birth" type="string"/>')
lines.append('      <attribute id="education" title="education" type="string"/>')
lines.append('      <attribute id="role" title="role" type="string"/>')
lines.append('      <attribute id="source" title="source" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="type" title="type" type="string"/>')
lines.append('      <attribute id="start" title="start" type="string"/>')
lines.append('      <attribute id="end" title="end" type="string"/>')
lines.append('      <attribute id="context" title="context" type="string"/>')
lines.append('    </attributes>')

# nodes
lines.append('    <nodes>')
for p in persons:
    pid, name, gender, _, birth, _, edu, _, _, post, org, src = p
    role_color = {"市委书记": "#E03C31", "市长": "#2563EB", "市委副书记": "#3B82F6",
                  "市纪委书记": "#F59E0B", "市委常委": "#6B7280", "副市长": "#3B82F6",
                  "市人大主任": "#10B981", "市政协主席": "#8B5CF6"}.get(
        post.split("/")[0] if "/" in post else post, "#9CA3AF")
    size = "20.0" if post.startswith("市委") and "书记" in post else "15.0" if "市长" in post else "12.0"
    lines.append(f'      <node id="{esc(pid)}" label="{esc(name)}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="person"/>')
    lines.append(f'          <attvalue for="birth" value="{esc(birth or "")}"/>')
    lines.append(f'          <attvalue for="education" value="{esc(edu or "")}"/>')
    lines.append(f'          <attvalue for="role" value="{esc(post)}"/>')
    lines.append(f'          <attvalue for="source" value="{esc(src or "")}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{int(role_color[1:3],16)}" g="{int(role_color[3:5],16)}" b="{int(role_color[5:7],16)}" a="1.0"/>')
    lines.append(f'        <viz:size value="{size}"/>')
    lines.append(f'      </node>')

# org nodes
for o in orgs:
    oid, name, otype, _, _, loc = o
    lines.append(f'      <node id="{esc(oid)}" label="{esc(name)}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="org"/>')
    lines.append(f'          <attvalue for="birth" value=""/>')
    lines.append(f'          <attvalue for="education" value=""/>')
    lines.append(f'          <attvalue for="role" value="{esc(otype)}"/>')
    lines.append(f'          <attvalue for="source" value=""/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="100" g="100" b="100" a="1.0"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append(f'      </node>')

lines.append('    </nodes>')

# edges
lines.append('    <edges>')
eid = 0
for po in positions:
    pid, oid, title, start, end, _, note = po
    eid += 1
    lines.append(f'      <edge id="{eid}" source="{esc(pid)}" target="{esc(oid)}" label="worked_at">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="worked_at"/>')
    lines.append(f'          <attvalue for="start" value="{esc(start or "")}"/>')
    lines.append(f'          <attvalue for="end" value="{esc(end or "")}"/>')
    lines.append(f'          <attvalue for="context" value="{esc(title)}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="150" g="150" b="150" a="1.0"/>')
    lines.append(f'        <viz:thickness value="1.0"/>')
    lines.append(f'      </edge>')

for r in relationships:
    pa, pb, rtype, ctx, oo, op = r
    eid += 1
    gold = rtype in ("正副搭档",)  # strong
    lines.append(f'      <edge id="{eid}" source="{esc(pa)}" target="{esc(pb)}" label="{esc(rtype)}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="relationship"/>')
    lines.append(f'          <attvalue for="start" value="{esc(op or "")}"/>')
    lines.append(f'          <attvalue for="end" value=""/>')
    lines.append(f'          <attvalue for="context" value="{esc(ctx)}"/>')
    lines.append(f'        </attvalues>')
    if gold:
        lines.append(f'        <viz:color r="201" g="169" b="78" a="1.0"/>')
        lines.append(f'        <viz:thickness value="2.0"/>')
    else:
        lines.append(f'        <viz:color r="100" g="150" b="255" a="1.0"/>')
        lines.append(f'        <viz:thickness value="1.5"/>')
    lines.append(f'      </edge>')

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GFX, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
print(f"[GEXF] {GFX} created — {len(persons)+len(orgs)} nodes, {eid} edges")
print("[DONE] All outputs generated.")
