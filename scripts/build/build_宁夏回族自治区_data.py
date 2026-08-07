#!/usr/bin/env python3
"""宁夏回族自治区省级领导班子工作关系网络生成脚本.

基于宁夏新闻网 / 宁夏人大网 / 自治区人民政府门户 (nx.gov.cn) 领导简介、
维基百科/中国经济网人物档案、财新/澎湃人事观察等公开来源，构建宁夏回族
自治区党委、政府领导班子及前任主要领导、部分常委的 SQLite 数据库与
GEXF 关系图。

数据时间锚点：截至 2026-08（模拟环境日期）
- 现任党委书记：李邑飞（2024-06-28 任，另兼自治区人大常委会主任）
- 现任自治区主席：张雨浦（2022-05 任）
- 专职党委副书记：庄严
- 党委常委、组织部长：冼国义（2026-04 由宣传部长转任）
- 党委常委、政法委书记：朱天舒（2023-07 由甘肃兰州书记转任）

来源：
- 宁夏人民政府门户 www.nx.gov.cn（主席、副主席「领导信息」简介），2026-08 访问
- 宁夏新闻网书记简历 / 宁夏人大网 (nxrd.gov.cn) 2025-01 常委会主任选民
- 维基百科（李邑飞/张雨浦/庄严/冼国义/买彦州/梁言顺），2026-08 访问
- 中国经济网 宁夏党政领导人物库 district.ce.cn/zt/rwk/sf/nx/，2026-08 访问
- 财新 2026-04-12《五年弘六度履新 冼国义改兼任宁夏党委组织部长》；澎湃 2026-04 冼国义转任组织部长新闻
- 澎湃新闻 2026-06-03 维基百科（冼国义）等
"""

from __future__ import annotations

import sqlite3  # SQLite 标准库（经由 gov_relation.runner 落库）
import sys
from pathlib import Path

# 项目根目录（向上寻找包含 gov_relation/ 的仓库根，兼容 data/tmp/<task>/, scripts/build/, 仓库根 三种位置）
_HERE = Path(__file__).resolve().parent
_PROJECT_ROOT = next((p for p in _HERE.parents if (p / "gov_relation").is_dir()), _HERE)
sys.path.insert(0, str(_PROJECT_ROOT))

from gov_relation.runner import run_build

SLUG = "宁夏回族自治区"
DB_PATH = _HERE / "宁夏回族自治区_network.db"
GEXF_PATH = _HERE / "宁夏回族自治区_network.gexf"

# ── Persons ───────────────────────────────────────────────────────────────
PERSONS = [
    # 1 现任自治区党委书记
    {
        "id": 1,
        "name": "李邑飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1964-01",
        "birthplace": "云南墨江",
        "education": "昆明医学院卫生系卫生学专业本科；清华大学公共管理学院公共管理专业研究生、公共管理硕士",
        "party_join": "1984-10",
        "work_start": "1985-07",
        "current_post": "宁夏回族自治区党委书记、自治区人大常委会主任",
        "current_org": "中国共产党宁夏回族自治区委员会",
        "source": "https://nxnews.net/dz/ldhdj/lyf/lyfjj/202501/t20250122_5040861.html",
    },
    # 2 现任自治区主席
    {
        "id": 2,
        "name": "张雨浦",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1962-08",
        "birthplace": "山东长清",
        "education": "东北农学院农机系农业机械化专业本科；哈尔滨工业大学高级管理人员工商管理硕士、管理科学与工程博士",
        "party_join": "1984-07",
        "work_start": "1984-08",
        "current_post": "宁夏回族自治区主席",
        "current_org": "宁夏回族自治区人民政府",
        "source": "https://www.nx.gov.cn/zzsl/zyp/",
    },
    # 3 现任党委副书记
    {
        "id": 3,
        "name": "庄严",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967-08",
        "birthplace": "吉林农安",
        "education": "吉林财贸学院贸易经济系商业经济专业本科；吉林大学东北亚研究院世界经济专业在职研究生、经济学博士",
        "party_join": "1985-05",
        "work_start": "1988-07",
        "current_post": "宁夏回族自治区党委副书记",
        "current_org": "中国共产党宁夏回族自治区委员会",
        "source": "https://baike.so.com/doc/5363252-5598814.html",
    },
    # 4 现任党委常委、组织部部长
    {
        "id": 4,
        "name": "冼国义",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1970-04",
        "birthplace": "河北丰宁",
        "education": "西安交通大学社会科学系审计学本科；中央财政金融学院会计学硕士；中国人民大学国民经济管理系国民经济学博士",
        "party_join": "1997-12",
        "work_start": "1995-04",
        "current_post": "宁夏回族自治区党委常委、组织部部长",
        "current_org": "中国共产党宁夏回族自治区委员会",
        "source": "https://baike.baidu.com/item/冼国义",
    },
    # 5 现任党委常委、常务副主席
    {
        "id": 5,
        "name": "陈春平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-01",
        "birthplace": "",
        "education": "研究生，经济学博士",
        "party_join": "",
        "work_start": "",
        "current_post": "宁夏回族自治区党委常委、常务副主席",
        "current_org": "宁夏回族自治区人民政府",
        "source": "https://www.nx.gov.cn/zzsl/ccp/",
    },
    # 6 现任党委常委 / 副主席
    {
        "id": 6,
        "name": "买彦州",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1968-10",
        "birthplace": "河南",
        "education": "郑州大学电子工程系电子学与信息系统本科；北京邮电大学电子与信息工程专业硕士；教授级高级工程师",
        "party_join": "",
        "work_start": "1991-10",
        "current_post": "宁夏回族自治区党委常委、副主席",
        "current_org": "宁夏回族自治区人民政府",
        "source": "https://www.nx.gov.cn/zzsl/myz/wap.html",
    },
    # 7 现任党委常委、银川市委书记
    {
        "id": 7,
        "name": "赵旭辉",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "宁夏回族自治区党委常委、银川市委书记",
        "current_org": "中国共产党银川市委员会",
        "source": "https://district.ce.cn/zt/rwk/sz/nx/",
    },
    # 8 现任党委常委、纪委书记
    {
        "id": 8,
        "name": "艾俊涛",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "宁夏回族自治区党委常委、纪委书记、监委主任",
        "current_org": "中国共产党宁夏回族自治区纪律检查委员会",
        "source": "https://district.ce.cn/zt/rwk/sz/nx/",
    },
    # 9 现任副主席、公安厅厅长（吴澜）
    {
        "id": 9,
        "name": "吴澜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-05",
        "birthplace": "",
        "education": "大学，法学硕士",
        "party_join": "1994-07",
        "work_start": "1995-07",
        "current_post": "宁夏回族自治区副主席、自治区公安厅厅长",
        "current_org": "宁夏回族自治区人民政府",
        "source": "https://baike.baidu.com/item/吴澜/20295350",
    },
    # 10 前任党委书记（2022-03~2024-06）
    {
        "id": 10,
        "name": "梁言顺",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1962-12",
        "birthplace": "山东泰安",
        "education": "山东理工大学本科；辽宁大学经济学硕士；中共中央党校在职经济学博士",
        "party_join": "",
        "work_start": "",
        "current_post": "安徽省委书记（宁夏前任党委书记）",
        "current_org": "中国共产党安徽省委员会",
        "source": "https://zh.wikipedia.org/wiki/梁言顺",
    },
    # 11 前任自治区主席（咸辉）
    {
        "id": 11,
        "name": "咸辉",
        "gender": "女",
        "ethnicity": "回族",
        "birth": "1958-03",
        "birthplace": "甘肃定西",
        "education": "中央广播电视大学金融专业；研究生",
        "party_join": "1985-08",
        "work_start": "1975-03",
        "current_post": "（宁夏前任自治区主席，已卸任）",
        "current_org": "",
        "source": "https://zh.wikipedia.org/zh-cn/咸辉",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────
ORGANIZATIONS = [
    {"id": 1, "name": "中国共产党宁夏回族自治区委员会", "type": "党委", "level": "省级", "parent": "", "location": "宁夏回族自治区银川市"},
    {"id": 2, "name": "宁夏回族自治区人民政府", "type": "政府", "level": "省级", "parent": "", "location": "宁夏回族自治区银川市"},
    {"id": 3, "name": "宁夏回族自治区人大常委会", "type": "人大", "level": "省级", "parent": "", "location": "宁夏回族自治区银川市"},
    {"id": 4, "name": "宁夏回族自治区纪律检查委员会", "type": "纪委", "level": "省级", "parent": "中国共产党宁夏回族自治区委员会", "location": "宁夏回族自治区银川市"},
    {"id": 5, "name": "宁夏回族自治区公安厅", "type": "政府", "level": "副省级", "parent": "宁夏回族自治区人民政府", "location": "宁夏回族自治区银川市"},
    {"id": 6, "name": "中国共产党银川市委员会", "type": "党委", "level": "地厅级", "parent": "中国共产党宁夏回族自治区委员会", "location": "宁夏回族自治区银川市"},
    {"id": 7, "name": "中国共产党安徽省委员会", "type": "党委", "level": "省级", "parent": "", "location": "安徽省合肥市"},
]

# ── Positions ─────────────────────────────────────────────────────────────
POSITIONS = [
    {"person_id": 1, "org_id": 1, "title": "宁夏回族自治区党委书记", "start_date": "2024-06", "end_date": "present", "rank": "正省级", "note": "2024-06-28 中央决定任党委书记；2025-01-22 当选自治区人大常委会主任；此前任新疆党委副书记、兵团政委（正部长级）"},
    {"person_id": 1, "org_id": 3, "title": "自治区人大常委会主任", "start_date": "2025-01", "end_date": "present", "rank": "正省级", "note": "2025年1月当选"}, 
    {"person_id": 2, "org_id": 2, "title": "宁夏回族自治区主席", "start_date": "2022-05", "end_date": "present", "rank": "正省级", "note": "2022-05-09 代主席，2022-05-21 当选；此前 2021-08 任银川市委书记、2022-04 任区党委副书记"},
    {"person_id": 3, "org_id": 1, "title": "宁夏回族自治区党委副书记", "start_date": "2023-08", "end_date": "present", "rank": "副省级", "note": "2023-08 由西藏自治区党委常务副书记转任"},
    {"person_id": 4, "org_id": 1, "title": "自治区党委常委、组织部部长", "start_date": "2026-04", "end_date": "present", "rank": "副省级", "note": "2026-04 由党委宣传部长转任组织部长；此前任自治区副主席"}
    ,
    {"person_id": 5, "org_id": 2, "title": "自治区党委常委、常务副主席", "start_date": "2021", "end_date": "present", "rank": "副省级", "note": "兼区党委金融委员会办公室主任"},
    {"person_id": 6, "org_id": 2, "title": "自治区党委常委、副主席", "start_date": "2022-05", "end_date": "present", "rank": "副省级", "note": "此前任中国联通副总经理"},
    {"person_id": 7, "org_id": 6, "title": "自治区党委常委、银川市委书记", "start_date": "2021", "end_date": "present", "rank": "副省级", "note": ""},
    {"person_id": 8, "org_id": 4, "title": "自治区党委常委、纪委书记、监委主任", "start_date": "2019", "end_date": "present", "rank": "副省级", "note": ""},
    {"person_id": 9, "org_id": 5, "title": "自治区副主席、公安厅厅长", "start_date": "2025-11", "end_date": "present", "rank": "副省级", "note": "2025-02 任公安厅党委书记/厅长，2025-11 任自治区副主席"},
    {"person_id": 10, "org_id": 1, "title": "宁夏回族自治区党委书记（前任）", "start_date": "2022-03", "end_date": "2024-06", "rank": "正省级", "note": "2024-06 转任安徽省委书记"},
    {"person_id": 11, "org_id": 2, "title": "宁夏回族自治区主席（前任）", "start_date": "2016", "end_date": "2022-05", "rank": "正省级", "note": "卸任由张雨浦接任"},
]

# ── Relationships ─────────────────────────────────────────────────────────
RELATIONSHIPS = [
    # 李邑飞 — 张雨浦（现任党政一把手搭档）
    {"person_a": 1, "person_b": 2, "type": "搭档", "context": "李邑飞2024-06任宁夏党委书记后与主席张雨浦组成党政一把手搭档", "overlap_org": "宁夏回族自治区", "overlap_period": "2024-06至今"},
    # 李邑飞 — 前党委书记梁言顺（前任后任）
    {"person_a": 1, "person_b": 10, "type": "前任后任", "context": "李邑飞2024-06接任宁夏党委书记（接替转任安徽的梁言顺）", "overlap_org": "中国共产党宁夏回族自治区委员会", "overlap_period": "2024-06"},
    # 张雨浦 — 前主席咸辉（主席继任链）
    {"person_a": 2, "person_b": 11, "type": "前任后任", "context": "咸辉卸任宁夏主席，张雨浦2022-05继任", "overlap_org": "宁夏回族自治区人民政府", "overlap_period": "2022"},
    # 李邑飞 — 副书记庄严（上下级）
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "党委书记与专职副书记同属自治区党委常委会", "overlap_org": "中国共产党宁夏回族自治区委员会", "overlap_period": "2023-08至今"},
    # 李邑飞 — 组织部长冼国义（上下级）
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "党委书记与党委常委、组织部长同属党委常委会", "overlap_org": "中国共产党宁夏回族自治区委员会", "overlap_period": "present"},
    # 张雨浦 — 常务副主席陈春平（上下级 / 政府班子）
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "主席与常务副主席同属自治区政府班子", "overlap_org": "宁夏回族自治区人民政府", "overlap_period": "present"},
    # 张雨浦 — 副主席吴澜（上下级 / 政府班子）
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "主席与副主席、公安厅厅长同属政府班子", "overlap_org": "宁夏回族自治区人民政府", "overlap_period": "2025-11至今"},
    # 李邑飞 — 银川市委书记赵旭辉（上下级）
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "党委书记与党委常委、银川市委书记同属党委常委会", "overlap_org": "中国共产党宁夏回族自治区委员会", "overlap_period": "present"},
    # 李邑飞 — 纪委书记艾俊涛（上下级）
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "党委书记与党委常委、纪委书记同属党委常委会", "overlap_org": "中国共产党宁夏回族自治区委员会", "overlap_period": "present"},
    # 李邑飞 — 副主席买彦州（上下级）
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "党委书记与党委常委、副主席同属党委常委会", "overlap_org": "中国共产党宁夏回族自治区委员会", "overlap_period": "present"},
    # 梁言顺 — 张雨浦（前任书记与后任主席曾搭档）
    {"person_a": 10, "person_b": 2, "type": "共事", "context": "梁言顺任宁夏党委书记期间（2022-2024）张雨浦任自治区主席", "overlap_org": "宁夏回族自治区", "overlap_period": "2022-2024"},
]


# ── Main ──────────────────────────────────────────────────────────────────
def main():
    print(f"Building Ningxia (宁夏回族自治区) provincial leadership network...")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")
    print()

    run_build(
        slug=SLUG,
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    print()
    print("Summary:")
    print(f"  Persons:        {len(PERSONS)}")
    print(f"  Organizations:  {len(ORGANIZATIONS)}")
    print(f"  Positions:      {len(POSITIONS)}")
    print(f"  Relationships:  {len(RELATIONSHIPS)}")
    print()

    for p in [DB_PATH, GEXF_PATH]:
        if p.exists():
            print(f"  OK {p.name} ({p.stat().st_size / 1024:.1f} KB)")
        else:
            print(f"  MISSING {p.name}")

    print()
    print("Done.")


if __name__ == "__main__":
    main()