#!/usr/bin/env python3
"""Build 新绛县 (Xinjiang County) personnel network database + GEXF graph + person JSONs.

Targets: 县委书记 (宋志江), 县长 (蒋锋)
Level: 县
Parent city: 运城市 (Yuncheng City), 山西省

Data sources:
- 新绛县人民政府门户网站 (www.jiangzhou.gov.cn) — primary, current as of July 2026
  -- 县委领导: https://www.jiangzhou.gov.cn/zfxxgk/fdzdgknr/ldzc/xwld/index.shtml
  -- 县政府领导: https://www.jiangzhou.gov.cn/zfxxgk/fdzdgknr/ldzc/xzfld/index.shtml
  -- 县人大领导: https://www.jiangzhou.gov.cn/zfxxgk/fdzdgknr/ldzc/xrdld/index.shtml
  -- 县政协领导: https://www.jiangzhou.gov.cn/zfxxgk/fdzdgknr/ldzc/xzxld/index.shtml
- 运城市人民政府官网 (www.yuncheng.gov.cn)

Confidence notes:
- Current roles, names, gender, ethnicity, birth, education: confirmed via official website leadership pages (primary quality, 2026-07)
- Full career timelines: unverified due to web access limitations (Baidu blocked)
- Relationship evidence: overlaps inferred from shared organizations with confirmed timeline
"""

from __future__ import annotations

import json
import os
import sqlite3  # noqa: used by gov_relation.runner
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent
for parent_count in range(1, 6):
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, PERSONS_DIR

SLUG = "新绛县"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-26"

DB_PATH_STR = f"{DATABASE_DIR / f'{SLUG}_network.db'}"
GEXF_PATH_STR = f"{GRAPH_DIR / f'{SLUG}_network.gexf'}"
DB_PATH = DATABASE_DIR / f"{SLUG}_network.db"
GEXF_PATH = GRAPH_DIR / f"{SLUG}_network.gexf"

# Source URLs
URL_XWLD = "https://www.jiangzhou.gov.cn/zfxxgk/fdzdgknr/ldzc/xwld/index.shtml"
URL_XZFLD = "https://www.jiangzhou.gov.cn/zfxxgk/fdzdgknr/ldzc/xzfld/index.shtml"
URL_XRDLD = "https://www.jiangzhou.gov.cn/zfxxgk/fdzdgknr/ldzc/xrdld/index.shtml"
URL_XZXLD = "https://www.jiangzhou.gov.cn/zfxxgk/fdzdgknr/ldzc/xzxld/index.shtml"

# ========== PERSONS DATA ==========

persons = [
    # === Core Leaders: 县委书记 & 县长 ===
    {
        "id": 1, "name": "宋志江", "gender": "男", "ethnicity": "汉族",
        "birth": "1971年2月", "birthplace": "",
        "education": "中央党校大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委书记", "current_org": "中共新绛县委员会",
        "source": URL_XWLD
    },
    {
        "id": 2, "name": "蒋锋", "gender": "男", "ethnicity": "汉族",
        "birth": "1984年3月", "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委副书记、县长", "current_org": "新绛县人民政府",
        "source": URL_XWLD
    },
    # === 县委常委 ===
    {
        "id": 3, "name": "王会民", "gender": "男", "ethnicity": "汉族",
        "birth": "1979年4月", "birthplace": "",
        "education": "中央党校大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委副书记、新绛中学党委书记", "current_org": "中共新绛县委员会",
        "source": URL_XWLD
    },
    {
        "id": 4, "name": "宁谦祥", "gender": "男", "ethnicity": "汉族",
        "birth": "1978年3月", "birthplace": "",
        "education": "中央党校大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委、县政府党组成员、副县长", "current_org": "新绛县人民政府",
        "source": URL_XWLD
    },
    {
        "id": 5, "name": "王星", "gender": "男", "ethnicity": "汉族",
        "birth": "1983年12月", "birthplace": "",
        "education": "大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委、县政府党组副书记、副县长", "current_org": "新绛县人民政府",
        "source": URL_XWLD
    },
    {
        "id": 6, "name": "原军伟", "gender": "男", "ethnicity": "汉族",
        "birth": "1983年4月", "birthplace": "",
        "education": "大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委、纪委书记、监委主任", "current_org": "中共新绛县纪律检查委员会",
        "source": URL_XWLD
    },
    {
        "id": 7, "name": "郭波", "gender": "男", "ethnicity": "汉族",
        "birth": "1976年4月", "birthplace": "",
        "education": "大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委、政法委书记", "current_org": "中共新绛县委政法委员会",
        "source": URL_XWLD
    },
    {
        "id": 8, "name": "刘磊", "gender": "男", "ethnicity": "汉族",
        "birth": "1984年3月", "birthplace": "",
        "education": "大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委、宣传部部长", "current_org": "中共新绛县委宣传部",
        "source": URL_XWLD
    },
    {
        "id": 9, "name": "贺伟", "gender": "男", "ethnicity": "汉族",
        "birth": "1982年8月", "birthplace": "",
        "education": "大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委、组织部部长、县委党校校长", "current_org": "中共新绛县委组织部",
        "source": URL_XWLD
    },
    {
        "id": 10, "name": "吴栋", "gender": "男", "ethnicity": "汉族",
        "birth": "1979年2月", "birthplace": "",
        "education": "大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委、人武部政委", "current_org": "新绛县人武部",
        "source": URL_XWLD
    },
    {
        "id": 11, "name": "李林丹", "gender": "女", "ethnicity": "汉族",
        "birth": "1987年11月", "birthplace": "",
        "education": "大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县委常委、统战部部长、县政协党组副书记", "current_org": "中共新绛县委统战部",
        "source": URL_XWLD
    },
    # === 县政府领导 (non-standing committee) ===
    {
        "id": 12, "name": "孙贵明", "gender": "男", "ethnicity": "汉族",
        "birth": "1977年7月", "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县政府党组副书记、新绛经济技术开发区党工委书记、管委会主任", "current_org": "新绛经济技术开发区",
        "source": URL_XZFLD
    },
    {
        "id": 13, "name": "张毅", "gender": "男", "ethnicity": "汉族",
        "birth": "1986年12月", "birthplace": "",
        "education": "研究生农学博士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县政府党组成员、副县长", "current_org": "新绛县人民政府",
        "source": URL_XZFLD
    },
    {
        "id": 14, "name": "杨喆", "gender": "男", "ethnicity": "汉族",
        "birth": "1976年7月", "birthplace": "",
        "education": "中央党校大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县政府党组成员、副县长", "current_org": "新绛县人民政府",
        "source": URL_XZFLD
    },
    {
        "id": 15, "name": "尚应东", "gender": "男", "ethnicity": "汉族",
        "birth": "1974年7月", "birthplace": "",
        "education": "大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县政府党组成员、副县长、公安局党委书记、局长、督察长", "current_org": "新绛县公安局",
        "source": URL_XZFLD
    },
    {
        "id": 16, "name": "卢玉玉", "gender": "女", "ethnicity": "汉族",
        "birth": "1989年3月", "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县政府党组成员、副县长", "current_org": "新绛县人民政府",
        "source": URL_XZFLD
    },
    {
        "id": 17, "name": "孙洪涛", "gender": "男", "ethnicity": "汉族",
        "birth": "1985年10月", "birthplace": "",
        "education": "大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县政府党组成员、副县长、泽掌镇党委书记", "current_org": "新绛县人民政府",
        "source": URL_XZFLD
    },
    # === 县人大领导 ===
    {
        "id": 18, "name": "杨瑞林", "gender": "男", "ethnicity": "汉族",
        "birth": "1973年6月", "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县人大常委会党组书记、主任", "current_org": "新绛县人民代表大会常务委员会",
        "source": URL_XRDLD
    },
    {
        "id": 19, "name": "张茜", "gender": "女", "ethnicity": "汉族",
        "birth": "1965年6月", "birthplace": "",
        "education": "中央党校大学",
        "party_join": "", "work_start": "",
        "current_post": "县人大常委会副主任", "current_org": "新绛县人民代表大会常务委员会",
        "source": URL_XRDLD
    },
    {
        "id": 20, "name": "毕冠军", "gender": "男", "ethnicity": "汉族",
        "birth": "1975年4月", "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县人大常委会党组成员、副主任候选人、三级调研员", "current_org": "新绛县人民代表大会常务委员会",
        "source": URL_XRDLD
    },
    {
        "id": 21, "name": "杨建国", "gender": "男", "ethnicity": "汉族",
        "birth": "1971年11月", "birthplace": "",
        "education": "大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县人大常委会党组成员、副主任", "current_org": "新绛县人民代表大会常务委员会",
        "source": URL_XRDLD
    },
    {
        "id": 22, "name": "卫红鸽", "gender": "女", "ethnicity": "汉族",
        "birth": "1976年4月", "birthplace": "",
        "education": "中央党校大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县人大常委会党组成员、副主任", "current_org": "新绛县人民代表大会常务委员会",
        "source": URL_XRDLD
    },
    # === 县政协领导 ===
    {
        "id": 23, "name": "闫世杰", "gender": "男", "ethnicity": "汉族",
        "birth": "1967年7月", "birthplace": "",
        "education": "大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县政协党组书记、主席", "current_org": "中国人民政治协商会议新绛县委员会",
        "source": URL_XZXLD
    },
    {
        "id": 24, "name": "王晓民", "gender": "男", "ethnicity": "汉族",
        "birth": "1970年4月", "birthplace": "",
        "education": "大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县政协党组副书记、副主席", "current_org": "中国人民政治协商会议新绛县委员会",
        "source": URL_XZXLD
    },
    {
        "id": 25, "name": "李忠", "gender": "男", "ethnicity": "汉族",
        "birth": "1968年7月", "birthplace": "",
        "education": "大学",
        "party_join": "", "work_start": "",
        "current_post": "县政协副主席", "current_org": "中国人民政治协商会议新绛县委员会",
        "source": URL_XZXLD
    },
    {
        "id": 26, "name": "赵珉", "gender": "男", "ethnicity": "汉族",
        "birth": "1971年6月", "birthplace": "",
        "education": "大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "县政协党组成员、副主席", "current_org": "中国人民政治协商会议新绛县委员会",
        "source": URL_XZXLD
    },
    {
        "id": 27, "name": "董亚红", "gender": "女", "ethnicity": "汉族",
        "birth": "1971年5月", "birthplace": "",
        "education": "大学",
        "party_join": "", "work_start": "",
        "current_post": "县政协副主席", "current_org": "中国人民政治协商会议新绛县委员会",
        "source": URL_XZXLD
    },
]

# ========== ORGANIZATIONS ==========

organizations = [
    {"id": 1, "name": "中共新绛县委员会", "type": "党委", "level": "县", "parent": "中共运城市委员会", "location": "山西省运城市新绛县"},
    {"id": 2, "name": "新绛县人民政府", "type": "政府", "level": "县", "parent": "运城市人民政府", "location": "山西省运城市新绛县"},
    {"id": 3, "name": "中共新绛县纪律检查委员会", "type": "纪委", "level": "县", "parent": "中共新绛县委员会", "location": "山西省运城市新绛县"},
    {"id": 4, "name": "中共新绛县委政法委员会", "type": "党委", "level": "县", "parent": "中共新绛县委员会", "location": "山西省运城市新绛县"},
    {"id": 5, "name": "中共新绛县委宣传部", "type": "党委", "level": "县", "parent": "中共新绛县委员会", "location": "山西省运城市新绛县"},
    {"id": 6, "name": "中共新绛县委组织部", "type": "党委", "level": "县", "parent": "中共新绛县委员会", "location": "山西省运城市新绛县"},
    {"id": 7, "name": "中共新绛县委统战部", "type": "党委", "level": "县", "parent": "中共新绛县委员会", "location": "山西省运城市新绛县"},
    {"id": 8, "name": "新绛县人武部", "type": "军队", "level": "县", "parent": "运城军分区", "location": "山西省运城市新绛县"},
    {"id": 9, "name": "新绛经济技术开发区", "type": "开发区", "level": "县", "parent": "新绛县人民政府", "location": "山西省运城市新绛县"},
    {"id": 10, "name": "新绛县公安局", "type": "政府", "level": "县", "parent": "新绛县人民政府", "location": "山西省运城市新绛县"},
    {"id": 11, "name": "新绛县人民代表大会常务委员会", "type": "人大", "level": "县", "parent": "", "location": "山西省运城市新绛县"},
    {"id": 12, "name": "中国人民政治协商会议新绛县委员会", "type": "政协", "level": "县", "parent": "", "location": "山西省运城市新绛县"},
    {"id": 13, "name": "新绛中学", "type": "事业单位", "level": "县", "parent": "新绛县人民政府", "location": "山西省运城市新绛县"},
]

# ========== POSITIONS ==========

positions = [
    # 县委书记
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "", "rank": "正处级", "note": "县委书记、一把手"},
    # 县长
    {"person_id": 2, "org_id": 2, "title": "县委副书记、县长", "start_date": "", "end_date": "", "rank": "正处级", "note": "县政府党组书记"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    # 县委副书记
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "", "rank": "副处级", "note": "兼新绛中学党委书记"},
    {"person_id": 3, "org_id": 13, "title": "新绛中学党委书记", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 县委常委、副县长
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "县政府党组成员"},
    # 县委常委、常务副县长
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": "县政府党组副书记"},
    {"person_id": 5, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "常务副县长，分管发展改革、财税、应急等"},
    # 纪委书记
    {"person_id": 6, "org_id": 3, "title": "县委常委、纪委书记、监委主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 政法委书记
    {"person_id": 7, "org_id": 4, "title": "县委常委、政法委书记", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 宣传部长
    {"person_id": 8, "org_id": 5, "title": "县委常委、宣传部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 组织部长
    {"person_id": 9, "org_id": 6, "title": "县委常委、组织部部长、县委党校校长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 人武部政委
    {"person_id": 10, "org_id": 8, "title": "县委常委、人武部政委", "start_date": "", "end_date": "", "rank": "副处级/上校", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 统战部长
    {"person_id": 11, "org_id": 7, "title": "县委常委、统战部部长、县政协党组副书记", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 开发区主任
    {"person_id": 12, "org_id": 9, "title": "县政府党组副书记、开发区党工委书记、管委会主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 副县长 张毅
    {"person_id": 13, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "县政府党组成员"},
    # 副县长 杨喆
    {"person_id": 14, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "县政府党组成员，负责工业、科技、生态环境等"},
    # 副县长 公安局长
    {"person_id": 15, "org_id": 10, "title": "副县长、公安局党委书记、局长、督察长", "start_date": "", "end_date": "", "rank": "副处级", "note": "县政府党组成员"},
    {"person_id": 15, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "县政府党组成员"},
    # 副县长 卢玉玉
    {"person_id": 16, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "县政府党组成员，分管文旅、教育、医疗等"},
    # 副县长 孙洪涛
    {"person_id": 17, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级", "note": "县政府党组成员，兼泽掌镇党委书记"},
    # 人大
    {"person_id": 18, "org_id": 11, "title": "县人大常委会党组书记、主任", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 19, "org_id": 11, "title": "县人大常委会副主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 20, "org_id": 11, "title": "县人大常委会党组成员、副主任候选人", "start_date": "", "end_date": "", "rank": "副处级", "note": "三级调研员"},
    {"person_id": 21, "org_id": 11, "title": "县人大常委会党组成员、副主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 22, "org_id": 11, "title": "县人大常委会党组成员、副主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 政协
    {"person_id": 23, "org_id": 12, "title": "县政协党组书记、主席", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 24, "org_id": 12, "title": "县政协党组副书记、副主席", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 25, "org_id": 12, "title": "县政协副主席", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 26, "org_id": 12, "title": "县政协党组成员、副主席", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 27, "org_id": 12, "title": "县政协副主席", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
]

# ========== RELATIONSHIPS ==========
# Note: Web access was limited — full career timelines not available to confirm overlap orgs.
# These relationships are based on current organizational overlap and shared leadership structures.

relationships = [
    # Core leadership team (confirmed overlap in county leadership)
    {"person_a": 1, "person_b": 2, "relationship_type": "superior_subordinate", "strength": "strong",
     "evidence": "县委书记与县长在中共新绛县委领导班子中共事", "overlap_org": "中共新绛县委员会",
     "overlap_period": "当前", "confidence": "confirmed", "source": URL_XWLD},
    {"person_a": 1, "person_b": 3, "relationship_type": "superior_subordinate", "strength": "strong",
     "evidence": "县委书记与县委副书记在县委领导班子共事", "overlap_org": "中共新绛县委员会",
     "overlap_period": "当前", "confidence": "confirmed", "source": URL_XWLD},
    {"person_a": 2, "person_b": 3, "relationship_type": "overlap", "strength": "strong",
     "evidence": "县长与县委副书记在县领导班子共事", "overlap_org": "中共新绛县委员会",
     "overlap_period": "当前", "confidence": "confirmed", "source": URL_XWLD},
    # Standing committee members all overlap in 县委
    {"person_a": 4, "person_b": 5, "relationship_type": "overlap", "strength": "strong",
     "evidence": "两位县委常委兼副县长在县政府党组和县委常委会共事", "overlap_org": "中共新绛县委员会",
     "overlap_period": "当前", "confidence": "confirmed", "source": URL_XWLD},
    # 纪委书记 with 县委书记
    {"person_a": 1, "person_b": 6, "relationship_type": "superior_subordinate", "strength": "strong",
     "evidence": "县委书记领导县纪委工作", "overlap_org": "中共新绛县委员会",
     "overlap_period": "当前", "confidence": "confirmed", "source": URL_XWLD},
    # 政法委书记 with 县长
    {"person_a": 2, "person_b": 7, "relationship_type": "overlap", "strength": "strong",
     "evidence": "县长与政法委书记在县委常委会共事", "overlap_org": "中共新绛县委员会",
     "overlap_period": "当前", "confidence": "confirmed", "source": URL_XWLD},
    # 组织部长 with 县委书记
    {"person_a": 1, "person_b": 9, "relationship_type": "superior_subordinate", "strength": "medium",
     "evidence": "县委书记领导县委组织部工作", "overlap_org": "中共新绛县委员会",
     "overlap_period": "当前", "confidence": "confirmed", "source": URL_XWLD},
    # 统战部长 (female, youngest) with other committee members
    {"person_a": 11, "person_b": 8, "relationship_type": "overlap", "strength": "medium",
     "evidence": "统战部长与宣传部长均为县委常委会成员", "overlap_org": "中共新绛县委员会",
     "overlap_period": "当前", "confidence": "confirmed", "source": URL_XWLD},
]

# ========== BUILD ==========

if __name__ == "__main__":
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

    # --- Generate Person JSONs for core leaders ---
    person_json_dir = PERSONS_DIR
    person_json_dir.mkdir(parents=True, exist_ok=True)

    core_figures = [
        {
            "person_id": "xinjiang_宋志江",
            "name": "宋志江",
            "role": "县委书记",
            "birth": "1971年2月",
            "gender": "男",
            "ethnicity": "汉族",
            "education": [{"institution": "中央党校", "degree": "大学", "study_type": "party_school"}],
            "party_join": "中共党员",
        },
        {
            "person_id": f"xinjiang_{'蒋锋'}",
            "name": "蒋锋",
            "role": "县长",
            "birth": "1984年3月",
            "gender": "男",
            "ethnicity": "汉族",
            "education": [{"institution": "省委党校", "degree": "研究生", "study_type": "party_school"}],
            "party_join": "中共党员",
        },
    ]

    for fig in core_figures:
        pid = f"xinjiang_{fig['name']}"
        pjson = {
            "schema_version": "1.0",
            "generated_at": TODAY,
            "investigation_scope": {
                "province": "山西省",
                "city": "运城市",
                "region": "新绛县",
                "job": fig["role"],
                "task_id": "shanxi_新绛县",
                "time_focus": "2026",
            },
            "identity": {
                "person_id": pid,
                "name": fig["name"],
                "gender": fig["gender"],
                "ethnicity": fig["ethnicity"],
                "birth": fig["birth"],
                "education": fig["education"],
                "party_join": fig["party_join"],
                "work_start": "",
                "dedupe_keys": {"name_birth": f"{fig['name']}_{fig['birth']}"},
            },
            "current_status": {
                "current_post": fig["role"],
                "current_org": "中共新绛县委员会" if "书记" in fig["role"] else "新绛县人民政府",
                "administrative_rank": "正处级",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001"]
            },
            "career_timeline": [
                {
                    "start": "未知",
                    "end": "当前",
                    "org": "新绛县",
                    "title": fig["role"],
                    "level": "正处级",
                    "location": "山西省运城市新绛县",
                    "confidence": "confirmed",
                    "note": "官方资料未提供完整履历；当前职务已确认",
                    "source_ids": ["S001"]
                }
            ],
            "organizations": [
                {"name": "中共新绛县委员会", "type": "党委", "role": "成员"},
                {"name": "新绛县人民政府", "type": "政府", "role": "领导"}
            ],
            "relationships": [],
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": ["地方党务/行政管理"],
                "secondary_specializations": [],
                "career_pattern": "未知",
                "systems_experience": ["党政"],
                "geographic_pattern": ["山西省"],
                "promotion_velocity": {"summary": "缺乏完整履历，无法评估", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "公开信息有限，无法推断工作风格"
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {
                    "type": "none_found",
                    "description": "截至2026年7月，公开信息中未发现该领导人涉及纪律处分或负面舆情",
                    "date": AS_OF,
                    "confidence": "unverified",
                    "source_ids": []
                }
            ],
            "source_register": [
                {
                    "id": "S001",
                    "title": "新绛县人民政府门户网站—领导之窗",
                    "url": f"https://www.jiangzhou.gov.cn/zfxxgk/fdzdgknr/ldzc/xwld/index.shtml?highlight={fig['name']}",
                    "publisher": "新绛县人民政府",
                    "published_at": AS_OF,
                    "accessed_at": AS_OF,
                    "source_type": "official",
                    "reliability": "high",
                    "notes": "县委领导页面，含个人简介照片和基本信息"
                }
            ],
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "low",
                "biggest_gap": "完整履历（前职、教育时段、入党时间、工作起始时间）"
            },
            "open_questions": [
                {
                    "priority": "critical",
                    "question": f"{fig['name']}的完整职业生涯履历（包括此前所有任职、晋升时间、教育背景时段）",
                    "why_it_matters": "缺少履历无法构建完整关系网络，无法识别与其他领导的连接点",
                    "suggested_queries": [f"{fig['name']} 简历", f"{fig['name']} 任前公示", f"{fig['name']} 运城"],
                    "last_attempted": AS_OF
                }
            ]
        }

        filename = f"{TODAY}-山西省-运城市-{fig['role']}-{fig['name']}.json"
        filepath = person_json_dir / filename
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(pjson, f, ensure_ascii=False, indent=2)
        print(f"  ✅ Person JSON: {filepath}")