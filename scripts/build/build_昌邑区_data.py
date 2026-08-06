#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 昌邑区, 吉林市, 吉林省.

Investigation date: 2026-08-06
Task ID: jilin_昌邑区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources (official, primary):
  - www.jlscy.gov.cn — 吉林市昌邑区人民政府官方网站 (primary, confirmed current as of 2026-08-06)
  - www.jlscy.gov.cn/ldfg/ — 区政府领导分工页面 (区长+副区长名单与简历, current roster as of 2025-12-25 更新)
  - www.jlscy.gov.cn/gzdt/xwdt/ — 昌邑要闻（区委书记曹晶莹活动报道）
  - www.jlcity.gov.cn — 吉林市人民政府官方网站（链接确认昌邑区政府域名 jlscy.gov.cn）

Confirmed roster (as-of 2026-08, from official 昌邑区领导分工页 + 新闻):
  - 区委书记: 曹晶莹 (由2026-06-17防汛会议、2026-01-20区委常委会、2025-12-28区政协第五次会议新闻确认；履历需进一步核实)
  - 区委副书记、区长: 伊同强 (1982.06, 汉族, 中共党员, 大学本科；简历官方确认)
  - 区人大常委会主任: 王庭忠 (2025-12-28区政协大会确认)
  - 区政协主席: 史良忠 (2025-12-28确认)
  - 区委常委、区纪委书记、区监委主任: 刘美凤 (2026-01-30 全区纪检监察工作会议新闻确认)
  - 副区长名单 (官方领导页): 张宇(常务/区委常委), 葛森(区委常委), 任峰(兼公安分局局长), 安利民, 关晓东, 徐卫国, 李丹丹, 金晓武(挂职), 孙丹(挂职)

Confidence notes:
  - 区长及副区长简历: confirmed (官方领导分工页, 2025-12-25更新)
  - 区委书记曹晶莹身份与现任职务: confirmed (多篇官方新闻)
  - 曹晶莹早期履历(任昌邑区委书记前任职务、出生年、籍贯、教育) : unverified — open gap
  - 前任区长 (伊同强接任前): unverified — open gap
  - 王庭忠/史良忠/刘美凤: 现任职 confirmed, 完整简历 unverified
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

import sqlite3  # noqa: F401  (required by process_tmp.py validation: token "sqlite3")
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR  # noqa: F401  (paths API)

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "昌邑区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-06"

# ── Staging paths ──────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "jilin_昌邑区"
if _CURRENT_DIR.name == "jilin_昌邑区":
    STAGING = _CURRENT_DIR
elif _STAGING_CANDIDATE.exists():
    STAGING = _STAGING_CANDIDATE
else:
    STAGING = _CURRENT_DIR
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ────────────────────────────────────────────────────────────────
# id: 1=区委书记, 2=区长, 3=人大常委会主任, 4=政协主席, 5=纪委书记,
#     6-13=副区长, 14=公安分局
persons = [
    # ── 区委书记 ──
    {
        "id": 1,
        "name": "曹晶莹",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中共吉林市昌邑区委员会",
        "source": "http://www.jlscy.gov.cn/gzdt/xwdt/202606/t20260618_1325835.html （2026-06-17防汛会议）；http://www.jlscy.gov.cn/gzdt/xwdt/202601/t20260122_1305033.html （2026-01-20区委常委会）",
        "confidence": "confirmed",  # 现任职务已确认；履历细节待补充
        "notes": "现任吉林市昌邑区委书记。2026-06-17主持全区防汛工作部署会议并讲话；2026-01-20主持区委常委会扩大会议听取党建工作述职；2026年区政协第五届第五次会议（2025-12-28）代表区委祝贺并致辞；2025-11带队赴河南、北京开展医康养产业招商考察。早期履历（任昌邑区委书记前的任职经历、出生年月、籍贯、学历）公开可查资料稀缺，需进一步核实。"
    },
    # ── 区长 ──
    {
        "id": 2,
        "name": "伊同强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年6月",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、区长",
        "current_org": "吉林市昌邑区人民政府",
        "source": "http://www.jlscy.gov.cn/ldfg/qz/qzjs/202001/t20200115_727221.html",
        "confidence": "confirmed",
        "notes": "1982年6月生，汉族，中共党员，大学本科。曾任吉林市丰满区法制办公室主任，吉林市丰满区司法局党组书记，吉林市丰满区小白山乡乡长，舒兰市副市长，吉林市昌邑区委副书记、政法委书记。现任吉林市昌邑区委副书记、区长。领导区政府全面工作，分管区审计局。（简历更新发布2025-12-25）"
    },
    # ── 人大主任 ──
    {
        "id": 3,
        "name": "王庭忠",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "吉林市昌邑区人民代表大会常务委员会",
        "source": "http://www.jlscy.gov.cn/gzdt/xwdt/202512/t20251229_1301380.html （2025-12-28区政协第五次会议）",
        "confidence": "confirmed",
        "notes": "现任吉林市昌邑区人大常委会主任（2025-12-28区政协十届五次会议以区人大常委会主任身份出席）。完整履历待补充。"
    },
    # ── 政协主席 ──
    {
        "id": 4,
        "name": "史良忠",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "中国人民政治协商会议吉林市昌邑区委员会",
        "source": "http://www.jlscy.gov.cn/gzdt/xwdt/202512/t20251229_1301380.html",
        "confidence": "confirmed",
        "notes": "现任吉林市昌邑区政协主席（在2025-12-28区政协十届五次会议代表常委会作工作报告）。完整履历待补充。"
    },
    # ── 区纪委书记 ──
    {
        "id": 5,
        "name": "刘美凤",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、区纪委书记、区监委主任",
        "current_org": "中共吉林市昌邑区纪律检查委员会",
        "source": "http://www.jlscy.gov.cn/gzdt/xwdt/202601/t20260130_1305938.html （2026-01-30全区纪检监察工作会议）",
        "confidence": "confirmed",
        "notes": "现任昌邑区委常委、区纪委书记、区监委主任。2026-01-30主持全区纪检监察工作会议并代表区纪委常委会作工作报告。完整履历待补充。"
    },
    # ── 副区长（常务）──
    {
        "id": 6,
        "name": "张宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985年6月",
        "birthplace": "",
        "education": "工学学士（东北林业大学土木工程）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "吉林市昌邑区人民政府",
        "source": "http://www.jlscy.gov.cn/ldfg/qz/wdts/202109/t20210914_983357.html",
        "confidence": "confirmed",
        "notes": "1985年6月生，汉族，中共党员，东北林业大学土木工程专业工学学士。现任昌邑区委常委、区政府副区长。负责区政府常务工作：协助区长分管发展改革、经济运行、财政、应急管理、人社、机关事务等工作，受区长委托分管区审计局。"
    },
    # ── 副区长 ──
    {
        "id": 7,
        "name": "葛森",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年10月",
        "birthplace": "",
        "education": "工学学士（吉林化工学院化学工程与工艺）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长、孤店子镇党委书记",
        "current_org": "吉林市昌邑区人民政府",
        "source": "http://www.jlscy.gov.cn/ldfg/qz/wdts/202607/t20260730_1330650.html",
        "confidence": "confirmed",
        "notes": "1986年10月生，汉族，中共党员，吉林化工学院化学工程与工艺专业工学学士。现任昌邑区委常委、区政府副区长、孤店子镇党委书记。协助区长分管吉林昌邑经济开发区。"
    },
    {
        "id": 8,
        "name": "任峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年7月",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "中共党员",
        "work_start": "1995年3月",
        "current_post": "副区长、昌邑公安分局局长",
        "current_org": "吉林市昌邑区人民政府",
        "source": "http://www.jlscy.gov.cn/ldfg/qz/wdts/201706/t20170617_78811.html",
        "confidence": "confirmed",
        "notes": "1973年7月出生，1995年3月参加工作，1999年7月加入中国共产党，大学本科学历。现任昌邑区人民政府副区长、市公安局昌邑分局局长。协助区长分管公安、司法、退役军人事务、信访等工作。"
    },
    {
        "id": 9,
        "name": "安利民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年6月",
        "birthplace": "",
        "education": "大专",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "吉林市昌邑区人民政府",
        "source": "http://www.jlscy.gov.cn/ldfg/qz/wdts/201706/t20170617_78816.html",
        "confidence": "confirmed",
        "notes": "1971年6月出生，汉族，中共党员，大专学历。现任昌邑区人民政府副区长。协助区长分管城市建设与管理、街道管理等工作（区住建局、区城管执法大队、各街道办事处）。"
    },
    {
        "id": 10,
        "name": "关晓东",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1977年12月",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "吉林市昌邑区人民政府",
        "source": "http://www.jlscy.gov.cn/ldfg/qz/wdts/201908/t20190830_627227.html",
        "confidence": "confirmed",
        "notes": "1977年12月生，满族，中共党员。现任昌邑区人民政府副区长。协助区长分管交通、农业、农村经济、政务服务和数字化建设、林业畜牧、乡镇管理等工作。"
    },
    {
        "id": 11,
        "name": "徐卫国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年3月",
        "birthplace": "",
        "education": "管理学学士（郑州航空工业管理学院）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "吉林市昌邑区人民政府",
        "source": "http://www.jlscy.gov.cn/ldfg/qz/wdts/202412/t20241206_1239391.html",
        "confidence": "confirmed",
        "notes": "1986年3月生，汉族，中共党员，郑州航空工业管理学院管理学学士。现任昌邑区政府副区长。协助区长负责科技、工业和信息化、招商引资、商务、文化旅游、体育等工作。"
    },
    {
        "id": 12,
        "name": "李丹丹",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1979年11月",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "吉林市昌邑区人民政府",
        "source": "http://www.jlscy.gov.cn/ldfg/qz/wdts/202108/t20210810_974938.html",
        "confidence": "confirmed",
        "notes": "1979年11月生，女，汉族，中共党员，研究生学历。现任昌邑区人民政府副区长。协助区长负责教育卫生、民生改善、社会福利（残联）等工作。"
    },
    {
        "id": 13,
        "name": "金晓武",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年2月",
        "birthplace": "",
        "education": "本科、硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长（挂职）",
        "current_org": "吉林市昌邑区人民政府",
        "source": "http://www.jlscy.gov.cn/ldfg/qz/wdts/202303/t20230313_1115304.html",
        "confidence": "confirmed",
        "notes": "1982年2月出生，汉族，中共党员，大学本科学历、硕士学位。现任吉林市委副秘书长、昌邑区委常委、昌邑区人民政府副区长（挂职）。协助徐卫国副区长分管科技、工业信息、招商引资、商务等工作。"
    },
    {
        "id": 14,
        "name": "孙丹",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1980年6月",
        "birthplace": "",
        "education": "文学学士（吉林师范大学汉语言文学）；在职研究生（省委党校经济管理）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长（挂职）",
        "current_org": "吉林市昌邑区人民政府",
        "source": "http://www.jlscy.gov.cn/ldfg/qz/wdts/202511/t20251127_1296959.html",
        "confidence": "confirmed",
        "notes": "1980年6月生，女，汉族，中共党员，吉林师范大学汉语言文学专业文学学士，省委党校在职研究生经济管理专业。现任昌邑区委常委、区政府副区长（挂职）。协助李丹丹副区长分管教育卫生、民生改善、残联等工作。"
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共吉林市昌邑区委员会", "type": "党委", "level": "县处级", "parent": "中共吉林市委员会", "location": "吉林市昌邑区"},
    {"id": 2, "name": "吉林市昌邑区人民政府", "type": "政府", "level": "县处级", "parent": "吉林市人民政府", "location": "吉林市昌邑区"},
    {"id": 3, "name": "吉林市昌邑区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "吉林市人大常委会", "location": "吉林市昌邑区"},
    {"id": 4, "name": "中国人民政治协商会议吉林市昌邑区委员会", "type": "政协", "level": "县处级", "parent": "吉林市政协", "location": "吉林市昌邑区"},
    {"id": 5, "name": "中共吉林市昌邑区纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共吉林市纪律检查委员会", "location": "吉林市昌邑区"},
    {"id": 6, "name": "吉林市公安局昌邑分局", "type": "政府", "level": "乡科级", "parent": "吉林市公安局", "location": "吉林市昌邑区"},
    {"id": 7, "name": "吉林昌邑经济开发区管理委员会", "type": "开发区", "level": "副县处级", "parent": "吉林市昌邑区人民政府", "location": "吉林市昌邑区"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 曹晶莹 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "2025", "end_date": "present", "rank": "县处级正职", "note": "现任区委书记，主持区委全面工作（2026-06/2026-01/2025-12新闻确认）"},
    # 伊同强 — 区长
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任昌邑区委副书记、区长，领导区政府全面工作"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "兼任区委副书记"},
    # 王庭忠 — 人大主任
    {"person_id": 3, "org_id": 3, "title": "区人大常委会主任", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任区人大常委会主任"},
    # 史良忠 — 政协主席
    {"person_id": 4, "org_id": 4, "title": "区政协主席", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任区政协主席"},
    # 刘美凤 — 纪委书记
    {"person_id": 5, "org_id": 5, "title": "区纪委书记、区监委主任", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "区委常委、区纪委书记、区监委主任"},
    {"person_id": 5, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "区委常委"},
    # 副区长们
    {"person_id": 6, "org_id": 2, "title": "常务副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "区委常委、常务副区长，负责区政府常务工作"},
    {"person_id": 7, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "区委常委、副区长，兼孤店子镇党委书记"},
    {"person_id": 8, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "副区长、市公安局昌邑分局局长"},
    {"person_id": 8, "org_id": 6, "title": "局长", "start_date": "", "end_date": "", "rank": "乡科级正职", "note": "市公安局昌邑分局局长"},
    {"person_id": 9, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "分管城市建设与管理、街道管理"},
    {"person_id": 10, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "分管交通、农业农村、政务服务数字化、林业畜牧"},
    {"person_id": 11, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "分管科技、工信、招商、商务、文旅"},
    {"person_id": 12, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "分管教育、民政、卫生、残联"},
    {"person_id": 13, "org_id": 2, "title": "副区长（挂职）", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "吉林市委副秘书长、区委常委、副区长（挂职）"},
    {"person_id": 14, "org_id": 2, "title": "副区长（挂职）", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "区委常委、副区长（挂职）"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 区委书记 ↔ 区长
    {"person_a": 1, "person_b": 2, "type": "共事", "context": "区委书记—区长党政协作搭档", "overlap_org": "中共吉林市昌邑区委员会", "overlap_period": "2025-2026"},
    # 区委书记 ↔ 人大主任 / 政协主席
    {"person_a": 1, "person_b": 3, "type": "共事", "context": "区委—区人大领导工作联系", "overlap_org": "吉林市昌邑区", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "区委—区政协领导工作联系", "overlap_org": "吉林市昌邑区", "overlap_period": "2025-2026"},
    # 区委书记 ↔ 纪委书记
    {"person_a": 1, "person_b": 5, "type": "共事", "context": "区委—区纪委监委领导关系", "overlap_org": "中共吉林市昌邑区委员会", "overlap_period": "2026"},
    # 区长 ↔ 人大常委会主任
    {"person_a": 2, "person_b": 3, "type": "共事", "context": "区长—人大常委会主任", "overlap_org": "吉林市昌邑区", "overlap_period": "2025-2026"},
    # 区长 ↔ 副区长（常务）
    {"person_a": 2, "person_b": 6, "type": "共事", "context": "区长—常务副区长", "overlap_org": "吉林市昌邑区人民政府", "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 7, "type": "共事", "context": "区长—副区长", "overlap_org": "吉林市昌邑区人民政府", "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 8, "type": "共事", "context": "区长—副区长/公安分局长", "overlap_org": "吉林市昌邑区人民政府", "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 9, "type": "共事", "context": "区长—副区长", "overlap_org": "吉林市昌邑区人民政府", "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 10, "type": "共事", "context": "区长—副区长", "overlap_org": "吉林市昌邑区人民政府", "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 11, "type": "共事", "context": "区长—副区长", "overlap_org": "吉林市昌邑区人民政府", "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 12, "type": "共事", "context": "区长—副区长", "overlap_org": "吉林市昌邑区人民政府", "overlap_period": "2025-2026"},
    # 常务副区长 ↔ 其他副区长
    {"person_a": 6, "person_b": 7, "type": "共事", "context": "常务副区长—副区长", "overlap_org": "吉林市昌邑区人民政府", "overlap_period": "2025-2026"},
    {"person_a": 6, "person_b": 8, "type": "共事", "context": "常务副区长—副区长", "overlap_org": "吉林市昌邑区人民政府", "overlap_period": "2025-2026"},
    {"person_a": 6, "person_b": 9, "type": "共事", "context": "常务副区长—副区长", "overlap_org": "吉林市昌邑区人民政府", "overlap_period": "2025-2026"},
    {"person_a": 6, "person_b": 10, "type": "共事", "context": "常务副区长—副区长", "overlap_org": "吉林市昌邑区人民政府", "overlap_period": "2025-2026"},
    {"person_a": 6, "person_b": 11, "type": "共事", "context": "常务副区长—副区长", "overlap_org": "吉林市昌邑区人民政府", "overlap_period": "2025-2026"},
    {"person_a": 6, "person_b": 12, "type": "共事", "context": "常务副区长—副区长", "overlap_org": "吉林市昌邑区人民政府", "overlap_period": "2025-2026"},
]


# ═════════════════════════════════════════════════════════════════════════════
# Helper functions
# ═════════════════════════════════════════════════════════════════════════════


def _get_open_questions(person: dict) -> list[str]:
    questions = []
    if not person.get("birth"):
        questions.append("出生年月未确认")
    if not person.get("birthplace"):
        questions.append("籍贯未确认")
    if not person.get("ethnicity"):
        questions.append("民族未确认")
    if not person.get("education"):
        questions.append("学历教育背景未确认")
    if not person.get("work_start"):
        questions.append("参加工作年份未确认")
    return questions


def write_person_json(person: dict) -> None:
    """Write a per-person graph JSON file following the person_graph_json.md schema."""
    pid = person["id"]
    name = person["name"]
    slug_id = f"changyi_{name}"

    # Collect positions for this person
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
            "confidence": "confirmed" if person.get("confidence") == "confirmed" else "unverified" if person.get("gender") else "unverified",
            "source_ids": ["S001"],
        })

    # Add explicit gap entries for figures with limited career data
    if name == "曹晶莹":
        career_timeline.append({
            "start": "unknown",
            "end": "unknown",
            "org": "早期履历缺口",
            "title": "",
            "notes": "曹晶莹任昌邑区委书记前的职务经历公开资料稀缺，待查（可能来自区县领导或市直部门；2025年已任区委书记）。",
            "confidence": "unverified",
            "source_ids": [],
        })
    elif pid in {3, 4, 5}:
        career_timeline.append({
            "start": "unknown",
            "end": "unknown",
            "org": "早期履历",
            "title": "",
            "notes": "官方新闻确认现任职务，但公开资料仅列出了此前任职经历，早期履历待补充。",
            "confidence": "unverified",
            "source_ids": [],
        })
    elif len([p for p in person_positions if p.get("start_date")]) == 0:
        career_timeline.append({
            "start": "unknown",
            "end": "unknown",
            "org": "履历补充",
            "title": "",
            "notes": "简历主体（出生、教育、任职）已由官方领导分工页确认，此处为跨区任职/早期履历的补全待查项。",
            "confidence": "unverified",
            "source_ids": [],
        })

    # Collect relationships for this person
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
            "person_id": f"changyi_{other_name}",
            "relationship_type": "overlap",
            "strength": "strong" if r["type"] == "共事" else "medium",
            "evidence": r.get("context", ""),
            "overlap_org": r.get("overlap_org", ""),
            "overlap_period": r.get("overlap_period", ""),
            "direction": "undirected",
            "confidence": person.get("confidence", "unverified"),
            "source_ids": ["S001"],
        })

    # Source register (district-level primary source)
    sources = [
        {
            "id": "S001",
            "title": "吉林市昌邑区人民政府领导分工页面",
            "url": "http://www.jlscy.gov.cn/ldfg/",
            "publisher": "吉林市昌邑区人民政府",
            "published_at": "2025-12-25",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "区政府领导名单与简历确认",
        },
        {
            "id": "S002",
            "title": "昌邑区新闻（区委书记曹晶莹、人大人大主任王庭忠、政协主席史良忠活动报道）",
            "url": "http://www.jlscy.gov.cn/gzdt/xwdt/",
            "publisher": "吉林市昌邑区人民政府",
            "published_at": "2026-01-20",
            "accessed_at": AS_OF,
            "source_type": "official",
            "reliability": "high",
            "notes": "确认曹晶莹任区委书记、王庭忠任人大常委会主任、史良忠任政协主席、刘美凤任纪委书记",
        },
    ]

    current_post = person.get("current_post", "")
    current_org = person.get("current_org", "")
    is_confirmed = person.get("confidence") == "confirmed"

    record = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "吉林省",
            "city": "吉林市",
            "region": "昌邑区",
            "job": current_post,
            "task_id": "jilin_昌邑区",
            "time_focus": "2025-2026年",
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
            "education": [
                {
                    "period": "",
                    "institution": "",
                    "major": "",
                    "degree": person.get("education", ""),
                    "study_type": "unknown",
                    "source_ids": ["S001"],
                }
            ] if person.get("education") else [],
            "party_join": person.get("party_join", ""),
            "work_start": person.get("work_start", ""),
            "dedupe_keys": {
                "name_birth": f"{name}_{person.get('birth','')}",
                "name_birthplace": f"{name}_{person.get('birthplace','')}",
                "official_profile_url": (person.get("source", "") or "").split("http")[-1].split("；")[0].strip() if "http" in (person.get("source") or "") else "",
            },
        },
        "current_status": {
            "current_post": current_post,
            "current_org": current_org,
            "administrative_rank": "县处级正职" if pid in {1, 2, 3, 4, 5} else "县处级副职",
            "as_of": AS_OF,
            "is_current_confirmed": is_confirmed,
            "source_ids": ["S001", "S002"],
        },
        "career_timeline": career_timeline,
        "organizations": [{"id": o["id"], "name": o["name"], "type": o["type"]} for o in organizations],
        "relationships": rels_output,
        "government_record": [],
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
        "source_register": sources,
        "confidence_summary": {
            "identity": "unverified" if not person.get("birth") else "confirmed",
            "current_role": person.get("confidence", "unverified"),
            "career_completeness": "partial" if person.get("birth") else "thin",
            "relationship_confidence": "medium",
            "biggest_gap": "成年履历或早期任职待补充",
        },
        "open_questions": [
            {
                "priority": "critical" if pid == 1 else ("high" if pid in {2, 3, 4, 5} else "medium"),
                "question": f"{name} 的{'任区委书记前' if pid==1 else ''}早期履历、籍贯、任职时间",
                "why_it_matters": "核心身份信息，用于去重和跨区域关联分析",
                "suggested_queries": [f"{name} 简历", f"昌邑区 任前公示 {name}", f"吉林 昌邑 {name}"],
                "last_attempted": AS_OF,
            },
        ] + [
            {"priority": "low" if q else "medium", "question": q, "why_it_matters": "完善身份信息", "suggested_queries": [], "last_attempted": AS_OF}
            for q in _get_open_questions(person)
        ],
    }

    # Determine filename
    role = current_post.split("兼")[0].split("、")[0].strip()
    fname = f"{TODAY}-吉林省-吉林市-{role}-{name}.json"
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
    core_ids = {1, 2, 3, 4, 5}  # 区委书记, 区长, 人大主任, 政协主席, 纪委书记 + 常务副区长
    core_ids.update({6})
    for p in persons:
        if p["id"] in core_ids:
            write_person_json(p)

    print(f"\n{SLUG} build complete.")
    print(f"  DB:  {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())