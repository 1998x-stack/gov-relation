#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 郑州市 (Zhengzhou City) leadership network.

郑州市（副省级城市）是河南省省会、国家中心城市。本脚本覆盖：
- 现任市委书记、市长
- 市政府领导班子（副市长、秘书长）
- 前任书记、市长
- 关键职务关系网络
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/郑州市_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/郑州市_network.gexf")

# ── DATA ────────────────────────────────────────────────────────────────────

persons = [
    # ═══════════════ Current Party Secretary ═══════════════
    {
        "id": 1, "name": "安伟", "gender": "男", "ethnicity": "汉族",
        "birth": "1966-05", "birthplace": "河南镇平",
        "education": "河南大学政治系本科、兰州大学世界近现代史硕士",
        "party_join": "1988-05", "work_start": "1991-06",
        "current_post": "河南省委常委、郑州市委书记",
        "current_org": "中共郑州市委员会",
        "source": "https://zh.wikipedia.org/wiki/%E5%AE%89%E4%BC%9F_(%E6%94%BF%E6%B2%BB%E4%BA%BA%E7%89%A9)"
    },
    # ═══════════════ Current Mayor ═══════════════
    {
        "id": 2, "name": "庄建球", "gender": "男", "ethnicity": "汉族",
        "birth": "1971-11", "birthplace": "湖南南县",
        "education": "中南工学院管理系会计专业本科、清华大学公共管理硕士（MPA）、北京航空航天大学管理科学与工程博士",
        "party_join": "1993-05", "work_start": "1995-06",
        "current_post": "郑州市委副书记、市长",
        "current_org": "郑州市人民政府",
        "source": "https://baike.baidu.com/item/%E5%BA%84%E5%BB%BA%E7%90%83/8004662"
    },
    # ═══════════════ Vice Mayors (市政府领导班子) ═══════════════
    {
        "id": 3, "name": "陈宏伟", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "郑州市委常委、副市长",
        "current_org": "郑州市人民政府",
        "source": "https://public.zhengzhou.gov.cn/?a=platform&k=law&t=org&i=02&d=4"
    },
    {
        "id": 4, "name": "石秀田", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "郑州市副市长、市公安局局长",
        "current_org": "郑州市人民政府",
        "source": "https://public.zhengzhou.gov.cn/?a=platform&k=law&t=org&i=02&d=4"
    },
    {
        "id": 5, "name": "陈红民", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "郑州市副市长",
        "current_org": "郑州市人民政府",
        "source": "https://public.zhengzhou.gov.cn/?a=platform&k=law&t=org&i=02&d=4"
    },
    {
        "id": 6, "name": "王滔", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "郑州市副市长",
        "current_org": "郑州市人民政府",
        "source": "https://public.zhengzhou.gov.cn/?a=platform&k=law&t=org&i=02&d=4"
    },
    {
        "id": 7, "name": "马志峰", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "郑州市副市长",
        "current_org": "郑州市人民政府",
        "source": "https://public.zhengzhou.gov.cn/?a=platform&k=law&t=org&i=02&d=4"
    },
    {
        "id": 8, "name": "李凤芝", "gender": "女", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "郑州市副市长",
        "current_org": "郑州市人民政府",
        "source": "https://public.zhengzhou.gov.cn/?a=platform&k=law&t=org&i=02&d=4"
    },
    {
        "id": 9, "name": "张艳敏", "gender": "女", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "郑州市副市长",
        "current_org": "郑州市人民政府",
        "source": "https://public.zhengzhou.gov.cn/?a=platform&k=law&t=org&i=02&d=4"
    },
    {
        "id": 10, "name": "杨金军", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "",
        "education": "",
        "party_join": "", "work_start": "",
        "current_post": "郑州市政府秘书长",
        "current_org": "郑州市人民政府",
        "source": "https://public.zhengzhou.gov.cn/?a=platform&k=law&t=org&i=02&d=4"
    },
    # ═══════════════ Predecessors — Party Secretary ═══════════════
    {
        "id": 11, "name": "徐立毅", "gender": "男", "ethnicity": "汉族",
        "birth": "1964-08", "birthplace": "浙江绍兴",
        "education": "浙江工学院（现浙江工业大学）",
        "party_join": "1986-05", "work_start": "1984-08",
        "current_post": "（原郑州市委书记，已因720特大暴雨灾害被处分）",
        "current_org": "",
        "source": "https://zh.wikipedia.org/wiki/%E5%BE%90%E7%AB%8B%E6%AF%85"
    },
    # ═══════════════ Predecessors — Mayor ═══════════════
    {
        "id": 12, "name": "何雄", "gender": "男", "ethnicity": "汉族",
        "birth": "1969-03", "birthplace": "湖北安陆",
        "education": "浙江大学工程热物理专业",
        "party_join": "1998-12", "work_start": "1990-07",
        "current_post": "（原郑州市市长，2025年卸任）",
        "current_org": "",
        "source": "https://zh.wikipedia.org/wiki/%E4%BD%95%E9%9B%84"
    },
    # ═══════════════ Previous predecessors — Mayor ═══════════════
    {
        "id": 13, "name": "侯红", "gender": "女", "ethnicity": "汉族",
        "birth": "1967-01", "birthplace": "河南社旗",
        "education": "河南大学区域经济学硕士",
        "party_join": "1989-09", "work_start": "1987-08",
        "current_post": "河南省卫健委党组副书记、副主任（原郑州市市长）",
        "current_org": "河南省卫生健康委员会",
        "source": "https://zh.wikipedia.org/wiki/%E4%BE%AF%E7%BA%A2"
    },
    # ═══════════════ Key historical leaders ═══════════════
    {
        "id": 14, "name": "马懿", "gender": "男", "ethnicity": "回族",
        "birth": "1959-04", "birthplace": "河北安国",
        "education": "大学学历",
        "party_join": "1983-10", "work_start": "1976-12",
        "current_post": "（原郑州市委书记、河南省人大常委会副主任，已退休）",
        "current_org": "",
        "source": "https://zh.wikipedia.org/wiki/%E9%A9%AC%E6%87%BF_(%E6%94%BF%E6%B2%BB%E4%BA%BA%E7%89%A9)"
    },
]

organizations = [
    # ── Zhengzhou city core ──
    {"id": 1, "name": "中共郑州市委员会", "type": "党委", "level": "副省级", "parent": "中共河南省委员会", "location": "河南省郑州市"},
    {"id": 2, "name": "郑州市人民政府", "type": "政府", "level": "副省级", "parent": "河南省人民政府", "location": "河南省郑州市"},
    {"id": 3, "name": "郑州市人大常委会", "type": "人大", "level": "副省级", "parent": "", "location": "河南省郑州市"},
    {"id": 4, "name": "政协郑州市委员会", "type": "政协", "level": "副省级", "parent": "", "location": "河南省郑州市"},
    {"id": 5, "name": "中共郑州市纪律检查委员会", "type": "党委", "level": "副省级", "parent": "中共郑州市委员会", "location": "河南省郑州市"},
    {"id": 6, "name": "郑州市公安局", "type": "政府", "level": "副省级", "parent": "郑州市人民政府", "location": "河南省郑州市"},

    # ── Central/Provincial orgs 庄建球 worked at ──
    {"id": 7, "name": "中国核工业总公司", "type": "事业单位", "level": "国家级", "parent": "", "location": "北京市"},
    {"id": 8, "name": "国防科工委", "type": "政府", "level": "国家级", "parent": "国务院", "location": "北京市"},
    {"id": 9, "name": "中央纪律检查委员会（驻国防科工委纪检组）", "type": "党委", "level": "国家级", "parent": "", "location": "北京市"},
    {"id": 10, "name": "中央纪委监察部", "type": "党委", "level": "国家级", "parent": "", "location": "北京市"},
    {"id": 11, "name": "中央纪委国家监委", "type": "党委", "level": "国家级", "parent": "", "location": "北京市"},
    {"id": 12, "name": "中共河南省委统战部", "type": "党委", "level": "省级", "parent": "中共河南省委员会", "location": "河南省郑州市"},
    {"id": 13, "name": "河南省工商联", "type": "群团", "level": "省级", "parent": "", "location": "河南省郑州市"},
    {"id": 14, "name": "济源产城融合示范区", "type": "政府", "level": "地级", "parent": "河南省人民政府", "location": "河南省济源市"},
    {"id": 15, "name": "中共济源市委", "type": "党委", "level": "地级", "parent": "中共河南省委员会", "location": "河南省济源市"},
    {"id": 16, "name": "济源市人民政府", "type": "政府", "level": "地级", "parent": "河南省人民政府", "location": "河南省济源市"},
    {"id": 17, "name": "济源市人大常委会", "type": "人大", "level": "地级", "parent": "", "location": "河南省济源市"},

    # ── Henan province orgs (shared) ──
    {"id": 18, "name": "中共河南省委员会", "type": "党委", "level": "省级", "parent": "", "location": "河南省郑州市"},
    {"id": 19, "name": "河南省人民政府", "type": "政府", "level": "省级", "parent": "", "location": "河南省郑州市"},
    {"id": 20, "name": "河南省卫生健康委员会", "type": "政府", "level": "省级", "parent": "河南省人民政府", "location": "河南省郑州市"},
    {"id": 21, "name": "河南省人大常委会", "type": "人大", "level": "省级", "parent": "", "location": "河南省郑州市"},
    {"id": 22, "name": "西藏拉萨市农业开发项目管理局", "type": "政府", "level": "地级", "parent": "", "location": "西藏自治区拉萨市"},
]

positions = [
    # ── 安伟 ──
    {"id": 1, "person_id": 1, "org_id": 1, "title": "河南省委常委、郑州市委书记", "start": "2022-01", "end": "", "rank": "副部级", "note": "2022年1月任郑州市委书记"},
    {"id": 2, "person_id": 1, "org_id": 18, "title": "河南省委常委", "start": "2021-10", "end": "", "rank": "副部级", "note": "当选第十一届省委常委"},
    {"id": 3, "person_id": 1, "org_id": 18, "title": "河南省委宣传部部长", "start": "2021-07", "end": "2021-10", "rank": "副部级", "note": "短暂担任省委宣传部长"},
    {"id": 4, "person_id": 1, "org_id": 18, "title": "河南省委组织部副部长（主持工作）", "start": "2020-05", "end": "2021-07", "rank": "正厅级", "note": "主持省委组织部日常工作"},
    {"id": 5, "person_id": 1, "org_id": 12, "title": "河南省委统战部副部长、省侨联主席", "start": "2018-11", "end": "2020-05", "rank": "正厅级", "note": ""},
    {"id": 6, "person_id": 1, "org_id": 12, "title": "河南省委台湾工作办公室主任", "start": "2017-12", "end": "2018-11", "rank": "正厅级", "note": ""},
    {"id": 7, "person_id": 1, "org_id": 21, "title": "河南省人大常委会副秘书长", "start": "2015-11", "end": "2017-12", "rank": "正厅级", "note": ""},
    {"id": 8, "person_id": 1, "org_id": 21, "title": "河南省人大常委会办公厅研究室主任", "start": "2013-06", "end": "2015-11", "rank": "副厅级", "note": ""},
    {"id": 9, "person_id": 1, "org_id": 21, "title": "河南省人大常委会办公厅副主任", "start": "2009-06", "end": "2013-06", "rank": "副厅级", "note": ""},
    {"id": 10, "person_id": 1, "org_id": 18, "title": "河南省委政策研究室副主任", "start": "2007-11", "end": "2009-06", "rank": "副厅级", "note": ""},
    {"id": 11, "person_id": 1, "org_id": 18, "title": "河南省委政策研究室综合处处长", "start": "2005-12", "end": "2007-11", "rank": "正处级", "note": ""},

    # ── 庄建球 ──
    {"id": 12, "person_id": 2, "org_id": 2, "title": "郑州市委副书记、市长", "start": "2025-02", "end": "", "rank": "副部级", "note": "2025.02任代市长，2025.07.17正式当选市长"},
    {"id": 13, "person_id": 2, "org_id": 15, "title": "济源市委书记", "start": "2023-04", "end": "2025-02", "rank": "正厅级", "note": "2023.05起兼任市人武部党委第一书记"},
    {"id": 14, "person_id": 2, "org_id": 14, "title": "济源产城融合示范区党工委书记", "start": "2023-04", "end": "2025-02", "rank": "正厅级", "note": "2023.05-2023.06兼管委会主任"},
    {"id": 15, "person_id": 2, "org_id": 17, "title": "济源市人大常委会主任", "start": "2023-08", "end": "2024-04", "rank": "正厅级", "note": "兼市人大常委会主任"},
    {"id": 16, "person_id": 2, "org_id": 15, "title": "济源市委副书记、市长", "start": "2021-09", "end": "2023-04", "rank": "正厅级", "note": "2021.09正式当选市长"},
    {"id": 17, "person_id": 2, "org_id": 14, "title": "济源产城融合示范区管委会主任", "start": "2021-06", "end": "2023-06", "rank": "正厅级", "note": "2021.06任副书记、代市长；2021.09正式任市长/管委会主任"},
    {"id": 18, "person_id": 2, "org_id": 12, "title": "河南省委统战部副部长", "start": "2020-10", "end": "2021-06", "rank": "正厅级", "note": ""},
    {"id": 19, "person_id": 2, "org_id": 13, "title": "河南省工商联党组书记", "start": "2020-10", "end": "2021-06", "rank": "正厅级", "note": "兼省工商联党组书记，省委统战部副部长"},
    {"id": 20, "person_id": 2, "org_id": 11, "title": "中央纪委国家监委第十六审查调查室主任", "start": "2018-05", "end": "2020-10", "rank": "正局级", "note": "监察体制改革后新设审查调查室"},
    {"id": 21, "person_id": 2, "org_id": 10, "title": "中央纪委第三纪检监察室主任", "start": "2017-07", "end": "2018-05", "rank": "正局级", "note": ""},
    {"id": 22, "person_id": 2, "org_id": 10, "title": "中央纪委第一纪检监察室副主任（正局级）", "start": "2016-01", "end": "2017-07", "rank": "正局级", "note": "正局级纪律检查员、监察专员兼副主任"},
    {"id": 23, "person_id": 2, "org_id": 10, "title": "中央纪委第一纪检监察室副主任", "start": "2014-12", "end": "2016-01", "rank": "副局级", "note": ""},
    {"id": 24, "person_id": 2, "org_id": 9, "title": "中央纪委监察部驻工信部纪检组监察局副局长", "start": "2010-07", "end": "2014-12", "rank": "副局级", "note": "工信部由国防科工委等部委合并而成"},
    {"id": 25, "person_id": 2, "org_id": 9, "title": "中央纪委监察部驻国防科工委纪检组监察局二室正处长级主任", "start": "2007-12", "end": "2008-07", "rank": "正处级", "note": ""},
    {"id": 26, "person_id": 2, "org_id": 9, "title": "中央纪委监察部驻国防科工委纪检组监察局二室副主任（正处长级）", "start": "2005-10", "end": "2007-12", "rank": "正处级", "note": ""},
    {"id": 27, "person_id": 2, "org_id": 9, "title": "中央纪委监察部驻国防科工委纪检组监察局二室副处级纪律检查员", "start": "2002-07", "end": "2005-10", "rank": "副处级", "note": ""},
    {"id": 28, "person_id": 2, "org_id": 9, "title": "中央纪委监察部驻国防科工委纪检组监察局二室主任科员", "start": "2001-02", "end": "2002-07", "rank": "正科级", "note": ""},
    {"id": 29, "person_id": 2, "org_id": 8, "title": "国防科工委办公厅财务处主任科员", "start": "2000-12", "end": "2001-02", "rank": "正科级", "note": ""},
    {"id": 30, "person_id": 2, "org_id": 8, "title": "国防科工委办公厅财务处副主任科员", "start": "1998-12", "end": "2000-12", "rank": "副科级", "note": ""},
    {"id": 31, "person_id": 2, "org_id": 7, "title": "中国核工业总公司审计局企业审计处干部", "start": "1995-06", "end": "1998-12", "rank": "", "note": "其间1995.08-1998.07在西藏拉萨基层锻炼"},
    {"id": 32, "person_id": 2, "org_id": 22, "title": "西藏拉萨市农业开发项目管理局（基层锻炼）", "start": "1995-08", "end": "1998-07", "rank": "", "note": "中国核工业总公司派驻基层锻炼"},

    # ── 陈宏伟 ──
    {"id": 33, "person_id": 3, "org_id": 2, "title": "郑州市委常委、副市长", "start": "", "end": "", "rank": "副厅级", "note": "现任"},
    # ── 石秀田 ──
    {"id": 34, "person_id": 4, "org_id": 2, "title": "郑州市副市长、市公安局局长", "start": "", "end": "", "rank": "副厅级", "note": "现任"},
    # ── 陈红民 ──
    {"id": 35, "person_id": 5, "org_id": 2, "title": "郑州市副市长", "start": "", "end": "", "rank": "副厅级", "note": "现任"},
    # ── 王滔 ──
    {"id": 36, "person_id": 6, "org_id": 2, "title": "郑州市副市长", "start": "", "end": "", "rank": "副厅级", "note": "现任"},
    # ── 马志峰 ──
    {"id": 37, "person_id": 7, "org_id": 2, "title": "郑州市副市长", "start": "", "end": "", "rank": "副厅级", "note": "现任"},
    # ── 李凤芝 ──
    {"id": 38, "person_id": 8, "org_id": 2, "title": "郑州市副市长", "start": "", "end": "", "rank": "副厅级", "note": "现任"},
    # ── 张艳敏 ──
    {"id": 39, "person_id": 9, "org_id": 2, "title": "郑州市副市长", "start": "", "end": "", "rank": "副厅级", "note": "现任"},
    # ── 杨金军 ──
    {"id": 40, "person_id": 10, "org_id": 2, "title": "郑州市政府秘书长", "start": "", "end": "", "rank": "正处级", "note": "现任"},

    # ── Predecessors — Party Secretary ──
    {"id": 41, "person_id": 11, "org_id": 1, "title": "郑州市委书记", "start": "2019-06", "end": "2021-01", "rank": "副部级", "note": "因720特大暴雨灾害被党内严重警告、政务降级处分，调离"},
    {"id": 42, "person_id": 11, "org_id": 2, "title": "郑州市市长", "start": "2017-01", "end": "2019-06", "rank": "副部级", "note": "2017年1月任郑州市长"},
    {"id": 43, "person_id": 14, "org_id": 1, "title": "郑州市委书记", "start": "2016-05", "end": "2019-06", "rank": "副部级", "note": ""},
    {"id": 44, "person_id": 14, "org_id": 2, "title": "郑州市市长", "start": "2011-12", "end": "2016-05", "rank": "副部级", "note": "约4年5个月"},

    # ── Predecessors — Mayor ──
    {"id": 45, "person_id": 12, "org_id": 2, "title": "郑州市市长", "start": "2022-01", "end": "2025-02", "rank": "副部级", "note": "2022.01任代市长，后当选市长；庄建球接任"},
    {"id": 46, "person_id": 13, "org_id": 2, "title": "郑州市市长", "start": "2021-01", "end": "2021-06", "rank": "副部级", "note": "约5个月，因720特大暴雨灾害被免职"},
    {"id": 47, "person_id": 13, "org_id": 20, "title": "河南省卫健委党组副书记、副主任", "start": "2022", "end": "", "rank": "正厅级", "note": "事故处分后调任"},
]

relationships = [
    # ── 安伟 ↔ 庄建球（党政一把手搭档）──
    {"id": 1, "person_a": 1, "person_b": 2, "type": "党政搭档",
     "context": "安伟（市委书记）与庄建球（市长）为郑州市党政一把手搭档",
     "overlap_org": "郑州市", "overlap_period": "2025-02至今"},
    # ── 庄建球前任/继任 ──
    {"id": 2, "person_a": 12, "person_b": 2, "type": "前后任",
     "context": "何雄（2022-2025.02郑州市长）→ 庄建球（2025.02接任）",
     "overlap_org": "郑州市人民政府", "overlap_period": "不重叠（前后任）"},
    {"id": 3, "person_a": 13, "person_b": 12, "type": "前后任",
     "context": "侯红（2021.01-2021.06郑州市长）→ 何雄（2022.01接任）",
     "overlap_org": "郑州市人民政府", "overlap_period": "不重叠（前后任）"},
    # ── 市委书纪前任/继任 ──
    {"id": 4, "person_a": 11, "person_b": 1, "type": "前后任",
     "context": "徐立毅（2019-2021郑州市委书记，因720被处分）→ 安伟（2022.01接任）",
     "overlap_org": "中共郑州市委员会", "overlap_period": "不重叠（前后任）"},
    {"id": 5, "person_a": 14, "person_b": 11, "type": "前后任",
     "context": "马懿（2016-2019郑州市委书记）→ 徐立毅（2019.06接任）",
     "overlap_org": "中共郑州市委员会", "overlap_period": "不重叠（前后任）"},
    # ── 安伟与省委核心班子 ──
    {"id": 6, "person_a": 1, "person_b": 0, "type": "省委班子",
     "context": "安伟（省委常委、郑州市委书记）在省委常委会中与其他常委共事",
     "overlap_org": "中共河南省委员会", "overlap_period": "2021-10至今"},
    # ── 党政班子成员关系 ──
    {"id": 7, "person_a": 2, "person_b": 3, "type": "上下级",
     "context": "庄建球（市长）与陈宏伟（市委常委、副市长）为政府班子搭档",
     "overlap_org": "郑州市人民政府", "overlap_period": ""},
    {"id": 8, "person_a": 2, "person_b": 4, "type": "上下级",
     "context": "庄建球（市长）与石秀田（副市长、公安局长）为政府班子搭档",
     "overlap_org": "郑州市人民政府", "overlap_period": ""},
    {"id": 9, "person_a": 2, "person_b": 5, "type": "上下级",
     "context": "庄建球（市长）与陈红民（副市长）为政府班子搭档",
     "overlap_org": "郑州市人民政府", "overlap_period": ""},
    {"id": 10, "person_a": 2, "person_b": 6, "type": "上下级",
     "context": "庄建球（市长）与王滔（副市长）为政府班子搭档",
     "overlap_org": "郑州市人民政府", "overlap_period": ""},
    {"id": 11, "person_a": 2, "person_b": 7, "type": "上下级",
     "context": "庄建球（市长）与马志峰（副市长）为政府班子搭档",
     "overlap_org": "郑州市人民政府", "overlap_period": ""},
    {"id": 12, "person_a": 2, "person_b": 8, "type": "上下级",
     "context": "庄建球（市长）与李凤芝（副市长）为政府班子搭档",
     "overlap_org": "郑州市人民政府", "overlap_period": ""},
    {"id": 13, "person_a": 2, "person_b": 9, "type": "上下级",
     "context": "庄建球（市长）与张艳敏（副市长）为政府班子搭档",
     "overlap_org": "郑州市人民政府", "overlap_period": ""},
    {"id": 14, "person_a": 2, "person_b": 10, "type": "上下级",
     "context": "庄建球（市长）与杨金军（秘书长）为政府班子搭档",
     "overlap_org": "郑州市人民政府", "overlap_period": ""},
]

# ── BUILD SQLITE ────────────────────────────────────────────────────────────
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.executescript("""
CREATE TABLE IF NOT EXISTS persons (id INTEGER PRIMARY KEY,name TEXT,gender TEXT,ethnicity TEXT,birth TEXT,birthplace TEXT,education TEXT,party_join TEXT,work_start TEXT,current_post TEXT,current_org TEXT,source TEXT);
CREATE TABLE IF NOT EXISTS organizations (id INTEGER PRIMARY KEY,name TEXT,type TEXT,level TEXT,parent TEXT,location TEXT);
CREATE TABLE IF NOT EXISTS positions (id INTEGER PRIMARY KEY,person_id INTEGER,org_id INTEGER,title TEXT,start TEXT,"end" TEXT,rank TEXT,note TEXT,FOREIGN KEY(person_id) REFERENCES persons(id),FOREIGN KEY(org_id) REFERENCES organizations(id));
CREATE TABLE IF NOT EXISTS relationships (id INTEGER PRIMARY KEY,person_a INTEGER,person_b INTEGER,type TEXT,context TEXT,overlap_org TEXT,overlap_period TEXT,FOREIGN KEY(person_a) REFERENCES persons(id),FOREIGN KEY(person_b) REFERENCES persons(id));
CREATE INDEX IF NOT EXISTS idx_pos_p ON positions(person_id);
CREATE INDEX IF NOT EXISTS idx_pos_o ON positions(org_id);
CREATE INDEX IF NOT EXISTS idx_rel_a ON relationships(person_a);
CREATE INDEX IF NOT EXISTS idx_rel_b ON relationships(person_b);
""")
for p in persons:
    c.execute("INSERT OR REPLACE INTO persons VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",
              (p["id"],p["name"],p["gender"],p["ethnicity"],p["birth"],p["birthplace"],p["education"],p["party_join"],p["work_start"],p["current_post"],p["current_org"],p["source"]))
for o in organizations:
    c.execute("INSERT OR REPLACE INTO organizations VALUES(?,?,?,?,?,?)",
              (o["id"],o["name"],o["type"],o["level"],o["parent"],o["location"]))
for pos in positions:
    c.execute("INSERT OR REPLACE INTO positions VALUES(?,?,?,?,?,?,?,?)",
              (pos["id"],pos["person_id"],pos["org_id"],pos["title"],pos["start"],pos["end"],pos["rank"],pos["note"]))
for r in relationships:
    c.execute("INSERT OR REPLACE INTO relationships VALUES(?,?,?,?,?,?,?)",
              (r["id"],r["person_a"],r["person_b"],r["type"],r["context"],r["overlap_org"],r["overlap_period"]))
conn.commit()

counts = {}
for t in ["persons","organizations","positions","relationships"]:
    counts[t] = c.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
conn.close()
print(f"SQLite DB: {DB_PATH}")
for t,n in counts.items():
    print(f"  {t}: {n} records")

# ── BUILD GEXF ──────────────────────────────────────────────────────────────
os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)

def esc(s):
    if s is None: return ""
    return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

def pcolor(post):
    if "市委书记" in post:
        return "220,50,50"
    if "市长" in post:
        return "50,100,220"
    if "副市长" in post or "秘书长" in post:
        return "80,140,240"
    if "纪委书记" in post or "监委" in post:
        return "230,150,0"
    return "120,120,120"

def ocolor(otype):
    return {"党委":"255,200,200","政府":"200,200,255","人大":"200,220,255","政协":"220,200,255",
            "事业单位":"210,210,210","群团":"255,220,255"}.get(otype,"200,200,200")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
lines.append('    <creator>OpenCode Research Agent</creator>')
lines.append('    <description>郑州市（副省级城市）领导班子工作关系网络 — 2026年7月24日生成</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')
lines.append('    <attributes class="node">')
for aid,atitle in [("0","type"),("1","birth"),("2","birthplace"),("3","current_post"),("4","entity_type"),("5","level")]:
    lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
for aid,atitle in [("0","type"),("1","start"),("2","end"),("3","context")]:
    lines.append(f'      <attribute id="{aid}" title="{atitle}" type="string"/>')
lines.append('    </attributes>')
lines.append('    <nodes>')
for p in persons:
    c = pcolor(p.get("current_post",""))
    sz = "20.0" if any(k in p.get("current_post","") for k in ["市委书记","市长","省委常委"]) else "12.0"
    lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
    lines.append('        <attvalues>')
    for f,v in [("0","person"),("1",p.get("birth","")),("2",p.get("birthplace","")),("3",p.get("current_post","")),("4","person"),("5","")]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="{sz}"/>')
    lines.append('      </node>')
for o in organizations:
    c = ocolor(o.get("type",""))
    lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
    lines.append('        <attvalues>')
    for f,v in [("0","organization"),("1",""),("2",o.get("location","")),("3",""),("4","organization"),("5",o.get("level",""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append('      </node>')
lines.append('    </nodes>')
lines.append('    <edges>')
eid = 0
for pos in positions:
    eid += 1
    lines.append(f'      <edge id="{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
    lines.append('        <attvalues>')
    for f,v in [("0","worked_at"),("1",pos.get("start","")),("2",pos.get("end","")),("3",pos.get("note",""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
for r in relationships:
    eid += 1
    ov = r.get("overlap_period","")
    ov_s = ov.split("至今")[0] if "至今" in ov else ov
    lines.append(f'      <edge id="{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
    lines.append('        <attvalues>')
    for f,v in [("0",r["type"]),("1",ov_s),("2",""),("3",r.get("context",""))]:
        lines.append(f'          <attvalue for="{f}" value="{esc(v)}"/>')
    lines.append('        </attvalues>')
    lines.append('      </edge>')
lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

tn = len(persons) + len(organizations)
te = len(positions) + len(relationships)
print(f"\nGEXF: {GEXF_PATH}")
print(f"  Nodes: {len(persons)} persons + {len(organizations)} orgs = {tn} total")
print(f"  Edges: {len(positions)} worked_at + {len(relationships)} relationships = {te} total")
print("\nDone!")
