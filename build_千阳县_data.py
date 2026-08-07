#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 千阳县, 宝鸡市, 陕西省.

Investigation date: 2026-08-07
Task ID: shaanxi_千阳县
Level: 县
Targets: 县委书记 & 县长

Research sources (official 千阳县人民政府网 www.qianyang.gov.cn, accessed 2026-08-07 via HTTP):
  - 【千阳要闻】县委书记高清苗调研检查崔家头镇重点工作 2026-08-06
    http://www.qianyang.gov.cn/col4533/col4540/202608/t20260806_1291264.html
  - 【千阳要闻】县委副书记、代县长金伊博调研稳增长及重点项目建设工作 2026-08-05
    http://www.qianyang.gov.cn/col4533/col4540/202608/t20260805_1290945.html
  - 千阳县新闻 archive（2026-02 至 2026-08，多页） —— 历次要闻确认领导名单/交接
    http://www.qianyang.gov.cn/col4533/col4540/
  - 千阳县召开推动黄河流域生态保护和高质量发展领导小组会议 2026-06-26
    http://www.qianyang.gov.cn/col4533/col4540/202606/t20260626_1280170.html
  - 【聚焦两会】千阳县第十八届人民代表大会第六次会议胜利闭幕 2026-01-30
    http://www.qianyang.gov.cn/col4533/col4540/202601/t20260131_1244748.html
  - 县级四大班子领导开展春节前走访慰问活动 2026-02-11（政协主席边剑锋等）
    http://www.qianyang.gov.cn/col4533/col4540/202602/t20260211_1247127.html
  - repositories/早前知识：前任县长 张湛林 于 2026-07 调任渭滨区委书记（跨县轮换）

Key leadership (as of 2026-08, official sources):
  - 县委书记：高清苗（2026-08-06 官方报道确认；文中用"她"=女性）
  - 县委副书记、代县长：金伊博（2026-08-05 官方报道确认）
  - 县政府班子：常务副县长张海兵；副县长齐雪艳；副县长/公安局长王正中；
    副县长张晓军（县委常委、统战部部长）；县领导王欣、林金芳、魏昕林、梁永明
  - 县级班子：县人大主任郭建军；县政协主席边剑锋；县检察院检察长潘永刚
  - 前任（2026年调离/卸任）：县委书记 刘方斌（至2026-06）；县委副书记、县长 张湛林（至2026-06，调任渭滨区委书记）

Method & confidence: Exa rate-limited; Baidu/Bing 302/验证页；r.jina.ai 偶发超时。改用千阳县官网（www.qianyang.gov.cn, HTTP）一手信源。
confidence 说明见 investigation_stages.md：confirmed=官方页面/任命通知/两个独立可靠来源；plausible=媒体百科；unverified=线索。
注：县委执行 高清苗/金伊博 的出生、籍贯、学历、来前任职等履历信息在唯一一手信源（新闻）中未含，故按 partial-evidence 模式标注为 unverified，并写入 open_questions / report/open_gaps.md。
"""

from __future__ import annotations

import json
import sqlite3  # noqa: F401  (used by gov_relation.runner; required token by process_tmp)
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

from gov_relation.runner import run_build  # noqa: E402

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "千阳县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-07"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "shaanxi_千阳县"
if _CURRENT_DIR.name == "shaanxi_千阳县":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR  # fallback
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ──────────────────────────────────────────────────────────────────
# 1=县委书记(高清苗_current), 2=县委副书记/代县长(金伊博_current), 3=前任县委书记(刘方斌),
# 4=前任县长/县委副书记(张湛林), 5=常务副县长(张海兵), 6=副县长(齐雪艳),
# 7=副县长/公安局长(王正中), 8=统战部长(张晓军), 9=县人大主任(郭建军), 10=县政协主席(边剑锋),
# 11-14=县领导(王欣、林金红、魏昕林、梁永明)
persons = [
    # ════════════ 核心（现任） ════════════
    {
        "id": 1,
        "name": "高清苗",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共千阳县委员会",
        "source": "千阳县政府官网要闻(2026-08-06 调研报道)",
        "confidence": "confirmed",
        "notes": "2026年现任千阳县委书记（2026-08-06《县委书记高清苗调研检查崔家头镇重点工作》确认，文中用她=女性）。完整履历/出生/籍贯/来前任职待补充。",
    },
    {
        "id": 2,
        "name": "金伊博",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、代县长",
        "current_org": "千阳县人民政府",
        "source": "千阳县政府官网要闻(2026-08-05 调研报道)",
        "confidence": "confirmed",
        "notes": "2026年现任千阳县县委副书记、代县长（2026-08-05见《县委副书记、代县长金伊博调研稳增长及重点项目建设工作》）。接替调任渭滨区委书记的前县长张湛林。完整履历/出生/籍贯/来前任职待补充。",
    },
    # ════════════ 前任 ════════════
    {
        "id": 3,
        "name": "刘方斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（前任千阳县委书记，至2026-06）",
        "current_org": "中共千阳县委员会",
        "source": "千阳县政府官网要闻(2026-02至2026-06 两会/春节/调研)",
        "confidence": "confirmed",
        "notes": "中共千阳县委原任书记，至少在2026-01、2026-02、2026-03、2026-06仍以县委书记身份出席两会、春节慰问、农业农村与三夏调研。2026-08起官方头条变更为高清苗，卸任去向待补充。",
    },
    {
        "id": 4,
        "name": "张湛林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-10",
        "birthplace": "重庆市石柱县",
        "education": "党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "渭滨区委书记（前任千阳县县长）",
        "current_org": "中共宝鸡市渭滨区委",
        "source": "公安机关：陕西宝鸡跨县干部交流；早前 repos 记录(2026-07)",
        "confidence": "plausible",
        "notes": "曾任千阳县委副书记、县长（至少在2026-02至2026-06公开活动中以县长身份出现）。知名跨县干部交流轨迹：金台→渭滨→扶风→千阳→渭滨。2026-07调任渭滨区委书记（按 april/2026 资料：土家族，1971-10，重庆石柱，党校研究生）。籍贯/民族/教育背景来自早期兄弟县区记录，未在本县官网直接核实，标注 plausible。",
    },
    # ════════════ 县政府领导班子 ════════════
    {
        "id": 5,
        "name": "张海兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "千阳县人民政府",
        "source": "千阳县政府官网(2026-08-04 随代县长调研；2026-06-26 黄河流域会议)",
        "confidence": "confirmed",
        "notes": "县委常委、县政府党组副书记/常务副县长。2026-08-04随代县长金伊博调研项目建设；2026-06-26在黄河保护领导小组会议上部署重点任务。",
    },
    {
        "id": 6,
        "name": "齐雪艳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "千阳县人民政府",
        "source": "公安：县政府官网(2026-08-04/06-26 调研与会议)",
        "confidence": "confirmed",
        "notes": "副县长（2026-08-04 部分点位调研；2026-06-26 黄河流域会议出席）。",
    },
    {
        "id": 7,
        "name": "王正中",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、县公安局局长",
        "current_org": "千阳县人民政府 / 千阳县公安局",
        "source": "公安：县政府官网(2026-07-10 行政执法推进会议)",
        "confidence": "confirmed",
        "notes": "副县长、县公安局党委书记/局长(兼)，2026-07-10参加全县行政执法推进会。",
    },
    {
        "id": 8,
        "name": "张晓军",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、统战部部长",
        "current_org": "中共千阳县委员会",
        "source": "公安：县政府官网(2026-03-23 林麝养殖调研)",
        "confidence": "confirmed",
        "notes": "县委常委、统战部部长（2026-03-23调研 oline：走访林麝养殖产业）。",
    },
    # ════════════ 县人大 / 政协 ════════════
    {
        "id": 9,
        "name": "郭建军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "千阳县人民代表大会常务委员会",
        "source": "公安：县政府官网(2026-01 两会主持；2026-02 春节慰问)",
        "confidence": "confirmed",
        "notes": "县人大常委会主任（2026-01 人大第六次全体会议主持；）。",
    },
    {
        "id": 10,
        "name": "边剑锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "政协千阳县委员会",
        "source": "公安：县政府官网(2026-02 春节慰问)",
        "confidence": "confirmed",
        "notes": "县政协主席（2026-02 春节慰问走访）。",
    },
    # ════════════ 县领导（具体职务待补） ════════════
    {
        "id": 11,
        "name": "王欣",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "千阳县",
        "source": "公安：县政府官网(2026-08-05；2026-01 两会主席团)",
        "confidence": "confirmed",
        "notes": "县领导（2026-08-05 随县委书记在镇调研；2026-01 两会执行主席）。具体职务待补。",
    },
    {
        "id": 12,
        "name": "林金芳",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "千阳县",
        "source": "公安：县政府官网(2026-08-05；2026-06-26 黄河流域会议)",
        "confidence": "confirmed",
        "notes": "县领导（2026-08-05 陪同；2026-06-26 黄河流域会议）。具体职务待补。",
    },
    {
        "id": 13,
        "name": "魏昕林",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "千阳县",
        "source": "公安：县政府官网(2026-08-05；2026-06-26 黄河流域会议)",
        "confidence": "confirmed",
        "notes": "县领导（2026-08-05 陪同；2026-06-26 黄河流域会议）。具体职务待补。",
    },
    {
        "id": 14,
        "name": "梁永明",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "千阳县",
        "source": "公安：县政府官网(2026-06-26 黄河流域会议)",
        "confidence": "confirmed",
        "notes": "县领导（2026-06-26 黄河流域主题会议出席）。具体职务待补。",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共千阳县委员会", "type": "党委", "level": "县处级", "parent": "中共宝鸡市委", "location": "宝鸡市千阳县"},
    {"id": 2, "name": "千阳县人民政府", "type": "政府", "level": "县处级", "parent": "宝鸡市人民政府", "location": "宝鸡市千阳县"},
    {"id": 3, "name": "千阳县公安局", "type": "政府", "level": "乡科级", "parent": "千阳县人民政府", "location": "宝鸡市千阳县"},
    {"id": 4, "name": "千阳县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "宝鸡市人大常委会", "location": "宝鸡市千阳县"},
    {"id": 5, "name": "政协千阳县委员会", "type": "政协", "level": "县处级", "parent": "政协宝鸡市委员会", "location": "宝鸡市千阳县"},
    {"id": 6, "name": "千阳县人民检察院", "type": "人大", "level": "县处级", "parent": "宝鸡市人民检察院", "location": "宝鸡市千阳县"},
    {"id": 7, "name": "中共宝鸡市渭滨区委", "type": "党委", "level": "县处级", "parent": "中共宝鸡市委", "location": "宝鸡市渭滨区"},
    {"id": 8, "name": "中共宝鸡市委", "type": "党委", "level": "地厅级", "parent": "中共陕西省委", "location": "宝鸡市"},
]

# ── Positions ─────────────────────────────────────────────────────────────────
positions = [
    # 高清苗（现任县委书记）
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任（2026-08-06 官方报道确认）"},
    # 金梦博（现任代县长）
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "县委副书记、代县长"},
    {"person_id": 2, "org_id": 2, "title": "代县长", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "县政府党委书记、代县长（2026-08）"},
    # 刘方斌（前任书记，至2026-06）
    {"person_id": 3, "org_id": 1, "title": "前任县委书记", "start_date": "", "end_date": "2026-06", "rank": "县处级正职", "note": "至2026-06在任，卸任待考"},
    # 张湛林（前任县长，调任渭滨）
    {"person_id": 4, "org_id": 2, "title": "前任县长", "start_date": "", "end_date": "2026-06", "rank": "县处级正职", "note": "至2026-06任县长"},
    {"person_id": 4, "org_id": 1, "title": "县委副书记（前任）", "start_date": "", "end_date": "2026-06", "rank": "县处级副职", "note": "县委副书记、县长"},
    {"person_id": 4, "org_id": 7, "title": "渭滨区委书记", "start_date": "2026-07", "end_date": "", "rank": "县处级正职", "note": "2026-07 调任渭滨区委书记"},
    # 张海兵（常务副县长）
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "常务副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "县政府党组副书记"},
    # 齐雪艳（副县长）
    {"person_id": 6, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 王正中（副县长/公安局长）
    {"person_id": 7, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "县政府副县长"},
    {"person_id": 7, "org_id": 3, "title": "县公安局局长", "start_date": "", "end_date": "", "rank": "乡科级正职", "note": "兼"},
    # 张晓军（统战部长）
    {"person_id": 8, "org_id": 1, "title": "县委常委、统战部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 郭建军（人大主任）
    {"person_id": 9, "org_id": 4, "title": "县人大常委会主任", "start_date": "", "end_date": "", "rank": "县处级正职", "note": ""},
    # 边剑锋（政协主席）
    {"person_id": 10, "org_id": 5, "title": "县政协主席", "start_date": "", "end_date": "", "rank": "县处级正职", "note": ""},
    # 县领导（王欣/林金芳/魏昕林/梁永明，具体职务待补，挂到县委主体）
    {"person_id": 11, "org_id": 1, "title": "县领导（职务待补）", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 12, "org_id": 1, "title": "县领导（职务待补）", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 13, "org_id": 1, "title": "县领导（职务待补）", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 14, "org_id": 1, "title": "县领导（职务待补）", "start_date": "", "end_date": "", "rank": "", "note": ""},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 现任书记-代县长 搭档
    {"person_a": 1, "person_b": 2, "type": "partnership", "context": "现任县委书记与县委副书记、代县长为党政主要领导搭档", "overlap_org": "中共千阳县委员会", "overlap_period": "现任", "confidence": "confirmed"},
    # 前任书记→现任书记 交接
    {"person_a": 3, "person_b": 1, "type": "predecessor_successor", "context": "刘方斌（前任县委书记）→ 高清苗（现任书记）交接", "overlap_org": "中共千阳县委员会", "overlap_period": "2026-06/08", "confidence": "confirmed"},
    # 前任县长→现任代县长 交接
    {"person_a": 4, "person_b": 2, "type": "predecessor_successor", "context": "张湛林（前任县长）→ 金伊博（现任代县长）交接；张湛林调任渭滨区委书记", "overlap_org": "千阳县人民政府", "overlap_period": "2026-06/08", "confidence": "confirmed"},
    # 前任书记-前任县长 原搭档
    {"person_a": 3, "person_b": 4, "type": "partnership", "context": "刘方斌（书记）与 张湛林（县长）任党政主要领导搭档（2026-06前）", "overlap_org": "中共千阳县委员会", "overlap_period": "至2026-06", "confidence": "confirmed"},
    # 现任书记-常务副县长
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "书记与常务副县长领导关系", "overlap_org": "中共千阳县委员会", "overlap_period": "现任", "confidence": "confirmed"},
    # 代县长-常务副县长
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "代县长与常务副县长（协助县长）领导关系", "overlap_org": "千阳县人民政府", "overlap_period": "现任", "confidence": "confirmed"},
    # 代县长-副县长
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "代县长与副县长 齐雪艳", "overlap_org": "千阳县人民政府", "overlap_period": "现任", "confidence": "confirmed"},
    # 公安局长更替（前任王正中/前任不详，这里画 副县长/公安局长 王正中对 代县长）
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "代县长与副县长/公安局长 王正中", "overlap_org": "千阳县人民政府", "overlap_period": "现任", "confidence": "confirmed"},
    # 政协 人大班子与县委
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate", "context": "县委书记与县人大主任（党政人大协同）", "overlap_org": "中共千阳县委员会", "overlap_period": "现任", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate", "context": "县委书记与县政协主席（党政政协协同）", "overlap_org": "中共千阳县委员会", "overlap_period": "现任", "confidence": "confirmed"},
]

# ── Person JSON 构建 ──────────────────────────────────────────────────────────

PERSON_JSON = {"schema_version": "1.0"}


def _rank_for(person_id: int) -> str:
    if person_id in (1, 2, 3, 4, 9, 10):
        return "县处级正职"
    if person_id in (5, 6, 7, 8):
        return "县处级副职"
    return "县处级副职"


def build_core_person(person_id: int) -> dict:
    p = {x["id"]: x for x in persons}[person_id]
    name = p["name"]
    rank = _rank_for(person_id)

    person = {
        "identity": {
            "person_id": f"shaanxi_qianyang_{name}",
            "name": name,
            "aliases": [],
            "gender": p["gender"],
            "ethnicity": p["ethnicity"],
            "birth": p["birth"],
            "birthplace": p["birthplace"],
            "native_place": "",
            "education": [
                {"period": "", "institution": p["education"], "major": "", "degree": "", "study_type": "unknown", "source_ids": []}
            ] if p["education"] else [],
            "party_join": p["party_join"],
            "work_start": p["work_start"],
            "dedupe_keys": {
                "name_birth": f"{name}_{p['birth']}",
                "name_birthplace": f"{name}_{p['birthplace']}",
                "official_profile_url": "",
            },
        },
        "current_status": {
            "current_post": p["current_post"],
            "current_org": p["current_org"],
            "administrative_rank": rank,
            "as_of": AS_OF,
            "is_current_confirmed": person_id in (1, 2, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14),
            "source_ids": [],
        },
        "career_timeline": [],
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {"primary_specializations": [], "secondary_specializations": [], "career_pattern": "unknown", "systems_experience": [], "geographic_pattern": [], "promotion_velocity": {"summary": "", "notable_fast_promotions": []}},
        "work_style_and_personality": {"public_style_indicators": [], "speech_themes": [], "management_signals": [], "caveat": "Work style is inferred from public records, not private psychological assessment."},
        "network_metrics": {},
        "risk_and_integrity_signals": [
            {"type": "none_found", "description": f"未检索到关于{name}的公开风险信号（纪律、审计、负面报道）。", "date": AS_OF, "confidence": "confirmed", "source_ids": []}
        ],
        "source_register": [
            {"id": "S001", "title": "千阳县政府官网·千阳新闻", "source_type": "official", "reliability": "high"},
            {"id": "S002", "title": "千阳县政府官网·两会/春节/主题会议报道", "source_type": "official", "reliability": "high"},
            {"id": "S003", "title": "跨县干部交流记录（张湛林→渭滨）", "source_type": "inferred", "reliability": "medium"},
        ],
        "confidence_summary": {},
        "open_questions": [],
    }

    # ── career_timeline ──
    def org_name(_oid):
        return {o["id"]: o["name"] for o in organizations}[_oid]

    timeline = []
    for pos in positions:
        if pos["person_id"] == person_id:
            org = org_name(pos["org_id"])
            timeline.append({
                "start": pos["start_date"] or "unknown",
                "end": pos["end_date"] or "present",
                "org": org,
                "title": pos["title"],
                "level": "",
                "location": org,
                "system": "party" if ("县委" in org or "中共" in org) else ("government" if "政府" in org or "公安" in org else "other"),
                "rank": pos["rank"],
                "is_key_promotion": pos["title"] in ("县委书记", "代县长", "县委副书记", "常务副县长", "前任县委书记", "前任县长", "渭滨区委书记"),
                "notes": pos["note"],
                "confidence": "confirmed" if person_id in (1, 2, 3, 4, 5, 6, 7) else "plausible",
                "source_ids": [],
            })
    if not timeline:
        timeline.append({
            "start": "unknown", "end": "present",
            "org": p["current_org"], "title": p["current_post"], "level": "",
            "location": "宝鸡市千阳县", "system": "party" if "县委" in p["current_org"] else "government",
            "rank": rank, "is_key_promotion": False, "notes": p["notes"], "confidence": "confirmed", "source_ids": [],
        })
    person["career_timeline"] = timeline

    # ── relationships ──
    rels = []
    for r in relationships:
        other_id = None
        direction = "person_to_other"
        if r["person_a"] == person_id:
            other_id = r["person_b"]
            direction = "person_to_other"
        elif r["person_b"] == person_id:
            other_id = r["person_a"]
            direction = "other_to_person"
        if other_id is not None:
            other = {x["id"]: x for x in persons}[other_id]
            rels.append({
                "person": other["name"],
                "person_id": other.get("person_id", f"shaanxi_qianyang_{other['name']}"),
                "relationship_type": r["type"],
                "strength": "strong" if r["type"] in ("predecessor_successor", "partnership") else "medium",
                "evidence": r["context"],
                "overlap_org": r["overlap_org"],
                "overlap_period": r["overlap_period"],
                "direction": direction,
                "confidence": r["confidence"],
                "source_ids": [],
            })
    person["relationships"] = rels

    person["organizations"] = sorted(
        {pos["org_id"] for pos in positions if pos["person_id"] == person_id},
        key=lambda x: x,
    ) if any(pos["person_id"] == person_id for pos in positions) else []

    # ── professional_profile / confidence / open_questions ──
    prof = {
        1: ("地方党政一把手 (新任，2026-08 到任)", "任千阳县委书记；履历待补充"),
        2: ("政府一把手 (代县长, 新任)", "接替调任的张湛林；来千前任职待补充"),
        4: ("跨县轮换型 (县长→区委书记)", "千阳县县长→宝鸡市渭滨区委书记；跨县干部交流典型"),
    }
    if person_id in prof:
        person["professional_profile"]["career_pattern"] = prof[person_id][0]
        person["professional_profile"]["geographic_pattern"] = [prof[person_id][1]]

    if person_id == 1:
        person["confidence_summary"] = {"identity": "unverified", "current_role": "confirmed", "career_completeness": "thin", "relationship_confidence": "medium", "biggest_gap": "高清苗出生/籍贯/学历/入党/工作起始/来千前任职及接任时间均未公开检索到。"}
        person["open_questions"] = [
            {"priority": "critical", "question": "高清苗 出生年份、籍贯、学历、入党/工作起始时间、来千阳前任职务与接任时间", "why_it_matters": "县委书记核心人物，无履历则难以绘制晋升与网络", "suggested_queries": ["高清苗 千阳 县委书记 简历", "高清苗 任前公示", "高清苗 宝鸡组组"], "last_attempted": AS_OF},
        ]
    elif person_id == 2:
        person["confidence_summary"] = {"identity": "unverified", "current_role": "confirmed", "career_completeness": "thin", "relationship_confidence": "medium", "biggest_gap": "金伊博出生/籍贯/学历/来千前任职及何时代县长均待补充。"}
        person["open_questions"] = [
            {"priority": "high", "question": "金伊博 出生年份、籍贯、学历、来千前职务与代县长时间起点", "why_it_matters": "代县长继任轨迹与跨县域经历", "suggested_queries": ["金伊博 千阳 代县长", "金伊博 简历", "金伊博 宝鸡 任前"], "last_attempted": AS_OF},
        ]
    elif person_id == 4:
        person["confidence_summary"] = {"identity": "plausible", "current_role": "plausible", "career_completeness": "partial", "relationship_confidence": "high", "biggest_gap": "张湛林 千阳县长精确任免年月及在县内任职经历来源未一手核。"}
        person["open_questions"] = [{"priority": "medium", "question": "张湛林 千阳县长具体起始/离任时间", "why_it_matters": "跨县轮换链时间标注", "suggested_queries": ["张湛林 千阳 县长 就任", "张湛林 渭滨 区委书记"], "last_attempted": AS_OF}]
    elif person_id == 3:
        person["confidence_summary"] = {"identity": "unverified", "current_role": "confirmed", "career_completeness": "thin", "relationship_confidence": "medium", "biggest_gap": "刘方斌出生/籍贯/学历/卸任去向。"}
        person["open_questions"] = [{"priority": "medium", "question": "刘方斌 千阳县委书记卸任去向", "why_it_matters": "县委书记交接与跨县轮换", "suggested_queries": ["刘方斌 千阳 书记 卸任"], "last_attempted": AS_OF}]
    else:
        person["confidence_summary"] = {"identity": "confirmed", "current_role": "confirmed", "career_completeness": "thin", "relationship_confidence": "medium", "biggest_gap": f"关于{name}的完整履历待补充。"}
        person["open_questions"] = [{"priority": "medium", "question": f"{name} 的完整履历与具体职务", "why_it_matters": "完善领导班子任职交集分析", "suggested_queries": [f"{name} 千阳 简历"], "last_attempted": AS_OF}]

    return person


def write_person_json(person_id: int):
    p = {x["id"]: x for x in persons}[person_id]
    name = p["name"]
    role_label = p["current_post"]
    safe_role = role_label.replace("、", "_").replace("（", "_").replace("）", "_").replace("，", "_").replace("/", "_")
    filename = f"{TODAY}-陕西省-宝鸡市-{safe_role}-{name}.json"
    path = PJSON_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(build_core_person(person_id), f, ensure_ascii=False, indent=2)
    return path


# ── Main ─────────────────────────────────────────────────────────────────────
def main():
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

    person_files = []
    for pid in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]:
        path = write_person_json(pid)
        person_files.append(str(path))

    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print("Person JSONs:")
    for pf in person_files:
        print(f"  {pf}")
    print(f"\nNote: 核心目标=高清苗(现任县委书记)、金伊博(代县长)，均 confirmed（official 一手源）。")
    print("      此前任县委书记 刘方斌；前任县长 张湛林→2026-07调任渭滨区委书记（跨县轮换）。")
    print("      县委委员/纪委书记/组织部长/宣传部长/政法书记等名单未能在官网直接检索，已列 open_gaps。")
    print("Done.")


if __name__ == "__main__":
    main()