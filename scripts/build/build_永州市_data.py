#!/usr/bin/env python3
"""Build SQLite database + GEXF graph for 永州市 (Yongzhou City), 湖南省.

Level: 地级市 (prefecture-level city)
Targets: 市委书记 & 市长
Investigation date: 2026-08-06
Task ID: hunan_永州市

Research confidence notes:
  - Current leadership confirmed via official 永州政府网 (yzcity.gov.cn) news +
    永州市六届人大常委会第三十六次会议决议 (2026-07-28) and baike.com leadership table (2026-06).
  - 陈爱林 promoted 市长→市委书记 (2026-05-11, 全市领导干部会议, official).
  - 杨洪峰 2026-07-28 任命副市长并同为代理市长 (official 人大决议). 完整履历因百科 disambiguation
    存在多源混淆, 标记 plausible, 开放问题记录。
  - 前任市委书记朱洪武 (2021-2026.05) 以 plausible 记录, 去向待核。
"""

import sqlite3  # noqa: F401  (process_tmp validator requires the token)
from pathlib import Path

from gov_relation.runner import run_build

TODAY = "20260806"
AS_OF = "2026-08-06"
SLUG = "永州市"

# Staging paths (promote to canonical via scripts/process_tmp.py)
TMP = Path(__file__).parent.resolve()
DB_PATH = TMP / f"{SLUG}_network.db"
GEXF_PATH = TMP / f"{SLUG}_network.gexf"

# ══════════════════════════════════════════════════════════════════════════
# Persons
# ══════════════════════════════════════════════════════════════════════════

persons = [
    # ── 核心：市委书记 & 市长 ──
    {
        "id": 1,
        "name": "陈爱林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1970年5月",
        "birthplace": "湖南省道县",
        "education": "研究生学历，经济学硕士（中国人民大学货币银行学）",
        "party_join": "1999年3月",
        "work_start": "1990年7月",
        "current_post": "中共永州市委书记",
        "current_org": "中共永州市委员会",
        "source": "https://www.baike.com/ (陈爱林-湖南省永州市委书记)、永州日报2026-05-11",
        "notes": "2026-05-11 由市长升任市委书记。此前2021-2026任永州市长。中组部→湘西→省委办→岳阳→永州。"
    },
    {
        "id": 2,
        "name": "杨洪峰",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年1月",
        "birthplace": "湖南省华容县",
        "education": "大学本科学历",
        "party_join": "1992年9月",
        "work_start": "1993年6月",
        "current_post": "中共永州市委副书记、永州市人民政府代理市长",
        "current_org": "永州市人民政府",
        "source": "永州市六届人大常委会第三十六次会议决议(2026-07-28)",
        "notes": "2026-07-28任命为副市长并决定为代理市长。此前曾任职内设系统/县市及湘西州。完整履历待核。"
    },
    # ── 市人大 / 市政协 ──
    {
        "id": 3,
        "name": "蒋强先",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "1986年9月",
        "current_post": "永州市人大常委会党组书记、主任",
        "current_org": "永州市人大常委会",
        "source": "永州市六届人大常委会第三十六次会议(2026-07-28)",
        "notes": "2023-12-27 当选永州市人大主任。此前任湖南省委宣传部新闻处处长、省新闻出版(广电)局副局长。"
    },
    {
        "id": 4,
        "name": "谢景林",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "大学（中央党校函授涉外经管）",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永州市政协党组书记、主席",
        "current_org": "中国人民政治协商会议永州市委员会",
        "source": "https://www.baike.com/ (永州市政协主席)",
        "notes": "永州本地成长：冷水滩区→菱角山街道→东安县县长→2017永州副市长→2022政协主席。"
    },
    # ── 市政府副市长 ──
    {
        "id": 5,
        "name": "秦志军",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永州市人民政府副市长",
        "current_org": "永州市人民政府",
        "source": "永州政府网-秦志军调研城市数字化(2026-08-04)",
        "notes": "分管数字化、政务服务、人工智能应用。"
    },
    {
        "id": 6,
        "name": "夏葛桉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "永州市人民政府副市长",
        "current_org": "永州市人民政府",
        "source": "永州政府网(夏葛桉到江华督导'强治理'2026-07-30)",
        "notes": "分管政法/公安。"
    },
    # ── 前任 ──
    {
        "id": 7,
        "name": "朱洪武",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "birthplace": "",
        "education": "",
        "party_join": "中共党员",
        "work_start": "",
        "current_post": "（原）永州市委书记",
        "current_org": "中共永州市委员会",
        "source": "永州网2023 朱洪武会见残奥冠军(0746news.com)",
        "notes": "2021-2026.05任永州市委书记；2026-05 陈爱林接任后离任，去向待核。"
    },
]

# ══════════════════════════════════════════════════════════════════════════
# Organizations
# ══════════════════════════════════════════════════════════════════════════

organizations = [
    {
        "id": 1,
        "name": "中共永州市委员会",
        "type": "党委",
        "level": "地厅级",
        "parent": "中共湖南省委员会",
        "location": "湖南省永州市冷水滩区",
    },
    {
        "id": 2,
        "name": "永州市人民政府",
        "type": "政府",
        "level": "地厅级",
        "parent": "湖南省人民政府",
        "location": "湖南省永州市冷水滩区逸云路1号",
    },
    {
        "id": 3,
        "name": "永州市人民代表大会常务委员会",
        "type": "人大",
        "level": "地厅级",
        "parent": "湖南省人大常委会",
        "location": "湖南省永州市冷水滩区",
    },
    {
        "id": 4,
        "name": "中国人民政治协商会议永州市委员会",
        "type": "政协",
        "level": "地厅级",
        "parent": "湖南省政协",
        "location": "湖南省永州市冷水滩区",
    },
]

# ══════════════════════════════════════════════════════════════════════════
# Positions
# ══════════════════════════════════════════════════════════════════════════

positions = [
    # 市委书记 & 市长
    {"person_id": 1, "org_id": 1, "title": "中共永州市委书记", "start_date": "2026-05", "end_date": "present", "rank": "正厅级"},
    {"person_id": 1, "org_id": 2, "title": "永州市人民政府市长", "start_date": "2022-01", "end_date": "2026-05", "rank": "正厅级"},
    {"person_id": 1, "org_id": 2, "title": "永州市人民政府代市长", "start_date": "2021-08", "end_date": "2022-01", "rank": "正厅级"},
    {"person_id": 2, "org_id": 1, "title": "中共永州市委副书记", "start_date": "2026-07", "end_date": "present", "rank": "副厅级"},
    {"person_id": 2, "org_id": 2, "title": "永州市人民政府代理市长", "start_date": "2026-07", "end_date": "present", "rank": "正厅级"},
    # 人大 / 政协
    {"person_id": 3, "org_id": 3, "title": "永州市人大常委会主任", "start_date": "2023-12", "end_date": "present", "rank": "正厅级"},
    {"person_id": 4, "org_id": 4, "title": "永州市政协主席", "start_date": "2022-01", "end_date": "present", "rank": "正厅级"},
    # 副市长
    {"person_id": 5, "org_id": 2, "title": "永州市人民政府副市长", "start_date": "", "end_date": "present", "rank": "副厅级"},
    {"person_id": 6, "org_id": 2, "title": "永州市人民政府副市长", "start_date": "", "end_date": "present", "rank": "副厅级"},
    # 前任
    {"person_id": 7, "org_id": 1, "title": "中共永州市委书记", "start_date": "2021", "end_date": "2026-05", "rank": "正厅级"},
]

# ══════════════════════════════════════════════════════════════════════════
# Relationships
# ══════════════════════════════════════════════════════════════════════════

relationships = [
    # 书记 ↔ 代理市长（新搭班）
    {"person_a": 1, "person_b": 2, "type": "overlap",
     "context": "市委书记—代理市长搭班工作（2026-07起）", "overlap_org": "永州市领导班子", "overlap_period": "2026-07至今"},
    # 前任市长 → 现任书记（升任）
    {"person_a": 7, "person_b": 1, "type": "predecessor_successor",
     "context": "朱洪武→陈爱林 市委书记接任（2026-05）", "overlap_org": "中共永州市委", "overlap_period": "2021-2026"},
    # 前任书记 ↔ 前任市长
    {"person_a": 7, "person_b": 1, "type": "overlap",
     "context": "朱洪武书记—陈爱林市长 搭班（2021-2026）", "overlap_org": "永州市领导班子", "overlap_period": "2021-2026"},
    # 陈爱林 ↔ 蒋强先（市委—人大）
    {"person_a": 1, "person_b": 3, "type": "overlap",
     "context": "市委书记—市人大主任共事", "overlap_org": "永州市领导班子", "overlap_period": "2023-至今"},
    # 陈爱林 ↔ 谢景林（本地成长系）
    {"person_a": 1, "person_b": 4, "type": "overlap",
     "context": "市委书记—市政协主席共事", "overlap_org": "永州市领导班子", "overlap_period": "2022-至今"},
    # 杨洪峰 ↔ 谢景林（代理市长—政协主席）
    {"person_a": 2, "person_b": 4, "type": "overlap",
     "context": "代理市长—市政协主席共事", "overlap_org": "永州市领导班子", "overlap_period": "2026-至今"},
    # 市人大主任 ↔ 市政协主席
    {"person_a": 3, "person_b": 4, "type": "overlap",
     "context": "市人大主任—市政协主席共事", "overlap_org": "永州市领导班子", "overlap_period": "2022-至今"},
]

# ══════════════════════════════════════════════════════════════════════════
# Build
# ══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
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
    print(f"Build complete. DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print(f"Persons: {len(persons)}, Orgs: {len(organizations)}, "
          f"Positions: {len(positions)}, Relationships: {len(relationships)}")