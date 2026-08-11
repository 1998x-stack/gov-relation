#!/usr/bin/env python3
"""娄底市 (Loudi City) 领导班子关系网络数据构建脚本。

数据来源:
- 娄底市人民政府官网 https://www.hnloudi.gov.cn
- 娄底市人大常委会官网 http://www.ldrd.gov.cn
- 娄底市政协官网 http://ldzx.hnloudi.gov.cn
- 维基百科 / 项目已有数据
"""

import sqlite3
import sys
from pathlib import Path

# Add project root for gov_relation imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

from gov_relation.gexf import GEXFBuilder
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR
from gov_relation.schema import create_tables, insert_organizations, insert_persons, insert_positions, insert_relationships
from gov_relation.log import get_logger

logger = get_logger(__name__)

SLUG = "娄底市"

_PERSON_STRING_IDS = [  # temp storage for mapping
    "loudi_zeng_chaoqun", "loudi_he_zhaohui", "loudi_cai_xinya", "loudi_wu_hu",
    "loudi_xiang_qianyong", "loudi_fu_xiaosong", "loudi_yang_wei", "loudi_wang_weiguo",
    "loudi_guo_jianhua", "loudi_zeng_zhiyan", "loudi_li_dingqiao", "loudi_liang_lijian",
    "loudi_li_yanwen", "loudi_liu_zhigang", "loudi_zeng_boyi", "loudi_chen_chuangye",
    "loudi_duan_xiaosai", "loudi_deng_weimou", "loudi_peng_ shiqing", "loudi_li_jilian",
    "loudi_peng_tao", "loudi_zou_jianfeng", "loudi_zou_wenhui",
]
_org_string_ids = [
    "org_loudi_party", "org_loudi_gov", "org_loudi_npc", "org_loudi_cppcc", "org_loudi_psb",
    "org_louxing_party", "org_louxing_gov", "org_lengshuijiang_party", "org_lengshuijiang_gov",
    "org_lianyuan_party", "org_lianyuan_gov", "org_shuangfeng_party", "org_shuangfeng_gov",
    "org_xinhua_party", "org_xinhua_gov", "org_hunan_npc",
]
PSID = {s: i+1 for i, s in enumerate(_PERSON_STRING_IDS)}
OSID = {s: i+1 for i, s in enumerate(_org_string_ids)}

PERSONS = [
    # ═════════════════════════════════════
    # 市级领导
    # ═════════════════════════════════════
    # 市委书记
    {
        "id": PSID["loudi_zeng_chaoqun"],
        "name": "曾超群",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年9月",
        "birthplace": "湖南省邵东市",
        "education": "北京大学经济学院国际经济专业本科、湖南农业大学管理学博士",
        "party_join": "1998年12月",
        "work_start": "1997年9月",
        "current_post": "中共娄底市委书记",
        "current_org": "中共娄底市委",
        "source": "https://www.hnloudi.gov.cn + 维基百科",
    },
    # 市长
    {
        "id": PSID["loudi_he_zhaohui"],
        "name": "何朝晖",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年4月",
        "birthplace": "湖南省攸县",
        "education": "在职研究生、管理学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "娄底市委副书记、市长",
        "current_org": "娄底市人民政府",
        "source": "https://www.hnloudi.gov.cn/loudi/zfld/201908/904b8ecd635045c18dc9d731d2504ecf.shtml",
    },
    # 市委常委、市政府党组副书记、市委秘书长
    {
        "id": "loudi_cai_xinya",
        "name": "蔡新亚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年10月",
        "birthplace": "",
        "education": "工商管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、市政府党组副书记、市委秘书长",
        "current_org": "中共娄底市委/娄底市人民政府",
        "source": "https://www.hnloudi.gov.cn/loudi/zfld/202403/3993ca4e01a44f9faf84f0ac43305c68.shtml",
    },
    # 副市长
    {
        "id": "loudi_wu_hu",
        "name": "伍鹄",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年10月",
        "birthplace": "",
        "education": "研究生、法学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "娄底市副市长",
        "current_org": "娄底市人民政府",
        "source": "https://www.hnloudi.gov.cn/loudi/zfld/201908/5c42a8bf7b0f463b8122fc04a11efaff.shtml",
    },
    {
        "id": "loudi_xiang_qianyong",
        "name": "向乾勇",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年9月",
        "birthplace": "",
        "education": "大学、理学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "娄底市副市长",
        "current_org": "娄底市人民政府",
        "source": "https://www.hnloudi.gov.cn/loudi/zfld/201908/d194d19088d54b3f91d0dc7ddd756f66.shtml",
    },
    {
        "id": "loudi_fu_xiaosong",
        "name": "傅小松",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年1月",
        "birthplace": "",
        "education": "大学、文学学士",
        "party_join": "民盟盟员",
        "work_start": "",
        "current_post": "娄底市副市长、民盟娄底市委会主委",
        "current_org": "娄底市人民政府",
        "source": "https://www.hnloudi.gov.cn/loudi/zfld/202601/3699d8171b344935ab51b333833242e5.shtml",
    },
    {
        "id": "loudi_yang_wei",
        "name": "杨维",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1966年11月",
        "birthplace": "",
        "education": "大学、工学学士、高级工程师",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "娄底市副市长",
        "current_org": "娄底市人民政府",
        "source": "https://www.hnloudi.gov.cn/loudi/zfld/202111/a4f867d1a7574a01a4f57c9d0d6cedf8.shtml",
    },
    {
        "id": "loudi_wang_weiguo",
        "name": "汪卫国",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年10月",
        "birthplace": "",
        "education": "中央党校研究生、法学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "娄底市副市长、市公安局党委书记、局长",
        "current_org": "娄底市人民政府/娄底市公安局",
        "source": "https://www.hnloudi.gov.cn/loudi/zfld/202508/afdc02db382f469497c4188688ad83a3.shtml",
    },
    {
        "id": "loudi_guo_jianhua",
        "name": "郭建华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年5月",
        "birthplace": "",
        "education": "研究生、经济学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "娄底市副市长",
        "current_org": "娄底市人民政府",
        "source": "https://www.hnloudi.gov.cn/loudi/zfld/202606/7e8b5405b2a142e9bf9de9ca46419054.shtml",
    },
    # 市政府秘书长
    {
        "id": "loudi_zeng_zhiyan",
        "name": "曾志彦",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年10月",
        "birthplace": "",
        "education": "中央党校研究生",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "娄底市政府秘书长、市政府办党组书记",
        "current_org": "娄底市人民政府",
        "source": "https://www.hnloudi.gov.cn/loudi/zfld/202311/5a9c228c5bf24a3986324ee8fa556eb3.shtml",
    },
    # 市人大常委会
    {
        "id": "loudi_li_dingqiao",
        "name": "李定桥",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年",
        "birthplace": "湖南省安仁县",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "娄底市人大常委会主任",
        "current_org": "娄底市人大常委会",
        "source": "http://www.ldrd.gov.cn",
    },
    # 市政协
    {
        "id": "loudi_liang_lijian",
        "name": "梁立坚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年",
        "birthplace": "湖南省涟源市",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "娄底市政协主席",
        "current_org": "政协娄底市委员会",
        "source": "http://ldzx.hnloudi.gov.cn",
    },
    # ═════════════════════════════════════
    # 县市区领导
    # ═════════════════════════════════════
    # 娄星区
    {
        "id": "loudi_li_yanwen",
        "name": "李彦文",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年",
        "birthplace": "湖南省涟源市",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "娄星区委书记",
        "current_org": "中共娄星区委",
        "source": "项目已有数据（维基百科）",
    },
    {
        "id": "loudi_liu_zhigang",
        "name": "刘志刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年",
        "birthplace": "湖南省新化县",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "娄星区长",
        "current_org": "娄星区人民政府",
        "source": "项目已有数据（维基百科）",
    },
    # 冷水江市
    {
        "id": "loudi_zeng_boyi",
        "name": "曾伯怡",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年",
        "birthplace": "湖南省双峰县",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "冷水江市委书记",
        "current_org": "中共冷水江市委",
        "source": "项目已有数据（维基百科）",
    },
    {
        "id": "loudi_chen_chuangye",
        "name": "陈创业",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年",
        "birthplace": "湖南省新化县",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "冷水江市长",
        "current_org": "冷水江市人民政府",
        "source": "项目已有数据（维基百科）",
    },
    # 涟源市
    {
        "id": "loudi_duan_xiaosai",
        "name": "段晓赛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年",
        "birthplace": "湖南省耒阳市",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "涟源市委书记",
        "current_org": "中共涟源市委",
        "source": "项目已有数据（维基百科）",
    },
    {
        "id": "loudi_deng_weimou",
        "name": "邓伟谋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1976年",
        "birthplace": "湖南省双峰县",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "涟源市长",
        "current_org": "涟源市人民政府",
        "source": "项目已有数据（维基百科）",
    },
    # 双峰县
    {
        "id": "loudi_peng_ shiqing",
        "name": "彭石清",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967年",
        "birthplace": "湖南省娄星区",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "双峰县委书记、娄底市政协副主席",
        "current_org": "中共双峰县委/政协娄底市委员会",
        "source": "项目已有数据（维基百科）/ 政协官网",
    },
    {
        "id": "loudi_li_jilian",
        "name": "李基联",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年",
        "birthplace": "湖南省溆浦县",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "双峰县长",
        "current_org": "双峰县人民政府",
        "source": "项目已有数据（维基百科）",
    },
    # 新化县
    {
        "id": "loudi_peng_tao",
        "name": "彭韬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年",
        "birthplace": "湖南省新化县",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "新化县委书记",
        "current_org": "中共新化县委",
        "source": "项目已有数据（维基百科）",
    },
    {
        "id": "loudi_zou_jianfeng",
        "name": "邹剑锋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985年",
        "birthplace": "湖南省长沙县",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "新化县长",
        "current_org": "新化县人民政府",
        "source": "项目已有数据（维基百科）",
    },
    # ═════════════════════════════════════
    # 前任领导
    # ═════════════════════════════════════
    {
        "id": "loudi_zou_wenhui",
        "name": "邹文辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1965年2月",
        "birthplace": "湖南省常宁市",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "湖南省人大常委会委员、环境与资源保护委员会主任委员",
        "current_org": "湖南省人大常委会",
        "source": "项目已有数据（维基百科）",
    },
]

ORGANIZATIONS = [
    # 市级组织
    {
        "id": "org_loudi_party",
        "name": "中共娄底市委",
        "type": "党委",
        "level": "地级市",
        "parent": "中共湖南省委",
        "location": "娄底市",
    },
    {
        "id": "org_loudi_gov",
        "name": "娄底市人民政府",
        "type": "政府",
        "level": "地级市",
        "parent": "娄底市委",
        "location": "娄底市",
    },
    {
        "id": "org_loudi_npc",
        "name": "娄底市人大常委会",
        "type": "人大",
        "level": "地级市",
        "parent": "娄底市委",
        "location": "娄底市",
    },
    {
        "id": "org_loudi_cppcc",
        "name": "政协娄底市委员会",
        "type": "政协",
        "level": "地级市",
        "parent": "娄底市委",
        "location": "娄底市",
    },
    {
        "id": "org_loudi_psb",
        "name": "娄底市公安局",
        "type": "政府部门",
        "level": "地级市",
        "parent": "娄底市人民政府",
        "location": "娄底市",
    },
    # 县市区组织
    {
        "id": "org_louxing_party",
        "name": "中共娄星区委",
        "type": "党委",
        "level": "县处级",
        "parent": "中共娄底市委",
        "location": "娄星区",
    },
    {
        "id": "org_louxing_gov",
        "name": "娄星区人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "娄底市人民政府",
        "location": "娄星区",
    },
    {
        "id": "org_lengshuijiang_party",
        "name": "中共冷水江市委",
        "type": "党委",
        "level": "县处级",
        "parent": "中共娄底市委",
        "location": "冷水江市",
    },
    {
        "id": "org_lengshuijiang_gov",
        "name": "冷水江市人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "娄底市人民政府",
        "location": "冷水江市",
    },
    {
        "id": "org_lianyuan_party",
        "name": "中共涟源市委",
        "type": "党委",
        "level": "县处级",
        "parent": "中共娄底市委",
        "location": "涟源市",
    },
    {
        "id": "org_lianyuan_gov",
        "name": "涟源市人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "娄底市人民政府",
        "location": "涟源市",
    },
    {
        "id": "org_shuangfeng_party",
        "name": "中共双峰县委",
        "type": "党委",
        "level": "县处级",
        "parent": "中共娄底市委",
        "location": "双峰县",
    },
    {
        "id": "org_shuangfeng_gov",
        "name": "双峰县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "娄底市人民政府",
        "location": "双峰县",
    },
    {
        "id": "org_xinhua_party",
        "name": "中共新化县委",
        "type": "党委",
        "level": "县处级",
        "parent": "中共娄底市委",
        "location": "新化县",
    },
    {
        "id": "org_xinhua_gov",
        "name": "新化县人民政府",
        "type": "政府",
        "level": "县处级",
        "parent": "娄底市人民政府",
        "location": "新化县",
    },
    # 省人大
    {
        "id": "org_hunan_npc",
        "name": "湖南省人大常委会",
        "type": "人大",
        "level": "省级",
        "parent": "中共湖南省委",
        "location": "长沙市",
    },
]

# String ID to numeric ID mapping (for GEXF)
PERSON_IDS = {p["id"]: i + 1 for i, p in enumerate(PERSONS)}
ORG_IDS = {o["id"]: i + 1 for i, o in enumerate(ORGANIZATIONS)}

def mid(s: str) -> int:
    """Map string ID to numeric ID."""
    return PERSON_IDS.get(s, 0)

def oid(s: str) -> int:
    """Map org string ID to numeric ID."""
    return ORG_IDS.get(s, 0)

POSITIONS = [
    # 曾超群
    {"person_id": mid("loudi_zeng_chaoqun"), "org_id": oid("org_loudi_party"), "title": "市委书记", "start_date": "2025-04", "end_date": "", "rank": "正厅级", "note": "由市长升任"},
    {"person_id": mid("loudi_zeng_chaoqun"), "org_id": oid("org_loudi_gov"), "title": "市长", "start_date": "2021-04", "end_date": "2025-04", "rank": "正厅级", "note": ""},
    # 何朝晖
    {"person_id": mid("loudi_he_zhaohui"), "org_id": oid("org_loudi_gov"), "title": "市长", "start_date": "2025-11", "end_date": "", "rank": "正厅级", "note": ""},
    # 蔡新亚
    {"person_id": mid("loudi_cai_xinya"), "org_id": oid("org_loudi_party"), "title": "市委常委、市委秘书长", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": mid("loudi_cai_xinya"), "org_id": oid("org_loudi_gov"), "title": "市政府党组副书记", "start_date": "", "end_date": "", "rank": "副厅级", "note": ""},
    # 副市长
    {"person_id": mid("loudi_wu_hu"), "org_id": oid("org_loudi_gov"), "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "分管水利、农业农村等"},
    {"person_id": mid("loudi_xiang_qianyong"), "org_id": oid("org_loudi_gov"), "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "分管自然资源、住建等"},
    {"person_id": mid("loudi_fu_xiaosong"), "org_id": oid("org_loudi_gov"), "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "民盟盟员"},
    {"person_id": mid("loudi_yang_wei"), "org_id": oid("org_loudi_gov"), "title": "副市长", "start_date": "", "end_date": "", "rank": "副厅级", "note": "分管商务、文旅等"},
    {"person_id": mid("loudi_wang_weiguo"), "org_id": oid("org_loudi_gov"), "title": "副市长、公安局长", "start_date": "2025-08", "end_date": "", "rank": "副厅级", "note": ""},
    {"person_id": mid("loudi_wang_weiguo"), "org_id": oid("org_loudi_psb"), "title": "党委书记、局长", "start_date": "2025-08", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": mid("loudi_guo_jianhua"), "org_id": oid("org_loudi_gov"), "title": "副市长", "start_date": "2026-06", "end_date": "", "rank": "副厅级", "note": "1983年生/经济学博士"},
    # 秘书长
    {"person_id": mid("loudi_zeng_zhiyan"), "org_id": oid("org_loudi_gov"), "title": "市政府秘书长", "start_date": "", "end_date": "", "rank": "正处级", "note": ""},
    # 人大
    {"person_id": mid("loudi_li_dingqiao"), "org_id": oid("org_loudi_npc"), "title": "主任", "start_date": "2026-01", "end_date": "", "rank": "正厅级", "note": ""},
    # 政协
    {"person_id": mid("loudi_liang_lijian"), "org_id": oid("org_loudi_cppcc"), "title": "主席", "start_date": "2022-01", "end_date": "", "rank": "正厅级", "note": ""},
    # 娄星区
    {"person_id": mid("loudi_li_yanwen"), "org_id": oid("org_louxing_party"), "title": "区委书记", "start_date": "2018-10", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": mid("loudi_liu_zhigang"), "org_id": oid("org_louxing_gov"), "title": "区长", "start_date": "2021-10", "end_date": "", "rank": "正处级", "note": ""},
    # 冷水江市
    {"person_id": mid("loudi_zeng_boyi"), "org_id": oid("org_lengshuijiang_party"), "title": "市委书记", "start_date": "2021-07", "end_date": "", "rank": "正处级", "note": ""},
    {"person_id": mid("loudi_chen_chuangye"), "org_id": oid("org_lengshuijiang_gov"), "title": "市长", "start_date": "2021-09", "end_date": "", "rank": "正处级", "note": ""},
    # 涟源市
    {"person_id": mid("loudi_duan_xiaosai"), "org_id": oid("org_lianyuan_party"), "title": "市委书记", "start_date": "2025-03", "end_date": "", "rank": "正处级", "note": "从衡山县县长跨市调任"},
    {"person_id": mid("loudi_deng_weimou"), "org_id": oid("org_lianyuan_gov"), "title": "市长", "start_date": "2021-07", "end_date": "", "rank": "正处级", "note": ""},
    # 双峰县
    {"person_id": mid("loudi_peng_ shiqing"), "org_id": oid("org_shuangfeng_party"), "title": "县委书记", "start_date": "2021-07", "end_date": "", "rank": "正处级", "note": "同时任市政协副主席"},
    {"person_id": mid("loudi_li_jilian"), "org_id": oid("org_shuangfeng_gov"), "title": "县长", "start_date": "2021-10", "end_date": "", "rank": "正处级", "note": "从溆浦跨市调任"},
    # 新化县
    {"person_id": mid("loudi_peng_tao"), "org_id": oid("org_xinhua_party"), "title": "县委书记", "start_date": "2025-06", "end_date": "", "rank": "正处级", "note": "1984年生"},
    {"person_id": mid("loudi_zou_jianfeng"), "org_id": oid("org_xinhua_gov"), "title": "县长", "start_date": "2025-12", "end_date": "", "rank": "正处级", "note": "1985年生，从长沙县调任"},
    # 前任
    {"person_id": mid("loudi_zou_wenhui"), "org_id": oid("org_loudi_party"), "title": "市委书记", "start_date": "2021-10", "end_date": "2025-04", "rank": "正厅级", "note": ""},
    {"person_id": mid("loudi_zou_wenhui"), "org_id": oid("org_hunan_npc"), "title": "省人大常委会委员/环资委主任委员", "start_date": "2025-01", "end_date": "", "rank": "正厅级", "note": ""},
]

RELATIONSHIPS = [
    # 同级党政搭档（强关系）
    {"person_a": mid("loudi_zeng_chaoqun"), "person_b": mid("loudi_he_zhaohui"), "type": "前后任", "context": "曾超群2025.4升书记，何朝晖2025.11接任市长", "overlap_org": "娄底市政府", "overlap_period": "2025.04-2025.11"},
    {"person_a": mid("loudi_peng_tao"), "person_b": mid("loudi_zou_jianfeng"), "type": "同级党政搭档", "context": "新化县党政一把手", "overlap_org": "新化县", "overlap_period": "2025.12-"},
    {"person_a": mid("loudi_zeng_boyi"), "person_b": mid("loudi_chen_chuangye"), "type": "同级党政搭档", "context": "冷水江党政一把手", "overlap_org": "冷水江市", "overlap_period": "2021.09-"},
    {"person_a": mid("loudi_duan_xiaosai"), "person_b": mid("loudi_deng_weimou"), "type": "同级党政搭档", "context": "涟源党政一把手", "overlap_org": "涟源市", "overlap_period": "2025.03-"},
    # 同乡关系
    {"person_a": mid("loudi_liang_lijian"), "person_b": mid("loudi_li_yanwen"), "type": "同乡", "context": "涟源人", "overlap_org": "", "overlap_period": ""},
    {"person_a": mid("loudi_liu_zhigang"), "person_b": mid("loudi_peng_tao"), "type": "同乡", "context": "新化人", "overlap_org": "", "overlap_period": ""},
    {"person_a": mid("loudi_chen_chuangye"), "person_b": mid("loudi_peng_tao"), "type": "同乡", "context": "新化人", "overlap_org": "", "overlap_period": ""},
    {"person_a": mid("loudi_zeng_boyi"), "person_b": mid("loudi_deng_weimou"), "type": "同乡", "context": "双峰人", "overlap_org": "", "overlap_period": ""},
    # 跨县交流
    {"person_a": mid("loudi_duan_xiaosai"), "person_b": mid("loudi_zeng_chaoqun"), "type": "跨县交流", "context": "段晓赛从衡山县跨市调任涟源市委书记", "overlap_org": "", "overlap_period": ""},
    {"person_a": mid("loudi_zou_jianfeng"), "person_b": mid("loudi_zeng_chaoqun"), "type": "跨县交流", "context": "邹剑锋从长沙县调任新化县长", "overlap_org": "长沙县", "overlap_period": ""},
    # 前后任
    {"person_a": mid("loudi_zeng_chaoqun"), "person_b": mid("loudi_zou_wenhui"), "type": "前后任", "context": "邹文辉2021-2025任书记，曾超群接任", "overlap_org": "娄底市委", "overlap_period": ""},
]

def main():
    db_path = DATABASE_DIR / f"{SLUG}_network.db"
    gexf_path = GRAPH_DIR / f"{SLUG}_network.gexf"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    gexf_path.parent.mkdir(parents=True, exist_ok=True)

    # Build SQLite
    logger.info("Building database: %s", db_path)
    conn = sqlite3.connect(str(db_path))
    try:
        create_tables(conn, overwrite=True)
        insert_persons(conn, PERSONS)
        insert_organizations(conn, ORGANIZATIONS)
        insert_positions(conn, POSITIONS)
        insert_relationships(conn, RELATIONSHIPS)
        logger.info("DB ready: %d persons, %d orgs, %d positions, %d relationships",
                     len(PERSONS), len(ORGANIZATIONS), len(POSITIONS), len(RELATIONSHIPS))
    finally:
        conn.close()

    # Build GEXF
    logger.info("Building GEXF: %s", gexf_path)
    builder = GEXFBuilder(title=SLUG)
    for p in PERSONS:
        builder.add_person(
            id=mid(p["id"]),
            name=p.get("name", ""),
            current_post=p.get("current_post", ""),
            current_org=p.get("current_org", ""),
            gender=p.get("gender", ""),
            ethnicity=p.get("ethnicity", ""),
            birth=p.get("birth", ""),
            source=p.get("source", ""),
        )
    for o in ORGANIZATIONS:
        builder.add_organization(
            id=oid(o["id"]) + 100000,
            name=o.get("name", ""),
            org_type=o.get("type", ""),
            level=o.get("level", ""),
            location=o.get("location", ""),
        )
    for r in RELATIONSHIPS:
        builder.add_relationship(
            source=r["person_a"],
            target=r["person_b"],
            rel_type=r.get("type", ""),
            context=r.get("context", ""),
            overlap_org=r.get("overlap_org", ""),
            overlap_period=r.get("overlap_period", ""),
        )
    builder.write(gexf_path)
    logger.info("GEXF ready: %s", gexf_path)


if __name__ == "__main__":
    main()
