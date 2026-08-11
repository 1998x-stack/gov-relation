#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 象州县 leadership network.

象州县隶属广西壮族自治区来宾市，位于广西中部、大瑶山南麓，地处柳江中上游，西汉置县，
是来宾市辖内重要县份。经济以制糖、木材加工、新能源材料（碳酸钙/硅基）、现代农业、文旅为主，
正建设"三区三地"、打造"产业盛、开放活、城乡美、百姓富、生态优、治理强"现代化新象州。

Current leadership as of 2026-08 (sources: 象州县人民政府门户网站 www.xiangzhou.gov.cn 官方任免/要闻):
- 县委书记: 罗威（2025-09-08 全县领导干部会议宣布，自治区党委任命；2026-07-30 中共象州县第十四届委员会第一次全体会议再次当选，连任）
- 县委副书记、县长: 梁建标（2024-02-23 象州县第十八届人大四次会议补选为县长，至今在任）

县委书记更替：张东（约2022-2025-09，任象州县委书记并宣导象州十四五；于2025-09-08 调离）→ 罗威（2025-09-08-今）。

Biographical/identity details for some individuals are unknown (罗威的出生/籍贯/调入前职务, 梁建标出生/籍贯).
These are encoded as open gaps (report/open_gaps.md) rather than fabricated. Confidence per person in report.
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

SLUG = "象州县"

_STAGING = os.environ.get("STAGING_DIR")
if _STAGING:
    DB_PATH = os.path.join(_STAGING, "象州县_network.db")
    GEXF_PATH = os.path.join(_STAGING, "象州县_network.gexf")
else:
    DB_PATH = DATABASE_DIR / "象州县_network.db"
    GEXF_PATH = GRAPH_DIR / "象州县_network.gexf"

# ── ORGANIZATIONS ───────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共象州县委员会", "type": "党委", "level": "县处级", "parent": "中共来宾市委", "location": "广西壮族自治区来宾市象州县"},
    {"id": 2, "name": "象州县人民政府", "type": "政府", "level": "县处级", "parent": "来宾市人民政府", "location": "广西壮族自治区来宾市象州县"},
    {"id": 3, "name": "象州县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "来宾市人大常委会", "location": "广西壮族自治区来宾市象州县"},
    {"id": 4, "name": "中国人民政治协商会议象州县委员会", "type": "政协", "level": "县处级", "parent": "政协来宾市委员会", "location": "广西壮族自治区来宾市象州县"},
    {"id": 5, "name": "中共象州县纪律检查委员会/象州县监察委员会", "type": "纪委", "level": "县处级", "parent": "中共来宾市纪委", "location": "广西壮族自治区来宾市象州县"},
    {"id": 6, "name": "中共来宾市委员会", "type": "党委", "level": "地厅级", "parent": "中共广西壮族自治区委员会", "location": "广西壮族自治区来宾市"},
    {"id": 7, "name": "来宾市人民代表大会常务委员会", "type": "人大", "level": "地厅级", "parent": "广西壮族自治区人大常委会", "location": "广西壮族自治区来宾市"},
    {"id": 8, "name": "中共广西壮族自治区委员会", "type": "党委", "level": "省部级", "parent": "中国共产党中央委员会", "location": "广西壮族自治区南宁市"},
    {"id": 9, "name": "中共来宾市委组织部", "type": "党委部门", "level": "地厅级", "parent": "中共来宾市委", "location": "广西壮族自治区来宾市"},
    {"id": 10, "name": "来宾市人民政府", "type": "政府", "level": "地厅级", "parent": "广西壮族自治区人民政府", "location": "广西壮族自治区来宾市"},
    {"id": 11, "name": "广西桂中（来宾）所辖县区（武宣、忻城、金秀、合山、兴宾等）", "type": "党委", "level": "县处级", "parent": "中共来宾市委", "location": "广西壮族自治区来宾市"},
]

# ── PERSONS ─────────────────────────────────────────────────────────
persons = [
    # 1 — 罗威 — 县委书记（现任，2025-09-08 任）
    {"id": 1, "name": "罗威", "gender": "",
     "ethnicity": "", "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共象州县委书记", "current_org": "中共象州县委员会",
     "source": "http://www.xiangzhou.gov.cn/zwdt/xzyw/t25948008.shtml"},
    # 2 — 梁建标 — 县长（现任，2024-02-23 当选）
    {"id": 2, "name": "梁建标", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "象州县委副书记、县长", "current_org": "象州县人民政府",
     "source": "http://www.xiangzhou.gov.cn/zwdt/xzyw/t18000248.shtml"},
    # 3 — 张东 — 前任县委书记（约2022-2025-09）
    {"id": 3, "name": "张东", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "象州县原县委书记（2025-09 调离）", "current_org": "中共象州县委员会",
     "source": "http://www.xiangzhou.gov.cn/zwdt/xzyw/index_6.shtml"},
    # 4 — 黄彩波 — 县领导（县委班子主要成员/人大主任，2024-02 起四家班子重要成员）
    {"id": 4, "name": "黄彩波", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "象州县四家班子主要成员（县委/人大）", "current_org": "象州县人民代表大会常务委员会",
     "source": "http://www.xiangzhou.gov.cn/zwdt/xzyw/t18000248.shtml"},
    # 5 — 袁永利 — 县四家班子领导
    {"id": 5, "name": "袁永利", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "象州县四家班子领导（县委副书记）", "current_org": "中共象州县委员会",
     "source": "http://www.xiangzhou.gov.cn/zwdt/xzyw/t25948008.shtml"},
    # 6 — 石宝璠 — 县四家班子领导
    {"id": 6, "name": "石宝璠", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "象州县四家班子领导", "current_org": "象州县人民政府",
     "source": "http://www.xiangzhou.gov.cn/zwdt/xzyw/t25948008.shtml"},
    # 7 — 罗昌勇 — 县四家班子领导
    {"id": 7, "name": "罗昌勇", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "象州县四家班子领导", "current_org": "象州县人民政府",
     "source": "http://www.xiangzhou.gov.cn/zwdt/xzyw/t25948008.shtml"},
    # 8 — 方杰 — 县四家班子领导
    {"id": 8, "name": "方杰", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "象州县四家班子领导", "current_org": "象州县人民政府",
     "source": "http://www.xiangzhou.gov.cn/zwdt/xzyw/t25948008.shtml"},
    # 9 — 曹捷 — 县四家班子领导
    {"id": 9, "name": "曹捷", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "象州县四家班子领导", "current_org": "象州县人民代表大会常务委员会",
     "source": "http://www.xiangzhou.gov.cn/zwdt/xzyw/t25948008.shtml"},
    # 10 — 谢永宁 — 县四家班子领导
    {"id": 10, "name": "谢永宁", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "象州县四家班子领导", "current_org": "象州县人民政府",
     "source": "http://www.xiangzhou.gov.cn/zwdt/xzyw/t25948008.shtml"},
    # 11 — 梁敏 — 县政府领导（副县长）
    {"id": 11, "name": "梁敏", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "象州县副处级领导", "current_org": "象州县人民政府",
     "source": "http://www.xiangzhou.gov.cn/zwdt/xzyw/t25948008.shtml"},
    # 12 — 韦茜 — 副县长
    {"id": 12, "name": "韦茜", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "象州县人民政府副县长", "current_org": "象州县人民政府",
     "source": "http://www.xiangzhou.gov.cn/zfxxgk/fdzdgknr/ldjj/"},
    # 13 — 黎裕宁 — 副县长，同时系县领导
    {"id": 13, "name": "黎裕宁", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "象州县人民政府副县长", "current_org": "象州县人民政府",
     "source": "http://www.xiangzhou.gov.cn/zfxxgk/fdzdgknr/ldjj/"},
    # 14 — 陈锋 — 副县长
    {"id": 14, "name": "陈锋", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "象州县人民政府副县长", "current_org": "象州县人民政府",
     "source": "http://www.xiangzhou.gov.cn/zfxxgk/fdzdgknr/ldjj/"},
    # 15 — 覃会雅 — 副县长
    {"id": 15, "name": "覃会雅", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "象州县人民政府副县长", "current_org": "象州县人民政府",
     "source": "http://www.xiangzhou.gov.cn/zfxxgk/fdzdgknr/ldjj/"},
    # 16 — 黄永君 — 副县长
    {"id": 16, "name": "黄永君", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "象州县人民政府副县长", "current_org": "象州县人民政府",
     "source": "http://www.xiangzhou.gov.cn/zfxxgk/fdzdgknr/ldjj/"},
    # 17 — 李耿 — 来宾市委组织部副部长（宣布任命）
    {"id": 17, "name": "李耿", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共来宾市委组织部副部长", "current_org": "中共来宾市委组织部",
     "source": "http://www.xiangzhou.gov.cn/zwdt/xzyw/t25948008.shtml"},
]

# ── POSITIONS ───────────────────────────────────────────────────────
positions = [
    # 罗威
    {"person_id": 1, "org_id": 1, "title": "象州县委书记", "start": "2025-09-08", "end": "present", "rank": "正处级", "note": "全区领导干部会议宣布，自治区党委任命；2026-07三十四届一次全会连任"},
    # 梁建标
    {"person_id": 2, "org_id": 2, "title": "象州县人民政府县长", "start": "2024-02-23", "end": "present", "rank": "正处级", "note": "象州县十八届人大五次会议补选当选"},
    {"person_id": 2, "org_id": 1, "title": "象州县委副书记", "start": "2024", "end": "present", "rank": "副处级", "note": "县委副书记、县长"},
    # 张东
    {"person_id": 3, "org_id": 1, "title": "象州县委书记", "start": "2022", "end": "2025-09-08", "rank": "正处级", "note": "2025-09-08 全区领导干部会议后调离"},
    # 黄彩波
    {"person_id": 4, "org_id": 3, "title": "象州县人大常委会主要职务/县领导", "start": "", "end": "present", "rank": "正处级", "note": "县四家班子主要成员（2024 党代会/人大负责人）"},
    # 袁永利
    {"person_id": 5, "org_id": 1, "title": "象州县委副书记", "start": "", "end": "present", "rank": "副处级", "note": "县四家班子领导"},
    # 石宝璠
    {"person_id": 6, "org_id": 2, "title": "县政府领导", "start": "", "end": "present", "rank": "副处级", "note": "县四家班子领导"},
    # 罗昌勇
    {"person_id": 7, "org_id": 2, "title": "县政府领导", "start": "", "end": "present", "rank": "副处级", "note": "县四家班子领导"},
    # 方杰
    {"person_id": 8, "org_id": 2, "title": "县政府领导", "start": "", "end": "present", "rank": "副处级", "note": "县四家班子领导"},
    # 曹捷
    {"person_id": 9, "org_id": 3, "title": "县人大领导", "start": "", "end": "present", "rank": "副处级", "note": "县四家班子领导"},
    # 谢永宁
    {"person_id": 10, "org_id": 2, "title": "县政府领导", "start": "", "end": "present", "rank": "副处级", "note": "县四家班子领导"},
    # 梁敏
    {"person_id": 11, "org_id": 2, "title": "县政府副县长", "start": "", "end": "present", "rank": "副处级", "note": "县四家班子领导"},
    # 韦茜
    {"person_id": 12, "org_id": 2, "title": "象州县人民政府副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 黎裕宁
    {"person_id": 13, "org_id": 2, "title": "象州县人民政府副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 陈锋
    {"person_id": 14, "org_id": 2, "title": "象州县人民政府副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 覃会雅
    {"person_id": 15, "org_id": 2, "title": "象州县人民政府副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 黄永君
    {"person_id": 16, "org_id": 2, "title": "象州县人民政府副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 李耿
    {"person_id": 17, "org_id": 9, "title": "中共来宾市委组织部副部长", "start": "", "end": "present", "rank": "副处级", "note": "2025-09-08 宣布象州县委书记任命决定"},
]

# ── RELATIONSHIPS ───────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "罗威（县委书记）与梁建标（县长）为象州县现任党政主要一把手，同一班子共事", "overlap_org": "象州县", "overlap_period": "2025-09至今"},
    {"person_a": 3, "person_b": 1, "type": "predecessor_successor", "context": "张东为罗威的直接前任象州县委书记，2025-09-08 干部大会宣布由罗威接任", "overlap_org": "象州县", "overlap_period": "2025-09"},
    {"person_a": 3, "person_b": 2, "type": "上下级", "context": "张东任书记期间（2022-2025），梁建标任县委副书记、县长；2024-02 县长选举由主席团执行主席张东主持", "overlap_org": "象州县", "overlap_period": "2024-2025"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "罗威现任书记与县委副书记袁永利等四家班子共事", "overlap_org": "象州县", "overlap_period": "2025-09至今"},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "罗威任书记与县人大/四家班子黄彩波共事", "overlap_org": "象州县", "overlap_period": "2025-09至今"},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "梁建标任县长与县政府班子石宝等共事", "overlap_org": "象州县", "overlap_period": "2024至今"},
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "梁建标县长与副县长韦茜共事（县政府班子）", "overlap_org": "象州县", "overlap_period": "2024至今"},
    {"person_a": 2, "person_b": 13, "type": "上下级", "context": "梁建标县长与副县长黎裕宁共事（县政府班子）", "overlap_org": "象州县", "overlap_period": "2024至今"},
    {"person_a": 1, "person_b": 17, "type": "组织任命", "context": "来宾市委组织部副部长李耿赴象州宣布罗威任县委书记决定", "overlap_org": "中共来宾市委组织部/象州县", "overlap_period": "2025-09"},
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