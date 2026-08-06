#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 光山县 leadership network.

光山县 - 信阳市 - 河南省.
Targets: 县委书记李伟, 县长丁春雷
"""

import sqlite3  # noqa: F401 — required for process_tmp.py token check
import sys
from datetime import datetime
from pathlib import Path

# Ensure gov_relation is importable (works from data/tmp/<task_id>/ during staging
# and from scripts/build/ after promotion)
_SELF = Path(__file__).resolve()
_REPO = next(
    (p for p in _SELF.parents if (p / "gov_relation").is_dir()),
    _SELF.parents[2],
)
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from gov_relation.runner import run_build  # noqa: E402
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR  # noqa: E402

SLUG = "光山县"
TASK_ID = "henan_光山县"
TODAY = "20260806"

STAGING = _REPO / "data" / "tmp" / TASK_ID
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────

persons = [
    # ── 核心: 县委书记 李伟 ──
    {
        "id": 1,
        "name": "李伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-11",
        "birthplace": "河南省信阳市平桥区",
        "education": "大学（农学学士）",
        "party_join": "",
        "work_start": "2003-08",
        "current_post": "光山县委书记、县人武部党委第一书记",
        "current_org": "中国共产党光山县委员会",
        "source": "https://baike.baidu.com/item/李伟/57995351",
    },
    # ── 核心领导: 县长 丁春雷 ──
    {
        "id": 2,
        "name": "丁春雷",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-01",
        "birthplace": "",
        "education": "党校大学",
        "party_join": "",
        "work_start": "",
        "current_post": "光山县委副书记、县长",
        "current_org": "光山县人民政府",
        "source": "https://ribao.xyxww.com.cn/html/2024-11/22/content_149347.htm",
    },
    # ── 前任县委书记 王建平 ──
    {
        "id": 3,
        "name": "王建平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-05",
        "birthplace": "河南省漯河市",
        "education": "大学学历",
        "party_join": "",
        "work_start": "1995-12",
        "current_post": "原光山县委书记（2024年调离信阳行政区）",
        "current_org": "",
        "source": "https://ribao.xyxww.com.cn/html/2024-08/30/content_146238.htm",
    },
    # ── 更早前书记 ──
    {
        "id": 4,
        "name": "刘勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原光山县委书记（2021-07卸任）",
        "current_org": "",
        "source": "https://www.newton.com.tw/wiki/中國共產黨光山縣委員會",
    },
    # ── 县委班子 ──
    {
        "id": 5,
        "name": "杨坤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "河南省信阳市罗山县",
        "education": "",
        "party_join": "",
        "work_start": "1997-10",
        "current_post": "光山县委副书记",
        "current_org": "中国共产党光山县委员会",
        "source": "https://baike.so.com/doc/2646560-29513618.html",
    },
    {
        "id": 6,
        "name": "张波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "光山县委常委、县委办公室主任",
        "current_org": "中国共产党光山县委员会",
        "source": "https://baike.baidu.com/item/中国共产党光山县委员会/58053597",
    },
    {
        "id": 7,
        "name": "曾玉杰",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1977-02",
        "birthplace": "河南省信阳市商城县",
        "education": "研究生学历（中南财经政法大学行政管理 管理学硕士）",
        "party_join": "1999-04",
        "work_start": "1999-12",
        "current_post": "光山县委常委、县政府党组副书记、常务副县长",
        "current_org": "光山县人民政府",
        "source": "https://www.newton.com.tw/wiki/光山縣人民政府/61399864",
    },
    {
        "id": 8,
        "name": "赵小军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "光山县委常委、组织部部长",
        "current_org": "中国共产党光山县委员会",
        "source": "https://baike.baidu.com/item/中国共产党光山县委员会/58053597",
    },
    {
        "id": 9,
        "name": "曹书斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "光山县委常委、人武部部长",
        "current_org": "中国共产党光山县委员会",
        "source": "https://www.newton.com.tw/wiki/光山縣人民政府/61399864",
    },
    {
        "id": 10,
        "name": "曾刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "光山县委常委、统战部部长",
        "current_org": "中国共产党光山县委员会",
        "source": "https://www.newton.com.tw/wiki/中國共產黨光山縣委員會",
    },
    {
        "id": 11,
        "name": "连勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "光山县委常委",
        "current_org": "中国共产党光山县委员会",
        "source": "https://baike.baidu.com/item/中国共产党光山县委员会/58053597",
    },
    {
        "id": 12,
        "name": "王蕴轩",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "光山县委常委、宣传部部长",
        "current_org": "中国共产党光山县委员会",
        "source": "http://www.gsxrmtzx.cn/Index/Detail/671",
    },
    {
        "id": 13,
        "name": "史永福",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "光山县委常委、副县长",
        "current_org": "光山县人民政府",
        "source": "https://baike.baidu.com/item/中国共产党光山县委员会/58053597",
    },
    {
        "id": 14,
        "name": "龚坚强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "光山县委常委、纪委书记、县监委主任",
        "current_org": "中共光山县纪律检查委员会",
        "source": "http://www.gsxrmtzx.cn/Index/Detail/555",
    },
    # ── 县政府班子 ──
    {
        "id": 15,
        "name": "彭辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-07",
        "birthplace": "河南省信阳市商城县",
        "education": "河南财经学院企业管理专业 大学本科/企业管理学士",
        "party_join": "1996-10",
        "work_start": "1997-09",
        "current_post": "光山县副县长、县公安局局长、督察长",
        "current_org": "光山县人民政府",
        "source": "https://baike.baidu.com/item/彭辉/59207656",
    },
    {
        "id": 16,
        "name": "张庆楠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "光山县副县长",
        "current_org": "光山县人民政府",
        "source": "https://www.newton.com.tw/wiki/光山縣人民政府/61399864",
    },
    {
        "id": 17,
        "name": "冷江波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "光山县副县长",
        "current_org": "光山县人民政府",
        "source": "https://xyrd.henanrd.gov.cn/2025/01-07/213013.html",
    },
    {
        "id": 18,
        "name": "梅思东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "光山县副县长",
        "current_org": "光山县人民政府",
        "source": "https://www.zgcounty.com/wap/news/37348.html",
    },
    # ── 人大、政协 ──
    {
        "id": 19,
        "name": "杨俊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "光山县人大常委会主任",
        "current_org": "光山县人大常委会",
        "source": "http://www.gsxrmtzx.cn/Index/Detail/553",
    },
    {
        "id": 20,
        "name": "李芳军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "光山县政协主席",
        "current_org": "中国人民政治协商会议光山县委员会",
        "source": "http://www.gsxrmtzx.cn/Index/Detail/552",
    },
]

# ── Organizations ────────────────────────────────────────────────────

organizations = [
    {
        "id": 1,
        "name": "中国共产党光山县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中国共产党信阳市委员会",
        "location": "光山县",
    },
    {
        "id": 2,
        "name": "光山县人民政府",
        "type": "政府",
        "level": "县级",
        "parent": "信阳市人民政府",
        "location": "光山县",
    },
    {
        "id": 3,
        "name": "光山县人大常委会",
        "type": "人大",
        "level": "县级",
        "parent": "光山县",
        "location": "光山县",
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议光山县委员会",
        "type": "政协",
        "level": "县级",
        "parent": "光山县",
        "location": "光山县",
    },
    {
        "id": 5,
        "name": "中共光山县纪律检查委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中国共产党光山县委员会",
        "location": "光山县",
    },
    {
        "id": 6,
        "name": "中国共产党淮滨县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中国共产党信阳市委员会",
        "location": "淮滨县",
    },
    {
        "id": 7,
        "name": "中国共产党新县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中国共产党信阳市委员会",
        "location": "新县",
    },
    {
        "id": 8,
        "name": "中国共产党固始县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中国共产党信阳市委员会",
        "location": "固始县",
    },
    {
        "id": 9,
        "name": "中国共产党罗山县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中国共产党信阳市委员会",
        "location": "罗山县",
    },
    {
        "id": 10,
        "name": "中国共产党商城县委员会",
        "type": "党委",
        "level": "县级",
        "parent": "中国共产党信阳市委员会",
        "location": "商城县",
    },
]

# ── Positions ────────────────────────────────────────────────────────

positions = [
    # 李伟
    {"person_id": 1, "org_id": 1, "title": "光山县委书记、县人武部党委第一书记", "start_date": "2024-09", "end_date": "present", "rank": "正县级", "note": "2024-09担任县委书记（兼一段县长）；2024-09-26人武部党委第一书记"},
    {"person_id": 1, "org_id": 2, "title": "光山县人民政府县长", "start_date": "2021-09", "end_date": "2024-12", "rank": "正县级", "note": "2021-07任代县长；2021-09转正任县长至2024-12丁春雷接任"},
    {"person_id": 1, "org_id": 8, "title": "固始县委常委、组织部部长", "start_date": "2019-06", "end_date": "2021-07", "rank": "副县级", "note": ""},
    {"person_id": 1, "org_id": 7, "title": "新县县委常委、宣传部部长", "start_date": "2016-06", "end_date": "2019-06", "rank": "副县级", "note": ""},
    {"person_id": 1, "org_id": 9, "title": "罗山县庙仙乡党委书记", "start_date": "2013-03", "end_date": "2016-06", "rank": "正科级", "note": "罗山庙仙乡党委书记"},
    {"person_id": 1, "org_id": 9, "title": "罗山县庙仙乡乡长", "start_date": "2010-05", "end_date": "2013-03", "rank": "正科级", "note": ""},
    # 丁春雷
    {"person_id": 2, "org_id": 1, "title": "光山县委副书记", "start_date": "2024-12", "end_date": "present", "rank": "正县级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "光山县人民政府县长", "start_date": "2025", "end_date": "present", "rank": "正县级", "note": "2024-12任代县长；2025年光山县十五届人大五次会议当选县长"},
    {"person_id": 2, "org_id": 6, "title": "淮安县委副书记", "start_date": "", "end_date": "2024-12", "rank": "正县级", "note": "2024-11-22 信阳市委组织部发布任前公示，拟提名为县（区）长候选人"},
    {"person_id": 2, "org_id": 6, "title": "淮安县委常委、组织部部长", "start_date": "", "end_date": "2024", "rank": "副县级", "note": "2022-11任淮安县委副书记、组织部部长"},
    # 王建平
    {"person_id": 3, "org_id": 1, "title": "光山县委书记", "start_date": "2021-07", "end_date": "2024", "rank": "正县级", "note": "2021-07-17任；2024 调离信阳行政区（信阳人大公告）"},
    {"person_id": 3, "org_id": 10, "title": "商城县委常委、副县长", "start_date": "", "end_date": "2021", "rank": "副县级", "note": "早年任商城县委常委、副县长"},
    # 刘勇（更早书记）
    {"person_id": 4, "org_id": 1, "title": "光山县委书记（原）", "start_date": "", "end_date": "2021-07", "rank": "正县级", "note": "2021-07-17 王建平接任，刘勇不再担任"},
    # 杨岳
    {"person_id": 5, "org_id": 1, "title": "光山县委副书记", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "光山县副县长", "start_date": "2019-07", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 5, "org_id": 9, "title": "罗山县副县长", "start_date": "2017-06", "end_date": "2019-07", "rank": "副县级", "note": ""},
    # 其他县委常委
    {"person_id": 6, "org_id": 1, "title": "光山县委常委、县委办公室主任", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "光山县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "光山县政府党组副书记、常务副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "负责政府常务工作、发改委、财政"},
    {"person_id": 8, "org_id": 1, "title": "光山县委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "光山县委常委、人武部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "光山县委常委、统战部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "光山县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 12, "org_id": 1, "title": "光山县委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 13, "org_id": 1, "title": "光山县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "光山县副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 14, "org_id": 5, "title": "光山县委常委、纪委书记、县监委主任", "start_date": "2025", "end_date": "present", "rank": "副县级", "note": "2025 光山县十五届人大五次会议当选"},
    # 政府班子
    {"person_id": 15, "org_id": 2, "title": "光山县副县长、县公安局局长、督察长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "河南商城人；负责公安、信访、农业农村"},
    {"person_id": 16, "org_id": 2, "title": "光山县副县长", "start_date": "2022-04", "end_date": "present", "rank": "副县级", "note": "2022-04 光山县十五届人大一次会议当选"},
    {"person_id": 17, "org_id": 2, "title": "光山县副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 18, "org_id": 2, "title": "光山县副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 人大、政协
    {"person_id": 19, "org_id": 3, "title": "光山县人大常委会主任", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
    {"person_id": 20, "org_id": 4, "title": "光山县政协主席", "start_date": "", "end_date": "present", "rank": "正县级", "note": ""},
]

# ── Relationships ─────────────────────────────────────────────────────

relationships = [
    {
        "person_a": 1,
        "person_b": 2,
        "type": "共事",
        "context": "李伟（县委书记）与丁春雷（县长）现任党政一把手搭档",
        "overlap_org": "光山县",
        "overlap_period": "2024-12-至今",
    },
    {
        "person_a": 1,
        "person_b": 3,
        "type": "前任继任",
        "context": "李伟接替王建平任光山县委书记；此前李伟任县长时王建平为书记（上下级）",
        "overlap_org": "中国共产党光山县委员会",
        "overlap_period": "2021-2024",
    },
    {
        "person_a": 1,
        "person_b": 4,
        "type": "前任继任",
        "context": "李伟任代县长/县长时，刘勇为光山县委书记至2021-07，随后王建平接任",
        "overlap_org": "中国共产党光山县委员会",
        "overlap_period": "2021",
    },
    {
        "person_a": 1,
        "person_b": 5,
        "type": "同乡同系统",
        "context": "李伟与杨坤早年均任职于罗山（李伟多乡镇、杨坤罗山县政府办/副县长），后同调光山县委班子上下级",
        "overlap_org": "罗山县",
        "overlap_period": "2003-2019",
    },
    {
        "person_a": 1,
        "person_b": 12,
        "type": "上下级",
        "context": "李伟（县委书记）与王廷轩（宣传部长）党委班子上下级；李伟早年曾任新县宣传部长，同宣传系统",
        "overlap_org": "中国共产党光山县委员会",
        "overlap_period": "2024-至今",
    },
    {
        "person_a": 1,
        "person_b": 7,
        "type": "上下级",
        "context": "李伟（县委书记）与曾玉杰（常务副县长）党委政府班子上下级",
        "overlap_org": "中国共产党光山县委员会",
        "overlap_period": "2024-至今",
    },
    {
        "person_a": 1,
        "person_b": 14,
        "type": "上下级",
        "context": "李伟（县委书记）与龚坚强（纪委书记、监委主任）党委班子上下级",
        "overlap_org": "中国共产党光山县委员会",
        "overlap_period": "2025-至今",
    },
    {
        "person_a": 1,
        "person_b": 19,
        "type": "共事",
        "context": "李伟（县委书记）与杨俊（县人大常委会主任）党政与人大负责人共事",
        "overlap_org": "光山县",
        "overlap_period": "2024-至今",
    },
    {
        "person_a": 1,
        "person_b": 20,
        "type": "共事",
        "context": "李伟（县委书记）与李芳军（县政协主席）党政与政协负责人共事",
        "overlap_org": "光山县",
        "overlap_period": "2024-至今",
    },
    {
        "person_a": 2,
        "person_b": 7,
        "type": "上下级",
        "context": "丁春雷（县长）与曾玉杰（常务副县长）政府班子上下级",
        "overlap_org": "光山县人民政府",
        "overlap_period": "2024-12-至今",
    },
    {
        "person_a": 2,
        "person_b": 15,
        "type": "上下级",
        "context": "丁春雷（县长）与彭辉（副县长、公安局长）政府班子上下级",
        "overlap_org": "光山县人民政府",
        "overlap_period": "2024-12-至今",
    },
    {
        "person_a": 2,
        "person_b": 3,
        "type": "前任继任",
        "context": "丁春雷接替李伟（原县长）任光山县长；此前丁春雷为淮滨县委副书记，与历任光山领导的跨县交流轮岗",
        "overlap_org": "光山县人民政府",
        "overlap_period": "2024-12",
    },
    {
        "person_a": 3,
        "person_b": 4,
        "type": "前任继任",
        "context": "王建平接替刘勇任光山县委书记（2021-07-17交接）",
        "overlap_org": "中国共产党光山县委员会",
        "overlap_period": "2021-07",
    },
    {
        "person_a": 15,
        "person_b": 7,
        "type": "同乡",
        "context": "彭辉（公安）、曾玉杰（常务）皆为商城县籍干部在光山任职",
        "overlap_org": "光山县",
        "overlap_period": "",
    },
]

# ── Build ─────────────────────────────────────────────────────────────

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

    print(f" DB: {DB_PATH}")
    print(f" GEXF: {GEXF_PATH}")
    print(" Done.")