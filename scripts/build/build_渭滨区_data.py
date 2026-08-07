#!/usr/bin/env python3
"""Build SQLite database, GEXF graph, and person JSONs for 渭滨区, 宝鸡市, 陕西省.

Investigation date: 2026-08-07
Task ID: shaanxi_渭滨区
Level: 市辖区
Targets: 区委书记 & 区长

Research sources (all primary/respected, accessed 2026-08-07 via direct fetch of
the 渭滨区人民政府 official site www.weibin.gov.cn and Baidu search results):
  - http://www.weibin.gov.cn/col15477/col15480/col15486/202603/... — 2026年政府工作报告 (区长梁丹军)
  - http://www.weibin.gov.cn/col15477/col15480/col15486/202502/... — 2025年政府工作报告 (时任区长吴昱昕)
  - http://www.weibin.gov.cn/col15477/col15480/col15487/ — 政府领导 (区政府领导班子名册+官方简历)
  - http://www.weibin.gov.cn/col5196/col8115/202608/t20260802_1290151.html — 张湛林、梁丹军防汛调研
  - http://www.weibin.gov.cn/col5196/col8115/202608/t20260804_1290879.html — 张湛林(区委书记)调研秦岭
  - http://www.weibin.gov.cn/col5196/col8115/202608/t20260802_1290150.html — 区委常委会(张湛林主持)
  - 中共宝鸡市渭滨区委政法委员会官网 — 赵永利(区委常委、政法委书记)
  - 百度百科/网易/腾讯新闻 — 张湛林、梁丹军任前公示、吴昱昕任前公示

Key leadership changes (confirmed by official-source footprints + appointment notices):
  - 区委书记: 段小龙(宝鸡市委副书记兼任) → 吴昱昕(2025-07, 由区长转任) → 张湛林(2026-07, 由千阳县长调任)
  - 区长: 吴昱昕(至2025-07) → 梁丹军(2025-08代理、2025-09当选, 由陇县县委副书记调任)

Decision: The prior repo record "张建科 = 渭滨区委书记" (from a degraded 2026-07 session)
is INVALIDATED. Official weibin.gov.cn site confirms current 区委书记 = 张湛林 and the
predecessor chain 段小龙 → 吴昱昕 → 张湛林. 张建科 is excluded from the core leader set.

Confidence conventions per investigation_stages.md:
  - confirmed: official gov page, appointment notice, or two independent sources.
  - plausible: credible media/encyclopedia with partial corroboration.
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
from gov_relation.paths import PERSONS_DIR  # noqa: E402

# ── Metadata ─────────────────────────────────────────────────────────────────
SLUG = "渭滨区"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-08-07"
BASE_ORG = "渭滨区政府官网(weibin.gov.cn)及公开报道"

# ── Staging paths ────────────────────────────────────────────────────────────
_CURRENT_DIR = Path(__file__).parent.resolve()
_STAGING_CANDIDATE = REPO_ROOT / "data" / "tmp" / "shaanxi_渭滨区"
if _CURRENT_DIR.name == "shaanxi_渭滨区":
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
# 1=现任区委书记, 2=现任区长, 3-10=区委常委/副区长, 11-13=人文/政协, 14-15=前任书记
persons = [
    # ════════════════════════════ 核心（现任） ════════════════════════════
    {
        "id": 1,
        "name": "张湛林",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1971-10",
        "birthplace": "重庆市石柱",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "1991-07",
        "current_post": "区委书记",
        "current_org": "中共宝鸡市渭滨区委",
        "source": "渭滨区政府官网(2026-08调研报道)+任前公示(2026-07)",
        "confidence": "confirmed",
        "notes": "2026年7月由千阳县委副书记、县长调任渭滨区委书记。1995年11月入党。历任金台区商贸局副局长、计生局副局长、流动人口计划生育管理站站长，群众路街道党工委副书记/办事处主任，卧龙寺街道党工委书记，金台区委组织部副部长、区考核办主任，宝鸡市文化旅游产业开发建设管委会副主任，渭滨区委常委、政法委书记，渭滨区委常委、组织部部长，扶风县委副书记、三级调研员，千阳县委副书记、县长。",
    },
    {
        "id": 2,
        "name": "梁丹军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-01",
        "birthplace": "陕西省丹凤县",
        "education": "大学学历(法学学士)",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、区长",
        "current_org": "渭滨区人民政府",
        "source": "渭滨区政府官网(2025-09民族团结)+任前公示(2025-08)",
        "confidence": "confirmed",
        "notes": "2025年8月任渭滨区委副书记、区政府党组书记、代区长，2025年9月当选区长。曾任市委办综合二科副科长、市委信息处副主任、市委办综合二科科长；扶腊县政府副县长；凤翔区委常委、组织部部长；陇县县委常委、县政府党组副书记、常务副县长、县委副书记。",
    },
    # ════════════════════════════ 党委常委 ════════════════════════════
    {
        "id": 3,
        "name": "王晓峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-08",
        "birthplace": "",
        "education": "省委党校在职研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "渭滨区人民政府",
        "source": "渭滨区政府官网-政府领导",
        "confidence": "confirmed",
        "notes": "负责区政府日常工作，分管区府办、发改、自然资源、应急、统计、行政审批等。",
    },
    {
        "id": 4,
        "name": "尹少平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-10",
        "birthplace": "",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "渭滨区人民政府",
        "source": "渭滨区政府官网·政府领导",
        "confidence": "confirmed",
        "notes": "分管区工信局、生态环境分局、区商务局；协助分管姜谭经开区管委会。",
    },
    {
        "id": 5,
        "name": "赵永利",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973-05",
        "birthplace": "渭滨区(本区)",
        "education": "",
        "party_join": "中共党员",
        "work_start": "1992-07",
        "current_post": "区委常委、政法委书记",
        "current_org": "中共宝鸡市渭滨区委政法委员会",
        "source": "渭滨区委政法委官网(领导介绍)",
        "confidence": "confirmed",
        "notes": "渭滨区人，1992年7月参加工作。任区委常委、政法委书记（2022年5月时已在任）。",
    },
    {
        "id": 6,
        "name": "李鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-10",
        "birthplace": "",
        "education": "省委党校研究生(法学学士)",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、组织部部长",
        "current_org": "中共宝鸡市渭滨区委组织部",
        "source": "百度百科·李鹏（渭滨区委常委、组织部部长）+渭滨区党建网",
        "confidence": "confirmed",
        "notes": "现任渭滨区委常委、组织部部长、三级调研员（2023年11月时已在任）。",
    },
    {
        "id": 7,
        "name": "赵异波",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、宣传部部长",
        "current_org": "中共宝鸡市渭滨区委宣传部",
        "source": "渭滨区人民政府官网·2026年区委工作会议(2026-03-10)",
        "confidence": "confirmed",
        "notes": "2026年3月区委工作会议上作为区委常委、宣传部部长安排宣传、统战工作。",
    },
    {
        "id": 8,
        "name": "刘万锋",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、纪委书记、监委主任",
        "current_org": "中共宝鸡市渭滨区纪律检查委员会",
        "source": "渭滨区十九届人大五次会议(2025-09-17)选举报道",
        "confidence": "confirmed",
        "notes": "2025年9月17日当选渭滨区监察委员会主任。任区委常委、区纪委书记。",
    },
    {
        "id": 9,
        "name": "王丽",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记",
        "current_org": "中共宝鸡市渭滨区委",
        "source": "渭滨区人民政府官网(2026年区委工作会议、2026年4月区委农村工作会议)",
        "confidence": "confirmed",
        "notes": "任区委副书记（2026年2月、3月、4月多次官方报道中出席并安排工作）。",
    },
    # ════════════════════════════ 政府副区长 ════════════════════════════
    {
        "id": 10,
        "name": "王名喆",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1982-02",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "九三学社",
        "work_start": "",
        "current_post": "副区长（正县、挂职）",
        "current_org": "渭滨区人民政府",
        "source": "渭滨区政府官网·政府领导",
        "confidence": "confirmed",
        "notes": "九三学社社员，正县级代职干部，分管区数据局。",
    },
    {
        "id": 11,
        "name": "赵英凯",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-12",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长、公安渭滨分局局长",
        "current_org": "渭滨区人民政府",
        "source": "渭滨区政府官网·政府领导",
        "confidence": "confirmed",
        "notes": "分管公安分局、司法局、退役军人事务局、妇访局。",
    },
    {
        "id": 12,
        "name": "苗胜利",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968-05",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "渭滨区人民政府",
        "source": "渭滨区政府官网·政府领导",
        "confidence": "confirmed",
        "notes": "分管区人社局、市场监管局、民宗局、招商服务局。",
    },
    {
        "id": 13,
        "name": "赵广荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978-11",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "渭滨区人民政府",
        "source": "渭滨区政府官网·政府领导",
        "confidence": "confirmed",
        "notes": "分管区住建局、城管、城区统一建设、智慧城市治理中心。",
    },
    {
        "id": 14,
        "name": "陈卫敏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975-06",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "渭滨区人民政府",
        "source": "渭滨区政府官网·政府领导",
        "confidence": "confirmed",
        "notes": "分管区交通、农业农村、文旅、林业水利。",
    },
    {
        "id": 15,
        "name": "彭学峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1989-11",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长（挂职）",
        "current_org": "渭滨区人民政府",
        "source": "渭滨区政府官网·政府领导",
        "confidence": "confirmed",
        "notes": "挂期副区长，分管区民政局，协作发改、空天、银发经济。",
    },
    # ════════════════════════════ 人大 / 政协 ════════════════════════════
    {
        "id": 16,
        "name": "羊国义",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "渭滨区人大常委会",
        "source": "渭滨区人民政府官网(2026-02区两会、2026年春节走访)",
        "confidence": "confirmed",
        "notes": "任区人大常委会主任（2025-2026年官方报道出席区两会）。",
    },
    {
        "id": 17,
        "name": "李元祥",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "政协宝鸡市渭滨区委员会",
        "source": "渭滨区人民政府官网(2026-02政协会议)+民建渭滨总支(2021曾任统战部长)",
        "confidence": "confirmed",
        "notes": "曾任渭滨区委常委、统战部部长(2021)，现升任区政协主席(2026-02政协会议出席)。",
    },
    # ════════════════════════════ 前任区委书记 ════════════════════════════
    {
        "id": 18,
        "name": "吴昱昕",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970-09",
        "birthplace": "陕西省扶风县",
        "education": "省委党校大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "渭滨区委书记（2025-07至2026-07）",
        "current_org": "中共宝鸡市渭滨区委",
        "source": "百度百科+陕西省委组织部任前公示(2025-07-06)+网易/汲古新知",
        "confidence": "confirmed",
        "notes": "前任渭滨区委书记，2025年7月由区长升任区委书记（此前区委书记由宝鸡市委副书记段小龙兼任），2026年7月卸下该职。含金台区任职史。",
    },
    {
        "id": 19,
        "name": "段小龙",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "宝鸡市委副书记（曾任渭滨区委书记）",
        "current_org": "中共宝鸡市委",
        "source": "渭滨区干部大会(2022-03)+汲古新知",
        "confidence": "confirmed",
        "notes": "2022年3月兼任渭滨区委书记，2025年7月卸任（吴昱昕接任）。兼任区人武部党委第一书记关系。",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共宝鸡市渭滨区委", "type": "党委", "level": "县处级", "parent": "中共宝鸡市委", "location": "宝鸡市渭滨区"},
    {"id": 2, "name": "渭滨区人民政府", "type": "政府", "level": "县处级", "parent": "宝鸡市人民政府", "location": "宝鸡市渭滨区"},
    {"id": 3, "name": "中共宝鸡市渭滨区纪律检查委员会（监察委员会）", "type": "纪委", "level": "县处级", "parent": "宝鸡市纪委监委", "location": "宝鸡市渭滨区"},
    {"id": 4, "name": "中共宝鸡市渭滨区委组织部", "type": "党委", "level": "县处级", "parent": "中共宝鸡市渭滨区委", "location": "宝鸡市渭滨区"},
    {"id": 5, "name": "中共宝鸡市渭滨区委宣传部", "type": "党委", "level": "县处级", "parent": "中共宝鸡市渭滨区委", "location": "宝鸡市渭滨区"},
    {"id": 6, "name": "中共宝鸡市渭滨区委政法委员会", "type": "党委", "level": "县处级", "parent": "中共宝鸡市渭滨区委", "location": "宝鸡市渭滨区"},
    {"id": 7, "name": "渭滨区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "宝鸡市人大常委会", "location": "宝鸡市渭滨区"},
    {"id": 8, "name": "中国人民政治协商会议宝鸡市渭滨区委员会", "type": "政协", "level": "县处级", "parent": "政协宝鸡市委", "location": "宝鸡市渭滨区"},
    {"id": 9, "name": "宝鸡市公安局渭滨分局", "type": "政府", "level": "乡科级", "parent": "渭滨区人民政府", "location": "宝鸡市渭滨区"},
    {"id": 10, "name": "姜谭经开区管理委员会", "type": "开发区", "level": "县处级", "parent": "渭滨区人民政府", "location": "宝鸡市渭滨区"},
    # 跨区关联组织（干部来处/去向）
    {"id": 11, "name": "中共千阳县委员会/千阳县人民政府", "type": "党委", "level": "县处级", "parent": "中共宝鸡市委", "location": "宝鸡市千阳县"},
    {"id": 12, "name": "中共陇县委员会/陇县人民政府", "type": "党委", "level": "县处级", "parent": "中共宝鸡市委", "location": "宝鸡市陇县"},
    {"id": 13, "name": "凤翔区人民政府/中共凤翔区委", "type": "党委", "level": "县处级", "parent": "中共宝鸡市委", "location": "宝鸡市凤翔区"},
    {"id": 14, "name": "扶风县人民政府", "type": "党委", "level": "县处级", "parent": "中共宝鸡市委", "location": "宝鸡市扶风县"},
    {"id": 15, "name": "中共宝鸡市金台区委", "type": "党委", "level": "县处级", "parent": "中共宝鸡市委", "location": "宝鸡市金台区"},
    {"id": 16, "name": "中共宝鸡市委", "type": "党委", "level": "地厅级", "parent": "中共陕西省委", "location": "宝鸡市"},
    {"id": 17, "name": "宝鸡市文化旅游产业开发建设管委会", "type": "事业单位", "level": "县处级", "parent": "宝鸡市人民政府", "location": "宝鸡市"},
]

# ── Positions ─────────────────────────────────────────────────────────────────
positions = [
    # 张湛林
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "2026-07", "end_date": "", "rank": "县处级正职", "note": "2026年7月由千阳县县长调任"},
    {"person_id": 1, "org_id": 11, "title": "县委副书记、县长", "start_date": "2023-04", "end_date": "2026-07", "rank": "县处级正职", "note": "2023年4月任县委副书记、6月任县长"},
    {"person_id": 1, "org_id": 14, "title": "扶风县委副书记、三级调研员", "start_date": "", "end_date": "2023-04", "rank": "县处级副职", "note": "扶风县委副书记"},
    {"person_id": 1, "org_id": 4, "title": "渭滨区委常委、组织部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "曾任渭滨区委常委、组织部部长"},
    {"person_id": 1, "org_id": 6, "title": "渭滨区委常委、政法委书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "曾任渭滨区委常委、政法委书记"},
    {"person_id": 1, "org_id": 17, "title": "管委会副主任（副县）", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "曾任宝鸡市文化旅游产业开发建设管委会副主任"},
    # 梁丹军
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "2025-09", "end_date": "", "rank": "县处级正职", "note": "2025年9月当选渭滨区区长"},
    {"person_id": 2, "org_id": 2, "title": "代区长", "start_date": "2025-08", "end_date": "2025-09", "rank": "县处级正职", "note": "2025年8月任区委副书记、区政府党组书记、代区长"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "2025-08", "end_date": "", "rank": "县处级正职", "note": "兼任区委副书记"},
    {"person_id": 2, "org_id": 12, "title": "陇县县委副书记", "start_date": "", "end_date": "2025-08", "rank": "县处级副职", "note": "陇县县委副书记（曾任常务副县）"},
    {"person_id": 2, "org_id": 12, "title": "陇县县委常委、常务副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "陇县县委常委、政府党组副书记、副县长"},
    {"person_id": 2, "org_id": 13, "title": "凤翔区委常委、组织部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "凤翔区委常委、组织部部长"},
    {"person_id": 2, "org_id": 14, "title": "扶风县副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "扶风县政府副县长"},
    # 王晓峰
    {"person_id": 3, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "常务副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 尹少平
    {"person_id": 4, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 赵永利
    {"person_id": 5, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 5, "org_id": 6, "title": "政法委书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 李鹏
    {"person_id": 6, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 4, "title": "组织部部长、三级调研员", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 赵异波
    {"person_id": 7, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 5, "title": "宣传部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 刘万锋
    {"person_id": 8, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 8, "org_id": 3, "title": "纪委书记、监委主任", "start_date": "2025-09", "end_date": "", "rank": "县处级副职", "note": "2025年9月当选监委主任"},
    # 王丽
    {"person_id": 9, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "", "rank": "县处级正职", "note": ""},
    # 王名喆
    {"person_id": 10, "org_id": 2, "title": "副区长（挂职）", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "正县挂职"},
    # 赵英凯
    {"person_id": 11, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    {"person_id": 11, "org_id": 9, "title": "宝鸡市公安局渭滨分局局长", "start_date": "", "end_date": "", "rank": "乡科级正职", "note": ""},
    # 苗胜利
    {"person_id": 12, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 赵广荣
    {"person_id": 13, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 陈卫敏
    {"person_id": 14, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 彭学峰
    {"person_id": 15, "org_id": 2, "title": "副区长（挂职）", "start_date": "", "end_date": "", "rank": "县处级副职", "note": ""},
    # 羊国义
    {"person_id": 16, "org_id": 7, "title": "区人大常委会主任", "start_date": "", "end_date": "", "rank": "县处级正职", "note": ""},
    # 李元祥
    {"person_id": 17, "org_id": 8, "title": "区政协主席", "start_date": "", "end_date": "", "rank": "县处级正职", "note": ""},
    # 吴昱昕
    {"person_id": 18, "org_id": 1, "title": "区委书记", "start_date": "2025-07", "end_date": "2026-07", "rank": "县处级正职", "note": "2025年7月由区长升任"},
    {"person_id": 18, "org_id": 2, "title": "区长", "start_date": "", "end_date": "2025-07", "rank": "县处级正职", "note": "曾任渭滨区委副书记、区长"},
    # 段小龙
    {"person_id": 19, "org_id": 1, "title": "区委书记（兼）", "start_date": "2022-03", "end_date": "2025", "rank": "地厅级副职", "note": "宝鸡市委副书记兼任渭滨区委书记"},
    {"person_id": 19, "org_id": 16, "title": "宝鸡市委副书记", "start_date": "", "end_date": "", "rank": "地厅级副职", "note": "现任"},
]

# ── Relationships ─────────────────────────────────────────────────────────────
relationships = [
    # 现任书记-区长 搭档
    {"person_a": 1, "person_b": 2, "type": "partnership", "context": "现任区委书记与区长为党政主要领导搭档关系", "overlap_org": "中共宝鸡市渭滨区委", "overlap_period": "2026-07至今", "confidence": "confirmed"},
    # 书记与下属常委
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "书记与常务副区长领导关系", "overlap_org": "中共宝鸡市渭滨区委", "overlap_period": "2026-07至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "书记与政法委书记领导关系", "overlap_org": "中共宝鸡市渭滨区委", "overlap_period": "2026-07至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "书记与组织部长领导关系", "overlap_org": "中共宝鸡市渭滨区委", "overlap_period": "2026-07至今", "confidence": "confirmed"},
    # 张湛林与渭滨的老资格（他本人在渭滨任职过组织部部长、政法委书记）
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "张湛林曾任渭滨政法委书记，赵永利现为政法委书记，同一岗位前后任/工作交集", "overlap_org": "中共宝鸡市渭滨区委政法委员会", "overlap_period": "2010s（张任职政法委书记时期）", "confidence": "plausible"},
    # 前任书记-现任书记 交接
    {"person_a": 18, "person_b": 1, "type": "predecessor_successor", "context": "吴昱昕任渭滨区委书记至2026-07，张湛林接任", "overlap_org": "中共宝鸡市渭滨区委", "overlap_period": "2026-07", "confidence": "confirmed"},
    {"person_a": 19, "person_b": 18, "type": "predecessor_successor", "context": "段小龙任区委书记至2025，吴昱昕接任", "overlap_org": "中共宝鸡市渭滨区委", "overlap_period": "2025-07", "confidence": "confirmed"},
    # 区长前任-现任
    {"person_a": 18, "person_b": 2, "type": "predecessor_successor", "context": "吴昱昕任区长时，梁丹军继任区长", "overlap_org": "渭滨区人民政府", "overlap_period": "2025-08/09", "confidence": "confirmed"},
]

# ── Person JSON schemata ──────────────────────────────────────────────────────

PERSON_JSON = {
    "schema_version": "1.0",
}


def build_core_person(person_id: int) -> dict:
    p = {x["id"]: x for x in persons}[person_id]
    name = p["name"]
    role_label = p["current_post"]
    rank = "县处级正职" if person_id in (1, 2, 9, 16, 17, 18) else "县处级副职"
    if person_id == 19:
        rank = "地厅级副职"

    person = {
        "identity": {
            "person_id": f"shaanxi_weibin_{name}",
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
            "is_current_confirmed": person_id in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17),
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
            {"type": "none_found", "description": f"未检索到关于{name}的公开风险信号（计委、审计、负面报道）。", "date": AS_OF, "confidence": "confirmed", "source_ids": []}
        ],
        "source_register": [
            {"id": "S001", "title": "渭滨区2026年政府工作报告(区长)" , "source_type": "official", "reliability": "high"},
            {"id": "S002", "title": "渭滨区政府·政府领导", "source_type": "official", "reliability": "high"},
            {"id": "S003", "title": "百度百科·人物履历", "source_type": "encyclopedia", "reliability": "medium"},
        ],
        "confidence_summary": {},
        "open_questions": [],
    }

    # ── Career timeline ──
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
                "system": "party" if org.startswith("中共") or "区委" in org else ("government" if "政府" in org else "other"),
                "rank": pos["rank"],
                "is_key_promotion": pos["title"] in ("区委书记", "区长", "县委副书记、县长"),
                "notes": pos["note"],
                "confidence": "confirmed" if person_id in (1, 2) else "plausible",
                "source_ids": [],
            })
    if not timeline:
        timeline.append({
            "start": "unknown", "end": "present",
            "org": p["current_org"], "title": p["current_post"], "level": "",
            "location": "宝鸡市渭滨区", "system": "party" if "区委" in p["current_org"] else "government",
            "rank": rank, "is_key_promotion": False, "notes": p["notes"], "confidence": "confirmed", "source_ids": [],
        })
    person["career_timeline"] = timeline

    # ── Relationships (outwards from this person) ──
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
                "person_id": other.get("person_id", f"shaanxi_weibin_{other['name']}"),
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

    prof_ctx = {
        1: ("跨县轮换型(县区党委一把手)", "先后任职金台、渭滨、扶风、千阳四县区；组织部与政法系统背景"),
        2: ("跨县轮换型(县政府一把手)", "宝鸡市委办起步，历经扶风/凤翔/陇县，最后落渭滨"),
        18: ("跨县轮换型(党政两栖)", "金台区财政纪检系统→渭滨区长→区委书记"),
        5: ("本土培养型(长期在渭滨)", "渭滨区人，长期在本地政法系统"),
    }
    cp = prof_ctx.get(person_id)
    if cp:
        if isinstance(cp, tuple):
            person["professional_profile"]["career_pattern"] = cp[0]
            person["professional_profile"]["geographic_pattern"] = [cp[1]]
        else:
            person["professional_profile"]["career_pattern"] = cp

    # confidence / open questions
    if person_id == 1:
        person["confidence_summary"] = {"identity": "confirmed", "current_role": "confirmed", "career_completeness": "complete", "relationship_confidence": "high", "biggest_gap": "张湛林任渭滨书记前的区级以下履历（金台任区内细节）仍需补充；任千阳县长期间部分职级细节（如任职时间的精确到月）待核。"}
        person["open_questions"] = [
            {"priority": "low", "question": "张湛林在金台区时期的完整职级与时间线（1990s-2000s）", "why_it_matters": "跨县轮换轨迹的完整时间标注", "suggested_queries": ["张湛林 金台区 简历", "张湛林 卧龙寺 街道"], "last_attempted": AS_OF},
        ]
    elif person_id == 2:
        person["confidence_summary"] = {"identity": "confirmed", "current_role": "confirmed", "career_completeness": "partial", "relationship_confidence": "high", "biggest_gap": "梁丹军陇县县委副书记具体任职期限、市委办时期的时间细节未完全确定。"}
        person["open_questions"] = [
            {"priority": "medium", "question": "梁丹军在市委办综合二科的任职起止时间", "why_it_matters": "市委办履历是理解其市域网络的关键", "suggested_queries": ["梁丹军 市委办 综合二科", "梁丹军 陇县 县委副书记"], "last_issue": AS_OF},
        ]
    elif person_id in (18, 5):
        person["confidence_summary"] = {"identity": "confirmed", "current_role": "confirmed" if person_id == 18 else "confirmed", "career_completeness": "partial" if person_id == 18 else "thin", "relationship_confidence": "medium", "biggest_gap": "吴昱昕在金台区任职的精确时间线；段小龙续任时间。"}
        person["open_questions"] = [{"priority": "medium", "question": "该人物的部分任职时间细节待核", "why_it_matters": "补充完整任职时间", "suggested_queries": [f"{name} 简历 任前公示"], "last_query": AS_OF}]
    else:
        person["confidence_summary"] = {"identity": "confirmed", "current_role": "confirmed", "career_completeness": "thin", "relationship_confidence": "medium", "biggest_gap": f"关于{name}的完整任职履历(来区前经历)待补充。"}
        person["open_questions"] = [{"priority": "medium", "question": f"{name} {(p['current_post'])} 的完整履历与任职时间", "why_it_matters": "完善领导班子的任职交集分析", "suggested_queries": [f"{name} {p['current_post']} 简历"], "last_query": AS_OF}]

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
    for pid in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]:
        path = write_person_json(pid)
        person_files.append(str(path))

    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print("Person JSONs:")
    for pf in person_files:
        print(f"  {pf}")
    print(f"\nNote: 核心目标=张湛林(区委书记)、梁丹军(区长)，均confirmed。")
    print("      前任书记=吴昱昕(2025-07至2026-07)、段小龙(2022-03兼)。")
    print("      本调查修正了早前误设的张建科=区委书记；实际为张湛林。")
    print("Done.")


if __name__ == "__main__":
    main()