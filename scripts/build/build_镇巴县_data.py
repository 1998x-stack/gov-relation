#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 镇巴县 (Zhenba County), 汉中市, 陕西省.

Investigation date: 2026-08-07
Task ID: shaanxi_镇巴县
Level: 县
Targets: 县委书记 & 县长

Research sources (primary official, accessed 2026-08-07):
  - 镇巴县人民政府官网 www.zb.gov.cn: 领导之窗 (县政府领导班子 9 名领导干部简历,
    更新 2026-03-12), 镇巴要闻, 公示公告, 会议公开.
  - 镇巴党建网 www.zbdj.net (镇巴县委组织部).
  - 镇巴发布 (新浪), 汉中日报 via 汉中市政府 www.hanzhong.gov.cn.

Confirmed leadership timeline (as of 2026-08-07):
  - 现任县委书记 徐红菊 (女) —— 自约 2026-07-28 起任书记; 2026-08-01 主持"四大班子"八一慰问。
    2026-07-28 调研稳增长/安全稳定工作 (镇巴要闻 2026-07-29).
  - 现任代县长 李波 —— 自约 2026-07/08 起代理; 2026-08-01 八一活动 "代理县长"。
    2026-08-03 调研基层治理/财政/审计/应急管理.
  - 前任书记 韩雄 —— 截至 2026-07-01 仍为县委书记 (七一走访慰问); 2026-06-30 主持县委常委会.
    2026-07 中下同后卸任, 去向待查.
  - 前任县长 程开耀 —— 2026-01-26 以县长身份主持县政府全体会议; 常务副县长武芯茹简历
    "协助程开耀同志抓好分管工作". 约2026-07 卸任, 去向待查.
  - 县人大常委会主任 魏强; 县政协主席 王孝琴 (2026-08-01 八一活动确认).
  - 县委常委会 (2025-08-25 县委十六届九次全会): 韩雄(书记)、程开耀(副书记/县长)、高栋梁(副书记)、
    武芯茹、黄伟、张学武、龙晓涛、蔡立新、周宇、王刚才、侯绪朋(常委).
  - 县政府班子 (领导之窗, 官方简历): 常务副县长 武芯茹; 副县长 周宇、王刚才、张文春、邵永宏、黄山、
    徐东(兼县公安局长)、刘伟(兼县农业农村局长)、杨永太(省级机关挂职).
  - 跨县网络线索: 现任城固县委书记 王钧平 (男,汉族,1974-10,省委党校研究生)
    曾任 镇巴县纪委书记 (城欧县调研数据源转载) -> 纪委条线自镇巴流向城欧任县委书记.

Confidence notes:
  - 党政正职 (书记徐红菊、代县长李波) 现任职务 —— confirmed (官方新闻一手, 2026-08).
  - 前任书记韩雄、前任县长程开耀 又一任 —— confirmed 现任官方新闻, 但去向后向为 unverified.
  - 县政府 9 名班子成员 简历 —— confirmed (官方领导之窗).
  - 县委常委分工 (纪委/组织/宣传/政法/统战/县委办) —— 未逐一验证, 记为 unverified.
  - 徐红菊/李波 出生、籍贯、学历、此前单位 —— 公开搜索受限 (Exa rate-limit / Baidu/DDG/Bing blocked, Jina 不可达),
    记入 open_questions / 报告缺口. 属 partial-evidence artifact.

This is a partial-evidence artifact. Current roles & roster are confirmed from official primary
sources; individual biographies of the newest leaders are preserved as gaps rather than fabricated.
"""

import sys
from datetime import datetime
from pathlib import Path

# process_tmp.py tokens: sqlite3, DB_PATH, GEXF_PATH
import sqlite3  # noqa: F401

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent


def _find_repo_root(start: Path) -> Path:
    for p in [start] + list(start.parents):
        if (p / "gov_relation").is_dir() and (p / "data").is_dir():
            return p
    return start


BASE = _find_repo_root(STAGING_DIR)
SLUG = "镇巴县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-07"

# Canonical output paths (self-contained reproducible build).
DB_PATH = BASE / "data" / "database" / f"{SLUG}_network.db"
GEXF_PATH = BASE / "data" / "graph" / f"{SLUG}_network.gexf"

ORG_OFFSET = 100000


# ── Persons ─────────────────────────────────────────────────────────────────
persons = [
    # ═══════ Core targets (县委书记 & 县长) ═══════
    {
        "id": 1,
        "name": "徐红菊",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共镇巴县委员会",
        "source": "镇巴县政府要闻 2026-07-29 (县委书记徐红菊调研稳增长/安全稳定); 八一慰问 2026-08-01 (四大班子带队); 汉中市…"
    },
    {
        "id": 2,
        "name": "李波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、代县长",
        "current_org": "镇巴县人民政府",
        "source": "八一慰问 2026-08-01 (县人民政府代理县长); 调研新闻 2026-08-03 (基层治理/财政/审计/应急); 出生于/此前单位待查"
    },
    # ═══════ 前任党政正职 ═══════
    {
        "id": 3,
        "name": "韩雄 (前任县委书记)",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任县委书记 (去向待查)",
        "current_org": "中共镇巴县委员会",
        "source": "县委常委会 2026-06-30 主持; 七一走访 2026-07-01; 2025-08-25 县委十六届九次全会 讲话. 约2026-07 卸任, 去向待查."
    },
    {
        "id": 4,
        "name": "程开耀 (前任县长)",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任县长 (去向待查)",
        "current_org": "镇巴县人民政府",
        "source": "县政府全体会议 2026-01-26 主持(县长); 县委十六届九次全会 2025-08-25 安排经济工作; 常务副县长简历'协助程开耀同志工作'. 2026-07 后卸任, 去向待查."
    },
    # ═══════ 县政府班子 (官方领导之窗, 更新2026-03-12) ═══════
    {
        "id": 5,
        "name": "武芯茹",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1983-01",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "镇巴县人民政府",
        "source": "官方领导之窗 ldzc.shtml (2026-03-12 更新); 原任市政府部门副职/正职、地级市辖区镇党委书记、县委工作机关正职."
    },
    {
        "id": 6,
        "name": "周宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-01",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "镇巴县人民政府",
        "source": "官方领导之窗; 曾任武警边防部队警官, 省委直属部门机关党委副书记/纪委副书记, 央企下属单位副职."
    },
    {
        "id": 7,
        "name": "王刚刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987-06",
        "birthplace": "",
        "education": "研究生学历(经济学博士)",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "镇巴县人民政府",
        "source": "官方领导之窗; 曾任县政府副职(挂职)、乡镇党委副职(挂职)、县直属部门党组书记(兼)."
    },
    {
        "id": 8,
        "name": "张文春",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-01",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "镇巴县人民政府",
        "source": "官方领导之窗; 曾任乡镇政府副职/正职、乡镇党委正职、县政府组成部门正职."
    },
    {
        "id": 9,
        "name": "邵永宏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-04",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "镇巴县人民政府",
        "source": "官方领导之窗; 曾任乡镇政府副职、乡镇党委副职、乡镇人大正职、县区委工作机关副职、乡镇政府/党委正职."
    },
    {
        "id": 10,
        "name": "黄山",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-08",
        "birthplace": "",
        "education": "大学学历(管理学学士)",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "镇巴县人民政府",
        "source": "官方领导之窗; 曾任县政府组成部门正职."
    },
    {
        "id": 11,
        "name": "徐东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-01",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、县公安局长",
        "current_org": "镇巴县公安局",
        "source": "官方领导之窗; 曾任县(区)政法委副书记、公安局副局长、县(区)公安局政委."
    },
    {
        "id": 12,
        "name": "刘伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-07",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长、县农业农村局局长",
        "current_org": "镇巴县人民政府",
        "source": "官方领导之窗; 曾任县委工作部门副职、乡镇党委政府正职、县政府组成部门正职; 兼农业农村局党组书记/局长."
    },
    {
        "id": 13,
        "name": "杨永太",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-11",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府党组成员(挂职)",
        "current_org": "镇巴县人民政府",
        "source": "官方领导之窗; 现任省级政府组成部门机关党委副书记/机关纪委书记, 县政府党组成员、泾洋街道党工委副书记(挂职); 曾任西藏阿里地区发改委副主任."
    },
    # ═══════ 县人大 / 政协 / 县委副书记 ═══════
    {
        "id": 14,
        "name": "魏强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "镇巴县人民代表大会常务委员会",
        "source": "八一慰问 2026-08-01 (县人大常委会主任); 县委十六届九次全会 2025-08-25."
    },
    {
        "id": 15,
        "name": "王孝琴",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "政协镇巴县委员会",
        "source": "八一慰问 2026-08-01 (县政协主席); 县委十六届九次全会 2025-08-25."
    },
    {
        "id": 16,
        "name": "高栋梁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共镇巴县委员会",
        "source": "县委十六届九次全会 2025-08-25 列名县委副书记."
    },
    # ═══════ 县委常委 (2025-08-25 全会列名, 分工待查) ═══════
    {
        "id": 17,
        "name": "黄伟 (县委常委)",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委 (分工待查)",
        "current_org": "中共镇巴县委员会",
        "source": "县委十六届九次全会 2025-08-25 列名常委; 分工/简历未公开."
    },
    {
        "id": 18,
        "name": "张学武 (县委常委)",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委 (分工待查)",
        "current_org": "中共镇巴县委员会",
        "source": "县委十六届九次全会 2025-08-25 列名常委; 分工/简历未公开."
    },
    {
        "id": 19,
        "name": "龙晓涛 (县委常委)",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委 (分工待查)",
        "current_org": "中共镇巴县委员会",
        "source": "县委十六届九次全会 2025-08-25 列名常委; 八一慰问 2026-08-01 参加."
    },
    {
        "id": 20,
        "name": "蔡立新 (县委常委)",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委 (分工待查)",
        "current_org": "中共镇巴县委员会",
        "source": "县委十六届九次全会 2025-08-25 列名常委; 八一慰问 2026-08-01 参加."
    },
    {
        "id": 21,
        "name": "侯绪朋 (县委常委)",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委 (分工待查)",
        "current_org": "中共镇巴县委员会",
        "source": "县委十六届九次全会 2025-08-25 列名常委."
    },
    # ═══════ 跨县网络 (王钧平: 城固县委书记·曾任镇巴县纪委书记) ═══════
    {
        "id": 22,
        "name": "王钧平 (城固县委书记)",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-10",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "城固县委书记 (跨县线索)",
        "current_org": "中共城固县委员会",
        "source": "城固县数据库 (build_城固县_data.py, 2026-08-07): 曾任镇巴县纪委书记→汉中市人大→应急局→滨江新区→城固县长→书记."
    },
    {
        "id": 23,
        "name": "王建平 (汉中市长)",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-10",
        "birthplace": "",
        "education": "大学学历(工学学士)",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "汉中市委副书记、市长 (上级 context)",
        "current_org": "汉中市人民政府",
        "source": "汉中市政府网 2026-08-07; 2026-08-05 到镇巴调研防汛/县域经济."
    },
]


# ── Organizations ───────────────────────────────────────────────────────────
organizations = [
    {
        "id": ORG_OFFSET + 1,
        "name": "中共镇巴县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共汉中市委",
        "location": "陕西省汉中市镇巴县"
    },
    {
        "id": ORG_OFFSET + 2,
        "name": "镇巴县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "汉中市人民政府",
        "location": "陕西省汉中市镇巴县"
    },
    {
        "id": ORG_OFFSET + 3,
        "name": "镇巴县人民代表大会常务委员会",
        "type": "人大",
        "level": "县级",
        "parent": "陕西省人民代表大会常务委员会",
        "location": "陕西省汉中市镇巴县"
    },
    {
        "id": ORG_OFFSET + 4,
        "name": "政协镇巴县委员会",
        "type": "政协",
        "level": "县级",
        "parent": "政协陕西省委员会",
        "location": "陕西省汉中市镇巴县"
    },
    {
        "id": ORG_OFFSET + 5,
        "name": "镇巴县纪律检查委员会",
        "type": "纪律检查",
        "level": "县级",
        "parent": "中共汉中市纪律检查委员会",
        "location": "陕西省汉中市镇巴县"
    },
    {
        "id": ORG_OFFSET + 6,
        "name": "镇巴县公安局",
        "type": "政府",
        "level": "县级",
        "parent": "镇巴县人民政府",
        "location": "陕西省汉中市镇巴县"
    },
    {
        "id": ORG_OFFSET + 7,
        "name": "镇巴县农业农村局",
        "type": "政府",
        "level": "县级",
        "parent": "镇巴县人民政府",
        "location": "陕西省汉中市镇巴县"
    },
    {
        "id": ORG_OFFSET + 8,
        "name": "中共汉中市委",
        "type": "党委",
        "level": "地级市",
        "parent": "中共陕西省委",
        "location": "陕西省汉中市"
    },
    {
        "id": ORG_OFFSET + 9,
        "name": "汉中市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "陕西省人民政府",
        "location": "陕西省汉中市"
    },
    {
        "id": ORG_OFFSET + 10,
        "name": "中共城固县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中共汉中市委",
        "location": "陕西省汉中市城固县"
    },
]


# ── Positions ──────────────────────────────────────────────────────────────
positions = [
    # 徐红菊 (书记)
    {"person_id": 1, "org_id": ORG_OFFSET + 1, "title": "县委书记", "start": "2026-07", "end": "present", "rank": "正处级", "note": "约2026-07-28起; 2026-08-01 带队八一慰问"},
    # 李波 (代县长)
    {"person_id": 2, "org_id": ORG_OFFSET + 2, "title": "县委副书记、代理县长", "start": "2026-07", "end": "present", "rank": "正处级", "note": "2026-08-01 八一活动确认; 2026-08-03 调研"},
    {"person_id": 2, "org_id": ORG_OFFSET + 1, "title": "县委副书记", "start": "2026-07", "end": "present", "rank": "正处级", "note": ""},
    # 韩雄 (前书记)
    {"person_id": 3, "org_id": ORG_OFFSET + 1, "title": "县委书记 (前任)", "start": "", "end": "2026-07", "rank": "正处级", "note": "截至2026-07-01在任, 之后卸任, 去向待查"},
    # 程开耀 (前县长)
    {"person_id": 4, "org_id": ORG_OFFSET + 2, "title": "县长 (前任)", "start": "", "end": "2026-07", "rank": "正处级", "note": "2026-01-26主持县政府全体会议; 卸任, 去向待查"},
    # 县政府班子
    {"person_id": 5, "org_id": ORG_OFFSET + 2, "title": "县委常委、常务副县长", "start": "", "end": "present", "rank": "副处级", "note": "党组副书记; 协助县长抓好日常工作"},
    {"person_id": 6, "org_id": ORG_OFFSET + 2, "title": "县委常委、副县长", "start": "", "end": "present", "rank": "副处级", "note": "原武警边防/省委机关"},
    {"person_id": 7, "org_id": ORG_OFFSET + 2, "title": "县委常委、副县长", "start": "", "end": "present", "rank": "副处级", "note": "经济学博士"},
    {"person_id": 8, "org_id": ORG_OFFSET + 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": ORG_OFFSET + 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "研究生"},
    {"person_id": 10, "org_id": ORG_OFFSET + 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "管理学学士"},
    {"person_id": 11, "org_id": ORG_OFFSET + 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": ORG_OFFSET + 6, "title": "县公安局长、党委书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": ORG_OFFSET + 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": ORG_OFFSET + 7, "title": "县农业农村局党组书记、局长(兼)", "start": "", "end": "present", "rank": "正科级", "note": "兼"},
    {"person_id": 13, "org_id": ORG_OFFSET + 2, "title": "县政府党组成员(挂职)", "start": "", "end": "present", "rank": "副处级", "note": "省级机关挂职; 泾洋街道党工委副书记"},
    # 人大 / 政协 / 县委
    {"person_id": 14, "org_id": ORG_OFFSET + 3, "title": "县人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 15, "org_id": ORG_OFFSET + 4, "title": "县政协主席", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 16, "org_id": ORG_OFFSET + 1, "title": "县委副书记", "start": "", "end": "present", "rank": "", "note": "2025-08 全会名录"},
    {"person_id": 17, "org_id": ORG_OFFSET + 1, "title": "县委常委", "start": "", "end": "present", "rank": "", "note": "分工待查"},
    {"person_id": 18, "org_id": ORG_OFFSET + 1, "title": "县委常委", "start": "", "end": "present", "rank": "", "note": "分工待查"},
    {"person_id": 19, "org_id": ORG_OFFSET + 1, "title": "县委常委", "start": "", "end": "present", "rank": "", "note": "分工待查"},
    {"person_id": 20, "org_id": ORG_OFFSET + 1, "title": "县委常委", "start": "", "end": "present", "rank": "", "note": "分工待查"},
    {"person_id": 21, "org_id": ORG_OFFSET + 1, "title": "县委常委", "start": "", "end": "present", "rank": "", "note": "分工待查"},
    # 跨县 / 上级
    {"person_id": 22, "org_id": ORG_OFFSET + 10, "title": "城固县委书记 (跨县线索)", "start": "2026-08", "end": "present", "rank": "正处级", "note": "前曾任镇巴县纪委书记"},
    {"person_id": 22, "org_id": ORG_OFFSET + 5, "title": "镇巴县纪委书记 (历史)", "start": "", "end": "", "rank": "副处级", "note": "跨县线索(转城固)"},
    {"person_id": 23, "org_id": ORG_OFFSET + 9, "title": "汉中市委副书记、市长", "start": "", "end": "present", "rank": "正厅级", "note": "上级 context"},
]


# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    # 党政正职搭档 (书记—代县长)
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记徐红菊 与 代县长李波 现党政搭档 (2026-07/08 换届后班子)",
        "overlap_org": "镇巴县",
        "overlap_period": "2026-",
        "strength": "strong",
        "confidence": "confirmed"
    },
    # 书记—代县长 班子交接
    {
        "person_a": 1, "person_b": 2,
        "type": "predecessor_successor",
        "context": "新任书记徐红菊 与 新任代县长李波 同期履新 (2026-07) — 全新党政班子",
        "overlap_org": "镇巴县",
        "overlap_period": "2026",
        "strength": "strong",
        "confidence": "plausible"
    },
    # 前任书记 韩雄 → 徐红菊 (书记接班)
    {
        "person_a": 3, "person_b": 1,
        "type": "predecessor_successor",
        "context": "韩雄卸任镇巴县委书记(约2026-07) 后 徐红菊接任",
        "overlap_org": "中共镇巴县委员会",
        "overlap_period": "2026",
        "strength": "strong",
        "confidence": "confirmed"
    },
    # 前任县长 程开耀 → 李波 (县长接班)
    {
        "person_a": 4, "person_b": 2,
        "type": "predecessor_successor",
        "context": "程开耀卸任镇长(2026-07)后李波任代县长",
        "overlap_org": "镇巴县人民政府",
        "overlap_period": "2026",
        "strength": "strong",
        "confidence": "confirmed"
    },
    # 前任书记 韩雄 — 前任县长 程开耀 (原党政搭档)
    {
        "person_a": 3, "person_b": 4,
        "type": "overlap",
        "context": "韩雄(书记) 与 程开耀(县长) 原党政搭档 (2025-2026初)",
        "overlap_org": "镇巴县",
        "overlap_period": "2025-2026",
        "strength": "strong",
        "confidence": "confirmed"
    },
    # 常务副县长 武芯茹 — 前县长 程开耀 (协助)
    {
        "person_a": 5, "person_b": 4,
        "type": "superior_subordinate",
        "context": "常务副县长武芯茹 协助前县长程开耀抓好日常工作 (领导之窗简历)",
        "overlap_org": "镇巴县人民政府",
        "overlap_period": "-2026",
        "strength": "strong",
        "confidence": "confirmed"
    },
    # 书记 与 常务副县长
    {
        "person_a": 1, "person_b": 5,
        "type": "superior_subordinate",
        "context": "县委书记 与 常务副县长武芯茹",
        "overlap_org": "镇巴县人民政府",
        "overlap_period": "2026-",
        "strength": "medium",
        "confidence": "confirmed"
    },
    # 代县长 与 常务副县长
    {
        "person_a": 2, "person_b": 5,
        "type": "overlap",
        "context": "代县长李波 与 常务副县长武芯茹 共事(政府班子)",
        "overlap_org": "镇巴县人民政府",
        "overlap_period": "2026-",
        "strength": "medium",
        "confidence": "confirmed"
    },
    # 同班子 副县长 (政府班子共同成员)
    {
        "person_a": 5, "person_b": 6,
        "type": "overlap",
        "context": "常务副县长武芯茹 与 副县长周宇 同政府班子",
        "overlap_org": "镇巴县人民政府",
        "overlap_period": "2026-",
        "strength": "weak",
        "confidence": "confirmed"
    },
    {
        "person_a": 11, "person_b": 1,
        "type": "superior_subordinate",
        "context": "副县长/公安局长徐东 隶属县委县政府领导",
        "overlap_org": "镇巴县人民政府",
        "overlap_period": "2026-",
        "strength": "medium",
        "confidence": "confirmed"
    },
    # 人大/政协 与 书记
    {
        "person_a": 14, "person_b": 1,
        "type": "overlap",
        "context": "县人大主任魏强 与 县委书记 (四套班子搭档, 八一活动同框)",
        "overlap_org": "镇巴县",
        "overlap_period": "2026-",
        "strength": "medium",
        "confidence": "confirmed"
    },
    {
        "person_a": 15, "person_b": 1,
        "type": "overlap",
        "context": "县政协主席王孝琴 与 书记 (四套班子搭档)",
        "overlap_org": "镇巴县",
        "overlap_period": "2026-",
        "strength": "medium",
        "confidence": "confirmed"
    },
    # 跨县网络: 镇巴县纪委 → 城固县委书记 (王钧平)
    {
        "person_a": 22, "person_b": 1,
        "type": "same_system",
        "context": "王钧平(现任城固县委书记)曾长期在镇巴县纪委工作, 与镇巴县委机构有组织条线交集",
        "overlap_org": "镇巴县",
        "overlap_period": "历史",
        "strength": "weak",
        "confidence": "plausible"
    },
    # 汉中市长 与 镇巴县委
    {
        "person_a": 23, "person_b": 1,
        "type": "superior_subordinate",
        "context": "汉中市长王建平 2026-08-05 到镇巴调研, 接受县委县政府工作汇报",
        "overlap_org": "汉中市",
        "overlap_period": "2026",
        "strength": "weak",
        "confidence": "confirmed"
    },
    {
        "person_a": 23, "person_b": 2,
        "type": "superior_subordinate",
        "context": "汉中市长 与 代县长李波 (市—县政府上下级)",
        "overlap_org": "汉中市",
        "overlap_period": "2026",
        "strength": "weak",
        "confidence": "confirmed"
    },
]


# ═══════════════════════════════════════════════════════════════════════════
# Database + GEXF build
# ═══════════════════════════════════════════════════════════════════════════

def build():
    """Build SQLite database and GEXF graph."""
    sys.path.insert(0, str(BASE))
    from gov_relation.runner import run_build

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


def verify():
    """Verify output files exist and have correct structure."""
    import sqlite3
    errors = []

    if not DB_PATH.exists():
        errors.append(f"Database not found: {DB_PATH}")
    else:
        conn = sqlite3.connect(str(DB_PATH))
        tables = [row[0] for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )]
        expected = ["persons", "organizations", "positions", "relationships"]
        for t in expected:
            if t not in tables:
                errors.append(f"Missing table: {t}")
        for t in expected:
            c = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
            print(f"  {t}: {c}")
        conn.close()

    if not GEXF_PATH.exists():
        errors.append(f"GEXF not found: {GEXF_PATH}")
    else:
        content = GEXF_PATH.read_text("utf-8")
        if '<gexf' not in content:
            errors.append("GEXF missing <gexf> tag")
        if '<nodes>' not in content:
            errors.append("GEXF missing <nodes>")
        if '<edges>' not in content:
            errors.append("GEXF missing <edges>")
        if '</gexf>' not in content:
            errors.append("GEXF missing closing </gexf>")

    if errors:
        for e in errors:
            print(f"  ERROR: {e}")
        return False
    print("  Verification: PASSED")
    return True


if __name__ == "__main__":
    print(f"Building {SLUG} network...")
    build()
    print("\nVerifying...")
    if verify():
        print("\nDone. Files created:")
        print(f"  DB:   {DB_PATH}")
        print(f"  GEXF: {GEXF_PATH}")
    else:
        print("\nFAILED: verification errors")
        sys.exit(1)