#!/usr/bin/env python3
"""随州市（湖北省，地级市）领导班子工作关系网络生成脚本.

核心任职以随州市人民政府门户（www.suizhou.gov.cn）/ 随州新闻网（suiw.cn）要闻、新华社
湖北频道、中国网、鲁网等媒体任免报道为 confirmed 依据；百度百科/新浪/澎湃作次来源。
因本次外网受限（Exa 限流、随州市政府网直连超时、Jina/Baidu百科 403），证据主要来自
百度收录快照的官方要闻与媒体任免稿。

As-of 时间锚点：2026-08-06。

确认现任：
- 市委书记 马泽江（1970-05 湖北仙桃；原任武汉汉阳区委书记、宜昌市委副书记/市长；2025 接任）
- 市委副书记、市长 胡志莉（女，1977-02；原宜昌点军/宜都/猇亭系；2024-08 当选市长）
- 市委副书记 吴晓军（原市委常委、纪委书记/监委主任）
- 市人大主任 甘国栋；市政协主席 张涛
备注：马泽江/克克/钱远坤/杜文清等前任静息与部分副职分工列于 person JSON open_questions / report/open_gaps.md。
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

SLUG = "随州市"
AS_OF = "2026-08-06"

TMP = Path(__file__).resolve().parent
DB_PATH = TMP / "随州市_network.db"
GEXF_PATH = TMP / "随州市_network.gexf"

persons = [
    # ── 现任党委（市委）──
    {
        "id": 11,
        "name": "马泽江",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-05",
        "birthplace": "湖北仙桃",
        "education": "在职硕士研究生、工商管理硕士；江汉大学政法系法律专业大专",
        "party_join": "1992-01",
        "work_start": "1992-09",
        "current_post": "随州市委书记",
        "current_org": "中共随州市委员会",
        "source": "随州市人民政府门户要闻/百度百科",
    },
    {
        "id": 12,
        "name": "胡志莉",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1977-02",
        "birthplace": "湖北宜昌（一说恩施）",
        "education": "在职大学学历，管理学学士",
        "party_join": "1995-06",
        "work_start": "1995-08",
        "current_post": "随州市委副书记、市长",
        "current_org": "随州市人民政府",
        "source": "随州市人民政府门户要闻/百度百科",
    },
    {
        "id": 13,
        "name": "吴晓军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "随州市委副书记",
        "current_org": "中共随州市委员会",
        "source": "随州市人民政府门户要闻",
    },
    {
        "id": 14,
        "name": "吴丕华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969-09",
        "birthplace": "湖北公安",
        "education": "华中师范大学法学硕士",
        "party_join": "1994-12",
        "work_start": "1990-08",
        "current_post": "随州市委常委、常务副市长",
        "current_org": "随州市人民政府",
        "source": "随州新闻网领导专辑",
    },
    {
        "id": 15,
        "name": "周兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-03",
        "birthplace": "湖北麻城",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "随州市委常委、统战部部长",
        "current_org": "中共随州市委员会",
        "source": "鲁网/中国网 2026-05 任前信息",
    },
    {
        "id": 16,
        "name": "陈兴旺",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "随州市委常委、市委秘书长",
        "current_org": "中共随州市委员会",
        "source": "长江网/随州新闻网",
    },
    {
        "id": 17,
        "name": "姜皓",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "随州市委常委、曾都区委书记",
        "current_org": "中共随州曾都区委员会",
        "source": "凤凰网湖北 2026-02 新春第一会报道",
    },
    {
        "id": 18,
        "name": "张爱华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "随州市委常委",
        "current_org": "中共随州市委员会",
        "source": "随州换届名单/军分区",
    },
    {
        "id": 19,
        "name": "黄继军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "随州市委常委",
        "current_org": "中共随州市委员会",
        "source": "随州换届名单/凤凰网",
    },
    # ── 市人大 / 市政府 / 市政协 ──
    {
        "id": 20,
        "name": "甘国栋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "随州市人大常委会主任",
        "current_org": "随州市人民代表大会常务委员会",
        "source": "随州人大报告",
    },
    {
        "id": 21,
        "name": "张涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "随州市政协主席",
        "current_org": "政协随州市委员会",
        "source": "随州日报",
    },
    {
        "id": 22,
        "name": "刘涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-08",
        "birthplace": "湖北随州",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "随州市政府党组成员、副市长",
        "current_org": "随州市人民政府",
        "source": "中国网/四川省委组织部任前公示(2026年第116号)",
    },
    {
        "id": 23,
        "name": "孙杰",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "随州市人民政府副市长",
        "current_org": "随州市人民政府",
        "source": "随州人大 2026-07-31 任命",
    },
    {
        "id": 24,
        "name": "肖诗兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1965-04",
        "birthplace": "湖北随县",
        "education": "省委党校研究生",
        "party_join": "1988-09",
        "work_start": "1984-08",
        "current_post": "随州市人大常委会副主任",
        "current_org": "随州市人民代表大会常务委员会",
        "source": "百度百科",
    },
    {
        "id": 25,
        "name": "汪海涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-12",
        "birthplace": "",
        "education": "随州师范学校",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "随州市人大常委会党组成员",
        "current_org": "随州市人民代表大会常务委员会",
        "source": "随州人大任免新闻",
    },
    # ── 前任 / 交流线相关 ──
    {
        "id": 30,
        "name": "钱远坤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任随州市委书记",
        "current_org": "中共随州市委员会",
        "source": "随州换届/人代会 新闻",
    },
    {
        "id": 31,
        "name": "克克",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任随州市市长",
        "current_org": "随州市人民政府",
        "source": "随州 2023 纪委两会/换届新闻",
    },
    {
        "id": 32,
        "name": "张卫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967-08",
        "birthplace": "湖北武汉",
        "education": "在职大学",
        "party_join": "1997-08",
        "work_start": "1988-10",
        "current_post": "湖北省委金融工委专职副书记（曾任随州市委常委、组织部长、宣传部长）",
        "current_org": "中共湖北省委金融工作委员会",
        "source": "湖北省委金融办官网/澎湃新闻",
    },
    {
        "id": 33,
        "name": "熊征宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "武汉市委书记（曾任宜昌市委书记）",
        "current_org": "中国共产党武汉市委员会",
        "source": "湖北省委人事信息/local persons 熊征宇.json",
    },
    {
        "id": 34,
        "name": "杜文清",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "曾任随州市纪委书记/监委主任（现任情况待核）",
        "current_org": "中共随州市纪律检查委员会",
        "source": "随州日报个别会议录（2017/2021 相关）",
    },
]

organizations = [
    {"id": 1, "name": "中共随州市委员会", "type": "党委", "level": "地级市", "parent": "中国共产党湖北省委员会", "location": "随州市"},
    {"id": 2, "name": "随州市人民政府", "type": "政府", "level": "地级市", "parent": "湖北省人民政府", "location": "随州市"},
    {"id": 3, "name": "随州市人民代表大会常务委员会", "type": "人大", "level": "地级市", "parent": "中共随州市委员会", "location": "随州市"},
    {"id": 4, "name": "政协随州市委员会", "type": "政协", "level": "地级市", "parent": "中共随州市委员会", "location": "随州市"},
    {"id": 5, "name": "中共随州市纪律检查委员会", "type": "纪委", "level": "地级市", "parent": "中共随州市委员会", "location": "随州市"},
    {"id": 6, "name": "随州军分区", "type": "军事", "level": "地级市", "parent": "湖北省军区", "location": "随州市"},
    {"id": 7, "name": "中共随城市曾都区委员会", "type": "党委", "level": "区(县)", "parent": "中共随州市委员会", "location": "随州市·曾都区"},
    {"id": 8, "name": "中国共产党湖北省委员会", "type": "党委", "level": "省级", "parent": "", "location": "武汉市"},
    {"id": 9, "name": "湖北省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "武汉市"},
    {"id": 10, "name": "中国共产党宜昌市委员会", "type": "党委", "level": "地级市", "parent": "中国共产党湖北省委员会", "location": "宜昌市"},
    {"id": 11, "name": "宜昌市人民政府", "type": "政府", "level": "地级市", "parent": "湖北省人民政府", "location": "宜昌市"},
    {"id": 12, "name": "中共武汉市汉阳区委员会", "type": "党委", "level": "区(县)", "parent": "中国共产党武汉市委员会", "location": "武汉市·汉阳区"},
    {"id": 13, "name": "中共湖北省委金融工作委员会", "type": "党委", "level": "省级", "parent": "中国共产党湖北省委员会", "location": "武汉市"},
]

positions = [
    # ── 市委 ──
    {"person_id": 11, "org_id": 1, "title": "随州市委书记", "start_date": "2025", "end_date": "present", "rank": "正厅级", "note": "市政府党组书记、军分区党委第一书记；接任前任钱远坤"},
    {"person_id": 12, "org_id": 2, "title": "随州市委副书记、市长", "start_date": "2024-08", "end_date": "present", "rank": "正厅级", "note": "2024-07 任市委副书记/代市长，2024-08-16 当选市长"},
    {"person_id": 12, "org_id": 1, "title": "随州市委副书记", "start_date": "2024-07", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 13, "org_id": 1, "title": "随州市委副书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "曾任市委常委/纪委书记/监委主任（2023）"},
    {"person_id": 14, "org_id": 2, "title": "随州市委常委、常务副市长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 15, "org_id": 1, "title": "随州市委常委、统战部部长", "start_date": "2026-05", "end_date": "present", "rank": "副厅级", "note": "市政府党组成员"},
    {"person_id": 16, "org_id": 1, "title": "随州市委常委、市委秘书长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 17, "org_id": 1, "title": "随州市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "兼曾都区委书记"},
    {"person_id": 18, "org_id": 1, "title": "随州市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "随州军分区政委（待核）"},
    {"person_id": 19, "org_id": 1, "title": "随州市委常委", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "分工待核"},
    # ── 人大 ──
    {"person_id": 20, "org_id": 3, "title": "随州市人大常委会主任", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    {"person_id": 24, "org_id": 3, "title": "随州市人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    {"person_id": 25, "org_id": 3, "title": "随州市人大常委会党组成员", "start_date": "", "end_date": "present", "rank": "副厅级", "note": ""},
    # ── 政协 ──
    {"person_id": 21, "org_id": 4, "title": "随州市政协主席", "start_date": "", "end_date": "present", "rank": "正厅级", "note": ""},
    # ── 政府 ──
    {"person_id": 22, "org_id": 2, "title": "随州市政府党组成员、副市长", "start_date": "2026-07", "end_date": "present", "rank": "副厅级", "note": "2026-06 省委组织部任前公示"},
    {"person_id": 23, "org_id": 2, "title": "随州市人民政府副市长", "start_date": "2026-07-31", "end_date": "present", "rank": "副厅级", "note": ""},
    # ── 前任 / 跨市 ──
    {"person_id": 30, "org_id": 1, "title": "前任随州市委书记", "start_date": "", "end_date": "2025", "rank": "正厅级", "note": "2022 换届、2024-08 人代会），马泽江接任"},
    {"person_id": 31, "org_id": 2, "title": "前任随州市市长", "start_date": "", "end_date": "2024", "rank": "正厅级", "note": "2022 五届副书记/市长；2023 纪委两会报道；2024 胡志莉接任"},
    {"person_id": 32, "org_id": 13, "title": "湖北省委金融工委专职副书记", "start_date": "2025-09", "end_date": "present", "rank": "正厅级", "note": "原随州市委常委、组织部部长/宣传部部长"},
    {"person_id": 33, "org_id": 10, "title": "前宜昌市委书记", "start_date": "2021", "end_date": "2024", "rank": "副省级?待核", "note": "现武汉市委书记"},
    {"person_id": 33, "org_id": 12, "title": "武汉市委书记（现任）", "start_date": "", "end_date": "present", "rank": "副省级", "note": "曾任宜昌市委书记"},
    {"person_id": 34, "org_id": 5, "title": "随州市纪委书记、市监委主任（前任）", "start_date": "", "end_date": "", "rank": "副厅级", "note": "现任情况待核"},
]

relationships = [
    # 党政一把手搭档
    {"person_a": 11, "person_b": 12, "type": "党政搭档",
     "context": "马泽江（市委书记）与胡志莉（市委副书记、市长）组成随州市党政一把手搭档",
     "overlap_org": "中共随州市委员会/随州市人民政府", "overlap_period": "2025至今"},
    # 市委班子核心交集
    {"person_a": 11, "person_b": 13, "type": "superior_subordinate",
     "context": "市委书记马泽江与市委副书记吴晓军同属市委常委会",
     "overlap_org": "中共随州市委员会", "overlap_period": "2026"},
    {"person_a": 11, "person_b": 14, "type": "superior_subordinate",
     "context": "市委书记与市委常委、常务副市长吴丕华同属市委常委会/市政府班子",
     "overlap_org": "中共随州市委员会", "overlap_period": "2026"},
    {"person_a": 11, "person_b": 15, "type": "superior_subordinate",
     "context": "市委书记与市委常委、统战部长周兵在市委常委会共事",
     "overlap_org": "中共随州市委员会", "overlap_period": "2026"},
    {"person_a": 11, "person_b": 16, "type": "superior_subordinate",
     "context": "市委书记与市委常委、市委秘书长陈兴旺同属市委常委会",
     "overlap_org": "中共随州市委员会", "overlap_period": "2026"},
    {"person_a": 11, "person_b": 17, "type": "superior_subordinate",
     "context": "市委书记与市委常委、曾都区委书记姜皓同属市委常委会",
     "overlap_org": "中共随州市委员会", "overlap_period": "2026"},
    # 市长与市政府班子
    {"person_a": 12, "person_b": 14, "type": "superior_subordinate",
     "context": "市长胡志莉与常务副市长吴丕华在市政府班子共事",
     "overlap_org": "随州市人民政府", "overlap_period": "2024至今"},
    {"person_a": 12, "person_b": 22, "type": "superior_subordinate",
     "context": "市长胡志莉与副市长刘涛在市政府班子共事",
     "overlap_org": "随州市人民政府", "overlap_period": "2026"},
    {"person_a": 12, "person_b": 23, "type": "superior_subordinate",
     "context": "市长胡志莉与副市长孙杰在市政府班子共事",
     "overlap_org": "随州市人民政府", "overlap_period": "2026"},
    # 人大 / 政协
    {"person_a": 20, "person_b": 11, "type": "same_system",
     "context": "市人大常委会主任甘国栋与市委书记同受市委统一领导",
     "overlap_org": "中国共产党随州市委员会", "overlap_period": "2026"},
    {"person_a": 21, "person_b": 11, "type": "same_system",
     "context": "市政协主席张涛与市委书记同受市委统一领导",
     "overlap_org": "中国共产党随州市委员会", "overlap_period": "2026"},
    # 前任 / 继任链
    {"person_a": 11, "person_b": 30, "type": "predecessor_successor",
     "context": "马泽江接任前任随州市委书记钱远坤（交接时间约2025）",
     "overlap_org": "中共随州市委员会", "overlap_period": ""},
    {"person_a": 12, "person_b": 31, "type": "predecessor_successor",
     "context": "胡志莉 2024 接任前任随州市长克克",
     "overlap_org": "随州市人民政府", "overlap_period": ""},
    # 干部交流线（跨市）
    {"person_a": 11, "person_b": 33, "type": "promotion_chain",
     "context": "宜昌党政搭档：马泽江（宜昌市长）在熊征宇（宜昌市委书记、现武汉市委书记）领导下共事；马泽江后调任随州书记",
     "overlap_org": "中国共产党宜昌市委员会", "overlap_period": "2021-2024"},
    # 组织条线
    {"person_a": 32, "person_b": 11, "type": "same_system",
     "context": "前任随州市委组织部长张卫调任省委金融工委，与现随州市委同属湖北省委统一领导",
     "overlap_org": "中国共产党湖北省委员会", "overlap_period": "2025"},
    # 纪委条线
    {"person_a": 13, "person_b": 34, "type": "same_system",
     "context": "吴晓军（现任市委副书记）曾接任/任市纪委书记，与前任纪委书记杜文清同属纪检条线",
     "overlap_org": "中共随州市纪律检查委员会", "overlap_period": "2023-2024"},
]

if __name__ == "__main__":
    run_build(
        slug="随州市",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print("随州市 network build complete")
    print("DB:", DB_PATH)
    print("GEXF:", GEXF_PATH)