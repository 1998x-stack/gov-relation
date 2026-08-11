#!/usr/bin/env python3
"""Build SQLite DB and GEXF graph for 珙县 leadership network.

Research date: 2026-07-26
Task ID: sichuan_珙县
Province: 四川省
Parent city: 宜宾市
Level: 县
Targets: 县委书记 & 县长

Primary sources:
  - https://www.gongxian.gov.cn/zfld/ (政府领导页面)
  - https://www.gongxian.gov.cn/zfld/xz/gg/ (县长高果简历)
  - https://www.gongxian.gov.cn/zfld/fxz/xjw/ (副县长谢建文简历)
  - https://www.gongxian.gov.cn/zfld/fxz/jzx/ (副县长贾泽鑫简历)
  - https://www.gongxian.gov.cn/ywdt/gxyw/202607/t20260717_2242654.html (沙之杰接访)
  - https://www.gongxian.gov.cn/ywdt/gxyw/202607/t20260724_2244421.html (县委常委会)
  - https://www.gongxian.gov.cn/ywdt/gxyw/202606/t20260608_2233895.html (沙之杰暗访)
  - 163.com/金台资讯 — "沙之杰任珙县县委书记" (2024-11-04)

Gaps:
  - 沙之杰早期履历未公开（到任珙县前经历）
  - 县委班子其他成员（专职副书记、纪委、组织、宣传、政法等）未在官网公开
  - 人大主任、政协主席名单
"""

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

slug = "珙县"

# ── Persons ──────────────────────────────────────────────────────────────
# ID convention: gongxian_{number}
persons = [
    # ── Top Leaders ──
    {
        "id": 10,
        "name": "沙之杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共珙县委员会",
        "source": "https://www.gongxian.gov.cn/ywdt/gxyw/202607/t20260717_2242654.html",
    },
    {
        "id": 11,
        "name": "高果",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年6月",
        "birthplace": "待查",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "珙县人民政府",
        "source": "https://www.gongxian.gov.cn/zfld/xz/gg/",
    },
    # ── Deputy County Mayors (县政府) ──
    {
        "id": 15,
        "name": "罗道戡",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "珙县人民政府",
        "source": "https://www.gongxian.gov.cn/ywdt/gxyw/202606/t20260608_2233895.html",
    },
    {
        "id": 16,
        "name": "侯杰",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委专职副书记",
        "current_org": "中共珙县委员会",
        "source": "会议报道确认",
    },
    {
        "id": 20,
        "name": "谢建文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1988年7月",
        "birthplace": "四川省南溪",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "珙县人民政府",
        "source": "https://www.gongxian.gov.cn/zfld/fxz/xjw/",
    },
    {
        "id": 21,
        "name": "贾泽鑫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年2月",
        "birthplace": "待查",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "珙县人民政府",
        "source": "https://www.gongxian.gov.cn/zfld/fxz/jzx/",
    },
    # ── Leaders mentioned in news (roles TBD) ──
    {
        "id": 30,
        "name": "谢国刚",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "珙县",
        "source": "https://www.gongxian.gov.cn/ywdt/gxyw/202607/t20260717_2242654.html",
    },
    {
        "id": 31,
        "name": "何银波",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "珙县",
        "source": "https://www.gongxian.gov.cn/ywdt/gxyw/202607/t20260717_2242654.html",
    },
    {
        "id": 32,
        "name": "罗道戡",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "珙县",
        "source": "https://www.gongxian.gov.cn/ywdt/gxyw/202606/t20260608_2233895.html",
    },
    # ── Other key officials ──
    {
        "id": 35,
        "name": "李智",
        "gender": "待查",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "珙县政协",
        "source": "会议报道确认",
    },
    # ── Predecessors ──
    {
        "id": 40,
        "name": "周文武",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任县委书记",
        "current_org": "（已离任）",
        "source": "https://www.163.com/search?keyword=周文武当选中共珙县县委书记",
    },
]

# ── Organizations ────────────────────────────────────────────────────────
orgs = [
    {"id": 1, "name": "中共珙县委员会", "type": "党委", "level": "县级", "parent": "中共宜宾市委员会", "location": "宜宾市珙县"},
    {"id": 2, "name": "珙县人民政府", "type": "政府", "level": "县级", "parent": "宜宾市人民政府", "location": "宜宾市珙县"},
    {"id": 3, "name": "珙县政协", "type": "政协", "level": "县级", "parent": "", "location": "宜宾市珙县"},
]

# ── Positions ────────────────────────────────────────────────────────────
positions = [
    # 沙之杰 — 县委书记
    {"person_id": 10, "org_id": 1, "title": "县委书记", "start_date": "2024-11", "end_date": "", "rank": "正县级", "note": "2024年11月任珙县县委书记（金台资讯）"},
    # 高果
    {"person_id": 11, "org_id": 1, "title": "县委副书记", "start_date": "2023-12", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "县长、县政府党组书记", "start_date": "2023-12", "end_date": "", "rank": "正县级", "note": ""},
    # 高果早期职务
    {"person_id": 11, "org_id": 2, "title": "县政府办副主任（江安县）", "start_date": "", "end_date": "", "rank": "副科级", "note": "江安县政府办"},
    {"person_id": 11, "org_id": 2, "title": "四面山镇党委副书记、镇长", "start_date": "", "end_date": "", "rank": "正科级", "note": "江安县四面山镇"},
    {"person_id": 11, "org_id": 1, "title": "四面山镇党委书记、人大主席", "start_date": "", "end_date": "", "rank": "正科级", "note": "江安县四面山镇"},
    {"person_id": 11, "org_id": 1, "title": "县委组织部副部长、老干部局局长", "start_date": "", "end_date": "", "rank": "正科级", "note": "江安县委"},
    {"person_id": 11, "org_id": 3, "title": "共青团宜宾市委副书记、党组成员", "start_date": "", "end_date": "", "rank": "副县级", "note": "宜宾市"},
    {"person_id": 11, "org_id": 1, "title": "翠屏区委常委、组织部部长", "start_date": "", "end_date": "", "rank": "副县级", "note": "兼任区委党校校长、区直机关工委书记"},
    {"person_id": 11, "org_id": 2, "title": "翠屏区委常委、常务副区长", "start_date": "", "end_date": "", "rank": "副县级", "note": "翠屏区政府"},
    {"person_id": 11, "org_id": 1, "title": "翠屏区委副书记", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "宜宾市人民政府副秘书长（兼）", "start_date": "", "end_date": "2023-12", "rank": "正县级", "note": "兼市信访局党组书记、局长"},
    # 罗道戡
    {"person_id": 15, "org_id": 1, "title": "县委常委", "start_date": "2026-05", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "常务副县长", "start_date": "2026-05", "end_date": "", "rank": "副县级", "note": "接替龚勋"},
    # 侯杰
    {"person_id": 16, "org_id": 1, "title": "县委专职副书记", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    # 谢建文
    {"person_id": 20, "org_id": 2, "title": "副县长", "start_date": "2025-12", "end_date": "", "rank": "副县级", "note": "负责交通、自然资源、住建、征地等"},
    # 贾泽鑫
    {"person_id": 21, "org_id": 2, "title": "副县长", "start_date": "2026-06", "end_date": "", "rank": "副县级", "note": "负责卫健、教育体育、民政、退役军人等；兼巡场镇党委书记"},
    # 谢国刚等 — 角色待确认
    {"person_id": 30, "org_id": 1, "title": "县领导", "start_date": "", "end_date": "", "rank": "", "note": "参加接访活动，具体职务待查"},
    {"person_id": 31, "org_id": 1, "title": "县领导", "start_date": "", "end_date": "", "rank": "", "note": "参加接访活动，具体职务待查"},
    {"person_id": 32, "org_id": 1, "title": "县领导", "start_date": "", "end_date": "", "rank": "", "note": "陪同县委书记调研，具体职务待查"},
    # 李智 — 县政协主席
    {"person_id": 35, "org_id": 3, "title": "县政协主席", "start_date": "", "end_date": "", "rank": "正县级", "note": ""},
    # 周文武 — 前任县委书记
    {"person_id": 40, "org_id": 1, "title": "县委书记", "start_date": "2021-09", "end_date": "2024-11", "rank": "正县级", "note": "2021年9月当选珙县县委书记"},
]

# ── Relationships ────────────────────────────────────────────────────────
relationships = [
    # 党政一把手
    {"person_a": 10, "person_b": 11, "type": "党政搭档", "context": "县委书记—县长搭档", "overlap_org": "中共珙县委员会", "overlap_period": "2024-11至今"},
    # 县委副书记—县长
    {"person_a": 11, "person_b": 16, "type": "党政搭档", "context": "县长—县委专职副书记", "overlap_org": "中共珙县委员会", "overlap_period": ""},
    # 县长—常务副县长
    {"person_a": 11, "person_b": 15, "type": "上下级", "context": "县长—常务副县长", "overlap_org": "珙县人民政府", "overlap_period": "2026-05至今"},
    # 县长—副县长
    {"person_a": 11, "person_b": 20, "type": "上下级", "context": "县长—副县长", "overlap_org": "珙县人民政府", "overlap_period": "2025-12至今"},
    {"person_a": 11, "person_b": 21, "type": "上下级", "context": "县长—副县长（乡镇党委书记兼）", "overlap_org": "珙县人民政府", "overlap_period": "2026-06至今"},
    # 前后任（县委书记）
    {"person_a": 40, "person_b": 10, "type": "前后任", "context": "周文武（2021-2024）→ 沙之杰（2024-迄今）", "overlap_org": "中共珙县委员会", "overlap_period": "2024年11月"},
    # 县委书记—其他参加活动的县领导
    {"person_a": 10, "person_b": 30, "type": "上下级", "context": "县委书记—县领导（共同参加接访）", "overlap_org": "中共珙县委员会", "overlap_period": "2026-07"},
    {"person_a": 10, "person_b": 31, "type": "上下级", "context": "县委书记—县领导（共同参加接访）", "overlap_org": "中共珙县委员会", "overlap_period": "2026-07"},
    {"person_a": 10, "person_b": 32, "type": "上下级", "context": "县委书记—县领导（陪同暗访督导）", "overlap_org": "中共珙县委员会", "overlap_period": "2026-06"},
]

if __name__ == "__main__":
    import os
    base = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    run_build(
        slug=slug,
        persons=persons,
        organizations=orgs,
        positions=positions,
        relationships=relationships,
        db_path=os.path.join(base, "珙县_network.db"),
        gexf_path=os.path.join(base, "珙县_network.gexf"),
        overwrite=True,
    )
    print("Done: 珙县 network built successfully!")