#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 理县 (Li County, Aba Prefecture, Sichuan) leadership network.

Data source: 理县人民政府 official leadership page (http://www.ablixian.gov.cn/lxrmzf/c100065/ldzc.shtml)
Accessed: 2026-08-03
"""

import sqlite3
import os
from datetime import datetime

STAGING = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(os.path.dirname(STAGING))
DB_PATH = os.path.join(STAGING, "理县_network.db")
GEXF_PATH = os.path.join(STAGING, "理县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ══════════════════════════════════════════════════════════════════
    # TOP LEADERS: Party Secretary & County Mayor
    # ══════════════════════════════════════════════════════════════════
    {"id": 1, "name": "杨健", "gender": "男", "ethnicity": "羌族",
     "birth": "1973-01", "birthplace": "", "education": "中央广播电视大学法学专业",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共理县县委书记", "current_org": "中共理县委员会",
     "source": "http://www.ablixian.gov.cn/lxrmzf/c100066/201908/a0844f4681b94730a6d8b2e6c4b1feb4.shtml"},
    {"id": 2, "name": "杜文钲", "gender": "男", "ethnicity": "汉族",
     "birth": "1979-04", "birthplace": "", "education": "四川大学工商管理学院企业管理专业硕士研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "理县县委副书记、县人民政府县长", "current_org": "理县人民政府",
     "source": "http://www.ablixian.gov.cn/lxrmzf/c100066/202111/d22c3fe53f244433abdb1c04cb6db00d.shtml"},

    # ══════════════════════════════════════════════════════════════════
    # DEPUTY PARTY SECRETARIES
    # ══════════════════════════════════════════════════════════════════
    {"id": 3, "name": "覃治", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "理县县委副书记", "current_org": "中共理县委员会",
     "source": "http://www.ablixian.gov.cn/lxrmzf/c100065/ldzc.shtml"},
    {"id": 4, "name": "邓志刚", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "理县县委副书记、朴头镇党委书记", "current_org": "中共理县委员会",
     "source": "http://www.ablixian.gov.cn/lxrmzf/c100065/ldzc.shtml"},

    # ══════════════════════════════════════════════════════════════════
    # PARTY STANDING COMMITTEE (县委常委)
    # ══════════════════════════════════════════════════════════════════
    {"id": 5, "name": "李凡", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "理县县委常委、政法委书记", "current_org": "中共理县委员会",
     "source": "http://www.ablixian.gov.cn/lxrmzf/c100065/ldzc.shtml"},
    {"id": 6, "name": "张静", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "理县县委常委、县纪委书记、县监委主任", "current_org": "中共理县纪律检查委员会",
     "source": "http://www.ablixian.gov.cn/lxrmzf/c100065/ldzc.shtml"},
    {"id": 7, "name": "秦元胜", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "理县县委常委、组织部部长", "current_org": "中共理县委员会组织部",
     "source": "http://www.ablixian.gov.cn/lxrmzf/c100065/ldzc.shtml"},
    {"id": 8, "name": "陈云", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "理县县委常委、统战部部长、县总工会主席", "current_org": "中共理县委员会统战部",
     "source": "http://www.ablixian.gov.cn/lxrmzf/c100065/ldzc.shtml"},
    {"id": 9, "name": "卓赛龙", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "理县县委常委、副县长（挂职）", "current_org": "理县人民政府",
     "source": "http://www.ablixian.gov.cn/lxrmzf/c100065/ldzc.shtml"},
    {"id": 10, "name": "颜贵军", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "理县县委常委、副县长", "current_org": "理县人民政府",
     "source": "http://www.ablixian.gov.cn/lxrmzf/c100065/ldzc.shtml"},
    {"id": 11, "name": "谢晓琴", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "理县县委常委、宣传部部长", "current_org": "中共理县委员会宣传部",
     "source": "http://www.ablixian.gov.cn/lxrmzf/c100065/ldzc.shtml"},
    {"id": 12, "name": "曾熠", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "理县县委常委、县人民政府党组副书记、副县长（分管常务工作）", "current_org": "理县人民政府",
     "source": "http://www.ablixian.gov.cn/lxrmzf/c100065/ldzc.shtml"},
    {"id": 13, "name": "张名举", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "理县县委常委、县人民武装部上校政治委员", "current_org": "理县人民武装部",
     "source": "http://www.ablixian.gov.cn/lxrmzf/c100065/ldzc.shtml"},
    {"id": 14, "name": "殷莉", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "理县县委常委", "current_org": "中共理县委员会",
     "source": "http://www.ablixian.gov.cn/lxrmzf/c100065/ldzc.shtml"},
    {"id": 15, "name": "任涛", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "理县县委常委、副县长（挂职）", "current_org": "理县人民政府",
     "source": "http://www.ablixian.gov.cn/lxrmzf/c100065/ldzc.shtml"},
    {"id": 16, "name": "赵瑞华", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "理县县委常委、副县长（挂职）", "current_org": "理县人民政府",
     "source": "http://www.ablixian.gov.cn/lxrmzf/c100065/ldzc.shtml"},

    # ══════════════════════════════════════════════════════════════════
    # GOVERNMENT DEPUTY HEADS (副县长)
    # ══════════════════════════════════════════════════════════════════
    {"id": 17, "name": "泽周", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "理县副县长、公安局局长", "current_org": "理县人民政府",
     "source": "http://www.ablixian.gov.cn/lxrmzf/c100065/ldzc.shtml"},
    {"id": 18, "name": "旦真泽仁", "gender": "男", "ethnicity": "藏族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "理县副县长", "current_org": "理县人民政府",
     "source": "http://www.ablixian.gov.cn/lxrmzf/c100065/ldzc.shtml"},
    {"id": 19, "name": "许志刚", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "理县副县长", "current_org": "理县人民政府",
     "source": "http://www.ablixian.gov.cn/lxrmzf/c100065/ldzc.shtml"},
    {"id": 20, "name": "代红", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "理县副县长", "current_org": "理县人民政府",
     "source": "http://www.ablixian.gov.cn/lxrmzf/c100065/ldzc.shtml"},
    {"id": 21, "name": "王双", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "理县副县长", "current_org": "理县人民政府",
     "source": "http://www.ablixian.gov.cn/lxrmzf/c100065/ldzc.shtml"},
    {"id": 22, "name": "银波", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "理县副县长", "current_org": "理县人民政府",
     "source": "http://www.ablixian.gov.cn/lxrmzf/c100065/ldzc.shtml"},

    # ══════════════════════════════════════════════════════════════════
    # PEOPLE'S CONGRESS (人大常委会)
    # ══════════════════════════════════════════════════════════════════
    {"id": 23, "name": "蒋明平", "gender": "男", "ethnicity": "汉族",
     "birth": "1969-05", "birthplace": "", "education": "中央广播电视大学法律专业",
     "party_join": "中共党员", "work_start": "",
     "current_post": "理县人大常委会党组书记、主任", "current_org": "理县人大常委会",
     "source": "http://www.ablixian.gov.cn/lxrmzf/c100065/ldzc.shtml"},
    {"id": 24, "name": "丁龙华", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "理县人大常委会党组副书记、副主任", "current_org": "理县人大常委会",
     "source": "http://www.ablixian.gov.cn/lxrmzf/c100065/ldzc.shtml"},
    {"id": 25, "name": "甘先群", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "理县人大常委会副主任", "current_org": "理县人大常委会",
     "source": "http://www.ablixian.gov.cn/lxrmzf/c100065/ldzc.shtml"},
    {"id": 26, "name": "雷琪", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "理县人大常委会党组成员、副主任", "current_org": "理县人大常委会",
     "source": "http://www.ablixian.gov.cn/lxrmzf/c100065/ldzc.shtml"},
    {"id": 27, "name": "朱继兵", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "理县人大常委会党组成员、副主任", "current_org": "理县人大常委会",
     "source": "http://www.ablixian.gov.cn/lxrmzf/c100065/ldzc.shtml"},

    # ══════════════════════════════════════════════════════════════════
    # CPPCC (政协)
    # ══════════════════════════════════════════════════════════════════
    {"id": 28, "name": "熊伟", "gender": "男", "ethnicity": "藏族",
     "birth": "1971-10", "birthplace": "", "education": "四川省委党校函授学院行政管理专业",
     "party_join": "中共党员", "work_start": "",
     "current_post": "理县政协党组副书记、副主席", "current_org": "政协理县委员会",
     "source": "http://www.ablixian.gov.cn/lxrmzf/c100065/ldzc.shtml"},
    {"id": 29, "name": "骆俊", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "理县政协党组成员、副主席", "current_org": "政协理县委员会",
     "source": "http://www.ablixian.gov.cn/lxrmzf/c100065/ldzc.shtml"},
    {"id": 30, "name": "余建英", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "理县政协党组成员、副主席", "current_org": "政协理县委员会",
     "source": "http://www.ablixian.gov.cn/lxrmzf/c100065/ldzc.shtml"},
    {"id": 31, "name": "孙春艳", "gender": "女", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "理县政协副主席", "current_org": "政协理县委员会",
     "source": "http://www.ablixian.gov.cn/lxrmzf/c100065/ldzc.shtml"},
]

organizations = [
    {"id": 1, "name": "中共理县委员会", "type": "党委", "level": "县处级", "parent": "中共阿坝州委员会", "location": "四川阿坝州理县"},
    {"id": 2, "name": "理县人民政府", "type": "政府", "level": "县处级", "parent": "阿坝州人民政府", "location": "四川阿坝州理县"},
    {"id": 3, "name": "中共理县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共阿坝州纪律检查委员会", "location": "四川阿坝州理县"},
    {"id": 4, "name": "中共理县委员会组织部", "type": "党委", "level": "县处级", "parent": "中共理县委员会", "location": "四川阿坝州理县"},
    {"id": 5, "name": "中共理县委员会宣传部", "type": "党委", "level": "县处级", "parent": "中共理县委员会", "location": "四川阿坝州理县"},
    {"id": 6, "name": "中共理县委员会统战部", "type": "党委", "level": "县处级", "parent": "中共理县委员会", "location": "四川阿坝州理县"},
    {"id": 7, "name": "中共理县委员会政法委员会", "type": "党委", "level": "县处级", "parent": "中共理县委员会", "location": "四川阿坝州理县"},
    {"id": 8, "name": "理县人民武装部", "type": "军事", "level": "县处级", "parent": "阿坝州军分区", "location": "四川阿坝州理县"},
    {"id": 9, "name": "理县人大常委会", "type": "人大", "level": "县处级", "parent": "阿坝州人大常委会", "location": "四川阿坝州理县"},
    {"id": 10, "name": "政协理县委员会", "type": "政协", "level": "县处级", "parent": "政协阿坝州委员会", "location": "四川阿坝州理县"},
    {"id": 11, "name": "理县公安局", "type": "政府", "level": "县处级", "parent": "理县人民政府", "location": "四川阿坝州理县"},
    {"id": 12, "name": "理县总工会", "type": "群团", "level": "县处级", "parent": "理县委员会", "location": "四川阿坝州理县"},
    {"id": 13, "name": "朴头镇党委", "type": "党委", "level": "乡镇级", "parent": "中共理县委员会", "location": "四川阿坝州理县朴头镇"},
]

positions = [
    # ── Yang Jian (杨健) ──
    {"id": 1, "person_id": 1, "org_id": 1, "title": "中共理县县委书记", "start": "", "end": "", "rank": "县处级正职", "note": "现任，主持县委全面工作。1973年1月生，羌族"},

    # ── Du Wenzheng (杜文钲) ──
    {"id": 2, "person_id": 2, "org_id": 2, "title": "理县县委副书记、县长", "start": "", "end": "", "rank": "县处级正职", "note": "现任，主持县政府全面工作。1979年4月生，汉族，四川大学工商管理硕士"},
    {"id": 3, "person_id": 2, "org_id": 1, "title": "理县县委副书记", "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # ─── Qin Zhi (覃治) ──
    {"id": 4, "person_id": 3, "org_id": 1, "title": "理县县委副书记", "start": "", "end": "", "rank": "县处级副职", "note": "协助县委日常事务、抓党的建设工作"},

    # ─── Deng Zhigang (邓志刚) ──
    {"id": 5, "person_id": 4, "org_id": 1, "title": "理县县委副书记", "start": "", "end": "", "rank": "县处级副职", "note": "分工负责毕棚沟景区建设、理小路交旅融合"},
    {"id": 6, "person_id": 4, "org_id": 13, "title": "朴头镇党委书记", "start": "", "end": "", "rank": "乡镇级正职", "note": ""},

    # ─── Li Fan (李凡) ──
    {"id": 7, "person_id": 5, "org_id": 7, "title": "理县县委常委、政法委书记", "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # ─── Zhang Jing (张静) ──
    {"id": 8, "person_id": 6, "org_id": 3, "title": "理县县委常委、县纪委书记、县监委主任", "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # ─── Qin Yuansheng (秦元胜) ──
    {"id": 9, "person_id": 7, "org_id": 4, "title": "理县县委常委、组织部部长", "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # ─── Chen Yun (陈云) ──
    {"id": 10, "person_id": 8, "org_id": 6, "title": "理县县委常委、统战部部长", "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # ─── Zhuo Sailong (卓赛龙) ──
    {"id": 11, "person_id": 9, "org_id": 2, "title": "理县县委常委、副县长（挂职）", "start": "", "end": "", "rank": "县处级副职", "note": "挂职干部，负责东西部协作和对口支援"},

    # ─── Yan Guijun (颜贵军) ──
    {"id": 12, "person_id": 10, "org_id": 2, "title": "理县县委常委、副县长", "start": "", "end": "", "rank": "县处级副职", "note": "负责林草、生态环境"},

    # ─── Xie Xiaoqin (谢晓琴) ──
    {"id": 13, "person_id": 11, "org_id": 5, "title": "理县县委常委、宣传部部长", "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # ─── Zeng Yi (曾熠) ──
    {"id": 14, "person_id": 12, "org_id": 2, "title": "理县县委常委、副县长（分管常务工作）", "start": "", "end": "", "rank": "县处级副职", "note": "负责县政府常务工作"},

    # ─── Zhang Mingju (张名举) ──
    {"id": 15, "person_id": 13, "org_id": 8, "title": "理县县委常委、县人民武装部上校政治委员", "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # ─── Yin Li (殷莉) ──
    {"id": 16, "person_id": 14, "org_id": 1, "title": "理县县委常委", "start": "", "end": "", "rank": "县处级副职", "note": "分工负责项目投资建设管理"},

    # ─── Ren Tao (任涛) ──
    {"id": 17, "person_id": 15, "org_id": 2, "title": "理县县委常委、副县长（挂职）", "start": "", "end": "", "rank": "县处级副职", "note": "省内对口帮扶挂职"},

    # ─── Zhao Ruihua (赵瑞华) ──
    {"id": 18, "person_id": 16, "org_id": 2, "title": "理县县委常委、副县长（挂职）", "start": "", "end": "", "rank": "县处级副职", "note": "中央定点扶贫挂职"},

    # ─── Ze Zhou (泽周) ──
    {"id": 19, "person_id": 17, "org_id": 11, "title": "理县副县长、公安局局长", "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # ─── Dan Zhenzeren (旦真泽仁) ──
    {"id": 20, "person_id": 18, "org_id": 2, "title": "理县副县长", "start": "", "end": "", "rank": "县处级副职", "note": "负责自然资源、住房城乡建设"},

    # ─── Xu Zhigang (许志刚) ──
    {"id": 21, "person_id": 19, "org_id": 2, "title": "理县副县长", "start": "", "end": "", "rank": "县处级副职", "note": "负责卫生健康、市场监管"},

    # ─── Dai Hong (代红) ──
    {"id": 22, "person_id": 20, "org_id": 2, "title": "理县副县长", "start": "", "end": "", "rank": "县处级副职", "note": "负责教育、体育、文旅"},

    # ─── Wang Shuang (王双) ──
    {"id": 23, "person_id": 21, "org_id": 2, "title": "理县副县长", "start": "", "end": "", "rank": "县处级副职", "note": "负责发改、经信、招商引资"},

    # ─── Yin Bo (银波) ──
    {"id": 24, "person_id": 22, "org_id": 2, "title": "理县副县长", "start": "", "end": "", "rank": "县处级副职", "note": "负责农业农村、水利、交通运输"},

    # ─── Jiang Mingping (蒋明平) ──
    {"id": 25, "person_id": 23, "org_id": 9, "title": "理县人大常委会党组书记、主任", "start": "", "end": "", "rank": "县处级正职", "note": "1969年5月生"},

    # ─── Ding Longhua (丁龙华) ──
    {"id": 26, "person_id": 24, "org_id": 9, "title": "理县人大常委会党组副书记、副主任", "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # ─── Gan Xianqun (甘先群) ──
    {"id": 27, "person_id": 25, "org_id": 9, "title": "理县人大常委会副主任", "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # ─── Lei Qi (雷琪) ──
    {"id": 28, "person_id": 26, "org_id": 9, "title": "理县人大常委会党组成员、副主任", "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # ─── Zhu Jibing (朱继兵) ──
    {"id": 29, "person_id": 27, "org_id": 9, "title": "理县人大常委会党组成员、副主任", "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # ─── Xiong Wei (熊伟) ──
    {"id": 30, "person_id": 28, "org_id": 10, "title": "理县政协党组副书记、副主席", "start": "", "end": "", "rank": "县处级副职", "note": "1971年10月生，藏族"},

    # ─── Luo Jun (骆俊) ──
    {"id": 31, "person_id": 29, "org_id": 10, "title": "理县政协党组成员、副主席", "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # ─── Yu Jianying (余建英) ──
    {"id": 32, "person_id": 30, "org_id": 10, "title": "理县政协党组成员、副主席", "start": "", "end": "", "rank": "县处级副职", "note": ""},

    # ─── Sun Chunyan (孙春艳) ──
    {"id": 33, "person_id": 31, "org_id": 10, "title": "理县政协副主席", "start": "", "end": "", "rank": "县处级副职", "note": ""},
]

relationships = [
    # ── 党政主要领导 (Party Secretary ↔ County Mayor) ──
    {"id": 1, "person_a_id": 1, "person_b_id": 2, "type": "党政搭档", "context": "杨健（县委书记）与杜文钲（县长）为现任理县党政主要领导搭档", "overlap_org": "中共理县委员会/理县人民政府", "overlap_period": "当前"},

    # ── 县委副书记们 ──
    {"id": 2, "person_a_id": 3, "person_b_id": 2, "type": "同僚", "context": "覃治（县委副书记）与杜文钲（县委副书记/县长）同为副书记", "overlap_org": "中共理县委员会", "overlap_period": "当前"},
    {"id": 3, "person_a_id": 4, "person_b_id": 2, "type": "同僚", "context": "邓志刚（县委副书记）与杜文钲（县委副书记/县长）同为副书记", "overlap_org": "中共理县委员会", "overlap_period": "当前"},
    {"id": 4, "person_a_id": 3, "person_b_id": 4, "type": "同僚", "context": "覃治与邓志刚同为理县县委副书记", "overlap_org": "中共理县委员会", "overlap_period": "当前"},

    # ── 县委常委之间的关系 ──
    {"id": 5, "person_a_id": 1, "person_b_id": 5, "type": "上下级", "context": "杨健（县委书记）与李凡（政法委书记）", "overlap_org": "中共理县委员会", "overlap_period": "当前"},
    {"id": 6, "person_a_id": 1, "person_b_id": 6, "type": "上下级", "context": "杨健（县委书记）与张静（纪委书记）", "overlap_org": "中共理县委员会", "overlap_period": "当前"},
    {"id": 7, "person_a_id": 1, "person_b_id": 7, "type": "上下级", "context": "杨健（县委书记）与秦元胜（组织部长）", "overlap_org": "中共理县委员会", "overlap_period": "当前"},

    # ── 副县长与县长 ──
    {"id": 8, "person_a_id": 2, "person_b_id": 12, "type": "上下级", "context": "杜文钲（县长）与曾熠（常务副县长）", "overlap_org": "理县人民政府", "overlap_period": "当前"},
    {"id": 9, "person_a_id": 2, "person_b_id": 17, "type": "上下级", "context": "杜文钲（县长）与泽周（副县长/公安局长）", "overlap_org": "理县人民政府", "overlap_period": "当前"},
    {"id": 10, "person_a_id": 2, "person_b_id": 20, "type": "上下级", "context": "杜文钲（县长）与代红（副县长）", "overlap_org": "理县人民政府", "overlap_period": "当前"},

    # ── 挂职县官 ──
    {"id": 11, "person_a_id": 9, "person_b_id": 15, "type": "同僚", "context": "卓赛龙（挂职）与任涛（挂职）同为挂职副县长", "overlap_org": "理县人民政府", "overlap_period": "当前"},
    {"id": 12, "person_a_id": 9, "person_b_id": 16, "type": "同僚", "context": "卓赛龙（挂职）与赵瑞华（挂职）同为挂职副县长", "overlap_org": "理县人民政府", "overlap_period": "当前"},

    # ── 人大与党委 ──
    {"id": 13, "person_a_id": 1, "person_b_id": 23, "type": "工作关系", "context": "杨健联系县人大蒋明平（人大常委会主任）", "overlap_org": "中共理县委员会/理县人大常委会", "overlap_period": "当前"},

    # ── 县委常委班子 ──
    {"id": 14, "person_a_id": 7, "person_b_id": 11, "type": "同僚", "context": "秦元胜（组织部长）与谢晓琴（宣传部长）同为县委常委", "overlap_org": "中共理县委员会", "overlap_period": "当前"},
    {"id": 15, "person_a_id": 12, "person_b_id": 8, "type": "同僚", "context": "曾熠（常务副县长）与陈云（统战部长）同为县委常委", "overlap_org": "中共理县委员会", "overlap_period": "当前"},
]

# ── BUILD SQLite DATABASE ────────────────────────────────────────────

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
                 p.get("birthplace", ""), p.get("education", ""), p.get("party_join", ""), p.get("work_start", ""),
                 p["current_post"], p["current_org"], p["source"]))

for o in organizations:
    cur.execute("""INSERT INTO organizations VALUES (?,?,?,?,?,?)""",
                (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o.get("location", "")))

for pos in positions:
    cur.execute("""INSERT INTO positions VALUES (?,?,?,?,?,?,?,?)""",
                (pos["id"], pos["person_id"], pos["org_id"], pos["title"],
                 pos.get("start", ""), pos.get("end", ""), pos.get("rank", ""), pos.get("note", "")))

for r in relationships:
    cur.execute("""INSERT INTO relationships VALUES (?,?,?,?,?,?,?)""",
                (r["id"], r["person_a_id"], r["person_b_id"], r["type"],
                 r.get("context", ""), r.get("overlap_org", ""), r.get("overlap_period", "")))

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

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

lines = []
lines.append('<?xml version="1.0" encoding="UTF-8"?>')
lines.append(f'<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
lines.append(f'  <meta lastmodifieddate="{today}">')
lines.append('    <creator>china-gov-network skill</creator>')
lines.append(f'    <description>理县领导班成员工作关系网络 - {today}</description>')
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
    pid = p["id"]
    if pid == 1:
        color = (255, 50, 50)    # Red: Party Secretary
        size = 20.0
    elif pid == 2:
        color = (50, 100, 255)   # Blue: Government leader (mayor)
        size = 20.0
    elif pid == 6:
        color = (255, 165, 0)    # Orange: Discipline Inspection
        size = 12.0
    elif pid in [3, 4]:
        color = (100, 100, 100)  # Grey: deputy secretary
        size = 12.0
    elif 5 <= pid <= 16:
        color = (100, 100, 100)  # Grey: 县委常委
        size = 12.0
    elif 17 <= pid <= 22:
        color = (50, 100, 255)   # Blue: government deputies
        size = 12.0
    elif 23 <= pid <= 27:
        color = (200, 255, 255)  # Cyan: 人大
        size = 10.0
    elif 28 <= pid <= 31:
        color = (255, 240, 200)  # Cream: 政协
        size = 10.0
    else:
        color = (100, 100, 100)
        size = 12.0

    lines.append(f'      <node id="{pid}" label="{esc(p["name"])}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="person"/>')
    lines.append(f'          <attvalue for="category" value="person"/>')
    lines.append(f'          <attvalue for="birth" value="{esc(p.get("birth", ""))}"/>')
    lines.append(f'          <attvalue for="birthplace" value="{esc(p.get("birthplace", ""))}"/>')
    lines.append(f'          <attvalue for="education" value="{esc(p.get("education", ""))}"/>')
    lines.append(f'          <attvalue for="current_post" value="{esc(p["current_post"])}"/>')
    lines.append(f'          <attvalue for="source" value="{esc(p.get("source", ""))}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{color[0]}" g="{color[1]}" b="{color[2]}"/>')
    lines.append(f'        <viz:size value="{size}"/>')
    lines.append(f'      </node>')

# ── Nodes: Organizations ──
org_colors = {
    "党委": (255, 200, 200),
    "政府": (200, 200, 255),
    "军事": (220, 220, 220),
    "人大": (200, 255, 255),
    "政协": (255, 240, 200),
    "群团": (255, 220, 255),
}
for o in organizations:
    oid = 1000 + o["id"]
    oc = org_colors.get(o["type"], (200, 200, 200))
    lines.append(f'      <node id="{oid}" label="{esc(o["name"])}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="org"/>')
    lines.append(f'          <attvalue for="category" value="{esc(o["type"])}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'        <viz:color r="{oc[0]}" g="{oc[1]}" b="{oc[2]}"/>')
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
    lines.append(f'          <attvalue for="context" value="{esc(pos["title"])}"/>')
    lines.append(f'          <attvalue for="period" value="{pos.get("start","?")} → {pos.get("end","今")}"/>')
    lines.append(f'        </attvalues>')
    lines.append(f'      </edge>')
    edge_id += 1

# person↔person (relationships)
for r in relationships:
    lines.append(f'      <edge id="{edge_id}" source="{r["person_a_id"]}" target="{r["person_b_id"]}" label="{esc(r["type"])}">')
    lines.append(f'        <attvalues>')
    lines.append(f'          <attvalue for="type" value="{esc(r["type"])}"/>')
    lines.append(f'          <attvalue for="context" value="{esc(r.get("context",""))}"/>')
    lines.append(f'          <attvalue for="period" value="{esc(r.get("overlap_period",""))}"/>')
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