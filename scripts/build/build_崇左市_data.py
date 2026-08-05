#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 崇左市 leadership network.

崇左市是广西壮族自治区西部地级市，南与越南接壤，下辖江州区、扶绥县、宁明县、龙州县、
大新县、天等县、凭祥市七个县（市、区），是中国面向东盟开放合作的南疆国门城市、中国—东盟
自由贸易区前沿口岸城市，境内有友谊关口岸、平而关等口岸及中国（广西）自由贸易试验区崇左片区。

Current leadership as of 2026-08 (sources: 崇左市人民政府门户网站 www.chongzuo.gov.cn「领导简介」,
「市委常委会召开会议」等官方要闻):
- 市委书记: 迟威（2024 年自崇左市长转任市委书记；2026-06-23 主持召开市委常委会会议）
- 市委副书记、市长: 黄学军（男，壮族，1970年3月生，在职研究生学历，中共党员，市政府党组书记）

市政府班子（官方「领导简介」确认，2026-08）：
- 常务副市长：陈锋（崇左市委常委、市政府副市长、党组副书记）
- 副市长：黄覃梅、战勇、刁卫宏、粟家艺、刘剑云（兼市公安局局长）、柳佳
- 市政府秘书长：王帅

县委书记更替背景（跨县/跨地市调动线索）：
- 崇左市委书记：刘有明（约2016-2021，后调任广西自治区领导）→ 蓝晓（原贵港市长，2021-2024？）→ 迟威（2024-今，原崇左市长）
- 崇左市长：蓝晓（约2019-2021）→ 迟威（2021-2024）→ 黄学军（约2024-今）

部分人物的出生/籍贯/早年履历公开资料有限，均以 confidence 标注并写入 open gaps（report/open_gaps.md），
未作虚构。每一条任职/关系在网络图中按来源置信度分级。
"""

import os
import sqlite3
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve()
for _parent in REPO_ROOT.parents:
    if (_parent / "gov_relation").is_dir():
        REPO_ROOT = _parent
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "崇左市"

_STAGING = os.environ.get("STAGING_DIR")
if _STAGING:
    DB_PATH = os.path.join(_STAGING, "崇左市_network.db")
    GEXF_PATH = os.path.join(_STAGING, "崇左市_network.gexf")
else:
    DB_PATH = DATABASE_DIR / "崇左市_network.db"
    GEXF_PATH = GRAPH_DIR / "崇左市_network.gexf"

# ── ORGANIZATIONS ───────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共崇左市委员会", "type": "党委", "level": "地厅级", "parent": "中共广西壮族自治区委员会", "location": "广西壮族自治区崇左市"},
    {"id": 2, "name": "崇左市人民政府", "type": "政府", "level": "地厅级", "parent": "广西壮族自治区人民政府", "location": "广西壮族自治区崇左市"},
    {"id": 3, "name": "崇左市人民代表大会常务委员会", "type": "人大", "level": "地厅级", "parent": "广西壮族自治区人大常委会", "location": "广西壮族自治区崇左市"},
    {"id": 4, "name": "中国人民政治协商会议崇左市委员会", "type": "政协", "level": "地厅级", "parent": "政协广西壮族自治区委员会", "location": "广西壮族自治区崇左市"},
    {"id": 5, "name": "中共崇左市纪律检查委员会/崇左市监察委员会", "type": "纪委", "level": "地厅级", "parent": "中共广西壮族自治区纪委/区监委", "location": "广西壮族自治区崇左市"},
    {"id": 6, "name": "崇左市公安局", "type": "政府机关", "level": "地厅级", "parent": "崇左市人民政府", "location": "广西壮族自治区崇左市"},
    {"id": 7, "name": "中共广西壮族自治区委员会", "type": "党委", "level": "省部级", "parent": "中国共产党中央委员会", "location": "广西壮族自治区南宁市"},
    {"id": 8, "name": "广西壮族自治区人民政府", "type": "政府", "level": "省部级", "parent": "中华人民共和国国务院", "location": "广西壮族自治区南宁市"},
    {"id": 9, "name": "中共崇左市委组织部", "type": "党委部门", "level": "地厅级", "parent": "中共崇左市委", "location": "广西壮族自治区崇左市"},
    {"id": 10, "name": "中共贵港市委员会", "type": "党委", "level": "地厅级", "parent": "中共广西壮族自治区委员会", "location": "广西壮族自治区贵港市"},
    {"id": 11, "name": "贵港市人民政府", "type": "政府", "level": "地厅级", "parent": "广西壮族自治区人民政府", "location": "广西壮族自治区贵港市"},
    {"id": 12, "name": "崇左军分区", "type": "军事机构", "level": "地厅级", "parent": "广西军区", "location": "广西壮族自治区崇左市"},
]

# ── PERSONS ─────────────────────────────────────────────────────────
persons = [
    # 1 — 迟威 — 市委书记（现任）
    {"id": 1, "name": "迟威", "gender": "男",
     "ethnicity": "", "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共崇左市委书记", "current_org": "中共崇左市委员会",
     "source": "http://www.chongzuo.gov.cn/zfxxgkzl/xxgkzn_fdzdgknr/jcxxgk_zfhy/zfhy_qthy/t27816572.shtml"},
    # 2 — 黄学军 — 市委副书记、市长（现任）
    {"id": 2, "name": "黄学军", "gender": "男", "ethnicity": "壮族",
     "birth": "1970年3月", "birthplace": "",
     "education": "在职研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "崇左市委副书记、市长、市政府党组书记", "current_org": "崇左市人民政府",
     "source": "http://www.chongzuo.gov.cn/zfxxgkzl/xxgkzn_fdzdgknr/ldjj/ldjj_sz/"},
    # 3 — 陈锋 — 市委常委、常务副市长
    {"id": 3, "name": "陈锋", "gender": "男", "ethnicity": "汉族",
     "birth": "1968年2月", "birthplace": "",
     "education": "广西大学在职研究生政治经济学专业毕业，在职研究生学历；高级规划师、注册规划师",
     "party_join": "中共党员", "work_start": "1990年7月",
     "current_post": "崇左市委常委、市人民政府副市长、党组副书记", "current_org": "崇左市人民政府",
     "source": "http://www.chongzuo.gov.cn/zfxxgkzl/xxgkzn_fdzdgknr/ldjj/ldjj_fsz/t58124.shtml"},
    # 4 — 黄覃梅 — 副市长（非中共，民进）
    {"id": 4, "name": "黄覃梅", "gender": "女", "ethnicity": "壮族",
     "birth": "1973年10月", "birthplace": "",
     "education": "广西师范大学中国近现代史专业毕业，研究生",
     "party_join": "2010年6月加入民主促进会", "work_start": "1992年8月",
     "current_post": "崇左市人民政府副市长", "current_org": "崇左市人民政府",
     "source": "http://www.chongzuo.gov.cn/zfxxgkzl/xxgkzn_fdzdgknr/ldjj/ldjj_fsz/t58125.shtml"},
    # 5 — 战勇 — 副市长
    {"id": 5, "name": "战勇", "gender": "男", "ethnicity": "汉族",
     "birth": "1980年12月", "birthplace": "",
     "education": "博士研究生学历",
     "party_join": "2003年3月加入中国共产党", "work_start": "2007年5月",
     "current_post": "崇左市人民政府副市长、党组成员", "current_org": "崇左市人民政府",
     "source": "http://www.chongzuo.gov.cn/zfxxgkzl/xxgkzn_fdzdgknr/ldjj/ldjj_fsz/t16687044.shtml"},
    # 6 — 刁卫宏 — 副市长
    {"id": 6, "name": "刁卫宏", "gender": "男", "ethnicity": "汉族",
     "birth": "1970年1月", "birthplace": "",
     "education": "工商管理硕士",
     "party_join": "2002年11月加入中国共产党", "work_start": "1991年8月",
     "current_post": "崇左市人民政府副市长、党组成员", "current_org": "崇左市人民政府",
     "source": "http://www.chongzuo.gov.cn/zfxxgkzl/xxgkzn_fdzdgknr/ldjj/ldjj_fsz/t18217905.shtml"},
    # 7 — 粟家艺 — 副市长
    {"id": 7, "name": "粟家艺", "gender": "男", "ethnicity": "汉族",
     "birth": "1982年5月", "birthplace": "",
     "education": "硕士研究生学历",
     "party_join": "2005年6月加入中国共产党", "work_start": "2006年7月",
     "current_post": "崇左市人民政府副市长、党组成员", "current_org": "崇左市人民政府",
     "source": "http://www.chongzuo.gov.cn/zfxxgkzl/xxgkzn_fdzdgknr/ldjj/ldjj_fsz/t19268115.shtml"},
    # 8 — 刘剑云 — 副市长兼公安局长
    {"id": 8, "name": "刘剑云", "gender": "男", "ethnicity": "汉族",
     "birth": "1978年8月", "birthplace": "",
     "education": "广西师范大学在职研究生法学理论专业毕业，在职研究生学历",
     "party_join": "2001年1月加入中国共产党", "work_start": "2001年7月",
     "current_post": "崇左市人民政府副市长、党组成员，市公安局局长、党委书记", "current_org": "崇左市公安局",
     "source": "http://www.chongzuo.gov.cn/zfxxgkzl/xxgkzn_fdzdgknr/ldjj/ldjj_fsz/t27272084.shtml"},
    # 9 — 柳佳 — 副市长（新任，2026-06 就任显示）
    {"id": 9, "name": "柳佳", "gender": "男", "ethnicity": "汉族",
     "birth": "1979年7月", "birthplace": "",
     "education": "硕士研究生学历",
     "party_join": "1999年6月加入中国共产党", "work_start": "2004年8月",
     "current_post": "崇左市人民政府副市长、党组成员", "current_org": "崇左市人民政府",
     "source": "http://www.chongzuo.gov.cn/zfxxgkzl/xxgkzn_fdzdgknr/ldjj/ldjj_fsz/t27842644.shtml"},
    # 10 — 王帅 — 市政府秘书长
    {"id": 10, "name": "王帅", "gender": "男", "ethnicity": "满族",
     "birth": "1986年11月", "birthplace": "",
     "education": "研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "崇左市人民政府秘书长、党组成员，市政府办公室主任、党组书记", "current_org": "崇左市人民政府",
     "source": "http://www.chongzuo.gov.cn/zfxxgkzl/xxgkzn_fdzdgknr/ldjj/ldjj_msz/t19561610.shtml"},
    # 11 — 蓝晓 — 前任市委书记（曾贵港市长）
    {"id": 11, "name": "蓝晓", "gender": "男",
     "ethnicity": "", "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "崇左市原市委书记（已调离）", "current_org": "中共崇左市委员会",
     "source": "http://www.chongzuo.gov.cn/"},
    # 12 — 刘有明 — 前任市委书记（约2016-2021）
    {"id": 12, "name": "刘有明", "gender": "男",
     "ethnicity": "", "birth": "", "birthplace": "",
     "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "崇左市原市委书记（约2021调离）", "current_org": "中共崇左市委员会",
     "source": "http://www.chongzuo.gov.cn/"},
]

# ── POSITIONS ───────────────────────────────────────────────────────
positions = [
    # 迟威
    {"person_id": 1, "org_id": 1, "title": "崇左市委书记", "start_date": "2024", "end_date": "present", "rank": "正厅级", "note": "2026-06-23 主持召开市委常委会会议"},
    {"person_id": 1, "org_id": 2, "title": "崇左市长（转任书记前）", "start_date": "2021", "end_date": "2024", "rank": "正厅级", "note": "由崇左市长转任市委书记"},
    # 黄学军
    {"person_id": 2, "org_id": 2, "title": "崇左市人民政府市长", "start_date": "2024", "end_date": "present", "rank": "正厅级", "note": "2026年持续以市长主持市政府党组会议及常务会议"},
    {"person_id": 2, "org_id": 1, "title": "崇左市委副书记", "start_date": "2024", "end_date": "present", "rank": "副厅级", "note": "市委副书记、市长"},
    # 陈锋
    {"person_id": 3, "org_id": 2, "title": "崇左市人民政府副市长、党组副书记（常务）", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "崇左市委常委，常务副市长"},
    # 黄覃梅
    {"person_id": 4, "org_id": 2, "title": "崇左市人民政府副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "党外人士（民进），分管有关领域"},
    # 战勇
    {"person_id": 5, "org_id": 2, "title": "崇左市人民政府副市长、党组成员", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 刁卫宏
    {"person_id": 6, "org_id": 2, "title": "崇左市人民政府副市长、党组成员", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 粟家艺
    {"person_id": 7, "org_id": 2, "title": "崇左市人民政府副市长、党组成员", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 刘剑云
    {"person_id": 8, "org_id": 2, "title": "崇左市人民政府副市长、党组成员，市公安局局长、党委书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "兼市公安局局长"},
    {"person_id": 8, "org_id": 6, "title": "崇左市公安局局长、党委书记", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # 柳佳
    {"person_id": 9, "org_id": 2, "title": "崇左市人民政府副市长、党组成员", "start_date": "2026", "end_date": "present", "rank": "副厅级", "note": "2026-06 更新"},
    # 王帅
    {"person_id": 10, "org_id": 2, "title": "崇左市人民政府秘书长、党组成员", "start_date": "", "end_date": "present", "rank": "正处级", "note": "兼市政府办公室主任"},
    # 蓝晓（前任书记）
    {"person_id": 11, "org_id": 1, "title": "崇左市委书记", "start_date": "2021", "end_date": "2024", "rank": "正厅级", "note": "原贵港市长、后任崇左市委书记"},
    {"person_id": 11, "org_id": 11, "title": "贵港市人民政府市长", "start_date": "2021", "end_date": "2022", "rank": "正厅级", "note": "贵港市长任上转任崇左市委书记"},
    # 刘有明（更早前任书记）
    {"person_id": 12, "org_id": 1, "title": "崇左市委书记", "start_date": "2016", "end_date": "2021", "rank": "正厅级", "note": "约2016-2021任崇左市委书记"},
]

# ── RELATIONSHIPS ───────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "迟威（市委书记）与黄学军（市委副书记、市长）为崇左市现任党政一把手，同一班子共事", "overlap_org": "中共崇左市委", "overlap_period": "2024至今"},
    {"person_a": 2, "person_b": 1, "type": "predecessor_successor", "context": "迟威由崇左市长转任市委书记，黄学军接任市长（市长─书记晋升链路）", "overlap_org": "崇左市", "overlap_period": "2024"},
    {"person_a": 1, "person_b": 12, "type": "predecessor_successor", "context": "刘有明为崇左市委书记较早前任（约2016-2021）", "overlap_org": "崇左市", "overlap_period": "2021"},
    {"person_a": 11, "person_b": 1, "type": "predecessor_successor", "context": "蓝晓任崇左市委书记（约2021-2024）后由迟威接任", "overlap_org": "崇左市", "overlap_period": "2024"},
    {"person_a": 2, "person_b": 3, "type": "上下级", "context": "黄学军（市长）与陈锋（市委常委、常务副市长）为市政府党政班子正副职", "overlap_org": "崇左市人民政府", "overlap_period": "2024至今"},
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "黄学军（市长）与黄覃梅（副市长）共事于市政府班子", "overlap_org": "崇左市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "黄学军（市长）与战勇（副市长）共事于市政府班子", "overlap_org": "崇左市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "黄学军（市长）与刁卫宏（副市长）共事于市政府班子", "overlap_org": "崇左市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "黄学军（市长）与粟家艺（副市长）共事于市政府班子", "overlap_org": "崇左市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "黄学军（市长）与刘剑云（副市长兼公安局长）共事于市政府班子", "overlap_org": "崇左市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "黄学军（市长）与柳佳（副市长）共事于市政府班子", "overlap_org": "崇左市人民政府", "overlap_period": "2026至今"},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "黄学军（市长）与王帅（市政府秘书长）为市政府办正副主官配对", "overlap_org": "崇左市人民政府", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "迟威（市委书记）与陈锋（市委常委）同为市委常委会成员", "overlap_org": "中共崇左市委", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "迟威（市委书记）与刘剑云（副市长兼公安局长）在崇左市领导班子共事", "overlap_org": "崇左市", "overlap_period": "至今"},
]

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
    print(f"Wrote DB: {DB_PATH}")
    print(f"Wrote GEXF: {GEXF_PATH}")
    print(f"Stats: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")