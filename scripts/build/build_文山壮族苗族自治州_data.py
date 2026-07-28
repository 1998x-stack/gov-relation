#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 文山壮族苗族自治州 leadership network.

Research date: 2026-07-28
Sources:
  - https://www.ynws.gov.cn (official site - confirmed 2026 data)
  - https://baike.baidu.com/item/文山壮族苗族自治州 (Baidu Baike, accessed via Jina)
  - https://baike.baidu.com/item/马忠俊/6796596 (Baidu Baike)
"""

import sqlite3
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

SLUG = "文山壮族苗族自治州"
NOW = "2026-07-28"
STAGING = os.path.join(os.path.dirname(__file__))
DB_PATH = os.path.join(STAGING, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING, f"{SLUG}_network.gexf")

from gov_relation.runner import run_build

SLUG = "文山壮族苗族自治州"
NOW = "2026-07-28"

# ── PERSONS ───────────────────────────────────────────────────────────

persons = [
    # ── Top Leaders ──
    {
        "id": 1,
        "name": "赵国良",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "文山州委书记",
        "current_org": "中共文山壮族苗族自治州委员会",
        "source": "https://baike.baidu.com/item/文山壮族苗族自治州 (截至2026年6月)",
    },
    {
        "id": 2,
        "name": "马忠俊",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1971-12",
        "birthplace": "云南文山",
        "education": "大学/工学学士/农业推广硕士(云南农业大学)",
        "party_join": "1993-12",
        "work_start": "1994-08",
        "current_post": "州委副书记、州政府党组书记、州长",
        "current_org": "文山壮族苗族自治州人民政府",
        "source": "https://baike.baidu.com/item/马忠俊/6796596",
    },

    # ── State Government Vice Governors ──
    {
        "id": 3,
        "name": "李永忠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副州长",
        "current_org": "文山壮族苗族自治州人民政府",
        "source": "https://www.ynws.gov.cn/wszzf/fzz/common/content/content_1855058728556261376.html",
    },
    {
        "id": 4,
        "name": "周立军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-11",
        "birthplace": "",
        "education": "硕士研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "州委常委、州政府党组成员、副州长",
        "current_org": "文山壮族苗族自治州人民政府",
        "source": "https://www.ynws.gov.cn/wszzf/fzz/common/content/content_1855058712898924544.html",
    },
    {
        "id": 5,
        "name": "陆波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副州长",
        "current_org": "文山壮族苗族自治州人民政府",
        "source": "https://www.ynws.gov.cn/wszzf/fzz/common/content/content_1855058694376878080.html",
    },
    {
        "id": 6,
        "name": "庄宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969-07",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "州政府党组成员、副州长、州公安局局长",
        "current_org": "文山壮族苗族自治州人民政府",
        "source": "https://www.ynws.gov.cn/wszzf/fzz/common/content/content_1855052682142982144.html",
    },
    {
        "id": 7,
        "name": "田燕",
        "gender": "女",
        "ethnicity": "壮族",
        "birth": "1975-01",
        "birthplace": "",
        "education": "中央党校大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "州政府党组成员、副州长",
        "current_org": "文山壮族苗族自治州人民政府",
        "source": "https://www.ynws.gov.cn/wszzf/fz/common/content/content_1855058666522505216.html",
    },
    {
        "id": 8,
        "name": "刘䶮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副州长",
        "current_org": "文山壮族苗族自治州人民政府",
        "source": "https://www.ynws.gov.cn/wszzf/fz/common/content/content_1855058647161597952.html",
    },
    {
        "id": 9,
        "name": "郑锦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副州长",
        "current_org": "文山壮族苗族自治州人民政府",
        "source": "https://www.ynws.gov.cn/wszzf/fz/common/content/content_1855058632909352960.html",
    },
    {
        "id": 10,
        "name": "张发政",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "州政府秘书长",
        "current_org": "文山壮族苗族自治州人民政府",
        "source": "https://www.ynws.gov.cn/wszzf/ms/common/content/content_1855058638810738688.html",
    },

    # ── Four-branch Leaders ──
    {
        "id": 11,
        "name": "王毅",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "州人大常委会主任",
        "current_org": "文山壮族苗族自治州人大常委会",
        "source": "https://baike.baidu.com/item/文山壮族苗族自治州",
    },
    {
        "id": 12,
        "name": "吴长昆",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "州政协主席",
        "current_org": "中国人民政治协商会议文山壮族苗族自治州委员会",
        "source": "https://baike.baidu.com/item/文山壮族苗族自治州",
    },

    # ── Predecessors ──
    {
        "id": 13,
        "name": "陈明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（原州委书记，已离任）",
        "current_org": "",
        "source": "https://baike.baidu.com/item/文山壮族苗族自治州 (2021年州委常委名单提及)",
    },
]

# ── ORGANIZATIONS ─────────────────────────────────────────────────────

organizations = [
    # Party & Government
    {"id": 1, "name": "中共文山壮族苗族自治州委员会", "type": "党委", "level": "地级", "parent": "中共云南省委", "location": "文山市"},
    {"id": 2, "name": "文山壮族苗族自治州人民政府", "type": "政府", "level": "地级", "parent": "云南省人民政府", "location": "文山市"},
    {"id": 3, "name": "文山壮族苗族自治州人大常委会", "type": "人大", "level": "地级", "parent": "云南省人大常委会", "location": "文山市"},
    {"id": 4, "name": "中国人民政治协商会议文山壮族苗族自治州委员会", "type": "政协", "level": "地级", "parent": "云南省政协", "location": "文山市"},
    {"id": 5, "name": "中共文山壮族苗族自治州纪律检查委员会", "type": "党委", "level": "地级", "location": "文山市"},

    # Earlier roles
    {"id": 6, "name": "文山州城市建设开发总公司", "type": "事业单位", "level": "县级", "location": "文山市"},
    {"id": 7, "name": "文山州建筑工程有限公司", "type": "事业单位", "level": "县级", "location": "文山市"},
    {"id": 8, "name": "文山州建筑设计院", "type": "事业单位", "level": "县级", "location": "文山市"},
    {"id": 9, "name": "丘北县人民政府", "type": "政府", "level": "县级", "parent": "文山壮族苗族自治州人民政府", "location": "丘北县"},
    {"id": 10, "name": "中共西畴县委员会", "type": "党委", "level": "县级", "parent": "中共文山州委员会", "location": "西畴县"},
    {"id": 11, "name": "文山州人民政府办公室", "type": "政府", "level": "县级", "parent": "文山州人民政府", "location": "文山市"},
    {"id": 12, "name": "文山州审计局", "type": "政府", "level": "县级", "location": "文山市"},
    {"id": 13, "name": "文山州公安局", "type": "政府", "level": "县级", "location": "文山市"},
]

# ── POSITIONS ─────────────────────────────────────────────────────────

positions = [
    # 赵国良 - 州委书记 (no detailed career available)
    {"id": 1, "person_id": 1, "org_id": 1, "title": "州委书记", "start": "2024/2025", "end": "至今", "rank": "正厅级", "note": "接替陈明"},

    # 马忠俊
    {"id": 2, "person_id": 2, "org_id": 6, "title": "生产技术科科长", "start": "1995-07", "end": "1997-02", "rank": "", "note": ""},
    {"id": 3, "person_id": 2, "org_id": 6, "title": "副总经理", "start": "1997-02", "end": "1999-07", "rank": "", "note": "兼文山州建筑工程有限公司经理 (1997.04起)"},
    {"id": 4, "person_id": 2, "org_id": 8, "title": "副院长", "start": "1999-07", "end": "2001-10", "rank": "", "note": "文山州建筑设计院"},
    {"id": 5, "person_id": 2, "org_id": 9, "title": "副县长", "start": "2001-10", "end": "2006-06", "rank": "副处级", "note": "丘北县副县长"},
    {"id": 6, "person_id": 2, "org_id": 10, "title": "县委书记", "start": "2006-06", "end": "2012-10", "rank": "正处级", "note": "西畴县委书记，2007.03-06省委党校中青班"},
    {"id": 7, "person_id": 2, "org_id": 11, "title": "秘书长", "start": "2012-10", "end": "2018-11", "rank": "正处级", "note": "州政府秘书长、办公室党组书记"},
    {"id": 8, "person_id": 2, "org_id": 2, "title": "副州长", "start": "2018-12", "end": "2021-05", "rank": "副厅级", "note": "兼秘书长至2018.12"},
    {"id": 9, "person_id": 2, "org_id": 1, "title": "州委副书记", "start": "2021-05", "end": "至今", "rank": "正厅级", "note": "2021.06任代州长，2021.07任州长"},
    {"id": 10, "person_id": 2, "org_id": 2, "title": "州长", "start": "2021-07", "end": "至今", "rank": "正厅级", "note": ""},

    # 田燕
    {"id": 11, "person_id": 7, "org_id": 2, "title": "副州长", "start": "", "end": "至今", "rank": "副厅级", "note": "负责民宗、卫健、医保等"},

    # 庄宇
    {"id": 12, "person_id": 6, "org_id": 2, "title": "副州长、公安局长", "start": "", "end": "至今", "rank": "副厅级", "note": "负责维稳、公安、司法、信访"},
    {"id": 13, "person_id": 6, "org_id": 13, "title": "局长", "start": "", "end": "至今", "rank": "", "note": "州公安局局长"},

    # 周立军
    {"id": 14, "person_id": 4, "org_id": 1, "title": "州委常委", "start": "", "end": "至今", "rank": "副厅级", "note": ""},
    {"id": 15, "person_id": 4, "org_id": 2, "title": "副州长", "start": "", "end": "至今", "rank": "副厅级", "note": "负责外事、供销等"},

    # 赵国良 - state committee secretary
    {"id": 16, "person_id": 1, "org_id": 1, "title": "州委书记", "start": "2024/2025", "end": "至今", "rank": "正厅级", "note": "现任州委书记"},

    # 陈明 - 前州委书记
    {"id": 17, "person_id": 13, "org_id": 1, "title": "州委书记", "start": "约2020/2021", "end": "约2024", "rank": "正厅级", "note": "前任州委书记，已离任"},

    # 王毅 - 人大
    {"id": 18, "person_id": 11, "org_id": 3, "title": "主任", "start": "", "end": "至今", "rank": "正厅级", "note": "州人大常委会主任"},

    # 吴长昆 - 政协
    {"id": 19, "person_id": 12, "org_id": 4, "title": "主席", "start": "", "end": "至今", "rank": "正厅级", "note": "州政协主席"},

    # 其他副州长
    {"id": 20, "person_id": 3, "org_id": 2, "title": "副州长", "start": "", "end": "至今", "rank": "副厅级", "note": ""},
    {"id": 21, "person_id": 5, "org_id": 2, "title": "副州长", "start": "", "end": "至今", "rank": "副厅级", "note": ""},
    {"id": 22, "person_id": 8, "org_id": 2, "title": "副州长", "start": "", "end": "至今", "rank": "副厅级", "note": ""},
    {"id": 23, "person_id": 9, "org_id": 2, "title": "副州长", "start": "", "end": "至今", "rank": "副厅级", "note": ""},
    {"id": 24, "person_id": 10, "org_id": 2, "title": "秘书长", "start": "", "end": "至今", "rank": "副厅级", "note": ""},

    # 马忠俊 earlier roles
    {"id": 25, "person_id": 2, "org_id": 7, "title": "经理（兼）", "start": "1997-04", "end": "1999-07", "rank": "", "note": "兼文山州建筑工程有限公司经理"},
]

# ── RELATIONSHIPS ─────────────────────────────────────────────────────

relationships = [
    # 马忠俊 → 赵国良 (overlap at current leadership)
    {
        "person_a": 2,
        "person_b": 1,
        "type": "overlap",
        "context": "马忠俊与赵国良在文山州党委和政府核心领导班子共事",
        "overlap_org": "中共文山壮族苗族自治州委员会",
        "overlap_period": "2024/2025-至今",
    },
    # 马忠俊 → 陈明 (predecessor successor in state leadership)
    {
        "person_a": 2,
        "person_b": 13,
        "type": "predecessor_successor",
        "context": "马忠俊在陈明担任州委书记期间任州委副书记、州长",
        "overlap_org": "中共文山壮族苗族自治州委员会",
        "overlap_period": "2021-约2024",
    },
    # 陈明 → 赵国良 (succession)
    {
        "person_a": 13,
        "person_b": 1,
        "type": "predecessor_successor",
        "context": "陈明离任文山州委书记后由赵国良接任",
        "overlap_org": "中共文山壮族苗族自治州委员会",
        "overlap_period": "交接期约2024/2025",
    },
    # 马忠俊 → 周立军 (current work overlap)
    {
        "person_a": 2,
        "person_b": 4,
        "type": "overlap",
        "context": "马忠俊与周立军在州政府班子中共事",
        "overlap_org": "文山壮族苗族自治州人民政府",
        "overlap_period": "至今",
    },
    # 马忠俊 → 庄宇 (government overlap)
    {
        "person_a": 2,
        "person_b": 6,
        "type": "overlap",
        "context": "州长与分管公安的副州长共事",
        "overlap_org": "文山壮族苗族自治州人民政府",
        "overlap_period": "至今",
    },
    # 马忠俊 → 田燕 (政府班子)
    {
        "person_a": 2,
        "person_b": 7,
        "type": "overlap",
        "context": "州政府领导班子成员",
        "overlap_org": "文山壮族苗族自治州人民政府",
        "overlap_period": "至今",
    },
    # 周立军 → 田燕 (同为副职)
    {
        "person_a": 4,
        "person_b": 7,
        "type": "overlap",
        "context": "副州长班子同僚",
        "overlap_org": "文山壮族苗族自治州人民政府",
        "overlap_period": "至今",
    },
    # 庄宇 → 张发政 (政法系统)
    {
        "person_a": 6,
        "person_b": 10,
        "type": "overlap",
        "context": "庄宇主抓政法且秘书长协调州政府事务",
        "overlap_org": "文山壮族苗族自治州人民政府",
        "overlap_period": "至今",
    },
    # 王毅 → 吴长昆 (人大政协)
    {
        "person_a": 11,
        "person_b": 12,
        "type": "overlap",
        "context": "州人大与州政协正职平行共事",
        "overlap_org": "文山州",
        "overlap_period": "至今",
    },
]

# ── BUILD ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    db_path = os.path.join(STAGING, f"{SLUG}_network.db")
    gexf_path = os.path.join(STAGING, f"{SLUG}_network.gexf")

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=db_path,
        gexf_path=gexf_path,
        overwrite=True,
    )
    print(f"Done. DB: {db_path}  GEXF: {gexf_path}")