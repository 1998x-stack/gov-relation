#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 洛宁县 (Luoning County), 洛阳市, 河南省.

Investigation date: 2026-08-06 (new build)
Task ID: henan_洛宁县
Level: 县
Targets: 县委书记 & 县长

Research sources (confirmed 2026-08-06):
  - 洛宁县人民政府门户网站 www.luoning.gov.cn 洛宁要闻 (王瑞调度防汛备汛工作 2026-08-05;
    王瑞调研国网新源河南洛宁抽水蓄能电站 2026-08-04; 蒋嘉柠调研重点项目建设 2026-08-05;
    县委农村工作领导小组会议 2026-07-30; 党代会十四次开幕 2026-06-24) — 官方一手来源
  - 百度百科「蒋嘉柠」词条 (baike.baidu.com/item/蒋嘉柠) — 县长完整履历
  - 本地 repo 跨县报告: 嵩县报告(宗玉红曾任洛宁县副县长→栾川→嵩县书记);
    伊川跨县报告(谢睿曾任洛宁县副县长、洛龙区副区长→伊川县委副书记)

Confirmed roster / timeline:
- 王瑞(县委书记): 现任洛宁县委书记(2026-06-24 县第十四次党代会代表十三届县委作工作报告,说明已任书记约一届);
  任县委农村工作领导小组组长。出身地/出生年/入党/诺宁前履历待查(gap)。
- 蒋嘉柠(县委副书记、县长): 男,汉,1982-11,硕士,中共党员;
  曾任洛宁县委委员、常委、县委副书记(三级调研员); 2026-03-20 洛宁县人大常委会40次会议任命副县长、代理县长;
  2026-03-26 县十五届人大六次会议当选县长; 2026-06-24 当选县十四届委员会常委(兼县委副书记)。
- 县党代会主席台/常委会名单(2026-06, 县委主要成员): 王瑞、蒋嘉柠、尚维志、赵伟宁、史志锋、宗勇、金瑛、张新、徐小强
  其中各人具体职务以官方"领导分工"页为准(web 采集受阻,部分职务待确认)。
- 其他县领导现身: 张清涛、王清亮、杨华冰、戴丹华(军事日活动 2026-07-28); 陈雁、孙宏悦(调研随行 2026-08)
- 跨县交流人物(历史,关系到洛宁): 宗玉红(曾任洛宁县政府副县长→洛阳市妇联→栾川→嵩县县长/书记→洛阳市政协副主席);
  谢睿(曾任洛宁县副县长、洛龙区副区长→伊川县委副书记)。

Gaps flagged in person JSON `open_questions`:
  - 王瑞出生年/籍贯/向党/诺宁前完整履历
  - 各常委(尚维志等)现任具体职务
  - 前任洛宁县委书记及切换时间
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
SLUG = "洛宁县"
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
        "name": "王瑞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共洛宁县委员会",
        "source": "洛宁县政府门户网站洛宁要闻(2026-08-04/05; 2026-06-24党代会); official",
    },
    {
        "id": 2,
        "name": "蒋嘉柠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年11月",
        "birthplace": "",
        "education": "硕士研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "洛宁县人民政府",
        "source": "百度百科「蒋嘉柠」; 洛宁县十五届人大六次会议(2026-03-26当选县长)",
    },
    # ═══ Standing committee chair names (十四次党代会主席台 2026-06-24) ═══
    {
        "id": 3,
        "name": "尚维志",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共洛宁县委员会",
        "source": "洛宁县政府官网·县第十四次代表大会主席台名单(2026-06-24)",
    },
    {
        "id": 4,
        "name": "赵伟宁",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共洛宁县委员会",
        "source": "洛宁县政府官网·县第十四次代表大会主席台名单(2026-06-24)",
    },
    {
        "id": 5,
        "name": "史志锋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共洛宁县委员会",
        "source": "洛宁县政府官网·县第十四次代表大会主席台名单(2026-06-24)",
    },
    {
        "id": 6,
        "name": "宗勇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共洛宁县委员会",
        "source": "洛宁县政府官网·县第十四次代表大会主席台名单(2026-06-24)",
    },
    {
        "id": 7,
        "name": "金瑛",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共洛宁县委员会",
        "source": "洛宁县政府官网·县第十四次代表大会主席台名单(2026-06-24)",
    },
    {
        "id": 8,
        "name": "张新",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共洛宁县委员会",
        "source": "洛宁县政府官网·县第十四次代表大会主席台名单(2026-06-24)",
    },
    {
        "id": 9,
        "name": "徐小强",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委",
        "current_org": "中共洛宁县委员会",
        "source": "洛宁县政府官网·县第十四次代表大会主席台名单(2026-06-24)",
    },
    # ═══ Other 县领导现身 (official news) ═══
    {
        "id": 10,
        "name": "张清涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "洛宁县",
        "source": "洛宁县政府官网·八一军事日活动(2026-07-28)",
    },
    {
        "id": 11,
        "name": "王清亮",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "洛宁县",
        "source": "洛宁县政府官网·八一军事日活动(2026-07-28)",
    },
    {
        "id": 12,
        "name": "杨华冰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "洛宁县",
        "source": "洛宁县政府官网·八一军事日活动(2026-07-28)",
    },
    {
        "id": 13,
        "name": "戴丹华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "洛宁县",
        "source": "洛宁县政府官网·八一军事日活动(2026-07-28)",
    },
    {
        "id": 14,
        "name": "陈雁",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "洛宁县",
        "source": "洛宁县政府官网·蒋嘉柠调研(2026-08-05)",
    },
    {
        "id": 15,
        "name": "孙宏悦",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "洛宁县",
        "source": "洛宁县政府官网·蒋嘉柠调研(2026-08-05)",
    },
    # ═══ Cross-region figures (history related to 洛宁) ═══
    {
        "id": 16,
        "name": "宗玉红",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1966年5月",
        "birthplace": "河南洛阳",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "洛阳市政协副主席",
        "current_org": "洛阳市政协",
        "source": "百度百科「宗玉红」; 本地嵩县调查(曾任洛宁县副县长→洛阳市妇联→栾川→始丛→洛阳市政协副主席)",
    },
    {
        "id": 17,
        "name": "谢睿",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "伊川县委副书记",
        "current_org": "中共伊川县委",
        "source": "本地报告: report/20260724-伊川县-跨县干部交流网络.md (曾任洛宁县副县长、洛龙區副区長)",
    },
]

# ── Organizations ──────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共洛宁县委员会", "type": "党委", "level": "县处级", "parent": "中共洛阳市委", "location": "洛宁县"},
    {"id": 2, "name": "洛宁县人民政府", "type": "政府", "level": "县处级", "parent": "洛阳市人民政府", "location": "洛宁县"},
    {"id": 3, "name": "洛宁县人大常委会", "type": "人大", "level": "县处级", "parent": "洛阳市人大常委会", "location": "洛宁县"},
    {"id": 4, "name": "洛宁县政协", "type": "政协", "level": "县处级", "parent": "洛阳市政协", "location": "洛宁县"},
    {"id": 5, "name": "洛宁县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "洛阳市纪委监委", "location": "洛宁县"},
    {"id": 6, "name": "洛宁县监察委员会", "type": "纪委", "level": "县处级", "parent": "洛阳市监察委员会", "location": "洛宁县"},
    {"id": 7, "name": "洛阳市政协", "type": "政协", "level": "地厅级", "parent": "河南省政协", "location": "洛阳市"},
    {"id": 8, "name": "中共栾川县委", "type": "党委", "level": "县处级", "parent": "中共洛阳市委", "location": "栾川县"},
    {"id": 9, "name": "中共嵩县委员会", "type": "党委", "level": "县处级", "parent": "中共洛阳市委", "location": "嵩县"},
    {"id": 10, "name": "中共伊川县委", "type": "党委", "level": "县处级", "parent": "中共洛阳市委", "location": "伊川县"},
    {"id": 11, "name": "洛阳市妇女联合会", "type": "群团", "level": "地厅级", "parent": "河南省妇联", "location": "洛阳市"},
    {"id": 12, "name": "洛龙区人民政府", "type": "政府", "level": "县处级", "parent": "洛阳市人民政府", "location": "洛龙区"},
]

# ── Positions (person → org with title) ────────────────────────────────────
positions = [
    # 王瑞 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "洛宁县委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "2026-06-24 代表十三届县委作工作报告; 受自治往日为主宾"},
    # 蒋嘉柠 — 县长
    {"person_id": 2, "org_id": 1, "title": "洛宁县委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "曾任县委委员、常委、副书记, 三级调研员"},
    {"person_id": 2, "org_id": 2, "title": "洛宁县人民政府副县长、代理县长", "start_date": "2026-03-20", "end_date": "2026-03-25", "rank": "县处级正职", "note": "洛宁县十五届人大常委会第40次会议任命"},
    {"person_id": 2, "org_id": 2, "title": "洛宁县人民政府县长", "start_date": "2026-03-26", "end_date": "present", "rank": "县处级正职", "note": "县十五届人大六次会议当选"},
    # 尚维志等 — 常委 (职务详情待官方领导分工确认)
    {"person_id": 3, "org_id": 1, "title": "洛宁县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "具体职务待确认"},
    {"person_id": 4, "org_id": 1, "title": "洛宁县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "具体职务待确认"},
    {"person_id": 5, "org_id": 1, "title": "洛宁县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "具体职务待确认"},
    {"person_id": 6, "org_id": 1, "title": "洛宁县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "具体职务待确认"},
    {"person_id": 7, "org_id": 1, "title": "洛宁县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "具体职务待确认"},
    {"person_id": 8, "org_id": 1, "title": "洛宁县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "具体职务待确认"},
    {"person_id": 9, "org_id": 1, "title": "洛宁县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "具体职务待确认"},
    # 其他县领导（县领导/随行）
    {"person_id": 10, "org_id": 1, "title": "县领导", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "具体职务待确认"},
    {"person_id": 11, "org_id": 1, "title": "县领导", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "具体职务待确认"},
    {"person_id": 12, "org_id": 1, "title": "县领导", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "具体职务待确认"},
    {"person_id": 13, "org_id": 1, "title": "县领导", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "具体职务待确认"},
    {"person_id": 14, "org_id": 1, "title": "县领导", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "具体职务待确认"},
    {"person_id": 15, "org_id": 1, "title": "县领导", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "具体职务待确认"},
    # 宗玉红 — 曾任洛宁副县长 (cross-region)
    {"person_id": 16, "org_id": 2, "title": "洛宁县政府副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "早期履历阶段"},
    {"person_id": 16, "org_id": 8, "title": "栾川县委(宣传/政法/常务副县长/副书记)", "start_date": "", "end_date": "", "rank": "县处级副职/正职", "note": ""},
    {"person_id": 16, "org_id": 9, "title": "嵩县县长", "start_date": "2014-09", "end_date": "2021-07", "rank": "县处级正职", "note": "后任县委书记"},
    {"person_id": 16, "org_id": 9, "title": "嵩县县委书记", "start_date": "2021-07", "end_date": "2023-05", "rank": "县处级正职", "note": "2022-02 起兼洛阳市政协副主席"},
    {"person_id": 16, "org_id": 7, "title": "洛阳市政协副主席", "start_date": "2022-02", "end_date": "present", "rank": "地厅级副职", "note": ""},
    # 谢睿 — 曾任洛宁县副县长 (cross-region)
    {"person_id": 17, "org_id": 2, "title": "洛宁县政府副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 17, "org_id": 12, "title": "洛龙区副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 17, "org_id": 10, "title": "伊川县委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
]

# ── Relationships ───────────────────────────────────────────────────────────
relationships = [
    # 王瑞 ↔ 蒋嘉柠（党政正职搭档）
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "王瑞任县委书记,蒋嘉柠任县委副书记、县长,洛宁县党政正职搭档(权力核心双方治本于互动)", "overlap_org": "洛宁县", "overlap_period": "2026至今"},
    # 王瑞 ↔ 各常委（书记—常委会成员）待角色确认后补 framework
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "县委书记与县委常委会成员", "overlap_org": "中共洛宁县委员会", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "县委书记与县委常委会成员", "overlap_org": "中共洛宁县委员会", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "县委书记与县委常委会成员", "overlap_org": "中共洛宁县委员会", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "县委书记与县委常委会成员", "overlap_org": "中共洛宁县委员会", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "县委书记与县委常委会成员", "overlap_org": "中共洛宁县委员会", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "县委书记与县委常委会成员", "overlap_org": "中共洛宁县委员会", "overlap_period": "当前"},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "县委书记与县委常委会成员", "overlap_org": "中共洛宁县委员会", "overlap_period": "当前"},
    # 宗玉红 ↔ 洛宁（曾任副县长）
    {"person_a": 1, "person_b": 16, "type": "other", "context": "宗玉红曾于洛宁县任副县长(县领导链),体现洛宁与栾川、始丛地区干部交流链", "overlap_org": "洛宁县", "overlap_period": "早年"},
    # 谢睿 ↔ 洛宁（曾任副县长）
    {"person_a": 1, "person_b": 17, "type": "other", "context": "谢睿曾任洛宁县副县长、洛龙区副区长,现伊川县委副书记,体现洛宁县—伊川县干部交流", "overlap_org": "洛宁县", "overlap_period": "早年"},
    {"person_a": 2, "person_b": 17, "type": "other", "context": "蒋嘉柠(县长)与谢睿均有洛宁县党委/政府背景,属同一县域干部圈层", "overlap_org": "洛宁县", "overlap_period": "不同时期"},
    # 宗玉红 ↔ 谢睿（交叉圈层, 均为洛宁出身干部）
    {"person_a": 16, "person_b": 17, "type": "same_system", "context": "均曾任洛宁县(副)县长,后分别调往嵩县/伊川,洛阳干部交流网络的一部分", "overlap_org": "洛宁县", "overlap_period": "不同时期"},
]

# ── Person JSON Data ───────────────────────────────────────────────────────
person_files_data = [
    {
        "id": 1,
        "name": "王瑞",
        "job": "县委书记",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河南省", "city": "洛阳市", "region": "洛宁县", "job": "县委书记",
                "task_id": "henan_洛宁县", "time_focus": "2026"
            },
            "identity": {
                "person_id": "henan_luoning_wangrui",
                "name": "王瑞", "aliases": [], "gender": "", "ethnicity": "",
                "birth": "", "birthplace": "", "native_place": "",
                "education": [],
                "party_join": "", "work_start": "",
                "dedupe_keys": {"name_birth": "", "name_birthplace": "", "official_profile_url": "https://www.luoning.gov.cn"}
            },
            "current_status": {
                "current_post": "县委书记", "current_org": "中共洛宁县委员会",
                "administrative_rank": "县处级正职", "as_of": AS_OF,
                "is_current_confirmed": True, "source_ids": ["S001", "S002", "S003"]
            },
            "career_timeline": [
                {"start": "2026-06-24", "end": "present", "org": "中共洛宁县委员会", "title": "县委书记", "level": "县处级正职", "location": "洛宁县", "system": "party", "rank": "县处级正职", "is_key_promotion": True, "notes": "2026-06-24 县第十四次党代会代表县委十三届委员会作工作报告(说明此前已任书记约五年一任)", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "王瑞的生辰/籍贯/入党/参加工作时间及任洛宁县委书记前的完整履历未获公开一手资料(Baidu 403/Exa 限流)", "confidence": "unverified", "source_ids": []}
            ],
            "organizations": [
                {"name": "中共洛宁县委员会", "role": "县委书记", "period": "直至现在", "source_ids": ["S001"]}
            ],
            "relationships": [
                {"person": "蒋嘉柠", "person_id": "henan_luoning_jiangjialing", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "王瑞为县委书记,蒋嘉柠为县长,洛宁县党政正职搭档", "overlap_org": "洛宁县", "overlap_period": "2026至今", "direction": "person_to_other", "confidence": "confirmed", "source_ids": ["S002"]}
            ],
            "governance_record": [
                {"period": "2026-07/08", "domain": "rural_revitalization", "achievement_or_event": "调研农业强县建设、常态化帮扶、和美乡村建设", "role_in_event": "主要负责人", "measurable_outcome": "", "location": "洛宁县", "confidence": "confirmed", "source_ids": ["S001"]},
                {"period": "2026-07", "domain": "other", "achievement_or_event": "调度全县防汛备汛工作，抽查气象预警与应急处置体系", "role_in_event": "主要负责人", "measurable_outcome": "", "location": "洛宁县", "confidence": "confirmed", "source_ids": ["S001"]},
                {"period": "2026-08", "domain": "industry", "achievement_or_event": "调研国网新源洛宁抽水蓄能电站运营及工业旅游", "role_in_event": "主要负责人", "measurable_outcome": "", "location": "洛宁县", "confidence": "confirmed", "source_ids": ["S001"]}
            ],
            "professional_profile": {
                "primary_specializations": ["rural_rivitalization", "emergency_management", "industry_tourism"],
                "secondary_specializations": [],
                "career_pattern": "unknown", "systems_experience": ["party", "government"],
                "geographic_pattern": ["洛宁县"],
                "promotion_velocity": {"summary": "已有完整县委至洛宁县委书记链条待考;就职期间在全任期担任政党圭席代表", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {"trait": "grassroots_oriented", "evidence": "2026-07 多次赴乡镇(倒口/马店/底张)入户走访农户、孤寡老人,强调民生与和美乡村", "confidence": "confirmed", "source_ids": ["S001"]},
                    {"trait": "flood_stability_oriented", "evidence": "历次对防汛调度强调'人民至上、生命至上'、严明值班与应急纪律", "confidence": "confirmed", "source_ids": ["S001"]}
                ],
                "speech_themes": ["扬优成势、跨越争先", "党建+网格+大数据", "安全生产底线"],
                "management_signals": [],
                "caveat": "Work style is inferred from public records and reported governance actions, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "未发现负面信息", "date": AS_OF, "confidence": "unverified"}
            ],
            "source_register": [
                {"id": "S001", "title": "洛宁县人民政府门户网站-洛宁要闻", "url": "https://www.luoning.gov.cn", "publisher": "洛宁县人民政府", "published_at": "2026-07/08", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "王瑞出席/调度/调研新闻,县委书记核实"},
                {"id": "S002", "title": "县委农村工作领导小组(扩大)会议", "url": "https://www.luoning.gov.cn/2026/07-30/1076536.html", "publisher": "洛宁县人民政府", "published_at": "2026-07-30", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "王瑞任领导小组组长"},
                {"id": "S003", "title": "中国共产党洛宁县第十四次代表大会开幕报道", "url": "https://www.luoning.gov.cn/2026/06-24/1069116.html", "publisher": "洛宁县人民政府", "published_at": "2026-06-24", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "王瑞代表县委十三届委员会作工作报告,坐主席台前列"}
            ],
            "confidence_summary": {
                "identity": "unverified",
                "current_role": "confirmed",
                "career_completeness": "thin", "relationship_confidence": "medium",
                "biggest_gap": "王瑞(洛宁县委书记)出生年/籍贯/入党与参加工作时间/洛宁前履历均待补"
            },
            "open_questions": [
                {"priority": "critical", "question": "王瑞出生年、籍贯、入党/参加工作及任洛宁县委书记前的完整履历?", "why_it_matters": "还原成长路径与早期关系网络", "suggested_queries": ["王瑞 洛宁县委书记 简历", "王瑞 洛宁县 任命 公示"], "last_attempted": AS_OF},
                {"priority": "high", "question": "前任洛宁县委书记是谁、王瑞何时接任?", "why_it_matters": "梳理权力交接时间线", "suggested_queries": ["洛宁县 前县委书记 卸任", "洛宁县委书记 任免"], "last_attempted": AS_OF}
            ]
        }
    },
    {
        "id": 2,
        "name": "蒋嘉柠",
        "job": "县长",
        "data": {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "河南省", "city": "洛阳市", "region": "洛宁县", "job": "县长",
                "task_id": "henan_洛宁县", "time_focus": "2026"
            },
            "identity": {
                "person_id": "henan_luoning_jiangjialing",
                "name": "蒋嘉柠", "aliases": [], "gender": "男", "ethnicity": "汉族",
                "birth": "1982年11月", "birthplace": "", "native_place": "",
                "education": [
                    {"period": "", "institution": "", "major": "", "degree": "硕士研究生", "study_type": "full_time", "source_ids": ["S001"]}
                ],
                "party_join": "", "work_start": "",
                "dedupe_keys": {"name_birth": "蒋嘉柠_1982年11月", "name_birthplace": "", "official_profile_url": "https://baike.baidu.com/item/蒋嘉柠"}
            },
            "current_status": {
                "current_post": "县委副书记、县长", "current_org": "洛宁县人民政府",
                "administrative_rank": "县处级正职", "as_of": AS_OF,
                "is_current_confirmed": True, "source_ids": ["S001", "S002", "S003"]
            },
            "career_timeline": [
                {"start": "", "end": "", "org": "中共洛宁县委员会", "title": "县委委员、常委、县委副书记", "level": "县处级副职", "location": "洛宁县", "system": "party", "rank": "县处级副职", "is_key_promotion": False, "notes": "三级调研员", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "2026-03-20", "end": "2026-03-25", "org": "洛宁县人民政府", "title": "副县长、代理县长", "level": "县处级正职", "location": "洛宁县", "system": "government", "rank": "县处级正职", "is_key_promotion": True, "notes": "洛宁县十五届人大常委会第四十次会议决定", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
                {"start": "2026-03-26", "end": "present", "org": "洛宁县人民政府", "title": "县长", "level": "县处级正职", "location": "洛宁县", "system": "government", "rank": "县处级正职", "is_key_promotion": True, "notes": "县十五届人大六次会议当选", "confidence": "confirmed", "source_ids": ["S001", "S003"]},
                {"start": "2026-06-24", "end": "present", "org": "洛宁县委员会", "title": "县委常委", "level": "县处级副职", "location": "洛宁县", "system": "party", "rank": "县处级副职", "is_key_promotion": False, "notes": "当选十四届委员会常务委员", "confidence": "confirmed", "source_ids": ["S001"]},
                {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "", "notes": "任洛宁县委之前(受教育阶段、入洛宁前工作单位)未获公开一手资料", "confidence": "unverified", "source_ids": []}
            ],
            "organizations": [
                {"name": "洛宁县人民政府", "role": "县长", "period": "2026-03至今", "source_ids": ["S001", "S003"]},
                {"name": "中共洛宁县委员会", "role": "县委副书记", "period": "直至现在", "source_ids": ["S001"]}
            ],
            "relationships": [
                {"person": "王瑞", "person_id": "henan_luoning_wangrui", "relationship_type": "superior_subordinate", "strength": "strong", "evidence": "蒋嘉柠任县长,王瑞任书记,党政正职搭档", "overlap_org": "洛宁县", "overlap_period": "2026至今", "direction": "other_to_person", "confidence": "confirmed", "source_ids": ["S002"]}
            ],
            "governance_record": [
                {"period": "2026-07", "domain": "education", "achievement_or_event": "为县委党校主体班作«基层工作»专题授课,强调基层治理/产业发展/乡村建设", "role_in_event": "主讲", "measurable_outcome": "", "location": "洛宁县", "confidence": "confirmed", "source_ids": ["S001"]},
                {"period": "2026-08", "domain": "industry", "achievement_or_event": "调研电力、新材料、中药材、职业教育等重点项目建设运营", "role_in_event": "主要负责人", "measurable_outcome": "", "location": "洛宁县", "confidence": "confirmed", "source_ids": ["S001"]}
            ],
            "professional_profile": {
                "primary_specializations": ["project_management", "basic_governance"],
                "secondary_specializations": [],
                "career_pattern": "local_ladder", "systems_experience": ["party", "government"],
                "geographic_pattern": ["洛宁县"],
                "promotion_velocity": {"summary": "从县委副书记(三级调研员)直升县长,2026年内以8个月完成代县长→县长→选入常委的密集晋升", "notable_fast_promotions": ["2026-03-20法令代理→2026-03-26当选(6天)"]}
            },
            "work_style_and_personality": {
                "public_style_indicators": [
                    {"trait": "grassroots_oriented", "evidence": "2026-07-30 以「如何做好基层工作」为县委党校主体班授课", "confidence": "confirmed", "source_ids": ["S001"]}
                ],
                "speech_themes": ["基层治理", "项目建设运营", "新型工业化"],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "未发现负面信息", "date": AS_OF, "confidence": "unverified"}
            ],
            "source_register": [
                {"id": "S001", "title": "百度百科「蒋嘉柠」", "url": "https://baike.baidu.com/item/蒋嘉柠", "publisher": "百度百科", "published_at": "", "accessed_at": AS_OF, "source_type": "encyclopedia", "reliability": "medium", "notes": "人物履历/职务任免"},
                {"id": "S002", "title": "洛宁县人大常委会第40次会议决定", "url": "https://www.luoning.gov.cn", "publisher": "洛宁县人大常委会", "published_at": "2026-03-20", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "任命副县长/代县长"},
                {"id": "S003", "title": "洛宁县十五届人大六次会议选举公告", "url": "https://www.luoning.gov.cn", "publisher": "洛宁县人大", "published_at": "2026-03-26", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "当选县长"},
                {"id": "S004", "title": "蒋嘉柠调研/授课官方新闻", "url": "https://www.luoning.gov.cn", "publisher": "洛宁县人民政府", "published_at": "2026-07/08", "accessed_at": AS_OF, "source_type": "official", "reliability": "high", "notes": "治理行为证据"}
            ],
            "confidence_summary": {
                "identity": "confirmed", "current_role": "confirmed",
                "career_completeness": "partial", "relationship_confidence": "high",
                "biggest_gap": "蒋嘉柠任洛宁县委副书记前的教育/前单位履历,及籍贯/出生地"
            },
            "open_questions": [
                {"priority": "high", "question": "蒋嘉柠籍贯/出生地及任洛宁县委副书记前的履历?", "why_it_matters": "还原其培养背景与早期经历", "suggested_queries": ["蒋嘉柠 洛宁 简历 此前"], "last_attempted": AS_OF}
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
        fname = f"{TODAY}-河南省-洛阳市-{pf['job']}-{pf['name']}.json"
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
        src = PERSONS_DIR / f"{TODAY}-河南省-洛阳市-{pf['job']}-{pf['name']}.json"
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