"""Build script for 白城市洮北区 (Taobei District, Baicheng, Jilin) leadership network.

Data sourced from official government website http://www.taobei.gov.cn/ (2026-08-03).
Research date: 2026-08-03
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "洮北区"

PERSONS = [
    {
        "id": 1, "name": "孙英宇", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "", "work_start": "",
        "current_post": "区委书记", "current_org": "中共白城市洮北区委员会",
        "source": "http://www.taobei.gov.cn/xxgk/tbyw/202607/t20260731_1040021.html",
    },
    {
        "id": 2, "name": "魏博扬", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "", "work_start": "",
        "current_post": "区委副书记、区长", "current_org": "洮北区人民政府",
        "source": "http://www.taobei.gov.cn/zfjg/gzbg/202601/t20260127_1030092.html",
    },
    {
        "id": 3, "name": "李敏", "gender": "女", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "", "work_start": "",
        "current_post": "区委副书记", "current_org": "中共洮北区委员会",
        "source": "http://www.taobei.gov.cn/xxgk/tbyw/202606/t20260610_1037198.html",
    },
    {
        "id": 4, "name": "王海军", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "", "work_start": "",
        "current_post": "区人大常委会主任", "current_org": "洮北区人民代表大会常务委员会",
        "source": "http://www.taobei.gov.cn/xxgk/tbyw/202601/t20260108_1028982.html",
    },
    {
        "id": 5, "name": "吴嘉彬", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "", "work_start": "",
        "current_post": "区政协主席", "current_org": "政协白城市洮北区委员会",
        "source": "http://www.taobei.gov.cn/xxgk/tbyw/202601/t20260107_1028912.html",
    },
    {
        "id": 6, "name": "刘永忠", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "", "work_start": "",
        "current_post": "区委常委、人武部政委", "current_org": "洮北区人民武装部",
        "source": "http://www.taobei.gov.cn/xxgk/tbyw/202607/t20260731_1040021.html",
    },
    {
        "id": 7, "name": "曹冶", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "", "work_start": "",
        "current_post": "区委常委、组织部部长", "current_org": "中共洮北区委组织部",
        "source": "http://www.taobei.gov.cn/xxgk/tbyw/202606/t20260610_1037198.html",
    },
    {
        "id": 8, "name": "暴龙", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "", "work_start": "",
        "current_post": "区委常委、副区长", "current_org": "洮北区人民政府",
        "source": "http://www.taobei.gov.cn/xxgk/tbyw/202601/t20260108_1028982.html",
    },
    {
        "id": 9, "name": "周彬", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "", "work_start": "",
        "current_post": "副区长", "current_org": "洮北区人民政府",
        "source": "http://www.taobei.gov.cn/zfjg/",
    },
    {
        "id": 10, "name": "高远", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "", "work_start": "",
        "current_post": "副区长", "current_org": "洮北区人民政府",
        "source": "http://xxgk.taobei.gov.cn/asd/szf/xxgkml/202412/t20241213_1004213.html",
    },
    {
        "id": 11, "name": "齐环宇", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "", "work_start": "",
        "current_post": "副区长", "current_org": "洮北区人民政府",
        "source": "http://www.taobei.gov.cn/zfjg/",
    },
    {
        "id": 12, "name": "焦雯倩", "gender": "女", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "", "work_start": "",
        "current_post": "副区长", "current_org": "洮北区人民政府",
        "source": "http://www.taobei.gov.cn/zfjg/",
    },
    {
        "id": 13, "name": "于龙", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "", "work_start": "",
        "current_post": "副区长", "current_org": "洮北区人民政府",
        "source": "http://www.taobei.gov.cn/zfjg/",
    },
    {
        "id": 14, "name": "王作书", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "", "work_start": "",
        "current_post": "副区长", "current_org": "洮北区人民政府",
        "source": "http://www.taobei.gov.cn/zfjg/",
    },
    {
        "id": 15, "name": "于文德", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "", "work_start": "",
        "current_post": "副区长", "current_org": "洮北区人民政府",
        "source": "http://www.taobei.gov.cn/zfjg/",
    },
    {
        "id": 16, "name": "王颖", "gender": "女", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "", "work_start": "",
        "current_post": "区人大常委会副主任", "current_org": "洮北区人民代表大会常务委员会",
        "source": "http://www.taobei.gov.cn/xxgk/tbyw/202601/t20260108_1028982.html",
    },
    {
        "id": 17, "name": "王林宇", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "", "work_start": "",
        "current_post": "区人大常委会副主任", "current_org": "洮北区人民代表大会常务委员会",
        "source": "http://www.taobei.gov.cn/xxgk/tbyw/202601/t20260108_1028982.html",
    },
    {
        "id": 18, "name": "张国华", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "", "work_start": "",
        "current_post": "区人大常委会副主任", "current_org": "洮北区人民代表大会常务委员会",
        "source": "http://www.taobei.gov.cn/xxgk/tbyw/202601/t20260108_1028982.html",
    },
    {
        "id": 19, "name": "张海茵", "gender": "女", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "", "work_start": "",
        "current_post": "区人大常委会副主任", "current_org": "洮北区人民代表大会常务委员会",
        "source": "http://www.taobei.gov.cn/xxgk/tbyw/202601/t20260108_1028982.html",
    },
    {
        "id": 20, "name": "谷晓飞", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "", "work_start": "",
        "current_post": "区政协副主席", "current_org": "政协白城市洮北区委员会",
        "source": "http://www.taobei.gov.cn/xxgk/tbyw/202601/t20260107_1028912.html",
    },
    {
        "id": 21, "name": "荣权", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "", "work_start": "",
        "current_post": "区政协副主席", "current_org": "政协白城市洮北区委员会",
        "source": "http://www.taobei.gov.cn/xxgk/tbyw/202601/t20260107_1028912.html",
    },
    {
        "id": 22, "name": "鲍明军", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "", "work_start": "",
        "current_post": "区领导", "current_org": "中共洮北区委员会",
        "source": "http://www.taobei.gov.cn/xxgk/tbyw/202601/t20260108_1028982.html",
    },
    {
        "id": 23, "name": "苗璐", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "", "work_start": "",
        "current_post": "区领导", "current_org": "中共洮北区委员会",
        "source": "http://www.taobei.gov.cn/xxgk/tbyw/202601/t20260108_1028982.html",
    },
    {
        "id": 24, "name": "曹希智", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "", "work_start": "",
        "current_post": "区领导", "current_org": "中共洮北区委员会",
        "source": "http://www.taobei.gov.cn/xxgk/tbyw/202601/t20260108_1028982.html",
    },
    {
        "id": 25, "name": "李永军", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "", "work_start": "",
        "current_post": "区领导", "current_org": "中共洮北区委员会",
        "source": "http://www.taobei.gov.cn/xxgk/tbyw/202601/t20260108_1028982.html",
    },
    {
        "id": 26, "name": "邢国涛", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "", "work_start": "",
        "current_post": "区领导", "current_org": "中共洮北区委员会",
        "source": "http://www.taobei.gov.cn/xxgk/tbyw/202601/t20260108_1028982.html",
    },
    {
        "id": 27, "name": "葛胜楠", "gender": "男", "ethnicity": "", "birth": "",
        "birthplace": "", "education": "", "party_join": "", "work_start": "",
        "current_post": "区领导", "current_org": "中共洮北区委员会",
        "source": "http://www.taobei.gov.cn/xxgk/tbyw/202601/t20260108_1028982.html",
    },
]

ORGANIZATIONS = [
    {"id": 1, "name": "中共白城市洮北区委员会", "type": "党委", "level": "县级", "parent": "中共白城市委员会", "location": "吉林省白城市洮北区"},
    {"id": 2, "name": "洮北区人民政府", "type": "政府", "level": "县级", "parent": "白城市人民政府", "location": "吉林省白城市洮北区"},
    {"id": 3, "name": "洮北区人民代表大会常务委员会", "type": "人大", "level": "县级", "parent": "白城市人民代表大会常务委员会", "location": "吉林省白城市洮北区"},
    {"id": 4, "name": "政协白城市洮北区委员会", "type": "政协", "level": "县级", "parent": "政协白城市委员会", "location": "吉林省白城市洮北区"},
    {"id": 5, "name": "中共洮北区委组织部", "type": "党委部门", "level": "县级", "parent": "中共洮北区委员会", "location": "吉林省白城市洮北区"},
    {"id": 6, "name": "洮北区人民武装部", "type": "军事", "level": "县级", "parent": "白城军分区", "location": "吉林省白城市洮北区"},
]

POSITIONS = [
    # 孙英宇 - 区委书记 (formerly 区长 ~202*)
    {"person_id": 1, "org_id": 1, "title": "区委书记", "start_date": "2025?", "end_date": "", "rank": "正县级", "note": "2026年3月已任区委书记"},
    {"person_id": 1, "org_id": 2, "title": "区长", "start_date": "2024?", "end_date": "2025?", "rank": "正县级", "note": "2024年12月以区长身份作政府工作报告"},
    # 2 - 魏博扬
    {"person_id": 2, "org_id": 1, "title": "区委副书记", "start_date": "2026?", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "区长", "start_date": "2026?", "end_date": "", "rank": "正县级", "note": "2026年1月首次以区长身份作政府工作报告"},
    # 3 - 李敏
    {"person_id": 3, "org_id": 1, "title": "区委副书记", "start_date": "", "end_date": "", "rank": "副县级", "note": "2026年6月以区委副书记身份出席会议"},
    # 4 - 王海军
    {"person_id": 4, "org_id": 3, "title": "区人大常委会主任", "start_date": "", "end_date": "", "rank": "正县级", "note": ""},
    # 5 - 吴嘉彬
    {"person_id": 5, "org_id": 4, "title": "区政协主席", "start_date": "", "end_date": "", "rank": "正县级", "note": "2026年1月作政协工作报告"},
    # 6 - 刘永忠
    {"person_id": 6, "org_id": 6, "title": "人武部政委", "start_date": "", "end_date": "", "rank": "副县级", "note": "区委常委"},
    {"person_id": 6, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    # 7 - 曹冶
    {"person_id": 7, "org_id": 5, "title": "组织部部长", "start_date": "", "end_date": "", "rank": "副县级", "note": "区委常委"},
    {"person_id": 7, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    # 8 - 暴龙
    {"person_id": 8, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副县级", "note": "区委常委"},
    {"person_id": 8, "org_id": 1, "title": "区委常委", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副县级", "note": "常务副区长?"},
    # 9-15 副区长
    {"person_id": 9, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副区长", "start_date": "2024-11-22", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 11, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 13, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 15, "org_id": 2, "title": "副区长", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    # 16-19 人大副主任
    {"person_id": 16, "org_id": 3, "title": "区人大常委会副主任", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 17, "org_id": 3, "title": "区人大常委会副主任", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 18, "org_id": 3, "title": "区人大常委会副主任", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 19, "org_id": 3, "title": "区人大常委会副主任", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    # 20-21 政协副主席
    {"person_id": 20, "org_id": 4, "title": "区政协副主席", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    {"person_id": 21, "org_id": 4, "title": "区政协副主席", "start_date": "", "end_date": "", "rank": "副县级", "note": ""},
    # 22-27 其他区领导（身份待确认具体职务）
    {"person_id": 22, "org_id": 1, "title": "区领导(待确认职务)", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 23, "org_id": 1, "title": "区领导(待确认职务)", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 24, "org_id": 1, "title": "区领导(待确认职务)", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 25, "org_id": 1, "title": "区领导(待确认职务)", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 26, "org_id": 1, "title": "区领导(待确认职务)", "start_date": "", "end_date": "", "rank": "", "note": ""},
    {"person_id": 27, "org_id": 1, "title": "区领导(待确认职务)", "start_date": "", "end_date": "", "rank": "", "note": ""},
]

RELATIONSHIPS = [
    # 孙英宇→魏博扬（区委书记-区长党政搭档）
    {"person_a": 1, "person_b": 2, "type": "党政搭档", "context": "区委书记与区长党政主要领导配合", "overlap_org": "中共洮北区委员会/洮北区人民政府", "overlap_period": "2026年至今"},
    # 李敏作为副书记与书记
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "区委书记与专职副书记", "overlap_org": "中共洮北区委员会", "overlap_period": "2026年至今"},
    # 刘永忠党委常委
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "区委书记与人武部政委", "overlap_org": "中共洮北区委员会", "overlap_period": "2026年至今"},
    # 曹冶组织部长
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "区委书记与组织部部长", "overlap_org": "中共洮北区委员会", "overlap_period": "2026年至今"},
    # 暴龙副区长
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "区长与副区长", "overlap_org": "洮北区人民政府", "overlap_period": "2026年至今"},
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "区委书记与区委常委副区长", "overlap_org": "中共洮北区委员会", "overlap_period": "2026年至今"},
    # 王海军人大主任
    {"person_a": 1, "person_b": 4, "type": "四套班子", "context": "区委书记与人大常委会主任", "overlap_org": "洮北区", "overlap_period": ""},
    # 吴嘉庭政协主席
    {"person_a": 1, "person_b": 5, "type": "四套班子", "context": "区委书记与政协主席", "overlap_org": "洮北区", "overlap_period": ""},
    # 高远副区长与区长
    {"person_a": 2, "person_b": 10, "type": "上下级", "context": "区长与副区长", "overlap_org": "洮北区人民政府", "overlap_period": "2026年至今"},
    # 焦文倩副区长
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "区长与副区长（分管教育）", "overlap_org": "洮北区人民政府", "overlap_period": "2026年至今"},
    # 李敏与曹冶（副书记+组织部长，党建工作配合）
    {"person_a": 3, "person_b": 7, "type": "同僚", "context": "区委专职副书记与组织部部长（党建工作配合）", "overlap_org": "中共洮北区委员会", "overlap_period": "2026年至今"},
    # 孙英宇与各副区长
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "区委书记与副区长", "overlap_org": "洮北区", "overlap_period": "2026年至今"},
    {"person_a": 1, "person_b": 11, "type": "上下级", "context": "区委书记与副区长", "overlap_org": "洮北区", "overlap_period": "2026年至今"},
    {"person_a": 1, "person_b": 13, "type": "上下级", "context": "区委书记与副区长", "overlap_org": "洮北区", "overlap_period": "2026年至今"},
    {"person_a": 1, "person_b": 14, "type": "上下级", "context": "区委书记与副区长", "overlap_org": "洮北区", "overlap_period": "2026年至今"},
    {"person_a": 1, "person_b": 15, "type": "上下级", "context": "区委书记与副区长", "overlap_org": "洮北区", "overlap_period": "2026年至今"},
]

if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=PERSONS,
        organizations=ORGANIZATIONS,
        positions=POSITIONS,
        relationships=RELATIONSHIPS,
        db_path=DATABASE_DIR / "洮北区_network.db",
        gexf_path=GRAPH_DIR / "洮北区_network.gexf",
    )
