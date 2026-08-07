#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 榆树市 (Yushu City), 吉林省.

Investigation date: 2026-08-06
Task ID: jilin_榆树市
Level: 县级市
Targets: 市委书记 & 市长

Research sources:
  - Official government site (live, HTTP): http://www.yushu.gov.cn/ (leaderboard pages
    /xxgk/ldjj/{sw,szf,srd,szx}/ + per-leader bio pages) — primary, high reliability.
  - Leader activity archives across 2023–2026 (to establish predecessors & roles).

Confidence notes:
  - 刘菁蕾 (Party Secretary): confirmed — official bio (born 1979-12, 吉林大安, 硕士研究生).
  - 张子明 (Mayor): confirmed — official bio (born 1985-02, 在职研究生, 2009-08 参加工作).
  - Full standing committee & deputy-mayor roster: confirmed via official leaderboard pages.
  - Predecessors (吴威, 林小明, 高洪洲, 金海) reconstructed from official activity archives;
    precise dates & bios of predecessors unverified (web search engines blocked/captcha'd).
  - All claims labeled with confidence; gaps explicitly documented.
"""

from __future__ import annotations

import json
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

import sqlite3  # noqa: used by gov_relation.runner via import
from gov_relation.runner import run_build

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "榆树市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "jilin_榆树市"
if _CURRENT_DIR.name == "jilin_榆树市":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
persons = [
    # ══════════════ Core (current) ══════════════
    {
        "id": 1, "name": "刘菁蕾", "gender": "男", "ethnicity": "汉族",
        "birth": "1979-12", "birthplace": "吉林大安", "education": "硕士研究生",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委书记", "current_org": "中共榆树市委",
        "source": "http://www.yushu.gov.cn/xxgk/ldjj/sw/ljl/",
        "confidence": "confirmed",
        "notes": "现任中共榆树市委书记。曾任长春市朝阳区委常委、政法委书记，长春市南关区委常委、区政府党组副书记、副区长，长春市南关区委副书记、区政府党组书记、区长。跨区(长春南关区→榆树市)调任。",
    },
    {
        "id": 2, "name": "张子明", "gender": "男", "ethnicity": "汉族",
        "birth": "1985-02", "birthplace": "", "education": "在职研究生",
        "party_join": "中共党员", "work_start": "2009-08",
        "current_post": "市长", "current_org": "榆树市人民政府",
        "source": "http://www.yushu.gov.cn/xxgk/ldjj/szf/zzm/",
        "confidence": "confirmed",
        "notes": "现任中共榆树市委副书记、榆树市人民政府党组书记、市长。2009年8月参加工作。曾任农安县烧锅镇人大代表主席，农安县委常委、烧锅镇党委书记，农安县委常委、政法委书记，农安县委常委、农安县人民政府党组成员、副县长。跨县(农安县→榆树市)调任。",
    },
    # ══════════════ 市委班子 ══════════════
    {
        "id": 10, "name": "贾朔", "gender": "男", "ethnicity": "汉族",
        "birth": "1982-01", "birthplace": "", "education": "在职研究生",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委副书记", "current_org": "中共榆树市委",
        "source": "http://www.yushu.gov.cn/xxgk/ldd/sw/js/",
        "confidence": "confirmed",
        "notes": "曾任长春市国有资本投资运营集团总经理助理、副总经理，长春市财政局金融处副处长。现任榆树市委副书记。来自长春市属国企/财政系统。",
    },
    {
        "id": 3, "name": "陈澎", "gender": "男", "ethnicity": "汉族",
        "birth": "1989-01", "birthplace": "", "education": "研究生",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委常委、常务副市长", "current_org": "榆树市人民政府",
        "source": "http://www.yushu.gov.cn/xxgk/ldd/sw/cp/",
        "confidence": "confirmed",
        "notes": "曾任农安县副县长、县政府党组成员。现任榆树市委常委、市政府常务副市长。跨县(农安→榆树)调任。",
    },
    {
        "id": 4, "name": "张龙彪", "gender": "男", "ethnicity": "汉族",
        "birth": "1978-08", "birthplace": "", "education": "大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委常委、副市长", "current_org": "榆树市人民政府",
        "source": "http://www.yushu.gov.cn/xxgk/ldd/sw/zlb/",
        "confidence": "confirmed",
        "notes": "曾任长春市审计局教科文卫审计处副处长、办公室主任、教科文卫审计处处长，榆树市人民政府党组成员、副市长。现任榆树市委常委、副市长。来自长春市直机关。",
    },
    {
        "id": 5, "name": "孙跃福", "gender": "男", "ethnicity": "汉族",
        "birth": "1976-10", "birthplace": "", "education": "大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委常委、政法委书记", "current_org": "中共榆树市委政法委",
        "source": "http://www.yushu.gov.cn/xxgk/ldd/sw/syf/",
        "confidence": "confirmed",
        "notes": "曾任榆树市龙泉镇党委副书记、镇长，榆树市委办公室主任、兼档案局局长，榆树市人民政府党组成员、副市长。现任榆树市委常委、政法委书记。本地成长。",
    },
    {
        "id": 6, "name": "李中萍", "gender": "女", "ethnicity": "汉族",
        "birth": "1974-03", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委常委、宣传部部长", "current_org": "中共榆树市委宣传部",
        "source": "http://www.yushu.gov.cn/xxgk/ldd/lizhongping/",
        "confidence": "confirmed",
        "notes": "",
    },
    {
        "id": 7, "name": "孙健鹏", "gender": "男", "ethnicity": "汉族",
        "birth": "1978-06", "birthplace": "", "education": "大学本科",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委常委、市纪委书记", "current_org": "中共榆树市纪律检查委员会",
        "source": "http://www.yushu.gov.cn/xxgk/ldd/sw/sjp/",
        "confidence": "confirmed",
        "notes": "曾任长春市纪委监委驻市建委纪检监察组副组长，长春市纪委监委案件监督管理室副主任、第三监督检查室副主任。现任榆树市委常委、市纪委书记、市监委主任。来自长春市纪委监委。",
    },
    {
        "id": 8, "name": "门立君", "gender": "男", "ethnicity": "汉族",
        "birth": "1978-02", "birthplace": "", "education": "大学本科",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委常委、组织部部长", "current_org": "中共榆树市委组织部",
        "source": "http://www.yushu.gov.cn/xxgk/ldd/sw/mlj/",
        "confidence": "confirmed",
        "notes": "曾任长春市绿园区同心街道党工委、迎宾街道党工委副书记、办事处主任，长春市合心镇党委书记。现任榆树市委常委、组织部部长。",
    },
    {
        "id": 9, "name": "马光辉", "gender": "男", "ethnicity": "汉族",
        "birth": "1971-08", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委常委、统战部部长", "current_org": "中共榆树市委统战部",
        "source": "http://www.yushu.gov.cn/xxgk/ldd/sw/mgh/",
        "confidence": "confirmed",
        "notes": "曾任榆树市政府办公室主任，五棵树镇党委书记，榆树市人民政府党组成员、副市长。现任榆树市委常委、统战部部长。本地成长。",
    },
    {
        "id": 12, "name": "杨楠", "gender": "男", "ethnicity": "汉族",
        "birth": "1979-02", "birthplace": "", "education": "大学本科",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市委常委、市人武部部长", "current_org": "榆树市人民武装部",
        "source": "http://www.yushu.gov.cn/xxgk/ldd/sw/yn/",
        "confidence": "confirmed",
        "notes": "曾任空军长春指挥所参谋长助理、黑龙江省军区佳木斯军分区郊区人武部部长。现任榆树市委常委、市人武部部长。军队转业。",
    },
    # ══════════════ 副市长 ══════════════
    {
        "id": 20, "name": "王海艳", "gender": "女", "ethnicity": "汉族",
        "birth": "1976-01", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副市长", "current_org": "榆树市人民政府",
        "source": "http://www.yushu.gov.cn/xxgk/ldd/szf/wanghaiyan/",
        "confidence": "confirmed",
        "notes": "曾任榆树市妇女联合会党组书记、主席，榆树市多年来黑林镇党委书记，榆树市城宜街道党工委书记。",
    },
    {
        "id": 21, "name": "王野", "gender": "男", "ethnicity": "汉族",
        "birth": "1979-06", "birthplace": "", "education": "大学本科",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副市长、市公安局局长", "current_org": "榆树市人民政府",
        "source": "http://www.yushu.gov.cn/xxgk/ldd/szf/wangye/",
        "confidence": "confirmed",
        "notes": "曾任长春市公安局朝阳分局建设广场派出所所长、桂林路派出所所长，长春市公安局绿园区分局副局长，长春市公安局九台区分局党委副书记、政委。",
    },
    {
        "id": 22, "name": "吕晓龙", "gender": "男", "ethnicity": "汉族",
        "birth": "1989-11", "birthplace": "", "education": "大学本科",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副市长", "current_org": "榆树市人民政府",
        "source": "http://www.yushu.gov.cn/xxgk/ldd/szf/lxl/",
        "confidence": "confirmed",
        "notes": "曾任农安县永安乡团委书记、副乡长，农安县经济合作促进中心主任，农安县巴吉垒镇党委书记。跨县(农安→榆树)。",
    },
    {
        "id": 23, "name": "于浩", "gender": "男", "ethnicity": "汉族",
        "birth": "1984-04", "birthplace": "", "education": "在职研究生",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副市长", "current_org": "榆树市人民政府",
        "source": "http://www.yushu.gov.cn/xxgk/ldd/szf/yuhao/",
        "confidence": "confirmed",
        "notes": "曾任九台区土伦岭街道党工委、九台区兴隆街道党工委书记，九台区委社会工作部部长。",
    },
    {
        "id": 24, "name": "周海松", "gender": "男", "ethnicity": "汉族",
        "birth": "1986-03", "birthplace": "", "education": "在职研究生",
        "party_join": "中共党员", "work_start": "",
        "current_post": "副市长", "current_org": "榆树市人民政府",
        "source": "http://www.yushu.gov.cn/xxgk/ldd/szf/zzh/",
        "confidence": "confirmed",
        "notes": "曾任德惠市米沙子党委副书记，长春市委组织部、长春市双阳区齐家镇党委副书记、镇长、党委书记。",
    },
    # ══════════════ 人大 ══════════════
    {
        "id": 30, "name": "吴喜庆", "gender": "男", "ethnicity": "汉族",
        "birth": "1968-10", "birthplace": "", "education": "研究生",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市人大常委会党组书记、主任", "current_org": "榆树市人大",
        "source": "http://www.yushu.gov.cn/xxgk/ldd/srd/wxq/",
        "confidence": "confirmed",
        "notes": "曾任榆树市经济局局长、长春五棵树经济开发区管委会主任、榆树市副市长、政法委书记、市委副书记等。现任榆树市人大常委会党组书记、主任。",
    },
    {
        "id": 31, "name": "姜兴俊", "gender": "男", "ethnicity": "汉族",
        "birth": "1972-10", "birthplace": "", "education": "大学本科",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市人大常委会副主任", "current_org": "榆树市人大",
        "source": "http://www.yushu.gov.cn/xxgk/ldd/srd/jxj/",
        "confidence": "confirmed",
        "notes": "曾任榆树市泗河镇党委书记、五棵树镇党委书记。",
    },
    {
        "id": 32, "name": "王树申", "gender": "男", "ethnicity": "汉族",
        "birth": "1971-03", "birthplace": "", "education": "研究生",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市人大常委会副主任", "current_org": "榆树市人大",
        "source": "http://www.yushu.gov.cn/xxgk/ldd/srd/wangss/",
        "confidence": "confirmed",
        "notes": "曾任榆树市污染源调查，榆树环城乡党委书记、五棵树镇党委书记、长春五棵科技开发区管委会主任。",
    },
    {
        "id": 33, "name": "宋学普", "gender": "男", "ethnicity": "汉族",
        "birth": "1978-01", "birthplace": "", "education": "大学本科",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市人大常委会副主任、市委组织部常务副部长", "current_org": "榆树市人大",
        "source": "http://www.yushu.gov.cn/xxgk/ldd/srd/sxp/",
        "confidence": "confirmed",
        "notes": "曾任榆树市刘家镇党委书记，市政府办公室党组书记、主任，市市场监督管理局党组书记、局长。",
    },
    # ══════════════ 政协 ══════════════
    {
        "id": 40, "name": "闫伟", "gender": "男", "ethnicity": "汉族",
        "birth": "1971-03", "birthplace": "", "education": "大学本科",
        "party_join": "中共党员", "work_start": "",
        "current_post": "市政协党组书记、主席", "current_org": "政协榆树市委员会",
        "source": "http://www.yushu.gov.cn/xxgk/ldd/szx/yw/",
        "confidence": "confirmed",
        "notes": "曾任榆树市五棵树镇党委书记，榆树市副市长、市委常委、统战部长，现任榆树市政协党组书记、主席。",
    },
    {
        "id": 41, "name": "绳丽光", "gender": "女", "ethnicity": "汉族",
        "birth": "1973-05", "birthplace": "", "education": "大学本科",
        "party_join": "中国民主促进会", "work_start": "1996-07",
        "current_post": "市政协副主席", "current_org": "政协榆树市委员会",
        "source": "http://www.yushu.gov.cn/xxgk/ldd/szx/slg/",
        "confidence": "confirmed",
        "notes": "2009年4月加入民进。曾任榆树市机关事务服务中心/管理局局长、融媒体中心主任。现任榆树市政协副主席、民进榆树市委主委。",
    },
    # ══════════════ 前任 ══════════════
    {
        "id": 50, "name": "吴威", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "前任市委书记", "current_org": "中共榆树市委",
        "source": "http://www.yushu.gov.cn/xxgk/ldd/ (activity archives)",
        "confidence": "plausible",
        "notes": "吴威 2024 任榆树市长，2025 升任榆树市委书记，至 2026 年初卸任，由刘菁蕾接任。去向待查。",
    },
    {
        "id": 51, "name": "高洪洲", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "前任市人大常委会主任", "current_org": "榆树市人大",
        "source": "http://www.yushu.gov.cn/xxgk/ldd/ (activity archives)",
        "confidence": "plausible",
        "notes": "2024-2026人大审议活动与班子成员并列，前任人大常委会主任，2026换届后由吴喜庆接任。",
    },
    {
        "id": 52, "name": "林小明", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "前任市委书记", "current_org": "中共榆树市委",
        "source": "http://www.yushu.gov.cn/xxgk/ldd/ (activity archives)",
        "confidence": "plausible",
        "notes": "2023-2024 任榆树市委书记(主持市委常委会、党建工作领导小组等)，后由吴威接任。去向待查。",
    },
    {
        "id": 53, "name": "金海", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "前任市政协主席", "current_org": "政协榆树市委员会",
        "source": "http://www.yushu.gov.cn/xxgk/ldd/ (activity archives)",
        "confidence": "plausible",
        "notes": "2024-2026 政协/人大活动与吴欢、张子明并列，前任市政协主席，2026换届后由闫伟接任。",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共榆树市委", "type": "党委", "level": "县级", "parent": "中共长春市委", "location": "榆树市"},
    {"id": 2, "name": "榆树市人民政府", "type": "政府", "level": "县级", "parent": "长春市人民政府", "location": "榆树市"},
    {"id": 3, "name": "中共榆树市纪律检查委员会", "type": "纪委", "level": "县级", "parent": "中共榆树市委", "location": "榆树市"},
    {"id": 4, "name": "中共榆树市委组织部", "type": "党委部门", "level": "县级", "parent": "中共榆树市委", "location": "榆树市"},
    {"id": 5, "name": "中共榆树市委宣传部", "type": "党委部门", "level": "县级", "parent": "中共榆树市委", "location": "榆树市"},
    {"id": 6, "name": "中共榆树市委政法委", "type": "党委部门", "level": "县级", "parent": "中共榆树市委", "location": "榆树市"},
    {"id": 7, "name": "中共榆树市委统战部", "type": "党委部门", "level": "县级", "parent": "中共榆树市委", "location": "榆树市"},
    {"id": 8, "name": "榆树市人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "长春市人大常委会", "location": "榆树市"},
    {"id": 9, "name": "中国人民政治协商会议榆树市委员会", "type": "政协", "level": "县级", "parent": "政协长春市委员会", "location": "榆树市"},
    {"id": 10, "name": "榆树市人民武装部", "type": "军事", "level": "县级", "parent": "长春警备区", "location": "榆树市"},
    {"id": 11, "name": "中共长春市委", "type": "党委", "level": "副省级", "parent": "中共吉林省委", "location": "长春市"},
    {"id": 12, "name": "长春市人民政府", "type": "政府", "level": "副省级", "parent": "吉林省人民政府", "location": "长春市"},
    {"id": 13, "name": "中共农安县委", "type": "党委", "level": "县级", "parent": "中共长春市委", "location": "农安县"},
    {"id": 14, "name": "农安县人民政府", "type": "政府", "level": "县级", "parent": "长春市人民政府", "location": "农安县"},
    {"id": 15, "name": "中共长春市南关区委员会", "type": "党委", "level": "县级", "parent": "中共长春市委", "location": "长春市南关区"},
    {"id": 16, "name": "长春市南关区人民政府", "type": "政府", "level": "县级", "parent": "长春市人民政府", "location": "长春市南关区"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 刘菁蕾
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "2026", "end_date": "present", "rank": "正处", "note": "现任中共榆树市委书记"},
    {"person_id": 1, "org_id": 15, "title": "南关区委副书记、区政府党组书记、区长", "start_date": "", "end_date": "2026", "rank": "正处", "note": "前任职务"},
    {"person_id": 1, "org_id": 15, "title": "南关区委常委、副区长", "start_date": "", "end_date": "", "rank": "副处", "note": ""},
    {"person_id": 1, "org_id": 11, "title": "(前)朝阳区委常委、政法委书记", "start_date": "", "end_date": "", "rank": "副处", "note": "长春市朝阳区"},
    # 张子明
    {"person_id": 2, "org_id": 2, "title": "市长(市政府党组书记)", "start_date": "2025", "end_date": "present", "rank": "正处", "note": "现任榆树市长"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记(兼)", "start_date": "2025", "end_date": "present", "rank": "正处", "note": ""},
    {"person_id": 2, "org_id": 14, "title": "农安县副县长(县委常委、政法委书记)", "start_date": "", "end_date": "2025", "rank": "副处", "note": ""},
    # 贾朔
    {"person_id": 10, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "", "rank": "副处", "note": ""},
    # 陈澎
    {"person_id": 3, "org_id": 2, "title": "常务副市长", "start_date": "", "end_date": "", "rank": "副处", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副处", "note": ""},
    # 张龙彪
    {"person_id": 4, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副处", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "副处", "note": ""},
    # 孙跃福
    {"person_id": 5, "org_id": 6, "title": "市委常委、政法委书记", "start_date": "", "end_date": "", "rank": "副处", "note": ""},
    # 李中萍
    {"person_id": 6, "org_id": 5, "title": "市委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "副处", "note": ""},
    # 孙健鹏
    {"person_id": 7, "org_id": 3, "title": "市委常委、市纪委书记", "start_date": "", "end_date": "", "rank": "副处", "note": ""},
    # 门立君
    {"person_id": 8, "org_id": 4, "title": "市委常委、组织部部长", "start_date": "", "end_date": "", "rank": "副处", "note": ""},
    # 马光辉
    {"person_id": 9, "org_id": 7, "title": "市委常委、统战部部长", "start_date": "", "end_date": "", "rank": "副处", "note": ""},
    # 杨楠
    {"person_id": 12, "org_id": 10, "title": "市委常委、市人武部部长", "start_date": "", "end_date": "", "rank": "副处", "note": ""},
    # 副市长
    {"person_id": 20, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副处", "note": ""},
    {"person_id": 21, "org_id": 2, "title": "副市长、市公安局局长", "start_date": "", "end_date": "", "rank": "副处", "note": ""},
    {"person_id": 22, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副处", "note": ""},
    {"person_id": 23, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副处", "note": ""},
    {"person_id": 24, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "副处", "note": ""},
    # 人大
    {"person_id": 30, "org_id": 8, "title": "市人大常委会主任(党组书记)", "start_date": "2026", "end_date": "present", "rank": "正处", "note": ""},
    {"person_id": 31, "org_id": 8, "title": "市人大常委会副主任", "start_date": "", "end_date": "", "rank": "副处", "note": ""},
    {"person_id": 32, "org_id": 8, "title": "市人大常委会副主任", "start_date": "", "end_date": "", "rank": "副处", "note": ""},
    {"person_id": 33, "org_id": 8, "title": "市人大常委会副主任", "start_date": "", "end_date": "", "rank": "副处", "note": ""},
    # 政协
    {"person_id": 40, "org_id": 9, "title": "市政协主席(党组书记)", "start_date": "2026", "end_date": "present", "rank": "正处", "note": ""},
    {"person_id": 41, "org_id": 9, "title": "市政协副主席", "start_date": "", "end_date": "", "rank": "副处", "note": ""},
    # 前任
    {"person_id": 50, "org_id": 1, "title": "市委书记", "start_date": "2025", "end_date": "2026", "rank": "正处", "note": "前任书记 吴威"},
    {"person_id": 50, "org_id": 2, "title": "市长", "start_date": "2024", "end_date": "2025", "rank": "正处", "note": "吴威 2024 任市长"},
    {"person_id": 52, "org_id": 1, "title": "市委书记", "start_date": "2023", "end_date": "2025", "rank": "正处", "note": "前任书记 林小明"},
    {"person_id": 51, "org_id": 8, "title": "市人大常委会主任", "start_date": "2024", "end_date": "2026", "rank": "正处", "note": "前任人大主任 高洪洲"},
    {"person_id": 53, "org_id": 9, "title": "市政协主席", "start_date": "2024", "end_date": "2026", "rank": "正处", "note": "前任政协主席 金海"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "市委书记—市长搭档", "overlap_org": "榆树市", "overlap_period": "2026-至今"},
    {"person_a": 1, "person_b": 10, "type": "共事", "context": "书记—副书记(贾朔)", "overlap_org": "中共榆树市委", "overlap_period": ""},
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "书记—常务副市长(陈澎)", "overlap_org": "中共榆树市委", "overlap_period": ""},
    {"person_a": 2, "person_b": 3, "type": "共事", "context": "市长—常务副市长", "overlap_org": "榆树市人民政府", "overlap_period": ""},
    # 市委班子内部
    {"person_a": 3, "person_b": 4, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共榆树市委", "overlap_period": ""},
    {"person_a": 3, "person_b": 5, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共榆树市委", "overlap_period": ""},
    {"person_a": 3, "person_b": 6, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共榆树市委", "overlap_period": ""},
    {"person_a": 3, "person_b": 7, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共榆树市委", "overlap_period": ""},
    {"person_a": 4, "person_b": 5, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共榆树市委", "overlap_period": ""},
    {"person_a": 4, "person_b": 6, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共榆树市委", "overlap_period": ""},
    {"person_a": 4, "person_b": 7, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共榆树市委", "overlap_period": ""},
    {"person_a": 5, "person_b": 6, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共榆树市委", "overlap_period": ""},
    {"person_a": 5, "person_b": 7, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共榆树市委", "overlap_period": ""},
    {"person_a": 6, "person_b": 7, "type": "同僚", "context": "市委常委同僚", "overlap_org": "中共榆树市委", "overlap_period": ""},
    # 人大/政协
    {"person_a": 1, "person_b": 30, "type": "共事", "context": "书记—人大主任(吴喜庆)", "overlap_org": "榆树市", "overlap_period": ""},
    {"person_a": 1, "person_b": 40, "type": "共事", "context": "书记—政协主席(闫伟)", "overlap_org": "榆树市", "overlap_period": ""},
    {"person_a": 2, "person_b": 30, "type": "共事", "context": "市长—人大主任", "overlap_org": "榆树市", "overlap_period": ""},
    {"person_a": 2, "person_b": 40, "type": "共事", "context": "市长—政协主席", "overlap_org": "榆树市", "overlap_period": ""},
    # 前任交接
    {"person_a": 50, "person_b": 1, "type": "交接", "context": "前任书记(吴威)→现任书记(刘菁蕾)", "overlap_org": "中共榆树市委", "overlap_period": "2026"},
    {"person_a": 52, "person_b": 50, "type": "交接", "context": "前任书记(林小明)→吴威", "overlap_org": "中共榆树市委", "overlap_period": "2025"},
    {"person_a": 50, "person_b": 2, "type": "交接", "context": "前任市长(吴威)→市长(张子明)", "overlap_org": "榆树市人民政府", "overlap_period": "2025"},
    {"person_a": 51, "person_b": 30, "type": "交接", "context": "前任人大主任(高洪洲)→吴喜庆", "overlap_org": "榆树市人大常委会", "overlap_period": "2026"},
    {"person_a": 53, "person_b": 40, "type": "交接", "context": "前任政协主席(金海)→闫伟", "overlap_org": "政协榆树市委员会", "overlap_period": "2026"},
    # 跨县交流
    {"person_a": 1, "person_b": 2, "type": "跨县交流", "context": "刘菁蕾(长春南关区长)与张子明(农安县副县长)先后调任榆树，长春县域干部交流", "overlap_org": "长春市", "overlap_period": "2025-2026"},
    {"person_a": 3, "person_b": 2, "type": "同县", "context": "陈澎与张子明均曾任农安县领导，同县行政共事", "overlap_org": "农安县", "overlap_period": ""},
]


def _get_open_questions(person: dict) -> list[str]:
    questions = []
    if not person.get("birth"):
        questions.append("出生年月未确认")
    if not person.get("birthplace"):
        questions.append("籍贯未确认")
    if not person.get("education"):
        questions.append("学历教育背景未确认")
    if not person.get("work_start"):
        questions.append("参加工作年份未确认")
    return questions


def write_person_json(person: dict) -> None:
    """Write a per-person graph JSON file following the person_graph_json.md schema."""
    pid = person["id"]
    name = person["name"]
    slug_id = f"yushu_{name}"

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
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001"],
        })

    person_rels = [r for r in relationships if r["person_a"] == pid or r["person_b"] == pid]
    rels_output = []
    for r in person_rels:
        other_id = r["person_b"] if r["person_a"] == pid else r["person_a"]
        other = next((p for p in persons if p["id"] == other_id), None)
        other_name = other["name"] if other else f"person_{other_id}"
        rels_output.append({
            "person": other_name,
            "person_id": f"yushu_{other_name}",
            "relationship_type": "overlap" if r["type"] in ("共事", "同僚", "跨县交流", "同县") else "predecessor_successor",
            "strength": "strong" if r["type"] in ("共事", "跨县交流") else ("medium" if r["type"] in ("同僚", "交接") else "weak"),
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "plausible",
            "source_ids": ["S001"],
        })

    sources = [{
        "id": "S001",
        "title": "榆树市人民政府领导简介（官方）",
        "url": person.get("source", "") or "http://www.yushu.gov.cn/xxgk/ldd/",
        "publisher": "榆树市人民政府",
        "published_at": "",
        "accessed_at": AS_OF,
        "source_type": "official",
        "reliability": "high" if person.get("confidence") == "confirmed" else "medium",
        "notes": "官方县网领导简介页面；前任领导履历基于活动归档推断",
    }]

    is_core = pid in {1, 2}
    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "吉林省", "city": "长春市", "region": "榆树市",
            "job": person.get("current_post", ""),
            "task_id": "jilin_榆树市", "time_focus": "2026年8月",
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
            "education": [{"period": "", "institution": "", "major": "", "degree": person.get("education", ""), "study_type": "unknown"}],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{person.get('birth','')}",
                "name_birthplace": f"{name}_{person.get('birthplace','')}",
                "official_profile_url": person.get("source", ""),
            },
        },
        "current_status": {
            "current_post": person.get("current_post", ""),
            "current_org": person.get("current_org", ""),
            "administrative_rank": "正处",
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
            "career_pattern": "cross_county_rotation",
            "systems_experience": [],
            "geographic_pattern": ["榆树市", "长春市"],
            "promotion_velocity": {"summary": "", "notable_fast_promotions": []},
        },
        "work_style_and_personality": {
            "public_style_indicators": [],
            "speech_themes": [],
            "management_signals": [],
            "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment.",
        },
        "network_metrics": {},
        "risk_and_integrity_signals": [{
            "type": "inspection_feedback",
            "description": "吉林省委第五巡视组 2024-09 曾在榆树反馈巡视情况(见于官方要闻)，属常规巡视，无公开个别违纪结论。",
            "date": "2024-09",
            "confidence": "plausible",
            "source_ids": ["S001"],
        }],
        "source_register": sources,
        "confidence_summary": {
            "identity": "confirmed" if person.get("birth") else "unverified",
            "current_role": person.get("confidence", "unverified"),
            "career_completeness": "partial" if is_core else "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "核心人物早期/中间段履历起止时间未公开标注(官网仅列现任与前职摘要)",
        },
        "open_questions": [
            {
                "priority": "critical",
                "question": f"{name}的完整任职履历(每段职务起止时间)",
                "why_it_matters": "关系网络时间线需要的精确起止信息",
                "suggested_queries": [f"{name} 简历", f"{name} 任前公示", f"{name} 任职经历"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "high",
                "question": "前任领导(吴威/林小明/高洪洲/金海)的去向与完整履历",
                "why_it_matters": "前任领导交接与跨区网络分析",
                "suggested_queries": ["榆树市 前任 市委书记 去向", "吴威 榆树", "林小明 榆树"],
                "last_attempted": AS_OF,
            },
            {
                "priority": "medium",
                "question": "榆树市跨县域干部交流的完整模式",
                "why_it_matters": "县域班子整体调任(长春市属)的人事关系图谱",
                "suggested_queries": ["榆树 农安 干部交流", "榆树 长春 县市干部 调任"],
                "last_attempted": AS_OF,
            },
        ],
    }

    job_for_name = person.get("current_post", "").split("、")[0]
    fname = f"{TODAY}-吉林省-长春市-{job_for_name}-{name}.json"
    fpath = PJSON_DIR / fname
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"  Person JSON: {fpath.name}")


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
    core_ids = {1, 2, 10, 3, 30, 40, 50}
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())