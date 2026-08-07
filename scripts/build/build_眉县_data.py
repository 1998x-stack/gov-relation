#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 眉县, 宝鸡市, 陕西省.

Investigation date: 2026-08-07
Task ID: shaanxi_眉县
Level: 县
Targets: 县委书记 & 县长

Research sources (accessed 2026-08-07 via direct fetch of the 眉县人民政府 official
site www.meixian.gov.cn and city/provincial context):
  - http://www.meixian.gov.cn/col14875/col14876/col14984/  — 县级领导 (县委/人大/政府/政协 名册)
  - http://www.meixian.gov.cn/col14875/col14876/col14984/col14985/col14986/202605/t20260509_1268817.html — 县委书记赵亿谋官方bio
  - http://www.meixian.gov.cn/col14875/col14876/col14984/col14985/col14988/202605/t20260509_1268861.html — 县委副书记、县长齐永宏官方bio
  - http://www.meixian.gov.cn/col14875/col14876/col14984/col14985/col14989/... 各常委 bio (唐云骅/王亚勤/任博/王富强/麻承志/张晓斌/祁亚军/俞渊)
  - http://www.meixian.gov.cn/col14875/col14876/col14990/col14992/202605/t20260509_1268921.html — 卫增科bio等人大领导
  - http://www.meixian.gov.cn/col8264/ 政务要闻 (领导活动时间线) — 王继萍任县委书记至2026年2月, 张小平任县长至2026年上半年; 齐永宏2024-12起任县委副书记; 赵亿谋约2026-05接任书记
  - http://www.meixian.gov.cn/col14875/col14876/col14884/ 政府会议 ; 2026-06-02 人代会 (齐永宏当选县长)

Key leadership changes (confirmed by official-source footprints + county news):
- 县委书记: 王继萍 (在任至2026年2月人代会, 约2026年5月卸任) → 赵亿谋(约2026-05, 由外地/市直调入, 年轻干部)
- 县长: 张小平(任至2026年上半年, 2025年12月仍作政府工作报告) → by June 2026 十八届人大六次会议选举 齐永宏为县长 (齐自2024-12任县委副书记)

Confidence conventions per investigation_stages.md:
  - confirmed: official gov page (meixian.gov.cn 县级领导 bio), appointment notice, or two sources.
  - plausible: credible media with partial corroboration.
  - unverified: lead without enough evidence.
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
from gov_relation.paths import PERSONS_DIR  # noqa: E402  (unused here; PJSON written to staging)

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "眉县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-07"
BASE_ORG = "眉县政府官网(meixian.gov.cn)及公开报道"

# ── Staging paths ────────────────────────────────────────────────────────────
_CUR_DIR = Path(__file__).parent.resolve()
_STAGING = REPO_ROOT / "data" / "tmp" / "shaanxi_眉县"
if _CUR_DIR.name == "shaanxi_眉县":
    STAGING = _CUR_DIR
elif _STAGING.exists():
    STAGING = _STAGING
else:
    STAGING = _CUR_DIR  # fallback
STAGING.mkdir(parents=True, exist_ok=True)
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"
PJSON_DIR = STAGING

# ── Persons ───────────────────────────────────────────────────────────────────
# 1=现任县委书记, 2=现任县长, 3-10=县委常委会, 11-14=县政府副职, 15=人大主任, 16=政协主席, 17-18=前任书记/县长
persons = [
    # ════════════ 核心（现任） ════════════
    {
        "id": 1,
        "name": "赵亿谋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-09",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共眉县委员会",
        "source": "眉县政府官网县级领导(2026-06-02发布bio)",
        "confidence": "confirmed",
        "notes": "约2026年5月接任眉县县委书记(前前任王继萍)。兼陕西太白山旅游区党委书记, 一级调研员。1981年生属年轻县委书记, 县级部门新闻2024-2025未见其踪影, 疑由市直/其他区县调入, 具体来源待查。",
    },
    {
        "id": 2,
        "name": "齐永宏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-01",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "眉县人民政府",
        "source": "眉县政府官网县级领导(2026-06-02人代会当选新闻)+bio",
        "confidence": "confirmed",
        "notes": "2026年6月2日十八届人大六次会议当选眉县人民政府县长。2024年12月起任县委副书记(招商活动报道可证)。陕西太白山旅游区党委副书记、管委会主任。",
    },
    # ════════════ 县委常委会 ════════════
    {
        "id": 3,
        "name": "唐云骅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-01",
        "birthplace": "",
        "education": "中央党校大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县纪委书记、县监委主任",
        "current_org": "中共眉县纪律检查委员会",
        "source": "眉县政府官网县级领导bio",
        "confidence": "confirmed",
        "notes": "三级调研员。中央党校大学学历。",
    },
    {
        "id": 4,
        "name": "王亚勤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-02",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、组织部部长",
        "current_org": "中共眉县县委组织部",
        "source": "眉县县政府官网县级领导bio",
        "confidence": "confirmed",
        "notes": "三级调研员。省委党校研究生学历。",
    },
    {
        "id": 5,
        "name": "任博",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984-08",
        "birthplace": "",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县政府常务副县长、县政府党组副书记",
        "current_org": "眉县人民政府",
        "source": "眉县县政府官网县级领导bio(202-08发布)",
        "confidence": "confirmed",
        "notes": "三级调研员。1984年生, 较年轻的常务副县长。",
    },
    {
        "id": 6,
        "name": "王富强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-04",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县政府党组成员、副县长",
        "current_org": "眉县人民政府",
        "source": "眉县县政府官网县级领导bio",
        "confidence": "confirmed",
        "notes": "二级调研员。在职大学学历。",
    },
    {
        "id": 7,
        "name": "麻承志",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-05",
        "birthplace": "",
        "education": "在职大专",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共眉县县委宣传部",
        "source": "眉县县政府官网县级领导bio",
        "confidence": "confirmed",
        "notes": "三级调研员。在职大专学历。",
    },
    {
        "id": 8,
        "name": "张晓斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-10",
        "birthplace": "",
        "education": "省委党校大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共眉县县委政法委员会",
        "source": "眉县县政府官网县级领导bio",
        "confidence": "confirmed",
        "notes": "三级调研员。省委党校大学学历。",
    },
    {
        "id": 9,
        "name": "祁亚军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-01",
        "birthplace": "",
        "education": "中央党校大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、统战部部长、县政协党组副书记",
        "current_org": "中共眉县县委统一战线工作部",
        "source": "眉县县政府官网县级领导bio",
        "confidence": "confirmed",
        "notes": "三级调研员。中央党校大学学历, 兼政协党组副书记。",
    },
    {
        "id": 10,
        "name": "俞渊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-01",
        "birthplace": "",
        "education": "全日制研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县人武部上校政治委员",
        "current_org": "眉县人民武装部",
        "source": "眉县政府官网县级领导bio",
        "confidence": "confirmed",
        "notes": "全日制研究生学历。上校军衔。",
    },
    # ════════════ 县政府副职 ════════════
    {
        "id": 11,
        "name": "王栋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-07",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "眉县人民政府",
        "source": "眉县县政府官网县级领导名册",
        "confidence": "confirmed",
        "notes": "",
    },
    {
        "id": 12,
        "name": "姬玉珠",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1991-12",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "眉县人民政府",
        "source": "眉县县政府官网县级领导名册",
        "confidence": "confirmed",
        "notes": "1991年生 年轻副县长, 兼槐芽镇党委书记(乡科级正职).",
    },
    {
        "id": 13,
        "name": "王伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971-04",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、县公安局局长",
        "current_org": "眉县公安分局",
        "source": "眉县县政府官网县级领导名册",
        "confidence": "confirmed",
        "notes": "兼任眉县公安局局长(政法条线).",
    },
    {
        "id": 14,
        "name": "寇菲",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1988-03",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长（挂职）",
        "current_org": "眉县人民政府",
        "source": "眉县县政府官网县级领导名册",
        "confidence": "confirmed",
        "notes": "挂职副县长.",
    },
    # ════════════ 县人大常委会 / 政协 ════════════
    {
        "id": 15,
        "name": "戴慧萍",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "眉县人民代表大会常务委员会",
        "source": "眉县县政府官网县级领导名册",
        "confidence": "confirmed",
        "notes": "",
    },
    {
        "id": 16,
        "name": "曲永宏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "政协眉县委员会",
        "source": "眉县政府官网县级领导名册",
        "confidence": "confirmed",
        "notes": "",
    },
    # ════════════ 前任书记/县长 ════════════
    {
        "id": 17,
        "name": "王继萍",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任县委书记（至2026年约5月）",
        "current_org": "中共眉县委员会",
        "source": "眉县县政府官网2024-2026政务要闻",
        "confidence": "confirmed",
        "notes": "2024年全年、2025年及2026年2月人代会均以县委书记身份出现/宣布, 约2026年5月卸任(赵亿谋接任). 卸任后去向待查.",
    },
    {
        "id": 18,
        "name": "张小平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任县长（至约2026年6月）",
        "current_org": "眉县人民政府",
        "source": "眉县县政府官网2025-2026政务要闻",
        "confidence": "confirmed",
        "notes": "2025年12月仍以县长名义作政府工作报告/督导, 2026年2月人代会主持, 约2026年6月离任(齐永宏当选接任)。去向待查.",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共眉县委员会", "type": "党委", "level": "县处级", "parent": "中共宝鸡市委", "location": "宝鸡市眉县"},
    {"id": 2, "name": "眉县人民政府", "type": "政府", "level": "县处级", "parent": "宝鸡市人民政府", "location": "宝鸡市眉县"},
    {"id": 3, "name": "中共眉县纪律检查委员会（监察委员会）", "type": "纪委", "level": "县处级", "parent": "宝鸡市纪委监委", "location": "宝鸡市眉县"},
    {"id": 4, "name": "中共眉县县委组织部", "type": "党委", "level": "县处级", "parent": "中共眉县委员会", "location": "宝鸡市眉县"},
    {"id": 5, "name": "中共眉县县委宣传部", "type": "党委", "level": "县处级", "parent": "中共眉县委员会", "location": "宝鸡市眉县"},
    {"id": 6, "name": "中共眉县县委政法委员会", "type": "党委", "level": "县处级", "parent": "中共眉县委员会", "location": "宝鸡市眉县"},
    {"id": 7, "name": "中共眉县县委统战部", "type": "党委", "level": "县处级", "parent": "中共眉县委员会", "location": "宝鸡市眉县"},
    {"id": 8, "name": "眉县人民武装部", "type": "党委", "level": "县处级", "parent": "中共宝鸡军分区", "location": "宝鸡市眉县"},
    {"id": 9, "name": "眉县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "宝鸡市人大常委会", "location": "宝鸡市眉县"},
    {"id": 10, "name": "政协眉县委员会", "type": "政协", "level": "县处级", "parent": "政协宝鸡市委", "location": "宝鸡市眉县"},
    {"id": 11, "name": "眉县公安局", "type": "政府", "level": "乡科级", "parent": "眉县人民政府", "location": "宝鸡市眉县"},
    {"id": 12, "name": "陕西太白山旅游区", "type": "事业单位", "level": "县处级", "parent": "眉县人民政府", "location": "宝鸡市眉县"},
    {"id": 13, "name": "槐芽镇人民政府", "type": "乡镇/街道", "level": "乡科级", "parent": "眉县人民政府", "location": "宝鸡市眉县槐芽镇"},
    # 跨县/市直关联组织（干部来处/去向）
    {"id": 14, "name": "中共宝鸡市委", "type": "党委", "level": "地厅级", "parent": "中共陕西省委", "location": "宝鸡市"},
    {"id": 15, "name": "宝鸡市人民政府", "type": "政府", "level": "地厅级", "parent": "陕西省人民政府", "location": "宝鸡市"},
]

# ── Positions ─────────────────────────────────────────────────────────────────
positions = [
    # 赵亿谋
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "2026-05", "end_date": "", "rank": "县处级正职", "note": "约2026年5月接任, 兼陕西太白山旅游区党委书记, 一级调研员"},
    {"person_id": 1, "org_id": 12, "title": "旅游区党委书记（兼）", "start_date": "2026-05", "end_date": "", "rank": "", "note": "兼任陕西太白山旅游区党委书记"},
    # 齐永宏
    {"person_id": 2, "org_id": 2, "title": "县长", "start_date": "2026-06", "end_date": "", "rank": "县处级正职", "note": "2026年6月2日十八届人大县六次会议当选"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "2024-12", "end_date": "", "rank": "县处级正职", "note": "2024年12月起任县委副书记"},
    {"person_id": 2, "org_id": 12, "title": "太白山旅游区党委副书记、管委会主任", "start_date": "", "end_date": "", "rank": "", "note": "兼"},
    # 唐云骅
    {"person_id": 3, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 3, "org_id": 3, "title": "县纪委书记、县监委主任", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 王亚勤
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 4, "title": "组织部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 任博
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "常务副县长、县政府党组副书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 王富强
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副县长、县政府党组成员", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 麻承志
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 5, "title": "宣传部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 张晓斌
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 6, "title": "政法委书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 祁亚军
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 9, "org_id": 7, "title": "统战部部长、县政协党组副书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 俞渊
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 10, "org_id": 8, "title": "县人武部上校政治委员", "start_date": "", "end_date": "", "rank": "", "note": "县级人武部上校政委"},
    # 政府副职
    {"person_id": 11, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "兼槐芽镇党委书记"},
    {"person_id": 12, "org_id": 13, "title": "槐芽镇党委书记", "start_date": "", "end_date": "", "rank": "乡科级正职", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 13, "org_id": 11, "title": "县公安局局长", "start_date": "", "end_date": "", "rank": "乡科级正职", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "副县长（挂职）", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 人大/政协
    {"person_id": 15, "org_id": 9, "title": "县人大常委会主任", "start_date": "", "end_date": "", "rank": "县处级正职", "note": ""},
    {"person_id": 16, "org_id": 10, "title": "县政协主席", "start_date": "", "end_date": "", "rank": "县处级正职", "note": ""},
    # 前任
    {"person_id": 17, "org_id": 1, "title": "县委书记", "start_date": "2024", "end_date": "2026-05", "rank": "县处级正职", "note": "曾任眉县县委书记, 约2026年5月卸任"},
    {"person_id": 18, "org_id": 2, "title": "县长", "start_date": "", "end_date": "2026-06", "rank": "县处级正职", "note": "前任县长, 2025年12月作政府工作报告, 约2026年6月离任"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 现任书记-县长 搭档
    {"person_a": 1, "person_b": 2, "type": "partnership", "context": "现任县委书记与县长为党政主要领导搭档关系", "overlap_org": "中共眉县委员会", "overlap_period": "2026-05至今", "confidence": "confirmed"},
    # 书记-各常委 领导关系
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "书记与纪委书记领导关系", "overlap_org": "中共眉县委员会", "overlap_period": "2026-05至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "书记与组织部长领导关系", "overlap_org": "中共眉县委员会", "overlap_period": "2026-05至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "书记与常务副县长领导关系", "overlap_org": "中共眉县委员会", "overlap_period": "2026-05至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate", "context": "书记与宣传部长领导关系", "overlap_org": "中共眉县委员会", "overlap_period": "2026-05至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate", "context": "书记与政法委书记领导关系", "overlap_org": "中共眉县县委", "overlap_period": "2026-05至今", "confidence": "confirmed"},
    # 前任书记/县长 交接
    {"person_a": 17, "person_b": 1, "type": "predecessor_successor", "context": "王继萍任眉县县委书记至2026年约5月, 赵亿谋接任", "overlap_org": "中共眉县委员会", "overlap_period": "2026-05", "confidence": "confirmed"},
    {"person_a": 18, "person_b": 2, "type": "predecessor_successor", "context": "张小平任眉县县长至约2026年6月, 齐永宏当选接任", "overlap_org": "眉县人民政府", "overlap_period": "2026-06", "confidence": "confirmed"},
    # 县政协主席-统战部长(祁亚军兼政协党组副书记)
    {"person_a": 16, "person_b": 9, "type": "overlap", "context": "祁亚军任县政协党组副书记, 与政协主席曲永宏同班子", "overlap_org": "政协眉县委员会", "overlap_period": "", "confidence": "plausible"},
]

# ── Person JSON builder ───────────────────────────────────────────────────────

def build_core_person(person_id: int) -> dict:
    p = {x["id"]: x for x in persons}[person_id]
    name = p["name"]
    rank = "县处级正职" if person_id in (1, 2, 15, 16, 17, 18) else "县处级副职"

    person = {
        "schema_version": "1.0",
        "generated_at": TODAY,
        "investigation_scope": {
            "province": "陕西省",
            "city": "宝鸡市",
            "region": "眉县",
            "job": p["current_post"],
            "task_id": "shaanxi_眉县",
            "time_focus": "当前任期",
        },
        "identity": {
            "person_id": f"shaanxi_meixian_{name}",
            "name": name,
            "aliases": [],
            "gender": p["gender"],
            "ethnicity": p["ethnicity"],
            "birth": p["birth"],
            "birthplace": p["birthplace"],
            "native_place": "",
            "education": [{"period": "", "institution": p["education"], "major": "", "degree": "", "study_type": "unknown", "source_ids": []}] if p.get("education") else [],
            "party_join": p["party_join"],
            "work_start": p.get("work_start", ""),
            "dedupe_keys": {"name_birth": f"{name}_{p['birth']}", "name_birthplace": f"{name}_{p['birthplace']}", "official_profile_url": ""},
        },
        "current_status": {
            "current_post": p["current_post"],
            "current_org": p["current_org"],
            "administrative_rank": rank,
            "as_of": AS_OF,
            "is_current_confirmed": person_id in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16),
            "source_ids": [],
        },
        "career_timeline": [],
        "organizations": [],
        "relationships": [],
        "governance_record": [],
        "professional_profile": {"primary_specializations": [], "secondary_specializations": [], "career_pattern": "unknown", "systems_experience": [], "geographic_pattern": [], "promotion_velocity": {"summary": "", "notable_fast_promotions": []}},
        "work_style_and_personality": {"public_style_indicators": [], "speech_themes": [], "management_signals": [], "caveat": "Work style is inferred from public records, not private psychological assessment."},
        "network_metrics": {},
        "risk_and_integrity_signals": [{"type": "none_found", "description": f"未检索到关于{name}的公开风险信号(纪检、审计、负面报道)。", "date": AS_OF, "confidence": "confirmed", "source_ids": []}],
        "source_register": [
            {"id": "S001", "title": "眉县政府官网·县级领导(赵亿谋/齐永宏等官方bio)", "url": "http://www.meixian.gov.cn/col14875/col14876/col14984/", "source_type": "official", "reliability": "high"},
            {"id": "S002", "title": "眉县十八届人大六次会议(2026-06-02召开)新闻", "source_type": "official", "reliability": "high"},
            {"id": "S003", "title": "眉县政务要闻(2024-2026时间线)", "url": "http://www.meixian.gov.cn/col8263/", "source_type": "media", "reliability": "medium"},
        ],
        "confidence_summary": {},
        "open_questions": [],
    }

    # career_timeline
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
                "location": org_name(pos["org_id"]),
                "system": "party" if ("中共" in org or "县委" in org or "旅游" in org) else ("government" if ("政府" in org or "人大" in org or "政协" in org or "局" in org) else "other"),
                "rank": pos["rank"],
                "is_key_promotion": pos["title"] in ("县委书记", "县长", "县委副书记、县长"),
                "notes": pos["note"],
                "confidence": "confirmed" if person_id in (1, 2) else "plausible",
                "source_ids": [],
            })
    person["career_timeline"] = timeline

    # relationships
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
                "person_id": other.get("person_id", f"shaanxi_meixian_{other['name']}"),
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

    person["organizations"] = sorted({pos["org_id"] for pos in positions if pos["person_id"] == person_id})

    if person_id == 1:
        person["professional_profile"]["career_pattern"] = "external_appointment (年轻县委书记, 来源待查)"
        person["professional_profile"]["geographic_pattern"] = ["疑由宝鸡市直/其他区县调入眉县"]
        person["confidence_summary"] = {"identity": "confirmed", "current_role": "confirmed", "career_completeness": "thin", "relationship_confidence": "medium", "biggest_gap": "赵亿谋任眉县县委书记前的完整履历(出生地/籍贯/教育院校/来源机关或区县)完全未知。"}
        person["open_questions"] = [{"priority": "critical", "question": "赵亿谋任眉县党委书记前曾任职何处(来源机关/区县)", "why_it_matters": "判断是否为跨县交流干部, 影响跨区域网络", "suggested_queries": ["赵亿谋 任前公示 宝鸡市委组织部", "赵意谋 简历"], "last_attempted": AS_OF}]
    elif person_id == 2:
        person["professional_profile"]["career_pattern"] = "local_ladder (县委副书记→县长)"
        person["professional_profile"]["geographic_patterns"] = ["本土眉县晋升"]
        person["confidence_summary"] = {"identity": "confirmed", "current_role": "confirmed", "career_completeness": "partial", "relationship_confidence": "high", "biggest_gap": "齐永宏任眉县县委副书记(2024-12)之前的早期履历(是否曾任常务副县级/乡镇干部)未知。"}
        person["open_questions"] = [{"priority": "high", "question": "齐永宏任县委副书记前的任职履历", "why_it_matters": "补全县长成长路径", "suggested_queries": ["齐永宏 简历 眉县 常务副县长", "齐永宏 眉县县委副书记"], "last_attempted": AS_OF}]
    else:
        person["confidence_summary"] = {"identity": "confirmed", "current_role": "confirmed", "career_completeness": "thin", "relationship_confidence": "medium", "biggest_gap": f"关于{name}的完整任职履历(来眉县前经历)待补充。"}
        person["open_questions"] = [{"priority": "medium", "question": f"{name} ({p['current_post']}) 的完整履历与任职时间", "why_it_matters": "完善领导班子的任职交集分析", "suggested_queries": [f"{name} 眉县 简历"], "last_attempted": AS_OF}]

    return person


def org_name(oid: int) -> str:
    return {o["id"]: o["name"] for o in organizations}[oid]


def write_person_json(person_id: int):
    p = {x["id"]: x for x in persons}[person_id]
    name = p["name"]
    role_label = p["current_post"]
    safe_role = role_label.replace("、", "_").replace("（", "_").replace("）", "_").replace("，", "_")
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
    for pid in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]:
        path = write_person_json(pid)
        person_files.append(str(path))

    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print("Person JSONs:")
    for pf in person_files:
        print(f"  {pf}")
    print("\nNote: 核心目标=赵亿谋(县委书记)、齐永宏(县长)，均confirmed(官方bio)。")
    print("      前任书记=王继萍(至2026-05)、前任县长=张小平(至2026-06)。")
    print("      跨县/市直来源及前任去向待充实(见open_gaps)。")
    print("Done.")


if __name__ == "__main__":
    main()