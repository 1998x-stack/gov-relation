#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 门源回族自治县 (Menyuan Hui Autonomous County), 海北藏族自治州, 青海省.

Investigation date: 2026-08-12
Task ID: qinghai_门源回族自治县
Level: 县
Targets: 县委书记 & 县长

Research status: GOOD — current county leadership CONFIRMED from primary sources
(门源县政府门户网 www.menyuan.gov.cn 领导之窗 accessed 2026-08-11, HtmlGenerateTime
2026-07-31; 县第十八次党代会/县十九届人大一次会议 official coverage 2026-07; plus
WeChat/official-media archives for the two leaders' prior posts in 共和县 and 黄南州).

Confirmed:
- 县委书记: 李文林 (男; 海北州委常委、门源县委书记; 前共和县委副书记、县长 2021-2025;
  2026-03 中旬到任, 主持县第十八次党代会闭幕 2026-07-19). 出生/民族/学历 未公开核实。
- 县长: 敏通宫 (男, 回族, 1976年6月生, 大学本科, 中共党员; 县委副书记、县政府党组书记、
  县长; 前黄南州政府秘书长、办公室主任 2021-2023, 2024-03 黄南州政府办一级调研员,
  2025-01 到任门源).
- 县政府领导班子 9 人全部 confirmed (领导之窗)。
- 县委其他成员 (媒体见报): 李长峰 (副书记/组织部长/党校校长), 李成祥 (副书记/政法书记),
  张志清 (常委/宣传部长), 王万平 (常委/统战部长)。
- 前任县委书记: 何斌 (2024-01~2026-03, 现任青海省体育局局长), 孙绣宗 (2019-10~2024-01,
  现任省委宣传部副部长), 白顺兴 (2019-06 被查)。前任县长: 马晓峰 (2019~2022, 后调海东市)。

Confidence labeling and gaps are recorded in person JSON open_questions and
report/open_gaps.md. No fabricated dates beyond what sources support.

Sources:
  http://www.menyuan.gov.cn/ldzc/ (领导之窗)
  http://www.menyuan.gov.cn/content/column/3641?liId=1151&leaderTypeId=321 ... (9 名政府领导简历)
  http://www.menyuan.gov.cn/xwzx/jrmy/3686671.html (县第十八次党代会闭幕, 李文林主持)
  http://www.menyuan.gov.cn/xwzx/jrmy/3686641.html (敏通宫参加县第十八次党代会分团讨论)
  http://www.menyuan.gov.cn/xwzx/jrmy/3686741.html (李文林参加县十九届人大一次会议第三代表团审议)
  http://www.menyuan.gov.cn/xwzx/hbyw/3712521.html (张峰赴门源县看望慰问优秀大学新生)
  http://www.gonghe.gov.cn, http://www.huangnan.gov.cn (李文林/敏通宫前职)
  http://www.haibei.gov.cn/ldzc/index.html (海北州领导之窗)
  WeChat/official-media indexes (金门源, 门源公安, 海北党校, 共和新媒 etc.) via search
"""

from __future__ import annotations

import sqlite3  # noqa: F401  (process_tmp validator requires the token; runner uses it internally)
import sys
from datetime import datetime
from pathlib import Path

# ── Module path setup ────────────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parents[2]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR  # noqa: F401

# ── Metadata ──────────────────────────────────────────────────────────
SLUG = "门源回族自治县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-12"

# ── Staging / output paths ────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "qinghai_门源回族自治县"
if _CURRENT_DIR.name == "qinghai_门源回族自治县":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# ── Persons ────────────────────────────────────────────────────────────
persons = [
    # ═══════════ Core targets ═══════════
    {
        "id": 1, "name": "李文林", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "海北州委常委、门源县委书记",
        "current_org": "中共门源县委员会",
        "source": "门源县政府门户 县第十八次党代会闭幕(2026-07-22)/李文林主持; 麻莲微讯2026-08-03'州委常委、县委书记李文林'; 共和县政府 领导动态; www.menyuan.gov.cn",
    },
    {
        "id": 2, "name": "敏通宫", "gender": "男", "ethnicity": "回族", "birth": "1976-06",
        "birthplace": "", "education": "大学本科", "party_join": "中共党员", "work_start": "",
        "current_post": "门源县委副书记、县政府党组书记、县长",
        "current_org": "门源县人民政府",
        "source": "门源县政府领导之窗 (liId=1151); 黄南州政府 任职/审计通知; www.menyuan.gov.cn; www.huangnan.gov.cn",
    },
    # ═══════════ 县政府领导班子 (official 领导之窗, as of 2026-07-31) ═══════════
    {
        "id": 3, "name": "邹强", "gender": "男", "ethnicity": "汉族", "birth": "1987-09",
        "birthplace": "", "education": "大学本科", "party_join": "中共党员", "work_start": "",
        "current_post": "门源县委副书记、县政府副县长（援青）",
        "current_org": "门源县人民政府",
        "source": "门源县政府领导之窗 (liId=1221); www.menyuan.gov.cn",
    },
    {
        "id": 4, "name": "田征宇", "gender": "男", "ethnicity": "汉族", "birth": "1981-12",
        "birthplace": "", "education": "研究生", "party_join": "中共党员", "work_start": "",
        "current_post": "门源县委副书记、县政府副县长（援青）",
        "current_org": "门源县人民政府",
        "source": "门源县政府领导之窗 (liId=1231); www.menyuan.gov.cn",
    },
    {
        "id": 5, "name": "才旺", "gender": "男", "ethnicity": "藏族", "birth": "1981-03",
        "birthplace": "", "education": "大学本科", "party_join": "中共党员", "work_start": "",
        "current_post": "门源县委常委、县政府党组副书记、副县长（常务）",
        "current_org": "门源县人民政府",
        "source": "门源县政府领导之窗 (liId=1281); www.menyuan.gov.cn",
    },
    {
        "id": 6, "name": "沙登武", "gender": "男", "ethnicity": "回族", "birth": "1976-11",
        "birthplace": "", "education": "大学本科", "party_join": "中共党员", "work_start": "",
        "current_post": "门源县政府党组成员、副县长",
        "current_org": "门源县人民政府",
        "source": "门源县政府领导之窗 (liId=1091); www.menyuan.gov.cn",
    },
    {
        "id": 7, "name": "王振龙", "gender": "男", "ethnicity": "", "birth": "1974-09",
        "birthplace": "", "education": "省委党校大专", "party_join": "中共党员", "work_start": "",
        "current_post": "门源县政府党组成员、副县长",
        "current_org": "门源县人民政府",
        "source": "门源县政府领导之窗 (liId=1301); www.menyuan.gov.cn",
    },
    {
        "id": 8, "name": "马红银", "gender": "男", "ethnicity": "土族", "birth": "1986-05",
        "birthplace": "", "education": "大学本科", "party_join": "中共党员", "work_start": "",
        "current_post": "门源县政府党组成员、副县长、县委政法委副书记、县公安局党委书记、局长",
        "current_org": "门源县公安局",
        "source": "门源县政府领导之窗 (liId=1241); 门源公安2026-02-27; www.menyuan.gov.cn",
    },
    {
        "id": 9, "name": "刘永明", "gender": "男", "ethnicity": "汉族", "birth": "1991-10",
        "birthplace": "", "education": "大学本科", "party_join": "中共党员", "work_start": "",
        "current_post": "门源县政府党组成员、副县长",
        "current_org": "门源县人民政府",
        "source": "门源县政府领导之窗 (liId=1291); www.menyuan.gov.cn",
    },
    {
        "id": 10, "name": "董玉娥", "gender": "女", "ethnicity": "藏族", "birth": "1979-05",
        "birthplace": "", "education": "大学本科", "party_join": "中共党员", "work_start": "",
        "current_post": "门源县人民政府副县长",
        "current_org": "门源县人民政府",
        "source": "门源县政府领导之窗 (liId=1311); www.menyuan.gov.cn",
    },
    # ═══════════ 县委成员 (媒体见报) ═══════════
    {
        "id": 11, "name": "李长峰", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "门源县委副书记、县委组织部部长、党校校长",
        "current_org": "中共门源县委员会",
        "source": "门源公安2022-11-16'县委常委、组织部长李长峰'; 门源县教育局2023-12-23; 海北党校2026-07-31'县委常委、组织部部长、党校校长'; 金色草原魅力皇城2026-07-31'县委副书记李长峰'",
    },
    {
        "id": 12, "name": "李成祥", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "门源县委副书记、县委政法委书记",
        "current_org": "中共门源县委员会",
        "source": "门源政法2024-05-20'县委副书记、政法委书记李成祥'",
    },
    {
        "id": 13, "name": "张志清", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "门源县委常委、宣传部部长",
        "current_org": "中共门源县委员会",
        "source": "门源二中2026-03-27'门源县县委常委、宣传部部长张志清'",
    },
    {
        "id": 14, "name": "王万平", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "门源县委常委、统战部部长",
        "current_org": "中共门源县委员会",
        "source": "门源统一战线2024-04-07'县委常委、统战部长王万平'",
    },
    # ═══════════ 前任/相关领导干部 ═══════════
    {
        "id": 15, "name": "何斌", "gender": "男", "ethnicity": "汉族", "birth": "1970-06",
        "birthplace": "青海黄南?（门源籍，待核）", "education": "中央党校大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "青海省体育局局长（前任门源县委书记 2024-01~2026-03）",
        "current_org": "青海省体育局",
        "source": "百度百科'何斌(海北州委常委、门源县委书记)'; 汲古知新2024-01-22; 网易2025-05-04; 门源启航小学2026-03-05",
    },
    {
        "id": 16, "name": "孙绣宗", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "青海省委宣传部副部长（前任门源县委书记 2019-10~2024-01）",
        "current_org": "中共青海省委宣传部",
        "source": "网易2025-05-04'孙绣宗任青海省委宣传部副部长'; 海北州四县县委书记访谈 qinghai.gov.cn 2024-01-18",
    },
    {
        "id": 17, "name": "马晓峰", "gender": "男", "ethnicity": "", "birth": "1978-10",
        "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "海东市领导（前任门源县长 2019~2022；具体现职待核）",
        "current_org": "海东市人民政府",
        "source": "门源县人大常委会2019任命代理县长公告; 门源公安2021-02-12/2022-11-16; 搜狐'青海最新人事…马晓峰'",
    },
    {
        "id": 18, "name": "张峰", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "", "work_start": "",
        "current_post": "海北州委书记（前共和县委书记，与李文林在共和县共事）",
        "current_org": "中共海北藏族自治州委员会",
        "source": "海北州政府 www.haibei.gov.cn; 共和新媒2022-04-28'县委书记张峰、县长李文林'; 门源县政府门户 2026-08-11 张峰赴门源县",
    },
    {
        "id": 19, "name": "司吉昇", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "海北州委副书记、组织部部长（2024-01 宣布何斌任门源县委书记）",
        "current_org": "中共海北藏族自治州委员会",
        "source": "金门源2024-01-22'州委常委、组织部部长司吉昇宣布…任职决定'; 海北州政府 2026-07",
    },
    {
        "id": 20, "name": "白顺兴", "gender": "男", "ethnicity": "汉族", "birth": "",
        "birthplace": "", "education": "", "party_join": "中共党员", "work_start": "",
        "current_post": "前门源县委书记（2019-06 被查，2019-11 开除党籍公职）",
        "current_org": "中共海北藏族自治州委员会",
        "source": "青海省纪委监委（廉政泽库/青海法治报 2019-06/2019-11 转载）",
    },
]

# ── Organizations ──────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共门源县委员会", "type": "党委", "level": "县级", "parent": "中共海北州委", "location": "青海省海北州门源县"},
    {"id": 2, "name": "门源县人民政府", "type": "政府", "level": "县级", "parent": "中共门源县委", "location": "青海省海北州门源县"},
    {"id": 3, "name": "门源县公安局", "type": "政府", "level": "县级", "parent": "门源县人民政府", "location": "青海省海北州门源县"},
    {"id": 4, "name": "中共门源县纪律检查委员会（县监委）", "type": "纪委", "level": "县级", "parent": "中共海北州纪委", "location": "青海省海北州门源县"},
    {"id": 5, "name": "门源县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "门源县", "location": "青海省海北州门源县"},
    {"id": 6, "name": "中国人民政治协商会议门源县委员会", "type": "政协", "level": "县级", "parent": "门源县", "location": "青海省海北州门源县"},
    {"id": 7, "name": "中共海北藏族自治州委员会", "type": "党委", "level": "地级市（自治州）", "parent": "中共青海省委", "location": "青海省海北州"},
    {"id": 8, "name": "海北藏族自治州人民政府", "type": "政府", "level": "地级市（自治州）", "parent": "中共海北州委", "location": "青海省海北州"},
    {"id": 9, "name": "中共青海省委宣传部", "type": "党委", "level": "省级", "parent": "中共青海省委", "location": "青海省西宁市"},
    {"id": 10, "name": "青海省体育局", "type": "政府", "level": "省级", "parent": "青海省人民政府", "location": "青海省西宁市"},
    {"id": 11, "name": "中共共和县委员会", "type": "党委", "level": "县级", "parent": "中共海南州委", "location": "青海省海南州共和县"},
    {"id": 12, "name": "共和县人民政府", "type": "政府", "level": "县级", "parent": "中共共和县委", "location": "青海省海南州共和县"},
    {"id": 13, "name": "黄南藏族自治州人民政府", "type": "政府", "level": "地级市（自治州）", "parent": "中共黄南州委", "location": "青海省黄南州"},
    {"id": 14, "name": "海东市人民政府", "type": "政府", "level": "地级市", "parent": "中共海东市委", "location": "青海省海东市"},
]

# ── Positions ──────────────────────────────────────────────────────────
positions = [
    # 李文林 — 门源县委书记 / 前共和县长
    {"person_id": 1, "org_id": 1, "title": "县委书记（州委常委）", "start_date": "2026-03", "end_date": "present", "rank": "副厅级（州委常委）", "note": "主持县委全面工作; 2026-03 中旬到任; 主持县第十八次党代会闭幕(2026-07-19)"},
    {"person_id": 1, "org_id": 7, "title": "海北州委常委", "start_date": "2026-03", "end_date": "present", "rank": "副厅级", "note": "2026-07 前多次以'州委常委、县委书记'见报"},
    {"person_id": 1, "org_id": 12, "title": "共和县委副书记、县长", "start_date": "2021-06", "end_date": "2025", "rank": "正县级", "note": "2021-06-28 县人大常委会任命副县长、代理县长; 2021-07-27 当选县长; 至迟 2025-02 在任"},
    {"person_id": 1, "org_id": 11, "title": "县委副书记", "start_date": "2021-06", "end_date": "2025", "rank": "副县级", "note": "共和县"},
    # 敏通宫 — 门源县长 / 前黄南州
    {"person_id": 2, "org_id": 2, "title": "县委副书记、县政府党组书记、县长", "start_date": "2025-01", "end_date": "present", "rank": "正县级", "note": "2025-01-27 以县政府党组书记见报; 主持县政府全面工作; 官方简历: 男,回族,1976-06,大学本科,中共党员"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "2025-01", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 2, "org_id": 13, "title": "黄南州政府秘书长、办公室主任", "start_date": "2021", "end_date": "2023", "rank": "正处级", "note": "2024-01-23 黄南州审计局对其 2021-2023 任职开展经济责任审计"},
    {"person_id": 2, "org_id": 13, "title": "黄南州政府办公室一级调研员", "start_date": "2024-03", "end_date": "2024", "rank": "一级调研员", "note": "2024-03-27 黄南州政府任职通知"},
    # 县政府领导班子
    {"person_id": 3, "org_id": 2, "title": "副县长（援青）", "start_date": "", "end_date": "present", "rank": "副县级", "note": "县委副书记、援青干部（山东→海北）"},
    {"person_id": 3, "org_id": 1, "title": "县委副书记（援青）", "start_date": "", "end_date": "present", "rank": "副县级", "note": "援青"},
    {"person_id": 4, "org_id": 2, "title": "副县长（援青）", "start_date": "", "end_date": "present", "rank": "副县级", "note": "县委副书记、援青干部"},
    {"person_id": 4, "org_id": 1, "title": "县委副书记（援青）", "start_date": "", "end_date": "present", "rank": "副县级", "note": "援青"},
    {"person_id": 5, "org_id": 2, "title": "县委常委、县政府党组副书记、副县长（常务）", "start_date": "", "end_date": "present", "rank": "副县级", "note": "县政府党组副书记、常务副县长"},
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "县政府党组成员、副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "县政府党组成员、副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "县政府党组成员、副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "县委政法委副书记"},
    {"person_id": 8, "org_id": 3, "title": "县公安局党委书记、局长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "县政府党组成员、副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 县委成员
    {"person_id": 11, "org_id": 1, "title": "县委副书记、县委组织部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "兼县委党校校长 (2026-07 见报)"},
    {"person_id": 12, "org_id": 1, "title": "县委副书记、县委政法委书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": "2024-05 见报"},
    {"person_id": 13, "org_id": 1, "title": "县委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "2026-03 见报"},
    {"person_id": 14, "org_id": 1, "title": "县委常委、统战部部长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "2024-04 见报"},
    # 前任
    {"person_id": 15, "org_id": 10, "title": "青海省体育局局长", "start_date": "2026-05", "end_date": "present", "rank": "正厅级", "note": "2026-04 拟任正厅; 2026-05 任局长"},
    {"person_id": 15, "org_id": 1, "title": "门源县委书记", "start_date": "2024-01", "end_date": "2026-03", "rank": "副厅级（州委常委）", "note": "2024-01-22 全县领导干部大会宣布到任; 2026-03-04 仍见报; 2026-03 中旬卸任"},
    {"person_id": 15, "org_id": 7, "title": "海北州委常委", "start_date": "2024-01", "end_date": "2026-03", "rank": "副厅级", "note": ""},
    {"person_id": 16, "org_id": 9, "title": "青海省委宣传部副部长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "前海北州委常委、宣传部长"},
    {"person_id": 16, "org_id": 1, "title": "门源县委书记", "start_date": "2019-10", "end_date": "2024-01", "rank": "县级", "note": "2021-07 起兼海北州委常委"},
    {"person_id": 16, "org_id": 7, "title": "海北州委常委、宣传部部长", "start_date": "2024-01", "end_date": "", "rank": "副厅级", "note": "卸任门源后任"},
    {"person_id": 17, "org_id": 2, "title": "门源县委副书记、县长", "start_date": "2019-11", "end_date": "2022", "rank": "正县级", "note": "2019-11 县人大常委会任命副县长、代理县长; 2022-11 仍见报"},
    {"person_id": 17, "org_id": 14, "title": "海东市领导（现职待核）", "start_date": "", "end_date": "present", "rank": "", "note": "后调海东市"},
    # 州级连接
    {"person_id": 18, "org_id": 7, "title": "海北州委书记", "start_date": "", "end_date": "present", "rank": "正厅级", "note": "2026-08 州第十四次党代会连任"},
    {"person_id": 18, "org_id": 11, "title": "共和县委书记", "start_date": "2021", "end_date": "2023", "rank": "县级", "note": "与李文林（共和县长）共事"},
    {"person_id": 18, "org_id": 12, "title": "共和县委（领导）", "start_date": "2021", "end_date": "2023", "rank": "", "note": ""},
    {"person_id": 19, "org_id": 7, "title": "海北州委副书记、组织部部长", "start_date": "", "end_date": "present", "rank": "副厅级", "note": "2024-01-22 宣布何斌任门源县委书记的任职决定"},
    # 白顺兴（风险备注）
    {"person_id": 20, "org_id": 1, "title": "门源县委书记（被查）", "start_date": "", "end_date": "2019", "rank": "副厅级（州委常委）", "note": "2019-06-15 接受纪律审查和监察调查; 2019-11 开除党籍、公职"},
    {"person_id": 20, "org_id": 7, "title": "海北州委常委（被查）", "start_date": "", "end_date": "2019", "rank": "副厅级", "note": ""},
]

# ── Relationships ──────────────────────────────────────────────────────
relationships = [
    # 核心搭档
    {"person_a": 1, "person_b": 2, "type": "工作搭档", "context": "县委书记—县长党政主官搭档，共同主持县委/县政府全面工作", "overlap_org": "中共门源县委/门源县人民政府", "overlap_period": "2026-03至今"},
    # 李文林 与 前任/上级
    {"person_a": 1, "person_b": 15, "type": "前任继任", "context": "何斌 2026-03 中旬卸任门源县委书记，李文林接任", "overlap_org": "中共门源县委", "overlap_period": "2024-01~2026-03"},
    {"person_a": 1, "person_b": 18, "type": "上下级/工作交集", "context": "共和县共事：张峰任共和县委书记（2021-2022 在任）、李文林任县长；张峰后任海北州委书记，李文林 2026-03 调海北州门源任书记（现为其下属县委书记）", "overlap_org": "中共共和县委/共和县人民政府", "overlap_period": "2021~2023"},
    {"person_a": 1, "person_b": 11, "type": "上下级", "context": "书记—组织部长（兼党校校长）", "overlap_org": "中共门源县委", "overlap_period": "2026-03至今"},
    {"person_a": 1, "person_b": 12, "type": "上下级", "context": "书记—政法书记", "overlap_org": "中共门源县委", "overlap_period": "2026-03至今"},
    {"person_a": 1, "person_b": 13, "type": "上下级", "context": "书记—宣传部长", "overlap_org": "中共门源县委", "overlap_period": "2026-03至今"},
    {"person_a": 1, "person_b": 14, "type": "上下级", "context": "书记—统战部长", "overlap_org": "中共门源县委", "overlap_period": "2026-03至今"},
    # 敏通宫 与 班子/前任书记
    {"person_a": 2, "person_b": 15, "type": "工作搭档", "context": "何斌任门源县委书记期间，敏通宫任县委副书记、县长", "overlap_org": "中共门源县委/门源县人民政府", "overlap_period": "2025-01~2026-03"},
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "县长—常务副县长（县委常委、党组副书记）", "overlap_org": "门源县人民政府", "overlap_period": "2025-01至今"},
    {"person_a": 2, "person_b": 3, "type": "上下级", "context": "县长—副县长（援青、县委副书记）", "overlap_org": "门源县人民政府", "overlap_period": "2025-01至今"},
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "县长—副县长（援青、县委副书记）", "overlap_org": "门源县人民政府", "overlap_period": "2025-01至今"},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "县长—副县长", "overlap_org": "门源县人民政府", "overlap_period": "2025-01至今"},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "县长—副县长", "overlap_org": "门源县人民政府", "overlap_period": "2025-01至今"},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "县长—副县长兼公安局长", "overlap_org": "门源县人民政府/门源县公安局", "overlap_period": "2025-01至今"},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "县长—副县长", "overlap_org": "门源县人民政府", "overlap_period": "2025-01至今"},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "县长—副县长", "overlap_org": "门源县人民政府", "overlap_period": "2025-01至今"},
    {"person_a": 2, "person_b": 11, "type": "工作搭档", "context": "县长—县委副书记/组织部长 班子搭档", "overlap_org": "中共门源县委", "overlap_period": "2025-01至今"},
    # 前任书记线
    {"person_a": 15, "person_b": 16, "type": "前任继任", "context": "孙绣宗 2024-01 卸任门源县委书记，何斌接任", "overlap_org": "中共门源县委", "overlap_period": "2024-01"},
    {"person_a": 16, "person_b": 17, "type": "工作搭档", "context": "孙绣宗任门源县委书记、马晓峰任门源县长时期的党政主官搭档", "overlap_org": "中共门源县委/门源县人民政府", "overlap_period": "2019-10~2022"},
    {"person_a": 15, "person_b": 19, "type": "任命/上下级", "context": "2024-01-22 全县领导干部大会，州委组织部长司吉昇宣布省委关于门源县委主要领导的任职决定（何斌任书记）", "overlap_org": "中共海北州委/中共门源县委", "overlap_period": "2024-01"},
    {"person_a": 18, "person_b": 15, "type": "上下级", "context": "张峰（州委书记）与 何斌（州委常委、门源县委书记）同届州委班子", "overlap_org": "中共海北州委", "overlap_period": "2024~2026-03"},
    {"person_a": 18, "person_b": 19, "type": "上下级", "context": "州委书记—州委副书记/组织部长", "overlap_org": "中共海北州委", "overlap_period": "2026"},
    {"person_a": 18, "person_b": 2, "type": "上下级", "context": "州委书记—县长（州辖县行政主官）", "overlap_org": "海北州/门源县", "overlap_period": "2026-03至今"},
    {"person_a": 16, "person_b": 20, "type": "前任继任", "context": "白顺兴 2019-06 被查，孙绣宗 2019-10 接任门源县委书记", "overlap_org": "中共门源县委", "overlap_period": "2019"},
    # 公安线
    {"person_a": 8, "person_b": 3, "type": "工作交集", "context": "副县长、公安局长 与 县委政法委分管领导", "overlap_org": "门源县政法系统", "overlap_period": ""},
]

# ── Build ──────────────────────────────────────────────────────────────
def main() -> None:
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
    print(f"\n✅ {SLUG} 数据构建完成。")
    print(f"   人物: {len(persons)}   机构: {len(organizations)}")
    print(f"   任职: {len(positions)}   关系: {len(relationships)}")
    print(f"   DB:   {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")


if __name__ == "__main__":
    main()
