#!/usr/bin/env python3
"""
庆阳市领导班子工作关系网络 — 数据构建脚本
Generate SQLite database + GEXF graph for Qingyang City leadership network.

Level: 地级市
Province: 甘肃省
Region: 庆阳市
Targets: 市委书记 & 市长

Research Sources:
- Wikipedia (zh.wikipedia.org) — 庆阳市, 周继军, 胡志勇, 黄泽元, 贠建民, 卢小亨 etc.
- 百度百科 — where available
- 新闻报道 (中国经济网, 中国甘肃网, 澎湃新闻 etc.)
- 任前公示 (甘肃组工网)

Research Date: 2026-07-22
"""

import json
import os
import sqlite3
from datetime import datetime

# ── Paths ──
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "庆阳市_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "庆阳市_network.gexf")

# ── DATA ──

# 1. Persons
persons = [
    # ════════════════════════════════════════
    # Current Top Leaders
    # ════════════════════════════════════════
    {
        "id": "p01",
        "name": "周继军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年12月",
        "birthplace": "甘肃兰州",
        "native_place": "甘肃兰州",
        "education": "大学/管理学硕士(兰州商学院会计学本科,厦门大学会计学硕士)",
        "party_join": "中共党员",
        "work_start": "1992年7月",
        "current_post": "庆阳市委书记",
        "current_org": "中共庆阳市委员会",
        "source": "Wikipedia: 周继军, 庆阳市; 中国甘肃网; 人民网",
        "person_id": "qingyang_zhou_jijun"
    },
    {
        "id": "p02",
        "name": "胡志勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年2月",
        "birthplace": "甘肃金塔",
        "native_place": "甘肃金塔",
        "education": "在职研究生(甘肃政法学院公安学大专,兰州大学法律专业)",
        "party_join": "中共党员",
        "work_start": "1995年7月",
        "current_post": "庆阳市委副书记、市政府党组书记、市长",
        "current_org": "庆阳市人民政府",
        "source": "Wikipedia: 胡志勇; 中国甘肃网; 中国经济网; 搜狐新闻",
        "person_id": "qingyang_hu_zhiyong"
    },
    # ════════════════════════════════════════
    # 市人大、政协领导
    # ════════════════════════════════════════
    {
        "id": "p03",
        "name": "王之臣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年11月",
        "birthplace": "甘肃武威",
        "native_place": "甘肃武威",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "庆阳市人大常委会主任",
        "current_org": "庆阳市人民代表大会常务委员会",
        "source": "Wikipedia: 庆阳市; 庆阳市政府网",
        "person_id": "qingyang_wang_zhichen"
    },
    {
        "id": "p04",
        "name": "李隆基",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966年11月",
        "birthplace": "甘肃民乐",
        "native_place": "甘肃民乐",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "庆阳市政协主席",
        "current_org": "中国人民政治协商会议庆阳市委员会",
        "source": "Wikipedia: 庆阳市; 庆阳市政府网",
        "person_id": "qingyang_li_longji"
    },
    # ════════════════════════════════════════
    # Predecessors — 市委书记
    # ════════════════════════════════════════
    {
        "id": "p05",
        "name": "黄泽元",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966年5月",
        "birthplace": "甘肃民勤",
        "native_place": "甘肃民勤",
        "education": "本科/公共管理硕士(西北师范大学历史系,兰州大学管理学院)",
        "party_join": "中共党员",
        "work_start": "1985年6月",
        "current_post": "甘肃省政协党组成员、秘书长",
        "current_org": "中国人民政治协商会议甘肃省委员会",
        "source": "Wikipedia: 黄泽元; 中国经济网; 中国甘肃网",
        "person_id": "qingyang_huang_zeyuan"
    },
    {
        "id": "p06",
        "name": "贠建民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1963年4月",
        "birthplace": "甘肃会宁",
        "native_place": "甘肃会宁",
        "education": "大学(甘肃农业大学,兰州大学)",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "甘肃省政协副主席",
        "current_org": "中国人民政治协商会议甘肃省委员会",
        "source": "Wikipedia: 贠建民; 中国经济网; 人民网",
        "person_id": "qingyang_yun_jianmin"
    },
    {
        "id": "p07",
        "name": "栾克军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1960年6月",
        "birthplace": "甘肃平凉",
        "native_place": "甘肃平凉",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "（服刑中—因受贿罪被判11年）",
        "current_org": "待查",
        "source": "Wikipedia; 新闻报道",
        "person_id": "qingyang_luan_kejun"
    },
    {
        "id": "p08",
        "name": "夏红民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1961年10月",
        "birthplace": "湖北监利",
        "native_place": "湖北监利",
        "education": "大学/农学学士(华中农学院)",
        "party_join": "中共党员",
        "work_start": "1982年8月",
        "current_post": "山东省委常委、省纪委书记",
        "current_org": "中共山东省纪律检查委员会",
        "source": "Wikipedia",
        "person_id": "qingyang_xia_hongmin"
    },
    # ════════════════════════════════════════
    # Predecessors — 市长
    # ════════════════════════════════════════
    {
        "id": "p09",
        "name": "卢小亨",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年",
        "birthplace": "甘肃通渭",
        "native_place": "甘肃通渭",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "甘肃省交通运输厅党组书记",
        "current_org": "甘肃省交通运输厅",
        "source": "Wikipedia: 卢小亨; 中国经济网",
        "person_id": "qingyang_lu_xiaoheng"
    },
    # ════════════════════════════════════════
    # Other noted connections
    # ════════════════════════════════════════
    {
        "id": "p10",
        "name": "白振海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年12月",
        "birthplace": "甘肃庆阳",
        "native_place": "甘肃庆阳",
        "education": "庆阳师范学校、中央党校研究生",
        "party_join": "中共党员",
        "work_start": "1989年7月",
        "current_post": "兰州市委常委、兰州新区党工委书记",
        "current_org": "中共兰州市委员会",
        "source": "build_平凉市_data.py; 百度百科",
        "person_id": "pingliang_bai_zhenhai"
    },
    {
        "id": "p11",
        "name": "李菊霞",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1975年3月",
        "birthplace": "甘肃西和",
        "native_place": "甘肃西和",
        "education": "省委党校研究生/经济学学士",
        "party_join": "中共党员",
        "work_start": "1996年8月",
        "current_post": "庆阳市委常委（原清水县委书记）",
        "current_org": "中共庆阳市委员会",
        "source": "data/persons/20260717-甘肃省-天水市-县委书记-李菊霞.json; 甘肃组工网",
        "person_id": "qingshui_li_juxia"
    },
    {
        "id": "p12",
        "name": "贾志升",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年7月",
        "birthplace": "甘肃镇原",
        "native_place": "甘肃镇原",
        "education": "在职大学(庆阳师范高等专科学校化学,兰州大学汉语言文学)",
        "party_join": "中共党员",
        "work_start": "1996年11月",
        "current_post": "酒泉市委副书记、市长",
        "current_org": "酒泉市人民政府",
        "source": "data/persons/20260722-甘肃省-酒泉市-市长-贾志升.json; 百度百科",
        "person_id": "jiuquan_jia_zhisheng"
    },
]

# 2. Organizations
organizations = [
    {"id": "o01", "name": "中共庆阳市委员会", "type": "党委", "level": "地厅级", "parent": "中共甘肃省委员会", "location": "甘肃省庆阳市西峰区"},
    {"id": "o02", "name": "庆阳市人民政府", "type": "政府", "level": "地厅级", "parent": "甘肃省人民政府", "location": "甘肃省庆阳市西峰区"},
    {"id": "o03", "name": "庆阳市人民代表大会常务委员会", "type": "人大", "level": "地厅级", "parent": "庆阳市", "location": "甘肃省庆阳市西峰区"},
    {"id": "o04", "name": "中国人民政治协商会议庆阳市委员会", "type": "政协", "level": "地厅级", "parent": "庆阳市", "location": "甘肃省庆阳市西峰区"},
    {"id": "o05", "name": "甘肃省政协", "type": "政协", "level": "省级", "parent": "中国人民政治协商会议", "location": "甘肃省兰州市"},
    {"id": "o06", "name": "甘肃省交通运输厅", "type": "政府", "level": "省级", "parent": "甘肃省人民政府", "location": "甘肃省兰州市"},
    {"id": "o07", "name": "中共山东省纪律检查委员会", "type": "党委", "level": "省级", "parent": "中共山东省委员会", "location": "山东省济南市"},
    {"id": "o08", "name": "中共兰州市委员会", "type": "党委", "level": "副省级", "parent": "中共甘肃省委员会", "location": "甘肃省兰州市"},
    {"id": "o09", "name": "兰州新区", "type": "政府", "level": "国家级新区", "parent": "兰州市", "location": "甘肃省兰州市"},
    {"id": "o10", "name": "酒泉市人民政府", "type": "政府", "level": "地厅级", "parent": "甘肃省人民政府", "location": "甘肃省酒泉市"},
    {"id": "o11", "name": "庆阳市人民政府（贾志升前职）", "type": "政府", "level": "地厅级", "parent": "甘肃省人民政府", "location": "甘肃省庆阳市"},
]

# 3. Positions
positions = [
    # 周继军 (p01)
    {"person_id": "p01", "org_id": "o01", "title": "庆阳市委书记", "start": "2026-01", "end": "至今", "rank": "正厅级", "note": "2026年1月接替黄泽元任书记"},
    {"person_id": "p01", "org_id": "o02", "title": "庆阳市人民政府市长（前任）", "start": "2021-12", "end": "2026-05", "rank": "正厅级", "note": "2021-2026任市长"},
    {"person_id": "p01", "org_id": "o01", "title": "庆阳市委副书记", "start": "2021-12", "end": "2026-01", "rank": "副厅级", "note": "兼任市长"},
    {"person_id": "p01", "org_id": "o01", "title": "甘肃省财政厅副厅长", "start": "2018-07", "end": "2021-12", "rank": "副厅级", "note": "省财政厅副厅长"},
    {"person_id": "p01", "org_id": "o01", "title": "甘肃省审计厅副厅长", "start": "2015-05", "end": "2018-07", "rank": "副厅级", "note": "其间挂职国家审计署金融审计司副司长"},
    {"person_id": "p01", "org_id": "o02", "title": "庆阳市副市长", "start": "2012-12", "end": "2015-05", "rank": "副厅级", "note": ""},
    {"person_id": "p01", "org_id": "o01", "title": "天水市秦州区委副书记、区长", "start": "2010-08", "end": "2012-12", "rank": "正处级", "note": ""},
    {"person_id": "p01", "org_id": "o01", "title": "甘肃省审计厅处长", "start": "2007", "end": "2010-08", "rank": "正处级", "note": "历任农业与资源环保审计处处长、财政审计处处长、人事处处长"},
    {"person_id": "p01", "org_id": "o01", "title": "甘肃省审计厅工作", "start": "1992-07", "end": "2007", "rank": "", "note": "1992年兰州商学院毕业进入省审计厅"},
    # 胡志勇 (p02)
    {"person_id": "p02", "org_id": "o02", "title": "庆阳市人民政府市长", "start": "2026-06", "end": "至今", "rank": "正厅级", "note": "2026年6月正式当选"},
    {"person_id": "p02", "org_id": "o02", "title": "庆阳市人民政府代市长", "start": "2026-04", "end": "2026-06", "rank": "正厅级", "note": "2026年4月任代市长"},
    {"person_id": "p02", "org_id": "o01", "title": "庆阳市委副书记、市政府党组书记", "start": "2026-04", "end": "至今", "rank": "副厅级", "note": ""},
    {"person_id": "p02", "org_id": "o01", "title": "天水市委常委、组织部部长", "start": "2024-05", "end": "2026-04", "rank": "副厅级", "note": ""},
    {"person_id": "p02", "org_id": "o02", "title": "天水市人民政府副市长", "start": "2021-10", "end": "2024-05", "rank": "副厅级", "note": ""},
    {"person_id": "p02", "org_id": "o01", "title": "玉门市委书记", "start": "2019-06", "end": "2021-10", "rank": "正处级", "note": "县级市"},
    {"person_id": "p02", "org_id": "o02", "title": "酒泉市工业和信息化局局长", "start": "2019-01", "end": "2019-06", "rank": "正处级", "note": ""},
    {"person_id": "p02", "org_id": "o01", "title": "酒泉市工作（早期）", "start": "1995-07", "end": "2019-01", "rank": "", "note": "1995年参加工作后在酒泉市逐步晋升"},
    # 王之臣 (p03)
    {"person_id": "p03", "org_id": "o03", "title": "庆阳市人大常委会主任", "start": "2026-02", "end": "至今", "rank": "正厅级", "note": ""},
    # 李隆基 (p04)
    {"person_id": "p04", "org_id": "o04", "title": "庆阳市政协主席", "start": "2021-12", "end": "至今", "rank": "正厅级", "note": ""},
    # 黄泽元 (p05)
    {"person_id": "p05", "org_id": "o05", "title": "甘肃省政协秘书长", "start": "2026-01", "end": "至今", "rank": "正厅级", "note": "2026年1月调任"},
    {"person_id": "p05", "org_id": "o01", "title": "庆阳市委书记", "start": "2021-07", "end": "2026-01", "rank": "正厅级", "note": "2021年7月空降"},
    {"person_id": "p05", "org_id": "o01", "title": "甘肃省应急管理厅党委书记、厅长", "start": "2019-03", "end": "2021-07", "rank": "正厅级", "note": ""},
    {"person_id": "p05", "org_id": "o02", "title": "张掖市人民政府市长", "start": "2012-12", "end": "2019-03", "rank": "正厅级", "note": "2012年8月代理,12月转正"},
    {"person_id": "p05", "org_id": "o01", "title": "中共陇南市委副书记", "start": "2005-04", "end": "2012-08", "rank": "副厅级", "note": ""},
    {"person_id": "p05", "org_id": "o01", "title": "共青团甘肃省委副书记", "start": "2001-02", "end": "2005-04", "rank": "副厅级", "note": ""},
    # 贠建民 (p06)
    {"person_id": "p06", "org_id": "o05", "title": "甘肃省政协副主席", "start": "2018-01", "end": "至今", "rank": "副省级", "note": "2018年首次当选,2023年连任"},
    {"person_id": "p06", "org_id": "o01", "title": "庆阳市委书记", "start": "2016-10", "end": "2021-07", "rank": "正厅级", "note": ""},
    {"person_id": "p06", "org_id": "o02", "title": "庆阳市人民政府市长", "start": "2014-10", "end": "2016-11", "rank": "正厅级", "note": ""},
    # 栾克军 (p07)
    {"person_id": "p07", "org_id": "o02", "title": "兰州市人民政府市长", "start": "2016-10", "end": "2017-11", "rank": "正厅级", "note": "2017年11月被调查"},
    {"person_id": "p07", "org_id": "o01", "title": "庆阳市委书记", "start": "2014-11", "end": "2016-10", "rank": "正厅级", "note": ""},
    {"person_id": "p07", "org_id": "o02", "title": "庆阳市人民政府市长", "start": "2012-08", "end": "2014-11", "rank": "正厅级", "note": ""},
    {"person_id": "p07", "org_id": "o02", "title": "张掖市人民政府市长", "start": "2010", "end": "2012-08", "rank": "正厅级", "note": "前职"},
    # 夏红民 (p08)
    {"person_id": "p08", "org_id": "o07", "title": "山东省委常委、省纪委书记", "start": "2018", "end": "至今", "rank": "副省级", "note": ""},
    {"person_id": "p08", "org_id": "o01", "title": "庆阳市委书记", "start": "2012-08", "end": "2014-10", "rank": "正厅级", "note": ""},
    {"person_id": "p08", "org_id": "o02", "title": "甘肃省副省长/省长助理", "start": "2009", "end": "2012-08", "rank": "副省级", "note": "前职"},
    # 卢小亨 (p09)
    {"person_id": "p09", "org_id": "o06", "title": "甘肃省交通运输厅党组书记", "start": "2025?", "end": "至今", "rank": "正厅级", "note": ""},
    {"person_id": "p09", "org_id": "o01", "title": "张掖市委书记", "start": "2021-07", "end": "2025?", "rank": "正厅级", "note": ""},
    {"person_id": "p09", "org_id": "o02", "title": "庆阳市人民政府市长", "start": "2020-01", "end": "2021-07", "rank": "正厅级", "note": ""},
    # 白振海 (p10)
    {"person_id": "p10", "org_id": "o08", "title": "兰州市委常委、兰州新区党工委书记", "start": "2025?", "end": "至今", "rank": "副厅级", "note": "原平凉市市长"},
    {"person_id": "p10", "org_id": "o02", "title": "平凉市人民政府市长（前任）", "start": "2021", "end": "2025", "rank": "正厅级", "note": ""},
    {"person_id": "p10", "org_id": "o02", "title": "庆阳市副市长", "start": "2011-11", "end": "2016-09", "rank": "副厅级", "note": ""},
    # 李菊霞 (p11)
    {"person_id": "p11", "org_id": "o01", "title": "庆阳市委常委", "start": "2026-06", "end": "至今", "rank": "副厅级", "note": "2026年6月调任"},
    {"person_id": "p11", "org_id": "o01", "title": "清水县委书记（前任）", "start": "2024-01", "end": "2026-06", "rank": "正处级", "note": "天水市清水县"},
    {"person_id": "p11", "org_id": "o02", "title": "清水县人民政府县长", "start": "2021-06", "end": "2024-01", "rank": "正处级", "note": ""},
    # 贾志升 (p12)
    {"person_id": "p12", "org_id": "o10", "title": "酒泉市委副书记、市长", "start": "2025-09", "end": "至今", "rank": "正厅级", "note": ""},
    {"person_id": "p12", "org_id": "o11", "title": "正宁县委书记", "start": "2020-04", "end": "2021-08", "rank": "正处级", "note": "庆阳市下辖县"},
    {"person_id": "p12", "org_id": "o11", "title": "庆阳市农业农村局局长", "start": "2019-02", "end": "2020-04", "rank": "正处级", "note": ""},
]

# 4. Relationships
relationships = [
    # 现任班子核心关系
    {"person_a": "p01", "person_b": "p02", "type": "overlap", "context": "周继军(书记)与胡志勇(市长): 党政一把手配合", "overlap_org": "中共庆阳市委员会/庆阳市人民政府", "overlap_period": "2026-04至今", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p01", "person_b": "p03", "type": "overlap", "context": "周继军(书记)与王之臣(人大主任): 市领导班子配合", "overlap_org": "庆阳市", "overlap_period": "2026-01至今", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p02", "person_b": "p04", "type": "overlap", "context": "胡志勇(市长)与李隆基(政协主席): 政-政协配合", "overlap_org": "庆阳市", "overlap_period": "2026-04至今", "strength": "strong", "confidence": "confirmed"},

    # 前后任关系
    {"person_a": "p01", "person_b": "p05", "type": "predecessor_successor", "context": "周继军接替黄泽元任庆阳市委书记", "overlap_org": "中共庆阳市委员会", "overlap_period": "2026-01", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p01", "person_b": "p06", "type": "predecessor_successor", "context": "周继军接替贠建民前市长; 贠为书记时周为下级", "overlap_org": "庆阳市", "overlap_period": "2016-2021", "strength": "medium", "confidence": "plausible"},
    {"person_a": "p05", "person_b": "p06", "type": "predecessor_successor", "context": "黄泽元接替贠建民任庆阳市委书记", "overlap_org": "中共庆阳市委员会", "overlap_period": "2021-07", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p06", "person_b": "p07", "type": "predecessor_successor", "context": "贠建民接替栾克军先后任市长和书记", "overlap_org": "庆阳市人民政府/中共庆阳市委员会", "overlap_period": "2014-2016", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p07", "person_b": "p08", "type": "predecessor_successor", "context": "栾克军接替夏红民任庆阳市委书记", "overlap_org": "中共庆阳市委员会", "overlap_period": "2014-11", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p02", "person_b": "p01", "type": "predecessor_successor", "context": "胡志勇接替周继军任庆阳市市长", "overlap_org": "庆阳市人民政府", "overlap_period": "2026-04/05", "strength": "strong", "confidence": "confirmed"},
    {"person_a": "p09", "person_b": "p01", "type": "predecessor_successor", "context": "卢小亨前手→周继军接任庆阳市市长", "overlap_org": "庆阳市人民政府", "overlap_period": "2021-07", "strength": "strong", "confidence": "confirmed"},

    # 跨市交流关系
    {"person_a": "p05", "person_b": "p07", "type": "same_system", "context": "黄泽元(张掖市长)→栾克军(张掖市长前)→庆阳书记链", "overlap_org": "张掖市人民政府/庆阳市", "overlap_period": "2010-2019", "strength": "medium", "confidence": "plausible"},
    {"person_a": "p09", "person_b": "p05", "type": "same_system", "context": "卢小亨(庆阳市长→张掖书记)与黄泽元(张掖市长→庆阳书记): 双向交流", "overlap_org": "张掖市/庆阳市", "overlap_period": "2012-2025", "strength": "medium", "confidence": "plausible"},

    # 庆阳本土干部外部网络
    {"person_a": "p10", "person_b": "p01", "type": "same_system", "context": "白振海(庆阳人,庆阳副市长2011-2016)与周继军(庆阳副市长2012-2015): 同期在庆阳任职", "overlap_org": "庆阳市人民政府", "overlap_period": "2012-2015", "strength": "medium", "confidence": "plausible"},

    # 新进常委
    {"person_a": "p11", "person_b": "p01", "type": "overlap", "context": "李菊霞(新调任庆阳市委常委)与周继军(书记): 上下级", "overlap_org": "中共庆阳市委员会", "overlap_period": "2026-06至今", "strength": "strong", "confidence": "confirmed"},

    # 贾志升庆阳连接
    {"person_a": "p12", "person_b": "p10", "type": "same_system", "context": "贾志升(庆阳市农业农村局/正宁县委书记)与白振海(庆阳副市长): 同源庆阳政坛", "overlap_org": "庆阳市", "overlap_period": "2019-2021", "strength": "medium", "confidence": "plausible"},

    # 跨市长链
    {"person_a": "p02", "person_b": "p08", "type": "same_system", "context": "胡志勇(天水工作过)与夏红民(曾任甘肃省长助理): 同在天水-庆阳系统", "overlap_org": "甘肃省干部交流体系", "overlap_period": "", "strength": "weak", "confidence": "plausible"},
]

# ── Helper Functions ──

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    """Return RGB color string based on role."""
    title = p["current_post"]
    if "书记" in title and "纪委" not in title and "统战" not in title and "人大" not in title and "政协" not in title:
        return "255,50,50"    # Red — Party Secretary
    if "市长" in title and ("副书记" in title or "党组书记" in title):
        return "50,100,255"   # Blue — Mayor
    if "市长" in title or ("副市长" in title and "常委" not in title):
        return "50,100,255"   # Blue — Government head
    if "纪委" in title or "监委" in title or "监察" in title or "纪委书记" in title:
        return "255,165,0"    # Orange — Discipline
    if "副书记" in title:
        return "200,50,50"    # Dark red — Deputy Secretary
    if "常委" in title:
        return "200,100,100"  # Pink — Other Standing Committee
    if "副市长" in title:
        return "100,100,200"  # Light blue — Deputy Mayor
    if "人大" in title:
        return "200,255,255"  # Cyan — People's Congress
    if "政协" in title:
        return "255,240,200"  # Cream — CPPCC
    return "100,100,100"      # Grey — Other

def person_size(p):
    """Return node size based on role."""
    title = p["current_post"]
    if "市委书记" in title or "人大主任" in title or "政协主席" in title:
        return "20.0"
    if "市长" in title and ("副书记" in title or "党组书记" in title):
        return "20.0"
    if "副书记" in title or "常委" in title:
        return "14.0"
    if "副市长" in title:
        return "12.0"
    if "人大" in title or "政协" in title:
        return "12.0"
    return "10.0"

def org_color(o):
    """Return RGB color string based on org type."""
    t = o["type"]
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "事业单位": "220,220,220",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }
    return colors.get(t, "200,200,200")

# ── Build Database ──

def build_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS persons (
        id TEXT PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
        birth TEXT, birthplace TEXT, native_place TEXT, education TEXT,
        party_join TEXT, work_start TEXT, current_post TEXT,
        current_org TEXT, source TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS organizations (
        id TEXT PRIMARY KEY, name TEXT, type TEXT, level TEXT,
        parent TEXT, location TEXT
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS positions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id TEXT, org_id TEXT, title TEXT,
        start TEXT, end TEXT, rank TEXT, note TEXT,
        FOREIGN KEY(person_id) REFERENCES persons(id),
        FOREIGN KEY(org_id) REFERENCES organizations(id)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS relationships (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_a TEXT, person_b TEXT, type TEXT, context TEXT,
        overlap_org TEXT, overlap_period TEXT,
        FOREIGN KEY(person_a) REFERENCES persons(id),
        FOREIGN KEY(person_b) REFERENCES persons(id)
    )""")

    c.execute("DELETE FROM persons")
    c.execute("DELETE FROM organizations")
    c.execute("DELETE FROM positions")
    c.execute("DELETE FROM relationships")

    for p in persons:
        c.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""", (
            p["id"], p["name"], p["gender"], p["ethnicity"],
            p["birth"], p["birthplace"], p["native_place"], p["education"],
            p["party_join"], p["work_start"], p["current_post"],
            p["current_org"], p["source"]
        ))

    for o in organizations:
        c.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""", (
            o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]
        ))

    for pos in positions:
        c.execute("""INSERT INTO positions (person_id, org_id, title, start, end, rank, note)
                     VALUES (?,?,?,?,?,?,?)""", (
            pos["person_id"], pos["org_id"], pos["title"],
            pos["start"], pos["end"], pos["rank"], pos["note"]
        ))

    for r in relationships:
        c.execute("""INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period)
                     VALUES (?,?,?,?,?,?)""", (
            r["person_a"], r["person_b"], r["type"], r["context"],
            r["overlap_org"], r["overlap_period"]
        ))

    conn.commit()
    conn.close()

# ── Build GEXF ──

def build_gexf():
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append('    <description>庆阳市领导班子工作关系网络 - 数据来源: Wikipedia及公开报道</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="role" type="string"/>')
    lines.append('      <attribute id="2" title="province" type="string"/>')
    lines.append('      <attribute id="3" title="city" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    # Nodes
    lines.append('    <nodes>')

    # Person nodes
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append('          <attvalue for="2" value="甘肃省"/>')
        lines.append('          <attvalue for="3" value="庆阳市"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    # Organization nodes
    for o in organizations:
        c = org_color(o)
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append('          <attvalue for="2" value="甘肃省"/>')
        lines.append('          <attvalue for="3" value="庆阳市"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person→Organization (worked_at)
    for pos in positions:
        eid += 1
        weight = "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["title"])}"/>')
        lines.append('          <attvalue for="2" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person↔Person (relationship)
    for r in relationships:
        eid += 1
        weight = "2.0"
        conf = r.get("confidence", "plausible")
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["context"])}" weight="{weight}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="{esc(r["type"])}"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{conf}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

# ── Main ──

def main():
    print(f"=== 庆阳市网络数据构建 ===")
    print(f"人员: {len(persons)} 人")
    print(f"组织机构: {len(organizations)} 个")
    print(f"任职记录: {len(positions)} 条")
    print(f"关系: {len(relationships)} 条")

    print(f"\n构建数据库...")
    build_db()
    db_size = os.path.getsize(DB_PATH)
    print(f"  ✓ {DB_PATH} ({db_size} bytes)")

    print(f"构建GEXF图文件...")
    build_gexf()
    gexf_size = os.path.getsize(GEXF_PATH)
    print(f"  ✓ {GEXF_PATH} ({gexf_size} bytes)")

    print(f"\n=== 完成 ===")

if __name__ == "__main__":
    main()
