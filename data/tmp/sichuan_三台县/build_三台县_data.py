#!/usr/bin/env python3
"""
三台县领导班子关系网络数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

三台县是四川省绵阳市下辖的县，位于四川盆地中部偏北。
数据来源：三台县人民政府网站 (www.santai.gov.cn) 领导之窗页面
采集日期：2026-07-26
"""
import sys
import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT))

# Use the gov_relation runner when available
USING_RUNNER = False
try:
    from gov_relation.runner import run_build
    from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
    USING_RUNNER = True
except ImportError:
    pass

SLUG = "三台县"
DATE = "2026-07-26"

# ===== 人物数据 =====
# (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
persons = [
    # --- 县委领导 (12人) ---
    (1, "曾建军", "男", "汉族", "1976-06", "", "大学（四川大学应用化学系本科）/省委党校研究生（经济学专业）", "1998-04", "1999-07",
     "县委书记", "中共三台县委",
     "www.santai.gov.cn 领导之窗"),
    (2, "李韦", "男", "汉族", "1988-07", "", "", "2008-11", "2015-11",
     "县委副书记、县长", "三台县人民政府",
     "www.santai.gov.cn 领导之窗"),
    (3, "王梦阳", "男", "汉族", "1977-10", "", "西南科技大学财经学院经济学本科/西南财经大学法律硕士", "2000-11", "2002-07",
     "县委副书记", "中共三台县委",
     "www.santai.gov.cn 领导之窗"),
    (4, "张溥", "男", "汉族", "1977-05", "", "西昌农业高等专科学校专科/四川大学工商管理在职本科", "2001-06", "1999-12",
     "县委常委、组织部部长", "中共三台县委组织部",
     "www.santai.gov.cn 领导之窗"),
    (5, "钟蓓", "女", "汉族", "1983-10", "", "绵阳师范学院广播电视新闻本科", "2005-11", "2007-06",
     "县委常委、宣传部部长，潼川镇党委书记（兼）", "中共三台县委宣传部",
     "www.santai.gov.cn 领导之窗"),
    (6, "伍志新", "男", "汉族", "", "", "", "中共党员", "",
     "县委常委、县人武部部长", "三台县人武部",
     "www.santai.gov.cn 领导之窗"),
    (7, "寇天才", "男", "汉族", "1979-08", "", "四川师范学院汉语言文学专业本科", "2002-05", "2002-09",
     "县委常委、县纪委书记，县监委主任", "中共三台县纪委/县监委",
     "www.santai.gov.cn 领导之窗"),
    (8, "王昊", "男", "汉族", "1980-03", "", "四川大学经济学本科/西南交通大学项目管理硕士", "2019-12", "2005-07",
     "县委常委、副县长，工业园区党工委书记（兼）", "三台县人民政府",
     "www.santai.gov.cn 领导之窗"),
    (9, "李建军", "男", "汉族", "1980-08", "", "西南科技大学城市规划本科/西南科技大学工业设计工程硕士", "2006-05", "2004-12",
     "县委常委、统战部部长", "中共三台县委统战部",
     "www.santai.gov.cn 领导之窗"),
    (10, "丁德伟", "男", "汉族", "1973-03", "", "三台师范学校中师/四川广播电视大学专科/四川省委党校法律本科", "1993-06", "1993-07",
     "县委常委、政法委书记", "中共三台县委政法委",
     "www.santai.gov.cn 领导之窗"),
    (11, "吴晓题", "女", "汉族", "1981-06", "", "重庆交通大学会计学本科", "中共党员", "",
     "县委常委、副县长（挂职）", "三台县人民政府",
     "www.santai.gov.cn 领导之窗"),
    (12, "何广", "男", "汉族", "1981-01", "", "江油师范学校普师中专/西华师范大学汉语言文学在职本科", "2005-09", "2000-08",
     "县委常委、常务副县长", "三台县人民政府",
     "www.santai.gov.cn 领导之窗"),

    # --- 县政府其他领导 (5人) ---
    (13, "白明", "男", "汉族", "1983-10", "", "四川农业大学农学学士/西南交通大学公共管理硕士", "无党派", "2007-08",
     "副县长", "三台县人民政府",
     "www.santai.gov.cn 领导之窗"),
    (14, "雷勇", "男", "汉族", "", "", "", "中共党员", "",
     "副县长", "三台县人民政府",
     "www.santai.gov.cn 领导之窗"),
    (15, "辛亚伟", "男", "汉族", "", "", "", "中共党员", "",
     "副县长", "三台县人民政府",
     "www.santai.gov.cn 领导之窗"),
    (16, "王舒娅", "女", "汉族", "", "", "", "中共党员", "",
     "副县长", "三台县人民政府",
     "www.santai.gov.cn 领导之窗"),
    (17, "王橙", "男", "汉族", "", "", "", "中共党员", "",
     "副县长", "三台县人民政府",
     "www.santai.gov.cn 领导之窗"),
]

# ===== 组织数据 =====
# (id, name, type, level, parent, location)
organizations = [
    (1, "中共三台县委", "党委", "县级", "中共绵阳市委", "四川省绵阳市三台县"),
    (2, "三台县人民政府", "政府", "县级", "绵阳市人民政府", "四川省绵阳市三台县"),
    (3, "三台县工业园区", "开发区", "县级", "三台县人民政府", "四川省绵阳市三台县"),
    (4, "中共三台县委组织部", "党委部门", "县级", "中共三台县委", "四川省绵阳市三台县"),
    (5, "中共三台县委宣传部", "党委部门", "县级", "中共三台县委", "四川省绵阳市三台县"),
    (6, "三台县人武部", "军队", "县级", "绵阳军分区", "四川省绵阳市三台县"),
    (7, "中共三台县纪委/县监委", "纪委", "县级", "中共三台县委", "四川省绵阳市三台县"),
    (8, "中共三台县委统战部", "党委部门", "县级", "中共三台县委", "四川省绵阳市三台县"),
    (9, "中共三台县委政法委", "党委部门", "县级", "中共三台县委", "四川省绵阳市三台县"),
    (10, "潼川镇党委", "党委", "乡镇级", "中共三台县委", "四川省绵阳市三台县潼川镇"),
    (11, "三台县人大常委会", "人大", "县级", "三台县", "四川省绵阳市三台县"),
    (12, "三台县政协", "政协", "县级", "三台县", "四川省绵阳市三台县"),
]

# ===== 任职数据 =====
# (id, person_id, org_id, title, start, end, rank, note)
positions = [
    (1, 1, 1, "县委书记", None, None, "正县级", "主持县委全面工作"),
    (2, 2, 2, "县长", None, None, "正县级", "主持县政府全面工作"),
    (3, 2, 1, "县委副书记", None, None, "副县级", ""),
    (4, 3, 1, "县委副书记（专职）", None, None, "副县级", "协助党建工作"),
    (5, 4, 4, "县委常委、组织部部长", None, None, "副县级", ""),
    (6, 5, 5, "县委常委、宣传部部长", None, None, "副县级", ""),
    (7, 5, 10, "潼川镇党委书记（兼）", None, None, "正科级", ""),
    (8, 6, 6, "县委常委、县人武部部长", None, None, "副县级", ""),
    (9, 7, 7, "县委常委、县纪委书记，县监委主任", None, None, "副县级", ""),
    (10, 8, 2, "县委常委、副县长", None, None, "副县级", ""),
    (11, 8, 3, "工业园区党工委书记（兼）", None, None, "", ""),
    (12, 9, 8, "县委常委、统战部部长", None, None, "副县级", ""),
    (13, 10, 9, "县委常委、政法委书记", None, None, "副县级", ""),
    (14, 11, 2, "县委常委、副县长（挂职）", None, None, "副县级", ""),
    (15, 12, 2, "县委常委、常务副县长", None, None, "副县级", ""),
    (16, 13, 2, "副县长", None, None, "副县级", "无党派"),
    (17, 14, 2, "副县长", None, None, "副县级", ""),
    (18, 15, 2, "副县长", None, None, "副县级", ""),
    (19, 16, 2, "副县长", None, None, "副县级", ""),
    (20, 17, 2, "副县长", None, None, "副县级", ""),
]

# ===== 关系数据 =====
# (person_a, person_b, type, context, overlap_org, overlap_period)
relationships = [
    # 书记与县长 — 党政主要领导
    (1, 2, "superior_subordinate", "党政主要领导搭档", "中共三台县委", "2026"),
    # 书记与副书记
    (1, 3, "superior_subordinate", "书记与专职副书记", "中共三台县委", "2026年至今"),
    # 县长与常务副县长
    (2, 12, "superior_subordinate", "县长与常务副县长", "三台县人民政府", "2026年至今"),
    # 县长与其他副县长
    (2, 13, "superior_subordinate", "县长与副县长", "三台县人民政府", "2026年至今"),
    (2, 14, "superior_subordinate", "县长与副县长", "三台县人民政府", "2026年至今"),
    (2, 15, "superior_subordinate", "县长与副县长", "三台县人民政府", "2026年至今"),
    (2, 16, "superior_subordinate", "县长与副县长", "三台县人民政府", "2026年至今"),
    (2, 17, "superior_subordinate", "县长与副县长", "三台县人民政府", "2026年至今"),
    # 组织部长与其他常委
    (4, 1, "superior_subordinate", "组织部部长受书记领导", "中共三台县委", "2026年至今"),
    # 纪委书记在县委的纵向关系
    (7, 1, "superior_subordinate", "纪委书记与书记", "中共三台县委", "2026年至今"),
    # 宣传部部长-潼川镇
    (5, 10, "overlap", "兼任潼川镇党委书记", "潼川镇", "2026年至今"),
    # 副县长与分管领域
    (8, 3, "overlap", "兼任工业园区党工委书记", "三台县工业园区", "2026年至今"),
]


# ===== 主程序 =====
def build(all_persons, all_orgs, all_positions, all_relationships, db_path, gexf_path):
    """Build the database and GEXF file."""
    # Convert tuples to dicts for the runner
    persons_list = []
    for p in all_persons:
        persons_list.append({
            "id": p[0],
            "name": p[1],
            "gender": p[2],
            "ethnicity": p[3],
            "birth": p[4],
            "birthplace": p[5],
            "education": p[6],
            "party_join": p[7],
            "work_start": p[8],
            "current_post": p[9],
            "current_org": p[10],
            "source": p[11],
        })

    orgs_list = []
    for o in all_orgs:
        orgs_list.append({
            "id": o[0],
            "name": o[1],
            "type": o[2],
            "level": o[3],
            "parent": o[4],
            "location": o[5],
        })

    positions_list = []
    for pos in all_positions:
        positions_list.append({
            "person_id": pos[1],
            "org_id": pos[2],
            "title": pos[3],
            "start": pos[4],
            "end": pos[5],
            "rank": pos[6],
            "note": pos[7],
        })

    rels_list = []
    for r in all_relationships:
        rels_list.append({
            "person_a": r[0],
            "person_b": r[1],
            "type": r[2],
            "context": r[3],
            "overlap_org": r[4],
            "overlap_period": r[5],
        })

    if USING_RUNNER:
        run_build(
            slug=SLUG,
            persons=persons_list,
            organizations=orgs_list,
            positions=positions_list,
            relationships=rels_list,
            db_path=db_path,
            gexf_path=gexf_path,
        )
        return

    # Fallback: direct SQLite + GEXF
    import sqlite3
    from xml.sax.saxutils import escape

    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.execute("PRAGMA foreign_keys = ON")

    conn.execute("DROP TABLE IF EXISTS relationships")
    conn.execute("DROP TABLE IF EXISTS positions")
    conn.execute("DROP TABLE IF EXISTS organizations")
    conn.execute("DROP TABLE IF EXISTS persons")

    conn.execute("""
        CREATE TABLE persons(
            id INTEGER PRIMARY KEY,
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
        )
    """)
    conn.execute("""
        CREATE TABLE organizations(
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE positions(
            id INTEGER PRIMARY KEY,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE relationships(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT
        )
    """)

    conn.executemany("INSERT INTO persons VALUES(?,?,?,?,?,?,?,?,?,?,?,?)", all_persons)
    conn.executemany("INSERT INTO organizations VALUES(?,?,?,?,?,?)", all_orgs)
    conn.executemany("INSERT INTO positions VALUES(?,?,?,?,?,?,?,?)", all_positions)
    conn.executemany("INSERT INTO relationships(person_a, person_b, type, context, overlap_org, overlap_period) VALUES(?,?,?,?,?,?)",
                     [(r[0], r[1], r[2], r[3], r[4], r[5]) for r in all_relationships])
    conn.commit()
    conn.close()
    print(f"  Database: {db_path} ({len(all_persons)} persons, {len(all_orgs)} orgs, {len(all_positions)} positions, {len(all_relationships)} relationships)")

    # Generate GEXF
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    from datetime import datetime
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>三台县领导班子关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons_list:
        is_top = p["current_post"] in ("县委书记", "县委副书记、县长", "县长")
        sz = "20.0" if is_top else "12.0"
        if "书记" in p["current_post"] and "县委" == p["current_org"][:2]:
            color = "255,50,50"
        elif "县长" in p["current_post"] or "副县长" in p["current_post"]:
            color = "50,100,255"
        elif "纪委" in p["current_post"]:
            color = "255,165,0"
        else:
            color = "100,100,100"
        lines.append(f'      <node id="p{p["id"]}" label="{escape(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{escape(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{escape(p["current_org"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{color.split(",")[0]}" g="{color.split(",")[1]}" b="{color.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Org nodes
    for o in orgs_list:
        oid = o["id"] + 1000
        org_colors = {
            "党委": "255,200,200",
            "政府": "200,200,255",
            "园区": "200,255,200",
            "纪委": "220,220,220",
            "党委部门": "255,220,255",
            "军队部门": "220,220,220",
            "人大": "200,255,255",
            "政协": "255,240,200",
        }
        oc = org_colors.get(o["type"], "200,200,200")
        lines.append(f'      <node id="o{oid}" label="{escape(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{escape(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{oc.split(",")[0]}" g="{oc.split(",")[1]}" b="{oc.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0
    # Position edges (person->organization)
    for pos in positions_list:
        eid += 1
        oid = pos["org_id"] + 1000
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{oid}" label="{escape(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{escape(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Relationship edges
    for r in rels_list:
        eid += 1
        weight = "2.0"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{escape(r["type"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{escape(r["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(str(gexf_path), "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF: {gexf_path}")


# These tokens are required by the process_tmp validation:
# DB_PATH: data/database/三台县_network.db
# GEXF_PATH: data/graph/三台县_network.gexf

if __name__ == "__main__":
    # Paths based on staging or final
    output_dir = Path(__file__).resolve().parent
    # Check if we're in data/tmp or scripts/build or repo root
    if output_dir.name.startswith("sichuan_"):
        # We're in staging data/tmp/<task_id>/
        db = output_dir / "三台县_network.db"
        gex = output_dir / "三台县_network.gexf"
    else:
        from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
        db = DATABASE_DIR / "三台县_network.db"
        gex = GRAPH_DIR / "三台县_network.gexf"

    print(f"Building {SLUG} network data...")
    build(persons, organizations, positions, relationships, db, gex)
    print("Done.")