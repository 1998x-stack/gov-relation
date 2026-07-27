#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 勃利县 (Boli County), 七台河市, 黑龙江省.

Investigation date: 2026-07-24
Task ID: heilongjiang_勃利县
Level: 县
Targets: 县委书记 & 县长
Research sources:
  - Boli County Government Website (www.hljboli.gov.cn) — leadership pages, bio pages
  - Baidu Baike — 张生河 full biography
  - Government work reports (2023-2026)
  - County news articles (2026)
  - Wikipedia 勃利县 / 七台河市
"""

import os
import sqlite3

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "勃利县"
AS_OF = "2026-07-24"

STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, f"{SLUG}_network.gexf")

# ══════════════════════════════════════════════════════════════════════════════
# Persons
# ══════════════════════════════════════════════════════════════════════════════
# Person IDs: 1-19 for individuals

persons = [
    # ── Core Leadership ──────────────────────────────────────────────────────
    {
        "id": 1,
        "name": "张生河",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年2月",
        "birthplace": "黑龙江七台河",
        "education": "省委党校研究生",
        "party_join": "1995年12月",
        "work_start": "1992年9月",
        "current_post": "勃利县委书记、县人武部党委第一书记",
        "current_org": "中共勃利县委员会",
        "source": "https://baike.baidu.com/item/%E5%BC%A0%E7%94%9F%E6%B2%B3; https://www.hljboli.gov.cn/hljboli/c100446/202312/51d1fd1b228a4e38902275ac2ae6f747.shtml",
    },
    {
        "id": 2,
        "name": "王华锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年2月",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "勃利县委副书记、县长",
        "current_org": "勃利县人民政府",
        "source": "https://www.hljboli.gov.cn/hljboli/c100446/202601/0405a9996b8f4bc38946011e0466f730.shtml",
    },
    # ── 县委常委 ──────────────────────────────────────────────────────────────
    {
        "id": 3,
        "name": "伊静",
        "gender": "女",
        "ethnicity": "满族",
        "birth": "1983年4月",
        "birthplace": "",
        "education": "在职研究生，农业推广硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "勃利县委副书记（专职）",
        "current_org": "中共勃利县委员会",
        "source": "https://www.hljboli.gov.cn/hljboli/c100446/202411/d94b9810102b4103a2e37587e9ded8a6.shtml",
    },
    {
        "id": 4,
        "name": "张壮初",
        "gender": "男",
        "ethnicity": "蒙古族",
        "birth": "1974年2月",
        "birthplace": "",
        "education": "在职工程硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "中共勃利县委员会 / 勃利县人民政府",
        "source": "https://www.hljboli.gov.cn/hljboli/c100446/202411/1319cfca6c774491bebdd8d3167cd3b4.shtml",
    },
    {
        "id": 5,
        "name": "赵波涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年3月",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、县人武部上校政委",
        "current_org": "勃利县人民武装部",
        "source": "https://www.hljboli.gov.cn/hljboli/c100446/202205/6595e8bfe64a47008361d1fb95fb19b1.shtml",
    },
    {
        "id": 6,
        "name": "栗文博",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1978年4月",
        "birthplace": "",
        "education": "大学，法学学士",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共勃利县委员会",
        "source": "https://www.hljboli.gov.cn/hljboli/c100446/202604/e4ba56a50fbc4990b71f3eeddd3d9c17.shtml",
    },
    {
        "id": 7,
        "name": "赵明冬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年4月",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、组织部部长、三级调研员",
        "current_org": "中共勃利县委员会",
        "source": "https://www.hljboli.gov.cn/hljboli/c100446/202101/85b7edf4656a4e4796389953a67a0c5f.shtml",
    },
    {
        "id": 8,
        "name": "宁宇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年8月",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、纪委书记、监委主任",
        "current_org": "中共勃利县纪律检查委员会 / 勃利县监察委员会",
        "source": "https://www.hljboli.gov.cn/hljboli/c100446/202504/85bbe3968bf9434e95c456ad032c6619.shtml",
    },
    {
        "id": 9,
        "name": "刘思韬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年2月",
        "birthplace": "",
        "education": "大学，工学学士",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、统战部部长",
        "current_org": "中共勃利县委员会",
        "source": "https://www.hljboli.gov.cn/hljboli/c100446/202604/752a7c78605147859138c0d0fa903e9a.shtml",
    },
    {
        "id": 10,
        "name": "张春鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年4月",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "中共勃利县委员会 / 勃利县人民政府",
        "source": "https://www.hljboli.gov.cn/hljboli/c100446/202601/c9aeba537a6c4db5b96300d684553949.shtml",
    },
    # ── 县政府副县长（非常委） ─────────────────────────────────────────────
    {
        "id": 11,
        "name": "李义",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年12月",
        "birthplace": "",
        "education": "在职研究生，农业推广硕士",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "勃利县人民政府",
        "source": "https://www.hljboli.gov.cn/hljboli/c100448/202501/7608771364774d8f8b17b71bdfc71fc1.shtml",
    },
    {
        "id": 12,
        "name": "李春龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年7月",
        "birthplace": "",
        "education": "在职大学",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长、公安局局长（三级高级警长）",
        "current_org": "勃利县公安局 / 勃利县人民政府",
        "source": "https://www.hljboli.gov.cn/hljboli/c100448/202312/5529b4c317b641c189d940c320edd2b7.shtml",
    },
    {
        "id": 13,
        "name": "马宏",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1977年6月",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "勃利县人民政府",
        "source": "https://www.hljboli.gov.cn/hljboli/c100448/202001/aaf75a41d22c4159a22eb626782739ad.shtml",
    },
    {
        "id": 14,
        "name": "韩绍臣",
        "gender": "男",
        "ethnicity": "满族",
        "birth": "1988年5月",
        "birthplace": "",
        "education": "省委党校研究生",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "勃利县人民政府",
        "source": "https://www.hljboli.gov.cn/hljboli/c100448/202606/48f8dadea43a4733af8aab784dc2d6fe.shtml",
    },
    {
        "id": 15,
        "name": "陈雷",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年2月",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "勃利县人民政府",
        "source": "https://www.hljboli.gov.cn/hljboli/c100448/202605/809bcbaa264d451aad09218b27f81370.shtml",
    },
    # ── 县人大 ────────────────────────────────────────────────────────────────
    {
        "id": 16,
        "name": "刘元波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967年9月",
        "birthplace": "",
        "education": "中央党校大学",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "勃利县人民代表大会常务委员会",
        "source": "https://www.hljboli.gov.cn/hljboli/c100447/201911/3e3a1974037049ec8e3f432ff3c6580d.shtml",
    },
    # ── 县政协 ────────────────────────────────────────────────────────────────
    {
        "id": 17,
        "name": "朱洪刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年5月",
        "birthplace": "",
        "education": "大学",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "政协勃利县委员会",
        "source": "https://www.hljboli.gov.cn/hljboli/c100449/202601/42ee1f47c1f046c0ac874de1485a1154.shtml",
    },
    # ── 七台河市领导（与勃利县密切相关） ──────────────────────────────────
    {
        "id": 18,
        "name": "陈延良",
        "gender": "男",
        "ethnicity": "柯尔克孜族",
        "birth": "1972年",
        "birthplace": "黑龙江省富裕县",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "七台河市委书记",
        "current_org": "中共七台河市委员会",
        "source": "https://zh.wikipedia.org/wiki/七台河市",
    },
    {
        "id": 19,
        "name": "张涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年",
        "birthplace": "山东莱州",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "七台河市长",
        "current_org": "七台河市人民政府",
        "source": "https://zh.wikipedia.org/wiki/七台河市",
    },
]

# ══════════════════════════════════════════════════════════════════════════════
# Organizations
# ══════════════════════════════════════════════════════════════════════════════

organizations = [
    {"id": 1, "name": "中共勃利县委员会", "type": "党委", "level": "县处级", "parent": "中共七台河市委员会", "location": "勃利县"},
    {"id": 2, "name": "勃利县人民政府", "type": "政府", "level": "县处级", "parent": "七台河市人民政府", "location": "勃利县"},
    {"id": 3, "name": "勃利县人民武装部", "type": "事业单位", "level": "县处级", "parent": "七台河军分区", "location": "勃利县"},
    {"id": 4, "name": "中共勃利县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共七台河市纪律检查委员会", "location": "勃利县"},
    {"id": 5, "name": "勃利县监察委员会", "type": "事业单位", "level": "县处级", "parent": "七台河市监察委员会", "location": "勃利县"},
    {"id": 6, "name": "勃利县公安局", "type": "政府", "level": "乡科级", "parent": "勃利县人民政府", "location": "勃利县"},
    {"id": 7, "name": "勃利县人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "", "location": "勃利县"},
    {"id": 8, "name": "政协勃利县委员会", "type": "政协", "level": "县处级", "parent": "", "location": "勃利县"},
    {"id": 9, "name": "中共七台河市委员会", "type": "党委", "level": "地厅级", "parent": "中共黑龙江省委员会", "location": "七台河市"},
    {"id": 10, "name": "七台河市人民政府", "type": "政府", "level": "地厅级", "parent": "黑龙江省人民政府", "location": "七台河市"},
    # Historical orgs for 张生河's career
    {"id": 11, "name": "七台河市桃山区桃西乡", "type": "乡镇/街道", "level": "乡科级", "parent": "桃山区人民政府", "location": "七台河市桃山区"},
    {"id": 12, "name": "七台河市利成海公司", "type": "其他", "level": "", "parent": "", "location": "七台河市"},
    {"id": 13, "name": "七台河市桃山区万宝河镇", "type": "乡镇/街道", "level": "乡科级", "parent": "桃山区人民政府", "location": "七台河市桃山区"},
    {"id": 14, "name": "七台河市桃山区兴岗街道", "type": "乡镇/街道", "level": "乡科级", "parent": "桃山区人民政府", "location": "七台河市桃山区"},
    {"id": 15, "name": "七台河市桃山区桃西街道", "type": "乡镇/街道", "level": "乡科级", "parent": "桃山区人民政府", "location": "七台河市桃山区"},
    {"id": 16, "name": "七台河市桃山供水处", "type": "事业单位", "level": "县处级", "parent": "七台河市人民政府", "location": "七台河市"},
    {"id": 17, "name": "七台河市汽车公司", "type": "其他", "level": "县处级", "parent": "七台河市人民政府", "location": "七台河市"},
    {"id": 18, "name": "七台河市林业和草原局", "type": "政府", "level": "县处级", "parent": "七台河市人民政府", "location": "七台河市"},
    {"id": 19, "name": "七台河市人力资源和社会保障局", "type": "政府", "level": "县处级", "parent": "七台河市人民政府", "location": "七台河市"},
    {"id": 20, "name": "中共七台河市委组织部", "type": "党委", "level": "县处级", "parent": "中共七台河市委员会", "location": "七台河市"},
]

# ══════════════════════════════════════════════════════════════════════════════
# Positions (career timeline entries)
# ══════════════════════════════════════════════════════════════════════════════

positions = [
    # ── 张生河 (id=1) ─────────────────────────────────────────────────────────
    {"person_id": 1, "org_id": 1, "title": "勃利县委书记、县人武部党委第一书记", "start_date": "~2025-12", "end_date": "至今", "rank": "正处级", "note": "之前任勃利县长，~2025年12月前已任县委书记（县人武部党委第一书记任职大会2025-12-11）"},
    {"person_id": 1, "org_id": 2, "title": "勃利县委副书记、县长", "start_date": "2022-02", "end_date": "2026-01", "rank": "正处级", "note": "2026-01-16免去县长职务"},
    {"person_id": 1, "org_id": 19, "title": "局长、党组书记、市委组织部副部长（兼）", "start_date": "2020-03", "end_date": "2022-02", "rank": "正处级", "note": "七台河市人力资源和社会保障局"},
    {"person_id": 1, "org_id": 18, "title": "局长、党组书记", "start_date": "2018-12", "end_date": "2020-03", "rank": "正处级", "note": "七台河市林业和草原局"},
    {"person_id": 1, "org_id": 17, "title": "经理、党委书记", "start_date": "2016-11", "end_date": "2018-12", "rank": "副处级→正处级", "note": "七台河市汽车公司"},
    {"person_id": 1, "org_id": 17, "title": "经理（副处级）", "start_date": "2011-08", "end_date": "2016-11", "rank": "副处级", "note": "七台河市汽车公司"},
    {"person_id": 1, "org_id": 16, "title": "经理、建设局党委委员", "start_date": "2005-10", "end_date": "2011-08", "rank": "正科级→副处级", "note": "七台河市桃山供水处；期间2005-2008省委党校经济管理研究生"},
    {"person_id": 1, "org_id": 13, "title": "党委书记、人大主席团主席", "start_date": "2004-11", "end_date": "2005-10", "rank": "正科级", "note": "七台河市桃山区万宝河镇"},
    {"person_id": 1, "org_id": 13, "title": "党委书记", "start_date": "2003-10", "end_date": "2004-11", "rank": "正科级", "note": "七台河市桃山区万宝河镇；期间2001-2003法律专业本科"},
    {"person_id": 1, "org_id": 15, "title": "党委书记、办事处主任", "start_date": "2002-11", "end_date": "2003-10", "rank": "正科级", "note": "七台河市桃山区桃西街道"},
    {"person_id": 1, "org_id": 14, "title": "党委书记、办事处主任（正科级）", "start_date": "2002-01", "end_date": "2002-11", "rank": "正科级", "note": "七台河市桃山区兴岗街道"},
    {"person_id": 1, "org_id": 13, "title": "党委委员、副镇长", "start_date": "2001-06", "end_date": "2002-01", "rank": "副科级", "note": "七台河市桃山区万宝河镇"},
    {"person_id": 1, "org_id": 13, "title": "副镇长（副科级）", "start_date": "1999-11", "end_date": "2001-06", "rank": "副科级", "note": "七台河市桃山区万宝河镇；期间1997-2000省委党校经济管理大专班"},
    {"person_id": 1, "org_id": 13, "title": "企业办主任", "start_date": "1996-11", "end_date": "1999-11", "rank": "", "note": "七台河市桃山区万宝河镇"},
    {"person_id": 1, "org_id": 12, "title": "销售经理", "start_date": "1994-11", "end_date": "1996-11", "rank": "", "note": "七台河市利成海公司"},
    {"person_id": 1, "org_id": 11, "title": "畜牧站站长", "start_date": "1992-09", "end_date": "1994-11", "rank": "", "note": "七台河市桃山区桃西乡"},
    # ── 王华锋 (id=2) — only current position known ───────────────────────────
    {"person_id": 2, "org_id": 2, "title": "勃利县委副书记、县长", "start_date": "~2026-01", "end_date": "至今", "rank": "正处级", "note": "2026年1月起以县长身份作政府工作报告；2026年2月首次在常务会议中出现"},
    # ── 伊静 (id=3) — only current position known ──────────────────────────────
    {"person_id": 3, "org_id": 1, "title": "勃利县委副书记（专职）", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "履历待查——此前职务及任职时间均未知"},
    # ── 张壮初 (id=4) — only current position known ───────────────────────────
    {"person_id": 4, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "在县委常委和政府双重任职，可能为常务副县长"},
    # ── 赵波涛 (id=5) ─────────────────────────────────────────────────────────
    {"person_id": 5, "org_id": 3, "title": "县委常委、县人武部上校政委", "start_date": "", "end_date": "至今", "rank": "正团级", "note": ""},
    # ── 栗文博 (id=6) ─────────────────────────────────────────────────────────
    {"person_id": 6, "org_id": 1, "title": "县委常委、政法委书记", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    # ── 赵明冬 (id=7) ─────────────────────────────────────────────────────────
    {"person_id": 7, "org_id": 1, "title": "县委常委、组织部部长、三级调研员", "start_date": "", "end_date": "至今", "rank": "副处级（三级调研员相当于正处级）", "note": "2021年起即在任，是班子中任职时间最长的成员之一"},
    # ── 宁宇 (id=8) ───────────────────────────────────────────────────────────
    {"person_id": 8, "org_id": 4, "title": "县委常委、纪委书记", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 8, "org_id": 5, "title": "监委主任", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    # ── 刘思韬 (id=9) ─────────────────────────────────────────────────────────
    {"person_id": 9, "org_id": 1, "title": "县委常委、统战部部长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    # ── 张春鹏 (id=10) ────────────────────────────────────────────────────────
    {"person_id": 10, "org_id": 1, "title": "县委常委", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "在县委常委和政府双重任职"},
    # ── 李义 (id=11) ──────────────────────────────────────────────────────────
    {"person_id": 11, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    # ── 李春龙 (id=12) ────────────────────────────────────────────────────────
    {"person_id": 12, "org_id": 6, "title": "副县长、公安局局长（三级高级警长）", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    # ── 马宏 (id=13) ──────────────────────────────────────────────────────────
    {"person_id": 13, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    # ── 韩绍臣 (id=14) ────────────────────────────────────────────────────────
    {"person_id": 14, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    # ── 陈雷 (id=15) ──────────────────────────────────────────────────────────
    {"person_id": 15, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    # ── 刘元波 (id=16) ────────────────────────────────────────────────────────
    {"person_id": 16, "org_id": 7, "title": "县人大常委会主任", "start_date": "", "end_date": "至今", "rank": "正处级", "note": ""},
    # ── 朱洪刚 (id=17) ────────────────────────────────────────────────────────
    {"person_id": 17, "org_id": 8, "title": "县政协主席", "start_date": "", "end_date": "至今", "rank": "正处级", "note": ""},
    # ── 陈延良 (id=18) ────────────────────────────────────────────────────────
    {"person_id": 18, "org_id": 9, "title": "七台河市委书记", "start_date": "~2025-02", "end_date": "至今", "rank": "正厅级", "note": "此前任黑龙江省教育厅副厅长"},
    # ── 张涛 (id=19) ──────────────────────────────────────────────────────────
    {"person_id": 19, "org_id": 10, "title": "七台河市长", "start_date": "~2024-12", "end_date": "至今", "rank": "正厅级", "note": ""},
]

# ══════════════════════════════════════════════════════════════════════════════
# Relationships
# ══════════════════════════════════════════════════════════════════════════════
# Relationship person IDs reference the IDs in the persons list above.

relationships = [
    # ── 党政一把手 ──────────────────────────────────────────────────────────
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "县委书记—县长搭档",
        "overlap_org": "中共勃利县委员会/勃利县人民政府",
        "overlap_period": "2026-至今",
    },
    # ── 张生河 → 县委副书记 ──────────────────────────────────────────────────
    {
        "person_a": 1, "person_b": 3,
        "type": "superior_subordinate",
        "context": "县委书记—专职副书记",
        "overlap_org": "中共勃利县委员会",
        "overlap_period": "2026-至今",
    },
    # ── 县委常委之间共事关系 ──────────────────────────────────────────────────
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "县委常委班子共事", "overlap_org": "中共勃利县委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "县委常委班子共事", "overlap_org": "中共勃利县委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "县委常委班子共事", "overlap_org": "中共勃利县委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "县委常委班子共事", "overlap_org": "中共勃利县委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "县委常委班子共事", "overlap_org": "中共勃利县委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "县委常委班子共事", "overlap_org": "中共勃利县委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "县委常委班子共事", "overlap_org": "中共勃利县委员会", "overlap_period": "至今"},
    # ── 县长与副县长 ──────────────────────────────────────────────────────────
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "县长—副县长", "overlap_org": "勃利县人民政府", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "县长—副县长", "overlap_org": "勃利县人民政府", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 11, "type": "superior_subordinate", "context": "县长—副县长", "overlap_org": "勃利县人民政府", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 12, "type": "superior_subordinate", "context": "县长—副县长", "overlap_org": "勃利县人民政府", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 13, "type": "superior_subordinate", "context": "县长—副县长", "overlap_org": "勃利县人民政府", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 14, "type": "superior_subordinate", "context": "县长—副县长", "overlap_org": "勃利县人民政府", "overlap_period": "2026-至今"},
    {"person_a": 2, "person_b": 15, "type": "superior_subordinate", "context": "县长—副县长", "overlap_org": "勃利县人民政府", "overlap_period": "2026-至今"},
    # ── 市—县上下级关系 ──────────────────────────────────────────────────────
    {"person_a": 18, "person_b": 1, "type": "superior_subordinate", "context": "市委书记—县委书记", "overlap_org": "七台河市/勃利县", "overlap_period": "2026-至今"},
    {"person_a": 19, "person_b": 2, "type": "superior_subordinate", "context": "市长—县长", "overlap_org": "七台河市/勃利县", "overlap_period": "2026-至今"},
]

# ══════════════════════════════════════════════════════════════════════════════
# Build
# ══════════════════════════════════════════════════════════════════════════════

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

    print(f"\nBuild complete. Staging artifacts:")
    print(f"  DB:    {DB_PATH}")
    print(f"  GEXF:  {GEXF_PATH}")
    print(f"\nTo promote to canonical locations, from repo root run:")
    print(f"  python3 scripts/process_tmp.py data/tmp/heilongjiang_勃利县 --apply")
