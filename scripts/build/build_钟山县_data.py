#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 钟山县 (Zhongshan County, Guangxi Hezhou) leadership network.

归口地区: 广西壮族自治区贺州市钟山县
核心目标: 县委书记 & 县长
"""

import sqlite3
import os
import sys
from datetime import datetime, date

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, REPO_ROOT

SLUG = "钟山县"
PROVINCE = "广西壮族自治区"
PARENT_CITY = "贺州市"
TODAY = "2026-08-05"

# Use staging directory
STAGING = REPO_ROOT / "data/tmp/guangxi_钟山县"
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# ═══════════════════════════════════════════════════════════════════════════
# DATA — hardcoded research data
# Sources (see person JSON source_register for full URLs):
#   - 新京报 (bjnews.com.cn) 2024-09-10 / 2025-07 (程钊任县委书记、拟任贺州副市长)
#   - 广西县域经济网 gxcounty.com/zhengwu/rsrm/182119 (程钊/陈信东简介与任免)
#   - 腾讯新闻 2024-08-20 / 2024-09-10 (公示、任免)
#   - 贺州市人民政府领导之窗 www.gxhz.gov.cn (程兼任贺州市副市长)
#   - 钟山纪检监察网 www.gxzsjjjc.gov.cn (领导成员访谈/会议)
#   - 人民网广西频道、360百科 (前任书记黄卫东)
# Confirmed as of 2026-08-05
# ═══════════════════════════════════════════════════════════════════════════

# ── Core figures & 四家班子 ──────────────────────────────────────────────
# 程钊 (id 1) — 县委书记
# 陈信东 (id 2) — 县长
persons = [
    {
        "id": 1,
        "name": "程钊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年12月",
        "birthplace": "湖北赤壁",
        "education": "上海交通大学船舶海洋与建筑工程学院水声工程专业（研究生学历，工学博士）；中国人民大学信息学工学学士",
        "party_join": "2005年5月",
        "work_start": "2012年7月",
        "current_post": "钟山县委书记（兼任贺州市副市长）",
        "current_org": "中共钟山县委员会（兼任贺州市人民政府）",
    },
    {
        "id": 2,
        "name": "陈信东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年1月",
        "birthplace": "广西贺州",
        "education": "桂林理工大学在职研究生（工程硕士）；桂林工学院高分子材料与工程专业本科",
        "party_join": "2005年4月",
        "work_start": "2002年11月",
        "current_post": "钟山县委副书记、县长",
        "current_org": "钟山县人民政府",
    },
    # 班子其他成员
    {
        "id": 3,
        "name": "杨喜",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "钟山县委副书记",
        "current_org": "中共钟山县委员会",
    },
    {
        "id": 4,
        "name": "张楠",
        "gender": "待查",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "钟山县委常委、县纪委书记、县监委代理主任",
        "current_org": "中共钟山县纪律检查委员会",
    },
    {
        "id": 5,
        "name": "兰宝铁",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "钟山县委常委、县委办公室主任",
        "current_org": "中共钟山县委员会办公室",
    },
    {
        "id": 6,
        "name": "廖正聪",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "钟山县人大常委会主任",
        "current_org": "钟山县人大常委会",
    },
    {
        "id": 7,
        "name": "罗敬资",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "钟山县政协主席",
        "current_org": "中国人民政治协商会议钟山县委员会",
    },
    {
        "id": 8,
        "name": "黄卫东",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1969年11月",
        "birthplace": "广西贺州",
        "education": "在职研究生学历",
        "party_join": "1992年5月",
        "work_start": "1992年7月",
        "current_post": "贺州市政协副主席（原钟山县委书记）",
        "current_org": "中国人民政治协商会议贺州市委员会",
    },
    {
        "id": 9,
        "name": "黎祖旗",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "钟山县原县委常委、纪委书记、监委主任",
        "current_org": "中共钟山县纪律检查委员会",
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共钟山县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共贺州市委员会",
        "location": "广西壮族自治区贺州市钟山县",
    },
    {
        "id": 2,
        "name": "钟山县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "贺州市人民政府",
        "location": "广西壮族自治区贺州市钟山县",
    },
    {
        "id": 3,
        "name": "中共钟山县纪律检查委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共贺州市纪律检查委员会",
        "location": "广西壮族自治区贺州市钟山县",
    },
    {
        "id": 4,
        "name": "钟山县人大常委会",
        "type": "人大",
        "level": "县级",
        "parent": "贺州市人大常委会",
        "location": "广西壮族自治区贺州市钟山县",
    },
    {
        "id": 5,
        "name": "中国人民政治协商会议钟山县委员会",
        "type": "政协",
        "level": "县级",
        "parent": "贺州市政协",
        "location": "广西壮族自治区贺州市钟山县",
    },
    {
        "id": 6,
        "name": "中国人民政治协商会议贺州市委员会",
        "type": "政协",
        "level": "市级",
        "parent": "广西壮族自治区政协",
        "location": "广西壮族自治区贺州市",
    },
    {
        "id": 7,
        "name": "中共昭平县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共贺州市委员会",
        "location": "广西壮族自治区贺州市昭平县",
    },
    {
        "id": 8,
        "name": "中共贺州市八步区委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共贺州市委员会",
        "location": "广西壮族自治区贺州市八步区",
    },
]

positions = [
    # 程钊 — 县委书记
    {"id": 1, "person_id": 1, "org_id": 1, "title": "钟山县委书记", "start": "2024-09", "end": "present", "rank": "正处级", "note": "2024年9月9日领导干部大会宣布任书记；兼任贺州市副市长"},
    {"id": 2, "person_id": 1, "org_id": 2, "title": "钟山县委副书记、县长", "start": "2021-09", "end": "2024-09", "rank": "正处级", "note": "2021年9月转正县长"},
    {"id": 3, "person_id": 1, "org_id": 2, "title": "钟山县委副书记、县长人选/政府主要负责人", "start": "2021-06", "end": "2021-09", "rank": "正处级", "note": "2021年6月拟任县区长人选，7-9月县长人选"},
    {"id": 4, "person_id": 1, "org_id": 2, "title": "钟山县委常委、常务副县长（三级调研员）", "start": "2018-10", "end": "2021-06", "rank": "副处级", "note": "2020年1月起三级调研员"},
    {"id": 5, "person_id": 1, "org_id": 2, "title": "柳州市鹿寨县副县长、县政府党组成员", "start": "2016-08", "end": "2018-10", "rank": "副处级", "note": "2016年4月提名为副县长人选" },
    {"id": 6, "person_id": 1, "org_id": 2, "title": "广西壮族自治区人民政府办公厅第五秘书处副调研员/鹿寨挂职", "start": "2015-02", "end": "2016-08", "rank": "副处级", "note": "自治区政府办第五秘书处副调研员"},
    {"id": 7, "person_id": 1, "org_id": 2, "title": "广西壮族自治区人民政府办公厅信息处（主任科员）", "start": "2012-07", "end": "2015-02", "rank": "正科级", "note": "选调生入桂，信息处干部/主任科员"},
    # 陈信东 — 县长
    {"id": 8, "person_id": 2, "org_id": 2, "title": "钟山县委副书记、县长", "start": "2024-09", "end": "present", "rank": "正处级", "note": "2024年9月任副书记、提名县长候选人"},
    {"id": 9, "person_id": 2, "org_id": 7, "title": "昭平县委副书记", "start": "2023-12", "end": "2024-09", "rank": "副处级", "note": "此前任昭平县委副书记"},
    {"id": 10, "person_id": 2, "org_id": 7, "title": "昭平县委常委、常务副县长、县政府党组副书记", "start": "2021-07", "end": "2023-12", "rank": "副处级", "note": "2023年10月一级调研员?（待核）"},
    {"id": 11, "person_id": 2, "org_id": 8, "title": "贺州市八步区委常委、区委办公室主任", "start": "2020-10", "end": "2021-07", "rank": "副处级", "note": ""},
    {"id": 12, "person_id": 2, "org_id": 8, "title": "八步区农业农村局党组书记、局长（一级主任科员）", "start": "2018-07", "end": "2020-10", "rank": "正科级", "note": ""},
    {"id": 13, "person_id": 2, "org_id": 8, "title": "八步区水利局党组书记、局长", "start": "2015-06", "end": "2018-07", "rank": "正科级", "note": "桂林理工大学在职工程硕士(2013-2015)"},
    {"id": 14, "person_id": 2, "org_id": 8, "title": "八步区乡镇党委书记 / 镇长", "start": "2008-06", "end": "2015-06", "rank": "正科级", "note": "乡镇党委副书记、镇长、乡镇党委书记等"},
    {"id": 15, "person_id": 2, "org_id": 8, "title": "八步区乡镇中学教师（团干部）", "start": "2002-11", "end": "2008-06", "rank": "事业编/公务员", "note": ""},
    # 杨喜 — 县委副书记
    {"id": 16, "person_id": 3, "org_id": 1, "title": "钟山县委副书记", "start": "待查", "end": "present", "rank": "副处级", "note": "纪检监察网多次报道在任"},
    # 张楠 — 纪委书记（代理）
    {"id": 17, "person_id": 4, "org_id": 3, "title": "钟山县委常委、县纪委书记、县监委代理主任", "start": "待查", "end": "present", "rank": "副处级", "note": "2026年纪检监察网报道"}, 
    # 兰宝铁 — 县委办主任
    {"id": 18, "person_id": 5, "org_id": 1, "title": "钟山县委常委、县委办公室主任", "start": "待查", "end": "present", "rank": "副处级", "note": ""},
    # 廖正聪 — 人大
    {"id": 19, "person_id": 6, "org_id": 4, "title": "钟山县人大常委会主任", "start": "待查", "end": "present", "rank": "正处级", "note": ""},
    # 罗敬资 — 政协
    {"id": 20, "person_id": 7, "org_id": 5, "title": "钟山县政协主席", "start": "待查", "end": "present", "rank": "正处级", "note": "继林婕之后任政协主席"},
    # 黄卫东 — 前任县委书记
    {"id": 21, "person_id": 8, "org_id": 1, "title": "钟山县委书记", "start": "待查", "end": "2024-09", "rank": "正处级", "note": "前任书记，2024-09卸任"},
    {"id": 22, "person_id": 8, "org_id": 6, "title": "贺州市政协副主席", "start": "2024-05", "end": "present", "rank": "副厅级", "note": "2024年5月提名为政协副主席人选"},
    # 黎祖旗 — 原纪委书记
    {"id": 23, "person_id": 9, "org_id": 3, "title": "钟山县委常委、县纪委书记、监委主任", "start": "待查", "end": "待查", "rank": "副处级", "note": "程任书记期间负责纪委工作"},
]

relationships = [
    {"id": 1, "person_a": 1, "person_b": 2, "type": "党政正职搭档", "context": "县委书记与县长，钟山县党政领导核心搭档（先后任同一县领导岗位）", "overlap_org": "钟山县", "overlap_period": "2024年9月至今"},
    {"id": 2, "person_a": 1, "person_b": 8, "type": "前任继任", "context": "程钊继黄卫东任钟山县委书记", "overlap_org": "中共钟山县委员会", "overlap_period": "2024年9月"},
    {"id": 3, "person_a": 1, "person_b": 9, "type": "同级班子", "context": "程与黎祖旗在钟山县委班子共事（黎任纪委书记期间）", "overlap_org": "中共钟山县委员会", "overlap_period": "2021-2023"},
    {"id": 4, "person_a": 1, "person_b": 3, "type": "上下级", "context": "程任县委书记，杨任县委副书记", "overlap_org": "中共钟山县委员会", "overlap_period": "2024年9月至今"},
    {"id": 5, "person_a": 2, "person_b": 3, "type": "上下级", "context": "陈任县长，杨任县委副书记", "overlap_org": "中共钟山县委员会", "overlap_period": "2024年9月至今"},
    {"id": 6, "person_a": 2, "person_b": 9, "type": "同级班子", "context": "陈、黎同期在钟山县班子（纪委）", "overlap_org": "中共钟山县委员会", "overlap_period": "2024-2026待核"},
    {"id": 7, "person_a": 8, "person_b": 1, "type": "工作交集", "context": "黄卫东任书记时，程为县长，二人为党政搭档", "overlap_org": "钟山县", "overlap_period": "2021-2024"},
]

# ═══════════════════════════════════════════════════════════════════════════
# GEXF node colors
# ═══════════════════════════════════════════════════════════════════════════

COLORS = {
    "party_secretary": "255,50,50",   # Red — 县委书记
    "mayor": "50,100,255",             # Blue — 县长/政府
    "discipline": "255,165,0",         # Orange — 纪委
    "other_person": "100,100,100",     # Grey
    "org_dangwei": "255,200,200",     # Pink — 党委
    "org_gov": "200,200,255",         # Light blue — 政府
    "org_renda": "200,255,255",       # Cyan — 人大
    "org_zhengxie": "255,240,200",    # Cream — 政协
    "org_default": "200,200,200",
}

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def build_gexf(output_path):
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>Sisyphus Research Agent</creator>')
    lines.append(f'    <description>钟山县领导工作关系网络 — 广西贺州市钟山县, as of {TODAY}</description>')
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
        pid = p["id"]
        name = p["name"]
        # 程钊 -> 书记(red), 陈信东 -> 政府(blue), 张楠/黎祖旗 -> 纪委(orange), 黄卫东 -> 书记红? 政协? 简化
        if pid == 1:
            color = COLORS["party_secretary"]; sz = "20.0"; role = "县委书记"
        elif pid == 2:
            color = COLORS["mayor"]; sz = "20.0"; role = "县长"
        elif pid in (4, 9):
            color = COLORS["discipline"]; sz = "12.0"; role = "纪委书记"
        elif pid == 8:
            color = COLORS["other_person"]; sz = "12.0"; role = "前任县委书记/市政协副主席"
        else:
            color = COLORS["other_person"]; sz = "12.0"; role = "班子成员"
        c = color.split(",")
        lines.append(f'      <node id="p{pid}" label="{esc(name)}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for org in organizations:
        oid = org["id"]; oname = org["name"]; otype = org["type"]
        color = COLORS["org_dangwei"]
        if otype == "政府": color = COLORS["org_gov"]
        elif otype == "人大": color = COLORS["org_renda"]
        elif otype == "政协": color = COLORS["org_zhengxie"]
        c = color.split(",")
        lines.append(f'      <node id="o{oid}" label="{esc(oname)}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(otype)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for rel in relationships:
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{rel["person_a"]}" target="p{rel["person_b"]}" label="{esc(rel["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(rel["context"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

def main():
    print(f"Building {SLUG} network...")
    print(f"  DB path: {DB_PATH}")
    print(f"  GEXF path: {GEXF_PATH}")

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    print("  Writing custom GEXF with viz attributes...")
    build_gexf(GEXF_PATH)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM persons"); p_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM organizations"); o_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM positions"); pos_count = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM relationships"); r_count = cur.fetchone()[0]
    conn.close()

    print(f"\n  Summary: {p_count} persons, {o_count} organizations, {pos_count} positions, {r_count} relationships")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print("Done.")


if __name__ == "__main__":
    main()