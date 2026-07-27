#!/usr/bin/env python3
"""蠡县 (Lixian, Baoding, Hebei) personnel network data builder.

Sources:
- lixian.gov.cn (政府领导信息 page, 2026-01-28)
- lixian.gov.cn news articles (2024-2026)
- zh.wikipedia.org/wiki/蠡县
"""

from __future__ import annotations

from gov_relation.paths import DATABASE_DIR, GRAPH_DIR, REPO_ROOT as BASE_DIR
from gov_relation.runner import run_build

# ── Persons ──────────────────────────────────────────────────────────
persons = [
    # ── Core leaders ──
    {
        "id": 1,
        "name": "高波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共蠡县委员会",
        "source": "https://www.lixian.gov.cn/content-173-92893.html; https://www.lixian.gov.cn/content-173-92646.html",
    },
    {
        "id": 2,
        "name": "王文刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "蠡县人民政府",
        "source": "https://www.lixian.gov.cn/ejjgszlist-1003-more.html",
    },
    # ── 人大/政协 ──
    {
        "id": 3,
        "name": "吴素杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "蠡县人大常委会",
        "source": "https://www.lixian.gov.cn/content-252-91283.html",
    },
    {
        "id": 4,
        "name": "许占杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导（人大）",
        "current_org": "蠡县人大常委会",
        "source": "https://www.lixian.gov.cn/content-173-92893.html",
    },
    # ── 县政府班子成员 ──
    {
        "id": 5,
        "name": "阮玉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "蠡县人民政府",
        "source": "https://www.lixian.gov.cn/content-252-90799.html",
    },
    {
        "id": 6,
        "name": "李小虎",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县政府负责人",
        "current_org": "蠡县人民政府",
        "source": "https://www.lixian.gov.cn/ejjgszlist-1003-more.html",
    },
    {
        "id": 7,
        "name": "吕高飞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府党组成员、副县长、县公安局局长",
        "current_org": "蠡县人民政府",
        "source": "https://www.lixian.gov.cn/ejjgszlist-1003-more.html",
    },
    {
        "id": 8,
        "name": "何晓阳",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "蠡县人民政府",
        "source": "https://www.lixian.gov.cn/ejjgszlist-1003-more.html",
    },
    {
        "id": 9,
        "name": "马巍",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府负责人",
        "current_org": "蠡县人民政府",
        "source": "https://www.lixian.gov.cn/ejjgszlist-1003-more.html",
    },
    {
        "id": 10,
        "name": "王杨",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府负责人",
        "current_org": "蠡县人民政府",
        "source": "https://www.lixian.gov.cn/ejjgszlist-1003-more.html",
    },
    {
        "id": 11,
        "name": "武旭朝",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政府负责人",
        "current_org": "蠡县人民政府",
        "source": "https://www.lixian.gov.cn/ejjgszlist-1003-more.html",
    },
    {
        "id": 12,
        "name": "陈红玉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "蠡县人民政府",
        "source": "https://www.lixian.gov.cn/content-252-90799.html",
    },
    {
        "id": 13,
        "name": "王建伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "蠡县人民政府",
        "source": "https://www.lixian.gov.cn/content-173-92893.html",
    },
    # ── 其他县领导（从新闻中出现的） ──
    {
        "id": 14,
        "name": "王艳宾",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "蠡县",
        "source": "https://www.lixian.gov.cn/content-252-91283.html",
    },
    {
        "id": 15,
        "name": "杜殿海",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "蠡县",
        "source": "https://www.lixian.gov.cn/content-252-91283.html",
    },
    {
        "id": 16,
        "name": "苑东念",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "蠡县",
        "source": "https://www.lixian.gov.cn/content-173-92893.html",
    },
    {
        "id": 17,
        "name": "李朋朋",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "蠡县",
        "source": "https://www.lixian.gov.cn/content-173-92893.html",
    },
    {
        "id": 18,
        "name": "李光",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "蠡县",
        "source": "https://www.lixian.gov.cn/content-252-91283.html",
    },
    {
        "id": 19,
        "name": "魏娜",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协副主席",
        "current_org": "蠡县政协",
        "source": "https://www.lixian.gov.cn/content-252-90799.html",
    },
    {
        "id": 20,
        "name": "张志辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县经济开发区党工委副书记、管委会常务副主任",
        "current_org": "蠡县经济开发区",
        "source": "https://www.lixian.gov.cn/content-252-90799.html",
    },
    # ── 前任领导 ──
    {
        "id": 21,
        "name": "陈伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "前任县委书记（已离任）",
        "current_org": "中共蠡县委员会（前任）",
        "source": "https://www.lixian.gov.cn/content-252-89786.html",
    },
    # ── 从领导慰问文章中出现的其他领导 ──
    {
        "id": 22,
        "name": "独宇明",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "蠡县",
        "source": "https://www.lixian.gov.cn/content-252-32728.html",
    },
    {
        "id": 23,
        "name": "王天宝",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县领导",
        "current_org": "蠡县",
        "source": "https://www.lixian.gov.cn/content-252-32728.html",
    },
    # ── 人大常委会委员 ──
    {
        "id": 24,
        "name": "边永",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "蠡县人大常委会",
        "source": "https://www.lixian.gov.cn/content-173-93174.html",
    },
]

# ── Organizations ─────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共蠡县委员会", "type": "党委", "level": "县处级", "parent": "中共保定市委", "location": "保定市蠡县"},
    {"id": 2, "name": "蠡县人民政府", "type": "政府", "level": "县处级", "parent": "保定市人民政府", "location": "保定市蠡县"},
    {"id": 3, "name": "蠡县人大常委会", "type": "人大", "level": "县处级", "parent": "", "location": "保定市蠡县"},
    {"id": 4, "name": "蠡县政协", "type": "政协", "level": "县处级", "parent": "", "location": "保定市蠡县"},
    {"id": 5, "name": "蠡县公安局", "type": "政府", "level": "乡科级", "parent": "蠡县人民政府", "location": "保定市蠡县"},
    {"id": 6, "name": "蠡县经济开发区", "type": "开发区", "level": "乡科级", "parent": "蠡县人民政府", "location": "保定市蠡县"},
    {"id": 7, "name": "中共保定市委", "type": "党委", "level": "地厅级", "parent": "中共河北省委", "location": "保定市"},
    {"id": 8, "name": "保定市人民政府", "type": "政府", "level": "地厅级", "parent": "河北省人民政府", "location": "保定市"},
    {"id": 9, "name": "蠡县", "type": "政府", "level": "县处级", "parent": "保定市", "location": "保定市蠡县"},
]

# ── Positions ────────────────────────────────────────────────────────
positions = [
    # 高波
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start": "2025", "end": "present", "rank": "县处级正职", "note": "前任为陈伟；之前任蠡县县长", "source": "https://www.lixian.gov.cn/content-173-92646.html"},
    {"person_id": 1, "org_id": 2, "title": "县长（前任）", "start": "~2021", "end": "2025", "rank": "县处级正职", "note": "与县委书记陈伟搭班；后升任县委书记", "source": "https://www.lixian.gov.cn/content-252-89786.html"},
    # 王文刚
    {"person_id": 2, "org_id": 2, "title": "县长", "start": "2025", "end": "present", "rank": "县处级正职", "note": "接替高波任县长", "source": "https://www.lixian.gov.cn/ejjgszlist-1003-more.html"},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start": "2025", "end": "present", "rank": "县处级副职", "note": "", "source": "https://www.lixian.gov.cn/content-252-91283.html"},
    # 吴素杰
    {"person_id": 3, "org_id": 3, "title": "县人大常委会主任", "start": "", "end": "present", "rank": "县处级正职", "note": "", "source": "https://www.lixian.gov.cn/content-252-91283.html"},
    # 许占杰
    {"person_id": 4, "org_id": 3, "title": "县领导（人大）", "start": "", "end": "present", "rank": "县处级", "note": "出现在2026年春节慰问活动中", "source": "https://www.lixian.gov.cn/content-173-92893.html"},
    # 阮玉
    {"person_id": 5, "org_id": 2, "title": "县委常委、常务副县长", "start": "", "end": "present", "rank": "县处级副职", "note": "", "source": "https://www.lixian.gov.cn/content-252-90799.html"},
    {"person_id": 5, "org_id": 1, "title": "县委常委", "start": "", "end": "present", "rank": "县处级副职", "note": "", "source": "https://www.lixian.gov.cn/content-252-90799.html"},
    # 李小虎
    {"person_id": 6, "org_id": 2, "title": "县委常委、县政府负责人", "start": "", "end": "present", "rank": "县处级副职", "note": "", "source": "https://www.lixian.gov.cn/ejjgszlist-1003-more.html"},
    # 吕高飞
    {"person_id": 7, "org_id": 2, "title": "副县长、县公安局局长", "start": "", "end": "present", "rank": "县处级副职", "note": "", "source": "https://www.lixian.gov.cn/ejjgszlist-1003-more.html"},
    {"person_id": 7, "org_id": 5, "title": "县公安局局长", "start": "", "end": "present", "rank": "乡科级正职", "note": "", "source": "https://www.lixian.gov.cn/ejjgszlist-1003-more.html"},
    # 何晓阳
    {"person_id": 8, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "县处级副职", "note": "", "source": "https://www.lixian.gov.cn/ejjgszlist-1003-more.html"},
    # 马巍
    {"person_id": 9, "org_id": 2, "title": "县政府负责人", "start": "", "end": "present", "rank": "县处级", "note": "", "source": "https://www.lixian.gov.cn/ejjgszlist-1003-more.html"},
    # 王杨
    {"person_id": 10, "org_id": 2, "title": "县政府负责人", "start": "", "end": "present", "rank": "县处级", "note": "", "source": "https://www.lixian.gov.cn/ejjgszlist-1003-more.html"},
    # 武旭朝
    {"person_id": 11, "org_id": 2, "title": "县政府负责人", "start": "", "end": "present", "rank": "县处级", "note": "", "source": "https://www.lixian.gov.cn/ejjgszlist-1003-more.html"},
    # 陈红玉
    {"person_id": 12, "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "县处级副职", "note": "", "source": "https://www.lixian.gov.cn/content-252-90799.html"},
    # 王建伟
    {"person_id": 13, "org_id": 9, "title": "县领导", "start": "", "end": "present", "rank": "县处级", "note": "", "source": "https://www.lixian.gov.cn/content-173-92893.html"},
    # 王艳宾
    {"person_id": 14, "org_id": 9, "title": "县领导", "start": "", "end": "present", "rank": "县处级", "note": "出现在2025年7月重点项目建设现场办公活动中", "source": "https://www.lixian.gov.cn/content-252-91283.html"},
    # 杜殿海
    {"person_id": 15, "org_id": 9, "title": "县领导", "start": "", "end": "present", "rank": "县处级", "note": "", "source": "https://www.lixian.gov.cn/content-252-91283.html"},
    # 苑东念
    {"person_id": 16, "org_id": 9, "title": "县领导", "start": "", "end": "present", "rank": "县处级", "note": "", "source": "https://www.lixian.gov.cn/content-173-92893.html"},
    # 李朋朋
    {"person_id": 17, "org_id": 9, "title": "县领导", "start": "", "end": "present", "rank": "县处级", "note": "", "source": "https://www.lixian.gov.cn/content-173-92893.html"},
    # 李光
    {"person_id": 18, "org_id": 9, "title": "县领导", "start": "", "end": "present", "rank": "县处级", "note": "", "source": "https://www.lixian.gov.cn/content-252-91283.html"},
    # 魏娜
    {"person_id": 19, "org_id": 4, "title": "县政协副主席", "start": "", "end": "present", "rank": "县处级副职", "note": "", "source": "https://www.lixian.gov.cn/content-252-90799.html"},
    # 张志辉
    {"person_id": 20, "org_id": 6, "title": "县经济开发区党工委副书记、管委会常务副主任", "start": "", "end": "present", "rank": "乡科级正职", "note": "", "source": "https://www.lixian.gov.cn/content-252-90799.html"},
    # 陈伟（前任县委书记）
    {"person_id": 21, "org_id": 1, "title": "县委书记（前任）", "start": "~2020", "end": "2025", "rank": "县处级正职", "note": "接任者高波；2024年9月仍以县委书记身份活动", "source": "https://www.lixian.gov.cn/content-252-89786.html; https://www.lixian.gov.cn/content-252-32728.html"},
    # 独宇明
    {"person_id": 22, "org_id": 9, "title": "县领导", "start": "", "end": "present", "rank": "县处级", "note": "出现在2024年9月陈伟带队活动中", "source": "https://www.lixian.gov.cn/content-252-32728.html"},
    # 王天宝
    {"person_id": 23, "org_id": 9, "title": "县领导", "start": "", "end": "present", "rank": "县处级", "note": "出现在2024年9月陈伟带队活动中", "source": "https://www.lixian.gov.cn/content-252-32728.html"},
    # 边永
    {"person_id": 24, "org_id": 3, "title": "县人大常委会副主任", "start": "", "end": "present", "rank": "县处级副职", "note": "", "source": "https://www.lixian.gov.cn/content-173-93174.html"},
]

# ── Relationships ────────────────────────────────────────────────────
relationships = [
    # 上下级/搭班关系（同县党政班子）
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "高波（县委书记）和王文刚（县长）为当前党政正职搭班", "overlap_org": "中共蠡县委员会/蠡县人民政府", "overlap_period": "2025-present", "source": "https://www.lixian.gov.cn/content-173-92646.html"},
    # 前任-继任关系（县长岗位）
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor", "context": "高波此前任县长，后升任县委书记；王文刚接任县长", "overlap_org": "蠡县人民政府", "overlap_period": "2025", "source": "https://www.lixian.gov.cn/ejjgszlist-1003-more.html"},
    # 前任-继任关系（书记岗位）
    {"person_a": 21, "person_b": 1, "type": "predecessor_successor", "context": "陈伟此前任县委书记，高波接任", "overlap_org": "中共蠡县委员会", "overlap_period": "2020-2025", "source": "https://www.lixian.gov.cn/content-252-89786.html"},
    # 搭班（陈伟+高波）
    {"person_a": 21, "person_b": 1, "type": "overlap", "context": "陈伟（县委书记）与高波（县长）搭班", "overlap_org": "中共蠡县委员会/蠡县人民政府", "overlap_period": "~2021-2025", "source": "https://www.lixian.gov.cn/content-252-89786.html"},
    # 常务副县长与县长
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "王文刚（县长）与阮玉（常务副县长）", "overlap_org": "蠡县人民政府", "overlap_period": "2025-present", "source": "https://www.lixian.gov.cn/content-173-92893.html"},
    # 高波与阮玉
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate", "context": "高波（书记/前县长）与阮玉（常务副县长）长期共事", "overlap_org": "蠡县人民政府/中共蠡县委员会", "overlap_period": "~2021-present", "source": "https://www.lixian.gov.cn/content-173-92893.html"},
    # 公安局领导与县长
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "王文刚（县长）与吕高飞（副县长兼公安局局长）", "overlap_org": "蠡县人民政府", "overlap_period": "2025-present", "source": "https://www.lixian.gov.cn/ejjgszlist-1003-more.html"},
]

# ── Run ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    staging = False
    import sys
    if "--staging" in sys.argv:
        staging = True

    if staging:
        db_path = BASE_DIR / "data/tmp/hebei_蠡县/蠡县_network.db"
        gexf_path = BASE_DIR / "data/tmp/hebei_蠡县/蠡县_network.gexf"
    else:
        db_path = DATABASE_DIR / "蠡县_network.db"
        gexf_path = GRAPH_DIR / "蠡县_network.gexf"

    run_build(
        slug="蠡县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=db_path,
        gexf_path=gexf_path,
        overwrite=True,
    )
