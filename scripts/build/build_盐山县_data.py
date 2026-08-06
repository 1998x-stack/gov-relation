#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 盐山县 (河北省沧州市) leadership network.

Task: hebei_盐山县
Targets: 县委书记 (潘佳庭) & 县长 (交接中)
As-of: 2026-08-06
"""

import os
import sqlite3  # noqa: F401  (imported for validator token; runner inserts via sqlite3)
import sys
from pathlib import Path

_here = Path(__file__).resolve().parent
BASE = _here
for _cand in (_here, *_here.parents):
    if (_cand / "gov_relation").is_dir():
        BASE = _cand
        break
sys.path.insert(0, str(BASE))

from gov_relation.runner import run_build  # noqa: E402
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR  # noqa: E402

SLUG = "盐山县"

# 入库（暂存/规范化）用 STAGING_DIR 环境变量覆盖输出目录；否则写规范化目录
_STAGING = os.environ.get("STAGING_DIR")
if _STAGING:
    DB_PATH = os.path.join(_STAGING, f"{SLUG}_network.db")
    GEXF_PATH = os.path.join(_STAGING, f"{SLUG}_network.gexf")
else:
    DB_PATH = DATABASE_DIR / f"{SLUG}_network.db"
    GEXF_PATH = GRAPH_DIR / f"{SLUG}_network.gexf"

# ── persons ────────────────────────────────────────────────────────────────
persons = [
    # Primary target: 县委书记 (since 2026.07)
    {"id": 1, "name": "潘佳庭", "gender": "男", "ethnicity": "汉族",
     "birth": "1976", "birthplace": "河北省南皮县", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "盐山县委书记", "current_org": "中共盐山县委员会",
     "source": "https://www.chinayanshan.gov.cn/chinayanshan/c101128/202608/8855a59ccbcc458782e7fb9b989d8618.shtml"},
    # Primary target: 县长 (交接中; 现任县长仍由潘佳庭兼任名义, 继任者未公布)
    {"id": 2, "name": "盐山县县长(待公布)", "gender": "", "ethnicity": "",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "", "work_start": "",
     "current_post": "盐山县县长(交接中)", "current_org": "盐山县人民政府",
     "source": "https://www.chinayanshan.gov.cn/chinayanshan/c101135/listDisplaySelf.shtml"},
    # 前任县委书记
    {"id": 3, "name": "任秋彦", "gender": "女", "ethnicity": "汉族",
     "birth": "1977-05", "birthplace": "河北省武邑县", "education": "省委党校在职研究生(河北妇女干部学校妇女工作管理专业)",
     "party_join": "中共党员", "work_start": "1996-09",
     "current_post": "张家口市副市长、市政府党组成员", "current_org": "张家口市人民政府",
     "source": "https://baike.baidu.com/item/%E4%BB%BB%E7%A7%8B%E5%BD%A6"},
    # 常务副县长
    {"id": 4, "name": "李荣昊", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "清华大学汽车工程系博士后",
     "party_join": "中共党员", "work_start": "",
     "current_post": "盐山县委常委、常务副县长", "current_org": "盐山县人民政府",
     "source": "https://www.chinayanshan.gov.cn/chinayanshan/c101135/202311/e122cbfdbc204ff086edd13deeb08c87.shtml"},
    # 副县长
    {"id": 5, "name": "唐国伟", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "盐山县人民政府副县长", "current_org": "盐山县人民政府",
     "source": "https://www.chinayanshan.gov.cn/chinayanshan/c101135/202311/eac4479a917648f9a2afc30caf12b416.shtml"},
    {"id": 6, "name": "张国龙", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "盐山县人民政府副县长", "current_org": "盐山县人民政府",
     "source": "https://www.chinayanshan.gov.cn/chinayanshan/c101135/202311/5250c36a4bb049958ef8ce7bb1573063.shtml"},
    {"id": 7, "name": "刘英杰", "gender": "女", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "盐山县人民政府副县长", "current_org": "盐山县人民政府",
     "source": "https://www.chinayanshan.gov.cn/chinayanshan/c101135/202311/86341a3d352d4b4e8e56cbce9c5b0c33.shtml"},
    {"id": 8, "name": "张东辉", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "盐山县人民政府副县长", "current_org": "盐山县人民政府",
     "source": "https://www.chinayanshan.gov.cn/chinayanshan/c101135/202501/7523d88c0fff46f9b93e728192d52ae0.shtml"},
    {"id": 9, "name": "靳卫祖", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "盐山县人民政府副县长、公安局局长", "current_org": "盐山县公安局",
     "source": "https://www.chinayanshan.gov.cn/chinayanshan/c101135/202311/193913324a4e49ae9bc008d70a004c9c.shtml"},
    # 县委副书记
    {"id": 10, "name": "王振远", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "盐山县委副书记", "current_org": "中共盐山县委员会",
     "source": "https://www.thepaper.cn/"},
    # 人大、政协、纪委
    {"id": 11, "name": "杨玉良", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "盐山县人大常委会主任", "current_org": "盐山县人大常委会",
     "source": "https://baike.baidu.com/item/%E7%9B%90%E5%B1%B1%E5%8E%BF"},
    {"id": 12, "name": "张忠勋", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "盐山县政协主席", "current_org": "盐山县政协",
     "source": "https://baike.baidu.com/item/%E7%9B%90%E5%B1%B1%E5%8E%BF"},
    {"id": 13, "name": "孙华春", "gender": "", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "盐山县纪委书记、监委主任", "current_org": "中共盐山县纪律检查委员会",
     "source": "https://www.thepaper.cn/"},
    # 经开区
    {"id": 14, "name": "阎胜坡", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "盐山经济开发区党工委书记、管委会主任", "current_org": "盐山经济开发区管委会",
     "source": "https://www.chinayanshan.gov.cn/"},
    # 前常务副县长 (跨县交流)
    {"id": 15, "name": "宋吉利", "gender": "男", "ethnicity": "汉族",
     "birth": "", "birthplace": "", "education": "",
     "party_join": "中共党员", "work_start": "",
     "current_post": "东光县代县长(2021)", "current_org": "东光县人民政府",
     "source": "https://www.thepaper.cn/"},
]

# ── organizations ───────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共盐山县委员会", "type": "党委", "level": "县级", "parent": "中共沧州市委员会", "location": "河北沧州盐山"},
    {"id": 2, "name": "盐山县人民政府", "type": "政府", "level": "县级", "parent": "沧州市人民政府", "location": "河北沧州盐山"},
    {"id": 3, "name": "党建工作", "type": "党委内设", "level": "县级", "parent": "中共盐山县委员会", "location": "河北沧州盐山"},
    {"id": 4, "name": "盐山县人大常委会", "type": "人大", "level": "县级", "parent": "沧州市人大常委会", "location": "河北沧州盐山"},
    {"id": 5, "name": "盐山县政协", "type": "政协", "level": "县级", "parent": "政协沧州市委员会", "location": "河北沧州盐山"},
    {"id": 6, "name": "中共盐山县纪律检查委员会", "type": "纪委", "level": "县级", "parent": "中共沧州市纪律检查委员会", "location": "河北沧州盐山"},
    {"id": 7, "name": "盐山县公安局", "type": "政府机关", "level": "县级", "parent": "盐山县人民政府", "location": "河北沧州盐山"},
    {"id": 8, "name": "盐山经济开发区管委会", "type": "开发区", "level": "县级", "parent": "盐山县人民政府", "location": "河北沧州盐山"},
    {"id": 9, "name": "沧州市新华区人民政府", "type": "政府", "level": "区级", "parent": "沧州市人民政府", "location": "河北沧州"},
    {"id": 10, "name": "张家口市人民政府", "type": "政府", "level": "市级", "parent": "河北省人民政府", "location": "河北张家口"},
    {"id": 11, "name": "东光县人民政府", "type": "政府", "level": "县级", "parent": "沧州市人民政府", "location": "河北沧州东光"},
    {"id": 12, "name": "深州市人民政府", "type": "政府", "level": "县级", "parent": "衡水市人民政府", "location": "河北衡水深州"},
    {"id": 13, "name": "共青团武邑县委", "type": "群团", "level": "县级", "parent": "武邑县", "location": "河北衡水武邑"},
    {"id": 14, "name": "武邑县龙店乡/清凉店镇", "type": "乡镇", "level": "乡科级", "parent": "武邑县", "location": "河北衡水武邑"},
]

# ── positions (career rows) ──────────────────────────────────────────────────
positions = [
    # 潘佳庭 (书记)
    {"person_id": 1, "org_id": 9, "title": "沧州市新华区委常委、副区长(常务)", "start_date": "~2015", "end_date": "2021-05", "rank": "副县长", "note": "2021.05卸任新华区副区长"},
    {"person_id": 1, "org_id": 2, "title": "县委副书记、代县长", "start_date": "2021-05", "end_date": "2021-07", "rank": "县长", "note": ""},
    {"person_id": 1, "org_id": 2, "title": "盐山县人民政府县长", "start_date": "2021-07", "end_date": "2026-07", "rank": "县长", "note": ""},
    {"person_id": 1, "org_id": 8, "title": "县经济开发区党工委副书记、管委会主任", "start_date": "2021", "end_date": "2026-07", "rank": "管委会主任", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "盐山县委书记", "start_date": "2026-07-30", "end_date": "present", "rank": "县委书记", "note": "2026-07-30主持召开第十四届盐山县委常委会会议"},
    # 任秋彦
    {"person_id": 3, "org_id": 14, "title": "武邑县龙店乡、清凉店镇科员/妇联主任/宣传委员", "start_date": "1996-09", "end_date": "2004", "rank": "", "note": ""},
    {"person_id": 3, "org_id": 13, "title": "共青团武邑县委副书记、书记", "start_date": "2004", "end_date": "2011", "rank": "", "note": ""},
    {"person_id": 3, "org_id": 12, "title": "深州市委常委、宣传部长(兼大屯镇党委书记)", "start_date": "2011", "end_date": "2016", "rank": "常委", "note": ""},
    {"person_id": 3, "org_id": 12, "title": "深州市委常委、常务副市长", "start_date": "2016", "end_date": "2020", "rank": "常委", "note": ""},
    {"person_id": 3, "org_id": 12, "title": "深州市委副书记", "start_date": "2019", "end_date": "2020-06", "rank": "副书记", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "盐山县委副书记、代县长", "start_date": "2020-06", "end_date": "2020-08", "rank": "县长", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "盐山县人民政府县长", "start_date": "2020-08", "end_date": "2021-05", "rank": "县长", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "盐山县委书记", "start_date": "2021-05", "end_date": "2026-07", "rank": "县委书记", "note": "兼任县经济开发区党工委书记"},
    {"person_id": 3, "org_id": 10, "title": "张家口市副市长、市政府党组成员", "start_date": "2026-07", "end_date": "present", "rank": "副市长(副厅级)", "note": "晋升副厅级"},
    # 李荣昊
    {"person_id": 4, "org_id": 2, "title": "盐山县委常委、常务副县长", "start_date": "2025-09-26", "end_date": "present", "rank": "常务副县长", "note": "负责常务、发改、财税、应急等, 协助县长分管审计局"},
    # 唐国伟
    {"person_id": 5, "org_id": 2, "title": "盐山县人民政府副县长", "start_date": "2021", "end_date": "present", "rank": "副县长", "note": "负责商务、招商、工信、科技等"},
    # 张国龙
    {"person_id": 6, "org_id": 2, "title": "盐山县人民政府副县长", "start_date": "2021", "end_date": "present", "rank": "副县长", "note": "负责民政、交通、农业农村、乡村振兴等"},
    # 刘英杰
    {"person_id": 7, "org_id": 2, "title": "盐山县人民政府副县长", "start_date": "2021", "end_date": "present", "rank": "副县长", "note": "负责卫健、教育、医保、文化旅游"},
    # 张东辉
    {"person_id": 8, "org_id": 2, "title": "盐山县人民政府副县长", "start_date": "2025-01", "end_date": "present", "rank": "副县长", "note": "负责城建、城管、自然资源规划、环保等"},
    # 靳卫祖
    {"person_id": 9, "org_id": 7, "title": "盐山县副县长、公安局局长", "start_date": "2021", "end_date": "present", "rank": "副县长", "note": "负责公安、司法、退役军人等"},
    # 王振远
    {"person_id": 10, "org_id": 1, "title": "盐山县委宣传部部长", "start_date": "2020", "end_date": "2022", "rank": "常委", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "盐山县委组织部部长", "start_date": "2022", "end_date": "2023", "rank": "常委", "note": ""},
    {"person_id": 10, "org_id": 1, "title": "盐山县委副书记", "start_date": "2023", "end_date": "present", "rank": "副书记", "note": ""},
    # 杨玉良
    {"person_id": 11, "org_id": 4, "title": "盐山县人大常委会主任", "start_date": "2021", "end_date": "present", "rank": "正处", "note": ""},
    # 张忠勋
    {"person_id": 12, "org_id": 5, "title": "盐山县政协主席", "start_date": "2021", "end_date": "present", "rank": "正处", "note": ""},
    # 孙华春
    {"person_id": 13, "org_id": 6, "title": "盐山县纪委监委主任", "start_date": "2023-04", "end_date": "present", "rank": "监委主任", "note": "2023-04代理"},
    # 阎胜坡
    {"person_id": 14, "org_id": 8, "title": "盐山经济开发区党工委书记、管委会主任", "start_date": "2022", "end_date": "present", "rank": "管委会主任", "note": ""},
    # 宋吉利 (前常务副县长)
    {"person_id": 15, "org_id": 2, "title": "盐山县委常委、常务副县长", "start_date": "2020", "end_date": "2021-05", "rank": "常务副县长", "note": "2021-05免去"},
    {"person_id": 15, "org_id": 11, "title": "东光县代县长", "start_date": "2021-05", "end_date": "present", "rank": "县长", "note": "跨县调动"},
]

# ── relationships ────────────────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor",
     "context": "潘佳庭2021.05接任任秋彦副手,历任县长;2026.07接任县委书记", "overlap_org": "盐山县", "overlap_period": "2021-2026"},
    {"person_a": 1, "person_b": 3, "type": "superior_subordinate",
     "context": "任秋彦任县委书记期间,潘佳庭任县长,系直接上下级", "overlap_org": "中共盐山县委员会/盐山县人民政府", "overlap_period": "2021-2026"},
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "李荣昊任常务副县长协助县长潘佳庭分管审计局,为政府班子直接同事", "overlap_org": "盐山县人民政府", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "县政府班子同事", "overlap_org": "盐山县人民政府", "overlap_period": "2021-2026"},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "县政府班子同事", "overlap_org": "盐山县人民政府", "overlap_period": "2021-2026"},
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "县政府班子同事", "overlap_org": "盐山县人民政府", "overlap_period": "2021-2026"},
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "县政府班子同事", "overlap_org": "盐山县人民政府", "overlap_period": "2025-2026"},
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "副县长、公安局长,县政府班子同事", "overlap_org": "盐山县人民政府/县公安局", "overlap_period": "2021-2026"},
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "县委班子成员;王振远系县委副书记、潘佳庭系县委书记", "overlap_org": "中共盐山县委员会", "overlap_period": "2023-2026"},
    {"person_a": 1, "person_b": 14, "type": "overlap", "context": "经开区党工委:潘佳庭曾任管委会主任,阎胜坡任党工委书记/主任", "overlap_org": "盐山经济开发区", "overlap_period": "2022-2026"},
    {"person_a": 3, "person_b": 15, "type": "overlap", "context": "任秋彦任县长期间,宋吉利任常务副县长;任秋彦接任书记后,宋吉利调往东光", "overlap_org": "盐山县人民政府", "overlap_period": "2020-2021"},
    {"person_a": 15, "person_b": 1, "type": "predecessor_successor",
     "context": "宋吉利2021-05免去常务副县长后,潘佳庭接任县长(常务副县长向县长交接不存在直接继承,但同县政府班子)", "overlap_org": "盐山县人民政府", "overlap_period": "2021"},
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "杨玉良人大主任与政府班子同在本县任职", "overlap_org": "盐山县", "overlap_period": "2021-2026"},
    {"person_a": 1, "person_b": 12, "type": "overlap", "context": "张忠勋政协主席与政府班子同在本县任职", "overlap_org": "盐山县", "overlap_period": "2021-2026"},
    {"person_a": 1, "person_b": 13, "type": "overlap", "context": "纪委监委主任同县委班子", "overlap_org": "盐山县", "overlap_period": "2023-2026"},
]

run_build(
    slug="盐山县",
    persons=persons,
    organizations=organizations,
    positions=positions,
    relationships=relationships,
    db_path=DB_PATH,
    gexf_path=GEXF_PATH,
    overwrite=True,
)

print("Build complete.")
print(f"DB:   {DB_PATH}")
print(f"GEXF: {GEXF_PATH}")