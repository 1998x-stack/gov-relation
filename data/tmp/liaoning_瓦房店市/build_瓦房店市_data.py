#!/usr/bin/env python3
"""
瓦房店市 — 领导班子工作关系网络数据生成脚本

数据限制声明:
由于本环境网络严重受限（Exa rate-limited、百度403、所有搜索引擎超时、
瓦房店市政府网站DNS不可解析），仅大连市人民政府网站(www.dl.gov.cn)可用，
本次仅能生成基于已确认信息的有限数据。

已确认人物:
1. 赵东 — 瓦房店市委书记（大连副市长兼任）
2. 熊茂平 — 大连市委书记（上级领导）
3. 李强 — 大连市长（上级领导）
4. 杨海三 — 前瓦房店市委副书记（已调离，现西岗区委书记）

待填补缺口:
- 瓦房店市长(姓名未知)
- 瓦房店市委副书记(姓名未知)
- 瓦房店常务副市长(姓名未知)
- 瓦房店纪委书记(姓名未知)
- 赵东任现职前全部履历
"""

from gov_relation.runner import run_build
from gov_relation.paths import DATABASE_DIR, GRAPH_DIR

SLUG = "瓦房店市"

persons = [
    {
        "id": "wafangdian_zhaodong",
        "name": "赵东",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1972年1月",
        "birthplace": "",
        "education": "在职研究生学历，工商管理硕士",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "大连市人民政府副市长、瓦房店市委书记、长兴岛经济技术开发区党工委书记",
        "current_org": "大连市人民政府 / 中共瓦房店市委员会 / 大连长兴岛经济技术开发区党工委",
        "source": "大连市人民政府官网 https://www.dl.gov.cn/col/col11565/index.html",
    },
    {
        "id": "dalian_xionghaoping",
        "name": "熊茂平",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1967年",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "辽宁省委副书记、大连市委书记",
        "current_org": "中共大连市委",
        "source": "大连市人民政府官网 https://www.dl.gov.cn/",
    },
    {
        "id": "dalian_liqiang",
        "name": "李强",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1968年11月",
        "birthplace": "",
        "education": "大学学历，硕士学位",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "大连市委副书记、市长、市政府党组书记",
        "current_org": "大连市人民政府",
        "source": "大连市人民政府官网 https://www.dl.gov.cn/col/col11600/index.html",
    },
    {
        "id": "xigangqu_yanghaisan",
        "name": "杨海三",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1977年",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "西岗区委书记（前瓦房店市委副书记）",
        "current_org": "中国共产党大连市西岗区委员会",
        "source": "西岗区调查报告 / data/persons/20260725-辽宁省-大连市-区委书记-杨海三.json",
    },
]

organizations = [
    {
        "id": 1,
        "name": "中共瓦房店市委员会",
        "type": "party",
        "level": "县级",
        "parent": "大连市",
        "location": "大连市瓦房店市",
    },
    {
        "id": 2,
        "name": "瓦房店市人民政府",
        "type": "government",
        "level": "县级",
        "parent": "大连市人民政府",
        "location": "大连市瓦房店市",
    },
    {
        "id": 3,
        "name": "中共大连市委",
        "type": "party",
        "level": "副省级",
        "parent": "辽宁省",
        "location": "大连市",
    },
    {
        "id": 4,
        "name": "大连市人民政府",
        "type": "government",
        "level": "副省级",
        "parent": "辽宁省人民政府",
        "location": "大连市",
    },
    {
        "id": 5,
        "name": "大连长兴岛经济技术开发区党工委",
        "type": "party",
        "level": "国家级开发区",
        "parent": "大连市",
        "location": "大连市长兴岛",
    },
    {
        "id": 6,
        "name": "中共大连市西岗区委员会",
        "type": "party",
        "level": "县级",
        "parent": "中共大连市委",
        "location": "大连市西岗区",
    },
]

positions = [
    # 赵东 — 瓦房店市委书记
    {
        "person_id": "wafangdian_zhaodong",
        "org_id": 1,
        "title": "中共瓦房店市委书记",
        "start": "已知不晚于2024年",
        "end": "present",
        "rank": "正处级",
        "note": "以大连市副市长身份兼任",
    },
    # 赵东 — 大连副市长
    {
        "person_id": "wafangdian_zhaodong",
        "org_id": 4,
        "title": "大连市人民政府副市长、党组成员",
        "start": "已知不晚于2024年",
        "end": "present",
        "rank": "副厅级",
        "note": "兼任瓦房店市委书记",
    },
    # 赵东 — 长兴岛经开区党工委书记
    {
        "person_id": "wafangdian_zhaodong",
        "org_id": 5,
        "title": "大连长兴岛经济技术开发区党工委书记",
        "start": "已知不晚于2024年",
        "end": "present",
        "rank": "",
        "note": "三级职务兼任",
    },
    # 熊茂平 — 大连市委书记
    {
        "person_id": "dalian_xionghaoping",
        "org_id": 3,
        "title": "中共大连市委书记、辽宁省委副书记",
        "start": "2024年4月",
        "end": "present",
        "rank": "副省级",
        "note": "省委副书记兼任",
    },
    # 李强 — 大连市长
    {
        "person_id": "dalian_liqiang",
        "org_id": 4,
        "title": "大连市委副书记、市长、市政府党组书记",
        "start": "已知不晚于2026年",
        "end": "present",
        "rank": "副省级",
        "note": "",
    },
    # 杨海三 — 前瓦房店市委副书记
    {
        "person_id": "xigangqu_yanghaisan",
        "org_id": 1,
        "title": "瓦房店市委副书记",
        "start": "约2018年",
        "end": "2020年",
        "rank": "正处级",
        "note": "已调离，现西岗区委书记",
    },
    # 杨海三 — 现西岗区委书记
    {
        "person_id": "xigangqu_yanghaisan",
        "org_id": 6,
        "title": "西岗区委书记",
        "start": "2024年12月",
        "end": "present",
        "rank": "正处级",
        "note": "",
    },
]

relationships = [
    # 赵东 ← 熊茂平 (上级)
    {
        "person_a": "wafangdian_zhaodong",
        "person_b": "dalian_xionghaoping",
        "type": "superior_subordinate",
        "context": "大连市委书记与瓦房店市委书记的上下级关系",
        "overlap_org": "中共大连市委",
        "overlap_period": "当前",
    },
    # 赵东 ← 李强 (上级)
    {
        "person_a": "wafangdian_zhaodong",
        "person_b": "dalian_liqiang",
        "type": "superior_subordinate",
        "context": "大连市长与副市长/瓦房店市委书记的上下级关系",
        "overlap_org": "大连市人民政府",
        "overlap_period": "当前",
    },
    # 杨海三 — 赵东 (前后任/曾共事于瓦房店)
    {
        "person_a": "xigangqu_yanghaisan",
        "person_b": "wafangdian_zhaodong",
        "type": "overlap",
        "context": "杨海三曾任瓦房店市委副书记(约2018-2020)，赵东为现任瓦房店市委书记(不晚于2024年起)。两人在瓦房店的工作时间是否有重叠取决于赵东的到任时间(未知)。",
        "overlap_org": "中共瓦房店市委员会",
        "overlap_period": "不确定",
    },
]

if __name__ == "__main__":
    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DATABASE_DIR / f"{SLUG}_network.db",
        gexf_path=GRAPH_DIR / f"{SLUG}_network.gexf",
        overwrite=False,
    )
