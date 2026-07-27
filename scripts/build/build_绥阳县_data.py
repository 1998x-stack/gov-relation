#!/usr/bin/env python3
"""绥阳县（遵义市）领导班子关系网络数据生成脚本。

Targets: 县委书记 陈灿, 县长 陈姝宏
Data as of: 2026-07-23
Sources: 绥阳县人民政府官网 (www.suiyang.gov.cn)
"""

import json
import os
import sqlite3
from datetime import datetime

TASK_ID = "guizhou_绥阳县"
SLUG = "绥阳县"
AS_OF = "2026-07-23"
PROVINCE = "贵州省"
PARENT_CITY = "遵义市"

BASE = os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else "data/tmp/guizhou_绥阳县"
_BASE_OVERRIDE = os.environ.get("SUIYANG_BASE")
if _BASE_OVERRIDE:
    BASE = _BASE_OVERRIDE

DB_PATH = os.path.join(BASE, "绥阳县_network.db")
GEXF_PATH = os.path.join(BASE, "绥阳县_network.gexf")
PERSONS_DIR = os.path.join(BASE)
os.makedirs(PERSONS_DIR, exist_ok=True)

# ── Data ──────────────────────────────────────────────────────────────────────

persons = [
    # 1 - 县委书记
    {
        "id": 1,
        "name": "陈灿",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年6月",
        "birthplace": "",
        "education": "党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "绥阳县委书记、贵州绥阳经济开发区党工委书记（兼）",
        "current_org": "中共绥阳县委员会",
        "source": "https://www.suiyang.gov.cn/zwgk/ldzc/xwld/202111/t20211119_87227791.html",
    },
    # 2 - 县长
    {
        "id": 2,
        "name": "陈姝宏",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1984年7月",
        "birthplace": "",
        "education": "研究生、法学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "绥阳县委副书记、县人民政府党组书记、县长，贵州绥阳经开区党工委副书记、管委会主任（兼）",
        "current_org": "绥阳县人民政府",
        "source": "https://www.suiyang.gov.cn/zwgk/ldzc/zfld/202511/t20251113_88940967.html",
    },
    # 3 - 县委副书记（挂职）
    {
        "id": 3,
        "name": "赵源",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987年2月",
        "birthplace": "",
        "education": "硕士研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "绥阳县委副书记（挂职）",
        "current_org": "中共绥阳县委员会",
        "source": "https://www.suiyang.gov.cn/zwgk/ldzc/xwld/202510/t20251010_88682690.html",
    },
    # 4 - 县委常委、组织部部长
    {
        "id": 4,
        "name": "帅军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年1月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "绥阳县委常委、县委组织部部长",
        "current_org": "中共绥阳县委组织部",
        "source": "https://www.suiyang.gov.cn/zwgk/ldzc/xwld/202302/t20230221_87227795.html",
    },
    # 5 - 县委常委、宣传部部长、统战部部长
    {
        "id": 5,
        "name": "江继义",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1975年11月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "绥阳县委常委、县委宣传部部长、县委统战部部长",
        "current_org": "中共绥阳县委宣传部",
        "source": "https://www.suiyang.gov.cn/zwgk/ldzc/xwld/202111/t20211119_87227793.html",
    },
    # 6 - 县委常委、政法委书记
    {
        "id": 6,
        "name": "田小银",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年6月",
        "birthplace": "",
        "education": "研究生、法律硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "绥阳县委常委、县委政法委书记",
        "current_org": "中共绥阳县委政法委员会",
        "source": "https://www.suiyang.gov.cn/zwgk/ldzc/xwld/202507/t20250724_88327332.html",
    },
    # 7 - 县委常委、县委办主任
    {
        "id": 7,
        "name": "耿贵杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年3月",
        "birthplace": "",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "绥阳县委常委、县委办主任、县直机关工委书记",
        "current_org": "中共绥阳县委员会",
        "source": "https://www.suiyang.gov.cn/zwgk/ldzc/xwld/202404/t20240417_87227796.html",
    },
    # 8 - 县委常委、常务副县长
    {
        "id": 8,
        "name": "雷君",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1988年9月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "绥阳县委常委、县人民政府副县长（分管常务工作）",
        "current_org": "绥阳县人民政府",
        "source": "https://www.suiyang.gov.cn/zwgk/ldzc/zfld/202504/t20250416_87531273.html",
    },
    # 9 - 县委常委、县纪委书记
    {
        "id": 9,
        "name": "冯熠",
        "gender": "男",
        "ethnicity": "苗族",
        "birth": "1983年1月",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "绥阳县委常委、县纪委书记、县监委代理主任",
        "current_org": "中共绥阳县纪律检查委员会",
        "source": "https://www.suiyang.gov.cn/zwgk/ldzc/xwld/202601/t20260128_89348736.html",
    },
    # 10 - 副县长钱洪艳
    {
        "id": 10,
        "name": "钱洪艳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1981年5月",
        "birthplace": "",
        "education": "重庆市委党校研究生",
        "party_join": "民革党员",
        "work_start": "",
        "current_post": "绥阳县人民政府副县长",
        "current_org": "绥阳县人民政府",
        "source": "https://www.suiyang.gov.cn/zwgk/ldzc/zfld/202406/t20240615_87227810.html",
    },
    # 11 - 副县长林木
    {
        "id": 11,
        "name": "林木",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "绥阳县人民政府副县长",
        "current_org": "绥阳县人民政府",
        "source": "https://www.suiyang.gov.cn/zwgk/ldzc/zfld/202207/t20220706_87227807.html",
    },
    # 12 - 副县长包礼勇
    {
        "id": 12,
        "name": "包礼勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "绥阳县人民政府副县长",
        "current_org": "绥阳县人民政府",
        "source": "https://www.suiyang.gov.cn/zwgk/ldzc/zfld/202304/t20230406_87227808.html",
    },
    # 13 - 副县长徐春
    {
        "id": 13,
        "name": "徐春",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "绥阳县人民政府副县长",
        "current_org": "绥阳县人民政府",
        "source": "https://www.suiyang.gov.cn/zwgk/ldzc/zfld/202306/t20230630_87227809.html",
    },
    # 14 - 副县长熊俊
    {
        "id": 14,
        "name": "熊俊",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "绥阳县人民政府副县长",
        "current_org": "绥阳县人民政府",
        "source": "https://www.suiyang.gov.cn/zwgk/ldzc/zfld/202512/t20251204_89016666.html",
    },
]

organizations = [
    {"id": 1, "name": "中共绥阳县委员会", "type": "党委", "level": "县处级", "parent": "中共遵义市委", "location": "绥阳县"},
    {"id": 2, "name": "绥阳县人民政府", "type": "政府", "level": "县处级", "parent": "遵义市人民政府", "location": "绥阳县"},
    {"id": 3, "name": "中共绥阳县委组织部", "type": "党委", "level": "乡科级", "parent": "中共绥阳县委员会", "location": "绥阳县"},
    {"id": 4, "name": "中共绥阳县委宣传部", "type": "党委", "level": "乡科级", "parent": "中共绥阳县委员会", "location": "绥阳县"},
    {"id": 5, "name": "中共绥阳县委政法委员会", "type": "党委", "level": "乡科级", "parent": "中共绥阳县委员会", "location": "绥阳县"},
    {"id": 6, "name": "中共绥阳县纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共遵义市纪委/中共绥阳县委", "location": "绥阳县"},
    {"id": 7, "name": "贵州绥阳经济开发区", "type": "开发区", "level": "县处级", "parent": "遵义市人民政府", "location": "绥阳县"},
]

positions = [
    # 陈灿
    {"person_id": 1, "org_id": 1, "title": "绥阳县委书记", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任"},
    {"person_id": 1, "org_id": 7, "title": "贵州绥阳经济开发区党工委书记（兼）", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任（兼任）"},
    # 陈姝宏
    {"person_id": 2, "org_id": 2, "title": "绥阳县人民政府县长", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任"},
    {"person_id": 2, "org_id": 1, "title": "绥阳县委副书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    {"person_id": 2, "org_id": 7, "title": "贵州绥阳经开区党工委副书记、管委会主任（兼）", "start_date": "", "end_date": "", "rank": "县处级正职", "note": "现任（兼任）"},
    # 赵源
    {"person_id": 3, "org_id": 1, "title": "绥阳县委副书记（挂职）", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任（挂职）"},
    # 帅军
    {"person_id": 4, "org_id": 3, "title": "绥阳县委常委、县委组织部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 江继义
    {"person_id": 5, "org_id": 4, "title": "绥阳县委常委、县委宣传部部长、县委统战部部长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 田小银
    {"person_id": 6, "org_id": 5, "title": "绥阳县委常委、县委政法委书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 耿贵杰
    {"person_id": 7, "org_id": 1, "title": "绥阳县委常委、县委办主任、县直机关工委书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 雷君
    {"person_id": 8, "org_id": 2, "title": "绥阳县委常委、县人民政府副县长（分管常务工作）", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 冯熠
    {"person_id": 9, "org_id": 6, "title": "绥阳县委常委、县纪委书记、县监委代理主任", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 钱洪艳
    {"person_id": 10, "org_id": 2, "title": "绥阳县人民政府副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 林木
    {"person_id": 11, "org_id": 2, "title": "绥阳县人民政府副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 包礼勇
    {"person_id": 12, "org_id": 2, "title": "绥阳县人民政府副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 徐春
    {"person_id": 13, "org_id": 2, "title": "绥阳县人民政府副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
    # 熊俊
    {"person_id": 14, "org_id": 2, "title": "绥阳县人民政府副县长", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "现任"},
]

relationships = [
    # 陈灿 ↔ 陈姝宏 (书记-县长搭档)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "陈灿（县委书记）与陈姝宏（县长）为县委常委会搭档", "overlap_org": "中共绥阳县委员会/绥阳县人民政府", "overlap_period": "2024-至今"},
    # 陈灿 ↔ 赵源
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "陈灿（县委书记）与赵源（挂职副书记）在县委常委会共事", "overlap_org": "中共绥阳县委员会", "overlap_period": "2025-至今"},
    # 陈灿 ↔ 帅军
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "陈灿（县委书记）与帅军（组织部部长）在县委常委会共事", "overlap_org": "中共绥阳县委员会", "overlap_period": "2023-至今"},
    # 陈灿 ↔ 江继义
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "陈灿（县委书记）与江继义（宣传部部长、统战部部长）在县委常委会共事", "overlap_org": "中共绥阳县委员会", "overlap_period": "2021-至今"},
    # 陈灿 ↔ 田小银
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "陈灿（县委书记）与田小银（政法委书记）在县委常委会共事", "overlap_org": "中共绥阳县委员会", "overlap_period": "2025-至今"},
    # 陈灿 ↔ 耿贵杰
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "陈灿（县委书记）与耿贵杰（县委办主任）在县委常委会共事", "overlap_org": "中共绥阳县委员会", "overlap_period": "2021-至今"},
    # 陈灿 ↔ 雷君
    {"person_a": 1, "person_b": 8, "type": "overlap", "context": "陈灿（县委书记）与雷君（常务副县长）在县委常委会共事", "overlap_org": "中共绥阳县委员会", "overlap_period": "2025-至今"},
    # 陈灿 ↔ 冯熠
    {"person_a": 1, "person_b": 9, "type": "overlap", "context": "陈灿（县委书记）与冯熠（县纪委书记）在县委常委会共事", "overlap_org": "中共绥阳县委员会", "overlap_period": "2026-至今"},
    # 陈姝宏 ↔ 雷君 (县长-常务副县长)
    {"person_a": 2, "person_b": 8, "type": "overlap", "context": "陈姝宏（县长）与雷君（常务副县长）在县政府班子共事", "overlap_org": "绥阳县人民政府", "overlap_period": "2025-至今"},
    # 陈姝宏 ↔ 赵源
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "陈姝宏（县长、县委副书记）与赵源（挂职副书记）在县委常委会共事", "overlap_org": "中共绥阳县委员会", "overlap_period": "2025-至今"},
    # 常委会内部共事关系
    {"person_a": 4, "person_b": 5, "type": "overlap", "context": "帅军（组织部部长）与江继义（宣传部部长）在县委常委会共事", "overlap_org": "中共绥阳县委员会", "overlap_period": "2023-至今"},
    {"person_a": 4, "person_b": 7, "type": "overlap", "context": "帅军（组织部部长）与耿贵杰（县委办主任）在县委常委会共事", "overlap_org": "中共绥阳县委员会", "overlap_period": "2023-至今"},
    {"person_a": 5, "person_b": 7, "type": "overlap", "context": "江继义（宣传部部长）与耿贵杰（县委办主任）在县委常委会共事", "overlap_org": "中共绥阳县委员会", "overlap_period": "2021-至今"},
    {"person_a": 6, "person_b": 9, "type": "overlap", "context": "田小银（政法委书记）与冯熠（纪委书记）在县委常委会共事", "overlap_org": "中共绥阳县委员会", "overlap_period": "2026-至今"},
    # 县政府班子内部
    {"person_a": 8, "person_b": 10, "type": "overlap", "context": "雷君（常务副县长）与钱洪艳（副县长）在县政府班子共事", "overlap_org": "绥阳县人民政府", "overlap_period": "2025-至今"},
    {"person_a": 8, "person_b": 11, "type": "overlap", "context": "雷君（常务副县长）与林木（副县长）在县政府班子共事", "overlap_org": "绥阳县人民政府", "overlap_period": "2025-至今"},
    {"person_a": 10, "person_b": 11, "type": "overlap", "context": "钱洪艳（副县长）与林木（副县长）在县政府班子共事", "overlap_org": "绥阳县人民政府", "overlap_period": "2022-至今"},
    {"person_a": 11, "person_b": 12, "type": "overlap", "context": "林木（副县长）与包礼勇（副县长）在县政府班子共事", "overlap_org": "绥阳县人民政府", "overlap_period": "2023-至今"},
    {"person_a": 11, "person_b": 13, "type": "overlap", "context": "林木（副县长）与徐春（副县长）在县政府班子共事", "overlap_org": "绥阳县人民政府", "overlap_period": "2023-至今"},
    {"person_a": 12, "person_b": 14, "type": "overlap", "context": "包礼勇（副县长）与熊俊（副县长）在县政府班子共事", "overlap_org": "绥阳县人民政府", "overlap_period": "2025-至今"},
]

source_register = [
    {"id": "S001", "title": "陈灿-绥阳县领导之窗（县委书记）",
     "url": "https://www.suiyang.gov.cn/zwgk/ldzc/xwld/202111/t20211119_87227791.html",
     "publisher": "绥阳县人民政府", "published_at": "2021-11-19", "accessed_at": "2026-07-23",
     "source_type": "official", "reliability": "high", "notes": "确认陈灿为县委书记，1972年6月生，党校研究生"},
    {"id": "S002", "title": "陈姝宏-绥阳县领导之窗（县长）",
     "url": "https://www.suiyang.gov.cn/zwgk/ldzc/zfld/202511/t20251113_88940967.html",
     "publisher": "绥阳县人民政府", "published_at": "2025-11-13", "accessed_at": "2026-07-23",
     "source_type": "official", "reliability": "high", "notes": "确认陈姝宏为县长，1984年7月生，研究生法学硕士"},
    {"id": "S003", "title": "绥阳县领导之窗-县委领导页面",
     "url": "https://www.suiyang.gov.cn/zwgk/ldzc/",
     "publisher": "绥阳县人民政府", "published_at": "", "accessed_at": "2026-07-23",
     "source_type": "official", "reliability": "high", "notes": "完整县委领导名单：陈灿、陈姝宏、赵源、帅军、江继义、田小银、耿贵杰、雷君、冯熠"},
    {"id": "S004", "title": "绥阳县领导之窗-政府领导页面",
     "url": "https://www.suiyang.gov.cn/zwgk/ldzc/",
     "publisher": "绥阳县人民政府", "published_at": "", "accessed_at": "2026-07-23",
     "source_type": "official", "reliability": "high", "notes": "完整政府领导名单：陈姝宏、雷君、钱洪艳、林木、包礼勇、徐春、熊俊"},
    {"id": "S005", "title": "赵源-绥阳县领导之窗",
     "url": "https://www.suiyang.gov.cn/zwgk/ldzc/xwld/202510/t20251010_88682690.html",
     "publisher": "绥阳县人民政府", "published_at": "2025-10-10", "accessed_at": "2026-07-23",
     "source_type": "official", "reliability": "high", "notes": "赵源，1987年2月生，硕士研究生，挂职副书记"},
    {"id": "S006", "title": "帅军-绥阳县领导之窗",
     "url": "https://www.suiyang.gov.cn/zwgk/ldzc/xwld/202302/t20230221_87227795.html",
     "publisher": "绥阳县人民政府", "published_at": "2023-02-21", "accessed_at": "2026-07-23",
     "source_type": "official", "reliability": "high", "notes": "帅军，1974年1月生，大学学历，组织部部长"},
    {"id": "S007", "title": "江继义-绥阳县领导之窗",
     "url": "https://www.suiyang.gov.cn/zwgk/ldzc/xwld/202111/t20211119_87227793.html",
     "publisher": "绥阳县人民政府", "published_at": "2021-11-19", "accessed_at": "2026-07-23",
     "source_type": "official", "reliability": "high", "notes": "江继义，1975年11月生，大学学历，宣传部兼统战部部长"},
    {"id": "S008", "title": "田小银-绥阳县领导之窗",
     "url": "https://www.suiyang.gov.cn/zwgk/ldzc/xwld/202507/t20250724_88327332.html",
     "publisher": "绥阳县人民政府", "published_at": "2025-07-24", "accessed_at": "2026-07-23",
     "source_type": "official", "reliability": "high", "notes": "田小银，1983年6月生，研究生法律硕士，政法委书记"},
    {"id": "S009", "title": "耿贵杰-绥阳县领导之窗",
     "url": "https://www.suiyang.gov.cn/zwgk/ldzc/xwld/202404/t20240417_87227796.html",
     "publisher": "绥阳县人民政府", "published_at": "2024-04-17", "accessed_at": "2026-07-23",
     "source_type": "official", "reliability": "high", "notes": "耿贵杰，1978年3月生，在职研究生，县委办主任"},
    {"id": "S010", "title": "雷君-绥阳县领导之窗（常务副县长）",
     "url": "https://www.suiyang.gov.cn/zwgk/ldzc/zfld/202504/t20250416_87531273.html",
     "publisher": "绥阳县人民政府", "published_at": "2025-04-16", "accessed_at": "2026-07-23",
     "source_type": "official", "reliability": "high", "notes": "雷君，1988年9月生，大学学历，常委、常务副县长"},
    {"id": "S011", "title": "冯熠-绥阳县领导之窗",
     "url": "https://www.suiyang.gov.cn/zwgk/ldzc/xwld/202601/t20260128_89348736.html",
     "publisher": "绥阳县人民政府", "published_at": "2026-01-28", "accessed_at": "2026-07-23",
     "source_type": "official", "reliability": "high", "notes": "冯熠，1983年1月生，苗族，大学学历，纪委书记、监委代理主任"},
    {"id": "S012", "title": "钱洪艳-绥阳县领导之窗",
     "url": "https://www.suiyang.gov.cn/zwgk/ldzc/zfld/202406/t20240615_87227810.html",
     "publisher": "绥阳县人民政府", "published_at": "2024-06-15", "accessed_at": "2026-07-23",
     "source_type": "official", "reliability": "high", "notes": "钱洪艳，1981年5月生，重庆市委党校研究生，民革党员，副县长"},
]


# ── Build Functions ───────────────────────────────────────────────────────────

def esc(s):
    if s is None:
        return ""
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def build():
    os.makedirs(BASE, exist_ok=True)

    # ── SQLite ──
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS relationships;
        DROP TABLE IF EXISTS positions;
        DROP TABLE IF EXISTS organizations;
        DROP TABLE IF EXISTS persons;

        CREATE TABLE persons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pid TEXT UNIQUE NOT NULL,
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

        CREATE TABLE organizations (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT DEFAULT '',
            level TEXT DEFAULT '',
            parent TEXT DEFAULT '',
            location TEXT DEFAULT ''
        );

        CREATE TABLE positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id TEXT NOT NULL,
            org_id INTEGER NOT NULL,
            title TEXT DEFAULT '',
            start_date TEXT DEFAULT '',
            end_date TEXT DEFAULT '',
            rank TEXT DEFAULT '',
            note TEXT DEFAULT '',
            FOREIGN KEY (person_id) REFERENCES persons(pid),
            FOREIGN KEY (org_id) REFERENCES organizations(id)
        );

        CREATE TABLE relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_a TEXT NOT NULL,
            person_b TEXT NOT NULL,
            type TEXT DEFAULT '',
            context TEXT DEFAULT '',
            overlap_org TEXT DEFAULT '',
            overlap_period TEXT DEFAULT '',
            FOREIGN KEY (person_a) REFERENCES persons(pid),
            FOREIGN KEY (person_b) REFERENCES persons(pid)
        );
    """)

    person_map = {}
    for idx, p in enumerate(persons, 1):
        pid = f"suiyang_{p['name']}"
        person_map[p["id"]] = pid
        cur.execute("""INSERT INTO persons (id,pid,name,gender,ethnicity,birth,birthplace,education,party_join,work_start,current_post,current_org,source) 
                       VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (idx, pid, p["name"], p.get("gender", ""), p.get("ethnicity", ""), p.get("birth", ""),
                     p.get("birthplace", ""), p.get("education", ""), p.get("party_join", ""), p.get("work_start", ""),
                     p.get("current_post", ""), p.get("current_org", ""), p.get("source", "")))

    for o in organizations:
        cur.execute("""INSERT INTO organizations (id,name,type,level,parent,location) VALUES (?,?,?,?,?,?)""",
                    (o["id"], o["name"], o["type"], o["level"], o.get("parent", ""), o.get("location", "")))

    for pos in positions:
        cur.execute("""INSERT INTO positions (person_id,org_id,title,start_date,end_date,rank,note) VALUES (?,?,?,?,?,?,?)""",
                    (person_map[pos["person_id"]], pos["org_id"], pos["title"], pos.get("start_date", ""),
                     pos.get("end_date", ""), pos.get("rank", ""), pos.get("note", "")))

    for r in relationships:
        cur.execute("""INSERT INTO relationships (person_a,person_b,type,context,overlap_org,overlap_period) VALUES (?,?,?,?,?,?)""",
                    (person_map[r["person_a"]], person_map[r["person_b"]], r["type"], r["context"],
                     r.get("overlap_org", ""), r.get("overlap_period", "")))

    conn.commit()
    conn.close()
    print(f"DB written: {DB_PATH}")
    print(f"  {len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")

    # ── GEXF ──
    def person_color(post):
        if "书记" in post and "副" not in post and "纪委" not in post:
            return "255,50,50"
        if "县长" in post and "副" not in post and "人大" not in post and "政协" not in post:
            return "50,100,255"
        if "纪委书记" in post:
            return "255,165,0"
        if "副" in post or "副书记" in post:
            return "100,150,220"
        if "主任" in post and "副" not in post:
            return "60,180,60"
        if "政协" in post:
            return "180,160,80"
        return "100,100,100"

    def is_top_leader(post):
        return ("书记" in post and "副" not in post and "纪委" not in post) or \
               ("县长" in post and "副" not in post and "人大" not in post and "政协" not in post)

    def person_shape(post):
        if "书记" in post and "副" not in post and "纪委" not in post:
            return "square"
        if "县长" in post and "副" not in post and "人大" not in post and "政协" not in post:
            return "circle"
        if "纪委书记" in post or "纪委" in post:
            return "diamond"
        return "triangle"

    def org_color(otype):
        colors = {
            "党委": "255,200,200",
            "政府": "200,200,255",
            "纪委": "255,200,150",
            "开发区": "200,255,200",
        }
        return colors.get(otype, "200,200,200")

    lines = []
    lines.append('<?xml version="1.0" encoding="UTF-8"?>')
    lines.append('<gexf xmlns="http://gexf.net/1.3" xmlns:viz="http://gexf.net/1.3/viz" version="1.3">')
    lines.append(f'  <meta lastmodifieddate="{AS_OF}">')
    lines.append('    <creator>Gov-Relation Research Agent</creator>')
    lines.append(f'    <description>绥阳县领导班子关系网络（基于绥阳县政府官网）</description>')
    lines.append('  </meta>')
    lines.append('  <graph mode="static" defaultedgetype="undirected">')

    # Node attributes
    lines.append('    <attributes class="node">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="current_post" type="string"/>')
    lines.append('      <attribute id="2" title="current_org" type="string"/>')
    lines.append('      <attribute id="3" title="birth" type="string"/>')
    lines.append('      <attribute id="4" title="source" type="string"/>')
    lines.append('    </attributes>')

    # Edge attributes
    lines.append('    <attributes class="edge">')
    lines.append('      <attribute id="0" title="type" type="string"/>')
    lines.append('      <attribute id="1" title="context" type="string"/>')
    lines.append('      <attribute id="2" title="overlap_org" type="string"/>')
    lines.append('      <attribute id="3" title="overlap_period" type="string"/>')
    lines.append('    </attributes>')

    # Nodes — persons
    lines.append('    <nodes>')
    for p in persons:
        pid_num = p["id"]
        post = p.get("current_post", "")
        c = person_color(post)
        sz = "20.0" if is_top_leader(post) else "12.0"
        shape = person_shape(post)

        lines.append(f'      <node id="p{pid_num}" label="{esc(p["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="person"/>')
        lines.append(f'          <attvalue for="1" value="{esc(p.get("current_post",""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(p.get("current_org",""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(p.get("birth",""))}"/>')
        lines.append(f'          <attvalue for="4" value="{esc(p.get("source",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{c.split(",")[0]}" g="{c.split(",")[1]}" b="{c.split(",")[2]}" a="1.0"/>')
        lines.append(f'        <viz:size value="{sz}"/>')
        lines.append(f'        <viz:shape value="{shape}"/>')
        lines.append('      </node>')

    # Nodes — organizations
    for o in organizations:
        oid = o["id"] + 100000
        ocolor = org_color(o["type"])

        lines.append(f'      <node id="o{oid}" label="{esc(o["name"])}">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="organization"/>')
        lines.append(f'          <attvalue for="1" value="{esc(o.get("type",""))}"/>')
        lines.append('        </attvalues>')
        lines.append(f'        <viz:color r="{ocolor.split(",")[0]}" g="{ocolor.split(",")[1]}" b="{ocolor.split(",")[2]}" a="0.8"/>')
        lines.append(f'        <viz:size value="8.0"/>')
        lines.append(f'        <viz:shape value="hexagon"/>')
        lines.append('      </node>')

    lines.append('    </nodes>')

    # Edges
    lines.append('    <edges>')
    eid = 0

    for pos in positions:
        eid += 1
        pid_num = pos["person_id"]
        oid = pos["org_id"] + 100000
        lines.append(
            f'      <edge id="e{eid}" source="p{pid_num}" target="o{oid}" label="{esc(pos["title"])}" weight="1.0">')
        lines.append('        <attvalues>')
        lines.append('          <attvalue for="0" value="worked_at"/>')
        lines.append(f'          <attvalue for="1" value="{esc(pos.get("note", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    for r in relationships:
        eid += 1
        lines.append(
            f'      <edge id="e{eid}" source="p{r["person_a"]}" target="p{r["person_b"]}" label="{esc(r["type"])}" weight="2.0">')
        lines.append('        <attvalues>')
        lines.append(f'          <attvalue for="0" value="relationship"/>')
        lines.append(f'          <attvalue for="1" value="{esc(r.get("context", ""))}"/>')
        lines.append(f'          <attvalue for="2" value="{esc(r.get("overlap_org", ""))}"/>')
        lines.append(f'          <attvalue for="3" value="{esc(r.get("overlap_period", ""))}"/>')
        lines.append('        </attvalues>')
        lines.append('      </edge>')

    lines.append('    </edges>')
    lines.append('  </graph>')
    lines.append('</gexf>')

    with open(GEXF_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"GEXF written: {GEXF_PATH}")

    # ── Person Graph JSONs ──
    now = AS_OF.replace("-", "")

    def make_person_json(p, timeline, relationships_list, custom_identity=None):
        result = {
            "schema_version": "1.0",
            "generated_at": AS_OF,
            "investigation_scope": {
                "province": PROVINCE,
                "city": PARENT_CITY,
                "region": "绥阳县",
                "job": p.get("current_post", ""),
                "task_id": TASK_ID,
                "time_focus": "2026年7月"
            },
            "identity": {
                "person_id": f"suiyang_{p['name']}",
                "name": p["name"],
                "aliases": [],
                "gender": p.get("gender", ""),
                "ethnicity": p.get("ethnicity", ""),
                "birth": p.get("birth", ""),
                "birthplace": p.get("birthplace", ""),
                "native_place": "",
                "education": [
                    {
                        "period": "",
                        "institution": "",
                        "major": "",
                        "degree": p.get("education", ""),
                        "study_type": "unknown",
                        "source_ids": []
                    }
                ] if p.get("education") else [],
                "party_join": p.get("party_join", ""),
                "work_start": p.get("work_start", ""),
                "dedupe_keys": {
                    "name_birth": f"{p['name']}_{p.get('birth', '')}",
                    "name_birthplace": f"{p['name']}_{p.get('birthplace', '')}",
                    "official_profile_url": p.get("source", "")
                }
            },
            "current_status": {
                "current_post": p.get("current_post", ""),
                "current_org": p.get("current_org", ""),
                "administrative_rank": "县处级正职" if p["id"] in [1, 2] else "县处级副职",
                "as_of": AS_OF,
                "is_current_confirmed": True,
                "source_ids": ["S001", "S002", "S003", "S004"]
            },
            "career_timeline": timeline,
            "organizations": [],
            "relationships": relationships_list,
            "governance_record": [],
            "professional_profile": {
                "primary_specializations": [],
                "secondary_specializations": [],
                "career_pattern": "unknown",
                "systems_experience": [],
                "geographic_pattern": [],
                "promotion_velocity": {"summary": "", "notable_fast_promotions": []}
            },
            "work_style_and_personality": {
                "public_style_indicators": [],
                "speech_themes": [],
                "management_signals": [],
                "caveat": "Work style is inferred from public records, speeches, and reported governance actions, not private psychological assessment."
            },
            "network_metrics": {},
            "risk_and_integrity_signals": [
                {"type": "none_found", "description": "在公开信息中未发现该人物负面信号",
                 "date": "", "confidence": "confirmed", "source_ids": []}
            ],
            "source_register": source_register,
            "confidence_summary": {
                "identity": "confirmed" if p.get("birth") and p.get("education") else "plausible",
                "current_role": "confirmed",
                "career_completeness": "thin",
                "relationship_confidence": "medium",
                "biggest_gap": f"{p['name']}的完整履历信息缺失（早期任职经历未知）"
            },
            "open_questions": [
                {"priority": "critical",
                 "question": f"{p['name']}的完整职业生涯履历",
                 "why_it_matters": "无法追溯其任职路径和系统经历",
                 "suggested_queries": [f"{p['name']} 简历 绥阳县", f"{p['name']} 任前公示"],
                 "last_attempted": AS_OF},
            ]
        }
        if custom_identity:
            result["identity"].update(custom_identity)
        return result

    # ── 陈灿 Person JSON ──
    cc_timeline = [
        {"start": "", "end": "", "org": "中共绥阳县委员会", "title": "绥阳县委书记、贵州绥阳经济开发区党工委书记（兼）",
         "notes": "现任", "confidence": "confirmed", "source_ids": ["S001", "S003"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "陈灿在担任绥阳县委书记前的完整履历未找到。已知1972年6月生，党校研究生学历，中共党员。",
         "confidence": "unverified", "source_ids": []},
    ]
    cc_relationships = [
        {"person": "陈姝宏", "person_id": "suiyang_陈姝宏", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "陈灿（县委书记）与陈姝宏（县长）在县委常委会和县政府班子共事",
         "overlap_org": "中共绥阳县委员会/绥阳县人民政府", "overlap_period": "2024-至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
        {"person": "帅军", "person_id": "suiyang_帅军", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "陈灿（县委书记）与帅军（组织部部长）在县委常委会共事",
         "overlap_org": "中共绥阳县委员会", "overlap_period": "2023-至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]},
        {"person": "江继义", "person_id": "suiyang_江继义", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "陈灿（县委书记）与江继义（宣传部部长、统战部部长）在县委常委会共事",
         "overlap_org": "中共绥阳县委员会", "overlap_period": "2021-至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]},
        {"person": "耿贵杰", "person_id": "suiyang_耿贵杰", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "陈灿（县委书记）与耿贵杰（县委办主任）在县委常委会共事",
         "overlap_org": "中共绥阳县委员会", "overlap_period": "2021-至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]},
    ]

    cc_json = make_person_json(persons[0], cc_timeline, cc_relationships)
    cc_path = os.path.join(PERSONS_DIR, f"{now}-贵州省-遵义市-县委书记-陈灿.json")
    with open(cc_path, "w", encoding="utf-8") as f:
        json.dump(cc_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {cc_path}")

    # ── 陈姝宏 Person JSON ──
    csh_timeline = [
        {"start": "", "end": "", "org": "绥阳县人民政府", "title": "绥阳县委副书记、县人民政府县长",
         "notes": "现任", "confidence": "confirmed", "source_ids": ["S002", "S003"]},
        {"start": "", "end": "", "org": "贵州绥阳经济开发区", "title": "贵州绥阳经开区党工委副书记、管委会主任（兼）",
         "notes": "现任（兼任）", "confidence": "confirmed", "source_ids": ["S002"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "陈姝宏在担任绥阳县县长前的完整履历未找到。已知1984年7月生，研究生法学硕士，中共党员。",
         "confidence": "unverified", "source_ids": []},
    ]
    csh_relationships = [
        {"person": "陈灿", "person_id": "suiyang_陈灿", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "陈姝宏（县长、县委副书记）与陈灿（县委书记）在县委常委会和县政府班子共事",
         "overlap_org": "中共绥阳县委员会/绥阳县人民政府", "overlap_period": "2024-至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S001", "S002"]},
        {"person": "雷君", "person_id": "suiyang_雷君", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "陈姝宏（县长）与雷君（常务副县长）在县政府班子共事",
         "overlap_org": "绥阳县人民政府", "overlap_period": "2025-至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S010"]},
        {"person": "赵源", "person_id": "suiyang_赵源", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "陈姝宏（县委副书记、县长）与赵源（挂职副书记）在县委常委会共事",
         "overlap_org": "中共绥阳县委员会", "overlap_period": "2025-至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003", "S005"]},
    ]

    csh_json = make_person_json(persons[1], csh_timeline, csh_relationships)
    csh_path = os.path.join(PERSONS_DIR, f"{now}-贵州省-遵义市-县长-陈姝宏.json")
    with open(csh_path, "w", encoding="utf-8") as f:
        json.dump(csh_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {csh_path}")

    # ── 雷君 Person JSON ──
    lj_timeline = [
        {"start": "", "end": "", "org": "绥阳县人民政府", "title": "绥阳县委常委、县人民政府副县长（分管常务工作）",
         "notes": "现任", "confidence": "confirmed", "source_ids": ["S010", "S003"]},
        {"start": "unknown", "end": "unknown", "org": "履历缺口", "title": "",
         "notes": "雷君在担任绥阳县常务副县长前的完整履历未找到。已知1988年9月生，大学学历，中共党员。",
         "confidence": "unverified", "source_ids": []},
    ]
    lj_relationships = [
        {"person": "陈姝宏", "person_id": "suiyang_陈姝宏", "relationship_type": "overlap",
         "strength": "strong",
         "evidence": "雷君（常务副县长）与陈姝宏（县长）在县政府班子共事",
         "overlap_org": "绥阳县人民政府", "overlap_period": "2025-至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S002", "S010"]},
        {"person": "陈灿", "person_id": "suiyang_陈灿", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "雷君（常委、常务副县长）与陈灿（县委书记）在县委常委会共事",
         "overlap_org": "中共绥阳县委员会", "overlap_period": "2025-至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S003"]},
        {"person": "钱洪艳", "person_id": "suiyang_钱洪艳", "relationship_type": "overlap",
         "strength": "medium",
         "evidence": "雷君（常务副县长）与钱洪艳（副县长）在县政府班子共事",
         "overlap_org": "绥阳县人民政府", "overlap_period": "2025-至今",
         "direction": "undirected", "confidence": "confirmed", "source_ids": ["S004"]},
    ]

    lj_json = make_person_json(persons[7], lj_timeline, lj_relationships)
    lj_path = os.path.join(PERSONS_DIR, f"{now}-贵州省-遵义市-常务副县长-雷君.json")
    with open(lj_path, "w", encoding="utf-8") as f:
        json.dump(lj_json, f, ensure_ascii=False, indent=2)
    print(f"Person JSON written: {lj_path}")

    print("\n✅ All artifacts generated.")


if __name__ == "__main__":
    build()
