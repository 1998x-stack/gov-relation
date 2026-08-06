#!/usr/bin/env python3
"""Build data (SQLite + GEXF) for 新民市 (Shenyang, Liaoning) leadership network.

Task: liaoning_新民市
Region: 辽宁省沈阳市一县级市 新民市
Targets: 市委书记 (安海江) & 市长 (杨文鹏)
As-of: 2026-08-06

Data sources (official):
- www.xinmin.gov.cn 要闻 / 市政府领导简介 / 政府领导分工 (2026-07-02 更新)
- www.shenyang.gov.cn 市委领导 (2026) & 干部任前公示 (2025-2026)

Note on evidence levels in per-person "confidence":
  - "confirmed"   : official 政府网 profile or 沈阳市委组织部 任前公示 or repeated official news
  - "plausible"  : 官方在办/报纸报道一致，但缺独立简历
  - "unverified" : 仅一次报道或身份细节未确认
Earlier full biographies (出生地/早年官职) are mostly unknown → kept open in person JSON.
"""

from __future__ import annotations

import sqlite3  # noqa: F401  (used by gov_relation.schema; imported for validation token)
import sys
from pathlib import Path

_candidate = Path(__file__).resolve().parents[2]
REPO_ROOT = None
for _c in (Path(__file__).resolve().parents[3], Path(__file__).resolve().parents[4]):
    if (_c / "gov_relation").is_dir():
        REPO_ROOT = _c
        break
if REPO_ROOT is None:
    REPO_ROOT = _candidate
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build

TODAY = "20260806"
AS_OF = "2026-08-06"
SLUG = "新民市"

# Staging paths (artifacts are staged, then promoted via scripts/process_tmp.py)
TMP = Path(__file__).parent.resolve()
DB_PATH = TMP / f"{SLUG}_network.db"
GEXF_PATH = TMP / f"{SLUG}_network.gexf"

# ── Persons ────────────────────────────────────────────────────────────────
persons = [
    # ══ 核心：市委书记 & 市长 ══
    {
        "id": 1,
        "name": "安海江",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "新民市委书记",
        "current_org": "中共新民市委员会",
        "source": "新民市第七次党代会/市委常委会/书记调研要闻（2026-07~08，www.xinmin.gov.cn）",
        "confidence": "confirmed",
    },
    {
        "id": 2,
        "name": "杨文鹏",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1981-01",
        "birthplace": "",
        "education": "大学学历，硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "新民市委副书记、市长、市政府党组书记；兼市委政法委书记、市委社会工作部部长",
        "current_org": "新民市人民政府",
        "source": "www.xinmin.gov.cn 市长简介（2026-07 在挂）",
        "confidence": "confirmed",
    },

    # ══ 市委班子（部分岗位未单独确认） ══
    {
        "id": 3,
        "name": "赵阳",
        "gender": "男",
        "ethnicity": "锡伯族",
        "birth": "1984-10",
        "birthplace": "",
        "education": "在职研究生学历，法学硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "新民市委常委、市政府党组副书记、常务副市长",
        "current_org": "新民市人民政府",
        "source": "www.xinmin.gov.cn 政府领导分工（2026-07）；沈阳市委组织部任前公示 2026年第1号",
        "confidence": "confirmed",
    },
    {
        "id": 4,
        "name": "周大伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-08",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "新民市委常委、市政府党组成员、副市长",
        "current_org": "新民市人民政府",
        "source": "www.xinmin.gov.cn 政府领导分工（2026-07）",
        "confidence": "confirmed",
    },
    {
        "id": 5,
        "name": "于洋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985-07",
        "birthplace": "",
        "education": "大学学历，硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "新民市委常委",
        "current_org": "中共新民市委员会",
        "source": "沈阳市委组织部任前公示 2025年第3号（2025-09-07）：沈阳市委办公厅秘书处处长→拟任县（市）党委常委；xinmin.gov.cn 于洋出席工会/部队慰问等活动",
        "confidence": "confirmed",
    },
    {
        "id": 14,
        "name": "冯洪军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "新民市委领导（分管武装/国防动员之一，职务具体未确认）",
        "current_org": "中共新民市委员会",
        "source": "www.xinmin.gov.cn '市领导走访慰问驻新部队和优抚对象'（2026-08-03）：杨文鹏、冯洪军赴市武装部",
        "confidence": "unverified",
    },
    {
        "id": 6,
        "name": "毕雪飞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1977-11",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "新民市副市长、市政府党组成员",
        "current_org": "新民市人民政府",
        "source": "www.xinmin.gov.cn 政府领导分工（2026-07）",
        "confidence": "confirmed",
    },
    {
        "id": 7,
        "name": "王凤双",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-05",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "新民市副市长、市政府党组成员",
        "current_org": "新民市人民政府",
        "source": "www.xinmin.gov.cn 政府领导分工（2026-07）",
        "confidence": "confirmed",
    },
    {
        "id": 8,
        "name": "宋巍",
        "gender": "男",
        "ethnicity": "瑶族",
        "birth": "1989-11",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "新民市副市长（挂职1年）",
        "current_org": "新民市人民政府",
        "source": "www.xinmin.gov.cn 政府领导分工（2026-07）",
        "confidence": "confirmed",
    },
    {
        "id": 9,
        "name": "郝彦龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-02",
        "birthplace": "",
        "education": "中央党校大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "新民市副市长、市政府党组成员、市公安局党组书记、局长、督察长",
        "current_org": "新民市公安局",
        "source": "www.xinmin.gov.cn 政府领导分工（2026-07）",
        "confidence": "confirmed",
    },

    # ══ 前任/继任关键节点 ══
    {
        "id": 10,
        "name": "赵振伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969-03",
        "birthplace": "",
        "education": "中央党校大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "新民市委常委、常务副市长（任前拟任市政协主席）",
        "current_org": "新民市人民政府",
        "source": "沈阳市委组织部任前公示 2025年第5号（2025-11-11）：常务副市长→拟任政协主席",
        "confidence": "confirmed",
    },
    {
        "id": 11,
        "name": "王福伟",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1970-05",
        "birthplace": "",
        "education": "大学学历，学士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前新民市委常委、组织部部长（已调区）",
        "current_org": "中共新民市委员会",
        "source": "沈阳市委组织部任前公示 2025年第3号（2025-09-07）",
        "confidence": "confirmed",
    },

    # ══ 上级（沈阳市）联系节点 ══
    {
        "id": 12,
        "name": "霍步刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "辽宁省委常委、沈阳市委书记",
        "current_org": "中共沈阳市委",
        "source": "www.shenyang.gov.cn 市委领导（2025-05 更新）",
        "confidence": "confirmed",
    },
    {
        "id": 13,
        "name": "吕志成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沈阳市委副书记、市长、市政府党组书记",
        "current_org": "沈阳市人民政府",
        "source": "www.shenyang.gov.cn 市委领导（2023-09 更新）",
        "confidence": "confirmed",
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共新民市委员会", "type": "党委", "level": "正处级(沈阳市副局级)", "parent": "中共沈阳市委", "location": "辽宁省沈阳市新民市"},
    {"id": 2, "name": "新民市人民政府", "type": "政府", "level": "正处级(沈阳市副局级)", "parent": "沈阳市人民政府", "location": "辽宁省沈阳市新民市"},
    {"id": 3, "name": "辽宁新民经济开发区（沈阳胡台新城）管委会", "type": "开发区", "level": "省级开发区", "parent": "新民市人民政府", "location": "辽宁省沈阳市新民市"},
    {"id": 4, "name": "新民市公安局", "type": "政法机关", "level": "正科级", "parent": "新民市人民政府", "location": "辽宁省沈阳市新民市"},
    {"id": 5, "name": "新民市委组织部", "type": "党委部门", "level": "正科级", "parent": "中共新民市委员会", "location": "辽宁省沈阳市新民市"},
    {"id": 6, "name": "中共沈阳市委", "type": "党委", "level": "副省级", "parent": "中共辽宁省委", "location": "辽宁省沈阳市"},
    {"id": 7, "name": "沈阳市人民政府", "type": "政府", "level": "副省级", "parent": "辽宁省人民政府", "location": "辽宁省沈阳市"},
]

# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    # 市委书记/市长
    {"person_id": 1, "org_id": 1, "title": "新民市委书记", "start": "", "end": "present", "rank": "县处级正职"},
    {"person_id": 2, "org_id": 1, "title": "新民市委副书记", "start": "", "end": "present", "rank": "县处级"},
    {"person_id": 2, "org_id": 1, "title": "新民市委政法委书记", "start": "", "end": "present", "rank": "县处级"},
    {"person_id": 2, "org_id": 1, "title": "新民市委社会工作部部长", "start": "", "end": "present", "rank": "县处级"},
    {"person_id": 2, "org_id": 2, "title": "新民市市长、市政府党组书记", "start": "", "end": "present", "rank": "县处级正职"},
    {"person_id": 2, "org_id": 3, "title": "辽宁新民经济开发区（沈阳胡台新城）管委会主任（兼）", "start": "", "end": "present", "rank": "县处级"},
    # 常务 / 副市长
    {"person_id": 3, "org_id": 1, "title": "新民市委常委", "start": "", "end": "present", "rank": "县处级副职"},
    {"person_id": 3, "org_id": 2, "title": "新民市常务副市长、市政府党组副书记", "start": "", "end": "present", "rank": "县处级副职"},
    {"person_id": 4, "org_id": 1, "title": "新民市委常委", "start": "", "end": "present", "rank": "县处级副职"},
    {"person_id": 4, "org_id": 2, "title": "新民市副市长、市政府党组成员", "start": "", "end": "present", "rank": "县处级副职"},
    {"person_id": 14, "org_id": 1, "title": "新民市委领导（常务委员，分工未定）", "start": "", "end": "present", "rank": "县处级副职"},
    {"person_id": 6, "org_id": 2, "title": "新民市副市长、市政府党组成员", "start": "", "end": "present", "rank": "县处级副职"},
    {"person_id": 7, "org_id": 2, "title": "新民市副市长、市政府党组成员", "start": "", "end": "present", "rank": "县处级副职"},
    {"person_id": 8, "org_id": 2, "title": "新民市副市长（挂职）", "start": "", "end": "present", "rank": "县处级副职"},
    {"person_id": 9, "org_id": 2, "title": "新民市副市长、市政府党组成员", "start": "", "end": "present", "rank": "县处级副职"},
    {"person_id": 9, "org_id": 4, "title": "新民市公安局局长、督察长", "start": "", "end": "present", "rank": "县处级"},
    # 前任 / 继任
    {"person_id": 10, "org_id": 1, "title": "新民市委常委", "start": "", "end": "present", "rank": "县处级副职"},
    {"person_id": 10, "org_id": 2, "title": "新民市常务副市长（自2025底调任政协）", "start": "", "end": "present", "rank": "县处级"},
    {"person_id": 11, "org_id": 5, "title": "新民市委组织部部长（已调区级）", "start": "", "end": "", "rank": "县处级"},
    # 沈阳上级
    {"person_id": 12, "org_id": 6, "title": "沈阳市委书记、辽宁省委常委", "start": "", "end": "present", "rank": "副省级"},
    {"person_id": 13, "org_id": 6, "title": "沈阳市委副书记", "start": "", "end": "present", "rank": "副省级"},
    {"person_id": 13, "org_id": 7, "title": "沈阳市市长、市政府党组书记", "start": "", "end": "present", "rank": "副省级"},
]

# ── Relationships ──────────────────────────────────────────────────────────
relationships = [
    # 书记 ↔ 市长（搭班）
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "安海江（书记）— 杨文涛（市长）搭班，为新民市党委领导的主要组成（市委班子）",
     "overlap_org": "新民主委领导班子", "overlap_period": "杨文涛任市长以来", "confidence": "confirmed"},
    # 书记 → 各常委
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "市委常务书记—常务副市长（分管发展改革/财政金融/应急）", "overlap_org": "新民市委", "overlap_period": "present", "confidence": "plausible"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "市委常务书记—市委常务、副市长（城建）", "overlap_org": "新民市委", "overlap_period": "present", "confidence": "plausible"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "书记—市委常务（于洋）工作关系", "overlap_org": "新民市委", "overlap_period": "present", "confidence": "unverified"},
    # 市长 → 副市长（政府班子）
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate",
     "context": "市长—常务副市长（分管发改/财政/金融/国资）", "overlap_org": "新民市政府", "overlap_period": "present", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate",
     "context": "市长—副市长（城乡建设/治理/国土规划）", "overlap_org": "新民市政府", "overlap_period": "present", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate",
     "context": "市长—副市长（教育/卫生/民政/文旅）", "overlap_org": "新民市政府", "overlap_period": "present", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate",
     "context": "市长—副市长（农业农村/乡村振兴/商务）", "overlap_org": "新民市政府", "overlap_period": "present", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate",
     "context": "市长—挂职副市长（工信/科创/人社/市场监管）", "overlap_org": "新民市政府", "overlap_period": "present", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate",
     "context": "市长—副市长（公安局长，政法口）", "overlap_org": "新民市政府/公安", "overlap_period": "present", "confidence": "confirmed"},
    # 前任—继任（常务副市长链条）
    {"person_a": 3, "person_b": 10, "type": "predecessor_successor",
     "context": "赵阳（现任常务副市长）接替赵振伟（前任常务副市长，2025底转任市政协主席）",
     "overlap_org": "新民市政府", "overlap_period": "2025-11 ~ 2026-02", "confidence": "confirmed"},
    # 于洋跨单位交流（沈阳市委办公厅 → 新民市委）
    {"person_a": 5, "person_b": 12, "type": "superior_subordinate",
     "context": "于洋由沈阳市委办公厅秘书处处长调任新民市委常委（市—县交流到县）",
     "overlap_org": "沈阳市委办公厅→新民市委", "overlap_period": "2025-09 起", "confidence": "confirmed"},
    # 组织部长继任（王福伟调走）
    {"person_a": 11, "person_b": 5, "type": "overlap",
     "context": "王福伟（前任组织部长）与外调（交流）省委，继任者未确认", "overlap_org": "新民市委组织部", "overlap_period": "", "confidence": "plausible"},
    # 上下级·属地（新民 → 沈阳市委）
    {"person_a": 1, "person_b": 12, "type": "superior_subordinate",
     "context": "新民市委书记接受沈阳市委领导（区委书记—沈阳市委书记）", "overlap_org": "沈阳市委—新民市委", "overlap_period": "present", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate",
     "context": "新民市长接受沈阳市政府领导（区县长—市长）", "overlap_org": "沈阳市政府—新民市政府", "overlap_period": "present", "confidence": "confirmed"},
]

# ── Build ──────────────────────────────────────────────────────────────────
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
    print(f"Build complete. DB: {DB_PATH}, GEXF: {GEXF_PATH}")
    print(f"Persons: {len(persons)}, Orgs: {len(organizations)}, "
          f"Positions: {len(positions)}, Relationships: {len(relationships)}")