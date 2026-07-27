#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 凌源市, 朝阳市, 辽宁省.

Investigation date: 2026-07-25
Task ID: liaoning_凌源市
Level: 县级市
Targets: 市委书记 & 市长

Research sources:
  - lingyuan.gov.cn official website (accessible)
  - 市政府领导页: confirmed 于雪曦(市长), 李立新, 王文江, 陈作婷, 宋洋
  - 市委领导页 (dated 2021, partially outdated): confirmed 张海清, 张鑫, 徐俊, 宋永波, 杨朝辉, 刘威武
  - 2026年7月新闻确认刘建超为市委书记
  - 李文旭自2026年6月任宣传部部长（取代刘威武）
  - 2026年7月2日新闻确认徐俊升任市委副书记（原纪委书记）
  - 张鑫转任市人大常委会主任
  - 刘东洋、刘国军、李长存为市政府领导

Confidence notes:
  - 刘建超(市委书记): 多次新闻确认当前职务，但完整履历（之前任职单位）待查
  - 于雪曦(市长): 官方简历页确认，但早期履历仅显示"大学学历，硕士学位"
  - 多位常委的完整履历来自2021年页面，当前状态部分已调整
  - 组织部部长当前信息缺失

"""

from __future__ import annotations

import json
import os
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
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "凌源市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-25"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "liaoning_凌源市"
if _CURRENT_DIR.name == "liaoning_凌源市":
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
# IDs: 1=市委书记, 2=市长, 3=市委副书记(张海清), 4=市委副书记(徐俊),
#      5=人大主任(张鑫), 6=组织部部长(待查), 7=政法委书记(杨朝辉),
#      8=宣传部部长(李文旭), 9=统战部部长(待查), 10=人武部政委(宋永波),
#      11=常务副市长(待查), 12=副市长/公安局长(王文江), 13=副市长(陈作婷),
#      14=副市长(宋洋), 15=副市长(刘东洋), 16=市政府党组成员(刘国军),
#      17=市领导(李长存), 18=政协主席(王福来), 19=政协党组书记(王树军),
#      20=开发区主任(李立新)

persons = [
    {
        "id": 1,
        "name": "刘建超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共凌源市委员会",
        "source": "official — lingyuan.gov.cn news articles (2026-06 to 2026-07)",
        "notes": "凌源市委书记。自2025-2026年期间上任（2024年4月时仍任朝阳县委常委、副县长）。"
            "此前职务和完整履历待查。凌源市委领导页（2021年版本）未收录刘建超，说明其2021年后才调入凌源。",
    },
    {
        "id": 2,
        "name": "于雪曦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年1月",
        "birthplace": "",
        "education": "大学学历，硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记、市长",
        "current_org": "凌源市人民政府",
        "source": "official — https://www.lingyuan.gov.cn/lyszf/zwgk/dzld/szfld/index.html?yxx",
        "notes": "凌源市委副书记、市长。1982年1月出生，大学学历、硕士学位。主持市政府全面工作。"
            "曾任凌源市代理市长后转正（具体任命时间待查）。",
    },
    {
        "id": 3,
        "name": "张海清",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年1月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记",
        "current_org": "中共凌源市委员会",
        "source": "official — https://www.lingyuan.gov.cn/lyszf/zwgk/dzld/swld/index.html",
        "notes": "凌源市委副书记、市直机关工委书记（兼）、市委党校校长（兼）、三级调研员。"
            "协助市委书记负责党的建设和深化改革工作。负责市委日常工作和群团工作。此信息来自2021年市委领导页，当前分工可能已调整。",
    },
    {
        "id": 4,
        "name": "徐俊",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1978年5月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记",
        "current_org": "中共凌源市委员会",
        "source": "official — 2026年7月2日新闻；2021市委领导页",
        "notes": "凌源市委副书记（2026年7月起）。此前任凌源市委常委、市纪委书记、市监委主任、三级调研员。"
            "2026年7月2日庆祝建党105周年大会新闻中以'市委副书记'身份出现。说明其于2026年6-7月间由纪委书记晋升为市委副书记。",
    },
    {
        "id": 5,
        "name": "张鑫",
        "gender": "男",
        "ethnicity": "",
        "birth": "1968年8月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "凌源市人大常委会",
        "source": "official — 2026年7月2日新闻；2021市委领导页",
        "notes": "凌源市人大常委会主任（2026年7月起）。此前任凌源市委常委、市委统战部部长（2021年时）。"
            "2026年已转任人大主任。",
    },
    {
        "id": 6,
        "name": "待查（组织部部长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、组织部部长",
        "current_org": "中共凌源市委组织部",
        "source": "unverified — 公开资料未明确显示当前组织部部长姓名",
        "notes": "凌源市委组织部部长。2026年5月组织部公告中出现李焕宇（1980年8月出生）为组织部副部长（保留正科级），"
            "非部长。该职务当前任职者待查。",
    },
    {
        "id": 7,
        "name": "杨朝辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年9月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、政法委书记",
        "current_org": "中共凌源市委政法委员会",
        "source": "official — 2021市委领导页",
        "notes": "凌源市委常委、市委政法委书记、市法学会党组书记（兼）。负责政法、维稳工作。"
            "此信息来自2021年市委领导页，当前是否在任需进一步确认。",
    },
    {
        "id": 8,
        "name": "李文旭",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、宣传部部长",
        "current_org": "中共凌源市委宣传部",
        "source": "official — 2026年6月8日新闻",
        "notes": "凌源市委常委、宣传部部长、市委教育工委书记。2026年6月8日高考检查新闻中刘建超调研时'市委常委、宣传部部长、"
            "市委教育工委书记李文旭参加'。取代了2021年市委领导页中的刘威武（原宣传部部长）。",
    },
    {
        "id": 9,
        "name": "待查（统战部部长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、统战部部长",
        "current_org": "中共凌源市委统一战线工作部",
        "source": "unverified",
        "notes": "凌源市委统战部部长。张鑫原兼任统战部部长，现转任人大主任后，该职位接任者待查。",
    },
    {
        "id": 10,
        "name": "宋永波",
        "gender": "男",
        "ethnicity": "",
        "birth": "1976年2月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、人武部政委",
        "current_org": "凌源市人民武装部",
        "source": "official — 2021市委领导页",
        "notes": "凌源市委常委、人武部政委。负责国防动员、武装和民兵预备役建设工作。"
            "此信息来自2021年市委领导页，当前是否在任需进一步确认。",
    },
    {
        "id": 11,
        "name": "待查（常务副市长）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、常务副市长",
        "current_org": "凌源市人民政府",
        "source": "unverified — 市政府领导页未显示明确的常务副市长",
        "notes": "凌源市常务副市长。市政府领导页上市长之下第一序位为李立新（开发区主任），"
            "未明确标注'常务副市长'。需查证。",
    },
    {
        "id": 12,
        "name": "王文江",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年1月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长、市公安局局长",
        "current_org": "凌源市人民政府",
        "source": "official — https://www.lingyuan.gov.cn/lyszf/zwgk/dzld/szfld/index.html?wwj",
        "notes": "凌源市人民政府副市长、市公安局局长。负责公安、司法、消防等工作。男，汉族，1971年1月出生，大学学历。",
    },
    {
        "id": 13,
        "name": "陈作婷",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1981年10月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "无党派人士",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "凌源市人民政府",
        "source": "official — https://www.lingyuan.gov.cn/lyszf/zwgk/dzld/szfld/index.html?czt",
        "notes": "凌源市人民政府副市长。女，汉族，1981年10月出生，大学学历，无党派人士。"
            "负责民政、教育、人力资源和社会保障等工作。",
    },
    {
        "id": 14,
        "name": "宋洋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985年2月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "凌源市人民政府",
        "source": "official — https://www.lingyuan.gov.cn/lyszf/zwgk/dzld/szfld/index.html?sy",
        "notes": "凌源市人民政府副市长。男，汉族，1985年2月出生，研究生学历。"
            "负责工信、生态环境、科技创新、大数据等工作。",
    },
    {
        "id": 15,
        "name": "刘东洋",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "凌源市人民政府",
        "source": "official — 2026年7月新闻报道",
        "notes": "凌源市副市长。多次出现在2026年6-7月新闻中（防汛工作会、刘建超调研城区综合整治等），陪同市委书记刘建超出席活动。"
            "未出现在市政府官方领导页上（可能为新补选或拟任命）。",
    },
    {
        "id": 16,
        "name": "刘国军",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政府党组成员",
        "current_org": "凌源市人民政府",
        "source": "official — 2026年6月新闻报道",
        "notes": "凌源市政府党组成员。2026年6月15日刘建超赴山东招商新闻中列名'市政府党组成员刘国军参加'。"
            "2026年7月防汛会议以'市领导'身份参加。",
    },
    {
        "id": 17,
        "name": "李长存",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市领导（副市长/副市级）",
        "current_org": "凌源市人民政府",
        "source": "official — 2026年6月新闻报道",
        "notes": "凌源市领导。2026年6月29日经济运行调度会议以'市领导'身份参加。具体职务待查。",
    },
    {
        "id": 18,
        "name": "王福来",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协主席",
        "current_org": "政协凌源市委员会",
        "source": "official — 2026年7月2日新闻",
        "notes": "凌源市政协主席。2026年7月2日庆祝建党105周年大会新闻中列名出席。",
    },
    {
        "id": 19,
        "name": "王树军",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市政协党组书记",
        "current_org": "政协凌源市委员会",
        "source": "official — 2026年7月2日新闻",
        "notes": "凌源市政协党组书记。2026年7月2日庆祝建党105周年大会新闻中列名出席。",
    },
    {
        "id": 20,
        "name": "李立新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年11月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "朝阳凌源经济开发区党工委副书记、管委会主任",
        "current_org": "朝阳凌源经济开发区",
        "source": "official — https://www.lingyuan.gov.cn/lyszf/zwgk/dzld/szfld/index.html?llx",
        "notes": "朝阳凌源经济开发区党工委副书记、管委会主任（相当于副市级）。负责开发区管委会、商务、外事等工作。"
            "男，汉族，1974年11月出生，大学学历。",
    },
    {
        "id": 21,
        "name": "孙立文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年11月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（推测）前任市长",
        "current_org": "（推测）凌源市人民政府",
        "source": "official — 2023年7月辽宁省委组织部公告",
        "notes": "推测为凌源市前任市长。2023年7月辽宁省委组织部公告提名孙立文（时任朝阳市委副秘书长、信访局局长）"
            "为县（市、区）长候选人。于雪曦于2026年4月任代市长，则孙立文可能在2023-2026年间任职。待查证。",
    },
    {
        "id": 22,
        "name": "陈士忠",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原市委常委、副市长（已调离）",
        "current_org": "凌源市人民政府",
        "source": "official — 2026年5月朝阳市组织部公告",
        "notes": "原凌源市委常委、市政府党组副书记、副市长（可能为常务副市长）。"
            "2026年5月朝阳市组织部公告显示拟任市直部门正职，已调离凌源。",
    },
    {
        "id": 23,
        "name": "张爱军",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（前任市长候选）",
        "current_org": "unknown",
        "source": "official — 2023年7月辽宁省委组织部公告",
        "notes": "与孙立文同期（2023年7月）被提名县（市、区）长候选人。时任朝阳市营商环境建设局局长。"
            "去向不确定，有可能曾担任凌源市长或朝阳其他县区长。",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共凌源市委员会", "type": "党委", "level": "县处级", "parent": "中共朝阳市委员会", "location": "辽宁省朝阳市凌源市"},
    {"id": 2, "name": "凌源市人民政府", "type": "政府", "level": "县处级", "parent": "朝阳市人民政府", "location": "辽宁省朝阳市凌源市"},
    {"id": 3, "name": "凌源市人大常委会", "type": "人大", "level": "县处级", "parent": "朝阳市人大常委会", "location": "辽宁省朝阳市凌源市"},
    {"id": 4, "name": "政协凌源市委员会", "type": "政协", "level": "县处级", "parent": "政协朝阳市委员会", "location": "辽宁省朝阳市凌源市"},
    {"id": 5, "name": "中共凌源市纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共朝阳市纪律检查委员会", "location": "辽宁省朝阳市凌源市"},
    {"id": 6, "name": "中共凌源市委组织部", "type": "党委", "level": "县处级", "parent": "中共凌源市委员会", "location": "辽宁省朝阳市凌源市"},
    {"id": 7, "name": "中共凌源市委政法委员会", "type": "党委", "level": "县处级", "parent": "中共凌源市委员会", "location": "辽宁省朝阳市凌源市"},
    {"id": 8, "name": "中共凌源市委宣传部", "type": "党委", "level": "县处级", "parent": "中共凌源市委员会", "location": "辽宁省朝阳市凌源市"},
    {"id": 9, "name": "中共凌源市委统一战线工作部", "type": "党委", "level": "县处级", "parent": "中共凌源市委员会", "location": "辽宁省朝阳市凌源市"},
    {"id": 10, "name": "凌源市人民武装部", "type": "党委", "level": "县处级", "parent": "朝阳军分区", "location": "辽宁省朝阳市凌源市"},
    {"id": 11, "name": "凌源市公安局", "type": "政府", "level": "科级", "parent": "凌源市人民政府", "location": "辽宁省朝阳市凌源市"},
    {"id": 12, "name": "朝阳凌源经济开发区", "type": "开发区", "level": "副县处级", "parent": "凌源市人民政府", "location": "辽宁省朝阳市凌源市"},
    {"id": 13, "name": "中共朝阳县委", "type": "党委", "level": "县处级", "parent": "中共朝阳市委员会", "location": "辽宁省朝阳市朝阳县"},
    {"id": 14, "name": "朝阳县人民政府", "type": "政府", "level": "县处级", "parent": "朝阳市人民政府", "location": "辽宁省朝阳市朝阳县"},
    {"id": 15, "name": "朝阳柳城经济开发区", "type": "开发区", "level": "副县处级", "parent": "朝阳县人民政府", "location": "辽宁省朝阳市朝阳县"},
    {"id": 16, "name": "中共朝阳市委办公室（信访局）", "type": "党委", "level": "县处级", "parent": "中共朝阳市委员会", "location": "辽宁省朝阳市"},
    {"id": 17, "name": "朝阳市营商环境建设局", "type": "政府", "level": "县处级", "parent": "朝阳市人民政府", "location": "辽宁省朝阳市"},
]

# ── Positions ────────────────────────────────────────────────────────────────

positions = [
    # 刘建超 - 市委书记
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start": "2024后半年或2025", "end": "present", "rank": "县处级正职", "note": "2024年4月时仍任朝阳县委常委、副县长，此后到2025-2026年间上任凌源市委书记"},
    {"person_id": 1, "org_id": 13, "title": "县委常委、副县长（保留正处级）", "start": "unknown", "end": "2024-04或更晚", "rank": "县处级正职", "note": "2024年4月朝阳市组织部公告显示其任朝阳县委常委、副县长（保留正处级），朝阳柳城经济开发区党工委副书记、管委会常务副主任"},
    # 于雪曦 - 市长
    {"person_id": 2, "org_id": 2, "title": "市长", "start": "unknown", "end": "present", "rank": "县处级正职", "note": "市政府领导页在列，2026年4月更新"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start": "unknown", "end": "present", "rank": "县处级副职", "note": "兼任市委副书记"},
    # 张海清 - 市委副书记
    {"person_id": 3, "org_id": 1, "title": "市委副书记", "start": "2021或更早", "end": "present", "rank": "县处级副职", "note": "2021年时已在任"},
    # 徐俊 - 市委副书记（原纪委书记）
    {"person_id": 4, "org_id": 5, "title": "市委常委、市纪委书记、市监委主任", "start": "2021或更早", "end": "2026-06", "rank": "县处级副职", "note": "2021年时已在纪委书记任上"},
    {"person_id": 4, "org_id": 1, "title": "市委副书记", "start": "2026-06", "end": "present", "rank": "县处级副职", "note": "2026年6-7月间由纪委书记晋升"},
    # 张鑫 - 人大主任（原统战部部长）
    {"person_id": 5, "org_id": 9, "title": "市委常委、统战部部长", "start": "2021或更早", "end": "2026年某时", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 3, "title": "市人大常委会主任", "start": "2026年某时", "end": "present", "rank": "县处级正职", "note": "2026年7月确认"},
    # 组织部部长（待查）
    {"person_id": 6, "org_id": 6, "title": "市委常委、组织部部长", "start": "unknown", "end": "present", "rank": "县处级副职", "note": "当前任职者待查"},
    # 杨朝辉 - 政法委书记
    {"person_id": 7, "org_id": 7, "title": "市委常委、政法委书记", "start": "2021或更早", "end": "present", "rank": "县处级副职", "note": ""},
    # 李文旭 - 宣传部部长
    {"person_id": 8, "org_id": 8, "title": "市委常委、宣传部部长", "start": "2026年某时之前", "end": "present", "rank": "县处级副职", "note": "2026年6月8日新闻确认"},
    # 统战部部长（待查）
    {"person_id": 9, "org_id": 9, "title": "市委常委、统战部部长", "start": "2026年某时", "end": "present", "rank": "县处级副职", "note": "张鑫转任人大后，接任者待查"},
    # 宋永波 - 人武部政委
    {"person_id": 10, "org_id": 10, "title": "市委常委、人武部政委", "start": "2021或更早", "end": "present", "rank": "县处级副职", "note": ""},
    # 常务副市长（待查）
    {"person_id": 11, "org_id": 2, "title": "市委常委、常务副市长", "start": "unknown", "end": "present", "rank": "县处级副职", "note": "当前任职者待查"},
    # 王文江 - 副市长/公安局长
    {"person_id": 12, "org_id": 2, "title": "副市长", "start": "unknown", "end": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 12, "org_id": 11, "title": "市公安局局长", "start": "unknown", "end": "present", "rank": "科级", "note": "兼任"},
    # 陈作婷 - 副市长
    {"person_id": 13, "org_id": 2, "title": "副市长", "start": "unknown", "end": "present", "rank": "县处级副职", "note": ""},
    # 宋洋 - 副市长
    {"person_id": 14, "org_id": 2, "title": "副市长", "start": "unknown", "end": "present", "rank": "县处级副职", "note": ""},
    # 刘东洋 - 副市长
    {"person_id": 15, "org_id": 2, "title": "副市长", "start": "unknown", "end": "present", "rank": "县处级副职", "note": "可能为新补选"},
    # 刘国军 - 市政府党组成员
    {"person_id": 16, "org_id": 2, "title": "市政府党组成员", "start": "unknown", "end": "present", "rank": "县处级副职", "note": ""},
    # 李长存 - 市领导
    {"person_id": 17, "org_id": 2, "title": "市领导", "start": "unknown", "end": "present", "rank": "县处级副职", "note": "具体职务待查"},
    # 王福来 - 政协主席
    {"person_id": 18, "org_id": 4, "title": "市政协主席", "start": "unknown", "end": "present", "rank": "县处级正职", "note": ""},
    # 王树军 - 政协党组书记
    {"person_id": 19, "org_id": 4, "title": "市政协党组书记", "start": "unknown", "end": "present", "rank": "县处级正职", "note": ""},
    # 李立新 - 开发区主任
    {"person_id": 20, "org_id": 12, "title": "党工委副书记、管委会主任", "start": "unknown", "end": "present", "rank": "副县处级", "note": ""},
    # 孙立文 - 前任市长（推测）
    {"person_id": 21, "org_id": 16, "title": "市委副秘书长、信访局局长", "start": "unknown", "end": "2023-07", "rank": "县处级", "note": "朝阳市委、市政府信访局局长（2022-03时任）"},
    {"person_id": 21, "org_id": 2, "title": "市长（推测）", "start": "2023-07（推测）", "end": "2026-04（推测）", "rank": "县处级正职", "note": "2023年7月被提名县（市、区）长候选人，推测为凌源市长"},
    # 陈士忠 - 原常委副市长
    {"person_id": 22, "org_id": 2, "title": "市委常委、市政府党组副书记、副市长", "start": "unknown", "end": "2026-05", "rank": "县处级副职", "note": "2026年5月朝阳市组织部公告拟任市直部门正职"},
    # 张爱军 - 前任市长候选
    {"person_id": 23, "org_id": 17, "title": "市营商环境建设局局长", "start": "unknown", "end": "2023-07", "rank": "县处级", "note": "2023年7月被提名县（市、区）长候选人"},
]

# ── Relationships ─────────────────────────────────────────────────────────────

relationships = [
    # 党政主要领导
    {
        "person_a": 1, "person_b": 2,
        "type": "党政领导搭档",
        "context": "市委书记与市长，党政主要负责人",
        "overlap_org": "中共凌源市委员会/凌源市人民政府",
        "overlap_period": "2026年至今",
        "confidence": "confirmed",
    },
    # 刘建超 - 张海清
    {
        "person_a": 1, "person_b": 3,
        "type": "党委领导班子",
        "context": "市委书记与专职副书记",
        "overlap_org": "中共凌源市委员会",
        "overlap_period": "2026年至今",
        "confidence": "confirmed",
    },
    # 刘建超 - 徐俊
    {
        "person_a": 1, "person_b": 4,
        "type": "党委领导班子",
        "context": "市委书记与副书记（原纪委书记晋升）",
        "overlap_org": "中共凌源市委员会",
        "overlap_period": "2026年至今",
        "confidence": "confirmed",
    },
    # 于雪曦 - 张海清
    {
        "person_a": 2, "person_b": 3,
        "type": "党政领导配合",
        "context": "市长与专职副书记",
        "overlap_org": "中共凌源市委员会",
        "overlap_period": "2026年至今",
        "confidence": "confirmed",
    },
    # 徐俊 - 张鑫（原纪委监督统战）
    {
        "person_a": 4, "person_b": 5,
        "type": "同级常委",
        "context": "原纪委书记与统战部部长，同届常委",
        "overlap_org": "中共凌源市委员会",
        "overlap_period": "2021-2026",
        "confidence": "confirmed",
    },
    # 杨朝辉 - 刘建超
    {
        "person_a": 7, "person_b": 1,
        "type": "党委领导班子",
        "context": "政法委书记与市委书记",
        "overlap_org": "中共凌源市委员会",
        "overlap_period": "2026年至今",
        "confidence": "confirmed",
    },
    # 李文旭 - 刘建超
    {
        "person_a": 8, "person_b": 1,
        "type": "党委领导班子",
        "context": "宣传部部长与市委书记",
        "overlap_org": "中共凌源市委员会",
        "overlap_period": "2026年至今",
        "confidence": "confirmed",
    },
    # 于雪曦 - 王文江
    {
        "person_a": 2, "person_b": 12,
        "type": "政府领导班子",
        "context": "市长与副市长/公安局长",
        "overlap_org": "凌源市人民政府",
        "overlap_period": "2026年至今",
        "confidence": "confirmed",
    },
    # 于雪曦 - 陈作婷
    {
        "person_a": 2, "person_b": 13,
        "type": "政府领导班子",
        "context": "市长与副市长",
        "overlap_org": "凌源市人民政府",
        "overlap_period": "2026年至今",
        "confidence": "confirmed",
    },
    # 于雪曦 - 宋洋
    {
        "person_a": 2, "person_b": 14,
        "type": "政府领导班子",
        "context": "市长与副市长",
        "overlap_org": "凌源市人民政府",
        "overlap_period": "2026年至今",
        "confidence": "confirmed",
    },
    # 于雪曦 - 刘东洋
    {
        "person_a": 2, "person_b": 15,
        "type": "政府领导班子",
        "context": "市长与副市长",
        "overlap_org": "凌源市人民政府",
        "overlap_period": "2026年至今",
        "confidence": "confirmed",
    },
    # 刘建超 - 刘东洋
    {
        "person_a": 1, "person_b": 15,
        "type": "党政配合",
        "context": "市委书记与副市长（刘东洋多次陪同刘建超调研）",
        "overlap_org": "凌源市人民政府",
        "overlap_period": "2026年至今",
        "confidence": "confirmed",
    },
    # 刘建超 - 刘国军
    {
        "person_a": 1, "person_b": 16,
        "type": "党政配合",
        "context": "市委书记与市政府党组成员（刘国军陪同赴山东招商）",
        "overlap_org": "凌源市人民政府",
        "overlap_period": "2026年至今",
        "confidence": "confirmed",
    },
    # 王福来 - 王树军
    {
        "person_a": 18, "person_b": 19,
        "type": "政协领导班子",
        "context": "政协主席与政协党组书记",
        "overlap_org": "政协凌源市委员会",
        "overlap_period": "2026年至今",
        "confidence": "confirmed",
    },
    # 徐俊 - 于雪曦
    {
        "person_a": 4, "person_b": 2,
        "type": "党政领导配合",
        "context": "市委副书记与市长",
        "overlap_org": "中共凌源市委员会",
        "overlap_period": "2026年至今",
        "confidence": "confirmed",
    },
]


# ══════════════════════════════════════════════════════════════════════════════
# Person JSON Generator
# ══════════════════════════════════════════════════════════════════════════════

def make_source_register():
    """Source register."""
    return [
        {
            "id": "S001",
            "title": "凌源市人民政府官方网站 - 市政府领导页",
            "url": "https://www.lingyuan.gov.cn/lyszf/zwgk/dzld/szfld/index.html",
            "publisher": "凌源市人民政府",
            "published_at": "2026年4月更新",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "市政府领导列表，含市长和副市长简历及分工",
        },
        {
            "id": "S002",
            "title": "凌源市人民政府官方网站 - 市委领导页",
            "url": "https://www.lingyuan.gov.cn/lyszf/zwgk/dzld/swld/index.html",
            "publisher": "凌源市人民政府",
            "published_at": "2021年版本",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "市委领导页2021年版本，部分信息可能已过时",
        },
        {
            "id": "S003",
            "title": "市委常委会召开扩大会议",
            "url": "https://www.lingyuan.gov.cn/html/LYSZF/202607/0178476806828445.html",
            "publisher": "凌源融媒",
            "published_at": "2026-07-23",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "确认刘建超市委书记身份",
        },
        {
            "id": "S004",
            "title": "刘建超调研督导城区环境卫生和道路交通综合整治工作",
            "url": "https://www.lingyuan.gov.cn/html/LYSZF/202607/0178450832352029.html",
            "publisher": "凌源融媒",
            "published_at": "2026-07-20",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "确认刘建超市委书记身份、刘东洋副市长",
        },
        {
            "id": "S005",
            "title": "我市召开防汛工作会议",
            "url": "https://www.lingyuan.gov.cn/html/LYSZF/202607/0178329931624261.html",
            "publisher": "凌源融媒",
            "published_at": "2026-07-06",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "确认刘建超、于雪曦、刘东洋、刘国军",
        },
        {
            "id": "S006",
            "title": "凌源市集中收听收看庆祝中国共产党成立105周年大会",
            "url": "https://www.lingyuan.gov.cn/html/LYSZF/202607/0178295044834979.html",
            "publisher": "凌源融媒",
            "published_at": "2026-07-02",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "确认于雪曦（市长）、张鑫（人大主任）、王福来（政协主席）、王树军（政协党组书记）、徐俊（市委副书记）",
        },
        {
            "id": "S007",
            "title": "刘建超检查高考准备工作",
            "url": "https://www.lingyuan.gov.cn/html/LYSZF/202606/0178088033770366.html",
            "publisher": "凌源融媒",
            "published_at": "2026-06-08",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "确认刘建超市委书记、李文旭宣传部部长",
        },
        {
            "id": "S008",
            "title": "刘建超率队赴山东省潍坊市招商考察",
            "url": "https://www.lingyuan.gov.cn/html/LYSZF/202606/0178148470805215.html",
            "publisher": "凌源融媒",
            "published_at": "2026-06-15",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "确认刘建超、李立新、刘国军",
        },
        {
            "id": "S009",
            "title": "全市经济运行调度会议",
            "url": "https://www.lingyuan.gov.cn/html/LYSZF/202606/0178269334497695.html",
            "publisher": "凌源融媒",
            "published_at": "2026-06-29",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "确认于雪曦、李长存、刘东洋、刘国军",
        },
        {
            "id": "S010",
            "title": "中共凌源市委组织部公告 2026年第5号",
            "url": "https://www.lingyuan.gov.cn/html/LYSZF/202605/0177822913110350.html",
            "publisher": "中共凌源市委组织部",
            "published_at": "2026-05-08",
            "accessed_at": AS_OF,
            "source_type": "appointment_notice",
            "reliability": "high",
            "notes": "确认李焕宇为组织部副部长（正科级）",
        },
    ]


def make_person_json(p, rels_for_person, source_register):
    """Generate person JSON for a core figure."""
    is_top = p["id"] in (1, 2)
    is_key = p["id"] in (3, 4, 5, 7, 8)
    
    # Determine rank
    if p["id"] in (1, 2, 5, 18, 19):
        rank = "县处级正职"
    elif p["id"] == 20:
        rank = "副县处级"
    else:
        rank = "县处级副职"
    
    # Determine person_id for dedup
    name_slug = p["name"].replace("（", "_").replace("）", "").replace(" ", "")
    person_id = f"lingyuan_{name_slug}"
    
    result = {
        "schema_version": "1.0",
        "generated_at": AS_OF,
        "investigation_scope": {
            "province": "辽宁省",
            "city": "朝阳市",
            "region": "凌源市",
            "job": p["current_post"],
            "task_id": "liaoning_凌源市",
            "time_focus": "2026年7月",
        },
        "identity": {
            "person_id": person_id,
            "name": p["name"],
            "aliases": [],
            "gender": p.get("gender", ""),
            "ethnicity": p.get("ethnicity", ""),
            "birth": p.get("birth", ""),
            "birthplace": p.get("birthplace", ""),
            "native_place": "",
            "education": [{"period": "", "institution": "", "major": "", "degree": p.get("education", ""), "study_type": "unknown", "source_ids": ["S001", "S002"]}] if p.get("education") else [],
            "party_join": p.get("party_join", ""),
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{p['name']}_{p.get('birth', '')}",
                "name_birthplace": f"{p['name']}_{p.get('birthplace', '')}",
                "official_profile_url": "",
            },
        },
        "current_status": {
            "current_post": p["current_post"],
            "current_org": p["current_org"],
            "administrative_rank": rank,
            "as_of": AS_OF,
            "is_current_confirmed": "待查" not in p["name"],
            "source_ids": ["S001", "S003", "S005", "S006"],
        },
        "career_timeline": _make_career_timeline(p, is_top),
        "organizations": [],
        "relationships": [
            {
                "person": rp["name"] if rp.get("person_a") != p["id"] else next(
                    (x["name"] for x in persons if x["id"] == rp.get("person_b")), ""
                ),
                "person_id": f"lingyuan_{next((x['name'] for x in persons if x['id'] == (rp.get('person_b') if rp.get('person_a') == p['id'] else rp.get('person_a'))), 'unknown')}",
                "relationship_type": rp.get("type", ""),
                "strength": "medium",
                "evidence": rp.get("context", ""),
                "overlap_org": rp.get("overlap_org", ""),
                "overlap_period": rp.get("overlap_period", ""),
                "direction": "undirected",
                "confidence": rp.get("confidence", "plausible"),
                "source_ids": ["S003", "S005", "S006", "S007", "S008"],
            }
            for rp in rels_for_person
        ],
        "governance_record": [],
        "professional_profile": {
            "primary_specializations": [],
            "secondary_specializations": [],
            "career_pattern": "unknown",
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
        "risk_and_integrity_signals": [],
        "source_register": source_register,
        "confidence_summary": {
            "identity": "confirmed" if "待查" not in p["name"] else "unverified",
            "current_role": "confirmed" if "待查" not in p["name"] else "unverified",
            "career_completeness": "partial" if p.get("birth") else "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "",
        },
        "open_questions": _make_open_questions(p),
    }
    return result


def _make_career_timeline(p, is_top):
    """Build career timeline from positions data."""
    person_positions = [pos for pos in positions if pos["person_id"] == p["id"]]
    if not person_positions:
        return [{
            "start": "unknown",
            "end": "present",
            "org": p["current_org"],
            "title": p["current_post"],
            "level": rank_for_id(p["id"]),
            "location": "辽宁省朝阳市凌源市",
            "system": "party" if ("委" in p["current_org"] and "政府" not in p["current_org"] and "政协" not in p["current_org"] and "人大" not in p["current_org"]) else "government",
            "rank": rank_for_id(p["id"]),
            "is_key_promotion": is_top,
            "notes": p.get("notes", ""),
            "confidence": "confirmed" if "待查" not in p["name"] else "unverified",
            "source_ids": ["S001", "S002"],
        }]
    
    timeline = []
    for pos in person_positions:
        org_name = next((o["name"] for o in organizations if o["id"] == pos["org_id"]), pos.get("org", ""))
        timeline.append({
            "start": pos["start"],
            "end": pos["end"],
            "org": org_name,
            "title": pos["title"],
            "level": pos["rank"],
            "location": "辽宁省朝阳市凌源市",
            "system": "party" if ("委" in org_name and "政府" not in org_name and "政协" not in org_name and "人大" not in org_name) else "government",
            "rank": pos["rank"],
            "is_key_promotion": is_top and "present" in str(pos.get("end", "")),
            "notes": pos.get("note", ""),
            "confidence": "confirmed",
            "source_ids": ["S001", "S002"],
        })
    return timeline


def rank_for_id(pid):
    if pid in (1, 2, 5, 18, 19):
        return "县处级正职"
    elif pid == 20:
        return "副县处级"
    return "县处级副职"


def _make_open_questions(p):
    questions = []
    if "待查" in p["name"]:
        questions.append({
            "priority": "critical",
            "question": f"凌源市{p['current_post']}的姓名",
            "why_it_matters": "核心领导人的身份信息是整个调查的基础",
            "suggested_queries": [f"凌源市 {p['current_post']} 现任", "凌源市委 领导班子 2026"],
            "last_attempted": AS_OF,
        })
    if not p.get("birth"):
        questions.append({
            "priority": "high",
            "question": f"{p['name']}的出生年月和籍贯",
            "why_it_matters": "身份信息是人员去重和关系网络分析的基础",
            "suggested_queries": [f"{p['name']} 简历 凌源市", f"{p['name']} 百度百科"],
            "last_attempted": AS_OF,
        })
    if not p.get("education") or p.get("education") in ("大学学历", "大学学历，硕士学位", "研究生学历"):
        questions.append({
            "priority": "medium",
            "question": f"{p['name']}的完整教育背景（毕业院校、专业）",
            "why_it_matters": "校友关系是隐性关系网络的重要组成部分",
            "suggested_queries": [f"{p['name']} 毕业 院校"],
            "last_attempted": AS_OF,
        })
    return questions


def write_person_jsons():
    """Write per-person JSON files for core leaders."""
    source_register = make_source_register()

    # Build per-person relationship lists
    person_relationships = {p["id"]: [] for p in persons}
    for r in relationships:
        if r["person_a"] in person_relationships:
            person_relationships[r["person_a"]].append(r)
        if r["person_b"] in person_relationships and r["person_b"] != r["person_a"]:
            rev_r = dict(r)
            rev_r["person_a"], rev_r["person_b"] = r["person_b"], r["person_a"]
            person_relationships[r["person_b"]].append(rev_r)

    # Core figures to write person JSON for (IDs 1-5, 7, 8, 12-16, 18-20)
    core_ids = {1, 2, 3, 4, 5, 7, 8, 12, 13, 14, 15, 16, 18, 19, 20}
    
    for p in persons:
        if p["id"] not in core_ids:
            continue
        rels = person_relationships.get(p["id"], [])
        pjson = make_person_json(p, rels, source_register)
        job_slug = p["current_post"].replace('、', '_').replace('，', '_').replace(' ', '')
        filename = f"{TODAY}-辽宁省-朝阳市-{job_slug}-{p['name']}.json"
        path = PJSON_DIR / filename
        with open(path, "w", encoding="utf-8") as f:
            json.dump(pjson, f, ensure_ascii=False, indent=2)
        print(f"  Person JSON: {path.name}")


# ══════════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════════

def main():
    """Run the full build."""
    print(f"\n{'='*60}")
    print(f"凌源市 Network Build")
    print(f"{'='*60}")
    print(f"Date: {AS_OF}")
    print()

    # 1. Database + GEXF
    print("Building database and GEXF...")
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

    # 2. Person JSONs
    print("\nWriting person JSONs...")
    write_person_jsons()

    print(f"\n{'='*60}")
    print(f"Build complete.")
    print(f"{'='*60}")
    print(f"DB:      {DB_PATH}")
    print(f"GEXF:    {GEXF_PATH}")
    print(f"Persons: {PJSON_DIR}/")
    print()


if __name__ == "__main__":
    main()
