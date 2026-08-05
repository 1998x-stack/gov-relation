#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 卫东区 (Weidong District, Pingdingshan, Henan) leadership network.

卫东区 — 河南省平顶山市辖区, 平顶山市中心城区之一, 总面积101平方公里, 辖12个街道,
常住人口30余万人. 资源和城区, 转型为第三代半导体、电子制造/智能制造等产业方向.

DataSource summary (confidence labels):
- 孟宪强 (区委书记): 任前公示(平顶山日报 2023-11-11)确认 1975年2月生, 大学, 经济学学士;
  市人大常委会任命为退役军人事务局局长 (2023-12-26); 市法制局/市委老干部局 (2025-11); 当选卫东区委书记 (2026-06-24).
- 宋建立 (区长): 官方简历页 1972年11月生, 省委党校研究生; 2022-07 起任区长.
- 朱晓鹏 (副书记): 任前公示(2025-02-13)确认 1978年8月生, 在职研究生, 经济学硕士; 曾任卫东区纪委书记.
- 现任区领导班子名单/分工确认自 卫东区县级领导干部接访表(2026-08).
- 前任区委书记 张斌 (2022-03~2026-03), 离任去向前 / 更早 王立波.

Confidence note: 领域字段 (birthplace/education party membership) 对增图 central leaders 据此来自
历年任前公示/官方简历; 其余值班成员身份信息(出生)未查得, 标注 unknown.
"""

import sys
import sqlite3
from pathlib import Path

BASE = Path("/workspace/data/xieming/other-codes/gov-relation")
sys.path.insert(0, str(BASE))

from gov_relation.runner import run_build

# ── Paths ────────────────────────────────────────────────────────────
STAGING = BASE / "data/tmp/henan_卫东区"
DB_PATH = STAGING / "卫东区_network.db"
GEXF_PATH = STAGING / "卫东区_network.gexf"


# ══════════════════════════════════════════════════════════════════════
# PERSONS
# ══════════════════════════════════════════════════════════════════════
persons = [
    # ── 核心目标: 区委书记 ──
    {
        "id": 1, "name": "孟宪强", "gender": "男", "ethnicity": "汉族",
        "birth": "1975-02", "birthplace": "",
        "education": "大学/经济学学士", "party_join": "中共党员", "work_start": "",
        "current_post": "卫东区委书记", "current_org": "中共卫东区委",
        "source": "任前公示(平顶山日报2023-11-11)+十届一次全会(2026-06-24)",
    },

    # ── 核心目标: 区长 ──
    {
        "id": 2, "name": "宋建立", "gender": "男", "ethnicity": "汉族",
        "birth": "1972-11", "birthplace": "",
        "education": "省委党校研究生", "party_join": "中共党员", "work_start": "",
        "current_post": "卫东区委副书记、区长", "current_org": "卫东区人民政府",
        "source": "区政府领导简历页(2024-05)",
    },

    # ── 区委班子 ──
    {
        "id": 3, "name": "朱晓鹏", "gender": "男", "ethnicity": "汉族",
        "birth": "1978-08", "birthplace": "",
        "education": "在职研究生/经济学硕士", "party_join": "中共党员", "work_start": "",
        "current_post": "卫东区委副书记", "current_org": "中共卫东区委",
        "source": "任前公示(平顶山日报2025-02-13)+十届一次全会",
    },
    {
        "id": 4, "name": "李彩霞", "gender": "女", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "卫东区人大常委会主任", "current_org": "卫东区人大常委会",
        "source": "卫东区十一届人大六次会议(2026-02)",
    },
    {
        "id": 5, "name": "金武军", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "卫东区委常委", "current_org": "中共卫东区委",
        "source": "区十次党代会主席台名单",
    },
    {
        "id": 6, "name": "赵飞", "gender": "男", "ethnicity": "汉族",
        "birth": "1978-09", "birthplace": "",
        "education": "大学", "party_join": "中共党员", "work_start": "",
        "current_post": "卫东区委常委、常务副区长", "current_org": "卫东区人民政府",
        "source": "区政府领导简历页(2024-05)+接访表(2026-08)",
    },
    {
        "id": 7, "name": "尹小曼", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "卫东区委常委", "current_org": "中共卫东区委",
        "source": "区十次党代会主席台名单",
    },
    {
        "id": 8, "name": "胡瑞挺", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "卫东区委常委、政法委书记", "current_org": "中共卫东区委政法委",
        "source": "接访表(2026-08)",
    },
    {
        "id": 9, "name": "刘彦福", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "卫东区委常委", "current_org": "中共卫东区委",
        "source": "区十次党代会主席台名单",
    },
    {
        "id": 10, "name": "王延锋", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "卫东区委常委、区纪委书记、监委主任", "current_org": "中共卫东区纪委",
        "source": "区纪委一次全会(2026-06-24)+接访表",
    },
    {
        "id": 11, "name": "张新蕾", "gender": "女", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "卫东区委常委、统战部部长", "current_org": "中共卫东区委统战部",
        "source": "接访表(2026-08)",
    },
    {
        "id": 12, "name": "马勇", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "卫东区委常委、办公室主任", "current_org": "中共卫东区委办公室",
        "source": "接访表(2026-08)",
    },
    {
        "id": 13, "name": "丁建民", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "卫东区委常委、组织部部长", "current_org": "中共卫东区委组织部",
        "source": "接访表(2026-08)",
    },

    # ── 政府班子 ──
    {
        "id": 14, "name": "李海强", "gender": "男", "ethnicity": "汉族",
        "birth": "1977-01", "birthplace": "",
        "education": "大学", "party_join": "中共党员", "work_start": "",
        "current_post": "卫东区副区长、公安分局局长", "current_org": "平顶山市公安局卫东分局",
        "source": "区政府领导简历页(2024-05)",
    },
    {
        "id": 15, "name": "张世卿", "gender": "男", "ethnicity": "汉族",
        "birth": "1980-11", "birthplace": "",
        "education": "省委党校研究生", "party_join": "中共党员", "work_start": "",
        "current_post": "卫东区副区长", "current_org": "卫东区人民政府",
        "source": "区政府领导简历页(2024-05)",
    },
    {
        "id": 16, "name": "王昀灿", "gender": "男", "ethnicity": "汉族",
        "birth": "1977-05", "birthplace": "",
        "education": "省委党校研究生", "party_join": "中共党员", "work_start": "",
        "current_post": "卫东区副区长", "current_org": "卫东区人民政府",
        "source": "区政府领导简历页(2024-05)",
    },
    {
        "id": 17, "name": "张昕媛", "gender": "女", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "卫东区副区长", "current_org": "卫东区人民政府",
        "source": "接访表(2026-08), 分管民政卫健教体医保",
    },

    # ── 人大 / 政协 / 其他 ──
    {
        "id": 18, "name": "宋志勇", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "卫东区人大常委会副主任", "current_org": "卫东区人大常委会",
        "source": "卫东区十一届人大六次会议(2026-02)",
    },
    {
        "id": 19, "name": "孙丽君", "gender": "女", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "卫东区人大常委会副主任", "current_org": "卫东区人大常委会",
        "source": "卫东区十一届人大六次会议+接访表",
    },
    {
        "id": 20, "name": "季梅香", "gender": "女", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "", "party_join": "", "work_start": "",
        "current_post": "卫东区政协副主席", "current_org": "卫东区政协",
        "source": "区政府第五次全体会议报道",
    },
    {
        "id": 21, "name": "陈汶", "gender": "", "ethnicity": "",
        "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "卫东区二级调研员", "current_org": "卫东区人民政府",
        "source": "接访表(2026-08), 分工提案委员会等",
    },

    # ── 前任区委书记(关键节点) ──
    {
        "id": 22, "name": "张伟", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "已离任(原卫东区委书记)", "current_org": "",
        "source": "平顶山日报2026-03-03 人大会议确认2026-02时任书记",
    },
]

organizations = [
    {"id": 1, "name": "中共卫东区委", "type": "党委", "level": "县处级",
     "parent": "中共平顶山市委", "location": "河南省平顶山市卫东区"},
    {"id": 2, "name": "卫东区人民政府", "type": "政府", "level": "县处级",
     "parent": "平顶山市人民政府", "location": "河南省平顶山市卫东区"},
    {"id": 3, "name": "中共卫东区纪委/监委", "type": "党委", "level": "县处级",
     "parent": "中共平顶山市纪委", "location": "河南省平顶山市卫东区"},
    {"id": 4, "name": "中共卫东区委组织部", "type": "党委", "level": "乡科级",
     "parent": "中共卫东区委", "location": "河南省平顶山市卫东区"},
    {"id": 5, "name": "中共卫东区委政法委", "type": "党委", "level": "乡科级",
     "parent": "中共卫东区委", "location": "河南省平顶山市卫东区"},
    {"id": 6, "name": "中共卫东区委统战部", "type": "党委", "level": "乡科级",
     "parent": "中共卫东区委", "location": "河南省平顶山市卫东区"},
    {"id": 7, "name": "中共卫东区委办公室", "type": "党委", "level": "乡科级",
     "parent": "中共卫东区委", "location": "河南省平顶山市卫东区"},
    {"id": 8, "name": "卫东区人大常委会", "type": "人大", "level": "县处级",
     "parent": "平顶山市人大常委会", "location": "河南省平顶山市卫东区"},
    {"id": 9, "name": "卫东区政协", "type": "政协", "level": "县处级",
     "parent": "政协平顶山市委员会", "location": "河南省平顶山市卫东区"},
    {"id": 10, "name": "平顶山市公安局卫东分局", "type": "政府", "level": "乡科级",
     "parent": "平顶山市公安局", "location": "河南省平顶山市卫东区"},
    {"id": 11, "name": "平顶山市委老干部局", "type": "党委", "level": "县处级",
     "parent": "中共平顶山市委", "location": "河南省平顶山市"},
    {"id": 12, "name": "平顶山市退役军人事务局", "type": "政府", "level": "县处级",
     "parent": "平顶山市人民政府", "location": "河南省平顶山市"},
]

positions = [
    # 孟宪强
    {"person_id": 1, "org_id": 1, "title": "卫东区委书记", "start": "2026-06", "end": "present",
     "rank": "县处级正职", "note": "2026年6月24日十届一次全会当选"},
    {"person_id": 1, "org_id": 11, "title": "平顶山市委老干部局局长", "start": "2025-10", "end": "2026-03",
     "rank": "县处级正职", "note": "2025-11 平顶山日报报道时在职; 上任细节待查", "confidence": "confirmed"},
    {"person_id": 1, "org_id": 12, "title": "平顶山市退役军人事务局局长", "start": "2023-12", "end": "2025-10",
     "rank": "县处级正职", "note": "2023-12-26 市人大常委会任免", "confidence": "confirmed"},
    # 宋建立
    {"person_id": 2, "org_id": 2, "title": "卫东区区长", "start": "2022-07", "end": "present",
     "rank": "县处级正职", "note": "兼卫东区委副书记; 主持政府全面, 分管审计", "confidence": "confirmed"},
    {"person_id": 2, "org_id": 1, "title": "卫东区委副书记", "start": "2026-06", "end": "present",
     "rank": "县处级副职", "note": "十届一次全会连任副书记"},
    # 朱晓鹏
    {"person_id": 3, "org_id": 1, "title": "卫东区委副书记", "start": "2025-11", "end": "present",
     "rank": "县处级副职", "note": "任前公示2025-02-13拟任, 2026-06连任"},
    {"person_id": 3, "org_id": 3, "title": "卫东区纪委书记、监委主任", "start": "2022", "end": "2025",
     "rank": "县处级副职", "note": "此前担任区委常委、纪委书记", "confidence": "confirmed"},
    # 李彩霞
    {"person_id": 4, "org_id": 8, "title": "卫东区人大常委会主任", "start": "", "end": "present",
     "rank": "县处级副职", "note": "主持人大常委会"},
    {"person_id": 4, "org_id": 1, "title": "卫东区委常委", "start": "", "end": "present",
     "rank": "县处级副职", "note": ""},
    # 金武军 / 尹小曼 / 刘彦福 (常委, 分工待查)
    {"person_id": 5, "org_id": 1, "title": "卫东区委常委", "start": "2026-06", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "卫东区委常委", "start": "2026-06", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "卫东区委常委", "start": "2026-06", "end": "present", "rank": "县处级副职", "note": ""},
    # 赵飞
    {"person_id": 6, "org_id": 2, "title": "卫东区委常委、常务副区长", "start": "", "end": "present",
     "rank": "县处级副职", "note": "协助区长分管审计"},
    {"person_id": 6, "org_id": 1, "title": "卫东区委常委", "start": "2026-06", "end": "present", "rank": "县处级副职", "note": ""},
    # 胡瑞挺 / 王延锋 / 张新蕾 / 马勇 / 丁建民 (常委+专责)
    {"person_id": 8, "org_id": 5, "title": "卫东区委政法委书记", "start": "", "end": "present", "rank": "乡科级正职", "note": "区委常委"},
    {"person_id": 10, "org_id": 3, "title": "卫东区纪委书记、监委主任", "start": "2026-06", "end": "present",
     "rank": "县处级副职", "note": "2026-06-24 区纪委一次全会当选, 区委常委"},
    {"person_id": 11, "org_id": 6, "title": "卫东区委统战部部长", "start": "", "end": "present", "rank": "乡科级正职", "note": "区委常委"},
    {"person_id": 12, "org_id": 7, "title": "卫东区委办公室主任", "start": "", "end": "present", "rank": "乡科级正职", "note": "区委常委"},
    {"person_id": 13, "org_id": 4, "title": "卫东区委组织部部长", "start": "", "end": "present", "rank": "乡科级正职", "note": "区委常委"},
    # 政府副职
    {"person_id": 14, "org_id": 10, "title": "卫东公安分局局长", "start": "", "end": "present", "rank": "乡科级正职", "note": "副区长兼任"},
    {"person_id": 14, "org_id": 2, "title": "卫东区副区长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "卫东区副区长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "卫东区副区长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "卫东区副区长", "start": "", "end": "present", "rank": "县处级副职", "note": "分管民政、教育、卫生健康、医保"},
    # 人大 / 政协
    {"person_id": 18, "org_id": 8, "title": "卫东区人大常委会副主任", "start": "2026-02", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 19, "org_id": 8, "title": "卫东区人大常委会副主任", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 20, "org_id": 9, "title": "卫东区政协副主席", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 21, "org_id": 2, "title": "卫东区二级调研员", "start": "", "end": "present", "rank": "", "note": ""},
    # 前任书记 张伟
    {"person_id": 22, "org_id": 1, "title": "卫东区委书记(前任,九届)", "start": "2022-03", "end": "2026-03",
     "rank": "县处级正职", "note": "2026-02 人大会议仍以区委书记致辞, 2026-03后离任"},
]

relationships = [
    # ── 现班子核心 ──
    {"person_a": 1, "person_b": 2, "type": "overlap", "strength": "strong",
     "context": "区委书记 [孟宪强] ↔ 区长 [宋建立] 正副书记搭档", "overlap_org": "中共卫东区委", "overlap_period": "2026-06至今"},
    {"person_a": 1, "person_b": 3, "type": "overlap", "strength": "strong",
     "context": "区委书记 ↔ 专职副书记", "overlap_org": "中共卫东区委", "overlap_period": "2026-06至今"},
    {"person_a": 3, "person_b": 10, "type": "overlap", "strength": "medium",
     "context": "前后任纪委书记(黄晓鹏→王延锋, 纪检系统交接)", "overlap_org": "中共卫东区纪委", "overlap_period": "2025-2026"},

    # ── 常委关系 ──
    {"person_a": 1, "person_b": 10, "type": "overlap", "strength": "strong",
     "context": "区委书记 ↔ 纪委书记(党内监督)", "overlap_org": "中共卫东区委常委会", "overlap_period": "2026-06至今"},
    {"person_a": 1, "person_b": 13, "type": "overlap", "strength": "medium",
     "context": "区委书记 ↔ 组织部长(干部工作)", "overlap_org": "中共卫东区委常委会", "overlap_period": "2026-06至今"},
    {"person_a": 1, "person_b": 8, "type": "overlap", "strength": "medium",
     "context": "区委书记 ↔ 政法委书记", "overlap_org": "中共卫东区委常委会", "overlap_period": "2026-06至今"},
    {"person_a": 1, "person_b": 6, "type": "overlap", "strength": "medium",
     "context": "区委书记 ↔ 常务副区长", "overlap_org": "中共卫东区委常委会", "overlap_period": "2026-06至今"},

    # ── 政府班子 ──
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "strength": "strong",
     "context": "区长 [宋建立] ↔ 常务副区长(协助分管审计)", "overlap_org": "卫东区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate", "strength": "medium",
     "context": "区长 ↔ 副区长/公安局长", "overlap_org": "卫东区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate", "strength": "medium",
     "context": "区长 ↔ 副区长", "overlap_org": "卫东区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 16, "type": "superior_subordinate", "strength": "medium",
     "context": "区长 ↔ 副区长", "overlap_org": "卫东区人民政府", "overlap_period": ""},

    # ── 前任/继任 (关键节点) ──
    {"person_a": 22, "person_b": 1, "type": "predecessor_successor", "strength": "strong",
     "context": "张冠 九届区委书记 → 孟宪强 十届区委书记 (2026-06交接)", "overlap_org": "中共卫东区委", "overlap_period": "2026-03~2026-06"},
    {"person_a": 22, "person_b": 2, "type": "overlap", "strength": "strong",
     "context": "前任书记 ↔ 区长(共事: 张伟为书记、宋建立为区长 2021-2026前)", "overlap_org": "中共卫东区委", "overlap_period": "2021-2026"},

    ]


def main():
    print("=== Building 卫东区 network data ===")
    print("Target: 区委书记 & 区长; 交叉区干部交流")

    run_build(
        slug="卫东区",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    print(f"\n=== Summary ===")
    print(f"Persons: {len(persons)}")
    print(f"Organizations: {len(organizations)}")
    print(f"Positions: {len(positions)}")
    print(f"Relationships: {len(relationships)}")
    print(f"\nDB:   {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print("=== Done ===")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())