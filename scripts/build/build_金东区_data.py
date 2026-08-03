#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 金东区 (Jindong District, Zhejiang) leadership network.

归口地区: 浙江省金华市金东区（金义新区）
数据来源:
- 金东区人民政府网站 (jindong.gov.cn) — 区领导及分工页面，2026年8月确认
- Baidu Baike — 部分领导人简历 (有限访问)
- 金华市相关任免公告
数据时效：2026-08-03
"""

import os
import sqlite3
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "金东区"
PROVINCE = "浙江省"
PARENT_CITY = "金华市"
TODAY = "2026-08-03"

DB_PATH = DATABASE_DIR / f"{SLUG}_network.db"
GEXF_PATH = GRAPH_DIR / f"{SLUG}_network.gexf"

# ═══════════════════════════════════════════════════════════════════════════
# DATA — hardcoded research data
# Sources: Official 金东区人民政府网站 (jindong.gov.cn), 金华市人民政府网站
# ═══════════════════════════════════════════════════════════════════════════

persons = [
    # ── 区委书记（当前） ──
    {
        "id": 1,
        "name": "黄国钧",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "新区党工委书记、管委会主任，区委书记",
        "current_org": "中共金华市金东区委员会",
        "source": "https://www.jindong.gov.cn/col/col1229412571/index.html",
    },
    # ── 区长（当前） ──
    {
        "id": 2,
        "name": "蒋涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委副书记、区长，新区党工委副书记、管委会副主任",
        "current_org": "金东区人民政府",
        "source": "https://www.jindong.gov.cn/col/col1229412572/index.html",
    },
    # ── 前任区委书记 ──
    {
        "id": 3,
        "name": "张群环",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "约1974年",
        "birthplace": "推测：浙江金东",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "曾为金东区委书记（前任兰溪市委书记、永康市长）",
        "current_org": "中共金华市金东区委员会（曾任职）",
        "source": "兰溪市网络数据/永康市网络数据",
    },
    # ── 区委副书记 ──
    {
        "id": 4,
        "name": "陈春梅",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委副书记、社会工作部部长、政法委书记，金党工委副书记",
        "current_org": "中共金华市金东区委员会",
        "source": "https://www.jindong.gov.cn/col/col1229617244/index.html",
    },
    # ── 常务副区长 ──
    {
        "id": 5,
        "name": "陈旭锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委、常务副区长，金党工委委员、管委会副主任",
        "current_org": "金东区人民政府",
        "source": "https://www.jindong.gov.cn/col/col1229617245/index.html",
    },
    # ── 统战部长 ──
    {
        "id": 6,
        "name": "周咸超",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委、统战部部长，金党工委委员",
        "current_org": "中共金华市金东区委员会",
        "source": "https://www.jindong.gov.cn/col/col1229412579/index.html",
    },
    # ── 纪委书记 ──
    {
        "id": 7,
        "name": "厉光明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委、纪委书记、监委主任，金党工委委员、纪检监察工委书记",
        "current_org": "中共金华市金东区纪委/区监委",
        "source": "https://www.jindong.gov.cn/col/col1229515017/index.html",
    },
    # ── 宣传部长 ──
    {
        "id": 8,
        "name": "华刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委、宣传部部长，金党工委委员",
        "current_org": "中共金华市金东区委员会",
        "source": "https://www.jindong.gov.cn/col/col1229412581/index.html",
    },
    # ── 区政府党组成员 ──
    {
        "id": 9,
        "name": "吴晓辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委、区政府党组成员，金党工委委员",
        "current_org": "金东区人民政府",
        "source": "https://www.jindong.gov.cn/col/col1229617246/index.html",
    },
    # ── 人武部政委 ──
    {
        "id": 10,
        "name": "秦成业",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委、人武部政委，金党工委委员",
        "current_org": "金华市金东区人民武装部",
        "source": "https://www.jindong.gov.cn/col/col1229412576/index.html",
    },
    # ── 组织部长 ──
    {
        "id": 11,
        "name": "李轶玮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委、组织部部长，金党工委委员",
        "current_org": "中共金华市金东区委组织部",
        "source": "https://www.jindong.gov.cn/col/col1229617247/index.html",
    },
    # ── 副区长(常委兼) ──
    {
        "id": 12,
        "name": "潘钢刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "区委常委、副区长，金党工委委员、管委会副主任",
        "current_org": "金东区人民政府",
        "source": "https://www.jindong.gov.cn/col/col1229865786/index.html",
    },
    # ── 副区长(周斌) ──
    {
        "id": 13,
        "name": "周斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "金党工委委员、管委会副主任，副区长",
        "current_org": "金东区人民政府",
        "source": "https://www.jindong.gov.cn/col/col1229412580/index.html",
    },
    # ── 金办党委委员 ──
    {
        "id": 14,
        "name": "舒跃成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "金党工委委员、管委会副主任，孝顺镇党委书记",
        "current_org": "金华市金东区孝顺镇",
        "source": "https://www.jindong.gov.cn/col/col1229865787/index.html",
    },
    # ── 金办管委会副主任 (吴晨飞，援川) ──
    {
        "id": 15,
        "name": "吴晨飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "金党工委委员、管委会副主任（援川）",
        "current_org": "四川丹巴",
        "source": "https://www.jindong.gov.cn/col/col1229865788/index.html",
    },
    # ── 挂职副区长(史策) ──
    {
        "id": 16,
        "name": "史策",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共员",
        "work_start": "待查",
        "current_post": "金党工委委员、管委会副主任，副区长（挂职）",
        "current_org": "金东区人民政府",
        "source": "https://www.jindong.gov.cn/col/col1229398162/sc/index.html",
    },
    # ── 金党工委委员(陶晓锋) ──
    {
        "id": 17,
        "name": "陶晓锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共员",
        "work_start": "待查",
        "current_post": "金党工委委员",
        "current_org": "金华市金义新区党工委",
        "source": "https://www.jindong.gov.cn/col/col1229865789/index.html",
    },
    # ── 副区长(郑攀) ──
    {
        "id": 18,
        "name": "郑攀",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副区长，金管委会副主任",
        "current_org": "金东区人民政府",
        "source": "https://www.jindong.gov.cn/col/col1229865791/index.html",
    },
    # ── 副区长(孙斌，公安) ──
    {
        "id": 19,
        "name": "孙斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副区长、区公安分局局长，金管委会副主任",
        "current_org": "金华市公安局金东区分局",
        "source": "https://www.jindong.gov.cn/col/col1229865790/index.html",
    },
    # ── 副区长(黄泽文) ──
    {
        "id": 20,
        "name": "黄泽文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副区长，金管委会副主任",
        "current_org": "金东区人民政府",
        "source": "https://www.jindong.gov.cn/col/col1229398162/hzw/index.html",
    },
    # ── 副区长(朱刚露) ──
    {
        "id": 21,
        "name": "朱刚露",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "副区长，金管委会副主任",
        "current_org": "金东区人民政府",
        "source": "https://www.jindong.gov.cn/col/col1229865792/index.html",
    },
]

organizations = [
    {"id": 1, "name": "中共金华市金东区委员会", "type": "党委", "level": "县级", "parent": "中共金华市委员会", "location": PROVINCE},
    {"id": 2, "name": "金东区人民政府", "type": "政府", "level": "县级", "parent": "中共金华市委员会", "location": PROVINCE},
    {"id": 3, "name": "金华市金义新区党工委", "type": "党委", "level": "县级", "parent": "中共金华市委员会", "location": PROVINCE},
    {"id": 4, "name": "金华市金义新区管委会", "type": "政府", "level": "县级", "parent": "中共金华市委员会", "location": PROVINCE},
    {"id": 5, "name": "中共金华市金东区委组织部", "type": "党委", "level": "县级", "parent": "中共金华市金东区委员会", "location": PROVINCE},
    {"id": 6, "name": "中共金华市金东区纪委/区监委", "type": "党委", "level": "县级", "parent": "中共金华市金东区委员会", "location": PROVINCE},
    {"id": 7, "name": "中共金华市金东区委统战部", "type": "党委", "level": "县级", "parent": "中共金华市金东区委员会", "location": PROVINCE},
    {"id": 8, "name": "中共金华市金东区委宣传部", "type": "党委", "level": "县级", "parent": "中共金华市金东区委员会", "location": PROVINCE},
    {"id": 9, "name": "中共金华市金东区委政法委员会", "type": "党委", "level": "县级", "parent": "中共金华市金东区委员会", "location": PROVINCE},
    {"id": 10, "name": "金华市金东区人民武装部", "type": "事业单位", "level": "县级", "parent": "金华军分区", "location": PROVINCE},
    {"id": 11, "name": "金华市公安局金东区分局", "type": "政府", "level": "县级", "parent": "金华市公安局", "location": PROVINCE},
    {"id": 12, "name": "金华市金东区孝顺镇", "type": "乡镇/街道", "level": "乡镇级", "parent": "金东区人民政府", "location": PROVINCE},
    {"id": 13, "name": "中共金华市委员会", "type": "党委", "level": "地市级", "parent": "中共浙江省委员会", "location": PROVINCE},
    {"id": 14, "name": "中共兰溪市委员会", "type": "党委", "level": "县级", "parent": "中共金华市委员会", "location": PROVINCE},
]

positions = [
    # ── 黄国钧 ──
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "待查", "end_date": "至今", "rank": "正处级"},
    {"person_id": 1, "org_id": 3, "title": "金义新区党工委书记", "start_date": "待查", "end_date": "至今", "rank": "正处级"},
    {"person_id": 1, "org_id": 4, "title": "金义新区管委会主任", "start_date": "待查", "end_date": "至今", "rank": "正处级"},
    # ── 蒋涛 ──
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "待查", "end_date": "至今", "rank": "正处级"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "待查", "end_date": "至今", "rank": "正处级"},
    {"person_id": 2, "org_id": 4, "title": "金管委会副主任", "start_date": "待查", "end_date": "至今", "rank": "正处级"},
    {"person_id": 2, "org_id": 3, "title": "金党工委副书记", "start_date": "待查", "end_date": "至今", "rank": "正处级"},
    # ── 张群环（前任区委书记） ──
    {"person_id": 3, "org_id": 1, "title": "区委书记（前任）", "start_date": "估计2023前", "end_date": "约2023-2024", "rank": "正处级"},
    {"person_id": 3, "org_id": 14, "title": "市委书记（兰溪前任）", "start_date": "约2021", "end_date": "约2023", "rank": "正处级"},
    # ── 陈春梅 ──
    {"person_id": 4, "org_id": 1, "title": "区委副书记", "start_date": "待查", "end_date": "至今", "rank": "副处级"},
    {"person_id": 4, "org_id": 9, "title": "政法书记", "start_date": "待查", "end_date": "至今", "rank": "副处级"},
    {"person_id": 4, "org_id": 3, "title": "金党工委副书记", "start_date": "待查", "end_date": "至今", "rank": "副处级"},
    # ── 陈旭锋 ──
    {"person_id": 5, "org_id": 1, "title": "区委常委", "start_date": "待查", "end_date": "至今", "rank": "副处级"},
    {"person_id": 5, "org_id": 2, "title": "常务副区长", "start_date": "待查", "end_date": "至今", "rank": "副处级"},
    {"person_id": 5, "org_id": 4, "title": "金管委会副主任", "start_date": "待查", "end_date": "至今", "rank": "副处级"},
    # ── 周咸超 ──
    {"person_id": 6, "org_id": 1, "title": "区委常委", "start_date": "待查", "end_date": "至今", "rank": "副处级"},
    {"person_id": 6, "org_id": 7, "title": "统战部部长", "start_date": "待查", "end_date": "至今", "rank": "副处级"},
    # ── 厉光明 ──
    {"person_id": 7, "org_id": 1, "title": "区委常委", "start_date": "待查", "end_date": "至今", "rank": "副处级"},
    {"person_id": 7, "org_id": 6, "title": "纪委书记、监委主任", "start_date": "待查", "end_date": "至今", "rank": "副处级"},
    {"person_id": 7, "org_id": 3, "title": "金纪检监察工委书记", "start_date": "待查", "end_date": "至今", "rank": "副处级"},
    # ── 华刚 ──
    {"person_id": 8, "org_id": 1, "title": "区委常委", "start_date": "待查", "end_date": "至今", "rank": "副处级"},
    {"person_id": 8, "org_id": 8, "title": "宣传部部长", "start_date": "待查", "end_date": "至今", "rank": "副处级"},
    # ── 吴晓辉 ──
    {"person_id": 9, "org_id": 1, "title": "区委常委", "start_date": "待查", "end_date": "至今", "rank": "副处级"},
    {"person_id": 9, "org_id": 2, "title": "区政府党组成员", "start_date": "待查", "end_date": "至今", "rank": "副处级"},
    # ── 秦成业 ──
    {"person_id": 10, "org_id": 1, "title": "区委常委", "start_date": "待查", "end_date": "至今", "rank": "副处级"},
    {"person_id": 10, "org_id": 10, "title": "人武部政委", "start_date": "待查", "end_date": "至今", "rank": "副处级"},
    # ── 李轶玮 ──
    {"person_id": 11, "org_id": 1, "title": "区委常委", "start_date": "待查", "end_date": "至今", "rank": "副处级"},
    {"person_id": 11, "org_id": 5, "title": "组织部部长", "start_date": "待查", "end_date": "至今", "rank": "副处级"},
    # ── 潘钢刚 ──
    {"person_id": 12, "org_id": 1, "title": "区委常委", "start_date": "待查", "end_date": "至今", "rank": "副处级"},
    {"person_id": 12, "org_id": 2, "title": "副区长", "start_date": "待查", "end_date": "至今", "rank": "副处级"},
    {"person_id": 12, "org_id": 4, "title": "金管委会副主任", "start_date": "待查", "end_date": "至今", "rank": "副处级"},
    # ── 周斌 ──
    {"person_id": 13, "org_id": 2, "title": "副区长（挂职）", "start_date": "待查", "end_date": "至今", "rank": "副处级"},
    {"person_id": 13, "org_id": 4, "title": "金管委会副主任", "start_date": "待查", "end_date": "至今", "rank": "副处级"},
    # ── 舒跃成 ──
    {"person_id": 14, "org_id": 12, "title": "孝顺镇党委书记", "start_date": "待查", "end_date": "至今", "rank": "正科级"},
    # ── 郑攀 ──
    {"person_id": 18, "org_id": 2, "title": "副区长", "start_date": "待查", "end_date": "至今", "rank": "副处级"},
    {"person_id": 18, "org_id": 4, "title": "金管委会副主任", "start_date": "待查", "end_date": "至今", "rank": "副处级"},
    # ── 孙斌 ──
    {"person_id": 19, "org_id": 2, "title": "副区长", "start_date": "待查", "end_date": "至今", "rank": "副处级"},
    {"person_id": 19, "org_id": 11, "title": "区公安分局局长", "start_date": "待查", "end_date": "至今", "rank": "副处级"},
    # ── 黄泽文 ──
    {"person_id": 20, "org_id": 2, "title": "副区长", "start_date": "待查", "end_date": "至今", "rank": "副处级"},
    {"person_id": 20, "org_id": 4, "title": "金管委会副主任", "start_date": "待查", "end_date": "至今", "rank": "副处级"},
    # ── 朱刚露 ──
    {"person_id": 21, "org_id": 2, "title": "副区长", "start_date": "待查", "end_date": "至今", "rank": "副处级"},
    {"person_id": 21, "org_id": 4, "title": "金管委会副主任", "start_date": "待查", "end_date": "至今", "rank": "副处级"},
]

relationships = [
    # ── 黄国钧与蒋涛（党政搭档） ──
    {
        "person_a": 1,
        "person_b": 2,
        "type": "superior_subordinate",
        "context": "金东区党政主要领导搭档（区委书记与区长）",
        "overlap_org": "中共金华市金东区委员会/金东区人民政府",
        "overlap_period": "至今",
    },
    # ── 黄氏与陈春梅（区委书记-副书记） ──
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "区委书记与区委副书记搭档", "overlap_org": "中共金华市金东区委员会",
     "overlap_period": "至今"},
    # ── 黄蒋与陈旭锋（书记-常务副区长） ──
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "区委书记与常委/常务副区长", "overlap_org": "中共金华市金东区委员会",
     "overlap_period": "至今"},
    # ── 黄与周咸超（书记-统战部长） ──
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "区委书记与统战部长", "overlap_org": "中共金华市金东区委员会",
     "overlap_period": "至今"},
    # ── 黄与厉光明（书记-纪委书记） ──
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate",
     "context": "区委书记与纪委书记", "overlap_org": "中共金华市金东区委员会",
     "overlap_period": "至今"},
    # ── 黄与华刚（书记-宣传部长） ──
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate",
     "context": "区委书记与宣传部长", "overlap_org": "中共金华市金东区委员会",
     "overlap_period": "至今"},
    # ── 黄与吴晓辉 ──
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate",
     "context": "区委书记与区委常委/政府党组成员", "overlap_org": "中共金华市金东区委员会",
     "overlap_period": "至今"},
    # ── 黄与秦成业 ──
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate",
     "context": "区委书记与人武部政委", "overlap_org": "中共金华市金东区委员会",
     "overlap_period": "至今"},
    # ── 黄与李轶玮（书记-组织部长） ──
    {"person_a": 1, "person_b": 11, "type": "superior_subordinate",
     "context": "区委书记与组织部长", "overlap_org": "中共金华市金东区委员会",
     "overlap_period": "至今"},
    # ── 黄与潘钢刚 ──
    {"person_a": 1, "person_b": 12, "type": "superior_subordinate",
     "context": "区委书记与常委副区长", "overlap_org": "中共金华市金东区委员会",
     "overlap_period": "至今"},
    # ── 黄国钧与张群环 ──
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor",
     "context": "黄国钧接替张群环任金东区委书记(推测)", "overlap_org": "中共金华市金东区委员会",
     "overlap_period": "约2023-2024"},
    # ── 蒋涛-陈旭锋 ──
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate",
     "context": "区长与常务副区长", "overlap_org": "金东区人民政府",
     "overlap_period": "至今"},
    # ── 蒋涛-潘钢刚 ──
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate",
     "context": "区长与副区长", "overlap_org": "金东区人民政府",
     "overlap_period": "至今"},
    # ── 蒋涛-周斌 ──
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate",
     "context": "区长与副区长(挂职)", "overlap_org": "金东区人民政府",
     "overlap_period": "至今"},
    # ── 其他 ──
    {"person_a": 1, "person_b": 13, "type": "superior_subordinate",
     "context": "区委书记-副区长(挂职)", "overlap_org": "中共金华市金东区委员会",
     "overlap_period": "至今"},
    {"person_a": 1, "person_b": 18, "type": "superior_subordinate",
     "context": "区委书记与副区长(郑攀)", "overlap_org": "金东区人民政府",
     "overlap_period": "至今"},
    {"person_a": 1, "person_b": 20, "type": "superior_subordinate",
     "context": "区委书记与副区长(黄泽文)", "overlap_org": "金东区人民政府",
     "overlap_period": "至今"},
    {"person_a": 1, "person_b": 21, "type": "superior_subordinate",
     "context": "区委书记与副区长(朱刚露)", "overlap_org": "金东区人民政府",
     "overlap_period": "至今"},
    # ── 张群环跨区关系 ──
    {"person_a": 3, "person_b": 1, "type": "predecessor_successor",
     "context": "张群环为黄国钧前任区委书记", "overlap_org": "中共金华市金东区委员会",
     "overlap_period": "约2023-2024"},
]

# ═══════════════════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════════════════

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

    db_size = os.path.getsize(DB_PATH) if os.path.exists(DB_PATH) else 0
    gexf_size = os.path.getsize(GEXF_PATH) if os.path.exists(GEXF_PATH) else 0
    print(f"Database: {DB_PATH} ({db_size} bytes)")
    print(f"GEXF graph: {GEXF_PATH} ({gexf_size} bytes)")
    print(f"Persons: {len(persons)}")
    print(f"Organizations: {len(organizations)}")
    print(f"Positions: {len(positions)}")
    print(f"Relationships: {len(relationships)}")
    print("Build complete.")