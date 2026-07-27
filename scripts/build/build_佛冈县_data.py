#!/usr/bin/env python3
"""
佛冈县领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

Level: 县
Province: 广东省
City: 清远市
County: 佛冈县
Targets: 县委书记 & 县长

Research Date: 2026-07-22

Research Notes:
- 芦湛（县委书记）的身份通过佛冈县人民政府官网多篇2026年新闻确认：
  http://www.fogang.gov.cn/ (首页新闻: 2026-06-29 县委十四届第130次常委会; 2026-07-06 第131次常委会; 2026-07-20 第132次常委会)
- 江红平（县长）的身份通过县政府领导之窗页面确认：
  http://www.fogang.gov.cn/ldzc/xzf/content/post_927396.html
  简历：江红平，男，汉族，1980年09月生，研究生，经济学博士，中共党员
- 县政府领导班子7人全部通过官方领导之窗页面确认
- 县委领导班子页面不可直接访问，县委常委成员信息通过县政府领导页面获取
- 芦湛的履历（出生年份、籍贯、学历、历任职务）完全缺失——县委领导页面不可访问

Sources:
  - http://www.fogang.gov.cn/ — 官网首页
  - http://www.fogang.gov.cn/ldzc/xzf/index.html — 县政府领导班子页面
  - 各领导人个人简历页面
"""

import sqlite3  # noqa: used by gov_relation.runner

from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
from gov_relation.runner import run_build

# ═══════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════

# fmt: off
PERSONS = [
    # ── Core targets: 县委书记 & 县长 ──
    {
        "id": 1,
        "name": "芦湛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中共佛冈县委书记",
        "current_org": "中共佛冈县委员会",
        "source": "佛冈县政府门户网站新闻: 2026-06-29起频发出席常委会活动。简历尚未公开。",
    },
    {
        "id": 2,
        "name": "江红平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年09月",
        "birthplace": "",
        "education": "研究生，经济学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "佛冈县人民政府",
        "source": "http://www.fogang.gov.cn/ldzc/xzf/content/post_927396.html — 江红平简历",
    },
    # ── 县政府领导班子 ──
    {
        "id": 3,
        "name": "陈技",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年07月",
        "birthplace": "",
        "education": "大学（硕士）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县政府党组副书记、副县长",
        "current_org": "佛冈县人民政府",
        "source": "http://www.fogang.gov.cn/ldzc/xzf/content/post_1958498.html — 陈技简历",
    },
    {
        "id": 4,
        "name": "解晟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年08月",
        "birthplace": "",
        "education": "大学，理学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、县政府党组成员、副县长",
        "current_org": "佛冈县人民政府",
        "source": "http://www.fogang.gov.cn/ldzc/xzf/content/post_1371858.html — 解晟简历",
    },
    {
        "id": 5,
        "name": "王澍",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年06月",
        "birthplace": "",
        "education": "研究生，公共管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府党组成员（挂职）、副县长",
        "current_org": "佛冈县人民政府",
        "source": "http://www.fogang.gov.cn/ldzc/xzf/content/post_1818766.html — 王澍简历",
    },
    {
        "id": 6,
        "name": "邓锐文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年04月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府党组成员、副县长，兼任县公安局局长",
        "current_org": "佛冈县人民政府/佛冈县公安局",
        "source": "http://www.fogang.gov.cn/ldzc/xzf/content/post_2039202.html — 邓锐文简历",
    },
    {
        "id": 7,
        "name": "叶荣盛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年05月",
        "birthplace": "",
        "education": "研究生，行政管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府党组成员、副县长",
        "current_org": "佛冈县人民政府",
        "source": "http://www.fogang.gov.cn/ldzc/xzf/content/post_1834622.html — 叶荣盛简历",
    },
    {
        "id": 8,
        "name": "姚莹丽",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1977年03月",
        "birthplace": "",
        "education": "本科",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政府党组成员、副县长",
        "current_org": "佛冈县人民政府",
        "source": "http://www.fogang.gov.cn/ldzc/xzf/content/post_1917355.html — 姚莹丽简历",
    },
    # ── 佛冈县四套班子 ──
    {
        "id": 9,
        "name": "县人大常委会主任（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "佛冈县人大常委会",
        "source": "placeholder - 领导页面不可访问",
    },
    {
        "id": 10,
        "name": "县政协主席（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "中国人民政治协商会议佛冈县委员会",
        "source": "placeholder - 领导页面不可访问",
    },
    # ── 县纪委 ──
    {
        "id": 11,
        "name": "县纪委书记（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县纪委书记",
        "current_org": "中共佛冈县纪律检查委员会",
        "source": "placeholder - 领导页面不可访问",
    },
    # ── 前县委书记 ──
    {
        "id": 12,
        "name": "前任佛冈县委书记（待确认）",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "已离任",
        "current_org": "",
        "source": "placeholder - 芦湛前任信息待查",
    },
]

ORGANIZATIONS = [
    {"id": 1, "name": "中共佛冈县委员会", "type": "党委", "level": "正处级", "parent": "中共清远市委员会", "location": "清远市佛冈县"},
    {"id": 2, "name": "佛冈县人民政府", "type": "政府", "level": "正处级", "parent": "清远市人民政府", "location": "清远市佛冈县"},
    {"id": 3, "name": "佛冈县人大常委会", "type": "人大", "level": "正处级", "parent": "清远市人大常委会", "location": "清远市佛冈县"},
    {"id": 4, "name": "中国人民政治协商会议佛冈县委员会", "type": "政协", "level": "正处级", "parent": "清远市政协", "location": "清远市佛冈县"},
    {"id": 5, "name": "中共佛冈县纪律检查委员会", "type": "纪委", "level": "正处级", "parent": "中共清远市纪律检查委员会", "location": "清远市佛冈县"},
    {"id": 6, "name": "佛冈县公安局", "type": "政府", "level": "正科级", "parent": "佛冈县人民政府", "location": "清远市佛冈县"},
    {"id": 7, "name": "广州对口帮扶清远指挥部驻佛冈工作队", "type": "事业单位", "level": "县处级", "parent": "", "location": "清远市佛冈县"},
]

POSITIONS = [
    # 芦湛
    {"person_id": 1, "org_id": 1, "title": "中共佛冈县委书记", "start_date": "", "end_date": "present", "rank": "正处级", "note": "2026年6月前已任职"},
    # 江红平
    {"person_id": 2, "org_id": 2, "title": "县委副书记、县政府党组书记、县长", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "县委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 陈技
    {"person_id": 3, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "县政府党组副书记、副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "协助县长处理县政府日常事务"},
    # 解晟
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "县政府党组成员、副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "负责住建、交通、水利、城管等"},
    # 王澍（挂职）
    {"person_id": 5, "org_id": 2, "title": "县政府党组成员（挂职）、副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "挂职，广州对口帮扶"},
    {"person_id": 5, "org_id": 7, "title": "广州对口帮扶清远指挥部驻佛冈工作队队长", "start_date": "", "end_date": "present", "rank": "", "note": ""},
    # 邓锐文
    {"person_id": 6, "org_id": 2, "title": "县政府党组成员、副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "兼任县公安局局长"},
    {"person_id": 6, "org_id": 6, "title": "佛冈县公安局局长", "start_date": "", "end_date": "present", "rank": "正科级", "note": ""},
    # 叶荣盛
    {"person_id": 7, "org_id": 2, "title": "县政府党组成员、副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "负责教育、民政、人社、卫健等"},
    # 姚莹丽
    {"person_id": 8, "org_id": 2, "title": "县政府党组成员、副县长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "负责自然资源、农业农村、乡村振兴等"},
    # 四套班子负责人（待确认）
    {"person_id": 9, "org_id": 3, "title": "县人大常委会主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": "待确认具体姓名"},
    {"person_id": 10, "org_id": 4, "title": "县政协主席", "start_date": "", "end_date": "present", "rank": "正处级", "note": "待确认具体姓名"},
    {"person_id": 11, "org_id": 5, "title": "县委常委、县纪委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": "待确认具体姓名"},
]

RELATIONSHIPS = [
    # 党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "党政正职搭档", "context": "县委书记-县长党政正职搭档", "overlap_org": "佛冈县四套班子", "overlap_period": "2026至今", "source": "佛冈县政府门户网站", "confidence": "confirmed"},
    # 县委常委关系
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "县委书记—县委常委（陈技）", "overlap_org": "佛冈县委常委会", "overlap_period": "2026至今", "source": "", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "县委书记—县委常委（解晟）", "overlap_org": "佛冈县委常委会", "overlap_period": "2026至今", "source": "", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 11, "type": "上下级", "context": "县委书记—县纪委书记", "overlap_org": "佛冈县委常委会", "overlap_period": "2026至今", "source": "", "confidence": "plausible"},
    # 县长与副县长
    {"person_a": 2, "person_b": 3, "type": "党政副职搭档", "context": "县长—常务副县长（陈技）", "overlap_org": "佛冈县人民政府", "overlap_period": "2026至今", "source": "", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 4, "type": "党政副职搭档", "context": "县长—副县长（解晟）", "overlap_org": "佛冈县人民政府", "overlap_period": "2026至今", "source": "", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 5, "type": "党政副职搭档", "context": "县长—挂职副县长（王澍）", "overlap_org": "佛冈县人民政府", "overlap_period": "2026至今", "source": "", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 6, "type": "党政副职搭档", "context": "县长—副县长兼公安局长（邓锐文）", "overlap_org": "佛冈县人民政府", "overlap_period": "2026至今", "source": "", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 7, "type": "党政副职搭档", "context": "县长—副县长（叶荣盛）", "overlap_org": "佛冈县人民政府", "overlap_period": "2026至今", "source": "", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 8, "type": "党政副职搭档", "context": "县长—副县长（姚莹丽）", "overlap_org": "佛冈县人民政府", "overlap_period": "2026至今", "source": "", "confidence": "confirmed"},
    # 副县长之间同僚关系
    {"person_a": 3, "person_b": 4, "type": "同僚", "context": "县委常委—副县长之间同僚关系", "overlap_org": "佛冈县党政班子", "overlap_period": "2026至今", "source": "", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 5, "type": "同僚", "context": "常务副县长—挂职副县长", "overlap_org": "佛冈县人民政府", "overlap_period": "2026至今", "source": "", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 6, "type": "同僚", "context": "常务副县长—公安局长", "overlap_org": "佛冈县人民政府", "overlap_period": "2026至今", "source": "", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 7, "type": "同僚", "context": "常务副县长—副县长（叶荣盛）", "overlap_org": "佛冈县人民政府", "overlap_period": "2026至今", "source": "", "confidence": "confirmed"},
    {"person_a": 3, "person_b": 8, "type": "同僚", "context": "常务副县长—副县长（姚莹丽）", "overlap_org": "佛冈县人民政府", "overlap_period": "2026至今", "source": "", "confidence": "confirmed"},
    # 四套班子正职之间
    {"person_a": 1, "person_b": 9, "type": "同僚", "context": "县委书记—县人大常委会主任", "overlap_org": "佛冈县四套班子", "overlap_period": "2026至今", "source": "", "confidence": "plausible"},
    {"person_a": 1, "person_b": 10, "type": "同僚", "context": "县委书记—县政协主席", "overlap_org": "佛冈县四套班子", "overlap_period": "2026至今", "source": "", "confidence": "plausible"},
    {"person_a": 2, "person_b": 9, "type": "同僚", "context": "县长—县人大常委会主任", "overlap_org": "佛冈县四套班子", "overlap_period": "2026至今", "source": "", "confidence": "plausible"},
    {"person_a": 2, "person_b": 10, "type": "同僚", "context": "县长—县政协主席", "overlap_org": "佛冈县四套班子", "overlap_period": "2026至今", "source": "", "confidence": "plausible"},
    # 前后任关系
    {"person_a": 12, "person_b": 1, "type": "前后任", "context": "前任佛冈县委书记—现任县委书记（芦湛）", "overlap_org": "中共佛冈县委员会", "overlap_period": "", "source": "", "confidence": "unverified"},
]

# fmt: on

# ═══════════════════════════════════════════════════════════════
# BUILD
# ═══════════════════════════════════════════════════════════════

DB_PATH = DATABASE_DIR / "佛冈县_network.db"
GEXF_PATH = GRAPH_DIR / "佛冈县_network.gexf"

if __name__ == "__main__":
    run_build(
        slug="佛冈县",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
