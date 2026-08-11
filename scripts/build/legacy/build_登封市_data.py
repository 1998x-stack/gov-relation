#!/usr/bin/env python3
"""登封市领导班子工作关系网络数据生成脚本。

行政区划：河南省 郑州市 登封市（县级市）。
目标对象：市委书记 & 市长。

数据来源：
- 登封市人民政府门户网站 (dengfeng.gov.cn) 政府领导 / 政务要闻 / 政府工作报告 / 人事任免（info 截至 2026-08）
- 百度百科/AI 摘要（履历细节，plausible 置信度）
核心任职均以政府官网新闻稿确认。丁晓永其民族/出生/学历与部分干部详情源自百科，未完全独立核验者标为 plausible
或写入 report 与 person JSON 的 open_questions。

用法：
    python3 build_登封市_data.py
"""

import os
import sys

# 允许独立运行（仓库根目录 / scripts/build / data/tmp 均可）
_HERE = os.path.dirname(os.path.abspath(__file__))
for _p in (_HERE, os.path.join(_HERE, "..", ".."), os.path.join(_HERE, "..", "..", "..")):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import sqlite3  # noqa: E402  (process_tmp 校验 token)

from gov_relation.paths import DATABASE_DIR, GRAPH_DIR  # noqa: E402
from gov_relation.runner import run_build  # noqa: E402

slug = "登封市"

# ── 规范化路径（写往 data/database 与 data/graph；保留 DB_PATH/GEXF_PATH token 供 process_tmp 校验）──
DB_PATH = str(DATABASE_DIR / f"{slug}_network.db")
GEXF_PATH = str(GRAPH_DIR / f"{slug}_network.gexf")

# ── 组织 ─────────────────────────────────────────────────────────────
organizations = [
    {"id": 1, "name": "中共登封市委员会", "type": "党委", "level": "县级市", "parent": "河南省郑州市", "location": "登封市"},
    {"id": 2, "name": "登封市人民政府", "type": "政府", "level": "县级市", "parent": "河南省郑州市", "location": "登封市"},
    {"id": 3, "name": "登封市人民代表大会常务委员会", "type": "人大", "level": "县级市", "parent": "", "location": "登封市"},
    {"id": 4, "name": "中国人民政治协商会议登封市委员会", "type": "政协", "level": "县级市", "parent": "", "location": "登封市"},
    {"id": 5, "name": "中共登封市委政法委员会", "type": "党委部门", "level": "县级市", "parent": "中共登封市委员会", "location": "登封市"},
    {"id": 6, "name": "登封市公安局", "type": "政府部门", "level": "县级市", "parent": "登封市人民政府", "location": "登封市"},
    {"id": 7, "name": "登封市人民政府办公室", "type": "政府部门", "level": "县级市", "parent": "登封市人民政府", "location": "登封市"},
]

# ── 人员 ─────────────────────────────────────────────────────────────
persons = [
    # ── 现任市委书记 / 前任书记 ──
    {"id": 1, "name": "丁晓永", "gender": "男", "ethnicity": "回族", "birth": "1974-02", "birthplace": "河南襄城",
     "education": "研究生学历，河南大学管理学硕士", "party_join": "中共党员", "work_start": "1995-09",
     "current_post": "市委书记、市人武部党委第一书记", "current_org": "中共登封市委员会",
     "source": "https://www.dengfeng.gov.cn/zwyw/10183260.jhtml"},
    {"id": 2, "name": "辛绍河", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "郑州市人大常委会秘书长（前任登封市委书记）", "current_org": "郑州市人民代表大会常务委员会",
     "source": "https://www.dengfeng.gov.cn/（2022-10~2026年初任登封市委书记）"},

    # ── 市政府 ──
    {"id": 3, "name": "张增伟", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "市委副书记、市长、市政府党组书记", "current_org": "登封市人民政府",
     "source": "https://public.dengfeng.gov.cn/D13X/1910694.jhtml"},
    {"id": 4, "name": "张魁文", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "市委常委、市政府党组副书记、常务副市长", "current_org": "登封市人民政府",
     "source": "https://www.dengfeng.gov.cn/leader.jhtml"},
    {"id": 5, "name": "张哲飞", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "市委常委、市政府党组成员、副市长，市红十字会会长", "current_org": "登封市人民政府",
     "source": "https://www.dengfeng.gov.cn/leader.jhtml"},
    {"id": 6, "name": "郭衍昌", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "市政府党组成员、副市长，市公安局局长", "current_org": "登封市公安局",
     "source": "https://www.dengfeng.gov.cn/leader.jhtml"},
    {"id": 7, "name": "梁跃杰", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "市政府党组成员、副市长，市政府办公室党组书记、主任", "current_org": "登封市人民政府办公室",
     "source": "https://www.dengfeng.gov.cn/leader.jhtml"},
    {"id": 8, "name": "何亮", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "副市长", "current_org": "登封市人民政府",
     "source": "https://www.dengfeng.gov.cn/leader.jhtml"},
    {"id": 9, "name": "何文龙", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "副市长", "current_org": "登封市人民政府",
     "source": "https://www.dengfeng.gov.cn/leader.jhtml"},
    {"id": 10, "name": "王岑", "gender": "女", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "市政府党组成员、副市长", "current_org": "登封市人民政府",
     "source": "https://www.dengfeng.gov.cn/leader.jhtml"},

    # ── 市委其他领导班子 ──
    {"id": 11, "name": "康红阳", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "市委副书记", "current_org": "中共登封市委员会",
     "source": "https://baike.baidu.com/ 中国共产党登封市委员会（第六届）"},
    {"id": 12, "name": "刘宁", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "市委常委、副市长", "current_org": "中共登封市委员会",
     "source": "https://baike.baidu.com/ 中国共产党登封市委员会"},
    {"id": 13, "name": "柴春晓", "gender": "女", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "市委常委、政法委书记", "current_org": "中共登封市委政法委员会",
     "source": "https://baike.baidu.com/ 中国共产党登封市委员会"},
    {"id": 14, "name": "何聪道", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "市委常委", "current_org": "中共登封市委员会",
     "source": "https://baike.baidu.com/ 中国共产党登封市委员会"},

    # ── 前任市长（2024 年在任）──
    {"id": 15, "name": "陈耀宗", "gender": "男", "ethnicity": "汉族", "birth": "", "birthplace": "",
     "education": "", "party_join": "中共党员", "work_start": "",
     "current_post": "前任市长（2024 年任登封市市长）", "current_org": "登封市人民政府",
     "source": "https://www.dengfeng.gov.cn/zfgzbb/8283884.jhtml"},
]

# ── 任职 ─────────────────────────────────────────────────────────────
positions = [
    # 市委
    {"person_id": 1, "org_id": 1, "title": "市委书记", "start_date": "2026-03", "end_date": "", "rank": "正处级", "note": "2026-03 起任登封市委书记，兼人武部党委第一书记"},
    {"person_id": 2, "org_id": 1, "title": "市委书记（前任）", "start_date": "2022-10", "end_date": "2026-02", "rank": "正处级", "note": "2026-02 起不再担任；后任郑州市人大常委会秘书长"},
    {"person_id": 3, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "", "rank": "县级市", "note": ""},
    {"person_id": 3, "org_id": 2, "title": "市长", "start_date": "2025-02", "end_date": "", "rank": "正处级", "note": "2025-02 在登封市第六届人大五次会议当选"},
    {"person_id": 11, "org_id": 1, "title": "市委副书记", "start_date": "", "end_date": "", "rank": "县级市", "note": ""},
    {"person_id": 4, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "县级市", "note": ""},
    {"person_id": 4, "org_id": 2, "title": "常务副市长", "start_date": "", "end_date": "", "rank": "县级市", "note": "市政府党组副书记"},
    {"person_id": 5, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "县级市", "note": ""},
    {"person_id": 5, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "县级市", "note": "市红十字会会长"},
    {"person_id": 12, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "县级市", "note": ""},
    {"person_id": 13, "org_id": 5, "title": "政法委书记", "start_date": "", "end_date": "", "rank": "县级市", "note": "市委常委"},
    {"person_id": 14, "org_id": 1, "title": "市委常委", "start_date": "", "end_date": "", "rank": "县级市", "note": ""},
    {"person_id": 6, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "县级市", "note": ""},
    {"person_id": 6, "org_id": 6, "title": "市公安局局长", "start_date": "", "end_date": "", "rank": "县级市", "note": ""},
    {"person_id": 7, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "县级市", "note": "兼市政府办主任"},
    {"person_id": 7, "org_id": 7, "title": "市政府办公室主任", "start_date": "", "end_date": "", "rank": "县级市", "note": ""},
    {"person_id": 8, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "县级市", "note": ""},
    {"person_id": 9, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "县级市", "note": ""},
    {"person_id": 10, "org_id": 2, "title": "副市长", "start_date": "", "end_date": "", "rank": "县级市", "note": "女"},
    {"person_id": 15, "org_id": 2, "title": "市长（前任）", "start_date": "2022", "end_date": "2025-02", "rank": "正处级", "note": "2024-03 作政府工作报告；2025 由张增伟接任"},
]

# ── 关系 ─────────────────────────────────────────────────────────────
relationships = [
    {"person_a": 1, "person_b": 3, "type": "党政同僚", "context": "书记—市长党政正职搭档", "overlap_org": "中共登封市委员会", "overlap_period": "2026-03 至今"},
    {"person_a": 1, "person_b": 2, "type": "前任继任", "context": "辛绍河卸任后丁晓永接任登封市委书记", "overlap_org": "中共登封市委员会", "overlap_period": "2026-02/03 交接"},
    {"person_a": 3, "person_b": 15, "type": "前任继任", "context": "陈耀宗卸任后张增伟当选市长", "overlap_org": "登封市人民政府", "overlap_period": "2025-02 交接"},
    {"person_a": 1, "person_b": 11, "type": "上下级", "context": "书记—副书记", "overlap_org": "中共登封市委员会", "overlap_period": "2026-"},
    {"person_a": 3, "person_b": 4, "type": "上下级", "context": "市长—常务副市长（政府党组副书记）", "overlap_org": "登封市人民政府", "overlap_period": "2025-"},
    {"person_a": 1, "person_b": 4, "type": "上下级", "context": "书记—常务副市长", "overlap_org": "中共登封市委员会", "overlap_period": "2026-"},
    {"person_a": 4, "person_b": 5, "type": "同僚", "context": "常务副市长与常委副市长同级共事", "overlap_org": "登封市人民政府", "overlap_period": ""},
    {"person_a": 3, "person_b": 8, "type": "上下级", "context": "市长—副市长", "overlap_org": "登封市人民政府", "overlap_period": ""},
    {"person_a": 3, "person_b": 9, "type": "上下级", "context": "市长—副市长", "overlap_org": "登封市人民政府", "overlap_period": ""},
    {"person_a": 3, "person_b": 10, "type": "上下级", "context": "市长—副市长", "overlap_org": "登封市人民政府", "overlap_period": ""},
    {"person_a": 3, "person_b": 7, "type": "上下级", "context": "市长—副市长兼政府办主任", "overlap_org": "登封市人民政府", "overlap_period": ""},
    {"person_a": 1, "person_b": 13, "type": "上下级", "context": "书记—政法委书记", "overlap_org": "中共登封市委员会", "overlap_period": "2026-"},
]

if __name__ == "__main__":
    run_build(
        slug=slug,
        persons=persons,
        organizations=organizations,
        positions=positions,
        relationships=relationships,
        db_path=DB_PATH,
        gexf_path=GEXF_PATH,
        overwrite=True,
    )
    print(f"完成！DB: {DB_PATH}")
    print(f"GEXF: {GEXF_PATH}")
    print(f"人数: {len(persons)} | 组织数: {len(organizations)} | 任职数: {len(positions)} | 关系数: {len(relationships)}")