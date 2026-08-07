#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 安塞区, 延安市, 陕西省.

Investigation date: 2026-08-07
Task ID: shaanxi_安塞区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources:
  - 安塞区人民政府官网 (www.ansai.gov.cn) — 本地要闻/公示公告/政府信息公开 多篇官方新闻
    确认现任党组书记/书记与代理区长、区委常委班子、人大政协领导
  - 官方新闻时间线重建 李延武 区长→区委书记 晋升路径

Confidence notes:
  - 李延武(区委书记): 2026-08-07 官方新闻 "区委书记李延武带队深入沿河湾镇督导调研防汛备汛工作",
    2026-05-15 区人武部党委第一书记任职大会(区委书记、区人武部党委第一书记); 此前长期任区委副书记、区长
    (2021-09 区委副书记、区政府党组书记; 2025-01/2025-02 区委副书记、区长). 及其完整履历(出生/籍贯/学历/任书记具体时间)公开未必齐, 以 open_questions 记录
  - 党晓明(区委副书记、代理区长): 2026-08-05 区政府第41次常务会议 "区委副书记、代理区长党晓明主持";
    完整履历待查
  - 常委班子: 2026 区委常委会(扩大)第19次会议列名 唐剑、孙学武、卢淑云、高流、王华、马伟伟;
    2026 区委理论学习中心组 列名 唐剑、高流、李林; 李林(纪委书记、监委主任)由2025官方新闻佐证
  - 区政府: 副区长 李娜、李建虎、申健枫; 区委常委、副区长王华
  - 区人大常委会主任 段玉凤; 区政协主席 张志贵 (均在多篇2026官方新闻确认)
  - 前任区委书记 曹振宇 (2023-09 二届五次全会 区委书记; 2025-02 安塞代表团 区委书记), 亦曾任区长(2018-2019)
"""

import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

BASE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE, "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.abspath(os.path.join(BASE, "..", "..", "..")))

from gov_relation.runner import run_build

SLUG = "安塞区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-07"

STAGING_DIR = Path(BASE)
DB_PATH = str(STAGING_DIR / f"{SLUG}_network.db")
GEXF_PATH = str(STAGING_DIR / f"{SLUG}_network.gexf")

# ═══════════════════════════════════════════════════════════════════════════════
# Data
# ═══════════════════════════════════════════════════════════════════════════════

persons_data = [
    # 区委
    {
        "id": 1,
        "name": "李延武",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共延安市安塞区委员会",
        "source": "安塞区政府官网新闻。2026-08-07'区委书记李延武带队督导防汛'；2026-05-15任区人武部党委第一书记；2021-09起任区长，2026-04短暂兼任区委书记+区长，2026-05起任区委书记"
    },
    {
        "id": 17,
        "name": "张进",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-04",
        "birthplace": "河南巩义",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长、公安安塞分局局长",
        "current_org": "延安市公安局安塞分局",
        "source": "安塞区政府官网领导之窗(政府领导页)。男1978年4月、河南巩义人、大学学历；县级公安副科→市级公安大队长→副支队长→支队长→公安分局局长/副区长(政法系统交流)"
    },
    {
        "id": 2,
        "name": "党晓明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、代理区长",
        "current_org": "安塞区人民政府",
        "source": "安塞区政府官网新闻确认。2026-08-05区政府第41次常务会议'区委副书记、代理区长党晓明主持并讲话'；2026-08-07区委理论学习中心组出席"
    },
    {
        "id": 3,
        "name": "唐剑",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、组织部部长",
        "current_org": "中共延安市安塞区委员会",
        "source": "安塞区政府官网。2026-08-07区委理论学习中心组列席(区委常委唐剑)；2023-06富县县委副书记调研时'区委常委、组织部部长唐剑陪同'"
    },
    {
        "id": 4,
        "name": "孙学武",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-10",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、常务副区长、高新区党工委书记",
        "current_org": "安塞区人民政府",
        "source": "安塞区政府官网政府领导页。1976年10月生、研究生；公安副科→市委政法委政治部副主任→市纪委监察局干部室主任→市纪委监委组织部部长→黄龙县、宝塔区纪委书记/监委主任→安塞区委常委、常务副区长(跨县轮换)"
    },
    {
        "id": 5,
        "name": "卢淑云",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共延安市安塞区委员会",
        "source": "2026-07-31区委常委会(扩大)第19次会议列席常委(2026-08-04发布)"
    },
    {
        "id": 6,
        "name": "高流",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共延安市安塞区委员会",
        "source": "2026-08-07区委理论学习中心组及2026-07-31区委常委会列席常委"
    },
    {
        "id": 7,
        "name": "王华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-03",
        "birthplace": "榆林市横山区",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、政府党组成员、副区长",
        "current_org": "安塞区人民政府",
        "source": "安塞区政府官网政府领导页。男1975年3月、榆林市横山区人、省委党校研究生、中共党员；中学教师→县政府办副主任→镇长→镇党委书记→县委机关党委书记/办公室主任→副县长→县委常委、政法委书记(跨市干部)"
    },
    {
        "id": 8,
        "name": "马伟伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共延安市安塞区委员会",
        "source": "2026-07-31区委常委会(扩大)第19次会议列席常委(2026-08-04发布)"
    },
    {
        "id": 9,
        "name": "李林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、纪委书记、监委主任",
        "current_org": "中共延安市安塞区纪律检查委员会",
        "source": "2026-08-07区委理论学习中心组列席(区委常委李林)；2025-02安塞代表团'区委常委、纪委书记、监委主任李林'"
    },
    # 政府班子
    {
        "id": 10,
        "name": "李娜",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1974-08",
        "birthplace": "",
        "education": "在职研究生",
        "party_join": "民革党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "安塞区人民政府",
        "source": "安塞区政府官网政府领导页。女1974年8月、在职研究生、民革党员(非中共)；曾任延安市政府组成部门科长"
    },
    {
        "id": 11,
        "name": "李建虎",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-07",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "安塞区人民政府",
        "source": "安塞区政府官网政府领导页。男1976年7月、研究生；纪委办公室主任→纪委常委/纠风办主任→组织部副部长→镇长→镇党委书记→街道党工委书记→县委办公室主任"
    },
    {
        "id": 12,
        "name": "申健枫",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "安塞区人民政府",
        "source": "2026-07-31区委常委会(扩大)第19次会议列席副区长(2026-08-04发布)；官网领导页暂未更新，履历待查"
    },
    # 人大/政协
    {
        "id": 13,
        "name": "段玉凤",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "安塞区人民代表大会常务委员会",
        "source": "2026-08-07区委理论学习中心组、2026-07-31区委常委会(扩大)第19次会议列席主任段玉凤"
    },
    {
        "id": 14,
        "name": "张志贵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "中国人民政治协商会议安塞区委员会",
        "source": "2026-08-07区委理论学习中心组出席'区政协主席张志贵'；2023-09二届五次全会'区政协党组书记、主席张志贵'；2018年曾任副区长"
    },
    # 前任
    {
        "id": 15,
        "name": "曹振宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任区委书记(离任)",
        "current_org": "中共延安市安塞区委员会",
        "source": "2023-09中共延安市安塞区第二届委员会第五次全体会议'区委书记曹振宇'；2025-02安塞代表团'区委书记曹振宇'；2018-2019曾任'区委副书记、区长'。李延武接任书记"
    },
    {
        "id": 16,
        "name": "闫晓妮",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记(2025年)",
        "current_org": "中共延安市安塞区委员会",
        "source": "2025-01-27'区委副书记、区长李延武，区委副书记闫晓妮带领多部门检查春节期间安全生产'"
    },
]

organizations_data = [
    {
        "id": 1,
        "name": "中共延安市安塞区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共延安市委员会",
        "location": "延安市安塞区"
    },
    {
        "id": 2,
        "name": "安塞区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "延安市人民政府",
        "location": "延安市安塞区"
    },
    {
        "id": 3,
        "name": "安塞区人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "延安市人民代表大会常务委员会",
        "location": "延安市安塞区"
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议安塞区委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "政协延安市委员会",
        "location": "延安市安塞区"
    },
    {
        "id": 5,
        "name": "中共延安市安塞区纪律检查委员会/区监委",
        "type": "纪委",
        "level": "县处级",
        "parent": "中共延安市纪律检查委员会",
        "location": "延安市安塞区"
    },
    {
        "id": 6,
        "name": "延安市公安局安塞分局",
        "type": "政府",
        "level": "正科级",
        "parent": "延安市公安局",
        "location": "延安市安塞区"
    },
]

positions_data = [
    # 区委
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "2025-2026", "end_date": "present", "rank": "县处级", "note": "兼区人武部党委第一书记(2026-05确认)；前任曹振宇离任后接任"},
    {"person_id": 15, "org_id": 1, "title": "区委书记(离任)", "start_date": "2021", "end_date": "2025-2026", "rank": "县处级", "note": "2023-09/2025-02均在任；后由李延武接任"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "2025-2026", "end_date": "present", "rank": "县处级", "note": "兼代理区长"},
    {"person_id": 3, "org_id": 1, "title": "区委常委、组织部部长", "start_date": "unknown", "end_date": "present", "rank": "副县处级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "区委常委", "start_date": "unknown", "end_date": "present", "rank": "副县处级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "区委常委", "start_date": "unknown", "end_date": "present", "rank": "副县处级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "区委常委", "start_date": "unknown", "end_date": "present", "rank": "副县处级", "note": ""},
    {"person_id": 16, "org_id": 1, "title": "区委副书记(2025)", "start_date": "unknown", "end_date": "unknown", "rank": "副县处级", "note": "2025-01公开活动；后去向待查"},

    # 政府
    {"person_id": 2, "org_id": 2, "title": "代理区长", "start_date": "2025-2026", "end_date": "present", "rank": "正县处级", "note": "接李延武任区长；主持区政府常务会议"},
    {"person_id": 4, "org_id": 2, "title": "常务副区长", "start_date": "unknown", "end_date": "present", "rank": "副县处级", "note": "区委常委兼常务副区长"},
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "unknown", "end_date": "present", "rank": "副县处级", "note": "区委常委兼副区长，分工城建"},
    {"person_id": 10, "org_id": 2, "title": "副区长", "start_date": "unknown", "end_date": "present", "rank": "副县处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "副区长", "start_date": "unknown", "end_date": "present", "rank": "副县处级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "副区长", "start_date": "unknown", "end_date": "present", "rank": "副县处级", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "副区长", "start_date": "unknown", "end_date": "present", "rank": "副县处级", "note": "政法系统交流；分管政法/公安"},
    {"person_id": 17, "org_id": 6, "title": "公安安塞分局局长", "start_date": "unknown", "end_date": "present", "rank": "副县处级", "note": "副区长兼公安局长"},

    # 纪委
    {"person_id": 9, "org_id": 5, "title": "纪委书记、监委主任", "start_date": "unknown", "end_date": "present", "rank": "副县处级", "note": "区委常委"},

    # 人大/政协
    {"person_id": 13, "org_id": 3, "title": "区人大常委会主任", "start_date": "unknown", "end_date": "present", "rank": "正县处级", "note": ""},
    {"person_id": 14, "org_id": 4, "title": "区政协主席", "start_date": "2020s", "end_date": "present", "rank": "正县处级", "note": "曾任副区长(2018)、区政协党组书记"}, 

    # 历史任职（关系佐证）
    {"person_id": 1, "org_id": 2, "title": "区长(前任)", "start_date": "2021", "end_date": "2025-2026", "rank": "正县处级", "note": "2021-09区委副书记、区政府党组书记；2023-2025区长"},
    {"person_id": 15, "org_id": 2, "title": "区长(前任)", "start_date": "2017-2018", "end_date": "2021", "rank": "正县处级", "note": "2018-2019区委副书记、区长，后转任区委书记"},
]

relationships_data = [
    # 党政主要领导搭档
    {"person_a": 1, "person_b": 2, "type": "党政搭档/前后任", "context": "李延武由区长升任区委书记后，原区长一职由党晓明代理；两人接续主导区委、区政府", "overlap_org": "中共安塞区委/区政府", "overlap_period": "2025-2026-present"},
    {"person_a": 1, "person_b": 15, "type": "前任/继任", "context": "曹振宇离任区委书记，李延武接任", "overlap_org": "中共延安市安塞区委", "overlap_period": "2025-2026"},
    {"person_a": 15, "person_b": 1, "type": "继任(前任区长→继任区委书记)", "context": "曹振宇原是区长(2018-2021)，李延武接任区长(2021)；后李延武任区委书记", "overlap_org": "安塞区政府", "overlap_period": "2021"},
    # 书记与班子
    {"person_a": 1, "person_b": 3, "type": "班子", "context": "区委书记李延武——组织部长唐剑同场开会", "overlap_org": "中共安塞区委", "overlap_period": "unknown-present"},
    {"person_a": 1, "person_b": 9, "type": "班子", "context": "区委书记——纪委书记李林班子关系", "overlap_org": "中共安塞区委", "overlap_period": "unknown-present"},
    {"person_a": 1, "person_b": 4, "type": "班子", "context": "区委书记——常务副区长孙学武工作关系（同场列席区委常委会）", "overlap_org": "中共安塞区委", "overlap_period": "unknown-present"},
    # 区长与政府班子
    {"person_a": 2, "person_b": 4, "type": "工作搭档", "context": "代理区长党晓明——常务副区长孙学武工作搭档（同场参加周解扣会议/区政府常务会）", "overlap_org": "安塞区政府", "overlap_period": "2025-2026-present"},
    {"person_a": 2, "person_b": 7, "type": "工作搭档", "context": "代理区长党晓明——副区长王华一同调研城市建设(2026-06)", "overlap_org": "安塞区政府", "overlap_period": "2026"},
    # 人大政协与区领导
    {"person_a": 2, "person_b": 13, "type": "工作关系", "context": "代理区长——人大常委会主任段玉凤（人大任免监督）", "overlap_org": "区人大/区政府", "overlap_period": "2025-2026-present"},
    {"person_a": 1, "person_b": 14, "type": "工作关系", "context": "区委书记——政协主席张志贵（政协协商）", "overlap_org": "中共安塞区委/区政协", "overlap_period": "2020s-present"},
    # 前任班子成员之间交叠
    {"person_a": 1, "person_b": 16, "type": "前任班子", "context": "李延武(区长)——闫晓妮(区委副书记)2025-01 同场检查安全生产", "overlap_org": "中共安塞区委", "overlap_period": "2025-01"},
]

# ═══════════════════════════════════════════════════════════════════════════════
# Person JSON generation
# ═══════════════════════════════════════════════════════════════════════════════

PERSON_JSON_TEMPLATE = {
    "李延武": {
        "filename": f"{TODAY}-陕西省-延安市-区委书记-李延武.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {"province": "陕西省", "city": "延安市", "region": "安塞区", "job": "区委书记", "task_id": "shaanxi_安塞区", "time_focus": "2026"},
            "identity": {
                "person_id": "ansai_li_yanwu",
                "name": "李延武",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {"name_birth": "李延武_未知", "name_birthplace": "李延武_未知", "official_profile_url": "http://www.ansai.gov.cn/"}
            },
            "current_status": {"current_post": "区委书记", "current_org": "中共延安市安塞区委员会", "administrative_rank": "正县处级", "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S001", "S002", "S003"]},
            "career_timeline": [
                {"start": "2025-2026", "end": "present", "org": "中共延安市安塞区委员会", "title": "区委书记", "level": "县处级", "location": "陕西延安安塞", "system": "party", "rank": "正县处级", "is_key_promotion": True, "notes": "2026-08-07'区委书记李延武带队督导防汛'；2026-05-15任区人武部党委第一书记；多次主持区委常委会", "confidence": "confirmed", "source_ids": ["S001", "S002", "S003"]},
                {"start": "2021", "end": "2025-2026", "org": "安塞区人民政府", "title": "区委副书记、区长", "level": "县处级", "location": "陕西延安安塞", "system": "government", "rank": "正县处级", "is_key_promotion": False, "notes": "2021-09'区委副书记、区政府党组书记'；2023-09二届五次全会'区委副书记、区长'；2025-02仍区长；主持区政府常务会议与经济工作", "confidence": "confirmed", "source_ids": ["S004", "S005", "S006"]},
                {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "公开渠道未获取任安塞区长/书记之前履历(出生、籍贯、学历、任职前任职务、任区长具体时间、任前公示)。", "confidence": "unverified", "source_ids": []},
            ],
            "organizations": [],
            "relationships": [
                {"person": "党晓明", "person_id": "ansai_dang_xiaoming", "relationship_type": "overlap", "strength": "strong", "evidence": "区委书记——代理区长党政搭档；李延武升书记后党小明白接任区长(代理)", "overlap_org": "中共安塞区委/区政府", "overlap_period": "2025-2026-present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]},
                {"person": "曹振宇", "person_id": "ansai_cao_zhenyu", "relationship_type": "predecessor_successor", "strength": "strong", "evidence": "曹振宇(原区委书记/区长)离任，李延武接任区委书记；两人先后任区长", "overlap_org": "安塞区", "overlap_period": "2021-2026", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S006"]},
                {"person": "唐剑", "person_id": "ansai_tang_jian", "relationship_type": "overlap", "strength": "medium", "evidence": "区委书记——组织部长共同出席常委会", "overlap_org": "中共安塞区委", "overlap_period": "unknown-present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]},
            ],
            "governance_record": [
                {"period": "2026-08", "domain": "public_security", "achievement_or_event": "率队督导沿河湾镇防汛备汛，检查淤地坝、过水桥、地质灾害点并部署全区防汛安排", "role_in_event": "带队", "measurable_outcome": "", "location": "延安安塞", "confidence": "confirmed", "source_ids": ["S001"]},
                {"period": "2023-01", "domain": "economic_development", "achievement_or_event": "在2023新春贺词中公布：总投资61亿元新能源装备制造产业园开工，GDP172.7亿元创新高，全市高质量发展考评第二", "role_in_event": "区长代表区委区政府", "measurable_outcome": "GDP 172.7亿元", "location": "延安安塞", "confidence": "confirmed", "source_ids": ["S005"]},
            ],
            "professional_profile": {
                "primary_specializations": ["党的建设", "县域治理", "经济调度"],
                "secondary_specializations": ["民生工程", "防汛安全"],
                "career_pattern": "local_ladder(区内政委)",
                "systems_experience": ["party", "government"],
                "geographic_pattern": ["延安市安塞区"],
                "promotion_velocity": {"summary": "2021-2025 区长→2025-2026 区委书记；本土晋升", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {"trait": "development_focused", "evidence": "强调项目、招商、经济提质增效（区委常委会第19次）", "confidence": "plausible", "source_ids": ["S003"]},
                    {"trait": "grassroots_oriented", "evidence": "多次带队调研镇街、防汛隐患一线", "confidence": "plausible", "source_ids": ["S001"]},
                ],
                "speech_themes": ["防汛安全", "党建引领", "经济调度", "民生实事"],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现公开纪律处分或负面报道", "date": "", "confidence": "unverified", "source_ids": []}],
            "source_register": [
                {"id": "S001", "title": "李延武调研沿河湾镇防汛备汛工作", "url": "http://www.ansai.gov.cn/xwzx/bdyw/2085553036377415681.html", "publisher": "安塞区融媒体中心", "published_at": "2026-08-07", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认'区委书记李延武'在任"},
                {"id": "S002", "title": "区人武部党委第一书记任职大会召开", "url": "http://www.ansai.gov.cn/xwzx/bdyw/2056563713167314945.html", "publisher": "安塞区融媒体中心", "published_at": "2026-05-19", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认区委书记李延武任区人武部党委第一书记"},
                {"id": "S003", "title": "区委常委会(扩大)第19次会议召开", "url": "http://www.ansai.gov.cn/xwzx/bdyw/2084448691087446017.html", "publisher": "安塞区融媒体中心", "published_at": "2026-08-04", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "区委书记李延武主持；列常委、副区长名单"},
                {"id": "S004", "title": "李延武调研我区财政运行情况", "url": "http://www.ansai.gov.cn/xwzx/bdyw/1534083364980637697.html", "publisher": "安塞区融媒体中心", "published_at": "2021-09-30", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "2021-09旧任区委副书记、区政府党组书记"},
                {"id": "S005", "title": "安塞区委副书记、区长李延武发表2023年新春贺词", "url": "http://www.ansai.gov.cn/xwzx/spxx/1617799465165508609.html", "publisher": "安塞区融媒体中心", "published_at": "2023-01-21", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "2023仍任区长；含经济成果"},
                {"id": "S006", "title": "中共延安市安塞区第二届委员会第五次全体会议召开", "url": "http://www.ansai.gov.cn/xwzx/bdyw/1704654096570630146.html", "publisher": "安塞区融媒体中心", "published_at": "2023-09-20", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "2023-09时曹振宇任书记、李延武任区长"},
            ],
            "confidence_summary": {"identity": "partial", "current_role": "confirmed", "career_completeness": "partial", "relationship_confidence": "medium", "biggest_gap": "任安塞区长/书记前的完整履历（出生、籍贯、学历、任职单位）与任区长/书记具体时间"},
            "open_questions": [
                {"priority": "critical", "question": "李延武的完整履历(出生、籍贯、学历、任安塞区长前的任职经历、任区长/区委书记的具体时间)", "why_it_matters": "关键人物履历不完整，影响网络与时间线", "suggested_queries": ["李延武 安塞 简历", "李延武 延安 任前公示", "安塞区 区委书记 任命"], "last_attempted": AS_OF},
                {"priority": "high", "question": "前任区委书记曹振宇的去向(是否升迁出安塞)", "why_it_matters": "区书记交接时间线", "suggested_queries": ["曹振宇 延安 任职", "安塞区 前任区委书记 去向"], "last_attempted": AS_OF},
            ]
        }
    },
    "党晓明": {
        "filename": f"{TODAY}-陕西省-延安市-代理区长-党晓明.json",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {"province": "陕西省", "city": "延安市", "region": "安塞区", "job": "代理区长", "task_id": "shaanxi_安塞区", "time_focus": "2026"},
            "identity": {
                "person_id": "ansai_dang_xiaoming",
                "name": "党晓明",
                "aliases": [],
                "gender": "男",
                "ethnicity": "汉族",
                "birth": "",
                "birthplace": "",
                "native_place": "",
                "education": [],
                "party_join": "中共党员",
                "work_start": "",
                "dedupe_keys": {"name_birth": "党晓明_未知", "name_birthplace": "党晓明_未知", "official_source": "http://www.ansai.gov.cn/"}
            },
            "current_status": {"current_post": "区委副书记、代理区长", "current_org": "安塞区人民政府", "administrative_rank": "正县处级", "as_of": AS_OF, "is_current_confirmed": True, "source_ids": ["S011", "S012"]},
            "career_timeline": [
                {"start": "2025-2026", "end": "present", "org": "安塞区人民政府", "title": "区委副书记、代理区长", "level": "县处级", "location": "陕西延安安塞", "system": "government", "rank": "正县处级", "is_key_promotion": True, "notes": "2026-08-05主持区政府第41次常务会议；代理区长(接李延武任区长职)", "confidence": "confirmed", "source_ids": ["S011"]},
                {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "未获取党晓明任代区长的公开履历(出生、籍贯、学历、此前任职单位与时间)。", "confidence": "unverified", "source_ids": []},
            ],
            "organizations": [],
            "relationships": [
                {"person": "李延武", "person_id": "ansai_li_yanwu", "relationship_type": "overlap", "strength": "strong", "evidence": "代理区长——区委书记党政搭档；李延武原任区长升任书记后其继任", "overlap_org": "中共安塞区委/区政府", "overlap_period": "2025-2026-present", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S011"]},
                {"person": "王华", "person_id": "ansai_wang_hua", "relationship_type": "overlap", "strength": "medium", "evidence": "代理区长——区委常委副区长王华一同调研城建(2026-06)", "overlap_org": "安塞区政府", "overlap_period": "2026", "direction": "undirected", "confidence": "confirmed", "source_ids": ["S012"]},
            ],
            "governance_record": [
                {"period": "2026-07", "domain": "rural_revitalization", "achievement_or_event": "调研高桥镇，强调农文旅+生态休闲、乡村治理、信访化解、果园管理、隐患排查", "role_in_event": "带队调研", "measurable_outcome": "", "location": "延安安塞", "confidence": "confirmed", "source_ids": ["S012"]},
                {"period": "2026-06", "domain": "urban_construction", "achievement_or_event": "调研城市建设与管理，察看老旧小区提质、马家沟大桥等，强调民生工程与正确政绩观", "role_in_event": "带队调研", "measurable_outcome": "", "location": "延安安塞", "confidence": "confirmed", "source_ids": ["S012"]},
            ],
            "professional_profile": {
                "primary_specializations": ["政府治理", "城市建设", "三农"],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": ["government"],
                "geographic_pattern": ["延安市"],
                "promotion_velocity": {"summary": "任代理区长初期，履历公开有限", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {"trait": "pragmatic", "evidence": "走访镇村、城乡供水、城建一线，强调'过紧日子'、树正确政绩观", "confidence": "plausible", "source_ids": ["S012"]},
                ],
                "speech_themes": ["民生工程", "农文旅", "城乡供水", "乡村振兴"],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [{"type": "none_found", "description": "未发现公开纪律处分或负面报道", "date": "", "confidence": "unverified", "source_ids": []}],
            "source_register": [
                {"id": "S011", "title": "区政府第41次常务会议召开", "url": "http://www.ansai.gov.cn/xwzx/bdyw/2084801345474289666.html", "publisher": "安塞区融媒体中心", "published_at": "2026-08-05", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "确认'区委副书记、代理区长党晓明主持'"},
                {"id": "S012", "title": "党晓明调研高桥镇重点工作等系列新闻", "url": "http://www.ansai.gov.cn/xwzx/bdyw/2084099718841602049.html", "publisher": "安塞区融媒体中心", "published_at": "2026-08-03", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "调研活动与分工佐证"},
            ],
            "confidence_summary": {"identity": "primary", "current_role": "confirmed", "career_completeness": "thin", "relationship_confidence": "medium", "biggest_gap": "党晓明完整履历（出生、籍贯、学历、此前所有单位与任区长/副书记时间）"},
            "open_questions": [
                {"priority": "critical", "question": "党晓明的完整履历(出生、籍贯、学历、此前任职单位、任安塞区代理区长具体时间)", "why_it_matters": "代理区长关键人物", "suggested_queries": ["党晓明 安塞 简历", "党晓明 延安 任前公示", "延安市安塞区 代理区长 任命"], "last_attempted": AS_OF},
                {"priority": "high", "question": "前任区长(李延武)向党晓明交棒的具体时间与任命文件", "why_it_matters": "区府交接时间线", "suggested_queries": ["安塞区 代区长 党晓明 任命"], "last_attempted": AS_OF},
            ]
        }
    },
}


def write_person_json(data: dict, filename: str) -> Path:
    path = STAGING_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"  Wrote {path}")
    return path


def main():
    print(f"Building network for {SLUG}...")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print()

    run_build(
        slug=SLUG,
        persons=persons_data,
        organizations=organizations_data,
        positions=positions_data,
        relationships=relationships_data,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print()

    print("Writing person JSON files...")
    for key, entry in PERSON_JSON_TEMPLATE.items():
        write_person_json(entry["data"], entry["filename"])

    print()
    print("=" * 60)
    print(f"Build complete for {SLUG}")
    print(f"  {len(persons_data)} persons")
    print(f"  {len(organizations_data)} organizations")
    print(f"  {len(positions_data)} positions")
    print(f"  {len(relationships_data)} relationships")
    print(f"  {len(PERSON_JSON_TEMPLATE)} person JSONs")
    print("=" * 60)


if __name__ == "__main__":
    main()