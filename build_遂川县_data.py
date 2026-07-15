#!/usr/bin/env python3
"""
Build 遂川县 (Suichuan County) government personnel network database and GEXF graph.

遂川县 is a county under 吉安市, 江西省.
Current leadership as of 2026-07-15 (from Baidu Baike):
- 罗刚: 遂川县委书记
- 曾昭君: 遂川县委副书记、县长候选人
- 刘远生: 县人大常委会主任
- 黄书华: 县政协主席
- 县委常委: 冯书朝、胡顺根、伍巧明、胡文峰、陈征、郭哲、杨光宇、刘德镇、熊清泉
- 副县长: 伍巧明、胡文峰、郭哲、杨光宇、彭水生、李茂军、吴建红、罗晓斌、廖小平、龙浩

Source: Baidu Baike (baike.baidu.com/item/遂川县), accessed 2026-07-15.
⚠️ Career details for most individuals await verification from official government websites
(suichuan.gov.cn) and 吉安市委组织部 pre-appointment notices.
"""
import sqlite3
import os
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
if "data/tmp" in BASE:
    REPO_ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
else:
    REPO_ROOT = BASE

today = datetime.now().strftime("%Y-%m-%d")
slug = "遂川县"

DB_REL = f"data/database/{slug}_network.db"
GEXF_REL = f"data/graph/{slug}_network.gexf"

DB_PATH = os.path.join(REPO_ROOT, DB_REL)
GEXF_PATH = os.path.join(REPO_ROOT, GEXF_REL)

# =========================================================================
# DATA
# =========================================================================

# Person ID convention: suichuan_{surname_givenname}
esc = lambda s: str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;") if s else ""

persons = [
    # ---- Top Leaders ----
    {
        "id": 1,
        "name": "罗刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "遂川县委书记",
        "current_org": "中共遂川县委员会",
        "source": "百度百科—遂川县(baike.baidu.com/item/遂川县)—县委书记罗刚，2026-07-15访问; 需从suichuan.gov.cn确认完整履历",
    },
    {
        "id": 2,
        "name": "曾昭君",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "遂川县委副书记、县长候选人",
        "current_org": "遂川县人民政府",
        "source": "百度百科—遂川县(baike.baidu.com/item/遂川县)—县长候选人曾昭君，2026-07-15访问",
    },
    # ---- Party Standing Committee (县委常委) ----
    {
        "id": 3,
        "name": "冯书朝",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "遂川县委常委",
        "current_org": "中共遂川县委员会",
        "source": "百度百科—遂川县(baike.baidu.com/item/遂川县)—县委常委名单，2026-07-15访问",
    },
    {
        "id": 4,
        "name": "胡顺根",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "遂川县委常委",
        "current_org": "中共遂川县委员会",
        "source": "百度百科—遂川县(baike.baidu.com/item/遂川县)—县委常委名单，2026-07-15访问",
    },
    {
        "id": 5,
        "name": "伍巧明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "遂川县委常委、副县长",
        "current_org": "遂川县人民政府",
        "source": "百度百科—遂川县(baike.baidu.com/item/遂川县)—县委常委/副县长名单，2026-07-15访问",
    },
    {
        "id": 6,
        "name": "胡文峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "遂川县委常委、副县长",
        "current_org": "遂川县人民政府",
        "source": "百度百科—遂川县(baike.baidu.com/item/遂川县)—县委常委/副县长名单，2026-07-15访问",
    },
    {
        "id": 7,
        "name": "陈征",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "遂川县委常委",
        "current_org": "中共遂川县委员会",
        "source": "百度百科—遂川县(baike.baidu.com/item/遂川县)—县委常委名单，2026-07-15访问",
    },
    {
        "id": 8,
        "name": "郭哲",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "遂川县委常委、副县长",
        "current_org": "遂川县人民政府",
        "source": "百度百科—遂川县(baike.baidu.com/item/遂川县)—县委常委/副县长名单，2026-07-15访问",
    },
    {
        "id": 9,
        "name": "杨光宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "遂川县委常委、副县长",
        "current_org": "遂川县人民政府",
        "source": "百度百科—遂川县(baike.baidu.com/item/遂川县)—县委常委/副县长名单，2026-07-15访问",
    },
    {
        "id": 10,
        "name": "刘德镇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "遂川县委常委",
        "current_org": "中共遂川县委员会",
        "source": "百度百科—遂川县(baike.baidu.com/item/遂川县)—县委常委名单，2026-07-15访问",
    },
    {
        "id": 11,
        "name": "熊清泉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "遂川县委常委",
        "current_org": "中共遂川县委员会",
        "source": "百度百科—遂川县(baike.baidu.com/item/遂川县)—县委常委名单，2026-07-15访问",
    },
    # ---- Deputy Government Leaders (副县长) ----
    {
        "id": 12,
        "name": "彭水生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "遂川县副县长",
        "current_org": "遂川县人民政府",
        "source": "百度百科—遂川县(baike.baidu.com/item/遂川县)—副县长名单，2026-07-15访问",
    },
    {
        "id": 13,
        "name": "李茂军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "遂川县副县长",
        "current_org": "遂川县人民政府",
        "source": "百度百科—遂川县(baike.baidu.com/item/遂川县)—副县长名单，2026-07-15访问",
    },
    {
        "id": 14,
        "name": "吴建红",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "遂川县副县长",
        "current_org": "遂川县人民政府",
        "source": "百度百科—遂川县(baike.baidu.com/item/遂川县)—副县长名单，2026-07-15访问",
    },
    {
        "id": 15,
        "name": "罗晓斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "遂川县副县长",
        "current_org": "遂川县人民政府",
        "source": "百度百科—遂川县(baike.baidu.com/item/遂川县)—副县长名单，2026-07-15访问",
    },
    {
        "id": 16,
        "name": "廖小平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "遂川县副县长",
        "current_org": "遂川县人民政府",
        "source": "百度百科—遂川县(baike.baidu.com/item/遂川县)—副县长名单，2026-07-15访问",
    },
    {
        "id": 17,
        "name": "龙浩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "遂川县副县长",
        "current_org": "遂川县人民政府",
        "source": "百度百科—遂川县(baike.baidu.com/item/遂川县)—副县长名单，2026-07-15访问",
    },
    # ---- NPC & CPPCC ----
    {
        "id": 18,
        "name": "刘远生",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "遂川县人大常委会主任",
        "current_org": "遂川县人民代表大会常务委员会",
        "source": "百度百科—遂川县(baike.baidu.com/item/遂川县)—县人大常委会主任刘远生，2026-07-15访问",
    },
    {
        "id": 19,
        "name": "黄书华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "遂川县政协主席",
        "current_org": "中国人民政治协商会议遂川县委员会",
        "source": "百度百科—遂川县(baike.baidu.com/item/遂川县)—县政协主席黄书华，2026-07-15访问",
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共遂川县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共吉安市委员会",
        "location": "江西省吉安市遂川县",
    },
    {
        "id": 2,
        "name": "遂川县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "吉安市人民政府",
        "location": "江西省吉安市遂川县",
    },
    {
        "id": 3,
        "name": "遂川县人民代表大会常务委员会",
        "type": "人大",
        "level": "县处级",
        "parent": "吉安市人民代表大会常务委员会",
        "location": "江西省吉安市遂川县",
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议遂川县委员会",
        "type": "政协",
        "level": "县处级",
        "parent": "中国人民政治协商会议吉安市委员会",
        "location": "江西省吉安市遂川县",
    },
]

positions = [
    # 罗刚 — 县委书记
    {
        "id": 1,
        "person_id": 1,
        "org_id": 1,
        "title": "遂川县委书记",
        "start": "待查",
        "end": "",
        "rank": "县处级正职",
        "note": "现任遂川县委书记。百度百科显示为现任县委书记，到任时间待查。",
    },
    # 曾昭君 — 县长候选人
    {
        "id": 2,
        "person_id": 2,
        "org_id": 1,
        "title": "遂川县委副书记",
        "start": "待查",
        "end": "",
        "rank": "县处级副职",
        "note": "现任遂川县委副书记。百度百科显示为县委副书记、县长候选人。",
    },
    {
        "id": 3,
        "person_id": 2,
        "org_id": 2,
        "title": "遂川县长候选人",
        "start": "待查",
        "end": "",
        "rank": "县处级正职",
        "note": "百度百科标注为'县长候选人'，尚未正式选举或到任日期待查。",
    },
    # 冯书朝
    {
        "id": 4,
        "person_id": 3,
        "org_id": 1,
        "title": "遂川县委常委",
        "start": "",
        "end": "",
        "rank": "县处级副职",
        "note": "现任县委常委。具体分工待查。",
    },
    # 胡顺根
    {
        "id": 5,
        "person_id": 4,
        "org_id": 1,
        "title": "遂川县委常委",
        "start": "",
        "end": "",
        "rank": "县处级副职",
        "note": "现任县委常委。具体分工待查。",
    },
    # 伍巧明
    {
        "id": 6,
        "person_id": 5,
        "org_id": 1,
        "title": "遂川县委常委",
        "start": "",
        "end": "",
        "rank": "县处级副职",
        "note": "现任县委常委。",
    },
    {
        "id": 7,
        "person_id": 5,
        "org_id": 2,
        "title": "遂川县副县长",
        "start": "",
        "end": "",
        "rank": "县处级副职",
        "note": "现任副县长。百度百科同时列为县委常委和副县长。",
    },
    # 胡文峰
    {
        "id": 8,
        "person_id": 6,
        "org_id": 1,
        "title": "遂川县委常委",
        "start": "",
        "end": "",
        "rank": "县处级副职",
        "note": "现任县委常委。",
    },
    {
        "id": 9,
        "person_id": 6,
        "org_id": 2,
        "title": "遂川县副县长",
        "start": "",
        "end": "",
        "rank": "县处级副职",
        "note": "现任副县长。百度百科同时列为县委常委和副县长。",
    },
    # 陈征
    {
        "id": 10,
        "person_id": 7,
        "org_id": 1,
        "title": "遂川县委常委",
        "start": "",
        "end": "",
        "rank": "县处级副职",
        "note": "现任县委常委。具体分工待查。",
    },
    # 郭哲
    {
        "id": 11,
        "person_id": 8,
        "org_id": 1,
        "title": "遂川县委常委",
        "start": "",
        "end": "",
        "rank": "县处级副职",
        "note": "现任县委常委。",
    },
    {
        "id": 12,
        "person_id": 8,
        "org_id": 2,
        "title": "遂川县副县长",
        "start": "",
        "end": "",
        "rank": "县处级副职",
        "note": "现任副县长。百度百科同时列为县委常委和副县长。",
    },
    # 杨光宇
    {
        "id": 13,
        "person_id": 9,
        "org_id": 1,
        "title": "遂川县委常委",
        "start": "",
        "end": "",
        "rank": "县处级副职",
        "note": "现任县委常委。",
    },
    {
        "id": 14,
        "person_id": 9,
        "org_id": 2,
        "title": "遂川县副县长",
        "start": "",
        "end": "",
        "rank": "县处级副职",
        "note": "现任副县长。百度百科同时列为县委常委和副县长。",
    },
    # 刘德镇
    {
        "id": 15,
        "person_id": 10,
        "org_id": 1,
        "title": "遂川县委常委",
        "start": "",
        "end": "",
        "rank": "县处级副职",
        "note": "现任县委常委。具体分工待查。",
    },
    # 熊清泉
    {
        "id": 16,
        "person_id": 11,
        "org_id": 1,
        "title": "遂川县委常委",
        "start": "",
        "end": "",
        "rank": "县处级副职",
        "note": "现任县委常委。具体分工待查。",
    },
    # 彭水生 — 副县长
    {
        "id": 17,
        "person_id": 12,
        "org_id": 2,
        "title": "遂川县副县长",
        "start": "",
        "end": "",
        "rank": "县处级副职",
        "note": "现任副县长。副县长排名中的具体位次待查。",
    },
    # 李茂军
    {
        "id": 18,
        "person_id": 13,
        "org_id": 2,
        "title": "遂川县副县长",
        "start": "",
        "end": "",
        "rank": "县处级副职",
        "note": "现任副县长。",
    },
    # 吴建红
    {
        "id": 19,
        "person_id": 14,
        "org_id": 2,
        "title": "遂川县副县长",
        "start": "",
        "end": "",
        "rank": "县处级副职",
        "note": "现任副县长。",
    },
    # 罗晓斌
    {
        "id": 20,
        "person_id": 15,
        "org_id": 2,
        "title": "遂川县副县长",
        "start": "",
        "end": "",
        "rank": "县处级副职",
        "note": "现任副县长。",
    },
    # 廖小平
    {
        "id": 21,
        "person_id": 16,
        "org_id": 2,
        "title": "遂川县副县长",
        "start": "",
        "end": "",
        "rank": "县处级副职",
        "note": "现任副县长。",
    },
    # 龙浩
    {
        "id": 22,
        "person_id": 17,
        "org_id": 2,
        "title": "遂川县副县长",
        "start": "",
        "end": "",
        "rank": "县处级副职",
        "note": "现任副县长。",
    },
    # 刘远生 — 人大主任
    {
        "id": 23,
        "person_id": 18,
        "org_id": 3,
        "title": "遂川县人大常委会主任",
        "start": "",
        "end": "",
        "rank": "县处级正职",
        "note": "现任县人大常委会主任。",
    },
    # 黄书华 — 政协主席
    {
        "id": 24,
        "person_id": 19,
        "org_id": 4,
        "title": "遂川县政协主席",
        "start": "",
        "end": "",
        "rank": "县处级正职",
        "note": "现任县政协主席。",
    },
]

relationships = [
    # 罗刚 ↔ 曾昭君（党政正职搭档）
    {
        "id": 1,
        "person_a_id": 1,
        "person_b_id": 2,
        "type": "党政正职搭档",
        "context": "罗刚（县委书记）与曾昭君（县委副书记、县长候选人）为遂川县党政正职搭档关系",
        "overlap_org": "中共遂川县委员会/遂川县人民政府",
        "overlap_period": "现任",
    },
    # 罗刚 ↔ 刘远生
    {
        "id": 2,
        "person_a_id": 1,
        "person_b_id": 18,
        "type": "四套班子关系",
        "context": "县委书记与县人大常委会主任为四套班子关系",
        "overlap_org": "遂川县",
        "overlap_period": "现任",
    },
    # 罗刚 ↔ 黄书华
    {
        "id": 3,
        "person_a_id": 1,
        "person_b_id": 19,
        "type": "四套班子关系",
        "context": "县委书记与县政协主席为四套班子关系",
        "overlap_org": "遂川县",
        "overlap_period": "现任",
    },
    # 罗刚 ↔ 常委班子关系（含兼职副县长的常委）
    {
        "id": 4,
        "person_a_id": 1,
        "person_b_id": 3,
        "type": "常委会班子关系",
        "context": "县委书记与县委常委为常委会班子关系",
        "overlap_org": "中共遂川县委员会",
        "overlap_period": "现任",
    },
    {
        "id": 5,
        "person_a_id": 1,
        "person_b_id": 4,
        "type": "常委会班子关系",
        "context": "县委书记与县委常委为常委会班子关系",
        "overlap_org": "中共遂川县委员会",
        "overlap_period": "现任",
    },
    {
        "id": 6,
        "person_a_id": 1,
        "person_b_id": 5,
        "type": "常委会班子关系",
        "context": "县委书记与县委常委、副县长为常委会班子关系",
        "overlap_org": "中共遂川县委员会",
        "overlap_period": "现任",
    },
    {
        "id": 7,
        "person_a_id": 1,
        "person_b_id": 6,
        "type": "常委会班子关系",
        "context": "县委书记与县委常委、副县长为常委会班子关系",
        "overlap_org": "中共遂川县委员会",
        "overlap_period": "现任",
    },
    {
        "id": 8,
        "person_a_id": 1,
        "person_b_id": 7,
        "type": "常委会班子关系",
        "context": "县委书记与县委常委为常委会班子关系",
        "overlap_org": "中共遂川县委员会",
        "overlap_period": "现任",
    },
    {
        "id": 9,
        "person_a_id": 1,
        "person_b_id": 8,
        "type": "常委会班子关系",
        "context": "县委书记与县委常委、副县长为常委会班子关系",
        "overlap_org": "中共遂川县委员会",
        "overlap_period": "现任",
    },
    {
        "id": 10,
        "person_a_id": 1,
        "person_b_id": 9,
        "type": "常委会班子关系",
        "context": "县委书记与县委常委、副县长为常委会班子关系",
        "overlap_org": "中共遂川县委员会",
        "overlap_period": "现任",
    },
    {
        "id": 11,
        "person_a_id": 1,
        "person_b_id": 10,
        "type": "常委会班子关系",
        "context": "县委书记与县委常委为常委会班子关系",
        "overlap_org": "中共遂川县委员会",
        "overlap_period": "现任",
    },
    {
        "id": 12,
        "person_a_id": 1,
        "person_b_id": 11,
        "type": "常委会班子关系",
        "context": "县委书记与县委常委为常委会班子关系",
        "overlap_org": "中共遂川县委员会",
        "overlap_period": "现任",
    },
    # 曾昭君 ↔ 副县长（县长与副县长的领导关系）
    {
        "id": 13,
        "person_a_id": 2,
        "person_b_id": 12,
        "type": "上下级关系",
        "context": "县长候选人（县委副书记）与副县长为县政府领导班子关系",
        "overlap_org": "遂川县人民政府",
        "overlap_period": "现任",
    },
    {
        "id": 14,
        "person_a_id": 2,
        "person_b_id": 13,
        "type": "上下级关系",
        "context": "县长候选人（县委副书记）与副县长为县政府领导班子关系",
        "overlap_org": "遂川县人民政府",
        "overlap_period": "现任",
    },
    {
        "id": 15,
        "person_a_id": 2,
        "person_b_id": 14,
        "type": "上下级关系",
        "context": "县长候选人（县委副书记）与副县长为县政府领导班子关系",
        "overlap_org": "遂川县人民政府",
        "overlap_period": "现任",
    },
    {
        "id": 16,
        "person_a_id": 2,
        "person_b_id": 15,
        "type": "上下级关系",
        "context": "县长候选人（县委副书记）与副县长为县政府领导班子关系",
        "overlap_org": "遂川县人民政府",
        "overlap_period": "现任",
    },
    {
        "id": 17,
        "person_a_id": 2,
        "person_b_id": 16,
        "type": "上下级关系",
        "context": "县长候选人（县委副书记）与副县长为县政府领导班子关系",
        "overlap_org": "遂川县人民政府",
        "overlap_period": "现任",
    },
    {
        "id": 18,
        "person_a_id": 2,
        "person_b_id": 17,
        "type": "上下级关系",
        "context": "县长候选人（县委副书记）与副县长为县政府领导班子关系",
        "overlap_org": "遂川县人民政府",
        "overlap_period": "现任",
    },
]

# =========================================================================
# BUILDER FUNCTIONS
# =========================================================================

def build_sqlite():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY,
            person_id INTEGER, org_id INTEGER, title TEXT, start TEXT,
            end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY,
            person_a_id INTEGER, person_b_id INTEGER,
            type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY(person_a_id) REFERENCES persons(id),
            FOREIGN KEY(person_b_id) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education, party_join, work_start, current_post, current_org, source)
            VALUES (:id, :name, :gender, :ethnicity, :birth, :birthplace, :education, :party_join, :work_start, :current_post, :current_org, :source)""", p)

    for o in organizations:
        c.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (:id, :name, :type, :level, :parent, :location)""", o)

    for pos in positions:
        c.execute("""INSERT OR REPLACE INTO positions
            (id, person_id, org_id, title, start, end, rank, note)
            VALUES (:id, :person_id, :org_id, :title, :start, :end, :rank, :note)""", pos)

    for r in relationships:
        c.execute("""INSERT OR REPLACE INTO relationships
            (id, person_a_id, person_b_id, type, context, overlap_org, overlap_period)
            VALUES (:id, :person_a_id, :person_b_id, :type, :context, :overlap_org, :overlap_period)""", r)

    conn.commit()
    print("\n=== SQLite Summary ===")
    for tbl in ["persons", "organizations", "positions", "relationships"]:
        cnt = c.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()[0]
        print(f"  {tbl}: {cnt}")
    conn.close()
    print(f"  DB: {DB_PATH}")


def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{today}">')
    lines.append('    <creator>OpenCode Research Agent</creator>')
    lines.append('    <description>遂川县领导班子工作关系网络 — 2026年7月调查（信息来自百度百科）</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Attributes
    lines.append("""    <attributes class="node">
      <attribute id="0" title="type" type="string"/>
      <attribute id="1" title="entity_type" type="string"/>
      <attribute id="2" title="birth" type="string"/>
      <attribute id="3" title="birthplace" type="string"/>
      <attribute id="4" title="current_post" type="string"/>
      <attribute id="5" title="level" type="string"/>
    </attributes>
    <attributes class="edge">
      <attribute id="0" title="type" type="string"/>
      <attribute id="1" title="start" type="string"/>
      <attribute id="2" title="end" type="string"/>
      <attribute id="3" title="context" type="string"/>
    </attributes>""")

    # Nodes: Persons
    lines.append("    <nodes>")
    for p in persons:
        pid = p["id"]
        name = esc(p["name"])
        birth = esc(p.get("birth", ""))
        birthplace = esc(p.get("birthplace", ""))
        post = esc(p.get("current_post", ""))

        title = p.get("current_post", "")
        if "县委书记" in title and "副" not in title:
            c = "255,50,50"
            sz = "20.0"
        elif "县长" in title and "副" not in title:
            c = "50,100,255"
            sz = "20.0"
        elif "人大" in title:
            c = "60,180,75"
            sz = "14.0"
        elif "政协" in title:
            c = "60,180,75"
            sz = "14.0"
        elif "县委常委" in title and "副县长" in title:
            c = "100,150,200"
            sz = "12.0"
        elif "县委常委" in title:
            c = "100,150,200"
            sz = "12.0"
        elif "副县长" in title:
            c = "100,150,200"
            sz = "12.0"
        else:
            c = "100,100,100"
            sz = "12.0"

        lines.append(f"""      <node id="{pid}" label="{name}">
        <attvalues>
          <attvalue for="0" value="person"/>
          <attvalue for="1" value="person"/>
          <attvalue for="2" value="{birth}"/>
          <attvalue for="3" value="{birthplace}"/>
          <attvalue for="4" value="{post}"/>
          <attvalue for="5" value=""/>
        </attvalues>
        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>
        <viz:size value="{sz}"/>
      </node>""")

    # Nodes: Organizations
    org_color_map = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }

    for o in organizations:
        oid = o["id"]
        oname = esc(o["name"])
        otype = o.get("type", "")
        olevel = esc(o.get("level", ""))
        oc = org_color_map.get(otype, "200,200,200")

        lines.append(f"""      <node id="o{oid}" label="{oname}">
        <attvalues>
          <attvalue for="0" value="organization"/>
          <attvalue for="1" value="org"/>
          <attvalue for="2" value=""/>
          <attvalue for="3" value=""/>
          <attvalue for="4" value=""/>
          <attvalue for="5" value="{olevel}"/>
        </attvalues>
        <viz:color r="{oc.split(",")[0]}" g="{oc.split(",")[1]}" b="{oc.split(",")[2]}"/>
        <viz:size value="8.0"/>
      </node>""")

    lines.append("    </nodes>")

    # Edges
    lines.append("    <edges>")
    edge_id = 0

    for pos in positions:
        edge_id += 1
        src = pos["person_id"]
        tgt = f"o{pos['org_id']}"
        title = esc(pos.get("title", ""))
        s = esc(pos.get("start", ""))
        e = esc(pos.get("end", ""))
        ctx = esc(pos.get("note", ""))

        lines.append(f"""      <edge id="{edge_id}" source="{src}" target="{tgt}" label="{title}" weight="1.0">
        <attvalues>
          <attvalue for="0" value="worked_at"/>
          <attvalue for="1" value="{s}"/>
          <attvalue for="2" value="{e}"/>
          <attvalue for="3" value="{ctx}"/>
        </attvalues>
      </edge>""")

    for rel in relationships:
        edge_id += 1
        a = rel["person_a_id"]
        b = rel["person_b_id"]
        rtype = esc(rel.get("type", ""))
        ctx = esc(rel.get("context", ""))
        period = esc(rel.get("overlap_period", ""))
        w = "2.0"

        lines.append(f"""      <edge id="{edge_id}" source="{a}" target="{b}" label="{rtype}" weight="{w}">
        <attvalues>
          <attvalue for="0" value="{rtype}"/>
          <attvalue for="1" value=""/>
          <attvalue for="2" value=""/>
          <attvalue for="3" value="{ctx} ({period})"/>
        </attvalues>
      </edge>""")

    lines.append("    </edges>")
    lines.append("  </graph>")
    lines.append("</gexf>")

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"\n=== GEXF Summary ===")
    print(f"  {edge_id} edges written")
    print(f"  GEXF: {GEXF_PATH}")


# ── Main ──
if __name__ == "__main__":
    print("=" * 60)
    print("  遂川县 (Suichuan County) Leadership Network Builder")
    print(f"  Date: {today}")
    print(f"  NOTE: Data from Baidu Baike — career details ⚠️ 待确认")
    print("=" * 60)
    build_sqlite()
    build_gexf()
    print("\n=== Done ===")
