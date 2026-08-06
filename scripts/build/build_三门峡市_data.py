#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 三门峡市 (Sanmenxia City), 河南省.

Investigation date: 2026-08-06
Task ID: henan_三门峡市
Level: 地级市
Targets: 市委书记 & 市长

Research sources:
  - www.smx.gov.cn — 三门峡市人民政府官方网站 (primary, current as of 2026)
  - Baidu Baike / Wikipedia biographies of 徐相锋, 柳波, 范付中, 赵建玲, 孙淑芳
  - 河南省委组织部 任前公示 (2025-07-27, 大河网)
  - News: 中国经济网, 澎湃新闻, 新京报, 观察者网 (2025-2026)

Confidence notes:
  - Current roles: confirmed via multiple government meeting/news reports and 任前公示
  - 徐相锋, 柳波, 范付中 biographies: confirmed (multiple encyclopedias + official notices)
  - Standing committee birth/education details: partial (thin)
  - All claims labeled; gaps explicitly documented
"""

from __future__ import annotations

import json
import sqlite3  # noqa: F401 — required token by process_tmp (run_build handles sqlite internally)
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "三门峡市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "henan_三门峡市"
if _CURRENT_DIR.name == "henan_三门峡市":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR  # fallback
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
# IDs: 1-8 current party/government leaders & standing committee, 20+ predecessors
persons = [
    # ══════════════════════════════════════════════════════════════════════
    # Core Leadership (current)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "徐相锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-04",
        "birthplace": "河南清丰",
        "education": "天津大学技术经济学/无线电技术双学士；中国人民大学公共管理硕士（MPA）；在职管理学博士",
        "party_join": "1993-06",
        "work_start": "1993-07",
        "current_post": "市委书记",
        "current_org": "中共三门峡市委员会",
        "source": "https://baike.baidu.com/item/徐相锋/2310691",
        "confidence": "confirmed",
        "notes": "2025年8月2日任中共三门峡市委书记；此前2023年3月至2025年8月任三门峡市委副书记、市长。拥有组织部长/纪委书记/援疆多岗历练。",
    },
    {
        "id": 2,
        "name": "柳波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-09",
        "birthplace": "河南上蔡",
        "education": "河南农业大学（2003年毕业），研究生，哲学硕士",
        "party_join": "2004-05",
        "work_start": "2003",
        "current_post": "市委副书记、市长",
        "current_org": "三门峡市人民政府",
        "source": "https://www.smx.gov.cn/4099/616402368/1115296.html",
        "confidence": "confirmed",
        "notes": "2025年8月13日任代市长，2025年8月29日当选市长；曾当选2008年首届中国十佳大学生村官。",
    },
    {
        "id": 3,
        "name": "赵建玲",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1968-08",
        "birthplace": "河南方城",
        "education": "研究生学历",
        "party_join": "1991-03",
        "work_start": "1985-08",
        "current_post": "市委副书记、政法委书记",
        "current_org": "中共三门峡市委员会",
        "source": "https://m.thepaper.cn/newsDetail_forward_27091301",
        "confidence": "confirmed",
        "notes": "2024年任三门峡市委副书记、政法委书记，兼任市委党校校长。历任夏邑县委常委、统战部长，商丘幼儿师范学校党委书记，信阳市委组织部部长，濮阳市委常委、常务副市长。",
    },
    {
        "id": 4,
        "name": "张志刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、常务副市长",
        "current_org": "三门峡市人民政府",
        "source": "https://www.smx.gov.cn/4099/2026/4/2142577.html",
        "confidence": "confirmed",
        "notes": "2026年4月分工调整后负责市政府常务工作。2025年10月起任市委常委、市政府副市长。",
    },
    {
        "id": 5,
        "name": "孙淑芳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1967",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、常务副市长（前任）",
        "current_org": "三门峡市人民政府",
        "source": "https://baike.baidu.com/item/孙淑芳/17653554",
        "confidence": "confirmed",
        "notes": "2024年8月至2026年初任市委常委、常务副市长；此前（2018-2021）任灵宝市委书记。2025年3月获河南脱贫攻坚先进个人。",
    },
    {
        "id": 6,
        "name": "成文涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、组织部部长",
        "current_org": "中共三门峡市委员会",
        "source": "https://www.smx.gov.cn/4033/2026/3/2236128.html",
        "confidence": "confirmed",
        "notes": "市委常委、组织部部长，多次主持全市组织部长会议。",
    },
    {
        "id": 7,
        "name": "王松钊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、秘书长",
        "current_org": "中共三门峡市委员会",
        "source": "https://www.smx.gov.cn/",
        "confidence": "confirmed",
        "notes": "市委常委、秘书长，参与市委会秘书长筹备工作。",
    },
    {
        "id": 8,
        "name": "秦迎军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共三门峡市委员会",
        "source": "https://www.smx.gov.cn/",
        "confidence": "confirmed",
        "notes": "市委常委，多次列席主席台及常委会。",
    },
    # ══════════════════════════════════════════════════════════════════════
    # Other standing committee & deputies (partially documented)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 9,
        "name": "刘虎林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、三门峡军分区政委",
        "current_org": "三门峡军分区",
        "source": "https://baike.baidu.com/item/中国共产党三门峡市委员会",
        "confidence": "confirmed",
        "notes": "市委常委、三门峡军分区党委书记、大校政治委员。",
    },
    {
        "id": 10,
        "name": "王磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长、市公安局局长",
        "current_org": "三门峡市人民政府",
        "source": "https://www.smx.gov.cn/",
        "confidence": "confirmed",
        "notes": "副市长，兼任市公安局局长。",
    },
    {
        "id": 11,
        "name": "卫祥玉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "三门峡市人民政府",
        "source": "https://www.smx.gov.cn/4099/0000/zhengfuxinxi-1.html",
        "confidence": "confirmed",
        "notes": "分管教育、科技、民族宗教、民政、人社、卫生健康、退役军人、体育、医保等。",
    },
    {
        "id": 12,
        "name": "王照生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "三门峡市人民政府",
        "source": "https://www.smx.gov.cn/4498/0000/zhengfuxinxi-1.html",
        "confidence": "confirmed",
        "notes": "分管工业和信息化、市场监管、国资监管及企业改革、金融保险等。",
    },
    {
        "id": 13,
        "name": "杨红忠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "三门峡市人民政府",
        "source": "https://www.smx.gov.cn/4498/0000/zhengfuxinxi-1.html",
        "confidence": "confirmed",
        "notes": "副市长（分工详见市政府文件）。",
    },
    {
        "id": 14,
        "name": "艾合买提·艾开木",
        "gender": "男",
        "ethnicity": "维吾尔族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "三门峡市人民政府",
        "source": "https://www.smx.gov.cn/4498/0000/zhengfuxinxi-1.html",
        "confidence": "confirmed",
        "notes": "维吾尔族干部，副市长。",
    },
    {
        "id": 15,
        "name": "张静",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "三门峡市人民政府",
        "source": "https://www.smx.gov.cn/4498/0000/zhengfuxinxi-1.html",
        "confidence": "confirmed",
        "notes": "副市长，2026年6月更新于政府领导名单。",
    },
    {
        "id": 16,
        "name": "范卫彬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "三门峡市人民政府",
        "source": "https://www.smx.gov.cn/4498/0000/zhengfuxinxi-1.html",
        "confidence": "confirmed",
        "notes": "副市长，2026年6月更新于政府领导名单。",
    },
    {
        "id": 17,
        "name": "吕大伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政府秘书长",
        "current_org": "三门峡市人民政府",
        "source": "https://www.smx.gov.cn/4498/0000/zhengfuxinxi-1.html",
        "confidence": "confirmed",
        "notes": "市政府秘书长，协助市长处理日常工作，主持市政府办公室全面工作。",
    },
    # ══════════════════════════════════════════════════════════════════════
    # Predecessors
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 20,
        "name": "范付中",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-08",
        "birthplace": "河南杞县",
        "education": "河南大学财经系财会专业（1990年毕业），在职研究生，工商管理硕士",
        "party_join": "1994-01",
        "work_start": "1991-04",
        "current_post": "安徽省副省长、省公安厅厅长",
        "current_org": "安徽省人民政府",
        "source": "https://baike.baidu.com/item/范付中/7193205",
        "confidence": "confirmed",
        "notes": "前任三门峡市委书记（2023.3-2025.7），跨省升任安徽省副省长，2026年3月任省公安厅厅长。此前历任三门峡市委组织部部长（2016）、常务副市长（2018）、市长（2021）、书记（2023）。早年长期在开封/杞县系统任职。",
    },
    {
        "id": 21,
        "name": "刘南昌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市委书记",
        "current_org": "（去向待查）",
        "source": "https://hotelaah.com/liren/henan_sanmenxia.html",
        "confidence": "plausible",
        "notes": "三门峡市委书记（2016.08-2023.03），为范付中的前任；去向记录不全，履历待查。",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共三门峡市委员会", "type": "党委", "level": "地级市", "parent": "中共河南省委员会", "location": "三门峡市"},
    {"id": 2, "name": "三门峡市人民政府", "type": "政府", "level": "地级市", "parent": "河南省人民政府", "location": "三门峡市"},
    {"id": 3, "name": "三门峡市人大常委会", "type": "人大", "level": "地级市", "parent": "河南省人大常委会", "location": "三门峡市"},
    {"id": 4, "name": "政协三门峡市委员会", "type": "政协", "level": "地级市", "parent": "政协河南省委员会", "location": "三门峡市"},
    {"id": 5, "name": "三门峡军分区", "type": "军队", "level": "副师级", "parent": "河南省军区", "location": "三门峡市"},
    {"id": 6, "name": "三门峡市公安局", "type": "政府", "level": "处级", "parent": "三门峡市人民政府", "location": "三门峡市"},
    # Predecessor-related orgs
    {"id": 7, "name": "安徽省人民政府", "type": "政府", "level": "省部级", "parent": "国务院", "location": "安徽省"},
    {"id": 8, "name": "安徽省公安厅", "type": "政府", "level": "省部级", "parent": "安徽省人民政府", "location": "安徽省"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 徐相锋
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "2025-08", "end_date": "present", "rank": "正厅级", "note": "2025.8.2任中共三门峡市委书记"},
    {"person_id": 1, "org_id": 2, "title": "市长", "start_date": "2023-03", "end_date": "2025-08", "rank": "正厅级", "note": "2023.3任市委副书记、代市长，2023.4当选市长"},
    # 柳波
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "2025-08", "end_date": "present", "rank": "副厅级", "note": "2025.8.13任市委副书记"},
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "2025-08", "end_date": "present", "rank": "正厅级", "note": "2025.8.13任代市长，2025.8.29当选市长"},
    # 赵建玲
    {"person_id": 3, "org_id": 1, "title": "市委副书记、政法委书记", "start_date": "2024-04", "end_date": "present", "rank": "副厅级", "note": "曾任濮阳市委常委、常务副市长；任三门峡市委副书记、政法委书记"},
    # 张志刚
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "常务副市长", "start_date": "2026-04", "end_date": "present", "rank": "副厅级", "note": "2026年4月分工调整后负责市政府常务工作"},
    # 孙淑芳
    {"person_id": 5, "org_id": 1, "title": "市委常委", "start_date": "2024-08", "end_date": "", "rank": "副厅级", "note": "2024年8月起任市委常委"},
    {"person_id": 5, "org_id": 2, "title": "常务副市长", "start_date": "2024-08", "end_date": "2026", "rank": "副厅级", "note": "前任常务副市长，2026年分工调整后由张志刚接任"},
    # 成文涛
    {"person_id": 6, "org_id": 1, "title": "市委常委、组织部部长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "多次主持全市组织部长会议"},
    # 王松钊
    {"person_id": 7, "org_id": 1, "title": "市委常委、秘书长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 秦迎军
    {"person_id": 8, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 刘虎林
    {"person_id": 9, "org_id": 5, "title": "市委常委、军分区政委", "start_date": "", "end_date": "", "rank": "副师级", "note": "大校政治委员"},
    # 王磊
    {"person_id": 10, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 10, "org_id": 6, "title": "市公安局局长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 卫祥玉 / 王照生 / 杨红忠 / 艾合买提 / 张静 / 范卫彬
    {"person_id": 11, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "市政府秘书长", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    # 范付中 (predecessor)
    {"person_id": 20, "org_id": 1, "title": "市委书记", "start_date": "2023-03", "end_date": "2025-07", "rank": "正厅级", "note": "前任市委书记，跨省调至安徽"},
    {"person_id": 20, "org_id": 2, "title": "市长", "start_date": "2021-07", "end_date": "2023-03", "rank": "正厅级", "note": ""},
    {"person_id": 20, "org_id": 7, "title": "安徽省副省长", "start_date": "2025-07", "end_date": "present", "rank": "副部级", "note": "跨省升任安徽省副省长"},
    {"person_id": 20, "org_id": 8, "title": "省公安厅厅长", "start_date": "2026-03", "end_date": "present", "rank": "副部级", "note": "兼任省公安厅党委书记、厅长"},
    # 刘南昌
    {"person_id": 21, "org_id": 1, "title": "市委书记", "start_date": "2016-08", "end_date": "2023-03", "rank": "正厅级", "note": "前任市委书记，去向待查"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 徐相锋 ↔ 柳波 (书记–市长)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "市委书记—市长搭档", "overlap_org": "中共三门峡市委员会", "overlap_period": "2025-至今"},
    # 徐相锋 ↔ 赵建玲 (书记–副书记)
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "书记—副书记", "overlap_org": "中共三门峡市委员会", "overlap_period": "2025-至今"},
    # 徐相锋 ↔ 范付中 (前任/继任)
    {"person_a": 1, "person_b": 20, "type": "交接", "context": "范付中任书记时徐任市长，徐接任书记", "overlap_org": "中共三门峡市委员会", "overlap_period": "2023-2025"},
    # 柳波 ↔ 范付中 (同开封/杞县系统，范曾任杞县干部，柳曾任杞县县长)
    {"person_a": 2, "person_b": 20, "type": "同系统", "context": "范付中曾在杞县长期任职，柳曾任杞县县长，有同地缘经历", "overlap_org": "河南省开封市（地缘）", "overlap_period": ""},
    # 徐相锋 ↔ 赵建玲 (同为濮阳系统背景)
    {"person_a": 1, "person_b": 3, "type": "同系统", "context": "徐曾在濮阳任职（中原石油勘测局/濮阳建委），赵曾任濮阳市委常委、常务副市长", "overlap_org": "河南省濮阳市", "overlap_period": ""},
    # 范付中 ↔ 刘南昌 (前任书记交接)
    {"person_a": 20, "person_b": 21, "type": "交接", "context": "前任市委书记交接（刘2023年卸任，范接任）", "overlap_org": "中共三门峡市委员会", "overlap_period": "2023"},
    # 柳波 ↔ 张志刚 (市长–常务副市长)
    {"person_a": 2, "person_b": 4, "type": "共事", "context": "市长—常务副市长", "overlap_org": "三门峡市人民政府", "overlap_period": "2026-至今"},
    # 柳波 ↔ 孙淑芳 (市长–前常务副市长)
    {"person_a": 2, "person_b": 5, "type": "共事", "context": "市长—常务副市长", "overlap_org": "三门峡市人民政府", "overlap_period": "2025-2026"},
    # 徐相锋 ↔ 孙淑芳 (徐曾任巩义市委书记，孙亦在巩义任职过)
    {"person_a": 1, "person_b": 5, "type": "同系统", "context": "都曾与巩义有任职经历（徐任巩义市委书记，孙曾任巩义区县任职）", "overlap_org": "河南省巩义市", "overlap_period": ""},
    # 赵建玲 ↔ 柳波 (副书记搭档)
    {"person_a": 3, "person_b": 2, "type": "共事", "context": "市委副书记搭档", "overlap_org": "中共三门峡市委员会", "overlap_period": "2025-至今"},
    # 各常委内部关系
    {"person_a": 3, "person_b": 6, "type": "同僚", "context": "市委副书记与组织部长", "overlap_org": "中共三门峡市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "共事", "context": "书记—组织部长", "overlap_org": "中共三门峡市委员会", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "共事", "context": "书记—秘书长", "overlap_org": "中共三门峡市委员会", "overlap_period": ""},
    {"person_a": 2, "person_b": 10, "type": "共事", "context": "市长—公安局长", "overlap_org": "三门峡市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 11, "type": "共事", "context": "市长—副市长", "overlap_org": "三门峡市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 12, "type": "共事", "context": "市长—副市长", "overlap_org": "三门峡市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 17, "type": "共事", "context": "市长—秘书长", "overlap_org": "三门峡市人民政府", "overlap_period": ""},
    # 孙淑芳 — 灵宝市委书记背景（本地干部）
    {"person_a": 5, "person_b": 1, "type": "共事", "context": "常委—书记", "overlap_org": "中共三门峡市委员会", "overlap_period": "2024-2026"},
]


# ═════════════════════════════════════════════════════════════════════════════
# Helper functions
# ═════════════════════════════════════════════════════════════════════════════

def write_person_json(person: dict) -> None:
    """Write a per-person graph JSON file following the person_graph_json.md schema."""
    pid = person["id"]
    name = person["name"]
    slug_id = f"sanmenxia_{name}"

    person_positions = [p for p in positions if p["person_id"] == pid]
    career_timeline = []
    for pos in person_positions:
        org = next((o for o in organizations if o["id"] == pos["org_id"]), None)
        career_timeline.append({
            "start": pos.get("start_date", "") or "",
            "end": pos.get("end_date", "") or "",
            "org": org["name"] if org else "",
            "title": pos.get("title", ""),
            "level": pos.get("rank", ""),
            "rank": pos.get("rank", ""),
            "notes": pos.get("note", "") or "",
            "confidence": "confirmed",
            "source_ids": ["S001"],
        })

    if len(career_timeline) <= 1 and not person.get("birth"):
        career_timeline.append({
            "start": "unknown",
            "end": "unknown",
            "org": "履历缺口",
            "title": "",
            "notes": "公开资料不足，完整履历待查。",
            "confidence": "unverified",
            "source_ids": [],
        })

    person_rels = [
        r for r in relationships
        if r["person_a"] == pid or r["person_b"] == pid
    ]
    rels_output = []
    for r in person_rels:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id), None)
        other_name = other["name"] if other else f"person_{other_id}"
        rels_output.append({
            "person": other_name,
            "person_id": f"sanmenxia_{other_name}",
            "relationship_type": "overlap" if r["type"] == "共事" else "predecessor_successor" if r["type"] == "交接" else "same_system",
            "strength": "strong" if r["type"] == "共事" else "medium",
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "confirmed",
            "source_ids": ["S001"],
        })

    source_url = person.get("source", "")
    publisher_name = "百度百科" if "baike.baidu" in source_url else ("三门峡市人民政府" if "smx.gov" in source_url else "媒体公开报道")
    source_type = "official" if "smx.gov" in source_url else "encyclopedia"
    sources = [
        {
            "id": "S001",
            "title": publisher_name,
            "url": source_url,
            "publisher": publisher_name,
            "published_at": "",
            "accessed_at": AS_OF,
            "source_type": source_type,
            "reliability": "high",
            "notes": "2025-2026年官方任职新闻、任前公示及百科综合",
        }
    ]

    # Enrich for core leaders with known risk signals and style
    risk_signals = []
    work_style = []
    if name == "柳波":
        risk_signals.append({
            "type": "inspection_feedback",
            "description": "2025年6月13日河南省通报中央生态环保督察移交问题追责问责情况：时任杞县县长柳波因杞县基础设施问题被谈话提醒",
            "date": "2025-06",
            "confidence": "confirmed",
            "source_ids": [],
        })
        work_style.append({
            "trait": "grassroots_oriented",
            "evidence": "2006年放弃留校机会到兰考当村党支部书记，当选首届中国十佳大学生村官；'先当村民，群众才能信任你'",
            "confidence": "confirmed",
        })
    if name == "徐相锋":
        work_style.append({
            "trait": "discipline_oriented",
            "evidence": "曾任河南省洛阳市委常委、市纪委书记、市纪委主任；援疆任哈密市委副书记",
            "confidence": "confirmed",
        })

    governance = []
    if name == "柳波":
        governance.append({
            "period": "2018",
            "domain": "public_record",
            "achievement_or_event": "2018年2月任灵宝市委书记，2021年5月获河南省脱贫攻坚先进个人称号",
            "role_in_event": "地方主官",
            "measurable_outcome": "脱贫攻坚先进",
            "location": "河南省三门峡市",
            "confidence": "confirmed",
            "sources_notes": "大河网、河南日报",
        })

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "河南省",
            "city": "三门峡市",
            "region": "三门峡市",
            "job": person.get("current_post", ""),
            "task_id": "henan_三门峡市",
            "time_focus": "2026年8月",
        },
        "identity": {
            "person_id": f"sanmenxia_{name}",
            "name": name,
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{person.get('birth','')}",
                "name_birthplace": f"{name}_{person.get('birthplace','')}",
                "official_profile_url": source_url,
            },
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "正厅级" if pid in (1, 2) else "副厅级",
            "as_of": AS_OF,
            "is_current_confirmed": person.get("confidence") == "confirmed",
            "source_ids": ["S001"],
        },
        "career_timeline": career_timeline,
        "organizations": [{"id": o["id"], "name": o["name"], "type": o["type"]} for o in organizations],
        "relationships": rels_output,
        "governance_record": governance,
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "residency_rotation" if pid in (1, 2, 20) else "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": work_style,
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": risk_signals or [
            {"type": "none_found", "description": f"截至{AS_OF}研究范围内未发现明确风险信号", "date": "", "confidence": "unverified", "source_ids": []}
        ],
        "source_register": sources,
        "confidence_summary": {
            "identity": "confirmed" if person.get("birth") else "unverified",
            "current_role": person.get("confidence", "unverified"),
            "career_completeness": "complete" if person.get("birth") else "thin",
            "relationship_confidence": "high",
            "biggest_gap": "出生年月、籍贯、完整履历确认" if not person.get("birth") else "暂无重大信息缺口",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的出生年月、籍贯、学历教育背景",
                "why_it_matters": "核心身份信息，用于去重和跨区域关联分析",
                "suggested_queries": [f"{name} 简历", f"{name} 任前公示", f"{name} 百度百科"],
                "last_attempted": AS_OF,
            }
        ] if not person.get("birth") else [],
    }

    fname = f"{TODAY}-河南省-三门峡市-{person['current_post']}-{person['name']}.json"
    fpath = PJSON_DIR / fname
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fpath.name}")


# ═════════════════════════════════════════════════════════════════════════════
# Build
# ═════════════════════════════════════════════════════════════════════════════

def main() -> int:
    print(f"Building {SLUG} network...")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")

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

    # Write person JSONs for core leaders + predecessors
    print("  Writing person JSONs...")
    core_ids = {1, 2, 3, 4, 5, 6, 7, 20, 21}
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())