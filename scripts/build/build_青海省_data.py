#!/usr/bin/env python3
"""青海省省级领导班子工作关系网络生成脚本.

基于维基百科（zh.wikipedia.org，含青海省现任省部级官员模板导航、各人物
传记条目并附官方/新华社/财新等参考文献）、中国政府网人事任免通稿等公开
来源，构建青海省委、省政府领导班子（2025-01 之后现任阵容）及前任主要领导
的 SQLite 数据库与 GEXF 关系图。

数据时间锚点：截至 2026-08（模拟环境日期，维基百科页面修订于 2026-05/06）
- 现任省委书记：吴晓军（2024-12-31 任，兼省人大常委会主任）
- 现任省长：罗东川（2025-01 任；2024-12 调任省委副书记、省政府党组书记）
- 专职省委副书记：刘奇凡（2023-12 由辽宁纪委书记转任）
- 省委常委、常务副省长：张锦刚（2024-12 由甘肃省委常委、副省长转任）
- 省委常委、纪委书记/监委主任：刘美频（2024-04 任）
- 省政协主席：公保扎西（藏族，2022-01 当选）
- 前任（2023-01~2024-12）省委书记：陈刚（转任广西壮族自治区党委书记）

来源（source 字段引用）：
- 维基百科 zh.wikipedia.org：吴晓军、罗东川、陈刚、刘奇凡、张锦刚、刘美频、公保扎西 等条目；「青海省现任省部级官员」一览表；青海省四大机构正职领导人沿革表
- 中国政府网 gov.cn 2025-01-23《吴晓军当选青海省人大常委会主任 罗东川当选青海省省长》
- 新华社/财新 2024-12-31 湖北、青海省委主要负责同志职务调整；财新 2025-01-04 罗东川代理青海省长

注意：本脚本在旧式 build_data.py 基础上新增，采用 gov_relation.runner.run_build() 统一落库。
"""

from __future__ import annotations

import sqlite3  # SQLite 标准库（经由 gov_relation.runner 落库）  # noqa: F401
import sys
from pathlib import Path

# 项目根目录（向上寻找包含 gov_relation/ 的仓库根，兼容 data/tmp/<task>/, scripts/build/, 仓库根 三种位置）
_HERE = Path(__file__).resolve().parent
_PROJECT_ROOT = next((p for p in _HERE.parents if (p / "gov_relation").is_dir()), _HERE)
sys.path.insert(0, str(_PROJECT_ROOT))

from gov_relation.runner import run_build  # noqa: E402

SLUG = "青海省"
DB_PATH = _HERE / "青海省_network.db"
GEXF_PATH = _HERE / "青海省_network.gexf"

# ── Persons ───────────────────────────────────────────────────────────────
PERSONS = [
    # 1 现任省委书记、省人大常委会主任（二十大中央委员）
    {
        "id": 1,
        "name": "吴晓军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966-01",
        "birthplace": "江西泰和",
        "education": "江西大学经济系政治经济学专业本科；江西财经大学在职研究生、经济学博士",
        "party_join": "1986-05",
        "work_start": "1988-07",
        "current_post": "中共青海省委书记、青海省人大常委会主任",
        "current_org": "中国共产党青海省委员会",
        "source": "https://zh.wikipedia.org/wiki/吴晓军",
    },
    # 2 现任省长（中央候补委员）
    {
        "id": 2,
        "name": "罗东川",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1965-10",
        "birthplace": "重庆",
        "education": "北京大学法律学专业法学学士；武汉大学法学院民商法专业法学硕士；北京大学知识产权专业法学博士",
        "party_join": "1986-06",
        "work_start": "1986-08",
        "current_post": "中共青海省委副书记、青海省人民政府省长、省政府党组书记",
        "current_org": "青海省人民政府",
        "source": "https://zh.wikipedia.org/wiki/罗东川",
    },
    # 3 现任省委专职副书记（中央纪委委员）
    {
        "id": 3,
        "name": "刘奇凡",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967-04",
        "birthplace": "贵州水城",
        "education": "厦门大学经济系政治经济学专业本科；研究生、管理学硕士",
        "party_join": "1994-09",
        "work_start": "1988-08",
        "current_post": "中共青海省委副书记",
        "current_org": "中国共产党青海省委员会",
        "source": "https://zh.wikipedia.org/wiki/刘奇凡",
    },
    # 4 省委常委、常务副省长（兼省政府党组副书记）
    {
        "id": 4,
        "name": "张锦刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-04",
        "birthplace": "山东威海",
        "education": "鞍山钢铁学院钢铁冶金专业本科；东北大学材料工程在职研究生、工学博士；教授级高级工程师",
        "party_join": "1991-05",
        "work_start": "1992-08",
        "current_post": "青海省委常委、常务副省长",
        "current_org": "青海省人民政府",
        "source": "https://zh.wikipedia.org/wiki/张锦刚",
    },
    # 5 省委常委、省纪委书记、省监委主任（中央纪委委员）
    {
        "id": 5,
        "name": "刘美频",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969-09",
        "birthplace": "湖北监利",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "青海省委常委、省纪委书记、省监委主任",
        "current_org": "中国共产党青海省纪律检查委员会",
        "source": "https://zh.wikipedia.org/wiki/刘美频",
    },
    # 6 省委常委、西宁市委书记
    {
        "id": 6,
        "name": "王卫东",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "青海省委常委、西宁市委书记",
        "current_org": "中国共产党西宁市委员会",
        "source": "https://zh.wikipedia.org/wiki/青海省",
    },
    # 7 省委常委、省委宣传部部长
    {
        "id": 7,
        "name": "王大南",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "青海省委常委、省委宣传部部长",
        "current_org": "中国共产党青海省委员会",
        "source": "https://zh.wikipedia.org/wiki/青海省",
    },
    # 8 省委常委、海东市委书记
    {
        "id": 8,
        "name": "乌拉孜别克·热苏力汗",
        "gender": "男",
        "ethnicity": "哈萨克族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "青海省委常委、海东市委书记",
        "current_org": "中国共产党海东市委员会",
        "source": "https://zh.wikipedia.org/wiki/青海省",
    },
    # 9 省委常委、省委统战部部长
    {
        "id": 9,
        "name": "班果",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "青海省委常委、省委统战部部长",
        "current_org": "中国共产党青海省委员会",
        "source": "https://zh.wikipedia.org/wiki/青海省",
    },
    # 10 省委常委、省委秘书长
    {
        "id": 10,
        "name": "朱向峰",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "青海省委常委、省委秘书长",
        "current_org": "中国共产党青海省委员会",
        "source": "https://zh.wikipedia.org/wiki/青海省",
    },
    # 11 省委常委、省委政法委书记
    {
        "id": 11,
        "name": "何录春",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "湖南道县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "青海省委常委、省委政法委书记",
        "current_org": "中国共产党青海省委员会",
        "source": "https://zh.wikipedia.org/wiki/青海省",
    },
    # 12 省委常委、省委组织部部长
    {
        "id": 12,
        "name": "曹俊",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "青海省委常委、省委组织部部长",
        "current_org": "中国共产党青海省委员会",
        "source": "https://zh.wikipedia.org/wiki/青海省",
    },
    # 13 副省长（省公安厅厅长）——现任省政府班子成员之一
    {
        "id": 13,
        "name": "李宏亚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "青海省副省长、省公安厅厅长",
        "current_org": "青海省公安厅",
        "source": "https://zh.wikipedia.org/wiki/青海省",
    },
    # 14 省政协主席（藏族，中央候补委员）
    {
        "id": 14,
        "name": "公保扎西",
        "gender": "男",
        "ethnicity": "藏族",
        "birth": "1962-10",
        "birthplace": "青海化隆",
        "education": "青海省湟源畜牧学校（今青海畜牧兽医职业技术学院）畜牧兽医专业；湖南大学国际商学院工商管理专业研究生、工商管理硕士",
        "party_join": "1983-07",
        "work_start": "1978-07",
        "current_post": "青海省政协主席",
        "current_org": "中国人民政治协商会议青海省委员会",
        "source": "https://zh.wikipedia.org/wiki/公保扎西",
    },
    # 15 前任省委书记（2023-01~2024-12，转任广西）
    {
        "id": 15,
        "name": "陈刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1965-04",
        "birthplace": "江苏高邮",
        "education": "扬州师范学院化学系；哈尔滨工业大学应用化学系高分子材料专业硕士；北京大学化学系无机化学专业理学博士",
        "party_join": "1986-12",
        "work_start": "1990-08",
        "current_post": "广西壮族自治区党委书记（青海省前任省委书记）",
        "current_org": "中国共产党广西壮族自治区委员会",
        "source": "https://zh.wikipedia.org/wiki/陈刚_(1965年)",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────
ORGANIZATIONS = [
    {"id": 1, "name": "中国共产党青海省委员会", "type": "党委", "level": "省级", "parent": "", "location": "青海省西宁市"},
    {"id": 2, "name": "青海省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "青海省西宁市"},
    {"id": 3, "name": "青海省人大常委会", "type": "人大", "level": "省级", "parent": "", "location": "青海省西宁市"},
    {"id": 4, "name": "青海省纪律检查委员会", "type": "纪委", "level": "省级", "parent": "中国共产党青海省委员会", "location": "青海省西宁市"},
    {"id": 5, "name": "青海省监察委员会", "type": "纪委", "level": "省级", "parent": "青海省纪律检查委员会", "location": "青海省西宁市"},
    {"id": 6, "name": "青海省公安厅", "type": "政府", "level": "副省级", "parent": "青海省人民政府", "location": "青海省西宁市"},
    {"id": 7, "name": "中国人民政治协商会议青海省委员会", "type": "政协", "level": "省级", "parent": "", "location": "青海省西宁市"},
    {"id": 8, "name": "中国共产党西宁市委员会", "type": "党委", "level": "地厅级", "parent": "中国共产党青海省委员会", "location": "青海省西宁市"},
    {"id": 9, "name": "中国共产党海东市委员会", "type": "党委", "level": "地厅级", "parent": "中国共产党青海省委员会", "location": "青海省海东市"},
    {"id": 10, "name": "中国共产党广西壮族自治区委员会", "type": "党委", "level": "省级", "parent": "", "location": "广西壮族自治区南宁市"},
]

# ── Positions ─────────────────────────────────────────────────────────────
POSITIONS = [
    # 吴晓军
    {"person_id": 1, "org_id": 1, "title": "中共青海省委书记", "start_date": "2024-12", "end_date": "present", "rank": "正省级", "note": "2024-12-31 中央决定任省委书记（接替转任广西的陈刚）；此前2022-03起任省长"},
    {"person_id": 1, "org_id": 3, "title": "青海省人大常委会主任", "start_date": "2025-01", "end_date": "present", "rank": "正省级", "note": "2025-01-23 当选"},
    {"person_id": 1, "org_id": 2, "title": "青海省人民政府省长", "start_date": "2022-03", "end_date": "2025-01", "rank": "正省级", "note": "2022-03 任党组书记、代省长，2022-05 当选；2025-01 辞职交由罗东川"},
    {"person_id": 1, "org_id": 1, "title": "中共青海省委副书记", "start_date": "2021-04", "end_date": "2022-03", "rank": "副省级", "note": "2021-04 由江西省委常委、南昌市委书记调任青海省委副书记"},
    # 罗东川
    {"person_id": 2, "org_id": 2, "title": "青海省人民政府省长、党组书记", "start_date": "2025-01", "end_date": "present", "rank": "正省级", "note": "2024-12 任省政府党组书记，2025-01-04 代理省长，2025-01-23 当选"},
    {"person_id": 2, "org_id": 1, "title": "中共青海省委副书记", "start_date": "2024-12", "end_date": "present", "rank": "副省级", "note": "2024-12-31 由福建省委副书记调任青海省委副书记"},
    # 刘奇凡
    {"person_id": 3, "org_id": 1, "title": "中共青海省委副书记", "start_date": "2023-12", "end_date": "present", "rank": "副省级", "note": "2023-12 由辽宁省委常委、省纪委书记、省监委主任转任"},
    # 张锦刚
    {"person_id": 4, "org_id": 2, "title": "青海省委常委、常务副省长、省政府党组副书记", "start_date": "2024-12", "end_date": "present", "rank": "副省级", "note": "2024-12 由甘肃省委常委、副省长转任"},
    {"person_id": 4, "org_id": 2, "title": "青海省人民政府副省长（常务）", "start_date": "2024-12", "end_date": "present", "rank": "副省级", "note": "兼任省政府党组副书记"},
    # 刘美频
    {"person_id": 5, "org_id": 4, "title": "青海省委常委、省纪委书记", "start_date": "2024-04", "end_date": "present", "rank": "副省级", "note": "2024-04 由中央纪委国家监委案件监督管理室主任转任"},
    {"person_id": 5, "org_id": 5, "title": "青海省监委主任", "start_date": "2025-05", "end_date": "present", "rank": "副省级", "note": "2025-01 当选"},
    # 王卫东（西宁）
    {"person_id": 6, "org_id": 8, "title": "青海省委常委、西宁市委书记", "start_date": "2022", "end_date": "present", "rank": "副省级", "note": ""},
    # 王大南（宣传）
    {"person_id": 7, "org_id": 1, "title": "青海省委常委、省委宣传部部长", "start_date": "2022", "end_date": "present", "rank": "副省级", "note": ""},
    # 乌拉孜别克（海东）
    {"person_id": 8, "org_id": 9, "title": "青海省委常委、海东市委书记", "start_date": "2021", "end_date": "present", "rank": "副省级", "note": ""},
    # 班果（统战）
    {"person_id": 9, "org_id": 1, "title": "青海省委常委、省委统战部部长", "start_date": "2022", "end_date": "present", "rank": "副省级", "note": ""},
    # 朱向峰（秘书长）
    {"person_id": 10, "org_id": 1, "title": "青海省委常委、省委秘书长", "start_date": "2023", "end_date": "present", "rank": "副省级", "note": ""},
    # 何录春（政法）
    {"person_id": 11, "org_id": 1, "title": "青海省委常委、省委政法委书记", "start_date": "2025", "end_date": "present", "rank": "副省级", "note": ""},
    # 曹俊（组织）
    {"person_id": 12, "org_id": 1, "title": "青海省委常委、省委组织部部长", "start_date": "2025", "end_date": "present", "rank": "副省级", "note": ""},
    # 李宏亚（公安）
    {"person_id": 13, "org_id": 6, "title": "青海省副省长、省公安厅厅长", "start_date": "2022", "end_date": "present", "rank": "副省级", "note": ""},
    # 公保扎西（政协）
    {"person_id": 14, "org_id": 7, "title": "青海省政协主席", "start_date": "2022-01", "end_date": "present", "rank": "正省级", "note": "2022-01-24 当选；曾任西藏自治区党委常委、省政协副主席、统战部部长"},
    # 陈刚（前任书记）
    {"person_id": 15, "org_id": 1, "title": "中共青海省委书记（前任）", "start_date": "2023-01", "end_date": "2024-12", "rank": "正省级", "note": "2024-12-31 转任广西壮族自治区党委书记"},
    {"person_id": 15, "org_id": 10, "title": "广西壮族自治区党委书记（现任）", "start_date": "2024-12", "end_date": "present", "rank": "正省级", "note": ""},
]

# ── Relationships ─────────────────────────────────────────────────────────
RELATIONSHIPS = [
    # 吴晓军 — 罗东川（现任党政一把手搭档，前省长→现省委书记）
    {"person_a": 1, "person_b": 2, "type": "搭档", "context": "吴晓军2024-12任省委书记后，与省长罗东川组成青海党政一把手搭档", "overlap_org": "青海省", "overlap_period": "2024-12至今"},
    # 罗东川 — 吴晓军（省长接任链：吴晓军让渡省长给罗东川）
    {"person_a": 2, "person_b": 1, "type": "前任后任", "context": "罗东川2025-01接任青海省长（接替转任省委书记的吴晓军）", "overlap_org": "青海省人民政府", "overlap_period": "2025-01"},
    # 吴晓军 — 陈刚（前省委书记）
    {"person_a": 1, "person_b": 15, "type": "前任后任", "context": "吴晓军2024-12接任青海省委书记（接替转任广西的陈刚）", "overlap_org": "中国共产党青海省委员会", "overlap_period": "2024-12"},
    # 陈刚 — 吴晓军（陈刚任书记期间吴晓军任省长）
    {"person_a": 15, "person_b": 1, "type": "共事", "context": "陈刚任青海省委书记期间（2023-01~2024-12）吴晓军任省长，属党政一把手搭档", "overlap_org": "青海省", "overlap_period": "2023-01~2024-12"},
    # 吴晓军 — 刘奇凡（书记与专职副书记）
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "省委书记与省委专职副书记同属省委常委会", "overlap_org": "中国共产党青海省委员会", "overlap_period": "2024-12至今"},
    # 吴晓军 — 张锦刚（书记与常务副省长）
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "省委书记与省委常委、常务副省长同属省委常委会及省政府班子", "overlap_org": "青海省人民政府", "overlap_period": "2024-12至今"},
    # 罗东川 — 张锦刚（省长与常务副省长）
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "省长与常务副省长同属省政府班子", "overlap_org": "青海省人民政府", "overlap_period": "2025至今"},
    # 吴晓军 — 刘美频（书记与纪委书记）
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "省委书记与省委常委、省纪委书记同属省委常委会", "overlap_org": "中国共产党青海省委员会", "overlap_period": "2024-12至今"},
    # 吴晓军 — 公保扎西（书记与政协主席）
    {"person_a": 1, "person_b": 14, "type": "共事", "context": "省委书记与省政协主席同属青海省部级领导层", "overlap_org": "青海省", "overlap_period": "2024-12至今"},
    # 吴晓军 — 王卫东（书记与西宁市委书记）
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "省委书记与省委常委、西宁市委书记同属省委常委会", "overlap_org": "中国共产党青海省委员会", "overlap_period": "present"},
    # 罗东川 — 李宏亚（省长与公安厅长）
    {"person_a": 2, "person_b": 13, "type": "上下级", "context": "省长与省公安厅厅长同属省政府班子（副省长兼）", "overlap_org": "青海省人民政府", "overlap_period": "2025至今"},
    # 刘奇凡 — 刘美频（职业同源：纪委系统）
    {"person_a": 3, "person_b": 5, "type": "共事", "context": "刘奇凡曾任内蒙古、辽宁纪委书记，刘美频现任青海纪委书记，均属纪检系统干部", "overlap_org": "纪检监察系统", "overlap_period": "present"},
]


# ── Main ──────────────────────────────────────────────────────────────────
def main():
    print(f"Building Qinghai (青海省) provincial leadership network...")
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