#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 敦化市, 延边朝鲜族自治州, 吉林省.

Investigation date: 2026-08-06
Task ID: jilin_敦化市
Primary sources:
  - Dunhua Municipal Government Website (www.dunhua.gov.cn) — official leadership pages
  - Dunhua gov site internal search (111.26.49.117:8082/was5/web/search)
  - 敦化市融媒体中心 news via gov site
"""

import os
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
SLUG = "敦化市"
AS_OF = datetime.now().strftime("%Y-%m-%d")

DB_PATH = os.path.join(BASE, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(BASE, f"{SLUG}_network.gexf")

# ── Persons ──────────────────────────────────────────────────────────────────
# confidence legend: confirmed (official gov page/notice), plausible (media/ency with partial corroboration), unverified

persons = [
    # ═══ Core — 市委书记 / 市长 ═══
    # 唐振生 — 市委书记 (confirmed; formerly 市委副书记、市长)
    {"id": 1, "name": "唐振生", "gender": "男", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "中共党员", "work_start": "",
     "current_post": "市委书记", "current_org": "中共敦化市委员会",
     "source": "敦化市政府官网领导活动 t20251010_556810.html",
     "notes": "曾任市委副书记、市长(2019-2024)，后转任市委书记(2024/2025-今)。confirmed via 2026-04/07 会议调研。",
     "confidence": "confirmed"},

    # 2 苏志远 — 市长 (confirmed)
    {"id": 2, "name": "苏志远", "gender": "男", "ethnicity": "汉族",
     "birth": "待查", "birthplace": "待查", "education": "待查",
     "party_join": "中共党员", "work_start": "",
     "current_post": "市委副书记、市长", "current_org": "敦化市人民政府",
     "source": "敦化市人民政府官网 市长 sz_33049 + 政府工作报告(2025-01)",
     "notes": "晋升路径: 市委常委/副市长(2022)→市委副书记/副市长/代市长(2024-12)→市长(2025-01-今)。held 市政府全面工作。",
     "confidence": "confirmed"},

    # ═══ 市委班子 ═══
    # 3 常仁龙 — 市委副书记
    {"id": 3, "name": "常仁龙", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "市委副书记", "current_org": "中共敦化市委员会",
     "source": "敦化市人民政府官网 农村人居环境整治会议(2026-04-14)、社区建设调研(2025-11)",
     "notes": "confirmed 市委副书记 2025-11 至 2026-04。",
     "confidence": "confirmed"},

    # 4 丁峰 — 市委常委、组织部部长
    {"id": 4, "name": "丁峰", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "市委常委、组织部部长", "current_org": "中共敦化市委组织部",
     "source": "敦化市人大常委会调研新闻(2025-11-28)、社区建设调研(2025-11-10)",
     "notes": "confirmed 2025-11。",
     "confidence": "confirmed"},

    # 5 刘国坤 — 市委常委、统战部部长
    {"id": 5, "name": "刘国坤", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "市委常委、统战部部长", "current_org": "中共敦化市委统战部",
     "source": "敦化市人民政府官网 民族团结活动宣讲(2026-06-16)、人居环境会议(2026-04-14)",
     "notes": "也曾以副市长身份出现(2025-12 人大会议列席)。",
     "confidence": "confirmed"},

    # 6 孙红霞 — 市委常委、宣传部部长
    {"id": 6, "name": "孙红霞", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "市委常委、宣传部部长", "current_org": "中共敦化市委宣传部",
     "source": "敦化市人民政府官网(2022-10-10 乡村振兴会议)",
     "notes": "2022年确认任宣传部长；当前任职状态待核。",
     "confidence": "plausible"},

    # 7 范世宏 — 市纪委书记、监委主任
    {"id": 7, "name": "范世宏", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "市纪委书记、监委主任", "current_org": "中共敦化市纪律检查委员会/监委",
     "source": "敦化市人民政府官网 市纪委十六届五次全会(2025-02-12)",
     "notes": "confirmed 2025-02。",
     "confidence": "confirmed"},

    # ═══ 市政府 ═══
    # 8 张庆荣 — 市委常委、常务副市长
    {"id": 8, "name": "张庆荣", "gender": "男", "ethnicity": "汉族",
     "birth": "1976年8月", "birthplace": "", "education": "东北师范大学",
     "party_join": "中共党员", "work_start": "1999年8月",
     "current_post": "市委常委、副市长(常务)", "current_org": "敦化市人民政府",
     "source": "敦化市人民政府官网 我的简历(fsz_12075/zqr)",
     "notes": "简历: 男,汉族,1976-08生,1999-08参加工作,2001-05入党,东北师大毕业。分管财政/发改/项目/应急/政务等。",
     "confidence": "confirmed"},

    # 9 矫健鹰 — 市委常委、副市长
    {"id": 9, "name": "矫健鹰", "gender": "女", "ethnicity": "汉族",
     "birth": "1980年8月", "birthplace": "", "education": "延边大学汉语言文学教育",
     "party_join": "中共党员", "work_start": "2003年9月",
     "current_post": "市委常委、副市长", "current_org": "敦化市人民政府",
     "source": "敦化市人民政府官网我的简历(fsz_12075/fsz)",
     "notes": "简历: 女,汉族,1980-08生,2003-09参加工作,2001-06入党,延边大学。分管交通运输/文化旅游/供销/市场监管/创新创业。",
     "confidence": "confirmed"},

    # 10 王琦 — 副市长、市公安局局长
    {"id": 10, "name": "王琦", "gender": "男", "ethnicity": "汉族",
     "birth": "1972年8月", "birthplace": "", "education": "延边大学法学专业",
     "party_join": "中共党员", "work_start": "1992年7月",
     "current_post": "副市长、市公安局局长", "current_org": "敦化市人民政府/市公安局",
     "source": "敦化市人民政府官网 我的简历(fsz_12075/fsz_12076)",
     "notes": "简历: 男,汉族,1972-08生,1992-07参加工作,1994-05入党,延边大学法学。市政府党组成员。分管公安/司法/信访/退役军人。",
     "confidence": "confirmed"},

    # 11 韩迪 — 副市长
    {"id": 11, "name": "韩迪", "gender": "女", "ethnicity": "汉族",
     "birth": "1977年11月", "birthplace": "", "education": "延边大学师范学院计算机科学",
     "party_join": "中共党员", "work_start": "1999年7月",
     "current_post": "副市长", "current_org": "敦化市人民政府",
     "source": "敦化市人民政府官网我的简历(fsz_12075/lgz_18906)",
     "notes": "简历: 女,汉族,1977-11生,1999-07参加工作,2005-06入党。分管卫生健康/医保/教育/民族宗教。",
     "confidence": "confirmed"},

    # 12 孙晓鹏 — 副市长
    {"id": 12, "name": "孙晓鹏", "gender": "男", "ethnicity": "汉族",
     "birth": "1975年6月", "birthplace": "", "education": "中国人民公安大学公安管理",
     "party_join": "中共党员", "work_start": "1996年8月",
     "current_post": "副市长", "current_org": "敦化市人民政府",
     "source": "敦化市人民政府官网我的简历(fsz_12075/ywy_18908)",
     "notes": "简历: 男,汉族,1975-06生,1996-08参加工作,2000-05入党,公安大学。分管自然资源/城市建设/城市管理/林业/城乡社区。",
     "confidence": "confirmed"},

    # 13 宗志国 — 副市长
    {"id": 13, "name": "宗志国", "gender": "男", "ethnicity": "汉族",
     "birth": "1978年6月", "birthplace": "", "education": "吉林大学",
     "party_join": "中共党员", "work_start": "1999年9月",
     "current_post": "副市长", "current_org": "敦化市人民政府",
     "source": "敦化市人民政府官网我的简历(fsz_12075/zzg)",
     "notes": "简历: 男,汉族,1978-06生,1999-09参加工作,2003-10入党,吉林大学。分管农业农村/乡村振兴/生态环境/水利。",
     "confidence": "confirmed"},

    # 14 杨元祺 — 副市长
    {"id": 14, "name": "杨元祺", "gender": "男", "ethnicity": "汉族",
     "birth": "1984年1月", "birthplace": "", "education": "吉林大学自动化",
     "party_join": "中共党员", "work_start": "2007年6月",
     "current_post": "副市长", "current_org": "敦化市人民政府",
     "source": "敦化市人民政府官网我的简历(fsz_12075/lgz_18911)",
     "notes": "简历: 男,汉族,1984-01生,2007-06参加工作,2008-08入党,吉林大学自动化。分管发改/应急(协助张庆荣)。",
     "confidence": "confirmed"},

    # 15 张晗竹 — 副市长
    {"id": 15, "name": "张晗竹", "gender": "女", "ethnicity": "汉族",
     "birth": "1989年9月", "birthplace": "", "education": "延边大学经济管理学院旅游管理",
     "party_join": "中共党员", "work_start": "2010年10月",
     "current_post": "副市长", "current_org": "敦化市人民政府",
     "source": "敦化市人民政府官网我的简历(fsz_12075/lgz_18907)",
     "notes": "简历: 女,汉族,1989-09生,2010-10参加工作,2014-08入党,延边大学。分管文化旅游/市场监管/协助矫健鹰。",
     "confidence": "confirmed"},

    # 16 杨文一 — 市委常委、副市长
    {"id": 16, "name": "杨文一", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "市委常委、副市长", "current_org": "敦化市人民政府",
     "source": "敦化市人民政府官网(2025-12政策性资金会议、2024-12安委会)",
     "notes": "confirmed 市委常务/副市长 2024-12、2025-12。",
     "confidence": "confirmed"},

    # ═══ 人大 / 政协 ═══
    # 17 孙金刚 — 市人大常委会主任
    {"id": 17, "name": "孙金刚", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "市人大常委会主任", "current_org": "敦化市人大常委会",
     "source": "敦化市人民政府官网(2026-01 人大五次会议、2025-11 调研)",
     "notes": "confirmed. 2025-01 十九届人大四次会议曾报道'孙长春'主持，疑为姓名报道或更替，以2025-06+的孙金刚为准。",
     "confidence": "confirmed"},

    # 18 郑立伟 — 市政协主席
    {"id": 18, "name": "郑立伟", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "市政协主席", "current_org": "政协敦化市委员会",
     "source": "敦化市人民政府官网(2025-06 高考考场、2025-12 项目会议)",
     "notes": "confirmed 2025-06 至 2025-12。",
     "confidence": "confirmed"},

    # ═══ 其他市领导 ═══
    # 19 公海波 — 六鼎山文化旅游区管委会主任
    {"id": 19, "name": "公海波", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "六鼎山文化旅游区管委会主任", "current_org": "六鼎山文化旅游区",
     "source": "敦化市人民政府官网(2025-12 政策性资金会议、2022-10 乡村振兴会议)",
     "notes": "confirmed。",
     "confidence": "confirmed"},

    # 20 娄晓霞 — 副市长 (可能前任)
    {"id": 20, "name": "娄晓霞", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "副市长（前）", "current_org": "敦化市人民政府",
     "source": "敦化市人民政府官网(2025-06 高考考场)",
     "notes": "2025-06 报道为副市长；未列入当前市政府领导页(市政府领导页为8名副市长)，疑已转任/离任。",
     "confidence": "plausible"},

    # ═══ 前任市委书记 (待确认) ═══
    # 21 前任市委书记 — (唐振生接任前的书记)
    {"id": 21, "name": "（前任市委书记·待查)", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "前任市委书记（待查）", "current_org": "中共敦化市委员会",
     "source": "待补充",
     "notes": "唐振生于2019-2022任市长时，市委书记另有其人（约2019-2023）。人选待核（疑为 刘岩智或他人）。",
     "confidence": "unverified"},
]

# ── Organizations ────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共敦化市委员会", "type": "党委", "level": "县处级", "parent": "中共延边州委", "location": "敦化市"},
    {"id": 2, "name": "敦化市人民政府", "type": "政府", "level": "县处级", "parent": "延边州人民政府", "location": "敦化市"},
    {"id": 3, "name": "敦化市人大常委会", "type": "人大", "level": "县处级", "parent": "延边州人大常委会", "location": "敦化市"},
    {"id": 4, "name": "政协敦化市委员会", "type": "政协", "level": "县处级", "parent": "政协延边州委", "location": "敦化市"},
    {"id": 5, "name": "中共敦化市委组织部", "type": "党委", "level": "县处级", "parent": "中共敦化市委员会", "location": "敦化市"},
    {"id": 6, "name": "中共敦化市委宣传部", "type": "党委", "level": "县处级", "parent": "中共敦化市委员会", "location": "敦化市"},
    {"id": 7, "name": "中共敦化市委统战部", "type": "党委", "level": "县处级", "parent": "中共敦化市委员会", "location": "敦化市"},
    {"id": 8, "name": "中共敦化市纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共敦化市委员会", "location": "敦化市"},
    {"id": 9, "name": "敦化市监察委员会", "type": "党委", "level": "县处级", "parent": "中共敦化市委员会", "location": "敦化市"},
    {"id": 10, "name": "敦化市公安局", "type": "政府", "level": "副县处级", "parent": "敦化市人民政府/延边州公安局", "location": "敦化市"},
    {"id": 11, "name": "六鼎山文化旅游区", "type": "政府", "level": "县处级", "parent": "敦化市人民政府", "location": "敦化市"},
    {"id": 12, "name": "中共延边朝鲜族自治州委员会", "type": "党委", "level": "地厅级", "parent": "中共吉林省委", "location": "延边州"},
    {"id": 13, "name": "延边朝鲜族自治州人民政府", "type": "政府", "level": "地厅级", "parent": "吉林省人民政府", "location": "延边州"},
]

# ── Positions ────────────────────────────────────────────────────────────────
positions = [
    # 唐振生
    {"person_id": "p1", "org_id": 1, "title": "市委书记", "start": "2024", "end": "present", "rank": "县处级正职",
     "note": "由市长升任书记(2024/2025) [官方会议记录确认]"},
    {"person_id": "p1", "org_id": 1, "title": "市委副书记", "start": "2019", "end": "2024", "rank": "县处级副职",
     "note": "任职市委副书记兼市长"},
    {"person_id": "p1", "org_id": 2, "title": "市长", "start": "2019", "end": "2024", "rank": "县处级正职",
     "note": "2019-2022年会议记录显示为市委副书记、市长"},

    # 苏志远
    {"person_id": "p2", "org_id": 2, "title": "市长", "start": "2025-01", "end": "present", "rank": "县处级正职",
     "note": "2025-01 任代市长并作政府工作报告，后转正"},
    {"person_id": "p2", "org_id": 1, "title": "市委副书记", "start": "2024-12", "end": "present", "rank": "县处级副职",
     "note": "2024-12 起任市委副书记、副市长、代市长"},
    {"person_id": "p2", "org_id": 2, "title": "副市长", "start": "2022", "end": "2024-12", "rank": "县处级副职",
     "note": "2022 年报道：市委常委、副市长"},

    # 常仁龙
    {"person_id": "p3", "org_id": 1, "title": "市委副书记", "start": "2025", "end": "present", "rank": "县处级副职",
     "note": "confirmed 2025-11 至 2026-04"},

    # 丁峰
    {"person_id": "p4", "org_id": 5, "title": "市委常委、组织部部长", "start": "", "end": "present", "rank": "县处级副职",
     "note": "confirmed 2025-11"},

    # 刘国坤
    {"person_id": "p5", "org_id": 7, "title": "市委常委、统战部部长", "start": "", "end": "present", "rank": "县处级副职",
     "note": "confirmed 2026-06"},

    # 孙红霞
    {"person_id": "p6", "org_id": 6, "title": "市委常委、宣传部部长", "start": "", "end": "present", "rank": "县处级副职",
     "note": "2022年报道任宣传部长；当前状态待核"},

    # 范世宏
    {"person_id": "p7", "org_id": 8, "title": "市纪委书记", "start": "", "end": "present", "rank": "县处级副职",
     "note": "confirmed 2025-02"},
    {"person_id": "p7", "org_id": 9, "title": "市监委主任", "start": "", "end": "present", "rank": "县处级副职",
     "note": "confirmed 2025-02"},

    # 张庆荣
    {"person_id": "p8", "org_id": 2, "title": "市委常委、副市长", "start": "", "end": "present", "rank": "县处级副职",
     "note": "常务副市长，分管财政收支/发改/项目/应急/政务公开等"},

    # 矫健鹰
    {"person_id": "p9", "org_id": 2, "title": "市委常委、副市长", "start": "", "end": "present", "rank": "县处级副职",
     "note": "confirmed 2026"},

    # 王琦
    {"person_id": "p10", "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "县处级副职",
     "note": "市政府党组成员，分管公安/司法/信访/退役军人"},
    {"person_id": "p10", "org_id": 10, "title": "市公安局局长", "start": "", "end": "present", "rank": "副县处级",
     "note": "兼任副市长"},

    # 韩迪
    {"person_id": "p11", "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 孙晓鹏
    {"person_id": "p12", "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 宗志国
    {"person_id": "p13", "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 杨元祺
    {"person_id": "p14", "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 张晗竹
    {"person_id": "p15", "org_id": 2, "title": "副市长", "start": "", "end": "present", "rank": "县处级副职", "note": ""},
    # 杨文一
    {"person_id": "p16", "org_id": 2, "title": "市委常委、副市长", "start": "2024", "end": "present", "rank": "县处级副职",
     "note": "2024-12 及 2025-12 confirmed"},

    # 孙金刚
    {"person_id": "p17", "org_id": 3, "title": "市人大常委会主任", "start": "", "end": "present", "rank": "县处级正职",
     "note": "confirmed 2025-2026"},
    # 郑立伟
    {"person_id": "p18", "org_id": 4, "title": "市政协主席", "start": "", "end": "present", "rank": "县处级正职",
     "note": "confirmed 2025-2026"},
    # 公海波
    {"person_id": "p19", "org_id": 11, "title": "管委会主任", "start": "", "end": "present", "rank": "县处级",
     "note": "六鼎山文化旅游区"},
    # 娄晓霞(前)
    {"person_id": "p20", "org_id": 2, "title": "副市长（前）", "start": "", "end": "2025", "rank": "县处级副职",
     "note": "2025-06 报道仍为副市长，后续未列入现任领导"},
    # 前任市委书记
    {"person_id": "p21", "org_id": 1, "title": "市委书记（前任）", "start": "", "end": "2023", "rank": "县处级正职",
     "note": "待查"},

    # 关联组织任职 (跨组织为关系线索)
    # 唐振生 - 延边上级
    {"person_id": "p1", "org_id": 12, "title": "（延边州委委员）", "start": "", "end": "", "rank": "", "note": "县级市书记通常为州委委员，待核"},
    {"person_id": "p2", "org_id": 13, "title": "（延边州政府层面）", "start": "", "end": "", "rank": "", "note": "市长正常列席州政府活动"},
]

# ── Relationships ────────────────────────────────────────────────────────────
relationships = [
    # 书记 + 市长 (搭档)
    {"person_a": "p1", "person_b": "p2", "type": "党政正职·前后任搭档",
     "context": "唐振生任市委书记、苏志远任市长。苏志远由副市长升任市长，接替唐振生曾任的市长岗位；现为一二把手搭档。",
     "overlap_org": "中共敦化市委/敦化市人民政府", "overlap_period": "2024-至今",
     "confidence": "confirmed"},

    # 唐振生 + 苏志远 (市长期内共事)
    {"person_a": "p1", "person_b": "p2", "type": "前任后任市长",
     "context": "苏志远接替唐振生出任市长（唐升任书记），历史上同在敦化市政府班子。",
     "overlap_org": "敦化市人民政府", "overlap_period": "2022-2024",
     "confidence": "confirmed"},

    # 张庆荣 + 苏志远 (政府正副职)
    {"person_a": "p2", "person_b": "p8", "type": "政府正副职搭档",
     "context": "苏志远(市长)与张庆荣(常务副市长)为政府正副职搭档。",
     "overlap_org": "敦化市人民政府", "overlap_period": "2025-至今",
     "confidence": "confirmed"},

    # 张庆荣 + 王琦 (政府常务与公安)
    {"person_a": "p8", "person_b": "p10", "type": "常委班子共事",
     "context": "张庆荣(市委常委/常务副市长)与王琦(副市长/公安局长)在市委常委会和市政府班子共事。",
     "overlap_org": "中共敦化市委常委会/市政府", "overlap_period": "",
     "confidence": "confirmed"},

    # 唐振生 + 常仁龙 (书记与副书记)
    {"person_a": "p1", "person_b": "p3", "type": "党政协同·书记与副书记",
     "context": "唐振生(市委书记)与常仁龙(市委副书记)在市委班子共事。",
     "overlap_org": "中共敦化市委常委会", "overlap_period": "2025-至今",
     "confidence": "confirmed"},

    # 唐振生 + 丁峰 (书记与组织部长)
    {"person_a": "p1", "person_b": "p4", "type": "书记与组织部长",
     "context": "唐振生(市委书记)与丁峰(市委常委、组织部长)共同开展组织/干部相关工作。",
     "overlap_org": "中共敦化市委", "overlap_period": "2025-至今",
     "confidence": "confirmed"},

    # 唐振生 + 刘国坤
    {"person_a": "p1", "person_b": "p5", "type": "书记与统战部长",
     "context": "市委常委会共事。",
     "overlap_org": "中共敦化市委常委会", "overlap_period": "",
     "confidence": "confirmed"},

    # 苏志远 + 杨文一 (政府班)
    {"person_a": "p2", "person_b": "p16", "type": "政府正副职",
     "context": "苏志远(市长)与杨文一(市委常委/副市长)在政府班子共事。",
     "overlap_org": "敦化市人民政府", "overlap_period": "2024-至今",
     "confidence": "confirmed"},

    # 郑立伟 + 孙金刚 (人大政协)
    {"person_a": "p17", "person_b": "p18", "type": "人大与政协联动",
     "context": "市人大主任与市政协主席同出席多项市级活动。",
     "overlap_org": "敦化市", "overlap_period": "2025-至今",
     "confidence": "confirmed"},

    # 苏志远 + 孙金刚/郑立伟
    {"person_a": "p2", "person_b": "p17", "type": "党政-人大",
     "context": "市长与市人大主任在人大会议、政府报告等场合互动。",
     "overlap_org": "敦化市", "overlap_period": "2025-至今",
     "confidence": "confirmed"},

    # 张庆荣 + 杨元祺 (常务带副职)
    {"person_a": "p8", "person_b": "p14", "type": "正副副市长协办",
     "context": "杨元祺(副市长)分管的发改/应急协助常务副市长张庆荣。",
     "overlap_org": "敦化市人民政府", "overlap_period": "",
     "confidence": "confirmed"},

    # 矫健鹰 + 张晗竹 (正副副市长协办)
    {"person_a": "p9", "person_b": "p15", "type": "正副副市长协办",
     "context": "张晗竹(副市长)分管文化旅游/市场监管协助矫健鹰(市委常委/副市长)。",
     "overlap_org": "敦化市人民政府", "overlap_period": "",
     "confidence": "confirmed"},

    # 王琦 + 孙晓鹏 (政法/公安与城市建设)
    {"person_a": "p10", "person_b": "p12", "type": "政府班子共事",
     "context": "王琦(副市长/公安局长)与孙晓鹏(副市长,公安大学背景)同在政府班子，均有公安系统背景。",
     "overlap_org": "敦化市人民政府", "overlap_period": "",
     "confidence": "plausible"},
]

# ── Build ──────────────────────────────────────────────────────────────────
import sqlite3

def build():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY, name TEXT, gender TEXT, ethnicity TEXT,
            birth TEXT, birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT, source TEXT, notes TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT, parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER, title TEXT, start TEXT, end TEXT,
            rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER, type TEXT, context TEXT,
            overlap_org TEXT, overlap_period TEXT, confidence TEXT DEFAULT 'unverified',
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)
    def pid(s):
        return int(s[1:])

    for p in persons:
        cur.execute(
            "INSERT INTO persons (id, name, gender, ethnicity, birth, birthplace, education, "
            "party_join, work_start, current_post, current_org, source, notes) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (pid("p"+str(p["id"])), p["name"], p.get("gender",""), p.get("ethnicity",""),
             p.get("birth",""), p.get("birthplace",""), p.get("education",""),
             p.get("party_join",""), p.get("work_start",""), p["current_post"],
             p["current_org"], p.get("source",""), p.get("notes",""))
        )
    for o in organizations:
        cur.execute("INSERT INTO organizations (id, name, type, level, parent, location) VALUES (?,?,?,?,?,?)",
                    (o["id"], o["name"], o.get("type",""), o.get("level",""), o.get("parent",""), o.get("location","")))
    for pos in positions:
        cur.execute("INSERT INTO positions (person_id, org_id, title, start, end, rank, note) VALUES (?,?,?,?,?,?,?)",
                    (pid(pos["person_id"]), pos["org_id"], pos["title"], pos.get("start",""),
                     pos.get("end","present"), pos.get("rank",""), pos.get("note","")))
    for r in relationships:
        cur.execute("INSERT INTO relationships (person_a, person_b, type, context, overlap_org, overlap_period, confidence) VALUES (?,?,?,?,?,?,?)",
                    (pid(r["person_a"]), pid(r["person_b"]), r["type"], r.get("context",""),
                     r.get("overlap_org",""), r.get("overlap_period",""), r.get("confidence","unverified")))
    conn.commit()
    conn.close()
    print(f"✅ Database created: {DB_PATH}")

    # ── GEXF ──
    def esc(s):
        if s is None: return ""
        return str(s).replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"',"&quot;")

    def person_color_and_size(post):
        if "市委书记" in post and "前任" not in post:
            return ("255,50,50", 20.0)
        elif "市长" in post and "副" not in post and "前任" not in post:
            return ("50,100,255", 20.0)
        elif "市委副书记" in post:
            return ("50,100,255", 15.0)
        elif "常委" in post and ("组织" in post or "宣传" in post or "统战" in post):
            return ("120,120,120", 13.0)
        elif "常委" in post:
            return ("100,150,255", 13.0)
        elif "纪委书记" in post or "监委" in post:
            return ("255,165,0", 12.0)
        elif "副" in post and "市长" in post:
            return ("100,150,255", 12.0)
        elif "人大" in post:
            return ("200,255,255", 12.0)
        elif "政协" in post:
            return ("255,240,200", 12.0)
        elif "前任" in post or "待查" in post:
            return ("150,150,150", 10.0)
        else:
            return ("100,100,100", 12.0)

    org_colors = {
        "党委": ("255,200,200", 8.0), "政府": ("200,200,255", 8.0),
        "人大": ("200,255,255", 8.0), "政协": ("255,240,200", 8.0),
        "群团": ("255,220,255", 8.0), "乡镇": ("255,255,200", 8.0),
        "事业单位": ("220,220,220", 8.0),
    }

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov Relation Research Agent</creator>')
    lines.append(f'    <description>敦化市领导班子工作关系网络 - {AS_OF}</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <nodes>')
    for p in persons:
        c, sz = person_color_and_size(p["current_post"])
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_post"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    for o in organizations:
        oc, osz = org_colors.get(o["type"], ("200,200,200", 8.0))
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{oc.split(",")[0]}" g="{oc.split(",")[1]}" b="{oc.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{osz}"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')
    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        eid += 1
        pv = int(pos["person_id"][1:])
        lines.append(f'      <edge id="e{eid}" source="p{pv}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    for r in relationships:
        eid += 1
        a = int(r["person_a"][1:]); b = int(r["person_b"][1:])
        lines.append(f'      <edge id="e{eid}" source="p{a}" target="p{b}" label="{esc(r.get("context",""))}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context",""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')
    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"✅ GEXF created: {GEXF_PATH}")
    print(f"\nPersons: {len(persons)}, Orgs: {len(organizations)}, Positions: {len(positions)}, Edges: {eid}")
    print(f"DB: {DB_PATH}\nGEXF: {GEXF_PATH}")

if __name__ == "__main__":
    build()