#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 友谊县 leadership network.

友谊县隶属黑龙江省双鸭山市，位于三江平原腹地，是国家重要的商品粮基地，
下辖友谊、兴隆、风岗等乡镇，境内有全国大型农场友谊农场（红兴隆管理局）。
县委、县政府负责全县党建、农业现代化、经济发展与社会建设等。

⚠️ 本脚本基于部分证据模式（Partial-Evidence Mode）：
- 本会话网络访问全面降级（Exa 速率限制 / Jina Reader 超时 / 政府官网 HTTP:000），
  无法现场核实现任县委书记、县长姓名。
- 现任县四大班子主要领导暂以"待查"占位，确保结构完整、缺口显式。
- 已确认的组织结构（中共友谊县委员会、友谊县人民政府、县人大、县政协、县纪委监监委、友谊县东建乡）
  来自县级四套班子结构 + 徐文韬官方履历（友谊县东建乡党委书记，见 build_四方台区_data.py）。

跨县干部交流确认证据（官方履历, confirmed）：
- 徐文韬（现任 双鸭山市四方台区委常委、副区长）曾任友谊县东建乡党委书记
  （2020.05–2021.07），体现"双鸭山市委组织部 → 友谊县乡镇 → 市政府办 → 区"交流路径。
"""

import os
import sqlite3  # noqa: F401
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve()
for _parent in REPO_ROOT.parents:
    if (_parent / "gov_relation").is_dir():
        REPO_ROOT = _parent
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "友谊县"

_STAGING = os.environ.get("STAGING_DIR")
if _STAGING:
    DB_PATH = os.path.join(_STAGING, "友谊县_network.db")
    GEXF_PATH = os.path.join(_STAGING, "友谊县_network.gexf")
else:
    DB_PATH = DATABASE_DIR / "友谊县_network.db"
    GEXF_PATH = GRAPH_DIR / "友谊县_network.gexf"

# ── ORGANIZATIONS ───────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共友谊县委员会", "type": "党委", "level": "县处级", "parent": "中共双鸭山市委", "location": "黑龙江省双鸭山市友谊县"},
    {"id": 2, "name": "友谊县人民政府", "type": "政府", "level": "县处级", "parent": "双鸭山市人民政府", "location": "黑龙江省双鸭山市友谊县"},
    {"id": 3, "name": "友谊县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "双鸭山市人大常委会", "location": "黑龙江省双鸭山市友谊县"},
    {"id": 4, "name": "中国人民政治协商会议友谊县委员会", "type": "政协", "level": "县处级", "parent": "双鸭山市政协", "location": "黑龙江省双鸭山市友谊县"},
    {"id": 5, "name": "中共友谊县纪律检查委员会/友谊县监察委员会", "type": "纪委", "level": "副县处级", "parent": "中共双鸭山市纪委", "location": "黑龙江省双鸭山市友谊县"},
    {"id": 6, "name": "中共友谊县委组织部", "type": "党委部门", "level": "正科级", "parent": "中共友谊县委", "location": "黑龙江省双鸭山市友谊县"},
    {"id": 7, "name": "友谊县东建乡", "type": "乡镇", "level": "正科级", "parent": "友谊县人民政府", "location": "黑龙江省双鸭山市友谊县东建乡"},
    {"id": 8, "name": "中共双鸭山市委", "type": "党委", "level": "地厅级", "parent": "", "location": "黑龙江省双鸭山市"},
    {"id": 9, "name": "双鸭山市人民政府", "type": "政府", "level": "地厅级", "parent": "", "location": "黑龙江省双鸭山市"},
]

# ── PERSONS ─────────────────────────────────────────────────────────
persons = [
    # 1 — 待查 — 县委书记（现任）
    {"id": 1, "name": "待查_县委书记", "gender": "", "ethnicity": "", "birth": "", "birthplace": "待查",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "中共友谊县委书记", "current_org": "中共友谊县委员会",
     "source": ""},
    # 2 — 待查 — 县委副书记、县长（现任）
    {"id": 2, "name": "待查_县长", "gender": "", "ethnicity": "", "birth": "", "birthplace": "待查",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "友谊县委副书记、县长、县政府党组书记", "current_org": "友谊县人民政府",
     "source": ""},
    # 3 — 待查 — 县人大常委会主任（现任）
    {"id": 3, "name": "待查_人大主任", "gender": "", "ethnicity": "", "birth": "", "birthplace": "待查",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "友谊县人大常委会主任", "current_org": "友谊县人民代表大会常务委员会",
     "source": ""},
    # 4 — 待查 — 县政协主席（现任）
    {"id": 4, "name": "待查_政协主席", "gender": "", "ethnicity": "", "birth": "", "birthplace": "待查",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "友谊县政协主席", "current_org": "中国人民政治协商会议友谊县委员会",
     "source": ""},
    # 5 — 徐文韬 — 双鸭山市委组织部研究室主任 / 曾任友谊县东建乡党委书记（confirmed 官方履历）
    {"id": 5, "name": "徐文韬", "gender": "男", "ethnicity": "汉族", "birth": "1986年9月", "birthplace": "待查",
     "education": "国家开放大学行政管理",
     "party_join": "2005年6月入党", "work_start": "2008年7月",
     "current_post": "双鸭山市四方台区委常委、副区长", "current_org": "四方台区人民政府",
     "source": "http://www.syssft.gov.cn/sft/283/202604/c07_246944.shtml"},
]

# ── POSITIONS ───────────────────────────────────────────────────────
positions = [
    # 待查_县委书记
    {"person_id": 1, "org_id": 1, "title": "中共友谊县委书记", "start": "unknown", "end": "present", "rank": "县处级正职", "note": "本会话网络降级，姓名及到任日期待官方来源确认"},
    # 待查_县长
    {"person_id": 2, "org_id": 2, "title": "友谊县委副书记、县长、县政府党组书记", "start": "unknown", "end": "present", "rank": "县处级正职", "note": "姓名待核实，待官方来源确认"},
    # 待查_人大主任
    {"person_id": 3, "org_id": 3, "title": "友谊县人大常委会主任", "start": "unknown", "end": "present", "rank": "县处级正职", "note": ""},
    # 待查_政协主席
    {"person_id": 4, "org_id": 4, "title": "友谊县政协主席", "start": "unknown", "end": "present", "rank": "县处级正职", "note": ""},
    # 徐文韬（友谊县东建乡党委书记 - confirmed）
    {"person_id": 5, "org_id": 7, "title": "友谊县东建乡党委书记", "start": "2020.05", "end": "2021.07", "rank": "正科级", "note": "官方履历确认（四方台区官网）"},
    {"person_id": 5, "org_id": 9, "title": "双鸭山市人民政府办公室副主任", "start": "2021.07", "end": "2025", "rank": "副处级", "note": "市政府办转任，后任四方台区委常委副区长"},
]

# ── RELATIONSHIPS (仅确认或结构性关系；均为班子成员关系或局际证据) ──
relationships = [
    # 县级四套班子（待查占位）内部结构关系
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "中共友谊县委书记与县委副书记、县长为党政一把手搭档，同一县级班子共事", "overlap_org": "友谊县", "overlap_period": "待核实"},
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "友谊县委书记与县人大常委会主任同台履职", "overlap_org": "友谊县", "overlap_period": "待核实"},
    {"person_a": 1, "person_b": 4, "type": "同场公职", "context": "友谊县委书记与县政协主席同台履职", "overlap_org": "友谊县", "overlap_period": "待核实"},
    {"person_a": 2, "person_b": 4, "type": "同场公职", "context": "友谊县长向县政协会议通报政府工作", "overlap_org": "友谊县", "overlap_period": "待核实"},
    # 徐文韬 —— 友谊县东建乡（confirmed 官方履历）：县→市→区 交流路径
    {"person_a": 5, "person_b": 1, "type": "县域共事", "context": "徐文韬曾任友谊县东建乡党委书记，属友谊县基层组织负责人，受县委领导", "overlap_org": "友谊县东建乡", "overlap_period": "2020.05-2021.07"},
]

if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print(f"Wrote DB: {DB_PATH}")
    print(f"Wrote GEXF: {GEXF_PATH}")
    print(f"Stats: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")