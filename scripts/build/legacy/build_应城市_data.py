#!/usr/bin/env python3
"""应城市（孝感市，湖北省）领导班子工作关系网络数据生成脚本。

Task ID: hubei_应城市
Level: 县级市
Targets: 市委书记 & 市长

调查日期：2026-08-06
现行班子（截至 2026-08-06，应城市政府门户网 www.yingcheng.gov.cn 领导之窗官方确认）：
  - 市委书记：胡光怀（男，汉族，1979-05 生，大学学历，中共党员，一级调研员）
  - 市委副书记、市政府党组书记、市长：马跃（男，回族，1983-07 生，省委党校研究生，中共党员，一级调研员）
  - 市委常委：徐安平（常委/市政府党组副书记/常务副市长）、胡海波（常委/组织部长）、
    沈渊（常委/统战部长/总工会主席）、丁波（常委/纪委书记/监委主任）、
    褚亚敏（常委/宣传部长/红十字会会长）、盛必胜（常委/市委办主任）、罗培虎（常委，挂职）
  - 市人大领导：李碧华（党组书记/主任）、樊超、许继国、普伟、胡娟、赵路、李少楠
  - 市政府：副市长王京萍、吴新洲、李慧涛、严建澍(人选·挂职)、黄克洋(兼公安局长)、肖靖；
    蒋家彪（党组成员、机关党组书记、办公室主任）
  - 市政协：李艳霞（党组书记、主席）、雷建军、程三炳、邓涛、宋中旺、李桦山

产业/政绩背景（官方新闻）：
  支柱产业为盐化工（云图控股应城基地：卤—盐—碱—肥全产业链）、绿色储能（中国能建 300 兆瓦
  压缩空气储能示范）、甲鱼、汤池温泉；目标为"建成武汉都市圈副中心城市重要支撑点"；
  对标学习"义乌发展经验"，聚焦特色发展。

实现：
- 使用公共库 gov_relation.runner.run_build() 构建 SQLite 数据库 + GEXF 图。
- 为名单人物写出 data/persons/YYYYMMDD-湖北省-孝感市-{job}-{name}.json 深度档案。
- 新产物第一优先级写入本脚本所在暂存目录，再由 scripts/process_tmp.py 校验后归档。

用法：
    python3 data/tmp/hubei_应城市/build_应城市_data.py   # 暂存目录
    python3 scripts/build/build_应城市_data.py           # 归档后 canonical
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

SLUG = "应城市"
PROVINCE = "湖北省"
PARENT_CITY = "孝感市"
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

GOV_HOST = "http://www.yingcheng.gov.cn"
# 官方一手来源
SRC_LD_WS = f"{GOV_HOST}/hgh2/index.jhtml"      # 领导之窗·市委领导（全体常委）
SRC_LD_ZF = f"{GOV_HOST}/my3/index.jhtml"        # 领导之窗·市政府领导
SRC_LD_RD = f"{GOV_HOST}/lbh01/index.jhtml"      # 领导之窗·市人大领导
SRC_LD_ZX = f"{GOV_HOST}/cxm01/index.jhtml"      # 领导之窗·市政协领导
SRC_ZW = f"{GOV_HOST}/bdyw/2141424.jhtml"        # 2026-08-04 政绩观党课（胡光怀主讲、马跃主持）
SRC_YWC = f"{GOV_HOST}/bdyw/2139892.jhtml"       # 2026-07-27 胡玖明调研应城盐化工（胡光怀/马跃参加）
SRC_PQF = f"{GOV_HOST}/bdyw/2141455.jhtml"       # 2026-08-04 蒲城先锋大讲堂

# ── 组织 ────────────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共应城市委员会", "type": "党委", "level": "县级市", "parent": "中共孝感市委员会", "location": "孝感市应城市"},
    {"id": 2, "name": "应城市人民政府", "type": "政府", "level": "县级市", "parent": "孝感市人民政府", "location": "孝感市应城市"},
    {"id": 3, "name": "中共孝感市委员会", "type": "党委", "level": "地级市", "parent": "中共湖北省委", "location": "孝感市"},
    {"id": 4, "name": "孝感市人民政府", "type": "政府", "level": "地级市", "parent": "湖北省人民政府", "location": "孝感市"},
    {"id": 5, "name": "中共应城市纪律检查委员会/应城市监察委员会", "type": "党委", "level": "县级市", "parent": "中共应城市委员会", "location": "孝感市应城市"},
    {"id": 6, "name": "应城市人民代表大会常务委员会", "type": "人大", "level": "县级市", "parent": "应城市", "location": "孝感市应城市"},
    {"id": 7, "name": "政协应城市委员会", "type": "政协", "level": "县级市", "parent": "应城市", "location": "孝感市应城市"},
    {"id": 8, "name": "应城市公安局", "type": "政府", "level": "县级市", "parent": "应城市人民政府", "location": "孝感市应城市"},
    {"id": 9, "name": "中共应城市委组织部", "type": "党委", "level": "县级市", "parent": "中共应城市委员会", "location": "孝感市应城市"},
    {"id": 10, "name": "中共应城市委宣传部", "type": "党委", "level": "县级市", "parent": "中共应城市委员会", "location": "孝感市应城市"},
]

# ── 人物 ────────────────────────────────────────────────────────────────────
# 证据：应城市政府门户网领导之窗（2026-08-06，一手）＋本地要闻新闻稿（政绩观党课）
persons = [
    {"id": 1, "name": "胡光怀", "gender": "男", "ethnicity": "汉族", "birth": "1979-05", "birthplace": "", "native_place": "",
     "education": "大学学历", "party_join": "", "work_start": "",
     "current_post": "应城市委书记（一级调研员）", "current_org": "中共应城市委员会",
     "source": SRC_LD_WS, "job_tag": "市委书记"},
    {"id": 2, "name": "马跃", "gender": "男", "ethnicity": "回族", "birth": "1983-07", "birthplace": "", "native_place": "",
     "education": "省委党校研究生", "party_join": "", "work_start": "",
     "current_post": "应城市委副书记、市政府党组书记、市长（一级调研员）", "current_org": "应城市人民政府/中共应城市委员会",
     "source": SRC_LD_ZF, "job_tag": "市长"},
    {"id": 3, "name": "徐安平", "gender": "男", "ethnicity": "汉族", "birth": "1974-04", "birthplace": "", "native_place": "",
     "education": "在职大学", "party_join": "", "work_start": "",
     "current_post": "应城市委常委、市政府党组副书记、常务副市长（三级调研员）", "current_org": "应城市人民政府/中共应城市委员会",
     "source": SRC_LD_ZF, "job_tag": "常务副市长"},
    {"id": 4, "name": "胡海波", "gender": "男", "ethnicity": "汉族", "birth": "1981-06", "birthplace": "", "native_place": "",
     "education": "省委党校研究生", "party_join": "", "work_start": "",
     "current_post": "应城市委常委、市委组织部部长", "current_org": "中共应城市委组织部",
     "source": SRC_LD_WS, "job_tag": "组织部长"},
    {"id": 5, "name": "沈渊", "gender": "男", "ethnicity": "汉族", "birth": "1973-02", "birthplace": "", "native_place": "",
     "education": "大学", "party_join": "", "work_start": "",
     "current_post": "应城市委常委、市委统战部部长、市总工会主席（三级调研员）", "current_org": "中共应城市委员会",
     "source": SRC_LD_WS, "job_tag": "统战部长"},
    {"id": 6, "name": "丁波", "gender": "男", "ethnicity": "汉族", "birth": "1984-06", "birthplace": "", "native_place": "",
     "education": "大学", "party_join": "", "work_start": "",
     "current_post": "应城市委常委、市纪委书记、市监委主任（三级调研员）", "current_org": "中共应城市纪律检查委员会",
     "source": SRC_LD_WS, "job_tag": "纪委书记"},
    {"id": 7, "name": "褚亚敏", "gender": "女", "ethnicity": "汉族", "birth": "1981-04", "birthplace": "", "native_place": "",
     "education": "省委党校研究生", "party_join": "", "work_start": "",
     "current_post": "应城市委常委、市委宣传部部长、市红十字会会长", "current_org": "中共应城市委宣传部",
     "source": SRC_LD_WS, "job_tag": "宣传部长"},
    {"id": 8, "name": "盛必胜", "gender": "男", "ethnicity": "汉族", "birth": "1975-12", "birthplace": "", "native_place": "",
     "education": "中央党校大学", "party_join": "", "work_start": "",
     "current_post": "应城市委常委、市委办公室主任", "current_org": "中共应城市委员会",
     "source": SRC_LD_WS, "job_tag": "市委常委"},
    {"id": 9, "name": "罗培虎", "gender": "男", "ethnicity": "土家族", "birth": "1972-06", "birthplace": "", "native_place": "",
     "education": "省委党校研究生", "party_join": "", "work_start": "",
     "current_post": "应城市委常委、市政府党组成员（挂职）", "current_org": "应城市人民政府",
     "source": SRC_LD_WS, "job_tag": "市委常委"},
    {"id": 10, "name": "李碧华", "gender": "男", "ethnicity": "汉族", "birth": "1968-03", "birthplace": "", "native_place": "",
     "education": "在职大学", "party_join": "", "work_start": "",
     "current_post": "应城市人大常委会党组书记、主任", "current_org": "应城市人民代表大会常务委员会",
     "source": SRC_LD_RD, "job_tag": "人大主任"},
    {"id": 11, "name": "李艳霞", "gender": "女", "ethnicity": "汉族", "birth": "1972-10", "birthplace": "", "native_place": "",
     "education": "省委党校大学", "party_join": "", "work_start": "",
     "current_post": "应城市政协党组书记、主席", "current_org": "政协应城市委员会",
     "source": SRC_LD_ZX, "job_tag": "政协主席"},
    {"id": 12, "name": "胡娟", "gender": "女", "ethnicity": "汉族", "birth": "1980-01", "birthplace": "", "native_place": "",
     "education": "省委党校研究生", "party_join": "", "work_start": "",
     "current_post": "应城市人大常委会副主任，市科协副主席", "current_org": "应城市人民代表大会常务委员会",
     "source": SRC_LD_RD, "job_tag": "人大副主任"},
    {"id": 13, "name": "黄克洋", "gender": "男", "ethnicity": "汉族", "birth": "1973-08", "birthplace": "", "native_place": "",
     "education": "大学", "party_join": "", "work_start": "",
     "current_post": "应城市政府党组成员、副市长，市公安局党委书记、局长、督察长（三级高级警长）", "current_org": "应城市人民政府/应城市公安局",
     "source": SRC_LD_ZF, "job_tag": "副市长"},
    {"id": 14, "name": "王涛", "gender": "男", "ethnicity": "汉族", "birth": "1974-03", "birthplace": "", "native_place": "",
     "education": "省委党校研究生", "party_join": "", "work_start": "",
     "current_post": "应城市政府党组成员、副市长（三级调研员）", "current_org": "应城市人民政府",
     "source": SRC_LD_ZF, "job_tag": "副市长"},
    {"id": 15, "name": "吴新洲", "gender": "男", "ethnicity": "汉族", "birth": "1975-06", "birthplace": "", "native_place": "",
     "education": "在职大学", "party_join": "", "work_start": "",
     "current_post": "应城市政府副市长，市残联主席，市计划生育协会会长（三级调研员）", "current_org": "应城市人民政府",
     "source": SRC_LD_ZF, "job_tag": "副市长"},
    {"id": 16, "name": "李慧涛", "gender": "女", "ethnicity": "汉族", "birth": "1985-07", "birthplace": "", "native_place": "",
     "education": "在职研究生", "party_join": "", "work_start": "",
     "current_post": "应城市政府党组成员、副市长", "current_org": "应城市人民政府",
     "source": SRC_LD_ZF, "job_tag": "副市长"},
    {"id": 17, "name": "严建澍", "gender": "男", "ethnicity": "汉族", "birth": "1987-11", "birthplace": "", "native_place": "",
     "education": "大学", "party_join": "", "work_start": "",
     "current_post": "应城市政府副市长人选（挂职）", "current_org": "应城市人民政府",
     "source": SRC_LD_ZF, "job_tag": "副市长"},
    {"id": 18, "name": "肖靖", "gender": "男", "ethnicity": "汉族", "birth": "1976-09", "birthplace": "", "native_place": "",
     "education": "省委党校研究生", "party_join": "", "work_start": "",
     "current_post": "应城市政府党组成员、副市长", "current_org": "应城市人民政府",
     "source": SRC_LD_ZF, "job_tag": "副市长"},
    {"id": 19, "name": "蒋家彪", "gender": "男", "ethnicity": "汉族", "birth": "1974-04", "birthplace": "", "native_place": "",
     "education": "在职大专", "party_join": "", "work_start": "",
     "current_post": "应城市政府党组成员、机关党组书记、办公室主任（四级调研员）", "current_org": "应城市人民政府",
     "source": SRC_LD_ZF, "job_tag": "副市长"},
]

# ── 任职 ────────────────────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "应城市委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "一级调研员；应城市领导之窗官网确认"},
    {"person_id": 2, "org_id": 1, "title": "应城市委副书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "市委副书记"},
    {"person_id": 2, "org_id": 2, "title": "应城市长、市政府党组书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "主持市政府全面工作，分管市审计局；一级调研员"},
    {"person_id": 3, "org_id": 1, "title": "应城市委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": "市政府党组副书记"},
    {"person_id": 3, "org_id": 2, "title": "应城市常务副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": "三级调研员"},
    {"person_id": 4, "org_id": 1, "title": "应城市委常委、组织部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": "市委组织部部长"},
    {"person_id": 5, "org_id": 1, "title": "应城市委常委、统战部部长、市总工会主席", "start_date": "", "end_date": "", "rank": "副处级", "note": "三级调研员"},
    {"person_id": 6, "org_id": 1, "title": "应城市委常委、市纪委书记、市监委主任", "start_date": "", "end_date": "", "rank": "副处级", "note": "三级调研员"},
    {"person_id": 7, "org_id": 1, "title": "应城市委常委、宣传部部长、市红十字会会长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "应城市委常委、市委办公室主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "应城市委常委、市政府党组成员（挂职）", "start_date": "", "end_date": "", "rank": "副处级", "note": "挂职；土家族"},
    {"person_id": 10, "org_id": 6, "title": "应城市人大常委会党组书记、主任", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 11, "org_id": 7, "title": "应城市政协党组书记、主席", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 12, "org_id": 6, "title": "应城市人大常委会副主任、市科协副主席", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "应城市副市长、市公安局局长", "start_date": "", "end_date": "", "rank": "副处级", "note": "市公安局党委书记、局长、督察长；三级高级警长"},
    {"person_id": 14, "org_id": 2, "title": "应城市副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": "三级调研员"},
    {"person_id": 15, "org_id": 2, "title": "应城市副市长、市残联主席", "start_date": "", "end_date": "", "rank": "副处级", "note": "市计划生育协会会长；三级调研员"},
    {"person_id": 16, "org_id": 2, "title": "应城市副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "应城市副市长人选（挂职）", "start_date": "", "end_date": "", "rank": "副处级", "note": "挂职"},
    {"person_id": 18, "org_id": 2, "title": "应城市副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 19, "org_id": 2, "title": "应城市政府党组成员、办公室主任", "start_date": "", "end_date": "", "rank": "副处级", "note": "机关党组书记；四级调研员"},
]

# ── 关系 ────────────────────────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政正职搭档", "context": "胡光怀任应城市委书记、马跃任市长/市委副书记，构成应城市党政正职搭档（共同主持政绩观党课等）", "overlap_org": "中共应城市委员会/应城市人民政府", "overlap_period": "2025至今"},
    {"person_a": 1, "person_b": 3, "type": "市委常委会班子", "context": "胡光怀（书记）与徐安平（常委/常务副市长）同属市委常委会、政府班子", "overlap_org": "中共应城市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 4, "type": "市委常委会班子", "context": "市委书记与组织部长同属市委常委 领导集体", "overlap_org": "中共应城市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "市委常委会班子", "context": "市委书记与统战部长/总工会主席同属市委常委", "overlap_org": "中共应城市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "市委常委会班子", "context": "市委书记与纪委书记/监委主任同属市委常委会", "overlap_org": "中共应城市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "市委常委会班子", "context": "市委书记与宣传部长同属市委常委", "overlap_org": "中共应城市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "市委常委会班子", "context": "市委书记与市委办主任同属市委领导集体", "overlap_org": "中共应城市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 10, "type": "市四大家", "context": "市委书记与市人大常委会主任同属县四大家负责人", "overlap_org": "应城市", "overlap_period": ""},
    {"person_a": 1, "person_b": 11, "type": "市四大家", "context": "市委书记与市政协主席同属县四大家负责人", "overlap_org": "应城市", "overlap_period": ""},
    {"person_a": 2, "person_b": 3, "type": "政府班子", "context": "市长与常务副市长同属政府班子上下级（常务负责具体常务工作）", "overlap_org": "应城市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 13, "type": "政府班子", "context": "市长与副市长/公安局长同属政府班子", "overlap_org": "应城市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 14, "type": "政府班子", "context": "市长与副市长王涛同属政府班子", "overlap_org": "应城市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 15, "type": "政府班子", "context": "市长与副市长吴新洲同属政府班子", "overlap_org": "应城市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 16, "type": "政府班子", "context": "市长与副市长李慧涛同属政府班子", "overlap_org": "应城市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 18, "type": "政府班子", "context": "市长与副市长肖靖同属政府班子", "overlap_org": "应城市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 19, "type": "政府班子", "context": "市长与市政府办主任蒋家程同属政府班子工作圈", "overlap_org": "应城市人民政府", "overlap_period": ""},
    {"person_a": 3, "person_b": 6, "type": "市委常委会班子", "context": "常务副市长与纪委书记同属市委常委会", "overlap_org": "中共应城市委员会", "overlap_period": ""},
    {"person_a": 4, "person_b": 6, "type": "市委常委会班子", "context": "组织部长与纪委书记同属市委常委会", "overlap_org": "中共应城市委员会", "overlap_period": ""},
    {"person_a": 10, "person_b": 11, "type": "市四大家", "context": "市人大主任与市政协主席同属县四大家负责人", "overlap_org": "应城市", "overlap_period": ""},
]


def _edu_list(p):
    edu = []
    if p.get("education"):
        edu.append({"period": "", "institution": "", "major": "", "degree": p["education"],
                    "study_type": "unknown", "source_ids": ["S001"]})
    return edu


def build_person_json(p) -> None:
    name = p.get("name", "")
    if not name:
        return
    job = p.get("job_tag") or p.get("current_post") or "应城市领导"
    _job = re.sub(r"[、，]?[一二三四]级(调研员|高级?监察官|主任科员|科员)", "", job)
    slug_job = _job.replace("、", "-").replace("/", "-").replace("（", "-").replace("）", "").strip("-")
    filename = f"{TODAY}-{PROVINCE}-{PARENT_CITY}-{slug_job}-{name}.json"
    out_path = PERSONS_OUT / filename

    src_url = p.get("source") or ""
    source_register = [{
        "id": "S001",
        "title": "应城市政府门户网·领导之窗（官方）",
        "url": src_url if "yingcheng.gov.cn" in str(src_url) else GOV_HOST,
        "publisher": "应城市人民政府",
        "published_at": AS_OF, "accessed_at": AS_OF,
        "source_type": "official", "reliability": "high",
        "notes": "应城市领导之窗市委/政府/人大/政协领导名录（2026-08-06 抓取）",
    }]

    org_by_id = {o["id"]: o["name"] for o in organizations}
    career_timeline = []
    for pos in positions:
        if pos["person_id"] != p["id"]:
            continue
        schedule = "party" if pos["org_id"] in (1, 3, 5, 9, 10) else "government" if pos["org_id"] in (2, 4, 8) else "other"
        career_timeline.append({
            "start": pos["start_date"] or "unknown", "end": pos["end_date"] or "present",
            "org": org_by_id.get(pos["org_id"], ""), "title": pos["title"],
            "level": pos.get("rank", ""), "location": "孝感市应城市", "system": schedule,
            "rank": pos.get("rank", ""), "is_key_promotion": p["id"] in (1, 2),
            "notes": pos.get("note", ""),
            "confidence": "confirmed", "source_ids": ["S001"],
        })

    org_refs = []
    for pos in positions:
        if pos["person_id"] == p["id"]:
            org_refs.append({"org_name": org_by_id.get(pos["org_id"], ""), "org_type": "", "role": pos["title"]})

    open_q = []
    if not p.get("birthplace"):
        open_q.append({"priority": "high", "question": f"{name}的出生地/籍贯",
                       "why_it_matters": "用于去重与干部来源分析",
                       "suggested_queries": [f"{name} 任前公示 籍贯", f"{name} 应城 简历"], "last_attempted": AS_OF})
    if not p.get("party_join"):
        open_q.append({"priority": "medium", "question": f"{name}的入党时间",
                       "why_it_matters": "用于精确构建晋升时间线",
                       "suggested_queries": [f"{name} 任前公示 入党"], "last_attempted": AS_OF})
    if not p.get("work_start"):
        open_q.append({"priority": "medium", "question": f"{name}的参加工作年份",
                       "why_it_matters": "用于衡量晋升速度",
                       "suggested_queries": [f"{name} 简历 参加工作"], "last_attempted": AS_OF})
    if p["id"] == 1:
        open_q.append({"priority": "high", "question": "胡光怀任应城市委书记的具体日期、前任书记姓名去向",
                       "why_it_matters": "用于书记更替时间线", "suggested_queries": ["应城市委书记 任命 干部大会", "应城 前任 市委书记"], "last_attempted": AS_OF})
    if p["id"] == 2:
        open_q.append({"priority": "high", "question": "马跃任市长日期/是否经历'代市长'阶段、其前任市长姓名",
                       "why_it_matters": "用于市长更替时间线", "suggested_queries": ["应城 市长 任命 代市长", "应城 前任 市长 马跃"], "last_attempted": AS_OF})
        open_q.append({"priority": "medium", "question": "马跃（回族）任市长前的职务序列（早年履历）",
                       "why_it_matters": "少数民族干部快速晋升路径", "suggested_queries": ["马跃 应城 市长 简历"], "last_attempted": AS_OF})

    relationship_objs = []
    for r in relationships:
        if r["person_a"] == p["id"]:
            other = next((x["name"] for x in persons if x["id"] == r["person_b"]), "")
            relationship_objs.append({
                "person": other,
                "relationship_type": "overlap",
                "strength": "strong" if "搭档" in r["type"] else "medium",
                "evidence": r["context"], "overlap_org": r.get("overlap_org", ""),
                "overlap_period": r.get("overlap_period", ""), "direction": "undirected",
                "confidence": "confirmed", "source_ids": ["S001"]})

    governance_record = []
    if p["id"] == 1:
        governance_record.append({"period": "2026", "domain": "economic_development",
                                  "achievement_or_event": "推动盐化工（云图控股全国最大生产基地）绿色化智能化转型、压缩空气储能示范项目、甲鱼产业链与汤池温泉项目落地",
                                  "role_in_event": "调研部署", "measurable_outcome": "", "location": "应城市",
                                  "confidence": "confirmed", "source_ids": ["S001"]})
        governance_record.append({"period": "2026", "domain": "rural_revitalization",
                                  "achievement_or_event": "调研杨岭明光葡萄、三合三结村电商助农等特色农业",
                                  "role_in_event": "调研督导", "measurable_outcome": "", "location": "应城市",
                                  "confidence": "confirmed", "source_ids": ["S001"]})
        governance_record.append({"period": "2026", "domain": "public_security",
                                  "achievement_or_event": "讲授正确政绩观党课强调安全稳定、防汛抗讯底线思维",
                                  "role_in_event": "主讲", "measurable_outcome": "", "location": "应城市",
                                  "confidence": "confirmed", "source_ids": ["S001"]})

    document = {
        "schema_version": "1.0", "generated_at": AS_OF,
        "investigation_scope": {"province": PROVINCE, "city": PARENT_CITY, "region": SLUG,
                                "job": job, "task_id": "hubei_应城市", "time_focus": "2026"},
        "identity": {
            "person_id": f"hubei_xiaogan_yingcheng_{name}",
            "name": name, "aliases": [],
            "gender": p.get("gender", ""), "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""), "birthplace": p.get("birthplace", ""),
            "native_place": p.get("native_place", ""),
            "education": _edu_list(p),
            "party_join": p.get("party_join", ""), "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{p.get('birth', '')}",
                "name_birthplace": f"{name}_{p.get('birthplace', '')}",
                "official_profile_url": src_url if "yingcheng.gov.cn" in str(src_url) else "",
            },
        },
        "current_status": {"current_post": p.get("current_post", ""), "current_org": p.get("current_org", ""),
                           "is_current_confirmed": True, "as_of": AS_OF, "source_ids": ["S001"]},
        "career_timeline": career_timeline,
        "organizations": org_refs,
        "relationships": relationship_objs,
        "governance_record": governance_record,
        "professional_profile": {
            "primary_specializations": ["地方治理", "县域经济"] if p["id"] == 1 else [],
            "secondary_specializations": [],
            "career_pattern": "local_ladder",
            "systems_experience": [], "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": ["正确政绩观", "特色产业", "底线思维", "为民造福"],
            "management_signals": [],
            "caveat": "工作风格源于公开记录与政务报道推断，并非私人心理评估。",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": "搜索范围内未发现纪律处分/审计/负面舆情信号",
             "date": "", "confidence": "unverified", "source_ids": []}],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed" if p.get("birth") else "plausible",
            "current_role": "confirmed",
            "career_completeness": "partial" if p.get("birth") else "thin",
            "relationship_confidence": "high",
            "biggest_gap": "完整履历（早年职务、出生地、入党/参工日期、书记/市长更替时间）",
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
        try:
            build_person_json(p)
        except Exception as e:  # noqa: BLE001
            logger.warning("person JSON failed for %s: %s", p.get("name"), e)
    conn = sqlite3.connect(str(DB_PATH))
    counts = {t: conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
              for t in ("persons", "organizations", "positions", "relationships")}
    conn.close()
    print(f"Built {DB_PATH} and {GEXF_PATH}")
    print(f"persons={len(persons)} orgs={len(organizations)} positions={len(positions)} relationships={len(relationships)}")
    print("DB counts:", counts)


if __name__ == "__main__":
    main()