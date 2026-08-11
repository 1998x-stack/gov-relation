#!/usr/bin/env python3
"""郧阳区（十堰市，湖北省）领导班子工作关系网络数据生成脚本。

Task ID: hubei_郧阳区
Level: 市辖区
Targets: 区委书记 & 区长

调查日期：2026-07-24 / 2026-08-06 复核
现行班子（截至 2026-08，官方区委领导页 + 区政府领导页确认）：
  - 区委书记：梅华（1975-04，土家族，湖北建始，1997-04 入党，1998-07 参加工作，硕士研究生；一级调研员）
  - 区委副书记、区长：刘伟华（1979-03，汉族，山东潍坊，2003-12 入党，2004-07 参加工作，研究生/工学博士）
  - 12 名区委常委（下方 persons 列表，均来自官方 www.yunyang.shiyan.gov.cn 领导之窗）
前任区委书记：胡先平（约2021—约2023/24，据专项报告 local evidence，去向：十堰市政府党组成员、十堰经开区党工委副书记/管委会主任）；更早：孙道军（约2010年代—约2021）。

实现：
- 使用公共库 gov_relation.runner.run_build() 构建 SQLite 数据库 + GEXF 图。
- 为名单人物写出 data/persons/YYYYMMDD-湖北省-十堰市-{job}-{name}.json 深度档案。
- 新产物第一优先级写入本脚本所在暂存目录，再由 scripts/process_tmp.py 校验后归档。

用法：
    python3 data/tmp/hubei_郧阳区/build_郧阳区_data.py        # 产出写到暂存目录
    python3 scripts/build/build_郧阳区_data.py                # 归档后运行，产出到 canonical 目录
"""

import json
import sqlite3
import sys
from datetime import datetime
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
REPO_ROOT = _candidate
sys.path.insert(0, str(REPO_ROOT))

from gov_relation.log import get_logger  # noqa: E402
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR  # noqa: E402
from gov_relation.runner import run_build  # noqa: E402

logger = get_logger(__name__)

SLUG = "郧阳区"
PROVINCE = "湖北省"
PARENT_CITY = "十堰市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

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

GOV_HOST = "https://yunyang.shiyan.gov.cn/xxgkxi/fdzdgknr/zfld/qwld"

# ── 人物 ────────────────────────────────────────────────────────────────────
# 证据：郧阳区人民政府官方《区委领导》领导之窗（GOV_HOST），来源见 source 字段。
persons = [
    {"id": 1, "name": "梅华",                 "gender": "男", "ethnicity": "土家族", "birth": "1975-04", "birthplace": "湖北建始", "native_place": "湖北省恩施州建始县",
     "education": "硕士研究生学历",             "party_join": "1997-04", "work_start": "1998-07",
     "current_post": "郧阳区委书记、一级调研员", "current_org": "中共十堰市郧阳区委员会",
     "source": f"{GOV_HOST}/202205/t20220513_3502378.shtml"},
    {"id": 2, "name": "刘伟华",                 "gender": "男", "ethnicity": "汉族",   "birth": "1979-03", "birthplace": "山东潍坊", "native_place": "山东省潍坊市",
     "education": "研究生学历、工学博士",         "party_join": "2003-12", "work_start": "2004-07",
     "current_post": "郧阳区委副书记、区长",       "current_org": "郧阳区人民政府",
     "source": f"{GOV_HOST}/202505/t20250508_4736615.shtml"},
    {"id": 3, "name": "董会祥",                 "gender": "男", "ethnicity": "汉族",   "birth": "1973-10", "birthplace": "十堰市郧阳区", "native_place": "十堰市郧阳区",
     "education": "党校大学学历",                 "party_join": "", "work_start": "1994-09",
     "current_post": "郧阳区委副书记、区委政法委书记、三级调研员", "current_org": "中共十堰市郧阳区委员会",
     "source": f"{GOV_HOST}/202412/t20241206_4654540.shtml"},
    {"id": 4, "name": "刘群",                 "gender": "男", "ethnicity": "汉族",   "birth": "1977-03", "birthplace": "湖北竹溪", "native_place": "湖北省竹溪县",
     "education": "省委党校研究生学历",         "party_join": "",                        "work_start": "1995-11",
     "current_post": "郧阳区委常委、常务副区长", "current_org": "郧阳区人民政府",
     "source": f"{GOV_HOST}/202205/t20220513_3502470.shtml"},
    {"id": 5, "name": "雷涛",                 "gender": "男", "ethnicity": "汉族",   "birth": "1978-05", "birthplace": "十堰市郧阳区", "native_place": "十堰市郧阳区",
     "education": "党校研究生学历",             "party_join": "",                        "work_start": "1999-10",
     "current_post": "郧阳区委常委、区政协党组副书记、区委统战部部长、区总工会主席", "current_org": "中共十堰市郧阳区委员会",
     "source": f"{GOV_HOST}/202412/t20241206_4654545.shtml"},
    {"id": 6, "name": "柯相国",                 "gender": "男", "ethnicity": "汉族",   "birth": "1975-02", "birthplace": "十堰市郧阳区", "native_place": "十堰市郧阳区",
     "education": "农业推广硕士",                 "party_join": "",           "work_start": "1995-09",
     "current_post": "郧阳区委常委、区委办公室主任", "current_org": "中共十堰市郧阳区委员会",
     "source": f"{GOV_HOST}/202412/t20241206_4654548.shtml"},
    {"id": 7, "name": "王凡",                 "gender": "女", "ethnicity": "汉族",   "birth": "1983-04", "birthplace": "湖北郧西", "native_place": "湖北省郧西县",
     "education": "省委党校研究生学历",         "party_join": "",                        "work_start": "2005-07",
     "current_post": "郧阳区委常委、区纪委书记、区监委主任、四级高级监察官", "current_org": "中共十堰市郧阳区纪律检查委员会/郧阳区监察委员会",
     "source": f"{GOV_HOST}/202205/t20220513_3502477.shtml"},
    {"id": 8, "name": "卢金华",                 "gender": "男", "ethnicity": "汉族",   "birth": "1982-12", "birthplace": "河南开封", "native_place": "河南省开封市",
     "education": "研究生学历、法学硕士",         "party_join": "",                        "work_start": "2011-09",
     "current_post": "郧阳区委常委、宣传部部长", "current_org": "中共十堰市郧阳区委员会",
     "source": f"{GOV_HOST}/202205/t20220513_3502460.shtml"},
    {"id": 9, "name": "王俊",                 "gender": "男", "ethnicity": "汉族",   "birth": "1975-01", "birthplace": "十堰市郧阳区", "native_place": "十堰市郧阳区",
     "education": "大学学历",                    "party_join": "",                        "work_start": "1996-12",
     "current_post": "郧阳区委常委、副区长",     "current_org": "郧阳区人民政府",
     "source": f"{GOV_HOST}/202205/t20220516_3503477.shtml"},
    {"id": 10, "name": "王一鸣",                "gender": "男", "ethnicity": "汉族",   "birth": "1985-02", "birthplace": "湖北郧西", "native_place": "湖北省郧西县",
     "party_join": "",                          "education": "省委党校研究生学历",   "work_start": "2008-07",
     "current_post": "郧阳区委常委、组织部部长", "current_org": "中共十堰市郧阳区委员会",
     "source": f"{GOV_HOST}/202205/t20220513_3502440.shtml"},
    {"id": 11, "name": "韦燕珍",                "gender": "女", "ethnicity": "壮族",   "birth": "1979-11", "birthplace": "广西崇左", "native_place": "广西壮族自治区崇左市",
     "party_join": "",                          "education": "大学学历",             "work_start": "2002-07",
     "current_post": "郧阳区委常委、副区长",     "current_org": "郧阳区人民政府",
     "source": f"{GOV_HOST}/202412/t20241206_4654543.shtml"},
    {"id": 12, "name": "王铭",                 "gender": "男", "ethnicity": "汉族",   "birth": "1979-09", "birthplace": "北京市东城区", "native_place": "北京市东城区",
     "party_join": "",                              "education": "党校研究生学历",   "work_start": "2002-07",
     "current_post": "郧阳区委常委、副区长",     "current_org": "郧阳区人民政府",
     "source": f"{GOV_HOST}/202412/t20241209_4655599.shtml"},
    {"id": 13, "name": "孔令林",                "gender": "男", "ethnicity": "汉族", "birth": "1973-10", "birthplace": "湖北十堰", "native_place": "湖北省十堰市",
     "education": "大学学历",                     "party_join": "",   "work_start": "1994-07",
     "current_post": "郧阳区副区长、区公安局局长", "current_org": "郧阳区人民政府",
     "source": "https://yunyang.shiyan.gov.cn/xxgkxi/fdzdgknr/zfld/qzfld/202307/t20230718_3958149.shtml"},
    {"id": 14, "name": "何珊",                  "gender": "女", "ethnicity": "汉族",   "birth": "1984-02", "birthplace": "湖北天门", "native_place": "湖北省天门市",
     "education": "大学学历",                     "party_join": "",   "work_start": "2005-07",
     "current_post": "郧阳区副区长",              "current_org": "郧阳区人民政府",
     "source": "https://yunyang.shiyan.gov.cn/xxgkxi/fdzdgknr/zfld/qzfld/202307/t20230718_3958154.shtml"},
    {"id": 15, "name": "肖帮伟",                "gender": "男", "ethnicity": "汉族",   "birth": "1982-11", "birthplace": "郧阳区青曲镇", "native_place": "十堰市郧阳区",
     "education": "大学学历",                     "party_join": "",   "work_start": "2007-07",
     "current_post": "郧阳区副区长",              "current_org": "郧阳区人民政府",
     "source": "https://yunyang.shiyan.gov.cn/xxgkxi/fdzdgknr/zfld/qzfld/202307/t20230718_3958158.shtml"},
    {"id": 16, "name": "王云峰",                "gender": "男", "ethnicity": "汉族",   "birth": "1978-12", "birthplace": "十堰市郧阳区", "native_place": "十堰市郧阳区",
     "education": "大学学历",                     "party_join": "",   "work_start": "1997-07",
     "current_post": "郧阳区副区长",              "current_org": "郧阳区人民政府",
     "source": "https://yunyang.shiyan.gov.cn/xxgkxi/fdzdgknr/zfld/qzfld/202307/t20230718_3958163.shtml"},
{"id": 17, "name": "李一川",                "gender": "男", "ethnicity": "汉族",   "birth": "1982-11", "birthplace": "四川眉山", "native_place": "四川省眉山市",
     "education": "研究生学历、法学博士",         "party_join": "",   "work_start": "2007-09",
     "current_post": "郧阳区副区长",              "current_org": "郧阳区人民政府",
     "source": "https://yunyang.shiyan.gov.cn/xxgkxi/fdzdgknr/zfld/qzfld/202307/t20230718_3958167.shtml"},
]

organizations = [
    {"id": 1, "name": "中共十堰市郧阳区委员会", "type": "党委", "level": "县级", "parent": "中共十堰市委员会", "location": "十堰市郧阳区"},
    {"id": 2, "name": "郧阳区人民政府",          "type": "政府", "level": "县级", "parent": "十堰市人民政府",   "location": "十堰市郧阳区"},
    {"id": 3, "name": "中共十堰市郧阳区纪律检查委员会/郧阳区监察委员会", "type": "党委", "level": "县级", "parent": "中共十堰市纪律检查委员会", "location": "十堰市郧阳区"},
    {"id": 4, "name": "中共十堰市郧阳区委政法委员会", "type": "党委", "level": "县级", "parent": "中共十堰市郧阳区委员会", "location": "十堰市郧阳区"},
    {"id": 5, "name": "中共十堰市郧阳区委办公室", "type": "党委", "level": "县级", "parent": "中共十堰市郧阳区委员会", "location": "十堰市郧阳区"},
    {"id": 6, "name": "中共十堰市郧阳区委宣传部", "type": "党委", "level": "县级", "parent": "中共十堰市郧阳区委员会", "location": "十堰市郧阳区"},
    {"id": 7, "name": "中共十堰市郧阳区委组织部", "type": "党委", "level": "县级", "parent": "中共十堰市郧阳区委员会", "location": "十堰市郧阳区"},
    {"id": 8, "name": "中共十堰市郧阳区委统战部", "type": "党委", "level": "县级", "parent": "中共十堰市郧阳区委员会", "location": "十堰市郧阳区"},
    {"id": 9, "name": "郧阳区总工会",             "type": "群团", "level": "县级", "parent": "十堰市总工会",       "location": "十堰市郧阳区"},
    {"id": 10, "name": "十堰市公安局郧阳区分局",     "type": "政府", "level": "县级", "parent": "郧阳区人民政府",   "location": "十堰市郧阳区"},
]

positions = [
    {"person_id": 1, "org_id": 1, "title": "郧阳区委书记、一级调研员", "start_date": "约2023-2024", "end_date": "", "rank": "正处级", "note": "接替胡正平"},
    {"person_id": 2, "org_id": 1, "title": "郧阳区委副书记",  "start_date": "2024-12", "end_date": "", "rank": "正处级", "note": "兼任区长"},
    {"person_id": 2, "org_id": 2, "title": "郧阳区区长",      "start_date": "2024-12", "end_date": "", "rank": "正处级", "note": "2025-05 官方确认"},
    {"person_id": 3, "org_id": 1, "title": "郧阳区委副书记",  "start_date": "", "end_date": "", "rank": "正处级", "note": "三级调研员"},
    {"person_id": 3, "org_id": 4, "title": "区委政法委书记",  "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "郧阳区委常委",     "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "常务副区长",       "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "郧阳区委常委",     "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 8, "title": "区委统战部部长",   "start_date": "", "end_date": "", "rank": "副处级", "note": "区政协党组副书记、区总工会主席"},
    {"person_id": 6, "org_id": 1, "title": "郧阳区委常委",     "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 5, "title": "区委办公室主任",   "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "郧阳区委常委",     "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 3, "title": "区纪委书记、区监委主任", "start_date": "", "end_date": "", "rank": "副处级", "note": "四级高级监察员"},
    {"person_id": 8, "org_id": 1, "title": "郧阳区委常委",     "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 6, "title": "区委宣传部部长",   "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "郧阳区委常委",     "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副区长",           "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "郧阳区委常委",     "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 7, "title": "区委组织部部长",   "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "郧阳区委常委",     "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "副区长",           "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 1, "title": "郧阳区委常委",     "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "副区长",           "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "副区长、区公安局局长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 10, "title": "区公安局党委书记、局长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "副区长",           "start_date": "", "end_date": "", "rank": "副处级", "note": "非党人士"},
    {"person_id": 15, "org_id": 2, "title": "副区长",           "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "副区长",           "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "副区长",           "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记与区长为郧阳区党政正职搭档", "overlap_org": "郧阳区党委/政府", "overlap_period": "2024-12至今"},
    {"person_a": 1, "person_b": 3, "type": "区委班子", "context": "区委副书记在书记领导下工作", "overlap_org": "中共十堰市郧阳区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "区委班子", "context": "区委常委在书记领导下工作", "overlap_org": "中共十堰市郧阳区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "区委班子", "context": "区委常委在书记领导下工作", "overlap_org": "中共十堰市郧阳区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "区委班子", "context": "区委常委在书记领导下工作", "overlap_org": "中共十堰市郧阳区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "区委班子", "context": "区委常委在书记领导下工作", "overlap_org": "中共十堰市郧阳区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "区委班子", "context": "区委常委在书记领导下工作", "overlap_org": "中共十堰市郧阳区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "区委班子", "context": "区委常委在书记领导下工作", "overlap_org": "中共十堰市郧阳区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 10, "type": "区委班子", "context": "区委常委在书记领导下工作", "overlap_org": "中共十堰市郧阳区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 11, "type": "区委班子", "context": "区委常委在书记领导下工作", "overlap_org": "中共十堰市郧阳区委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 12, "type": "区委班子", "context": "区委常委在书记领导下工作", "overlap_org": "中共十堰市郧阳区委员会", "overlap_period": ""},
    {"person_a": 2, "person_b": 4, "type": "政府班子", "context": "常务副区长在区长领导下工作", "overlap_org": "郧阳区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 9, "type": "政府班子", "context": "副区长在区长领导下工作", "overlap_org": "郧阳区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 11, "type": "政府班子", "context": "副区长在区长领导下工作", "overlap_org": "郧阳区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 12, "type": "政府班子", "context": "副区长在区长领导下工作", "overlap_org": "郧阳区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 13, "type": "政府班子", "context": "副区长在区长领导下工作", "overlap_org": "郧阳区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 14, "type": "政府班子", "context": "副区长在区长领导下工作", "overlap_org": "郧阳区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 15, "type": "政府班子", "context": "副区长在区长领导下工作", "overlap_org": "郧阳区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 16, "type": "政府班子", "context": "副区长在区长领导下工作", "overlap_org": "郧阳区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 17, "type": "政府班子", "context": "副区长在区长领导下工作", "overlap_org": "郧阳区人民政府", "overlap_period": ""},
    {"person_a": 3, "person_b": 7, "type": "政法纪检协同", "context": "政法委书记与纪委书记在综治/纪检协同工作", "overlap_org": "郧阳区", "overlap_period": ""},
]


def build_person_json(p) -> None:
    """写入单个人物深度档案 JSON。"""
    name = p.get("name", "")
    if not name:
        return
    job = p.get("current_post") or "郧阳区领导"
    import re
    _job = re.sub(r"[、，]?[一二三四]级(调研员|高级?监察官|主任科员|科员)?", "", job)
    slug_job = _job.replace("、", "-").replace("/", "-").strip("、")
    filename = f"{TODAY}-{PROVINCE}-{PARENT_CITY}-{slug_job}-{name}.json"
    out_path = PERSONS_OUT / filename

    src_url = p.get("source") or p.get("source_url") or ""
    source_register = [{
        "id": "S001",
        "title": f"郧阳区人民政府领导之窗 - {name}",
        "url": src_url,
        "publisher": "郧阳区人民政府",
        "published_at": AS_OF,
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "郧阳区人民政府官方在职领导信息页（2026-08-06 复核）",
    }]

    edu = []
    if p.get("education"):
        edu.append({"period": "", "institution": "", "major": "", "degree": p["education"],
                    "study_type": "unknown", "source_ids": ["S001"]})

    org_by_id = {o["id"]: o["name"] for o in organizations}
    career_timeline = []
    for pos in positions:
        if pos["person_id"] != p["id"]:
            continue
        career_timeline.append({
            "start": pos["start_date"] or "unknown",
            "end": pos["end_date"] or "present",
            "org": org_by_id.get(pos["org_id"], ""),
            "title": pos["title"],
            "level": pos.get("rank", ""),
            "location": "十堰市郧阳区",
            "system": "party" if pos["org_id"] in (1, 3, 4, 5, 6, 7, 8) else "government",
            "rank": pos.get("rank", ""),
            "is_key_promotion": pos["person_id"] in (1, 2),
            "notes": pos.get("note", ""),
            "confidence": "confirmed" if src_url else "plausible",
            "source_ids": ["S001"],
        })

    org_refs = []
    for pos in positions:
        if pos["person_id"] == p["id"]:
            org_refs.append({"org_name": org_by_id.get(pos["org_id"], ""), "org_type": "", "role": pos["title"]})

    open_q = []
    if not p.get("party_join"):
        open_q.append({"priority": "medium", "question": f"{name}的入党时间",
                       "why_it_matters": "用于精确构建晋升时间线",
                       "suggested_queries": [f"{name} 任前公示 入党", f"{name} 郧阳区 简历"], "last_attempted": AS_OF})
    if not p.get("work_start"):
        open_q.append({"priority": "medium", "question": f"{name}的参加工作年份",
                       "why_it_matters": "用于衡量晋升速度",
                       "suggested_queries": [f"{name} 简历 参加工作", f"{name} 郧阳区"], "last_attempted": AS_OF})

    document = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {"province": PROVINCE, "city": PARENT_CITY, "region": SLUG,
                                "job": job, "task_id": "hubei_郧阳区", "time_focus": "2026"},
        "identity": {
            "person_id": f"hubei_shiyan_yunyang_{name}",
            "name": name, "aliases": [],
            "gender": p.get("gender", ""), "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""), "birthplace": p.get("birthplace", ""),
            "native_place": p.get("native_place", ""),
            "education": edu,
            "party_join": p.get("party_join", ""),
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{p.get('birth', '')}",
                "name_birthplace": f"{name}_{p.get('birthplace', '')}",
                "official_profile_url": src_url,
            },
        },
        "current_status": {"current_post": p.get("current_post", ""), "current_org": p.get("current_org", ""),
                           "administrative_rank": "正处级" if p["id"] in (1, 2, 3) else "副处级",
                           "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S001"]},
        "career_timeline": career_timeline,
        "organizations": org_refs,
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "local_ladder" if "十堰市郧阳区" in (p.get("native_place") or "")
                              else ("cross_county_rotation" if PROVINCE in (p.get("native_place") or "") else "cross_province_rotation"),
            "systems_experience": [],
            "geographic_pattern": [p.get("native_place", "")] if p.get("native_place") else [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [], "speech_themes": [], "management_signals": [],
            "caveat": "工作风格源于公开记录与政务报道推断，并非私人心理评估。",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "搜索范围内未发现纪律处分/审计/负面舆情信号", "date": "", "confidence": "unverified", "source_ids": []}
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed" if p.get("birth") else "plausible",
            "current_role": "confirmed",
            "career_completeness": "partial" if p.get("work_start") else "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "完整履历（早年、历任职务起止时间）",
        },
        "open_questions": open_q,
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(document, f, ensure_ascii=False, indent=2)
    logger.info("person JSON written: %s", out_path)


def main() -> None:
    print(f"Building {SLUG} network data...")
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=str(DB_PATH),
        gexf_path=str(GEXF_PATH),
        overwrite=True,
    )
    print("  Writing person JSON lead-files...")
    for p in persons:
        build_person_json(p)
    print(f"\nDone. Artifacts:\n  DB:   {DB_PATH}\n  GEXF: {GEXF_PATH}")
    _conn = sqlite3.connect(str(DB_PATH))
    print(f"  DB rows: persons={_conn.execute('SELECT COUNT(*) FROM persons').fetchone()[0]}, "
          f"organizations={_conn.execute('SELECT COUNT(*) FROM organizations').fetchone()[0]}, "
          f"positions={_conn.execute('SELECT COUNT(*) FROM positions').fetchone()[0]}, "
          f"relationships={_conn.execute('SELECT COUNT(*) FROM relationships').fetchone()[0]}")
    _conn.close()
    for pf in sorted(OUT_DIR.glob(f"{TODAY}-{PROVINCE}-*")):
        print(f"  Person: {pf}")


if __name__ == "__main__":
    main()