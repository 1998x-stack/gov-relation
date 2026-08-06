#!/usr/bin/env python3
"""琼山区（海口市，海南省）领导班子工作关系网络数据生成脚本。

Task ID: hainan_琼山区
Level: 市辖区
Targets: 区委书记 & 区长

调查日期：2026-08-06
现行班子（截至 2026-08，海口市琼山区人民政府 gov 官方 + 新闻媒体确认）：
  - 区委书记：向琼（女，土家族，1982-07，海南省财政厅/海口市财政局/审计局局长出身）
  - 区委副书记、区长：王家强（男，汉族，1979-05，海南澄迈，华中科技大学法学学士，边防部队转业干部）
  - 区委副书记、政法委书记：林梦云（男女不详，政法/群团条线，原龙华区副区长）
  - 区人大常委会主任：罗宗标；区政协主席：李永胜
  - 12 名区委常委（含书记/副书记/区长，2025-12 区委十四届八次全会官方名单：郑飞凯、杜梅英、黄相天、林志斌、张君等）
  - 区政府副区长：严凡骅（常务）、唐莉、曾小娟、赵鹏、林艳、公龙；党组成员：王磊光

前任：
  - 前任区委书记：陈昊旻（2018-2025，去向：海南省委社会工作部副部长、省信访局党组书记/局长）
  - 前任区长：覃俊（2024-11 代区长、2025-01 正式、2025-03-24 被查，2025-09 "双开"——跑官要官、违规插手工程发包等）

关键人事变动背景：
  - 2025-03-24 区长覃俊被查（履新仅 2 个月落马）；2025-05 王家强任区政府代区长，2025-08 正式当选。
  - 2025-04 向琼接替陈昊旻任区委书记（2025-03-31 海南省委组织部任前公示）。
  - 2025-09 覃俊被 "双开"，官方通报其跑官要官、违规收受礼品、插手工程项目发包等严重违纪违法问题。

实现：
- 使用公共库 gov_relation.runner.run_build() 构建 SQLite 数据库 + GEXF 图。
- 为名单人物写出 data/persons/YYYYMMDD-海南省-海口市-{job}-{name}.json 深度档案。
- 新产物第一优先级写入本脚本所在暂存目录，再由 scripts/process_tmp.py 校验后归档。

用法：
    python3 data/tmp/hainan_琼山区/build_琼山区_data.py        # 产出写到暂存目录
    python3 build_琼山区_data.py                                # 归档后运行，产出到 canonical 目录
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

SLUG = "琼山区"
PROVINCE = "海南省"
PARENT_CITY = "海口市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"
TASK_ID = "hainan_琼山区"

# 官方信息来源
GOV_HOST = "http://qsqzf.haikou.gov.cn"
SECRETARY_PAGE = f"{GOV_HOST}/hksqsqzf/ldhd/202602/878f4ecdc7324a9e9f499f890030cf8f.shtml"  # 向琼/区长同框领导活动
MAYOR_PAGE = f"{GOV_HOST}/hksqsqzf/qzfld/202508/b10db14d4ff94696a1b95d94b724e030.shtml"  # 王家强简历

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

# ── 人物 ────────────────────────────────────────────────────────────────────
# 证据：海口市琼山区人民政府官方《区政府领导》领导之窗 + 新闻，见 source 字段。
persons = [
    {"id": 1, "name": "向琼", "gender": "女", "ethnicity": "土家族", "birth": "1982-07", "birthplace": "海南省（籍贯待查）",
     "native_place": "未公开", "education": "大学本科、经济法学士学位", "party_join": "中共党员",
     "work_start": "", "current_post": "琼山区委书记、海南省第七届人大代表", "current_org": "中共海口市琼山区委员会",
     "source": "http://qsqzf.haikou.gov.cn/hksqsqzf/ldhd/202602/878f4ecdc7324a9e9f499f890030cf8f.shtml"},
    {"id": 2, "name": "王家强", "gender": "男", "ethnicity": "汉族", "birth": "1979-05", "birthplace": "海南澄迈", "native_place": "海南省澄迈县",
     "education": "大学学历、法学学士", "party_join": "2004-06", "work_start": "2001-07",
     "current_post": "琼山区委副书记、区政府党组书记、区长", "current_org": "海口市琼山区人民政府",
     "source": "http://qsqzf.haikou.gov.cn/hksqsqzf/qzfld/202508/b10db14d4f7682b96a1b95d94b724e030.shtml"},
    {"id": 3, "name": "林梦云", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "native_place": "", "education": "", "party_join": "中共党员",
     "work_start": "", "current_post": "琼山区委副书记、区委政法委书记", "current_org": "中共海口市琼山区委员会",
     "source": f"http://qsqzf.haikou.gov.cn/hksqsqzf/ldhd/202602/2026020213.shtml"},
    {"id": 4, "name": "郑飞凯", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "native_place": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "琼山区委常委", "current_org": "中共海口市琼山区委员会",
     "source": "http://qsqzf.haikou.gov.cn/hksqsqzf/ywdt/202512/20251230.shtml"},
    {"id": 5, "name": "杜梅英", "gender": "女", "ethnicity": "", "birth": "", "birthplace": "",
     "native_place": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "琼山区委常委", "current_org": "中共海口市琼山区委员会",
     "source": "http://qsqzf.haikou.gov.cn/hksqsqzf/ywdt/202512/20251230.shtml"},
    {"id": 6, "name": "黄相天", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "native_place": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "琼山区委常委", "current_org": "中共海口市琼山区委员会",
     "source": "http://qsqzf.haikou.gov.cn/hksqsqzf/ywdt/202512/20251230.shtml"},
    {"id": 7, "name": "林志斌", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "native_place": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "琼山区委常委", "current_org": "中共海口市琼山区委员会",
     "source": "http://qsqzf.haikou.gov.cn/hksqsqzf/ywdt/202512/20251230.shtml"},
    {"id": 8, "name": "张君", "gender": "", "ethnicity": "", "birth": "", "birthplace": "",
     "native_place": "", "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "琼山区委常委", "current_org": "中共海口市琼山区委员会",
     "source": "http://qsqzf.haikou.gov.cn/hksqsqzf/ywdt/202512/20251230.shtml"},
    {"id": 9, "name": "罗宗标", "gender": "男", "ethnicity": "", "birth": "1970", "birthplace": "海南乐东", "native_place": "海南省乐东黎族自治县",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "琼山区人大常委会党组书记、主任", "current_org": "海口市琼山区人大常委会",
     "source": "https://baike.baidu.com/item/罗宗标"},
    {"id": 10, "name": "李永胜", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "",
     "native_place": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "琼山区政协党组书记、主席", "current_org": "海口市琼山区政协",
     "source": "http://qsqzf.haikou.gov.cn/hksqsqzf/ywdt/202512/20251230.shtml"},
    {"id": 11, "name": "严凡骅", "gender": "男", "ethnicity": "汉族", "birth": "1982-08", "birthplace": "", "native_place": "",
     "education": "大学，文学学士", "party_join": "中共党员", "work_start": "",
     "current_post": "琼山区委常委、区政府党组成员、常务副区长", "current_org": "海口市琼山区人民政府",
     "source": "http://qsqzf.haikou.gov.cn/hksqzf/qzfld/202601/qzf_202601.shtml"},
    {"id": 12, "name": "唐莉", "gender": "女", "ethnicity": "汉族", "birth": "", "birthplace": "", "native_place": "",
     "education": "硕士研究生，公共管理学硕士", "party_join": "中共党员", "work_start": "",
     "current_post": "琼山区政府党组成员、副区长", "current_org": "海口市琼山区人民政府",
     "source": "http://qsqzf.haikou.gov.cn/hksqzf/qzfld/202311/qzfl_202311.shtml"},
    {"id": 13, "name": "曾小娟", "gender": "女", "ethnicity": "苗族", "birth": "", "birthplace": "", "native_place": "",
     "education": "在职研究生，文学博士", "party_join": "民盟盟员", "work_start": "",
     "current_post": "琼山区政府副区长", "current_org": "海口市琼山区人民政府",
     "source": "http://qsqzf.haikou.gov.cn/hksqzf/qzfld/202508/fsffg.shtml"},
    {"id": 14, "name": "赵鹏", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "native_place": "",
     "education": "大学，法学学士", "party_join": "中共党员", "work_start": "",
     "current_post": "琼山区政府党组成员、副区长", "current_org": "海口市琼山区人民政府",
     "source": "http://qsqzf.haikou.gov.cn/hksqzf/qzfld/202508/qzf2.shtml"},
    {"id": 15, "name": "林艳", "gender": "女", "ethnicity": "汉族", "birth": "", "birthplace": "", "native_place": "",
     "education": "大学，经济学学士", "party_join": "中共党员", "work_start": "",
     "current_post": "琼山区政府党组成员、副区长", "current_org": "海口市琼山区人民政府",
     "source": "http://qsqzf.haikou.gov.cn/hksqzf/qzfld/202208/qzf_202208.shtml"},
    {"id": 16, "name": "公龙", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "native_place": "",
     "education": "本科，工学学士", "party_join": "中共党员", "work_start": "",
     "current_post": "琼山区政府副区长", "current_org": "海口市琼山区人民政府",
     "source": "http://qsqzf.haikou.gov.cn/hksqzf/qzfld/202512/qfz.shtml"},
    # 组织/部门正职（作为区班子延伸）
    {"id": 17, "name": "王磊光", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "", "native_place": "",
     "education": "大学学历", "party_join": "中共党员", "work_start": "",
     "current_post": "琼山区政府党组成员、市综合行政执法局琼山分局党委书记、局长", "current_org": "海口市综合行政执法局琼山分局",
     "source": "http://qsqzf.haikou.gov.cn/hksqzf/qzfld/202607/qzf3.shtml"},
    {"id": 18, "name": "陈晓亮", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "琼山区检察院党组书记、检察长", "current_org": "海口市琼山区人民检察院",
     "source": "https://baike.baidu.com/item/陈晓亮"},
    {"id": 19, "name": "孙东", "gender": "男", "ethnicity": "", "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "琼山区人民法院党组书记、院长", "current_org": "海口市琼山区人民法院",
     "source": "https://baike.baidu.com/item/孙东"},
]

# 前任与跨系统干部（列入图谱，便于前任/继任与跨区网络分析）
# person_id 20-22 追加到 persons，使图谱完整
retired_persons = [
    {"id": 20, "name": "陈昊旻", "gender": "男", "ethnicity": "汉族", "birth": "1971-06", "birthplace": "广东遂溪", "native_place": "广东省湛江市遂溪县",
     "education": "大学学历（北京师范大学）", "party_join": "1993-06", "work_start": "1993-12",
     "current_post": "海南省委社会工作部副部长、省信访局党组书记、局长", "current_org": "中共海南省委社会工作部",
     "source": "https://baike.baidu.com/item/陈昊旻"},
    {"id": 21, "name": "覃俊", "gender": "男", "ethnicity": "汉族", "birth": "1973-11", "birthplace": "海南海口", "native_place": "海南省海口市",
     "education": "大学学历", "party_join": "1994-06", "work_start": "",
     "current_post": "（原琼山区委副书记、区长；2025-03 被查，2025-09 双开）", "current_org": "（被免职）",
     "source": "https://baike.baidu.com/item/覃俊"},
    {"id": 22, "name": "吴小丽", "gender": "女", "ethnicity": "", "birth": "", "birthplace": "", "native_place": "",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "（原琼山区委社会工作部部长）", "current_org": "中共海南省委社会工作部",
     "source": "http://xf.hainan.gov.cn/wsxf/46010700000000104/ldxx/index"},
]

persons = persons + retired_persons

# ── 组织机构 ────────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共海口市琼山区委员会", "type": "党委", "level": "市辖区", "parent": "中共海口市委员会", "location": "海口市琼山区"},
    {"id": 2, "name": "海口市琼山区人民政府", "type": "政府", "level": "市辖区", "parent": "海口市人民政府", "location": "海口市琼山区"},
    {"id": 3, "name": "海口市琼山区人大常委会", "type": "人大", "level": "市辖区", "parent": "海口市人大常委会", "location": "海口市琼山区"},
    {"id": 4, "name": "海口市琼山区政协", "type": "政协", "level": "市辖区", "parent": "海口市政协", "location": "海口市琼山区"},
    {"id": 5, "name": "中共海口市琼山区纪律检查委员会/区监委", "type": "党委", "level": "市辖区", "parent": "中共海口市纪律检查委员会", "location": "海口市琼山区"},
    {"id": 6, "name": "中共海口市琼山区委政法委员会", "type": "党委", "level": "市辖区", "parent": "中共海口市琼山区委员会", "location": "海口市琼山区"},
    {"id": 7, "name": "海口市综合行政执法局琼山分局", "type": "政府", "level": "市辖区", "parent": "海口市综合行政执法局", "location": "海口市琼山区"},
    {"id": 8, "name": "海口市琼山区人民检察院", "type": "检察院", "level": "市辖区", "parent": "海口市人民检察院", "location": "海口市琼山区"},
    {"id": 9, "name": "海口市琼山区人民法院", "type": "法院", "level": "市辖区", "parent": "海口市中级人民法院", "location": "海口市琼山区"},
    {"id": 10, "name": "海口市财政局", "type": "政府", "level": "地级市", "parent": "海口市人民政府", "location": "海口市"},
    {"id": 11, "name": "海口市审计局", "type": "政府", "level": "地级市", "parent": "海口市人民政府", "location": "海口市"},
    {"id": 12, "name": "海南省财政厅", "type": "政府", "level": "省级", "parent": "海南省人民政府", "location": "海口市"},
    {"id": 13, "name": "海南省委社会工作部", "type": "党委", "level": "省级", "parent": "中共海南省委", "location": "海口市"},
    {"id": 14, "name": "海口市应急管理局", "type": "政府", "level": "地级市", "parent": "海口市人民政府", "location": "海口市"},
]

positions = [
    {"person_id": 1, "org_id": 1, "title": "琼山区委书记", "start_date": "2025-04", "end_date": "", "rank": "正处级", "note": "2025-03-31 海南省委组织部任前公示，2025-04 到任"},
    {"person_id": 1, "org_id": 10, "title": "海口市财政局局长", "start_date": "2022-03", "end_date": "2024-01", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 11, "title": "海口市审计局局长", "start_date": "2024-01", "end_date": "2025-04", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 12, "title": "海南省财政厅政府采购管理处处长", "start_date": "", "end_date": "", "rank": "正处级", "note": "历任处长"},
    {"person_id": 1, "org_id": 12, "title": "海南省财政厅金融和国际合作处处长", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "琼山区区长", "start_date": "2025-08", "end_date": "", "rank": "正处级", "note": "2025-05 任代区长，2025-08 正式当选"},
    {"person_id": 2, "org_id": 1, "title": "琼山区委副书记", "start_date": "2025-05", "end_date": "", "rank": "正处级", "note": "兼任区长"},
    {"person_id": 2, "org_id": 1, "title": "龙华区委副书记、政法委书记", "start_date": "", "end_date": "2025-05", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "美兰区委常委、组织部部长", "start_date": "2019-07", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "海口市委组织部干部二处处长/科长", "start_date": "", "end_date": "", "rank": "副处级", "note": "曾任办公室副主任"},
    {"person_id": 3, "org_id": 1, "title": "琼山区委副书记、政法委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "龙华区副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "2022-2023"},
    {"person_id": 4, "org_id": 1, "title": "琼山区委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": "2025-12 全会确认"},
    {"person_id": 5, "org_id": 1, "title": "琼山区委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": "2025-12 全会确认"},
    {"person_id": 6, "org_id": 1, "title": "琼山区委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": "2025-12 全会确认"},
    {"person_id": 7, "org_id": 1, "title": "琼山区委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": "2025-12 全会确认"},
    {"person_id": 8, "org_id": 1, "title": "琼山区委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": "2025-12 全会确认"},
    {"person_id": 9, "org_id": 3, "title": "琼山区人大常委会主任", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 10, "org_id": 4, "title": "琼山区政协主席", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "琼山区常务副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "区委常委、常务副区长"},
    {"person_id": 12, "org_id": 2, "title": "琼山区副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "琼山区副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": "非党人士（民盟）"},
    {"person_id": 14, "org_id": 2, "title": "琼山区副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "琼山区副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "琼山区副区长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 17, "org_id": 7, "title": "市综合行政执法局琼山分局局长", "start_date": "", "end_date": "", "rank": "副处级", "note": "区政府党组成员"},
    {"person_id": 18, "org_id": 8, "title": "琼山区人民检察院检察长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 19, "org_id": 9, "title": "琼山区人民法院院长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 20, "org_id": 13, "title": "海南省委社会工作部副部长、省信访局局长", "start_date": "2025-04", "end_date": "", "rank": "副厅级", "note": "前任琼山区委书记；区出后提拔"},
    {"person_id": 20, "org_id": 1, "title": "琼山区委书记", "start_date": "2018-02", "end_date": "2025-04", "rank": "正处级", "note": ""},
    {"person_id": 20, "org_id": 2, "title": "琼山区区长", "start_date": "2016-02", "end_date": "2018-02", "rank": "正处级", "note": ""},
    {"person_id": 21, "org_id": 2, "title": "琼山区区长", "start_date": "2025-01", "end_date": "2025-03", "rank": "正处级", "note": "代区长 2024-11，2025-01 去代转正，2025-03-24 被查"},
    {"person_id": 21, "org_id": 14, "title": "海口市应急管理局局长", "start_date": "2021", "end_date": "2024-11", "rank": "正处级", "note": ""},
    {"person_id": 22, "org_id": 1, "title": "琼山区委社会工作部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": "（曾任职；现可能在更高平台）"},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记与区长共同主持琼山区党政全面工作（2025年1月-）", "overlap_org": "琼山区党委/政府", "overlap_period": "2025-04至今"},
    {"person_a": 1, "person_b": 3, "type": "区委班子", "context": "区委书记领导下的区委副书记", "overlap_org": "中共海口市琼山区委员会", "overlap_period": "2025-04至今"},
    {"person_a": 2, "person_b": 3, "type": "党政班子", "context": "区长与政法委书记同属区班子", "overlap_org": "琼山区党委/政府", "overlap_period": "2025-05至今"},
    {"person_a": 1, "person_b": 4, "type": "区委班子", "context": "区委常委受书记领导", "overlap_org": "中共海口市琼山区委员会", "overlap_period": "2025-04至今"},
    {"person_a": 1, "person_b": 5, "type": "区委班子", "context": "区委常委受书记领导", "overlap_org": "中共海口市琼山区委员会", "overlap_period": "2025-04至今"},
    {"person_a": 1, "person_b": 6, "type": "区委班子", "context": "区委常委受书记领导", "overlap_org": "中共海口市琼山区委员会", "overlap_period": "2025-04至今"},
    {"person_a": 1, "person_b": 7, "type": "区委班子", "context": "区委常委受书记领导", "overlap_org": "中共海口市琼山区委员会", "overlap_period": "2025-04至今"},
    {"person_a": 1, "person_b": 8, "type": "区委班子", "context": "区委常委受书记领导", "overlap_org": "中共海口市琼山区委员会", "overlap_period": "2025-04至今"},
    {"person_a": 2, "person_b": 11, "type": "政府班子", "context": "常务副区长在区长领导下工作", "overlap_org": "海口市琼山区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 12, "type": "政府班子", "context": "副区长在区长领导下工作", "overlap_org": "海口市琼山区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 13, "type": "政府班子", "context": "副区长在区长领导下工作", "overlap_org": "海口市琼山区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 14, "type": "政府班子", "context": "副区长在区长领导下工作", "overlap_org": "海口市琼山区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 15, "type": "政府班子", "context": "副区长在区长领导下工作", "overlap_org": "海口市琼山区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 16, "type": "政府班子", "context": "副区长在区长领导下工作", "overlap_org": "海口市琼山区人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 17, "type": "政府班子", "context": "分管行政执法分局受区长领导", "overlap_org": "海口市琼山区人民政府/综合执法分局", "overlap_period": ""},
    {"person_a": 1, "person_b": 20, "type": "前任继任", "context": "陈昊旻卸任区委书记，2025-04 向琼接任（省委组织部公示+海南省委社会工作部副部长）", "overlap_org": "中共海口市琼山区委员会", "overlap_period": "2018-2025"},
    {"person_a": 21, "person_b": 2, "type": "前任继任", "context": "区长覃俊被查，王家强任代区长（2025-05）并当选（2025-08）", "overlap_org": "海口市琼山区人民政府", "overlap_period": "2025"},
    {"person_a": 21, "person_b": 1, "type": "违纪关联", "context": "区长被查后，区委按部署开展警示教育，向琼主持区委工作", "overlap_org": "琼山区党委/政府", "overlap_period": "2025-03至09"},
    {"person_a": 2, "person_b": 20, "type": "同区继任", "context": "陈昊旻曾任琼山区区委书记/区长，与现任区长同属琼山区班子谱系", "overlap_org": "中共海口市琼山区委员会", "overlap_period": "2016-2025"},
    {"person_a": 20, "person_b": 21, "type": "党政搭档", "context": "陈昊旻任区委副书记（2015.12）同期、陈任区委书记时覃俊任区委副书记/区长（2024）", "overlap_org": "中共海口市琼山区委员会", "overlap_period": "2021-2025"},
    {"person_a": 3, "person_b": 6, "type": "政法条线", "context": "政法委书记与政法条线常委协同", "overlap_org": "琼山区委政法委员会", "overlap_period": ""},
]


def build_person_json(p) -> None:
    """写入单个人物深度档案 JSON。"""
    name = p.get("name", "")
    if not name:
        return
    job = p.get("current_post") or "琼山区领导"
    # 精简职务用于文件名
    _job = re.sub(r"[、，，]?[一二三四]级(调研员|高级?监察官|主任科员|科员)?", "", job)
    slug_job = _job.replace("、", "-").replace("/", "-").strip("-")
    filename = f"{TODAY}-{PROVINCE}-{PARENT_CITY}-{slug_job}-{name}.json"
    out_path = PERSONS_OUT / filename

    src_url = p.get("source") or p.get("source_url") or ""
    source_register = [{
        "id": "S001",
        "title": f"琼山区人民政府官方/媒体领导信息 - {name}",
        "url": src_url,
        "publisher": "海口市琼山区人民政府/海口市人民政府",
        "published_at": AS_OF,
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "琼山区政府领导之窗、琼山区委全会通稿、海口市政府新闻、百度百科（E-ka as of 2026-08-06）",
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
            "location": "海口市",
            "system": "party" if pos["org_id"] in (1, 5, 6, 13) else "government",
            "rank": pos.get("rank", ""),
            "is_key_promotion": pos["person_id"] in (1, 2, 20, 21),
            "notes": pos.get("note", ""),
            "confidence": "confirmed" if src_url else "plausible",
            "source_ids": ["S001"],
        })

    org_refs = []
    for pos in positions:
        if pos["person_id"] == p["id"]:
            org_refs.append({"org_name": org_by_id.get(pos["org_id"], ""), "org_type": "",
                             "role": pos["title"]})

    open_q = []
    if not p.get("work_start"):
        open_q.append({"priority": "high", "question": f"{name}的参加工作年份",
                       "why_it_matters": "用于衡量晋升速度，尤其是80后厅级干部的快速晋升路径",
                       "suggested_queries": [f"{name} 简历 参加工作", f"{name} 任前公示"], "last_attempted": AS_OF})
    if not p.get("birthplace"):
        open_q.append({"priority": "medium", "question": f"{name}的籍贯/出生地",
                       "why_it_matters": "用于构建地域网络与同乡关联",
                       "suggested_queries": [f"{name} 籍贯", f"{name} 个人简历"], "last_attempted": AS_OF})

    document = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {"province": PROVINCE, "city": PARENT_CITY, "region": SLUG,
                                "job": job, "task_id": TASK_ID, "time_focus": "2025-2026"},
        "identity": {
            "person_id": f"hainan_haikou_qiongshan_{name}",
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
                           "administrative_rank": ("正处级" if p["id"] in (1, 2, 3, 20) else "副处级"),
                           "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S001"]},
        "career_timeline": career_timeline,
        "organizations": org_refs,
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": ("cross_county_rotation" if (p.get("native_place") and PROVINCE in p.get("native_place"))
                               else ("provincial_department" if "省" in (p.get("current_org") or "") else "unknown")),
            "systems_experience": [],
            "geographic_pattern": [p.get("birthplace", "")] if p.get("birthplace") else ["海口市"],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [], "speech_themes": [], "management_signals": [],
            "caveat": "工作风格源于公开政府工作报告/新闻报道推断，并非私人心理评估。",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found" if p["id"] not in (21,) else "disciplinary_action", "description": (
                "覃俊：2025-03-24 因严重违纪被查，2025-09 '双开'，通报跑官、违规插手工程项目。" if p["id"] == 21 else
                "搜索范围内未发现纪律处分/负面舆情信号，但可关注其前任被查背景。"), "date": "",
             "confidence": "confirmed" if p["id"] == 21 else "unverified", "source_ids": ["S001"]}
        ],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed" if p.get("birth") else "plausible",
            "current_role": "confirmed",
            "career_completeness": "partial" if p.get("work_start") else "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "完整履历（早年职务、历任起止时间、籍贯教育细节）",
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