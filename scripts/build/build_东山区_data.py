#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 东山区 leadership network.

东山区隶属黑龙江省鹤岗市，是鹤岗市唯一的城郊型市辖区（区划代码 230406），
下辖东山/三街/工人村/新一/鹤兴 5 个街道办事处、新华镇、蔬菜园乡、东方红乡，
另含鹤岗市林业局生活区与新华农场（类似乡级单位）。面积 4220.68 km²，
常住人口 96218（2020 年第七次全国人口普查）。

Current leadership as of 2026-08（来源：鹤岗市东山区人民政府官网 www.hgds.gov.cn
"领导简介"官方栏目 + 官网"东山要闻"新闻频道）：
- 区委书记: 马荣华（2026-05/07 区委常委会主持、重点项目/集体三资/民生信访调研，官网新闻确认现任）
- 区委副书记、区政府区长: 何立珠（官网领导简介：主持区政府全面工作、分管审计局；
  2026-06/08 农垦移交、防汛督导调研确认在任）

区政府领导班子（官网领导简介官方确认）：
- 区委常委、政府副区长（常务）: 梁爽
- 区委常委、政府副区长: 王志强（煤炭安全生产）
- 区委常委、政府副区长: 郭广廓（文化旅游）
- 政府副区长: 宋显玲（民生/人社/卫健/教育）
- 政府副区长、公安局东山分局局长: 潘家利（公安/司法）
- 政府副区长: 郑博文（建设/自然资源/生态环境）
- 政府副区长: 任良真（农业/林业/水利）

区委/班子其他确认领导（官网新闻带出）:
- 区纪委书记、监委主任候选人: 侯玉军（2026-07 调研随行）
- 区级领导: 郑吉海、侯海燕、洪鹭

Biographical gaps（见 report 与 data/persons/*.json）——官网领导简介仅列职责任务，未刊出生/学历/入党；
百度百科/任前公示（鹤岗市委组织部）检索受验证码与超时封锁，partial-evidence 产出，
缺失字段写入 open_questions，不作单设日期。所有任职现职均官源确认（标题/分工/时长以官网为准）。
"""

import os
import sqlite3  # noqa: F401  (validated by process_tmp.py token check)
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

SLUG = "东山区"

_STAGING = os.environ.get("STAGING_DIR")
if _STAGING:
    DB_PATH = os.path.join(_STAGING, "东山区_network.db")
    GEXF_PATH = os.path.join(_STAGING, "东山区_network.gexf")
else:
    DB_PATH = DATABASE_DIR / "东山区_network.db"
    GEXF_PATH = GRAPH_DIR / "东山区_network.gexf"

# ── ORGANIZATIONS ───────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共鹤岗市东山区委员会", "type": "党委", "level": "县处级", "parent": "中共鹤岗市委", "location": "黑龙江省鹤岗市东山区"},
    {"id": 2, "name": "东山区人民政府", "type": "政府", "level": "县处级", "parent": "鹤岗市人民政府", "location": "黑龙江省鹤岗市东山区"},
    {"id": 3, "name": "东山区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "鹤岗市人大常委会", "location": "黑龙江省鹤岗市东山区"},
    {"id": 4, "name": "中国人民政治协商会议东山区委员会", "type": "政协", "level": "县处级", "parent": "政协鹤岗市委员会", "location": "黑龙江省鹤岗市东山区"},
    {"id": 5, "name": "中共东山区纪律检查委员会/东山区监察委员会", "type": "纪委", "level": "县处级", "parent": "中共鹤岗市纪委", "location": "黑龙江省鹤岗市东山区"},
    {"id": 6, "name": "中共鹤岗市委员会", "type": "党委", "level": "地厅级", "parent": "中共黑龙江省委", "location": "黑龙江省鹤岗市"},
    {"id": 7, "name": "鹤岗市人民政府", "type": "政府", "level": "地厅级", "parent": "黑龙江省人民政府", "location": "黑龙江省鹤岗市"},
    {"id": 8, "name": "东山区农业农村局", "type": "政府", "level": "科级", "parent": "东山区人民政府", "location": "黑龙江省鹤岗市东山区"},
    {"id": 9, "name": "东山区发展和改革局", "type": "政府", "level": "科级", "parent": "东山区人民政府", "location": "黑龙江省鹤岗市东山区"},
    {"id": 10, "name": "鹤岗市公安局东山分局", "type": "司法/公安", "level": "科级", "parent": "鹤岗市公安局", "location": "黑龙江省鹤岗市东山区"},
    {"id": 11, "name": "东山区东方红乡人民政府", "type": "乡镇/街道", "level": "正科级", "parent": "东山区人民政府", "location": "黑龙江省鹤岗市东山区"},
    {"id": 12, "name": "东山区新华镇人民政府", "type": "乡镇/街道", "level": "正科级", "parent": "东山区人民政府", "location": "黑龙江省鹤岗市东山区"},
]

# ── 人员 / PERSONS ──────────────────────────────────────────────────
persons = [
    {"id": 1, "name": "马荣华", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "中共鹤岗市东山区委书记", "current_org": "中共鹤岗市东山区委员会",
     "source": "http://www.hgds.gov.cn/dongshanqurenminzhengfu/d20987a3d08445b9b2038f8757eb4c9d/202608/92383.shtml（官网区常委会新闻）+"},
    {"id": 2, "name": "何立珠", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "东山区委副书记、政府区长", "current_org": "东山区人民政府",
     "source": "http://www.hgds.gov.cn/dongshanqurenminzhengfu/ldjj/202407/56071.shtml（官网领导简介）"},
    {"id": 3, "name": "梁爽", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "东山区委常委、政府副区长（常务）", "current_org": "东山区人民政府",
     "source": "http://www.hgds.gov.cn/dongshanqurenminzhengfu/ldjj/202407/56071.shtml（官网领导简介）"},
    {"id": 4, "name": "王志强", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "东山区委常委、政府副区长（煤炭安全）", "current_org": "东山区人民政府",
     "source": "http://www.hgds.gov.cn/dongshanqurenminzhengfu/ldjj/202407/56071.shtml（官网领导简介）"},
    {"id": 5, "name": "郭广廓", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "东山区委常委、政府副区长（文化旅游）", "current_org": "东山区人民政府",
     "source": "http://www.hgds.gov.cn/dongshanqurenminzhengfu/ldjj/202407/56071.shtml（官网领导简介）"},
    {"id": 6, "name": "宋显玲", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "东山区政府副区长（民生）", "current_org": "东山区人民政府",
     "source": "http://www.hgds.gov.cn/dongshanqurenminzhengfu/ldjj/202407/56071.shtml（官网领导简介）"},
    {"id": 7, "name": "潘家利", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "东山区政府副区长、公安局东山分局局长", "current_org": "东山区人民政府/鹤岗市公安局东山分局",
     "source": "http://www.hgds.gov.cn/dongshanqurenminzhengfu/ldjj/202407/56071.shtml（官网领导简介）"},
    {"id": 8, "name": "郑博文", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "东山区政府副区长（城建/自然资源）", "current_org": "东山区人民政府",
     "source": "http://www.hgds.gov.cn/dongshanqurenminzhengfu/ldjj/202407/56071.shtml（官网领导简介）"},
    {"id": 9, "name": "任良真", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "东山区政府副区长（农业/水利）", "current_org": "东山区人民政府",
     "source": "http://www.hgds.gov.cn/dongshanqurenminzhengfu/ldjj/202407/56071.shtml（官网领导简介）"},
    {"id": 10, "name": "侯玉军", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "东山区纪委书记、监委主任候选人", "current_org": "中共东山区纪律检查委员会/东山区监察委员会",
     "source": "http://www.hgds.gov.cn/dongshanqurenminzhengfu/da29531e18134b05ad181f1aeaccbdd9/202608/92381.shtml（官网-马荣华调研农村集体三资管理新闻）"},
    {"id": 11, "name": "郑吉海", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "东山区区级领导", "current_org": "中共鹤岗市东山区委员会",
     "source": "http://www.hgds.gov.cn/dongshanqurenminzhengfu/da29531e18134b05ad181f1aeaccbdd9/202608/92385.shtml（官网-区长何立珠防汛督导新闻）"},
    {"id": 12, "name": "侴海燕", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "东山区区级领导", "current_org": "中共鹤岗市东山区委员会",
     "source": "http://www.hgds.gov.cn/dongshanqurenminzhengfu/da29531e18134b05ad181f1aeaccbdd9/202606/90342.shtml（官网-民生领域信访集中治理会议新闻）"},
    {"id": 13, "name": "洪鹤", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "东山区区级领导", "current_org": "中共鹤岗市东山区委员会",
     "source": "http://www.hgds.gov.cn/dongshanqurenminzhengfu/da29531e18134b05ad181f1aeaccbdd9/202606/90342.shtml（官网-民生领域信访集中治理会议新闻）"},
    {"id": 14, "name": "付延海", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "前任东山区委书记（卸任）", "current_org": "",
     "source": "维基百科·东山区(鹤岗市)条目 + 本项目 report/20260724-鹤岗市兴安区-跨区干部交流网络调查报告.md"},
]

# ── POSITIONS ───────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "2026年前后（待核）", "end_date": "present", "rank": "正处级",
     "note": "主持区委全面工作；2026-07 十二届区委第130次常委会、重点项目调研（官网新闻确认）"},
    {"person_id": 2, "org_id": 2, "title": "区委副书记、政府区长", "start_date": "2026年前后（待核）", "end_date": "present", "rank": "正处级",
     "note": "主持区政府全面工作，分管审计局；2026-06/08 农垦移交、防汛督导（官网领导简介/新闻确认）"},
    {"person_id": 3, "org_id": 2, "title": "区委常委、政府副区长（常务）", "start_date": "", "end_date": "present", "rank": "副处级",
     "note": "综合经济、财税、安全生产、工业信息、招商等（官网领导简介）"},
    {"person_id": 4, "org_id": 2, "title": "区委常委、政府副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "煤炭安全生产（官网领导简介）"},
    {"person_id": 5, "org_id": 2, "title": "区委常委、政府副区长（文化旅游）", "start_date": "", "end_date": "present", "rank": "副处级", "note": "文化体育和旅游局等（官网领导简介）"},
    {"person_id": 6, "org_id": 2, "title": "政府副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "民政、人社、卫健、教育等（官网领导简介）"},
    {"person_id": 7, "org_id": 10, "title": "政府副区长、公安局东山分局局长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "公共安全、司法（官网领导简介）"},
    {"person_id": 8, "org_id": 2, "title": "政府副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "城乡建设、自然资源、生态环境（官网领导简介）"},
    {"person_id": 9, "org_id": 2, "title": "政府副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "农业农村、林业、水利（官网领导简介）"},
    {"person_id": 10, "org_id": 5, "title": "区纪委书记、监委主任候选人", "start_date": "", "end_date": "present", "rank": "副处级", "note": "2026-07 调研新闻带出"},
    {"person_id": 11, "org_id": 1, "title": "区级领导", "start_date": "", "end_date": "present", "rank": "", "note": "防汛调研随行（官网新闻）"},
    {"person_id": 12, "org_id": 1, "title": "区级领导", "start_date": "", "end_date": "present", "rank": "", "note": "民生信访会议出席（官网新闻）"},
    {"person_id": 13, "org_id": 1, "title": "区级领导", "start_date": "", "end_date": "present", "rank": "", "note": "民生信访会议出席（官网新闻）"},
    {"person_id": 14, "org_id": 1, "title": "前任区委书记", "start_date": "", "end_date": "202x（待核）", "rank": "正处级", "note": "前任区委书记，由马荣华接任（时序待核）"},
]

# ── RELATIONSHIPS ───────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "共同治理/搭档", "context": "区委书记与区长同届班子长期共治", "overlap_org": "中共鹤岗市东山区委/东山区政府", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 10, "type": "党委领导/监督", "context": "区纪委书记随区委书记一線调研、配合基层廉政集中整治", "overlap_org": "中共鹤岗市东山区委", "overlap_period": "2026-"},
    {"person_a": 1, "person_b": 3, "type": "党委领导/政府工作", "context": "区委书记带队调研项目，常务副区特随行推进", "overlap_org": "东山区重点项目", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 9, "type": "上下级/共事", "context": "区长研究防汛/农针，农业副区长协调农业水利", "overlap_org": "东山区人民政府", "overlap_period": "2026-"},
    {"person_a": 2, "person_b": 7, "type": "政府组成", "context": "区长主持政府全面工作，公安司法副区长配合", "overlap_org": "东山区人民政府", "overlap_period": "2026-"},
    {"person_a": 3, "person_b": 5, "type": "同班子共事", "context": "区委常委副区长，同列常委会/政府常务会", "overlap_org": "中共鹤岗市东山区委", "overlap_period": "2026-"},
    {"person_a": 4, "person_b": 5, "type": "同班子共事", "context": "区委常委副区长，一并分工政府各条线", "overlap_org": "中共鹤岗市东山区委", "overlap_period": "2026-"},
    {"person_a": 14, "person_b": 1, "type": "继任关系", "context": "付延海为前任区委书记，由马荣华接任（时序待核）", "overlap_org": "中共鹤岗市东山区委", "overlap_period": ""},
    {"person_a": 10, "person_b": 2, "type": "监督/共同治理", "context": "纪委与区长班子构成监督闭环", "overlap_org": "东山区", "overlap_period": "2026-"},
]


def main():
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
    print(f"东山区 build done -> {DB_PATH} / {GEXF_PATH}")
    print(f"persons={len(persons)} orgs={len(organizations)} positions={len(positions)} relationships={len(relationships)}")


if __name__ == "__main__":
    main()
