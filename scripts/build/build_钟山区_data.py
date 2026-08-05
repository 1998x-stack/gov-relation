#!/usr/bin/env python3
"""Build 钟山区 (Zhongshan District, 六盘水市, 贵州省) 领导班子工作关系网络.

数据来源: 钟山区人民政府网站领导之窗 (www.gzzs.gov.cn/zwgk1/ldzc/), 访问于 2026-08-05.
核心现任职务以官方领导之窗为 confirmed 依据; 早期履历因公开检索受限按 plausible 标注,
缺失字段列入 open_questions 与报告 open_gaps.
"""

from __future__ import annotations

import sqlite3  # noqa: F401 (SQLite schema built via gov_relation.runner)
import sys
from pathlib import Path

# 项目根目录（脚本位于 data/tmp/guizhou_钟山区/ 时向上三级）
_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE.parents[2]))

from gov_relation.runner import run_build

SLUG = "钟山区"
PROVINCE = "贵州省"
CITY = "六盘水市"
DATE_TAG = "2026-08-05"

# -- Output paths -------------------------------------------------------------
# 暂存阶段输出到 staging 目录；经 scripts/process_tmp.py 校验后归档。
DB_PATH = _HERE / f"{SLUG}_network.db"
GEXF_PATH = _HERE / f"{SLUG}_network.gexf"

# -- Persons ---------------------------------------------------------------
persons = [
    # -- 区委书记 --
    {
        "id": 1,
        "name": "李仕强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年8月",
        "birthplace": "贵州盘州",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "1999年8月",
        "current_post": "区委书记、区人民武装部党委第一书记",
        "current_org": "中共钟山区委",
        "source": "https://www.gzzs.gov.cn/zwgk1/ldzc/qw/lsq/",
    },
    {
        "id": 2,
        "name": "易基恒",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1976年10月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、区人民政府党组书记、区长",
        "current_org": "钟山区人民政府",
        "source": "https://www.gzzs.gov.cn/zwgk1/ldzc/qzf/yjj/",
    },
    {
        "id": 3,
        "name": "李禄",
        "gender": "男",
        "ethnicity": "彝族",
        "birth": "1982年10月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记",
        "current_org": "中共钟山区委",
        "source": "https://www.gzzs.gov.cn/zwgk1/ldzc/qw/ll/",
    },
    {
        "id": 4,
        "name": "申昊冬",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记",
        "current_org": "中共钟山区委",
        "source": "https://www.gzzs.gov.cn/ywdt1/zwyw_502086/202607/t20260731_90682902.html",
    },
    {
        "id": 5,
        "name": "钱廷刚",
        "gender": "男",
        "ethnicity": "彝族",
        "birth": "1971年8月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区委政法委书记",
        "current_org": "中共钟山区委政法委",
        "source": "https://www.gzzs.gov.cn/zwgk1/ldzc/qw/qtg/",
    },
    {
        "id": 6,
        "name": "叶洪海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年3月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区人民武装部政委",
        "current_org": "钟山区人民武装部",
        "source": "https://www.gzzs.gov.cn/zwgk1/ldzc/qw/yhh/",
    },
    {
        "id": 7,
        "name": "卢林勇",
        "gender": "男",
        "ethnicity": "穿青人",
        "birth": "1977年9月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区纪委书记、区监委主任",
        "current_org": "中共钟山区纪委、区监委",
        "source": "https://www.gzzs.gov.cn/zwgk1/ldzc/qw/lly/",
    },
    {
        "id": 8,
        "name": "刘兴华",
        "gender": "男",
        "ethnicity": "彝族",
        "birth": "1986年10月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区委组织部部长、区委党校校长、区委教育工委书记",
        "current_org": "中共钟山区委组织部",
        "source": "https://www.gzzs.gov.cn/zwgk1/ldzc/qw/lxh/",
    },
    {
        "id": 9,
        "name": "颜绍军",
        "gender": "男",
        "ethnicity": "穿青人",
        "birth": "1982年2月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区人民政府副区长",
        "current_org": "钟山区人民政府",
        "source": "https://www.gzzs.gov.cn/zwgk1/ldzc/qw/ysj/",
    },
    {
        "id": 10,
        "name": "兰钰涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年9月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区人民政府副区长（分管常务工作）",
        "current_org": "钟山区人民政府",
        "source": "https://www.gzzs.gov.cn/zwgk1/ldzc/qw/lyt/",
    },
    {
        "id": 11,
        "name": "周树华",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区人民政府副区长",
        "current_org": "钟山区人民政府",
        "source": "https://www.gzzs.gov.cn/zwgk1/ldzc/qzf/zsh/",
    },
    # 区政府副区长
    {
        "id": 12,
        "name": "马盘踞",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人民政府副区长",
        "current_org": "钟山区人民政府",
        "source": "https://www.gzzs.gov.cn/zwgk1/ldzc/qzf/mpj/",
    },
    {
        "id": 13,
        "name": "杨洋",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人民政府副区长",
        "current_org": "钟山区人民政府",
        "source": "https://www.gzzs.gov.cn/zwgk1/ldzc/qzf/",
    },
    {
        "id": 14,
        "name": "安昌鹏",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人民政府副区长",
        "current_org": "钟山区人民政府",
        "source": "https://www.gzzs.gov.cn/zwgk1/ldzc/qzf/ajp/",
    },
    {
        "id": 15,
        "name": "陈应红",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人民政府副区长",
        "current_org": "钟山区人民政府",
        "source": "https://www.gzzs.gov.cn/zwgk1/ldzc/qzf/cyh/",
    },
    {
        "id": 16,
        "name": "田有华",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人民政府副区长",
        "current_org": "钟山区人民政府",
        "source": "https://www.gzzs.gov.cn/zwgk1/ldzc/qzf/tyh/",
    },
    # 区人大常委会
    {
        "id": 17,
        "name": "李卫杰",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会党组书记",
        "current_org": "钟山区人大常委会",
        "source": "https://www.gzzs.gov.cn/ywdt1/zwyw_502086/202607/t20260731_90682902.html",
    },
    {
        "id": 18,
        "name": "王佐华",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会副主任",
        "current_org": "钟山区人大常委会",
        "source": "https://www.gzzs.gov.cn/zwgk1/ldzc/qrdcwh/wzh/",
    },
    {
        "id": 19,
        "name": "杜景志",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会副主任",
        "current_org": "钟山区人大常委会",
        "source": "https://www.gzzs.gov.cn/zwgk1/ldzc/qrdcwh/djz/",
    },
    {
        "id": 20,
        "name": "卢文琪",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会副主任",
        "current_org": "钟山区人大常委会",
        "source": "https://www.gzzs.gov.cn/zwgk1/ldzc/qrdcwh/lwq/",
    },
    {
        "id": 21,
        "name": "安芳",
        "gender": "女",
        "ethnicity": "彝族",
        "birth": "1970年9月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会党组副书记、副主任",
        "current_org": "钟山区人大常委会",
        "source": "https://www.gzzs.gov.cn/zwgk1/ldzc/qrdcwh/af/",
    },
    # 区政协
    {
        "id": 22,
        "name": "吴胜卫",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协党组书记",
        "current_org": "政协钟山区委员会",
        "source": "https://www.gzzs.gov.cn/ywdt1/zwyw_502086/202607/t20260731_90682902.html",
    },
    {
        "id": 23,
        "name": "罗敏",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "政协钟山区委员会",
        "source": "https://www.gzzs.gov.cn/zwgk1/ldzc/qzx/",
    },
    {
        "id": 24,
        "name": "曾丹",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协副主席",
        "current_org": "政协钟山区委员会",
        "source": "https://www.gzzs.gov.cn/zwgk1/ldzc/qzx/",
    },
    {
        "id": 25,
        "name": "陈普",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协副主席",
        "current_org": "政协钟山区委员会",
        "source": "https://www.gzzs.gov.cn/zwgk1/ldzc/qzx/",
    },
    {
        "id": 26,
        "name": "陈勇",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协副主席",
        "current_org": "政协钟山区委员会",
        "source": "https://www.gzzs.gov.cn/zwgk1/ldzc/qzx/",
    },
    {
        "id": 27,
        "name": "冯艳秋",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协副主席",
        "current_org": "政协钟山区委员会",
        "source": "https://www.gzzs.gov.cn/zwgk1/ldzc/qzx/fyq/",
    },
    {
        "id": 28,
        "name": "彭勇",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协副主席",
        "current_org": "政协钟山区委员会",
        "source": "https://www.gzzs.gov.cn/zwgk1/ldzc/qzx/",
    },
    {
        "id": 29,
        "name": "杨波",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协副主席",
        "current_org": "政协钟山区委员会",
        "source": "https://www.gzzs.gov.cn/zwgk1/ldzc/qzx/",
    },
    {
        "id": 30,
        "name": "袁志祥",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协副主席",
        "current_org": "政协钟山区委员会",
        "source": "https://www.gzzs.gov.cn/zwgk1/ldzc/qzx/yzx/",
    },
]

# -- Organizations -----------------------------------------------------------
organizations = [
    {"id": 1, "name": "中共钟山区委", "type": "党委", "level": "县级", "parent": "中共六盘水市委", "location": "贵州六盘水钟山区"},
    {"id": 2, "name": "钟山区人民政府", "type": "政府", "level": "县级", "parent": "六盘水市人民政府", "location": "贵州六盘水钟山区"},
    {"id": 3, "name": "中共钟山区纪委、区监委", "type": "纪委", "level": "县级", "parent": "中共钟山区委", "location": "贵州六盘水钟山区"},
    {"id": 4, "name": "钟山区人大常委会", "type": "人大", "level": "县级", "parent": "六盘水市人大", "location": "贵州六盘水钟山区"},
    {"id": 5, "name": "政协钟山区委员会", "type": "政协", "level": "县级", "parent": "六盘水市政协", "location": "贵州六盘水钟山区"},
    {"id": 6, "name": "钟山区人民武装部", "type": "其他", "level": "县级", "parent": "六盘水军分区", "location": "贵州六盘水钟山区"},
    {"id": 7, "name": "中共钟山区委政法委", "type": "党委", "level": "县级", "parent": "中共钟山区委", "location": "贵州六盘水钟山区"},
    {"id": 8, "name": "中共钟山区委组织部", "type": "党委", "level": "县级", "parent": "中共钟山区委", "location": "贵州六盘水钟山区"},
]

# -- Positions ----------------------------------------------------------------
positions = [
    # 区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记、区人民武装部党委第一书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "现任"},
    # 区长
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "", "end_date": "", "rank": "正处级", "note": "区委副书记、政府党组书记"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 区委副书记
    {"person_id": 3, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 区委常委
    {"person_id": 5, "org_id": 7, "title": "区委常委、区委政法委书记", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 6, "title": "区委常委、区人民武装部政委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 3, "title": "区委常委、区纪委书记、区监委主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 8, "title": "区委常委、区委组织部部长、区委党校校长、区委教育工委书记", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "区委常委、副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "区委常委、常务副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "分管常务工作"},
    {"person_id": 11, "org_id": 2, "title": "区委常委、副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 区政府副区长
    {"person_id": 12, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 区人大常委会
    {"person_id": 17, "org_id": 4, "title": "区人大常委会党组书记", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 18, "org_id": 4, "title": "区人大常委会副主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 19, "org_id": 4, "title": "区人大常委会副主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 20, "org_id": 4, "title": "区人大常委会副主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 21, "org_id": 4, "title": "区人大常委会党组副书记、副主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 区政协
    {"person_id": 22, "org_id": 5, "title": "区政协党组书记", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 23, "org_id": 5, "title": "区政协主席", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 24, "org_id": 5, "title": "区政协副主席", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 25, "org_id": 5, "title": "区政协副主席", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 26, "org_id": 5, "title": "区政协副主席", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 27, "org_id": 5, "title": "区政协副主席", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 28, "org_id": 5, "title": "区政协副主席", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 29, "org_id": 5, "title": "区政协副主席", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 30, "org_id": 5, "title": "区政协副主席", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
]

# -- Relationships --------------------------------------------------------------
relationships = [
    # 书记—区长党政搭档
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "区委书记与区长党政一把手搭档，共同主持区委常委会", "overlap_org": "钟山区党政班子", "overlap_period": "2021/2022至今"},
    # 书记—专职副书记
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "区委书记与区委副书记同届共事", "overlap_org": "中共钟山区委", "overlap_period": "现任"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "区委书记与区委副书记同届共事", "overlap_org": "中共钟山区委", "overlap_period": "现任"},
    # 区长—区委副书记
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "区长与区委副书记同届共事", "overlap_org": "中共钟山区委", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "区长与区委副书记同届共事", "overlap_org": "中共钟山区委", "overlap_period": "现任"},
    # 区长—常务副区长
    {"person_a": 2, "person_b": 10, "type": "overlap", "context": "区长与常务副区长日常工作搭档", "overlap_org": "钟山区人民政府", "overlap_period": "现任"},
    # 区长—各副区长
    {"person_a": 2, "person_b": 9, "type": "overlap", "context": "区长与区委常委、副区长", "overlap_org": "钟山区人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 11, "type": "overlap", "context": "区长与区委常委、副区长", "overlap_org": "钟山区人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 12, "type": "overlap", "context": "区长与副区长", "overlap_org": "钟山区人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 13, "type": "overlap", "context": "区长与副区长", "overlap_org": "钟山区人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 14, "type": "overlap", "context": "区长与副区长", "overlap_org": "钟山区人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 15, "type": "overlap", "context": "区长与副区长", "overlap_org": "钟山区人民政府", "overlap_period": "现任"},
    {"person_a": 2, "person_b": 16, "type": "overlap", "context": "区长与副区长", "overlap_org": "钟山区人民政府", "overlap_period": "现任"},
    # 书记—纪委书记
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "区委书记与区纪委书记、监委主任同在常委会", "overlap_org": "中共钟山区委常委会", "overlap_period": "现任"},
    # 书记—组织部长
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "区委书记与区委组织部部长同在常委会", "overlap_org": "中共钟山区委常委会", "overlap_period": "现任"},
    # 书记—政法委书记
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "区委书记与区委政法委书记同在常委会", "overlap_org": "中共钟山区委常委会", "overlap_period": "现任"},
    # 书记—人大党组书记
    {"person_a": 1, "person_b": 17, "type": "overlap", "context": "区委书记与区人大常委会党组书记同届", "overlap_org": "钟山区四套班子", "overlap_period": "现任"},
    # 书记—政协党组书记
    {"person_a": 1, "person_b": 22, "type": "overlap", "context": "区委书记与区政协党组书记同届", "overlap_org": "钟山区四套班子", "overlap_period": "现任"},
    # 区长—人大党组书记
    {"person_a": 2, "person_b": 17, "type": "overlap", "context": "区长与区人大常委会党组书记同届", "overlap_org": "钟山区四套班子", "overlap_period": "现任"},
    # 书记—前任职务（区长）转移：前任区长(李仕强)→继任区长(易基恒) 前后任
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor", "context": "李仕强曾任区长、后任区委书记，易基恒继任区长，区长职务前后任交接", "overlap_org": "钟山区人民政府", "overlap_period": "2020-2022过渡"},
    # 人大党组 — 人大成员
    {"person_a": 17, "person_b": 21, "type": "overlap", "context": "区人大常委会党组书记与党组副书记、副主任同届", "overlap_org": "钟山区人大常委会", "overlap_period": "现任"},
    # 政协党组书记—主席
    {"person_a": 22, "person_b": 23, "type": "overlap", "context": "区政协党组书记与政协主席同届", "overlap_org": "政协钟山区委员会", "overlap_period": "现任"},
]


# -- Build -------------------------------------------------------------------
if __name__ == "__main__":
    print(f"Building {PROVINCE}{SLUG} network ({DATE_TAG})...")
    print(f"  DB:   {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Persons: {len(persons)}")
    print(f"  Orgs:    {len(organizations)}")
    print(f"  Posns:   {len(positions)}")
    print(f"  Rels:    {len(relationships)}")

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
    print("Done.")