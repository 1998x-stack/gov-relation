#!/usr/bin/env python3
"""营口市西市区（辽宁省·市辖区）领导班子工作关系网络 - 数据构建脚本

目标职务：区委书记 & 区长
调查截至：2026-08-07
一手来源：营口市西市区政务信息网 www.ykxs.gov.cn（区政府领导之窗）、西市区官方政务微信公众号《河海西市》
（中国共产党营口市西市区第十五次代表大会开幕/胜利闭幕报道、曹德强防汛检查报道）、营口市人民政府官网。

调查说明（外部检索受限）：
- 搜索引擎（Exa/百度/必应/搜狗/360）在本机网络下全部 captcha 或超时不可用。
- 姜营市区政府官网 www.ykxs.gov.cn 可正常访问，区长/副区长班子全部确认。
- 中共西市区委班子成员通过第十五次党代会主席台前排名单确认，具体分工（副书记/纪委书记/组宣统政法等）部分未获，标为 plausible/unverified。
- 曹德强（区委书记）与李金玲（区长）身份已由官方/政务号双重确认。

数据分级（confidence）：
- confirmed：一手官方来源或两处独立可靠来源
- plausible：可信媒体/政务号，部分佐证
- unverified：线索不足，不构成强图边
"""

from __future__ import annotations

import sqlite3
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve()
for _ in range(6):
    if (REPO_ROOT / "gov_relation").is_dir():
        break
    REPO_ROOT = REPO_ROOT.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.paths import DATABASE_DIR, GRAPH_DIR  # noqa: E402
from gov_relation.runner import run_build  # noqa: E402

# ── 元数据 ─────────────────────────────────────────────────────────────
SLUG = "西市区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-08"

# ── 暂存路径（先写 staging，验证通过后再推广到 canonical）─────────────
_CURRENT = Path(__file__).resolve().parent
_CANDIDATE = REPO_ROOT / "data" / "tmp" / "liaoning_西市区"
if _CURRENT.name == "liaoning_西市区":
    STAGING = _CURRENT
elif _CANDIDATE.exists():
    STAGING = _CANDIDATE
else:
    STAGING = _CURRENT
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# ── 信息来源（统一 source_register）───────────────────────────────────
SRC_LDZC = "http://www.ykxs.gov.cn/ldzc/017001/017001001/leader.html"  # 区政府领导之窗（李金玲等）
SRC_LDZC_FY = "http://www.ykxs.gov.cn/ldzc/017004/{x}/leader.html"     # 副区长之窗
SRC_DDH_KAI = "https://mp.weixin.qq.com/s/lGTZ5FllPgLOp2ePXZgxug"       # 第十五次党代会开幕
SRC_DDH_BI = "https://mp.weixin.qq.com/s/fc-XQP-HqAQLUJWoCh0gmA"        # 第十五次党代会胜利闭幕
SRC_CDQ_FX = "https://mp.weixin.qq.com/s/W9vIGhQoInG2pf9ZGE9dkQ"        # 曹德强防汛检查
SRC_AQ_HY = "https://mp.weixin.qq.com/s/q39qmedd4FMw4S-_rhfj2A"         # 安全生产会议（李金玲讲话）
SRC_HOME = "http://www.ykxs.gov.cn/"

# ── 人员数据 ─────────────────────────────────────────────────────────────
# ID: 1=区委书记, 2=区长, 3-13=区委常委（3,4,5,8,9,10,11,12,13 分工待核），
#     6=常务副区长, 7=副区长区委常委, 14,15,16=副区长
persons = [
    # ═══ 核心两领导 ═══
    {
        "id": 1,
        "name": "曹德强",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "西市区委书记、辽宁（营口）沿海产业基地党工委书记",
        "current_org": "中共营口市西市区委员会",
        "source": SRC_DDH_BI + " ；" + SRC_CDQ_FX,
        "notes": "2026-07-22 第十五次党代会主席台前排首位；代表十四届区委作工作报告；7-24 主持闭幕并讲话。2026-07-13 报道标题明确'西市区委书记、辽宁（营口）沿海产业基地党工委书记曹德强'。身份 confirmed；完整简历待查。",
    },
    {
        "id": 2,
        "name": "李金玲",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1987-12",
        "birthplace": "",
        "education": "全日制大学学历、管理学学士，省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "西市区委副书记、区人民政府党组书记、区长",
        "current_org": "西市区人民政府",
        "source": SRC_LDZC,
    },
    # ═══ 区委常委班子（第十五次党代会主席台前排，分工部分待核实）═══
    {
        "id": 3,
        "name": "王启新",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "西市区委常委、区委副书记",
        "current_org": "中共营口市西市区委员会",
        "source": SRC_DDH_KAI,
        "notes": "第十五次党代会主席台前排第3位（书记、区长之后）。常委身份 confirmed；是否兼任区委副书记为 plausible。",
    },
    {
        "id": 4,
        "name": "邢文才",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "西市区委常委、区纪委书记（疑）",
        "current_org": "中共营口市西市区委员会",
        "source": SRC_DDH_KAI,
        "notes": "党代会主席台前排第4位。纪委职责为 plausible（未获任职文件确认）。",
    },
    {
        "id": 5,
        "name": "毛玉萧",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "西市区委常委",
        "current_org": "中共营口市西市区委员会",
        "source": SRC_DDH_KAI,
        "notes": "党代会主席台前排第5位。分工待核实。",
    },
    {
        "id": 6,
        "name": "刘佳斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985-08",
        "birthplace": "",
        "education": "研究生学历、经济学博士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "西市区委常委、区人民政府党组副书记、常务副区长",
        "current_org": "西市区人民政府",
        "source": "http://www.ykxs.gov.cn/ldzc/017004/017004001/leader.html",
    },
    {
        "id": 7,
        "name": "王运喜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-07",
        "birthplace": "",
        "education": "在职研究生学历、工商管理硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "西市区委常委、区人民政府党组成员、副区长",
        "current_org": "西市区人民政府",
        "source": "http://www.ykxs.gov.cn/ldzc/017004/017004003/leader.html",
    },
    {
        "id": 8,
        "name": "李生全",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "西市区委常委",
        "current_org": "中共营口市西市区委员会",
        "source": SRC_DDH_KAI,
        "notes": "党代会主席台前排第8位。分工待核实。",
    },
    {
        "id": 9,
        "name": "魏伊含",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "西市区委常委",
        "current_org": "中共营口市西市区委员会",
        "source": SRC_DDH_KAI,
        "notes": "党代会主席台前排第9位。分工待核实。",
    },
    {
        "id": 10,
        "name": "吕威",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "西市区委常委",
        "current_org": "中共营口市西市区委员会",
        "source": SRC_DDH_KAI,
        "notes": "党代会主席台前排第10位。分工待核实。",
    },
    {
        "id": 11,
        "name": "于淼",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "西市区委常委",
        "current_org": "中共营口市西市区委员会",
        "source": SRC_DDH_KAI,
        "notes": "党代会主席台前排第11位。分工待核实。",
    },
    {
        "id": 12,
        "name": "王海波",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "西市区委常委",
        "current_org": "中共营口市西市区委员会",
        "source": SRC_DDH_KAI,
        "notes": "党代会主席台前排第12位。分工待核实。",
    },
    {
        "id": 13,
        "name": "李刚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "西市区委常委",
        "current_org": "中共营口市西市区委员会",
        "source": SRC_DDH_KAI,
        "notes": "党代会主席台前排第13位。分工待核实。",
    },
    # ═══ 区政府其他部门负责人（副区长）═══
    {
        "id": 14,
        "name": "李克柏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-10",
        "birthplace": "",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "西市区人民政府党组成员、副区长",
        "current_org": "西市区人民政府",
        "source": "http://www.ykxs.gov.cn/ldzx/017004/017004002/leader.html",
        "notes": "分工：公安、司法、社会稳定、海防、打击走私。",
    },
    {
        "id": 15,
        "name": "李俊武",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983-06",
        "birthplace": "",
        "education": "全日制研究生学历、管理学硕士学位",
        "party_join": "",
        "work_start": "",
        "current_post": "西市区人民政府副区长",
        "current_org": "西市区人民政府",
        "source": "http://www.ykxs.gov.cn/ldzx/017004/017004005/leader.html",
        "notes": "分工：工业、商务、民营经济、文旅、市场监管。",
    },
    {
        "id": 16,
        "name": "续军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-05",
        "birthplace": "",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "西市区人民政府党组成员、副区长",
        "current_org": "西市区人民政府",
        "source": "http://www.ykxs.gov.cn/ldzx/017004/017004006/leader.html",
        "notes": "分工：民政、农业农村、退役军人事务。",
    },
]

# ── 机构数据 ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共营口市西市区委员会", "type": "党委", "level": "市辖区", "parent": "中共营口市委员会", "location": "辽宁省营口市西市区"},
    {"id": 2, "name": "西市区人民政府", "type": "政府", "level": "市辖区", "parent": "营口市人民政府", "location": "辽宁省营口市西市区"},
    {"id": 3, "name": "辽宁（营口）沿海产业基地党工委", "type": "开发区", "level": "市级产业园区", "parent": "营口市", "location": "辽宁省营口市"},
    {"id": 4, "name": "中共营口市西市区纪律检查委员会/监委", "type": "党委", "level": "市辖区", "parent": "中共营口市西市区委员会", "location": "辽宁省营口市西市区"},
    {"id": 5, "name": "营口市西市区人大常委会", "type": "人大", "level": "市辖区", "parent": "营口市西市区", "location": "辽宁省营口市西市区"},
    {"id": 6, "name": "政协营口市西市区委员会", "type": "政协", "level": "市辖区", "parent": "营口市西市区", "location": "辽宁省营口市西市区"},
]

# ── 任职数据 ─────────────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "present", "rank": "县处级正职",
     "note": "第十五次党代会（2026-07-22 开幕）主席台首位，代表十四届区委作报告，7-24 主持大会并讲话；身份 confirmed。任期起止待核实。"},
    {"person_id": 1, "org_id": 3, "title": "辽宁（营口）沿海产业基地党工委书记", "start_date": "", "end_date": "present", "rank": "",
     "note": "2026-07-13 报道明确其兼任沿海产业基地党工委书记。"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "区政府党组书记；confirmed。"},
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "主持区政府全面工作，分管审计局；confirmed。"},
    {"person_id": 3, "org_id": 1, "title": "区委常委、区委副书记（疑）", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "党代会主席台前排第3位；副书记职责为 plausible。"},
    {"person_id": 4, "org_id": 1, "title": "区委常委、区纪委书记（疑）", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "党代会主席台前排第4位；纪委职责为 plausible。"},
    {"person_id": 5, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "党代会主席台前排第5位；分工待核实。"},
    {"person_id": 6, "org_id": 2, "title": "区委常委、常务副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "区政府党组副书记；负责政法/发改/财税/住建/应急等常务；confirmed。"},
    {"person_id": 7, "org_id": 2, "title": "区委常委、副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责营商环境、住建、招商、生态 等；confirmed。"},
    {"person_id": 8, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "党代会主席台前排第8位；分工待核实。"},
    {"person_id": 9, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "党代会主席台前排第9位；分工待核实。"},
    {"person_id": 10, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "党代会主席台前排第10位；分工待核实。"},
    {"person_id": 11, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "党代会主席台前排第11位；分工待核实。"},
    {"person_id": 12, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "党代会主席台前排第12位；分工待核实。"},
    {"person_id": 13, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "党代会主席台前排第13位；分工待核实。"},
    {"person_id": 14, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责公安、司法、社会稳定、海防、打击走私；confirmed。"},
    {"person_id": 15, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责工业、商务、文旅、市场监管；confirmed。"},
    {"person_id": 16, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责民政、农业农村、退役军人事务；confirmed。"},
]

# ── 关系数据 ─────────────────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "区委书记—区长，党政一把手分工格局；2026-07-15 届党代会同一班子。",
     "overlap_org": "中共营口市西市区委员会 / 西市区人民政府", "overlap_period": "现任（2026）"},
    {"person_a": 1, "person_b": 6, "type": "上下级",
     "context": "区委书记—常务副区长（区委常委），区政府党组副书记。", "overlap_org": "西市区人民政府", "overlap_period": "现任（2026）"},
    {"person_a": 1, "person_b": 7, "type": "上下级",
     "context": "区委书记—区委常委（副区长）。", "overlap_org": "西市区人民政府", "overlap_period": "现任（2026）"},
    {"person_a": 2, "person_b": 6, "type": "上下级",
     "context": "区长—常务副区长（区政府党组副书记）。", "overlap_org": "西市区人民政府", "overlap_period": "现任（2026）"},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "区长—区委常委副区长。", "overlap_org": "西市区人民政府", "overlap_period": "现任（2026）"},
    {"person_a": 2, "person_b": 14, "type": "上下级", "context": "区长—副区长（公安/司法）。", "overlap_org": "西市区人民政府", "overlap_period": "现任（2026）"},
    {"person_a": 2, "person_b": 15, "type": "上下级", "context": "区长—副区长（工业/文旅）。", "overlap_org": "西市区人民政府", "overlap_period": "现任（2026）"},
    {"person_a": 2, "person_b": 16, "type": "上下级", "context": "区长—副区长（民政/农业农村）。", "overlap_org": "西市区人民政府", "overlap_period": "现任（2026）"},
    {"person_a": 6, "person_b": 7, "type": "同僚", "context": "同为区委常委、政府副职，党代会议上台前排并列。", "overlap_org": "中共营口市西市区委员会", "overlap_period": "现任（2026）"},
]


def main() -> None:
    print("=" * 60)
    print(f"  {SLUG} 领导班子工作关系网络")
    print(f"  等级: 市辖区（辽宁省营口市）")
    print(f"  调查日期: {AS_OF}")
    print("=" * 60)

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )

    print(f"\n  DB  : {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")
    print(f"\n✅ {SLUG} 数据构建完成。")


if __name__ == "__main__":
    main()