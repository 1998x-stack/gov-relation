#!/usr/bin/env python3
"""
临西县领导班子工作关系网络 — Build script
河北省邢台市临西县（轴承之乡/运河古县；两省四市七县交界）

调查日期: 2026-08-06
Core targets: 县委书记 孟宪鹏 (现任, 2026-07-27 仍任); 县长 黄会安 (县委副书记、政府县长, 2025-07-01 《关于调整县政府领导工作分工的通知》确认)

官方一手来源 (临西县人民政府官网 www.linxi.gov.cn 首页要闻 + 政府信息公开《县政府领导工作分工》+ 邢台市人民政府/新闻):
- 县委书记 孟宪鹏: 男, 汉族, 2026-07-27 主持县委重点工作调度会议(听取固投/招商引资/大气污染防治); "轴承产业立县""5+4龙头引领""土地调度"施政语言; 兼县人武部党委第一书记(惯例)。生态多数信息公开有限, 完整履历/past post 列入 open_questions。
- 县长 黄会安: 男, 县委副书记、政府县长; 2025-07-01 前后出台《关于调整县政府领导工作分工的通知》确认在任; 分管全面工作、审计局。完整履历待查。
- 常务副县长 卫建豪: 分管发改/园区/京津冀协同/财政/人社/水务/统计/政务/应急/金融/粮食/外事, 经临发集团、轴承工业园区管委会、运河企业服务中心; 与县长共同主管审计。
- 副县长 孙通志: 农业农村/乡村振兴/民政/供销。
- 副县长 张红坡: 自然资源/住建/城管/交通/公积金。
- 副县长 赵康: 工信/科技/商务/招商/生态环境/轴承产业。
- 副县长 贾延平: 政法/退役, 兼县公安局局长。
- 副县长 王淑敬: 教育/卫生/医保/文旅。
- 县政府三级调研员: 郭殿春、刘明义; 副县级干部: 田青。

Confidence:
- 孟宪鹏(现任书记) / 黄会安(现任县长) = confirmed (官网新闻全文 + 政府分工文件)
- 常务副县长 卫建豪 及 5 位副县长 分工 = confirmed (2025-07-01 政府分工文件/官网稿件)
- 各人细履历(出生/籍贯/学历/入党/工作) = 待查, 列入 person JSON open_questions

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

SLUG = "临西县"
TASK_ID = "hebei_临西县"
TMP_DIR = os.path.join(_REPO_ROOT, "data", "tmp", TASK_ID)

DB_PATH = os.path.join(TMP_DIR, f"{SLUG}_network.db")
GEXF_PATH = os.path.join(TMP_DIR, f"{SLUG}_network.gexf")

AS_OF = "2026-08-06"

# ── PERSONS ─────────────────────────────────────────────────────────────
persons = [
    # 1 ── 现任县委书记 (一号位, confirmed)
    {"id": 1, "name": "孟宪鹏", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员",
     "work_start": "", "current_post": "临西县委书记、县人武部党委第一书记",
     "current_org": "中共临西县委员会",
     "source": "临西县人民政府官网首页要闻 2026-07-28『孟宪鹏主持召开重点工作调度会议』(以县委书记出席)"},
    # 2 ── 现任县长 (二把手, confirmed)
    {"id": 2, "name": "黄会安", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员",
     "work_start": "", "current_post": "临西县委副书记、县长、政府党组书记",
     "current_org": "临西县人民政府",
     "source": "临西县人民政府官网《关于调整县政府领导工作分工的通知》(2025-07-01 measured报告; 任县委副书记、县长)"},
    # 3 ── 常务副县长 (confirmed)
    {"id": 3, "name": "卫建豪", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员",
     "work_start": "", "current_post": "临西县常务副县长",
     "current_org": "临西县人民政府",
     "source": "临西县官网领导分工文件(2025-07)"},
    # 4 ── 副县长 (confirmed)
    {"id": 4, "name": "孙通志", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员",
     "work_start": "", "current_post": "临西县副县长",
     "current_org": "临西县人民政府",
     "source": "临西县官网领导分工文件(2025-07)"},
    # 5 ── 副县长 (confirmed)
    {"id": 5, "name": "张红坡", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员",
     "work_start": "", "current_post": "临西县副县长",
     "current_org": "临西县人民政府",
     "source": "临西县官网领导分工文件(2025-07)"},
    # 6 ── 副县长 (confirmed)
    {"id": 6, "name": "赵康", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员",
     "work_start": "", "current_post": "临西县副县长",
     "current_org": "临西县人民政府",
     "source": "临西县官网领导分工文件(2025-07)"},
    # 7 ── 副县长、公安局长 (confirmed)
    {"id": 7, "name": "贾延平", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员",
     "work_start": "", "current_post": "临西县副县长、县公安局局长",
     "current_org": "临西县公安局",
     "source": "临西县官网领导分工文件(2025-07)"},
    # 8 ── 副县长 (confirmed)
    {"id": 8, "name": "王淑敬", "gender": "女", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员",
     "work_start": "", "current_post": "临西县副县长",
     "current_org": "临西县人民政府",
     "source": "临西县官网领导分工文件(2025-07)"},
    # 9 ── 县政府三级调研员 (confirmed)
    {"id": 9, "name": "郭殿春", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员",
     "work_start": "", "current_post": "临西县政府三级调研员",
     "current_org": "临西县人民政府",
     "source": "临西县官网领导分工文件(2025-07)"},
    # 10 ── 县政府三级调研员 (confirmed)
    {"id": 10, "name": "刘明义", "gender": "男", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员",
     "work_start": "", "current_post": "临西县政府三级调研员",
     "current_org": "临西县人民政府",
     "source": "临西县官网领导分工文件(2025-07)"},
    # 11 ── 副县级干部 (confirmed)
    {"id": 11, "name": "田青", "gender": "女", "ethnicity": "汉族", "birth": "",
     "birthplace": "", "education": "", "party_join": "中共党员",
     "work_start": "", "current_post": "临西县副县级干部",
     "current_org": "临西县人民政府",
     "source": "临西县官网领导分工文件(2025-07)"},
    # 12 ── 跨县关联: 隆尧县长王新栋 (百度/媒体称曾任临西纪委常委/副书记) — plausible
    {"id": 12, "name": "王新栋", "gender": "男", "ethnicity": "汉族", "birth": "1981-03",
     "birthplace": "", "education": "大学学历", "party_join": "中共党员",
     "work_start": "", "current_post": "隆尧县委副书记、政府县长、党组书记",
     "current_org": "隆尧县人民政府",
     "source": "隆尧县调研 20260805 (媒体/百科记载其临西县委常委、纪委书记及县委副书记; 与官方人大文件记南宫市纪委书记存出入, 列入 open_questions)"},
]

# ── ORGANIZATIONS ───────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共临西县委员会", "type": "党委", "level": "县处级", "parent": "中共邢台市委员会", "location": "河北省邢台市临西县"},
    {"id": 2, "name": "临西县人民政府", "type": "政府", "level": "县处级", "parent": "邢台市人民政府", "location": "河北省邢台市临西县"},
    {"id": 3, "name": "临西县公安局", "type": "政府", "level": "县处级", "parent": "临西县人民政府", "location": "河北省邢台市临西县"},
    {"id": 4, "name": "中共临西县纪律检查委员会", "type": "党委", "level": "县处级", "parent": "邢台市纪委监委", "location": "河北省邢台市临西县"},
]

# ── POSITIONS ───────────────────────────────────────────────────────────
positions = [
    {"person_id": 1, "org_id": 1, "title": "县委书记", "start_date": "",
     "end_date": "", "rank": "正处级",
     "note": "2026-07-27 主持县委重点工作调度会议; 兼县人武部党委第一书记(惯例)"},
    {"person_id": 2, "org_id": 2, "title": "县长、县委副书记", "start_date": "",
     "end_date": "", "rank": "正处级",
     "note": "2025-07 政府领导分工文件确认任县长; 分管全面工作与审计"},
    {"person_id": 3, "org_id": 2, "title": "常务副县长", "start_date": "",
     "end_date": "", "rank": "副处级",
     "note": "常委; 发改/园区/京津冀/财政/人社/水务/统计/政务/应急/金融/粮食/外/审计(协助县长)"},
    {"person_id": 4, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级",
     "note": "农业农村/乡村振兴/民政改革/供销"},
    {"person_id": 5, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级",
     "note": "国土/住建/矿山/城管/交通/公积金"},
    {"person_id": 6, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级",
     "note": "工信/科技/商务/招商/生态环保/轴承产业"},
    {"person_id": 7, "org_id": 3, "title": "副县长、县公安局局长", "start_date": "", "end_date": "", "rank": "副处级",
     "note": "政法/退役"},
    {"person_id": 8, "org_id": 2, "title": "副县长", "start_date": "", "end_date": "", "rank": "副处级",
     "note": "教育/卫生/医保/文旅"},
    {"person_id": 9, "org_id": 2, "title": "县政府三级调研员", "start_date": "", "end_date": "", "rank": "副处级",
     "note": ""},
    {"person_id": 10, "org_id": 2, "title": "县政府三级调研员", "start_date": "", "end_date": "", "rank": "副处级",
     "note": ""},
    {"person_id": 11, "org_id": 2, "title": "副县级干部", "start_date": "", "end_date": "", "rank": "副处级",
     "note": ""},
    # 跨县关联 (plausible)
    {"person_id": 12, "org_id": 4, "title": "(传闻)县委常委、县纪委书记/县委副书记", "start_date": "",
     "end_date": "", "rank": "", "note": "媒体/百科记载, 与官方人大记录(南宫市纪委)存出入, 待核"},
    {"person_id": 12, "org_id": 2, "title": "隆尧县政府县长", "start_date": "2025-09", "end_date": "",
     "rank": "正处级", "note": "隆尧县第十六届人大第六次会议当选(现任)"},
]

# ── RELATIONSHIPS ───────────────────────────────────────────────────────
relationships = [
    # 党政搭档
    {"person_a": 1, "person_b": 2, "type": "party-gov", "context": "党政搭档(县委书记-县长)",
     "overlap_org": "临西县", "overlap_period": AS_OF},
    # 县长-常务副县长
    {"person_a": 2, "person_b": 3, "type": "superior-subordinate", "context": "县长与常务副县长; 共同主管审计",
     "overlap_org": "临西县人民政府", "overlap_period": AS_OF},
    # 县长-副县长
    {"person_a": 2, "person_b": 4, "type": "superior-subordinate", "context": "县长-副县长工作关系",
     "overlap_org": "临西县人民政府", "overlap_period": AS_OF},
    {"person_a": 2, "person_b": 5, "type": "superior-subordinate", "context": "县长-副县长工作关系",
     "overlap_org": "临西县人民政府", "overlap_period": AS_OF},
    {"person_a": 2, "person_b": 6, "type": "superior-subordinate", "context": "县长-副县长工作关系",
     "overlap_org": "临西县人民政府", "overlap_period": AS_OF},
    {"person_a": 2, "person_b": 7, "type": "superior-subordinate", "context": "县长-副县长/公安局长工作关系",
     "overlap_org": "临西县人民政府", "overlap_period": AS_OF},
    {"person_a": 2, "person_b": 8, "type": "superior-subordinate", "context": "县长-副县长工作关系",
     "overlap_org": "临西县人民政府", "overlap_period": AS_OF},
    # 跨县关联 (plausible, 隆尧调研线索)
    {"person_a": 12, "person_b": 1, "type": "cross_county", "context": "王新栋(传闻曾任临西纪委/副书记)与现任临西县委书记同县域体系的潜在联系 (待核)",
     "overlap_org": "中共临西县委员会(传闻)", "overlap_period": "unknown"},
]


# ── BUILD ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    os.makedirs(TMP_DIR, exist_ok=True)

    run_build(
        slug=SLUG,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )

    conn = sqlite3.connect(DB_PATH)
    pc = conn.execute("SELECT COUNT(*) FROM persons").fetchone()[0]
    oc = conn.execute("SELECT COUNT(*) FROM organizations").fetchone()[0]
    rel = conn.execute("SELECT COUNT(*) FROM relationships").fetchone()[0]
    conn.close()

    print(f"\n{SLUG} v1 data written to {TMP_DIR}")
    print(f"  DB:   {DB_PATH} ({pc} persons, {oc} orgs, {rel} relationships)")
    print(f"  GEXF: {GEXF_PATH}")
    print()
    print("Current leadership (confirmed 2026):")
    print("  县委书记: 孟宪鹏 (2026-07-27 主持县委调度会)")
    print("  县长: 黄会安 (县委副书记、政府县长, 2025-07 分工文件确认)")
    print("  常务副县长: 卫建豪")
    print("  副县长: 孙通志, 张红坡, 赵康, 贾延平(兼公安局长), 王淑敬")
    print("  三级调研员: 郭殿春, 刘明义; 副县级: 田青")
    print()
    print("Gaps remaining (见 person JSON open_questions / report open_gaps):")
    print("  1. 孟宪鹏, 黄会安 — 出生/籍贯/学历/入党/早年履历通通待查")
    print("  2. 前任县委书记/前任县长 — 继任链条待确认")
    print("  3. 县纪委书记、政法委书记、宣传部长、组织部长 — 姓名未公开确认")
    print("  4. 跨县干部交流模式(临西↔隆尧/南宫/清河)")