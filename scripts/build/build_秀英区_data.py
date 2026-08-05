#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 海口市秀英区 leadership network.

秀英区隶属海南省省会海口市，位于海南岛北部，是海口市市辖区之一，辖 6 镇（长流、西秀、海秀、
东山、永兴、石山）与 2 街道（秀英、书海）等。区情以港口经济、自贸港园区（海口综合保税区、
海口国家高新技术产业开发区）、城市更新、乡村振兴等为主要领域。

Current officeholders (as of 2026-08, sources: 海口市秀英区人民政府门户网“领导信息/区政府领导”、
海口市委组织部任前公示、海南省委组织部干部任前公示、澎湃/新浪/网易等多家权威媒体):
- 区委书记: 薄毅（2025-10-17 到任，仍任；原海口市生态环境局党组书记、局长）
- 区长: 吴翔（2025-11-26 当选；原海口市人民政府副秘书长）
- 前任区委书记 符勇（2022—2025，2025-03 落马、双开、公诉）
- 前任区长 柳战良（2020-06—2025-11，2025-11-18 落马被查）

Biographical data sourced from official government pages and appointment notices.
Confidence per person/claim marked where uncertain（见 report 与 report/open_gaps.md）。
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

SLUG = "秀英区"

_STAGING = os.environ.get("STAGING_DIR")
if _STAGING:
    DB_PATH = os.path.join(_STAGING, "秀英区_network.db")
    GEXF_PATH = os.path.join(_STAGING, "秀英区_network.gexf")
else:
    DB_PATH = DATABASE_DIR / "秀英区_network.db"
    GEXF_PATH = GRAPH_DIR / "秀英区_network.gexf"

# ── ORGANIZATIONS ───────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共海口市秀英区委员会", "type": "党委", "level": "县处级", "parent": "中共海口市委", "location": "海南省海口市秀英区"},
    {"id": 2, "name": "海口市秀英区人民政府", "type": "政府", "level": "县处级", "parent": "海口市人民政府", "location": "海南省海口市秀英区"},
    {"id": 3, "name": "海口市秀英区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "海口市人大常委会", "location": "海南省海口市秀英区"},
    {"id": 4, "name": "中国人民政治协商会议海口市秀英区委员会", "type": "政协", "level": "县处级", "parent": "政协海口市委员会", "location": "海南省海口市秀英区"},
    {"id": 5, "name": "中共海口市秀英区纪律检查委员会/秀英区监察委员会", "type": "纪委", "level": "县处级", "parent": "中共海口市纪委", "location": "海南省海口市秀英区"},
    {"id": 6, "name": "海口市生态环境局", "type": "政府部门", "level": "县处级", "parent": "海口市人民政府", "location": "海南省海口市"},
    {"id": 7, "name": "海南省生态环境厅", "type": "政府部门", "level": "省厅级", "parent": "海南省人民政府", "location": "海南省海口市"},
    {"id": 8, "name": "中共海口市委员会", "type": "党委", "level": "地厅级", "parent": "中共海南省委员会", "location": "海南省海口市"},
    {"id": 9, "name": "海口市人民政府", "type": "政府", "level": "地厅级", "parent": "海南省人民政府", "location": "海南省海口市"},
    {"id": 10, "name": "中共海口市琼山区委员会", "type": "党委", "level": "县处级", "parent": "中共海口市委", "location": "海南省海口市琼山区"},
    {"id": 11, "name": "海口市食品药品监督管理局", "type": "政府部门", "level": "县处级", "parent": "海口市人民政府", "location": "海南省海口市"},
    {"id": 12, "name": "海口市市场监督管理局", "type": "政府部门", "level": "县处级", "parent": "海口市人民政府", "location": "海南省海口市"},
    {"id": 13, "name": "海南洋浦经济开发区安全生产监督管理局", "type": "开发区/政府部门", "level": "副厅级", "parent": "洋浦经济开发区管委会", "location": "海南省儋州市洋浦"},
    {"id": 14, "name": "海口市人民政府办公厅", "type": "政府部门", "level": "县处级", "parent": "海口市人民政府", "location": "海南省海口市"},
    {"id": 15, "name": "海口国家高新技术产业开发区管委会", "type": "开发区", "level": "县处级", "parent": "海口市人民政府", "location": "海南省海口市"},
    {"id": 16, "name": "海口市龙华区人民政府", "type": "政府", "level": "县处级", "parent": "海口市人民政府", "location": "海南省海口市龙华区"},
    {"id": 17, "name": "琼山市龙桥镇人民政府", "type": "乡镇/街道", "level": "乡镇级", "parent": "琼山市人民政府", "location": "海南省海口市（原琼山市）"},
    {"id": 18, "name": "海口市龙华区龙桥镇人民政府", "type": "乡镇/街道", "level": "乡镇级", "parent": "海口市龙华区人民政府", "location": "海南省海口市龙华区"},
    {"id": 19, "name": "共青团海口市龙华区委员会", "type": "群团", "level": "县处级以下", "parent": "共青团海口市委员会", "location": "海南省海口市龙华区"},
    {"id": 20, "name": "海口市龙华区龙泉镇人民政府", "type": "乡镇/街道", "level": "乡镇级", "parent": "海口市龙华区人民政府", "location": "海南省海口市龙华区"},
    {"id": 21, "name": "中共海口市龙华区龙泉镇委员会", "type": "党委（基层）", "level": "乡镇级", "parent": "中共海口市龙华区委", "location": "海南省海口市龙华区"},
    {"id": 22, "name": "中共海南省委员会", "type": "党委", "level": "省部级", "parent": "", "location": "海南省海口市"},
    {"id": 23, "name": "海口市综合保税区", "type": "开发区", "level": "县处级", "parent": "海口市人民政府", "location": "海南省海口市秀英区"},
]

# ── PERSONS ─────────────────────────────────────────────────────────
persons = [
    # 1 — 薄毅 — 现任区委书记
    {"id": 1, "name": "薄毅", "gender": "男", "ethnicity": "汉族",
     "birth": "1977年2月", "birthplace": "（中文资料未载明）",
     "education": "大学本科学历，工学学士，法律硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共海口市秀英区委书记", "current_org": "中共海口市秀英区委员会",
     "source": "https://www.xiuyingqu.gov.cn/（领导信息）；澎湃新闻2025-10-17"},
    # 2 — 吴翔 — 现任区长
    {"id": 2, "name": "吴翔", "gender": "男", "ethnicity": "汉族",
     "birth": "1975年1月", "birthplace": "海南海口",
     "education": "大学学历，公共管理硕士",
     "party_join": "中共党员", "work_start": "1999年4月",
     "current_post": "秀英区委副书记、区政府党组书记、区长", "current_org": "海口市秀英区人民政府",
     "source": "https://www.xiuying.haikou.gov.cn/ 区政府领导信息 2025-12-01"},
    # 3 — 符勇 — 前任区委书记（落马）
    {"id": 3, "name": "符勇", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "（原）海口市秀英区委书记，2025年3月起接受审查调查", "current_org": "中共海口市秀英区委员会",
     "source": "清廉海南网 2025-06-24；海南省纪委监委"},
    # 4 — 柳战良 — 前任区长（落马）
    {"id": 4, "name": "柳战良", "gender": "男", "ethnicity": "汉族",
     "birth": "1982年5月", "birthplace": "湖南浏阳",
     "education": "研究生学历，工学硕士（中国石油大学本硕）",
     "party_join": "中共党员", "work_start": "2007年",
     "current_post": "（原）秀英区人民政府区长，2025年11月被查", "current_org": "海口市秀英区人民政府",
     "source": "人民网干部任前公示 2025-06-24；海口市纪委监委 2025-11-18"},
    # 5 — 郭刚 — 更早前任区委书记（2021年八届区委书记）
    {"id": 5, "name": "郭刚", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "（曾任）海口市秀英区委书记（2021年在任）", "current_org": "中共海口市秀英区委员会",
     "source": "人民网海南频道 2021-11-28"},
    # 6 — 冯锦川 — 区委副书记、政法委书记
    {"id": 6, "name": "冯锦川", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "秀英区委副书记、政法委书记", "current_org": "中共海口市秀英区委员会",
     "source": "海口市秀英区人民政府 工作动态（西秀镇会议）"},
    # 7 — 肖就荣 — 区委常委、副区长
    {"id": 7, "name": "肖就荣", "gender": "男", "ethnicity": "汉族",
     "birth": "1973年3月", "birthplace": "",
     "education": "大学学历", "party_join": "中共党员", "work_start": "",
     "current_post": "秀英区委常委、区政府党组成员、副区长", "current_org": "海口市秀英区人民政府",
     "source": "海口市秀英区人民政府 领导信息 2026-06-09"},
    # 8 — 郭文超 — 区委常委、副区长
    {"id": 8, "name": "郭文超", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "秀英区委常委、副区长", "current_org": "海口市秀英区人民政府",
     "source": "秀英区要闻（微信）2024-12-23 投资项目签约仪式"},
    # 9 — 黄先锋 — 副区长（挂职）
    {"id": 9, "name": "黄先锋", "gender": "男", "ethnicity": "汉族",
     "birth": "1978年10月", "birthplace": "",
     "education": "大学学历", "party_join": "中共党员", "work_start": "",
     "current_post": "秀英区政府党组成员、副区长（挂职）", "current_org": "海口市秀英区人民政府",
     "source": "海口市秀英区人民政府 领导信息 2026-06-09"},
    # 10 — 陈绮 — 区监委主任
    {"id": 10, "name": "陈绮", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "海口市秀英区监察委员会主任", "current_org": "中共海口市秀英区纪律检查委员会/监察委员会",
     "source": "海南特区报 2025-11-26"},
    # 11 — 林晓霞 — 区人大常委会副主任
    {"id": 11, "name": "林晓霞", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "海口市秀英区人大常委会副主任", "current_org": "海口市秀英区人民代表大会常务委员会",
     "source": "海南特区报 2025-11-26"},
    # 12 — 裴克波 — 区人大常委会主任
    {"id": 12, "name": "裴克波", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "海口市秀英区人大常委会主任", "current_org": "海口市秀英区人民代表大会常务委员会",
     "source": "消费日报网 2025-01-22（区政协一届五次会议）"},
    # 13 — 符源明 — 区政协副主席
    {"id": 13, "name": "符源明", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "海口市秀英区政协副主席", "current_org": "中国人民政治协商会议海口市秀英区委员会",
     "source": "百度百科（秀英区政协副主席）"},
]

# ── POSITIONS ───────────────────────────────────────────────────────
positions = [
    # 薄毅 (1)
    {"person_id": 1, "org_id": 1, "title": "海口市秀英区委书记", "start": "2025-10-17", "end": "present", "rank": "正处级", "note": "2025-10-17 省委决定任区委书记"},
    {"person_id": 1, "org_id": 6, "title": "海口市生态环境局党组书记、局长", "start": "2021", "end": "2025-10", "rank": "正处级", "note": "2021年履新，2025-10-08公示拟任区党委书记"},
    {"person_id": 1, "org_id": 7, "title": "海南省生态环境厅大气环境管理处处长", "start": "", "end": "2021", "rank": "正处级", "note": "此前曾任省生态环境厅生态监测与科技标准处副处长、大气环境管理处处长等"},
    # 吴翔（区长）
    {"person_id": 2, "org_id": 2, "title": "秀英区委副书记、区政府党组书记、区长", "start": "2025-11-26", "end": "present", "rank": "正处级", "note": "2025-11-26 八届人大六次会议当选区长"},
    {"person_id": 2, "org_id": 9, "title": "海口市人民政府副秘书长（正处级）", "start": "", "end": "2025-11", "rank": "正处级", "note": "市人民政府机关党组成员（任前公示2025-09-27）"},
    {"person_id": 2, "org_id": 15, "title": "海口国家高新技术产业开发区管委会（领导）", "start": "", "end": "", "rank": "县处级", "note": "2019年任前公示时已在高新区管委会规划处任职（待细化）"},
    {"person_id": 2, "org_id": 21, "title": "海口市龙华区龙泉镇委书记", "start": "", "end": "", "rank": "正科级", "note": "曾任龙泉镇委副书记、镇长、镇委书记、镇人大主席"},
    {"person_id": 2, "org_id": 19, "title": "共青团海口市龙华区委书记", "start": "", "end": "", "rank": "正科级", "note": ""},
    {"person_id": 2, "org_id": 18, "title": "海口市龙华区龙桥镇副镇长", "start": "", "end": "", "rank": "副科级", "note": ""},
    {"person_id": 2, "org_id": 17, "title": "琼山市龙桥镇副镇长", "start": "", "end": "", "rank": "副科级", "note": "参加工作之初基层起步"},
    # 符勇（前任书记，落马）
    {"person_id": 3, "org_id": 1, "title": "海口市秀英区委书记", "start": "2022", "end": "2025-03", "rank": "正处级", "note": "2025-03-21 被查"},
    {"person_id": 3, "org_id": 12, "title": "海口市市场监督管理局副局长、局长", "start": "", "end": "2022", "rank": "正处级", "note": "涉氏市监局任职"},
    {"person_id": 3, "org_id": 11, "title": "海口市食品药品监督管理局局长", "start": "", "end": "", "rank": "正处级", "note": ""},
    {"person_id": 3, "org_id": 10, "title": "海口市琼山区委常委、宣传部部长", "start": "", "end": "", "rank": "副处级", "note": ""},
    # 柳战良（前任区长，落马）
    {"person_id": 4, "org_id": 2, "title": "秀英区委副书记、区长", "start": "2020-06-30", "end": "2025-11", "rank": "正处级", "note": "2020-06-30 全票当选；2025-11-18 被查"},
    {"person_id": 4, "org_id": 14, "title": "海口市政府办公厅主任", "start": "", "end": "", "rank": "正处级", "note": ""},
    {"person_id": 4, "org_id": 9, "title": "海口市人民政府副秘书长", "start": "", "end": "", "rank": "正处级", "note": ""},
    {"person_id": 4, "org_id": 13, "title": "洋浦经济开发区安监局局长、党组书记", "start": "", "end": "", "rank": "正处级", "note": "曾任洋浦安监局长、市政府办公厅等"},
    # 郭刚（更早前任书记）
    {"person_id": 5, "org_id": 1, "title": "海口市秀英区委书记", "start": "", "end": "2021", "rank": "正处级", "note": "2021-11 八届区委书记在任"},
    # 冯锦川
    {"person_id": 6, "org_id": 1, "title": "秀英区委副书记、政法委书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 肖就荣
    {"person_id": 7, "org_id": 2, "title": "秀英区委常委、副区长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 郭文超
    {"person_id": 8, "org_id": 2, "title": "秀英区委常委、副区长", "start": "", "end": "present", "rank": "副处级", "note": "2024-12 负责招商工作"},
    # 黄先锋
    {"person_id": 9, "org_id": 2, "title": "秀英区副区长（挂职）", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 陈绮
    {"person_id": 10, "org_id": 5, "title": "秀英区监察委员会主任", "start": "2025-11-26", "end": "present", "rank": "副处级", "note": ""},
    # 林晓霞
    {"person_id": 11, "org_id": 3, "title": "秀英区人大常委会副主任", "start": "2025-11-26", "end": "present", "rank": "副处级", "note": ""},
    # 裴克波
    {"person_id": 12, "org_id": 3, "title": "秀英区人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 符源明
    {"person_id": 13, "org_id": 4, "title": "秀英区政协副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
]

# ── RELATIONSHIPS ───────────────────────────────────────────────────
relationships = [
    # 现任党政一把手搭档
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "薄毅（区委书记）与吴翔（区长）为秀英区现任党政一把手，同一班子共事", "overlap_org": "海口市秀英区", "overlap_period": "2025-11 至今"},
    {"person_a": 1, "person_b": 2, "type": "上下级", "context": "薄毅任书记，吴翔任区长（党政上下级搭档）", "overlap_org": "海口市秀英区", "overlap_period": "2025-11 至今"},
    # 继任链条：符勇 → 薄毅
    {"person_a": 3, "person_b": 1, "type": "predecessor_successor", "context": "薄毅接任被查前任书记符勇的秀英区委书记职务", "overlap_org": "海口市秀英区", "overlap_period": "2025"},
    # 继任链条：柳战良 → 吴翔
    {"person_a": 4, "person_b": 2, "type": "predecessor_successor", "context": "吴翔接任被查原区长柳战良的区长职务", "overlap_org": "海口市秀英区", "overlap_period": "2025-11"},
    # 前任两主官相继被查（相互独立事件，但同区）
    {"person_a": 3, "person_b": 4, "type": "同一班子", "context": "符勇任书记、柳战良任区长同期（2022-2025），两人相继被查", "overlap_org": "海口市秀英区", "overlap_period": "2022-2025"},
    # 薄毅与区委班子（党代会/常委会）
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "薄毅任书记时期冯锦川任区委副书记、政法委书记", "overlap_org": "海口市秀英区", "overlap_period": "2025 至今"},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "薄毅任书记时肖就荣任区委常委、副区长", "overlap_org": "海口市秀英区", "overlap_period": "2025 至今"},
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "薄毅任书记时郭文超任区委常委、副区长", "overlap_org": "海口市秀英区", "overlap_period": "2025 至今"},
    # 吴翔与区政府班子（区政府领导分工）
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "吴翔任区长时肖就荣任常务副区长", "overlap_org": "海口市秀英区人民政府", "overlap_period": "2025-11 至今"},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "吴翔任区长时郭文超任副区长", "overlap_org": "海口市秀英区人民政府", "overlap_period": "2025-11 至今"},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "吴翔任区长时黄先锋任副区长（挂职）", "overlap_org": "海口市秀英区人民政府", "overlap_period": "2025-11 至今"},
    # 人大/政协/纪委同步班子
    {"person_a": 1, "person_b": 12, "type": "同一班子", "context": "薄毅任书记时裴克波任区人大主任", "overlap_org": "海口市秀英区", "overlap_period": "2025 至今"},
    {"person_a": 2, "person_b": 10, "type": "同一班子", "context": "吴翔当选区长同日陈绮当选区监委主任", "overlap_org": "区八届人大六次会", "overlap_period": "2025-11-26"},
    {"person_a": 2, "person_b": 11, "type": "同一班子", "context": "吴翔当选区长时林晓霞当选区人大副主任", "overlap_org": "区人大", "overlap_period": "2025-11-26"},
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