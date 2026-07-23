#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 大方县 leadership network.

Targets: 县委书记 (杨滨) & 县长 (任劲飞)
Data as of: 2026-07-23
Sources: www.gzdafang.gov.cn (official county government website)
"""

import os
import sys
import json
import sqlite3
from datetime import datetime

# ── Paths ──────────────────────────────────────────────────────────────
TASK_ID = "guizhou_大方县"
AS_OF = "2026-07-23"
TMP_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(TMP_DIR, "..", "..")
DB_PATH = os.path.join(TMP_DIR, "大方县_network.db")
GEXF_PATH = os.path.join(TMP_DIR, "大方县_network.gexf")
PERSONS_DIR = os.path.join(TMP_DIR, "persons")
os.makedirs(PERSONS_DIR, exist_ok=True)


# ── Source Register ────────────────────────────────────────────────────
source_register = []
def S(name, url):
    src_id = f"S{len(source_register)+1:03d}"
    source_register.append({"id": src_id, "name": name, "url": url})
    return src_id

S001 = S("大方县人民政府官网", "https://www.gzdafang.gov.cn/")
S002 = S("大方县领导之窗", "https://www.gzdafang.gov.cn/zwgk/ldzc/")
S003 = S("任劲飞简历", "https://www.gzdafang.gov.cn/zwgk/ldzc/xzfld/rjf/")
S004 = S("李萍简历", "https://www.gzdafang.gov.cn/zwgk/ldzc/xzfld/lp/")
S005 = S("王瑜简历", "https://www.gzdafang.gov.cn/zwgk/ldzc/xzfld/wy/")
S006 = S("张世达简历", "https://www.gzdafang.gov.cn/zwgk/ldzc/xzfld/zsd/")
S007 = S("赖吉珂简历", "https://www.gzdafang.gov.cn/zwgk/ldzc/xzfld/ljk/")
S008 = S("杨丽娟简历", "https://www.gzdafang.gov.cn/zwgk/ldzc/xzfld/ylj/")
S009 = S("向阳简历", "https://www.gzdafang.gov.cn/zwgk/ldzc/xzfld/xy/")
S010 = S("朱军简历", "https://www.gzdafang.gov.cn/zwgk/ldzc/xzfld/zj_5947596/")
S011 = S("胡荣华简历", "https://www.gzdafang.gov.cn/zwgk/ldzc/xzfld/hrh/")
S012 = S("罗兵简历", "https://www.gzdafang.gov.cn/zwgk/ldzc/xzfld/lb/")
S013 = S("丁灿辉简历", "https://www.gzdafang.gov.cn/zwgk/ldzc/xzfld/dch/")
S014 = S("张波简历", "https://www.gzdafang.gov.cn/zwgk/ldzc/xzfld/zb/")
S015 = S("大方县党政领导联系电话公示", "https://www.gzdafang.gov.cn/xwzx/tzgg/202606/t20260624_90552220.html")
S016 = S("大方县'两优一先'表彰大会新闻", "https://www.gzdafang.gov.cn/xwzx/zwyw/202607/t20260703_90582684.html")


# ── Data ───────────────────────────────────────────────────────────────

# Persons
persons = [
    {
        "id": 1,
        "name": "杨滨",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "大方县委书记",
        "current_org": "中共大方县委员会",
        "source": S002,
    },
    {
        "id": 2,
        "name": "任劲飞",
        "gender": "男",
        "ethnicity": "土家族",
        "birth": "1975年9月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "1998年8月",
        "current_post": "大方县委副书记、县人民政府县长",
        "current_org": "大方县人民政府",
        "source": S003,
    },
    {
        "id": 3,
        "name": "徐田",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "大方县委常委、县委组织部部长",
        "current_org": "中共大方县委员会",
        "source": S015,
    },
    {
        "id": 4,
        "name": "严红",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "大方县委常委、县委宣传部部长",
        "current_org": "中共大方县委员会",
        "source": S015,
    },
    {
        "id": 5,
        "name": "段习义",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "大方县委常委、县纪委书记、监委副主任(代理主任)",
        "current_org": "中共大方县纪律检查委员会",
        "source": S015,
    },
    {
        "id": 6,
        "name": "张祥",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "大方县委常委、县委政法委书记",
        "current_org": "中共大方县委员会",
        "source": S015,
    },
    {
        "id": 7,
        "name": "邱林",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "大方县委常委、县委办主任、县委统战部部长",
        "current_org": "中共大方县委员会",
        "source": S015,
    },
    {
        "id": 8,
        "name": "高朝宁",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "大方县委常委、县人武部部长",
        "current_org": "大方县人民武装部",
        "source": S015,
    },
    {
        "id": 9,
        "name": "李萍",
        "gender": "女",
        "ethnicity": "彝族",
        "birth": "1979年10月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "1999年12月",
        "current_post": "大方经济开发区党工委副书记、管委会主任，县政府党组副书记，县委教育工委副书记",
        "current_org": "大方县人民政府",
        "source": S004,
    },
    {
        "id": 10,
        "name": "王瑜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年8月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "2003年9月",
        "current_post": "大方县委常委、副县长",
        "current_org": "大方县人民政府",
        "source": S005,
    },
    {
        "id": 11,
        "name": "张世达",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年3月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "2010年5月",
        "current_post": "大方县委常委、副县长",
        "current_org": "大方县人民政府",
        "source": S006,
    },
    {
        "id": 12,
        "name": "赖吉珂",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987年7月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "2010年7月",
        "current_post": "大方县委常委、副县长（挂职）",
        "current_org": "大方县人民政府",
        "source": S007,
    },
    {
        "id": 13,
        "name": "杨丽娟",
        "gender": "女",
        "ethnicity": "穿青人",
        "birth": "1973年9月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "1996年1月",
        "current_post": "大方县人民政府副县长、县公安局党委书记、局长、督察长",
        "current_org": "大方县人民政府",
        "source": S008,
    },
    {
        "id": 14,
        "name": "向阳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985年11月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "2009年12月",
        "current_post": "大方县人民政府副县长",
        "current_org": "大方县人民政府",
        "source": S009,
    },
    {
        "id": 15,
        "name": "朱军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1988年1月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "2011年8月",
        "current_post": "大方县人民政府副县长",
        "current_org": "大方县人民政府",
        "source": S010,
    },
    {
        "id": 16,
        "name": "胡荣华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年10月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "2003年8月",
        "current_post": "大方县人民政府副县长、县教育局党组书记、局长",
        "current_org": "大方县人民政府",
        "source": S011,
    },
    {
        "id": 17,
        "name": "罗兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年11月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "2011年1月",
        "current_post": "大方县人民政府副县长",
        "current_org": "大方县人民政府",
        "source": S012,
    },
    {
        "id": 18,
        "name": "丁灿辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年9月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "2005年8月",
        "current_post": "大方县人民政府副县长（挂职）",
        "current_org": "大方县人民政府",
        "source": S013,
    },
    {
        "id": 19,
        "name": "张波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年11月",
        "birthplace": "",
        "education": "行政管理专业",
        "party_join": "中共党员",
        "work_start": "2007年12月",
        "current_post": "大方县人民政府党组成员、政府办党组书记、主任",
        "current_org": "大方县人民政府办公室",
        "source": S014,
    },
    {
        "id": 20,
        "name": "张锦",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "大方县人大常委会主任",
        "current_org": "大方县人大常委会",
        "source": S016,
    },
    {
        "id": 21,
        "name": "杨忠强",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "大方县政协主席",
        "current_org": "政协大方县委员会",
        "source": S016,
    },
]

# Organizations
organizations = [
    {"id": 1, "name": "中共大方县委员会", "type": "党委", "level": "县处级", "location": "贵州省毕节市大方县"},
    {"id": 2, "name": "大方县人民政府", "type": "政府", "level": "县处级", "location": "贵州省毕节市大方县"},
    {"id": 3, "name": "中共大方县纪律检查委员会", "type": "纪委", "level": "县处级", "location": "贵州省毕节市大方县"},
    {"id": 4, "name": "大方县人民武装部", "type": "政府", "level": "县处级", "location": "贵州省毕节市大方县"},
    {"id": 5, "name": "大方县人大常委会", "type": "人大", "level": "县处级", "location": "贵州省毕节市大方县"},
    {"id": 6, "name": "政协大方县委员会", "type": "政协", "level": "县处级", "location": "贵州省毕节市大方县"},
    {"id": 7, "name": "大方县人民政府办公室", "type": "政府", "level": "乡科级", "location": "贵州省毕节市大方县"},
    {"id": 8, "name": "大方经济开发区管委会", "type": "开发区", "level": "县处级", "location": "贵州省毕节市大方县"},
    {"id": 9, "name": "大方县公安局", "type": "政府", "level": "乡科级", "location": "贵州省毕节市大方县"},
    {"id": 10, "name": "大方县教育局", "type": "政府", "level": "乡科级", "location": "贵州省毕节市大方县"},
]

# Positions
positions = [
    # 杨滨 - 县委书记
    {"person_id": 1, "org_id": 1, "title": "大方县委书记", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任，此前曾任大方县县长"},
    # 任劲飞 - 县长
    {"person_id": 2, "org_id": 2, "title": "大方县人民政府县长", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任"},
    {"person_id": 2, "org_id": 1, "title": "大方县委副书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 县委常委
    {"person_id": 3, "org_id": 1, "title": "大方县委常委、县委组织部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 4, "org_id": 1, "title": "大方县委常委、县委宣传部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 5, "org_id": 3, "title": "大方县委常委、县纪委书记、监委副主任(代理主任)", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 6, "org_id": 1, "title": "大方县委常委、县委政法委书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 7, "org_id": 1, "title": "大方县委常委、县委办主任、县委统战部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 8, "org_id": 4, "title": "大方县委常委、县人武部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 李萍
    {"person_id": 9, "org_id": 2, "title": "大方经济开发区党工委副书记、管委会主任", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任，县政府党组副书记"},
    {"person_id": 9, "org_id": 8, "title": "大方经济开发区党工委副书记、管委会主任", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 王瑜 - 县委常委、副县长
    {"person_id": 10, "org_id": 2, "title": "大方县委常委、副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 10, "org_id": 1, "title": "大方县委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 张世达 - 县委常委、副县长
    {"person_id": 11, "org_id": 2, "title": "大方县委常委、副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "2026年4月更新"},
    {"person_id": 11, "org_id": 1, "title": "大方县委常委", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 赖吉珂 - 挂职副县长
    {"person_id": 12, "org_id": 2, "title": "大方县委常委、副县长（挂职）", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "挂职，天河区对口帮扶"},
    # 杨丽娟 - 副县长兼公安局长
    {"person_id": 13, "org_id": 2, "title": "大方县人民政府副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 13, "org_id": 9, "title": "大方县公安局党委书记、局长、督察长", "start_date": "", "end_date": "", "rank": "乡科级正职", "note": "现任，二级高级警长"},
    # 向阳 - 副县长
    {"person_id": 14, "org_id": 2, "title": "大方县人民政府副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 朱军 - 副县长
    {"person_id": 15, "org_id": 2, "title": "大方县人民政府副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 胡荣华 - 副县长
    {"person_id": 16, "org_id": 2, "title": "大方县人民政府副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 16, "org_id": 10, "title": "大方县教育局党组书记、局长", "start_date": "", "end_date": "", "rank": "乡科级正职", "note": "兼任"},
    # 罗兵 - 副县长
    {"person_id": 17, "org_id": 2, "title": "大方县人民政府副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 丁灿辉 - 挂职副县长
    {"person_id": 18, "org_id": 2, "title": "大方县人民政府副县长（挂职）", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "挂职"},
    # 张波 - 政府办主任
    {"person_id": 19, "org_id": 2, "title": "大方县人民政府党组成员", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 19, "org_id": 7, "title": "大方县人民政府办公室党组书记、主任", "start_date": "", "end_date": "", "rank": "乡科级正职", "note": "现任"},
    # 张锦 - 人大主任
    {"person_id": 20, "org_id": 5, "title": "大方县人大常委会主任", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任"},
    # 杨忠强 - 政协主席
    {"person_id": 21, "org_id": 6, "title": "大方县政协主席", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任"},
]

# Relationships (工作关系)
relationships = [
    # 县委书记 ↔ 县长 (核心搭档)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "杨滨（县委书记）与任劲飞（县长）构成县委-政府核心搭档", "overlap_org": "中共大方县委员会/大方县人民政府", "overlap_period": ""},
    # 县委书记 ↔ 县委组织部部长
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "杨滨（县委书记）与徐田（县委组织部部长）在县委常委会共事", "overlap_org": "中共大方县委员会", "overlap_period": ""},
    # 县委书记 ↔ 县委宣传部部长
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "杨滨（县委书记）与严红（县委宣传部部长）在县委常委会共事", "overlap_org": "中共大方县委员会", "overlap_period": ""},
    # 县委书记 ↔ 县纪委书记
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "杨滨（县委书记）与段习义（县纪委书记）在县委常委会共事", "overlap_org": "中共大方县委员会", "overlap_period": ""},
    # 县委书记 ↔ 政法委书记
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "杨滨（县委书记）与张祥（县委政法委书记）在县委常委会共事", "overlap_org": "中共大方县委员会", "overlap_period": ""},
    # 县委书记 ↔ 县委办主任
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "杨滨（县委书记）与邱林（县委办主任、统战部部长）在县委常委会共事", "overlap_org": "中共大方县委员会", "overlap_period": ""},
    # 县长 ↔ 副县长李萍
    {"person_a": 2, "person_b": 9, "type": "overlap", "context": "任劲飞（县长）与李萍（县政府党组副书记）在县政府班子共事", "overlap_org": "大方县人民政府", "overlap_period": ""},
    # 县长 ↔ 副县长王瑜
    {"person_a": 2, "person_b": 10, "type": "overlap", "context": "任劲飞（县长）与王瑜（县委常委、副县长）在县政府班子共事", "overlap_org": "大方县人民政府", "overlap_period": ""},
    # 县长 ↔ 副县长张世达
    {"person_a": 2, "person_b": 11, "type": "overlap", "context": "任劲飞（县长）与张世达（县委常委、副县长）在县政府班子共事", "overlap_org": "大方县人民政府", "overlap_period": ""},
    # 县长 ↔ 副县长杨丽娟
    {"person_a": 2, "person_b": 13, "type": "overlap", "context": "任劲飞（县长）与杨丽娟（副县长、县公安局长）在县政府班子共事", "overlap_org": "大方县人民政府", "overlap_period": ""},
    # 县长 ↔ 副县长向阳
    {"person_a": 2, "person_b": 14, "type": "overlap", "context": "任劲飞（县长）与向阳（副县长）在县政府班子共事", "overlap_org": "大方县人民政府", "overlap_period": ""},
    # 县长 ↔ 副县长朱军
    {"person_a": 2, "person_b": 15, "type": "overlap", "context": "任劲飞（县长）与朱军（副县长）在县政府班子共事", "overlap_org": "大方县人民政府", "overlap_period": ""},
    # 县长 ↔ 副县长胡荣华
    {"person_a": 2, "person_b": 16, "type": "overlap", "context": "任劲飞（县长）与胡荣华（副县长）在县政府班子共事", "overlap_org": "大方县人民政府", "overlap_period": ""},
    # 县长 ↔ 副县长罗兵
    {"person_a": 2, "person_b": 17, "type": "overlap", "context": "任劲飞（县长）与罗兵（副县长）在县政府班子共事", "overlap_org": "大方县人民政府", "overlap_period": ""},
    # 副县长之间的常委联系
    {"person_a": 10, "person_b": 11, "type": "overlap", "context": "王瑜与张世达同为县委常委、副县长", "overlap_org": "中共大方县委员会/大方县人民政府", "overlap_period": ""},
    {"person_a": 10, "person_b": 12, "type": "overlap", "context": "王瑜与赖吉珂（挂职）在县政府班子共事，赖吉珂协助王瑜工作", "overlap_org": "大方县人民政府", "overlap_period": ""},
    {"person_a": 11, "person_b": 12, "type": "overlap", "context": "张世达与赖吉珂（挂职）同为县委常委、副县长", "overlap_org": "中共大方县委员会/大方县人民政府", "overlap_period": ""},
    # 县委制度性联系
    {"person_a": 3, "person_b": 7, "type": "overlap", "context": "徐田（组织部部长）与邱林（县委办主任）在县委常委会共事", "overlap_org": "中共大方县委员会", "overlap_period": ""},
    {"person_a": 4, "person_b": 7, "type": "overlap", "context": "严红（宣传部部长）与邱林（统战部部长）在县委常委会共事", "overlap_org": "中共大方县委员会", "overlap_period": ""},
    {"person_a": 6, "person_b": 13, "type": "overlap", "context": "张祥（政法委书记）与杨丽娟（公安局长）在政法系统有工作联系", "overlap_org": "大方县政法系统", "overlap_period": ""},
    # 人大/政协与县委
    {"person_a": 1, "person_b": 20, "type": "overlap", "context": "杨滨（县委书记）与张锦（县人大常委会主任）在县领导班子的制度性联系", "overlap_org": "大方县领导班子", "overlap_period": ""},
    {"person_a": 1, "person_b": 21, "type": "overlap", "context": "杨滨（县委书记）与杨忠强（县政协主席）在县领导班子的制度性联系", "overlap_org": "大方县领导班子", "overlap_period": ""},
    {"person_a": 2, "person_b": 20, "type": "overlap", "context": "任劲飞（县长）与张锦（人大主任）在县领导班子的制度性联系", "overlap_org": "大方县领导班子", "overlap_period": ""},
    {"person_a": 2, "person_b": 21, "type": "overlap", "context": "任劲飞（县长）与杨忠强（政协主席）在县领导班子的制度性联系", "overlap_org": "大方县领导班子", "overlap_period": ""},
]


# =========================================================================
# Build functions
# =========================================================================

def esc(s):
    """XML-escape a string."""
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def person_color(post):
    if "书记" in post and "副" not in post and "纪委" not in post:
        return "255,50,50"
    if "县长" in post and "副" not in post and "人大" not in post and "政协" not in post:
        return "50,100,255"
    if "纪委书记" in post or "监委" in post:
        return "255,165,0"
    if "人大" in post and "主任" in post and "副" not in post:
        return "200,100,100"
    if "政协" in post and "主席" in post and "副" not in post:
        return "180,120,80"
    if "副" in post or "副书记" in post:
        return "100,150,220"
    if "主任" in post and "副" not in post:
        return "60,180,60"
    if "政协" in post:
        return "180,160,80"
    return "100,100,100"


def is_top_leader(post):
    return ("书记" in post and "副" not in post and "纪委" not in post) or \
           ("县长" in post and "副" not in post and "人大" not in post and "政协" not in post)


def person_shape(post):
    if "书记" in post and "副" not in post and "纪委" not in post:
        return "square"
    if "县长" in post and "副" not in post and "人大" not in post and "政协" not in post:
        return "circle"
    if "纪委书记" in post or "纪委" in post:
        return "diamond"
    return "triangle"


def org_color(otype):
    colors = {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "人大": "200,255,255",
        "政协": "255,240,200",
        "纪委": "255,200,150",
        "开发区": "200,255,200",
    }
    return colors.get(otype, "200,200,200")


def build():
    os.makedirs(BASE, exist_ok=True)

    # ── SQLite ──
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS organizations;
        DROP TABLE IF EXISTS persons;

        CREATE TABLE persons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pid TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            gender TEXT DEFAULT '',
            ethnicity TEXT DEFAULT '',
            birth TEXT DEFAULT '',
            birthplace TEXT DEFAULT '',
            education TEXT DEFAULT '',
            party_join TEXT DEFAULT '',
            work_start TEXT DEFAULT '',
            current_post TEXT DEFAULT '',
            current_org TEXT DEFAULT '',
            source TEXT DEFAULT ''
        );

        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        );

        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT DEFAULT '',
            start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '',
            note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(pid),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );

        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(pid),
            FOREIGN KEY (person_b) REFERENCES persons(pid)
        );
    """)

    person_map = {}
    for idx, p in enumerate(persons, 1):
        pid = f"dafang_{p['name']}"
        person_map[p["id"]] = pid
        cur.execute("""INSERT INTO persons (id,pid,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source) 
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (idx, pid, p["name"], p.get("gender", ""), p.get("ethnicity", ""), p.get("birth", ""),
                     p.get("birthplace", ""), p.get("education", ""), p.get("party_join", ""), p.get("work_start", ""),
                     p.get("current_post", ""), p.get("current_org", ""), p.get("source", "")))

    for o in organizations:
        cur.execute("""INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)""",
                    (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        cur.execute("""INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)""",
                    (person_map[pos["person_id"]], pos["org_id"], pos["title"], pos.get("start_date", ""),
                     pos.get("end_date", ""), pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)""",
                    (person_map[r["person_a"]], person_map[r["person_b"]], r["type"], r["context"],
                     r.get("overlap_org", ""), r.get("overlap_period", "")))

    conn.commit()

    person_count = len(persons)
    org_count = len(organizations)
    pos_count = len(positions)
    rel_count = len(relationships)

    print(f"DB written: {DB_PATH}")
    print(f"  {person_count} persons, {org_count} orgs, {pos_count} positions, {rel_count} relationships")

    conn.close()

    # ── GEXF ──
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append(f'    <description>大方县领导班子关系网络（基于大方县政府官网、联系电话公示、新闻报道）</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="source" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes — persons
    lines.append('    <nodes>')
    for p in persons:
        pid_num = p["id"]
        post = p.get("current_post", "")
        c = person_color(post)
        sz = "20.0" if is_top_leader(post) else "12.0"
        shape = person_shape(post)

        lines.append(f'      <node id="p{pid_num}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("source",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}" a="1.0"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append(f'        <viz:shape value="{shape}"/>')
        lines.append('      </node>')

    # Nodes — organizations
    for o in organizations:
        oid = o["id"] + 100000
        ocolor = org_color(o["type"])

        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{ocolor.split(",")[0]}" g="{ocolor.split(",")[1]}" b="{ocolor.split(",")[2]}" a="0.8"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append(f'        <viz:shape value="hexagon"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    # Person → organization
    for pos in positions:
        if pos["org_id"] == 99:
            continue
        eid += 1
        pid_num = pos["person_id"]
        oid = pos["org_id"] + 100000
        lines.append(
            f'      <edge id="e{eid}" source="p{pid_num}" target="o{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    # Person ↔ person
    for r in relationships:
        eid += 1
        lines.append(
            f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")

    # ── Person Graph JSONs ──
    now = AS_OF.replace("-", "")

    def make_person_json(p, timeline, relationships_list, custom_identity=None):
        result = {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": "贵州省",
                "city": "毕节市",
                "region": "大方县",
                "job": p.get("current_post", ""),
                "task_id": TASK_ID,
                "time_focus": "2026年7月"
            },
            "identity": {
                "person_id": f"dafang_{p['name']}",
                "name": p["name"],
                "aliases": [],
                "gender": p.get("gender", ""),
                "ethnicity": p.get("ethnicity", ""),
                "birth": p.get("birth", ""),
                "birthplace": p.get("birthplace", ""),
                "native_place": "",
                "education": [
                    {
                        "period": "",
                        "institution": "",
                        "major": "",
                        "degree": p.get("education", ""),
                        "study_type": "unknown",
                        "source_ids": []
                    }
                ] if p.get("education") else [],
                "party_join": p.get("party_join", ""),
                "work_start": p.get("work_start", ""),
                "dedupe_keys": {
                    "name_birth": f"{p['name']}_{p.get('birth', '')}",
                    "name_birthplace": f"{p['name']}_{p.get('birthplace', '')}",
                    "official_profile_url": p.get("source", "")
                }
            },
            "current_status": {
                "current_post": p.get("current_post", ""),
                "current_org": p.get("current_org", ""),
                "administrative_rank": "县处级正职" if is_top_leader(p.get("current_post", "")) else "县处级副职",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": []
            },
            "career_timeline": timeline,
            "organizations": [],
            "relationships": relationships_list,
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": [],
                "geographic_pattern": [],
                "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "在公开信息中未发现该人物负面信号",
                 "date": "", "confidence": "confirmed", "source_ids": []}
            ],
            "source_register": source_register,
            "confidence_summary": {
                "identity": "confirmed",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": f"{p['name']}的完整履历信息缺失（出生地、早期职业生涯、教育经历等）"
            },
            "open_questions": [
                {"priority": "critical",
                 "question": f"{p['name']}的完整职业生涯履历",
                 "why_it_matters": "无法追溯其任职路径和系统经历",
                 "suggested_queries": [f"{p['name']} 简历 大方县"],
                 "last_attempted": AS_OF},
            ]
        }
        if custom_identity:
            result["identity"].update(custom_identity)
        return result

    # ── 杨滨 Person JSON ──
    yb_timeline = [
        {"start": "", "end": "", "org": "中共大方县委员会", "title": "大方县委书记",
         "notes": "现任（2026年6月确认）", "confidence": "confirmed", "source_ids": ["S015", "S016"]},
        {"start": "", "end": "", "org": "大方县人民政府", "title": "大方县人民政府县长",
         "notes": "此前曾任大方县县长，后升任县委书记", "confidence": "plausible", "source_ids": ["S015"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "杨滨的大方县以前完整履历未找到",
         "confidence": "unverified", "source_ids": []},
    ]
    yb_relationships = [
        {"person": "任劲飞", "person_id": "dafang_任劲飞", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "杨滨（县委书记）与任劲飞（县长）在县委常委会和县政府班子构成核心搭档",
         "overlap_org": "中共大方县委员会/大方县人民政府", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S015", "S016"]},
        {"person": "徐田", "person_id": "dafang_徐田", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "杨滨（县委书记）与徐田（县委组织部部长）在县委常委会共事",
         "overlap_org": "中共大方县委员会", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S015"]},
        {"person": "张锦", "person_id": "dafang_张锦", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "杨滨（县委书记）与张锦（人大主任）在县领导班子中制度性联系",
         "overlap_org": "大方县领导班子", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S016"]},
    ]

    yb_json = make_person_json(persons[0], yb_timeline, yb_relationships)
    yb_path = os.path.join(PERSONS_DIR, f"{now}-贵州省-毕节市-县委书记-杨滨.json")
    with open(yb_path, "w", encoding="utf-8") as f:
        json.dump(yb_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {yb_path}")

    # ── 任劲飞 Person JSON ──
    rjf_timeline = [
        {"start": "", "end": "", "org": "大方县人民政府", "title": "大方县人民政府县长",
         "notes": "现任", "confidence": "confirmed", "source_ids": ["S003"]},
        {"start": "", "end": "", "org": "中共大方县委员会", "title": "大方县委副书记",
         "notes": "现任", "confidence": "confirmed", "source_ids": ["S003"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "1998年8月参加工作至任大方县县长期间完整履历未找到",
         "confidence": "unverified", "source_ids": []},
    ]
    rjf_relationships = [
        {"person": "杨滨", "person_id": "dafang_杨滨", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "任劲飞（县长）与杨滨（县委书记）构成县委-政府核心搭档",
         "overlap_org": "中共大方县委员会/大方县人民政府", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S015", "S016"]},
        {"person": "李萍", "person_id": "dafang_李萍", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "任劲飞（县长）与李萍（县政府党组副书记）在县政府班子共事",
         "overlap_org": "大方县人民政府", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003", "S004"]},
        {"person": "王瑜", "person_id": "dafang_王瑜", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "任劲飞（县长）与王瑜（县委常委、副县长）在县政府班子共事",
         "overlap_org": "大方县人民政府", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003", "S005"]},
        {"person": "张世达", "person_id": "dafang_张世达", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "任劲飞（县长）与张世达（县委常委、副县长）在县政府班子共事",
         "overlap_org": "大方县人民政府", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003", "S006"]},
        {"person": "杨丽娟", "person_id": "dafang_杨丽娟", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "任劲飞（县长）与杨丽娟（副县长、公安局长）在县政府班子共事",
         "overlap_org": "大方县人民政府", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003", "S008"]},
    ]

    rjf_json = make_person_json(persons[1], rjf_timeline, rjf_relationships)
    rjf_path = os.path.join(PERSONS_DIR, f"{now}-贵州省-毕节市-县长-任劲飞.json")
    with open(rjf_path, "w", encoding="utf-8") as f:
        json.dump(rjf_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {rjf_path}")

    # ── 李萍 Person JSON ──
    lp_timeline = [
        {"start": "", "end": "", "org": "大方县人民政府", "title": "大方经济开发区党工委副书记、管委会主任，县政府党组副书记",
         "notes": "现任", "confidence": "confirmed", "source_ids": ["S004"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "1999年12月参加工作至今完整履历未找到",
         "confidence": "unverified", "source_ids": []},
    ]
    lp_relationships = [
        {"person": "任劲飞", "person_id": "dafang_任劲飞", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "李萍（县政府党组副书记）与任劲飞（县长）在县政府班子共事",
         "overlap_org": "大方县人民政府", "overlap_period": "",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003", "S004"]},
    ]

    lp_json = make_person_json(persons[8], lp_timeline, lp_relationships)
    lp_path = os.path.join(PERSONS_DIR, f"{now}-贵州省-毕节市-常务副县长-李萍.json")
    with open(lp_path, "w", encoding="utf-8") as f:
        json.dump(lp_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {lp_path}")

    # ── Summary ──
    print(f"\nSummary:")
    print(f"  Persons: {person_count}")
    print(f"  Organizations: {org_count}")
    print(f"  Positions: {pos_count}")
    print(f"  Relationships: {rel_count}")
    print(f"  Sources: {len(source_register)}")
    print(f"\nArtifacts:")
    print(f"  DB: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")
    print(f"  Person JSONs: {yb_path}, {rjf_path}, {lp_path}")


if __name__ == "__main__":
    build()
