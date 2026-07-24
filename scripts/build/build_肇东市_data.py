#!/usr/bin/env python3
"""Build 肇东市 (Zhaodong City, 绥化市, 黑龙江省) government network data.

Generated: 2026-07-24
Task: heilongjiang_肇东市
Level: 县级市
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure repo root is on sys.path so gov_relation module can be imported
_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from gov_relation.runner import run_build

SCRIPT_DIR = Path(__file__).resolve().parent
DB_PATH = SCRIPT_DIR / "肇东市_network.db"
GEXF_PATH = SCRIPT_DIR / "肇东市_network.gexf"

# ── Persons ──────────────────────────────────────────────────────────────────
# sqlite3 imported via gov_relation.schema (used by runner)
# ID scheme: 1xx = party secretaries, 2xx = mayors, 3xx = deputy secretaries,
# 4xx = standing committee, 5xx = vice mayors, 6xx =人大/政协

persons = [
    # -- Core leaders --
    {
        "id": 101,
        "name": "肖福凌",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1978年10月",
        "education": "",
        "party_join": "1999年12月",
        "work_start": "",
        "current_post": "市委书记、市长",
        "current_org": "中共肇东市委员会、肇东市人民政府",
        "source": "https://www.hljzhaodong.gov.cn/zd/c17/202607/c12_237814.shtml",
    },
    {
        "id": 102,
        "name": "吕江",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "原市委书记（至2026年6-7月）",
        "current_org": "中共肇东市委员会（前任）",
        "source": "https://www.hljzhaodong.gov.cn/zd/c32/202606/c12_235040.shtml",
    },
    # -- Deputy secretary --
    {
        "id": 301,
        "name": "周海波",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年11月",
        "education": "",
        "party_join": "1997年6月",
        "work_start": "",
        "current_post": "市委副书记",
        "current_org": "中共肇东市委员会",
        "source": "https://www.hljzhaodong.gov.cn/zd/c18/202408/c12_190893.shtml",
    },
    # -- Standing committee members --
    {
        "id": 401,
        "name": "姜涛",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1971年12月",
        "education": "",
        "party_join": "1999年10月",
        "work_start": "",
        "current_post": "市委常委、纪委书记、监委主任",
        "current_org": "中共肇东市纪律检查委员会、肇东市监察委员会",
        "source": "https://www.hljzhaodong.gov.cn/zd/c19/202405/c12_185340.shtml",
    },
    {
        "id": 402,
        "name": "郭戬威",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共肇东市委员会",
        "source": "https://www.hljzhaodong.gov.cn/zd/c15/ldsc.shtml",
    },
    {
        "id": 403,
        "name": "李世玉",
        "gender": "男",
        "ethnicity": "汉族",
        "birth": "1975年2月",
        "education": "",
        "party_join": "1999年12月",
        "work_start": "",
        "current_post": "市委常委、常务副市长",
        "current_org": "肇东市人民政府",
        "source": "https://www.hljzhaodong.gov.cn/zd/c19/202404/c12_182638.shtml",
    },
    {
        "id": 404,
        "name": "刘立",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共肇东市委员会",
        "source": "https://www.hljzhaodong.gov.cn/zd/c15/ldsc.shtml",
    },
    {
        "id": 405,
        "name": "单奎",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、副市长",
        "current_org": "肇东市人民政府",
        "source": "https://www.hljzhaodong.gov.cn/zd/c15/ldsc.shtml",
    },
    {
        "id": 406,
        "name": "杜美玲",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共肇东市委员会",
        "source": "https://www.hljzhaodong.gov.cn/zd/c15/ldsc.shtml",
    },
    {
        "id": 407,
        "name": "魏俊明",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委、副市长",
        "current_org": "肇东市人民政府",
        "source": "https://www.hljzhaodong.gov.cn/zd/c15/ldsc.shtml",
    },
    {
        "id": 408,
        "name": "李博",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市委常委",
        "current_org": "中共肇东市委员会",
        "source": "https://www.hljzhaodong.gov.cn/zd/c19/202607/c12_237964.shtml",
    },
    # -- Vice mayors (in addition to standing committee members who are also vice mayors) --
    {
        "id": 501,
        "name": "王显刚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "肇东市人民政府",
        "source": "https://www.hljzhaodong.gov.cn/zd/c25/202308/c12_fb6d806cf39141eba86ff61db79510dc.shtml",
    },
    {
        "id": 502,
        "name": "韩晓蕾",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "肇东市人民政府",
        "source": "https://www.hljzhaodong.gov.cn/zd/c25/202408/c12_190896.shtml",
    },
    {
        "id": 503,
        "name": "刘闯",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "肇东市人民政府",
        "source": "https://www.hljzhaodong.gov.cn/zd/c25/202404/c12_182486.shtml",
    },
    {
        "id": 504,
        "name": "李纯魁",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "肇东市人民政府",
        "source": "https://www.hljzhaodong.gov.cn/zd/c25/202407/c12_187734.shtml",
    },
    {
        "id": 505,
        "name": "徐东华",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "副市长",
        "current_org": "肇东市人民政府",
        "source": "https://www.hljzhaodong.gov.cn/zd/c25/202407/c12_187735.shtml",
    },
    # -- 人大 --
    {
        "id": 601,
        "name": "吕鑫",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会主任",
        "current_org": "肇东市人大常委会",
        "source": "https://www.hljzhaodong.gov.cn/zd/c21/202308/c12_5d6bdc436c154ee1b842be5772c52a92.shtml",
    },
    {
        "id": 602,
        "name": "张桂荣",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会副主任",
        "current_org": "肇东市人大常委会",
        "source": "https://www.hljzhaodong.gov.cn/zd/c22/202404/c12_182712.shtml",
    },
    {
        "id": 603,
        "name": "葛刚",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会副主任",
        "current_org": "肇东市人大常委会",
        "source": "https://www.hljzhaodong.gov.cn/zd/c22/202308/c12_ee7dba40891e4eed8fe4f27ad4d32ec6.shtml",
    },
    {
        "id": 604,
        "name": "潘振生",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会副主任",
        "current_org": "肇东市人大常委会",
        "source": "https://www.hljzhaodong.gov.cn/zd/c22/202308/c12_e57b47f8d8e84ea7857f2a9936eb413e.shtml",
    },
    {
        "id": 605,
        "name": "臧艳华",
        "gender": "女",
        "ethnicity": "",
        "birth": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市人大常委会副主任",
        "current_org": "肇东市人大常委会",
        "source": "https://www.hljzhaodong.gov.cn/zd/c22/202308/c12_900d7de61e984cff9e5b2bb3ed949800.shtml",
    },
    # -- 政协 --
    {
        "id": 701,
        "name": "田宇",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协主席（候选人）",
        "current_org": "肇东市政协",
        "source": "https://www.hljzhaodong.gov.cn/zd/c27/202607/c12_237967.shtml",
    },
    {
        "id": 702,
        "name": "赵传虹",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协副主席",
        "current_org": "肇东市政协",
        "source": "https://www.hljzhaodong.gov.cn/zd/c28/202308/c12_03fa716f9f4546edbee4c685b0292e7a.shtml",
    },
    {
        "id": 703,
        "name": "惠涛",
        "gender": "",
        "ethnicity": "",
        "birth": "",
        "education": "",
        "party_join": "",
        "work_start": "",
        "current_post": "市政协副主席",
        "current_org": "肇东市政协",
        "source": "https://www.hljzhaodong.gov.cn/zd/c28/202501/c12_201990.shtml",
    },
]

# ── Organizations ─────────────────────────────────────────────────────────────

organizations = [
    {"id": 1, "name": "中共肇东市委员会", "type": "党委", "level": "县级", "parent": "中共绥化市委员会", "location": "肇东市"},
    {"id": 2, "name": "肇东市人民政府", "type": "政府", "level": "县级", "parent": "绥化市人民政府", "location": "肇东市"},
    {"id": 3, "name": "中共肇东市纪律检查委员会", "type": "纪委", "level": "县级", "parent": "中共绥化市纪律检查委员会", "location": "肇东市"},
    {"id": 4, "name": "肇东市监察委员会", "type": "纪委", "level": "县级", "parent": "绥化市监察委员会", "location": "肇东市"},
    {"id": 5, "name": "肇东市人大常委会", "type": "人大", "level": "县级", "parent": "绥化市人大常委会", "location": "肇东市"},
    {"id": 6, "name": "肇东市政协", "type": "政协", "level": "县级", "parent": "绥化市政协", "location": "肇东市"},
    {"id": 7, "name": "肇东经济开发区", "type": "开发区", "level": "省级", "parent": "肇东市人民政府", "location": "肇东市"},
]

# ── Positions ─────────────────────────────────────────────────────────────────

positions = [
    # 肖福凌
    {"person_id": 101, "org_id": 1, "title": "市委书记", "start_date": "2026-07", "end_date": "present", "rank": "正处级", "note": "接替吕江，近期上任"},
    {"person_id": 101, "org_id": 2, "title": "市长", "start_date": "", "end_date": "present", "rank": "正处级", "note": "同时兼任市委书记和市长"},
    # 吕江（前任）
    {"person_id": 102, "org_id": 1, "title": "市委书记", "start_date": "", "end_date": "2026-06", "rank": "正处级", "note": "2026年6月4日仍在主持市委常委会"},
    # 周海波
    {"person_id": 301, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 姜涛
    {"person_id": 401, "org_id": 3, "title": "市委常委、纪委书记", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 401, "org_id": 4, "title": "监委主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 郭戬威
    {"person_id": 402, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 李世玉
    {"person_id": 403, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 403, "org_id": 2, "title": "常务副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": "负责政府常务、城乡建设、自然资源、生态环境、应急管理、信访"},
    # 刘立
    {"person_id": 404, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 单奎
    {"person_id": 405, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 405, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 杜美玲
    {"person_id": 406, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 魏俊明
    {"person_id": 407, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 407, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 李博
    {"person_id": 408, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "present", "rank": "副处级", "note": "2026年7月新入常"},
    # 王显刚
    {"person_id": 501, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 韩晓蕾
    {"person_id": 502, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 刘闯
    {"person_id": 503, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 李纯魁
    {"person_id": 504, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 徐东华
    {"person_id": 505, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 人大
    {"person_id": 601, "org_id": 5, "title": "主任", "start_date": "", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 602, "org_id": 5, "title": "副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 603, "org_id": 5, "title": "副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 604, "org_id": 5, "title": "副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 605, "org_id": 5, "title": "副主任", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    # 政协
    {"person_id": 701, "org_id": 6, "title": "主席（候选人）", "start_date": "2026-07", "end_date": "present", "rank": "正处级", "note": ""},
    {"person_id": 702, "org_id": 6, "title": "副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
    {"person_id": 703, "org_id": 6, "title": "副主席", "start_date": "", "end_date": "present", "rank": "副处级", "note": ""},
]

# ── Relationships ─────────────────────────────────────────────────────────────

relationships = [
    # 肖福凌 — 吕江（前后任）
    {
        "person_a": 101,
        "person_b": 102,
        "type": "predecessor_successor",
        "context": "肖福凌接替吕江任肇东市委书记",
        "overlap_org": "中共肇东市委员会",
        "overlap_period": "2026年6-7月交接",
    },
    # 肖福凌 — 周海波（党政搭档？肖同时担任书记和市长，周为专职副书记）
    {
        "person_a": 101,
        "person_b": 301,
        "type": "overlap",
        "context": "肖福凌任市委书记，周海波任市委副书记，长期在同一届常委会中共事",
        "overlap_org": "中共肇东市委员会",
        "overlap_period": "2026年",
    },
    # 肖福凌 — 李世玉（书记—常务副市长）
    {
        "person_a": 101,
        "person_b": 403,
        "type": "overlap",
        "context": "肖福凌任市委书记/市长，李世玉任市委常委、常务副市长，党政核心领导班子成员",
        "overlap_org": "肇东市人民政府",
        "overlap_period": "2026年",
    },
    # 肖福凌 — 姜涛（书记—纪委书记）
    {
        "person_a": 101,
        "person_b": 401,
        "type": "overlap",
        "context": "肖福凌任市委书记，姜涛任市委常委、纪委书记、监委主任",
        "overlap_org": "中共肇东市委员会",
        "overlap_period": "2026年",
    },
    # 周海波 — 姜涛（副书记—纪委书记）
    {
        "person_a": 301,
        "person_b": 401,
        "type": "overlap",
        "context": "同届市委常委会成员",
        "overlap_org": "中共肇东市委员会",
        "overlap_period": "2026年",
    },
    # 李世玉 — 单奎（常务副市长—副市长）
    {
        "person_a": 403,
        "person_b": 405,
        "type": "overlap",
        "context": "同为肇东市副市长，在政府领导班子中共事",
        "overlap_org": "肇东市人民政府",
        "overlap_period": "2026年",
    },
    # 吕鑫 — 人大全体（人大主任与各位副主任）
    {
        "person_a": 601,
        "person_b": 602,
        "type": "overlap",
        "context": "吕鑫任人大主任，张桂荣任副主任",
        "overlap_org": "肇东市人大常委会",
        "overlap_period": "",
    },
    {
        "person_a": 601,
        "person_b": 603,
        "type": "overlap",
        "context": "吕鑫任人大主任，葛刚任副主任",
        "overlap_org": "肇东市人大常委会",
        "overlap_period": "",
    },
    {
        "person_a": 601,
        "person_b": 604,
        "type": "overlap",
        "context": "吕鑫任人大主任，潘振生任副主任",
        "overlap_org": "肇东市人大常委会",
        "overlap_period": "",
    },
    {
        "person_a": 601,
        "person_b": 605,
        "type": "overlap",
        "context": "吕鑫任人大主任，臧艳华任副主任",
        "overlap_org": "肇东市人大常委会",
        "overlap_period": "",
    },
    # 田宇 — 政协副主席
    {
        "person_a": 701,
        "person_b": 702,
        "type": "overlap",
        "context": "田宇（主席候选人）与赵传虹（副主席）在政协领导班子中共事",
        "overlap_org": "肇东市政协",
        "overlap_period": "2026年",
    },
    {
        "person_a": 701,
        "person_b": 703,
        "type": "overlap",
        "context": "田宇（主席候选人）与惠涛（副主席）在政协领导班子中共事",
        "overlap_org": "肇东市政协",
        "overlap_period": "2026年",
    },
]

# ── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    run_build(
        slug="肇东市",
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print("Done: 肇东市 network built successfully.")
