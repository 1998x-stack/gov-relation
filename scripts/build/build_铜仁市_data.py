#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 铜仁市 leadership network (地级市).

Targets: 市委书记 (李作勋) & 市长 (穆嵘坤)
Data as of: 2026-08-05
Sources:
- 铜仁市人民政府门户 www.trs.gov.cn / www.tongren.gov.cn — 领导之窗 (市委/市政府领导班子, 2025-2026 更新)
- 中国经济网 district.ce.cn 地方党政领导人物库 (铜仁市委书记/市长名单)
- 中国经济网《李作勋任铜仁市委书记》(2022-03-29)
- 人民网贵州省管干部任前言公示 (2023-02-20 穆嵘坤拟提名市长候选人; 2021-01 黔西南州常务副州长)
- 贵州省政府任免通知 (2021-09-23 穆嵘坤任省乡村振兴局党组书记、局长)
- 铜仁市人大公告 (2026-02-11 胡洪成当选市人大常委会主任)
- 政协铜仁市委员会补选公告 (2025-02-27 喻国君补选为主席)
- 澎湃新闻/网易 (前任肖洪投案 2025-03-24; 皮贵怀被查 2023-03-17; 陈少荣被查 2025-01-02)
"""

import os
import sqlite3
from datetime import datetime

# Staging directory (this file lives in data/tmp/guizhou_铜仁市/)
TMP_DIR = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(TMP_DIR, "..", "..", "..")
DB_PATH = os.path.join(TMP_DIR, "铜仁市_network.db")
GEXF_PATH = os.path.join(TMP_DIR, "铜仁市_network.gexf")

# ── Data ──────────────────────────────────────────────────────────────────

persons = [
    # === Current Top Leaders ===
    {
        "id": 1, "name": "李作勋", "gender": "男", "ethnicity": "汉族",
        "birth": "1972年10月", "birthplace": "贵州遵义",
        "education": "南京大学，研究生，哲学博士",
        "party_join": "1993年5月", "work_start": "1996年3月",
        "current_post": "铜仁市委书记",
        "current_org": "中共铜仁市委员会",
        "source": "中国经济网 district.ce.cn 2022-03-29; 铜仁市政府官网 www.trs.gov.cn 领导之窗 2026",
    },
    {
        "id": 2, "name": "穆嵘坤", "gender": "男", "ethnicity": "汉族",
        "birth": "1972年9月", "birthplace": "贵州遵义",
        "education": "贵州省委党校在职研究生(经济学)、云南大学工程硕士",
        "party_join": "1998年3月", "work_start": "1991年8月",
        "current_post": "铜仁市委副书记、市人民政府市长、市政府党组书记",
        "current_org": "铜仁市人民政府",
        "source": "铜仁市政府官网/领导之窗 2023-02-26; 人民网 任前言公示 2023-02-20",
    },
    # === 市委常委 & 政府领导 ===
    {
        "id": 3, "name": "兰青", "gender": "男", "ethnicity": "",
        "birth": "1978年10月", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "铜仁市委常委、市人民政府常务副市长",
        "current_org": "铜仁市人民政府",
        "source": "铜仁市政府官网·领导之窗 2026-06-30; 贵州人大/动静",
    },
    {
        "id": 4, "name": "张勇", "gender": "男", "ethnicity": "",
        "birth": "1975年8月", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "铜仁市委常委、市人民政府副市长",
        "current_org": "铜仁市人民政府",
        "source": "铜仁市政府官网·领导之窗 2026-07-08",
    },
    {
        "id": 5, "name": "张茂", "gender": "男", "ethnicity": "回族",
        "birth": "1975年12月", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "铜仁市委常委、市委政法委书记",
        "current_org": "中共铜仁市委员会",
        "source": "铜仁市政府官网·领导之窗 2026-02-28 政法会议",
    },
    {
        "id": 6, "name": "许飞", "gender": "女", "ethnicity": "",
        "birth": "1979年7月", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "铜仁市委常委、市委宣传部部长、市委统战部部长、市委教育工委书记",
        "current_org": "中共铜仁市委员会",
        "source": "铜仁市政府官网·领导之窗; 澎湃/贵州统战部(2025-03-17)",
    },
    {
        "id": 7, "name": "王剑波", "gender": "男", "ethnicity": "",
        "birth": "1971年9月", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "铜仁市委常委、市纪委书记、市监委主任",
        "current_org": "铜仁市纪委监委",
        "source": "铜仁市政府官网·领导之窗 2026-06-11",
    },
    {
        "id": 8, "name": "向波", "gender": "男", "ethnicity": "",
        "birth": "1975年8月", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "铜仁市委常委、市委秘书长、市委办公室主任",
        "current_org": "中共铜仁市委员会",
        "source": "铜仁市政府官网·领导之窗 2026-07-17",
    },
    {
        "id": 9, "name": "杨启明", "gender": "男", "ethnicity": "仡佬族",
        "birth": "1973年8月", "birthplace": "贵州石阡",
        "education": "在职本科(贵州教育学院)",
        "party_join": "", "work_start": "",
        "current_post": "铜仁市委常委、玉屏县委书记、大龙经开区党工委书记、市政协副主席",
        "current_org": "中共铜仁市委员会 / 中共玉屏县委",
        "source": "铜仁市政府官网·领导之窗 2026-01-06; 大龙经开区官网 2025-04-08",
    },
    {
        "id": 10, "name": "蒋雪明", "gender": "男", "ethnicity": "",
        "birth": "1982年8月", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "铜仁市委常委、市委组织部部长、市委党校校长(兼)、市委国企工委书记",
        "current_org": "中共铜仁市委员会",
        "source": "铜仁市政府官网·领导之窗 2026-08-03",
    },
    {
        "id": 11, "name": "王飚", "gender": "", "ethnicity": "",
        "birth": "1967年10月", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "铜仁市人民政府副市长",
        "current_org": "铜仁市人民政府",
        "source": "铜仁市政府官网·领导之窗(政府) 2025-03-21",
    },
    {
        "id": 12, "name": "李俊宏", "gender": "", "ethnicity": "",
        "birth": "1971年5月", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "铜仁市人民政府副市长",
        "current_org": "铜仁市人民政府",
        "source": "铜仁市政府官网·领导之窗(政府) 2025-03-21",
    },
    {
        "id": 13, "name": "吴启疆", "gender": "", "ethnicity": "",
        "birth": "1977年8月", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "铜仁市人民政府副市长",
        "current_org": "铜仁市人民政府",
        "source": "铜仁市政府官网·领导之窗(政府) 2025-09-22",
    },
    {
        "id": 14, "name": "吴绍东", "gender": "", "ethnicity": "",
        "birth": "1970年1月", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "铜仁市人民政府副市长、市公安局局长",
        "current_org": "铜仁市人民政府 / 市公安局",
        "source": "铜仁市政府官网·领导之窗(政府) 2025-03-21",
    },
    {
        "id": 15, "name": "杨雪峰", "gender": "", "ethnicity": "",
        "birth": "1978年7月", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "铜仁市人民政府副市长",
        "current_org": "铜仁市人民政府",
        "source": "铜仁市政府官网·领导之窗(政府) 2025-03-21",
    },
    {
        "id": 16, "name": "马兴方", "gender": "", "ethnicity": "",
        "birth": "1980年9月", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "铜仁市人民政府党组成员、秘书长",
        "current_org": "铜仁市人民政府",
        "source": "铜仁市政府官网·领导之窗(政府) 2025-03-21",
    },
    # === 人大 / 政协 ===
    {
        "id": 17, "name": "胡洪成", "gender": "男", "ethnicity": "侗族",
        "birth": "1969年9月", "birthplace": "贵州江口",
        "education": "省委党校研究生",
        "party_join": "", "work_start": "",
        "current_post": "铜仁市人大常委会主任、党组书记",
        "current_org": "铜仁市人大常委会",
        "source": "铜仁网公告第1号(2026-02-11); 百度百科",
    },
    {
        "id": 18, "name": "喻国君", "gender": "男", "ethnicity": "土家族",
        "birth": "1969年12月", "birthplace": "贵州德江",
        "education": "省委党校研究生、理学学士",
        "party_join": "", "work_start": "",
        "current_post": "政协铜仁市委员会主席、党组书记",
        "current_org": "政协铜仁市委员会",
        "source": "政协补选公告(2025-02-27); 百度百科",
    },
    # === 前任 / 网络相关 ===
    {
        "id": 19, "name": "陈昌旭", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "贵州遵义",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "（前任铜仁市委书记）贵州省政府发展研究中心党组书记",
        "current_org": "中共铜仁市委员会 / 贵州省政府发展研究中心",
        "source": "中国经济网 district.ce.cn; 黔西南州委官网",
    },
    {
        "id": 20, "name": "皮贵怀", "gender": "男", "ethnicity": "汉族",
        "birth": "1972年3月", "birthplace": "湖南益阳",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "（前任铜仁市长，已被查）",
        "current_org": "铜仁市人民政府",
        "source": "媒体/纪委监委报道(2023-03-17 被查)",
    },
    {
        "id": 21, "name": "陈少荣", "gender": "男", "ethnicity": "",
        "birth": "", "birthplace": "",
        "education": "", "party_join": "", "work_start": "",
        "current_post": "（前任铜仁市长，已被查）",
        "current_org": "铜仁市人民政府",
        "source": "贵州省纪委监委通报(2025-01-02 被查)",
    },
    {
        "id": 22, "name": "韩佐芝", "gender": "男", "ethnicity": "仡佬族",
        "birth": "1972年5月", "birthplace": "贵州遵义道真",
        "education": "哈尔滨工业大学 MPA",
        "party_join": "", "work_start": "",
        "current_post": "（前任铜仁市委组织部部长）安顺市政协党组书记",
        "current_org": "中共铜仁市委组织部 / 政协安顺市委员会",
        "source": "百度百科; 网易(韩佐芝任安顺市政协党组书记)",
    },
]

organizations = [
    {"id": 1, "name": "中共铜仁市委员会", "type": "党委",
     "level": "地级市", "parent": "中共贵州省委员会", "location": "贵州省铜仁市"},
    {"id": 2, "name": "铜仁市人民政府", "type": "政府",
     "level": "地级市", "parent": "贵州省人民政府", "location": "贵州省铜仁市"},
    {"id": 3, "name": "铜仁市人大常委会", "type": "人大",
     "level": "地级市", "parent": "贵州省人大常委会", "location": "贵州省铜仁市"},
    {"id": 4, "name": "政协铜仁市委员会", "type": "政协",
     "level": "地级市", "parent": "政协贵州省委员会", "location": "贵州省铜仁市"},
    {"id": 5, "name": "铜仁市纪委监委", "type": "党委",
     "level": "地级市", "parent": "贵州省纪委监委", "location": "贵州省铜仁市"},
    {"id": 6, "name": "中共贵州省委员会", "type": "党委",
     "level": "省级", "parent": "", "location": "贵州省贵阳市"},
    {"id": 7, "name": "贵州省人民政府", "type": "政府",
     "level": "省级", "parent": "", "location": "贵州省贵阳市"},
    {"id": 8, "name": "中共黔西南州委员会", "type": "党委",
     "level": "地级市", "parent": "中共贵州省委员会", "location": "贵州省黔西南州"},
    {"id": 9, "name": "贵州省政府发展研究中心", "type": "事业单位",
     "level": "省级", "parent": "贵州省人民政府", "location": "贵州省贵阳市"},
    {"id": 10, "name": "中共玉屏侗族自治县委员会", "type": "党委",
     "level": "县", "parent": "中共铜仁市委员会", "location": "贵州省铜仁市玉屏县"},
    {"id": 11, "name": "大龙经开区管委会", "type": "开发区",
     "level": "地级市", "parent": "铜仁市人民政府", "location": "贵州省铜仁市"},
    {"id": 12, "name": "政协安顺市委员会", "type": "政协",
     "level": "地级市", "parent": "政协贵州省委员会", "location": "贵州省安顺市"},
]

positions = [
    # 李作勋（市委书记）
    {"person_id": 1, "org_id": 1, "title": "铜仁市委书记", "start": "2022-03", "end": "present", "rank": "正厅级", "note": "2022-03-29 中国经济网报道就任"},
    {"person_id": 1, "org_id": 6, "title": "贵州省委副秘书长(正厅)、省委办公厅主任", "start": "~2019", "end": "2022-03", "rank": "正厅级", "note": "接任铜仁市委书记前任职"},
    {"person_id": 1, "org_id": 6, "title": "贵州省委办公厅处室（贵阳多岗/省发改委）", "start": "unknown", "end": "~2019", "rank": "", "note": "早期履历待补（调研称曾任职贵阳多岗）"},
    # 穆嵘坤（市长）
    {"person_id": 2, "org_id": 2, "title": "铜仁市人民政府市长、市政府党组书记", "start": "2023-03-02", "end": "present", "rank": "正厅级", "note": "2023-03-02 当选；2023-02-25 代理市长"},
    {"person_id": 2, "org_id": 1, "title": "铜仁市委副书记", "start": "2023-02", "end": "present", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 7, "title": "贵州省乡村振兴局党组书记、局长", "start": "2021-09-23", "end": "2023-02", "rank": "正厅级", "note": "省政府任免通知"},
    {"person_id": 2, "org_id": 7, "title": "贵州省农业农村厅党组成员", "start": "~2021", "end": "2023-02", "rank": "正厅级", "note": ""},
    {"person_id": 2, "org_id": 8, "title": "黔西南州委副书记、州委政法委书记", "start": "unknown", "end": "2017-12", "rank": "副厅级", "note": ""},
    {"person_id": 2, "org_id": 8, "title": "黔西南州委常委、组织部部长", "start": "~2012", "end": "unknown", "rank": "副厅级", "note": ""},
    {"person_id": 2, "org_id": 8, "title": "黔西南州常务副州长", "start": "2017-12-27", "end": "~2018", "rank": "副厅级", "note": "八届人大第6次会议"},
    {"person_id": 2, "org_id": 6, "title": "遵义县政府办→遵义市政府办→遵义市委系统职务", "start": "1991-08", "end": "~2012", "rank": "", "note": "早期履历（月份未完全核实）"},
    # 兰青（常务副市长，东部→西部交流）
    {"person_id": 3, "org_id": 2, "title": "铜仁市委常委、常务副市长", "start": "2026-06-30", "end": "present", "rank": "副厅级", "note": "2026-06-30 任命"},
    {"person_id": 3, "org_id": 7, "title": "贵州省发改委副主任", "start": "2024-08", "end": "2026-06", "rank": "副厅级", "note": "此前任深圳发改委"},
    {"person_id": 3, "org_id": 7, "title": "深圳市发改委协调发展处处长", "start": "unknown", "end": "2024-08", "rank": "正处级", "note": "东部→西部干部交流"},
    # 其他常委 / 副市长
    {"person_id": 4, "org_id": 2, "title": "铜仁市委常委、市人民政府副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 5, "org_id": 1, "title": "铜仁市委常委、市委政法委书记", "start": "2025-12", "end": "present", "rank": "副厅级", "note": "此前任市委宣传部长兼统战部长"},
    {"person_id": 6, "org_id": 1, "title": "铜仁市委常委、市委宣传部部长、统战部部长、教育工委书记", "start": "2025-03", "end": "present", "rank": "副厅级", "note": "原贵州省委宣传部政策研究室主任/贵州文化演艺集团副总（空降）"},
    {"person_id": 7, "org_id": 5, "title": "铜仁市委常委、市纪委书记、市监委主任", "start": "2026", "end": "present", "rank": "副厅级", "note": "原贵州省纪委派驻省交通运输厅纪检组副组长/组长（空降）"},
    {"person_id": 8, "org_id": 1, "title": "铜仁市委常委、市委秘书长、市委办公室主任", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 9, "org_id": 10, "title": "玉屏县委书记（铜仁市委常委兼任）", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 9, "org_id": 11, "title": "大龙经开区党工委书记", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": 9, "org_id": 4, "title": "政协铜仁市委员会副主席（兼）", "start": "", "end": "present", "rank": "", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "铜仁市委常委、市委组织部部长、市委党校校长、市国企工委书记", "start": "2026-08", "end": "present", "rank": "副厅级", "note": "接任组织部长"},
    {"person_id": 11, "org_id": 2, "title": "铜仁市人民政府副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "铜仁市人民政府副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "铜仁市人民政府副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "铜仁市人民政府副市长、市公安局局长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "铜仁市人民政府副市长", "start": "", "end": "present", "rank": "副厅级", "note": ""},
    {"person_id": 16, "org_id": 2, "title": "铜仁市人民政府党组成员、秘书长", "start": "", "end": "present", "rank": "正处级", "note": ""},
    # 人大 / 政协
    {"person_id": 17, "org_id": 3, "title": "铜仁市人大常委会主任、党组书记", "start": "2026-02-11", "end": "present", "rank": "正厅级", "note": "2026-02 当选；曾任遵义市委常委、常务副市长/省林业局局长"},
    {"person_id": 18, "org_id": 4, "title": "政协铜仁市委员会主席、党组书记", "start": "2025-02-27", "end": "present", "rank": "正厅级", "note": "2024-12 拟任；2025-02-27 补选"},
    # 前任书记 / 市长
    {"person_id": 19, "org_id": 1, "title": "铜仁市委书记（前任）", "start": "2016-08", "end": "2022-03", "rank": "正厅级", "note": "前任陈昌旭；李作勋 2022-03 接任"},
    {"person_id": 19, "org_id": 8, "title": "黔西南州委书记", "start": "2022-03", "end": "2025-11", "rank": "正厅级", "note": "调任黔西南"},
    {"person_id": 19, "org_id": 9, "title": "贵州省政府发展研究中心党组书记", "start": "2025-11", "end": "present", "rank": "正厅级", "note": "2025-11 转省直"},
    {"person_id": 20, "org_id": 2, "title": "铜仁市人民政府市长（前任、被查）", "start": "2021-03", "end": "2023-01", "rank": "正厅级", "note": "2023-01 离任；2023-03-17 被查"},
    {"person_id": 21, "org_id": 2, "title": "铜仁市人民政府市长（前任、被查）", "start": "2018-01", "end": "2021-01", "rank": "正厅级", "note": "任安顺市委书记后 2025-01-02 被查"},
    {"person_id": 22, "org_id": 1, "title": "铜仁市委组织部部长（前任）", "start": "2024-04", "end": "2026", "rank": "副厅级", "note": "省人大常委会副秘书长 → 铜仁组织部 → 安顺政协"},
]

relationships = [
    # 党政一把手搭档
    {
        "person_a": 1, "person_b": 2,
        "type": "党政一把手搭档",
        "context": "李作勋（市委书记）与穆嵘坤（市委副书记、市长、市政府党组书记）为铜仁市党政一把手搭档，共同主持市委、市政府全面工作，同场出席市委深改委会议、'八一'走访慰问等",
        "overlap_org": "中共铜仁市委 / 铜仁市政府",
        "overlap_period": "2023-03 至今",
        "strength": "strong",
        "confidence": "confirmed",
    },
    # 书记—常委上下级
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "李作勋（书记）与兰青（市委常委、常务副市长）同班子", "overlap_org": "中共铜仁市委", "overlap_period": "2026", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "张茂为市委政法委书记", "overlap_org": "中共铜仁市委", "overlap_period": "2026", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "王剑波为市纪委书记（空降）", "overlap_org": "中共铜仁市委", "overlap_period": "2026", "strength": "strong", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 10, "type": "上下级", "context": "蒋雪明为市委组织部长", "overlap_org": "中共铜仁市委", "overlap_period": "2026", "strength": "strong", "confidence": "confirmed"},
    # 市委交流 / 空降网络
    {"person_a": 6, "person_b": 7, "type": "overlap", "context": "许飞（宣传）与王剑波（纪检）均为 2025-2026 自贵州省直空降铜仁的常委，同级省级干部下派", "overlap_org": "中共铜仁市委", "overlap_period": "2025-2026", "strength": "medium", "confidence": "plausible"},
    {"person_a": 10, "person_b": 22, "type": "predecessor_successor", "context": "蒋雪明（2026-08）接任韩佐芝（2024-2026）任组织部长；韩调安顺市政协党组书记", "overlap_org": "中共铜仁市委组织部", "overlap_period": "2026", "strength": "medium", "confidence": "confirmed"},
    # 人大 / 政协
    {"person_a": 1, "person_b": 17, "type": "共事", "context": "李作勋（书记）与胡洪成（市人大主任）共同出席'八一'走访、半年经济会", "overlap_org": "铜仁市四套班子", "overlap_period": "2026", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 17, "type": "共事", "context": "穆嵘坤（市长）与胡洪成共同出席市政府各项会议", "overlap_org": "铜仁市四套班子", "overlap_period": "2026", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 18, "type": "共事", "context": "穆嵘坤（市长）与喻国君（市政协主席）共同出席春节慰问、两会", "overlap_org": "铜仁市四套班子", "overlap_period": "2025-2026", "strength": "medium", "confidence": "confirmed"},
    # 前任后任
    {"person_a": 1, "person_b": 19, "type": "predecessor_successor", "context": "李作勋 2022-03 接替陈昌旭任铜仁市委书记；陈调黔西南州委书记", "overlap_org": "中共铜仁市委", "overlap_period": "2022-03", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 20, "type": "predecessor_successor", "context": "穆嵘坤 2023-03 接任市长；前任皮贵怀 2023-03-17 被查", "overlap_org": "铜仁市政府", "overlap_period": "2023", "strength": "medium", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 21, "type": "predecessor_successor", "context": "陈少荣2018-2021任铜仁市长，后任安顺市委书记，2025-01-02 被查", "overlap_org": "铜仁市政府", "overlap_period": "2018-2021", "strength": "medium", "confidence": "confirmed"},
    # 本土网络
    {"person_a": 9, "person_b": 17, "type": "same_native_place", "context": "杨启明（贵州石阡人）本土提拔；胡洪成（江口人）本地系统成长", "overlap_org": "铜仁市", "overlap_period": "", "strength": "weak", "confidence": "plausible"},
    # 跨区域轮换
    {"person_a": 2, "person_b": 22, "type": "cross_region", "context": "穆嵘坤（遵义→黔西南→省乡村振兴→铜仁）与 韩佐芝（省人大→铜仁→安顺）均体现贵州跨地市轮换", "overlap_org": "贵州省级干部系统", "overlap_period": "", "strength": "weak", "confidence": "plausible"},
]

# ── Build SQLite DB ───────────────────────────────────────────────────────

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS relationships;
DROP TABLE IF EXISTS positions;
DROP TABLE IF EXISTS organizations;
DROP TABLE IF EXISTS persons;

CREATE TABLE persons (
    id INTEGER PRIMARY KEY,
    name TEXT, gender TEXT, ethnicity TEXT,
    birth TEXT, birthplace TEXT, education TEXT,
    party_join TEXT, work_start TEXT,
    current_post TEXT, current_org TEXT, source TEXT
);
CREATE TABLE IF NOT EXISTS organizations (
    id INTEGER PRIMARY KEY,
    name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
);
CREATE TABLE IF NOT EXISTS positions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_id INTEGER, org_id INTEGER,
    title TEXT, start TEXT, end TEXT, rank TEXT, note TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);
CREATE TABLE IF NOT EXISTS relationships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    person_a INTEGER, person_b INTEGER,
    type TEXT, context TEXT,
    overlap_org TEXT, overlap_period TEXT,
    strength TEXT, confidence TEXT,
    FOREIGN KEY (person_a) REFERENCES persons(id),
    FOREIGN KEY (person_b) REFERENCES persons(id)
);
""")

cur.executemany(
    "INSERT OR REPLACE INTO persons VALUES(:id,:name,:gender,:ethnicity,:birth,:birthplace,:education,:party_join,:work_start,:current_post,:current_org,:source)",
    persons,
)
cur.executemany(
    "INSERT OR REPLACE INTO organizations VALUES(:id,:name,:type,:level,:parent,:location)",
    organizations,
)
cur.executemany(
    "INSERT INTO positions(person_id,org_id,title,start,end,rank,note) VALUES(:person_id,:org_id,:title,:start,:end,:rank,:note)",
    positions,
)
cur.executemany(
    "INSERT INTO relationships(person_a,person_b,type,context,overlap_org,overlap_period,strength,confidence) VALUES(:person_a,:person_b,:type,:context,:overlap_org,:overlap_period,:strength,:confidence)",
    relationships,
)

conn.commit()

cur.execute("SELECT COUNT(*) FROM persons")
pc = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM organizations")
oc = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM positions")
ps = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM relationships")
rc = cur.fetchone()[0]
conn.close()

print(f"Database: {DB_PATH}")
print(f"  Persons: {pc}, Organizations: {oc}, Positions: {ps}, Relationships: {rc}")

# ── Build GEXF Graph ─────────────────────────────────────────────────────


def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(p):
    post = p.get("current_post", "")
    if "市委书记" in post:
        return "255,50,50"
    if "市长" in post and "副" not in post:
        return "50,100,255"
    if "纪委" in post:
        return "255,165,0"
    if "人大" in post:
        return "200,255,255"
    if "政协" in post:
        return "255,240,200"
    if "副市长" in post or "秘书长" in post:
        return "100,100,255"
    return "100,100,100"


def org_color(o):
    color_map = {
        "党委": "255,200,200", "政府": "200,200,255", "开发区": "200,255,200",
        "乡镇,街道": "255,255,200", "事业单位": "220,220,220", "群团": "255,220,255",
        "人大": "200,255,255", "政协": "255,240,200",
    }
    return color_map.get(o.get("type", ""), "200,200,200")


today = datetime.now().strftime("%Y-%m-%d")

node_lines = []
for p in persons:
    c = person_color(p)
    sz = "20.0" if ("市委书记" in p["current_post"] or ("市长" in p["current_post"] and "副" not in p["current_post"])) else "12.0"
    node_lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    node_lines.append('        <attvalues>')
    node_lines.append('          <attvalue for="0" value="person"/>')
    node_lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
    node_lines.append(f'          <attvalue for="2" value="{esc(p.get("ethnicity",""))}"/>')
    node_lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
    node_lines.append('        </attvalues>')
    c = person_color(p).split(",")
    node_lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
    node_lines.append(f'        <viz:size value="{sz}"/>')
    node_lines.append('      </node>')

for o in organizations:
    node_lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    node_lines.append('        <attvalues>')
    node_lines.append('          <attvalue for="0" value="organization"/>')
    node_lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
    node_lines.append('        </attvalues>')
    c = org_color(o).split(",")
    node_lines.append(f'        <viz:color r="{c[0]}" g="{c[1]}" b="{c[2]}"/>')
    node_lines.append('        <viz:size value="8.0"/>')
    node_lines.append('      </node>')

edge_lines = []
eid = 0
for pos in positions:
    eid += 1
    edge_lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
    edge_lines.append('        <attvalues>')
    edge_lines.append('          <attvalue for="0" value="worked_at"/>')
    edge_lines.append(f'          <attvalue for="1" value="{esc(pos.get("start",""))}"/>')
    edge_lines.append(f'          <attvalue for="2" value="{esc(pos.get("end",""))}"/>')
    edge_lines.append('        </attvalues>')
    edge_lines.append('      </edge>')
for r in relationships:
    eid += 1
    w = "3.0" if r["strength"] == "strong" else ("2.0" if r["strength"] == "medium" else "1.0")
    edge_lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{w}">')
    edge_lines.append('        <attvalues>')
    edge_lines.append('          <attvalue for="0" value="relationship"/>')
    edge_lines.append(f'          <attvalue for="1" value="{esc(r.get("overlap_period",""))}"/>')
    edge_lines.append(f'          <attvalue for="2" value="{esc(r.get("context",""))}"/>')
    edge_lines.append(f'          <attvalue for="3" value="{esc(r.get("confidence",""))}"/>')
    edge_lines.append('        </attvalues>')
    edge_lines.append('      </edge>')

gexf_lines = []
gexf_lines.append('<?xml version="1.0" encoding="UTF-8"?>')
gexf_lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
gexf_lines.append(f'  <meta lastmodifieddate="{today}">')
gexf_lines.append('    <creator>Sisyphus Research Agent</creator>')
gexf_lines.append('    <description>铜仁市领导班子工作关系网络 — 市委书记李作勋与市长穆嵘坤（地级市）</description>')
gexf_lines.append('  </meta>')
gexf_lines.append('  <graph mode="static" defaultedgetype="undirected">')
gexf_lines.append('    <attributes class="node">')
gexf_lines.append('      <attribute id="0" title="type" type="string"/>')
gexf_lines.append('      <attribute id="1" title="role" type="string"/>')
gexf_lines.append('      <attribute id="2" title="ethnicity" type="string"/>')
gexf_lines.append('      <attribute id="3" title="birth" type="string"/>')
gexf_lines.append('    </attributes>')
gexf_lines.append('    <attributes class="edge">')
gexf_lines.append('      <attribute id="0" title="edge_type" type="string"/>')
gexf_lines.append('      <attribute id="1" title="period" type="string"/>')
gexf_lines.append('      <attribute id="2" title="context" type="string"/>')
gexf_lines.append('      <attribute id="3" title="confidence" type="string"/>')
gexf_lines.append('    </attributes>')
gexf_lines.append('    <nodes>')
gexf_lines.extend(node_lines)
gexf_lines.append('    </nodes>')
gexf_lines.append('    <edges>')
gexf_lines.extend(edge_lines)
gexf_lines.append('    </edges>')
gexf_lines.append('  </graph>')
gexf_lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(gexf_lines))

print(f"Graph:   {GEXF_PATH}")
print(f"  Nodes: {len(persons)+len(organizations)}, Edges: {eid}")
print("铜仁市 network build complete.")