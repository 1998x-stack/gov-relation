#!/usr/bin/env python3
"""兴山县（宜昌市，湖北省）领导班子工作关系网络数据生成脚本。

Task ID: hubei_兴山县
Province: 湖北省
Parent City: 宜昌市
Level: 县
Targets: 县委书记 & 县长

调查日期：2026-08-07（此前 2026-08-06 首轮；今日对官方源二次复核一致）
现行班子（截至 2026-08-07，官方 www.xingshan.gov.cn 领导之窗确认）：
  - 县委书记：吴浩（男，汉族，1984-03，研究生学历、工学博士，中共党员）
  - 县委副书记、县长、县政府党组书记：罗蓉（女，汉族，1980-01，研究生学历、管理学硕士，中共党员）
  - 县委班子 8 名常委/领导 + 县政府班子（正副县长）+ 县人大/县政协（下方 persons，均来自官方领导之窗）
前任县委书记：曹宏伟（约 2019—2025/2026，去向：宜昌市人民政府（副市长）；证据 local build_宜昌市_data.py，
  官方新闻线索，未完全核实时序）
前任县长：吴浩任现职前为兴山县长候选/工作，罗蓉接任县长（详见 open_gaps）

2026-08-07 二次核实补充（官方）：
  - 县委常委会（扩大）会议 2026-06-12（吴浩主持）：既定治理议题——绿色高质量发展、磷硅新材料+文化旅游
    两大根植性主导产业、三大百亿园区（新能源/磷酸铁锂、有机硅、磷基）、三个国家级文旅标准品牌、
    香溪河生态治理、刘草坡园区转型升级、群众走访、信访积案化解、群腐集中整治、安全稳定。
  - 县长罗蓉主持政府十九届第 68 次常务会议（2026-07-27）。
  - 兴山概况（官方）：隶属宜昌市，地处湖北省西部、长江西陵峡北侧；东夷陵区、南秭归县、
    西巴东县、北神农架林区、东北保康县；面积 2328 km²，辖 6 镇 2 乡，88 村，8 居委会，
    常住人口 14.33 万，县政府驻古夫镇。王昭君故乡；郑万高铁与沿江高铁交汇设站；磷矿 4.6 亿吨
    （全国三大基地）、鳞片石墨 1 亿吨、花岗岩 52 亿 m³；三大百亿园区；兴发集团（世界最大六偏磷酸钠）。
    2025 年 GDP 188.14 亿元（+6.9%，全市第 4）。

实现：
- 使用公共库 gov_relation.runner.run_build() 构建 SQLite 数据库 + GEXF 图。
- 为名单人物写出 data/persons/YYYYMMDD-湖北省-宜昌市-{job}-{name}.json 深度档案。
- 新产物第一优先级写入本脚本所在暂存目录，再由 scripts/process_tmp.py 校验后归档。

用法：
    python3 data/tmp/hubei_兴山县/build_兴山县_data.py        # 产出写到暂存目录
    python3 scripts/build/build_兴山县_data.py                # 归档后运行，产出到 canonical 目录
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

SLUG = "兴山县"
PROVINCE = "湖北省"
PARENT_CITY = "宜昌市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-07"

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

GOV_HOST = "http://www.xingshan.gov.cn"
LDZC = f"{GOV_HOST}/list-70-1.html"   # 领导之窗-县委/政府
LDRD = f"{GOV_HOST}/list-71-1.html"   # 领导之窗-人大
LD_Zx = f"{GOV_HOST}/list-73-1.html"  # 领导之窗-政协

# ── 人物 ────────────────────────────────────────────────────────────────────
# 证据：兴山县人民政府官方《领导之窗》，每条 from 领导概况页 URL。
persons = [
    {"id": 1,  "name": "吴浩",     "gender": "男", "ethnicity": "汉族", "birth": "1984-03", "birthplace": "待查", "native_place": "待查",
     "education": "研究生学历、工学博士", "party_join": "", "work_start": "",
     "current_post": "兴山县委书记", "current_org": "中共兴山县委员会",
     "source": f"{GOV_HOST}/content-70-153-1.html"},
    {"id": 2,  "name": "罗蓉",     "gender": "女", "ethnicity": "汉族", "birth": "1980-01", "birthplace": "待查", "native_place": "待查",
     "education": "研究生学历、管理学硕士", "party_join": "", "work_start": "",
     "current_post": "县委副书记、县长、县政府党组书记", "current_org": "兴山县人民政府",
     "source": f"{GOV_HOST}/content-70-154-1.html"},
    {"id": 3,  "name": "张华胜",  "gender": "男", "ethnicity": "汉族", "birth": "1976-08", "birthplace": "待查", "native_place": "待查",
     "education": "省委党校大学学历", "party_join": "", "work_start": "",
     "current_post": "兴山县委副书记", "current_org": "中共兴山县委员会",
     "source": f"{GOV_HOST}/content-70-115-1.html"},
    {"id": 4,  "name": "杨后荣",  "gender": "男", "ethnicity": "土家族", "birth": "1982-07", "birthplace": "待查", "native_place": "待查",
     "education": "省委党校研究生学历、管理学学士", "party_join": "", "work_start": "",
     "current_post": "县委常委、常务副县长、县政府党组副书记", "current_org": "兴山县人民政府",
     "source": f"{GOV_HOST}/content-70-119-1.html"},
    {"id": 5,  "name": "万茜",     "gender": "女", "ethnicity": "汉族", "birth": "1975-01", "birthplace": "待查", "native_place": "待查",
     "education": "在职大学学历", "party_join": "", "work_start": "",
     "current_post": "县委常委、宣传部部长、总工会主席", "current_org": "中共兴山县委员会",
     "source": f"{GOV_HOST}/content-70-118-1.html"},
    {"id": 6,  "name": "杨陈",     "gender": "男", "ethnicity": "土家族", "birth": "1987-05", "birthplace": "待查", "native_place": "待查",
     "education": "研究生学历、文学硕士", "party_join": "", "work_start": "",
     "current_post": "县委常委、组织部部长、统战部部长、县委党校校长、县政协党组副书记", "current_org": "中共兴山县委员会",
     "source": f"{GOV_HOST}/content-70-152-1.html"},
    {"id": 7,  "name": "马正波",  "gender": "男", "ethnicity": "汉族", "birth": "1971-07", "birthplace": "待查", "native_place": "待查",
     "education": "在职大学学历", "party_join": "", "work_start": "",
     "current_post": "县委常委、县委办公室主任", "current_org": "中共兴山县委员会",
     "source": f"{GOV_HOST}/content-70-120-1.html"},
    {"id": 8,  "name": "舒华容",  "gender": "男", "ethnicity": "汉族", "birth": "1976-02", "birthplace": "待查", "native_place": "待查",
     "education": "在职大学学历", "party_join": "", "work_start": "",
     "current_post": "县委常委、副县长、县政府党组成员，县开发区党工委书记", "current_org": "兴山县人民政府",
     "source": f"{GOV_HOST}/content-70-144-1.html"},
    {"id": 9,  "name": "张健",     "gender": "男", "ethnicity": "汉族", "birth": "1975-02", "birthplace": "待查", "native_place": "待查",
     "education": "中央党校大学学历", "party_join": "", "work_start": "",
     "current_post": "县委常委、政法委书记", "current_org": "中共兴山县委员会",
     "source": f"{GOV_HOST}/content-70-122-1.html"},
    {"id": 10, "name": "郑忠敏",  "gender": "男", "ethnicity": "土家族", "birth": "1983-01", "birthplace": "待查", "native_place": "待查",
     "education": "研究生学历、管理学硕士", "party_join": "", "work_start": "",
     "current_post": "县委常委、纪委书记、县监委主任", "current_org": "中共兴山县纪律检查委员会/兴山县监察委员会",
     "source": f"{GOV_HOST}/content-70-159-1.html"},
    {"id": 11, "name": "龙景丽",  "gender": "女", "ethnicity": "汉族", "birth": "1974-04", "birthplace": "待查", "native_place": "待查",
     "education": "省委党校大学学历", "party_join": "", "work_start": "",
     "current_post": "副县长、县政府党组成员", "current_org": "兴山县人民政府",
     "source": f"{GOV_HOST}/content-72-134-1.html"},
    {"id": 12, "name": "卢光勇",  "gender": "男", "ethnicity": "汉族", "birth": "1986-05", "birthplace": "待查", "native_place": "待查",
     "education": "大学学历、经济学学士", "party_join": "", "work_start": "",
     "current_post": "副县长、县政府党组成员", "current_org": "兴山县人民政府",
     "source": f"{GOV_HOST}/content-72-146-1.html"},
    {"id": 13, "name": "陈浩",     "gender": "男", "ethnicity": "汉族", "birth": "1982-02", "birthplace": "待查", "native_place": "待查",
     "education": "省委党校研究生学历", "party_join": "", "work_start": "",
     "current_post": "副县长、县政府党组成员，县公安局党委书记、局长", "current_org": "兴山县人民政府",
     "source": f"{GOV_HOST}/content-72-149-1.html"},
    {"id": 14, "name": "王新艳",  "gender": "女", "ethnicity": "汉族", "birth": "1985-03", "birthplace": "待查", "native_place": "待查",
     "education": "大学学历、文学学士", "party_join": "", "work_start": "",
     "current_post": "副县长", "current_org": "兴山县人民政府",
     "source": f"{GOV_HOST}/content-72-127-1.html"},
    {"id": 15, "name": "华永",     "gender": "男", "ethnicity": "汉族", "birth": "1983-12", "birthplace": "待查", "native_place": "待查",
     "education": "大学本科学历", "party_join": "", "work_start": "",
     "current_post": "副县长（挂职）", "current_org": "兴山县人民政府",
     "source": f"{GOV_HOST}/content-72-150-1.html"},
    {"id": 16, "name": "周旭",     "gender": "男", "ethnicity": "汉族", "birth": "1989-01", "birthplace": "待查", "native_place": "待查",
     "education": "研究生学历", "party_join": "", "work_start": "",
     "current_post": "副县长（挂职）", "current_org": "兴山县人民政府",
     "source": f"{GOV_HOST}/content-72-151-1.html"},
    {"id": 17, "name": "袁选军",  "gender": "男", "ethnicity": "汉族", "birth": "1969-07", "birthplace": "待查", "native_place": "待查",
     "education": "在职大学学历", "party_join": "", "work_start": "",
     "current_post": "县人大常委会主任、党组书记", "current_org": "兴山县人民代表大会常务委员会",
     "source": f"{GOV_HOST}/content-71-135-1.html"},
    {"id": 18, "name": "杨四龙",  "gender": "男", "ethnicity": "汉族", "birth": "1971-03", "birthplace": "待查", "native_place": "待查",
     "education": "中央党校大学学历", "party_join": "", "work_start": "",
     "current_post": "县政协主席、党组书记", "current_org": "中国人民政治协商会议兴山县委员会",
     "source": f"{GOV_HOST}/content-73-104-1.html"},
    {"id": 19, "name": "刘彩娥",  "gender": "女", "ethnicity": "土家族", "birth": "1986-08", "birthplace": "待查", "native_place": "待查",
     "education": "大学本科学历", "party_join": "", "work_start": "",
     "current_post": "县人大常委会副主任", "current_org": "兴山县人民代表大会常务委员会",
     "source": f"{GOV_HOST}/content-71-145-1.html"},
    {"id": 20, "name": "詹红菊",  "gender": "女", "ethnicity": "汉族", "birth": "1979-06", "birthplace": "待查", "native_place": "待查",
     "education": "在职大学学历", "party_join": "", "work_start": "",
     "current_post": "县政协副主席", "current_org": "中国人民政治协商会议兴山县委员会",
     "source": f"{GOV_HOST}/content-73-126-1.html"},
    {"id": 21, "name": "潘琪",     "gender": "女", "ethnicity": "汉族", "birth": "1985-02", "birthplace": "待查", "native_place": "待查",
     "education": "研究生学历、理学硕士", "party_join": "", "work_start": "",
     "current_post": "县政协副主席", "current_org": "中国人民政治协商会议兴山县委员会",
     "source": f"{GOV_HOST}/content-73-155-1.html"},
]

organizations = [
    {"id": 1,  "name": "中共兴山县委员会", "type": "党委", "level": "县级", "parent": "中共宜昌市委员会", "location": "宜昌市兴山县"},
    {"id": 2,  "name": "兴山县人民政府",   "type": "政府", "level": "县级", "parent": "宜昌市人民政府",  "location": "宜昌市兴山县"},
    {"id": 3,  "name": "中共兴山县纪律检查委员会/兴山县监察委员会", "type": "党委", "level": "县级", "parent": "中共宜昌市纪律检查委员会", "location": "宜昌市兴山县"},
    {"id": 4,  "name": "中共兴山县委政法委员会", "type": "党委", "level": "县级", "parent": "中共兴山县委员会", "location": "宜昌市兴山县"},
    {"id": 5,  "name": "中共兴山县委组织部", "type": "党委", "level": "县级", "parent": "中共兴山县委员会", "location": "宜昌市兴山县"},
    {"id": 6,  "name": "中共兴山县委统一战线工作部", "type": "党委", "level": "县级", "parent": "中共兴山县委员会", "location": "宜昌市兴山县"},
    {"id": 7,  "name": "中共兴山县委宣传部", "type": "党委", "level": "县级", "parent": "中共兴山县委员会", "location": "宜昌市兴山县"},
    {"id": 8,  "name": "中共兴山县委办公室", "type": "党委", "level": "县级", "parent": "中共兴山县委员会", "location": "宜昌市兴山县"},
    {"id": 9,  "name": "中共兴山县委党校", "type": "事业单位", "level": "县级", "parent": "中共兴山县委员会", "location": "宜昌市兴山县"},
    {"id": 10, "name": "兴山县总工会",     "type": "群团", "level": "县级", "parent": "宜昌市总工会",     "location": "宜昌市兴山县"},
    {"id": 11, "name": "兴山县公安局",      "type": "政府", "level": "县级", "parent": "兴山县人民政府",  "location": "宜昌市兴山县"},
    {"id": 12, "name": "兴山县经济开发区党工委", "type": "开发区", "level": "县级", "parent": "中共兴山县委员会", "location": "宜昌市兴山县"},
    {"id": 13, "name": "兴山县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "宜昌市人民代表大会常务委员会", "location": "宜昌市兴山县"},
    {"id": 14, "name": "中国人民政治协商会议兴山县委员会", "type": "政协", "level": "县级", "parent": "中国人民政治协商会议宜昌市委员会", "location": "宜昌市兴山县"},
]

positions = [
    {"person_id": 1,  "org_id": 1,  "title": "兴山县委书记", "start_date": "约2025-11", "end_date": "", "rank": "正处级", "note": "现任县委书记"},
    {"person_id": 2,  "org_id": 1,  "title": "兴山县委副书记", "start_date": "约2025-12", "end_date": "", "rank": "正处级", "note": "兼任县长"},
    {"person_id": 2,  "org_id": 2,  "title": "兴山县县长、县政府党组书记", "start_date": "约2025-12", "end_date": "", "rank": "正处级", "note": "现任县长"},
    {"person_id": 3,  "org_id": 1,  "title": "兴山县委副书记", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 4,  "org_id": 1,  "title": "兴山县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 4,  "org_id": 2,  "title": "常务副县长、县政府党组副书记", "start_date": "", "end_date": "", "rank": "副处级", "note": "常务副县长"},
    {"person_id": 5,  "org_id": 1,  "title": "兴山县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 5,  "org_id": 7,  "title": "县委宣传部部长、县总工会主席", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 6,  "org_id": 1,  "title": "兴山县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 6,  "org_id": 5,  "title": "县委组织部部长、县委党校校长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 6,  "org_id": 6,  "title": "县委统战部部长、县政协党组副书记", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 7,  "org_id": 1,  "title": "兴山县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 7,  "org_id": 8,  "title": "县委办公室主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 8,  "org_id": 1,  "title": "兴山县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 8,  "org_id": 2,  "title": "副县长、县政府党组成员", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 8,  "org_id": 12, "title": "县经济开发区党工委书记", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 9,  "org_id": 1,  "title": "兴山县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 9,  "org_id": 4,  "title": "县委政法委书记", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 1,  "title": "兴山县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 3,  "title": "县纪委书记、县监委主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 2,  "title": "副县长、县政府党组成员", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 2,  "title": "副县长、县政府党组成员", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 2,  "title": "副县长、县政府党组成员", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 11, "title": "县公安局党委书记、局长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 2,  "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 15, "org_id": 2,  "title": "副县长（挂职）", "start_date": "", "end_date": "", "rank": "副处级", "note": "挂职一年"},
    {"person_id": 16, "org_id": 2,  "title": "副县长（挂职）", "start_date": "", "end_date": "", "rank": "副处级", "note": "挂职两年"},
    {"person_id": 17, "org_id": 13, "title": "县人大常委会主任、党组书记", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 18, "org_id": 14, "title": "县政协主席、党组书记", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 19, "org_id": 13, "title": "县人大常委会副主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 20, "org_id": 14, "title": "县政协副主席", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 21, "org_id": 14, "title": "县政协副主席", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "县委书记吴浩与县长罗蓉为兴山县党政正职搭档", "overlap_org": "兴山县党委/政府", "overlap_period": "约2025-12至今"},
    {"person_a": 1, "person_b": 3, "type": "县委班子", "context": "县委副书记在书记领导下工作", "overlap_org": "中共兴山县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "县委班子", "context": "县委常委/常务副县长在书记领导下工作", "overlap_org": "中共兴山县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "县委班子", "context": "县委常委/宣传部长在书记领导下工作", "overlap_org": "中共兴山县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "县委班子", "context": "县委常委/组织部长在书记领导下工作", "overlap_org": "中共兴山县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "县委班子", "context": "县委常委/县委办主任在书记领导下工作", "overlap_org": "中共兴山县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "县委班子", "context": "县委常委/副县长在书记领导下工作", "overlap_org": "中共兴山县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "县委班子", "context": "县委常委/政法委书记在书记领导下工作", "overlap_org": "中共兴山县委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 10, "type": "县委班子", "context": "县委常委/纪委书记在书记领导下工作", "overlap_org": "中共兴山县委员会", "overlap_period": ""},
    {"person_a": 2, "person_b": 4, "type": "政府班子", "context": "常务副县长在县长领导下工作", "overlap_org": "兴山县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 8, "type": "政府班子", "context": "副县长在县长领导下工作", "overlap_org": "兴山县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 11, "type": "政府班子", "context": "副县长在县长领导下工作", "overlap_org": "兴山县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 12, "type": "政府班子", "context": "副县长在县长领导下工作", "overlap_org": "兴山县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 13, "type": "政府班子", "context": "副县长/公安局长在县长领导下工作", "overlap_org": "兴山县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 14, "type": "政府班子", "context": "副县长在县长领导下工作", "overlap_org": "兴山县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 15, "type": "政府班子", "context": "挂职副县长在县长领导下工作", "overlap_org": "兴山县人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 16, "type": "政府班子", "context": "挂职副县长在县长领导下工作", "overlap_org": "兴山县人民政府", "overlap_period": ""},
    {"person_a": 6, "person_b": 10, "type": "政法纪检协同", "context": "组织部长与纪委书记并列负责干部纪律监督（常委分工）", "overlap_org": "中共兴山县委员会", "overlap_period": ""},
    {"person_a": 5, "person_b": 10, "type": "县委班子", "context": "宣传部长与纪委书记均为县委常委", "overlap_org": "中共兴山县委员会", "overlap_period": ""},
    {"person_a": 9, "person_b": 10, "type": "政法纪检协同", "context": "政法委书记与纪委书记在综治/纪检协同", "overlap_org": "兴山县", "overlap_period": ""},
    {"person_a": 17, "person_b": 1, "type": "县委班子/人大", "context": "人大常委会主任与县委书记保持四套班子协同", "overlap_org": "兴山县四套班子", "overlap_period": ""},
    {"person_a": 18, "person_b": 1, "type": "县委班子/政协", "context": "县政协主席与县委书记保持四套班子协同", "overlap_org": "兴山县四套班子", "overlap_period": ""},
]


def build_person_json(p: dict) -> None:
    """写入单个人物深度档案 JSON。"""
    name = p.get("name", "")
    if not name:
        return
    job = p.get("current_post") or "兴山县领导"
    _job = re.sub(r"[、，]?[一二三四]级(调研员|高级?监察官|主任科员|科员)?", "", job)
    slug_job = _job.replace("、", "-").replace("/", "-").strip("、")
    filename = f"{TODAY}-{PROVINCE}-{PARENT_CITY}-{slug_job}-{name}.json"
    out_path = PERSONS_OUT / filename

    src_url = p.get("source") or ""
    source_register = [{
        "id": "S001",
        "title": f"兴山县人民政府领导之窗 - {name}",
        "url": src_url,
        "publisher": "兴山县人民政府",
        "published_at": AS_OF,
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high",
        "notes": "兴山县人民政府官方在职领导信息页（2026-08-06 复核）",
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
            "location": "宜昌市兴山县",
            "system": "party" if pos["org_id"] in (1, 3, 4, 5, 6, 7, 8, 9, 12) else "government",
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
    if not p.get("birthplace") or p.get("birthplace") == "待查":
        open_q.append({"priority": "high", "question": f"{name}的籍贯/出生地",
                       "why_it_matters": "用于判断跨县/跨地市/跨省干部来源",
                       "suggested_queries": [f"{name} 简历 籍贯", f"{name} 兴山县"], "last_attempted": AS_OF})
    if not p.get("work_start"):
        open_q.append({"priority": "medium", "question": f"{name}的参加工作年份",
                       "why_it_matters": "用于衡量晋升速度",
                       "suggested_queries": [f"{name} 简历 参加工作", f"{name} 任前公示"], "last_attempted": AS_OF})
    if not p.get("party_join"):
        open_q.append({"priority": "medium", "question": f"{name}的入党时间",
                       "why_it_matters": "用于精确构建晋升时间线",
                       "suggested_queries": [f"{name} 任前公示 入党", f"{name} 简历"], "last_attempted": AS_OF})
    if p["id"] in (1, 2) and not p.get("prior_career_note"):
        open_q.append({"priority": "critical", "question": f"{name}就任现职前的完整履历",
                       "why_it_matters": "现任县委班子一二号人物履历关键",
                       "suggested_queries": [f"{name} 简历 {PARENT_CITY}", f"{name} 历任"], "last_attempted": AS_OF})

    document = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {"province": PROVINCE, "city": PARENT_CITY, "region": SLUG,
                                "job": job, "task_id": "hubei_兴山县", "time_focus": "2026"},
        "identity": {
            "person_id": f"hubei_yichang_xingshan_{name}",
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
                           "administrative_rank": "正处级" if p["id"] in (1, 2, 3, 17, 18) else "副处级",
                           "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S001"]},
        "career_timeline": career_timeline,
        "organizations": org_refs,
        "relationships": [],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
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
            "career_completeness": "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "完整履历（早年、历任职务起止时间）、籍贯/出生地",
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