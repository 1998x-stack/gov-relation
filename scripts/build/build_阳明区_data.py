#!/usr/bin/env python3
"""阳明区(牡丹江市) 领导班子工作关系网络 — 数据构建脚本.

任务: heilongjiang_阳明区
地区: 黑龙江省牡丹江市阳明区(市辖区)
目标: 区委书记 & 区长
数据基准: 截至 2026-08-05
一手来源: 阳明区人民政府官网「领导之窗」
  - 领导之窗索引 https://www.yangming.gov.cn/mdjymqrmzf/c102127/ldzc.shtml
  - 区委领导   https://www.yangming.gov.cn/mdjymqrmzf/c102128/ldzc.shtml (孙传宝 c03_342930, 葛建军 c03_1047881, ...)
  - 区政府领导 https://www.yangming.gov.cn/mdjymqrmzf/c102130/ldzc.shtml
  - 区人大     https://www.yangming.gov.cn/mdjymqrmzf/c102129/ldzc.shtml
  - 区政协     https://www.yangming.gov.cn/mdjymqrmzf/c102131/ldzc.shtml

运行: python3 scripts/build/build_阳明区_data.py  (或暂存区内直接运行)
"""

import sqlite3
from pathlib import Path

import sys

# 定位仓库根目录：脚本可能在 data/tmp/<task>/（parents[3]）或 scripts/build/（parents[2]）下运行
_BASE = Path(__file__).resolve().parent
if _BASE.name == "build" and _BASE.parent.name == "scripts":
    _ROOT = _BASE.parents[1]
else:
    _ROOT = _BASE.parents[3]
sys.path.insert(0, str(_ROOT))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── 输出目录：在 scripts/build/ 下运行写规范路径，在暂存区运行写暂存区 ──
STAGING = Path(__file__).resolve().parent
if STAGING.name == "build" and STAGING.parent.name == "scripts":
    DB_PATH = DATABASE_DIR / "阳明区_network.db"
    GEXF_PATH = GRAPH_DIR / "阳明区_network.gexf"
else:
    DB_PATH = STAGING / "阳明区_network.db"
    GEXF_PATH = STAGING / "阳明区_network.gexf"

# ══════════════════════════════════════════════════════════════
# 人员 (persons)  — 全部为官方领导之窗 confirmed
# 来源缩写: O = 阳明区人民政府官网领导之窗 (访问 2026-08-05)
# ══════════════════════════════════════════════════════════════
persons = [
    # ── 核心: 区委书记 ──
    {
        "id": 1,
        "name": "孙传宝",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "黑龙江省穆棱市",
        "education": "待查",
        "party_join": "2000年6月",
        "work_start": "待查",
        "current_post": "阳明区委书记、一级调研员",
        "current_org": "中共牡丹江市阳明区委员会",
        "source": "O-阳明区政府官网领导之窗-区委(c102128/202109/c03_342930.shtml)",
    },
    # ── 核心: 区委副书记、区长 ──
    {
        "id": 2,
        "name": "葛建军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "黑龙江省牡丹江市",
        "education": "待查",
        "party_join": "2000年6月",
        "work_start": "待查",
        "current_post": "阳明区委副书记、区长",
        "current_org": "牡丹江市阳明区人民政府",
        "source": "O-阳明区政府官网领导之窗-区长页(c102130/202605/c03_1047887.shtml);区委页(c102128/202605/c03_1047881.shtml)",
    },
    # ── 区委常委会 ──
    {
        "id": 3,
        "name": "陈兆中",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "黑龙江省牡丹江市",
        "education": "待查",
        "party_join": "2000年6月",
        "work_start": "待查",
        "current_post": "阳明区委常委、纪委书记、监委主任、三级高级监察官",
        "current_org": "中共牡丹江市阳明区纪律检查委员会",
        "source": "O-阳明区官网-区委页(c102128/202508/c03_1014333.shtml)",
    },
    {
        "id": 4,
        "name": "邵宗杰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "黑龙江省牡丹江市",
        "education": "待查",
        "party_join": "2003年6月",
        "work_start": "待查",
        "current_post": "阳明区委常委、组织部部长、统战部部长兼区政协党组副书记",
        "current_org": "中共牡丹江市阳明区委员会",
        "source": "O-阳明区委官网-区委(c102128/202404/c03_923690.shtml)",
    },
    {
        "id": 5,
        "name": "王鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "黑龙江省密山市",
        "education": "待查",
        "party_join": "1998年5月",
        "work_start": "待查",
        "current_post": "阳明区委常委、武装部部长",
        "current_org": "牡丹江市阳明区人民武装部",
        "source": "O-阳明区委官网-区委(c102128/202109/c03_342928.shtml)",
    },
    {
        "id": 6,
        "name": "赵双美",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "黑龙江省哈尔滨市",
        "education": "待查",
        "party_join": "2006年5月",
        "work_start": "待查",
        "current_post": "阳明区委常委、政府副区长(常务)",
        "current_org": "牡丹江市阳明区人民政府",
        "source": "O-阳明区委(区委 202209/c03_342942.shtml; 政府 202505/c03_988693.shtml)",
    },
    {
        "id": 7,
        "name": "葛岩松",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "黑龙江省兰西县",
        "education": "待查",
        "party_join": "2016年6月",
        "work_start": "待查",
        "current_post": "阳明区委常委、铁岭镇党委书记",
        "current_org": "中共牡丹江市阳明区铁岭镇委员会",
        "source": "O-阳明区委官网-区委(202209/c03_342940.shtml)",
    },
    {
        "id": 8,
        "name": "周庆婉",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "黑龙江省牡丹江市",
        "education": "待查",
        "party_join": "2011年5月",
        "work_start": "待查",
        "current_post": "阳明区委常委、宣传部部长兼五林镇党委书记",
        "current_org": "中共牡丹江市阳明区委员会",
        "source": "O-阳明区委(202508/c03_1014583.shtml)",
    },
    # ── 区政府其余副区长 ──
    {
        "id": 9,
        "name": "张蕾",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "吉林省长春市",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "阳明区政府副区长",
        "current_org": "牡丹江市阳明区人民政府",
        "source": "O-阳明区政府(c102130/202505/c03_1005599.shtml)",
    },
    {
        "id": 10,
        "name": "任智锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "黑龙江省牡丹江市",
        "education": "待查",
        "party_join": "2003年6月",
        "work_start": "待查",
        "current_post": "阳明区政府副区长",
        "current_org": "牡丹江市阳明区人民政府",
        "source": "O-阳明区政府(202209/c03_342955.shtml)",
    },
    {
        "id": 11,
        "name": "谢军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "黑龙江省虎林市",
        "education": "待查",
        "party_join": "2002年12月",
        "work_start": "待查",
        "current_post": "阳明区政府副区长、阳明公安分局局长",
        "current_org": "牡丹江市阳明区人民政府",
        "source": "O-阳明区政府(202209/c03_342953.shtml)",
    },
    {
        "id": 12,
        "name": "郭景泉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "黑龙江省牡丹江市",
        "education": "待查",
        "party_join": "2000年",
        "work_start": "待查",
        "current_post": "阳明区政府副区长",
        "current_org": "牡丹江市阳明区人民政府",
        "source": "O-阳明区政府(202404/c03_923678.shtml)",
    },
    {
        "id": 13,
        "name": "李伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "黑龙江省牡丹江市",
        "education": "待查",
        "party_join": "1998年",
        "work_start": "待查",
        "current_post": "阳明区政府副区长、桦林镇党委书记兼桦橡街道党工委书记",
        "current_org": "牡丹江市阳明区人民政府",
        "source": "O-阳明区政府(202607/c03_1052446.shtml)",
    },
    # ── 人大常委会 ──
    {
        "id": 14,
        "name": "张世红",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "黑龙江省牡丹江市",
        "education": "待查",
        "party_join": "1994年9月",
        "work_start": "待查",
        "current_post": "阳明区人大常委会主任",
        "current_org": "牡丹江市阳明区人民代表大会常务委员会",
        "source": "O-阳明区人大(c102129/202109/c03_342944.shtml)",
    },
    {
        "id": 15,
        "name": "白云龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "黑龙江省林口县",
        "education": "待查",
        "party_join": "1995年7月",
        "work_start": "待查",
        "current_post": "阳明区人大常委会副主任、三级调研员",
        "current_org": "牡丹江市阳明区人民代表大会常务委员会",
        "source": "O-阳明区人大(c102129/202109/c03_342946.shtml)",
    },
    {
        "id": 16,
        "name": "李晶",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "黑龙江省牡丹江市",
        "education": "待查",
        "party_join": "无党派",
        "work_start": "待查",
        "current_post": "阳明区人大常委会副主任、三级调研员",
        "current_org": "牡丹江市阳明区人民代表大会常务委员会",
        "source": "O-阳明区人大(c102129/202404/c03_923679.shtml)",
    },
    {
        "id": 17,
        "name": "王春杰",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "黑龙江省绥阳",
        "education": "待查",
        "party_join": "1996年6月",
        "work_start": "待查",
        "current_post": "阳明区人大常委会副主任",
        "current_org": "牡丹江市阳明区人民代表大会常务委员会",
        "source": "O-阳明区人大(c102129/202110/c03_342947.shtml)",
    },
    {
        "id": 18,
        "name": "王丽娟",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "黑龙江省牡丹江市",
        "education": "待查",
        "party_join": "1992年6月",
        "work_start": "待查",
        "current_post": "阳明区人大常委会副主任",
        "current_org": "牡丹江市阳明区人民代表大会常务委员会",
        "source": "O-阳明区人大(c102129/202404/c03_923681.shtml)",
    },
    # ── 区政协 ──
    {
        "id": 19,
        "name": "吴龙海",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "黑龙江省牡丹江市",
        "education": "待查",
        "party_join": "1998年6月",
        "work_start": "待查",
        "current_post": "阳明区政协主席",
        "current_org": "政协牡丹江市阳明区委员会",
        "source": "O-阳明区政协(c102131/202109/c03_342964.shtml)",
    },
    {
        "id": 20,
        "name": "靳艳东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "黑龙江省穆棱市",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "阳明区政协副主席、二级调研员",
        "current_org": "政协牡丹江市阳明区委员会",
        "source": "O-阳明区政协(c102131/202109/c03_342966.shtml)",
    },
    {
        "id": 21,
        "name": "赵晶馥",
        "gender": "女",
        "ethnicity": "满族",
        "birth": "待查",
        "birthplace": "黑龙江省牡丹江市",
        "education": "待查",
        "party_join": "待查",
        "work_start": "待查",
        "current_post": "阳明区政协副主席、三级调研员",
        "current_org": "政协牡丹江市阳明区委员会",
        "source": "O-阳明区政协(c102131/202109/c03_342968.shtml)",
    },
    {
        "id": 22,
        "name": "刘辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "黑龙江省牡丹江市",
        "education": "待查",
        "party_join": "1990年11月",
        "work_start": "待查",
        "current_post": "阳明区政协副主席",
        "current_org": "政协牡丹江市阳明区委员会",
        "source": "O-阳明区政协(c102131/202109/c03_342971.shtml)",
    },
]

# ══════════════════════════════════════════════════════════════
# 机构 (organizations)
# ══════════════════════════════════════════════════════════════
organizations = [
    {"id": 1, "name": "中共牡丹江市阳明区委员会", "type": "党委", "level": "县处级", "parent": "中共牡丹江市委", "location": "黑龙江省牡丹江市阳明区"},
    {"id": 2, "name": "牡丹江市阳明区人民政府", "type": "政府", "level": "县处级", "parent": "牡丹江市人民政府", "location": "黑龙江省牡丹江市阳明区"},
    {"id": 3, "name": "中共牡丹江市阳明区纪律检查委员会", "type": "纪委", "level": "县处级", "parent": "中共牡丹江市阳明区委员会", "location": "黑龙江省牡丹江市阳明区"},
    {"id": 4, "name": "牡丹江市阳明区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "牡丹江市人民代表大会常务委员会", "location": "黑龙江省牡丹江市阳明区"},
    {"id": 5, "name": "政协牡丹江市阳明区委员会", "type": "政协", "level": "县处级", "parent": "政协牡丹江市委员会", "location": "黑龙江省牡丹江市阳明区"},
    {"id": 6, "name": "牡丹江市阳明区人民武装部", "type": "军队", "level": "县处级", "parent": "中国人民解放军黑龙江省牡丹江军分区", "location": "黑龙江省牡丹江市阳明区"},
    {"id": 7, "name": "牡丹江市公安局阳明分局", "type": "政法", "level": "乡镇级", "parent": "牡丹江市公安局", "location": "黑龙江省牡丹江市阳明区"},
    {"id": 8, "name": "中共牡丹江市阳明区铁岭镇委员会", "type": "党委", "level": "乡镇级", "parent": "中共牡丹江市阳明区委员会", "location": "黑龙江省牡丹江市阳明区铁岭镇"},
    {"id": 9, "name": "中共牡丹江市阳明区五林镇委员会", "type": "党委", "level": "乡镇级", "parent": "中共牡丹江市阳明区委员会", "location": "黑龙江省牡丹江市阳明区五林镇"},
    {"id": 10, "name": "中共牡丹江市阳明区桦林镇委员会", "type": "党委", "level": "乡镇级", "parent": "中共牡丹江市阳明区委员会", "location": "黑龙江省牡丹江市阳明区桦林镇"},
]

# ══════════════════════════════════════════════════════════════
# 任职 (positions)
# ══════════════════════════════════════════════════════════════
positions = [
    # 区委书记 孙传宝 (1)
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "待查", "end_date": "present", "rank": "县处级正职", "note": "一级调研员;官方领导之窗首页第一"},
    # 区长/副书记 葛建军 (2)
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "待查", "end_date": "present", "rank": "县处级正职", "note": "官方‘区委副书记、区长’"},
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 常委 陈兆中 (3)
    {"person_id": 3, "org_id": 1, "title": "区委常委、纪委书记", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "兼监委主任"},
    {"person_id": 3, "org_id": 3, "title": "区纪委书记、监委主任", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "三级高级监察官"},
    # 常委 邵宗杰 (4)
    {"person_id": 4, "org_id": 1, "title": "区委常委、组织部部长、统战部部长", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "兼区政协党组副书记"},
    # 常委 王鹏 (5)
    {"person_id": 5, "org_id": 6, "title": "区委常委、武装部部长", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 常委兼副区长 赵双美 (6)
    {"person_id": 6, "org_id": 1, "title": "区委常委", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "政府副区长(常务)", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    # 常委 葛岩松 (7)
    {"person_id": 7, "org_id": 1, "title": "区委常委", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 7, "org_id": 8, "title": "铁岭镇党委书记", "start_date": "待查", "end_date": "present", "rank": "乡科级正职", "note": ""},
    # 常委 周庆婉 (8)
    {"person_id": 8, "org_id": 1, "title": "区委常委、宣传部部长", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "兼五林镇党委书记"},
    {"person_id": 8, "org_id": 9, "title": "五林镇党委书记", "start_date": "待查", "end_date": "present", "rank": "乡科级正职", "note": ""},
    # 副区长
    {"person_id": 9, "org_id": 2, "title": "政府副区长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": "女,长春人"},
    {"person_id": 10, "org_id": 2, "title": "政府副区长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "政府副区长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 11, "org_id": 7, "title": "阳明公安分局局长", "start_date": "待查", "end_date": "present", "rank": "乡镇级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "政府副区长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "政府副区长", "start_date": "待查", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 13, "org_id": 10, "title": "桦林镇党委书记兼桦橡街道党工委书记", "start_date": "待查", "end_date": "present", "rank": "乡科级正职", "note": ""},
    # 人大
    {"person_id": 14, "org_id": 4, "title": "人大常委会主任", "start_date": "待查", "end_date": "present", "rank": "县处级正职", "note": ""},
    {"person_id": 15, "org_id": 4, "title": "人大常委会副主任", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "三级调研员"},
    {"person_id": 16, "org_id": 4, "title": "人大常委会副主任", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "无党派,三级调研员"},
    {"person_id": 17, "org_id": 4, "title": "人大常委会副主任", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": ""},
    {"person_id": 18, "org_id": 4, "title": "人大常委会副主任", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 政协
    {"person_id": 19, "org_id": 5, "title": "政协主席", "start_date": "待查", "end_date": "present", "rank": "县处级正职", "note": ""},
    {"person_id": 20, "org_id": 5, "title": "政协副主席", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "二级调研员"},
    {"person_id": 21, "org_id": 5, "title": "政协副主席", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": "满族,三级调研员"},
    {"person_id": 22, "org_id": 5, "title": "政协副主席", "start_date": "待查", "end_date": "present", "rank": "县处级副职", "note": ""},
]

# ══════════════════════════════════════════════════════════════
# 关系 (relationships)
# ══════════════════════════════════════════════════════════════
relationships = [
    {"person_a": 1, "person_b": 2, "type": "党政搭班子", "context": "孙传宝书记—葛建军区长共同领导阳明区", "overlap_org": "阳明区四套班子", "overlap_period": "present"},
    {"person_a": 1, "person_b": 3, "type": "班子成员", "context": "区委书记-区纪委书记同班子", "overlap_org": "中共阳明区委", "overlap_period": "present"},
    {"person_a": 1, "person_b": 4, "type": "班子成员", "context": "区委书记-组织部长同班子", "overlap_org": "中共阳明区委", "overlap_period": "present"},
    {"person_a": 1, "person_b": 5, "type": "班子成员", "context": "区委书记-武装部长同班子", "overlap_org": "中共阳明区委", "overlap_period": "present"},
    {"person_a": 1, "person_b": 6, "type": "班子成员", "context": "区委书记-区委常委、副区长", "overlap_org": "中共阳明区委", "overlap_period": "present"},
    {"person_a": 1, "person_b": 7, "type": "班子成员", "context": "区委书记-区委常委(铁岭镇书记)", "overlap_org": "中共阳明区委", "overlap_period": "present"},
    {"person_a": 1, "person_b": 8, "type": "班子成员", "context": "区委书记-宣传部长", "overlap_org": "中共阳明区委", "overlap_period": "present"},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "区长-副区长(常务)", "overlap_org": "阳明区人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 9, "type": "上下级", "context": "区长-副区长", "overlap_org": "阳明区人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "区长-副区长", "overlap_org": "阳明区人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 11, "type": "上下级", "context": "区长-副区长(公安局长)", "overlap_org": "阳明区人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "区长-副区长", "overlap_org": "阳明区人民政府", "overlap_period": "present"},
    {"person_a": 2, "person_b": 13, "type": "上下级", "context": "区长-副区长(桦林镇书记)", "overlap_org": "阳明区人民政府", "overlap_period": "present"},
    {"person_a": 1, "person_b": 14, "type": "四套班子协同", "context": "区委书记-人大主任协同", "overlap_org": "阳明区四套班子", "overlap_period": "present"},
    {"person_a": 1, "person_b": 19, "type": "四套班子协同", "context": "区委书记-政协主席协同", "overlap_org": "阳明区四套班子", "overlap_period": "present"},
    {"person_a": 4, "person_b": 19, "type": "党委政协交叉", "context": "邵宗杰兼统战部长、区政协党组副书记,与政协主席工作交叉", "overlap_org": "阳明区政协", "overlap_period": "present", "strength": "medium"},
    {"person_a": 7, "person_b": 13, "type": "同岗序列", "context": "葛岩松(铁岭镇党委书记)、李伟(桦林镇党委书记)同为乡镇党委书记进区委/区府", "overlap_org": "阳明区乡镇党委", "overlap_period": "present", "strength": "weak"},
    {"person_a": 2, "person_b": 4, "type": "同乡", "context": "葛建军、邵宗杰皆出生于牡丹江市", "overlap_org": "牡丹江市", "overlap_period": "", "strength": "weak"},
    {"person_a": 2, "person_b": 10, "type": "同乡", "context": "葛建军、任智锋皆出生于牡丹江市", "overlap_org": "牡丹江市", "overlap_period": "", "strength": "weak"},
    {"person_a": 1, "person_b": 3, "type": "同期入党", "context": "孙传宝、陈兆中皆2000年6月入党", "overlap_org": "中国共产党", "overlap_period": "2000-06", "strength": "weak"},
    {"person_a": 2, "person_b": 3, "type": "同期入党", "context": "葛建军、陈兆中皆2000年6月入党", "overlap_org": "中国共产党", "overlap_period": "2000-06", "strength": "weak"},
]


def main() -> None:
    run_build(
        slug="阳明区",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    conn = sqlite3.connect(str(DB_PATH))
    for t in ("persons", "organizations", "positions", "relationships"):
        n = conn.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        print(f"{t}: {n}")
    conn.close()


if __name__ == "__main__":
    main()