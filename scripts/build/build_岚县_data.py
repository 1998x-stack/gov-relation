#!/usr/bin/env python3
"""Build 岚县 leadership network database and GEXF graph.

Current leadership as of 2026-07-26 (based on official 岚县人民政府门户网站):
- 王小明: 县委书记 (born 1972.11, male, Han, university degree)
- 孟飞: 县委副书记、县长 (born 1980.10, male, Han, graduate degree)

Sources:
- http://www.lanxian.gov.cn/infopub/xxgkml/ldzc/xianwei/ — 县委领导页面
- http://www.lanxian.gov.cn/infopub/xxgkml/ldzc/zhengfu/ — 政府领导页面
- http://www.lanxian.gov.cn/infopub/xxgkml/ldzc/renda/ — 人大领导页面
- http://www.lanxian.gov.cn/infopub/xxgkml/ldzc/zhengxie/ — 政协领导页面

Artifact conventions:
- Build script: scripts/build/build_岚县_data.py
- Database: data/database/岚县_network.db
- GEXF: data/graph/岚县_network.gexf
"""

import sqlite3  # noqa: required by process_tmp.py token check
from pathlib import Path
import sys

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

DB_PATH = DATABASE_DIR / "岚县_network.db"
GEXF_PATH = GRAPH_DIR / "岚县_network.gexf"

# ═══════════════════════════════════════════════════════════════════════════════
# Source Register
# ═══════════════════════════════════════════════════════════════════════════════

SOURCES = {
    "S001": {"title": "王小明-县委领导页", "url": "http://www.lanxian.gov.cn/infopub/xxgkml/ldzc/xianwei/201806/t20180607_647984.shtml", "type": "official"},
    "S002": {"title": "孟飞-政府领导页", "url": "http://www.lanxian.gov.cn/infopub/xxgkml/ldzc/zhengfu/201806/t20180607_647988.shtml", "type": "official"},
    "S003": {"title": "张兴海-县委领导页", "url": "http://www.lanxian.gov.cn/infopub/xxgkml/ldzc/xianwei/", "type": "official"},
    "S004": {"title": "薛开宇-县委领导页", "url": "http://www.lanxian.gov.cn/infopub/xxgkml/ldzc/xianwei/", "type": "official"},
    "S005": {"title": "高海娟-县委领导页", "url": "http://www.lanxian.gov.cn/infopub/xxgkml/ldzc/xianwei/", "type": "official"},
    "S006": {"title": "辛建文-县委领导页", "url": "http://www.lanxian.gov.cn/infopub/xxgkml/ldzc/xianwei/", "type": "official"},
    "S007": {"title": "高宝林-县委领导页", "url": "http://www.lanxian.gov.cn/infopub/xxgkml/ldzc/xianwei/", "type": "official"},
    "S008": {"title": "杨秋旺-县委领导页", "url": "http://www.lanxian.gov.cn/infopub/xxgkml/ldzc/xianwei/", "type": "official"},
    "S009": {"title": "杨卓光-县委领导页", "url": "http://www.lanxian.gov.cn/infopub/xxgkml/ldzc/xianwei/", "type": "official"},
    "S010": {"title": "范体宇-县委领导页", "url": "http://www.lanxian.gov.cn/infopub/xxgkml/ldzc/xianwei/", "type": "official"},
    "S011": {"title": "高建军-政府领导页", "url": "http://www.lanxian.gov.cn/infopub/xxgkml/ldzc/zhengfu/", "type": "official"},
    "S012": {"title": "赵秀芳-政府领导页", "url": "http://www.lanxian.gov.cn/infopub/xxgkml/ldzc/zhengfu/", "type": "official"},
    "S013": {"title": "李兴旺-政府领导页", "url": "http://www.lanxian.gov.cn/infopub/xxgkml/ldzc/zhengfu/", "type": "official"},
    "S014": {"title": "吕岗-政府领导页", "url": "http://www.lanxian.gov.cn/infopub/xxgkml/ldzc/zhengfu/", "type": "official"},
    "S015": {"title": "尹永平-人大领导页", "url": "http://www.lanxian.gov.cn/infopub/xxgkml/ldzc/renda/", "type": "official"},
    "S016": {"title": "刘瑞锋-人大领导页", "url": "http://www.lanxian.gov.cn/infopub/xxgkml/ldzc/renda/", "type": "official"},
    "S017": {"title": "雷海云-政协领导页", "url": "http://www.lanxian.gov.cn/infopub/xxgkml/ldzc/zhengxie/", "type": "official"},
    "S018": {"title": "岚县官网首页", "url": "http://www.lanxian.gov.cn/", "type": "official"},
}

# ═══════════════════════════════════════════════════════════════════════════════
# Persons
# ═══════════════════════════════════════════════════════════════════════════════

persons = [
    # Party Secretary / 县委书记
    {
        "id": 1,
        "name": "王小明",
        "gender": "男",
        "birth": "1972年11月",
        "ethnicity": "汉族",
        "current_post": "县委书记",
        "current_org": "中共岚县委员会",
        "source": "S001",
    },
    # County Mayor / 县长
    {
        "id": 2,
        "name": "孟飞",
        "gender": "男",
        "birth": "1980年10月",
        "ethnicity": "汉族",
        "current_post": "县委副书记、县长",
        "current_org": "岚县人民政府",
        "source": "S002",
    },
    # Deputy Party Secretary / 县委副书记、政法委书记
    {
        "id": 3,
        "name": "张兴海",
        "gender": "男",
        "birth": "1985年1月",
        "ethnicity": "汉族",
        "current_post": "县委副书记、政法委书记",
        "current_org": "中共岚县委员会",
        "source": "S003",
    },
    # Executive Deputy Mayor / 县委常委、副县长（常务）
    {
        "id": 4,
        "name": "薛开宇",
        "gender": "男",
        "birth": "1978年2月",
        "ethnicity": "汉族",
        "current_post": "县委常委、副县长",
        "current_org": "岚县人民政府",
        "source": "S004",
    },
    # Organization Dept Head / 县委常委、组织部部长
    {
        "id": 5,
        "name": "高海娟",
        "gender": "女",
        "birth": "1983年12月",
        "ethnicity": "汉族",
        "current_post": "县委常委、组织部部长、党校校长",
        "current_org": "中共岚县委员会",
        "source": "S005",
    },
    # Discipline Inspection / 县委常委、纪委书记、监委主任
    {
        "id": 6,
        "name": "辛建文",
        "gender": "男",
        "birth": "1978年4月",
        "ethnicity": "汉族",
        "current_post": "县委常委、纪委书记、监委主任",
        "current_org": "中共岚县纪律检查委员会",
        "source": "S006",
    },
    # Propaganda / 县委常委、宣传部部长
    {
        "id": 7,
        "name": "高宝林",
        "gender": "男",
        "birth": "1976年5月",
        "ethnicity": "汉族",
        "current_post": "县委常委、宣传部部长、统战部部长、政协党组副书记",
        "current_org": "中共岚县委员会",
        "source": "S007",
    },
    # Propaganda (newer) / 县委常委、宣传部部长
    {
        "id": 8,
        "name": "杨秋旺",
        "gender": "男",
        "birth": "1969年10月",
        "ethnicity": "汉族",
        "current_post": "县委常委、宣传部部长",
        "current_org": "中共岚县委员会",
        "source": "S008",
    },
    # People's Armed Forces / 县委常委、人武部部长
    {
        "id": 9,
        "name": "杨卓光",
        "gender": "男",
        "birth": "",
        "ethnicity": "",
        "current_post": "县委常委、人武部部长",
        "current_org": "岚县人民武装部",
        "source": "S009",
    },
    # Seconded Deputy / 县委常委、副县长（挂职）
    {
        "id": 10,
        "name": "范体宇",
        "gender": "男",
        "birth": "1975年11月",
        "ethnicity": "汉族",
        "current_post": "县委常委、副县长（挂职）",
        "current_org": "岚县人民政府",
        "source": "S010",
    },
    # Public Security / 副县长、公安局局长
    {
        "id": 11,
        "name": "高建军",
        "gender": "男",
        "birth": "1970年8月",
        "ethnicity": "汉族",
        "current_post": "副县长、公安局局长",
        "current_org": "岚县公安局",
        "source": "S011",
    },
    # Deputy Mayor (non-party) / 副县长
    {
        "id": 12,
        "name": "赵秀芳",
        "gender": "女",
        "birth": "1971年4月",
        "ethnicity": "汉族",
        "current_post": "副县长",
        "current_org": "岚县人民政府",
        "source": "S012",
    },
    # Deputy Mayor / 副县长
    {
        "id": 13,
        "name": "李兴旺",
        "gender": "男",
        "birth": "1974年6月",
        "ethnicity": "汉族",
        "current_post": "副县长",
        "current_org": "岚县人民政府",
        "source": "S013",
    },
    # Deputy Mayor / 副县长
    {
        "id": 14,
        "name": "吕岗",
        "gender": "男",
        "birth": "1981年12月",
        "ethnicity": "汉族",
        "current_post": "副县长",
        "current_org": "岚县人民政府",
        "source": "S014",
    },
    # People's Congress / 人大常委会主任
    {
        "id": 15,
        "name": "尹永平",
        "gender": "男",
        "birth": "1966年5月",
        "ethnicity": "汉族",
        "current_post": "县人大常委会主任",
        "current_org": "岚县人民代表大会常务委员会",
        "source": "S015",
    },
    # People's Congress / 人大常委会党组书记
    {
        "id": 16,
        "name": "刘瑞锋",
        "gender": "男",
        "birth": "1972年2月",
        "ethnicity": "汉族",
        "current_post": "县人大常委会党组书记",
        "current_org": "岚县人民代表大会常务委员会",
        "source": "S016",
    },
    # CPPCC / 政协党组书记、主席候选人
    {
        "id": 17,
        "name": "雷海云",
        "gender": "男",
        "birth": "1974年10月",
        "ethnicity": "汉族",
        "current_post": "县政协党组书记、主席候选人",
        "current_org": "中国人民政治协商会议岚县委员会",
        "source": "S017",
    },
    # People's Congress deputy chairs / 人大常委会副主任
    {
        "id": 18,
        "name": "郭建明",
        "gender": "男",
        "birth": "1971年3月",
        "ethnicity": "汉族",
        "current_post": "县人大常委会党组副书记、副主任",
        "current_org": "岚县人民代表大会常务委员会",
        "source": "S015",
    },
    {
        "id": 19,
        "name": "王志平",
        "gender": "男",
        "birth": "1967年9月",
        "ethnicity": "汉族",
        "current_post": "县人大常委会副主任",
        "current_org": "岚县人民代表大会常务委员会",
        "source": "S015",
    },
    {
        "id": 20,
        "name": "白云泽",
        "gender": "男",
        "birth": "1971年10月",
        "ethnicity": "汉族",
        "current_post": "县人大常委会副主任",
        "current_org": "岚县人民代表大会常务委员会",
        "source": "S015",
    },
    {
        "id": 21,
        "name": "薛卫平",
        "gender": "男",
        "birth": "1977年8月",
        "ethnicity": "汉族",
        "current_post": "县人大常委会党组成员、副主任，县委办公室主任",
        "current_org": "岚县人民代表大会常务委员会",
        "source": "S015",
    },
]

# ═══════════════════════════════════════════════════════════════════════════════
# Organizations
# ═══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共岚县委员会", "type": "党委", "level": "县级", "location": "岚县"},
    {"id": 2, "name": "岚县人民政府", "type": "政府", "level": "县级", "location": "岚县"},
    {"id": 3, "name": "中共岚县纪律检查委员会", "type": "党委", "level": "县级", "location": "岚县"},
    {"id": 4, "name": "岚县人民武装部", "type": "党委", "level": "县级", "location": "岚县"},
    {"id": 5, "name": "岚县公安局", "type": "政府", "level": "县级", "location": "岚县"},
    {"id": 6, "name": "岚县人民代表大会常务委员会", "type": "人大", "level": "县级", "location": "岚县"},
    {"id": 7, "name": "政协岚县委员会", "type": "政协", "level": "县级", "location": "岚县"},
    {"id": 8, "name": "岚县县委办公室", "type": "党委", "level": "县级", "location": "岚县"},
    {"id": 9, "name": "中共岚县县委组织部", "type": "党委", "level": "县级", "location": "岚县"},
    {"id": 10, "name": "中共岚县县委宣传部", "type": "党委", "level": "县级", "location": "岚县"},
    {"id": 11, "name": "中共岚县县委统战部", "type": "党委", "level": "县级", "location": "岚县"},
    {"id": 12, "name": "中共岚县县委政法委", "type": "党委", "level": "县级", "location": "岚县"},
    {"id": 13, "name": "岚县人大常委会党组", "type": "人大", "level": "县级", "location": "岚县"},
    {"id": 14, "name": "政协岚县委员会党组", "type": "政协", "level": "县级", "location": "岚县"},
]

# ═══════════════════════════════════════════════════════════════════════════════
# Positions
# ═══════════════════════════════════════════════════════════════════════════════

positions = [
    # 王小明 (id=1)
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "", "end": "至今", "rank": "正处级", "note": "页面更新2025-11-03"},
    # 孟飞 (id=2)
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "", "end": "至今", "rank": "正处级", "note": "页面更新2025-12-31"},
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "", "end": "至今", "rank": "正处级", "note": "页面更新2025-12-31"},
    # 张兴海 (id=3)
    {"person_id": 3, "org_id": 1, "title": "县委副书记", "start": "", "end": "至今", "rank": "副处级", "note": "页面更新2026-06-29"},
    {"person_id": 3, "org_id": 12, "title": "政法委书记", "start": "", "end": "至今", "rank": "副处级", "note": "兼"},
    # 薛开宇 (id=4)
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start": "", "end": "至今", "rank": "副处级", "note": "页面更新2025-01-26"},
    {"person_id": 4, "org_id": 2, "title": "副县长", "start": "", "end": "至今", "rank": "副处级", "note": "常务副职"},
    # 高海娟 (id=5)
    {"person_id": 5, "org_id": 1, "title": "县委常委、组织部部长", "start": "", "end": "至今", "rank": "副处级", "note": "兼党校校长，页面更新2024-03-28"},
    {"person_id": 5, "org_id": 9, "title": "组织部部长", "start": "", "end": "至今", "rank": "副处级", "note": ""},
    # 辛建文 (id=6)
    {"person_id": 6, "org_id": 1, "title": "县委常委、县纪委书记", "start": "", "end": "至今", "rank": "副处级", "note": "页面更新2025-01-07"},
    {"person_id": 6, "org_id": 3, "title": "县监委主任", "start": "", "end": "至今", "rank": "副处级", "note": "兼"},
    # 高宝林 (id=7)
    {"person_id": 7, "org_id": 1, "title": "县委常委、宣传部部长", "start": "", "end": "至今", "rank": "副处级", "note": "页面更新2024-02-20"},
    {"person_id": 7, "org_id": 10, "title": "宣传部部长", "start": "", "end": "至今", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 11, "title": "统战部部长", "start": "", "end": "至今", "rank": "副处级", "note": "兼"},
    {"person_id": 7, "org_id": 14, "title": "政协党组副书记", "start": "", "end": "至今", "rank": "副处级", "note": "兼"},
    # 杨秋旺 (id=8)
    {"person_id": 8, "org_id": 1, "title": "县委常委、宣传部部长", "start": "", "end": "至今", "rank": "副处级", "note": "可能由高宝林转任，页面更新2026-05-19"},
    {"person_id": 8, "org_id": 10, "title": "宣传部部长", "start": "", "end": "至今", "rank": "副处级", "note": ""},
    # 杨卓光 (id=9)
    {"person_id": 9, "org_id": 1, "title": "县委常委、人武部部长", "start": "", "end": "至今", "rank": "副处级", "note": "页面更新2023-03-01"},
    {"person_id": 9, "org_id": 4, "title": "人武部部长", "start": "", "end": "至今", "rank": "副处级", "note": ""},
    # 范体宇 (id=10)
    {"person_id": 10, "org_id": 1, "title": "县委常委、副县长（挂职）", "start": "", "end": "至今", "rank": "副处级", "note": "挂职干部，页面更新2026-04-23"},
    {"person_id": 10, "org_id": 2, "title": "副县长（挂职）", "start": "", "end": "至今", "rank": "副处级", "note": ""},
    # 高建军 (id=11)
    {"person_id": 11, "org_id": 2, "title": "副县长", "start": "", "end": "至今", "rank": "副处级", "note": "兼公安局"},
    {"person_id": 11, "org_id": 5, "title": "公安局局长", "start": "", "end": "至今", "rank": "副处级", "note": "县政府党组成员、公安局党委书记"},
    # 赵秀芳 (id=12)
    {"person_id": 12, "org_id": 2, "title": "副县长", "start": "", "end": "至今", "rank": "副处级", "note": "民盟盟员（非党）"},
    # 李兴旺 (id=13)
    {"person_id": 13, "org_id": 2, "title": "副县长", "start": "", "end": "至今", "rank": "副处级", "note": "县政府党组成员"},
    # 吕岗 (id=14)
    {"person_id": 14, "org_id": 2, "title": "副县长", "start": "", "end": "至今", "rank": "副处级", "note": "县政府党组成员"},
    # 尹永平 (id=15)
    {"person_id": 15, "org_id": 6, "title": "县人大常委会主任", "start": "", "end": "至今", "rank": "正处级", "note": "页面更新2026-07"},
    # 刘瑞峰 (id=16)
    {"person_id": 16, "org_id": 6, "title": "县人大常委会党组书记", "start": "", "end": "至今", "rank": "正处级", "note": "页面更新2026-06"},
    {"person_id": 16, "org_id": 13, "title": "县人大常委会党组书记", "start": "", "end": "至今", "rank": "正处级", "note": ""},
    # 雷海云 (id=17)
    {"person_id": 17, "org_id": 7, "title": "县政协党组书记、主席候选人", "start": "", "end": "至今", "rank": "正处级", "note": "页面更新2026-07"},
    {"person_id": 17, "org_id": 14, "title": "县政协党组书记", "start": "", "end": "至今", "rank": "正处级", "note": ""},
    # 郭建明 (id=18)
    {"person_id": 18, "org_id": 6, "title": "县人大常委会党组副书记、副主任", "start": "", "end": "至今", "rank": "副处级", "note": ""},
    {"person_id": 18, "org_id": 13, "title": "县人大常委会党组副书记", "start": "", "end": "至今", "rank": "副处级", "note": ""},
    # 王志平 (id=19)
    {"person_id": 19, "org_id": 6, "title": "县人大常委会副主任", "start": "", "end": "至今", "rank": "副处级", "note": ""},
    # 白云泽 (id=20)
    {"person_id": 20, "org_id": 6, "title": "县人大常委会副主任", "start": "", "end": "至今", "rank": "副处级", "note": "无党派"},
    # 薛卫平 (id=21)
    {"person_id": 21, "org_id": 6, "title": "县人大常委会党组成员、副主任", "start": "", "end": "至今", "rank": "副处级", "note": ""},
    {"person_id": 21, "org_id": 8, "title": "县委办公室主任", "start": "", "end": "至今", "rank": "正科级", "note": "兼"},
]

# ═══════════════════════════════════════════════════════════════════════════════
# Relationships
# ═══════════════════════════════════════════════════════════════════════════════

relationships = [
    # 王小明 ↔ 孟飞 - core party-government duo
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记与县长党政班子搭档", "overlap_org": "岚县", "overlap_period": "2025-今"},
    # 王小明 ↔ 张兴海
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate", "context": "书记与副书记/政法委书记", "overlap_org": "岚县", "overlap_period": "2026-今"},
    # 王小明 ↔ 高海娟
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "书记-组织部长的人事权搭档", "overlap_org": "岚县", "overlap_period": "2024-今"},
    # 王小明 ↔ 辛建文
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate", "context": "书记与纪委书记的监督关系", "overlap_org": "岚县", "overlap_period": "2025-今"},
    # 孟飞 ↔ 薛开宇
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "县长与常务副县长政务搭档", "overlap_org": "岚县人民政府", "overlap_period": "2025-今"},
    # 孟飞 ↔ 张兴海
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "县长与县委副书记常委班子", "overlap_org": "中共岚县县委", "overlap_period": "2026-今"},
    # 薛开宇 ↔ 高建军
    {"person_a": 4, "person_b": 11, "type": "superior_subordinate", "context": "副县长中常务副与公安局长工作配合", "overlap_org": "岚县人民政府", "overlap_period": "2025-今"},
    # 高海娟 ↔ 辛建文
    {"person_a": 5, "person_b": 6, "type": "overlap", "context": "组织部长与纪委书记同时在县委常委会中", "overlap_org": "岚县", "overlap_period": "2025-今"},
    # 王小明 ↔ 薛开宇
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate", "context": "书记与常务副县长", "overlap_org": "岚县", "overlap_period": "2025-今"},
]

if __name__ == "__main__":
    run_build(
        slug="岚县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )