#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 宝丰县 (Baofeng County), 平顶山市, 河南省.

Investigation date: 2026-08-06 (new build)
Task ID: henan_宝丰县
Level: 县
Targets: 县委书记 & 县长

Research sources (confirmed 2026-08-06, official primary source):
  - 宝丰县人民政府门户网站 www.baofeng.gov.cn 宝丰新闻/县常委会:
    - 2026-08-05 2026年度全县高质量发展综合绩效考评工作推进会 "县委书记刘海亮主持并讲话,县委副书记、县长龚宪君就重点任务作具体安排,县委副书记郑华永出席"
    - 2026-07-23 全县安全生产工作会议 "县委书记刘海亮主持并讲话;县委副书记、县长龚宪君安排;县委副书记郑华永、县人大常委会主任申红霞、县政协主席马胜昔等县四大班子领导参加"
    - 2026-07-30 龚宪君开展"八一"走访慰问 "(县委副书记、县长龚宪君率队)…郑华永、申红霞、王克平、赵卫东、李俊杰参加"
    - 2026-07-20 龚宪君主持召开县政府常务会议暨党组(扩大)会议 "(县长、县政府党组书记龚宪君)…王清政、王克平、崔仓、何四军等应邀出席"
    - 2026-07-31 宝丰县综合治税暨自然资源工作推进会 "(县委副书记、县长龚宪君主持会议)…陈国辉、赵卫东、陈卫东参加"
    - 2026-06-25 中国共产党宝丰县第十四次代表大会闭幕 刘海亮主持大会并讲话 (确认刘海亮任一届县委书记)
    - 2026-06-14 全县2026年争资工作会议 刘海亮主持并讲话; 2026-06-07 刘海亮调研高考; 2026-06-02 刘海亮调研"三夏"/秸秆
    - 2026-07-14 龚宪君调研生态环境和防汛; 2026-07-28 龚宪君调研督导防汛; 2026-07-04 龚宪君调研防溺水; 2026-04-30 龚宪君调研县高新技术产业开发区
  - 平顶山市/平顶山新闻网联动 (www.pds.gov.cn / www.pdsxww.com.cn):
    - 2026-06-04/2026-04-18 平顶山市委书记 陈向平 到宝丰县调研(汝瓷产业)
    - 2026-07-09/2026-03-30 平顶山市长 李明俊 到宝丰县接访下访; 2026-05-09 李明俊以人大代表身份到宝丰人大联络站

Confirmed roster (as of 2026-08):
- 刘海亮(县委书记): 现任宝丰县委书记,2026-06-25县第十四次党代会闭幕主持大会并讲话,确认任一届县委书记。
  出生年/籍贯/学历/入党/参加工作及任宝丰前完整履历待查(gap)。
- 龚宪君(县委副书记、县长,县政府党组书记): 主持县府常务会,围绕安全/防汛/科技创新/县域经济发展,主抓财税、土地清查、项目建设;
  其任庞前履历、出生信息待查(gap)。
- 郑华永(县委副书记); 申红霞(县人大常委会主任); 马胜昔(县政协主席) —— 四大班子主官。
- 县领导/部门领导:(王清政、王克平、陈国辉、赵卫东、李俊杰、陈卫东; 崔仓、何四军疑人大/政协副主席)—— 具体分工待官方"领导分工"页确认(web 采集受阻)。

Cross-region / interaction:
- 平顶山市委书记陈向平多次到宝丰调研(汝瓷产业),市长李明俊接访/人大代表——体现县委-市政紧密联系。
- 宝丰为"汝瓷之都",与平顶山市汝州(汝瓷主产区)存在产业-人事联动线索(跨县交流推断,需考据)。

Gaps flagged in person JSON `open_questions`:
  - 刘海亮/龚宪君出生年/籍贯/学历/入党/合计工作及任宝丰前完整履历
  - 前任宝丰县委书记(刘海前)及前任县长(龚宪前)及切换时间线
  - 常委会其余成员(副书记郑华永之外)现任具体职务、常务副县长/组织部长/纪委书记/宣传部长等
  - 纪委监委、监察委主任、法院院长、检察院检察长、人武部领导名单
"""

# process_tmp.py tokens: sqlite3, DB_PATH, GEXF_PATH
import json
import os
import sys
import shutil
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = STAGING_DIR.parents[2]  # repo root
SLUG = "宝丰县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

# Staging paths
DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"
PERSONS_DIR = STAGING_DIR
REPORT_DIR = STAGING_DIR

# ── Persons ─────────────────────────────────────────────────────────────────
persons = [
    # ═══ Core Leadership (targets) ═══
    {
        "id": 1,
        "name": "刘海亮",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共宝丰县委员会",
        "source": "宝丰县人民政府门户网站·宝丰新闻(2026-08-05绩效考评会;2026-06-25党代会闭幕;2026-06-14争资会议); official",
    },
    {
        "id": 2,
        "name": "龚宪君",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "宝丰县人民政府",
        "source": "宝丰县政府官网·龚宪君开展\"1\"走访慰问(2026-07-30)/县政府常务会议(2026-07-20)/综合治税会(2026-07-31); official",
    },
    # ═══ 四套班子主官 (official news) ═══
    {
        "id": 3,
        "name": "郑华永",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共宝丰县委员会",
        "source": "宝丰政府官网·全县安全生产会议(2026-07-22)/高质量发展绩效考评会(2026-08-04)",
    },
    {
        "id": 4,
        "name": "申红霞",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "宝丰县人大常委会",
        "source": "宝丰政府官网·全县安全生产会议(2026-07-22县人大班子领导)",
    },
    {
        "id": 5,
        "name": "马胜昔",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "政协宝丰县委员会",
        "source": "宝丰政府官网·全县安全生产会议(2026-07-22县四大班子领导)",
    },
    # ═══ Other 县领导 (official news, 职务以"县领导"占位待官方领导分工确认) ═══
    {
        "id": 6,
        "name": "王清政",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "宝丰县",
        "source": "宝丰政府官网·县政府常务会议暨党组(扩大)会议(2026-07-20应邀出席)",
    },
    {
        "id": 7,
        "name": "王克平",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "宝丰县",
        "source": "宝丰政府官网·龚宪君走访慰问(2026-07-30)/县政府常务会议(2026-07-20)",
    },
    {
        "id": 8,
        "name": "陈国辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "宝丰县",
        "source": "宝丰政府官网·高质量发展绩效考评会(2026-08-04)/综合治税会(2026-07-31)",
    },
    {
        "id": 9,
        "name": "赵卫东",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "宝丰县",
        "source": "宝丰政府官网·龚宪君走访慰问(2026-07-30)/综合治税会(2026-07-31)",
    },
    {
        "id": 10,
        "name": "李俊杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "宝丰县",
        "source": "宝丰政府官网·龚宪君开展“八一”走访慰问(2026-07-30)",
    },
    {
        "id": 11,
        "name": "陈卫东",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "宝丰县",
        "source": "宝丰政府官网·综合治税推进会(2026-07-31)",
    },
    {
        "id": 12,
        "name": "崔仓",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "宝丰县",
        "source": "宝丰政府官网·县政府常务会议暨党组(扩大)会议(2026-07-20应邀出席)",
    },
    {
        "id": 13,
        "name": "何四军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "宝丰县",
        "source": "宝丰政府官网·县政府常务会议暨党组(扩大)会议(2026-07-20应邀出席)",
    },
    # ═══ Cross-region figures (平顶山市委/市政府 interacting with 宝丰) ═══
    {
        "id": 14,
        "name": "陈向平",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平顶山市委书记",
        "current_org": "中共平顶山市委",
        "source": "本地平顶山市调查(report/20260805-平顶山市-领导网络调查报告.md); 宝丰政府官网(2026-06-04/04-18赴宝丰调研汝瓷)",
    },
    {
        "id": 15,
        "name": "李明俊",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "平顶山市委副书记、市长",
        "current_org": "平顶山市人民政府",
        "source": "宝丰政府官网(2026-07-09接访/2026-05-09人大代表活动/2026-03-30接访); 平顶山市调查报告",
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共宝丰县委员会", "type": "党委", "level": "县处级", "parent": "中共平顶山市委", "location": "宝丰县"},
    {"id": 2, "name": "宝丰县人民政府", "type": "政府", "level": "县处级", "parent": "平顶山市人民政府", "location": "宝丰县"},
    {"id": 3, "name": "宝丰县人大常委会", "type": "人大", "level": "县处级", "parent": "平顶山市人大常委会", "location": "宝丰县"},
    {"id": 4, "name": "政协宝丰县委员会", "type": "政协", "level": "县处级", "parent": "平顶山市政协", "location": "宝丰县"},
    {"id": 5, "name": "中共宝丰县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "平顶山市纪委监委", "location": "宝丰县"},
    {"id": 6, "name": "宝丰县监察委员会", "type": "纪委", "level": "县处级", "parent": "平顶山市监委", "location": "宝丰县"},
    {"id": 7, "name": "宝丰县高新技术产业开发区", "type": "开发区", "level": "县处级", "parent": "宝丰县人民政府", "location": "宝丰县"},
    {"id": 8, "name": "中共平顶山市委", "type": "党委", "level": "地厅级", "parent": "中共河南省委", "location": "平顶山市"},
    {"id": 9, "name": "平顶山市人民政府", "type": "政府", "level": "地厅级", "parent": "河南省人民政府", "location": "平顶山市"},
    {"id": 10, "name": "平顶山市人大常委会", "type": "人大", "level": "地厅级", "parent": "河南省人大常委会", "location": "平顶山市"},
    {"id": 11, "name": "平顶山市政协", "type": "政协", "level": "地厅级", "parent": "河南省政协", "location": "平顶山市"},
]

# ── Positions (person → org with title) ────────────────────────────────────
positions = [
    # 刘海亮 — 宝丰县委书记
    {"person_id": 1, "org_id": 1, "title": "宝丰县委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "2026-06-25县十四次党代会闭幕主持并讲话,确认任一县委书记; 2026-07-22主持全县安全生产会; 2026-08-04主持高质量发展绩效考评会"},
    # 龚宪君 — 县长
    {"person_id": 2, "org_id": 1, "title": "宝丰县委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "宝丰县人民政府县长、县政府党组书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "2026-07-20主持县政府常务会议暨党组(扩大)会议"},
    # 郑华永 — 县委副书记
    {"person_id": 3, "org_id": 1, "title": "宝丰县委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 申红霞 — 县人大常委会主任
    {"person_id": 4, "org_id": 3, "title": "宝丰县人大常委会主任", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "县四大班子领导"},
    # 马胜昔 — 县政协主席
    {"person_id": 5, "org_id": 4, "title": "宝丰县政协主席", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "县四大班子领导"},
    # 其他县领导
    {"person_id": 6, "org_id": 1, "title": "县领导", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "具体职务待确认"},
    {"person_id": 7, "org_id": 1, "title": "县领导", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "具体职务待确认"},
    {"person_id": 8, "org_id": 1, "title": "县领导", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "具体职务待确认"},
    {"person_id": 9, "org_id": 1, "title": "县领导", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "具体职务待确认"},
    {"person_id": 10, "org_id": 1, "title": "县领导", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "具体职务待确认"},
    {"person_id": 11, "org_id": 1, "title": "县领导", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "具体职务待确认"},
    {"person_id": 12, "org_id": 1, "title": "县领导", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "具体职务待确认"},
    {"person_id": 13, "org_id": 1, "title": "县领导", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "具体职务待确认"},
    # 陈向平 — 平顶山市委书记 (到宝丰调研)
    {"person_id": 14, "org_id": 8, "title": "平顶山市委书记", "start_date": "", "end_date": "present", "rank": "地厅级正职", "note": "2026-06-04/04-18赴宝丰调研汝瓷产业"},
    # 李明俊 — 平顶山市长
    {"person_id": 15, "org_id": 8, "title": "平顶山市委副书记", "start_date": "", "end_date": "present", "rank": "地厅级副职", "note": ""},
    {"person_id": 15, "org_id": 9, "title": "平顶山市市长", "start_date": "", "end_date": "present", "rank": "地厅级正职", "note": "2026-07-09/03-30到宝丰接访下访"},
]

# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    # 刘海亮 ↔ 龚宪君（党政正职搭档）
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "刘海亮任县委书记,龚宪君任县委副书记、县长,宝丰县党政正职搭档(权力核心双方)", "overlap_org": "宝丰县", "overlap_period": "2026至今"},
    # 刘海亮 ↔ 郑华永（副书记）
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县委书记与县委副书记", "overlap_org": "中共宝丰县委员会", "overlap_period": "当前"},
    # 龚宪君 ↔ 郑华永（县长-副书记）
    {"person_a": 2, "person_b": 3, "type": "same_system", "context": "均为宝丰县委副书记(龚兼县长)", "overlap_org": "中共宝丰县委员会", "overlap_period": "当前"},
    # 县四大班子联系
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "县委与县人大常委会(申红霞主任)工作班子", "overlap_org": "宝丰县", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "县委与县政协(马胜昔主席)工作班子", "overlap_org": "宝丰县", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 4, "type": "same_system", "context": "县政府与县人大班子工作联系", "overlap_org": "宝丰县", "overlap_period": "当前"},
    {"person_a": 2, "person_b": 5, "type": "same_system", "context": "县政府与县政协班子工作联系", "overlap_org": "宝丰县", "overlap_period": "当前"},
    # 平顶山市委书记/市长与宝丰互动
    {"person_a": 14, "person_b": 1, "type": "superior_subordinate", "context": "平顶山市委书记陈向平到宝丰县调研汝瓷产业,属市→县联系", "overlap_org": "宝丰县", "overlap_period": "2026-06/04"},
    {"person_a": 15, "person_b": 2, "type": "superior_subordinate", "context": "平顶山市长李明俊到宝丰县接访下访/以人大代表身份参加县活动", "overlap_org": "宝丰县", "overlap_period": "2026-07/05/03"},
]

# ── Person JSON Data ───────────────────────────────────────────────────────
person_files_data = [
    {
        "id": 1,
        "name": "刘海亮",
        "job": "县委书记",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河南省", "city": "平顶山市", "region": "宝丰县", "job": "县委书记",
                "task_id": "henan_宝丰县", "time_focus": "2026"
            },
            "identity": {
                "person_id": "baofeng_刘海亮",
                "name": "刘海亮", "aliases": [], "gender": "", "ethnicity": "",
                "birth": "", "birthplace": "", "native_place": "",
                "education": [],
                "party_join": "", "work_start": "",
                "dedupe_keys": {"name_birth": "刘海亮_", "name_birthplace": "刘海亮_", "official_profile_url": "http://www.baofeng.gov.cn"}
            },
            "current_status": {
                "current_post": "县委书记", "current_org": "中共宝丰县委员会",
                "administrative_rank": "县处级正职", "as_of": AS_OF,
                "is_current_confirmed": True, "source_ids": ["S001", "S002", "S003"]
            },
            "career_timeline": [
                {"start": "2026-06", "end": "present", "org": "中共宝丰县委员会", "title": "县委书记", "level": "县处级正职", "location": "宝丰县", "system": "party", "rank": "县处级正职", "is_key_promotion": True, "notes": "2026-06-25县第14次党代会闭幕主持并讲话(确认其一届县委书记); 2026-06-14主持全县争资会; 2026-06-07调研高考", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
                {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "刘海亮出生年/籍贯/学历/入党/参加工作及任宝丰县委书记前的完整履历未获公开一手资料(Baidu 403/Exa限流/Sogou/360验证码/Jina超时)", "confidence": "unverified", "source_ids": []}
            ],
            "organizations": [
                {"name": "中共宝丰县委员会", "role": "县委书记", "period": "2026至今", "source_ids": ["S001", "S002"]}
            ],
            "relationships": [
                {"person": "龚宪君", "person_id": "baofeng_龚宪君", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "刘海亮任县委书记,龚宪君任县委副书记、县长,宝丰县党政正职搭档", "overlap_org": "宝丰县", "overlap_period": "2026至今", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S001"]}
            ],
            "governance_record": [
                {"period": "2026-08", "domain": "economic_development", "achievement_or_event": "主持全县高质量发展绩效考评工作推进会,强调“工业优先、项目为王”,统筹经济调度", "role_in_event": "主持人", "measurable_outcome": "", "location": "宝丰县", "confidence": "confirmed", "source_ids": ["S001"]},
                {"period": "2026-07", "domain": "public_security", "achievement_or_event": "主持全县安全生产会议,强调压实'防线/底线'思维、分级管控", "role_in_event": "主持人", "measurable_outcome": "", "location": "宝丰县", "confidence": "confirmed", "source_ids": ["S002"]},
                {"period": "2026-06", "domain": "education", "achievement_or_event": "调研检查高考准备工作,强调周密细致保障高考安全平稳", "role_in_event": "主要负责人", "measurable_outcome": "", "location": "宝丰县", "confidence": "confirmed", "source_ids": ["S003"]}
            ],
            "professional_profile": {
                "primary_specializations": ["economic_development", "public_security", "rural_work"],
                "secondary_specializations": [],
                "career_pattern": "unknown", "systems_experience": ["party"],
                "geographic_pattern": ["宝丰县"],
                "promotion_velocity": {"summary": "宝丰县委书记任内活动密集(党代会/维稳/招商引资),完整晋升链条待考", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {"trait": "stability_oriented", "evidence": "2026-07-22主持安全生产会议,强调'红线意识''底线思维',压实'一把手'责任", "confidence": "confirmed", "source_ids": ["S002"]},
                    {"trait": "economic_driver", "evidence": "2026-08-04主持高质量发展考评,提出'工业优先、项目为王'", "confidence": "confirmed", "source_ids": ["S001"]}
                ],
                "speech_themes": ["工业优先、项目为王", "高质量发展综合绩效考评争先进位", "安全隐患'红线''底线'"],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "未发现负面信息", "date": AS_OF, "confidence": "unverified"}
            ],
            "source_register": [
                {"id": "S001", "title": "2026年度全县高质量发展综合绩效考评工作推进会", "url": "http://www.baofeng.gov.cn/contents/16432/51348.html", "publisher": "宝丰县融媒体中心", "published_at": "2026-08-05", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "县委书记刘海亮主持并讲话"},
                {"id": "S002", "title": "全县安全生产工作会议", "url": "http://www.baofeng.gov.cn/contents/16432/51297.html", "publisher": "宝丰县融媒体中心", "published_at": "2026-07-23", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "县委书记刘海亮主持并讲话"},
                {"id": "S003", "title": "中国共产党宝丰县第十四次代表大会闭幕报道", "url": "http://www.baofeng.gov.cn/channels/16432.html", "publisher": "宝丰县融媒体中心", "published_at": "2026-06-25", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "党代表刘海亮主持大会并由总书记讲话"}
            ],
            "confidence_summary": {
                "identity": "unverified",
                "current_role": "confirmed",
                "career_completeness": "thin", "relationship_confidence": "high",
                "biggest_gap": "刘海亮本人生辰/学历/籍贯/入党参加工作时间及任宝丰县委书记前的完整履历"
            },
            "open_questions": [
                {"priority": "critical", "question": "刘海亮出生年、籍贯、学历、入党/参加工作及任宝丰县委书记前的完整履历?", "why_it_matters": "还原其成长路径与早期关系网络", "suggested_queries": ["刘海亮 宝丰县委书记 简历", "刘海亮 平顶山 任前公示"], "last_attempted": AS_OF},
                {"priority": "high", "question": "前任宝丰县委书记是谁、刘海亮何时接任?", "why_it_matters": "梳理权力交接时间线", "suggested_queries": ["宝丰县 前县委书记 卸任", "宝丰县委书记 任免"], "last_attempted": AS_OF}
            ]
        }
    },
    {
        "id": 2,
        "name": "龚宪君",
        "job": "县长",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河南省", "city": "平顶山市", "region": "宝丰县", "job": "县长",
                "task_id": "henan_宝丰县", "time_focus": "2026"
            },
            "identity": {
                "person_id": "baofeng_龚宪君",
                "name": "龚宪君", "aliases": [], "gender": "", "ethnicity": "",
                "birth": "", "birthplace": "", "native_place": "",
                "education": [],
                "party_join": "", "work_start": "",
                "dedupe_keys": {"name_birth": "龚宪君_", "name_birthplace": "龚宪君_", "official_profile_url": "http://www.baofeng.gov.cn"}
            },
            "current_status": {
                "current_post": "县委副书记、县长", "current_org": "宝丰县人民政府",
                "administrative_rank": "县处级正职", "as_of": AS_OF,
                "is_current_confirmed": True, "source_ids": ["S001", "S002", "S003"]
            },
            "career_timeline": [
                {"start": "", "end": "present", "org": "中共宝丰县委员会", "title": "县委副书记", "level": "县处级副职", "location": "宝丰县", "system": "party", "rank": "县处级副职", "is_key_promotion": False, "notes": "", "confidence": "confirmed", "source_ids": ["S001", "S002", "S003"]},
                {"start": "未知", "end": "present", "org": "宝丰县人民政府", "title": "县长、县政府党组书记", "level": "县处级正职", "location": "宝丰县", "system": "government", "rank": "县处级正职", "is_key_promotion": True, "notes": "2026-07-20主持县政府常务会议暨党组(扩大)会议", "confidence": "confirmed", "source_ids": ["S002"]},
                {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "龚宪君出生年/籍贯、学历及任宝丰县长前履历未获公开一手资料", "confidence": "unverified", "source_ids": []}
            ],
            "organizations": [
                {"name": "宝丰县人民政府", "role": "县长", "period": "直至现在", "source_ids": ["S002"]},
                {"name": "中共宝丰县委员会", "role": "县委副书记", "period": "直至现在", "source_ids": ["S001", "S003"]}
            ],
            "relationships": [
                {"person": "刘海亮", "person_id": "baofeng_刘海亮", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "龚宪君任县长,刘海亮任县委书记,党政正职搭档", "overlap_org": "宝丰县", "overlap_period": "2026至今", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S001"]}
            ],
            "governance_record": [
                {"period": "2026-07", "domain": "public_security", "achievement_or_event": "主持县政府常务会议,部署安全生产、防汛救灾、科技创新、基层治理", "role_in_event": "主持人", "measurable_outcome": "", "location": "宝丰县", "confidence": "confirmed", "source_ids": ["S002"]},
                {"period": "2026-07", "domain": "economic_development", "achievement_or_event": "主持综合治税暨自然资源工作推进会,强调培植税源、土地清查", "role_in_event": "主持人", "measurable_outcome": "", "location": "宝丰县", "confidence": "confirmed", "source_ids": ["S003"]},
                {"period": "2026-07", "domain": "industry", "achievement_or_event": "调研高新开发区,聚焦碳新材料、高端装备制造主导产业", "role_in_event": "主要负责人", "measurable_outcome": "", "location": "宝丰县", "confidence": "confirmed", "source_ids": ["S002"]}
            ],
            "professional_profile": {
                "primary_specializations": ["fiscal_management", "project_management", "governance"],
                "secondary_specializations": [],
                "career_pattern": "unknown", "systems_experience": ["party", "government"],
                "geographic_pattern": ["宝丰县"],
                "promotion_velocity": {"summary": "现任县委副书记兼县长(县政府党组书记),司职财税/项目/安全治理,晋升链条待考", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {"trait": "pragmatic", "evidence": "2026-07-31综合治税会讲话强调'抓总抓重抓要''法治思维处理复杂问题'", "confidence": "confirmed", "source_ids": ["S003"]},
                    {"trait": "grassroots_oriented", "evidence": "多次赴防汛点位/开发区/走访慰问一线官兵民警", "confidence": "confirmed", "source_ids": ["S001", "S004"]}
                ],
                "speech_themes": ["法治思维", "钉钉子精神", "底线思维与极限思维", "防涝防汛"],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "未发现负面信息", "date": AS_OF, "confidence": "unverified"}
            ],
            "source_register": [
                {"id": "S001", "title": "龚宪君开展“八一”走访慰问", "url": "http://www.baofeng.gov.cn/contents/16432/51323.html", "publisher": "宝丰县融媒体中心", "published_at": "2026-07-30", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "县委副书记、县长龚宪君率队"},
                {"id": "S002", "title": "龚宪君主持召开县政府常务会议暨党组(扩大)会议", "url": "http://www.baofeng.gov.cn/contents/16432/51284.html", "publisher": "宝丰县融媒体中心", "published_at": "2026-07-20", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "县长、县政府党组书记龚宪君主持"},
                {"id": "S003", "title": "宝丰县综合治税暨自然资源工作推进会", "url": "http://www.baofeng.gov.cn/contents/16432/51325.html", "publisher": "宝丰县融媒体中心", "published_at": "2026-07-31", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "县委副书记、县长龚宪君主持并讲话"},
                {"id": "S004", "title": "龚宪君调研督导防汛/防涝", "url": "http://www.baofeng.gov.cn/contents/16432/51313.html", "publisher": "宝丰县融媒体中心", "published_at": "2026-07-29", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "深入排查积水风险"}
            ],
            "confidence_summary": {
                "identity": "unverified", "current_role": "confirmed",
                "career_completeness": "thin", "relationship_confidence": "high",
                "biggest_gap": "龚宪君出生年/籍贯/学历及任宝丰县长前履历"
            },
            "open_questions": [
                {"priority": "critical", "question": "龚宪君出生年、籍贯、学历、入党/参加工作及任宝丰县长前的履历?", "why_it_matters": "还原其培养背景与早期经历", "suggested_queries": ["龚宪君 宝丰 简历 此前", "龚宪君 平顶山 任命"], "last_attempted": AS_OF}
            ]
        }
    },
]

# ── Main ────────────────────────────────────────────────────────────────────
def main() -> None:
    sys.path.insert(0, str(BASE))
    from gov_relation.runner import run_build

    # Write DB+GEXF to staging
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

    # Write person JSON files
    for pf in person_files_data:
        fname = f"{TODAY}-河南省-平顶山市-{pf['job']}-{pf['name']}.json"
        path = PERSONS_DIR / fname
        with open(path, "w", encoding="utf-8") as f:
            json.dump(pf["data"], f, ensure_ascii=False, indent=2)
        print(f"  ✅ Person JSON: {path}")

    # ── Copy to canonical paths ────────────────────────────────────
    CANONICAL_DB = BASE / "data" / "database" / f"{SLUG}_network.db"
    CANONICAL_GEXF = BASE / "data" / "graph" / f"{SLUG}_network.gexf"
    CANONICAL_BUILD = BASE / f"build_{SLUG}_data.py"
    CANONICAL_PERSONS = BASE / "data" / "persons"

    CANONICAL_DB.parent.mkdir(parents=True, exist_ok=True)
    CANONICAL_GEXF.parent.mkdir(parents=True, exist_ok=True)
    CANONICAL_BUILD.parent.mkdir(parents=True, exist_ok=True)
    CANONICAL_PERSONS.mkdir(parents=True, exist_ok=True)

    shutil.copy2(DB_PATH, CANONICAL_DB)
    shutil.copy2(GEXF_PATH, CANONICAL_GEXF)
    shutil.copy2(__file__, CANONICAL_BUILD)

    for pf in person_files_data:
        src = PERSONS_DIR / f"{TODAY}-河南省-平顶山市-{pf['job']}-{pf['name']}.json"
        dst = CANONICAL_PERSONS / src.name
        if src.exists():
            shutil.copy2(src, dst)
            print(f"  ✅ Canonical person JSON: {dst}")

    print(f"\n📦 Canonical build script: {CANONICAL_BUILD}")
    print(f"📦 Canonical DB: {CANONICAL_DB}")
    print(f"📦 Canonical GEXF: {CANONICAL_GEXF}")
    print(f"\n✅ Done — {SLUG} data build complete.")


if __name__ == "__main__":
    main()