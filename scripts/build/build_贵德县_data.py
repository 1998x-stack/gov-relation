#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for Guide County (贵德县),
Hainan Tibetan Autonomous Prefecture (海南藏族自治州), Qinghai (青海省).

task_id: qinghai_贵德县
targets: 县委书记 & 县长 (李正业 as 县委书记; 张有强 as 县委副书记、县长)

Research as-of: 2026-08-07 (based on official guide.gov.cn 领导之窗/新闻, hainanzhou.gov.cn,
and media). Generic web search engines (Exa/Baidu/Sogou/360) were rate-limited or
captcha-blocked in the research environment, so career timelines are partial. Durations
and personal fields that could not be verified are marked unknown; uncertainty is
preserved in the person JSON open_questions and the report open gaps, not fabricated.
"""

import sqlite3
import os
from datetime import datetime

BASE = "/workspace/data/xieming/other-codes/gov-relation"
TMP = os.path.join(BASE, "data/tmp/qinghai_贵德县")
DB_PATH = os.path.join(TMP, "贵德县_network.db")
GEXF_PATH = os.path.join(TMP, "贵德县_network.gexf")

# ── DATA ─────────────────────────────────────────────────────────────

persons = [
    # ── Current Top Leaders ──
    {"id": 1, "name": "李正业", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "贵德县委书记", "current_org": "中共贵德县委员会",
     "source": "https://www.guide.gov.cn/xwbd/bxxw/content_1013654286"},
    {"id": 2, "name": "张有强", "gender": "男", "ethnicity": "汉族",
     "birth": "1978-11", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员(2008-10入党)", "work_start": "2004-04",
     "current_post": "贵德县委副书记、县人民政府县长、党组书记", "current_org": "贵德县人民政府",
     "source": "https://www.guide.gov.cn/zwgk/fdzdgknr/jgjj/zfld/content_1013648384"},

    # ── 县委副书记 ──
    {"id": 3, "name": "华列", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "贵德县委副书记", "current_org": "中共贵德县委员会",
     "source": "https://www.guide.gov.cn/xwbd/bxxw/content_1013654286"},
    {"id": 4, "name": "韩贵军", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "贵德县委副书记", "current_org": "中共贵德县委员会",
     "source": "https://www.guide.gov.cn/xwbd/bxxw/content_1013654286"},
    {"id": 5, "name": "卢林", "gender": "男", "ethnicity": "汉族",
     "birth": "1985-08", "birthplace": "", "education": "研究生",
     "party_join": "中共党员(2004-12入党)", "work_start": "2007-07",
     "current_post": "贵德县委副书记、县人民政府副县长（援青）", "current_org": "贵德县人民政府",
     "source": "https://www.guide.gov.cn/zwgk/fdzdgknr/jgjj/zfld/content_1013650273"},
    {"id": 6, "name": "梁祎", "gender": "男", "ethnicity": "汉族",
     "birth": "1983-07", "birthplace": "", "education": "大学工学学士",
     "party_join": "中共党员(2007-12入党)", "work_start": "2006-07",
     "current_post": "贵德县委副书记、县人民政府副县长（援青）", "current_org": "贵德县人民政府",
     "source": "https://www.guide.gov.cn/zwgk/fdzdgknr/jgjj/zfld/content_1013650274"},

    # ── 政府领导 ──
    {"id": 7, "name": "扎西尼玛", "gender": "男", "ethnicity": "藏族",
     "birth": "1980-07", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员(2009-07入党)", "work_start": "2005-11",
     "current_post": "贵德县委常委、县人民政府副县长、党组副书记", "current_org": "贵德县人民政府",
     "source": "https://www.guide.gov.cn/zwgk/fdzdgknr/jgjj/zfld/content_1013654112"},
    {"id": 8, "name": "徐瑞", "gender": "女", "ethnicity": "汉族",
     "birth": "1986-02", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员(2013-01入党)", "work_start": "2008-11",
     "current_post": "贵德县人民政府副县长、党组成员", "current_org": "贵德县人民政府",
     "source": "https://www.guide.gov.cn/zwgk/fdzdgknr/jgjj/zfld/content_1013654113"},
    {"id": 9, "name": "才太本", "gender": "男", "ethnicity": "藏族",
     "birth": "1982-12", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员(2011-04入党)", "work_start": "2007-10",
     "current_post": "贵德县人民政府副县长、党组成员", "current_org": "贵德县人民政府",
     "source": "https://www.guide.gov.cn/zwgk/fdzdgknr/jgjj/zfld/content_1013650857"},
    {"id": 10, "name": "张志愿", "gender": "男", "ethnicity": "汉族",
     "birth": "1982-06", "birthplace": "", "education": "在职大学",
     "party_join": "中共党员(2011-07入党)", "work_start": "2001-12",
     "current_post": "贵德县人民政府副县长、党组成员，县公安局党委书记、局长", "current_org": "贵德县公安局/贵德县人民政府",
     "source": "https://www.guide.gov.cn/zwgk/fdzdgknr/jgjj/zfld/content_1013653244"},
    {"id": 11, "name": "刘大庆", "gender": "男", "ethnicity": "汉族",
     "birth": "1981-03", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员(2008-06入党)", "work_start": "2005-11",
     "current_post": "贵德县人民政府副县长、党组成员", "current_org": "贵德县人民政府",
     "source": "https://www.guide.gov.cn/zwgk/fdzdgknr/jgjj/zfld/content_1013654114"},
    {"id": 12, "name": "师海成", "gender": "男", "ethnicity": "汉族",
     "birth": "1975-11", "birthplace": "", "education": "大学学历",
     "party_join": "中共党员(2003-07入党)", "work_start": "1994-07",
     "current_post": "贵德县人民政府副县长、党组成员", "current_org": "贵德县人民政府",
     "source": "https://www.guide.gov.cn/zwgk/fdzdgknr/jgjj/zfld/content_1013654115"},
    {"id": 13, "name": "郑凯", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "贵德县人民政府副县长（挂职）", "current_org": "贵德县人民政府",
     "source": "https://www.guide.gov.cn/zwgk/fdzdgknr/jgjj/zfld"},

    # ── 县委常委（其他） ──
    {"id": 14, "name": "赵统英", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "贵德县委常委", "current_org": "中共贵德县委员会",
     "source": "https://www.guide.gov.cn/xwbd/bxxw/content_1013654286"},
    {"id": 15, "name": "游桂亭", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "贵德县委常委", "current_org": "中共贵德县委员会",
     "source": "https://www.guide.gov.cn/xwbd/bxxw/content_1013654286"},
    {"id": 16, "name": "曹锐宁", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "贵德县委常委", "current_org": "中共贵德县委员会",
     "source": "https://www.guide.gov.cn/xwbd/bxxw/content_1013654286"},
    {"id": 17, "name": "华秀才让", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "贵德县委常委", "current_org": "中共贵德县委员会",
     "source": "https://www.guide.gov.cn/xwbd/bxxw/content_1013654286"},
    {"id": 18, "name": "魏强", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "贵德县委常委", "current_org": "中共贵德县委员会",
     "source": "https://www.guide.gov.cn/xwbd/bxxw/content_1013654286"},

    # ── 海南州层级（网络背景） ──
    {"id": 19, "name": "熊元来", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "海南州委书记", "current_org": "中共海南藏族自治州委员会",
     "source": "https://www.hainanzhou.gov.cn/"},
    {"id": 20, "name": "当周", "gender": "男", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "海南州委副书记、州政府代理州长", "current_org": "海南藏族自治州人民政府",
     "source": "https://www.hainanzhou.gov.cn/"},
    {"id": 21, "name": "戴敏捷", "gender": "男", "ethnicity": "汉族",
     "birth": "1972-02", "birthplace": "", "education": "研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "省政府副秘书长、海南州委副书记、州政府副州长", "current_org": "海南藏族自治州人民政府",
     "source": "https://www.hainanzhou.gov.cn/zwgk/fdzdgknr/jgjj/zzfld"},
]

organizations = [
    {"id": 1, "name": "中共贵德县委员会", "type": "党委", "level": "县处级",
     "parent": "中共海南藏族自治州委员会", "location": "青海省海南藏族自治州贵德县"},
    {"id": 2, "name": "贵德县人民政府", "type": "政府", "level": "县处级",
     "parent": "海南藏族自治州人民政府", "location": "青海省海南藏族自治州贵德县"},
    {"id": 3, "name": "贵德县公安局", "type": "政府", "level": "乡科级",
     "parent": "海南藏族自治州公安局", "location": "青海省海南藏族自治州贵德县"},
    {"id": 4, "name": "贵德县人民代表大会常务委员会", "type": "人大", "level": "县处级",
     "parent": "海南藏族自治州人大常委会", "location": "青海省海南藏族自治州贵德县"},
    {"id": 5, "name": "中国人民政治协商会议贵德县委员会", "type": "政协", "level": "县处级",
     "parent": "政协海南藏族自治州委员会", "location": "青海省海南藏族自治州贵德县"},
    {"id": 6, "name": "中共海南藏族自治州委员会", "type": "党委", "level": "地厅级",
     "parent": "中共青海省委员会", "location": "青海省海南藏族自治州"},
    {"id": 7, "name": "海南藏族自治州人民政府", "type": "政府", "level": "地厅级",
     "parent": "青海省人民政府", "location": "青海省海南藏族自治州"},
]

positions = [
    # ── 李正业 县委书记 ──
    {"person_id": 1, "org_id": 1, "title": "贵德县委书记", "start": "", "end": "present", "rank": "正县级",
     "note": "2026-07-19 县委十八届一次全会当选，连任（第十七届已在任）；2026-08-04 主持十八届县委第一次常委会会议"},
    {"person_id": 1, "org_id": 0, "title": "履历缺口", "start": "unknown", "end": "unknown", "rank": "",
     "note": "公开可及官方源未公布任县委书记前的完整履历（出生、籍贯、学历、此前职务均待核实）"},

    # ── 张有强 县长 ──
    {"person_id": 2, "org_id": 2, "title": "贵德县人民政府县长、党组书记", "start": "", "end": "present", "rank": "正县级",
     "note": "主持县政府全面工作，负责审计；任县长前的此前履历与具体到任日期待核实"},
    {"person_id": 2, "org_id": 1, "title": "贵德县委副书记", "start": "", "end": "present", "rank": "县处级",
     "note": "2026-07-19 当选十八届县委副书记"},

    # ── 县委副书记 ──
    {"person_id": 3, "org_id": 1, "title": "贵德县委副书记", "start": "2026-07-19", "end": "present", "rank": "县处级",
     "note": "2026-07-19 县委十八届一次全会当选副书记"},
    {"person_id": 4, "org_id": 1, "title": "贵德县委副书记", "start": "2026-07-19", "end": "present", "rank": "县处级",
     "note": "2026-07-19 县委十八届一次全会当选副书记"},
    {"person_id": 5, "org_id": 2, "title": "贵德县委副书记、副县长（援青）", "start": "", "end": "present", "rank": "县处级",
     "note": "援青干部；负责旅游开发、教育、招商引资、对口支援"},
    {"person_id": 6, "org_id": 2, "title": "贵德县委副书记、副县长（援青）", "start": "", "end": "present", "rank": "县处级",
     "note": "援青干部；负责水利、库区移民安置、数字经济、政务服务"},

    # ── 政府领导 ──
    {"person_id": 7, "org_id": 2, "title": "县政府副县长、党组副书记（常务）", "start": "", "end": "present", "rank": "副县级",
     "note": "负责县政府日常工作，分管发改、应急、招商、国资等"},
    {"person_id": 8, "org_id": 2, "title": "县人民政府副县长", "start": "", "end": "present", "rank": "副县级",
     "note": "负责生态环境、卫生健康、人社医保、创卫"},
    {"person_id": 9, "org_id": 2, "title": "县人民政府副县长", "start": "", "end": "present", "rank": "副县级",
     "note": "负责自然资源、林业草原、城乡建设、城市管理"},
    {"person_id": 10, "org_id": 2, "title": "县人民政府副县长", "start": "", "end": "present", "rank": "副县级",
     "note": "负责公安、民族宗教、司法、市监、综合行政执法"},
    {"person_id": 10, "org_id": 3, "title": "县公安局党委书记、局长", "start": "", "end": "present", "rank": "正科级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "县人民政府副县长", "start": "", "end": "present", "rank": "副县级",
     "note": "负责农牧（乡村振兴）、交通、房屋征收、供销"},
    {"person_id": 12, "org_id": 2, "title": "县人民政府副县长", "start": "", "end": "present", "rank": "副县级",
     "note": "负责财政税务、文旅体广、民政、退役军人事务"},
    {"person_id": 13, "org_id": 2, "title": "县人民政府副县长（挂职）", "start": "", "end": "present", "rank": "副县级",
     "note": "挂职；负责海南州可持续发展议程创新示范区及黄河高质量发展实验室建设协作"},

    # ── 其他县委常委会成员 ──
    {"person_id": 14, "org_id": 1, "title": "县委常委", "start": "2026-07-19", "end": "present", "rank": "县处级",
     "note": "十八届县委常委会委员"},
    {"person_id": 15, "org_id": 1, "title": "县委常委", "start": "2026-07-19", "end": "present", "rank": "县处级",
     "note": "十八届县委常委会委员"},
    {"person_id": 16, "org_id": 1, "title": "县委常委", "start": "2026-07-19", "end": "present", "rank": "县处级",
     "note": "十八届县委常委会委员"},
    {"person_id": 17, "org_id": 1, "title": "县委常委", "start": "2026-07-19", "end": "present", "rank": "县处级",
     "note": "十八届县委常委会委员"},
    {"person_id": 18, "org_id": 1, "title": "县委常委", "start": "2026-07-19", "end": "present", "rank": "县处级",
     "note": "十八届县委常委会委员"},

    # ── 海南州层级 ──
    {"person_id": 19, "org_id": 6, "title": "海南州委书记", "start": "", "end": "present", "rank": "正厅级", "note": ""},
    {"person_id": 20, "org_id": 7, "title": "海南州委副书记、州政府代理州长", "start": "", "end": "present", "rank": "正厅级", "note": ""},
    {"person_id": 21, "org_id": 7, "title": "省政府副秘书长、海南州委副书记、副州长", "start": "", "end": "present", "rank": "副厅级",
     "note": "对口支援、东西部协作、招商引资分工；跨省/省直交流干部"},
    {"person_id": 21, "org_id": 6, "title": "海南州委副书记", "start": "", "end": "present", "rank": "副厅级", "note": ""},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "strength": "strong",
     "context": "李正业任县委书记，张有强任县委副书记、县长，为党政一把手搭档",
     "overlap_org": "中共贵德县委员会/贵德县人民政府",
     "overlap_period": "至今（2026-07 连任）", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 3, "type": "overlap", "strength": "strong",
     "context": "李正业与华列同任十八届县委常委会，华列任县委副书记",
     "overlap_org": "中共贵德县委员会",
     "overlap_period": "2026-07-19至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "strength": "strong",
     "context": "李正业与韩贵军同任十八届县委常委会，韩贵军任县委副书记",
     "overlap_org": "中共贵德县委员会",
     "overlap_period": "2026-07-19至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 3, "type": "overlap", "strength": "strong",
     "context": "张有强与华列同为十八届县委副书记",
     "overlap_org": "中共贵德县委员会",
     "overlap_period": "2026-07-19至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 4, "type": "overlap", "strength": "strong",
     "context": "张有强与韩贵军同为十八届县委副书记",
     "overlap_org": "中共贵德县委员会",
     "overlap_period": "2026-07-19至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 7, "type": "overlap", "strength": "medium",
     "context": "扎西尼玛为县委常委、县政府常务副县长，与县委书记同常委会班子",
     "overlap_org": "中共贵德县委员会",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "strength": "strong",
     "context": "张有强任县长主持县政府全面工作，扎西尼玛任常务副县长分管日常工作",
     "overlap_org": "贵德县人民政府",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "strength": "strong",
     "context": "张有强任县长，徐瑞任副县长，行政上下级",
     "overlap_org": "贵德县人民政府",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "strength": "strong",
     "context": "张有强任县长，才太本任副县长",
     "overlap_org": "贵德县人民政府",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "strength": "strong",
     "context": "张有强任县长，张志愿任副县长兼公安局长",
     "overlap_org": "贵德县人民政府",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "strength": "strong",
     "context": "张有强任县长，刘大庆任副县长",
     "overlap_org": "贵德县人民政府",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "strength": "strong",
     "context": "张有强任县长，师海成任副县长",
     "overlap_org": "贵德县人民政府",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 5, "person_b": 6, "type": "overlap", "strength": "medium",
     "context": "卢林与梁祎均为援青干部、县委副书记、副县长，同批对口支援",
     "overlap_org": "贵德县人民政府",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 19, "type": "superior_subordinate", "strength": "medium",
     "context": "李正业为贵德县委书记，熊元来为海南州委书记，县委-州委上下级关系",
     "overlap_org": "中共海南藏族自治州委员会",
     "overlap_period": "至今", "confidence": "confirmed"},
    {"person_a": 1, "person_b": 20, "type": "overlap", "strength": "medium",
     "context": "贵德为海南州下辖县，当周为州委副书记、代理州长，领导工作联系密切",
     "overlap_org": "海南藏族自治州党委/政府",
     "overlap_period": "至今", "confidence": "plausible"},
    {"person_a": 19, "person_b": 20, "type": "overlap", "strength": "strong",
     "context": "熊元来任海南州委书记，当周任州委副书记、州政府代理州长，为州级党政一把手",
     "overlap_org": "海南藏族自治州委员会/人民政府",
     "overlap_period": "至今", "confidence": "confirmed"},
]

# ── HELPERS ─────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

def person_color(p):
    role = p["current_post"]
    if ("县委书记" in role) and ("副书记" not in role):
        return "255,50,50"
    elif "县长" in role and "县" in role:
        return "50,100,255"
    elif "纪委书记" in role or "纪检" in role:
        return "255,165,0"
    elif "人大常委会" in role or "人大" in role:
        return "200,255,255"
    elif "政协" in role:
        return "255,240,200"
    elif "副州长" in role or "州长" in role or "州委书记" in role:
        return "255,165,0"
    else:
        return "100,100,100"

def org_color(o):
    t = o["type"]
    return {
        "党委": "255,200,200",
        "政府": "200,200,255",
        "纪委": "255,180,120",
        "人大": "200,255,255",
        "政协": "255,240,200",
    }.get(t, "200,200,200")

def is_top_leader(p):
    role = p["current_post"]
    return ("县委书记" in role and "副书记" not in role) or ("县长" in role)

def person_size(p):
    return "20.0" if is_top_leader(p) else "12.0"

# ── BUILD DB ─────────────────────────────────────────────────

def build_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.executescript("""
        CREATE TABLE IF NOT EXISTS persons (
            id INTEGER PRIMARY KEY,
            name TEXT, gender TEXT, ethnicity TEXT, birth TEXT,
            birthplace TEXT, education TEXT, party_join TEXT,
            work_start TEXT, current_post TEXT, current_org TEXT, source TEXT
        );
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY, name TEXT, type TEXT, level TEXT,
            parent TEXT, location TEXT
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER, org_id INTEGER, title TEXT,
            start TEXT, end TEXT, rank TEXT, note TEXT,
            FOREIGN KEY(person_id) REFERENCES persons(id),
            FOREIGN KEY(org_id) REFERENCES organizations(id)
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER, person_b INTEGER, type TEXT, strength TEXT,
            context TEXT, overlap_org TEXT, overlap_period TEXT, confidence TEXT,
            FOREIGN KEY(person_a) REFERENCES persons(id),
            FOREIGN KEY(person_b) REFERENCES persons(id)
        );
    """)

    for p in persons:
        c.execute("""INSERT OR REPLACE INTO persons
            (id, name, gender, ethnicity, birth, birthplace, education,
             party_join, work_start, current_post, current_org, source)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)""",
            (p["id"], p["name"], p["gender"], p["ethnicity"], p["birth"],
             p["birthplace"], p["education"], p["party_join"], p["work_start"],
             p["current_post"], p["current_org"], p["source"]))

    for o in organizations:
        c.execute("""INSERT OR REPLACE INTO organizations
            (id, name, type, level, parent, location)
            VALUES (?,?,?,?,?,?)""",
            (o["id"], o["name"], o["type"], o["level"], o["parent"], o["location"]))

    for pos in positions:
        c.execute("""INSERT OR REPLACE INTO positions
            (person_id, org_id, title, start, end, rank, note)
            VALUES (?,?,?,?,?,?,?)""",
            (pos["person_id"], pos["org_id"], pos["title"], pos["start"],
             pos["end"], pos["rank"], pos["note"]))

    for r in relationships:
        c.execute("""INSERT OR REPLACE INTO relationships
            (person_a, person_b, type, strength, context, overlap_org, overlap_period, confidence)
            VALUES (?,?,?,?,?,?,?,?)""",
            (r["person_a"], r["person_b"], r["type"], r["strength"], r["context"],
             r["overlap_org"], r["overlap_period"], r["confidence"]))

    conn.commit()
    conn.close()
    print(f"Database created: {DB_PATH}")

# ── BUILD GEXF ─────────────────────────────────────────────────

def build_gexf():
    os.makedirs(os.path.dirname(GEXF_PATH), exist_ok=True)
    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{datetime.now().strftime("%Y-%m-%d")}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>贵德县领导班子工作关系网络 (task_id qinghai_贵德县)</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="org_type" type="string"/>')
    lines.append('      <attribute id="2" title="title" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="etype" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="period" type="string"/>')
    lines.append('      <attribute id="3" title="confidence" type="string"/>')
    lines.append('    </attributes>')

    lines.append('    <nodes>')
    for p in persons:
        c = person_color(p)
        sz = person_size(p)
        lines.append(f'      <node id="p{p["id"]}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p["current_org"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p["current_post"])}"/>')
        lines.append('        </attvalues>')
        r, g, b = [x.strip() for x in c.split(",")]
        lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')

    for o in organizations:
        c = org_color(o)
        r, g, b = [x.strip() for x in c.split(",")]
        lines.append(f'      <node id="o{o["id"]}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="org"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o["type"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(o["parent"])}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{r}" g="{g}" b="{b}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        if pos["org_id"] == 0:
            continue  # skip placeholder person gap row (no org node)
        eid += 1
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos["note"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(pos["start"])}~{esc(pos["end"])}"/>')
        lines.append('          <attvalue for="3" value="confirmed"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        w = "2.0" if r["strength"] == "strong" else "1.5" if r["strength"] == "medium" else "1.0"
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="{w}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r["context"])}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r["overlap_period"])}"/>')
        lines.append(f'          <attvalue for="3" value="{r["confidence"]}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF created: {GEXF_PATH}")

# ── SUMMARY ─────────────────────────────────────────────────

def print_summary():
    print(f"\nSummary:")
    print(f"  Persons: {len(persons)}")
    print(f"  Organizations: {len(organizations)}")
    print(f"  Positions: {len(positions)}")
    print(f"  Relationships: {len(relationships)}")
    print(f"  Database: {DB_PATH}")
    print(f"  GEXF: {GEXF_PATH}")

if __name__ == "__main__":
    build_db()
    build_gexf()
    print_summary()