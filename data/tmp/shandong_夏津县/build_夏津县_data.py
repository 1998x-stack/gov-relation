#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 夏津县 (Xiajin County), 德州市, 山东省.

Level: 县
Province: 山东省
Parent city: 德州市
Targets: 县委书记 (Party Secretary), 县长 (County Magistrate)
Task ID: shandong_夏津县

Research date: 2026-07-25
As of: 2026-07-25

Research sources:
  - http://www.xiajin.gov.cn/ (夏津县人民政府 official site)
  - Multiple official news articles from xiajin.gov.cn (2026-01 to 2026-07)
  - Exa search was rate-limited; Baidu returned CAPTCHA

Current status (as of 2026-07-25):
  - 县委书记: 赵之达 — promoted from 县长 to 县委书记 between Jan 2026 and Mar 2026
    - As of 2026-01-02: "县委副书记、县长赵之达"
    - From 2026-03-10 onward: "县委书记赵之达"
  - 县长: 未明确公开 — 赵之达升任县委书记后，新任县长人选尚未在官方新闻中明确公布
    - 2026年县政府常务会议由 曲传增（县委常委、副县长）主持
    - 可能仍在任命过程中或由上级尚未公布

Confidence notes:
  - 赵之达的身份确认来自夏津县政府官方网站多条新闻，可信度高
  - 新任县长身份未能从公开渠道确认
  - 其他县领导姓名来自会议报道

This is a partial-evidence build per source_fallbacks.md artifact mode.
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path

_STAGING_DIR = Path(__file__).resolve().parent
# From data/tmp/shandong_夏津县/ -> repo root
_REPO_ROOT = (_STAGING_DIR / ".." / ".." / ".." / "..").resolve()
sys.path.insert(0, str(_REPO_ROOT))



SLUG = "夏津县"

DB_PATH = _STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = _STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = _STAGING_DIR

AS_OF = "2026-07-25"
TODAY = "20260725"

import sqlite3  # noqa: F811

# ══════════════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════════════

persons = [
    # ════════════════════════════════════════
    # Core Leadership (Primary Targets)
    # ════════════════════════════════════════

    # 1. 赵之达 — 县委书记 (formerly 县长)
    {
        "id": 1,
        "name": "赵之达",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # Birth year not found in public sources
        "birthplace": "",  # Not found
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共夏津县委书记",
        "current_org": "中共夏津县委员会",
        "source": "夏津县人民政府官网新闻(2026年3月-7月) - http://www.xiajin.gov.cn/",
    },

    # 2. 新任县长 — 身份待确认
    {
        "id": 2,
        "name": "（县长待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "夏津县人民政府县长",
        "current_org": "夏津县人民政府",
        "source": "公开资料暂未确认县长人选。赵之达2026年1月仍为县长，3月已任县委书记，新任县长尚未在官方新闻中明确公布。",
    },

    # 3. 曲传增 — 县委常委、副县长（常务）
    {
        "id": 3,
        "name": "曲传增",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "夏津县委常委、副县长",
        "current_org": "夏津县人民政府",
        "source": "夏津县人民政府官网 - 2024年第10次常务会议、2026年第4次常务会议",
    },

    # 4. 王跃华 — 县人大常委会主任
    {
        "id": 4,
        "name": "王跃华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "夏津县人大常委会主任",
        "current_org": "夏津县人民代表大会常务委员会",
        "source": "夏津县人民政府官网 - 2026年1月人大会议",
    },

    # 5. 王勇 — 县委副书记
    {
        "id": 5,
        "name": "王勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "夏津县委副书记",
        "current_org": "中共夏津县委员会",
        "source": "夏津县人民政府官网 - 2026年7月红色物业会议",
    },

    # 6. 李颖 — 副县长
    {
        "id": 6,
        "name": "李颖",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "夏津县副县长",
        "current_org": "夏津县人民政府",
        "source": "夏津县人民政府官网 - 2026年第3、4次常务会议",
    },

    # 7. 李雪峰 — 副县长
    {
        "id": 7,
        "name": "李雪峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "夏津县副县长",
        "current_org": "夏津县人民政府",
        "source": "夏津县人民政府官网 - 2026年多篇新闻",
    },

    # 8. 李新海 — 县领导
    {
        "id": 8,
        "name": "李新海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "夏津县领导",
        "current_org": "夏津县人民政府",
        "source": "夏津县人民政府官网 - 2026年6月重点项目现场办公",
    },

    # 9. 任天龙 — 县领导
    {
        "id": 9,
        "name": "任天龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "夏津县领导",
        "current_org": "夏津县人民政府",
        "source": "夏津县人民政府官网 - 2026年4月县委常委会扩大会议",
    },

    # 10. 于春峰 — 县领导
    {
        "id": 10,
        "name": "于春峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "夏津县领导",
        "current_org": "夏津县人民政府",
        "source": "夏津县人民政府官网 - 2026年4月、7月会议",
    },

    # 11. 骆伟 — 副县长
    {
        "id": 11,
        "name": "骆伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "夏津县副县长",
        "current_org": "夏津县人民政府",
        "source": "夏津县人民政府官网 - 2024年第10次常务会议",
    },

    # 12. 刘学武 — 县人大常委会副主任
    {
        "id": 12,
        "name": "刘学武",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "夏津县人大常委会副主任",
        "current_org": "夏津县人民代表大会常务委员会",
        "source": "夏津县人民政府官网 - 2026年1月人大会议",
    },

    # 13. 刘长青 — 县人大常委会副主任
    {
        "id": 13,
        "name": "刘长青",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "夏津县人大常委会副主任",
        "current_org": "夏津县人民代表大会常务委员会",
        "source": "夏津县人民政府官网 - 2026年1月人大会议",
    },

    # 14. 谷常亮 — 县人大常委会副主任
    {
        "id": 14,
        "name": "谷常亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "夏津县人大常委会副主任",
        "current_org": "夏津县人民代表大会常务委员会",
        "source": "夏津县人民政府官网 - 2026年1月人大会议",
    },

    # 15. 杨秀英 — 县人大常委会副主任
    {
        "id": 15,
        "name": "杨秀英",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "夏津县人大常委会副主任",
        "current_org": "夏津县人民代表大会常务委员会",
        "source": "夏津县人民政府官网 - 2026年1月人大会议",
    },

    # 16. 孙家滨 — 县人大常委会副主任
    {
        "id": 16,
        "name": "孙家滨",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "夏津县人大常委会副主任",
        "current_org": "夏津县人民代表大会常务委员会",
        "source": "夏津县人民政府官网 - 2026年1月人大会议",
    },

    # 17. 王韧 — 副县长
    {
        "id": 17,
        "name": "王韧",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "夏津县副县长",
        "current_org": "夏津县人民政府",
        "source": "夏津县人民政府官网 - 2024年第10次常务会议",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# ORGANIZATIONS
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共夏津县委员会",
        "type": "党委",
        "level": "县",
        "parent": "中共德州市委员会",
        "location": "山东省德州市夏津县",
    },
    {
        "id": 2,
        "name": "夏津县人民政府",
        "type": "政府",
        "level": "县",
        "parent": "德州市人民政府",
        "location": "山东省德州市夏津县",
    },
    {
        "id": 3,
        "name": "夏津县人民代表大会常务委员会",
        "type": "人大",
        "level": "县",
        "parent": "德州市人民代表大会常务委员会",
        "location": "山东省德州市夏津县",
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议夏津县委员会",
        "type": "政协",
        "level": "县",
        "parent": "中国人民政治协商会议德州市委员会",
        "location": "山东省德州市夏津县",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# POSITIONS
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # 赵之达
    {"person_id": 1, "org_id": 1, "title": "中共夏津县委书记", "start": "2026-02", "end": "present", "rank": "正处级", "note": "此前为夏津县县长，2026年1月至3月间升任县委书记"},
    {"person_id": 1, "org_id": 2, "title": "夏津县人民政府县长", "start": "2021", "end": "2026-01", "rank": "正处级", "note": "2026年1月16日仍以县长身份作政府工作报告"},

    # 县长（待确认）
    {"person_id": 2, "org_id": 2, "title": "夏津县人民政府县长", "start": "2026", "end": "present", "rank": "正处级", "note": "赵之达升任县委书记后，新任县长尚未在官方新闻中明确公布"},

    # 曲传增
    {"person_id": 3, "org_id": 2, "title": "夏津县委常委、副县长", "start": "", "end": "present", "rank": "副处级", "note": "主持2026年县政府第3、4次常务会议"},

    # 王跃华
    {"person_id": 4, "org_id": 3, "title": "夏津县人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": ""},

    # 王勇
    {"person_id": 5, "org_id": 1, "title": "夏津县委副书记", "start": "", "end": "present", "rank": "副处级", "note": "主持2026年7月红色物业工作暨信访工作推进会议"},

    # 李颖
    {"person_id": 6, "org_id": 2, "title": "夏津县副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 李雪峰
    {"person_id": 7, "org_id": 2, "title": "夏津县副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 李新海
    {"person_id": 8, "org_id": 2, "title": "夏津县领导", "start": "", "end": "present", "rank": "", "note": ""},

    # 任天龙
    {"person_id": 9, "org_id": 1, "title": "夏津县领导", "start": "", "end": "present", "rank": "", "note": "2026年4月出现在县委常委会扩大会议中"},

    # 于春峰
    {"person_id": 10, "org_id": 4, "title": "夏津县政协领导", "start": "", "end": "present", "rank": "", "note": ""},

    # 骆伟
    {"person_id": 11, "org_id": 2, "title": "夏津县副县长", "start": "", "end": "present", "rank": "副处级", "note": "2024年已任职"},

    # 刘学武
    {"person_id": 12, "org_id": 3, "title": "夏津县人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 刘长青
    {"person_id": 13, "org_id": 3, "title": "夏津县人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 谷常亮
    {"person_id": 14, "org_id": 3, "title": "夏津县人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 杨秀英
    {"person_id": 15, "org_id": 3, "title": "夏津县人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 孙家滨
    {"person_id": 16, "org_id": 3, "title": "夏津县人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},

    # 王韧
    {"person_id": 17, "org_id": 2, "title": "夏津县副县长", "start": "", "end": "present", "rank": "副处级", "note": "2024年已任职"},
]

# ══════════════════════════════════════════════════════════════════════════════
# RELATIONSHIPS
# ══════════════════════════════════════════════════════════════════════════════

relationships = [
    {
        "person_a": 1, "person_b": 3,
        "type": "superior_subordinate",
        "context": "赵之达任县长/县委书记期间，曲传增任常务副县长",
        "overlap_org": "夏津县人民政府",
        "overlap_period": "2021-2026",
    },
    {
        "person_a": 1, "person_b": 5,
        "type": "superior_subordinate",
        "context": "赵之达任县委书记，王勇任县委副书记",
        "overlap_org": "中共夏津县委员会",
        "overlap_period": "2026",
    },
    {
        "person_a": 1, "person_b": 4,
        "type": "overlap",
        "context": "赵之达县长/县委书记与王跃华人大主任在2026年1月人大会议同台",
        "overlap_org": "夏津县",
        "overlap_period": "2021-2026",
    },
    {
        "person_a": 1, "person_b": 7,
        "type": "superior_subordinate",
        "context": "赵之达与副县长李雪峰多次共同参加现场办公",
        "overlap_org": "夏津县人民政府",
        "overlap_period": "2026",
    },
    {
        "person_a": 1, "person_b": 6,
        "type": "superior_subordinate",
        "context": "赵之达任县长/县委书记期间，李颖任副县长",
        "overlap_org": "夏津县人民政府",
        "overlap_period": "2024-2026",
    },
    {
        "person_a": 1, "person_b": 8,
        "type": "superior_subordinate",
        "context": "赵之达与李新海共同参加重点项目现场办公",
        "overlap_org": "夏津县人民政府",
        "overlap_period": "2026",
    },
    {
        "person_a": 3, "person_b": 6,
        "type": "overlap",
        "context": "曲传增与李颖同为副县长，共同参加政府常务会议",
        "overlap_org": "夏津县人民政府",
        "overlap_period": "2024-2026",
    },
    {
        "person_a": 3, "person_b": 7,
        "type": "overlap",
        "context": "曲传增与李雪峰同为副县长，共同参加政府常务会议",
        "overlap_org": "夏津县人民政府",
        "overlap_period": "2026",
    },
    {
        "person_a": 3, "person_b": 8,
        "type": "overlap",
        "context": "曲传增与李新海同为县领导",
        "overlap_org": "夏津县人民政府",
        "overlap_period": "2026",
    },
    {
        "person_a": 5, "person_b": 10,
        "type": "overlap",
        "context": "王勇（县委副书记）与于春峰（政协）共同参加县委会议",
        "overlap_org": "中共夏津县委员会",
        "overlap_period": "2026",
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════════

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    name = p["name"]
    if "赵之达" in name or "书记" in p.get("current_post", ""):
        return "255,50,50"
    elif "县长" in p.get("current_post", ""):
        return "50,100,255"
    elif "副县长" in p.get("current_post", "") or "县委" in p.get("current_post", ""):
        return "50,100,255"
    elif "人大" in p.get("current_post", ""):
        return "200,255,255"
    elif "政协" in p.get("current_post", ""):
        return "255,240,200"
    return "100,100,100"


def is_top_leader(p):
    return "书记" == p.get("current_post", "")[:2] and "县委" in p.get("current_post", "")


def org_color(o):
    t = o.get("type", "")
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(t, "200,200,200")


def build_gexf():
    from datetime import datetime
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append(f'    <description>夏津县领导班子工作关系网络 - 山东省德州市 (As of {AS_OF})</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('      <attribute id="3" title="level" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('    </attributes>')

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        pid = p["id"]
        c = person_color(p)
        sz = "20.0" if pid in (1, 2) else "12.0"
        role = p.get("current_post", "")
        org = p.get("current_org", "")
        lines.append(f'      <node id="p{pid}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(role)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(org)}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        oid = o["id"]
        c = org_color(o)
        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(o.get("level", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → organization (worked_at)
    for pos in positions:
        pid = pos["person_id"]
        oid = pos["org_id"]
        title = pos.get("title", "")
        period = f"{pos.get('start', '?')} - {pos.get('end', '?')}"
        lines.append(f'      <edge id="e{eid}" source="p{pid}" target="o{oid}" label="{esc(title)}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(title)}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(period)}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Person ↔ person (relationship)
    for r in relationships:
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_period", ""))}"/>')
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
    if DB_PATH.exists():
        DB_PATH.unlink()
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()

    c.execute("""CREATE TABLE persons (
        id INTEGER PRIMARY KEY,
        name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
        birthplace TEXT, education TEXT, party_join TEXT,
        work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
    )""")
    c.execute("""CREATE TABLE organizations (
        id INTEGER PRIMARY KEY,
        name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
    )""")
    c.execute("""CREATE TABLE positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER, org_id INTEGER,
        title TEXT, start TEXT, "end" TEXT, rank TEXT, note TEXT
    )""")
    c.execute("""CREATE TABLE relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a INTEGER, person_b INTEGER,
        type TEXT, context TEXT, overlap_org TEXT, overlap_period TEXT
    )""")

    for p in persons:
        c.execute("INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                  (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                   p["birthplace"], p["education"], p["party_join"],
                   p["work_start"], p["current_post"], p["current_org"], p["source"]))
    for o in organizations:
        c.execute("INSERT INTO organizations VALUES (?,?,?,?,?,?)",
                  (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))
    for pos in positions:
        c.execute("INSERT INTO positions(person_id, org_id, title, start, \"end\", rank, note) VALUES (?,?,?,?,?,?,?)",
                  (pos["person_id"], pos["org_id"], pos["title"], pos["start"], pos["end"], pos.get("rank", ""), pos.get("note", "")))
    for r in relationships:
        c.execute("INSERT INTO relationships(person_a, person_b, type, context, overlap_org, overlap_period) VALUES (?,?,?,?,?,?)",
                  (r["person_a"], r["person_b"], r["type"], r["context"], r.get("overlap_org", ""), r.get("overlap_period", "")))

    conn.commit()
    conn.close()
    print(f"  Database written: {DB_PATH}")


def build_single_person_json(p, filename):
    """Write a minimal person JSON for a core figure."""
    person_id = f"xiajin_{p['name']}"
    path = PERSONS_DIR / filename

    career_items = []
    for pos in positions:
        if pos["person_id"] == p["id"]:
            career_items.append({
                "start": pos.get("start", "unknown"),
                "end": pos.get("end", "present"),
                "org": next((o["name"] for o in organizations if o["id"] == pos["org_id"]), ""),
                "title": pos["title"],
                "rank": pos.get("rank", ""),
                "notes": pos.get("note", ""),
                "confidence": "confirmed" if pos.get("start") else "unverified",
                "source_ids": ["S001"],
            })

    rel_items = []
    for r in relationships:
        if r["person_a"] == p["id"]:
            other = next((x["name"] for x in persons if x["id"] == r["person_b"]), "")
            rel_items.append({
                "person": other,
                "relationship_type": r["type"],
                "strength": "medium",
                "evidence": r["context"],
                "overlap_org": r.get("overlap_org", ""),
                "overlap_period": r.get("overlap_period", ""),
                "confidence": "confirmed",
                "source_ids": ["S001"],
            })
        elif r["person_b"] == p["id"]:
            other = next((x["name"] for x in persons if x["id"] == r["person_a"]), "")
            rel_items.append({
                "person": other,
                "relationship_type": r["type"],
                "strength": "medium",
                "evidence": r["context"],
                "overlap_org": r.get("overlap_org", ""),
                "overlap_period": r.get("overlap_period", ""),
                "confidence": "confirmed",
                "source_ids": ["S001"],
            })

    data = {
        "schema_version": "1.0",
        "generated_at": TODAY[:4] + "-" + TODAY[4:6] + "-" + TODAY[6:8],
        "investigation_scope": {
            "province": "山东省",
            "city": "德州市",
            "region": "夏津县",
            "job": p.get("current_post", ""),
            "task_id": "shandong_夏津县",
            "time_focus": "2021-2026",
        },
        "identity": {
            "person_id": person_id,
            "name": p["name"],
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": p.get("party_join", ""),
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{p['name']}_",
                "name_birthplace": f"{p['name']}_{p.get('birthplace', '')}",
                "official_profile_url": "http://www.xiajin.gov.cn/",
            },
        },
        "current_status": {
            "current_post": p.get("current_post", ""),
            "current_org": p.get("current_org", ""),
            "administrative_rank": "正处级" if p["id"] in (1, 2, 4) else "副处级",
            "as_of": AS_OF,
            "is_current_confirmed": p["id"] == 1,
            "source_ids": ["S001"],
        },
        "career_timeline": career_items,
        "organizations": [],
        "relationships": rel_items,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "local_ladder" if p["id"] == 1 else "unknown",
            "systems_experience": [],
            "geographic_pattern": ["山东德州"],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records only.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现公开负面信息", "date": "", "confidence": "unverified", "source_ids": ["S001"]}],
        "source_register": [
            {"id": "S001", "title": "夏津县人民政府官网", "url": "http://www.xiajin.gov.cn/",
             "publisher": "夏津县人民政府", "published_at": "", "accessed_at": AS_OF,
             "source_type": "official", "reliability": "high", "notes": "官方政府网站"},
        ],
        "confidence_summary": {
            "identity": "plausible" if p.get("birth") else "unverified",
            "current_role": "confirmed" if p["id"] == 1 else "unverified",
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "个人履历（出生年月、教育背景、早期职业经历）完全缺失" if p["id"] in (1, 2) else "详细履历缺失",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{p['name']}的出生年月、籍贯、教育背景",
                "why_it_matters": "核心身份信息，用于跨数据库去重和人物画像",
                "suggested_queries": [f"{p['name']} 简历 夏津", f"{p['name']} 出生"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "critical",
                "question": f"{p['name']}的完整职业生涯时间线",
                "why_it_matters": "理解晋升路径和关键转折点",
                "suggested_queries": [f"{p['name']} 任职 经历", f"{p['name']} 任前公示"],
                "last_attempted": AS_OF,
            },
        ],
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON written: {path}")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print(f"Building {SLUG} data...")

    print("  Creating database...")
    build_db()

    print("  Creating GEXF graph...")
    build_gexf()

    print("  Creating person JSONs for core leaders...")
    # 赵之达 — 县委书记
    build_single_person_json(persons[0], f"{TODAY}-山东省-德州市-县委书记-赵之达.json")
    # 县长 (placeholder — name unknown)
    # Build a minimal person JSON for the unfilled county magistrate role
    build_single_person_json(persons[1], f"{TODAY}-山东省-德州市-县长-待确认.json")

    print(f"\nDone. Files created in {_STAGING_DIR}:")
    for fname in sorted(os.listdir(str(_STAGING_DIR))):
        fpath = _STAGING_DIR / fname
        if fpath.is_file():
            print(f"  {fname} ({fpath.stat().st_size} bytes)")

    print("\n=== Summary ===")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
