#!/usr/bin/env python3
"""
志丹县领导班子工作关系网络数据生成脚本

数据来源：志丹县人民政府官方网站 (www.zhidan.gov.cn)、志丹融媒新闻报道
生成日期：2026-07-25
"""

import sys
sys.path.insert(0, '.')

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

slug = "志丹县"

persons = [
    # ===== 县委领导班子 =====
    {
        "id": "zhidan_li_yongjun",
        "name": "李永军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委书记",
        "current_org": "中共志丹县委员会",
        "source": "https://www.zhidan.gov.cn/xwzx/hdyw/2075465065605107713.html"
    },
    {
        "id": "zhidan_liu_xiaojun",
        "name": "刘晓军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979-10",
        "birthplace": "",
        "education": "经济管理学研究生/理学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记、县长",
        "current_org": "志丹县人民政府",
        "source": "https://www.zhidan.gov.cn/zfxxgk/fdzdgknr/zfld/xc/lxj/grjl/1922830736117903361.html"
    },
    {
        "id": "zhidan_feng_xiangbin",
        "name": "冯向斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委副书记",
        "current_org": "中共志丹县委员会",
        "source": "https://www.zhidan.gov.cn/xwzx/hdyw/2075465065605107713.html"
    },
    {
        "id": "zhidan_ye_erao",
        "name": "叶二凹",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982-06",
        "birthplace": "",
        "education": "本科/历史学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、常务副县长",
        "current_org": "志丹县人民政府",
        "source": "https://www.zhidan.gov.cn/zfxxgk/fdzdgknr/zfld/cwfxc/yea/grjl/1988518976979787777.html"
    },
    {
        "id": "zhidan_zhao_wei",
        "name": "赵伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972-08",
        "birthplace": "",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、副县长",
        "current_org": "志丹县人民政府",
        "source": "https://www.zhidan.gov.cn/zfxxgk/fdzdgknr/zfld/fxc/zw/grjl/1558278318590066689.html"
    },
    {
        "id": "zhidan_shi_zhenwen",
        "name": "石振文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县委常委、政法委书记",
        "current_org": "中共志丹县委员会",
        "source": "https://www.zhidan.gov.cn/xwzx/hdyw/2026189834766499841.html"
    },
    # ===== 县政府其他领导 =====
    {
        "id": "zhidan_li_mei",
        "name": "李梅",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1978-08",
        "birthplace": "",
        "education": "在职研究生",
        "party_join": "无党派",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "志丹县人民政府",
        "source": "https://www.zhidan.gov.cn/zfxxgk/fdzdgknr/zfld/fxc/lm/grjl/1558278810179276802.html"
    },
    {
        "id": "zhidan_yang_haidong",
        "name": "杨海东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-04",
        "birthplace": "",
        "education": "在职研究生",
        "party_join": "中共党员",
        "work_start": "1994-09",
        "current_post": "副县长",
        "current_org": "志丹县人民政府",
        "source": "https://www.zhidan.gov.cn/zfxxgk/fdzdgknr/zfld/fxc/yhd/grjl/1845741676623159297.html"
    },
    {
        "id": "zhidan_liang_wei",
        "name": "梁炜",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977-08",
        "birthplace": "陕西吴起",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长、公安局局长",
        "current_org": "志丹县人民政府",
        "source": "https://www.zhidan.gov.cn/zfxxgk/fdzdgknr/zfld/fxc/lw/grjl/1845742152638812161.html"
    },
    {
        "id": "zhidan_xie_chunrong",
        "name": "谢春荣",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976-11",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "志丹县人民政府",
        "source": "https://www.zhidan.gov.cn/zfxxgk/fdzdgknr/zfld/fxc/xcr/grjl/1922835897464823810.html"
    },
    {
        "id": "zhidan_liu_xiaoyong",
        "name": "刘小勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980-07",
        "birthplace": "",
        "education": "大学",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "志丹县人民政府",
        "source": "https://www.zhidan.gov.cn/zfxxgk/fdzdgknr/zfld/fxc/lxy/grjl/1922836344766304258.html"
    },
    {
        "id": "zhidan_hao_yudong",
        "name": "郝煜东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1990-08",
        "birthplace": "",
        "education": "研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副县长",
        "current_org": "志丹县人民政府",
        "source": "https://www.zhidan.gov.cn/zfxxgk/fdzdgknr/zfld/fxc/hyd/grjl/2074404080645767170.html"
    },
    # ===== 人大、政协领导 =====
    {
        "id": "zhidan_liu_jianzhong",
        "name": "刘建忠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县人大常委会主任",
        "current_org": "志丹县人大常委会",
        "source": "https://www.zhidan.gov.cn/xwzx/hdyw/2075465065605107713.html"
    },
    {
        "id": "zhidan_you_shuping",
        "name": "尤淑萍",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "志丹县人大常委会",
        "source": "https://www.zhidan.gov.cn/xwzx/hdyw/2080555074815475713.html"
    },
    {
        "id": "zhidan_li_hu",
        "name": "李虎",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县人大常委会副主任",
        "current_org": "志丹县人大常委会",
        "source": "https://www.zhidan.gov.cn/xwzx/hdyw/2052563445601046530.html"
    },
    {
        "id": "zhidan_bai_baoming",
        "name": "白保明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "县政协主席",
        "current_org": "政协志丹县委员会",
        "source": "https://www.zhidan.gov.cn/xwzx/hdyw/2075465065605107713.html"
    },
    {
        "id": "zhidan_wu_zhixin",
        "name": "吴志新",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "县政协副主席",
        "current_org": "政协志丹县委员会",
        "source": "https://www.zhidan.gov.cn/xwzx/hdyw/2052563445601046530.html"
    },
]

organizations = [
    {"id": "zhidan_county_committee", "name": "中共志丹县委员会", "type": "县委", "level": "县", "parent": "延安市委"},
    {"id": "zhidan_county_gov", "name": "志丹县人民政府", "type": "政府", "level": "县", "parent": "延安市政府"},
    {"id": "zhidan_npc", "name": "志丹县人大常委会", "type": "人大", "level": "县", "parent": ""},
    {"id": "zhidan_cppcc", "name": "政协志丹县委员会", "type": "政协", "level": "县", "parent": ""},
    {"id": "zhidan_psb", "name": "志丹县公安局", "type": "政府部门", "level": "县", "parent": "志丹县人民政府"},
]

positions = [
    # 县委
    {"person_id": "zhidan_li_yongjun", "org_id": "zhidan_county_committee", "title": "县委书记", "start": "", "end": "", "rank": "1", "note": ""},
    {"person_id": "zhidan_liu_xiaojun", "org_id": "zhidan_county_committee", "title": "县委副书记", "start": "", "end": "", "rank": "2", "note": ""},
    {"person_id": "zhidan_liu_xiaojun", "org_id": "zhidan_county_gov", "title": "县长", "start": "", "end": "", "rank": "1", "note": "主持县政府全面工作"},
    {"person_id": "zhidan_feng_xiangbin", "org_id": "zhidan_county_committee", "title": "县委副书记", "start": "", "end": "", "rank": "3", "note": ""},
    {"person_id": "zhidan_ye_erao", "org_id": "zhidan_county_committee", "title": "县委常委", "start": "", "end": "", "rank": "4", "note": ""},
    {"person_id": "zhidan_ye_erao", "org_id": "zhidan_county_gov", "title": "常务副县长", "start": "", "end": "", "rank": "2", "note": "负责县政府常务工作"},
    {"person_id": "zhidan_zhao_wei", "org_id": "zhidan_county_committee", "title": "县委常委", "start": "", "end": "", "rank": "5", "note": ""},
    {"person_id": "zhidan_zhao_wei", "org_id": "zhidan_county_gov", "title": "副县长", "start": "", "end": "", "rank": "3", "note": "负责油气、自然资源、生态环境"},
    {"person_id": "zhidan_shi_zhenwen", "org_id": "zhidan_county_committee", "title": "县委常委、政法委书记", "start": "", "end": "", "rank": "6", "note": ""},
    # 县政府
    {"person_id": "zhidan_li_mei", "org_id": "zhidan_county_gov", "title": "副县长", "start": "", "end": "", "rank": "4", "note": "负责人社、文旅、民政"},
    {"person_id": "zhidan_yang_haidong", "org_id": "zhidan_county_gov", "title": "副县长", "start": "", "end": "", "rank": "5", "note": "负责教育、住建、城管"},
    {"person_id": "zhidan_liang_wei", "org_id": "zhidan_county_gov", "title": "副县长", "start": "", "end": "", "rank": "6", "note": "负责公安、司法、退役军人"},
    {"person_id": "zhidan_liang_wei", "org_id": "zhidan_psb", "title": "局长", "start": "", "end": "", "rank": "1", "note": ""},
    {"person_id": "zhidan_xie_chunrong", "org_id": "zhidan_county_gov", "title": "副县长", "start": "", "end": "", "rank": "7", "note": "负责交通、卫健、医保"},
    {"person_id": "zhidan_liu_xiaoyong", "org_id": "zhidan_county_gov", "title": "副县长", "start": "", "end": "", "rank": "8", "note": "负责农业农村、乡村振兴"},
    {"person_id": "zhidan_hao_yudong", "org_id": "zhidan_county_gov", "title": "副县长", "start": "", "end": "", "rank": "9", "note": "负责市场监管、招商引资"},
    # 人大、政协
    {"person_id": "zhidan_liu_jianzhong", "org_id": "zhidan_npc", "title": "主任", "start": "", "end": "", "rank": "1", "note": ""},
    {"person_id": "zhidan_you_shuping", "org_id": "zhidan_npc", "title": "副主任", "start": "", "end": "", "rank": "2", "note": ""},
    {"person_id": "zhidan_li_hu", "org_id": "zhidan_npc", "title": "副主任", "start": "", "end": "", "rank": "3", "note": ""},
    {"person_id": "zhidan_bai_baoming", "org_id": "zhidan_cppcc", "title": "主席", "start": "", "end": "", "rank": "1", "note": ""},
    {"person_id": "zhidan_wu_zhixin", "org_id": "zhidan_cppcc", "title": "副主席", "start": "", "end": "", "rank": "2", "note": ""},
]

relationships = [
    {"person_a": "zhidan_li_yongjun", "person_b": "zhidan_liu_xiaojun", "type": "党政搭档", "context": "县委书记与县长", "overlap_org": "中共志丹县委员会", "overlap_period": ""},
    {"person_a": "zhidan_liu_xiaojun", "person_b": "zhidan_ye_erao", "type": "上下级", "context": "县长与常务副县长（县政府党组正副书记）", "overlap_org": "志丹县人民政府", "overlap_period": ""},
    {"person_a": "zhidan_liu_xiaojun", "person_b": "zhidan_zhao_wei", "type": "上下级", "context": "县长与副县长（县政府党组成员）", "overlap_org": "志丹县人民政府", "overlap_period": ""},
    {"person_a": "zhidan_liu_xiaojun", "person_b": "zhidan_li_mei", "type": "上下级", "context": "县长与副县长", "overlap_org": "志丹县人民政府", "overlap_period": ""},
    {"person_a": "zhidan_liu_xiaojun", "person_b": "zhidan_yang_haidong", "type": "上下级", "context": "县长与副县长（党组成员）", "overlap_org": "志丹县人民政府", "overlap_period": ""},
    {"person_a": "zhidan_liu_xiaojun", "person_b": "zhidan_liang_wei", "type": "上下级", "context": "县长与副县长（党组成员）", "overlap_org": "志丹县人民政府", "overlap_period": ""},
    {"person_a": "zhidan_liu_xiaojun", "person_b": "zhidan_xie_chunrong", "type": "上下级", "context": "县长与副县长（党组成员）", "overlap_org": "志丹县人民政府", "overlap_period": ""},
    {"person_a": "zhidan_liu_xiaojun", "person_b": "zhidan_liu_xiaoyong", "type": "上下级", "context": "县长与副县长（党组成员）", "overlap_org": "志丹县人民政府", "overlap_period": ""},
    {"person_a": "zhidan_liu_xiaojun", "person_b": "zhidan_hao_yudong", "type": "上下级", "context": "县长与副县长（党组成员）", "overlap_org": "志丹县人民政府", "overlap_period": ""},
    {"person_a": "zhidan_liu_xiaojun", "person_b": "zhidan_feng_xiangbin", "type": "同事", "context": "县委正副书记", "overlap_org": "中共志丹县委员会", "overlap_period": ""},
    {"person_a": "zhidan_li_yongjun", "person_b": "zhidan_shi_zhenwen", "type": "上下级", "context": "县委书记与政法委书记", "overlap_org": "中共志丹县委员会", "overlap_period": ""},
    {"person_a": "zhidan_shi_zhenwen", "person_b": "zhidan_liang_wei", "type": "协作", "context": "政法委书记与公安局长工作协作", "overlap_org": "志丹县", "overlap_period": ""},
    {"person_a": "zhidan_liu_xiaojun", "person_b": "zhidan_liu_jianzhong", "type": "党政人大联系", "context": "县长与人大主任", "overlap_org": "志丹县", "overlap_period": ""},
    {"person_a": "zhidan_liu_xiaojun", "person_b": "zhidan_bai_baoming", "type": "党政政协联系", "context": "县长与政协主席", "overlap_org": "志丹县", "overlap_period": ""},
]

print(f"Building data for {slug}...")
print(f"  Persons: {len(persons)}")
print(f"  Organizations: {len(organizations)}")
print(f"  Positions: {len(positions)}")
print(f"  Relationships: {len(relationships)}")

run_build(
    slug=slug,
    persons=persons,
    organizations=organizations,
    positions=positions,
    relationships=relationships,
    db_path=DATABASE_DIR / f"{slug}_network.db",
    gexf_path=GRAPH_DIR / f"{slug}_network.gexf",
)

print("Done!")
