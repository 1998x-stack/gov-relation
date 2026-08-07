#!/usr/bin/env python3
"""灵武市领导班子关系网络 build script.

任务: ningxia_灵武市 (宁夏回族自治区银川市灵武市, 县级市)
目标: 市委书记 & 市长
数据基准: 截至 2026-08-07
运行: python3 data/tmp/ningxia_灵武市/build_灵武市_data.py
"""

import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from gov_relation.runner import run_build

# ── 目录（暂存区）─────────────────────────────────────────
STAGING = Path(__file__).resolve().parent
DB_PATH = STAGING / "灵武市_network.db"
GEXF_PATH = STAGING / "灵武市_network.gexf"

# ══════════════════════════════════════════════════════════════
# 人员 (persons)
# ══════════════════════════════════════════════════════════════
persons = [
    {
        "id": 1,
        "name": "李伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年8月",
        "birthplace": "宁夏贺兰",
        "education": "大学学历(西北第二民族学院)",
        "party_join": "2004年6月",
        "work_start": "1999年8月",
        "current_post": "灵武市委书记",
        "current_org": "中共灵武市委员会",
        "source": "灵武市政府门户(2025-01-10人武部第一书记任命/2026-02常委会);银川市人大常委会免职名单(2024-12);宁夏日报(2026-02-07自治区人大代表);百科(2004.06入党/1999.08工作)",
    },
    {
        "id": 2,
        "name": "刘磊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年7月",
        "birthplace": "待查",
        "education": "博士研究生(清华大学法学院宪法学与行政法学)",
        "party_join": "中共党员",
        "work_start": "2015年8月",
        "current_post": "灵武市委副书记、市长",
        "current_org": "灵武市人民政府",
        "source": "灵武市政府官网领导之窗(2024/2026);极目新闻(2024-11-07提名市长候选人);腾讯新闻(2024-11)",
    },
    {
        "id": 3,
        "name": "刘国强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中卫市委书记(原银川市委副书记兼灵武市委书记)",
        "current_org": "中共中卫市委员会",
        "source": "澎湃新闻(2024-08);中卫市政府领导干部大会公告(2024-08-03);中国经济网/灵武市政府(2020-12任灵武书记)",
    },
    {
        "id": 4,
        "name": "杨玉龙",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "current_post": "银川市政府副市长、党组成员(原灵武市委副书记、市长)",
        "current_org": "银川市人民政府",
        "source": "银川市政府官网领导分工(2024-11-12);灵武市政府常务会议新闻(2024-10-31)",
    },
    {
        "id": 5,
        "name": "刘斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年3月",
        "birthplace": "待查",
        "education": "研究生学历",
        "current_post": "宁东能源化工基地党工委委员、管委会副主任(原灵武市委书记)",
        "current_org": "宁夏宁东能源化工基地管委会",
        "source": "灵武市政府门户市委领导页(2018,历史任职)",
    },
    {
        "id": 6,
        "name": "陈文宁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967年12月",
        "birthplace": "待查",
        "education": "大学学历",
        "current_post": "灵武市人大常委会党组书记、主任",
        "current_org": "灵武市人大常委会",
        "source": "灵武市政府门户人大领导页;市十八届人大四次会议新闻(2025-01-08)",
    },
    {
        "id": 7,
        "name": "黄文东",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1971年6月",
        "birthplace": "待查",
        "education": "大学学历",
        "current_post": "灵武市政协党组书记、主席",
        "current_org": "政协灵武市委员会",
        "source": "灵武市政府门户政协领导页;银川市政协网站(政协十三届五次会议补选,2026)",
    },
    {
        "id": 8,
        "name": "杨文炯",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "current_post": "原灵武市政协主席(2026年卸任)",
        "current_org": "",
        "source": "银川市政协网站(黄文东接其政协主席, 杨文炯自2016任政协主席)",
    },
    {
        "id": 9,
        "name": "马世龙",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1991年8月",
        "birthplace": "待查",
        "education": "研究生学历",
        "current_post": "灵武市委常委、常务副市长",
        "current_org": "灵武市人民政府",
        "source": "灵武市政府门户政府领导页(2026-05-06)",
    },
    {
        "id": 10,
        "name": "吴伟",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "current_post": "灵武市委常委、市政府副市长",
        "current_org": "灵武市人民政府",
        "source": "灵武市政府官网政府领导页;银川市管干部任前公示(2025,拟进一步使用)",
    },
    {
        "id": 11,
        "name": "李明",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "current_post": "灵武市政府副市长、公安局局长、督察长",
        "current_org": "灵武市公安局",
        "source": "灵武市政府官网政府领导页(2026)",
    },
    {
        "id": 12,
        "name": "孙学福",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "current_post": "灵武市政府党组成员、副市长",
        "current_org": "灵武市人民政府",
        "source": "灵武市政府官网政府领导页;市政府领导班子分工(2024-12,与葛翔AB岗)",
    },
    {
        "id": 13,
        "name": "马莉",
        "gender": "女",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "current_post": "灵武市政府党组成员、副市长",
        "current_org": "灵武市人民政府",
        "source": "灵武市政府官网政府领导页(2025-10-31)",
    },
    {
        "id": 14,
        "name": "葛翔",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "current_post": "灵武市人民政府党组副书记、副市长(常务)",
        "current_org": "灵武市人民政府",
        "source": "灵武市政府领导班子分工通知(2024-12-04)",
    },
    {
        "id": 15,
        "name": "冯哲",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "current_post": "灵武市委常委、市纪委书记、监委主任",
        "current_org": "中共灵武市纪律检查委员会",
        "source": "灵武市纪委五次全会新闻(2025-01-27);中国县域领导信息(2024-03)",
    },
    {
        "id": 16,
        "name": "刘静林",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "current_post": "灵武市委常委、政法委书记",
        "current_org": "中共灵武市委政法委员会",
        "source": "灵武市政府门户市委领导页(2022-03)",
    },
    {
        "id": 17,
        "name": "张耀翔",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "current_post": "灵武市委常委、组织部长",
        "current_org": "中共灵武市委组织部",
        "source": "灵武市政府门户市委领导页(2021-07)",
    },
    {
        "id": 18,
        "name": "徐少辉",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "current_post": "灵武市委常委、崇兴镇党委书记",
        "current_org": "中共灵武市崇兴镇委员会",
        "source": "灵武市政府门户市委领导页(2024-08);灵武市人武部党委第一书记大会(2025-01)",
    },
    {
        "id": 19,
        "name": "归宗库",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "current_post": "灵武市委常委、人武部部长",
        "current_org": "灵武市人民武装部",
        "source": "灵武市政府门户市委领导页(2022-03);中国县域网站信息(2024-03)",
    },
    {
        "id": 20,
        "name": "司应源",
        "gender": "男",
        "ethnicity": "待查",
        "birth": "待查",
        "birthplace": "待查",
        "education": "",
        "current_post": "灵武市委副书记(历史/2020-2021记载)",
        "current_org": "中共灵武市委员会",
        "source": "灵武市政府门户市委领导页(2020-01,历史)",
    },
    {
        "id": 21,
        "name": "何韬",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1989年6月",
        "birthplace": "待查",
        "education": "大学学历",
        "current_post": "灵武市委常委、宣传部部长、统战部部长、市政协党组副书记",
        "current_org": "中共灵武市委宣传部",
        "source": "灵武市政府门户市委领导页;银川市政协网(政协十三届五次会议执行主席)",
    },
]

# ══════════════════════════════════════════════════════════════
# 机构 (organizations)
# ══════════════════════════════════════════════════════════════
organizations = [
    {"id": 1, "name": "中共灵武市委员会", "type": "党委", "level": "县处级", "parent": "中共银川市委员会", "location": "宁夏回族自治区银川市灵武市"},
    {"id": 2, "name": "灵武市人民政府", "type": "政府", "level": "县处级", "parent": "银川市人民政府", "location": "宁夏回族自治区银川市灵武市"},
    {"id": 3, "name": "灵武市人大常委会", "type": "人大", "level": "县处级", "parent": "灵武市", "location": "灵武市"},
    {"id": 4, "name": "政协灵武市委员会", "type": "政协", "level": "县处级", "parent": "灵武市", "location": "灵武市"},
    {"id": 5, "name": "中共灵武市纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共灵武市委员会", "location": "灵武市"},
    {"id": 6, "name": "灵武市公安局", "type": "政府", "level": "县处级", "parent": "灵武市人民政府", "location": "灵武市"},
    {"id": 7, "name": "中共银川市委员会", "type": "党委", "level": "厅局级", "parent": "中共宁夏回族自治区委员会", "location": "宁夏回族自治区银川市"},
    {"id": 8, "name": "银川市人民政府", "type": "政府", "level": "厅局级", "parent": "宁夏回族自治区人民政府", "location": "宁夏回族自治区银川市"},
    {"id": 9, "name": "银川市自然资源局", "type": "政府", "level": "县处级", "parent": "银川市人民政府", "location": "银川市"},
    {"id": 10, "name": "银川高新技术产业开发区", "type": "开发区", "level": "开发区", "parent": "灵武市", "location": "灵武市"},
    {"id": 11, "name": "宁夏宁东能源化工基地管委会", "type": "事业单位", "level": "厅局级", "parent": "宁夏回族自治区", "location": "银川市宁东基地"},
    {"id": 12, "name": "中共中卫市委员会", "type": "党委", "level": "厅局级", "parent": "中共宁夏回族自治区委员会", "location": "宁夏回族自治区中卫市"},
    {"id": 13, "name": "中共贺兰县委员会", "type": "党委", "level": "县处级", "parent": "中共银川市委员会", "location": "银川市贺兰县"},
    {"id": 14, "name": "共青团银川市委员会", "type": "群团", "level": "县处级", "parent": "共青团宁夏回族自治区委员会", "location": "银川市"},
    {"id": 15, "name": "银川市兴庆区人民政府", "type": "政府", "level": "县处级", "parent": "银川市人民政府", "location": "银川市兴庆区"},
    {"id": 16, "name": "银川市发展和改革委员会", "type": "政府", "level": "县处级", "parent": "银川市人民政府", "location": "银川市"},
    {"id": 17, "name": "中共灵武市崇兴镇委员会", "type": "乡镇", "level": "乡科级", "parent": "中共灵武市委员会", "location": "灵武市崇兴镇"},
    {"id": 18, "name": "灵武市人民武装部", "type": "事业单位", "level": "县处级", "parent": "银川警备区", "location": "灵武市"},
    {"id": 19, "name": "中共灵武市委宣传部", "type": "党委", "level": "县处级", "parent": "中共灵武市委员会", "location": "灵武市"},
]

# ══════════════════════════════════════════════════════════════
# 任职 (positions)
# ══════════════════════════════════════════════════════════════
positions = [
    # 李伟 (1)
    {"person_id": 1, "org_id": 1, "title": "灵武市委书记", "start_date": "2024-11", "end_date": "present", "rank": "县处级正职", "note": "约2024年11月起就任;2025-01任市人武部党委第一书记;2026-02仍任(自治区人大代表)"},
    {"person_id": 1, "org_id": 9, "title": "银川市自然资源局党组书记、局长", "start_date": "2022-01", "end_date": "2024-12", "rank": "正处级", "note": "2022-01拟任市直单位正处级;2024-12-30银川市人大常委会免去局长职务"},
    # 刘磊 (2)
    {"person_id": 2, "org_id": 2, "title": "灵武市委副书记、市长", "start_date": "2024-11", "end_date": "present", "rank": "县处级正职", "note": "2024-11-07提名市长候选人;2024-12代市长;2025-01-07当选市长;兼银川高新区党工委副书记/管委会主任"},
    {"person_id": 2, "org_id": 1, "title": "灵武市委副书记、国安办主任、白土岗乡党委书记", "start_date": "2023", "end_date": "2024-11", "rank": "县处级", "note": "任市长候选人前在灵武市委副书记岗位"},
    {"person_id": 2, "org_id": 16, "title": "银川市发展和改革委员会副主任(正处级)", "start_date": "2022-01", "end_date": "2023", "rank": "正处级", "note": "2022-01银川市政府任命为发改委副主任"},
    {"person_id": 2, "org_id": 15, "title": "银川市兴庆区人民政府副区长", "start_date": "2020", "end_date": "2022-01", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 14, "title": "共青团银川市委副书记", "start_date": "2017", "end_date": "2020", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 13, "title": "共青团贺兰县委书记/习岗镇主任科员", "start_date": "2015", "end_date": "2017", "rank": "正科级", "note": "2015-08参加工作,起步于贺兰县"},
    # 刘国强 (3)
    {"person_id": 3, "org_id": 12, "title": "中卫市委书记", "start_date": "2024-08", "end_date": "present", "rank": "厅局级正职", "note": "2024-07公示拟任地级市书记,2024-08-03中卫干部大会宣布"},
    {"person_id": 3, "org_id": 1, "title": "灵武市委书记(银川市委副书记兼任)", "start_date": "2020-12", "end_date": "2024-08", "rank": "厅局级(挂县处级正职)", "note": "银川市委副书记兼任灵武市委书记;2024-07离任"},
    # 杨玉龙 (4)
    {"person_id": 4, "org_id": 8, "title": "银川市政府副市长、党组成员", "start_date": "2024-11", "end_date": "present", "rank": "厅局级副职", "note": "2024-11调任"},
    {"person_id": 4, "org_id": 2, "title": "灵武市委副书记、市长", "start_date": "2021", "end_date": "2024-11", "rank": "县处级正职", "note": "兼银川高新区党工委书记、宁东基地管委会副主任"},
    # 刘斌 (5)
    {"person_id": 5, "org_id": 11, "title": "宁东能源化工基地管委会副主任", "start_date": "2018", "end_date": "present", "rank": "厅局级", "note": "兼灵武市委书记(历史)"},
    {"person_id": 5, "org_id": 1, "title": "灵武市委书记", "start_date": "2018", "end_date": "2020-12", "rank": "县处级正职", "note": "任内兼宁东基地管委会副主任"},
    # 陈文宁 (6)
    {"person_id": 6, "org_id": 3, "title": "灵武市人大常委会党组书记、主任", "start_date": "2021", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 黄文东 (7)
    {"person_id": 7, "org_id": 4, "title": "灵武市政协党组书记、主席", "start_date": "2026", "end_date": "present", "rank": "县处级正职", "note": "政协十三届五次会议补选"},
    # 杨文炯 (8)
    {"person_id": 8, "org_id": 4, "title": "灵武市政协主席", "start_date": "2016", "end_date": "2026-05", "rank": "县处级正职", "note": "2016年起任,2026年卸任"},
    # 马世龙 (9)
    {"person_id": 9, "org_id": 2, "title": "灵武市委常委、常务副市长", "start_date": "2026-05", "end_date": "present", "rank": "副处级", "note": "负责市政府常务工作"},
    # 吴伟 (10)
    {"person_id": 10, "org_id": 2, "title": "灵武市委常委、市政府副市长", "start_date": "2021", "end_date": "present", "rank": "副处级", "note": ""},
    # 李明 (11)
    {"person_id": 11, "org_id": 2, "title": "灵武市副市长、市公安局局长、督察长", "start_date": "2019", "end_date": "present", "rank": "副处级", "note": ""},
    # 孙学福 (12)
    {"person_id": 12, "org_id": 2, "title": "灵武市政府党组成员、副市长", "start_date": "2023", "end_date": "present", "rank": "副处级", "note": "2023-07任职;与葛翔AB岗(2024-12分工)"},
    # 马莉 (13)
    {"person_id": 13, "org_id": 2, "title": "灵武市政府党组成员、副市长", "start_date": "2025-10", "end_date": "present", "rank": "副处级", "note": "2025-10领导之窗"},
    # 葛翔 (14)
    {"person_id": 14, "org_id": 2, "title": "灵武市政府党组副书记、常务副市长", "start_date": "2024", "end_date": "present", "rank": "副处级", "note": "2024-12政府领导班子分工通知主持常务工作"},
    # 冯哲 (15)
    {"person_id": 15, "org_id": 5, "title": "灵武市委常委、市纪委书记、监委主任", "start_date": "2021", "end_date": "present", "rank": "副处级", "note": "纪委五次全会出席(2025-01)"},
    # 刘静林 (16)
    {"person_id": 16, "org_id": 1, "title": "灵武市委常委、政法委书记", "start_date": "2022", "end_date": "present", "rank": "副处级", "note": ""},
    # 张耀翔 (17)
    {"person_id": 17, "org_id": 1, "title": "灵武市委常委、组织部长", "start_date": "2021", "end_date": "present", "rank": "副处级", "note": ""},
    # 徐少辉 (18)
    {"person_id": 18, "org_id": 17, "title": "灵武市委常委、崇兴镇党委书记", "start_date": "2024", "end_date": "present", "rank": "副处级", "note": "出席人武部党委会/市人大常委会"},
    # 归宗库 (19)
    {"person_id": 19, "org_id": 18, "title": "灵武市委常委、人武部部长", "start_date": "2022", "end_date": "present", "rank": "副处级", "note": ""},
    # 司应源 (20)
    {"person_id": 20, "org_id": 1, "title": "灵武市委副书记(专职)", "start_date": "2020", "end_date": "2021", "rank": "县处级", "note": "历史任职,现职待核"},
    # 何韬 (21)
    {"person_id": 21, "org_id": 19, "title": "灵武市委常委、宣传部部长、统战部部长、市政协党组副书记", "start_date": "2022", "end_date": "present", "rank": "副处级", "note": "回族,1989年6月生"},
]

# ══════════════════════════════════════════════════════════════
# 关系 (relationships)
# ══════════════════════════════════════════════════════════════
relationships = [
    # 现任书记与市长
    {"person_a": 1, "person_b": 2, "type": "党政搭班子", "context": "市委书记—市长/市委副书记,同为党政主要领导", "overlap_org": "灵武市四家班子", "overlap_period": "2024-11—present"},
    # 前任继任-书记
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor", "context": "李伟接替刘国强任灵武市委书记(刘国强2024-08调离)", "overlap_org": "中共灵武市委员会", "overlap_period": "2024-11交接"},
    {"person_a": 3, "person_b": 5, "type": "predecessor_successor", "context": "刘国强2020-12接替刘斌任灵武市委书记", "overlap_org": "中共灵武市委员会", "overlap_period": "2020-12"},
    # 前任-市长
    {"person_a": 2, "person_b": 4, "type": "predecessor_successor", "context": "刘磊2024-11接替杨玉龙任市长(杨玉林调银川副市长)", "overlap_org": "灵武市人民政府", "overlap_period": "2024-11交接"},
    # 班子内部关系
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "书记—人大主任四家班子搭档", "overlap_org": "灵武市四家班子", "overlap_period": "2024-11—present"},
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "书记—政协主席四家班子搭档", "overlap_org": "灵武市四家班子", "overlap_period": "2026—present"},
    {"person_a": 2, "person_b": 9, "type": "overlap", "context": "市长—常务副市长政府班子搭档", "overlap_org": "灵武市人民政府", "overlap_period": "2026-05—present"},
    {"person_a": 2, "person_b": 14, "type": "overlap", "context": "市长—常务副市长(前任常务)政府班子搭档", "overlap_org": "灵武市人民政府", "overlap_period": "2024-2026"},
    {"person_a": 1, "person_b": 15, "type": "overlap", "context": "书记—纪委书记同级联动", "overlap_org": "中共灵武市委员会", "overlap_period": "2024-11—present"},
    # 区域交流网络线索
    {"person_a": 3, "person_b": 4, "type": "overlap", "context": "杨玉龙市长任内刘国强书记搭班子(2020-2024)", "overlap_org": "灵武市四家班子", "overlap_period": "2020-2024"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "李伟前任银川市直部门局长、杨玉龙前任灵武市长后调银川市副市长,为银川市直—县(市)交流(推断弱)", "overlap_org": "银川市", "overlap_period": "2024"},
]

# ──────────────────────────────────────────────────────────────
def main() -> None:
    run_build(
        slug="灵武市",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    conn = sqlite3.connect(str(DB_PATH))
    for t in ("persons", "organizations", "positions", "relationships"):
        n = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"{t}: {n}")
    conn.close()


if __name__ == "__main__":
    main()