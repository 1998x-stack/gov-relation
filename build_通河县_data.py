#!/usr/bin/env python3
"""通河县（哈尔滨市）领导班子关系网络生成脚本

数据来源：
  - 通河县人民政府官网 (www.hrbtonghe.gov.cn) 领导信息页面
  - 通河县人民政府官网新闻报道
  - 通河县人民政府官网人事信息（任前公示）

数据截至：2026年7月

Target roles:
  - 县委书记: 高俊杰
  - 县委副书记、县长: 孟祥伟
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ── Ensure gov_relation is importable ──
_script_dir = Path(__file__).resolve().parent
# Staging path: data/tmp/heilongjiang_通河县/ -> need 3 levels up for repo root
_REPO_CANDIDATE = _script_dir.parent.parent.parent
if (_REPO_CANDIDATE / "gov_relation").is_dir():
    sys.path.insert(0, str(_REPO_CANDIDATE))
else:
    sys.path.insert(0, str(_script_dir.parent.parent))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── Paths ──
STAGING = Path(__file__).parent
DB_PATH = STAGING / "通河县_network.db"
GEXF_PATH = STAGING / "通河县_network.gexf"
PERSONS_DIR = STAGING

TODAY = "2026-07-24"
AS_OF = TODAY

# =========================================================================
# DATA
# =========================================================================

person_id_map = {}  # name -> id
_pid = [0]

def next_id():
    _pid[0] += 1
    return _pid[0]

# ── Persons ──
persons = []

# 1. 高俊杰 — 县委书记
p = {
    "id": next_id(),
    "name": "高俊杰",
    "gender": "男",
    "ethnicity": "汉族",
    "birth": "1974-07",
    "birthplace": "黑龙江省大庆市",
    "education": "哈尔滨工业大学机械设计及制造专业毕业",
    "party_join": "2002-12",
    "work_start": "1996-07",
    "current_post": "县委书记",
    "current_org": "中共通河县委员会",
    "source": "https://www.hrbtonghe.gov.cn/hebthxx/c109569/202101/c01_450708.shtml",
}
person_id_map[p["name"]] = p["id"]
persons.append(p)

# 2. 孟祥伟 — 县委副书记、县长
p = {
    "id": next_id(),
    "name": "孟祥伟",
    "gender": "男",
    "ethnicity": "满族",
    "birth": "1978-09",
    "birthplace": "黑龙江省哈尔滨市",
    "education": "哈尔滨工业大学公共管理专业在职研究生",
    "party_join": "1998-12",
    "work_start": "1999-09",
    "current_post": "县委副书记、县长",
    "current_org": "通河县人民政府",
    "source": "https://www.hrbtonghe.gov.cn/hebthxx/c109571/202101/c01_377193.shtml",
}
person_id_map[p["name"]] = p["id"]
persons.append(p)

# 3. 赵春明 — 县委副书记
p = {
    "id": next_id(),
    "name": "赵春明",
    "gender": "男",
    "ethnicity": "汉族",
    "birth": "1972-06",
    "birthplace": "黑龙江五常",
    "education": "黑龙江省委党校经济管理专业在职研究生",
    "party_join": "1993-06",
    "work_start": "1991-09",
    "current_post": "县委副书记",
    "current_org": "中共通河县委员会",
    "source": "https://www.hrbtonghe.gov.cn/hebthxx/c109569/202111/c01_450707.shtml",
}
person_id_map[p["name"]] = p["id"]
persons.append(p)

# 4. 潘旭明 — 县委副书记（挂职）
p = {
    "id": next_id(),
    "name": "潘旭明",
    "gender": "男",
    "ethnicity": "汉族",
    "birth": "1987-10",
    "birthplace": "黑龙江省双鸭山市",
    "education": "中国海洋大学水产专业，理学博士",
    "party_join": "2010-01",
    "work_start": "2015-09",
    "current_post": "县委副书记（挂职）",
    "current_org": "中共通河县委员会",
    "source": "https://www.hrbtonghe.gov.cn/hebthxx/c109569/202504/c01_1053610.shtml",
}
person_id_map[p["name"]] = p["id"]
persons.append(p)

# 5. 荆勇 — 县委常委、组织部部长
p = {
    "id": next_id(),
    "name": "荆勇",
    "gender": "男",
    "ethnicity": "汉族",
    "birth": "1972-12",
    "birthplace": "黑龙江依安",
    "education": "国家开放大学行政管理专业",
    "party_join": "1996-04",
    "work_start": "1994-07",
    "current_post": "县委常委、组织部部长",
    "current_org": "中共通河县委组织部",
    "source": "https://www.hrbtonghe.gov.cn/hebthxx/c109569/202111/c01_450704.shtml",
}
person_id_map[p["name"]] = p["id"]
persons.append(p)

# 6. 李颖 — 县委常委、常务副县长
p = {
    "id": next_id(),
    "name": "李颖",
    "gender": "女",
    "ethnicity": "汉族",
    "birth": "1976-12",
    "birthplace": "黑龙江依兰",
    "education": "研究生学历",
    "party_join": "1996-07",
    "work_start": "1996-07",
    "current_post": "县委常委、政府常务副县长",
    "current_org": "通河县人民政府",
    "source": "https://www.hrbtonghe.gov.cn/hebthxx/c109569/201911/c01_450711.shtml",
}
person_id_map[p["name"]] = p["id"]
persons.append(p)

# 7. 赵鹏辉 — 县委常委、宣传部部长
p = {
    "id": next_id(),
    "name": "赵鹏辉",
    "gender": "男",
    "ethnicity": "汉族",
    "birth": "1972-05",
    "birthplace": "黑龙江通河",
    "education": "哈尔滨市委党校法律专业本科",
    "party_join": "1997-11",
    "work_start": "1996-11",
    "current_post": "县委常委、宣传部部长",
    "current_org": "中共通河县委宣传部",
    "source": "https://www.hrbtonghe.gov.cn/hebthxx/c109569/201911/c01_450710.shtml",
}
person_id_map[p["name"]] = p["id"]
persons.append(p)

# 8. 徐鸣超 — 县委常委、副县长
p = {
    "id": next_id(),
    "name": "徐鸣超",
    "gender": "男",
    "ethnicity": "汉族",
    "birth": "1983-07",
    "birthplace": "黑龙江方正",
    "education": "黑龙江省委党校公共管理专业在职研究生",
    "party_join": "2005-04",
    "work_start": "2006-03",
    "current_post": "县委常委、政府副县长",
    "current_org": "通河县人民政府",
    "source": "https://www.hrbtonghe.gov.cn/hebthxx/c109569/202111/c01_1034495.shtml",
}
person_id_map[p["name"]] = p["id"]
persons.append(p)

# 9. 陈建名 — 县委常委、政法委书记
p = {
    "id": next_id(),
    "name": "陈建名",
    "gender": "男",
    "ethnicity": "汉族",
    "birth": "1981-07",
    "birthplace": "黑龙江省哈尔滨市",
    "education": "东北林业大学毕业，南京农业大学博士后",
    "party_join": "2002-07",
    "work_start": "2004-07",
    "current_post": "县委常委、政法委书记",
    "current_org": "中共通河县委政法委员会",
    "source": "https://www.hrbtonghe.gov.cn/hebthxx/c109569/202105/c01_450713.shtml",
}
person_id_map[p["name"]] = p["id"]
persons.append(p)

# 10. 李僖讴 — 县委常委、纪委书记、监委主任
p = {
    "id": next_id(),
    "name": "李僖讴",
    "gender": "男",
    "ethnicity": "汉族",
    "birth": "1979-11",
    "birthplace": "黑龙江哈尔滨",
    "education": "国家开放大学法律事务专业",
    "party_join": "2002-10",
    "work_start": "1998-09",
    "current_post": "县委常委、县纪委书记、县监委主任",
    "current_org": "中共通河县纪律检查委员会",
    "source": "https://www.hrbtonghe.gov.cn/hebthxx/c109569/202402/c01_966599.shtml",
}
person_id_map[p["name"]] = p["id"]
persons.append(p)

# 11. 张静 — 县委常委、统战部部长
p = {
    "id": next_id(),
    "name": "张静",
    "gender": "女",
    "ethnicity": "汉族",
    "birth": "1980-09",
    "birthplace": "黑龙江省方正县",
    "education": "哈尔滨商业大学金融学，经济学学士",
    "party_join": "2002-12",
    "work_start": "2005-08",
    "current_post": "县委常委、统战部部长",
    "current_org": "中共通河县委统战部",
    "source": "https://www.hrbtonghe.gov.cn/hebthxx/c109569/202111/c01_377190.shtml",
}
person_id_map[p["name"]] = p["id"]
persons.append(p)

# 12. 王思库 — 县人大常委会主任
p = {
    "id": next_id(),
    "name": "王思库",
    "gender": "男",
    "ethnicity": "汉族",
    "birth": "",
    "birthplace": "",
    "education": "",
    "party_join": "",
    "work_start": "",
    "current_post": "县人大常委会主任",
    "current_org": "通河县人大常委会",
    "source": "https://www.hrbtonghe.gov.cn/hebthxx/c109570/201911/c01_377202.shtml",
}
person_id_map[p["name"]] = p["id"]
persons.append(p)

# 13. 管耀辉 — 县人大常委会副主任
p = {
    "id": next_id(),
    "name": "管耀辉",
    "gender": "男",
    "ethnicity": "汉族",
    "birth": "",
    "birthplace": "",
    "education": "",
    "party_join": "",
    "work_start": "",
    "current_post": "县人大常委会副主任",
    "current_org": "通河县人大常委会",
    "source": "https://www.hrbtonghe.gov.cn/hebthxx/c109570/201911/c01_377201.shtml",
}
person_id_map[p["name"]] = p["id"]
persons.append(p)

# 14. 张国志 — 县人大常委会副主任
p = {
    "id": next_id(),
    "name": "张国志",
    "gender": "男",
    "ethnicity": "汉族",
    "birth": "",
    "birthplace": "",
    "education": "",
    "party_join": "",
    "work_start": "",
    "current_post": "县人大常委会副主任",
    "current_org": "通河县人大常委会",
    "source": "https://www.hrbtonghe.gov.cn/hebthxx/c109570/201911/c01_377200.shtml",
}
person_id_map[p["name"]] = p["id"]
persons.append(p)

# 15. 宋瑞宏 — 县人大常委会副主任
p = {
    "id": next_id(),
    "name": "宋瑞宏",
    "gender": "男",
    "ethnicity": "汉族",
    "birth": "",
    "birthplace": "",
    "education": "",
    "party_join": "",
    "work_start": "",
    "current_post": "县人大常委会副主任",
    "current_org": "通河县人大常委会",
    "source": "https://www.hrbtonghe.gov.cn/hebthxx/c109570/201911/c01_377199.shtml",
}
person_id_map[p["name"]] = p["id"]
persons.append(p)

# 16. 宋喜波 — 县人大常委会副主任
p = {
    "id": next_id(),
    "name": "宋喜波",
    "gender": "男",
    "ethnicity": "汉族",
    "birth": "",
    "birthplace": "",
    "education": "",
    "party_join": "",
    "work_start": "",
    "current_post": "县人大常委会副主任",
    "current_org": "通河县人大常委会",
    "source": "https://www.hrbtonghe.gov.cn/hebthxx/c109570/202603/c01_1113280.shtml",
}
person_id_map[p["name"]] = p["id"]
persons.append(p)

# 17. 赵宏宝 — 副县长
p = {
    "id": next_id(),
    "name": "赵宏宝",
    "gender": "男",
    "ethnicity": "汉族",
    "birth": "",
    "birthplace": "",
    "education": "",
    "party_join": "",
    "work_start": "",
    "current_post": "副县长",
    "current_org": "通河县人民政府",
    "source": "https://www.hrbtonghe.gov.cn/hebthxx/c109571/201911/c01_377197.shtml",
}
person_id_map[p["name"]] = p["id"]
persons.append(p)

# 18. 商震 — 副县长
p = {
    "id": next_id(),
    "name": "商震",
    "gender": "男",
    "ethnicity": "汉族",
    "birth": "",
    "birthplace": "",
    "education": "",
    "party_join": "",
    "work_start": "",
    "current_post": "副县长",
    "current_org": "通河县人民政府",
    "source": "https://www.hrbtonghe.gov.cn/hebthxx/c109571/202311/c01_946313.shtml",
}
person_id_map[p["name"]] = p["id"]
persons.append(p)

# 19. 贾文鹏 — 副县长
p = {
    "id": next_id(),
    "name": "贾文鹏",
    "gender": "男",
    "ethnicity": "汉族",
    "birth": "",
    "birthplace": "",
    "education": "",
    "party_join": "",
    "work_start": "",
    "current_post": "副县长",
    "current_org": "通河县人民政府",
    "source": "https://www.hrbtonghe.gov.cn/hebthxx/c109571/202311/c01_946315.shtml",
}
person_id_map[p["name"]] = p["id"]
persons.append(p)

# 20. 葛书范 — 副县长
p = {
    "id": next_id(),
    "name": "葛书范",
    "gender": "男",
    "ethnicity": "汉族",
    "birth": "",
    "birthplace": "",
    "education": "",
    "party_join": "",
    "work_start": "",
    "current_post": "副县长",
    "current_org": "通河县人民政府",
    "source": "https://www.hrbtonghe.gov.cn/hebthxx/c109571/202412/c01_1034296.shtml",
}
person_id_map[p["name"]] = p["id"]
persons.append(p)

# 21. 马哲 — 县政协主席
p = {
    "id": next_id(),
    "name": "马哲",
    "gender": "男",
    "ethnicity": "汉族",
    "birth": "",
    "birthplace": "",
    "education": "",
    "party_join": "",
    "work_start": "",
    "current_post": "县政协主席",
    "current_org": "通河县政协",
    "source": "https://www.hrbtonghe.gov.cn/hebthxx/c109572/202111/c01_377185.shtml",
}
person_id_map[p["name"]] = p["id"]
persons.append(p)

# 22. 王厚平 — 县政协副主席
p = {
    "id": next_id(),
    "name": "王厚平",
    "gender": "男",
    "ethnicity": "汉族",
    "birth": "",
    "birthplace": "",
    "education": "",
    "party_join": "",
    "work_start": "",
    "current_post": "县政协副主席",
    "current_org": "通河县政协",
    "source": "https://www.hrbtonghe.gov.cn/hebthxx/c109572/202502/c01_1042423.shtml",
}
person_id_map[p["name"]] = p["id"]
persons.append(p)

# 23. 曲春林 — 县政协副主席
p = {
    "id": next_id(),
    "name": "曲春林",
    "gender": "男",
    "ethnicity": "汉族",
    "birth": "",
    "birthplace": "",
    "education": "",
    "party_join": "",
    "work_start": "",
    "current_post": "县政协副主席",
    "current_org": "通河县政协",
    "source": "https://www.hrbtonghe.gov.cn/hebthxx/c109572/201911/c01_377187.shtml",
}
person_id_map[p["name"]] = p["id"]
persons.append(p)

# 24. 王占英 — 县政协副主席
p = {
    "id": next_id(),
    "name": "王占英",
    "gender": "男",
    "ethnicity": "汉族",
    "birth": "",
    "birthplace": "",
    "education": "",
    "party_join": "",
    "work_start": "",
    "current_post": "县政协副主席",
    "current_org": "通河县政协",
    "source": "https://www.hrbtonghe.gov.cn/hebthxx/c109572/201911/c01_377186.shtml",
}
person_id_map[p["name"]] = p["id"]
persons.append(p)

# ── Organizations ──
organizations = [
    {"id": 1, "name": "中共通河县委员会", "type": "党委", "level": "县级", "parent": "中共哈尔滨市委", "location": "通河县"},
    {"id": 2, "name": "通河县人民政府", "type": "政府", "level": "县级", "parent": "哈尔滨市人民政府", "location": "通河县"},
    {"id": 3, "name": "中共通河县委组织部", "type": "党委", "level": "县级", "parent": "中共通河县委员会", "location": "通河县"},
    {"id": 4, "name": "中共通河县委宣传部", "type": "党委", "level": "县级", "parent": "中共通河县委员会", "location": "通河县"},
    {"id": 5, "name": "中共通河县委政法委员会", "type": "党委", "level": "县级", "parent": "中共通河县委员会", "location": "通河县"},
    {"id": 6, "name": "中共通河县委统战部", "type": "党委", "level": "县级", "parent": "中共通河县委员会", "location": "通河县"},
    {"id": 7, "name": "中共通河县纪律检查委员会", "type": "党委", "level": "县级", "parent": "中共通河县委员会", "location": "通河县"},
    {"id": 8, "name": "通河县人大常委会", "type": "人大", "level": "县级", "parent": "哈尔滨市人大常委会", "location": "通河县"},
    {"id": 9, "name": "通河县政协", "type": "政协", "level": "县级", "parent": "哈尔滨市政协", "location": "通河县"},
    {"id": 10, "name": "通河县经济开发区", "type": "开发区", "level": "县级", "parent": "通河县人民政府", "location": "通河县"},
]

# ── Positions ──
positions = [
    {"person_id": person_id_map["高俊杰"], "org_id": 1, "title": "县委书记", "start": "~2024", "end": "present", "rank": "正处级", "note": "曾任通河县县长，后升任县委书记"},
    {"person_id": person_id_map["孟祥伟"], "org_id": 2, "title": "县长", "start": "~2024", "end": "present", "rank": "正处级", "note": "兼任通河县经济开发区党工委书记、管委会主任"},
    {"person_id": person_id_map["孟祥伟"], "org_id": 1, "title": "县委副书记", "start": "~2024", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": person_id_map["赵春明"], "org_id": 1, "title": "县委副书记", "start": "", "end": "present", "rank": "副处级", "note": "负责县委日常工作"},
    {"person_id": person_id_map["潘旭明"], "org_id": 1, "title": "县委副书记（挂职）", "start": "~2025-04", "end": "present", "rank": "副处级", "note": "挂职，负责农业农村工作"},
    {"person_id": person_id_map["荆勇"], "org_id": 3, "title": "组织部部长", "start": "", "end": "present", "rank": "副处级", "note": "县委常委"},
    {"person_id": person_id_map["李颖"], "org_id": 2, "title": "常务副县长", "start": "", "end": "present", "rank": "副处级", "note": "县委常委"},
    {"person_id": person_id_map["赵鹏辉"], "org_id": 4, "title": "宣传部部长", "start": "", "end": "present", "rank": "副处级", "note": "县委常委"},
    {"person_id": person_id_map["徐鸣超"], "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "县委常委，负责招商引资"},
    {"person_id": person_id_map["陈建名"], "org_id": 5, "title": "政法委书记", "start": "", "end": "present", "rank": "正处级", "note": "县委常委（正处级）"},
    {"person_id": person_id_map["李僖讴"], "org_id": 7, "title": "县纪委书记、县监委主任", "start": "", "end": "present", "rank": "副处级", "note": "县委常委"},
    {"person_id": person_id_map["张静"], "org_id": 6, "title": "统战部部长", "start": "", "end": "present", "rank": "副处级", "note": "县委常委"},
    {"person_id": person_id_map["王思库"], "org_id": 8, "title": "县人大常委会主任", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": person_id_map["管耀辉"], "org_id": 8, "title": "县人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": person_id_map["张国志"], "org_id": 8, "title": "县人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": person_id_map["宋瑞宏"], "org_id": 8, "title": "县人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": person_id_map["宋喜波"], "org_id": 8, "title": "县人大常委会副主任", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": person_id_map["赵宏宝"], "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": person_id_map["商震"], "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": person_id_map["贾文鹏"], "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": "分管文旅、教育等工作"},
    {"person_id": person_id_map["葛书范"], "org_id": 2, "title": "副县长", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": person_id_map["马哲"], "org_id": 9, "title": "县政协主席", "start": "", "end": "present", "rank": "正处级", "note": ""},
    {"person_id": person_id_map["王厚平"], "org_id": 9, "title": "县政协副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": person_id_map["曲春林"], "org_id": 9, "title": "县政协副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
    {"person_id": person_id_map["王占英"], "org_id": 9, "title": "县政协副主席", "start": "", "end": "present", "rank": "副处级", "note": ""},
    # Historical: 高俊杰曾任县长
    {"person_id": person_id_map["高俊杰"], "org_id": 2, "title": "县长（前任）", "start": "~2021.12", "end": "~2024", "rank": "正处级", "note": "高俊杰在升任县委书记前曾任通河县县长"},
]

# ── Relationships ──
relationships = [
    {
        "person_a": person_id_map["高俊杰"],
        "person_b": person_id_map["孟祥伟"],
        "type": "predecessor_successor",
        "context": "高俊杰由县长升任县委书记，孟祥伟接任县长，党政一把手搭班配合",
        "overlap_org": "通河县人民政府/中共通河县委员会",
        "overlap_period": "2024至今",
    },
    {
        "person_a": person_id_map["高俊杰"],
        "person_b": person_id_map["赵春明"],
        "type": "superior_subordinate",
        "context": "赵春明作为县委副书记协助高俊杰抓县委日常工作",
        "overlap_org": "中共通河县委员会",
        "overlap_period": "",
    },
    {
        "person_a": person_id_map["孟祥伟"],
        "person_b": person_id_map["李颖"],
        "type": "superior_subordinate",
        "context": "李颖作为常务副县长协助孟祥伟主持县政府日常工作",
        "overlap_org": "通河县人民政府",
        "overlap_period": "",
    },
    {
        "person_a": person_id_map["徐鸣超"],
        "person_b": person_id_map["张静"],
        "type": "same_native_place",
        "context": "徐鸣超为黑龙江方正县人，张静为黑龙江省方正县人，同为方正籍",
        "overlap_org": "",
        "overlap_period": "",
    },
    {
        "person_a": person_id_map["高俊杰"],
        "person_b": person_id_map["李颖"],
        "type": "overlap",
        "context": "高俊杰任县长期间，李颖任常务副县长",
        "overlap_org": "通河县人民政府",
        "overlap_period": "",
    },
    {
        "person_a": person_id_map["陈建名"],
        "person_b": person_id_map["赵宏宝"],
        "type": "superior_subordinate",
        "context": "陈建名作为政法委书记联系县公安局，赵宏宝为副县长分管公安",
        "overlap_org": "通河县",
        "overlap_period": "",
    },
    {
        "person_a": person_id_map["孟祥伟"],
        "person_b": person_id_map["潘旭明"],
        "type": "overlap",
        "context": "孟祥伟（县长）与潘旭明（挂职副书记）在县委班子共事",
        "overlap_org": "中共通河县委员会",
        "overlap_period": "2025-04至今",
    },
]

# =========================================================================
# BUILD
# =========================================================================

if __name__ == "__main__":
    run_build(
        slug="通河县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    print(f"\n✅ Build complete!")
    print(f"   DB:   {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")
    print(f"   Persons: {len(persons)}")
    print(f"   Orgs: {len(organizations)}")
    print(f"   Positions: {len(positions)}")
    print(f"   Relationships: {len(relationships)}")
