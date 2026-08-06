#!/usr/bin/env python3
"""龙亭区领导班子工作关系网络数据生成脚本。

行政区划：河南省 开封市 龙亭区（市辖区）。
目标对象：区委书记 李涛  &  区长 陈嘉慧。

数据来源（均为龙亭区人民政府门户网站 longting.gov.cn 官方一手信源）：
- 领导信息栏目（c00873）：陈嘉慧（区长）、刘国歌（常务副区长）、张永刚（副区长/宣传部长）、
  刘卫华（副区长/公安分局局长）、王风来（副区长）等编制简历
- 龙亭要闻（c00292）：任免公告、中国共产党龙亭区第十二届委员会第一次全体会议（2026-06）、
  第十七届人大六次会议（2026-02）等
- 信息截至 2026-08

用法：
    python3 data/tmp/henan_龙亭区/build_龙亭区_data.py
"""

import os
import sys

# 允许独立运行（仓库根目录 / scripts/build / data/tmp 均可）
_HERE = os.path.dirname(os.path.abspath(__file__))
for _p in (_HERE, os.path.join(_HERE, "..", ".."), os.path.join(_HERE, "..", "..", "..")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import sqlite3  # noqa: E402  (process_tmp 校验 token)
from pathlib import Path  # noqa: E402

from gov_relation.paths import REPO_ROOT  # noqa: E402
from gov_relation.runner import run_build  # noqa: E402

SLUG = "龙亭区"
TASK_ID = "henan_龙亭区"
STAGING = REPO_ROOT / "data" / "tmp" / TASK_ID

# ── 规范化路径（写往 staging；DB_PATH/GEXF_PATH token 供 process_tmp 校验与提升）──
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# ── 组织 ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共开封市龙亭区委员会", "type": "党委", "level": "市辖区", "parent": "中共开封市委员会", "location": "龙亭区"},
    {"id": 2, "name": "开封市龙亭区人民政府", "type": "政府", "level": "市辖区", "parent": "开封市人民政府", "location": "龙亭区"},
    {"id": 3, "name": "开封市龙亭区人民代表大会常务委员会", "type": "人大", "level": "市辖区", "parent": "开封市龙亭区委员会", "location": "龙亭区"},
    {"id": 4, "name": "政协开封市龙亭区委员会", "type": "政协", "level": "市辖区", "parent": "政协开封市委员会", "location": "龙亭区"},
    {"id": 5, "name": "中共龙亭区纪律检查委员会", "type": "党委", "level": "市辖区", "parent": "中共开封市龙亭区委员会", "location": "龙亭区"},
    {"id": 6, "name": "中共龙亭区委组织部", "type": "党委", "level": "市辖区", "parent": "中共开封市龙亭区委员会", "location": "龙亭区"},
    {"id": 7, "name": "中共龙亭区委宣传部", "type": "党委", "level": "市辖区", "parent": "中共开封市龙亭区委员会", "location": "龙亭区"},
    {"id": 8, "name": "开封市公安局龙亭分局", "type": "政府部门", "level": "市辖区", "parent": "开封市公安局", "location": "龙亭区"},
    {"id": 9, "name": "中共开封市委员会", "type": "党委", "level": "地级市", "parent": "中共河南省委", "location": "开封市"},
    {"id": 10, "name": "开封市人民政府", "type": "政府", "level": "地级市", "parent": "河南省人民政府", "location": "开封市"},
    {"id": 11, "name": "政协开封市委员会", "type": "政协", "level": "地级市", "parent": "政协河南省委员会", "location": "开封市"},
]

# ── 人员 ─────────────────────────────────────────────────────────────
persons = [
    # ── 现任党政正职 ──
    {"id": 1, "name": "李涛", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "中共龙亭区委书记", "current_org": "中共开封市龙亭区委员会",
     "source": "https://www.longting.gov.cn/（2023-04-26《李涛同志任中共开封市龙亭区委书记》）"},
    {"id": 2, "name": "陈嘉慧", "gender": "女", "ethnicity": "汉族", "birth": "1983-03", "birthplace": "",
     "education": "本科学历，经济学硕士", "party_join": "中共党员", "work_start": "",
     "current_post": "区委副书记、区长、区政府党组书记", "current_org": "开封市龙亭区人民政府",
     "source": "https://www.longting.gov.cn/ltq/c00873/pc/content/content_1899310511980101632.html"},

    # ── 区委十二届常委会（2026-06-22 当选）──
    {"id": 3, "name": "郑华腾", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区委副书记", "current_org": "中共开封市龙亭区委员会",
     "source": "https://www.longting.gov.cn/（龙亭区第十二届区委一次全会，2026-06-22）"},
    {"id": 4, "name": "刘国歌", "gender": "女", "ethnicity": "汉族", "birth": "1980-12", "birthplace": "",
     "education": "硕士研究生学历", "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、区政府党组副书记、常务副区长", "current_org": "开封市龙亭区人民政府",
     "source": "https://www.longting.gov.cn/ltq/c00873/pc/content/content_1899310558331075072.html"},
    {"id": 5, "name": "李希峰", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委", "current_org": "中共开封市龙亭区委员会",
     "source": "https://www.longting.gov.cn/（龙亭区第十二届区委全会，2026-06-22）"},
    {"id": 6, "name": "张永刚", "gender": "男", "ethnicity": "汉族", "birth": "1974-10", "birthplace": "",
     "education": "大学学历", "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委、宣传部部长、副区长", "current_org": "开封市龙亭区人民政府",
     "source": "https://www.longting.gov.cn/ltq/c00873/pc/content/content_1899310519538237440.html"},
    {"id": 7, "name": "刘龙飞", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委", "current_org": "中共开封市龙亭区委员会",
     "source": "https://www.longting.gov.cn/（龙亭区第十二届区委全会，2026-06-22）"},
    {"id": 8, "name": "阮志鹏", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委", "current_org": "中共开封市龙亭区委员会",
     "source": "https://www.longting.gov.cn/（龙亭区第十二届区委全会，2026-06-22）"},
    {"id": 9, "name": "张波", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委", "current_org": "中共开封市龙亭区委员会",
     "source": "https://www.longting.gov.cn/（龙亭区第十二届区委全会，2026-06-22）"},
    {"id": 10, "name": "王硕", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委", "current_org": "中共开封市龙亭区委员会",
     "source": "https://www.longting.gov.cn/（龙亭区第十二届区委全会，2026-06-22）"},
    {"id": 11, "name": "孙文超", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区委常委", "current_org": "中共开封市龙亭区委员会",
     "source": "https://www.longting.gov.cn/（龙亭区第十二届区委全会，2026-06-22）"},

    # ── 区政府其他副区长 ──
    {"id": 12, "name": "刘卫华", "gender": "男", "ethnicity": "汉族", "birth": "1976-12", "birthplace": "",
     "education": "研究生学历", "party_join": "中共党员", "work_start": "",
     "current_post": "副区长、龙亭公安分局局长", "current_org": "开封市公安局龙亭分局",
     "source": "https://www.longting.gov.cn/ltq/c00873/pc/content/content_1899310523279556608.html"},
    {"id": 13, "name": "王风来", "gender": "男", "ethnicity": "汉族", "birth": "1974-10", "birthplace": "",
     "education": "大学学历", "party_join": "中共党员", "work_start": "",
     "current_post": "副区长", "current_org": "开封市龙亭区人民政府",
     "source": "https://www.longting.gov.cn/ltq/c00873/pc/content/content_1899310603692752896.html"},

    # ── 人大 / 政协 ──
    {"id": 14, "name": "郭峰", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "区人大常委会主任", "current_org": "开封市龙亭区人民代表大会常务委员会",
     "source": "https://www.longting.gov.cn/（龙亭区第十七届人大六次会议，2026-02）"},

    # ── 前任领导 ──
    {"id": 15, "name": "张正濠", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "开封市政协党组成员、副主席（前任龙亭区委书记）", "current_org": "政协开封市委员会",
     "source": "https://www.longting.gov.cn/（2023-04 卸任区委书记）"},
    {"id": 16, "name": "张海", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "前任常务副区长（2023 年在任）", "current_org": "开封市龙亭区人民政府",
     "source": "https://www.longting.gov.cn/（2023 年新闻）"},
    {"id": 17, "name": "闫泊含", "gender": "女", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "前任副区长（2023 年在任）", "current_org": "开封市龙亭区人民政府",
     "source": "https://www.longting.gov.cn/（2023 年新闻）"},
]

# ── 任职 ─────────────────────────────────────────────────────────────
positions = [
    # 李涛
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "2023-04", "end_date": "present", "rank": "县处级", "note": "2023-04-25 市委组织部宣布任区委书记，此前任区长；一肩挑至 2023-09"},
    {"person_id": 1, "org_id": 2, "title": "区长（前任）", "start_date": "", "end_date": "2023-09", "rank": "县处级", "note": "就地晋升，区长任内被沿用至陈嘉慧接任"},
    # 陈嘉慧
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "2023-09", "end_date": "present", "rank": "县处级", "note": "2023-09-04 市委宣布任区委副书记、提名区长"},
    {"person_id": 2, "org_id": 2, "title": "区长、区政府党组书记", "start_date": "2023-09", "end_date": "present", "rank": "县处级", "note": ""},
    # 郑华腾
    {"person_id": 3, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "present", "rank": "县处级", "note": "2026-06 当选十二届区委副书记"},
    # 刘国歌
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "县处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "常务副区长", "start_date": "", "end_date": "present", "rank": "县处级", "note": "区政府党组副书记"},
    # 李希峰
    {"person_id": 5, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "县处级", "note": ""},
    # 张永刚
    {"person_id": 6, "org_id": 1, "title": "区委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "县处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "县处级", "note": ""},
    # 刘龙飞 / 阮志鹏 / 张波 / 王硕 / 孙文超
    {"person_id": 7, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "县处级", "note": "2026-06 当选"},
    {"person_id": 8, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "县处级", "note": "2026-06 当选"},
    {"person_id": 9, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "县处级", "note": "2026-06 当选"},
    {"person_id": 10, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "县处级", "note": "2026-06 当选"},
    {"person_id": 11, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "县处级", "note": "2026-06 当选"},
    # 刘卫华
    {"person_id": 12, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "县处级", "note": ""},
    {"person_id": 12, "org_id": 8, "title": "公安分局局长", "start_date": "", "end_date": "present", "rank": "县处级", "note": ""},
    # 王风来
    {"person_id": 13, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "县处级", "note": ""},
    # 郭峰
    {"person_id": 14, "org_id": 3, "title": "区人大常委会主任", "start_date": "", "end_date": "present", "rank": "县处级", "note": ""},
    # 张正濠（前任书记）
    {"person_id": 15, "org_id": 1, "title": "区委书记（前任）", "start_date": "2017", "end_date": "2023-04", "rank": "县处级", "note": "在龙亭区工作近六年；兼开封市政协副主席"},
    {"person_id": 15, "org_id": 11, "title": "市政协副主席（兼）", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "卸任区委书记后仍任市政协党组成员、副主席"},
    # 张海 / 闫泊含（前任副区长）
    {"person_id": 16, "org_id": 2, "title": "常务副区长（前任）", "start_date": "", "end_date": "2023", "rank": "县处级", "note": "2023 年在任"},
    {"person_id": 17, "org_id": 2, "title": "副区长（前任）", "start_date": "", "end_date": "2023", "rank": "县处级", "note": "2023 年在任"},
]

# ── 关系 ─────────────────────────────────────────────────────────────
relationships = [
    # 党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "党政同僚", "context": "李涛（区委书记）与陈嘉慧（区长）党政正职搭档", "overlap_org": "中共开封市龙亭区委员会", "overlap_period": "2023-09 至今"},
    # 前任继任
    {"person_a": 1, "person_b": 15, "type": "前任继任", "context": "李涛接替张正濠任龙亭区委书记", "overlap_org": "中共开封市龙亭区委员会", "overlap_period": "2023-04 交接"},
    {"person_a": 2, "person_b": 1, "type": "前任继任", "context": "陈嘉慧接任区长（李涛此前任区长后转任书记）", "overlap_org": "开封市龙亭区人民政府", "overlap_period": "2023-09 交接"},
    # 书记—副书记
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "李涛与郑华腾（区委副书记）", "overlap_org": "中共开封市龙亭区委员会", "overlap_period": "2026-06 至今"},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "李涛与刘国歌（区委常委、常务副区长）", "overlap_org": "中共开封市龙亭区委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "李涛与李希峰（区委常委）", "overlap_org": "中共开封市龙亭区委员会", "overlap_period": "2026-06 至今"},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "李涛与张永刚（区委常委、宣传部长）", "overlap_org": "中共开封市龙亭区委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "李涛与刘龙飞（区委常委）", "overlap_org": "中共开封市龙亭区委员会", "overlap_period": "2026-06 至今"},
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "李涛与阮志鹏（区委常委）", "overlap_org": "中共开封市龙亭区委员会", "overlap_period": "2026-06 至今"},
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "李涛与张波（区委常委）", "overlap_org": "中共开封市龙亭区委员会", "overlap_period": "2026-06 至今"},
    {"person_a": 1, "person_b": 10, "type": "上下级", "context": "李涛与王硕（区委常委）", "overlap_org": "中共开封市龙亭区委员会", "overlap_period": "2026-06 至今"},
    {"person_a": 1, "person_b": 11, "type": "上下级", "context": "李涛与孙文超（区委常委）", "overlap_org": "中共开封市龙亭区委员会", "overlap_period": "2026-06 至今"},
    # 政府班子
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "陈嘉慧（区长）与刘国歌（常务副区长）", "overlap_org": "开封市龙亭区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "陈嘉慧（区长）与张永刚（副区长）", "overlap_org": "开封市龙亭区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "陈嘉慧（区长）与刘卫华（副区长）", "overlap_org": "开封市龙亭区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 13, "type": "上下级", "context": "陈嘉慧（区长）与王风来（副区长）", "overlap_org": "开封市龙亭区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 16, "type": "前任继任", "context": "刘国歌接任常务副区长（张海此前任）", "overlap_org": "开封市龙亭区人民政府", "overlap_period": "2024 前后"},
    # 市—区关联
    {"person_a": 15, "person_b": 9, "type": "任职关联", "context": "张正濠兼任开封市政协副主席，与市委、市政府有协调关系", "overlap_org": "政协开封市委员会", "overlap_period": ""},
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
    print(f"完成！DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print(f"人数: {len(persons)} | 组织数: {len(organizations)} | 任职数: {len(positions)} | 关系数: {len(relationships)}")