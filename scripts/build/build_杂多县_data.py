#!/usr/bin/env python3
"""杂多县（青海省玉树藏族自治州）县委书记、县长领导班子工作关系网络数据构建脚本。

数据来源（截至 2026-07）：
- 杂多县人民政府官网 www.zaduo.gov.cn
  - 领导之窗/领导活动列表（县委书记赵邦彩、县委副书记县长更阳 一手新闻）
  - 政府信息公开 > 机关简介 > 政府领导（现任政府班子名单）
  - 2019-06-19《杂多县人民政府关于调整县长、副县长工作分工的通知》（html/1095/296488）历史班子
- 360百科：才旦周（杂多县原县委书记/县长）、索河（原县长）人物小传
- 玉树融媒/玉树发布：龙措（玉树州委副书记、州长）赴杂多督导调研报道

注意：
- 现任县委书记赵邦彩、县长更阳的出生年月/学历/入党时间/早年履历，公开源（360百科未收录、
  百度系被风控拦截）暂缺，已在 report 与 person JSON 的 open_questions 中标注。
- 部分历史班子职务/日期为 plausible（由县域官方新闻与履历小传交叉推断）。

生成产物：data/database/杂多县_network.db + data/graph/杂多县_network.gexf
"""

import os
import sqlite3  # noqa: F401  (含于标准库，供脚本校验 DB；数据写入由 run_build 完成)

from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
from gov_relation.runner import run_build

# ── 路径（规范目标：data/database、data/graph）──
DB_PATH = DATABASE_DIR / "杂多县_network.db"
GEXF_PATH = GRAPH_DIR / "杂多县_network.gexf"

# ── 人员（id 为整数，positions/relationships 用同一整数引用）──
# 1-8 现任班子；9 现任县委副书记；10-12 历任书记/县长；13-14 历史政府班子；15 玉树州州长
persons = [
    # ===== 现任核心（confirmed，政府官网 2026-07-29 截止）=====
    {
        "id": 1, "name": "赵邦彩", "gender": "男", "birth": "待查", "education": "待查",
        "current_post": "杂多县委书记", "current_org": "中共杂多县委员会",
        # 2024-10 首次以县委书记见于杂多官网新闻；2026-07-29 仍在任
        "source": "http://www.zaduo.gov.cn",
    },
    {
        "id": 2, "name": "更阳", "gender": "男", "birth": "待查", "education": "待查",
        "current_post": "杂多县委副书记、县长", "current_org": "杂多县人民政府",
        # 2026-07-29 参加阿多乡代表团审议
        "source": "http://www.zaduo.gov.cn",
    },
    {
        "id": 3, "name": "台智", "gender": "男", "birth": "待查", "education": "待查",
        "current_post": "杂多县委常委、常务副县长", "current_org": "杂多县人民政府",
        "source": "http://www.zaduo.gov.cn/xxgk/jgjj.aspx",
    },
    {
        "id": 4, "name": "刘强", "gender": "男", "birth": "待查", "education": "待查",
        "current_post": "杂多县副县长", "current_org": "杂多县人民政府",
        "source": "http://www.zaduo.gov.cn/xxgk/jgjj.aspx",
    },
    {
        "id": 5, "name": "王宇", "gender": "男", "birth": "待查", "education": "待查",
        "current_post": "杂多县副县长", "current_org": "杂多县人民政府",
        "source": "http://www.zaduo.gov.cn/xxgk/jgjj.aspx",
    },
    {
        "id": 6, "name": "扎西朋措", "gender": "男", "birth": "待查", "education": "待查",
        "current_post": "杂多县副县长", "current_org": "杂多县人民政府",
        "source": "http://www.zaduo.gov.cn/xxgk/jgjj.aspx",
    },
    {
        "id": 7, "name": "才拉求吉", "gender": "待查", "birth": "待查", "education": "待查",
        "current_post": "杂多县副县长", "current_org": "杂多县人民政府",
        "source": "http://www.zaduo.gov.cn/xxgk/jgjj.aspx",
    },
    {
        "id": 8, "name": "王偕亮", "gender": "男", "birth": "待查", "education": "待查",
        "current_post": "杂多县副县长", "current_org": "杂多县人民政府",
        "source": "http://www.zaduo.gov.cn/xxgk/jgjj.aspx",
    },
    {
        "id": 9, "name": "陈如金", "gender": "男", "birth": "待查", "education": "待查",
        "current_post": "杂多县委副书记", "current_org": "中共杂多县委员会",
        # 2025-09 深入县城水源地督导水质安全
        "source": "http://www.zaduo.gov.cn",
    },
    # ===== 历任县委书记 =====
    {
        "id": 10, "name": "刘中", "gender": "男", "birth": "待查", "education": "待查",
        "current_post": "〔前任〕杂多县委书记（约2021-2024）", "current_org": "中共杂多县委员会",
        # 2021-08 至 2024-09 均见"县委书记刘中"，其后交棒赵邦彩
        "source": "http://www.zaduo.gov.cn",
    },
    {
        "id": 11, "name": "才旦周", "gender": "男", "birth": "1966-07", "education": "青海省警察学校（1982-1984 学习）",
        "current_post": "〔前县委书记/前县长〕", "current_org": "中共杂多县委员会",
        # 360百科：历任杂多县长（2014.03）→县委书记（2016）→ 2019.05 拟提副厅级
        "source": "https://baike.so.com/doc-search/才旦周",
    },
    # ===== 历任县长 =====
    {
        "id": 12, "name": "索河", "gender": "男", "birth": "1966-08", "education": "青海教育学院进修（1989-1991）",
        "current_post": "〔前县长〕", "current_org": "杂多县人民政府",
        # 360百科：多年称多县工作 → 玉树州政府秘书长（2011-2016）→ 杂多县代县长（2016.06）/县长（2016.10）
        "source": "https://baike.so.com/doc-search/索河",
    },
    # ===== 历史政府班子（2019）=====
    {
        "id": 13, "name": "康军", "gender": "男", "birth": "待查", "education": "待查",
        "current_post": "〔前常务副县长〕", "current_org": "杂多县人民政府",
        # 2019 政府分工文件 常务副县长
        "source": "http://www.zaduo.gov.cn/html/1095/296488.html",
    },
    {
        "id": 14, "name": "钟保杰", "gender": "男", "birth": "待查", "education": "待查",
        "current_post": "〔前常务副县长〕", "current_org": "杂多县人民政府",
        # 2019 分工文件副县长；2020-06 常务副县长
        "source": "http://www.zaduo.gov.cn",
    },
    # ===== 州上级联系 =====
    {
        "id": 15, "name": "龙措", "gender": "女", "birth": "待查", "education": "待查",
        "current_post": "玉树州委副书记、州长", "current_org": "玉树藏族自治州人民政府",
        # 2026-07 两次赴杂多督导（山体滑坡、高海拔乡镇）
        "source": "玉树融媒/玉树发布",
    },
]

# ── 组织 ──
organizations = [
    {"id": 1, "name": "中共杂多县委员会", "type": "党委", "level": "县级", "location": "青海省玉树藏族自治州杂多县"},
    {"id": 2, "name": "杂多县人民政府", "type": "政府", "level": "县级", "location": "青海省玉树藏族自治州杂多县"},
    {"id": 3, "name": "中共杂多县纪律检查委员会", "type": "党委", "level": "县级", "location": "青海省玉树藏族自治州杂多县"},
    {"id": 4, "name": "玉树藏族自治州人民政府", "type": "政府", "level": "地级", "location": "青海省玉树藏族自治州"},
    {"id": 5, "name": "中共玉树藏族自治州委员会", "type": "党委", "level": "地级", "location": "青海省玉树藏族自治州"},
]

# ── 任职 ──
positions = [
    # 现任
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "2024-10"},
    {"person_id": 2, "org_id": 2, "title": "县委副书记、县长", "start": "2021?"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "2021?"},
    {"person_id": 3, "org_id": 2, "title": "县委常委、常务副县长", "start": "2022?"},
    {"person_id": 4, "org_id": 2, "title": "副县长", "start": ""},
    {"person_id": 5, "org_id": 2, "title": "副县长", "start": ""},
    {"person_id": 6, "org_id": 2, "title": "副县长", "start": ""},
    {"person_id": 7, "org_id": 2, "title": "副县长", "start": ""},
    {"person_id": 8, "org_id": 2, "title": "副县长", "start": ""},
    {"person_id": 9, "org_id": 1, "title": "县委副书记", "start": "2025?"},
    # 历任县委书记 / 县长
    {"person_id": 10, "org_id": 1, "title": "县委书记", "start": "2021", "end": "2024"},
    {"person_id": 11, "org_id": 1, "title": "县委书记", "start": "2016", "end": "2019"},
    {"person_id": 11, "org_id": 2, "title": "县长", "start": "2014", "end": "2016"},
    {"person_id": 12, "org_id": 2, "title": "县长（代县长 2016.06；县长 2016.10）", "start": "2016", "end": "2020"},
    # 历史政府班子（2019-2020）
    {"person_id": 13, "org_id": 2, "title": "常务副县长", "start": "2019"},
    {"person_id": 14, "org_id": 2, "title": "副县长 → 常务副县长", "start": "2019"},
    # 州联系
    {"person_id": 15, "org_id": 4, "title": "州长", "start": "2025?"},
    {"person_id": 15, "org_id": 5, "title": "州委副书记", "start": "2025?"},
]

# ── 关系 ──
relationships = [
    # 现任核心搭档与班子
    {
        "person_a": 1, "person_b": 2, "type": "党政搭档",
        "context": "县委书记与县长（党政一把手搭档），共同调研、对接国家电网玉树供电公司等",
        "overlap_org": "杂多县（县委/县政府）", "overlap_period": "2024-10 至今",
    },
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "县委书记与县委副书记", "overlap_org": "中共杂多县委员会"},
    {"person_a": 2, "person_b": 3, "type": "上下级", "context": "县长与常务副县长（政府核心搭档）", "overlap_org": "杂多县人民政府"},
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "县长与副县长", "overlap_org": "杂多县人民政府"},
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "县长与副县长", "overlap_org": "杂多县人民政府"},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "县长与副县长", "overlap_org": "杂多县人民政府"},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "县长与副县长", "overlap_org": "杂多县人民政府"},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "县长与副县长", "overlap_org": "杂多县人民政府"},
    # 前后任接替（政治传承）
    {
        "person_a": 10, "person_b": 1, "type": "前后任",
        "context": "刘中（县委书记）→ 赵邦彩（县委书记），约 2024-09/10 交接",
        "overlap_org": "中共杂多县委员会", "overlap_period": "2024",
    },
    {
        "person_a": 11, "person_b": 10, "type": "前后任",
        "context": "才旦周（县委书记，晋升副厅）→ 刘中（县委书记）",
        "overlap_org": "中共杂多县委员会",
    },
    {
        "person_a": 11, "person_b": 12, "type": "前后任",
        "context": "才旦周（县长 2014-2016）→ 索河（县长 2016.10）",
        "overlap_org": "杂多县人民政府",
    },
    {
        "person_a": 12, "person_b": 2, "type": "前后任",
        "context": "索河（县长 2016-2020）→ 更阳（县长 2021-至今）",
        "overlap_org": "杂多县人民政府",
    },
    # 历史班子内部
    {
        "person_a": 13, "person_b": 14, "type": "同级",
        "context": "同为 2019 县政府班子（常务副县长与副县长）",
        "overlap_org": "杂多县人民政府", "overlap_period": "2019",
    },
    # 州 — 县上下级工作关系
    {
        "person_a": 15, "person_b": 2, "type": "州县长下级",
        "context": "玉树州州长龙措多次赴杂多县督导调研，直接指挥县长更阳工作",
        "overlap_org": "玉树藏族自治州/杂多县",
    },
    {
        "person_a": 15, "person_b": 1, "type": "州县级领导上下级",
        "context": "玉树州州长龙措赴杂多督导防汛暨民生保障，县委书记赵邦彩县域工作接受州级督导",
        "overlap_org": "玉树藏族自治州/杂多县",
    },
]

# ── 构建 ──
if __name__ == "__main__":
    run_build(
        slug="杂多县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print(f"✅ 数据库: {DB_PATH}")
    print(f"✅ 图文件: {GEXF_PATH}")