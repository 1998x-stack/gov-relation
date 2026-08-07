#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Sanyuan County leadership network.

三原县·咸阳市·陕西省 — 县委书记 杨红刚；县委副书记、代县长 段朋泊。
Research as of 2026-08-07 (sources: official 领导之窗 pages on snsanyuan.gov.cn).
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
DB_PATH = os.path.join(BASE, "data/database/三原县_network.db")
GEXF_PATH = os.path.join(BASE, "data/graph/三原县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── 现任县委班子 (10名, 含县委书记) ──
    {"id": 1, "name": "杨红刚", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-11", "birthplace": "", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委书记", "current_org": "中共三原县委",
     "source": "https://www.snsanyuan.gov.cn/zfxxgk/fdzdgknr/ldzc/xwld/yhg/"},
    {"id": 2, "name": "段朋泊", "gender": "男", "ethnicity": "汉族",
     "birth": "1979-10", "birthplace": "", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委副书记、县政府党组书记、代县长", "current_org": "三原县人民政府",
     "source": "https://www.snsanyuan.gov.cn/zfxxgk/fdzdgknr/ldzc/xwld/dpb/"},
    {"id": 3, "name": "刘晖", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-06", "birthplace": "", "education": "大学本科",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、宣传部部长", "current_org": "中共三原县委宣传部",
     "source": "https://www.snsanyuan.gov.cn/zfxxgk/fdzdgknr/ldzc/xwld/lh_0001/"},
    {"id": 4, "name": "曹博", "gender": "男", "ethnicity": "汉族",
     "birth": "1979-10", "birthplace": "", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、常务副县长", "current_org": "三原县人民政府",
     "source": "https://www.snsanyuan.gov.cn/zfxxgk/fdzdgknr/ldzc/xwld/cb/"},
    {"id": 5, "name": "田广军", "gender": "男", "ethnicity": "汉族",
     "birth": "1982-07", "birthplace": "", "education": "大学学历、工学学士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、县纪委书记、县监委主任", "current_org": "中共三原县纪委/县监委",
     "source": "https://www.snsanyuan.gov.cn/zfxxgk/fdzdgknr/ldzc/xwld/tgj/"},
    {"id": 6, "name": "李科显", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-08", "birthplace": "", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、副县长", "current_org": "三原县人民政府",
     "source": "https://www.snsanyuan.gov.cn/zfxxgk/fdzdgknr/ldzc/xwld/lkx/"},
    {"id": 7, "name": "许超莹", "gender": "女", "ethnicity": "汉族",
     "birth": "1977-06", "birthplace": "", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、政法委书记", "current_org": "中共三原县委政法委",
     "source": "https://www.snsanyuan.gov.cn/zfxxgk/fdzdgknr/ldzc/xwld/xcy/"},
    {"id": 8, "name": "李超", "gender": "男", "ethnicity": "汉族",
     "birth": "1984-10", "birthplace": "", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、组织部部长", "current_org": "中共三原县委组织部",
     "source": "https://www.snsanyuan.gov.cn/zfxxgk/fdzdgknr/ldzc/xwld/lc/"},
    {"id": 9, "name": "田成博", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-04", "birthplace": "", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、县人武部部长", "current_org": "三原县人武部",
     "source": "https://www.snsanyuan.gov.cn/zfxxgk/fdzdgknr/ldzc/xwld/tcb/"},
    {"id": 10, "name": "雷彬献", "gender": "男", "ethnicity": "汉族",
     "birth": "1976-06", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县委常委、统战部部长", "current_org": "中共三原县委统战部",
     "source": "https://www.snsanyuan.gov.cn/zfxxgk/fdzdgknr/ldzc/xwld/lbx/"},

    # ── 县政府班子成员 (除已列者) ──
    {"id": 11, "name": "尚科", "gender": "男", "ethnicity": "汉族",
     "birth": "1977-11", "birthplace": "", "education": "大学学历",
     "party_join": "", "work_start": "",
     "current_post": "副县长", "current_org": "三原县人民政府",
     "source": "https://www.snsanyuan.gov.cn/zfxxgk/fdzdgknr/ldzc/xzfld/sk/"},
    {"id": 12, "name": "常俊鸿", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-09", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "副县长、县公安局局长", "current_org": "三原县公安局",
     "source": "https://www.snsanyuan.gov.cn/zfxxgk/fdzdgknr/ldzc/xzfld/cjh/"},
    {"id": 13, "name": "陈飞", "gender": "男", "ethnicity": "汉族",
     "birth": "1987-11", "birthplace": "", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "副县长", "current_org": "三原县人民政府",
     "source": "https://www.snsanyuan.gov.cn/zfxxgk/fdzdgknr/ldzc/xzfld/cf/"},
    {"id": 14, "name": "魏书威", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-03", "birthplace": "", "education": "研究生（工学博士，博士生导师，正高级工程师）",
     "party_join": "中共党员", "work_start": "",
     "current_post": "副县长", "current_org": "三原县人民政府",
     "source": "https://www.snsanyuan.gov.cn/zfxxgk/fdzdgknr/ldzc/xzfld/wsw/"},

    # ── 县人大常委会 ──
    {"id": 15, "name": "蒙小卫", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-03", "birthplace": "", "education": "大专学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县人大常委会党组书记、主任", "current_org": "三原县人大常委会",
     "source": "https://www.snsanyuan.gov.cn/zfxxgk/fdzdgknr/ldzc/xrdld/mxw/"},
    {"id": 16, "name": "倪新刚", "gender": "男", "ethnicity": "汉族",
     "birth": "1971-04", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县人大常委会副主任", "current_org": "三原县人大常委会",
     "source": "https://www.snsanyuan.gov.cn/zfxxgk/fdzdgknr/ldzc/xrdld/nxg/"},
    {"id": 17, "name": "李鹏科", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-10", "birthplace": "", "education": "大专学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县人大常委会副主任 (兼任县委组织部常务副部长)", "current_org": "三原县人大常委会",
     "source": "https://www.snsanyuan.gov.cn/zfxxgk/fdzdgknr/ldzc/xrdld/lpk/"},
    {"id": 18, "name": "蔺永芳", "gender": "女", "ethnicity": "汉族",
     "birth": "1972-07", "birthplace": "", "education": "大专学历",
     "party_join": "民建会员", "work_start": "",
     "current_post": "县人大常委会副主任", "current_org": "三原县人大常委会",
     "source": "https://www.snsanyuan.gov.cn/zfxxgk/fdzdgknr/ldzc/xrdld/lyf/"},

    # ── 县政协 ──
    {"id": 19, "name": "李学军", "gender": "男", "ethnicity": "汉族",
     "birth": "1968-10", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县政协党组书记、主席", "current_org": "三原县政协",
     "source": "https://www.snsanyuan.gov.cn/zfxxgk/fdzdgknr/ldzc/xzxld/lxj/"},
    {"id": 20, "name": "张永刚", "gender": "男", "ethnicity": "汉族",
     "birth": "1970-01", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "县政协党组副书记、副主席", "current_org": "三原县政协",
     "source": "https://www.snsanyuan.gov.cn/zfxxgk/fdzdgknr/ldzc/xzxld/zyg/"},
    {"id": 21, "name": "钱滨", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-07", "birthplace": "", "education": "",
     "party_join": "民盟盟员", "work_start": "",
     "current_post": "县政协副主席", "current_org": "三原县政协",
     "source": "https://www.snsanyuan.gov.cn/zfxxgk/fdzdgknr/ldzc/xzxld/qb/"},
    {"id": 22, "name": "姚青勋", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-11", "birthplace": "", "education": "",
     "party_join": "农工党党员", "work_start": "",
     "current_post": "县政协副主席", "current_org": "三原县政协",
     "source": "https://www.snsanyuan.gov.cn/zfxxgk/fdzdgknr/ldzc/xzxld/yqx/"},

    # ── 前任县委书记 赵俊强 (已卸任，去向待查) ──
    {"id": 23, "name": "赵俊强", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "（卸任）", "current_org": "（卸任县委书记）",
     "source": "https://www.snsanyuan.gov.cn/xw/ (2026年6月前仍以县委书记身份出席活动)"},
]

organizations = [
    {"id": 1, "name": "中共三原县委", "type": "党委", "level": "县级", "parent": "中共咸阳市委", "location": "陕西省咸阳市三原县"},
    {"id": 2, "name": "三原县人民政府", "type": "政府", "level": "县级", "parent": "咸阳市人民政府", "location": "陕西省咸阳市三原县"},
    {"id": 3, "name": "中共三原县纪律检查委员会", "type": "纪委", "level": "县级", "parent": "中共三原县委", "location": "陕西省咸阳市三原县"},
    {"id": 4, "name": "三原县监察委员会", "type": "监察", "level": "县级", "parent": "三原县人民政府", "location": "陕西省咸阳市三原县"},
    {"id": 5, "name": "三原县人大常委会", "type": "人大", "level": "县级", "parent": "", "location": "陕西省咸阳市三原县"},
    {"id": 6, "name": "三原县政协", "type": "政协", "level": "县级", "parent": "", "location": "陕西省咸阳市三原县"},
    {"id": 7, "name": "中共三原县委宣传部", "type": "党委部门", "level": "县级", "parent": "中共三原县委", "location": "陕西省咸阳市三原县"},
    {"id": 8, "name": "中共三原县委政法委", "type": "党委部门", "level": "县级", "parent": "中共三原县委", "location": "陕西省咸阳市三原县"},
    {"id": 9, "name": "中共三原县委组织部", "type": "党委部门", "level": "县级", "parent": "中共三原县委", "location": "陕西省咸阳市三原县"},
    {"id": 10, "name": "中共三原县委统战部", "type": "党委部门", "level": "县级", "parent": "中共三原县委", "location": "陕西省咸阳市三原县"},
    {"id": 11, "name": "三原县人武部", "type": "军事", "level": "县级", "parent": "咸阳军分区", "location": "陕西省咸阳市三原县"},
    {"id": 12, "name": "三原县公安局", "type": "政府", "level": "县级", "parent": "咸阳市公安局", "location": "陕西省咸阳市三原县"},
]

positions = [
    # ── 杨红刚 (县委书记, 原县长) ──
    {"id": 1, "person_id": 1, "org_id": 1, "title": "县委书记", "start": "2026-06", "end": "", "rank": "正县级", "note": "现任"},
    {"id": 2, "person_id": 1, "org_id": 2, "title": "县长", "start": "", "end": "2026-06", "rank": "正县级", "note": "前任职务，2026年4月仍以县长身份出席五四晚会"},

    # ── 段朋泊 (代县长) ──
    {"id": 3, "person_id": 2, "org_id": 2, "title": "县委副书记、县政府党组书记、代县长", "start": "2026-07", "end": "", "rank": "正县级", "note": "现任"},
    {"id": 4, "person_id": 2, "org_id": 1, "title": "县委副书记（专职)", "start": "", "end": "2026-07", "rank": "副县级", "note": "前任职务"},

    # ── 县委常委成员 ──
    {"id": 5, "person_id": 3, "org_id": 7, "title": "县委常委、宣传部部长", "start": "", "end": "", "rank": "副县级", "note": "现任"},
    {"id": 6, "person_id": 4, "org_id": 1, "title": "县委常委", "start": "", "end": "", "rank": "副县级", "note": "现任"},
    {"id": 7, "person_id": 4, "org_id": 2, "title": "常务副县长", "start": "", "end": "", "rank": "副县级", "note": "现任"},
    {"id": 8, "person_id": 5, "org_id": 3, "title": "县委常委、纪委书记、县监委主任", "start": "2026", "end": "", "rank": "副县级", "note": "现任，曾任宣传部长"},
    {"id": 9, "person_id": 6, "org_id": 1, "title": "县委常委", "start": "", "end": "", "rank": "副县级", "note": "现任"},
    {"id": 10, "person_id": 6, "org_id": 2, "title": "副县长", "start": "", "end": "", "rank": "副县级", "note": "现任"},
    {"id": 11, "person_id": 7, "org_id": 1, "title": "县委常委、政法委书记", "start": "", "end": "", "rank": "副县级", "note": "现任"},
    {"id": 12, "person_id": 8, "org_id": 1, "title": "县委常委、组织部部长", "start": "", "end": "", "rank": "副县级", "note": "现任"},
    {"id": 13, "person_id": 9, "org_id": 1, "title": "县委常委、县人武部部长", "start": "", "end": "", "rank": "副县级", "note": "现任"},
    {"id": 14, "person_id": 10, "org_id": 10, "title": "县委常委、统战部部长", "start": "", "end": "", "rank": "副县级", "note": "现任"},

    # ── 县政府其他副县长 ──
    {"id": 15, "person_id": 11, "org_id": 2, "title": "副县长", "start": "", "end": "", "rank": "副县级", "note": "现任"},
    {"id": 16, "person_id": 12, "org_id": 12, "title": "副县长、县公安局局长", "start": "", "end": "", "rank": "副县级", "note": "现任"},
    {"id": 17, "person_id": 13, "org_id": 2, "title": "副县长", "start": "", "end": "", "rank": "副县级", "note": "现任"},
    {"id": 18, "person_id": 14, "org_id": 2, "title": "副县长", "start": "", "end": "", "rank": "副县级", "note": "现任——专家型人才;技术/挂职"},

    # ── 县人大常委会 ──
    {"id": 19, "person_id": 15, "org_id": 5, "title": "县人大常委会党组书记、主任", "start": "", "end": "", "rank": "正县级", "note": "现任"},
    {"id": 20, "person_id": 16, "org_id": 5, "title": "县人大常委会副主任", "start": "", "end": "", "rank": "副县级", "note": "现任"},
    {"id": 21, "person_id": 17, "org_id": 5, "title": "县人大常委会副主任", "start": "", "end": "", "rank": "副县级", "note": "现任，兼县委组织部常务副部长"},
    {"id": 22, "person_id": 18, "org_id": 5, "title": "县人大常委会副主任", "start": "", "end": "", "rank": "副县级", "note": "现任，民建" },

    # ── 县政协 ──
    {"id": 23, "person_id": 19, "org_id": 6, "title": "县政协党组书记、主席", "start": "", "end": "", "rank": "正县级", "note": "现任"},
    {"id": 24, "person_id": 20, "org_id": 6, "title": "县政协党组副书记、副主席", "start": "", "end": "", "rank": "副县级", "note": "现任"},
    {"id": 25, "person_id": 21, "org_id": 6, "title": "县政协副主席", "start": "", "end": "", "rank": "副县级", "note": "现任 (民盟)"},
    {"id": 26, "person_id": 22, "org_id": 6, "title": "县政协副主席", "start": "", "end": "", "rank": "副县级", "note": "现任 (农工党)"},

    # ── 前任县委书记 赵俊强 ──
    {"id": 27, "person_id": 23, "org_id": 1, "title": "县委书记", "start": "", "end": "2026-06", "rank": "正县级", "note": "前任县委书记；2026年4-6月尚以书记身份参加活动，6月底前卸任；去向待查"},
]

relationships = [
    # ── 书记-县长搭档 ──
    {"id": 1, "person_a_id": 1, "person_b_id": 2, "type": "党政搭档", "context": "杨红刚任县委书记，段朋泊任代县长，新一届党政班子", "overlap_org": "中共三原县委", "overlap_period": "2026-07"},
    {"id": 2, "person_a_id": 23, "person_b_id": 1, "type": "交接", "context": "赵俊强→杨红刚 县委书记交接（约2026年6-7月）", "overlap_org": "中共三原县委", "overlap_period": "2026"},
    {"id": 3, "person_a_id": 1, "person_b_id": 2, "type": "交接", "context": "杨红刚由县长升任书记，段朋泊由副书记接任代县长（2026年夏）", "overlap_org": "三原县人民政府", "overlap_period": "2026"},

    # ── 县委常委会成员同僚 ──
    {"id": 4, "person_a_id": 1, "person_b_id": 3, "type": "同僚", "context": "县委常委成员在县委常委会共事", "overlap_org": "中共三原县委", "overlap_period": "2026"},
    {"id": 5, "person_a_id": 1, "person_b_id": 4, "type": "同僚", "context": "县委书记与常务副县长共事", "overlap_org": "中共三原县委", "overlap_period": "2026"},
    {"id": 6, "person_a_id": 1, "person_b_id": 5, "type": "同僚", "context": "县委书记与县纪委书记共事", "overlap_org": "中共三原县纪委", "overlap_period": "2026"},
    {"id": 7, "person_a_id": 1, "person_b_id": 6, "type": "同僚", "context": "县委书记与副县长共事", "overlap_org": "中共三原县委", "overlap_period": "2026"},
    {"id": 8, "person_a_id": 1, "person_b_id": 7, "type": "同僚", "context": "县委书记与政法委书记共事", "overlap_org": "中共三原县委", "overlap_period": "2026"},
    {"id": 9, "person_a_id": 1, "person_b_id": 8, "type": "同僚", "context": "县委书记与组织部长共事", "overlap_org": "中共三原县委", "overlap_period": "2026"},
    {"id": 10, "person_a_id": 1, "person_b_id": 9, "type": "同僚", "context": "县委书记与人武部长共事", "overlap_org": "中共三原县委", "overlap_period": "2026"},
    {"id": 11, "person_a_id": 1, "person_b_id": 10, "type": "同僚", "context": "县委书记与统战部长共事", "overlap_org": "中共三原县委", "overlap_period": "2026"},

    # ── 县长-政府班子 ──
    {"id": 12, "person_a_id": 2, "person_b_id": 11, "type": "同僚", "context": "代县长与副县长共事", "overlap_org": "三原县人民政府", "overlap_period": "2026"},
    {"id": 13, "person_a_id": 2, "person_b_id": 12, "type": "同僚", "context": "代县长与副县长、公安局长共事", "overlap_org": "三原县人民政府", "overlap_period": "2026"},
    {"id": 14, "person_a_id": 2, "person_b_id": 13, "type": "同僚", "context": "代县长与副县长共事", "overlap_org": "三原县人民政府", "overlap_period": "2026"},
    {"id": 15, "person_a_id": 2, "person_b_id": 14, "type": "同僚", "context": "代县长与专家型副县长共事", "overlap_org": "三原县人民政府", "overlap_period": "2026"},

    # ── 人大/政协 ──
    {"id": 16, "person_a_id": 1, "person_b_id": 15, "type": "工作关系", "context": "县委书记与县人大主任", "overlap_org": "三原县", "overlap_period": "2026"},
    {"id": 17, "person_a_id": 1, "person_b_id": 19, "type": "工作关系", "context": "县委书记与县政协主席", "overlap_org": "三原县", "overlap_period": "2026"},

    # ── 前任链条 ──
    {"id": 18, "person_a_id": 23, "person_b_id": 2, "type": "前后任", "context": "赵俊强任县委书记时，段朋泊任县委副书记", "overlap_org": "中共三原县委", "overlap_period": "2025-2026"},
    {"id": 19, "person_a_id": 23, "person_b_id": 3, "type": "保存任免", "context": "赵俊强任县委书记时刘晖任宣传部长", "overlap_org": "中共三原县委", "overlap_period": "2025-2026"},
    {"id": 20, "person_a_id": 23, "person_b_id": 5, "type": "工作关系", "context": "赵俊强任县委书记时，田广军先后任宣传部长、纪委书记", "overlap_org": "中共三原县委", "overlap_period": "2025-2026"},

    # ── 提升链条 (田广军 宣传→纪委) ──
    {"id": 21, "person_a_id": 3, "person_b_id": 5, "type": "前后任", "context": "田广军接任宣传部长（由宣传部长升任纪委书记，宣传部长一职由刘朝接任）", "overlap_org": "中共三原县委宣传部", "overlap_period": ""},
]


# ── BUILD SQLITE DATABASE ────────────────────────────────────────────

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.executescript("""
CREATE TABLE persons (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    gender TEXT,
    ethnicity TEXT,
    birth TEXT,
    birthplace TEXT,
    education TEXT,
    party_join TEXT,
    work_start TEXT,
    current_post TEXT,
    current_org TEXT,
    source TEXT
);

CREATE TABLE organizations (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT,
    level TEXT,
    parent TEXT,
    location TEXT
);

CREATE TABLE positions (
    id INTEGER PRIMARY KEY,
    person_id INTEGER NOT NULL,
    org_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    start TEXT,
    end TEXT,
    rank TEXT,
    note TEXT,
    FOREIGN KEY (person_id) REFERENCES persons(id),
    FOREIGN KEY (org_id) REFERENCES organizations(id)
);

CREATE TABLE relationships (
    id INTEGER PRIMARY KEY,
    person_a_id INTEGER NOT NULL,
    person_b_id INTEGER NOT NULL,
    type TEXT NOT NULL,
    context TEXT,
    overlap_org TEXT,
    overlap_period TEXT,
    FOREIGN KEY (person_a_id) REFERENCES persons(id),
    FOREIGN KEY (person_b_id) REFERENCES persons(id)
);
""")

for p in persons:
    cur.execute("""INSERT INTO persons VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
                (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
                 p["birthplace"], p["education"], p["party_join"], p["work_start"],
                 p["current_post"], p["current_org"], p["source"]))

for o in organizations:
    cur.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""",
                (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

for pos in positions:
    cur.execute("""INSERT INTO positions VALUES (?,?,?,?,?,?,?,?)""",
                (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
                 pos["start"], pos["end"], pos["rank"], pos["note"]))

for r in relationships:
    cur.execute("""INSERT INTO relationships VALUES (?,?,?,?,?,?,?)""",
                (r["id"], r["person_a_id"], r["person_b_id"], r["type"],
                 r["context"], r["overlap_org"], r["overlap_period"]))

conn.commit()

# Summary stats
cur.execute("SELECT COUNT(*) FROM persons")
person_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM organizations")
org_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM positions")
pos_count = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM relationships")
rel_count = cur.fetchone()[0]

conn.close()
print(f"SQLite database written: {DB_PATH}")
print(f"  Persons: {person_count}")
print(f"  Organizations: {org_count}")
print(f"  Positions: {pos_count}")
print(f"  Relationships: {rel_count}")


# ── BUILD GEXF GRAPH ────────────────────────────────────────────────

today = datetime.now().strftime("%Y-%m-%d")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{today}">')
lines.append('    <creator>china-gov-network skill</creator>')
lines.append(f'    <description>三原县领导班子工作关系网络 - {today}</description>')
lines.append('  </meta>')
lines.append('  <graph mode="static" defaultedgetype="undirected">')

# ── Attributes ──
lines.append('    <attributes class="node">')
lines.append('      <attribute id="type" title="Type" type="string"/>')
lines.append('      <attribute id="category" title="Category" type="string"/>')
lines.append('      <attribute id="birth" title="Birth" type="string"/>')
lines.append('      <attribute id="birthplace" title="Birthplace" type="string"/>')
lines.append('      <attribute id="education" title="Education" type="string"/>')
lines.append('      <attribute id="current_post" title="Current Post" type="string"/>')
lines.append('      <attribute id="source" title="Source" type="string"/>')
lines.append('    </attributes>')
lines.append('    <attributes class="edge">')
lines.append('      <attribute id="type" title="Type" type="string"/>')
lines.append('      <attribute id="context" title="Context" type="string"/>')
lines.append('      <attribute id="period" title="Period" type="string"/>')
lines.append('    </attributes>')

# ── Nodes: Persons ──
lines.append('    <nodes>')
for p in persons:
    if p["id"] in [1, 23]:
        color = (255, 50, 50)   # red: 县委书记
        size = 20.0
    elif p["id"] in [2]:
        color = (50, 100, 255)  # blue: 政府领导(县长/代县长)
        size = 20.0
    elif p["id"] in [5]:
        color = (255, 165, 0)   # orange: 纪委书记
        size = 16.0
    elif p["id"] in [4, 11, 12, 13, 6, 14]:
        color = (50, 100, 255)  # blue: 政府领导
        size = 12.0
    else:
        color = (100, 100, 100) # grey: 其他
        size = 12.0

    lines.append(f'      <node id="{p["id"]}" label="{p["name"]}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="person"/>')
    lines.append(f'          <attvalue for="category" value="person"/>')
    lines.append(f'          <attvalue for="birth" value="{p["birth"]}"/>')
    lines.append(f'          <attvalue for="birthplace" value="{p["birthplace"]}"/>')
    lines.append(f'          <attvalue for="education" value="{p["education"]}"/>')
    lines.append(f'          <attvalue for="current_post" value="{p["current_post"]}"/>')
    lines.append(f'          <attvalue for="source" value="{p["source"]}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{color[0]}" g="{color[1]}" b="{color[2]}"/>')
    lines.append(f'        <viz:size value="{size}"/>')
    lines.append(f'      </node>')

# ── Nodes: Organizations ──
for o in organizations:
    oid = 1000 + o["id"]
    lines.append(f'      <node id="{oid}" label="{o["name"]}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="org"/>')
    lines.append(f'          <attvalue for="category" value="{o["type"]}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="44" g="62" b="80"/>')
    lines.append(f'        <viz:size value="8.0"/>')
    lines.append(f'      </node>')
lines.append('    </nodes>')

# ── Edges ──
lines.append('    <edges>')
edge_id = 1

# person→organization (worked_at)
for pos in positions:
    oid = 1000 + pos["org_id"]
    lines.append(f'      <edge id="{edge_id}" source="{pos["person_id"]}" target="{oid}" label="worked_at">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="worked_at"/>')
    lines.append(f'          <attvalue for="context" value="{pos["title"]}"/>')
    lines.append(f'          <attvalue for="period" value="{pos["start"] or "?"} → {pos["end"] or "今"}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')
    edge_id += 1

# person↔person (relationships)
for r in relationships:
    lines.append(f'      <edge id="{edge_id}" source="{r["person_a_id"]}" target="{r["person_b_id"]}" label="{r["type"]}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="{r["type"]}"/>')
    lines.append(f'          <attvalue for="context" value="{r["context"]}"/>')
    lines.append(f'          <attvalue for="period" value="{r["overlap_period"]}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')
    edge_id += 1

lines.append('    </edges>')
lines.append('  </graph>')
lines.append('</gexf>')

with open(GEXF_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

total_nodes = len(persons) + len(organizations)
total_edges = len(positions) + len(relationships)
print(f"\nGEXF graph written: {GEXF_PATH}")
print(f"  Nodes: {len(persons)} persons + {len(organizations)} organizations = {total_nodes} total")
print(f"  Edges: {len(positions)} worked_at + {len(relationships)} relationships = {total_edges} total")
print("\nDone!")