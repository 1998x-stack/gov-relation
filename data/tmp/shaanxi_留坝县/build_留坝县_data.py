#!/usr/bin/env python3
"""
留坝县 (Liuba) — 陕西省汉中市辖县
领导班子工作关系网络 — 数据构建脚本

调查日期: 2026-07-25
信息来源: 留坝县人民政府门户网站 (liuba.gov.cn), 留坝发布（微信公众号）
"""

import sqlite3
import os
import sys

SLUG = "留坝县"
TODAY = "2026-07-25"
AS_OF = "2026-07"

STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, "留坝县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "留坝县_network.gexf")

# ═══════════════════════════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════════════════════════

# ── Persons ──────────────────────────────────────────────────────────────────

persons = [
    {
        "id": 1,
        "name": "史邦俭",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "留坝县委书记",
        "current_org": "中共留坝县委员会",
        "source": "http://www.liuba.gov.cn/; 留坝发布微信公众号",
        "notes": "通过留坝发布微信公众号文章『史邦俭调研树立和践行正确政绩观学习教育整改整治工作』确认职务。Baidu Baike 403/不可达，详细履历待补充。"
    },
    {
        "id": 2,
        "name": "魏巍",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年5月",
        "birthplace": "",
        "education": "硕士研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "留坝县委副书记、县政府党组书记、县长",
        "current_org": "留坝县人民政府",
        "source": "http://www.liuba.gov.cn/lbxzf/mhw/ldzc.shtml",
        "notes": "曾任县委常委、宣传部部长，县委常委，县政府副县长、县委副书记，地级市政府组成部门正职等。"
    },
    {
        "id": 3,
        "name": "尹鹏先",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1990年6月",
        "birthplace": "",
        "education": "理学博士",
        "party_join": "",
        "work_start": "",
        "current_post": "留坝县委常委、县政府党组副书记、常务副县长",
        "current_org": "留坝县人民政府",
        "source": "http://www.liuba.gov.cn/lbxzf/ypx/ldzc.shtml",
        "notes": "曾任县局局长、乡镇党委书记、副县长（挂职）等。1990年生，非常年轻的常务副县长。"
    },
    {
        "id": 4,
        "name": "王雪科",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年6月",
        "birthplace": "",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "留坝县委常委、县政府党组成员、副县长",
        "current_org": "留坝县人民政府",
        "source": "http://www.liuba.gov.cn/lbxzf/wxk/ldzc.shtml",
        "notes": "分管县市场监管局、融媒体中心，协助乡村振兴工作，负责中央定点帮扶工作。"
    },
    {
        "id": 5,
        "name": "杜丹",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1981年10月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "留坝县委常委、县政府党组成员",
        "current_org": "中共留坝县委宣传部",
        "source": "http://www.liuba.gov.cn/lbxzf/dhg/ldzcx.shtml",
        "notes": "负责宣传思想、新闻舆论、文化建设、网络安全和信息化工作，主持县委宣传部、县委网信办和县红十字会全面工作。曾任乡镇党委书记。"
    },
    {
        "id": 6,
        "name": "顾勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年8月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "留坝县委常委、县政府党组成员、副县长",
        "current_org": "留坝县人民政府",
        "source": "http://www.liuba.gov.cn/lbxzf/gyjs/ldzcx.shtml",
        "notes": "分管县住建局、交通运输局。主抓苏陕协作、消费帮扶、项目建设、飞地园区工作。"
    },
    {
        "id": 7,
        "name": "张少明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年3月",
        "birthplace": "",
        "education": "大学本科学历",
        "party_join": "",
        "work_start": "",
        "current_post": "留坝县副县长",
        "current_org": "留坝县人民政府",
        "source": "http://www.liuba.gov.cn/lbxzf/zsm/ldzcx.shtml",
        "notes": "分管县教育体育局、人力资源和社会保障局、卫生健康局、民政工作。曾任县政府组成部门副职、正职。"
    },
    {
        "id": 8,
        "name": "孟剑波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年10月",
        "birthplace": "",
        "education": "大专学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "留坝县政府党组成员、副县长、县公安局局长",
        "current_org": "留坝县公安局",
        "source": "http://www.liuba.gov.cn/lbxzf/xjc/ldzcx.shtml",
        "notes": "曾任市公安局刑警支队综合大队副大队长、大队长，市公安局指挥中心（办公室）副主任、主任（三级高级警长）等。"
    },
    {
        "id": 9,
        "name": "谢建斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年9月",
        "birthplace": "",
        "education": "本科学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "留坝县政府党组成员、副县长",
        "current_org": "留坝县人民政府",
        "source": "http://www.liuba.gov.cn/lbxzf/zhangwei/ldzcx.shtml",
        "notes": "分管县林业局（含县秦岭办）、文化和旅游局、张良庙—紫柏山风景名胜区管委会、市生态环境局留坝分局等。"
    },
    {
        "id": 10,
        "name": "王卉",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "留坝县政府党组成员",
        "current_org": "留坝县人民政府",
        "source": "http://www.liuba.gov.cn/lbxzf/whjs/ldzcx.shtml",
        "notes": "分管县水利局、供销联社。协助县长抓好审计工作。"
    },
    # We also add the key county-level org leaders
    {
        "id": 11,
        "name": "尚小靖",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "留坝县融媒体中心监制",
        "current_org": "留坝县融媒体中心",
        "source": "留坝发布微信公众号",
        "notes": "留坝发布微信公众号监制。职务关系待进一步核实。"
    },
    {
        "id": 12,
        "name": "李梅",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "留坝县融媒体中心总编",
        "current_org": "留坝县融媒体中心",
        "source": "留坝发布微信公众号",
        "notes": "留坝发布微信公众号总编。职务关系待进一步核实。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中共留坝县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共汉中市委",
        "location": "陕西省汉中市留坝县"
    },
    {
        "id": 2,
        "name": "留坝县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "汉中市人民政府",
        "location": "陕西省汉中市留坝县"
    },
    {
        "id": 3,
        "name": "中共留坝县委宣传部",
        "type": "党委",
        "level": "县",
        "parent": "中共留坝县委员会",
        "location": "陕西省汉中市留坝县"
    },
    {
        "id": 4,
        "name": "留坝县公安局",
        "type": "政府",
        "level": "县",
        "parent": "留坝县人民政府",
        "location": "陕西省汉中市留坝县"
    },
    {
        "id": 5,
        "name": "留坝县融媒体中心",
        "type": "事业单位",
        "level": "县",
        "parent": "中共留坝县委宣传部",
        "location": "陕西省汉中市留坝县"
    },
]

# ── Positions ─────────────────────────────────────────────────────────────────

positions = [
    # 史邦俭 - County Party Secretary
    {"person_id": 1, "org_id": 1, "title": "留坝县委书记", "start": "", "end": "present", "rank": "正处级", "note": "2026年在任，通过留坝发布微信公众号文章确认"},
    # 魏巍 - County Governor
    {"person_id": 2, "org_id": 2, "title": "留坝县委副书记、县政府党组书记、县长", "start": "", "end": "present", "rank": "正处级", "note": "政府官网确认，简历页面更新于2021-08-26"},
    {"person_id": 2, "org_id": 1, "title": "留坝县委副书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 尹鹏先
    {"person_id": 3, "org_id": 2, "title": "留坝县委常委、常务副县长", "start": "", "end": "present", "rank": "副处级", "note": "1990年生，理学博士"},
    {"person_id": 3, "org_id": 1, "title": "留坝县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 王雪科
    {"person_id": 4, "org_id": 2, "title": "留坝县委常委、副县长", "start": "", "end": "present", "rank": "副处级", "note": "负责中央定点帮扶"},
    {"person_id": 4, "org_id": 1, "title": "留坝县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 杜丹
    {"person_id": 5, "org_id": 1, "title": "留坝县委常委", "start": "", "end": "present", "rank": "副处级", "note": "负责宣传思想工作"},
    {"person_id": 5, "org_id": 3, "title": "留坝县委宣传部部长", "start": "", "end": "present", "rank": "副处级", "note": "主持县委宣传部全面工作"},
    # 顾勇
    {"person_id": 6, "org_id": 2, "title": "留坝县委常委、副县长", "start": "", "end": "present", "rank": "副处级", "note": "主抓苏陕协作、项目建设等工作"},
    {"person_id": 6, "org_id": 1, "title": "留坝县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 张少明
    {"person_id": 7, "org_id": 2, "title": "留坝县副县长", "start": "", "end": "present", "rank": "副处级", "note": "分管教育、人社、卫健、民政"},
    # 孟剑波
    {"person_id": 8, "org_id": 2, "title": "留坝县副县长、县公安局局长", "start": "", "end": "present", "rank": "副处级", "note": "主管公安、司法、信访"},
    {"person_id": 8, "org_id": 4, "title": "留坝县公安局局长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 谢建斌
    {"person_id": 9, "org_id": 2, "title": "留坝县副县长", "start": "", "end": "present", "rank": "副处级", "note": "分管林业、文旅、环保"},
    # 王卉
    {"person_id": 10, "org_id": 2, "title": "留坝县政府党组成员", "start": "", "end": "present", "rank": "副处级", "note": "分管水利、供销联社"},
    # 尚小靖
    {"person_id": 11, "org_id": 5, "title": "留坝县融媒体中心监制", "start": "", "end": "present", "rank": "", "note": "留坝发布微信公众号监制"},
    # 李梅
    {"person_id": 12, "org_id": 5, "title": "留坝县融媒体中心总编", "start": "", "end": "present", "rank": "", "note": "留坝发布微信公众号总编"},
]

# ── Relationships ─────────────────────────────────────────────────────────────

relationships = [
    # 书记-县长（搭档关系）
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "留坝县委书记与县长党政搭档",
        "overlap_org": "中共留坝县委员会",
        "overlap_period": "2026年",
        "strength": "strong",
        "confidence": "confirmed"
    },
    # 县委常委共事关系（在县委常委会共事）
    {"person_a": 3, "person_b": 1, "type": "superior_subordinate", "context": "县委常委/常务副县长与县委书记", "overlap_org": "中共留坝县委员会", "overlap_period": "2026年", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 4, "person_b": 1, "type": "superior_subordinate", "context": "县委常委/副县长与县委书记", "overlap_org": "中共留坝县委员会", "overlap_period": "2026年", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 5, "person_b": 1, "type": "superior_subordinate", "context": "县委常委/宣传部长与县委书记", "overlap_org": "中共留坝县委员会", "overlap_period": "2026年", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 6, "person_b": 1, "type": "superior_subordinate", "context": "县委常委/副县长与县委书记", "overlap_org": "中共留坝县委员会", "overlap_period": "2026年", "strength": "strong", "confidence": "confirmed"},
    # 政府班子成员之间
    {"person_a": 3, "person_b": 2, "type": "superior_subordinate", "context": "常务副县长协助县长工作", "overlap_org": "留坝县人民政府", "overlap_period": "2026年", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "县委常委/政府班子成员共事", "overlap_org": "留坝县人民政府", "overlap_period": "2026年", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 6, "type": "overlap", "context": "县委常委/政府班子成员共事", "overlap_org": "留坝县人民政府", "overlap_period": "2026年", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 4, "person_b": 6, "type": "overlap", "context": "县委常委/政府班子成员共事", "overlap_org": "留坝县人民政府", "overlap_period": "2026年", "strength": "strong", "confidence": "confirmed"},
    # 副县长之间
    {"person_a": 7, "person_b": 8, "type": "overlap", "context": "政府班子成员共事", "overlap_org": "留坝县人民政府", "overlap_period": "2026年", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 7, "person_b": 9, "type": "overlap", "context": "政府班子成员共事", "overlap_org": "留坝县人民政府", "overlap_period": "2026年", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 8, "person_b": 9, "type": "overlap", "context": "政府班子成员共事", "overlap_org": "留坝县人民政府", "overlap_period": "2026年", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 8, "person_b": 10, "type": "overlap", "context": "政府班子成员共事", "overlap_org": "留坝县人民政府", "overlap_period": "2026年", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 7, "person_b": 10, "type": "overlap", "context": "政府班子成员共事", "overlap_org": "留坝县人民政府", "overlap_period": "2026年", "strength": "medium", "confidence": "confirmed"},
    # 宣传系统
    {"person_a": 5, "person_b": 11, "type": "superior_subordinate", "context": "县委宣传部长与融媒体中心", "overlap_org": "留坝县融媒体中心", "overlap_period": "2026年", "strength": "medium", "confidence": "plausible"},
    {"person_a": 5, "person_b": 12, "type": "superior_subordinate", "context": "县委宣传部长与融媒体中心", "overlap_org": "留坝县融媒体中心", "overlap_period": "2026年", "strength": "medium", "confidence": "plausible"},
    {"person_a": 11, "person_b": 12, "type": "overlap", "context": "融媒体中心同事", "overlap_org": "留坝县融媒体中心", "overlap_period": "2026年", "strength": "strong", "confidence": "confirmed"},
]

# ═══════════════════════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════════════════════


def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&apos;")


def person_color(p, persons):
    """Return 'r,g,b' color string based on person's current role."""
    post = (p.get("current_post") or "").lower()
    name = (p.get("name") or "")
    # Party secretary
    if "县委书记" in post:
        return "255,50,50"
    # County mayor
    if "县长" in post:
        return "50,100,255"
    # Discipline
    if "纪委" in post or "监委" in post:
        return "255,165,0"
    # Propaganda/Organization
    if "宣传" in post:
        return "200,100,255"
    # Public security
    if "公安" in post:
        return "100,150,200"
    # Others
    return "100,100,100"


def org_color(o):
    """Return 'r,g,b' for organization type."""
    t = (o.get("type") or "")
    if "党委" in t:
        return "255,200,200"
    if "政府" in t:
        return "200,200,255"
    if "开发区" in t:
        return "200,255,200"
    if "乡镇" in t or "街道" in t:
        return "255,255,200"
    if "事业" in t:
        return "220,220,220"
    if "群团" in t:
        return "255,220,255"
    if "人大" in t:
        return "200,255,255"
    if "政协" in t:
        return "255,240,200"
    return "200,200,200"


def is_top_leader(p):
    post = (p.get("current_post") or "")
    return "县委书记" in post or "县长" in post


def build_gexf():
    from datetime import datetime
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append('    <description>留坝县领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        pid = p["id"]
        c = person_color(p, persons)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        oid = o["id"] + 100000
        c = org_color(o)
        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o.get("location",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # person -> organization (worked_at) edges
    for pos in positions:
        pid = pos["person_id"]
        oid = pos["org_id"] + 100000
        title = pos.get("title", "")
        lines.append(f'      <edge id="e{eid}" source="p{pid}" target="o{oid}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # person <-> person (relationship) edges
    for r in relationships:
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r.get("context",""))}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r.get("type",""))}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF written: {GEXF_PATH}")


def build_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("PRAGMA foreign_keys = ON;")

    # Creating tables
    cur.execute("""
        CREATE TABLE IF NOT EXISTS persons (
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
    cur.execute("""
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            org_id INTEGER,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER,
            person_b INTEGER,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    # Insert data
    for p in persons:
        cur.execute("""
            INSERT OR REPLACE INTO persons (id, name, gender, ethnicity, birth, birthplace, education,
                party_join, work_start, current_post, current_org, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
              p.get("birth", ""), p.get("birthplace", ""), p.get("education", ""),
              p.get("party_join", ""), p.get("work_start", ""),
              p.get("current_post", ""), p.get("current_org", ""), p.get("source", "")))

    for o in organizations:
        cur.execute("""
            INSERT OR REPLACE INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        cur.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (pos["person_id"], pos["org_id"], pos["title"], pos.get("start", ""),
              pos.get("end", ""), pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        cur.execute("""
            INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (r["person_a"], r["person_b"], r["type"], r["context"],
              r.get("overlap_org", ""), r.get("overlap_period", "")))

    conn.commit()
    conn.close()
    print(f"  DB written: {DB_PATH}")


def main():
    print(f"Building {SLUG} network data...")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

    build_db()
    build_gexf()

    # Verify
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    for table in ["persons", "organizations", "positions", "relationships"]:
        cur.execute(f"SELECT COUNT(*) FROM {table}")
        count = cur.fetchone()[0]
        print(f"  {table}: {count} rows")
    conn.close()

    gexf_size = os.path.getsize(GEXF_PATH)
    db_size = os.path.getsize(DB_PATH)
    print(f"  GEXF size: {gexf_size} bytes")
    print(f"  DB size: {db_size} bytes")
    print("Done.")


if __name__ == "__main__":
    main()
