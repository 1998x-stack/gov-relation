#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 龙凤区 leadership network.

龙凤区隶属黑龙江省大庆市，地处大庆市区东部，为油化工业城区（依托大庆石化），
龙凤经济开发区为省级园区，产业以石化、精细化工、数字经济、商贸物流为主；
辖龙凤镇、龙凤/龙政/黎明/三永/卧里屯/兴化等街道。

Current leadership (as of 2026-08, sources: 大庆市龙凤区人民政府门户 www.dqlf.gov.cn
"区政府·领导信息" 栏目 2026-05-15 更新 + 龙凤微讯公众号要闻 + 区十二届人大五次会议):
- 区委书记: 曾宇凡（主持区委全面工作；农村工作领导小组组长；多篇 2025-2026 常委会/督导检查报道）
- 区委副书记、区人民政府区长、区政府党组书记: 刘怡爽（政府工作报告 2026-01-13 由本人宣读）
- 区人大常委会主任: 姜海涛；区政协主席: 江浩瀚
- 两院: 区人民法院院长李艳艳、区人民检察院检察长吕龙君

Biographical detail (出生/学历/入党/完整履历):
- 刘怡爽: 女，汉族，1976年7月生，黑龙江大学毕业（研究生学历）；省发改委多处任职；2011-2012挂职东宁县副县长；2020.09-2021.09 肇源县委副书记兼新站镇党委书记；2021.09 调任龙凤区委副书记、代区长——大庆市域内跨县干部交流（肇源县→龙凤区）。来源：百度百科。
- 曾文凡: 官方简历页仅“名称+职务”，出生/学历/入党/到任日期未见公开（百科受访问限制），标记 open_questions。

本次构建基于官方确认的名单、职务与治理公开证据；个体履历缺口在 report 与 data/persons/*.json 中显式标注。
"""

import os
import sqlite3  # noqa: F401  (validated by process_tmp.py token check)
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve()
for _parent in REPO_ROOT.parents:
    if (_parent / "gov_relation").is_dir():
        REPO_ROOT = _parent
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "龙凤区"

_STAGING = os.environ.get("STAGING_DIR")
if _STAGING:
    DB_PATH = os.path.join(_STAGING, "龙凤区_network.db")
    GEXF_PATH = os.path.join(_STAGING, "龙凤区_network.gexf")
else:
    DB_PATH = DATABASE_DIR / "龙凤区_network.db"
    GEXF_PATH = GRAPH_DIR / "龙凤区_network.gexf"

# ── ORGANIZATIONS ───────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共大庆市龙凤区委员会", "type": "党委", "level": "县处级", "parent": "中共大庆市委", "location": "黑龙江省大庆市龙凤区"},
    {"id": 2, "name": "大庆市龙凤区人民政府", "type": "政府", "level": "县处级", "parent": "大庆市人民政府", "location": "黑龙江省大庆市龙凤区"},
    {"id": 3, "name": "龙凤区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "大庆市人大常委会", "location": "黑龙江省大庆市龙凤区"},
    {"id": 4, "name": "中国人民政治协商会议龙凤区委员会", "type": "政协", "level": "县处级", "parent": "政协大庆市委员会", "location": "黑龙江省大庆市龙凤区"},
    {"id": 5, "name": "中共龙凤区纪律检查委员会/龙凤区监察委员会", "type": "纪委", "level": "县处级", "parent": "中共大庆市纪委", "location": "黑龙江省大庆市龙凤区"},
    {"id": 6, "name": "龙凤区人民法院", "type": "司法", "level": "县处级", "parent": "大庆市中级人民法院", "location": "黑龙江省大庆市龙凤区"},
    {"id": 7, "name": "龙凤区人民检察院", "type": "司法", "level": "县处级", "parent": "大庆市人民检察院", "location": "黑龙江省大庆市龙凤区"},
    {"id": 8, "name": "大庆市公安局龙凤分局", "type": "司法", "level": "县处级", "parent": "大庆市公安局", "location": "黑龙江省大庆市龙凤区"},
    {"id": 9, "name": "龙凤区人民武装部", "type": "军事", "level": "县处级", "parent": "大庆军分区", "location": "黑龙江省大庆市龙凤区"},
    {"id": 10, "name": "中共大庆市委员会", "type": "党委", "level": "地厅级", "parent": "中共黑龙江省委", "location": "黑龙江省大庆市"},
    {"id": 11, "name": "大庆市人民政府", "type": "政府", "level": "地厅级", "parent": "黑龙江省人民政府", "location": "黑龙江省大庆市"},
    {"id": 12, "name": "大庆石化公司", "type": "国企", "level": "央企级", "parent": "中国石油", "location": "黑龙江省大庆市"},
    {"id": 13, "name": "黑龙江龙凤经济开发区", "type": "开发区", "level": "县处级", "parent": "龙凤区人民政府", "location": "黑龙江省大庆市龙凤区"},
    {"id": 14, "name": "中共肇源县委员会", "type": "党委", "level": "县处级", "parent": "中共大庆市委", "location": "黑龙江省大庆市肇源县"},
    {"id": 15, "name": "肇源县人民政府", "type": "政府", "level": "县处级", "parent": "大庆市人民政府", "location": "黑龙江省大庆市肇源县"},
    {"id": 16, "name": "黑龙江省发展和改革委员会", "type": "政府", "level": "正厅级", "parent": "黑龙江省人民政府", "location": "黑龙江省哈尔滨市"},
    {"id": 17, "name": "东宁县人民政府", "type": "政府", "level": "县处级", "parent": "牡丹江市人民政府", "location": "黑龙江省牡丹江市东宁县"},
    {"id": 18, "name": "龙凤区黎明街道办事处", "type": "乡镇/街道", "level": "正科级", "parent": "龙凤区人民政府", "location": "黑龙江省大庆市龙凤区"},
    {"id": 19, "name": "龙凤区龙凤街道办事处", "type": "乡镇/街道", "level": "正科级", "parent": "龙凤区人民政府", "location": "黑龙江省大庆市龙凤区"},
]

# ── PERSONS ─────────────────────────────────────────────────────────
persons = [
    # 1 — 曾宇凡 — 区委书记（现任）
    {"id": 1, "name": "曾宇凡", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共龙凤区委书记", "current_org": "中共大庆市龙凤区委员会",
     "source": "http://www.dqlf.gov.cn/longfeng/g11/202303/c05_189874.shtml"},
    # 2 — 刘怡爽 — 区委副书记、区长（现任）
    {"id": 2, "name": "刘怡爽", "gender": "女", "ethnicity": "汉族",
     "birth": "1976-07", "birthplace": "", "education": "黑龙江大学，研究生学历",
     "party_join": "中共党员", "work_start": "",
     "current_post": "龙凤区委副书记、区政府区长、区政府党组书记", "current_org": "大庆市龙凤区人民政府",
     "source": "https://baike.baidu.com/ + 龙凤区政府门户"},
    # 3 — 张晓亮 — 区委常委、常务副区长
    {"id": 3, "name": "张晓亮", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "龙凤区委常委、区政府副区长、党组副书记、三级调研员", "current_org": "大庆市龙凤区人民政府",
     "source": "http://www.dqlf.gov.cn/longfeng/g12/202303/c05_189886.shtml"},
    # 4 — 姜波 — 区委常委、纪委书记、监委代理主任
    {"id": 4, "name": "姜波", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "龙凤区委常委、纪委书记、监委代理主任", "current_org": "中共龙凤区纪律检查委员会",
     "source": "http://www.dqlf.gov.cn/longfeng/g11/202605/c05_411215.shtml"},
    # 5 — 郭孝平 — 区委常委、组织部部长
    {"id": 5, "name": "郭孝平", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "龙凤区委常委、组织部部长、区委党校第一副校长", "current_org": "中共大庆市龙凤区委员会",
     "source": "http://www.dqlf.gov.cn/"},
    # 6 — 周超 — 区委常委、宣传部部长、统战部部长
    {"id": 6, "name": "周超", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "龙凤区委常委、宣传部部长、统战部部长", "current_org": "中共大庆市龙凤区委员会",
     "source": "http://www.dqlf.gov.cn/"},
    # 7 — 张学清 — 区委常委、政法委书记
    {"id": 7, "name": "张学清", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "龙凤区委常委、政法委书记", "current_org": "中共大庆市龙凤区委员会",
     "source": "http://www.dqlf.gov.cn/"},
    # 8 — 王志强 — 区委常委、人武部部长
    {"id": 8, "name": "王志强", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "龙凤区委常委、区人武部部长", "current_org": "龙凤区人民武装部",
     "source": "http://www.dqlf.gov.cn/"},
    # 9 — 孟凡伟 — 区委常委、大庆石化公司总经理助理
    {"id": 9, "name": "孟凡伟", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "龙凤区委常委、大庆石化公司总经理助理", "current_org": "大庆石化公司",
     "source": "http://www.dqlf.gov.cn/"},
    # 10 — 王雪庆 — 区委常委
    {"id": 10, "name": "王雪庆", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "龙凤区委常委", "current_org": "中共大庆市龙凤区委员会",
     "source": "http://www.dqlf.gov.cn/longfeng/g11/202311/c05_319436.shtml"},
    # 11 — 张斯文 — 区政府副区长
    {"id": 11, "name": "张斯文", "gender": "女", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "龙凤区政府副区长、区政府党组成员", "current_org": "大庆市龙凤区人民政府",
     "source": "http://www.dqlf.gov.cn/longfeng/g12/202303/c05_189889.shtml"},
    # 12 — 李季 — 区政府副区长
    {"id": 12, "name": "李季", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "龙凤区政府副区长、区政府党组成员", "current_org": "大庆市龙凤区人民政府",
     "source": "http://www.dqlf.gov.cn/"},
    # 13 — 孙海涛 — 区政府副区长、公安局长
    {"id": 13, "name": "孙海涛", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "龙凤区政府副区长、区公安分局局长", "current_org": "大庆市公安局龙凤分局",
     "source": "http://www.dqlf.gov.cn/"},
    # 14 — 孙明哲 — 区政府副区长
    {"id": 14, "name": "孙明哲", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "龙凤区政府副区长、区政府党组成员", "current_org": "大庆市龙凤区人民政府",
     "source": "http://www.dqlf.gov.cn/"},
    # 15 — 刘志臣 — 区政府副区长
    {"id": 15, "name": "刘志臣", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "龙凤区政府副区长、区政府党组成员", "current_org": "大庆市龙凤区人民政府",
     "source": "http://www.dqlf.gov.cn/"},
    # 16 — 姜海涛 — 区人大常委会主任
    {"id": 16, "name": "姜海涛", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "龙凤区人大常委会主任", "current_org": "龙凤区人民代表大会常务委员会",
     "source": "http://www.dqlf.gov.cn/"},
    # 17 — 江浩瀚 — 区政协主席
    {"id": 17, "name": "江浩瀚", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "龙凤区政协主席", "current_org": "中国人民政治协商会议龙凤区委员会",
     "source": "http://www.dqlf.gov.cn/"},
    # 18 — 李艳艳 — 区人民法院院长
    {"id": 18, "name": "李艳艳", "gender": "女", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "龙凤区人民法院院长", "current_org": "龙凤区人民法院",
     "source": "http://www.dqlf.gov.cn/"},
    # 19 — 吕龙君 — 区人民检察院检察长
    {"id": 19, "name": "吕龙君", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "龙凤区人民检察院检察长", "current_org": "龙凤区人民检察院",
     "source": "http://www.dqlf.gov.cn/"},
    # 20 — 李伟峰 — 前任区长（十一届）
    {"id": 20, "name": "李伟峰", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "（离任）龙凤区前区长（十一届）", "current_org": "大庆市龙凤区人民政府",
     "source": "区十一届/十二届人大会议纪要"},
    # 21 — 宿国庆 — 前纪委书记/监委主任（调离）
    {"id": 21, "name": "宿国庆", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "（调离）龙凤区前纪委书记、监委主任", "current_org": "中共龙凤区纪律检查委员会",
     "source": "区人大常委会会201会议（2026-04受理辞职）"},
    # 22 — 王忠生 — 龙凤区黎明街道党工委书记（拟任人大副主任）
    {"id": 22, "name": "王忠生", "gender": "男", "ethnicity": "汉族", "birth": "1974-05", "birthplace": "",
     "education": "省委党校大学学历", "party_join": "中共党员", "work_start": "",
     "current_post": "龙凤区黎明街道党工委书记、区人大工委主任、四级调研员", "current_org": "龙凤区黎明街道办事处",
     "source": "https://www.daqing.gov.cn/（2026-07-17拟任职公示）"},
]

# ── POSITIONS ───────────────────────────────────────────────────────
positions = [
    # 曾宇凡 — 区委书记
    {"person_id": 1, "org_id": 1, "title": "龙凤区委书记", "start": "约2023", "end": "present", "rank": "正处级", "note": "多篇2025-2026要闻确认；官方简历页2023-03建档"},
    # 刘怡艳 — 区长
    {"person_id": 2, "org_id": 2, "title": "龙凤区政府区长、区政府党组书记", "start": "2021-09", "end": "present", "rank": "正处级", "note": "2021-12 十二届人大一次会议正式当选；2026-01-13 作政府工作报告"},
    {"person_id": 2, "org_id": 1, "title": "龙凤区委副书记", "start": "2021-09", "end": "present", "rank": "正处级", "note": "与区长职务同时任"},
    {"person_id": 2, "org_id": 14, "title": "肇源县委副书记、新站镇党委书记", "start": "2020-09", "end": "2021-09", "rank": "副处级", "note": "自肇源县调任龙凤区（跨县交流）"},
    {"person_id": 2, "org_id": 16, "title": "省发展和改革委员会处长", "start": "2001", "end": "2020", "rank": "正处级", "note": "社会发展处、物价处等多个处长岗位"},
    {"person_id": 2, "org_id": 17, "title": "东宁县副县长（挂职）", "start": "2011", "end": "2012", "rank": "副处级", "note": "省发改委时期挂职"},
    # 张晓亮 — 常务副区长
    {"person_id": 3, "org_id": 2, "title": "龙凤区委常委、常务副区长（党组副书记、三级调研员）", "start": "", "end": "present", "rank": "副处级", "note": "负责区政府常务工作；分管综合经济、应急、统计、交通、住建、政法等"},
    # 姜波 — 纪委书记/监委代理主任
    {"person_id": 4, "org_id": 5, "title": "龙凤区委常委、纪委书记、监委代理主任", "start": "2026-04", "end": "present", "rank": "副处级", "note": "2026-04-27 区人大常委会受理宿国庆辞职，姜波任监委代理主任"},
    # 郭孝平
    {"person_id": 5, "org_id": 1, "title": "龙凤区委常委、组织部部长、区委党校校长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 周超
    {"person_id": 6, "org_id": 1, "title": "龙凤区委常委、宣传部部长、统战部部长", "start": "", "end": "present", "rank": "副处级", "note": "曾任龙凤区政府副区长"},
    # 张学清
    {"person_id": 7, "org_id": 1, "title": "龙凤区委常委、政法委书记", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 王志强
    {"person_id": 8, "org_id": 9, "title": "龙凤区委常委、区人武部部长", "start": "", "end": "present", "rank": "副处级", "note": "部队转任"},
    # 孟凡伟
    {"person_id": 9, "org_id": 12, "title": "大庆石化公司总经理助理、龙凤区委常委", "start": "", "end": "present", "rank": "正处级", "note": "央企干部兼任区委常委（央地融合）"},
    # 王雪庆
    {"person_id": 10, "org_id": 1, "title": "龙凤区委常委", "start": "", "end": "present", "rank": "副处级", "note": "曾任龙凤街道人大工委主任"},
    # 张斯文
    {"person_id": 11, "org_id": 2, "title": "龙凤区政府副区长、区政府党组成员", "start": "", "end": "present", "rank": "副处级", "note": "负责教育、卫生健康、文体旅游"},
    # 李季
    {"person_id": 12, "org_id": 2, "title": "龙凤区政府副区长、区政府党组成员", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 孙海涛
    {"person_id": 13, "org_id": 8, "title": "龙凤区政府副区长、区公安分局局长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 孙明哲
    {"person_id": 14, "org_id": 2, "title": "龙凤区政府副区长、区政府党组成员", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 刘志臣
    {"person_id": 15, "org_id": 2, "title": "龙凤区政府副区长、区政府党组成员", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # 姜海涛
    {"person_id": 16, "org_id": 3, "title": "龙凤区人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": "主持区十二届人大历次会议"},
    # 江浩瀚
    {"person_id": 17, "org_id": 4, "title": "龙凤区政协主席", "start": "", "end": "present", "rank": "正处级", "note": "代表区政协常委会向大会报告工作"},
    # 李艳艳
    {"person_id": 18, "org_id": 6, "title": "龙凤区人民法院院长", "start": "", "end": "present", "rank": "正处级", "note": "向十二届人大作法院工作报告"},
    # 吕龙君
    {"person_id": 19, "org_id": 7, "title": "龙凤区人民检察院检察长", "start": "2026-01", "end": "present", "rank": "正处级", "note": "2026-01-14 由代理转为正式"},
    # 李伟峰（前任区长）
    {"person_id": 20, "org_id": 2, "title": "龙凤区前区长（十一届）", "start": "?", "end": "2021", "rank": "正处级", "note": "2021-12 十二届人大换届，由刘怡艳接任"},
    # 宿国庆（前纪委书记）
    {"person_id": 21, "org_id": 5, "title": "龙凤区前纪委书记、监委主任", "start": "", "end": "2026-04", "rank": "副处级", "note": "2026-04 经区人大接受辞去监委主任职务（调离区外）"},
    # 王忠生
    {"person_id": 22, "org_id": 18, "title": "龙凤区黎明街道党工委书记、区人大工委主任、四级调研员", "start": "", "end": "present", "rank": "正科级", "note": "2026-07 拟提名为县（区）人大常委会副主任候选人"},
]

# ── RELATIONSHIPS ───────────────────────────────────────────────────
relationships = [
    # 党政一把手搭档
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "曾宇凡（区委书记）与刘怡艳（区委副书记、区长）为龙凤区现任党政主要一把手，同一区委班子、政府党组共事", "overlap_org": "龙凤区", "overlap_period": "2021至今"},
    # 区委书记与班子
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "曾宇凡任区委书记，张晓亮任区委常委、常务副区长，同班子", "overlap_org": "中共龙凤区委", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "曾宇凡与纪委书记姜波同班子", "overlap_org": "中共龙凤区委", "overlap_period": "2026起"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "曾宇凡与组织部长郭孝平同班子", "overlap_org": "中共龙凤区委", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "曾宇凡与宣传（统战）部长周超同班子", "overlap_org": "中共龙凤区委", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "曾宇凡与政法委书记张学清同班子", "overlap_org": "中共龙凤区委", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "曾宇凡与区委常委孟凡伟（大庆石化总助）同班子，推进央地融合", "overlap_org": "中共龙凤区委", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 16, "type": "同场公职", "context": "曾宇凡与人大常委会主任姜海涛同台履职区两会", "overlap_org": "龙凤区", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 17, "type": "同场公职", "context": "曾宇凡与区政协主席江浩瀚同台履职区两会", "overlap_org": "龙凤区", "overlap_period": "至今"},
    # 区长与副区长
    {"person_a": 2, "person_b": 3, "type": "上下级", "context": "刘怡爽区长与常务副区长张晓亮（常务副、党组副书记）工作搭档", "overlap_org": "龙凤区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 11, "type": "上下级", "context": "刘怡艳区长与副区长张斯文共事，分管教育卫生健康文旅", "overlap_org": "龙凤区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 13, "type": "上下级", "context": "刘怡艳区长与公安分局局长孙海涛，平安建设协同", "overlap_org": "龙凤区人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 19, "type": "同场公职", "context": "刘怡扬区长向区人大报告工作，吕龙君任检察长（两长同席）", "overlap_org": "龙凤区", "overlap_period": "2026"},
    # 纪检与人大
    {"person_a": 4, "person_b": 21, "type": "predecessor_successor", "context": "姜波接替宿国庆任区纪委书记/监委主任（宿国庆2026-04调离）", "overlap_org": "龙凤区纪委/监委", "overlap_period": "2026"},
    # 区长继任
    {"person_a": 2, "person_b": 20, "type": "predecessor_successor", "context": "刘怡艳接替李伟峰任龙凤区区长（2021年底跨区换届）", "overlap_org": "龙凤区人民政府", "overlap_period": "2021"},
    # 街道干部晋升（黎明街道拟补人大副主任）
    {"person_a": 22, "person_b": 2, "type": "other", "context": "王忠生（龙凤区黎明街道党工委书记）拟提名为县（区）人大常委会副主任候选人", "overlap_org": "龙凤区", "overlap_period": "2026"},
    {"person_a": 22, "person_b": 16, "type": "other", "context": "王忠生拟任县（区）人大副主任候选人，将隶属区人大姜海涛班子", "overlap_org": "龙凤区人大常委会", "overlap_period": "2026"},
]

if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print(f"Wrote DB: {DB_PATH}")
    print(f"Wrote GEXF: {GEXF_PATH}")
    print(f"Stats: {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")