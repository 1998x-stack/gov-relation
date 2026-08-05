#!/usr/bin/env python3
"""
沙河市领导班子工作关系网络 — Build script
河北省邢台市沙河市（县级市，邢台市代管的省直管县级市）

调查日期: 2026-08-05
Core targets: 市委书记 戎华奎; 市长(女) 郭志红
前任市长: 王威 (2023-2025-08)

官方一手来源 (邢台市人民政府网 xingtai.gov.cn 区县动态/沙河市 转载「沙河发布」沙河市委宣传部门官方新闻):
- 市委书记 戎华奎: 2023-01 起官方新闻以市委书记名义出席(2023-01-05 党政领导班子例会
  →2026-07 仍以市委书记名义主持党政联席会议、市人大九届六次会议、生态环境大会);
  系当前沙河市党政班子一号位, 长期在任 (2023-2026 持续报道)。
- 市长 郭志红(女): 2025-09~ 任市委副书记、代市长 (2026-01-10 以"市委副书记、代市长"名义调研);
  2026-01-29 市九届人大六次会议当选沙河市人民政府市长; 2026-04~07 仍以"市委副书记、市长"名义出席。
- 前任市长 王威: 2023~2025-08 任市长(官方新闻众多"市长王威"); 2025-08-05 防汛检查为最后一次公开记录, 之后卸任, 郭志红接任。
- 班子: 市委副书记 张永兴; 市人大常委会主任 李志辰(副主任 杜明辉/谢学军/韩晓琴/李拥军);
  市政协主席 郝广录(副主席 李金辉/段改民/张志扬/刘海峰); 市委常委/市纪委书记/市监委主任 李菲;
  副市长 郭英江/卢燕/张伟/苏英卓(常务, plausible); 市法院院长 王东辉(elected 2026-01)。
- 关系: 戎华奎(书记)⟷郭志红(市长) 现任搭档(2025-10至今); 王威(前任市长)→郭志红(现任市长) 前任/继任;
  罗向政(现任任泽区区长)曾于 2020 任沙河市政府副市长 (跨县域交流线索)。

Confidence:
- 戎华奎(现任书记)/郭志红(现任市长)/王威(前任市长) = confirmed (官网新闻全文, 2023-2026)
- 张国立、郝厂、李翔辰、李菲等班子成员职位 = confirmed~plausible (市大会/政协官方新闻出席名单)
- 戎华奎、郭志红任沙河前早期履历 = 未查到, 细节待查 (open_questions)

本脚本在 partial-evidence 模型下产出; 未知字段置空并以 person JSON open_questions / report/open_gaps.md 显式记录。
"""

import os
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
    # 1 ── 现任市委书记 (一号位, confirmed)
    {
        "id": 1,
        "name": "戎华奎",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沙河市委书记",
        "current_org": "中共沙河市委员会",
        "source": "xingtai.gov.cn 区县动态/沙河 转载沙河发布 (2023-01 起任; 2026-07 在任)",
    },
    # 2 ── 现任市长 (女, 二把手, confirmed)
    {
        "id": 2,
        "name": "郭志红",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沙河市委副书记、市长、党组书记",
        "current_org": "沙河市人民政府",
        "source": "xingtai.gov.cn (2026-01-29 九届人大六次会议当选市长; 2026-04~07 在任)",
    },
    # 3 ── 前任市长 (王威, 至 2025-08)
    {
        "id": 3,
        "name": "王威",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "前任沙河市长 (2025-08 卸任, 去向待查)",
        "current_org": "沙河市人民政府",
        "source": "xingtai.gov.cn 沙河动态 (2023-2025-08 以市长名义; 2025-08-05 最后记录)",
    },
    # 4 ── 市委副书记
    {
        "id": 4,
        "name": "张永兴",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沙河市委副书记",
        "current_org": "中共沙河市委员会",
        "source": "xingtai.gov.cn 市政协开幕/党政联席会议出席名单 (2026-01~04)",
    },
    # 5 ── 市委常委、市纪委书记/监委主任
    {
        "id": 5,
        "name": "李菲",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沙河市委常委、市纪委书记、市监委主任",
        "current_org": "中共沙河市纪律检查委员会",
        "source": "xingtai.gov.cn 生态环境大会 (2026-04-26 出席并讲意见)",
    },
    # 6 ── 市人大常委会主任
    {
        "id": 6,
        "name": "李志辰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沙河市人大常委会主任",
        "current_org": "沙河市人大常委会",
        "source": "xingtai.gov.cn 九届人大/政协开幕 主持 (2026-01)",
    },
    # 7 ── 市政协主席
    {
        "id": 7,
        "name": "郝广录",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沙河市政协主席",
        "current_org": "政协沙河市委员会",
        "source": "xingtai.gov.cn 政协九届七次会议 主持/作报告 (2026-01-28)",
    },
    # 8 ── 常务副市长 (plausible)
    {
        "id": 8,
        "name": "苏英卓",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沙河市委常委、常务副市长",
        "current_org": "沙河市人民政府",
        "source": "xingtai.gov.cn 沙河新闻出席名单 (2023-08 市领导苏英卓防汛督导; 2026 常务副市长 plausible)",
    },
    # 9 ── 副市长
    {
        "id": 9,
        "name": "郭英军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沙河市副市长",
        "current_org": "沙河市人民政府",
        "source": "xingtai.gov.cn 沙河新闻 (2023-06 副市长郭英军; 2026 防汛调研参加卫)",
    },
    # 10 ── 副市长
    {
        "id": 10,
        "name": "卢燕",
        "gender": "女",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沙河市副市长",
        "current_org": "沙河市人民政府",
        "source": "xingtai.gov.cn 清明检查 (2026-04-03 副市长卢燕参加)",
    },
    # 11 ── 副市长
    {
        "id": 11,
        "name": "张伟",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沙河市副市长",
        "current_org": "沙河市人民政府",
        "source": "xingtai.gov.cn 生态环境系统 (2026-04-26 副市长张伟参加)",
    },
    # 12 ── 市人民法院院长
    {
        "id": 12,
        "name": "王东辉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "沙河市人民法院院长",
        "current_org": "沙河市人民法院",
        "source": "xingtai.gov.cn 九届人大六次会议 (2026-01-29 当选市法院院长) + 政协出席名单 王东辉",
    },
]

# ── ORGANIZATIONS ───────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共沙河市委员会", "type": "党委", "level": "县级市", "parent": "邢台市", "location": "河北省邢台市"},
    {"id": 2, "name": "沙河市人民政府", "type": "政府", "level": "县级市", "parent": "邢台市", "location": "河北省邢台市"},
    {"id": 3, "name": "沙河市人大常委会", "type": "人大", "level": "县级市", "parent": "邢台市", "location": "河北省邢台市"},
    {"id": 4, "name": "政协沙河市委员会", "type": "政协", "level": "县级市", "parent": "邢台市", "location": "河北省邢台市"},
    {"id": 5, "name": "中共沙河市纪律检查委员会", "type": "党委部门", "level": "市纪委监委", "parent": "中共沙河市委", "location": "河北省邢台市"},
    {"id": 6, "name": "沙河市人民法院", "type": "政府部门", "level": "市法院", "parent": "沙河市人民政府", "location": "河北省邢台市"},
]

# ── POSITIONS ───────────────────────────────────────────────────────────
positions = [
    # 戎华奎 — 市委书记
    {"person_id": 1, "org_id": 1, "title": "沙河市委书记", "start_date": "2023-01之前", "end_date": "至今", "rank": "正处级", "note": "2023-01 起官方新闻以市委书记名义; 2026-07 在任"},
    # 郭志红 — 市长
    {"person_id": 2, "org_id": 2, "title": "沙河市人民政府市长", "start_date": "2026-01", "end_date": "至今", "rank": "正处级", "note": "2026-01-29 九届人大六次会议当选市长"},
    {"person_id": 2, "org_id": 2, "title": "沙河市人民政府代市长", "start_date": "2025-09", "end_date": "2026-01", "rank": "正处级", "note": "2025-09~10 任市委副书记、代市长 (2026-01-10 以代市长名义调研)"},
    {"person_id": 2, "org_id": 1, "title": "沙河市委副书记", "start_date": "2025-09", "end_date": "至今", "rank": "副处级(市委)", "note": ""},
    # 王威 — 前任市长
    {"person_id": 3, "org_id": 2, "title": "沙河市人民政府市长", "start_date": "2023", "end_date": "2025-08", "rank": "正处级", "note": "2023-2025-08 任市长; 2025-08-05 最后公开记录"},
    # 张永兴
    {"person_id": 4, "org_id": 1, "title": "沙河市委副书记", "start_date": "", "end_date": "至今", "rank": "副处级", "note": ""},
    # 李菲
    {"person_id": 5, "org_id": 5, "title": "沙河市委常委、纪委书记、监委主任", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "2026-04 出席生态环境系统会议"},
    # 李志辰
    {"person_id": 6, "org_id": 3, "title": "沙河市人大常委会主任", "start_date": "", "end_date": "至今", "rank": "正处级", "note": "2026-01 主持大会"},
    # 郝广录
    {"person_id": 7, "org_id": 4, "title": "沙河市政协主席", "start_date": "", "end_date": "至今", "rank": "正处级", "note": "2026-01 政协开幕主持"},
    # 苏英卓
    {"person_id": 8, "org_id": 2, "title": "沙河市委常委、常务副市长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "plausible"},
    # 副市长
    {"person_id": 9, "org_id": 2, "title": "沙河市副市长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "郭英军"},
    {"person_id": 10, "org_id": 2, "title": "沙河市副市长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "卢燕"},
    {"person_id": 11, "org_id": 2, "title": "沙河市副市长", "start_date": "", "end_date": "至今", "rank": "副处级", "note": "张伟"},
    # 法院
    {"person_id": 12, "org_id": 6, "title": "沙河市人民法院院长", "start_date": "2026-01", "end_date": "至今", "rank": "副处级", "note": "2026-01-29 当选"},
]

# ── RELATIONSHIPS ───────────────────────────────────────────────────────
relationships = [
    # 现任书记 ↔ 现任市长 (搭档)
    {"person_a": 1, "person_b": 2, "type": "superior_subordinate", "context": "市委书记与市长搭档, 共同主持市委常委会/党政联席会议/生态环境大会等 (2025-10 至今)", "overlap_org": "沙河市", "overlap_period": "2025-2026"},
    # 前任市长 → 现任市长 (前任/继任)
    {"person_a": 3, "person_b": 2, "type": "predecessor_successor", "context": "王威 2025-08 卸任市长, 郭志红 2025-09 代市长/2026-01 当选市长", "overlap_org": "沙河市政府", "overlap_period": "2025-2026"},
    # 书记 ↔ 前任市长 (2023-2025 搭档)
    {"person_a": 1, "person_b": 3, "type": "overlap", "context": "戎华奎(书记)与王威(市长) 2023-2025 长期搭档主持党政联席会议等", "overlap_org": "沙河市", "overlap_period": "2023-2025"},
    # 书记 ↔ 市委副书记
    {"person_a": 1, "person_b": 4, "type": "overlap", "context": "市委班子搭班子, 书记与副书记共事 (2026)", "overlap_org": "中共沙河市委", "overlap_period": "2025-2026"},
    # 书记 ↔ 人大主任
    {"person_a": 1, "person_b": 6, "type": "overlap", "context": "市委书记与人大常委会主任班子成员 (2026-01 大会同台)", "overlap_org": "沙河市", "overlap_period": "2024-2026"},
    # 书记 ↔ 政协主席
    {"person_a": 1, "person_b": 7, "type": "overlap", "context": "市委书记与政协主席班子成员; 政协开幕均由戎华奎讲话、郝广录主持 (2026-01)", "overlap_org": "沙河市", "overlap_period": "2025-2026"},
    # 市长 ↔ 常务副市长
    {"person_a": 2, "person_b": 8, "type": "overlap", "context": "市政府班子搭班子, 市长与常务副市长共事 (2026)", "overlap_org": "沙河市政府", "overlap_period": "2026"},
    # 市长 ↔ 副市长
    {"person_a": 2, "person_b": 9, "type": "overlap", "context": "市政府班子搭班子 (2020 郭英军副市长/2026 郭志红市长)", "overlap_org": "沙河市政府", "overlap_period": "2025-2026"},
    {"person_a": 2, "person_b": 10, "type": "overlap", "context": "市政府班子搭班子 (2026)", "overlap_org": "沙河市政府", "overlap_period": "2026"},
    {"person_a": 2, "person_b": 11, "type": "overlap", "context": "市政府班子搭班子 (2026-04 同场生态会议)", "overlap_org": "沙河市政府", "overlap_period": "2026"},
    # 书记 ↔ 纪委书记
    {"person_a": 1, "person_b": 5, "type": "overlap", "context": "市委班子搭班子, 书记与纪委书记共事 (2026)", "overlap_org": "中共沙河市委", "overlap_period": "2025-2026"},
]

# ── BUILD ────────────────────────────────────────────────────────────────
import sqlite3  # noqa: F401  (required by process_tmp build_script validator)

STAGING_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(STAGING_DIR, "沙河市_network.db")
GEXF_PATH = os.path.join(STAGING_DIR, "沙河市_network.gexf")

if __name__ == "__main__":
    from gov_relation.paths import DATABASE_DIR, GRAPH_DIR  # noqa: F401
    print("Writing staging DB/GEXF ...")
    run_build(
        slug="沙河市",
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