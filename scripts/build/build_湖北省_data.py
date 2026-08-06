#!/usr/bin/env python3
"""湖北省省级领导班子工作关系网络生成脚本.

基于湖北省人民政府门户 (www.hubei.gov.cn)、荆楚网（湖北日报网）头版领导活动
专集、以及百度百科公开人物履历，构建湖北省省委、省政府、省人大、省政协、
省纪委监委主要领导的 SQLite 数据库与 GEXF 关系图。

数据时间锚点：截至 2026-08-06（模拟环境日期）
核心任职信息以百度百科公开履历 and 湖北日报网领导活动专集为 confirmed 依据；
早期履历细节以官方/主流媒体公开来源确认；无法确认的现任岗位列于 report/open_gaps.md。

来源：
- 百度百科人物词条（关志鸥/李殿勋/王忠林/王蒙徽/应勇/王晓东/孙伟/侯淅珉），2026-08 访问
- 荆楚网(湖北日报网) www.cnhubei.com 2026-08-05 头版「关志鸥在孝感调研」「李殿勋在宜昌市调研」
- 湖北省人民政府门户 www.hubei.gov.cn（408/412，本次未能直接抓取，列于 open_gaps）
"""

from __future__ import annotations

import sqlite3  # SQLite 标准库（经由 gov_relation.runner 落库）

import sys
from datetime import datetime
from pathlib import Path

# 项目根目录（向上寻找包含 gov_relation/ 的仓库根，兼容 data/tmp/<task>/, scripts/build/, 仓库根 三种位置）
_HERE = Path(__file__).resolve().parent
_PROJECT_ROOT = next((p for p in _HERE.parents if (p / "gov_relation").is_dir()), _HERE)
sys.path.insert(0, str(_PROJECT_ROOT))

from gov_relation.runner import run_build

SLUG = "湖北省"
DB_PATH = _HERE / "湖北省_network.db"
GEXF_PATH = _HERE / "湖北省_network.gexf"

# ── Persons ───────────────────────────────────────────────────────────────
PERSONS = [
    # 1 现任省委书记
    {
        "id": 1,
        "name": "关志鸥",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1969-12",
        "birthplace": "辽宁沈阳",
        "education": "沈阳农业大学农学系生态学专业硕士；沈阳农业大学在职研究生，生态学/理学博士",
        "party_join": "1993-12",
        "work_start": "1995-07",
        "current_post": "湖北省委书记",
        "current_org": "中国共产党湖北省委员会",
        "source": "https://baike.baidu.com/item/关志鸥",
    },
    # 2 现任省长
    {
        "id": 2,
        "name": "李殿勋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967-11",
        "birthplace": "",
        "education": "华东师范大学历史系历史学学士；西南政法学院法律系法学学士",
        "party_join": "1994-06",
        "work_start": "1991-07",
        "current_post": "湖北省省长",
        "current_org": "湖北省人民政府",
        "source": "https://baike.baidu.com/item/李殿勋",
    },
    # 3 现任省人大常委会主任（前省长、前省委书记）
    {
        "id": 3,
        "name": "王忠林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1962-08",
        "birthplace": "山东费县",
        "education": "华东政法学院法律系、中国人民大学、中国海洋大学管理学博士（在职研究生）",
        "party_join": "1984-06",
        "work_start": "1984-07",
        "current_post": "湖北省人大常委会主任",
        "current_org": "湖北省人大常委会",
        "source": "https://baike.baidu.com/item/王忠林",
    },
    # 4 现任省政协主席
    {
        "id": 4,
        "name": "孙伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1961-12",
        "birthplace": "山东蓬莱",
        "education": "北京大学地理学系经济地理-区域与城市规划专业，理学学士",
        "party_join": "1988-02",
        "work_start": "1977-12",
        "current_post": "湖北省政协主席",
        "current_org": "中国人民政治协商会议湖北省委员会",
        "source": "https://baike.baidu.com/item/孙伟",
    },
    # 5 现任省纪委书记
    {
        "id": 5,
        "name": "侯淅珉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1963-07",
        "birthplace": "河南淅川",
        "education": "北京大学地理学系自然地理学士、社会学硕士；华中科技大学管理学博士（在职研究生）",
        "party_join": "1998-04",
        "work_start": "1987-07",
        "current_post": "湖北省纪委书记",
        "current_org": "中共湖北省纪律检查委员会",
        "source": "https://baike.baidu.com/item/侯淅珉",
    },
    # 6 前任省委书记（2022-2024），全国人大环资委副主任委员
    {
        "id": 6,
        "name": "王蒙徽",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1960-01",
        "birthplace": "江苏盐城",
        "education": "清华大学建筑系建筑学学士、清华大学城市规划与设计专业工学博士",
        "party_join": "1981-11",
        "work_start": "1983-07",
        "current_post": "全国人大环境与资源保护委员会副主任委员",
        "current_org": "全国人民代表大会",
        "source": "https://baike.baidu.com/item/王蒙徽",
    },
    # 7 前任省委书记（2020-2022，现最高检检察长）
    {
        "id": 7,
        "name": "应勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1957-11",
        "birthplace": "浙江仙居",
        "education": "浙江大学行政管理（在职大学）、法学硕士",
        "party_join": "1979-04",
        "work_start": "1976-12",
        "current_post": "最高人民检察院检察长",
        "current_org": "最高人民检察院",
        "source": "https://baike.baidu.com/item/应勇",
    },
    # 8 前任省长（2017-2021，2026-05被审查调查）
    {
        "id": 8,
        "name": "王晓东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1960-01",
        "birthplace": "江西信丰",
        "education": "江西大学哲学系学士；中央党校在职研究生（政治学）",
        "party_join": "1983-01",
        "work_start": "1983-08",
        "current_post": "（原十四届全国政协常委、农业农村委副主任；2026-05 接受审查调查）",
        "current_org": "",
        "source": "https://baike.baidu.com/item/王晓东",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────
ORGANIZATIONS = [
    {"id": 1, "name": "中国共产党湖北省委员会", "type": "党委", "level": "省级", "parent": "", "location": "湖北省武汉市"},
    {"id": 2, "name": "湖北省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "湖北省武汉市"},
    {"id": 3, "name": "湖北省人大常委会", "type": "人大", "level": "省级", "parent": "", "location": "湖北省武汉市"},
    {"id": 4, "name": "中国人民政治协商会议湖北省委员会", "type": "政协", "level": "省级", "parent": "", "location": "湖北省武汉市"},
    {"id": 5, "name": "中共湖北省纪律检查委员会（省监委）", "type": "党委", "level": "省级", "parent": "中国共产党湖北省委员会", "location": "湖北省武汉市"},
]

# ── Positions ─────────────────────────────────────────────────────────────
POSITIONS = [
    {"person_id": 1, "org_id": 1, "title": "湖北省委书记", "start_date": "2026-05", "end_date": "present", "rank": "正省级", "note": "此前任自然资源部部长；2026-05 任湖北省委书记，接任卸任的王忠林"},
    {"person_id": 2, "org_id": 2, "title": "湖北省省长", "start_date": "2025-01", "end_date": "present", "rank": "正省级", "note": "2024-12 任湖北省委副书记/省政府党组书记，2025-01-20 当选省长"},
    {"person_id": 3, "org_id": 3, "title": "湖北省人大常委会主任", "start_date": "2025-01", "end_date": "present", "rank": "正省级", "note": "2021-05 至 2024-12 任省长，2024-12 至 2026-05 任省委书记，2026-05 卸任省委书记"},
    {"person_id": 4, "org_id": 4, "title": "湖北省政协主席", "start_date": "2022-01", "end_date": "present", "rank": "正省级", "note": "2022-01 起任省政协党组书记、主席"},
    {"person_id": 5, "org_id": 5, "title": "湖北省委常委、省纪委书记、省监委主任", "start_date": "2021-05", "end_date": "present", "rank": "副省级", "note": "2021-05 起任湖北省委常委、纪委书记、监委主任"},
    {"person_id": 6, "org_id": 1, "title": "湖北省委书记（前任）", "start_date": "2022-03", "end_date": "2024-12", "rank": "正省级", "note": "2022-03 起任省委书记，2024-12 卸任，转任全国人大环资委副主任委员"},
    {"person_id": 7, "org_id": 1, "title": "湖北省委书记（前任）", "start_date": "2020-02", "end_date": "2022-03", "rank": "正省级", "note": "2020-02 任省委书记，2022-03 卸任；2023-03 起任最高人民检察院检察长"},
    {"person_id": 8, "org_id": 2, "title": "湖北省省长（前任）", "start_date": "2017-01", "end_date": "2021-05", "rank": "正省级", "note": "2017 任代省长、省长，2021-05 卸任；2026-05 涉嫌严重违纪违法接受审查调查"},
]

# ── Relationships (person <-> person) ─────────────────────────────────────
RELATIONSHIPS = [
    # 关志鸥 — 李殿勋（现任党政一把手搭档）
    {"person_a": 1, "person_b": 2, "type": "搭档", "context": "关志鸥2026-05任湖北省委书记后与省长李殿勋组成党政一把手搭档", "overlap_org": "湖北省", "overlap_period": "2026-05至今"},
    # 关志鸥 — 前任省委书记 王忠林（前任后任）
    {"person_a": 1, "person_b": 3, "type": "前任后任", "context": "王忠林2026-05 卸任湖北省委书记后由关志鸥接任", "overlap_org": "中国共产党湖北省委员会", "overlap_period": "2026-05"},
    # 李殿勋 — 前任省长 王忠林（省长继任链）
    {"person_a": 2, "person_b": 3, "type": "前任后任", "context": "王忠林2024-12 由省长转任省委书记，李殿勋2025-01 继任省长", "overlap_org": "湖北省人民政府", "overlap_period": "2024-12至2025-01"},
    # 王忠林 — 前前任省委书记 王蒙徽（前任后任）
    {"person_a": 3, "person_b": 6, "type": "前任后任", "context": "王蒙徽2024-12 卸任湖北省委书记，由王忠林接任（2024-12）", "overlap_org": "中国共产党湖北省委员会", "overlap_period": "2024-12"},
    # 王忠林 — 前前任省长 王晓东（前任后任）
    {"person_a": 3, "person_b": 8, "type": "前任后任", "context": "王晓东2021-05 卸任湖北省长，王忠林继任", "overlap_org": "湖北省人民政府", "overlap_period": "2021-05"},
    # 应勇 — 王蒙温（省委书记前任后任 / 共事）
    {"person_a": 7, "person_b": 6, "type": "前任后任", "context": "应勇2020-2022 任省委书记，2022-03 由王蒙徽接任", "overlap_org": "中国共产党湖北省委员会", "overlap_period": "2022-03"},
    # 王蒙徽 — 现任省长李殿勋（期间李任一副书记/省政府工作）
    {"person_a": 6, "person_b": 2, "type": "共事", "context": "王蒙徽任省委书记期间，李殿勋2024-12 进入湖北省委任副书记、省政府党组书记", "overlap_org": "中国共产党湖北省委员会", "overlap_period": "2024-12"},
    # 孙伟 — 关志怀（省委与政协 四套班子 协作）
    {"person_a": 4, "person_b": 1, "type": "共事", "context": "省委书记与省政协主席同属省级领导层", "overlap_org": "湖北省", "overlap_period": "2026-05至今"},
    # 孙伟 — 李殿勋（省政府与省政协 协作）
    {"person_a": 4, "person_b": 2, "type": "共事", "context": "省长大与省政协主席同属省级班子，省政府与省政协日常协作", "overlap_org": "湖北省", "overlap_period": "2025-01至今"},
    # 侯阳珉 — 与省委书记（纪委与省委）
    {"person_a": 5, "person_b": 1, "type": "上下级", "context": "省纪委书记关志鸥同志为省委班子之列", "overlap_org": "湖北省", "overlap_period": "present"},
]


# ── Main ──────────────────────────────────────────────────────────────────
def main():
    print(f"Building Hubei (湖北省) provincial leadership network...")
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