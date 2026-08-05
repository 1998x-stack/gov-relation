#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 金秀瑶族自治县 leadership network.

金秀瑶族自治县隶属广西壮族自治区来宾市，地处广西桂中大瑶山腹地，是著名的"世界瑶都"，
全国瑶族人口最集中的县之一，国家重点生态功能区。

Current leadership as of 2026-08（官方确认，来源见 report 与 person JSON）：
- 县委书记：覃健（2026-07 中共金秀县第16次代表大会作报告，2026-07-29 主持县委常委会）
- 县委副书记、县长：欧树和（男 瑶族 1978年9月生 中共党员 在职研究生学历，县政府党组书记、县长）

县委常委会（2026-07 党代会主席台前排名单）：覃健、欧树和、覃双顶、魏海松、赵德乾、秦龙珍、
段祚勇、曹方、赵团、田润娟、宋文杰。

县政府班子（官方"领导之窗"确认）：县长 欧树和；副县长 彭飞、何林国、邓华（挂职自治区生态环境厅）、
赵德乾、覃富荣（兼公安局长）、覃玲玲、梁永帅（挂职广东茂名电白）。

个别人员出生/民族/学历字段缺公开档案资料，置空并记入 open_gaps
（见 report/open_gaps.md 与 person JSON open_questions）。
数据主要来源：金秀县人民政府门户网站 www.jinxiu.gov.cn（领导之窗、金秀要闻、党代会报道）。
"""
import os
import sqlite3
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

SLUG = "金秀瑶族自治县"

STAGING = os.environ.get("STAGING_DIR")
if STAGING:
    DB_PATH = os.path.join(STAGING, "金秀瑶族自治县_network.db")
    GEXF_PATH = os.path.join(STAGING, "金秀瑶族自治县_network.gexf")
else:
    DB_PATH = DATABASE_DIR / "金秀瑶族自治县_network.db"
    GEXF_PATH = GRAPH_DIR / "金秀瑶族自治县_network.gexf"

# ── ORGANIZATIONS ───────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共金秀瑶族自治县委员会", "type": "党委", "level": "县处级", "parent": "中共来宾市委", "location": "广西壮族自治区来宾市金秀瑶族自治县"},
    {"id": 2, "name": "金秀瑶族自治县人民政府", "type": "政府", "level": "县处级", "parent": "来宾市人民政府", "location": "广西壮族自治区来宾市金秀瑶族自治县"},
    {"id": 3, "name": "金秀瑶族自治县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "来宾市人大常委会", "location": "广西壮族自治区来宾市金秀瑶族自治县"},
    {"id": 4, "name": "中国人民政治协商会议金秀瑶族自治县委员会", "type": "政协", "level": "县处级", "parent": "政协来宾市委员会", "location": "广西壮族自治区来宾市金秀瑶族自治县"},
    {"id": 5, "name": "中共金秀瑶族自治县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共来宾市纪委", "location": "广西壮族自治区来宾市金秀瑶族自治县"},
    {"id": 6, "name": "中共来宾市委员会", "type": "党委", "level": "地厅级", "parent": "中共广西壮族自治区委员会", "location": "广西壮族自治区来宾市"},
    {"id": 7, "name": "来宾市人民政府", "type": "政府", "level": "地厅级", "parent": "广西壮族自治区人民政府", "location": "广西壮族自治区来宾市"},
    {"id": 8, "name": "金秀瑶族自治县公安局", "type": "政府", "level": "县处级", "parent": "来宾市公安局", "location": "广西壮族自治区来宾市金秀瑶族自治县"},
    {"id": 9, "name": "广西壮族自治区生态环境厅", "type": "政府", "level": "省部级", "parent": "广西壮族自治区人民政府", "location": "广西壮族自治区南宁市"},
    {"id": 10, "name": "广东省茂名市电白区人民政府", "type": "政府", "level": "县处级", "parent": "茂名市人民政府", "location": "广东省茂名市电白区"},
    {"id": 11, "name": "金秀瑶族自治县委政法委", "type": "党委部门", "level": "县处级", "parent": "中共金秀瑶族自治县委员会", "location": "广西壮族自治区来宾市金秀瑶族自治县"},
]

# ── PERSONS ─────────────────────────────────────────────────────────
persons = [
    # 1 覃健 — 县委书记
    {"id": 1, "name": "覃健", "gender": "男", "ethnicity": "壮族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "中共金秀瑶族自治县委书记", "current_org": "中共金秀瑶族自治县委员会",
     "source": "http://www.jinxiu.gov.cn/zwdt/jxyw/2026jxyw/t27967076.shtml"},
    # 2 欧树和 — 县长
    {"id": 2, "name": "欧树和", "gender": "男", "ethnicity": "瑶族", "birth": "1978年9月", "birthplace": "",
     "education": "在职研究生学历", "party_join": "中共党员", "work_start": "",
     "current_post": "金秀自治县委副书记、县政府党组书记、县长", "current_org": "金秀瑶族自治县人民政府",
     "source": "http://www.jinxiu.gov.cn/xxgk/zfxxgk/fdzdgknr/ldjj/xz/"},
    # 3 覃双顶 — 县委副书记
    {"id": 3, "name": "覃双顶", "gender": "男", "ethnicity": "壮族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "中共金秀瑶族自治县委副书记", "current_org": "中共金秀瑶族自治县委员会",
     "source": "http://www.jinxiu.gov.cn/zwdt/jxyw/2026jxyw/t27967076.shtml"},
    # 4 魏海松 — 县委常委
    {"id": 4, "name": "魏海松", "gender": "男", "ethnicity": "壮族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "中共金秀瑶族自治县委常委", "current_org": "中共金秀瑶族自治县委员会",
     "source": "http://www.jinxiu.gov.cn/zwdt/jxyw/2026jxyw/t27967076.shtml"},
    # 5 赵德乾 — 县委常委、副县长
    {"id": 5, "name": "赵德乾", "gender": "男", "ethnicity": "瑶族", "birth": "1977年11月", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "中共金秀瑶族自治县委常委、县人民政府党组成员、副县长", "current_org": "金秀瑶族自治县人民政府",
     "source": "http://www.jinxiu.gov.cn/xxgk/zfxxgk/fdzdgknr/ldjj/fxz/t16877477.shtml"},
    # 6 秦龙珍 — 县委常委
    {"id": 6, "name": "秦龙珍", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "中共金秀瑶族自治县委常委", "current_org": "中共金秀瑶族自治县委员会",
     "source": "http://www.jinxiu.gov.cn/zwdt/jxyw/2026jxyw/t27967076.shtml"},
    # 7 段柞勇 — 县委常委
    {"id": 7, "name": "段祚勇", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "中共金秀瑶族自治县委常委", "current_org": "中共金秀瑶族自治县委员会",
     "source": "http://www.jinxiu.gov.cn/zwdt/jxyw/2026jxyw/t27967076.shtml"},
    # 8 曹公 — 县委常委
    {"id": 8, "name": "曹方", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "中共金秀瑶族自治县委常委", "current_org": "中共金秀瑶族自治县委员会",
     "source": "http://www.jinxiu.gov.cn/zwdt/jxyw/2026jxyw/t27967076.shtml"},
    # 9 赵勇 — 县委常委
    {"id": 9, "name": "赵团", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "中共金秀瑶族自治县委常委", "current_org": "中共金秀瑶族自治县委员会",
     "source": "http://www.jinxiu.gov.cn/zwdt/jxyw/2026jxyw/t27967076.shtml"},
    # 10 田润娟 — 县委常委
    {"id": 10, "name": "田润娟", "gender": "女", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "中共金秀瑶族自治县委常委", "current_org": "中共金秀瑶族自治县委员会",
     "source": "http://www.jinxiu.gov.cn/zwdt/jxyw/2026jxyw/t27967076.shtml"},
    # 11 宋文杰 — 县委常委
    {"id": 11, "name": "宋文杰", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "中共金秀瑶族自治县委常委", "current_org": "中共金秀瑶族自治县委员会",
     "source": "http://www.jinxiu.gov.cn/zwdt/jxyw/2026jxyw/t27967076.shtml"},
    # 12 彭飞 — 县委常委、副县长
    {"id": 12, "name": "彭飞", "gender": "男", "ethnicity": "蒙古族", "birth": "1987年2月", "birthplace": "",
     "education": "研究生学历", "party_join": "中共党员", "work_start": "",
     "current_post": "金秀瑶族自治县委常委、县政府党组成员、副县长", "current_org": "金秀瑶族自治县人民政府",
     "source": "http://www.jinxiu.gov.cn/xxgk/zfxxgk/fdzdgknr/ldjj/fxz/t18294462.shtml"},
    # 13 何林国 — 县委常委、副县长
    {"id": 13, "name": "何林国", "gender": "男", "ethnicity": "汉族", "birth": "1975年12月", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "金秀瑶族自治县委常委、县政府党组成员、副县长", "current_org": "金秀瑶族自治县人民政府",
     "source": "http://www.jinxiu.gov.cn/xxgk/zfxxgk/fdzdgknr/ldjj/fxz/t18490095.shtml"},
    # 14 邓华 — 副县长（挂职）
    {"id": 14, "name": "邓华", "gender": "男", "ethnicity": "壮族", "birth": "1981年4月", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "金秀瑶族自治县人民政府副县长（挂职，自治区生态环境厅环评处二级调研员）", "current_org": "金秀瑶族自治县人民政府",
     "source": "http://www.jinxiu.gov.cn/xxgk/zfxxgk/fdzdgknr/ldjj/fxz/t611764.shtml"},
    # 15 覃富荣 — 副县长、公安局长
    {"id": 15, "name": "覃富荣", "gender": "男", "ethnicity": "汉族", "birth": "1979年8月", "birthplace": "",
     "education": "在职研究生学历", "party_join": "中共党员", "work_start": "",
     "current_post": "金秀瑶族自治县政府党组成员、副县长，公安局党委书记、局长、督察长", "current_org": "金秀瑶族自治县人民政府",
     "source": "http://www.jinxiu.gov.cn/xxgk/zfxxgk/fdzdgknr/ldjj/fxz/t16877481.shtml"},
    # 16 覃玲玲 — 副县长
    {"id": 16, "name": "覃玲玲", "gender": "女", "ethnicity": "壮族", "birth": "1983年8月", "birthplace": "",
     "education": "大学本科学历", "party_join": "中共党员", "work_start": "",
     "current_post": "金秀瑶族自治县人民政府副县长", "current_org": "金秀瑶族自治县人民政府",
     "source": "http://www.jinxiu.gov.cn/xxgk/zfxxgk/fdzdgknr/ldjj/fxz/t17981188.shtml"},
    # 17 梁永帅 — 副县长（挂职广东）
    {"id": 17, "name": "梁永帅", "gender": "男", "ethnicity": "壮族", "birth": "1981年9月", "birthplace": "",
     "education": "大学本科学历", "party_join": "中共党员", "work_start": "",
     "current_post": "金秀瑶族自治县政府党组成员、副县长（到广东茂名市电白区挂职）", "current_org": "金秀瑶族自治县人民政府",
     "source": "http://www.jinxiu.gov.cn/xxgk/zfxxgk/fdzdgknr/ldjj/fxz/t17981162.shtml"},
]

# ── POSITIONS ───────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "中共金秀瑶族自治县委书记", "start": "2026", "end": "present", "rank": "正处级", "note": "2026-07 党代会作报告，主持县委常委会"},
    {"person_id": 2, "org_id": 2, "title": "金秀瑶族自治县委副书记、县长、政府党组书记", "start": "", "end": "present", "rank": "正处级", "note": "负责县政府全面工作、财政审计"},
    {"person_id": 3, "org_id": 1, "title": "中共金秀瑶族自治县委副书记", "start": "", "end": "present", "rank": "副处级", "note": "第16次党代会致开幕词"},
    {"person_id": 4, "org_id": 1, "title": "中共金秀瑶族自治县委常委", "start": "", "end": "present", "rank": "副处级", "note": "党代会主席台名单"},
    {"person_id": 5, "org_id": 1, "title": "金秀瑶族自治县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "金秀瑶族自治县人民政府副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "中共金秀瑶族自治县委常委", "start": "", "end": "present", "rank": "副处级", "note": "党代会主席台名单"},
    {"person_id": 7, "org_id": 1, "title": "中共金秀瑶族自治县委常委", "start": "", "end": "present", "rank": "副处级", "note": "党代会主席台名单"},
    {"person_id": 8, "org_id": 1, "title": "中共金秀瑶族自治县委常委", "start": "", "end": "present", "rank": "副处级", "note": "党代会主席台名单"},
    {"person_id": 9, "org_id": 1, "title": "中共金秀瑶族自治县委常委", "start": "", "end": "present", "rank": "副处级", "note": "党代会主席台名单"},
    {"person_id": 10, "org_id": 1, "title": "中共金秀瑶族自治县委常委", "start": "", "end": "present", "rank": "副处级", "note": "党代会主席台名单"},
    {"person_id": 11, "org_id": 1, "title": "中共金秀瑶族自治县委常委", "start": "", "end": "present", "rank": "副处级", "note": "党代会主席台名单"},
    {"person_id": 12, "org_id": 1, "title": "金秀瑶族自治县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "金秀瑶族自治县人民政府副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 1, "title": "金秀瑶族自治县委常委", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "金秀瑶族自治县人民政府副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "金秀瑶族自治县副县长（挂职）", "start": "", "end": "present", "rank": "副处级", "note": "自治区生态环境厅挂任"},
    {"person_id": 15, "org_id": 2, "title": "金秀瑶族自治县人民政府副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 15, "org_id": 8, "title": "金秀瑶族自治县公安局党委书记、局长、督察长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "金秀瑶族自治县人民政府副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "金秀瑶族自治县人民政府副县长", "start": "", "end": "present", "rank": "副处级", "note": "广东茂名电白挂职"},
]

# ── RELATIONSHIPS ───────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "覃健（县委书记）与欧树和（县长）为金秀县现任党政主要负责人，同一县委班子", "overlap_org": "金秀瑶族自治县", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "覃健任书记，覃双顶任县委副书记", "overlap_org": "中共金秀县委", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "覃健书记与县委常委、副县长赵德乾共事", "overlap_org": "金秀县委", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 12, "type": "上下级", "context": "覃健书记与县委常委、副县长彭飞共事", "overlap_org": "金秀县委", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 13, "type": "上下级", "context": "覃健书记与县委常委、副县长何林国共事", "overlap_org": "金秀县委", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 15, "type": "上下级", "context": "覃健书记与副县长、公安局长覃富荣共事", "overlap_org": "金秀县委/政法", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "欧树和县长与副县长赵德乾共事", "overlap_org": "金秀县人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "欧树和县长与副县长彭飞共事", "overlap_org": "金秀县人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 14, "type": "上下级", "context": "欧树和县长与挂职副县长邓华共事", "overlap_org": "金秀县人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 15, "type": "上下级", "context": "欧树和县长与副县长覃富荣共事", "overlap_org": "金秀县人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 16, "type": "上下级", "context": "欧树和县长与副县长覃玲玲共事", "overlap_org": "金秀县人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 17, "type": "上下级", "context": "欧树和县长与副县长梁永帅共事", "overlap_org": "金秀县人民政府", "overlap_period": "现任"},
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

    conn = sqlite3.connect(DB_PATH)
    tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
    conn.close()
    required = {"persons", "organizations", "positions", "relationships"}
    assert required.issubset(tables), f"missing tables: {required - tables}"
    print(f"DB verification OK: tables {sorted(required)} present")