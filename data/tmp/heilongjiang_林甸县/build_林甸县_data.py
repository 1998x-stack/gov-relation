#!/usr/bin/env python3
"""
林甸县（黑龙江省大庆市）领导班子工作关系网络 — 2026-07-24
Build script for Lindian County, Daqing City, Heilongjiang Province.

Data sources:
- 林甸县人民政府官网 https://www.lindian.gov.cn/ — official leadership pages (2026-07)
- Baidu Baike / Wikipedia — predecessor identification

TASK: heilongjiang_林甸县

Note: Due to geo-restrictions, Baidu Baike and other Chinese biography
sites were inaccessible. Leadership data confirmed from official county
government website leadership pages. Biographical details (birth dates,
education, early career) remain incomplete and are marked accordingly.
"""

import json
import os
import sqlite3  # noqa: used via gov_relation.runner
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

TODAY = "2026-07-24"
AS_OF = TODAY

# ── STAGING DIRECTORIES ──
STAGING = Path(__file__).resolve().parent
DB_PATH = STAGING / "林甸县_network.db"
GEXF_PATH = STAGING / "林甸县_network.gexf"
PERSONS_DIR = STAGING

# ── DATA ──

# Integer IDs mapped
PERSON_ID_MAP = {
    "朱学良": 1,
    "张继祥": 2,
    "白滨": 3,
    "张博": 4,
    "范萌": 5,
    "王永垠": 6,
    "李刚": 7,
    "张志华": 8,
    "徐亚辉": 9,
    "那策": 10,
    "秦浩": 11,
    "付兴": 12,
    "赵光": 13,
    "赵锡贵": 14,
    "王晓东": 15,
    "慕常锋": 16,
    "王永民": 17,
    "孟祥富": 18,
    "李东": 19,
    "梁岩": 20,
    "晋伟": 21,
}

persons = [
    {
        "id": 1,
        "name": "朱学良",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "林甸县委书记",
        "current_org": "中共林甸县委员会",
        "source": "https://www.lindian.gov.cn/lindian/zfxxgk511/202305/c05_269649.shtml",
    },
    {
        "id": 2,
        "name": "张继祥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "林甸县委副书记、县长",
        "current_org": "林甸县人民政府",
        "source": "https://www.lindian.gov.cn/lindian/zfxxgk513/202305/c05_269749.shtml",
    },
    {
        "id": 3,
        "name": "白滨",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "林甸县委常委、常务副县长",
        "current_org": "林甸县人民政府",
        "source": "https://www.lindian.gov.cn/lindian/zfxxgk511/202312/c05_322028.shtml",
    },
    {
        "id": 4,
        "name": "张博",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "林甸县委常委、副县长",
        "current_org": "林甸县人民政府",
        "source": "https://www.lindian.gov.cn/lindian/zfxxgk511/202512/c05_398141.shtml",
    },
    {
        "id": 5,
        "name": "范萌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "林甸县委常委、副县长",
        "current_org": "林甸县人民政府",
        "source": "https://www.lindian.gov.cn/lindian/zfxxgk511/202512/c05_398143.shtml",
    },
    {
        "id": 6,
        "name": "王永垠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "林甸县委常委、组织部部长",
        "current_org": "中共林甸县委员会组织部",
        "source": "https://www.lindian.gov.cn/lindian/zfxxgk511/202305/c05_269732.shtml",
    },
    {
        "id": 7,
        "name": "李刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "林甸县委常委、纪委书记、监委主任",
        "current_org": "中共林甸县纪律检查委员会",
        "source": "https://www.lindian.gov.cn/lindian/zfxxgk511/202305/c05_269730.shtml",
    },
    {
        "id": 8,
        "name": "张志华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "林甸县委常委、宣传部部长",
        "current_org": "中共林甸县委员会宣传部",
        "source": "https://www.lindian.gov.cn/lindian/zfxxgk511/202305/c05_269729.shtml",
    },
    {
        "id": 9,
        "name": "徐亚辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "林甸县委常委、政法委书记",
        "current_org": "中共林甸县委员会政法委员会",
        "source": "https://www.lindian.gov.cn/lindian/zfxxgk511/202504/c05_375877.shtml",
    },
    {
        "id": 10,
        "name": "那策",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "林甸县副县长",
        "current_org": "林甸县人民政府",
        "source": "https://www.lindian.gov.cn/lindian/zfxxgk513/202305/c05_269748.shtml",
    },
    {
        "id": 11,
        "name": "秦浩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "林甸县副县长",
        "current_org": "林甸县人民政府",
        "source": "https://www.lindian.gov.cn/lindian/zfxxgk513/202312/c05_324133.shtml",
    },
    {
        "id": 12,
        "name": "付兴",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "林甸县副县长",
        "current_org": "林甸县人民政府",
        "source": "https://www.lindian.gov.cn/lindian/zfxxgk513/202506/c05_382296.shtml",
    },
    {
        "id": 13,
        "name": "赵光",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "林甸县副县长",
        "current_org": "林甸县人民政府",
        "source": "https://www.lindian.gov.cn/lindian/zfxxgk513/202504/c05_375891.shtml",
    },
    {
        "id": 14,
        "name": "赵锡贵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "林甸县人大常委会党组书记、主任",
        "current_org": "林甸县人民代表大会常务委员会",
        "source": "https://www.lindian.gov.cn/lindian/zfxxgk512/202607/c05_416333.shtml",
    },
    {
        "id": 15,
        "name": "王晓东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "林甸县政协党组书记、主席",
        "current_org": "中国人民政治协商会议林甸县委员会",
        "source": "https://www.lindian.gov.cn/lindian/zfxxgk514/202305/c05_269758.shtml",
    },
    {
        "id": 16,
        "name": "慕常锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "林甸县政协副主席",
        "current_org": "中国人民政治协商会议林甸县委员会",
        "source": "https://www.lindian.gov.cn/lindian/zfxxgk514/202305/c05_269755.shtml",
    },
    {
        "id": 17,
        "name": "王永民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "林甸县政协党组副书记、三级调研员",
        "current_org": "中国人民政治协商会议林甸县委员会",
        "source": "https://www.lindian.gov.cn/lindian/zfxxgk514/202305/c05_269754.shtml",
    },
    {
        "id": 18,
        "name": "孟祥富",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "林甸县政府二级调研员",
        "current_org": "林甸县人民政府",
        "source": "https://www.lindian.gov.cn/lindian/zfxxgk513/202409/c05_356150.shtml",
    },
    {
        "id": 19,
        "name": "李东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "林甸县人大常委会党组成员",
        "current_org": "林甸县人民代表大会常务委员会",
        "source": "https://www.lindian.gov.cn/lindian/zfxxgk512/202509/c05_389009.shtml",
    },
    {
        "id": 20,
        "name": "梁岩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "林甸县人大常委会党组成员",
        "current_org": "林甸县人民代表大会常务委员会",
        "source": "https://www.lindian.gov.cn/lindian/zfxxgk512/202509/c05_389010.shtml",
    },
    {
        "id": 21,
        "name": "晋伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任林甸县委书记",
        "current_org": "（已离任）",
        "source": "Wikipedia（林甸县条目，可能已过时）",
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共林甸县委员会",
        "type": "党委",
        "level": "县处级",
        "location": "黑龙江省大庆市林甸县",
    },
    {
        "id": 2,
        "name": "林甸县人民政府",
        "type": "政府",
        "level": "县处级",
        "location": "黑龙江省大庆市林甸县",
    },
    {
        "id": 3,
        "name": "中共林甸县纪律检查委员会",
        "type": "纪委",
        "level": "县处级",
        "location": "黑龙江省大庆市林甸县",
    },
    {
        "id": 4,
        "name": "中共林甸县委员会组织部",
        "type": "党委部门",
        "level": "乡科级",
        "location": "黑龙江省大庆市林甸县",
    },
    {
        "id": 5,
        "name": "中共林甸县委员会宣传部",
        "type": "党委部门",
        "level": "乡科级",
        "location": "黑龙江省大庆市林甸县",
    },
    {
        "id": 6,
        "name": "中共林甸县委员会政法委员会",
        "type": "党委部门",
        "level": "乡科级",
        "location": "黑龙江省大庆市林甸县",
    },
    {
        "id": 7,
        "name": "林甸县人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "location": "黑龙江省大庆市林甸县",
    },
    {
        "id": 8,
        "name": "中国人民政治协商会议林甸县委员会",
        "type": "政协",
        "level": "县处级",
        "location": "黑龙江省大庆市林甸县",
    },
]

positions = [
    # 朱学良 — 县委书记
    {
        "person_id": 1,
        "org_id": 1,
        "title": "林甸县委书记",
        "start": "待查",
        "end": "present",
        "rank": "县处级正职",
        "note": "主持县委全面工作。2026年7月仍任现职。此前曾任林甸县长，后晋升县委书记",
    },
    # 朱学良 — 此前任林甸县长
    {
        "person_id": 1,
        "org_id": 2,
        "title": "林甸县委副书记、县长（前任）",
        "start": "待查",
        "end": "待查",
        "rank": "县处级正职",
        "note": "晋升县委书记前曾任林甸县长",
    },
    # 张继祥 — 县长
    {
        "person_id": 2,
        "org_id": 2,
        "title": "林甸县委副书记、县长",
        "start": "待查",
        "end": "present",
        "rank": "县处级正职",
        "note": "主持县政府全面工作。2026年7月仍任现职",
    },
    {
        "person_id": 2,
        "org_id": 1,
        "title": "林甸县委副书记",
        "start": "待查",
        "end": "present",
        "rank": "县处级副职",
        "note": "兼任县政府党组书记",
    },
    # 白滨 — 常委、常务副县长
    {
        "person_id": 3,
        "org_id": 2,
        "title": "林甸县委常委、常务副县长",
        "start": "待查",
        "end": "present",
        "rank": "县处级副职",
        "note": "协助县长工作，负责县政府常务工作、信访召集人；主持鹤鸣湖镇党委全面工作",
    },
    {
        "person_id": 3,
        "org_id": 1,
        "title": "林甸县委常委",
        "start": "待查",
        "end": "present",
        "rank": "县处级副职",
        "note": "县委常务委员会委员",
    },
    # 张博 — 常委、副县长
    {
        "person_id": 4,
        "org_id": 2,
        "title": "林甸县委常委、副县长",
        "start": "待查",
        "end": "present",
        "rank": "县处级副职",
        "note": "负责协调对接贸促会帮扶工作，协助抓招商引资和乡村振兴专项工作",
    },
    {
        "person_id": 4,
        "org_id": 1,
        "title": "林甸县委常委",
        "start": "待查",
        "end": "present",
        "rank": "县处级副职",
        "note": "县委常务委员会委员",
    },
    # 范萌 — 常委、副县长
    {
        "person_id": 5,
        "org_id": 2,
        "title": "林甸县委常委、副县长",
        "start": "待查",
        "end": "present",
        "rank": "县处级副职",
        "note": "负责人社、自然资源、交通运输、林草、退役军人事务等",
    },
    {
        "person_id": 5,
        "org_id": 1,
        "title": "林甸县委常委",
        "start": "待查",
        "end": "present",
        "rank": "县处级副职",
        "note": "县委常务委员会委员",
    },
    # 王永垠 — 组织部长
    {
        "person_id": 6,
        "org_id": 4,
        "title": "林甸县委常委、组织部部长",
        "start": "待查",
        "end": "present",
        "rank": "县处级副职",
        "note": "负责组织、干部、人才工作，主持县委组织部全面工作",
    },
    {
        "person_id": 6,
        "org_id": 1,
        "title": "林甸县委常委",
        "start": "待查",
        "end": "present",
        "rank": "县处级副职",
        "note": "县委常务委员会委员",
    },
    # 李刚 — 纪委书记
    {
        "person_id": 7,
        "org_id": 3,
        "title": "林甸县委常委、纪委书记、监委主任",
        "start": "待查",
        "end": "present",
        "rank": "县处级副职",
        "note": "负责纪检、监察、巡察工作",
    },
    {
        "person_id": 7,
        "org_id": 1,
        "title": "林甸县委常委",
        "start": "待查",
        "end": "present",
        "rank": "县处级副职",
        "note": "县委常务委员会委员",
    },
    # 张志华 — 宣传部长
    {
        "person_id": 8,
        "org_id": 5,
        "title": "林甸县委常委、宣传部部长",
        "start": "待查",
        "end": "present",
        "rank": "县处级副职",
        "note": "负责宣传思想文化和意识形态工作",
    },
    {
        "person_id": 8,
        "org_id": 1,
        "title": "林甸县委常委",
        "start": "待查",
        "end": "present",
        "rank": "县处级副职",
        "note": "县委常务委员会委员",
    },
    # 徐亚辉 — 政法委书记
    {
        "person_id": 9,
        "org_id": 6,
        "title": "林甸县委常委、政法委书记",
        "start": "待查",
        "end": "present",
        "rank": "县处级副职",
        "note": "负责政法、社会稳定工作；同时负责农业农村、乡村振兴、水务、供销合作等工作",
    },
    {
        "person_id": 9,
        "org_id": 1,
        "title": "林甸县委常委",
        "start": "待查",
        "end": "present",
        "rank": "县处级副职",
        "note": "县委常务委员会委员",
    },
    # 那策 — 副县长
    {
        "person_id": 10,
        "org_id": 2,
        "title": "林甸县副县长",
        "start": "待查",
        "end": "present",
        "rank": "县处级副职",
        "note": "负责公共安全、法治建设；分管公安局、司法局",
    },
    # 秦浩 — 副县长
    {
        "person_id": 11,
        "org_id": 2,
        "title": "林甸县副县长",
        "start": "待查",
        "end": "present",
        "rank": "县处级副职",
        "note": "负责工信科技、商务粮储、营商环境、招商",
    },
    # 付兴 — 副县长
    {
        "person_id": 12,
        "org_id": 2,
        "title": "林甸县副县长",
        "start": "待查",
        "end": "present",
        "rank": "县处级副职",
        "note": "负责教育、卫生、文体、旅游、县校合作",
    },
    # 赵光 — 副县长
    {
        "person_id": 13,
        "org_id": 2,
        "title": "林甸县副县长",
        "start": "待查",
        "end": "present",
        "rank": "县处级副职",
        "note": "负责民政、医保、市场监管、社区工作",
    },
    # 赵锡贵 — 人大主任
    {
        "person_id": 14,
        "org_id": 7,
        "title": "林甸县人大常委会党组书记、主任",
        "start": "待查",
        "end": "present",
        "rank": "县处级正职",
    },
    # 王晓东 — 政协主席
    {
        "person_id": 15,
        "org_id": 8,
        "title": "林甸县政协党组书记、主席",
        "start": "待查",
        "end": "present",
        "rank": "县处级正职",
    },
    # 慕常锋 — 政协副主席
    {
        "person_id": 16,
        "org_id": 8,
        "title": "林甸县政协副主席",
        "start": "待查",
        "end": "present",
        "rank": "县处级副职",
        "note": "兼代管住建、城管工作",
    },
    # 王永民 — 政协党组副书记
    {
        "person_id": 17,
        "org_id": 8,
        "title": "林甸县政协党组副书记、三级调研员",
        "start": "待查",
        "end": "present",
        "rank": "县处级副职",
    },
    # 孟祥富 — 二级调研员
    {
        "person_id": 18,
        "org_id": 2,
        "title": "林甸县政府二级调研员",
        "start": "待查",
        "end": "present",
        "rank": "县处级副职",
        "note": "协助常务副县长工作",
    },
    # 李东 — 人大常委会党组成员
    {
        "person_id": 19,
        "org_id": 7,
        "title": "林甸县人大常委会党组成员",
        "start": "待查",
        "end": "present",
        "rank": "县处级副职",
    },
    # 梁岩 — 人大常委会党组成员
    {
        "person_id": 20,
        "org_id": 7,
        "title": "林甸县人大常委会党组成员",
        "start": "待查",
        "end": "present",
        "rank": "县处级副职",
    },
    # 晋伟 — 前任县委书记
    {
        "person_id": 21,
        "org_id": 1,
        "title": "林甸县委书记（前任）",
        "start": "待查",
        "end": "待查",
        "rank": "县处级正职",
        "note": "朱学良的前任，具体任期和去向待查",
    },
]

relationships = [
    # 党政正职搭档
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记与县长党政正职搭档关系",
        "overlap_org": "中共林甸县委员会/林甸县人民政府",
        "overlap_period": "待查至今",
    },
    # 朱学良与晋伟 — 前后任关系
    {
        "person_a": 1,
        "person_b": 21,
        "type": "successor_predecessor",
        "context": "朱学良接替晋伟任林甸县委书记",
        "overlap_org": "中共林甸县委员会",
        "overlap_period": "交接期",
    },
    # 朱学良与张继祥 — 前后任县长（朱学良此前任县长，张继祥接任）
    {
        "person_a": 1,
        "person_b": 2,
        "type": "successor_predecessor",
        "context": "朱学良此前任林甸县长，晋升书记后张继祥接任县长",
        "overlap_org": "林甸县人民政府",
        "overlap_period": "交接期",
    },
    # 县委常委之间的同僚关系
    {
        "person_a": 3,
        "person_b": 6,
        "type": "colleague",
        "context": "同为县委常委",
        "overlap_org": "中共林甸县委员会",
        "overlap_period": "待查至今",
    },
    {
        "person_a": 3,
        "person_b": 7,
        "type": "colleague",
        "context": "同为县委常委",
        "overlap_org": "中共林甸县委员会",
        "overlap_period": "待查至今",
    },
    {
        "person_a": 3,
        "person_b": 8,
        "type": "colleague",
        "context": "同为县委常委",
        "overlap_org": "中共林甸县委员会",
        "overlap_period": "待查至今",
    },
    {
        "person_a": 3,
        "person_b": 9,
        "type": "colleague",
        "context": "同为县委常委",
        "overlap_org": "中共林甸县委员会",
        "overlap_period": "待查至今",
    },
    {
        "person_a": 6,
        "person_b": 7,
        "type": "colleague",
        "context": "同为县委常委",
        "overlap_org": "中共林甸县委员会",
        "overlap_period": "待查至今",
    },
    {
        "person_a": 6,
        "person_b": 8,
        "type": "colleague",
        "context": "同为县委常委",
        "overlap_org": "中共林甸县委员会",
        "overlap_period": "待查至今",
    },
    {
        "person_a": 6,
        "person_b": 9,
        "type": "colleague",
        "context": "同为县委常委",
        "overlap_org": "中共林甸县委员会",
        "overlap_period": "待查至今",
    },
    {
        "person_a": 7,
        "person_b": 8,
        "type": "colleague",
        "context": "同为县委常委",
        "overlap_org": "中共林甸县委员会",
        "overlap_period": "待查至今",
    },
    {
        "person_a": 7,
        "person_b": 9,
        "type": "colleague",
        "context": "同为县委常委",
        "overlap_org": "中共林甸县委员会",
        "overlap_period": "待查至今",
    },
    {
        "person_a": 8,
        "person_b": 9,
        "type": "colleague",
        "context": "同为县委常委",
        "overlap_org": "中共林甸县委员会",
        "overlap_period": "待查至今",
    },
    {
        "person_a": 4,
        "person_b": 5,
        "type": "colleague",
        "context": "同为县委常委、副县长",
        "overlap_org": "中共林甸县委员会/林甸县人民政府",
        "overlap_period": "待查至今",
    },
    # 县政府领导同僚关系
    {
        "person_a": 10,
        "person_b": 11,
        "type": "colleague",
        "context": "同为县政府副县长",
        "overlap_org": "林甸县人民政府",
        "overlap_period": "待查至今",
    },
    {
        "person_a": 10,
        "person_b": 12,
        "type": "colleague",
        "context": "同为县政府副县长",
        "overlap_org": "林甸县人民政府",
        "overlap_period": "待查至今",
    },
    {
        "person_a": 10,
        "person_b": 13,
        "type": "colleague",
        "context": "同为县政府副县长",
        "overlap_org": "林甸县人民政府",
        "overlap_period": "待查至今",
    },
    {
        "person_a": 11,
        "person_b": 12,
        "type": "colleague",
        "context": "同为县政府副县长",
        "overlap_org": "林甸县人民政府",
        "overlap_period": "待查至今",
    },
    {
        "person_a": 11,
        "person_b": 13,
        "type": "colleague",
        "context": "同为县政府副县长",
        "overlap_org": "林甸县人民政府",
        "overlap_period": "待查至今",
    },
    {
        "person_a": 12,
        "person_b": 13,
        "type": "colleague",
        "context": "同为县政府副县长",
        "overlap_org": "林甸县人民政府",
        "overlap_period": "待查至今",
    },
]


def main():
    # Build DB and GEXF
    run_build(
        slug="林甸县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    # Print summary
    print(f"\nBuild complete: {TODAY}")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")
    print(f"  Persons:  {len(persons)}")
    print(f"  Orgs:     {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print("\nNote: Biographical details limited due to web access constraints.")
    print("See open questions in person JSON files and report for gaps.")


if __name__ == "__main__":
    main()
