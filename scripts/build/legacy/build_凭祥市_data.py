#!/usr/bin/env python3
"""凭祥市领导班子关系网络 build script.

任务: guangxi_凭祥市 (广西壮族自治区崇左市凭祥市, 县级市)
目标: 市委书记 & 市长
数据基准: 截至 2026-08-05
运行: python3 data/tmp/guangxi_凭祥市/build_凭祥市_data.py
"""

import sqlite3
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from gov_relation.runner import run_build

# ── 目录（暂存区）─────────────────────────────────────────
STAGING = Path(__file__).resolve().parent
DB_PATH = STAGING / "凭祥市_network.db"
GEXF_PATH = STAGING / "凭祥市_network.gexf"

# ══════════════════════════════════════════════════════════════
# 人员 (persons)
# ══════════════════════════════════════════════════════════════
persons = [
    {
        "id": 1,
        "name": "何永恒",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年5月",
        "birthplace": "广西崇左市扶绥县",
        "education": "广西区委党校研究生学历",
        "party_join": "1999年6月",
        "work_start": "2000年7月",
        "current_post": "凭祥市委书记",
        "current_org": "中共凭祥市委员会",
        "source": "凭祥市融媒体中心(2026-07-23党代会/八一走访);网易号探秘桂北(2025-02-07);崇左市委组织部任前公示(2023-07-11)",
    },
    {
        "id": 2,
        "name": "左涛",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "凭祥市委副书记、市长",
        "current_org": "凭祥市人民政府",
        "source": "凭祥市融媒体中心(2026-07-22四家班子联席会/07-27高质量发展/07-30八一慰问);扶绥县政府(扶政发〔2023〕9号)",
    },
    {
        "id": 3,
        "name": "武晓辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年2月",
        "birthplace": "河北邯郸",
        "education": "南京理工大学博士研究生",
        "party_join": "1998年6月",
        "work_start": "2007年7月",
        "current_post": "梧州市政府党组成员、副市长(原凭祥市委书记)",
        "current_org": "梧州市人民政府",
        "source": "广西县人民政府网(2026-03-19);梧州发布(2026-03-09)",
    },
    {
        "id": 4,
        "name": "贾耀锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987年6月",
        "birthplace": "河北任县",
        "education": "上海交通大学硕士(管理科学与工程)",
        "party_join": "中共党员",
        "work_start": "2012年",
        "current_post": "原凭祥市委副书记、市长(2026中交接)",
        "current_org": "",
        "source": "凭祥市政府工作报告(2026-05-19);凭祥市纪检监察网(2026-06-08);新京报(2022-07-16)",
    },
    {
        "id": 5,
        "name": "黄爽",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "凭祥市委副书记",
        "current_org": "中共凭祥市委员会",
        "source": "凭祥市融媒体中心(2026-07-22党代会/07-22四家班子联席会/07-27高质量发展);凭政发〔2025〕1号",
    },
    {
        "id": 6,
        "name": "覃志雄",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "凭祥市人大常委会主任",
        "current_org": "凭祥市人大常委会",
        "source": "凭祥市融媒体中心(2026-07-22/07-30八一慰问);凭祥市纪检监察公报(2026-06-08)",
    },
    {
        "id": 7,
        "name": "张儒聪",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "凭祥市政协党组书记",
        "current_org": "政协凭祥市委员会",
        "source": "凭祥市融媒体中心(2026-07-22/07-30八一慰问)",
    },
    {
        "id": 8,
        "name": "潘国威",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "凭祥市常务副市长",
        "current_org": "凭祥市人民政府",
        "source": "凭祥市政府门户领导之窗(2026-06-04);凭祥市融媒体中心(2026-07-22/07-27)",
    },
    {
        "id": 9,
        "name": "刘德崇",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "凭祥市副市长",
        "current_org": "凭祥市人民政府",
        "source": "凭祥市政府门户领导之窗(2026-07-27);凭祥市融媒体中心(2026-07-27)",
    },
    {
        "id": 10,
        "name": "陆万敏",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "凭祥市副市长兼市公安局局长",
        "current_org": "凭祥市人民政府",
        "source": "凭祥市政府门户领导之窗(2025-03-06);凭政发〔2025〕1号",
    },
    {
        "id": 11,
        "name": "何春华",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "凭祥市副市长",
        "current_org": "凭祥市人民政府",
        "source": "凭祥市政府门户领导之窗(2025-03-06);凭政发〔2025〕1号",
    },
    {
        "id": 12,
        "name": "黄荣荣",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原凭祥市常务副市长(2025)",
        "current_org": "",
        "source": "凭政发〔2025〕1号(2025-01-06)",
    },
    {
        "id": 13,
        "name": "罗国谣",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原凭祥市委副书记(2026-06)",
        "source": "凭祥市纪检监察网(2026-06-08)",
    },
    {
        "id": 14,
        "name": "龚志卫",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "凭祥市领导",
        "current_org": "中共凭祥市委员会",
        "source": "凭祥市融媒体中心(2026-07-22/07-30八一慰问)",
    },
]

# ══════════════════════════════════════════════════════════════
# 机构 (organizations)
# ══════════════════════════════════════════════════════════════
organizations = [
    {
        "id": 1,
        "name": "中共凭祥市委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共崇左市委员会",
        "location": "广西壮族自治区崇左市凭祥市",
    },
    {
        "id": 2,
        "name": "凭祥市人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "崇左市人民政府",
        "location": "广西壮族自治区崇左市凭祥市",
    },
    {
        "id": 3,
        "name": "凭祥市人大常委会",
        "type": "人大",
        "level": "县处级",
        "parent": "凭祥市",
        "location": "广西壮族自治区崇左市凭祥市",
    },
    {
        "id": 4,
        "name": "政协凭祥市委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "凭祥市",
        "location": "广西壮族自治区崇左市凭祥市",
    },
    {
        "id": 5,
        "name": "中共凭祥市纪律检查委员会",
        "type": "纪委",
        "level": "县处级",
        "parent": "中共凭祥市委员会",
        "location": "凭祥市",
    },
    {
        "id": 6,
        "name": "凭祥市公安局",
        "type": "政府",
        "level": "县处级",
        "parent": "凭祥市人民政府",
        "location": "凭祥市",
    },
    {
        "id": 7,
        "name": "崇左市人民政府",
        "type": "政府",
        "level": "厅局级",
        "parent": "广西壮族自治区人民政府",
        "location": "广西壮族自治区崇左市",
    },
    {
        "id": 8,
        "name": "崇左市住房和城乡建设局",
        "type": "政府",
        "level": "县处级",
        "parent": "崇左市人民政府",
        "location": "崇左市",
    },
    {
        "id": 9,
        "name": "中共扶绥县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共崇左市委员会",
        "location": "崇左市扶绥县",
    },
    {
        "id": 10,
        "name": "扶绥县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "崇左市人民政府",
        "location": "崇左市扶绥县",
    },
    {
        "id": 11,
        "name": "梧州市人民政府",
        "type": "政府",
        "level": "厅局级",
        "parent": "广西壮族自治区人民政府",
        "location": "广西壮族自治区梧州市",
    },
    {
        "id": 12,
        "name": "凭祥市人民法院",
        "type": "司法机关",
        "level": "县处级",
        "parent": "崇左市中级人民法院",
        "location": "凭祥市",
    },
]

# ══════════════════════════════════════════════════════════════
# 任职 (positions)
# ══════════════════════════════════════════════════════════════
positions = [
    # 何永恒 (1)
    {"person_id": 1, "org_id": 1, "title": "凭祥市委书记", "start_date": "2026-03", "end_date": "present", "rank": "县处级正职", "note": "约2026年3月接武晓辉任市委书记;新一届市委班子2026-07-22产生"},
    {"person_id": 1, "org_id": 7, "title": "崇左市人民政府秘书长、办公室主任", "start_date": "2025-01", "end_date": "2026-02", "rank": "正处级", "note": "2025-01免住建局长后任市政府秘书长"},
    {"person_id": 1, "org_id": 8, "title": "崇左市住房和城乡建设局党组书记、局长", "start_date": "2023-08", "end_date": "2025-01", "rank": "正处级", "note": "2023-07公示,2023-08任命"},
    {"person_id": 1, "org_id": 9, "title": "扶绥县委常委、常务副县长/政法委书记", "start_date": "2020-02", "end_date": "2023-08", "rank": "副处级", "note": "2020-02政法委书记,2022-08常务副县长"},
    {"person_id": 1, "org_id": 10, "title": "扶绥县副县长", "start_date": "2017-12", "end_date": "2020-02", "rank": "副处级", "note": ""},
    # 左涛 (2)
    {"person_id": 2, "org_id": 1, "title": "凭祥市委副书记", "start_date": "2026-06", "end_date": "present", "rank": "县处级", "note": "2026-07起与市委书记何永恒并列居首;市长(代市长)为强推断"},
    {"person_id": 2, "org_id": 10, "title": "扶绥县委常委、常务副县长", "start_date": "2023", "end_date": "2026", "rank": "副处级", "note": "2023-11分工通知确认(扶政发〔2023〕9号)"},
    # 武晓辉 (3)
    {"person_id": 3, "org_id": 11, "title": "梧州市政府党组成员、副市长", "start_date": "2026-03", "end_date": "present", "rank": "厅局级副职", "note": "2026-02公示,2026-03调任"},
    {"person_id": 3, "org_id": 1, "title": "凭祥市委书记", "start_date": "2022-06", "end_date": "2026-02", "rank": "县处级正职", "note": "二级巡视员"},
    {"person_id": 3, "org_id": 2, "title": "凭祥市委副书记、市长", "start_date": "2017-07", "end_date": "2022-06", "rank": "县处级正职", "note": "兼凭祥综合保税区管委会副主任"},
    # 贾耀锋 (4)
    {"person_id": 4, "org_id": 2, "title": "凭祥市委副书记、市长", "start_date": "2022-07", "end_date": "2026-06", "rank": "县处级正职", "note": "2022-07任市委副书记、市政府主要领导;2026-05作政府工作报告;2026-06-08仍为市长"},
    # 黄爽 (5)
    {"person_id": 5, "org_id": 1, "title": "凭祥市委副书记", "start_date": "2026", "end_date": "present", "rank": "县处级", "note": "2026-07新班子"},
    {"person_id": 5, "org_id": 2, "title": "凭祥市副市长(挂职)", "start_date": "2025-01", "end_date": "2025", "rank": "副处级", "note": "凭政发〔2025〕1号,负责驻村工作队"},
    # 覃志雄 (6)
    {"person_id": 6, "org_id": 3, "title": "凭祥市人大常委会主任", "start_date": "2026", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 张儒聪 (7)
    {"person_id": 7, "org_id": 4, "title": "凭祥市政协党组书记", "start_date": "2026", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 潘国威 (8)
    {"person_id": 8, "org_id": 2, "title": "凭祥市常务副市长", "start_date": "2026-06", "end_date": "present", "rank": "副处级", "note": "2026-06官网领导之窗更新"},
    # 刘德崇 (9)
    {"person_id": 9, "org_id": 2, "title": "凭祥市副市长", "start_date": "2026-07", "end_date": "present", "rank": "副处级", "note": ""},
    # 陆万敏 (10)
    {"person_id": 10, "org_id": 2, "title": "凭祥市副市长、市公安局局长", "start_date": "2025-03", "end_date": "present", "rank": "副处级", "note": ""},
    # 何春华 (11)
    {"person_id": 11, "org_id": 2, "title": "凭祥市副市长", "start_date": "2025-03", "end_date": "present", "rank": "副处级", "note": ""},
    # 黄荣荣 (12)
    {"person_id": 12, "org_id": 2, "title": "凭祥市常务副市长", "start_date": "2025-01", "end_date": "2025", "rank": "副处级", "note": "凭政发〔2025〕1号"},
    # 罗国谣 (13)
    {"person_id": 13, "org_id": 1, "title": "凭祥市委副书记", "start_date": "2026-06", "end_date": "2026-06", "rank": "县处级", "note": "2026-06-08出席警示教育会议"},
    {"person_id": 14, "org_id": 1, "title": "凭祥市领导(市委常委)", "start_date": "2026", "end_date": "present", "rank": "县处级", "note": "2026-07出席八一慰问"},
]

# ══════════════════════════════════════════════════════════════
# 关系 (relationships)
# ══════════════════════════════════════════════════════════════
relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭班子", "context": "市委书记—市长/市委副书记,同为核心领导", "overlap_org": "凭祥市四家班子", "overlap_period": "2026-07—present"},
    {"person_a": 1, "person_b": 3, "type": "前任继任", "context": "何永恒接替武晓辉担任凭祥市委书记", "overlap_org": "中共凭祥市委员会", "overlap_period": "2026-03"},
    {"person_a": 2, "person_b": 4, "type": "predecessor_successor", "context": "左涛接替贾耀锋任市长(代市长,推断)", "overlap_org": "凭祥市人民政府", "overlap_period": "2026-07"},
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "书记-专职副书记同班", "overlap_org": "中共凭祥市委员会", "overlap_period": "2026-07—present"},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "书记-人大主任四家班子", "overlap_org": "凭祥市四家班子", "overlap_period": "2026-07—present"},
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "书记-政协党组书记四家班子", "overlap_org": "凭祥市四家班子", "overlap_period": "2026-07—present"},
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "书记-常务副市长", "overlap_org": "凭祥市四家班子", "overlap_period": "2026-07—present"},
    {"person_a": 1, "person_b": 14, "type": "overlap", "context": "书记-市委常委", "overlap_org": "中共凭祥市委员会", "overlap_period": "2026-07"},
    {"person_a": 1, "person_b": 13, "type": "overlap", "context": "书记-前任副书记同台会议", "overlap_org": "凭祥市四家班子", "overlap_period": "2026-06"},
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "双副书记同班", "overlap_org": "中共凭祥市委员会", "overlap_period": "2026-07—present"},
    {"person_a": 8, "person_b": 9, "type": "overlap", "context": "常务副市长-副市长同政府班子", "overlap_org": "凭祥市人民政府", "overlap_period": "2026-07—present"},
    {"person_a": 10, "person_b": 8, "type": "overlap", "context": "副市长(公安)-常务副市长同班", "overlap_org": "凭祥市人民政府", "overlap_period": "2026—present"},
    {"person_a": 1, "person_b": 12, "type": "overlap", "context": "何永恒任扶绥常委时与黄荣荣(前常委副市长)同系统(推断弱)", "overlap_org": "扶绥县", "overlap_period": "2020-2023"},
    {"person_a": 3, "person_b": 4, "type": "predecessor_successor", "context": "武晓辉书记任上时段贾耀锋任市长;书记-市长搭班子", "overlap_org": "凭祥市四家班子", "overlap_period": "2022-06-2026-02"},
]


def main() -> None:
    run_build(
        slug="凭祥市",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    conn = sqlite3.connect(str(DB_PATH))
    for t in ("persons", "organizations", "positions", "relationships"):
        n = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"{t}: {n}")
    conn.close()


if __name__ == "__main__":
    main()