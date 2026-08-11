#!/usr/bin/env python3
"""印台区领导班子关系网络生成脚本。

铜川市印台区领导团队：区委书记龚颖、区长马海峰。
数据来源：印台区政府官网 (www.yintai.gov.cn)、百度百科、新闻报道。
信息截止日期：2026年7月。
"""

import sys
from pathlib import Path

# Ensure gov_relation package is importable
_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build

SLUG = "印台区"
THIS_DIR = Path(__file__).resolve().parent
DB_PATH = THIS_DIR / f"{SLUG}_network.db"
GEXF_PATH = THIS_DIR / f"{SLUG}_network.gexf"

import sqlite3  # noqa: used by validator

# ── 人员 ──────────────────────────────────────────────────────────
persons = [
    {
        "id": 1,
        "name": "龚颖",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1981年4月",
        "birthplace": "",
        "education": "省委党校研究生学历",
        "party_join": "",
        "work_start": "",
        "current_post": "区委书记、区人武部党委第一书记",
        "current_org": "中共铜川市印台区委员会",
        "source": "印台区政府官网, 百度百科",
    },
    {
        "id": 2,
        "name": "马海峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年10月",
        "birthplace": "陕西西安",
        "education": "大学学历",
        "party_join": "2002年12月",
        "work_start": "2003年7月",
        "current_post": "区委副书记、区长",
        "current_org": "铜川市印台区人民政府",
        "source": "印台区政府官网, 百度百科",
    },
    {
        "id": 3,
        "name": "朱伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委副书记",
        "current_org": "中共铜川市印台区委员会",
        "source": "百度百科",
    },
    {
        "id": 4,
        "name": "刘先",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委副书记",
        "current_org": "中共铜川市印台区委员会",
        "source": "印台区政府官网, 印台党建网",
    },
    {
        "id": 5,
        "name": "薛新华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "铜川市印台区人民政府",
        "source": "印台区政府官网",
    },
    {
        "id": 6,
        "name": "杨勇武",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、区人武部上校政治委员",
        "current_org": "铜川市印台区人民武装部",
        "source": "百度百科",
    },
    {
        "id": 7,
        "name": "梁东",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共铜川市印台区委员会",
        "source": "百度百科",
    },
    {
        "id": 8,
        "name": "罗星智",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、组织部部长",
        "current_org": "中共铜川市印台区委员会",
        "source": "印台党建网",
    },
    {
        "id": 9,
        "name": "窦凯",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、区纪委书记、区监委主任",
        "current_org": "中共铜川市印台区纪律检查委员会",
        "source": "印台区纪委监委网站",
    },
    {
        "id": 10,
        "name": "丁冲",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委",
        "current_org": "中共铜川市印台区委员会",
        "source": "印台区政府官网",
    },
    {
        "id": 11,
        "name": "肖忠宏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、政法委书记",
        "current_org": "中共铜川市印台区委员会",
        "source": "澎湃新闻",
    },
    {
        "id": 12,
        "name": "刘涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "铜川市印台区人民政府",
        "source": "印台区政府官网, 同花顺财经",
    },
    {
        "id": 13,
        "name": "李亚莉",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1970年11月",
        "birthplace": "陕西长武",
        "education": "大学学历",
        "party_join": "1996年6月",
        "work_start": "1992年12月",
        "current_post": "铜川市人民政府副市长",
        "current_org": "铜川市人民政府",
        "source": "百度百科",
    },
]

# ── 组织 ──────────────────────────────────────────────────────────
organizations = [
    {
        "id": 1,
        "name": "中共铜川市印台区委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共铜川市委员会",
        "location": "陕西省铜川市印台区",
    },
    {
        "id": 2,
        "name": "铜川市印台区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "铜川市人民政府",
        "location": "陕西省铜川市印台区",
    },
    {
        "id": 3,
        "name": "铜川市印台区人民武装部",
        "type": "事业单位",
        "level": "县处级",
        "parent": "铜川军分区",
        "location": "陕西省铜川市印台区",
    },
    {
        "id": 4,
        "name": "中共铜川市印台区纪律检查委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共铜川市纪律检查委员会",
        "location": "陕西省铜川市印台区",
    },
    {
        "id": 5,
        "name": "铜川市人民政府",
        "type": "政府",
        "level": "地厅级",
        "parent": "陕西省人民政府",
        "location": "陕西省铜川市",
    },
    {
        "id": 6,
        "name": "中共紫阳县委员会",
        "type": "党委",
        "level": "县处级",
        "parent": "中共安康市委员会",
        "location": "陕西省安康市紫阳县",
    },
    {
        "id": 7,
        "name": "中共白河县委员会/白河县人民政府",
        "type": "党委",
        "level": "县处级",
        "parent": "中共安康市委员会",
        "location": "陕西省安康市白河县",
    },
]

# ── 任职记录 ──────────────────────────────────────────────────────
positions = [
    # 龚颖
    {"person_id": 1, "org_id": 6, "title": "紫阳县委常委、统战部部长", "start_date": "", "end_date": "", "rank": "", "note": "履历来源：百度百科"},
    {"person_id": 1, "org_id": 7, "title": "白河县委常委、县政府党组副书记、副县长", "start_date": "", "end_date": "", "rank": "", "note": "履历来源：百度百科"},
    {"person_id": 1, "org_id": 7, "title": "白河县委副书记、县政府党组书记、代县长", "start_date": "", "end_date": "", "rank": "", "note": "履历来源：百度百科"},
    {"person_id": 1, "org_id": 7, "title": "白河县委副书记、县长", "start_date": "", "end_date": "2026年4月", "rank": "县处级正职", "note": ""},
    {"person_id": 1, "org_id": 1, "title": "区委书记、区人武部党委第一书记", "start_date": "2026年5月", "end_date": "至今", "rank": "县处级正职", "note": "2026年4月拟进一步使用公示，5月正式到任"},
    # 马海峰
    {"person_id": 2, "org_id": 2, "title": "印台区委副书记、区长", "start_date": "2021年", "end_date": "至今", "rank": "县处级正职", "note": "与李亚莉搭班子，后与龚颖搭班子"},
    # 朱伟
    {"person_id": 3, "org_id": 1, "title": "区委副书记", "start_date": "2021年", "end_date": "至今", "rank": "县处级副职", "note": "2021年9月十一届一次全会当选"},
    # 刘先
    {"person_id": 4, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": "2026年新闻中出现"},
    # 薛新华
    {"person_id": 5, "org_id": 2, "title": "区委常委、常务副区长", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": "2026年多次新闻中出现"},
    # 杨勇武
    {"person_id": 6, "org_id": 3, "title": "区委常委、区人武部上校政治委员", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": "百度百科"},
    # 梁东
    {"person_id": 7, "org_id": 1, "title": "区委常委", "start_date": "2021年", "end_date": "至今", "rank": "县处级副职", "note": "2021年9月十一届一次全会当选"},
    # 罗星智
    {"person_id": 8, "org_id": 1, "title": "区委常委、组织部部长", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": "2026年7月新闻中出现"},
    # 窦凯
    {"person_id": 9, "org_id": 4, "title": "区委常委、区纪委书记、区监委主任", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": "2026年3月新闻中出现"},
    # 丁冲
    {"person_id": 10, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": "2026年新闻中出现"},
    # 肖忠宏
    {"person_id": 11, "org_id": 1, "title": "区委常委、政法委书记", "start_date": "", "end_date": "", "rank": "县处级副职", "note": "2023年6月新闻中出现，当前任职状态待确认"},
    # 刘涛
    {"person_id": 12, "org_id": 2, "title": "区委常委、副区长", "start_date": "", "end_date": "至今", "rank": "县处级副职", "note": "2026年6月新闻中出现"},
    # 李亚莉（前任区委书记）
    {"person_id": 13, "org_id": 2, "title": "印台区委副书记、区长", "start_date": "2016年2月", "end_date": "2021年6月", "rank": "县处级正职", "note": ""},
    {"person_id": 13, "org_id": 1, "title": "印台区委书记", "start_date": "2021年6月", "end_date": "2026年6月", "rank": "县处级正职", "note": ""},
    {"person_id": 13, "org_id": 5, "title": "铜川市人民政府副市长", "start_date": "2026年6月", "end_date": "至今", "rank": "副厅级", "note": "2026年6月25日铜川市第十七届人大常委会任命"},
]

# ── 关系 ──────────────────────────────────────────────────────────
relationships = [
    # 区委书记-区长搭班子
    {
        "person_a": 1, "person_b": 2,
        "type": "superior_subordinate",
        "context": "区委书记—区长搭班子",
        "overlap_org": "中共铜川市印台区委员会/铜川市印台区人民政府",
        "overlap_period": "2026年5月至今",
    },
    # 前任区委书记与现任区长（曾搭班子）
    {
        "person_a": 13, "person_b": 2,
        "type": "superior_subordinate",
        "context": "前任区委书记—区长搭班子",
        "overlap_org": "中共铜川市印台区委员会/铜川市印台区人民政府",
        "overlap_period": "2021年至2026年5月",
    },
    # 区委书记与副书记
    {
        "person_a": 1, "person_b": 3,
        "type": "superior_subordinate",
        "context": "区委书记—区委副书记",
        "overlap_org": "中共铜川市印台区委员会",
        "overlap_period": "2026年5月至今",
    },
    {
        "person_a": 1, "person_b": 4,
        "type": "superior_subordinate",
        "context": "区委书记—区委副书记",
        "overlap_org": "中共铜川市印台区委员会",
        "overlap_period": "2026年至今",
    },
    # 区长与常务副区长
    {
        "person_a": 2, "person_b": 5,
        "type": "superior_subordinate",
        "context": "区长—常务副区长",
        "overlap_org": "铜川市印台区人民政府",
        "overlap_period": "",
    },
    # 区委常委班子共事关系
    {
        "person_a": 1, "person_b": 5,
        "type": "overlap",
        "context": "区委常委班子共事",
        "overlap_org": "中共铜川市印台区委员会",
        "overlap_period": "2026年至今",
    },
    {
        "person_a": 1, "person_b": 6,
        "type": "overlap",
        "context": "区委常委班子共事",
        "overlap_org": "中共铜川市印台区委员会",
        "overlap_period": "2026年至今",
    },
    {
        "person_a": 1, "person_b": 7,
        "type": "overlap",
        "context": "区委常委班子共事",
        "overlap_org": "中共铜川市印台区委员会",
        "overlap_period": "2026年至今",
    },
    {
        "person_a": 1, "person_b": 8,
        "type": "overlap",
        "context": "区委常委班子共事",
        "overlap_org": "中共铜川市印台区委员会",
        "overlap_period": "2026年至今",
    },
    {
        "person_a": 1, "person_b": 9,
        "type": "overlap",
        "context": "区委常委班子共事",
        "overlap_org": "中共铜川市印台区委员会",
        "overlap_period": "2026年至今",
    },
    {
        "person_a": 1, "person_b": 10,
        "type": "overlap",
        "context": "区委常委班子共事",
        "overlap_org": "中共铜川市印台区委员会",
        "overlap_period": "2026年至今",
    },
    {
        "person_a": 1, "person_b": 11,
        "type": "overlap",
        "context": "区委常委班子共事（可能）",
        "overlap_org": "中共铜川市印台区委员会",
        "overlap_period": "",
    },
    {
        "person_a": 1, "person_b": 12,
        "type": "overlap",
        "context": "区委常委班子共事",
        "overlap_org": "中共铜川市印台区委员会",
        "overlap_period": "2026年至今",
    },
    # 常务副区长与副区长
    {
        "person_a": 5, "person_b": 12,
        "type": "overlap",
        "context": "常务副区长—副区长共事",
        "overlap_org": "铜川市印台区人民政府",
        "overlap_period": "",
    },
    # 前任与现任区委书记交接
    {
        "person_a": 13, "person_b": 1,
        "type": "predecessor_successor",
        "context": "前任区委书记交接到现任区委书记",
        "overlap_org": "中共铜川市印台区委员会",
        "overlap_period": "2026年5-6月",
    },
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
    )
    print(f"✅ {SLUG} 数据构建完成")
    print(f"   DB:   {DB_PATH}")
    print(f"   GEXF: {GEXF_PATH}")
