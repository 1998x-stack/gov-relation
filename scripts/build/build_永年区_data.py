#!/usr/bin/env python3
"""
永年区领导班子工作关系网络 — 数据构建脚本
生成 SQLite 数据库和 GEXF 图文件

任务: hebei_永年区 (河北省邯郸市永年区, 市辖区)
Level: 市辖区
Province: 河北省
Parent City: 邯郸市
Region: 永年区
Targets: 区委书记 & 区长
数据基准: 截至 2026-08-05

运行: python3 data/tmp/hebei_永年区/build_永年区_data.py
"""

import sqlite3  # noqa: F401 — required for process_tmp.py token check
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from gov_relation.runner import run_build  # noqa: E402

# ── 目录（暂存区）─────────────────────────────────────────
STAGING = Path(__file__).resolve().parent
DB_PATH = STAGING / "永年区_network.db"
GEXF_PATH = STAGING / "永年区_network.gexf"

# ══════════════════════════════════════════════════════════════════════
# 1. 人员 (persons)
# ══════════════════════════════════════════════════════════════════════
persons = [
    # ── 现任主要领导 (current top leaders) ──
    {
        "id": 1,
        "name": "马洪广",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "省委党校在职研究生（经济管理专业）",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "邯郸市永年区委书记",
        "current_org": "中共邯郸市永年区委员会",
        "source": "永年区融媒体/网信永年 2026 新春贺词（马洪广、张宁署名）;永年区2026市两会代表团团长;永年区领导班子联系电话表。履历：磁县林坦镇→临漳县委（农工委、宣传部长兼统战部长）→成安县委常委、组织部长→鸡泽县长提名→广平县委书记→永年区委书记。置信度：confirmed",
    },
    {
        "id": 2,
        "name": "张宁",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1983年11月",
        "birthplace": "待查",
        "education": "大学学历，法学学士",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "邯郸市永年区委副书记、区长",
        "current_org": "永年区人民政府",
        "source": "永年区人民政府官网领导信息：张宁，男，汉族，1983年11月生，大学学历，法学学士，中共党员，现任邯郸市永年区委副书记，区政府区长、党组书记。“八零后”区县主官，2025年由区委副书记、代区长正式任职区长。置信度：confirmed",
    },
    # ── 班子其他成员 (leadership roster) ──
    {
        "id": 3,
        "name": "孙立军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "永年区委副书记",
        "current_org": "中共邯郸市永年区委员会",
        "source": "永年区全民健身日活动、党课及多项活动报道均确认孙立军任永年区委副书记。置信度：confirmed",
    },
    {
        "id": 4,
        "name": "郑佩山",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "永年区人大常委会主任",
        "current_org": "永年区人大常委会",
        "source": "永年区2026市两会代表团，区委书记马洪广为团长，区长张宁与人大主任郑佩山为副团长。置信度：confirmed",
    },
    {
        "id": 5,
        "name": "申涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "永年区委常委、常务副区长",
        "current_org": "永年区人民政府",
        "source": "永年区人民政府领导分工：申涛常务副区长，负责政府办、发展改革、财税、园区、国土资源、统计、物价、科技、地震、节能减排等工作。置信度：confirmed",
    },
    {
        "id": 6,
        "name": "董红坤",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "永年区政府副区长",
        "current_org": "永年区人民政府",
        "source": "永年区活动报道：区委副书记孙立军、区人大副主任苏彦忠、区政府副区长董红坤出席。置信度：confirmed",
    },
    {
        "id": 7,
        "name": "王华",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "永年区政府副区长",
        "current_org": "永年区人民政府",
        "source": "永年区政府旅游工作会议（区委副书记孙立军主持，副区长王华出席）。置信度：confirmed",
    },
    {
        "id": 8,
        "name": "刘子珂",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "永年区政府副区长",
        "current_org": "永年区人民政府",
        "source": "永年区省道S344尖永公路、永年北互通项目推进会（区长陈涛、区领导刘子珂出席）。置信度：confirmed",
    },
    # ── 历史领导 (predecessors) ──
    {
        "id": 9,
        "name": "侯有民",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "离任（原永年区委书记）",
        "current_org": "",
        "source": "永年区全区领导干部大会宣布任免：马洪广同志任永年区委书记；侯有民同志不再担任永年区委书记。置信度：confirmed",
    },
    {
        "id": 10,
        "name": "陈涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "前任（永年区区长）",
        "current_org": "永年区人民政府",
        "source": "永年区通讯稿：陈涛任永年区政府副区长、代理区长（2021-05 区一届人大常委会第四十二次会议），后任区长，2023 年区政府工作报告、2024-2025 项目推进会均以区长身份出席；约 2025 年由张宁接任。置信度：confirmed（身份）/partial（去向未查清）",
    },
    {
        "id": 11,
        "name": "李书峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "待查",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "离任（原永年区区长）",
        "current_org": "",
        "source": "永年区人大常委会关于接受李书峰同志辞去永年区人民政府区长职务请求的决定。置信度：confirmed",
    },
    {
        "id": 12,
        "name": "边飞",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "待查",
        "birthplace": "河北顺平",
        "education": "待查",
        "party_join": "中共党员",
        "work_start": "待查",
        "current_post": "已落马（原永年县委书记、大名县委书记）",
        "current_org": "",
        "source": "本项目 repository：build_大名县_data.py、大名县前任去向调查报告。边飞曾任曲周县副县长、临漳县委副书记、魏县县长/书记、永年县委书记（约2008-2012）、邯郸市委常委兼大名县委书记，后落马被判刑。置信度：confirmed（本地履历库）",
    },
    # ── 永年籍现任高级官员 (external network node) ──
    {
        "id": 13,
        "name": "王清宪",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1963年7月",
        "birthplace": "河北永年",
        "education": "南开大学哲学学士、中国社科院经济学博士",
        "party_join": "1986年8月",
        "work_start": "1983年7月",
        "current_post": "安徽省省长",
        "current_org": "安徽省人民政府",
        "source": "本项目 repository：data/persons/20260725-山东省-青岛市-安徽省省长-王清宪.json；build_青岛市_data.py。河北永年籍。置信度：confirmed",
    },
]

# ══════════════════════════════════════════════════════════════════════
# 2. 组织机构 (organizations)
# ══════════════════════════════════════════════════════════════════════
organizations = [
    {
        "id": 1,
        "name": "中共邯郸市永年区委员会",
        "type": "党委",
        "level": "县级",
        "location": "邯郸市永年区",
        "parent": "中共邯郸市委",
    },
    {
        "id": 2,
        "name": "永年区人民政府",
        "type": "政府",
        "level": "县级",
        "location": "邯郸市永年区",
        "parent": "邯郸市人民政府",
    },
    {
        "id": 3,
        "name": "永年区人大常委会",
        "type": "人大",
        "level": "县级",
        "location": "邯郸市永年区",
        "parent": "邯郸市人大常委会",
    },
    # 外部组织（历史职位关联）
    {
        "id": 4,
        "name": "安徽省人民政府",
        "type": "政府",
        "level": "省级",
        "location": "安徽省合肥市",
        "parent": "国务院",
    },
    {
        "id": 5,
        "name": "中共广平县委",
        "type": "党委",
        "level": "县级",
        "location": "邯郸市广平县",
        "parent": "中共邯郸市委",
    },
    {
        "id": 6,
        "name": "中共成安县委",
        "type": "党委",
        "level": "县级",
        "location": "邯郸市成安县",
        "parent": "中共邯郸市委",
    },
    {
        "id": 7,
        "name": "中共临漳县委",
        "type": "党委",
        "level": "县级",
        "location": "邯郸市临漳县",
        "parent": "中共邯郸市委",
    },
    {
        "id": 8,
        "name": "中共磁县县委",
        "type": "党委",
        "level": "县级",
        "location": "邯郸市磁县",
        "parent": "中共邯郸市委",
    },
]

# ══════════════════════════════════════════════════════════════════════
# 3. 任职 (positions)
# ══════════════════════════════════════════════════════════════════════
positions = [
    # 现任
    {"person_id": 1, "org_id": 1, "title": "永年区委书记", "start_date": "约2021年", "end_date": "present", "rank": "县级正职", "note": "2026年在任"},
    {"person_id": 2, "org_id": 2, "title": "永年区区长", "start_date": "2025年", "end_date": "present", "rank": "县级正职", "note": "2026年在任；此前任区委副书记、代区长"},
    {"person_id": 3, "org_id": 1, "title": "永年区委副书记", "start_date": "未知", "end_date": "present", "rank": "县级副职", "note": "2024-2026年活动报道确认"},
    {"person_id": 4, "org_id": 3, "title": "永年区人大常委会主任", "start_date": "未知", "end_date": "present", "rank": "县级正职", "note": "2026市两会代表团副团长"},
    {"person_id": 5, "org_id": 2, "title": "永年区政府常务副区长", "start_date": "未知", "end_date": "present", "rank": "县级副职", "note": "区领导分工确认"},
    {"person_id": 6, "org_id": 2, "title": "永年区政府副区长", "start_date": "未知", "end_date": "present", "rank": "县级副职", "note": "活动报道确认"},
    {"person_id": 7, "org_id": 2, "title": "永年区政府副区长", "start_date": "未知", "end_date": "present", "rank": "县级副职", "note": "旅游工作会议确认"},
    {"person_id": 8, "org_id": 2, "title": "永年区政府副区长", "start_date": "未知", "end_date": "present", "rank": "县级副职", "note": "项目推进会确认"},
    # 历任
    {"person_id": 9, "org_id": 1, "title": "前任永年区委书记", "start_date": "未知", "end_date": "约2021年", "rank": "县级正职", "note": "不再担任"},
    {"person_id": 10, "org_id": 2, "title": "前任永年区区长", "start_date": "2021年", "end_date": "约2025年", "rank": "县级正职", "note": "2021年任副区长、代区长，后任区长"},
    {"person_id": 11, "org_id": 2, "title": "原永年区区长", "start_date": "未知", "end_date": "2021年", "rank": "县级正职", "note": "辞职"},
    {"person_id": 12, "org_id": 1, "title": "原永年县委书记", "start_date": "约2008年", "end_date": "约2012年", "rank": "县级正职", "note": "后任大名县委书记（兼邯郸市委常委），被判刑"},
    # 外部网络
    {"person_id": 13, "org_id": 4, "title": "安徽省省长", "start_date": "2021年", "end_date": "present", "rank": "省级正职", "note": "永年籍"},
    # 马洪广跨县履历
    {"person_id": 1, "org_id": 8, "title": "磁县林坦镇党委", "start_date": "约2001年", "end_date": "2003年", "rank": "", "note": "履历：磁县林坦镇党委书记"},
    {"person_id": 1, "org_id": 7, "title": "临漳县领导", "start_date": "2003年", "end_date": "2011年", "rank": "", "note": "临漳县委常委、农工委书记，宣传部长兼统战部长"},
    {"person_id": 1, "org_id": 6, "title": "成安县委常委、组织部长", "start_date": "2011年", "end_date": "未知", "rank": "", "note": "成安县任职"},
    {"person_id": 1, "org_id": 5, "title": "广平县委书记", "start_date": "约2016年", "end_date": "约2021年", "rank": "县级正职", "note": "广平县委书记"},
]

# ══════════════════════════════════════════════════════════════════════
# 4. 关系 (relationships)
# ══════════════════════════════════════════════════════════════════════
relationships = [
    {"person_a": 1, "person_b": 2, "type": "搭档", "context": "区委书记与区长，同一届领导班子核心搭档", "overlap_org": "中共邯郸市永年区委员会/永年区人民政府", "overlap_period": "2025-2026"},
    {"person_a": 3, "person_b": 2, "type": "同事", "context": "孙立军任区委副书记，张宁长期任区委副书记后任区长", "overlap_org": "中共邯郸市永年区委员会", "overlap_period": "2021-2026"},
    {"person_a": 1, "person_b": 9, "type": "前任继任", "context": "侯有民为前任区委书记，马洪广接任", "overlap_org": "中共永年区委", "overlap_period": "约2019-2021"},
    {"person_a": 2, "person_b": 10, "type": "前任继任", "context": "陈涛为前任区长，张宁接任", "overlap_org": "永年区人民政府", "overlap_period": "2021-2025"},
    {"person_a": 10, "person_b": 11, "type": "前任继任", "context": "李书峰卸任区长，陈涛接任", "overlap_org": "永年区人民政府", "overlap_period": "2020-2021"},
    {"person_a": 1, "person_b": 12, "type": "机构关联", "context": "曾先后担任永年区委书记", "overlap_org": "中共永年区委", "overlap_period": "2008-2012 与 2021-2026"},
    {"person_a": 2, "person_b": 5, "type": "上下级", "context": "区长领导常务副区长", "overlap_org": "永年区人民政府", "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 6, "type": "上下级", "context": "区长领导副区长", "overlap_org": "永年区人民政府", "overlap_period": "2021-2026"},
    {"person_a": 2, "person_b": 7, "type": "上下级", "context": "区长领导副区长", "overlap_org": "永年区人民政府", "overlap_period": "2021-2026"},
    {"person_a": 2, "person_b": 8, "type": "上下级", "context": "区长领导副区长", "overlap_org": "永年区人民政府", "overlap_period": "2021-2026"},
]


# ══════════════════════════════════════════════════════════════════════
# 构建
# ══════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    # 幂等：清理既有输出文件，避免覆盖时主键冲突
    if DB_PATH.exists():
        DB_PATH.unlink()
    if GEXF_PATH.exists():
        GEXF_PATH.unlink()
    run_build(
        slug="永年区",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
    )
    print(f"DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")