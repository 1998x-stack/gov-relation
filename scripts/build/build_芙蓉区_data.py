#!/usr/bin/env python3
"""芙蓉区（长沙市，湖南省）领导班子工作关系网络数据生成脚本。

Task ID: hunan_芙蓉区
Level: 市辖区
Targets: 区委书记 & 区长

调查日期：2026-08-06
现行班子（截至 2026-07/08，官方确认）：
  - 区委书记：蒋君（原区长，2024-10-08 任代理区长、2024-12-27 当选区长；2026-06 转任区委书记，
    2026-07-30 芙蓉区第七次代表大会七届一次全会再次确认/连任）
  - 区委副书记、代理区长：胡珊珊（女，1985-11，经济学硕士；2026-06-18 区六届人大常委会四次会议
    任命为副区长、代理区长）
  - 区委副书记：刘重（七届一次全会当选）
  - 区委常委（第七届 10 人）：蒋君、胡珊珊、刘重、唐安石、高蒙(纪委书记)、罗加祥、蒋苒、刘胜强、陈国政、杜宸亿
  - 前任区委书记：崔晓（女，2024-05-17 任，至 2026-05），再前任周春晖、于新凡
  - 区人大常委会主任：伍艳飞  区政协主席：喻志刚
  - 区政府副区长：文升云、蒋苒、刘广(公安)、谢孟、杜宸亿、向小芳、石磊

实现：
- 使用公共库 gov_relation.runner.run_build() 构建 SQLite 数据库 + GEXF 图。
- 为核心人物（区委书记蒋君、代理区长胡珊珊）写出 data/persons/ 深度档案 JSON。
- 新产物第一优先级写入本脚本所在暂存目录，再由 scripts/process_tmp.py 校验后归档。

用法：
    python3 data/tmp/hunan_芙蓉区/build_芙蓉区_data.py        # 产出写到暂存目录
    python3 scripts/build/build_芙蓉区_data.py               # 归档后运行，产出到 canonical 目录
"""

import json
import re
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

SLUG = "芙蓉区"
PROVINCE = "湖南省"
PARENT_CITY = "长沙市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

if "__file__" in globals():
    _this = Path(__file__).resolve()
    _in_staging = ("data" in _this.parts) and ("tmp" in _this.parts)
else:
    _in_staging = False
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

GOV_HOST = "http://www.furong.gov.cn"

# ── 人物 ────────────────────────────────────────────────────────────────────
# 证据优先级：芙蓉区人民政府官方《政府领导》专栏（furong.gov.cn/qzf/leaders/，一手官方）>掌上长沙/星辰在线七届区委名单
persons = [
    # ── 核心目标：区委书记 & 区长 ──
    {"id": 1, "name": "蒋君", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_org": "中共长沙市芙蓉区委员会",
     "current_post": "芙蓉区委书记（原区长）",
     "source": "http://www.furong.gov.cn/affairs/fdzdgknr/qtfdxx/zwdt/news/202607/t20260730_12514414.html"},
    {"id": 2, "name": "胡珊珊", "gender": "女", "ethnicity": "汉族",
     "birth": "1985-11", "birthplace": "", "native_place": "",
     "education": "研究生学历、经济学硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "芙蓉区委副书记、代理区长",
     "current_org": "芙蓉区人民政府",
     "source": "http://www.furong.gov.cn/qzf/leaders/202606/t20260622_12415817.html"},
    # ── 前任区委书记 ──
    {"id": 3, "name": "崔晓", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "前任芙蓉区委书记（2024-05 至 2026-05）",
     "current_org": "中共长沙市委员会",
     "source": "http://www.furong.gov.cn/ 领导干部会议 2024-05-17"},
    # ── 区监委 / 纪委（七届常委、高蒙）──
    {"id": 4, "name": "高蒙", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "芙蓉区委常委、纪委书记", "current_org": "中共长沙市芙蓉区纪律检查委员会",
     "source": "news.changsha.cn 七届区委尽职名单"},
    # ── 区委副书记（刘重）──
    {"id": 5, "name": "刘重", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "芙蓉区委副书记", "current_org": "中共长沙市芙蓉区委员会",
     "source": "news.changsha.cn 七届区委一次全会名单"},
    # ── 区委常委 ──
    {"id": 6, "name": "唐安石", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "芙蓉区委常委", "current_org": "中共长沙市芙蓉区委员会",
     "source": "news.changsha.cn 七届区委一次全会名单"},
    {"id": 7, "name": "罗加祥", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "芙蓉区委常委（原副区长）", "current_org": "中共长沙市芙蓉区委员会",
     "source": "news.changsha.cn 七届区委一次全会名单"},
    {"id": 8, "name": "刘胜强", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "芙蓉区委常委", "current_org": "中共长沙市芙蓉区委员会",
     "source": "news.changsha.cn 七届区委一次全会名单"},
    {"id": 9, "name": "陈国政", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "芙蓉区委常委", "current_org": "中共长沙市芙蓉区委员会",
     "source": "news.changsha.cn 七届区委一次全会名单"},
    # ── 人大 / 政协 ──
    {"id": 10, "name": "伍艳飞", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "芙蓉区人大常委会主任", "current_org": "芙蓉区人民代表大会常务委员会",
     "source": "芙蓉区人大 / 媒体（第六届，2024 在任）"},
    {"id": 11, "name": "喻志刚", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "芙蓉区政协主席", "current_org": "中国人民政治协商会议芙蓉区委员会",
     "source": "芙蓉区政协 / 媒体（第六届，2024 在任）"},
    # ── 区政府副区长（官方 furong.gov.cn/qzf/leaders/）──
    {"id": 12, "name": "文升云", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-05", "birthplace": "湖南长沙", "native_place": "湖南省长沙市",
     "education": "党校研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "芙蓉区委常委、副区长", "current_org": "芙蓉区人民政府",
     "source": "http://www.furong.gov.cn/qzf/leaders/202111/t20211118_10355165.html"},
    {"id": 13, "name": "蒋苒", "gender": "女", "ethnicity": "汉族",
     "birth": "1985-07", "birthplace": "", "native_place": "",
     "education": "研究生学历、法学硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "芙蓉区委常委、副区长", "current_org": "芙蓉区人民政府",
     "source": "http://www.furong.gov.cn/qzf/leaders/202111/t20211118_10355136.html"},
    {"id": 14, "name": "刘广", "gender": "男", "ethnicity": "",
     "birth": "1972-08", "birthplace": "", "native_place": "",
     "education": "本科学历、法学硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "芙蓉区副区长、区公安分局党委书记/局长", "current_org": "芙蓉区人民政府",
     "source": "http://www.furong.gov.cn/qzf/leaders/202402/t20240202_11364131.html"},
    {"id": 15, "name": "谢孟", "gender": "男", "ethnicity": "汉族",
     "birth": "1979-05", "birthplace": "", "native_place": "",
     "education": "本科学历（致公党员）",
     "party_join": "", "work_start": "",
     "current_post": "芙蓉区副区长", "current_org": "芙蓉区人民政府",
     "source": "http://www.furong.gov.cn/qzf/leaders/202111/t20211118_10355151.html"},
    {"id": 16, "name": "杜宸亿", "gender": "男", "ethnicity": "回族",
     "birth": "1987-03", "birthplace": "", "native_place": "",
     "education": "本科学历、法学学士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "芙蓉区副区长", "current_org": "芙蓉区人民政府",
     "source": "http://www.furong.gov.cn/qzf/leaders/202508/t20250829_11976367.html"},
    {"id": 17, "name": "向小芳", "gender": "女", "ethnicity": "土家族",
     "birth": "1986-07", "birthplace": "", "native_place": "",
     "education": "本科学历、文学学士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "芙蓉区副区长", "current_org": "芙蓉区人民政府",
     "source": "http://www.furong.gov.cn/qzf/leaders/202512/t20251203_12090860.html"},
    {"id": 18, "name": "石磊", "gender": "男", "ethnicity": "汉族",
     "birth": "1982-07", "birthplace": "", "native_place": "",
     "education": "党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "芙蓉区副区长", "current_org": "芙蓉区人民政府",
     "source": "http://www.furong.gov.cn/qzf/leaders/202504/t20250424_11827847.html"},
]

organizations = [
    {"id": 1, "name": "中共长沙市芙蓉区委员会", "type": "党委", "level": "区级", "parent": "中共长沙市委", "location": "长沙市芙蓉区"},
    {"id": 2, "name": "芙蓉区人民政府", "type": "政府", "level": "区级", "parent": "长沙市人民政府", "location": "长沙市芙蓉区"},
    {"id": 3, "name": "芙蓉区纪律检查委员会/监委", "type": "党委", "level": "区级", "parent": "中共长沙市纪律检查委员会", "location": "长沙市芙蓉区"},
    {"id": 4, "name": "芙蓉区委组织部", "type": "党委", "level": "区级", "parent": "中共芙蓉区委", "location": "长沙市芙蓉区"},
    {"id": 5, "name": "芙蓉区委宣传部/统战部/政法委", "type": "党委", "level": "区级", "parent": "中共芙蓉区委", "location": "长沙市芙蓉区"},
    {"id": 6, "name": "芙蓉区人民代表大会常务委员会", "type": "人大", "level": "区级", "parent": "长沙市人民代表大会常务委员会", "location": "长沙市芙蓉区"},
    {"id": 7, "name": "中国人民政治协商会议芙蓉区委员会", "type": "政协", "level": "区级", "parent": "中国人民政治协商会议长沙市委员会", "location": "长沙市芙蓉区"},
    {"id": 8, "name": "长沙市公安局芙蓉区分局", "type": "政府", "level": "区级", "parent": "芙蓉区人民政府", "location": "长沙市芙蓉区"},
]

positions = [
    # ── 区委班子 ──
    {"person_id": 1, "org_id": 1, "title": "芙蓉区委书记", "start_date": "2026-06", "end_date": "", "rank": "正处级",
     "note": "2026-06 由区长转任书记；2026-07-30 七届一次全会连任"},
    {"person_id": 1, "org_id": 2, "title": "芙蓉区区长（此前）", "start_date": "2024-10", "end_date": "2026-06", "rank": "正处级",
     "note": "2024-10-08 区六届人大二十六次会议任代理区长；2024-12-27 当选区长"},
    {"person_id": 2, "org_id": 1, "title": "芙蓉区委副书记", "start_date": "2026-06", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "芙蓉区代理区长", "start_date": "2026-06-18", "end_date": "", "rank": "正处级",
     "note": "区六届人大常委会四次会议任命为副区长、代理区长；主持区政府全面工作"},
    {"person_id": 3, "org_id": 1, "title": "前任芙蓉区委书记", "start_date": "2024-05", "end_date": "2026-05", "rank": "正处级",
     "note": "2024-05-17 省委/市委决定任区委书记；2026-05 卸任，去向待查（open gap）"},
    {"person_id": 5, "org_id": 1, "title": "芙蓉区委副书记", "start_date": "", "end_date": "", "rank": "正处级",
     "note": "七届一次全会当选；六届曾任区委副书记兼统战部长"},
    {"person_id": 4, "org_id": 3, "title": "芙蓉区委常委、纪委书记", "start_date": "", "end_date": "", "rank": "副处级",
     "note": "七届区委常委"},
    {"person_id": 6, "org_id": 1, "title": "芙蓉区委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": "七届区委常委"},
    {"person_id": 7, "org_id": 1, "title": "芙蓉区委常委（原副区长）", "start_date": "", "end_date": "", "rank": "副处级", "note": "七届区委常委"},
    {"person_id": 8, "org_id": 1, "title": "芙蓉区委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": "七届区委常委"},
    {"person_id": 9, "org_id": 1, "title": "芙蓉区委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": "七届区委常委"},
    # ── 人大 / 政协 ──
    {"person_id": 10, "org_id": 6, "title": "芙蓉区人大常委会主任", "start_date": "", "end_date": "", "rank": "正处级", "note": "第六届在任"},
    {"person_id": 11, "org_id": 7, "title": "芙蓉区政协主席", "start_date": "", "end_date": "", "rank": "正处级", "note": "第六届在任"},
    # ── 政府副区长（含常委）──
    {"person_id": 12, "org_id": 2, "title": "芙蓉区委常委、副区长", "start_date": "", "end_date": "", "rank": "副处级",
     "note": "分管教育/文旅/卫健/医保"},
    {"person_id": 13, "org_id": 2, "title": "芙蓉区委常委、副区长", "start_date": "", "end_date": "", "rank": "副处级",
     "note": "分管商务/金融/楼宇经济/自贸区"},
    {"person_id": 14, "org_id": 2, "title": "芙蓉区副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "分管公安/信访"},
    {"person_id": 14, "org_id": 8, "title": "区公安分局党委书记/局长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "芙蓉区副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "分管住建/拆迁/规划"},
    {"person_id": 16, "org_id": 2, "title": "芙蓉区副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "分管科技/工信/司法/隆平园区"},
    {"person_id": 17, "org_id": 2, "title": "芙蓉区副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "分管民政/农业农村/市场监管"},
    {"person_id": 18, "org_id": 2, "title": "芙蓉区副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "分管城管/执法/生态环境"},
]

relationships = [
    # 前任→现任 书记交接
    {"person_a": 3, "person_b": 1, "type": "predecessor_successor",
     "context": "崔晓（女，2024-05 起任芙蓉区委书记）与蒋君（区长）完成区委一把手交接；蒋君于2026-06接任区委书记",
     "overlap_org": "中共长沙市芙蓉区委员会", "overlap_period": "2024-2026"},
    # 现任书记 × 区党政搭档（区长）
    {"person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "蒋君（区委书记）与胡珊珊（区委副书记、代理区长）组成芙蓉区党政正职搭配",
     "overlap_org": "芙蓉区党委/政府", "overlap_period": "2026至今"},
    # 书记 × 区委副书记
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "区委书记与区委副书记刘重同属芙蓉区区委常委会",
     "overlap_org": "中共长沙市芙蓉区委员会", "overlap_period": "2026"},
    # 书记 × 纪委书记
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "区委书记与区纪委书记高蒙同属区委常委会（管党治党）",
     "overlap_org": "中共长沙市芙蓉区委员会", "overlap_period": "2026"},
    # 书记 × 其他常委
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "区委书记与区委常委唐安石同属区委常委会",
     "overlap_org": "中共长沙市芙蓉区委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate",
     "context": "区委书记与区委常委罗加祥同属区委常委会",
     "overlap_org": "中共长沙市芙蓉区委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate",
     "context": "区委书记与区委常委刘胜强同属区委常委会",
     "overlap_org": "中共长沙市芙蓉区委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate",
     "context": "区委书记与区委常委陈国政同属区委常委会",
     "overlap_org": "中共长沙市芙蓉区委员会", "overlap_period": "2026"},
    # 四套班子
    {"person_a": 1, "person_b": 10, "type": "四套班子",
     "context": "区委书记与区人大常委会主任同属区四套班子",
     "overlap_org": "芙蓉区", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 11, "type": "四套班子",
     "context": "区委书记与区政协主席同属区四套班子",
     "overlap_org": "芙蓉区", "overlap_period": "2026"},
    # 区长（胡）与区政府副区长
    {"person_a": 2, "person_b": 12, "type": "政府班子",
     "context": "代理区长与区委常委副区长文升云在区政府班子共事",
     "overlap_org": "芙蓉区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 13, "type": "政府班子",
     "context": "代理区长与区委常委副区长蒋苒在区政府班子共事",
     "overlap_org": "芙蓉区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 14, "type": "政府班子",
     "context": "代理区长与副区长刘广（公安局长）在区政府班子共事",
     "overlap_org": "芙蓉区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 15, "type": "政府班子",
     "context": "代理区长与副区长谢孟在区政府班子共事",
     "overlap_org": "芙蓉区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 16, "type": "政府班子",
     "context": "代理区长与副区长杜宸亿在区政府班子共事",
     "overlap_org": "芙蓉区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 17, "type": "政府班子",
     "context": "代理区长与副区长向小芳在区政府班子共事",
     "overlap_org": "芙蓉区人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 18, "type": "政府班子",
     "context": "代理区长与副区长石磊在区政府班子共事",
     "overlap_org": "芙蓉区人民政府", "overlap_period": "2026"},
]


def build_person_json(p) -> None:
    """写入单个人物深度档案 JSON。"""
    name = p.get("name", "")
    if not name:
        return
    job = p.get("current_post") or "芙蓉区领导"
    _job = re.sub(r"[、，]?[一二三四]级(调研员|高级?监察官|主任科员|科员)?", "", job)
    slug_job = _job.replace("、", "-").replace("/", "-").strip("、")
    filename = f"{TODAY}-{PROVINCE}-{PARENT_CITY}-{slug_job}-{name}.json"
    out_path = PERSONS_OUT / filename

    src_url = p.get("source") or p.get("source_url") or ""
    source_register = [{
        "id": "S001", "title": f"芙蓉区官方组织/《政府之窗》2026 复核 - {name}",
        "url": src_url, "publisher": "芙蓉区人民政府/长沙本地媒体", "published_at": AS_OF,
        "accessed_at": AS_OF, "source_type": "official" if "furong.gov.cn" in str(src_url) else "encyclopedia",
        "reliability": "high" if "furong.gov.cn" in str(src_url) else "medium",
        "notes": "芙蓉区领导班子在任信息（2026-08-06 复核）",
    }]

    edu = []
    if p.get("education"):
        edu.append({"period": "", "institution": "", "major": "",
                    "degree": p["education"], "study_type": "unknown", "source_ids": ["S001"]})

    org_by_id = {o["id"]: o["name"] for o in organizations}
    career_timeline = []
    for pos in positions:
        if pos["person_id"] != p["id"]:
            continue
        e_system = "party" if pos["org_id"] in (1, 3, 4, 5) else "government"
        career_timeline.append({
            "start": pos["start_date"] or "unknown", "end": pos["end_date"] or "present",
            "org": org_by_id.get(pos["org_id"], ""), "title": pos["title"],
            "level": pos.get("rank", ""), "location": "长沙市芙蓉区",
            "system": e_system,
            "rank": pos.get("rank", ""), "is_key_promotion": pos["person_id"] in (1, 2, 3),
            "notes": pos.get("note", ""), "confidence": "confirmed" if p.get("birth") or p["id"] in (1,2,3) else "plausible",
            "source_ids": ["S001"],
        })

    open_q = []
    if name == "蒋君":
        open_q.extend([
            {"priority": "critical", "question": "蒋君完整履历（出生年月、籍贯、学历、入党/参加工作时间、2024 年前任职序列）",
             "why_it_matters": "核心人物区委书记的主要履历完全未公开搜索到",
             "suggested_queries": ["蒋君 芙蓉区委书记 简历", "蒋君 任前公示"], "last_attempted": AS_OF},
        ])
    elif name == "胡珊珊":
        open_q.extend([
            {"priority": "high", "question": "胡珊珊的籍贯、工作起始时间、2026-06 前完整任职序列",
             "why_it_matters": "确认代理区长的完整身份与晋升路径",
             "suggested_queries": ["胡珊珊 芙蓉区 简历", "胡珊珊 任前公示"], "last_attempted": AS_OF},
        ])
    elif name == "崔晓":
        open_q.append({"priority": "high", "question": "崔晓（前任区委书记）卸任去向与完整履历",
                       "why_it_matters": "核心前任的去向是突破线索",
                       "suggested_queries": ["崔晓 芙蓉 卸任 去向"], "last_attempted": AS_OF})

    document = {
        "schema_version": "1.0", "generated_at": AS_OF,
        "investigation_scope": {"province": PROVINCE, "city": PARENT_CITY, "region": SLUG,
                                "job": job, "task_id": "hunan_芙蓉区", "time_focus": "2026"},
        "identity": {
            "person_id": f"hunan_changsha_furong_{name}",
            "name": name, "aliases": [],
            "gender": p.get("gender", ""), "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""), "birthplace": p.get("birthplace", ""),
            "native_place": p.get("native_place", ""), "education": edu,
            "party_join": p.get("party_join", ""), "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{p.get('birth', '')}",
                "name_birthplace": f"{name}_{p.get('birthplace', '')}",
                "official_profile_url": src_url,
            },
        },
        "current_status": {"current_post": p.get("current_post", ""),
                           "current_org": p.get("current_org", ""),
                           "administrative_rank": "正处级" if p["id"] in (1, 2, 3, 5, 10, 11) else "副处级",
                           "as_of": AS_OF, "is_current_confirmed": p["id"] in (1, 2, 3, 4, 12, 13),
                           "source_ids": ["S001"]},
        "career_timeline": career_timeline,
        "organizations": [{"org_name": org_by_id.get(idx, ""), "org_type": "", "role": t}
                          for idx, t in [(pos["org_id"], pos["title"]) for pos in positions if pos["person_id"] == p["id"]]],
        "relationships": [], "governance_record": [],
        "professional_profile": {
            "primary_specializations": [], "secondary_specializations": [],
            "career_pattern": "local_ladder", "systems_experience": [],
            "geographic_pattern": [p.get("native_place", "")] if p.get("native_place") else [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [], "speech_themes": [], "management_signals": [],
            "caveat": "工作风格源于公开记录与政务报道推断，并非私人心理评估。",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "搜索范围内未发现纪律处分/审计/负面舆情信号（备注：芙蓉区系省会中心城区，房地产业转型与基建阵痛期治理压力较大，未发现针对核心人物的立案信号）", "date": "", "confidence": "unverified", "source_ids": []}
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed" if p.get("birth") else "partial",
            "current_role": "confirmed" if p["id"] in (1, 2, 3) else "plausible",
            "career_completeness": "thin", "relationship_confidence": "medium",
            "biggest_gap": "核心人物早年/完整履历、前任去向",
        },
        "open_questions": open_q,
    }
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(document, f, ensure_ascii=False, indent=2)
    logger.info("person JSON written: %s", out_path)


def main() -> None:
    print(f"Building {SLUG} network data...")
    run_build(
        slug=SLUG, persons=persons, organizations=organizations,
        positions=positions, relationships=relationships,
        db_path=str(DB_PATH), gexf_path=str(GEXF_PATH), overwrite=True,
    )
    print("  Writing person JSON lead-files...")
    core = {p["id"] for p in persons if p["name"] in ("蒋君", "胡珊珊", "崔晓")}
    for p in persons:
        if p["id"] in core:
            build_person_json(p)
    print(f"\nDone. Artifacts:\n  DB:   {DB_PATH}\n  GEXF: {GEXF_PATH}")
    _conn = sqlite3.connect(str(DB_PATH))
    print(f"  DB rows: persons={_conn.execute('SELECT COUNT(*) FROM persons').fetchone()[0]}, "
          f"organizations={_conn.execute('SELECT COUNT(*) FROM organizations').fetchone()[0]}, "
          f"positions={_conn.execute('SELECT COUNT(*) FROM positions').fetchone()[0]}, "
          f"relationships={_conn.execute('SELECT COUNT(*) FROM relationships').fetchone()[0]}")
    _conn.close()
    for pf in sorted(PERSONS_OUT.glob(f"{TODAY}-{PROVINCE}-*")):
        print(f"  Person: {pf}")


if __name__ == "__main__":
    main()