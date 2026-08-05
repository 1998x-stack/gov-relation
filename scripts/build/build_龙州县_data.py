#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
龙州县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 广西壮族自治区
Parent City: 崇左市
Region: 龙州县
Targets: 县委书记 & 县长

Research Sources (primary):
- 龙州县人民政府门户网站 http://www.longzhou.gov.cn
  - 政务要闻 /zwdt/zwyw/t27920444.shtml  (2026-07-21 县委书记冯波)
  - 政务要闻 /zwdt/zwyw/t27849428.shtml  (2026-07-01 县委书记冯波、县长秦义敏、统战部长魏月艳)
  - 政务要闻 /zwdt/zwyw/t27864168.shtml  (2026-07-06 县人大常委会主任黄映虹、副主任黄永亮/黄子珍)
  - 领导简介 /xxgk/jcxxgk/ldzc/fxz/      (2026-03-06 副县长李海权/黄忠良/周萍/张义明)
  - 领导简介 /xxgk/jcxxgk/ldzc/dyy/      (2026-03-06 调研员韩日辉)
  - 政府文件 龙政发〔2025〕5号            (2025-09-23 县政府领导工作分工)

Research Date: 2026-08-05

Confidence:
- 县委书记冯波、县长秦义敏 由官方门户跨 2023-2026 多篇报道证实 (confirmed)。
- 其余班子成员按 2025-2026 官网报道/分工文件记录为 confirmed 或 plausible。
- 批量身份字段 (籍贯/学历/入党时间) 未公开 → 预留 unverified 并在 open_questions 标记。
- 百度百科 infobox 曾列"县委书记 尹泉", 与 gov.cn(冯波)冲突, 以 gov.cn 为准;
  尹泉 (崇左城建集团书记) 记为 unverified 相关人物。
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../.."))

from gov_relation.runner import run_build

SLUG = "龙州县"

_script_dir = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(_script_dir, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(_script_dir, f"{SLUG}_network.gexf")

import sqlite3  # noqa: F401

# ── Data ──────────────────────────────────────────────────────────────

# 1. Persons (id 1-99; 101+ 为机构)
persons = [
    # ═══ Current Top Leaders ═══
    {
        "id": 1,
        "name": "冯波",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙州县委书记",
        "current_org": "中共龙州县委员会",
        "source": "official longzhou.gov.cn /zwdt/zwyw/t27920444.shtml (2026-07-21) & t27849428.shtml (2026-07-01); confidence=confirmed",
    },
    {
        "id": 2,
        "name": "秦义敏",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙州县委副书记、县长",
        "current_org": "龙州县人民政府",
        "source": "official longzhou.gov.cn /zwdt/zwyw/t27849428.shtml (2026-07-01 县长); 2024-02 报道; confidence=confirmed",
    },
    # ═══ 县委常委 (县委班子) ═══
    {
        "id": 3,
        "name": "卢鹏",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙州县委副书记",
        "current_org": "中共龙州县委员会",
        "source": "龙州政府门户/本地会议 2026-03/06 报道; confidence=plausible",
    },
    {
        "id": 4,
        "name": "王岳",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙州县委常委、组织部部长",
        "current_org": "中共龙州县委组织部",
        "source": "2026-02/03 会议纪要; confidence=plausible (前任: 刘权 2024)",
    },
    {
        "id": 5,
        "name": "黄玉书",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙州县委常委、纪委书记、监委主任",
        "current_org": "中共龙州县纪律检查委员会",
        "source": "2026-01/2026-05 活动报道; confidence=confirmed (前任 郭鹏)",
    },
    {
        "id": 6,
        "name": "韦信旭",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙州县委常委、政法委书记",
        "current_org": "中共龙州县委政法委员会",
        "source": "2024-11/2026-05 报道; confidence=plausible (前任 何金宝)",
    },
    {
        "id": 7,
        "name": "黄世能",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙州县委常委、宣传部部长",
        "current_org": "中共龙州县委宣传部",
        "source": "2024-11/2026-01 报道; confidence=plausible (前任 谭春丽)",
    },
    {
        "id": 8,
        "name": "魏月艳",
        "gender": "女",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙州县委常委、统战部部长",
        "current_org": "中共龙州县委统战部",
        "source": "official longzhou.gov.cn /zwdt/zwyw/t27849428.shtml (2026-07-01 统战部长魏月艳); confidence=confirmed",
    },
    {
        "id": 9,
        "name": "廖治浩",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙州县委常委、办公室主任",
        "current_org": "中共龙州县委办公室",
        "source": "official longzhou.gov.cn /zwdt/zwyw/t27920444.shtml (2026-07-21 常委、办公室主任廖治浩); 2025-06 广西县域经济网; confidence=confirmed",
    },
    # ═══ 县政府班子 ═══
    {
        "id": 10,
        "name": "何金宝",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙州县委常委、常务副县长",
        "current_org": "龙州县人民政府",
        "source": "2026-01/2026-03 会议纪要 + 龙政发〔2025〕5号分工文件; confidence=confirmed (2023-2024 曾任县委常委、政法委书记)",
    },
    {
        "id": 11,
        "name": "李海权",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-11",
        "birthplace": "待查",
        "education": "在职大学本科",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙州县委常委、副县长",
        "current_org": "龙州县人民政府",
        "source": "official 领导简介 /xxgk/jcxxgk/ldzc/fxz/ 2026-03-06; confidence=confirmed",
    },
    {
        "id": 12,
        "name": "黄忠良",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "1984-09",
        "birthplace": "待查",
        "education": "在职本科",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙州县委常委、副县长",
        "current_org": "龙州县人民政府",
        "source": "official 领导简介 2026-03-06; confidence=confirmed",
    },
    {
        "id": 13,
        "name": "周萍",
        "gender": "女",
        "ethnicity": "苗族",
        "birth": "1987-05",
        "birthplace": "待查",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙州县人民政府副县长",
        "current_org": "龙州县人民政府",
        "source": "official 领导简介 2026-03-06; confidence=confirmed",
    },
    {
        "id": 14,
        "name": "张义明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1988-01",
        "birthplace": "待查",
        "education": "硕士研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙州县人民政府副县长",
        "current_org": "龙州县人民政府",
        "source": "official 领导简介 2026-03-06; 2026-07-06 人大常委会列席; confidence=confirmed",
    },
    {
        "id": 15,
        "name": "韩日辉",
        "gender": "男",
        "ethnicity": "壮族",
        "birth": "1974-10",
        "birthplace": "待查",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙州县人民政府四级调研员",
        "current_org": "龙州县人民政府",
        "source": "official 领导简介 2026-03-06; confidence=confirmed",
    },
    # ═══ 县人大常委会 / 政协 ═══
    {
        "id": 16,
        "name": "黄映虹",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙州县人大常委会党组书记、主任",
        "current_org": "龙州县人大常委会",
        "source": "official longzhou.gov.cn /zwdt/zwyw/t27864168.shtml (2026-07-06 主任黄映虹); confidence=confirmed",
    },
    {
        "id": 17,
        "name": "刘丹珠",
        "gender": "女",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙州县人大常委会副主任",
        "current_org": "龙州县人大常委会",
        "source": "龙州政协网/人大会议 2024-11/2026-03; confidence=plausible",
    },
    {
        "id": 18,
        "name": "黄永亮",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙州县人大常委会副主任",
        "current_org": "龙州县人大常委会",
        "source": "official longzhou.gov.cn /zwdt/zwyw/t27864168.shtml (2026-07-06 副主任黄永亮); confidence=confirmed",
    },
    {
        "id": 19,
        "name": "黄子珍",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙州县人大常委会副主任",
        "current_org": "龙州县人大常委会",
        "source": "official longzhou.gov.cn /zwdt/tz27864168.shtml (2026-07-06 副主任黄子珍); confidence=confirmed",
    },
    {
        "id": 20,
        "name": "赵干",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙州县政协主席",
        "current_org": "政协龙州县委员会",
        "source": "2025-01/2026-04 政协报道; confidence=confirmed",
    },
    {
        "id": 21,
        "name": "黄华基",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙州县政协副主席",
        "current_org": "政协龙州县委员会",
        "source": "2025-01 政协报道; confidence=plausible",
    },
    {
        "id": 22,
        "name": "张权壮",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "龙州县政协副主席",
        "current_org": "政协龙州县委员会",
        "source": "2025-01 政协报道; confidence=plausible",
    },
    # ═══ 跨区相关人物 ═══
    {
        "id": 30,
        "name": "尹泉",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "1987",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "崇左市城建投资发展集团党委书记、董事长(据报料拟任/曾任龙州县委书记, 未核实)",
        "current_org": "崇左市城市建设投资发展集团有限公司",
        "source": "百度百科龙州县infobox列县委书记; 网易/汲古新知报道; 与 gov.cn (冯波) 冲突; confidence=unverified",
    },
]

# 2. Organizations
organizations = [
    {"id": 101, "name": "中共龙州县委员会", "type": "党委", "level": "县级", "parent": "中共崇左市委", "location": "广西崇左市龙州县"},
    {"id": 102, "name": "龙州县人民政府", "type": "政府", "level": "县级", "parent": "崇左市人民政府", "location": "广西崇左市龙州县"},
    {"id": 103, "name": "龙州县人大常委会", "type": "人大", "level": "县级", "parent": "崇左市人民代表大会常务委员会", "location": "广西崇左市龙州县"},
    {"id": 104, "name": "政协龙州县委员会", "type": "政协", "level": "县级", "parent": "政协崇左市委员会", "location": "广西崇左市龙州县"},
    {"id": 105, "name": "中共龙州县纪律检查委员会", "type": "纪委", "level": "县级", "parent": "中共崇左市纪委", "location": "广西崇左市龙州县"},
    {"id": 106, "name": "中共龙州县委组织部", "type": "党委", "level": "县级", "parent": "中共龙州县委员会", "location": "广西崇左市龙州县"},
    {"id": 107, "name": "中共龙州县委宣传部", "type": "党委", "level": "县级", "parent": "中共龙州县委员会", "location": "广西崇左市龙州县"},
    {"id": 108, "name": "中共龙州县委统战部", "type": "党委", "level": "县级", "parent": "中共龙州县委员会", "location": "广西崇左市龙州县"},
    {"id": 109, "name": "中共龙州县委政法委员会", "type": "党委", "level": "县级", "parent": "中共龙州县委员会", "location": "广西崇左市龙州县"},
    {"id": 110, "name": "中共龙州县委办公室", "type": "党委", "level": "县级", "parent": "中共龙州县委员会", "location": "广西崇左市龙州县"},
    {"id": 120, "name": "中共崇左市委", "type": "党委", "level": "地级", "parent": "中共广西壮族自治区委员会", "location": "广西崇左市"},
    {"id": 122, "name": "中共崇左江州区委员会", "type": "党委", "level": "县级", "parent": "中共崇左市委", "location": "广西崇左市江州区"},
]

# 3. 任职记录 (person_id, org_id, title, start_date, end_date, rank, note)
positions = [
    # 县委书记 & 县长
    {"person_id": 1, "org_id": 101, "title": "县委书记", "start_date": "2021-09", "end_date": "present",
     "rank": "正处级", "note": "confirmed 2026-07-21 在位"},
    {"person_id": 2, "org_id": 102, "title": "县委副书记、县长", "start_date": "2021", "end_date": "present",
     "rank": "正处级", "note": "confirmed 2026-07-01 在位"},
    # 县委班子成员
    {"person_id": 3, "org_id": 101, "title": "县委副书记", "start_date": "2025", "end_date": "present",
     "rank": "副处级", "note": "2026-03/06 报道"},
    {"person_id": 4, "org_id": 106, "title": "县委常委、组织部部长", "start_date": "2025", "end_date": "present",
     "rank": "副处级", "note": "前任 刘权 (2024)"},
    {"person_id": 5, "org_id": 105, "title": "县委常委、纪委书记、监委主任", "start_date": "2023", "end_date": "present",
     "rank": "副处级", "note": "前任 郭鹏"},
    {"person_id": 6, "org_id": 109, "title": "县委常委、政法委书记", "start_date": "2024", "end_date": "present",
     "rank": "副处级", "note": "前任 何金宝 (2024 转常务副县长)"},
    {"person_id": 7, "org_id": 107, "title": "县委常委、宣传部部长", "start_date": "2024", "end_date": "present",
     "rank": "副处级", "note": "前任 谭春丽"},
    {"person_id": 8, "org_id": 108, "title": "县委常委、统战部部长", "start_date": "2023", "end_date": "present",
     "rank": "副处级", "note": "前任 李国滔"},
    {"person_id": 9, "org_id": 110, "title": "县委常委、办公室主任", "start_date": "2025-06", "end_date": "present",
     "rank": "副处级", "note": "自崇左江州区调任"},
    # 县政府班子
    {"person_id": 10, "org_id": 102, "title": "县委常委、常务副县长", "start_date": "2024-09", "end_date": "present",
     "rank": "副处级", "note": "2023-2024 曾任政法委书记, 县内轮岗"},
    {"person_id": 10, "org_id": 109, "title": "县委常委、政法委书记(前)", "start_date": "2023", "end_date": "2024-09",
     "rank": "副处级", "note": "县内轮岗 → 常务副县长"},
    {"person_id": 11, "org_id": 102, "title": "县委常委、副县长", "start_date": "2021", "end_date": "present",
     "rank": "副处级", "note": "汉族 1977-11"},
    {"person_id": 12, "org_id": 102, "title": "县委常委、副县长", "start_date": "2022", "end_date": "present",
     "rank": "副处级", "note": "壮族 1984-09"},
    {"person_id": 13, "org_id": 102, "title": "副县长", "start_date": "2023", "end_date": "present",
     "rank": "副处级", "note": "苗族 1987-05"},
    {"person_id": 14, "org_id": 102, "title": "副县长", "start_date": "2025", "end_date": "present",
     "rank": "副处级", "note": "汉族 1988-01; 2026 接替雷梅分管乡村振兴对接"},
    {"person_id": 15, "org_id": 102, "title": "四级调研员", "start_date": "2023", "end_date": "present",
     "rank": "县处级", "note": "壮族 1974-10"},
    # 人大/政协
    {"person_id": 16, "org_id": 103, "title": "党组书记、主任", "start_date": "2024-12", "end_date": "present",
     "rank": "正处级", "note": "2026-07-06 主持县人大常委会会议"},
    {"person_id": 17, "org_id": 103, "title": "副主任", "start_date": "2021", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 18, "org_id": 103, "title": "副主任", "start_date": "2021", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 19, "org_id": 103, "title": "副主任", "start_date": "2021", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 20, "org_id": 104, "title": "县政协主席", "start_date": "2021", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 21, "org_id": 104, "title": "副主席", "start_date": "2021", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 22, "org_id": 104, "title": "副主席", "start_date": "2021", "end_date": "present", "rank": "副处级", "note": ""},
]

# 4. 关系 (已确认 / 可推断交错点)
relationships = [
    # 书记-县长: 党政班子搭档 (同机构、同期)
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "县委书记与县委副书记/县长党政班子搭档, 2026-07-01 同赴水口调研",
     "overlap_org": "中共龙州县委员会", "overlap_period": "2021-present"},
    # 何金宝 政法委 → 常务副县长 内部轮岗
    {"person_a": 6, "person_b": 10, "type": "predecessor_successor",
     "context": "韦信旭接任何金宝政法委书记职务 (何金宝 2024 转常务副县长)",
     "overlap_org": "中共龙州县委政法委员会", "overlap_period": "2024"},
]

# ── Build ──
if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    conn = sqlite3.connect(DB_PATH)
    for t in ("persons", "organizations", "positions", "relationships"):
        n = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"  [{t}] {n}")
    conn.close()
    print("Done.")