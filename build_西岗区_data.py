#!/usr/bin/env python3
"""Build 西岗区 (Xigang District, Dalian, Liaoning) personnel network database and graph."""

import os
import sys
from datetime import datetime

# ── Paths ──────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(BASE, "..", "..", ".."))
sys.path.insert(0, REPO_ROOT)

from gov_relation.runner import run_build

SLUG = "西岗区"
TASK_ID = "liaoning_西岗区"

# ── Persons ──────────────────────────────────────────────────────────
persons = [
    # ════════ Top Leaders ════════
    {
        "id": 1,
        "name": "杨海三",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中国共产党大连市西岗区委员会",
        "source": "https://www.163.com/dy/article/JJ8EFHCS05563DJA.html",
    },
    {
        "id": 2,
        "name": "张琛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年7月",
        "birthplace": "",
        "education": "大学学历，硕士学位",
        "party_join": "2002年7月",
        "work_start": "2004年7月",
        "current_post": "区委副书记、区长",
        "current_org": "大连市西岗区人民政府",
        "source": "https://baike.baidu.com/item/%E5%BC%A0%E7%90%9B/24214003",
    },
    # ════════ Party Standing Committee Members ════════
    {
        "id": 3,
        "name": "李鹏业",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年8月",
        "birthplace": "",
        "education": "大学学历，学士学位",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、副区长（常务）",
        "current_org": "大连市西岗区人民政府",
        "source": "https://www.dlxg.gov.cn/minglu/content.jsp?user_id=145",
    },
    {
        "id": 4,
        "name": "蔡学石",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年7月",
        "birthplace": "",
        "education": "研究生学历，硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "大连市西岗区人民政府",
        "source": "https://www.dlxg.gov.cn/minglu/content.jsp?user_id=140",
    },
    {
        "id": 5,
        "name": "曲光耀",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年5月",
        "birthplace": "",
        "education": "大学学历，硕士学位",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、区政府党组成员",
        "current_org": "大连市西岗区人民政府",
        "source": "https://www.dlxg.gov.cn/minglu/content.jsp?user_id=136",
    },
    # ════════ Government Leaders ════════
    {
        "id": 6,
        "name": "姜正山",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年5月",
        "birthplace": "",
        "education": "中央党校大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长、西岗公安分局局长",
        "current_org": "大连市西岗区人民政府",
        "source": "https://www.dlxg.gov.cn/minglu/content.jsp?user_id=82",
    },
    {
        "id": 7,
        "name": "张璐",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年11月",
        "birthplace": "",
        "education": "大学学历，学士学位",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "大连市西岗区人民政府",
        "source": "https://www.dlxg.gov.cn/minglu/content.jsp?user_id=146",
    },
    {
        "id": 8,
        "name": "丁丽丽",
        "gender": "女",
        "ethnicity": "满族",
        "birth": "1980年12月",
        "birthplace": "",
        "education": "大学学历，硕士学位",
        "party_join": "",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "大连市西岗区人民政府",
        "source": "https://www.dlxg.gov.cn/minglu/content.jsp?user_id=120",
    },
    # ════════ Legislative & Advisory ════════
    {
        "id": 9,
        "name": "常胜强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年1月",
        "birthplace": "辽宁瓦房店",
        "education": "研究生学历，硕士学位",
        "party_join": "1993年11月",
        "work_start": "1995年7月",
        "current_post": "区人大常委会主任",
        "current_org": "大连市西岗区人民代表大会常务委员会",
        "source": "https://baike.baidu.com/item/%E5%B8%B8%E8%83%9C%E5%BC%BA",
    },
    {
        "id": 10,
        "name": "苗亚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年3月",
        "birthplace": "",
        "education": "在职大学学历，学士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "中国人民政治协商会议大连市西岗区委员会",
        "source": "https://baike.baidu.com/item/%E8%8B%97%E4%BA%9A",
    },
    # ════════ Important Predecessors ════════
    {
        "id": 11,
        "name": "王标",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "大连市委常委、秘书长",
        "current_org": "中国共产党大连市委员会",
        "source": "https://www.163.com/dy/article/JJ8EFHCS05563DJA.html",
    },
    {
        "id": 12,
        "name": "阎利军",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（离任）",
        "current_org": "",
        "source": "http://www.hotelaah.com/liren/liaoning_dalian_xigang.html",
    },
    {
        "id": 13,
        "name": "徐从琪",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（退休后被查）",
        "current_org": "",
        "source": "搜狗搜索结果",
    },
    {
        "id": 14,
        "name": "吴开华",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "（离任）",
        "current_org": "",
        "source": "http://www.hotelaah.com/liren/liaoning_dalian_xigang.html",
    },
]

# ── Organizations ──────────────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "中国共产党大连市西岗区委员会",
        "type": "党委",
        "level": "区级（正处级）",
        "parent": "中国共产党大连市委员会",
        "location": "大连市西岗区",
    },
    {
        "id": 2,
        "name": "大连市西岗区人民政府",
        "type": "政府",
        "level": "区级（正处级）",
        "parent": "大连市人民政府",
        "location": "大连市西岗区",
    },
    {
        "id": 3,
        "name": "大连市西岗区人民代表大会常务委员会",
        "type": "人大",
        "level": "区级（正处级）",
        "parent": "",
        "location": "大连市西岗区",
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议大连市西岗区委员会",
        "type": "政协",
        "level": "区级（正处级）",
        "parent": "",
        "location": "大连市西岗区",
    },
    {
        "id": 5,
        "name": "大连市公安局西岗分局",
        "type": "政府",
        "level": "区级（副处级）",
        "parent": "大连市西岗区人民政府",
        "location": "大连市西岗区",
    },
    {
        "id": 6,
        "name": "大连市中山区",
        "type": "政府",
        "level": "区级（正处级）",
        "parent": "大连市人民政府",
        "location": "大连市中山区",
    },
    {
        "id": 7,
        "name": "大连市信访局",
        "type": "政府",
        "level": "副厅级",
        "parent": "大连市人民政府",
        "location": "大连市",
    },
    {
        "id": 8,
        "name": "中国共产党瓦房店市委员会",
        "type": "党委",
        "level": "县级市（正处级）",
        "parent": "中国共产党大连市委员会",
        "location": "大连市瓦房店市",
    },
    {
        "id": 9,
        "name": "共青团沈阳市委员会",
        "type": "群团",
        "level": "副厅级",
        "parent": "",
        "location": "沈阳市",
    },
    {
        "id": 10,
        "name": "中共沈阳市委网络安全和信息化委员会办公室",
        "type": "党委",
        "level": "副厅级",
        "parent": "中国共产党沈阳市委员会",
        "location": "沈阳市",
    },
    {
        "id": 11,
        "name": "中国共产党沈阳市浑南区委员会",
        "type": "党委",
        "level": "区级（正处级）",
        "parent": "中国共产党沈阳市委员会",
        "location": "沈阳市浑南区",
    },
    {
        "id": 12,
        "name": "沈阳棋盘山国际风景旅游开发区管理委员会",
        "type": "开发区",
        "level": "副厅级",
        "parent": "沈阳市人民政府",
        "location": "沈阳市浑南区",
    },
    {
        "id": 13,
        "name": "中国共产党大连市委员会",
        "type": "党委",
        "level": "副省级",
        "parent": "中国共产党辽宁省委员会",
        "location": "大连市",
    },
]

# ── Positions ──────────────────────────────────────────────────────
positions = [
    # ** 杨海三 **
    {"person_id": 1, "org_id": 6, "title": "中山区干部（科技局、政府办、桂林街道、人民路街道、民政局等）", "start": "", "end": "约2015年", "rank": "", "note": "早年在大连市中山区多部门任职"},
    {"person_id": 1, "org_id": 7, "title": "大连市信访局副局长", "start": "约2015年", "end": "约2018年", "rank": "副局级", "note": ""},
    {"person_id": 1, "org_id": 8, "title": "瓦房店市委副书记", "start": "约2018年", "end": "2020年", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 2, "title": "西岗区委副书记、区长", "start": "2021年", "end": "2024年12月", "rank": "正处级", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "西岗区委书记", "start": "2024年12月", "end": "", "rank": "正处级", "note": "现任"},

    # ** 张琛 **
    {"person_id": 2, "org_id": 9, "title": "共青团沈阳市委员会办公室主任", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 2, "org_id": 10, "title": "沈阳市委网信办副主任", "start": "", "end": "", "rank": "副局级", "note": ""},
    {"person_id": 2, "org_id": 11, "title": "浑南区委常委、副区长（负责常务工作）", "start": "", "end": "", "rank": "副厅级?", "note": "负责区政府常务工作"},
    {"person_id": 2, "org_id": 12, "title": "棋盘山管委会分管日常工作的副主任", "start": "", "end": "2026年4月", "rank": "副厅级", "note": "党工委副书记"},
    {"person_id": 2, "org_id": 2, "title": "西岗区委副书记、代区长", "start": "2026年5月6日", "end": "2026年6月2日", "rank": "正处级", "note": "区人大常委会任命"},
    {"person_id": 2, "org_id": 2, "title": "西岗区委副书记、区长", "start": "2026年6月2日", "end": "", "rank": "正处级", "note": "区人大会议选举"},

    # ** 李鹏业 **
    {"person_id": 3, "org_id": 2, "title": "区委常委、副区长（常务）", "start": "", "end": "", "rank": "副处级", "note": "负责常务工作"},

    # ** 蔡学石 **
    {"person_id": 4, "org_id": 2, "title": "区委常委、副区长", "start": "", "end": "", "rank": "副处级", "note": ""},

    # ** 曲光耀 **
    {"person_id": 5, "org_id": 2, "title": "区委常委、区政府党组成员", "start": "", "end": "", "rank": "副处级", "note": ""},

    # ** 姜正山 **
    {"person_id": 6, "org_id": 5, "title": "西岗公安分局局长", "start": "", "end": "", "rank": "", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副区长", "start": "", "end": "", "rank": "副处级", "note": "兼任公安分局局长"},

    # ** 张璐 **
    {"person_id": 7, "org_id": 2, "title": "副区长", "start": "", "end": "", "rank": "副处级", "note": ""},

    # ** 丁丽丽 **
    {"person_id": 8, "org_id": 2, "title": "副区长", "start": "", "end": "", "rank": "副处级", "note": ""},

    # ** 常胜强 **
    {"person_id": 9, "org_id": 3, "title": "区人大常委会主任", "start": "2025年12月31日", "end": "", "rank": "正处级", "note": "当选"},

    # ** 苗亚 **
    {"person_id": 10, "org_id": 4, "title": "区政协主席", "start": "2025年12月31日", "end": "", "rank": "正处级", "note": "当选"},

    # ** 王标（前任书记） **
    {"person_id": 11, "org_id": 1, "title": "西岗区委书记", "start": "", "end": "2024年12月", "rank": "正处级", "note": ""},
    {"person_id": 11, "org_id": 13, "title": "大连市委常委、秘书长", "start": "2024年12月", "end": "", "rank": "副厅级", "note": "升任"},

    # ** 阎利军（更早书记） **
    {"person_id": 12, "org_id": 1, "title": "西岗区委书记", "start": "约2016年5月", "end": "约2021年", "rank": "正处级", "note": ""},

    # ** 徐从琪 （历史书记，退休被查）**
    {"person_id": 13, "org_id": 1, "title": "西岗区委书记", "start": "", "end": "", "rank": "正处级", "note": ""},

    # ** 吴开华（前区长） **
    {"person_id": 14, "org_id": 2, "title": "西岗区长", "start": "约2007年", "end": "约2021年", "rank": "正处级", "note": "任期约14年"},
]

# ── Relationships ──────────────────────────────────────────────────
relationships = [
    # 杨海三 → 张琛（前后任区长）
    {"person_a": 1, "person_b": 2, "type": "前后任", "context": "杨海三2021-2024任区长，张琛2026年接任区长", "overlap_org": "大连市西岗区人民政府", "overlap_period": ""},
    # 杨海三 → 王标（前后任书记）
    {"person_a": 1, "person_b": 11, "type": "前后任", "context": "王标前任西岗区委书记→大连市委常委/秘书长，杨海三2024.12接任书记", "overlap_org": "中国共产党大连市西岗区委员会", "overlap_period": ""},
    # 王标 → 阎利军（前后任书记）
    {"person_a": 11, "person_b": 12, "type": "前后任", "context": "阎利军约2016-约2021任书记，王标接任", "overlap_org": "中国共产党大连市西岗区委员会", "overlap_period": ""},
    # 杨海三 → 常胜强（同事，书记-人大主任）
    {"person_a": 1, "person_b": 9, "type": "同事", "context": "区委书记与区人大常委会主任", "overlap_org": "大连市西岗区", "overlap_period": "2025年至今"},
    # 杨海三 → 苗亚（同事，书记-政协主席）
    {"person_a": 1, "person_b": 10, "type": "同事", "context": "区委书记与区政协主席", "overlap_org": "大连市西岗区", "overlap_period": "2025年至今"},
    # 张琛 → 李鹏业（上下级，正副区长）
    {"person_a": 2, "person_b": 3, "type": "上下级", "context": "区长与常务副区长", "overlap_org": "大连市西岗区人民政府", "overlap_period": "2026年至今"},
    # 张琛 → 蔡学石（上下级）
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "区长与副区长（区委常委）", "overlap_org": "大连市西岗区人民政府", "overlap_period": "2026年至今"},
    # 张琛 → 曲光耀（同事，区委常委）
    {"person_a": 2, "person_b": 5, "type": "同事", "context": "区委副书记与区委常委", "overlap_org": "中国共产党大连市西岗区委员会", "overlap_period": "2026年至今"},
    # 李鹏业 → 蔡学石（同事，常委+副区长）
    {"person_a": 3, "person_b": 4, "type": "同事", "context": "同为区委常委、副区长", "overlap_org": "大连市西岗区人民政府", "overlap_period": ""},
    # 杨海三 → 吴开华（前后任区长）
    {"person_a": 1, "person_b": 14, "type": "前后任", "context": "吴开华约2007-2021任西岗区长，杨海三2021接任", "overlap_org": "大连市西岗区人民政府", "overlap_period": ""},
]

# ── Build ──────────────────────────────────────────────────────────
if __name__ == "__main__":
    from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DATABASE_DIR / f"{SLUG}_network.db",
        gexf_path=GRAPH_DIR / f"{SLUG}_network.gexf",
    )
    print(f"\n✨ {SLUG} build complete!")
