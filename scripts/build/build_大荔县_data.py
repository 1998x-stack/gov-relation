#!/usr/bin/env python3
"""
大荔县领导班子关系网络数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

大荔县是陕西省渭南市下辖的县，位于关中平原东部、黄洛渭三河汇流处。
数据来源：大荔县人民政府官网（www.dalisn.gov.cn）领导之窗、本地要闻（本地权威信源）
         及百度百科等公开资料。
采集日期：2026-08-07

当前领导（官方确认，截至 2026-08）:
  县委书记: 景军荣（男，汉族，1971-10，陕西省委党校研究生；2026-06-03 到任，
            此前任富平县县长 2021-2026）
  县委副书记、县长: 沙伟伟（男，回族，1976-03，研究生，中共党员；
            2026-05-21 当选大荔县县长）

近期主要领导更替（2026 年换届）:
  县委书记 由建新（~2021-2026.06）→ 景军荣（2026.06-今）
  县长 杜鑫（~2021-2026.04）→ 沙伟伟（代县长 → 2026-05-21 当选）
  更早县委书记 王青峰（至 ~2021-07，后任商洛市长）

说明：县领导换届调整中，个别任职起点为约值。本脚本以官方确认的现任职为骨架，
对履历未完全公开者用 confidence 标注（confirmed/plausible/unverified）。
"""
import sys
import os
import sqlite3
from pathlib import Path
from datetime import datetime
from xml.sax.saxutils import escape

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))

SLUG = "大荔县"
DATE = "2026-08-07"

# ===== 人物数据 =====
# (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source, confidence)
persons = [
    # --- 县委核心领导 ---
    (1, "景军荣", "男", "汉族", "1971年10月", "陕西省澄城县", "陕西省委党校研究生", "中共党员", "",
     "县委书记", "中共大荔县委员会",
     "https://www.dalisn.gov.cn/xwzx/zwyw/2062345498475319297.html", "confirmed"),
    (2, "沙伟伟", "男", "回族", "1976年3月", "", "研究生", "中共党员", "",
     "县委副书记、县长", "大荔县人民政府",
     "https://www.dalisn.gov.cn/zfxxgk/fdzdgknr/ldzc/1.html", "confirmed"),
    # --- 县人大 / 县政协 ---
    (3, "张红林", "男", "汉族", "", "", "", "中共党员", "",
     "县人大常委会主任", "大荔县人大常委会",
     "https://www.dalisn.gov.cn/", "confirmed"),
    (4, "谢文秀", "女", "汉族", "", "", "", "中共党员", "",
     "县政协主席", "大荔县政协",
     "https://www.dalisn.gov.cn/", "confirmed"),
    # --- 县政府副县长 ---
    (5, "卢高昌", "男", "汉族", "", "", "", "中共党员", "",
     "副县长", "大荔县人民政府",
     "https://www.dalisn.gov.cn/zfxxgk/fdzdgknr/ldzc/1.html", "confirmed"),
    (6, "王耀龙", "男", "汉族", "", "", "", "中共党员", "",
     "副县长", "大荔县人民政府",
     "https://www.dalisn.gov.cn/zfxxgk/fdzdgknr/ldzc/1.html", "confirmed"),
    (7, "张晓民", "男", "汉族", "1970年2月", "", "大学", "中共党员", "",
     "副县长", "大荔县人民政府",
     "https://www.dalisn.gov.cn/zfxxgk/fdzdgknr/ldzc/1.html", "confirmed"),
    (8, "高雪燕", "男", "汉族", "", "", "", "中共党员", "",
     "副县长", "大荔县人民政府",
     "https://www.dalisn.gov.cn/zfxxgk/fdzdgknr/ldzc/1.html", "confirmed"),
    (9, "雷渤", "男", "汉族", "1983年2月", "", "大学", "民建会员", "",
     "副县长", "大荔县人民政府",
     "https://www.dalisn.gov.cn/zfxxgk/fdzdgknr/ldzc/1.html", "confirmed"),
    (10, "朱志超", "男", "汉族", "", "", "", "中共党员", "",
     "副县长", "大荔县人民政府",
     "https://www.dalisn.gov.cn/zfxxgk/fdzdgknr/ldzc/1.html", "confirmed"),
    (11, "龙延", "男", "汉族", "1979年10月", "", "本科", "中共党员", "",
     "副县长、县公安局局长", "大荔县公安局",
     "https://www.dalisn.gov.cn/zfxxgk/fdzdgknr/ldzc/1.html", "confirmed"),
    (12, "陆峰", "男", "汉族", "1977年10月", "", "大学", "中共党员", "",
     "副县长、县财政局局长", "大荔县财政局",
     "https://www.dalisn.gov.cn/zfxxgk/fdzdgknr/ldzc/1.html", "confirmed"),
    (13, "哈伦别克·海诺拉", "男", "哈萨克族", "1988年7月", "", "大学", "中共党员", "",
     "副县长", "大荔县人民政府",
     "https://www.dalisn.gov.cn/zfxxgk/fdzdgknr/ldzc/1.html", "confirmed"),
    # --- 前任（更替链）---
    (14, "由建新", "男", "汉族", "", "", "", "中共党员", "",
     "原县委书记（去向待查）", "", "https://www.dalisn.gov.cn/", "confirmed"),
    (15, "杜鑫", "男", "汉族", "", "", "", "中共党员", "",
     "原县长（去向待查）", "", "https://www.dalisn.gov.cn/", "confirmed"),
    (16, "王青峰", "男", "汉族", "1968年7月", "", "", "中共党员", "",
     "前任县委书记（现任商洛市长）", "商洛市人民政府",
     "https://www.dalisn.gov.cn/", "plausible"),
]

# ===== 组织数据 =====
# (id, name, type, level, parent, location)
organizations = [
    (1, "中共大荔县委员会", "党委", "县级", "中共渭南市委员会", "陕西省渭南市大荔县"),
    (2, "大荔县人民政府", "政府", "县级", "渭南市人民政府", "陕西省渭南市大荔县"),
    (3, "大荔县人大常委会", "人大", "县级", "渭南市人大常委会", "陕西省渭南市大荔县"),
    (4, "大荔县政协", "政协", "县级", "政协渭南市委员会", "陕西省渭南市大荔县"),
    (5, "大荔县纪律检查委员会/县监委", "纪委", "县级", "中共渭南市纪律检查委员会", "陕西省渭南市大荔县"),
    (6, "大荔县公安局", "政府机构", "正科级", "大荔县人民政府", "陕西省渭南市大荔县"),
    (7, "大荔县财政局", "政府机构", "正科级", "大荔县人民政府", "陕西省渭南市大荔县"),
    (8, "中共富平县委员会", "党委", "县级", "中共渭南市委员会", "陕西省渭南市富平县"),
    (9, "富平县人民政府", "政府", "县级", "渭南市人民政府", "陕西省渭南市富平县"),
]

# ===== 任职数据 =====
# (id, person_id, org_id, title, start, end, rank, note)
positions = [
    # 景军荣 — 县委书记
    (1, 1, 1, "县委书记", "2026-06", "至今", "正县级", "2026-06-03全县领导干部大会宣布，主持县委全面工作；此前2022-2026任富平县长"),
    (2, 1, 9, "县长", "2022-03", "2026-06", "正县级", "富平县县长；2021-08~2022-03代县长"),
    (3, 1, 8, "县委副书记、代县长", "2021-08", "2022-03", "副县级", "富平县委副书记、代县长"),
    # 沙伟伟 — 县长
    (4, 2, 1, "县委副书记", "2026", "至今", "副县级", "历任县委副书记"),
    (5, 2, 2, "县长", "2026-05-21", "至今", "正县级", "2026-05-21当选县长；此前为代县长；分管县财政局、县审计局"),
    # 人大政协
    (6, 3, 3, "县人大常委会主任", "至今", "至今", "正县级", "主持县人大常委会工作"),
    (7, 4, 4, "县政协主席", "至今", "至今", "正县级", "主持县政协工作"),
    # 副县长
    (8, 5, 2, "副县长", "至今", "至今", "副县级", ""),
    (9, 6, 2, "副县长", "至今", "至今", "副县级", ""),
    (10, 7, 2, "副县长", "至今", "至今", "副县级", "曾任县财政局局长、县人大常委会副主任"),
    (11, 8, 2, "副县长", "至今", "至今", "副县级", ""),
    (12, 9, 2, "副县长", "至今", "至今", "副县级", "民建会员；分管民政、商务、招商引资、生态环境、供销、大数据"),
    (13, 10, 2, "副县长", "至今", "至今", "副县级", ""),
    (14, 11, 2, "副县长", "至今", "至今", "副县级", "分管公安、政法；兼县公安局局长"),
    (15, 11, 6, "县公安局局长", "至今", "至今", "副县级", ""),
    (16, 12, 2, "副县长", "至今", "至今", "副县级", "分管农业农村、乡村振兴、水务"),
    (17, 12, 7, "县财政局局长", "至今", "至今", "正科级", "县财政局党组书记、局长"),
    (18, 13, 2, "副县长", "至今", "至今", "副县级", "县政府党组成员；协管农业农村、工业经济"),
    # 前任
    (19, 14, 1, "县委书记", "约2021-08", "2026-06", "正县级", "2026-06由景军荣接任"),
    (20, 15, 2, "县长", "约2021", "2026-04", "正县级", "2026年由沙伟伟接任"),
    (21, 16, 1, "县委书记", "约201?", "约2021-07", "正县级", "王青峰大荔县委书记任期待考，后任商洛市长"),
]

# ===== 关系数据 =====
# (id, person_a, person_b, type, context, overlap_org, overlap_period, confidence)
relationships = [
    # 党政一把手搭档
    (1, 1, 2, "搭档", "县委书记与县长——2026年新一届党政一把手搭档", "中共大荔县委员会/大荔县人民政府", "2026-06至今", "confirmed"),
    # 书记与副书记
    (2, 1, 2, "上下级", "县委书记与县委副书记、县长沙伟伟", "中共大荔县委员会", "2026-06至今", "confirmed"),
    # 书记与人大政协
    (3, 1, 3, "上下级", "县委书记与县人大常委会主任", "大荔县人大常委会", "2026-06至今", "confirmed"),
    (4, 1, 4, "上下级", "县委书记与县政协主席", "大荔县政协", "2026-06至今", "confirmed"),
    # 县长与副县长
    (5, 2, 5, "上下级", "县长与副县长卢高昌", "大荔县人民政府", "至今", "confirmed"),
    (6, 2, 6, "上下级", "县长与副县长王耀龙", "大荔县人民政府", "至今", "confirmed"),
    (7, 2, 7, "上下级", "县长与副县长张晓民", "大荔县人民政府", "至今", "confirmed"),
    (8, 2, 8, "上下级", "县长与副县长高雪燕", "大荔县人民政府", "至今", "confirmed"),
    (9, 2, 9, "上下级", "县长与副县长雷渤", "大荔县人民政府", "至今", "confirmed"),
    (10, 2, 10, "上下级", "县长与副县长朱志超", "大荔县人民政府", "至今", "confirmed"),
    (11, 2, 11, "上下级", "县长与副县长（兼公安局长）龙延", "大荔县人民政府", "至今", "confirmed"),
    (12, 2, 12, "上下级", "县长与副县长（兼财政局长）陆峰", "大荔县人民政府", "至今", "confirmed"),
    (13, 2, 13, "上下级", "县长与副县长哈伦别克·海诺拉", "大荔县人民政府", "至今", "confirmed"),
    # 县委交接
    (14, 1, 14, "前任继任", "由建新→房军荣：景军荣接任大荔县委书记，前任为由建新", "中共大荔县委员会", "2026-06交接", "confirmed"),
    (15, 1, 16, "前任继任", "更早前任王青峰（时任商洛市长）", "中共大荔县委员会", "早期", "plausible"),
    # 县政府交接
    (16, 2, 15, "前任继任", "杜鑫→沙伟伟：沙伟伟接任大荔县长，前任为杜鑫", "大荔县人民政府", "2026交接", "confirmed"),
    # 景军荣与渭南干部交流
    (17, 1, 5, "跨县任职", "景军荣（富平县长）与副县长卢高昌等大荔县干部（富平—大荔跨县交流信号待验证）", "大荔县人民政府", "2026-06至今", "plausible"),
]

# ===== 生成函数 =====
def esc(s):
    return escape(str(s)) if s is not None else ""

def person_color(pid, post):
    if post == "县委书记":
        return "255,50,50"  # 红 = 书记
    if "县长" in post and "副" not in post[:2]:
        return "50,100,255"  # 蓝 = 县长
    if "副县长" in post:
        return "50,150,255"
    if "人大" in post:
        return "50,150,150"
    if "政协" in post:
        return "150,80,150"
    return "100,100,100"

def is_top_leader(post):
    return post == "县委书记" or ("县长" in post and "副" not in post[:2])

def build_sqlite(DB_PATH):
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, education TEXT,
            party_join TEXT, work_start TEXT,
            current_post TEXT, current_org TEXT, source TEXT,
            confidence TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY,
            person_id INTEGER, org_id INTEGER,
            title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY,
            person_a INTEGER, person_b INTEGER,
            type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT, confidence TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)
    c.executemany("INSERT OR REPLACE INTO persons(id,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source,confidence) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", persons)
    c.executemany("INSERT OR REPLACE INTO organizations VALUES (?,?,?,?,?,?)", organizations)
    c.executemany("INSERT OR REPLACE INTO positions VALUES (?,?,?,?,?,?,?,?)", positions)
    c.executemany("INSERT OR REPLACE INTO relationships VALUES (?,?,?,?,?,?,?,?)", relationships)
    conn.commit()
    conn.close()
    print(f"  SQLite 数据库已生成: {DB_PATH}")
    print(f"    - {len(persons)} 人物")
    print(f"    - {len(organizations)} 组织")
    print(f"    - {len(positions)} 任职记录")
    print(f"    - {len(relationships)} 关系记录")

def build_gexf(GEXF_PATH):
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{DATE}">')
    lines.append('    <creator>OpenCode Gov-Relation Agent</creator>')
    lines.append(f'    <description>大荔县领导班子关系网络 - {DATE}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <nodes>')
    for p in persons:
        pid, name, gender, ethnicity, birth, birthplace, edu, party, work, post, org, source, conf = p
        c = person_color(pid, post)
        sz = "20.0" if is_top_leader(post) else "12.0"
        lines.append(f'      <node id="p{pid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(post)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        oid, oname, otype, olevel, oparent, oloc = o
        color_map = {
            "党委": "255,200,200", "政府": "200,200,255",
            "纪委": "255,220,200", "党委部门": "255,210,210",
            "人大": "200,255,255", "政协": "255,240,200", "公安局": "200,220,255",
            "财政局": "200,230,255",
        }
        oc = color_map.get(otype, "200,200,200")
        lines.append(f'      <node id="o{oid}" label="{esc(oname)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(otype)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{oc.split(",")[0]}" g="{oc.split(",")[1]}" b="{oc.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('        <viz:shape value="square"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        pos_id, pid, oid, title, start, end, rank, note = pos
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pid}" target="o{oid}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for rel in relationships:
        rid, pa, pb, rtype, context, overlap_org, overlap_period, conf = rel
        eid += 1
        w = "2.0" if ("搭档" in rtype or "前任继任" in rtype) else "1.5"
        lines.append(f'      <edge id="e{eid}" source="p{pa}" target="p{pb}" label="{esc(context)}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(context)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF 图文件已生成: {GEXF_PATH}")
    print(f"    - {len(persons)} 个人物节点 + {len(organizations)} 个组织节点")
    print(f"    - {len(positions)} 条任职边 + {len(relationships)} 条关系边")


if __name__ == "__main__":
    staging = Path(__file__).parent.resolve()
    DB_PATH = staging / "大荔县_network.db"
    GEXF_PATH = staging / "大荔县_network.gexf"

    print(f"========== 构建 {SLUG} 数据 ==========")
    print(f"日期: {DATE}")

    build_sqlite(DB_PATH)
    build_gexf(GEXF_PATH)

    print(f"\n========== 构建完成 ==========")
    print(f"数据库: {DB_PATH} ({DB_PATH.stat().st_size} bytes)")
    print(f"GEXF:   {GEXF_PATH} ({GEXF_PATH.stat().st_size} bytes)")