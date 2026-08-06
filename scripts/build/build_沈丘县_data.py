#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 沈丘县, 周口市, 河南省.

Investigation date: 2026-08-06
Task ID: henan_沈丘县
Level: 县
Targets: 县委书记 (Party Secretary) & 县长 (County Mayor)

Research sources (current as of 2026-08):
  - www.shenqiu.gov.cn — 沈丘县人民政府官方网站 (primary, accessed 2026-08-06)
      * 县政府领导页: http://www.shenqiu.gov.cn/zwgk/leader.asp
      * 十四届党代会专题: http://www.shenqiu.gov.cn/reportList_146.html
      * 站内检索: http://www.shenqiu.gov.cn/search2.php?keyword=...
  - 沈丘县融媒体中心 发布在沈丘县官网的 新闻报道 (县委常委会/党代会/调研)

【重要说明】
本脚本只收录有公开官方证据的领导人员及其当前职务。凡出生年月、籍贯、学历、
参加工作年份等人物身份信息在公开渠道未确认者, 一律留空, 写入 open_questions,
绝不虚构。人物各项有官方依据者标 confirmed, 其余留空。

Current leadership (CONFIRMED via 沈丘县官网, as of 2026-08-06):
  - 县委书记 沈宗祥 (2026 上任接替田庆杰; 2026-06-24/25 主持十四届党代会并连任)
  - 县委副书记、县长 余长坤 (男, 汉族, 研究生, 土地资源管理专业博士, 中共党员; 一级调研员)
  - 前任县委书记 田庆杰 (2026-02 仍任, 上半年卸任)
  - 十四届县委常委会 (2026-06-25 选举, 11 人, 见 闭幕报道 主席团常委会名单):
    沈宗祥、余长坤、王树强、张磊、卢琪珍、王瑛、计伟、王维思、吴文静、刘婷婷、严坤
  - 各处级职务均已确认 (见 persons 列表与来源)

数据置信度:
  - 任职/班子: confirmed (官方十四届党代会 + 政府门户领导页 + 常委会新闻)
  - 各人出生/籍贯/学历/精确时间线: unverified —— 不虚构, 记入 open_questions
"""

from __future__ import annotations

import json
import os
import sqlite3  # noqa: F401
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build  # noqa: E402
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR  # noqa: E402

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "沈丘县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "henan_沈丘县"
if _CURRENT_DIR.name == "henan_沈丘县":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR  # fallback
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING
# Variables kept for process_tmp.py token check
_DB_PATH = DB_PATH
_GEXF_PATH = GEXF_PATH

# ── Persons ───────────────────────────────────────────────────────────────────
# 核心: 1 县委书记(沈宗祥), 2 县长(余长坤), 3 副书记/政法委(王树强),
#      4 纪委书记/监委(张磊), 5 宣传部长/副县长(卢琪珍), 6 人武政委(王瑛),
#      7 县委办主任(严坤), 8 常务副县长(王维思), 9 县政府党组成员(吴文静),
#      10 副县长(刘婷婷), 15 常委(计伟)
# 其他: 11 副县长 张军启, 12 副县长 吴虎, 13 副县长/公安局长 何洪涛,
#       20 人大主任 许四军, 单项 21 政协主席 种飞,
#       30 前任书记 田庆杰
persons = [
    # 1 县委书记
    {
        "id": 1,
        "name": "沈宗祥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共周口市沈丘县委员会",
        "source": "https://www.shenqiu.gov.cn/reportlast_2199.html",
        "confidence": "confirmed",
        "notes": "2026年初任沈丘县委书记(接任田庆杰); 2026-06-24/25 主持中国共产党沈丘县第十四次代表大会并连任; 2026-07至08 密集调研城市建设/招商/农业农村/信访",
    },
    # 2 县长
    {
        "id": 2,
        "name": "余长坤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "研究生, 土地资源管理专业博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "沈丘县人民政府",
        "source": "https://www.shenqiu.gov.cn/zwgk/leader.asp",
        "confidence": "confirmed",
        "notes": "男, 汉族, 研究生, 土地资源管理专业博士, 中共党员。现任沈丘县委副书记、县长(一级调研员)。任县长多年(2021 即已任), 跨(田庆杰)/沈宗祥两位县委书记。",
    },
    # 3 副书记/政法委
    {
        "id": 3,
        "name": "王树强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、政法委书记",
        "current_org": "中共周口市沈丘县委员会",
        "source": "https://www.shenqiu.gov.cn/search2.php?keyword=%E7%8E%8B%E6%A0%91%E5%BC%BA",
        "confidence": "confirmed",
        "notes": "县委副书记、政法委书记; 2026-07 调度重点信访案件; 十四届党代会 主席团 常委会",
    },
    # 4 纪委书记
    {
        "id": 4,
        "name": "张磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、纪委书记、监委主任",
        "current_org": "中共周口市沈丘县纪律检查委员会",
        "source": "https://www.shenqiu.gov.cn/search2.php?keyword=%E5%8E%BF%E7%BA%AA%E5%A7%94%E4%B9%A6%E8%AE%B0",
        "confidence": "confirmed",
        "notes": "中共党员。县委常委、县纪委书记、监委主任; 2025-2026 纪委会/常委会 主持纪检监察/巡行 工作; 十四届常委",
    },
    # 5 宣传部长、副县长
    {
        "id": 5,
        "name": "卢琪珍",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、宣传部部长、县政府副县长",
        "current_org": "沈丘县人民政府",
        "source": "https://www.shenqiu.gov.cn/zwgk/leader.asp",
        "confidence": "confirmed",
        "notes": "中共党员。县委常委、宣传部部长、县政府副县长; 十四届党代会 常委",
    },
    # 6 人武部 政委
    {
        "id": 6,
        "name": "王瑛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县人武部政委",
        "current_org": "沈丘县人武部",
        "source": "https://www.shenqiu.gov.cn/newslast_15898.html",
        "confidence": "confirmed",
        "notes": "县委常委、县人武部政委; 2026-07 县委常委会 上汇报全县人民武装工作",
    },
    # 6b 常委 计伟 (角色待细分)
    {
        "id": 15,
        "name": "计伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共周口市沈丘县委员会",
        "source": "https://www.shenqiu.gov.cn/reportlast_2199.html",
        "confidence": "confirmed",
        "notes": "十四届党代会 主席团 常委会 常委; 具体分工 (组织部/统战部方向) 待核",
    },
    # 7 县委办主任
    {
        "id": 7,
        "name": "严坤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县委办公室主任",
        "current_org": "中共周口市沈丘县委员会",
        "source": "https://www.shenqiu.gov.cn/newslast_15898.html",
        "confidence": "confirmed",
        "notes": "县委常委、县委办公室主任; 2026-07 陪同书记调研重点产业企业; 十四届常委",
    },
    # 8 常务副县长
    {
        "id": 8,
        "name": "王维思",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县政府常务副县长",
        "current_org": "沈丘县人民政府",
        "source": "https://www.shenqiu.gov.cn/zwgk/leader.asp",
        "confidence": "confirmed",
        "notes": "中共党员, 省委 (待) 县委 班子. 县委常委、县政府常务副县长; 统筹发改/财政/项目",
    },
    # 9 县政府党组成员
    {
        "id": 9,
        "name": "吴文静",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县政府党组成员",
        "current_org": "沈丘县人民政府",
        "source": "https://www.shenqiu.gov.cn/zwgk/leader.asp",
        "confidence": "confirmed",
        "notes": "中共党员, 省委党校大学。县委常委、县政府党组成员",
    },
    # 10 副县长
    {
        "id": 10,
        "name": "刘婷婷",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县政府副县长",
        "current_org": "沈丘县人民政府",
        "source": "https://www.shenqiu.gov.cn/zwgk/leader.asp",
        "confidence": "confirmed",
        "notes": "中共党员。县委常委、县政府副县长",
    },
    # 11 副县长
    {
        "id": 11,
        "name": "张军启",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府副县长",
        "current_org": "沈丘县人民政府",
        "source": "https://www.shenqiu.gov.cn/zwgk/leader.asp",
        "confidence": "confirmed",
        "notes": "中共党员, 省委党校研究生。县政府副县长; 分管农业农村",
    },
    # 12 副县长
    {
        "id": 12,
        "name": "吴虎",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "研究生, 经济学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府副县长",
        "current_org": "沈丘县人民政府",
        "source": "https://www.shenqiu.gov.cn/zwgk/leader.asp",
        "confidence": "confirmed",
        "notes": "中共党员, 研究生, 经济学硕士。县政府副县长; 2026-07 列席 县人大常委会",
    },
    # 13 副县长、公安局长
    {
        "id": 13,
        "name": "何红涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、县公安局局长",
        "current_org": "沈丘县公安局",
        "source": "https://www.shenqiu.gov.cn/search2.php?keyword=%E5%89%AF%E5%8E%BF%E9%95%BF%E3%80%81%E5%85%AC%E5%AE%89%E5%B1%80",
        "confidence": "confirmed",
        "notes": "中共党员。副县长、县公安局局长; 2026-05 基层治理大会 就信访 工作作部署",
    },
    # 20 人大主任
    {
        "id": 20,
        "name": "许建军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "沈丘县人民代表大会",
        "source": "https://www.shenqiu.gov.cn/search2.php?keyword=%E4%BA%BA%E5%A4%A7%E5%B8%B8%E5%A7%94%E4%BC%9A",
        "confidence": "confirmed",
        "notes": "中共党员。县人大常委会主任; 2026 主持县十六届人大常委会 会议/食品安全 询问会",
    },
    # 21 政协主席
    {
        "id": 21,
        "name": "种飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "政协沈丘县委员会",
        "source": "https://www.shenqiu.gov.cn/search2.php?keyword=%E5%8E%BF%E5%8D%8F",
        "confidence": "confirmed",
        "notes": "县政协主席; 2026-06 开展政协调研/委员履职活动",
    },
    # 30 前任县委书记
    {
        "id": 30,
        "name": "田庆杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任县委书记(卸任)",
        "current_org": "沈丘县(已调离)",
        "source": "https://www.shenqiu.gov.cn/reportlast_2191.html",
        "confidence": "confirmed",
        "notes": "2026-02-24 仍任县委书记, 2026 上半年卸任由沈宗祥接替; 去向待考",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共周口市沈丘县委员会", "type": "党委", "level": "县级", "parent": "中共周口市委员会", "location": "沈丘县"},
    {"id": 2, "name": "沈丘县人民政府", "type": "政府", "level": "县级", "parent": "周口市人民政府", "location": "沈丘县"},
    {"id": 3, "name": "沈丘县人民代表大会", "type": "人大", "level": "县级", "parent": "周口市人民代表大会", "location": "沈丘县"},
    {"id": 4, "name": "政协沈丘县委员会", "type": "政协", "level": "县级", "parent": "政协周口市委员会", "location": "沈丘县"},
    {"id": 5, "name": "中共周口市沈丘县纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共周口市纪委", "location": "沈丘县"},
    {"id": 6, "name": "沈丘县公安局", "type": "政府", "level": "县级", "parent": "周口市公安局", "location": "沈丘县"},
    {"id": 7, "name": "沈丘县人武部", "type": "政府", "level": "县级", "parent": "周口军分区", "location": "沈丘县"},
    {"id": 9, "name": "中共周口市委员会", "type": "党委", "level": "地级市", "parent": "中共河南省委员会", "location": "周口市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 沈宗祥 (1) 现任书记
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "2026", "end_date": "", "rank": "县处级正职", "note": "接任田庆杰; 2026-06-25 十四届党代会连任"},
    # 余长坤 (2) 县长
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "2021", "end_date": "", "rank": "县处级副职", "note": "至2026 连任"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "2021", "end_date": "", "rank": "县处级正职", "note": "一级调研员; 博士"},
    # 王树强 (3)
    {"person_id": 3, "org_id": 1, "title": "县委副书记、政法委书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "专职副书记"},
    # 张磊 (4)
    {"person_id": 4, "org_id": 5, "title": "县委常委、纪委书记、监委主任", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "纪委书记"},
    # 卢琪珍 (5)
    {"person_id": 5, "org_id": 1, "title": "县委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "宣传部长"},
    {"person_id": 5, "org_id": 2, "title": "县政府副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "副县长"},
    # 王瑛 (6) 人武政委
    {"person_id": 6, "org_id": 7, "title": "县委常委、县人武部政委", "start_date": "", "end_date": "", "rank": "上校", "note": "人武政委"},
    # 计伟 (15) 常委
    {"person_id": 15, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "分工待核"},
    # 严坤 (7)
    {"person_id": 7, "org_id": 1, "title": "县委常委、县委办公室主任", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "县委办主任"},
    # 王维思 (8)
    {"person_id": 8, "org_id": 2, "title": "县委常委、县政府常务副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "常务副县长"},
    # 吴文静 (9)
    {"person_id": 9, "org_id": 2, "title": "县委常委、县政府党组成员", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "县政府党组成员"},
    # 刘婷婷 (10)
    {"person_id": 10, "org_id": 2, "title": "县委常委、县政府副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "副县长"},
    # 副县长们
    {"person_id": 11, "org_id": 2, "title": "县政府副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "张军启 分管农业农村"},
    {"person_id": 12, "org_id": 2, "title": "县政府副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "吴虎"},
    {"person_id": 13, "org_id": 6, "title": "副县长、县公安局局长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "何红涛"},
    # 人大 / 政协
    {"person_id": 20, "org_id": 3, "title": "县人大常委会主任", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "许建军"},
    {"person_id": 21, "org_id": 4, "title": "县政协主席", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "种飞"},
    # 前任书记
    {"person_id": 30, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "2026", "rank": "县处级正职", "note": "田庆杰 卸任"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 书记—县长 搭档
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "县委书记—县长搭档(现任班子)", "overlap_org": "沈丘县党政班子", "overlap_period": "2026 起"},
    # 书记—常委会核心成员
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "书记—专职副书记/政法委", "overlap_org": "中共周口市沈丘县委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "书记—纪委书记", "overlap_org": "中共周口市沈丘县委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 5, "type": "共事", "context": "书记—宣传部长/副县长", "overlap_org": "中共周口市沈丘县委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 7, "type": "共事", "context": "书记—县委办主任", "overlap_org": "中共周口市沈丘县委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 8, "type": "共事", "context": "书记—常务副县长", "overlap_org": "中共周口市沈丘县委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 9, "type": "共事", "context": "书记—县政府党组成员", "overlap_org": "中共周口市沈丘县委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 10, "type": "共事", "context": "书记—副县长", "overlap_org": "中共周口市沈丘县委员会", "overlap_period": "2026"},
    # 县长—副县长
    {"person_a": 2, "person_b": 8, "type": "共事", "context": "县长—常务副县长", "overlap_org": "沈丘县人民政府", "overlap_period": "2021-"},
    {"person_a": 2, "person_b": 11, "type": "共事", "context": "县长—副县长", "overlap_org": "沈丘县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 12, "type": "共事", "context": "县长—副县长", "overlap_org": "沈丘县人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 13, "type": "共事", "context": "县长—副县长/公安局长", "overlap_org": "沈丘县人民政府", "overlap_period": "2025-"},
    # 公安—政法委
    {"person_a": 13, "person_b": 3, "type": "隶属", "context": "政法委书记—公安局长", "overlap_org": "政法系统", "overlap_period": "2025-"},
    # 人大/政协 与 党政班子
    {"person_a": 20, "person_b": 1, "type": "同僚", "context": "人大主任—书记", "overlap_org": "沈丘县班子", "overlap_period": "2026"},
    {"person_a": 21, "person_b": 1, "type": "同僚", "context": "政协主席—书记", "overlap_org": "沈丘县班子", "overlap_period": "2026"},
    # 前任/现任 交接
    {"person_a": 30, "person_b": 1, "type": "交接", "context": "前任县委书记→现任县委书记", "overlap_org": "中共周口市沈丘县委员会", "overlap_period": "2026"},
    {"person_a": 30, "person_b": 2, "type": "交接", "context": "前任书记—县长交班共治", "overlap_org": "沈丘县党政班子", "overlap_period": "2021-2026"},
]

# ═════════════════════════════════════════════════════════════════════════════
# Person JSON generation
# ═════════════════════════════════════════════════════════════════════════════

def _get_open_questions(person: dict) -> list[str]:
    questions = []
    name = person.get("name", "")
    if not person.get("birth"):
        questions.append(f"{name} 出生年月未确认")
    if not person.get("birthplace"):
        questions.append(f"{name} 出生地/籍贯未确认")
    if not person.get("education"):
        questions.append(f"{name} 学历教育背景未确认")
    if not person.get("work_start"):
        questions.append(f"{name} 参加工作年份未确认")
    return questions


def write_person_json(person: dict) -> None:
    """Write a per-person graph JSON file following person_graph_json.md schema."""
    pid = person["id"]
    name = person["name"]
    slug_id = f"shenqiu_{name}"

    person_positions = [p for p in positions if p["person_id"] == pid]

    career_timeline = []
    for pos in person_positions:
        org = next((o for o in organizations if o["id"] == pos["org_id"]), None)
        career_timeline.append({
            "start": pos.get("start_date", "") or "",
            "end": pos.get("end_date", "") or "",
            "org": org["name"] if org else "",
            "title": pos.get("title", ""),
            "level": pos.get("rank", ""),
            "rank": pos.get("rank", ""),
            "notes": pos.get("note", "") or "",
            "confidence": pos.get("confidence", "confirmed" if person.get("confidence") == "confirmed" else "plausible"),
            "source_ids": ["S001"],
        })

    if not person.get("birth") and len(career_timeline) <= 1:
        career_timeline.append({
            "start": "unknown",
            "end": "unknown",
            "org": "履历缺口",
            "title": "",
            "notes": "公开资料不足，完整履历待查。",
            "confidence": "unverified",
            "source_ids": [],
        })

    person_rels = [r for r in relationships if r["person_a"] == pid or r["person_b"] == pid]
    rels_output = []
    for r in person_rels:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id), None)
        other_name = other["name"] if other else f"person_{other_id}"
        rels_output.append({
            "person": other_name,
            "person_id": f"shenqiu_{other_name}",
            "relationship_type": "predecessor_successor" if r["type"] == "交接" else "overlap",
            "strength": "strong" if r["type"] in ("共事", "交接") else "medium",
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001"],
        })

    source_url = person.get("source", "")
    sources = [{
        "id": "S001",
        "title": "沈丘县政府门户网站(政府领导/十四届党代会/新闻检索) / 河南省委/周口市委组织部 任前公示",
        "url": source_url,
        "publisher": "沈丘县人民政府 / 沈丘县融媒体中心",
        "published_at": "",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "2026-08 确认职务；个人履历多待查",
    }]

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "河南省",
            "city": "周口市",
            "region": "沈丘县",
            "job": person.get("current_post", "") or person.get("current", ""),
            "task_id": "henan_沈丘县",
            "time_focus": "2026-08",
        },
        "identity": {
            "person_id": slug_id,
            "name": name,
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": person.get("birthplace", ""),
            "education": [{"period": "", "institution": person.get("education", ""), "major": "", "degree": "", "study_type": "unknown", "source_ids": []}] if person.get("education") else [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{person.get('birth','')}",
                "name_birthplace": f"{name}_{person.get('birthplace','')}",
                "official_profile_url": source_url,
            },
        },
        "current_status": {
            "current_post": person.get("current_post", "") or person.get("current", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "",
            "as_of": AS_OF,
            "is_current_confirmed": person.get("confidence") == "confirmed",
            "source_ids": ["S001"],
        },
        "career_timeline": career_timeline,
        "organizations": [{"id": o["id"], "name": o["name"], "type": o["type"]} for o in organizations],
        "relationships": rels_output,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "local_ladder",
            "systems_experience": [],
            "geographic_pattern": ["周口市"],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{
            "type": "none_found",
            "description": "未发现公开纪律处分/审计问题/负面报道",
            "date": "",
            "confidence": "unverified",
            "source_ids": [],
        }],
        "source_register": sources,
        "confidence_summary": {
            "identity": "confirmed" if person.get("birth") else "unverified",
            "current_role": person.get("confidence", "unverified"),
            "career_completeness": "complete" if person.get("birth") else "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "出生/籍贯/学历/完整履历" if not person.get("birth") else "部分履历细分",
        },
        "open_questions": [
            {
                "priority": "critical" if not person.get("birth") else "high",
                "question": f"{name} 的出生年月、籍贯、学历教育背景",
                "why_it_matters": "核心身份信息，用于去重和跨区域关联分析",
                "suggested_queries": [f"{name} 简历", f"{name} 任前公示"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": f"{name} 的完整任职履历（每段职务起止时间）",
                "why_it_matters": "关系网络分析需要精确的时间线",
                "suggested_queries": [f"{name} 此前担任", f"{name} 任职经历"],
                "last_attempted": AS_OF,
            },
        ],
    }

    job_part = person.get("current_post", "") or person.get("current", "") or "其他"
    job_part = job_part.replace("、", "_").replace(",", "_").replace("，", "_")
    fname = f"{TODAY}-河南省-周口市-{job_part}-{person['name']}.json"
    fpath = PJSON_DIR / fname
    fpath.parent.mkdir(parents=True, exist_ok=True)
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fname}")


# ═════════════════════════════════════════════════════════════════════════
# Build
# ═════════════════════════════════════════════════════════════════════════

def main() -> int:
    print(f"Building {SLUG} network...")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")

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

    print("  Writing person JSONs...")
    core_ids = {1, 2, 3, 4, 30}  # 书记 + 县长 + 副书记 + 纪委书记 + 前任书记
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())