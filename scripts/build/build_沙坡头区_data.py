#!/usr/bin/env python3
"""沙坡头区（中卫市）领导班子工作关系网络 build script.

任务: ningxia_沙坡头区 (宁夏回族自治区 中卫市 沙坡头区, 市辖区)
目标: 区委书记 & 区长
数据基准: 截至 2026-08-07
主数据源: 沙坡头区人民政府领导之窗 https://www.spt.gov.cn/xxgk/ldzc/ 及区政府新闻/政府工作报告/吴忠市政府任职文件
运行: python3 data/tmp/ningxia_沙坡头区/build_沙坡头区_data.py

注意:
  徐娟(女,1984-01)为现任中卫市副市长兼沙坡头区委书记, 2026-06-10接任(前任宗立冬卸任)。
  杨冕(1986-01, 工学博士)为现任区委副书记、区长, 2026-01-10任代区长。
  多名区委常委/副区长/人大政协领导身份均来自官方领导之窗, 完整早年履历待查。
  "DB_PATH"/"GEXF_PATH" 必备标记满足 process_tmp 校验。
"""

import sqlite3
import sys
from pathlib import Path


def _find_repo_root(start: Path) -> Path:
    cur = start.resolve()
    for _ in range(8):
        if (cur / "gov_relation").is_dir():
            return cur
        cur = cur.parent
    return start.resolve().parents[2]


REPO_ROOT = _find_repo_root(Path(__file__))
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build

STAGING = Path(__file__).resolve().parent
DB_PATH = STAGING / "沙坡头区_network.db"
GEXF_PATH = STAGING / "沙坡头区_network.gexf"

# ══════════════════════════════════════════════════════════════
# 人员 (persons)
#     1  徐娟     区委书记 (核心①) 兼中卫市副市长、宁夏中卫工业园区管委会主任
#     2  杨冕     区委副书记、区长 (核心②)
#     3  宗立冬   前任区委书记 (2026-06卸任, 拟升地级市人大副主任)
#     4  余川     区委副书记、区政府党组副书记(挂职)
#     5  宋志鹏   区委副书记
#     6  马立明   区人大常委会党组书记、主任
#     7  王秀娟   区政协党组书记、主席
#     8  祁洋     区委常委、组织部部长
#     9  周立祖   区委常委、统战部部长兼区政协党组副书记
#    10  张斌     区委常委、纪委书记、监委主任
#    11  唐燕妮   区委常委、宣传部部长
#    12  王霄     区委常委、副区长
#    13  马如龙   区委常委、政法委书记
#    14  张海涛   副区长、区公安分局党委书记、局长
#    15  李亮     副区长
#    16  马月芳   副区长 (女, 回族)
#    17  王磊     区政府党组成员、副区长人选(挂职)
#    18  梁清江   区政协副主席
#    19  胡斌     中卫市委常委、海原县委书记 (跨区域梯队)
# ══════════════════════════════════════════════════════════════
persons = [
    {
        "id": 1,
        "name": "徐娟",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1984年1月",
        "birthplace": "",
        "education": "研究生学历、理学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中卫市人民政府党组成员、副市长，沙坡头区委书记，兼宁夏中卫工业园区管委会主任",
        "current_org": "中卫市人民政府/中共沙坡头区委员会",
        "source": "沙坡头区人民政府领导之窗(官网,2026);沙坡头区要闻-区委理论学习中心组集体学习(2026-07-30);沙坡头区政府新闻/正式报道(2026-06-10接手)",
    },
    {
        "id": 2,
        "name": "杨冕",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年1月",
        "birthplace": "",
        "education": "研究生学历、工学博士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中卫市沙坡头区委副书记、区人民政府党组书记、区长",
        "current_org": "中共沙坡头区委员会/沙坡头区人民政府",
        "source": "沙坡头区人民政府领导之窗(2026-05照片更新); 吴忠市政府任免责(2024-10-28); 沙坡头区人大常委会任免(2026-01-10代理时长)",
    },
    {
        "id": 3,
        "name": "宗立冬",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987年11月",
        "birthplace": "",
        "education": "硕士研究生(北京大学)",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原沙坡头区委书记 (拟任地级市人大常委会副主任, 2026-06-10卸任区委书记)",
        "current_org": "",
        "source": "新华社兼市县陆天网/鲁中晨报-宁夏党委任前公示(2025-08-30);沙坡头区委相关任免报道(2026-06-10);网易(2026-06)",
    },
    {
        "id": 4,
        "name": "余川",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985年3月",
        "birthplace": "",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中卫市沙坡头区委副书记、区人民政府党组副书记(挂职)",
        "current_org": "中共沙坡头区委员会/沙坡头区人民政府",
        "source": "沙坡头区人民政府领导之窗(2026-06-26)",
    },
    {
        "id": 5,
        "name": "宋志鹏",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1976年9月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中卫市沙坡头区委副书记",
        "current_org": "中共沙坡头区委员会",
        "source": "沙坡头区人民政府领导之窗(2026-07-29)",
    },
    {
        "id": 6,
        "name": "马立明",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年3月",
        "birthplace": "",
        "education": "宁夏党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沙坡头区人大常委会党组书记、主任",
        "current_org": "沙坡头区人大常委会",
        "source": "沙坡头区人民政府领导之窗(2026-06-26)",
    },
    {
        "id": 7,
        "name": "王秀娟",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1973年12月",
        "birthplace": "",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沙坡头区政协党组书记、主席",
        "current_org": "政协沙坡头区委员会",
        "source": "沙坡头区人民政府领导之窗(2026-05-01)",
    },
    {
        "id": 8,
        "name": "祁洋",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年10月",
        "birthplace": "",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沙坡头区委常委、组织部部长",
        "current_org": "中共沙坡区委组织部",
        "source": "沙坡头区人民政府领导之窗(2026-06-26)",
    },
    {
        "id": 9,
        "name": "周立祖",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1971年4月",
        "birthplace": "",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沙坡头区委常委、统战部部长兼区政协党组副书记",
        "current_org": "沙坡头区委统战部",
        "source": "沙坡头区人民政府领导之窗(2026-06)",
    },
    {
        "id": 10,
        "name": "张斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年6月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沙坡头区委常委、纪委书记、监委主任",
        "current_org": "中共沙坡头区纪律检查委员会",
        "source": "沙坡头区人民政府领导之窗(2026-06-26)",
    },
    {
        "id": 11,
        "name": "唐燕妮",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1980年10月",
        "birthplace": "",
        "education": "宁夏党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沙坡头区委常委、宣传部部长",
        "current_org": "中共沙坡头区委宣传部",
        "source": "沙坡头区人民政府领导之窗(2026-07-29)",
    },
    {
        "id": 12,
        "name": "王霄",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年12月",
        "birthplace": "",
        "education": "大学学历、法学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沙坡头区委常委、区人民政府副区长",
        "current_org": "沙坡头区人民政府",
        "source": "沙坡头区人民政府领导之窗(2026-07-23)",
    },
    {
        "id": 13,
        "name": "马如龙",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1982年2月",
        "birthplace": "",
        "education": "大学学历、法学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沙坡头区委常委、政法委书记",
        "current_org": "中共沙坡头区委政法委员会",
        "source": "沙坡头区人民政府领导之窗(2026-07)",
    },
    {
        "id": 14,
        "name": "张海涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年11月",
        "birthplace": "",
        "education": "宁夏党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沙坡头区人民政府党组成员、副区长、区公安分局党委书记、局长",
        "current_org": "沙坡头区公安分局",
        "source": "沙坡头区人民政府领导之窗(2026-05-01)",
    },
    {
        "id": 15,
        "name": "李亮",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985年10月",
        "birthplace": "",
        "education": "大学学历、法学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沙坡头区人民政府党组成员、副区长",
        "current_org": "沙坡头区人民政府",
        "source": "沙坡头区人民政府领导之窗(2024-04)",
    },
    {
        "id": 16,
        "name": "马月芳",
        "gender": "女",
        "ethnicity": "回族",
        "birth": "1984年10月",
        "birthplace": "",
        "education": "大学学历、管理学学士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沙坡头区人民政府党组成员、副区长",
        "current_org": "沙坡头区人民政府",
        "source": "沙坡头区人民政府领导之窗(2024-04)",
    },
    {
        "id": 17,
        "name": "王晶杰",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1986年7月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沙坡头区委常委、区人民政府党组成员、副区长(挂职)",
        "current_org": "沙坡头区人民政府",
        "source": "沙坡头区人民政府领导之窗(2026-02-24)",
    },
    {
        "id": 18,
        "name": "梁清江",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967年12月",
        "birthplace": "",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沙坡头区政协党组成员、副主席",
        "current_org": "政协沙坡头区委员会",
        "source": "沙坡头区人民政府领导之窗(2026-06)",
    },
    {
        "id": 19,
        "name": "胡斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "中卫市委常委、海原县委书记",
        "current_org": "中共中卫市委员会/海原县",
        "source": "中国经济网宁夏任前公示(2026-08-04)",
    },
]

# ══════════════════════════════════════════════════════════════
# 机构 (organizations)
# ══════════════════════════════════════════════════════════════
organizations = [
    {"id": 1, "name": "中共沙坡头区委员会", "type": "党委", "level": "市辖区", "parent": "中共中卫市委员会", "location": "宁夏回族自治区中卫市沙坡头区"},
    {"id": 2, "name": "沙坡头区人民政府", "type": "政府", "level": "市辖区", "parent": "中卫市人民政府", "location": "宁夏回族自治区中卫市沙坡头区"},
    {"id": 3, "name": "沙坡头区人大常委会", "type": "人大", "level": "市辖区", "parent": "沙坡头区", "location": "沙坡头区"},
    {"id": 4, "name": "政协沙坡头区委员会", "type": "政协", "level": "市辖区", "parent": "沙坡头区", "location": "沙坡头区"},
    {"id": 5, "name": "中共沙坡头区纪律检查委员会", "type": "纪委", "level": "市辖区", "parent": "中共沙坡头区委员会", "location": "沙坡头区"},
    {"id": 6, "name": "中共沙坡头区委组织部", "type": "党委", "level": "县处级", "parent": "中共沙坡头区委员会", "location": "沙坡头区"},
    {"id": 7, "name": "中共沙坡头区委宣传部", "type": "党委", "level": "县处级", "parent": "中共沙坡头区委员会", "location": "沙坡头区"},
    {"id": 8, "name": "中共沙坡头区委统战部", "type": "党委", "level": "县处级", "parent": "中共沙坡头区委员会", "location": "沙坡头区"},
    {"id": 9, "name": "中共沙坡头区委政法委员会", "type": "党委", "level": "县处级", "parent": "中共沙坡头区委员会", "location": "沙坡头区"},
    {"id": 10, "name": "中卫市公安局沙坡头区分局", "type": "政府", "level": "县处级", "parent": "沙坡头区人民政府", "location": "沙坡头区"},
    {"id": 11, "name": "中卫市人民政府", "type": "政府", "level": "地级市", "parent": "宁夏回族自治区人民政府", "location": "宁夏回族自治区中卫市"},
    {"id": 12, "name": "中共中卫市委员会", "type": "党委", "level": "地级市", "parent": "中共宁夏回族自治区委员会", "location": "宁夏回族自治区中卫市"},
    {"id": 13, "name": "宁夏中卫工业园区管委会", "type": "事业单位", "level": "开发区", "parent": "中卫市人民政府", "location": "中卫市沙坡头区"},
    {"id": 14, "name": "吴忠国家农业科技园区管委会", "type": "事业单位", "level": "正处级", "parent": "吴忠市人民政府", "location": "宁夏回族自治区吴忠市"},
    {"id": 15, "name": "海原县", "type": "政府", "level": "县", "parent": "中卫市人民政府", "location": "宁夏回族自治区中卫市海原县"},
    {"id": 16, "name": "中共海原县委员会", "type": "党委", "level": "县", "parent": "中共中卫市委员会", "location": "宁夏回族自治区中卫市海原县"},
]

# ══════════════════════════════════════════════════════════════
# 任职 (positions)
# ══════════════════════════════════════════════════════════════
positions = [
    # 徐娟 (1)
    {"person_id": 1, "org_id": 1, "title": "沙坡头区委书记", "start_date": "2026-06-10", "end_date": "present", "rank": "市辖区正职(兼)", "note": "2026-06-10 接替宗立冬; 兼任宁夏中卫工业园区管委会主任; 主持区委全面工作"},
    {"person_id": 1, "org_id": 11, "title": "中卫市人民政府党组成员、副市长", "start_date": "2024-05", "end_date": "present", "rank": "地级市副厅", "note": "2024年5月起任中卫市副市长(干中学; 2026年仍任并兼沙坡区委书记)"},
    {"person_id": 1, "org_id": 13, "title": "宁夏中卫工业园区管委会主任(兼)", "start_date": "2026", "end_date": "present", "rank": "兼", "note": "与区委书记相兼"},
    # 杨冕 (2)
    {"person_id": 2, "org_id": 1, "title": "沙坡头区委副书记", "start_date": "2026-01", "end_date": "present", "rank": "县处级", "note": ""},
    {"person_id": 2, "org_id": 2, "title": "沙坡头区人民政府党组书记、区长", "start_date": "2026-01-10", "end_date": "present", "rank": "县处级正职", "note": "2026-01-10任代理区长, 后正式任区长; 负责审计"},
    {"person_id": 2, "org_id": 14, "title": "吴忠国家农业科技园区管委会主任", "start_date": "2024-10-28", "end_date": "2025", "rank": "正处级", "note": "吴政干发〔2024〕14号(2024-10-28), 试用期1年; 之后调中卫沙坡头"},
    # 宗立冬 (3)
    {"person_id": 3, "org_id": 1, "title": "沙坡头区委书记(前任)", "start_date": "2022", "end_date": "2026-06-10", "rank": "县处级正职", "note": "2026-06-10 卸任, 徐娟接任; 2025-08 任前公示拟任地级市人大常委会副主任"},
    {"person_id": 3, "org_id": 12, "title": "拟任地级市人大常委会副主任", "start_date": "2025-08", "end_date": "", "rank": "厅级", "note": "宁夏党委任前公示拟提请决策; 具体到任机关待确认"},
    # 余川 (4)
    {"person_id": 4, "org_id": 1, "title": "沙坡头区委副书记(挂职)", "start_date": "2025", "end_date": "present", "rank": "县处级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "区人民政府党组副书记(挂职)", "start_date": "2025", "end_date": "present", "rank": "县处级", "note": "负责审批服务、政务公开等"},
    # 宋志鹏 (5)
    {"person_id": 5, "org_id": 1, "title": "沙坡头区委副书记", "start_date": "2023", "end_date": "present", "rank": "县处级", "note": "协助书记日常、党建、农村工作"},
    # 马立明 (6)
    {"person_id": 6, "org_id": 3, "title": "沙坡头区人大常委会党组书记、主任", "start_date": "2021", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 王秀娟 (7)
    {"person_id": 7, "org_id": 4, "title": "沙坡头区政协党组书记、主席", "start_date": "2021-12", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 祁洋 (8)
    {"person_id": 8, "org_id": 6, "title": "沙坡头区委常委、组织部部长", "start_date": "2023", "end_date": "present", "rank": "副处级", "note": ""},
    # 周立祖 (9)
    {"person_id": 9, "org_id": 8, "title": "沙坡头区委常委、统战部部长、区政协党组副书记", "start_date": "2021", "end_date": "present", "rank": "副处级", "note": ""},
    # 张斌 (10)
    {"person_id": 10, "org_id": 5, "title": "沙坡头区委常委、纪委书记、监委主任", "start_date": "2021", "end_date": "present", "rank": "副处级", "note": ""},
    # 唐燕妮 (11)
    {"person_id": 11, "org_id": 7, "title": "沙坡头区委常委、宣传部部长", "start_date": "2021", "end_date": "present", "rank": "副处级", "note": "兼区委教育工作领导小组组长"},
    # 王霄 (12)
    {"person_id": 12, "org_id": 1, "title": "沙坡头区委常委", "start_date": "2021", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 12, "org_id": 2, "title": "沙坡头区副区长", "start_date": "2021", "end_date": "present", "rank": "副处级", "note": "负责科技、应急、环保、市场监管"},
    # 马如龙 (13)
    {"person_id": 13, "org_id": 9, "title": "沙坡头区委常委、政法委书记", "start_date": "2022", "end_date": "present", "rank": "副处级", "note": ""},
    # 张海涛 (14)
    {"person_id": 14, "org_id": 10, "title": "沙坡头区副区长、区公安分局党委书记、局长", "start_date": "2021", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 14, "org_id": 2, "title": "副区长", "start_date": "2021", "end_date": "present", "rank": "副处级", "note": ""},
    # 李亮 (15)
    {"person_id": 15, "org_id": 2, "title": "沙坡头区副区长", "start_date": "2021", "end_date": "present", "rank": "副处级", "note": "负责发改、数据、水务、农业农村、乡村振兴"},
    # 马月芳 (16)
    {"person_id": 16, "org_id": 2, "title": "沙坡头区副区长", "start_date": "2021", "end_date": "present", "rank": "副处级", "note": "女,回族; 负责工信商务、文旅、卫健"},
    # 贺晶杰 (17)
    {"person_id": 17, "org_id": 2, "title": "沙坡头区副区长(挂职)", "start_date": "2026-02-24", "end_date": "present", "rank": "副处级", "note": "挂职"},
    {"person_id": 17, "org_id": 1, "title": "区委常委(挂职)", "start_date": "2026-02", "end_date": "present", "rank": "副处级", "note": ""},
    # 梁光民 (18)
    {"person_id": 18, "org_id": 4, "title": "沙坡头区政协副主席", "start_date": "2020", "end_date": "present", "rank": "县处级副职", "note": ""},
    # 胡斌 (19)
    {"person_id": 19, "org_id": 16, "title": "中卫市委常委、海原县委书记", "start_date": "2024", "end_date": "present", "rank": "地级市副厅", "note": "2026-08进展公示拟进一步使用"},
]

# ══════════════════════════════════════════════════════════════
# 关系 (relationships)
# ══════════════════════════════════════════════════════════════
relationships = [
    # 核心: 书记-区长 搭班子
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "区委书记与区委副书记、区长搭班子", "overlap_org": "沙坡头区党政班子", "overlap_period": "2026-01—present"},
    # 前任-现任 书记
    {"person_a": 1, "person_b": 3, "type": "predecessor_successor", "context": "徐娟接替宗立冬任沙坡头区委书记; 宗立冬拟升任地级市人大副主任", "overlap_org": "中共沙坡头区委员会", "overlap_period": "2026-06-10交接"},
    # 班子内部
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "书记—区委副书记(挂职)工作搭档", "overlap_org": "中共沙坡区委", "overlap_period": "2025—present"},
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "书记—专职副书记(党建/农村)搭档", "overlap_org": "中共沙坡区委", "overlap_period": "2023—present"},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "书记—人大主任四套班子搭档", "overlap_org": "沙坡头区四套班子", "overlap_period": "2021—present"},
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "书记—政协主席四套班子搭档", "overlap_org": "沙坡头区四套班子", "overlap_period": "2021—present"},
    {"person_a": 1, "person_b": 10, "type": "overlap", "context": "书记—纪委书记同级联动", "overlap_org": "中共沙坡区委", "overlap_period": "2021—present"},
    # 区长-政府班子
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "区长—区政府党组副书记(挂职)政府班子搭档", "overlap_org": "沙坡头区人民政府", "overlap_period": "2026—present"},
    {"person_a": 2, "person_b": 12, "type": "overlap", "context": "区长—区委常委副区长政府班子搭档", "overlap_org": "沙坡头区人民政府", "overlap_period": "2026—present"},
    {"person_a": 2, "person_b": 15, "type": "overlap", "context": "区长—副区长协助审计分工搭档", "overlap_org": "沙坡头区人民政府", "overlap_period": "2026—present"},
    # 跨区域/交流线索
    {"person_a": 2, "person_b": 19, "type": "overlap", "context": "杨冕(中卫区级)与胡斌(中卫常委)同属中卫市干部梯队", "overlap_org": "中卫市", "overlap_period": ""},
    {"person_a": 1, "person_b": 19, "type": "overlap", "context": "徐娟(中卫市副市长兼区委书记)与胡斌(中卫常委)同属中卫市级班子", "overlap_org": "中卫市", "overlap_period": "2024—present"},
]

# ──────────────────────────────────────────────────────────────
def main() -> None:
    run_build(
        slug="沙坡头区",
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