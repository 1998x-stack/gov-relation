#!/usr/bin/env python3
"""
彬州市领导班子关系网络数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

彬州市是陕西省咸阳市下辖的县级市，位于咸阳市西北部。
前身为彬县，2018年撤县设市。

数据来源：
- 彬州市人民政府官网 (www.snbinzhou.gov.cn) 领导之窗
- 官方新闻报道

采集日期：2026-07-25

当前领导：
  市委书记：陈加宝（1985年5月生）
  市长：尚小刚（1974年10月生）
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build

SLUG = "彬州市"
DATE = "2026-07-25"

# =========================================================================
# 人物数据
# =========================================================================
persons = [
    {
        "id": 1,
        "name": "陈加宝",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1985年5月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委书记",
        "current_org": "中共彬州市委",
        "source": "http://www.snbinzhou.gov.cn/zwgk/fdzdgknr/ldzc/swld/202406/t20240611_1776667.html",
        "confidence": "confirmed",
    },
    {
        "id": 2,
        "name": "尚小刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年10月",
        "birthplace": "",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记、市长",
        "current_org": "彬州市人民政府",
        "source": "http://www.snbinzhou.gov.cn/zwgk/fdzdgknr/ldzc/swld/202406/t20240611_1776666.html",
        "confidence": "confirmed",
    },
    {
        "id": 3,
        "name": "王斌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年6月",
        "birthplace": "",
        "education": "省委党校研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委副书记",
        "current_org": "中共彬州市委",
        "source": "http://www.snbinzhou.gov.cn/zwgk/fdzdgknr/ldzc/swld/202406/t20240611_1776665.html",
        "confidence": "confirmed",
    },
    {
        "id": 4,
        "name": "李军申",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年11月",
        "birthplace": "",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、常务副市长",
        "current_org": "彬州市人民政府",
        "source": "http://www.snbinzhou.gov.cn/zwgk/fdzdgknr/ldzc/swld/202406/t20240611_1776662.html",
        "confidence": "confirmed",
    },
    {
        "id": 5,
        "name": "郭嘉楠",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1984年9月",
        "birthplace": "",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、宣传部部长",
        "current_org": "中共彬州市委宣传部",
        "source": "http://www.snbinzhou.gov.cn/zwgk/fdzdgknr/ldzc/swld/202406/t20240611_1776661.html",
        "confidence": "confirmed",
    },
    {
        "id": 6,
        "name": "吕银河",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1973年8月",
        "birthplace": "",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、副市长",
        "current_org": "彬州市人民政府",
        "source": "http://www.snbinzhou.gov.cn/zwgk/fdzdgknr/ldzc/swld/202409/t20240903_1807428.html",
        "confidence": "confirmed",
    },
    {
        "id": 7,
        "name": "张明军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1979年3月",
        "birthplace": "",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、政法委书记",
        "current_org": "中共彬州市委政法委",
        "source": "http://www.snbinzhou.gov.cn/zwgk/fdzdgknr/ldzc/swld/202406/t20240611_1776660.html",
        "confidence": "confirmed",
    },
    {
        "id": 8,
        "name": "李剑",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年7月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、组织部部长",
        "current_org": "中共彬州市委组织部",
        "source": "http://www.snbinzhou.gov.cn/zwgk/fdzdgknr/ldzc/swld/202406/t20240611_1776658.html",
        "confidence": "confirmed",
    },
    {
        "id": 9,
        "name": "葛兵",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年12月",
        "birthplace": "",
        "education": "研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、纪委书记",
        "current_org": "中共彬州市纪委/市监委",
        "source": "http://www.snbinzhou.gov.cn/zwgk/fdzdgknr/ldzc/swld/202406/t20240611_1776663.html",
        "confidence": "confirmed",
    },
    {
        "id": 10,
        "name": "权海峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年7月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、人武部政委",
        "current_org": "彬州市人民武装部",
        "source": "http://www.snbinzhou.gov.cn/zwgk/fdzdgknr/ldzc/swld/202406/t20240611_1776664.html",
        "confidence": "confirmed",
    },
    {
        "id": 11,
        "name": "唐海岗",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1981年12月",
        "birthplace": "",
        "education": "在职研究生学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "市委常委、统战部部长",
        "current_org": "中共彬州市委统战部",
        "source": "http://www.snbinzhou.gov.cn/zwgk/fdzdgknr/ldzc/swld/202511/t20251128_2037379.html",
        "confidence": "confirmed",
    },
    {
        "id": 12,
        "name": "姜岗",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年12月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长、公安局局长",
        "current_org": "彬州市公安局",
        "source": "http://www.snbinzhou.gov.cn/zwgk/fdzdgknr/ldzc/zfld/202207/t20220705_787014.html",
        "confidence": "confirmed",
    },
    {
        "id": 13,
        "name": "伊丽娜",
        "gender": "女",
        "ethnicity": "维吾尔族",
        "birth": "1981年5月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "民建会员/中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "彬州市人民政府",
        "source": "http://www.snbinzhou.gov.cn/zwgk/fdzdgknr/ldzc/zfld/202301/t20230116_1586733.html",
        "confidence": "confirmed",
    },
    {
        "id": 14,
        "name": "赵亚鹏",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1974年11月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "彬州市人民政府",
        "source": "http://www.snbinzhou.gov.cn/zwgk/fdzdgknr/ldzc/zfld/202409/t20240903_1807392.html",
        "confidence": "confirmed",
    },
    {
        "id": 15,
        "name": "怀刚",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1980年8月",
        "birthplace": "",
        "education": "大学学历",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "彬州市人民政府",
        "source": "http://www.snbinzhou.gov.cn/zwgk/fdzdgknr/ldzc/zfld/202207/t20220705_787013.html",
        "confidence": "confirmed",
    },
]

# =========================================================================
# 组织数据
# =========================================================================
organizations = [
    {"id": 1, "name": "中共彬州市委", "type": "党委", "level": "县处级", "parent": "中共咸阳市委", "location": "陕西省咸阳市彬州市"},
    {"id": 2, "name": "彬州市人民政府", "type": "政府", "level": "县处级", "parent": "咸阳市人民政府", "location": "陕西省咸阳市彬州市"},
    {"id": 3, "name": "中共彬州市纪委/市监委", "type": "纪委", "level": "县处级", "parent": "中共彬州市委", "location": "陕西省咸阳市彬州市"},
    {"id": 4, "name": "中共彬州市委组织部", "type": "党委部门", "level": "正科级", "parent": "中共彬州市委", "location": "陕西省咸阳市彬州市"},
    {"id": 5, "name": "中共彬州市委宣传部", "type": "党委部门", "level": "正科级", "parent": "中共彬州市委", "location": "陕西省咸阳市彬州市"},
    {"id": 6, "name": "中共彬州市委统战部", "type": "党委部门", "level": "正科级", "parent": "中共彬州市委", "location": "陕西省咸阳市彬州市"},
    {"id": 7, "name": "中共彬州市委政法委", "type": "党委部门", "level": "正科级", "parent": "中共彬州市委", "location": "陕西省咸阳市彬州市"},
    {"id": 8, "name": "彬州市人民武装部", "type": "军事", "level": "县处级", "parent": "咸阳军分区", "location": "陕西省咸阳市彬州市"},
    {"id": 9, "name": "彬州市公安局", "type": "政府", "level": "正科级", "parent": "彬州市人民政府", "location": "陕西省咸阳市彬州市"},
]

# =========================================================================
# 任职数据
# =========================================================================
positions = [
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "未知", "end_date": "至今", "rank": "正县级", "note": "主持市委全面工作"},
    {"person_id": 2, "org_id": 1, "title": "市委副书记", "start_date": "未知", "end_date": "至今", "rank": "正县级", "note": "同时任市长"},
    {"person_id": 2, "org_id": 2, "title": "市长", "start_date": "未知", "end_date": "至今", "rank": "正县级", "note": "领导市政府全面工作"},
    {"person_id": 3, "org_id": 1, "title": "市委副书记", "start_date": "未知", "end_date": "至今", "rank": "副县级", "note": "协助书记抓党建，分管三农、群团"},
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start_date": "未知", "end_date": "至今", "rank": "副县级", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "常务副市长", "start_date": "未知", "end_date": "至今", "rank": "副县级", "note": "分管发改、应急、人社等"},
    {"person_id": 5, "org_id": 1, "title": "市委常委", "start_date": "未知", "end_date": "至今", "rank": "副县级", "note": ""},
    {"person_id": 5, "org_id": 5, "title": "宣传部部长", "start_date": "未知", "end_date": "至今", "rank": "副县级", "note": "分管宣传、意识形态、网信"},
    {"person_id": 6, "org_id": 1, "title": "市委常委", "start_date": "未知", "end_date": "至今", "rank": "副县级", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副市长", "start_date": "未知", "end_date": "至今", "rank": "副县级", "note": "分管工信、民政、交通、经开区"},
    {"person_id": 7, "org_id": 1, "title": "市委常委", "start_date": "未知", "end_date": "至今", "rank": "副县级", "note": ""},
    {"person_id": 7, "org_id": 7, "title": "政法委书记", "start_date": "未知", "end_date": "至今", "rank": "副县级", "note": "负责政法、平安建设、信访"},
    {"person_id": 8, "org_id": 1, "title": "市委常委", "start_date": "未知", "end_date": "至今", "rank": "副县级", "note": ""},
    {"person_id": 8, "org_id": 4, "title": "组织部部长", "start_date": "未知", "end_date": "至今", "rank": "副县级", "note": "负责组织工作"},
    {"person_id": 9, "org_id": 1, "title": "市委常委", "start_date": "未知", "end_date": "至今", "rank": "副县级", "note": ""},
    {"person_id": 9, "org_id": 3, "title": "纪委书记", "start_date": "未知", "end_date": "至今", "rank": "副县级", "note": "主持纪委监委工作"},
    {"person_id": 10, "org_id": 1, "title": "市委常委", "start_date": "未知", "end_date": "至今", "rank": "副县级", "note": ""},
    {"person_id": 10, "org_id": 8, "title": "人武部政委", "start_date": "未知", "end_date": "至今", "rank": "副县级", "note": "负责军事和人民武装"},
    {"person_id": 11, "org_id": 1, "title": "市委常委", "start_date": "未知", "end_date": "至今", "rank": "副县级", "note": ""},
    {"person_id": 11, "org_id": 6, "title": "统战部部长", "start_date": "未知", "end_date": "至今", "rank": "副县级", "note": "负责统一战线、民族宗教"},
    {"person_id": 12, "org_id": 9, "title": "副市长、公安局局长", "start_date": "未知", "end_date": "至今", "rank": "副县级", "note": "分管公安、司法、退役军人"},
    {"person_id": 13, "org_id": 2, "title": "副市长", "start_date": "未知", "end_date": "至今", "rank": "副县级", "note": "分管教育、文旅、卫健、医保"},
    {"person_id": 14, "org_id": 2, "title": "副市长", "start_date": "未知", "end_date": "至今", "rank": "副县级", "note": "分管自然资源、水利、农业农村"},
    {"person_id": 15, "org_id": 2, "title": "副市长", "start_date": "未知", "end_date": "至今", "rank": "副县级", "note": "分管科技、招商"},
]

# =========================================================================
# 关系数据
# =========================================================================
relationships = [
    # 党政一把手
    {"person_a": 1, "person_b": 2, "type": "搭档", "context": "市委书记与市长——党政一把手搭档工作", "overlap_org": "中共彬州市委/彬州市人民政府", "overlap_period": "至今"},
    # 书记与市委常委
    {"person_a": 1, "person_b": 3, "type": "上下级", "context": "市委书记与专职副书记", "overlap_org": "中共彬州市委", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "市委书记与常务副市长", "overlap_org": "中共彬州市委", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 5, "type": "上下级", "context": "市委书记与宣传部部长", "overlap_org": "中共彬州市委", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 6, "type": "上下级", "context": "市委书记与副市长吕银河", "overlap_org": "中共彬州市委", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 7, "type": "上下级", "context": "市委书记与政法委书记", "overlap_org": "中共彬州市委", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 8, "type": "上下级", "context": "市委书记与组织部部长", "overlap_org": "中共彬州市委", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 9, "type": "上下级", "context": "市委书记与纪委书记", "overlap_org": "中共彬州市委", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 10, "type": "上下级", "context": "市委书记与人武部政委", "overlap_org": "中共彬州市委", "overlap_period": "至今"},
    {"person_a": 1, "person_b": 11, "type": "上下级", "context": "市委书记与统战部部长", "overlap_org": "中共彬州市委", "overlap_period": "至今"},
    # 市长与副市长
    {"person_a": 2, "person_b": 4, "type": "上下级", "context": "市长与常务副市长——政府日常工作搭档", "overlap_org": "彬州市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "市长与副市长吕银河", "overlap_org": "彬州市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 12, "type": "上下级", "context": "市长与副市长、公安局长姜岗", "overlap_org": "彬州市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 13, "type": "上下级", "context": "市长与副市长伊丽娜", "overlap_org": "彬州市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 14, "type": "上下级", "context": "市长与副市长赵亚鹏", "overlap_org": "彬州市人民政府", "overlap_period": "至今"},
    {"person_a": 2, "person_b": 15, "type": "上下级", "context": "市长与副市长怀刚", "overlap_org": "彬州市人民政府", "overlap_period": "至今"},
    # 常委之间工作协作
    {"person_a": 4, "person_b": 8, "type": "同僚", "context": "同一届市委常委班子中的工作协作", "overlap_org": "中共彬州市委", "overlap_period": "至今"},
    {"person_a": 8, "person_b": 9, "type": "同僚", "context": "组织部与纪委的工作协作（干部监督）", "overlap_org": "中共彬州市委", "overlap_period": "至今"},
    {"person_a": 7, "person_b": 12, "type": "同僚", "context": "政法委与公安局的工作协作", "overlap_org": "中共彬州市委/彬州市公安局", "overlap_period": "至今"},
]

# =========================================================================
# 主函数
# =========================================================================
def main():
    db_path = Path(__file__).parent / f"{SLUG}_network.db"
    gexf_path = Path(__file__).parent / f"{SLUG}_network.gexf"

    print(f"========== 构建 {SLUG} 数据 ==========")
    print(f"日期: {DATE}")

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=db_path,
        gexf_path=gexf_path,
        overwrite=True,
    )

    print(f"\n========== 构建完成 ==========")
    print(f"数据库: {db_path}")
    print(f"GEXF:   {gexf_path}")


if __name__ == "__main__":
    main()
