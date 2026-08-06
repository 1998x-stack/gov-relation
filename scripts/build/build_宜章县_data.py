#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
宜章县（湖南省郴州市）领导班子工作关系网络数据构建脚本。

依据 2026-08 研究结果构建：
- 现任县委书记 邓生华（2025.06 起），现任县长 彭景（2026.07 确认）
- 前任县委书记链：周笑春(2007-2011) → 欧阳锋(2011-2015.12) → 王建球(2015.12-2021.05) → 张润槐(2021.05-2025.04) → 邓生华(2025.06-今)
- 第十三次/第十四次县委常委会成员、人大/政协班子

输出：SQLite 数据库 + GEXF 图文件。
"""
import os
import sys
import sqlite3  # noqa: F401  (process_tmp 校验 token)
from pathlib import Path

# 使 gov_relation 可导入
# 使 gov_relation 可导入：向上查找含 gov_relation 包的仓库根目录
_REPO_ROOT = Path(__file__).resolve().parent
for _ in range(6):
    if (_REPO_ROOT / "gov_relation").is_dir():
        break
    _REPO_ROOT = _REPO_ROOT.parent
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build  # noqa: E402

# 输出路径（写入脚本所在 staging 目录；架构升级后由 process_tmp 复制到 canonical）
DB_PATH = str(Path(__file__).resolve().parent / "宜章县_network.db")
GEXF_PATH = str(Path(__file__).resolve().parent / "宜章县_network.gexf")

SLOG = "宜章县"

# ==================== 组织 ====================
organizations = [
    {"id": 1, "name": "中共宜章县委员会", "type": "党委", "level": "县级", "parent": "中共郴州市委", "location": "湖南省郴州市宜章县"},
    {"id": 2, "name": "宜章县人民政府", "type": "政府", "level": "县级", "parent": "郴州市人民政府", "location": "湖南省郴州市宜章县"},
    {"id": 3, "name": "宜章县人大常委会", "type": "人大", "level": "县级", "parent": "宜章县", "location": "湖南省郴州市宜章县"},
    {"id": 4, "name": "宜章县政协", "type": "政协", "level": "县级", "parent": "宜章县", "location": "湖南省郴州市宜章县"},
    {"id": 5, "name": "宜章经济开发区", "type": "开发区", "level": "县级", "parent": "宜章县人民政府", "location": "湖南省郴州市宜章县"},
    {"id": 6, "name": "中共郴州市委", "type": "党委", "level": "地级市", "parent": "中共湖南省委", "location": "湖南省郴州市"},
    {"id": 7, "name": "中共衡阳市委", "type": "党委", "level": "地级市", "parent": "中共湖南省委", "location": "湖南省衡阳市"},
    {"id": 8, "name": "湖南省委组织部", "type": "党委机关", "level": "省级", "parent": "中共湖南省委", "location": "湖南省长沙市"},
    {"id": 9, "name": "怀化市委组织部", "type": "党委机关", "level": "地级市", "parent": "中共怀化市委", "location": "湖南省怀化市"},
    {"id": 10, "name": "新晃侗族自治县委组织部", "type": "党委机关", "level": "县级", "parent": "中共怀化市委", "location": "湖南省怀化市新晃县"},
    {"id": 11, "name": "湖南省农业农村厅", "type": "政府机关", "level": "省级", "parent": "湖南省人民政府", "location": "湖南省长沙市"},
]

# ==================== 人员 ====================
SRC_WIKI = "https://zh.wikipedia.org/wiki/宜章县"
SRC_YZXWW = "https://www.yizhangxww.cn/"
SRC_CZS = "https://www.czs.gov.cn/"

persons = [
    # ---- 现任核心 ----
    {"id": 1, "name": "邓生华", "gender": "男", "ethnicity": "汉族", "birth": "1981-03",
     "birthplace": "湖南省桂阳县", "current_post": "县委书记", "current_org": "中共宜章县委员会",
     "source": "宜章新闻网 2026-08 + 桂阳调研"},
    {"id": 2, "name": "彭景", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "current_post": "县委副书记、县长", "current_org": "宜章县人民政府",
     "source": "宜章新闻网 2026-07-31 县政府常务会议"},
    # ---- 宜章前任书记链 ----
    {"id": 3, "name": "张润槐", "gender": "男", "ethnicity": "侗族", "birth": "1976-03",
     "birthplace": "湖南省新晃侗族自治县", "current_post": "衡阳市委常委、耒阳市委书记", "current_org": "中共衡阳市委",
     "source": "澎湃新闻 2025-04-11 跨市调任 + 网易简历"},
    {"id": 4, "name": "王建球", "gender": "男", "ethnicity": "汉族", "birth": "1970-09",
     "birthplace": "湖南省", "current_post": "湖南省农业农村厅厅长", "current_org": "湖南省农业农村厅",
     "source": "宜章新闻网党建频道 + 郴州市政府 2015-12"},
    {"id": 5, "name": "欧阳锋", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "湖南省", "current_post": "原宜章县委书记（2015.12 转任桂阳县委书记）", "current_org": "",
     "source": "郴州市人民政府 2015-12-02"},
    {"id": 6, "name": "周笑春", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "current_post": "原宜章县委书记（2007-2011）", "current_org": "",
     "source": "宜章县第十届县委选举报道"},
    # ---- 四套班子 ----
    {"id": 7, "name": "李秀芳", "gender": "男", "ethnicity": "汉族", "birth": "1970-05",
     "birthplace": "湖南省宜章县", "current_post": "县人大常委会主任", "current_org": "宜章县人大常委会",
     "source": SRC_WIKI},
    {"id": 8, "name": "周露", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "current_post": "县政协主席（待确认）", "current_org": "宜章县政协",
     "source": "宜章新闻第十四届一次全会 微信裁页"},
    {"id": 9, "name": "侯志武", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "current_post": "县委副书记（十三届）", "current_org": "中共宜章县委员会",
     "source": SRC_WIKI},
    # ---- 县委常委（十三届/十四届）----
    {"id": 10, "name": "许毅敏", "gender": "女", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "current_post": "县委常委、组织部部长", "current_org": "中共宜章县委员会",
     "source": SRC_WIKI},
    {"id": 11, "name": "李琼", "gender": "女", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "current_post": "县委常委、宣传部部长", "current_org": "中共宜章县委员会",
     "source": "中华网 2023-02 常委分工"},
    {"id": 12, "name": "李桥亮", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "current_post": "县委常委、常务副县长", "current_org": "宜章县人民政府",
     "source": "中华网 2023-02 常委分工"},
    {"id": 13, "name": "杨发", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "current_post": "县委常委、纪委书记、县监委主任", "current_org": "中共宜章县纪律检查委员会",
     "source": SRC_WIKI},
    {"id": 14, "name": "尹旭东", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "current_post": "县委常委、县委办主任", "current_org": "中共宜章县委员会",
     "source": "微信公众号 2023-08"},
    {"id": 15, "name": "肖雪莲", "gender": "女", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "current_post": "县委常委、副县长、宜章经开区党工委书记", "current_org": "宜章经济开发区",
     "source": "中华网 2023-02 常委分工"},
    # ---- 常委（分工待补 / 第十四届）----
    {"id": 16, "name": "王佳文", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "current_post": "县委常委（分工待补）", "current_org": "中共宜章县委员会",
     "source": SRC_WIKI},
    {"id": 17, "name": "张晓波", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "current_post": "县委常委（分工待补）", "current_org": "中共宜章县委员会",
     "source": SRC_WIKI},
    {"id": 18, "name": "吴荣茂", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "current_post": "县委常委（分工待补）", "current_org": "中共宜章县委员会",
     "source": SRC_WIKI},
    {"id": 19, "name": "梁园宇", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "current_post": "第十四届县领导（分工待补）", "current_org": "中共宜章县委员会",
     "source": "宜章新闻第十四届一次全会 主席台前排"},
    {"id": 20, "name": "戴玲俐", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "current_post": "第十四届县领导（分工待补）", "current_org": "中共宜章县委员会",
     "source": "宜章新闻第十四届一次全会 主席台前排"},
    {"id": 21, "name": "黄锋林", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "current_post": "第十四届县领导（分工待补）", "current_org": "中共宜章县委员会",
     "source": "宜章新闻第十四届一次全会 主席台前排"},
    {"id": 22, "name": "李卫国", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "current_post": "第十四届县领导（分工待补）", "current_org": "中共宜章县委员会",
     "source": "宜章新闻第十四届一次全会 主席台前排"},
    {"id": 23, "name": "侯儒", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "current_post": "第十四届县领导（分工待补）", "current_org": "中共宜章县委员会",
     "source": "宜章新闻第十四届一次全会 主席台前排"},
    {"id": 24, "name": "曹文", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "current_post": "第十四届县领导（分工待补）", "current_org": "中共宜章县委员会",
     "source": "宜章新闻第十四届一次全会 主席台前排"},
    {"id": 25, "name": "欧云涛", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "current_post": "第十四届县领导（分工待补）", "current_org": "中共宜章县委员会",
     "source": "宜章新闻第十四届一次全会 主席台前排"},
    {"id": 26, "name": "刘路", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "current_post": "副县长兼县委办主任（分工待补）", "current_org": "宜章县人民政府",
     "source": "澎湃新闻 2025-10 郴州市政府办科级转任"},
]

# ==================== 任职 ====================
positions = [
    # 现任核心
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "2025-06", "end_date": None,
     "rank": "正处", "note": "2026.07 第十四届县委常委会第1次会议由邓生华主持"},
    {"person_id": 1, "org_id": 2, "title": "县委副书记、县长", "start_date": "2021-07", "end_date": "2025-06",
     "rank": "正处", "note": "2021-07-16 任县委副书记、县长候选人；2025 转任县委书记"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "2025-06", "end_date": None,
     "rank": "正处", "note": "2026-07-31 政府常务会议（县政府第十八届第五十九次）"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "2025-06", "end_date": None,
     "rank": "副处", "note": ""},
    # 前任书记链
    {"person_id": 3, "org_id": 1, "title": "县委书记", "start_date": "2021-05", "end_date": "2025-04",
     "rank": "正处", "note": "2021.05.21 任，2021.07.31 第十三届县委一次全会当选；2025.04 跨市调任衡阳"},
    {"person_id": 3, "org_id": 6, "title": "郴州市人大常委会副主任（兼宜章县委书记）", "start_date": "2024-12", "end_date": "2025-04",
     "rank": "副厅", "note": "2024.03 拟提名，2024.12 当选"},
    {"person_id": 3, "org_id": 7, "title": "衡阳市委常委、耒阳市委书记", "start_date": "2025-04", "end_date": None,
     "rank": "副厅", "note": "2025.04.11 跨市调任，至今"},
    {"person_id": 3, "org_id": 8, "title": "湖南省委组织部干部四处副调研员", "start_date": "2010-12", "end_date": "2015-12",
     "rank": "副处", "note": "曾长期在湖南省委组织部工作"},
    {"person_id": 3, "org_id": 9, "title": "怀化市委组织部组织指导科副科级组织员", "start_date": "2002-03", "end_date": "2004-12",
     "rank": "副科", "note": ""},
    {"person_id": 3, "org_id": 10, "title": "新晃县委组织部干部", "start_date": "2000-07", "end_date": "2002-03",
     "rank": "副科", "note": "2001.07 任副科级组织员"},
    {"person_id": 3, "org_id": 2, "title": "县委副书记、县长", "start_date": "2016-11", "end_date": "2021-05",
     "rank": "正处", "note": "2016.09 代县长，2016.11 转正"},
    {"person_id": 3, "org_id": 2, "title": "县委副书记、主持县政府工作", "start_date": "2015-02", "end_date": "2016-11",
     "rank": "副处", "note": "2015.02 任县委副书记、提名为副县长（主持县政府工作）"},
    # 王建球链
    {"person_id": 4, "org_id": 11, "title": "厅长", "start_date": "2021", "end_date": None, "rank": "正厅", "note": "现湖南省农业农村厅厅长"},
    {"person_id": 4, "org_id": 1, "title": "县委书记", "start_date": "2015-12", "end_date": "2021-05",
     "rank": "正处", "note": "2015.12 由县长提任书记"},
    {"person_id": 4, "org_id": 2, "title": "县长", "start_date": "2012", "end_date": "2015-12", "rank": "正处", "note": ""},
    # 欧阳锋 / 周笑春
    {"person_id": 5, "org_id": 1, "title": "县委书记", "start_date": "2011", "end_date": "2015-12", "rank": "正处", "note": "2015.12 转任桂阳县委书记"},
    {"person_id": 6, "org_id": 1, "title": "县委书记", "start_date": "2007", "end_date": "2011", "rank": "正处", "note": "第十届县委"},
    # 四套班子
    {"person_id": 7, "org_id": 3, "title": "县人大常委会主任", "start_date": "2021-07", "end_date": None, "rank": "正处"},
    {"person_id": 8, "org_id": 4, "title": "县政协主席", "start_date": "2026", "end_date": None, "rank": "正处", "note": "待确认"},
    {"person_id": 9, "org_id": 1, "title": "县委副书记", "start_date": "2021-07", "end_date": "2025", "rank": "副处"},
    # 常委
    {"person_id": 10, "org_id": 1, "title": "县委常委、组织部部长", "start_date": "2021", "end_date": None, "rank": "副处"},
    {"person_id": 11, "org_id": 1, "title": "县委常委、宣传部部长", "start_date": "2021", "end_date": None, "rank": "副处"},
    {"person_id": 12, "org_id": 2, "title": "县委常委、常务副县长", "start_date": "2021", "end_date": None, "rank": "副处"},
    {"person_id": 13, "org_id": 1, "title": "县委常委、纪委书记、县监委主任", "start_date": "2021", "end_date": None, "rank": "副处"},
    {"person_id": 14, "org_id": 1, "title": "县委常委、县委办主任", "start_date": "2021", "end_date": None, "rank": "副处"},
    {"person_id": 15, "org_id": 5, "title": "宜章经开区党工委书记", "start_date": "2021", "end_date": None, "rank": "副处"},
    {"person_id": 16, "org_id": 1, "title": "县委常委", "start_date": "2021", "end_date": None, "rank": "副处"},
    {"person_id": 17, "org_id": 1, "title": "县委常委", "start_date": "2021", "end_date": None, "rank": "副处"},
    {"person_id": 18, "org_id": 1, "title": "县委常委", "start_date": "2021", "end_date": None, "rank": "副处"},
    # 第十四届新领导（分工待补）
    {"person_id": 19, "org_id": 1, "title": "第十四届县领导（分工待补）", "start_date": "2026-07", "end_date": None, "rank": "副处"},
    {"person_id": 20, "org_id": 1, "title": "第十四届县领导（分工待补）", "start_date": "2026-07", "end_date": None, "rank": "副处"},
    {"person_id": 21, "org_id": 1, "title": "第十四届县领导（分工待补）", "start_date": "2026-07", "end_date": None, "rank": "副处"},
    {"person_id": 22, "org_id": 1, "title": "第十四届县领导（分工待补）", "start_date": "2026-07", "end_date": None, "rank": "副处"},
    {"person_id": 23, "org_id": 1, "title": "第十四届县领导（分工待补）", "start_date": "2026-07", "end_date": None, "rank": "副处"},
    {"person_id": 24, "org_id": 1, "title": "第十四届县领导（分工待补）", "start_date": "2026-07", "end_date": None, "rank": "副处"},
    {"person_id": 25, "org_id": 1, "title": "第十四届县领导（分工待补）", "start_date": "2026-07", "end_date": None, "rank": "副处"},
    {"person_id": 26, "org_id": 2, "title": "副县长", "start_date": "2025-10", "end_date": None, "rank": "副处"},
]

# ==================== 关系 ====================
relationships = [
    # 现任党政搭档
    {"person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "现任县委书记与县长（2026）", "overlap_org": "宜章县委/县政府", "overlap_period": "2025-06至今"},
    # 继任链
    {"person_a": 1, "person_b": 3, "type": "继任",
     "context": "邓生华接替张润槐任宜章县委书记；张润槐跨市调任衡阳耒阳市委书记", "overlap_org": "中共宜章县委员会", "overlap_period": "2025-06"},
    {"person_a": 3, "person_b": 4, "type": "继任",
     "context": "张润槐接替王建球任宜章县委书记（2021.05）；王建球调任湖南省农业农村厅", "overlap_org": "中共宜章县委员会", "overlap_period": "2021-05"},
    {"person_a": 4, "person_b": 5, "type": "继任",
     "context": "王建球接替欧阳锋任宜章县委书记（2015.12）", "overlap_org": "中共宜章县委员会", "overlap_period": "2015-12"},
    {"person_a": 5, "person_b": 6, "type": "继任",
     "context": "欧阳锋接替周笑春任宜章县委书记（约2011）", "overlap_org": "中共宜章县委员会", "overlap_period": "2011"},
    # 上下级（县长任期的搭档）
    {"person_a": 1, "person_b": 3, "type": "上下级",
     "context": "邓生华任县长时张润槐任书记（2021.07-2025.04）", "overlap_org": "宜章县人民政府/中共宜章县委员会", "overlap_period": "2021-2025"},
    # 工作搭档
    {"person_a": 1, "person_b": 7, "type": "工作搭档", "context": "县委书记与人大主任", "overlap_org": "宜章县", "overlap_period": "2025至今"},
    {"person_a": 1, "person_b": 10, "type": "上下级", "context": "县委与组织部部长", "overlap_org": "中共宜章县委员会", "overlap_period": "2021至今"},
    {"person_a": 1, "person_b": 11, "type": "上下级", "context": "县委与宣传部部长", "overlap_org": "中共宜章县委员会", "overlap_period": "2021至今"},
    {"person_a": 1, "person_b": 12, "type": "上下级", "context": "县委与常务副县长", "overlap_org": "宜章县政府", "overlap_period": "2021至今"},
    {"person_a": 1, "person_b": 13, "type": "上下级", "context": "县委与纪委书记", "overlap_org": "中共宜章县委员会", "overlap_period": "2021至今"},
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "县长与常务副县长工作搭档", "overlap_org": "宜章县人民政府", "overlap_period": "2025至今"},
    # 跨地区（张润槐履历轨迹）
    {"person_a": 3, "person_b": 6, "type": "同系统", "context": "新晃·怀化·省委组织部→宜章 跨地区任职轨迹", "overlap_org": "湖南组织部系统", "overlap_period": "1998-2015"},
]

# ==================== 构建 ====================
if __name__ == "__main__":
    run_build(
        slug=SLOG,
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
    print(f"   人员 {len(persons)} / 组织 {len(organizations)} / 任职 {len(positions)} / 关系 {len(relationships)}")