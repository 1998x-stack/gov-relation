#!/usr/bin/env python3
"""
阆中市 (Langzhong City, Nanchong City, Sichuan Province)
领导班子工作关系网络 — 数据构建脚本

调查日期: 2026-07-26
信息来源:
  - 阆中市人民政府网站 (langzhong.gov.cn): 市长及8位副市长的官方简历、领导分工
  - 中共阆中市委十四届十一次全会公报 (2026-07-14): 确认杨德宇为市委书记
"""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../.."))

from gov_relation.runner import run_build

TODAY = "2026-07-26"
SLUG = "阆中市"
PROVINCE = "四川省"
PARENT_CITY = "南充市"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "阆中市_network.db")
GEXF_PATH = os.path.join(SCRIPT_DIR, "阆中市_network.gexf")

# ═══════════════════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════════════════

persons = [
    {
        "id": 1,
        "name": "杨德宇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共阆中市委员会",
        "source": "https://www.langzhong.gov.cn/xwdt/tttj/202607/t20260717_2347947.html",
    },
    {
        "id": 2,
        "name": "唐硕",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年12月",
        "birthplace": "四川南充",
        "education": "西华师范大学公共事业管理，大学学历",
        "party_join": "2005年6月",
        "work_start": "1999年8月",
        "current_post": "市委副书记、市长",
        "current_org": "阆中市人民政府",
        "source": "https://www.langzhong.gov.cn/zwgk/fdzdgknr/jgzn/ldxx/sz/ts/202204/t20220401_600010.html",
    },
    {
        "id": 3,
        "name": "张小林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年5月",
        "birthplace": "四川营山",
        "education": "四川师范大学汉语言文学专业，大学学历",
        "party_join": "1999年6月",
        "work_start": "2000年8月",
        "current_post": "市委常委、副市长（常务）",
        "current_org": "阆中市人民政府",
        "source": "https://www.langzhong.gov.cn/zwgk/fdzdgknr/jgzn/ldxx/fsz/zxl/202604/t20260422_2327917.html",
    },
    {
        "id": 4,
        "name": "李新建",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年11月",
        "birthplace": "浙江仙居",
        "education": "硕士，高级经济师",
        "party_join": "2001年5月",
        "work_start": "2002年8月",
        "current_post": "市委常委、副市长（挂职）",
        "current_org": "阆中市人民政府",
        "source": "https://www.langzhong.gov.cn/zwgk/fdzdgknr/jgzn/ldxx/fsz/lxj/202408/t20240801_2000564.html",
    },
    {
        "id": 5,
        "name": "杜小兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年9月",
        "birthplace": "四川南部",
        "education": "四川省委党校法律专业，大学学历",
        "party_join": "1996年12月",
        "work_start": "1991年8月",
        "current_post": "副市长、市公安局局长",
        "current_org": "阆中市人民政府",
        "source": "https://www.langzhong.gov.cn/zwgk/fdzdgknr/jgzn/ldxx/fsz/dxb/202204/t20220401_601071.html",
    },
    {
        "id": 6,
        "name": "杜敏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年6月",
        "birthplace": "四川阆中",
        "education": "四川师范大学应用化学专业，大学学历",
        "party_join": "1999年4月",
        "work_start": "1998年2月",
        "current_post": "副市长",
        "current_org": "阆中市人民政府",
        "source": "https://www.langzhong.gov.cn/zwgk/fdzdgknr/jgzn/ldxx/fsz/dm/202502/t20250217_2092426.html",
    },
    {
        "id": 7,
        "name": "杨劲松",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年3月",
        "birthplace": "四川阆中",
        "education": "四川大学法律专业，大学学历",
        "party_join": "2000年5月",
        "work_start": "2001年9月",
        "current_post": "副市长",
        "current_org": "阆中市人民政府",
        "source": "https://www.langzhong.gov.cn/zwgk/fdzdgknr/jgzn/ldxx/fsz/yjs/202204/t20220401_601457.html",
    },
    {
        "id": 8,
        "name": "张松",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年7月",
        "birthplace": "四川阆中",
        "education": "四川师范大学汉语言文学专业，大学学历",
        "party_join": "2002年7月",
        "work_start": "2000年9月",
        "current_post": "副市长",
        "current_org": "阆中市人民政府",
        "source": "https://www.langzhong.gov.cn/zwgk/fdzdgknr/jgzn/ldxx/fsz/zsld/202204/t20220401_601585.html",
    },
    {
        "id": 9,
        "name": "邓雁城",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年4月",
        "birthplace": "河南延津",
        "education": "山东大学数学与应用数学专业，硕士",
        "party_join": "",
        "work_start": "2000年7月",
        "current_post": "副市长（挂职）",
        "current_org": "阆中市人民政府",
        "source": "https://www.langzhong.gov.cn/zwgk/fdzdgknr/jgzn/ldxx/fsz/dyc/202510/t20251022_2274722.html",
    },
    {
        "id": 10,
        "name": "何姝睿",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1988年1月",
        "birthplace": "四川营山",
        "education": "西华师范大学公共管理专业，硕士",
        "party_join": "",
        "work_start": "2011年5月",
        "current_post": "副市长",
        "current_org": "阆中市人民政府",
        "source": "https://www.langzhong.gov.cn/zwgk/fdzdgknr/jyly/fsz/hdr/202510/t20251022_2274730.html",
    },
]

organizations = [
    {"id": 1, "name": "中共阆中市委员会", "type": "党委", "level": "县级", "location": "四川省南充市阆中市"},
    {"id": 2, "name": "阆中市人民政府", "type": "政府", "level": "县级", "location": "四川省南充市阆中市"},
    {"id": 3, "name": "阆中市公安局", "type": "政府", "level": "县级", "location": "四川省南充市阆中市"},
    {"id": 4, "name": "南充市人民政府", "type": "政府", "level": "地市级", "location": "四川省南充市"},
]

positions = [
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start": "", "end": "至今", "rank": "正县级", "note": "任职起始时间待查"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start": "", "end": "至今", "rank": "副县级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "市长、党组书记", "start": "", "end": "至今", "rank": "正县级", "note": ""},
    {"person_id": 3, "org_id": 1, "title": "市委常委", "start": "", "end": "至今", "rank": "副县级", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "副市长（常务）、党组副书记", "start": "", "end": "至今", "rank": "副县级", "note": ""},
    {"person_id": 4, "org_id": 4, "title": "南充市政府副秘书长", "start": "", "end": "至今", "rank": "正县级", "note": "挂职前职务"},
    {"person_id": 4, "org_id": 1, "title": "市委常委（挂职）", "start": "2024-08", "end": "至今", "rank": "副县级", "note": "东西部协作，3年期"},
    {"person_id": 4, "org_id": 2, "title": "副市长（挂职）", "start": "2024-08", "end": "至今", "rank": "副县级", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "副市长、党组成员", "start": "", "end": "至今", "rank": "副县级", "note": ""},
    {"person_id": 5, "org_id": 3, "title": "市公安局局长、党委书记", "start": "", "end": "至今", "rank": "正科级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副市长、党组成员", "start": "", "end": "至今", "rank": "副县级", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "副市长、党组成员", "start": "", "end": "至今", "rank": "副县级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "副市长、党组成员", "start": "", "end": "至今", "rank": "副县级", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副市长（挂职）", "start": "2025-10", "end": "至今", "rank": "副县级", "note": "中国电子集团对口帮扶，2年期"},
    {"person_id": 10, "org_id": 2, "title": "副市长", "start": "", "end": "至今", "rank": "副县级", "note": "请假中"},
]

relationships = [
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "市委班子搭档", "overlap_org": "中共阆中市委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "市委常委班子成员", "overlap_org": "中共阆中市委员会", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "市委常委班子（挂职）", "overlap_org": "中共阆中市委员会", "overlap_period": "2024-至今"},
    {"person_a": 2, "person_b": 3, "type": "superior_subordinate", "context": "市长与常务副市长", "overlap_org": "阆中市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 4, "type": "superior_subordinate", "context": "市长与挂职副市长", "overlap_org": "阆中市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 5, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "阆中市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 6, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "阆中市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 7, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "阆中市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 8, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "阆中市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 9, "type": "superior_subordinate", "context": "市长与挂职副市长", "overlap_org": "阆中市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 10, "type": "superior_subordinate", "context": "市长与副市长", "overlap_org": "阆中市人民政府", "overlap_period": "至今"},
    {"person_a": 3, "person_b": 5, "type": "overlap", "context": "市政府AB角", "overlap_org": "阆中市人民政府", "overlap_period": "至今"},
    {"person_a": 4, "person_b": 7, "type": "overlap", "context": "市政府AB角", "overlap_org": "阆中市人民政府", "overlap_period": "至今"},
    {"person_a": 6, "person_b": 8, "type": "overlap", "context": "市政府AB角", "overlap_org": "阆中市人民政府", "overlap_period": "至今"},
    {"person_a": 3, "person_b": 10, "type": "same_native_place", "context": "同为四川营山籍", "overlap_org": "", "overlap_period": ""},
    {"person_a": 4, "person_b": 9, "type": "same_system", "context": "均为外省在阆中挂职干部", "overlap_org": "阆中市人民政府", "overlap_period": "2025-至今"},
    {"person_a": 6, "person_b": 7, "type": "same_native_place", "context": "同为四川阆中籍", "overlap_org": "", "overlap_period": ""},
    {"person_a": 6, "person_b": 8, "type": "same_native_place", "context": "同为四川阆中籍", "overlap_org": "", "overlap_period": ""},
    {"person_a": 7, "person_b": 8, "type": "same_native_place", "context": "同为四川阆中籍", "overlap_org": "", "overlap_period": ""},
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