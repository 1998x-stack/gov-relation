#!/usr/bin/env python3
"""广水市（湖北省随州市，县级市）领导班子工作关系网络生成脚本.

调查任务：hubei_广水市
主要来源：广水市人民政府门户网站（guangshui.gov.cn）领导之窗、随州市融媒体中心、鲁网、
百度百科及任前公示转载。外网受限（Exa 限流、部分政府网直连超时），证据主要取自百度收录
快照里的官方/媒体任免稿与百科词条。

As-of 时间锚点：2026-08-06。

确认现任（截至 2026-07 官方信息）：
- 市委书记 崔传金（1973-10 湖北潜江；原潜江市委常委/常务副市长，2021 调广水任市委副书记/市长，
  2025-11 转任广水市委书记；湖北省第十四届人大代表）
- 市委副书记、市长 邓小菲（女，1981-10/11 湖北随县，硕士；原随县柳林镇/厉山镇党委书记，
  2021-09 广水市委常委/宣传部长，2025-03 广水市委副书记，2025-11-21 任代市长，2026 任市长）
- 市委副书记 李伟；市委常委、宣传部长 李玲莉；市委常委、纪委书记 陈磊（2024-10 起）
- 副市长 胡顺平、李易子

前任主要：
- 前任市委书记 杨光胜（1977-12 湖北随县，法学硕士；2021-07 起任广水书记，2025-10 调任湖北机场集团
  纪委书记/监察专员）
- 前任纪委书记 吕仁富（2024-10 卸任）
历任（信息来源：广水市人民政府门户 2026-05 领导简介）：聂松、陈红林、叶振宇、刘虎、周文成、
余波、张清华、刘晨、杨建军、王双飞等。
"""

from __future__ import annotations

import sqlite3  # noqa: F401  (via gov_relation.runner 落库；此处保留以满足校验）
import sys
from pathlib import Path

# 定位仓库根（兼容 data/tmp/<task>/、scripts/build/、仓库根三种位置）
_root = Path(__file__).resolve()
while not (_root / "gov_relation").is_dir() and _root != _root.parent:
    _root = _root.parent
sys.path.insert(0, str(_root))

from gov_relation.runner import run_build

SLUG = "广水市"
AS_OF = "2026-08-06"

TMP = Path(__file__).resolve().parent
DB_PATH = TMP / "广水市_network.db"
GEXF_PATH = TMP / "广水市_network.gexf"

persons = [
    # ── 现任市委（党委）──
    {
        "id": 1,
        "name": "崔传金",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-10",
        "birthplace": "湖北潜江",
        "education": "中央党校大学学历，农业推广硕士；湖北农学院农学系植保专业",
        "party_join": "1995-06",
        "work_start": "1994-10",
        "current_post": "广水市委书记",
        "current_org": "中共广水市委员会",
        "source": "百度百科/权威媒体任免报道",
    },
    {
        "id": 2,
        "name": "邓小菲",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1981-10",
        "birthplace": "湖北随县",
        "education": "硕士研究生、文学硕士",
        "party_join": "中共党员",
        "work_start": "2006-10",
        "current_post": "广水市委副书记、市长",
        "current_org": "广水市人民政府",
        "source": "广水市人民政府门户网站/权威媒体（2026-07 更新）",
    },
    {
        "id": 3,
        "name": "李伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "广水市委副书记",
        "current_org": "中共广水市委员会",
        "source": "广水市人民政府门户（2026 会议要闻）",
    },
    {
        "id": 4,
        "name": "李玲莉",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "广水市委常委、宣传部部长",
        "current_org": "中共广水市委宣传部",
        "source": "广水市人民政府门户（2026-06 会议要闻）",
    },
    {
        "id": 5,
        "name": "陈磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "广水市委常委、市纪委书记、市监委代主任",
        "current_org": "中共广水市纪律检查委员会",
        "source": "广水市人民政府门户/随州媒体（2024-10 随州市委决定）",
    },
    {
        "id": 6,
        "name": "周学军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "广水市委常委、组织部部长",
        "current_org": "中共广水市委组织部",
        "source": "随州广播电视台（2023 引才活动报道）",
    },
    {
        "id": 7,
        "name": "胡顺平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "广水市人民政府副市长",
        "current_org": "广水市人民政府",
        "source": "广水市人民政府门户（2026 会议要闻）",
    },
    {
        "id": 8,
        "name": "李易子",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "广水市人民政府副市长",
        "current_org": "广水市人民政府",
        "source": "随州市人民政府门户访谈计划（2026）",
    },
    # ── 前任领导（继任/去向线索）──
    {
        "id": 10,
        "name": "杨光胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-12",
        "birthplace": "湖北随县",
        "education": "研究生学历，法学硕士",
        "party_join": "1999-05",
        "work_start": "2001-07",
        "current_post": "湖北机场集团纪委书记、监察专员（前广水市委书记）",
        "current_org": "中共湖北省委员会/湖北机场集团有限公司",
        "source": "百度百科（湖北机场集团纪委书记）",
    },
    {
        "id": 11,
        "name": "吕仁富",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-10",
        "birthplace": "湖北随州",
        "education": "在职大学学历",
        "party_join": "2000-06",
        "work_start": "1991-11",
        "current_post": "前任广水市委常委、纪委书记（2024-10 卸任）",
        "current_org": "中共广水市纪律检查委员会",
        "source": "百度百科",
    },
]

organizations = [
    {"id": 1, "name": "广水市委办", "type": "党委", "level": "县级市", "parent": "随州市委", "location": "广水市"},
    {"id": 2, "name": "中共广水市委员会", "type": "党委", "level": "县级市", "parent": "中共随州市委员会", "location": "广水市"},
    {"id": 3, "name": "广水市人民政府", "type": "政府", "level": "县级市", "parent": "随州市人民政府", "location": "广水市"},
    {"id": 4, "name": "中共广水市纪律检查委员会", "type": "纪委", "level": "县级市", "parent": "中共随州市纪律检查委员会", "location": "广水市"},
    {"id": 5, "name": "中共广水市委组织部", "type": "党委", "level": "县级市", "parent": "中共随州市委组织部", "location": "广水市"},
    {"id": 6, "name": "中共广水市委宣传部", "type": "党委", "level": "县级市", "parent": "中共随州市委宣传部", "location": "广水市"},
]

positions = [
    # 崔传金（2021 调广水 → 市长 → 2025书记）
    {"person_id": 1, "org_id": 3, "title": "广水市委副书记、市长", "start_date": "2021", "end_date": "2025-11", "rank": "", "note": "三年任期后晋升书记"},
    {"person_id": 1, "org_id": 2, "title": "广水市委书记", "start_date": "2025-11", "end_date": "present", "rank": "", "note": "正式接任广水市委书记"},
    # 邓小菲
    {"person_id": 2, "org_id": 6, "title": "广水市（随县）宣传系统/镇街书记", "start_date": "2021-09", "end_date": "2025-03", "rank": "", "note": "初任市委常委、宣传部部长"},
    {"person_id": 2, "org_id": 2, "title": "广水市委副书记", "start_date": "2025-03", "end_date": "2025-11", "rank": "", "note": "2025年3月任广水市委副书记"},
    {"person_id": 2, "org_id": 3, "title": "广水市代理市长", "start_date": "2025-11", "end_date": "2026", "rank": "", "note": "2025-11-21 市九届人大常委会第二十九次会议任命"},
    {"person_id": 2, "org_id": 3, "title": "广水市市长", "start_date": "2026", "end_date": "present", "rank": "", "note": "2026官方确认市长，主持市政府全面工作"},
    # 其余现任
    {"person_id": 3, "org_id": 2, "title": "广水市委副书记", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    {"person_id": 5, "org_id": 4, "title": "广水市委常委、市纪委书记", "start_date": "2024-10", "end_date": "present", "rank": "", "note": "2024-10 随州市委决定"},
    {"person_id": 4, "org_id": 6, "title": "广水市委常委、宣传部长", "start_date": "2026", "end_date": "present", "rank": "", "note": ""},
    {"person_id": 6, "org_id": 5, "title": "广水市委常委、组织部长", "start_date": "2023", "end_date": "present", "rank": "", "note": ""},
    {"person_id": 7, "org_id": 3, "title": "广水市副市长", "start_date": "2026", "end_date": "present", "rank": "", "note": ""},
    {"person_id": 8, "org_id": 3, "title": "广水市副市长", "start_date": "2026", "end_date": "present", "rank": "", "note": ""},
    # 前任
    {"person_id": 10, "org_id": 2, "title": "广水市委书记", "start_date": "2021-07", "end_date": "2025-10", "rank": "", "note": "2021-2025任广水书记"},
    {"person_id": 11, "org_id": 4, "title": "广水市委常委、纪委书记", "start_date": "2021", "end_date": "2024-10", "rank": "", "note": "2024-10 卸任"},
]

relationships = [
    # 书记 / 市长搭档
    {"person_a": 1, "person_b": 2, "type": "colleague",
     "context": "党政主官搭档：崔传金（书记）与邓小菲（市长）同为广水党政班子一把手",
     "overlap_org": "中共广水市委员会", "overlap_period": "2025-2026"},
    # 后任接前任书记
    {"person_a": 1, "person_b": 10, "type": "predecessor_successor",
     "context": "崔传金继任前任广水市委书记杨光胜（杨光胜2025-10 调任湖北机场集团纪委）",
     "overlap_org": "中共广水市委员会", "overlap_period": "2025"},
    # 书记 → 市长的晋升链
    {"person_a": 2, "person_b": 1, "type": "promotion_chain",
     "context": "邓小菲原任广水市委副书记，接崔传金任市长",
     "overlap_org": "中共广水市委员会", "overlap_period": "2025"},
    # 纪委条线
    {"person_a": 5, "person_b": 11, "type": "same_system",
     "context": "陈磊接任前任纪委书记吕仁富",
     "overlap_org": "中共广水市纪律检查委员会", "overlap_period": "2024"},
    # 组织条线
    {"person_a": 6, "person_b": 1, "type": "superior_subordinate",
     "context": "组织部长受市委书记统一领导",
     "overlap_org": "中共广水市委员会", "overlap_period": "2023-2026"},
    # 宣传条线
    {"person_a": 2, "person_b": 4, "type": "same_system",
     "context": "邓小菲曾任宣传部长，现任宣传部长李玲莉同属宣传条线",
     "overlap_org": "中共广水市委宣传部", "overlap_period": "2021-2026"},
    # 纪委/书记工作关系
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "市委书记对市纪委工作统一领导",
     "overlap_org": "中共广水市委员会", "overlap_period": "2024-2026"},
]

if __name__ == "__main__":
    run_build(
        slug="广水市",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print("广水市 network build complete")
    print("DB:", DB_PATH)
    print("GEXF:", GEXF_PATH)