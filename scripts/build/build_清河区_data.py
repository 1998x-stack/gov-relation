#!/usr/bin/env python3
"""Build 铁岭市清河区 (Qinghe District, Tieling City, Liaoning) personnel network
database and graph.

Research source: 铁岭市清河区人民政府官方网站 (www.tlqh.gov.cn), 铁岭市人民政府
官方网站 (tieling.gov.cn)
- 区委书记王亮 & 区长张宇 confirmed by 2026-08-03 官方新闻
- 区政府领导分工通知 (铁清政办发〔2026〕2号, 2026-03-12)
- 清河区第十一次党代会代表报道 (2026-07-27/29)
- 2025/2024/2023 年度政府工作报告
- Data collected: 2026-08-06
- Research constraints: Web search (Exa/Baidu/Sogou/Bing/Jina) was unavailable;
  detailed prior career histories and predecessor secretary name are marked
  "unverified" / "open_question".
"""

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
for parent_count in [2, 3, 4, 5]:
    candidate = Path(__file__).resolve().parents[parent_count]
    if (candidate / "gov_relation").is_dir():
        REPO_ROOT = candidate
        break
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from gov_relation.runner import run_build

SLUG = "清河区"
TASK_ID = "liaoning_清河区"

# ── Persons ──────────────────────────────────────────────────────────
persons = [
    # === Target 1: 区委书记 王亮 ===
    {
        "id": 1,
        "name": "王亮",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委书记",
        "current_org": "中国共产党铁岭市清河区委员会",
        "source": "https://www.tlqh.gov.cn/qinghe/ywdt/jryw/2026080308381785894/index.html",
    },
    # === Target 2: 区长 张宇 ===
    {
        "id": 2,
        "name": "张宇",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委副书记、区长",
        "current_org": "铁岭市清河区人民政府",
        "source": "https://www.tlqh.gov.cn/qinghe/ywdt/jryw/2026080308381785894/index.html",
    },
    # === 区人大常委会主任 ===
    {
        "id": 3,
        "name": "李景涛",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区人大常委会主任",
        "current_org": "铁岭市清河区人民代表大会常务委员会",
        "source": "https://www.tlqh.gov.cn/qinghe/ywdt/jryw/2026070814030793108/index.html",
    },
    # === 区政协主席 ===
    {
        "id": 4,
        "name": "邹立璞",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区政协主席",
        "current_org": "中国人民政治协商会议铁岭市清河区委员会",
        "source": "https://www.tlqh.gov.cn/qinghe/ywdt/jryw/2026062210024056125/index.html",
    },
    # === 区委常委、常务副区长 张岩 ===
    {
        "id": 5,
        "name": "张岩",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、常务副区长",
        "current_org": "铁岭市清河区人民政府",
        "source": "https://www.tlqh.gov.cn/qinghe/zwgk/zfxxgk/fdzdgknr/lzyj62/qzfbgswj/2026070810412814191/index.html",
    },
    # === 区委常委、副区长 史国鹏 ===
    {
        "id": 6,
        "name": "史国鹏",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委、副区长",
        "current_org": "铁岭市清河区人民政府",
        "source": "https://www.tlqh.gov.cn/qinghe/ywdt/jryw/2026071610172873638/index.html",
    },
    # === 副区长 ===
    {
        "id": 7,
        "name": "董萌",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "铁岭市清河区人民政府",
        "source": "https://www.tlqh.gov.cn/qinghe/zwgk/zfxxgk/fdzdgknr/lzyj62/qzfbgswj/2026070810412814191/index.html",
    },
    {
        "id": 8,
        "name": "马辉",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长、区公安分局局长",
        "current_org": "铁岭市清河区人民政府",
        "source": "https://www.tlqh.gov.cn/qinghe/zwgk/zfxxgk/fdzdgknr/lzyj62/qzfbgswj/2026070810412814191/index.html",
    },
    {
        "id": 9,
        "name": "肖天舒",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "铁岭市清河区人民政府",
        "source": "https://www.tlqh.gov.cn/qinghe/zwgk/zfxxgk/fdzdgknr/lzyj62/qzfbgswj/2026070810412814191/index.html",
    },
    {
        "id": 10,
        "name": "张寨",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "副区长",
        "current_org": "铁岭市清河区人民政府",
        "source": "https://www.tlqh.gov.cn/qinghe/zwgk/zfxxgk/fdzdgknr/lzyj62/qzfbgswj/2026070810412814191/index.html",
    },
    # === 区委班子成员（十一届党代会前排就座，具体职务待核） ===
    {
        "id": 11,
        "name": "贾峰",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委（具体职务待查）",
        "current_org": "中国共产党铁岭市清河区委员会",
        "source": "https://www.tlqh.gov.cn/qinghe/ywdt/jryw/2026072915050094138/index.html",
    },
    {
        "id": 12,
        "name": "刘其伟",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委（具体职务待查）",
        "current_org": "中国共产党铁岭市清河区委员会",
        "source": "https://www.tlqh.gov.cn/qinghe/ywdt/jryw/2026072915050094138/index.html",
    },
    {
        "id": 13,
        "name": "张朝",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委（具体职务待查）",
        "current_org": "中国共产党铁岭市清河区委员会",
        "source": "https://www.tlqh.gov.cn/qinghe/ywdt/jryw/2026072915050094138/index.html",
    },
    {
        "id": 14,
        "name": "李学敏",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委（具体职务待查）",
        "current_org": "中国共产党铁岭市清河区委员会",
        "source": "https://www.tlqh.gov.cn/qinghe/ywdt/jryw/2026072915050094138/index.html",
    },
    {
        "id": 15,
        "name": "吕宁",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委（具体职务待查）",
        "current_org": "中国共产党铁岭市清河区委员会",
        "source": "https://www.tlqh.gov.cn/qinghe/ywdt/jryw/2026072915050094138/index.html",
    },
    {
        "id": 16,
        "name": "赵慧丽",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "区委常委（具体职务待查）",
        "current_org": "中国共产党铁岭市清河区委员会",
        "source": "https://www.tlqh.gov.cn/qinghe/ywdt/jryw/2026072915050094138/index.html",
    },
    # === 前任区长 王俊平 ===
    {
        "id": 17,
        "name": "王俊平",
        "gender": "男",
        "ethnicity": "",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任区长（2021-2023年任职）",
        "current_org": "",
        "source": "https://www.tlqh.gov.cn/qinghe/zwgk/zfxxgk/fdzdgknr/qtfdxx/zfgzbg/2023122512470179671/index.html",
    },
]

# ── Organizations ────────────────────────────────────────────────────
organizations = [
    {"id": 0, "name": "中国共产党铁岭市清河区委员会", "type": "党委", "level": "县处级", "parent": "中国共产党铁岭市委员会", "location": "辽宁省铁岭市清河区"},
    {"id": 1, "name": "铁岭市清河区人民政府", "type": "政府", "level": "县处级", "parent": "铁岭市人民政府", "location": "辽宁省铁岭市清河区"},
    {"id": 2, "name": "铁岭市清河区人民代表大会常务委员会", "type": "人大", "level": "县处级", "parent": "", "location": "辽宁省铁岭市清河区"},
    {"id": 3, "name": "中国人民政治协商会议铁岭市清河区委员会", "type": "政协", "level": "县处级", "parent": "", "location": "辽宁省铁岭市清河区"},
    {"id": 4, "name": "铁岭市清河区监察委员会", "type": "纪委", "level": "县处级", "parent": "", "location": "辽宁省铁岭市清河区"},
    {"id": 5, "name": "铁岭市清河区公安分局", "type": "政府", "level": "乡科级", "parent": "铁岭市清河区人民政府", "location": "辽宁省铁岭市清河区"},
    {"id": 6, "name": "铁岭市清河区人民法院", "type": "司法", "level": "县处级", "parent": "", "location": "辽宁省铁岭市清河区"},
    {"id": 7, "name": "铁岭市清河区人民检察院", "type": "司法", "level": "县处级", "parent": "", "location": "辽宁省铁岭市清河区"},
]

# ── Positions ────────────────────────────────────────────────────────
positions = [
    # 王亮 - 区委书记
    {"person_id": 1, "org_id": 0, "title": "区委书记", "start_date": "2026", "end_date": "present", "rank": "县处级正职", "note": "2026年3月前后由区长转任区委书记；2026-07-27 区第十一次党代会上作区委工作报告"},
    {"person_id": 1, "org_id": 1, "title": "区长", "start_date": "2024", "end_date": "2026-03", "rank": "县处级正职", "note": "2024年起任清河区人民政府区长，主持区政府全面工作；2024、2025年度政府工作报告报告人；2026-03-12分工通知仍列区长"},
    {"person_id": 1, "org_id": 0, "title": "区委副书记", "start_date": "2024", "end_date": "2026-03", "rank": "县处级副职", "note": "区长期间兼任区委副书记"},
    # 张宇 - 区委副书记、区长
    {"person_id": 2, "org_id": 0, "title": "区委副书记", "start_date": "2026-03", "end_date": "present", "rank": "县处级副职", "note": "2026年3月前后任区委副书记"},
    {"person_id": 2, "org_id": 1, "title": "区长（区防汛抗旱指挥部总指挥）", "start_date": "2026-03", "end_date": "present", "rank": "县处级正职", "note": "2026年3月后接任区长；主持区政府全面工作；持续出席区政府常务会、防汛调研等活动"},
    # 李景涛 - 人大主任
    {"person_id": 3, "org_id": 2, "title": "区人大常委会主任", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "出席区两优一先表彰大会、区委民生实事视察等"},
    # 邹立璞 - 政协主席
    {"person_id": 4, "org_id": 3, "title": "区政协主席", "start_date": "", "end_date": "present", "rank": "县处级正职", "note": "随四大班子视察民生实事工程"},
    # 张岩 - 常务副区长
    {"person_id": 5, "org_id": 0, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "清河区委常委"},
    {"person_id": 5, "org_id": 1, "title": "常务副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责区政府常务、发展改革、财税、金融、人社、农业农村、应急、统计、数据、营商环境、信访、消防等；与董萌互为AB角"},
    {"person_id": 5, "org_id": 1, "title": "区政府党组副书记", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "协助区长（王亮当时）分管区审计局"},
    # 史国鹏 - 常委、副区长
    {"person_id": 6, "org_id": 0, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "清河区委常委"},
    {"person_id": 6, "org_id": 1, "title": "副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "2026-07-14清河水库泄洪准备工作会议上传达泄洪专项工作方案"},
    # 各副区长
    {"person_id": 7, "org_id": 1, "title": "副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责教育、民政、水利、卫生健康、退役军人事务、医疗保障等；与张岩互为AB角"},
    {"person_id": 8, "org_id": 1, "title": "副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责公安、司法、打击走私、交通管理等；与肖天舒互为AB角；联系区法院、区检察院、杨木林子镇"},
    {"person_id": 8, "org_id": 5, "title": "区公安分局局长", "start_date": "", "end_date": "present", "rank": "乡科级正职", "note": "主持区公安分局工作"},
    {"person_id": 9, "org_id": 1, "title": "副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责工业和信息化、科技、市场监管、文旅、商务、招商、供销等；与马辉互为AB角"},
    {"person_id": 10, "org_id": 1, "title": "副区长", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "负责住房和城乡建设、城市管理、交通运输、自然资源、生态环境等；AB角领导临时调剂"},
    # 未定职务的区委常委
    {"person_id": 11, "org_id": 0, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "十一届区委班子成员，具体分管职务待查"},
    {"person_id": 12, "org_id": 0, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "十一届区委班子成员，具体分管职务待查"},
    {"person_id": 13, "org_id": 0, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "十一届区委班子成员，具体分管职务待查"},
    {"person_id": 14, "org_id": 0, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "十一届区委班子成员，具体分管职务待查"},
    {"person_id": 15, "org_id": 0, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "十一届区委班子成员，具体分管职务待查"},
    {"person_id": 16, "org_id": 0, "title": "区委常委", "start_date": "", "end_date": "present", "rank": "县处级副职", "note": "十一届区委班子成员，具体分管职务待查"},
    # 王俊平 - 前任区长
    {"person_id": 17, "org_id": 1, "title": "区长", "start_date": "2021", "end_date": "2023", "rank": "县处级正职", "note": "2021-2023年任清河区人民政府区长，连续在2021/2022/2023年度政府工作报告作报告"},
]

# ── Relationships ────────────────────────────────────────────────────
relationships = [
    # 党政一把手
    {"person_a": 1, "person_b": 2, "type": "overlap", "context": "区委书记与区委副书记、区长党政搭档（2026年至今）", "overlap_org": "中共铁岭市清河区委员会", "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 2, "type": "predecessor_successor", "context": "王亮任区长时张宇接任区长，王亮转任区委书记后与张宇成为上下级搭档", "overlap_org": "铁岭市清河区人民政府", "overlap_period": "2026年"},
    # 王亮 - 王俊平：前后任区长
    {"person_a": 17, "person_b": 1, "type": "predecessor_successor", "context": "王俊平2021-2023任区长，王亮2024年接任区长", "overlap_org": "铁岭市清河区人民政府", "overlap_period": "2023-2024"},
    # 四大班子主要领导
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "区委书记与区人大主任，四大班子领导成员", "overlap_org": "清河区四大班子", "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "区委书记与区政协主席，四大班子领导成员", "overlap_org": "清河区四大班子", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 3, "type": "overlap", "context": "区长与区人大主任", "overlap_org": "清河区四大班子", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "区长与区政协主席", "overlap_org": "清河区四大班子", "overlap_period": "2026年"},
    # 区委常委班子内部（十一届区委）
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "区委书记与区委常委/常务副区长", "overlap_org": "清河区委常委班子", "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "区委书记与区委常委/副区长", "overlap_org": "清河区委常委班子", "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 11, "type": "overlap", "context": "区委书记与区委常委", "overlap_org": "清河区委常委班子", "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 12, "type": "overlap", "context": "区委书记与区委常委", "overlap_org": "清河区委常委班子", "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 13, "type": "overlap", "context": "区委书记与区委常委", "overlap_org": "清河区委常委班子", "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 14, "type": "overlap", "context": "区委书记与区委常委", "overlap_org": "清河区委常委班子", "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 15, "type": "overlap", "context": "区委书记与区委常委", "overlap_org": "清河区委常委班子", "overlap_period": "2026年"},
    {"person_a": 1, "person_b": 16, "type": "overlap", "context": "区委书记与区委常委", "overlap_org": "清河区委常委班子", "overlap_period": "2026年"},
    # 区长与副区长们
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "区长与常务副区长", "overlap_org": "清河区人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 6, "type": "overlap", "context": "区长与区委常委、副区长", "overlap_org": "清河区人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "区长与副区长", "overlap_org": "清河区人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 8, "type": "overlap", "context": "区长与副区长（公安）", "overlap_org": "清河区人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 9, "type": "overlap", "context": "区长与副区长", "overlap_org": "清河区人民政府", "overlap_period": "2026年"},
    {"person_a": 2, "person_b": 10, "type": "overlap", "context": "区长与副区长", "overlap_org": "清河区人民政府", "overlap_period": "2026年"},
    # AB角互补
    {"person_a": 5, "person_b": 7, "type": "overlap", "context": "AB角互补：张岩与董萌", "overlap_org": "清河区人民政府", "overlap_period": "2026年"},
    {"person_a": 8, "person_b": 9, "type": "overlap", "context": "AB角互补：马辉与肖天舒", "overlap_org": "清河区人民政府", "overlap_period": "2026年"},
    # 分工联系
    {"person_a": 8, "person_b": 6, "type": "other", "context": "马辉(公安副区长)联系区法院、区检察院，与贾峰等政法口常委可能共事", "overlap_org": "清河区政法系统", "overlap_period": "2026年"},
]

if __name__ == "__main__":
    _CURRENT_DIR = Path(__file__).parent.resolve()
    if _CURRENT_DIR.name == "liaoning_清河区" or (_CURRENT_DIR / "清河区_network.db").parent.name.startswith("tmp"):
        staging = _CURRENT_DIR
    else:
        staging = REPO_ROOT / "data/tmp" / TASK_ID
    staging.mkdir(parents=True, exist_ok=True)

    db_path = staging / f"{SLUG}_network.db"
    gexf_path = staging / f"{SLUG}_network.gexf"

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

    DB_PATH = db_path
    GEXF_PATH = gexf_path
    import sqlite3 as _sqlite

    conn = _sqlite.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    for table in ("persons", "organizations", "positions", "relationships"):
        count = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
        print(f"{table}: {count}")
    conn.close()
    ok = GEXF_PATH.exists() and "<nodes>" in GEXF_PATH.read_text(encoding="utf-8")
    print(f"DB_PATH={DB_PATH}")
    print(f"GEXF_PATH={GEXF_PATH}")
    print(f"GEXF valid: {ok}")
    if not ok:
        raise SystemExit(1)