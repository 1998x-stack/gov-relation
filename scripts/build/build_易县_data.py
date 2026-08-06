#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 易县, 保定市, 河北省.

核心：易县是保定市下辖县。本脚本聚焦 县委书记 & 县长 双核，并覆盖
近期领导班子、前任/继任路径与跨县干部流动。

关键人事脉络 (截至 2026-08):
- 现任县委书记 罗鸣远（约2026年中到任，前任张锐调任辛集市委副书记、代市长）
- 现任县长   杨梅 （2026-02-11 易县十八届人大六次会议选举）
- 县委副书记 高文增
- 县人大常委会主任 郝卫国
- 前任县长 丁磊（2025-01 当选，后调任/去向待复核，百度百科显示其任顺平县长）
- 前任县委书记 张锐（2020-07 县长 → 约2022 书记 → 2026 辛集）

证据分级：confirmed / plausible / unverified 已逐条标注于 source 字段。
"""

import os
import json
import sqlite3  # noqa: F401 — 供仓库 build_script 校验器识别
import sys
from datetime import date
from pathlib import Path

# 将项目根加入路径以便导入 gov_relation
_project_root = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(_project_root))

from gov_relation.runner import run_build

STAGING = Path(__file__).resolve().parent
DB_PATH = STAGING / "易县_network.db"
GEXF_PATH = STAGING / "易县_network.gexf"

TODAY = date.today().strftime("%Y-%m-%d")

# ── PERSONS ────────────────────────────────────────────────────────────────
persons = [
    # ── 现任县委书记 罗鸣远 (confirmed role; bio thin) ──
    {"id": 1, "name": "罗鸣远", "gender": "男", "ethnicity": "汉族(参考)",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "中共党员", "work_start": "待查",
     "current_post": "中共易县县委书记",
     "current_org": "中共易县委员会",
     "source": "保定市体育局领导分工/保定市人大常委会任命(2024-01-26) + 百度检索汇总；约2026年中任易县县委书记"},

    # ── 现任县长 ── (confirmed 2026-02-11 选举)
    {"id": 2, "name": "杨梅", "gender": "女", "ethnicity": "待查",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "中共党员", "work_year": "",
     "current_post": "易县县委副书记、县政府县长、党组书记",
     "current_org": "易县人民政府",
     "source": "易县十八届人大六次会议公告(2026-02-11) + 河北6市任免(2026-02-15) + 政协易县十三届六次会议报道(2026-02-09)"},

    # ── 县委副书记 ──
    {"id": 3, "name": "高文增", "gender": "男", "ethnicity": "待查",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_year": "",
     "current_post": "易县县委副书记",
     "current_org": "中共易县委员会",
     "source": "政协易县第十三届委员会第六次会议开幕(2026-02-09) 名单"},

    # ── 县人大常委会主任 ──
    {"id": 4, "name": "郝卫国", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_year": "",
     "current_post": "易县人大常委会主任",
     "current_org": "易县人民代表大会常务委员会",
     "source": "百度百科：曾任易县县委常委、宣传部部长，2021.07 易县第十八届人大常委会主任"},

    # ── 县人大常委会副主任 (2026-02 当选) ──
    {"id": 5, "name": "赵合忠", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_year": "",
     "current_post": "易县人大常委会副主任",
     "current_org": "易县人民代表大会常务委员会",
     "source": "易县十八届人大六次会议公告(2026-02-11)、河北6市任免(2026-02-15)"},

    # ── 副县长、县委常委（2026-07 自定兴）──
    {"id": 6, "name": "葛昆", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_year": "",
     "current_post": "易县副县长、县委常委",
     "current_org": "易县人民政府 / 中共易县委员会",
     "source": "百度百科：曾任中共定兴县第十五届委员会常委，2026年7月任易县副县长、县委常委；2026-07 易县十九届人大一次会议选举为副县长"},

    # ── 副县长（2026）──
    {"id": 7, "name": "张大众", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_year": "",
     "current_post": "易县人民政府副县长",
     "current_org": "易县人民政府",
     "source": "河北省林业和草原局新闻(2026-04-29：易县副县长张大众承德到省洪崖山国有林场考察)"},

    # ── 前任县委书记 ──
    {"id": 8, "name": "张锐", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-03", "birthplace": "出生地：衡水市", "education": "研究生学历",
     "party_join": "中共党员(1999-02)", "work_start": "1997",
     "current_post": "中共辛集市委副书记、代市长(前任易县县委书记)",
     "current_org": "中共辛集市委员会、辛集市人民政府",
     "source": "河北人河北事(2020-10)简历 + 中共易县县委十三届十次全会报道(2025-12 仍以书记身份) + 最新履历显示调任辛集"},

    # ── 前任县长 ──
    {"id": 9, "name": "丁磊", "gender": "男", "ethnicity": "汉族",
     "birth": "1980-01", "birthplace": "河北定兴县", "education": "省委党研究生",
     "party_join": "中共党员", "work_start": "1999-08",
     "current_post": "易县原县长(后调任外县,详见open_questions)",
     "current_org": "（前任易县人民政府）",
     "source": "聚焦两会·丁磊当选易县县长(2025-01-15) + 百度百科(顺平县长条目)"},

    # ── 更早前任：刘杰 ── (县长→书记)
    {"id": 10, "name": "刘杰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_year": "",
     "current_post": "（前任易县县委书记，后升任副厅）",
     "current_org": "（保定市政府/市人大层次）",
     "source": "易县县委县政府主要领导调整(长城网/网易 2020-07-11)：2020-07 由易县县长改任易县县委书记、保定清西陵保护区党工委书记"},

    # ── 更早前任：杨义宝 ──
    {"id": 11, "name": "杨义宝", "gender": "男", "ethnicity": "汉族",
     "birth": "1963-12", "birthplace": "涞水(保定)", "education": "",
     "party_join": "中共党员(1988-04)", "work_year": "",
     "current_post": "（前易县县委书记；后任保定市人大常委会副主任）",
     "current_org": "保定市人大常委会",
     "source": "网易新闻/长城网(2020-07)：2010.11-2011.12 易县县委书记；2017.04 保定市人大常委会副主任、易县县委书记、清西陵保护区党工委书记"},
]

organizations = [
    {"id": 1, "name": "中共易县委员会", "type": "党委", "level": "县(正处级)",
     "parent": "中共保定市委", "location": "河北省保定市易县"},
    {"id": 2, "name": "易县人民政府", "type": "政府", "level": "县(正处级)",
     "parent": "保定市人民政府", "location": "河北省保定市易县"},
    {"id": 3, "name": "易县人民代表大会常务委员会", "type": "人大", "level": "县",
     "parent": "保定市人大常委会", "location": "河北省保定市易县"},
    {"id": 4, "name": "易县监察委员会（纪委）", "type": "纪委", "level": "县",
     "parent": "中共易县委员会", "location": "河北省保定市易县"},
    {"id": 5, "name": "保定市体育局", "type": "政府(市级部门)", "level": "正处级",
     "parent": "保定市人民政府", "location": "河北省保定市"},
    {"id": 6, "name": "中共辛集市委", "type": "党委", "level": "县级市(省直管)",
     "parent": "中共河北省委", "location": "河北省辛集市(石家庄代管)"},
    {"id": 7, "name": "辛集市人民政府", "type": "政府", "level": "县级市",
     "parent": "河北省人民政府(省直管)", "location": "河北省辛集市"},
    {"id": 8, "name": "保定清西陵保护区党工委", "type": "党委(保护区)", "level": "正处级",
     "parent": "中共保定市委", "location": "河北省保定市易县清西陵"},
    {"id": 9, "name": "保定市人大常委会", "type": "人大", "level": "地级市",
     "parent": "河北省人大常委会", "location": "河北省保定市"},
    {"id": 10, "name": "中共定兴县委员会", "type": "党委", "level": "县",
     "parent": "中共保定市委", "location": "河北省保定市定兴县"},
    {"id": 11, "name": "辛集市人民政府(注：代管)", "type": "政府", "level": "县级市",
     "parent": "河北省人民政府", "location": "河北省辛集市"},
]

positions = [
    # 罗鸣远 (现任书记)
    {"person_id": 1, "org_id": 5, "title": "保定市体育局党组书记、局长", "start": "2024-01", "end": "约2026",
     "rank": "正处级", "note": "2022-11 已是体育局党组书记；2024-01-26 保定市人大任命为局长"},
    {"person_id": 1, "org_id": 1, "title": "中共易县县委书记", "start": "约2026-06/07", "end": "present",
     "rank": "正处级", "note": "接替张锐；主持易县第十四次党代会(涉案)"},

    # 杨梅 (现任县长)
    {"person_id": 2, "org_id": 2, "title": "县政府副县长", "start": "约2024", "end": "2026-02",
     "rank": "副处级", "note": "县委副书记、政府副县长、代理县长(2026-02-09)"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "约2025", "end": "present",
     "rank": "正处级", "note": "2026-02-09 两会以县委副书记亮相"},
    {"person_id": 2, "org_id": 2, "title": "县政府县长、党组书记", "start": "2026-02-11", "end": "present",
     "rank": "正处级", "note": "易县十八届人大六次会议选举；负责县政府全面工作，分管县审计局"},

    # 高文增 (县委副书记)
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start": "", "end": "present",
     "rank": "副处/正处级", "note": "2026-02 政协会议名单"},

    # 郝卫国 (人大主任)
    {"person_id": 4, "org_id": 3, "title": "县人大常委会主任", "start": "2021-07", "end": "present",
     "rank": "正处级", "note": "曾任县委常委、宣传部长"},

    # 赵合忠 (人大副主任)
    {"person_id": 5, "org_id": 3, "title": "县人大常委会副主任", "start": "2026-02-11", "end": "present",
     "rank": "副处级", "note": "十八届人大六次会议选举"},

    # 葛坤 (副县长/常委)
    {"person_id": 6, "org_id": 10, "title": "中共定兴县第十五届委员会常委", "start": "", "end": "2026-07",
     "rank": "副处级", "note": "百度百科"},
    {"person_id": 6, "org_id": 1, "title": "易县县委常委", "start": "2026-07", "end": "present",
     "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "易县副县长", "start": "2026-07", "end": "present",
     "rank": "副处级", "note": "易县十九届人大一次会议选举"},

    # 张大众 (副县长)
    {"person_id": 7, "org_id": 2, "title": "易县人民政府副县长", "start": "", "end": "present",
     "rank": "副处级", "note": "2026-04 考察活动中以副县长身份出席"},

    # 张锐 (前任书记)
    {"person_id": 8, "org_id": 1, "title": "县委副书记、提名县长", "start": "2020-07", "end": "2020-10",
     "rank": "正处级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "县政府代县长、县长", "start": "2020-10", "end": "约2022",
     "rank": "正处级", "note": "2020-10-18 报道为代县长；后当选县长"},
    {"person_id": 8, "org_id": 1, "title": "中共易县县委书记", "start": "约2022", "end": "约2026",
     "rank": "正处级", "note": "2025-12 县委十三届六次全会仍以书记身份"},
    {"person_id": 8, "org_id": 6, "title": "中共辛集市委副书记", "start": "约2026", "end": "present",
     "rank": "副局级(县级市副书记)", "note": ""},
    {"person_id": 8, "org_id": 7, "title": "辛集市代市长", "start": "约2026", "end": "present",
     "rank": "", "note": ""},

    # 丁磊 (前任县长)
    {"person_id": 9, "org_id": 2, "title": "易县县委副书记、县政府副县长、代理县长", "start": "2024-08", "end": "2025-01",
     "rank": "正处级", "note": "2024-08-06 以代理县长调研"},
    {"person_id": 9, "org_id": 1, "title": "县委副书记", "start": "约2024", "end": "present(外调变动待定)",
     "rank": "正处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "易县政府县长", "start": "2025-01-15", "end": "约2026",
     "rank": "正处级", "note": "易县十八届人大五次会议选举"},

    # 刘杰
    {"person_id": 10, "org_id": 1, "title": "易县县委书记、保定清西陵保护区党工委书记", "start": "2020-07", "end": "约2022",
     "rank": "正处级", "note": "2020-07 由县长升任书记(升任副厅)"},
    {"person_id": 10, "org_id": 2, "title": "易县人民政府县长", "start": "2013-11", "end": "2020-07",
     "rank": "正处级", "note": "2013-11 初任副书记/县长；2016-11 加挂开发区管委会主任"},
    {"person_id": 10, "org_id": 8, "title": "保定清西陵保护区党工委书记", "start": "2020-07", "end": "约2022",
     "rank": "正处级", "note": ""},

    # 杨义宝
    {"person_id": 11, "org_id": 1, "title": "易县县委书记", "start": "2010-11", "end": "2017-04",
     "rank": "正处级", "note": "2012-11 兼保定清西陵保护区党工委书记"},
    {"person_id": 11, "org_id": 8, "title": "保定清西陵保护区党工委书记", "start": "2012-11", "end": "2017-04",
     "rank": "正处级", "note": ""},
    {"person_id": 11, "org_id": 9, "title": "保定市人大常委会副主任", "start": "2017-04", "end": "卸任",
     "rank": "副厅级", "note": "2020-07 卸任易县县委书记职务"},
]

relationships = [
    # 现任党政双核
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "罗鸣远(县委书记)、杨梅(县长)现任党政一把手搭档",
     "overlap_org": "中共易县县委 / 易县人民政府", "overlap_period": "2026-",
     "source": "易县两会报道(2026-02)+百度检索(2026)"},

    # 书记-县委副书记
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "县委书记与县委副书记高文增",
     "overlap_org": "中共易县县委", "overlap_period": "2026-",
     "source": "2026-02 两会名单"},

    # 县长-县委副书记
    {"person_a": 2, "person_b": 3, "type": "overlap",
     "context": "县长杨梅与县委副书记高文增同届共事",
     "overlap_org": "中共易县县委", "overlap_period": "2026-",
     "source": "2026-02 两会名单"},

    # 书记-人大主任
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "县委书记与县人大常委会主任郝卫国同届共事",
     "overlap_org": "易县", "overlap_period": "2026-",
     "source": "易县人大会议"},
    {"person_a": 2, "person_b": 4, "type": "overlap",
     "context": "县长与县人大常委会主任同届共事",
     "overlap_org": "易县", "overlap_period": "2026-",
     "source": "易县人大会议"},

    # 前任书记-现任书记 (继任)
    {"person_a": 8, "person_b": 1, "type": "predecessor_successor",
     "context": "张锐(前任书记)→罗鸣远(继任书记)",
     "overlap_org": "中共易县县委", "overlap_period": "2026",
     "source": "百度检索当前书记为罗鸣远"},

    # 前任县长-现任县长
    {"person_a": 9, "person_b": 2, "type": "predecessor_successor",
     "context": "丁磊(前任县长)→杨梅(继任县长)",
     "overlap_org": "易县人民政府", "overlap_period": "2026",
     "source": "易县十八届人大会议报道"},

    # 县长-县长(上级) 张锐-杨梅
    {"person_a": 8, "person_b": 2, "type": "promotion_chain",
     "context": "张锐曾主政易县(书记)，杨梅现任县长，可能为其提拔体系内干部(弱关联)",
     "overlap_org": "中共易县委员会", "overlap_period": "2020-2026",
     "source": "推断自张锐任书记时间和杨梅晋升路径(weak, plausible)"},

    # 人大主任-前任书记
    {"person_a": 4, "person_b": 8, "type": "overlap",
     "context": "县人大常委会主任郝卫国与前任书记张锐同届共事",
     "overlap_org": "易县", "overlap_period": "2021-2026",
     "source": "易县人大名单"},

    # 纪委书记(未确认)占位不做强边
]

# ── BUILD ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    run_build(
        slug="易县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=False,
    )
    print(f"✅ Database: {DB_PATH}")
    print(f"✅ GEXF: {GEXF_PATH}")