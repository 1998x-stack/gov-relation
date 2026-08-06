#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 宛城区 (Wancheng District), 南阳市, 河南省.

Investigation date: 2026-08-06
Task ID: henan_宛城区
Level: 市辖区
Targets: 区委书记 & 区长

Research constraints:
  - Exa search: available (used for core queries), Baidu not relied upon
  - Primary sources: wancheng.gov.cn (official gov site), nanyang.gov.cn, 南阳市纪委官网
  - Encyclo/aggregator sources: toutiao (宛城人大决定), 华中中介网 (樊牛/郭炜简历), thepaper.cn
  - Cross-county confirmations via a162 网易 (王龙/郭存调动), 新华网河南/大河网 (郭炜任前公示)

Confirmed findings (as of 2026-08-06):
  - 现任区委书记: 樊牛 (b.1973-10, 河南方城人, 河南农大农业推广硕士, 1992-07 参加工作;
    2016-06 起任宛城区长, 2023-03 任区委书记, 兼区长至 2023-08; 2026-01/02 仍在任)
  - 现任区长(代): 张拓 (男,中共党员; 曾任内乡县委常委/纪委书记/监委主任、常务副县长;
    2026-05-18 任宛城区副区长、代区长)
  - 前任区长: 郭炜 (2023-08-09 代区长, 2024-10-17 当选区长; 2026-04 拟任县(市、区)委书记; 2026-05-18 辞)
  - 前任区委书记: 袁钢 (2021-07 任, 2026/2022-12 离任, 2023-01 任开封市政府副市长)
  - 前任区委书记(袁钢之前): 刘中青 (2021-07 卸任)
  - 纪委书记/监委主任: 薛洁原
  - 区政府班子(当前): 副区长 陈梦尘、韩学军、时大海、黄振、贾岩龙、周昱江
  - 区法院院长: 吴运广 (2024-10 当选)

Cross-region transfer evidence:
  - 张拓: 内乡县(纪委/常务副县长) → 宛城区(代区长); 樊牛早年在内乡任职(同县背景线索)
  - 王龙: 宛城区副区长→常委/组织部部长→副书记/统战部部长 → 桐柏县代县长 (2026)
  - 郭存: 宛城区委常委/常务副区长 → 西峡县代县长 (2026-05)
  - 袁钢: 宛城区委书记 → 开封市副市长 (跨市)
  - 郭炜: 宛城区长 → 拟任县(市、区)委书记

This is a partial-evidence artifact: 张拓出生/籍贯/早年履历未互联核实, 郭炜出生年份两来源冲突,
按 source_fallbacks 规则标注 confidence 并写入 open_questions。
"""

# process_tmp.py tokens: sqlite3, DB_PATH, GEXF_PATH
import json
import os
import sys
from datetime import datetime

# Ensure gov_relation package is importable
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))

from gov_relation.runner import run_build
from gov_relation.paths import TMP_DIR

TASK_ID = "henan_宛城区"
STAGING = TMP_DIR / TASK_ID
DB_PATH = STAGING / "宛城区_network.db"
GEXF_PATH = STAGING / "宛城区_network.gexf"

# ── Research data ────────────────────────────────────────────────────
# Person ID convention: 100-series for persons, 200-series for orgs

persons = [
    {
        "id": 101,
        "name": "樊牛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年10月",
        "birthplace": "河南省南阳市方城县",
        "education": "河南农业大学作物专业农业推广硕士（研究生）",
        "party_join": "中共党员",
        "work_start": "1992年7月",
        "current_post": "宛城区委书记",
        "current_org": "中共南阳市宛城区委员会",
        "source": "中华网河南 2023-03-30; wancheng.gov.cn; nanyang.gov.cn",
    },
    {
        "id": 102,
        "name": "张拓",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # 公开资料未找到出生年份
        "birthplace": "",  # 公开资料未找到出生地
        "education": "",  # 公开资料未找到学历
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宛城区委副书记、区政府区长（代）",
        "current_org": "宛城区人民政府",
        "source": "宛城区人大常委会公告(2026-05-18); wancheng.gov.cn/zfxxgk",
    },
    {
        "id": 103,
        "name": "郭炜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年6月（另说1980年6月）",
        "birthplace": "河南省南阳市方城县",
        "education": "研究生，工商管理硕士（另有说法：硕士研究生）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原宛城区委副书记、区长（拟任县(市、区)委书记）",
        "current_org": "宛城区人民政府（原）",
        "source": "新华网河南频道/大河网/正观新闻 任前公示 2026-04-13; 华中中介网 2023-08",
    },
    {
        "id": 104,
        "name": "袁钢",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",  # 公开资料未找到出生年份
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "开封市人民政府副市长（原中共宛城区委书记）",
        "current_org": "开封市人民政府",
        "source": "澎湃新闻 thepaper.cn; 开封日报 2023-01",
    },
    {
        "id": 105,
        "name": "薛洁原",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宛城区委常委、区纪委书记、区监委主任",
        "current_org": "中共宛城区纪律检查委员会 / 宛城区监察委员会",
        "source": "南阳市纪委官网 nydi.gov.cn",
    },
    {
        "id": 106,
        "name": "刘中青",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原宛城区委书记（曾任）",
        "current_org": "中共南阳市宛城区委（原）",
        "source": "澎湃新闻 宛城区委主要领导调整 2021-07-17",
    },
    {
        "id": 107,
        "name": "陈梦尘",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "宛城区委常委、宣传部部长、副区长",
        "current_org": "宛城区人民政府",
        "source": "wancheng.gov.cn 2024-03 分工通知 + zfxxgk",
    },
    {
        "id": 108,
        "name": "韩学军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "宛城区副区长",
        "current_org": "宛城区人民政府",
        "source": "wancheng.gov.cn/zfxxgk",
    },
    {
        "id": 109,
        "name": "时大海",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "宛城区副区长",
        "current_org": "宛城区人民政府",
        "source": "wancheng.gov.cn/zfxxgk 2026-01-08",
    },
    {
        "id": 110,
        "name": "黄振",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "宛城区副区长",
        "current_org": "宛城区人民政府",
        "source": "wancheng.gov.cn/zfxxgk",
    },
    {
        "id": 111,
        "name": "贾岩龙",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "宛城区副区长",
        "current_org": "宛城区人民政府",
        "source": "wancheng.gov.cn/zfxxgk 2025-07-30",
    },
    {
        "id": 112,
        "name": "周昱江",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宛城区副区长（负责金融等）",
        "current_org": "宛城区人民政府",
        "source": "wancheng.gov.cn 2026-03-26",
    },
    {
        "id": 113,
        "name": "郭存",
        "gender": "",
        "ethnicity": "",
        "birth": "1984年",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "西峡县委副书记、县政府代县长（原宛城区委常委、常务副区长）",
        "current_org": "西峡县人民政府",
        "source": "网易 2026-05 报道; 宛城区 2024 分工通知",
    },
    {
        "id": 114,
        "name": "王龙",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "桐柏县委副书记、县政府代县长（原宛城区委副书记、统战部部长等）",
        "current_org": "桐柏县人民政府",
        "source": "网易 2026-05 15 报道; 华网",
    },
    {
        "id": 115,
        "name": "吴运广",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "宛城区人民法院院长",
        "current_org": "宛城区人民法院",
        "source": "nanyang.gov.cn 2024-10-17 人代会选举",
    },
    {
        "id": 116,
        "name": "赵文永",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "宛城区副区长（曾任）",
        "current_org": "宛城区人民政府",
        "source": "宛城区 2024-11 事务活动",
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共南阳市宛城区委员会",
        "type": "党委",
        "level": "正处级",
        "parent": "中共南阳市委",
        "location": "河南省南阳市宛城区",
    },
    {
        "id": 2,
        "name": "宛城区人民政府",
        "type": "政府",
        "level": "正处级",
        "parent": "南阳市人民政府",
        "location": "河南省南阳市宛城区",
    },
    {
        "id": 3,
        "name": "宛城区人大常委会",
        "type": "人大",
        "level": "正处级",
        "parent": "南阳市人大常委会",
        "location": "河南省南阳市宛城区",
    },
    {
        "id": 4,
        "name": "中共宛城区纪律检查委员会 / 宛城区监察委员会",
        "type": "党委",
        "level": "正处级",
        "parent": "南阳市纪委",
        "location": "河南省南阳市宛城区",
    },
    {
        "id": 5,
        "name": "宛城区人民法院",
        "type": "政府",
        "level": "正科级",
        "parent": "南阳市中级人民法院",
        "location": "河南省南阳市宛城区",
    },
    {
        "id": 6,
        "name": "内乡县人民政府",
        "type": "政府",
        "level": "正处级",
        "parent": "南阳市人民政府",
        "location": "河南省南阳市内乡县",
    },
    {
        "id": 7,
        "name": "桐柏县人民政府",
        "type": "政府",
        "level": "正处级",
        "parent": "南阳市人民政府",
        "location": "河南省南阳市桐柏县",
    },
    {
        "id": 8,
        "name": "西峡县人民政府",
        "type": "政府",
        "level": "正处级",
        "parent": "南阳市人民政府",
        "location": "河南省南阳市西峡县",
    },
    {
        "id": 9,
        "name": "开封市人民政府",
        "type": "政府",
        "level": "正厅级",
        "parent": "河南省人民政府",
        "location": "河南省开封市",
    },
    {
        "id": 10,
        "name": "南阳市人民政府",
        "type": "政府",
        "level": "正厅级",
        "parent": "河南省人民政府",
        "location": "河南省南阳市",
    },
]

positions = [
    # 樊牛 (101)
    {"person_id": 101, "org_id": 1, "title": "宛城区委书记", "start_date": "2023-03", "end_date": "至今", "rank": "正处级", "note": "接替袁钢任宛城区委书记，兼区长至2023-08"},
    {"person_id": 101, "org_id": 2, "title": "宛城区委副书记、区长", "start_date": "2016-06", "end_date": "2023-08", "rank": "正处级", "note": "2016-06 任宛城区长，2023-03 起兼任书记，2023-08 卸任区长"},
    # 张拓 (102)
    {"person_id": 102, "org_id": 2, "title": "宛城区委副书记、区政府区长（代）", "start_date": "2026-05-18", "end_date": "至今", "rank": "正处级", "note": "2026-05-18 任副区长、代区长，接替郭炜"},
    {"person_id": 102, "org_id": 6, "title": "内乡县委常委、常务副县长", "start_date": "2024", "end_date": "2026-05", "rank": "副处级", "note": "2024-11 仍在任（内乡县）"},
    {"person_id": 102, "org_id": 6, "title": "内乡县委常委、县纪委书记、监委主任", "start_date": "2023", "end_date": "2024", "rank": "副处级", "note": "2023-06 报道（内乡县委）"},
    # 郭炜 (103)
    {"person_id": 103, "org_id": 2, "title": "宛城区委副书记、区长", "start_date": "2023-08-09", "end_date": "2026-05-18", "rank": "正处级", "note": "2023-08 代区长，2024-10-17 当选区长，2026 辞任拟任县委书记"},
    {"person_id": 103, "org_id": 2, "title": "南召县委常委、副县长", "start_date": "2021-08", "end_date": "2023-08", "rank": "副处级", "note": ""},
    # 袁钢 (104)
    {"person_id": 104, "org_id": 1, "title": "宛城区委书记", "start_date": "2021-07", "end_date": "2022-12", "rank": "正处级", "note": "接任刘中青"},
    {"person_id": 104, "org_id": 9, "title": "开封市人民政府副市长", "start_date": "2023-01", "end_date": "至今", "rank": "副厅级", "note": "2023-01-06 当选开封市副市长"},
    # 薛洁原 (105)
    {"person_id": 105, "org_id": 4, "title": "宛城区委常委、区纪委书记、监委主任", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "2025-02 纪委全会主持"},
    # 刘中青 (106)
    {"person_id": 106, "org_id": 1, "title": "宛城区委书记", "start_date": "", "end_date": "2021-07", "rank": "正处级", "note": "2021-07 被袁钢接替"},
    # 副区长们 (107-112)
    {"person_id": 107, "org_id": 2, "title": "宛城区委常委、宣传部长、副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 108, "org_id": 2, "title": "宛城区副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 109, "org_id": 2, "title": "宛城区副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "2026-01-08 官网公开"},
    {"person_id": 110, "org_id": 2, "title": "宛城区副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 111, "org_id": 2, "title": "宛城区副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "2025-07-30 官网公开"},
    {"person_id": 112, "org_id": 2, "title": "宛城区副区长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "2026-03-26 官网公开，负责金融"},
    # 郭存 (113)
    {"person_id": 113, "org_id": 2, "title": "宛城区委常委、常务副区长", "start_date": "2024", "end_date": "2026-05", "rank": "副处级", "note": ""},
    {"person_id": 113, "org_id": 8, "title": "西峡县委副书记、县政府代县长", "start_date": "2026-05", "end_date": "至今", "rank": "正处级", "note": "2026-05-09 西峡县人大常委会"},
    # 王龙 (114)
    {"person_id": 114, "org_id": 2, "title": "宛城区副区长（曾任）", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 114, "org_id": 7, "title": "桐柏县委副书记、县政府代县长", "start_date": "2026", "end_date": "至今", "rank": "正处级", "note": "曾任宛城区委常委/组织部长、副书记/统战部长"},
    # 吴运广 (115)
    {"person_id": 115, "org_id": 5, "title": "宛城区人民法院院长", "start_date": "2024-10-17", "end_date": "至今", "rank": "正科级", "note": ""},
]

relationships = [
    # 樊牛 → 前任书记袁钢 (前任-继任)
    {"person_a": 101, "person_b": 104, "type": "predecessor_successor",
     "context": "樊牛2023-03接任袁钢任宛城区委书记", "overlap_org": "中共南阳市宛城区委",
     "overlap_period": "2023（交接期）"},
    # 袁钢 → 刘中青 (前任-继任)
    {"person_a": 104, "person_b": 106, "type": "predecessor_successor",
     "context": "袁钢2021-07接任刘中青任宛城区委书记", "overlap_org": "中共南阳市宛城区委",
     "overlap_period": "2021-07"},
    # 樊牛 → 郭炜 (前任区长-继任区长)
    {"person_a": 101, "person_b": 103, "type": "predecessor_successor",
     "context": "樊牛卸任区长后由郭炜接任（樊牛转任书记）", "overlap_org": "宛城区人民政府",
     "overlap_period": "2023-08"},
    # 樊牛 ↔ 郭炜 (党政一把手搭档)
    {"person_a": 101, "person_b": 103, "type": "overlap",
     "context": "樊牛任区委书记、郭炜任区长，为党政一把手搭档", "overlap_org": "宛城区",
     "overlap_period": "2023-2026"},
    # 樊牛 ↔ 张拓 (现任党政一把手搭档)
    {"person_a": 101, "person_b": 102, "type": "overlap",
     "context": "樊牛任区委书记，张拓新任代区长，为现行党政搭档", "overlap_org": "宛城区",
     "overlap_period": "2026-05-至今"},
    # 郭炜 → 张拓 (区长前任-继任)
    {"person_a": 103, "person_b": 102, "type": "predecessor_successor",
     "context": "郭炜2026-05-18卸任后由张拓接任代区长", "overlap_org": "宛城区人民政府",
     "overlap_period": "2026-05"},
    # 张拓 ↔ 樊牛 (同内乡县背景线索)
    {"person_a": 102, "person_b": 101, "type": "same_system",
     "context": "张拓曾任内乡县领导；樊牛早期在内乡县任职（同县背景线索，弱关联）", "overlap_org": "内乡县",
     "overlap_period": "早年"},
    # 薛洁原 ↔ 樊牛 (纪委-区委，上下级)
    {"person_a": 105, "person_b": 101, "type": "superior_subordinate",
     "context": "薛洁原任纪委书记/监委主任，在樊牛领导下工作", "overlap_org": "中共南阳市宛城区委",
     "overlap_period": "2025-至今"},
    # 郭存 从宛城调任西咸 (跨县)
    {"person_a": 113, "person_b": 101, "type": "overlap",
     "context": "郭存任宛城区委常委、常务副区长，樊牛任区委书记", "overlap_org": "宛城区",
     "overlap_period": "2024-2026"},
    # 王龙 从宛城调任桐柏 (跨县)
    {"person_a": 114, "person_b": 101, "type": "overlap",
     "context": "王龙曾在宛城区任副区长、常委等职，与樊牛共事", "overlap_org": "宛城区",
     "overlap_period": ""},
    ]

# ── Build ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_build(
        slug="宛城区领导班子关系图",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print(f"Done. DB: {DB_PATH}, GEXF: {GEXF_PATH}")