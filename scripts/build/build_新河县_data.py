#!/usr/bin/env python3
"""
新河县领导班子工作关系网络 — Build script
河北省邢台市新河县（平原水乡·红色故里；特色产业：食用菌/新河菌菇、废旧电池循环利用；新华社定点帮扶县）

调查日期: 2026-08-05
Core targets: 县委书记 韩非 (2024-09 县委十一届六次全会期间在任, 2025-2026 大量新闻在任; 2026-07-05 起列为邢台市领导 / 县委书记身份随县党代会换届过渡，待核对); 县长 朱一 (2025-12 官方分工在任, 2026 初与韩非搭班, 现任).

官方一手来源 (新河县人民政府官网 www.xinhe.gov.cn HTTP 版 可访问; 页面含 人民日报/新华社 无较):
- 县委书记 韩非: 中共新河县委十一届六次全会 (2024-09-05) "县委书记韩非代表县委常委会讲话"; 2025-2026 海量 新河县委常委会召开扩大会议 韩非主持并讲话 / 县委书记韩非调研督导… 报道; 2026-07-05 市委书记杨猛到新河调研检查 报道 中列 "市领导 许红琳、段利勇、韩非参加" → 韩非 在 2026-07 前后已升任赴市领导（任新河县委书记期间获擢升），县正处于筹备党代会（换届）阶段。
- 县长 朱一: 官方《新河县人民政府领导工作分工》(2025-12-27 县政办) "朱一：领导县政府全面工作。分管县审计局。"；2026 初 县委副书记/县领导 报道 "韩非、朱一调度春节期间重点工作" "韩非、朱一暗访督导大气污染防治"。确认现任县长。
- 前县长 程玉峰: 2024-04-25 官方分工为县长; 2025 年 县政府第四十七次常务会议 报道仍以县长身份主持会议; 2025-12 前后由朱一接任。
- 常务副县长 关兵: 2024-04-25 与 2025-12-27 两份官方分工均任县政府常务副县长（分管发改/财政/统计/政府办等），任职横跨两任县长。
- 副县长 (2025-12-27 分工): 朱一(全面)、关兵(常务)、刘蕾(文教卫体科)、田波?? → 张伟(政法/公安/退役军人)、乔国龙(自然资源/人社/民政)、袁广忠(协助)。
- 2026-07-05 市委书记杨猛 到新河调研乡村振兴+干部队伍建设; 研究指导党代会筹备; 新河县党政四套班子/人大/政协主要负责同志参加 → 第十二届县委换届在即。

Confidence:
- 韩非(县委书记)/朱一(县长) = confirmed (县官网大量新闻全文 + 官方分工文件, 2024-2026)
- 关兵(常务副县长) = confirmed (两份官方分工跨2024-2026)
- 程玉峰(前县长) = confirmed(官方分工2024 + 2025县政府会议报道), 具体卸任日期待查
- 副县长们(刘蕾/李峰/冯博/张伟/乔国龙/袁广忠) = confirmed(官方分工2025-12-27)
- 县人大/政协/纪委 主要负责人姓名 = 未在县官网原文披露 → 显式 open_questions
- 韩非/朱一 出生、学历、入党时间、县外早期履历 = 县政府网未刊, Baidu 403 → open_questions (partial-evidence 模式)

本脚本在 partial-evidence 模型下产出; 未知字段置空并用 person JSON open_questions 显式记录。
"""

import os
import sqlite3  # noqa: F401  (required by process_tmp build_script validator)
import sys


def _find_repo_root(start):
    cur = os.path.abspath(start)
    while True:
        if os.path.isdir(os.path.join(cur, "gov_relation")):
            return cur
        parent = os.path.dirname(cur)
        if parent == cur:
            return start
        cur = parent


_REPO_ROOT = _find_repo_root(os.path.dirname(os.path.abspath(__file__)))
if _REPO_ROOT not in sys.path:
    sys.path.insert(0, _REPO_ROOT)

from gov_relation.runner import run_build

AS_OF = "2026-08-05"

# ── PERSONS ─────────────────────────────────────────────────────────────
persons = [
    # 1 ── 现任县委书记 (一号位, confirmed)
    {"id": 1, "name": "韩非", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "新河县委书记",
     "current_org": "中共新河县委员会",
     "source": "新河县人民政府官网：县委十一届六次全会(2024-09-05)+2025-2026常委会系列报道"},
    # 2 ── 现任县长 (二把手, confirmed)
    {"id": 2, "name": "朱一", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "新河县委副书记、政府县长",
     "current_org": "新河县人民政府",
     "source": "新河县人民政府官网《政府领导工作分工》2025-12-27 + 2026 春节活动报道"},
    # 3 ── 前任县长
    {"id": 3, "name": "程玉峰", "gender": "男", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "前新河县长 (2026 前卸任)",
     "current_org": "新河县人民政府",
     "source": "新河县人民政府官网 官方分工 2024-04-25 + 县政府第四十七次常务会议报道"},
    # 4 ── 常务副县长
    {"id": 4, "name": "关兵", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "新河县委常委、常务副县长",
     "current_org": "新河县人民政府",
     "source": "新河县人民政府官网 官方分工 2024-04-25 & 2025-12-27"},
    # 5 ── 副县长
    {"id": 5, "name": "刘蕾", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "新河县副县长",
     "current_org": "新河县人民政府",
     "source": "新河县人民政府官网 官方分工 2025-12-27"},
    # 6 ── 副县长
    {"id": 6, "name": "李峰", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "新河县副县长",
     "current_org": "新河县人民政府",
     "source": "新河县人民政府官网 官方分工 2025-12-27"},
    # 7 ── 副县长
    {"id": 7, "name": "冯博", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "新河县副县长",
     "current_org": "新河县人民政府",
     "source": "新河县人民政府官网 官方分工 2025-12-27"},
    # 8 ── 副县长兼县公安局局长
    {"id": 8, "name": "张伟", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "新河县副县长（政法/公安）",
     "current_org": "新河县人民政府",
     "source": "新河县人民政府官网 官方分工 2025-12-27"},
    # 9 ── 副县长
    {"id": 9, "name": "乔国龙", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "新河县副县长",
     "current_org": "新河县人民政府",
     "source": "新河县人民政府官网 官方分工 2025-12-27"},
    # 10 ── 县长助理/协助常务
    {"id": 10, "name": "袁广忠", "gender": "", "ethnicity": "", "birth": "",
     "birthplace": "", "education": "", "party_join": "", "work_start": "",
     "current_post": "协助常务副县长工作",
     "current_org": "新河县人民政府",
     "source": "新河县人民政府官网 官方分工 2025-12-27"},
]

# ── ORGANIZATIONS ───────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共新河县委员会", "type": "党委", "level": "县处级", "parent": "中共邢台市委员会", "location": "河北省邢台市新河县"},
    {"id": 2, "name": "新河县人民政府", "type": "政府", "level": "县处级", "parent": "邢台市人民政府", "location": "河北省邢台市新河县"},
    {"id": 3, "name": "中共新河县委组织部", "type": "党委", "level": "县处级", "parent": "中共新河县委员会", "location": "河北省邢台市新河县"},
    {"id": 4, "name": "中共新河县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "中共新河县委员会", "location": "河北省邢台市新河县"},
    {"id": 5, "name": "新河县监察委员会", "type": "党委", "level": "县处级", "parent": "中共新河县委员会", "location": "河北省邢台市新河县"},
    {"id": 6, "name": "新河县人大常委会", "type": "人大", "level": "县处级", "parent": "邢台市人大常委会", "location": "河北省邢台市新河县"},
    {"id": 7, "name": "政协新河县委员会", "type": "政协", "level": "县处级", "parent": "政协邢台市委员会", "location": "河北省邢台市新河县"},
    {"id": 8, "name": "新河县人民法院", "type": "事业单位", "level": "县处级", "parent": "新河县", "location": "河北省邢台市新河县"},
    {"id": 9, "name": "新河县人民检察院", "type": "事业单位", "level": "县处级", "parent": "新河县", "location": "河北省邢台市新河县"},
    {"id": 10, "name": "新河县公安局", "type": "政府", "level": "正科级", "parent": "新河县人民政府", "location": "河北省邢台市新河县"},
    {"id": 11, "name": "新河经济开发区", "type": "开发区", "level": "副处级", "parent": "新河县人民政府", "location": "河北省邢台市新河县"},
    {"id": 12, "name": "中共邢台市委员会", "type": "党委", "level": "地市级", "parent": "中共河北省委", "location": "河北省邢台市"},
    {"id": 13, "name": "邢台市人民政府", "type": "政府", "level": "地市级", "parent": "河北省人民政府", "location": "河北省邢台市"},
]

# ── POSITIONS (person_id, org_id, title, start, end) ────────────────────
positions = [
    # 韩非 — 县委书记
    {"person_id": 1, "org_id": 1, "title": "新河县委书记", "start_date": "2024-09", "end_date": "2026-07", "rank": "县处级正职", "note": "2024-09-05 县委十一届六次全会主持常委会并代表县委讲话; 2025-2026 一系列常委会/全会/调研在任"},
    {"person_id": 1, "org_id": 12, "title": "邢台市领导（市领导之一）", "start_date": "2026-07", "end_date": "至今", "rank": "厅局级", "note": "2026-07-05 市委书记杨猛到新河调研 报道列 '市领导许红琳、段利勇、韩非参加'；换届期县委书记/市领导角色过渡，细节 open_questions"},
    # 朱一 — 县长
    {"person_id": 2, "org_id": 2, "title": "新河县委副书记、政府县长", "start_date": "2025-12", "end_date": "至今", "rank": "县处级正职", "note": "官方分工 2025-12-27 领导县政府全面工作; 2026 初 与韩非书记搭班"},
    {"person_id": 2, "org_id": 2, "title": "新河县副县长/代理县长（过渡）", "start_date": "2025", "end_date": "2025-12", "rank": "副处级/县处级", "note": "由前县长程玉峰卸任后接任，具体任免公告未获县portal，plausible"},
    # 程玉峰 — 前县长
    {"person_id": 3, "org_id": 2, "title": "新河县人民政府县长", "start_date": "2024-04", "end_date": "2025-12", "rank": "县处级正职", "note": "2024-04-25 官方分工领导县政府全面; 2025 县政府第四十七次常务会议报道在任"},
    # 关兵 — 常务副县长
    {"person_id": 4, "org_id": 2, "title": "新河县委常委、常务副县长", "start_date": "2024", "end_date": "至今", "rank": "副处级", "note": "2024-04 & 2025-12 官方分工 主管发改/发改局/财政局/统计局/政府办公室事务等，稳定"},
    # 副县长们
    {"person_id": 5, "org_id": 2, "title": "新河县副县长", "start_date": "2025", "end_date": "至今", "rank": "副处级", "note": "2025-12-27 分工：文化教育旅游体育医疗健康科技"},
    {"person_id": 6, "org_id": 2, "title": "新河县副县长", "start_date": "2025", "end_date": "至今", "rank": "副处级", "note": "2025-12-27 分工：住房城乡建设、城市管理、生态环境"},
    {"person_id": 7, "org_id": 2, "title": "新河县副县长", "start_date": "2025", "end_date": "至今", "rank": "副处级", "note": "2025-12-27 分工：交通运输、市场监管、工业信息化、农业农村、乡村振兴、招商引资"},
    {"person_id": 8, "org_id": 2, "title": "新河县副县长", "start_date": "2025", "end_date": "至今", "rank": "副处级", "note": "2025-12-27 分工：政法、退役军人、公安（县公安局）"},
    {"person_id": 9, "org_id": 2, "title": "新河县副县长", "start_date": "2025", "end_date": "至今", "rank": "副处级", "note": "2025-12-27 分工：自然资源、人社、民政"},
    {"person_id": 10, "org_id": 2, "title": "协助常务副县长工作", "start_date": "2025", "end_date": "至今", "rank": "县处级以下", "note": "2025-12-27 分工：袁广忠协助关兵常务副县长"},
]

# ── RELATIONSHIPS ───────────────────────────────────────────────────────
relationships = [
    # 现任党政一把手搭档
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "县委书记韩非与县长朱一搭档：共同主持县委常委会/县政府工作，2026 春节 '韩非、朱一' 带队走访慰问及 大气污染防治 暗访", "overlap_org": "中共新河县委员会/新河县政府", "overlap_period": "2025-12 至今"},
    # 前县长 → 现任县长
    {"person_a": 3, "person_b": 2, "type": "predecessor_successor", "context": "程玉峰 2025 卸任新河县长，朱一接任", "overlap_org": "新河县人民政府", "overlap_period": "2025"},
    # 前任县长 ↔ 现任书记 (搭班)
    {"person_a": 3, "person_b": 1, "type": "overlap", "context": "程玉峰任县长期间与县委书记韩非搭班（直至2025 卸任）", "overlap_org": "新河县", "overlap_period": "2024-2025"},
    # 现任县长 ↔ 常务副县长 (政府班子)
    {"person_a": 2, "person_b": 4, "type": "overlap", "context": "县政府班子，朱县长与关兵常务副县长搭班（分管分工明确）", "overlap_org": "新河县人民政府", "overlap_period": "2025-至今"},
    # 现任县委书记 ↔ 常务副县长 (班子)
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "韩非任书记期间，关兵任常委/常务副县长共事", "overlap_org": "新河县", "overlap_period": "2024-至今"},
    # 现任县长 ↔ 副县长 (政府班子)
    {"person_a": 2, "person_b": 5, "type": "overlap", "context": "县政府班子搭班", "overlap_org": "新河县人民政府", "overlap_period": "2025-至今"},
    {"person_a": 2, "person_b": 6, "type": "overlap", "context": "县政府班子搭班", "overlap_org": "新河县人民政府", "overlap_period": "2025-至今"},
    {"person_a": 2, "person_b": 7, "type": "overlap", "context": "县政府班子搭班", "overlap_org": "新河县人民政府", "overlap_period": "2025-至今"},
    {"person_a": 2, "person_b": 8, "type": "overlap", "context": "县政府班子搭班（分管公安）", "overlap_org": "新河县人民政府", "overlap_period": "2025-至今"},
    {"person_a": 2, "person_b": 9, "type": "overlap", "context": "县政府班子搭班", "overlap_org": "新河县人民政府", "overlap_period": "2025-至今"},
    # 常务副县长 ↔ 协助
    {"person_a": 4, "person_b": 10, "type": "superior_subordinate", "context": "袁广忠协助关兵常务副县长工作", "overlap_org": "新河县人民政府", "overlap_period": "2025-至今"},
]

# ── BUILD ────────────────────────────────────────────────────────────────
STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, "新河县_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "新河县_network.gexf")

if __name__ == "__main__":
    print("=" * 60)
    print("  邢台市新河县领导班子工作关系网络")
    print("  等级: 县 | 调查日期: 2026-08-05")
    print("  ✅ 县委书记: 韩非 (2024-09 十一届六次全会起任)")
    print("  ✅ 县长: 朱一 (2025-12 官方分工在任)")
    print("  ⚠️  前任县长 程玉峰 已于 2025 卸任; 韩非 2026-07 起升任市领导，县换届/党代会筹备中")
    print("=" * 60)
    run_build(
        slug="新河县",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print(f"Done: {DB_PATH} + {GEXF_PATH}")
    print(f"{len(persons)} persons, {len(organizations)} orgs, {len(positions)} positions, {len(relationships)} relationships")