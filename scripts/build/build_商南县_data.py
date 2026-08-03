#!/usr/bin/env python3
"""Build SQLite database and GEXF graph for 商南县 leadership network.

Uses gov_relation.runner.run_build() API.
Person/org IDs are string-based for cross-county dedup.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

# ── PERSONS ──────────────────────────────────────────────────────────

PERSONS = [
    # ── Top Leaders ──
    {
        "id": "shangnan_liu_hua",
        "name": "刘华", "gender": "女", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "中共商南县委书记", "current_org": "中共商南县委员会",
        "source": "https://www.shangnan.gov.cn/xwzx/jrsn.htm",
    },
    {
        "id": "shangnan_li_jun",
        "name": "李军", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "硕士研究生",
        "party_join": "中共党员", "work_start": "",
        "current_post": "商南县委副书记、县政府县长", "current_org": "商南县人民政府",
        "source": "https://www.shangnan.gov.cn/info/1470/1009312.htm",
    },

    # ── Standing Committee ──
    {
        "id": "shangnan_shi_chenxi",
        "name": "施晨曦", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "中共商南县委副书记", "current_org": "中共商南县委员会",
        "source": "https://www.shangnan.gov.cn/info/1032/1218002.htm",
    },
    {
        "id": "shangnan_wang_jiangang",
        "name": "王建刚", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "硕士研究生",
        "party_join": "中共党员", "work_start": "",
        "current_post": "商南县委常委、常务副县长", "current_org": "商南县人民政府",
        "source": "https://www.shangnan.gov.cn/info/1470/1009382.htm",
    },
    {
        "id": "shangnan_han_shoushan",
        "name": "韩寿山", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "商南县委常委", "current_org": "中共商南县委员会",
        "source": "https://www.shangnan.gov.cn/info/1032/1218222.htm",
    },
    {
        "id": "shangnan_lei_baowei",
        "name": "雷保卫", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "商南县委常委", "current_org": "中共商南县委员会",
        "source": "https://www.shangnan.gov.cn/info/1032/1218222.htm",
    },
    {
        "id": "shangnan_xiang_lin",
        "name": "相林", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "商南县委常委", "current_org": "中共商南县委员会",
        "source": "https://www.shangnan.gov.cn/info/1032/1218222.htm",
    },
    {
        "id": "shangnan_zhang_jie",
        "name": "张杰", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "商南县委常委", "current_org": "中共商南县委员会",
        "source": "https://www.shangnan.gov.cn/info/1032/1218222.htm",
    },
    {
        "id": "shangnan_nie_shicheng",
        "name": "聂仕成", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "商南县委常委、统战部部长", "current_org": "中共商南县委员会",
        "source": "https://www.shangnan.gov.cn/info/1032/1217752.htm",
    },
    {
        "id": "shangnan_guo_xin",
        "name": "郭鑫", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "商南县委常委、县人武部部长", "current_org": "商南县人武部",
        "source": "https://www.shangnan.gov.cn/info/1032/1218472.htm",
    },

    # ── Government Deputy Mayors ──
    {
        "id": "shangnan_jiang_guonian",
        "name": "蒋国年", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "大学本科",
        "party_join": "中共党员", "work_start": "",
        "current_post": "商南县政府副县长、县公安局长", "current_org": "商南县人民政府",
        "source": "https://www.shangnan.gov.cn/info/1470/1009422.htm",
    },
    {
        "id": "shangnan_wang_kun",
        "name": "王琨", "gender": "女", "ethnicity": "蒙古族",
        "birth": "", "birthplace": "", "education": "大学本科",
        "party_join": "", "work_start": "",
        "current_post": "商南县政府副县长", "current_org": "商南县人民政府",
        "source": "https://www.shangnan.gov.cn/info/1470/1009432.htm",
    },
    {
        "id": "shangnan_wang_zhongliang",
        "name": "王重良", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "陕西商南", "education": "",
        "party_join": "中共党员", "work_start": "1995年11月",
        "current_post": "商南县政府副县长", "current_org": "商南县人民政府",
        "source": "https://www.shangnan.gov.cn/info/1470/1009462.htm",
    },
    {
        "id": "shangnan_chen_siliang",
        "name": "陈斯亮", "gender": "男", "ethnicity": "汉族",
        "birth": "1988年11月", "birthplace": "", "education": "工学博士",
        "party_join": "", "work_start": "",
        "current_post": "商南县政府副县长（挂职）", "current_org": "商南县人民政府",
        "source": "https://www.shangnan.gov.cn/info/1470/1009372.htm",
    },
    {
        "id": "shangnan_wu_kailiang",
        "name": "吴锴亮", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "大学本科",
        "party_join": "中共党员", "work_start": "",
        "current_post": "商南县政府党组成员", "current_org": "商南县人民政府",
        "source": "https://www.shangnan.gov.cn/info/1470/1009472.htm",
    },

    # ── Other Leaders ──
    {
        "id": "shangnan_wang_xiaohu",
        "name": "王晓虎", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "商南县人大常委会主任", "current_org": "商南县人大常委会",
        "source": "https://www.shangnan.gov.cn/info/1032/1218472.htm",
    },
    {
        "id": "shangnan_zhang_xianhui",
        "name": "张贤慧", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "商南县政协主席", "current_org": "政协商南县委员会",
        "source": "https://www.shangnan.gov.cn/info/1032/1218472.htm",
    },
    {
        "id": "shangnan_wang_zuo",
        "name": "王佐", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "原副县长（已离职）", "current_org": "",
        "source": "https://www.shangnan.gov.cn/info/1515/1215342.htm",
    },
    {
        "id": "shangnan_chen_yao",
        "name": "陈瑶", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "商南县人大常委会副主任", "current_org": "商南县人大常委会",
        "source": "https://www.shangnan.gov.cn/info/1032/1218002.htm",
    },
    {
        "id": "shangnan_gao_shibin",
        "name": "高世斌", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "商南县域工业集中区党工委书记", "current_org": "商南县域工业集中区",
        "source": "https://www.shangnan.gov.cn/info/1032/1217752.htm",
    },
    {
        "id": "shangnan_jiang_guolin",
        "name": "江国林", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "商南县政协副主席", "current_org": "政协商南县委员会",
        "source": "https://www.shangnan.gov.cn/info/1032/1216152.htm",
    },
    {
        "id": "shangnan_li_yuepeng",
        "name": "李岳鹏", "gender": "男", "ethnicity": "汉族",
        "birth": "", "birthplace": "", "education": "",
        "party_join": "中共党员", "work_start": "",
        "current_post": "商南县人武部政委", "current_org": "商南县人武部",
        "source": "https://www.shangnan.gov.cn/info/1032/1218472.htm",
    },
]

# ── ORGANIZATIONS ────────────────────────────────────────────────────

ORGANIZATIONS = [
    {"id": "org_cpc_shangnan", "name": "中共商南县委员会", "type": "党委", "level": "县处级", "parent": "中共商洛市委员会", "location": "陕西省商洛市商南县"},
    {"id": "org_gov_shangnan", "name": "商南县人民政府", "type": "政府", "level": "县处级", "parent": "商洛市人民政府", "location": "陕西省商洛市商南县"},
    {"id": "org_npc_shangnan", "name": "商南县人大常委会", "type": "人大", "level": "县处级", "parent": "商洛市人大常委会", "location": "陕西省商洛市商南县"},
    {"id": "org_cppcc_shangnan", "name": "政协商南县委员会", "type": "政协", "level": "县处级", "parent": "政协商洛市委员会", "location": "陕西省商洛市商南县"},
    {"id": "org_mil_shangnan", "name": "商南县人武部", "type": "军事", "level": "县处级", "parent": "商洛军分区", "location": "陕西省商洛市商南县"},
    {"id": "org_zone_shangnan", "name": "商南县域工业集中区", "type": "开发区", "level": "县处级", "parent": "商南县人民政府", "location": "陕西省商洛市商南县"},
]

# ── POSITIONS ────────────────────────────────────────────────────────

POSITIONS = [
    {"person_id": "shangnan_liu_hua", "org_id": "org_cpc_shangnan", "title": "县委书记", "start": "", "end": "", "rank": "正处级", "note": "全面主持县委工作"},
    {"person_id": "shangnan_li_jun", "org_id": "org_gov_shangnan", "title": "县长", "start": "", "end": "", "rank": "正处级", "note": "主持县政府全面工作"},
    {"person_id": "shangnan_li_jun", "org_id": "org_cpc_shangnan", "title": "县委副书记", "start": "", "end": "", "rank": "正处级", "note": ""},
    {"person_id": "shangnan_shi_chenxi", "org_id": "org_cpc_shangnan", "title": "县委副书记", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": "shangnan_wang_jiangang", "org_id": "org_gov_shangnan", "title": "常务副县长", "start": "", "end": "", "rank": "副处级", "note": "县政府党组副书记"},
    {"person_id": "shangnan_wang_jiangang", "org_id": "org_cpc_shangnan", "title": "县委常委", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": "shangnan_jiang_guonian", "org_id": "org_gov_shangnan", "title": "副县长", "start": "", "end": "", "rank": "副处级", "note": "兼县公安局长"},
    {"person_id": "shangnan_wang_kun", "org_id": "org_gov_shangnan", "title": "副县长", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": "shangnan_wang_zhongliang", "org_id": "org_gov_shangnan", "title": "副县长", "start": "2022年9月", "end": "", "rank": "副处级", "note": ""},
    {"person_id": "shangnan_chen_siliang", "org_id": "org_gov_shangnan", "title": "副县长（挂职）", "start": "", "end": "", "rank": "副处级", "note": "长安大学挂职"},
    {"person_id": "shangnan_wu_kailiang", "org_id": "org_gov_shangnan", "title": "县政府党组成员", "start": "", "end": "", "rank": "副处级", "note": "兼青山镇党委副书记（挂职）"},
    {"person_id": "shangnan_han_shoushan", "org_id": "org_cpc_shangnan", "title": "县委常委", "start": "", "end": "", "rank": "副处级", "note": "推测为组织部部长"},
    {"person_id": "shangnan_lei_baowei", "org_id": "org_cpc_shangnan", "title": "县委常委", "start": "", "end": "", "rank": "副处级", "note": "推测为县纪委书记"},
    {"person_id": "shangnan_xiang_lin", "org_id": "org_cpc_shangnan", "title": "县委常委", "start": "", "end": "", "rank": "副处级", "note": "推测为政法委书记"},
    {"person_id": "shangnan_zhang_jie", "org_id": "org_cpc_shangnan", "title": "县委常委", "start": "", "end": "", "rank": "副处级", "note": "推测为宣传部部长"},
    {"person_id": "shangnan_nie_shicheng", "org_id": "org_cpc_shangnan", "title": "县委常委、统战部部长", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": "shangnan_guo_xin", "org_id": "org_mil_shangnan", "title": "县委常委、县人武部部长", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": "shangnan_wang_xiaohu", "org_id": "org_npc_shangnan", "title": "县人大常委会主任", "start": "", "end": "", "rank": "正处级", "note": ""},
    {"person_id": "shangnan_zhang_xianhui", "org_id": "org_cppcc_shangnan", "title": "县政协主席", "start": "", "end": "", "rank": "正处级", "note": ""},
    {"person_id": "shangnan_wang_zuo", "org_id": "org_gov_shangnan", "title": "原副县长（已离职）", "start": "", "end": "2026年6月", "rank": "副处级", "note": ""},
    {"person_id": "shangnan_chen_yao", "org_id": "org_npc_shangnan", "title": "县人大常委会副主任", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": "shangnan_gao_shibin", "org_id": "org_zone_shangnan", "title": "党工委书记", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": "shangnan_jiang_guolin", "org_id": "org_cppcc_shangnan", "title": "县政协副主席", "start": "", "end": "", "rank": "副处级", "note": ""},
    {"person_id": "shangnan_li_yuepeng", "org_id": "org_mil_shangnan", "title": "政委", "start": "", "end": "", "rank": "副处级", "note": ""},
]

# ── RELATIONSHIPS ────────────────────────────────────────────────────

RELATIONSHIPS = [
    {"person_a": "shangnan_liu_hua", "person_b": "shangnan_li_jun", "type": "党政搭档", "context": "县委书记与县长", "overlap_org": "中共商南县委员会", "overlap_period": "2026年至今"},
    {"person_a": "shangnan_li_jun", "person_b": "shangnan_wang_jiangang", "type": "上下级", "context": "县长与常务副县长，日常政府运作核心", "overlap_org": "商南县人民政府", "overlap_period": "2026年至今"},
    {"person_a": "shangnan_liu_hua", "person_b": "shangnan_shi_chenxi", "type": "上下级", "context": "县委书记与县委副书记，工作协调", "overlap_org": "中共商南县委员会", "overlap_period": "2026年至今"},
    {"person_a": "shangnan_liu_hua", "person_b": "shangnan_nie_shicheng", "type": "上下级", "context": "统战部长多次陪同书记调研", "overlap_org": "中共商南县委员会", "overlap_period": "2026年至今"},
    {"person_a": "shangnan_wang_jiangang", "person_b": "shangnan_jiang_guonian", "type": "同僚", "context": "同为县政府副县长", "overlap_org": "商南县人民政府", "overlap_period": "2026年至今"},
    {"person_a": "shangnan_wang_jiangang", "person_b": "shangnan_wang_kun", "type": "同僚", "context": "同为县政府副县长", "overlap_org": "商南县人民政府", "overlap_period": "2026年至今"},
    {"person_a": "shangnan_wang_jiangang", "person_b": "shangnan_wang_zhongliang", "type": "同僚", "context": "同为县政府副县长", "overlap_org": "商南县人民政府", "overlap_period": "2022年至今"},
    {"person_a": "shangnan_wang_jiangang", "person_b": "shangnan_chen_siliang", "type": "同僚", "context": "陈斯亮协助王建刚分管相关工作", "overlap_org": "商南县人民政府", "overlap_period": "2026年至今"},
    {"person_a": "shangnan_wang_kun", "person_b": "shangnan_chen_siliang", "type": "协助关系", "context": "陈斯亮协助王琨分管相关工作", "overlap_org": "商南县人民政府", "overlap_period": "2026年至今"},
    {"person_a": "shangnan_wang_zhongliang", "person_b": "shangnan_wu_kailiang", "type": "协助关系", "context": "吴锴亮协助王重良分管相关工作", "overlap_org": "商南县人民政府", "overlap_period": "2026年至今"},
    {"person_a": "shangnan_wang_zuo", "person_b": "shangnan_jiang_guonian", "type": "工作交接", "context": "王佐离职后水利工作由蒋国年接手", "overlap_org": "商南县人民政府", "overlap_period": "2026年6月"},
    {"person_a": "shangnan_liu_hua", "person_b": "shangnan_guo_xin", "type": "同僚", "context": "同为县委常委", "overlap_org": "中共商南县委员会", "overlap_period": "2026年至今"},
    {"person_a": "shangnan_han_shoushan", "person_b": "shangnan_lei_baowei", "type": "同僚", "context": "同为县委常委", "overlap_org": "中共商南县委员会", "overlap_period": "2026年至今"},
    {"person_a": "shangnan_xiang_lin", "person_b": "shangnan_zhang_jie", "type": "同僚", "context": "相林与张杰均为县委常委", "overlap_org": "中共商南县委员会", "overlap_period": "2026年至今"},
]

# ── BUILD ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    run_build(
        slug="商南县",
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DATABASE_DIR / "商南县_network.db",
        gexf_path=GRAPH_DIR / "商南县_network.gexf",
    )
    print("Done!")