#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 泰来县 leadership network.

泰来县隶属黑龙江省齐齐哈尔市。

Current leadership as of 2026-07 (source: http://www.tailai.gov.cn/tailai/c100242/xzf.shtml):
- 县委书记: 郑德利
- 县长: 曲喜民

All biographical data sourced from official government leadership pages on www.tailai.gov.cn.
"""

import sqlite3
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "泰来县"
DB_PATH = DATABASE_DIR / "泰来县_network.db"
GEXF_PATH = GRAPH_DIR / "泰来县_network.gexf"

# ── ORGANIZATIONS ───────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共泰来县委员会", "type": "党委", "level": "县处级", "parent": "中共齐齐哈尔市委", "location": "黑龙江省齐齐哈尔市泰来县"},
    {"id": 2, "name": "泰来县人民政府", "type": "政府", "level": "县处级", "parent": "齐齐哈尔市人民政府", "location": "黑龙江省齐齐哈尔市泰来县"},
    {"id": 3, "name": "泰来县人大常委会", "type": "人大", "level": "县处级", "parent": "齐齐哈尔市人大常委会", "location": "黑龙江省齐齐哈尔市泰来县"},
    {"id": 4, "name": "泰来县政协", "type": "政协", "level": "县处级", "parent": "齐齐哈尔市政协", "location": "黑龙江省齐齐哈尔市泰来县"},
    {"id": 5, "name": "中共泰来县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共齐齐哈尔市纪委", "location": "黑龙江省齐齐哈尔市泰来县"},
    {"id": 6, "name": "中共泰来县委政法委员会", "type": "党委", "level": "县处级", "parent": "中共泰来县委员会", "location": "黑龙江省齐齐哈尔市泰来县"},
    {"id": 7, "name": "中共泰来县委组织部", "type": "党委", "level": "县处级", "parent": "中共泰来县委员会", "location": "黑龙江省齐齐哈尔市泰来县"},
    {"id": 8, "name": "中共泰来县委宣传部", "type": "党委", "level": "县处级", "parent": "中共泰来县委员会", "location": "黑龙江省齐齐哈尔市泰来县"},
    {"id": 9, "name": "中共泰来县委统战部", "type": "党委", "level": "县处级", "parent": "中共泰来县委员会", "location": "黑龙江省齐齐哈尔市泰来县"},
    {"id": 10, "name": "泰来县人民武装部", "type": "事业单位", "level": "县处级", "parent": "齐齐哈尔军分区", "location": "黑龙江省齐齐哈尔市泰来县"},
    {"id": 11, "name": "泰来县公安局", "type": "政府", "level": "县处级", "parent": "泰来县人民政府", "location": "黑龙江省齐齐哈尔市泰来县"},
    {"id": 12, "name": "泰来县经济开发区", "type": "开发区", "level": "县处级", "parent": "泰来县人民政府", "location": "黑龙江省齐齐哈尔市泰来县"},
]

# ── PERSONS ─────────────────────────────────────────────────────────

persons = [
    # ═══ 县委领导 ═══
    # 1 — 郑德利 — 县委书记
    {"id": 1, "name": "郑德利", "gender": "男", "ethnicity": "汉族",
     "birth": "1980年12月", "birthplace": "", "education": "大学，农业推广硕士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "中共泰来县委书记", "current_org": "中共泰来县委员会",
     "source": "https://www.tailai.gov.cn/tailai/c103730/202009/c02_248194.shtml"},
    # 2 — 曲喜民 — 县长
    {"id": 2, "name": "曲喜民", "gender": "男", "ethnicity": "汉族",
     "birth": "1982年3月", "birthplace": "", "education": "大学，管理学学士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泰来县委副书记、县政府县长", "current_org": "泰来县人民政府",
     "source": "https://www.tailai.gov.cn/tailai/c103735/202009/c02_248211.shtml"},
    # 3 — 徐春波 — 副书记、统战部长
    {"id": 3, "name": "徐春波", "gender": "男", "ethnicity": "汉族",
     "birth": "1973年11月", "birthplace": "", "education": "大学，农学学士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泰来县委副书记、统战部部长", "current_org": "中共泰来县委员会",
     "source": "https://www.tailai.gov.cn/tailai/c103731/202107/c02_379257.shtml"},
    # 4 — 王朋 — 政法委书记
    {"id": 4, "name": "王朋", "gender": "男", "ethnicity": "汉族",
     "birth": "1971年6月", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泰来县委常委、政法委书记", "current_org": "中共泰来县委政法委员会",
     "source": "https://www.tailai.gov.cn/tailai/c103732/202010/c02_379260.shtml"},
    # 5 — 赵志新 — 组织部长
    {"id": 5, "name": "赵志新", "gender": "男", "ethnicity": "汉族",
     "birth": "1973年8月", "birthplace": "", "education": "大学，管理学学士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泰来县委常委、组织部部长", "current_org": "中共泰来县委组织部",
     "source": "https://www.tailai.gov.cn/tailai/c103732/202010/c02_379261.shtml"},
    # 6 — 阚振波 — 县委常委、副县长
    {"id": 6, "name": "阚振波", "gender": "男", "ethnicity": "汉族",
     "birth": "1969年4月", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泰来县委常委、县政府副县长", "current_org": "泰来县人民政府",
     "source": "https://www.tailai.gov.cn/tailai/c103732/202109/c02_379262.shtml"},
    # 7 — 田宇 — 常务副县长
    {"id": 7, "name": "田宇", "gender": "男", "ethnicity": "汉族",
     "birth": "1981年5月", "birthplace": "", "education": "大学，省委党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泰来县委常委、县政府副县长（常务）", "current_org": "泰来县人民政府",
     "source": "https://www.tailai.gov.cn/tailai/c103736/202109/c02_248218.shtml"},
    # 8 — 孙岩 — 宣传部长
    {"id": 8, "name": "孙岩", "gender": "女", "ethnicity": "汉族",
     "birth": "1971年7月", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泰来县委常委、宣传部部长", "current_org": "中共泰来县委宣传部",
     "source": "https://www.tailai.gov.cn/tailai/c103732/202101/c02_379266.shtml"},
    # 9 — 韦超 — 县委办主任
    {"id": 9, "name": "韦超", "gender": "男", "ethnicity": "汉族",
     "birth": "1986年1月", "birthplace": "", "education": "大学，法学学士，中央党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泰来县委常委、县委办主任", "current_org": "中共泰来县委员会",
     "source": "https://www.tailai.gov.cn/tailai/c103732/202401/c02_444723.shtml"},
    # 10 — 张华 — 纪委书记
    {"id": 10, "name": "张华", "gender": "男", "ethnicity": "汉族",
     "birth": "1974年10月", "birthplace": "", "education": "大学，教育学学士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泰来县委常委、纪委书记、监委主任", "current_org": "中共泰来县纪律检查委员会",
     "source": "https://www.tailai.gov.cn/tailai/c103732/202107/c02_379258.shtml"},
    # 11 — 尹新 — 挂职副县长
    {"id": 11, "name": "尹新", "gender": "男", "ethnicity": "汉族",
     "birth": "1992年6月", "birthplace": "", "education": "大学，管理学学士，省委党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泰来县委常委、政府挂职副县长", "current_org": "泰来县人民政府",
     "source": "https://www.tailai.gov.cn/tailai/c103732/202505/c02_553475.shtml"},
    # 12 — 刘洪宇 — 人武部政委
    {"id": 12, "name": "刘洪宇", "gender": "男", "ethnicity": "汉族",
     "birth": "1981年9月", "birthplace": "", "education": "大学，工学学士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泰来县委常委、人武部上校政治委员", "current_org": "泰来县人民武装部",
     "source": "https://www.tailai.gov.cn/tailai/c103732/202010/c02_379265.shtml"},

    # ═══ 县政府领导 ═══
    # 13 — 李井凡 — 副县长
    {"id": 13, "name": "李井凡", "gender": "男", "ethnicity": "汉族",
     "birth": "1980年12月", "birthplace": "", "education": "大学，农业推广硕士",
     "party_join": "民建会员", "work_start": "",
     "current_post": "泰来县政府副县长", "current_org": "泰来县人民政府",
     "source": "https://www.tailai.gov.cn/tailai/c103736/202010/c02_248214.shtml"},
    # 14 — 姜兴业 — 副县长
    {"id": 14, "name": "姜兴业", "gender": "男", "ethnicity": "汉族",
     "birth": "1974年9月", "birthplace": "黑龙江泰来", "education": "黑龙江省中医药大学骨伤学专业",
     "party_join": "中共党员", "work_start": "1998年11月",
     "current_post": "泰来县政府副县长", "current_org": "泰来县人民政府",
     "source": "https://www.tailai.gov.cn/tailai/c103736/202010/c02_248212.shtml"},
    # 15 — 呼延莉 — 副县长
    {"id": 15, "name": "呼延莉", "gender": "女", "ethnicity": "蒙古族",
     "birth": "1977年11月", "birthplace": "", "education": "大学，党校研究生",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泰来县政府副县长", "current_org": "泰来县人民政府",
     "source": "https://www.tailai.gov.cn/tailai/c103736/202109/c02_248217.shtml"},
    # 16 — 朱瑞军 — 副县长、公安局长
    {"id": 16, "name": "朱瑞军", "gender": "男", "ethnicity": "汉族",
     "birth": "1972年5月", "birthplace": "", "education": "大学",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泰来县政府副县长、公安局局长", "current_org": "泰来县公安局",
     "source": "https://www.tailai.gov.cn/tailai/c103736/202106/c02_248216.shtml"},
    # 17 — 黄英来 — 挂职副县长
    {"id": 17, "name": "黄英来", "gender": "男", "ethnicity": "蒙古族",
     "birth": "1978年10月", "birthplace": "", "education": "大学，工学博士",
     "party_join": "中共党员", "work_start": "",
     "current_post": "泰来县政府挂职副县长", "current_org": "泰来县人民政府",
     "source": "https://www.tailai.gov.cn/tailai/c103736/202209/c02_248220.shtml"},

    # ═══ 人大领导 ═══
    # 18 — 赫萍 — 人大主任
    {"id": 18, "name": "赫萍", "gender": "女", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "泰来县人大常委会主任", "current_org": "泰来县人大常委会",
     "source": "https://www.tailai.gov.cn/tailai/c103733/202107/c02_248210.shtml"},
    # 19 — 倪茹伟 — 人大副主任
    {"id": 19, "name": "倪茹伟", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "泰来县人大常委会副主任", "current_org": "泰来县人大常委会",
     "source": "https://www.tailai.gov.cn/tailai/c103734/202009/c02_248206.shtml"},
    # 20 — 朱清江 — 人大副主任
    {"id": 20, "name": "朱清江", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "泰来县人大常委会副主任", "current_org": "泰来县人大常委会",
     "source": "https://www.tailai.gov.cn/tailai/c103734/202010/c02_248207.shtml"},
    # 21 — 郑军 — 人大副主任
    {"id": 21, "name": "郑军", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "泰来县人大常委会副主任", "current_org": "泰来县人大常委会",
     "source": "https://www.tailai.gov.cn/tailai/c103734/202010/c02_248208.shtml"},
    # 22 — 李彦会 — 人大副主任
    {"id": 22, "name": "李彦会", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "泰来县人大常委会副主任", "current_org": "泰来县人大常委会",
     "source": "https://www.tailai.gov.cn/tailai/c103734/202010/c02_248209.shtml"},

    # ═══ 政协领导 ═══
    # 23 — 于泳涛 — 政协主席
    {"id": 23, "name": "于泳涛", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "泰来县政协主席", "current_org": "泰来县政协",
     "source": "https://www.tailai.gov.cn/tailai/c103737/202109/c02_248223.shtml"},
    # 24 — 王继业 — 政协副主席
    {"id": 24, "name": "王继业", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "泰来县政协副主席", "current_org": "泰来县政协",
     "source": "https://www.tailai.gov.cn/tailai/c103738/202010/c02_248222.shtml"},
    # 25 — 张永忠 — 政协副主席
    {"id": 25, "name": "张永忠", "gender": "", "ethnicity": "", "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "泰来县政协副主席", "current_org": "泰来县政协",
     "source": "https://www.tailai.gov.cn/tailai/c103738/202010/c02_248221.shtml"},
]

# ── POSITIONS ──────────────────────────────────────────────────────

positions = [
    # 郑德利
    {"person_id": 1, "org_id": 1, "title": "中共泰来县委书记", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "主持县委全面工作"},

    # 曲喜民
    {"person_id": 2, "org_id": 1, "title": "泰来县委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "泰来县政府县长", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "兼任泰来县经济开发区党工委书记、管委会主任"},
    {"person_id": 2, "org_id": 12, "title": "泰来县经济开发区党工委书记、管委会主任", "start_date": "", "end_date": "present", "rank": "", "note": "兼任"},

    # 徐春波
    {"person_id": 3, "org_id": 1, "title": "泰来县委副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "协助书记抓日常党建、深化改革、乡村振兴"},
    {"person_id": 3, "org_id": 9, "title": "泰来县委统战部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},

    # 王朋
    {"person_id": 4, "org_id": 6, "title": "泰来县委常委、政法委书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},

    # 赵志新
    {"person_id": 5, "org_id": 7, "title": "泰来县委常委、组织部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},

    # 阚振波
    {"person_id": 6, "org_id": 1, "title": "泰来县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "泰来县政府副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "分管住建、城管、市场监管、民政"},

    # 田宇
    {"person_id": 7, "org_id": 1, "title": "泰来县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "泰来县政府副县长（常务）", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责政府常务工作"},

    # 孙岩
    {"person_id": 8, "org_id": 8, "title": "泰来县委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},

    # 韦超
    {"person_id": 9, "org_id": 1, "title": "泰来县委常委、县委办主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},

    # 张华
    {"person_id": 10, "org_id": 5, "title": "泰来县委常委、纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},

    # 尹新
    {"person_id": 11, "org_id": 1, "title": "泰来县委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "挂职"},
    {"person_id": 11, "org_id": 2, "title": "泰来县政府挂职副县长", "start_date": "", "end_date": "present", "rank": "", "note": "分管体育和旅游，推进县校共建"},

    # 刘洪宇
    {"person_id": 12, "org_id": 10, "title": "泰来县委常委、人武部上校政治委员", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},

    # 李井凡
    {"person_id": 13, "org_id": 2, "title": "泰来县政府副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "民建会员，分管教育、卫生健康"},

    # 姜兴业
    {"person_id": 14, "org_id": 2, "title": "泰来县政府副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "分管产业项目、工业经济、开发区"},

    # 呼延莉
    {"person_id": 15, "org_id": 2, "title": "泰来县政府副县长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "分管农业农村、乡村振兴、水务"},

    # 朱瑞军
    {"person_id": 16, "org_id": 11, "title": "泰来县政府副县长、公安局局长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": ""},

    # 黄英来
    {"person_id": 17, "org_id": 2, "title": "泰来县政府挂职副县长", "start_date": "", "end_date": "present", "rank": "", "note": "东北林业大学挂职"},
]

# ── RELATIONSHIPS ──────────────────────────────────────────────────

relationships = [
    # 党政正职搭档
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "泰来县党政正职搭档: 县委书记与县长", "overlap_org": "中共泰来县委员会/泰来县人民政府", "overlap_period": "current"},
    # 县委副书记搭档关系
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "县委书记与专职副书记", "overlap_org": "中共泰来县委员会", "overlap_period": "current"},
    # 县长与常务副县长
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "县长与常务副县长", "overlap_org": "泰来县人民政府", "overlap_period": "current"},
    # 县委常委班子
    {"person_a": 4, "person_b": 5, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共泰来县委员会", "overlap_period": "current"},
    {"person_a": 4, "person_b": 6, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共泰来县委员会", "overlap_period": "current"},
    {"person_a": 4, "person_b": 7, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共泰来县委员会", "overlap_period": "current"},
    {"person_a": 5, "person_b": 6, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共泰来县委员会", "overlap_period": "current"},
    {"person_a": 5, "person_b": 7, "type": "overlap", "context": "县委常委班子成员", "overlap_org": "中共泰来县委员会", "overlap_period": "current"},
    {"person_a": 5, "person_b": 10, "type": "overlap", "context": "县委常委班子成员：组织部长与纪委书记", "overlap_org": "中共泰来县委员会", "overlap_period": "current"},
    {"person_a": 9, "person_b": 1, "type": "overlap", "context": "县委办主任与县委书记", "overlap_org": "中共泰来县委员会", "overlap_period": "current"},
    # 县政府班子
    {"person_a": 2, "person_b": 6, "type": "overlap", "context": "县政府班子成员", "overlap_org": "泰来县人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 13, "type": "overlap", "context": "县政府班子成员", "overlap_org": "泰来县人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 14, "type": "overlap", "context": "县政府班子成员", "overlap_org": "泰来县人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 15, "type": "overlap", "context": "县政府班子成员", "overlap_org": "泰来县人民政府", "overlap_period": "current"},
    {"person_a": 2, "person_b": 16, "type": "overlap", "context": "县政府班子成员", "overlap_org": "泰来县人民政府", "overlap_period": "current"},
    # 姜兴业 — 本地干部（泰来出生）
    {"person_a": 14, "person_b": 1, "type": "overlap", "context": "姜兴业为泰来本地人，与县委书记郑德利在县委/县政府班子中共事", "overlap_org": "泰来县人民政府", "overlap_period": "current"},
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
    print("Build complete.")
