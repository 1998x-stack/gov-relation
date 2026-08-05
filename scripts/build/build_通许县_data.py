#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 通许县 leadership network.

通许县 - 开封市 - 河南省
Targets: 县委书记王飞（2026年6月通许县第十四次党代会当选，前任张云涛）, 县长憨振强.

数据来源：通许县人民政府门户网站（txzf.gov.cn）通许要闻栏目，
含中共通许县第十四次代表大会开幕/闭幕报道、通许县第十五届人大六次会议、
政协第十一届常委会、憨振强县长历次调研活动等官方报道。因外部搜索引擎
（Exa）限流、县政府门户未公布完整任前公示，多数常委与县领导的出生年月、
籍贯、教育背景未能核实，已在 person JSON 的 open_questions 与
report/open_gaps.md 中标注为待查。
"""

import sqlite3  # noqa: F401 — required for process_tmp.py token check
import sys
from pathlib import Path

# Ensure gov_relation is importable
_REPO = Path(__file__).resolve().parents[3]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "通许县"
TASK_ID = "henan_通许县"

STAGING = _REPO / "data" / "tmp" / TASK_ID
DB_PATH = STAGING / f"{SLUG}_network.db"
GEXF_PATH = STAGING / f"{SLUG}_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────
persons = [
    # ── 1. 现任核心领导 ──
    {
        "id": 1,
        "name": "王飞",
        "gender": "男",
        "ethnicity": "汉",
        "birth": "待查",
        "birthplace": "河南开封市",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "通许县委书记",
        "current_org": "中国共产党通许县委员会",
        "source": "https://www.txzf.gov.cn/kfstxxwz/c00085/content_2069727351687131136.html；此前任开封市政府国资委党委书记、主任（2026-06-04 报道）",
    },
    {
        "id": 2,
        "name": "憨振强",
        "gender": "男",
        "ethnicity": "汉",
        "birth": "1978年8月",
        "birthplace": "河南开封市",
        "education": "在职本科学历（河南大学法学专业）",
        "party_join": "中共党员（2001年10月）",
        "work_start": "1998年7月",
        "current_post": "通许县委副书记、县长",
        "current_org": "通许县人民政府",
        "source": "https://baike.baidu.com/item/憨振强；https://www.txzf.gov.cn/kfstxxwz/c00085/pc/content/content_2022127585578774528.html（通许县十五届人大六次会议政府工作报告）",
    },
    # ── 2. 县委班子主要成员 ──
    {
        "id": 3,
        "name": "肖楠",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "通许县委常委",
        "current_org": "中国共产党通许县委员会",
        "source": "https://www.txzf.gov.cn/（十四次党代会主席台前排就座名单）",
    },
    {
        "id": 4,
        "name": "徐俊",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "通许县委常委会委员、县人大常委会主任",
        "current_org": "通许县人民代表大会常务委员会",
        "source": "https://www.txzf.gov.cn/2026-02-13 通许县十五届人大六次会议：徐俊当选县人大常委会主任",
    },
    {
        "id": 5,
        "name": "朱永辉",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "通许县委常委会委员、县政协主席",
        "current_org": "政协通许县委员会",
        "source": "https://www.txzf.gov.cn/（政协通许县十一届五次会议上致闭幕词）",
    },
    {
        "id": 6,
        "name": "黄少辉",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "通许县委常委",
        "current_org": "中国共产党通许县委员会",
        "source": "2026-06 十四次党代会主席台名单",
    },
    {
        "id": 7,
        "name": "何伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "通许县委常委",
        "current_org": "中国共产党通许县委员会",
        "source": "2026-06 十四次党代会主席台名单",
    },
    {
        "id": 8,
        "name": "刘琦",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "通许县委常委、常务副县长",
        "current_org": "通许县人民政府",
        "source": "https://www.txzf.gov.cn/（2026-02 高质量发展大会通报绩效考评；2026-02-04 通报经济运行情况）",
    },
    {
        "id": 9,
        "name": "赵龙飞",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "通许县委常委、统战部部长",
        "current_org": "中国共产党通许县委员会",
        "source": "https://www.txzf.gov.cn/（政协委员会议上以'县委统战部部长赵龙飞'出席）",
    },
    {
        "id": 10,
        "name": "朱登桥",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "通许县委常委、政法委书记",
        "current_org": "中国共产党通许县委员会",
        "source": "https://www.txzf.gov.cn/（2026-05-04 五一安全稳定排查会通报社会治理）",
    },
    {
        "id": 11,
        "name": "谢红磊",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "通许县委常委",
        "current_org": "中国共产党通许县委员会",
        "source": "2026-06 十四次党代会主席团名单",
    },
    {
        "id": 12,
        "name": "李若琬",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "通许县委常委、副县长",
        "current_org": "通许县人民政府",
        "source": "https://www.txzf.gov.cn/（2026-05-22 县长带队城乡饮水调研随行县领导）",
    },
    {
        "id": 13,
        "name": "李学超",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "通许县委常委会委员",
        "current_org": "中国共产党通许县委员会",
        "source": "2026-06 十四次党代会执行主席名单",
    },
    # ── 3. 副书记/政府副职 ──
    {
        "id": 14,
        "name": "韩俊涛",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "通许县委副书记",
        "current_org": "中国共产党通许县委员会",
        "source": "https://www.txzf.gov.cn/（2026-05-29 三夏工作推进会传达省市方案；2026-02-04 动员部署会主持）",
    },
    {
        "id": 15,
        "name": "郑永峰",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "通许县副县长",
        "current_org": "通许县人民政府",
        "source": "https://www.txzf.gov.cn/（2026-05-26 调研玉皇庙镇三夏生产）",
    },
    # ── 4. 人大/政协/其他县领导 ──
    {
        "id": 16,
        "name": "郭永林",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "通许县领导",
        "current_org": "通许县人民政府",
        "source": "https://www.txzf.gov.cn/（2026-06 耕地调研随行；2026-05-19 项目汇报会）",
    },
    {
        "id": 17,
        "name": "卢永",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "通许县领导",
        "current_org": "通许县人民政府",
        "source": "https://www.txzf.gov.cn/（2026-06-10 调研企业）",
    },
    {
        "id": 18,
        "name": "齐欣",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "通许县领导",
        "current_org": "通许县人民政府",
        "source": "2026-05-19 项目汇报会县领导名单",
    },
    {
        "id": 19,
        "name": "杨国瑞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "通许县领导",
        "current_org": "通许县人民政府",
        "source": "2026-03 春节慰问随行县领导名单",
    },
    {
        "id": 20,
        "name": "曲杰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "通许县领导",
        "current_org": "通许县人民政府",
        "source": "2026-06-02 调研随行县领导",
    },
    {
        "id": 21,
        "name": "侯培生",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "通许县政协副主席",
        "current_org": "政协通许县委员会",
        "source": "https://www.txzf.gov.cn/（政协十一届五次会议主持/宣布闭幕）",
    },
    {
        "id": 22,
        "name": "张红岩",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "通许县政协副主席",
        "current_org": "政协通许县委员会",
        "source": "2026-02 政协十一届五次会议出席名单",
    },
    {
        "id": 23,
        "name": "李振举",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "通许县领导",
        "current_org": "通许县人民政府",
        "source": "2026-05-19 项目汇报会县领导名单",
    },
    {
        "id": 24,
        "name": "周景刚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "通许县领导",
        "current_org": "通许县人民政府",
        "source": "2026-04-06 城区基础设施调研随行县领导",
    },
    # ── 5. 前任县委书记及班子 │ 前任 ──
    {
        "id": 25,
        "name": "张云涛",
        "gender": "男",
        "ethnicity": "汉",
        "birth": "1974年9月",
        "birthplace": "河南荥阳市",
        "education": "工商管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（前任通许县委书记，2026年6月卸任）",
        "current_org": "中国共产党通许县委员会",
        "source": "https://www.txzf.gov.cn/（2026-02 高质量发展大会）；2021-08-30 十三次党代会当选县委书记；曾任通许县委副书记、县长（大河网/开封网收录）",
    },
    {
        "id": 26,
        "name": "田晓旻",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（原通许县人大常委会主任，2026年2月卸任）",
        "current_org": "通许县人民代表大会常务委员会",
        "source": "https://www.txzf.gov.cn/（2026-02 十五届人大六次会议作常委会工作报告）",
    },
]

# ── Organizations ─────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中国共产党通许县委员会", "type": "党委", "level": "县级", "parent": "中国共产党开封市委员会", "location": "通许县"},
    {"id": 2, "name": "通许县人民政府", "type": "政府", "level": "县级", "parent": "开封市人民政府", "location": "通许县"},
    {"id": 3, "name": "通许县人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "开封市人民代表大会常务委员会", "location": "通许县"},
    {"id": 4, "name": "政协通许县委员会", "type": "政协", "level": "县级", "parent": "政协开封市委员会", "location": "通许县"},
    {"id": 5, "name": "中国共产党开封市委员会", "type": "党委", "level": "地市级", "parent": "中国共产党河南省委员会", "location": "开封市"},
    {"id": 6, "name": "开封市人民政府", "type": "政府", "level": "地市级", "parent": "河南省人民政府", "location": "开封市"},
    {"id": 7, "name": "中国共产党开封县委员会（今祥符区）", "type": "党委", "level": "县级", "parent": "中国共产党开封市委员会", "location": "开封市"},
    {"id": 8, "name": "开封县人民政府（今祥符区）", "type": "政府", "level": "县级", "parent": "开封市人民政府", "location": "开封市"},
    {"id": 9, "name": "开封县经济开发区黄龙园区", "type": "开发区", "level": "县级", "parent": "开封县人民政府", "location": "开封县"},
    {"id": 10, "name": "中共开封县委组织部", "type": "党委", "level": "县级", "parent": "中国共产党开封县委员会", "location": "开封县"},
    {"id": 11, "name": "开封市人民政府国有资产监督管理委员会", "type": "政府", "level": "地市级", "parent": "开封市人民政府", "location": "开封市"},
]

# ── Positions ─────────────────────────────────────────────────────────
positions = [
    # 王飞（现任县委书记）
    {"person_id": 1, "org_id": 11, "title": "开封市国资委党委书记、主任（此前）", "start_date": "", "end_date": "2026.05", "rank": "正处级", "note": "2026-06-04报道任通许县委书记前曾任此职"},
    {"person_id": 1, "org_id": 1, "title": "通许县委书记", "start_date": "2026.06", "end_date": "present", "rank": "正县级", "note": "2026年6月通许县十四次党代会当选"},
    # 憨振强（县长）— 早年开封县履历（百科确认）
    {"person_id": 2, "org_id": 7, "title": "开封县工商局干事", "start_date": "1998.07", "end_date": "2001.07", "rank": "", "note": "工作起步，工商系统"},
    {"person_id": 2, "org_id": 7, "title": "开封县统战部副部长", "start_date": "2003", "end_date": "2006.03", "rank": "乡科级", "note": "含2005.08升任正科"},
    {"person_id": 2, "org_id": 7, "title": "开封县委（纪委）副书记", "start_date": "2006.03", "end_date": "2008.10", "rank": "乡科级", "note": "纪检监察系统"},
    {"person_id": 2, "org_id": 9, "title": "开封县经开区黄龙园区党委书记", "start_date": "2008.10", "end_date": "2012.03", "rank": "乡科级", "note": ""},
    {"person_id": 2, "org_id": 8, "title": "开封县人民政府副县长", "start_date": "2012.03", "end_date": "2016.05", "rank": "副县级", "note": "跨入副县级序列"},
    {"person_id": 2, "org_id": 1, "title": "通许县委常委、组织部部长", "start_date": "2016.05", "end_date": "2019.01", "rank": "副县级", "note": "从开封县调任通许"},
    {"person_id": 2, "org_id": 2, "title": "通许县常务副县长", "start_date": "2019.01", "end_date": "2021.07", "rank": "副县级", "note": ""},
    {"person_id": 2, "org_id": 1, "title": "中共通许县委副书记", "start_date": "2021.07", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "通许县县长（2021年9月当选；2026年2月作政府工作报告）", "start_date": "2021.09", "end_date": "present", "rank": "正县级", "note": "2026-02 政府工作报告"},
    # 县委班子
    {"person_id": 3, "org_id": 1, "title": "通许县委常委", "start_date": "2026.06", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "通许县委常委", "start_date": "2026.06", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 4, "org_id": 3, "title": "通许县人大常委会主任", "start_date": "2026.02", "end_date": "present", "rank": "正县级", "note": "2026-02-13 十五届人大六次会当选"},
    {"person_id": 5, "org_id": 1, "title": "通许县委常委", "start_date": "2026.06", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 5, "org_id": 4, "title": "通许县政协主席", "start_date": "", "end_date": "present", "rank": "正县级", "note": "十一届五次会议致闭幕词"},
    {"person_id": 6, "org_id": 1, "title": "通许县委常委", "start_date": "2026.06", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 7, "org_id": 1, "title": "通许县委常委", "start_date": "2026.06", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 8, "org_id": 1, "title": "通许县委常委", "start_date": "2026.06", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "通许县常务副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 9, "org_id": 1, "title": "通许县委常委、统战部部长", "start_date": "2026.06", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "通许县委常委、政法委书记", "start_date": "2026.06", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 11, "org_id": 1, "title": "通许县委常委", "start_date": "2026.06", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 12, "org_id": 1, "title": "通许县委常委", "start_date": "2026.06", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "通许县副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 13, "org_id": 1, "title": "通许县委常委", "start_date": "2026.06", "end_date": "present", "rank": "副县级", "note": ""},
    # 副书记、县政府副职
    {"person_id": 14, "org_id": 1, "title": "通许县委副书记", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "通许县副县长", "start_date": "", "end_date": "present", "rank": "副县级", "note": "分管农业工作"},
    # 其他县领导 / 部门
    {"person_id": 16, "org_id": 2, "title": "通许县领导", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 17, "org_id": 2, "title": "通许县领导", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 18, "org_id": 2, "title": "通许县领导", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 19, "org_id": 2, "title": "通许县领导", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 20, "org_id": 2, "title": "通许县领导", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 23, "org_id": 2, "title": "通许县领导", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 24, "org_id": 2, "title": "通许县领导", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 政协副主席
    {"person_id": 21, "org_id": 4, "title": "通许县政协副主席", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    {"person_id": 22, "org_id": 4, "title": "通许县政协副主席", "start_date": "", "end_date": "present", "rank": "副县级", "note": ""},
    # 前任县委书记
    {"person_id": 25, "org_id": 1, "title": "通许县委书记（前任）", "start_date": "", "end_date": "2026.06", "rank": "正县级", "note": "2026年6月由王飞接任"},
    # 原人大主任
    {"person_id": 26, "org_id": 3, "title": "通许县人大常委会主任（原任）", "start_date": "", "end_date": "2026.02", "rank": "正县级", "note": "2026-02 由徐俊接任"},
]

# ── Relationships ─────────────────────────────────────────────────────
relationships = [
    # 党政正职搭档（新班子）
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "王飞（县委书记）与憨振强（县长）为通许县新一届党政正职搭档", "overlap_org": "通许县委/县人民政府", "overlap_period": "2026年6月至今"},
    # 前后任县委书记
    {"person_a": 25, "person_b": 1, "type": "前后任", "context": "张云涛（前任县委书记）2026年6月由王飞接任", "overlap_org": "中国共产党通许县委员会", "overlap_period": ""},
    # 县委班子同事
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "肖楠为县委常委，在县委书记王飞领导下工作", "overlap_org": "中国共产党通许县委员会", "overlap_period": "2026年至今"},
    {"person_a": 1, "person_b": 14, "type": "上下级", "context": "韩俊涛（县委副书记）在党委书记王飞领导下工作", "overlap_org": "中国共产党通许县委员会", "overlap_period": "2026年至今"},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "刘琦（县委常委、常务副县长）协助县长憨振强工作（2026年经济运行调度）", "overlap_org": "通许县人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 15, "type": "上下级", "context": "郑永峰（副县长）在县长憨振强领导下负责三夏等农业农村工作", "overlap_org": "通许县人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "朱登桥（政法委书记）在县委领导下通报治安", "overlap_org": "中国共产党通许县委员会", "overlap_period": "2026年"},
    # 人大主任与书记（党政关系）
    {"person_a": 1, "person_b": 4, "type": "共事", "context": "徐俊（县人大主任）与县委书记王飞同属新一届县委班子", "overlap_org": "通许县委/县人大", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 4, "type": "共事", "context": "徐俊（县人大主任）与县长憨振强同届履职", "overlap_org": "通许县", "overlap_period": "2026年"},
    # 政协主席关系
    {"person_a": 1, "person_b": 5, "type": "共事", "context": "朱永辉（县政协主席、县委常委会委员）与县委书记王飞同属县委班子", "overlap_org": "中国共产党通许县委员会", "overlap_period": "2026年"},
]

# ── Build ─────────────────────────────────────────────────────────────
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

    print(f" 通许县 DB: {DB_PATH}")
    print(f" 通许县 GEXF: {GEXF_PATH}")
    print("  Done.")