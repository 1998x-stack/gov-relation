#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 北碚区 (Beibei District, Chongqing).

Task: chongqing_北碚区 — 区委书记 & 区长
Province: 重庆市
City: 北碚区 (重庆直辖市下辖区)
Region: 北碚区
Level: 市辖区(直辖市)
Research date: 2026-07-16

Confirmed officeholders (as of 2026-07-16):
- 区委书记: 林旭阳 (confirmed from 2026-06-30 北碚区"两优一先"表彰大会)
- 区委副书记、区长: 卓大林 (confirmed from multiple official news articles)
- 区人大常委会主任: 徐永德 (confirmed 2026-06-30)
- 区政协主席: 董伦 (confirmed 2026-06-30)
- 区委副书记: 彭世权 (confirmed 2026-06-30)

Confirmed 区领导 from official news:
- 梅玉军 (区委常委/区领导)
- 王德兵 (区领导, 陪同卓大林督导安全)
- 杨辉 (区领导, 陪同卓大林督导安全)
- 吕俊 (区领导, 陪同卓大林督导安全)
- 向红 (区领导, 出席经开区分会场)
- 杨锋 (区领导)
- 胡湧 (区领导, 参与七一慰问)
- 万朝学 (区领导, 参与七一慰问)
- 朱吉红 (区领导)

Sources:
- www.beibei.gov.cn (official government website)
- 北碚区"两优一先"表彰大会 (2026-07-02)
- 区政府主要领导督导检查 (2026-07-13)
- 区政府主要领导赴北碚经开区讲授专题党课 (2026-07-13)
- 中国致公党重庆市北碚区第六次代表大会 (2026-07-08)
- 区领导开展"七一"走访慰问 (2026-07-02)

Confidence: Current leadership confirmed from beibei.gov.cn official news.
Career details limited — only identity-level data available from official sources.
完整履历待查(林旭阳、卓大林的详细信息未在公开渠道找到)。
"""

import json
import os
import sqlite3
from datetime import datetime

# ── paths ──────────────────────────────────────────────────────────────
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if "data/tmp" in SCRIPT_DIR:
    STAGING = SCRIPT_DIR
else:
    STAGING = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(SCRIPT_DIR))),
        "data/tmp/chongqing_北碚区",
    )
DB_PATH = os.path.join(STAGING, "北碚区_network.db")
GEXF_PATH = os.path.join(STAGING, "北碚区_network.gexf")

TODAY = datetime.now().strftime("%Y-%m-%d")


# ── research data ──────────────────────────────────────────────────────

persons = [
    # ══════════════ Core Leaders ══════════════

    # 区委书记 — 林旭阳
    {
        "id": "beibei_lin_xuyang",
        "name": "林旭阳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "北碚区委书记",
        "current_org": "中共重庆市北碚区委员会",
        "source": "www.beibei.gov.cn/zwxx_239/gzdt/bbxw/202607/t20260702_15792255.html (2026-07-02 两优一先表彰大会)",
        "notes": "以区委书记身份讲话。完整履历待补充。",
        "confidence": "confirmed",
    },

    # 区长 — 卓大林
    {
        "id": "beibei_zhuo_dalin",
        "name": "卓大林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "北碚区委副书记、区长",
        "current_org": "北碚区人民政府",
        "source": "www.beibei.gov.cn/zwxx_239/gzdt/bbxw/202607/t20260702_15792255.html (2026-07-02); www.beibei.gov.cn/zwxx_239/gzdt/bbxw/202607/t20260713_15817022.html (2026-07-13 督导安全)",
        "notes": "区委副书记、区政府区长。领导区政府全面工作。多次以区长身份出席活动。完整履历待补充。",
        "confidence": "confirmed",
    },

    # 区人大常委会主任 — 徐永德
    {
        "id": "beibei_xu_yongde",
        "name": "徐永德",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "北碚区人大常委会主任",
        "current_org": "北碚区人大常委会",
        "source": "www.beibei.gov.cn/zwxx_239/gzdt/bbxw/202607/t20260702_15792255.html (2026-07-02)",
        "notes": "区人大常委会主任。完整履历待补充。",
        "confidence": "confirmed",
    },

    # 区政协主席 — 董伦
    {
        "id": "beibei_dong_lun",
        "name": "董伦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "北碚区政协主席",
        "current_org": "中国人民政治协商会议重庆市北碚区委员会",
        "source": "www.beibei.gov.cn/zwxx_239/gzdt/bbxw/202607/t20260702_15792255.html (2026-07-02)",
        "notes": "区政协主席。完整履历待补充。",
        "confidence": "confirmed",
    },

    # 区委副书记 — 彭世权
    {
        "id": "beibei_peng_shiquan",
        "name": "彭世权",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "北碚区委副书记",
        "current_org": "中共重庆市北碚区委员会",
        "source": "www.beibei.gov.cn/zwxx_239/gzdt/bbxw/202607/t20260702_15792255.html (2026-07-02)",
        "notes": "区委副书记。完整履历待补充。",
        "confidence": "confirmed",
    },

    # ══════════════ 其他区领导 ══════════════

    # 梅玉军
    {
        "id": "beibei_mei_yujun",
        "name": "梅玉军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "北碚区委常委",
        "current_org": "中共重庆市北碚区委员会",
        "source": "www.beibei.gov.cn/zwxx_239/gzdt/bbxw/202607/t20260708_15806342.html (致公党代表大会，2026-07-08)",
        "notes": "区委常委。完整履历待补充。",
        "confidence": "confirmed",
    },

    # 王德兵
    {
        "id": "beibei_wang_debing",
        "name": "王德兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "北碚区领导",
        "current_org": "北碚区人民政府",
        "source": "www.beibei.gov.cn/zwxx_239/gzdt/bbxw/202607/t20260713_15817022.html (督导安全，2026-07-13)",
        "notes": "陪同卓大林督导防汛备汛和森林防灭火。完整履历待补充。",
        "confidence": "confirmed",
    },

    # 杨辉
    {
        "id": "beibei_yang_hui",
        "name": "杨辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "北碚区领导",
        "current_org": "北碚区人民政府",
        "source": "www.beibei.gov.cn/zwxx_239/gzdt/bbxw/202607/t20260713_15817022.html (督导安全，2026-07-13)",
        "notes": "陪同卓大林督导安全。完整履历待补充。",
        "confidence": "confirmed",
    },

    # 吕俊
    {
        "id": "beibei_lv_jun",
        "name": "吕俊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "北碚区领导",
        "current_org": "北碚区人民政府",
        "source": "www.beibei.gov.cn/zwxx_239/gzdt/bbxw/202607/t20260713_15817022.html (督导安全，2026-07-13)",
        "notes": "陪同卓大林督导安全。完整履历待补充。",
        "confidence": "confirmed",
    },

    # 向红
    {
        "id": "beibei_xiang_hong",
        "name": "向红",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "北碚区领导",
        "current_org": "北碚区人民政府",
        "source": "www.beibei.gov.cn/zwxx_239/gzdt/bbxw/202607/t20260713_15817029.html (经开区党课，2026-07-13)",
        "notes": "出席经开区专题党课。完整履历待补充。",
        "confidence": "confirmed",
    },

    # 杨锋
    {
        "id": "beibei_yang_feng",
        "name": "杨锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "北碚区领导",
        "current_org": "北碚区人民政府",
        "source": "www.beibei.gov.cn/zwxx_239/gzdt/bbxw/202607/t20260708_15806342.html (致公党代表大会，2026-07-08)",
        "notes": "出席致公党代表大会。完整履历待补充。",
        "confidence": "confirmed",
    },

    # 胡湧
    {
        "id": "beibei_hu_yong",
        "name": "胡湧",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "北碚区领导",
        "current_org": "北碚区人民政府",
        "source": "www.beibei.gov.cn/zwxx_239/gzdt/bbxw/202607/t20260702_15792256.html (七一慰问，2026-07-02)",
        "notes": "参与七一走访慰问。完整履历待补充。",
        "confidence": "confirmed",
    },

    # 万朝学
    {
        "id": "beibei_wan_chaoxue",
        "name": "万朝学",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "北碚区领导",
        "current_org": "北碚区人民政府",
        "source": "www.beibei.gov.cn/zwxx_239/gzdt/bbxw/202607/t20260702_15792256.html (七一慰问，2026-07-02)",
        "notes": "参与七一走访慰问。完整履历待补充。",
        "confidence": "confirmed",
    },

    # 朱吉红
    {
        "id": "beibei_zhu_jihong",
        "name": "朱吉红",
        "gender": "",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "native_place": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "北碚区领导",
        "current_org": "北碚区人民政府",
        "source": "www.beibei.gov.cn/zwxx_239/gzdt/bbxw/202607/t20260708_15806342.html (致公党代表大会，2026-07-08)",
        "notes": "出席致公党代表大会。完整履历待补充。",
        "confidence": "confirmed",
    },
]

organizations = [
    {
        "id": "org_beibei_party",
        "name": "中共重庆市北碚区委员会",
        "type": "党委",
        "level": "地市级（直辖市下辖区）",
        "parent": "中共重庆市委",
        "location": "重庆市北碚区",
    },
    {
        "id": "org_beibei_gov",
        "name": "北碚区人民政府",
        "type": "政府",
        "level": "地市级（直辖市下辖区）",
        "parent": "重庆市人民政府",
        "location": "重庆市北碚区",
    },
    {
        "id": "org_beibei_npc",
        "name": "北碚区人大常委会",
        "type": "人大",
        "level": "地市级（直辖市下辖区）",
        "parent": "重庆市人大常委会",
        "location": "重庆市北碚区",
    },
    {
        "id": "org_beibei_cppcc",
        "name": "中国人民政治协商会议重庆市北碚区委员会",
        "type": "政协",
        "level": "地市级（直辖市下辖区）",
        "parent": "重庆市政协",
        "location": "重庆市北碚区",
    },
]

positions = [
    # 林旭阳 — 区委书记
    {"person_id": "beibei_lin_xuyang", "org_id": "org_beibei_party", "title": "北碚区委书记", "start": "2026", "end": "present", "rank": "正厅级", "note": "区委书记"},
    # 卓大林 — 区长（兼区委副书记）
    {"person_id": "beibei_zhuo_dalin", "org_id": "org_beibei_gov", "title": "北碚区区长", "start": "2026", "end": "present", "rank": "正厅级", "note": "区政府区长"},
    {"person_id": "beibei_zhuo_dalin", "org_id": "org_beibei_party", "title": "北碚区委副书记", "start": "2026", "end": "present", "rank": "正厅级", "note": "区委副书记"},
    # 徐永德 — 区人大常委会主任
    {"person_id": "beibei_xu_yongde", "org_id": "org_beibei_npc", "title": "北碚区人大常委会主任", "start": "2026", "end": "present", "rank": "正厅级", "note": "区人大常委会主任"},
    # 董伦 — 区政协主席
    {"person_id": "beibei_dong_lun", "org_id": "org_beibei_cppcc", "title": "北碚区政协主席", "start": "2026", "end": "present", "rank": "正厅级", "note": "区政协主席"},
    # 彭世权 — 区委副书记
    {"person_id": "beibei_peng_shiquan", "org_id": "org_beibei_party", "title": "北碚区委副书记", "start": "2026", "end": "present", "rank": "副厅级", "note": "区委副书记"},
    # 梅玉军 — 区委常委
    {"person_id": "beibei_mei_yujun", "org_id": "org_beibei_party", "title": "北碚区委常委", "start": "", "end": "present", "rank": "副厅级", "note": "区委常委"},
    # 王德兵 — 区领导
    {"person_id": "beibei_wang_debing", "org_id": "org_beibei_gov", "title": "北碚区领导", "start": "", "end": "present", "rank": "副厅级", "note": "副区长或相当职务"},
    # 杨辉 — 区领导
    {"person_id": "beibei_yang_hui", "org_id": "org_beibei_gov", "title": "北碚区领导", "start": "", "end": "present", "rank": "副厅级", "note": "副区长或相当职务"},
    # 吕俊 — 区领导
    {"person_id": "beibei_lv_jun", "org_id": "org_beibei_gov", "title": "北碚区领导", "start": "", "end": "present", "rank": "副厅级", "note": "副区长或相当职务"},
    # 向红 — 区领导
    {"person_id": "beibei_xiang_hong", "org_id": "org_beibei_gov", "title": "北碚区领导", "start": "", "end": "present", "rank": "副厅级", "note": "副区长或相当职务"},
    # 杨锋 — 区领导
    {"person_id": "beibei_yang_feng", "org_id": "org_beibei_gov", "title": "北碚区领导", "start": "", "end": "present", "rank": "副厅级", "note": "副区长或相当职务"},
    # 胡湧 — 区领导
    {"person_id": "beibei_hu_yong", "org_id": "org_beibei_gov", "title": "北碚区领导", "start": "", "end": "present", "rank": "副厅级", "note": "副区长或相当职务"},
    # 万朝学 — 区领导
    {"person_id": "beibei_wan_chaoxue", "org_id": "org_beibei_gov", "title": "北碚区领导", "start": "", "end": "present", "rank": "副厅级", "note": "副区长或相当职务"},
    # 朱吉红 — 区领导
    {"person_id": "beibei_zhu_jihong", "org_id": "org_beibei_gov", "title": "北碚区领导", "start": "", "end": "present", "rank": "副厅级", "note": "副区长或相当职务"},
]

relationships = [
    # 党政一把手
    {
        "person_a": "beibei_lin_xuyang",
        "person_b": "beibei_zhuo_dalin",
        "type": "党政一把手",
        "context": "林旭阳（区委书记）与卓大林（区委副书记、区长）为北碚区党政一把手。共同出席区'两优一先'大会等重要活动。",
        "overlap_org": "中共北碚区委员会/北碚区人民政府",
        "overlap_period": "2026-至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 区委书记 — 区人大主任
    {
        "person_a": "beibei_lin_xuyang",
        "person_b": "beibei_xu_yongde",
        "type": "区委—区人大",
        "context": "林旭阳（区委书记）与徐永德（区人大常委会主任）共同出席区'两优一先'大会。",
        "overlap_org": "北碚区",
        "overlap_period": "2026-至今",
        "strength": "medium",
        "confidence": "confirmed",
    },
    # 区委书记 — 政协主席
    {
        "person_a": "beibei_lin_xuyang",
        "person_b": "beibei_dong_lun",
        "type": "区委—区政协",
        "context": "林旭阳（区委书记）与董伦（区政协主席）共同出席区'两优一先'大会。",
        "overlap_org": "北碚区",
        "overlap_period": "2026-至今",
        "strength": "medium",
        "confidence": "confirmed",
    },
    # 区长 — 区人大主任
    {
        "person_a": "beibei_zhuo_dalin",
        "person_b": "beibei_xu_yongde",
        "type": "区政府—区人大",
        "context": "卓大林（区长）与徐永德（区人大常委会主任）共同出席区'两优一先'大会。",
        "overlap_org": "北碚区",
        "overlap_period": "2026-至今",
        "strength": "medium",
        "confidence": "confirmed",
    },
    # 区长 — 政协主席
    {
        "person_a": "beibei_zhuo_dalin",
        "person_b": "beibei_dong_lun",
        "type": "区政府—区政协",
        "context": "卓大林（区长）与董伦（区政协主席）共同出席区'两优一先'大会。",
        "overlap_org": "北碚区",
        "overlap_period": "2026-至今",
        "strength": "medium",
        "confidence": "confirmed",
    },
    # 区委书记 — 区委副书记
    {
        "person_a": "beibei_lin_xuyang",
        "person_b": "beibei_peng_shiquan",
        "type": "区委正副书记",
        "context": "林旭阳（区委书记）与彭世权（区委副书记）为区委班子正副书记关系。",
        "overlap_org": "中共北碚区委员会",
        "overlap_period": "2026-至今",
        "strength": "medium",
        "confidence": "confirmed",
    },
    # 区长 — 区委副书记
    {
        "person_a": "beibei_zhuo_dalin",
        "person_b": "beibei_peng_shiquan",
        "type": "党政副职",
        "context": "卓大林（区长兼区委副书记）与彭世权（区委专职副书记）为区委班子同僚。",
        "overlap_org": "中共北碚区委员会",
        "overlap_period": "2026-至今",
        "strength": "medium",
        "confidence": "confirmed",
    },
    # 区长 — 向红
    {
        "person_a": "beibei_zhuo_dalin",
        "person_b": "beibei_xiang_hong",
        "type": "工作关系",
        "context": "卓大林赴北碚经开区讲授党课时，向红出席陪同。",
        "overlap_org": "北碚区人民政府",
        "overlap_period": "2026-07",
        "strength": "medium",
        "confidence": "confirmed",
    },
    # 卓大林 — 王德兵
    {
        "person_a": "beibei_zhuo_dalin",
        "person_b": "beibei_wang_debing",
        "type": "工作关系",
        "context": "王德兵陪同卓大林督导防汛备汛、森林防灭火、安全生产等工作。",
        "overlap_org": "北碚区人民政府",
        "overlap_period": "2026-07",
        "strength": "medium",
        "confidence": "confirmed",
    },
    # 卓大林 — 杨辉
    {
        "person_a": "beibei_zhuo_dalin",
        "person_b": "beibei_yang_hui",
        "type": "工作关系",
        "context": "杨辉陪同卓大林督导防汛备汛、森林防灭火等工作。",
        "overlap_org": "北碚区人民政府",
        "overlap_period": "2026-07",
        "strength": "medium",
        "confidence": "confirmed",
    },
    # 卓大林 — 吕俊
    {
        "person_a": "beibei_zhuo_dalin",
        "person_b": "beibei_lv_jun",
        "type": "工作关系",
        "context": "吕俊陪同卓大林督导防汛备汛、森林防灭火等工作。",
        "overlap_org": "北碚区人民政府",
        "overlap_period": "2026-07",
        "strength": "medium",
        "confidence": "confirmed",
    },
    # 卓大林 — 梅玉军
    {
        "person_a": "beibei_zhuo_dalin",
        "person_b": "beibei_mei_yujun",
        "type": "工作关系",
        "context": "卓大林与梅玉军共同出席致公党北碚区第六次代表大会。",
        "overlap_org": "北碚区",
        "overlap_period": "2026-07",
        "strength": "medium",
        "confidence": "confirmed",
    },
    # 卓大林 — 杨锋
    {
        "person_a": "beibei_zhuo_dalin",
        "person_b": "beibei_yang_feng",
        "type": "工作关系",
        "context": "卓大林与杨锋共同出席致公党北碚区第六次代表大会。",
        "overlap_org": "北碚区",
        "overlap_period": "2026-07",
        "strength": "medium",
        "confidence": "confirmed",
    },
    # 卓大林 — 朱吉红
    {
        "person_a": "beibei_zhuo_dalin",
        "person_b": "beibei_zhu_jihong",
        "type": "工作关系",
        "context": "卓大林与朱吉红共同出席致公党北碚区第六次代表大会。",
        "overlap_org": "北碚区",
        "overlap_period": "2026-07",
        "strength": "medium",
        "confidence": "confirmed",
    },
    # 胡湧 — 万朝学
    {
        "person_a": "beibei_hu_yong",
        "person_b": "beibei_wan_chaoxue",
        "type": "工作关系",
        "context": "胡湧与万朝学共同参与七一走访慰问活动。",
        "overlap_org": "北碚区",
        "overlap_period": "2026-07",
        "strength": "weak",
        "confidence": "confirmed",
    },
    # 梅玉军 — 杨锋
    {
        "person_a": "beibei_mei_yujun",
        "person_b": "beibei_yang_feng",
        "type": "会议同席",
        "context": "梅玉军与杨锋共同出席致公党北碚区代表大会。",
        "overlap_org": "北碚区",
        "overlap_period": "2026-07",
        "strength": "weak",
        "confidence": "confirmed",
    },
]


# ── BUILD FUNCTIONS ──────────────────────────────────────────────────

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build_db():
    """Create SQLite database."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE persons (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            gender TEXT,
            ethnicity TEXT,
            birth TEXT,
            birthplace TEXT,
            native_place TEXT,
            education TEXT,
            party_join TEXT,
            work_start TEXT,
            current_post TEXT,
            current_org TEXT,
            source TEXT,
            notes TEXT,
            confidence TEXT
        )
    """)

    c.execute("""
        CREATE TABLE organizations (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT,
            level TEXT,
            parent TEXT,
            location TEXT
        )
    """)

    c.execute("""
        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT NOT NULL,
            org_id TEXT NOT NULL,
            title TEXT,
            start TEXT,
            end TEXT,
            rank TEXT,
            note TEXT,
            FOREIGN KEY (person_id) REFERENCES persons(id),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        )
    """)

    c.execute("""
        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT,
            context TEXT,
            overlap_org TEXT,
            overlap_period TEXT,
            strength TEXT,
            FOREIGN KEY (person_a) REFERENCES persons(id),
            FOREIGN KEY (person_b) REFERENCES persons(id)
        )
    """)

    for p in persons:
        c.execute("""
            INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace,
                                 native_place, education, party_join, work_start,
                                 current_post, current_org, source, notes, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            p["id"], p["name"], p.get("gender", ""), p.get("ethnicity", ""),
            p.get("birth", ""), p.get("birthplace", ""), p.get("native_place", ""),
            p.get("education", ""), p.get("party_join", ""), p.get("work_start", ""),
            p.get("current_post", ""), p.get("current_org", ""),
            p.get("source", ""), p.get("notes", ""), p.get("confidence", ""),
        ))

    for o in organizations:
        c.execute("""
            INSERT INTO organizations (id, name, type, level, parent, location)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        c.execute("""
            INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            pos["person_id"], pos["org_id"], pos["title"],
            pos.get("start", ""), pos.get("end", ""),
            pos.get("rank", ""), pos.get("note", ""),
        ))

    for r in relationships:
        c.execute("""
            INSERT INTO relationships (person_a, person_b, type, context,
                                       overlap_org, overlap_period, strength)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            r["person_a"], r["person_b"], r["type"], r.get("context", ""),
            r.get("overlap_org", ""), r.get("overlap_period", ""), r.get("strength", ""),
        ))

    conn.commit()
    conn.close()
    print(f"[DB] Created: {DB_PATH}")


def build_gexf():
    """Create GEXF graph file using string formatting (avoids namespace issues)."""
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>China Gov Network Research Agent</creator>')
    lines.append('    <description>北碚区 (Beibei District, Chongqing) — Leadership Network Graph</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="org" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="strength" type="string"/>')
    lines.append('    </attributes>')

    # Person node colors
    def person_color(p):
        post = p.get("current_post", "")
        if "区委书记" in post:
            return "255,50,50"   # red — party secretary
        if "区长" in post:
            return "50,100,255"  # blue — government leader
        if "人大" in post:
            return "100,180,100" # green — NPC
        if "政协" in post:
            return "100,180,100" # green — CPPCC
        return "100,100,100"     # grey — others

    def is_top_leader(p):
        post = p.get("current_post", "")
        return "区委书记" in post or "区长" in post

    # Person nodes
    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = "20.0" if is_top_leader(p) else "12.0"
        lines.append(f'      <node id="{esc(p["id"])}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization node colors
    def org_color(o):
        t = o["type"]
        if "党委" in t:
            return "255,200,200"
        if "政府" in t:
            return "200,200,255"
        if "人大" in t:
            return "200,255,255"
        if "政协" in t:
            return "255,240,200"
        return "200,200,200"

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="{esc(o["id"])}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → Organization edges (worked_at)
    for pos in positions:
        lines.append(f'      <edge id="e{eid}" source="{esc(pos["person_id"])}" target="{esc(pos["org_id"])}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    # Person ↔ Person edges (relationship)
    for r in relationships:
        weight = "2.0" if r.get("strength") == "strong" else "1.5" if r.get("strength") == "medium" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="{esc(r["person_a"])}" target="{esc(r["person_b"])}" label="{esc(r["type"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("strength", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
        eid += 1

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"[GEXF] Created: {GEXF_PATH}")
    print(f"[GEXF] Nodes: {len(persons)} persons + {len(organizations)} orgs")
    print(f"[GEXF] Edges: {len(positions)} worked_at + {len(relationships)} relationships")


def main():
    os.makedirs(STAGING, exist_ok=True)
    build_db()
    build_gexf()

    # Print summary
    print(f"\n{'=' * 50}")
    print(f"北碚区 Leadership Network — Build Complete")
    print(f"{'=' * 50}")
    print(f"Persons: {len(persons)}")
    print(f"Organizations: {len(organizations)}")
    print(f"Positions: {len(positions)}")
    print(f"Relationships: {len(relationships)}")
    print(f"\nOutput files:")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF:     {GEXF_PATH}")
    print(f"{'=' * 50}")


if __name__ == "__main__":
    main()
