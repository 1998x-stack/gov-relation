#!/usr/bin/env python3
"""滴道区(黑龙江省鸡西市)领导班子工作关系网络生成脚本.

基于滴道区人民政府门户网站 (www.didaoqu.gov.cn) 官方"走进滴道·区领导"页面、
官方图片/新闻稿、区人大任免公告及公开人物百科资料，构建滴道区区委、区政府、
区人大、区政协及纪委监委核心领导的 SQLite 数据库与 GEXF 关系图。

数据时间锚点：截至 2026-08。现任区委书记张旭、区委副书记/代区长王勇以官方
领导之窗与新闻为直接依据 (confirmed)。前任区长陈文波以 2026-01-30 政府工作报告
署名确认，其离职去向与张旭的前任书记因公开网络检索受限列为 open_questions。

来源：
- 滴道区人民政府门户 www.didaoqu.gov.cn（2026-08-05 访问）
- 区领导之窗页面 /ddq/dadd98ee7c7648c68a65ba2c0d3a1ba3/zjdd.shtml
- 区委书记张旭 2026-07 防汛调研新闻稿（来源:区委办）
- 区委副书记/代区长王勇 2026-07 调研新闻稿（来源:政府办）
- 滴道区第十七届人大常委会第三十八次会议公告（2026-07-08 王勇为代理区长）
- 滴道区 2026 年政府工作报告（2026-01-30 区长陈文波署名）
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

# 脚本位于 scripts/build/ 时向上一级到达仓库根
_HERE = Path(__file__).resolve().parent
_PROJECT_ROOT = _HERE.parents[1].resolve()

import sys
sys.path.insert(0, str(_PROJECT_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "滴道区"
DATE_TAG = datetime.now().strftime("%Y%m%d")

# process_tmp.py tokens: sqlite3, DB_PATH, GEXF_PATH
DB_PATH = DATABASE_DIR / "滴道区_network.db"
GEXF_PATH = GRAPH_DIR / "滴道区_network.gexf"

# ── 组织机构 ─────────────────────────────────────────────────────────
# id 避开 1-14 (人员使用 1-15, 机构从 101 起) 以保持人员/机构 id 不冲突
organizations = [
    {
        "id": 101,
        "name": "中共滴道区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共鸡西市委",
        "location": "黑龙江省鸡西市滴道区",
    },
    {
        "id": 102,
        "name": "滴道区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "鸡西市人民政府",
        "location": "黑龙江省鸡西市滴道区",
    },
    {
        "id": 103,
        "name": "滴道区人民代表大会",
        "type": "人大",
        "level": "县处级",
        "parent": "鸡西市人大",
        "location": "黑龙江省鸡西市滴道区",
    },
    {
        "id": 104,
        "name": "中国人民政治协商会议滴道区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协鸡西市委员会",
        "location": "黑龙江省鸡西市滴道区",
    },
    {
        "id": 105,
        "name": "滴道区纪委监委",
        "type": "党委",
        "level": "县处级",
        "parent": "中共鸡西市纪律检查委员会",
        "location": "黑龙江省鸡西市滴道区",
    },
    {
        "id": 106,
        "name": "中共鸡西市委",
        "type": "党委",
        "level": "地厅级",
        "parent": "中共黑龙江省委",
        "location": "黑龙江省鸡西市",
    },
    {
        "id": 107,
        "name": "中共鸡西市虎林市委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共鸡西市委",
        "location": "黑龙江省鸡西市虎林市",
    },
    {
        "id": 108,
        "name": "中共鸡西市鸡东县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共鸡西市委",
        "location": "黑龙江省鸡西市鸡东县",
    },
]

# ── 人员 ───────────────────────────────────────────────────
persons = [
    {
        "id": 1,
        "name": "张旭",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1985-02",
        "birthplace": "待查",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委书记",
        "current_org": "中共滴道区委员会",
        "source": "官方领导之窗 + 新闻稿(she委办) + 百科",
    },
    {
        "id": 2,
        "name": "王勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-07",
        "birthplace": "待查",
        "education": "省委党校研究生(公共管理)",
        "party_join": "2003-01",
        "work_start": "2005-06",
        "current_post": "区委副书记、代区长",
        "current_org": "滴道区人民政府",
        "source": "官方领导之窗/新闻稿(政府办)/百科/人大公告",
    },
    {
        "id": 3,
        "name": "关靖伟",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、政法委书记",
        "current_org": "中共滴道区委员会",
        "source": "官方领导之窗",
    },
    {
        "id": 4,
        "name": "王世斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、组织部部长、统战部部长",
        "current_org": "中共滴道区委员会",
        "source": "官方领导之窗",
    },
    {
        "id": 5,
        "name": "金永海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、纪委书记、监委主任",
        "current_org": "中共滴道区纪律检查委员会",
        "source": "官方领导之窗",
    },
    {
        "id": 6,
        "name": "李婷婷",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、宣传部部长",
        "current_org": "中共滴道区委员会",
        "source": "官方领导之窗",
    },
    {
        "id": 7,
        "name": "姜天宇",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "滴道区人民政府",
        "source": "官方领导之窗",
    },
    {
        "id": 8,
        "name": "栗明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "滴道区人民政府",
        "source": "官方领导之窗",
    },
    {
        "id": 9,
        "name": "苏珊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区人民武装部上校部长",
        "current_org": "滴道区人民武装部",
        "source": "官方领导之窗",
    },
    {
        "id": 10,
        "name": "程显峰",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会主任、党组书记",
        "current_org": "滴道区人民代表大会",
        "source": "官方领导之窗",
    },
    {
        "id": 11,
        "name": "赵淑梅",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协主席、党组书记",
        "current_org": "中国人民政治协商会议滴道区委员会",
        "source": "官方领导之窗",
    },
    {
        "id": 12,
        "name": "邢长昊",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政府副区长",
        "current_org": "滴道区人民政府",
        "source": "官方领导之窗",
    },
    {
        "id": 13,
        "name": "李云鹤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政府副区长、公安分局党委书记、局长",
        "current_org": "滴道区人民政府",
        "source": "官方领导之窗",
    },
    {
        "id": 14,
        "name": "曹华",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区政府副区长",
        "current_org": "滴道区人民政府",
        "source": "官方领导之窗",
    },
    {
        "id": 15,
        "name": "陈文波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（前任区长，2026 年上半年离任）",
        "current_org": "滴道区人民政府",
        "source": "2026-01-30 区政府工作报告署名",
    },
]

# ── 任职 ───────────────────────────────────────────────────
positions = [
    # 张旭
    {"person_id": 1, "org_id": 108, "title": "鸡东县委常委、副县长", "start_date": "", "end_date": "2024-09", "rank": "副处级", "note": "百度百科记载其任鸡东县领导职务"},
    {"person_id": 1, "org_id": 101, "title": "滴道区委书记", "start_date": "2024-10", "end_date": "present", "rank": "正处级", "note": "2026-07以区委书记身份公开调研 (confirmed)"},
    # 王勇
    {"person_id": 2, "org_id": 102, "title": "滴道区政府副区长", "start_date": "2021-08", "end_date": "2026-06", "rank": "副处级", "note": "2021-07-29 拟任县（市）区政府副职公示，后任副区长"},
    {"person_id": 2, "org_id": 102, "title": "区委副书记、区政府代区长、区政府党组书记", "start_date": "2026-07", "end_date": "present", "rank": "正处级", "note": "2026-07-08 人大常委会第三十八次会议决定为代理区长 (confirmed)"},
    {"person_id": 2, "org_id": 107, "title": "虎林市阿北乡党委书记", "start_date": "", "end_date": "2021", "rank": "正科级", "note": "2021-07-29 拟任届县市区政府副职公示时身份为阿北乡党委书记"},
    # 关靖伟
    {"person_id": 3, "org_id": 101, "title": "区委副书记、政法委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 王世斌
    {"person_id": 4, "org_id": 101, "title": "区委常委、组织部部长、统战部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 金永海
    {"person_id": 5, "org_id": 105, "title": "区委常委、纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 李婷婷
    {"person_id": 6, "org_id": 101, "title": "区委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 姜天宇
    {"person_id": 7, "org_id": 102, "title": "区委常委、副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 栗明
    {"person_id": 8, "org_id": 102, "title": "区委常委、副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 苏珊
    {"person_id": 9, "org_id": 101, "title": "区委常委、区人民武装部上校部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 程显峰
    {"person_id": 10, "org_id": 103, "title": "区人大常委会主任、党组书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 赵淑梅
    {"person_id": 11, "org_id": 104, "title": "区政协主席、党组书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    # 邢长昊
    {"person_id": 12, "org_id": 102, "title": "区政府副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 李云鹤
    {"person_id": 13, "org_id": 102, "title": "区政府副区长、公安分局党委书记、局长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 曹华
    {"person_id": 14, "org_id": 102, "title": "区政府副区长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 陈文波
    {"person_id": 15, "org_id": 102, "title": "滴道区区长", "start_date": "", "end_date": "2026-06", "rank": "正处级", "note": "2026-01-30 作政府工作报告；2026 上半年离任（去向待查）"},
    # 王勇 与 鸡西市委的上下级
    {"person_id": 2, "org_id": 106, "title": "接受中共鸡西市委领导（区领导）", "start_date": "2026-07", "end_date": "present", "rank": "", "note": ""},
    # 张旭 与 鸡西市委
    {"person_id": 1, "org_id": 106, "title": "接受中共鸡西市委领导（区委书记）", "start_date": "", "end_date": "present", "rank": "", "note": ""},
]

# ── 关系 ───────────────────────────────────────────────────
relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "共事",
        "context": "区委书记—区政府代区长，党政一把手搭档，共治理区",
        "overlap_org": "中共滴道区委员会/滴道区人民政府",
        "overlap_period": "2026-07 至今",
    },
    {
        "person_a": 2,
        "person_b": 15,
        "type": "前任继任",
        "context": "陈文波离任区长后，王勇于 2026-07-08 经人大常委会决定为代理区长",
        "overlap_org": "滴道区人民政府",
        "overlap_period": "2026",
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "上下级",
        "context": "张旭为区委书记，关靖伟为区委副书记/政法委书记，班子内上下级",
        "overlap_org": "中共滴道区委员会",
        "overlap_period": "至今",
    },
    {
        "person_a": 1,
        "person_b": 5,
        "type": "班子共事",
        "context": "区委书记与纪委书记、监委主任同班子",
        "overlap_org": "中共滴道区委员会",
        "overlap_period": "至今",
    },
    {
        "person_a": 2,
        "person_b": 13,
        "type": "上下级",
        "context": "政府一把手与副区长/公安局长",
        "overlap_org": "滴道区人民政府",
        "overlap_period": "2026-07 至今",
    },
    {
        "person_a": 2,
        "person_b": 7,
        "type": "班子共事",
        "context": "政府主要负责人与副区长（姜天宇兼管区财政局、发改、投资等）",
        "overlap_org": "滴道区人民政府",
        "overlap_period": "至今",
    },
    {
        "person_a": 1,
        "person_b": 2,
        "type": "cross_region_rotation",
        "context": "跨区县调入：张旭（原鸡东县常委/副县长）/ 王勇（原虎林市乡书记）先后到滴道区，属鸡西市内跨区县干部交流",
        "overlap_org": "鸡西市组织系统",
        "overlap_period": "2024—2026",
    },
]

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

print(f"✅ 写入 {DB_PATH}")
print(f"✅ 写入 {GEXF_PATH}")
print(f"人员 {len(persons)}、机构 {len(organizations)}、任职 {len(positions)}、关系 {len(relationships)}")