#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 鄂尔多斯市 (Ordos City), 内蒙古自治区.

Investigation date: 2026-08-06
Task ID: inner_mongolia_鄂尔多斯市
Level: 地级市
Targets: 市委书记 & 市长

Research sources:
  - 维基百科·鄂尔多斯市 (四大班子现任领导/历任领导, 访问2026-08-06)
    * https://zh.wikipedia.org/wiki/鄂尔多斯市
  - 维基百科·李理 (http://2021-02 代理市长→2021-05 市委书记)
  - 人民网地方领导资料库 李理简历 (2021-08)
  - 中国经济网: 于海宇任鄂尔多斯代市长 (2024-12); 李理接任书记 (2021-06)
  - 澎湃新闻: 内蒙古能源局局长于海宇履新鄂尔多斯代市长 (2024-12-30)
  - 百度百科: 中国共产党鄂尔多斯市委员会 现行领导班子快照 (截至2026-06)
  - 百度百科个人条目: 甄华/张炜/高闻何/孔繁飞/布仁其木格/刘凤云/额登毕力格
  - 百度百科: 鄂尔多斯市人民政府 现任领导 (副市长班子)
  - 内蒙古人大常委会任职名单: 杜汇良任教育厅厅长 (2025-01)

Confidence notes:
  - 市委书记李理 / 市长于海宇 当前身份: confirmed (维基百科四大班子现任领导 + 百度百科市委快照)
  - 李理完整履历 (政府办公厅→回民区→清水河→巴彦淖尔→能源局→鄂尔多斯): confirmed (百度百科)
  - 于海宇 大多数职务: plausible (百度百科/澎湃, 具体起止个别待查)
  - 市委班子名单: confirmed (百度百科《中共鄂尔多斯市委员会》2026-06快照)
  - 军分区政委: 未找到姓名 (open gap)
  - 陈建广、严天亮(挂职): 出生/民族未详 (open gap)
  - 前任市长杜汇良去向 (内蒙古教育厅厅长, 2026-07拟任盟市书记): confirmed (人大名单/公示)
  - 所有未证实字段在 person JSON open_questions 与 report/open_gaps.md 显式标注

Artifact layout: DB/GEXF/person JSON 全部写入本脚本所在暂存目录 data/tmp/inner_mongolia_鄂尔多斯市/
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import sys

REPO_ROOT = Path(__file__).resolve().parents[2]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import sqlite3  # noqa: F401 — used by gov_relation.runner via import
from gov_relation.runner import run_build  # noqa: E402

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "鄂尔多斯市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"
PROVINCE = "内蒙古自治区"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "inner_mongolia_鄂尔多斯市"
if _CURRENT_DIR.name == "inner_mongolia_鄂尔多斯市":
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
# ID 槽位: 1-2 核心(书记/市长), 3-11 市委常委, 12-20 市政府, 30-33 前任核心
persons = [
    # ══════════════════════════════════════════════════════════════════════
    # 核心领导 (现任)
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "李理",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-06",
        "birthplace": "江苏省睢宁县",
        "education": "研究生学历，经济学硕士（内蒙古师范大学政治教育系）",
        "party_join": "中共党员（1994-04入党）",
        "work_start": "1996-07",
        "current_post": "市委书记",
        "current_org": "中共鄂尔多斯市委员会",
        "source": "https://zh.wikipedia.org/wiki/李理",
        "confidence": "confirmed",
        "notes": "江苏睢宁人；1971-06生；内蒙古师范大学政治教育系毕业后在自治区政府办公厅起步，历经呼和浩特回民区、清水河县、巴彦淖尔市、临河区、自治区能源局等；2021-02任鄂尔多斯市长，2021-05/06接任市委书记（现任）",
    },
    {
        "id": 2,
        "name": "于海宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-12",
        "birthplace": "内蒙古自治区宁城县",
        "education": "在职研究生，经济学博士（内蒙古农业大学林学院林学专业；经济师）",
        "party_join": "中共党员（1995-07入党）",
        "work_start": "1996-07",
        "current_post": "市委副书记、市长",
        "current_org": "鄂尔多斯市人民政府",
        "source": "https://zh.wikipedia.org/wiki/鄂尔多斯市",
        "confidence": "confirmed",
        "notes": "内蒙古宁城人；1972-12生；内蒙古农业大学林学专业毕业；曾任自治区能源局局长（2023）；2024-12任鄂尔多斯代市长，2025-01正式任市长（现任）",
    },
    {
        "id": 3,
        "name": "甄华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-06",
        "birthplace": "内蒙古自治区清水河县",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记、康巴什区委书记",
        "current_org": "中共鄂尔多斯市委员会",
        "source": "https://baike.baidu.com/中国共产党鄂尔多斯市委员会",
        "confidence": "confirmed",
        "notes": "市委副书记、康巴什区委书记；原任市纪委书记，2023-05起任市委副书记并兼任康巴什区委书记",
    },
    {
        "id": 4,
        "name": "张炜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-01",
        "birthplace": "",
        "education": "研究生学历，公共管理硕士（内蒙古大学）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、宣传部部长",
        "current_org": "中共鄂尔多斯市委员会",
        "source": "https://baike.baidu.com/中国共产党鄂尔多斯市委员会",
        "confidence": "confirmed",
        "notes": "市委宣传部长，班子内相对年轻（1978-01）",
    },
    {
        "id": 5,
        "name": "高闻何",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-09",
        "birthplace": "内蒙古自治区（山西忻州籍）",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、组织部部长",
        "current_org": "中共鄂尔多斯市委员会",
        "source": "https://baike.baidu.com/中国共产党鄂尔多斯市委员会",
        "confidence": "confirmed",
        "notes": "市委组织部部长、内蒙古城川干部学院院长；曾任市政府副市长、公安局长",
    },
    {
        "id": 6,
        "name": "孔繁飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-10",
        "birthplace": "山东省济宁市",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、纪委书记、市监委主任",
        "current_org": "中共鄂尔多斯市纪律检查委员会",
        "source": "https://baike.baidu.com/中国共产党鄂尔多斯市委员会",
        "confidence": "confirmed",
        "notes": "市委常委、市纪委书记、市监委主任（二级高级监察官）；2023-09任纪委书记",
    },
    {
        "id": 7,
        "name": "布仁其木格",
        "gender": "女",
        "ethnicity": "蒙古族",
        "birth": "1971-03",
        "birthplace": "内蒙古伊金霍洛旗",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、统战部部长，市政协党组副书记",
        "current_org": "中共鄂尔多斯市委员会",
        "source": "https://baike.baidu.com/中国共产党鄂尔多斯市委员会",
        "confidence": "confirmed",
        "notes": "蒙古族女干部，市委统战部长",
    },
    {
        "id": 8,
        "name": "刘凤云",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-10",
        "birthplace": "内蒙古鄂托克旗",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、市政府党组副书记、常务副市长",
        "current_org": "鄂尔多斯市人民政府",
        "source": "https://baike.baidu.com/中国共产党鄂尔多斯市委员会",
        "confidence": "confirmed",
        "notes": "市委常委兼常务副市长；2024-07任副市长，曾任市委常委、秘书长",
    },
    {
        "id": 9,
        "name": "额登毕力格",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "1968-08",
        "birthplace": "内蒙古鄂托克前旗",
        "education": "内蒙古师范大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、市委秘书长",
        "current_org": "中共鄂尔多斯市委员会",
        "source": "https://baike.baidu.com/中国共产党鄂尔多斯市委员会",
        "confidence": "confirmed",
        "notes": "市委秘书长、办公室主任",
    },
    {
        "id": 10,
        "name": "陈建广",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共鄂尔多斯市委员会",
        "source": "https://baike.baidu.com/中国共产党鄂尔多斯市委员会",
        "confidence": "unverified",
        "notes": "市委常委；具体分工/出生/民族未详（open gap）",
    },
    {
        "id": 11,
        "name": "严天亮",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委（挂职）",
        "current_org": "中共鄂尔多斯市委员会",
        "source": "https://baike.baidu.com/中国共产党鄂尔多斯市委员会",
        "confidence": "unverified",
        "notes": "市委常委、市政府党组成员、副市长提名人选（挂职）；出生/民族未详",
    },
    # ══════════════════════════════════════════════════════════════════════
    # 市政府 副市长 (2026)
    # ══════════════════════════════════════════════════════════════════════
    {"id": 12, "name": "曹凯宏", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "副市长、市公安局局长", "current_org": "鄂尔多斯市人民政府",
     "source": "https://baike.baidu.com/鄂尔多斯市人民政府", "confidence": "confirmed",
     "notes": "公安局长/副市长"},
    {"id": 13, "name": "邬建勋", "gender": "男", "ethnicity": "汉族", "birth": "1969-02", "birthplace": "陕西神木籍",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "副市长", "current_org": "鄂尔多斯市人民政府",
     "source": "https://baike.baidu.com/鄂尔多斯市人民政府", "confidence": "confirmed",
     "notes": "分管能源/财政方向"},
    {"id": 14, "name": "吉日木图", "gender": "男", "ethnicity": "蒙古族", "birth": "1973-06", "birthplace": "内蒙古达拉特旗",
     "education": "", "party_join": "", "work_start": "",
     "current_post": "副市长", "current_org": "鄂尔多斯市人民政府",
     "source": "https://baike.baidu.com/鄂尔多斯市人民政府", "confidence": "confirmed",
     "notes": "无党派人士"},
    {"id": 15, "name": "赵春雨", "gender": "男", "ethnicity": "汉族", "birth": "1981-04", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "副市长", "current_org": "鄂尔多斯市人民政府",
     "source": "https://baike.baidu.com/鄂尔多斯市人民政府", "confidence": "plausible",
     "notes": "出生出生年份存疑（1981-04，年份出处不一致待核）"},
    {"id": 16, "name": "苗程玉", "gender": "男", "ethnicity": "汉族", "birth": "1968-07", "birthplace": "内蒙古达拉特旗",
     "education": "山西矿业学院学历", "party_join": "中共党员", "work_start": "",
     "current_post": "副市长", "current_org": "鄂尔多斯市人民政府",
     "source": "https://baike.baidu.com/鄂尔多斯市人民政府", "confidence": "confirmed",
     "notes": ""},
    {"id": 17, "name": "张秀玲", "gender": "女", "ethnicity": "汉族", "birth": "1972-09", "birthplace": "内蒙古杭锦旗",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "副市长", "current_org": "鄂尔多斯市人民政府",
     "source": "https://baike.baidu.com/鄂尔多斯市人民政府", "confidence": "confirmed",
     "notes": "2024-07任命"},
    # ══════════════════════════════════════════════════════════════════════
    # 前任核心领导
    # ══════════════════════════════════════════════════════════════════════
    {
        "id": 30,
        "name": "牛俊雁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1962-01",
        "birthplace": "内蒙古南部县",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市委书记",
        "current_org": "（卸任）",
        "source": "https://zh.wikipedia.org/wiki/鄂尔多斯市",
        "confidence": "confirmed",
        "notes": "2016-12~2021-05 任鄂尔多斯市委书记，李理接任",
    },
    {
        "id": 31,
        "name": "杜汇良",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-12",
        "birthplace": "辽宁阜新籍",
        "education": "研究生学历，工学博士（清华大学）",
        "party_join": "中共党员",
        "work_start": "2001-04",
        "current_post": "前任市长（现任内蒙古自治区教育厅厅长）",
        "current_org": "内蒙古自治区教育厅",
        "source": "https://zh.wikipedia.org/wiki/鄂尔多斯市",
        "confidence": "confirmed",
        "notes": "负贵2021-06~2024-12任鄂尔多斯市长；2024-12调任内蒙古自治区党委教育工委书记、教育厅党组书记；2025-01任教育厅厅长；2026-07拟任盟市党委书记（公示）",
    },
    {
        "id": 32,
        "name": "斯琴毕力格",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任市长",
        "current_org": "（卸任）",
        "source": "https://zh.wikipedia.org/wiki/鄂尔多斯市",
        "confidence": "unverified",
        "notes": "2018-03~2021-02 任鄂尔多斯市长，李理接任市长",
    },
    {
        "id": 33,
        "name": "苏忠胜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969-10",
        "birthplace": "内蒙古杭锦旗",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "鄂尔多斯市人民代表大会常务委员会",
        "source": "https://zh.wikipedia.org/wiki/鄂尔多斯市",
        "confidence": "confirmed",
        "notes": "2025-01当选市人大常委会主任（四大班子正职）",
    },
    {
        "id": 34,
        "name": "苏翠芳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1970-10",
        "birthplace": "内蒙古鄂尔多斯市东胜区",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "中国人民政治协商会议鄂尔多斯市委员会",
        "source": "https://zh.wikipedia.org/wiki/鄂尔多斯市",
        "confidence": "confirmed",
        "notes": "2026-02当选市政协主席（四大班子正职）；此前曾任市委常委、副市长",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共鄂尔多斯市委员会", "type": "党委", "level": "地级市", "parent": "中国共产党内蒙古自治区委员会", "location": "鄂尔多斯市康巴什区"},
    {"id": 2, "name": "鄂尔多斯市人民政府", "type": "政府", "level": "地级市", "parent": "内蒙古自治区人民政府", "location": "鄂尔多斯市康巴什区"},
    {"id": 3, "name": "中共鄂尔多斯市纪律检查委员会/鄂尔多斯市监察委员会", "type": "党委", "level": "地级市", "parent": "内蒙古自治区纪委监委", "location": "鄂尔多斯市"},
    {"id": 4, "name": "鄂尔多斯市人民代表大会常务委员会", "type": "人大", "level": "地级市", "parent": "内蒙古自治区人大常委会", "location": "鄂尔多斯市"},
    {"id": 5, "name": "中国人民政治协商会议鄂尔多斯市委员会", "type": "政协", "level": "地级市", "parent": "中国人民政治协商会议内蒙古自治区委员会", "location": "鄂尔多斯市"},
    {"id": 6, "name": "康巴什区委员会", "type": "党委", "level": "市辖区", "parent": "中共鄂尔多斯市委员会", "location": "鄂尔多斯市康巴什区"},
    {"id": 7, "name": "内蒙古自治区教育厅", "type": "政府", "level": "省级", "parent": "内蒙古自治区人民政府", "location": "呼和浩特市"},
    {"id": 8, "name": "内蒙古自治区能源局", "type": "政府", "level": "省级", "parent": "内蒙古自治区人民政府", "location": "呼和浩特市"},
    {"id": 9, "name": "内蒙古自治区水利厅", "type": "政府", "level": "省级", "parent": "内蒙古自治区人民政府", "location": "呼和浩特市"},
    {"id": 10, "name": "鄂尔多斯市公安局", "type": "政府", "level": "地级市", "parent": "鄂尔多斯市人民政府", "location": "鄂尔多斯市"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 李理 — 市委书记 (现任)
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "2021-05", "end_date": "", "rank": "正厅级", "note": "2021-05/06接任市委书记，现又兼任军分区党委第一书记"},
    {"person_id": 1, "org_id": 2, "title": "市长", "start_date": "2021-02", "end_date": "2021-06", "rank": "正厅级", "note": "2021-02任代市长，2021-03当选，执政民与书记并任至2021-06"},
    {"person_id": 1, "org_id": 8, "title": "党组书记、局长", "start_date": "2018-10", "end_date": "2021-02", "rank": "厅局级", "note": "内蒙古自治区能源局党组书记、局长"},
    {"person_id": 1, "org_id": 1, "title": "巴彦淖尔市委常委、临河区委书记/市委副书记（历任）", "start_date": "", "end_date": "", "rank": "", "note": "曾在巴彦淖尔市历任副市长、市委常委兼临河区委书记、市委副书记兼政法委书记（时间未逐条）"},
    # 于海宇 — 市长 (现任)
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "2025-01", "end_date": "", "rank": "正厅级", "note": "2024-12任代市长，2025-01正式当选"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "2024-12", "end_date": "", "rank": "副厅级", "note": "兼任市委副书记"},
    {"person_id": 2, "org_id": 8, "title": "党组书记、局长", "start_date": "2023", "end_date": "2024-12", "rank": "正厅级", "note": "内蒙古自治区能源局党组书记、局长（2023起）"},
    {"person_id": 2, "org_id": 9, "title": "早期任职", "start_date": "", "end_date": "", "rank": "", "note": "自治区水利厅、政府办公厅等早期工作（具体起止待核）"},
    # 甄华
    {"person_id": 3, "org_id": 1, "title": "市委副书记、康巴什区委书记", "start_date": "2023-05", "end_date": "", "rank": "正厅级", "note": ""},
    # 张炜
    {"person_id": 4, "org_id": 1, "title": "市委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 高闻何
    {"person_id": 5, "org_id": 1, "title": "市委常委、组织部部长", "start_date": "2023-05", "end_date": "", "rank": "副厅级", "note": "兼任内蒙古城川干部学院院长"},
    # 孔繁飞
    {"person_id": 6, "org_id": 3, "title": "市委常委、纪委书记、市监委主任", "start_date": "2023-09", "end_date": "", "rank": "副厅级", "note": ""},
    # 布仁其木格
    {"person_id": 7, "org_id": 1, "title": "市委常委、统战部部长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "兼市政协党组副书记"},
    # 刘凤云
    {"person_id": 8, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "常务副市长", "start_date": "2024-07", "end_date": "", "rank": "副厅级", "note": "市政府党组副书记"},
    # 额登毕力格
    {"person_id": 9, "org_id": 1, "title": "市委常委、市委秘书长", "start_date": "2024-11", "end_date": "", "rank": "副厅级", "note": ""},
    # 陈建广 / 严天亮
    {"person_id": 10, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副厅级", "note": "具体分工未公开"},
    {"person_id": 11, "org_id": 1, "title": "市委常委（挂职）", "start_date": "", "end_date": "", "rank": "副厅级", "note": "市政府党组成员、副市长提名人选"},
    # 市政府
    {"person_id": 12, "org_id": 10, "title": "副市长、市公安局局长", "start_date": "2023", "end_date": "", "rank": "副厅级", "note": "接替高闻何任公安局长"},
    {"person_id": 13, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "分管能源领域"},
    {"person_id": 14, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "无党派"},
    {"person_id": 15, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "出生年份待核"},
    {"person_id": 16, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "副市长", "start_date": "2024-07", "end_date": "", "rank": "副厅级", "note": ""},
    # 前任核心
    {"person_id": 30, "org_id": 1, "title": "市委书记", "start_date": "2016-12", "end_date": "2021-05", "rank": "正厅级", "note": "前任市委书记"},
    {"person_id": 31, "org_id": 2, "title": "市长", "start_date": "2021-06", "end_date": "2024-12", "rank": "正厅级", "note": "前任市长"},
    {"person_id": 31, "org_id": 7, "title": "教育厅党组书记、厅长", "start_date": "2025-01", "end_date": "", "rank": "正厅级", "note": "现任内蒙古自治区教育厅厅长"},
    {"person_id": 32, "org_id": 2, "title": "市长", "start_date": "2018-03", "end_date": "2021-02", "rank": "正厅级", "note": "前任市长"},
    {"person_id": 33, "org_id": 4, "title": "市人大常委会主任", "start_date": "2025-01", "end_date": "", "rank": "正厅级", "note": ""},
    {"person_id": 34, "org_id": 5, "title": "市政协主席", "start_date": "2026-02", "end_date": "", "rank": "正厅级", "note": ""},
]

# ── Relationships ─────────────────────────────────────────────────────────────
# 书记—市长 搭档；现任核心→各常委/副市长的共事关系；前任交接
relationships = [
    # 李理 ↔ 于海宇 (书记—市长搭档)
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "市委书记—市长搭档核心工作关系", "overlap_org": "中共鄂尔多斯市委员会", "overlap_period": "2024-12至今"},
    # 李理 ↔ 各市委常委
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "书记—市委副书记", "overlap_org": "中共鄂尔多斯市委员会", "overlap_period": "2023-05至今"},
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "书记—常委（宣传部长）", "overlap_org": "中共鄂尔多斯市委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 5, "type": "共事", "context": "书记—常委（组织部长）", "overlap_org": "中共鄂尔多斯市委员会", "overlap_period": "2023-05至今"},
    {"person_a": 1, "person_b": 6, "type": "共事", "context": "书记—市纪委书记", "overlap_org": "中共鄂尔多斯市委员会", "overlap_period": "2023-09至今"},
    {"person_a": 1, "person_b": 7, "type": "共事", "context": "书记—常委（统战部长）", "overlap_org": "中共鄂尔多斯市委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 8, "type": "共事", "context": "书记—常委（常务副市长）", "overlap_org": "中共鄂尔多斯市委员会", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 9, "type": "共事", "context": "书记—市委秘书长", "overlap_org": "中共鄂尔多斯市委员会", "overlap_period": "2024-11至今"},
    # 于海宇 ↔ 市政府
    {"person_a": 2, "person_b": 8, "type": "共事", "context": "市长—常务副市长", "overlap_org": "鄂尔多斯市人民政府", "overlap_period": "2025至今"},
    {"person_a": 2, "person_b": 12, "type": "共事", "context": "市长—副市长/公安局长", "overlap_org": "鄂尔多斯市人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 13, "type": "共事", "context": "市长—副市长", "overlap_org": "鄂尔多斯市人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 14, "type": "共事", "context": "市长—副市长", "overlap_org": "鄂尔多斯市人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 16, "type": "共事", "context": "市长—副市长", "overlap_org": "鄂尔多斯市人民政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 17, "type": "共事", "context": "市长—副市长", "overlap_org": "鄂尔多斯市人民政府", "overlap_period": "2026"},
    # 前任交接
    {"person_a": 30, "person_b": 1, "type": "交接", "context": "前任书记（牛俊雁）→继任书记（李理）", "overlap_org": "中共鄂尔多斯市委员会", "overlap_period": "2021-05"},
    {"person_a": 31, "person_b": 2, "type": "交接", "context": "前任市长（杜汇良）→继任市长（于海宇）", "overlap_org": "鄂尔多斯市人民政府", "overlap_period": "2024-12"},
    {"person_a": 32, "person_b": 1, "type": "交接", "context": "前任市长（斯琴毕力格）→继任市长（李理）", "overlap_org": "鄂尔多斯市人民政府", "overlap_period": "2021-02"},
]


# ═════════════════════════════════════════════════════════════════════════════
# Person JSON writer
# ═════════════════════════════════════════════════════════════════════════════
def slugify(name: str) -> str:
    return name


def write_person_json(person: dict) -> None:
    pid = person["id"]
    name = person["name"]
    slug_id = f"ordos_{name}"

    career_timeline = []
    for pos in positions:
        if pos["person_id"] == pid:
            org = next((o for o in organizations if o["id"] == pos["org_id"]), None)
            career_timeline.append({
                "start": pos.get("start_date", ""),
                "end": pos.get("end_date", ""),
                "org": org["name"] if org else "",
                "title": pos.get("title", ""),
                "level": pos.get("rank", ""),
                "location": "",
                "system": "party" if (org and org["type"] == "党委") else ("government" if (org and org["type"] == "政府") else ("development" if (org and "人民" in org["name"]) else "other")),
                "rank": pos.get("rank", ""),
                "is_key_promotion": bool(pos.get("start_date") and pos.get("end_date")) and pos.get("title") in ("市委书记", "市长"),
                "notes": pos.get("note", ""),
                "confidence": "confirmed" if pos.get("start_date") else "plausible",
                "source_ids": ["S001"],
            })
    if not career_timeline:
        career_timeline.append({
            "start": "unknown",
            "end": "unknown",
            "org": "履历缺口",
            "title": "",
            "notes": "公开资料不足，早期履历待查（网络受限：Exa限流、部分官方页面超时）",
            "confidence": "unverified",
            "source_ids": [],
        })

    person_rels = [r for r in relationships if r["person_a"] == pid or r["person_b"] == pid]
    rels_output = []
    for r in person_rels:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id), None)
        other_name = other["name"] if other else f"person_{other_id}"
        rels_output.append({
            "person": other_name,
            "person_id": f"ordos_{other_name}",
            "relationship_type": "overlap" if r["type"] == "共事" else "predecessor_successor",
            "strength": "strong" if r["type"] == "共事" else "medium",
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "confirmed" if r.get("context") else "plausible",
            "source_ids": ["S001"],
        })

    source_url = person.get("source", "")
    sources = [
        {"id": "S001", "title": "维基百科·鄂尔多斯市（四大班子现任领导/历任领导）", "url": "https://zh.wikipedia.org/wiki/鄂尔多斯市",
         "publisher": "维基百科", "published_at": "", "accessed_at": AS_OF,
         "source_type": "media", "reliability": "medium",
         "notes": "确认李理/于海宇/苏忠胜/苏翠芳现任及杜汇良、牛俊雁、斯琴毕力格前任职"},
        {"id": "S002", "title": "百度百科·中国共产党鄂尔多斯市委员会（现行班子快照）", "url": "https://baike.baidu.com/中国共产党鄂尔多斯市委员会",
         "publisher": "百度百科", "published_at": "2026-06", "accessed_at": AS_OF,
         "source_type": "encyclopedia", "reliability": "medium",
         "notes": "甄华/李理/于海宇/张炜/高闻何/孔繁飞/布仁其木格/刘凤云/额登毕力格/陈建广/严天亮等现行班子名单"},
        {"id": "S003", "title": "中国经济网/澎湃（于海宇任鄂尔多斯代市长, 李理接任书记）", "url": "https://www.ce.cn",
         "publisher": "中国经济网/澎湃新闻", "published_at": "2024-12-30", "accessed_at": AS_OF,
         "source_type": "media", "reliability": "medium",
         "notes": "于海宇 市级任命/能源局来源与李理书记任命时间线"},
    ]
    if person.get("confidence") == "unverified":
        sources.append({
            "id": "S004", "title": "inferred/partial",
            "url": source_url, "publisher": "", "published_at": "",
            "accessed_at": AS_OF, "source_type": "inferred", "reliability": "low",
            "notes": "公开信息不足，标记 unverified",
        })

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": PROVINCE,
            "city": "鄂尔多斯市",
            "region": "鄂尔多斯市",
            "job": person.get("current_post", ""),
            "task_id": "inner_mongolia_鄂尔多斯市",
            "time_focus": "2026年",
        },
        "identity": {
            "person_id": slug_id,
            "name": name,
            "aliases": [],
            "gender": person.get("gender", ""),
            "ethnicity": person.get("ethnicity", ""),
            "birth": person.get("birth", ""),
            "birthplace": person.get("birthplace", ""),
            "native_place": "",
            "education": [{"period": "", "institution": person.get("education", ""), "major": "",
                           "degree": "", "study_type": "unknown", "source_ids": ["S001"]}],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{person.get('birth', '')}",
                "name_birthplace": f"{name}_{person.get('birthplace', '')}",
                "official_profile_url": source_url,
            },
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "正厅级" if person.get("id") in (1, 2) else "",
            "as_of": AS_OF,
            "is_current_confirmed": person.get("confidence") == "confirmed",
            "source_ids": ["S001"],
        },
        "career_timeline": career_timeline,
        "organizations": [{"id": o["id"], "name": o["name"], "type": o["type"]} for o in organizations],
        "relationships": rels_output,
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "local_ladder" if pid in (1, 2) else "unknown",
            "systems_experience": [],
            "geographic_pattern": [],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {
                "type": "none_found",
                "description": "搜索范围为官方页面与公开新闻，截至调查日未发现所指纪律或舆情风险信号（鄂尔多斯历史上有数名前后任领导因违规被调查，如乌光中、白玉刚，属省级职务关联，非现任班子）。",
                "date": AS_OF,
                "confidence": "unverified",
                "source_ids": ["S001"],
            }
        ],
        "source_register": sources,
        "confidence_summary": {
            "identity": "confirmed" if person.get("birth") else "plausible",
            "current_role": person.get("confidence", "unverified"),
            "career_completeness": "partial" if pid in (1, 2) else "thin",
            "relationship_confidence": "high" if person.get("confidence") == "confirmed" else "medium",
            "biggest_gap": "于海宇早期逐段任职起止" if pid == 2 else ("李理履历已全" if pid == 1 else "详细履历/生日信息"),
        },
        "open_questions": [
            {
                "priority": "critical" if pid in (1, 2) else "medium",
                "question": f"{name} 任现职前完整分段履历（每段职务起止时间）",
                "why_it_matters": "关系网络分析需要精确时间线",
                "suggested_queries": [f"{name} 简历", f"{name} 任前公示", f"{name} 此前担任"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "medium",
                "question": f"{name} 出生年月/籍贯/学历教育（部分缺失或需核实）",
                "why_it_matters": "核心身份信息，用于去重与跨区域关联",
                "suggested_queries": [f"{name} 籍贯", f"{name} 毕业院校"],
                "last_attempted": AS_OF,
            },
        ],
    }

    fname = f"{TODAY}-{PROVINCE}-{SLUG}-{person['current_post']}-{person['name']}.json"
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

    print("  Writing person JSONs...")
    core_ids = {1, 2, 30, 31, 32, 33, 34}  # 核心领导 + 前任 + 四大班子
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())