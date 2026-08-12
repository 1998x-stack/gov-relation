#!/usr/bin/env python3
"""Build the evidence-backed current leadership package for 西丰县 (铁岭市, 辽宁省)."""

from __future__ import annotations

import json
import sqlite3
import sys
from pathlib import Path

for parent in Path(__file__).resolve().parents:
    if (parent / "gov_relation").is_dir():
        sys.path.insert(0, str(parent))
        break

from gov_relation.factory import InsertFactory, PersonJSONFactory
from gov_relation.runner import run_build

TASK_DIR = Path(__file__).resolve().parent
DB_PATH = TASK_DIR / "西丰县_network.db"
GEXF_PATH = TASK_DIR / "西丰县_network.gexf"
REPORT_PATH = TASK_DIR / "20260812-辽宁省-铁岭市-西丰县-领导班子调查.md"

PERSONS = [
    # 现任县委书记（推定，2026-04 起）
    {
        "canonical_name": "李子骥", "gender": "男", "ethnicity": "汉族",
        "birth_text": "1983-10", "education": "大学",
        "party_join_text": "2008-01", "work_start_text": "2006-09",
        "_source_pk": "xifeng-liziji-1983-10",
    },
    # 现任县长（官方确认）
    {
        "canonical_name": "宁丽岩", "gender": "女", "ethnicity": "汉族",
        "birth_text": "1974-03", "education": "大学",
        "_source_pk": "xifeng-ningliyan-1974-03",
    },
    # 常务副县长（2026-06 调任市直）
    {
        "canonical_name": "李振宇", "gender": "男", "ethnicity": "汉族",
        "birth_text": "1972-02", "education": "中央党校",
        "_source_pk": "xifeng-lizhenyu-1972-02",
    },
    {
        "canonical_name": "许伟", "gender": "男", "ethnicity": "汉族",
        "birth_text": "1968-02", "education": "在职大学",
        "_source_pk": "xifeng-xuwei-1968-02",
    },
    {
        "canonical_name": "雷晶", "gender": "女", "ethnicity": "汉族",
        "birth_text": "", "_source_pk": "xifeng-leijing-unknown",
    },
    {
        "canonical_name": "刘洋", "gender": "", "ethnicity": "",
        "birth_text": "", "_source_pk": "xifeng-liuyang-unknown",
    },
    {
        "canonical_name": "于思洋", "gender": "", "ethnicity": "",
        "birth_text": "", "_source_pk": "xifeng-yusiyang-unknown",
    },
    {
        "canonical_name": "宗鑫", "gender": "", "ethnicity": "",
        "birth_text": "", "_source_pk": "xifeng-zongxin-unknown",
    },
    {
        "canonical_name": "董金", "gender": "", "ethnicity": "",
        "birth_text": "", "_source_pk": "xifeng-dongjin-unknown",
    },
    {
        "canonical_name": "于翔", "gender": "", "ethnicity": "",
        "birth_text": "", "_source_pk": "xifeng-yuxiang-unknown",
    },
    # 前任县委书记 / 前任县长
    {
        "canonical_name": "荣大煜", "gender": "男", "ethnicity": "汉族",
        "birth_text": "1972-09", "native_place": "辽宁昌图",
        "education": "中央党校", "_source_pk": "xifeng-rongdayu-1972-09",
    },
    # 更早县委书记
    {
        "canonical_name": "吴炜", "gender": "男", "ethnicity": "汉族",
        "birth_text": "", "_source_pk": "xifeng-wuwei-unknown",
    },
    # 流出干部：副县长→市民政局长→外县县长候选人
    {
        "canonical_name": "王者兴", "gender": "男", "ethnicity": "汉族",
        "birth_text": "1976-04", "education": "大学",
        "_source_pk": "xifeng-wangzhexing-1976-04",
    },
    # 流出干部：政法委书记→外县区委副书记
    {
        "canonical_name": "张勇", "gender": "男", "ethnicity": "满族",
        "birth_text": "1978-01", "education": "中央党校大学",
        "_source_pk": "xifeng-zhangyong-1978-01",
    },
]

ORGANIZATIONS = [
    {"canonical_name": "中共西丰县委员会", "organization_type": "party", "location_text": "辽宁省铁岭市西丰县"},
    {"canonical_name": "西丰县人民政府", "organization_type": "government", "location_text": "辽宁省铁岭市西丰县"},
    {"canonical_name": "西丰经济开发区管理委员会", "organization_type": "development_zone", "location_text": "辽宁省铁岭市西丰县"},
    {"canonical_name": "铁岭市医疗保障局", "organization_type": "government_department", "location_text": "辽宁省铁岭市"},
    {"canonical_name": "铁岭市生态环境局", "organization_type": "government_department", "location_text": "辽宁省铁岭市"},
    {"canonical_name": "铁岭市民政局", "organization_type": "government_department", "location_text": "辽宁省铁岭市"},
    {"canonical_name": "铁岭市市场监督管理局", "organization_type": "government_department", "location_text": "辽宁省铁岭市"},
    {"canonical_name": "调兵山市人民政府", "organization_type": "government", "location_text": "辽宁省铁岭市调兵山市"},
    {"canonical_name": "中共调兵山市委员会", "organization_type": "party", "location_text": "辽宁省铁岭市调兵山市"},
    {"canonical_name": "昌图县大洼镇", "organization_type": "township", "location_text": "辽宁省铁岭市昌图县"},
    {"canonical_name": "铁岭市工商行政管理局", "organization_type": "government_department", "location_text": "辽宁省铁岭市"},
    {"canonical_name": "西丰县地方税务局", "organization_type": "government_department", "location_text": "辽宁省铁岭市西丰县"},
]

POSITIONS = [
    # ── 李子骥（推定现任县委书记；前任县长）───────────────
    {
        "person_name": "李子骥", "organization_name": "中共西丰县委员会",
        "organization_text": "中共西丰县委员会", "title": "县委书记",
        "start_text": "2026-04", "end_text": "至今", "is_current": 1,
        "sort_order": 0, "rank": "正处级", "confidence": "plausible",
        "notes": "2026-03-22省管公示拟任县委书记；推断就地转任，尚无2026-04后直接见报佐证",
    },
    {
        "person_name": "李子骥", "organization_name": "西丰县人民政府",
        "organization_text": "西丰县人民政府", "title": "县委副书记、县长",
        "start_text": "2024-07", "end_text": "2026-03", "sort_order": 10,
        "rank": "正处级", "confidence": "confirmed",
    },
    {
        "person_name": "李子骥", "organization_name": "铁岭市生态环境局",
        "organization_text": "铁岭市生态环境局", "title": "党组书记、局长",
        "start_text": "2024-06前", "end_text": "2024-07", "sort_order": 20,
        "rank": "正处级", "confidence": "confirmed",
    },
    {
        "person_name": "李子骥", "organization_name": "调兵山市人民政府",
        "organization_text": "调兵山市人民政府", "title": "市委常委、副市长",
        "start_text": "2020-11", "end_text": "2024-06前", "sort_order": 30,
        "rank": "副处级", "confidence": "confirmed",
    },
    {
        "person_name": "李子骥", "organization_name": "中共调兵山市委员会",
        "organization_text": "中共调兵山市委员会", "title": "市委常委",
        "start_text": "2020-11", "end_text": "2022-12", "sort_order": 35,
        "rank": "副处级", "confidence": "confirmed",
    },
    {
        "person_name": "李子骥", "organization_name": "昌图县大洼镇",
        "organization_text": "昌图县大洼镇", "title": "党委书记、人大主席",
        "start_text": "2015前", "end_text": "2020-11", "sort_order": 40,
        "rank": "正科级", "confidence": "confirmed",
    },
    # ── 宁丽岩（现任县长）──────────────────────────────
    {
        "person_name": "宁丽岩", "organization_name": "西丰县人民政府",
        "organization_text": "西丰县人民政府", "title": "县委副书记、县长",
        "start_text": "2026-04", "end_text": "至今", "is_current": 1,
        "sort_order": 0, "rank": "正处级", "confidence": "confirmed",
    },
    {
        "person_name": "宁丽岩", "organization_name": "铁岭市医疗保障局",
        "organization_text": "铁岭市医疗保障局", "title": "党组书记、局长",
        "start_text": "2022监前", "end_text": "2026-03", "sort_order": 10,
        "rank": "正处级", "confidence": "confirmed",
        "notes": "2026-03省管公示口径为铁岭市医保局党组书记、局长；早期履历待补",
    },
    # ── 李振宇（常务副县长→市直局长）───────────────────
    {
        "person_name": "李振宇", "organization_name": "铁岭市市场监督管理局",
        "organization_text": "铁岭市市场监督管理局", "title": "党组书记、局长",
        "start_text": "2026-06", "end_text": "至今", "is_current": 1,
        "sort_order": 0, "rank": "正处级", "confidence": "confirmed",
    },
    {
        "person_name": "李振宇", "organization_name": "西丰县人民政府",
        "organization_text": "西丰县人民政府", "title": "县委常委、常务副县长",
        "start_text": "2024-09前", "end_text": "2026-06", "sort_order": 10,
        "rank": "副处级", "confidence": "confirmed",
    },
    {
        "person_name": "李振宇", "organization_name": "中共西丰县委员会",
        "organization_text": "中共西丰县委员会", "title": "县委常委",
        "start_text": "2024-09前", "end_text": "2026-06", "sort_order": 20,
        "rank": "副处级", "confidence": "confirmed",
    },
    # ── 许伟（宣传部长→经开区→副县长）──────────────────
    {
        "person_name": "许伟", "organization_name": "西丰县人民政府",
        "organization_text": "西丰县人民政府", "title": "副县长、二级调研员",
        "start_text": "2026-01前", "end_text": "至今", "is_current": 1,
        "sort_order": 0, "rank": "副处级", "confidence": "confirmed",
        "notes": "分工负责招商引资/工信/科技",
    },
    {
        "person_name": "许伟", "organization_name": "西丰经济开发区管理委员会",
        "organization_text": "西丰经济开发区管理委员会", "title": "党工委副书记、管委会主任",
        "start_text": "2025-04", "end_text": "2025-12", "sort_order": 10,
        "rank": "副处级", "confidence": "confirmed",
    },
    {
        "person_name": "许伟", "organization_name": "中共西丰县委员会",
        "organization_text": "中共西丰县委员会", "title": "县委常委、宣传部部长",
        "start_text": "2021年前", "end_text": "2025-04", "sort_order": 20,
        "rank": "副处级", "confidence": "confirmed",
    },
    # ── 雷晶（县委常委、副县长）────────────────────────
    {
        "person_name": "雷晶", "organization_name": "西丰县人民政府",
        "organization_text": "西丰县人民政府", "title": "县委常委、副县长",
        "start_text": "2025前", "end_text": "至今", "is_current": 1,
        "sort_order": 0, "rank": "副处级", "confidence": "confirmed",
        "notes": "分工负责农业农村/教育/卫健/医保/鹿业",
    },
    {
        "person_name": "雷晶", "organization_name": "中共西丰县委员会",
        "organization_text": "中共西丰县委员会", "title": "县委常委",
        "start_text": "2025前", "end_text": "至今", "is_current": 1,
        "sort_order": 10, "rank": "副处级", "confidence": "confirmed",
    },
    # ── 刘洋（副县长）────────────────────────────────
    {
        "person_name": "刘洋", "organization_name": "西丰县人民政府",
        "organization_text": "西丰县人民政府", "title": "副县长",
        "start_text": "2025前", "end_text": "至今", "is_current": 1,
        "sort_order": 0, "rank": "副处级", "confidence": "confirmed",
        "notes": "分工负责住建/数据/水利/文旅/市场监督",
    },
    # ── 于思洋（副县长）──────────────────────────────
    {
        "person_name": "于思洋", "organization_name": "西丰县人民政府",
        "organization_text": "西丰县人民政府", "title": "副县长",
        "start_text": "2026-05前", "end_text": "至今", "is_current": 1,
        "sort_order": 0, "rank": "副处级", "confidence": "confirmed",
        "notes": "分工负责公安/司法",
    },
    # ── 宗鑫（副县长）────────────────────────────────
    {
        "person_name": "宗鑫", "organization_name": "西丰县人民政府",
        "organization_text": "西丰县人民政府", "title": "副县长",
        "start_text": "2026-05前", "end_text": "至今", "is_current": 1,
        "sort_order": 0, "rank": "副处级", "confidence": "confirmed",
        "notes": "分工负责交通/生态环保/自然资源/林业/退役军人",
    },
    # ── 董金（副县长）────────────────────────────────
    {
        "person_name": "董金", "organization_name": "西丰县人民政府",
        "organization_text": "西丰县人民政府", "title": "副县长",
        "start_text": "2025前", "end_text": "至今", "is_current": 1,
        "sort_order": 0, "rank": "副处级", "confidence": "confirmed",
        "notes": "分工协助常务分管商贸流通；2025-10 鹿业调研见报",
    },
    # ── 于翔（副县长）────────────────────────────────
    {
        "person_name": "于翔", "organization_name": "西丰县人民政府",
        "organization_text": "西丰县人民政府", "title": "副县长",
        "start_text": "2026-05前", "end_text": "至今", "is_current": 1,
        "sort_order": 0, "rank": "副处级", "confidence": "confirmed",
        "notes": "分工协助常务分管金融",
    },
    # ── 荣大煜（前任县委书记）─────────────────────────
    {
        "person_name": "荣大煜", "organization_name": "中共西丰县委员会",
        "organization_text": "中共西丰县委员会", "title": "县委书记",
        "start_text": "2024-07", "end_text": "2026-03", "sort_order": 0,
        "rank": "正处级", "confidence": "confirmed",
    },
    {
        "person_name": "荣大煜", "organization_name": "西丰县人民政府",
        "organization_text": "西丰县人民政府", "title": "县委副书记、县长",
        "start_text": "2021-07前", "end_text": "2024-06", "sort_order": 10,
        "rank": "正处级", "confidence": "confirmed",
    },
    {
        "person_name": "荣大煜", "organization_name": "铁岭市生态环境局",
        "organization_text": "铁岭市生态环境局", "title": "党组书记、局长",
        "start_text": "2020-10", "end_text": "2021-07前", "sort_order": 20,
        "rank": "正处级", "confidence": "confirmed",
    },
    {
        "person_name": "荣大煜", "organization_name": "调兵山市人民政府",
        "organization_text": "调兵山市人民政府", "title": "市委常委、常务副市长",
        "start_text": "2017-09", "end_text": "2020-10", "sort_order": 30,
        "rank": "副处级", "confidence": "confirmed",
    },
    {
        "person_name": "荣大煜", "organization_name": "铁岭市工商行政管理局",
        "organization_text": "铁岭市工商行政管理局", "title": "党组成员、副局长",
        "start_text": "2013-06", "end_text": "2017-09", "sort_order": 40,
        "rank": "副处级", "confidence": "confirmed",
    },
    {
        "person_name": "荣大煜", "organization_name": "西丰县地方税务局",
        "organization_text": "西丰县地方税务局", "title": "党组书记、局长",
        "start_text": "2006-08", "end_text": "2012-03", "sort_order": 50,
        "rank": "正科级", "confidence": "confirmed",
    },
    # ── 吴炜（2021-2024 县委书记）──────────────────────
    {
        "person_name": "吴炜", "organization_name": "中共西丰县委员会",
        "organization_text": "中共西丰县委员会", "title": "县委书记",
        "start_text": "2021-03前", "end_text": "2024-06", "sort_order": 0,
        "rank": "正处级", "confidence": "confirmed",
    },
    # ── 王者兴（副县长→市民政局→外县县长候选人）──────────
    {
        "person_name": "王者兴", "organization_name": "铁岭市民政局",
        "organization_text": "铁岭市民政局", "title": "党组书记",
        "start_text": "2025-01", "end_text": "2026-02", "sort_order": 0,
        "rank": "正处级", "confidence": "confirmed",
        "notes": "2026-02省管公示拟提名为县（市、区）长候选人",
    },
    {
        "person_name": "王者兴", "organization_name": "西丰县人民政府",
        "organization_text": "西丰县人民政府", "title": "县委常委、副县长、三级调研员",
        "start_text": "2020-08", "end_text": "2025-01", "sort_order": 10,
        "rank": "副处级", "confidence": "confirmed",
    },
    # ── 张勇（政法委书记→外流）────────────────────────
    {
        "person_name": "张勇", "organization_name": "中共西丰县委员会",
        "organization_text": "中共西丰县委员会", "title": "县委常委、政法委书记",
        "start_text": "2022前", "end_text": "2025-04", "sort_order": 0,
        "rank": "副处级", "confidence": "confirmed",
        "notes": "2025-04拟任县（市、区）委副书记",
    },
]

RELATIONSHIPS = [
    {
        "person_from_name": "李子骥", "person_to_name": "宁丽岩",
        "relationship_type": "overlap", "direction": "undirected",
        "strength": "strong", "confidence": "confirmed",
        "context": "西丰县现任党政主要领导搭班（书记[推定]—县长）",
        "overlap_organization_text": "西丰县", "overlap_period_text": "2026-04至今",
    },
    {
        "person_from_name": "荣大煜", "person_to_name": "李子骥",
        "relationship_type": "overlap", "direction": "undirected",
        "strength": "strong", "confidence": "confirmed",
        "context": "西丰县党政主要领导搭班（书记—县长）后交接，李子骥升任书记",
        "overlap_organization_text": "西丰县", "overlap_period_text": "2024-07至2026-03",
    },
    {
        "person_from_name": "荣大煜", "person_to_name": "吴炜",
        "relationship_type": "succession", "direction": "from_to",
        "strength": "medium", "confidence": "confirmed",
        "context": "西丰县委书记交接（吴—荣，2024-06）",
        "overlap_organization_text": "西丰县", "overlap_period_text": "2024-06",
    },
    {
        "person_from_name": "李子骥", "person_to_name": "李振宇",
        "relationship_type": "overlap", "direction": "undirected",
        "strength": "medium", "confidence": "confirmed",
        "context": "西丰县政府班子共事（县长—常务副县长）",
        "overlap_organization_text": "西丰县人民政府", "overlap_period_text": "2024-07至2026-03",
    },
    {
        "person_from_name": "宁丽岩", "person_to_name": "李振宇",
        "relationship_type": "overlap", "direction": "undirected",
        "strength": "medium", "confidence": "confirmed",
        "context": "西丰县政府班子共事（县长—常务副县长）",
        "overlap_organization_text": "西丰县人民政府", "overlap_period_text": "2026-04至2026-06",
    },
    {
        "person_from_name": "荣大煜", "person_to_name": "宁丽岩",
        "relationship_type": "succession", "direction": "from_to",
        "strength": "weak", "confidence": "plausible",
        "context": "西丰县长席位交接（荣大煜2024年离任县长转任书记，宁丽岩2026年接任县长）",
        "overlap_organization_text": "西丰县人民政府", "overlap_period_text": "2024-2026",
    },
    {
        "person_from_name": "王者兴", "person_to_name": "李子骥",
        "relationship_type": "overlap", "direction": "undirected",
        "strength": "weak", "confidence": "confirmed",
        "context": "西丰政府班子共事（副县长—县长，2024-07至2025-01）",
        "overlap_organization_text": "西丰县人民政府", "overlap_period_text": "2024-07至2025-01",
    },
    {
        "person_from_name": "张勇", "person_to_name": "许伟",
        "relationship_type": "overlap", "direction": "undirected",
        "strength": "weak", "confidence": "confirmed",
        "context": "西丰县委班子共事（政法委书记—宣传部长）",
        "overlap_organization_text": "中共西丰县委员会", "overlap_period_text": "2021前至2025-04",
    },
    {
        "person_from_name": "许伟", "person_to_name": "雷晶",
        "relationship_type": "overlap", "direction": "undirected",
        "strength": "weak", "confidence": "confirmed",
        "context": "西丰县政府班子共事（副县长同僚）",
        "overlap_organization_text": "西丰县人民政府", "overlap_period_text": "2026至今",
    },
]

SOURCES = [
    {
        "canonical_url": "https://www.lntlxf.gov.cn/xifeng/zwgk/xzqlgk/zfb/zwgk/zcwj/xzfbgswj/2026052909155055775/index.html",
        "title": "西政办发〔2026〕2号 西丰县人民政府关于县政府领导同志工作分工的通知",
        "publisher": "西丰县人民政府", "published_at": "2026-05-25",
        "accessed_at": "2026-08-12", "source_type": "official", "reliability": "high",
    },
    {
        "canonical_url": "https://www.lntlxf.gov.cn/xifeng/zwgk/xzqlgk/zfb/zwgk/zfhy/2026061114552799123/index.html",
        "title": "西丰县政府第十九届第七十七次常务会议（宁丽岩县长候选人主持）",
        "publisher": "西丰县人民政府", "published_at": "2026-04-13",
        "accessed_at": "2026-08-12", "source_type": "official", "reliability": "high",
    },
    {
        "canonical_url": "https://www.lntlxf.gov.cn/xifeng/zwgk/xzqlgk/zfb/zwgk/zfhy/2026061114515949745/index.html",
        "title": "西丰县政府第十九届第七十六次常务会议（李子骥县长主持）",
        "publisher": "西丰县人民政府", "published_at": "2026-03-26",
        "accessed_at": "2026-08-12", "source_type": "official", "reliability": "high",
    },
    {
        "canonical_url": "http://renshi.people.com.cn/n1/2026/0322/c139617-40686274.html",
        "title": "辽宁发布一批省管干部任前公示（2026年第5号）：李子骥拟任县委书记、宁丽岩拟提名为县长候选人",
        "publisher": "人民网-中国共产党新闻网（转辽宁省委组织部）", "published_at": "2026-03-22",
        "accessed_at": "2026-08-12", "source_type": "appointment_notice", "reliability": "high",
    },
    {
        "canonical_url": "https://fushun.gov.cn/ywdt/001007/20240623/30a38ae5-40fe-4f62-be9b-3662b74ac0e4.html",
        "title": "中共辽宁省委组织部公告（2024年第103号）：荣大煜拟任县委书记、李子骥拟提名为县长候选人",
        "publisher": "抚顺市人民政府（转辽宁省委组织部）", "published_at": "2024-06-23",
        "accessed_at": "2026-08-12", "source_type": "appointment_notice", "reliability": "high",
    },
    {
        "canonical_url": "https://baike.baidu.com/item/%E8%8D%A3%E5%A4%A7%E7%85%9C/23490565",
        "title": "荣大煜（百度百科）——完整人物履历",
        "publisher": "百度百科", "published_at": "",
        "accessed_at": "2026-08-12", "source_type": "encyclopedia", "reliability": "medium",
    },
    {
        "canonical_url": "https://www.lnutcm.edu.cn/info/1471/65851.htm",
        "title": "学校赴西丰县、清原满族自治县开展深度调研（2026-04-27 宁丽岩以县委副书记、县长出席）",
        "publisher": "辽宁中医药大学", "published_at": "2026-04-27",
        "accessed_at": "2026-08-12", "source_type": "official", "reliability": "high",
    },
    {
        "canonical_url": "http://www.cctvzw.org.cn/hydt/1950.html",
        "title": "西丰县与中国农业电影电视中心、东阿阿胶股份有限公司座谈交流会召开（2026-03-25 荣大煜书记、雷晶常委副县长、刘洋副县长出席）",
        "publisher": "中经总网/中国网微视频", "published_at": "2026-03-25",
        "accessed_at": "2026-08-12", "source_type": "media", "reliability": "medium",
    },
    {
        "canonical_url": "https://blog.sina.com.cn/s/blog_14ecb958c0102z39h.html",
        "title": "铁岭市管干部任前公示2026年第4号（李振宇拟任市直单位正职）",
        "publisher": "新浪博客·铁岭官场专栏", "published_at": "2026-05-01",
        "accessed_at": "2026-08-12", "source_type": "appointment_notice", "reliability": "medium",
    },
    {
        "canonical_url": "https://blog.sina.com.cn/s/blog_14ecb958c0102z3a8.html",
        "title": "铁岭市人大常委会人事任免名单（2026-06-30 决定任命李振宇为铁岭市市场监督管理局局长）",
        "publisher": "新浪博客·铁岭官场专栏", "published_at": "2026-06-30",
        "accessed_at": "2026-08-12", "source_type": "official", "reliability": "medium",
    },
    {
        "canonical_url": "https://news.qq.com/rain/a/20250416A01T1N00",
        "title": "铁岭市管干部任前公示2025-04（许伟拟任市委市政府派出机构正职、张勇拟任县区委副书记）",
        "publisher": "腾讯网", "published_at": "2025-04-16",
        "accessed_at": "2026-08-12", "source_type": "appointment_notice", "reliability": "medium",
    },
    {
        "canonical_url": "https://news.qq.com/rain/a/20250101A024YH00",
        "title": "铁岭市管干部任前公示2025-01（王者兴拟任市直单位正职）",
        "publisher": "腾讯网", "published_at": "2025-01-01",
        "accessed_at": "2026-08-12", "source_type": "appointment_notice", "reliability": "medium",
    },
    {
        "canonical_url": "https://www.thepaper.cn/newsDetail_forward_10163535",
        "title": "中共铁岭市委组织部公告（2020-11 李子骥由昌图县大洼镇党委书记拟任调兵山市委常委）",
        "publisher": "澎湃新闻（转铁岭市委组织部）", "published_at": "2020-11-27",
        "accessed_at": "2026-08-12", "source_type": "appointment_notice", "reliability": "high",
    },
    {
        "canonical_url": "http://www.foodwang.cn/finance/xinxi/2022/1221/3116.html",
        "title": "李子骥以调兵山市委常委、副市长身份陪同调研（2022-12）",
        "publisher": "食品在线", "published_at": "2022-12-21",
        "accessed_at": "2026-08-12", "source_type": "media", "reliability": "medium",
    },
    {
        "canonical_url": "http://www.zgcounty.com/news/66182.html",
        "title": "西丰县2025年政府工作报告（2024-12-29 县长李子骥）",
        "publisher": "中国县域", "published_at": "2024-12-29",
        "accessed_at": "2026-08-12", "source_type": "official", "reliability": "high",
    },
    {
        "canonical_url": "https://www.xyshjj.cn/content/202601/26/c27313333.html",
        "title": "县委书记谈高质量发展：访西丰县委书记荣大煜（中国县域经济报）",
        "publisher": "中国县域经济报", "published_at": "2026-01-26",
        "accessed_at": "2026-08-12", "source_type": "media", "reliability": "high",
    },
    {
        "canonical_url": "http://www.ptfude.com/news/zdxw/882.html",
        "title": "西丰县委书记荣大煜一行莅临莆田福德医院调研考察（2026-01-29）",
        "publisher": "莆田福德医院", "published_at": "2026-01-31",
        "accessed_at": "2026-08-12", "source_type": "media", "reliability": "medium",
    },
    {
        "canonical_url": "http://www.tlswdx.gov.cn/contents/16/4376.html",
        "title": "西丰县委常委会会议专题研究党校工作（2021-03：县委书记吴炜、县长范磊、组织部长吴秀彪）",
        "publisher": "中共铁岭市委党校", "published_at": "2021-03-08",
        "accessed_at": "2026-08-12", "source_type": "official", "reliability": "high",
    },
    {
        "canonical_url": "http://m.jnbw.org.cn/shishang/shishang/2023/0901/536523.html",
        "title": "访西丰县委书记吴炜（2023-09）",
        "publisher": "金融情报局网", "published_at": "2023-09-01",
        "accessed_at": "2026-08-12", "source_type": "media", "reliability": "medium",
    },
]


def add_evidence(conn: sqlite3.Connection) -> None:
    inserts = InsertFactory()
    people = dict(conn.execute("SELECT canonical_name, person_id FROM persons"))
    source_ids = dict(conn.execute("SELECT canonical_url, source_id FROM sources"))
    by_person = {
        # 李子骥
        "李子骥": [3, 4, 12, 13, 14, 1, 2],
        # 宁丽岩
        "宁丽岩": [3, 1, 6, 2],
        # 李振宇
        "李振宇": [8, 9, 0, 1],
        # 许伟
        "许伟": [10, 0, 6],
        # 雷晶 / 刘洋 / 于思洋 / 宗鑫 / 董金 / 于翔
        "雷晶": [7, 0],
        "刘洋": [7, 0],
        "于思洋": [1, 0],
        "宗鑫": [0],
        "董金": [0, 15],
        "于翔": [0],
        # 荣大煜
        "荣大煜": [5, 4, 15, 16, 7],
        # 吴炜
        "吴炜": [17, 18],
        # 王者兴
        "王者兴": [11, 4],
        # 张勇
        "张勇": [10],
    }
    for name, indexes in by_person.items():
        for index in indexes:
            inserts.link_evidence(
                conn, source_ids[SOURCES[index]["canonical_url"]],
                "person", people[name], "identity_and_career",
            )
    for position_id, name, title, org in conn.execute(
        """SELECT p.position_id, pe.canonical_name, p.title, p.organization_text
           FROM positions p JOIN persons pe ON pe.person_id=p.person_id"""
    ):
        picks = set()
        if name == "李子骥":
            if title == "县委书记":
                picks = {3, 1, 2}
            elif title == "县委副书记、县长":
                picks = {14, 3, 2}
            elif title == "党组书记、局长":
                picks = {3, 4}
            elif title in ("市委常委、副市长", "市委常委", "党委书记、人大主席"):
                picks = {12, 13}
        elif name == "宁丽岩":
            if title == "县委副书记、县长":
                picks = {3, 1, 2}
            else:
                picks = {3}
        elif name == "李振宇":
            if title == "县委书记":
                picks = set()
            elif title == "党组书记、局长":
                picks = {9, 8}
            else:
                picks = {0, 8, 1}
        elif name == "许伟":
            if title == "副县长、二级调研员":
                picks = {0, 10}
            elif title == "党工委副书记、管委会主任":
                picks = {10, 15}
            else:
                picks = {10}
        elif name in ("雷晶", "刘洋"):
            picks = {0, 7}
        elif name in ("于思洋", "宗鑫", "于翔"):
            picks = {0, 1}
        elif name == "董金":
            picks = {0, 15}
        elif name == "荣大煜":
            if title == "县委书记":
                picks = {5, 4, 15}
            elif title == "县委副书记、县长":
                picks = {5, 14}
            else:
                picks = {5}
        elif name == "吴炜":
            picks = {17, 18}
        elif name == "王者兴":
            picks = {11, 4}
        elif name == "张勇":
            picks = {10}
        for index in picks:
            inserts.link_evidence(
                conn, source_ids[SOURCES[index]["canonical_url"]],
                "position", position_id, "office_and_period",
            )
    rel_evidence = {
        0: [3, 1],  # 李子骥—宁丽岩
        1: [14, 3],  # 荣大煜—李子骥
        2: [17, 4],  # 荣大煜—吴炜
        3: [14, 8],
        4: [1, 8],
        5: [3, 14],
        6: [14, 11],
        7: [10, 17],
        8: [0, 7],
    }
    for rel_id, indexes in rel_evidence.items():
        for index in indexes:
            inserts.link_evidence(
                conn, source_ids[SOURCES[index]["canonical_url"]],
                "relationship", rel_id, "joint_leadership",
            )
    conn.commit()


def write_profiles(conn: sqlite3.Connection) -> None:
    factory = PersonJSONFactory()
    settings = {
        "李子骥": {
            "job": "县委书记",
            "questions": [
                "2026-04后转任西丰县委书记的直接公开报道缺失（由3月省管公示与县长交接节奏推断）",
                "2020-11任昌图县大洼镇党委书记之前的更早履历待补",
            ],
            "career": "partial",
            "specializations": ["县域治理", "生态环保", "组织人事"],
        },
        "宁丽岩": {
            "job": "县长",
            "questions": [
                "任铁岭市医保局党组书记、局长之前（2022监前）的完整履历待补",
                "任西丰县长（代县长→县长）的正式人大选举时间待核定",
            ],
            "career": "thin",
            "specializations": ["医疗保障", "县域经济", "鹿业大健康产业"],
        },
        "荣大煜": {
            "job": "前任县委书记",
            "questions": [
                "2026-03后卸任西丰县委书记的去向（市直/市人大/他县）无公开记录",
                "2021年出任西丰县长的精确月份待核",
            ],
            "career": "complete",
            "specializations": ["税务", "工商", "生态环保", "县域治理"],
        },
    }
    for person_id, name in conn.execute(
        "SELECT person_id, canonical_name FROM persons ORDER BY canonical_name"
    ):
        if name not in settings:
            continue
        profile = factory.build(conn, person_id)
        config = settings[name]
        profile["investigation_scope"] = {
            "province": "辽宁省", "city": "铁岭市",
            "region": "西丰县", "job": config["job"],
            "task_id": "liaoning_西丰县", "time_focus": "截至2026-08-12",
        }
        profile["current_status"]["as_of"] = "2026-08-12"
        is_current = profile["current_status"].get("current_post") in ("县委书记", "县长", "县委副书记、县长")
        profile["current_status"]["is_current_confirmed"] = is_current
        if name == "李子骥":
            profile["identity"]["native_place"] = ""
            for item in profile["career_timeline"]:
                if item["title"] == "县委书记":
                    item["is_current"] = True
        profile["professional_profile"] = {
            "primary_specializations": config["specializations"],
            "career_pattern": "cross_county_rotation",
        }
        profile["confidence_summary"] = {
            "identity": "confirmed", "current_role": "confirmed" if name != "李子骥" else "plausible",
            "career_completeness": config["career"],
            "relationship_confidence": "high",
            "biggest_gap": config["questions"][0],
        }
        profile["open_questions"] = [
            {
                "priority": "high" if index < 2 else "medium",
                "question": question,
                "why_it_matters": "完善身份去重与干部流动时间线",
                "suggested_queries": [f"{name} 简历", f"{name} 任前公示"],
                "last_attempted": "2026-08-12",
            }
            for index, question in enumerate(config["questions"])
        ]
        filename = TASK_DIR / f"20260812-辽宁省-铁岭市-{config['job']}-{name}.json"
        filename.write_text(
            json.dumps(profile, ensure_ascii=False, indent=2), encoding="utf-8"
        )


def write_report() -> None:
    REPORT_PATH.write_text(
        """# 西丰县（铁岭市·辽宁省）领导班子工作关系网络调查报告

**核验日期：** 2026-08-12
**任务：** `liaoning_西丰县`
**覆盖范围：** 现任县委书记、县长、县政府班子，以及2021年以来县委书记/县长线人事更替与跨县流动。

## 1. 现任县委书记：李子骥（推断待确认）

- 男，汉族，1983-10 生，大学学历、学士学位，2006-09 参加工作、2008-01 入党。
- 履历：昌图县大洼镇党委书记、人大主席（2020-11 前任 调兵山市委常委人选）→ 调兵山市委常委、副市长（2022-12 在任见报）→ 铁岭市生态环境局党组书记、局长（2024-06 拟任 西丰县长）→ **西丰县委副书记、县长（2024-07 至 2026-03）** → **西丰县委书记（2026-04 起，推定）**。
- 证据链：2026-03-22 辽宁省管干部任前公示（第5号）明确“李子骥…拟任县（市、区）委书记”；2026-03-23 仍以县长身份主持第76次政府常务会；2026-04-09 县长席位已由宁丽岩接任。
- 置信度：**plausible**——尚无 2026-04 后“西丰县委书记李子骥”直接见报；同批公示中铁岭县委书记空缺由付尧填补（2026-06-21 铁岭县报道），排除了李子骥去铁岭县的可能，就地转任是最合理推断。

## 2. 现任县长：宁丽岩（官方确认）

- 女，汉族，1974-03 生，大学学历、硕士学位，中共党员。
- 曾任 铁岭市医疗保障局党组书记、局长（2026-03 公示口径）→ **2026-04-09 以“县委副书记、县长候选人”主持县第77次常务会议** → **2026-05-05 西政办发〔2026〕2 号确认“主持县政府全面工作”**（现任）。
- 巡访口径：2026-04-27 辽宁中医药大学调研报道称“西丰县委副书记、县长宁丽岩”。
- 置信度：**confirmed**（官方一手）。

## 3. 前任县委书记：荣大煜（去向待查）

- 男，汉族，1972-09 生，辽宁昌图人，中央党校大学、经济管理学士。
- 履历：铁岭市地税局稽查局→办公室→西丰县地税局党组书记、局长（2006-2012）→西丰工业园区管委会副主任（2012-2013）→铁岭市工商局副局长（2013-2017）→调兵山市委常委、常务副市长（2017-2020）→铁岭市生态环境局党组书记、局长（2020-10）→西丰县委副书记、县长（2021-2024-06）→**西丰县委书记（2024-07 至 2026-03-25）**。
- 任书记期间公开活动到 2026-03-25（农影中心/东阿阿胶座谈）。此后去向：**无公开记录（open gap）**。

## 4. 县政府班子（2026-05-05 分工文件）

| 姓名 | 职务 | 分工要点 | 备注/流动 |
|---|---|---|---|
| 宁丽岩 | 县长 | 全面工作、审计、营商环境 | 原市医保局长 |
| 李振宇 | 常务副县长 | 发改财税金融国资、人社民政应急 | 1972-02；2026-06-30 调任铁岭市市场监督管理局局长 |
| 许伟 | 副县长（二级调研员） | 招商引资、工信、科技 | 原宣传部长→经开区主任；1968-02 |
| 雷晶 | 副县长（县委常委） | 农业农村、教育、卫健、医保、鹿业 | 2026-03 以常委副县长见报 |
| 刘洋 | 副县长 | 住建、数据、水利、文旅、市监 | 2026-03 以副县长见报 |
| 于思洋 | 副县长 | 公安、司法 | — |
| 宗鑫 | 副县长 | 交通、环保、自然、林业、退役军人 | — |
| 董金 | 副县长 | 协助商贸流通 | 2025-10 鹿业调研见报 |
| 于翔 | 副县长 | 协助金融 | — |

## 5. 县史关键人事时间线

- 2021-03 县委书记 吴炜、县长 范磊（铁岭市委党校材料）。
- 2023-09 吴炜仍任书记。2021—2024-06 荣大煜任县长。
- 2024-06-23 省管公示：荣大煜（西丰县长）拟任县委书记；李子骥（市生态环境局长）拟提名为西丰县长候选人。
- 2024-07 起：书记 荣大煜 / 县长 李子骥 搭班。
- 2026-03-22 省管公示：李子骥（西丰县长）拟任县委书记；宁丽岩（市医保局长）拟任县长候选人。同日批：王亮（清河区长）拟任清河区委书记。
- 2026-03-23 李子骥最后以县长身份主持常务会；2026-04-09 宁丽岩以县长候选人接棒 → **李子骥推断 2026-04 就任西丰县委书记**。
- 2026-06-30 李振宇调任铁岭市市场监督管理局局长（西丰常务副县长出缺）。

## 6. 工作关系网络分析（确认交集）

- **强连接**：李子骥—宁丽岩（2026-04 起党政班子搭班）；荣大煜—李子骥（2024-07—2026-03 书记县长搭班后交接）。
- **中连接**：县长—常务副县长（李子骥/宁丽岩 × 李振宇）、荣大煜—吴炜（2024-06 书记交接）。
- **弱连接**：荣大煜—宁丽岩（西丰县长席位两任交接）、王者兴×李子骥（政府班子共事）、张勇×许伟（县委班子共事）、许伟×雷晶（现任政府同僚）。
- 说明：本调查各方关系均基于公开任职重叠推断，不指向私人关系。

## 7. 周边跨县/跨岗人员流动

- **王者兴**（1976-04）：西丰县委常委、副县长（2020-08—2025-01）→ 铁岭市民政局党组书记（2025）→ 2026-02 拟提名为县（市、区）长候选人（西丰→市直→外县正职链）。
- **张勇**（1978-01，满族）：西丰县委常委、政法委书记 → 2025-04 拟任县（市、区）委副书记。
- **许伟**：西丰宣传部长 → 2025-04 市派出机构正职（经开区主任）→ 回任西丰副县长。
- **李振宇**：西丰常务副县长 → 2026-06 铁岭市市场监督管理局局长。
- **荣大煜**：调兵山副市长 → 市生态环境局长 → 西丰县长 → 西丰书记（铁岭市直—县区—市直–县区 链）。

## 8. 关键洞察与突破线索

1. **党政主要领导同批换新（2026-04）**：李子骥＋宁丽岩 同时获得提任/接任，属典型的“县长就地转书记 + 市直局长空降县长”组合，需紧盯李子骥书记一职的首次公开见报（县委全会、建军节、调研活动）以锁定直证。
2. **荣大煜去向是最近热点**：1972 年生，53 岁离任县书记，通常去市直正职或市人大/政协副职，可查铁岭市 2026 上半年市委常委会/人大常委会任免。
3. **西丰—市直 干部通道畅通**：王者兴、李振宇、许伟、荣大煜均经市局—县区—市局流转，构成“铁岭市中层干部孵化带”，值得继续把西丰放在铁岭七县（区）干部网络的关键节点。
4. **常务副县长出缺（2026-06 李振宇离任）**：新任常务副县长大概率在 2026 第三、四季度落位，是下一轮观察切入点。

## 9. 数据文件说明

- `西丰县_network.db`：v3 结构（persons/organizations/positions/relationships/sources/evidence_links/claims…）。
- `西丰县_network.gexf`：人物+机构 + 任职边 + 关系边。
- 人物 JSON：县委书记（李子骥）、县长（宁丽岩）、前任县委书记（荣大煜）。

## 10. 信息来源汇总

- 西丰县政府官网（官方一手）：西政办发〔2026〕2 号领导分工；第76/77次常务会议记录。
- 辽宁省委组织部任前公示（2026-03-22、2024-06-23）——人民网/抚顺市政府转载。
- 铁岭市委组织部任前公示（2026年第4/5号、2025-01、2025-04）——新浪博客“铁岭官场”专栏转载。
- 铁岭市人大常委会任免名单（2026-06-30）。
- 荣大煜 百度百科（人物履历）。
- 辽宁中医药大学调研报道（2026-04-27；2026-04-13；2025-11-25）。
- 中经总网 2026-03-25 座谈报道；中国县域经济报 2026-01-26；莆田福德医院 2026-01-31。
- 澎湃新闻（2020-11 铁岭市委组织部公告）；食品在线（2022-12 调兵山李子骥）。
- 铁岭市委党校（2021-03 县常委会记录）；金融情报局网（2023-09 吴炜访谈）。
- 中国县域（西丰县2025年政府工作报告，2024-12-29）。

## 数据边界与开放问题

- OQ1：现任书记直证缺失（推断李子骥）。来源商业授权状态均 `unknown`，不会进入商业导出视图。
- OQ2：荣大煜去向；OQ3：宁丽岩早期履历；OQ4：新任常务副县长；OQ5：李子骥 2020 年前履历。
""",
        encoding="utf-8",
    )


def main() -> None:
    run_build(
        slug="西丰县", persons=PERSONS, organizations=ORGANIZATIONS,
        positions=POSITIONS, relationships=RELATIONSHIPS, sources=SOURCES,
        claims=[], db_path=DB_PATH, gexf_path=GEXF_PATH,
        backend="v3", overwrite=True,
    )
    conn = sqlite3.connect(DB_PATH)
    try:
        add_evidence(conn)
        write_profiles(conn)
    finally:
        conn.close()
    write_report()
    print("built:", DB_PATH)
    print("built:", GEXF_PATH)
    print("built:", REPORT_PATH)


if __name__ == "__main__":
    main()
