#!/usr/bin/env python3
"""枣阳市（襄阳市，湖北省）领导班子工作关系网络数据生成脚本。

Targets: 市委书记 & 市长
  - 市委书记：杨晶（1981-12，汉族，大学学历/学士学位；2024-05 由湖北省发改委副主任调任襄阳市委常委、枣阳市委书记）
  - 市委副书记、市长：孔令波（1981-09，汉族，湖北樊城人，武汉大学物理化学专业理学博士；2021-08 代理→2021-11 转正市长）
  - 市委副书记：张少卿；市人大常委会主任：谢正旺；市政协主席：孙襄林
  - 前任市委书记：孟艳清（2024 上半年卸任，相关去向待核实）

Generated: 2026-08-06
Task: hubei_枣阳市
Sources:
  - 百度百科「枣阳市」政治栏目（领导班子，截至 2024-08）
  - 百度百科人物词条：杨晶 / 孔令波 / 孟艳清
  - 鲁网「杨晶任襄阳市委常委、枣阳市委书记」2024-06-07
  - 凤凰网湖北「湖北省发改委副主任杨晶调任枣阳市委书记」2024-05-31
  - 云上枣阳「关于孔令波同志为枣阳市人民政府副市长、代理市长的决定」2021-08-22

注：庞常委中纪委/组织/宣传/政法等分工角色的姓名映射采用百度百科政治栏目截至2024-08的名单，
     具体分管（如纪委书记、组织部长）未在公开稳定资料中逐一定位，未杜撰具体兼职。
"""

import sqlite3
import sys
from pathlib import Path

if "__file__" in globals():
    _here = Path(__file__).resolve()
    _candidate = _here.parent
    while True:
        if (_candidate / "gov_relation").is_dir():
            break
        _parent = _candidate.parent
        if _parent == _candidate:
            _candidate = Path.cwd()
            break
        _candidate = _parent
else:
    _candidate = Path.cwd()
sys.path.insert(0, str(_candidate))

from gov_relation.runner import run_build  # noqa: E402
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR  # noqa: E402

SLUG = "枣阳市"

if "__file__" in globals():
    _this = Path(__file__).resolve()
    _in_staging = ("data" in _this.parts) and ("tmp" in _this.parts)
else:
    _in_staging = False
# 暂存运行（data/tmp/<task>/）→ 产物写到该暂存目录；canonical 运行 → 写到 data/database|graph|persons
if _in_staging:
    OUT_DIR = Path(__file__).resolve().parent
    PERSONS_OUT = OUT_DIR
    GEXF_OUT = OUT_DIR
else:
    OUT_DIR = DATABASE_DIR
    PERSONS_OUT = PERSONS_DIR
    GEXF_OUT = GRAPH_DIR
DB_PATH = OUT_DIR / f"{SLUG}_network.db"
GEXF_PATH = GEXF_OUT / f"{SLUG}_network.gexf"

# Person IDs:
#   1 杨晶（书记） 2 孔令波（市长） 3 张少卿（副书记） 4 谢正旺（人大主任） 5 孙襄林（政协主席）
#   6 乔军强（市委常委、副市长） 7 邢红丽（市委常委、副市长）
#   8 杨朝晖（常委） 9 康丹（常委） 10 望少辉（常委） 11 张文广（常委） 12 曾刚（常委）
#   13 孟艳清（前任书记）
#   （另有副市长：廖新安、张小顺、聂荣毅、王金枝、马磊）

persons = [
    {
        "id": 1, "name": "杨晶", "gender": "男", "ethnicity": "汉族",
        "birth": "1981-12", "birthplace": "", "native_place": "",
        "education": "大学学历、学士学位", "party_join": "", "work_start": "",
        "current_post": "襄阳市委常委、枣阳市委书记、枣阳市委党校第一校长、枣阳市人武部党委第一书记",
        "current_org": "中共枣阳市委员会", "source": "百度百科：杨晶（湖北省襄阳市委常委、枣阳市委书记）",
    },
    {
        "id": 2, "name": "孔令波", "gender": "男", "ethnicity": "汉族",
        "birth": "1981-09", "birthplace": "湖北省襄阳市樊城区", "native_place": "湖北省襄阳市樊城区",
        "education": "理学博士（武汉大学物理化学专业）",
        "party_join": "2005-05", "work_start": "2008-07",
        "current_post": "枣阳市委副书记、市人民政府市长、枣阳经济开发区党工委书记",
        "current_org": "枣阳市人民政府", "source": "https://baike.baidu.com/item/孔令波",
    },
    {
        "id": 3, "name": "张少卿", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "native_place": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "枣阳市委副书记", "current_org": "中共枣阳市委员会",
        "source": "https://baike.baidu.com/item/枣阳市（政治）",
    },
    {
        "id": 4, "name": "谢正旺", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "native_place": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "枣阳市人大常委会主任", "current_org": "枣阳市人民代表大会常务委员会",
        "source": "https://baike.baidu.com/item/枣阳市（截至2024-08）",
    },
    {
        "id": 5, "name": "孙襄林", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "native_place": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "枣阳市政协主席", "current_org": "中国人民政治协商会议枣阳市委员会",
        "source": "https://baike.baidu.com/item/枣阳市（截至2024-08）",
    },
    {
        "id": 6, "name": "邢红丽", "gender": "女", "ethnicity": "",
        "birth": "", "birthplace": "", "native_place": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "枣阳市委常委、副市长", "current_org": "枣阳市人民政府",
        "source": "https://baike.baidu.com/item/枣阳市（截至2024-08）",
    },
    {
        "id": 7, "name": "乔军强", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "native_place": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "枣阳市委常委、副市长", "current_org": "枣阳市人民政府",
        "source": "https://baike.baidu.com/item/枣阳市",
    },
    {
        "id": 8, "name": "杨朝晖", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "native_place": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "枣阳市委常委", "current_org": "中共枣阳市委员会",
        "source": "https://baike.baidu.com/item/枣阳市",
    },
    {
        "id": 9, "name": "康丹", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "native_place": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "枣阳市委常委", "current_org": "中共枣阳市委员会",
        "source": "https://baike.baidu.com/item/枣阳市",
    },
    {
        "id": 10, "name": "望少辉", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "native_place": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "枣阳市委常委", "current_org": "中共枣阳市委员会",
        "source": "https://baike.baidu.com/item/枣阳市",
    },
    {
        "id": 11, "name": "张文广", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "native_place": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "枣阳市委常委", "current_org": "中共枣阳市委员会",
        "source": "https://baike.baidu.com/item/枣阳市",
    },
    {
        "id": 12, "name": "曾刚", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "", "native_place": "", "education": "",
        "party_join": "", "work_start": "",
        "current_post": "枣阳市委常委", "current_org": "中共枣阳市委员会",
        "source": "https://baike.baidu.com/item/枣阳市",
    },
    {
        "id": 13, "name": "孟艳清", "gender": "男", "ethnicity": "汉族",
        "birth": "1973-09", "birthplace": "湖北省襄阳市襄州区", "native_place": "湖北省襄阳市襄州区",
        "education": "湖北省委党校（党校）", "party_join": "1994-05", "work_start": "1992-10",
        "current_post": "（已卸任枣阳市委书记，去向待核实）", "current_org": "（离任）",
        "source": "https://baike.baidu.com/item/孟艳清",
    },
]

organizations = [
    {"id": 1, "name": "中共枣阳市委", "type": "党委", "level": "正县级", "parent": "中共襄阳市委", "location": "湖北省襄阳市枣阳市"},
    {"id": 2, "name": "枣阳市人民政府", "type": "政府", "level": "正县级", "parent": "襄阳市人民政府", "location": "湖北省襄阳市枣阳市"},
    {"id": 3, "name": "中共枣阳市纪律检查委员会", "type": "党委", "level": "正科级（县级）", "parent": "", "location": "湖北省襄阳市枣阳市"},
    {"id": 4, "name": "中共枣阳市委组织部", "type": "党委", "level": "正科级", "parent": "中共枣阳市委", "location": "湖北省襄阳市枣阳市"},
    {"id": 5, "name": "中共枣阳市委宣传部", "type": "党委", "level": "正科级", "parent": "中共枣阳市委", "location": "湖北省襄阳市枣阳市"},
    {"id": 6, "name": "中共枣阳市委政法委", "type": "党委", "level": "正科级", "parent": "中共枣阳市委", "location": "湖北省襄阳市枣阳市"},
    {"id": 7, "name": "枣阳市人民代表大会常务委员会", "type": "人大", "level": "正县级", "parent": "", "location": "湖北省襄阳市枣阳市"},
    {"id": 8, "name": "枣阳市政协委员会", "type": "政协", "level": "正县级", "parent": "", "location": "湖北省襄阳市枣阳市"},
    {"id": 9, "name": "中共襄阳市委", "type": "党委", "level": "地厅级", "parent": "中共湖北省委", "location": "湖北省襄阳市"},
    {"id": 10, "name": "襄阳市人民政府", "type": "政府", "level": "地厅级", "parent": "湖北省人民政府", "location": "湖北省襄阳市"},
    {"id": 11, "name": "襄阳市高新区管委会", "type": "开发区", "level": "副厅级", "parent": "襄阳市人民政府", "location": "湖北省襄阳市"},
    {"id": 12, "name": "保康县人民政府", "type": "政府", "level": "县处级", "parent": "襄阳市人民政府", "location": "湖北省襄阳市保康县"},
    {"id": 13, "name": "谷城县（石台镇）", "type": "乡镇", "level": "乡镇级", "parent": "谷城县", "location": "湖北省襄阳市谷城县"},
    {"id": 14, "name": "襄阳市住房保障和房屋管理局", "type": "政府", "level": "县处级", "parent": "襄阳市人民政府", "location": "湖北省襄阳市"},
    {"id": 15, "name": "湖北省发展和改革委员会", "type": "政府", "level": "厅级", "parent": "湖北省人民政府", "location": "湖北省武汉市"},
    {"id": 16, "name": "枣阳经济开发区", "type": "开发区", "level": "县处级", "parent": "枣阳市人民政府", "location": "湖北省襄阳市枣阳市"},
]

positions = [
    # 杨晶 (id=1)
    {"person_id": 1, "org_id": 9, "title": "襄阳市委常委", "start_date": "2024-05", "end_date": "present", "rank": "副厅级", "note": "2024年5月同时任枣阳市委书记"},
    {"person_id": 1, "org_id": 1, "title": "枣阳市委书记、市委党校第一校长、市人武部党委第一书记", "start_date": "2024-05", "end_date": "present", "rank": "县处级正职", "note": "2024年5月28日看望慰问老干部，正式履职"},
    {"person_id": 1, "org_id": 15, "title": "湖北省发改委副主任、党组成员", "start_date": "2023", "end_date": "2024-05", "rank": "厅级", "note": "此前任湖北省发改委固定资产投资处处长，长期在省直机关工作20余年"},
    # 孔令波 (id=2)
    {"person_id": 2, "org_id": 2, "title": "枣阳市市长", "start_date": "2021-11", "end_date": "present", "rank": "县处级正职", "note": "2021年11月正式当选市长"},
    {"person_id": 2, "org_id": 2, "title": "枣阳市人民政府副市长、代理市长", "start_date": "2021-08", "end_date": "2021-11", "rank": "县处级正职", "note": "2021年8月20日市人大常委会任命为代理市长"},
    {"person_id": 2, "org_id": 1, "title": "枣阳市委副书记", "start_date": "2021-08", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 2, "org_id": 16, "title": "枣阳经济开发区党工委书记", "start_date": "2021-08", "end_date": "present", "rank": "县处级", "note": "兼任"},
    {"person_id": 2, "org_id": 11, "title": "襄阳市高新区党工委委员", "start_date": "2019", "end_date": "2021-08", "rank": "县处级", "note": "晋升节点"},
    {"person_id": 2, "org_id": 14, "title": "襄阳市住房保障和房屋管理局副局长", "start_date": "2017", "end_date": "2019", "rank": "县处级副职", "note": ""},
    {"person_id": 2, "org_id": 12, "title": "保康县人民政府副县长", "start_date": "2015", "end_date": "2017", "rank": "县处级副职", "note": ""},
    {"person_id": 2, "org_id": 13, "title": "谷城县石台镇工作（基层）", "start_date": "2008-07", "end_date": "2015", "rank": "乡镇级", "note": "2008年7月参加工作，从谷城县石台镇基层做起"},
    # 张少卿 (id=3)
    {"person_id": 3, "org_id": 1, "title": "枣阳市委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 谢正旺 (id=4)
    {"person_id": 4, "org_id": 7, "title": "枣阳市人大常委会主任", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 孙襄林 (id=5)
    {"person_id": 5, "org_id": 8, "title": "枣阳市政协主席", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 邢红丽 (id=6)
    {"person_id": 6, "org_id": 2, "title": "枣阳市委常委、副市长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 乔军强 (id=7)
    {"person_id": 7, "org_id": 2, "title": "枣阳市委常委、副市长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 常委（杨朝晖 8 / 康丹 9 / 望少辉 10 / 张文广 11 / 曾刚 12）
    {"person_id": 8, "org_id": 1, "title": "枣阳市委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "枣阳市委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "枣阳市委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "枣阳市委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 12, "org_id": 1, "title": "枣阳市委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 孟艳清 (id=13)
    {"person_id": 13, "org_id": 1, "title": "枣阳市委书记", "start_date": "2021", "end_date": "2024-05", "rank": "县处级正职", "note": "先任枣阳市委书记后任襄阳市委常委（兼任）直至离任"},
    {"person_id": 13, "org_id": 9, "title": "襄阳市委常委", "start_date": "2021", "end_date": "2024-05", "rank": "副厅级", "note": ""},
]

relationships = [
    # 核心搭班子（现任）
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "市委书记与市长搭班子（现任）", "overlap_org": "枣阳市", "overlap_period": "2024-05至今"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "市委书记与副书记搭班子", "overlap_org": "枣阳市委", "overlap_period": ""},
    # 前任市委书记与现任市长
    {"person_a": 13, "person_b": 2, "type": "predecessor_successor", "context": "前任市委书记与现任市长搭班子（2021-2024）", "overlap_org": "枣阳市", "overlap_period": "2021-2024"},
    # 市委书记接任
    {"person_a": 1, "person_b": 13, "type": "predecessor_successor", "context": "杨晶接任孟艳清的枣阳市委书记（交接）", "overlap_org": "枣阳市", "overlap_period": "2024-05"},
    # 政府班子内部
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "市长与常委/副市长搭班子", "overlap_org": "枣阳市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "市长与常委/副市长搭班子", "overlap_org": "枣阳市人民政府", "overlap_period": ""},
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
    print(f"DB:  {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")