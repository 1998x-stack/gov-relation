#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 老河口市, 襄阳市, 湖北省.

Investigation date: 2026-07-24
Task ID: hubei_老河口市
Level: 县级市
Targets: 市委书记 & 市长

Research status: COMPLETED (sources: Baidu search, Baike, government portal)
As of: 2026-07-24

Current leadership (as of May-June 2026):
- 市委书记: 郭方芳 (female, Han, Oct 1975, Danjiangkou, Hubei)
- 市长: 冯晓濮 (male, Han, Sep 1979, Puyang, Henan)

Key predecessor transitions:
- 曹祖金 (Jul 2021 - Aug 2024 市委书记) → promoted to 襄阳市副市长
- 冯玉强 (Nov 2021 - Sep 2024 市长; Sep 2024 - May 2026 市委书记) → rotated out
- 郭章新 (Dec 2024 - May 2026 市长) → rotated out
- 张学林 (pre-2021 市委书记) → predecessor to 曹祖金
"""

from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────
STAGING_DIR = Path(__file__).resolve().parent
BASE = STAGING_DIR.parents[2]  # repo root
SLUG = "老河口市"
TODAY = datetime.now().strftime("%Y%m%d")
AS_OF = "2026-07-24"

DB_PATH = STAGING_DIR / f"{SLUG}_network.db"
GEXF_PATH = STAGING_DIR / f"{SLUG}_network.gexf"

# ── Person Data ────────────────────────────────────────────────────────────
# Source confidence:
#   confirmed = multiple sources (Baidu Baike, government portal, media)
#   plausible = single reliable source
#   unverified = inferred or uncorroborated

persons = [
    # ═══════ Current Core Leadership ═══════
    {
        "id": 1,
        "name": "郭方芳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1975-10",
        "birthplace": "湖北省丹江口市",
        "education": "大学学历，在职大学学历，管理学学士",
        "party_join": "1996-06",
        "work_start": "1995-08",
        "current_post": "老河口市委书记",
        "current_org": "中共老河口市委员会",
        "source": "https://www.laohekou.gov.cn/ 郭方芳简历; Baidu Baike; 老河口市委书记、市长同时调整 (2026-05-14)"
    },
    {
        "id": 2,
        "name": "冯晓濮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-09",
        "birthplace": "河南省濮阳市",
        "education": "大学学历，法学学士",
        "party_join": "2004-06",
        "work_start": "2003-11",
        "current_post": "老河口市人民政府市长",
        "current_org": "老河口市人民政府",
        "source": "https://www.laohekou.gov.cn/ 冯晓濮简历; 老河口市第十一届人民代表大会第六次会议公告 (2026-06-26)"
    },
    # ═══════ Deputy Party Secretary ═══════
    {
        "id": 3,
        "name": "邓琪",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "老河口市委副书记",
        "current_org": "中共老河口市委员会",
        "source": "老河口市人大常委会会议报道 (2026-05); 洪山嘴镇人大代表活动报道 (2026-04-17)"
    },
    # ═══════ 市委常委班子 ═══════
    {
        "id": 4,
        "name": "王双义",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "老河口市委常委、纪委书记、监委主任",
        "current_org": "中共老河口市纪律检查委员会/老河口市监察委员会",
        "source": "老河口市委常委名单 (Baidu Baike); 老河口市第十一届人民代表大会第六次会议"
    },
    {
        "id": 5,
        "name": "肖凌志",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "老河口市委常委、组织部部长",
        "current_org": "中共老河口市委组织部",
        "source": "老河口市委常委名单 (Baidu Baike)"
    },
    {
        "id": 6,
        "name": "尚钰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "老河口市委常委、副市长（协助市长负责政府日常工作）",
        "current_org": "老河口市人民政府",
        "source": "老河口市委常委名单 (Baidu Baike)"
    },
    {
        "id": 7,
        "name": "王兵",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "老河口市委常委、市委办公室主任、政法委书记",
        "current_org": "中共老河口市委员会办公室",
        "source": "老河口市委常委名单 (Baidu Baike); 曹祖金巡林报道 (2023-05)"
    },
    {
        "id": 8,
        "name": "白家强",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "老河口市委常委、宣传部部长",
        "current_org": "中共老河口市委宣传部",
        "source": "老河口人民政府网站 (2023-08 白家强已任市委常委)"
    },
    {
        "id": 9,
        "name": "杨敏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "老河口市委常委、统战部部长",
        "current_org": "中共老河口市委统战部",
        "source": "老河口市委常委名单 (Baidu Baike)"
    },
    {
        "id": 10,
        "name": "孙卓鹏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "老河口市委常委、人民武装部政治委员",
        "current_org": "老河口市人民武装部",
        "source": "老河口市委常委名单 (Baidu Baike)"
    },
    {
        "id": 11,
        "name": "付静忠",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "老河口市委常委、副市长",
        "current_org": "老河口市人民政府",
        "source": "老河口市委常委名单 (Baidu Baike); 曹祖金巡林报道 (2023-05)"
    },
    # ═══════ 市政府领导班子 ═══════
    {
        "id": 12,
        "name": "何靖",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "老河口市人民政府副市长",
        "current_org": "老河口市人民政府",
        "source": "老河口市政府门户网站 领导之窗"
    },
    {
        "id": 13,
        "name": "杨军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "老河口市人民政府副市长、党组成员",
        "current_org": "老河口市人民政府",
        "source": "老河口市政府门户网站 领导之窗"
    },
    {
        "id": 14,
        "name": "瞿飞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "老河口市人民政府副市长、党组成员",
        "current_org": "老河口市人民政府",
        "source": "老河口市政府门户网站 领导之窗"
    },
    {
        "id": 15,
        "name": "康祖全",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "老河口市人民政府副市长、党组成员",
        "current_org": "老河口市人民政府",
        "source": "老河口市第十一届人民代表大会第六次会议 (2026-06-26)"
    },
    {
        "id": 16,
        "name": "陈俊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "老河口市人民政府副市长、党组成员",
        "current_org": "老河口市人民政府",
        "source": "老河口市政府门户网站 领导之窗"
    },
    {
        "id": 17,
        "name": "黄伟森",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "老河口市人民政府副市长、党组成员",
        "current_org": "老河口市人民政府",
        "source": "老河口市政府门户网站 领导之窗"
    },
    # ═══════ 人大、政协 ═══════
    {
        "id": 18,
        "name": "刘国强",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "老河口市人大常委会党组书记、主任",
        "current_org": "老河口市人民代表大会常务委员会",
        "source": "老河口市第十一届人民代表大会第六次会议 (2026-06-26)"
    },
    {
        "id": 19,
        "name": "胡松",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "老河口市委常委（近期新晋）",
        "current_org": "中共老河口市委员会",
        "source": "老河口市乡人大换届选举工作部署会议报道 (2026-07-21)"
    },
    # ═══════ 关键前任 ═══════
    {
        "id": 20,
        "name": "冯玉强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-09",
        "birthplace": "湖北省枣阳市",
        "education": "在职硕士研究生学历，管理学硕士",
        "party_join": "1998-12",
        "work_start": "1999-07",
        "current_post": "（前任老河口市委书记/市长）",
        "current_org": "",
        "source": "冯玉强 Baidu Baike; 晋升公示 (2024-09-14); 老河口市委书记、市长同时调整 (2026-05-14)"
    },
    {
        "id": 21,
        "name": "曹祖金",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974-10",
        "birthplace": "湖北省枣阳市",
        "education": "党校大学学历",
        "party_join": "1996-07",
        "work_start": "1992-08",
        "current_post": "襄阳市人民政府副市长、党组成员",
        "current_org": "襄阳市人民政府",
        "source": "曹祖金 Baidu Baike; 襄阳市人大常委会任命 (2024-08-30)"
    },
    {
        "id": 22,
        "name": "郭章新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981-11",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（前任老河口市市长）",
        "current_org": "",
        "source": "老河口市人大常委会任命 (2024-12-16); 老河口市委书记、市长同时调整 (2026-05-14)"
    },
    {
        "id": 23,
        "name": "张学林",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（前任老河口市委书记）",
        "current_org": "",
        "source": "老河口市领导干部会议 (2021-06-29); 曹祖金接任报道"
    },
]

organizations = [
    {"id": 1, "name": "中共老河口市委员会", "type": "党委", "level": "县级", "parent": "中共襄阳市委员会", "location": "襄阳市老河口市"},
    {"id": 2, "name": "老河口市人民政府", "type": "政府", "level": "县级", "parent": "襄阳市人民政府", "location": "襄阳市老河口市"},
    {"id": 3, "name": "中共老河口市纪律检查委员会/老河口市监察委员会", "type": "党委", "level": "县级", "parent": "中共襄阳市纪律检查委员会", "location": "襄阳市老河口市"},
    {"id": 4, "name": "中共老河口市委组织部", "type": "党委", "level": "县级", "parent": "中共襄阳市委员会", "location": "襄阳市老河口市"},
    {"id": 5, "name": "中共老河口市委宣传部", "type": "党委", "level": "县级", "parent": "中共襄阳市委员会", "location": "襄阳市老河口市"},
    {"id": 6, "name": "中共老河口市委统战部", "type": "党委", "level": "县级", "parent": "中共襄阳市委员会", "location": "襄阳市老河口市"},
    {"id": 7, "name": "中共老河口市委政法委员会", "type": "党委", "level": "县级", "parent": "中共襄阳市委员会", "location": "襄阳市老河口市"},
    {"id": 8, "name": "老河口市人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "襄阳市人民代表大会常务委员会", "location": "襄阳市老河口市"},
    {"id": 9, "name": "中国人民政治协商会议老河口市委员会", "type": "政协", "level": "县级", "parent": "政协襄阳市委员会", "location": "襄阳市老河口市"},
    {"id": 10, "name": "老河口市人民武装部", "type": "事业单位", "level": "县级", "parent": "襄阳军分区", "location": "襄阳市老河口市"},
    {"id": 11, "name": "中共老河口市委员会办公室", "type": "党委", "level": "县级", "parent": "中共老河口市委员会", "location": "襄阳市老河口市"},
    {"id": 12, "name": "襄阳市人民政府", "type": "政府", "level": "地市级", "parent": "湖北省人民政府", "location": "湖北省襄阳市"},
]

positions = [
    # 郭方芳
    {"person_id": 1, "org_id": 1, "title": "老河口市委书记", "start_date": "2026-05", "end_date": "", "rank": "正处级", "note": "同时任一级调研员"},
    # 冯晓濮
    {"person_id": 2, "org_id": 1, "title": "老河口市委副书记", "start_date": "2026-05", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "老河口市人民政府市长", "start_date": "2026-06-26", "end_date": "", "rank": "正处级", "note": "2026-05-15 任代理市长, 2026-06-26 正式当选"},
    # 邓琪
    {"person_id": 3, "org_id": 1, "title": "老河口市委副书记", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 王双义
    {"person_id": 4, "org_id": 1, "title": "老河口市委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 3, "title": "老河口市纪委书记、监委主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 肖凌志
    {"person_id": 5, "org_id": 1, "title": "老河口市委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 5, "org_id": 4, "title": "老河口市委组织部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 尚钰
    {"person_id": 6, "org_id": 1, "title": "老河口市委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "老河口市人民政府副市长（常务）", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 王兵
    {"person_id": 7, "org_id": 1, "title": "老河口市委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 11, "title": "老河口市委办公室主任", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 7, "title": "老河口市委政法委书记", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 白家强
    {"person_id": 8, "org_id": 1, "title": "老河口市委常委", "start_date": "2023-08", "end_date": "", "rank": "副处级", "note": "此前任老河口人民政府副市长"},
    {"person_id": 8, "org_id": 5, "title": "老河口市委宣传部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 杨敏
    {"person_id": 9, "org_id": 1, "title": "老河口市委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 9, "org_id": 6, "title": "老河口市委统战部部长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 孙卓鹏
    {"person_id": 10, "org_id": 1, "title": "老河口市委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 10, "title": "老河口市人民武装部政治委员", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 付静忠
    {"person_id": 11, "org_id": 1, "title": "老河口市委常委", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "老河口市人民政府副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 何靖
    {"person_id": 12, "org_id": 2, "title": "老河口市人民政府副市长", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 杨军
    {"person_id": 13, "org_id": 2, "title": "老河口市人民政府副市长、党组成员", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 瞿飞
    {"person_id": 14, "org_id": 2, "title": "老河口市人民政府副市长、党组成员", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 康祖全
    {"person_id": 15, "org_id": 2, "title": "老河口市人民政府副市长、党组成员", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 陈俊
    {"person_id": 16, "org_id": 2, "title": "老河口市人民政府副市长、党组成员", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 黄伟森
    {"person_id": 17, "org_id": 2, "title": "老河口市人民政府副市长、党组成员", "start_date": "", "end_date": "", "rank": "副处级", "note": ""},
    # 刘国强
    {"person_id": 18, "org_id": 8, "title": "老河口市人大常委会党组书记、主任", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    # 胡松
    {"person_id": 19, "org_id": 1, "title": "老河口市委常委", "start_date": "2026-07", "end_date": "", "rank": "副处级", "note": "近期新晋市委常委"},
    # 冯玉强 - 前任
    {"person_id": 20, "org_id": 1, "title": "老河口市委书记", "start_date": "2024-09", "end_date": "2026-05", "rank": "正处级", "note": "2024年9月至2026年5月任市委书记"},
    {"person_id": 20, "org_id": 2, "title": "老河口市人民政府市长", "start_date": "2021-11", "end_date": "2024-09", "rank": "正处级", "note": "2021年11月至2024年9月任市长"},
    # 曹祖金 - 前任
    {"person_id": 21, "org_id": 1, "title": "老河口市委书记", "start_date": "2021-06", "end_date": "2024-08", "rank": "正处级", "note": "2021年6月至2024年8月任市委书记"},
    {"person_id": 21, "org_id": 12, "title": "襄阳市人民政府副市长", "start_date": "2024-08", "end_date": "", "rank": "副厅级", "note": "2024年8月起任现职"},
    # 郭章新 - 前任
    {"person_id": 22, "org_id": 2, "title": "老河口市人民政府市长", "start_date": "2024-12", "end_date": "2026-05", "rank": "正处级", "note": "2024年12月代理市长至2026年5月"},
    {"person_id": 22, "org_id": 1, "title": "老河口市委副书记", "start_date": "", "end_date": "2026-05", "rank": "正处级", "note": "此前任市委副书记、政法委书记"},
    # 张学林 - 前任
    {"person_id": 23, "org_id": 1, "title": "老河口市委书记", "start_date": "", "end_date": "2021-06", "rank": "正处级", "note": "2021年6月离任"},
]

relationships = [
    # 党政搭档 - 现任
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "郭方芳（市委书记）与冯晓濮（市长）为老河口市党政正职搭档（2026年5月起）", "overlap_org": "老河口市", "overlap_period": "2026-05至今"},
    # 党政搭档 - 前任
    {"person_a": 20, "person_b": 22, "type": "党政搭档", "context": "冯玉强（市委书记）与郭章新（市长）为前任党政正职搭档（2024年12月至2026年5月）", "overlap_org": "老河口市", "overlap_period": "2024-12至2026-05"},
    {"person_a": 20, "person_b": 21, "type": "predecessor_successor", "context": "冯玉强接替曹祖金任老河口市委书记", "overlap_org": "中共老河口市委员会", "overlap_period": "2024-09"},
    {"person_a": 21, "person_b": 23, "type": "predecessor_successor", "context": "曹祖金接替张学林任老河口市委书记", "overlap_org": "中共老河口市委员会", "overlap_period": "2021-06"},
    {"person_a": 22, "person_b": 2, "type": "predecessor_successor", "context": "冯晓濮接替郭章新任老河口市长", "overlap_org": "老河口市人民政府", "overlap_period": "2026-05"},
    # 郭方芳前任搭档关系
    {"person_a": 1, "person_b": 20, "type": "predecessor_successor", "context": "郭方芳接替冯玉强任老河口市委书记", "overlap_org": "中共老河口市委员会", "overlap_period": "2026-05"},
    {"person_a": 1, "person_b": 22, "type": "overlap", "context": "郭方芳（樊城区委书记）与郭章新（老河口市长）曾同期任职襄阳市辖县区", "overlap_org": "襄阳市", "overlap_period": "2024-12至2026-05"},
    # 常委班子内部
    {"person_a": 4, "person_b": 5, "type": "overlap", "context": "王双义（纪委书记）与肖凌志（组织部长）同期任老河口市委常委", "overlap_org": "中共老河口市委员会", "overlap_period": ""},
    {"person_a": 7, "person_b": 11, "type": "overlap", "context": "王兵与付静忠同期任副市长", "overlap_org": "老河口市人民政府", "overlap_period": "2023"},
    # 曹祖金与冯玉强工作交接
    {"person_a": 20, "person_b": 21, "type": "same_native_place", "context": "冯玉强与曹祖金均为湖北枣阳人", "overlap_org": "", "overlap_period": ""},
    # 郭方芳与老河口的渊源
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "郭方芳2011-2015年任老河口市委常委、常务副市长、副书记期间，与王双义等人曾有工作交集", "overlap_org": "中共老河口市委员会", "overlap_period": "2011-2015"},
    {"person_a": 1, "person_b": 21, "type": "overlap", "context": "郭方芳（樊城区委书记）与曹祖金（老河口市委书记）同期任襄阳市辖县区主要领导（2021-2024）", "overlap_org": "襄阳市", "overlap_period": "2021-2024"},
    {"person_a": 1, "person_b": 20, "type": "overlap", "context": "郭方芳（樊城区委书记）与冯玉强（老河口市委书记）同期任襄阳市辖县区主要领导", "overlap_org": "襄阳市", "overlap_period": "2021-2024"},
]


# ── Helper Functions ───────────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(name, current_post):
    """Return RGB color string for a person based on role."""
    if "市委书记" in (current_post or "") or "书记" in (name or ""):
        return "255,50,50"
    if "市长" in (current_post or ""):
        return "50,100,255"
    if "纪委书记" in (current_post or "") or "监委" in (current_post or ""):
        return "255,165,0"
    if "组织部" in (current_post or ""):
        return "200,100,0"
    if "宣传部" in (current_post or ""):
        return "0,150,150"
    if "统战" in (current_post or ""):
        return "150,0,150"
    if "武装部" in (current_post or ""):
        return "100,150,0"
    if "人大" in (current_post or ""):
        return "200,100,100"
    if "政协" in (current_post or ""):
        return "150,100,50"
    if "副市长" in (current_post or ""):
        return "50,100,200"
    if "前任" in (current_post or ""):
        return "100,100,100"
    return "100,100,100"


def org_color(org_type):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "事业单位": "220,220,220",
    }
    return colors.get(org_type, "200,200,200")


def is_top_leader(name, current_post):
    if name == "郭方芳" or name == "冯晓濮":
        return True
    if "市委书记" in (current_post or "") or "市长" in (current_post or ""):
        return True
    return False


# ── Build Database ─────────────────────────────────────────────────────────

def build_database():
    conn = sqlite3.connect(str(DB_PATH))
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER, title TEXT,
            start_date TEXT, end_date TEXT, rank TEXT, note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER, type TEXT,
            context TEXT, overlap_org TEXT, overlap_period TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"],
             p["work_start"], p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("""INSERT INTO positions
            (person_id, org_id, title, start_date, end_date, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"],
             pos["start_date"], pos["end_date"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("""INSERT INTO relationships
            (person_a, person_b, type, context, overlap_org, overlap_period)
            VALUES (?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"],
             r["context"], r["overlap_org"], r["overlap_period"]))

    conn.commit()
    conn.close()
    print(f"  Database: {DB_PATH}")


# ── Build GEXF ─────────────────────────────────────────────────────────────

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append(f'    <description>{SLUG} Leadership Network</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org_type" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes - Persons
    lines.append('    <nodes>')
    eid = 0
    for p in persons:
        c = person_color(p["name"], p["current_post"])
        sz = "20.0" if is_top_leader(p["name"], p["current_post"]) else "12.0"
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Nodes - Organizations
    for o in organizations:
        c = org_color(o["type"])
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value=""/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="3" value=""/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges - Positions (person -> organization)
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append(f'          <attvalue for="2" value=""/>')
        lines.append(f'          <attvalue for="3" value="{esc(pos.get("start_date", ""))} - {esc(pos.get("end_date", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Edges - Relationships (person <-> person)
    for r in relationships:
        weight = "2.0" if r["type"] in ("党政搭档", "predecessor_successor") else "1.5"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r["overlap_period"])}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"  GEXF: {GEXF_PATH}")


# ── Main ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print(f"Building {SLUG} network data...")
    build_database()
    build_gexf()
    print(f"\nSummary:")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print("Done.")
