#!/usr/bin/env python3
"""Build script for 青神县 (眉山市·四川省) government personnel network data.

Generated: 2026-07-26
Sources:
  - Official site (scqs.gov.cn): https://www.scqs.gov.cn/zwgk/jbxxgk/ldzc/xwld.htm (县委领导)
  - Official site: https://www.scqs.gov.cn/zwgk/jbxxgk/ldzc/xzfld.htm (县政府领导)
  - Official site: https://www.scqs.gov.cn/zwgk/jbxxgk/ldzc/xrdld.htm (县人大领导)
  - Official site: https://www.scqs.gov.cn/zwgk/jbxxgk/ldzc/xzxld.htm (县政协领导)
  - Official bio pages for each leader (individual detail pages)
  - News articles on scqs.gov.cn (2026年7月)
  - Baidu Baike: 周代军 (for cross-county connection via 青神 career start)
  - Baidu Baike: 李忠云 (for cross-county connection: served as 青神县委常委、常务副县长 2016-2018)
  - Existing repo: build_洪雅县_data.py (cross-county exchange data)
"""

import os, sys, json
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "青神县"

# ── Persons ──
# id is INTEGER PRIMARY KEY in schema
# NOTE: 邱磊 serves as BOTH 县委书记 AND 县长 (一肩挑 arrangement)
persons = [
    # ═══════════════════════════════════════════════════════════════════
    # 1. County Party Leadership (县委领导)
    # ═══════════════════════════════════════════════════════════════════
    {
        "id": 1,
        "name": "邱磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年1月",
        "birthplace": "",
        "education": "党校研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "青神县委书记、县政府县长（一肩挑）",
        "current_org": "中共青神县委/青神县人民政府",
        "source": "https://www.scqs.gov.cn/info/11120/227836.htm"
    },
    {
        "id": 2,
        "name": "黄勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年8月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "青神县委副书记",
        "current_org": "中共青神县委",
        "source": "https://www.scqs.gov.cn/info/11120/120701.htm"
    },
    {
        "id": 3,
        "name": "程玉",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1983年6月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "青神县委常委、县政府副县长（常务）",
        "current_org": "中共青神县委/青神县人民政府",
        "source": "https://www.scqs.gov.cn/info/11120/221279.htm"
    },
    {
        "id": 4,
        "name": "廖长明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年5月",
        "birthplace": "",
        "education": "大学本科学历",
        "party_join": "",
        "work_start": "",
        "current_post": "青神县委常委、政法委书记",
        "current_org": "中共青神县委",
        "source": "https://www.scqs.gov.cn/info/11120/168917.htm"
    },
    {
        "id": 5,
        "name": "李泽",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年2月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "青神县委常委、组织部部长",
        "current_org": "中共青神县委",
        "source": "https://www.scqs.gov.cn/info/11120/215870.htm"
    },
    {
        "id": 6,
        "name": "杨玉刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年2月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "青神县委常委、县纪委书记、县监委主任",
        "current_org": "青神县纪委监委",
        "source": "https://www.scqs.gov.cn/info/11120/222900.htm"
    },
    {
        "id": 7,
        "name": "王果",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985年1月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "青神县委常委、县总工会主席",
        "current_org": "中共青神县委/县总工会",
        "source": "https://www.scqs.gov.cn/info/11120/203598.htm"
    },
    {
        "id": 8,
        "name": "杨燕强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年5月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "青神县委常委、统战部部长",
        "current_org": "中共青神县委",
        "source": "https://www.scqs.gov.cn/info/11120/221278.htm"
    },
    {
        "id": 9,
        "name": "张勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年12月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "",
        "work_start": "",
        "current_post": "青神县委常委、宣传部部长",
        "current_org": "中共青神县委",
        "source": "https://www.scqs.gov.cn/info/11120/203770.htm"
    },
    # ═══════════════════════════════════════════════════════════════════
    # 2. 县政府其他领导
    # ═══════════════════════════════════════════════════════════════════
    {
        "id": 10,
        "name": "梁颖",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "青神县人民政府副县长",
        "current_org": "青神县人民政府",
        "source": "https://www.scqs.gov.cn/info/6028/168521.htm"
    },
    {
        "id": 11,
        "name": "向煊锋",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "青神县人民政府副县长",
        "current_org": "青神县人民政府",
        "source": "https://www.scqs.gov.cn/info/6028/168524.htm"
    },
    {
        "id": 12,
        "name": "陈晓红",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "青神县人民政府副县长",
        "current_org": "青神县人民政府",
        "source": "https://www.scqs.gov.cn/info/6028/221282.htm"
    },
    {
        "id": 13,
        "name": "文伟",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "青神县人民政府副县长、县公安局党委书记、局长",
        "current_org": "青神县人民政府/青神县公安局",
        "source": "https://www.scqs.gov.cn/info/6028/170122.htm"
    },
    {
        "id": 14,
        "name": "王超",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "青神县人民政府副县长",
        "current_org": "青神县人民政府",
        "source": "https://www.scqs.gov.cn/info/6028/212752.htm"
    },
    # ═══════════════════════════════════════════════════════════════════
    # 3. 县人大领导
    # ═══════════════════════════════════════════════════════════════════
    {
        "id": 15,
        "name": "卢明春",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "青神县人大常委会党组书记、主任",
        "current_org": "青神县人大常委会",
        "source": "https://www.scqs.gov.cn/zwgk/jbxxgk/ldzc/xrdld.htm"
    },
    {
        "id": 16,
        "name": "彭志军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "青神县人大常委会党组副书记、副主任",
        "current_org": "青神县人大常委会",
        "source": "https://www.scqs.gov.cn/zwgk/jbxxgk/ldzc/xrdld.htm"
    },
    {
        "id": 17,
        "name": "郑学敏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "青神县人大常委会副主任",
        "current_org": "青神县人大常委会",
        "source": "https://www.scqs.gov.cn/zwgk/jbxxgk/ldzc/xrdld.htm"
    },
    {
        "id": 18,
        "name": "王军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "青神县人大常委会党组成员、副主任",
        "current_org": "青神县人大常委会",
        "source": "https://www.scqs.gov.cn/zwgk/jbxxgk/ldzc/xrdld.htm"
    },
    {
        "id": 19,
        "name": "刘建林",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "青神县人大常委会党组成员、副主任",
        "current_org": "青神县人大常委会",
        "source": "https://www.scqs.gov.cn/zwgk/jbxxgk/ldzc/xrdld.htm"
    },
    # ═══════════════════════════════════════════════════════════════════
    # 4. 县政协领导
    # ═══════════════════════════════════════════════════════════════════
    {
        "id": 20,
        "name": "陈开军",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "青神县政协主席、党组书记",
        "current_org": "政协青神县委员会",
        "source": "https://www.scqs.gov.cn/info/6029/133211.htm"
    },
    {
        "id": 21,
        "name": "涂成钢",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "青神县政协副主席",
        "current_org": "政协青神县委员会",
        "source": "https://www.scqs.gov.cn/info/6029/40169.htm"
    },
    {
        "id": 22,
        "name": "李仕贵",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "青神县政协副主席、党组副书记",
        "current_org": "政协青神县委员会",
        "source": "https://www.scqs.gov.cn/info/6029/169630.htm"
    },
    {
        "id": 23,
        "name": "刘勇义",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "青神县政协副主席、县工商联主席",
        "current_org": "政协青神县委员会/县工商联",
        "source": "https://www.scqs.gov.cn/info/6029/169631.htm"
    },
    {
        "id": 24,
        "name": "尹永刚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "青神县政协副主席",
        "current_org": "政协青神县委员会",
        "source": "https://www.scqs.gov.cn/info/6029/169632.htm"
    },
    {
        "id": 25,
        "name": "余卫红",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "青神县政协秘书长、党组成员",
        "current_org": "政协青神县委员会",
        "source": "https://www.scqs.gov.cn/info/6029/169633.htm"
    },
    # ═══════════════════════════════════════════════════════════════════
    # 5. Cross-county exchange figures (from 洪雅县 research)
    # ═══════════════════════════════════════════════════════════════════
    {
        "id": 26,
        "name": "李忠云",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年11月",
        "birthplace": "四川井研",
        "education": "四川大学行政管理（自考）；省委党校经济管理（本科）",
        "party_join": "1996年6月",
        "work_start": "1994年8月",
        "current_post": "洪雅县委副书记、县长",
        "current_org": "洪雅县人民政府",
        "source": "https://baike.baidu.com/item/%E6%9D%8E%E5%BF%A0%E4%BA%91/20241483"
    },
    {
        "id": 27,
        "name": "周代军",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1974年11月",
        "birthplace": "重庆彭水",
        "education": "四川工业学院（西华大学）建筑工程系 大学学历",
        "party_join": "1995年12月",
        "work_start": "1998年7月",
        "current_post": "眉山市副市长、洪雅县委书记",
        "current_org": "眉山市人民政府/中共洪雅县委",
        "source": "https://baike.baidu.com/item/%E5%91%A8%E4%BB%A3%E5%86%9B/23219420"
    },
]

# ── Organizations ──

organizations = [
    {"id": 1, "name": "中共青神县委", "type": "党委", "level": "县", "parent": "中共眉山市委", "location": "四川省眉山市青神县"},
    {"id": 2, "name": "青神县人民政府", "type": "政府", "level": "县", "parent": "眉山市人民政府", "location": "四川省眉山市青神县"},
    {"id": 3, "name": "青神县人大常委会", "type": "人大", "level": "县", "parent": "眉山市人大常委会", "location": "四川省眉山市青神县"},
    {"id": 4, "name": "政协青神县委员会", "type": "政协", "level": "县", "parent": "政协眉山市委员会", "location": "四川省眉山市青神县"},
    {"id": 5, "name": "青神县纪委监委", "type": "纪委", "level": "县", "parent": "中共青神县委", "location": "四川省眉山市青神县"},
    {"id": 6, "name": "青神县委统战部", "type": "党委", "level": "县", "parent": "中共青神县委", "location": "四川省眉山市青神县"},
    {"id": 7, "name": "青神县委政法委", "type": "党委", "level": "县", "parent": "中共青神县委", "location": "四川省眉山市青神县"},
    {"id": 8, "name": "青神县委宣传部", "type": "党委", "level": "县", "parent": "中共青神县委", "location": "四川省眉山市青神县"},
    {"id": 9, "name": "青神县委组织部", "type": "党委", "level": "县", "parent": "中共青神县委", "location": "四川省眉山市青神县"},
    {"id": 10, "name": "青神县总工会", "type": "群团", "level": "县", "parent": "中共青神县委", "location": "四川省眉山市青神县"},
    {"id": 11, "name": "青神县公安局", "type": "政府", "level": "县", "parent": "青神县人民政府", "location": "四川省眉山市青神县"},
    {"id": 12, "name": "青神县工商业联合会", "type": "群团", "level": "县", "parent": "中共青神县委", "location": "四川省眉山市青神县"},
    # Cross-county orgs (for exchange connections)
    {"id": 13, "name": "中共眉山市委", "type": "党委", "level": "地市", "parent": "中共四川省委", "location": "四川省眉山市"},
    {"id": 14, "name": "眉山市人民政府", "type": "政府", "level": "地市", "parent": "四川省人民政府", "location": "四川省眉山市"},
    {"id": 15, "name": "眉山市委组织部", "type": "党委", "level": "地市", "parent": "中共眉山市委", "location": "四川省眉山市"},
    {"id": 16, "name": "洪雅县人民政府", "type": "政府", "level": "县", "parent": "眉山市人民政府", "location": "四川省眉山市洪雅县"},
    {"id": 17, "name": "中共洪雅县委", "type": "党委", "level": "县", "parent": "中共眉山市委", "location": "四川省眉山市洪雅县"},
    {"id": 18, "name": "中共彭山区委", "type": "党委", "level": "县", "parent": "中共眉山市委", "location": "四川省眉山市彭山区"},
    {"id": 19, "name": "彭山区人民政府", "type": "政府", "level": "县", "parent": "眉山市人民政府", "location": "四川省眉山市彭山区"},
]

# ── Positions ──

positions = [
    # 邱磊 (id=1) — 县委书记兼县长
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "一肩挑县委书记和县长职务"},
    {"person_id": 1, "org_id": 2, "title": "县政府县长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "兼县长"},
    # NOTE: 邱磊的此前履历在政府官网上未列出，待补充

    # 黄勇 (id=2) — 县委副书记
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "协助抓党建工作"},
    # NOTE: 黄勇的此前履历在政府官网上未列出

    # 程玉 (id=3) — 县委常委、常务副县长
    {"person_id": 3, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "分管县政府常务工作"},
    {"person_id": 3, "org_id": 2, "title": "县政府副县长（常务）", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},

    # 廖长明 (id=4) — 县委常委、政法委书记
    {"person_id": 4, "org_id": 1, "title": "县委常委、政法委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},

    # 李泽 (id=5) — 县委常委、组织部部长
    {"person_id": 5, "org_id": 1, "title": "县委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},

    # 杨玉刚 (id=6) — 县委常委、纪委书记
    {"person_id": 6, "org_id": 1, "title": "县委常委、县纪委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 6, "org_id": 5, "title": "县监委主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},

    # 王果 (id=7) — 县委常委、总工会主席
    {"person_id": 7, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 7, "org_id": 10, "title": "县总工会主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},

    # 杨燕强 (id=8) — 县委常委、统战部部长
    {"person_id": 8, "org_id": 1, "title": "县委常委、统战部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "兼县政协党组副书记"},

    # 张勇 (id=9) — 县委常委、宣传部部长
    {"person_id": 9, "org_id": 1, "title": "县委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},

    # 梁颖 (id=10) — 副县长
    {"person_id": 10, "org_id": 2, "title": "县政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "负责人力资源和社会保障、退役军人事务等"},

    # 向煊锋 (id=11) — 副县长
    {"person_id": 11, "org_id": 2, "title": "县政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "负责工业经济、科技、商务等"},

    # 陈晓红 (id=12) — 副县长
    {"person_id": 12, "org_id": 2, "title": "县政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "负责民政、司法工作"},

    # 文伟 (id=13) — 副县长、公安局局长
    {"person_id": 13, "org_id": 2, "title": "县政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 11, "title": "县公安局党委书记、局长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},

    # 王超 (id=14) — 副县长
    {"person_id": 14, "org_id": 2, "title": "县政府副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "负责住建、交通、农业农村等"},

    # 卢明春 (id=15) — 人大主任
    {"person_id": 15, "org_id": 3, "title": "县人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": "党组书记"},

    # 彭志军 (id=16) — 人大副主任
    {"person_id": 16, "org_id": 3, "title": "县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": "党组副书记"},

    # 郑学敏 (id=17) — 人大副主任
    {"person_id": 17, "org_id": 3, "title": "县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},

    # 王军 (id=18) — 人大副主任
    {"person_id": 18, "org_id": 3, "title": "县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": "党组成员"},

    # 刘建林 (id=19) — 人大副主任
    {"person_id": 19, "org_id": 3, "title": "县人大常委会副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": "党组成员"},

    # 陈开军 (id=20) — 政协主席
    {"person_id": 20, "org_id": 4, "title": "县政协主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": "党组书记"},

    # 涂成钢 (id=21) — 政协副主席
    {"person_id": 21, "org_id": 4, "title": "县政协副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},

    # 李仕贵 (id=22) — 政协副主席
    {"person_id": 22, "org_id": 4, "title": "县政协副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": "党组副书记"},

    # 刘勇义 (id=23) — 政协副主席
    {"person_id": 23, "org_id": 4, "title": "县政协副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": "兼县工商联主席"},

    # 尹永刚 (id=24) — 政协副主席
    {"person_id": 24, "org_id": 4, "title": "县政协副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},

    # 余卫红 (id=25) — 政协秘书长
    {"person_id": 25, "org_id": 4, "title": "县政协秘书长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "党组成员"},

    # 李忠云 (id=26) — 曾任青神县委常委、常务副县长 (cross-county exchange)
    {"person_id": 26, "org_id": 1, "title": "青神县委常委", "start_date": "2016-10", "end_date": "2018-09", "rank": "副处级", "note": "在青神县任职期间"},
    {"person_id": 26, "org_id": 2, "title": "青神县常务副县长", "start_date": "2016-10", "end_date": "2018-09", "rank": "副处级", "note": ""},

    # 周代军 (id=27) — 在青神县开始职业生涯（洪雅县委书记）
    {"person_id": 27, "org_id": 1, "title": "青神县基层干部", "start_date": "1998-07", "end_date": "2001-11", "rank": "", "note": "1998-2001在青神县黑龙镇政府、共青团青神县委、青神县委组织部工作"},
]

# ── Relationships ──

relationships = [
    # 1. 党政一把手（邱磊实际兼任党政两职）
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate",
     "context": "邱磊（县委书记兼县长）与黄勇（县委副书记）—— 党政一把手与专职副书记",
     "overlap_org": "中共青神县委", "overlap_period": ""},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "邱磊（书记/县长）与程玉（常务副县长）",
     "overlap_org": "青神县委常委会", "overlap_period": ""},

    # 2. 县委常委间的工作关系
    {"person_a": 1, "person_b": 4, "type": "superior_subordinate",
     "context": "邱磊（书记）与廖长明（政法委书记）",
     "overlap_org": "青神县委常委会", "overlap_period": ""},
    {"person_a": 1, "person_b": 5, "type": "superior_subordinate",
     "context": "邱磊（书记）与李泽（组织部长）",
     "overlap_org": "青神县委常委会", "overlap_period": ""},
    {"person_a": 1, "person_b": 6, "type": "superior_subordinate",
     "context": "邱磊（书记）与杨玉刚（纪委书记）",
     "overlap_org": "青神县委常委会", "overlap_period": ""},
    {"person_a": 1, "person_b": 7, "type": "superior_subordinate",
     "context": "邱磊（书记）与王果（总工会主席）",
     "overlap_org": "青神县委常委会", "overlap_period": ""},
    {"person_a": 1, "person_b": 8, "type": "superior_subordinate",
     "context": "邱磊（书记）与杨燕强（统战部长）",
     "overlap_org": "青神县委常委会", "overlap_period": ""},
    {"person_a": 1, "person_b": 9, "type": "superior_subordinate",
     "context": "邱磊（书记）与张勇（宣传部长）",
     "overlap_org": "青神县委常委会", "overlap_period": ""},

    # 3. 县长 vs 副县长（邱磊兼县长）
    {"person_a": 1, "person_b": 10, "type": "superior_subordinate",
     "context": "邱磊（县长）与梁颖（副县长）",
     "overlap_org": "青神县人民政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 11, "type": "superior_subordinate",
     "context": "邱磊（县长）与向煊锋（副县长）",
     "overlap_org": "青神县人民政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 12, "type": "superior_subordinate",
     "context": "邱磊（县长）与陈晓红（副县长）",
     "overlap_org": "青神县人民政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 13, "type": "superior_subordinate",
     "context": "邱磊（县长）与文伟（副县长、公安局长）",
     "overlap_org": "青神县人民政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 14, "type": "superior_subordinate",
     "context": "邱磊（县长）与王超（副县长）",
     "overlap_org": "青神县人民政府", "overlap_period": ""},

    # 4. 人大与政协领导关系
    {"person_a": 1, "person_b": 15, "type": "other",
     "context": "邱磊（书记）与卢明春（人大主任）——党政领导与人大系统",
     "overlap_org": "青神县", "overlap_period": ""},
    {"person_a": 1, "person_b": 20, "type": "other",
     "context": "邱磊（书记）与陈开军（政协主席）——党政领导与政协系统",
     "overlap_org": "青神县", "overlap_period": ""},

    # 5. Cross-county exchanges (via 李忠云 — 曾任青神常务副县长)
    {"person_a": 26, "person_b": 1, "type": "overlap",
     "context": "李忠云曾任青神县委常委、常务副县长（2016-2018），与邱磊在当前时间点上未必直接共事，但属于同县领导序列",
     "overlap_org": "青神县委/县政府", "overlap_period": ""},

    # 6. 周代军 — 从青神起步的跨县领导
    {"person_a": 27, "person_b": 1, "type": "other",
     "context": "周代军（现任眉山市副市长、洪雅县委书记）1998-2001年在青神县黑龙镇、团县委、县委组织部工作，属于'青神出身'的跨县领导",
     "overlap_org": "青神县", "overlap_period": "1998-2001"},
]

# ── Main ──

if __name__ == "__main__":
    # Determine output paths
    STAGING_DIR = Path(__file__).parent.resolve()
    db_path = STAGING_DIR / "青神县_network.db"
    gexf_path = STAGING_DIR / "青神县_network.gexf"
    DB_PATH = db_path  # uppercase alias for process_tmp.py compatibility
    GEXF_PATH = gexf_path  # uppercase alias for process_tmp.py compatibility

    print(f"Building 青神县 network data...")
    print(f"  Persons: {len(persons)}")
    print(f"  Orgs: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")

    run_build(
        slug="青神县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=db_path,
        gexf_path=gexf_path,
        overwrite=True,
    )

    print(f"\nOutputs:")
    print(f"  DB:   {db_path}")
    print(f"  GEXF: {gexf_path}")

    # Quick verification
    import sqlite3
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM persons")
    pc = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM organizations")
    oc = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM positions")
    poc = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM relationships")
    rc = cur.fetchone()[0]
    conn.close()
    print(f"\nVerification: {pc} persons, {oc} orgs, {poc} positions, {rc} relationships")