#!/usr/bin/env python3
"""龙沙区(齐齐哈尔市) 领导班子工作关系网络 — 数据构建脚本

研究日期: 2026-08-06
主要来源:
  - 龙沙区人民政府官网 领导之窗 https://www.qqhrlsq.gov.cn/lsq/c100242/xzf.shtml
    区委/区人大/区政府/区政协 领导简介页
  - 齐齐哈尔市人民政府 拟任职干部公示 (央广网/公众号) 2026-04-18, 2026-07-08
  - 齐齐哈尔市人民政府 齐政发干〔2026〕4号 王树文等任免职通知 (2026-05-15)
  - 汲古新知 "王友良已任齐齐哈尔市龙沙区代区长" (2024-03-05)
  - 人民网 2021-12-10 王树文采访

人物ID约定(去重用): {district}_{surname_givenname}
"""
import os
from datetime import date

TODAY = date.today().isoformat()
SLUG = "龙沙区"

BASE = os.path.dirname(os.path.abspath(__file__))
# 规范产物路径：统一写入 data/database 与 data/graph
if os.path.basename(BASE) == "build" and os.path.basename(os.path.dirname(BASE)) == "scripts":
    REPO = os.path.dirname(os.path.dirname(BASE))
else:
    REPO = os.path.dirname(os.path.dirname(os.path.dirname(BASE)))
# 暂存（staging）用 STAGING_DIR 环境变量覆盖输出目录；否则写规范化目录
_STAGING = os.environ.get("STAGING_DIR")
if _STAGING:
    DB_PATH = os.path.join(_STAGING, "龙沙区_network.db")
    GEXF_PATH = os.path.join(_STAGING, "龙沙区_network.gexf")
else:
    DB_PATH = os.path.join(REPO, "data", "database", "龙沙区_network.db")
    GEXF_PATH = os.path.join(REPO, "data", "graph", "龙沙区_network.gexf")

# ── RESEARCH DATA ──────────────────────────────────────────────────────────
persons = [
    # ── 核心:区委书记 ──
    {
        "id": 1, "name": "王友良", "gender": "男", "ethnicity": "汉族",
        "birth": "1978年4月", "birthplace": "山东临沂", "education": "研究生，法学硕士",
        "party_join": "中共党员", "work_start": "2003年7月",
        "current_post": "龙沙区委书记、区委党校校长、一级调研员", "current_org": "中共龙沙区委员会",
        "source": "https://www.qqhrlsq.gov.cn/"
    },
    # ── 核心:区长 ──
    {
        "id": 2, "name": "王世锋", "gender": "男", "ethnicity": "汉族",
        "birth": "1976年11月", "birthplace": "黑龙江讷河", "education": "省委党校研究生，经济管理",
        "party_join": "中共党员", "work_start": "2000年11月",
        "current_post": "龙沙区委副书记、区政府区长、党组书记", "current_org": "龙沙区人民政府",
        "source": "https://www.qqhrlsq.gov.cn/"
    },
    # ── 区委其他班子 ──
    {
        "id": 3, "name": "魏朝举", "gender": "男", "ethnicity": "汉族",
        "birth": "1971年11月", "birthplace": "", "education": "中央党校大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区委副书记、统战部部长，兼区政协党组副书记、三级调研员", "current_org": "中共龙沙区委员会",
        "source": "https://www.qqhrlsq.gov.cn/"
    },
    {
        "id": 4, "name": "王扬", "gender": "女", "ethnicity": "汉族",
        "birth": "1978年7月", "birthplace": "", "education": "在职大学，工商管理硕士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区委常委、组织部部长、区委党校第一副校长、三级调研员", "current_org": "中共龙沙区委员会",
        "source": "https://www.qqhrlsq.gov.cn/"
    },
    {
        "id": 5, "name": "邸文明", "gender": "男", "ethnicity": "汉族",
        "birth": "1974年6月", "birthplace": "", "education": "在职大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区委常委、纪委书记、监委主任、四级高级监察官", "current_org": "龙沙区纪律检查委员会",
        "source": "https://www.qqhrlsq.gov.cn/"
    },
    {
        "id": 6, "name": "何绮春", "gender": "男", "ethnicity": "汉族",
        "birth": "1972年4月", "birthplace": "", "education": "在职大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区委常委、区政府常务副区长、党组副书记、三级调研员", "current_org": "龙沙区人民政府",
        "source": "https://www.qqhrlsq.gov.cn/"
    },
    {
        "id": 7, "name": "董宝生", "gender": "男", "ethnicity": "汉族",
        "birth": "1974年5月", "birthplace": "", "education": "大学，工学学士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区委常委、宣传部部长、三级调研员", "current_org": "中共龙沙区委员会",
        "source": "https://www.qqhrlsq.gov.cn/"
    },
    {
        "id": 8, "name": "赵荣启", "gender": "男", "ethnicity": "汉族",
        "birth": "1977年11月", "birthplace": "", "education": "大学，工学学士，工商管理硕士",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区委常委、政法委书记、三级调研员", "current_org": "中共龙沙区委员会",
        "source": "https://www.qqhrlsq.gov.cn/"
    },
    {
        "id": 9, "name": "庞永", "gender": "男", "ethnicity": "汉族",
        "birth": "1977年6月", "birthplace": "", "education": "大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区委常委、人民武装部部长", "current_org": "龙沙区人民武装部",
        "source": "https://www.qqhrlsq.gov.cn/"
    },
    {
        "id": 10, "name": "于舟", "gender": "男", "ethnicity": "汉族",
        "birth": "1991年1月", "birthplace": "", "education": "全日制大学",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区委常委、区政府副区长（挂职）、党组成员", "current_org": "龙沙区人民政府",
        "source": "https://www.qqhrlsq.gov.cn/"
    },
    # ── 区政府副区长（非常委）──
    {
        "id": 11, "name": "魏巍", "gender": "男", "ethnicity": "汉族",
        "birth": "1982年1月", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区政府副区长、党组成员", "current_org": "龙沙区人民政府",
        "source": "https://www.qqhrlsq.gov.cn/"
    },
    {
        "id": 12, "name": "孙智嘉", "gender": "男", "ethnicity": "汉族",
        "birth": "1972年7月", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区政府副区长、党组成员，市公安局龙沙分局局长、三级高级警长", "current_org": "龙沙区人民政府",
        "source": "https://www.qqhrlsq.gov.cn/"
    },
    {
        "id": 13, "name": "王汝新", "gender": "男", "ethnicity": "汉族",
        "birth": "1984年1月", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区政府副区长、党组成员、三级调研员", "current_org": "龙沙区人民政府",
        "source": "https://www.qqhrlsq.gov.cn/"
    },
    # ── 区人大 ──
    {
        "id": 14, "name": "李莉", "gender": "女", "ethnicity": "汉族",
        "birth": "1973年9月", "birthplace": "吉林公主岭", "education": "齐齐哈尔大学研究生，法学硕士",
        "party_join": "中共党员", "work_start": "1996年8月",
        "current_post": "区人大常委会主任、党组书记、一级调研员", "current_org": "龙沙区人大常委会",
        "source": "https://www.qqhrlsq.gov.cn/"
    },
    {
        "id": 15, "name": "孙洪巍", "gender": "男", "ethnicity": "汉族",
        "birth": "1968年8月", "birthplace": "辽宁沈阳", "education": "齐齐哈尔大学自考艺术设计大专",
        "party_join": "中共党员", "work_start": "1988年7月",
        "current_post": "区人大常委会副主任、党组副书记、三级调研员", "current_org": "龙沙区人大常委会",
        "source": "https://www.qqhrlsq.gov.cn/"
    },
    {
        "id": 16, "name": "王美杰", "gender": "女", "ethnicity": "汉族",
        "birth": "1972年3月", "birthplace": "辽宁辽阳", "education": "国家开放大学行政管理大专",
        "party_join": "", "work_start": "1988年3月",
        "current_post": "区人大常委会副主任", "current_org": "龙沙区人大常委会",
        "source": "https://www.qqhrlsq.gov.cn/"
    },
    {
        "id": 17, "name": "杨曙光", "gender": "男", "ethnicity": "汉族",
        "birth": "1967年2月", "birthplace": "黑龙江嫩江", "education": "省委党校经济管理研究生",
        "party_join": "中共党员", "work_start": "1990年9月",
        "current_post": "区人大常委会副主任、党组成员、法制委员会主任委员、三级调研员", "current_org": "龙沙区人大常委会",
        "source": "https://www.qqhrlsq.gov.cn/"
    },
    {
        "id": 18, "name": "姜永忠", "gender": "男", "ethnicity": "汉族",
        "birth": "1968年8月", "birthplace": "黑龙江富裕", "education": "东北师范大学体育大学",
        "party_join": "中共党员", "work_start": "1988年7月",
        "current_post": "区人大常委会副主任、党组成员、财经委员会主任委员、三级调研员", "current_org": "龙沙区人大常委会",
        "source": "https://www.qqhrlsq.gov.cn/"
    },
    # ── 区政协 ──
    {
        "id": 19, "name": "田忠启", "gender": "男", "ethnicity": "汉族",
        "birth": "1969年4月", "birthplace": "山东成武", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区政协主席、党组书记、一级调研员", "current_org": "龙沙区政协",
        "source": "https://www.qqhrlsq.gov.cn/"
    },
    {
        "id": 20, "name": "齐士宏", "gender": "男", "ethnicity": "汉族",
        "birth": "1968年9月", "birthplace": "黑龙江宾县", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "区政协副主席、党组副书记", "current_org": "龙沙区政协",
        "source": "https://www.qqhrlsq.gov.cn/"
    },
    {
        "id": 21, "name": "张桓", "gender": "男", "ethnicity": "汉族",
        "birth": "1982年7月", "birthplace": "", "education": "省委党校研究生", "party_join": "农工党员", "work_start": "",
        "current_post": "区政协副主席", "current_org": "龙沙区政协",
        "source": "https://www.qqhrlsq.gov.cn/"
    },
    {
        "id": 22, "name": "田野", "gender": "男", "ethnicity": "汉族",
        "birth": "1982年6月", "birthplace": "黑龙江泰来", "education": "",
        "party_join": "九三学社", "work_start": "",
        "current_post": "区政协副主席（不驻会）、区工商联主席", "current_org": "龙沙区政协",
        "source": "https://www.qqhrlsq.gov.cn/"
    },
    # ── 前任领导（人事网络）──
    {
        "id": 23, "name": "王树文", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "前龙沙区委书记，现任齐齐哈尔市政府副秘书长", "current_org": "齐齐哈尔市人民政府",
        "source": "https://www.qqhr.gov.cn/"
    },
    {
        "id": 24, "name": "曲文珣", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "前龙沙区区长（2023年被查）", "current_org": "龙沙区人民政府",
        "source": "汲古新知 2024-03-05"
    },
]

organizations = [
    {"id": 1, "name": "中共龙沙区委员会", "type": "党委", "level": "区级", "parent": "中共齐齐哈尔市委", "location": "齐齐哈尔市龙沙区"},
    {"id": 2, "name": "龙沙区人民政府", "type": "政府", "level": "区级", "parent": "齐齐哈尔市人民政府", "location": "齐齐哈尔市龙沙区"},
    {"id": 3, "name": "龙沙区纪律检查委员会", "type": "党委", "level": "区级", "parent": "龙沙区委员会", "location": "齐齐哈尔市龙沙区"},
    {"id": 4, "name": "龙沙区人民武装部", "type": "事业单位", "level": "区级", "parent": "龙沙区委员会", "location": "齐齐哈尔市龙沙区"},
    {"id": 5, "name": "龙沙区人大常委会", "type": "人大", "level": "区级", "parent": "龙沙区", "location": "齐齐哈尔市龙沙区"},
    {"id": 6, "name": "龙沙区政协", "type": "政协", "level": "区级", "parent": "龙沙区", "location": "齐齐哈尔市龙沙区"},
    {"id": 7, "name": "齐齐哈尔市人民政府", "type": "政府", "level": "市级", "parent": "黑龙江省人民政府", "location": "齐齐哈尔市"},
    {"id": 8, "name": "齐齐哈尔市市场监督管理局", "type": "政府", "level": "市级", "parent": "齐齐哈尔市人民政府", "location": "齐齐哈尔市"},
    {"id": 9, "name": "龙江县政府", "type": "政府", "level": "县级", "parent": "齐齐哈尔市人民政府", "location": "齐齐哈尔市龙江县"},
    {"id": 10, "name": "依安县委", "type": "党委", "level": "县级", "parent": "中共齐齐哈尔市委", "location": "齐齐哈尔市依安县"},
    {"id": 11, "name": "齐齐哈尔市经济合作促进局", "type": "政府", "level": "市级", "parent": "齐齐哈尔市人民政府", "location": "齐齐哈尔市"},
]

positions = [
    # 王友良 (1)
    {"person_id": 1, "org_id": 1, "title": "区委书记、区委党校校长、一级调研员", "start_date": "2026", "end_date": "present", "rank": "县处级正职"},
    {"person_id": 1, "org_id": 2, "title": "区长", "start_date": "2024-03", "end_date": "2026", "rank": "县处级正职", "note": "2024-03-13 区八届人大五次会议当选区长；后任区委书记，曾短暂一肩挑"},
    {"person_id": 1, "org_id": 11, "title": "局长", "start_date": "2022-05", "end_date": "2024-02", "rank": "县处级"},
    {"person_id": 1, "org_id": 10, "title": "县委副书记、统战部部长", "start_date": "2020-06", "end_date": "2022-05", "rank": "县处级"},
    {"person_id": 1, "org_id": 9, "title": "县委常委、组织部部长", "start_date": "2018-02", "end_date": "2020-06", "rank": "县处级"},
    {"person_id": 1, "org_id": 9, "title": "副县长", "start_date": "2016-11", "end_date": "2018-02", "rank": "县处级"},
    {"person_id": 1, "org_id": 9, "title": "挂职副县长", "start_date": "2015-01", "end_date": "2016-11", "rank": "县处级"},
    # 王世锋 (2)
    {"person_id": 2, "org_id": 2, "title": "区委副书记、区长、党组书记", "start_date": "2026-07", "end_date": "present", "rank": "县处级正"},
    {"person_id": 2, "org_id": 8, "title": "局长、党组书记、市政府食品安全委员会办公室主任", "start_date": "", "end_date": "2026-06", "rank": "县处级"},
    # 魏朝举 (3)
    {"person_id": 3, "org_id": 1, "title": "区委副书记、统战部部长、区政协党组副书记", "start_date": "", "end_date": "present", "rank": "县处级"},
    # 王扬 (4)
    {"person_id": 4, "org_id": 1, "title": "区委常委、组织部部长、区委党校第一副校长", "start_date": "", "end_date": "present", "rank": "县处级"},
    # 邸文明 (5)
    {"person_id": 5, "org_id": 3, "title": "区委常委、纪委书记、监委主任", "start_date": "", "end_date": "present", "rank": "县处级"},
    # 何绮春 (6)
    {"person_id": 6, "org_id": 2, "title": "区委常委、常务副区长、党组副书记", "start_date": "", "end_date": "present", "rank": "县处级"},
    # 董宝生 (7)
    {"person_id": 7, "org_id": 1, "title": "区委常委、宣传部部长", "start_date": "", "end_date": "present", "rank": "县处级"},
    # 赵荣启 (8)
    {"person_id": 8, "org_id": 1, "title": "区委常委、政法委书记", "start_date": "", "end_date": "present", "rank": "县处级"},
    # 庞永 (9)
    {"person_id": 9, "org_id": 4, "title": "区委常委、人民武装部部长", "start_date": "", "end_date": "present", "rank": "县处级"},
    # 于舟 (10)
    {"person_id": 10, "org_id": 2, "title": "区委常委、副区长（挂职）", "start_date": "", "end_date": "present", "rank": "挂职"},
    # 魏巍 (11)
    {"person_id": 11, "org_id": 2, "title": "副区长、党组成员", "start_date": "", "end_date": "present", "rank": "县处级"},
    # 孙智嘉 (12)
    {"person_id": 12, "org_id": 2, "title": "副区长、市公安局龙沙分局局长", "start_date": "", "end_date": "present", "rank": "县处级"},
    # 王汝新 (13)
    {"person_id": 13, "org_id": 2, "title": "副区长、党组成员、三级调研员", "start_date": "", "end_date": "present", "rank": "县处级"},
    # 人大
    {"person_id": 14, "org_id": 5, "title": "区人大常委会主任、党组书记", "start_date": "", "end_date": "present", "rank": "县处级"},
    {"person_id": 15, "org_id": 5, "title": "区人大常委会副主任、党组副书记", "start_date": "", "end_date": "present", "rank": "县处级"},
    {"person_id": 16, "org_id": 5, "title": "区人大常委会副主任", "start_date": "", "end_date": "present", "rank": "县处级"},
    {"person_id": 17, "org_id": 5, "title": "区人大常委会副主任", "start_date": "", "end_date": "present", "rank": "县处级"},
    {"person_id": 18, "org_id": 5, "title": "区人大常委会副主任", "start_date": "", "end_date": "present", "rank": "县处级"},
    # 政协
    {"person_id": 19, "org_id": 6, "title": "区政协主席、党组书记", "start_date": "", "end_date": "present", "rank": "县处级"},
    {"person_id": 20, "org_id": 6, "title": "区政协副主席、党组副书记", "start_date": "", "end_date": "present", "rank": "县处级"},
    {"person_id": 21, "org_id": 6, "title": "区政协副主席", "start_date": "", "end_date": "present", "rank": "县处级"},
    {"person_id": 22, "org_id": 6, "title": "区政协副主席（不驻会）、区工商联主席", "start_date": "", "end_date": "present", "rank": "县处级"},
    # 前任
    {"person_id": 23, "org_id": 7, "title": "市政府副秘书长", "start_date": "2026-04", "end_date": "present", "rank": "市府副秘书长"},
    {"person_id": 23, "org_id": 1, "title": "区委书记", "start_date": "", "end_date": "2026-04", "rank": "区处级正"},
    {"person_id": 24, "org_id": 2, "title": "区长", "start_date": "", "end_date": "2023", "rank": "区处级正", "note": "2023-10 被齐齐哈尔市纪委监委立案审查调查"},
]

relationships = [  # (person_a, person_b, type, context, overlap_org, overlap_period)
    # 党政主官
    {"person_a": 1, "person_b": 2, "type": "上下级", "context": "现任区委书记王友良与现任区长王世锋党政搭配", "overlap_org": "龙沙区委", "overlap_period": "2026-至今"},
    # 书记-副书记/常委
    {"person_a": 1, "person_b": 3, "type": "班子成员", "context": "区委书记与区委副书记同班子", "overlap_org": "龙沙区委", "overlap_period": "2026-至今"},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "区委书记与组织部长（党建分工）", "overlap_org": "龙沙区委", "overlap_period": "2026-至今"},
    {"person_a": 1, "person_b": 5, "type": "班子成员", "context": "区委书记与纪委书记同班子", "overlap_org": "龙沙区委", "overlap_period": "2026-至今"},
    {"person_a": 1, "person_b": 6, "type": "班子成员", "context": "区委书记与常务副区长同班子", "overlap_org": "龙沙区委", "overlap_period": "2026-至今"},
    # 区长-副区长
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "区长与常务副区长上下级", "overlap_org": "龙沙区人民政府", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 11, "type": "上下级", "context": "区长与副区长工作关系", "overlap_org": "龙沙区人民政府", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "区长与副区长（公安系统）", "overlap_org": "龙沙区人民政府", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 13, "type": "上下级", "context": "区长与副区长工作关系", "overlap_org": "龙沙区人民政府", "overlap_period": "2026-至今"},
    # 前任继任链
    {"person_a": 1, "person_b": 23, "type": "前任继任", "context": "王友良接任王树文区委书记职务", "overlap_org": "龙沙区委", "overlap_period": "2026"},
    {"person_a": 1, "person_b": 24, "type": "前任继任", "context": "王友良接任曲文珣区长（曲2023被查）", "overlap_org": "龙沙区人民政府", "overlap_period": "2024"},
    # 跨机构桥接
    {"person_a": 6, "person_b": 11, "type": "同事", "context": "常务副区长与副区长同政府班子", "overlap_org": "龙沙区人民政府", "overlap_period": "2026-至今"},
    {"person_a": 6, "person_b": 13, "type": "同事", "context": "常务副区长与副区长同政府班子", "overlap_org": "龙沙区人民政府", "overlap_period": "2026-至今"},
]


# ── DATABASE BUILD ─────────────────────────────────────────────────────────

def create_tables(conn):
    conn.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS organizations;
        DROP TABLE IF EXISTS persons;
        CREATE TABLE persons (
            id INTEGER PRIMARY KEY,
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
        CREATE TABLE IF NOT EXISTS organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT DEFAULT '',
            start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '',
            note TEXT DEFAULT ''
        );
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a INTEGER NOT NULL,
            person_b INTEGER NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT ''
        );
    """)


def build():
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    create_tables(conn)

    cols_p = ["id", "name", "gender", "ethnicity", "birth", "birthplace", "education",
              "party_join", "work_start", "current_post", "current_org", "source"]
    for p in persons:
        vals = [p.get(c, "") for c in cols_p]
        conn.execute(f"INSERT INTO persons ({','.join(cols_p)}) VALUES ({','.join(['?'] * len(cols_p))})", vals)

    cols_o = ["id", "name", "type", "level", "parent", "location"]
    for o in organizations:
        vals = [o.get(c, "") for c in cols_o]
        conn.execute(f"INSERT INTO organizations ({','.join(cols_o)}) VALUES ({','.join(['?'] * len(cols_o))})", vals)

    cols_pos = ["person_id", "org_id", "title", "start_date", "end_date", "rank", "note"]
    for pos in positions:
        vals = [pos.get(c, "") for c in cols_pos]
        conn.execute(f"INSERT INTO positions ({','.join(cols_pos)}) VALUES ({','.join(['?'] * len(cols_pos))})", vals)

    cols_r = ["person_a", "person_b", "type", "context", "overlap_org", "overlap_period"]
    for r in relationships:
        vals = [r.get(c, "") for c in cols_r]
        conn.execute(f"INSERT INTO relationships ({','.join(cols_r)}) VALUES ({','.join(['?'] * len(cols_r))})", vals)

    conn.commit()
    conn.close()

    # ── GEXF ──────────────────────────────────────────────────────────
    def esc(s):
        if s is None:
            return ""
        return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

    def person_color(post):
        if "区委书记" in post and "副书记" not in post:
            return ("255,50,50", 20.0)
        elif "区长" in post:
            return ("50,100,255", 20.0)
        elif "纪委书记" in post or "监委主任" in post:
            return ("255,165,0", 15.0)
        elif "人大主任" in post:
            return ("200,255,255", 15.0)
        elif "政协主席" in post:
            return ("255,240,200", 15.0)
        elif "副区长" in post:
            return ("100,100,255", 12.0)
        else:
            return ("100,100,100", 12.0)

    def org_color(typ):
        return {
            "党委": ("255,200,200"),
            "政府": ("200,200,255"),
            "人大": ("200,255,255"),
            "政协": ("255,240,200"),
            "事业单位": ("220,220,220"),
        }.get(typ, ("200,200,200"))

    import sqlite3 as _s
    _conn = _s.connect(DB_PATH)
    person_rows = _conn.execute("SELECT id,name,current_post,current_org FROM persons").fetchall()
    org_rows = _conn.execute("SELECT id,name,type FROM organizations").fetchall()

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{TODAY}">')
    lines.append('    <creator>gov-relation research agent</creator>')
    lines.append('    <description>龙沙区领导班子工作关系网络</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="kind" type="string"/>')
    lines.append('    </attributes>')
    lines.append('    <nodes>')
    for r in person_rows:
        c, sz = person_color(r[2])
        lines.append(f'      <node id="p{r[0]}" label="{esc(r[1])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="person"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append('      </node>')
    for r in org_rows:
        c = org_color(r[2])
        lines.append(f'      <node id="o{r[0]}" label="{esc(r[1])}">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="organization"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}"/>')
        lines.append('        <viz:size value="8.0"/>')
        lines.append('      </node>')
    lines.append('    </nodes>')

    lines.append('    <edges>')
    eid = 0
    for pos in positions:
        lines.append(f'      <edge id="e{eid}" source="p{pos["person_id"]}" target="o{pos["org_id"]}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues><attvalue for="0" value="worked_at"/></attvalues>')
        lines.append('      </edge>')
        eid += 1
    for r in relationships:
        lines.append(f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues><attvalue for="0" value="relationship"/></attvalues>')
        lines.append('      </edge>')
        eid += 1
    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\n  DB: {DB_PATH}")
    print(f"  人物: {len(persons)} 人")
    print(f"  机构: {len(organizations)} 个")
    print(f"  任职: {len(positions)} 条")
    print(f"  关系: {len(relationships)} 条")
    print(f"  GEXF: {GEXF_PATH}")


if __name__ == "__main__":
    build()