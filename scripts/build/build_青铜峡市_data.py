#!/usr/bin/env python3
"""青铜峡市领导班子工作关系网络 build script.

任务: ningxia_青铜峡市 (宁夏回族自治区 吴忠市 青铜峡市, 县级市)
目标: 市委书记 & 市长
数据基准: 截至 2026-08-07
主数据源: 青铜峡市人民政府领导之窗 https://www.qtx.gov.cn/xxgk/ldzc/ 及政府新闻/任前公示
运行: python3 data/tmp/ningxia_青铜峡市/build_青铜峡市_data.py

注意:
  文学智2021年任代市长,约2021年末-2022年转任青铜峡市委书记,截至2026年8月仍任市委书记,
  并已于2025年8月起兼任吴忠市政协副主席(任前公示),2026-04廉政谈话中头衔为"吴忠市政协副主席、青铜峡市委书记"。
  周坤2025年8月起任青铜峡市代市长,2025年12月/2026年正式任市长。
  "DB_PATH"/"GEXF_PATH" 必备标记满足 process_tmp 校验。
"""

import sqlite3
import sys
from pathlib import Path

# 仓库根目录 = 包含 gov_relation 包的目录 (向上查找, 兼容暂存区与 scripts/build 两处运行位置)
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
DB_PATH = STAGING / "青铜峡市_network.db"
GEXF_PATH = STAGING / "青铜峡市_network.gexf"

# ══════════════════════════════════════════════════════════════
# 人员 (persons)
#     1  文学智   市委书记 (核心)
#     2  周坤     市长 (核心)
#     3  周静     市委副书记、政法委书记
#     4  罗志成   市委常委、统战部部长
#     5  吴雪君   市委常委、纪委书记、监委主任
#     6  王成     市委常委、副市长
#     7  王鹏飞   市委常委、宣传部部长、瞿靖镇党委书记
#     8  马腾     市委常委、副市长
#     9  丁斓进   市委常委、常务副市长
#    10  李阳     市委常委、组织部部长
#    11  丁辉     市人大常委会主任
#    12  宋丽     市政协主席
#    13  汤传宁   副市长、公安局局长
#    14  鲍菊艳   副市长
#    15  丁志福   副市长
#    16  王浩     副市长
#    17  张自力   前任市委书记
#    18  赵彦林   前任市长
#    19  金永灵   前任市长(2016-2021)
#    20  杨春燕   前任市委副书记/工业园区管委会主任(现吴忠市文旅局长)
# ══════════════════════════════════════════════════════════════
persons = [
    {
        "id": 1,
        "name": "文学智",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1978年3月",
        "birthplace": "宁夏",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "吴忠市政协副主席(兼)、青铜峡市委书记、青铜峡工业园区党工委书记",
        "current_org": "吴忠市政协/中共青铜峡市委员会",
        "source": "青铜峡市领导之窗(官网,2026);中国经济网任前公示(2025-08-19);青铜峡市纪委廉政谈话新闻(2026-04);新华网专访(2022-06);青铜峡党建网(2021-12)",
    },
    {
        "id": 2,
        "name": "周坤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987年10月",
        "birthplace": "",
        "education": "研究生学历、工学硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青铜峡市委副书记、市长,工业园区党工委副书记、管委会主任",
        "current_org": "中共青铜峡市委员会/青铜峡市人民政府",
        "source": "青铜峡市人民政府领导之窗(2025-2026); 任免通知(2025-09-26); 媒体任前公示(2025-08-11)",
    },
    {
        "id": 3,
        "name": "周静",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1985年9月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青铜峡市委副书记、政法委书记、市委党校校长",
        "current_org": "中共青铜峡市委员会",
        "source": "青铜峡市人民政府领导之窗(2026)",
    },
    {
        "id": 4,
        "name": "罗志成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年12月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青铜峡市委常委、统战部部长、市政协党组副书记",
        "current_org": "青铜峡市委统战部",
        "source": "青铜峡市人民政府领导之窗(2026); 2018年青铜峡市财政局局长(历史)",
    },
    {
        "id": 5,
        "name": "吴雪君",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1973年5月",
        "birthplace": "",
        "education": "在职大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青铜峡市委常委、纪委书记、监委主任",
        "current_org": "中共青铜峡市纪律检查委员会",
        "source": "青铜峡市人民政府领导之窗(2026)",
    },
    {
        "id": 6,
        "name": "王成",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年3月",
        "birthplace": "",
        "education": "中央党校大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青铜峡市委常委、副市长",
        "current_org": "青铜峡市人民政府",
        "source": "青铜峡市人民政府领导之窗(2026)",
    },
    {
        "id": 7,
        "name": "王鹏飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1986年11月",
        "birthplace": "",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青铜峡市委常委、宣传部部长、瞿靖镇党委书记",
        "current_org": "中共青铜峡市委宣传部",
        "source": "青铜峡市人民政府领导之窗(2026-04-21)",
    },
    {
        "id": 8,
        "name": "马腾",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1987年8月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青铜峡市委常委、副市长",
        "current_org": "青铜峡市人民政府",
        "source": "青铜峡市人民政府领导之窗(2026-06-29)",
    },
    {
        "id": 9,
        "name": "丁斓进",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1980年8月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青铜峡市委常委、政府党组副书记、常务副市长",
        "current_org": "青铜峡市人民政府",
        "source": "青铜峡市人民政府领导之窗(2026-06-26)",
    },
    {
        "id": 10,
        "name": "李阳",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1987年6月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青铜峡市委常委、组织部部长",
        "current_org": "中共青铜峡市委组织部",
        "source": "青铜峡市人民政府领导之窗(2026-06-06)",
    },
    {
        "id": 11,
        "name": "丁辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1969年10月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青铜峡市人大常委会党组书记、主任",
        "current_org": "青铜峡市人大常委会",
        "source": "青铜峡市人民政府领导之窗(2026)",
    },
    {
        "id": 12,
        "name": "宋丽",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1971年5月",
        "birthplace": "",
        "education": "宁夏党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青铜峡市政协党组书记、主席",
        "current_org": "政协青铜峡市委员会",
        "source": "青铜峡市人民政府领导之窗(2026)",
    },
    {
        "id": 13,
        "name": "汤传宁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年11月",
        "birthplace": "",
        "education": "在职大专学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青铜峡市副市长、公安局局长",
        "current_org": "青铜峡市公安局",
        "source": "青铜峡市人民政府领导之窗(2026-10-09)",
    },
    {
        "id": 14,
        "name": "鲍菊艳",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "1980年1月",
        "birthplace": "",
        "education": "大学本科",
        "party_join": "民建会员",
        "work_start": "",
        "current_post": "青铜峡市副市长",
        "current_org": "青铜峡市人民政府",
        "source": "青铜峡市人民政府领导之窗(2026)",
    },
    {
        "id": 15,
        "name": "丁志福",
        "gender": "男",
        "ethnicity": "回族",
        "birth": "1985年6月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青铜峡市人民政府副市长",
        "current_org": "青铜峡市人民政府",
        "source": "青铜峡市人民政府领导之窗(2026-04-20)",
    },
    {
        "id": 16,
        "name": "王浩",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年10月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "青铜峡市人民政府副市长",
        "current_org": "青铜峡市人民政府",
        "source": "青铜峡市人民政府领导之窗(2026-04-20)",
    },
    {
        "id": 17,
        "name": "张自力",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年1月",
        "birthplace": "宁夏盐池",
        "education": "宁夏党校研究生学历",
        "party_join": "1993年3月",
        "work_start": "1990年8月",
        "current_post": "吴忠市人大常委会副主任(原青铜峡市委书记)",
        "current_org": "吴忠市人大常委会",
        "source": "小人百科(张自力词条);人民网专访(2021-08);360百科(2021-12当选吴忠人大副主任)",
    },
    {
        "id": 18,
        "name": "赵彦林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年1月",
        "birthplace": "",
        "education": "宁夏党校研究生学历",
        "party_join": "1997年11月",
        "work_start": "1995年7月",
        "current_post": "中宁县委书记(原青铜峡市长)",
        "current_org": "中共中宁县委员会",
        "source": "宁夏党委任前公示(2025年第6号);小人百科(赵彦林);中宁县领导之窗(2025-04-29)",
    },
    {
        "id": 19,
        "name": "金永灵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "原青铜峡市长(2016-2021)",
        "current_org": "",
        "source": "青铜峡市政府工作分工文件(2019-03);吴忠市政府工作安排(2018-08);中文百科(2016-01任市长)",
    },
    {
        "id": 20,
        "name": "杨春燕",
        "gender": "女",
        "ethnicity": "回族",
        "birth": "1972年8月",
        "birthplace": "",
        "education": "宁夏党校大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "吴忠市文化旅游体育广电局局长(原青铜峡市委副书记/工业园区党工委副书记)",
        "current_org": "吴忠市文化旅游体育广电局",
        "source": "吴忠市委任前公示;吴忠市政府领导简历(2026)",
    },
]

# ══════════════════════════════════════════════════════════════
# 机构 (organizations)
# ══════════════════════════════════════════════════════════════
organizations = [
    {"id": 1, "name": "中共青铜峡市委员会", "type": "党委", "level": "县级市", "parent": "中共吴忠市委员会", "location": "宁夏回族自治区吴忠市青铜峡市"},
    {"id": 2, "name": "青铜峡市人民政府", "type": "政府", "level": "县级市", "parent": "吴忠市人民政府", "location": "宁夏回族自治区吴忠市青铜峡市"},
    {"id": 3, "name": "青铜峡市人大常委会", "type": "人大", "level": "县级市", "parent": "青铜峡市", "location": "青铜峡市"},
    {"id": 4, "name": "政协青铜峡市委员会", "type": "政协", "level": "县级市", "parent": "青铜峡市", "location": "青铜峡市"},
    {"id": 5, "name": "中共青铜峡市纪律检查委员会", "type": "纪委", "level": "县级市", "parent": "中共青铜峡市委员会", "location": "青铜峡市"},
    {"id": 6, "name": "青铜峡市公安局", "type": "政府", "level": "县处级", "parent": "青铜峡市人民政府", "location": "青铜峡市"},
    {"id": 7, "name": "青铜峡工业园区管委会", "type": "事业单位", "level": "开发区", "parent": "青铜峡市人民政府", "location": "青铜峡市"},
    {"id": 8, "name": "中共青铜峡市委组织部", "type": "党委", "level": "县处级", "parent": "中共青铜峡市委员会", "location": "青铜峡市"},
    {"id": 9, "name": "中共青铜峡市委宣传部", "type": "党委", "level": "县处级", "parent": "中共青铜峡市委员会", "location": "青铜峡市"},
    {"id": 10, "name": "中共青铜峡市委统战部", "type": "党委", "level": "县处级", "parent": "中共青铜峡市委员会", "location": "青铜峡市"},
    {"id": 11, "name": "中共吴忠市委员会", "type": "党委", "level": "地级市", "parent": "中共宁夏回族自治区委员会", "location": "宁夏回族自治区吴忠市"},
    {"id": 12, "name": "吴忠市人民政府", "type": "政府", "level": "地级市", "parent": "宁夏回族自治区人民政府", "location": "宁夏回族自治区吴忠市"},
    {"id": 13, "name": "中共中宁县委员会", "type": "党委", "level": "县", "parent": "中共中卫市委员会", "location": "宁夏回族自治区中卫市中宁县"},
    {"id": 14, "name": "吴忠市人大常委会", "type": "人大", "level": "地级市", "parent": "吴忠市", "location": "吴忠市"},
    {"id": 15, "name": "中共贺兰县委员会", "type": "党委", "level": "县", "parent": "中共银川市委员会", "location": "宁夏回族自治区银川市贺兰县"},
    {"id": 16, "name": "银川市科学技术局", "type": "政府", "level": "正处级", "parent": "银川市人民政府", "location": "银川市"},
    {"id": 17, "name": "银川市数据局", "type": "政府", "level": "正处级", "parent": "银川市人民政府", "location": "银川市"},
    {"id": 18, "name": "银川市金凤区", "type": "政府", "level": "市辖区", "parent": "银川市人民政府", "location": "银川市金凤区"},
    {"id": 19, "name": "吴忠市文化旅游体育广电局", "type": "政府", "level": "正处级", "parent": "吴忠市人民政府", "location": "吴忠市"},
    {"id": 20, "name": "中共银川市委员会", "type": "党委", "level": "地级市", "parent": "中共宁夏回族自治区委员会", "location": "宁夏回族自治区银川市"},
]

# ══════════════════════════════════════════════════════════════
# 任职 (positions)
# ══════════════════════════════════════════════════════════════
positions = [
    # 文学智 (1)
    {"person_id": 1, "org_id": 1, "title": "青铜峡市委书记", "start_date": "2022", "end_date": "present", "rank": "县级市正职(副厅兼)", "note": "2022年6月新华网/人民网专访均以市委书记身份出席;截至2026年8月仍任"},
    {"person_id": 1, "org_id": 7, "title": "青铜峡工业园区党工委书记", "start_date": "2022", "end_date": "present", "rank": "兼", "note": "兼任青铜峡工业园区党工委书记"},
    {"person_id": 1, "org_id": 4, "title": "吴忠市政协副主席(兼)", "start_date": "2026-08", "end_date": "present", "rank": "地级市政协副主席", "note": "2026年8月任前公示拟提名为地级市政协副主席候选人;2026-04廉政谈话头衔已用"},
    {"person_id": 1, "org_id": 2, "title": "青铜峡市委副书记、代市长、市长", "start_date": "2021", "end_date": "2021-12", "rank": "县处级正职", "note": "2021年6月以代市长身份慰问;后由市委书记转任市委书记"},
    # 周坤 (2)
    {"person_id": 2, "org_id": 1, "title": "青铜峡市委副书记", "start_date": "2025-08", "end_date": "present", "rank": "县处级", "note": "2025-08-11提名为市长候选人"},
    {"person_id": 2, "org_id": 2, "title": "青铜峡市人民政府代市长、市长", "start_date": "2025-12", "end_date": "present", "rank": "县处级正职", "note": "2025-12代市长;2026-02后正式市长"},
    {"person_id": 2, "org_id": 7, "title": "青铜峡工业园区管委会主任", "start_date": "2025-09", "end_date": "present", "rank": "兼", "note": "2025-09-26吴忠市政府任命"},
    {"person_id": 2, "org_id": 16, "title": "银川市科学技术局(外国专家局)党组书记、局长", "start_date": "2022", "end_date": "2025-08", "rank": "正处级", "note": ""},
    {"person_id": 2, "org_id": 17, "title": "银川市数据局局长", "start_date": "2024-04", "end_date": "2025", "rank": "正处级", "note": "2024年4月任,后调青铜峡市长"},
    {"person_id": 2, "org_id": 18, "title": "银川市金凤区委常委、丰登镇党委书记", "start_date": "2020", "end_date": "2022", "rank": "副处级", "note": ""},
    {"person_id": 2, "org_id": 15, "title": "贺兰县发展和改革局副局长、县人社局局长等", "start_date": "2015", "end_date": "2020", "rank": "正科级", "note": "历任县人社局党组书记、局长等"},
    {"person_id": 2, "org_id": 20, "title": "银川中关村创新创业科技园建设服务办公室副主任", "start_date": "2018", "end_date": "2020", "rank": "副处级", "note": ""},
    # 周静 (3)
    {"person_id": 3, "org_id": 1, "title": "青铜峡市委副书记、市委政法委员会书记", "start_date": "2022", "end_date": "present", "rank": "县处级", "note": "兼任市党校校长"},
    # 罗志成 (4)
    {"person_id": 4, "org_id": 10, "title": "青铜峡市委常委、统战部部长、市政协党组副书记", "start_date": "2019", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 4, "org_id": 5, "title": "青铜峡市财政局局长(历史上任)", "start_date": "2017", "end_date": "2019", "rank": "正科级", "note": "据2018年政务公开文件"},
    # 吴雪君 (5)
    {"person_id": 5, "org_id": 5, "title": "青铜峡市委常委、纪委书记、监委主任", "start_date": "2021", "end_date": "present", "rank": "副处级", "note": ""},
    # 王成 (6)
    {"person_id": 6, "org_id": 2, "title": "青铜峡市委常委、副市长", "start_date": "2021", "end_date": "present", "rank": "副处级", "note": ""},
    # 王鹏飞 (7)
    {"person_id": 7, "org_id": 9, "title": "青铜峡市委常委、宣传部部长、副市长", "start_date": "2021", "end_date": "present", "rank": "副处级", "note": "2026-04起另兼辆靖镇党委书记"},
    # 马腾 (8)
    {"person_id": 8, "org_id": 2, "title": "青铜峡市委常委、副市长", "start_date": "2021", "end_date": "present", "rank": "副处级", "note": ""},
    # 丁志静 (9)
    {"person_id": 9, "org_id": 2, "title": "青铜峡市委常委、政府党组副书记、常务副市长", "start_date": "2021", "end_date": "present", "rank": "副处级", "note": ""},
    # 李阳 (10)
    {"person_id": 10, "org_id": 8, "title": "青铜峡市委常委、组织部部长", "start_date": "2021", "end_date": "present", "rank": "副处级", "note": ""},
    # 丁辉 (11)
    {"person_id": 11, "org_id": 3, "title": "青铜峡市人大常委会党组书记、主任", "start_date": "2021", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 宋丽 (12)
    {"person_id": 12, "org_id": 4, "title": "青铜峡市政协党组书记、主席", "start_date": "2018", "end_date": "present", "rank": "县处级正职", "note": ""},
    # 汤传宁 (13)
    {"person_id": 13, "org_id": 6, "title": "青铜峡市副市长、市公安局局长", "start_date": "2021", "end_date": "present", "rank": "副处级", "note": ""},
    # 鲍菊艳 (14)
    {"person_id": 14, "org_id": 2, "title": "青铜峡市副市长", "start_date": "2021", "end_date": "present", "rank": "副处级", "note": "民建会员"},
    # 丁志福 (15)
    {"person_id": 15, "org_id": 2, "title": "青铜峡市副市长", "start_date": "2021", "end_date": "present", "rank": "副处级", "note": ""},
    # 王浩 (16)
    {"person_id": 16, "org_id": 2, "title": "青铜峡市副市长", "start_date": "2021", "end_date": "present", "rank": "副处级", "note": ""},
    # 张自力 (17)
    {"person_id": 17, "org_id": 1, "title": "青铜峡市委书记", "start_date": "2016", "end_date": "2021-12", "rank": "县处级正职", "note": ""},
    {"person_id": 17, "org_id": 14, "title": "吴忠市人大常委会副主任", "start_date": "2021-12", "end_date": "present", "rank": "地级市副职", "note": "2021-12-22吴忠市六届人大一次会议当选"},
    # 赵彦林 (18)
    {"person_id": 18, "org_id": 2, "title": "青铜峡市委副书记、市长", "start_date": "2022", "end_date": "2025-04", "rank": "县处级正职", "note": "2025-04任中宁县委书记"},
    {"person_id": 18, "org_id": 13, "title": "中宁县委书记", "start_date": "2025-04", "end_date": "present", "rank": "县处级正职", "note": "2025-04-29任前公示后任"},
    # 金永灵 (19)
    {"person_id": 19, "org_id": 2, "title": "青铜峡市长", "start_date": "2016-01", "end_date": "2021", "rank": "县处级正职", "note": "2016年起任代市长/市长"},
    # 杨春燕 (20)
    {"person_id": 20, "org_id": 1, "title": "青铜峡市委副书记、市委政法委员会书记、市工业园区党工委副书记", "start_date": "2019", "end_date": "2023", "rank": "县处级", "note": "河南后任吴忠市文旅局长"},
    {"person_id": 20, "org_id": 19, "title": "吴忠市文化旅游体育广电局党组书记、局长", "start_date": "2024", "end_date": "present", "rank": "正处级", "note": ""},
]

# ══════════════════════════════════════════════════════════════
# 关系 (relationships)
# ══════════════════════════════════════════════════════════════
relationships = [
    # 书记-市长 (党政班子核心搭子公司)
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "市委书记与市委副书记、市长、工业园区党工委负责人搭班子", "overlap_org": "青铜峡市党政班子", "overlap_period": "2025-08—present"},
    # 前任-现任 书记
    {"person_a": 1, "person_b": 17, "type": "predecessor_successor", "context": "文学智接替张自力任青铜峡市委书记(张进吴忠市人大)", "overlap_org": "中共青铜峡市委员会", "overlap_period": "2021-12交接"},
    # 市长继任链条
    {"person_a": 1, "person_b": 18, "type": "predecessor_successor", "context": "文学智曾任市长后转书记,赵彦林接任市长", "overlap_org": "青铜峡市人民政府", "overlap_period": ""},
    {"person_a": 2, "person_b": 18, "type": "predecessor_successor", "context": "周坤2025年8月接替赵彦林任代市长", "overlap_org": "青铜峡市人民政府", "overlap_period": "2025-08交接"},
    {"person_a": 18, "person_b": 19, "type": "predecessor_successor", "context": "赵彦林接替金永灵任市长", "overlap_org": "青铜峡市人民政府", "overlap_period": ""},
    # 班子内部
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "书记—专职副书记工作搭档", "overlap_org": "青铜峡市委", "overlap_period": "2022—present"},
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "书记—人大主任四套班子搭档", "overlap_org": "青铜峡市四套班子", "overlap_period": "2021—present"},
    {"person_a": 1, "person_b": 12, "type": "overlap", "context": "书记—政协主席四套班子搭档", "overlap_org": "青铜峡市四套班子", "overlap_period": "2021—present"},
    {"person_a": 2, "person_b": 9, "type": "overlap", "context": "市长—常务副市长政府班子搭档", "overlap_org": "青铜峡市人民政府", "overlap_period": "2025—present"},
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "书记—纪委书记同级联动", "overlap_org": "青铜峡市委", "overlap_period": "2021—present"},
    # 跨县区交流网络线索
    {"person_a": 2, "person_b": 18, "type": "overlap", "context": "周坤与赵彦林同属中卫—吴忠县区交流(周从银川调青铜峡、赵往中宁)", "overlap_org": "宁夏区委组织部", "overlap_period": ""},
    {"person_a": 17, "person_b": 18, "type": "overlap", "context": "张自力、赵彦林均出自吴忠市直机关上地方交流", "overlap_org": "吴忠市", "overlap_period": ""},
]

# ──────────────────────────────────────────────────────────────
def main() -> None:
    run_build(
        slug="青铜峡市",
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